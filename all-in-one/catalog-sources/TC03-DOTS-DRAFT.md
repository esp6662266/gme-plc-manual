# TC03 온도 계측 — 고유 원본 조사 7영역 초안

## 핵심 확인·인계

- TC03 한 개의 문서 조사다. `%IW276:P` → 선형화 → `Data.Temp_TC03` DB1.DBW112와 별도 HMI 원시 미러 DB13.DBW40을 구분했다. 원시 입력의 형식은 Int, 미러는 Word다.
- LOW/HIGH/MAX_MAX 세 온도경보와 `TC03_OFR`는 서로 다르다. LOW는 BWF01/02 처리 Run OR 조건, 세 경보의 지연은 각각 별도 타이머의 `S5T#3S`다. LOW/HIGH는 ±5 회복 비교와 ENO를 거치며 MAX_MAX는 별도 RESET_ALLARM 가지다.
- MAX_MAX는 `Temp > (TC03_MAX_ALL+50) OR Temp>750 OR Temp<-60`이다. “온도가 매우 높음”이라는 이름만으로 저범위 고장 가지를 누락하면 안 된다. 이 숫자는 원본 코드 상수이며 현행 안전 설정이나 조작 지시가 아니다.
- LOW는 RD01 투입금지 로컬 비트, MAX/MAX_MAX는 BR01 고화염·자동버너·정지 가지에서 소비한다. MV01 PID는 TC03 관련 로컬 Real을 읽는다. 해당 설비의 소유를 TC03로 바꾸거나 함께 완료로 세지 않는다.
- OEM FG77/PDF78은 TC03 송신출력 4–20mA·0/750°C, X1:192/193/194, FG106/PDF107은 PEW276의 AI 모듈 단자10/I2+와 공통12/18을 보여준다. 현행 설치·교정·CPU 동일성은 미확인이다.

### 상충·누락·공유 근거

| 구분 | 근거와 처리 |
|---|---|
| 고유 상충 | 같은 시공 케이블 8_18 `=FLB+UC01-TC03A`: 시공 PDF32 행10 LOC=FN-01, PDF58 행8_18 TO LOC=UC-01. 임의 정정·동일 실물 단정 없음 |
| 계측 경계 | OEM은 4–20mA 송신출력, 시공은 TC/KX 2S 케이블. 프로브부터 송신기까지 위치·열전대 타입·냉접점 보상·보상선/연장선 실제 구간 미확정. KX 표기만으로 현재 센서 형식을 확정하지 않음 |
| 추가 상충 | 보충 STL 색인 `_7ex/9` 실행텍스트는 `L -15`, 주석은 “meno 30°C”. 둘을 합치지 않는다. 이 가지는 MV04 명칭/VT02 관련 소비 경계이고 제외 MV04를 재개하지 않음 |
| 새 보충 근거 | 기존 MV01 초안은 SP/PV 상류를 FlgNet에서 미확보로 남겼다. 이번 live_index `_7ex/10`에 TC03_SETPOINT+0 및 Temp_TC03의 ITD/DTR 텍스트가 있다. XML 선언의 Local Real Write와 대조했지만 원래 STL 전체 객체·CPU 실행 동일성은 별도 미확정 |
| 공유 재사용 | BF01/RO01의 0291/0014 공통 선형화, MV01의 0477/0342 PID·방향 소유 설명을 탐색 인덱스로 재사용. 본 작업에서 TC03 호출/고유 알람/해당 핀을 독립 재확인하고 고정 blob 해시를 대조 |
| 미확보 | 현행 계수/제로·온도 설정·안전 승인값, ON/OFF 현재값, HMI 실제 이벤트·경보화면·통신, 승인 준공도·명판·교정·복구 결과 |

## 1. 설비·자료 기준

catalog_id TC03, 온도 계측, sensor/계측, parent 없음/depth0/priority_key 없음, 별칭 tc_03. INVENTORY catalog[14], equipment[78], phase2/planned다. 대장 역할은 배출가스 온도·MV01 관련 제어값이다. TC01/02나 UC01, RD01, MV01, BR01과 동일 실물/완료 항목으로 병합하지 않는다. `TASK3-BATCH07-SCOPE.json`, `GME-CATALOG-OVERLAP-REVIEW.json` 고유 범위를 따르며 로컬 2차133 통합 제외를 유지한다.

- 고정 원본: `gme-research/source-mv06`, commit `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, VERSION 1.12.0. 현재 main·현재 CPU·현행 도면이라는 뜻이 아니다.
- AGENTS, 스킬/source-map, WORK-STANDARD/WORK-ITEM-TEMPLATE/INVENTORY/START-GPT61, VERSION/EXPANSION-WORK/WORKSPACE-HANDOFF/PUBLICATION_STATUS/ACTIVE-WORK 최신 항목을 읽었다. 최신 배치 지시가 이전 최대2 병렬과 통합 지시보다 우선한다.
- 실행 모델·추론 수준 런타임 증명은 미확인. 새 Work/Codex·재위임·사용자 Mac·로컬 TIA 접근 없음.
- 쓰기는 `drafts/TC03-DOTS-DRAFT.md`, `extracts/TC03/`뿐이다. 원본/공유코드/대장/버전/게시/운영 기록/SEJIN 변경0, 시뮬레이터 작성·수정·생성·실행·행동시험0, PLC/현장/보호값 변경0. 원본 build/test/generator 실행0.
- 이하 원본 경로 기본은 `source-mv06/all-in-one/`. `0491` 등은 `sources/decoded-original/0491-FlgNet.xml`, 선언은 별도 `NNNN-IdentXmlPart.xml`이다. LAD 문서번호와 NID를 구분한다. 추출 refs의 RID 충돌 후보는 해당 블록 선언 파일/UID/NID로 재선별했다.

| 7영역 | 적용 상태 | 확보/미확정 |
|---|---|---|
| 설비·자료 기준 | 적용 | 고유 ID·역할·판본/현행 실물 미확정 |
| I/O·HMI | 적용/일부 미확보 | 주소·형식·쓰기·미러/실제 화면 이벤트 미확정 |
| 제어 | 적용 | 환산·호출·소비·복수 쓰기/현재 순서 미확정 |
| 전기 끝점 | 적용/일부 미확보 | OEM2쪽·시공2쪽 실제 렌더/현행 센서·변환기 상세 미확정 |
| 알람·복구 | 적용/복구 미확보 | OFR+3온도경보·소비/현장 복구 미수행 |
| 증상 관찰 | 적용 | 읽기 전용 비교지침/조치·운전시험 없음 |
| 완료·누락 | 적용 | 문서·검사·현장 분리/제품 통합·독립 검토 별도 |

## 2. I/O·HMI

### 2.1 고유 선언·주소

SSD.AO와 AOS.BO는 bit offset이다. BAD BIRID는 DepDBBlock.TOD로 대조: 0674 RID8/11/354→Coeff DB4/Data DB1/Allarm DB3, 0628 RID4→Inputs DB13, 0682 RID3/10/15/135→DB1/3/2/13. 현재 DB 구성까지 증명하지 않는다.

| 신호 | 형식·백업 주소 | 선언·핀 |
|---|---|---|
| TC03 환산 원시 | Int IW276:P | 0678 RID76 AO2208 Input SAM=Peripherie, NID11 UID364;0491 W371→356.Analog_input |
| TC03 HMI 원시 읽기 | Int IW276 | 0627 RID67 AO2208 SAM=None, NID2 UID76 |
| Inputs.TC_03 | Word DB13.DBW40 | 0629 RID69 AO320 NID2 UID77 Write;0398 Move 원시전달. 환산값 아님 |
| Coeff.ZERO_TC03 / COEFF_TC03 | Int DB4.DBW20/22 | 0676 RID78/77 AO160/176;0491 UID366/365 W373/W372→Zero/Coeff |
| Data.Temp_TC03 | Int DB1.DBW112 | 0676 RID79 AO896 NID11 UID367 Write, W374 OutValue;0684 RID27 소비 |
| TC03_OFR | Bool DB3.DBX21.4 | 0676 RID377 AO172 NID11 UID23 Write,0491 W24 Out_of_range |
| TC03_SETPOINT | Int DB1.DBW50 | 0668 RID45 AO400 NID16 UID37 Write;0577 RID74 NID3 UID662/NID4 UID1011 Write;0642 RID101 NID1 UID3571 Write |
| TC03_MIN_ALL / MAX_ALL | Int DB1.DBW72/74 | 0684 RID28/33 AO576/592;MIN은0528 UID32 Write도 있음 |
| LOW / MAX / MAX_MAX_TC03_TEMP | Bool DB3.DBX8.3/8.4/8.5 | 0684 RID31/35/42 AO67/68/69;0528 UID434·441/448·455/469·472 S/R |
| Tag_101/102/103 | Timer T87/T88/T89 | 0686 RID30/34/41 SAD Timer AO87/88/89;HMI 태그가 아님 |
| app00 / max_max_tc3 | Local Int BO0/64 | 0685 RID14/39;NID2 UID438/452 및459 Write. DB 설정주소를 임의 부여하지 않음 |
| Real_SP_TC03xMV01 / Real_TC03xMV01 | Local Real BO64/608 | 0669 RID62/63 NID7 UID255/271 Write, NID8 UID401/402 Read |
| Disable_Load_RD01 | Local Bool | 0605 RID16 NID2 UID77 Write;0238 Coil66. RD01 소유 내부 금지이지 TC03 출력 접점 아님 |

### 2.2 HMI 연결

`sources/hmi_plc_tags.csv`의 Access Name PLC 설정 행 8개를 확인했다: I_TC_03 DB13,INT40(00063), data_DB1_DBW112 DB1,INT112(00248), SETPOINT DB1,INT50(002A9), MIN DB1,INT72(002A8), MAX DB1,INT74(0028C), ZERO DB4,INT20(00210), COEFF DB4,INT22(001EE), Editor_TC03 DB26,INT20(00413). CSV는 dde.cfg 설정 추출이며 온라인 현재값·실제 화면 버튼·소수점·사용자 권한·쓰기 이벤트의 증거가 아니다. Editor_TC03는 레시피 편집 버퍼이고 실행 SETPOINT와 동일 저장부가 아니다.

레시피 보충 텍스트 `live_index.json` `_7ev/364`는 Recipes[0]=Recipes[HMI_index] AND vis_loadrecipe AND load_recipe 때 Recipes[0].TC03→Data.TC03_SETPOINT를 기록한다. 0642 RID101 Write 선언이 이를 보충한다. 실제 화면의 Load 버튼 이벤트·현재 선택 레시피·외부 Writer는 미확인이다. Bool 경보 비트와 Word 단위 HMI 전달/쓰기의 간접 영향도 별도 대조가 필요하다.

## 3. 제어 구조·사용처

### 3.1 TC03 환산의 직접 핀

0491 LAD1741 NID11: ORef362(0678 RID1 ON)→Contact375.operand W369;375.out W376→CRef356.en. ORef363 ON W370→356.IN0. TC03/계수/제로는 W371/372/373, OutValue W374→ORef367, Out_of_range W24→ORef23이다. CRef356 RID351의 BlockInterfaceInfo는 0680, CodeBlock368 RID5는 0672의 Signal linearization이다. EN과 IN0 모두 ON을 쓰지만 이름만으로 현재 TRUE를 보장하지 않는다.

공통 함수 0291 및 0014는 같은 고정 원본으로 재사용하되 핵심 핀을 다시 확인했다. 0291 IN0 접점255→W256에서 범위를 분기한다. 유효범위 `raw>-1382 AND raw<=32767`(Gt258/Le161). Convert164/167/174와 Add170/Mul177/Div181는 ENO 연쇄 W227/230/234/237/241/245, `(DInt(raw)+DInt(zero))*DInt(coeff)/28000`를 계산하고 Move185로 Int OutValue에 전달한다. Real PID 입력 변환과 같은 계산이 아니다. 정수 오버플로/절삭·ENO/호출 비활성 때 최종값·리텐션은 현재 CPU에서 미검증이다.

범위 이탈 `raw>32767 OR raw<=-1382`는 OR47→Move193(-9999). OutValue W253, **Move193.eno W21→Coil23→Out_of_range**다. OFR를 단순 비교기 출력으로 치환하지 않는다. 0014는 NOT IN0 Contact171 W172→Move162(0)→OutValue W170이다. -9999/0은 원본 코드 대체값이며 현장 안전 대체값이 아니다. raw Int 상한 초과 가지가 존재한다는 정적 사실과 그 가지의 실제 도달성을 구분한다.

### 3.2 MV01·VT02 관련 소비

0477 LAD11 NID8 CONT_S LRef366(0671 RID113), Instance412 PIDMV01(0665 RID71, DB21). ON Contact463 W464→en, NOT Flag.MV01_Auto Contact465 W466→COM_RST. W442/443이 SP_INT/PV_IN에 Local Real62/63을 넣고 W457/458은 UP/DOWN MV01 PID로 전달한다. CYCLE T#100MS, GAIN3.0, TI T#3M, DEADB_W1.0, PULSE_TM T#500MS, BREAK_TM T#1S, MTR_TM T#31S, DISV1.0은 원본 호출 인자다. 현행 튜닝값이나 조정 권고가 아니다. LMNR_HS/LS는 실제 처리 Open/Close OR OFF가지의 Pot_MV01>=100/<=10이고, 아홉 미결속 파라미터는 이번에도 추정하지 않는다.

0342 LAD1702 NID1은 이 PID 요청·수동 요청·MV01_FAULT 반전·반대 방향 반전·리미트 반전·ResetEncoderProcedure를 소비하여 Start Open/Close MV-01을 쓴다. TC03 자체가 모터 전원이나 방향 출력을 직접 소유한다는 뜻이 아니다. 상세 MV01 전기/교정은 기존 MV01 초안의 범위이고 이번에 함께 완료로 집계하지 않는다.

보충 `live_index` `_7ex/10` STL텍스트는 TC03_SETPOINT에 0을 +I하고 ITD/DTR해 Real_SP_TC03xMV01에 전달, Temp_TC03를 ITD/DTR해 Real_TC03xMV01에 전달한다. Temp_T6 로드는 주석이다. 0668 RID45/48 Read 및0669 RID62/63 NID7 Write가 결속되지만 FlgNet 핀 문서가 없는 텍스트이므로 별도 증거등급으로 둔다. `_7ex/9`의 Real_*MV04 명칭은 `_7ex/13` CONT_C PID_VT02의 SP/PV로도 소비된다. MV04 명칭만으로 실제 MV04 물리제어 소유를 단정하지 않는다.

### 3.3 설정의 여러 쓰기

0480 LAD8 NID16은 rail→Lt22(SETPOINT<200)→Move32(200)→UID37로 쓴다. ON 접점을 임의 추가하지 않는다. 별도0528의 MIN_ALL<200→Move27(200)은 SETPOINT와 다른 저장부다. 0164/0165 LAD1843/1844 NID3/4는 예열/생산의 ON·긴급모듈고장 반전·Auto_ON1·Tipo_preset·Tempo_presetting(45/62) 뒤 **OFF 가지**의 Move500→SETPOINT(UID662/1011)가 존재한다. `OFF` 이름 때문에 제거하거나 무조건 실행이라고 보지 않는다. 레시피/HMI/전체 DB전달 등 다른 쓰기도 가능하므로 백업 초기값·상수500·현재 운전 설정을 혼동하지 않는다.

### 3.4 RD01·버너·UC01의 관련 소유

0238 LAD1931 NID2: ON91 이후 LOW_TC03_TEMP95의 출력 W96→OR56.in1. 다른 7가지(Oxigen_Fault, Oxigen_Too_high, STANDBY_ON, MAX_MAX_TC09, HYDROGEN_BOX_FAULT, NOT R1 Gate ON, NOT RD01_Fbk)와 OR이고 W88→Coil66→W90 Local Disable_Load_RD01. 하나의 TC03 경보가 이 투입 금지 조건의 충분한 OR 가지이나 실제 RD01 정지·투입차단·복구는 RD01의 후속 소비까지 별도 확인해야 한다.

0175 LAD1858에서 MAX_MAX_TC03_TEMP ORef242는 버너정지 OR 조건에 들어가 Start_Burner RCoil232를 구동한다. 0178 LAD1862에서 MAX_TC03_TEMP는 고화염 해제/패널 설정0 및 고화염 재Set 금지에 사용되고50ms·8s는 이 버너 소유 타이머다. TC03 고유3초와 혼합하지 않는다.0186 LAD1870에서 MAX_TC03 반전은 AutoBurner Coil1172 직렬 허가, 정방향은 Panel_SetPoint=0 Move1181 OR 가지다.0181 LAD1865 Lock Burner에는 OFF 가지와 ON OR 가지가 있어 단순 “고온=무조건 lock”으로 축약하지 않는다. 버너 외부 화염/점화/안전 순서를 이 PLC 자료로 발명하지 않는다.

UC01은 시공 케이블 목적 위치의 관련 소유 표기다. 본 조사에서 `UC01` 이름의 TC03 전용 PLC 조건·출력을 입증하지 않았다. 케이블 LOC를 별도 온도제어기나 자동 복구 로직으로 만들지 않는다.

## 4. 전기 끝점·실제 PDF

| 자료·실제 페이지 | 직접 경로·판본 |
|---|---|
| Electrical_Rev2.pdf FG77 / PDF78 | +24Vdc10.7(76/9→78/0)→5×20 50mA F→X1:192→77.3→TC03 +5. TC03 -6→X1:193→+PEW276(106/5). 실드→X1:194→77SCH3(106/4). OUTPUT4–20mA,0/750°C. 하단 THERMOCOUPLE,27.05.2024,FG77/TOT262,별도 개정 기입 관찰 없음 |
| Electrical_Rev2.pdf FG106 / PDF107 | +PEW276→모듈단자10 I2+, 77SCH3은 실드 접지. 채널 공통12(U2-/I2-)는8/4 및18 MANA와 -0Vdc10.6 연결. CPU515/MOD3 표기. 이 시트에서 정확한 제조사 주문번호는 확보 안 됨. 하단 ANALOG INPUT MODULE,27.05.2024,FG106/TOT262,별도 개정 기입 관찰 없음 |
| Electrical_Can_Decoating_20241118.pdf PDF32 | CANDC-CONS-E015-032, FLOW B ROUTE CONDUIT PIPING(2),행10 Pipe16 TC03,LOC FN01,케이블8_18=FLB+UC01-TC03A,KX1.0/2심. 하단 Rev1 24.11.11 first draft design;CHECKED/APPROVED 공란 |
| 같은 시공 PDF58 | CANDC-CONS-C008-058 CABLE SCHEDULE(7),행8_18 CR→UC01/TC03,Type TC,KX2S1.0,spare0,route100→120RBD1→E1000,Adjustment8,LEN59. 수치를 현행 실측 길이로 표시하지 않음. 하단 Rev1 24.11.11 first draft design;CHECKED/APPROVED 공란 |

네 페이지 모두 텍스트만이 아니라 실제 원본 렌더 이미지를 눈으로 대조했다(`extracts/TC03/render/`). PDF 페이지와 FG를 일반식으로 만들지 않았다. 시공 PDF32/58의 위치 불일치, OEM 송신출력/시공 열전대선 구분을 그대로 남긴다. +5/-6 도면 단자 극성은 자료상 사실이나 현재 센서 정상극성·배선·설치가 맞다는 검증은 아니다. 릴레이 부하접점은 이 온도입력 경로의 핵심 구성으로 확인되지 않아 타 설비의5/9 또는1/5/9를 복제하지 않는다. 센서 타입, 송신기 모델·위치·전원·분리기, 열전대 보상, 단선/역극성 반응, 승인 보호설정, 교정이력은 별도 확보 대상이다.

## 5. 고유 경보·복구

모두0528 LAD1980 NID2, ON ORef426→Contact543→W544 분기다. 선언0684/0685/0686 및 상수0683을 원본 대조했다.

| 경보 | 발생·지연·Set | 해제·영향 경계 |
|---|---|---|
| LOW_TC03_TEMP | Inputs.BWF01 RUN545 또는 BWF02 RUN547→OR333 W476→Lt336(Temp<MIN). W479→SdCoil342,상수UID431 S5T#3S,Tag101 T87 UID432. 같은Lt 출력+Tag101 Contact549→SCoil347/UID434 | ON AND LOW Contact551→Add352(MIN+5),**ENO W491**→Gt356(Temp>app00)→W494 RCoil360/UID441 및STOP_HORN SCoil362/UID442. BWF가 꺼졌다는 사실만으로 Reset 가지를 대신하지 않음 |
| MAX_TC03_TEMP | Gt366(Temp>MAX) W500→SdCoil372(T88/S5T#3S),Contact553→SCoil377/UID448 | ON AND MAX Contact555→Sub382(MAX-5),**ENO W512**→Lt386(Temp<app00)→W515 RCoil390/UID455 및STOP_HORN SCoil392/UID456 |
| MAX_MAX_TC03_TEMP | ON→Add396(MAX+50) W521→Local max_max_tc3. Gt403(Temp>local),Gt406(Temp>750),Lt409(Temp<-60)→OR402 W531→SdCoil415(T89/S5T#3S),Contact557→SCoil420/UID469 | ON→RESET_ALLARM Contact559→기존MAX_MAX Contact561→RCoil425/UID472. 이 Reset 가지에 온도정상 비교는 없음. 원인 지속 시 재Set 가능성/실제 우선순서는 실행검증 전 미확정 |
| TC03_OFR | 0491 Signal linearization Out_of_range→DB3.DBX21.4 | 0291 Move193 ENO 코일과0014 경로를 분리. 세 온도경보와 같은 래치/RESET이라고 하지 않음 |

LOW/MIN 하한강제는 Gt/Lt의 등호 경계와 별개다. 각 온도 비교는 strict Lt/Gt이므로 같은 값에서는 비교가 참이 아니다. MAX_MAX 상수750은 OEM0/750°C 상한표기와 숫자가 같지만 이것만으로 현재 보호등급·안전설정 승인·센서 타입을 확정하지 않는다. Add/Sub는 Int이고 ENO·오버플로의 동작을 생략하지 않는다. STOP_HORN Set은 온도 정상, 전체 경보 해소, 안전 재시동 또는 현장 복구를 뜻하지 않는다. 실제 경보문자·ACK·음향·램프·전체 Word 복사·간접 Reset은 이번 고유경보 범위를 넘어 미확정으로 남긴다.

## 6. 증상별 읽기 전용 관찰

아래는 관찰 계획이며 센서 탈거·회로주입·보호값 변경·리셋·시동 지시가 아니다. 위험구역/전기 접근은 승인된 현장 절차·자격을 따른다.

| 증상 | 같은 시각에 모을 값·위치 | 비교·원인 배제·남길 증거 |
|---|---|---|
| HMI 온도와 PLC가 다름 | IW276:P, IW276, DB13W40, DB1W112, HMI 태그주소/표시,통신시각 | 원시 미러와 환산값 혼동,접근/갱신주기·스케일·계수 확인;값을 임의 덮어쓰지 않음 |
| -9999 또는 OFR | 호출EN/IN0,raw,zero/coeff,OFR 및MAX_MAX/T89 | 입력범위 가지와 MoveENO,호출비활성,송신기/루프/보상선 단절을 구분;실물 원인 단정 금지 |
| 온도 낮지만 LOW 없음 | BWF01/02 처리Run,Temp/MIN,T87,LOW | Run OR 전제와3초 지연,MIN하한 강제 확인;경보가 없다고 공정 안전 판정 금지 |
| 온도 내려와도 MAX_MAX 유지 | Temp/MAX/local MAX+50,T89,RESET_ALLARM,MAX_MAX | LOW/HIGH 자동 히스테리시스와 MAX_MAX 수동요청 가지를 구분;승인 없이 Reset 금지 |
| RD01 투입 금지 | LOW와0238 OR8가지,Local Disable_Load_RD01,후속 RD01 상태 | TC03 이외 OR 원인을 함께 확인;금지비트와 실물 정지/완료 피드백 구분 |
| MV01 동작/버너고화염 기대와 다름 | TC03 SP/PV,Auto,UP/DOWN 요청,리미트·고장·교정요청,MAX/MAX_MAX,버너응답 | TC03측 데이터,타 설비 허가/전기/기구를 분리. PID 임의 튜닝·강제 출력 금지 |

관찰 기록 틀: 관찰자, 실제 시각/시간대, 위치·태그·주소, 수치/단위·신선도, 수집장치, 프로젝트/CPU 식별, 비교 원본·개정, 사진·원인배제 결과, 승인조치와 별도 복구확인. 지금 실제 운영 기록은 만들거나 복제하지 않았다.

## 7. 완료·검증·누락

| 상태 | 이번 판정 |
|---|---|
| documentation | draft_complete_with_gaps: 고유7영역 문서 조사 |
| static_review | 고유 XML 핀/선언·공유 함수·원본 PDF 대조 완료,독립 검토는 부모에게 인계 |
| ui_records | not_run: 실제 화면·저장·재읽기·재열기 없음 |
| publication | not_published: 원본/제품 통합·게시 없음 |
| tia_compile/live_cpu/field_recovery | 모두 not_performed |

네 기능: 도면·래더 비교는 본 문서의 원본 위치까지 준비;앱 구현/링크 동작 미검증. 백업·선택복원,기록 전후비교,관찰 보고서/PDF는 기존 구현을 실행·변경하지 않았고 TC03 지원 완료로 세지 않는다. 기존 note/repair_observation/미지 필드/다른 설비·초안·저장키 보존. 본 PDF 렌더는 원본 도면 확인이며 새 관찰보고서 출력시험이 아니다.

직접 의미검토:0491/0528/0480/0238 전체 고유 회로,0398 TC03 Move,0477 SP/PV·호출·리미트,0342 TC03 관련 MV01 방향 경계,0164/0165 설정쓰기 가지,0175/0178/0181/0186 버너 소비 가지,0291/0014 공통 환산. 추출된 나머지 네트워크 전체의 의미완료를 주장하지 않는다. live_index/CSV는 보충·탐색 자료이고 해시 검증 파일 수를 의미검토 수로 대신하지 않는다.

추가로 필요한 것은 (1) 승인 준공도/TC03 실물·송신기·프로브·보상선 및시공LOC 상충 해소,(2) 허가된 현재 프로젝트/CPU 주소·호출·Writer 비교,(3) 현행 계수·제로·설정/안전승인·교정자료,(4) HMI 실제 화면 이벤트·표시·ACK,(5) 승인 현장 관찰·조치·복구 증거다. 새 자료가 없으면 같은 실물보류를 반복 조사하지 않는다. 다음 조치는 부모의 고유 핀/상충 독립 검토이며 TC03의 제품통합 또는 제외설비 재개를 이 초안으로 승인하지 않는다.

### 실제 작업 단계 시각 (UTC)

- 2026-10-11T10:52:58Z — instructions_and_scope_read
- 2026-10-11T10:53:43Z — first_xml_extraction_completed
- 2026-10-11T10:54:43Z — four_pdf_renders_visually_reviewed
- 2026-10-11T10:58:53Z — seven_area_draft_written
- 2026-10-11T11:00:00.273348+00:00 — static_assertions_and_fixed_blob_hashes_verified

### 원본·중지 자산 해시 전체 목록

선택 원본·맥락·보존 84파일 SHA-256와 고정 Git blob이 모두 일치했다. 중지5자산 freeze도 일치,원본 Git 변경0. 이 수는 전체 의미검토 수가 아니다. 검사JSON은 extracts/TC03/static-review.json,해시JSON은 source-hashes.json이다.

| 원본 경로 | SHA-256 | 고정 Git blob OID |
|---|---|---|
| `.agents/skills/gme-equipment-rollout/SKILL.md` | `fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b` | `9aa820ea6ca15b4e136c9772423b78ed4df6a3d4` |
| `.agents/skills/gme-equipment-rollout/references/source-map.md` | `40612c5efb8f94608840c7bc0e9095ea840df54920861c388ae48ea34c7998dc` | `49e50a7a8e56a16e2ec7f3607a03fd90adb8f1d3` |
| `AGENTS.md` | `0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2` | `073164bc6efd5791032d62c71b03b4dab48cb6f8` |
| `VERSION.json` | `5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7` | `fffb51663b7705aec91cb119ca80ee943a4ce758` |
| `all-in-one/assets/program-model-data.js` | `52f8199371e3399b7c0d44ab5469f0472aced79d56bbef2887f7625f5d2aff0f` | `38f34b0caa380a16ccad6f6f1e234a2fdf23f327` |
| `all-in-one/assets/simulator-workspace.js` | `3a6dfc618ff7e7b238f2671dc85d65704f33093a18eac879d86081d92c31e8bc` | `97c2c831c77a9699fff0e0960b3bc1b7d93d45b3` |
| `all-in-one/assets/virtual-plc.js` | `5f1876052dc0067b1f010af0dfc941946e37003167481731293615d9c1c36dbc` | `0bd9eceb54365a91214a37c5601b5067c39a3f75` |
| `all-in-one/registers/equipment.json` | `7870325dff32bbca90fa34507b301c4aad3347d669fddcd03b910343663996fa` | `acc42633033398216469064932c4b76987371606` |
| `all-in-one/registers/program-model.json` | `6203479c086b15bada12ac9d7e37db9280234ec26f1ea6091d7211dc09a577c5` | `9860b10f008d3a5ae714be50d77b703dfec32f3a` |
| `all-in-one/registers/simulator-freeze.json` | `bb93c1994effc5609939ba566b7802ce7ed55154a7310f02379b308ac2c8c835` | `808ffac14dbd1b4a7d797fa6cd0d647635d90b47` |
| `all-in-one/registers/virtual-plc-test-results.json` | `a6b389f797f9a8b5ffe6928b8420f55c4cc459a327b0b48d716079d2eca6dd64` | `757dd50e45184568facb8ff62900b39d3ce848d1` |
| `all-in-one/sources/Electrical_Can_Decoating_20241118.pdf` | `3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd` | `0ee6b6f8361c5790864dbba4bbd9d55e8e7c08f8` |
| `all-in-one/sources/Electrical_Rev2.pdf` | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` | `f610fd7c7ce14ae951b00cff57b969259bfb389d` |
| `all-in-one/sources/GME_20250506.zap18` | `00c79b6d986e68298f65b172c1807115bc5d9e450a74fcc989d0796d8d8a4ea8` | `211c4f604627a32f82a1124c2a9872c2fcf00865` |
| `all-in-one/sources/PEData.plf` | `647de7ea123daced41c27bec8f81aeb93c712cac714d4754d7da5c528abb016a` | `65605ff8910f920109da731604aa5dc8d83fc956` |
| `all-in-one/sources/decoded-original/0014-FlgNet.xml` | `2e814adbaac6bab99bc668bfdab74f0fc90576324d0b88728951683869cfac30` | `4d164b074fcc13a8f97da9e24382cc169ef29555` |
| `all-in-one/sources/decoded-original/0164-FlgNet.xml` | `15884b2b362842279b626b669a484b1daa269f5ecd99112b8391bb0387382491` | `1035a51ee3100d524da1b7b204ba142b6b509ac5` |
| `all-in-one/sources/decoded-original/0165-FlgNet.xml` | `4513a5f6e77717c99c5e869105483be31f7f62ab280e271dc36cd7a2d3e3bb88` | `8d636eb535060037ccf00ebdfb328b8775225fe4` |
| `all-in-one/sources/decoded-original/0175-FlgNet.xml` | `41279d6aaa157de3be963d010d6ca7dea94811a0ace519c8a3d8baa015f67f97` | `1626da00b3bbcb46f77720271ecf0f50db9dc63b` |
| `all-in-one/sources/decoded-original/0178-FlgNet.xml` | `36752e04a38e486ad4a0857d6baa8119d9b757678300358bcc95881f23e266c9` | `5831f5a312f2fbc2738b5e18de1aba6016bd8c36` |
| `all-in-one/sources/decoded-original/0181-FlgNet.xml` | `98e839ee13a05db05768503e768e9238d892c4788dc7b6c9d3017fc86d3b722b` | `ff48f9494436c2557ad1d3d45edd4197f3e622fe` |
| `all-in-one/sources/decoded-original/0186-FlgNet.xml` | `932f8756ee0e4385553944bd166109c45684766a136bfddd68cdf08552a83883` | `744ced99611f666064f30aae4ac32c5d38622d9e` |
| `all-in-one/sources/decoded-original/0237-FlgNet.xml` | `ad3721660c2f357e76c1a351f7898691271f35c341efe775e5780d749b2c4aa0` | `c97f914bb78760dd6fd42a46d3596983beb352f4` |
| `all-in-one/sources/decoded-original/0238-FlgNet.xml` | `8f6a5537084e092c352552dc469bbe8469b33412971219e51bba211ef607dfa8` | `c1093180555a6a00486d0a7268bb3a059b7cbf9e` |
| `all-in-one/sources/decoded-original/0291-FlgNet.xml` | `fe0b92f074eba25148ce34084649af3d968962558d652727f1eea19f3e3c2550` | `1418fb2ed172c6df694a5eb8bf2dffd0b177653b` |
| `all-in-one/sources/decoded-original/0342-FlgNet.xml` | `9ef93abad16cc055509ef98c388417c716cb03d23cb02aed6d95888beb43bef8` | `a9b1841964216331887d18f91c014c0534cc9df1` |
| `all-in-one/sources/decoded-original/0398-FlgNet.xml` | `4f092b18df4e44af98fd44e173f48dad213a4e80b71f46b0a5e8a700f5b0a747` | `67ebb54daa55093487ea7e780f23ae2cf193c397` |
| `all-in-one/sources/decoded-original/0401-FlgNet.xml` | `60171c213e666de544077b7e4b497675813f7c0e75df85a3e76ab1def49b04ae` | `aadefbd35d305dd4a1146bf383b988a903802bf4` |
| `all-in-one/sources/decoded-original/0477-FlgNet.xml` | `e7b5b0cb95c60d1112081f6129a3127f8413e1b1d2a4c67d0e203d36ea0a711a` | `8bc2088bf4bb5eb8d51e0d9186879fc61d2c27df` |
| `all-in-one/sources/decoded-original/0480-FlgNet.xml` | `c14d2fee14b38b7c597edb46626676f0cf550b5831668884cb2fac341b559273` | `d17dfbf4a5e25e09c25b13721d6a81636ad62ad9` |
| `all-in-one/sources/decoded-original/0491-FlgNet.xml` | `f7395b1dc4f33553114a108c61691cb24b830d2152b31e6e9cd9f7718ecc9b1d` | `a2eb014c107e824cd0ab6285d61b70ce4f03781a` |
| `all-in-one/sources/decoded-original/0528-FlgNet.xml` | `cc856c9e70accae5f3f3ff16cb1d4f6d3c00ab7f5b538ff9d58cdf97b23845d0` | `e7029045fdd4e8bae4c766507dc71eadabfc30dc` |
| `all-in-one/sources/decoded-original/0548-FlgNet.xml` | `cc21a5b04a0d17b1d0ce7dceca752b6570ccd9d961c0ec3c6c5c734f648ae83e` | `149b184192970060f32956ec81a8408c7f7a30b1` |
| `all-in-one/sources/decoded-original/0549-FlgNet.xml` | `49f7169c33ed7f54559b0801e21a7d618584900972840e91cf51ad032e8febb1` | `985b5310b43b1015b5dee286aa0e42800564b94b` |
| `all-in-one/sources/decoded-original/0554-IdentXmlPart.xml` | `4ae3e7d0bca0f78c9e94617abeb70bdd228d85d74bff2224174fa1bb0076e78c` | `cdb68b35a7287f6b5636c01ea3a01747d3d60e81` |
| `all-in-one/sources/decoded-original/0564-IdentXmlPart.xml` | `2aed17fa02d19b0a081023282841aa561d6a2dca3e393284da3622b967af00b1` | `c4b1f2cb191970cfce1cce59cb290a9f1f934c37` |
| `all-in-one/sources/decoded-original/0575-IdentXmlPart.xml` | `40e7b2caf89ab7f1ed9075547a7728bd02441e24451bdd8bf97c843637daad06` | `07d5d2548e8f36252a346d0b83341e27c3cb14ba` |
| `all-in-one/sources/decoded-original/0577-IdentXmlPart.xml` | `511e01fae619dc385357908a1ac62030dbdfd5f5399bd4c22bc58bebbfc3bf47` | `a505ebf7efd05a85850dc29559a4f71242bacae3` |
| `all-in-one/sources/decoded-original/0578-IdentXmlPart.xml` | `0f9f41b5dee25ea17c7a29ab6f7b00503c13d0f265266acd660072baf061d32b` | `070a79fb12139898dd44a17ab2061e795956b9c6` |
| `all-in-one/sources/decoded-original/0582-IdentXmlPart.xml` | `41d4c2bd750392bbc2edc43995ec3a9da47a63c13ee86496df8f187492008951` | `82636dec064876d0f4cc714ef385b07d6e05efe0` |
| `all-in-one/sources/decoded-original/0583-IdentXmlPart.xml` | `0a34a2b7ad17eba6198dbe53d5c6aa8e87710c7436b832b9d39a075074ab58a8` | `63a23c921a53805f135a0399ba076265907d0eda` |
| `all-in-one/sources/decoded-original/0585-IdentXmlPart.xml` | `e36ec18aa4abebea8f9160254522bb51ff722eae804c5a469790f85f02939184` | `16574d37ef3ca61b59ba396c400e269ab1dd3440` |
| `all-in-one/sources/decoded-original/0586-IdentXmlPart.xml` | `f16c4c68bde8a737372c219a10b21501653dfd3ba8c59bd84b60ae6d62da8250` | `266989c590cf52f82e1553f8626a209b8c0b6e0b` |
| `all-in-one/sources/decoded-original/0602-IdentXmlPart.xml` | `46ab21151eddaaf616469db520730c60423eb742aa491af194e6710c751b4caf` | `bcb12ab1ce8c476ff921baa1608f29d9822f76b4` |
| `all-in-one/sources/decoded-original/0604-IdentXmlPart.xml` | `b798d29c5499b5314a1ee3cff9139dae64c887533b86baa43b6e9a052373a6af` | `bb2c318788b97e7a4924a176275c12d805aa519d` |
| `all-in-one/sources/decoded-original/0605-IdentXmlPart.xml` | `0ff6e2228dbfbc9f657359fe1055083ce621365084ea24c4160e4969b3eaac8b` | `30e199288c147aa22d5ce8407178a391b89c6b1b` |
| `all-in-one/sources/decoded-original/0611-IdentXmlPart.xml` | `0d583915a261703954da22c176ba9f81338ad13ea2810e7cd5f7de8aa1bfa089` | `bad6b16fb32a32d47d882f48754994887457872b` |
| `all-in-one/sources/decoded-original/0612-IdentXmlPart.xml` | `95b545d4964d371ebfc107894ea90b8b1d0d7ab5d3a70e643f8ce539063c0f38` | `7cc782d33d07ef225c2104f3e7c9fbd31f7c7467` |
| `all-in-one/sources/decoded-original/0617-IdentXmlPart.xml` | `10bcf85169cb2512f55acadaef299a3d46b4b4cecd88032d739cfeba23e94aa9` | `9527658ee6808be34bd513b1b2ebaf3a4a5a6f3e` |
| `all-in-one/sources/decoded-original/0619-IdentXmlPart.xml` | `85694bb5b696e31e6a1217431112e5b750516c4f94078d6e127d4394a8b80456` | `11f0502c84a1f319a21459a35c0dc1c6ce8e8f36` |
| `all-in-one/sources/decoded-original/0627-IdentXmlPart.xml` | `08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb` | `61ebc0abbb2ca160e11e1da400a3f14a397d8bc5` |
| `all-in-one/sources/decoded-original/0628-IdentXmlPart.xml` | `9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd` | `170ca5c72599edc7ea7eefe651c3680ce325e76a` |
| `all-in-one/sources/decoded-original/0629-IdentXmlPart.xml` | `67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972` | `058129bb01e27f7a6a0d0293f332d745e5bab74e` |
| `all-in-one/sources/decoded-original/0632-IdentXmlPart.xml` | `fd162c603476c2cac899010cee7a8ee382b6092c115135e3ac1007ae71c544e9` | `600935fa8d394c0d247ea20040d5dfff4f05b500` |
| `all-in-one/sources/decoded-original/0633-IdentXmlPart.xml` | `9e00aa275fa1b4e488b73983b309c6b73dcf4f3dd9be5dec13e9975d68f3c0fc` | `a1ab5ee12addbc92d04c9950d4437e2b564d6b5c` |
| `all-in-one/sources/decoded-original/0642-IdentXmlPart.xml` | `c922483c261c8ddb98c239a7b4dc3d7f73f9a45261dd5b4d669f39d6918a1c21` | `398f73b99c4a792a68387485fcb47048d166b2a1` |
| `all-in-one/sources/decoded-original/0665-IdentXmlPart.xml` | `50e88d5f50f555151b35cfb17225e766c34ef6b490bd3a48e0a4e335fd17e3dd` | `ea4a8a5013081f648722c5ebbde3bb1366787990` |
| `all-in-one/sources/decoded-original/0667-IdentXmlPart.xml` | `ef924ced3e0e2b17e9c8440eb4946cd50d55df644c6ec24a1c4fd288fa6b73a3` | `7f2e1798eb9f260d19d038a83369484d0f438856` |
| `all-in-one/sources/decoded-original/0668-IdentXmlPart.xml` | `2248e994a0a02cd37c5c5edaca199b3421068feea91e2e8616560e814ef9f6ed` | `fe0f30d1eaae37783b0f03cb090353b3a3de3600` |
| `all-in-one/sources/decoded-original/0669-IdentXmlPart.xml` | `754c513339d00918717010047b8f9d865d8674c6978a6f86c6f1fa5d683506e2` | `f5bf8f3c41d2a07ba9dcfd8f400548be8cf51cd3` |
| `all-in-one/sources/decoded-original/0670-IdentXmlPart.xml` | `e56f3f0c4f2a86dd18578dedd4453915c2a51cd25e2cd9feced8538171a00841` | `b9466007b14e5c4f5d353dca5734401317e2dc03` |
| `all-in-one/sources/decoded-original/0671-IdentXmlPart.xml` | `26cb51706305c372d512c19770648bb0dbb74df8bd2277b1e0da1b8c88cca293` | `e38a4e2c93ac8093e2b0b8e082a64688b5d9845e` |
| `all-in-one/sources/decoded-original/0672-IdentXmlPart.xml` | `6bfc2ba142d6270c39eb1f13b2886204865af6d46eadc5f410c26981b8da9222` | `2f2790dab4bb2357733112220e0acc41edb6feb6` |
| `all-in-one/sources/decoded-original/0674-IdentXmlPart.xml` | `4770702f519bacda69202bb2f7733d983074bda90964360c238f990d9d08fd84` | `f210593944547b63eab10c667348711413600aab` |
| `all-in-one/sources/decoded-original/0676-IdentXmlPart.xml` | `c58427c5b0ac6c11cdb52e4c6d0461c7b191fae81ccace191048e9f175fcec59` | `1ed67265f69796a4e659f9438e551068037f33a4` |
| `all-in-one/sources/decoded-original/0678-IdentXmlPart.xml` | `51e637e0b9713c028810f2a717b5c3804a3a26c2f1be7e332a4d6bf277bfc382` | `7fafb2297bcdf739bf1d1dd68cebc0d74f2a40cc` |
| `all-in-one/sources/decoded-original/0680-IdentXmlPart.xml` | `fd551ad5d47bbd66c6bcdcc1949aaddf68cc086a3ddf6fb337adc767954c2b95` | `c9049ced1eaed72c5e251a88601d46ddec8c3e50` |
| `all-in-one/sources/decoded-original/0682-IdentXmlPart.xml` | `25c7aeb1bfa29c178eaa396db33d4eb6d2d29b9a3f2eb965fa61fae8ce7f1092` | `61182411e912941161eccf4e90c1f174e5379f0a` |
| `all-in-one/sources/decoded-original/0683-IdentXmlPart.xml` | `0c9b569d041cd5babbbeded8a3bdc5d3754927125756b6ac54b7cb991b22fc22` | `662acdb9a06c0ba1c0027e7dd215a28f07d3f02b` |
| `all-in-one/sources/decoded-original/0684-IdentXmlPart.xml` | `6e9b3f173184adcddca503e81e2649022734b6ea3639c1d5ddaf0a08bac00208` | `d67b98b5d5516e0330aae5cfdbee41a3e09206e1` |
| `all-in-one/sources/decoded-original/0685-IdentXmlPart.xml` | `2003d5741a0d707755c5e6e8b737fa106414b87b5b431b97271d9f1a5d343448` | `86bda988d9efedba92ba2f3e4877497d9eb5230a` |
| `all-in-one/sources/decoded-original/0686-IdentXmlPart.xml` | `b450d8ff22f0fffd7a214b2a696af28a03a27834ebf862bfaa822dc9bfb3c8d4` | `8c152d926692a8e15973c980e08e338d29411814` |
| `all-in-one/sources/decoded-original/0688-IdentXmlPart.xml` | `ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda` | `463585759f1ecd94f32362b4fefb000a152f5773` |
| `all-in-one/sources/decoded-original/0690-IdentXmlPart.xml` | `fcd6af9e8af48f9737d4764d7765d2eebdf95bd5e0c8e7b4faf6d1ed4eba1541` | `36bd403f48ba8e364126837b19fb0419bbe78941` |
| `all-in-one/sources/decoded-original/0692-IdentXmlPart.xml` | `bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037` | `737785d03b5fad43c5b4d451955726d800edb1c0` |
| `all-in-one/sources/decoded-original/0694-IdentXmlPart.xml` | `757ccebdf32d0a168dd787bfa735fe6494eac4c4a9f7a5adc63898a88e8b152d` | `c45e8f3ca4129dc06734f6a12ef79e6ed6528a7d` |
| `all-in-one/sources/decoded-original/network-map.json` | `c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60` | `424430b6b953e43138e5d0a18ca40c949e21cfa1` |
| `all-in-one/sources/hmi_plc_tags.csv` | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` | `cf4c0650e7c7baac350dcb89909b808435704880` |
| `all-in-one/sources/live_index.json` | `14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1` | `e35ccea1f841349c632666c29954b7bcd4f5839e` |
| `all-in-one/sources/source-manifest.json` | `5af6e85994536897fd92f75972534a691e6eb0f067aafe07679c0788fd84e5bf` | `38cf407491d52dc6128cf94ca8a4bddee350de6d` |
| `docs/equipment-standard/INVENTORY.json` | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` | `587c3748ad9224718f95ba06463fee913dae231d` |
| `docs/equipment-standard/START-GPT61.md` | `35769e3146ccd707fea2b81b67b30376b76a0a19c7e662fe2bb4fdd382306f94` | `0d08cab3678df7e2625251b641b138ef4956483b` |
| `docs/equipment-standard/WORK-ITEM-TEMPLATE.md` | `4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586` | `e546f39535d2b589e80f97db869ac37ce4d05cfd` |
| `docs/equipment-standard/WORK-STANDARD.md` | `05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99` | `f76a570cc73098632e08759b17934000f7e3a253` |
