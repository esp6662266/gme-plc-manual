# CLIENT-CL02 · Impactor — 고정 원본 자체 조사 초안

## 먼저 확인할 핵심

- 고유 입력은 IMPACTOR RUN `%I12.4`, IMPACTOR FAULT `%I14.7`이다. HMI `IMPACTOR_RUN`은 물리 I가 아닌 `DB13,X12.4`, 고장 래치는 `DB3.X14.2`이다.
- 직접 렌더한 FG88/PDF89, FG92/PDF93, FG128/PDF129, FG130/PDF131은 모두 **Rev2, 17.03.2025**이며 해당 IMPACTOR 채널은 **SPARE** 점선 범위에 있다. 백업 이름이 남아 있다는 사실로 현재 설치·사용을 확정하지 않는다.
- 고장 네트워크는 `ON AND FAULT → Set`, `ON AND NOT FAULT AND RESET_ALLARM → Reset`이다. 이 고유망에는 고장 지연 타이머·FB 호출·정지 출력이 없다. 외부 제어반 내부 고장/정지/복구 순서는 미확보다.
- 운전시간은 `Tag_47(T13) AND RUN` 허가로 MIN에 1을 더한다. 60 이상이면 HOUR에 **Move 1**하고 MIN을 0으로 쓴다. HOUR를 1씩 누적하는 Add로 바꿔 읽으면 안 된다. T17 조건의 별도 HOUR 0쓰기와 외부 누적 소유도 구분한다.
- CLIENT-CL02와 공압 CYL-CL02는 서로 다른 이름 공간이다. 현재 실물 동일성 확인, TIA 컴파일, CPU 비교, 현장 복구, 시뮬레이터 작업은 하지 않았다.
- 공유 근거: [SYS-PLC-IO](SYS-PLC-IO-DOTS-DRAFT.md)의 입력 Word 미러/호출 경계, [SYS-RUNHOURS](SYS-RUNHOURS-DOTS-DRAFT.md)의 공통 T13·T17·갱신 핸드셰이크, [SYS-ALARM](SYS-ALARM-DOTS-DRAFT.md)의 공통 집계/RESET/HMI 경계를 같은 고정입력에서 연결 재사용한다. 이번 고유 확인은 CL02 선언·핀·명령 미확보 경계·전기 4쪽·RUN 및 고장 HMI 주소다. 공통 설명을 CL02 전용 제어기로 복제하지 않는다.

## 1. 설비·자료 기준 — 적용 / 실물 근거 미확보

|항목|확인 및 경계|
|---|---|
|대상|catalog_id CLIENT-CL02, Impactor, client, 외부 연동, phase2, parent 없음; INVENTORY catalog index58. 이 문서만 한 ID로 집계|
|별칭|motor_client_02, client motor 2, cl02, impactor; CYL-CL과 병합 금지|
|기준|source-mv06, Git abcf31c5030bc7ef8749ed8e869a857f2387a28a, v1.12.0. 로컬 최신 버전/실제 CPU를 확인한 문서가 아님|
|범위|원본 XML·선언·HMI CSV·PDF 렌더 읽기 전용. 초안 첨부는 dot, 로컬 통합·검증·게시는 사용자/Codex만 담당. 원본 build/test/generator 및 PLC·보호값·SEJIN 변경 없음|
|시점|착수 2026-10-11 12:12:27 UTC, 고유 XML 대조 12:13:18, PDF 시각대조 12:13:27. 최종 해시·검사는 extracts/CLIENT-CL02/timeline.json 및 static-checks.json에 실제 시각 기록|
|모델|실제 모델 런타임 증명 미확인. 모델/추론 수준 선택을 이 문서로 입증하지 않음|
|자료 충돌|live_index 주석의 RUN `e 13.1`, FAULT `e 17.7`은 과거 주소 문자열. 선언 AO100/119 및 현 도면 E12.4/E14.7과 구분. 현재 설치 판정은 보류|

이 문서에서 `0221` 등은 `all-in-one/sources/decoded-original/0221-FlgNet.xml`을 뜻한다. doc411/1003은 검색 문서 번호이며 원본 파일 번호·실행순서·실제 TIA 페이지와 같지 않다. NID/UID/RID는 해당 파일/블록 문맥 안에서만 결속한다.

## 2. I/O·HMI — 적용

### 2.1 선언과 주소

|신호|원본 선언/문맥|형식·주소·해석|
|---|---|---|
|IMPACTOR FAULT|0599 SimpleAccess Global RID8, NID2 UID71/73, SSD.AO119, SAD Input|Bool I14.7, 외부 고장 원시 입력. PLC는 1을 고장 Set 조건으로 해석하지만 외부 접점의 현장 정상극성·단선검출은 미확정|
|IMPACTOR RUN|0613 SimpleAccess Global RID14, NID2 UID154, AO100, Input; 0558 RID30 Monitor도 AO100|Bool I12.4, 운전 응답 입력. 모터 회전/속도/접촉기 실제 상태와 동등함은 미확정|
|ON|0599 RID1/NID2 UID70, Memory AO0; Main0692 RID52도 AO0|M0.0 Bool. 이름 ON만으로 상수 true라고 단정하지 않음|
|Allarm.motor_client_02_fault|0601 Global RID9, NID2 UID72/75 Write, AO114 Bool; BAD4→0600 Allarm TOD3|DB3.X14.2 래치. 원시 I14.7과 다른 상태|
|Flag.RESET_ALLARM|0601 Global RID7, NID2 UID74, AO48 Bool; BAD6→0600 Flag TOD2|DB2.X6.0 내부 Reset 허가. HMI 버튼 이벤트와 곧바로 동일시하지 않음|
|CLIENT_MOTOR_2_MIN|0615 Global RID16, NID2 UID155/157/158/163, AO32 Int; BAD5→0614 TOD9|DB9.DBW4, 16-bit Int. UID157 Add 쓰기와 UID163 Move0 쓰기|
|CLIENT_MOTOR_2_HOUR|0615 Global RID18, NID2 UID161·NID47 UID2593 Write, AO48 Int|DB9.DBW6, Move1/Move0의 복수쓰기 대상|
|Tag_47 / Tag_48|0613 Global RID1 Timer AO13 / RID284 Timer AO17|T13/T17. 물리 I 또는 HMI bit가 아님|
|Flag_Aggiorna_DB|0613 Global RID13 Bool Memory AO15, NID2 UID164 Write|M1.7 공통 갱신요청; CL02 전용 영구 누적치가 아님|

본 고유망에서 위 피연산자는 Local이 아닌 Global이다. 정수 literal은 0616 Constant RID7=Int1, RID8=Int60, RID12=Int0로 NID2 해당 UID까지 대조했다. Global/Constant와 다른 블록 Local의 같은 UID를 섞지 않는다.

### 2.2 Word 미러와 HMI

0397/doc1070 입력 미러 NID1에서 ORef63/RID19(0627 Tag_183, Input Word AO96 = IW12) → W70 → Move60.in; Move60.out1 → W72 → ORef64/RID20(0629 Global Word AO96, BAD4/0628 DB13)이다. 따라서 **IW12→DB13.DBW12**이며 RUN bit12.4의 HMI 경로가 연결된다. 이어 Move60.eno → W71 → Move61.en, ORef65/RID21 IW14 → W73 → Move61.in, out1 → W75 → ORef66/RID22 DB13.DBW14이다. 원시 고장 I14.7 미러와 알람 DB3.X14.2 래치는 다른 값이다.

Word 복사 경로는 bit 개별 쓰기와 구분한다. 이 공통망에 다른 입력의 NOT/bit 쓰기가 존재하므로 DB13 전체의 무조건적인 raw 동일성·다른 Writer 부재를 주장하지 않는다. 입력 Word를 읽어 DB로 쓰며 물리 입력 강제나 주변부 PIW 접근이라고 바꾸지 않는다.

`all-in-one/sources/hmi_plc_tags.csv` 실제 행77 `IMPACTOR_RUN, DB13,X12.4, PLC, 00404`, 행572 `Allarmi_115, DB3,X14.2, PLC, 0011A`를 확인했다. 이는 dde.cfg 주소 설정 색인이다. 버튼/색상/팝업/ACK 이벤트·주기 스크립트·현재 통신·현장값은 미확보다. RUN과 alarm 두 항목을 운전 명령 또는 HOUR 누적 표시로 해석하지 않는다. DB9 직접 HMI 연결의 미확보 경계는 SYS-RUNHOURS와 공유한다.

## 3. 제어 구조 — 적용 / 외부 명령 경계 미확보

### 3.1 호출자와 명령 범위

0549/doc1620 Main NID7: Powerrail W352→Contact350.in, W348 ORef335/RID52 ON→operand, Contact350.out W351은 CRef319/322/325/328/331/334.en에 병렬 분기한다. CRef331 RefId80 안 CodeBlock345 RefId79는 0688의 **Motor/Alarm Client FC9**(NID7 UID345 Call)와 0694 RID80/NID7 UID331의 interface를 연결한다. CRef334 RefId83/CodeBlock347 RefId82는 **time work motor FC2**다. 이 둘의 실행 허가는 ON에 걸리며 앞 호출의 ENO 직렬 의존으로 읽지 않는다.

선정 원본과 live_index 심볼에서 CL02 전용 Start/Stop Q 명령, 전용 ready/permission handshake, 외부 fault reset Q를 결속하지 못했다. live_index의 `start client motor 4` Q61.2와 6/8/9/10의 출력 선언은 다른 채널로 보존한다. CL02의 출력이 시스템 어디에도 없다고 증명한 것은 아니며, 위 선언을 CL02에 복제하지 않는다. 도면의 외부 접점으로 들어오는 RUN/FAULT를 GME 모터구동 출력으로 뒤집지 않는다.

### 3.2 CL02 고장 Set/Reset 고유망

0221-FlgNet/doc411, motor/alarm client NID2, 6 Part/11 Wire:

|경로|원본 핀/해석|
|---|---|
|공통허가|W93 rail→Contact85.in, W76 ORef70/RID1 ON→85.operand; W86 85.out→87.in 및89.in|
|Set|W77 ORef71/RID8 FAULT→87.operand, W88 87.out→SCoil64.in, W79 ORef72/RID9→64.operand. ON∧FAULT이면 DB3.X14.2 Set|
|Reset|Contact89의 operand에 Negated 명시; W80 ORef73/RID8→89.operand; W90 89.out→Contact91.in; W81 ORef74/RID7 RESET→91.operand; W92 91.out→RCoil69.in; W83 ORef75/RID9→69.operand. ON∧¬FAULT∧RESET이면 같은 bit Reset|

원인이 계속 1인 동안 Reset만으로 이 경로의 래치는 내려가지 않는다. FAULT가 0으로 돌아오는 것만으로 자동 해제되지 않는다. ON이 0이면 본 두 쓰기 경로는 성립하지 않는다. 다른 Word/간접/외부 쓰기와 실행순서까지 폐쇄 검증한 것은 아니다. 고유망에는 TON/SD·시간상수·Coil Q·CRef가 없으므로 주변 모터의 2초/7초 fault delay를 가져오지 않는다.

### 3.3 CL02 운전시간: 단순 누적 HOUR가 아닌 전달 구조

0293/doc1003, time work motor NID2, 7 Part/18 Wire. W186 rail→Contact182, W165 ORef153/RID1 T13→182.operand; W183 182.out→Contact184, W166 ORef154/RID14 RUN→184.operand. W185 184.out은 Add136.en과 Ge143.pre에 병렬로 연결된다.

- Add136 SrcType Int: W167 ORef155/RID16 MIN→in1, W168 ORef156/RID7 Int1→in2, W169 out→ORef157/RID16 MIN. RUN·T13 접점 허가 아래 MIN+1 쓰기.
- Ge143 SrcType Int: W170 MIN ORef158→in1, W171 Int60 ORef159→in2; out W172→Move146.en.
- Move146.in W174/ORef160/RID7은 Int1. out1 W175→ORef161/RID18 HOUR. **HOUR←1**이며 HOUR+1이 아니다.
- Move146.eno W176→Move149.en. W177/ORef162/RID12 Int0→Move149.in, out1 W178→ORef163/RID16 MIN. 다음 eno W179→SCoil152.in, W180/ORef164/RID13 M1.7에 Set.
- Add136의 ENO를 Ge143.pre에 잇는 경로가 아니다. 공통 W185와 후속 Move의 ENO를 구분하며 실제 scan 내 값 갱신/overflow/CPU 동작을 시험했다고 하지 않는다.

0332/doc1045/NID47에는 T17(0613 RID284, ORef2589)→W2600→Contact2615, out W2616→첫 Move2574.en 이후 **W2603 첫 Move.eno→CL02 Move2577.en**이 있다. CL02 입력은 W2604/ORef2592/RID12 Int0, 출력은 W2605/ORef2593/RID18 DB9.DBW6다. 따라서 HOUR에는 별도 0쓰기 또한 존재한다. 같은 망의 CLIENT1/3/4/5는 관련 범위일 뿐 이 문서의 완료 설비가 아니다.

T13의 생성은 0019/doc1056/NID58, `NOT T13 → SdCoil3112`, value ORef3114/RID335 `S5T#1M`이며 W3117(value)/W3119(operand), W3121(Contact3120.out→in)으로 확인한다. T17 5초와 갱신요청/M2.0 기억의 0341 공통 흐름은 SYS-RUNHOURS 참조. T13은 고장 타이머가 아니고 T17도 CL02 재기동 지연이 아니다. 외부 M1.7 소비·누적 저장과 한 분 정확도, 전원차단 유지, 현재 정비주기는 미확정이다.

## 4. 전기 전달 경로 — 입력 회로 적용 / 외부 제어반 미확보

원본 `all-in-one/sources/Electrical_Rev2.pdf`를 직접 렌더했다. 표 아래 값은 도면 판독이며 현행 보호값 확인이나 변경 지시가 아니다.

|원본 FG / 실제 PDF|직접 시각 확인한 양 끝점|표제/개정·경계|
|---|---|---|
|FG88 / PDF89|+24Vdc 10.7(87/9→89/0) → 5×20 2A F 표시 → X1:286 → 선표시88.2 및 외부 NO형으로 그린 접점 → X1:287 → E12.4 → 교차참조128/5|DIGITAL INPUT FROM CLIENT MACHINE, IMPACTOR RUN. SPARE 점선 안. Rev2 17.03.2025, DATA27.05.2024|
|FG128 / PDF129|E12.4의 88/3 참조 → DIGITAL INPUT MODULE 표 terminal5 / CPU515 / MOD11 / IMPACTOR RUN|SPARE 구역. Rev2 17.03.2025, DATA27.05.2024. CPU515는 도면 표기이지 현재 CPU 실물검증이 아님|
|FG92 / PDF93|+24Vdc10.7(91/9→93/0) → 5×20 2A F 표시 → X1:324 → 선표시92.1 및 외부 NO형 접점 → X1:325 → E14.7 →130/7|DIGITAL INPUT FROM CLIENT MACHINE, IMPACTOR FAULT. SPARE 점선 안. Rev2 17.03.2025, DATA27.05.2024|
|FG130 / PDF131|E14.7의92/1 참조 → module terminal28 / CPU515 / MOD11 / IMPACTOR FAULT|SPARE 구역. Rev2 17.03.2025, DATA27.05.2024|

탐색 경계로 직접 렌더한 FG86/PDF87 및 FG87/PDF88은 BWF01/02 입력이며 개정란 공란, DATA27.05.2024이다. 이를 CL02 입력으로 복제하지 않는다. FG89~91·93~95 전체의 시각검토 완료를 주장하지 않는다.

CL02의 이 두 회로에는 GME KA 릴레이 부하5/9 또는 하단 접점표1/5/9가 제시되지 않는다. 다른 설비의 KA 접점을 덧붙일 근거가 없다. NO형 도면 기호는 무전압 정상상태/가동 시 정상극성/선로 단선진단을 단독 입증하지 않는다. 외부 제어반 접점 번호·공급원/절연·케이블 번호·심선색·접촉기/인버터·모터 전원·보호기 설정·현행 명판은 미확보다. GME X1–DI 양 끝점 이후를 추정하지 않는다.

## 5. 알람·복구 — 문서 적용 / 현장 미확보

1. 외부 원인 상태 I14.7, PLC 기억 DB3.X14.2, HMI Allarmi_115를 분리한다. RUN I12.4와 FAULT I14.7은 독립 입력이므로 둘이 동시에 1/0인 관찰을 임의 정상/불능으로 확정하지 않는다.
2. 고장 Set/Reset 조건은 3.2의 원본 그대로다. 알람 래치에 고유 지연은 없다. ON 또는 호출 중단은 외부 고장 해소가 아니다.
3. 공통 alarm word 집계·사이렌·ACK/RESET 신호 생성은 SYS-ALARM의 동일원본 연결을 사용한다. 해당 공통 기능을 CL02 전용 모터 정지 출력이라고 하지 않는다. 본 조사에서 CL02 전용 정지·재기동/재허가 출력을 결속하지 못했다.
4. 외부 고장 원인 해결, I14.7 복귀, Reset 요청, DB3 래치 해제, 화면 갱신, 재기동, 실제 회전 확인은 각각 다른 단계다. 현장 승인 절차·보호조건을 확보하지 않았으므로 강제 입력·접점 우회·전원 재투입·보호값 변경 등 조작 절차를 제안하지 않는다.

## 6. 증상별 관찰 — 승인 전 문서 점검안

|증상|읽기 전용으로 필요한 동시점 증거|원본 비교 및 보류|
|---|---|---|
|HMI RUN이 안 켜짐|관찰 시각/시간대, 실제 모터 상태의 승인된 관찰, I12.4, IW12, DB13.W12/X12.4, 통신상태|FG88/128 및0397 미러; 단자/미러/HMI를 분리. SPARE와 현재 사용 여부 먼저 확인|
|FAULT 표시가 계속 남음|I14.7, ON, FC9 호출허가, DB2.X6.0, DB3.X14.2, Allarmi_115|0221 S/R 조건. 원인 0만으로 래치가 풀리지 않음. 외부 원인 제거/RESET 이벤트 미확보|
|입력은 0인데 화면 alarm 1|같은 시각 원시 FAULT·래치·HMI 주소와 과거 발생 시각|래치 유지 또는 표시/통신 지연을 구별; 값 하나로 PLC 고장 단정 금지|
|운전시간 MIN 불변|FC2/ON·T13·I12.4·DB9.DBW4|0293의 en/pre 및0019. 타이머 접점·입력·호출 원인을 구분; 실제 운전시간 누적 검증 아님|
|HOUR가1 또는0으로 보임|DB9.DBW6, MIN, M1.7, T17, 외부 누적 저장 기록|0293 Move1과0332 Move0. 수리 필요나 오버플로로 곧바로 단정 금지|
|명령을 보냈다고 하나 기계 무응답|요청을 만든 시스템·대상 Q/통신 경로·외부 제어반 판본|CL02 전용 GME 명령 결속 미확보. 다른 client Q61.2를 대신 사용하지 않음|

관찰 기록은 ID, 관찰자, 시각/시간대, 원본/현재 프로젝트 판본, 위치/주소, 값·단위, 장치/방법, 비교 근거, 배제 결과, 승인 조치, 복구 증거를 구분한다. 빈칸은 미확보이며 0과 다르다. 실제 사진/사용자 운영 이력은 이 공개용 초안에 복제하지 않았다.

## 7. 완료·누락과 후속 인계

|상태|판정|
|---|---|
|documentation|complete_with_gaps: 고유 원본 7영역 초안. 외부 제어반/현행 실물 미확정|
|static_review|selected_source_review_complete: 원본 선언/핵심 Part·Wire·PDF6쪽 시각검토 및 선정26파일 SHA/Gitblob 일치. XML 전체/전체 PLC 전수 의미검토 아님|
|ui_records|not_run: 나란히보기·선택백업복원·전후비교·보고서 생성/UI/저장 재열기 검증 미수행|
|publication|not_published: 부모 첨부 예정 초안. 로컬 2차 통합·Git push·운영 반영 없음|
|tia_compile / live_cpu / field_recovery|모두 not_performed|
|simulator|영구중지 유지: 생성·수정·실행·행동시험 없음|

필요 자료는 ① SPARE 도면 채널의 현재 사용 여부/실물명판 및 CL02 식별, ② 외부 제어반 승인 회로와 RUN/FAULT 접점·케이블 양 끝점, ③ 현재 PLC 프로젝트의 해당 선언/호출/Writer 및 입력 미러, ④ HMI 위젯/알람/Reset 실제 이벤트, ⑤ 운전시간 외부 누적·M1.7 소비와 현재 유지주기 증거다. 새로운 자료가 없으면 이 보류를 반복 전검색하지 않는다. 안전한 현장 관찰/복구는 담당자 승인 및 적합한 절차 확보 후 별도다.

### 선정 원본 전체 SHA256 및 고정 Git blob 대조

아래26개는 이 초안의 선정 입력이다. 해시 개수는 의미검토한 회로/네트워크/설비 수가 아니다. PDF 파일 전체 해시는 같아도 실제 시각검토는 위6쪽으로 한정한다. 파생 live_index/network-map/CSV는 탐색·주소설정 보조이고 핵심 조건의 근거는 XML 및 도면이다. 검사 JSON과 SHA JSON은 `extracts/CLIENT-CL02/`에 보관한다. 원본 Git 상태 clean을 확인했고 어떤 원본도 쓰지 않았다.

|원본 상대경로(source-mv06 기준)|SHA256|고정 커밋 Git blob|바이트 대조|
|---|---|---|---|
|docs/equipment-standard/INVENTORY.json|720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc|587c3748ad9224718f95ba06463fee913dae231d|일치|
|all-in-one/sources/Electrical_Rev2.pdf|5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6|f610fd7c7ce14ae951b00cff57b969259bfb389d|일치|
|all-in-one/sources/hmi_plc_tags.csv|a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404|cf4c0650e7c7baac350dcb89909b808435704880|일치|
|all-in-one/sources/live_index.json|14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1|e35ccea1f841349c632666c29954b7bcd4f5839e|일치|
|all-in-one/sources/decoded-original/network-map.json|c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60|424430b6b953e43138e5d0a18ca40c949e21cfa1|일치|
|all-in-one/sources/decoded-original/0221-FlgNet.xml|112333900f566632a1b9207ff123b7a66f5a49be0e299ef24d2ee44f1c34542b|d0e9f8b8d735c7a8ba531d9f86ee485cae18ccab|일치|
|all-in-one/sources/decoded-original/0293-FlgNet.xml|e63ffe5d62c91b8d9c664fc9935f4f8144f68d598f643e7d00d4127da8f00500|37cd6c09f676682b2ad7589f828d0af8e3c7039e|일치|
|all-in-one/sources/decoded-original/0332-FlgNet.xml|c677499004010aba2746412a08e32f3e4206e9212d481fc08ee1c6023326cef7|50e3451e01b63fb9311aade1c4bfefa0719d305b|일치|
|all-in-one/sources/decoded-original/0019-FlgNet.xml|a3301f4d07c2d36aefa6faa6c3559a1cff4565fc6de40cd17e54b548b30c0ce5|f78cfdbf5e717304114660ffbd3bb42cbed6d79d|일치|
|all-in-one/sources/decoded-original/0341-FlgNet.xml|e9921cb52ecba4ef1df14758d29e4091fc510a8e792130e855b869dbab4a1c96|45dbda06a692b21380a52207a22094b2e0a9c5a3|일치|
|all-in-one/sources/decoded-original/0397-FlgNet.xml|bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834|4ab8370493c4e28fc1eabeeebe2743d27f0c4021|일치|
|all-in-one/sources/decoded-original/0549-FlgNet.xml|49f7169c33ed7f54559b0801e21a7d618584900972840e91cf51ad032e8febb1|985b5310b43b1015b5dee286aa0e42800564b94b|일치|
|all-in-one/sources/decoded-original/0558-IdentXmlPart.xml|45d49d53b6b41312960bb2a329663e87d8803e28d7832308424a6bf5091e6d1b|a0b681bd15e9ae15f2e1437576a4486cc732fdf2|일치|
|all-in-one/sources/decoded-original/0599-IdentXmlPart.xml|32a693fe12134febbd9f5c7da10c3469ef4d5b164ab8b6bd9ea3867c358936c1|493de77fc827d8f14192ced05d82df3a062f7965|일치|
|all-in-one/sources/decoded-original/0600-IdentXmlPart.xml|20c58ee0383d0b6c275bd2d96abd30af7c5d1f3fff59c7d5034cd758936b57d5|f22a7ededd0576cf379ee19908da067f08d45412|일치|
|all-in-one/sources/decoded-original/0601-IdentXmlPart.xml|04c9481f7381284de689ef5c7ff40d7aea93f2004cd877a4e4f27e47baa6d862|07bcf656fa58e4a305999456644acd24b3dc6bec|일치|
|all-in-one/sources/decoded-original/0613-IdentXmlPart.xml|09d3b1397a987898334218f37e025661af162438582e649f671e7abec443d3cb|c9d19a48e947098914f4d2de3348c05b4f6d37e8|일치|
|all-in-one/sources/decoded-original/0614-IdentXmlPart.xml|c6de26f74d75f5be858a406de75eaf6faf62ba9b89c8f9a085b5dd206e93d294|da0485aa033700f08c8695d30b93ebd2d377d6c7|일치|
|all-in-one/sources/decoded-original/0615-IdentXmlPart.xml|80f4544edca56c6e6bb2713c758c92ade9202255110074931e03fe34d0d0801a|49eb86fe01feb83de8c0864b21493d305aff8b20|일치|
|all-in-one/sources/decoded-original/0616-IdentXmlPart.xml|650b53354a0c8443d94adc5bd6a860d3c5313014a52e0fb98a5656a65b58cc0d|9f7fdd5f93ac149c139a054ebb34f63c632ef7fd|일치|
|all-in-one/sources/decoded-original/0627-IdentXmlPart.xml|08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb|61ebc0abbb2ca160e11e1da400a3f14a397d8bc5|일치|
|all-in-one/sources/decoded-original/0628-IdentXmlPart.xml|9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd|170ca5c72599edc7ea7eefe651c3680ce325e76a|일치|
|all-in-one/sources/decoded-original/0629-IdentXmlPart.xml|67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972|058129bb01e27f7a6a0d0293f332d745e5bab74e|일치|
|all-in-one/sources/decoded-original/0688-IdentXmlPart.xml|ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda|463585759f1ecd94f32362b4fefb000a152f5773|일치|
|all-in-one/sources/decoded-original/0692-IdentXmlPart.xml|bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037|737785d03b5fad43c5b4d451955726d800edb1c0|일치|
|all-in-one/sources/decoded-original/0694-IdentXmlPart.xml|757ccebdf32d0a168dd787bfa735fe6494eac4c4a9f7a5adc63898a88e8b152d|c45e8f3ca4129dc06734f6a12ef79e6ed6528a7d|일치|