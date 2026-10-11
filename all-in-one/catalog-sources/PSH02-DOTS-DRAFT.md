# PSH02 자체 조사 초안 — 압력 채널, 환산과 고압 경보

고정 원본 abcf31c5030bc7ef8749ed8e869a857f2387a28a / v1.12.0. 조사 시작 2026-10-11 10:28:53 UTC. 문서 초안이며 제품 통합·게시·현장 복구 완료가 아니다. 실행 모델/추론 런타임 증명 미확인. 작업 범위는 PSH02 하나이며 PC02·MV06·PSH01/03의 별도 완료를 집계하지 않는다.

## 핵심 확인 및 인계 요약

1. PSH02 원시값은 주소 286이지만 두 접근이 다르다. 0398의 HMI 입력복사는 Input/SAM=None인 IW286 → DB13.DBW50 Word이다. 0496 환산과 0348 제어는 SAM=Peripherie인 PSH02:P/PIW286을 읽는다. HMI 입력값과 환산 Data.PSH_02(DB1.DBW196)를 합치지 않는다.
2. 환산 호출 0496은 ON → FC Signal linearization, Coeff DB4.DBW42, Zero DB4.DBW40, 출력 DB1.DBW196, OFR DB3.DBX22.1이다. 정수 환산·ENO·범위 오류값 −9999·호출 비실행을 분리한다.
3. PSH02 고압은 0537의 환산값 ≥ Data.PSH02_MAX_SETPOINT(DB1.DBW28), SD 원문 S5T#3M, Tag_111(T132) 이후 MAX_PSH_02(DB3.DBX8.2) Set이다. 해제는 현재 알람 AND 환산값 < (MAX_SETPOINT−5)에서 Reset과 STOP_HORN Set이며 RESET_ALLARM 접점은 이 네트워크에 없다.
4. 고압 비트에는 startup의 DB3.DBW8←0 겹침 쓰기도 있다. OFR는 DBX22.1이므로 공통 W0~16 경보비교 및 이 startup 범위 밖이다. HMI Allarmi_67과 Allarmi_215 설정 주소는 각각 확인했지만 실제 경보 이벤트는 미검증이다.
5. 실제 PDF 렌더: FG75/PDF76 X1:175/176/177 → PEW286/75SCH2 → FG107/PDF108 MOD3 I7+34 및 U7−/I7−36. 센서 P-BADR, 4–20mA, 0/10mbar는 도면 인쇄값이다. FG75 개정란 공란, FG107 Rev2 17.03.2025를 각각 확인했다.
6. 상충: OEM FG75/107과 원시 심볼 설명은 OUTPUT MV03, PLC 0347/0348은 MV06 제어이며 P&ID PSH-02는 UC01 쪽에서 MV06으로 연결된다. 시공 PDF58은 UC01-PSH02A이다. PC02 이름·과거 주석만으로 물리 PSH02와 병합하지 않는다.
7. 핵심 누락: 현재 CPU/하드웨어 구성, 계수·영점·HMI 스케일/편집 이벤트, 모든 간접·통신 Writer, 실물 명판/루프 교정/설치 위치 및 안전 복구 증거. 새 현장 자료 없이 반복 확인하거나 추정하지 않는다.

공유 근거와 신규 확인을 구분한다. BF01/BF02 초안의 공통 0291/0014 정수환산, 0151~0153 Word 경보, 0148 startup 분석은 동일 고정 원본의 연결 인덱스로 사용했다. MV06 초안은 0347/0348·0496·FG75/107·시공58의 탐색 인덱스로 사용했다. 이번에는 PSH02 고유 선언, 신호 핀, 고압 0537 전체 및 위 두 전기쪽/시공58/P&ID를 독립 대조했다. BF의 차압 임계값·Reset 조건을 PSH02에 복제하지 않았다.

## 1. 설비·자료 기준

- INVENTORY.json catalog[5]: PSH02, sensor, 계측, parent_id=null, phase2 planned, alias psh_02. 대장 계획상태를 문서 완료로 바꾸지 않았다.
- TASK3-BATCH05-SCOPE.json과 GME-CATALOG-OVERLAP-REVIEW.json의 PSH02는 고유 신규 조사대상이며 physical_identity_verified=false. 동일 이름 PSH01/02/03은 서로 다른 catalog ID이다.
- 원본은 source-mv06/all-in-one. 아래 모든 XML 경로의 공통 접두사는 `all-in-one/sources/decoded-original/`이다. 도면은 `all-in-one/sources/` 아래에 있다. 번호 LAD/doc는 탐색 색인의 문서 ID이고 원본 XML 파일 번호/NID와 구분한다.
- ZAP18/PEData.plf 및 중지5자산은 보존 해시만 확인한다. 원본 생성기·빌드·시험·시뮬레이터·TIA·현장 명령은 실행하지 않았다. SEJIN 원본/사진/운영기록과 공개대장도 수정하지 않았다.
- 적용 7영역은 모두 아래에 기술하며 현장 자료가 없는 부분은 근거 미확보로 남긴다. 압력센서 자체의 모터 방향 출력/접촉기 부하접점/정비 토크는 비해당이다. 주변 MV06 구동기의 자료를 센서의 전용 부품으로 복제하지 않는다.

### P&ID 판본과 공정 위치

PID_1684n002I.pdf 실제 1쪽 전체 및 PSH02/개정란 확대를 확인했다. 도면 1684n002, Rev I, 원도 06/04/2011, I 개정 15/01/2013. Rev F 29/02/2012는 REVISED POSITION OF PSH-02, Rev H 01/08/2012는 ADDED MV-06 AND MODIFIED MV-03 COMMAND INSTRUMENT이다. PSH-02와 MV-06 Overflow valve 사이 신호선 및 UC-01 쪽 압력 취출 위치가 그려져 있으며 SetPoint=+0.2mBar 인쇄가 있다. 이는 과거 설계값으로 현재 제어 설정값/안전 기준으로 적용하지 않는다. 현행 설치 및 PC02와의 실물 동일성은 미확정이다.

## 2. I/O·HMI: 원시·복사·환산·설정의 분리

| 계층/대상 | 백업 형식·주소 | 원본 선언 및 직접 연결 | 판단 경계 |
|---|---|---|---|
|PSH02 원시 입력 복사|Int IW286|0627 SimpleAccess Global RID82, NID2 UID102, SSD AO2288, SAD Input/SAM=None|프로세스 이미지 접근; 현행 채널 구성 미확인|
|Inputs.PSH_02|Word DB13.DBW50|0629 Global RID84, NID2 UID103 AK=Write, AO400; 0398 Move97 in W112/ORef102, out1 W114/ORef103|HMI용 원시 Word; 압력단위 환산 아님|
|PSH02 환산 원천|Int PIW286|0678 SimpleAccess Global RID101, NID16 UID464, AO2288, SAD Input/SAM=Peripherie|IW와 주소 숫자는 같아도 접근/샘플시점 동일성 보장 없음|
|PSH02 SP=0 원천|Int PIW286|0617 RID84, NID8 UID751/757, Peripherie|0 비교를 0mbar라고 바꾸지 않음|
|Coeff.COEFF_PSH02|Int DB4.DBW42|0676 Global RID102, NID16 UID465, AO336|현재 계수 미확인|
|Coeff.ZERO_PSH02|Int DB4.DBW40|0676 Global RID103, NID16 UID466, AO320|현재 영점/교정값 미확인|
|Data.PSH_02|Int DB1.DBW196|0676 Global RID104 NID16 UID467 Write AO1568; 0619 RID73 NID7 UID632 및0684 RID94 NID11 UID941/951 Read|공정제어/고압 비교값; mbar 배율 미확정|
|Data.PSH02_SETPOINT|Int DB1.DBW42|0619 Global RID71 AO336, NID7 UID629/631, NID8 UID747|제어 분기값; MAX_SETPOINT와 별도|
|Data.PSH02_MAX_SETPOINT|Int DB1.DBW28|0684 Global RID95 AO224, NID11 UID942/948|고압 한계의 현재값 미확정|
|ErrPSH02|Local Int|0062 InterfaceAccess Local RID74 AO128, NID7 UID633 Write/641·644 Read|DB에 저장된 전역 값으로 오인하지 않음|
|app06|Local Int|0685 Local RID100 NID11 UID950 Write/952 Read|고압 해제용 임시 MAX−5|
|MAX_PSH_02|Bool DB3.DBX8.2|0684 Global RID98 AO66, NID11 UID946 Set/953 Reset/947 Read|하나의 알람 비트|
|PSH02_OFR|Bool DB3.DBX22.1|0676 Global RID387 AO177, NID16 UID23 Write|고압 비트와 다른 일반 출력|
|Tag_111|Timer T132|0686 SimpleAccess Global RID97 SSD AO132, SAD Timer, UID944 Write/945 Read|HMI 태그 아님; 3분 SD 타이머|

0398/NID2, LAD1071: Powerrail W21은 Move96.en에 연결되고 PSH02 Move97.en은 앞 Move96.eno의 W110을 통해 연결된다. Move97 자체 DisableENO=true이고 출력 eno W113은 다음 Move98.en에 간다. raw 전달은 bit Set/Reset이 아닌 16bit Word 쓰기다. 이 직렬 연결을 아무 실행 조건도 없는 독립 복사라고 단정하지 않는다. 현재 호출/ENO 상태는 미확인이다.

HMI `sources/hmi_plc_tags.csv` 직접 주소 조회:

| 태그 | 설정 주소 | 내부 ID | 의미 경계 |
|---|---|---|---|
|I_PSH_02|DB13,INT50|00055|Word 입력 복사 위치를 HMI Int로 설정|
|data_DB1_DBW196|DB1,INT196|00292|환산값 주소|
|Editor_PSH02|DB26,INT18|00410|레시피 편집 버퍼 주소; DB1W42 직접 쓰기와 다름|
|data_DB1_DBW42|DB1,INT42|0027C|제어 설정 주소|
|data_DB1_DBW28|DB1,INT28|001E6|고압 설정 주소|
|Coeff_DB4_DBW40|DB4,INT40|00237|영점 주소|
|Coeff_DB4_DBW42|DB4,INT42|0020F|계수 주소|
|Allarmi_67|DB3,X8.2|0014A|고압 알람 설정 주소|
|Allarmi_215|DB3,X22.1|00280|OFR 설정 주소|

모두 Access Name=PLC이고 CSV는 dde.cfg 설정 근거다. 화면 위젯·경보 문구·발생/해제 이벤트·소리/로그·사용자 쓰기권한·단위/배율과 온라인 값은 확인하지 않았다. 설정 주소 존재를 실제 표시/사용/복구 완료로 승격하지 않는다.

## 3. 제어 구조와 환산

### 3.1 PSH02 고유 환산 호출

0496-FlgNet.xml, LAD1746, NID16의 Contact475: operand W469/ORef462→ON(0678 RID1). 출력 W476→CRef456.en. CRef456 RID351의 CodeBlock468 RID5는 0672 FCBlock Signal linearization과 0680 인터페이스 선언으로 결속한다.

| 호출 핀 | Wire/ORef | 결속 |
|---|---|---|
|IN0|W470/463|ON|
|Analog_input|W471/464|PSH02:P, Peripherie PIW286|
|Coeff|W472/465|Coeff.COEFF_PSH02|
|Zero|W473/466|Coeff.ZERO_PSH02|
|OutValue|W474/467|Data.PSH_02, AK=Write|
|Out_of_range|W24/23|Allarm.PSH02_OFR, AK=Write|

ON이 호출 EN과 IN0 양쪽에 사용된다. 호출 EN이 거짓일 때와 블록 내부 IN0=false 실행은 다른 상황이다. ON이 꺼졌다고 이 호출로 OutValue=0이 실행되었다고 단정하지 않는다.

### 3.2 공통 함수의 형식·ENO·오류 분기

공통 근거 0291/NID1 및0014/NID2를 직접 재대조했다. Local 선언0611과 상수0612를 사용하며 동일 RID/UID가 다른 블록에 나온다는 이유로 전역 ON/Data에 결속하지 않는다.

- 0291 Contact255 IN0→W256. Gt258는 Analog_input > −1382, 뒤 Le161은 ≤32767이다. W26→Convert164: Int→DInt.
- Convert164.eno W227→Convert167(Zero Int→DInt). eno W230→Add170, out W233→local App3. eno W234→Convert174(Coeff Int→DInt). eno W237→Mul177, eno W241→Div181(상수28000), eno W245→Move185→OutValue Int W247/ORef215.
- 계산 의미는 `(DInt(raw)+DInt(Zero))*DInt(Coeff)/28000`의 정수 경로다. REAL 스케일/소수압력 표시가 아니다. 마지막은 Move이며 Float→Int 변환기라는 명칭을 붙이지 않는다. 잘림/범위 초과/ENO 최종 실행상태는 현재 CPU에서 미검증이다.
- 별도 Gt190(raw>32767) OR Le259(raw≤−1382)→O47 W49→Move193 −9999, out1 W253/ORef219→OutValue. Move193.eno W21→일반 Coil23, operand W22/ORef24→Out_of_range. OFR는 SCoil 래치가 아니다.
- 0014 Contact171의 operand가 Negated, Local IN0이다. NOT IN0→W172 Move162, 0 W169/ORef166→OutValue W170/ORef167. 해당 함수가 실제 호출되었을 때의 내부 분기다.
- −1382/32767/−9999는 함수 원시 정수/센티널이고 OEM의 0/10mbar나 HMI 표시 단위와 같지 않다. 현재 계수·영점을 추측하여 압력값을 산출하지 않았다.

### 3.3 환산값의 제어 사용처

0347/NID7, LAD1709는 ON675→Ne592(PSH02_SETPOINT≠0) W650 아래 Sub598를 수행한다. W651/ORef631=SP, W652/ORef632=Data.PSH_02, out W653/ORef633=Local ErrPSH02. 이 출력은 Sub.eno를 경유하지 않는 별도 접점/타이머 가지와 나란히 연결되어 있어 전체를 단일 ENO 사슬로 그리지 않는다.

- NOT Tag149 Contact677→SD605 S5T#300MS(Tag150), Tag150 Contact679→SD610 S5T#4S(Tag149).
- NOT Tag150 Contact681→W682→Ge618 Err≥5→Coil621 MV06 PID DOWN(W667/ORef643), Le624 Err≤−5→Coil627 MV06 PID UP(W672/ORef646). 일반 Coil이며 방향 실제 출력/밸브 위치와는 별도 내부 요청이다.

0348/NID8, LAD1710는 ON807 AND MV06_Auto809 AND SP=0(Eq693) AND NOT ShotClose811 AND NOT ShotOpen813를 통과한다.

- PSH02:P≤0(Le701 W777/778)→SD707 S5T#20S→Tag151 Contact815→S712 ShotClose.
- PSH02:P>0(Gt715 W786/787)→SD721 S5T#2S→Tag152 Contact817→S726 ShotOpen.
- 별도 ON 아래 ShotClose OR ShotOpen→SD735 S5T#300MS(Tag153)→Contact823→R741/R743 두 Shot 해제. W824는 두 Reset에 병렬 연결된다.

0원시값을 0mbar로 바꾸거나 300ms를 실제 밸브 움직임 시간으로 확정하지 않는다. MV06 방향 허가/출력/전기/응답/엔코더 전체는 기존 MV06 초안의 별도 범위이다. 이 조사로 MV06 또는 PC02를 추가 완료로 세지 않는다.

### 3.4 호출·레시피·복수 쓰기 경계

- 0031/NID6: ON282 W280/ORef271→W283에서 CRef261(FC3 Analog input conversion) 및 CRef264/267/270(FC4/5/6 Allarms1/2/3)의 en이 병렬 연결된다. CodeBlock273/279는 0688 RID55/64, 0694 인터페이스와 대조했다. XML의 병렬 en 결속은 현재 스캔 순서/활성 CPU 증명이 아니다.
- 0032/NID8: ON352 W350/ORef345→W353 CRef341.en(FC14 Valve Control loop), CRef344.en(FC18 Analog output conversion). 0688 CodeBlock347/349 및0694로 대조했다.
- 전체 식별 XML 이름검색에서 Data.PSH_02 직접 명명 Write는 0676 NID16 UID467, Inputs.PSH_02는0629 NID2 UID103으로 확인했다. 모든 간접 포인터·블록복사·절대 DB쓰기·통신 Writer가 없다는 결론은 아니다.
- Data.PSH02_SETPOINT는0642 Global RID99 NID1 UID3641 AK=Write도 있다. RID100/UID3607은 RecipesDB.Recipes.PSH02 읽기이다. 0554 레시피 Monitor 선언과0668 NID11의 REAL 변환 참조도 발견했다. 상류 코드/활성 레시피/쓰기 우선순위는 완전 결속하지 못했다.
- live_index의 `_7ex` 별도 세그먼트 doc14 “control pc02 moduling mv03 - convert values in real”은 PSH02 SP/환산값의 ITD/DTR 검색 텍스트다. 이를 주 제어 0347과 동일 네트워크로 만들거나 PC02의 물리 동일성/현재 실행을 확정하지 않는다.

## 4. 전기 전달 끝점과 실제 PDF

### 4.1 OEM 센서 → 입력 채널

Electrical_Rev2.pdf의 실제 PDF76, footer FG75, PRESSURE CONTROL, DATA27.05.2024, 개정란 공란. 중앙 PSH-02 회로:

- +24Vdc10.7 → X1:175, 5×20/50mA F → 도선75.2 → PSH-02 `+`.
- PSH-02 `−` → X1:176 → +PEW286, 교차참조107/5.
- 차폐 → X1:177 →75SCH2, 교차참조107/5. 센서 출력은4–20mA, P-BADR, 0/10mbar 인쇄.

실제 PDF108, footer FG107, ANALOG INPUT MODULE, DATA27.05.2024, Rev2 17.03.2025:

- 75/5의 +PEW286 → MOD3/CPU515 인쇄 블록 I7+ 단자34. U7−/I7− 단자36은 공통 −0Vdc10.6 귀로. Uv7 33/U7+35를 실제 사용 단자로 대체하지 않는다.
- 75SCH2의 차폐 기호를 별도로 확인했다. 차폐를 신호 음극과 같은 선으로 합치지 않는다.
- 모듈 전원 +24Vdc10.7→X21:3001(5×20/500mA F)→107.1→41 L+, 44 M→−0Vdc10.6. 이 500mA는 PSH02 분기50mA와 다른 보호다.

도면 인쇄값과 실제 하드웨어/현행 보호값/퓨즈 장착/교정은 분리한다. 도면의 CPU515라는 글자를 현재 CPU 모델 확인으로 쓰지 않는다. 센서는 이 자료상 아날로그 출력 기기이며 릴레이 부하접점5/9를 적용할 근거가 없다.

### 4.2 시공 케이블과 상충

Electrical_Can_Decoating_20241118.pdf 실제58쪽, D-PAGE8/TOTAL58/64, DWG CANDC-CONS-C008-058, 개정1 24.11.11 “first draft design”, Checked/Approved 공란을 실제 렌더로 확인했다.

행8_10: `=FLB+UC01-PSH02A`, FROM CR → TO UC-01/PSH-02, AI, CVV-S, CORE4S, SIZE1.0, SPARE1, route100 →120 RBD1→E800, Adjustment4, LEN55. 이는 시공 표의 설계 길이/경로로 실측 길이나 현재 승인 결선 완료가 아니다. 이 표는 OEM X1:175/176/177의 선심 번호까지 주지 않는다. CR/UC01 케이블과 OEM 단자별 실물 결속은 보류한다.

전기 FG75/107의 OUTPUT MV03, PLC MV06 사용, P&ID 개정H의 변경 이력 및 시공 UC01 위치는 서로 구별한다. “오탈자 수정”이나 설비명 통합을 수행하지 않았다. 현행 명판·루프도·실물 단자/케이블 번호·프로젝트 채널 구성의 동시 확인이 필요하다.

## 5. 알람·복구

### 5.1 고압 래치: PSH02 독립 확인

0537-FlgNet.xml 전체, LAD1989, NID11:

1. ON Contact977(operand W955/ORef940,0686 RID1) out W978→Ge908.pre.
2. Ge908 in1 W956/ORef941=Data.PSH_02(0684 RID94), in2 W957/ORef942=Data.PSH02_MAX_SETPOINT(RID95). 비교는 `≥`이다.
3. W958→SdCoil914.in와Contact979.in. SD 값 W959/ORef943=상수 S5T#3M(0683 RID96), operand W960/ORef944=Tag_111(0686 RID97 Timer T132). Contact979 operand W961/ORef945=같은 타이머, out W980→SCoil919. W963/ORef946→Allarm.MAX_PSH_02(RID98).
4. ON의 W978는Contact981.in도 공급한다. Contact981 operand W965/ORef947=현재 MAX_PSH_02. W982는 Sub926.en과 Lt932.pre에 병렬 연결된다.
5. Sub926의 in1 W966/ORef948=MAX_SETPOINT, in2 W967/ORef949=Int5(0683 RID13), out W968/ORef950=Local app06(0685 RID100 AK=Write).
6. Lt932의 in1 W969/ORef951=Data.PSH_02, in2 W970/ORef952=app06. W971→RCoil936와 SCoil938 병렬. W972/ORef953는MAX_PSH_02 Reset, W973/ORef954는Flag.STOP_HORN Set(0684 RID16).

Sub926.eno가 Lt932.pre를 공급하는 연결은 없다. 위 원본 연결·Int 연산을 보존하고 정상 실행/오버플로우 시 최종값은 미검증으로 남긴다. 해제는 strict `<`이고 정상범위 하한 검사는 없다. OFR가 −9999를 쓰면 정상화되지 않았더라도 한계−5보다 작아질 수 있다. 따라서 알람 해제는 계측 정상/안전 운전/재시작 가능 증거가 아니다. 고압 한계 및 지연시간을 변경하거나 현장 Reset을 수행하지 않았다.

### 5.2 겹침 Word와 공통 경보

0148 startup, LAD403, NID3: ON329→W330→Move267.en, Int0 W315/ORef293(RID54)→out1 W316/ORef294(RID32). 0563 GlobalAccess AO64와0562 Allarm DB3로 DB3.DBW8←0임을 대조했다. 이16bit 영역은 MAX_PSH_02 DBX8.2를 포함한다. 이 startup 쓰기를0537의 자동 해제와 같게 세지 않는다.

공통 근거는 BF01 초안§5.2를 연결 재사용하며 PSH02 주소 포함 여부를 직접 대조했다. 0151/NID1의 RESET_ALLARM/RUN_HORN/STOP_HORN OR 아래 DB3W0~16 복사, W8 Move147 in W202/ORef181→WorkData.W4 out W203/ORef182. 0152/NID2 Ne203는DB3W8 W252/ORef228과WorkData.W4 W253/ORef229를 비교하여 OR190.in5 W254, NOT STOP_HORN271을 거쳐NEW_ALLARM Coil219. 0153/NID3은NEW_ALLARM AND NOT RESET_ALLARM AND NOT STOP_HORN→RUN_HORN Set/NEW_ALLARM Reset이다.

MAX_PSH_02는 이W8 범위에 포함된다. PSH02_OFR X22.1은 W0~16 범위 밖이며 이 경로로 경적이 울린다고 말할 수 없다. HMI Allarmi_215 설정은 존재하지만 다른 알림경로 존재/부재나 실제 이벤트를 확인한 것은 아니다. 알람 단일 비트 이름검색만으로startup·Word 전달을 놓치지 않도록 유지한다.

## 6. 증상별 관찰 초안

현장 조작 지시가 아니라, 승인된 관찰 때 확보할 기록 목록이다. 관찰자·시각/시간대·장치/프로젝트 식별·단위·비교근거·배제결과·조치·복구증거를 각각 남긴다. 실제 값은 현재 미수집이다.

| 증상 | 먼저 분리할 관찰 | 원인 판정 전에 확인할 근거 | 보류 조건 |
|---|---|---|---|
|HMI 값과 제어값이 다름|IW286, PIW286, DB13W50, DB1W196을 같은 시각에 비교|0398 원시Word 복사와0496 정수 환산, HMI 각 주소/배율|읽기시점·호출·설정·교정 없이 센서고장 단정 금지|
|고압 표시가 지연되거나 해제됨|DB1W28, DB1W196, T132, DB3X8.2, startup 시각|0537 ≥/3M/strict<(한계−5),0148 겹침쓰기|알람사라짐만으로 정상/복구 완료 금지|
|OFR 또는 −9999|PIW286, IN0/EN, Coeff/Zero, DB3X22.1|0291 범위·Move193.eno→Coil; FG75 loop/FG107 채널|현재 전원·결선·기기교정 증거 없이 교체 지시 금지|
|압력 변해도 MV06 반응 불명|SP=0/≠0, Auto, Err, PID UP/DOWN, Shot, 타이머|0347 환산오차±5와0348 원시0 비교를 분리|논리요청과 실제 구동/위치 응답 구분|
|HMI 레시피 편집이 적용되지 않음|Editor DB26W18, 활성레시피 식별, DB1W42|레시피 버퍼/쓰기 요청·0642 writer·최종제어 사용값|저장/전송/활성화 이벤트 미확정|
|도면과 명판 설비명 다름|PSH02 명판·케이블8_10·X1 단자·채널정보 동시사진|OEM MV03, P&ID MV06,시공 UC01 출처별 시점|PC02/PSH02 병합 및 임의 태그 수정 금지|

## 7. 완료·누락·검증 및 다음 작업

### 적용 상태와 네 기능

| 영역 | 상태 | 확보/미확보 |
|---|---|---|
|설비·자료 기준|적용, 현행 미확정|대장·별칭·P&ID 개정·소유 상충|
|I/O·HMI|적용, 실제 이벤트 미확인|원시 접근·Word·환산·HMI 주소9행|
|제어 구조|적용, 전체 Writer 미확정|환산·고압·MV06 사용·호출선/지역선언|
|전기 끝점|적용, 실물 미확인|OEM2쪽·시공1쪽·P&ID1쪽|
|알람·복구|적용, 현장 복구 미확인|SD3M·Set/Reset·Word겹침·OFR 별도|
|증상별 수리/관찰|관찰 초안|실제 관찰·진단·조치 없음|
|완료 기준|문서 complete_with_gaps|기능/현장/게시 완료와 분리|

도면·래더 나란히 보기, 백업 미리보기/선택 복원, 기록 전후 비교, 관찰 보고서/PDF의 PSH02 전용 구현/저장·재읽기·재열기 검증은 모두 not_run이다. 이 MD는 실제 UI나 사용자 기록 기능을 만들지 않는다. note/repair_observation/미지필드/타설비/초안/저장키를 변경하지 않았다.

| 상태 | 결과 |
|---|---|
|documentation|complete_with_gaps, 자체 조사 초안|
|static_review|핵심 원본·선택 도면 대조 완료, 부모 독립검토 대기|
|ui_records|not_run|
|publication|not_published|
|tia_compile|not_performed|
|live_cpu|not_performed|
|field_recovery|not_performed|

의미검토 범위: 0496/0291/0014/0347/0348/0537 전체 핵심6네트워크;0398은PSH02 입력복사/ENO연결 분기;0031/0032 호출핀;0148 DB3W8 초기화;0152 W8 비교/0153 경적분기. 공통0151은 기존 BF 원본 분석의 연결 재사용이며 동일 파일 해시와 PSH02 포함 주소를 점검했다. 다른 블록의전체 가지·간접/통신 Writer·현재 OB 순서는 완료 범위가 아니다. 실제 PDF4개 고유 페이지(전기2+시공1+P&ID1), P&ID 확대2개는 별도 페이지로 더하지 않는다. 해시 파일 수는 의미검토 수가 아니다.

중요 미확정:
- 현재 프로젝트/CPU 비교, 장치 구성의 PIW286 채널·프로세스 이미지 갱신·모듈진단.
- 현행 센서 모델/명판, 양 끝점·차폐·선심 확인, 교정성적서, 압력 취출부의 위치와 정상 극성.
- 현재 Coeff/Zero/SP/MAX, 출력단위/표시배율, 승인된 보호설정. 과거 P&ID +0.2mBar를 현재값으로 대체 금지.
- 레시피 적용의 실제 이벤트/현재활성코드 및 PC02 명칭의 물리 대응, 모든 Word/블록복사/통신 Writer.
- HMI의 화면·경보문구·발생/해제/ACK/소리·히스토리·알람 이후 복구/재요청 절차.

다음 한 작업: 부모가 0537의 ≥/3M/strict 해제/STOP_HORN, 0148의 DBW8 겹침, 0398 IW와0496 PIW 분리, FG75/107 개정·단자 및P&ID 변경이력을 독립 대조한다. 새 자료 없는 실물 보류를 반복 조사하지 않는다. 로컬2차133 통합 제외를 유지한다.

## 부록. 파일 무결성과 실제 작업 시각

아래 모든 SHA-256은 고정 커밋 Git blob 내용과 직접 바이트 비교한 것이다. 압축백업·PLF·중지5자산은 보존확인만 수행했다. 선택 파일 수를 전체 원본 의미검토 완료로 해석하지 않는다. 실행은 자체 XML 파싱·PDF렌더·해시·읽기전용 Git 확인으로 한정했다.

원본/맥락/보존 67파일 모두 Git blob과 바이트 일치. 중지5자산 freeze 해시 일치. 종료 원본 Git 변경0. 정적 원본단언16개 passed. 완료시각 2026-10-11T10:36:32.662423+00:00.

| 파일 | SHA-256 | 고정 Git blob OID |
|---|---|---|
| `.agents/skills/gme-equipment-rollout/SKILL.md` | `fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b` | `9aa820ea6ca15b4e136c9772423b78ed4df6a3d4` |
| `AGENTS.md` | `0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2` | `073164bc6efd5791032d62c71b03b4dab48cb6f8` |
| `EXPANSION-WORK.md` | `ec624de9fd2fcfac861a67fd5e828b25ef46db50bfd7a37ff16e2cb54cd0f7e2` | `4c42d88ecc2d48269eb23e13a20ebf3721a092a1` |
| `PUBLICATION_STATUS.md` | `efe4857aec598d90470322cf3962eb3fe1f64947630e1fdf71d1c90134de8740` | `d76401cf291fc0be681acc51fa898ad3ce46ff78` |
| `VERSION.json` | `5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7` | `fffb51663b7705aec91cb119ca80ee943a4ce758` |
| `WORKSPACE-HANDOFF.md` | `215096d997782e78e901dfae36c782937e49611fbeb677a0d3fa50cbecf8d074` | `dd0b8989d2376c4415bba9bd826fe6754c6b1a12` |
| `all-in-one/ACTIVE-WORK.md` | `eff3bbc08ecff41da3beff77f3fec48e7d148708192bcaaab00f34b6a721afc2` | `6eb947c629b5ddf9c759ef87649451303938864b` |
| `all-in-one/assets/program-model-data.js` | `52f8199371e3399b7c0d44ab5469f0472aced79d56bbef2887f7625f5d2aff0f` | `38f34b0caa380a16ccad6f6f1e234a2fdf23f327` |
| `all-in-one/assets/simulator-workspace.js` | `3a6dfc618ff7e7b238f2671dc85d65704f33093a18eac879d86081d92c31e8bc` | `97c2c831c77a9699fff0e0960b3bc1b7d93d45b3` |
| `all-in-one/assets/virtual-plc.js` | `5f1876052dc0067b1f010af0dfc941946e37003167481731293615d9c1c36dbc` | `0bd9eceb54365a91214a37c5601b5067c39a3f75` |
| `all-in-one/registers/program-model.json` | `6203479c086b15bada12ac9d7e37db9280234ec26f1ea6091d7211dc09a577c5` | `9860b10f008d3a5ae714be50d77b703dfec32f3a` |
| `all-in-one/registers/simulator-freeze.json` | `bb93c1994effc5609939ba566b7802ce7ed55154a7310f02379b308ac2c8c835` | `808ffac14dbd1b4a7d797fa6cd0d647635d90b47` |
| `all-in-one/registers/virtual-plc-test-results.json` | `a6b389f797f9a8b5ffe6928b8420f55c4cc459a327b0b48d716079d2eca6dd64` | `757dd50e45184568facb8ff62900b39d3ce848d1` |
| `all-in-one/sources/Electrical_Can_Decoating_20241118.pdf` | `3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd` | `0ee6b6f8361c5790864dbba4bbd9d55e8e7c08f8` |
| `all-in-one/sources/Electrical_Rev2.pdf` | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` | `f610fd7c7ce14ae951b00cff57b969259bfb389d` |
| `all-in-one/sources/GME_20250506.zap18` | `00c79b6d986e68298f65b172c1807115bc5d9e450a74fcc989d0796d8d8a4ea8` | `211c4f604627a32f82a1124c2a9872c2fcf00865` |
| `all-in-one/sources/PEData.plf` | `647de7ea123daced41c27bec8f81aeb93c712cac714d4754d7da5c528abb016a` | `65605ff8910f920109da731604aa5dc8d83fc956` |
| `all-in-one/sources/PID_1684n002I.pdf` | `2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b` | `8c83a59fefd5b8b651ec3537ea4236a073f5e109` |
| `all-in-one/sources/decoded-original/0014-FlgNet.xml` | `2e814adbaac6bab99bc668bfdab74f0fc90576324d0b88728951683869cfac30` | `4d164b074fcc13a8f97da9e24382cc169ef29555` |
| `all-in-one/sources/decoded-original/0031-FlgNet.xml` | `76385eab8f8f72b9faa16f7cf8905f395591b18c0a9ee9e6d7dd085a38c45c65` | `653d27572de6beedcf3eb6c95702bb119a8b567f` |
| `all-in-one/sources/decoded-original/0032-FlgNet.xml` | `070bb8efa33d03b18add5da81d3f670a47c12b288076b7bfee11ac87fe6fa7e4` | `e31cf9aeecfbfc0c264921ac217cbd15479c1f34` |
| `all-in-one/sources/decoded-original/0047-IdentXmlPart.xml` | `2e53bb895dd1ad2a74efaeb1ef16dfd61e62b1b2d7aa34cec8612f1b9cb0928e` | `3dc282f149a21fdf76d5521ef1c833be63b578b4` |
| `all-in-one/sources/decoded-original/0048-IdentXmlPart.xml` | `d8e8687de7271bd294c2b62b33d789700af9d5014d82b130141988c4d479253d` | `64fc5a7f1ad33f3b901b00f0d22d23578ffabff8` |
| `all-in-one/sources/decoded-original/0062-IdentXmlPart.xml` | `34f188168dc4fad0d6e2c813028045f37b84025636bcebd8aa1c7ffb4cfd9bcd` | `624eed3ba6cd1eb54e7e3f316f8c4c159ca3b4b5` |
| `all-in-one/sources/decoded-original/0148-FlgNet.xml` | `1d80e1bbf1c82dcc4dd18628c35935bbd55a17b5be9c1ca7bfb249600d154313` | `3069ae3b5fa16ed10a64c149b6cf5cb5ace423b3` |
| `all-in-one/sources/decoded-original/0151-FlgNet.xml` | `227627d165c6240a4c15b62fd4e4c8d7a621c15f35319cb424601df5cc52c904` | `8e8a9801d1f57180fc3747f6515c0353f38f7dc5` |
| `all-in-one/sources/decoded-original/0152-FlgNet.xml` | `2b6165460f06a52de56afcb4d65ed163d64320e24af1b194e934a4d7c6bfe49f` | `dd8e35b98043d9d0f230351352273eac1d783990` |
| `all-in-one/sources/decoded-original/0153-FlgNet.xml` | `3d3a236a66a7a5c9b8e2d1e15da63cc943ba5cd266949583cbac6ffbb2f88bc6` | `d50223c45f5eb1d1c1d3530b41db1e79ad6c71f3` |
| `all-in-one/sources/decoded-original/0291-FlgNet.xml` | `fe0b92f074eba25148ce34084649af3d968962558d652727f1eea19f3e3c2550` | `1418fb2ed172c6df694a5eb8bf2dffd0b177653b` |
| `all-in-one/sources/decoded-original/0347-FlgNet.xml` | `092aa32263fce728afde49d5fff0dddb6cc1445c6f71e4fb45956129beda4d6d` | `81a970037cf8bb628c67b61185635e2ae0f574c6` |
| `all-in-one/sources/decoded-original/0348-FlgNet.xml` | `00570dd8c0945f04304c8820b8e3d7294916aa04aaa1158d1c630062961bbedf` | `77338b9dbe0ffd938a992311c55bc07b7f4eaed0` |
| `all-in-one/sources/decoded-original/0398-FlgNet.xml` | `4f092b18df4e44af98fd44e173f48dad213a4e80b71f46b0a5e8a700f5b0a747` | `67ebb54daa55093487ea7e780f23ae2cf193c397` |
| `all-in-one/sources/decoded-original/0496-FlgNet.xml` | `9a5c816b27efc2afbe84a170b1f80959c4992829d10eaa55f6bd18f28030808a` | `afe8556ec23887983b4ed5d75e259647374bf1b3` |
| `all-in-one/sources/decoded-original/0537-FlgNet.xml` | `a616e375d6b27b2fe3406838574f75a811357ac0a2a50c949e51201e3d9b5115` | `50169469a1ef3d65bd10c6d2f2a38f522ec7447a` |
| `all-in-one/sources/decoded-original/0554-IdentXmlPart.xml` | `4ae3e7d0bca0f78c9e94617abeb70bdd228d85d74bff2224174fa1bb0076e78c` | `cdb68b35a7287f6b5636c01ea3a01747d3d60e81` |
| `all-in-one/sources/decoded-original/0562-IdentXmlPart.xml` | `85aada44dd9a3e66835463c3fed400f1efe121f4f5bc5ab8f0ad49481ec0ea1c` | `1609802542a3e560baba3f2b73c306be281dfb23` |
| `all-in-one/sources/decoded-original/0563-IdentXmlPart.xml` | `86cf35b6baebc079cb5a092baf53ec3364c377ea7318eb263ab69c8b4550b4ad` | `6a10fc694f896cda16409804daf2554c91635654` |
| `all-in-one/sources/decoded-original/0564-IdentXmlPart.xml` | `2aed17fa02d19b0a081023282841aa561d6a2dca3e393284da3622b967af00b1` | `c4b1f2cb191970cfce1cce59cb290a9f1f934c37` |
| `all-in-one/sources/decoded-original/0565-IdentXmlPart.xml` | `0f7f970faa6c456f2bb032b1a2072a2f52db1e03fc77bd8d35d4583deeaf1149` | `c2e3e2d57c94c5da864f6e172f0a7a925da942d6` |
| `all-in-one/sources/decoded-original/0611-IdentXmlPart.xml` | `0d583915a261703954da22c176ba9f81338ad13ea2810e7cd5f7de8aa1bfa089` | `bad6b16fb32a32d47d882f48754994887457872b` |
| `all-in-one/sources/decoded-original/0612-IdentXmlPart.xml` | `95b545d4964d371ebfc107894ea90b8b1d0d7ab5d3a70e643f8ce539063c0f38` | `7cc782d33d07ef225c2104f3e7c9fbd31f7c7467` |
| `all-in-one/sources/decoded-original/0617-IdentXmlPart.xml` | `10bcf85169cb2512f55acadaef299a3d46b4b4cecd88032d739cfeba23e94aa9` | `9527658ee6808be34bd513b1b2ebaf3a4a5a6f3e` |
| `all-in-one/sources/decoded-original/0619-IdentXmlPart.xml` | `85694bb5b696e31e6a1217431112e5b750516c4f94078d6e127d4394a8b80456` | `11f0502c84a1f319a21459a35c0dc1c6ce8e8f36` |
| `all-in-one/sources/decoded-original/0620-IdentXmlPart.xml` | `da97226a148a1a8babaea67db412761a718b7e7537212b7807e8ea27d000d2d3` | `dc88b5e87ad3331928f14fcf647673a26fb70b6b` |
| `all-in-one/sources/decoded-original/0627-IdentXmlPart.xml` | `08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb` | `61ebc0abbb2ca160e11e1da400a3f14a397d8bc5` |
| `all-in-one/sources/decoded-original/0629-IdentXmlPart.xml` | `67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972` | `058129bb01e27f7a6a0d0293f332d745e5bab74e` |
| `all-in-one/sources/decoded-original/0631-IdentXmlPart.xml` | `8e5072374f8ef098de72fbf93965b2a7bb0965c0f803e397daa68588c0c38555` | `27aa5aef2b126820b4658362e4aad5ca6d709fee` |
| `all-in-one/sources/decoded-original/0642-IdentXmlPart.xml` | `c922483c261c8ddb98c239a7b4dc3d7f73f9a45261dd5b4d669f39d6918a1c21` | `398f73b99c4a792a68387485fcb47048d166b2a1` |
| `all-in-one/sources/decoded-original/0668-IdentXmlPart.xml` | `2248e994a0a02cd37c5c5edaca199b3421068feea91e2e8616560e814ef9f6ed` | `fe0f30d1eaae37783b0f03cb090353b3a3de3600` |
| `all-in-one/sources/decoded-original/0672-IdentXmlPart.xml` | `6bfc2ba142d6270c39eb1f13b2886204865af6d46eadc5f410c26981b8da9222` | `2f2790dab4bb2357733112220e0acc41edb6feb6` |
| `all-in-one/sources/decoded-original/0676-IdentXmlPart.xml` | `c58427c5b0ac6c11cdb52e4c6d0461c7b191fae81ccace191048e9f175fcec59` | `1ed67265f69796a4e659f9438e551068037f33a4` |
| `all-in-one/sources/decoded-original/0678-IdentXmlPart.xml` | `51e637e0b9713c028810f2a717b5c3804a3a26c2f1be7e332a4d6bf277bfc382` | `7fafb2297bcdf739bf1d1dd68cebc0d74f2a40cc` |
| `all-in-one/sources/decoded-original/0680-IdentXmlPart.xml` | `fd551ad5d47bbd66c6bcdcc1949aaddf68cc086a3ddf6fb337adc767954c2b95` | `c9049ced1eaed72c5e251a88601d46ddec8c3e50` |
| `all-in-one/sources/decoded-original/0683-IdentXmlPart.xml` | `0c9b569d041cd5babbbeded8a3bdc5d3754927125756b6ac54b7cb991b22fc22` | `662acdb9a06c0ba1c0027e7dd215a28f07d3f02b` |
| `all-in-one/sources/decoded-original/0684-IdentXmlPart.xml` | `6e9b3f173184adcddca503e81e2649022734b6ea3639c1d5ddaf0a08bac00208` | `d67b98b5d5516e0330aae5cfdbee41a3e09206e1` |
| `all-in-one/sources/decoded-original/0685-IdentXmlPart.xml` | `2003d5741a0d707755c5e6e8b737fa106414b87b5b431b97271d9f1a5d343448` | `86bda988d9efedba92ba2f3e4877497d9eb5230a` |
| `all-in-one/sources/decoded-original/0686-IdentXmlPart.xml` | `b450d8ff22f0fffd7a214b2a696af28a03a27834ebf862bfaa822dc9bfb3c8d4` | `8c152d926692a8e15973c980e08e338d29411814` |
| `all-in-one/sources/decoded-original/0688-IdentXmlPart.xml` | `ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda` | `463585759f1ecd94f32362b4fefb000a152f5773` |
| `all-in-one/sources/decoded-original/0692-IdentXmlPart.xml` | `bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037` | `737785d03b5fad43c5b4d451955726d800edb1c0` |
| `all-in-one/sources/decoded-original/0694-IdentXmlPart.xml` | `757ccebdf32d0a168dd787bfa735fe6494eac4c4a9f7a5adc63898a88e8b152d` | `c45e8f3ca4129dc06734f6a12ef79e6ed6528a7d` |
| `all-in-one/sources/decoded-original/network-map.json` | `c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60` | `424430b6b953e43138e5d0a18ca40c949e21cfa1` |
| `all-in-one/sources/hmi_plc_tags.csv` | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` | `cf4c0650e7c7baac350dcb89909b808435704880` |
| `all-in-one/sources/live_index.json` | `14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1` | `e35ccea1f841349c632666c29954b7bcd4f5839e` |
| `all-in-one/sources/source-manifest.json` | `5af6e85994536897fd92f75972534a691e6eb0f067aafe07679c0788fd84e5bf` | `38cf407491d52dc6128cf94ca8a4bddee350de6d` |
| `docs/equipment-standard/INVENTORY.json` | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` | `587c3748ad9224718f95ba06463fee913dae231d` |
| `docs/equipment-standard/WORK-ITEM-TEMPLATE.md` | `4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586` | `e546f39535d2b589e80f97db869ac37ce4d05cfd` |
| `docs/equipment-standard/WORK-STANDARD.md` | `05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99` | `f76a570cc73098632e08759b17934000f7e3a253` |
