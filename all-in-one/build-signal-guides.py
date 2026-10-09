"""Read original XML pins/declarations into a static signal-use manual.

No simulator, PLC evaluation, source replacement or parameter write occurs.
Local names stay scoped to their block. Unresolved call directions stay pending.
"""
from pathlib import Path
from collections import defaultdict, Counter
import csv, hashlib, html, json, re, xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parent
native=json.loads((ROOT/'registers/program-model.json').read_text())
original={n['document_id']:n for n in json.loads((ROOT/'sources/decoded-original/network-map.json').read_text())}
specs={s['id']:s for s in json.loads((ROOT/'registers/control-spec.json').read_text())['specifications']}
circuits=json.loads((ROOT/'registers/electrical-trace.json').read_text())
symbols=list(csv.DictReader((ROOT/'registers/plc-symbols.csv').open(encoding='utf-8-sig')))
e=lambda v:html.escape(str(v))
canon=lambda v:str(v).replace('"','').casefold()
normalized=lambda v:re.sub(r'[^a-z0-9]','',canon(v))
local=lambda x:x.tag.rsplit('}',1)[-1]
def literal(v):
    return bool(v and (v.upper() in ('TRUE','FALSE') or re.fullmatch(r'[+-]?\d+(?:\.\d+)?|(?:2|8|10|16)#[0-9A-Fa-f]+',v) or v.upper().startswith(('S5T#','T#','TIME#'))))
def walk(v):
    if isinstance(v,dict):
        yield v
        for x in v.values():yield from walk(x)
    elif isinstance(v,list):
        for x in v:yield from walk(x)
def expression(v):
    op=v.get('op')
    if op=='const':return str(v.get('literal','1' if v['value'] is True else '0' if v['value'] is False else v['value']))
    if op=='read':return v['name']
    if op=='unknown':return '[미확인: '+v['reason']+']'
    if op=='not':return 'NOT ('+expression(v['arg'])+')'
    if op in ('and','or'):
        values=[expression(x) for x in v['args']]
        if op=='and':values=[x for x in values if x!='1']
        return '('+(' AND ' if op=='and' else ' OR ').join(dict.fromkeys(values))+')' if len(values)>1 else values[0] if values else '1'
    return '('+expression(v['left'])+' '+{'eq':'=','ne':'<>','gt':'>','ge':'>=','lt':'<','le':'<='}.get(op,op)+' '+expression(v['right'])+')'
def single_source(v):
    if v.get('op')=='read':return (v['name'],False)
    if v.get('op')=='not':
        r=single_source(v['arg']);return (r[0],not r[1]) if r else None
    if v.get('op')=='and':
        args=[x for x in v['args'] if not (x.get('op')=='const' and x.get('value') is True)]
        return single_source(args[0]) if len(args)==1 else None
    return None
declaration_cache={}
def declaration(n,uid):
    r=original[n['id']]['resolved_operands'].get(uid)
    if not r:return []
    result=[]
    for f in r['identifier_files']:
        if f not in declaration_cache:
            rows=[]
            for node in ET.parse(ROOT/'sources/decoded-original'/f).getroot():
                ident=next((x for x in node if local(x)=='ID'),None)
                if ident is not None:
                    for c in ident.iter():
                        if local(c)=='C':rows.append((ident.get('RID'),c.get('UID'),c.get('NID'),dict(kind=local(node),scope=ident.get('S'),access_kind=c.get('AK'),file='sources/decoded-original/'+f)))
            declaration_cache[f]=rows
        result.extend(v for rid,u,nid,v in declaration_cache[f] if rid==r['ref_id'] and u==uid and nid==original[n['id']]['inferred_original_nid'])
    return result
def role(gate,pin,decl):
    if gate in ('Contact','PContact') and pin=='operand':return 'read','접점 operand'
    if gate in ('Coil','SCoil','RCoil','SdCoil') and pin=='operand':return 'write','코일 operand'
    if gate=='SdCoil' and pin=='value':return 'read','타이머 설정 value'
    if gate=='Move' and pin=='in':return 'read','Move in'
    if gate=='Move' and re.fullmatch(r'out\d*',pin):return 'write','Move out'
    if gate in ('Add','Sub','Mul','Div','Convert'):
        if re.fullmatch(r'in\d*',pin):return 'read','연산 입력 핀'
        if re.fullmatch(r'out\d*',pin):return 'write','연산 출력 핀'
    if gate in ('Eq','Ne','Lt','Le','Gt','Ge') and re.fullmatch(r'in\d+',pin):return 'read','비교 입력 핀'
    if decl and all(d['access_kind']=='Write' for d in decl):return 'write','식별 원본 AK=Write · 호출 방향/인터페이스 추가 확인'
    return 'pending','호출 방향·미분류 핀 확인 필요'

usages=[];by_name=defaultdict(list);unresolved=[];transfers=[]
for n in native['networks']:
    tree=ET.parse(ROOT/n['file']).getroot()
    parts={x.get('UId'):x.get('Gate') for x in tree.iter() if local(x)=='Part'}
    for w in tree.iter():
        if local(w)!='Wire':continue
        for ref in (x for x in w if local(x)=='OCon'):
            uid=ref.get('UId');name=n['refs'].get(uid,{}).get('name')
            if literal(name):continue
            decl=declaration(n,uid);scopes={d['scope'] for d in decl}
            scope='Global' if scopes=={'Global'} else 'Local' if scopes=={'Local'} else 'Unknown'
            identity=(canon(name) if scope=='Global' else n['block']+'::'+canon(name)) if name else None
            for p in (x for x in w if local(x)=='PCon'):
                gate=parts.get(p.get('UId'),'CRef');pin=p.get('PinName');access,basis=role(gate,pin,decl)
                row=dict(network=n['id'],block=n['block'],title=n['title'],file=n['file'],wire=w.get('UId'),oref=uid,part=p.get('UId'),gate=gate,pin=pin,name=name,identity=identity,scope=scope,role=access,role_basis=basis,declarations=decl,legacy_simulation_block=canon(n['block'])=='simulation')
                usages.append(row)
                if name:by_name[canon(name)].append(row)
                else:unresolved.append(row)
    for a in n['actions']:
        src=single_source(a['condition']) if a['gate']=='Coil' else single_source(a['value']) if a['gate']=='Move' and 'value' in a else None
        if src:transfers.append(dict(network=n['id'],block=n['block'],file=n['file'],part=a['uid'],gate=a['gate'],source=src[0],inverted=src[1],target=a['name'],condition=expression(a['condition']),legacy_simulation_block=canon(n['block'])=='simulation'))

devices=[]
for d in circuits['devices']:
    id=d['id'];spec=specs[id];nets=set(native['equipment'].get(id,{}).get('networks',[]))|set(d['networks'])
    seeds={canon(s['원본 심볼']) for key in ('inputs','outputs','internal') for s in spec[key]}
    seeds|={canon(p['backup'].split(' / ',1)[1]) for p in d['paths'] if p['backup']}
    seeds|={canon(r['name']) for n in native['networks'] if n['id'] in nets for r in n['refs'].values() if r['name'] and normalized(id) in normalized(r['name']) and not literal(r['name'])}
    connected={canon(t[key]) for t in transfers if canon(t['source']) in seeds or canon(t['target']) in seeds for key in ('source','target')}
    seeds|=connected-{'on','off','reset_allarm','simulation(1)'}
    signals=[]
    for name in sorted(seeds):
        rows=by_name.get(name,[]);global_rows=[r for r in rows if r['scope']=='Global'];writers=[r for r in global_rows if r['role']=='write']
        addresses=[s['백업 주소'].upper() for s in symbols if canon(s['원본 심볼'])==name]
        signals.append(dict(name=rows[0]['name'] if rows else name,addresses=addresses,usages=rows,global_writes=len(writers),global_write_networks=sorted({r['network'] for r in writers}),local_or_unknown_scope_count=sum(r['scope']!='Global' for r in rows),direct_reference_missing=not rows))
    devices.append(dict(id=id,title=d['title'],signals=signals,networks=sorted(nets),transfers=[t for t in transfers if canon(t['source']) in seeds or canon(t['target']) in seeds],unresolved_usages=[r for r in unresolved if r['network'] in nets],field_verified=False))
main_calls=[c for c in native['calls'] if c['caller']=='main' and canon(c['callee']) in ('simulation','hmi inputs','hmi output','motors 1','r1 scraps gate 2','burner control','valve control loop')]
record=dict(date='2026-10-07',scope='original XML pins and declaration scope; static source analysis only',source='sources/decoded-original/network-map.json',source_sha256=hashlib.sha256((ROOT/'sources/decoded-original/network-map.json').read_bytes()).hexdigest(),source_networks=426,usage_count=len(usages),role_counts=dict(Counter(r['role'] for r in usages)),unresolved_usage_count=len(unresolved),local_usages_separated=sum(r['scope']=='Local' for r in usages),devices=devices,usages=usages,transfers=transfers,main_calls=main_calls,plc_changes=0,field_verified=0,simulator_behavior_tests='not_rerun')
(ROOT/'registers/signal-trace.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
with (ROOT/'registers/signal-usages.csv').open('w',encoding='utf-8-sig',newline='') as f:
    cols=['network','block','name','scope','role','role_basis','wire','oref','part','gate','pin','file'];w=csv.DictWriter(f,fieldnames=cols,extrasaction='ignore');w.writeheader();w.writerows(usages)
def table(headers,rows):return '<div class="table-wrap"><table><thead><tr>'+''.join('<th>'+e(h)+'</th>' for h in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+c+'</td>' for c in row)+'</tr>' for row in rows)+'</tbody></table></div>'
def net(n):return '<a href="../networks/network-'+str(n)+'.html">원본 '+str(n)+'</a>'
def loc(r):return e(r['block'])+' · '+net(r['network'])+'<br>Wire '+e(r['wire'])+' · ORef '+e(r['oref'])+' · Part '+e(r['part'])+'.'+e(r['pin'])
def location_table(rows):return table(['역할·범위','원본 핀 근거','블록·위치'],[[e({'read':'읽기','write':'쓰기','pending':'방향 미확정'}[r['role']])+' · '+e(r['scope'])+'<br>'+e(r['role_basis']),e(r['gate'])+'.'+e(r['pin'])+('<br>백업 Simulation 블록' if r['legacy_simulation_block'] else ''),loc(r)] for r in rows])
out=ROOT/'signal-guides';out.mkdir(exist_ok=True)
guard='<div class="notice">원본 호출1612는 Simulation(1),1613의 HMI Inputs는 NOT Simulation(1)과 앞 호출 ENO 경로를 사용합니다. 백업 심볼은 %M180.0입니다. ENO 해석·현재 모드·전체 실행은 확인 전이며 두 블록이 동시에 쓰는 것으로 단정하지 않습니다. 백업 Simulation 블록의 정적 참조이며 새 시뮬레이터 실행·시험은 하지 않았습니다.</div>'
for d in devices:
    id=d['id'];multi=[s for s in d['signals'] if s['global_writes']>1]
    body='<h1>'+e(id+' · 신호 전달·복수 쓰기 분석')+'</h1><div class="notice info">원본 XML 핀과 식별 자료의 Global/Local 범위를 대조한 정적 작업지입니다. 읽기·쓰기 위치는 현재 호출·실행 순서·정상 극성·실제 값을 확정하지 않습니다. 이름만 같은 로컬 변수는 블록별로 구분합니다.</div><nav class="inline-actions"><a href="../circuit-guides/'+id+'.html">전기 회로 추적</a><a href="../construction-guides/'+id+'.html">시공 케이블 경로</a><a href="../procedures/'+id+'.html">진단·수리 작업지</a><a href="../signal-trace.html">전체 신호 분석 목록</a><a href="#multiple">복수 쓰기</a><a href="#transfer">직접 전달</a><a href="#signals">신호별 원본 위치</a></nav>'+guard
    body+='<h2 id="multiple">1. 같은 전역 신호의 쓰기 위치</h2><p>같은 네트워크의 Set/Reset도 별도 위치입니다. 복수 쓰기는 확인 대상이며 오류 판정이 아닙니다. Global 범위가 확인된 동일 이름만 합산합니다.</p>'+table(['신호·백업 주소','쓰기 Part/네트워크','쓰기 위치'],[[e(s['name'])+'<br>'+e(' / '.join(s['addresses']) or 'DB/주소 별도 확인'),e(str(s['global_writes'])+'곳 / '+str(len(s['global_write_networks']))+'개 네트워크'),'<details><summary>위치 펼치기</summary>'+location_table([r for r in s['usages'] if r['scope']=='Global' and r['role']=='write'])+'</details>'] for s in multi])
    body+='<h2 id="transfer">2. 단일 신호 전달·반전</h2><p>단일 읽기에서 Coil 또는 Move로 이어지는 확인 가능한 경로입니다. 아래 조건과 현재 호출을 함께 확인하며 일반 논리식·호출 인자를 단순 전달로 바꾸지 않습니다.</p>'+table(['읽기 → 쓰기','명령·반전·조건','원본'],[[e(t['source'])+' → '+e(t['target']),e(t['gate']+' / '+('NOT 반전' if t['inverted'] else '단일 전달'))+'<br><code>'+e(t['condition'])+'</code>',e(t['block'])+' · '+net(t['network'])+' · Part '+e(t['part'])] for t in d['transfers']])
    body+='<h2 id="signals">3. 신호별 원본 위치</h2><p>'+str(len(d['signals']))+'개 이름을 선택했습니다. 참조가 없는 심볼은 미사용으로 확정하지 않으며 미복원 자료·간접 접근·현재 프로그램을 추가 확인합니다.</p>'
    for i,s in enumerate(d['signals'],1):
        body+='<details id="signal-'+str(i)+'"><summary>'+e(s['name'])+' · '+e(' / '.join(s['addresses']) or '내부/주소 확인')+' · 쓰기 '+str(s['global_writes'])+'곳</summary>'+(location_table(s['usages']) if s['usages'] else '<p>복원 원본에서 같은 이름의 직접 핀 참조를 찾지 못했습니다.</p>')+'</details>'
    body+='<h2>4. 관련 호출 조건</h2>'+table(['main 호출','원본·Call UID','정적 허가'],[[e(c['caller']+' → '+str(c['callee'])),net(c['network'])+' · CRef '+e(c['uid']),'<code>'+e(expression(c['enable']))+'</code>'] for c in main_calls])
    body+='<h2>5. 관련 미해석 피연산자</h2><p>아래는 관련 네트워크의 공유 미해석 위치이며 이 장치 전용 신호라고 단정하지 않습니다. 방향·이름·블록 인터페이스가 미확정인 참조는 읽기 또는 False로 치환하지 않습니다.</p><details><summary>'+str(len(d['unresolved_usages']))+'개 핀 위치 펼치기</summary>'+location_table(d['unresolved_usages'])+'</details><h2>6. 수리·개선 확인 기록</h2><ol><li>현장 입력·처리된 Inputs·요청 Flag·실제 출력·응답·알람을 별도로 기록합니다.</li><li>동일 신호의 모든 쓰기 Part와 main 허가·호출 경로를 대조합니다.</li><li>리셋·새 운전 요청·자동 시퀀스·전원 재시작의 값 유지 여부를 현재 PLC/TIA에서 확인합니다.</li><li>원본 이름·주소·범위와 관찰 사실을 기록한 뒤 변경 후보를 검토합니다.</li></ol>'
    (out/(id+'.html')).write_text('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+id+' 신호 전달 분석</title><link rel="stylesheet" href="../assets/all-in-one.css"></head><body><main style="max-width:1240px;margin:auto;padding:24px">'+body+'</main></body></html>')
body='<h1>PLC 신호 전달·복수 쓰기 분석</h1><div class="notice">426개 원본 XML의 '+str(len(usages))+'개 비상수 핀 참조를 대조했습니다. 장치'+str(len(devices))+'개 작업지에 전역/로컬 범위·단일 전달·반전·쓰기 위치·미해석 참조를 연결했습니다. 현장 검증·PLC 변경0건, 시뮬레이터 개발·시험 중지 상태입니다.</div><nav class="inline-actions">'+''.join('<a href="signal-guides/'+d['id']+'.html">'+e(d['id']+' · '+d['title'])+'</a>' for d in devices)+'</nav>'+guard+'<p><a href="registers/signal-trace.json">정적 근거 JSON</a> · <a href="registers/signal-usages.csv">핀 사용 CSV</a> · <a href="electrical-trace.html">전기 회로 목록</a></p>'
(ROOT/'signal-trace.html').write_text('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>PLC 신호 전달 분석</title><link rel="stylesheet" href="assets/all-in-one.css"></head><body><main style="max-width:1240px;margin:auto;padding:24px">'+body+'</main></body></html>')
print(json.dumps({k:record[k] for k in ['source_networks','usage_count','role_counts','unresolved_usage_count','local_usages_separated']}|dict(device_guides=len(devices),simulator_behavior_tests='not_rerun'),ensure_ascii=False))
