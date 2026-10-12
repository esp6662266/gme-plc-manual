# CYL-CL08 고유 구성품 조사 초안

- 대상: CYL-CL08 공압 실린더 한 개, 부모 PV02, phase2, parent_child_separate.
- 기준: GME-STD-1.0.0 / source-mv06 고정 commit abcf31c5030bc7ef8749ed8e869a857f2387a28a / VERSION v1.12.0.
- 조사일: 2026-10-11 UTC. 실제 실행 모델·추론 설정은 관측 미확인.
- PV02 및 CYL-CL05 초안은 공통 탐색색인으로만 재사용했다. CL08 P&ID 공압 분기, 리더 위치, Gate B 출력·기억 선언과 관련 전기 끝점은 원본으로 직접 확인했다. 부모 완료·게시 상태를 상속하지 않는다.
- 쓰기: 본 초안과 extracts/CYL-CL08만. 원본/공통코드/버전/대장/배포/운영/PLC/보호값/SEJIN 변경 없음. 시뮬레이터 작성·수정·생성·실행·행동시험 및 원본 생성기·앱빌드 실행 없음.

## 1. 설비·자료 기준 — 적용

INVENTORY.json catalog[208]는 CYL-CL08을 component, parent_id=PV02, depth1, baseline/not_assessed로 둔다. 중복 검토 GME-CATALOG-OVERLAP-REVIEW.json catalog_rows의 해당 행도 parent_child_separate, physical_identity_verified=false다. 이름이 같은 공압 실린더들을 병합하지 않는다. CLIENT-CL08은 부모 없는 Shredder vibration feeder/client이며 CYL-CL08과 별개다. 기존 devices/CYL-CL08.html의 직접 I/O·내부·HMI·래더 각0은 이름 기반 미식별 상태이지 물리적으로 제어가 없다는 증거가 아니다. 기존 시뮬레이션 문구는 역사 자료로 보존하고 최신 영구 중지 지침을 적용한다.

### 고유 P&ID 근거

all-in-one/sources/PID_1684n002I.pdf 실제 PDF1의 PV-02 Detail을 회전·확대하여 확인했다(자체 pid-detail.png).

- COMPRESSED AIR 공통선에서 EV04와 EV05가 분리된다. EV05 뒤의 두 선이 CL07 및 아래 CL08 실린더 도식으로 분기한다. CL08은 EV05 공유 구동군이며 독립 EV08이나 별도 PLC 출력을 뜻하지 않는다.
- LS30/LS29 리더는 CL07 도식의 좌·우 위치에 닿는다. CL08 도식에는 같은 리더가 직접 닿지 않는다. 따라서 Gate B 피드백을 CL08 독립 리미트라고 재배정하지 않는다.
- 오른쪽 기계 그림은 위 Gate “A”, 아래 Gate “B”를 표시한다. OEM 전기도면의 EV05=OPENING GATE “B”와 교차하여 부모 Gate B 구동군을 연결한다. CL07/08의 실물 설치방향·동기성·로드와 링크 관계는 현장 표찰/설치도 없이 확정하지 않는다.
- EV05의 포트번호·스풀/복귀·튜브 양 끝점, CL08 보어·스트로크·제조사·모델은 확보하지 못했다. 단순 기호로 정상 극성·안전 위치·잔압 소거를 선언하지 않는다.

### 자료 판본과 실제 페이지

| 원본 | 실제 PDF/도면 | 판본·개정 및 한계 |
|---|---|---|
| PID_1684n002I.pdf | PDF1, drawing1684n002, FG ‘−’ | 기본06/04/2011, Apex I, 변경란 I15/01/2013; pid-title.png 확인 |
| Electrical_Rev2.pdf | PDF72=FG71, PDF73=FG72, PDF126=FG125 | DATA27.05.2024, 각 페이지 변경란 공란 |
| Electrical_Rev2.pdf | PDF142=FG141 | DATA27.05.2024, 개정2/17.03.2025; 파일명 Rev2를 다른 페이지에 전파하지 않음 |
| Electrical_Can_Decoating_20241118.pdf | PDF24/64 CANDC-CONS-E007-024 D-PAGE7 | ROTARY ROUTE CONDUIT PIPING(1), No.1 24.11.11 first draft design |
| 같은 시공자료 | PDF25/64 CANDC-CONS-E008-025 D-PAGE8 | ROTARY ROUTE CONDUIT PIPING(2), No.1 24.11.11 first draft design |
| 같은 시공자료 | PDF55/64 CANDC-CONS-C005-055 D-PAGE5 | CABLE SCHEDULE(4), No.1 24.11.11 first draft design |

시공자료의 초안을 승인 준공도나 현행 설치상태로 승격하지 않는다.

## 2. I/O·HMI — 부모 연관 적용 / CL08 독립 소유 근거 미확보

XML 경로 약기는 all-in-one/sources/decoded-original/이다. 아래 모두 Bool이며 AO는 비트 오프셋이다. 부모 Gate B 신호를 CL08 단독 신호로 복제하지 않는다.

| 신호 | 백업 주소 | 원본 선언·결속 | 해석 경계 |
|---|---|---|---|
| PV-02 GATE B EV | Q5.5 | 0607 RID84 SAD Output AO45, NID8 UID729 Write | EV05→CL07/08 공유 구동 |
| EV05_Open / EV05_Close | I9.6 / I9.7 | 0607 RID140/142 SAD Input AO78/79, NID14 UID38/44 | OEM LS29/30 Gate B 피드백 |
| Inputs.PV-02 GATE B OPEN/CLOSE | DB13.DBX9.6/9.7 | 0609 RID141/143 AO78/79 BAD86;0608 RID86 Inputs TOD13, NID14 UID39/45 | 처리 변수, raw와 구분 |
| Flag.PV_02_GATE_B_MEM_OPEN/CLOSE | DB2.DBX8.7/8.6 | 0609 RID56/144 AO71/70 BAD5;0608 RID5 Flag TOD2;NID14 UID40/42 및46/48 | 방향별 기억, 기계 위치 아님 |
| Open EV B 00 PV-02 | M30.5 | 0607 RID82 Memory AO245, NID8 UID726 | 부모 local 요청 |
| Open EV B 01 PV-02 | M30.1 | 0607 RID62 Memory AO241, NID8 UID727 | 부모 auto 요청 |
| maintenance PV02 | M80.6 | 0607 RID83 Memory AO646, NID8 UID728 | 공통 가지, 작성 경로 미확정 |
| ON | M0.0 | 0607 RID1 Memory AO0, NID8 UID725/NID14 UID36 | 이름 ON인 메모리, 상수 true 아님 |

hmi_plc_tags.csv 행714/715/718은 PV_02\GateB_Open DB11,X78.3(00077), GateB_Close DB11,X78.4(00076), Allarme1 DB11,X78.0(00073)이다. 이 설정은 부모 표시 후보이며 CL08 독립 HMI 객체·이벤트·쓰기 경로의 근거가 아니다. 부모 PV02 초안 §2.4의 HMI 호출17실인수 미결속 경계도 유지한다. 현재 HMI 통신/PLC 프로젝트 일치는 미확정이다.

독립 이름 검색: decoded-original XML695개를 CL08/CL-08/CL_08/CL 08 및 CYL 접두어 패턴으로 정적 검색한 결과0건(cl08-xml-search.json). 이름 검색의 부재이며 별칭을 통한 모든 제어·알람의 부재 증명은 아니다. 검색 파일수와 아래 의미 검토 수를 합산하지 않는다.

## 3. 제어 구조 — 공유 출력·기억 전달 적용

0283-FlgNet.xml LAD1920/r1 scraps gate 2/선언 NID8(색인 index_order10과 다름)의 B 경로를 직접 확인했다.

Q5.5 = ON AND (Open EV B 00 OR Open EV B 01 OR maintenance PV02).

- Contact748 operand W734/ORef725→0607 RID1. Contact748.out W749→Contact750/752/754.in.
- Contact750 operand W735/ORef726→RID82, out W751→OR713.in1.
- Contact752 operand W736/ORef727→RID62, out W753→OR713.in2.
- Contact754 operand W737/ORef728→RID83, out W755→OR713.in3.
- OR713(Card3).out W738→Coil717.in; operand W740/ORef729→RID84 Q5.5.
- 이 네트워크에 CRef 호출 및 OFF 네 번째 가지는 없다. 부모 Enable만 해제하면 local/maintenance 가지까지 무조건 꺼진다고 설명하지 않는다. 별도 CL08 닫힘 코일도 만들지 않는다.

물리 전달: Q5.5→71KA2 제어코일→71KA2 부하접점5–9→EV05→CL07/08 공압 분기. Q=1은 EV전압·공기압·CL08 이동 완료 증거가 아니고 Q=0은 닫힘/무압/안전 접근 허가가 아니다.

0289-FlgNet.xml LAD1924/NID14의 Gate B 기억부:

- ON Contact21 operand W50/ORef36→RID1, out W51은22/27/29/34.in으로 공통 전달.
- Q Contact22 operand W82/ORef83→RID84, out W53→Contact23/24.in. Contact23 raw operand W54/ORef38→RID140, out W55→OR25.in1. Contact24 Inputs operand W56/ORef39→RID141, out W57→OR25.in2. OR25.out W58→SCoil26.in, operand W59/ORef40→RID56 MEM_OPEN.
- NOT Q Contact27 operand W85/ORef86→RID84, out W84→RCoil28.in, operand W62/ORef42→RID56.
- NOT Q Contact29 operand W87/ORef88→RID84, out W64→Contact30/31.in. Contact30 raw operand W65/ORef44→RID142, out W66→OR32.in1. Contact31 Inputs operand W67/ORef45→RID143, out W68→OR32.in2. OR32.out W69→SCoil33.in, operand W70/ORef46→RID144 MEM_CLOSE.
- Q Contact34 operand W90/ORef91→RID84, out W89→RCoil35.in, operand W73/ORef48→RID144.

따라서 OPEN Set=ON·Q·(raw OR Inputs), Reset=ON·NOT Q; CLOSE Set=ON·NOT Q·(raw OR Inputs), Reset=ON·Q다. 두 OR는 raw와 처리값의 병렬이며 별도 CL08 센서 두 개가 아니다. 다른 쓰기·시작 초기화·자동 상태기계·원시Word 전달·호출순서는 부모 PV02 초안 §3의 공통 근거를 참조한다. 이 한 구성품 조사에서 부모 전체를 반복 의미검토한 것으로 집계하지 않는다. 현행 호출순서/다중쓰기/CPU 실행 검증은 미수행이다.

## 4. 전기·공압 끝점 — Gate B 연관 회로 적용

### 제어 전원과 부하 전원

실제 PDF142 FG141: CPU515 MOD15 terminal16 A5.5→cross-reference71/6. 모듈 전원은 +24Vdc10.9→X21/3033 5×20 4A F→wire141.1이며 −0Vdc10.6 귀환이 표시된다. PDF72 FG71의 A5.5→71KA2 A1, A2→−0Vdc10.6을 확인했다.

EV05 부하: 110Vac9.7→71KA2 접점5–9→wire71.3→X1/143(5×20 2A F)→wire71.4→EV05 A1; A2→X1/144→0Vac9.9. 24Vdc 코일제어와110Vac 부하는 서로 다른 회로다. 부모 PV02 초기 초안의1/9 문구는 사용하지 않고 후속 정정 및 실제 렌더의5–9를 적용한다. 69KA/71KA 정정5–9를 유지하며 다른 설비의 릴레이를 CL08에 가져오지 않는다. 퓨즈 표기는 도면 정보이며 현행 보호설정·교체 승인값이 아니다.

### Gate B 피드백

PDF73 FG72:
- +24Vdc10.7→X1/149(5×20 2A F)→wire72.3→LS29 13–14→X1/150→E9.6→FG125/PDF126 CPU515 MOD10 terminal17.
- +24Vdc10.7→X1/151(5×20 2A F)→wire72.4→LS30 13–14→X1/152→E9.7→FG125/PDF126 MOD10 terminal18.

OEM 명칭은 GATE “B” OPEN/CLOSE다. P&ID 리더가 CL07에 위치한다는 근거를 함께 보존하고 CL08의 독립 OPEN/CLOSE라고 표현하지 않는다. CL07 측 피드백 하나로 CL08까지 이동 완료라고 판정할 수 없다. 접점 도식은 현행 정상 극성·실제 센서 장착 상태·안전등급을 대신하지 않는다.

### 시공자료·끝점 누락

PDF25 ROTARY SIDE02의 분기8=LS29,9=LS30,10=EV05,11=PB16을 직접 렌더 확인했다. 아래 Cable No.는 PDF25와 PDF55에서 일치한다.

| Cable No. / 전체 ID | PDF55 FROM→TO | 종류·심수·굵기 |
|---|---|---|
| 5_9 / =ROT+PV02-LS29A | UC-01 ROT1TB1→PV-02 LS-29 | DC CVV 2C 1.0 SPARE0 |
| 5_10 / =ROT+PV02-LS30A | UC-01 ROT1TB1→PV-02 LS-30 | DC CVV 2C 1.0 SPARE0 |
| 5_13 / =ROT+PV02-EV05A | UC-01 ROT1TB1→PV-02 EV-05 | AC CVV 3G 1.0 SPARE0 |

PDF24에는 공통 ROT1TB1A CORE26, PDF55에는25G가 있어 상충을 유지한다. PDF24의 LS25/26 짧은 번호5_3/5_4와 PDF55의5_4/5_5도 공통자료 불일치이며 CL08 번호로 고쳐 쓰지 않는다. PDF55의 LS31/32(5_11/5_12)는 추가 가지지만 이번 OEM LS29/30나 P&ID CL08 리미트로 배정할 근거가 없다. 전용 CL08 센서가 추가되었다고 추정하지 않는다.

OEM X1/143~152↔ROT1TB1 개별 단자·심선·분기 접속표는 미확보다. EV05 공압 포트↔CL08 양 챔버/CL07 분기 끝점도 전기 케이블표에서 해결되지 않는다. 최종 설치도·튜브 표찰·현행 단자표를 확보해야 물리 동일성을 확정할 수 있다.

## 5. 알람·복구 — 부모 기능 참조 / 독립 근거 미확보

CL08 고유 알람·전용 타이머·복구 시퀀스 근거는 확보하지 못했다. 부모 PV02 초안 §5의 Gate B 열림/닫힘 감시와7초 설명(0452/NID45,0656~0658 선언)은 부모 공통 자료로만 참조하며 CL08 독립7초 알람으로 복제하지 않는다. 해당 부모 알람 XML 전체는 이번 직접 의미검토 수에 포함하지 않는다.

Gate B 알람은 EV05 공통 전원·릴레이·공기 공급·게이트 링크·CL07/08·피드백/처리/기억 경로를 분리할 출발점이며 CL08 고장의 단독 증거가 아니다. 특히 LS29/30 리더가 CL07에 있는 P&ID 때문에 CL08 움직임과 부모 피드백의 일치를 별도로 관찰해야 한다. 알람 Reset은 기계 복구/안전 위치/재요청 허가와 다르다. 강제출력·접점 우회·타이머 연장·반복 Reset을 처방하지 않는다.

## 6. 증상별 관찰 — 적용, 현장 운전·수리 미수행

자격자 승인·에너지 격리·잔압 및 끼임/중력 위험 통제를 전제로 한 자료 수집 항목이다. 이 문서는 통전·운전·접근 명령이 아니다.

| 증상 | 분리 관찰 위치 | 판정 한계/필요 자료 |
|---|---|---|
| CL08 움직임 없음 | M30.5/M30.1/M80.6→Q5.5→71KA2 A1/A2·5–9→EV05→공압 분기 | Q값은 부하전압/압력/이동 증거 아님. 현행 튜브·스풀자료 필요 |
| CL07과 CL08 움직임 불일치 | 두 실린더 실제 위치·링크·튜브 양 끝점을 같은 시각에 기록 | 공유EV만으로 동기성 단정 금지; CL08 위치를 직접 확인해야 함 |
| Gate B 피드백 정상인데 CL08 위치 불명 | LS29/30, raw I9.6/.7, DB13, DB2 기억과 CL08 실제 위치 분리 | P&ID 리더는 CL07에 있으므로 CL08 완료를 자동 추론하지 않음 |
| 이동은 보이나 부모 알람 지속 | raw/Inputs/MEM, EV 명령, HMI DB11을 같은 시각으로 비교 | 표시·기억은 실물 센서와 다름; 부모 알람을 독립 CL08 고장으로 한정 금지 |
| Q해제 뒤 위치·압력 불명 | Q5.5, EV전원, 승인된 비접촉 위치 관찰 및 공압 도면 비교 | Q0≠닫힘/무압/안전 접근. 복귀형식 자료 필요 |

관찰 필드: 관찰자·시간대 포함 시각·CL07/08 표찰 위치·원본/현재 프로젝트 ID·신호명/값/단위·수집 장치·비교 끝점·사진근거·배제 결과·승인 조치·복구 확인자. 실제 사용자 운영기록·사진·SEJIN 자료를 생성/복제하지 않았다.

## 7. 완료·누락 — 문서 초안, 현장 미확정 유지

| 구분 | 실제 상태 |
|---|---|
| documentation | complete_with_gaps 초안:7영역·CL08 고유 분기·리더·공유 소유·누락 기록 |
| static_review | 선정 원본 SHA/Gitblob 검증 및 XML5개·PDF8페이지·HMI CSV1개 직접 의미검토; 부모 독립검토 대기 |
| ui_records | not_run. 도면·래더 비교/백업·선택복원/전후기록 비교/보고서PDF는 적용 후보이나 구현·저장·재읽기·재열기 검증 없음 |
| publication | not_published. 부모 게시 결과를 상속하지 않음 |
| tia_compile / live_cpu / field_recovery | not_performed |

남은 자료와 완료 조건:
1. CL08 명판·실물 표찰·Gate B 링크/CL07 연계 설치도를 확보해 P&ID 도식과 실제 부품을 대조한다.
2. EV05 포트/스풀/복귀 방식·CL08 양 챔버 튜브·모델/보어/스트로크 자료를 확보한다. 압력/유량/토크/정비주기/안전 위치를 추정하지 않는다.
3. 현재 OEM↔ROT1TB1 단자·심선표와 공통 케이블 상충 개정본을 확보한다. LS31/32의 현행 역할은 별도 근거 필요하다.
4. 현재 CPU 호출/다중쓰기/원시전달 및 HMI 실인수·이벤트를 확인해야 백업의 현행 적용을 판정할 수 있다.
5. CL08 위치를 부모 Gate B 명령·CL07 측 피드백·알람과 동시 비교한 승인 복구 증거가 필요하다. 문서 완료로 현장 완료를 대체하지 않는다.

다음 한 작업: 부모 검토자가 CL08 고유 P&ID 리더 경계, Gate B 선언/핀, 실제 PDF 끝점과 해시를 독립 확인한다. 새 현장 자료 없이는 동일 미확정을 반복 추정하지 않는다.

## 부록 A. 검사 범위와 선정 전체 원본 무결성

직접 의미검토: XML5개(0283/0289/0607/0608/0609), PDF3파일의8페이지(PID1; OEM72/73/126/142; 시공24/25/55), HMI CSV1개. 대장/지침/기존 HTML/색인은 배경·보존 확인이다. PDF렌더8개와PID확대2개를 보관했다. XML695개 이름검색 및 파일 해시 검사 수는 의미검토 수가 아니다. 부모 PV02 전체 알람/상태기계/호출은 탐색 재사용이며 새 전체 의미검토로 주장하지 않는다.

selected-declarations.txt에 SAD/SSD/BAD/TOD·RID/NID 전체 선택 선언을 보존했다. cl08-xml-search.json은 검색 경계, source-integrity.json은 아래 선정 원본 전부의 SHA256 및 고정 Gitblob 바이트 일치 결과다. 파생 초안·범위지침·중복 검토 JSON은 고정 Git 원본으로 위장하지 않는다.

선정 해시검사 22파일, 고정 Gitblob 바이트 일치 22/22. source Git 변경 0. 현장/CPU 동일성 검증은 아니다.

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
| all-in-one/devices/CYL-CL08.html | `272fd5de99cbc7812e5ecf02b86ad01e4d244fdc9fe41045a295281170a4e967` | `0114649ccbc80ac13d5aa9e30f57ad75a5d18d84` | True |
| all-in-one/devices/CLIENT-CL08.html | `bf86e2020d4feaa5eda4baf0049abd0fb3e521e508a61f9b2c4b09f6626b4d1e` | `99d17151e6a944d393ae856c2faded37707c2f67` | True |
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

도구·범위 기록: 최초 source-mv06 상대경로를 저장소 밖에서 조회해 파일없음이 발생했으나 gme-research/source-mv06로 바로잡아 전부 읽었다. 설치·권한 우회·원본 변경 없이 조사했다. 정적 추출/렌더/해시 이외 생성기·시뮬레이터·앱시험·현장 동작검사는 미실행이다.
