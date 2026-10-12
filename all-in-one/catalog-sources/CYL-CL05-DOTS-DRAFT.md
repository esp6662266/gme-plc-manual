# CYL-CL05 고유 구성품 조사 초안

- 대상: CYL-CL05 공압 실린더 1개, 부모 PV02, phase2, parent_child_separate. CLIENT-CL05 Air knife와 별개다.
- 작성일: 2026-10-11 UTC. 표준: GME-STD-1.0.0. 고정 원본: source-mv06, abcf31c5030bc7ef8749ed8e869a857f2387a28a, VERSION v1.12.0.
- 범위: 자체 원본 정적 조사와 MD 초안. 부모 PV02 초안은 공통 탐색색인으로 재사용하고 CL05 고유 공압 분기와 접속 도식, 부모 Gate A에 이르는 전기·선언을 독립 확인했다. 부모 완료 상태를 상속하지 않는다.
- 쓰기 범위: 이 MD 및 extracts/CYL-CL05만. 원본·공통코드·대장·버전·운영/PLC/보호값/SEJIN 변경 없음. 시뮬레이터 작성·수정·생성·실행·행동시험, 원본 생성기·앱빌드 실행 없음. 원본 worktree clean 확인. 실제 모델/추론 설정은 관측 미확인.

## 1. 설비·자료 기준 — 적용

### 고유 식별과 소유

INVENTORY.json catalog[205]는 CYL-CL05를 kind=component, parent_id=PV02, depth=1, baseline/not_assessed로 둔다. GME-CATALOG-OVERLAP-REVIEW.json의 같은 행은 physical_identity_verified=false, parent_child_separate다. 이는 별도 조사 단위라는 뜻이며 부모와 실물 중복 또는 별도 PLC 출력 소유를 뜻하지 않는다. CLIENT-CL05는 부모 없는 Air knife/client 행이다. 이름의 05만으로 두 ID를 병합하지 않는다.

원본 PID_1684n002I.pdf 실제 PDF1을 회전·확대 렌더했다. PV-02 Detail에서 COMPRESSED AIR 공통선이 EV-04/EV-05로 갈라진다. EV-04 뒤 선은 CL-05와 CL-06 도식으로 분기하고, LS-26/LS-25 지시선이 CL-05 도식의 양쪽 위치에 놓인다. EV-05 뒤는 별도 CL-07/08이다. 오른쪽 기계 그림의 위 Gate “A”, 아래 Gate “B”와 OEM Gate A/EV04 표기를 교차 확인했다. CL05는 EV04 구동군에 속하지만 EV04는 CL05 단독 코일이 아니다. CL05와 CL06 동기성, 실제 로드·핀·실린더 설치 방향, 공압 포트 번호와 스트로크/보어/모델은 이 도식만으로 확정하지 않는다.

자료 구분:
- P&ID: drawing 1684n002, Apex I, 기본 날짜 06/04/2011; 변경란 I 15/01/2013. 실제 PDF1, FG 표기는 ‘−’. 렌더 pid-detail.png와 pid-title.png.
- Electrical_Rev2.pdf: 실제 PDF72=FG71, PDF73=FG72, PDF126=FG125, PDF142=FG141. 파일명 Rev2를 모든 페이지 개정으로 전파하지 않는다. FG71/72/125 기본 DATA 27.05.2024·개정란 공란; FG141 기본 DATA 27.05.2024·개정2 17.03.2025.
- Electrical_Can_Decoating_20241118.pdf: PDF24/64, CANDC-CONS-E007-024, D-PAGE7, ROTARY ROUTE CONDUIT PIPING(1); PDF55/64, CANDC-CONS-C005-055, D-PAGE5, CABLE SCHEDULE(4). 둘 다 변경란 No.1 24.11.11 first draft design. 승인 시공 완료 자료로 승격하지 않는다.
- 기존 devices/CYL-CL05.html의 직접 I/O·내부·HMI·래더 0은 이름 기반 미식별 상태다. 기존 시뮬레이션 계획은 역사 자료로 보존하며 최신 영구 중지 지침이 우선한다. 이번에 실행하거나 새로운 시험을 만들지 않았다.

## 2. I/O·HMI — 부모 연관 적용 / 독립 소유 근거 미확보

다음은 CL05 독립 신호 목록이 아니라 PV02 Gate A와 EV04 구동군의 백업 선언이다. XML 경로 약기는 all-in-one/sources/decoded-original/이다. AO는 비트 오프셋이며 현재 CPU 값·배선을 뜻하지 않는다.

| 신호 | 백업 주소/형식 | 원본 선언과 결속 | 소유 한계 |
|---|---|---|---|
| PV-02 GATE A EV | Q5.4 Bool | 0607-IdentXmlPart RID85 SAD Output AO44, NID8 UID733 Write | EV04→CL05/06 공유 명령 |
| EV04_Open | I9.4 Bool | 0607 RID135 SAD Input AO76, NID13 UID38 | OEM LS25 Gate A OPEN; CL05 단독 위치 확정 아님 |
| EV04_Close | I9.5 Bool | 0607 RID137 SAD Input AO77, NID13 UID44 | OEM LS26 Gate A CLOSED |
| Inputs.PV-02 EV A OPEN/CLOSE | DB13.DBX9.4/9.5 Bool | 0609 RID136/138 AO76/77 BAD86;0608 RID86 Inputs TOD13;NID13 UID39/45 | raw와 다른 처리 변수 |
| Flag.PV_02_GATE_A_MEM_OPEN/CLOSE | DB2.DBX8.5/8.4 Bool | 0609 RID55/139 AO69/68 BAD5;0608 RID5 Flag TOD2;NID13 UID40/42,46/48 | 방향별 기억; 실물 센서 아님 |
| Open EV A 00 PV-02 | M30.4 Bool | 0607 RID80 Memory AO244, NID8 UID730 | 부모 local 요청 |
| Open EV A 01 PV-02 | M30.3 Bool | 0607 RID61 Memory AO243, NID8 UID731 | 부모 auto 요청 |
| maintenance PV02 | M80.6 Bool | 0607 RID83 Memory AO646, NID8 UID732 | 부모 공통 가지, 쓰기 경로 미확정 |
| ON | M0.0 Bool | 0607 RID1 Memory AO0, NID8 UID725/NID13 UID36 | 명칭이 ON인 메모리, 상수 true 아님 |

hmi_plc_tags.csv의 PV_02\GateA_Open DB11,X78.1(000A6), GateA_Close DB11,X78.2(000A5), Allarme1 DB11,X78.0(00073), Flag DB2,X10.3(000A8)은 부모 설정이다. CL05 독립 HMI 태그·조작 객체·이벤트는 확보하지 못했다. 부모 PV02 초안 §2.4의 HMI 호출17실인수 미결속 경계도 유지한다. 이 CSV 일치로 표시/쓰기 이벤트나 CL05 독점 소유를 확정하지 않는다.

추가 부재 검색 근거: decoded-original의 XML 695개 전체를 CL05/CL-05/CL_05/CL 05/CYL-CL05 패턴으로 정적 검색한 결과 0건. 검색 파일수·정규식은 extracts/CYL-CL05/cl05-xml-search.json에 기록했다. 이것은 이름 검색 범위의 결과이며 별칭으로 존재할 모든 PLC 신호 부재를 증명하지 않는다. 단순검색 건수는 의미 검토 수가 아니다.

## 3. 제어 구조 — 부모 전달 경계 적용

0283-FlgNet.xml, LAD1920, block r1 scraps gate 2, 선언 NID8을 직접 확인했다. index_order10과 NID8은 다른 식별자다.

Q5.4 = ON AND (OpenA00 OR OpenA01 OR maintenance PV02).

- Part748 Contact의 operand W734/ORef725→0607 RID1. out W749가 A Contact756/758/760의 in으로 전달된다.
- Contact756 operand W741/ORef730→RID80; out W757→OR720.in1.
- Contact758 operand W742/ORef731→RID61; out W759→OR720.in2.
- Contact760 operand W743/ORef732→RID83; out W761→OR720.in3.
- OR720(Card=3).out W744→Coil724.in; Coil724.operand W746/ORef733→RID85(Q5.4).
- 이 A 구간에 CRef 호출은 없다. OFF 네 번째 가지도 없다. 별도 CL05 닫힘 코일을 만들지 않는다. Enable 해제만으로 local/maintenance 가지가 반드시 해제된다고 설명하지 않는다.

명령의 물리 전달은 Q5.4→71KA1→EV04→CL05/CL06 공유 공압 분기다. Q=0을 CL05 안전 닫힘이나 잔압 소거로 치환할 근거가 없다. 공압 스풀/복귀·스프링·밸브 포트·잔압 자료가 필요하다.

0288-FlgNet.xml LAD1923/NID13 Gate A 기억부도 직접 확인했다:
- ON Part21, Q Part22 후 raw Contact23(I9.4 W54/ORef38)와 처리 Contact24(DB13 W56/ORef39)가 병렬. W55/W57→OR25.in1/in2, out W58→SCoil26, operand W59/ORef40→RID55 MEM_OPEN.
- NOT Q Contact27→W61→RCoil28, operand W62/ORef42→RID55.
- NOT Q Contact29 후 raw Contact30(I9.5 W64/ORef44)·처리 Contact31(DB13 W66/ORef45)→OR32→W69→SCoil33, operand W70/ORef46→RID139 MEM_CLOSE.
- Q Contact34→W72→RCoil35, operand W73/ORef48→RID139.

따라서 OPEN 기억 Set는 ON·Q·(raw OR Inputs), CLOSE 기억 Set는 ON·NOT Q·(raw OR Inputs)다. 반대 방향 Q에 의해 각각 Reset된다. 입력 순간값/처리값/기억/기계위치는 별도로 관찰해야 한다. 부모 전체의 호출순서·자동 상태기계·다중 쓰기를 여기서 재조사하거나 CL05 로컬 순서로 복제하지 않았다. 부모 PV02 초안 §3을 공통 참조하되 현재 CPU 실행·호출·다른 쓰기 검증은 미수행이다.

## 4. 전기·공압 끝점 — 연관 회로 적용

### 출력/부하 분리

실제 렌더 FG141/PDF142에서 CPU515 MOD15 terminal15 A5.4→cross-ref71/3. FG71/PDF72에서 A5.4→71KA1 코일 A1, A2→−0Vdc10.6이다. +24Vdc10.9에서 X21/3033 5×20 4A F를 거쳐 모듈 전원 경로가 그려진다. 도면 보호기 표기를 현행 설치·허용 교체 정격으로 승인하지 않는다.

EV04 부하 경로는 110Vac9.7→71KA1 접점5–9→wire71.1→X1/141(5×20 2A F)→wire71.2→EV-04 A1→A2→X1/142→0Vac9.9다. 제어 24Vdc와 부하110Vac는 다른 회로다. 71KA1 하단 접점표의1/5/9를 실제 부하 접점1–9로 오독하지 않는다. 기존 PV01 69KA 및 PV02 71KA 정정5–9를 유지하며, CL05 문서에는 관련71KA1만 직접 연결한다.

### 위치 경로

FG72/PDF73: +24Vdc10.7→X1/145(2A F)→wire72.1→LS25 13–14→X1/146→E9.4→FG125/PDF126 CPU515 MOD10 terminal15. CLOSE는 +24Vdc10.7→X1/147(2A F)→wire72.2→LS26 13–14→X1/148→E9.5→FG125 terminal16. 두 신호의 OEM 명칭은 Gate A OPEN/CLOSE다. P&ID가 CL05 도식에 붙여 그린 센서라는 사실과, 현장 CL05만의 독립·안전 등급 피드백이라는 주장은 구분한다. 도면 접점 기호는 현재 장착 극성이나 정상 운전값을 대신하지 않는다.

### 시공자료와 끝점 공백

PDF55 Cable Schedule(4):
- 5_8 =ROT+PV02-EV04A, UC-01 ROT1TB1→PV-02 EV-04, AC CVV 3G 1.0, spare0.
- 5_4 =ROT+PV02-LS25A, UC-01 ROT1TB1→PV-02 LS-25, DC CVV 2C 1.0, spare0.
- 5_5 =ROT+PV02-LS26A, UC-01 ROT1TB1→PV-02 LS-26, DC CVV 2C 1.0, spare0.

PDF24 도식 ROT1TB1의5/6/7 분기는 LS25/LS26/EV04다. 이 페이지의 짧은 Cable No.는 LS25=5_3, LS26=5_4이나 PDF55는5_4/5_5다. 전체 케이블 ID와 FROM/TO를 함께 사용하고 번호를 임의 정정하지 않는다. 공통 ROT1TB1A의 PDF24 CORE26와 PDF55 25G도 상충으로 보존한다. PDF55 LS27/28 추가 행을 CL05 리미트로 배정하지 않는다. OEM X1/141~148↔ROT1TB1 개별 단자/심선 매핑은 미확보다. 공압 튜브·EV04 포트↔CL05 양 챔버 식별은 전기 케이블표에서 해결되지 않는다.

## 5. 알람·복구 — 부모 참조 적용 / 독립 알람 미확보

CL05 고유 알람 선언·전용 타이머·복구 시퀀스 근거는 확보하지 못했다. PV02 Gate A 열림/닫힘 미확인 알람은 부모 기능으로 유지한다. 기존 PV02 초안 §5의 원본 위치(0451/NID44;0656~0658 선언), 부모의7초 감시와 Reset 설명을 참조하되 CL05 독립7초 알람으로 복제하지 않는다. 이번 선정 XML 의미검토는0283/0288과0607~0609이며 부모 알람 전체의 재검토를 수행한 것으로 집계하지 않는다.

Gate A 알람 하나로 CL05 고장이라고 판정할 수 없다. EV04 전원·릴레이·공압 공급·CL06/게이트 공통 기구·LS25/26 전달·raw/Inputs/MEM을 분리해야 한다. 부모 알람 Reset은 기계 복구·안전 위치·실린더 정상 판정과 다르다. 강제출력, 접점 우회, 타이머 연장, 반복 Reset을 처방하지 않는다.

## 6. 증상별 관찰 — 적용, 실제 수리/운전 미수행

승인된 현장 점검에서 수집할 자료 목록이다. 전기 격리·잔압·중력/끼임 위험 통제와 자격자의 승인 절차가 선행되어야 하며, 본 문서는 통전·접근·운전 명령이 아니다.

| 증상 | 분리 관찰과 비교 | 오판 방지·필요 증거 |
|---|---|---|
| CL05 움직임 없음 | local/auto/M80.6→Q5.4→71KA1 코일/5–9→EV04 전원→공압 분기 순서의 동일시각 관찰 | Q=1은 EV 전압·공기압·이동 완료 증거 아님; 현행 결선/밸브형식 필요 |
| CL05와 CL06 움직임 다름 | 같은 EV04 구동군의 양 실린더 실제 위치·로드/연결·튜브 식별 | 공동 코일만으로 동기 이동 단정 금지; 독립 위치 관찰 필요 |
| CL05 이동 보이나 Gate A 알람 | LS25/26 상태→I9.4/9.5→Inputs→MEM→부모 알람을 분리 | CL05 실물만으로 Gate A 전체/CL06 완료 판정 금지 |
| 표시와 실물 불일치 | HMI DB11 표시, raw, DB13, DB2 기억, 실물의 시각 일치 기록 | CSV 주소는 현재 통신·이벤트·HMI 호출 결속 증거 아님 |
| 출력 해제 뒤 위치 불명 | Q5.4, EV04 전원, 승인된 비접촉 위치 관찰과 공압 회로 도면 비교 | Q0을 닫힘/무압/접근 안전으로 간주하지 않음 |

관찰 기록 필드: 관찰자·시각/시간대·CL05/CL06 표찰 위치·원본/현재 프로젝트 식별·신호명/값/단위·수집장치·사진 근거·비교 끝점·배제 결과·승인 조치·복구 확인자. 실제 사용자 운영기록은 생성·복제하지 않았다.

## 7. 완료·누락과 인계 — 문서 초안, 현장 미확정 유지

| 상태 | 결과 |
|---|---|
| documentation | complete_with_gaps 초안:7영역·직접 근거·소유·상충·누락 명시 |
| static_review | 아래 선정 파일 바이트 검증 및 지정 XML/실제PDF7페이지 의미 검토 완료; 독립 검토는 부모 검토 대기 |
| ui_records | not_run. 도면/래더 비교, 백업·선택 복원, 기록 전후 비교, 보고서/PDF UI 네 기능은 요구 후보이며 구현·저장·재열기 검증 없음 |
| publication | not_published: 이 CYL-CL05 초안 게시 안 함. 기존 PV02 게시 결과를 상속하지 않음 |
| tia_compile/live_cpu/field_recovery | not_performed |

남은 자료와 판정 조건:
1. CL05 실물 표찰/명판/설치도 및 Gate A 링크·CL06 관계. P&ID 그림과 실제 부품 번호가 일치해야 실물 대응을 확정한다.
2. EV04 제조사/포트·스풀·복귀·튜브 양 끝점 도면, 실린더 모델/스트로크/부착. 압력·유량·정비 주기·토크·안전 위치는 승인 자료 없이 채우지 않는다.
3. 현행 OEM↔ROT1TB1 단자/심선표와 Cable No. 상충 개정 자료. 현재 보호기·정상 극성·배선은 현장 확인 전이다.
4. 현재 CPU 프로젝트/호출·다중쓰기/원시전달 및 HMI 실인수·이벤트. 부모 정적 백업을 현행과 동일하다고 단정하지 않는다.
5. 부모 Gate A 알람과 CL05/CL06 실제 위치를 동시 관찰한 복구 증거. 문서 확인으로 현장 완료 처리하지 않는다.

다음 조치: 부모 검토자가 이 초안의 CL05 고유 소유·P&ID 및7페이지 끝점과 해시를 독립 확인한 뒤, 허용된 통합 작업에서 필요한 연결만 반영한다. 새 자료 없이는 미확정 항목을 반복 추정하지 않는다.

## 부록 A. 검증 범위와 파일

직접 의미 검토는 PLC XML5개(0283/0288,0607/0608/0609), 원본 PDF3파일의7페이지(PID1;OEM72/73/126/142;시공24/55), HMI CSV1개다. 선언 부분 발췌 및 핀 대조는 selected-xml.txt에 있다. 대장·지침·기존 페이지·색인은 별도 배경/보존 확인이며 XML 전체 이름검색 및 SHA 검사는 의미 검토 수에 더하지 않는다. 이미지9개는 PDF7페이지 렌더+PID 상세/제목 확대2개다.

선정 원본 전부에 대해 SHA256과 고정 commit Gitblob 바이트 동등성을 검사했다. 아래 검증은 현장/CPU 동일성 검증이 아니다. 공유 초안/PV01-PV02 정정은 파생 연구 자료로 별도 참조했으며 Gitblob 원본으로 위장하지 않는다. 검사 JSON: ../extracts/CYL-CL05/source-integrity.json.

선정 해시 검사 22파일, 고정 Gitblob 바이트 일치 22/22; source Git 변경0.

| 원본 경로(source-mv06 기준) | SHA256 | 고정 Gitblob OID | 바이트 일치 |
|---|---|---|---|
| AGENTS.md | `0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2` | `073164bc6efd5791032d62c71b03b4dab48cb6f8` | True |
| .agents/skills/gme-equipment-rollout/SKILL.md | `fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b` | `9aa820ea6ca15b4e136c9772423b78ed4df6a3d4` | True |
| docs/equipment-standard/WORK-STANDARD.md | `05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99` | `f76a570cc73098632e08759b17934000f7e3a253` | True |
| docs/equipment-standard/WORK-ITEM-TEMPLATE.md | `4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586` | `e546f39535d2b589e80f97db869ac37ce4d05cfd` | True |
| docs/equipment-standard/INVENTORY.json | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` | `587c3748ad9224718f95ba06463fee913dae231d` | True |
| VERSION.json | `5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7` | `fffb51663b7705aec91cb119ca80ee943a4ce758` | True |
| WORKSPACE-HANDOFF.md | `215096d997782e78e901dfae36c782937e49611fbeb677a0d3fa50cbecf8d074` | `dd0b8989d2376c4415bba9bd826fe6754c6b1a12` | True |
| PUBLICATION_STATUS.md | `efe4857aec598d90470322cf3962eb3fe1f64947630e1fdf71d1c90134de8740` | `d76401cf291fc0be681acc51fa898ad3ce46ff78` | True |
| all-in-one/ACTIVE-WORK.md | `eff3bbc08ecff41da3beff77f3fec48e7d148708192bcaaab00f34b6a721afc2` | `6eb947c629b5ddf9c759ef87649451303938864b` | True |
| EXPANSION-WORK.md | `ec624de9fd2fcfac861a67fd5e828b25ef46db50bfd7a37ff16e2cb54cd0f7e2` | `4c42d88ecc2d48269eb23e13a20ebf3721a092a1` | True |
| all-in-one/devices/CYL-CL05.html | `c991ac374fd21d61b0ccdb20a098626f7d7001ef213f5026610f5be5a2349211` | `995bb3e444ef6a7ba8354d6ca95dd642dcb11a08` | True |
| all-in-one/devices/CLIENT-CL05.html | `7af37ef78d507e385c99180a01448e28d9ab6308b063196ceb57798f9c7e3116` | `9474828095edba234b2e370a049e8a060b701856` | True |
| all-in-one/sources/PID_1684n002I.pdf | `2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b` | `8c83a59fefd5b8b651ec3537ea4236a073f5e109` | True |
| all-in-one/sources/Electrical_Rev2.pdf | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` | `f610fd7c7ce14ae951b00cff57b969259bfb389d` | True |
| all-in-one/sources/Electrical_Can_Decoating_20241118.pdf | `3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd` | `0ee6b6f8361c5790864dbba4bbd9d55e8e7c08f8` | True |
| all-in-one/sources/hmi_plc_tags.csv | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` | `cf4c0650e7c7baac350dcb89909b808435704880` | True |
| all-in-one/sources/decoded-original/network-map.json | `c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60` | `424430b6b953e43138e5d0a18ca40c949e21cfa1` | True |
| all-in-one/sources/decoded-original/0283-FlgNet.xml | `ab46cabcba6cbf8155c47075a66a1573d9f12e01de1f2faccc0eb8ed2cb69cc3` | `996699492035dd8f7ab7e9fbaa0e0033b4cf7407` | True |
| all-in-one/sources/decoded-original/0288-FlgNet.xml | `af4d15dcde4680ef5b788f88f198a47886857c8db7f7d9b550276fb5eea3c90e` | `a7b2995e8d87de3990a201969c0f7b9547e6d0ba` | True |
| all-in-one/sources/decoded-original/0607-IdentXmlPart.xml | `9b76b53536a26e7b45961fecbf825ae1552e16c2fd9af5736864193c01d77f93` | `dbd4da513171f04cca9b1c1741d0293c3e38f98c` | True |
| all-in-one/sources/decoded-original/0608-IdentXmlPart.xml | `24adec2035b65c0c310d637bcea74374896875b6465a16aa2f2cfc8fd55fa4b8` | `cea8f4160d2da00023b1ecc5e591b561e4a08330` | True |
| all-in-one/sources/decoded-original/0609-IdentXmlPart.xml | `395de8ebb2168848cf96fe015bd7334d71107c114a4e441ef36346b8f22031db` | `ee2aab34c0116642dd9f4364b236426f78a876a3` | True |

검사 실패/도구 제한: HTML 가독화 도구 bs4 모듈 미설치로 첫 읽기 실패 후 내장 HTML 제거/이스케이프 해제로 원문을 읽었다. 자료 손실 없이 재확인했고 설치·외부 변경은 하지 않았다. 원본 생성기/행동시험 미실행.
