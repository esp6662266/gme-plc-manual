# BWF01 · 현재 보존 원본 검토

## 1. 설비·자료 기준

BWF01(고객 설비 계량 피더)는 실제 대장에서 외부 연동 설비으로 분류합니다. 별도 부모 ID는 배정되어 있지 않습니다.

외부 피더의 준비·운전·고장·레벨·유량과 원격 운전 허가를 교환한다.

외부 인터페이스 범위입니다. 명령·피드백·상태 원본 참조만으로 고객 모터의 배선·내부 인터록·현재 실물 동일성을 확정하지 않습니다. OEM은 OK 인터페이스를 MANU STATUS로 표시합니다. 원시 운전·고장·레벨 및 기동 허가가 고객 내부 자동 모드나 안전 상태의 확정은 아닙니다. 보존된 과거 Simulation 가공값 쓰기는 정적 참조입니다.

외부 인터페이스 범위입니다. 명령·피드백·상태 원본 참조만으로 고객 모터의 배선·내부 인터록·현재 실물 동일성을 확정하지 않습니다. OEM은 OK 인터페이스를 MANU STATUS로 표시합니다. 원시 운전·고장·레벨 및 기동 허가가 고객 내부 자동 모드나 안전 상태의 확정은 아닙니다. 보존된 과거 Simulation 가공값 쓰기는 정적 참조입니다.

Dots 상담에서 기존 완성 초안이 없음을 확인했습니다. 아래는 현재 보존 원본을 독립 대조한 Codex 검토본입니다.

## 2. I/O·HMI

BWF01 대장에는 입력·출력·내부 신호 11행과 HMI 설정 7행이 연결됩니다.

- bwf1_inverter_high_speed — %i14.4 / bool / 원본 문서531; 원본 검색 색인 Name/Address 근거 · 같은 이름의 복원 XML 주소 선언 미확보; 같은 이름 LAD 핀 0곳. 원문 설명: e 17.0 bwf1_inverter_high_speed
- bwf01 ok — %i11.1 / bool / 원본 문서959; 원본 XML의 SAD/SSD·자료형 및 백업 주소 대응 확인; 같은 이름 LAD 핀 0곳. 원문 설명: e 64.0 bwf 01 manu status
- bwf01 fault — %i11.3 / bool / 원본 문서960; 원본 XML의 SAD/SSD·자료형 및 백업 주소 대응 확인; 같은 이름 LAD 핀 0곳. 원문 설명: e 64.2 bwf 01 fault
- min lev bwf01 — %i11.4 / bool / 원본 문서961; 원본 XML의 SAD/SSD·자료형 및 백업 주소 대응 확인; 같은 이름 LAD 핀 0곳. 원문 설명: e 64.3 bwf 01 minimum level
- max lev bwf01 — %i11.5 / bool / 원본 문서962; 원본 XML의 SAD/SSD·자료형 및 백업 주소 대응 확인; 같은 이름 LAD 핀 0곳. 원문 설명: e 64.4 bwf 01maximum level
- bwf01 pulse — %i20.1 / bool / 원본 문서1520; 원본 XML의 SAD/SSD·자료형 및 백업 주소 대응 확인; 같은 이름 LAD 핀 1곳. 원문 설명: old address
- bwf01_level — %iw268 / int / 원본 문서1548; 원본 XML의 SAD/SSD·자료형 및 백업 주소 대응 확인; 같은 이름 LAD 핀 2곳. 원문 설명: level bwf 01 (client machine)
- bwf 01 run — %i11.2 / bool / 원본 문서1551; 원본 XML의 SAD/SSD·자료형 및 백업 주소 대응 확인; 같은 이름 LAD 핀 2곳. 원문 설명: e 64.1 bwf 01 run
- bwf01_flowrate — %iw264 / int / 원본 문서1553; 원본 XML의 SAD/SSD·자료형 및 백업 주소 대응 확인; 같은 이름 LAD 핀 2곳. 원문 설명: flow rate bwf 01(client machine)
- bwf01_sp_flowrate — %qw298 / word / 원본 문서1356; 원본 XML의 SAD/SSD·자료형 및 백업 주소 대응 확인; 같은 이름 LAD 핀 2곳. 원문 설명: flow rate speed set bwf 01(client machine)(4-20ma)
- consent start bwf01 — %q6.2 / bool / 원본 문서1666; 원본 XML의 SAD/SSD·자료형 및 백업 주소 대응 확인; 같은 이름 LAD 핀 6곳. 원문 설명: a 61.7 bwf 01 remotestart
- Editor_BWF01 — DB26,INT8 / Access Name PLC / 내부 ID 00417; HMI 설정 주소와 물리 I/O를 구분
- BWF01\Risposta — DB11,X70.1 / Access Name PLC / 내부 ID 000EC; HMI 설정 주소와 물리 I/O를 구분
- BWF01\StatusOK — DB11,X70.0 / Access Name PLC / 내부 ID 000EA; HMI 설정 주소와 물리 I/O를 구분
- BWF01\Allarme1 — DB11,X70.2 / Access Name PLC / 내부 ID 000E9; HMI 설정 주소와 물리 I/O를 구분
- BWF01\Flag — DB2,X12.0 / Access Name PLC / 내부 ID 000E8; HMI 설정 주소와 물리 I/O를 구분
- I_Level_BWF01 — DB13,INT32 / Access Name PLC / 내부 ID 0005D; HMI 설정 주소와 물리 I/O를 구분
- I_Flow_rate_BWF01 — DB13,INT28 / Access Name PLC / 내부 ID 0005C; HMI 설정 주소와 물리 I/O를 구분

| 원문 신호 | 백업 주소 | 형식 | 주소 증거 |
| --- | --- | --- | --- |
| bwf1_inverter_high_speed | %i14.4 | bool | Address 색인; native 선언 미확보 |
| bwf01 ok | %i11.1 | bool | native 선언 일치 |
| bwf01 fault | %i11.3 | bool | native 선언 일치 |
| min lev bwf01 | %i11.4 | bool | native 선언 일치 |
| max lev bwf01 | %i11.5 | bool | native 선언 일치 |
| bwf01 pulse | %i20.1 | bool | native 선언 일치 |
| bwf01_level | %iw268 | int | native 선언 일치 |
| bwf 01 run | %i11.2 | bool | native 선언 일치 |
| bwf01_flowrate | %iw264 | int | native 선언 일치 |
| bwf01_sp_flowrate | %qw298 | word | native 선언 일치 |
| consent start bwf01 | %q6.2 | bool | native 선언 일치 |

## 3. 제어 구조

외부 인터페이스 범위입니다. 명령·피드백·상태 원본 참조만으로 고객 모터의 배선·내부 인터록·현재 실물 동일성을 확정하지 않습니다. OEM은 OK 인터페이스를 MANU STATUS로 표시합니다. 원시 운전·고장·레벨 및 기동 허가가 고객 내부 자동 모드나 안전 상태의 확정은 아닙니다. 보존된 과거 Simulation 가공값 쓰기는 정적 참조입니다.

GME 네트워크1932의 Consent Start BWF01 출력은 ON AND Flag.M_BWF01입니다. 요청 Reset 조건에는 전용 고장·제어 고장, Data.SET_PERC_BWF01=0, NOT 전용 OK, NOT BC01 run 및 Disable_Load_RD01이 포함됩니다. 정확한 분기와 반전은 원본으로 유지합니다.

제어 속도 고장 네트워크1820은 원본 OFF 허가를 사용합니다. 네트워크1680의 소프트웨어 백분율 제한은0 또는100을 기록하며 실제 피더 용량이나 교정값을 확정하지 않습니다.

OEM FG85/PDF86 아날로그 인터페이스는 유량·레벨·속도 설정 배선을4-20mA로 표시합니다. 원시 I/O·Inputs 가공·공학 환산 계수·출력 스케일을 다른 단계로 추적합니다.

- 원시 이름의 핀 참조를 확인한 네트워크: 1071, 1681, 1735, 1737, 1776, 1781, 1782, 1849, 1932. 읽기·쓰기·호출은 원본 Part/Wire/ORef 표로 구분합니다.
- 원본 정적 조건 1932:109 / RCoil / Flag.M_BWF01: ((ON AND Allarm.BWF01_FAULT) OR (ON AND Allarm.BWF01_Fault_Control) OR (ON AND [Data.SET_PERC_BWF01 = 0]) OR (ON AND NOT [Inputs.BWF01 OK]) OR (ON AND NOT [Inputs.BC01 run]) OR (ON AND Disable_Load_RD01)); 현재 호출·실행·최종값 확인 전
- 원본 정적 조건 1932:113 / Coil / Consent Start BWF01: (ON AND Flag.M_BWF01); 현재 호출·실행·최종값 확인 전

| 고유/관련 원문 이름 | 원본 네트워크 | 명령 UID·Gate·Pin | Wire·ORef | 소유 경계 |
| --- | --- | --- | --- | --- |
| BWF01 Pulse | 1776 | 1774 Contact.operand | 1745 / 1722 | 외부 인터페이스 범위입니다. 명령·피드백·상태 원본 참조만으로 고객 모터의 배선·내부 인터록·현재 실물 동일성을 확정하지 않습니다. OEM은 OK 인터페이스를 MANU STATUS로 표시합니다. 원시 운전·고장·레벨 및 기동 허가가 고객 내부 자동 모드나 안전 상태의 확정은 아닙니다. 보존된 과거 Simulation 가공값 쓰기는 정적 참조입니다. |
| BWF01_Level | 1071 | 48 Move.in | 61 / 52 | 외부 인터페이스 범위입니다. 명령·피드백·상태 원본 참조만으로 고객 모터의 배선·내부 인터록·현재 실물 동일성을 확정하지 않습니다. OEM은 OK 인터페이스를 MANU STATUS로 표시합니다. 원시 운전·고장·레벨 및 기동 허가가 고객 내부 자동 모드나 안전 상태의 확정은 아닙니다. 보존된 과거 Simulation 가공값 쓰기는 정적 참조입니다. |
| BWF01_Level | 1737 | 276 CRef.Analog_input | 291 / 284 | 외부 인터페이스 범위입니다. 명령·피드백·상태 원본 참조만으로 고객 모터의 배선·내부 인터록·현재 실물 동일성을 확정하지 않습니다. OEM은 OK 인터페이스를 MANU STATUS로 표시합니다. 원시 운전·고장·레벨 및 기동 허가가 고객 내부 자동 모드나 안전 상태의 확정은 아닙니다. 보존된 과거 Simulation 가공값 쓰기는 정적 참조입니다. |
| BWF 01 RUN | 1735 | 262 Contact.operand | 241 / 222 | 외부 인터페이스 범위입니다. 명령·피드백·상태 원본 참조만으로 고객 모터의 배선·내부 인터록·현재 실물 동일성을 확정하지 않습니다. OEM은 OK 인터페이스를 MANU STATUS로 표시합니다. 원시 운전·고장·레벨 및 기동 허가가 고객 내부 자동 모드나 안전 상태의 확정은 아닙니다. 보존된 과거 Simulation 가공값 쓰기는 정적 참조입니다. |
| BWF 01 RUN | 1735 | 264 Contact.operand | 250 / 229 | 외부 인터페이스 범위입니다. 명령·피드백·상태 원본 참조만으로 고객 모터의 배선·내부 인터록·현재 실물 동일성을 확정하지 않습니다. OEM은 OK 인터페이스를 MANU STATUS로 표시합니다. 원시 운전·고장·레벨 및 기동 허가가 고객 내부 자동 모드나 안전 상태의 확정은 아닙니다. 보존된 과거 Simulation 가공값 쓰기는 정적 참조입니다. |
| BWF01_FlowRate | 1071 | 34 Move.in | 38 / 35 | 외부 인터페이스 범위입니다. 명령·피드백·상태 원본 참조만으로 고객 모터의 배선·내부 인터록·현재 실물 동일성을 확정하지 않습니다. OEM은 OK 인터페이스를 MANU STATUS로 표시합니다. 원시 운전·고장·레벨 및 기동 허가가 고객 내부 자동 모드나 안전 상태의 확정은 아닙니다. 보존된 과거 Simulation 가공값 쓰기는 정적 참조입니다. |
| BWF01_FlowRate | 1735 | 185 CRef.Analog_input | 236 / 216 | 외부 인터페이스 범위입니다. 명령·피드백·상태 원본 참조만으로 고객 모터의 배선·내부 인터록·현재 실물 동일성을 확정하지 않습니다. OEM은 OK 인터페이스를 MANU STATUS로 표시합니다. 원시 운전·고장·레벨 및 기동 허가가 고객 내부 자동 모드나 안전 상태의 확정은 아닙니다. 보존된 과거 Simulation 가공값 쓰기는 정적 참조입니다. |
| BWF01_SP_FlowRate | 1681 | 240 Move.out1 | 281 / 260 | 외부 인터페이스 범위입니다. 명령·피드백·상태 원본 참조만으로 고객 모터의 배선·내부 인터록·현재 실물 동일성을 확정하지 않습니다. OEM은 OK 인터페이스를 MANU STATUS로 표시합니다. 원시 운전·고장·레벨 및 기동 허가가 고객 내부 자동 모드나 안전 상태의 확정은 아닙니다. 보존된 과거 Simulation 가공값 쓰기는 정적 참조입니다. |
| BWF01_SP_FlowRate | 1681 | 323 Move.out1 | 349 / 334 | 외부 인터페이스 범위입니다. 명령·피드백·상태 원본 참조만으로 고객 모터의 배선·내부 인터록·현재 실물 동일성을 확정하지 않습니다. OEM은 OK 인터페이스를 MANU STATUS로 표시합니다. 원시 운전·고장·레벨 및 기동 허가가 고객 내부 자동 모드나 안전 상태의 확정은 아닙니다. 보존된 과거 Simulation 가공값 쓰기는 정적 참조입니다. |
| Consent Start BWF01 | 1781 | 119 Contact.operand | 100 / 88 | 외부 인터페이스 범위입니다. 명령·피드백·상태 원본 참조만으로 고객 모터의 배선·내부 인터록·현재 실물 동일성을 확정하지 않습니다. OEM은 OK 인터페이스를 MANU STATUS로 표시합니다. 원시 운전·고장·레벨 및 기동 허가가 고객 내부 자동 모드나 안전 상태의 확정은 아닙니다. 보존된 과거 Simulation 가공값 쓰기는 정적 참조입니다. |
| Consent Start BWF01 | 1782 | 152 Contact.operand | 134 / 123 | 외부 인터페이스 범위입니다. 명령·피드백·상태 원본 참조만으로 고객 모터의 배선·내부 인터록·현재 실물 동일성을 확정하지 않습니다. OEM은 OK 인터페이스를 MANU STATUS로 표시합니다. 원시 운전·고장·레벨 및 기동 허가가 고객 내부 자동 모드나 안전 상태의 확정은 아닙니다. 보존된 과거 Simulation 가공값 쓰기는 정적 참조입니다. |
| Consent Start BWF01 | 1849 | 61 Contact.operand | 60 / 62 | 외부 인터페이스 범위입니다. 명령·피드백·상태 원본 참조만으로 고객 모터의 배선·내부 인터록·현재 실물 동일성을 확정하지 않습니다. OEM은 OK 인터페이스를 MANU STATUS로 표시합니다. 원시 운전·고장·레벨 및 기동 허가가 고객 내부 자동 모드나 안전 상태의 확정은 아닙니다. 보존된 과거 Simulation 가공값 쓰기는 정적 참조입니다. |
| Consent Start BWF01 | 1849 | 109 Contact.operand | 115 / 116 | 외부 인터페이스 범위입니다. 명령·피드백·상태 원본 참조만으로 고객 모터의 배선·내부 인터록·현재 실물 동일성을 확정하지 않습니다. OEM은 OK 인터페이스를 MANU STATUS로 표시합니다. 원시 운전·고장·레벨 및 기동 허가가 고객 내부 자동 모드나 안전 상태의 확정은 아닙니다. 보존된 과거 Simulation 가공값 쓰기는 정적 참조입니다. |
| Consent Start BWF01 | 1849 | 117 Contact.operand | 122 / 119 | 외부 인터페이스 범위입니다. 명령·피드백·상태 원본 참조만으로 고객 모터의 배선·내부 인터록·현재 실물 동일성을 확정하지 않습니다. OEM은 OK 인터페이스를 MANU STATUS로 표시합니다. 원시 운전·고장·레벨 및 기동 허가가 고객 내부 자동 모드나 안전 상태의 확정은 아닙니다. 보존된 과거 Simulation 가공값 쓰기는 정적 참조입니다. |
| Consent Start BWF01 | 1932 | 113 Coil.operand | 143 / 125 | 외부 인터페이스 범위입니다. 명령·피드백·상태 원본 참조만으로 고객 모터의 배선·내부 인터록·현재 실물 동일성을 확정하지 않습니다. OEM은 OK 인터페이스를 MANU STATUS로 표시합니다. 원시 운전·고장·레벨 및 기동 허가가 고객 내부 자동 모드나 안전 상태의 확정은 아닙니다. 보존된 과거 Simulation 가공값 쓰기는 정적 참조입니다. |

| 원본 | 명령 UID·동작 | 대상 | 정적 Wire 조건 · 현재 실행 별도 |
| --- | --- | --- | --- |
| 935 | 311 Move | Data.BWF01_count_rep | PBox UID 306.out (블록 동작 확인) |
| 1071 | 34 Move | Inputs.Flow_rate_BWF01 | Move UID 27.eno (블록 동작 확인) |
| 1071 | 48 Move | Inputs.Level_BWF01 | POWER |
| 1679 | 107 Move | Data.SET_PERC_BWF01 | (ON AND [Prod_h < 0.0]) |
| 1680 | 121 Move | Data.SET_PERC_BWF01 | (ON AND [Data.SET_PERC_BWF01 < 0]) |
| 1680 | 129 Move | Data.SET_PERC_BWF01 | (ON AND [Data.SET_PERC_BWF01 > 100]) |
| 1681 | 240 Move | BWF01_SP_FlowRate | Div UID 236.eno (블록 동작 확인) |
| 1681 | 323 Move | BWF01_SP_FlowRate | Div UID 356.eno (블록 동작 확인) |
| 1781 | 80 SCoil | Allarm.BWF01_FAULT | ((((ON AND Consent Start BWF01) AND Tag_49) AND NOT [Inputs.BWF 01 RUN]) OR ((ON AND Consent Start BWF01) AND Inputs.BWF01 FAULT)) |
| 1781 | 86 RCoil | Allarm.BWF01_FAULT | (((ON AND Flag.RESET_ALLARM) AND Allarm.BWF01_FAULT) AND NOT [Inputs.BWF01 FAULT]) |
| 1782 | 105 SCoil | Allarm.BWF01_min_LEVEL | ((ON AND Consent Start BWF01) AND Inputs.min LEV BWF01) |
| 1782 | 109 SCoil | Allarm.BWF01_MAX_LEVEL | (ON AND Inputs.MAX LEV BWF01) |
| 1782 | 117 RCoil | Allarm.BWF01_min_LEVEL | ((ON AND Flag.RESET_ALLARM) AND NOT [Inputs.min LEV BWF01]) |
| 1782 | 121 RCoil | Allarm.BWF01_MAX_LEVEL | ((ON AND Flag.RESET_ALLARM) AND NOT [Inputs.MAX LEV BWF01]) |
| 1820 | 1780 SCoil | Allarm.BWF01_Fault_Control | ((OFF AND NOT [Inputs.BWF1_INVERTER_HIGH_SPEED]) AND Tag_90) |
| 1820 | 1801 RCoil | Allarm.BWF01_Fault_Control | (((OFF AND Flag.RESET_ALLARM) AND Allarm.BWF01_Fault_Control) AND Inputs.BWF1_INVERTER_HIGH_SPEED) |
| 1932 | 109 RCoil | Flag.M_BWF01 | ((ON AND Allarm.BWF01_FAULT) OR (ON AND Allarm.BWF01_Fault_Control) OR (ON AND [Data.SET_PERC_BWF01 = 0]) OR (ON AND NOT [Inputs.BWF01 OK]) OR (ON AND NOT [Inputs.BC01 run]) OR (ON AND Disable_Load_RD01)) |
| 1932 | 113 Coil | Consent Start BWF01 | (ON AND Flag.M_BWF01) |
| 1934 | 170 RCoil | Flag.M_BWF01 | (((OFF AND Flag.M_BWF01) OR (OFF AND Flag.M_BWF02)) AND Tag_114) |
| 1934 | 210 RCoil | Flag.M_BWF01 | RCoil UID 228.out (블록 동작 확인) |

## 4. 전기 전달 경로

선택한 OEM 원본 위치는 FG84/PDF85, FG85/PDF86, FG86/PDF87, FG91/PDF92입니다. 도면 FG와 PDF 페이지를 별도 필드로 유지합니다.

P&ID에서 이 고유 ID의 독립된 정확한 태그는 확인하지 못했습니다. 대장 pid 표시는 전용 I/O·회로 근거가 아닙니다.

- OEM FG85/PDF86 아날로그 인터페이스는 유량·레벨·속도 설정 배선을4-20mA로 표시합니다. 원시 I/O·Inputs 가공·공학 환산 계수·출력 스케일을 다른 단계로 추적합니다.
- bwf1_inverter_high_speed %i14.4와 OEM 인터페이스 단자 X1:318/319를 비교합니다. 고객 제어반 끝점 및 현재 접속은 별도 확인입니다.
- bwf01 ok %i11.1와 OEM 인터페이스 단자 X1:264/265를 비교합니다. 고객 제어반 끝점 및 현재 접속은 별도 확인입니다.
- bwf01 fault %i11.3와 OEM 인터페이스 단자 X1:268/269를 비교합니다. 고객 제어반 끝점 및 현재 접속은 별도 확인입니다.
- min lev bwf01 %i11.4와 OEM 인터페이스 단자 X1:270/271를 비교합니다. 고객 제어반 끝점 및 현재 접속은 별도 확인입니다.
- max lev bwf01 %i11.5와 OEM 인터페이스 단자 X1:272/273를 비교합니다. 고객 제어반 끝점 및 현재 접속은 별도 확인입니다.
- bwf 01 run %i11.2와 OEM 인터페이스 단자 X1:266/267를 비교합니다. 고객 제어반 끝점 및 현재 접속은 별도 확인입니다.

| 원문 신호 | 백업 주소 | OEM 원문 끝점 | 현재 고객/현장 경계 |
| --- | --- | --- | --- |
| bwf1_inverter_high_speed | %i14.4 | X1:318/319 | 인터페이스 단자 근거; 고객 제어반 내부/현재 배선 미확정 |
| bwf01 ok | %i11.1 | X1:264/265 | 인터페이스 단자 근거; 고객 제어반 내부/현재 배선 미확정 |
| bwf01 fault | %i11.3 | X1:268/269 | 인터페이스 단자 근거; 고객 제어반 내부/현재 배선 미확정 |
| min lev bwf01 | %i11.4 | X1:270/271 | 인터페이스 단자 근거; 고객 제어반 내부/현재 배선 미확정 |
| max lev bwf01 | %i11.5 | X1:272/273 | 인터페이스 단자 근거; 고객 제어반 내부/현재 배선 미확정 |
| bwf 01 run | %i11.2 | X1:266/267 | 인터페이스 단자 근거; 고객 제어반 내부/현재 배선 미확정 |

## 5. 알람·복구

알람1781은 기동 허가 후 시간 조건이 성립해도 운전 응답이 없는 경로와 외부 FAULT를 구분합니다. 최소·최대 레벨 알람은 별도 네트워크1782입니다. 이 인터페이스만으로 외부 안전·드라이브 내부 순서를 설명하지 않습니다.

제어 속도 고장 네트워크1820은 원본 OFF 허가를 사용합니다. 네트워크1680의 소프트웨어 백분율 제한은0 또는100을 기록하며 실제 피더 용량이나 교정값을 확정하지 않습니다.

원본1781의 SdCoil71는 Tag_49를 사용하며 시간 피연산자 ORef89/RID6은 S5T#10S입니다. 공통 모터 피드백 시간으로 치환하지 않습니다.

외부 인터페이스 범위입니다. 명령·피드백·상태 원본 참조만으로 고객 모터의 배선·내부 인터록·현재 실물 동일성을 확정하지 않습니다. OEM은 OK 인터페이스를 MANU STATUS로 표시합니다. 원시 운전·고장·레벨 및 기동 허가가 고객 내부 자동 모드나 안전 상태의 확정은 아닙니다. 보존된 과거 Simulation 가공값 쓰기는 정적 참조입니다.

## 6. 증상별 관찰

BWF01의 원인은 아래 관찰을 실제로 수집한 뒤 원본과 비교합니다. 빈 관찰 양식을 현재 값이나 복구 완료 증거로 채우지 않습니다.

- 고객 설비 계량 피더 인터페이스의 실제 값·시각·주소(bwf1_inverter_high_speed %i14.4, bwf01 ok %i11.1, bwf01 fault %i11.3, min lev bwf01 %i11.4, max lev bwf01 %i11.5, bwf01 pulse %i20.1, bwf01_level %iw268, bwf 01 run %i11.2, bwf01_flowrate %iw264, bwf01_sp_flowrate %qw298, consent start bwf01 %q6.2)와 OEM 단자 및 고객 제어반 끝점의 비교
- 고객 인터페이스·운전시간 원본 참조를 대조하되 고객 안전·기동 내부 회로를 추정하지 않음
- 현재 설치·명판·호출 주체·명령 계약을 독립 확인

## 7. 완료·누락·검증

BWF01의 문서·정적 검토 결과와 다음에 필요한 증거를 구분하여 인계합니다.

- 같은 이름 XML 주소 선언 미확보: bwf1_inverter_high_speed %i14.4. 검색 색인 근거와 직접 선언 근거를 구분합니다.
- 고객 제어반의 실제 끝점·신호 계약·정상 접점 극성·현재 명판·설치 상태가 필요합니다. 외부 안전 내부 순서는 이번 원본으로 확정하지 않습니다.
- 제어 속도 고장 네트워크1820은 원본 OFF 허가를 사용합니다. 네트워크1680의 소프트웨어 백분율 제한은0 또는100을 기록하며 실제 피더 용량이나 교정값을 확정하지 않습니다.
- 외부 인터페이스 범위입니다. 명령·피드백·상태 원본 참조만으로 고객 모터의 배선·내부 인터록·현재 실물 동일성을 확정하지 않습니다. OEM은 OK 인터페이스를 MANU STATUS로 표시합니다. 원시 운전·고장·레벨 및 기동 허가가 고객 내부 자동 모드나 안전 상태의 확정은 아닙니다. 보존된 과거 Simulation 가공값 쓰기는 정적 참조입니다.
- 이번 범위는 원본 정적 문서 검토입니다. TIA에서 현재 프로젝트·호출·복수 쓰기·컴파일을 확인하는 작업, 현재 CPU 비교, 실제 현장 시험·복구는 미수행·미확정입니다.
- 시뮬레이터는 영구 중지입니다. 이전 대장의 오프라인 실행·시험 설계 문구를 시뮬레이터 생성·실행 재개 지시로 사용하지 않습니다. 실제 PLC·현장·보호값 변경은 수행하지 않았습니다.

현재 CPU·호출/최종쓰기·실물·정상 극성·현재 승인 설정·TIA 컴파일·현장 복구는 확인 전입니다.

- 같은 이름 XML 주소 선언 미확보: bwf1_inverter_high_speed %i14.4. 검색 색인 근거와 직접 선언 근거를 구분합니다.
- 고객 제어반의 실제 끝점·신호 계약·정상 접점 극성·현재 명판·설치 상태가 필요합니다. 외부 안전 내부 순서는 이번 원본으로 확정하지 않습니다.
- 제어 속도 고장 네트워크1820은 원본 OFF 허가를 사용합니다. 네트워크1680의 소프트웨어 백분율 제한은0 또는100을 기록하며 실제 피더 용량이나 교정값을 확정하지 않습니다.
- 외부 인터페이스 범위입니다. 명령·피드백·상태 원본 참조만으로 고객 모터의 배선·내부 인터록·현재 실물 동일성을 확정하지 않습니다. OEM은 OK 인터페이스를 MANU STATUS로 표시합니다. 원시 운전·고장·레벨 및 기동 허가가 고객 내부 자동 모드나 안전 상태의 확정은 아닙니다. 보존된 과거 Simulation 가공값 쓰기는 정적 참조입니다.
- 이번 범위는 원본 정적 문서 검토입니다. TIA에서 현재 프로젝트·호출·복수 쓰기·컴파일을 확인하는 작업, 현재 CPU 비교, 실제 현장 시험·복구는 미수행·미확정입니다.
- 시뮬레이터는 영구 중지입니다. 이전 대장의 오프라인 실행·시험 설계 문구를 시뮬레이터 생성·실행 재개 지시로 사용하지 않습니다. 실제 PLC·현장·보호값 변경은 수행하지 않았습니다.
