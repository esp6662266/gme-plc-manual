"""Source-linked diagnostic worksheets; no fabricated terminal numbers or limits."""
from pathlib import Path
import json
import html

ROOT=Path(__file__).resolve().parent
specs=json.loads((ROOT/'registers/control-spec.json').read_text())['specifications']
model=json.loads((ROOT/'registers/program-model.json').read_text())
network_map={n['id']:n for n in model['networks']}
out=ROOT/'procedures';out.mkdir(exist_ok=True)
e=lambda v:html.escape(str(v))

def expression(a):
    op=a.get('op')
    if op=='const':return a.get('literal', '1' if a['value'] is True else '0' if a['value'] is False else str(a['value']))
    if op=='read':return a['name']
    if op=='unknown':return '[미확인: '+a['reason']+']'
    if op=='not':return 'NOT ('+expression(a['arg'])+')'
    if op in ('and','or'):
        values=[expression(v) for v in a['args']]
        values=[v for v in values if v!='1'] if op=='and' else values
        return '('+(' AND ' if op=='and' else ' OR ').join(dict.fromkeys(values))+')' if len(values)>1 else values[0] if values else '1'
    return '('+expression(a['left'])+' '+{'eq':'=','ne':'<>','gt':'>','ge':'>=','lt':'<','le':'<='}.get(op,op)+' '+expression(a['right'])+')'

def table(head,rows):
    return '<div class="table-wrap"><table><thead><tr>'+''.join('<th>'+e(h)+'</th>' for h in head)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+v+'</td>' for v in row)+'</tr>' for row in rows)+'</tbody></table></div>'

def netlink(id):return '<a href="../networks/network-'+str(id)+'.html">원본 '+str(id)+'</a>'
def pdfpage(fg):
    if str(fg) in ('5A','180A','180B'):return {'5A':6,'180A':182,'180B':183}[str(fg)]
    return int(fg)+(1 if int(fg)>5 else 0)+(2 if int(fg)>180 else 0)

pilots={
 'BC01':dict(core=[1935,1785,1786],
   summary='운전 요청 Flag와 세 허가 경로를 확인한 뒤, 피드백·인버터 이상을 2초 감시합니다. 트립와이어 알람은 별도 네트워크에서 래치됩니다.',
   cases=[
    ('기동을 눌러도 Start가 0','Flag.M_BC_01, ON과 R1_GATE_LOOP_ON·MemoCMD_BC01_Startup·Maintenance_ON을 순서대로 확인합니다. 세 허가 경로는 OR이며, 고장 경로는 요청 Flag를 리셋합니다.','1935의 Start BC01 코일과 Flag.M_BC_01 리셋 조건을 함께 기록합니다. 보존한 과거 부분 시험에서는 세 허가0일 때 기동 억제를 관찰했습니다. 이번 작업은 해당 원본 조건을 정적으로 대조합니다.','실제 자동·수동 요청을 누가 쓰는지 HMI Inputs와 자동 시퀀스의 복수 쓰기 위치를 확인합니다.'),
    ('Start는 1인데 운전 피드백이 없음','백업 기준 Q0.0(Start), I0.0(피드백), I0.1(인버터 이상)을 대조합니다. 출력 명령·인버터 운전 상태·보조접점·PLC 입력을 구간별로 확인합니다.','1785의 Tag_51은 S5T#2S입니다. 감시 만료 후 BC_01_FAULT가 래치되면 1935에서 요청 Flag가 해제되고 Start가 0이 되는 경로를 추적합니다.','단자 번호·인버터 파라미터·현장 입력의 정상 극성은 FG18·19와 현장 상태를 대조해 기록합니다.'),
    ('트립와이어 알람이 리셋되지 않음','I6.2 백업 심볼 bc01_tripwire와 Inputs.BC01 trip wire를 추적합니다. 현장 안전 스위치의 원인과 복귀 상태를 확인합니다.','1786은 RESET_ALLARM AND NOT trip wire AND 기존 FC 래치 조건에서 FC를 리셋합니다. 신호가 남아 있으면 리셋되지 않는 조건을 원본 접점·실제 입력 기록과 대조합니다.','I6.3의 bc01_prox는 다른 입력입니다. 트립와이어와 대신 연결하지 않습니다. UNDER TESTING 상태의 실제 용도는 별도 확인합니다.'),
    ('원인을 제거했는데 다시 운전하지 않음','원인 입력 해제와 기존 래치 해제를 구분합니다. 리셋 후 요청 Flag와 세 허가 경로를 다시 확인합니다.','원본1935의 고장 경로는 요청 Flag를 리셋합니다. 원인 해제·알람 리셋·새 운전 요청의 역할을 따로 확인하며, 다른 블록의 자동 재요청은 전체 호출에서 대조합니다.','전원 재시작·유지 메모리·다른 블록의 자동 재요청은 현재 CPU와 TIA에서 확인 전입니다. 실제 잔존 요청을 기록합니다.')]),
 'FN04':dict(core=[1965,1809,1964],
   summary='운전 요청 외에 풍량 설정, 90분 지연 정지, TC09 상상한 알람이 요청 Flag 해제 조건입니다. 피드백·인버터 감시는 17초이며 관련 설비 응답 감시는 별도입니다.',
   cases=[
    ('기동 요청이 곧바로 사라짐','Flag.M_FN_04와 ON을 확인한 뒤 FN_04_FAULT·FN04_INV·SET_PERC_FN04=0·Stop_Fan_FN04·MAX_MAX_TC09 조건을 분리해 기록합니다.','1965에서 해당 조건은 OR로 요청 Flag를 리셋합니다. 보존한 과거 부분 시험은 설정0을 직접 주입했습니다. 이번 작업에서 가상 시험을 다시 실행하지 않습니다. 원본1689는 ON일 때 설정을 5~100으로 제한하므로 전체 실행에서 설정0이 언제 도달하는지는 호출·쓰기 순서 확인이 필요합니다.','온도 설정값·인버터 운전 제한·풍량 설정의 실제 유효 범위는 현재 PLC 값과 제작사 자료를 확인합니다.'),
    ('인버터 명령과 실제 운전이 맞지 않음','백업은 Q17.1을 start fn04, Q4.2를 spare_0으로 정의합니다. I28.2 피드백·I28.3 인버터 이상·QW336 속도·IW394 전류를 별도로 추적합니다.','1809의 Tag_74 설정은 S5T#17S입니다. 피드백 없음 또는 인버터 이상이 지속될 때 각 래치와 1965의 요청 해제를 대조합니다.','과거 Q4.2 설명과 현재 Q17.1 주소가 다릅니다. FG59·60의 실제 출력·배선과 대조 전 어느 주소를 현장 명령으로 단정하지 않습니다.'),
    ('약 90분 뒤 팬이 정지함','FN04 피드백이 1인 동안 SC-01·VR03·SC-10·VR04·SC-11·VR05 중 0인 피드백을 찾습니다. 어느 신호가 언제 떨어졌는지 이력을 기록합니다.','1964는 해당 부족 조건에서 Prealarms_FN04와 SD Tag_126(S5T#1H_30M)을 구동합니다. 부족 조건 AND 타이머 상태가 Stop_Fan_FN04를 만들고 1965에서 요청을 해제합니다.','실제 정상 극성·스페어 장치 상태·설비 생략 운전 정책을 확인합니다. 90분을 17초 기동 감시와 혼동하지 않습니다.'),
    ('고장 리셋 후 반복해서 알람이 뜸','리셋 시점의 피드백·인버터 상태와 설정값, 새 기동 요청의 시점을 함께 기록합니다. 입력 원인이 남아 있는지 먼저 확인합니다.','원본 1809의 래치 리셋 경로와 재설정 경로를 각각 확인합니다. 입력 원인 해제·래치 리셋·새 요청 시점의 원본 조건과 승인된 현장 기록을 각각 대조합니다.','원인이 남은 상태에서 리셋을 유지하는 경우의 재기동 정책은 개선 검토 대상으로 남깁니다. 전체 호출·전원 재시작은 별도 확인 전입니다. 과거 부분 시험을 전체 실행의 합격으로 처리하지 않습니다.')])
}
pilots.update({
 'RD01':dict(core=[1931,1936,1939,1787,1788],summary='RD01 구동과 RD01 팬, 투입 금지 신호는 별도 경로입니다. 킬른 본체와 구동모터의 실제 관리 관계는 대응 후보 상태입니다.',cases=[
   ('드럼 요청이 해제됨','RD_01_FAULT·RD01_INV, SET_PERC_FR01=0, 팬 운전 응답, R2_GATE_LOOP_ON·STANDBY_ON 조합을 순서대로 기록합니다.','1936의 요청 리셋과 Start RD01 코일을 함께 추적합니다. 1787의 피드백·인버터 감시 설정은 5초입니다.','팬 출력 Q0.2와 드럼 출력 Q0.1을 분리합니다. UNDER TESTING을 현장 해결책으로 사용하지 않습니다.'),
   ('드럼은 회전하지만 원료 투입이 안 됨','Disable_Load_RD01 경로에서 TC03 저온, 산소 이상·고농도, 대기 모드, TC09 상상한, 가스 박스, R1 Gate ON과 RD01 피드백을 각각 확인합니다.','1931은 투입 금지 조건을 모읍니다. 드럼 회전 요청과 원료 투입 허가는 다른 신호입니다.','HYDROGEN_BOX 명칭과 실물 가스 계통은 별도 확인합니다. 본체 씰·가이드·구동부 이력과 PLC 조건을 합쳐 단정하지 않습니다.')]),
 'MC04':dict(core=[1941,1791,1792,1693,1769],summary='MC04 기동은 VS01 운전 응답과 연동됩니다. 이전·삭제 회로와 현재 토크·피드백 입력을 분리해 추적합니다.',cases=[
   ('하류 스크린 정지와 함께 컨베이어 정지','MC_04_FAULT·MC04_INV, Inputs.VS01 run과 Allarm.Maintenance_ON을 확인합니다.','1941은 VS01 응답 없음 AND 유지보수 신호 없음에서 요청 Flag를 리셋합니다.','Allarm.Maintenance_ON을 다른 경로의 Flag.Maintenance_ON으로 자동 치환하지 않습니다. DB 선언·쓰기 위치를 확인합니다.'),
   ('피드백·토크 이상이 혼재함','I0.6 피드백, I0.7 인버터 이상, I6.5 토크 입력과 Q0.4 기동을 구분합니다.','1791의 감시 설정은 5초입니다. 1792는 제목에 deleted가 있으므로 현재 활성 회로와 구분합니다.','원본 MV04-MC04 아날로그 혼용 사항과 FG24·25를 대조합니다. 토크 입력을 기동 피드백으로 대신 쓰지 않습니다.')]),
 'VS01':dict(core=[1943,1944,1794],summary='VS01 운전 요청과 브레이크 경로는 별도입니다. 브레이크 네트워크는 제목과 OFF 신호를 함께 확인해야 합니다.',cases=[
   ('스크린 요청이 사라짐','VS_01_FAULT·VS01_INV와 Flag.M_VS_01을 확인합니다.','1943에서 두 고장 경로가 요청을 리셋하며 1794의 감시 설정은 2초입니다.','I1.1 피드백·I1.2 이상과 Q0.6 기동을 비교하고 실제 진동·기계적 상태는 별도로 기록합니다.'),
   ('브레이크 표시 또는 출력이 예상과 다름','Start VS01 BRAKE, Braking VS01, OFF, 운전 피드백과 Tag_117을 함께 기록합니다.','1944 제목은 vs01 brake (off)이며 조건은 OFF를 사용합니다. Q49.5는 백업 브레이크 심볼입니다.','네트워크 존재만으로 현장 브레이크가 사용 중이라고 판단하지 않습니다. OFF의 실제 쓰기와 회로 활성 여부를 확인합니다.')]),
 'FN01':dict(core=[1950,1951,1798,1988],summary='FN01은 2초 기동 감시와 90분 지연 정지를 구분합니다. 팬 보조 회로·진동·온도·가스 계통이 함께 연결됩니다.',cases=[
   ('기동이 억제됨','FN_01_FAULT·FN01_INV, SET_PERC_VT01=0, Stop_Fan_FN01, HYDROGEN_BOX_FAULT 조건을 확인합니다.','1951 요청 리셋과 1798의 2초 기동 감시를 추적합니다.','FN01 본체와 보조 팬 FN01F의 I4.5·Q3.5는 별도이며 스페어 상태 불일치를 확인합니다.'),
   ('장시간 운전 후 정지함','TC04·TC05 최대온도, ZT01 진동, VR01·VR02 운전 응답과 Prealarms_FN01을 시각순으로 기록합니다.','1950은 해당 경로를 Tag_122의 1시간 30분 설정과 연결해 Stop_Fan_FN01을 만듭니다.','진동·온도 임계값, TC05 채널·범위, 실제 사용 상태는 현재 설정과 도면으로 확인합니다.')]),
 'FN02':dict(core=[1948,1796,1688,1767,1770],summary='FN02의 기동 요청, 풍량 설정과 아날로그 변환을 분리합니다. FN04 전류 변환과 원본 제목의 혼동을 검토합니다.',cases=[
   ('기동 요청 즉시 해제','FN_02_FAULT·FN02_INV와 Data.Set_Perc_VT02 값을 확인합니다.','1948은 풍량 설정 0을 요청 리셋 조건에 포함합니다. 1796의 감시 설정은 2초입니다.','Q2.3 기동·QW306 설정과 I3.0 피드백·I3.1 이상을 구분합니다.'),
   ('화면의 전류·풍량이 실제 팬과 다름','1767·1770의 실제 입력 피연산자와 변환 대상, HMI 설정 주소를 나란히 비교합니다.','네트워크 제목의 fn-02 aspirator만으로 전류 신호가 FN02라고 판단하지 않습니다.','원본 FN04 변환 제목 불일치 항목과 함께 물리 입력 주소·변환 DB·HMI를 확인합니다.')]),
 'FN03':dict(core=[1954,1801,1866],summary='FN03은 연소 공기와 버너 허가에 연결됩니다. FG51의 물리 피드백은 소프트스타터TOR이며 RUN 접점과 구분합니다. 35초 타이머의 중복 구동과 펄스 접점은 실행 해석이 필요한 항목입니다.',cases=[
   ('운전 피드백 고장 감시가 예상과 다름','FG51의 I4.1은 소프트스타터TOR 단자5에 연결됩니다. RUN 단자4와 같은 시점으로 가정하지 않습니다. 내부FN03 Run, Memo_M25_Running, Tag_66과 Part854·908의 SD 조건을 각각 기록합니다.','1801에는 같은 Tag_66(RefId 95)을 대상으로 한 SD 코일 두 곳과35초 설정이 있습니다. PContact도 포함됩니다.','소프트스타터의 실제 TOR/RUN 기능·램프와 입력 전달을 확인하고 TIA에서 펄스·같은 타이머의 쓰기 순서를 대조합니다.'),
   ('버너 시작과 팬 기동의 연결이 맞지 않음','Flag.M_FN_03과 Flag.Start_Burner·Lock Burner·OFF, Inputs.FN03 Run을 함께 추적합니다.','1866의 FN03 요청 Set 경로에는 OFF가 있으며 버너 허가는 FN03 Run을 사용합니다.','팬과 버너의 독립 운전 정책, 소프트스타터 이상 I4.2의 내부 전달을 확인합니다. 버너 허가를 임의로 강제하지 않습니다.')]),
 'FN06':dict(core=[1955,1802],summary='FN06은 RD01 운전 응답과 연동되며 원본 고장 이름이 다른 장치 명칭으로 나타납니다.',cases=[
   ('드럼 정지 후 보조 팬 요청이 사라짐','Inputs.RD01 run과 UNDER TESTING, Flag.M_FN_06을 확인합니다.','1955는 RD01 응답 없음 AND NOT UNDER TESTING을 요청 리셋 경로로 사용합니다.','설비 간 정지 정책과 실제 RD01 응답 전달을 확인합니다.'),
   ('FN06 고장 표시 이름이 다름','Allarm.MBVA01_FAULT의 Set·Reset과 FN06 요청 리셋을 연결해 봅니다.','1802의 감시 설정은 2초이며 1955는 MBVA01_FAULT를 사용합니다.','태그명만 보고 다른 고장으로 치환하지 않습니다. 알람 이름·HMI 문구·실물 장치의 관계를 확인합니다.')]),
 'PV01':dict(core=[1911,1913,1914,1915,1921,1922,1815,1816],summary='두 게이트의 명령, 열림·닫힘 기억, 선택 스위치와 원료 투입 단계가 분리되어 있습니다.',cases=[
   ('자동 게이트 순서가 진행되지 않음','Flag.Enable_R1_GATE, R1 Gate ON과 WorkData.R1State를 확인하고 명령 Set·Reset을 단계별로 기록합니다.','1913에서 상태 0은 A 닫기, 1은 B 열기, 3은 B 닫기, 4는 A 열기 요청 경로입니다. 상태 전환은 같은 네트워크의 값 전달 조건을 함께 확인합니다.','명령 상태만으로 실제 게이트 위치를 판단하지 않습니다. 단계 번호 2 등의 전환 조건은 전체 원본 명세를 대조합니다.'),
   ('열림·닫힘 알람이 발생함','A·B 명령과 각 MEM_OPEN·MEM_CLOSE, 직접 EV 응답과 내부 Inputs 응답을 분리합니다.','1921·1922의 기억 조건과 1815·1816의 지연·래치 조건을 대조합니다. 1815의 A 감시는 4초입니다.','I8.7(닫힘)과 LS02·SPARE 도면 불일치를 확인합니다. 센서 위치·접점 극성·단자 번호를 임의로 확정하지 않습니다.')]),
 'PV02':dict(core=[1916,1918,1919,1920,1923,1924,1817,1818],summary='PV02 배출 게이트는 MC04 응답과 연결되며 두 게이트의 명령·기억·모드가 별도로 유지됩니다.',cases=[
   ('배출 게이트 운전이 허가되지 않음','MC04_Fbk·Inputs.MC04 run·Allarm.Maintenance_ON, Enable_R2_GATE와 두 NOT_OPEN 알람을 확인합니다.','1916의 PV-02 Gate ON은 MC04 응답 경로, 자동 허가 경로와 두 열림 기억 조건을 조합합니다.','수동·유지보수 경로가 자동 순서를 대신했다고 판단하지 않습니다. 실제 운전 모드를 기록합니다.'),
   ('게이트 동작 후 다음 단계로 안 넘어감','WorkData.W7, A·B 명령, MEM_OPEN·MEM_CLOSE와 EV04·EV05 응답을 시각순으로 기록합니다.','1918의 상태 0·1·3·4 요청과 1923·1924 기억을 확인합니다. 1817의 A 감시는 7초입니다.','Q5.4·Q5.5 출력과 I9.4~I9.7 응답을 도면 FG71·72에 대조합니다. 명령과 위치 센서를 같은 의미로 표시하지 않습니다.')]),
 'MV01':dict(core=[1702,1703,1714,1226,11],summary='MV01은 수동 열기·닫기, 자동 TC03 제어, 리미트와 엔코더 교정이 분리되어 있습니다.',cases=[
   ('한 방향으로 움직이지 않음','수동 Flag·자동 모드, MV01_FAULT, 반대 방향 출력, 해당 리미트와 ResetEncoderProcedure를 확인합니다.','1702는 열기·닫기의 반대 출력과 끝단 응답을 조건으로 사용합니다. 일부 경로에 미해석 ORef가 남아 있습니다.','Q2.4·Q2.5와 I3.2·I3.3 운전 응답, I8.1·I8.2 리미트를 구분하고 미해석 경로를 임의로 채우지 않습니다.'),
   ('표시 개도와 실제 위치가 다름','엔코더 원시값·환산값·설정값과 교정 요청·완료 신호를 함께 기록합니다.','1703 교정과 1714의 WorkData.W33>2000, W34<-2000 고장 경로를 대조합니다.','2000은 원본 수치이며 물리 각도·단위를 뜻한다고 단정하지 않습니다. 실제 변환과 제작사 교정 절차를 확인합니다.')]),
 'MV03':dict(core=[1705,1706,1707,1714,1868,15],summary='MV03은 PSH03 제어와 버너 세정·기동 단계의 요청을 함께 받습니다. 미사용 제어 제목과 실제 연결을 구분합니다.',cases=[
   ('압력 제어 방향이 예상과 반대','ErrPSH03·Tag_148, PID UP/down, 수동 Flag, 버너 세정·닫힘 요청을 확인합니다.','1705에는 오차 >=5와 <-5 방향 조건이 있으며 1706에는 자동·수동·세정·기동 요청이 함께 있습니다.','백업에 연관된 PSH02 주소와 제어 이름 PSH03을 직접 동일시하지 않습니다. 현재 센서·변환·설정 경로를 확인합니다.'),
   ('버너 기동 또는 교정 중 개폐가 멈춤','BR01_State, Open MV03 for washing, Close MV03 for Burner Startup, 양쪽 리미트와 ResetEncoderProcedure를 시각순으로 기록합니다.','1868의 단계 1·4·7 요청, 1707 교정과 1714의 ±3400 경로를 분리해 봅니다.','15번 네트워크 제목에는 not used가 있습니다. 모든 제어 루프가 동시에 사용된다고 판단하지 않습니다.')]),
 'MV06':dict(core=[1709,1711,1714,1760,1766],summary='MV06의 PSH02 제어, ON 반전 접점과 실물 리미트 명칭 불일치를 함께 확인합니다.',cases=[
   ('수동·자동 요청에도 출력이 없음','1711의 첫 접점 NOT ON, MV_06_FAULT, 모드·요청·반대 출력·해당 리미트를 순서대로 확인합니다.','1709는 PSH02_SETPOINT!=0, Tag_150, 오차 >=5 또는 <=-5를 사용합니다. 1711은 NOT ON으로 시작하는 경로입니다.','원본 ON 반전 조건을 자동 수정하지 않습니다. 활성 네트워크·다른 MV06 쓰기·운전 정책을 TIA에서 확인합니다.'),
   ('리미트 또는 위치 고장이 맞지 않음','I6.7 열림·I7.0 닫힘, I1.6·I1.7 운전 응답, 공통 전원·인버터 신호를 나눠 기록합니다.','1714는 WorkData.W19>2200 또는 W20<-2200에서 MV_06_FAULT를 Set합니다.','LS34·35와 LS40·41 도면·백업 차이를 해소하기 전 단자·센서명을 확정하지 않습니다.')]),
 'BR01':dict(core=[1854,1857,1861,1865,1866,1868],summary='일반 PLC의 버너 운전 요청과 전용 연소 제어기의 안전 시퀀스 경계를 구분합니다. 가스·공기·세정·MV03의 연동을 추적합니다.',cases=[
   ('버너 시작 허가가 형성되지 않음','Flag.Start_Burner, Lock Burner, Inputs.FN03 Run, Enable start burner(1)와 Enable start burner를 나눠 기록합니다.','1866은 시작 Flag AND NOT Lock Burner AND FN03 Run을 허가 경로에 사용합니다. 최종 원격 Start/Stop은 추가 허가와 AND입니다.','I17.0 Burner On, I17.1 Lock out, I17.2 On and OK를 구분합니다. 전용 버너 도면·제어기 매뉴얼은 추가 확인 대상입니다.'),
   ('세정·댐퍼 단계에서 기동이 멈춤','WorkData.BR01_State, MV03 열림·닫힘, 세정 요청·기동 닫힘 요청과 타이머를 단계별로 기록합니다.','1868의 상태 1·4·7·11 동작과 1857의 가스 시험 경로를 확인합니다. 원본 Add 등 값 전달 명령과 상태 전환은 정적 조건만으로 실행 확정하지 않습니다.','화염·가스밸브의 안전 시간과 정상 절차를 일반 PLC의 단계명만으로 만들어내지 않습니다. 제작사 자료와 전용 회로를 확인합니다.')])
})

for s in specs:
    id=s['id'];linked=[network_map[int(n['문서 ID'])] for n in s['networks'] if int(n['문서 ID']) in network_map]
    pilot=pilots.get(id)
    body='<p class="eyebrow">근거 기반 진단 작업지 · 2026-10-07</p><h1>'+e(id+' · '+s['name'])+'</h1><p>'+e(s['role'])+'</p><div class="notice">원본 백업·도면의 자료를 연결한 검토본입니다. 현재 운전 상태, 단자 측정 결과, 실제 정상 극성, 전체 PLC 실행은 확인 전입니다. 현장 작업은 설비의 승인된 정지·전원 격리 절차에 따라 수행합니다.</div>'
    if id.startswith('EV') and id[2:].isdigit() and 1<=int(id[2:])<=90:body+='<div class="notice">'+id+'는 EV01~EV90 매뉴얼 작성 제외 범위 · 사용자 제공(2026-10-09). 별도 요청 전 상세 조사·새 설명/수리 절차를 추가하지 않습니다. 아래는 보존된 과거 자료입니다. 현재 실물/용도 검증 결과가 아닙니다.</div>'
    if id in ['SC12','PV04']:body+='<div class="notice">'+id+('는 현장 없음' if id=='SC12' else '는 사용 계획 없음')+' · 사용자 제공(2026-10-09). 현재 상세 조사·매뉴얼 보강에서 제외합니다. 아래는 보존된 과거 백업·도면 자료입니다. 부모 현장 검증 미실시.</div>'
    if id=='MV04':body+='<div class="notice">MV04는 철거됨 · 사용자 제공(2026-10-09). 현재 상세 조사 대상에서 제외합니다. 아래는 보존된 과거 백업·도면의 참고 자료이며 현행 점검·재기동 대상으로 사용하지 않습니다. 현장 실물 검증 미실시.</div>'
    body+='<nav class="inline-actions"><a href="../devices/'+e(id)+'.html">기존 설비 매뉴얼</a><a href="../control-specs/'+e(id)+'.html">전체 제어 명세</a>'+''.join('<a href="../sources/Electrical_Rev2.pdf#page='+str(pdfpage(f))+'">FG '+e(f)+' / PDF '+str(pdfpage(f))+'</a>' for f in s['electrical_fgs'])+'</nav>'
    if id in ['CC01','AB01','HE01']:body+='<div class="inline-actions"><a href="../body-manual.html#body-'+id+'">본체·공정/계측 경계·증상별 수리 근거</a></div>'
    if (ROOT/'circuit-guides'/(id+'.html')).exists():
        body+='<div class="inline-actions"><a href="../circuit-guides/'+e(id)+'.html">도면 시각 확인 · 단자·릴레이·신호 경로</a></div>'
    if (ROOT/'construction-guides'/(id+'.html')).exists():
        body+='<div class="inline-actions"><a href="../construction-guides/'+e(id)+'.html">추가 시공도면 · 케이블·접속함·배관 경로</a></div>'
    if id in ['BC01','FN04','RD01','MC04','VS01','FN01','FN02','FN03','FN06','PV01','PV02','MV01','MV03','MV06']:
        body+='<div class="inline-actions"><a href="../alarm-guides/'+e(id)+'.html">알람 발생·리셋·재기동 · 원본 접점 비교</a></div>'
    if id in ['MV01','MV02','MV03','MV05','MV06']:body+='<div class="inline-actions"><a href="../encoder-position.html#position-'+id+'">엔코더·위치·교정 수리 근거</a></div>'
    body+='<div class="inline-actions"><a href="../hmi-transfer.html#tags">HMI 전체 태그·설정·표시 전달 확인</a><a href="../recipe-settings.html#repair">레시피·설정값·초기화의 공통 진단</a></div>'
    loops_for={'FN04':['FN04'],'MV01':['MV01'],'MV02':['MV02'],'MV03':['MV03'],'MV05':['MV05'],'MV06':['MV06'],'FN02':['VT02'],'BR01':['BR01','STECHIO'],'TC01':['BR01'],'TC02':['BR01'],'TC03':['MV01','VT02'],'PSH01':['MV02'],'PSH02':['MV06','MV03'],'PSH03':['MV03'],'PC01':['FN04'],'RO01':['MV05']}.get(id,[])
    if loops_for:body+='<div class="inline-actions">'+''.join('<a href="../regulation-manual.html#loop-'+key+'">'+key+' 조절 루프 수리·구조 근거</a>' for key in loops_for)+'</div>'
    if id in ['TC01','TC02','TC03','TC04','TC05','TC06','TC07','TC09','TC10','PSH01','PSH02','PSH03','PC01','DP01','DP02','RO01','RO02','RO03','RO04','BR01']:body+='<div class="inline-actions"><a href="../sensor-measurement.html'+('' if id=='BR01' else '#sensor-'+id)+'">온도·압력·산소 입력·환산·수리 근거</a></div>'
    if id=='BR01':body+='<div class="inline-actions"><a href="../measurement-trace.html">가스·공기 환산·출력 추적</a></div>'
    if id in ['BR01','TC01','TC02','TC03','TC04','TC05','TC09','PC01','RO01','RO02']:body+='<div class="inline-actions"><a href="../process-stop-alarms.html">관련 공정 알람·버너 정지 원인 근거</a></div>'
    if id in ['BR01','MV03']:body+='<div class="inline-actions"><a href="../burner-interface.html">BR01 외부 연동·정지·복구 및 MV03 요청 근거</a></div>'
    body+='<h2>1. 증상 기록과 조사 범위</h2><ol><li>설비 ID·실물 명판·제어반·도면 위치를 기록하고 본체와 모터를 구분합니다.</li><li>발생 시각, 자동·수동 모드, 운전 요청, 출력 명령, 실제 응답, 최초 알람과 후속 알람을 순서대로 기록합니다.</li><li>PLC 백업 버전과 현장 CPU의 프로그램 일치 여부를 확인합니다. 과거 주석 주소를 현재 주소 대신 사용하지 않습니다.</li><li>공유 네트워크와 상위 허가의 영향을 함께 확인하고 원본 매뉴얼·도면·래더의 위치를 기록합니다.</li></ol>'
    body+='<h2>2. 입력·출력의 구간별 확인</h2>'+table(['구분','백업 주소·심볼','원문 설명','확인할 구간'],[[e(kind),'<code>'+e(v['백업 주소'].upper())+' · '+e(v['원본 심볼'])+'</code>',e(v['설명']),e('센서·접점 → 단자·배선 → PLC 입력 → 내부 DB 전달' if kind=='입력' else '요청·인터록 → PLC 출력 → 구동·전용 제어기 → 실제 장치 응답')] for kind,rows in [('입력',s['inputs']),('출력',s['outputs'])] for v in rows])
    body+='<p>측정값·정상 기준·판정·사진·측정 위치를 기록합니다. 도면에서 직접 확인하지 않은 단자 번호, 장치 정격과 알람 임계값은 임의로 채우지 않습니다.</p>'
    if (ROOT/'signal-guides'/(id+'.html')).exists():body+='<p><a href="../signal-guides/'+e(id)+'.html">PLC 신호 전달·반전·복수 쓰기 분석</a></p>'
    if (ROOT/'common-control.html').exists():body+='<p><a href="../common-control.html">공통 운전 허가·자동 요청·알람·리셋 매뉴얼</a></p>'
    for p in json.loads((ROOT/'registers/all-in-one-data.json').read_text())['priority']:
        if p['plc_id']==id and (ROOT/'repair-guides'/(p['key']+'.html')).exists():body+='<p><a href="../repair-guides/'+p['key']+'.html">수리 판단·공통 영향 통합 작업지</a></p>'
    if pilot:
        body+='<h2>3. 원본에서 확인한 핵심 동작</h2><p>'+e(pilot['summary'])+'</p>'+table(['증상','확인 순서','원본 로직·확인 범위','추가 확인'],[[e(v) for v in row] for row in pilot['cases']])
        chosen=[network_map[n] for n in pilot['core']]
    else:
        if s['kind']=='passive':
            body+='<h2>3. 본체 점검과 제어 경계</h2><p>이 항목은 직접 제어 출력·전용 래더가 식별되지 않은 본체 자료입니다. 주변 모터·밸브·센서와 같은 설비라고 병합하거나 기동 순서를 임의로 부여하지 않습니다.</p><ol><li>본체 명판·설치 위치·P&ID 연결, 투입·배출·가스·공기 계통을 대조합니다.</li><li>외관, 체결·씰·연결부, 누설·막힘·온도·압력·소음 등의 관찰을 시각·위치·사진과 함께 기록합니다.</li><li>주변 센서·구동부와 제어반의 관계를 확인하고 이상 시 최초 원인과 후속 정지를 구분합니다.</li><li>교체품 규격·재질·조임값·허용 온도·압력과 내부 점검 절차는 제작사 도면·승인된 현장 절차로 확인합니다.</li></ol>'
            if id in ('CC01','AB01','HE01'):
                body+='<div class="notice">이 본체는 디코팅 배치도 설비와의 공정 역할 대응 후보입니다. 실물 동일성 확인과 기계·전용 제어 자료가 필요합니다.</div>'
        else:
            body+='<h2>3. 증상에서 로직으로 추적</h2><ol><li>요청이 없으면 HMI 명령·모드·초기화와 요청 Flag의 다른 쓰기 위치를 확인합니다.</li><li>요청은 있는데 출력이 없으면 아래 코일·값 전달 조건과 공유 허가를 한 항목씩 비교합니다.</li><li>출력이 있는데 응답이 없으면 장치 전원·운전 허가·릴레이·구동기·센서 전달 구간을 도면과 대조합니다.</li><li>운전 중 정지하면 최초 고장 입력, 타이머 완료, 단계 전환과 요청 Flag 리셋을 시각순으로 비교합니다.</li></ol>'
        chosen=[n for n in linked if n['actions'] and id.replace('-','').casefold() in n['title'].replace('-','').replace(' ','').casefold()]
        if not chosen:chosen=[n for n in linked if n['actions']][:4]
        body+='<div class="notice">아래는 관련·공유 네트워크의 조건입니다. 전용 로직이라고 단정하지 않으며 대상 신호를 대조합니다. 상세 증상별 원인 확정은 추가 분석 중입니다.</div>'
    body+='<h2>4. 읽기·쓰기 조건과 타이머 근거</h2>'+table(['블록·근거','명령·대상','조건','값·시간','정적 해석 범위'],[[e(n['block'])+' · '+netlink(n['id']),e(a['gate'])+'<br><code>'+e(a['name'])+'</code>','<code>'+e(expression(a['condition']))+'</code>',e(expression(a['preset'])) if 'preset' in a else e(expression(a['value'])) if 'value' in a else '',e('지원 명령으로 정적 해석 / TIA 검증 전' if n['executable'] else '정적 해석 제약: '+' / '.join(n['blockers']))] for n in chosen for a in n['actions']])
    if not chosen:body+='<p>직접 쓰기 조건은 식별되지 않았습니다. 주변 설비와 센서의 실제 연결을 확인한 뒤 근거를 추가합니다.</p>'
    if s['sequence']:
        body+='<h3>단계·상태에 연결된 원본 정적 경로</h3><p>아래 경로는 단계 전환과 관련된 원본 참조입니다. 실행 순서를 확정한 표는 아니며 공유 경로가 포함됩니다.</p>'+table(['근거·Part','대상·명령','원본 조건','내용'],[[netlink(a['네트워크 문서'])+' / '+e(a['Part UID']),e(a['대상'])+'<br>'+e(a['동작']),'<code>'+e(a['정적 조건식'])+'</code>',e(a['내용'])] for a in s['sequence']])
    body+='<h2>5. 복구와 재기동 확인</h2><ol><li>원인 입력과 실제 장치 이상이 복구됐는지 별도로 확인합니다.</li><li>래치 해제 조건을 원본에서 확인하고 Reset 펄스·유지 상태를 구분해 기록합니다.</li><li>운전 요청 Flag, 단계 기억, 타이머·재시도 상태가 남는지 확인합니다.</li><li>정지 상태에서 허가를 확인한 뒤 승인된 새 기동 절차로 응답·출력·알람을 관찰합니다.</li><li>정상·고장·복구·전원 재시작을 분리해 결과를 남깁니다. 보존한 과거 가상 시험 결과와 실제 수리 완료를 구분합니다. 추가 가상 시험은 중지 상태입니다.</li></ol>'
    body+='<h2>6. 개선 검토와 남은 확인</h2><ul>'+''.join('<li>'+e(p)+'</li>' for p in s['pending'])+'</ul><p>개선 후보는 문제 조건·원본 위치·변경 전후 기대 동작·회귀 시험·현장 확인 기준으로 기록합니다. 타이머 축소, 인터록 삭제, 신호 강제와 자동 재기동은 근거와 승인된 운전 정책을 확인한 뒤 판단합니다.</p>'
    if s['source_conflicts']:body+='<h3>관련 자료 불일치</h3>'+table(['ID·항목','자료 내용','다음 확인'],[[e(c['ID']+' · '+c['확인 항목']),e(c['자료 내용']),e(c['다음 검증'])] for c in s['source_conflicts']])
    body+='<h2>7. 결과 기록 양식</h2>'+table(['항목','기록 내용'],[[e(k),e(v)] for k,v in [('발생 조건','시각 / 모드 / 단계 / 최초 증상'),('입출력 확인','명령 / 출력 / 피드백 / 이상 입력 / 정상 기준'),('근거','FG·PDF 페이지 / 블록 / 네트워크 / Part·주소'),('원인과 조치','관찰 사실 / 원인 후보 / 수행한 조치'),('복구 시험','원인 해제 / Reset / 재요청 / 연동 영향'),('확인 상태','원본 해석 / 과거 가상 시험 기록 / TIA 실행 / 현장 측정의 구분')]])
    document='<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+e(id)+' 진단·수리 작업지</title><link rel="stylesheet" href="../assets/all-in-one.css"></head><body><main style="max-width:1240px;margin:auto;padding:24px">'+body+'</main></body></html>'
    (out/(id+'.html')).write_text(document)
coverage=dict(date='2026-10-07',procedures=len(specs),detailed_devices=list(pilots),detailed_device_count=len(pilots),detailed_symptom_cases=sum(len(p['cases']) for p in pilots.values()),source_linked=True,field_verified=0,remaining_scope='Other items have source-linked baseline worksheets. Terminal tracing, native execution and field recovery confirmation remain separate.',priority_passive_candidates=['CC01','AB01','HE01'])
(ROOT/'registers/diagnostic-coverage.json').write_text(json.dumps(coverage,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(coverage,ensure_ascii=False))
