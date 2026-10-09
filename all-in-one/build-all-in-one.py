"""Build the single-entry web workspace from preserved manual registers.

The application uses a small, embedded data bundle and existing documents.
No PLC execution or SEJIN writes are performed by this build or the UI.
"""
from pathlib import Path
import csv
import json
import hashlib

ROOT = Path(__file__).resolve().parent

def readcsv(name):
    with (ROOT / 'registers' / name).open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))

def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

# Names and positions observed in the user's named canvas on 2026-10-07.
# A tag-name match is not a field-verified identity, and a role match is a candidate.
observed = [
    ('BC-01(벨트)', 'BC01', 'tag', '첫 상세 사례', 990, 1220, ''),
    ('FN-04 팬 모터', 'FN04', 'tag', '첫 상세 사례', 2250, 470, '팬 본체와 모터의 관리 관계 확인'),
    ('웨잉호퍼1', '', 'unknown', '원료·제품 이송', 470, 1235, '호퍼 번호·계량 제어 주체 확인. 호퍼2 태그를 대신 연결하지 않음'),
    ('웨잉호퍼배출컨베이어', '', 'unknown', '원료·제품 이송', 730, 1230, '실제 컨베이어 태그·제어반·앞뒤 운전 신호 확인'),
    ('PV-01', 'PV01', 'tag', '원료·제품 이송', 1250, 1235, ''),
    ('킬른', 'RD01', 'candidate', '원료·제품 이송', 1530, 1235, '킬른 본체와 RD01 구동 설비의 관계를 확인. 동일 설비로 병합하지 않음'),
    ('PV-02', 'PV02', 'tag', '원료·제품 이송', 1830, 1230, ''),
    ('MC04', 'MC04', 'tag', '원료·제품 이송', 2090, 1220, ''),
    ('VS01', 'VS01', 'tag', '원료·제품 이송', 2350, 1220, ''),
    ('CC챔버', 'CC01', 'candidate', '원료·제품 이송', 1530, 1530, '투입·배출 챔버 구분과 실물 위치 확인'),
    ('BR01', 'BR01', 'tag', '열처리·순환', 750, 800, '버너 전용 도면과 연소 제어 경계 확인'),
    ('재연소로', 'AB01', 'candidate', '열처리·순환', 1050, 790, '공정 역할을 기준으로 한 후보. 본체·버너·챔버 관계 확인'),
    ('열교환기', 'HE01', 'candidate', '열처리·순환', 1430, 800, '명판·P&ID·주변 연결로 동일성 확인'),
    ('2사이클론', '', 'unknown', '열처리·순환', 1970, 790, '숫자 2가 장치 번호인지 수량인지 확인. CY02로 자동 연결하지 않음'),
    ('FN-01 팬 모터', 'FN01', 'tag', '열처리·순환', 2250, 800, '팬 본체와 모터의 관리 관계 확인'),
    ('FN-02 팬 모터', 'FN02', 'tag', '열처리·순환', 1430, 485, '팬 본체와 모터의 관리 관계 확인'),
    ('FN-03 팬 모터', 'FN03', 'tag', '열처리·순환', 470, 795, '팬 본체와 모터의 관리 관계 확인'),
    ('FN-06 팬 모터', 'FN06', 'tag', '열처리·순환', 1110, 1525, '팬 본체와 모터의 관리 관계 확인'),
    ('MV-01', 'MV01', 'tag', '열처리·순환', 1710, 790, ''),
    ('MV-03 댐퍼 모터', 'MV03', 'tag', '열처리·순환', 1710, 480, '댐퍼 본체와 구동모터 관계 확인'),
    ('MV-06 댐퍼 모터', 'MV06', 'tag', '열처리·순환', 1970, 475, '댐퍼 본체와 구동모터 관계 확인'),
    ('GSS', '', 'unknown', '연결 공정', 2610, 1525, '설비 카드·제어 주체·디코팅 연동 신호 확인'),
    ('85톤로(압연)', '', 'unknown', '연결 공정', 2610, 1220, 'GME 제어 범위와 상위 공정의 허가·정지 신호 확인'),
]
priority = []
for i, (name, plc_id, match, phase, x, y, note) in enumerate(observed, 1):
    priority.append(dict(key=f'P{i:02}', name=name, plc_id=plc_id, match=match,
                         phase=phase, x=x, y=y, note=note,
                         identity_verified=False,
                         sejin_id='1766455617361' if name == '킬른' else ''))

all_specs = json.loads((ROOT / 'registers/control-spec.json').read_text())['specifications']
equipment_rows = {r['ID']: r for r in readcsv('equipment.csv')}
trace_path = ROOT / 'registers/electrical-trace.json'
electrical_trace = json.loads(trace_path.read_text()) if trace_path.exists() else {}
circuit_sheets = {d['id']:d['sheets'] for d in electrical_trace.get('devices',[])}
signal_path=ROOT/'registers/signal-trace.json'
signal_trace=json.loads(signal_path.read_text()) if signal_path.exists() else {}
construction_path=ROOT/'registers/construction-reference.json'
construction=json.loads(construction_path.read_text()) if construction_path.exists() else {}
construction_profiles={p['id']:p for p in construction.get('profiles',[])}
specs = []
for s in all_specs:
    specs.append({k: s[k] for k in [
        'id', 'name', 'group', 'kind', 'parent', 'role', 'installation_status',
        'evidence_status', 'inputs', 'outputs', 'internal', 'hmi', 'networks',
        'electrical_fgs', 'pid_present', 'source_conflicts', 'pending',
        'plc_execution_verified', 'field_verified', 'simulator_model_ready']}
    )
    specs[-1].update(
        direct_rule_count=len(s['direct_rules']), state_path_count=len(s['sequence']),
        test_count=len(s['test_designs']), verification_count=len(s['verification']),
        search=' '.join([s['id'], s['name'], s['group'], s['role']] +
                        [v['원본 심볼'] + ' ' + v['백업 주소'] for v in s['inputs'] + s['outputs'] + s['internal']] +
                        [h['HMI 태그'] for h in s['hmi']]),
        note=equipment_rows[s['id']]['특이점'],
        circuit_fgs=circuit_sheets.get(s['id'],[]),
        construction_pages=construction_profiles.get(s['id'],{}).get('pages',[]),
    )

paths = sorted(str(p.relative_to(ROOT)) for p in ROOT.rglob('*')
               if p.is_file() and p.suffix.lower() in ('.html', '.pdf', '.xml', '.svg', '.png', '.md', '.csv', '.json', '.zap18', '.plf')
               and p.name not in ('all-in-one-data.json', 'all-in-one-verification.json'))
if 'manual-catalog.html' not in paths:
    old_index = ROOT / 'index.html'
    if old_index.exists() and 'data-gme-app' not in old_index.read_text():
        (ROOT / 'manual-catalog.html').write_bytes(old_index.read_bytes())
        paths.append('manual-catalog.html')
paths.extend(p for p in ('registers/priority-equipment.csv', 'registers/all-in-one-data.json') if p not in paths)

program_path = ROOT / 'registers/program-model.json'
program = json.loads(program_path.read_text()) if program_path.exists() else None
results_path = ROOT / 'registers/virtual-plc-test-results.json'
virtual_results = json.loads(results_path.read_text()) if results_path.exists() else None
if virtual_results and virtual_results.get('model_sha256') != hashlib.sha256(program_path.read_bytes()).hexdigest():
    virtual_results = None  # A changed source model must be tested again.
data = dict(
    version='0.4.0', updated='2026-10-09', equipment=specs, priority=priority,
    priority_source=dict(canvas='디코팅 시안', url='https://sejin-facility-manager.romancetiger.chatgpt.site/',
                         observed='2026-10-07', equipment_count=23, edge_count=24, group_count=5,
                         revision='2026-09-30T21:57:30.103Z',
                         layout_is_reference=True, edges_imported=False,
                         groups=['01 원료 투입', '02 열처리', '03 제품 배출', '04 열풍·순환', '05 보조 팬·댐퍼']),
    counts=json.loads((ROOT / 'registers/control-spec-coverage.json').read_text()),
    tests=readcsv('simulation-tests.csv'), verification=readcsv('verification.csv'),
    conflicts=readcsv('source-conflict-review.csv'), resources=paths,
    execution=dict(engine_implemented=bool(program), plc_connected=False, tia_verified=False,
                   full_cpu_emulation=False),
    work_scope=dict(simulator_development='stopped_by_user', simulator_tests='frozen',
                    active=['manual','repair','program_structure','improvement_review']),
    program_counts=program['counts'] if program else {}, virtual_results=virtual_results,
    review_counts=dict(improvement_candidates=len(json.loads((ROOT/'registers/improvement-review.json').read_text())['items']) if (ROOT/'registers/improvement-review.json').exists() else 0,
                      electrical_paths=electrical_trace.get('signal_paths',0),
                      electrical_devices=electrical_trace.get('circuit_guides',0),
                      electrical_sheets=electrical_trace.get('diagrams_visually_reviewed',0),
                      signal_guides=len(signal_trace.get('devices',[])),signal_pin_usages=signal_trace.get('usage_count',0),
                      common_guides=len(json.loads((ROOT/'registers/common-control.json').read_text())['priority_profiles']) if (ROOT/'registers/common-control.json').exists() else 0,
                      repair_guides=len(json.loads((ROOT/'registers/repair-decision.json').read_text())['records']) if (ROOT/'registers/repair-decision.json').exists() else 0,
                      alarm_guides=len(json.loads((ROOT/'registers/alarm-recovery.json').read_text())['profiles']) if (ROOT/'registers/alarm-recovery.json').exists() else 0),
    burner_interface_counts=dict(networks=len(json.loads((ROOT/'registers/burner-interface.json').read_text())['selected_networks']),signals=len(json.loads((ROOT/'registers/burner-interface.json').read_text())['signals'])) if (ROOT/'registers/burner-interface.json').exists() else {},
    process_measurement_counts=dict(channels=len(json.loads((ROOT/'registers/process-measurement.json').read_text())['channels']),outputs=len(json.loads((ROOT/'registers/process-measurement.json').read_text())['outputs']),alarms=len(json.loads((ROOT/'registers/process-measurement.json').read_text())['alarms'])) if (ROOT/'registers/process-measurement.json').exists() else {},
    sensor_measurement_counts=dict(channels=len(json.loads((ROOT/'registers/sensor-measurement.json').read_text())['channels']),networks=len(json.loads((ROOT/'registers/sensor-measurement.json').read_text())['selected_networks']),fgs=len(json.loads((ROOT/'registers/sensor-measurement.json').read_text())['reviewed_fgs'])) if (ROOT/'registers/sensor-measurement.json').exists() else {},
    requirements_audit_counts=json.loads((ROOT/'registers/requirements-audit.json').read_text())['counts'] if (ROOT/'registers/requirements-audit.json').exists() else {},
    project_work_scope=json.loads((ROOT/'registers/body-manual.json').read_text()).get('project_work_scope',{}),
    manual_exclusion_ranges=json.loads((ROOT/'registers/body-manual.json').read_text()).get('manual_exclusion_ranges',[]),
    current_priority_count=21,excluded_priority=['P22','P23'],
    equipment_status_notes=json.loads((ROOT/'registers/body-manual.json').read_text()).get('equipment_status_notes',[]),
    unresolved_identity_counts=json.loads((ROOT/'registers/unresolved-identity.json').read_text())['counts'],
    body_manual_counts=json.loads((ROOT/'registers/body-manual.json').read_text())['counts'] if (ROOT/'registers/body-manual.json').exists() else {},
    recipe_settings_counts=json.loads((ROOT/'registers/recipe-settings.json').read_text())['counts'] if (ROOT/'registers/recipe-settings.json').exists() else {},
    hmi_transfer_counts={k:v for k,v in json.loads((ROOT/'registers/hmi-transfer.json').read_text())['counts'].items() if k in ['tags','windows','native_networks','priority_profiles','shared_address_groups']} if (ROOT/'registers/hmi-transfer.json').exists() else {},
    encoder_position_counts=dict(channels=5,networks=26,counter_calls=5,calibration_paths=2) if (ROOT/'registers/encoder-position.json').exists() else {},
    regulation_counts=dict(loops=len(json.loads((ROOT/'registers/regulation-manual.json').read_text())['loops']),networks=len(json.loads((ROOT/'registers/regulation-manual.json').read_text())['native_ids']),texts=len(json.loads((ROOT/'registers/regulation-manual.json').read_text())['indexed_texts'])) if (ROOT/'registers/regulation-manual.json').exists() else {},
    construction_reference=construction,
    evidence_review=json.loads((ROOT/'registers/evidence-review.json').read_text()) if (ROOT/'registers/evidence-review.json').exists() else dict(items=[],counts={}),
    repair_record_forms=json.loads((ROOT/'registers/repair-record-forms.json').read_text()) if (ROOT/'registers/repair-record-forms.json').exists() else dict(profiles=[],counts={}),
)
# Display existing source references for the current21 only; no new I/O assignments.
def oem_page(fg):
    if str(fg) == '5A': return 6
    if str(fg) == '180A': return 182
    if str(fg) == '180B': return 183
    n=int(fg); return n + (n>5) + 2*(n>180)
circuits_by_id={d['id']:d for d in electrical_trace.get('devices',[])}
bodies_by_id={d['id']:d for d in json.loads((ROOT/'registers/body-manual.json').read_text())['profiles']}
specs_by_id={d['id']:d for d in specs}
drawing_profiles=[]
for item in priority[:21]:
    device=specs_by_id.get(item['plc_id'],{})
    circuit=circuits_by_id.get(item['plc_id'])
    body=bodies_by_id.get(item['plc_id'])
    sheets=[]
    fgs=list(dict.fromkeys(device.get('circuit_fgs',[])+device.get('electrical_fgs',[])))
    for fg in fgs:
        image=next((f'assets/{folder}/FG{fg}.png' for folder in ['circuits','sensor-circuits'] if (ROOT/f'assets/{folder}/FG{fg}.png').is_file()),'')
        sheets.append(dict(id='oem-'+str(fg),kind='OEM 전기',title='FG '+str(fg)+' · PDF '+str(oem_page(fg)),source=electrical_trace['source'],page=oem_page(fg),fg=fg,image=image,extent='원본 한 페이지',status='기존 관련 참조 · 실물 동일성 확인 전',revision='Electrical_Rev2 · 원본 개정란은 PDF에서 확인'))
    if body:
        sheets.append(dict(id='pid-detail',kind='P&ID',title=item['plc_id']+' 본체 참고 영역',source='sources/PID_1684n002I.pdf',page=1,image=body['pid_image'],extent='기존 본체 참고 영역 · 주변 설비 포함',status=body['boundary'],revision='1684n002I · 원본 개정란은 PDF에서 확인'))
    sheets.append(dict(id='pid',kind='P&ID',title='전체 공정 · PDF 1',source='sources/PID_1684n002I.pdf',page=1,image='assets/PID-landscape.png',extent='전체 도면 · 회전 보기',status='공정 전체 참고 · 선택 설비의 전용 회로 아님',revision='1684n002I · 원본 개정란은 PDF에서 확인'))
    for page in device.get('construction_pages',[]):
        image=f'assets/construction/P{page:02}.png'
        sheets.append(dict(id='construction-'+str(page),kind='시공·케이블',title='시공 PDF '+str(page),source=construction['source'],page=page,image=image if (ROOT/image).is_file() else '',extent='원본 한 페이지 · 공유 배치/케이블 포함',status='FOR APPROVAL · 현재 승인·현행 배선 확인 전',revision='24.11.11 first draft design'))
    sheets.append(dict(id='hmi',kind='HMI 참고',title='기존 DECOATER 화면',source='assets/HMI_DECOATER.png',page=None,image='assets/HMI_DECOATER.png',extent='제공된 기존 화면 전체',status='촬영 당시 표시값 · 현재 운전값 아님',revision='이미지 · 촬영 시점 미확인'))
    warnings=[]
    if item['plc_id']=='BC01': warnings.append('시공 PDF21 SS01 CORE=4와 PDF53 3_18 CORE=5G 표기가 다릅니다. 현행 케이블 사양은 확인 전입니다.')
    if item['plc_id']=='FN04': warnings.append('C05: 시공 PDF48의 모터 그림 M34/M38·TAG M31/M34·케이블 M31/M36이 혼재합니다. PDF52의 두 케이블 행과 구분하며 실물 대응은 확인 전입니다.')
    drawing_profiles.append(dict(key=item['key'],plc_id=item['plc_id'],match=item['match'],sheets=sheets,circuit=circuit,warnings=warnings,identity_verified=False,field_verified=False))
data['drawing_workspace']=dict(profiles=drawing_profiles,source_hashes={path:hashlib.sha256((ROOT/path).read_bytes()).hexdigest() for path in ['registers/electrical-trace.json','registers/control-spec.json','registers/construction-reference.json','registers/body-manual.json','sources/Electrical_Rev2.pdf','sources/Electrical_Can_Decoating_20241118.pdf','sources/PID_1684n002I.pdf']},preview_hashes={sheet['image']:hashlib.sha256((ROOT/sheet['image']).read_bytes()).hexdigest() for profile in drawing_profiles for sheet in profile['sheets'] if sheet['image']},scope='current21 source-reference display; no new control claims')
# BC01 alone is the standardization pilot; source records remain unchanged.
bc01_spec=next(p for p in all_specs if p['id']=='BC01')
# Display-only source ASTs; never evaluate or modify the preserved model.
bc01_model=json.loads((ROOT/'registers/program-model.json').read_text())
bc01_control_conditions={}
for rule in bc01_spec['direct_rules']:
    network=next(n for n in bc01_model['networks'] if n['id']==int(rule['네트워크 문서']))
    action=next(a for a in network['actions'] if a['uid']==rule['Part UID'])
    bc01_control_conditions[rule['rule_id']]=dict(network=network['id'],file=network['file'],action={k:v for k,v in action.items() if k in ['uid','gate','name','condition','value']})

data['bc01_standard']=dict(version=1,priority_key='P01',scope='BC01 only; other-equipment expansion held by user',
    sections=['overview','io','control','circuits','alarms','repair','completion'],
    specification=bc01_spec,control_conditions=bc01_control_conditions,
    alarm=next(p for p in json.loads((ROOT/'registers/alarm-recovery.json').read_text())['profiles'] if p['id']=='BC01'),
    repair=next(p for p in json.loads((ROOT/'registers/repair-decision.json').read_text())['records'] if p['key']=='P01'),
    source_hashes={path:hashlib.sha256((ROOT/path).read_bytes()).hexdigest() for path in ['registers/program-model.json','registers/control-spec.json','registers/alarm-recovery.json','registers/repair-decision.json','registers/repair-record-forms.json','registers/electrical-trace.json']},
    field_verified=False,tia_verified=False,repairs_completed=0,simulator_work='stopped_by_user')
dump(ROOT / 'registers/all-in-one-data.json', data)
payload = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c').replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
(ROOT / 'assets/all-in-one-data.js').write_text('window.GME_APP_DATA = ' + payload + ';\n', encoding='utf-8')
with (ROOT / 'registers/priority-equipment.csv').open('w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=list(priority[0]))
    writer.writeheader()
    writer.writerows(priority)

(ROOT / 'index.html').write_text('''<!doctype html>
<html lang="ko" data-gme-app="all-in-one"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="GME 디코팅 설비 매뉴얼, 수리 진단, PLC 분석과 시뮬레이터 준비 자료를 한곳에서 사용하는 통합 프로그램">
<title>GME 올인원 · 설비 매뉴얼과 PLC 작업실</title>
<link rel="stylesheet" href="assets/all-in-one.css"></head><body>
<a class="skip" href="#workspace">본문으로 이동</a>
<aside class="sidebar" aria-label="통합 메뉴와 설비 선택">
<a class="brand" href="#overview"><span class="brand-mark">G</span><span>GME <b>ALL-IN-ONE</b><small>설비 매뉴얼 · PLC 작업실</small></span></a>
<nav class="primary-nav" aria-label="프로그램 메뉴">
<button type="button" data-view="overview">통합 현황</button>
<button type="button" data-view="priority">공정 배치도·설비카드</button>
<button type="button" data-view="simulator">시뮬레이터 · 개발 중지</button>
<button type="button" data-view="structure">PLC 호출·신호 구조</button>
<button type="button" data-view="tests">시험·검증</button>
<button type="button" data-view="review">근거 검토·확인</button>
<button type="button" data-view="notes">개선·작업 메모</button>
<button type="button" data-view="resources">전체 자료</button>
</nav>
<section class="equipment-picker" aria-labelledby="picker-title">
<div class="picker-heading"><h2 id="picker-title">설비 선택</h2><span id="equipment-count"></span></div>
<div class="scope-switch" role="group" aria-label="설비 목록 범위"><button type="button" data-scope="priority" aria-pressed="true">우선 23</button><button type="button" data-scope="all" aria-pressed="false">전체 248</button></div>
<label class="sr-only" for="equipment-search">설비·주소 검색</label><input id="equipment-search" type="search" placeholder="설비명·태그·I/O 주소 검색" autocomplete="off">
<label class="sr-only" for="equipment-group">설비 영역</label><select id="equipment-group"><option value="">전체 영역</option></select>
<div id="equipment-list" class="equipment-list" aria-label="설비 목록"></div>
</section><p class="sidebar-foot">v0.4 · 매뉴얼·수리·구조 분석<br>시뮬레이터 개발 중지</p></aside>
<div class="app-body"><header class="app-header"><div><span class="eyebrow">매뉴얼 · 수리 · 구조 분석 · 개선</span><strong>하나의 화면, 같은 설비 기준</strong></div><div class="header-status"><span class="dot"></span>매뉴얼 작성 중 <span class="chip">시뮬레이터 개발 중지</span></div></header>
<section class="context" aria-labelledby="context-title"><div><span id="context-kicker" class="eyebrow"></span><h1 id="context-title"></h1><p id="context-meta"></p></div><button type="button" id="context-summary">설비 요약</button></section>
<nav id="device-tabs" class="device-tabs" aria-label="선택 설비 작업"></nav>
<main id="workspace" tabindex="-1"><div id="workspace-content"></div><section id="document-workspace" hidden><div class="document-toolbar"><span id="document-label"></span><div><button type="button" id="document-print">인쇄</button><a id="document-source" href="manual-catalog.html" target="_blank" rel="noopener">자료 따로 열기 ↗</a></div></div><iframe id="document-frame" title="통합 자료 보기"></iframe></section></main>
<footer class="app-footer">원본·정적 해석·실행 결과·현장 확인을 구분하여 관리합니다.<span id="app-message" role="status" aria-live="polite"></span></footer></div>
<noscript><p>통합 탐색에는 JavaScript가 필요합니다. <a href="manual-catalog.html">기존 전체 매뉴얼</a>을 열어 자료를 읽을 수 있습니다.</p></noscript>
<div hidden aria-hidden="true"><span id="overview"></span><span id="purpose"></span><span id="equipment"></span><span id="scope"></span><span id="method"></span><span id="read"></span><span id="workflow"></span><span id="program"></span><span id="conflicts"></span><span id="drawing"></span></div>
<script src="assets/all-in-one-data.js"></script><script src="assets/program-model-data.js"></script><script src="assets/virtual-plc.js"></script><script src="assets/simulator-workspace.js"></script><script src="assets/note-record-store.js"></script><script src="assets/repair-records.js"></script><script src="assets/all-in-one.js"></script></body></html>
''', encoding='utf-8')

# Refresh the manual UI and register bundle after rebuilds without changing
# the preserved simulator assets or requiring a cache-clearing action.
entry=(ROOT/'index.html').read_text(encoding='utf-8')
for resource in ('assets/all-in-one.js','assets/all-in-one-data.js','assets/all-in-one.css','assets/note-record-store.js','assets/repair-records.js'):
    digest=hashlib.sha256((ROOT/resource).read_bytes()).hexdigest()[:12]
    entry=entry.replace('"'+resource+'"','"'+resource+'?v='+digest+'"')
(ROOT/'index.html').write_text(entry,encoding='utf-8')

print(json.dumps(dict(status='built', entry='index.html', equipment=len(specs), priority=len(priority),
                      tests=len(data['tests']), verification=len(data['verification']),
                      bundle_bytes=(ROOT / 'assets/all-in-one-data.js').stat().st_size,
                      simulator_engine_implemented=bool(program)), ensure_ascii=False))
