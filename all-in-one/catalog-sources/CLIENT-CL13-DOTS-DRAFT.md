# CLIENT-CL13 · Apron conveyor B · 7영역 원본 조사 초안

고정 원본: `source-mv06`, Git `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, v1.12.0. 문서 조사만 수행했다. 실물·현재 CPU·TIA 컴파일·현장 복구·로컬 기능 구현/게시 완료를 뜻하지 않는다. 모델 런타임 증명은 미확인이다.

## 핵심 확인·상충·누락·공유근거

- 독립 확인: RUN I13.5, FAULT I16.0, 유지경보 DB3.DBX15.5, MIN DB9.DBW48, HOUR DB9.DBW50. 0230 FC9 NID13과 0302 FC2 NID13의 전체 핀, 0334 NID49의 CL13 쓰기를 원본 XML로 결속했다.
- 독립 전기 확인: FG90/PDF91 X1:304/305 → FG129/PDF130 입력16; FG93/PDF94 X1:342/343 → FG132/PDF133 입력1. 실제 렌더 네 쪽 모두 Rev2 17.03.2025, DATA 27.05.2024.
- 상충: RUN 백업 comment는 `e 14.4`, FAULT comment는 `e19.2`이나 Address와 XML·전기도면은 각각 I13.5/I16.0이다. 과거 comment를 현재 주소로 대체하지 않는다.
- 누락: CL13 기동 출력 심볼/실행 writer/릴레이·접촉기·외부 제어반 내부 시퀀스·상대단자·현행 보호값·정상극성·실물 동일성. 다른 CLIENT의 Q61.x를 순번으로 배정하지 않았다.
- 공유근거: [CLIENT-CL09](CLIENT-CL09-DOTS-DRAFT.md)를 공통 FC9/FC2 호출·Word 미러·타이머 구조의 색인으로 사용했다. 공유 원본 0549/0397/0019와 관련 선언의 선택 핀은 다시 확인했다. SYS-ALARM/SYS-RUNHOURS의 공통 Reset 생성·집계·저장 경계는 해당 기존 문서에 연결하며 CL13 전체 소유로 확대하지 않는다.

## 1. 설비·자료 기준

적용. `docs/equipment-standard/INVENTORY.json#/catalog/67`의 CLIENT-CL13, Apron conveyor B, client/외부 연동, parent 없음, phase2 항목 하나만 조사했다. 별칭은 motor_client_13 / client motor 13 / cl13 / apron conveyor b이다. 대장의 planned와 not_assessed를 현장 완료로 변경하지 않는다. 공압 CYL-CL 이름 공간과 별개이며 같은 숫자만으로 병합하지 않는다. CL11/12 독립 catalog ID를 발명하지 않는다.

원본 경로 축약: 아래 XML 번호는 모두 `all-in-one/sources/decoded-original/NNNN-FlgNet.xml` 또는 `NNNN-IdentXmlPart.xml`을 뜻한다. `network-map.json`과 `live_index.json`은 탐색·문맥 색인이고 핵심 선언/논리는 XML로 확인했다. OEM 전기 원본은 `all-in-one/sources/Electrical_Rev2.pdf`, HMI 원본은 `all-in-one/sources/hmi_plc_tags.csv`이다. 원본 문서는 외부 설비의 실제 설치·사용 증명이 아니다. 선택 도면에는 SPARE 구획이 있다.

AGENTS·작업 스킬·WORK-STANDARD·WORK-ITEM-TEMPLATE·대장 및 판본/인계 최상단을 읽었다. 이번 권한은 배정 extracts와 본 초안 작성뿐이다. 원본 코드/발전기/build/test/시뮬레이터/실PLC/현장/보호값/SEJIN 변경·실행은 하지 않았다. 로컬 통합은 별도 담당이다.

## 2. I/O·HMI

적용. AO는 bit offset이며 DB 번호는 BAD→DepDBBlock TOD로 확인한다. 아래 범위는 모두 Global이고 Local 가상주소로 바꾸지 않는다.

|대상|선언·문맥|주소/형식·해석|
|---|---|---|
|APRON CONVEYOR B RUN|0613 RID80, SSD AO109, SAD Input SAM=None; FC2 NID13 UID748|I13.5 Bool. 실제 회전/이송 상태 자체가 아니라 외부 RUN 입력|
|APRON CONVEYOR B FAULT|0599 RID30 AO128, SAD Input SAM=None; FC9 NID13 UID269/271|I16.0 Bool. 외부 고장 내용과 정상극성 미확정|
|Allarm.motor_client_13_fault|0601 RID31 AO125 BAD4; 0600 RID4 TOD3; NID13 UID270/273 Write|DB3.DBX15.5 Bool, Set/Reset 유지비트|
|ON|0599 RID1 AO0 SAD Memory; NID13 UID268|M0.0 Bool, 공통 논리 허가|
|Flag.RESET_ALLARM|0601 RID7 AO48 BAD6; 0600 RID6 TOD2; UID272|DB2.DBX6.0 Bool, 내부 Reset 신호이며 HMI ACK와 동일하지 않음|
|CLIENT_MOTOR_13_MIN|0615 RID82 AO384 BAD5; 0614 RID5 TOD9; UID749/751/752/757|DB9.DBW48 Int, Add+1 및 Move0 쓰기|
|CLIENT_MOTOR_13_HOUR|0615 RID84 AO400 BAD5; UID755(NID13),2719(NID49) Write|DB9.DBW50 Int, Move1/Move0. 장기 누적시간으로 단정 금지|
|Tag_47 / Tag_48|0613 RID1 AO13 Timer / RID284 AO17 Timer|T13/T17, 공유 시간계수/저장 관련 PLC 타이머|
|Flag_Aggiorna_DB|0613 RID13 AO15 Memory; NID13 UID758 Write|M1.7 Bool, 저장 갱신 요청 관련 Set|

HMI CSV: `APRON_CONVEYOR_B_RUN,"DB13,X13.5",PLC,003FB`, `Allarmi_126,"DB3,X15.5",PLC,0010F`이다. 전자는 입력 미러, 후자는 유지경보 주소에 대응한다. CSV 설정만으로 실제 화면 문구·객체·이벤트·통신·ACK/Reset·권한을 확인했다고 쓰지 않는다. 고유 기동 버튼/쓰기 이벤트 및 DB9 HMI 직접 태그는 미확보다.

### Word 미러와 bit 유지경보 분리

0397 document1070 `hmi inputs` NID1: rail W21→Move60.en. ORef63/RID19(0627 Word AO96 Input SAM=None) W70→Move60.in; out1 W72→ORef64/RID20(0629 Word AO96 BAD4→0628 TOD13). **IW12→DB13.DBW12**로 I13.5가 포함된다.

Move60.eno W71→Move61.en; Move61.eno W74→Move62.en. ORef67/RID23(0627 Word AO128) W76→Move62.in; out1 W77→ORef68/RID24(0629 Word AO128 BAD4). **IW16→DB13.DBW16**에 I16.0이 포함된다. 중간 Move61은 IW14→DB13.DBW14이고 CL13 두 신호의 개별 원인비트가 아니다. Move60/61/62의 DisableENO=true 속성과 원문 eno/en 연결을 함께 보존한다. 독립 Bool Coil/PIW 접근/DB3 경보쓰기와 혼동하지 않는다. 전체 FC15 호출 및 다른 writer에 따른 현재 스캔 최종값·통신 상태는 미검증이다.

## 3. 제어 구조

### 3.1 호출 경계

0549 Main document1620 NID7: rail W352→Contact350.in, ON ORef335/RID52(0692 Global Memory AO0) W348→operand. 350.out W351은 CRef331/334.en에 병렬 연결된다. CRef331 RefId80 안 CodeBlock345 RefId79→0688 RID79 TOD9 FC `Motor/Alarm Client`; 0694 RID80 NID7 UID331 TORID79. CRef334 RefId83 안 CodeBlock347 RefId82→0688 RID82 TOD2 FC `time work motor`; 0694 RID83 NID7 UID334 TORID82. FC9 ENO 뒤에 FC2가 직렬 허가되는 것으로 바꾸지 않는다. 현재 CPU 실행·스캔주기는 미확인이다.

### 3.2 CL13 시간계수 고유 핀

0302 document1012, FC2 NID13:

1. rail W780→Contact776.in; T13 ORef747/RID1 W759→operand. 776.out W777→Contact778.in; RUN I13.5 ORef748/RID80 W760→operand.
2. 778.out W779는 Add730.en과 Ge737.pre에 분기한다. Add730 SrcType Int: MIN ORef749/RID82 W761→in1, Int1 ORef750/RID7 W762→in2, out W763→ORef751/RID82 MIN이다.
3. Ge737 SrcType Int: MIN ORef752 W764→in1, Int60 ORef753/RID8 W765→in2; out W766→Move740.en.
4. Move740.in W768/ORef754/RID7=Int1; out1 W769/ORef755/RID84=HOUR. **HOUR:=1**이며 HOUR+1이 아니다.
5. Move740.eno W770→Move743.en. Int0 ORef756/RID12 W771→in; out1 W772/ORef757/RID82=MIN. Move743.eno W773→SCoil746.in; operand W774/ORef758/RID13=M1.7 Set. ENO 조건을 생략하지 않는다.

0334 document1047, FC2 NID49의 다른 writer: T17 ORef2713/RID284 W2724→Contact2739.operand; rail W2741→in; out W2740→Move2698.en. Move2698.eno W2727→Move2701.en; 2701.eno W2730→Move2704.en. **Move2704.in W2731/ORef2718/RID12=Int0 → out1 W2732/ORef2719/RID84=DB9.DBW50**이다. 나머지 주변 CLIENT writer를 CL13 소유나 완료로 집계하지 않았다.

공유 0019 FC2 NID58: Contact3120의 operand는 NOT(T13 ORef3115/RID1/W3118), out W3121→SdCoil3112.in. value W3117/ORef3114/RID335는 0616 S5Time `S5T#1M`(V5632), operand W3119/ORef3116=T13이다. 이것은 분 계수용 공유 타이머이며 CL13 기동/FAULT 지연이 아니다. T17 저장/ACK 경계는 SYS-RUNHOURS 공통 조사 범위를 재사용한다. MIN/HOUR 값만으로 장기누적·저장 성공·정확한 현행 운전시간을 입증하지 않는다.

### 3.3 명령·정지의 누락

IdentXmlPart 181개에서 이름 기준으로 찾은 CL13 고유 선언은 RUN/FAULT/경보/MIN/HOUR 다섯 항목이다. live_index의 `start client` 명명 출력 검색에는 4/6/8/9/10 심볼이 있으나 CL13 기동 심볼은 확인되지 않았다. 이는 선택 검색 결과이며 간접/절대주소/블록복사 모든 writer 부재의 증명이 아니다. Q61.7 등을 번호로 추정하지 않는다. 외부 기동·정지·수동/자동·허가·속도·드라이브·보호 시퀀스는 근거 미확보이며 비해당으로 처리하지 않는다.

## 4. 전기 전달 끝점

적용. `Electrical_Rev2.pdf` 실제 PDF91/94/130/133쪽을 렌더하여 각 footer와 끝점을 직접 보았다. 네 쪽 각각 **Rev2 17.03.2025 / DATA 27.05.2024**다. FG 번호를 PDF 페이지에서 일괄 뺄셈한 것이 아니다.

|경로|직접 관찰 끝점|한계|
|---|---|---|
|RUN 외부 접점|FG90/PDF91: +24Vdc10.7→5x20 2A F, X1:304→선90.1→그린 열린 접점→X1:305→E13.5 /129/5|외부 상대 단자·접점기기명·케이블 번호/규격 미확보|
|RUN PLC 입력|FG129/PDF130: E13.5 역참조90/1→입력 단자16, 표기 CPU515 MOD11|현재 CPU/장착모듈/실물배선 확인 아님|
|FAULT 외부 접점|FG93/PDF94: +24Vdc10.7→5x20 2A F, X1:342→선93.5→열린 접점→X1:343→E16.0 /132/2|고장 종류·정상극성·외부 보호값 미확정|
|FAULT PLC 입력|FG132/PDF133: E16.0 역참조93/7→입력 단자1, 표기 CPU515 MOD12|외부 제어반 내부와 보호 Reset 회로 미확보|
|RUN 입력 보조전원|FG129/PDF130: +24Vdc10.7→X21:3012 5x20 2A IST.→129.1→단자19, -0Vdc10.6→20|도면 정격이며 현행 보호설정/교체 추천 아님|
|기동 출력/동력|CL13 고유 출력·릴레이·접촉기·드라이브·모터 끝점 미확보|RUN/FAULT를 기동명령으로 바꾸거나 인접 채널 출력 복제 금지|

FG90와 FG93 전체 외부 접점은 SPARE 점선 안이다. FG129의 I13.0~7 및 FG132의 I16.0~3도 SPARE 구획 안이다. 따라서 그림상 열린 접점이 현장 정상극성/실사용을 확정하지 않는다. 다른 장치 릴레이 부하5/9 또는 하단 접점표1/5/9를 이 입력 경로에 복제하지 않는다. 외부 Apron conveyor B 제어반·모터 동력회로·케이블표 및 현행 도면이 있어야 양 끝점을 완결할 수 있다.

## 5. 알람·복구

적용. 0230 document420 `motor/alarm client`, FC9 NID13의 전체 고유 경로:

- rail W291→Contact283.in; ON ORef268/RID1 W274→operand. 283.out W284가 Contact285와 Contact287.in으로 분기한다.
- Set: I16.0 ORef269/RID30 W275→Contact285.operand; out W286→SCoil262.in; operand W277/ORef270/RID31=DB3.X15.5. **ON AND I16.0 → Set**.
- Reset: I16.0 ORef271/RID30 W278→Contact287.operand는 Negated다. out W288→Contact289.in; RESET_ALLARM ORef272/RID7 W279→operand; out W290→RCoil267.in, operand W281/ORef273/RID31=같은 경보. **ON AND NOT I16.0 AND RESET_ALLARM → Reset**.

0230에 타이머 Part는 없다. RUN I13.5=0이나 공유 T13 시간을 이 경보 원인/지연에 추가하지 않는다. I16.0이 참이면 위 Reset 가지는 성립하지 않는다. 원시 FAULT 소멸, DB3 유지경보 해제, HMI ACK, 외부 제어반 자체 Reset, 재기동, 실제 정상복구는 별개다. Allarmi_126 주소는 유지비트와 일치하나 표시문구·경보이력/소리·ACK 이벤트는 미확정이다. 공통 DB3 집계/Reset 생성은 SYS-ALARM의 같은 고정입력 근거를 연결한다. 이 경보가 Apron conveyor B의 전력을 직접 차단하는 인과·출력 writer는 미확보다.

## 6. 증상별 읽기 전용 관찰 기준

적용. 승인된 담당자가 제공한 자료를 비교할 지점이며 현장 조작 지시가 아니다. 강제출력·바이패스·활선 점검·보호값 변경·Reset 실행을 수행하거나 권하지 않는다.

|증상|같은 시각 비교할 값/위치|판단 경계|
|---|---|---|
|현장 RUN이나 HMI 미표시|I13.5, IW12, DB13.W12/X13.5, HMI003FB, X1:304/305와 입력16 자료|원시입력·Word미러·통신·화면 구분. 배선/극성 고장 단정 금지|
|컨베이어 정지인데 RUN 표시|외부 RUN 접점의 정의, I13.5, 동시 실제 이송상태 기록|RUN 입력이 실제 움직임을 완전 대변한다고 가정하지 않음|
|FAULT 화면과 현장 불일치|I16.0, DB13.X16.0, DB3.X15.5, Allarmi_126, X1:342/343와 입력1|원시값과 래치, 외부 보호 원인 구분|
|외부 고장 소멸 후 경보 유지|ON, I16.0, RESET_ALLARM DB2.X6.0, DB3.X15.5, HMI 이벤트|NOT FAULT Reset 조건과 실제 복구 분리|
|기동 버튼에도 움직이지 않음|현행 HMI 이벤트·명령 writer·허가표·외부 제어반 로그|고유 출력 미확보. 다른 CL의 Q61.x를 대신 보지 않음|
|시간 값 1/0 반복|I13.5,T13,T17,DB9.W48/W50,M1.7,저장 로그|Move1/Move0와 장기누적 저장 경계 구분|
|주석과 주소 불일치|백업 판본·현행 프로젝트·모듈표찰·도면개정·사진 출처|e14.4/e19.2 주석을 유지하고 임의 배선수정하지 않음|

관찰자·실제 시각/시간대·장치 위치·값/단위·자료 판본·사진/로그 출처·비교결과·원인 배제·승인된 조치·복구 증거를 별도로 수집해야 한다. 현장 관찰값이나 SEJIN 운영 기록을 이번 문서에 만들어 넣지 않았다.

## 7. 완료·누락·검증

|영역|문서 상태|추가 필요|
|---|---|---|
|설비·자료 기준|적용, 고유 ID 분리|실물 동일성·실사용 여부|
|I/O·HMI|고유 선언·CSV·Word미러 선택 검토|기동 출력·HMI 실제 이벤트/통신|
|제어|FC9/FC2 고유핀·호출/복수쓰기 확인|외부 기동/정지/수자동/허가|
|전기|네 실제 렌더 끝점/개정 확인|외부 상대단자·케이블·전력·현행 판본|
|알람·복구|S/R·NOT·무타이머 확인|외부 원인·ACK·현장 복구|
|증상 관찰|읽기 전용 비교 기준 작성|실제 관찰자료|
|완료·누락|documentation complete_with_gaps|BC01 동등 구현/게시/현장 완료 아님|

필요자료: 외부 Apron conveyor B 제어반 프로그램·회로·기동허가표, 현재 프로젝트에서 CL13 명령 출력의 간접/절대주소 포함 교차참조, X1:304/305/342/343 상대 단자 및 케이블표, SPARE 표기와 실제 사용 여부, HMI 화면 이벤트·스크립트, 명판/현행 보호 문서 및 승인된 정상상태 근거. 새 자료 없이 같은 실물 보류를 반복 조사하지 않는다.

백업 미리보기/선택복원, 기록 전후비교, 관찰 보고서/PDF 등의 기능 구현·저장·재읽기·재열기는 수행하지 않았다. 기존 note/repair_observation/미지 필드·초안·저장키·타설비 자료는 변경하지 않았다. documentation=`complete_with_gaps`; static_review=`selected_original_xml_and_pdf_reviewed`; ui_records=`not_run`; publication=`not_published`; tia_compile/live_cpu/field_recovery=`not_performed`.

### 검색·의미검토·해시 구분

181개 IdentXmlPart 이름 검색은 전체181개 의미검토가 아니다. 직접 고유 의미검토는 0230 전체 핀, 0302 전체 핀, 0334 CL13 쓰기와 관련 ENO 체인, 선택 선언이다. 공유 원본 선택 재확인은 0397 IW12/IW16 Word 경로, 0549 FC 호출, 0019 T13 가지이다. PDF 전체 의미검토가 아니라 실제91/94/130/133 네 쪽 시각검토다. 아래 선정 원본 byte 검증 개수 역시 전체 논리 의미검토 개수와 다르다.

검사·해시·원형 추출·렌더: `../extracts/CLIENT-CL13/verification.json`, `source-hashes.json`, `declaration-search.json`, `live-symbols.json`, `common-declarations.txt`, `stages.json` 및 같은 디렉터리. 원본은 읽기 전용이며 본 MD와 자기 extracts만 작성했다.

### 선정 원본 SHA256 + 고정 Git blob 전체 표

경로는 `source-mv06/` 기준. 각 로컬 byte를 고정 commit의 `git show` byte와 직접 비교했다.

|원본 경로|SHA256|Git blob|내용 일치|
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
|`EXPANSION-WORK.md`|`ec624de9fd2fcfac861a67fd5e828b25ef46db50bfd7a37ff16e2cb54cd0f7e2`|`4c42d88ecc2d48269eb23e13a20ebf3721a092a1`|일치|
|`all-in-one/sources/Electrical_Rev2.pdf`|`5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6`|`f610fd7c7ce14ae951b00cff57b969259bfb389d`|일치|
|`all-in-one/sources/hmi_plc_tags.csv`|`a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404`|`cf4c0650e7c7baac350dcb89909b808435704880`|일치|
|`all-in-one/sources/live_index.json`|`14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1`|`e35ccea1f841349c632666c29954b7bcd4f5839e`|일치|
|`all-in-one/sources/decoded-original/network-map.json`|`c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60`|`424430b6b953e43138e5d0a18ca40c949e21cfa1`|일치|
|`all-in-one/sources/decoded-original/0019-FlgNet.xml`|`a3301f4d07c2d36aefa6faa6c3559a1cff4565fc6de40cd17e54b548b30c0ce5`|`f78cfdbf5e717304114660ffbd3bb42cbed6d79d`|일치|
|`all-in-one/sources/decoded-original/0230-FlgNet.xml`|`96ee91a4c8e5349befca65989d2ae32a07bd7c0344cdb68419d12fa27db947c2`|`fc7ac243227eae74638aaa5b39419611e923663b`|일치|
|`all-in-one/sources/decoded-original/0302-FlgNet.xml`|`b5e69b459caae2929f037343ccbdba1da28b523c39371cff1583c7b96b21e6ba`|`2a35aa4ec31de80589b66119d5269c53c53f4b66`|일치|
|`all-in-one/sources/decoded-original/0334-FlgNet.xml`|`d76007d20f67bcb8f127fef6e7050e0973619a35ef4f5c34c367dc3b3c38932e`|`7310cc3d9a1324fa17c3c7ea7b8ffe1c62be96fa`|일치|
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

선정 원본 33개 내용 일치. 초안 작성 완료 실제시각: 2026-10-11T12:35:28.061955+00:00
