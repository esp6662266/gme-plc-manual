# LS25 고유 구성품 조사 초안

- 대상 LS25 밸브 위치 리미트 스위치, 부모 PV02, phase2 / parent_child_separate. 조사일 2026-10-11 UTC.
- 고정 원본 source-mv06: abcf31c5030bc7ef8749ed8e869a857f2387a28a, VERSION v1.12.0, 표준 GME-STD-1.0.0. 실제 모델·추론 설정 관측 미확인.
- PV02 및 CYL-CL05~08 초안은 탐색색인/공통근거로 재사용했다. LS25 고유 위치, 선언·핀, raw/DB/기억의 다른 쓰기, 실제 PDF 끝점·개정을 직접 확인했다. 부모 전체 자동순서·알람 재조사는 하지 않았다.
- 본 MD와 extracts/LS25만 작성. 원본·공통코드·대장·버전·배포·운영·PLC·현장·보호값·SEJIN 변경 없음. 시뮬레이터 작성/수정/생성/실행/행동시험, 원본 생성기·앱빌드 미수행. 아래 simulation XML은 보존 원문의 다른 쓰기 정적 확인만 했다.

## 1. 설비·자료 기준 — 적용

INVENTORY.json catalog[238]는 LS25를 component, parent_id=PV02, depth1, baseline/not_assessed로 둔다. TASK3-BATCH24-SCOPE.json 및 GME-CATALOG-OVERLAP-REVIEW.json의 LS25는 parent_child_separate이고 physical_identity_verified=false다. 같은 이름의 다른 LS와 합치지 않고 부모 완료를 상속하지 않는다.

PID_1684n002I.pdf 실제 PDF1 PV-02 Detail에서 LS-25 리더는 CL-05 로드 측 도식에 닿고 LS-26은 같은 CL-05의 반대 위치에 놓인다. EV-04 뒤 공압선은 CL-05/06에 공유 분기한다. LS25를 CL06의 별도 검출기나 EV04 명령 그 자체로 취급하지 않는다. Gate A OPEN 명칭은 OEM FG72/125와 교차 확인한 문서 관계다. 실제 장착방향·로드 스트로크·센서 작동점·실물 동일성은 미확정이다.

| 원본/실제 PDF | 페이지별 판본·제목 | 경계 |
|---|---|---|
| PID_1684n002I.pdf PDF1 | drawing1684n002, Apex I, 기본06/04/2011, 변경 I15/01/2013, FG ‘−’ | 구형 P&ID 도식, 현행 실물 확인 아님 |
| Electrical_Rev2.pdf PDF73=FG72 | LOAD DRUM CLAPPE VALVE PV-02, DATA27.05.2024, 개정란 공란 | 파일명 Rev2를 페이지 개정으로 옮기지 않음 |
| 같은 PDF126=FG125 | DIGITAL INPUT MODULE, DATA27.05.2024, 개정란 공란 | 도면의 CPU515/MOD10 표기, 현재 CPU 식별 아님 |
| Electrical_Can_Decoating_20241118.pdf PDF24/64 | CANDC-CONS-E007-024, D-PAGE7, ROTARY ROUTE CONDUIT PIPING(1), No.1 24.11.11 first draft design | 승인 준공도 아님 |
| 같은 PDF55/64 | CANDC-CONS-C005-055, D-PAGE5, CABLE SCHEDULE(4), No.1 24.11.11 first draft design | 케이블 일정 초안, 현행 심선표 아님 |

실제5페이지를 자체 렌더해 확인했고 P&ID 상세/제목과 FG125 제목을 확대했다. 렌더·원문 추출은 extracts/LS25에 있다.

## 2. I/O·HMI — 적용, 표시 이벤트 근거 미확보

아래 XML 약기 경로는 all-in-one/sources/decoded-original/이다. RID는 같은 선언 문맥에서만 결속하며 AO는 비트 오프셋이다. 주소는 백업값이며 현재 CPU에 대한 진술이 아니다.

| 층위/신호 | 주소·형식 | 선언과 사용 | 해석/한계 |
|---|---|---|---|
| LS25의 문서상 raw EV04_Open | I9.4 Bool | 0607 RID135, SAD Input, AO76; NID13 UID38 | OEM LS25 Gate A OPEN/E9.4와 연결; 물리 센서 극성은 미확정 |
| Inputs.PV-02 EV A OPEN | DB13.DBX9.4 Bool | 0609 RID136 AO76 BAD86;0608 RID86 Inputs TOD13; NID13 UID39 | raw와 다른 처리 DB 변수, 다른 쓰기 존재 |
| Flag.PV_02_GATE_A_MEM_OPEN | DB2.DBX8.5 Bool | 0609 RID55 AO69 BAD5;0608 RID5 Flag TOD2; NID13 UID40 Set/42 Reset | 위치 기억; 순간 센서값 아님 |
| 부모 Q_A PV-02 GATE A EV | Q5.4 Bool | 0607 RID85 SAD Output AO44; NID13 UID37/41/43/47 | 기억 설정/해제 방향 조건. LS25가 소유한 출력 아님 |
| ON | M0.0 Bool | 0607 RID1 Memory AO0, NID13 UID36 | 이름 ON을 상수 true로 해석하지 않음 |
| 비교용 LS26 EV04_Close | I9.5 Bool | 0607 RID137 AO77, NID13 UID44 | 별도 LS26; LS25의 반전 비트라고 정의하지 않음 |
| 비교용 A MEM_CLOSE | DB2.DBX8.4 Bool | 0609 RID139 AO68 BAD5; NID13 UID46/48 | 별도 닫힘 기억, startup Set 포함 |

hmi_plc_tags.csv 원문 PV_02\GateA_Open은 DB11,X78.1, ID000A6, GateA_Close는 DB11,X78.2, ID000A5이다. 이것은 HMI 설정 주소이며 I9.4/DB13/DB2와 별도다. LS25 전용 HMI 객체·화면 이벤트·쓰기 방향 근거는 확보하지 못했다. 부모 초안의 0392 HMI PV_2Gate 호출17실인수 미결속을 유지하며, CSV 이름만으로 raw→HMI 표시 이벤트를 확정하지 않는다. 독립 HMI 조작/독립 PLC 출력은 센서 문서 경계상 비해당; 실제 표시 연결은 근거 미확보다.

## 3. 제어 구조 — 적용: raw, 처리, 기억과 다른 쓰기

### 3.1 기억 설정의 원본 핀

0288-FlgNet.xml LAD1923/NID13, r1 scraps gate 2:
- W49 powerrail→Contact21.in; W50/ORef36→RID1 ON operand.
- Contact21.out W51→Contact22.in 및 Contact27.in. Contact22 operand W52/ORef37→RID85 Q5.4.
- Contact22.out W53→Contact23.in와Contact24.in. Contact23 operand W54/ORef38→RID135 I9.4. Contact24 operand W56/ORef39→0609 RID136 DB13.DBX9.4.
- Contact23.out W55→OR25.in1; Contact24.out W57→OR25.in2. OR25.out W58→SCoil26.in; W59/ORef40→0609 RID55 MEM_OPEN.
- Contact27은 operand Negated: W60/ORef41→Q5.4. out W61→RCoil28.in; W62/ORef42→RID55 MEM_OPEN.

백업 조건은 S(MEM_OPEN)=ON AND Q_A AND(raw_OPEN OR Inputs_OPEN), R(MEM_OPEN)=ON AND NOT Q_A다. LS25 raw와 Inputs에는 이 OPEN 가지에서 Negated가 없으며, 반전은 Q_A Reset 조건에 있다. 전기도면 접점13–14/정논리 사용이 현장 정상극성·안전위치 증거는 아니다. 이 네트워크에 CRef 호출은 없다.

비교 CLOSE 가지는 NOT Q_A Contact29.out W64가 Contact30/31.in으로 가고, operand는 각각 W65/ORef44(raw_CLOSE), W67/ORef45(Inputs_CLOSE)다. W66/W68은 OR32 입력선이다. 기존 CYL-CL05 초안의 W64/W66 operand 표기 오류는 보강 정정대로 W65/W67로 유지한다. 이 비교는 LS26을 LS25 소유로 옮기는 뜻이 아니다.

### 3.2 raw의 처리 DB 복사와 호출 조건

0397-FlgNet.xml LAD1070/NID1 HMI Inputs에서 Move43.in W55/ORef47→0627 RID15 Tag_181, Input Word AO64=IW8. Move43.out1 W57/ORef48→0629 RID16 Word AO64 BAD4→0628 RID4 Inputs TOD13=DB13.DBW8. 따라서 I9.4를 포함하는 IW8의16비트가 DB13.DBW8에 전달되는 정적 경로가 있다. 이 경로에 LS25 단독 NOT·디바운스·스케일링은 없다. Move43.en은 Move42.eno에서 W53으로 이어지며, Move43의 DisableENO=true 표기도 보존한다. 연결만으로 항상 실행/최종값을 확정하지 않는다.

0030-FlgNet.xml LAD1613/NID19: CRef21 Recipes Handler(CodeBlock22 RID120) eno→W32→CRef23 HMI(CodeBlock24 RID124) en; eno→W33→CRef25 HMI Output(CodeBlock26 RID128) en; eno→W42→Contact37.in. Contact37 operand는 W44/ORef45→0692 RID140 Simulation(1), Memory AO1440=M180.0이며 Negated다. Contact37.out W43→CRef28.en; CRef28 RID136→0694 BIID TORID135→0688 RID135 HMI Inputs FC15(CodeBlock29). 따라서 NOT Simulation(1) 및 앞 ENO 연결의 조건부 호출 경계다. 현재 M180.0/ENO/스캔호출은 미확정이다.

### 3.3 다른 DB 쓰기: 보존 원문의 정적 확인

0411-FlgNet.xml LAD1091/NID13, block simulation의 보존 원문에는 다음 별도 쓰기가 있다. 시뮬레이터 생성·수정·실행·행동시험은 전혀 하지 않았다.
- Contact22 operand W39/ORef30→0636 RID213, Q5.4 Output AO44, NID13 UID30.
- Contact22.out W40→Coil23.in; Coil23 operand W41/ORef31→0635 RID215, AO76 BAD5→0634 RID5 Inputs TOD13, NID13 UID31 Write.
- 따라서 이 원문의 쓰기 대상은 DB13.DBX9.4이고 raw I9.4가 아니다. Coil23은 일반 Coil이며 Set 기억 코일도 아니다.

같은 NID13이라도 0607 RID135를 simulation 문맥에 끼워넣지 않는다. 0635/0636 선언 문맥을 별도 결속했다. 원문에 경로가 있다는 것은 현재 CPU에서 실행 중이라는 뜻이 아니다. 동적 최종값·호출 순서·추가 간접 쓰기는 현재 프로젝트 교차참조가 필요하다.

### 3.4 기억의 전체 Word 초기화

0147-FlgNet.xml LAD402/NID2 startup only에서 Contact208 ON(0047 RID1, M0.0, W184/ORef167)의 out W209→Move155.en. Move155.in W196/ORef176→0048 RID54 INT#0; out1 W197/ORef177→0563 RID15 Word AO64 BAD6→0562 RID6 Flag TOD2, 즉 DB2.DBW8이다. 따라서 MEM_OPEN(DBX8.5)과 MEM_CLOSE(DBX8.4)를 포함하는 Word에 초기화 쓰기가 존재한다. 0288 개별 S/R만 유일한 쓰기라고 설명하지 않는다.

0150-FlgNet.xml LAD405/NID5의 ON Contact326.out W327→SCoil303.in, W320/ORef314→0563 RID49 AO68 BAD6는 A MEM_CLOSE Set이다. 이것은 LS25 OPEN Set이 아니며 시작시 닫힘기억이 실제 닫힘을 확인했다는 증거도 아니다. 해당 선언·상수와 원문은 selected-xml.txt의 추가 발췌에 포함했다.

전체 Ident XML의 AO76 포함 쓰기 후보 검색은 서로 다른 DB의 같은 오프셋도 포함한다. 그 후보 수를 LS25 쓰기 수로 세지 않는다. 직접 결속한 처리 DB 쓰기는 0397 Word와0411 bit이며, 기억은0288 S/R 외0147 Word 초기화가 있다. 전체 간접/외부 쓰기 부재를 주장하지 않는다.

## 4. 전기 전달 경로 — 적용, 시공 접속표 미확보

Electrical_Rev2.pdf 실제 PDF73/FG72를 렌더해 접점·단자를 확인했다:

+24Vdc10.7 → X1/145 (5×20, 2A F 도면표기) → wire72.1 → LS-25 접점13–14 → X1/146 → E9.4, cross-ref125/5.

실제 PDF126/FG125의 대응은 E9.4, 역참조72/1 → CPU515 MOD10 단자15, 설명 LIMIT SWITCH LS-25 GATE “A” OPEN VALVE PV-02다. 페이지의 모듈 전원은 +24Vdc10.7→X21/3010(5×20 2A IST.)→wire125.1→단자19, −0Vdc10.6→단자20이다. 이 도면 정격은 현행 설치 보호값이나 교체 승인값이 아니다.

센서 접점 양 끝점과 PLC 끝점이 문서상 연속하나 OEM X1/145·146과 현장 ROT1TB1 개별 단자·심선의 일대일 대응표는 없다. 전기도면의 접점 기호만으로 현장 장착시 NO/NC·정상 0/1·배선 단선진단을 확정하지 않는다.

시공 PDF24: ROT1TB1의 분기5→LS-25. 도표의 LS25 짧은 Cable No.5_3, 전체 =ROT+PV02-LS25A, CVV1.0 2core. PDF55: No.5_4 =ROT+PV02-LS25A, FROM UC-01 ROT1TB1→TO PV-02 LS-25, DC CVV 2C1.0, SPARE0, 경로 RDD1 E300→100 RDD1→RDD1 E500, LEN13 표기. 길이단위는 이 페이지에서 독립 확인하지 않아 임의로 m를 붙이지 않는다.

상충: LS25의 짧은 번호5_3/5_4는 동일하지 않다. PDF55의5_3은 별도의 RD01-ROT1TB2A다. 전체 ID·FROM/TO와 함께 대조하고 임의 수정하지 않는다. 공통 ROT1TB1A는 PDF24 CORE26 대 PDF55 25G로도 상충한다. PDF55 LS27/28 추가 행은 LS25의 별명으로 합치지 않는다. 최신 승인 시공도·개별 단자/심선표가 필요하다.

부모 EV04 구동은 PV02/CYL-CL05 공통근거를 참조한다. 69KA/71KA 부하 접점은 기존 정정5–9를 유지한다. LS25 입력 조사에서 부모 출력 회로를 다시 검토한 것으로 세지 않으며 센서에 독립 EV 출력/코일을 배정하지 않는다.

## 5. 알람·복구 — 부모 참조 적용, LS25 독립 알람 근거 미확보

부모 PV02 초안 §5의 Gate A 위치 미확인 감시(0451/NID44,0656~0658 선언,7초)는 부모 기능이다. LS25 독립 알람·독립 타이머로 복제하지 않았다. 이번 직접 핀검토에 그 알람 네트워크 전체는 포함하지 않았다. 원시 입력만이 아니라 처리 DB와 MEM이 부모 판단에 관여하므로 부모 알람 하나를 LS25 단독 고장으로 확정할 수 없다.

부모 Reset, MEM 변화, HMI 표시 해제는 센서 기계 작동점·배선·Gate A 실제 복구 증거가 아니다. 복구 판정에는 승인된 현행 회로 및 동일시각 실물/LS25 raw/DB13/MEM/부모 알람 관찰이 필요하다. 강제출력·접점우회·감시연장·반복 Reset을 조치로 제시하지 않는다.

## 6. 증상별 관찰 — 적용, 수리·운전 미수행

자격자의 승인 점검에 필요한 자료 목록이다. 접근 전 전기·공압·중력/끼임 위험 통제와 격리 절차가 선행되어야 하며 본 문서는 통전 점검·운전 명령이 아니다.

| 증상 | 분리해서 수집할 관찰 | 비교/배제 경계 |
|---|---|---|
| Gate A 열림인데 I9.4가0 | 실물 위치/LS25 표찰·작동점, 접점13/14, X1/145·146, MOD10/15 관찰을 시각과 함께 기록 | 기구 미도달/센서/전원/전달단을 분리; 강제조작 금지 |
| raw와Inputs가 다름 | I9.4, DB13.DBX9.4, M180.0·HMI Inputs 호출·현재 교차참조 | 0397 조건부 복사 및0411 다른 쓰기를 검토; 즉시 센서불량 판정 금지 |
| raw0인데MEM_OPEN1 | DB13 값, Q5.4, ON, MEM 이력·시각 | raw OR Inputs와S/R 기억을 구분; 기억1은 실물 확인 아님 |
| 시작 후표시/기억 변화 | 시작 이벤트, DB2.DBW8 초기화 및MEM_CLOSE Set의 현재 프로젝트 근거 | startup 상태와 실제 기계위치 구분 |
| HMI와현장 불일치 | DB11.X78.1, DB13, I9.4, DB2와화면 객체/이벤트 Export | CSV 설정만으로실인수/통신상태확정금지 |
| 케이블 번호가 안 맞음 | 전체 =ROT+PV02-LS25A, 양 끝 표찰, 승인 개정·단자/심선표 | 5_3/5_4 상충을 임의해소하지 않음 |

기록필드: 관찰자, 시각/시간대, 실물표찰/위치, 현재프로젝트/장치 식별, 신호명·값·단위, 수집장치, 비교원본·끝점, 배제결과, 승인조치, 복구확인자/증거. 실제 운영·사진·수리기록은 생성하거나 복제하지 않았다.

## 7. 완료·누락과 인계 — 적용

| 상태 | 결과 |
|---|---|
| documentation | complete_with_gaps 조사 초안, 부모 독립검토 대기 |
| static_review | 선정 원본 바이트 검증 및 아래 XML·PDF 의미검토; 현재 실행/간접쓰기 완전성 미확정 |
| ui_records | not_run: 도면·래더 비교/백업·선택복원/전후비교/보고서PDF의 LS25 적용 구현·저장·재열기 미검증 |
| publication | not_published, 부모 게시 상태 상속 안 함 |
| tia_compile / live_cpu / field_recovery | not_performed |

남은 자료:
1. LS25 명판·설치도·제조사 형식/단자/접점·작동점 및 CL05/Gate A 실물 연계 증거.
2. 최신 승인 OEM↔ROT1TB1↔LS25 개별 단자·심선표, 5_3/5_4 및26/25G 상충 해소 개정.
3. 현재 CPU 프로젝트·호출순서·모든 직접/간접/외부 쓰기 교차참조. 보존 simulation 원문이 현행 실행이라는 추정 금지.
4. HMI PV_2Gate 실인수 Export와 LS25 관련 표시 객체·이벤트·통신 근거.
5. 정상극성·현행 보호값·실제 Gate A 도달/알람/복구의 승인 관찰 기록. 문서 검사를 현장 복구 완료로 대신하지 않는다.

다음 한 작업: 부모 검토자가 LS25 원본 선언/끝점·다른 쓰기를 검토하고, 허용된 통합 단계에서 고유 센서 관계만 반영한다. 새 근거 없이는 미확정을 추정으로 메우지 않는다.

## 부록 A. 직접검토·검사와 근거 보존

직접 의미검토: 네트워크 XML6개(0288,0397,0030,0411,0147,0150), 대응 선언 XML16개(0607~0609,0627~0629,0634~0636,0688,0692,0694,0047/0048,0562/0563)의 대상 부분, HMI CSV1개, PDF3파일의5페이지. 네트워크/선언 전체의 모든 설비 의미를 검토한 것은 아니다. 대장·지침·기존 초안은 분류/색인 검토이며 PDF 확대3개를 페이지수에 중복 합산하지 않았다. 이름/주소후보 정적검색과 SHA검사수는 의미검토수와 다르다.

선정 원본 SHA256/고정 Gitblob 바이트 검사는 source-integrity.json에 있다. 아래 표는 source-mv06 상대경로다. 파생 연구지침·scope·overlap·부모 초안은 research-index-integrity.json에 별도로 해시했으며 고정 Gitblob 원본이라고 부르지 않는다. 보존 원문을 읽었을 뿐 시뮬레이터나 앱을 작성·생성·실행하지 않았다.

선정 해시검사 37파일, 고정 Gitblob 바이트 일치 37/37, 원본 Git 변경 0행.

| 원본 경로 | SHA256 | 고정 Gitblob OID | 바이트 일치 |
|---|---|---|---|
| AGENTS.md | `0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2` | `073164bc6efd5791032d62c71b03b4dab48cb6f8` | True |
| .agents/skills/gme-equipment-rollout/SKILL.md | `fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b` | `9aa820ea6ca15b4e136c9772423b78ed4df6a3d4` | True |
| docs/equipment-standard/WORK-STANDARD.md | `05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99` | `f76a570cc73098632e08759b17934000f7e3a253` | True |
| docs/equipment-standard/WORK-ITEM-TEMPLATE.md | `4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586` | `e546f39535d2b589e80f97db869ac37ce4d05cfd` | True |
| docs/equipment-standard/INVENTORY.json | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` | `587c3748ad9224718f95ba06463fee913dae231d` | True |
| VERSION.json | `5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7` | `fffb51663b7705aec91cb119ca80ee943a4ce758` | True |
| WORKSPACE-HANDOFF.md | `215096d997782e78e901dfae36c782937e49611fbeb677a0d3fa50cbecf8d074` | `dd0b8989d2376c4415bba9bd826fe6754c6b1a12` | True |
| PUBLICATION_STATUS.md | `efe4857aec598d90470322cf3962eb3fe1f64947630e1fdf71d1c90134de8740` | `d76401cf291fc0be681acc51fa898ad3ce46ff78` | True |
| EXPANSION-WORK.md | `ec624de9fd2fcfac861a67fd5e828b25ef46db50bfd7a37ff16e2cb54cd0f7e2` | `4c42d88ecc2d48269eb23e13a20ebf3721a092a1` | True |
| all-in-one/ACTIVE-WORK.md | `eff3bbc08ecff41da3beff77f3fec48e7d148708192bcaaab00f34b6a721afc2` | `6eb947c629b5ddf9c759ef87649451303938864b` | True |
| all-in-one/sources/Electrical_Rev2.pdf | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` | `f610fd7c7ce14ae951b00cff57b969259bfb389d` | True |
| all-in-one/sources/Electrical_Can_Decoating_20241118.pdf | `3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd` | `0ee6b6f8361c5790864dbba4bbd9d55e8e7c08f8` | True |
| all-in-one/sources/PID_1684n002I.pdf | `2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b` | `8c83a59fefd5b8b651ec3537ea4236a073f5e109` | True |
| all-in-one/sources/hmi_plc_tags.csv | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` | `cf4c0650e7c7baac350dcb89909b808435704880` | True |
| all-in-one/sources/decoded-original/network-map.json | `c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60` | `424430b6b953e43138e5d0a18ca40c949e21cfa1` | True |
| all-in-one/sources/decoded-original/0288-FlgNet.xml | `af4d15dcde4680ef5b788f88f198a47886857c8db7f7d9b550276fb5eea3c90e` | `a7b2995e8d87de3990a201969c0f7b9547e6d0ba` | True |
| all-in-one/sources/decoded-original/0397-FlgNet.xml | `bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834` | `4ab8370493c4e28fc1eabeeebe2743d27f0c4021` | True |
| all-in-one/sources/decoded-original/0030-FlgNet.xml | `9252c9da764993de1edb8b2e44c46d6e9f9d4b6118e751a0dbeaa9ffd8ea721b` | `e74c70b751acdcdbc7a8b3b0c98aa773c2107cab` | True |
| all-in-one/sources/decoded-original/0411-FlgNet.xml | `282267b493e6b584959a5367d628bf86d15304d901a610614ecd2209d4d01884` | `c2143650e3de0e25c253e1652242e3cfdf4b394f` | True |
| all-in-one/sources/decoded-original/0147-FlgNet.xml | `386513b215a8cc433f414b1b08279e9760e0efe209070ea95f8e445f674f428c` | `0027890eca158e714dd6260dc920a5d3aa83319b` | True |
| all-in-one/sources/decoded-original/0150-FlgNet.xml | `829ca4aa3bd2bb6ee406f7f204add2987ec6159ef0fd6dd3dfc075592664a98e` | `b8130ae4a433018f7513d24bd8f0cf79a7897238` | True |
| all-in-one/sources/decoded-original/0607-IdentXmlPart.xml | `9b76b53536a26e7b45961fecbf825ae1552e16c2fd9af5736864193c01d77f93` | `dbd4da513171f04cca9b1c1741d0293c3e38f98c` | True |
| all-in-one/sources/decoded-original/0608-IdentXmlPart.xml | `24adec2035b65c0c310d637bcea74374896875b6465a16aa2f2cfc8fd55fa4b8` | `cea8f4160d2da00023b1ecc5e591b561e4a08330` | True |
| all-in-one/sources/decoded-original/0609-IdentXmlPart.xml | `395de8ebb2168848cf96fe015bd7334d71107c114a4e441ef36346b8f22031db` | `ee2aab34c0116642dd9f4364b236426f78a876a3` | True |
| all-in-one/sources/decoded-original/0627-IdentXmlPart.xml | `08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb` | `61ebc0abbb2ca160e11e1da400a3f14a397d8bc5` | True |
| all-in-one/sources/decoded-original/0628-IdentXmlPart.xml | `9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd` | `170ca5c72599edc7ea7eefe651c3680ce325e76a` | True |
| all-in-one/sources/decoded-original/0629-IdentXmlPart.xml | `67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972` | `058129bb01e27f7a6a0d0293f332d745e5bab74e` | True |
| all-in-one/sources/decoded-original/0634-IdentXmlPart.xml | `af3fcb536a6270ffb9a19e5b3f2c284a38d67d465f5147961005c1c01d11299d` | `877d9e0734dc7f3e5a8cea789eeb58a208501f48` | True |
| all-in-one/sources/decoded-original/0635-IdentXmlPart.xml | `1a057d686446a3fdab7ac61bb09bc543c52f49646c9ca71ac323c10fcdffe457` | `95bfcad59cfb0c12b573e9e8face4262d1e94622` | True |
| all-in-one/sources/decoded-original/0636-IdentXmlPart.xml | `ec3d79f03e2748f8def4409ad676a97b98e28b9d8e68f6a64b3fe894466832ca` | `86114327ba1a010b2fcc01dd12b1bf86c01bc02c` | True |
| all-in-one/sources/decoded-original/0688-IdentXmlPart.xml | `ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda` | `463585759f1ecd94f32362b4fefb000a152f5773` | True |
| all-in-one/sources/decoded-original/0692-IdentXmlPart.xml | `bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037` | `737785d03b5fad43c5b4d451955726d800edb1c0` | True |
| all-in-one/sources/decoded-original/0694-IdentXmlPart.xml | `757ccebdf32d0a168dd787bfa735fe6494eac4c4a9f7a5adc63898a88e8b152d` | `c45e8f3ca4129dc06734f6a12ef79e6ed6528a7d` | True |
| all-in-one/sources/decoded-original/0047-IdentXmlPart.xml | `2e53bb895dd1ad2a74efaeb1ef16dfd61e62b1b2d7aa34cec8612f1b9cb0928e` | `3dc282f149a21fdf76d5521ef1c833be63b578b4` | True |
| all-in-one/sources/decoded-original/0048-IdentXmlPart.xml | `d8e8687de7271bd294c2b62b33d789700af9d5014d82b130141988c4d479253d` | `64fc5a7f1ad33f3b901b00f0d22d23578ffabff8` | True |
| all-in-one/sources/decoded-original/0562-IdentXmlPart.xml | `85aada44dd9a3e66835463c3fed400f1efe121f4f5bc5ab8f0ad49481ec0ea1c` | `1609802542a3e560baba3f2b73c306be281dfb23` | True |
| all-in-one/sources/decoded-original/0563-IdentXmlPart.xml | `86cf35b6baebc079cb5a092baf53ec3364c377ea7318eb263ab69c8b4550b4ad` | `6a10fc694f896cda16409804daf2554c91635654` | True |
