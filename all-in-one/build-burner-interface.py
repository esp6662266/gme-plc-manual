"""BR01 interface and repair source manual. Static references only; no execution."""
from pathlib import Path
from collections import Counter
import hashlib, html, json, csv, xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parent
load=lambda f:json.loads((ROOT/f).read_text())
sha=lambda f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest()
local=lambda x:x.tag.rsplit('}',1)[-1]
canon=lambda s:str(s or '').replace('"','').casefold()
e=lambda s:html.escape(str(s))
model=load('registers/program-model.json')
trace=load('registers/signal-trace.json')
nets={n['id']:n for n in model['networks']}
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

selected=[1854,1855,1856,1857,1858,1859,1861,1862,1863,1865,1866,1867,1868,1869,1871,1872]
proofs=[native(n) for n in selected];by_net={n['network']:n for n in proofs}
source_paths={'registers/program-model.json','registers/signal-trace.json','registers/electrical-trace.json',
 'registers/plc-symbols.csv','sources/Electrical_Rev2.pdf','sources/electrical-page-text.json',
 'sources/decoded-original/network-map.json','sources/decoded-original/identifier-declarations.json'}
source_paths.update(n['file'] for n in proofs)
actions=[]
for i in selected:
    for action in nets[i]['actions']:
        a=dict(network=i,**action,native_upstream=upstream(by_net[i],action['uid']))
        if a['gate']=='SdCoil':
            v=next(x for x in a['native_upstream']['reference_pins'] if x['part']==a['uid'] and x['pin']=='value')
            decl=[d for d in declarations if d['uid']==v['oref'] and d['rid']==v['ref_id'] and d['nid']==source_map[i]['inferred_original_nid'] and d['name']==v['name']]
            assert decl and v['name']==a['preset']['literal'],(i,a['uid'])
            a['value_declarations']=decl
            source_paths.update('sources/decoded-original/'+d['file'] for d in decl)
        actions.append(a)
symbols=list(csv.DictReader((ROOT/'registers/plc-symbols.csv').open(encoding='utf-8-sig')))
signal_names=['Flag.Start_Burner','Flag.Burner_ready','Enable start burner(1)','Enable start burner',
 'Rem. Start/Stop Burner','Start Burner','Lock Burner','Programmed stop burner','Allarm.BURNER_LDU_FAULT',
 'Allarm.BURNER_START_FAULT','Allarm.SERVOMOTOR_MIN_POS_ALL','m491','APP M10.2','Rst allarm Burner',
 'Tag_142','Burner On','Inputs.Burner On','Inputs.Burner ON and OK','Burner ON and OK',
 'WorkData.BR01_State','WorkData.BR01_CleanTime','WorkData.W5','Open MV03 for washing',
 'Close MV03 for Burner Startup','Start High Flame','Foced Spark','Main flame ON',
 'Data.Burner_Panel_SetPoint','Flag AutoBurner','Flag.AUTO_BURNER','ON','OFF']
signals=[]
for name in signal_names:
    uses=[u for u in trace['usages'] if u['scope']=='Global' and canon(u['name'])==canon(name)]
    other=[u for u in trace['usages'] if u['scope']!='Global' and canon(u['name'])==canon(name)]
    source_paths.update(u['file'] for u in uses+other)
    source_paths.update(d['file'] for u in uses+other for d in u['declarations'])
    signals.append(dict(name=name,scope='Global',usages=uses,other_scope_usages=other,
        symbols=[s for s in symbols if canon(s['원본 심볼'])==canon(name)]))
circuit=next(d for d in load('registers/electrical-trace.json')['devices'] if d['id']=='BR01')
source_paths.update(r['file'] for p in circuit['paths'] for r in p['native_symbol_references'])
index=[dict(id=n['id'],index=n['index'],title=n['title'],file=n['file'],detailed=n['id'] in selected,
 legacy_source_only='simulation' in n['title'].casefold()) for n in model['networks'] if n['block']=='burner control']
source_paths.update(n['file'] for n in index)
page100=next(p['text'] for p in load('sources/electrical-page-text.json') if p['page']==100)
assert 'ENABLE SPARK FOR 3 sec' in page100
observations=[
 dict(id='BR-01',status='현재 PLC·제작사 확인 대기',title='두 Enable와 기동 요청·출력의 경계',
  text='Enable start burner(1)는 M48.0, Enable start burner는 M48.2입니다. Flag.Start_Burner 요청, Q6.5 Rem. Start/Stop Burner, M48.3 Start Burner, 버너 ON 응답을 하나의 상태로 합치지 않습니다.',networks=[1866,1868]),
 dict(id='BR-02',status='발생 쓰기 근거 추가 확인 대기',title='BURNER_START_FAULT 발생 조건 미확정',
  text='복원된 정확한 Global 참조에서는 1857/1858 읽기와 1869 Reset 쓰기를 확인합니다. 이 목록만으로 고장 미사용·발생 불가를 단정하지 않습니다. 현재 TIA 교차참조·HMI/외부 쓰기·미복원 자료를 대조합니다.',networks=[1857,1858,1869]),
 dict(id='BR-03',status='현재 유지·호출 확인 대기',title='리셋 요청과 버너반 복구의 경계',
  text='1854의 6초 APP M10.2 감시와 m491, Tag136/137의 각 2초 원본 설정을 보존합니다. Q6.7 리셋 출력, LDU 래치Reset, 원시 Lock Out의 실제 변화와 전용반 복구는 각각 기록합니다. 전체 펄스 길이·Set/Reset 우선순위를 정적 표로 확정하지 않습니다.',networks=[1854]),
 dict(id='BR-04',status='MV03 입력 전달·현재 호출 확인 대기',title='MV03 닫힘 요청과 세정 상태 전환',
  text='1868 Part1669는 같은 Inputs.MV03 Close의 정·반전 조건을 함께 읽지만, 상태7의 Part1306에는 별도 닫힘 Set이 있습니다. 세정 상태2의 Part1188은 NOT Inputs.MV03 open을 읽습니다. 전체 닫힘 요청 불가·실제 댐퍼 위치를 단정하지 않고 전달 극성·다른 쓰기·현재 호출을 대조합니다.',networks=[1868]),
 dict(id='BR-05',status='현재 TIA·제작사 시간 확인 대기',title='점화 전환 도면 문구와 원본 타이머',
  text='OEM FG99/PDF100의 전환 출력 문구는 3 sec, 1863 Part472 Tag_141의 SD 원본 선언은 S5T#4S입니다. 같은 기능·현재 개정인지 확인 전에는 설정을 수정하거나 시간값을 권장하지 않습니다. 기존 불일치18건의 상태·개수는 변경하지 않습니다.',networks=[1863]),
 dict(id='BR-06',status='카운터·ON/OFF·현재 주기 확인 대기',title='22h/24h 제목과 실제 동작 시간',
  text='1861은 OFF와 W5>=1320/1440을 읽고 1859의 Tag138 원본 설정은 1분입니다. Add의 값/호출과 ON/OFF 현재값, 다른 쓰기·리셋·CPU 주기 확인 전에는 실제 22/24시간 보호 동작을 확정하지 않습니다.',networks=[1859,1861]),
 dict(id='BR-07',status='복수 쓰기·값 전달·상태 도달 확인 대기',title='표시 상태 번호와 실제 운전 순서',
  text='1868의 상태77도 원본 그대로 보존합니다. 상태 Move 뒤 조건을 같은 스캔에 읽는지와 실제 단계 체류 시간은 확인 전입니다. Tag142는 1867/1868에 두 SD가 있고 세정 시간 Add도 별도입니다. 상태표를 실행 모델이나 실제 화염 순서로 사용하지 않습니다.',networks=[1867,1868]),
]
symptoms=[
 ('기동 요청이 들어오지 않음','모드·자동 시퀀스 종류·Flag.Start_Burner와 최초 정지 시각을 기록합니다.','공통1843/1844 요청 쓰기와 1858 해제, 1857 Burner_ready를 비교합니다. FN01/04/02·RD01 응답과 FN06 또는 버너ON 분기를 함께 기록합니다.','실제 요청 변화·새 기동 허가가 확인되지 않으면 출력/버너반 불량으로 결론 내리지 않습니다.',[1857,1858]),
 ('요청은 있으나 Q6.5 출력이 없음','Flag.Start_Burner, Lock Burner, FN03 Run, M48.0/M48.2와 Q6.5를 같은 시각 기준으로 기록합니다.','1866 Part607과611의 입력 조건, 1868의 Enable Set/Reset, 1865 Lock Set/Reset을 비교합니다.','M48.0과 M48.2를 구분합니다. 1866 FN03 요청 Part600의 OFF 현재값·다른 FN03 요청도 확인합니다.',[1865,1866,1868]),
 ('Q6.5는 있으나 버너 ON 응답이 없음','Q6.5·99KA1·X1:388/389·I17.0·Inputs.Burner On과 버너반 자체 표시/알람을 기록합니다.','FG99/PDF100 출력과 FG97/PDF98 ON 응답, 1868의 상태8/11과 ON 피드백을 구간별로 비교합니다.','코일 전원과 버너측 접점 전원을 구분합니다. 전용010-390의 허가·내부 기동 실패 근거를 추가 확보합니다.',[1866,1868]),
 ('Lock Out 발생 또는 리셋 후 재발','버너반 최초 코드·원시I17.1·LDU 래치·Reset 요청·m491·APP M10.2·Q6.7·Tag135/136/137을 기록합니다.','1854의 Set/Reset/SD와 99KA3·X1:392/393 전달을 대조합니다.','PLC 래치 해제와 실제 Lock Out 해소를 구분하고 원인/전용반 리셋 조건을 확인합니다. 반복 리셋을 해결 방법으로 기록하지 않습니다.',[1854]),
 ('세정·댐퍼 단계에 머무름','BR01_State·MV03 처리 open/Close·열림/닫힘 요청·리미트/엔코더·CleanTime·Tag142~145를 기록합니다.','1868 상태0·1·2·3·4·5·6·7·8·9·10·11·77의 원본 쓰기와 조건을 대조합니다. 1707 교정·1714 오차 감시도 관련 작업지에서 확인합니다.','상태번호를 현장 진행 완료로 대신 판정하지 않습니다. 입력 반전·150S 감시·다른 닫힘 요청·현재 교정을 확인합니다.',[1867,1868]),
 ('고화염·점화 전환 또는 설정값이 예상과 다름','원시I17.2·Inputs.Burner ON and OK·Burner ON and OK·Q7.0/Q7.1·Main flame ON·Tag139~141·패널 설정값을 기록합니다.','1862/1863 전환 출력·1868/1871/1872 설정 쓰기와 원본 값 전달 핀을 비교합니다. FG100/PDF101 아날로그는 별도 구간으로 기록합니다.','도면3초/래더4초·설정값 복수 쓰기·환산 단위와 전용 제어기 역할을 확인합니다. 출력 접점을 화염 검출 자체로 표시하지 않습니다.',[1862,1863,1868,1871,1872]),
]
data=dict(date='2026-10-08',equipment='BR01',priority_key='P11',scope='GME burner external interface and static repair evidence; dedicated combustion controller internals unverified',
 selected_networks=selected,block_index=index,native_networks=proofs,actions=actions,signals=signals,circuit=circuit,
 observations=observations,symptoms=[dict(symptom=s,observe=o,compare=c,next_check=n,networks=ids) for s,o,c,n,ids in symptoms],
 sources={f:sha(f) for f in sorted(source_paths)},field_verified=False,tia_verified=False,plc_changes=0,
 repairs_completed=0,simulator_development='stopped_by_user',simulator_behavior_tests='not_rerun')
(ROOT/'registers/burner-interface.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')

def link(label,path):return '<a href="'+e(path)+'">'+e(label)+'</a>'
def netlink(n,uid=None):return link('원본 '+str(n)+(' / Part '+str(uid) if uid else ''),'networks/network-'+str(n)+'.html')
def table(head,rows):return '<div class="table-wrap"><table><thead><tr>'+''.join('<th>'+e(h)+'</th>' for h in head)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+str(c)+'</td>' for c in r)+'</tr>' for r in rows)+'</tbody></table></div>'
def action_rows(rows):
    return [[e(a['gate']+' / '+a['name']),'<code>'+e(expression(a['condition']))+'</code>',e(expression(a['value'])) if 'value' in a else '',netlink(a['network'],a['uid'])] for a in rows]
body='<h1>BR01 · 외부 연동·정지·복구 근거</h1><div class="notice">원본 백업·OEM 회로의 정적 검토본입니다. 버너 전용반010-390 내부의 점화·화염 보호·가스 밸브·퍼지 안전 순서는 확보 전입니다. 현재 PLC/TIA·실물 동일성·현장 복구는 확인 전이며 PLC 변경0건, 시뮬레이터 작성·시험 중지.</div>'
body+='<p>운전 요청·허가·실제 출력·버너반 응답·래치/기억을 구분하여 수리 관찰 근거를 모읍니다. 원본 설정은 권장 보호값이나 실제 경과시간을 뜻하지 않습니다.</p><nav class="inline-actions">'+link('BR01 기존 수리 판단','repair-guides/P11.html')+link('외부 회로·단자','circuit-guides/BR01.html')+link('MV03 알람·복구','alarm-guides/MV03.html')+link('공통 요청·리셋','common-guides/P11.html')+link('BR01 수리 기록','index.html#view=repair-record&equipment=P11&scope=priority')+'</nav>'
body+='<div class="inline-actions">'+link('가스·공기 환산·출력 근거','measurement-trace.html')+link('공정 알람·버너 정지 원인','process-stop-alarms.html')+'</div>'
body+='<h2 id="workflow">1. 증상별 관찰·비교 순서</h2>'+table(['증상','먼저 기록','원본 비교','다음 확인'],[[e(s),e(o),e(c)+'<br>'+', '.join(netlink(n) for n in ids),e(check)] for s,o,c,check,ids in symptoms])
body+='<h2 id="boundary">2. 이름·주소·쓰기의 경계</h2><p>Global의 정확한 이름으로 찾은 전체 정적 참조입니다. 같은 단어가 포함된 태그를 추가 배정하지 않습니다. 아래 백업 주소와 처리 DB의 전달은 각각 확인하며, 참조0은 현재 신호 미사용의 증거가 아닙니다. 다른 범위와 미해석 참조·HMI/외부 쓰기는 별도 확인합니다.</p>'
body+=table(['선택 신호·범위','백업 심볼 주소','전체 정적 참조','쓰기·방향 미확정 근거'],[[e(s['name'])+' / Global','<br>'.join(e(x['백업 주소'].upper()+' / '+x['원본 심볼']) for x in s['symbols']) or 'DB/주소 추가 확인',' · '.join(e(k)+' '+str(Counter(u['role'] for u in s['usages'])[k]) for k in ['read','write','pending'])+' · 다른범위 '+str(len(s['other_scope_usages'])),'<br>'.join(netlink(u['network'],u['part'])+' '+e(u['gate']+'/'+u['pin']+(' · 백업 기존simulation블록' if u['legacy_simulation_block'] else '')) for u in s['usages'] if u['role']!='read') or '복원된 정확한 Global 쓰기/방향미확정 참조 없음'] for s in signals])
body+='<h2 id="permit">3. 기동 허가·최종 출력·정지</h2><p>1857의 Burner_ready는 GME 허가 비교이며 전용 연소 제어기 Ready·화염 확인을 대신하지 않습니다. 1858의 연관 알람은 정지 조건에서 읽은 이름이며 모두 BR01 전용 알람으로 배정하지 않습니다. ON/OFF는 현재값을 확인할 심볼입니다.</p>'+table(['명령·대상','전체 정적 조건','전달값','원본'],action_rows([a for a in actions if a['network'] in [1856,1857,1858,1861,1865,1866]]))
body+='<h2 id="reset">4. Lock Out·최소 위치·기동 고장과 리셋</h2><p>1855의 PBox 앞 조건은 기존 해석에서 지원 전으로 남습니다. 원본 핀/배선을 함께 보며 기동 고장 발생 조건을 추정하지 않습니다. PLC 래치 Reset·Q6.7 출력·버너반의 Lock Out 해소·재기동 허가는 서로 다른 확인 항목입니다.</p>'+table(['명령·대상','전체 정적 조건','전달값','원본'],action_rows([a for a in actions if a['network'] in [1854,1855,1869]]))
body+='<h2 id="sequence">5. 세정·MV03·상태 쓰기</h2><p>원본 상태값과 조건의 비교표입니다. 상태 Move 뒤의 조건을 같은 스캔에 읽는지·체류 시간·현재 도달 상태는 확인 전입니다. 행 순서나 Part UID는 실행 순서가 아닙니다. Add의 미해석 조건을 실행 가능한 모델로 대신하지 않습니다.</p>'+table(['명령·대상','전체 정적 조건','전달값','원본'],action_rows([a for a in actions if a['network'] in [1859,1867,1868]]))
body+='<h2 id="transition">6. 고화염·점화 전환·설정값</h2><p>원시 입력 I17.2와 처리 Inputs, 고화염 출력 Q7.0과 점화 전환 Q7.1, Main flame ON 기억을 구분합니다. 설정값의 Add·제한·0 쓰기와 아날로그 변환은 현재 호출·다른 쓰기·단위를 확인한 뒤 판단합니다.</p>'+table(['명령·대상','전체 정적 조건','전달값','원본'],action_rows([a for a in actions if a['network'] in [1862,1863,1871,1872]]))
body+='<h2 id="timers">7. 원본 SD 시간과 선언 근거</h2><p>시간값은 각 SD의 value 핀에 연결한 ORef/RefId/NID 선언과 대조했습니다. Tag142의 두 SD를 합치지 않으며 도면3초/Tag141 원본4초는 확인 대기로 남깁니다.</p>'+table(['SD·원본','시간·정적 조건','LiteralConstant 선언'],[[e(a['name'])+'<br>'+netlink(a['network'],a['uid']),'<code>'+e(expression(a['preset']))+'</code><br>'+e(expression(a['condition'])),'<br>'.join(link('UID '+d['uid']+' / RID '+d['rid']+' / NID '+str(d['nid']),'sources/decoded-original/'+d['file']) for d in a['value_declarations'])] for a in actions if a['gate']=='SdCoil'])
body+='<h2 id="circuit">8. GME ↔ 외부 버너반 회로</h2><p>'+e(circuit['equipment'])+'</p><p>'+e(circuit['distinction'])+'</p>'+table(['신호·주소','도면·경로','비교 경계'],[[e(p['signal'])+'<br>'+e(p['backup']),link('FG '+str(p['fg'])+' / PDF '+str(p['fg']+1),'sources/Electrical_Rev2.pdf#page='+str(p['fg']+1))+'<br>'+'<br>'.join(e(n) for n in p['nodes']),e(p['check'])] for p in circuit['paths']])
body+='<h2 id="checks">9. 추가 확인 항목</h2>'+table(['항목·상태','원본 관찰·확인 범위','근거'],[[e(o['id']+' / '+o['title'])+'<br>'+e(o['status']),e(o['text']),', '.join(netlink(n) for n in o['networks'])] for o in observations])
body+='<h2 id="native">10. 원본 접점·핀·Wire</h2><p>명령의 in/pre/en 입력을 원본 배선에서 역추적했습니다. 접점표의 정렬과 UID는 실행 순서가 아닙니다. 비교 명령·미지원 명령의 값 핀도 별도 표시하며 논리를 평가하지 않습니다.</p>'
for n in proofs:
    rows=[a for a in actions if a['network']==n['network']]
    body+='<details><summary>'+e(str(n['network'])+' · '+n['title'])+' / '+str(len(rows))+'개 원본 명령</summary><p>'+link('원본 XML',n['file'])+' · '+netlink(n['network'])+' · SHA256 '+e(n['sha256'])+'</p>'
    body+=table(['대상 명령','앞 연결 접점','피연산자·원본 식별'],[[e(a['gate']+' '+a['name'])+'<br>Part '+e(a['uid']),'<br>'.join(e(c['gate']+' '+str(c['name'])+' / Negated '+(','.join(c['negated_pins']) or '없음')) for c in a['native_upstream']['contacts']),'<br>'.join(e(x['gate']+'/'+str(x['pin'])+' '+str(x['name'])+' / Part '+x['part']+' / Wire '+x['wire']+' / ORef '+x['oref']+' / RID '+str(x['ref_id'])) for x in a['native_upstream']['reference_pins'])] for a in rows])
    body+=table(['Part','Gate·반전'],[[e(x['uid']),e(x['gate']+' / '+(','.join(x['negated_pins']) or '없음'))] for x in n['parts']])+table(['Wire','원본 연결'],[[e(w['uid']),'<br>'.join(e(x['kind']+' '+str(x['uid'] or '')+' / '+str(x['pin'] or ''))+(' · '+e(n['refs'][x['uid']]['name'])+' / RID '+e(n['refs'][x['uid']]['ref_id']) if x['kind']=='OCon' else '') for x in w['endpoints'])] for w in n['wires']])+'</details>'
body+='<h2 id="index">11. 원본 버너 블록 전체 색인·분석 범위</h2><p>선택16개 네트워크의 원본 명령을 상세 대조했습니다. 나머지는 원본 색인과 기존 작업지에서 추가 검토합니다. 기존 simulation 제목은 백업 원본의 구조이며 시뮬레이터 작성·실행을 뜻하지 않습니다.</p>'+table(['원본','제목','상세 대조 범위'],[[netlink(n['id']),e(n['title']),e('이번 상세대조' if n['detailed'] else '기존 원본 색인 / 백업 기존블록' if n['legacy_source_only'] else '기존 원본 색인 / 추가검토')] for n in index])
body+='<p>'+link('전체 정적 근거 JSON','registers/burner-interface.json')+'</p>'
page='<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BR01 외부 연동·정지·복구 근거</title><link rel="stylesheet" href="assets/all-in-one.css"><style>main{max-width:1320px;margin:auto;padding:24px}td{vertical-align:top}code{white-space:normal;overflow-wrap:anywhere}details{margin:16px 0}summary{cursor:pointer}</style></head><body><main>'+body+'</main></body></html>'
(ROOT/'burner-interface.html').write_text(page)
print(json.dumps(dict(burner_networks=len(proofs),actions=len(actions),timers=sum(a['gate']=='SdCoil' for a in actions),signals=len(signals),symptoms=len(symptoms),source_files=len(source_paths),plc_changes=0,simulator_behavior_tests='not_rerun'),ensure_ascii=False))
