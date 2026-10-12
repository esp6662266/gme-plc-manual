# CLIENT-CL05 — Air knife 자체 원본 조사 초안

## 핵심 확인·상충·누락

- 독립확인: RUN I12.7, FAULT I15.2, 유지경보 DB3.DBX14.5; 0224 NID5의 Set/Reset와 0296 NID5의 시간계수 핀을 직접 대조했다.
- 중요한 배정 경계: live_index의 Q61.3 이름은 `start client motor 6`이다. CLIENT-CL05의 출력이 아니다. CL05 기동 출력 선언·writer·전기 끝점은 이번 명명 검색에서 미확보다. 순번을 보간하여 Q61.3을 배정하지 않는다.
- 시간계수: DB9.DBW16 MIN은 Int +1, DB9.DBW18 HOUR는 Move 1이다. HOUR+1 누적기로 바꾸지 않는다. NID47에서 HOUR에 Move 0도 존재한다.
- 전기 독립확인: OEM FG88/PDF89 RUN X1:292/293 → E12.7, FG128/PDF129 모듈 단자8; FG92/PDF93 FAULT X1:330/331 → E15.2, FG131/PDF132 모듈 단자33. 네 실제 렌더의 개정란을 각각 읽었다.
- 상충 보존: live_index의 RUN 과거 설명 `e 13.4`, FAULT `e 18.2`와 실제 백업 Address `%i12.7`/`%i15.2`를 혼합하지 않는다. 해당 회로의 SPARE 표기도 보존한다.
- 공통 근거: 이전 [CLIENT-CL04](CLIENT-CL04-DOTS-DRAFT.md)와 CL01~03은 FC9/FC2·T13·HMI Word 전달의 색인으로만 사용했다. 채널별 선언/핀/알람/단자/페이지는 이번 원본에서 독립 확인했다. 전체 Reset·장기 저장 핸드셰이크는 [SYS-ALARM](SYS-ALARM-DOTS-DRAFT.md), [SYS-RUNHOURS](SYS-RUNHOURS-DOTS-DRAFT.md)의 동일 고정원본 공통 상세를 연결한다.
- 미확정: 외부 Air knife 제어반·명판·케이블·기동허가·실제 정상극성·현재 CPU/HMI·현행 보호값·현장복구. CLIENT-CL05와 CYL-CL05를 병합하지 않는다.

## 1. 설비·자료 기준

대상은 INVENTORY.json catalog index61의 CLIENT-CL05, 이름 Air knife, kind client, group 외부 연동, phase2, 부모 없음이다. 별칭 motor_client_05/client motor 5/cl05/air knife는 탐색용이며 실물 동일성을 증명하지 않는다. 이 문서는 GME PLC가 외부 설비로부터 받은 운전·고장 관찰 및 시간계수를 다룬다. 송풍기·노즐·압력조절기·외부 인버터 구성은 이름만으로 발명하지 않는다.

고정 읽기전용 원본: `gme-research/source-mv06`, commit `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, v1.12.0. 이후 사용자의 게시보고와 이 백업 검토를 구분한다. 표준 GME-STD-1.0.0 및 WORK-ITEM-TEMPLATE에 맞춘 문서 조사이며 로컬 통합·배포는 별도 작업이다. 모델 런타임 증명은 미확인이다.

실제 작업시각(UTC): 지시/원본 읽기 2026-10-11 12:22:25부터, 고유 선언/핀 조사 12:22:50부터, 도면 렌더 12:23:30 및 시각검토 12:23:38, 해시 검사 12:24:35. 추정 소요시간을 작업기록으로 쓰지 않았다.

아래 XML 약호는 모두 `all-in-one/sources/decoded-original/NNNN-FlgNet.xml` 또는 `NNNN-IdentXmlPart.xml`, HMI와 live_index는 `all-in-one/sources/` 아래 원본이다. network-map/live_index는 탐색 인덱스이며 핵심 해석은 XML 핀·선언으로 대조했다.

## 2. I/O·HMI

|대상|독립 원본 선언·문맥|주소·형식·소유|
|---|---|---|
|AIR KNIFE RUN|0613 RID32 Global, NID5 UID316; SSD AO103, SAD Input SAM=None|I12.7 Bool 입력영상. 실제 풍량이나 기계 작동의 증명 아님|
|AIR KNIFE FAULT|0599 RID14 Global, NID5 UID125/127; AO122 Input SAM=None|I15.2 Bool 원시 입력|
|Allarm.motor_client_05_fault|0601 RID15 Global AO117 Bool BAD4 →0600 RID4 TOD3; NID5 UID126/129 Write|DB3.DBX14.5 내부 유지경보|
|Flag.RESET_ALLARM|0601 RID7 Global AO48 Bool BAD6 →0600 RID6 TOD2; NID5 UID128|DB2.DBX6.0 내부 공통 Reset. HMI 버튼 자체와 구별|
|ON|0599 RID1 Global AO0 SAD Memory, NID5 UID124|M0.0 Bool. 이름 ON을 상수 true로 치환하지 않음|
|CLIENT_MOTOR_5_MIN|0615 RID34 Global Int AO128 BAD5 →0614 RID5 TOD9; NID5 UID317/319/320/325|DB9.DBW16; Add 및 Move0 writer|
|CLIENT_MOTOR_5_HOUR|0615 RID36 Global Int AO144 BAD5; NID5 UID323 Write, NID47 UID2599 Write|DB9.DBW18; Move1/Move0|
|Tag_47 / Flag_Aggiorna_DB|0613 RID1 Timer AO13 / RID13 Bool Memory AO15|T13 / M1.7 공통 PLC 시간·갱신 신호|
|기동 출력|live_index `start client motor 5` 고유 심볼 미식별|주소를 지정하지 않음. Q61.3은 doc481의 motor6 심볼|

위 채널 선언은 Global이고 Int1/60/0 및 S5T#1M은 Constant다. 다른 문맥의 같은 RID/UID를 Local 변수와 결속하지 않았다.

HMI CSV의 `AIR_KNIFE_RUN`은 `DB13,X12.7`, ID00401, Access Name PLC다. `Allarmi_118`은 `DB3,X14.5`, ID00117다. 주소 설정은 확인했지만 화면 이벤트·통신현재값·표시문구·ACK 이력은 미확보다. CSV ID와 태그 이름의 숫자118을 외부 오류코드로 바꾸지 않는다.

0397 HMI Inputs NID1의 Word 전달: rail W21→Move60.en, ORef63/RID19(0627 Global Tag_183 Word Input AO96 SAM=None = IW12) →W70→Move60.in, out1→W72→ORef64/RID20(0629 Word AO96 BAD4→0628 TOD13 = DB13.DBW12). 이 Word 전체 복사가 I12.7을 포함하는 DB13 바이트 범위를 전달한다. Bool 코일 쓰기나 PIW 직접 접근으로 설명하지 않는다. Move60에는 DisableENO=true와 동시에 XML상 eno W71→Move61.en 연결이 있으므로 두 원문 특성을 보존한다. FC15 상위 호출·다른 writer·실제 스캔 최종값은 공통 SYS-PLC-IO 경계이며 이 한 연결로 현행 HMI 정상통신을 증명하지 않는다.

## 3. 제어 구조

### 호출과 외부 소유 경계

0549 Main document1620 NID7: rail W352→Contact350.in; ON ORef335/RID52(0692, Global M0.0)→W348→operand. Contact350.out W351은 CRef331/334 등의 en에 병렬 연결된다.

- CRef331 RefId80, 내부 CodeBlock345 RefId79; 0688 RID79 TOD9 FC `Motor/Alarm Client`, 0694 RID80 NID7 UID331의 호출 인터페이스와 결속.
- CRef334 RefId83, 내부 CodeBlock347 RefId82; 0688 RID82 TOD2 FC `time work motor`, 0694 RID83 NID7 UID334와 결속.

FC9의 ENO가 FC2를 직렬 허가하는 구조가 아니다. 호출 경로를 확인했으나 현재 CPU 실행주기·기동/정지 FB·외부 제어반 순서를 확인한 것은 아니다.

### 고유 시간계수 — 0296 document1006 FC2 NID5

|단계|Part/ORef/Wire 직접 대조|해석|
|---|---|---|
|계수 허가|rail W348→Contact344.in; T13 ORef315/RID1→W327→344.operand; out W345→Contact346.in; I12.7 ORef316/RID32→W328→346.operand; out W347→Add298.en 및 Ge305.pre|T13 AND AIR KNIFE RUN일 때 계수 가지 활성|
|MIN 증가|Add298 SrcType=Int, in1 W329/ORef317=MIN, in2 W330/ORef318/RID7=Int1, out W331/ORef319=MIN|DB9.W16 := DB9.W16 + 1|
|60 비교|Ge305 Int, in1 W332/ORef320=MIN, in2 W333/ORef321/RID8=60; out W334→Move308.en|MIN≥60 가지|
|HOUR 쓰기|Move308.in W336/ORef322/RID7=1, out1 W337/ORef323/RID36=HOUR|DB9.W18 := 1. HOUR+1이 아님|
|MIN 초기화|Move308.eno W338→Move311.en; in W339/ORef324/RID12=0, out1 W340/ORef325=MIN|앞 Move ENO 이후 MIN:=0|
|갱신 플래그|Move311.eno W341→SCoil314.in, operand W342/ORef326/RID13=M1.7|ENO 의존으로 Flag_Aggiorna_DB Set|

0019 FC2 NID58 공유 분 타이머: Contact3120 operand NOT(T13 ORef3115/RID1/W3118), out W3121→SdCoil3112.in; value W3117/ORef3114/RID335는 0616 Constant S5Time `S5T#1M`(V5632); operand W3119/ORef3116=T13. 이는 계수용 공통 타이머이며 Air knife의 기동지연/무응답/보호 설정이 아니다. 실제 1분 정확도·시간 저장 성공은 미확정이다.

0332 FC2 NID47은 고유 HOUR의 다른 writer다. T17(0613 RID284 Tag_48, ORef2589)→W2600→Contact2615, out W2616→Move2574.en. Move2574→2577→2580→2583의 ENO 체인을 거쳐 W2612→Move2586.en; in W2613/ORef2598/RID12=0, out1 W2614/ORef2599/RID36=CLIENT_MOTOR_5_HOUR. 즉 DB9.W18에도 Move0가 있다. 외부 장기누적·T17/M1.7 핸드셰이크는 SYS-RUNHOURS 공통 조사 참조이며 이 문서에서 외부 ACK·저장 완료를 추가 주장하지 않는다.

### 명령 부재의 정확한 한계

decoded-original IdentXmlPart 181개에서 Air knife 및 CL05 명명 검색으로 고유 선언5개를 식별했다. `start client motor 5` 심볼·직접 출력 writer는 미식별이다. live_index doc480~484에는 CL4/6/8/9/10 기동 심볼만 확인된다. 따라서 Q61.2/3/4/5/6을 순서상 CL05에 배정하지 않는다. 명명 검색은 절대주소·간접주소·블록복사까지 포함한 실행 부재 증명이 아니며, 전체 프로그램 의미검토181개 완료도 아니다. 외부 제어반의 독립기동 가능성을 사실로 단정하지 않는다.

## 4. 전기 전달 경로

`all-in-one/sources/Electrical_Rev2.pdf` 실제 PDF89·93·129·132를 각각 렌더해 눈으로 확인했다. 각 페이지 footer의 Rev2 17.03.2025 및 DATA 27.05.2024를 읽었다. 이번 네 페이지는 FG+1이 실제 PDF였지만 다른 페이지에 공식을 확장하지 않는다.

|구분|FG / 실제 PDF와 원본 끝점|미확정 경계|
|---|---|---|
|RUN 외부 접점|FG88/PDF89 AIR KNIFE RUN: +24Vdc10.7 → 5x20 2A F 퓨즈 표기 X1:292 → 선88.5 → 열린 접점 기호 → X1:293 → E12.7 /128/7|외부 접점 기기번호·상대 제어반 단자·케이블 번호/규격 미기재|
|RUN 입력|FG128/PDF129 E12.7, 상호참조88/7 → 모듈 단자8; CPU515 / MOD11, AIR KNIFE RUN|도면 표기는 현재 CPU 실물 증명이 아님|
|FAULT 외부 접점|FG92/PDF93 AIR KNIFE FAULT: +24Vdc10.7 → 5x20 2A F 퓨즈 표기 X1:330 → 선92.4 → 열린 접점 기호 → X1:331 → E15.2 /131/3|외부 고장 내부회로·실제 극성/정상상태 미확정|
|FAULT 입력|FG131/PDF132 E15.2, 상호참조92/6 → 모듈 단자33; CPU515 / MOD11|외부 보호기 종류·고장 상세와 별개|
|모듈 보조전원|같은 FG131 +24Vdc10.7→X21:3013, 5x20 2A IST.→선131.1→단자39; -0Vdc10.6→단자40|도면 정격이며 현행 퓨즈/보호값 추천이 아님|
|기동·전력 출력|이번 선택원본에서 Air knife 전용 GME 출력/릴레이/컨택터/모터전력 끝점 미식별|모터·드라이브·정격·상대반 도면 확보 필요|

네 페이지의 해당 입력 범위는 SPARE 점선 안에 그려져 있다. 표기와 심볼이 존재한다는 사실을 실제 배선/설비 사용 확정으로 바꾸지 않는다. 열린 접점 기호로 현장 정상극성·무전압 안전성·고장시 접점 동작을 추정하지 않는다. 이 입력 도면은 릴레이 부하5/9 및 하단 접점표1/5/9를 판정하는 출력 회로가 아니므로 숫자를 복제하지 않는다. 시공도 전수 렌더·외부 Air knife 제어반 조사 완료를 주장하지 않는다.

## 5. 알람·복구

0224 document414, FC9 `Motor/Alarm Client` NID5를 전체 핀 대조했다.

- 공통허가: rail W147→Contact139.in; ON ORef124/RID1→W130→operand; out W140은 Set/Reset 가지로 분기.
- Set: FAULT I15.2 ORef125/RID14→W131→Contact141.operand; out W142→SCoil118.in; operand W133/ORef126/RID15=DB3.X14.5. `ON AND FAULT`에서 Set.
- Reset: 같은 FAULT ORef127/RID14→W134→Contact143.operand에는 Negated 표시; out W144→Contact145.in; RESET_ALLARM ORef128/RID7→W135→operand; out W146→RCoil123.in; operand W137/ORef129/RID15=같은 경보. `ON AND NOT FAULT AND RESET_ALLARM`에서 Reset.

네트워크에는 타이머 Part가 없다. 1분 계수 타이머를 고장지연으로 바꾸거나 다른 설비의 3초/5초 값을 복제하지 않는다. RUN=0은 이 고장 래치의 직접 원인이 아니다. 입력 FAULT가 계속 참이면 이 Reset 조건은 성립하지 않는다.

HMI Allarmi_118의 주소는 래치와 일치하지만 실제 경보 표시 문자열·이력·ACK 이벤트는 미확보다. 공통 Reset 생성과 DB3 집계는 SYS-ALARM 참조 범위다. 원인 소멸, 내부 래치 해제, HMI ACK, 외부 제어반 Reset, 재기동, 실제 복구는 모두 구별한다. 이 경보가 모터를 직접 정지시키는 출력 writer 경로는 미확인이므로 정지 인과를 추가하지 않는다.

## 6. 증상별 읽기 전용 관찰

승인된 담당자가 제공할 관찰 자료의 비교 기준이며 현장 조작 절차가 아니다. 강제출력·바이패스·활선점검·Reset 실행·보호값 변경을 하지 않는다.

|증상|같은 시각에 수집할 정보|비교 기준과 판정 한계|
|---|---|---|
|Air knife 작동인데 RUN 표시 없음|현행 프로젝트 식별, I12.7, IW12, DB13.W12/X12.7, HMI ID00401, 외부반 상태|X1:292/293→E12.7 단자8과 Word 미러를 분리. 단선·통신·정상극성을 바로 단정하지 않음|
|시작 표시인데 작동 없음|화면 버튼/이벤트, 실제 기동 writer 교차참조, 외부반 기동허가·상태, I12.7|Q61.3을 CL05로 가정하지 않음. 명판·외부반 회로·케이블 자료부터 필요|
|FAULT 소멸 후 경보 유지|I15.2, ON, DB2.X6.0, DB3.X14.5, Allarmi_118 이벤트|0224 유지 래치와 NOT FAULT Reset 조건. 외부 고장 소멸만으로 자동해제 아님|
|Reset 요청에도 유지|현재 FAULT와 내부 Reset 전후, HMI 요청/소비 로그|HMI 요청과 내부 비트 및 외부 Reset 구분. 반복 재기동으로 해결 주장 금지|
|시간 값이 1에서 멈추거나 누적이 안 됨|I12.7,T13,DB9.W16/W18,M1.7,T17,외부 저장내역|0296 MIN+1/HOUR Move1,0332 HOUR Move0를 먼저 비교. 장기 누적기·저장 성공 미확정|
|도면/명칭 충돌|프로젝트·도면 판본, X1/모듈/외부반 표찰과 담당자 설명|과거 e13.4/e18.2와 백업 I12.7/I15.2를 별도 보존; CYL-CL05와 혼합 금지|

관찰 기록은 관찰자·실제시각/시간대·위치·값/단위·장치·프로젝트/도면 판본·자료 출처·비교결과·배제된 원인·미확정 사항을 담는다. 실제 사용자 운영/SEJIN 기록이나 사진은 이번 문서에 복제하지 않았다.

## 7. 완료 기준·누락·검증

|영역|상태|남은 조건|
|---|---|---|
|설비·자료 기준|적용, 문서 작성|실물 동일성 미확정|
|I/O·HMI|적용, 입력/알람/시간 및 Word 경로 확인|기동 선언/writer, HMI 이벤트·현재 통신 미확보|
|제어 구조|적용, 고유 FC9/FC2 선택 논리 대조|기동/정지·수자동·외부반 내부 시퀀스 미확보|
|전기 끝점|입력 두 경로 실제 렌더4쪽 확인|상대 제어반·케이블·기동전력·실물 미확보|
|알람·복구|고유 S/R 조건 확인|외부 원인·ACK/Reset·현장복구 미확인|
|증상 관찰|읽기전용 비교 기준 작성|현장 관찰값 미취득|
|완료·누락|문서/구현/게시/현장 분리|BC01 동등 기능완료나 현장완료 아님|

추가자료: 현재 Air knife 명판 및 외부 제어반 회로/프로그램·기동허가표, GME 출력 전체 교차참조(절대·간접쓰기 포함), X1:292/293/330/331 상대 단자·케이블표, 현행 HMI 이벤트/스크립트, 정상 RUN/FAULT 상태의 승인 근거, 장기 운전시간 저장 인터페이스. 새 자료 없이 같은 실물 보류를 반복 조사하지 않는다.

네 기능 적용: 도면·래더 비교 근거는 본 문서로 준비했다. 백업 미리보기/선택복원, 기록 전후비교, 관찰보고서/PDF의 이 ID 전용 구현·저장/재읽기·재열기는 실행하지 않았다. note/repair_observation 미지필드·초안·저장키·원본코드 변경 없음. 원본 build/test/generator, 시뮬레이터 작성/수정/생성/실행/행동시험, TIA, PLC, 현장, 보호값 및 SEJIN 변경은 하지 않았다.

최종 상태: documentation `complete_with_gaps`; static_review `selected_original_xml_and_pdf_reviewed`; ui_records `not_run`; publication `not_published`; tia_compile/live_cpu/field_recovery `not_performed`. 부모의 독립 검토 및 첨부 대기다. 공개 대장/배포/로컬통합 기록은 이 작업에서 갱신하지 않았다.

검사범위: 선정 원본32개 SHA256·고정 Git blob 내용 일치. 해시32개는 의미검토32개가 아니다. 핵심 의미검토는 0224/0296 고유 전체 핀,0332 CL05 Reset 가지,0397 IW12 Word 미러,0019 T13 가지,0549 FC9/FC2 호출 및 선택 선언이다. 명명 검색181개/선언 hit5개는 경계 탐색 수다. OEM 실제 렌더4쪽 확인. 검사 JSON·검색 발췌·렌더는 `../extracts/CLIENT-CL05/`에 보존했다.

### 선정 원본 SHA256·고정 Git blob 전체 목록

경로는 source-mv06 기준이다. 내용 일치는 파일 전체 byte와 `git show abcf31c:경로` 직접 비교다.

|선정 원본 경로|SHA256|고정 Git blob|내용 일치|
|---|---|---|---|
|`AGENTS.md`|`0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2`|`073164bc6efd5791032d62c71b03b4dab48cb6f8`|일치|
|`.agents/skills/gme-equipment-rollout/SKILL.md`|`fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b`|`9aa820ea6ca15b4e136c9772423b78ed4df6a3d4`|일치|
|`docs/equipment-standard/WORK-STANDARD.md`|`05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99`|`f76a570cc73098632e08759b17934000f7e3a253`|일치|
|`docs/equipment-standard/WORK-ITEM-TEMPLATE.md`|`4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586`|`e546f39535d2b589e80f97db869ac37ce4d05cfd`|일치|
|`docs/equipment-standard/INVENTORY.json`|`720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc`|`587c3748ad9224718f95ba06463fee913dae231d`|일치|
|`VERSION.json`|`5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7`|`fffb51663b7705aec91cb119ca80ee943a4ce758`|일치|
|`WORKSPACE-HANDOFF.md`|`215096d997782e78e901dfae36c782937e49611fbeb677a0d3fa50cbecf8d074`|`dd0b8989d2376c4415bba9bd826fe6754c6b1a12`|일치|
|`PUBLICATION_STATUS.md`|`efe4857aec598d90470322cf3962eb3fe1f64947630e1fdf71d1c90134de8740`|`d76401cf291fc0be681acc51fa898ad3ce46ff78`|일치|
|`all-in-one/ACTIVE-WORK.md`|`eff3bbc08ecff41da3beff77f3fec48e7d148708192bcaaab00f34b6a721afc2`|`6eb947c629b5ddf9c759ef87649451303938864b`|일치|
|`all-in-one/sources/Electrical_Rev2.pdf`|`5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6`|`f610fd7c7ce14ae951b00cff57b969259bfb389d`|일치|
|`all-in-one/sources/hmi_plc_tags.csv`|`a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404`|`cf4c0650e7c7baac350dcb89909b808435704880`|일치|
|`all-in-one/sources/live_index.json`|`14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1`|`e35ccea1f841349c632666c29954b7bcd4f5839e`|일치|
|`all-in-one/sources/decoded-original/network-map.json`|`c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60`|`424430b6b953e43138e5d0a18ca40c949e21cfa1`|일치|
|`all-in-one/sources/decoded-original/0019-FlgNet.xml`|`a3301f4d07c2d36aefa6faa6c3559a1cff4565fc6de40cd17e54b548b30c0ce5`|`f78cfdbf5e717304114660ffbd3bb42cbed6d79d`|일치|
|`all-in-one/sources/decoded-original/0224-FlgNet.xml`|`cca832c330559a2871c014722c05861dcddbe536b6dbaad46cf5c0adce09a190`|`4f4be07b04636e8a11621d8c843172e5360be8bf`|일치|
|`all-in-one/sources/decoded-original/0296-FlgNet.xml`|`8326d0a6474b89cf31127b1e3cf907b4b1e92cfb76d781045cbadfaaab6ac964`|`6895ea3252d40326d266003b954529b286005221`|일치|
|`all-in-one/sources/decoded-original/0332-FlgNet.xml`|`c677499004010aba2746412a08e32f3e4206e9212d481fc08ee1c6023326cef7`|`50e3451e01b63fb9311aade1c4bfefa0719d305b`|일치|
|`all-in-one/sources/decoded-original/0397-FlgNet.xml`|`bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834`|`4ab8370493c4e28fc1eabeeebe2743d27f0c4021`|일치|
|`all-in-one/sources/decoded-original/0549-FlgNet.xml`|`49f7169c33ed7f54559b0801e21a7d618584900972840e91cf51ad032e8febb1`|`985b5310b43b1015b5dee286aa0e42800564b94b`|일치|
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

초안 작성·검사 완료 실제시각: 2026-10-11T12:26:51.129535+00:00
