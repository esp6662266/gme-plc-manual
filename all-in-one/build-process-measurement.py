"""Process measurements and burner stop sources; documentation only, no execution."""
from pathlib import Path
from collections import Counter
import hashlib, html, json, csv, xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parent
load=lambda f:json.loads((ROOT/f).read_text())
sha=lambda f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest()
tag=lambda x:x.tag.rsplit('}',1)[-1]
canon=lambda s:str(s or '').replace('"','').casefold()
e=lambda s:html.escape(str(s))
model=load('registers/program-model.json');nets={n['id']:n for n in model['networks']}
trace=load('registers/signal-trace.json')['usages']
source_map={n['document_id']:n for n in load('sources/decoded-original/network-map.json')}
declarations=load('sources/decoded-original/identifier-declarations.json')
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

source_paths={'registers/program-model.json','registers/signal-trace.json','registers/plc-symbols.csv',
 'registers/electrical-trace.json','registers/equipment-hmi.csv','sources/decoded-original/network-map.json',
 'sources/decoded-original/identifier-declarations.json','sources/Electrical_Rev2.pdf'}

def native(i):
    n=nets[i];root=ET.parse(ROOT/n['file']).getroot();source_paths.add(n['file'])
    parts=[dict(uid=x.get('UId'),gate=x.get('Gate'),attributes=dict(x.attrib),
        negated_pins=[c.get('PinName') for c in x if tag(c)=='Negated'],
        templates=[dict(attributes=dict(c.attrib),value=c.text) for c in x if tag(c)=='TemplateValue']) for x in root.iter() if tag(x)=='Part']
    refs={x.get('UId'):dict(ref_id=x.get('RefId'),name=n['refs'][x.get('UId')].get('name')) for x in root.iter() if tag(x)=='ORef'}
    for uid,r in refs.items():
        r['declarations']=[d for d in declarations if d['uid']==uid and d['rid']==r['ref_id'] and d['nid']==source_map[i]['inferred_original_nid'] and d['name']==r['name']]
        source_paths.update('sources/decoded-original/'+d['file'] for d in r['declarations'])
    calls=[]
    for c in [x for x in model['calls'] if x['network']==i]:
        ref=next(x for x in root.iter() if tag(x)=='CRef' and x.get('UId')==c['uid']);block=next(x for x in ref if tag(x)=='CodeBlock')
        decl=[d for d in declarations if d['uid']==block.get('UId') and d['rid']==block.get('RefId') and d['nid']==source_map[i]['inferred_original_nid'] and d['name']==c['callee']]
        assert decl,(i,c['callee']);source_paths.update('sources/decoded-original/'+d['file'] for d in decl)
        calls.append(dict(**c,cref_ref_id=ref.get('RefId'),block_ref_id=block.get('RefId'),native_declarations=decl))
    wires=[dict(uid=w.get('UId'),endpoints=[dict(kind=tag(x),uid=x.get('UId'),pin=x.get('PinName')) for x in w]) for w in root.iter() if tag(w)=='Wire']
    return dict(network=i,block=n['block'],index=n['index'],title=n['title'],file=n['file'],sha256=sha(n['file']),parts=parts,refs=refs,calls=calls,wires=wires)

def proof(p,uid):
    nodes={x['uid']:x for x in p['parts']};nodes.update({c['uid']:dict(uid=c['uid'],gate='CRef',negated_pins=[]) for c in p['calls']})
    seen=set();todo=[uid]
    while todo:
        current=todo.pop()
        if current in seen:continue
        seen.add(current)
        for w in p['wires']:
            if any(x['kind']=='PCon' and x['uid']==current and (x['pin'] in ['in','en','pre'] or x['pin'] and x['pin'].startswith('in') and x['pin'][2:].isdigit()) for x in w['endpoints']):
                todo.extend(x['uid'] for x in w['endpoints'] if x['kind']=='PCon' and x['pin'] in ['out','eno'])
    pins=[];contacts=[]
    for w in p['wires']:
        for x in w['endpoints']:
            if x['kind']=='PCon' and x['uid'] in seen:
                for c in w['endpoints']:
                    if c['kind']!='OCon':continue
                    row=dict(part=x['uid'],gate=nodes[x['uid']]['gate'],pin=x['pin'],wire=w['uid'],oref=c['uid'],name=p['refs'][c['uid']]['name'],ref_id=p['refs'][c['uid']]['ref_id'])
                    pins.append(row)
                    if row['gate'] in ['Contact','PContact','NContact'] and row['pin']=='operand':contacts.append(dict(**row,negated_pins=nodes[x['uid']]['negated_pins']))
    return dict(nodes=sorted(seen,key=int),reference_pins=pins,contacts=contacts)

def reads(v):
    if isinstance(v,dict):
        if v.get('op')=='read':yield v['name']
        for value in v.values():yield from reads(value)
    elif isinstance(v,list):
        for value in v:yield from reads(value)

alarm_names=['Allarm.MAX_MAX_TC09','Allarm.MAX_MAX_TC01_TEMP','Allarm.MAX_TC04_TEMP','Allarm.MAX_TC05_TEMP',
 'Allarm.MAX_MAX_TC03_TEMP','Allarm.RO01_Signal_Fault','Allarm.TC01_TC02_COMP_FAULT','Allarm.Low_Aspiration',
 'Allarm.PSL_AIR_LOW','Allarm.HYDROGEN_BOX_FAULT','Allarm.EmergencyStopTC1_2']
alarm_networks=[1227,1979,1980,1981,1985,1986,1987,1990,1991]
analog_networks=[1658,1659,1686,1687,1724,1752,1753,1754,1755,1834]
selected=sorted(analog_networks+alarm_networks+[1858])
proofs=[native(i) for i in selected];by_net={p['network']:p for p in proofs}

def enriched(i,a):
    result=dict(network=i,**a,native_upstream=proof(by_net[i],a['uid']))
    if a['gate']=='SdCoil':
        v=next(x for x in result['native_upstream']['reference_pins'] if x['part']==a['uid'] and x['pin']=='value')
        result['value_declarations']=by_net[i]['refs'][v['oref']]['declarations']
        assert result['value_declarations'] and v['name']==a['preset']['literal']
    return result

analog_actions=[enriched(i,a) for i in analog_networks for a in nets[i]['actions']]
alarms=[]
for name in alarm_names:
    uses=[u for u in trace if u['scope']=='Global' and canon(u['name'])==canon(name)]
    acts=[enriched(i,a) for i in alarm_networks for a in nets[i]['actions'] if a['name']==name]
    timer_names={name for a in acts for name in reads(a['condition']) if name.startswith('Tag_')}
    timers=[enriched(i,a) for i in alarm_networks for a in nets[i]['actions'] if a['gate']=='SdCoil' and a['name'] in timer_names]
    support_names={canon(x) for a in acts+timers for x in reads(a['condition'])}
    supports=[enriched(i,a) for i in {a['network'] for a in acts} for a in nets[i]['actions'] if a['gate'] in ['Add','Sub','Mul','Div','Convert'] and canon(a['name']) in support_names]
    alarms.append(dict(name=name,scope='Global',actions=acts,timers=timers,support_actions=supports,
        usages=uses,other_scope_usages=[u for u in trace if u['scope']!='Global' and canon(u['name'])==canon(name)],
        writer_coverage='selected_original_set_reset' if acts else 'no_exact_global_writer_in_reconstructed_index'))
stop=enriched(1858,next(a for a in nets[1858]['actions'] if a['name']=='Flag.Start_Burner'))
stop_names=list(dict.fromkeys(n for n in reads(stop['condition']) if n.startswith('Allarm.')))
assert set(alarm_names)<=set(stop_names)
call_specs=[('가스 서보 위치',1752,'%IW360','Data.GAS_BR_01','Allarm.BR01_Gas_OFR'),
 ('공기 서보 위치',1753,'%IW362','Data.AIR_BR_01','Allarm.BR01_Air_OFR'),
 ('가스 질량유량',1754,'%IW364','Data.MASSICO_FLOW_GAS','Allarm.Massico_Gas_OFR'),
 ('공기 질량유량',1755,'%IW366','Data.MASSICO_FLOW_AIR','Allarm.Massico_Air_OFR')]
circuit=next(d for d in load('registers/electrical-trace.json')['devices'] if d['id']=='BR01')
channels=[]
for title,i,address,out,ofr in call_specs:
    call=by_net[i]['calls'][0]
    assert call['callee']=='Signal linearization' and call['bindings']['OutValue']==[out] and call['bindings']['Out_of_range']==[ofr]
    path=next(p for p in circuit['paths'] if p['backup'].upper().startswith(address+' '))
    channels.append(dict(title=title,network=i,address=address,call=call,native_upstream=proof(by_net[i],call['uid']),circuit=path))
outputs=[dict(title='공기 서보 설정',network=1686,address='%QW310',value='Data.Burner_Air_Out',scale='272',part='536',
 circuit=next(p for p in circuit['paths'] if p['backup'].upper().startswith('%QW310 '))),
 dict(title='가스 서보 설정',network=1687,address='%QW308',value='Data.Burner_Gas_Out',scale='285',part='590',
 circuit=next(p for p in circuit['paths'] if p['backup'].upper().startswith('%QW308 ')))]
focus=list(dict.fromkeys([n for c in channels for values in c['call']['bindings'].values() for n in values]+
 [n for o in outputs for n in [o['value']]]+['BR01_AIR_SP','BR01_GAS_SP','Calcolo_Aria','Data.Burner_Panel_SetPoint']+alarm_names+
 ['Manage_TC1_2.PID_Ref_Temp','Data.Temp_TC01','Data.Temp_TC02','Data.Temp_TC03','Data.Temp_TC04','Data.Temp_TC05',
 'Data.TC_09','Data.TC01_MAX_ALL','Data.TC03_MAX_ALL','Data.TC04_TC05_MAX_ALL','Data.TC09_MAX_MAX','Data.PC_01',
 'Data.Min_Pressure_PC_01','Inputs.Low Pressure Air','Inputs.NITROGEN TANK READY','ServiceBit','RO01-RO02control disable','TC01-TC02control disable']))
symbols=list(csv.DictReader((ROOT/'registers/plc-symbols.csv').open(encoding='utf-8-sig')))
selectors=[(n,'Global',None) for n in focus]+[(n,'Local','signal linearization') for n in ['IN0','Analog_input','Zero','Coeff','App3','App4','App5','App6','OutValue','Out_of_range']]
signals=[]
for name,scope,block in selectors:
    uses=[u for u in trace if canon(u['name'])==canon(name) and u['scope']==scope and (block is None or u['block']==block)]
    other=[u for u in trace if canon(u['name'])==canon(name) and not(u['scope']==scope and (block is None or u['block']==block))]
    source_paths.update(u['file'] for u in uses+other);source_paths.update(d['file'] for u in uses+other for d in u['declarations'])
    signals.append(dict(name=name,scope=scope,block=block,usages=uses,other_scope_usages=other,
       symbols=[s for s in symbols if scope=='Global' and canon(s['원본 심볼'])==canon(name)]))
hmi=[r for r in csv.DictReader((ROOT/'registers/equipment-hmi.csv').open(encoding='utf-8-sig')) if r['설비 ID']=='BR01']
observations=[
 dict(id='PM-01',status='현재 모듈·계수·단위 확인 대기',title='4–20mA 도면과 원본 환산의 경계',text='네 입력은 같은 Signal linearization 블록을 호출하지만 Coeff와 Zero 피연산자는 각각 다릅니다. 원본 Int→DInt, Add·Mul·Div(28000)와 원시 범위 비교를 보존합니다. 현재 모듈 범위·단위·계수/영점 값과 수치 잘림·오버플로·ENO는 확인 전입니다.',networks=[1658,1659,1752,1753,1754,1755]),
 dict(id='PM-02',status='현재 값·호출·후속 쓰기 확인 대기',title='가스 유량의 하한1과 범위 이상 표시',text='1658의 범위 이상 분기는 OutValue에 -9999를 쓰고 Out_of_range를 출력합니다. 1754에는 Data.MASSICO_FLOW_GAS<1이면1을 쓰는 별도 Move가 있습니다. 변환값·후속값·OFR 플래그를 함께 기록하며 최종 표시값만으로 센서 정상/복구를 판정하지 않습니다. 같은 스캔의 최종값은 확인 전입니다.',networks=[1658,1754]),
 dict(id='PM-03',status='현재 출력 범위·쓰기 주체 확인 대기',title='공기272·가스285와 설정값의 복수 쓰기',text='1686 공기 Mul은272, 1687 가스 Mul은285입니다. 0~100 제한·QW 값 전달과 1724/1834의 관련 쓰기는 별도입니다. 현재 출력 모듈 범위나 실제 mA/위치에 대한 환산 기준을 임의로27648 등으로 바꾸지 않습니다.',networks=[1686,1687,1724,1834]),
 dict(id='PM-04',status='발생·해제 쓰기 자료 추가 확인 대기',title='EmergencyStopTC1_2 LAD 쓰기 미확정·별도 SCL 문자 근거',text='1858에서 Allarm.EmergencyStopTC1_2를 읽지만 복원된 LAD 핀 색인의 정확한 Global 쓰기는 확인하지 못했습니다. 별도 백업 색인 SCL1719에는 Manage_TC1_2.EmergencyStop의 해당 알람 대입이 표시됩니다. 조절 루프 작업지에서 원문을 함께 보고 현재 SCL/TIA와 센서 선택·초기 Enable·호출 순서를 확인합니다. 문자 근거를 LAD 쓰기 핀이나 현재 발생 조건 확정으로 바꾸지 않습니다.',networks=[1858]),
 dict(id='PM-05',status='현재 정상 극성·명칭·기능 확인 대기',title='HYDROGEN 이름과 NITROGEN 입력',text='1990의 HYDROGEN_BOX_FAULT는 Inputs.NITROGEN TANK READY와 ServiceBit를 읽습니다. 원본 이름을 보존하고 실물 가스 종류·신호 극성·전용반 기능을 추가 확인합니다. GSS나 미확정 설비에 이 태그를 배정하지 않습니다.',networks=[1990]),
 dict(id='PM-06',status='현재 허가·리셋·센서값 확인 대기',title='정지 래치와 리셋 접점의 차이',text='TC04/05·TC01/03 MAX_MAX·TC09·RO/TC비교의 리셋과 PC01·PSL·전용반 리셋은 원본 접점 구성이 다릅니다. Low_Aspiration 리셋은 FN01/FN04 운전 응답도 읽고, PSL은 압력 입력의 정상 접점을 읽습니다. 래치 해제·원인 해소·기동 허가는 각각 확인합니다.',networks=alarm_networks),
]
data=dict(date='2026-10-08',scope='Native measurement conversion and process causes read by burner stop; no execution or safety-value recommendation',
 selected_networks=selected,analog_networks=analog_networks,alarm_networks=alarm_networks,native_networks=proofs,
 analog_actions=analog_actions,channels=channels,outputs=outputs,alarms=alarms,stop_action=stop,stop_alarm_names=stop_names,
 signals=signals,hmi_reference_rows=hmi,observations=observations,sources={f:sha(f) for f in sorted(source_paths)},
 field_verified=False,tia_verified=False,plc_changes=0,simulator_development='stopped_by_user',simulator_behavior_tests='not_rerun')
(ROOT/'registers/process-measurement.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')

def link(label,path):return '<a href="'+e(path)+'">'+e(label)+'</a>'
def netlink(n,uid=None):return link('원본 '+str(n)+(' / Part '+str(uid) if uid else ''),'networks/network-'+str(n)+'.html')
def table(head,rows):return '<div class="table-wrap"><table><thead><tr>'+''.join('<th>'+e(h)+'</th>' for h in head)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+str(c)+'</td>' for c in row)+'</tr>' for row in rows)+'</tbody></table></div>'
def arows(rows):return [[e(a['gate']+' / '+a['name']),'<code>'+e(expression(a['condition']))+'</code>',e(expression(a['value'])) if 'value' in a else '',netlink(a['network'],a['uid'])] for a in rows]
def pinrows(p,uid):
    return [[e(x['gate']+'/'+str(x['pin'])+' / '+str(x['name'])),e('Part '+x['part']+' / Wire '+x['wire']+' / ORef '+x['oref']+' / RID '+str(x['ref_id']))] for x in proof(p,uid)['reference_pins']]
def page(title,body):return '<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+e(title)+'</title><link rel="stylesheet" href="assets/all-in-one.css"><style>main{max-width:1320px;margin:auto;padding:24px}td{vertical-align:top}code{white-space:normal;overflow-wrap:anywhere}details{margin:16px 0}summary{cursor:pointer}</style></head><body><main><h1>'+e(title)+'</h1>'+body+'</main></body></html>'
notice='<div class="notice">원본 백업·OEM 도면의 정적 근거입니다. 현재값·계수·물리 단위·모듈 설정·CPU/TIA·현장 복구는 확인 전입니다. 원본 수치는 권장 보호값이나 실제 검출 시간으로 사용하지 않습니다. PLC 변경0건, 시뮬레이터 작성·행동 시험 중지.</div>'
nav='<nav class="inline-actions">'+link('온도·압력·산소 계측 수리','sensor-measurement.html')+link('가스·공기 환산 근거','measurement-trace.html')+link('공정 알람·버너 정지 원인','process-stop-alarms.html')+link('BR01 외부 연동·리셋','burner-interface.html')+link('버너 외부 회로','circuit-guides/BR01.html')+link('BR01 수리 기록','index.html#view=repair-record&equipment=P11&scope=priority')+'</nav>'
body=notice+nav+'<p>물리 입력·원시값·변환값·후속 제한·설정 출력·HMI 표시를 구간별로 비교합니다. 별칭이나 출력 범위를 임의로 통일하지 않습니다.</p>'
body+='<h2 id="channels">1. 네 입력의 호출·계수·범위 이상 연결</h2>'+table(['입력·백업 주소','원본 호출 핀 연결','물리 경로·추가 확인'],[[e(c['title']+' / '+c['address'])+'<br>'+netlink(c['network'],c['call']['uid']),'<br>'.join(e(k+' ← '+', '.join(v)) for k,v in c['call']['bindings'].items()),'<br>'.join(e(n) for n in c['circuit']['nodes'])+'<br>'+e(c['circuit']['check'])] for c in channels])
body+='<p>Coeff·Zero는 각각의 원본 피연산자이며 현재 계수/영점값을 자동 표시하지 않습니다. Out_of_range 출력 연결은 센서 이상 플래그의 원본 참고입니다. 버너 정지와의 직접 연결 여부는 정확한 읽기 참조로 별도 확인합니다.</p>'
body+='<h2 id="linear">2. Signal linearization 내부의 원본 값 전달</h2><p>1658에서 Analog_input·Zero·Coeff를 Int→DInt로 변환하고 Add→Mul→Div(28000)→OutValue로 전달하는 배선을 확인합니다. 이는 정수형 원본 구조의 설명이며 실행 계산이나 현재 환산값이 아닙니다. IN0·범위 조건·ENO·현재 호출·값 잘림과 오버플로는 확인 전입니다.</p>'
body+=table(['원본 명령','형식·값 핀','근거'],[[e(x['gate']+' / Part '+x['uid']),'<br>'.join(e(t['attributes']['Name']+'='+str(t['value'])) for t in x['templates'])+'<br>'+table(['피연산자','배선 식별'],pinrows(by_net[1658],x['uid'])),netlink(1658,x['uid'])] for x in by_net[1658]['parts'] if x['gate'] in ['Convert','Add','Mul','Div','Move']])
body+='<h3>범위 이상과 호출 허가 해제</h3>'+table(['명령·대상','정적 조건','전달값','근거'],arows([a for a in analog_actions if a['network'] in [1658,1659] and a['gate'] in ['Move','Coil']]))
body+='<p>1658의 범위 이상 분기는 OutValue에 -9999를 쓰고 Out_of_range를 출력합니다. 1659는 NOT IN0일 때 OutValue에0을 쓰며 같은 네트워크에는 Out_of_range 쓰기가 없습니다. 호출되지 않은 때의 값/플래그 유지와 현재 실행 순서는 확인 전입니다.</p>'
body+='<h2 id="flow">3. 가스 유량의 후속 하한 처리</h2>'+table(['명령·대상','정적 조건','전달값','근거'],arows([a for a in analog_actions if a['network']==1754]))+'<p>1754에는 Data.MASSICO_FLOW_GAS&lt;1이면1을 쓰는 Move가 있습니다. 1755의 공기 유량에는 같은 후속 Move를 확인하지 않았습니다. 원시값·변환 직후 값·OFR 플래그·Move 이후 값·HMI 표시를 함께 기록하고 최종 표시값만으로 정상/복구를 판정하지 않습니다.</p>'
body+='<h2 id="outputs">4. 공기272·가스285와 실제 출력</h2>'+table(['출력·백업 주소','원본 Mul·피연산자','단자 경로'],[[e(o['title']+' / '+o['address']),netlink(o['network'],o['part'])+'<br>'+table(['값 핀','식별'],pinrows(by_net[o['network']],o['part'])),'<br>'.join(e(n) for n in o['circuit']['nodes'])] for o in outputs])
body+=table(['명령·대상','정적 조건','전달값','근거'],arows([a for a in analog_actions if a['network'] in [1686,1687,1724,1834]]))+'<p>0~100 제한과 272/285 원본 계수를 보존합니다. QW 원시값과 실제 mA·서보 위치·유량은 서로 다른 확인 항목입니다. 1724의 주기 제목은 현재 CPU의 실행 주기 증거가 아니며, 복수 쓰기와 현재 ENO/호출을 확인하기 전에는 최종 값을 확정하지 않습니다.</p>'
body+='<h2 id="hmi">5. 기존 HMI 설정 참고</h2>'+table(['태그','설정 주소','Access Name'],[[e(r[k]) for k in ['HMI 태그','설정 주소','Access Name']] for r in hmi])+'<p>기존 BR01 분류의 설정 행을 그대로 연결한 참고 목록입니다. 태그명만으로 현재 DB 배치·물리 단위·실제값과 위 OutValue의 전달 일치를 확정하지 않습니다. 현재 HMI/PLC 버전과 표시 환산을 대조합니다.</p>'
body+='<h2 id="writes">6. Global/Local 범위와 전체 정적 쓰기</h2><p>알고리즘의 Local 변수는 signal linearization 블록 범위로 관리하며 같은 이름의 Global·다른 블록 Local을 합치지 않습니다. 기존 trace에서 방향 미확정으로 남은 호출 핀은 그대로 보존합니다. 백업 기존simulation 참조는 원본 구조 자료입니다.</p>'
for s in signals:
    body+='<details><summary>'+e(s['name']+' / '+s['scope']+(' / '+s['block'] if s['block'] else ''))+'</summary><p>읽기 '+str(Counter(u['role'] for u in s['usages'])['read'])+' · 쓰기 '+str(Counter(u['role'] for u in s['usages'])['write'])+' · 방향 미확정 '+str(Counter(u['role'] for u in s['usages'])['pending'])+' · 다른 범위 '+str(len(s['other_scope_usages']))+'</p>'+table(['방향·블록','명령·핀·근거'],[[e(u['role']+' / '+u['block']),netlink(u['network'],u['part'])+'<br>'+e(u['gate']+'/'+u['pin']+' / Wire '+u['wire']+' / ORef '+u['oref'])] for u in s['usages'] if u['role']!='read'])+'</details>'
body+='<h2 id="checks">7. 추가 확인</h2>'+table(['항목','관찰·확인 경계'],[[e(o['id']+' / '+o['title'])+'<br>'+e(o['status']),e(o['text'])] for o in observations[:3]])
body+='<h2 id="native">8. 원본 Part·CRef·Wire·선언</h2>'
for p in [p for p in proofs if p['network'] in analog_networks]:
    body+='<details><summary>'+e(str(p['network'])+' / '+p['block']+' / '+p['title'])+'</summary><p>'+link('원본 XML',p['file'])+' · SHA256 '+e(p['sha256'])+'</p>'+table(['Part','Gate·형식·반전'],[[e(x['uid']),e(x['gate']+' / '+json.dumps(x['attributes'],ensure_ascii=False)+' / '+json.dumps(x['templates'],ensure_ascii=False)+' / '+str(x['negated_pins']))] for x in p['parts']])+table(['호출','CRef/CodeBlock·선언'],[[e(c['callee'])+'<br>'+e(expression(c['enable'])),e('CRef '+c['uid']+' / RID '+c['cref_ref_id']+' / CodeBlock '+c['block_uid']+' / RID '+c['block_ref_id'])+'<br>'+', '.join(link('UID '+d['uid']+' RID '+d['rid']+' NID '+d['nid'],'sources/decoded-original/'+d['file']) for d in c['native_declarations'])] for c in p['calls']])+table(['Wire','연결'],[[e(w['uid']),'<br>'.join(e(x['kind']+' '+str(x['uid'] or '')+' / '+str(x['pin'] or ''))+(' · '+e(p['refs'][x['uid']]['name']) if x['kind']=='OCon' else '') for x in w['endpoints'])] for w in p['wires']])+'</details>'
body+='<p>'+link('전체 정적 근거 JSON','registers/process-measurement.json')+'</p>'
(ROOT/'measurement-trace.html').write_text(page('BR01 가스·공기 계측·환산·출력 추적',body))

body=notice+nav+'<p>1858 버너 운전 요청 해제에서 읽는15개 알람 중 공정 계측·전용반 관련11개 이름을 추적합니다. 이 목록은 버너의 모든 안전 보호 기능이나 설비별 알람 소유 관계를 확정하는 목록이 아닙니다.</p>'
body+='<h2 id="stop">1. 버너 요청 해제의 원본 조건</h2>'+table(['명령·대상','전체 정적 조건','근거'],[[e(stop['gate']+' / '+stop['name']),'<code>'+e(expression(stop['condition']))+'</code>',netlink(1858,stop['uid'])]])
existing={'Allarm.FN_03_FAULT':'alarm-guides/FN03.html','Allarm.SERVOMOTOR_MIN_POS_ALL':'burner-interface.html#reset','Allarm.BURNER_START_FAULT':'burner-interface.html#reset','Allarm.BURNER_LDU_FAULT':'burner-interface.html#reset'}
body+=table(['읽은 알람 이름','원본 근거 범위'],[[e(name),link('아래 발생·리셋 근거','#alarm-'+str(alarm_names.index(name)+1)) if name in alarm_names else link('기존 상세 근거',existing[name])] for name in stop_names])
body+='<h2 id="alarms">2. 발생·리셋·시간·값 전달 비교</h2><p>선택한 고장 이름만 연결합니다. 공유 원본 네트워크의 다른 알람·예경보·경적·부속 요청은 아래 선택 알람의 전용 조건으로 배정하지 않습니다. 정적 조건에 남은 미해석 ENO/Add/Sub는 원본 값 핀과 함께 확인합니다.</p>'
for index,a in enumerate(alarms,1):
    body+='<h3 id="alarm-'+str(index)+'">'+e(a['name'])+'</h3>'
    if not a['actions']:body+='<p>1858 읽기를 확인했고 복원된 LAD 핀 색인의 정확한 Global 쓰기는 확인하지 못했습니다. 별도 백업 SCL1719 색인 문자에는 해당 알람 대입이 표시됩니다. 현재 SCL/TIA·센서 선택·초기 Enable·호출 순서를 확인하며 문자 자료를 현재 실행 확정으로 처리하지 않습니다.</p>'+link('TC01/TC02 선택·EmergencyStop의 별도 SCL 문자 근거','regulation-manual.html#text-1719')
    body+=table(['명령·대상','전체 정적 조건','전달값','근거'],arows(a['actions']))
    body+=table(['SD·시간','전체 정적 조건','선언 근거'],[[e(t['name']+' / '+t['preset']['literal'])+'<br>'+netlink(t['network'],t['uid']),'<code>'+e(expression(t['condition']))+'</code>','<br>'.join(link('UID '+d['uid']+' / RID '+d['rid']+' / NID '+d['nid'],'sources/decoded-original/'+d['file']) for d in t['value_declarations'])] for t in a['timers']])
    if a['support_actions']:body+='<h4>비교값의 관련 연산·원본 핀</h4>'+table(['연산','값/ENO 연결'],[[e(x['gate']+' / '+x['name'])+'<br>'+netlink(x['network'],x['uid']),table(['핀·피연산자','원본 식별'],pinrows(by_net[x['network']],x['uid']))] for x in a['support_actions']])
    body+='<details><summary>Set/Reset 앞 접점·값 핀·전체 쓰기</summary>'+table(['명령·근거','연결 접점·반전','전체 값 핀'],[[netlink(x['network'],x['uid']),'<br>'.join(e(c['gate']+' '+str(c['name'])+' / Negated '+str(c['negated_pins'])) for c in x['native_upstream']['contacts']),table(['피연산자','식별'],pinrows(by_net[x['network']],x['uid']))] for x in a['actions']])+table(['방향·원본','명령·핀'],[[e(u['role'])+'<br>'+netlink(u['network'],u['part']),e(u['gate']+'/'+u['pin']+' / Wire '+u['wire']+' / ORef '+u['oref'])] for u in a['usages'] if u['role']!='read'])+'</details>'
body+='<h2 id="repair">3. 수리 관찰·복구 확인 순서</h2><ol><li>최초 알람과 센서/전용반 상태·모드·운전 응답·현재 버전을 같은 시각 기준으로 기록합니다.</li><li>원시 입력·환산값·상태 접점·기억·비교 설정과 실제 물리 상태를 구분합니다. 현재 단위·극성·계수 근거를 확인합니다.</li><li>Set 앞 조건과 시간의 원본 선언, 연산의 ENO·다른 쓰기·현재 호출을 대조합니다. 제목이나 숫자를 현재 보호값으로 확정하지 않습니다.</li><li>Reset 접점·원인 해소·래치 변화·새 기동 허가·출력·실제 응답을 각각 기록합니다. Low_Aspiration·PSL·전용반의 서로 다른 리셋 구성을 비교합니다.</li><li>미확인 쓰기·제작사 기능·자료 차이는 후속 확인으로 남깁니다. 기록 저장은 수리 완료·불일치 해소 판정을 바꾸지 않습니다.</li></ol>'
body+='<h2 id="checks">4. 추가 확인과 경계</h2>'+table(['항목·상태','관찰·필요한 확인','원본'],[[e(o['id']+' / '+o['title'])+'<br>'+e(o['status']),e(o['text']),', '.join(netlink(n) for n in o['networks'])] for o in observations[3:]])
body+='<p>기존 불일치18건·현장 확인 대장1,060건·설계 시험577건의 상태를 변경하지 않습니다. 현재 정지 원인·복구 결과·전용 연소 제어기의 내부 보호는 확인 전입니다.</p><p>'+link('전체 정적 근거 JSON','registers/process-measurement.json')+'</p>'
(ROOT/'process-stop-alarms.html').write_text(page('공정 계측·전용반 알람과 BR01 정지 원인',body))
print(json.dumps(dict(native_networks=len(proofs),input_channels=len(channels),output_channels=len(outputs),process_alarm_names=len(alarms),alarms_with_original_actions=sum(bool(a['actions']) for a in alarms),signal_scopes=len(signals),source_files=len(source_paths),simulator_behavior_tests='not_rerun'),ensure_ascii=False))
