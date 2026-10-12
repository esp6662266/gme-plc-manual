# CYL-CL07 고유 구성품 조사 초안

- 대상: CYL-CL07 공압 실린더, 부모 PV02, phase2, parent_child_separate. 외부 CLIENT-CL07 Shredder 1과 별도 ID다.
- 기준: GME-STD-1.0.0; source-mv06 고정 abcf31c5030bc7ef8749ed8e869a857f2387a28a, VERSION v1.12.0. 조사일 2026-10-11 UTC. 실제 모델/추론 설정 관측 미확인.
- 작업: 읽기 전용 원본 조사와 자체 초안/추출만 작성. 부모 PV02와 CYL-CL05 초안은 탐색색인·공통근거로 재사용하고 CL07 고유 P&ID 분기, Gate B 출력/기억 및 도면 끝점은 직접 확인했다. 부모 전체 자동순서·알람 재조사는 하지 않았다.
- 보존: 원본·공통코드·대장·버전·배포·운영·PLC·현장·보호값·SEJIN 변경 없음. 원본 Git 변경0. 시뮬레이터 작성·수정·생성·실행·행동시험, 원본 생성기·앱빌드 모두 미실행. 쓰기는 drafts/CYL-CL07-DOTS-DRAFT.md와 extracts/CYL-CL07만.

## 1. 설비·자료 기준 — 적용

INVENTORY.json catalog[207]에서 CYL-CL07는 공압 실린더/component, parent_id=PV02, depth1, phase2, baseline/not_assessed다. GME-CATALOG-OVERLAP-REVIEW.json catalog_rows의 동일 ID는 parent_child_separate, physical_identity_verified=false다. 별도 문서 조사단위이며 부모 완료나 실물 검증을 상속하지 않는다. CLIENT-CL07.html의 Shredder 1은 이름공간이 다르고 해당 외부 모터 신호·알람을 가져오지 않는다.

PID_1684n002I.pdf 실제 PDF1의 PV-02 Detail을 직접 회전·확대 렌더했다. COMPRESSED AIR 공통선에서 EV-04/EV-05로 분기하며, EV-05 이후 CL-07과 CL-08의 도식이 공유 분기로 연결된다. LS-30 리더는 CL-07 몸체/로드 인접부, LS-29 리더는 CL-07 로드 측에 붙는다. CL-08에는 이와 같은 별도 LS 리더가 그려져 있지 않다. 오른쪽 기계 그림은 위 Gate “A”, 아래 Gate “B”이고, OEM 전기도면의 Gate B/EV05 명칭과 교차 확인했다. 따라서 CL07는 EV05 구동군에 속한다. EV05가 CL07 전용 코일이라는 뜻은 아니며, 그림의 리더만으로 현장 센서 장착 위치·CL07만의 독점 피드백·정상 극성·안전기능을 확정하지 않는다.

자료 시점과 실제 페이지:
- P&ID: 1684n002, Apex I, 기본 06/04/2011, 변경 I 15/01/2013, FG ‘−’, 실제 PDF1. pid-detail.png 및 pid-title.png 참조.
- Electrical_Rev2.pdf: FG71/PDF72, FG72/PDF73, FG125/PDF126은 DATA27.05.2024 및 개정란 공란. FG141/PDF142는 DATA27.05.2024, Rev2 17.03.2025. 파일명 Rev2를 전 페이지에 일괄 부여하지 않는다.
- Electrical_Can_Decoating_20241118.pdf: PDF24 CANDC-CONS-E007-024 D-PAGE7 ROTARY ROUTE CONDUIT PIPING(1); PDF25 CANDC-CONS-E008-025 D-PAGE8 같은 제목(2); PDF55 CANDC-CONS-C005-055 D-PAGE5 CABLE SCHEDULE(4). 세 페이지 모두 개정1 24.11.11 first draft design. 승인 시공/as-built 근거로 승격하지 않는다.

기존 CYL-CL07.html은 직접 I/O·내부·HMI·래더0으로 미식별 상태다. 이는 별칭/부모 공유신호까지 없다는 의미가 아니다. 과거 시뮬레이션 계획은 역사 자료로만 보존하고 최신 영구 중지 정책을 적용했다.

## 2. I/O·HMI — 부모 연관 적용 / 독립 소유 근거 미확보

아래는 CL07 전용 신호가 아니라 PV02 Gate B/EV05 구동군의 백업 신호다. 원본 XML 경로는 all-in-one/sources/decoded-original/이며 AO는 bit offset이다. 현재 CPU 주소·값·연결 검증과 구분한다.

| 신호 | 백업 주소·형식 | 선언·결속 | 해석/경계 |
|---|---|---|---|
| PV-02 GATE B EV | Q5.5 Bool | 0607 RID84 SAD Output AO45; NID8 UID729 Write | EV05/CL07·08 공유 명령 |
| EV05_Open | I9.6 Bool | 0607 RID140 SAD Input AO78; NID14 UID38 | OEM LS29 Gate B OPEN |
| EV05_Close | I9.7 Bool | 0607 RID142 SAD Input AO79; NID14 UID44 | OEM LS30 Gate B CLOSED |
| Inputs.PV-02 GATE B OPEN/CLOSE | DB13.DBX9.6/9.7 Bool | 0609 RID141/143 AO78/79 BAD86;0608 RID86 TOD13;NID14 UID39/45 | 원시 입력과 다른 DB 처리값 |
| Flag.PV_02_GATE_B_MEM_OPEN/CLOSE | DB2.DBX8.7/8.6 Bool | 0609 RID56/144 AO71/70 BAD5;0608 RID5 TOD2;NID14 UID40/42,46/48 | 위치 기억; 실제 센서값 아님 |
| Open EV B 00 PV-02 | M30.5 Bool | 0607 RID82 Memory AO245;NID8 UID726 | 부모 local 요청 |
| Open EV B 01 PV-02 | M30.1 Bool | 0607 RID62 Memory AO241;NID8 UID727 | 부모 auto 요청 |
| maintenance PV02 | M80.6 Bool | 0607 RID83 Memory AO646;NID8 UID728 | 부모 공유 가지; 작성 경로 미확정 |
| ON | M0.0 Bool | 0607 RID1 Memory AO0;NID8 UID725,NID14 UID36 | 이름이 ON인 메모리, 상수 true 아님 |

hmi_plc_tags.csv 직접 확인: PV_02\GateB_Open DB11,X78.3 ID00077, GateB_Close DB11,X78.4 ID00076, Selector_GateB DB11,X78.6 ID00074, Allarme1 DB11,X78.0 ID00073, Flag DB2,X10.3 ID000A8. 모두 부모 설정이며 CL07 독립 HMI 객체·이벤트·조작신호 근거는 미확보다. 부모 초안 §2.4의 HMI 호출17실인수 미결속 상태를 유지한다. CSV는 현재 통신·화면·쓰기 이벤트의 증거가 아니다.

물리 입력→Inputs Word전달·호출조건은 PV02 초안 §2.3 공통근거(0397 Move43 IW8→DB13.DBW8 및0030 호출 경계)를 참조한다. 이번에 이 공통 전송을 별도 전수검토하지 않았다. raw/DB/기억/실물의 현재값을 같다고 단정하지 않는다.

decoded-original XML695개를 CL07/CL-07/CL_07/CL 07/CYL-CL07 및 한자리7 변형으로 검색한 결과0건이다. 정확한 정규식·파일수는 cl07-xml-search.json에 기록했다. 이름검색 범위의 부재이며 모든 별칭 신호 부재의 증명은 아니다. 검색695건은 의미검토5XML에 합산하지 않는다.

## 3. 제어 구조 — 공유 구동 전달 경계 적용

0283-FlgNet.xml LAD1920, r1 scraps gate 2, 선언 NID8의 B 출력부를 직접 확인했다. network-map은 탐색용이며 실제 조건은 아래 Part/Wire/ORef와0607 선언에 근거한다.

Q5.5 = ON AND (OpenB00 OR OpenB01 OR maintenance PV02).

- Powerrail W762→Contact748.in; W734/ORef725→RID1 ON, out W749→Contact750/752/754.in.
- Contact750.operand W735/ORef726→RID82 M30.5; out W751→OR713.in1.
- Contact752.operand W736/ORef727→RID62 M30.1; out W753→OR713.in2.
- Contact754.operand W737/ORef728→RID83 M80.6; out W755→OR713.in3.
- OR713 Cardinality3.out W738→Coil717.in; operand W740/ORef729→RID84 Q5.5.
- 이 구간 CRef 호출 없음. OFF 네 번째 가지 없음. 별도 CL07 닫힘 출력 코일을 만들지 않는다. Enable·자동허가 해제로 local/maintenance 가지가 반드시 해제된다는 설명도 하지 않는다.

전달은 Q5.5→71KA2→EV05→CL07/08 공유 공압 분기다. Q=1은 밸브 전압·공기 공급·실린더 이동을 증명하지 않으며 Q=0은 CL07 닫힘·무압·안전 위치를 증명하지 않는다.

0289-FlgNet.xml LAD1924/NID14의 Gate B 기억부를 직접 확인했다. 동일 UID라도 NID13(A)과 NID14(B)를 혼용하지 않는다.
- ON: Contact21 operand W50/ORef36 RID1, out W51이22/27/29/34.in으로 간다.
- OPEN Set: Contact22 operand W82/ORef83 RID84(Q), out W53→Contact23/24; raw I9.6은 W54/ORef38 RID140→Contact23, 처리 DB13은 W56/ORef39 RID141→Contact24. out W55/W57→OR25.in1/2; out W58→SCoil26, operand W59/ORef40 RID56 MEM_OPEN.
- OPEN Reset: NOT Contact27 operand W85/ORef86 RID84; out W84→RCoil28, operand W62/ORef42 RID56.
- CLOSE Set: NOT Contact29 operand W87/ORef88 RID84; out W64→Contact30/31. raw I9.7 W65/ORef44 RID142→30, 처리 DB13 W67/ORef45 RID143→31; out W66/W68→OR32.in1/2; W69→SCoil33, operand W70/ORef46 RID144 MEM_CLOSE.
- CLOSE Reset: Contact34 operand W90/ORef91 RID84; out W89→RCoil35, operand W73/ORef48 RID144.

따라서 MEM_OPEN Set는 ON·Q·(raw OR Inputs), Reset은 ON·NOT Q다. MEM_CLOSE Set는 ON·NOT Q·(raw OR Inputs), Reset은 ON·Q다. 기억은 원시 위치와 별개이며 두 입력의 OR도 보존한다. 부모 자동0~5순서·체류 변환·호출/다중쓰기 전체는 기존 PV02 초안 §3 공통참조로 유지한다. 현행 스캔·최종값·물리 안전 판단은 미수행이다.

## 4. 전기·공압 끝점 — 연관 회로 적용

### PLC 제어와 EV 부하를 분리

FG141/PDF142의 CPU515 MOD15 terminal16 A5.5→cross-ref71/6, FG71/PDF72 A5.5→71KA2 A1, A2→−0Vdc10.6을 렌더 확인했다. 모듈 전원은 +24Vdc10.9→X21/3033(5×20 4A F) 경로다. 이 보호기 표기는 도면값이며 현행 설치·승인 교체정격을 확정하지 않는다.

EV05 부하: 110Vac9.7→71KA2 접점5–9→wire71.3→X1/143(5×20 2A F)→wire71.4→EV-05 A1→A2→X1/144→0Vac9.9. 24Vdc 제어코일과110Vac 부하는 다르다. 하단 접점표의1/5/9를 부하1–9로 오독하지 않는다. 기존 PV01 69KA 및 PV02 71KA의5–9 정정을 유지한다. 이 구성품의 관련 경로는71KA2이며69KA는 직접 소유하지 않는다.

### LS 위치 신호

FG72/PDF73 및 FG125/PDF126의 양 끝점을 직접 대조했다.
- OPEN: +24Vdc10.7→X1/149(5×20 2A F)→wire72.3→LS29 13–14→X1/150→E9.6→FG125 CPU515 MOD10 terminal17.
- CLOSE: +24Vdc10.7→X1/151(5×20 2A F)→wire72.4→LS30 13–14→X1/152→E9.7→FG125 CPU515 MOD10 terminal18.

OEM 명칭은 Gate B OPEN/CLOSE다. P&ID 리더가 CL07 도식에 닿는다는 사실은 구분해 기록하되 현장 CL07 독점 감시·정상극성·실물센서 종류는 미확정이다. CL08의 독립 센서번호를 추정하지 않는다.

### 시공 케이블·경로와 상충

Electrical_Can_Decoating_20241118.pdf PDF55:

| Cable No. / 전체 ID | FROM→TO | 사양 |
|---|---|---|
| 5_9 =ROT+PV02-LS29A | UC-01 ROT1TB1→PV-02 LS-29 | DC CVV2C 1.0, spare0 |
| 5_10 =ROT+PV02-LS30A | UC-01 ROT1TB1→PV-02 LS-30 | DC CVV2C 1.0, spare0 |
| 5_13 =ROT+PV02-EV05A | UC-01 ROT1TB1→PV-02 EV-05 | AC CVV3G 1.0, spare0 |

PDF25 ROTARY SIDE02의 분기8/9/10은 각각 LS29/LS30/EV05이며 Cable No.5_9/5_10/5_13 및 전체 ID가 PDF55와 일치한다. PDF24의 공통 ROT1TB1 conduit 표에도 동일 B 측 ID들이 있다. 이것은 conduit/케이블 근거이며 OEM X1/143~152와 ROT1TB1의 개별 단자·심선 결속은 확보하지 못했다.

공통 상충은 보존한다: PDF24 ROT1TB1A CORE26 vs PDF55 25G. PDF24 Gate A LS25/26의 짧은 Cable No.5_3/5_4 vs PDF55 5_4/5_5는 CL05 공통정정 색인과 일치하는 범위로 남기되 CL07의 B측 일치와 섞지 않는다. PDF55의 추가 LS27/28 및 LS31/32 행을 CL07/08의 새 위치센서로 임의 배정하지 않는다. 공압 EV05 포트번호·튜브·CL07 양 챔버·기계 링크 끝점은 이 전기 자료에 없으며 확보 필요다.

## 5. 알람·복구 — 부모 참조 적용 / 독립 근거 미확보

CL07 고유 알람·타이머·복구 시퀀스 선언은 확보하지 못했다. 부모 PV02 초안 §5의 Gate B 열림/닫힘 감시7초·알람 유지/Reset(0451 NID44 및0656~0658 선언)은 부모 기능으로 참조만 한다. CL07 독립7초 알람으로 복제하지 않는다. 해당 부모 알람 원본 전체는 이번 의미검토 범위에 포함하지 않았다.

Gate B 알람은 CL07 자체 고장 확정이 아니다. EV05·71KA2·공압 공급·CL08/공동 게이트 기구·LS29/30·raw/Inputs/기억을 나누어 관찰해야 한다. PLC 알람 Reset은 실린더 기계 복구·안전 위치·정상 운전 증거가 아니다. 강제출력·인터록 우회·타이머 연장·반복 Reset 지시를 만들지 않는다.

## 6. 증상별 관찰 — 적용 / 실제 정비·운전 미수행

승인된 현장 점검에서 받을 관찰자료 목록이다. 전기 격리·잔압·중력/끼임 위험 통제와 자격자의 승인 절차가 선행되어야 한다. 본 초안은 통전·운전·접근 허가가 아니다.

| 증상 | 관찰·비교 | 오판 방지 |
|---|---|---|
| CL07 동작 없음 | local/auto/M80.6, Q5.5, 71KA2 A1/A2·접점5–9, EV05 전압/공급, 공압 분기의 동일시각 관찰 | 출력1을 실물 이동완료와 같게 보지 않음 |
| CL07·CL08 이동 차이 | 각 실물 표찰/로드·기계 링크·공압 튜브·실제 위치 비교 | 공유 EV 하나로 두 실린더 동기성 단정 금지 |
| 이동했는데 Gate B 알람 | LS29/30→I9.6/9.7→DB13→DB2 기억→부모 알람 기록 | CL07만 보고 공동 Gate B/CL08 복구 판정 금지 |
| HMI와 실제 위치 불일치 | HMI DB11 설정과 raw/DB13/MEM 및 비접촉 실제 위치의 시각 일치 | HMI CSV는 현행 화면 이벤트/온라인값 증거 아님 |
| 출력0 뒤 위치·잔압 불명 | 승인 공압 회로·스풀/복귀·잔압 자료 및 실제 위치 관찰 | Q0을 닫힘·무압·접근 안전으로 바꾸지 않음 |

관찰 필드: 관찰자, 시각/시간대, CL07/08 표찰·위치, 장비/현재 프로젝트 식별, 신호명·값·단위, 수집장치, 비교 도면·단자·사진, 원인 배제 결과, 승인된 조치, 복구 확인자와 증거. 실제 운영기록·사진·SEJIN 데이터는 생성/복제하지 않았다.

## 7. 완료·누락 — 초안 완료와 현장 확인 분리

| 상태 | 결과 |
|---|---|
| documentation | complete_with_gaps:7영역, 직접 근거·소유·상충·누락 명시 |
| static_review | 선정22파일 SHA/Gitblob, XML5개·CSV1개·PDF3파일8페이지의 지정 의미검토 완료; 부모 독립검토 대기 |
| ui_records | not_run: 도면/래더 비교·선택복원·전후기록·보고서/PDF 네 기능의 구현/저장/재열기 검증 안 함 |
| publication | not_published: CL07 초안 게시 없음; 기존 PV02 게시 상태 상속 안 함 |
| tia_compile / live_cpu / field_recovery | not_performed |

필요 자료와 판정 조건:
1. CL07 표찰/명판·설치도 및 Gate B·CL08 기계 링크. 원본 태그와 실제 위치 일치 확인 전 physical_identity_verified를 변경하지 않는다.
2. EV05 형식/포트·스풀·복귀·튜브 양 끝점과 CL07 보어·스트로크·고정방식. 압력·유량·정비주기·토크·안전위치는 승인 제조사 자료 없이는 채우지 않는다.
3. OEM X1↔ROT1TB1 개별 심선/단자표 및 CORE26/25G 해소된 승인 개정. 현행 보호기·정상극성·배선 검증 필요.
4. 현재 CPU 프로젝트·호출/다른쓰기, HMI17 미결속 실인수·실제 이벤트·통신 및 관찰 기록. 백업 정적 구조로 현행 상태를 대신하지 않는다.
5. CL07/08 위치와 부모 Gate B 알람/신호를 동시 기록한 복구 증거. 문서검사만으로 복구 완료 판정하지 않는다.

다음 조치: 부모 검토자가 CL07 고유 P&ID 리더·EV05 공유소유와 선언/전기 끝점을 독립 검토한 뒤 허용된 통합에서 연결한다. 새 자료 없는 미확정 반복 추정은 하지 않는다.

## 부록 A. 검사 범위·산출물

직접 의미검토: XML5개(0283/0289 및0607/0608/0609), CSV1개, PDF3파일8페이지(PID1;OEM72/73/126/142;시공24/25/55). 선언 및 결선 원문은 extracts/CYL-CL07/selected-xml.txt, PDF별 text/png와 PID 상세·제목 확대를 보존했다. 대장·지침·기존 HTML·network-map은 배경/식별/탐색 검토이고 XML695파일 이름검색·SHA검사를 PLC 의미검토 수에 더하지 않는다.

검사 JSON: ../extracts/CYL-CL07/source-integrity.json. 아래 선정 원본22파일 모두 고정 commit Gitblob 바이트와 일치했다. 파일 동등성은 현재 CPU·현장 동일성 검증이 아니다. PV02/CL05 초안 및 batch scope/review는 파생 조사자료로 재사용했으며 고정 Git 원본으로 표시하지 않는다. 독립 리뷰·TIA·앱·시뮬레이터 시험은 수행하지 않았다.

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
| all-in-one/devices/CYL-CL07.html | `6836b5bc24c5ff335a1fad64ea2abecfbc64dbe2ff0dd6cb1ba3e737106a83a2` | `984106acf9daf13f596282230fb87d3ce290015b` | True |
| all-in-one/devices/CLIENT-CL07.html | `5cefd5b797ca137877ccb5d9aea50607dce286423a03a54de5ea84105d75f69b` | `2cb9f7b2fda2368b8fda58a7b79344aa48f5fa8b` | True |
| all-in-one/sources/PID_1684n002I.pdf | `2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b` | `8c83a59fefd5b8b651ec3537ea4236a073f5e109` | True |
| all-in-one/sources/Electrical_Rev2.pdf | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` | `f610fd7c7ce14ae951b00cff57b969259bfb389d` | True |
| all-in-one/sources/Electrical_Can_Decoating_20241118.pdf | `3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd` | `0ee6b6f8361c5790864dbba4bbd9d55e8e7c08f8` | True |
| all-in-one/sources/hmi_plc_tags.csv | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` | `cf4c0650e7c7baac350dcb89909b808435704880` | True |
| all-in-one/sources/decoded-original/network-map.json | `c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60` | `424430b6b953e43138e5d0a18ca40c949e21cfa1` | True |
| all-in-one/sources/decoded-original/0283-FlgNet.xml | `ab46cabcba6cbf8155c47075a66a1573d9f12e01de1f2faccc0eb8ed2cb69cc3` | `996699492035dd8f7ab7e9fbaa0e0033b4cf7407` | True |
| all-in-one/sources/decoded-original/0289-FlgNet.xml | `5460dc0d52bafeeaee0cfd2d66476f7df582002f05a6a17fb4a0928b7e750165` | `fbacf4172f1e1383998a6af80388ecc96c24572b` | True |
| all-in-one/sources/decoded-original/0607-IdentXmlPart.xml | `9b76b53536a26e7b45961fecbf825ae1552e16c2fd9af5736864193c01d77f93` | `dbd4da513171f04cca9b1c1741d0293c3e38f98c` | True |
| all-in-one/sources/decoded-original/0608-IdentXmlPart.xml | `24adec2035b65c0c310d637bcea74374896875b6465a16aa2f2cfc8fd55fa4b8` | `cea8f4160d2da00023b1ecc5e591b561e4a08330` | True |
| all-in-one/sources/decoded-original/0609-IdentXmlPart.xml | `395de8ebb2168848cf96fe015bd7334d71107c114a4e441ef36346b8f22031db` | `ee2aab34c0116642dd9f4364b236426f78a876a3` | True |

정적 재대조: 지정 Wire 연결11개를 XML 구조로 재확인(11/11), 7영역 제목·해시표22행 확인. static-checks.json 참조. 정적 연결 검사는 행동시험·실행모델이 아니다.
