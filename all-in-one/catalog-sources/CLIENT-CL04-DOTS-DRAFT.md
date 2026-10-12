# CLIENT-CL04 Belt conveyor A 자체 원본 조사 초안

## 먼저 확인할 핵심과 경계

- 고유 catalog ID는 CLIENT-CL04 한 개다. 외부 Belt conveyor A 채널이며 공압 CYL-CL04, GME BC01과 병합하지 않는다.
- RUN은 백업 I12.6, FAULT는 I15.1이다. 각 원본 선언과 실제 OEM 도면 FG88/PDF89, FG92/PDF93 및 PLC 입력 FG128/PDF129, FG131/PDF132를 직접 대조했다.
- **명령 연결 공백:** 백업 심볼 `start client motor 4`는 Q61.2이지만, 해당 이름의 원본 XML 쓰기/호출 핀 및 OEM 출력 회로 끝점은 확보하지 못했다. 이 선언만으로 PLC가 현재 외부 컨베이어를 기동한다고 쓰지 않는다.
- **도면과 설명의 상충:** RUN 심볼 설명의 과거 `e 13.3`과 실제 주소 I12.6, FAULT 설명의 `e 18.1`과 실제 주소 I15.1을 구분한다. Rev2 도면에는 해당 회로를 둘러싼 SPARE 점선이 있다. 이름/접점 도해는 실제 배선·사용 확인을 대신하지 않는다.
- **고장과 시간계수의 소유 분리:** 0223은 고장 래치, 0295는 RUN을 참조한 시간계수다. 0295의 HOUR 쓰기는 누적 ADD가 아닌 **Move 1**이고 별도 0332에서 Move 0이 있다.
- 공유 근거는 같은 고정입력의 [SYS-RUNHOURS](SYS-RUNHOURS-DOTS-DRAFT.md) 공통 타이머·저장 핸드셰이크, [SYS-ALARM](SYS-ALARM-DOTS-DRAFT.md) 공통 Reset·경보 집계, [SYS-PLC-IO](SYS-PLC-IO-DOTS-DRAFT.md) 입력미러 호출 및 [SYS-HMI](SYS-HMI-DOTS-DRAFT.md) 이벤트 미확정 경계를 연결 재사용했다. 이번 고유 채널 선언, Part/Wire, HMI 주소 및 전기 끝점은 독립 확인했다.

## 1 설비와 자료 기준

대상은 `docs/equipment-standard/INVENTORY.json#/catalog/60`의 CLIENT-CL04, 이름 Belt conveyor A, kind client, 외부 연동, 부모 없음, phase2다. 기준은 고정 읽기 전용 `source-mv06`, Git `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, v1.12.0이다. 로컬 후속 릴리스의 구현이나 게시 상태를 조사한 문서가 아니다.

원본 약칭 NNNN은 `all-in-one/sources/decoded-original/NNNN-FlgNet.xml` 또는 같은 번호의 IdentXmlPart.xml을 뜻한다. document_id와 NID, 파일번호를 혼용하지 않는다. XML은 백업 정적 근거이며 온라인 CPU 프로젝트가 아니다. `live_index.json`과 network-map은 바이너리에서 추출한 색인으로, 원형 XML이 있는 핵심은 선언·핀을 재확인했다. Q61.2는 현재 확보범위에서 색인 선언 수준이다.

- 착수 실제시각: 2026-10-11 12:12:50 UTC
- 고유 XML 및 실제 도면 대조: 12:13~12:14 UTC의 실행 기록
- 해시·검사 JSON 기록: 2026-10-11 12:15:21.655563 UTC; JSON에 실제 ISO시각 보존
- 실행 모델/추론 런타임 증명: 미확인
- 원본 Git 상태: 조사 중 `git status --short` 출력 없음. 원본·공통코드·공개대장·운영기록·보호값 변경 없음. 원본 build/test/generator 및 시뮬레이터 실행 없음.

## 2 I/O와 HMI

### 고유 선언 결속

|대상|원본 선언 및 문맥|주소·형식과 해석|
|---|---|---|
|BELT CONVEYOR A RUN|0613 RID26, Global, NID4 UID262; SSD AO102, SAD Input SAM=None|I12.6 Bool 입력영상. 실제 벨트 움직임 자체의 증명은 아님|
|BELT CONVEYOR A RUN 모니터|0558 RID32 NID -2147483648 UID45, AK Monitor, AO102|별도 모니터 선언이며 제어 쓰기 아님|
|BELT CONVEYOR  A FAULT|0599 RID12 Global NID4 UID107/109, AO121, SAD Input SAM=None|I15.1 Bool; 두 공백 원문도 동일 문맥으로 결속|
|start client motor 4|live_index segment _7ev doc480 Name/Address/Datatype/Comment|Q61.2 Bool, comment `it should be free but it is used`; XML 선언/쓰기 미확보|
|Allarm.motor_client_04_fault|0601 RID13 Global AO116 Bool, BAD4 →0600 RID4 TOD3; NID4 UID108/111 Write|DB3.DBX14.4, 내부 유지 경보|
|Flag.RESET_ALLARM|0601 RID7 Global AO48 Bool BAD6 →0600 RID6 TOD2; NID4 UID110|DB2.DBX6.0 공통 내부 Reset. HMI 버튼 그 자체가 아님|
|ON|0599 RID1 Global AO0 SAD Memory; NID4 UID106|M0.0 Bool. 이름 ON을 상수 true로 치환하지 않음|
|CLIENT_MOTOR_4_MIN|0615 RID28 Global Int AO96 BAD5 →0614 RID5 TOD9; NID4 UID263/265/266/271|DB9.DBW12 Int, ADD 및 Move 0 writer|
|CLIENT_MOTOR_4_HOUR|0615 RID30 Global Int AO112 BAD5; NID4 UID269, NID47 UID2597 Write|DB9.DBW14 Int, Move 1/Move 0. 단순 누적시간 레지스터로 설명 금지|
|Tag_47 / Flag_Aggiorna_DB|0613 RID1 Timer AO13 / RID13 Bool Memory AO15|T13 / M1.7. HMI 태그와 구분|

이 핵심 채널의 직접 선언은 Global이고, 1·60·0·S5T#1M은 Constant다. 동일 RID/UID 숫자를 다른 블록의 Local 변수나 다른 NID와 결속하지 않았다.

### HMI 데이터 경로

`all-in-one/sources/hmi_plc_tags.csv`에는 `BELT_CONVEYOR_A_RUN`, 주소 `DB13,X12.6`, 내부 ID00402, Access Name PLC가 있다. 이는 설정 주소이며 클릭 이벤트·현재 통신·표시 정확성 증거는 아니다.

0397 HMI Inputs NID1의 Move60은 rail W21로 en을 받는다. ORef63/RID19(0627, Tag_183, Word Input AO96, SAM=None = IW12)가 W70→Move60.in, out1 W72→ORef64/RID20(0629 Global Word AO96, BAD4→0628 TOD13 = DB13.DBW12)로 전달된다. 즉 **Word 전체 복사**가 I12.6을 포함하는 DB13 바이트 범위로 전달한다. 별도 Bool 코일 쓰기나 PIW 직접접근으로 바꾸지 않는다. Move60.eno W71→Move61.en도 원문에 존재한다. FC15의 상위 호출과 다른 writer/스캔 최종값은 SYS-PLC-IO의 공통 경계를 따른다.

동일 CSV의 `Allarmi_117` 주소 `DB3,X14.4`, ID00118은 내부 유지경보와 같은 주소다. 경보 번호117은 태그 이름이며 물리 입력번호/외부 제어반 오류코드를 뜻하지 않는다. CSV의 DB9 직접 태그는 이번 검색에서 없었다. Q61.2 버튼·ON/OFF 이벤트·허가·권한·통신 writer는 확보하지 못했다. `0401-FlgNet.xml`은 Q→DB14 미러라는 공통 근거를 참고할 뿐, 이를 Q61.2 기동 명령으로 설명하지 않는다.

## 3 제어 구조

### 호출 경계

0549 Main document1620, NID7에서 W352 rail→Contact350.in, ORef335/RID52→W348→operand다. 0692 RID52의 ON이 허가하며 Contact350.out W351은 여러 CRef의 en으로 병렬 분기한다.

- CRef331 RefId80 내부 CodeBlock345 RefId79. 0688 RID79 `Motor/Alarm Client` TOD9, NID7 UID345 Call; 0694 RID80 NID7 UID331 TORID79와 결속한다.
- CRef334 RefId83 내부 CodeBlock347 RefId82. 0688 RID82 `time work motor` TOD2, NID7 UID347 Call; 0694 RID83 NID7 UID334 TORID82와 결속한다.

앞 블록의 ENO가 순차 직렬로 성공해야 두 FC가 호출되는 배선이 아니다. 백업 Main 허가 구조이며 실제 스캔주기·CPU 실행은 미확정이다. 별도 모터 제어 FB에 CL04가 실제 호출된다고 추정하지 않는다.

### RUN을 사용하는 시간계수 고유 경로

0295 document1005, FC2 NID4:

1. T13 ORef261/RID1 → W273 → Contact290, RUN ORef262/RID26 → W274 → Contact292. Contact290.out W291→292.in. 292.out W293은 Add244.en 및 Ge251.pre로 분기한다.
2. Add244 `SrcType=Int`, in1 W275/ORef263=DB9.DBW12, in2 W276/ORef264/RID7=Int1, out W277/ORef265=같은 MIN. 이 단계만 MIN+1이다.
3. Ge251 Int는 in1 W278/ORef266=MIN, in2 W279/ORef267/RID8=60. out W280→Move254.en.
4. Move254.in W282/ORef268/RID7=1, out1 W283/ORef269/RID30=HOUR. **HOUR := 1**이다. `HOUR := HOUR+1`로 바꾸지 않는다.
5. Move254.eno W284→Move257.en; in W285/ORef270/RID12=0; out1 W286/ORef271/RID28=MIN. 이어 Move257.eno W287→SCoil260.in, operand W288/ORef272/RID13=M1.7을 Set한다. ENO 의존을 유지한다.

0019 document1056, FC2 NID58의 Contact3120는 operand NOT(T13, ORef3115/RID1/W3118). out W3121→SdCoil3112.in, value W3117/ORef3114/RID335는 0616의 S5Time `S5T#1M`(인코딩 V5632), operand W3119/ORef3116은 T13다. 이것은 공유 분 타이머 근거이며 CL04 기동지연/무응답 고장 타이머가 아니다. CPU 주기와 실시간 정확도는 확인하지 않았다.

0332 FC2 NID47의 HOUR Reset도 독립 확인했다. T17 ORef2589/RID284 →W2600→Contact2615→W2616→Move2574.en 이후 Move2577,2580의 ENO 체인을 거쳐 W2609→Move2583.en. Move2583.in W2610/ORef2596/RID12=0, out1 W2611/ORef2597/RID30=CLIENT_MOTOR_4_HOUR에 0을 쓴다. 다른 CLIENT 필드도 같은 네트워크지만 그 설비의 조사 완료로 세지 않는다. T17/M1.7/M2.0의 저장 핸드셰이크·외부 ACK 미확보는 SYS-RUNHOURS 공통 상세를 따른다. HOUR 0/1만으로 정비기록 저장 성공·분실을 판정하지 않는다.

### 명령·정지 소유의 미확정

명명 검색은 decoded-original의 IdentXmlPart 181개에서 수행했으며 CL04 관련 선택 선언 hit는 6개다. Q61.2 심볼 이름의 직접 선언이 없었고 Output AO490(bit Q61.2), AO480/488(범위 후보)도 이번 선택 조회에서 결속되지 않았다. live_index doc480의 심볼 존재를 쓰기 회로 존재로 바꾸지 않는다. 다중 writer·절대주소/간접주소·블록 복사까지 부재를 증명한 것은 아니다. 기동/정지/수자동/외부준비/인터록 전체 원문과 외부 제어반 프로그램이 추가로 필요하다.

## 4 전기 전달 경로

원본 `all-in-one/sources/Electrical_Rev2.pdf`를 실제 PDF 페이지 89·93·129·132로 렌더하고 눈으로 확인했다. **네 페이지 모두 footer Rev2 17.03.2025, DATA 27.05.2024**이며 FG와 PDF를 각각 기록한다. 파일명 Rev2만 보고 모든 페이지의 개정란을 추정하지 않았다.

|구분|직접 확인한 실제 끝점·접점·페이지|미확정|
|---|---|---|
|RUN 외부 접점|FG88/PDF89, BELT CONVEYOR “A” RUN: +24Vdc10.7 → 5x20 2A F 퓨즈 표기 X1:290 → 선88.4 → 그려진 열린 접점 → X1:291 → E12.6 /128/6|외부 접점 기기번호·상대 제어반 단자·케이블번호/규격 없음. 정상극성·실제 연결 미확정|
|RUN PLC 입력|FG128/PDF129: E12.6, 상호참조88/6 → 입력 모듈 단자7; 표기 CPU515 / MOD11; BELT CONVEYOR “A” RUN|도면의 CPU/MOD 표시이며 현재 CPU 모델/실물 설치 증명 아님|
|FAULT 외부 접점|FG92/PDF93: +24Vdc10.7 → 5x20 2A F 퓨즈 표기 X1:328 → 선92.3 → 그려진 열린 접점 → X1:329 → E15.1 /131/2|외부 고장 접점의 실제 논리/정상상태·고장코드 미확정|
|FAULT PLC 입력|FG131/PDF132: E15.1, 상호참조92/4 → 입력 모듈 단자32; CPU515 / MOD11|외부 장치 내부 보호회로와 별개|
|모듈 보조전원|같은 FG131: +24Vdc10.7 → X21:3013의 5x20 2A IST. → 선131.1 → 단자39, -0Vdc10.6→단자40|그린 도면 정격이며 현행 퓨즈/보호설정 추천 아님|
|기동 출력|Q61.2는 백업 심볼만 확인. OEM 페이지 텍스트 및 고유 채널 검색에서 A61.2/CL04 기동 회로 미식별|릴레이명·코일 A1/A2·부하접점·단자·외부모터 전력·컨택터·보호기 미확보|

RUN/FAULT 입력에는 열린 접점 기호가 그려져 있지만 현장 정상극성, 무전압상태의 안전성, 고장 시 접점 동작을 확정하지 않는다. 네 도면의 해당 범위에 SPARE 점선이 있어 실사용 대조가 특히 필요하다. 이 페이지는 릴레이 부하접점5/9나 하단 접점표1/5/9 회로가 아니므로 다른 설비의 숫자를 복제하지 않는다.

`Electrical_Can_Decoating_20241118.pdf`의 기존 페이지 텍스트에서도 Belt conveyor A 고유 외부 제어반 결속을 찾지 못했다. 이번 시공 PDF 실물 렌더는 수행하지 않았으며 도면 전수 의미검토를 주장하지 않는다. 케이블과 외부 제어반 도면이 새로 들어오기 전 추측 연결이나 반복 검색을 하지 않는다.

## 5 알람과 복구

0223 document413, `Motor/Alarm Client` NID4의 직접 경로:

- ON ORef106/RID1 → W112 → Contact121. Powerrail W129→121.in, 121.out W122가 Set/Reset 두 가지로 갈린다.
- Set: I15.1 ORef107/RID12 →W113→Contact123, out W124→SCoil100.in, operand W115/ORef108/RID13=DB3.X14.4. 따라서 `ON AND FAULT`일 때 경보 Set.
- Reset: I15.1 ORef109/RID12 →W116→Contact125(operand Negated), out W126→Contact127.in, RESET_ALLARM ORef110/RID7→W117→127.operand, out W128→RCoil105.in, operand W119/ORef111/RID13=같은 경보. 따라서 `ON AND NOT FAULT AND RESET_ALLARM`일 때 Reset.

이 네트워크에는 타이머 Part가 없다. 다른 장치의 3초/5초 무응답 타이머를 넣지 않는다. 원인이 계속 참이면 Reset 조건은 성립하지 않는다. RUN=0을 이 경보의 직접 원인으로 바꾸지 않는다. 고장 소멸·PLC 래치 해제·HMI ACK·외부 제어반 Reset·재기동·현장 복구는 서로 다른 상태다.

Allarmi_117은 DB3.X14.4 설정 주소로 결속되지만 실제 표시 문자열·경보이력·소리·ACK 이벤트를 확보하지 못했다. 공통 DB3 집계와 Reset 생성은 SYS-ALARM을 참조한다. 이 한 비트가 외부 모터를 직접 정지시키는 writer 경로는 확인하지 못했으므로 정지 인과를 추가하지 않는다.

## 6 증상별 읽기 전용 관찰

현장 조작법이 아니라 승인된 담당자가 제공할 관찰 자료의 비교 기준이다. 강제출력·바이패스·보호값 변경·활선 점검이나 Reset 실행을 제안하지 않는다.

|증상|같은 시각에 남길 값/위치|원본 비교와 판단 한계|
|---|---|---|
|시작 표시인데 벨트 정지|화면·버튼 이벤트, 현재 프로젝트 식별, Q61.2 값/실제 writer, 외부제어반 상태, I12.6|Q61.2 이름만으로 출력을 실제 모터전원에 결속하지 않음. 외부 도면/명판/케이블표 필요|
|외부 운전중인데 HMI RUN 없음|I12.6, IW12, DB13.W12/X12.6, HMI ID00402, 이벤트 시각|FG88 X1:290/291 및 FG128 단자7과 0397 Word 경로를 분리. 단선/통신고장/실물극성을 단정하지 않음|
|FAULT가 사라졌는데 경보 유지|I15.1, ON, DB2.X6.0, DB3.X14.4, HMI Allarmi_117|0223 래치 유지·Reset 조건 확인. 외부 원인 소멸만으로 자동 해제되는 식이 아님|
|Reset 요청에도 유지|현재 I15.1, 내부 Reset 전후, HMI 요청·소비 로그|NOT FAULT 조건과 공통 Reset 생성 구분. 반복 재기동으로 해결했다고 쓰지 않음|
|시간계수가 늘지 않음/1에서 멈춤|I12.6,T13,DB9.W12/W14,M1.7,T17,외부 저장내역|0295 MIN+1/HOUR Move1 및 0332 Move0, 외부 장기누적을 분리. 운전시간 정확도/기록 저장 미확정|
|도면 주소와 심볼 설명이 다름|자료 개정·CPU 프로젝트·X1/모듈 표찰·외부회로 사진|과거 e13.3/e18.1 설명과 현재 백업 주소를 별도 열로 보존. 임의 배선 수정 금지|

관찰기록에는 관찰자, 실제시각/시간대, 위치, 값/단위, 프로젝트·도면 판본, 장치, 사진/로그 출처, 비교결과, 미확정 사항을 남긴다. 실제 운영/SEJIN 기록은 이번 문서로 복제하지 않았다.

## 7 완료 기준과 누락

|영역|상태|잔여 조건|
|---|---|---|
|설비·자료 기준|적용, 문서 작성|CLIENT-CL04 실물 동일성 미확정|
|I/O·HMI|적용, 입력·알람·시간 선언 확인|명령 XML, HMI 이벤트·현재 통신 미확보|
|제어|적용, FC9/FC2 및 채널 선택 의미검토|모터기동/정지 writer·외부 시퀀스 미확보|
|전기 끝점|입력 두 경로 실제 렌더 확인|출력·상대 제어반·케이블·실물 미확보|
|알람/복구|고유 S/R 확인|HMI ACK/외부 Reset·현장복구 미확인|
|증상 관찰|읽기 전용 비교기준 작성|현장 관찰값 미취득|
|완료·누락|문서와 구현/현장 분리|BC01 동등 기능완료 또는 게시완료 아님|

추가자료는 현재 외부 Belt conveyor A 제어반 회로 및 PLC 프로그램/기동 허가표, GME Q61.2 교차참조·간접쓰기 포함 writer, X1:290/291/328/329 상대 단자와 케이블표, 현행 HMI 이벤트·스크립트, 명판/회로 개정 및 RUN/FAULT 정상상태 증거다. 새 자료 없이 동일 실물 보류를 반복 조사하지 않는다.

네 기능은 도면·래더 비교용 근거만 준비했다. 백업 미리보기/선택복원, 기록 전후비교, 관찰보고서/PDF의 이 ID 전용 구현·저장/재읽기·화면 재열기는 실행/검증하지 않았다. 기존 note/repair_observation/미지필드/초안/저장키 변경 없음.

최종 상태: documentation `complete_with_gaps`; static_review `selected_original_xml_and_pdf_reviewed`; ui_records `not_run`; publication `not_published`; tia_compile/live_cpu/field_recovery 모두 `not_performed`. 독립 부모 검토·첨부 대기다. 현장 보호값·정상극성·실제 모델/현행 CPU·복구 완료는 채우지 않았다.

### 검증 범위

선정 원본30개 SHA256과 고정 Git blob 전체 내용이 일치했다. 이는30개 전체 문맥 의미검토가 아니다. 직접 의미대조는 0223/0295 고유 전체 핀, 0332의 CL04 reset 가지, 0397의 IW12 전달, 0549 FC9/FC2 호출 및0019 T13 가지와 선택 선언이다. 전기 실제 렌더4쪽을 확인했다. XML181개 명명 검색은 경계 탐색일 뿐181개 의미검토로 세지 않는다. 원본 생성기/시험기, TIA, 시뮬레이터는 실행하지 않았다.

검사 JSON 및 검색/원형 발췌는 `../extracts/CLIENT-CL04/verification.json`, `source-hashes.json`, `declaration-search.json`에 있다. 이번 산출물은 본 MD와 배정 extracts 디렉터리뿐이다.

### 선정 원본 SHA256 전체 표

경로는 고정 `source-mv06/` 기준이다. 모든 행의 Git 내용 일치는 파일 byte와 `git show abcf31c:경로`의 직접 비교다.

|선정 원본 경로|SHA256|고정 Git blob|내용 일치|
|---|---|---|---|
|`AGENTS.md`|`0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2`|`073164bc6efd5791032d62c71b03b4dab48cb6f8`|일치|
|`.agents/skills/gme-equipment-rollout/SKILL.md`|`fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b`|`9aa820ea6ca15b4e136c9772423b78ed4df6a3d4`|일치|
|`docs/equipment-standard/WORK-STANDARD.md`|`05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99`|`f76a570cc73098632e08759b17934000f7e3a253`|일치|
|`docs/equipment-standard/WORK-ITEM-TEMPLATE.md`|`4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586`|`e546f39535d2b589e80f97db869ac37ce4d05cfd`|일치|
|`docs/equipment-standard/INVENTORY.json`|`720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc`|`587c3748ad9224718f95ba06463fee913dae231d`|일치|
|`all-in-one/sources/Electrical_Rev2.pdf`|`5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6`|`f610fd7c7ce14ae951b00cff57b969259bfb389d`|일치|
|`all-in-one/sources/Electrical_Can_Decoating_20241118.pdf`|`3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd`|`0ee6b6f8361c5790864dbba4bbd9d55e8e7c08f8`|일치|
|`all-in-one/sources/hmi_plc_tags.csv`|`a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404`|`cf4c0650e7c7baac350dcb89909b808435704880`|일치|
|`all-in-one/sources/live_index.json`|`14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1`|`e35ccea1f841349c632666c29954b7bcd4f5839e`|일치|
|`all-in-one/sources/decoded-original/network-map.json`|`c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60`|`424430b6b953e43138e5d0a18ca40c949e21cfa1`|일치|
|`all-in-one/sources/decoded-original/0019-FlgNet.xml`|`a3301f4d07c2d36aefa6faa6c3559a1cff4565fc6de40cd17e54b548b30c0ce5`|`f78cfdbf5e717304114660ffbd3bb42cbed6d79d`|일치|
|`all-in-one/sources/decoded-original/0223-FlgNet.xml`|`ef5a6a12a839e888bf61a7fde898bb63053fe3680dc0ef4fe30ca338487cca72`|`def6d6058fdb74592cb7b53bba80ee20d8896594`|일치|
|`all-in-one/sources/decoded-original/0295-FlgNet.xml`|`db68ca1f7e56b71860458ebc5f257a2956933f239736ed3bf31e7b74520918f9`|`3694d5caf61f77aea3d57f275f89340a1d63248b`|일치|
|`all-in-one/sources/decoded-original/0332-FlgNet.xml`|`c677499004010aba2746412a08e32f3e4206e9212d481fc08ee1c6023326cef7`|`50e3451e01b63fb9311aade1c4bfefa0719d305b`|일치|
|`all-in-one/sources/decoded-original/0397-FlgNet.xml`|`bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834`|`4ab8370493c4e28fc1eabeeebe2743d27f0c4021`|일치|
|`all-in-one/sources/decoded-original/0549-FlgNet.xml`|`49f7169c33ed7f54559b0801e21a7d618584900972840e91cf51ad032e8febb1`|`985b5310b43b1015b5dee286aa0e42800564b94b`|일치|
|`all-in-one/sources/decoded-original/0558-IdentXmlPart.xml`|`45d49d53b6b41312960bb2a329663e87d8803e28d7832308424a6bf5091e6d1b`|`a0b681bd15e9ae15f2e1437576a4486cc732fdf2`|일치|
|`all-in-one/sources/decoded-original/0599-IdentXmlPart.xml`|`32a693fe12134febbd9f5c7da10c3469ef4d5b164ab8b6bd9ea3867c358936c1`|`493de77fc827d8f14192ced05d82df3a062f7965`|일치|
|`all-in-one/sources/decoded-original/0600-IdentXmlPart.xml`|`20c58ee0383d0b6c275bd2d96abd30af7c5d1f3fff59c7d5034cd758936b57d5`|`f22a7ededd0576cf379ee19908da067f08d45412`|일치|
|`all-in-one/sources/decoded-original/0601-IdentXmlPart.xml`|`04c9481f7381284de689ef5c7ff40d7aea93f2004cd877a4e4f27e47baa6d862`|`07bcf656fa58e4a305999456644acd24b3dc6bec`|일치|
|`all-in-one/sources/decoded-original/0613-IdentXmlPart.xml`|`09d3b1397a987898334218f37e025661af162438582e649f671e7abec443d3cb`|`c9d19a48e947098914f4d2de3348c05b4f6d37e8`|일치|
|`all-in-one/sources/decoded-original/0614-IdentXmlPart.xml`|`c6de26f74d75f5be858a406de75eaf6faf62ba9b89c8f9a085b5dd206e93d294`|`da0485aa033700f08c8695d30b93ebd2d377d6c7`|일치|
|`all-in-one/sources/decoded-original/0615-IdentXmlPart.xml`|`80f4544edca56c6e6bb2713c758c92ade9202255110074931e03fe34d0d0801a`|`49eb86fe01feb83de8c0864b21493d305aff8b20`|일치|
|`all-in-one/sources/decoded-original/0616-IdentXmlPart.xml`|`650b53354a0c8443d94adc5bd6a860d3c5313014a52e0fb98a5656a65b58cc0d`|`9f7fdd5f93ac149c139a054ebb34f63c632ef7fd`|일치|
|`all-in-one/sources/decoded-original/0627-IdentXmlPart.xml`|`08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb`|`61ebc0abbb2ca160e11e1da400a3f14a397d8bc5`|일치|
|`all-in-one/sources/decoded-original/0628-IdentXmlPart.xml`|`9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd`|`170ca5c72599edc7ea7eefe651c3680ce325e76a`|일치|
|`all-in-one/sources/decoded-original/0629-IdentXmlPart.xml`|`67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972`|`058129bb01e27f7a6a0d0293f332d745e5bab74e`|일치|
|`all-in-one/sources/decoded-original/0688-IdentXmlPart.xml`|`ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda`|`463585759f1ecd94f32362b4fefb000a152f5773`|일치|
|`all-in-one/sources/decoded-original/0692-IdentXmlPart.xml`|`bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037`|`737785d03b5fad43c5b4d451955726d800edb1c0`|일치|
|`all-in-one/sources/decoded-original/0694-IdentXmlPart.xml`|`757ccebdf32d0a168dd787bfa735fe6494eac4c4a9f7a5adc63898a88e8b152d`|`c45e8f3ca4129dc06734f6a12ef79e6ed6528a7d`|일치|

초안 작성/검사 완료 실제시각: 2026-10-11T12:18:10.870277+00:00
