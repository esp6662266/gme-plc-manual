"""Visually reviewed electrical paths, kept separate from virtual PLC behavior."""
from pathlib import Path
import csv, hashlib, html, json, runpy

ROOT = Path(__file__).resolve().parent
out = ROOT / 'circuit-guides'
out.mkdir(exist_ok=True)
e = lambda value: html.escape(str(value))

devices = [
    dict(id='BC01', title='드럼 투입 컨베이어', sheets=[18, 19], pages=[19, 20],
         equipment='FG18: 모터 M02 BC-01, 18AS1 ABB ACS355-03E-08A8-4(4kW), 18QM1·18QS1. 도면 정격은 현장 명판 확인 전 참고값입니다.',
         distinction='PLC 출력 1과 인버터 DI1의 실제 기동 입력은 다릅니다. SS-01·18QS1·18QM1의 직렬 접점과 19KA1을 거친 회로를 별도로 확인합니다.',
         paths=[
             dict(signal='기동 명령', drawing='A0.0', backup='%Q0.0 / start bc01', fg=19,
                  nodes=['A0.0 (FG136/1 참조)', 'X1:44 / 2A F(5×20)', 'SS-01:11→12', 'X1:45 → XS:1', '18QS1 보조접점 → XS:2', '18QM1 보조접점', '19KA1 코일 A1→A2 / 0V'],
                  destination='FG18: +24V 단자9 → 19KA1 접점1→9 → 인버터 단자12(DI1 START).',
                  check='Q0.0=1인데 DI1이 없으면 직렬 회로·19KA1 코일과 접점을 구간별로 확인합니다. PLC 로직 허가와 현장 접점 허가를 함께 기록합니다.'),
             dict(signal='운전 응답', drawing='E0.0', backup='%I0.0 / bc01_fbk', fg=18,
                  nodes=['+24Vdc 10.7 → 18AS1 단자17(RUNNING 공통)', '18AS1 단자19 → E0.0', 'FG116/2 PLC 입력 참조'],
                  destination='PLC 입력 → 내부 Inputs.BC01 run 전달 위치는 현재 복원 자료에서 확정하지 못했습니다. 알람 사용 위치는 원본1785입니다.',
                  check='인버터 RUNNING 출력, PLC I0.0, 내부 응답을 따로 기록합니다. 릴레이 출력의 파라미터 기능·정상 극성은 현재 설정과 대조합니다.'),
             dict(signal='인버터 이상', drawing='E0.1', backup='%I0.1 / bc01_all_inv', fg=18,
                  nodes=['+24Vdc 10.7 → 18AS1 단자20(ALARM 공통)', '18AS1 단자21 → E0.1', 'FG116/2 PLC 입력 참조'],
                  destination='원본1785는 Inputs.BC01_All_inv를 읽어 Allarm.BC01_INV를 Set/Reset합니다. 물리 입력과 내부 신호의 전체 전달은 미확정입니다.',
                  check='도면의 ALARM 표기만으로 입력1=고장이라고 확정하지 않습니다. 출력 접점 기능·정상 상태·입력 반전 여부를 확인합니다.'),
             dict(signal='트립와이어 감시', drawing='E6.2', backup='%I6.2 / bc01_tripwire', fg=19,
                  nodes=['+24Vdc 10.7 → X1:46 / 2A F(5×20)', 'SS-01:13→14', 'X1:47 → E6.2', 'FG122/3 PLC 입력 참조'],
                  destination='SS-01의 기동 회로 접점11/12와 감시 접점13/14는 점선으로 기계적 연결이 표시됩니다. 원본1786은 내부 trip wire 알람을 관리합니다.',
                  check='두 접점의 동작·복귀와 PLC 입력을 함께 확인합니다. 내부 시험 모드로 현장 직렬 접점의 허가를 대신할 수 있다고 설명하지 않습니다.'),
             dict(signal='회전 감시 예비', drawing='E6.3', backup='%I6.3 / bc01_prox', fg=19,
                  nodes=['+24Vdc 10.7 → X1:48 / 2A F(5×20)', 'SSL-01:13→14', 'X1:49 → E6.3', 'FG122/4 PLC 입력 참조'],
                  destination='FG19의 점선 SPARE 영역에 있습니다. 트립와이어 E6.2와 별도 신호입니다.',
                  check='도면 존재와 실제 설치·사용을 구분합니다. 예비 입력을 회전 정상 조건이나 안전 스위치 대체 입력으로 지정하지 않습니다.'),
         ], networks=[1785, 1786, 1935],
         pending=['FG136/116/122 PLC 단자 모듈과 현장 배선의 끝점 대조', 'BC01 물리 입력→Inputs DB의 전달 위치 및 반전 확인', 'SS-01 두 접점의 정상·트립·복귀 상태와 설치 상태', '18AS1 출력 접점 설정 및 현장 명판·파라미터', '별도 속도 회로: FG18의 ±PAW288·AI1 단자2/3, FG112/1 참조 확인']),
    dict(id='FN04', title='집진 흡입 팬', sheets=[59, 60], pages=[60, 61],
         equipment='FG59: 59AS1 ABB ACS580-01-293A-4(160kW) 출력에서 M31 FN-04와 M36 FN-04A 두 모터(도면 각75kW·123A)로 분기합니다. 두 모터의 실물·설비 카드 관계는 미확인입니다.',
         distinction='FN04 PLC 태그 하나를 단일 모터로 해석하면 안 됩니다. 공동 인버터와 두 분기 차단기·개폐기·모터를 나눠 진단합니다.',
         paths=[
             dict(signal='기동 명령', drawing='A17.1', backup='%Q17.1 / start fn04', fg=60,
                  nodes=['A17.1 (FG180/1 참조)', 'X3:124 → X5:14', '59QS1 보조접점 → X5:15', '59QS2 보조접점 → X5:16', '59QM1 보조접점', '59QM2 보조접점', '59QM3 보조접점', '60KA1 코일 A1→A2 / 0V152.4'],
                  destination='FG59: 인버터 단자10(+24V) → 60KA1 접점1→9 → 단자13(DI1).',
                  check='Q17.1=1이어도 직렬 접점이 열리면 60KA1·DI1의 기동이 전달되지 않을 수 있습니다. 두 모터 분기와 공통 인버터 허가를 함께 조사합니다.'),
             dict(signal='운전 응답', drawing='E28.2', backup='%I28.2 / fn04_fbk', fg=59,
                  nodes=['+24Vdc152.5 → 59AS1 단자22(RUNNING 공통)', '59AS1 단자24 → X5:7 → X3:107', 'E28.2 → FG177/3 PLC 입력 참조'],
                  destination='원본1070 hmi inputs: FN04_Fbk → Inputs.FN04 Run(코일 Part118). 사용 위치1809·1964 등. 원본1085 simulation도 같은 내부 응답을 씁니다.',
                  check='공통 인버터 RUNNING만으로 두 모터가 각각 정상 회전했다고 판단하지 않습니다. 물리 입력, 내부 응답, 두 모터 관찰을 별도 기록합니다. 입력 전달 블록의 현재 호출과 다른 쓰기 위치도 확인합니다.'),
             dict(signal='인버터 이상', drawing='E28.3', backup='%I28.3 / fn04_all_inv', fg=59,
                  nodes=['+24Vdc152.5 → 59AS1 단자25(ALARM 공통)', '59AS1 단자27 → X5:8 → X3:108', 'E28.3 → FG177/4 PLC 입력 참조'],
                  destination='원본1070: FN04_All_inv → Inputs.FN04_All_inv(코일 Part120). 원본1809에서 래치,1965에서 요청 해제.',
                  check='ALARM 릴레이 기능·현재 정상 극성과 PLC 내부 반전을 확인합니다. 표기 또는 가상 시험의 초기값을 현장 정상값으로 쓰지 않습니다.'),
             dict(signal='속도 설정', drawing='±PAW336', backup='%QW336 / fn04_sp', fg=59,
                  nodes=['+PAW336 → X3:120 → X5:10 → 59AS1 단자2(AI1+)', '-PAW336 → X3:121 → X5:11 → 단자3(AGND)', 'FG180A/1 아날로그 출력 참조'],
                  destination='도면 AI1은 4–20mA 표기. 원본1689는 Data.SET_PERC_FN04와 FN04_SP를 연결합니다. 변환 명령은 지원 부분 실행 범위 밖입니다.',
                  check='요청 백분율·PLC 원시 출력·실제 AI1 신호·인버터 주파수의 네 값을 구분합니다. PLC 스케일·인버터 파라미터·허용 풍량을 확인한 뒤 판단합니다.'),
             dict(signal='전류 전달', drawing='±PEW394', backup='%IW394 / fn04_current', fg=59,
                  nodes=['59AS1 단자8(AO2) → X5:12 → X3:122 → +PEW394', '단자9(AGND) → X5:13 → X3:123 → -PEW394', 'FG172/1·2 아날로그 입력 참조'],
                  destination='원본1071: FN04_Current → Inputs.FN04_Absorption(Part123). 변환 제목 fn-02 aspirator와 실제 FN04 신호의 불일치는 계속 확인합니다.',
                  check='공통 인버터의 전달값을 각 모터 개별 전류라고 단정하지 않습니다. AO2 기능과 환산 범위·HMI 표시 단위를 대조합니다.'),
         ], networks=[1070,1071,1085,1689,1770,1809,1964,1965],
         pending=['Q17.1→60KA1 명령 회로와 FG180 출력 모듈·현재 배선 대조', '백업 Q4.2 spare_0와 과거 설명의 관계: 기존 FN04 자료 불일치 유지', 'M31 FN-04와 M36 FN-04A 실물·설비 카드·정비 이력을 별도 식별', '두 분기 중 한쪽 차단 시 기동 허가·운전 응답·보호 정책 확인', '59AS1 AI1/AO2·RUNNING/ALARM의 현재 파라미터·스케일 확인', 'hmi inputs와 원본 simulation 블록의 현재 호출 조건·동일 응답 복수 쓰기 확인', '1689에서 SET_PERC_FN04를 5~100으로 제한하는 쓰기와 1965의 설정0 정지 조건: 전체 호출·다른 쓰기 순서 확인']),
]
devices.extend(runpy.run_path(str(ROOT/'circuit-source-details.py'))['extra_devices'])
devices.extend(runpy.run_path(str(ROOT/'circuit-actuator-details.py'))['actuator_devices'])
native=json.loads((ROOT/'registers/program-model.json').read_text())['networks']
for d in devices:
    for p in d['paths']:
        p['native_symbol_references']=[]
        if p['backup']:
            name=p['backup'].split(' / ',1)[1].casefold()
            p['native_symbol_references']=[dict(network=n['id'],uid=uid,block=n['block'],title=n['title'],file=n['file']) for n in native for uid,r in n['refs'].items() if (r['name'] or '').casefold()==name]
    d['networks']=sorted(set(d['networks'])|{r['network'] for p in d['paths'] for r in p['native_symbol_references']})
reviewed_fgs=sorted({f for d in devices for f in d['sheets']})
path_count=sum(len(d['paths']) for d in devices)
unresolved_addresses=sum(p['backup'] is None for d in devices for p in d['paths'])
vendor_review=json.loads((ROOT/'registers/vendor-reference-review.json').read_text()) if (ROOT/'registers/vendor-reference-review.json').exists() else None

def table(headers, rows):
    return '<div class="table-wrap"><table><thead><tr>'+''.join('<th>'+e(h)+'</th>' for h in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+v+'</td>' for v in row)+'</tr>' for row in rows)+'</tbody></table></div>'

def pdf_link(fg):
    pg = {'5A':6,'180A':182,'180B':183}.get(str(fg), int(fg)+(1 if int(fg)>5 else 0)+(2 if int(fg)>180 else 0) if str(fg).isdigit() else 0)
    return '<a href="../sources/Electrical_Rev2.pdf#page='+str(pg)+'">FG'+e(fg)+' · PDF '+str(pg)+'</a>'

for d in devices:
    body='<h1>'+e(d['id']+' · '+d['title']+' 전기 회로 추적')+'</h1><div class="notice info">원본 전기도면을 시각 확인한 정적 회로 해석입니다. 현재 배선·입력 극성·파라미터와 현장 측정은 미확인입니다. 전기 작업은 승인된 현장 절차와 자격 범위에서 수행합니다.</div>'
    body+='<nav class="inline-actions">'+''.join(pdf_link(f) for f in d['sheets'])+'<a href="../procedures/'+d['id']+'.html">진단·수리 작업지</a><a href="../electrical-trace.html">회로 추적 목록</a></nav><h2>1. 도면의 구성과 진단 경계</h2><p>'+e(d['equipment'])+'</p><p>'+e(d['distinction'])+'</p>'
    if (ROOT/'construction-guides'/(d['id']+'.html')).exists():
        body+='<p><a href="../construction-guides/'+e(d['id'])+'.html">추가 시공도면 · 접속함·케이블·배관 경로</a> — 승인·현재 설치는 확인 전입니다.</p>'
    body+='<p><a href="../signal-guides/'+e(d['id'])+'.html">PLC 신호 전달·반전·복수 쓰기 위치</a></p>'
    body+='<nav class="inline-actions" aria-label="신호 경로 바로가기">'+''.join('<a href="#signal-'+str(i)+'">'+e(p['signal'])+'</a>' for i,p in enumerate(d['paths'],1))+'</nav>'
    for i, path in enumerate(d['paths'],1):
        backup=e(path['backup']) if path['backup'] else '주소·채널 오프셋 미확정 · TM 구성/선언 확인 필요'
        body+='<h2 id="signal-'+str(i)+'">'+str(i+1)+'. '+e(path['signal'])+'</h2><p><strong>'+e(path['drawing'])+'</strong> ↔ 백업 '+backup+' · '+pdf_link(path['fg'])+'</p><ol>'+''.join('<li>'+e(n)+'</li>' for n in path['nodes'])+'</ol><p><strong>전달·사용 위치:</strong> '+e(path['destination'])+'</p><div class="notice"><strong>진단 판단:</strong> '+e(path['check'])+'</div>'
        if path['backup']:
            body+='<p><strong>원본 심볼 직접 참조:</strong> '+(' · '.join('<a href="../networks/network-'+str(r['network'])+'.html">'+e(str(r['network'])+' / '+r['block']+' / ORef '+r['uid'])+'</a>' for r in path['native_symbol_references']) or '복원 LAD에서 이 이름의 직접 참조는 찾지 못했습니다. 내부 Inputs 등의 별도 전달·미해석 참조·현재 프로그램은 확인 전입니다.')+'</p>'
    body+='<p>위 직접 참조는 복원 원본의 같은 심볼명 위치입니다. 읽기·쓰기 역할, 현재 호출, 현장 사용을 함께 확정한 표는 아닙니다. 원본의 simulation 블록 참조가 있더라도 이번 작업에서 가상 실행·개발·시험은 진행하지 않았습니다.</p>'
    body+='<h2>원본 PLC와 연결</h2><nav class="inline-actions">'+''.join('<a href="../networks/network-'+str(n)+'.html">원본 '+str(n)+'</a>' for n in d['networks'])+'</nav><h2>남은 확인과 기록</h2><ul>'+''.join('<li>'+e(v)+'</li>' for v in d['pending'])+'</ul>'
    if vendor_review and d['id'] in ('RD01','FN01','FN02','FN04'):
        body+='<h2>제조사 단자 정의 대조</h2><p>ABB ACS580-01 하드웨어 매뉴얼 Rev.D의 인쇄141·142페이지(PDF145·146)는22=RO2C,25=RO3C로 정의합니다. 이 자료는 단자 정의 대조에 사용하며 기본 매크로의 신호 기능·전압 모드를 현재 현장 설정으로 간주하지 않습니다.</p><p><a href="'+e(vendor_review['url'])+'#page=146" target="_blank" rel="noopener">ABB 공식 하드웨어 매뉴얼</a></p>'
    if d['id']=='FN04':
        body+='<p>정정 기록: 초기 작업지의 공통 단자23·26 표기를 확대 도면과 ABB 정의에 따라22·25로 바로잡았습니다. 원본 도면은 변경하지 않았습니다.</p>'
    body+='<h2>도면을 함께 확인</h2>'+''.join('<details><summary>FG '+e(f)+' · 해당 도면 보기</summary><a href="../sources/Electrical_Rev2.pdf#page='+str(d['pages'][d['sheets'].index(f)])+'"><img class="source-image" src="../assets/circuits/FG'+e(f)+'.png" alt="전기도면 FG '+e(f)+' 원본 페이지 렌더" loading="lazy"></a></details>' for f in d['sheets'] if (ROOT/'assets/circuits'/('FG'+str(f)+'.png')).exists())
    body+=table(['기록 항목','내용'],[[e(k),e(v)] for k,v in [('현장 식별','설비 ID / 반·단자대 / 모터·인버터 명판 / 도면 개정'),('신호 구간','PLC 명령 / 단자 / 직렬 접점 / 릴레이 / DI / 응답 접점 / 입력 / 내부 DB'),('관찰 결과','시각 / 운전 모드 / 기준값의 근거 / 관찰값 / 최초 불일치 구간'),('복구 확인','원인·조치 / 원인 해제 / Reset / 재요청 / 주변 설비 영향')]])
    page='<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+e(d['id'])+' 전기 회로 추적</title><link rel="stylesheet" href="../assets/all-in-one.css"></head><body><main style="max-width:1240px;margin:auto;padding:24px">'+body+'</main></body></html>'
    (out/(d['id']+'.html')).write_text(page)

record=dict(source='sources/Electrical_Rev2.pdf', source_sha256=hashlib.sha256((ROOT/'sources/Electrical_Rev2.pdf').read_bytes()).hexdigest(), date='2026-10-07', scope='visual review of listed GME electrical sheets and original ladder static references; no field verification', reviewed_fgs=reviewed_fgs, diagrams_visually_reviewed=len(reviewed_fgs), signal_paths=path_count, circuit_guides=len(devices), unresolved_backup_addresses=unresolved_addresses, direct_symbol_reference_count=sum(len(p['native_symbol_references']) for d in devices for p in d['paths']), simulator_behavior_tests='not_rerun', field_verified=0, plc_changes=0, devices=devices)
(ROOT/'registers/electrical-trace.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
with (ROOT/'registers/electrical-trace.csv').open('w',encoding='utf-8-sig',newline='') as f:
    writer=csv.writer(f); writer.writerow(['설비','신호','도면 주소','백업 주소','FG','회로 경로','내부 전달·사용','진단','확인 상태'])
    for d in devices:
        for p in d['paths']:writer.writerow([d['id'],p['signal'],p['drawing'],p['backup'] or '주소·채널 오프셋 미확정',p['fg'],' → '.join(p['nodes']),p['destination'],p['check'],'도면 시각 확인 / 현장 미확인'])
body='<h1>전기 회로 추적 · 모터·팬·게이트·댐퍼·버너</h1><div class="notice">'+str(len(devices))+'개 항목의 '+str(path_count)+'개 신호 경로, '+str(len(reviewed_fgs))+'개 FG의 도면 시각 확인을 기록했습니다. '+str(unresolved_addresses)+'개 엔코더 경로의 백업 주소·채널 오프셋은 미확정입니다. 현장 배선·정상 극성·설정은 확인 전입니다.</div><nav class="inline-actions">'+''.join('<a href="circuit-guides/'+d['id']+'.html">'+e(d['id']+' · '+d['title'])+'</a>' for d in devices)+'</nav><p>직렬 접점·릴레이·공통 인버터·개별 모터·소프트스타터TOR·방향 접촉기·끝단·엔코더·게이트 기억을 구분합니다. 버너는 전용010-390 도면과의 외부 인터페이스 범위입니다. 전체248개 ID와 우선23개 대응 상태는 보존합니다.</p><p><a href="construction-guide.html">추가 시공도면 · 배관·케이블 참조</a> · <a href="registers/electrical-trace.json">검토 JSON</a> · <a href="registers/electrical-trace.csv">검토 CSV</a> · <a href="registers/manual-corrections.json">단자 표기 정정 기록</a></p>'
(ROOT/'electrical-trace.html').write_text('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>전기 회로 추적</title><link rel="stylesheet" href="assets/all-in-one.css"></head><body><main style="max-width:1240px;margin:auto;padding:24px">'+body+'</main></body></html>')
print(json.dumps(dict(circuit_guides=len(devices),signal_paths=path_count,diagrams_visually_reviewed=len(reviewed_fgs),unresolved_backup_addresses=unresolved_addresses,field_verified=0),ensure_ascii=False))
