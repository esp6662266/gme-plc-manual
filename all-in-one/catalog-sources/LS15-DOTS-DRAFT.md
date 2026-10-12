# LS15 — MV05 개방측 리미트 스위치 원본 조사 초안

## 1. 설비·자료 기준

- catalog LS15, component, parent MV05, phase2. INVENTORY.json catalog[226] 및 TASK3-BATCH22-SCOPE.json, GME-CATALOG-OVERLAP-REVIEW.json에서 parent_child_separate와 physical_identity_verified=false를 확인했다. 부모 MV05 완료를 상속하지 않는다.
- 고정 읽기 전용 원본 source-mv06, commit abcf31c5030bc7ef8749ed8e869a857f2387a28a, VERSION v1.12.0. 현재 배포/CPU와 구별한다. AGENTS, rollout SKILL, WORK-STANDARD, WORK-ITEM-TEMPLATE, 시작/인계 최신 항목을 읽었다. 실제 모델 UI 선택 결과는 관측하지 못했다.
- P&ID `all-in-one/sources/PID_1684n002I.pdf` 실제 p1: MV-05 밸브 리더는 M15 구동기 묶음으로 연결되고 LS-15, LS-16, ZT-05 및 0.25 kW 440V가 함께 표시된다. LS15와 MV05의 문서상 관계이지 현재 실물 일치 완료가 아니다. 도면1684n002, Apex I, 기본일06/04/2011, 최종표시 I 15/01/2013. 개방 방향은 P&ID의 묶음만으로 정하지 않고 OEM FG35의 LIMIT SWITCH VALVE OPEN으로 확인했다.
- MV05·ZT05 초안은 공통 제어/엔코더 색인으로 재사용했다. 부모 전력·산소 PID 전체·엔코더 전체는 이번 전수 의미검토가 아니다. PV01/PV02 및 EV69KA/71KA 실부하 5–9 정정을 유지하며 LS15로 부모 EV 출력/타이머를 복제하지 않는다.
- 자신의 draft/extracts만 작성했다. 원본·코드·PLC·현장·보호값·SEJIN·배포 변경, 시뮬레이터 작성/수정/생성/실행/행동시험, 원본 생성기/앱 빌드, 업로드 없음.

## 2. I/O·HMI — 원시/처리/요청/표시 구분

|층|원본 위치·선언|해석·미확정|
|---|---|---|
|물리 입력|Electrical_Rev2.pdf FG35/p36, FG123/p124 E7.1, LS15, MOD9 단자32|PLC 입력 주소 I7.1에 대응하는 문서 경로. 이번 Ident XML 전역 검색에서 Input AO57 단독 Bool 이름 선언은 찾지 못했다. 부모의 `MV05_open`이라는 raw 이름을 독립 선언 검증으로 승격하지 않음|
|입력 Word|0627 SimpleAccess RID13 Tag_171, Input AO48 Word, NID1 UID45|IW6. I6.0~I7.7을 포함하는 원시 Word|
|처리 Word|0629 Global RID14, AO48 Word, BAD4, NID1 UID46 AK Write;0628 DepDBBlock RID4 Inputs TOD13|DB13.DBW6. raw와 별도 메모리이며 다른 쓰기 가능|
|처리 개방비트|0619 Global RID179 Inputs.MV05 open, AO57 Bool, BAD168;0618 Inputs RID168 TOD13;NID6 UID579/595|DB13.DBX7.1, 리미트 처리값. 이름 open만으로 TRUE=기계 개방완료라고 단정하지 않음|
|PID 입력|0668 Global RID119 Inputs.MV05 open AO57, BAD118;0666 RID118 TOD13;NID2 UID135|같은 DB13.X7.1을 0475에서 반전하여 LMNR_HS에 전달|
|수동 요청 기억|0619 RID62 Flag.M_MV05_OPEN AO76 Bool, BAD5;0618 Flag TOD2|DB2.X9.4. 물리 LS나 위치 기억값이 아니라 수동 요청. 본 고유 경로에 LS15 전용 MEM_OPEN 위치 래치 근거 미확보|
|구동 출력|0617 SimpleAccess RID69 Open MV05, Output AO11, NID6 UID596 Write|Q1.3. 부모 구동 출력이며 LS15 자체 출력 아님|
|HMI 설정|hmi_plc_tags.csv 행67 MV_05\LimitSwitchOpen, DB11,X26.3, PLC, ID0040F|현재값·이벤트·표시극성 미확정. DB13.X7.1 또는 Q1.3과 합치지 않음|

모든 FlgNet/Ident의 저장소 경로 접두사는 `all-in-one/sources/decoded-original/`이다. RID는 동일 블록/NID/UID 문맥에서만 결속했다.

### HMI 호출과 공통 FC 경계

0365 LAD1188, hmi index_order11: Powerrail W21→CRef22.en; CRef22 RID639, CodeBlock23 RID130. 0623 FCBlock RID130 TOD10=HMI Standard Motorized Valve, 0624 BlockInterfaceInfo RID639에 NID11 UID22/23와 인터페이스 Bool 형식을 확인했다. LS 관련 입력은 W56/O33 RID699→Limit_switch_Open, 출력은 W64/O41 RID176←Limit_Switch_Open_HMI. **이 두 실제 인수의 선언 결속은 확보하지 못했다.** network-map의 Inputs.MV05 open/Motors.mv05.limit_switch_open 문자열은 탐색 후보이고 CSV 주소를 핀에 끼워 넣지 않는다.

공통 FC 본문 0356 LAD336/NID1은 Local `Limit_switch_Open` RID33/UID99(0622, S=I PN7 Bool)→W102→정접점97→W103→일반 Coil98→W104/O100→Local `Limit_Switch_Open_HMI` RID35/UID100(0622,S=O PN11 Bool,Write)이다. 여기에는 NOT/래치/지연이 없다. 공통 FC의 전달 구조를 확인한 것이며, 0365의 미결속 실제주소가 해소되거나 현재 HMI 화면이 검증된 것은 아니다. LS15 전용 버튼·HMI 이벤트 근거 미확보.

## 3. 제어 구조 — LS15 고유 쓰기·읽기

### 3.1 원시 Word 전달

0397 LAD1070/NID1: Powerrail W21→Move42.en; W52/O45 RID13→Move42.in(IW6); Move42.out1→W54/O46 RID14→DB13.DBW6. Move42.eno는 W53으로 Move43.en에 연결된다. DisableENO=true 속성과 실제 XML 배선을 모두 보존한다. 이 Move 자체에 입력 반전은 없다. Word의 해당 비트 전달과 스캔말 최종값/현재 호출은 구분한다.

### 3.2 요청 Reset과 열림 출력 허가

0346 LAD1708/NID6 고유 대조:
- Contact652와654는 모두 NOT ON, W23/O24 및 W21/O22. 0617 RID1 Memory AO0=M0.0. 부모의 main ON 호출과 내부 NOT ON 상충을 보존하며 운전 가능/불가능으로 단정하거나 수정하지 않는다.
- NOT Inputs.MV05 open Contact656: W608/O579 RID179 operand, out W657→OR531.in1. 같은 OR에는 CLOSE 요청 Contact658와 Auto Contact660가 들어간다. OR531.out W611→RCoil535; W613/O582 RID62→DB2.X9.4 수동 OPEN 요청 Reset. LS15 위치 자체를 Reset하는 명령이 아니다.
- 열림 방향의 마지막 허가: 반대출력 NOT Close Contact682.out W683→**정접점684**(operand W633/O595 RID179)→W685→일반 Coil561, operand W635/O596 RID69→Q1.3.
- 따라서 처리비트가 열림 요청 Reset에서는 반전, 열림 출력 허가에서는 정접점으로 쓰인다. 도면 NC와 일관될 수 있지만 현재 캠 작동·단선·정상극성·안전성은 이를 통해 확정할 수 없다. 앞단 Auto/PID 또는 수동펄스, 산소고장/시험, 부모고장/반대출력 조건은 MV05 초안 §3.2 공통 경계를 유지한다.

### 3.3 PID 종단 입력

0475 LAD5/NID2: O135 RID119→W156→NOT Contact196; Powerrail W200이 Contact196.in 공급, Contact196.out W197→LRef109.LMNR_HS. LRef109 RID113는 0671 CONT_S, Instance149 RID20는 0665 PID_MV05 DB22. 공통 호출 en은 ON188→W189다. 처리 DB13.X7.1을 반전해 상단 리미트 핀에 전달하며 raw I7.1 직접 입력이 아니다. LS16의 LMNR_LS 및 ZT05 raw I7.2 기반 게이트/0쓰기를 LS15 기능으로 복제하지 않는다. PID 전체 튜닝값·실제 실행주기는 이번 고유 검토 범위 아님.

### 3.4 보존된 중지 블록의 추가 쓰기 존재

정적 원문 쓰기 검토만 수행: 0403 LAD1083, simulation, NID2에서 Lt565 Int in1 W24/O31 RID324(Data.Pot_MV05,0635 AO1120,BAD247;0634 Data TOD1=DB1.DBW140), in2 W30/O32 RID253(0637 Int98), pre W21 Powerrail. out W23→**일반 Coil566**; W617/O587 RID241(0635 Inputs.MV05 open AO57, BAD5;0634 Inputs TOD13), NID2 UID587 AK Write →DB13.X7.1.

즉 이 보존 원문에는 Pot_MV05<98 비교 결과를 처리비트에 쓰는 별도 경로가 있다. 숫자98을 현장 개방한계/보호값/권장 설정으로 사용하지 않는다. 블록이 현재 호출된다는 주장은 하지 않으며, 중지 정책하에서 생성·수정·실행·행동시험은 일절 하지 않았다. 이것이 0397 Word Move를 유일 writer 또는 raw=처리 최종값으로 주장하지 않는 이유다.

## 4. 전기 양 끝점·실제 PDF·페이지별 개정

### OEM 고유 경로 직접 렌더

|구간|양 끝점·도면상 접속|페이지·개정|
|---|---|---|
|공급|+24Vdc10.7 수평선 34/9→36/3, 접속점→X1/72, 5×20 2A F→35.5|Electrical_Rev2.pdf FG35/실제p36, DATA27.05.2024, 개정란 공란|
|센서|35.5→LS15 NC11–12→X1/73→E7.1, 하향 123/2|같은 FG35; 제목 MOTORIZED VALVE MV-05, 개방측 LIMIT SWITCH VALVE OPEN|
|PLC 입력|상향35/5→E7.1→MOD9 단자32, LS-15, CPU515 표시|FG123/실제p124, **Rev2 17.03.2025**, 기본 DATA27.05.2024|
|모듈 공통전원|+24V10.7→X21/3009 5×20 2A IST→123.1→단자39; −0V10.6→단자40|FG123; LS15 자체2A F 분기와 모듈2A IST 공급은 별도|

부모 MV05 초안 §4.3의 “FG123 개정란 공란”은 직접 렌더와 불일치한다. 이 초안은 Rev2 17.03.2025를 채택하고 별도 `extracts/LS15/MV05-FG123-REVISION-SUPPLEMENT.md`로 좁힌 정정을 인계한다. 부모 원초안은 수정하지 않았다. 도면 개정 정정은 제어논리/현장상태 변경이 아니다.

LS16은 X1/74~75,35.6,E7.2,MOD9/33의 별도 폐쇄측 경로이고 ZT05 X1/67~71은 별도 엔코더다. LS15의 공급/접점을 엔코더 A/B 또는 접촉기 피드백과 동일화하지 않는다. 현재 LS 모델·장착·접점 상태·케이블 연속성·퓨즈 실제품/정상극성은 미확인.

### 시공 자료의 중계 경로

Electrical_Can_Decoating_20241118.pdf 직접 p26(CANDC-CONS-E009-026, FLOW A ROUTE CONDUIT PIPING(1)) 및 p56(CANDC-CONS-C006-056, CABLE SCHEDULE(5)): 둘 다 Rev1 24.11.11 first draft design. 준공/승인 상태는 미확보.

- p56 행6_1 `=FLA+MV03-FLO1TB1A`: CR→MV03/FLO1TB1, 설명 LS15/16/19/20, DC CVV12G1.0, spare3, LEN44. 공유 feeder이며 MV03 소유 리미트로 재분류하지 않음.
- p56 행6_12 `=FLA+MV05-FLO1TB2A`: MV03/FLO1TB1→MV05/FLO1TB2, 설명 LS15/16, DC CVV7G1.0, spare2, Adjustment18, LEN19.
- p56 행6_18 `=FLA+MV05-LS15A`: MV05/FLO1TB2→MV05/LS-15, DC CVV2C1.0, spare0, route E210, Adjustment3, LEN3. p26 장치 LS15 행6_18의 케이블 표기와 대응.
- p26 위쪽 장치 묶음에는 LS15/16/ZT05와 중계함 주변 FLO1TB2 및 FLO1TB1 표기가 함께 보인다. 표의 MV05 FLO1TB2와 그림의 명칭 위치를 구별하고 내부 단자표 없이 임의로 수정·합치지 않는다.
- 같은 p26/p56의 ZT06A/ZT05A 및 incoming ZT06 상충은 ZT05 초안 공통 미확정으로 보존한다. LS15 케이블을 엔코더 케이블과 합치지 않음. 검은 가림 행은 텍스트로 복원하지 않음.

OEM X1/72~73과 시공 중계함 내 개별 단자번호/심선색 양끝 결속표는 미확보다. 따라서 위 문서들을 현재 검증된 하나의 준공회로로 완성하지 않는다. 길이/규격/2A는 원문 설계 표기이며 실측 또는 현행 보호설정이 아니다.

## 5. 알람·복구 — 부모 고장과 센서 분리

확인한 LS15 원시전달/요청Reset/PID종단/공통HMI 가지에는 LS15 전용 타이머나 알람 S/R 래치가 없다. 전체 프로그램의 부재 증명은 아니다. 부모 MV05 초안의 0159 T15 S5T#150MS 접촉기 응답 고장,0351/0352 ±700 방향출력 누적, DB3.X11.5 MV_05_FAULT는 부모 범위 공통근거로 남긴다. 이를 LS15 단선 고장/종단 도달시간/센서 리셋으로 가져오지 않는다. ZT05 OFR DB3.X25.1 역시 LS15 고장으로 재분류하지 않는다.

0346 R535는 수동 요청 해제이며 리미트 접점이나 HMI 알람의 복구가 아니다. HMI 표시 변화, 처리비트 변경, 실제 접점/기구 정상, 부모고장 해제, 재요청 가능, 현장복구 확인을 분리한다. 현장 강제입력·우회·점퍼·교정·보호설정 변경을 수행하거나 권고하지 않았다.

## 6. 증상별 관찰 — 읽기 전용 기록안

|증상|관찰·비교 위치|배제할 성급한 결론|
|---|---|---|
|개방 위치인데 표시가 반대|기구/캠 사진·시각, FG35 NC11–12, raw I7.1, DB13.X7.1, DB11.X26.3와 실제 HMI 이벤트|태그 open=TRUE가 반드시 기계 개방완료|
|입력과 처리값 불일치|IW6→0397 Move42→DB13.DBW6,0403 별도 writer 존재·현재 호출/승인 프로젝트|센서 불량 또는 Word 복사 오류 단정|
|열림 명령이 풀림|0346 NOT 처리비트656, CLOSE 요청658, Auto660→R535; 실제 모드/시각|LS 자체 Reset 실행·자동복구 완료|
|열림 출력이 억제됨|정접점684, 반대출력682, 앞단부모허가/고장/NOT ON 경계|리미트 하나가 유일 원인|
|PID 상단제한 표시|0475 NOT DB13.X7.1→LMNR_HS, HMI 실제 표시 결속|엔코더 영점·기계 완전개방 보증|
|복수 LS 동시 이상|공유feeder6_1/6_12와LS15 branch6_18, 모듈전원39/40·개별 X1/72|공유인버터/엔코더와 같은 센서회로|

기록 필드: 관찰자·시각/시간대·설비/캠·배선 양끝 사진·현재 프로젝트/자료시점·raw/처리/HMI 값과 형식·비교원본·배제결과·승인조치·복구 후 증거. 이번에는 실제 운영 관찰자료를 수집/변경하지 않았다.

## 7. 완료·누락·인계

|영역|상태|미확정 경계|
|---|---|---|
|설비·자료|적용|문서상 parent/leader 확인, 실물동일성 미확정|
|I/O·HMI|부분 적용|IW6/DB13·CSV·공통FC, 호출 실제인수/화면 이벤트 결속 미확보|
|제어|부분 적용|고유핀·반전·별도쓰기 존재, 현재 호출/최종값/정상극성 미확정|
|전기|부분 적용|OEM2쪽+시공2쪽+P&ID1쪽 실제 렌더, 중계함 내부단자표 미확보|
|알람·복구|부분 적용|부모와 소유 분리, 독립센서고장/현장복구 근거 미확보|
|증상관찰|문서 적용|관찰표만 작성, 현장 조작/행동시험 없음|
|완료기준|초안 complete_with_gaps|BC01 동등 UI/게시/현장 완료 아님|

필요 자료: (1) LS15 명판·MV05 장착/캠·실제 끝위치 사진, (2) 승인 준공 X1/72~73↔FLO1TB1/2↔LS15 11/12 단자·심선표, (3) 현재 PLC 프로젝트/DI 주소·전체 writer/호출순서와 시간 동기화 관찰값, (4) 0365 실제 인수의 원형 선언 및 HMI DB11.X26.3 이벤트/표시극성, (5) 적격 담당자의 실제 기구/접점·복구 기록. 새 근거 없이는 미확정을 유지한다.

도면·래더 비교 근거는 제공했지만 앱의 나란히 보기·백업/선택복원·기록 전후비교·보고서/PDF 기능 구현/시험은 미수행. documentation=complete_with_gaps; static_review=고유 XML/PDF 정적대조; ui_records/publication/tia_compile/live_cpu/field_recovery=미수행. 현장 및 독립 검토 완료를 주장하지 않는다.

## 부록 A. 선정 원본 SHA256 / 고정 Git blob 전체표

고정 커밋 바이트 일치는 의미 전수검토·현장/현재 CPU 일치와 다르다. 6개 네트워크의 LS15 관련 가지(0397/0346/0475/0365/0356/0403)와 관련 선언, PDF5쪽을 의미검토했다. 0403은 중지 원문 추가쓰기 정적 확인만 했다. 부모의 main/알람/엔코더 전체는 재사용 공통근거이며 이번 의미 전수검토가 아니다.

|원본 경로|SHA256|고정 Git blob SHA1|바이트 일치|
|---|---|---|---|
|`AGENTS.md`|`0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2`|`073164bc6efd5791032d62c71b03b4dab48cb6f8`|Yes|
|`.agents/skills/gme-equipment-rollout/SKILL.md`|`fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b`|`9aa820ea6ca15b4e136c9772423b78ed4df6a3d4`|Yes|
|`.agents/skills/gme-equipment-rollout/references/source-map.md`|`40612c5efb8f94608840c7bc0e9095ea840df54920861c388ae48ea34c7998dc`|`49e50a7a8e56a16e2ec7f3607a03fd90adb8f1d3`|Yes|
|`docs/equipment-standard/WORK-STANDARD.md`|`05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99`|`f76a570cc73098632e08759b17934000f7e3a253`|Yes|
|`docs/equipment-standard/WORK-ITEM-TEMPLATE.md`|`4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586`|`e546f39535d2b589e80f97db869ac37ce4d05cfd`|Yes|
|`docs/equipment-standard/START-GPT61.md`|`35769e3146ccd707fea2b81b67b30376b76a0a19c7e662fe2bb4fdd382306f94`|`0d08cab3678df7e2625251b641b138ef4956483b`|Yes|
|`docs/equipment-standard/INVENTORY.json`|`720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc`|`587c3748ad9224718f95ba06463fee913dae231d`|Yes|
|`VERSION.json`|`5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7`|`fffb51663b7705aec91cb119ca80ee943a4ce758`|Yes|
|`EXPANSION-WORK.md`|`ec624de9fd2fcfac861a67fd5e828b25ef46db50bfd7a37ff16e2cb54cd0f7e2`|`4c42d88ecc2d48269eb23e13a20ebf3721a092a1`|Yes|
|`WORKSPACE-HANDOFF.md`|`215096d997782e78e901dfae36c782937e49611fbeb677a0d3fa50cbecf8d074`|`dd0b8989d2376c4415bba9bd826fe6754c6b1a12`|Yes|
|`PUBLICATION_STATUS.md`|`efe4857aec598d90470322cf3962eb3fe1f64947630e1fdf71d1c90134de8740`|`d76401cf291fc0be681acc51fa898ad3ce46ff78`|Yes|
|`all-in-one/ACTIVE-WORK.md`|`eff3bbc08ecff41da3beff77f3fec48e7d148708192bcaaab00f34b6a721afc2`|`6eb947c629b5ddf9c759ef87649451303938864b`|Yes|
|`all-in-one/sources/PID_1684n002I.pdf`|`2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b`|`8c83a59fefd5b8b651ec3537ea4236a073f5e109`|Yes|
|`all-in-one/sources/Electrical_Rev2.pdf`|`5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6`|`f610fd7c7ce14ae951b00cff57b969259bfb389d`|Yes|
|`all-in-one/sources/Electrical_Can_Decoating_20241118.pdf`|`3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd`|`0ee6b6f8361c5790864dbba4bbd9d55e8e7c08f8`|Yes|
|`all-in-one/sources/hmi_plc_tags.csv`|`a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404`|`cf4c0650e7c7baac350dcb89909b808435704880`|Yes|
|`all-in-one/sources/decoded-original/network-map.json`|`c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60`|`424430b6b953e43138e5d0a18ca40c949e21cfa1`|Yes|
|`all-in-one/sources/decoded-original/0397-FlgNet.xml`|`bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834`|`4ab8370493c4e28fc1eabeeebe2743d27f0c4021`|Yes|
|`all-in-one/sources/decoded-original/0346-FlgNet.xml`|`7c782d799751476d88794a5d3d993e91878e03a39147d3b13233193dd3f6ce09`|`da4eb2f53c127242aeeca371ae3ee4d29228d4f1`|Yes|
|`all-in-one/sources/decoded-original/0475-FlgNet.xml`|`ca3a5bf5bce9189b7c63dd27057b6b759e74a7793d34d2d050fe7e69951ae2b3`|`5d03d472dc65fb5dc6b0442caae0167b938bf57f`|Yes|
|`all-in-one/sources/decoded-original/0365-FlgNet.xml`|`99285443609a94429b3310720f3ebdcea63f3273ab0fc8ac9d4ae2bd1dd0377a`|`e6a379db52a421bd602b2cbfc8b99af6b7262704`|Yes|
|`all-in-one/sources/decoded-original/0356-FlgNet.xml`|`5fdf9fada8777584ffcac96cc99cc532625d867754e0d6cdd03690e3fb9bff44`|`0298d246d7c29be946a246d407dddfccece58597`|Yes|
|`all-in-one/sources/decoded-original/0403-FlgNet.xml`|`77b03e38aa857ac8dd404f2f66a56256939b4e7924b41334a7981b86089c1e6b`|`4c806e31eb65f00cbb7870c72896ac26a8bc3dd3`|Yes|
|`all-in-one/sources/decoded-original/0617-IdentXmlPart.xml`|`10bcf85169cb2512f55acadaef299a3d46b4b4cecd88032d739cfeba23e94aa9`|`9527658ee6808be34bd513b1b2ebaf3a4a5a6f3e`|Yes|
|`all-in-one/sources/decoded-original/0618-IdentXmlPart.xml`|`0c6762de9cdf0e294317f7463bea3d8e6df5673d333d9b1826ebd17a7ded044c`|`9eec0dbd8abde4aa7295f77b63ad473f895f274b`|Yes|
|`all-in-one/sources/decoded-original/0619-IdentXmlPart.xml`|`85694bb5b696e31e6a1217431112e5b750516c4f94078d6e127d4394a8b80456`|`11f0502c84a1f319a21459a35c0dc1c6ce8e8f36`|Yes|
|`all-in-one/sources/decoded-original/0622-IdentXmlPart.xml`|`f0b997f1246d76cff71de2160eb617caa936e6987bdf43c73f55cdcf77dccdb6`|`3b1ae1987950d0754aec37282960b314e9913cd3`|Yes|
|`all-in-one/sources/decoded-original/0623-IdentXmlPart.xml`|`4acd00406ea92466169e57e59fc90b0da4d9ec55fd19e2e96c9556e939cb83a6`|`13b3af0459c8e6069bb9b2f1b16454bf479e08dc`|Yes|
|`all-in-one/sources/decoded-original/0624-IdentXmlPart.xml`|`24607c0827fbde428bccf8637ef4ae490798a69a7c2f3b87861d0749082d367a`|`02511fea47fc47981c101bba49dc40adde1cdcc3`|Yes|
|`all-in-one/sources/decoded-original/0627-IdentXmlPart.xml`|`08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb`|`61ebc0abbb2ca160e11e1da400a3f14a397d8bc5`|Yes|
|`all-in-one/sources/decoded-original/0628-IdentXmlPart.xml`|`9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd`|`170ca5c72599edc7ea7eefe651c3680ce325e76a`|Yes|
|`all-in-one/sources/decoded-original/0629-IdentXmlPart.xml`|`67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972`|`058129bb01e27f7a6a0d0293f332d745e5bab74e`|Yes|
|`all-in-one/sources/decoded-original/0634-IdentXmlPart.xml`|`af3fcb536a6270ffb9a19e5b3f2c284a38d67d465f5147961005c1c01d11299d`|`877d9e0734dc7f3e5a8cea789eeb58a208501f48`|Yes|
|`all-in-one/sources/decoded-original/0635-IdentXmlPart.xml`|`1a057d686446a3fdab7ac61bb09bc543c52f49646c9ca71ac323c10fcdffe457`|`95bfcad59cfb0c12b573e9e8face4262d1e94622`|Yes|
|`all-in-one/sources/decoded-original/0636-IdentXmlPart.xml`|`ec3d79f03e2748f8def4409ad676a97b98e28b9d8e68f6a64b3fe894466832ca`|`86114327ba1a010b2fcc01dd12b1bf86c01bc02c`|Yes|
|`all-in-one/sources/decoded-original/0637-IdentXmlPart.xml`|`3fb68f57dbe2a877c4ad5aa1b3316810cf84958f2d13b5b1d7d321e0915271c7`|`cb1d7fb76aa2afd96eb46984cc1e71b77f36395c`|Yes|
|`all-in-one/sources/decoded-original/0665-IdentXmlPart.xml`|`50e88d5f50f555151b35cfb17225e766c34ef6b490bd3a48e0a4e335fd17e3dd`|`ea4a8a5013081f648722c5ebbde3bb1366787990`|Yes|
|`all-in-one/sources/decoded-original/0666-IdentXmlPart.xml`|`19a9ccb83ad7070d23726250870d0ca0c33d797ab9ffe679c9d2c0d109cc95e6`|`b6130b32498b6fee0d9e4db7a04dc79f785e1fbb`|Yes|
|`all-in-one/sources/decoded-original/0668-IdentXmlPart.xml`|`2248e994a0a02cd37c5c5edaca199b3421068feea91e2e8616560e814ef9f6ed`|`fe0f30d1eaae37783b0f03cb090353b3a3de3600`|Yes|
|`all-in-one/sources/decoded-original/0671-IdentXmlPart.xml`|`26cb51706305c372d512c19770648bb0dbb74df8bd2277b1e0da1b8c88cca293`|`e38a4e2c93ac8093e2b0b8e082a64688b5d9845e`|Yes|

## 부록 B. 실제 검사 결과

- 검사 시각 2026-10-11T13:42:14.630494+00:00. 선정 원본 40개 SHA256/고정 Git blob 일치. 전체 sources 712파일과 중지자산5개 해시/고정 blob 일치, 원본 저장소 Git status clean. 바이트 검사수와 의미검토수는 다르다.
- 의미검토는 LS15 관련 6네트워크 가지와 선언, P&ID1/OEM2/시공2 실제5쪽. 전체 695 XML 이름/주소 검색은 의미 전수검토가 아니다.
- 검사JSON: extracts/LS15/source-hashes.json, source-preservation-hashes.json, stopped-assets-preservation.json, search.json, static-review.json. 추출 XML은 읽기용 pretty print이며 원본 대체/실행 파일이 아니다.
- 원본·부모/다른 작업자 초안·공통코드·대장·버전·배포·운영·PLC·보호값·SEJIN 변경 없음. 시뮬레이터/원본 생성기/앱 실행검사 미수행.
