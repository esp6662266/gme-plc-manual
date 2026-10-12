# RD01-FAN 드럼 모터 냉각팬 — 독립 구성품 조사 초안

고정 원본: `abcf31c5030bc7ef8749ed8e869a857f2387a28a` / v1.12.0 / `gme-research/source-mv06`. 작성일 2026-10-11 UTC. 문서조사 범위만 완료하며 RD01 부모의 통합·게시·현장 완료를 상속하지 않는다. 모델 런타임 증명은 미확인이다.

## 핵심 확인·상충·누락·공유 근거

- 고유 근거: `0245`의 팬 요청 DB2.X0.2 → Q0.2, `0425`의 DB13.X0.4 응답부재 → T52/S5T#2S → DB3.X0.2, `0310`의 원시 I0.4 운전시간 경로를 직접 대조했다. 팬이라는 이름만으로 I/O를 발명한 것이 아니다.
- 전기 고유 근거: FG22/실제 PDF23의 M04/RD-01F, 22QM1/22KM1/22QS1, A0.2와 E0.4를 FG136/PDF137, FG116/PDF117 양 끝점까지 직접 렌더 대조했다.
- 소유 경계: I0.4는 22KM1 보조접점 응답이다. 풍량·실회전·냉각효과·드럼 정상의 증명이 아니다. 주모터 M03/Q0.1·윤활 EV03/Q5.1은 팬 소유가 아니다.
- 중요한 별도 경로: 부모 `0243`은 NOT 팬 처리응답 자체를 주구동 요청 Reset 조건으로 사용한다. “팬 고장 2초 뒤에만 주구동 정지”로 단순화하지 않는다.
- 상충/주의: HMI CSV 주소는 있으나 `0359`의 네 고유 run/Alarm1/Risposta/누적알람 operand는 같은 호출 문맥의 선언 결속이 미확보다. DB11 표시를 DB3 알람 자체와 동일시하지 않는다. 팬 시간 HOUR는 `Move 1`이지 `HOUR+1`이 아니다.
- 공유 근거 색인: 기존 `RD01-DOTS-DRAFT.md` §2.3/3.3/4.3/4.5/5.2를 탐색 인덱스로 재사용했다. 동일 고정 원본의 공통 자동순서·Word입력·HMI 처리 경계는 연결 재사용하고, 팬 고유 핀/선언/도면은 재확인했다. RD01 전체·STO·주모터 속도/전류·윤활을 반복 조사하지 않았다.
- 미확정: 현재 CPU/실물 동일성/정상 극성/현행 보호 설정/현재 동작·복구, HMI 실제 이벤트, 다른 쓰기의 실행 우선순위, 실측 케이블과 명판. 현장 자료 없이 이를 채우지 않는다.

## 1. 설비·자료 기준

|항목|확인 및 범위|
|---|---|
|대장|`docs/equipment-standard/INVENTORY.json#/catalog/119`: RD01-FAN, motor, parent RD01, depth1, phase2, planned, specialist, not_assessed|
|배치|TASK3-BATCH18-SCOPE의 별칭 fan rd01/rd01f/rd_01_fan, 역할 RD01 구동 모터 냉각 보조장치, FG22. 별칭은 현장 실물 일치 판정이 아니다.|
|P&ID|`PID_1684n002I.pdf` 실제 PDF1: RD-01 곁의 M04 0.75kW 440V와 M03은 별도 표기. 도면 1684n002, Apice I, 개정 I 15/01/2013 “REMOVED MC-05, CHANGED POWER OF FN-02”, 원 도면일 06/04/2011. 이 오래된 공정도와 2024/2025 전기도를 동일 시점으로 취급하지 않는다.|
|OEM 회로|`Electrical_Rev2.pdf` FG22/PDF23, DATA27.05.2024, 페이지 개정란 공란. M04 RD-01F, COOLING FAN ROTATION DRUM MOTOR. 인쇄 0.75kW/1.67A/440V60Hz는 현재 명판 증명이 아니다.|
|시공도|`Electrical_Can_Decoating_20241118.pdf` PDF24/51의 M04와 =ROT+RD01-M04A. 기존 원자료만 읽었으며 SEJIN 프로그램·운영자료 편집/통합 없음. 승인·준공/현재 배선 일치는 별도 필요.|

루트 AGENTS, rollout SKILL, WORK-STANDARD, WORK-ITEM-TEMPLATE, INVENTORY 및 최신 고정판 인계 머리말을 읽었다. 원본 생성기/시험을 실행하지 않고 자체 XML 파싱·원본 해시·PDF 렌더만 사용했다. 문서 내 네 자리 숫자는 `all-in-one/sources/decoded-original/NNNN-FlgNet.xml` 또는 명시한 IdentXmlPart를 뜻한다. LAD 문서 번호는 network-map의 색인이며 선언 NID와 다르다.

## 2. I/O·HMI·선언

### 2.1 팬 고유 물리/내부 층

|신호|원본 선언과 주소|결속/소유|
|---|---|---|
|Start fan RD01|0602 SimpleAccess RID56, Global Bool, Output AO2/SAM None → Q0.2|NID9 UID294 AK Write → 0245 Coil287 operand W305/ORef294. 0658 RID42는 0425 NID9 UID362 읽기.|
|RD01F_Fbk|0613 SimpleAccess RID134, Global Bool, Input AO4 → I0.4|NID22 UID1234 읽기 → 0310 Contact1264. 원시 입력이며 팬풍량 센서로 명명하지 않는다.|
|Flag.M_RD_01_FAN|0604 GlobalAccess RID55, Bool AO2 BAD2; 0603 DepDBBlock RID2 TOD2 → DB2.X0.2|NID9 UID292 Reset Write / UID293 Read. 0577 RID36에도 NID3 UID620 Set, NID4 UID971 Set, NID5 UID1012 Reset.|
|Inputs.fan RD01 run|0657 GlobalAccess RID271 AO4 BAD247; 0655 RID247 TOD13 → DB13.X0.4|0425 NID9 UID399/366 Read. 부모 사용은 0604 RID222 BAD218 및 0603 TOD13, NID7 UID27.|
|Allarm.RD_01_FAN_FAULT|0657 GlobalAccess RID45 AO2 BAD10; 0655 RID10 TOD3 → DB3.X0.2|NID9 UID367 Set/UID370 Reset/UID369 Read. 0604 RID54 NID9 UID289가 요청 Reset에 읽음.|
|Tag_55|0658 SimpleAccess RID43, Global Timer AO52 → T52|NID9 UID364 Write / UID365 Read. HMI 태그가 아니다.|
|팬 MIN/HOUR|0615 GlobalAccess RID136/138 Int AO672/688 BAD5, 0614 RID5 TOD9|DB9.DBW84/86. NID22 UID1235/1237/1238/1243와 UID1241.|

DB2.X0.2, DB3.X0.2, Q0.2는 서로 다른 영역이다. 숫자 0.2만으로 병합하지 않는다. 위 고유 대상은 Global/SimpleAccess이며 임의 Local 변수/직접 주변장치 PIW로 재분류하지 않았다.

### 2.2 Word 전달과 다른 writer

`0397` LAD1070/NID1, Move22 in W23/ORef25=0627 RID3 Tag_178 Word Input AO0/SAM None(IW0), out1 W24/ORef26=0629 RID5 Word AO0/BAD4→0628 RID4 Inputs TOD13(DB13.DBW0). I0.4를 포함하는 입력 Word 전달을 확인했다. 해당 Move의 DisableENO=true와 후속 eno W34 연결은 원문대로 보존한다. 이 Word경로를 팬전용 bit Coil이나 PIW 읽기로 바꾸지 않는다.

부모 초안의 main0030 호출/NOT Simulation 경계는 같은 고정원본 공유 근거로 연결한다. 이번에 전체 main/모든 writer를 재분석했다고 주장하지 않는다. `0635`에는 Inputs.fan RD01 run RID206/NID1 UID42 AK Write 및 Flag팬 RID10 UID30 Read가 남아 있다. 기존 중지 영역의 선언 존재만 확인했으며 실행·활성·현재값으로 해석하지 않았다. 팬 응답이 언제나 원시 I0.4와 같다는 완전성 주장은 보류한다.

### 2.3 HMI 설정 및 호출의 미결속

CSV `hmi_plc_tags.csv` 줄26/137/425:

|태그|주소|TagID|
|---|---|---|
|RD_01_FAN\Allarme1|DB11,X4.1|0044B|
|RD_01_FAN\RispostaA|DB11,X4.0|00326|
|RD_01_FAN\Flag|DB2,X0.2|001B2|

AccessName PLC, dde.cfg 설정이며 버튼 이벤트/현재 접근권한·온라인값 확인은 아니다.

`0359` LAD1180은 CRef22 Ref638 / CodeBlock23 Ref1, powerrail W21→en. 0624 RID638 인터페이스와 0623 RID1 FC “HMI Standard Motors”를 확인했다. NID는 network-map 미추론(None); 0626 상수의 NID3/UID27~30는 후보 문맥을 지지하나 원래 전체 결속 완료로 올리지 않는다.

|핀|Wire/ORef/RID|판정|
|---|---|---|
|Ingresso_run|W37/ORef24/RID712|호출 문맥의 대응 GlobalAccess 미확보|
|Allarme1|W39/ORef26/RID44|같은 문맥의 선언 미확보; 다른 파일 RID44로 대체 금지|
|Allarme2|W40/ORef27/RID48|0626 LiteralConstant Bool FALSE, V0, NID3 UID27|
|Allarme3/4/5|W41/42/43, ORef28/29/30, RID20|0626 Bool false V0, NID3 UID28/29/30|
|Risposta|W46/ORef33/RID37|출력 결속 미확보|
|Comulativo_allarmi|W48/ORef35/RID39|출력 결속 미확보|

0625의 Motors TOD11, Allarm TOD3, Inputs TOD13 의존 블록은 존재하나 개별 변수 선언을 대신하지 않는다. DB11.X4.1을 DB3.X0.2와 직접 동일시하거나 태그 Flag라는 이름만으로 실제 HMI 쓰기를 확정하지 않는다.

## 3. 제어 구조·요청 소유

### 3.1 팬 요청 Reset과 출력은 별도 가지

`0245` LAD1939/NID9 원본:

- Powerrail W317→ON Contact307(operand W295/ORef288/RID1, 0602 ON M0.0).
- W308에서 fanFault Contact309(W296/ORef289/RID54)와 NOT R2_GATE_LOOP_ON Contact311(W297/ORef290/RID46), 그리고 팬요청 Contact315로 분기.
- fault309→W310→OR278.in1.
- NOT R2 Contact311→W312→NOT STANDBY Contact313(W298/ORef291/RID11)→W21→NOT UNDER TESTING Contact318(W321/ORef319/RID4)→W22→OR278.in2.
- OR278.out W300→RCoil283, operand W302/ORef292/RID55=Flag.M_RD_01_FAN.
- 다른 가지 ON→팬요청 Contact315(W303/ORef293/RID55)→W316→Coil287, operand W305/ORef294/RID56=Q0.2.

정적 Reset식: ON AND [fanFault OR (NOT R2loop AND NOT Standby AND NOT UnderTesting)]. 출력 가지: ON AND 팬요청. 원문 UNDER TESTING은 0602 RID4 Memory AO45(M5.5), Standby는 0604 RID11 AO60(DB2.X7.4), R2loop RID46 AO84(DB2.X10.4). 현장 우회나 강제 조작을 제안하지 않는다. 동일 주기 Set/Reset/HMI 쓰기 우선순위와 최종 Q의 온라인 결과는 미확정이다.

### 3.2 자동 요청 writer의 팬 부분만 재확인

공통 선행조건은 부모 RD01 초안 §3.3과 연결하고 팬 부분 원본 핀을 직접 대조했다.

|네트워크|팬 고유 부분|선언|
|---|---|---|
|0164 LAD1843/NID3|ON785→NOT Emergency fault22→Tipo_preset=1 Eq400→Auto_ON1 Contact823. Eq466 Tempo_presetting W711/ORef618 ==19 W712/ORef619→W713→S469, operand W715/ORef620|0577 RID7 Tempo Int; 0578 RID35 Int19; 0577 RID36 Flag팬 Set|
|0165 LAD1844/NID4|생산 Tipo_preset=2 공통 허가 후 Contact737.out W1021→Eq814. Tempo W1073/ORef969 ==33 W1074/ORef970→W1075→S817, operand W1077/ORef971|0577 RID7; 0578 RID61 Int33; 0577 RID36 Flag팬 Set|
|0166 LAD1847/NID5|Auto_ON1 Contact1095→Eq881 Tipo_preset=5→W1031. Eq945 Tempo W1066/ORef1010 ==17 W1067/ORef1011 또는 Emergency fault1114 W1117/ORef1115→OR39→W41→R948 operand W1070/ORef1012|0578 RID30 Int17; 0577 RID108 Emergency_module_fault; 0577 RID36 Flag팬 Reset|

19/33/17은 정수 비교값이다. 시간 단위나 현재 지연을 초로 발명하지 않는다. NID5 앞단에 ON을 추가하지 않는다. 요청 writer를 확인했지 자동순서 전체의 안전성·현재 운전 허가를 판정한 것이 아니다.

### 3.3 부모에 미치는 영향

`0243` LAD1936/NID7: ON270 뒤 W271→NOT Contact26, operand W25/ORef27/RID222=Inputs.fan RD01 run→W32→OR28.in4→W30→RCoil236, operand W265/ORef249/RID47=Flag.M_RD_01(DB2.X0.1). 이것은 팬 응답 미도달에 대한 주구동 요청 Reset이며, `0425`의 2초 fanFault 래치와 별개다. 다른 OR 네 조건·Q0.1 회로는 부모 소유로 연결하고 이 구성품의 신규 알람으로 집계하지 않는다.

### 3.4 팬 운전시간

`0310` LAD1020/NID22: Tag_47 Contact1262(W1245/ORef1233,0613 RID1 Timer AO13=T13) AND RD01F_Fbk Contact1264(W1246/ORef1234)→W1265에서 Add1216와 Ge1223으로 분기.

- Add1216 Int: in1 MIN W1247/ORef1235, in2 Int1 W1248/ORef1236, out MIN W1249/ORef1237.
- Ge1223: MIN W1250/ORef1238 ≥ Int60 W1251/ORef1239→W1252→Move1226.
- Move1226 in Int1 W1254/ORef1240, out1 HOUR W1255/ORef1241. HOUR에 1을 쓰는 원문이지 HOUR 누적 덧셈이 아니다.
- eno W1256→Move1229, in Int0 W1257/ORef1242→MIN out1 W1258/ORef1243; eno W1259→SCoil1232 operand W1260/ORef1244(0613 RID13 Global Bool Flag_Aggiorna_DB, Memory AO15=M1.7).

Int1/60/0은 0616 RID7/8/12, 팬 MIN/HOUR은 0615 RID136/138로 확인했다. Tag47 생성주기·공통0336·다른 DB갱신/보존은 부모/공통 운전시간 조사와 연결하며 이번 팬 조사에서 전체 재분석하지 않았다. 실제 정비주기나 누적시간 정확성을 보증하지 않는다.

## 4. 전기 전달 경로·끝점·개정

실제 PDF 렌더 6쪽과 P&ID 확대를 확인했다. FG와 PDF페이지를 별도로 기록한다.

|원본/실제 페이지|고유 끝점과 해석|개정란|
|---|---|---|
|Electrical_Rev2 FG22/PDF23|440V60Hz 8.3L1/L2/L3(8/1)→22QM1 1/3/5→2/4/6→22KM1 전력접점1/3/5→2/4/6→22U1/V1/W1→XM→22QS1 1/3/5→2/4/6→M04 RD-01F U/V/W 및 PE. 22QM1 인쇄1.4–2A, BLACK FS17 1.5mmq, 모터0.75kW1.67A|DATA27.05.2024, REV 공란|
|FG136/PDF137→FG22/PDF23|MOD14 단자3 A0.2, 참조22/4→XS5→22QS1 보조→XS6→22.1→22QM1 보조→22KM1 A1/A2→−0Vdc10.6. 두 보조접점의 단자번호는 그림에 별도 숫자가 없어 발명하지 않음.|FG136 Rev2 17.03.2025, FG22 공란|
|FG22/PDF23→FG116/PDF117|+24Vdc10.7→22KM1 보조13–14→E0.4(116/5)→MOD8 단자5 E0.4 “FEEDBACK MOTOR RD-01F”, 반대참조22/6|FG116 공란, DATA27.05.2024|
|시공 PDF24/64|ROTARY SIDE01, 100RC에서 M04 경로2, Pipe16, =ROT+RD01-M04A, CV/1.5/4. M03/EV03·PV02 경로는 주변이며 팬 소유로 합치지 않음.|CANDC-CONS-E007-024, D-PAGE7, Rev1 24.11.11 first draft design; CHECKED/APPROVED 공란|
|시공 PDF51/64 행1_6|=ROT+RD01-M04A, FROM CR→TO RD-01 M04 “COOLINGFAN ROTATION DRUM MOTOR”; GAC/CV/CORE4/SIZE1.5/SPARE0, Route100RC→E200, Adjustment7, LEN39|CANDC-CONS-C001-051, D-PAGE1, Rev1 24.11.11 first draft design; CHECKED/APPROVED 공란|

FG136의 CPU515 표시는 도면 문자열이며 현재 설치 CPU 검증이 아니다. 전원/차단기 범위·전선 단면·길이는 설계 인쇄치로만 남긴다. M03의 케이블16/25SB 상충은 부모 고유 문제이며 M04 팬 케이블의 상충으로 복사하지 않는다. FG22의 실제 보조응답은13–14이며 다른 릴레이의 하단1/5/9 표를 이 접점에 적용하지 않는다.

팬 독립 속도지령·인버터·전류 AI·풍량센서·냉각온도센서는 이 선정 원본에서 팬 고유 대응 근거 미확보다. 부모 RD01의 PQW290/PIW332를 팬에 배정하지 않는다.

## 5. 알람·Reset·복구

`0425` LAD1788/NID9의 별도 팬감시:

|부분|Part/Wire/ORef와 원본 해석|
|---|---|
|허가|Powerrail W397→ON385 operand W371/ORef361=0658 RID1 ON → W386→Startfan387 operand W372/ORef362=0658 RID42 Q0.2|
|응답부재 타이머|Startfan.out W388→NOT Contact398 operand W401/ORef399=0657 RID271→W21→SdCoil349.in. value W373/ORef363=0656 RID28 S5Time SV S5T#2S/V512; operand W374/ORef364=0658 RID43 Tag55 T52|
|Set|Startfan뒤 W388→Tag55 Contact389 operand W375/ORef365→W390→NOT 팬RUN Contact391 operand W376/ORef366→W392→SCoil355 operand W378/ORef367=0657 RID45 DB3.X0.2|
|Reset|ON뒤 W386→RESET_ALLARM Contact393 operand W380/ORef368=0657 RID13 Flag.RESET_ALLARM AO48/BAD12→W394→fanFault Contact395 W381/ORef369→W396→RCoil360 operand W383/ORef370=DB3.X0.2|

Set의 원인은 Q0.2 요청 출력에 대해 처리응답 부재가 2초 감시 경로를 통과하는 것이다. 차단기 전용 trip입력·팬풍량 부족 알람으로 바꾸지 않는다. Reset 가지에는 원인입력 정상화 접점이 별도로 없다. Reset 요청/래치해제/재기동/실제 팬회전/냉각 회복은 각각 별도 증거가 필요하다. `0245`의 fault에 의한 팬요청 Reset, `0243`의 팬응답 부재에 의한 부모 요청 Reset과 구분한다.

현재 타이머 실행·래치 우선순위·정상극성·실제 복구가 확인되지 않았다. 강제출력, 접점우회, 보호값/타이머 변경, 현장 행동시험은 하지 않으며 이 문서는 그러한 조작 지시가 아니다.

## 6. 증상별 관찰·자료 수집 경계

|증상|문서상 비교 위치|필요한 관찰/판정 경계|
|---|---|---|
|팬 요청이 유지되지 않음|DB2.X0.2의 자동 Set/Reset,0245 Reset 조건, HMI 설정|현재 프로젝트 식별/시각, 요청·fault·R2loop·Standby 값 및 실제 writer 순서. 새 우회 권고 없음.|
|Q0.2 표시가 있으나 응답 없음|FG136 단자3→FG22 XS5/6·22QS1·22QM1·22KM1 A1/A2, 보조13/14→FG116 단자5|자격자가 별도 안전절차 아래 확보한 회로/측정 기록이 필요. 원인구간을 현재 증거 없이 단정하지 않음.|
|fanFault 발생|I0.4→IW0/DB13.DBW0→DB13.X0.4, Q0.2, T52, DB3.X0.2|발생/Reset 시각과 raw·처리·명령·알람의 동시 기록. HMI DB11.X4.1과 직접 동일시 금지.|
|RD01 본체 요청도 해제됨|0243 NOT 팬응답 가지|팬 2초 래치와 별도의 부모 연동인지 비교. 부모 전체 고장원인 완료판정 아님.|
|응답은 있으나 냉각 불명|22KM1 보조응답의 의미 한계|모터/팬 명판과 별도 현장 회전·냉각 관찰. 보조접점만으로 정상판정 금지.|
|시간/표시 이상|0310 MIN/HOUR Move1 및 ENO 경로, HMI0359/CSV|현재 시간베이스·다른 writer·표시 이벤트 자료. 누적시간이나 정비주기를 추정하지 않음.|

관찰자·시각/시간대·장치/프로젝트식별·값/단위·비교원본·최초 불일치구간·조치 권한·복구증거를 별도 수집해야 한다. 이번 조사에 현장 관찰·실제 운영기록은 없다.

## 7. 완료·누락·인계

|7영역|문서 상태|남은 증거|
|---|---|---|
|설비·자료 기준|적용, 부모/팬 분리|현재 M04 실물·명판/설치 동일성|
|I/O·HMI|적용, 원시/Word/처리/표시 분리|HMI 고유 네 핀 결속·이벤트, 현재 I/O 구성|
|제어 구조|적용, 팬 고유 요청/출력/시간과 부모영향|전체 호출·복수쓰기 우선순위·온라인 현재값|
|전기 끝점|적용, 지정6쪽 렌더 확인|준공/현행 단자·보조접점·케이블/명판|
|알람·복구|적용, 별도2초 Set/Reset|현재 원인해소·래치해제·재기동·냉각 회복 증거|
|증상 관찰|적용, 관찰 항목만 작성|현장 안전절차에 따른 별도 측정/관찰|
|완료/누락|문서초안 준비|통합 독립검토·UI/기록·배포·TIA/CPU/현장 별도|

도면·래더 비교는 이 초안의 근거 연결만 준비했다. 백업 선택복원, 기록 전후비교, 보고서/PDF 기능은 팬 ID에서 실제 구현·저장/재읽기/재열기를 이번에 검증하지 않았다. 기존 note/repair_observation/미지필드/저장키/초안·다른 설비를 변경하지 않았다.

상태: documentation=draft_ready; static_review=selected_read_only_review; ui_records=not_run; publication=not_published; tia_compile/live_cpu/field_recovery=not_performed. 다음 조치는 이 팬 초안의 원문 인계와 통합 담당자의 독립 검토다. 신규 현장 자료 없는 반복 재조사는 하지 않는다.

### 조사 실적과 보존

- 2026-10-11 13:05:15 UTC 배정; 13:05:19–13:05:37 지시·기준·부모 색인·고정 HEAD/clean 상태 확인.
- 13:05:45–13:07:12 XML 선언/팬 네트워크·자동 고유 writer·Word/시간/HMI 경계 대조.
- 13:06:07–13:07:48 지정 PDF6쪽 렌더와 P&ID 개정란 확대 시각 확인.
- 13:08:09 네트워크색인/선언 추출 저장. 후속 실제 검증 시각과 해시 결과는 아래 검사 부록에 기록한다.

검색은 경계 탐색이며 원본 전체 의미검토 완료 수가 아니다. 팬 핵심 의미검토는 0245/0425/0310/0359와 0397 첫 Move, 0243 팬사용 가지, 0164/0165/0166 팬 writer에 한정했다. 0635는 다른 writer 선언 존재만 확인했다. 공개고정 원본을 읽기전용으로 유지했고 원본·공통코드·버전·대장·배포·운영·PLC·현장·보호값·SEJIN·중지자산 변경 및 시뮬레이터 작성/수정/생성/실행/행동시험은 없다.

## 부록 A. 선정 원본 전체 SHA-256 및 고정 Git blob 대조

아래 선정 파일의 모든 바이트를 고정 commit의 Git blob과 대조한다. 해시/byte 일치는 의미검토 범위·현장 검증을 넓히지 않는다. 중지5자산은 아래 근거와 별도로 해시만 보존 확인한다.

|원본 경로|SHA-256 전체|고정 Git blob|byte 일치|
|---|---|---|---|
|AGENTS.md|`0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2`|`073164bc6efd5791032d62c71b03b4dab48cb6f8`|일치|
|.agents/skills/gme-equipment-rollout/SKILL.md|`fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b`|`9aa820ea6ca15b4e136c9772423b78ed4df6a3d4`|일치|
|docs/equipment-standard/WORK-STANDARD.md|`05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99`|`f76a570cc73098632e08759b17934000f7e3a253`|일치|
|docs/equipment-standard/WORK-ITEM-TEMPLATE.md|`4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586`|`e546f39535d2b589e80f97db869ac37ce4d05cfd`|일치|
|docs/equipment-standard/INVENTORY.json|`720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc`|`587c3748ad9224718f95ba06463fee913dae231d`|일치|
|VERSION.json|`5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7`|`fffb51663b7705aec91cb119ca80ee943a4ce758`|일치|
|all-in-one/sources/Electrical_Rev2.pdf|`5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6`|`f610fd7c7ce14ae951b00cff57b969259bfb389d`|일치|
|all-in-one/sources/Electrical_Can_Decoating_20241118.pdf|`3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd`|`0ee6b6f8361c5790864dbba4bbd9d55e8e7c08f8`|일치|
|all-in-one/sources/PID_1684n002I.pdf|`2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b`|`8c83a59fefd5b8b651ec3537ea4236a073f5e109`|일치|
|all-in-one/sources/hmi_plc_tags.csv|`a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404`|`cf4c0650e7c7baac350dcb89909b808435704880`|일치|
|all-in-one/sources/decoded-original/network-map.json|`c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60`|`424430b6b953e43138e5d0a18ca40c949e21cfa1`|일치|
|all-in-one/sources/decoded-original/0164-FlgNet.xml|`15884b2b362842279b626b669a484b1daa269f5ecd99112b8391bb0387382491`|`1035a51ee3100d524da1b7b204ba142b6b509ac5`|일치|
|all-in-one/sources/decoded-original/0165-FlgNet.xml|`4513a5f6e77717c99c5e869105483be31f7f62ab280e271dc36cd7a2d3e3bb88`|`8d636eb535060037ccf00ebdfb328b8775225fe4`|일치|
|all-in-one/sources/decoded-original/0166-FlgNet.xml|`0330a505877be92172f94bce83222a0bfc8d64aab700a69fc1fa2188010d3853`|`6b3062ae9ac2bc6ad8c2509d3fc4c15609a4b892`|일치|
|all-in-one/sources/decoded-original/0243-FlgNet.xml|`4b3a77029b4d5901ff40f260d54189748e7697bb6077fca502165fa7cd5ea3b5`|`53fff711852ac7ea3150a4cb51d83813d640210d`|일치|
|all-in-one/sources/decoded-original/0245-FlgNet.xml|`c89543f2a25028652f425fc8979bae3cde56cdcf8022b81beaadd49ab568abb6`|`0571bcd756f08cbff2162f09fbec178bc71f0b00`|일치|
|all-in-one/sources/decoded-original/0310-FlgNet.xml|`c9f5daacd865ba3757ba2621250c8240659c98dc30d38c012ca72e608b613e5f`|`b66213e3c7ecfe62b52634fdfc99aa8533f6538d`|일치|
|all-in-one/sources/decoded-original/0359-FlgNet.xml|`eb4aae8bb8ef4e805f42c7ba320ad5f2f1b0a442c1f949a5ef161e4dcc1e1dec`|`b77b3ff2e0571afc664f7f30842e4fe2faa1351c`|일치|
|all-in-one/sources/decoded-original/0397-FlgNet.xml|`bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834`|`4ab8370493c4e28fc1eabeeebe2743d27f0c4021`|일치|
|all-in-one/sources/decoded-original/0425-FlgNet.xml|`9db302ef56730d0219869c9a9e1a38d0a8d0378a1f84cb94472f0f453ca0401c`|`ca964fdbda4714123adb71e36ec874c8ac4e9e24`|일치|
|all-in-one/sources/decoded-original/0555-IdentXmlPart.xml|`46c36333e249dd775c1db94a1f6e80a36cf1a5a9c998b7d0980ae01d862901e6`|`9a915a8b9a260b48402df151c1fe0bbcb2f4ea1c`|일치|
|all-in-one/sources/decoded-original/0575-IdentXmlPart.xml|`40e7b2caf89ab7f1ed9075547a7728bd02441e24451bdd8bf97c843637daad06`|`07d5d2548e8f36252a346d0b83341e27c3cb14ba`|일치|
|all-in-one/sources/decoded-original/0576-IdentXmlPart.xml|`c8b5f9b9ead0e124f1f817b49d89611ed7b2ce04ecd91ddaa139f2ec89d48dbe`|`819b47160eaa6d08c212f71e5b5486ef5b55b6f2`|일치|
|all-in-one/sources/decoded-original/0577-IdentXmlPart.xml|`511e01fae619dc385357908a1ac62030dbdfd5f5399bd4c22bc58bebbfc3bf47`|`a505ebf7efd05a85850dc29559a4f71242bacae3`|일치|
|all-in-one/sources/decoded-original/0578-IdentXmlPart.xml|`0f9f41b5dee25ea17c7a29ab6f7b00503c13d0f265266acd660072baf061d32b`|`070a79fb12139898dd44a17ab2061e795956b9c6`|일치|
|all-in-one/sources/decoded-original/0602-IdentXmlPart.xml|`46ab21151eddaaf616469db520730c60423eb742aa491af194e6710c751b4caf`|`bcb12ab1ce8c476ff921baa1608f29d9822f76b4`|일치|
|all-in-one/sources/decoded-original/0603-IdentXmlPart.xml|`e93969dfa281d75b49b24127793068e33472dadb19729c1c48fc4a8dad075ef8`|`3a92b304baf4dbf6147e944d9778d2da11285cb1`|일치|
|all-in-one/sources/decoded-original/0604-IdentXmlPart.xml|`b798d29c5499b5314a1ee3cff9139dae64c887533b86baa43b6e9a052373a6af`|`bb2c318788b97e7a4924a176275c12d805aa519d`|일치|
|all-in-one/sources/decoded-original/0613-IdentXmlPart.xml|`09d3b1397a987898334218f37e025661af162438582e649f671e7abec443d3cb`|`c9d19a48e947098914f4d2de3348c05b4f6d37e8`|일치|
|all-in-one/sources/decoded-original/0614-IdentXmlPart.xml|`c6de26f74d75f5be858a406de75eaf6faf62ba9b89c8f9a085b5dd206e93d294`|`da0485aa033700f08c8695d30b93ebd2d377d6c7`|일치|
|all-in-one/sources/decoded-original/0615-IdentXmlPart.xml|`80f4544edca56c6e6bb2713c758c92ade9202255110074931e03fe34d0d0801a`|`49eb86fe01feb83de8c0864b21493d305aff8b20`|일치|
|all-in-one/sources/decoded-original/0616-IdentXmlPart.xml|`650b53354a0c8443d94adc5bd6a860d3c5313014a52e0fb98a5656a65b58cc0d`|`9f7fdd5f93ac149c139a054ebb34f63c632ef7fd`|일치|
|all-in-one/sources/decoded-original/0623-IdentXmlPart.xml|`4acd00406ea92466169e57e59fc90b0da4d9ec55fd19e2e96c9556e939cb83a6`|`13b3af0459c8e6069bb9b2f1b16454bf479e08dc`|일치|
|all-in-one/sources/decoded-original/0624-IdentXmlPart.xml|`24607c0827fbde428bccf8637ef4ae490798a69a7c2f3b87861d0749082d367a`|`02511fea47fc47981c101bba49dc40adde1cdcc3`|일치|
|all-in-one/sources/decoded-original/0625-IdentXmlPart.xml|`17a9f9bd540bf0a54e9973391fa258d81e567248fd201ae4ff32c367359e69f9`|`047b29b8c09a15a666553bf04eb4fb00f00e1bf8`|일치|
|all-in-one/sources/decoded-original/0626-IdentXmlPart.xml|`a9d7fbea345eca70325a8c2e44058c23e96add1b7207eabbb09445118b18188b`|`e0fc80d0c20f4db3eea31d35f578a2fa3c09f8e7`|일치|
|all-in-one/sources/decoded-original/0627-IdentXmlPart.xml|`08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb`|`61ebc0abbb2ca160e11e1da400a3f14a397d8bc5`|일치|
|all-in-one/sources/decoded-original/0628-IdentXmlPart.xml|`9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd`|`170ca5c72599edc7ea7eefe651c3680ce325e76a`|일치|
|all-in-one/sources/decoded-original/0629-IdentXmlPart.xml|`67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972`|`058129bb01e27f7a6a0d0293f332d745e5bab74e`|일치|
|all-in-one/sources/decoded-original/0635-IdentXmlPart.xml|`1a057d686446a3fdab7ac61bb09bc543c52f49646c9ca71ac323c10fcdffe457`|`95bfcad59cfb0c12b573e9e8face4262d1e94622`|일치|
|all-in-one/sources/decoded-original/0655-IdentXmlPart.xml|`38e9f323024fba19582b473f39b1ed03ffe6a0b390218894029a6edb0b1ff9fb`|`83b60b9de4541a3ffa6ee0db98205a372b525665`|일치|
|all-in-one/sources/decoded-original/0656-IdentXmlPart.xml|`0dbc45e84732a8848f17b094ea08ab8578dbf240bfe15cd7086859395c27c592`|`9bfb9842e55901bab9a71d1ac03158467dfbb1bc`|일치|
|all-in-one/sources/decoded-original/0657-IdentXmlPart.xml|`0f70cda60a6b1a17175876d58e25b2686952642de6cffb21213aeef8b347a22b`|`e625f3d8999c7be7d88c50eab0d93107117b58ec`|일치|
|all-in-one/sources/decoded-original/0658-IdentXmlPart.xml|`998294c0c8a99e00ceb33c2c60def2cd4850e34328917ae506244c2be2df3831`|`de9a12a6be87466ef1bf05df71c54580c556a827`|일치|

## 부록 B. 검사 및 중지5자산 보존

실제 확인 시각 2026-10-11T13:11:53.966455+00:00. 선정 44파일은 모두 고정 Git blob bytes와 일치. 원본 Git status clean. 이는 전체 논리 의미검토나 TIA/CPU/현장 검증이 아니다.

|중지자산|SHA-256 전체|동결 manifest 일치|
|---|---|---|
|all-in-one/registers/program-model.json|`6203479c086b15bada12ac9d7e37db9280234ec26f1ea6091d7211dc09a577c5`|일치|
|all-in-one/assets/program-model-data.js|`52f8199371e3399b7c0d44ab5469f0472aced79d56bbef2887f7625f5d2aff0f`|일치|
|all-in-one/assets/virtual-plc.js|`5f1876052dc0067b1f010af0dfc941946e37003167481731293615d9c1c36dbc`|일치|
|all-in-one/assets/simulator-workspace.js|`3a6dfc618ff7e7b238f2671dc85d65704f33093a18eac879d86081d92c31e8bc`|일치|
|all-in-one/registers/virtual-plc-test-results.json|`a6b389f797f9a8b5ffe6928b8420f55c4cc459a327b0b48d716079d2eca6dd64`|일치|

산출물: `extracts/RD01-FAN/research-check.json`, `source-hashes.json`, `selected-declarations.json`, `fan-declarations.json`, `network-map-selected.json`, 원본 지정 PDF 렌더/텍스트. 이들 정적 추출은 원본을 변경하지 않는다. 독립 2차 검토 및 사용자 전송·통합·게시 작업은 이번 작성자가 수행하지 않았다.
