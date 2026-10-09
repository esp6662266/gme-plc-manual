"""Create reviewable control specifications from preserved evidence registers.

Relationships and static expressions are evidence for review, not executable PLC
semantics. Never promote an unknown call, timer or field value to a verified rule.
"""
from pathlib import Path
import collections, csv, html, json, re, runpy

ROOT = Path(__file__).resolve().parent
DEST = ROOT / 'control-specs'
DEST.mkdir(exist_ok=True)

def readcsv(name):
    return list(csv.DictReader((ROOT / 'registers' / name).open(encoding='utf-8-sig')))

def writecsv(name, headers, rows):
    with (ROOT / 'registers' / name).open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f); w.writerow(headers); w.writerows(rows)

def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def e(value):
    return html.escape(str(value), quote=True)

def tbl(headers, rows, empty='자료에서 직접 식별되지 않음. 확인 항목 참조.'):
    rows = list(rows)
    if not rows:
        return '<p class="muted">' + e(empty) + '</p>'
    return '<div class="table-wrap"><table><thead><tr>' + ''.join('<th>' + e(x) + '</th>' for x in headers) + '</tr></thead><tbody>' + ''.join('<tr>' + ''.join('<td>' + str(x) + '</td>' for x in row) + '</tr>' for row in rows) + '</tbody></table></div>'

def page(title, body, prefix='../', nav=''):
    return '<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>' + e(title) + '</title><link rel="stylesheet" href="' + prefix + 'assets/manual.css"></head><body><header><a href="' + prefix + 'index.html">GME 전체 설비 매뉴얼</a><a href="' + prefix + 'control-spec.html">전체 제어 명세</a><span>2026-10-07 · 원본 기준 검토본</span></header><div class="layout">' + nav + '<main><h1>' + e(title) + '</h1>' + body + '</main></div><footer>매뉴얼·수리·프로그램 구조 파악·개선 검토를 위한 제어 명세</footer></body></html>'

def grouped(rows, key):
    result = collections.defaultdict(list)
    for row in rows:
        result[row[key]].append(row)
    return result

equipment = json.loads((ROOT / 'registers/equipment.json').read_text())
io = grouped(readcsv('equipment-io.csv'), '설비 ID')
hmi = grouped(readcsv('equipment-hmi.csv'), '설비 ID')
links = grouped(readcsv('equipment-networks.csv'), '설비 ID')
checks = grouped(readcsv('verification.csv'), '설비 ID')
tests = grouped(readcsv('simulation-tests.csv'), '설비 ID')
actions = readcsv('lad-conditions.csv')
action_by_net = grouped(actions, '네트워크 문서')
nets = {str(n['document_id']): n for n in json.loads((ROOT / 'sources/decoded-original/network-map.json').read_text())}
conflicts = readcsv('source-conflicts.csv')

CONFLICT_DEVICES = {
    'PV01-LS02': ['PV01', 'LS02'],
    'MC05-SC12-PV04': ['MC05', 'SC12', 'PV04', 'EV07', 'CYL-CL11'],
    'FN01-FAN': ['FN01', 'FN01-FAN'],
    'MV04-MC04': ['MV04', 'MC04'],
    'FN04': ['FN04', 'PC01', 'SYS-PID'],
    'MV06-LS': ['MV06', 'LS34', 'LS35', 'LS40', 'LS41'],
    'CL-NAMESPACE': [d['id'] for d in equipment if d['id'].startswith(('CYL-', 'CLIENT-'))],
    'TC05': ['TC04', 'TC05', 'FN01'],
    'RO03': ['RO03', 'RO02', 'SYS-PID'],
    'BF02-DP': ['BF02', 'DP01', 'DP02', 'SYS-PID'],
    'CLIENT19': ['CLIENT-CL19', 'SYS-ALARM'],
    'BR01': ['BR01', 'AB01', 'FN03', 'SYS-SAFETY'],
    'PID-TM': ['ZT02', 'ZT03', 'ZT04', 'ZT05', 'ZT06', 'MV01', 'MV02', 'MV03', 'MV05', 'MV06'],
}
GLOBAL_CONFLICTS = {'BASELINE', 'POWER', 'VOLTAGE', 'ADDRESS', 'SOURCE-XML'}

def normalize(value):
    return re.sub(r'[\s"\']+', '', value).casefold()

def tag_pattern(tag):
    # Use separators between letters and digits; avoid EV21 matching EV210.
    pieces = re.split(r'([0-9]+)', tag)
    value = '[-_ .]*'.join(re.escape(p) for p in pieces if p)
    return re.compile(r'(?<![a-z0-9])' + value + r'(?![a-z0-9])', re.I)

def target_relation(d, row):
    target = row['대상']
    symbols = [s['원본 심볼'] for s in io[d['id']]]
    if any(normalize(target) == normalize(s) for s in symbols):
        return '관련 심볼 이름과 대상 일치'
    if d['id'].startswith(('CYL-', 'CLIENT-', 'SYS-')):
        return ''
    if tag_pattern(d['id']).search(target):
        return '설비 태그 명칭 일치 후보'
    return ''

OPAQUE = re.compile(r'미해석|미연결|순환 참조|RefId|ORef UID|블록 동작 확인')
TOPICS = {
    'mode': re.compile(r'maintenance|manual|manu|auto', re.I),
    'permit': re.compile(r'enable|abilita|ready|permit|consens|gate.loop|loop.on', re.I),
    'fault': re.compile(r'allarm|alarm|fault|lock.out|overload|trip|emerg', re.I),
    'reset': re.compile(r'reset|rst|init|startup', re.I),
}

specs = []
rule_links = []
for d in equipment:
    id = d['id']
    related = []
    for link in links[id]:
        net_id = link['문서 ID']
        for row in action_by_net[net_id]:
            relation = target_relation(d, row)
            item = dict(row, rule_id=net_id + ':' + row['Part UID'],
                        relation=relation or '관련 네트워크의 공유·연관 동작',
                        direct_target=bool(relation),
                        opaque=bool(OPAQUE.search(row['정적 조건식'] + ' ' + row['내용'])),
                        source_kind='원본 Wire 기반 정적 경로',
                        execution_status='실행·호출 순서 미검증')
            related.append(item)
            rule_links.append([id, item['rule_id'], net_id, row['Part UID'], item['relation'], item['execution_status']])
    related = list({a['rule_id']: a for a in related}.values())
    direct = [a for a in related if a['direct_target']]
    own_net_ids = {l['문서 ID'] for l in links[id] if tag_pattern(id).search(l['제목'])}
    direct_net_ids = {a['네트워크 문서'] for a in direct}
    if d['kind'] == 'pulse':
        scoped = direct
    else:
        scoped = [a for a in related if a['direct_target'] or a['네트워크 문서'] in own_net_ids | direct_net_ids]
    modes = [a['rule_id'] for a in scoped if TOPICS['mode'].search(a['정적 조건식'])]
    permits = [a['rule_id'] for a in scoped if TOPICS['permit'].search(a['정적 조건식'])]
    faults = [a['rule_id'] for a in related if TOPICS['fault'].search(a['대상'] + ' ' + a['정적 조건식'])]
    resets = [a['rule_id'] for a in related if TOPICS['reset'].search(a['대상'] + ' ' + a['정적 조건식'])]
    sequence = [a for a in scoped if re.search(r'\[[^\[\]]*(?:state|step|passo|ev_filter_on)\s*[=!<>]', a['정적 조건식'], re.I)]
    timers = [a for a in scoped if a['동작'] == 'SdCoil' or re.search(r'S5T#|T#', a['정적 조건식'] + a['내용'], re.I)]
    settings = []
    for link in links[id]:
        n = nets[link['문서 ID']]
        for uid, operand in n['resolved_operands'].items():
            name = operand.get('name', '')
            if re.search(r'set[_ .]|\b(?:Data|data_pid)\.|S5T#|T#', name, re.I):
                settings.append(dict(network=link['문서 ID'], operand_uid=uid, name=name,
                                     name_status=operand['status'], runtime_value='미취득·미확정',
                                     relation='관련 네트워크 참조; 장치 전용 여부 확인'))
    missing = ['TIA 호출 조건·주기·중복 쓰기 순서와 전원 재시작 동작 확인',
               '현재 PLC 프로그램·현장 설치·단자·정상 극성 및 실제 설정값 대조',
               '시험 기대 결과 확정과 실행 증거 수집']
    if not io[id]: missing.append('직접 I/O 미식별: 상위 장치·로컬 계측·공통 기능 여부 확인')
    if not hmi[id]: missing.append('직접 HMI 설정 미식별: 표시용 가공 태그·상위 화면 여부 확인')
    if not links[id]: missing.append('직접 LAD 미식별: 실물/예비 상태 또는 상위 제어 연결 확인')
    if not modes: missing.append('자동·수동 모드 전환 및 우선순위 미확정')
    if not timers: missing.append('전용 타이머 또는 무지연 동작 여부 미확정')
    if not sequence: missing.append('상태 전환 순서 또는 단일 동작·수동 장치 여부 미확정')
    if any(a['opaque'] for a in scoped): missing.append('정적 조건에 미해석 참조·호출·타이머 출력 등이 있음')
    relevant_conflicts = [c for c in conflicts if c['ID'] in GLOBAL_CONFLICTS or id in CONFLICT_DEVICES.get(c['ID'], [])]
    spec = dict(id=id, name=d['name'], group=d['group'], kind=d['kind'], parent=d['parent'],
                role=d['role'], installation_status=d['status'],
                evidence_status='자료 연결 완료 · 동작 확정 검토 중',
                inputs=[s for s in io[id] if re.match(r'%i', s['백업 주소'], re.I)],
                outputs=[s for s in io[id] if re.match(r'%q', s['백업 주소'], re.I)],
                internal=[s for s in io[id] if not re.match(r'%[iq]', s['백업 주소'], re.I)],
                hmi=hmi[id], networks=links[id], electrical_fgs=d['fgs'], pid_present=d['pid'],
                direct_rules=direct, scoped_rules=scoped, related_rules=related,
                mode_rule_ids=modes, permit_rule_ids=permits, fault_rule_ids=faults,
                reset_rule_ids=resets, sequence=sequence, timers=timers, settings=settings,
                source_conflicts=relevant_conflicts, pending=missing,
                verification=checks[id], test_designs=tests[id],
                plc_execution_verified=False, field_verified=False, simulator_model_ready=False)
    specs.append(spec)

def netlink(id, prefix='../'):
    return '<a href="' + prefix + 'networks/network-' + e(id) + '.html">#' + e(id) + '</a>'

def rule_table(rows):
    return tbl(['규칙 ID', '블록·원본', '동작·대상', '정적 조건', '인자·해석 범위'],
               ([e(a['rule_id']), e(a['블록']) + '<br>' + netlink(a['네트워크 문서']),
                 e(a['동작']) + '<br><code>' + e(a['대상']) + '</code>',
                 '<code class="condition">' + e(a['정적 조건식']) + '</code>', e(a['내용']) + '<br>' + e(a['relation']) + '<br>' + ('미해석 동작 포함 · ' if a['opaque'] else '') + e(a['execution_status'])] for a in rows))

def signal_table(rows):
    return tbl(['백업 주소', '원본 심볼', '자료형', '원본 설명', '근거 문서'],
               ([e(s['백업 주소'].upper()), e(s['원본 심볼']), e(s['자료형']), e(s['설명']), e(s['문서 ID'])] for s in rows))

for s in specs:
    id = s['id']
    b = '<div class="source"><strong>' + e(s['group']) + ' · ' + e(s['evidence_status']) + '</strong><br>' + e(s['role']) + '</div><p><a href="../devices/' + e(id) + '.html">설비 매뉴얼·수리 진단</a> · <a href="../registers/control-spec.json">전체 구조화 명세 JSON</a></p>'
    b += '<div class="note">원본 조건의 정적 해석을 정리한 검토본이다. PLC 실행 순서·타이머 동작·현재 설정값·현장 일치는 확인 중이다. 관련 네트워크와 신호에는 공유 참조가 포함되며 전용 소유를 뜻하지 않는다.</div>'
    b += '<h2 id="io">1. 입출력과 HMI</h2><h3>물리 입력</h3>' + signal_table(s['inputs']) + '<h3>물리 출력</h3>' + signal_table(s['outputs']) + '<h3>내부 심볼</h3>' + signal_table(s['internal'])
    b += '<h3>HMI 설정</h3>' + tbl(['태그', '설정 주소', 'Access Name', '내부 ID'], ([e(h[k]) for k in ['HMI 태그', '설정 주소', 'Access Name', '내부 ID']] for h in s['hmi']))
    b += '<h2 id="conditions">2. 동작 조건·모드·허가·정지</h2><p>아래는 관련 심볼 또는 설비 명칭과 쓰기 대상이 일치하는 원본 경로다. 자동·수동 또는 허가 관련 이름은 조건식에서 찾아 분류했으며 모드 우선순위와 완전한 인터록은 호출 구조 및 공유 동작과 함께 확인한다.</p>' + rule_table(s['direct_rules'])
    b += '<p class="muted">읽는 방법: AND는 모든 조건, OR는 하나 이상의 조건, NOT는 반전이다. SCoil/RCoil은 Set/Reset, Move는 입력값 전달을 뜻한다. SdCoil과 호출 블록의 실제 시간·실행 동작은 추가 확인한다. 식의 ON은 원본 심볼 이름으로, 무조건 참인 값으로 가정하지 않는다.</p>'
    b += tbl(['조건식 분류', '참조 규칙 ID'], [[e('자동·수동·유지보수 이름 참조'), e(', '.join(s['mode_rule_ids']) or '미식별')], [e('허가·준비 이름 참조'), e(', '.join(s['permit_rule_ids']) or '미식별')]])
    b += '<h2 id="sequence">3. 운전 순서·타이머·설정값</h2><h3>상태·단계 조건</h3><p>조건식의 상태 변수와 Move 입력·Set/Reset 경로를 함께 제공한다. 비교값과 밸브 번호가 같다는 가정은 사용하지 않는다. 각 규칙의 블록·Part UID가 추적 기준이다.</p>' + rule_table(s['sequence'])
    b += '<h3>시간 조건·인자</h3>' + rule_table(s['timers'])
    b += '<details><summary>관련 설정·계수 피연산자 ' + str(len(s['settings'])) + '개</summary><p>관련 네트워크 참조 목록이다. 상수 해석 후보와 실행 시 DB 값은 구분한다.</p>' + tbl(['원본', 'ORef UID', '명칭', '이름 해석 근거', '실행 시 값'], ([netlink(x['network']), e(x['operand_uid']), e(x['name']), e(x['name_status']), '미취득·미확정'] for x in s['settings'])) + '</details>'
    selected = {a['rule_id']: a for a in s['related_rules']}
    b += '<h2 id="fault">4. 이상 처리·알람·리셋·재기동</h2><p>고장·알람·리셋 관련 이름을 참조하는 경로다. 모든 RCoil을 알람 해제로 취급하지 않으며, 정상 극성·발생 지연·래치·리셋 허가와 재기동은 원본 및 현장으로 확정한다.</p><details><summary>고장·알람 참조 ' + str(len(s['fault_rule_ids'])) + '개</summary>' + rule_table(selected[x] for x in s['fault_rule_ids']) + '</details><details><summary>리셋·초기화·Startup 명칭 참조 ' + str(len(s['reset_rule_ids'])) + '개</summary>' + rule_table(selected[x] for x in s['reset_rule_ids']) + '</details>'
    b += '<h2 id="source">5. 도면·래더 근거</h2>'
    if s['pid_present']: b += '<p><a href="../sources/PID_1684n002I.pdf#page=1">P&ID 1684n002 Rev.I / 1페이지</a></p>'
    def pdfpage(fg):
        if str(fg) == '5A': return 6
        if str(fg) == '180A': return 182
        if str(fg) == '180B': return 183
        n = int(fg); return n + (n > 5) + (2 if n > 180 else 0)
    b += '<p>' + ', '.join('<a href="../sources/Electrical_Rev2.pdf#page=' + str(pdfpage(f)) + '">FG ' + e(f) + ' / PDF ' + str(pdfpage(f)) + '</a>' for f in s['electrical_fgs']) + '</p>'
    b += tbl(['블록', '제목', '네트워크', '원본 XML', '식별한 피연산자'], ([e(l['블록']), e(l['제목']), netlink(l['문서 ID']), '<a href="../sources/decoded-original/' + e(l['원본 XML']) + '">' + e(l['원본 XML']) + '</a>', e(l['해석 피연산자'] + '/' + l['전체 피연산자'])] for l in s['networks']))
    b += '<details><summary>공유·연관 동작을 포함한 정적 경로 ' + str(len(s['related_rules'])) + '개</summary>' + rule_table(s['related_rules']) + '</details>'
    b += '<h2 id="pending">6. 미확정 사항과 자료 불일치</h2><ul>' + ''.join('<li>' + e(x) + '</li>' for x in s['pending']) + '</ul>'
    b += tbl(['ID', '불일치·확인 내용', '다음 검증', '상태'], ([e(c['ID']), e(c['자료 내용']), e(c['다음 검증']), '자료 대조됨 · 원인·해소 미확정'] for c in s['source_conflicts']))
    b += '<h2 id="tests">7. 진단·시뮬레이션 검증 항목</h2><p>이 명세는 수리 진단·프로그램 구조 분석·개선안 검토의 공통 기준이다. 각 시험의 기대 결과를 원본 조건과 대조하고 실행 값·시간·버전·증거를 기록한다.</p>'
    b += tbl(['시험 ID', '상황', '주입 조건', '기대 결과 검토안', '상태'], ([e(t[k]) for k in ['시험 ID', '상황', '주입 조건', '확인할 결과', '상태']] for t in s['test_designs']))
    b += tbl(['확인 ID', '항목', '작업', '상태'], ([e(c[k]) for k in ['확인 ID', '항목', '확인 작업', '상태']] for c in s['verification']))
    nav = '<aside class="toc">' + ''.join('<a href="#' + a + '">' + n + '</a>' for a,n in [('io','입출력·HMI'),('conditions','모드·동작 조건'),('sequence','순서·시간·설정'),('fault','이상·리셋'),('source','도면·래더 근거'),('pending','미확정·불일치'),('tests','검증 항목')]) + '</aside>'
    (DEST / (id + '.html')).write_text(page(id + ' · 제어 명세', b, nav=nav))
    device = ROOT / 'devices' / (id + '.html')
    text = device.read_text()
    marker = '<p class="control-spec-link"><a href="../control-specs/' + id + '.html">설비 제어 명세: 입출력·동작 조건·순서·이상 처리·근거</a></p>'
    if 'class="control-spec-link"' not in text:
        text = text.replace('</h1>', '</h1>' + marker, 1)
        device.write_text(text)

def signal_text(rows):
    return '; '.join(s['원본 심볼'] + ' (' + s['백업 주소'].upper() + ')' for s in rows)

def rules_text(rows):
    return '\n'.join(a['rule_id'] + ' ' + a['동작'] + ' ' + a['대상'] + ' <- ' + a['정적 조건식'] + ' / ' + a['내용'] for a in rows)

writecsv('control-spec.csv', ['설비 ID','설비명','영역','상위','자료 상태','입력','출력','내부 심볼','HMI 설정','직접 대상 정적 조건','모드 참조 규칙','허가 참조 규칙','단계 조건·전환','타이머 인자','고장·알람 참조 규칙','리셋·초기화 참조 규칙','도면 FG','원본 네트워크','관련 불일치 ID','미확정 항목','동작 확정 상태'],
         [[s['id'],s['name'],s['group'],s['parent'],s['installation_status'],signal_text(s['inputs']),signal_text(s['outputs']),signal_text(s['internal']),'; '.join(h['HMI 태그']+' ('+h['설정 주소']+')' for h in s['hmi']),rules_text(s['direct_rules']),', '.join(s['mode_rule_ids']),', '.join(s['permit_rule_ids']),rules_text(s['sequence']),rules_text(s['timers']),', '.join(s['fault_rule_ids']),', '.join(s['reset_rule_ids']),', '.join(map(str,s['electrical_fgs'])),', '.join(l['문서 ID'] for l in s['networks']),', '.join(c['ID'] for c in s['source_conflicts']),'; '.join(s['pending']),s['evidence_status']] for s in specs])
writecsv('control-rule-links.csv',['설비 ID','규칙 ID','네트워크 문서','Part UID','연관 근거','실행 확인 상태'],rule_links)
writecsv('source-conflict-review.csv',['ID','항목','자료 내용','관련 범위','근거','다음 검증','문서 검토 상태','해소 상태'],
         [[c['ID'],c['확인 항목'],c['자료 내용'],'전체 공통' if c['ID'] in GLOBAL_CONFLICTS else ', '.join(CONFLICT_DEVICES.get(c['ID'],[])),'sources 원본 PDF·ZAP18·PLF 및 관련 설비 신호·네트워크 대장',c['다음 검증'],'제어 명세에 연결','원인·해소 미확정'] for c in conflicts])
dump(ROOT / 'registers/control-spec.json', dict(schema_version='0.1', created='2026-10-07', purpose='매뉴얼·수리·프로그램 구조 파악·개선 검토 및 후속 HMI 시뮬레이터',
    analysis_scope='original static conditions and related references; no execution or field verification', specifications=specs))

body = '<div class="source">전체 설비의 입출력·동작 조건·운전 순서·이상 처리·근거를 연결했다. 매뉴얼·수리·프로그램 분석·개선 검토와 후속 시뮬레이터의 공통 기준이다.</div><p><a href="registers/control-spec.csv">전체 명세 CSV</a> · <a href="registers/control-spec.json">전체 명세 JSON</a> · <a href="registers/control-rule-links.csv">설비·원본 규칙 연결 대장</a> · <a href="registers/source-conflict-review.csv">18개 불일치 검토 대장</a> · <a href="PROJECT-PURPOSE.md">프로젝트 목적</a></p><div class="note">모든 항목은 동작 확정 검토 중이다. 원본 자료 연결과 실제 PLC 실행·현재 설정·현장 확인을 구분한다. 미해석 참조·공유 신호·미식별 장치를 표시했으며, 시험 실행은 0건이다.</div>'
body += '<div class="controls"><input id="spec-search" aria-label="제어 명세 검색" placeholder="설비 ID, 이름, 영역, 주소 검색"><select id="spec-group" aria-label="제어 명세 영역"><option value="">전체 영역</option>' + ''.join('<option>' + e(g) + '</option>' for g in dict.fromkeys(s['group'] for s in specs)) + '</select></div><p id="spec-count" aria-live="polite">248개 관리 항목</p>'
body += '<div class="table-wrap"><table id="spec-table"><thead><tr>' + ''.join('<th>'+e(t)+'</th>' for t in ['설비','영역','I / Q','HMI','직접 대상 경로','단계 경로','관련 LAD','명세 상태']) + '</tr></thead><tbody>'
for s in specs:
    search = ' '.join([s['id'],s['name'],s['group'],signal_text(s['inputs']+s['outputs'])]).casefold()
    body += '<tr data-search="' + e(search) + '" data-group="' + e(s['group']) + '"><td><a href="control-specs/' + e(s['id']) + '.html"><strong>' + e(s['id']) + '</strong></a><br>' + e(s['name']) + '</td><td>' + e(s['group']) + '</td><td>' + str(len(s['inputs'])) + ' / ' + str(len(s['outputs'])) + '</td><td>' + str(len(s['hmi'])) + '</td><td>' + str(len(s['direct_rules'])) + '</td><td>' + str(len(s['sequence'])) + '</td><td>' + str(len(s['networks'])) + '</td><td>자료 연결 · 동작 검토 중</td></tr>'
body += '</tbody></table></div><script>const q=document.getElementById("spec-search"),g=document.getElementById("spec-group"),rows=[...document.querySelectorAll("#spec-table tbody tr")];function filter(){let n=0;for(const r of rows){const ok=(!q.value.trim()||r.dataset.search.includes(q.value.trim().toLowerCase()))&&(!g.value||r.dataset.group===g.value);r.hidden=!ok;if(ok)n++}document.getElementById("spec-count").textContent=n+" / "+rows.length+"개 항목"}q.addEventListener("input",filter);g.addEventListener("change",filter);filter();</script>'
(ROOT / 'control-spec.html').write_text(page('전체 설비 제어 명세 · 248개 관리 항목', body, prefix=''))
summary = dict(equipment_specs=len(specs), inputs_reference_rows=sum(len(s['inputs']) for s in specs),
    outputs_reference_rows=sum(len(s['outputs']) for s in specs), hmi_reference_rows=sum(len(s['hmi']) for s in specs),
    original_static_rules=len(actions), device_rule_links=len(rule_links),
    specs_with_direct_target_paths=sum(bool(s['direct_rules']) for s in specs),
    specs_with_state_paths=sum(bool(s['sequence']) for s in specs),
    source_conflicts_reviewed=len(conflicts), source_conflicts_resolved=0,
    plc_execution_verified=0, field_verified=0, test_designs=sum(len(s['test_designs']) for s in specs), tests_executed=0)
dump(ROOT / 'registers/control-spec-coverage.json', summary)
print(json.dumps(summary, ensure_ascii=False, indent=2))
if (ROOT / 'build-all-in-one.py').exists():
    if (ROOT / 'build-program-model.py').exists():
        runpy.run_path(str(ROOT / 'build-program-model.py'), run_name='__main__')
    if (ROOT / 'build-detailed-procedures.py').exists():
        runpy.run_path(str(ROOT / 'build-detailed-procedures.py'), run_name='__main__')
    runpy.run_path(str(ROOT / 'build-all-in-one.py'), run_name='__main__')
