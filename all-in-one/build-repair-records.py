"""Derive blank, source-linked repair record forms; never execute control logic."""
from pathlib import Path
import hashlib, json

ROOT=Path(__file__).resolve().parent
source=ROOT/'registers/repair-decision.json'
repair=json.loads(source.read_text())
hub=json.loads((ROOT/'registers/evidence-review.json').read_text())
electrical=json.loads((ROOT/'registers/electrical-trace.json').read_text())
construction=json.loads((ROOT/'registers/construction-reference.json').read_text())
circuits={r['id']:r for r in electrical['devices']}
installations={r['id']:r for r in construction['profiles']}
evidence_sources={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in
    ['registers/repair-decision.json','registers/evidence-review.json',
     'registers/electrical-trace.json','registers/construction-reference.json','registers/alarm-recovery.json','registers/burner-interface.json','registers/process-measurement.json','registers/sensor-measurement.json','registers/regulation-manual.json','registers/encoder-position.json','registers/hmi-transfer.json','registers/recipe-settings.json','registers/body-manual.json','registers/unresolved-identity.json']}

# These are evidence collection instructions, not additional PLC conditions.
# Keep declared, exact-reference-related and global review contexts distinct.
review_steps={
    'source:BASELINE':['preflight'], 'source:ADDRESS':['preflight','response'],
    'source:SOURCE-XML':['preflight'], 'source:POWER':['preflight','response'],
    'source:VOLTAGE':['preflight','response'], 'source:FN04':['preflight','permit','response'],
    'source:PV01-LS02':['response'], 'source:MV04-MC04':['response'],
    'source:FN01-FAN':['preflight','response'], 'source:MV06-LS':['response'],
    'source:TC05':['response','stop'], 'source:BR01':['preflight','response','recovery'],
    'source:PID-TM':['response','recovery'],
    'common:COM-01':['request','permit','stop','recovery'],
    'common:COM-02':['request','stop'], 'common:COM-03':['request'],
    'common:COM-04':['request','stop'], 'common:COM-05':['recovery'],
    'common:COM-06':['permit','stop','recovery'], 'common:COM-07':['preflight','recovery'],
    'common:COM-08':['request','permit','response'],
    'common:COM-09':['permit','stop','recovery'], 'common:COM-10':['request','stop','recovery'],
    'improvement:IMP-01':['stop','recovery'], 'improvement:IMP-02':['permit','stop'],
    'improvement:IMP-03':['request','permit'], 'improvement:IMP-04':['stop','recovery'],
    'improvement:IMP-05':['permit','stop'], 'improvement:IMP-06':['permit','response'],
}
requirements={
 'request':[
  ('현재 PLC·TIA','현재 모드·공정 종류·요청 비트와 해당 Set/Reset의 호출 조건·다른 쓰기를 같은 시각 기준으로 대조합니다. 단계 값의 실제 시간은 OB 설정 근거가 있어야 합니다.'),
  ('HMI·현장 기록','최초 조작·요청 변화·공정 단계의 시각과 화면/알람 기록 위치를 남깁니다. 원본 HMI 태그의 존재만으로 현재 전달을 확정하지 않습니다.')],
 'permit':[
  ('현재 PLC·TIA','최종 출력 네트워크의 각 피연산자·모드·현재 호출과 다른 출력 쓰기를 대조합니다. 미해석 참조와 관찰하지 않은 값은 미확인으로 남깁니다.'),
  ('현장·회로 자료','PLC 논리 허가와 현장 직렬 접점·구동기 허가를 분리합니다. 현재 모듈 주소·단자·표찰과 승인된 회로 개정 근거를 남깁니다.')],
 'response':[
  ('현장·회로 자료','PLC 최종 출력 → 단자/릴레이 → 구동기 입력 → 실제 장치, 원시 센서 → 물리 입력 → 내부 응답을 구간별로 구분해 관찰값·시각·근거를 기록합니다.'),
  ('현재 PLC·TIA','원시 입력과 처리 응답의 전달·반전·복수 쓰기·현재 호출을 확인합니다. 내부 기억 또는 공통 구동기 응답만으로 개별 장치의 동작을 확정하지 않습니다.'),
  ('제작사·현재 설정','구동기/센서의 모델·접점 기능·정상 극성·신호 범위·환산 설정을 현재 파라미터와 해당 모델 매뉴얼의 개정/페이지로 대조합니다.')],
 'stop':[
  ('현장·알람 이력','최초 알람, 주변 설비 응답, 요청 해제, 출력 해제의 시각을 구분해 보존합니다. 후속 알람만으로 최초 원인을 확정하지 않습니다.'),
  ('현재 PLC·TIA','관련 감시 Set/Reset·타이머·공통 정지 단계와 현재 호출을 대조합니다. 원본 설정값과 실제 경과시간을 별도로 기록합니다.')],
 'recovery':[
  ('현재 PLC·TIA','원인 입력·래치·리셋 요청/출력·새 요청·허가·응답·유지 설정을 각각 대조합니다. 리셋 출력만으로 원인 해소를 판단하지 않습니다.'),
  ('현장·제작사 자료','제작사의 해당 모델 복구 기준과 승인된 운전 절차, 실제 수행한 조치, 복구 이후 관찰·연동 결과를 기록합니다. 근거 없는 허용값·재기동 순서를 만들지 않습니다.')],
 'identity':[
  ('현장·설비 자료','명판·설비 카드 ID·위치·본체/구동부·제어반·전용 제어기의 식별 근거와 사진 위치를 기록합니다.'),
  ('제작사·설계 자료','P&ID 연결과 해당 본체/전용 제어기의 모델·승인 개정본·I/O 목록을 확보한 후 대응을 대조합니다. 다른 장치의 태그를 대신 배정하지 않습니다.')],
 'local':[
  ('현장·알람 이력','발생 위치·시각·본체 증상과 주변 장치의 상태를 별도로 기록하고 전용 제어기의 최초 알람과 비교합니다.'),
  ('제작사·해당 제어기','전용 매뉴얼의 수치·허용값·점검 기준과 실제 모델/개정을 대조합니다. GME 연동은 확인된 접속 자료가 있을 때만 연결합니다.')],
}

def reviews_for(record, stage):
    result=[]
    for item in hub['items']:
        if item['kind']=='identity' and item['source_id']!=record['key']:continue
        primary=record['plc_id'] and record['plc_id'] in item['equipment_ids']
        related=record['plc_id'] and record['plc_id'] in item['related_equipment_ids']
        identity=item['kind']=='identity' and item['source_id']==record['key']
        if not (primary or related or identity or item['global_scope']):continue
        if item['kind']=='identity':stages=['preflight','identity']
        elif item['kind']=='construction':stages=['preflight','response'] if record['boundary']=='source_linked' else ['preflight','identity','local']
        else:stages=review_steps.get(item['id'],['preflight'])
        # No common-control steps are assigned to an unidentified/passive body.
        if record['boundary']!='source_linked' and item['kind']=='common':continue
        if stage not in stages:continue
        relationship='identity' if identity else 'declared' if primary else 'related' if related else 'global'
        result.append(dict(id=item['id'],title=item['title'],relationship=relationship,
            observation=item['observation'],next_check=item['next_check'],status=item['source_status'],
            links=item['links'],source_file=item['source_file']))
    return result

def evidence_plan(record):
    linked=record['boundary']=='source_linked'
    circuit=circuits.get(record['plc_id']) if linked else None
    install=installations.get(record['plc_id']) if linked else None
    preflight=dict(requirements=[
        dict(owner='현장·설비 자료',work='명판·실물 설비 ID·위치·본체와 구동부·제어 주체를 먼저 대조하고 사진/자료 위치를 기록합니다.'),
        dict(owner='현재 PLC·TIA',work='백업 파일명과 현재 프로젝트/CPU의 일치 여부, 비교한 프로젝트 버전·블록·주소·비교 시각을 남깁니다. 백업만으로 현재 설치 프로그램 일치를 확정하지 않습니다.')
    ],reviews=reviews_for(record,'preflight'))
    if not linked:preflight['requirements'][1]=dict(owner='제작사·전용 제어기',work='해당 설비의 제어 주체·모델·I/O·알람·승인된 운전 자료를 식별합니다. PLC 대응 미확정 또는 본체 후보에는 다른 장치의 제어 조건을 부여하지 않습니다.')
    steps=[]
    for decision in record['decisions']:
        key=decision['id']
        wanted={'request':['requests'],'permit':['requests','outputs'],
            'response':['outputs','responses'],'stop':['requests','outputs','responses'],
            'recovery':['requests','outputs','responses']}.get(key,[])
        refs=[dict(label='레시피·설정값·전원 복귀의 다른 쓰기 확인',path='recipe-settings.html#profile-'+record['key']),dict(label='HMI 기존 태그·주소·표시/요청 연결 확인',path='hmi-transfer.html#profile-'+record['key'])]
        if record['key'] in ['P03','P04','P14']:refs.append(dict(label='식별·자료 후보·배정하지 않는 근거',path='unresolved-identity.html#identity-'+record['key']))
        if record['plc_id'] in ['CC01','AB01','HE01']:
            anchor=('flow-' if key=='identity' else 'symptoms-' if key=='local' else 'body-')+record['plc_id']
            refs.append(dict(label='본체·공정/계측 경계·증상별 수리 근거',path='body-manual.html#'+anchor))
        for binding in record['bindings']:
            if binding['role'] in wanted:
                refs.extend(dict(label=binding['name']+' · 원본 '+str(ref['network'])+' / ORef '+ref['oref'],
                    path='networks/network-'+str(ref['network'])+'.html') for ref in binding['refs'])
        refs.append(dict(label='이 단계의 수리 판단',path='repair-guides/'+record['key']+'.html#'+decision['common']))
        if circuit and key in ['permit','response','stop','recovery']:
            refs.append(dict(label=record['plc_id']+' 전기 회로·전달 경로',path='circuit-guides/'+record['plc_id']+'.html'))
        if linked and (ROOT/'signal-guides'/str(record['plc_id']+'.html')).exists():
            refs.append(dict(label=record['plc_id']+' 원시/처리 신호·복수 쓰기',path='signal-guides/'+record['plc_id']+'.html'))
        if install and key in ['response','recovery']:
            refs.append(dict(label=record['plc_id']+' 시공 케이블·접속함',path=install['guide']))
        if record['plc_id']=='BR01' and key in ['response','recovery']:
            refs.append(dict(label='가스·공기 원시값·환산·후속 제한·출력 근거',path='measurement-trace.html'))
        if record['plc_id']=='BR01' and key in ['response','stop','recovery']:
            refs.append(dict(label='온도·압력·산소 원시 입력·환산·다른 쓰기·수리 근거',path='sensor-measurement.html'))
        if record['plc_id'] in ['MV01','MV03','MV06'] and key in ['permit','response','stop','recovery']:
            refs.append(dict(label='엔코더·위치 환산·교정·방향 누적 감시',path='encoder-position.html#position-'+record['plc_id']))
        loop_id={'FN04':'FN04','MV01':'MV01','MV03':'MV03','MV06':'MV06','FN02':'VT02','BR01':'BR01'}.get(record['plc_id'])
        if loop_id and key in ['permit','response','stop','recovery']:
            refs.append(dict(label=loop_id+' 조절 루프 입력·설정·출력·다른 쓰기·수리 근거',path='regulation-manual.html#loop-'+loop_id))
            if loop_id=='BR01':refs.append(dict(label='가스·공기 비율 CONT_C 보정·곡선·가스 출력',path='regulation-manual.html#loop-STECHIO'))
        if record['plc_id']=='BR01' and key in ['permit','stop','recovery']:
            refs.append(dict(label='공정 계측·전용반 알람과 버너 정지 원인',path='process-stop-alarms.html'))
        if record['plc_id']=='BR01' and key in ['permit','response','stop','recovery'] or record['plc_id']=='MV03' and key in ['response','recovery']:
            refs.append(dict(label='BR01 외부 연동·정지·복구 및 MV03 요청 근거',path='burner-interface.html'))
        if linked and key in ['stop','recovery'] and (ROOT/'alarm-guides'/(record['plc_id']+'.html')).exists():
            refs.append(dict(label=record['plc_id']+' 알람 발생·리셋·재기동 근거',path='alarm-guides/'+record['plc_id']+'.html'))
        specific=[]
        if circuit and key=='response':
            specific=[dict(owner='회로 작업지의 확인 대기',work=work) for work in circuit['pending']]
        req=requirements[key]
        if not linked and key=='recovery':req=[requirements['recovery'][1],('전용 제어기·현장','해당 제어기의 알람·복구 기준·연동 접속이 확인된 근거를 사용합니다. GME 신호와의 관계는 자료 확인 전입니다.')]
        steps.append(dict(step_id=key,requirements=[dict(owner=o,work=w) for o,w in req]+specific,
            source_links=list({(r['label'],r['path']):r for r in refs}.values()),reviews=reviews_for(record,key)))
    return dict(scope='Evidence collection order; no new control conditions or automatic verification',
        sources=evidence_sources,preflight=preflight,steps=steps,
        circuit_equipment=circuit['equipment'] if circuit else None,
        circuit_distinction=circuit['distinction'] if circuit else None,
        circuit_pages=[dict(label='OEM FG'+str(fg)+' · PDF '+str(page),path=electrical['source']+'#page='+str(page))
            for fg,page in zip(circuit['sheets'],circuit['pages'])] if circuit else [],
        construction_boundary=install['boundary'] if install else None,
        construction_pages=[dict(label='추가 시공도면 PDF '+str(page),path=construction['source']+'#page='+str(page))
            for page in install['pages']] if install else [],
        field_verified=False)
profiles=[]
for r in repair['records']:
    profiles.append(dict(key=r['key'],name=r['name'],reference_plc_id=r['plc_id'],boundary=r['boundary'],
        identity_confirmed=False,field_verified=False,
        signals=[dict(id='signal-'+str(i+1),**b) for i,b in enumerate(r['bindings'])],
        steps=r['decisions'],manual='repair-guides/'+r['key']+'.html',
        blank_template='registers/repair-observation-'+r['key']+'.json',evidence_plan=evidence_plan(r)))
data=dict(schema_version=1,date='2026-10-08',scope='User-entered local repair observations; no automatic resolution or PLC writes',
    source=dict(path='registers/repair-decision.json',sha256=hashlib.sha256(source.read_bytes()).hexdigest()),
    profiles=profiles,counts=dict(profiles=len(profiles),signals=sum(len(r['signals']) for r in profiles),steps=sum(len(r['steps']) for r in profiles)),
    field_verified=False,repairs_completed=0,plc_changes=0,simulator_behavior_tests='not_rerun')
(ROOT/'registers/repair-record-forms.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(data['counts']))
