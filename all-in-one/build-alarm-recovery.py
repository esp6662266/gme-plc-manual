"""Native-source motor/actuator alarm manuals. No control evaluation or PLC writes."""
from pathlib import Path
from collections import Counter
import hashlib, html, json, xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parent
load=lambda f:json.loads((ROOT/f).read_text())
sha=lambda f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest()
local=lambda x:x.tag.rsplit('}',1)[-1]
canon=lambda s:str(s).replace('"','').casefold()
e=lambda s:html.escape(str(s))
model=load('registers/program-model.json')
trace=load('registers/signal-trace.json')
repair=load('registers/repair-decision.json')
nets={n['id']:n for n in model['networks']}
source_map={n['document_id']:n for n in load('sources/decoded-original/network-map.json')}
declarations=load('sources/decoded-original/identifier-declarations.json')
focus={'BC01':[1785,1786],'FN04':[1809],'RD01':[1787],'MC04':[1791],
       'VS01':[1794],'FN01':[1798],'FN02':[1796],'FN03':[1801],'FN06':[1802],
       'PV01':[1815,1816],'PV02':[1817,1818],
       'MV01':[1226,1714],'MV03':[1226,1714],'MV06':[1226,1714]}
motor_ids=list(focus)[:9]
selected_alarms={'MV01':['Allarm.MV01_FAULT'],'MV03':['Allarm.MV03_FAULT'],'MV06':['Allarm.MV_06_FAULT']}
selected_timers={'MV01':['Tag_92'],'MV03':['Tag_94'],'MV06':['Tag_97']}
context_nets={'PV01':[1921,1922],'PV02':[1923,1924]}
context_names={'MV01':['WorkData.W33','WorkData.W34'],'MV03':['WorkData.W29','WorkData.W30'],'MV06':['WorkData.W19','WorkData.W20']}
notes={
 'BC01':'1786 트립와이어 래치의 Reset에는 NOT Inputs.BC01 trip wire가 명시됩니다. 1785의 운전/인버터 고장 Reset에는 같은 원인 정상화 접점이 명시되지 않습니다. 트립와이어와 근접 운전 응답을 구분합니다.',
 'FN04':'17초 감시의 운전 응답과 인버터 이상 분기는 같은 Tag_74를 읽습니다. 공동 인버터의 M31/M36 두 모터·90분 연관 정지·설정 제한/0 요청 해제를 별도로 확인합니다.',
 'RD01':'5초 감시는 RD01 구동부 참고입니다. 킬른 본체의 정상 상태나 원료 투입 허가, 별도 냉각팬의 응답으로 대신 판단하지 않습니다.',
 'MC04':'5초 감시와 VS01 응답에 의한 요청 해제는 서로 다른 원본 경로입니다. Allarm.Maintenance_ON과 Flag.Maintenance_ON을 합치지 않습니다.',
 'VS01':'2초 감시는 공통 인버터 응답 자료입니다. 두 진동 모터의 실제 상태와 별도 브레이크 OFF 경로를 구분합니다.',
 'FN01':'1798의2초 기동 감시와1950의1시간30분 예경보/Local Stop_Fan_FN01 경로를 구분합니다. 베어링·진동·VR01/VR02 상태와 보조 냉각팬은 별도 확인 대상입니다.',
 'FN02':'2초 감시와 풍량 설정0에 의한 요청 해제를 구분합니다. 제목이FN02인 변환 네트워크가 실제FN04 신호를 읽는 불일치도 함께 확인합니다.',
 'FN03':'Tag_66에는35초 SD 두 곳이 있습니다. 운전/인버터 고장의Set은 다르며 인버터 고장Set에는Tag_66 접점이 없습니다. 펄스·Memo_M25_Running과TOR/RUN 전달을 함께 확인합니다.',
 'FN06':'2초 감시의 원본 래치 이름은 Allarm.MBVA01_FAULT입니다. FN06 별칭 관계는 확인 전이며 RD01 응답 상실에 의한 요청 해제와 구분합니다.',
 'PV01':'열림·닫힘 감시의 원본 설정은 A 게이트 4초, B 게이트 7초입니다. 감시는 실제 센서와 구분되는 MEM_OPEN/CLOSE를 읽습니다. 출력 0의 닫힘 감시·EV 직접 응답·처리 Inputs·startup 닫힘 기억을 각각 확인합니다.',
 'PV02':'열림·닫힘 감시의 원본 설정은 A·B 게이트 모두 7초입니다. 감시 입력은 MEM_OPEN/CLOSE이며 명령 반전의 닫힘 감시를 별도로 봅니다. MC04 응답·자동 허가와 실제 위치를 구분합니다.',
 'MV01':'원본 1226의 방향 응답 감시(Tag_92, S5T#150mS)와 1714의 W33>2000 / W34<-2000은 같은 고장 래치를 Set합니다. 비교 후 오차값에 0을 쓰는 Move와 래치 Reset은 서로 다른 명령입니다. 수치의 물리 단위·현재 교정은 확인 전입니다.',
 'MV03':'원본 1226의 방향 응답 감시 Tag_94는 S5T#150S로, MV01·MV06의 150ms 표기와 다릅니다. 현재 TIA의 시간 설정과 제작사 의도를 확인합니다. 원본 1714의 W29>3400 / W30<-3400과 오차값 0 쓰기를 분리하고 버너 세정·기동 연동도 확인합니다.',
 'MV06':'원본 1226의 방향 응답 감시(Tag_97, S5T#150MS)와 1714의 W19>2200 / W20<-2200을 구분합니다. 1711의 반전 ON 출력 조건·실물 리미트 명칭·TM 엔코더 주소는 확인 전입니다. 공유 래더의 다른 댐퍼를 이 설비에 배정하지 않습니다.',
}

def expression(v):
    op=v['op']
    if op=='read':return v['name']
    if op=='const':return str(v.get('literal',v.get('value')))
    if op=='unknown':return '[원본 추가 해석: '+v['reason']+']'
    if op=='not':return 'NOT ('+expression(v['arg'])+')'
    if op in ('and','or'):
        args=[a for a in v['args'] if not(op=='and' and a.get('op')=='const' and a.get('value') is True)]
        return '('+(' AND ' if op=='and' else ' OR ').join(expression(a) for a in args)+')'
    if op in ('eq','ne','gt','ge','lt','le'):
        return '('+expression(v['left'])+' '+{'eq':'=','ne':'<>','gt':'>','ge':'>=','lt':'<','le':'<='}[op]+' '+expression(v['right'])+')'
    return json.dumps(v,ensure_ascii=False)

def native(network):
    n=nets[network];root=ET.parse(ROOT/n['file']).getroot()
    parts=[dict(uid=p.get('UId'),gate=p.get('Gate'),negated_pins=[x.get('PinName') for x in p if local(x)=='Negated']) for p in root.iter() if local(p)=='Part']
    refs={x.get('UId'):dict(ref_id=x.get('RefId'),name=n['refs'].get(x.get('UId'),{}).get('name')) for x in root.iter() if local(x)=='ORef'}
    wires=[dict(uid=w.get('UId'),endpoints=[dict(kind=local(x),uid=x.get('UId'),pin=x.get('PinName')) for x in w]) for w in root.iter() if local(w)=='Wire']
    return dict(network=network,block=n['block'],network_index=n['index'],title=n['title'],file=n['file'],sha256=sha(n['file']),parts=parts,refs=refs,wires=wires)

def upstream(proof,uid):
    # Only follow connected static input wires; this is a reference graph, not logic execution.
    seen=set();pending=[uid];parts={p['uid']:p for p in proof['parts']};contacts=[]
    while pending:
        current=pending.pop()
        if current in seen:continue
        seen.add(current)
        if parts[current]['gate'] in ['Contact','PContact','NContact']:
            for w in proof['wires']:
                if any(x['kind']=='PCon' and x['uid']==current and x['pin']=='operand' for x in w['endpoints']):
                    for x in w['endpoints']:
                        if x['kind']=='OCon':contacts.append(dict(part=current,gate=parts[current]['gate'],negated_pins=parts[current]['negated_pins'],wire=w['uid'],oref=x['uid'],**proof['refs'][x['uid']]))
        for w in proof['wires']:
            if any(x['kind']=='PCon' and x['uid']==current and x['pin'] and (x['pin'] in ['in','pre','en'] or x['pin'].startswith('in') and x['pin'][2:].isdigit()) for x in w['endpoints']):
                pending.extend(x['uid'] for x in w['endpoints'] if x['kind']=='PCon' and x['pin']=='out')
    reference_pins=[]
    for w in proof['wires']:
        for pin in w['endpoints']:
            if pin['kind']=='PCon' and pin['uid'] in seen:
                for x in w['endpoints']:
                    if x['kind']=='OCon':reference_pins.append(dict(part=pin['uid'],gate=parts[pin['uid']]['gate'],pin=pin['pin'],wire=w['uid'],oref=x['uid'],**proof['refs'][x['uid']]))
    return dict(parts=sorted(seen,key=int),contacts=contacts,reference_pins=reference_pins)

source_paths={'registers/program-model.json','registers/signal-trace.json','registers/repair-decision.json',
              'sources/decoded-original/network-map.json','sources/decoded-original/identifier-declarations.json'}
profiles=[]
for device,network_ids in focus.items():
    r=next(r for r in repair['records'] if r['plc_id']==device)
    proofs=[native(n) for n in network_ids+context_nets.get(device,[])];by_net={p['network']:p for p in proofs}
    source_paths.update(p['file'] for p in proofs)
    alarms=[];timers=[]
    names=list(dict.fromkeys(a['name'] for n in network_ids for a in nets[n]['actions'] if a['gate']=='SCoil' and a['name'].startswith('Allarm.')))
    if device in selected_alarms:names=selected_alarms[device]
    for name in names:
        uses=[u for u in trace['usages'] if u['scope']=='Global' and canon(u['name'])==canon(name)]
        writers=[u for u in uses if u['role']=='write']
        source_paths.update(u['file'] for u in uses)
        source_paths.update(d['file'] for u in uses for d in u['declarations'])
        actions=[dict(network=n,**a,native_upstream=upstream(by_net[n],a['uid'])) for n in network_ids for a in nets[n]['actions'] if a['name']==name]
        assert {a['gate'] for a in actions}=={'SCoil','RCoil'},(device,name)
        alarms.append(dict(name=name,actions=actions,usages=uses,all_static_writers=writers,
            other_scope_usages=[u for u in trace['usages'] if canon(u['name'])==canon(name) and u['scope']!='Global']))
    for n in network_ids:
        for a in nets[n]['actions']:
            if a['gate']=='SdCoil' and (device not in selected_timers or a['name'] in selected_timers[device]):
                proof=upstream(by_net[n],a['uid'])
                value=next(x for x in proof['reference_pins'] if x['part']==a['uid'] and x['pin']=='value')
                decl=[d for d in declarations if d['uid']==value['oref'] and d['rid']==value['ref_id'] and d['nid']==source_map[n]['inferred_original_nid'] and d['name']==value['name']]
                assert decl and value['name']==a['preset']['literal'],(device,n,a['uid'])
                source_paths.update('sources/decoded-original/'+d['file'] for d in decl)
                timers.append(dict(network=n,**a,native_upstream=proof,value_declarations=decl))
    contexts=[dict(network=n,**a,native_upstream=upstream(by_net[n],a['uid'])) for n in context_nets.get(device,network_ids if device in context_names else []) for a in nets[n]['actions'] if (device not in context_names or a['name'] in context_names[device])]
    profiles.append(dict(id=device,priority_key=r['key'],name=r['name'],boundary=r['boundary'],note=notes[device],
        family='motor' if device in motor_ids else 'gate' if device.startswith('PV') else 'damper',
        source_networks=network_ids,native_networks=proofs,alarms=alarms,timers=timers,
        context_actions=contexts,
        request_reset_actions=r['request_reset_actions'],field_verified=False,tia_verified=False,repairs_completed=0))
data=dict(date='2026-10-08',scope='Native static alarm, timer and reset reference manuals; no execution',
    profiles=profiles,sources={p:sha(p) for p in sorted(source_paths)},field_verified=0,tia_verified=0,
    plc_changes=0,simulator_development='stopped_by_user',simulator_behavior_tests='not_rerun')
(ROOT/'registers/alarm-recovery.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
out=ROOT/'alarm-guides';out.mkdir(exist_ok=True)
def link(label,path,prefix='../'):
    assert (ROOT/path.split('#')[0]).is_file(),path
    return '<a href="'+prefix+e(path)+'">'+e(label)+'</a>'
def netlink(n,uid=None,prefix='../'):
    return link('원본 '+str(n),'networks/network-'+str(n)+'.html',prefix)+(' · Part '+e(uid) if uid else '')
def table(headers,rows):
    return '<div class="table-wrap"><table><thead><tr>'+''.join('<th>'+e(h)+'</th>' for h in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+str(v)+'</td>' for v in row)+'</tr>' for row in rows)+'</tbody></table></div>'
def page(title,body,prefix='../'):
    return '<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+e(title)+'</title><link rel="stylesheet" href="'+prefix+'assets/all-in-one.css"><style>td code{white-space:normal;overflow-wrap:anywhere}td{vertical-align:top}</style></head><body><main style="max-width:1240px;margin:auto;padding:24px"><h1>'+e(title)+'</h1>'+body+'</main></body></html>'
notice='<div class="notice">원본 백업의 정적 알람·타이머·리셋 근거입니다. 현재값·실물 동일성·현재 CPU/TIA 실행·복구 완료는 확인 전입니다. 원본 설정은 권장 보호값이나 실제 경과시간을 뜻하지 않습니다. PLC 변경0건, 시뮬레이터 작성·시험 중지.</div>'
for p in profiles:
    body=notice+'<nav class="inline-actions"><a href="../alarm-recovery.html">알람·복구 전체 비교</a>'+link('수리 판단','repair-guides/'+p['priority_key']+'.html')+link('전기 회로','circuit-guides/'+p['id']+'.html')+link('신호 전달·다른 쓰기','signal-guides/'+p['id']+'.html')+link('수리 관찰 기록','index.html#view=repair-record&equipment='+p['priority_key']+'&scope=priority')+'</nav><p>'+e(p['note'])+'</p>'
    body+='<h2 id="alarms">1. 발생·리셋 조건 비교</h2><p>Set은 래치 발생 조건, Reset은 래치 해제 조건입니다. 아래 식은 기존 원본 분석의 정적 요약이며 1/ON을 현재 상수로 보지 않습니다. 원인 해소·리셋 명령·래치 해제·새 운전 요청·실제 응답을 각각 확인합니다.</p>'
    body+=table(['원본 래치','Set 전체 정적 조건','Reset 전체 정적 조건','원본 위치'],[[e(a['name']),'<br>'.join('<code>'+e(expression(x['condition']))+'</code>' for x in a['actions'] if x['gate']=='SCoil'),'<br>'.join('<code>'+e(expression(x['condition']))+'</code>' for x in a['actions'] if x['gate']=='RCoil'),'<br>'.join(e(x['gate'])+' · '+netlink(x['network'],x['uid']) for x in a['actions'])] for a in p['alarms']])
    body+='<p>Reset 조건에 원인 입력의 정상화 접점이 명시되는지 아래 원본 접점표와 대조합니다. 명시되지 않은 경우에도 현재 호출·다른 쓰기·기억 상태를 확인하기 전에는 즉시 재발·리셋 우선순위·재기동을 확정하지 않습니다.</p>'
    body+='<h2 id="timers">2. 감시 타이머와 분기</h2>'+table(['타이머·명령','원본 시간 설정','정적 입력 조건','근거'],[[e(t['name']+' / '+t['gate']),'<code>'+e(expression(t['preset']))+'</code>','<code>'+e(expression(t['condition']))+'</code>',netlink(t['network'],t['uid'])+'<br>'+', '.join(link('시간 원본 선언 UID '+d['uid']+' / RID '+d['rid'],'sources/decoded-original/'+d['file']) for d in t['value_declarations'])] for t in p['timers']])
    if p['family']=='damper':body+='<p>150mS/150MS와150S의 원본 단위를 보존합니다. 값의 의도·현재 CPU 설정·원시 응답→Inputs 전달을 확인하기 전에는 감시 시간을 바꾸거나 실제 검출 시간으로 확정하지 않습니다.</p>'
    body+='<h2 id="contacts">3. Set/Reset 앞의 실제 연결 접점</h2><p>각 명령의 입력 배선을 역으로 따라간 접점 목록입니다. 목록의 행 순서는 실행 순서가 아닙니다. 직렬/병렬 전체 연결은 아래 원본 Wire 표와 래더 페이지에서 확인합니다. 접점 이름은 물리 센서·처리 Inputs·타이머·내부 래치가 혼재하므로 정상 극성을 따로 확인합니다.</p>'
    body+=table(['명령·대상','연결 접점·원본 이름','반전·원본 식별'],[[e(x['gate']+' / '+a['name'])+'<br>'+netlink(x['network'],x['uid']),'<br>'.join(e(c['gate']+' '+str(c['name'])) for c in x['native_upstream']['contacts']),'<br>'.join(e('Part '+c['part']+' / Negated '+(','.join(c['negated_pins']) or '없음')+' / ORef '+c['oref']+' / RefId '+str(c['ref_id'])+' / Wire '+c['wire']) for c in x['native_upstream']['contacts'])] for a in p['alarms'] for x in a['actions']])
    if p['family']=='damper':
        body+=link('엔코더 실제 위치와 방향 명령 누적 감시의 차이','encoder-position.html#position-'+p['id'])
        body+='<h3>방향 명령 누적값 비교의 피연산자</h3>'+table(['고장 쓰기·원본','비교 명령·연결 피연산자','배선 식별'],[[e(a['name'])+'<br>'+netlink(x['network'],x['uid']),'<br>'.join(e(c['gate']+' / '+c['pin']+' / '+str(c['name'])) for c in x['native_upstream']['reference_pins'] if c['gate'] in ['Gt','Lt']),'<br>'.join(e('Part '+c['part']+' / ORef '+c['oref']+' / RefId '+str(c['ref_id'])+' / Wire '+c['wire']) for c in x['native_upstream']['reference_pins'] if c['gate'] in ['Gt','Lt'])] for a in p['alarms'] for x in a['actions'] if x['network']==1714])
    if p['context_actions']:
        body+='<h2 id="context">위치 기억·방향 누적값 쓰기의 경계</h2><p>'+('MEM_OPEN/CLOSE는 명령과 직접 EV 응답·처리 Inputs로 Set/Reset되는 기억입니다. 센서 자체나 현재 위치로 대신 표시하지 않습니다. startup의 닫힘 기억 초기화도 현재 유지 상태와 함께 확인합니다.' if p['family']=='gate' else '같은 비교 조건으로 방향 명령 누적값에0을 쓰는Move가 있습니다. 누적값0은 고장 래치Reset·실제 위치 정상·교정 완료의 증거가 아닙니다. 공유 네트워크의 같은 스캔 실행 순서와 다른 쓰기는 확인 전입니다.')+'</p>'+table(['명령·대상','전체 정적 조건','원본 전달값','근거'],[[e(x['gate']+' / '+x['name']),'<code>'+e(expression(x['condition']))+'</code>',e(expression(x['value'])) if 'value' in x else '',netlink(x['network'],x['uid'])] for x in p['context_actions']])
    body+='<h2 id="request">4. 요청 해제와 재기동 경계</h2>'
    if p['request_reset_actions']:
        body+=table(['요청 해제','전체 정적 조건','근거'],[[e(a['gate']+' / '+a['name']),'<code>'+e(expression(a['condition']))+'</code>',netlink(a['network'],a['uid'])] for a in p['request_reset_actions']])
    else:body+='<p>기존 수리 판단 대장에 직접 배정된 요청RCoil은 없습니다. 자동 허가·단계·출력·위치 기억의 조건은 수리 판단/제어 명세와 함께 확인하며 요청 해제 경로 전체가 없다는 뜻으로 해석하지 않습니다.</p>'
    body+='<ol><li>최초 원인 입력과 현장 상태·최초 알람의 시각을 기록합니다.</li><li>원인 해소 근거와 리셋 요청·래치 변화·현재 호출·다른 쓰기를 구분합니다.</li><li>래치 해제 이후 새 요청·모드·최종 출력 허가와 구동기 자체 복구 조건을 대조합니다.</li><li>승인된 재기동의 실제 출력·응답·연동 상태를 기록합니다. 빈 관찰값은 미확인으로 남깁니다.</li></ol>'+link('공통 리셋 요청·물리 출력','common-control.html#reset')+' · '+link('startup 기억과 재기동','common-control.html#restart')
    body+='<h2 id="writes">5. 래치의 전체 정적 쓰기·미확정 방향</h2><p>정확한 Global 이름 범위의 원본 참조를 사용합니다. 복원된 참조가 현재 프로그램 전체 쓰기/HMI/외부 쓰기의 완전한 목록이라는 뜻은 아닙니다. 기존 simulation 블록은 백업 원본 참조이며 작성·실행하지 않습니다.</p>'
    for a in p['alarms']:
        counts=Counter(u['role'] for u in a['usages'])
        labels={'read':'읽기','write':'쓰기','pending':'방향 미확정'}
        body+='<h3>'+e(a['name'])+'</h3><p>'+' · '.join(labels[role]+' '+str(counts[role])+'곳' for role in ['read','write','pending'])+' · 다른 범위 '+str(len(a['other_scope_usages']))+'곳</p>'
        body+=table(['방향·블록','원본 명령/핀','선언 근거'],[[e(labels[u['role']]+' / '+u['block']+(' · 백업 기존 블록' if u['legacy_simulation_block'] else '')),netlink(u['network'],u['part'])+'<br>'+e(u['gate']+' / '+u['pin']+' / Wire '+u['wire']+' / ORef '+u['oref']),'<br>'.join(link(d['kind']+' / '+d['scope']+' / AK '+str(d['access_kind']),d['file']) for d in u['declarations'])] for u in a['usages'] if u['role']!='read'])
    body+='<h2 id="native">6. 원본 Part·Wire·ORef 증거</h2>'
    if p['family']=='damper':body+='<p>1226·1714는 여러 댐퍼가 함께 있는 원본입니다. 위 알람·타이머·오차값 표는 선택 설비의 정확한 이름만 배정했습니다. 아래 펼침의 전체 원본 Part/Wire에는 다른 댐퍼도 포함되며 이 설비의 전용 조건으로 해석하지 않습니다.</p>'
    for n in p['native_networks']:
        body+='<details><summary>원본 '+str(n['network'])+' · '+e(n['title'])+' · '+str(len(n['parts']))+' Parts</summary><p>'+link('원본 XML',n['file'])+' · SHA256 <code>'+n['sha256']+'</code></p>'+table(['Part','Gate','Negated pins'],[[e(x['uid']),e(x['gate']),e(', '.join(x['negated_pins']) or '없음')] for x in n['parts']])+table(['Wire','연결점'],[[e(w['uid']),'<br>'.join(e(x['kind']+' '+str(x['uid'] or '')+' / '+str(x['pin'] or ''))+(' · '+e(n['refs'][x['uid']]['name'])+' / RefId '+e(n['refs'][x['uid']]['ref_id']) if x['kind']=='OCon' else '') for x in w['endpoints'])] for w in n['wires']])+'</details>'
    body+='<p>'+link('전체 정적 근거 JSON','registers/alarm-recovery.json')+'</p>'
    (out/(p['id']+'.html')).write_text(page(p['id']+' · 알람 발생·리셋·재기동 근거',body))
body=notice+'<p>모터·팬9개와 게이트·댐퍼5개의 알람 래치·감시 시간·요청 해제를 비교합니다. 원인 입력·위치 기억·오차값·고장 래치·운전 허가를 구분합니다.</p>'+table(['설비·범위','알람·타이머','주의할 경계','작업지'],[[e(p['id']+' / '+p['priority_key'])+'<br>'+e(p['name']),str(len(p['alarms']))+' 래치 / '+str(len(p['timers']))+' SD',e(p['note']),link('알람·복구 근거','alarm-guides/'+p['id']+'.html','')] for p in profiles])+link('정적 근거 JSON','registers/alarm-recovery.json','')
(ROOT/'alarm-recovery.html').write_text(page('모터·밸브 알람 발생·리셋·재기동 비교',body,''))
print(json.dumps(dict(guides=len(profiles),alarms=sum(len(p['alarms']) for p in profiles),timers=sum(len(p['timers']) for p in profiles),native_networks=len({n['network'] for p in profiles for n in p['native_networks']}),profile_network_references=sum(len(p['native_networks']) for p in profiles),plc_changes=0,simulator_behavior_tests='not_rerun'),ensure_ascii=False))
