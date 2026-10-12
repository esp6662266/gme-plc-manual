# ZT06 — MV06 위치 계측 고유 원본 조사 초안

- 대상 한 ID: ZT06, sensor/계측, parent_id MV06, phase2. 부모 MV06 완료를 상속하지 않는다.
- 고정 원본: `gme-research/source-mv06`, Git `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, v1.12.0. 2026-10-11 UTC 정적 문서 조사. 모델 런타임 증명 미확인.
- 적용 기준: AGENTS, rollout SKILL, WORK-STANDARD, WORK-ITEM-TEMPLATE, INVENTORY 및 BATCH18 범위. 원본/코드/버전/대장/배포/운영/SEJIN 변경 없음. 생성기·시험·시뮬레이터 작성/수정/생성/실행/행동시험 없음.

## 핵심 확인·상충·누락·공유 근거

1. OEM FG33/실제 PDF34는 ZT-06를 ENCODER READING POSITION VALVE로, FG148/실제 PDF149는 MV-06 ENCODER ZT-06와 CH0.A/B로 명시한다. 독립 아날로그 IW 채널로 만들지 않는다.
2. 소프트웨어 후보는 MV06_Encoder DB19 → ACT_CNTV4 → Encoder_CH04 → Pot_MV06다. 물리 CH0와 프로그램 CH04 번호만으로 동일성/불일치를 판정하지 않는다. 기술 객체·모듈 매핑과 현장 센서 명판 미확보.
3. 0516은 **NOT raw MV06_Close I7.0**를 사용한다. ZT04의 NOT 가공 Inputs.MV03 Close 경로 또는 입력 반전을 복제하지 않는다. LS41은 별도 종단센서이며 ZT06의 펄스값이 아니다.
4. /100 DInt 연산 후 Int 저장이다. CH04_10이라는 이름을 /10으로 읽지 않는다. Pot_MV06_OFR DB3.X25.2는 범위 환산 출력이며 부모의 150ms 응답/누적 고장이 아니다.
5. HSC 데이터 23핀 중 SwGate/CountValue만 RefId가 있다. 나머지21개 ACK·오류·상태 핀은 미결속으로 남긴다. 전용 RESET_ENC_MV06 태그/교정 절차를 확보하지 못했다.
6. 시공 PDF56 행6_6의 MV05→ZT06와6_20의 MV05→ZT05 명칭 상충, PDF58 FLO4TB2A 중복 ID를 보존한다. ZT06을 MV05로 재배정하지 않는다.
7. MV06-DOTS-DRAFT.md와 ZT02~04 중 ZT04 초안을 공유 근거 색인으로 사용했다. 부모 전체 압력·방향·공유 인버터를 재조사하지 않았다. 본문 0510/0511/0516·선언 및 도면 끝점은 고정 원본에서 독립 확인했다. 공통 FC63은 같은 고정 입력을 연결 재사용하며 핵심 핀을 재대조했다.

## 1. 설비·자료 기준

INVENTORY catalog ZT06은 parent MV06, queue_state planned, existing_detail baseline이다. 이는 실물/문서 완료 상태가 아니다. TASK3-BATCH18-SCOPE의 role은 P&ID MV06 위치 계측 태그이며 현재 엔코더/TM 채널 동일성은 확인 항목이다.

`all-in-one/sources/PID_1684n002I.pdf` 실제1쪽에는 Overflow valve MV-06, M14, ZT-06, LS-34/35가 표시된다. 도면1684n002, Apex I, 기본일06/04/2011. 개정란에는 MV-06 추가 및 MV-03 command instrument 변경, 마지막 I의 MC-05 제거/FN-02 출력 변경이 있다. 이 과거 도면은 현재 설치 증명이 아니다.

`Electrical_Rev2.pdf` FG33/PDF34, FG148/PDF149는 날짜27.05.2024, 두 페이지 개정란 공란이다. 파일명 Rev2를 각 페이지 개정으로 만들지 않는다. 시공 `Electrical_Can_Decoating_20241118.pdf` 실제56/64와58/64는 각각 CANDC-CONS-C006-056/D-PAGE6, CANDC-CONS-C008-058/D-PAGE8, 개정1 24.11.11 first draft design이다. 준공/현장 결선 확인으로 승격하지 않는다.

ZT06 계측, MV06 모터 M14 및 방향출력, LS34/35 또는 OEM LS40/41 종단 위치, 접촉기 응답, PSH02 압력, MV02/MV05/MV06 공유 인버터는 기능 소유가 다르다. Pot 이름만으로 포텐셔미터·4–20mA 센서로 바꾸지 않는다.

## 2. I/O·HMI

아래 NNNN은 `all-in-one/sources/decoded-original/NNNN-FlgNet.xml` 또는 명시한 IdentXmlPart다. NID는 원본 네트워크, RID는 선언, UID는 해당 문맥 요소다. 주소는 백업 선언 AO bit offset와 DepDB TOD의 결속이며 현재 CPU 주소 검증이 아니다.

| 항목 | 원본 선언/문맥 | 형식·백업 주소 | 경계 |
|---|---|---|---|
| MV06_Encoder |0673 RID350, NID49 UID24 InstanceDB|DB19, High_Speed_Counter|하드웨어 매핑 미확정|
| SW_GATE4 |0676 Global RID261, NID35 UID1482 Write/1491 Read, NID49 UID27|Bool DB91.X23.4, AO188|소프트웨어 gate|
| ACT_CNTV4 |0676 Global RID263, NID49 UID47 Write, NID35 UID1484|DInt DB91.DBD180, AO1440|CountValue 출력|
| Encoder_CH04 |0676 Global RID204, NID30 UID950 Write, NID35 UID1483 Read/1495 Write|DInt DB8.DBD16, AO128|누적 저장|
| Encoder_CH04_10 |0676 Global RID267, NID35 UID1490/1493 Write,1498 Read|Int DB8.DBW44, AO352|/100 후 값|
| CNT_Act_4 / CNTV4_100 |0677 InterfaceAccess Local RID203/265, NID35 UID1485/1488 Write|DInt, Local AO528/240|전역 DB주소 부여 금지|
| Pot_MV06 |0676 Global RID273, NID35 UID1501 Write|Int DB1.DBW136, AO1088|개도%/각도 단위 미확정|
| Coeff_MV06 / Zero_MV06 |0676 Global RID271/272, NID35 UID1499/1500|Int DB4.DBW224/222|현행 계수/영점 미확정|
| Pot_MV06_OFR |0676 Global RID440, NID35 UID23 Write|Bool DB3.X25.2, AO202|위치 환산 범위 결과|
| MV06_Close |0678 SimpleAccess Global RID260, NID35 UID1481|Bool Input AO56=I7.0|raw 종단 입력|
| EM_OK |0678 SimpleAccess Global RID173, NID49 UID26/NID35 UID1480/NID30 UID940|Bool Input AO156=I19.4|호출 조건, 안전 인증 주장 아님|
| ON |0678 SimpleAccess Global RID1, NID35 UID1497|Bool Memory AO0=M0.0|FC63 IN0|

0674 DepDBBlock RID177 fill_unit1 TOD91, RID191 Memory encoder TOD8, RID11 Data TOD1, RID8 Coeff TOD4, RID354 Allarm TOD3를 직접 대조했다. Global/Local 및 Int/DInt/Bool을 구별한다.

HMI CSV에는 MV_06의8행이 있다: Allarme1 DB11.X28.2(ID0040E), Flag_CLOSE DB2.X10.6(0040D), Flag_OPEN DB2.X10.5(0040C), LimitSwitchClose DB11.X28.4(0040B), LimitSwitchOpen DB11.X28.3(0040A), OutputClose DB11.X28.1(00312), AutoMan DB2.X6.5(00047), OutputOpen DB11.X28.0(00046). 모두 부모 MV06 표시/요청이며 ZT06 연속 위치 태그가 아니다. 이벤트/쓰기권한/현재값은 CSV로 입증되지 않는다.

decoded-original XML695개의 ZT06 경계 문자열검색0건, HMI ZT06 검색0건. HMI Pot_MV06/RESET_ENC_MV06/Coeff_MV06/Zero_MV06 이름검색도0건. 이는 해당 텍스트 미확보이며 간접주소/바이너리/TIA 기술 객체 전체 부재 증명이 아니다.

## 3. 제어 구조 — 위치 후보 경로만

### 3.1 HSC 0510, LAD1760, NID49

NOT Contact21 operand W51/ORef25 RID344(0678 Simulation(1), M180.0) → W52 → EM_OK Contact22 operand W53/ORef26 RID173 → W54 → LRef23.en. LRef23은0679 RID330 High_Speed_Counter, NID49 UID23 Call이고 Instance24는0673 RID350 DB19다. 소스의 이 조건을 정적으로 읽었으며 시뮬레이터를 만들거나 실행하지 않았다.

- SwGate: W55/ORef27 RID261 → LRef23.SwGate, SW_GATE4 Read.
- CountValue: LRef23.CountValue → W75/ORef47 RID263, ACT_CNTV4 Write.
- RefId 없는21핀: CaptureEnable W56/O28, SyncEnable57/29, ErrorAck58/30, EventAck59/31, SetCountValue60/32, StatusHW61/33, StatusGate62/34, StatusUp63/35, StatusDown64/36, CompResult0 65/37, CompResult1 66/38, SyncStatus67/39, CaptureStatus68/40, CapturedValue69/41, ZeroStatus70/42, PosOverflow71/43, NegOverflow72/44, Error73/45, ErrorID74/46, MeasuredValue76/48, CompareMeasuredValue77/49.

빈 참조를 FALSE/0/사용 안 함으로 채우지 않는다. 0679는 CountValue DInt, ErrorID Word, MeasuredValue Real, SetCountValue InOut Bool로 선언한다. 이름만으로 인스턴스 내부 멤버와 자동 연결하지 않는다.

### 3.2 게이트·누적·선형화 0516, LAD1766, NID35

1. EM_OK Contact1529 W1503/ORef1480 → W1530가 Contact1531,1533 및 CRef1475.en으로 분기한다.
2. NOT raw MV06_Close Contact1531 W1504/ORef1481 RID260 → W1532 → 일반 Coil1441 SW_GATE4(W1505/O1482)와 Add1446.en.
3. Add1446 SrcType DInt: in1 W1506/O1483=Encoder_CH04 + in2 W1507/O1484=ACT_CNTV4 → out W1508/O1485=CNT_Act_4 Local. ENO W1509 → Div1450.en.
4. Div1450 SrcType DInt: in1 W1510/O1486=CNT_Act_4, in2 W1511/O1487=100(0675 RID211 DInt) → out W1512/O1488=CNTV4_100 Local. ENO W1513 → Move1454.en. Move1454 in W1514/O1489 → out1 W1515/O1490=Encoder_CH04_10 Int.
5. EM_OK → NOT SW_GATE4 Contact1533 W1517/O1491 → W1534: Move1463 in W1518/O1492=Int0(0675 RID44), out W1519/O1493=CH04_10; Move1468 in W1520/O1494=INT#0(0675 RID327 Int), out W1521/O1495=CH04 DInt. 상수와 목적지의 형식 차이를 보존한다.
6. CRef1475 RID351/CodeBlock1502 RID5는0680 BlockInterfaceInfo 및0672 FCBlock Signal linearization FC63, NID35 UID1502 Call에 결속된다. IN0 W1523/O1497=ON, Analog_input W1524/O1498=CH04_10, Coeff W1525/O1499=Coeff_MV06, Zero W1526/O1500=Zero_MV06, OutValue W1527/O1501=Pot_MV06, Out_of_range W24/O23=Pot_MV06_OFR.

따라서 카운터 호출조건, 소프트웨어 gate, 산술 ENO, FC63 IN0는 별개다. 현재 scan순서·값 갱신주기·정확한 물리 개도는 미확정이다. 다른 MV의 가공 Close를 이 raw I7.0 조건으로 옮기지 않는다.

### 3.3 저장·복수 쓰기·교정 한계

0511 LAD1761 NID30: NOT EM_OK Contact963 operand W951/O940 → W964 → Move937.en. in W960/O949 RID203는 Local CNT_Act_4, out W961/O950 RID204는 Encoder_CH04 Write다. 0516의0 쓰기와 별도 Writer이며 지역값 수명·실제 호출순서 없이 정전 복원/완전 위치 보존을 단정하지 않는다.

별도 RESET_ENC_MV06 HMI 태그 및 전용 교정 네트워크는 검색에서 확보하지 못했다. ZT04의0353 교정요청을 복제하지 않는다. 부모 초안에 기록된 과거 별도 Pot_MV06 쓰기 참조는 공유 경계로 유지하고 중지 블록 분석으로 확대하지 않았다. 본5개 FlgNet만으로 단일 Writer/온라인 최종값을 보증하지 않는다.

## 4. 전기 전달 경로 — 직접 도면 양 끝점

| 센서측 | 단자·선번 | FG148/PDF149 모듈 끝점 | 근거 |
|---|---|---|---|
|ZT06 B +24Vdc|X1/58 →33.1|TM1 단자9 24VDC|FG33/PDF34 및FG148/PDF149|
|ZT06 C −0Vdc|X1/59 →33.2|TM1 단자10 M|동일|
|ZT06 D|X1/60 →33.3|MOD18 TM1 단자1 CH0.A|동일|
|ZT06 E|X1/61 →33.4|MOD18 TM1 단자2 CH0.B|동일|
|차폐|X1/62 →33SCH1|FG148 차폐/접지 표시|실제 접지 연속성 미확인|

FG148 CH0.N 단자3에는 현장선 표시가 없다. 단자4/5/6 E22.0/.1/.2와7/8 A10.0/.1은 SPARE. 이를 ZT06 전용 DI/IW/PIW 또는 카운트 주소로 배정하지 않는다. 도면 CPU515/MOD18/TM1/TECNOLOGY MODULE TM TIMER는 설계 표기이며 현재 장치 모델/슬롯 증거가 아니다.

FG33 오른쪽 LS40/41 NC11/12, X1/63~66, E6.7/E7.0은 종단센서 별도 경로다. 상단+24V10.7 버스를 ZT06 B에 직접 결선했다고 하지 않는다. B/C의 도면 공급 경로는 하단33.1/33.2이다. OEM NC기호는 현장 정상 극성 확인을 대신하지 않는다.

시공 PDF58:

| 행 | 케이블 ID/방향 | 사양·표기 | 판정 경계 |
|---|---|---|---|
|8_6|=FLB+MV06-FLO4TB2A, CR→MV-06 FLO4TB2 ZT06|TM,CVV-S,4S,1.0,spare0;100→120 RBD1→E1300;Adjustment12,LEN63|중계함 trunk 후보|
|8_21|=FLB+MV06-ZT06A, MV-06 FLO4TB2→MV-06 ZT-06|TM,CVV-S,4S,1.0,spare0;E1330;Adjustment3,LEN4|센서 branch|
|8_17|동일=FLB+MV06-FLO4TB2A, UC-01 FLO4TB1→MV-06 FLO4TB2 LS34/35|DC,CVV,7G,1.0,spare2;Adjustment8,LEN9|8_6과 동일 케이블로 합치지 않음|

LEN은 설계 표기이며 실측이 아니다. X1/58~62와 FLO4TB2 내부 단자 세부 결속은 미확보이므로 OEM 끝점과 시공 중계함을 하나의 검증된 준공 배선으로 합치지 않는다. 가려진8_5/7/8은 복원해 활성 배선으로 사용하지 않았다.

시공 PDF56 행6_6은 MV05 FLO1TB2 ZT-06, 케이블=FLA+MV05-FLO1TB2B이고,6_20은 MV05 ZT-05다. 부모 초안의 명칭 상충을 실제 페이지에서 재확인했다. ZT05/06 이동·동일실물·오타 확정은 보류한다. P&ID LS34/35 대 OEM LS40/41도 같은 원칙이다.

## 5. 알람·복구 — 범위 결과와 부모 고장 구분

공통 FC63 0291(LAD1658 NID1)/0014(LAD1659 NID2), 선언0611/0612의 같은 고정 원본을 재사용하고 핵심 핀을 직접 대조했다.

- IN0 Contact255 W220/O196 RID1 Local → W256. Analog_input Int >−1382 Gt258(W30/O32,31/O33) → W25 → ≤32767 Le161(W27/O29,28/O34) → W26 Convert164.
- Int→DInt Convert164/167, Add170(입력+Zero), Convert174(Coeff), Mul177, Div181의28000, Move185 OutValue Int. ENO W227/230/234/237/241/245가 존재한다. 이것을 실수 연산/센서 실제 허용범위/개도 단위로 바꾸지 않는다.
- Gt190 >32767 또는 Le259 ≤−1382 → OR47 W49 → Move193, W252/O218=−9999(0612 RID21), W253/O219=OutValue(0611 Local RID19). ENO W21 → 일반 Coil23 W22/O24=Out_of_range(0611 Local RID26). S/R 래치가 아니다.
- 0014: NOT IN0 Contact171 W168/O165 → W172 Move162,0 W169/O166 → OutValue W170/O167. 여기에는 별도 OFR Reset coil이 없다.

호출측0516 OFR W24/O23은 DB3.X25.2다. 검토한 위치 경로5개 FlgNet에서 ZT06 전용 지연타이머/S/R 고장 래치를 확보하지 못했다. 모든 프로그램에 없는 것으로 일반화하지 않는다. HSC Error/ErrorID/ACK가 미결속이므로 진단알람 번호·RESET_ALLARM 연결·하드웨어 복구 성공을 발명하지 않는다.

부모 MV06 초안의 MV_06_FAULT DB3.X11.6,0159의150ms 및0352 W19>2200/W20<−2200은 방향응답/명령 누적의 부모 고장이다. ZT06 펄스 소실 검출시간·위치 임계값으로 복제하지 않는다. 부모 Reset·공유 인버터 고장 전체는 부모 초안을 참조한다. OFR 해제·요청 해제·모터고장 Reset·실제 위치 복구는 서로 다른 관찰이다.

## 6. 증상별 관찰 — 조작/운전시험 지시 아님

| 증상 | 확보할 읽기 전용 기록/대조 | 미확정 경계 |
|---|---|---|
|위치값 정지|프로젝트 식별,0510 enable조건,SW_GATE4/ACT_CNTV4,0516 raw I7.0와 각 값의 동일시각 기록|즉시 센서 고장으로 결론 내리지 않음|
|값 튐/0으로 변화|0516 두0 Writer,0511 저장 Writer,EM_OK 및 호출순서 기록|0을 물리 완전닫힘으로 단정하지 않음|
|OFR 또는−9999|Int 환산입력/계수/영점,0291 범위식과 호출 조건|센서 전기 허용범위 또는 보호값 제시 금지|
|끝단 표시와 연속값 불일치|LS34/35↔LS40/41 승인 대응,raw I7.0,DB11 표시와ZT06 값을 분리|HMI 끝단표시를 엔코더 측정으로 쓰지 않음|
|장치/케이블 식별 불명|ZT06 명판·단자·FLO4TB2 준공표·MV05 상충 승인 정정본|이름만으로 배선변경/교체 판단 금지|
|복구 여부 문의|권한 있는 현장 기록의 전후값·시각·실제 위치·관찰자·프로젝트 일치|ACK/알람소멸만으로 현장복구 완료 불가|

관찰자·시각/시간대·장치/프로젝트 식별·값/단위·비교원본을 갖춘 자료가 필요하다. 현장 조작, 출력 강제, 접점 우회, 계수 변경, 보호값 변경, 시뮬레이터 또는 행동시험을 수행하거나 제안하지 않는다.

## 7. 완료·누락·인계

| 영역 | 상태 | 누락/한계 |
|---|---|---|
|설비·자료 기준|적용/문서 초안|현재 실물 동일성 미확정|
|IO·HMI|적용|ZT06 전용 HMI/기술 객체 연결 미확보|
|제어|적용/후보 위치 경로|모듈 매핑·온라인 호출순서·전체Writer 미확정|
|전기 끝점|적용|준공 중계함 세부결선/현장 확인 없음|
|알람·복구|적용|HSC 진단21핀 미결속·현장복구 없음|
|증상 관찰|적용|실측기록 없이 원인 확정 안 함|
|완료 기준|문서 인계 준비|통합/UI/배포/TIA/CPU/현장은 미수행|

필요 자료: 현행 TIA 기술 객체와 모듈/채널 매핑, 현장 ZT06 명판 및 기계결합, PPR/방향/출력형식 제조사 원문, 승인 준공 단자표, LS/케이블 명칭 상충 승인 정정, 현재 프로젝트와 CPU 일치 증거, HMI 이벤트와 진단 핀 선언, 권한 있는 현장 전후 관찰. 새 자료 없이 부모 전체/보류 항목을 반복조사하지 않는다.

도면·래더 비교는 본 문서 범위 정적 조사만 수행했다. 백업/선택복원·기록 전후비교·보고서 UI 기능·게시 검증은 미수행이며 해당 구현을 완료했다고 하지 않는다. 실제 문서 근거 보존 해시와 논리 의미검토 범위는 구별한다.

## 부록 A. 선정 원본 전체 SHA256 + 고정 Git blob

선정 31파일은 아래 전부 표시했다. 해시 일치는 의미검토 완료 수가 아니다. NNNN XML 표의 경로는 본문의 원본경로 약어와 동일하다.

| 원본 경로 | SHA256 | Git blob | 고정 내용 일치 |
|---|---|---|---|
| `AGENTS.md` | `0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2` | `073164bc6efd5791032d62c71b03b4dab48cb6f8` | True |
| `.agents/skills/gme-equipment-rollout/SKILL.md` | `fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b` | `9aa820ea6ca15b4e136c9772423b78ed4df6a3d4` | True |
| `docs/equipment-standard/WORK-STANDARD.md` | `05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99` | `f76a570cc73098632e08759b17934000f7e3a253` | True |
| `docs/equipment-standard/WORK-ITEM-TEMPLATE.md` | `4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586` | `e546f39535d2b589e80f97db869ac37ce4d05cfd` | True |
| `docs/equipment-standard/INVENTORY.json` | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` | `587c3748ad9224718f95ba06463fee913dae231d` | True |
| `VERSION.json` | `5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7` | `fffb51663b7705aec91cb119ca80ee943a4ce758` | True |
| `WORKSPACE-HANDOFF.md` | `215096d997782e78e901dfae36c782937e49611fbeb677a0d3fa50cbecf8d074` | `dd0b8989d2376c4415bba9bd826fe6754c6b1a12` | True |
| `PUBLICATION_STATUS.md` | `efe4857aec598d90470322cf3962eb3fe1f64947630e1fdf71d1c90134de8740` | `d76401cf291fc0be681acc51fa898ad3ce46ff78` | True |
| `EXPANSION-WORK.md` | `ec624de9fd2fcfac861a67fd5e828b25ef46db50bfd7a37ff16e2cb54cd0f7e2` | `4c42d88ecc2d48269eb23e13a20ebf3721a092a1` | True |
| `all-in-one/ACTIVE-WORK.md` | `eff3bbc08ecff41da3beff77f3fec48e7d148708192bcaaab00f34b6a721afc2` | `6eb947c629b5ddf9c759ef87649451303938864b` | True |
| `all-in-one/sources/Electrical_Rev2.pdf` | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` | `f610fd7c7ce14ae951b00cff57b969259bfb389d` | True |
| `all-in-one/sources/Electrical_Can_Decoating_20241118.pdf` | `3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd` | `0ee6b6f8361c5790864dbba4bbd9d55e8e7c08f8` | True |
| `all-in-one/sources/PID_1684n002I.pdf` | `2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b` | `8c83a59fefd5b8b651ec3537ea4236a073f5e109` | True |
| `all-in-one/sources/hmi_plc_tags.csv` | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` | `cf4c0650e7c7baac350dcb89909b808435704880` | True |
| `all-in-one/sources/decoded-original/network-map.json` | `c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60` | `424430b6b953e43138e5d0a18ca40c949e21cfa1` | True |
| `all-in-one/sources/decoded-original/0510-FlgNet.xml` | `0e755f251ab92f2b1904be6812b4995ba04285f99de068b8bc794d31c1cee0dd` | `ca06d39dc0bf873f7ece4ff984b9d615a95617e8` | True |
| `all-in-one/sources/decoded-original/0511-FlgNet.xml` | `a4bf314bf817f0f666a0c9fdd26df134cedeed8666819c7a3e8e6438850eace6` | `2730bc98903fc1a89effa1911c5ac82ddd7b4957` | True |
| `all-in-one/sources/decoded-original/0516-FlgNet.xml` | `382738875d4fe8ebcf38f878eafd6486047e3cdd6de7a98bebcafc2afd124c8f` | `06030b0a2ec9e27ee53298e46584373ec92ab97b` | True |
| `all-in-one/sources/decoded-original/0291-FlgNet.xml` | `fe0b92f074eba25148ce34084649af3d968962558d652727f1eea19f3e3c2550` | `1418fb2ed172c6df694a5eb8bf2dffd0b177653b` | True |
| `all-in-one/sources/decoded-original/0014-FlgNet.xml` | `2e814adbaac6bab99bc668bfdab74f0fc90576324d0b88728951683869cfac30` | `4d164b074fcc13a8f97da9e24382cc169ef29555` | True |
| `all-in-one/sources/decoded-original/0672-IdentXmlPart.xml` | `6bfc2ba142d6270c39eb1f13b2886204865af6d46eadc5f410c26981b8da9222` | `2f2790dab4bb2357733112220e0acc41edb6feb6` | True |
| `all-in-one/sources/decoded-original/0673-IdentXmlPart.xml` | `450ef74e2d2fb65dfbb5f6bad9e28ccacf6bf0caf64327a0e20aff84d6e40f58` | `1957bff7dd1beffcb6e2a40d6a541c1751753548` | True |
| `all-in-one/sources/decoded-original/0674-IdentXmlPart.xml` | `4770702f519bacda69202bb2f7733d983074bda90964360c238f990d9d08fd84` | `f210593944547b63eab10c667348711413600aab` | True |
| `all-in-one/sources/decoded-original/0675-IdentXmlPart.xml` | `b1902886927d8403fab736d9c8ffe73f2fbc8ce4b7ca7c345144964668b051c3` | `d82a33b173c8dc0737fd890eb2a63a88a07d0831` | True |
| `all-in-one/sources/decoded-original/0676-IdentXmlPart.xml` | `c58427c5b0ac6c11cdb52e4c6d0461c7b191fae81ccace191048e9f175fcec59` | `1ed67265f69796a4e659f9438e551068037f33a4` | True |
| `all-in-one/sources/decoded-original/0677-IdentXmlPart.xml` | `69922fcc5c67d00cdf1c5f712efa3db7638d20c88318d35fe6196467796ab1e3` | `b9437406a7e24f073ef88b8369cacc9ad4ecc5ac` | True |
| `all-in-one/sources/decoded-original/0678-IdentXmlPart.xml` | `51e637e0b9713c028810f2a717b5c3804a3a26c2f1be7e332a4d6bf277bfc382` | `7fafb2297bcdf739bf1d1dd68cebc0d74f2a40cc` | True |
| `all-in-one/sources/decoded-original/0679-IdentXmlPart.xml` | `d0fcb93e188c8ae2ae0c0423f0b78b129bf3c168e33a6855262d34b8682b9b56` | `e8d8a014609871082bf5cfca0f9ab9b78136e920` | True |
| `all-in-one/sources/decoded-original/0680-IdentXmlPart.xml` | `fd551ad5d47bbd66c6bcdcc1949aaddf68cc086a3ddf6fb337adc767954c2b95` | `c9049ced1eaed72c5e251a88601d46ddec8c3e50` | True |
| `all-in-one/sources/decoded-original/0611-IdentXmlPart.xml` | `0d583915a261703954da22c176ba9f81338ad13ea2810e7cd5f7de8aa1bfa089` | `bad6b16fb32a32d47d882f48754994887457872b` | True |
| `all-in-one/sources/decoded-original/0612-IdentXmlPart.xml` | `95b545d4964d371ebfc107894ea90b8b1d0d7ab5d3a70e643f8ce539063c0f38` | `7cc782d33d07ef225c2104f3e7c9fbd31f7c7467` | True |

## 부록 B. 검사 결과와 실제 시각

- 완료 검사: 2026-10-11T13:10:20.830725+00:00 UTC. 선정 31파일, 전체 sources 712파일 및 중지5자산의 고정 Git 내용 일치. 원본 Git status clean.
- 독립 핵심검토 FlgNet5개(0510,0511의MV06가지,0516,0291,0014), 관련 선언/상수, 실제 PDF5쪽. 695 XML 이름검색은 전 논리검토가 아니다.
- HSC 미결속 ORef21개 확인. source-hashes.json, source-preservation-hashes.json, stopped-assets-preservation.json, static-review.json, search.json, stages.json은 extracts/ZT06에 기록했다.
- 단계 실제시각: 13:04:49 배정/범위읽기 시작,13:05:36 고유XML 확인,13:06:06 도면5쪽 시각검토 진행,13:09:39 초안작성,위 완료검사시각에 보존 확인. 모든 시각2026-10-11 UTC.
- TIA/현재CPU/실물/정상극성/보호설정/현장복구 미확정. 통합·게시·생성기·시뮬레이터·행동시험 미수행.
