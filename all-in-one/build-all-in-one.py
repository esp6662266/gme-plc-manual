# coding: utf-8
"""Build the single-entry web workspace from preserved manual registers.

The application uses a small, embedded data bundle and existing documents.
No PLC execution or SEJIN writes are performed by this build or the UI.
"""
from pathlib import Path
import csv
import json
import hashlib
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from collections import defaultdict

ROOT = Path(__file__).resolve().parent
release=json.loads((ROOT/'VERSION.json').read_text(encoding='utf-8'))

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

paths = sorted(p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*')
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
    version=release['version'], updated=release['released'], equipment=specs, priority=priority,
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
    work_scope=dict(simulator_development='stopped_by_user', simulator_tests='frozen', simulator_policy='permanently_stopped',
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

# Pin evidence is a read-only annotation, not an executable condition.
bc01_pin_evidence={}
bc01_network_map={n['document_id']:n for n in json.loads((ROOT/'sources/decoded-original/network-map.json').read_text())}
lad_ns={'s':'http://www.siemens.com/automation/2015/FunctionLadderDiagram'}
for rule in [r for r in bc01_spec['direct_rules'] if r['opaque']]:
    network=bc01_network_map[int(rule['네트워크 문서'])]
    file='sources/decoded-original/'+network['xml_file']
    xml=ET.parse(ROOT/file).getroot()
    parts={p.get('UId'):p for p in xml.find('s:Parts',lad_ns)}
    wires=list(xml.find('s:Wires',lad_ns))
    uid=rule['Part UID'];gate=parts[uid].get('Gate');target_pin='en' if gate=='Move' else 'in'
    incoming=[w for w in wires if any(c.get('UId')==uid and c.get('PinName')==target_pin for c in w)]
    assert len(incoming)==1
    wire=incoming[0];upstream=[c for c in wire if c.tag.endswith('PCon') and c.get('UId')!=uid]
    assert len(upstream)==1
    source_uid=upstream[0].get('UId');source_pin=upstream[0].get('PinName')
    assert source_pin in ('eno','out')
    def pin_reference(part_uid,pin):
        found=[c for w in wires if any(c.get('UId')==part_uid and c.get('PinName')==pin for c in w) for c in w if c.tag.endswith('OCon')]
        assert len(found)==1
        oref=found[0].get('UId');ref_id=parts[oref].get('RefId');resolved=network['resolved_operands'][oref]
        declarations=[]
        for filename in resolved['identifier_files']:
            path='sources/decoded-original/'+filename
            for access in ET.parse(ROOT/path).getroot():
                ident=next((c for c in access if c.tag.endswith('ID') and c.get('RID')==ref_id),None)
                if ident is not None and any(c.get('UID')==oref and c.get('NID')==network['inferred_original_nid'] for c in ident.iter()):
                    literal=next((c for c in access.iter() if c.tag.endswith('CB')),None)
                    aos=next((c for c in access.iter() if c.tag.endswith('AOS')),None)
                    name=literal.get('V') if literal is not None else '.'.join(c.get('N') for c in aos if c.tag.endswith('AO')) if aos is not None and len(aos) else ident.get('N')
                    assert name==resolved['name']
                    declarations.append(dict(oref=oref,ref_id=ref_id,nid=network['inferred_original_nid'],identifier_file=path,name=name,scope=ident.get('S')))
        assert len(declarations)==1
        return declarations[0]
    source_gate=parts[source_uid].get('Gate')
    source=dict(uid=source_uid,gate=source_gate,pin=source_pin,target=pin_reference(source_uid,'out1' if source_gate=='Move' else 'operand'))
    target=dict(uid=uid,gate=gate,pin=target_pin,target=pin_reference(uid,'out1' if gate=='Move' else 'operand'))
    if source_gate=='Move':source['value']=pin_reference(source_uid,'in')
    if gate=='Move':target['value']=pin_reference(uid,'in')
    bc01_pin_evidence[rule['rule_id']]=dict(network=network['document_id'],file=file,wire=wire.get('UId'),source=source,target=target,status='static_pin_connection_only',execution_verified=False)

bc01_media_evidence={'checked': '2026-10-11', 'source_site': 'https://sejin-facility-manager.romancetiger.chatgpt.site/', 'source_card': 'BC-01(벨트)', 'method': 'read_only_visible_ui_and_visual_review', 'raw_images_copied': False, 'identity_verified': False, 'field_verified': False, 'groups': [{'id': 'belt', 'title': '벨트·본체'}, {'id': 'drive', 'title': '모터·구동부'}, {'id': 'chain', 'title': '체인·스프로킷'}, {'id': 'support', 'title': '축받침·장력부'}, {'id': 'reference', 'title': '도면·시험·참고'}], 'photos': [{'id': 'photo-01', 'source_order': 1, 'group': 'belt', 'title': '경사 벨트·프레임', 'kind': 'photograph', 'original_url': 'https://sejin-facility-manager.romancetiger.chatgpt.site/api/photos/photo_1778489279552_9081_8f5e', 'observation': '경사 컨베이어의 벨트와 지지 프레임이 보입니다.', 'pending': '촬영 시점·현재 설치 위치·BC01 실물 동일성을 확인합니다.', 'field_verified': False}, {'id': 'photo-02', 'source_order': 2, 'group': 'belt', 'title': '이전 설비자료의 컨베이어', 'kind': 'historical_photograph', 'original_url': 'https://sejin-facility-manager.romancetiger.chatgpt.site/api/photos/excel%3Aphoto%3A5b9b979c090c3a952fee5e44?v=2d6cd8a4b139458acff542dc733b8b6e6dcd8f1da89b0f8d6ce0257251f26c9a', 'observation': '엑셀 설비자료에 등록된 컨베이어·가드 참고 사진입니다.', 'pending': '등록 자료와 현재 설비의 동일성·촬영 시점은 확인 전입니다.', 'field_verified': False}, {'id': 'photo-03', 'source_order': 3, 'group': 'chain', 'title': '분리된 스프로킷·줄자 1', 'kind': 'photograph', 'original_url': 'https://sejin-facility-manager.romancetiger.chatgpt.site/api/photos/photo_1787117258069_5653_1929', 'observation': '바닥에 놓인 스프로킷과 줄자가 보입니다.', 'pending': '치수·치수 기준·잇수·설치 측·부품 번호는 승인 도면과 실물로 확인합니다.', 'field_verified': False}, {'id': 'photo-04', 'source_order': 4, 'group': 'reference', 'title': 'BEARING TEST 그래픽', 'kind': 'test_graphic', 'original_url': 'https://sejin-facility-manager.romancetiger.chatgpt.site/api/photos/photo_1787117549952_4411_bxn8', 'observation': 'BC-01 BEARING TEST 문구의 그래픽입니다. 실제 베어링 사진이 아닙니다.', 'pending': '현장 시험·배선 이상·고장·복구의 증거로 사용하지 않습니다.', 'field_verified': False}, {'id': 'photo-05', 'source_order': 5, 'group': 'reference', 'title': '체인 스프라켓 사양 도면 이미지', 'kind': 'technical_drawing_image', 'original_url': 'https://sejin-facility-manager.romancetiger.chatgpt.site/api/photos/photo_1787118145180_1789_mpcq', 'observation': '이미지 제목에 Chain 80-18T가 보입니다. 부품 도면을 촬영·등록한 자료입니다.', 'pending': '현장 적용 도면·설치 측·개정·승인 원본은 확인 전입니다. 이미지로 제작 치수를 확정하지 않습니다.', 'field_verified': False}, {'id': 'photo-06', 'source_order': 6, 'group': 'reference', 'title': '동일성 미확인 3D 참고', 'kind': 'unidentified_3d', 'original_url': 'https://sejin-facility-manager.romancetiger.chatgpt.site/api/photos/photo_1787107597033_7642_j8ln', 'observation': '플랫폼·호퍼 형태의 3D 참고 이미지입니다. BC01 식별 표기는 확인되지 않습니다.', 'pending': 'BC01 본체·모터·PLC 신호에 직접 대응시키지 않습니다.', 'field_verified': False}, {'id': 'photo-07', 'source_order': 7, 'group': 'chain', 'title': '분리된 스프로킷 2', 'kind': 'photograph', 'original_url': 'https://sejin-facility-manager.romancetiger.chatgpt.site/api/photos/photo_1787116885164_4599_q6y5', 'observation': '분리된 스프로킷의 외관 사진입니다.', 'pending': '마모 판정·잇수·동일 부품·교체 전후 관계는 확인 전입니다.', 'field_verified': False}, {'id': 'photo-08', 'source_order': 8, 'group': 'chain', 'title': '분리된 스프로킷·줄자 2', 'kind': 'photograph', 'original_url': 'https://sejin-facility-manager.romancetiger.chatgpt.site/api/photos/photo_1787117169000_6122_8wg0', 'observation': '스프로킷과 줄자가 함께 보입니다.', 'pending': '줄자 사진만으로 교체 규격이나 교체 완료를 판단하지 않습니다.', 'field_verified': False}, {'id': 'photo-09', 'source_order': 9, 'group': 'drive', 'title': '컨베이어 주변 모터 1', 'kind': 'photograph', 'original_url': 'https://sejin-facility-manager.romancetiger.chatgpt.site/api/photos/photo_1779107633205_3858_sud7', 'observation': '상부 지지 구조의 모터·팬 커버·배선관이 보입니다. 명판은 판독되지 않습니다.', 'pending': 'M02와의 실물 대응·모터 모델·정격·현행 배선은 확인 전입니다.', 'field_verified': False}, {'id': 'photo-10', 'source_order': 10, 'group': 'drive', 'title': '컨베이어 주변 모터 2', 'kind': 'photograph', 'original_url': 'https://sejin-facility-manager.romancetiger.chatgpt.site/api/photos/photo_1779119208962_5448_3x8u', 'observation': '앞 모터 사진과 비슷한 구도의 별도 등록 사진입니다.', 'pending': '중복·교체 전후·동일 촬영 시점으로 확정하지 않습니다. 원본 등록을 보존합니다.', 'field_verified': False}, {'id': 'photo-11', 'source_order': 11, 'group': 'belt', 'title': '벨트 연결부', 'kind': 'photograph', 'original_url': 'https://sejin-facility-manager.romancetiger.chatgpt.site/api/photos/photo_1778489213424_8861_9y4h', 'observation': '벨트 연결부와 여러 체결 요소가 보입니다.', 'pending': '규격·체결 토크·이상 유무·복구 완료는 사진만으로 확인할 수 없습니다.', 'field_verified': False}, {'id': 'photo-12', 'source_order': 12, 'group': 'support', 'title': '축받침·장력 조절부 주변', 'kind': 'photograph', 'original_url': 'https://sejin-facility-manager.romancetiger.chatgpt.site/api/photos/photo_1778489188097_9746_e8ez', 'observation': '축받침 주변과 나사식 조절 기구가 보입니다.', 'pending': '베어링 형식·규격·설치 측·정확한 위치를 확인합니다.', 'field_verified': False}], 'references': {'belt': {'description': 'P&ID의 BC-01 경사 컨베이어는 본체·벨트 위치를 비교할 참고입니다. 기계 부품에 전용 PLC 신호를 배정하지 않습니다.', 'paths': [], 'documents': [['P&ID · BC01 위치', 'sources/PID_1684n002I.pdf#page=1']]}, 'drive': {'description': 'P&ID의 M02 및 OEM FG18의 M02는 모터 위치·구동 계통 비교 자료입니다. 사진과 M02의 동일성을 확정한 연결이 아닙니다.', 'paths': [1, 2], 'documents': [['P&ID · M02 참고', 'sources/PID_1684n002I.pdf#page=1'], ['OEM FG18 · PDF19', 'sources/Electrical_Rev2.pdf#page=19']]}, 'chain': {'description': '기계 전달 부품 참고입니다. 스프로킷에 직접 PLC 입출력·알람을 배정한 근거는 확보하지 못했습니다.', 'paths': [], 'documents': [['P&ID · 본체 계통 참고', 'sources/PID_1684n002I.pdf#page=1']]}, 'support': {'description': '사진에 보이는 축받침·조절 기구의 위치와 형식을 먼저 확인합니다. 베어링 고장 신호나 전용 알람으로 연결하지 않습니다.', 'paths': [], 'documents': [['P&ID · 본체 계통 참고', 'sources/PID_1684n002I.pdf#page=1']]}, 'reference': {'description': '도면 이미지·TEST 그래픽·동일성 미확인 3D를 현장 사진과 구분합니다. 등록 태그는 실제 고장·정상·복구 판정이 아닙니다.', 'paths': [], 'documents': []}}, 'missing': [{'title': '현재 ABB 인버터 명판·단자', 'paths': [1, 2], 'text': '현재 제작사는 사용자 확인으로 ABB입니다. 사진12장에서는 인버터 명판·단자를 식별하지 못했습니다. 정확한 모델·정격·접속을 확보합니다.'}, {'title': 'SS01 트립와이어·현행 접점', 'paths': [0, 3], 'text': 'FG19의 SS01 11/12 기동 허가와 13/14 감시 경로는 보존 도면 근거입니다. 현장 설치·접점·정상 극성 사진은 추가 확인합니다.'}, {'title': 'SSL01 회전 감시 예비', 'paths': [4], 'text': 'FG19의 SSL01은 SPARE 표기입니다. 실제 설치·사용 여부와 현행 접속은 확인 전입니다.'}], 'part_revision_boundary': '스프로킷 이미지에는 80-18T가 보이지만 현재 적용 규격을 확정하지 않습니다. 설치 측·개정·승인 원본·실물 잇수를 대조한 뒤 선택합니다.'}

# Additional, display-only native paths. They do not extend the execution AST.
def bc01_native_ref(network_id, part_uid, pin):
    n=bc01_network_map[network_id]
    file='sources/decoded-original/'+n['xml_file']
    xml=ET.parse(ROOT/file).getroot()
    wires=[w for w in xml.findall('s:Wires/s:Wire',lad_ns)
           if any(c.get('UId')==part_uid and c.get('PinName')==pin for c in w)]
    assert len(wires)==1,(network_id,part_uid,pin)
    refs=[c for c in wires[0] if c.tag.endswith('OCon')]
    assert len(refs)==1
    oref=refs[0].get('UId')
    operand=next(p for p in xml.findall('s:Parts/s:ORef',lad_ns) if p.get('UId')==oref)
    rid=operand.get('RefId');resolved=n['resolved_operands'][oref]
    declarations=[]
    # ON/UID/RID can recur in other blocks. Restrict to the reviewed context.
    declaration_files={1692:['0661-IdentXmlPart.xml','0662-IdentXmlPart.xml','0664-IdentXmlPart.xml'],
        1018:['0613-IdentXmlPart.xml','0615-IdentXmlPart.xml','0616-IdentXmlPart.xml'],
        1768:['0675-IdentXmlPart.xml','0676-IdentXmlPart.xml','0678-IdentXmlPart.xml']}
    for filename in declaration_files[network_id]:
        path='sources/decoded-original/'+filename
        for access in ET.parse(ROOT/path).getroot():
            ident=next((c for c in access if c.tag.endswith('ID') and c.get('RID')==rid),None)
            if ident is None:continue
            matches=[c for c in ident.iter() if c.get('NID')==n['inferred_original_nid'] and c.get('UID')==oref]
            if not matches:continue
            assert len(matches)==1
            literal=next((c for c in access.iter() if c.tag.endswith('CB')),None)
            names=[c.get('N') for c in access.iter() if c.tag.endswith('AO')]
            name=literal.get('V') if literal is not None else '.'.join(names) if names else ident.get('N')
            assert name==resolved['name']
            td=next(c for c in access.iter() if c.tag.endswith('TD'))
            declarations.append(dict(oref=oref,rid=rid,nid=n['inferred_original_nid'],name=name,
                scope=ident.get('S'),type=td.get('T').split(':')[0],identifier_file=path,
                role='write' if matches[0].get('AK')=='Write' else 'read',literal_value=literal.get('V') if literal is not None else None))
    assert len(declarations)==1,(network_id,oref)
    return dict(network=network_id,file=file,part=part_uid,pin=pin,wire=wires[0].get('UId'),**declarations[0])

bc01_supplemental=[]
for network,uid,gate,section,title,pins,enable_parts,enable_wire in [
    (1692,'39','Mul','speed','속도 설정값의 계산·출력 연결',['in1','in2','out'],['34'],'54'),
    (1018,'1108','Add','other','같은 누적값의 증가와 0 쓰기',['in1','in2','out'],['1154','1156'],'1157'),
    (1768,'22','CRef','alarms','별도 계측 호출의 값·범위 출력',['IN0','Analog_input','Coeff','Zero','OutValue','Out_of_range'],['21'],'33')]:
    file='sources/decoded-original/'+bc01_network_map[network]['xml_file']
    xml=ET.parse(ROOT/file).getroot()
    part=next(p for p in xml.find('s:Parts',lad_ns) if p.get('UId')==uid)
    assert (part.tag.endswith('CRef') if gate=='CRef' else part.get('Gate')==gate)
    wire=next(w for w in xml.findall('s:Wires/s:Wire',lad_ns) if w.get('UId')==enable_wire)
    assert any(c.get('UId')==uid and c.get('PinName')=='en' for c in wire)
    bc01_supplemental.append(dict(id=f'{network}:{uid}',network=network,file=file,part=uid,gate=gate,
        section=section,title=title,refs=[bc01_native_ref(network,uid,pin) for pin in pins],
        enable_refs=[bc01_native_ref(network,p,'operand') for p in enable_parts],enable_wire=enable_wire,
        execution_verified=False,field_verified=False,internal_xml_mapping_verified=False))

def bc01_access(file,rid):
    rows=[a for a in ET.parse(ROOT/file).getroot() if any(c.tag.endswith('ID') and c.get('RID')==rid for c in a)]
    assert len(rows)==1
    return rows[0]

bc01_addresses=[]
hmi_source=list(csv.DictReader((ROOT/'sources/hmi_plc_tags.csv').open(encoding='utf-8-sig',newline='')))
for name,type_name,address,tag,parent_file,parent_rid,member_file,member_rid,bits,width in [
    ('HMI_DB.SET_PERC_BC01','Int','DB41.DBW52','data_DB41_DBW52','0660','147','0662','148',416,16),
    ('102A5_SPARE0','Word','%QW288','AW288',None,None,'0664','144',2304,16),
    ('Flag.M_BC_01','Bool','DB2.DBX0.0','BC_01\\Flag','0603','2','0604','41',0,1)]:
    member_path='sources/decoded-original/'+member_file+'-IdentXmlPart.xml'
    access=bc01_access(member_path,member_rid)
    ssd=next(e for e in access.iter() if e.tag.endswith('SSD'))
    td=next(e for e in access.iter() if e.tag.endswith('TD'))
    assert int(ssd.get('AO'))==bits and td.get('T').split(':')[0]==type_name
    proof=[dict(file=member_path,rid=member_rid,offset_bits=bits,width_bits=width)]
    if parent_file:
        parent_path='sources/decoded-original/'+parent_file+'-IdentXmlPart.xml'
        parent=bc01_access(parent_path,parent_rid)
        tod=next(e for e in parent.iter() if e.tag.endswith('TOD'))
        bad=next(e for e in access.iter() if e.tag.endswith('BAD'))
        assert bad.get('BIRID')==parent_rid and tod.get('BT')=='DB'
        aos=[e for e in access.iter() if e.tag.endswith('AO')]
        assert int(aos[-1].get('BO'))==bits and int(aos[-1].get('BS'))==width
        derived=f"DB{tod.get('N')}.DBX{bits//8}.{bits%8}" if type_name=='Bool' else f"DB{tod.get('N')}.DBW{bits//8}"
        assert derived==address
        proof.insert(0,dict(file=parent_path,rid=parent_rid,db_number=tod.get('N')))
    else:
        sad=next(e for e in access.iter() if e.tag.endswith('SAD'))
        assert sad.get('R')=='Output' and sad.get('SAM')=='Peripherie' and address==f'%QW{bits//8}'
    hmi=next(r for r in hmi_source if r['HMI 태그']==tag)
    bc01_addresses.append(dict(name=name,type=type_name,backup_address=address,hmi=hmi,
        access_mode='Peripherie' if not parent_file else 'DB',declarations=proof,
        static_address_verified=True,current_mapping_verified=False,screen_read_write_verified=False,retain_verified=False))

# Row IDs only on the existing BC01 source tables; source cells stay unchanged.
bc01_locations=defaultdict(set)
for rule in bc01_spec['direct_rules']:bc01_locations[int(rule['네트워크 문서'])].add(('part',rule['Part UID']))
bc01_alarm=next(p for p in json.loads((ROOT/'registers/alarm-recovery.json').read_text())['profiles'] if p['id']=='BC01')
for alarm in bc01_alarm['alarms']:
    for action in alarm['actions']:bc01_locations[action['network']].add(('part',action['uid']))
    for usage in alarm['usages']:bc01_locations[usage['network']].add(('part',usage['part']))
for timer in bc01_alarm['timers']:bc01_locations[timer['network']].add(('part',timer['uid']))
for evidence in bc01_pin_evidence.values():
    bc01_locations[evidence['network']].update([('part',evidence['source']['uid']),('part',evidence['target']['uid']),('wire',evidence['wire'])])
for evidence in bc01_supplemental:
    bc01_locations[evidence['network']].update([('part',evidence['part']),('wire',evidence['enable_wire'])])
    for ref in evidence['refs']+evidence['enable_refs']:
        bc01_locations[evidence['network']].update([('part',ref['part']),('wire',ref['wire'])])

class BC01SourceRows(HTMLParser):
    def __init__(self,text,allowed,prefix='bc01'):
        super().__init__(convert_charrefs=True)
        self.prefix=prefix;self.text=text;self.allowed=allowed;self.edits=[];self.found=set();self.anchors={};self.headers=[];self.cells=[];self.cell=None;self.start=None
        self.lines=[0]
        for i,c in enumerate(text):
            if c=='\n':self.lines.append(i+1)
    def handle_starttag(self,tag,attrs):
        if tag=='table':self.headers=[]
        if tag=='tr':
            line,col=self.getpos();self.start=(self.lines[line-1]+col,self.get_starttag_text(),dict(attrs));self.cells=[]
        if tag in ('th','td'):self.cell=(tag,[])
    def handle_data(self,text):
        if self.cell:self.cell[1].append(text)
    def handle_endtag(self,tag):
        if tag in ('th','td') and self.cell:
            kind,values=self.cell;value=''.join(values).strip()
            if kind=='th':self.headers.append(value)
            else:self.cells.append(value)
            self.cell=None
        if tag=='tr' and self.start and self.cells:
            kind='part' if self.headers[:1]==['Part UID'] else 'wire' if self.headers[:1]==['Wire UID'] else None
            key=(kind,self.cells[0])
            if key in self.allowed:
                assert key not in self.found,key
                self.found.add(key);pos,original,attrs=self.start;anchor=f'{self.prefix}-{kind}-{self.cells[0]}'
                existing=attrs.get('id')
                if existing and existing!=anchor:
                    # Shared source rows keep the first published equipment anchor.
                    import re
                    assert re.fullmatch(r'(?:bc01|gme-[a-z0-9]+)-'+kind+'-'+re.escape(self.cells[0]),existing),(key,existing)
                    anchor=existing
                self.anchors[key]=anchor
                if 'id' not in attrs:self.edits.append((pos,len(original),original[:-1]+' id="'+anchor+'">'))
        if tag=='tr':self.start=None

bc01_source_locations=[]
for network,allowed in sorted(bc01_locations.items()):
    path=ROOT/f'networks/network-{network}.html';text=path.read_text();parser=BC01SourceRows(text,allowed);parser.feed(text)
    assert parser.found==allowed,(network,allowed-parser.found)
    for pos,length,value in sorted(parser.edits,reverse=True):text=text[:pos]+value+text[pos+length:]
    style='<style id="bc01-source-locations">tr[id^="bc01-"]{scroll-margin-top:65px}tr[id^="bc01-"]:target td{background:#e0f2e9!important;box-shadow:inset 0 2px #167769,inset 0 -2px #167769}tr[id^="bc01-"]:target td:first-child{font-weight:800;border-left:4px solid #167769}</style>'
    if 'id="bc01-source-locations"' not in text:text=text.replace('</head>',style+'</head>',1)
    if text!=path.read_text():path.write_text(text)
    bc01_source_locations.extend(dict(network=network,kind=kind,uid=uid,path=f'networks/network-{network}.html#bc01-{kind}-{uid}') for kind,uid in sorted(allowed))

data['bc01_standard']=dict(version=1,priority_key='P01',scope='BC01 only; other-equipment expansion held by user',
    sections=['overview','io','control','circuits','alarms','repair','completion'],
    specification=bc01_spec,control_conditions=bc01_control_conditions,pin_evidence=bc01_pin_evidence,media_evidence=bc01_media_evidence,
    alarm=bc01_alarm,supplemental_evidence=bc01_supplemental,address_evidence=bc01_addresses,source_locations=bc01_source_locations,
    repair=next(p for p in json.loads((ROOT/'registers/repair-decision.json').read_text())['records'] if p['key']=='P01'),
    source_hashes={path:hashlib.sha256((ROOT/path).read_bytes()).hexdigest() for path in ['registers/program-model.json','registers/control-spec.json','registers/alarm-recovery.json','registers/repair-decision.json','registers/repair-record-forms.json','registers/electrical-trace.json','sources/decoded-original/network-map.json']+sorted({e['file'] for e in bc01_pin_evidence.values()} | {ref['identifier_file'] for e in bc01_pin_evidence.values() for part in [e['source'],e['target']] for key,ref in part.items() if key in ('target','value')})},
    field_verified=False,tia_verified=False,repairs_completed=0,simulator_work='stopped_by_user')
bc01_extra_sources={'sources/hmi_plc_tags.csv','registers/plc-symbols.csv'}
for evidence in bc01_supplemental:
    bc01_extra_sources.add(evidence['file'])
    bc01_extra_sources.update(r['identifier_file'] for r in evidence['refs']+evidence['enable_refs'])
for address in bc01_addresses:bc01_extra_sources.update(r['file'] for r in address['declarations'])
data['bc01_standard']['source_navigation']=dict(
    facility_id='3',equipment='BC-01(벨트)',
    url='https://sejin-facility-manager.romancetiger.chatgpt.site/?facility=3&mode=detail',
    destination='card_detail',tabs=['작업이력','사진'],checked='2026-10-11',
    histories_copied=False,automatic_sync=False)
bc01_rel_nodes=[
 dict(id='request',group='request',title='운전 요청 Set',caption='Flag.M_BC_01',rule_ids=['1843:492','1844:1162'],note='자동 종류1/2의 보존 요청 경로입니다. 비교값24/43을 실제 시간으로 확정하지 않습니다.'),
 dict(id='memo',group='request',title='기동 기억 Set/Reset',caption='MemoCMD_BC01_Startup',rule_ids=['1843:102','1843:828'],note='Set의 선행492.out→102.in은 핀 연결만 확인됐습니다. Reset의 전체 NOT 조건을 보존합니다.'),
 dict(id='request-reset',group='request',title='운전 요청 Reset',caption='Flag.M_BC_01 해제',rule_ids=['1847:927','1935:198'],note='종류5 정지 경로와 알람에 따른 요청 해제를 구분합니다. UNDER TESTING 반전은 FC 분기에만 있습니다.'),
 dict(id='output',group='output',title='최종 출력 허가',caption='Start BC01 · %Q0.0',rule_ids=['1935:202'],note='ON과 운전 요청은 세 OR 경로 모두에서 읽습니다. R1_GATE_LOOP_ON·기동 기억·정비 모드의 분기를 원본과 대조합니다.'),
 dict(id='timer',group='output',title='기동 감시 타이머',caption='Tag_51 · S5T#2S',rule_ids=[],note='FAULT와 INV의 감시가 공유하는 보존 타이머 비트입니다. 실제 경과시간·현재 상태는 미취득입니다.'),
 dict(id='fault',group='alarm',title='운전 응답 고장',caption='Allarm.BC_01_FAULT',rule_ids=['1785:223','1785:228'],note='처리된 운전 응답의 반전과 감시 비트를 읽습니다. Reset에는 응답 정상화 직접 접점이 없습니다.'),
 dict(id='inv',group='alarm',title='인버터 이상',caption='Allarm.BC01_INV',rule_ids=['1785:27','1785:267'],note='처리된 인버터 이상과 감시 비트를 읽습니다. Reset에는 이상 해소 직접 접점이 없습니다.'),
 dict(id='trip',group='alarm',title='트립와이어 감시',caption='Allarm.BC_01_FC',rule_ids=['1786:234','1786:240'],note='발생 경로에 Start BC01·Tag_51 직접 접점은 없습니다. Reset은 처리 트립 신호의 반전을 포함하며 실물 정상 극성은 확인 전입니다.')]
bc01_rel_edges=[
 dict(from_names=['Flag.M_BC_01','Flag.R1_GATE_LOOP_ON','MemoCMD_BC01_Startup','Flag.Maintenance_ON'],to='Start BC01',rules=['1935:202'],note='세 OR 허가 경로의 접점 참조입니다. 각 경로의 ON·요청 조건을 함께 확인합니다.'),
 dict(from_names=['Start BC01','Inputs.BC01 run','Inputs.BC01_All_inv'],to='Tag_51',rules=['1785:217'],note='운전 응답/인버터 이상 두 감시 경로가 타이머를 공유합니다.'),
 dict(from_names=['Start BC01','Tag_51','Inputs.BC01 run'],to='Allarm.BC_01_FAULT',rules=['1785:223'],note='응답 접점은 반전입니다. 입력 정상 극성·현재 전달은 확인 전입니다.'),
 dict(from_names=['Start BC01','Tag_51','Inputs.BC01_All_inv'],to='Allarm.BC01_INV',rules=['1785:27'],note='인버터 이상 감시의 읽기→Set 참조입니다.'),
 dict(from_names=['Inputs.BC01 trip wire'],to='Allarm.BC_01_FC',rules=['1786:234'],note='Start·타이머 직접 접점 없이 처리 트립 신호를 읽습니다.'),
 dict(from_names=['Allarm.BC_01_FAULT','Allarm.BC01_INV','Allarm.BC_01_FC'],to='Flag.M_BC_01',rules=['1935:198'],note='알람을 읽어 요청을 Reset하는 경로입니다. FC 분기의 UNDER TESTING 반전을 보존합니다.'),
 dict(from_names=['Flag.RESET_ALLARM','Allarm.BC_01_FAULT'],to='Allarm.BC_01_FAULT',rules=['1785:228'],note='공통 ON·리셋·자기 래치가 Reset 조건입니다.'),
 dict(from_names=['Flag.RESET_ALLARM','Allarm.BC01_INV'],to='Allarm.BC01_INV',rules=['1785:267'],note='공통 ON·리셋·자기 래치가 Reset 조건입니다.'),
 dict(from_names=['Flag.RESET_ALLARM','Inputs.BC01 trip wire','Allarm.BC_01_FC'],to='Allarm.BC_01_FC',rules=['1786:240'],note='처리 트립 신호의 반전을 포함하는 Reset 경로입니다.')]
for edge in bc01_rel_edges:edge['from']=edge.pop('from_names')
data['bc01_standard']['relationships']=dict(nodes=bc01_rel_nodes,edges=bc01_rel_edges,scope='static_read_write_only',execution_verified=False,raw_input_mapping_verified=False)
def bc01_target(label,section,item,**kwargs):return dict(label=label,section=section,item=item,**kwargs)
def bc01_card(id,title,signals,observe,compare,pending,rules,targets):return dict(id=id,title=title,signals=signals,observe=observe,compare=compare,pending=pending,rules=rules,targets=targets)
request_jump=bc01_target('요청·모드 근거','control','request')
output_jump=bc01_target('최종 출력 허가','control','output')
reset_jump=bc01_target('알람에 따른 요청 해제','control','reset')
alarms_jump=[bc01_target(t,'alarms','alarm-'+str(i)) for i,t in enumerate(['운전 응답 고장','인버터 이상','트립와이어 감시'])]
circuit_jump=lambda i:bc01_target('전기 전달 경로 '+str(i+1),'circuits','path-'+str(i))
data['bc01_standard']['repair_navigation']={
 'request':[
  bc01_card('mode','모드·자동 단계','Data.Tipo_preset · Flag.Auto_ON1 · Data.Tempo_presetting','요청 전후의 모드·단계 값과 조작 시각을 따로 기록합니다.','종류1/2의 요청 Set과 종류5의 정지 Reset을 원본과 비교합니다.','현재 호출·24/43/13의 실제 시간 의미·HMI 조작 전달은 확인 전입니다.',['1843:492','1844:1162','1847:927'],[request_jump]),
  bc01_card('writers','요청의 여러 쓰기','Flag.M_BC_01','운전 요청이 생긴 시각과 사라진 시각을 비교합니다.','Set/Reset의 쓰기 위치를 함께 확인하고 UID 나열을 실행 순서로 해석하지 않습니다.','현재 OB/호출·다른 쓰기·외부 요청과 최종값은 확인 전입니다.',['1843:492','1844:1162','1847:927','1935:198'],[request_jump,reset_jump]),
  bc01_card('memo','기동 기억','MemoCMD_BC01_Startup','기동 기억의 관찰값·변화 시각·수집 위치를 기록합니다.','Set의492.out→102.in 연결과 전체조건 NOT의 별도 Reset을 비교합니다.','ENO/out 실제 전달·초기화·현재 호출/다른 쓰기는 확인 전입니다.',['1843:102','1843:828'],[request_jump]),
  bc01_card('alarm-reset','알람에 따른 요청 해제','Allarm.BC_01_FAULT · BC01_INV · BC_01_FC','최초 알람과 운전 요청이 해제된 시각을 따로 기록합니다.','1935:198의 세 분기와 FC 분기의 UNDER TESTING 반전을 확인합니다.','원인 후보를 확정 고장으로 바꾸지 않고 현재 발생 순서를 확보합니다.',['1935:198'],[reset_jump,*alarms_jump])],
 'permit':[
  bc01_card('base','공통 조건·운전 요청','ON · Flag.M_BC_01','최종 출력을 관찰한 시각의 ON·운전 요청을 함께 기록합니다.','세 OR 허가 경로에 공통으로 들어가는 ON과 요청 접점을 확인합니다.','현재 CPU 주소·호출·다른 쓰기와 요청 유지 상태는 확인 전입니다.',['1935:202'],[output_jump,request_jump]),
  bc01_card('or','세 OR 허가 경로','Flag.R1_GATE_LOOP_ON · MemoCMD_BC01_Startup · Flag.Maintenance_ON','세 분기의 실제 값과 운전 모드를 각각 기록합니다.','한 경로의 참이 OR 허가를 구성하지만 현재 운전 완료를 입증하지는 않습니다.','각 허가의 현재 생성 위치·공통 ON·요청·호출을 함께 대조합니다.',['1935:202'],[output_jump]),
  bc01_card('q','최종 PLC 출력','Start BC01 · %Q0.0','출력 비트가 변하는 시각과 수집한 CPU/화면을 기록합니다.','1935:202의 코일 조건과 도면상 기동 전달 위치를 구분합니다.','현재 CPU·Q 변화·다른 출력 쓰기·현장 기동 전달은 확인 전입니다.',['1935:202'],[output_jump,circuit_jump(0)]),
  bc01_card('field','현장 직렬 허가','SS01 · 18QS1 · 18QM1 · 19KA1','보존 도면의 직렬 접점·릴레이 코일/접점을 구간별로 비교할 위치입니다.','FG19/PDF20의 기동 회로와 FG18/PDF19의 DI1 도착점을 확인합니다.','현재 ABB 모델·단자·접속·전압·접점 상태는 확인 전입니다.',['1935:202'],[circuit_jump(0),bc01_target('실물 확인 준비','completion','field')])],
 'stop':[
  bc01_card('first','최초 변화와 후속 알람','알람3개 · 처리 Inputs · Flag.M_BC_01 · %Q0.0','최초/후속 알람과 요청·출력 OFF의 관찰 시각을 구분합니다.','알람 발생 조건과1935:198의 요청 Reset 경로를 비교합니다.','같이 정지한 설비만으로 최초 원인·소유 관계를 확정하지 않습니다.',['1935:198'],[*alarms_jump,reset_jump]),
  bc01_card('reset','정지 요청의 쓰기','Flag.M_BC_01 · Data.Tipo_preset','종류5 정지와 알람 요청 해제의 관찰 근거를 따로 기록합니다.','1847:927과1935:198의 조건을 각각 확인합니다.','현재 호출 순서·외부/다른 쓰기·최종 요청 상태는 확인 전입니다.',['1847:927','1935:198'],[request_jump,reset_jump]),
  bc01_card('timer','기동 감시','Tag_51 · SdCoil · S5T#2S','타이머 비트와 감시 입력의 현재 상태·변화 시각을 기록합니다.','FAULT/INV가 공유하는 원본 감시 경로를 확인하며 FC와 분리합니다.','원문 시간 선언과 실제 경과시간·현재 호출/동작을 구분합니다.',['1785:217','1785:223','1785:27'],alarms_jump[:2]),
  bc01_card('raw','현장 보호·원시/처리 응답','%I0.0 · %I0.1 · %I6.2 / 처리 Inputs','원시 입력과 처리된 운전/이상/트립 신호를 각각 관찰합니다.','SS01 11/12 기동 접점과13/14 감시 접점을 구분해 도면을 확인합니다.','원시→처리 전달·정상 극성·현행 접속과 보호 상태는 확인 전입니다.',['1785:223','1785:27','1786:234'],[circuit_jump(1),circuit_jump(2),circuit_jump(3)])],
 'recovery':[
  bc01_card('cause','원인 입력의 정상화 근거','Inputs.BC01 run · BC01_All_inv · BC01 trip wire','원인 입력과 실물 상태가 어떻게 바뀌었는지 값·시각·근거를 기록합니다.','원시/처리 신호·각 알람의 발생 조건을 대조합니다.','이름만으로 정상 극성을 판단하지 않습니다. 현재 모델의 제조사 기준이 필요합니다.',['1785:223','1785:27','1786:234'],[circuit_jump(1),circuit_jump(2),circuit_jump(3)]),
  bc01_card('latch','알람 기억 해제','Flag.RESET_ALLARM · 알람3개 RCoil','리셋 요청과 각 알람 기억의 해제 시각을 따로 기록합니다.','FAULT/INV의 Reset과 ¬트립 입력을 포함하는 FC Reset을 구분합니다.','래치 해제가 원인 해소·새 요청·실제 복구를 보장하지 않습니다.',['1785:228','1785:267','1786:240'],[dict(t,alarmStep='reset') for t in alarms_jump]),
  bc01_card('new-request','새 요청·출력 허가','Flag.M_BC_01 · OR허가3개 · Start BC01','리셋 이후의 운전 요청·허가·최종 출력을 각각 기록합니다.','Reset 경로와 요청 Set·출력 조건을 별도로 확인합니다.','현재 쓰기 순서·기억 상태·승인된 조작 전달은 확인 전입니다.',['1843:492','1844:1162','1935:202'],[request_jump,output_jump]),
  bc01_card('actual','실제 전달·응답·재발 확인','%Q0.0 / 현장 DI1 / %I0.0 / Inputs.BC01 run','출력·현장 기동·실제 응답·재발과 연동 영향을 각각 기록합니다.','기동 회로·운전 응답 회로와 기존 복구 증거 준비를 비교합니다.','현재 ABB 단자·원시→처리 전달·실제 운전 복구는 확인 전입니다.',['1935:202','1785:223'],[circuit_jump(0),circuit_jump(1),bc01_target('복구 증거 확인','completion','recovery')])]
}
bc01_circuit=next(p for p in drawing_profiles if p['key']=='P01')['circuit']
data['bc01_standard']['inverter_comparison']=[
 dict(aspect='제작사·모델·정격',saved=bc01_circuit['equipment'],current='제작사 ABB: 2026-10-11 사용자 확인. 현재 모델·정격은 확인 전.',needed='현재 장착품 명판·위치·촬영 시점·BC01/M02 동일성 자료.',targets=[bc01_target('실물 확인 준비','completion','field')]),
 dict(aspect='기동 입력·릴레이 전달',saved=bc01_circuit['paths'][0]['destination'],current='현재 ABB의 기동 단자·직렬 허가·릴레이 전달은 확인 전.',needed='현행 승인 접속도·단자/배선 식별·접점/전압 관찰 위치와 근거.',targets=[circuit_jump(0)]),
 dict(aspect='운전 응답',saved=' / '.join(bc01_circuit['paths'][1]['nodes']),current='현재 릴레이 출력 기능·극성·배선·원시→처리 전달은 확인 전.',needed='해당 모델의 출력 기능 정의·현재 접속도·입력/처리 신호의 관찰 자료.',targets=[circuit_jump(1)]),
 dict(aspect='인버터 이상 응답',saved=' / '.join(bc01_circuit['paths'][2]['nodes']),current='현재 ABB 고장 응답 단자·출력 기능·정상 극성은 확인 전.',needed='해당 모델의 고장 출력 정의·현행 배선·I0.1/처리 Inputs 대조 근거.',targets=[circuit_jump(2)]),
 dict(aspect='속도 설정·PLC 아날로그 출력',saved='HMI_DB.SET_PERC_BC01 DB41.DBW52(Int) / Mul 상수272 / 102A5_SPARE0 %QW288(Word). 보존 선언·핀 연결.',current='현재 ABB 입력 단자·설정/단위·PLC 최종값과 실제 속도는 확인 전.',needed='현재 모델/승인 접속·아날로그 입력 기능·HMI 이벤트/PLC 쓰기·관찰 근거. 보호값 변경은 수행하지 않음.',targets=[bc01_target('속도·주소 원본 근거','control','speed')])]

data['bc01_standard']['source_hashes'].update({path:hashlib.sha256((ROOT/path).read_bytes()).hexdigest() for path in sorted(bc01_extra_sources)})
data['bc01_standard']['source_hashes'].update(next(p for p in data['repair_record_forms']['profiles'] if p['key']=='P01').get('additional_signal_sources',{}))
data['bc01_standard']['source_bundle_sha256']=hashlib.sha256(json.dumps(data['bc01_standard']['source_hashes'],sort_keys=True,separators=(',',':')).encode()).hexdigest()
# Capability registration is separate from the preserved BC01 evidence.
data['equipment_standards']=dict(schema_version=1,profiles=[dict(
    priority_key='P01',catalog_id='BC01',source_key='bc01_standard',type='motor_conveyor',
    tools=dict(sources=True,restore=True,compare=True,report=True),
    source_pairs=[
        dict(signal='기동 명령',path='networks/network-1935.html#bc01-part-202',label='직접 출력 참조 · Start BC01',boundary='최종 출력 참조와 도면 경로를 비교합니다. 현재 출력·접속·실물 응답은 확인 전입니다.'),
        dict(signal='운전 응답',path='networks/network-1018.html',label='직접 원시 참조 · BC01_Fbk',boundary='원시 입력과 처리된 Inputs 신호를 구분합니다. 원시→처리 전달·정상 극성·현재 ABB 접속은 확인 전입니다.'),
        dict(signal='인버터 이상',path='networks/network-1785.html#bc01-part-27',label='처리 신호 알람 참고 · 원시 입력 직접 대응 미확정',boundary='원시 입력과 처리된 Inputs 신호를 구분합니다. 원시→처리 전달·정상 극성·현재 ABB 접속은 확인 전입니다.'),
        dict(signal='트립와이어 감시',path='networks/network-1786.html#bc01-part-234',label='처리 신호 알람 참고 · 원시 입력 직접 대응 미확정',boundary='원시 입력과 처리된 Inputs 신호를 구분합니다. 원시→처리 전달·정상 극성·현재 ABB 접속은 확인 전입니다.'),
        dict(signal='회전 감시 예비',path='',label='예비 입력 · 직접 대응 없음',boundary='예비 표기와 직접 대응 없음 상태를 보존합니다.')])])
from equipment_standard_profiles import build_fn04_profile,build_fn01_profile,build_fn02_profile,build_fn03_profile,build_fn06_profile,build_mc04_profile,build_vs01_profile,build_pv01_profile
data['equipment_standards']['profiles'].append(build_fn04_profile(ROOT,data,BC01SourceRows))
data['equipment_standards']['profiles'].append(build_fn01_profile(ROOT,data,BC01SourceRows))
data['equipment_standards']['profiles'].append(build_fn02_profile(ROOT,data,BC01SourceRows))
data['equipment_standards']['profiles'].append(build_fn03_profile(ROOT,data,BC01SourceRows))
data['equipment_standards']['profiles'].append(build_fn06_profile(ROOT,data,BC01SourceRows))
data['equipment_standards']['profiles'].append(build_mc04_profile(ROOT,data,BC01SourceRows))
data['equipment_standards']['profiles'].append(build_vs01_profile(ROOT,data,BC01SourceRows))
data['equipment_standards']['profiles'].append(build_pv01_profile(ROOT,data,BC01SourceRows))
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
<meta name="description" content="GME 디코팅 설비 매뉴얼, 수리 진단과 PLC 정적 분석을 한곳에서 사용하는 통합 프로그램. 시뮬레이터 영구 중지.">
<title>GME 올인원 · 설비 매뉴얼과 PLC 작업실</title>
<link rel="stylesheet" href="assets/all-in-one.css"><link rel="stylesheet" href="assets/bc01-tools.css"></head><body>
<a class="skip" href="#workspace">본문으로 이동</a>
<aside class="sidebar" aria-label="통합 메뉴와 설비 선택">
<a class="brand" href="#overview"><span class="brand-mark">G</span><span>GME <b>ALL-IN-ONE</b><small>설비 매뉴얼 · PLC 작업실</small></span></a>
<nav class="primary-nav" aria-label="프로그램 메뉴">
<button type="button" data-view="overview">통합 현황</button>
<button type="button" data-view="priority">공정 배치도·설비카드</button>
<button type="button" data-view="simulator">시뮬레이터 · 영구 중지</button>
<button type="button" data-view="structure">PLC 호출·신호 구조</button>
<button type="button" data-view="tests">시험·검증</button>
<button type="button" data-view="review">근거 검토·확인</button>
<button type="button" data-view="notes">개선·작업 메모</button>
<button type="button" data-view="resources">전체 자료</button>
<button type="button" data-unified-backup>모든 설비 통합 백업·복원</button>
</nav>
<section class="equipment-picker" aria-labelledby="picker-title">
<div class="picker-heading"><h2 id="picker-title">설비 선택</h2><span id="equipment-count"></span></div>
<div class="scope-switch" role="group" aria-label="설비 목록 범위"><button type="button" data-scope="priority" aria-pressed="true">우선 23</button><button type="button" data-scope="all" aria-pressed="false">전체 248</button></div>
<label class="sr-only" for="equipment-search">설비·주소 검색</label><input id="equipment-search" type="search" placeholder="설비명·태그·I/O 주소 검색" autocomplete="off">
<label class="sr-only" for="equipment-group">설비 영역</label><select id="equipment-group"><option value="">전체 영역</option></select>
<div id="equipment-list" class="equipment-list" aria-label="설비 목록"></div>
</section><p class="sidebar-foot">v__GME_VERSION__ · 매뉴얼·수리·구조 분석<br>시뮬레이터 영구 중지</p></aside>
<div class="app-body"><header class="app-header"><div><span class="eyebrow">매뉴얼 · 수리 · 구조 분석 · 개선</span><strong>하나의 화면, 같은 설비 기준</strong></div><div class="header-status"><span class="dot"></span>매뉴얼 작성 중 <span class="chip">시뮬레이터 영구 중지</span></div></header>
<section class="context" aria-labelledby="context-title"><div><span id="context-kicker" class="eyebrow"></span><h1 id="context-title"></h1><p id="context-meta"></p></div><button type="button" id="context-summary">설비 요약</button></section>
<nav id="device-tabs" class="device-tabs" aria-label="선택 설비 작업"></nav>
<main id="workspace" tabindex="-1"><div id="workspace-content"></div><section id="document-workspace" hidden><div class="document-toolbar"><span id="document-label"></span><div><button type="button" id="document-print">인쇄</button><a id="document-source" href="manual-catalog.html" target="_blank" rel="noopener">자료 따로 열기 ↗</a></div></div><iframe id="document-frame" title="통합 자료 보기"></iframe></section></main>
<footer class="app-footer">원본·정적 해석·실행 결과·현장 확인을 구분하여 관리합니다.<span id="app-message" role="status" aria-live="polite"></span></footer></div>
<noscript><p>통합 탐색에는 JavaScript가 필요합니다. <a href="manual-catalog.html">기존 전체 매뉴얼</a>을 열어 자료를 읽을 수 있습니다.</p></noscript>
<div hidden aria-hidden="true"><span id="overview"></span><span id="purpose"></span><span id="equipment"></span><span id="scope"></span><span id="method"></span><span id="read"></span><span id="workflow"></span><span id="program"></span><span id="conflicts"></span><span id="drawing"></span></div>
<script src="assets/all-in-one-data.js"></script><script src="assets/program-model-data.js"></script><script src="assets/note-record-store.js"></script><script src="assets/repair-records.js"></script><script src="assets/equipment-standard.js"></script><script src="assets/bc01-tools.js"></script><script src="assets/unified-backup.js"></script><script src="assets/all-in-one.js"></script></body></html>
''', encoding='utf-8')

# Refresh the manual UI and register bundle after rebuilds without changing
# the preserved simulator assets or requiring a cache-clearing action.
entry=(ROOT/'index.html').read_text(encoding='utf-8').replace('__GME_VERSION__',release['version'])
for resource in ('assets/all-in-one.js','assets/all-in-one-data.js','assets/all-in-one.css','assets/note-record-store.js','assets/repair-records.js','assets/bc01-tools.js','assets/bc01-tools.css','assets/equipment-standard.js','assets/unified-backup.js'):
    digest=hashlib.sha256((ROOT/resource).read_bytes()).hexdigest()[:12]
    entry=entry.replace('"'+resource+'"','"'+resource+'?v='+digest+'"')
(ROOT/'index.html').write_text(entry,encoding='utf-8')

print(json.dumps(dict(status='built', entry='index.html', equipment=len(specs), priority=len(priority),
                      tests=len(data['tests']), verification=len(data['verification']),
                      bundle_bytes=(ROOT / 'assets/all-in-one-data.js').stat().st_size,
                      simulator_engine_implemented=bool(program)), ensure_ascii=False))
