# SYS-PLC-IO — CPU·분산 I/O·신호 변환 7영역 자체 조사 초안

문서 범위 완료·누락 포함. 고정 백업과 도면의 대표 핵심 정적 조사이며 현재 CPU 모델/통신/설정, TIA 컴파일, 현장 복구, 매뉴얼 통합·게시 완료가 아니다.

## 핵심 확인·상충·누락·공유 근거

- 원시 I/O와 내부 DB 미러를 분리했다. 0397은 Word 복사 외에도 MV03 입력 Bool을 NOT 처리하므로 `Inputs = 모든 원시입력의 무가공 복제`라는 설명은 부정확하다.
- TC04 대표 채널은 미러에서 IW256(SAM=None), 환산 호출에서 IW256:P(SAM=Peripherie)이다. 주소 숫자가 같아도 접근 종류·형식·관측시점을 같다고 단정하지 않는다.
- 0401은 출력 Q Word → DB14 미러다. HMI가 DB14를 썼다는 것과 물리 Q 명령은 별개다. SYS-HMI의 공유주소/실제 위젯 미확정은 그대로 연결한다.
- 진단 이벤트 OB의 SCoil과 allarms 0542의 집계·Reset을 직접 대조했다. Reset은 누적 표시와 원인 기억 비트를 지우는 코드이며 실제 통신·하드웨어 복구 증거가 아니다.
- TM 대표 MV01은 ErrorAck/EventAck가 RESET_ALLARM에 결속되지만 MV06 동일 핀에는 RefId가 없다. MV01의 결속을 모든 엔코더에 복사하지 않는다. Error/ErrorID 등 미결속 핀의 현재 진단 저장 위치도 발명하지 않는다.
- 도면 FG102는 CPU 1515-2 PN, FG103은 TM COUNT를 표시하고 FG144/148 제목은 TM TIMER다. FG103의 103A6/7/8 도상 안에는 6ES7550-1AA00-0AB0, 하단에는 6ES7550-1AA01-0AB0로 서로 다르다. 백업 명령 High_Speed_Counter와 도면 제목 차이를 보존한다. 현재 하드웨어·온라인 구성의 일치와 TM 파라미터는 미확정이다.
- JB2 구성은 **FG182 / 실제 PDF185**. 고정 원본 devices/SYS-PLC-IO.html의 `#page=183`은 실제 FG180B다. 이 경계는 이미 [BF02](BF02-DOTS-DRAFT.md)가 확인한 사실이며 이전 초안의 신규 오류라고 주장하지 않는다.
- 공유 연결: [SYS-HMI](SYS-HMI-DOTS-DRAFT.md)의 출력미러·CSV/이벤트 경계, [TC04](TC04-DOTS-DRAFT.md)의 선형화·계측 전기, [MV01](MV01-DOTS-DRAFT.md)·[MV03](MV03-DOTS-DRAFT.md)·[MV06](MV06-DOTS-DRAFT.md)의 엔코더/처리 입력, [BF01](BF01-DOTS-DRAFT.md)·[BF02](BF02-DOTS-DRAFT.md)의 분산 I/O 근거. 아래 선택 핀·선언·도면은 원본 독립 대조했고 관련 설비 전체 완료를 복제하지 않는다.

## 1. 설비·자료 기준

catalog_id SYS-PLC-IO, software/공통 시스템, parent 없음, phase2. INVENTORY catalog[41], equipment[238], 별칭 mod_err/prog_err/rack_flt. 한 소프트웨어 기능 ID이며 CPU·각 I/O 모듈·모터·센서를 한 실물로 병합하거나 하위 설비 완료로 집계하지 않는다.

고정 읽기전용 `gme-research/source-mv06`, commit `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, v1.12.0. AGENTS, rollout SKILL, WORK-STANDARD, WORK-ITEM-TEMPLATE, INVENTORY와 VERSION/WORKSPACE-HANDOFF/PUBLICATION_STATUS/EXPANSION/ACTIVE-WORK 최신 머리말, BATCH12 지시·범위와 GME-CATALOG-OVERLAP-REVIEW의 해당 ID를 읽었다. 로컬 2차133 통합 제외 유지. 모델 런타임·추론 증명 미확인. 이후 사용자 보고 게시 버전을 이 자료로 검증했다고 주장하지 않는다.

아래 네 자리 파일번호는 `all-in-one/sources/decoded-original/NNNN-FlgNet.xml`, 선언번호는 같은 경로의 `NNNN-IdentXmlPart.xml`. 문서 ID/LAD, NID, UID/RID와 파일번호를 구분한다. network-map/live_index는 탐색 색인; 핵심은 XML 선언·Part/Wire·실제 PDF로 대조한다. archive GME_20250506.zap18와 PEData.plf는 존재하는 백업 원본이며 이번에 TIA로 열거나 하드웨어 전수 추출하지 않았다. FG102의 모델은 도면 표기이며 백업 하드웨어 구성/현재 CPU 모델을 확정하는 대체자료가 아니다.

선택 의미 검토: 0000/0001/0002/0003 진단, 0542 집계·Reset, 0397 입력 Word/대표 NOT, 0398 대표 아날로그 미러, 0401 출력 미러 대표, 0481 환산 호출, 0291/0014 공통 환산, 0506/0510 대표 엔코더, 0030 입력미러 호출 경계. 전체 입력/출력/환산 46네트워크·모든 핀·모든 Writer·바이너리 프로젝트 전수 의미검토가 아니다.

수정 범위는 이 MD 및 `extracts/SYS-PLC-IO/`뿐. 새 Work/Codex·재위임·사용자 Mac/TIA 접근 없음. 공통코드/대장/버전/배포/운영 기록/원본/다른 초안 수정0. 원본 build/test/generator, 시뮬레이터 작성·수정·생성·실행·행동시험, 실제 PLC·현장·보호값·SEJIN 변경0.

## 2. I/O·HMI

### 2.1 원시·Word·Bool·환산을 분리한 대표 주소

SSD.AO는 bit offset. DB 번호는 DepDBBlock.TOD와 결속한다: 0628 RID4=DB13, 0064 RID26=DB14, 0674 RID8/11/354/177=DB4/1/3/91, 0682 RID10/15=DB3/2.

|대상|백업 선언·주소|역할/한계|
|---|---|---|
|Tag_178|0627 RID3, Global Word Input AO0/SAM=None, NID1 UID25 = IW0|0397 Word 원시 복사 입력|
|DB13.DBW0|0629 RID5 Global Word AO0 BAD4, NID1 UID26 Write|원시 입력과 별도 메모리 Writer|
|MV03_Open / Close|0627 RID152/154 Global Bool Input AO61/62 = I7.5/I7.6|0397 UID132/152, 원시 리미트|
|Inputs.MV03 open / Close|0629 RID153/155 Global Bool AO61/62 BAD4 = DB13.X7.5/X7.6|UID148/153 Write, NOT 처리. 정상 실물극성은 미확정|
|TC04 미러 입력|0627 RID156 Global Int Input AO2048 SAM=None = IW256|0398 NID2 UID25|
|Inputs.TC_04|0629 RID157 Word AO192 BAD4 = DB13.DBW24|0398 UID26 Write; CSV INT와 원형 Word 구분|
|TC04 환산 입력|0678 RID456 Int Input AO2048 SAM=Peripherie = IW256:P|0481 NID1 UID54; PIW 접근과 미러 접근을 구분|
|Coeff.ZERO_TC04 / COEFF_TC04|0676 RID10/9 Int AO864/880 = DB4.DBW108/110|보정값, 현재 설정 미확정|
|Data.Temp_TC04 / TC04_OFR|0676 RID12 Int AO928 DB1.DBW116 / RID355 Bool AO162 DB3.X20.2|환산 결과/범위출력; 원시 미러와 별도|
|Tag_280 / Tag_291|0632 RID24/48 Global Word Output AO0/176 = QW0/QW22|0401 NID1 UID33/89 읽기|
|DB14.DBW0 / DBW22|0633 RID27/49 Global Word AO0/176 BAD26, UID34/90 Write|0401 출력 관찰용 미러|
|fill_unit1.SW_GATE0 / ACT_CNTV0|0676 RID207/209 Bool AO184 / DInt AO1184 BAD177 = DB91.X23.0/DBD148|0506 NID50 UID27 입력/47 CountValue Write|
|fill_unit1.SW_GATE4 / ACT_CNTV4|0676 RID261/263 Bool AO188 / DInt AO1440 = DB91.X23.4/DBD180|0510 NID49 UID27 입력/47 Write|

### 2.2 HMI 설정 대표

`all-in-one/sources/hmi_plc_tags.csv` 실제 행729 I_TC_04(00065)=DB13,INT24, 행595 Allarmi_139(00103)=DB3,X17.3, 행189 StatusPLC(002DF)=$SYS$Status. Access Name PLC는 설정 문자열이다. DB13 Word를 HMI에서 INT로 읽는 형식 차이를 보존한다. 진단 집계 DB3.X17.3과 드라이버 상태는 다르며 현재 통신 정상·화면 위젯·Writer·ACK 이벤트를 입증하지 않는다. HMI 전체 계수/동일주소 I_W20/O_W20 등은 SYS-HMI의 고정입력 검토를 연결 재사용한다.

## 3. 제어 구조

### 3.1 입력 미러와 개별 재쓰기

0397 LAD1070 NID1: rail W21→Move22.en, W23 UID25/RID3 IW0→22.in, W24 22.out1→UID26/RID5 DB13.DBW0. Move22 DisableENO=true지만 원본 W34는22.eno→Move27.en을 연결한다. 표시속성과 연결을 모두 남기며 실행 성공·주기를 추측하지 않는다.

동일 네트워크 MV03는 W122 UID132→Contact127.operand, W137 127.out→Not142.in, W145→Coil147.in, W146 UID148→operand. Close는 W155 UID152→Contact149, W156→Not150, W157→Coil151, W158 UID153→operand. Word복사(예: IW6→DB13.DBW6, Move42 W52/W54)와 그 안에 속하는 개별 bit 쓰기가 같은 DB 범위를 다룬다. 따라서 이 미러 전체가 단순 raw 동일성 보장이라는 설명을 금한다. 현재 스캔 최종값·다른 Writer 부재는 미확정.

0030 main LAD1613 NID19: W31→CRef21.en, ENO 사슬 W32→CRef23, W33→CRef25, W42→Contact37, W44 UID45/RID140 Simulation(1)(0692 M180.0)의 NOT, W43→CRef28.en. 0688 FCBlock RID120/124/128/135의 TOD는 각각 FC21 Recipes Handler / FC11 HMI / FC19 HMI Output / FC15 HMI Inputs로 직접 대조했다. 이 조건 이름을 근거로 중지된 시뮬레이터를 실행하지 않았다. 현재 해당 비트 상태·실제 호출주기·온라인 스캔 순서는 미확정.

0398 LAD1071 NID2의 TC04는 Move22 W23 UID25(Int IW256)→in, W24 out1→UID26(Word DB13.DBW24). W33은22.eno→27.en. 미러는 물리 입력으로 되쓰지 않는다.

### 3.2 출력 관찰 미러

0401 hmi output NID1: W56 UID33/RID24 QW0→Move22.in, W58 out1→UID34/RID27 DB14.DBW0. 마지막 대표는 W87 UID89/RID48 QW22→Move85.in, W88 out1→UID90/RID49 DB14.DBW22, W86=Move32.eno→85.en. 개별 설비의 최종 Q Coil/아날로그 출력 Writer는 각 설비 소유다. 이 함수는 Q를 읽어서 DB에 쓰며 방향을 반대로 설명하지 않는다. startup live_index doc401과 파일0401은 별개다.

### 3.3 공통 선형화와 대표 TC04

0481 LAD1731 NID1: ON UID52 W59→Contact65, rail W67;65.out W66→CRef46.en. CRef46 RID351/0680, CodeBlock58 RID5/0672 = FC63 Signal linearization. IN0는 ON UID53 W60, Analog_input은 TC04:P UID54 W61, Coeff/Zero UID55/56 W62/63. OutValue W64→UID57, Out_of_range W24→UID23. 출력 소유는 TC04; SYS-PLC-IO는 공통 변환/접근 경계만 묶는다.

0291 LAD1658 NID1, 0611 Local InterfaceAccess: IN0 RID1 Bool, Analog_input RID3 Int, Zero RID8 Int, Coeff RID13 Int, OutValue RID19 Int, Out_of_range RID26 Bool. App3/4/5/6는 Local이며 DB 전역으로 만들지 않는다. 0612 상수 RID25=-1382,29=32767,17=28000,21=-9999.

- IN0 Contact255 W256 뒤 Gt258 raw>-1382, Le161 raw<=32767→Convert164. Int→DInt 변환164/167/174, Add170/Mul177/Div181을 거쳐 `(DInt(raw)+DInt(zero))*DInt(coeff)/28000`; Move185 W247→OutValue UID215. ENO W227/230/234/237/241/245 보존.
- Gt190(raw>32767) 또는 Le259(raw<=-1382)→OR47 W49→Move193, W252=-9999, W253→OutValue UID219. Move193.eno W21→Coil23, W22 UID24→Out_of_range. OFR를 단순 비교 Bool로 축약하지 않는다. Int 상한초과 조건의 실제 도달 가능성도 현재 CPU에서 시험하지 않았다.
- 0014 LAD1659 NID2: NOT IN0 Contact171 W172→Move162, W169 UID166/RID23=0, W170→OutValue UID167. 비활성 함수 호출과 IN0=false 실행은 구분한다. -9999/0은 백업 대체값이며 안전 설정 권고가 아니다.

TC04 개별 경보·온도단위·현재 교정·발생 후 정지는 TC04/FN01/BR01 관련 소유다. 다른 아날로그 45개 분기의 선택접점/복수쓰기(RO03의 별도 Add 등)는 각 초안의 근거를 재사용하고 전수 검토했다고 하지 않는다.

### 3.4 엔코더·TM 대표와 미결속 경계

0506 LAD1756 NID50: W50 rail→NOT Contact21(Simulation(1) UID25/RID344 W51,0678 M180.0), W52→Contact22(EM_OK UID26/RID173 W53), W54→LRef23.en. 0679 Instruction RID330 High_Speed_Counter(S71500 Target), 0673 RID462 UID24 InstanceDB DB15 MV01_Encoder. W55 UID27/RID207→SwGate, W58/59 UID30/31 RID464 Flag.RESET_ALLARM→ErrorAck/EventAck, W75 CountValue→UID47/RID209 ACT_CNTV0 DInt DB91.DBD148. RESET_ALLARM은 물리 동기화·완전복구 자체가 아니다.

0510 LAD1760 NID49는 같은 조건/명령 형식, Instance RID350 DB19 MV06_Encoder, SwGate UID27/RID261, CountValue UID47/RID263 DB91.DBD180. 그러나 ErrorAck/EventAck의 UID30/31은 RefId가 없다. 원본에 없는 Reset 배선을 MV01에서 복사하면 안 된다.

두 호출의 StatusHW/StatusGate/StatusUp/StatusDown, CompResult0/1, SyncStatus/CaptureStatus, CapturedValue, ZeroStatus, PosOverflow/NegOverflow, Error/ErrorID, MeasuredValue/CompareMeasuredValue에 연결된 ORef33~46/48/49는 RefId가 없다. 이 출력들을 특정 DB/HMI 경보에 연결되었다고 단정하지 않는다. CaptureEnable/SyncEnable/SetCountValue 미결속, 실제 하드웨어 ID·카운터 입력 형식/분해능/필터/주파수·제로/교정 파라미터도 미확정이다. MV02/03/05의 전체 호출·기억/위치관리 0511~0516은 이번 대표 의미검토 밖이며 기존 MV 초안을 연결 참조한다.

## 4. 전기 끝점·구성·실제 PDF

원본은 `all-in-one/sources/Electrical_Rev2.pdf`. 아래 **11개 서로 다른 실제 PDF 페이지**를 렌더하여 직접 시각 확인했다. 표의 DATA는 모두27.05.2024, TOT262. 개정란 공란은 파일명이 Rev2라는 이유로 Rev2라고 채우지 않았다.

|실제 FG / PDF|확인 내용·대표 끝점|개정란|
|---|---|---|
|102 /103|CONFIGURATION PLC. 102CPU SIMATIC S7-1500 1515-2 PN,6ES7515-2AN03-0AB0,메모리6ES7954-8LE03-0AA0. X80 L+/M, +24Vdc10.10/-0Vdc10.6, 16/9·99/9→103/1. RJ45 PROFINET 양측1/2/3/6 도식. 102A1~4 POS2~5 AI8xU/I/RTD/TC ST6ES7531-7KF00-0AB0;A5/6 POS6/7 AQ8xU/I HS6ES7532-5HF00-0AB0;A7/8 POS8/9 DI32x24VDC HF6ES7521-1BL00-0AB0|공란|
|103 /104|103A1~3 POS10~12 DI32 6ES7521-1BL00-0AB0;103GD1 POS13 PS25W24VDC6ES7505-0KA00-0AB0, X80 1 L+/2 M/3 PE.103A4/5 POS14/15 DQ32x24VDC0.5A HF6ES7522-1BL01-0AB0.103A6/7/8 POS16/17/18 TM COUNT2x24V6ES7550-1AA01-0AB0. 도상 내부 6ES7550-1AA00-0AB0와 하단 6ES7550-1AA01-0AB0가 상충하며 실제 부품번호는 제조사/현물 대조 필요|공란|
|104 /105|ANALOG INPUT MODULE, CPU515 MOD2. TC04 +PEW256(79/3)→2 I0+ 및6 I1+, -PEW256→4 U0-/I0- 및8 U1-/I1-;PEW256/258 병렬. TC05 +PEW260→10 I2+ 및14 I3+, -→12/16.18 MANA→-0Vdc10.6. 온도범위/4–20mA표기|Rev2 17.03.2025|
|116 /117|DIGITAL INPUT MODULE CPU515 MOD8,단자1 E0.0 BC01 feedback→18/7,2 E0.1 BC01 alarm→18/7;3/4 RD01 E0.2/0.3→20/7,7/8 MC04 E0.6/0.7→24/7. 센서/드라이브 실제 상태·정상극성 미확정|공란|
|134 /135|DIGITAL INPUT MODULE MOD12,SPARE E18.0~18.7,단자21~28→X21:3015~3022. 예비표기만으로 현장 미배선/사용불가 확정 금지|공란|
|136 /137|DIGITAL OUTPUT MODULE MOD14,단자1 A0.0 BC01→19/2,2 A0.1 RD01→21/2,5 A0.4 MC04→25/2,7 A0.6 VS01/01A→28/2. +24Vdc10.9→X21:3028 5x20 4AF→단자9;10→-0Vdc10.6. 표기 퓨즈값은 현행 보호설정 권고가 아님|Rev2 17.03.2025|
|144 /145|TECNOLOGY MODULE TM TIMER,CPU515 MOD16,MV01 encoder ZT02.45.1→단자2 CH0.B,45.2→3 CH0.N,실드45SCH1→접지.37.2→9(24VDC),37.1→10(M),FG45/3.1 CH0.A에는 이 그림에서 신호선 미표시. E20.0/1/2 예비4/5/6;A8.0/1 예비7/8|공란|
|148 /149|동일 제목,MOD18,MV06 ZT06.33.3→2 CH0.B,33.4→3 CH0.N,33SCH1 실드.33.2→9 24VDC,33.1→10 M(FG33/2).E22.0~2 및A10.0/1 예비. 현재 엔코더 유형/채널설정은 미확정|공란|
|153 /154|CONFIGURATION PLC JB1 BOX.153IM1556ES7155-5AA01-0AB0,153A1 AI6ES7531-7KF00-0AB0 POS2,A2 DQ6ES7522-1BL01-0AB0 POS3,A3 DI/DQ6ES7523-1BL00-0AA0 POS4,A4 AQ6ES7532-5HF00-0AB0 POS5.24Vdc152.5/0Vdc152.4→1L+/1M·2L+/2M도식. PROFINET X1P1/P2 기호;실제 IP/장치명/토폴로지 미확정|공란|
|180B /183|ANALOG OUTPUT MODULE MOD5,PAW344/346/348/350 SPARE 단자21~36,+24Vdc152.5→X22:4028 500mAF→41 L+,44 M→0Vdc152.4. 이 페이지는 FG182가 아님|공란|
|182 /185|CONFIGURATION PLC JB2 BOX.182IM1556ES7155-5AA01-0AB0,182A1 DQ6ES7522-1BL01-0AB0 POS2,182A2 DI/DQ6ES7523-1BL00-0AA0 POS3.24Vdc181.5/0Vdc181.4→1L+/1M·2L+/2M. FG181/1·2→197/0·183/0. CPU 본체와 JB2 인터페이스를 같은 장치로 병합하지 않음|공란|

대장 electrical_fgs 102~149,153,182는 후보범위50개다. 이 문서에서 그50페이지를 전부 시각/의미 검토한 것이 아니다. 실제 시각 확인은 위11페이지이며 그중 FG180B는 잘못된 기존 링크의 확인을 위한 범위 확장이다. FG105~115/117~133/135/137~143/145~147/149 등 나머지의 개별 배선·개정은 이번 확인 밖이다. 일부 페이지 텍스트를 검색용 추출했어도 의미검토/실제 footer 확인에 포함하지 않는다. 원격 I/O 채널 전수, 내장 진단, 승인 시공선/현장 케이블 전체 경로는 미확보다.

## 5. 알람·복구

### 5.1 이벤트 기억과 집계는 다른 층

live_index _7ev doc436 mod_err Event class io access error,doc441 prog_err programming error,doc762 rack_flt rack or station failure; 상수 doc299/300/301 ob_mod_err122/ob_prog_err121/ob_rack_flt86. OB 번호는 백업 색인값이며 현재 CPU 지원/동작 보증이 아니다.

0000 i/o_flt1 LAD434,0001 mod_err LAD439,0002 prog_err LAD444,0003 rack_flt LAD765는 각각 NID1,Contact33→SCoil28: W35 rail→33.in;W31 UID29/RID1 ON→33.operand;W34 33.out→28.in;W32 UID30/RID2→28.operand. 선언0043/0044/0045/0046은 Global Bool Memory AO256/259/260/258으로 각각 I/O FLT M32.0 / Module Access FLT M32.3 / Prog FAULT M32.4 / Rack FAULT M32.2. ON은 M0.0. 단순 Coil이 아니라 SCoil이며 이벤트 블록 호출과 기억을 분리한다. OB Fault M32.1(0542 0686 RID130)의 Set 발생원은 이번 직접검토에서 미확보다.

### 5.2 0542 집계·Reset

0542 LAD1994 allarms index3,원본 NID16.0686 RID129~133 Global Memory AO256~260=5원인.0684 RID134 Global Bool AO139 BAD10=DB3.X17.3 PLC_DIAGNOSTIC_FAULT;RID24 AO48 BAD15=DB2.X6.0 RESET_ALLARM.

ON UID1235 W1250→Contact1269. W1270 이후 원인Contact1271/1273/1275/1277/1279에 병렬 공급, W1251~1255는 각 원인 UID1236~1240. W1272/1274/1276/1278/1280→OR1211.in1~5,W1256 OR.out→SCoil1217,W1258 UID1241→operand. 따라서 ON AND 5원인 OR가 집계 Set의 대표 식이다. 전용 지연 타이머는 이 선택 네트워크에 없다.

Reset 가지는 ON 뒤 Contact1281 RESET_ALLARM UID1242 W1259, W1282→Contact1283 집계 UID1243 W1260, W1284→6개 RCoil1223/1225/1227/1229/1231/1233. W1261~1266은 집계 UID1244 및 5원인 UID1245~1249. 즉 ON AND RESET_ALLARM AND 집계조건에서 집계와 기억 비트를 지운다. 모든 원인 제거를 확인하는 별도 NOT 조건은 이 Reset 가지에 없다. 사건 재발·여러 Writer·실제 OB 우선순위·스캔 최종값/경보 출력 소비는 현재 CPU 미검증. HMI ACK만으로 하드웨어 복구했다고 쓰지 않는다.

SYS-ALARM의 경보 Word·출력/허가 소비는 공통 기능 소유이고 각 계측 OFR는 해당 센서 소유다. TM Error 핀의 미결속을 PLC_DIAGNOSTIC_FAULT에 자동 결속시키지 않는다.

## 6. 증상 관찰·자료 수집

현장 조작법/전압 인가/강제 I/O/CPU 재기동/보호값 변경을 제안하거나 수행하지 않는다. 아래는 승인된 담당자가 제공할 읽기전용 관찰자료의 비교 설계다.

|증상|동시 기록할 자료|비교·배제 경계|
|---|---|---|
|HMI만 값이 멈춤|발생시각·화면·StatusPLC·raw IW/PIW와DB13·호출조건·프로젝트 판본|HMI 드라이버 상태,호출 비활성,원시 실제 변화,미러 변경을 분리;통신고장 단정 금지|
|raw와처리bit 반대|I7.5/I7.6,DB13.X7.5/X7.6,0397의 Word/NOT Writer,현재 도면|설계된 NOT와 배선·극성 문제 구분;입력 강제금지|
|온도가 -9999/0 또는이상|동일시각 IW256·IW256:P·DB13.W24·DB1.W116·DB4계수·OFR·IN0|범위/형변환/비활성·변환기 교정과 실제고온을 구분;백업 계수를 현장 설정으로 적용금지|
|Q미러 ON이나 기계무응답|실제Q 명령·DB14·모듈진단·해당모터응답·회로판본|0401은Q 관찰미러일뿐 부하전원/접점/운동증거아님|
|엔코더카운트 정지|DB15/19 판본·SwGate/CountValue·EM_OK·접근가능한모듈진단·설정기록|RefId없는 ErrorID의 저장주소 발명금지;펄스·영점·교정 시험미실행|
|집계알람 Reset뒤재발|OB 발생시각/진단버퍼 제공본·M32.0~4·DB3.X17.3·Reset요청/내부신호|기억지움과원인수리 구분;재기동/모듈탈착을 복구방법으로지정금지|

관찰 기록에는 관찰자·시각/시간대·물리위치·원시형식/단위·프로젝트/CPU 식별 출처·비교원본·원인배제 결과·승인조치·복구증거를 각각 둔다. 이번 작업은 운영 기록을 작성하거나 가져오지 않았다.

## 7. 완료·누락·인계

|영역/상태|판정|
|---|---|
|설비·자료|적용.고유ID·고정판본·도면과백업구분.현재CPU/실물미확보|
|IO/HMI|적용.대표선언/Word/Bool/Peripherie/미러·설정대조.전체Writer/위젯미확보|
|제어|적용.대표호출/ENO/형변환/엔코더핀.전체스캔/모든환산분기미검토|
|전기|적용/일부미확보.11실제페이지렌더,나머지범위명시|
|알람/복구|적용.이벤트SCoil·집계Reset대조.OB Fault 발생원·실제복구미확보|
|증상관찰|적용.읽기전용수집설계;현장시험없음|
|documentation|complete_with_gaps /부모독립검토전|
|static_review|대표핵심자체검토·해시·MD검사,전체논리검증아님|
|ui_records / publication|not_run /not_published;실제UI·저장복원·배포범위아님|
|tia_compile / live_cpu / field_recovery|모두not_performed|

BC01 네 기능(도면·래더 비교,선택복원,전후기록비교,보고서/PDF)의 SYS-PLC-IO 구현·저장/재읽기/재열기·모바일/PC 기능은 이번 문서조사에서 검증하지 않았다. 원본 렌더PNG는 전기근거확인이고 제품 보고서기능 시험이 아니다. 기존메모/미지필드/다른설비/운영기록/초안 보존.

다음 독립 검토는 대표 진단 NID16와 엔코더 NID50/49 문맥·DB별 선언, FG103 모듈 주문번호의 도상/하단 차이, FG182 실제PDF185를 우선한다. 현재 CPU 프로젝트 하드웨어 내보내기(MLFB/슬롯/주소/펌웨어/장치명),승인 네트워크 도면·진단버퍼·TM 파라미터/결속된 출력정보,현장변경도면/교정기록이 있어야 남은 현행성 항목을 확정할 수 있다. 새 자료없이실물보류반복조사하지 않는다.

## 실제 작업 단계 시각(UTC)

- 2026-10-11 11:56:09 착수,배치12지시/범위읽기.
- 11:56:14~11:56:43 표준·원본판본·대장·기존공유초안·색인검토.
- 11:56:51~11:57:19 진단/환산/엔코더대표원본탐색,1차PDF렌더및시각검토.
- 11:57:29~11:58:01 실제PDF185확인,진단집계·Reset원본대조;부모에게중간결과보고.
- 11:58:08~11:59:13 Word/PIW·선형화·DB결속·TM대표핀대조,잘못된FG182 추출명칭을실제FG180B로바로잡음.
- 11:59:27~11:59:35 디지털입력/예비/출력추가렌더및실제개정란확인.
- 12:03:23 초안 본문 작성 완료. 12:04:36 첫 자체 검사14항목 통과. 12:04:50 FG103 상세 확대 렌더로 도상/하단 주문번호 차이를 재확인했다. 최종 선정 SHA/Gitblob·원본/중지5보존·자체 검사 시각은 아래 JSON과 완료란에 기록한다. 추정 시간을 실제 작업 시간으로 쓰지 않는다.

## 선정 원본 SHA256·고정 Git blob 전체 목록

선정 파일의 바이트 동일성 수는 전체 의미검토 수가 아니다. 선언은 위에 명시한 RID/NID/UID 분기만 대조했다. 중지5자산은 해시보존 대상만이며 실행·논리해석 대상이 아니다. 모든 경로는 고정 저장소 상대경로.

|원본 경로|SHA256|고정 Git blob|바이트 일치|
|---|---|---|---|
|`all-in-one/assets/program-model-data.js`|`52f8199371e3399b7c0d44ab5469f0472aced79d56bbef2887f7625f5d2aff0f`|`38f34b0caa380a16ccad6f6f1e234a2fdf23f327`|일치|
|`all-in-one/assets/simulator-workspace.js`|`3a6dfc618ff7e7b238f2671dc85d65704f33093a18eac879d86081d92c31e8bc`|`97c2c831c77a9699fff0e0960b3bc1b7d93d45b3`|일치|
|`all-in-one/assets/virtual-plc.js`|`5f1876052dc0067b1f010af0dfc941946e37003167481731293615d9c1c36dbc`|`0bd9eceb54365a91214a37c5601b5067c39a3f75`|일치|
|`all-in-one/devices/SYS-PLC-IO.html`|`c95043fe3de737703a16824c44e3b1d109d49941c7202c8e7154a9c6c1f43a06`|`1ba92115d48d6b52a062a65d11f650610cb0f277`|일치|
|`all-in-one/registers/program-model.json`|`6203479c086b15bada12ac9d7e37db9280234ec26f1ea6091d7211dc09a577c5`|`9860b10f008d3a5ae714be50d77b703dfec32f3a`|일치|
|`all-in-one/registers/simulator-freeze.json`|`bb93c1994effc5609939ba566b7802ce7ed55154a7310f02379b308ac2c8c835`|`808ffac14dbd1b4a7d797fa6cd0d647635d90b47`|일치|
|`all-in-one/registers/virtual-plc-test-results.json`|`a6b389f797f9a8b5ffe6928b8420f55c4cc459a327b0b48d716079d2eca6dd64`|`757dd50e45184568facb8ff62900b39d3ce848d1`|일치|
|`all-in-one/sources/Electrical_Rev2.pdf`|`5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6`|`f610fd7c7ce14ae951b00cff57b969259bfb389d`|일치|
|`all-in-one/sources/GME_20250506.zap18`|`00c79b6d986e68298f65b172c1807115bc5d9e450a74fcc989d0796d8d8a4ea8`|`211c4f604627a32f82a1124c2a9872c2fcf00865`|일치|
|`all-in-one/sources/PEData.plf`|`647de7ea123daced41c27bec8f81aeb93c712cac714d4754d7da5c528abb016a`|`65605ff8910f920109da731604aa5dc8d83fc956`|일치|
|`all-in-one/sources/block_summary.json`|`68253f9366908244a27ed461c66d465da7ec1723571f27deaa9a6f81a542de63`|`15b570a011645023dbfca2d5332a9e0ae3b0a7b6`|일치|
|`all-in-one/sources/decoded-original/0000-FlgNet.xml`|`35711962149caae7cd4fb8498301d9fef9acddbf816d496300c0db08063cd2ae`|`9ee3e46ddd40a3258195e88563f73789438e1175`|일치|
|`all-in-one/sources/decoded-original/0001-FlgNet.xml`|`35711962149caae7cd4fb8498301d9fef9acddbf816d496300c0db08063cd2ae`|`9ee3e46ddd40a3258195e88563f73789438e1175`|일치|
|`all-in-one/sources/decoded-original/0002-FlgNet.xml`|`35711962149caae7cd4fb8498301d9fef9acddbf816d496300c0db08063cd2ae`|`9ee3e46ddd40a3258195e88563f73789438e1175`|일치|
|`all-in-one/sources/decoded-original/0003-FlgNet.xml`|`a1bfce0bdd5b227f391b5b51933216c63cf4357747f954abbcc49522f81e5d1d`|`c719d8cc606f98a6f694b6c465e74a7289fc1f91`|일치|
|`all-in-one/sources/decoded-original/0014-FlgNet.xml`|`2e814adbaac6bab99bc668bfdab74f0fc90576324d0b88728951683869cfac30`|`4d164b074fcc13a8f97da9e24382cc169ef29555`|일치|
|`all-in-one/sources/decoded-original/0030-FlgNet.xml`|`9252c9da764993de1edb8b2e44c46d6e9f9d4b6118e751a0dbeaa9ffd8ea721b`|`e74c70b751acdcdbc7a8b3b0c98aa773c2107cab`|일치|
|`all-in-one/sources/decoded-original/0043-IdentXmlPart.xml`|`c71c75f0b13763a806cc984f933fd0ec785f77a0fe6915267ebf7648189ddb33`|`f20ba4e4479e42f8496e637a0e755814fe1dac56`|일치|
|`all-in-one/sources/decoded-original/0044-IdentXmlPart.xml`|`80ed7b8be0e4988ac52ac84cbc7e68a29a15755c821d9b0452247d9f362638c2`|`eb44635cb72b77f04dea4319e47d96ee68c09a58`|일치|
|`all-in-one/sources/decoded-original/0045-IdentXmlPart.xml`|`334d3c31a4dc1084cd9e6d870058e32f5e96c17ece69e5fc52038965416a1c79`|`d455986215307b725280a4ff3beea011d8d37e25`|일치|
|`all-in-one/sources/decoded-original/0046-IdentXmlPart.xml`|`1df29e9d0382743dcf42b287223f63f9880740616318769d8e23fdb8a68a97b1`|`8c7426049cdd9f9f00d96c6298af443d5a336e38`|일치|
|`all-in-one/sources/decoded-original/0049-IdentXmlPart.xml`|`d4c49fa00735537ee8cce4baba526b0027e4fe25343074e83de5719cafd1bacc`|`50478b19d7a3d4af551c914f181fb25b6f809331`|일치|
|`all-in-one/sources/decoded-original/0064-IdentXmlPart.xml`|`ce6afc4f7ca0a8059c2e3cab25d202f0faaa49a3bc6a2e9ee238964a76e9fc9d`|`300d74239868f4f4595d4d5bbb848b4b58bbae76`|일치|
|`all-in-one/sources/decoded-original/0291-FlgNet.xml`|`fe0b92f074eba25148ce34084649af3d968962558d652727f1eea19f3e3c2550`|`1418fb2ed172c6df694a5eb8bf2dffd0b177653b`|일치|
|`all-in-one/sources/decoded-original/0397-FlgNet.xml`|`bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834`|`4ab8370493c4e28fc1eabeeebe2743d27f0c4021`|일치|
|`all-in-one/sources/decoded-original/0398-FlgNet.xml`|`4f092b18df4e44af98fd44e173f48dad213a4e80b71f46b0a5e8a700f5b0a747`|`67ebb54daa55093487ea7e780f23ae2cf193c397`|일치|
|`all-in-one/sources/decoded-original/0401-FlgNet.xml`|`60171c213e666de544077b7e4b497675813f7c0e75df85a3e76ab1def49b04ae`|`aadefbd35d305dd4a1146bf383b988a903802bf4`|일치|
|`all-in-one/sources/decoded-original/0481-FlgNet.xml`|`190354dc7d59686f17368b7186bbc782a67ccef603f65a13f10e631446ee5d7d`|`5f275350dad39b1eeccb61f10072768deb938461`|일치|
|`all-in-one/sources/decoded-original/0506-FlgNet.xml`|`71b9ac920eb891ec8965506c40ae3f1d050a2f8a899f79f6afdc81f669717fbe`|`8e26b2cc02f4e38863022d2fb8da0f7322e2125f`|일치|
|`all-in-one/sources/decoded-original/0510-FlgNet.xml`|`0e755f251ab92f2b1904be6812b4995ba04285f99de068b8bc794d31c1cee0dd`|`ca06d39dc0bf873f7ece4ff984b9d615a95617e8`|일치|
|`all-in-one/sources/decoded-original/0542-FlgNet.xml`|`49d01523b89e14a4aae3120853c397c2b73725f1948493ec48f80c1f4ff0890f`|`715d2eb45b5ff8bb9171306903050180ad5220a3`|일치|
|`all-in-one/sources/decoded-original/0599-IdentXmlPart.xml`|`32a693fe12134febbd9f5c7da10c3469ef4d5b164ab8b6bd9ea3867c358936c1`|`493de77fc827d8f14192ced05d82df3a062f7965`|일치|
|`all-in-one/sources/decoded-original/0611-IdentXmlPart.xml`|`0d583915a261703954da22c176ba9f81338ad13ea2810e7cd5f7de8aa1bfa089`|`bad6b16fb32a32d47d882f48754994887457872b`|일치|
|`all-in-one/sources/decoded-original/0612-IdentXmlPart.xml`|`95b545d4964d371ebfc107894ea90b8b1d0d7ab5d3a70e643f8ce539063c0f38`|`7cc782d33d07ef225c2104f3e7c9fbd31f7c7467`|일치|
|`all-in-one/sources/decoded-original/0627-IdentXmlPart.xml`|`08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb`|`61ebc0abbb2ca160e11e1da400a3f14a397d8bc5`|일치|
|`all-in-one/sources/decoded-original/0628-IdentXmlPart.xml`|`9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd`|`170ca5c72599edc7ea7eefe651c3680ce325e76a`|일치|
|`all-in-one/sources/decoded-original/0629-IdentXmlPart.xml`|`67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972`|`058129bb01e27f7a6a0d0293f332d745e5bab74e`|일치|
|`all-in-one/sources/decoded-original/0632-IdentXmlPart.xml`|`fd162c603476c2cac899010cee7a8ee382b6092c115135e3ac1007ae71c544e9`|`600935fa8d394c0d247ea20040d5dfff4f05b500`|일치|
|`all-in-one/sources/decoded-original/0633-IdentXmlPart.xml`|`9e00aa275fa1b4e488b73983b309c6b73dcf4f3dd9be5dec13e9975d68f3c0fc`|`a1ab5ee12addbc92d04c9950d4437e2b564d6b5c`|일치|
|`all-in-one/sources/decoded-original/0672-IdentXmlPart.xml`|`6bfc2ba142d6270c39eb1f13b2886204865af6d46eadc5f410c26981b8da9222`|`2f2790dab4bb2357733112220e0acc41edb6feb6`|일치|
|`all-in-one/sources/decoded-original/0673-IdentXmlPart.xml`|`450ef74e2d2fb65dfbb5f6bad9e28ccacf6bf0caf64327a0e20aff84d6e40f58`|`1957bff7dd1beffcb6e2a40d6a541c1751753548`|일치|
|`all-in-one/sources/decoded-original/0674-IdentXmlPart.xml`|`4770702f519bacda69202bb2f7733d983074bda90964360c238f990d9d08fd84`|`f210593944547b63eab10c667348711413600aab`|일치|
|`all-in-one/sources/decoded-original/0676-IdentXmlPart.xml`|`c58427c5b0ac6c11cdb52e4c6d0461c7b191fae81ccace191048e9f175fcec59`|`1ed67265f69796a4e659f9438e551068037f33a4`|일치|
|`all-in-one/sources/decoded-original/0678-IdentXmlPart.xml`|`51e637e0b9713c028810f2a717b5c3804a3a26c2f1be7e332a4d6bf277bfc382`|`7fafb2297bcdf739bf1d1dd68cebc0d74f2a40cc`|일치|
|`all-in-one/sources/decoded-original/0679-IdentXmlPart.xml`|`d0fcb93e188c8ae2ae0c0423f0b78b129bf3c168e33a6855262d34b8682b9b56`|`e8d8a014609871082bf5cfca0f9ab9b78136e920`|일치|
|`all-in-one/sources/decoded-original/0680-IdentXmlPart.xml`|`fd551ad5d47bbd66c6bcdcc1949aaddf68cc086a3ddf6fb337adc767954c2b95`|`c9049ced1eaed72c5e251a88601d46ddec8c3e50`|일치|
|`all-in-one/sources/decoded-original/0682-IdentXmlPart.xml`|`25c7aeb1bfa29c178eaa396db33d4eb6d2d29b9a3f2eb965fa61fae8ce7f1092`|`61182411e912941161eccf4e90c1f174e5379f0a`|일치|
|`all-in-one/sources/decoded-original/0684-IdentXmlPart.xml`|`6e9b3f173184adcddca503e81e2649022734b6ea3639c1d5ddaf0a08bac00208`|`d67b98b5d5516e0330aae5cfdbee41a3e09206e1`|일치|
|`all-in-one/sources/decoded-original/0686-IdentXmlPart.xml`|`b450d8ff22f0fffd7a214b2a696af28a03a27834ebf862bfaa822dc9bfb3c8d4`|`8c152d926692a8e15973c980e08e338d29411814`|일치|
|`all-in-one/sources/decoded-original/0688-IdentXmlPart.xml`|`ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda`|`463585759f1ecd94f32362b4fefb000a152f5773`|일치|
|`all-in-one/sources/decoded-original/0692-IdentXmlPart.xml`|`bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037`|`737785d03b5fad43c5b4d451955726d800edb1c0`|일치|
|`all-in-one/sources/decoded-original/network-map.json`|`c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60`|`424430b6b953e43138e5d0a18ca40c949e21cfa1`|일치|
|`all-in-one/sources/hmi-windows.csv`|`15f8d69b5c43d4fdbe550f9cd2717f855fea877ed8146973054cb6dbcaa9892e`|`8401dcfe5ba3e7e244eea0f501bb84a2e387da39`|일치|
|`all-in-one/sources/hmi_plc_tags.csv`|`a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404`|`cf4c0650e7c7baac350dcb89909b808435704880`|일치|
|`all-in-one/sources/live_index.json`|`14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1`|`e35ccea1f841349c632666c29954b7bcd4f5839e`|일치|
|`all-in-one/sources/source-manifest.json`|`5af6e85994536897fd92f75972534a691e6eb0f067aafe07679c0788fd84e5bf`|`38cf407491d52dc6128cf94ca8a4bddee350de6d`|일치|
|`docs/equipment-standard/INVENTORY.json`|`720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc`|`587c3748ad9224718f95ba06463fee913dae231d`|일치|

## 자체검사 실제 결과

2026-10-11T12:05:08.953229+00:00 UTC, 자체 XML/해시/문서 검사 verify.py 종료0, 14항목 passed. 선정 57파일 SHA256 및 고정 Git blob 일치, sources/ 전체 712파일 바이트 보존 일치, 중지5자산 freeze 해시 일치, 원본 Git 변경0. 전체 보존 수와 14개 선택 FlgNet의 대표 의미검토를 구분한다. 실제 시각확인 PDF11페이지; 검색용 추가렌더/텍스트는 그수에 포함하지 않았다. 상세 self-check.json/source-hashes.json/all-source-preservation.json은 extracts/SYS-PLC-IO/에 보존했다. 원본 테스트/생성기/시뮬레이터·현장 실행 없음. 부모의 독립검토와 사용자전송은 별도다.
