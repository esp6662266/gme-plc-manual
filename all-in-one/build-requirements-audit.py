# -*- coding: utf-8 -*-
"""Publish source-derived document coverage and an operator guide; no PLC execution."""
from pathlib import Path
from html import escape as esc
import csv, hashlib, json
ROOT=Path(__file__).resolve().parent
inputs={}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def source(path):
    p=ROOT/path
    assert p.is_file(),path
    inputs[path]=sha(p)
    return p
def load(path):return json.loads(source(path).read_text())
def link(path,label):
    if path.split('#')[0] in {'index.html','requirements-audit.html','operator-guide.html'}:assert (ROOT/path.split('#')[0]).is_file()
    else:source(path.split('#')[0])
    target=' target="_top"' if path.startswith('index.html#view=drawings&') else ''
    return '<a href="'+esc(path,quote=True)+'"'+target+'>'+esc(str(label))+'</a>'
def table(headers,rows):
    return '<div class="table-wrap"><table><thead><tr>'+''.join('<th>'+esc(h)+'</th>' for h in headers)+'</tr></thead><tbody>'+''.join(rows)+'</tbody></table></div>'
def tr(cells,anchor='',attrs=''):
    return '<tr'+(' id="'+esc(anchor,quote=True)+'"' if anchor else '')+attrs+'>'+''.join('<td>'+c+'</td>' for c in cells)+'</tr>'
specs=load('registers/control-spec.json')['specifications']
diag=load('registers/diagnostic-coverage.json')
sensor=load('registers/sensor-measurement.json')
reg=load('registers/regulation-manual.json')
enc=load('registers/encoder-position.json')
alarm=load('registers/alarm-recovery.json')
circuit=load('registers/electrical-trace.json')
hub=load('registers/evidence-review.json')
body_manual=load('registers/body-manual.json')
body_ids={p['id'] for p in body_manual['profiles']}
repair=load('registers/repair-decision.json')
identity=load('registers/unresolved-identity.json')
burner=load('registers/burner-interface.json')
freeze=load('registers/simulator-freeze.json')
with source('registers/priority-equipment.csv').open(encoding='utf-8-sig',newline='') as f:priority=list(csv.DictReader(f))
with source('registers/simulation-tests.csv').open(encoding='utf-8-sig',newline='') as f:tests=list(csv.DictReader(f))
with source('registers/verification.csv').open(encoding='utf-8-sig',newline='') as f:checks=list(csv.DictReader(f))
assert len(specs)==248 and len(priority)==23 and len(tests)==577 and len(checks)==1060
assert all(r['상태']=='설계·미실행' for r in tests)
assert all(sha(ROOT/f)==h for f,h in freeze['files'].items())
pmap={p['plc_id']:p['key'] for p in priority if p['plc_id']}
detailed=set(diag['detailed_devices'])
sensorids={c['id'] for c in sensor['channels']}
encids={c['id'] for c in enc['channels']}
alarmids={p['id'] for p in alarm['profiles']}
circuitids={d['id'] for d in circuit['devices']}
labels={'symptom':'대표 증상별 절차','specialist':'전문 분야 상세 근거','baseline':'기본 자료·상세 보강 대기'}
rows=[]
for s in specs:
    ident=s['id'];special=[]
    if ident in sensorids:special.append(dict(kind='계측',path='sensor-measurement.html#sensor-'+ident))
    if ident in encids:special.append(dict(kind='위치·교정',path='encoder-position.html#position-'+ident))
    for loop in reg['loops']:
        if ident in loop['equipment']:special.append(dict(kind='조절 '+loop['id'],path='regulation-manual.html#loop-'+loop['id']))
    if ident in alarmids:special.append(dict(kind='알람·복구',path='alarm-guides/'+ident+'.html'))
    if ident in circuitids:special.append(dict(kind='전기 회로',path='circuit-guides/'+ident+'.html'))
    if ident in body_ids:special.append(dict(kind='본체·증상·공정 경계',path='body-manual.html#body-'+ident))
    level='symptom' if ident in detailed else 'specialist' if special else 'baseline'
    if ident in ['CC01','AB01','HE01']:next_task='본체 자료 확인7항목의 설치/기계/제작사 근거 수집; MV04 관련1항목은 사용자 제공 철거에 따라 상세 조사 제외'
    elif level=='symptom':next_task='현재 프로그램·실물 대응과 관찰값을 수집하여 원인 배제·복구 확인을 기록'
    elif s['kind'] in ['passive','client']:next_task='본체 또는 외부 제어 주체·접속 경계·제작사 자료 확인; 직접 PLC 출력을 임의 배정하지 않음'
    elif s['kind'] in ['sensor','software']:next_task='미보강 입력/변환/표시 또는 공통 기능의 원본 조건·소비 위치·다른 쓰기를 상세 추적'
    else:next_task='요청→허가→출력→응답→감시→정지/리셋의 직접 원본 경로와 대표 고장 절차 보강'
    if any(n['id']==ident and n['status']=='manual_deferred_user_reported' for n in body_manual['equipment_status_notes']):next_task='EV01~EV90 매뉴얼 작성 제외 · 사용자 제공(2026-10-09). 추가 요청 전 상세 보강 중단; 기존 원본/문서 보존'
    if ident=='PV04':next_task='사용 계획 없음 · 사용자 제공(2026-10-09). 현재 상세 조사 제외; 과거 도면·백업 보존, 현재 사용 상태 부모 검증 미실시'
    if ident=='SC12':next_task='현장 없음 · 사용자 제공(2026-10-09). 현재 상세 조사 제외; 과거 도면·백업 보존, 부모 현장 검증 미실시'
    if ident=='MV04':next_task='철거됨 · 사용자 제공(2026-10-09). 현재 상세 조사 제외; 과거 도면·백업·기존 불일치 보존, 현장 검증 미실시'
    row=dict(id=ident,name=s['name'],group=s['group'],kind=s['kind'],parent=s['parent'],priority=pmap.get(ident,''),detail_level=level,symptom_detail=ident in detailed,specialist=special,inputs=len(s['inputs']),outputs=len(s['outputs']),hmi=len(s['hmi']),networks=len(s['networks']),direct_paths=len(s['direct_rules']),pending=len(s['pending']),next_task=next_task,field_verified=False,tia_verified=False)
    row['lifecycle_note']=next((n for n in body_manual['equipment_status_notes'] if n['id']==ident),None)
    row['base_documents']=[dict(path=folder+'/'+ident+'.html',label=label) for folder,label in [('devices','기본 매뉴얼'),('control-specs','제어 명세'),('procedures','수리 절차')]]
    for ref in row['base_documents']+special:source(ref['path'].split('#')[0])
    rows.append(row)
byid={r['id']:r for r in rows}
for p in priority:
    assert not p['plc_id'] or p['plc_id'] in byid
    p['identity_verified']=False
    p['lifecycle_note']=next((n for n in body_manual['equipment_status_notes'] if n['id']==p['key']),None)
    p['detail_level']=byid[p['plc_id']]['detail_level'] if p['plc_id'] else 'identity_unresolved'
    p['next_task']=byid[p['plc_id']]['next_task'] if p['plc_id'] else '명판·현장 위치·설비 카드 ID·제어반·전용 제어기·도면 개정을 확보한 후 제어 주체 식별'
    if p['lifecycle_note']:p['next_task']='다른 공정 · 사용자 제공. 관련 조사·분석·보강 중단; 기존 배치도 자료 보존'
    elif p['key'] in ['P03','P04','P14']:p['next_task']='식별 작업지에서 후보/배제 근거와 필요한 명판·제어반·연동 자료 대조'
# Reclassify preserved evidence; no new PLC condition or pending closure.
identity_bykey={r['key']:r for r in identity['profiles']}
alarm_byid={r['id']:r for r in alarm['profiles']}
spec_byid={r['id']:r for r in specs}
priority_open_work=[]
for p in priority:
    if p['lifecycle_note']:continue
    key,ident=p['key'],p['plc_id']
    existing=[dict(path='repair-guides/'+key+'.html',label='수리 판단'),dict(path='priority-guides/'+key+'.html',label='설비 대응')]
    references=[dict(path='registers/repair-decision.json',record=key)]
    collected='현재 사용 백업의 버전·날짜, 현행 접속도·단자표, 설비/구동기/제어반 명판과 위치 사진'
    field='동일 시각의 요청·허가·최종 출력·원시/처리 응답·최초 알람·리셋 전후 관찰과 실제 복구 결과. 관찰값은 확보 전 비워 둠'
    boundary=p['note'] or '태그명 일치는 실제 설치·현재 CPU 대응의 확인을 뜻하지 않음'
    pending=list(spec_byid[ident]['pending']) if ident else []
    body_checks=[]
    review_items=[r for r in hub['items'] if key in r['priority_keys'] and not r['resolved'] and not any(ex in r['title']+' '+r['source_id'] for ex in ['MV04','SC12','PV04'])]
    review_items=[{k:r[k] for k in ['id','source_id','title','next_check','source_status','priority_keys','resolved']} for r in review_items]
    notes=[]
    document='기존 근거와 미확정 항목을 정리. 새 자료가 도착한 항목만 원본 대조 후 수리 절차에 반영; 완료 분석은 반복하지 않음'
    lane='현행 자료·관찰 보강'
    if ident:
        existing+=byid[ident]['base_documents']+byid[ident]['specialist']
        references.append(dict(path='registers/control-spec.json',record=ident))
    if ident in alarm_byid:
        notes.append(alarm_byid[ident]['note'])
        references.append(dict(path='registers/alarm-recovery.json',record=ident))
    if not ident:
        lane='식별 자료 우선'
        u=identity_bykey[key]
        boundary=u['excluded'];collected=u['needed'];field=u['symptom']
        document='기존 식별 작업지는 완료·보존. 명판/제어 주체/현행 연결 근거 확보 후에만 I/O·알람·수리 조건 연결; 후보 재작성·태그 임의 배정 금지'
        notes.append(u['confirmed'])
        existing.append(dict(path='unresolved-identity.html#identity-'+key,label='식별 작업지'))
        references.append(dict(path='registers/unresolved-identity.json',record=key))
        completion='명판·위치·제어반·현행 도면으로 동일성/제어 주체를 대조하고 확인된 I/O·연동 근거를 연결. 확인 전 PLC 태그 공란 유지'
    elif ident in body_ids:
        lane='본체·계측·제작사 자료'
        body_checks=[c for c in body_manual['checks'] if ident in c['equipment'] and not c['excluded_from_current_analysis']]
        collected='최신 본체 기계도·부품명세·제작사 점검/교체/복구 기준, 실제 계측 취출부·소자/변환기 양단·표찰 자료'
        field='본체와 주변 모터·버너·계측 경계, 해당 본체 확인 항목의 현재 설치/표시와 관찰 결과 기록'
        references.append(dict(path='registers/body-manual.json',record=ident))
        completion='해당 본체 확인 항목에 설치/제작사 근거와 관찰을 연결하고 미확정 사항 명시. 주변 태그를 본체 직접 출력으로 배정하지 않음'
        if ident=='AB01':document='완료한 AB01 알람·근거표 분석 보존. 새 자료 또는 확인된 오류가 있을 때만 영향받는 항목 재검토'
    else:
        completion='현재 버전·실물 대응과 요청→허가→출력→전기 전달→응답 관찰, 원인 해소/래치 해제/재기동/실제 복구를 구분해 기록. 단순 리셋을 수리 완료로 판정하지 않음'
    if ident=='BR01':
        lane='전용 버너 자료·현행 연동'
        collected+='; 전용010-390 회로·버너/연소 제어기 모델·제작사 승인 운전/보호/복구 자료'
        notes.extend(o['title']+' · '+o['status'] for o in burner['observations'])
        existing.append(dict(path='burner-interface.html',label='버너 외부 연동'))
        references.append(dict(path='registers/burner-interface.json',record='BR01'))
        boundary+='; 외부 연동 근거로 전용 버너 내부 안전 순서를 추정하지 않음'
    if ident in encids:
        collected+='; 현재 TM/엔코더 채널·구동기 모델·리미트 명칭/극성·기계 기준·교정/유지 자료'
        references.append(dict(path='registers/encoder-position.json',record=ident))
    if review_items:
        references.append(dict(path='registers/evidence-review.json',record=key))
    existing=list({r['path']:r for r in existing}.values())
    for ref in existing:source(ref['path'].split('#')[0])
    priority_open_work.append(dict(key=key,name=p['name'],plc_id=ident,match=p['match'],lane=lane,boundary=boundary,existing_documents=existing,evidence_references=references,existing_pending=pending,existing_notes=notes,body_checks=body_checks,existing_review=review_items,document_work=document,additional_materials=collected,field_work=field,completion_criterion=completion,identity_verified=False,field_verified=False,tia_verified=False,repairs_completed=0))
assert len(priority_open_work)==21 and {r['key'] for r in priority_open_work}=={'P'+str(i).zfill(2) for i in range(1,22)}
counts=dict(current_priority=21,other_process_excluded=2,retired_equipment_excluded=1,absent_equipment_excluded=1,not_planned_equipment_excluded=1,manual_deferred_equipment_excluded=sum(n['status']=='manual_deferred_user_reported' for n in body_manual['equipment_status_notes']),eligible_history_equipment=sum(not r['lifecycle_note'] for r in rows),current_equipment_detail_scope=21,body_source_devices=len(body_ids),body_symptom_cases=body_manual['counts']['symptom_cases'],equipment=len(rows),priority=len(priority),priority_referenced_equipment=len(pmap),priority_unknown=sum(not p['plc_id'] for p in priority),base_manuals=len(rows),base_specs=len(rows),base_procedures=len(rows),representative_symptom_devices=sum(r['symptom_detail'] for r in rows),representative_symptom_cases=diag['detailed_symptom_cases'],specialist_only_devices=sum(r['detail_level']=='specialist' for r in rows),baseline_only_devices=sum(r['detail_level']=='baseline' for r in rows),with_io=sum(bool(r['inputs'] or r['outputs']) for r in rows),with_hmi=sum(bool(r['hmi']) for r in rows),with_direct_paths=sum(bool(r['direct_paths']) for r in rows),tests_designed=len(tests),tests_executed=0,pending_checks=len(checks),source_conflicts=hub['counts']['source'],review_items=len(hub['items']),field_verified=0,tia_verified=0)
requirements=[
 ('R01','한곳의 HTML에서 사용','구현·통합 검증 대상','index.html의 설비 선택과 문서 탐색. 최신 브라우저 검증과 ZIP은 별도 단계의 결과','ALL-IN-ONE.md'),
 ('R02','전체 248개 자료','기본 자료 연결','매뉴얼·제어 명세·수리 절차 각248개. 자료 깊이는 아래 개별 목록으로 구분','manual-catalog.html'),
 ('R03','디코팅 우선23개','참조 대응·실물 확인 대기','태그 일치14·역할 후보4·미확정5. 참조 PLC18개와 실물23개를 구분','repair-decision.html'),
 ('R04','전문적인 상세 수리 매뉴얼','보강 중','대표 증상15설비/34사례, 본체3개/12사례 및 계측·조절·위치·회로 자료. 전체248개 상세 완성은 확인 전','repair-decision.html'),
 ('R05','입출력·조건·순서·고장·근거','기본 명세·정적 분석','직접 정적 경로148항목. 본체·외부 장치에는 직접 경로 부재가 곧 누락/오류는 아님','control-spec.html'),
 ('R06','PLC 호출·신호 구조','정적 근거 연결','원본426 LAD와 호출·읽기/쓰기. 미해석 참조·현재 OB 순서·TIA 컴파일은 확인 전','signal-trace.html'),
 ('R07','P&ID·OEM·추가 전기도면','원본 보존·선택 상세 분석','세 원본을 보존. 추가64페이지의 승인·준공/실제 배선 확인 전; 가림 행 제외','construction-guide.html'),
 ('R08','HMI·레시피·설정값','원본 설정 분석','782태그·17화면 메타데이터·8운전 대입. 현재 DB 오프셋·이벤트·통신·Retain 확인 전','recipe-settings.html'),
 ('R09','불일치·미확정 확인','확인 대기','원본18건 해소 미확정·원래 확인1060건 보존·추가 검토 포함64건','evidence-review.html'),
 ('R10','프로그램 개선','후보 검토','6개 후보의 영향·대안·근거. 실제 PLC 개선 적용0건','improvement-review.html'),
 ('R11','수리·관찰 기록','양식·로컬 저장','23개 양식과 메모; 브라우저/주소별 저장. JSON 다운로드는 별도 보관하며 가져오기·공유 동기화 미구현','ALL-IN-ONE.md'),
 ('R12','577개 시험','설계·미실행','기존 가상 부분 시험19개는 과거 기록. 전체577개 실행·TIA·실물 검증과 구분','registers/simulation-tests.csv'),
 ('R13','시뮬레이터','사용자 지시로 중지','별도 작성 요청 전까지 개발·수정·확장·행동 시험 중지. 기존5개 파일 해시 보존','ACTIVE-WORK.md'),
 ('R14','최종 제공·운영 반영','작업 단위 패키지 갱신','링크·원본·브라우저 검증 후 ZIP. SEJIN 운영 배포/현장 PLC 변경은 별도 요청 범위','PACKAGE-NOTES.md')]
counts['eligible_history_baseline_devices']=sum(r['detail_level']=='baseline' and not r['lifecycle_note'] for r in rows)
requirement_rows=[]
for key,title,status,note,path in requirements:
    requirement_rows.append(dict(id=key,title=title,status=status,detail=note,path=path))
    source(path)
styles='''body{font:16px/1.7 system-ui,sans-serif;color:#183247;background:#f2f6f9;margin:0;padding:28px}main{max-width:1400px;margin:auto}h1{font-size:28px}section{background:white;border:1px solid #dbe5ed;border-radius:12px;padding:22px;margin:18px 0}.notice{padding:16px;background:#fff6dc;border-left:5px solid #e4b33c}.stats{display:flex;flex-wrap:wrap;gap:12px}.stats div{background:#eaf2f7;padding:12px;border-radius:8px}.table-wrap{overflow:auto}table{border-collapse:collapse;width:100%;font-size:14px}th,td{padding:12px;vertical-align:top;text-align:left;border-bottom:1px solid #dbe5ed}th{background:#edf3f8}a{color:#0a658b}tr:target{outline:3px solid #d5a900;background:#fff8d9}nav a{display:inline-block;margin:6px 14px 6px 0}label{display:inline-block;margin:6px 12px 6px 0}input,select{font:inherit;padding:7px;max-width:100%}[hidden]{display:none!important}.muted{color:#576a7a}@media(max-width:720px){body{padding:12px}section{padding:12px}}@media print{body{padding:0;background:white}.filters{display:none}section{border:0}tr{break-inside:avoid}tr[hidden]{display:table-row!important}}'''
styles+='''#priority-open-work details{border:1px solid #dbe5ed;border-radius:8px;margin:12px 0;padding:12px}#priority-open-work summary{cursor:pointer;padding:8px;background:#edf3f8;border-radius:6px}#priority-open-work li{margin:8px 0}#priority-open-work td:first-child{min-width:80px}#priority-open-work a{overflow-wrap:anywhere}'''
stats=''.join('<div><b>'+str(v)+'</b><br>'+esc(k)+'</div>' for k,v in [('현재 집중 대상',21),('보존된 전체 참고 자료',248),('대표 증상 상세',counts['representative_symptom_devices']),('전문 자료만 연결',counts['specialist_only_devices']),('기본 자료·보강 대기',counts['baseline_only_devices']),('우선 실물 미확정',23)])
reqhtml=table(['요구사항','현재 상태','판단 근거'],[tr([esc(r['id']+' '+r['title']),esc(r['status']),esc(r['detail'])+'<br>'+link(r['path'],'근거 보기')],r['id']) for r in requirement_rows])
prihtml=table(['우선 설비','참조 PLC·대응','자료 깊이·다음 확인','작업지'],[tr([esc(p['key']+' '+p['name']),esc((p['plc_id'] or '미확정')+' / '+p['match'])+'<br>실물 동일성 확인 전',esc(labels.get(p['detail_level'],'설비 식별 대기'))+'<br>'+esc(p['next_task']),link('repair-guides/'+p['key']+'.html','수리 판단')+' · '+link('common-guides/'+p['key']+'.html','공통 제어')], 'priority-'+p['key']) for p in priority])
eqhtml=table(['항목·상하위','기본·상세 자료','백업 참조 수','다음 작업'],[tr([esc(r['id']+' · '+r['name'])+'<br>'+esc(r['group']+' / '+r['kind'])+'<br>'+esc('상위 '+(r['parent'] or '없음')),esc(labels[r['detail_level']])+'<br>'+' · '.join(link(d['path'],d.get('label',d.get('kind',''))) for d in r['base_documents'])+'<br>'+' · '.join(link(d['path'],d['kind']) for d in r['specialist']),esc(f"I/O {r['inputs']}/{r['outputs']} · HMI {r['hmi']} · 관련망 {r['networks']} · 직접경로 {r['direct_paths']}")+'<br>현재 값·실행 확인 전',esc(r['next_task'])], 'equipment-'+r['id'], ' data-detail="'+r['detail_level']+'" data-priority="'+('yes' if r['priority'] else 'no')+'" data-search="'+esc(' '.join(str(r[k]) for k in ['id','name','group','kind','parent']),quote=True)+'"') for r in rows])
script='''const rows=[...document.querySelectorAll('#equipment tbody tr')];const search=document.querySelector('#search'),depth=document.querySelector('#depth'),scope=document.querySelector('#scope');function apply(){let n=0;for(const r of rows){r.hidden=!(r.dataset.search.toLowerCase().includes(search.value.trim().toLowerCase())&&(depth.value==='all'||r.dataset.detail===depth.value)&&(scope.value==='all'||r.dataset.priority==='yes'));if(!r.hidden)n++;}document.querySelector('#visible-count').textContent=n+' / '+rows.length+' 항목';}function anchor(){const r=document.getElementById(decodeURIComponent(location.hash.slice(1)));if(r&&rows.includes(r)){search.value='';depth.value='all';scope.value='all';apply();r.scrollIntoView();}}for(const el of [search,depth,scope])el.addEventListener('input',apply);window.addEventListener('hashchange',anchor);apply();anchor();'''
openhtml=''
for r in priority_open_work:
    facts='<ul>'+''.join('<li>'+esc(t)+'</li>' for t in r['existing_notes']+r['existing_pending'])+'</ul>' if r['existing_notes'] or r['existing_pending'] else ''
    checks=''.join('<li><b>'+esc(c['id']+' · '+c['title'])+'</b>: '+esc(c['next_check'])+'</li>' for c in r['body_checks'])
    reviews=''.join('<li>'+link('evidence-review.html#review-'+c['id'].replace(':','-'),c['source_id']+' · '+c['title'])+': '+esc(c['next_check'])+'</li>' for c in r['existing_review'])
    refs=' · '.join(link(d['path'],d.get('label',d.get('kind','자료'))) for d in r['existing_documents'])
    openhtml+='<details id="open-'+r['key']+'"><summary><b>'+esc(r['key']+' · '+r['name'])+'</b> — '+esc(r['lane'])+'</summary><p>'+esc(r['boundary'])+'</p><p><b>기존 자료</b> '+refs+'</p>'+table(['미완료 종류','다음 작업'],[tr([esc(label),esc(r[field])]) for label,field in [('문서 보강','document_work'),('추가 자료','additional_materials'),('현장 확인','field_work'),('완료 기준','completion_criterion')]])+('<p><b>기존 원본 근거·미확정 사항</b></p>'+facts if facts else '')+('<p><b>현재 본체 확인 항목</b></p><ul>'+checks+'</ul>' if checks else '')+'<p class="muted">문서 재분류이며 현장 확인·TIA 검증·수리 완료를 뜻하지 않습니다.</p></details>'
    if reviews:openhtml=openhtml[:-10]+'<p><b>기존 근거 검토의 관련 항목</b> · 공유 참조를 포함하며 직접 소유·고장 원인 확정을 뜻하지 않습니다. 새 확인 건수로 합산하지 않습니다.</p><ul>'+reviews+'</ul></details>'
openhtml='<section id="priority-open-work"><h2>현재21개 · 미완료 항목과 완료 기준</h2><p>완료 분석은 보존하고 남은 일을 문서 보강·추가 자료·현장 확인으로 구분했습니다. 식별3개, 본체3개, 전용 버너1개, 구동부14개입니다. 모두 현장 확인 전입니다. 항목을 펼쳐 기존 근거와 다음 증거를 확인합니다.</p><p>BC01·FN04 현행 자료/관찰을 먼저 보강하고 미확정3개 식별 자료를 병행 수집합니다. 작업 순서 제안이며 새 현장 관찰이나 PLC 변경 결과가 아닙니다. GSS·85톤로·MV04·SC12·PV04·EV01~90 상세 작업과 전체248개 확대는 포함하지 않습니다.</p>'+openhtml+'</section>'
# Output links are generated alongside this page, so they are not immutable input hashes.
audit_html='<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>작성 상태·누락·다음 작업 | GME</title><style>'+styles+'</style><main><h1>작성 상태·누락·다음 작업</h1><p>기본 자료·상세 분석·실제 운전 확인을 구분합니다. 전체 완료율은 계산하지 않습니다. 현재는 우선23개 완성 단계입니다. GSS·85톤로를 제외한21개에 집중하고 전체248개는 참고 목록으로 보존합니다. 전체 확장은 우선 대상 완료 후 필요 항목을 추가하는 단계입니다.</p><div class="notice">현장·현재 TIA 확인0건. 시험577개는 설계·미실행. 시뮬레이터 개발·수정·행동 시험은 사용자 재개 요청 전까지 중지합니다.</div><nav><a href="#requirements">요구사항</a><a href="#priority">우선23개</a><a href="#equipment">전체248개</a><a href="operator-guide.html">사용 안내</a><a href="work-progress.html">진행 순서</a></nav><div class="stats">'+stats+'</div><section id="requirements"><h2>요구사항별 현재 상태</h2>'+reqhtml+'</section><section id="priority"><h2>디코팅 우선23개</h2><p>참조 PLC18개·대응 미확정5개 중 현재 식별 대상3개·다른 공정 제외2개. 태그명 일치와 역할 후보 모두 실물 동일성은 확인 전입니다. 본체와 구동부를 합치지 않습니다.</p>'+prihtml+'</section><section id="equipment"><h2>전체248개 · 기본 자료와 상세 보강 범위</h2><p>대표 증상별 절차15개 설비/34사례와 별도 본체3개/12사례. 전문 자료는 명시적으로 참조하는 항목만 연결합니다. 관련 설비는 루프 소유 관계를 증명하지 않습니다. 기본 절차가 있어도 상세 완성으로 간주하지 않습니다. 공통 HMI·레시피·시스템 분석은 이 설비별 분류와 별도로 함께 제공합니다.</p><div class="filters"><label>검색 <input id="search" type="search" placeholder="설비·계통·상위 항목"></label><label for="depth">자료 깊이</label><select id="depth"><option value="all">전체</option><option value="symptom">대표 증상별 절차</option><option value="specialist">전문 자료만 연결</option><option value="baseline">기본 자료·보강 대기</option></select> <label for="scope">범위</label><select id="scope"><option value="all">전체248개</option><option value="priority">우선 PLC 참조18개</option></select> <b id="visible-count"></b></div>'+eqhtml+'</section><section id="limits"><h2>집계와 검증의 한계</h2><p>페이지 존재·명세 참조 수·상세 JSON의 명시적 관계를 대조한 정적 목록입니다. 공유 참조·원본 XML·문서 링크 검사는 현재 CPU 실행·실물 수리 완료를 입증하지 않습니다. 직접 제어 경로가 없는 본체·외부 제어 설비·센서는 역할별 근거로 확인합니다.</p><p>원본 불일치18건·기존 확인1060건·검토64건의 완료 상태를 바꾸지 않습니다. ZIP과 브라우저 검증 결과는 별도 단계에서 최신 파일을 확인합니다.</p><a href="registers/requirements-audit.json">집계 JSON</a> · <a href="registers/requirements-audit.csv">설비별 CSV</a></section></main><script>'+script+'</script></html>'
audit_html=audit_html.replace('<a href="#priority">우선23개</a>','<a href="#priority-open-work">현재21개 미완료</a><a href="#priority">보존된 우선23개</a>').replace('<section id="priority">',openhtml+'<section id="priority">')
(ROOT/'requirements-audit.html').write_text(audit_html,encoding='utf-8')
# Operator links use preserved documents or the already supported record/review application routes.
guide='<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>사용 안내 | GME</title><style>'+styles+'</style><main><h1>올인원 사용 안내</h1><p>처음 열면 디코팅 배치도와 설비카드가 나옵니다. 설비를 눌러 선택 카드의 증상별 수리·알람·매뉴얼·I/O·래더·도면으로 이동합니다. 카드 목록·검색·확대·전체 보기를 사용할 수 있고, 작은 화면에서는 선택 카드로 이동한 뒤 돌아가기 버튼으로 배치도를 다시 봅니다. 자료 화면의 위쪽 탭과 왼쪽 설비 목록도 유지됩니다. 문서 링크는 작업실 안에서 열립니다.</p><nav><a href="requirements-audit.html">작성 상태·다음 작업</a><a href="work-progress.html">진행 순서</a><a href="ALL-IN-ONE.md">설치·저장 상세 안내</a></nav>'
guide_sections=[
 ('drawings','설비별 도면을 중심으로 확인','설비카드의 설비별 도면 작업실을 엽니다. OEM 전기·P&ID·시공/케이블·HMI 썸네일을 선택하고 중앙 그림을 확대합니다. 도면 넓게 보기는 목록과 근거를 접으며 근거 함께 보기로 복원합니다. 원본 페이지는 FG와 실제 PDF 페이지를 구분합니다. 관련 단자·PLC 원본·케이블·알람·수리와 미완료 기준을 연결하며 미확정 설비에 전용 회로를 임의 배정하지 않습니다. FN04 공유 인버터/C05와 BC01 SS01 심선 표기 차이는 현행 자료 확인 전입니다.',[('index.html#view=drawings&equipment=P01&scope=priority','BC01 도면 작업실'),('index.html#view=drawings&equipment=P02&scope=priority','FN04 도면 작업실')]),
 ('start','1. 설비를 찾고 대응부터 확인','우선23개 또는 전체248개 범위를 선택합니다. 태그명 일치·후보·미확정을 읽고, 실물 명판·제어반·도면 개정을 대조합니다. 대응 미확정 설비에 PLC 주소를 임의 배정하지 않습니다.',[('priority-guides/P01.html','BC01 대응 예시'),('priority-guides/P03.html','미확정 설비 예시')]),
 ('repair','2. 증상과 고장 근거를 비교','진단·수리 탭에서 증상을 고르고 요청·허가·출력·전기 전달·응답·알람을 순서대로 비교합니다. 원본 래더를 열어 반전 접점·분기·타이머를 확인합니다. 관찰하지 않은 값은 비워 둡니다.',[('procedures/BC01.html','BC01 증상별 절차'),('circuit-guides/BC01.html','BC01 회로'),('alarm-guides/BC01.html','BC01 알람·복구')]),
 ('structure','3. 프로그램과 설정값 출처를 추적','호출·신호 구조에서 읽기/쓰기 위치와 다른 블록의 쓰기를 함께 봅니다. HMI 표시·편집·저장본·운전 적용값을 구분합니다. 백업 색인의 나열 순서를 현재 CPU 실행 순서로 판단하지 않습니다.',[('signal-trace.html','신호 전달'),('hmi-transfer.html','HMI 주소·전달'),('recipe-settings.html','레시피·설정'),('encoder-position.html','위치·방향 누적')]),
 ('records','4. 확인한 내용만 기록하고 다운로드','수리 기록에서 관찰값·원인 배제·조치·후속 확인을 작성하고 저장 후 다시 열어 확인합니다. 개선·작업 메모는 별도 저장입니다. 주소·포트·브라우저별 로컬 저장이며 다른 직원과 자동 공유되지 않습니다. 기록/메모 JSON 다운로드를 별도로 보관합니다. 현재 가져오기·병합·서버 동기화는 없습니다. 프로그램 ZIP에 브라우저 기록이 자동 포함되지 않습니다.',[('index.html#view=repair-record&equipment=P01&scope=priority','BC01 수리 기록'),('ALL-IN-ONE.md','저장·충돌·설치 안내')]),
 ('pending','5. 미확정 근거와 개선 후보를 남기기','확인 대장·근거 검토에서 원본과 현재 값의 차이, 확인에 필요한 자료를 기록합니다. 18개 불일치의 해소나 복구 완료는 실제 근거가 있을 때 판정합니다. 개선 후보는 영향과 대안을 검토한 자료이며 실제 PLC에 적용하지 않았습니다.',[('index.html#view=review&equipment=P01&scope=priority','BC01 근거 검토'),('improvement-review.html','개선 후보6개'),('evidence-review.html','검토 목록')]),
 ('limits','6. 현재 검증 범위를 읽기','정적 문서 검증·브라우저 기능 확인·TIA 실행·현장 복구는 다른 결과입니다. 전체577개 시험은 설계·미실행이고 과거 가상 부분 시험19개와 구분합니다. 시뮬레이터는 사용자 재개 요청 전까지 작성·수정·행동 시험을 진행하지 않습니다.',[('requirements-audit.html#requirements','요구사항별 상태'),('ACTIVE-WORK.md','현재 작업 범위')])]
for anchor,title,body,refs in guide_sections:
    guide+='<section id="'+anchor+'"><h2>'+title+'</h2><p>'+body+'</p><p>'+' · '.join(link(p,t) for p,t in refs)+'</p></section>'
guide+='<section id="install"><h2>다른 컴퓨터에서 열기</h2><p>최신 ZIP을 전체 폴더로 풀고 index.html에서 시작합니다. sources·assets·문서 폴더를 함께 유지합니다. PDF와 문서 탐색은 폴더에서 실행한 로컬 HTTP 서버 사용을 권장합니다. 서버 주소가 바뀌면 기존 브라우저 기록이 자동 이동하지 않습니다. 시작 명령과 현재 Mac 경로는 설치 안내에 있습니다.</p>'+link('ALL-IN-ONE.md','설치 안내')+'</section></main></html>'
(ROOT/'operator-guide.html').write_text(guide,encoding='utf-8')
for path in ['PROJECT-PURPOSE.md','build-requirements-audit.py']:source(path)
record=dict(date='2026-10-09',scope='static document coverage; not PLC execution',overall_completion_proven=False,counts=counts,requirements=requirement_rows,priority=priority,priority_open_work=priority_open_work,equipment=rows,inputs=inputs,simulator_development='stopped_by_user',simulator_behavior_tests='not_rerun',field_verified=False,tia_verified=False)
(ROOT/'registers/requirements-audit.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
with (ROOT/'registers/requirements-audit.csv').open('w',encoding='utf-8-sig',newline='') as f:
    keys=['id','name','group','kind','parent','priority','detail_level','symptom_detail','inputs','outputs','hmi','networks','direct_paths','pending','next_task','field_verified','tia_verified']
    w=csv.DictWriter(f,fieldnames=keys,extrasaction='ignore');w.writeheader();w.writerows(rows)
print(json.dumps(dict(status='built',counts=counts,source_hashes=len(inputs)),ensure_ascii=False))
