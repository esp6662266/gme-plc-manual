# CLIENT-CL19 · Primary shredder · 7영역 원본 조사 초안

## 핵심 확인·상충·공유 근거

- 고유 선언/핀으로 확인: PRIMARYSHREDDER RUN I14.2, 유지경보 DB3.DBX16.3, 분 계수 DB9.DBW72, HOUR 전달 DB9.DBW74. 0236/0307/0335의 해당 고유 경로를 직접 대조했다.
- **중요 상충:** 0236의 제목은 `primary shradder fault (cl19)`이지만 Set 원인은 별도 FAULT가 아닌 **PRIMARYSHREDDER RUN I14.2**다. 같은 입력이 0307 시간계수에도 사용된다. 원형대로 `ON AND I14.2 → 경보 Set`을 기록하며 오배선/프로그램 오류/정상운전 여부를 단정하거나 코드를 수정하지 않는다.
- 실제 FG91/PDF92와 FG130/PDF131: X1:314/315 → E14.2 → 입력 단자23. 두 페이지 모두 CL19 가지가 SPARE 점선에 포함되며 Rev2 17.03.2025 / DATA 27.05.2024를 직접 렌더 확인했다.
- 주소 상충: live_index doc530 주석 `e 15.2 primaryshredder run`과 선언·Address `%i14.2`, 실제 도면 E14.2는 다르다. 과거 주석을 현행 주소로 채택하지 않는다.
- 누락: CL19 전용 기동 Q writer, 독립 FAULT 입력, 출력릴레이·전력 회로, 외부반 내부 순서/보호, 현재 실물과 SPARE 사용상태는 미확정이다.
- 공유 근거: [CLIENT-CL16](CLIENT-CL16-DOTS-DRAFT.md), [SYS-RUNHOURS](SYS-RUNHOURS-DOTS-DRAFT.md), [SYS-ALARM](SYS-ALARM-DOTS-DRAFT.md)의 같은 고정원본 공통 구조를 색인으로 재사용했다. 0549 호출, 0019 T13, 0397 IW14 미러의 필요한 원형 핀은 다시 확인했고 다른 CLIENT 주소·조건·끝점을 복제하지 않았다.

## 1. 설비·자료 기준

`docs/equipment-standard/INVENTORY.json#/catalog/73`: CLIENT-CL19, Primary shredder, client/외부 연동, 부모 없음, phase2. 범위는 GME PLC의 외부 19번 인터페이스와 확인된 입력·내부 처리다. 같은 번호의 CYL-CL 공압 실린더와 별도 이름 공간이며 실물 동일성 확인/다른 설비 완료를 뜻하지 않는다.

고정 읽기전용 기준은 `source-mv06`, Git `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, v1.12.0이다. 아래 4자리 XML은 `all-in-one/sources/decoded-original/` 하위 파일을 가리킨다. 파일번호, document_id, NID, RID, UID는 별개 식별자이며 UID만 같은 다른 문맥을 연결하지 않는다. `live_index.json` 및 `network-map.json`은 탐색 색인이고 고유 핵심은 원형 XML 및 실제 PDF로 확인했다.

실제 시각(UTC): 2026-10-11 12:37:13 착수, 12:37:42~12:38:27 고유 선언·핀 및 공유 연결 대조, 12:38:06 PDF 렌더, 12:38:12 두 페이지 시각 확인. 해시/최종 검사 시각은 검사 JSON과 아래 표에 기록한다. 실행 모델·추론 런타임 증명은 미확인이다. 로컬 TIA/사용자 Mac 추가접근·새 Work/Codex 생성·재위임 없이 문서만 작성했다.

## 2. I/O·HMI

### 고유 선언·형식·소유

|신호|원형 선언 및 참조|해석·경계|
|---|---|---|
|PRIMARYSHREDDER RUN|0599 RID44 Global Bool, SSD AO114, SAD Input SAM=None; NID19 UID377/379. 0613 RID116 같은 AO114, NID19 UID1072|I14.2 입력영상. 알람과 시간계수의 같은 원시 신호; 물리 운전/고장 의미 미확정|
|Allarm.motor_client_19_fault|0601 RID43 Global Bool AO131, BAD4→0600 RID4 TOD3; NID19 UID378/381 AK=Write|DB3.DBX16.3 내부 S/R 경보. 별도 물리 FAULT 입력으로 만들지 않음|
|Flag.RESET_ALLARM|0601 RID7 Global Bool AO48 BAD6→0600 RID6 TOD2; NID19 UID380|DB2.DBX6.0 내부 Reset 조건; HMI 버튼·외부반 Reset과 별개|
|ON|0599 RID1 Global Bool Memory AO0, NID19 UID376|M0.0 공통 허가; 이름만으로 항상 true 상수로 단정하지 않음|
|CLIENT_MOTOR_19_MIN|0615 RID118 Global Int AO576 BAD5→0614 RID5 TOD9; NID19 UID1073/1075/1076/1081|DB9.DBW72, Int Add/비교/Move0 대상|
|CLIENT_MOTOR_19_HOUR|0615 RID120 Global Int AO592 BAD5; NID19 UID1079와 NID50 UID2783 Write|DB9.DBW74, Move1 및 다른 네트워크 Move0 대상; 자체 장기 누적 Add 아님|
|Tag_47 / Tag_48|0613 RID1 Timer AO13 / RID284 Timer AO17|T13/T17 공유 PLC 시간계수·전달 타이머, CL19 고장지연 타이머 아님|
|Flag_Aggiorna_DB|0613 RID13 Global Bool Memory AO15; NID19 UID1082 Write|M1.7 공유 DB 갱신 요청 관련 Set 비트|

고유 선언은 Global이고 상수는 0616의 Constant다. Local 변수로 오인하지 않는다. 입력 Bool, DB Bool, Int, Word 복사, Timer/S5Time의 형식을 구별한다. 전체 IdentXmlPart 명명 검색에서 CL19 원시입력 2개 문맥, 경보 1개, MIN/HOUR 각1개의 선언을 발견했다. 검색은 절대/간접쓰기 전수부재 또는 모든 원본 의미검토의 증명이 아니다.

### HMI와 Word 미러

`all-in-one/sources/hmi_plc_tags.csv`의 직접 확인 행:

- `PRIMARYSHREDDER_RUN,"DB13,X14.2",PLC,003F7`
- `Allarmi_132,"DB3,X16.3",PLC,0010A`

이는 dde.cfg 태그 설정이며 현재값·실제 화면·텍스트·스크립트·이벤트·ACK·통신의 검증이 아니다. RUN 미러와 유지경보는 다른 주소다. MIN/HOUR 표시 및 기동 이벤트 결속은 미확보다.

0397 HMI Inputs NID1: 0627 RID21 `Tag_274` Global Word AO112 Input SAM=None는 IW14. ORef65 W73→Move61.in, Move60.eno W71→61.en, 61.out1 W75→ORef66/0629 RID22 Global Word AO112 BAD4→0628 RID4 TOD13으로 **IW14→DB13.DBW14**를 쓴다. 이 Word가 I14.2를 DB13.X14.2로 전달한다. rail W21→Move60.en, Move60/61의 DisableENO=true와 실제 eno/en 연결을 함께 보존했다. bit별 Coil 또는 PIW/Peripherie 읽기로 바꾸지 않는다. 상위 FC15 호출·다른 writer·현재 스캔 최종값은 공통 미확정 경계다.

## 3. 제어 구조

### 상위 호출과 미확보 기동 경계

0549 Main document1620 NID7: rail W352→Contact350.in, ON ORef335/RID52 W348→operand(0692 Global Memory AO0). out W351이 CRef331/334.en에 병렬 연결된다. CRef331 RefId80/CodeBlock345 RefId79는 0688 RID79 `Motor/Alarm Client` TOD9 FC, 0694 RID80 TORID79다. CRef334 RefId83/CodeBlock347 RefId82는 0688 RID82 `time work motor` TOD2 FC, 0694 RID83 TORID82다. 앞 FC의 ENO를 뒤 FC의 순차 허가로 발명하지 않는다.

확보 경로는 외부 접점→I14.2→FC9 경보/FC2 계수→DB 및 HMI다. 기동요청→허가→Q→외부 컨택터→모터 앞부분과 수동/자동·정지 순서는 미확보다. 전용 start client motor 19 이름/writer는 명명 검색에서 확보하지 못했으며 다른 CLIENT Q61.x를 번호 연장해 지정하지 않는다.

### 고유 시간계수: 0307 document1017 FC2 NID19

1. rail W1104→Contact1100.in. T13 ORef1071/RID1 W1083→operand, out W1101→Contact1102.in. RUN I14.2 ORef1072/RID116 W1084→1102.operand.
2. 1102.out W1103은 Add1054.en 및 Ge1061.pre에 분기한다. Add1054 SrcType=Int: MIN ORef1073 W1085→in1, Int1 ORef1074/RID7 W1086→in2, out W1087→ORef1075 MIN. 허가 경로에서 MIN := MIN+1.
3. Ge1061 Int: MIN ORef1076 W1088→in1, Int60 ORef1077/RID8 W1089→in2. out W1090→Move1064.en.
4. Int1 ORef1078/RID7 W1092→Move1064.in; out1 W1093→ORef1079/RID120 HOUR. **HOUR := 1**이지 HOUR+1이 아니다.
5. 1064.eno W1094→Move1067.en. Int0 ORef1080/RID12 W1095→1067.in; out1 W1096→ORef1081 MIN. 1067.eno W1097→SCoil1070.in, operand W1098/ORef1082/RID13=M1.7 Set. ENO 연결을 생략하지 않는다.

0616 RID7/8/12는 각각 Constant Int 1/60/0이다. 실물 운전시간·타이머 정확도·외부 누적 저장 성공까지 확정하지 않는다.

### HOUR 다른 쓰기와 공유 타이머

0335 document1048 FC2 NID50: rail W2803→Contact2801.in, T17 ORef2775/RID284 W2786→operand. out W2802→Move2760.en, 그 eno W2789→2763.en, eno W2792→2766.en, eno W2795→**Move2769.en**. Int0 ORef2782/RID12 W2796→2769.in, out1 W2797→ORef2783/RID120=DB9.DBW74. 앞 세 Move는 타 CLIENT HOUR이고 CL19 소유로 집계하지 않는다. 2769.eno W2798은 뒤 BC01 Move2772로 이어진다. 이 ENO 의존 Reset 경로 때문에 DB9.W74를 영구 누적 HOUR로 단정할 수 없다.

0019 NID58: rail W3122→Contact3120.in. Negated operand는 T13 ORef3115/RID1 W3118, out W3121→SdCoil3112.in. value W3117/ORef3114/RID335는 0616 S5Time `S5T#1M`(V5632), operand W3119/ORef3116=T13. 공유 분 펄스 관련 원형으로 CL19 고장감시 지연이 아니다. T17 생성 및 M1.7/M2.0 외부 저장 ACK 상세는 SYS-RUNHOURS의 동일 고정원본 공통 근거를 연결 재사용한다. 외부 저장 시스템과 현재 실행은 미검증이다.

## 4. 전기 전달 끝점

`all-in-one/sources/Electrical_Rev2.pdf` 실제 PDF92/131을 직접 렌더했다. 페이지마다 footer **FG91/130, Rev2 17.03.2025, DATA 27.05.2024, TOT262**를 확인했다. FG=PDF−1은 이번 확인 두 쪽의 사실이며 전체 PDF의 일반 규칙이 아니다.

|경로|실제 원본 끝점|미확정|
|---|---|---|
|외부 RUN 접점, FG91/PDF92|+24Vdc10.7, 전원 역참조90/9→5x20 2A F→X1:314→선91.1→그려진 열린 접점→X1:315→E14.2 /130/3|외부 접점기기번호/상대단자/케이블 번호·규격·실제 정상극성 미기재|
|PLC 입력, FG130/PDF131|E14.2 역참조91/1→입력 단자23, CPU515 MOD11 표기, 이름 PRIMARY SHREDDER RUN|현재 CPU/장착 모듈 및 실물 운동·고장 의미 미확정|
|기동출력·전력|CL19 전용 Q writer/릴레이·컨택터/모터 전력·보호 끝점 미확보|다른 CL의 출력·릴레이·보호값을 복제하지 않음|

FG91의 PRIMARY SHREDDER RUN 가지와 FG130의 E14.2는 각각 SPARE 점선 안이다. 회로·태그가 존재해도 현장 사용 중이라고 판단할 수 없다. 인접 E14.3 CONSENT AVAILABLE은 별도 신호이며 자료 없이 CL19 전용 ready/허가로 배정하지 않는다. 열린 접점 그림은 정상극성·고장극성의 현장 증명이 아니다. 2A는 도면 표기만 기록한 것이며 현행 보호값·교체 권장이 아니다. 이 입력경로에 릴레이 부하5/9나 하단 접점표1/5/9를 가져오지 않는다. 외부 제어반 및 모터 내부 시퀀스·회로전원·안전인증은 미확보다.

## 5. 알람·복구

0236 document426, FC9 NID19의 제목은 `primary shradder fault (cl19)`다. 고유 전체 Part/Wire를 확인했다.

- 허가: rail W399→Contact391.in, ON ORef376/RID1 W382→operand. out W392→Contact393/395.in.
- Set: **PRIMARYSHREDDER RUN I14.2** ORef377/RID44 W383→Contact393.operand; out W394→SCoil370.in; operand W385/ORef378/RID43=DB3.DBX16.3. 식은 ON AND I14.2 → Set.
- Reset: 같은 I14.2 ORef379/RID44 W386→Contact395.operand가 Negated. out W396→Contact397.in, RESET_ALLARM ORef380/RID7 W387→operand; out W398→RCoil375.in, operand W389/ORef381/RID43=같은 경보. 식은 ON AND NOT I14.2 AND RESET_ALLARM → Reset.

이 네트워크에는 타이머 Part가 없다. 다른 CL의 FAULT 입력 주소 또는 2초 같은 고장지연을 복제하지 않는다. RUN이라는 이름과 fault 경보 제목·DB명 간 의미 상충을 유지한다. RUN=0 경보로 뒤집거나 독립 FAULT 입력으로 설명하면 원형과 반대가 된다. **I14.2=1일 때 이 Reset 가지는 성립하지 않는다**는 문서 논리 사실이며 실제 안전한 복구 조작을 뜻하지 않는다.

DB3.X16.3과 HMI Allarmi_132의 주소는 일치하지만 표시문구·ACK·사이렌·정지 영향의 고유 writer는 확인되지 않았다. 공통 DB3 집계/RESET 생성은 SYS-ALARM 참조 범위다. 원인 소멸, 내부 래치 해제, HMI ACK, 외부 제어반 Reset, 재기동 요청, 현장 복구는 별개다. 실제 운영 사용과 의도를 확인할 외부반 문서/현행 승인 교차참조가 필요하다.

## 6. 증상별 읽기 전용 관찰 기준

아래는 승인된 담당자가 제공하는 자료의 비교 기준이다. 출력강제·바이패스·보호변경·활선 점검·Reset 실행 지시가 아니다.

|증상|같은 시각 확보할 자료|비교·배제 근거|
|---|---|---|
|기동하지 않음|실물/프로젝트 식별, 실제 요청·허가·Q writer, 외부반 상태, I14.2|기동 앞부분 미확보. I14.2만으로 전력/모터 상태 판정 불가|
|RUN 표시와 fault 경보 동시|I14.2, DB13.X14.2, DB3.X16.3, M0.0 및 HMI 태그/표시 캡처|0236은 RUN이 참일 때 경보 Set. 명칭 상충을 코드 수정 없이 대조|
|Reset 표시 후 경보 지속|원시 I14.2, DB2.X6.0, M0.0, 유지경보의 전후 기록|NOT I14.2 조건과 별도 외부반 복구를 구별|
|실물 RUN과 HMI 불일치|I14.2/IW14/DB13.W14/X14.2 및 HMI003F7|외부접점→X1:314/315→FG130 단자23→0397 미러 각 단계 분리|
|운전시간 HOUR가 1/0 반복|I14.2, T13/T17, DB9.W72/W74, M1.7와 외부저장 로그|0307 Move1/0335 Move0/ENO 체인. 장기누적값 오인 금지|
|자료 주소/사용상태 불일치|현행 도면·승인 변경본·명판·SPARE 사용 근거|doc530 e15.2 주석과 I14.2 선언/도면 상충; 단자 변경 금지|

관찰자, 실제 시각/시간대, 위치, 값/단위, 수집장치, 현재 프로젝트 식별, 비교 도면/프로그램 판본, 사진·로그 출처, 원인 배제 및 승인된 조치·복구 증거는 별도 기록한다. 실제 운영·SEJIN 기록/사진을 복제하거나 변경하지 않았다.

## 7. 완료·누락·검증 경계

|영역|이번 문서 상태|남은 자료|
|---|---|---|
|설비·자료|적용|CL19 실물 동일성 및 SPARE 사용 여부|
|I/O·HMI|원시RUN/내부경보/시간/Word 미러 확인|독립FAULT/기동출력 존재 여부, 화면·이벤트·통신|
|제어|고유계수/다른쓰기/호출 확인|기동·정지·모드·허가·외부 순서|
|전기|입력 접점→PLC 두 쪽 실제 끝점 확인|외부 상대단자·케이블·전력·보호기 자료|
|알람·복구|고유 S/R와 무타이머 구조 확인|RUN/fault 의미 상충의 현행 의도와 실제 복구|
|증상관찰|읽기 전용 비교기준 작성|실제 관찰/로그 미취득|
|완료·누락|complete_with_gaps|UI·게시·TIA·현재CPU·현장 완료 아님|

다음 필요한 한 작업은 **현행 외부 Primary shredder 제어반 도면/프로그램과 X1:314/315 상대단자·I14.2 의미·SPARE 사용 승인 근거 확보 후 대조**다. 외부 제조사/모델/보호값/정상극성은 자료 없이 채우지 않는다. 새 자료 없이 같은 실물 보류를 반복 조사하지 않는다.

문서·래더/도면 비교 근거는 제공했으나 백업 미리보기/선택복원·전후비교·보고서/PDF의 로컬 UI 구현·저장/재읽기·재열기는 실행하지 않았다. note/repair_observation 미지 필드·사용자 초안·저장키·다른설비는 변경하지 않았다. 구현/통합/게시와 원본 generator/build/test는 범위 밖이다.

직접 의미검토 범위는 0236 전체 고유 S/R, 0307 전체 고유 계수, 0335의 T17 및 CL19까지 ENO 체인/Move0, 0397 IW14 미러, 0549 FC9/FC2 호출, 0019 T13이다. 전체 선정파일 해시는 모든 본문 의미검토 수가 아니다. XML 모든 네트워크·전체 I/O 도면 검증을 주장하지 않는다. 시뮬레이터 작성/수정/생성/실행/행동시험과 PLC/현장/보호값/SEJIN 변경은 없으며 중지5자산은 해시만 보존 확인했다.

상태: documentation `complete_with_gaps`; static_review `selected_original_xml_and_pdf_reviewed`; ui_records `not_run`; publication `not_published`; tia_compile/live_cpu/field_recovery `not_performed`. 부모 독립검토/첨부 대기.

추출·검사: `../extracts/CLIENT-CL19/declaration-search.json`, `selected-declarations.json`, `network-map.json`, `live_index.json`, `electrical-page-text.json`, 6개 pretty XML, PDF92/131 PNG, `verification.json`, `source-hashes.json`.

### 선정 원본 SHA256 + 고정 Git blob 전체 표

경로는 `source-mv06/` 기준. 고정커밋 `git show`의 내용과 현재 bytes를 직접 비교했다. 중지 자산은 보존 해시 확인만 했으며 논리 조사·실행하지 않았다.

검사 실제 시각: 2026-10-11T12:41:05.916610+00:00. 선정 40파일 고정 Git byte일치; 중지5자산 보존 True. 선언 검색 181파일은 의미검토 전수가 아니다.

|선정 원본 경로|SHA256|고정 Git blob|내용 일치|
|---|---|---|---|
|`AGENTS.md`|`0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2`|`073164bc6efd5791032d62c71b03b4dab48cb6f8`|True|
|`.agents/skills/gme-equipment-rollout/SKILL.md`|`fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b`|`9aa820ea6ca15b4e136c9772423b78ed4df6a3d4`|True|
|`docs/equipment-standard/WORK-STANDARD.md`|`05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99`|`f76a570cc73098632e08759b17934000f7e3a253`|True|
|`docs/equipment-standard/WORK-ITEM-TEMPLATE.md`|`4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586`|`e546f39535d2b589e80f97db869ac37ce4d05cfd`|True|
|`docs/equipment-standard/INVENTORY.json`|`720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc`|`587c3748ad9224718f95ba06463fee913dae231d`|True|
|`VERSION.json`|`5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7`|`fffb51663b7705aec91cb119ca80ee943a4ce758`|True|
|`WORKSPACE-HANDOFF.md`|`215096d997782e78e901dfae36c782937e49611fbeb677a0d3fa50cbecf8d074`|`dd0b8989d2376c4415bba9bd826fe6754c6b1a12`|True|
|`PUBLICATION_STATUS.md`|`efe4857aec598d90470322cf3962eb3fe1f64947630e1fdf71d1c90134de8740`|`d76401cf291fc0be681acc51fa898ad3ce46ff78`|True|
|`EXPANSION-WORK.md`|`ec624de9fd2fcfac861a67fd5e828b25ef46db50bfd7a37ff16e2cb54cd0f7e2`|`4c42d88ecc2d48269eb23e13a20ebf3721a092a1`|True|
|`all-in-one/ACTIVE-WORK.md`|`eff3bbc08ecff41da3beff77f3fec48e7d148708192bcaaab00f34b6a721afc2`|`6eb947c629b5ddf9c759ef87649451303938864b`|True|
|`all-in-one/sources/Electrical_Rev2.pdf`|`5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6`|`f610fd7c7ce14ae951b00cff57b969259bfb389d`|True|
|`all-in-one/sources/hmi_plc_tags.csv`|`a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404`|`cf4c0650e7c7baac350dcb89909b808435704880`|True|
|`all-in-one/sources/live_index.json`|`14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1`|`e35ccea1f841349c632666c29954b7bcd4f5839e`|True|
|`all-in-one/sources/decoded-original/network-map.json`|`c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60`|`424430b6b953e43138e5d0a18ca40c949e21cfa1`|True|
|`all-in-one/sources/decoded-original/0019-FlgNet.xml`|`a3301f4d07c2d36aefa6faa6c3559a1cff4565fc6de40cd17e54b548b30c0ce5`|`f78cfdbf5e717304114660ffbd3bb42cbed6d79d`|True|
|`all-in-one/sources/decoded-original/0236-FlgNet.xml`|`b5e41705ed6b7924841980f71f8a3c24758e2433914571a051e87de875dd5a4b`|`fad024a83d9caa193955804a6cd3eb3e2b04239f`|True|
|`all-in-one/sources/decoded-original/0307-FlgNet.xml`|`7b985a52bf2589306512c69dfd3d222e5341f7d5f7da58dca4a43786380d4446`|`b15a95a01a7c16b49b5c4385d411b4068ee5f62b`|True|
|`all-in-one/sources/decoded-original/0335-FlgNet.xml`|`6f0214de436cfaac95750cc25ba3d6f306d33174472618754fac38ad4caf4781`|`6f065e48bd456e656557f1f94896597028f42c5f`|True|
|`all-in-one/sources/decoded-original/0397-FlgNet.xml`|`bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834`|`4ab8370493c4e28fc1eabeeebe2743d27f0c4021`|True|
|`all-in-one/sources/decoded-original/0549-FlgNet.xml`|`49f7169c33ed7f54559b0801e21a7d618584900972840e91cf51ad032e8febb1`|`985b5310b43b1015b5dee286aa0e42800564b94b`|True|
|`all-in-one/sources/decoded-original/0599-IdentXmlPart.xml`|`32a693fe12134febbd9f5c7da10c3469ef4d5b164ab8b6bd9ea3867c358936c1`|`493de77fc827d8f14192ced05d82df3a062f7965`|True|
|`all-in-one/sources/decoded-original/0600-IdentXmlPart.xml`|`20c58ee0383d0b6c275bd2d96abd30af7c5d1f3fff59c7d5034cd758936b57d5`|`f22a7ededd0576cf379ee19908da067f08d45412`|True|
|`all-in-one/sources/decoded-original/0601-IdentXmlPart.xml`|`04c9481f7381284de689ef5c7ff40d7aea93f2004cd877a4e4f27e47baa6d862`|`07bcf656fa58e4a305999456644acd24b3dc6bec`|True|
|`all-in-one/sources/decoded-original/0613-IdentXmlPart.xml`|`09d3b1397a987898334218f37e025661af162438582e649f671e7abec443d3cb`|`c9d19a48e947098914f4d2de3348c05b4f6d37e8`|True|
|`all-in-one/sources/decoded-original/0614-IdentXmlPart.xml`|`c6de26f74d75f5be858a406de75eaf6faf62ba9b89c8f9a085b5dd206e93d294`|`da0485aa033700f08c8695d30b93ebd2d377d6c7`|True|
|`all-in-one/sources/decoded-original/0615-IdentXmlPart.xml`|`80f4544edca56c6e6bb2713c758c92ade9202255110074931e03fe34d0d0801a`|`49eb86fe01feb83de8c0864b21493d305aff8b20`|True|
|`all-in-one/sources/decoded-original/0616-IdentXmlPart.xml`|`650b53354a0c8443d94adc5bd6a860d3c5313014a52e0fb98a5656a65b58cc0d`|`9f7fdd5f93ac149c139a054ebb34f63c632ef7fd`|True|
|`all-in-one/sources/decoded-original/0627-IdentXmlPart.xml`|`08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb`|`61ebc0abbb2ca160e11e1da400a3f14a397d8bc5`|True|
|`all-in-one/sources/decoded-original/0628-IdentXmlPart.xml`|`9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd`|`170ca5c72599edc7ea7eefe651c3680ce325e76a`|True|
|`all-in-one/sources/decoded-original/0629-IdentXmlPart.xml`|`67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972`|`058129bb01e27f7a6a0d0293f332d745e5bab74e`|True|
|`all-in-one/sources/decoded-original/0688-IdentXmlPart.xml`|`ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda`|`463585759f1ecd94f32362b4fefb000a152f5773`|True|
|`all-in-one/sources/decoded-original/0692-IdentXmlPart.xml`|`bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037`|`737785d03b5fad43c5b4d451955726d800edb1c0`|True|
|`all-in-one/sources/decoded-original/0694-IdentXmlPart.xml`|`757ccebdf32d0a168dd787bfa735fe6494eac4c4a9f7a5adc63898a88e8b152d`|`c45e8f3ca4129dc06734f6a12ef79e6ed6528a7d`|True|
|`all-in-one/sources/electrical-page-text.json`|`4b846819aab7e1306aebea617042f9f9ffe0c8aee1930e6f3db035bea3739153`|`1f48073c07b28e668d3d72d5ce49db263a5214e6`|True|
|`all-in-one/registers/simulator-freeze.json`|`bb93c1994effc5609939ba566b7802ce7ed55154a7310f02379b308ac2c8c835`|`808ffac14dbd1b4a7d797fa6cd0d647635d90b47`|True|
|`all-in-one/registers/program-model.json`|`6203479c086b15bada12ac9d7e37db9280234ec26f1ea6091d7211dc09a577c5`|`9860b10f008d3a5ae714be50d77b703dfec32f3a`|True|
|`all-in-one/assets/program-model-data.js`|`52f8199371e3399b7c0d44ab5469f0472aced79d56bbef2887f7625f5d2aff0f`|`38f34b0caa380a16ccad6f6f1e234a2fdf23f327`|True|
|`all-in-one/assets/virtual-plc.js`|`5f1876052dc0067b1f010af0dfc941946e37003167481731293615d9c1c36dbc`|`0bd9eceb54365a91214a37c5601b5067c39a3f75`|True|
|`all-in-one/assets/simulator-workspace.js`|`3a6dfc618ff7e7b238f2671dc85d65704f33093a18eac879d86081d92c31e8bc`|`97c2c831c77a9699fff0e0960b3bc1b7d93d45b3`|True|
|`all-in-one/registers/virtual-plc-test-results.json`|`a6b389f797f9a8b5ffe6928b8420f55c4cc459a327b0b48d716079d2eca6dd64`|`757dd50e45184568facb8ff62900b39d3ce848d1`|True|
