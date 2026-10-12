# CLIENT-CL16 · Belt conveyor E · 7영역 원본 조사 초안

## 핵심 확인·상충·공유 근거

- 고유 원본으로 확인: RUN I14.0, FAULT I16.3, 유지경보 DB3.DBX16.0, 분 계수 DB9.DBW60 및 HOUR 전달 필드 DB9.DBW62. 고유 0233/0305/0335 XML의 선언·핀을 대조했다.
- 실제 PDF91/95/131/133 렌더 확인: FG90 X1:310/311→FG130 입력21, FG94 X1:348/349→FG132 입력4. 네 페이지 모두 Rev2 17.03.2025 / DATA 27.05.2024. RUN/FAULT 회로가 SPARE 점선에 포함된다.
- 상충 보존: live_index doc528의 과거 주석 e14.7과 실제 I14.0, doc564의 e19.5와 실제 I16.3은 다르다. 주석으로 주소를 덮어쓰지 않았다.
- 누락: CL16 전용 기동 출력 심볼/실제 writer/전력 회로/외부 제어반 내부 시퀀스는 미확보. CL09·CL10의 Q61.x를 번호로 연장하거나 CL16에 복제하지 않는다. 실제 사용·정상극성·보호값·복구 완료는 미확정이다.
- 공유 근거: [CLIENT-CL09](CLIENT-CL09-DOTS-DRAFT.md), [SYS-RUNHOURS](SYS-RUNHOURS-DOTS-DRAFT.md), [SYS-ALARM](SYS-ALARM-DOTS-DRAFT.md)을 공통 색인으로 활용했다. 0549 호출/0019 T13/0397 Word 미러의 필요한 원형 핀은 재확인했다. 다른 CLIENT의 고유 주소·타이머·끝점은 복제하지 않았다.

## 1. 설비·자료 기준

대장은 `docs/equipment-standard/INVENTORY.json#/catalog/70`: CLIENT-CL16, Belt conveyor E, client, 외부 연동, 부모 없음, phase2다. 외부 벨트 컨베이어 E의 PLC 인터페이스 채널을 다룬다. 공압 CYL-CL 번호와 별도 이름 공간이며 실물 동일성 확인이나 부모/하위 동시완료가 아니다.

읽기 전용 기준 `source-mv06` Git `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, v1.12.0. NNNN은 `all-in-one/sources/decoded-original/NNNN-FlgNet.xml` 또는 동일 번호 IdentXmlPart.xml 약칭이다. 파일번호/document_id/NID/UID는 서로 다른 식별자다. live_index와 network-map은 탐색 색인이고 핵심 판단은 원형 선언 및 회로를 사용했다.

실제 작업 시각(UTC): 2026-10-11 12:33:09 착수, 12:33:22~12:34:22 XML/선언·HMI 및 공유 핀 확인, 12:33:53 렌더 준비, 12:33:57~12:34:02 네 PDF쪽 시각 검토. 해시 및 검사 생성 시각은 아래 기록 참조. 모델·추론 런타임 증명 미확인. 로컬 통합·UI·게시·TIA·현재 CPU·현장 검증은 수행하지 않았다.

## 2. I/O·HMI

### 고유 선언과 주소

|신호|원형 선언/참조|자료 의미·경계|
|---|---|---|
|BELT CONVEYOR E RUN|0613 RID98 Global Bool, SSD AO112, Input SAM=None; NID16 UID910 → I14.0|원시 입력영상; 실물 벨트 운동의 직접 증명 아님|
|BELT CONVEYOR  E FAULT|0599 RID36 Global Bool AO131 Input SAM=None; NID16 UID323/325 → I16.3|0233 유지경보 원인 입력|
|Allarm.motor_client_16_fault|0601 RID37 Global Bool AO128 BAD4→0600 RID4 TOD3; NID16 UID324/327 Write → DB3.DBX16.0|내부 Set/Reset 경보, 원시 FAULT 및 HMI ACK와 별도|
|Flag.RESET_ALLARM|0601 RID7 Global Bool AO48 BAD6→0600 RID6 TOD2; NID16 UID326 → DB2.DBX6.0|내부 공통 Reset 조건|
|ON|0599 RID1 Global Bool AO0 SAD Memory; NID16 UID322 → M0.0|명칭만으로 상수 true로 간주하지 않음|
|CLIENT_MOTOR_16_MIN|0615 RID100 Global Int AO480 BAD5→0614 RID5 TOD9; NID16 UID911/913/914/919 → DB9.DBW60|Add+1, 비교, Move0 대상|
|CLIENT_MOTOR_16_HOUR|0615 RID102 Global Int AO496 BAD5; NID16 UID917 및 NID50 UID2777 Write → DB9.DBW62|Move1 및 Move0; 자체 누적 Add가 아님|
|Tag_47 / Tag_48|0613 RID1 Timer AO13 / RID284 Timer AO17 → T13/T17|공유 시간계수·전달용 PLC 타이머; HMI 태그/CL16 기동감시 타이머 아님|
|Flag_Aggiorna_DB|0613 RID13 Global Bool Memory AO15; NID16 UID920 Write → M1.7|공유 저장 갱신 요청 관련 Set 비트|

선언 Scope은 위 Global과 0616의 Constant이며 Local로 바꾸지 않았다. 형식은 Bool/Int/Word/Timer/S5Time을 구분했다. IdentXmlPart 181개와 XmlPartIdentMapping 42개를 포함한 `*Ident*.xml` 223개 파일의 명명 검색에서 CL16 RUN/FAULT/경보/MIN/HOUR 5항목을 확인했다. 이는 선언 검색이지 모든 네트워크 의미검토나 절대/간접쓰기 부재의 증명이 아니다. `start client motor 16`은 live_index 명명 검색에서 0건이며 다른 출력의 실제 소유를 번호로 추정하지 않는다.

### HMI 및 Word 미러

`all-in-one/sources/hmi_plc_tags.csv`에서 `BELT_CONVEYOR_E_RUN,"DB13,X14.0",PLC,003F8`과 `Allarmi_129,"DB3,X16.0",PLC,0010C`를 직접 확인했다. 전자는 가공 입력 미러, 후자는 유지경보다. 태그 설정과 실제 화면·문구·이벤트·스크립트·권한·통신·ACK는 별개다. MIN/HOUR 화면 및 기동 버튼 이벤트는 미확보다.

0397 HMI Inputs NID1은 Bool Coil이 아닌 Word 복사다.

|결속|원형 핀·선언|해석|
|---|---|---|
|IW14→DB13.DBW14|0627 RID21 Tag_274 Word AO112 SAD Input SAM=None, ORef65 W73→Move61.in; Move60.eno W71→61.en; 61.out1 W75→ORef66/0629 RID22 Word AO112 BAD4→0628 RID4 TOD13|I14.0 RUN을 포함하는 byte14~15 미러|
|IW16→DB13.DBW16|0627 RID23 Tag_275 Word AO128, ORef67 W76→Move62.in; Move61.eno W74→62.en; 62.out1 W77→ORef68/0629 RID24 Word AO128 BAD4|I16.3 FAULT를 포함하는 byte16~17 미러|

Move60의 en은 rail W21, Move60/61/62의 DisableENO=true와 원형 eno/en 연결을 함께 보존한다. PIW/Peripherie 읽기로 변경하거나 bit별 별도 writer로 세지 않는다. FC15 상위 호출과 다른 writer·현재 스캔 최종값은 공통 경계로 남긴다.

## 3. 제어 구조

### 상위 호출과 출력 소유

0549 Main document1620 NID7: rail W352→Contact350.in, ORef335 RefId52 W348→operand(0692 ON), out W351은 CRef331/334의 en에 병렬이다. CRef331 RefId80/CodeBlock345 RefId79는 0688 RID79 `Motor/Alarm Client` TOD9 FC 및 0694 RID80 TORID79에 대응한다. CRef334 RefId83/CodeBlock347 RefId82는 0688 RID82 `time work motor` TOD2 FC, 0694 RID83 TORID82다. 앞 FC의 ENO가 뒤 FC의 순차 허가라는 해석은 하지 않는다.

확인된 경로는 외부 RUN/FAULT 입력→FC2 계수/FC9 유지경보→DB 및 HMI 미러다. 요청→허가→기동출력→외부 컨택터→모터의 앞부분은 미확보다. 수자동·정지·재기동·외부 보호 시퀀스를 발명하지 않는다.

### 고유 시간계수: 0305, document1015, FC2 NID16

1. rail W942→Contact938.in. T13 ORef909/RID1 W921→938.operand; 938.out W939→Contact940.in; RUN I14.0 ORef910/RID98 W922→940.operand.
2. 940.out W941이 Add892.en 및 Ge899.pre에 분기한다. Add892 SrcType Int의 in1은 MIN ORef911 W923, in2는 Int1 ORef912/RID7 W924; out W925→ORef913 MIN. 즉 허가 경로에서 MIN := MIN + 1.
3. Ge899 Int는 MIN ORef914 W926→in1, Int60 ORef915/RID8 W927→in2. 비교 out W928→Move902.en.
4. Move902.in W930/ORef916/RID7=Int1, out1 W931/ORef917/RID102=HOUR. **HOUR := 1**이며 HOUR+1 누적이 아니다.
5. 902.eno W932→Move905.en. Int0 ORef918/RID12 W933→905.in; out1 W934→ORef919 MIN. 905.eno W935→SCoil908.in, operand W936/ORef920/RID13=M1.7 Set. ENO 체인을 생략하지 않는다.

0616 RID7/8/12는 Int 1/60/0이다. 원시 입력의 불명확한 정상극성이나 실제 시간 정확도는 이 코드로 확정하지 않는다.

### 다른 writer 및 공유 타이머

0335 document1048 FC2 NID50: rail W2803→Contact2801.in, T17 ORef2775/RID284 W2786→operand. out W2802→Move2760.en, Int0 ORef2776/RID12 W2787→in, out1 W2788→ORef2777/RID102=DB9.DBW62. HOUR 필드는 이 경로에서 0으로 다시 쓰인다. 2760.eno W2789는 다음 타설비 Move2763으로 이어지며 타설비를 CL16 소유로 집계하지 않는다.

0019 NID58: Contact3120의 Negated operand는 T13 ORef3115/RID1 W3118, rail W3122→in, out W3121→SdCoil3112.in. value W3117/ORef3114/RID335는 0616 S5Time `S5T#1M`(V5632), operand W3119/ORef3116=T13. 분 계수의 공유 타이머 근거이며 CL16 고장지연으로 바꾸지 않는다. T17 및 M1.7/M2.0 외부 저장 ACK의 상세는 SYS-RUNHOURS 동일 고정입력 참조. 장기누적 또는 외부 저장 성공은 이번 자료로 확정할 수 없다.

## 4. 전기 전달 끝점

원본 `all-in-one/sources/Electrical_Rev2.pdf` 실제 PDF91/95/131/133을 렌더하여 페이지별 footer를 직접 확인했다. 아래 모든 페이지는 Rev2 17.03.2025, DATA 27.05.2024, 총 FG262 표기다. FG=PDF−1은 해당 확인 페이지에서만 성립하며 일반 규칙으로 강제하지 않는다.

|고유 경로|실제 도면 끝점|미확정|
|---|---|---|
|RUN 접점, FG90/PDF91|+24Vdc10.7 → 5x20 2A F, X1:310 → 선90.4 → 그려진 열린 접점 → X1:311 → E14.0 /130/2|외부 상대 단자·접점기기번호·케이블 번호/규격 미기재|
|RUN 입력, FG130/PDF131|E14.0 역참조90/6 → 입력 단자21, CPU515 MOD11 표기|현재 CPU·장착 모듈·실제 사용·정상극성 미확인|
|FAULT 접점, FG94/PDF95|+24Vdc10.7 → 5x20 2A F, X1:348 → 선94.3 → 열린 접점 → X1:349 → E16.3 /132/4|외부 고장원인·보호기·상대 단자/케이블 미확보|
|FAULT 입력, FG132/PDF133|E16.3 역참조94/4 → 입력 단자4, CPU515 MOD12 표기|외부 제어반 Reset·안전인증·현장 복구 미확인|
|기동 출력 및 전력|CL16 전용 Q writer/출력회로/릴레이/모터 전력 끝점 미확보|다른 CLIENT Q61.x·접점·퓨즈·보호값 복제 금지|

FG90의 전체 입력 묶음, FG94의 Shredder2/BeltD/BeltE 묶음, FG130 E14.0/E14.1 묶음, FG132 E16.0~3 묶음은 SPARE 점선에 포함된다. 따라서 이름과 회로 존재만으로 현장 사용을 확정하지 않는다. 열린 접점 표시는 정상극성 검증이 아니다. 2A는 이 도면에 그린 퓨즈 정격이며 현행 설정/교체 추천이 아니다. 이 입력 회로에는 릴레이 부하5/9나 하단 접점표1/5/9를 임의로 가져오지 않는다. 입력 모듈 보조전원 세부와 외부 전력·케이블표는 이번 4쪽 직접 검토 범위 밖이다.

## 5. 알람·복구

0233 document423 `motor/alarm client`, FC9 NID16의 전체 고유 S/R 핀을 확인했다.

- 공통 허가: rail W345→Contact337.in, ON ORef322/RID1 W328→operand. 337.out W338이 Contact339/341.in으로 분기.
- Set: I16.3 ORef323/RID36 W329→Contact339.operand; out W340→SCoil316.in; operand W331/ORef324/RID37=DB3.DBX16.0. 식은 ON AND I16.3 → 경보 Set.
- Reset: I16.3 ORef325/RID36 W332→Contact341.operand는 Negated. out W342→Contact343.in, RESET_ALLARM ORef326/RID7 W333→operand; out W344→RCoil321.in; operand W335/ORef327/RID37=같은 경보. 식은 ON AND NOT I16.3 AND RESET_ALLARM → 경보 Reset.

이 네트워크에는 타이머 Part가 없다. RUN=0을 고장 원인으로 추가하지 않는다. 원시 고장이 계속 참이면 이 Reset 가지는 성립하지 않는다. 입력 원인 소멸/유지경보 해제/HMI ACK/외부 제어반 자체 Reset/재요청/현장 정상복구는 별도다. Allarmi_129 주소는 내부 경보와 결속하지만 실제 표시 문구·ACK 이벤트·소리·경보 이력은 미확정이다. 공통 DB3 집계/Reset 생성은 SYS-ALARM 공통 근거를 연결하며 CL16 비트가 직접 벨트를 정지시키는 writer는 확보하지 못했다.

## 6. 증상별 읽기 전용 관찰 기준

현장 조작 절차가 아니라 승인된 담당자가 제공하는 자료의 비교 위치다. 출력강제·바이패스·보호값 변경·활선 점검·Reset 실행을 요구하지 않는다.

|증상|동일시각 관찰 자료|비교 기준·경계|
|---|---|---|
|벨트가 안 움직임|현행 프로젝트 식별, 실제 기동 요청/허가/writer, 외부 제어반 상태, I14.0|기동출력 미확보; RUN명칭만으로 모터전원 판단 불가|
|현장 RUN인데 화면 미표시|I14.0/IW14/DB13.W14/X14.0, HMI ID003F8, 표찰 사진|FG90 X1:310/311→FG130 단자21과 0397 Word 미러를 분리|
|FAULT 또는 경보만 지속|I16.3/DB13.X16.3/DB3.X16.0, M0.0, DB2.X6.0|원시입력, 유지래치, ACK를 구분; 원인 단정 금지|
|Reset 요청에도 경보 유지|요청 이벤트·내부 Reset 생성·원시고장 전후·경보비트|0233 NOT FAULT 조건; 외부 보호기 복구는 별도 자료 필요|
|시간값 1 또는 0으로 반복|I14.0,T13,T17,DB9.W60/W62,M1.7,외부 저장로그|0305 Move1/0335 Move0; 누적 HOUR로 오인 금지|
|주소·도면·명칭 다름|백업판본, 현행 단자표, SPARE 실제 사용 승인/개정 근거|e14.7/e19.5와 I14.0/I16.3 상충 보존; 임의 배선변경 금지|

관찰자·실제 시각/시간대·위치·값/단위·장치·프로젝트/도면 판본·사진/로그 출처·비교/배제 결과·승인된 조치 및 복구증거를 별도 기록해야 한다. 실제 운영/SEJIN 기록이나 사진은 복제하지 않았다.

## 7. 완료·누락·검증 경계

|영역|문서 상태|남은 근거|
|---|---|---|
|설비/자료|적용|외부 Belt conveyor E 실물 동일성 및 SPARE 실제 사용|
|I/O/HMI|입력·경보·시간 선언/미러 확인|전용 기동출력, HMI 이벤트/통신/화면|
|제어|고유 알람/시간/다른 writer 및 공통 호출 확인|기동·정지·모드·외부 허가/순서|
|전기|입력 접점→PLC 두 경로 실제4쪽 확인|외부 상대단자·케이블·전력·보조전원 상세|
|알람/복구|고유 Set/Reset·무타이머 구조 확인|외부 보호 원인/설정·현장복구|
|증상관찰|읽기 전용 기준 작성|실제 관찰값/로그 미취득|
|완료/누락|문서 complete_with_gaps|UI·기록·게시·TIA·CPU·현장 완료 아님|

필요 자료는 현행 외부 벨트E 제어반 도면/프로그램, 기동허가/출력 교차참조, X1:310/311/348/349 상대단자 및 케이블표, SPARE 사용 변경근거, 명판·도면개정·정상극성/보호 설정의 승인 자료, HMI 이벤트 및 실제 시간 저장 로그다. 새 자료 없이 같은 실물보류를 반복 조사하지 않는다.

백업 미리보기/선택복원·기록 전후비교·관찰 보고서/PDF 등 사용자 로컬 기능 구현/저장/재읽기/재열기는 이번 조사에서 실행하지 않았다. note/repair_observation의 미지 필드·초안·저장키를 변경하지 않았다. 로컬 통합은 사용자 Codex의 별도 범위다.

검증 구분: 선정 원본33개 SHA256/고정Gitblob byte일치와 IdentXmlPart 181개와 XmlPartIdentMapping 42개를 포함한 `*Ident*.xml` 223개 파일의 명명검색은 33개 또는 223개 전체 의미검토를 뜻하지 않는다. 직접 의미검토는 0233/0305 전체 고유 핀, 0335 첫 Move 가지, 0397 IW14/16 미러, 0549 FC9/FC2 호출 및 0019 T13 가지다. PDF4쪽의 실제 렌더/개정란을 확인했다. 원본 build/test/generator·시뮬레이터 작성/수정/실행/행동시험, PLC/현장/보호값/SEJIN 변경 없음. source Git 상태 공란을 확인했다.

상태: documentation `complete_with_gaps`; static_review `selected_original_xml_and_pdf_reviewed`; ui_records `not_run`; publication `not_published`; tia_compile/live_cpu/field_recovery `not_performed`. 부모 독립검토와 첨부 대기.

검사 및 원형 추출: `../extracts/CLIENT-CL16/verification.json`, `source-hashes.json`, `declaration-search.json`, `live-index-search.json`, 선택 XML·PDF 렌더. 해시/검사 실제 시각: 2026-10-11T12:36:47.143852+00:00.

### 선정 원본 SHA256 + 고정 Git blob 전체 표

경로는 `source-mv06/` 기준. 모든 byte를 `git show abcf31c:경로`와 직접 비교했으며 추출물 재서식은 원본 변경이 아니다.

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
|`EXPANSION-WORK.md`|`ec624de9fd2fcfac861a67fd5e828b25ef46db50bfd7a37ff16e2cb54cd0f7e2`|`4c42d88ecc2d48269eb23e13a20ebf3721a092a1`|일치|
|`all-in-one/ACTIVE-WORK.md`|`eff3bbc08ecff41da3beff77f3fec48e7d148708192bcaaab00f34b6a721afc2`|`6eb947c629b5ddf9c759ef87649451303938864b`|일치|
|`all-in-one/sources/Electrical_Rev2.pdf`|`5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6`|`f610fd7c7ce14ae951b00cff57b969259bfb389d`|일치|
|`all-in-one/sources/hmi_plc_tags.csv`|`a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404`|`cf4c0650e7c7baac350dcb89909b808435704880`|일치|
|`all-in-one/sources/live_index.json`|`14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1`|`e35ccea1f841349c632666c29954b7bcd4f5839e`|일치|
|`all-in-one/sources/decoded-original/network-map.json`|`c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60`|`424430b6b953e43138e5d0a18ca40c949e21cfa1`|일치|
|`all-in-one/sources/decoded-original/0019-FlgNet.xml`|`a3301f4d07c2d36aefa6faa6c3559a1cff4565fc6de40cd17e54b548b30c0ce5`|`f78cfdbf5e717304114660ffbd3bb42cbed6d79d`|일치|
|`all-in-one/sources/decoded-original/0233-FlgNet.xml`|`a5da6ea52e89feb1961f8ee9b582fbf37fc617c841a5ef56b3fa20f14e4d9cf1`|`21475f3cbe8f0540c001f12e5a6f328e59505af3`|일치|
|`all-in-one/sources/decoded-original/0305-FlgNet.xml`|`949ca5dbd42f4084b75f881da1fd530af096a94c11c6f4d9b7e4eed4b3cf3f97`|`c66451d899d0e545f55ed32fd2beeb74777df222`|일치|
|`all-in-one/sources/decoded-original/0335-FlgNet.xml`|`6f0214de436cfaac95750cc25ba3d6f306d33174472618754fac38ad4caf4781`|`6f065e48bd456e656557f1f94896597028f42c5f`|일치|
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
