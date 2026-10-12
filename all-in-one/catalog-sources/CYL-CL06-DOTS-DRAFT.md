# CYL-CL06 고유 구성품 조사 초안

- 대상: CYL-CL06 공압 실린더, 부모 PV02, phase2 / parent_child_separate. 조사일 2026-10-11 UTC.
- 기준: GME-STD-1.0.0, source-mv06 고정 commit abcf31c5030bc7ef8749ed8e869a857f2387a28a, VERSION 1.12.0. 실제 실행 모델·추론 설정은 관측 미확인.
- 범위: 이 MD와 extracts/CYL-CL06만 작성. 원본·공통코드·대장·버전·배포·운영·PLC·현장·보호값·SEJIN 변경 없음. 생성기·앱빌드·시뮬레이터 작성/수정/생성/실행/행동시험 없음.
- PV02 및 CYL-CL05 초안은 탐색색인/부모 공통근거로 재사용했다. 부모 전체를 반복 조사하지 않고 CL06 고유 공압 분기, 리더 유무, 관련 Gate A 끝점 및 지정 선언/핀을 직접 대조했다. 부모 완료 상태를 상속하지 않는다.

## 1. 설비·자료 기준 — 적용

INVENTORY.json catalog[206]는 CYL-CL06을 component, parent_id PV02, depth 1, baseline/not_assessed로 분류한다. GME-CATALOG-OVERLAP-REVIEW.json 동일 ID는 parent_child_separate, physical_identity_verified=false이다. 같은 번호의 CLIENT-CL06은 별도의 Belt conveyor B 외부 연동 행이며 그 모터 출력·알람을 실린더에 가져오지 않는다.

PID_1684n002I.pdf 실제 PDF1의 PV-02 Detail을 직접 회전 확대했다. EV-04 뒤 공압선이 CL-05와 CL-06 두 도식으로 갈라진다. CL-06은 이 도식에서 CL-05 아래, CL-07 위에 위치한다. LS-26 및 LS-25 리더는 CL-05 도식에 닿으며 CL-06에는 별도 위치센서 리더가 그려져 있지 않다. 따라서 EV04 공유 구동군이라는 문서상 관계를 확정하되 CL06 전용 코일이나 LS25/26의 CL06 독점 소유는 확정하지 않는다. EV05→CL07/08과 구분한다. 오른쪽 Gate A/B 기계 그림과 OEM EV04=Gate A 명칭은 연관 근거이나 두 실린더의 실제 부착 위치·링크·동기성·로드 방향을 증명하지 않는다.

| 원본 | 직접 확인 페이지·개정 | 해석 경계 |
|---|---|---|
| PID_1684n002I.pdf | 실제 PDF1, 도면1684n002 Apex I, 기본06/04/2011, 변경란 I 15/01/2013, FG ‘−’ | 구형 P&ID; 현행 실물 동일성 아님 |
| Electrical_Rev2.pdf | PDF72/FG71,73/FG72,126/FG125: DATA27.05.2024, 페이지 개정란 공란 | 파일명 Rev2를 모든 페이지 개정으로 전파하지 않음 |
| Electrical_Rev2.pdf | PDF142/FG141: DATA27.05.2024, 개정2 17.03.2025 | 백업 전기 경로이며 현재 설치 확인 아님 |
| Electrical_Can_Decoating_20241118.pdf | PDF24/64, CANDC-CONS-E007-024, D-PAGE7, ROTARY ROUTE CONDUIT PIPING(1) | 변경1 24.11.11 first draft design |
| 같은 시공 PDF | PDF55/64, CANDC-CONS-C005-055, D-PAGE5, CABLE SCHEDULE(4) | 변경1 24.11.11 first draft design; 승인 시공도로 승격 금지 |

기존 devices/CYL-CL06.html의 물리 I/O·내부·HMI·래더 0은 직접 태그 미식별 기록이다. 실제 독립 신호의 부재 증명은 아니다. 기존 시뮬레이션 계획은 역사 자료로 보존하고 최신 영구 중지 지침을 적용한다. 실린더 제조사·형식·보어·스트로크·포트·압력·토크·교환주기는 자료 미확보다.

## 2. I/O·HMI — 부모 연관 적용, CL06 독립 근거 미확보

아래 주소는 백업 선언이며 현재 CPU 값이 아니다. XML 약기 경로는 all-in-one/sources/decoded-original/이다. AO는 비트 오프셋이다.

| 부모 Gate A 신호 | 백업 주소/형식 | 원본 선언·참조 | CL06 소유 한계 |
|---|---|---|---|
| PV-02 GATE A EV | Q5.4 Bool | 0607 RID85, SAD Output AO44, NID8 UID733 Write | EV04→CL05/06 공통 명령 |
| EV04_Open / Close | I9.4 / I9.5 Bool | 0607 RID135/137, Input AO76/77, NID13 UID38/44 | LS25/26의 Gate A 응답, CL06 독립 검출 아님 |
| Inputs.PV-02 EV A OPEN / CLOSE | DB13.DBX9.4/9.5 Bool | 0609 RID136/138 AO76/77 BAD86;0608 RID86 TOD13;NID13 UID39/45 | raw와 구별되는 처리 변수 |
| Flag.PV_02_GATE_A_MEM_OPEN / CLOSE | DB2.DBX8.5/8.4 Bool | 0609 RID55/139 AO69/68 BAD5;0608 RID5 TOD2;NID13 UID40/42,46/48 | 부모 기억 상태, 센서가 아님 |
| Open EV A 00 PV-02 / Open EV A 01 PV-02 | M30.4 / M30.3 Bool | 0607 RID80/61 Memory AO244/243, NID8 UID730/731 | local / auto 요청 |
| maintenance PV02 | M80.6 Bool | 0607 RID83 Memory AO646,NID8 UID732 | 부모 공통 가지; 쓰기 전체 재조사 안 함 |
| ON | M0.0 Bool | 0607 RID1 Memory AO0,NID8 UID725,NID13 UID36 | 이름이 ON인 변수; 상수 true로 취급 금지 |

hmi_plc_tags.csv의 PV_02\\GateA_Open DB11,X78.1(000A6), GateA_Close DB11,X78.2(000A5), Allarme1 DB11,X78.0(00073), Flag DB2,X10.3(000A8)은 부모 설정이다. CL06 독립 태그·조작 객체·이벤트는 확보하지 못했다. CSV는 HMI 이벤트나 현재 통신·쓰기의 증명이 아니며 PV02 초안의 HMI 실인수17 미결속 경계를 유지한다.

decoded-original XML695개에서 CL06/CL-06/CL_06/CL 06 및 한 자리6 변형을 정적 이름 검색하여 0건이었다. 정규식·파일수는 cl06-xml-search.json에 있다. 별칭 신호까지 부재라는 뜻이 아니며 검색수695를 의미검토695로 집계하지 않는다.

## 3. 제어 구조 — EV04 공유 전달 적용

0283-FlgNet.xml LAD1920, block r1 scraps gate 2, 선언 NID8의 A 출력부를 직접 확인했다. index_order10과 NID8은 다르다.

Q5.4 = ON AND (local M30.4 OR auto M30.3 OR maintenance M80.6).

| 원본 Part·Wire·핀 | 결속·해석 |
|---|---|
| Part748 Contact operand W734/ORef725→RID1 | ON 공통 직렬; out W749→Part756/758/760.in |
| Part756 operand W741/ORef730→RID80; out W757→OR720.in1 | local 요청 |
| Part758 operand W742/ORef731→RID61; out W759→OR720.in2 | auto 요청 |
| Part760 operand W743/ORef732→RID83; out W761→OR720.in3 | maintenance 요청 |
| OR720 Card3.out W744→Coil724.in; operand W746/ORef733→RID85 | EV04 출력 Q5.4, CL06 단독 출력 아님 |

이 구간은 CRef 호출 없이 ORef로 연결되며 OFF 네 번째 가지가 없다. Enable 해제만으로 local/maintenance 요청이 해제된다고 설명하지 않는다. 부모 자동 상태기계/모든 호출·다중쓰기는 이번 재조사 범위가 아니며 PV02 초안 §3을 참조한다.

0288-FlgNet.xml LAD1923/NID13의 Gate A 기억부:
- Part21(ON) out W51에서 모든 Set/Reset 가지로 분기한다. OPEN Set: Part22 Q(operand W52/ORef37)→W53→Part23 raw(operand W54/ORef38)와 Part24 Inputs(operand W56/ORef39). W55/W57→OR25.in1/in2; W58→SCoil26; operand W59/ORef40→RID55.
- OPEN Reset: Part27 NOT Q(operand W60/ORef41) out W61→RCoil28, operand W62/ORef42→RID55.
- CLOSE Set: Part29 NOT Q(operand W63/ORef43) out W64→Part30/31.in. Part30 raw operand W65/ORef44→RID137; out W66→OR32.in1. Part31 Inputs operand W67/ORef45→RID138; out W68→OR32.in2. OR32.out W69→SCoil33; operand W70/ORef46→RID139.
- CLOSE Reset: Part34 Q(operand W71/ORef47) out W72→RCoil35; operand W73/ORef48→RID139.

OPEN Set는 ON·Q·(raw OR Inputs), Reset은 ON·NOT Q이다. CLOSE Set는 ON·NOT Q·(raw OR Inputs), Reset은 ON·Q이다. ON 직렬 조건을 생략하지 않는다. 기억비트와 원시입력, 실제 CL06 위치는 별도 관찰 대상이다. Q=0을 CL06 닫힘/무압/접근 안전으로 판정할 자료는 없다.

공통 색인 정정 메모: CYL-CL05 초안의 CLOSE Part30/31 operand Wire 서술(W64/W66)은 실제 원본 W65/W67과 다르다. 이 초안은 원본을 따르며 타 초안은 수정하지 않았다. 이는 논리식 변경이 아닌 핀 위치 표기 정정 사항이다.

## 4. 전기·공압 끝점 — 부모 연관 회로 적용

직접 렌더 확인:
- FG141/PDF142: CPU515 MOD15 terminal15 A5.4→FG71/3. 공통 모듈 +24Vdc10.9→X21/3033 5×20 4A F 전원 경로가 표시된다.
- FG71/PDF72: A5.4→71KA1 코일 A1, A2→−0Vdc10.6. 이는 24Vdc 제어부이다.
- 같은 FG71 EV04 부하: 110Vac9.7→71KA1 접점5–9→wire71.1→X1/141(5×20 2A F)→wire71.2→EV-04 A1→A2→X1/142→0Vac9.9. 하단 접점표1/5/9를 부하1–9로 오독하지 않는다. 기존 69KA/71KA 부하5–9 정정 유지.
- P&ID PDF1: EV04 뒤 공압 분기→CL05 및 CL06. 공압 포트/튜브 번호와 CL06 양 챔버 연결, 복귀 방식·스풀·잔압은 미확보다. 전기 끝점 EV04 뒤를 추정 튜브 번호로 완성하지 않는다.

부모 Gate A 위치 응답 경로:
- FG72/PDF73: +24Vdc10.7→X1/145(2A F)→wire72.1→LS25 접점13–14→X1/146→E9.4→FG125/PDF126 CPU515 MOD10 terminal15.
- CLOSE: +24Vdc10.7→X1/147(2A F)→wire72.2→LS26 접점13–14→X1/148→E9.5→FG125 terminal16.
- OEM 명칭은 Gate A OPEN/CLOSE다. P&ID 리더가 CL05에 위치하므로 이 입력만으로 CL06의 독립 스트로크 도달을 입증하지 않는다. 정상 극성·안전 등급·현재 설치 및 보호정격은 미확정이다.

시공 PDF55: 5_8 =ROT+PV02-EV04A, UC-01 ROT1TB1→PV-02 EV-04, AC CVV 3G 1.0 spare0. 관련 Gate A 피드백 5_4 =ROT+PV02-LS25A 및 5_5 =ROT+PV02-LS26A는 같은 출발점→LS25/26, DC CVV 2C 1.0 spare0다. PDF24 도식 분기5/6/7은 LS25/LS26/EV04이다.

상충 보존: PDF24의 LS25/26 짧은 No.는5_3/5_4, PDF55는5_4/5_5다. 전체 케이블 ID와 FROM/TO를 함께 대조한다. 공통 ROT1TB1A는 PDF24 CORE26 대 PDF55 25G가 상충한다. PDF55에 LS27/28 행이 있어도 CL06 전용 센서라는 근거가 없으므로 배정하지 않는다. OEM X1/141~148와 ROT1TB1 개별 단자·심선 매핑 및 CL06 공압 튜브는 미확보 상태로 둔다.

## 5. 알람·복구 — 부모 참조 적용, CL06 독립 근거 미확보

CL06 전용 알람·전용 타이머·복구 시퀀스 선언을 확보하지 못했다. PV02 Gate A 열림/닫힘 위치 기억 감시는 부모 기능이다. PV02 초안 §5의 0451/NID44 및 0656~0658 선언·7초 감시·Reset 설명은 공통근거로만 참조한다. 이번 XML 의미검토5파일에 부모 알람 파일을 포함하지 않았으며 CL06 독립7초 알람을 만들지 않는다.

Gate A 알람만으로 CL06 고장을 확정할 수 없다. EV04 전기, 공유 공압 공급, CL05/06 기구, LS25/26→raw→Inputs→MEM과 실제 CL06 이동을 분리한다. 부모 Reset은 실물 복구·안전 위치 확보와 다르다. 출력 강제, 접점 우회, 타이머 연장, 반복 Reset 처방을 하지 않는다.

## 6. 증상별 관찰 — 적용, 현장 수리 미수행

다음은 자격자·현장 승인 절차 아래 수집할 자료 목록이다. 전기 격리·잔압 및 중력/끼임 위험 통제가 선행되어야 하며 통전·접근·운전 지시가 아니다.

| 증상 | 관찰·비교할 지점 | 배제 근거와 필요한 자료 |
|---|---|---|
| CL06만 움직이지 않음 | 같은 시각 CL05/CL06 실제 위치와 공유 Q5.4/EV04 상태 | CL05 이동은 CL06 튜브·기구 정상 증명 아님; 현행 튜브·명판·링크 도면 |
| 두 실린더 모두 미동작 | local/auto/M80.6→Q5.4→71KA1→EV04→공급 분기 | PLC 명령, 코일전원, 공압, 기계 동작을 분리; 승인된 측정자료 필요 |
| Gate A OPEN 표시이나 CL06 위치 불명 | I9.4/9.5, DB13, DB2 기억, 실물 위치의 동일시각 기록 | CL05에 그린 센서와 부모 기억을 CL06 스트로크 완료로 치환 금지 |
| CL05/06 이동차 또는 기구 걸림 의심 | 각 로드/링크·튜브 식별·비접촉 위치자료 | 공동 EV04만으로 동기 동작 보장 금지; 승인 기계 기준 필요 |
| 출력 OFF 후 위치·잔압 불명 | Q/EV04 상태, 승인된 공압 회로·복귀 방식·위치 관찰 | Q0=닫힘/무압/안전 아님 |

기록 필드: 관찰자·시각/시간대·CL06 및 CL05 표찰 위치·프로젝트/원본판본·신호명/값/단위·수집장치·증거사진 참조·양 끝점 비교·배제 결과·승인 조치·복구 확인자. 실제 사용자 운영기록이나 사진을 생성·복제하지 않았다.

## 7. 완료·누락 — 초안 complete_with_gaps

| 상태 | 판정 |
|---|---|
| documentation | 7영역 초안 complete_with_gaps; 고유 P&ID·부모 전달·상충·누락 명시 |
| static_review | 지정 XML5파일, PDF3파일의7페이지 및 HMI CSV 대조; 독립검토는 부모 대기 |
| ui_records | not_run. 도면·래더 비교/백업·선택 복원/기록 전후 비교/보고서·PDF 네 기능은 구현 및 실제 저장·재열기 미검증 |
| publication | not_published; 기존 PV02 결과 상속하지 않음 |
| tia_compile / live_cpu / field_recovery | 모두 not_performed |

필요 자료와 종료 경계:
1. CL06 명판/표찰·실제 설치도·Gate A 및 CL05와 기계 연결. 현장 대조 전 physical_identity_verified는 false 유지.
2. EV04 포트·스풀·복귀 형식 및 튜브 양 끝점, CL06 모델/보어/스트로크·부착. 안전 위치·압력·유량·정비주기는 승인 제조사 자료 없이는 채우지 않음.
3. OEM↔ROT1TB1 현행 단자/심선표, Cable No./CORE 상충을 해소하는 개정 자료. 현재 보호기/극성/배선은 별도 현장 확인.
4. 현행 CPU 프로젝트·호출·다중쓰기와 HMI 이벤트/실인수. 이름 검색0을 전체 PLC 부재 증명으로 바꾸지 않음.
5. CL06의 실제 위치와 부모 Gate A 알람/센서 상태의 동시 관찰 및 승인 복구 증거. 부모 센서가 정상이어도 CL06 완료 자동 판정 금지.

다음 한 작업: 부모 검토자가 이 CL06 초안의 고유 공압 분기·리더 부재·핀/끝점과 해시를 독립 대조한다. 새 현장 자료 없이는 미확정을 반복 추정하지 않는다. 원본 변경이나 완료 커밋 생성은 하지 않았다.

## 부록 A. 검사 범위와 원본 무결성

직접 의미검토: XML5파일(0283/0288/0607/0608/0609)의 지정 네트워크·선언, PDF3파일의7페이지(PID1;OEM72/73/126/142;시공24/55), HMI CSV1파일의 지정 부모행. 대장·기존페이지·지침·network-map은 배경/색인으로 구분한다. XML695개 이름 검색과 해시파일 수는 의미검토 수에 합산하지 않는다. 실제 PDF7페이지 렌더 및 PID 상세/제목 확대2개는 extracts/CYL-CL06에 보관했다.

selected-xml.txt는 직접 원본 추출, cl06-xml-search.json은 이름검색, source-integrity.json은 선정 원본 전체 SHA256·고정 Gitblob 비교다. 기존 PV02/CYL-CL05 초안과 배정/중복 검토 JSON은 파생 연구자료이며 고정 Gitblob 원본으로 위장하지 않는다.

선정 해시 검사 22파일, 고정 Gitblob 바이트 일치 22/22. 원본 Git 변경 0. CPU/현장 동일성 검증 아님.

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
| all-in-one/devices/CYL-CL06.html | `a13f51e042a3fe9d09d9f481a3d54fe0e8e7704066e16e4fb6907a6c6d7dbdd6` | `53b0bb2de321a8c864b8d314be67dd4aa7641066` | True |
| all-in-one/devices/CLIENT-CL06.html | `d027c71f93ddeaf61de2d7a521cc6e07fa7c1efb608872d4b0c57d86157b5445` | `800132ffa8a9949ff07dbbceef1c707047775f93` | True |
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

실행 검사는 자체 PDF 렌더/정적 XML 발췌/이름검색/해시·Gitblob 비교뿐이다. 각 명령 종료0. 원본 생성기·앱빌드·시뮬레이터·행동시험·업로드·외부 작업 생성은 수행하지 않았다.
