# LS16 — MV05 닫힘측 위치 리미트 원본 조사 초안

> 고정 원본 정적 조사. documentation=complete_with_gaps. 현재 CPU·실물·정상극성·현장 복구 완료를 뜻하지 않는다.

## 1. 설비·자료 기준

- catalog LS16, 별칭 ls-16/ls.16, component, parent MV05, phase2. INVENTORY.json catalog[227] 및 BATCH22 scope에서 부모·하위 별도 분류를 확인했다. LS15나 ZT05의 별칭 중복이 아니며 부모 완료를 상속하지 않는다.
- 기준 저장소 esp6662266/gme-plc-manual, 고정 commit `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, VERSION 1.12.0, 원본 `all-in-one/`. 후속 게시판과 분리한다. AGENTS·rollout SKILL·WORK-STANDARD·WORK-ITEM-TEMPLATE·INVENTORY 및 최신 인계 상단을 읽었다. 모델/추론 설정은 이 산출물에서 독립 확인하지 못했다.
- P&ID `PID_1684n002I.pdf` 실제 p1의 MV-05/M15 리더에 LS-15/LS-16/ZT-05가 묶인다. M15 0.25 kW 440 V는 부모 구동 표기다. 제목 UBC AND SCRAPS DECOATER 10Ton/h, 도번1684n002, 날짜06/04/2011, 개정 I 15/01/2013을 렌더로 확인했다. 이 관계와 OEM FG35 제목 MOTORlZED VALVE MV-05가 LS16의 문서상 소유 근거다. 현장 장착·캠 방향·센서 모델은 미확인이다.
- 기존 MV05-DOTS-DRAFT와 ZT05-DOTS-DRAFT는 부모 출력/알람 및 엔코더 전체의 공통 색인으로 재사용한다. LS16 고유 입력·접점·소비핀·전기끝점은 직접 확인했다. 이름검색만으로 실물 동일성을 확정하지 않는다.
- 조사자는 자신의 `drafts/LS16-DOTS-DRAFT.md`와 `extracts/LS16/`만 썼다. 원본/코드/PLC/현장/보호값/운영·SEJIN 자료 수정, 생성기·앱빌드·시뮬레이터 작성/수정/생성/실행/행동시험은 수행하지 않았다.

## 2. I/O·HMI — raw, 가공, 요청, 기억을 분리

XML 파일 위치는 모두 `all-in-one/sources/decoded-original/`이다. AO는 비트 오프셋이며 다른 블록의 같은 RID는 섞지 않았다.

| 층 | 원본 선언과 주소 | 해석/미확정 |
|---|---|---|
| 원시 입력 | 0678 SimpleAccess RID447 `MV05_Close`, Input AO58, Bool; NID33 UID22 → I7.2 | OEM E7.2 대응. 이름 Close가 현재 1=완전닫힘을 증명하지 않음 |
| 처리 입력 | 0619 Global RID180 `Inputs.MV05 Close`, AO58, BAD168; 0618 Inputs RID168 TOD13 → DB13.X7.2 | NID6 UID583/604 읽기. 원시 I7.2와 주소공간이 다름 |
| PID 처리 입력 | 0668 Global RID120 AO58 BAD118, NID2 UID136; 0666 Inputs RID118 TOD13 | 같은 DB13.X7.2이나 PID 문맥 선언을 별도 결속 |
| 수동 닫힘 요청 | 0619 RID60 `Flag.M_MV05_CLOSE` AO75 BAD5;0618 Flag TOD2 → DB2.X9.3 | NID6 UID586 RCoil 쓰기. 센서 기억/실물 위치가 아님 |
| 방향 출력 | 0617 RID68 `Close MV05`, Output AO12 → Q1.4 | NID6 UID605 Write. LS16 자체 출력이 아닌 MV05 구동 명령 |
| 엔코더 gate | 0676 RID345 fill_unit1.CONTROL_SIGNALS.SW_GATE3 AO187 BAD177;0674 TOD91 → DB91.X23.3 | 0515 NID33 UID1274 Write/1283 Read. 위치 센서나 종단 기억값이 아님 |
| 엔코더 저장 | 0676 RID201 AO96/RID349 AO336 BAD191;0674 Memory encoder TOD8 → DB8.DBD12/DB8.DBW42 | LS16 원시값과 관련한 0쓰기 경로. LS16의 별도 MEM_CLOSE로 명명하지 않음 |

### raw Word 복사와 별도 쓰기

0397 LAD1070/NID1: Powerrail W21→Move42.en; W52/O45 RID13→Move42.in; Move42.out1 W54/O46 RID14. 0627 RID13 Tag_171는 Input Word AO48=IW6이고, 0629 RID14는 Word AO48 BAD4 Write, 0628 Inputs RID4 TOD13이므로 DB13.DBW6이다. 이 Word는 I6~I7 묶음을 DB13 byte6~7로 복사하는 경로이며 LS16 bit I7.2가 포함된다. 이 Move에 NOT가 없다. 동일 0397의 별도 MV03 반전 분기를 LS16에 복사하지 않는다. 실제 호출/스캔·다른 쓰기까지 동일성을 보장하지 않는다.

중지 simulation 원본의 **정적 쓰기 경계만** 확인: 0403 NID2의 Coil568, operand W621/O590 RID240; 0635 Global RID240 Inputs.MV05 Close AO58 BAD5, NID2 UID590 AK=Write, 0634 Inputs RID5 TOD13. 즉 DB13.X7.2의 다른 writer가 보존 원문에 있다. 이 블록의 실행/생성/수정/행동시험을 하지 않았고, 현재 실행 여부·호출 순서·최종값을 주장하지 않는다. raw I7.2 자체를 덮어쓴다는 뜻도 아니다.

### HMI 설정과 미결속

`all-in-one/sources/hmi_plc_tags.csv` 행758: `MV_05\LimitSwitchClose`, `DB11,X26.4`, Access PLC, ID00044. 행67의 Open은 DB11.X26.3이며 구분한다. 행142 Flag_CLOSE DB2.X9.3과 행436 OutputClose DB11.X26.1은 각각 요청/표시 설정으로 직접 Q1.4와 같다고 하지 않는다.

0365 LAD1188/NID 미확정의 CRef22/RID639, CodeBlock23/RID130: 닫힘 입력 W57/O34 RID698→`Limiti_Switch_Close`; 출력 `Limit_Switch_Close_HMI`→W65/O42 RID177. 이 호출문맥의 RID698/177 직접 선언을 확보하지 못했다. 다른 문맥 RID177 fill_unit1을 끼워 넣지 않는다. CSV와 핀 이름만으로 DB13→DB11 반전/유지/갱신 경로를 확정하지 않으며 실제 화면·이벤트·현재 극성은 미확정이다.

## 3. 제어 — LS16 소비핀과 호출 경계

### 3.1 0346 LAD1708/NID6: 요청 해제 및 닫힘 허가

- 첫 Contact652는 NOT ON(O24/W23), 다음 요청 Reset 앞 Contact654도 NOT ON(O22/W21)이다. 두 ON은 0617 RID1 Memory AO0=M0.0. 원문 반전을 임의 수정하지 않는다. 부모 main ON 호출과 내부 NOT ON의 경계는 MV05 §3.1 공통근거이며 현재 동작 여부는 미확정이다.
- 처리 닫힘 DB13.X7.2: O583/RID180→W614→**NOT Contact662.operand**; outW663→OR538.in1. 다른 입력은 수동Open Contact664(W615/O584)와 Auto Contact666(W616/O585). OR538.out W617→RCoil542; operand W619/O586 RID60=DB2.X9.3. 조건에 따라 수동닫힘 요청을 Reset하는 경로이지 LS16 원시입력의 Reset이 아니다.
- 방향출력 마지막 허가는 **정접점 Contact700**: W647/O604 RID180→operand; 상대 출력 NC Contact698.out W699→700.in; 700.out W701→Coil576.in; W649/O605 RID68→Q1.4. 따라서 이 네트워크의 LS16 소비는 NOT 요청Reset과 정접점 출력허가를 구별한다.
- 앞의 전체 방향 요청은 Auto/PID_DOWN 또는 수동Close/MV WORK PULSE 또는 Oxigen_Fault/NOT UNDER_TESTING의 OR와 고장·반대출력 조건을 포함한다. 부모 MV05 §3.2를 참조하며 LS16만으로 출력을 허가한다고 축약하지 않는다. 회로 NC 및 논리 반전으로 현재 안전정지 성능을 인증하지 않는다.

### 3.2 0475 LAD5/NID2: PID 하한 입력

0668 RID120/UID136의 DB13.X7.2→O136/W157→**NOT Contact198**; out W199→LRef109.`LMNR_LS`. LRef109 RID113는0671 CONT_S, Instance149 RID20는0665 PID_MV05 DB22. ON Contact188.out W189→en. LMNR_LS는 부모 PID 입력이며 LS16 독립 PID나 알람이 아니다. 실제 CONT_S 상태·동작 주기·현재 튜닝/종단극성은 미확정이다.

### 3.3 0515 LAD1765/NID33: raw 입력에 의한 엔코더 연산 gate

EM_OK Contact1321(I19.4,0678RID173)→W1322→**NOT Contact1323**. operand W21/O22 RID447는 처리 DB가 아닌 raw I7.2이다. outW1324→Coil1233.in와Add1238.en, Coil operandW1297/O1274 RID345→DB91.X23.3 SW_GATE3.

같은 EM_OK 가지에서 NOT SW_GATE3 Contact1325(W1309/O1283 RID345)→W1326→Move1255/1260.en. Move1255: Int0 O1284/W1310→out1 W1311/O1285 RID349(DB8.DBW42). Move1260: Int#0 O1286/W1312→out1 W1313/O1287 RID201(DB8.DBD12). 상수0675 RID44/327, 대상0676/0674로 대조했다. 0쓰기는 실제 밸브 영점·종단복구를 증명하지 않는다. 산술·HSC·보존의 전체는 ZT05 §3 공통근거로 재사용한다. 현재 스캔 순서·저장 유효성·유일 writer는 미확정이다.

## 4. 전기 양 끝점·개정·시공 경계

직접 렌더: P&ID p1, OEM p36/p124, 시공 p26/p56의 5쪽. FG와 실제 PDF쪽을 구분한다.

| 자료/쪽 | 직접 확인한 끝점 | 개정/경계 |
|---|---|---|
| Electrical_Rev2 FG35/PDF36 | +24Vdc10.7 분기 접속점→X1/74(5×20 2A F)→35.6→LS16 NC 11–12→X1/75→E7.2, 넘김123/3 | 작성27.05.2024, 개정란 공란. 제목 MV-05. 현재 접점 정상극성·퓨즈실물/설정 미확인 |
| 같은 FG123/PDF124 | E7.2 역참조35/7→CPU515 MOD9 단자33, LIMIT SWITCH LS-16 | **Rev2 17.03.2025**. 부모 MV05 §4.3의 공란 주장과 상충하며 이번 실제 렌더를 우선 기록. 원초안은 수정하지 않음 |
| 같은 FG123/PDF124 모듈공급 | +24V10.7→X21/3009 5×20 2A IST→123.1→단자39; 단자40→0V10.6 | 센서의 X1/74 퓨즈와 별도 모듈 공급. 도면 CPU515 표기는 현재 CPU 확인이 아님 |
| Electrical_Can_Decoating_20241118 p26 | MV05 LS-16, branch2, 표 행6_19 `=FLA+MV05-LS16A`, Flexible16, CVV1.0/2core | 최초안24.11.11; 준공 승인 증거 아님. MV05측 중계함 그림 위 FLO1TB2/아래 FLO1TB1, 표 FLO1TB2 표기를 함께 보존 |
| 같은 p56 행6_19 | MV-05/FLO1TB2→MV-05/LS-16, =FLA+MV05-LS16A, DC CVV2C1.0 spare0, E220, Adjustment3 LEN3 | 설계 길이이며 실측 아님 |
| 같은 p56 행6_12 | MV-03/FLO1TB1→MV-05/FLO1TB2, =FLA+MV05-FLO1TB2A, LS15/16, DC CVV7G1.0 spare2, LEN19 | 공유함 연결이 MV03의 센서 소유를 뜻하지 않음 |

OEM X1/74~75와 시공 중계함 내부 단자/심선의 일대일 연결표는 미확보다. 두 자료를 현재 준공 전구간으로 단정하지 않는다. p56의 검은 가림 행6_7~10은 복원하지 않았다. 주변 ZT05/ZT06A 및 FLO1TB1/2 불일치는 기존 ZT05 문서와 함께 보존하며 LS16 케이블 번호를 바꾸는 근거로 쓰지 않는다. 부모 인버터/정역전력/접촉기·LS15/ZT05 회로 전체를 LS16 소유로 복제하지 않는다.

## 5. 알람·복구 — 부모 고장과 센서 자체를 분리

- 직접 검토한 LS16 소비 네트워크 0346/0475/0515 및 복사0397에서 LS16 전용 명칭 알람·지연타이머·MEM_CLOSE S/R 선언을 확보하지 못했다. 이는 전체 프로그램의 부재 증명이 아니다.
- MV05 공통초안 §5의 T15 S5T#150MS 응답고장, W31/W32 ±700 방향명령 누적, MV_05_FAULT DB3.X11.5는 부모 제어에 해당한다. LS16의 단선 타이머/이중리미트 불일치 진단/독립 알람으로 복제하지 않는다. 이번에는 부모 고장 전체 의미 재검토를 수행하지 않았다.
- LS16 원시회로/처리 DB/요청Reset/엔코더0쓰기/HMI표시/부모고장 Reset/실제 복구는 서로 다른 사건이다. 부모 RESET_ALLARM이 LS16 접점을 복구하거나 현재 안전한 재기동을 보장한다는 근거는 없다.
- NC 도면만으로 단선과 종단 도달을 구분하는 현재 진단 기능을 단정하지 않는다. 현행 프로젝트·알람 이력·위치/캠/준공 결선·적격 담당자 관찰 기록이 필요하다. 강제입력·단락우회·반전 수정·보호값 조정·리셋 조작을 제안하거나 실행하지 않았다.

## 6. 증상별 읽기전용 관찰 문서

| 증상 | 구분하여 대조할 자료/관찰 | 확정 금지 |
|---|---|---|
| 닫힘표시 고정/반대 | LS16 명판·캠·실제 위치, E7.2/I7.2, DB13.X7.2, DB11.X26.4의 동일시각 기록 | NC 또는 Close 이름만으로 정상극성 |
| 닫힘 요청이 사라짐 | 0346 NOT 처리Close/수동Open/Auto→R542, NOT ON 경계 | 원시센서 자체가 Reset되었다는 해석 |
| 닫힘 출력 안 나옴 | 700 처리리미트·반대출력·고장·모드/요청·상위 호출 | LS16 하나만 교체하면 해결 |
| PID와 표시가 다름 | LMNR_LS의 NOT DB13.X7.2와 미결속 HMI 호출 | HMI=raw=PID를 동일 신호로 취급 |
| 위치값 급변/0 | raw I7.2→SW_GATE3, 두 Move0와 엔코더 저장 경로 | 실제 닫힘완료/교정성공 |
| raw/DB 불일치 | 0397 IW6 복사, 0403 별도 쓰기 존재, 현행 호출순서·취득시각 | 중지 블록이 현재 실행된다는 단정 |
| 단자/케이블 식별 불일치 | X1/74~75, LS16A, FLO1TB1/2 양끝 사진·준공표 | 공유함을 이유로 부모 소유 변경 |

기록 필드: 관찰자·시각/시간대·자료/프로젝트 식별·값/자료형/단위·실제 위치 사진·비교 원본·배제 근거·승인된 조치·후속 복구증거. 본 문서는 관찰 틀이며 현장 수행 기록은 없다.

## 7. 완료·누락·다음 자료

| 영역 | 상태 | 남은 경계 |
|---|---|---|
| 설비·자료 | 적용 | 문서 소유 확보, 실물/현재설치 미확인 |
| IO/HMI | 부분 적용 | raw/DB/요청 분리, HMI 선언·이벤트 미결속 |
| 제어 | 부분 적용 | 고유 소비핀/다른 writer, 현재 호출순서 미확인 |
| 전기 | 부분 적용 | 5쪽 렌더/양끝점 확인, 준공 중계함 심선표 미확보 |
| 알람·복구 | 부분 적용 | 부모 소유 분리, 현장 진단/복구 미확정 |
| 증상 관찰 | 문서 적용 | 실제 관찰/조작 미수행 |
| 완료 기준 | complete_with_gaps | UI/게시/TIA/CPU/현장 완료 아님 |

다음에 필요한 것은 LS16 장착·캠/접점 식별 사진, 승인 준공도/중계함 내부 심선표, 현재 CPU 프로젝트·HW매핑/호출 및 writer 정보, HMI DB11.X26.4의 실제 이벤트·표시극성, 승인된 동일시각 입력/위치/알람 기록이다. 없는 자료를 이름/부모완료로 채우지 않는다.

도면·래더 나란히 보기, 백업·선택복원, 전후 기록 비교, 보고서/PDF UI 구현·검사는 모두 미수행이다. documentation만 complete_with_gaps, static_review는 이번 정적 검사 범위, ui_records=not_run, publication=not_published, tia_compile/live_cpu/field_recovery=not_performed. 원본 보호와 현재 현장 안전성 검증을 혼동하지 않는다.

## 부록 A. 선정 전체 원본 SHA256 / 고정 Git blob 표

선정 39개 전부 표시한다. 해시검사는 의미 전수검토가 아니다. 표의 판본은 고정 commit이며 실제 현재 CPU 일치 증거가 아니다.

| 원본 경로 | SHA256 | Git blob SHA1 | 고정 바이트 일치 |
|---|---|---|---|
| `AGENTS.md` | `0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2` | `073164bc6efd5791032d62c71b03b4dab48cb6f8` | True |
| `.agents/skills/gme-equipment-rollout/SKILL.md` | `fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b` | `9aa820ea6ca15b4e136c9772423b78ed4df6a3d4` | True |
| `.agents/skills/gme-equipment-rollout/references/source-map.md` | `40612c5efb8f94608840c7bc0e9095ea840df54920861c388ae48ea34c7998dc` | `49e50a7a8e56a16e2ec7f3607a03fd90adb8f1d3` | True |
| `docs/equipment-standard/WORK-STANDARD.md` | `05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99` | `f76a570cc73098632e08759b17934000f7e3a253` | True |
| `docs/equipment-standard/WORK-ITEM-TEMPLATE.md` | `4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586` | `e546f39535d2b589e80f97db869ac37ce4d05cfd` | True |
| `docs/equipment-standard/INVENTORY.json` | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` | `587c3748ad9224718f95ba06463fee913dae231d` | True |
| `docs/equipment-standard/START-GPT61.md` | `35769e3146ccd707fea2b81b67b30376b76a0a19c7e662fe2bb4fdd382306f94` | `0d08cab3678df7e2625251b641b138ef4956483b` | True |
| `VERSION.json` | `5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7` | `fffb51663b7705aec91cb119ca80ee943a4ce758` | True |
| `WORKSPACE-HANDOFF.md` | `215096d997782e78e901dfae36c782937e49611fbeb677a0d3fa50cbecf8d074` | `dd0b8989d2376c4415bba9bd826fe6754c6b1a12` | True |
| `PUBLICATION_STATUS.md` | `efe4857aec598d90470322cf3962eb3fe1f64947630e1fdf71d1c90134de8740` | `d76401cf291fc0be681acc51fa898ad3ce46ff78` | True |
| `all-in-one/ACTIVE-WORK.md` | `eff3bbc08ecff41da3beff77f3fec48e7d148708192bcaaab00f34b6a721afc2` | `6eb947c629b5ddf9c759ef87649451303938864b` | True |
| `EXPANSION-WORK.md` | `ec624de9fd2fcfac861a67fd5e828b25ef46db50bfd7a37ff16e2cb54cd0f7e2` | `4c42d88ecc2d48269eb23e13a20ebf3721a092a1` | True |
| `all-in-one/sources/PID_1684n002I.pdf` | `2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b` | `8c83a59fefd5b8b651ec3537ea4236a073f5e109` | True |
| `all-in-one/sources/Electrical_Rev2.pdf` | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` | `f610fd7c7ce14ae951b00cff57b969259bfb389d` | True |
| `all-in-one/sources/Electrical_Can_Decoating_20241118.pdf` | `3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd` | `0ee6b6f8361c5790864dbba4bbd9d55e8e7c08f8` | True |
| `all-in-one/sources/hmi_plc_tags.csv` | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` | `cf4c0650e7c7baac350dcb89909b808435704880` | True |
| `all-in-one/sources/decoded-original/network-map.json` | `c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60` | `424430b6b953e43138e5d0a18ca40c949e21cfa1` | True |
| `all-in-one/sources/decoded-original/0346-FlgNet.xml` | `7c782d799751476d88794a5d3d993e91878e03a39147d3b13233193dd3f6ce09` | `da4eb2f53c127242aeeca371ae3ee4d29228d4f1` | True |
| `all-in-one/sources/decoded-original/0365-FlgNet.xml` | `99285443609a94429b3310720f3ebdcea63f3273ab0fc8ac9d4ae2bd1dd0377a` | `e6a379db52a421bd602b2cbfc8b99af6b7262704` | True |
| `all-in-one/sources/decoded-original/0397-FlgNet.xml` | `bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834` | `4ab8370493c4e28fc1eabeeebe2743d27f0c4021` | True |
| `all-in-one/sources/decoded-original/0403-FlgNet.xml` | `77b03e38aa857ac8dd404f2f66a56256939b4e7924b41334a7981b86089c1e6b` | `4c806e31eb65f00cbb7870c72896ac26a8bc3dd3` | True |
| `all-in-one/sources/decoded-original/0475-FlgNet.xml` | `ca3a5bf5bce9189b7c63dd27057b6b759e74a7793d34d2d050fe7e69951ae2b3` | `5d03d472dc65fb5dc6b0442caae0167b938bf57f` | True |
| `all-in-one/sources/decoded-original/0515-FlgNet.xml` | `504f68cf91ee6b33d6b29ab8549a013fed0d11b46212ad58f0aa377f33816ccf` | `d876759299a419e63c0b58d423e2c215ca40a146` | True |
| `all-in-one/sources/decoded-original/0617-IdentXmlPart.xml` | `10bcf85169cb2512f55acadaef299a3d46b4b4cecd88032d739cfeba23e94aa9` | `9527658ee6808be34bd513b1b2ebaf3a4a5a6f3e` | True |
| `all-in-one/sources/decoded-original/0618-IdentXmlPart.xml` | `0c6762de9cdf0e294317f7463bea3d8e6df5673d333d9b1826ebd17a7ded044c` | `9eec0dbd8abde4aa7295f77b63ad473f895f274b` | True |
| `all-in-one/sources/decoded-original/0619-IdentXmlPart.xml` | `85694bb5b696e31e6a1217431112e5b750516c4f94078d6e127d4394a8b80456` | `11f0502c84a1f319a21459a35c0dc1c6ce8e8f36` | True |
| `all-in-one/sources/decoded-original/0627-IdentXmlPart.xml` | `08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb` | `61ebc0abbb2ca160e11e1da400a3f14a397d8bc5` | True |
| `all-in-one/sources/decoded-original/0628-IdentXmlPart.xml` | `9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd` | `170ca5c72599edc7ea7eefe651c3680ce325e76a` | True |
| `all-in-one/sources/decoded-original/0629-IdentXmlPart.xml` | `67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972` | `058129bb01e27f7a6a0d0293f332d745e5bab74e` | True |
| `all-in-one/sources/decoded-original/0634-IdentXmlPart.xml` | `af3fcb536a6270ffb9a19e5b3f2c284a38d67d465f5147961005c1c01d11299d` | `877d9e0734dc7f3e5a8cea789eeb58a208501f48` | True |
| `all-in-one/sources/decoded-original/0635-IdentXmlPart.xml` | `1a057d686446a3fdab7ac61bb09bc543c52f49646c9ca71ac323c10fcdffe457` | `95bfcad59cfb0c12b573e9e8face4262d1e94622` | True |
| `all-in-one/sources/decoded-original/0665-IdentXmlPart.xml` | `50e88d5f50f555151b35cfb17225e766c34ef6b490bd3a48e0a4e335fd17e3dd` | `ea4a8a5013081f648722c5ebbde3bb1366787990` | True |
| `all-in-one/sources/decoded-original/0666-IdentXmlPart.xml` | `19a9ccb83ad7070d23726250870d0ca0c33d797ab9ffe679c9d2c0d109cc95e6` | `b6130b32498b6fee0d9e4db7a04dc79f785e1fbb` | True |
| `all-in-one/sources/decoded-original/0668-IdentXmlPart.xml` | `2248e994a0a02cd37c5c5edaca199b3421068feea91e2e8616560e814ef9f6ed` | `fe0f30d1eaae37783b0f03cb090353b3a3de3600` | True |
| `all-in-one/sources/decoded-original/0671-IdentXmlPart.xml` | `26cb51706305c372d512c19770648bb0dbb74df8bd2277b1e0da1b8c88cca293` | `e38a4e2c93ac8093e2b0b8e082a64688b5d9845e` | True |
| `all-in-one/sources/decoded-original/0674-IdentXmlPart.xml` | `4770702f519bacda69202bb2f7733d983074bda90964360c238f990d9d08fd84` | `f210593944547b63eab10c667348711413600aab` | True |
| `all-in-one/sources/decoded-original/0675-IdentXmlPart.xml` | `b1902886927d8403fab736d9c8ffe73f2fbc8ce4b7ca7c345144964668b051c3` | `d82a33b173c8dc0737fd890eb2a63a88a07d0831` | True |
| `all-in-one/sources/decoded-original/0676-IdentXmlPart.xml` | `c58427c5b0ac6c11cdb52e4c6d0461c7b191fae81ccace191048e9f175fcec59` | `1ed67265f69796a4e659f9438e551068037f33a4` | True |
| `all-in-one/sources/decoded-original/0678-IdentXmlPart.xml` | `51e637e0b9713c028810f2a717b5c3804a3a26c2f1be7e332a4d6bf277bfc382` | `7fafb2297bcdf739bf1d1dd68cebc0d74f2a40cc` | True |

## 부록 B. 실제 검사와 경계

- 최종 검사 2026-10-11T13:41:24.891409+00:00. 선정 39개, 전체 sources 712개, 중지 자산5개 고정 blob 바이트 일치. Git status clean.
- 의미검토는 고유 네트워크3개 소비/쓰기 가지, 공통복사1개, HMI 호출1개 닫힘핀, 중지 원문1개 쓰기끝점에 한정한다. 전체 695 XML 선언 이름검색은 탐색이지 전수 의미검토가 아니다. PDF 실제5쪽을 렌더·시각검토했다.
- 원본검사 수와 의미검토 수를 합산하지 않는다. 원본 생성기/스킬 preflight/앱빌드/시뮬레이터/PLC/현장/UI/게시 검사는 실행하지 않았다. 이 작업은 자체 XML/PDF 정적 분석과 자체 해시검사만 수행했다.
- 직접 관찰한 정정: FG123/PDF124 Rev2 17.03.2025. HMI 호출 NID·RID698/177 결속은 미확정으로 보존.
- 검사JSON: extracts/LS16/source-hashes.json, source-preservation-hashes.json, stopped-assets-preservation.json, static-review.json. 원본과 다른 조사자의 산출물은 변경하지 않았다.
