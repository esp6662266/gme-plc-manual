"""Build three passive-body manuals from reviewed drawings and preserved PLC sources."""
from pathlib import Path
from html import escape as e
import hashlib,json,runpy,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
inputs={}
def load(p):
    inputs[p]=sha(ROOT/p);return json.loads((ROOT/p).read_text())
def ref(p,label):
    if p.split('#')[0]!='registers/body-manual.json':assert (ROOT/p.split('#')[0]).is_file(),p
    return '<a href="'+e(p,quote=True)+'">'+e(str(label))+'</a>'
def table(headers,rows):
    return '<div class="table-wrap"><table><thead><tr>'+''.join('<th>'+e(h)+'</th>' for h in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+str(v)+'</td>' for v in r)+'</tr>' for r in rows)+'</tbody></table></div>'
details=runpy.run_path(str(ROOT/'body-source-details.py'))
profiles=details['PROFILES'];cables=details['CABLE_ROWS'];checks=details['CHECKS'];status_notes=details['EQUIPMENT_STATUS_NOTES']
inputs['body-source-details.py']=sha(ROOT/'body-source-details.py')
inputs['build-body-manual.py']=sha(ROOT/'build-body-manual.py')
specs={s['id']:s for s in load('registers/control-spec.json')['specifications']}
manual_ranges=details.get('MANUAL_EXCLUSION_RANGES',[])
for boundary in manual_ranges:
    for i in range(boundary['start'],boundary['end']+1):
        ident=boundary['prefix']+str(i).zfill(2)
        if ident in specs:status_notes.append(dict(boundary,id=ident))
sensors={c['id']:c for c in load('registers/sensor-measurement.json')['channels']}
nets={n['id']:n for n in load('registers/program-model.json')['networks']}
regulation=load('registers/regulation-manual.json')
construction=load('registers/construction-reference.json')
hub=load('registers/evidence-review.json')
reviewer=load('registers/body-independent-review.json')
for f,h in reviewer['source_hashes'].items():assert sha(ROOT/f)==h,f
ab01=load('registers/ab01-independent-investigation.json')
for item in ab01['sources']:
    if item['file'].startswith('sources/'):
        assert sha(ROOT/item['file'])==item['sha256'],item['file']
        inputs[item['file']]=item['sha256']
freeze=load('registers/simulator-freeze.json')
for p,h in freeze['files'].items():assert sha(ROOT/p)==h,p
for p in ['sources/PID_1684n002I.pdf','sources/Electrical_Rev2.pdf','sources/Electrical_Can_Decoating_20241118.pdf','assets/PID-landscape.png','registers/body-pid-render-verification.json']:inputs[p]=sha(ROOT/p)
review_images=['assets/construction/P'+str(p).zfill(2)+'.png' for p in [3,6,21,53,56,57,64]]+['assets/sensor-circuits/FG'+str(f)+'.png' for f in [77,78,80,81]]
for p in review_images:inputs[p]=sha(ROOT/p)
for p in profiles:
    s=specs[p['id']];assert s['kind']=='passive' and not s['outputs'] and not s['networks']
    p['direct_spec_counts']={k:len(s[k]) for k in ['inputs','outputs','hmi','networks','direct_rules']}
    p['identity_verified']=False;p['field_verified']=False;p['tia_verified']=False
    p['sensor_references']=[dict(id=i,raw_symbol=sensors[i]['raw_symbol'],network=sensors[i]['network'],bindings=sensors[i]['call']['bindings'],circuit=sensors[i]['circuit'],ownership_verified=False,kind='source reference context') for i in p['sensors']]
    p['network_ids']=sorted(set(p['networks']+[sensors[i]['network'] for i in p['sensors']]))
    p['symptoms']=[dict(id=c[0],title=c[1],observe=c[2],compare=c[3],reasoning=c[4],next=c[5],paths=c[6],field_verified=False,repair_completed=False) for c in p.pop('cases')]
    p['checks']=[c[0] for c in checks if p['id'] in c[1]]
    p['pid_image']='assets/body-pid/'+p['id']+'.png';inputs[p['pid_image']]=sha(ROOT/p['pid_image'])
selected_ids=sorted({n for p in profiles for n in p['network_ids']})
from importlib.machinery import SourceFileLoader
helpers=SourceFileLoader('body_native_evidence',str(ROOT/'body-native-evidence.py')).load_module()
inputs['body-native-evidence.py']=sha(ROOT/'body-native-evidence.py')
network_map={n['document_id']:n for n in load('sources/decoded-original/network-map.json')}
declarations=load('sources/decoded-original/identifier-declarations.json')
def source_hash(p):inputs[p]=sha(ROOT/p)
native_proof=helpers.collect(ROOT,nets,network_map,declarations,source_hash)
native=[]
for n in selected_ids:
    original=nets[n];path=original['file'];inputs[path]=sha(ROOT/path)
    tree=ET.parse(ROOT/path)
    tag=lambda x:x.tag.rsplit('}',1)[-1]
    parts=[x for x in tree.iter() if tag(x)=='Part'];wires=[x for x in tree.iter() if tag(x)=='Wire'];orefs=[x for x in tree.iter() if tag(x)=='ORef']
    native.append(dict(id=n,block=original['block'],title=original['title'],file=path,sha256=inputs[path],native_parts=len(parts),native_wires=len(wires),native_orefs=len(orefs),reference_only=True,ownership_verified=False,evidence=native_proof(n)))
selected_rows=[dict(page=p,id=i,ends=ends,description=d,kind=k,cable=c,note=note,visually_reviewed=True,current_wiring_verified=False) for p,i,ends,d,k,c,note in cables]
review=[dict(id=i,equipment=eq,title=t,observation=o,next_check=n,status='확인 대기',resolved=False,field_verified=False) for i,eq,t,o,n in checks]
for c in review:
    c['excluded_from_current_analysis']=c['id']=='BODY-07'
    if c['excluded_from_current_analysis']:c['status']='상세 조사 제외 · 사용자 제공 철거'
counts=dict(profiles=3,symptom_cases=sum(len(p['symptoms']) for p in profiles),sensor_reference_contexts=sum(len(p['sensor_references']) for p in profiles),unique_sensor_references=len({i for p in profiles for i in p['sensors']}),native_networks=len(native),native_parts=sum(n['native_parts'] for n in native),native_wires=sum(n['native_wires'] for n in native),native_orefs=sum(n['native_orefs'] for n in native),native_declarations=sum(len(r['declarations']) for n in native for r in n['evidence']['references'].values()),selected_visible_cable_rows=len(selected_rows),body_check_records=len(review),body_checks_pending=sum(not c['excluded_from_current_analysis'] for c in review),body_checks_excluded=sum(c['excluded_from_current_analysis'] for c in review),original_conflicts_preserved=18,original_pending_checks_preserved=1060,tests_designed_preserved=577,tests_executed=0,field_verified=0,plc_changes=0)
alarm_paths=[dict(id=x['id'],network=x['network'],target=x['target'],set=x['set'],reset=x['reset'],boundary=x['boundary'],field_verified=False) for x in ab01['core_facts'] if 'set' in x]
record=dict(project_work_scope=details.get('PROJECT_WORK_SCOPE',{}),equipment_status_notes=status_notes,manual_exclusion_ranges=manual_ranges,independent_review='registers/body-independent-review.json',alarm_paths=alarm_paths,alarm_investigation='registers/ab01-independent-investigation.json',date='2026-10-09',scope='passive-body source boundaries and repair worksheets; no new equipment ownership or PLC control',profiles=profiles,counts=counts,native=native,cable_rows=selected_rows,checks=review,masked_cable_rows_excluded=[dict(page=53,id='3_5')]+[dict(page=56,id='6_'+str(i)) for i in range(7,11)],existing_review_references=['construction:C02','source:MV04-MC04'],sources=inputs,source_roles=dict(pid='historical process diagram; current installation/settings unverified',oem='circuit labels and reference addresses; current wiring/configuration unverified',construction='zone/junction/cable references; approved/as-built unverified'),direct_io_assignments=0,current_values_written=0,field_verified=False,tia_verified=False,plc_changes=0,simulator_development='stopped_by_user',simulator_behavior_tests='not_rerun')
style='''body{margin:0;padding:24px;background:#f2f6f9;color:#183247;font:16px/1.7 system-ui,sans-serif}main{max-width:1350px;margin:auto}h1{font-size:27px}h2{font-size:23px}section{margin:20px 0;padding:24px;background:white;border:1px solid #d8e5ed;border-radius:12px}.notice{background:#fff5db;border-left:5px solid #d7a832;padding:14px}nav a,a.chip{display:inline-block;margin:5px 12px 5px 0}a{color:#06678d}.table-wrap{overflow:auto}table{width:100%;border-collapse:collapse;font-size:14px}td,th{padding:12px;border-bottom:1px solid #dbe5ee;text-align:left;vertical-align:top}th{background:#eaf2f7}.pid{width:100%;max-height:630px;object-fit:contain;background:white}details{border:1px solid #cddce7;margin:14px 0;padding:14px;border-radius:8px}summary{cursor:pointer;font-weight:700}dt{font-weight:700;margin-top:14px}dd{margin:5px 0}.stats{display:flex;flex-wrap:wrap;gap:12px}.stats div{padding:12px;background:#e8f1f6;border-radius:8px}:target{outline:3px solid #d5a800}.muted{color:#556b7a}@media(max-width:720px){body{padding:10px}section{padding:12px}}@media print{body{background:white;padding:0}section,details{break-inside:avoid;border:0}details> :not(summary){display:block!important}.table-wrap{overflow:visible}.pid{max-height:450px}}'''
body='<h1>CC01·AB01·HE01 본체 매뉴얼</h1><p>본체 증상, 주변 장치의 제어와 계측, 시공 구역·접속함을 구분해 근거를 비교합니다.</p><div class="notice">세 설비의 실물 동일성은 후보 상태입니다. 현재 TIA·현장 수리 확인 전이며 본체에 주변 PLC 태그를 새로 배정하지 않습니다. 시뮬레이터 작성·수정·행동 시험은 중지합니다.</div><nav>'+''.join('<a href="#body-'+p['id']+'">'+e(p['title'])+'</a>' for p in profiles)+'<a href="#cables">선택 케이블32행</a><a href="#checks">확인 대기7건 · 조사 제외1건</a><a href="#native">원본 래더</a></nav>'
body+='<div class="stats">'+''.join('<div><b>'+str(v)+'</b><br>'+e(label)+'</div>' for label,v in [('본체',3),('증상 작업지',counts['symptom_cases']),('참조 계측',counts['unique_sensor_references']),('원본 네트워크',len(native))])+'</div>'
for p in profiles:
    ident=p['id'];body+='<section id="body-'+ident+'"><h2>'+e(p['title'])+'</h2><p>'+e(p['boundary'])+'</p><p class="muted">기존 명세: 입력 참조'+str(p['direct_spec_counts']['inputs'])+' · 출력0 · HMI0 · 전용LAD0. 여기의 계측/래더 목록은 주변 관계의 참조이며 새 직접 제어 할당이 아닙니다.</p>'
    if ident=='HE01':body+='<div class="notice" id="status-MV04">MV04는 철거됨 · 사용자 제공(2026-10-09). 현재 상세 조사에서 제외합니다. 아래 MV04 유로·케이블은 과거 도면 참조이며 현재 설치를 뜻하지 않습니다. 현장 실물 검증으로 표시하지 않습니다.</div>'
    body+='<div id="flow-'+ident+'"><h3>P&ID에서 보는 공정 경계</h3><img class="pid" src="'+p['pid_image']+'" alt="P&ID 원본에서 추출한 '+ident+' 주변 공정"><p>'+e(p['pid'])+'</p><p class="muted">원본 일부를 잘라 표시했습니다. 새로 그린 연결선·실시간 값·정밀 기계도는 아닙니다.</p>'+ref('sources/PID_1684n002I.pdf#page=1','P&ID 전체')+'</div>'
    body+='<nav>'+ref('devices/'+ident+'.html','기존 본체 매뉴얼')+ref('control-specs/'+ident+'.html','기존 명세')+ref('procedures/'+ident+'.html','진단 절차')+ref('construction-guides/'+ident+'.html','시공 자료')+ref('index.html#view=repair-record&equipment='+p['priority']+'&scope=priority','관찰·수리 기록')+'</nav>'
    body+='<h3>주변 설비의 역할·제어를 따로 보기</h3><p>'+''.join(ref('control-specs/'+i+'.html',i+(' · 철거됨 / 과거 자료' if i=='MV04' else '')) for i in p['related'])+'</p><h3>계측 참조 · 설치 위치·소유 확인 전</h3>'
    body+=table(['참조','OEM 회로·원본 설명','환산 전달·PLC 근거','확인 경계'],[[ref('sensor-measurement.html#sensor-'+c['id'],c['id']),e(c['raw_symbol']['백업 주소'].upper()+' · '+c['raw_symbol']['설명'])+'<br>'+ref('sources/Electrical_Rev2.pdf#page='+str(c['circuit']['page']),'FG'+str(c['circuit']['fg'])+' / PDF'+str(c['circuit']['page'])),e(c['circuit']['path'])+'<br>'+e(json.dumps(c['bindings'],ensure_ascii=False))+'<br>'+ref('networks/network-'+str(c['network'])+'.html','원본 '+str(c['network'])), '도면→실제 취출부→전원/단자→원시값→환산→표시. 단위·현재 설정·사용 여부 확인 전'] for c in p['sensor_references']])
    body+='<h3 id="symptoms-'+ident+'">증상별 조사·원인 배제·후속 확인</h3>'
    for c in p['symptoms']:
        body+='<details id="'+c['id']+'"><summary>'+e(c['id']+' · '+c['title'])+'</summary><dl>'+''.join('<dt>'+label+'</dt><dd>'+e(c[key])+'</dd>' for label,key in [('관찰할 내용','observe'),('도면·PLC에서 비교','compare'),('원인 후보를 나누는 근거','reasoning'),('필요 자료·복구 확인','next')])+'</dl><p>'+''.join(ref(path,'근거 '+str(i+1)) for i,path in enumerate(c['paths']))+'</p><p class="muted">자료 기반 점검 안내입니다. 실제 관찰·수리 완료·정상 판정은 기록되지 않았습니다.</p></details>'
    if ident=='AB01':
        body+='<div id="alarms-AB01"><h3>온도 알람·리셋·버너 요청 경계</h3><p>백업 원본의 정적 조건입니다. 아래 상수는 현재 승인된 운전값·보호값을 뜻하지 않습니다. 원인 해소·래치 해제·새 요청·허가·최종 출력·실물 복구를 각각 확인합니다.</p>'
        body+=table(['알람·원본','발생 조건','래치 해제·후속 동작','확인 경계'],[
            [ref('networks/network-1979.html','MAX_TC01_TEMP · 1979'),'ON 및 PID_Ref_Temp > TC01_MAX_ALL → Tag_99 SD(S5T#6S) → Set. 비교 분기와 타이머 접점이 함께 연결됨.','ON 및 자기 래치 → Int Sub(TC01_MAX_ALL,5) → Local app00; Sub.eno → Real Lt(PID_Ref_Temp,app00) → Reset와 Flag.STOP_HORN Set. 이 분기에는 RESET_ALLARM 접점 없음.','Int 연산과 Real 비교 형식, ENO·현재 값·단위는 확인 전.'],
            [ref('networks/network-1979.html','MAX_MAX_TC01_TEMP · 1979'),'ON 분기: TC01_MAX_ALL+20의 Local max_max_tc1, PID_Ref_Temp > max_max_tc1 OR >1250.0 OR <−60.0 → Tag_100 SD(S5T#6S) → Set.','ON AND Flag.RESET_ALLARM AND 자기 래치 → Reset. 원인 온도 정상 접점은 이 Reset 분기에서 확인되지 않음.','Add.en과 비교.pre는 ON에서 분기하며 Add.eno의 직렬 허가가 아님.'],
            [ref('networks/network-1986.html','TC01_TC02_COMP_FAULT · 1986'),'ON AND NOT TC01-TC02control disable AND (Temp_TC01>400 OR Temp_TC02>400). Int Sub 차이 app02가 <−100 OR >100 → Tag_108 SD(S5T#1M) → Set.','ON AND Flag.RESET_ALLARM AND 자기 래치 → Reset. disable·온도·차이·타이머 발생 경로와 별도 분기.','disable은 반전 접점. Sub.en과 차이 비교.pre는 Wire809에서 병렬 분기. ±100과 같은 값은 범위 밖 비교가 아님.']])
        body+='<p>'+ref('networks/network-1856.html','1856 온도 인터록')+': ON AND NOT MAX_MAX_TC09 AND NOT MAX_MAX_TC01_TEMP → Temperature Interlock OK Coil. MAX와 MAXMAX를 구분합니다.</p><p>'+ref('networks/network-1858.html','1858 버너 요청 정지')+': MAXMAX·두 온도 비교 고장·EmergencyStopTC1_2 등이 OR 분기로 Flag.Start_Burner를 Reset합니다. 선택 원본에 MAX_TC01_TEMP의 같은 이름 참조는 없습니다.</p><p>'+ref('networks/network-1866.html','1866 허가·원격 출력')+': Start_Burner AND NOT Lock Burner AND Inputs.FN03 Run → Enable start burner(1)(M48.0). 같은 분기 AND Enable start burner(M48.2) → Rem. Start/Stop Burner(Q6.5). 두 Enable과 물리 화염 응답을 합치지 않습니다.</p>'
        body+='<details id="selection-AB01"><summary>1719 입력 선택 SCL 색인 · 원형/현재 동작 확인 전</summary><p>두 채널 Enable과 OFR에 따라 평균 또는 단독 값을 PID_Ref_Temp로 쓰고 EmergencyStopTC1_2로 전달하는 검색색인 문자가 있습니다. TC02 단독 분기에서도 원문은 TC01_OFR 확인·EnableTC01 := false입니다. TC02로 바꾸어 해석하거나 현재 프로그램의 오류로 확정하지 않습니다. 원형 SCL·컴파일 목록·현재 CPU와 DB가 필요합니다.</p>'+ref('regulation-manual.html#loop-BR01','기존 입력 선택·조절 자료')+' · '+ref('sources/live_index.json','보존 검색색인')+'</details><p>'+ref('registers/ab01-independent-investigation.json','조사 근거·정확한 Part/Wire/선언')+' · '+ref('AB01-INVESTIGATION.md','조사 설명')+'</p></div>'
    body+='<h3>이 본체에 남은 확인</h3><ul>'+''.join('<li><a href="#'+i+'">'+i+'</a></li>' for i in p['checks'])+'</ul><p>씰·내화재·재질·조임값·허용 온도/압력·점검/세정 주기와 내부 작업은 최신 제작사 자료 및 승인된 현장 절차로 확인합니다. 관찰 기록에는 근거 버전·실제 위치·조치 전후 조건을 남깁니다.</p></section>'
body+='<section id="cables"><h2>눈으로 확인한 선택 케이블 행</h2><p>LOC는 시공 구역/접속 참조입니다. 실제 장치 소유나 현재 배선을 증명하지 않습니다. 가려진53페이지3_5,56페이지6_7–6_10은 제외합니다. 제목/재질/전류 종류/심선 수는 도면 표기이며 현재 설치 규격은 확인 전입니다.</p>'+table(['원본 행','양단·설명','도면 표기','구분할 경계'],[[ref('sources/Electrical_Can_Decoating_20241118.pdf#page='+str(r['page']),'PDF'+str(r['page'])+' / '+r['id']),e(r['ends'])+'<br>'+e(r['description']),e(r['kind']+' · '+r['cable']),e(r['note'])] for r in selected_rows])+'</section>'
body+='<section id="checks"><h2>본체 자료 확인 대기7건 · 조사 제외1건</h2><p>아래는 별도의 본체 자료 수집 작업지입니다. 원본 불일치18건·기존 확인1060건·검토64건의 해소/완료 상태를 변경하지 않습니다. 버너 반복 케이블C02와 MV04-MC04는 기존 항목을 참조하며 자동 수정하지 않습니다.</p>'
for c in review:body+='<details id="'+c['id']+'"><summary>'+e(c['id']+' · '+c['title'])+'</summary><p>'+e(c['observation'])+'</p><p><b>다음 확인:</b> '+e(c['next_check'])+'</p><p>'+e(c['status'])+' · 원본 불일치 해소 판정 아님</p></details>'
body+='<p>'+ref('BODY-INDEPENDENT-REVIEW.md','독립 도면 검토·표현 수정 근거')+' · '+ref('registers/body-independent-review.json','원본 대조·그림 비교·AB01 재검토')+'</p><p class="muted">P&amp;ID와 OEM 선택 그림은 새 원본 렌더와 픽셀 일치를 확인했습니다. 시공 선택 그림7개는 같은 크기의 새 렌더와 픽셀 차이가 있어 전체 의미 동일성을 해시만으로 확정하지 않습니다. 선택 케이블과 표기는 도면의 보이는 행을 시각 대조한 범위입니다.</p>'
body+='</section><section id="native"><h2>주변 제어·환산의 원본 LAD</h2><p>목록은 참조 범위입니다. 본체 전용 제어·현재 호출 순서·실행을 의미하지 않습니다. 미해석 핀·상수와 다른 쓰기는 기존 네트워크/신호 작업지에서 따로 확인합니다.</p>'+table(['네트워크','블록·제목','원본 규모','원본XML'],[[ref('networks/network-'+str(n['id'])+'.html',n['id']),e(n['block']+' / '+n['title']),e(f"Part {n['native_parts']} / Wire {n['native_wires']} / ORef {n['native_orefs']}"),ref(n['file'],'복원 원본')] for n in native])+'</section><p>'+ref('registers/body-manual.json','본문 근거 JSON')+' · '+ref('requirements-audit.html','전체 작성 상태')+' · '+ref('operator-guide.html','사용 안내')+'</p>'
(ROOT/'registers/body-manual.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
(ROOT/'body-manual.html').write_text('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>본체 매뉴얼·수리 | GME</title><style>'+style+'</style></head><body><main>'+body+'</main></body></html>')
print(json.dumps(dict(status='built',counts=counts,source_hashes=len(inputs)),ensure_ascii=False))
