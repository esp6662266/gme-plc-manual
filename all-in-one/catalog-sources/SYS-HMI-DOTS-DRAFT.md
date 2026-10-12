# SYS-HMI — HMI·통신·가공 상태 7영역 자체 조사 초안

문서 범위 완료·누락 포함. 원본 HMI 실행, 화면 이벤트 검증, 현재 통신 정상, 매뉴얼 통합·게시, TIA·현재 CPU·현장 복구 완료가 아니다.

## 핵심 확인·상충·누락·공유 근거

- 실제 CSV 데이터 782행, 이름/내부 ID 각782개, 화면 목록17행을 독립 계수했다. 782행 전체 계수·주소 구문 검사는 했지만 782개 모두의 제어 의미·실제 위젯을 검토한 것은 아니다.
- 동일 주소2쌍: `I_W20`과 `O_W20` 모두 DB14,W20, `I_W22`와 `O_W22` 모두 DB14,W22. 태그 접두사 I/O로 입력/출력을 결정하지 않는다. 원문 수정 없이 상충으로 보존한다.
- `0401-FlgNet.xml`은 Q Word를 읽어 DB14 Output에 쓰는 미러다. HMI 명령을 물리 Q에 쓰는 네트워크가 아니다. startup의 live_index document401과 파일0401은 서로 다른 식별자다.
- ResetAlarms 설정 DB2,X13.4는 `Flag.Reset_Allarms_HMI`; 내부 `Flag.RESET_ALLARM` DB2.DBX6.0과 별개다. `0158`에서 입력/요청 OR → 내부 SCoil, HMI 요청 RCoil 및 TOF 경로를 직접 확인했다.
- `AbilitaAuto` DB2,X7.3는 `Flag.Auto_ON1`, `AbilitaMaintenance` DB2,X7.5는 `Flag.Maintenance_ON` 주소와 맞는다. CSV 이름의 “허가”를 전체 안전 허가·실제 클릭 Writer로 해석하지 않는다.
- `StatusPLC`의 `$SYS$Status`는 드라이버 상태용 주소 문자열이다. PLC 물리 주소나 현재 통신 정상 증거가 아니다.
- 공유 근거: [BF01](BF01-DOTS-DRAFT.md), [BF02](BF02-DOTS-DRAFT.md), [LD01](LD01-DOTS-DRAFT.md)의 공통 입력/출력 미러·HMI 미결속 경계를 참고했다. 0355 상태 함수, 0401 출력 미러, 0158 Reset, 0162 요청 소비, 0357 호출 경계는 이번에 원본 Part/Wire와 선언을 직접 대조했다. [CR01](CR01-DOTS-DRAFT.md)의 공통 운전반 전기 근거 중 FG17은 이번에도 실제 렌더했다. 각 설비 전체 논리나 하위부품 완료를 복제하지 않는다.

## 1. 설비·자료 기준

- catalog_id SYS-HMI, software, 공통 시스템, parent 없음, phase2, INVENTORY catalog[38], equipment[239], 별칭 hmi_db. 단일 소프트웨어 기능 경계이며 PLC 전체나 HMI 물리 PC 본체를 동일 ID로 합치지 않는다.
- 고정 읽기전용 원본 `gme-research/source-mv06`, commit `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, v1.12.0. 이후 로컬 v1.16.0 기능/게시 상태를 검증하지 않았다. 로컬 2차133 통합 제외 유지.
- root AGENTS, 저장소 rollout 스킬, WORK-STANDARD, WORK-ITEM-TEMPLATE, INVENTORY, 버전/인계/공개상태/ACTIVE-WORK/EXPANSION 최신 머리말, 배치11 범위 및 overlap SYS-HMI 행을 읽었다. 모델·추론 런타임 증명 미확인.
- 이하 XML 약칭은 `all-in-one/sources/decoded-original/`; CSV는 `all-in-one/sources/`. CSV의 출처 표기는 dde.cfg 및 WindowsInfo.json이지만 원래 화면 이벤트/프로젝트 런타임을 열거나 실행하지 않았다. `registers/hmi-transfer.json`과 network-map은 파생 색인이다.
- 대표 의미 대조는 5개 FlgNet(0355/0357/0401/0158/0162)와 관련 선언의 선택 분기다. 전체 HMI 함수·원본 XML 전수 의미검토, 바이너리 프로젝트의 모든 Writer 분석을 주장하지 않는다.
- 수정 범위는 본 초안 및 `extracts/SYS-HMI/`뿐. 공통코드·버전·대장·배포·운영·원본·타 초안 변경 없음. 원본 build/test/generator, UI/시뮬레이터/PLC/현장 시험 없음. 보호값·SEJIN 변경 없음.

## 2. I/O·HMI

### 2.1 782 설정 대장 검산

`hmi_plc_tags.csv` 헤더 제외782행(물리 CSV 행2~783), 고유태그782, 고유내부ID782, Access Name은 모두 PLC. 분류: DB678, 물리주소문자열101(EW40/EB24/AB20/AW17), MX 메모리2, 드라이버상태1. 실제 통신 드라이버·IP·Rack/Slot·연결 상태는 이 계수에서 확인되지 않는다.

DB678행의 주소구문을 비트범위로 변환해 중첩17쌍을 확인했다. 그중 완전 동일 주소2쌍, 나머지15쌍은 DB13 Word와 포함 Bool의 범위 중첩이다. DB범위만의 정적 산술이며 물리접근/드라이버의 모든 별칭 중첩을 전수 판정한 것이 아니다. 전체 행은 원본 CSV 및 `extracts/SYS-HMI/tag-ledger.json`, 계수·중첩 전체 목록은 `csv-audit.json`에 보존했다.

|CSV 실제행|태그/내부ID|설정 주소|독립 대조·한계|
|---|---|---|---|
|3|FN01_Preathing_enable /00467|DB41,X50.0|0577 RID156 AO400 Bool, NID11 UID79;0576 HMI_DB RID155 TOD41 → PreheatingControl_Enabled. 이름 철자·기능표현 차이 보존; 클릭/화면 위치 미확정|
|7|RESET_PROD_COUNT /00463|DB41,X50.3|0577 RID213 AO403 Bool, NID13 UID67 read/96 Write; DB41.ResetCounter_PartialProduction. 누적 알고리즘은 SYS-COUNTERS 소유|
|73|AbilitaMaintenance /00409|DB2,X7.5|0604 RID3 AO61 Bool;0603 Flag RID2 TOD2 → Maintenance_ON. NID1 UID39/6 UID27 read. 시작 조건 전체 미검토|
|176/186|I_W20 /002FA, O_W20 /002F0|DB14,W20|같은 Word; 이름만으로 별개 입력/출력 취급 금지. 0401 해당 복사 아래 대조|
|177/187|I_W22 /002F9, O_W22 /002EF|DB14,W22|같은 Word; 두태그 실제 위젯·Reader/Writer 미확정|
|188|ResetAlarms /002E1|DB2,X13.4|0565 RID61 AO108 Bool;0564 Flag RID1 TOD2. 요청 소비와 내부 Reset 분리|
|189|StatusPLC /002DF|$SYS$Status|드라이버 상태 특수문자열; 현재값·상태값 의미/통신건전성 미확보|
|632|AbilitaAuto /000DB|DB2,X7.3|0577 RID4 AO59 Bool;0576 Flag RID3 TOD2 → Auto_ON1. 요청/상태 저장과 안전허가 전체를 구분|

내부ID와 행번호를 서로 바꾸지 않는다. 위 표는 대표 대조이며 CSV 이름을 PLC 심볼과 동의어로 일괄 병합하지 않는다. DB 주소가 맞아도 HMI의 읽기/쓰기권한·변경 이벤트·다운/업 동작·수치검증·사용자역할은 별도 미확정이다.

### 2.2 화면 목록17행

ALARM, ALARM_HIST, ALARM_RECENT, BOTTOM, CONFIG1, CONFIG2, CONFIG3, HOMEPAGE, PLC_RACK1, PLC_RACK2, POPUP LISTA PENNE, Popup_AutoCycle, RECIPES, SIN1_DECOATER, SIN2_LOAD_MATERIAL, TOP, TRENDS. CSV ID4/5/7~21, Parent ID 모두3. CONFIG3 설명은 Burner configuration page, PLC_RACK1은 PLC and IO status page, PLC_RACK2는 IM status page다. 목록17은 화면 존재 메타데이터이며 메뉴노출·화면간 이동·각위젯·알람 ACK·클릭 스크립트·현재값 갱신을 확인하지 않았다.

## 3. 제어 구조

### 3.1 가공 상태: 0355 HMI Standard Motors, NID1

0621 선언은 모두 **Local InterfaceAccess Bool**이다. RID16 Ingresso_run(UID24 Input), RID17 Risposta(UID28 Output Write), RID18/19/20/21/29 Allarme1~5(UID34/37/40/47/31 Input), RID22 Comulativo_allarmi(UID60 Output Write). Local AO0은 각각 인터페이스의 배치이며 이를 전역 DBX0.0으로 바꾸지 않는다.

- W21 Powerrail→Contact23.in; W22 ORef24/RID16→23.operand; W25 23.out→Coil27.in; W26 ORef28/RID17→27.operand. 이 함수에서 Risposta는 입력을 복사한 처리 Bool이며 별도 물리 센서를 만든 것이 아니다.
- 5접점 P33/36/39/46/30, W32/35/38/45/29 각각 입력 ORef→operand. W42/43/44/48/49가 OR Part41.in1~5로 들어간다. W57 OR.out→Coil59.in, W58 ORef60/RID22→59.operand. 누적표시 = 다섯 알람의 OR.
- 이 선택 함수에는 S/R·NOT·타이머가 없다. 가공 OR 표시가 원인알람의 발생/지연/유지/리셋 로직을 대체하지 않는다. 호출 전후 실제 스캔·UI 갱신은 미확정.

### 3.2 호출 경계: 0357 HMI 대표 호출

0357 CRef23/RID638 + CodeBlock22/RID1. 0623은 FCBlock `HMI Standard Motors`, TOD1;0624 BlockInterfaceInfo RID638/TORID1은 Bool 입력 Ingresso_run/Allarme1~5와 출력 Risposta/Comulativo_allarmi를 선언한다.

W21→CRef23.en. W24 입력 ORef25/RID772→Ingresso_run, W28/30/32/34/45가 Allarme1~5, W36 Risposta→ORef37/RID6, W40 Comulativo_allarmi→ORef41/RID773이다. 호출핀 경계는 확인했지만 network-map의 이 FlgNet inferred_original_nid는 null이고 resolved_operands는 비어 있다. 색인의 BC01 운전/고장 이름만으로 8개 데이터 ORef를 강제 결속하지 않는다. 0623에 NID1/UID22가 있어도 모든 데이터가 같은 문맥이라는 증명이 되지는 않는다. 함수 내부의 Local 선언과 호출자의 Global DB 주소 결속은 추가 확인 필요.

### 3.3 출력 미러: 0401 HMI Output NID1

0632는 Global SimpleAccess Word, SAD Output SAM=None. 0633은 GlobalAccess Word Write이며 BAD26;0064 Output RID26/TOD14가 DB14를 확정한다. 선택 분기:

|분기|읽기 선언/주소|Part·Wire|쓰기 선언/주소|
|---|---|---|---|
|첫 Word|0632 RID24 NID1 UID33 AO0 → QW0|W21 rail→Move22.en;W56 ORef33→22.in;W58 22.out1→ORef34|0633 RID27 UID34 AKWrite AO0 BAD26 → DB14.DBW0|
|후반 Word20|0632 RID46 UID53 AO160 → QW20|W83 ORef53→Move32.in;W84 32.out1→ORef54|0633 RID59 UID54 AKWrite AO160 → DB14.DBW20|
|후반 Word22|0632 RID48 UID89 AO176 → QW22|W87 ORef89→Move85.in;W88 85.out1→ORef90|0633 RID49 UID90 AKWrite AO176 → DB14.DBW22|

12개 Move Part 모두 DisableENO=true. 그래프에는 W57 Move22.eno→Move23.en 등의 ENO 연쇄가 실제 존재한다. DisableENO와 eno 핀 연결을 모두 보존하고 실제 실행/최종 Word 갱신을 정적으로 확정하지 않는다. QW는 출력 프로세스 이미지 Word이며 HMI 명령·현장 전압/부하 동작 피드백이 아니다. Word20/22의 같은주소 태그쌍은 이 출력미러를 읽을 수 있는 설정 후보일 뿐 실제 읽기 이벤트 증거가 아니다.

### 3.4 운전 요청 소비 대표: 0162 auto start motors NID1

0575 ON RID1 Global Bool Memory AO0 → M0.0, UID69. 0577 Auto_ON1 RID4 Global Bool AO59/BAD3 → DB2.DBX7.3 UID70/74. Data.Tempo_presetting RID7 Global Int AO768/BAD6,0576 Data TOD1 → DB1.DBW96, UID71 read/73·76 Write. 0578 RID8 Int1 UID72, RID10 Int0 UID75.

W94→P88 ContactON.in, W77 ORef69→operand;W89 P88.out가 P90과 P92 입력으로 분기. P90은 Auto_ON1 접점(W78)이고 W91→Add59.en;W80/81 Tempo/Int1→in1/in2, W82 out→동일 Tempo. P92는 Auto_ON1 operand **Negated**(W83), W93→Move66.en, W85 Int0→in, W86 out1→Tempo. ON 참인 호출에서 Auto_ON1에 따른 Int 증가 또는0 쓰기의 정적 경로다. 호출주기 미확정이므로 1초당 증가나 실제 대기시간을 추정하지 않는다. Auto_ON1 하나를 전체 공정 허가·모터출력·안전완료로 표현하지 않는다. Maintenance_ON 전이/자동기동 전체는 SYS-AUTO 경계이며 이번 선택분기 밖이다.

## 4. 전기 전달 경로

SYS-HMI는 소프트웨어 기능이므로 독립 모터전원/접촉기 회로는 비해당. HMI PC/통신 케이블·IP·스위치·PLC 포트까지 양 끝점은 근거 미확보이며 StatusPLC 문자열로 채우지 않는다. 아래는 **공통 Reset 입력과 출력의 관련 끝점**이다.

`all-in-one/sources/Electrical_Rev2.pdf`, 실제 PDF18, footer FG17, ALARMS CIRCUIT, DATA27.05.2024, Rev2 17.03.2025, TOT262를 렌더 시각 확인했다. 렌더 `extracts/SYS-HMI/Electrical_Rev2-p18.png`. FG≠PDF라고 구별한다.

- +24Vdc10.7 → X20:2013 → Reset 버튼17SB2(blue) 접점13–14 → X20:2015 → E19.7, 다음 FG135/7. 옆17SB1 yellow는 침묵 요청 E19.6/X20:2014이며 Reset 입력과 구분한다.
- 관련 출력 A7.4→17KA1 A1, A2→-0Vdc10.6, A7.5→17KA2 A1/A2→동일0V. 출력측 참조 FG143/1. 본문 PLC Q7.4/Q7.5와 주소 대조는 가능하지만 HMI 자체 하드웨어 출력으로 취급하지 않는다.
- A7.6→X1:41(도면5x20 2A IST.)→17HL2→X1:43→0V, A7.7→X1:42→17HL1→X1:43→0V도 표시된다. 이 램프가 HMI 위젯이라는 뜻은 아니다.
- 하단17KA 접점표의1/5/9 등은 다른 회로 참조표다. 이 페이지의 A1/A2 코일에서 부하접점5–9/1–9를 임의 구성하지 않는다. 실제 릴레이 부하/현행 설치/보호값·정상극성·통신 경로는 별도다. FG135/143 상세와 전체 후단은 공유 CR01/알람 조사로 연결하며 본 초안에서 전체 새 검토로 세지 않는다.

## 5. 알람·복구

### 5.1 HMI 요청과 내부 Reset: 0158 allarm manager NID9

0564 Flag RID1 TOD2 및 Inputs RID56 TOD13. 0565 RID57 Inputs.Reset_allarmi Bool AO159→DB13.DBX19.7 UID24; RID61 Flag.Reset_Allarms_HMI Bool AO108→DB2.DBX13.4 UID27 read/UID43 Write; RID2 Flag.RESET_ALLARM Bool AO48→DB2.DBX6.0 UID37 Write. 전기 E19.7와 내부 DB13 전달은 CR01/LD01의0397 Word공통 경로 참조이며 물리 입력과 내부 비트를 동일 객체로 합치지 않는다.

- W21 rail→P23/P26.in;W22 ORef24/RID57→P23.operand, W25 ORef27/RID61→P26.operand.
- W29 P23.out→OR28.in1, W30 P26.out→OR28.in2. W38 OR28.out→SCoil33.in + RCoil40.in + LRef64.IN + LRef73.IN.
- W36 ORef37/RID2→SCoil33.operand: 내부 RESET_ALLARM Set. W42 ORef43/RID61→RCoil40.operand: HMI Reset 요청 Reset. 순간 클릭이 있었다거나 유일 Writer임을 증명하는 것은 아니다.
- 0568 Instruction RID77는 TOF, NID9 UID64/73 AKCall, ENENO=false. 0569 Instance RID78/UID72 DB36와 RID84/UID74 DB37. 0566 Literal RID79 Time T#3s/V3000 UID70/75, W68/78→두 PT.
- W67 LRef64.Q→Coil48.in, W62 ORef63/RID76→operand;0567 `103A7` Global Bool Output AO60 = Q7.4. W77 LRef73.Q→Coil60.in, W51 ORef55/RID74→operand;0567 Reset_Inverter AO61 = Q7.5. ET는 W69/79의 RefId 없는 ORef71/76 끝점이며 사용처 확정 안 함.

TOF T#3s는 원본 정적 상수이며 현장 리셋시간 권고가 아니다. 내부 RESET_ALLARM은 다른 네트워크의 Reset Writer(0565 NID4 UID246)도 있으므로 이 Set만으로 영구유지/해제완료를 단정하지 않는다. 같은 네트워크의 침묵요청/Stop_Horn 병렬 가지는 존재하나 전 원인·ACK·히스토리 유지·Reset 우선순위 전체는 SYS-ALARM 별도 분석 범위다.

### 5.2 복구 판단 경계

HMI 요청비트의 소거, 내부 Reset Set, TOF 출력, 인버터/원인알람 해제, 실제 장치복구, 재기동은 서로 다른 관찰이다. CSV/정적 Reset 경로만으로 알람없음·재기동 안전·통신복구를 표시하지 않는다. 화면 ALARM/ALARM_HIST/ALARM_RECENT의 ACK 이벤트와 이 PLC Reset의 관계는 미확정이다.

## 6. 증상 관찰·수리 기록 설계

아래는 읽기전용 조사로 만들 수 있는 관찰 항목이며 조작/시험 지시나 수행 기록이 아니다. 현장 수집은 별도 승인·안전절차와 함께 실시해야 한다.

|증상|구분하여 수집할 증거|비교·배제 기준|현재 상태|
|---|---|---|---|
|전체 화면 값이 고정됨|관찰 시각/시간대, 화면명, 표시값/품질/갱신시각, 드라이버 상태값과 로그, PLC 프로젝트 식별|$SYS$Status의 설정 존재와 실제 정상통신 분리; 일부/전부 태그·다른 연결의 범위를 비교|현행 로그·상태정의 미확보|
|I_W20/O_W20가 같은 값|실제 두 위젯 식별자, 바인딩/권한, 읽기 로그|CSV 두태그는 같은 DB14W20이므로 이름만으로 입출력 불일치 원인 확정 금지|위젯/이벤트 미확보|
|운전중인데 표시가 다름|물리 입력, DB13 처리 입력, 호출의 Ingresso_run, Local Risposta, 호출 출력, 위젯 값을 같은 시각 기준으로 기록|0355 복사/OR,0357 미결속,현재호출/순서/화면갱신을 단계별 분리|현재값·실물 미확인|
|Reset 버튼 반응이 없음|위젯 클릭 이벤트/권한/실제 쓰기 로그, DB2X13.4,DB2X6.0,DB13X19.7,Q7.4/7.5,원인알람 상태|요청 소거와 원인 소멸 분리;0158 및 원인 소유 로직과 비교|버튼 Writer·현장복구 미확정|
|자동 요청 후 기동 안 됨|Auto_ON1,ON,Tempo_presetting와 시간기준,안전허가·모드·출력/피드백|0162는 선택 소비 경로이며 전체 자동 시퀀스/허가를 대표하지 않음|추가 SYS-AUTO/현행자료 필요|

기록 필드: 관찰자, UTC/현지시각, 장치/화면/태그/주소, 값·형식·단위·품질, 수집경로, 프로젝트 버전, 비교원본, 배제결과, 승인된 조치, 후속복구 근거. 0과 빈칸·미확인 분리. 사용자 운영 기록·사진·인증정보를 본 초안에 복사하지 않았다.

## 7. 완료·누락·다음 자료

|영역|상태|경계|
|---|---|---|
|설비·자료 기준|적용|SYS-HMI 한 ID·고정 버전·소프트웨어 소유 유지|
|I/O·HMI|적용·누락 포함|782 계수/주소검산,대표 선언 결속. 실제 화면 이벤트·통신 미확정|
|제어|적용·대표 범위|5 FlgNet 선택 의미대조. 전 네트워크·전 Writer·현재 실행 검증 아님|
|전기끝점|관련경계 적용/고유PC회로 근거 미확보|FG17 렌더. HMI 네트워크 케이블·포트·현장 미확정|
|알람·복구|적용·대표 범위|Reset 요청→내부 신호/TOF, ACK/원인전체/현장복구 미확정|
|증상관찰|설계됨|실제 관찰·수리·복구 미수행|
|완료기준|complete_with_gaps|문서 초안만. 하위장치·SYS다른ID 완료 상속 없음|

- documentation: complete_with_gaps. static_review: selected XML/CSV/PDF self_checked. 독립 검토·부모 통합은 별도.
- ui_records / publication / tia_compile / live_cpu / field_recovery: not_performed. BC01 등 기존 회귀, UI 저장/복원/재열기, PDF 보고서 생성, 패키지·배포를 하지 않았다.
- 네 기능(도면·래더 비교/백업·선택복원/전후비교/관찰 보고서)은 요구·연결 자료에 그치며 이 작업에서 구현/검증하지 않았다. 기존 note/repair_observation·미지필드·초안·저장키 변경 없음.
- 우선 필요한 자료: 원본 HMI 프로젝트의 위젯·이벤트·액세스권한·드라이버 연결설정 및 버전, 현재 PLC DB 레이아웃/호출순서/실행 프로젝트, 허용된 읽기로그/동시각 상태, HMI-PC↔스위치↔PLC 포트/케이블 승인도. 확보 전 UI 클릭시험·현장 Reset을 대신 수행하지 않는다.
- 다음 작업 한 가지: 원본 이벤트 내보내기가 확보되면 ResetAlarms 위젯→쓰기 이벤트→DB2X13.4 경로부터 독립 결속 검토. 새 자료 없이 동일한 현장보류 검색을 반복하지 않는다.

## 실제 작업 시각·자체검사

모두 UTC 실제 도구시각: 2026-10-11 11:45:02 배치지시/범위 읽기,11:45:23 CSV782/화면17 최초계수,11:46:31 FG17/PDF18 렌더,11:46:40 렌더시각확인,11:47:54 주소중첩17쌍/선정33파일 첫 해시검사,11:48:28 대표 호출·선언 추가 후 선정37파일 전부 고정 Gitblob 일치. 종료·검사시각은 self-check.json 및 아래 결과에 기록한다. 추정 소요시간을 실행시각으로 쓰지 않는다.

## 선정 원본 SHA256 / 고정 Git blob 전체 목록

37개 해시는 보존·파일동일성 검사 수이며 37파일 전체 의미검토 수가 아니다. 중지5자산은 해시만 대조했으며 실행/내용해석 대상이 아니다. 목록의 선택 선언파일은 필요한 RID/NID 분기만 검토했다. 모든 경로는 고정 저장소 상대경로다.

|원본 경로|SHA256|고정 Git blob|바이트 일치|
|---|---|---|---|
| `all-in-one/assets/program-model-data.js` | `52f8199371e3399b7c0d44ab5469f0472aced79d56bbef2887f7625f5d2aff0f` | `38f34b0caa380a16ccad6f6f1e234a2fdf23f327` | 일치 |
| `all-in-one/assets/simulator-workspace.js` | `3a6dfc618ff7e7b238f2671dc85d65704f33093a18eac879d86081d92c31e8bc` | `97c2c831c77a9699fff0e0960b3bc1b7d93d45b3` | 일치 |
| `all-in-one/assets/virtual-plc.js` | `5f1876052dc0067b1f010af0dfc941946e37003167481731293615d9c1c36dbc` | `0bd9eceb54365a91214a37c5601b5067c39a3f75` | 일치 |
| `all-in-one/registers/equipment.json` | `7870325dff32bbca90fa34507b301c4aad3347d669fddcd03b910343663996fa` | `acc42633033398216469064932c4b76987371606` | 일치 |
| `all-in-one/registers/hmi-transfer.json` | `235dec78a1a1d87d316df5339a18c19d279f7274d0e08912b5f4b2f0af0e7f9f` | `767fabb966bbb59dd9fffea5eb69bc654fcb3762` | 일치 |
| `all-in-one/registers/program-model.json` | `6203479c086b15bada12ac9d7e37db9280234ec26f1ea6091d7211dc09a577c5` | `9860b10f008d3a5ae714be50d77b703dfec32f3a` | 일치 |
| `all-in-one/registers/simulator-freeze.json` | `bb93c1994effc5609939ba566b7802ce7ed55154a7310f02379b308ac2c8c835` | `808ffac14dbd1b4a7d797fa6cd0d647635d90b47` | 일치 |
| `all-in-one/registers/virtual-plc-test-results.json` | `a6b389f797f9a8b5ffe6928b8420f55c4cc459a327b0b48d716079d2eca6dd64` | `757dd50e45184568facb8ff62900b39d3ce848d1` | 일치 |
| `all-in-one/sources/Electrical_Rev2.pdf` | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` | `f610fd7c7ce14ae951b00cff57b969259bfb389d` | 일치 |
| `all-in-one/sources/decoded-original/0064-IdentXmlPart.xml` | `ce6afc4f7ca0a8059c2e3cab25d202f0faaa49a3bc6a2e9ee238964a76e9fc9d` | `300d74239868f4f4595d4d5bbb848b4b58bbae76` | 일치 |
| `all-in-one/sources/decoded-original/0158-FlgNet.xml` | `d3f3adebc3d990b85c5d4c294906ae3bc3dafebb49d25b030bf9cc2ccf905651` | `233ccf8f9d82ffffa498e04cbdcd3de07115c1db` | 일치 |
| `all-in-one/sources/decoded-original/0162-FlgNet.xml` | `892eab96a4f5c87cfafd35f8a2e2a04982a93ca23c777312101882e408b11deb` | `8b3887811075409309a0428bd49842dd9b6c1486` | 일치 |
| `all-in-one/sources/decoded-original/0355-FlgNet.xml` | `73592d33f8b3a71effeb36f25427c76e931485e7ce31f5c81f144ddae83c4247` | `54f7a267c9b44c325fd5af31ea78736049d8b1ef` | 일치 |
| `all-in-one/sources/decoded-original/0357-FlgNet.xml` | `a0334f249d3b026599a24ab6e59645e045302e802f70ed0ecf7be8d830d46d3c` | `190480a9be7c3bc231442791aa3675c59c3778d4` | 일치 |
| `all-in-one/sources/decoded-original/0401-FlgNet.xml` | `60171c213e666de544077b7e4b497675813f7c0e75df85a3e76ab1def49b04ae` | `aadefbd35d305dd4a1146bf383b988a903802bf4` | 일치 |
| `all-in-one/sources/decoded-original/0564-IdentXmlPart.xml` | `2aed17fa02d19b0a081023282841aa561d6a2dca3e393284da3622b967af00b1` | `c4b1f2cb191970cfce1cce59cb290a9f1f934c37` | 일치 |
| `all-in-one/sources/decoded-original/0565-IdentXmlPart.xml` | `0f7f970faa6c456f2bb032b1a2072a2f52db1e03fc77bd8d35d4583deeaf1149` | `c2e3e2d57c94c5da864f6e172f0a7a925da942d6` | 일치 |
| `all-in-one/sources/decoded-original/0566-IdentXmlPart.xml` | `a1914c7ae085acc1f949a649979824bec8b46fcd78a8055318272a1eb5a45265` | `348e6fccf44a8497f58f73e89ec98e892b2df436` | 일치 |
| `all-in-one/sources/decoded-original/0567-IdentXmlPart.xml` | `5d428b5d5a2b0f4649dbbbb4e4f060a9d89a107e9cf4b6139d8f003c4371347e` | `48d2fdc3a37b692bfda5234b3cd84c48269552f2` | 일치 |
| `all-in-one/sources/decoded-original/0568-IdentXmlPart.xml` | `4ea2540c76f86ab5b17a30c7c9182cc0026bc6b05e605eddcd4af6fc3b919f89` | `c3b9bb052c2200805c3d0af5237d41ebaafaaad5` | 일치 |
| `all-in-one/sources/decoded-original/0569-IdentXmlPart.xml` | `2e77bb83cf9a7aecd228dac33fe1c897e1149f2063786f4f4e54c66be618a2c7` | `d58446112989460d247fc9f2e1b39bb7e4ada67d` | 일치 |
| `all-in-one/sources/decoded-original/0575-IdentXmlPart.xml` | `40e7b2caf89ab7f1ed9075547a7728bd02441e24451bdd8bf97c843637daad06` | `07d5d2548e8f36252a346d0b83341e27c3cb14ba` | 일치 |
| `all-in-one/sources/decoded-original/0576-IdentXmlPart.xml` | `c8b5f9b9ead0e124f1f817b49d89611ed7b2ce04ecd91ddaa139f2ec89d48dbe` | `819b47160eaa6d08c212f71e5b5486ef5b55b6f2` | 일치 |
| `all-in-one/sources/decoded-original/0577-IdentXmlPart.xml` | `511e01fae619dc385357908a1ac62030dbdfd5f5399bd4c22bc58bebbfc3bf47` | `a505ebf7efd05a85850dc29559a4f71242bacae3` | 일치 |
| `all-in-one/sources/decoded-original/0578-IdentXmlPart.xml` | `0f9f41b5dee25ea17c7a29ab6f7b00503c13d0f265266acd660072baf061d32b` | `070a79fb12139898dd44a17ab2061e795956b9c6` | 일치 |
| `all-in-one/sources/decoded-original/0579-IdentXmlPart.xml` | `ee35cf525388f2b38399787caef57a978b0bb17216a90e1a90ac4391e0e799fe` | `19d1039319ffeb150767d96fc36205326483b1c4` | 일치 |
| `all-in-one/sources/decoded-original/0603-IdentXmlPart.xml` | `e93969dfa281d75b49b24127793068e33472dadb19729c1c48fc4a8dad075ef8` | `3a92b304baf4dbf6147e944d9778d2da11285cb1` | 일치 |
| `all-in-one/sources/decoded-original/0604-IdentXmlPart.xml` | `b798d29c5499b5314a1ee3cff9139dae64c887533b86baa43b6e9a052373a6af` | `bb2c318788b97e7a4924a176275c12d805aa519d` | 일치 |
| `all-in-one/sources/decoded-original/0621-IdentXmlPart.xml` | `a63e2b97ea9eb2691cb478666afed77fc58a2da2f8170422dc09e24b102c88ee` | `844516839e55f8bf231a18630e010b912190664e` | 일치 |
| `all-in-one/sources/decoded-original/0623-IdentXmlPart.xml` | `4acd00406ea92466169e57e59fc90b0da4d9ec55fd19e2e96c9556e939cb83a6` | `13b3af0459c8e6069bb9b2f1b16454bf479e08dc` | 일치 |
| `all-in-one/sources/decoded-original/0624-IdentXmlPart.xml` | `24607c0827fbde428bccf8637ef4ae490798a69a7c2f3b87861d0749082d367a` | `02511fea47fc47981c101bba49dc40adde1cdcc3` | 일치 |
| `all-in-one/sources/decoded-original/0632-IdentXmlPart.xml` | `fd162c603476c2cac899010cee7a8ee382b6092c115135e3ac1007ae71c544e9` | `600935fa8d394c0d247ea20040d5dfff4f05b500` | 일치 |
| `all-in-one/sources/decoded-original/0633-IdentXmlPart.xml` | `9e00aa275fa1b4e488b73983b309c6b73dcf4f3dd9be5dec13e9975d68f3c0fc` | `a1ab5ee12addbc92d04c9950d4437e2b564d6b5c` | 일치 |
| `all-in-one/sources/decoded-original/network-map.json` | `c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60` | `424430b6b953e43138e5d0a18ca40c949e21cfa1` | 일치 |
| `all-in-one/sources/hmi-windows.csv` | `15f8d69b5c43d4fdbe550f9cd2717f855fea877ed8146973054cb6dbcaa9892e` | `8401dcfe5ba3e7e244eea0f501bb84a2e387da39` | 일치 |
| `all-in-one/sources/hmi_plc_tags.csv` | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` | `cf4c0650e7c7baac350dcb89909b808435704880` | 일치 |
| `docs/equipment-standard/INVENTORY.json` | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` | `587c3748ad9224718f95ba06463fee913dae231d` | 일치 |

### 자체검사 결과

2026-10-11T11:52:13.298525+00:00 UTC, `python extracts/SYS-HMI/verify.py` 종료0, 문서 자체검사16항목 passed. 선정37파일 고정 Gitblob/현 바이트 일치, 중지5자산 freeze해시 일치, 원본 Git 변경0. 작성 중 동일주소 태그 내부ID4개와 Word20/22 Wire 번호를 실제 CSV/XML로 재확인·정정한 후 통과했다. 원본 시험/생성기·UI·시뮬레이터·현장 시험은 실행하지 않았다. 자체검사 로그는 `extracts/SYS-HMI/self-check.json`. 부모의 독립 검토·전송 전 단계이다.
