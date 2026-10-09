"""Static encoder evidence and repair manual. No evaluator or PLC mutation."""
from pathlib import Path
import csv,hashlib,html,json,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parent
load=lambda f:json.loads((ROOT/f).read_text())
sha=lambda f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest()
e=lambda s:html.escape(str(s))
tag=lambda x:x.tag.rsplit('}',1)[-1]
canon=lambda s:str(s or '').replace('"','').casefold()
m=load('registers/program-model.json');nets={n['id']:n for n in m['networks']}
mp={n['document_id']:n for n in load('sources/decoded-original/network-map.json')}
decls=load('sources/decoded-original/identifier-declarations.json')
trace=load('registers/signal-trace.json')['usages']
live={(r['segment'],r['i']):r for r in load('sources/live_index.json') if not r['deleted']}
blocks=load('sources/block_summary.json')
paths={'registers/program-model.json','registers/signal-trace.json','sources/live_index.json','sources/block_summary.json','sources/decoded-original/network-map.json','sources/decoded-original/identifier-declarations.json','registers/plc-symbols.csv','registers/equipment-hmi.csv'}
def tree(x):return dict(tag=tag(x),attributes=dict(x.attrib),text=x.text.strip() if x.text else None,children=[tree(c) for c in x])
def declarations(i,x):
    return [d for d in decls if d['nid']==mp[i]['inferred_original_nid'] and d['uid']==x.get('UId') and d['rid']==x.get('RefId')]
def native(i):
    n=nets[i];r=ET.parse(ROOT/n['file']).getroot();paths.add(n['file'])
    refs={x.get('UId'):dict(ref_id=x.get('RefId'),name=n['refs'][x.get('UId')]['name'],declarations=declarations(i,x)) for x in r.iter() if tag(x)=='ORef'}
    wires=[dict(uid=w.get('UId'),ends=[dict(kind=tag(x),uid=x.get('UId'),pin=x.get('PinName')) for x in w]) for w in r.iter() if tag(w)=='Wire']
    nodes=[]
    for x in next(x for x in r if tag(x)=='Parts'):
        if tag(x) not in ['Part','LRef','CRef']:continue
        pins=[]
        for w in wires:
            for p in w['ends']:
                if p['kind']=='PCon' and p['uid']==x.get('UId'):
                    pins.append(dict(pin=p['pin'],wire=w['uid'],references=[dict(oref=a['uid'],**refs[a['uid']]) for a in w['ends'] if a['kind']=='OCon'],peers=[a for a in w['ends'] if a!=p and a['kind']!='OCon']))
        node=dict(uid=x.get('UId'),kind=tag(x),gate=x.get('Gate'),tree=tree(x),declarations=declarations(i,x),children_declarations=[dict(kind=tag(y),uid=y.get('UId'),rid=y.get('RefId'),declarations=declarations(i,y)) for y in x if tag(y) in ['Instance','CodeBlock']],pins=pins)
        nodes.append(node)
    for ref in refs.values():paths.update('sources/decoded-original/'+d['file'] for d in ref['declarations'])
    for node in nodes:
        paths.update('sources/decoded-original/'+d['file'] for d in node['declarations'])
        paths.update('sources/decoded-original/'+d['file'] for c in node['children_declarations'] for d in c['declarations'])
    return dict(id=i,block=n['block'],index=n['index'],title=n['title'],file=n['file'],sha256=sha(n['file']),tree=tree(r),refs=refs,wires=wires,nodes=nodes)
selected=[11,1070,1226,1658,1659,1702,1703,1704,1706,1707,1708,1711,1712,1713,1714]+list(range(1756,1767))
proofs=[native(i) for i in selected];pn={p['id']:p for p in proofs}
paths.add('registers/electrical-trace.json')
electrical=load('registers/electrical-trace.json')
hmi=list(csv.DictReader((ROOT/'registers/equipment-hmi.csv').open(encoding='utf-8-sig')))
symbols=list(csv.DictReader((ROOT/'registers/plc-symbols.csv').open(encoding='utf-8-sig')))
def node(i,uid):return next(n for n in pn[i]['nodes'] if n['uid']==uid)
def values(n,pin):return [r['name'] for p in n['pins'] if p['pin']==pin for r in p['references']]
channels=[]
for j,(equipment,read_id,data_id,final_id,cal_id,priority,up,down,limit) in enumerate([
 ('MV01',1756,1762,1702,1703,'P19','W33','W34',2000),
 ('MV02',1757,1763,1704,None,None,'W35','W36',1000),
 ('MV03',1758,1764,1706,1707,'P20','W29','W30',3400),
 ('MV05',1759,1765,1708,None,None,'W31','W32',700),
 ('MV06',1760,1766,1711,None,'P21','W19','W20',2200)]):
 call=next(n for n in pn[read_id]['nodes'] if n['kind']=='LRef')
 conversion=next(n for n in pn[data_id]['nodes'] if n['kind']=='CRef')
 gate=next(n for n in pn[data_id]['nodes'] if n['gate']=='Coil' and values(n,'operand')==[f'fill_unit1.CONTROL_SIGNALS.SW_GATE{j}'])
 circuit=next((d for d in electrical['devices'] if d['id']==equipment),None)
 channels.append(dict(id=equipment,software_index=j,reading_network=read_id,data_network=data_id,final_network=final_id,calibration_network=cal_id,priority=priority,counter_call=call,conversion_call=conversion,gate_coil=gate,
     raw_count=f'fill_unit1.ACT_CNTV{j}',total=f'CNT_Act_{j}',divided=f'CNTV{j}_100',memory=f'Memory encoder.Encoder_CH{j:02d}',divided_memory=f'Memory encoder.Encoder_CH{j:02d}_10',position=f'Data.Pot_{equipment}',
     command_monitor=dict(open='WorkData.'+up,close='WorkData.'+down,open_threshold=limit,close_threshold=-limit,networks=[1713,1714]),
     circuit_reference=circuit,hmi_reference_rows=[r for r in hmi if r['설비 ID']==equipment],field_verified=False,tia_verified=False,plc_changes=0))
# Copy exact scoped usages, preserving unknown directions and other-block Local identities.
selectors=[]
for p in proofs:
 for uid in p['refs']:
  for u in trace:
   if u['network']==p['id'] and u['oref']==uid and u['scope'] in ['Global','Local'] and u['name']:
    s=(u['name'],u['scope'],u['block'] if u['scope']=='Local' else None)
    if s not in selectors:selectors.append(s)
signals=[]
for name,scope,block in selectors:
 same=lambda u:canon(u['name'])==canon(name) and u['scope']==scope and (scope!='Local' or u['block']==block)
 uses=[u for u in trace if same(u)];other=[u for u in trace if canon(u['name'])==canon(name) and not same(u)]
 paths.update(u['file'] for u in uses+other)
 signals.append(dict(name=name,scope=scope,block=block,usages=uses,other_scope_usages=other,symbols=[s for s in symbols if canon(s['원본 심볼'])==canon(name)] if scope=='Global' else []))
result=dict(date='2026-10-08',scope='Static native LAD counter, position, calibration and command-monitor evidence; not hardware configuration or current PLC execution',channels=channels,native_ids=selected,native=proofs,signals=signals,sources={p:sha(p) for p in sorted(paths)},field_verified=False,tia_verified=False,plc_changes=0,simulator_development='stopped_by_user',simulator_behavior_tests='not_rerun')
(ROOT/'registers/encoder-position.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
def link(path,label):return '<a href="'+e(path)+'">'+e(label)+'</a>'
def table(headers,rows):return '<div class="table-wrap"><table><thead><tr>'+''.join('<th>'+e(h)+'</th>' for h in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+str(v)+'</td>' for v in row)+'</tr>' for row in rows)+'</tbody></table></div>'
def netlink(i):return link('networks/network-'+str(i)+'.html','원본 '+str(i))
def pins_table(n,i):
 return table(['핀','원본 참조·연결','Wire'],[[e(p['pin']),e(' / '.join('ORef '+r['oref']+' · '+(r['name'] or '[RefId 없음·미해석; 기본값 추정 금지]') for r in p['references']) or ' / '.join(q['kind']+' '+str(q['uid'])+'.'+str(q['pin']) for q in p['peers'])),link('#wire-'+str(i)+'-'+p['wire'],p['wire'])] for p in n['pins']])
body='<h1>엔코더·밸브 위치·교정 수리 매뉴얼</h1><p>5개 밸브 · High_Speed_Counter 원본5호출 · 위치 환산5호출 · 교정 요청2경로 · 선택 LAD26네트워크</p><div class="notice info">엔코더 카운트·환산 위치·끝단 리미트·접촉기 응답·방향 명령 감시를 구분합니다. 소프트웨어 색인0~4는 물리 TM 채널 번호나 주소를 증명하지 않습니다. 현재 하드웨어 구성·정상 극성·기계 기준·단위·복구는 확인 전입니다. 시뮬레이터 작성·수정·행동 시험은 중지합니다.</div>'
body+='<nav class="inline-actions">'+link('regulation-manual.html','조절 루프 수리·구조')+link('electrical-trace.html','전기 회로·단자')+link('alarm-recovery.html','알람·복구')+link('work-progress.html','현재 진행 순서')+'</nav><h2 id="index">밸브 선택</h2>'
body+=table(['설비','원본 읽기 → 환산','소프트웨어 카운트','교정 요청','현장 연결'],[[link('#position-'+c['id'],c['id']),netlink(c['reading_network'])+' → '+netlink(c['data_network']),e(c['raw_count']),netlink(c['calibration_network']) if c['calibration_network'] else '동일 교정 경로 확인 전',link('circuit-guides/'+c['id']+'.html','기존 회로') if c['circuit_reference'] else '이 작업지의 회로 상세 근거 없음'] for c in channels])
for c in channels:
 id_=c['id'];j=c['software_index'];i=c['data_network'];call=c['counter_call'];cv=c['conversion_call']
 body+='<section><h2 id="position-'+id_+'">'+id_+' · 입력부터 위치 표시까지</h2><nav class="inline-actions">'+link('procedures/'+id_+'.html','증상별 수리')+link('regulation-manual.html#loop-'+id_,'조절·최종 방향 명령')
 if c['priority']:body+=link('index.html#view=repair-record&equipment='+c['priority']+'&scope=priority','우선 설비 수리 기록')
 if c['circuit_reference']:body+=link('circuit-guides/'+id_+'.html','전기 회로·단자·현장 경계')
 body+='</nav><h3>1. 원본 카운터 호출과 사용 허가</h3><p>'+netlink(c['reading_network'])+'의 LRef '+e(call['uid'])+'는 선언 '+e(' / '.join(d['name'] for d in call['declarations']))+' / 인스턴스 '+e(' / '.join(d['name'] for x in call['children_declarations'] for d in x['declarations']))+'입니다. en 앞에는 반전 Simulation(1)과 EM_OK 접점이 직렬 연결됩니다. 원본의 신호명이며 가상 프로그램을 실행하지 않습니다.</p>'+pins_table(call,c['reading_network'])
 body+='<p>CountValue→'+e(c['raw_count'])+'는 원본 배선으로 확인합니다. SetCountValue·상태·에러 등 RefId 없는 연결은 false·0·현재 미사용으로 채우지 않습니다. MV01의 ErrorAck/EventAck에는 Flag.RESET_ALLARM이 표시되며 다른4호출의 같은 핀은 미해석입니다.</p>'
 body+='<h3>2. 게이트·저장값·합산·환산</h3><ol><li>'+netlink(i)+'에서 EM_OK와 반전 닫힘 입력을 따라 SwGate 쓰기를 확인합니다. MV03은 Inputs.MV03 Close, 다른4개는 물리 심볼 MVxx_Close를 사용합니다. MV03의 원본1070 반전 입력 전달과 다른 입력의 미확정 전달을 구분합니다.</li><li>'+e(c['memory']+' + '+c['raw_count']+' → '+c['total'])+' (DInt Add), '+e(c['total']+' ÷ 100 → '+c['divided'])+' (DInt Div), 이후 '+e(c['divided_memory'])+'로 Move합니다. 이름의 _10과 실제 나누기100을 구분하며 각도·퍼센트·분해능으로 단정하지 않습니다.</li><li>SwGate 반전 분기에는 '+e(c['divided_memory'])+'로0, '+e(c['memory'])+'로INT#0을 쓰는 Move가 별도로 있습니다. 같은 값의 다른 쓰기·현재 호출 순서를 확인합니다.</li><li>Signal linearization 호출은 IN0=ON, Analog_input='+e(c['divided_memory'])+', Coeff='+e(' / '.join(values(cv,'Coeff')))+', Zero='+e(' / '.join(values(cv,'Zero')))+', OutValue='+e(c['position'])+', Out_of_range='+e(' / '.join(values(cv,'Out_of_range')))+'를 연결합니다.</li></ol>'+pins_table(cv,i)
 body+='<p>'+netlink(1658)+'의 공통 환산은 Int 입력/계수/영점의 DInt 변환, 영점 더하기·계수 곱하기·28000 나누기를 표시합니다. 입력 >-1382 및 ≤32767, 범위 밖 -9999/OFR, '+netlink(1659)+'의 NOT IN0일 때0 쓰기를 구분합니다. 호출 쪽 DInt 카운트 나눗셈과 공통 Int 입력 경계의 타입·절삭·넘침·ENO·현재 계수는 TIA에서 확인합니다.</p>'
 body+='<h3>3. 저장·교정·다른 쓰기</h3><p>'+netlink(1761)+'은 NOT EM_OK 뒤 '+e(c['total']+' → '+c['memory'])+' Move를 표시합니다. 제목 power-off만으로 실제 정전 직전 실행·영구 저장·재기동 복원을 확정하지 않습니다. 현재 전원 감시·호출·DB 유지 설정을 확인합니다.</p>'
 if c['calibration_network']:
  body+='<p>'+netlink(c['calibration_network'])+'은 HMI_DB.ResetEncoderProcedure_'+id_+'와 Inputs.'+id_+' Close 뒤 NewCountValue로0 Move, 반전 SetCountValue 접점, SetCountValue Coil, HMI 요청 RCoil의 Wire를 보존합니다. Move의 DisableENO=true도 보존하며 한 번의 교정 펄스·하드웨어 적용 완료로 추정하지 않습니다. 인스턴스 필드 쓰기와 호출 핀의 미해석 연결은 별도 근거입니다. '+netlink(c['final_network'])+'의 교정 요청/출력 억제·닫힘 요청과 실제 기준 위치를 함께 봅니다.</p>'
 else:
  body+='<p>선택 원본에서 MV01/MV03과 같은 HMI 교정 요청 네트워크는 확인하지 못했습니다. 다른 밸브의 교정 명령을 복사해 절차로 제시하지 않습니다. 현재 프로젝트와 제작사 기준을 확인합니다.</p>'
 position=next(s for s in signals if s['name']==c['position'] and s['scope']=='Global')
 writers=sorted({u['network'] for u in position['usages'] if u['role']=='write'})
 body+='<p>기존 LAD핀 색인의 '+e(c['position'])+' 쓰기 위치: '+' · '.join(netlink(w) for w in writers)+'. 원본 simulation/추세 시험 블록 등 다른 쓰기는 현재 호출·활성 여부 확인 전이며 실행·수정하지 않습니다. 인스턴스 내부나 문자 코드의 전체 쓰기 목록을 증명하는 표가 아닙니다.</p>'
 body+='<h3>4. 방향 명령 누적 감시와 위치 센서의 차이</h3><p>'+netlink(1713)+'은 최종 열기 명령 뒤 '+e(c['command_monitor']['open'])+'에+1, 닫기 명령 뒤 '+e(c['command_monitor']['close'])+'에-1, 반대 방향 누적값에0을 쓰는 경로를 표시합니다. '+netlink(1714)+'의 '+e(c['command_monitor']['open']+' > '+str(c['command_monitor']['open_threshold']))+' / '+e(c['command_monitor']['close']+' < '+str(c['command_monitor']['close_threshold']))+'는 고장 래치와 해당 누적값0 쓰기에 연결됩니다.</p><p>이 비교 입력은 엔코더 CountValue나 Pot 위치 오차가 아닙니다. 원본에는 방향 명령 누적값이 표시됩니다. PLS 50 7·ON 분기·10ms SD·호출 주기·다른 쓰기를 확인해야 하며 실제 이동 시간이나 분해능으로 환산하지 않습니다. '+netlink(1226)+'의 방향 응답 감시와도 구분합니다.</p>'
 body+='<h3>5. 증상별 비교와 다음 확인</h3>'+table(['증상','관찰 순서','확인 경계'],[
 ['명령은 있으나 위치가 고정','최종Q → 접촉기 응답 → 모터/밸브 이동 → 리미트 → CountValue → 합산/환산 위치를 같은 시각에 기록합니다.','접촉기 응답만으로 이동을 판정하지 않습니다. A/B 신호·전원·커플링·HW 채널은 현장 자료로 확인합니다.'],
 ['원시 카운트는 변하지만 위치가 고정','SwGate·저장값·합산값·나눗셈값·계수·영점·OutValue/OFR·같은 값의 다른 쓰기를 비교합니다.','DInt/Int 변환 경계와 실제 단위를 확인합니다. 화면 태그의 존재만으로 표시 전달을 확정하지 않습니다.'],
 ['닫힘에서 값이0 또는 재기동 후 값이 바뀜','닫힘 원시/처리 신호·SwGate 반전·0쓰기·NOT EM_OK 저장·DB 유지 설정·현재 호출을 기록합니다.','정전 중 저장 보장이나 자동 복원 완료로 판단하지 않습니다. 정상 극성과 실제 기준 위치를 확인합니다.'],
 ['교정 요청 후 표시와 실물이 다름','요청·닫힘 입력·NewCountValue/SetCountValue·실제HW값·위치 환산·출력 억제를 비교합니다.','해당 교정 경로가 확인된 밸브에만 적용합니다. 실제 조작·교정 완료 결과는 이 문서에서 생성하지 않습니다.'],
 ['MV 고장과 위치/OFR가 함께 표시','1713/1714 방향 누적·1226 방향 응답·Pot_OFR·처음 알람의 시각을 분리합니다.','방향 누적 한계·엔코더 값·리미트·공통 인버터를 동일한 고장으로 묶지 않습니다.']])
 if c['circuit_reference']:
  cr=c['circuit_reference'];body+='<details><summary>기존 전기 회로 작업지의 연결 근거 · 현재 배선 확인 전</summary><p>'+e(cr['distinction'])+'</p>'+table(['PDF 페이지','원본'],[[e(p),link(electrical['source']+'#page='+str(p),'PDF '+str(p))] for p in cr['pages']])+table(['경로','단자·노드','다음 확인'],[[e(p['signal']),'<br>'.join(e(s) for s in p['nodes']),e(p['check'])] for p in cr['paths'] if '엔코더' in p['signal'] or '끝단' in p['signal']])+'</details>'
 body+='<details><summary>HMI 기존 설정 참고 · '+str(len(c['hmi_reference_rows']))+'행</summary>'+table(['태그','설정주소','Access Name','내부ID'],[[e(r[k]) for k in ['HMI 태그','설정 주소','Access Name','내부 ID']] for r in c['hmi_reference_rows']])+'<p>현재 DB 오프셋·표시 단위·쓰기/읽기 전달은 추가 확인합니다.</p></details></section>'
body+='<h2 id="native">원본 LAD 전체 접점·연산·핀·Wire</h2><p>원본 XML의 트리·속성·반전·템플릿·참조 선언과 전체 Wire를 JSON에 보존합니다. 표의 나열 순서는 실행 순서나 논리식이 아닙니다.</p>'
for p in proofs:
 body+='<details id="native-'+str(p['id'])+'"><summary>'+e(str(p['id'])+' · '+p['block']+' · '+p['title'])+'</summary><p>'+netlink(p['id'])+' · '+link(p['file'],'원본 XML')+' · SHA256 '+e(p['sha256'])+'</p>'
 for n in p['nodes']:
  body+='<h3>'+e(n['uid']+' · '+str(n['gate'] or n['kind']))+'</h3><p>'+e(str(n['tree']['attributes'])+' / '+str(n['tree']['children'])+' / '+str(n['declarations'])+' / '+str(n['children_declarations']))+'</p>'+pins_table(n,p['id'])
 body+=table(['Wire','모든 연결'],[['<span id="wire-'+str(p['id'])+'-'+w['uid']+'">'+e(w['uid'])+'</span>',e(' / '.join(x['kind']+' '+str(x['uid'])+'.'+str(x['pin']) for x in w['ends']))] for w in p['wires']])+'</details>'
body+='<h2 id="writes">같은 신호의 읽기·쓰기 · 다른 블록 Local 분리</h2><p>기존 LAD핀 색인의 범위와 역할을 그대로 보존합니다. pending은 방향 확인 전입니다. HW/인스턴스 내부·검색색인 문자만의 쓰기는 이 핀 목록으로 확정하지 않습니다.</p>'
for s in signals:
 body+='<details><summary>'+e(s['name']+' · '+s['scope']+' · '+str(s['block'] or ''))+' · '+str(len(s['usages']))+'핀 / 다른 범위 '+str(len(s['other_scope_usages']))+'</summary>'+table(['네트워크·핀','역할','블록·범위','백업 주소'],[[netlink(u['network'])+' · '+e(u['part']+'.'+str(u['pin'])),e(u['role']),e(u['block']+' / '+u['scope']),e(' / '.join(x['백업 주소'] for x in s['symbols']))] for u in s['usages']])
 if s['other_scope_usages']:body+='<p>'+e(' / '.join(str(u['network'])+' '+u['scope']+' '+u['block'] for u in s['other_scope_usages']))+'</p>'
 body+='</details>'
body+='<h2 id="checks">현재 TIA·현장·제작사에서 확정할 항목</h2><p>TM 모델/HW 식별자·실제 채널/주소·엔코더 전원/A/B 위상·분해능/기어비·카운트 방향·리미트 정상극성·계수/영점·현재DB 유지·기준 위치·교정 적용 확인·HMI 실제 전달·OB 호출 순서·정전 감시/저장 기회를 확인합니다. 기존 불일치18건·확인 대장1,060건·설계시험577건의 상태는 변경하지 않습니다.</p>'+link('registers/encoder-position.json','원본 트리·호출·범위·해시 JSON')
body+='''<script>function revealEvidence(){let id;try{id=decodeURIComponent(location.hash.slice(1));}catch(_){return;}const target=document.getElementById(id);if(!target)return;let parent=target;while(parent){if(parent.tagName==='DETAILS')parent.open=true;parent=parent.parentElement;}target.scrollIntoView({block:'start'});}addEventListener('hashchange',revealEvidence);revealEvidence();</script>'''
(ROOT/'encoder-position.html').write_text('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>엔코더·밸브 위치·교정 수리 매뉴얼</title><link rel="stylesheet" href="assets/all-in-one.css"><style>main{max-width:1320px;margin:auto;padding:24px}td{vertical-align:top;overflow-wrap:anywhere}h2{scroll-margin-top:20px}li{margin:.6em 0}details{margin:12px 0}summary{cursor:pointer;font-weight:600}.inline-actions{flex-wrap:wrap}</style></head><body><main>'+body+'</main></body></html>')
print(json.dumps(dict(status='built',channels=5,native_networks=len(selected),counter_calls=5,conversion_calls=5,calibration_paths=2,signal_scopes=len(signals),source_hashes=len(paths),simulator_development='stopped_by_user'),ensure_ascii=False))
