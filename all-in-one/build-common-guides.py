"""Create source-linked common-control manuals; never evaluate PLC logic.

The existing model is read only as an index of recovered conditions. Original
XML connections and identifier declarations are copied as documentary evidence.
No simulator model, engine or behavior result is written or executed.
"""
from collections import defaultdict
from pathlib import Path
import csv
import hashlib
import html
import json
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
model = json.loads((ROOT / 'registers/program-model.json').read_text())
signal = json.loads((ROOT / 'registers/signal-trace.json').read_text())
app = json.loads((ROOT / 'registers/all-in-one-data.json').read_text())
nets = {n['id']: n for n in model['networks']}
selected = [402, 403, 404, 405, 930, 931, 1613, 1619, 1620, 1621, 1622,
            1723, 1824, 1841, 1842, 1843, 1844, 1845, 1846, 1847, 1848,
            1856, 1857, 1858, 1865, 1866, 1868, 1935, 1948, 1951, 1955]
SEQUENCES = {1843: (1, '예열 요청'), 1844: (2, '생산 요청'),
             1847: (5, '전체 정지 요청'), 1848: (6, 'no sequence')}
COMMON = ['ON', 'OFF', 'Flag.Auto_ON1', 'Data.Tipo_preset',
          'Data.Tempo_presetting', 'Data.D37', 'Flag.Maintenance_ON',
          'Inputs.EM_OK', 'Allarm.Emergency_module_fault',
          'Inputs.Reset_allarmi', 'Flag.Reset_Allarms_HMI',
          'Flag.RESET_ALLARM', 'Flag.STOP_HORN', 'Tag_160',
          '103A7', 'Reset_Inverter', 'Lock Burner',
          'Enable start burner', 'Enable start burner(1)']
DEVICE_SIGNALS = {
    'BC01': ['Flag.M_BC_01', 'MemoCMD_BC01_Startup', 'Flag.R1_GATE_LOOP_ON', 'Start BC01'],
    'FN04': ['Flag.M_FN_04', 'Flag.FN_04_AUTO', 'Data.SET_PERC_FN04', 'Inputs.FN04 Run', 'Start FN04'],
    'PV01': ['Flag.Enable_R1_GATE', 'MemoCMD_PV1_Startup', 'Flag.PV_01_GATE_A_MEM_CLOSE', 'Flag.PV_01_GATE_B_MEM_CLOSE'],
    'RD01': ['Flag.M_RD_01', 'Flag.M_RD_01_FAN', 'Inputs.RD01 run', 'Start RD01'],
    'PV02': ['Flag.Enable_R2_GATE', 'Flag.PV_02_GATE_A_MEM_CLOSE', 'Flag.PV_02_GATE_B_MEM_CLOSE'],
    'MC04': ['Flag.M_MC_04', 'Start MC04', 'Allarm.Maintenance_ON'],
    'VS01': ['Flag.M_VS_01', 'Start VS01'],
    'BR01': ['Flag.Start_Burner', 'Flag.AUTO_BURNER', 'Flag.Burner_ready', 'Lock Burner',
             'Enable start burner', 'Enable start burner(1)', 'Rem. Start/Stop Burner'],
    'FN01': ['Flag.M_FN_01', 'Flag.M_FN_01_FAN', 'Data.SET_PERC_VT01', 'Start FN01'],
    'FN02': ['Flag.M_FN_02', 'Data.Set_Perc_VT02', 'Start FN02'],
    'FN03': ['Flag.M_FN_03', 'Start FN03'],
    'FN06': ['Flag.M_FN_06', 'Start FN06', 'Allarm.MBVA01_FAULT'],
    'MV01': ['Flag.MV01_Auto'],
    'MV03': ['Flag.MV03_Auto', 'Close MV03 for Burner Startup', 'Open MV03 for washing'],
    'MV06': ['Flag.MV06_Auto'],
}
CHECKS = [
    ('COM-01', 'ON·OFF 값과 초기화', [1619, 1620, 1621, 1723],
     'ON=%M0.0·OFF=%M0.1의 현재값, 초기화·외부 쓰기·호출 조건을 확인한다. 이름만으로 상수 True/False로 치환하지 않는다.'),
    ('COM-02', '주기와 카운터 시간', [1723, 1841],
     'cyc_int2 ogni 1s의 실제 OB 설정·호출 간격과 카운터 증가를 대조한다. 단계 값을 초로 확정하기 전 시간 근거를 기록한다.'),
    ('COM-03', '예열·생산 요청의 시작 주체', [1842, 1843, 1844, 1846],
     'Data.Tipo_preset=1/2와 Flag.Auto_ON1의 HMI·외부·다른 언어 블록 쓰기를 찾는다. 복원 LAD의 직접 쓰기만으로 전체 요청 경로를 확정하지 않는다.'),
    ('COM-04', '카운터 초기화 미해석', [1841],
     'NOT 접점 Part92의 ORef74 이름과 호출을 TIA에서 확인한다. RefId4가 다른 피연산자와 같지만 해당 UID의 이름은 미복원 상태로 유지한다.'),
    ('COM-05', '리셋 타이머·출력', [930, 931],
     'TOF 두 인스턴스·PT=T#3s·Q→Q7.4/Q7.5 경로와 SD Tag_160의 S5T#1S를 현재 프로그램·출력 회로에서 대조한다. 알람 해제·인버터 출력·경음기 정지를 구분한다.'),
    ('COM-06', '비상 모듈 알람의 Set/Reset', [1824, 1846, 1847],
     'Inputs.EM_OK 불량과 RESET_ALLARM이 겹칠 때 같은 알람의 Set·Reset 및 이후 쓰기를 확인한다. 리셋만으로 원인 제거·하드웨어 복구 완료로 판단하지 않는다.'),
    ('COM-07', '기동 초기화와 기억 상태', [402, 403, 404, 405],
     'startup only의 실제 OB 조건·미해석 Move 대상 범위·DB 유지 설정·게이트 닫힘 메모를 대조한다. 닫힘 메모는 실제 센서 응답과 별도로 기록한다.'),
    ('COM-08', 'BC01 요청과 출력 허가', [1843, 1844, 1847, 1935],
     'Flag.M_BC_01, R1_GATE_LOOP_ON, MemoCMD_BC01_Startup, Maintenance_ON, Start BC01 및 피드백을 함께 기록한다. 자동 요청 Set만으로 실제 운전을 판단하지 않는다.'),
    ('COM-09', '버너 허가의 서로 다른 주소', [1857, 1858, 1866, 1868],
     'Enable start burner=%M48.2와 Enable start burner(1)=%M48.0을 구분한다. FN03 응답·세정 단계·Lock Burner·외부 버너 제어기의 허가를 대조한다.'),
    ('COM-10', 'OFF 분기의 활성 여부·재기동', [1843, 1844, 1865, 1866],
     '추가 OFF 접점이 있는 FN02 해제·온도 설정·MC05·FN03 요청 분기를 현재값·호출·다른 쓰기와 대조한다. 삭제하거나 조건을 활성화하기 전 의도를 확인한다.'),
]

local = lambda x: x.tag.rsplit('}', 1)[-1]
canonical = lambda value: str(value).replace('"', '').casefold()
e = lambda value: html.escape(str(value))


def walk(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def expression(value):
    op = value['op']
    if op == 'const':
        return str(value.get('literal', '1' if value['value'] is True else '0' if value['value'] is False else value['value']))
    if op == 'read':
        return value['name']
    if op == 'unknown':
        return '[미확정: ' + value['reason'] + ']'
    if op == 'not':
        return 'NOT (' + expression(value['arg']) + ')'
    if op in ('and', 'or'):
        terms = [expression(x) for x in value['args']
                 if not (op == 'and' and x.get('op') == 'const' and x.get('value') is True)]
        return '(' + (' AND ' if op == 'and' else ' OR ').join(terms) + ')' if len(terms) > 1 else terms[0] if terms else '1'
    return '(' + expression(value['left']) + ' ' + {'eq': '=', 'ne': '<>', 'gt': '>', 'ge': '>=', 'lt': '<', 'le': '<='}.get(op, op) + ' ' + expression(value['right']) + ')'


trees = {id: ET.parse(ROOT / nets[id]['file']).getroot() for id in selected}


def connections(id, uid):
    """Document every wire attached to a Part/LRef; no runtime interpretation."""
    rows = []
    for wire in trees[id].iter():
        if local(wire) != 'Wire':
            continue
        if any(local(p) == 'PCon' and p.get('UId') == uid for p in wire):
            ends = [dict(kind=local(p), uid=p.get('UId'), pin=p.get('PinName'),
                         name=nets[id]['refs'].get(p.get('UId'), {}).get('name')) for p in wire]
            rows.append(dict(wire=wire.get('UId'), endpoints=ends))
    return rows


stages = []
for id, (kind, title) in SEQUENCES.items():
    for action in nets[id]['actions']:
        compares = [v for v in walk(action['condition']) if v.get('op') == 'eq'
                    and v.get('left', {}).get('name') == 'Data.Tempo_presetting'
                    and v.get('right', {}).get('op') == 'const']
        values = sorted({v['right']['value'] for v in compares})
        stages.append(dict(network=id, type_value=kind, title=title, part=action['uid'],
                           gate=action['gate'], target=action['name'], counter_values=values,
                           additional_off=any(v.get('op') == 'read' and canonical(v['name']) == 'off' for v in walk(action['condition'])),
                           condition=action['condition'], value=action.get('value'),
                           has_unknown=any(v.get('op') == 'unknown' for v in walk(action['condition'])),
                           source=nets[id]['file'], connections=connections(id, action['uid'])))

symbols = list(csv.DictReader((ROOT / 'registers/plc-symbols.csv').open(encoding='utf-8-sig')))
global_signals = []
for name in COMMON:
    uses = [r for r in signal['usages'] if canonical(r['name']) == canonical(name)]
    global_signals.append(dict(name=name,
                              addresses=[s['백업 주소'].upper() for s in symbols if canonical(s['원본 심볼']) == canonical(name)],
                              usages=uses, writers=[r for r in uses if r['scope'] == 'Global' and r['role'] == 'write']))

raw_paths = [dict(network=id, uid=uid, note=note, connections=connections(id, uid)) for id, uid, note in [
    (1841, '59', 'Add Int: in1=Data.Tempo_presetting, in2=1, out=같은 이름의 카운터. en은 ON·Auto_ON1 접점에서 연결.'),
    (1841, '66', 'Move 0→Data.Tempo_presetting. en은 ON 뒤의 NOT 접점 Part92·ORef74(미해석)에서 연결.'),
    (1846, '21', 'PContact operand=Allarm.Emergency_module_fault, bit=Tag_292. 출력은 두 Move와 Set 코일 경로로 연결. 실제 펄스·ENO·호출 주기는 확인 전.'),
    (930, '64', 'TOF · IEC_Timer_0_DB · PT=T#3s · Q→Coil48→103A7(%Q7.4).'),
    (930, '73', 'TOF · IEC_Timer_1_DB · PT=T#3s · Q→Coil60→Reset_Inverter(%Q7.5).'),
    (931, '229', 'SdCoil Tag_160 · value=S5T#1S. 이후 접점 Part263을 통해 리셋·정음·점멸 기억을 Reset.'),
]]

source_paths = {nets[id]['file'] for id in selected} | {
    'sources/decoded-original/0568-IdentXmlPart.xml',
    'sources/decoded-original/0569-IdentXmlPart.xml',
    'sources/decoded-original/0566-IdentXmlPart.xml'}
source_hashes = {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in sorted(source_paths)}
calls = [c for c in model['calls'] if c['network'] in selected]
profiles = []
for p in app['priority']:
    names = DEVICE_SIGNALS.get(p['plc_id'], [])
    normalized_names = {canonical(name) for name in names}
    profiles.append(dict(key=p['key'], name=p['name'], plc_id=p['plc_id'], match=p['match'],
                         note=p['note'], signals=names,
                         stage_locations=[dict(network=a['network'], part=a['part']) for a in stages if canonical(a['target']) in normalized_names],
                         field_verified=False))
record = dict(date='2026-10-07', scope='static source manual; no PLC evaluation or simulator authoring',
              networks=selected, sources=source_hashes, stages=stages, signals=global_signals,
              raw_paths=raw_paths, calls=calls, priority_profiles=profiles,
              checks=[dict(id=id, title=title, networks=ids, work=work, status='확인 대기') for id, title, ids, work in CHECKS],
              simulator_development='stopped_by_user', simulator_behavior_tests='not_rerun',
              plc_changes=0, field_verified=0)
(ROOT / 'registers/common-control.json').write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
with (ROOT / 'registers/common-control-stages.csv').open('w', encoding='utf-8-sig', newline='') as stream:
    writer = csv.DictWriter(stream, fieldnames=['network', 'type_value', 'part', 'gate', 'target', 'counter_values', 'additional_off', 'condition', 'value'])
    writer.writeheader()
    for row in stages:
        writer.writerow({key: (expression(row[key]) if row[key] is not None else '') if key in ('condition', 'value') else row[key]
                         for key in writer.fieldnames})


def link(path, label, prefix=''):
    return '<a href="' + e(prefix + path) + '">' + e(label) + '</a>'


def source_link(id, prefix=''):
    return link('networks/network-' + str(id) + '.html', '원본 ' + str(id), prefix)


def table(headers, rows):
    return '<div class="table-wrap"><table><thead><tr>' + ''.join('<th>' + e(x) + '</th>' for x in headers) + '</tr></thead><tbody>' + ''.join('<tr>' + ''.join('<td>' + x + '</td>' for x in row) + '</tr>' for row in rows) + '</tbody></table></div>'


def page(title, body, prefix=''):
    styles = '<style>.common-control td code{white-space:normal;overflow-wrap:anywhere}.common-control td:last-child{min-width:140px}.common-control td:last-child a{display:inline-block;white-space:nowrap}.common-control th:nth-child(2),.common-control td:nth-child(2){min-width:160px}</style>'
    return '<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>' + e(title) + '</title><link rel="stylesheet" href="' + prefix + 'assets/all-in-one.css">' + styles + '</head><body class="common-control"><main style="max-width:1240px;margin:auto;padding:24px"><h1>' + e(title) + '</h1>' + body + '</main></body></html>'


def stage_table(rows, prefix=''):
    return table(['종류·카운터', '요청·메모·설정 쓰기', '전체 정적 조건', '원본 위치'], [
        [e(str(a['type_value']) + ' / ' + (','.join(map(str, a['counter_values'])) or '카운터 비교 없음')),
         e(a['gate'] + ' → ' + a['target']) + ('<br>값: <code>' + e(expression(a['value'])) + '</code>' if a['value'] else '') + ('<br><strong>추가 OFF 접점</strong>' if a['additional_off'] else ''),
         '<code>' + e(expression(a['condition'])) + '</code>', source_link(a['network'], prefix) + ' · Part ' + e(a['part'])] for a in rows])


intro = '<div class="notice info">원본 래더의 공통 허가·자동 요청·알람·리셋을 설명하는 정적 매뉴얼입니다. Set/Reset 요청, 실제 출력, 입력 응답, 안전 회로를 구분합니다. 현재 PLC 실행·현재값·TIA 검증·실물 동일성은 확인 전입니다. 시뮬레이터 작성·시험은 중지 상태입니다.</div>'
body = intro + '<nav class="inline-actions">' + ''.join(link('common-control.html#' + anchor, label) for anchor, label in [('calls', '호출·공통 허가'), ('signals', '공통 신호'), ('sequences', '자동 요청 순서'), ('reset', '알람·리셋'), ('restart', '기동·재시작'), ('priority', '우선23 작업지'), ('checks', '확인 대기')]) + '</nav>'
body += '<h2 id="calls">1. 호출 경계와 ON·OFF</h2><p>ON=%M0.0·OFF=%M0.1은 백업의 Bool 심볼입니다. 이름만으로 상수로 확정하지 않습니다. 복원한 직접 핀 쓰기는 찾지 못했으므로 초기값·외부 쓰기·미복원 코드와 현재값을 확인합니다. main의 여러 블록은 ON 접점을 통해 호출됩니다. 1723의 Auto start motors는 cyc_int2 ogni 1s에서 ON을 읽습니다. 블록 이름은 실제 OB 주기 설정의 증거가 아닙니다.</p>'
body += table(['호출 주체 → 대상', '원본 호출·UID', '정적 허가'], [[e(c['caller'] + ' → ' + str(c['callee'])), source_link(c['network']) + ' · CRef ' + e(c['uid']), '<code>' + e(expression(c['enable'])) + '</code>'] for c in calls])
body += '<p>HMI 경로의 ENO는 미해석으로 유지합니다. 백업의 기존 Simulation 블록 호출 조건에 관한 설명은 원본 신호 분석 목록에 있으며 새 모델·시뮬레이터를 작성하지 않습니다.</p>' + link('signal-trace.html', '원본 신호 분석 목록')
body += '<h2 id="signals">2. 공통 신호와 쓰기 주체</h2><p>같은 Global 이름의 직접 쓰기를 집계합니다. 0곳은 미사용·외부 쓰기 없음의 증거가 아닙니다. 초기화·HMI 통신·간접 접근·호출 인터페이스를 추가 확인합니다.</p>'
body += table(['신호·백업 주소', '직접 Global 쓰기', '원본 위치'], [[e(s['name']) + '<br>' + e(' / '.join(s['addresses']) or 'DB/주소 확인'), e(len(s['writers'])), '<details><summary>쓰기 위치</summary>' + ''.join('<p>' + source_link(w['network']) + ' · Part ' + e(w['part']) + '.' + e(w['pin']) + ' · ' + e(w['gate']) + ' · Wire ' + e(w['wire']) + '</p>' for w in s['writers']) + '</details>'] for s in global_signals])
body += '<h2 id="sequences">3. 자동 요청·정지 순서</h2><p>종류는 Data.Tipo_preset, 단계는 Data.Tempo_presetting의 비교값입니다. 아래 값은 카운터 값이며 실제 초 단위는 OB 주기·호출·초기화 확인 후 판단합니다. SCoil은 요청/메모를 Set하고 RCoil은 Reset하며 실제 Q·모터 응답을 의미하지 않습니다. 예열·생산에는 ON, NOT Emergency_module_fault, Auto_ON1 조건이 있습니다. 정지 종류5에는 비상 알람의 OR 경로가 있습니다. 전체 조건을 각 행에서 확인합니다.</p>'
for id, (kind, title) in SEQUENCES.items():
    body += '<h3 id="sequence-' + str(kind) + '">' + e(str(kind) + ' · ' + title) + '</h3>' + stage_table([a for a in stages if a['network'] == id])
body += '<h3 id="native-paths">카운터·펄스·타이머의 원본 배선</h3><p>보존된 조건 색인이 해석하지 못한 명령은 동작을 추정하지 않고 원본 핀·Wire를 표시합니다. 1841의 Add는 Int 입력과 +1 출력 연결이 확인되며 카운터 초기화 ORef74의 이름은 미해석입니다.</p>'
for path in raw_paths:
    body += '<details><summary>' + e(str(path['network']) + ' · ' + path['note']) + '</summary><p>' + source_link(path['network']) + ' · Part/LRef ' + e(path['uid']) + '</p>' + table(['Wire', '원본 끝점'], [[e(w['wire']), '<br>'.join(e(x['kind'] + ' ' + str(x['uid'] or '') + '.' + str(x['pin'] or '') + (' = ' + str(x['name']) if x['kind'] == 'OCon' else '')) for x in w['endpoints'])] for w in path['connections']]) + '</details>'
body += '<h2 id="reset">4. 알람 리셋·비상 정지·버너 허가</h2><p>930은 Inputs.Reset_allarmi 또는 Flag.Reset_Allarms_HMI로 RESET_ALLARM을 Set하고 HMI 요청을 Reset합니다. 같은 분기는 두 TOF의 IN에 연결됩니다. 원본 식별 파일0568은 LRef64/73=TOF,0569는 인스턴스 IEC_Timer_0_DB/1_DB를 확인하며 PT는 T#3s입니다. Q는 각각103A7(%Q7.4), Reset_Inverter(%Q7.5)에 연결됩니다. 931은 RESET_ALLARM 또는 STOP_HORN으로 SD Tag_160(S5T#1S)을 구동한 뒤 관련 기억을 Reset합니다. 지속 시간은 현재 호출·입력 유지·타이머 상태·다른 쓰기를 함께 확인합니다.</p>'
body += '<p>1824는 NOT Inputs.EM_OK로 Emergency_module_fault를 Set합니다. 같은 알람의 Reset 조건은 RESET_ALLARM AND Emergency_module_fault이며 EM_OK 정상 접점이 별도로 포함되지 않습니다. 불량 입력과 리셋이 겹칠 때 Set/Reset의 실제 순서와 이후 재설정을 확인합니다. 1846의 PContact·Tag_292 경로는 카운터0·종류5·Auto_ON1 Set에 연결되고 1847의 종류5 정지에 연결됩니다. 이 자료는 하드웨어 안전 회로의 동작 검증 결과가 아닙니다.</p>'
body += '<p>버너 준비1857은 FN01·FN04·RD01·FN02 응답과 FN06 응답 또는 Burner On, 관련 알람 상태를 읽습니다. 정지1858은 준비 상실과 온도·연소·흡인·압력·수소함 등 알람으로 Start_Burner 요청을 Reset합니다. 1866은 FN03 응답과 Lock Burner를 확인합니다. Enable start burner(1)=%M48.0과 Enable start burner=%M48.2는 서로 다른 심볼·주소입니다. 후자는1868의 세정 단계에서 쓰며 둘을 합치지 않습니다. 전용 버너010-390의 내부 안전 시퀀스는 확보 전입니다.</p>'
alarm_ids = [930, 931, 1824, 1846, 1857, 1858, 1866]
alarm_rows = [(id, a) for id in alarm_ids for a in nets[id]['actions']]
body += '<p>930의 Coil48/60에서 보존된 조건 색인이 “연결된 입력이 없음”으로 표시한 것은 호출 출력의 미해석 상태입니다. 원본 XML에는 TOF.Q→코일 입력 연결(Wire67/77)이 있습니다. 이 문구를 현장 배선 단선으로 해석하지 않습니다.</p>'
body += table(['신호·명령', '보존된 정적 조건·미해석', '근거'], [[e(a['gate'] + ' → ' + a['name']), '<code>' + e(expression(a['condition'])) + '</code>', source_link(id) + ' · Part ' + e(a['uid'])] for id, a in alarm_rows])
body += '<h2 id="restart">5. 기동·재시작과 기억 상태</h2><p>startup only의404는 MV01~06 Auto와 FN04 Auto를 Set하고405는 PV01·02 양쪽 Gate와 PV03 닫힘 메모를 Set합니다. 이것은 물리 닫힘 센서의 확인과 다릅니다. 402·403의 초기화 Move에는 이름을 복원하지 못한 입력·대상이 있으므로 “모든 Flag가0으로 초기화된다”고 확정하지 않습니다. 실제 Startup OB 연결·DB 유지·전원 재시작·HMI 상태를 대조합니다.</p>'
body += table(['초기화 원본', '확인 범위'], [[source_link(id), e(nets[id]['title']) + ' · ' + link(nets[id]['file'], '원본 XML')] for id in [402, 403, 404, 405]])
body += '<h2 id="priority">6. 디코팅 우선23개의 공통 제어 확인 작업지</h2><p>태그 일치·역할 후보·미확정을 구분합니다. 설비 본체와 구동부·냉각팬·전용 제어기를 같은 장치로 합치지 않습니다. PLC 대응 미확정5개에는 태그·자동 단계를 새로 부여하지 않습니다.</p>'
body += table(['우선 설비', 'PLC 자료 대응', '공통 제어 작업지'], [[e(p['key'] + ' · ' + p['name']), e((p['plc_id'] or '미확정') + ' / ' + {'tag':'태그명 일치·실물 확인 전','candidate':'역할 대응 후보','unknown':'대응 미확정'}[p['match']]), link('common-guides/' + p['key'] + '.html', '요청·허가·정지·재기동 확인')] for p in profiles])
body += '<h2 id="checks">7. TIA·현장 확인 대기10건</h2><p>이 목록은 원본 확인 대장1,060건과 불일치18건을 변경하지 않는 공통 제어 보완 목록입니다. 모두 확인 대기이며 원인 해소·시험 합격·현장 수리 완료는0건입니다.</p>'
body += table(['ID·항목', '확인할 작업', '원본·상태'], [[e(id + ' · ' + title), e(work), ' · '.join(source_link(n) for n in ids) + '<br>확인 대기'] for id, title, ids, work in CHECKS])
body += '<h2>자료와 기록</h2><p>' + link('registers/common-control.json', '정적 근거 JSON') + ' · ' + link('registers/common-control-stages.csv', '자동 요청 단계 CSV') + ' · ' + link('ACTIVE-WORK.md', '현재 작업 범위') + '</p>'
(ROOT / 'common-control.html').write_text(page('공통 운전 허가·자동 요청·알람·리셋 매뉴얼', body))

out = ROOT / 'common-guides'
out.mkdir(exist_ok=True)
for profile in profiles:
    key = profile['key']
    status = {'tag': '태그명 일치 · 실물 동일성 확인 전', 'candidate': '역할 대응 후보 · 본체/제어 경계 확인 전', 'unknown': 'PLC 대응 미확정'}[profile['match']]
    content = intro + '<div class="notice">' + e(status + ' · ' + profile['note']) + '</div><nav class="inline-actions">' + link('common-control.html', '공통 제어 전체 매뉴얼', '../') + link('priority-guides/' + key + '.html', '실물 대응·점검 작업지', '../') + '</nav>'
    if profile['plc_id']:
        for directory, label in [('procedures', '진단·수리'), ('signal-guides', '신호 전달·복수 쓰기'), ('circuit-guides', '전기 회로'), ('construction-guides', '시공 케이블')]:
            path = directory + '/' + profile['plc_id'] + '.html'
            if (ROOT / path).exists():
                content += '<p>' + link(path, label, '../') + '</p>'
    if not profile['signals']:
        content += '<h2>제어 범위 식별</h2><p>이 설비 본체의 직접 요청·출력 또는 PLC 대응을 확정하지 않았습니다. 명판·반 명칭·전용 제어기·P&ID 경계를 확인한 뒤 신호를 연결합니다. 공통 제어 매뉴얼의 팬·버너·드럼 신호를 이 본체의 직접 제어 태그로 채택하지 않습니다.</p>'
    else:
        content += '<h2 id="signals">1. 요청·메모·설정과 실제 응답</h2><p>아래 이름은 참고 PLC 자료의 원본 신호입니다. 동명 Local 변수를 합치지 않으며 설치·현재 주소·정상 극성은 추가 확인합니다. 드럼·주 팬과 냉각팬의 요청은 서로 다른 신호입니다.</p>'
        content += table(['관련 신호', '직접 Global 쓰기 위치'], [[e(name), '<br>'.join(source_link(r['network'], '../') + ' · Part ' + e(r['part']) + '.' + e(r['pin']) for r in signal['usages'] if canonical(r['name']) == canonical(name) and r['scope'] == 'Global' and r['role'] == 'write') or '복원 원본의 직접 쓰기 미식별 · 외부/간접 경로 확인'] for name in profile['signals']])
        own = {(a['network'], a['part']) for a in profile['stage_locations']}
        content += '<h2 id="sequences">2. 공통 자동 요청·정지의 관련 쓰기</h2><p>단계는 카운터 비교값이며 초 단위 확정 전입니다. 요청 Set/Reset과 실제 출력·피드백을 함께 확인합니다. 추가 OFF 접점은 현재값·의도 확인 전입니다.</p>' + stage_table([a for a in stages if (a['network'], a['part']) in own], '../')
        if not own:
            content += '<p>이 선택 신호의 예열·생산·정지 단계 쓰기는 미식별입니다. 초기화·PID·버너 세정·다른 요청 경로를 확인하며 임의로 단계를 추가하지 않습니다.</p>'
    content += '<h2 id="repair">수리 판단과 복구 기록 순서</h2><p>별도 제어 설비는 해당 제어기의 상태·신호 기록을 사용합니다. 아래 GME 공통 신호는 해당 설비와의 연동이 확인된 경우에만 함께 기록합니다.</p><ol><li>증상 시각·공정 종류·Auto_ON1·카운터·현재 모드와 최초 알람을 기록합니다.</li><li>원시 입력·처리된 Inputs·운전 요청·허가·실제 출력·물리 응답을 따로 기록합니다.</li><li>공통 정지의 영향인지 해당 장치의 전기·기계 고장인지 출력 전달 경로와 비교합니다.</li><li>리셋 출력과 요청 해제·원인 제거를 구분하고 재기동 조건·후속 설비 영향을 확인합니다.</li><li>관찰 결과·FG/단자·네트워크·작업 내용을 올인원 개선·작업 메모에 기록합니다. 근거 확인 전 완료 판정을 하지 않습니다.</li></ol><p>' + link('common-control.html#checks', '공통 확인 대기10건', '../') + ' · ' + link('ACTIVE-WORK.md', '시뮬레이터 중지와 현재 작업 범위', '../') + '</p>'
    (out / (key + '.html')).write_text(page(key + ' · ' + profile['name'] + ' 공통 제어·복구 확인', content, '../'))
print(json.dumps(dict(common_source_networks=len(selected), documented_stage_writes=len(stages), priority_guides=len(profiles), pending_common_checks=len(CHECKS), simulator_behavior_tests='not_rerun'), ensure_ascii=False))
