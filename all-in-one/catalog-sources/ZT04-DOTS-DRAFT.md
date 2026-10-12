# ZT04 — MV03 위치 계측 고유 원본 조사 초안

- 한 ID: ZT04, P&ID 밸브 위치 계측, sensor/계측, parent MV03, phase2. 부모 완료를 상속하지 않는다.
- 고정 읽기 전용 원본: `source-mv06`, Git `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, v1.12.0. 문서 조사일 2026-10-11 UTC. 모델 런타임 증명 미확인.
- 조사 범위: ZT04 도면 식별/전기 끝점과 대응 후보 MV03 엔코더 읽기·저장·환산·교정·위치 범위 알람. 부모 전체 제어·모터·압력·버너를 재조사하지 않았다.
- 상태: 고유 문서 초안 작성, 현재 실물/CPU/TIA/준공 매핑/정상 극성/현행 보호 설정/복구 모두 미확인. 기능 통합·게시 완료가 아니다.

## 핵심 확인·상충·누락

1. **직접 도면 근거 있음:** OEM FG39/실제 PDF40은 ZT-04를 `ENCODER READING POSITION VALVE / ENCODER`로 명시한다. FG146/실제 PDF147은 MOD17 TM1의 CH0.A/B 입력과 `MV-03 ENCODER ZT-04`를 명시한다. P&ID 이름만으로 발명한 센서가 아니다.
2. **소프트웨어 대응은 후보:** XML의 MV03_Encoder(DB17) → fill_unit1.ACT_CNTV2 → Encoder_CH02 계열 → Data.Pot_MV03 경로는 확인했다. 그러나 ZT04 원문 태그 선언은 찾지 못했고, 도면 CH0 ↔ 프로그램 CH02의 기술 객체/하드웨어 매핑을 확인하지 못했다. 숫자만으로 불일치 또는 동일성을 확정하지 않는다.
3. **독립 AI 주소 없음:** FG146 E21.0/1/2, A9.0/1은 SPARE 표기다. 이를 ZT04의 IW/PIW·아날로그 채널 또는 카운트 주소로 지정하지 않는다. Q1.7/Q2.0은 부모 구동 출력이며 위치 측정값이 아니다.
4. **처리값/극성 구분:** 0514 게이트는 NOT 처리 Inputs.MV03 Close(DB13.X7.6)를 읽는다. 그 처리 비트는 0397에서 raw I7.6을 NOT하여 쓴다. LS20와 ZT04는 별도 장치다.
5. **환산/알람 경계:** CH02 DInt 합산 후 DInt /100, Int 저장 후 선형화다. `CH02_10` 이름을 /10으로 해석하지 않는다. Pot_MV03_OFR DB3.X25.0은 선형화 범위 출력이며 부모 MV03_FAULT의 응답 타이머/명령 누적 고장과 다르다.
6. **미결속 유지:** HSC 23개 데이터 핀 중 SwGate·CountValue만 RefId 있음. 나머지 21개는 참조 없는 ORef다. 오류 ACK나 SetCountValue가 실제 하드웨어에 전달됐다고 단정하지 않는다.
7. **공유 근거:** `MV03-DOTS-DRAFT.md`는 인덱스로 사용했다. 그 초안의 c14bfd1 원본과 본 조사 abcf31c의 선정 sources는 바이트 동일성을 별도 확인한다. 부모 응답 150초·출력·버너·압력 상충은 부모 소유로 연결 재사용하며 ZT04 고장으로 복제하지 않는다.

## 1. 설비·자료 기준

### 1.1 원본과 식별

- `docs/equipment-standard/INVENTORY.json` catalog ZT04: sensor, parent_id MV03, phase2, queue_state planned, existing_detail baseline. 대장의 상태는 문서 또는 실물 완료 증명이 아니다.
- `all-in-one/sources/PID_1684n002I.pdf`, 실제 1쪽, 도면번호 1684n002, Apex I, 기본일 06/04/2011. 개정란 I 15/01/2013 `REMOVED MC-05, CHANGED POWER OF FN-02`; H 01/08/2012 `ADDED MV-06, AND MODIFIED MV-03 COMMAND INSTRUMENT`. 실제 이미지에서 ZT-04, LS-19/20, M17, MV-03 Overflow valve를 확인했다. H 개정이 현재 센서 구성까지 증명하지는 않는다.
- `Electrical_Rev2.pdf` FG39/PDF40 및 FG146/PDF147의 도면 날짜는 27.05.2024, 개정란은 공란이다. 파일명 Rev2를 두 페이지의 개정번호로 일괄 부여하지 않는다.
- `Electrical_Can_Decoating_20241118.pdf` 실제 56/64쪽, CANDC-CONS-C006-056, D-PAGE 6, 개정1 24.11.11 `first draft design`. 시공 설계 자료이며 현재 준공 검증이 아니다.

### 1.2 소유 분리

ZT04는 위치 계측 구성요소다. MV03 모터·열림/닫힘 명령, LS19/20 종단 검출, 접촉기 응답 I2.4/I2.5, 압력 제어 PSH03는 별개 기능 소유다. Pot_MV03라는 소프트웨어 이름은 도면의 ENCODER를 포텐셔미터 또는 4–20mA 전송기로 바꾸는 근거가 아니다. 제조사/형식/PPR·회전방향/전압허용오차/기계결합/현재 설치 위치는 미확정이다.

## 2. I/O·HMI — 물리·내부·지역 변수를 분리

이하 `NNNN`은 `all-in-one/sources/decoded-original/NNNN-FlgNet.xml`, 선언은 같은 폴더의 `NNNN-IdentXmlPart.xml`이다. 주소는 고정 백업의 SSD AO(bit offset)와 DepDBBlock TOD 결속으로 읽었으며 현재 주소 확인이 아니다.

| 항목 | 선언/원본 문맥 | 형식·백업 위치 | 의미/미확정 |
|---|---|---|---|
| ZT04 물리 측정 | FG39/PDF40 → FG146/PDF147 | 펄스 A/B 배선, 아래 끝점 표 | 독립 AI 주소 미확보 |
| MV03_Encoder | 0673 RID340, NID47 UID23 InstanceDB | DB17, HSC 인스턴스 | 기술 객체 하드웨어 결속 미확정 |
| SW_GATE2 | 0676 Global RID236 NID47 UID25; NID32 UID1170 Write/1179 Read | Bool DB91.X23.2, AO186 | 카운터 소프트웨어 gate |
| ACT_CNTV2 | 0676 Global RID238 NID47 UID45 Write/NID32 UID1172 | DInt DB91.DBD164, AO1312 | HSC CountValue 출력 저장 |
| Encoder_CH02 | 0676 Global RID198 NID30 UID946 Write/NID32 UID1171 Read·1183 Write | DInt DB8.DBD8, AO64 | 저장 누적값, 실제 각도 단위 아님 |
| Encoder_CH02_10 | 0676 Global RID242 NID32 UID1178·1181 Write/1186 Read | Int DB8.DBW40, AO320 | /100 후 저장값 |
| CNT_Act_2 / CNTV2_100 | 0677 InterfaceAccess Local RID197/240, NID32 UID1173/1176 Write | DInt, 지역 AO464/176 | 전역 DB 주소를 부여하지 않음 |
| Data.Pot_MV03 | 0676 Global RID234 NID32 UID1189 Write | Int DB1.DBW144, AO1152 | 선형화 결과, %/도 단위 미확정 |
| ZERO_TRASM_MV03 / COEFF_TRASM_MV03 | 0676 Global RID233/232 NID32 UID1188/1187 | Int DB4.DBW200/202 | 현행 교정값 미확정 |
| Pot_MV03_OFR | 0676 Global RID436 NID32 UID23 Write | Bool DB3.X25.0, AO200 | 선형화 범위 결과 |
| Inputs.MV03 Close | 0676 Global RID446 NID32 UID22 | Bool DB13.X7.6, AO62 | raw I7.6와 반전된 처리값 |
| ResetEncoderProcedure_MV03 | 0619 Global RID191 NID13 UID23 Read/52 Write | Bool DB41.X50.6, AO406 | 요청 비트, 복구 완료 표시 아님 |
| EM_OK | 0678 SimpleAccess Global RID173 NID47 UID24/NID32 UID1168 | Bool Input AO156=I19.4 | 호출 조건; 안전 인증 증명 아님 |

DB 번호: 0674 DepDBBlock RID177 fill_unit1 TOD91, RID191 Memory encoder TOD8, RID11 Data TOD1, RID8 Coeff TOD4, RID354 Allarm TOD3, RID445 Inputs TOD13. HMI_DB TOD41/엔코더 TOD17은 0618 관련 선언을 참조한다.

`hmi_plc_tags.csv`에서 RESET_ENC_MV03 → `DB41,X50.6`, ID00465, dde.cfg 설정을 확인했다. ZT04/Pot_MV03/COEFF·ZERO_TRASM_MV03 표시 태그는 이 CSV의 해당 이름 검색에서 미확보다. 태그 존재는 버튼/스크립트 이벤트나 실제 쓰기 증명이 아니다. 부모 MV_03의 LimitSwitchOpen/Close, OutputOpen/Close는 ZT04 연속 위치 태그가 아니다.

정확 태그 경계검색: decoded-original XML 695개에서 대소문자 무시 `ZT[ _-]?0?4` 0건. 같은 패턴의 HMI CSV 검색도 0건이다. 이는 텍스트 이름 미확보이고 모든 간접주소/바이너리/TIA 기술 객체 부재를 입증하지 않는다.

## 3. 제어 구조 — 위치 신호 관련 후보 경로

### 3.1 HSC 읽기 0508, LAD1758, analog input conversion, NID47

- NOT Simulation(1) Part75: W74/ORef76/RID344 (0678, Memory AO1440=M180.0) → W77 → EM_OK Contact21, operand W49/ORef24/RID173 → W50 → LRef22.en.
- LRef22 RID330은 0679 Instruction High_Speed_Counter, NID47 UID22 Call; Instance23 RID340은 0673 MV03_Encoder DB17이다. 이름/자료형/문맥을 함께 대조했다.
- SwGate W51/ORef25 RID236은 SW_GATE2 읽기. CountValue W71/ORef45 RID238은 ACT_CNTV2 쓰기다.
- RefId 없는 핀: CaptureEnable(W52/O26), SyncEnable(53/27), ErrorAck(54/28), EventAck(55/29), SetCountValue(56/30), StatusHW(57/31), StatusGate(58/32), StatusUp(59/33), StatusDown(60/34), CompResult0(61/35), CompResult1(62/36), SyncStatus(63/37), CaptureStatus(64/38), CapturedValue(65/39), ZeroStatus(66/40), PosOverflow(67/41), NegOverflow(68/42), Error(69/43), ErrorID(70/44), MeasuredValue(72/46), CompareMeasuredValue(73/47).
- 빈 ORef를 FALSE/0, 미사용 또는 임의 DB 주소로 채우지 않는다. 선언상 CountValue DInt, ErrorID Word, MeasuredValue Real도 서로 구분한다. 조건의 정적 연결만 읽었고 중지 시뮬레이터를 실행·분석 확장하지 않았다.

### 3.2 누적·환산 0514, LAD1764, NID32

1. EM_OK Contact1217 operand W1191/ORef1168 → W1218가 Contact1219, Contact1221, CRef1163.en으로 분기한다.
2. NOT Inputs.MV03 Close Contact1219 operand W21/ORef22 RID446 → W1220 → Coil1129(SW_GATE2 W1193/ORef1170) 및 Add1134.en.
3. Add1134 DInt: in1 W1194/ORef1171=Encoder_CH02, in2 W1195/ORef1172=ACT_CNTV2; out W1196/ORef1173=CNT_Act_2 Local. eno W1197 → Div1138.en.
4. Div1138 DInt: in1 W1198/ORef1174=CNT_Act_2, in2 W1199/ORef1175=100(0675 Literal RID211); out W1200/ORef1176=CNTV2_100 Local. eno W1201 → Move1142.en; W1202/ORef1177 → W1203/ORef1178=Encoder_CH02_10 Int.
5. NOT SW_GATE2 Contact1221 W1205/ORef1179 → W1222: Move1151 W1206/ORef1180 Int0 → W1207/ORef1181 CH02_10; Move1156 W1208/ORef1182 INT#0 → W1209/ORef1183 DInt CH02. 타입 경계를 보존한다.
6. 선형화 CRef1163/CodeBlock1190 RID5는 0672 FCBlock Signal linearization, FC63, NID32 UID1190 Call에 결속된다. IN0 W1211/ORef1185=ON(M0.0); Analog_input W1212/ORef1186=CH02_10; Coeff W1213/ORef1187; Zero W1214/ORef1188; OutValue W1215/ORef1189=Pot_MV03; Out_of_range W24/ORef23=Pot_MV03_OFR.

게이트 상태와 산술 ENO가 자료 갱신에 관계한다. 이 정적 경로를 일정 주기 보장·기구 위치 보장·실제 개도%로 설명하지 않는다. EM_OK=0에서 0514 전체를 실행하지 않는 조건과, 분기 조건이 false일 때 개별 값 쓰기의 차이를 구분한다.

### 3.3 추가 저장과 raw/처리값

- 0511 LAD1761 NID30: NOT EM_OK Contact963 W951/ORef940 → W964 Move927.en; in W956/ORef945=Local CNT_Act_2(0677 RID197) → out W957/ORef946=Encoder_CH02(0676 RID198 Write). 부모 색인을 재사용하되 이 고유 가지를 직접 확인했다. 지역변수 수명·호출 순서·정전시 저장 완전성은 미확정이다.
- 0397 LAD1070 NID1: raw MV03_Close 0627 SimpleAccess RID154 Input AO62=I7.6 → ORef152/W155 Contact149 → W156 Not150 → W157 Coil151 → W158/ORef153, 0629 Global RID155 Inputs.MV03 Close AO62. 별도 NOT 쓰기가 존재하므로 raw/DB 처리값을 동일 극성으로 설명하지 않는다. 주변 Word 전송 전체를 본 조사에서 재분석하지 않았다.

### 3.4 교정 요청 경계 0353, LAD1707, NID13

ResetProc Contact22(W25/ORef23 RID191) → W28 → 처리 Close Contact26(W29/ORef30 RID176) → W33 Move32.en. Move32는 **DisableENO=true** 속성과 eno 연결 W38을 동시에 갖는다. in W34/ORef36=0(DInt,0620 RID194), out1 W35/ORef37=NewCountValue(0619 RID193).

W38 → NOT SetCountValue Contact40(W39/ORef41 RID195) → W42 Coil44(W43/ORef45 RID195) → W50 RCoil48(W51/ORef52 RID191)로 요청 Reset. 이 사슬을 성공 ACK로 단정하지 않는다. DisableENO 속성의 실제 런타임 효과도 현 프로젝트에서 미검증이다.

DB17 NewCountValue는 SSD S=S AO320, SetCountValue는 SSD S=IO AO288 Bool(OD S8/SD BB1)이다. 내부 세그먼트 offset를 단순 절대주소로 발명하지 않는다. 특히 0508 SetCountValue ORef30에 RefId가 없어, 여기 쓴 멤버와 HSC 호출 핀을 이름만으로 연결하지 않는다. 부모 출력0345에도 교정 요청 영향이 있다는 것은 부모 초안 공유 근거이며 현장 교정 절차/명령 권고가 아니다.

### 3.5 다른 쓰기·해석 범위

위 표의 직접 쓰기는 NID/RID/UID/형식을 결속한 범위다. 부모 초안은 Data.Pot_MV03에 과거 별도 블록 쓰기 후보를 기록했으므로 단일 Writer·현재 최종값의 유일 경로라고 주장하지 않는다. 이번에는 중지 블록 조사로 확대하지 않았다. HMI/간접주소/현재 온라인 쓰기 전체 목록 및 OB 실제 호출 순서는 미확정이다.

## 4. 전기 전달 경로 — 실제 렌더 4쪽 확인

| 대상 | 현장측 → 단자/선 → 모듈측 | 직접 근거와 경계 |
|---|---|---|
| ZT04 공급 + | B +24Vdc → X1/85 → 35.1 → TM1 단자9 24VDC | FG39/PDF40, FG146/PDF147; 35/2 공급 연속참조는 이 범위 밖 |
| ZT04 공급 귀로 | C −0Vdc → X1/86 → 35.2 → TM1 단자10 M | 같은 2쪽; 센서 허용전원은 명판 미확보 |
| A상 후보 | D → X1/87 → 39.1 → MOD17 TM1 단자1 CH0.A | 도면 핀 표기를 그대로 보존 |
| B상 후보 | E → X1/88 → 39.2 → MOD17 TM1 단자2 CH0.B | 도면 핀 표기를 그대로 보존 |
| 실드 | X1/89 → 39SCH1 → FG146 실드접지 표시 | 실제 접지 시공·연속성 미확인 |
| 미배선 표시 | TM1 단자3 CH0.N | 해당 페이지에 현장선 표시 없음; 실물 미사용 단정 금지 |

FG146 상단 A9.0/A9.1 단자7/8 및 E21.0/E21.1/E21.2 단자4/5/6은 SPARE. CPU 515, MOD17 표기는 도면 설계 식별이며 현재 CPU 모델/슬롯 확인을 대신하지 않는다. `TECNOLOGY MODULE TM TIMER`와 TM1 표기를 보존한다.

FG39 오른쪽 LS19/20 NC11/12와 X1/90~93, E7.5/7.6은 종단 위치 회로다. ZT04의 X1/85~89와 구분한다. +24Vdc10.7 상단 버스를 ZT04의 실제 B 공급과 바로 연결하지 않는다. ZT04 B/C는 하단 35.1/35.2 경로에 그려져 있다.

시공 실제 PDF56의 고유 두 행:

| 행 | 케이블 ID | FROM → TO | 사양/경로 표기 |
|---|---|---|---|
| 6_3 | =FLA+MV03-FLO1TB1C | CR → MV-03 / FLO1TB1 / ZT-04 | TM, CVV-S,4S,1.0,spare0;100 LBD1→E100;Adjustment7,LEN42 |
| 6_17 | =FLA+MV03-ZT04A | MV-03 FLO1TB1 → MV-03 ZT-04 | TM,CVV-S,4S,1.0,spare0;LAD1 E300→LAD1→E1400;Adjustment5,LEN6 |

따라서 공유함까지의 trunk와 센서 branch가 별도 행이다. LEN은 설계길이이며 실제 시공 측정치가 아니다. 이 케이블표에는 X1/85~89와 FLO1TB1 내부 단자 번호를 결속하는 상세가 없어, 도면의 OEM 끝점과 시공 중계함 상세를 하나의 검증된 준공 배선으로 합치지 않는다. 가림 행 6_7~6_10은 조사 근거로 사용하지 않았다.

## 5. 알람·복구 — ZT04 후보 위치 경로와 부모 고장 분리

### 5.1 선형화 범위 알람

공통 FC63 본문 0291(LAD1658,NID1)/0014(LAD1659,NID2), 선언0611/0612를 연결 재사용하되 핵심 Part/Wire를 직접 대조했다.

- IN0 Contact255 W220/ORef196(RID1 Local) → W256; Analog_input Int >−1382 Gt258(W30/31,ORef32/33) → W25 → ≤32767 Le161(W27/28,ORef29/34) → W26 Convert164.
- Int→DInt Convert164/167, Add170(입력+Zero), Convert174(Coeff), Mul177, Div181(28000), Move185 OutValue Int. ENO 사슬 W227/230/234/237/241/245가 존재한다. 실수식이나 센서 물리규격으로 바꾸지 않는다.
- >32767 Gt190 또는 ≤−1382 Le259 → OR47 W49 → Move193, in W252/ORef218=−9999(0612 RID21), out W253/ORef219=Local OutValue(RID19). eno W21 → 일반 Coil23 W22/ORef24=Local Out_of_range(RID26).
- 별도0014는 NOT IN0 Contact171(W168/ORef165) → W172 Move162, 0 W169/ORef166 → OutValue W170/ORef167. 이 네트워크에는 별도 알람 Reset Coil이 없다.

ZT04 후보 값의 호출측 0514 Out_of_range W24/ORef23은 DB3.X25.0에 결속된다. 확인 범위에서 위치 OFR 전용 지연 타이머·S/R 래치 없음. 이를 모든 프로그램에 해당하는 부재 증명으로 확대하지 않는다. 호출이 생략되거나 다른 쓰기가 있으면 실제 갱신 상태를 별도로 확인해야 한다.

### 5.2 부모와 공유하는 사항

부모 초안의 MV03_FAULT DB3.X4.3은 0159의 **S5T#150S** 방향 접촉기 응답 감시와 0351/0352의 방향 명령 누적 초과 등 부모 경로다. ZT04 위치 OFR와 같은 비트가 아니며 150ms 또는 ZT04 신호불량 검출시간으로 복제하지 않는다. 부모 고장식/Reset 전체는 MV03 초안에서 재사용하고 본 조사에서 반복하지 않았다.

HSC Error/ErrorID/ErrorAck/EventAck는 0508에서 RefId가 없어, 대응 경보 번호/공통Reset 연결/실제 복구 절차를 발명하지 않는다. 교정요청 해제, OFR 비트 변화, 모터고장 Reset, 실제 위치 복구는 서로 다른 관찰이다.

## 6. 증상별 관찰 기록 — 조작 절차 아님

| 증상 | 읽기 전용으로 대조할 자료/관찰 | 배제해야 할 성급한 결론 |
|---|---|---|
| 화면 위치가 멈춤 | 승인된 기존 기록에서 시각 일치한 EM_OK, 처리 Close, SW_GATE2, ACT_CNTV2, CH02/CH02_10, Pot_MV03, 원본 프로젝트 식별 | Q 출력 또는 접촉기 응답만으로 엔코더 고장 확정 금지 |
| 위치가 0으로 바뀜 | 0514 NOT SW_GATE2의 2개 Move0, 0511 저장, FC63 NOT IN0 값 쓰기, 요청/호출 기록 | 기계가 닫혔다/영점 교정 성공이라는 해석 금지 |
| −9999 또는 OFR | FC63 입력 Int 범위와 계수/Zero·형식, 실제 표시 태그 주소 및 갱신시각 | OFR를 하드웨어 단선 또는 부모 응답고장과 동일시 금지 |
| 닫힘 종단값과 위치값 불일치 | LS20 raw I7.6/처리 DB13.X7.6 구분, 기계 위치 사진·명판·캠 기준, A/B 배선 준공도 | raw/처리 극성을 같게 두거나 엔코더와 LS20을 같은 센서로 병합 금지 |
| 재기동 뒤 값 변화 | 저장 경로 0511의 지역값 수명·현재 호출순서·실제 DB retentivity 설정 자료 | 제목 power-off만으로 전원차단 위치보존 보장 금지 |
| Reset 요청 후 위치 불명 | DB41.X50.6, 내부 NewCountValue/SetCountValue, HSC 핀 매핑·상태 증거 | 요청 Reset=센서 영점/기구 복구 완료로 표시 금지 |

기록 필드: 관찰자, UTC/현장 시간대, 설비 위치/태그 사진, 자료 취득 시각, 값/자료형/단위, 현재 프로젝트 식별, 비교 원본, 배제 결과, 승인된 조치 및 이후 복구 증거. 본 문서는 현재 현장 기록을 수집하거나 값을 변경한 결과가 아니다. 강제 I/O·배선 우회·리셋/교정 실행·보호값 조정은 제안하지 않는다.

## 7. 완료·누락·인계

| 영역 | 상태 | 완료 경계 |
|---|---|---|
| 설비·자료 기준 | 문서 적용 | 대장 한 ID·P&ID·도면 식별, 현재 실물 동일성 보류 |
| I/O·HMI | 부분 적용 | 도면 A/B 끝점·후보 DB·HMI 요청 확인, ZT04 직접 PLC 심볼/표시 이벤트 미확보 |
| 제어 | 부분 적용 | 엔코더 후보 고유 4네트워크/NOT 처리/선형화 대조, 현재 호출/매핑 미확정 |
| 전기 | 부분 적용 | P&ID1,OEM40/147,시공56 렌더 직접 확인, 중계함 단자 상세·준공 연속성 미확정 |
| 알람·복구 | 부분 적용 | Pot_MV03_OFR 일반 Coil·부모 고장 분리, HSC진단/실제복구 미확정 |
| 증상 관찰 | 문서 적용 | 관찰표 작성, 현장 시험·조작 미수행 |
| 완료 기준 | 초안 완료 | 통합/UI/기록/게시/TIA/현장 완료 아님 |

필요 자료와 통과 기준:

1. 현 ZT04 명판·기계 장착 위치·MV03 연결 사진과 준공 P&ID: 문서 태그와 설치물 식별 일치 여부.
2. 현재 TIA 기술 객체/HSC DB17 하드웨어 식별·TM1 슬롯/채널·입출력 파라미터: MOD17 CH0 ↔ MV03_Encoder ↔ ACT_CNTV2 대응을 실제 설정으로 확인.
3. 승인된 준공 단자/케이블 결선표: X1/85~89 ↔ FLO1TB1 내부 단자 ↔ ZT04 B/C/D/E/실드 전구간 결속.
4. 현 HMI 프로젝트와 위치 표시/교정 이벤트 자료: 요청·표시값·쓰기 대상·갱신 경로 결속.
5. 현재 프로젝트의 호출 순서/다른 쓰기·보존 설정·교정 계수/Zero의 승인 근거와 취득시각. 값 변경 없이 먼저 읽기 전용 자료로 확인.
6. 적격 담당자가 제공하는 실제 위치/종단/계수 비교 및 복구 기록. 본 문서의 백업 상수로 현장 허용값을 결정하지 않는다.

이 자료가 없으면 현장 보류를 유지한다. 새 자료 없이 부모 전체 반복조사·센서 모델 추측·별도 AI 주소 생성으로 확대하지 않는다.

### 수행·보존

2026-10-11 12:50:15 UTC 지시 확인 시작, 12:50:51–12:51:46 UTC 원본 PDF 렌더·확대 확인, 12:51:16–12:52:47 UTC XML/선언/핀·상수 정적 대조. 마지막 검사/완료 시각은 부록 검사 기록에 실제 시각으로 저장한다.

수행은 원본 읽기, 자체 XML 파싱, PDF 렌더, 해시/Git blob 내용 비교, 이 초안과 ZT04 추출물 작성뿐이다. 원본 build/test/generator·시뮬레이터·PLC·현장·보호값·SEJIN 변경·운영자료 복제·로컬 Mac 접근·재위임 없음. 도면/래더 비교 자료는 작성했으나 앱 기록/백업·선택복원/보고서UI·게시 기능은 구현·시험하지 않았다.

## 부록 A. 선정 원본 SHA-256 / 고정 Git blob 전체표

선정 31개 전체이며 내용일치 Yes는 고정 commit blob 바이트와 작업 원본의 일치다. 해시수는 의미 검토 수가 아니다. 0159/0351/0352는 부모 알람 경계 연결 재사용용이며 본 조사 전부 의미 검토한 것으로 세지 않는다. 선정 sources의 이전 부모 c14bfd1 바이트도 모두 동일하다. 원본 경로는 고정 저장소 루트 상대경로다.

| 원본 경로 | SHA-256 | Git blob SHA-1 | 고정 내용일치 |
|---|---|---|---|
| `docs/equipment-standard/INVENTORY.json` | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` | `587c3748ad9224718f95ba06463fee913dae231d` | Yes |
| `all-in-one/sources/PID_1684n002I.pdf` | `2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b` | `8c83a59fefd5b8b651ec3537ea4236a073f5e109` | Yes |
| `all-in-one/sources/Electrical_Rev2.pdf` | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` | `f610fd7c7ce14ae951b00cff57b969259bfb389d` | Yes |
| `all-in-one/sources/Electrical_Can_Decoating_20241118.pdf` | `3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd` | `0ee6b6f8361c5790864dbba4bbd9d55e8e7c08f8` | Yes |
| `all-in-one/sources/hmi_plc_tags.csv` | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` | `cf4c0650e7c7baac350dcb89909b808435704880` | Yes |
| `all-in-one/sources/decoded-original/network-map.json` | `c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60` | `424430b6b953e43138e5d0a18ca40c949e21cfa1` | Yes |
| `all-in-one/sources/decoded-original/0508-FlgNet.xml` | `21f461aced38216c15a873f61b461c962662aa11367309835c7203508f804bb4` | `a31b3473212775d5a2264223d2853240104ce07c` | Yes |
| `all-in-one/sources/decoded-original/0514-FlgNet.xml` | `3826044da205b26e31f400232a55aa240eef8a4933e532d0bf9a3bccee2d19c5` | `efecda3b942fba7ce4ab9cd8c773136a6a021f83` | Yes |
| `all-in-one/sources/decoded-original/0511-FlgNet.xml` | `a4bf314bf817f0f666a0c9fdd26df134cedeed8666819c7a3e8e6438850eace6` | `2730bc98903fc1a89effa1911c5ac82ddd7b4957` | Yes |
| `all-in-one/sources/decoded-original/0353-FlgNet.xml` | `062854b25c5afacb34e53ce0ee7cd8c660cd9a0f5b79a02d8a5fbed89c794766` | `19b9493c88c95031ee327dc9e567bc7780fd4839` | Yes |
| `all-in-one/sources/decoded-original/0397-FlgNet.xml` | `bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834` | `4ab8370493c4e28fc1eabeeebe2743d27f0c4021` | Yes |
| `all-in-one/sources/decoded-original/0291-FlgNet.xml` | `fe0b92f074eba25148ce34084649af3d968962558d652727f1eea19f3e3c2550` | `1418fb2ed172c6df694a5eb8bf2dffd0b177653b` | Yes |
| `all-in-one/sources/decoded-original/0014-FlgNet.xml` | `2e814adbaac6bab99bc668bfdab74f0fc90576324d0b88728951683869cfac30` | `4d164b074fcc13a8f97da9e24382cc169ef29555` | Yes |
| `all-in-one/sources/decoded-original/0672-IdentXmlPart.xml` | `6bfc2ba142d6270c39eb1f13b2886204865af6d46eadc5f410c26981b8da9222` | `2f2790dab4bb2357733112220e0acc41edb6feb6` | Yes |
| `all-in-one/sources/decoded-original/0673-IdentXmlPart.xml` | `450ef74e2d2fb65dfbb5f6bad9e28ccacf6bf0caf64327a0e20aff84d6e40f58` | `1957bff7dd1beffcb6e2a40d6a541c1751753548` | Yes |
| `all-in-one/sources/decoded-original/0674-IdentXmlPart.xml` | `4770702f519bacda69202bb2f7733d983074bda90964360c238f990d9d08fd84` | `f210593944547b63eab10c667348711413600aab` | Yes |
| `all-in-one/sources/decoded-original/0675-IdentXmlPart.xml` | `b1902886927d8403fab736d9c8ffe73f2fbc8ce4b7ca7c345144964668b051c3` | `d82a33b173c8dc0737fd890eb2a63a88a07d0831` | Yes |
| `all-in-one/sources/decoded-original/0676-IdentXmlPart.xml` | `c58427c5b0ac6c11cdb52e4c6d0461c7b191fae81ccace191048e9f175fcec59` | `1ed67265f69796a4e659f9438e551068037f33a4` | Yes |
| `all-in-one/sources/decoded-original/0677-IdentXmlPart.xml` | `69922fcc5c67d00cdf1c5f712efa3db7638d20c88318d35fe6196467796ab1e3` | `b9437406a7e24f073ef88b8369cacc9ad4ecc5ac` | Yes |
| `all-in-one/sources/decoded-original/0678-IdentXmlPart.xml` | `51e637e0b9713c028810f2a717b5c3804a3a26c2f1be7e332a4d6bf277bfc382` | `7fafb2297bcdf739bf1d1dd68cebc0d74f2a40cc` | Yes |
| `all-in-one/sources/decoded-original/0679-IdentXmlPart.xml` | `d0fcb93e188c8ae2ae0c0423f0b78b129bf3c168e33a6855262d34b8682b9b56` | `e8d8a014609871082bf5cfca0f9ab9b78136e920` | Yes |
| `all-in-one/sources/decoded-original/0618-IdentXmlPart.xml` | `0c6762de9cdf0e294317f7463bea3d8e6df5673d333d9b1826ebd17a7ded044c` | `9eec0dbd8abde4aa7295f77b63ad473f895f274b` | Yes |
| `all-in-one/sources/decoded-original/0619-IdentXmlPart.xml` | `85694bb5b696e31e6a1217431112e5b750516c4f94078d6e127d4394a8b80456` | `11f0502c84a1f319a21459a35c0dc1c6ce8e8f36` | Yes |
| `all-in-one/sources/decoded-original/0620-IdentXmlPart.xml` | `da97226a148a1a8babaea67db412761a718b7e7537212b7807e8ea27d000d2d3` | `dc88b5e87ad3331928f14fcf647673a26fb70b6b` | Yes |
| `all-in-one/sources/decoded-original/0627-IdentXmlPart.xml` | `08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb` | `61ebc0abbb2ca160e11e1da400a3f14a397d8bc5` | Yes |
| `all-in-one/sources/decoded-original/0629-IdentXmlPart.xml` | `67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972` | `058129bb01e27f7a6a0d0293f332d745e5bab74e` | Yes |
| `all-in-one/sources/decoded-original/0611-IdentXmlPart.xml` | `0d583915a261703954da22c176ba9f81338ad13ea2810e7cd5f7de8aa1bfa089` | `bad6b16fb32a32d47d882f48754994887457872b` | Yes |
| `all-in-one/sources/decoded-original/0612-IdentXmlPart.xml` | `95b545d4964d371ebfc107894ea90b8b1d0d7ab5d3a70e643f8ce539063c0f38` | `7cc782d33d07ef225c2104f3e7c9fbd31f7c7467` | Yes |
| `all-in-one/sources/decoded-original/0159-FlgNet.xml` | `5598abbad86ed26fa8dd17fc3eca3e1c0b7941a2798db6ae1e2472a7ca448d2a` | `d8d368282fd2eb4c55d877c57c64ad869a778fa2` | Yes |
| `all-in-one/sources/decoded-original/0351-FlgNet.xml` | `1448cd179747074ae5ac3647c52e47950d18e0d90fa2f1cb155dbb24af50a7f6` | `6af091ec6d9a7840c2e5f532bf232fcb1c67fa0c` | Yes |
| `all-in-one/sources/decoded-original/0352-FlgNet.xml` | `03e2d68dda289fcb7e7738c2f52e675890b252f5b526cab1ec2049323ab30d75` | `3da6a9790606a29f9423bfc7001f377ffb02899e` | Yes |

## 부록 B. 검사 결과

- 실제 완료 검사 시각: 2026-10-11T12:56:47.394131+00:00 UTC.
- 선정 31개 fixed blob 일치, 그중 sources는 부모 c14bfd1 바이트 동일. 전체 sources 보존 712파일 fixed Git blob 일치, 중지5자산 SHA-256/바이트 일치. 전체 보존 해시는 XML 전수 논리검토가 아니다.
- 원본 Git status: clean. 7영역 존재, HSC 미결속 ORef 21개, 고유 도면4쪽 실제 렌더/시각확인. 핵심 FlgNet 7개(0397은 닫힘 반전 가지), 관련 선언·상수 문맥 검토.
- `extracts/ZT04/source-hashes.json`, `source-preservation-hashes.json`, `stopped-assets-preservation.json`, `static-review.json`, `search.json`, `stages.json`은 재현/검사용 별도 추출물이다.
- XML695파일 검색은 이름 경계 탐색만이며 전 네트워크 의미검토를 뜻하지 않는다. TIA/현장/보호/시뮬레이터/생성기/게시 검사 미수행.
