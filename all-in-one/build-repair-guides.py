"""Join static equipment conditions, common effects and circuit evidence for repairs.

This produces manuals and blank observation templates, never evaluates PLC logic.
The frozen program model is a source index, not a live controller.
"""
from pathlib import Path
import csv, hashlib, html, json

ROOT = Path(__file__).resolve().parent
model = json.loads((ROOT / 'registers/program-model.json').read_text())
nets = {n['id']: n for n in model['networks']}
common = json.loads((ROOT / 'registers/common-control.json').read_text())
signal = json.loads((ROOT / 'registers/signal-trace.json').read_text())
electrical = json.loads((ROOT / 'registers/electrical-trace.json').read_text())
circuits = {d['id']: d for d in electrical['devices']}
app = json.loads((ROOT / 'registers/all-in-one-data.json').read_text())
symbols = list(csv.DictReader((ROOT / 'registers/plc-symbols.csv').open(encoding='utf-8-sig')))
out = ROOT / 'repair-guides'
out.mkdir(exist_ok=True)
e = lambda v: html.escape(str(v))
canon = lambda s: str(s).replace('"', '').casefold()

# Explicitly reviewed boundaries. No device-name similarity or fuzzy tag allocation.
# A request is not a Q output; processed Inputs and memories are not raw sensors.
DEVICES = {
    'BC01': dict(control=[1935], monitor=[1785, 1786],
        requests=['Flag.M_BC_01'], outputs=['Start BC01'],
        responses=['Inputs.BC01 run', 'Inputs.BC01_All_inv'],
        note='자동 단계의 요청 Set 이후에도 R1_GATE_LOOP_ON·MemoCMD_BC01_Startup·Flag.Maintenance_ON의 OR 허가를 확인합니다. 트립와이어와 근접센서는 다른 입력입니다.'),
    'FN04': dict(control=[1965], monitor=[1809, 1964],
        requests=['Flag.M_FN_04'], outputs=['Start FN04'],
        responses=['Inputs.FN04 Run', 'Inputs.FN04_All_inv'],
        note='설정0 요청 해제와1689의5~100 제한 쓰기를 함께 추적합니다. 17초 기동 감시와90분 연관 설비 감시는 구분하며, 공동 인버터의 두 모터도 별도로 확인합니다.'),
    'RD01': dict(control=[1936], monitor=[1787, 1931],
        requests=['Flag.M_RD_01'], outputs=['Start RD01'],
        responses=['Inputs.RD01 run', 'Inputs.RD01_All_inv', 'Inputs.fan RD01 run'],
        note='킬른 본체·드럼 구동·드럼 냉각팬·투입 허가는 서로 다른 경계입니다. 드럼 응답만으로 투입 허가나 본체 정상 상태를 확정하지 않습니다.'),
    'MC04': dict(control=[1941], monitor=[1791],
        requests=['Flag.M_MC_04'], outputs=['Start MC04'],
        responses=['Inputs.MC04 run', 'Inputs.MC04_All_inv', 'Inputs.VS01 run'],
        note='VS01 미운전과 Allarm.Maintenance_ON의 조합이 요청 해제에 연결됩니다. Flag.Maintenance_ON과 같은 신호로 치환하지 않습니다.'),
    'VS01': dict(control=[1943], monitor=[1794, 1944],
        requests=['Flag.M_VS_01'], outputs=['Start VS01'],
        responses=['Inputs.VS01 run', 'Inputs.VS01_All_Inv'],
        note='공동 인버터·두 진동 모터·브레이크 경로를 구분합니다. 1944의OFF 접점과 brake(off) 제목은 현재 활성 여부 확인 대상입니다.'),
    'FN01': dict(control=[1951], monitor=[1798, 1950],
        requests=['Flag.M_FN_01'], outputs=['Start FN01'],
        responses=['Inputs.FN01 Run', 'Inputs.FN01_All_Inv'],
        note='2초 기동 감시와90분 지연 정지·가스 박스·보조 냉각팬의 조건을 구분합니다. 시간값은 원본 설정이며 현장 동작 확인 결과가 아닙니다.'),
    'FN02': dict(control=[1948], monitor=[1796],
        requests=['Flag.M_FN_02'], outputs=['Start FN02'],
        responses=['Inputs.FN02 Run', 'Inputs.FN02_All_Inv'],
        note='Data.Set_Perc_VT02=0의 요청 해제와 예열 단계의 추가OFF 분기를 구분합니다. 전류 변환 제목만으로 신호가FN02 소유라고 판단하지 않습니다.'),
    'FN03': dict(control=[1954], monitor=[1801, 1866],
        requests=['Flag.M_FN_03'], outputs=['Start FN03'],
        responses=['Inputs.FN03 Run', 'Inputs.FN03_All_SoftStarter'],
        note='FG51 TOR 피드백과 소프트스타터RUN 접점은 구분합니다. Tag_66의 두SD 쓰기·펄스 접점·버너 기동OFF 분기는 현재 실행 순서 확인 대상입니다.'),
    'FN06': dict(control=[1955], monitor=[1802],
        requests=['Flag.M_FN_06'], outputs=['Start FN06'],
        responses=['Inputs.FEEDBACKMOTOR FN-06', 'Inputs.RD01 run'],
        note='RD01 응답 상실에 따른 요청 해제와 MBVA01_FAULT 래치를 분리합니다. 다른 이름의 고장 태그는 원본 그대로 기록합니다.'),
    'PV01': dict(control=[1911, 1914, 1915], monitor=[1921, 1922, 1815, 1816],
        requests=['Flag.Enable_R1_GATE'], outputs=['PV-01 Gate a', 'PV-01 GATE B EV'],
        responses=['EV01_Open', 'EV01_Close', 'EV02_Open', 'EV02_Close', 'Inputs.FC GATE A OPEN', 'Inputs.LIMIT SWITCH LS-02GATE A CLOSEDVALVE PV-01'],
        note='자동 허가·게이트 명령·최종EV 출력·위치 입력·MEM_OPEN/CLOSE는 다른 단계입니다. LS02/SPARE와 원시 입력→Inputs 전달 미확정은 별도 확인합니다.'),
    'PV02': dict(control=[1916, 1919, 1920], monitor=[1923, 1924, 1817, 1818],
        requests=['Flag.Enable_R2_GATE'], outputs=['PV-02 GATE A EV', 'PV-02 GATE B EV'],
        responses=['EV04_Open', 'EV04_Close', 'EV05_Open', 'EV05_Close', 'Inputs.MC04 run'],
        note='MC04 응답·배출 자동 허가·두 게이트 명령과EV 출력을 구분합니다. LS25/26 행 위치와 현재 센서 극성·배선은 확인 전입니다.'),
    'MV01': dict(control=[1702], monitor=[1703, 1714],
        requests=['Flag.M_MV01_OPEN', 'Flag.M_MV01_Close', 'Flag.MV01_Auto'],
        outputs=['Start Open MV-01', 'Start Close MV-01'],
        responses=['Inputs.MV01 Open', 'Inputs.MV01 Close'],
        note='수동 방향 요청·자동PID·반대 방향 출력·끝단·엔코더 교정 허가를 분리합니다. TM 채널 주소와±2000의 실제 단위는 확인 전입니다.'),
    'MV03': dict(control=[1706], monitor=[1707, 1714, 1868],
        requests=['Flag.M_MV03_OPEN', 'Flag.M_MV03_CLOSE', 'Flag.MV03_Auto', 'Close MV03 for Burner Startup', 'Open MV03 for washing'],
        outputs=['Start open MV03', 'Start Close MV03'],
        responses=['Inputs.MV03 open', 'Inputs.MV03 Close'],
        note='일반 압력 제어와 버너 세정·기동 요청을 구분합니다. 원시 리미트→Inputs의 반전, PSH02/PSH03 명칭과 교정 조건을 확인합니다.'),
    'MV06': dict(control=[1711], monitor=[1709, 1714],
        requests=['Flag.MV06_Open', 'Flag.MV06_Close', 'Flag.MV06_Auto'],
        outputs=['Open MV06', 'Close MV06'],
        responses=['Inputs.MV06_Open', 'Inputs.MV06 Close'],
        note='1711의NOT ON 조건을 원본 그대로 기록합니다. 공동 인버터 허가와 방향 접촉기를 구분하며 LS34/35와40/41, TM 엔코더 주소는 미확정입니다.'),
    'BR01': dict(control=[1866], monitor=[1857, 1858, 1868, 1854],
        requests=['Flag.Start_Burner'], outputs=['Rem. Start/Stop Burner'],
        responses=['Inputs.Burner On', 'Inputs.FN03 Run', 'Flag.Burner_ready'],
        note='GME 운전 요청·두Enable 주소·외부 버너 제어기 응답을 구분합니다. 전용010-390 내부 연소 안전 시퀀스는 확보 전이며 이 작업지로 내부 고장을 확정하지 않습니다.'),
}

def expr(v):
    op = v['op']
    if op == 'const': return str(v.get('literal', int(v['value']) if isinstance(v['value'], bool) else v['value']))
    if op == 'read': return v['name']
    if op == 'unknown': return '[미해석: ' + v['reason'] + ']'
    if op == 'not': return 'NOT (' + expr(v['arg']) + ')'
    if op in ('and', 'or'):
        parts = [expr(x) for x in v['args'] if not (op == 'and' and x.get('op') == 'const' and x.get('value') is True)]
        return '(' + (' AND ' if op == 'and' else ' OR ').join(parts) + ')' if len(parts)>1 else parts[0] if parts else '1'
    return '(' + expr(v['left']) + ' ' + {'eq':'=','ne':'<>','gt':'>','ge':'>=','lt':'<','le':'<='}.get(op,op) + ' ' + expr(v['right']) + ')'

def netlink(n, part=None, oref=None, prefix='../'):
    # Existing source pages do not define per-ORef anchors. Show the UID alongside
    # the network link so it can be compared in its native reference table.
    return '<a href="'+prefix+'networks/network-'+str(n)+'.html">원본 '+str(n)+'</a>' + (' · Part '+e(part) if part else '')

def table(headers, rows):
    return '<div class="table-wrap"><table><thead><tr>'+''.join('<th>'+e(h)+'</th>' for h in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+v+'</td>' for v in row)+'</tr>' for row in rows)+'</tbody></table></div>'

def page(title, body, prefix='../'):
    return '<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+e(title)+'</title><link rel="stylesheet" href="'+prefix+'assets/all-in-one.css"><style>.repair-manual td code{white-space:normal;overflow-wrap:anywhere}.repair-manual td:last-child{min-width:150px}.repair-manual td a{display:inline-block}.repair-manual td:first-child{min-width:140px}</style></head><body class="repair-manual"><main style="max-width:1240px;margin:auto;padding:24px"><h1>'+e(title)+'</h1>'+body+'</main></body></html>'

stages = {(a['network'],a['part']):a for a in common['stages']}
records = []
source_paths = set()
for p in common['priority_profiles']:
    device = DEVICES.get(p['plc_id'])
    record = dict(key=p['key'], name=p['name'], plc_id=p['plc_id'], match=p['match'],
                  boundary='source_linked' if device else 'body_candidate' if p['plc_id'] else 'identity_unresolved',
                  common_stages=[stages[(a['network'],a['part'])] for a in p['stage_locations']],
                  bindings=[], output_actions=[], request_reset_actions=[], monitoring_actions=[], decisions=[],
                  source_networks=[], field_verified=False, repairs_completed=0)
    if device:
        record['note'] = device['note']
        record['source_networks'] = list(dict.fromkeys(device['control']+device['monitor']))
        for role in ('requests','outputs','responses'):
            for name in device[role]:
                refs = [dict(network=n, oref=u, source=nets[n]['file']) for n in record['source_networks']
                        for u,v in nets[n]['refs'].items() if v.get('name') and canon(v['name'])==canon(name)]
                if not refs:
                    refs = [dict(network=a['network'], oref=a['oref'], source=a['file'])
                            for a in signal['usages'] if a['scope']=='Global' and canon(a['name'])==canon(name)]
                assert refs, (p['key'],role,name)
                source_paths.update(r['source'] for r in refs)
                record['bindings'].append(dict(role=role, name=name,
                    addresses=[s['백업 주소'].upper() for s in symbols if canon(s['원본 심볼'])==canon(name)], refs=refs))
        names = {canon(n) for n in device['outputs']}
        record['output_actions'] = [dict(network=n, source=nets[n]['file'], **a) for n in device['control']
                                    for a in nets[n]['actions'] if canon(a['name']) in names]
        assert len(record['output_actions'])==len(device['outputs']),p['key']
        request_names={canon(n) for n in device['requests']}
        record['request_reset_actions'] = [dict(network=n, source=nets[n]['file'], **a) for n in record['source_networks']
                                           for a in nets[n]['actions'] if a['gate']=='RCoil' and canon(a['name']) in request_names]
        # Shared MV fault network contains six devices. Select only this device's
        # alarm and associated encoder-error values, without allocating neighbors.
        mv_faults = {'MV01': {'Allarm.MV01_FAULT','WorkData.W33','WorkData.W34'},
                     'MV03': {'Allarm.MV03_FAULT','WorkData.W29','WorkData.W30'},
                     'MV06': {'Allarm.MV_06_FAULT','WorkData.W19','WorkData.W20'}}
        washing = {'Open MV03 for washing','Close MV03 for Burner Startup','WorkData.BR01_State',
                   'Tag_142','Tag_143','Tag_144','Tag_145'}
        record['monitoring_actions'] = [dict(network=n, source=nets[n]['file'], **a) for n in device['monitor']
                                       for a in nets[n]['actions']
                                       if (n!=1714 or a['name'] in mv_faults[p['plc_id']])
                                       and (n!=1868 or p['plc_id']!='MV03' or a['name'] in washing)]
        record['decisions'] = [
            dict(id='request',title='운전 요청이 없거나 곧 해제됨',observe='현재 모드·공정 종류·Auto_ON1·카운터와 해당 요청의 변화를 같은 시각 기준으로 기록합니다.',
                 compare='아래 공통 단계의 관련 쓰기와 해당 요청의 모든 Global 쓰기 위치를 비교합니다. 원본 단계 Set이 현재 호출됐는지는 별도 확인합니다.',
                 next='상위 요청 미발생, 정상 정지 단계, 고장에 의한 요청 Reset을 구분합니다. 기동 명령을 추가하기 전 요청을 지운 주체를 확인합니다.',
                 common='common-stages'),
            dict(id='permit',title='요청은 있지만 최종 출력이 없음',observe='아래 최종 출력의 전체 조건과 현재 피연산자·모드를 기록합니다. 미해석 조건은 임의로0/1로 채우지 않습니다.',
                 compare='공통 ON·비상 모듈·모드 허가와 장치별 출력 조건을 대조합니다. Set 요청은 실제 Q 출력 또는 위치 도달의 증거가 아닙니다.',
                 next='억제 접점·반대 방향 출력·끝단·상하류 응답 중 실제로 조건이 다른 지점을 찾습니다. 현재 호출·다른 출력 쓰기도 함께 확인합니다.',
                 common='output-evidence'),
            dict(id='response',title='출력은 있지만 현장 응답이 없음',observe='최종 PLC 출력, 릴레이·구동기 입력, 실제 장치 상태, 원시 센서와 처리된 응답을 구간별로 기록합니다.',
                 compare='회로 작업지의 단자·직렬 허가·전원·구동기와 아래 응답 원본 참조를 비교합니다. 내부 기억만으로 물리 동작을 판단하지 않습니다.',
                 next='출력 전달 구간과 센서 전달 구간을 각각 확인합니다. 회로·원시 입력·Inputs·기억 중 어디서 차이가 시작됐는지 남깁니다.',
                 common='signal-boundary'),
            dict(id='stop',title='운전 중 정지하거나 연관 설비와 함께 정지함',observe='최초 알람·상하류 응답 변화·카운터·요청 Reset·출력 OFF의 시각을 기록합니다.',
                 compare='종류5 공통 정지 및 아래 장치 감시의 Set/Reset·시간 설정을 함께 비교합니다. 자동 단계 수치를 실제 초로 확정하지 않습니다.',
                 next='최초 원인과 후속 정지를 구분하고 관련 설비의 상태도 남깁니다. 최초 발생 기록 없이 후속 알람만으로 원인을 확정하지 않습니다.',
                 common='monitor-evidence'),
            dict(id='recovery',title='리셋 후 재기동되지 않거나 같은 알람이 반복됨',observe='원인 입력·래치·새 요청·출력·응답과 리셋 요청/출력을 각각 기록합니다.',
                 compare='장치별 RCoil과 공통930/931·비상1824·startup404/405의 기억을 구분합니다. 공통 리셋 출력은 물리 이상 해소의 증거가 아닙니다.',
                 next='원인 해소·래치 해제·허가 확인·승인된 재기동·연동 영향 확인을 분리해 기록합니다. 현재 PLC·실물 증거 전에는 수리 완료로 표시하지 않습니다.',
                 common='recovery')]
    else:
        record['note'] = '본체·전용 제어기·구동부의 경계와 실제 자료를 먼저 식별합니다. 주변 장치의 GME 신호를 이 설비의 직접 태그로 부여하지 않습니다.'
        record['decisions'] = [
            dict(id='identity',title='설비와 제어 주체 식별',observe='명판·설비 카드ID·위치·제어반·전용 제어기·자료 개정을 기록합니다.',compare='SEJIN 배치도·P&ID 연결과 실제 투입·배출·가스·공기·연동 경계를 대조합니다.',next='동일성 확인 후 해당 제어기의 I/O·알람·승인된 운전 순서 자료를 연결합니다.',common='boundary'),
            dict(id='local',title='본체 증상과 주변 설비 정지 구분',observe='발생 위치·시각·누설·막힘·온도·압력·소음 등 관찰 사실과 주변 설비 상태를 기록합니다.',compare='전용 제어기의 최초 알람과 상하류 요청·응답의 변화를 대조합니다. 수치·허용값·점검 주기는 제작사 근거가 필요합니다.',next='본체 이상과 구동부·계측·공통 정지의 영향을 분리합니다. 자료가 없는 장치의 제어 조건을 대신 만들지 않습니다.',common='boundary'),
            dict(id='recovery',title='복구 판단과 필요한 자료',observe='관찰 결과·조치·제작사 기준·원인 해소·전용 제어기 알람·승인된 복구 결과를 기록합니다.',compare='GME 공통 신호는 해당 설비와의 연동이 확인된 경우에만 함께 사용합니다.',next='확인 전 항목과 추가 사진·기계도면·전기도면·전용 매뉴얼을 명시하고 완료 판정을 유보합니다.',common='recovery')]
    source_paths.update(nets[n]['file'] for n in record['source_networks'])
    source_paths.update(a['source'] for a in record['common_stages'])
    records.append(record)

sources = {p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sorted(source_paths)}
register = dict(date='2026-10-08',scope='static repair decision manual; no PLC execution or simulator authoring',
                records=records,sources=sources,field_verified=0,repairs_completed=0,plc_changes=0,
                simulator_behavior_tests='not_rerun',simulator_development='stopped_by_user')
(ROOT/'registers/repair-decision.json').write_text(json.dumps(register,ensure_ascii=False,indent=2)+'\n')
flat=[dict(equipment=r['key'],plc_id=r['plc_id'],boundary=r['boundary'],**d) for r in records for d in r['decisions']]
with (ROOT/'registers/repair-decision.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(flat[0]));w.writeheader();w.writerows(flat)

for r in records:
    title=r['key']+' · '+r['name']+' 수리 판단·공통 영향 작업지'
    body='<div class="notice">원본 근거를 연결한 수리 판단 검토본입니다. 현재값·설치 동일성·현재 CPU·TIA 동작·현장 수리 완료는 확인 전입니다. 시뮬레이터 작성·시험 중지.</div>'
    body+='<p>'+e({'tag':'태그명 일치 / 실물 확인 전','candidate':'공정 역할 대응 후보 / 실물 확인 전','unknown':'PLC 대응 미확정'}[r['match']])+' · 참고 PLC 자료: '+e(r['plc_id'] or '미지정')+'</p>'
    body+='<p>'+e(r['note'])+'</p><nav class="inline-actions"><a href="../repair-decision.html">수리 판단 전체 목록</a><a href="../priority-guides/'+r['key']+'.html">실물 대응·점검</a><a href="../common-guides/'+r['key']+'.html">이 설비의 공통 제어</a>'
    if r['plc_id']:body+='<a href="../procedures/'+r['plc_id']+'.html">증상별 상세 수리</a>'
    if r['plc_id'] in ['CC01','AB01','HE01']:body+='<a href="../body-manual.html#body-'+r['plc_id']+'">본체·공정/계측 경계·증상별 수리 근거</a>'
    if r['plc_id'] in circuits:body+='<a href="../circuit-guides/'+r['plc_id']+'.html">전기 회로 추적</a><a href="../signal-guides/'+r['plc_id']+'.html">신호 전달·복수 쓰기</a>'
    if r['key'] in ['P03','P04','P14']:body+='<a href="../unresolved-identity.html#identity-'+r['key']+'">식별·원본 후보·필요 자료</a>'
    if r['key'] in ['P22','P23']:body+='<span>다른 공정 · 사용자 요청으로 관련 분석·보강 중단. 아래 기존 자료 보존.</span>'
    if r['plc_id'] in ['BC01','FN04','RD01','MC04','VS01','FN01','FN02','FN03','FN06','PV01','PV02','MV01','MV03','MV06']:
        body+='<a href="../alarm-guides/'+r['plc_id']+'.html">알람 발생·리셋·재기동 근거</a>'
    if r['plc_id']=='BR01':body+='<a href="../sensor-measurement.html">온도·압력·산소 입력·환산·수리 근거</a>'
    if r['plc_id'] in ['MV01','MV03','MV06']:body+='<a href="../encoder-position.html#position-'+r['plc_id']+'">엔코더·위치·교정 수리 근거</a>'
    body+='<a href="../hmi-transfer.html#profile-'+r['key']+'">HMI 태그·설정·표시 전달 확인</a>'
    body+='<a href="../recipe-settings.html#profile-'+r['key']+'">레시피·설정값·초기화와 다른 쓰기</a>'
    loop_id={'FN04':'FN04','MV01':'MV01','MV03':'MV03','MV06':'MV06','FN02':'VT02','BR01':'BR01'}.get(r['plc_id'])
    if loop_id:body+='<a href="../regulation-manual.html#loop-'+loop_id+'">조절 루프 입력·설정·출력·수리 근거</a>'
    if r['plc_id']=='BR01':body+='<a href="../measurement-trace.html">가스·공기 환산·출력 추적</a><a href="../process-stop-alarms.html">공정 알람·버너 정지 원인</a>'
    if r['plc_id'] in ['BR01','MV03']:body+='<a href="../burner-interface.html">BR01 외부 연동·정지·복구 및 MV03 요청 근거</a>'
    body+='</nav><h2 id="decision">1. 관찰 결과별 판단 순서</h2>'+table(['관찰 분기','먼저 기록','원본 비교','다음 판단'],[[e(d['title']),e(d['observe']),e(d['compare']),e(d['next'])+'<br><a href="#'+d['common']+'">관련 근거·확인</a>'] for d in r['decisions']])
    body+='<h2 id="boundary">2. 설비·신호 경계</h2>'
    if r['bindings']:
        body+=table(['역할·원본 이름','백업 주소','참조 근거'],[[e({'requests':'요청·모드','outputs':'최종 출력','responses':'응답·연관 상태'}[b['role']])+'<br><code>'+e(b['name'])+'</code>',e(' / '.join(b['addresses']) or 'DB/주소 추가 확인'),'<br>'.join(netlink(x['network'],oref=x['oref'])+' · ORef '+e(x['oref']) for x in b['refs'])] for b in r['bindings']])
    else:body+='<p>직접 요청·출력·PLC 태그를 부여하지 않았습니다. 본체 또는 전용 제어기의 명판·반 명칭·전용 자료·접점/통신 연동 근거가 필요합니다.</p>'
    body+='<h2 id="common-stages">3. 공통 단계의 해당 신호 쓰기</h2>'
    if r['boundary']=='source_linked':body+='<p>종류와 단계는 원본 비교값입니다. 현재 시작 주체·호출·OB 주기·카운터·ON/OFF를 확인하며 초 단위나 현재 운전 상태로 해석하지 않습니다.</p>'
    if r['common_stages']:
        body+=table(['종류·카운터','명령·대상','전체 정적 조건','근거'],[[e(str(a['type_value'])+' / '+(', '.join(map(str,a['counter_values'])) or '비교값 없음')),e(a['gate'])+'<br><code>'+e(a['target'])+'</code>','<code>'+e(expr(a['condition']))+'</code>',netlink(a['network'],a['part'])] for a in r['common_stages']])
    else:body+='<p>직접 배정한 공통 자동 단계는 없습니다. '+('아래 별도 자동/PID·버너 연동의 원본 조건을 확인합니다.' if r['boundary']=='source_linked' else '전용 제어기와 GME의 연동 경계를 먼저 식별합니다.')+'</p>'
    body+='<h2 id="output-evidence">4. 최종 출력의 허가·억제 조건</h2>'
    if r['request_reset_actions']:
        body+='<h3>운전 요청을 해제하는 관련 쓰기</h3>'+table(['요청·명령','해제의 전체 정적 조건','근거'],[[e(a['gate'])+'<br><code>'+e(a['name'])+'</code>','<code>'+e(expr(a['condition']))+'</code>',netlink(a['network'],a['uid'])] for a in r['request_reset_actions']])
    if r['output_actions']:
        body+=table(['최종 명령','전체 정적 조건','근거'],[[e(a['gate'])+'<br><code>'+e(a['name'])+'</code>','<code>'+e(expr(a['condition']))+'</code>',netlink(a['network'],a['uid'])] for a in r['output_actions']])
    else:body+='<p>최종 출력을 식별하기 전입니다. 해당 설비의 전용 자료와 현재 I/O를 확인합니다.</p>'
    body+='<h2 id="signal-boundary">5. 현장 출력·응답 전달</h2>'
    circuit=circuits.get(r['plc_id'])
    if circuit:
        body+='<p>'+e(circuit['distinction'])+'</p>'+table(['신호·백업','원본 FG·전달 구간','확인 지점'],[[e(x['signal'])+'<br>'+e(x['backup']),e('FG'+str(x['fg'])+' / '+' → '.join(x['nodes']))+'<br>'+e(x.get('destination','')),e(x['check'])] for x in circuit['paths']])
        body+='<p><a href="../circuit-guides/'+r['plc_id']+'.html">도면·단자·원본 ORef 상세 보기</a> · <a href="../signal-guides/'+r['plc_id']+'.html">원시 입력·Inputs·메모의 전달과 쓰기 위치</a></p>'
    else:body+='<p>현재 회로와 연동을 확인하기 전입니다. 다른 설비의 단자·출력·센서를 복사하지 않습니다.</p>'
    body+='<h2 id="monitor-evidence">6. 감시·연관 허가·복구의 관련 쓰기</h2>'
    if r['monitoring_actions']:
        body+='<p>선택한 원본 경로의 감시·허가·교정·연관 쓰기입니다. 요청·최종 출력·메모·연산 값은 서로 다른 역할이며 미해석은 원본 확인 항목입니다.</p>'
        if r['plc_id'] in ('MV01','MV03','MV06'):body+='<p>공유1714는 해당 댐퍼의 고장·오차 값만 표시합니다. 다른 댐퍼의 고장을 이 장치에 배정하지 않습니다.</p>'
        if r['plc_id'] in ('MV03','BR01'):body+='<p>버너 연동은 GME 원본의 관련 경로이며 전용 연소 제어기의 내부 안전 로직은 확보 전입니다.</p>'
    if r['monitoring_actions']:
        body+=table(['명령·대상','전체 정적 조건','원본 시간·전달값','근거'],[[e(a['gate'])+'<br><code>'+e(a['name'])+'</code>','<code>'+e(expr(a['condition']))+'</code>',e(expr(a['preset'])) if 'preset' in a else e(expr(a['value'])) if 'value' in a else '',netlink(a['network'],a['uid'])] for a in r['monitoring_actions']])
    else:body+='<p>전용 알람 조건을 식별하기 전입니다. 현재 제어기의 알람·리셋 근거를 확보합니다.</p>'
    body+='<h2 id="recovery">7. 복구 증거와 기록</h2>'
    if r['boundary']=='source_linked':
        body+='<ol><li>원인 입력·장치 상태와 최초 알람을 각각 확인합니다.</li><li>장치별 래치 해제와 공통 리셋의 요청·타이머·출력을 구분합니다. <a href="../common-control.html#reset">공통930/931·비상1824 근거</a></li><li>요청·허가·단계·방향·타이머와 전원 재시작의 기억 상태를 확인합니다. <a href="../common-control.html#restart">startup 초기화·유지 상태 확인</a></li><li>승인된 복구 절차의 응답·출력·알람·연동 영향을 기록하고, 미확인 조건은 남깁니다.</li></ol>'
    else:
        body+='<ol><li>본체·전용 제어기의 자료와 현재 상태를 확인하고 관찰·조치·미확인 항목을 기록합니다.</li><li>제작사·현장의 승인된 복구 기준으로 원인 해소·알람·요청·응답을 확인합니다.</li><li>GME와의 연동이 확인된 경우에만 공통 정지·리셋·재기동 영향을 함께 기록합니다. <a href="../common-control.html">GME 공통 자료 참고</a></li><li>확인한 근거와 승인된 복구 결과가 갖춰지기 전에는 수리 완료로 판정하지 않습니다.</li></ol>'
    template=dict(equipment=r['key'],name=r['name'],reference_plc_id=r['plc_id'],actual_equipment_id=None,
        timestamp=None,mode=None,first_symptom=None,first_alarm=None,current_plc_version=None,observations=[],
        cause_candidates=[],work_performed=None,recovery_evidence=[],unresolved=[],status='미작성',field_verified=False)
    (ROOT/'registers'/('repair-observation-'+r['key']+'.json')).write_text(json.dumps(template,ensure_ascii=False,indent=2)+'\n')
    body+='<p><a href="../index.html#view=repair-record&amp;equipment='+r['key']+'&amp;scope=priority">올인원에서 수리 관찰 기록 작성</a> · <a download href="../registers/repair-observation-'+r['key']+'.json">빈 수리 관찰 기록 JSON 다운로드</a> · 실제 관찰값은 채우지 않았습니다. 작성한 기록은 현재 브라우저에 저장하고 JSON으로 별도 보관합니다. 자동 가져오기·동기화 기능은 제공하지 않습니다.</p>'
    (out/(r['key']+'.html')).write_text(page(title,body))

body='<div class="notice">디코팅 우선23개 설비의 수리 판단과 공통 제어 영향을 연결합니다. 원본 제어 근거를 식별한15개(킬른 구동부 참고1개 포함), 본체 후보3개, PLC 대응 미확정5개를 구분합니다. 현재값·실물·현재 CPU·현장 수리 결과는 확인 전, PLC 변경0건입니다. 시뮬레이터 작성·시험 중지.</div>'
body+='<p>증상 기록 → 요청·허가 → 최종 출력 → 전기·물리 응답 → 알람·복구 순서로 확인합니다. 원본 조건과 현장 관찰을 구분하며 공통 정지와 개별 고장을 함께 비교합니다.</p>'
body+=table(['우선 설비','자료 범위','판단 분기','작업지'],[[e(r['key']+' · '+r['name']),e({'source_linked':'PLC·회로 근거 연결 / 실물 확인 전','body_candidate':'본체 대응 후보 / 직접 태그 미부여','identity_unresolved':'제어 주체·PLC 대응 미확정'}[r['boundary']]),str(len(r['decisions'])),'<a href="repair-guides/'+r['key']+'.html">수리 판단 작업지</a>'] for r in records])
body+='<p><a href="common-control.html">공통 제어 매뉴얼</a> · <a href="registers/repair-decision.json">수리 판단 JSON</a> · <a href="registers/repair-decision.csv">수리 판단 CSV</a></p>'
(ROOT/'repair-decision.html').write_text(page('수리 판단·공통 영향 통합 작업지',body,''))
print(json.dumps(dict(priority_repair_guides=len(records),source_linked_devices=len(DEVICES),
                     decision_branches=len(flat),source_files=len(sources),field_verified=0,
                     simulator_behavior_tests='not_rerun'),ensure_ascii=False))
