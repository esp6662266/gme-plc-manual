# LS30 고유 구성품 조사 초안

- 대상 LS30 / 밸브 위치 리미트 스위치 / component / 부모 PV02 / phase2 / parent_child_separate.
- 기준 GME-STD-1.0.0, source-mv06 고정 커밋 abcf31c5030bc7ef8749ed8e869a857f2387a28a, VERSION v1.12.0. 조사 2026-10-11 UTC. 실제 실행 모델·추론 설정은 관측 미확인.
- 실제 범위는 TASK3-BATCH24-SCOPE.json의 LS30 행을 우선했다. PV02·CYL-CL05~08 초안은 탐색색인/공통근거로 재사용하고 아래 LS30 선언·핀·다른 쓰기·PDF 끝점은 고정 원본으로 직접 확인했다. 부모 전체를 재조사한 결과나 부모 완료의 상속이 아니다.
- 작성 범위는 본 MD와 extracts/LS30뿐이다. 원본·공통코드·대장·버전·배포·PLC·현장·보호값·SEJIN 변경 없음. 시뮬레이터 작성/수정/생성/실행/행동시험, 원본 생성기·앱빌드·재위임·업로드 미실행. 보존된 simulation XML은 다른 DB 쓰기를 확인하기 위한 읽기 전용 정적 분석만 수행했다.

## 1. 설비·자료 기준 — 적용

INVENTORY.json catalog[241]는 LS30을 PV02 하위 component, depth1, baseline/not_assessed로 분류한다. GME-CATALOG-OVERLAP-REVIEW.json 해당 행은 parent_child_separate 및 physical_identity_verified=false다. 별칭 ls-30/ls.30은 문서 검색 별칭이고 다른 LS의 이름·실물을 병합하지 않는다.

PID_1684n002I.pdf 실제 PDF1 PV-02 Detail을 확대해 확인했다. EV05 뒤 공압선은 CL07/CL08로 분기한다. LS30 리더는 CL07 몸체/로드 인접부, LS29 리더는 CL07 로드 측에 닿고 CL08에는 이 리더가 직접 닿지 않는다. 오른쪽 기계 그림은 Gate A/B를 구분한다. OEM 전기도면 PDF73 FG72는 LS30을 LIMIT SWITCH GATE “B” CLOSE, PDF126 FG125는 GATE “B” CLOSED VALVE PV-02로 명시한다. 따라서 문서상 LS30=PV02 Gate B 닫힘 피드백을 연결한다. 리더와 공통 EV만으로 CL07 독점 감시·CL08 실제 위치·두 실린더 동기성·현장 설치방향을 확정하지 않는다.

| 실제 원본/페이지 | 제목·개정 직접 확인 | 경계 |
|---|---|---|
| PID_1684n002I.pdf PDF1 | drawing1684n002, 기본06/04/2011, Apex I, 변경란 I15/01/2013, FG ‘−’ | 과거 P&ID이며 현장 일치 미확인 |
| Electrical_Rev2.pdf PDF73/FG72 | LOAD DRUM CLAPPE VALVE PV-02, DATA27.05.2024, 페이지 변경란 공란 | 파일명 Rev2를 페이지 개정으로 전파하지 않음 |
| 같은 PDF126/FG125 | DIGITAL INPUT MODULE, DATA27.05.2024, 페이지 변경란 공란 | CPU515/MOD10은 도면 표기 |
| Electrical_Can_Decoating_20241118.pdf PDF24 | CANDC-CONS-E007-024, ROTARY ROUTE CONDUIT PIPING(1), D-PAGE7 | No.1 24.11.11 first draft design |
| 같은 PDF25 | CANDC-CONS-E008-025, ROTARY ROUTE CONDUIT PIPING(2), D-PAGE8 | No.1 24.11.11 first draft design |
| 같은 PDF55 | CANDC-CONS-C005-055, CABLE SCHEDULE(4), D-PAGE5 | No.1 24.11.11 first draft design |

시공 PDF 파일 총64페이지와 PDF24/25/55 제목란의 TORAL-PAGE 24/64·25/64·55/64를 구분한다. 초안 도면을 승인 준공도나 현재 시공 결과로 바꾸지 않는다.

## 2. I/O·HMI — 적용

이하 네 자리 XML 약기는 all-in-one/sources/decoded-original/NNNN-FlgNet.xml 또는 NNNN-IdentXmlPart.xml이다. RID는 해당 선언 묶음과 NID/UID를 함께 사용한다. AO는 bit offset이다.

| 계층 | 백업 주소/형식 | 원본 선언·사용 문맥 | 해석 |
|---|---|---|---|
| 원시 LS30 피드백 | EV05_Close I9.7 Bool | 0607 RID142 SAD Input AO79, NID14 UID44 | OEM E9.7과 번호/방향 대조; 전기적 정상극성은 미확정 |
| 가공/전달 DB | Inputs.PV-02 GATE B CLOSE DB13.DBX9.7 Bool | 0609 RID143 AO79 BAD86;0608 RID86 Inputs TOD13;NID14 UID45 | raw와 OR로 소비, 이름만으로 현재 동일값 보장 안 됨 |
| 닫힘 기억 | Flag.PV_02_GATE_B_MEM_CLOSE DB2.DBX8.6 Bool | 0609 RID144 AO70 BAD5;0608 RID5 Flag TOD2;NID14 UID46 Set/48 Reset | 순간 위치나 안전 확인 비트가 아님 |
| 부모 구동 명령 | PV-02 GATE B EV Q5.5 Bool | 0607 RID84 Output AO45;NID14 UID83/86/88/91 | LS30 출력이 아니며 EV05/CL07·08 공유 명령 |
| 공통 조건 | ON M0.0 Bool | 0607 RID1 Memory AO0,NID14 UID36 | 상수 true로 간주 금지 |
| 부모 HMI 닫힘 표시 후보 | PV_02\GateB_Close DB11,X78.4 | hmi_plc_tags.csv 행715,PLC,ID00076 | DB13/DB2/raw와 다른 주소 |
| 부모 HMI 통합 알람 후보 | PV_02\Allarme1 DB11,X78.0 | CSV 행718,ID00073 | 개별 LS30 고장 알람으로 동일시 금지 |

HMI CSV는 dde.cfg 설정이며 실제 현재값이 아니다. 부모 PV02 초안 §2.4의 0392/LAD1216 HMI PV_2Gate 17실인수 미결속 경계를 유지한다. 이번에는 그 호출의 전체 결속을 다시 검토하지 않았으며 LS30 독립 화면 객체·이벤트·쓰기·실제 통신은 미확보다.

## 3. 제어 구조 — 원시·가공·기억·다른 쓰기 적용

### 3.1 LS30가 들어가는 기억 논리

0289 LAD1924, block r1 scraps gate 2, NID14의 CLOSE 가지를 직접 대조했다. CRef 호출은 이 네트워크에 없다.

- W49 powerrail→Contact21.in. W50/ORef36→Contact21.operand=ON. Contact21.out W51→Contact29.in 및 Contact34.in.
- Contact29의 operand는 **반전 Q5.5**: W87/ORef88→0607 RID84. out W64→Contact30/31.in.
- Contact30은 **비반전 raw I9.7**: operand W65/ORef44→0607 RID142, out W66→OR32.in1.
- Contact31은 **비반전 DB13.DBX9.7**: operand W67/ORef45→0609 RID143, out W68→OR32.in2.
- OR32(Card2).out W69→SCoil33.in, operand W70/ORef46→0609 RID144 MEM_CLOSE.
- Reset 가지 Contact34는 비반전 Q5.5: operand W90/ORef91→RID84, out W89→RCoil35.in, operand W73/ORef48→RID144.

따라서 Set=ON AND NOT Q5.5 AND (I9.7 OR DB13.DBX9.7), Reset=ON AND Q5.5다. NOT은 Q 가지에 있고 LS30 raw 접점 자체에는 없다. raw/DB는 두 실물 센서가 아닌 두 데이터 경로다. Set/Reset의 기억성과 별도 초기화 때문에 MEM_CLOSE=1을 현재 실제 닫힘 증거로 사용하지 않는다. LS26 등 다른 LS의 타이머나 반전을 복제하지 않았다. CYL-CL05의 0288 operand W65/W67 정정은 별도 보강으로 보존하며 본 LS30는 0289 자신의 W65/W67을 확인했다.

### 3.2 원시 Word 전달과 호출 조건

0397 LAD1070 hmi inputs/NID1 Move43: in W55/ORef47→0627 RID15 Tag_181 SAD Input Word AO64=IW8. out1 W57/ORef48→0629 RID16 Word AO64 BAD4→0628 RID4 Inputs TOD13=DB13.DBW8. I9.7과 DB13.DBX9.7이 이 Word 범위에 포함된다. en은 Move42.eno→W53이고 Move43.eno는 W56→Move44.en으로 이어진다. 이 Move 자체에 LS30 비트 반전은 없다.

0030 LAD1613 main/NID19: CRef21 Recipes Handler.eno→W32→CRef23 HMI.en→W33→CRef25 HMI Output.en; CRef25.eno→W42→Contact37.in. Contact37 operand W44/ORef45→0692 RID140 Simulation(1),Memory AO1440=M180.0가 반전되고 out W43→CRef28 HMI Inputs.en이다. CodeBlock22/24/26/29→0688 RID120/124/128/135; CRef28 RefID136은0694 RID136 TORID135로 결속한다. 앞 ENO·M180.0·현재 호출 여부는 확인하지 않았다. raw와 DB가 항상 동기라고 선언하지 않는다.

### 3.3 별도 쓰기: 닫힘기억 startup와 보존된 simulation 원문

0150 LAD405 startup only/NID5: W328 powerrail→Contact326; operand W319/ORef313→0047 RID1 ON M0.0. Contact326.out W327→SCoil305.in, operand W321/ORef315→0563 RID50 AO70 BAD6,0562 RID6 Flag TOD2=DB2.DBX8.6. startup에서 닫힘기억을 Set하는 쓰기이며 이 가지에는 LS30 센서 직렬 확인이 없다. 실제 startup 호출·현재 CPU 초기화는 미확정이다.

0147 LAD402 startup only/NID2에는 Word 초기화 쓰기도 있다. W210 powerrail→Contact208.in, operand W184/ORef167→0047 RID1 ON(NID2 UID167). Contact208.out W209→Move155.en. Move155.in W196/ORef176→0048 RID54 INT#0, out1 W197/ORef177→0563 RID15 Word AO64 BAD6→0562 RID6 Flag TOD2=DB2.DBW8. DB2.DBX8.6은 이 Word 범위에 포함되므로 이름 기반 S/R 검색만으로 쓰기 전체를 확정할 수 없다. 0147 Word0와0150 Set,0289 S/R의 실제 호출·스캔 우선순위는 미확정이며 정적 문서 순서를 현재 최종값으로 단정하지 않는다.

0411 LAD1091 simulation/NID13의 보존 원문에는 DB13.DBX9.7에 대한 다른 쓰기가 존재한다:
- W21 powerrail→Contact28.in.
- Contact28는 반전 operand W48/ORef36 RefID214. 같은 문맥 0636 RID214 SAD Output AO45, NID13 UID36=PV-02 GATE B EV Q5.5.
- Contact28.out W49→Coil29.in. operand W50/ORef37 RefID218→0635 RID218 AO79 BAD5 NID13 UID37 AK Write;0634 RID5 Inputs TOD13.
- 정적 표현은 해당 네트워크가 실행된다는 가정하에 DB13.DBX9.7:=NOT Q5.5다. 이것은 실제 LS30 입력 I9.7의 쓰기가 아니며, 현재 실행·설치·동작 증거도 아니다. 시뮬레이터는 영구 중지했고 실행/수정/생성하지 않았다.

선언 파일 전체에서 EV05_Close, PV-02 GATE B CLOSE, PV_02_GATE_B_MEM_CLOSE 이름을 찾아 해당 문맥을 대조했다(declaration-search.json). 이름 검색만으로 모든 간접/블록/외부 쓰기와 최종 scan 우선순위를 배제할 수 없다. 확인된 raw→Word 쓰기, 다른 DB 쓰기, MEM S/R·startup를 구분하고 현재 호출순서/CPU 프로젝트/강제값·통신 쓰기를 추가 확인 대상으로 남긴다.

부모 Q5.5 요청·EV05 전기부하·공압 구동 상세는 PV02/CYL-CL07~08의 공통근거를 참조한다. 69KA/71KA EV부하접점 **5–9** 정정을 유지한다. 본 LS30에 독립 출력/밸브코일을 만들지 않으며 Q0을 닫힘·무압·안전 접근으로 해석하지 않는다.

## 4. 전기 전달 끝점 — 적용

실제 렌더 oem-73.png/oem-126.png에서 다음 연결을 확인했다.

**+24Vdc10.7→X1/151(도면5×20 2A F)→wire72.4→LS30 contact13→14→X1/152→E9.7→FG125/PDF126 CPU515 MOD10 terminal18.**

FG72의 E9.7 아래 cross-reference는125/7이고 FG125 입력 화살표는72/5이다. 종단 주소 E9.7은 백업 I9.7과 일치한다. FG125 모듈 전원은 +24Vdc10.7→X21/3010(5×20 2A IST.)→wire125.1→terminal19이고 −0Vdc10.6→terminal20이다. 이는 모듈 공통 전원 경로로 LS30 접점 신호선과 구별한다. LS30 도식은13–14 열린 접점 표기이나 실제 설치 정상극성·센서 유형·안전등급·Fail-safe 동작의 증명이 아니다. 퓨즈 표기를 현행 보호값이나 교체 승인으로 사용하지 않는다.

시공 PDF25 ROTARY SIDE02 분기9 LS-30의 cable은 **5_10 =ROT+PV02-LS30A**, CVV1.0 CORE2다. PDF24 공통 분기표에도 같은 전체 ID/5_10이 있고 PDF55 행5_10은 **FROM UC-01 ROT1TB1→TO PV-02 LS-30**, DC CVV2C1.0, SPARE0, 경로 RDD1 E400→100 RDD1→RDD1 E900을 표시한다. 분기9는 장치/도관 번호이며 OEM terminal9로 해석하지 않는다.

상충과 누락을 보존한다:
- PDF24 공통 =ROT+UC01-ROT1TB1A CORE26 vs PDF55 동일 케이블25G.
- PDF24 LS25/26의 짧은 번호5_3/5_4 vs PDF55 5_4/5_5. LS30의5_10 일치와 혼합하지 않는다.
- PDF55 추가 LS31/32를 LS30 별칭·CL08 새 센서로 임의 배정하지 않는다.
- OEM X1/151·152↔ROT1TB1 개별 단자/심선↔LS30 실제 핀/표찰 결속은 미확보다. 현행 단자표·케이블 심선표·승인 준공도 없이는 전 구간 실물 동일성을 확정할 수 없다.

## 5. 알람·복구 — 부모 Gate B 감시 연관 적용, LS30 독립 알람 근거 미확보

LS30 단독 고장 타이머/알람을 새로 만들지 않는다. 직접 연관된 부모 **Allarm.PV_02_GATE_B_NOT_CLOSE DB3.DBX11.0**의 정적 경로만 확인했다. 0452 LAD1818 allarms1/NID45와0655~0658 선언을 대조했다.

- 0657 RID191 AO88 BAD10→0655 RID10 Allarm TOD3. 10.8로 표기하지 않는다.
- ON 공통 가지→Contact1732 **NOT Q5.5**(W31/ORef32→0658 RID165 Output AO45), out W1733→Contact1747와Contact1734.in.
- Contact1747 **NOT MEM_CLOSE** operand W1750/ORef1748→0657 RID169 AO70 BAD12→0655 RID12 Flag TOD2; out W23→SdCoil1663.in.
- SD1663 value W1708/ORef1686→0656 RID320 S5T#7S; operand W1709/ORef1687→0658 RID190 Tag_87 Timer AO110=T110.
- Contact1734 timer operand W1710/ORef1688→RID190, out W24→SCoil1669, operand W1713/ORef1690→RID191. Timer 시작은 ON·!Q·!MEM이고 알람 Set은 ON·!Q·T110 접점이다.
- Reset는 ON·Flag.RESET_ALLARM·자기알람. Contact1738 operand W1715/ORef1691→0657 RID13 Flag AO48=DB2.DBX6.0; out W1739→Contact1740, operand W1716/ORef1692→RID191; out W1741→RCoil1674, operand W1718/ORef1693→RID191.

7초는 백업 부모 감시설정이며 LS30 전용 응답시간/안전시간/현재 보호설정이 아니다. Q=0 감시를 운전중 조건으로 좁히지 않는다. 부모의 나머지 알람·공통 Reset 작성자·자동 상태기계는 기존 PV02 조사로 참조하며 이번에 모두 재검토한 수로 세지 않는다. raw/DB 병렬과 startup Set 때문에 부모 알람의 유무로 LS30 고장 또는 실제 닫힘을 단정할 수 없다. Reset은 원인 제거·실제 복구·재기동 허가와 별개이며 강제입력/접점우회/타이머 연장/반복 Reset을 처방하지 않는다.

## 6. 증상별 관찰 — 적용, 현장 시험·수리 미수행

아래는 승인된 자료 수집 항목이며 통전/구동/접근 명령이 아니다. 자격자의 에너지 격리·잔압·끼임/중력 위험 통제와 승인 절차를 전제로 한다.

| 증상 | 분리해서 남길 관찰 | 판정 한계 |
|---|---|---|
| 실제 닫힌 것으로 보이나 I9.7=0 | LS30 표찰·장착 위치, X1/151·72.4·13/14·X1/152·E9.7의 승인된 관찰 기록 | 공통전원·배선·장착·센서·입력모듈을 분리; 접점 단락으로 시험하지 않음 |
| I9.7와 DB13.DBX9.7 불일치 | 동일 시각 raw/DB, 현재 호출·M180.0·Word 전달·기타 쓰기 근거 | simulation 원문 존재를 현재 실행이라고 해석하지 않음 |
| raw=0인데 MEM_CLOSE=1 | raw/DB 두 OR 입력, Q5.5, ON, startup 이력과 MEM | 래치/초기화 가능성; 실제 위치로 역추론 금지 |
| 닫힘 표시와 HMI 불일치 | I9.7→DB13→DB2→DB11.X78.4를 각각 시각과 프로젝트 근거로 기록 | HMI17인수·이벤트/통신 미결속 유지 |
| 부모 닫힘 미확인 알람 | Q5.5, MEM_CLOSE, T110·DB3.X11.0, 기계 위치와 시간 근거 | 공압/EV/공통게이트/센서 경로 모두 후보; LS30 독립고장 단정 금지 |
| LS30 반응은 있으나 CL08 위치 불명 | CL07/CL08 실물 위치·링크·표찰을 별도 확인 | P&ID 리더가 CL07에 있어 CL08 이동완료를 자동 보증하지 못함 |

관찰 필드: 관찰자, 시간대 포함 시각, 정확한 부품 위치/표찰, 원본과 현재 프로젝트 ID, 값·단위·수집장치, 비교 끝점, 사진 근거, 배제 결과, 승인 조치, 복구 확인자. 실제 사용자 기록·사진·SEJIN 자료를 생성/복제하지 않았다.

## 7. 완료·누락 — 문서 초안과 현장 상태 분리

| 상태 | 판정 |
|---|---|
| documentation | complete_with_gaps 초안:7영역/소유/선언·핀/다른쓰기/PDF 끝점·개정/상충·누락 작성 |
| static_review | 자체 정적 대조 및 선정 원본 해시검사 완료, 부모 독립검토 대기 |
| ui_records | not_run:도면·래더 비교, 백업·선택 복원, 전후기록 비교, 보고서/PDF 기능은 적용 후보이나 구현/저장·재읽기·재열기 검증 없음 |
| publication | not_published; 부모 게시상태 미상속 |
| tia_compile / live_cpu / field_recovery | not_performed |

추가 자료·판정 조건:
1. LS30 명판·센서 형식/제조사·현재 위치/작동점·정상극성·실물 리더 대응이 필요하다.
2. X1/151·152↔ROT1TB1↔LS30 양 끝점 단자·심선표와 승인 준공도로 공통 케이블 상충을 해소해야 한다.
3. 현재 CPU/프로젝트의 raw·DB·기억·startup·다른 쓰기·호출순서를 확인해야 백업 의미가 현행에 적용되는지 판정할 수 있다. 금지 시뮬레이터는 재개하지 않는다.
4. HMI 현재 프로젝트·17실인수/이벤트·통신 주소 확인과 실물 위치의 동시관찰이 필요하다.
5. 승인된 복구 결과·관찰시각·확인자 없이는 정상복구 또는 안전 위치로 완료 처리하지 않는다.

다음 한 작업: 부모가 LS30 0289 Close S/R와0411 다른 쓰기, startup 및 실제 PDF 양 끝점/해시를 독립 검토한다. 새 자료 없이 현장 미확정을 추정으로 채우지 않는다.

## 부록 A. 검사 범위와 전체 선정 원본 무결성

직접 의미검토는 XML27파일의 선택 선언·7네트워크 가지(0147/0289/0397/0030/0150/0411/0452 및 선언20파일), PDF3파일의 실제6페이지(PID1/OEM73·126/시공24·25·55), HMI CSV1파일의 지정 행이다. 전체 XML 내용이나 부모 전체 제어를 의미검토했다는 수가 아니다. 대장·지침·색인 열람, 검색 범위와 파일 해시검사 수는 이 수에 합산하지 않는다.

원본 PDF6페이지 렌더와 PID 상세/개정 확대2개를 extracts/LS30에 보관했다. 처음 PID 확대 범위를 잘못 잡은 출력은 같은 자체 파일을 올바른 좌표로 교체하고 실제 리더·제목란을 다시 확인했다. selected-declarations.txt, 7개의 pretty XML은 읽기 전용 원본에서 만든 정적 발췌다. 원본 생성기/앱/행동시험을 실행한 결과가 아니다.

source-integrity.json: 선정42파일 SHA256 및 고정 Gitblob 바이트 일치42/42, source Git 변경0. 아래 표는 선정 원본 전부이며 파생 초안/범위JSON/중복검토JSON을 고정 Git 원본으로 위장하지 않는다. 해시일치는 현재 CPU·실물·정상극성·현장 복구 검증이 아니다.

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
| EXPANSION-WORK.md | `ec624de9fd2fcfac861a67fd5e828b25ef46db50bfd7a37ff16e2cb54cd0f7e2` | `4c42d88ecc2d48269eb23e13a20ebf3721a092a1` | True |
| all-in-one/ACTIVE-WORK.md | `eff3bbc08ecff41da3beff77f3fec48e7d148708192bcaaab00f34b6a721afc2` | `6eb947c629b5ddf9c759ef87649451303938864b` | True |
| all-in-one/sources/PID_1684n002I.pdf | `2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b` | `8c83a59fefd5b8b651ec3537ea4236a073f5e109` | True |
| all-in-one/sources/Electrical_Rev2.pdf | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` | `f610fd7c7ce14ae951b00cff57b969259bfb389d` | True |
| all-in-one/sources/Electrical_Can_Decoating_20241118.pdf | `3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd` | `0ee6b6f8361c5790864dbba4bbd9d55e8e7c08f8` | True |
| all-in-one/sources/hmi_plc_tags.csv | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` | `cf4c0650e7c7baac350dcb89909b808435704880` | True |
| all-in-one/sources/decoded-original/network-map.json | `c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60` | `424430b6b953e43138e5d0a18ca40c949e21cfa1` | True |
| all-in-one/sources/decoded-original/0147-FlgNet.xml | `386513b215a8cc433f414b1b08279e9760e0efe209070ea95f8e445f674f428c` | `0027890eca158e714dd6260dc920a5d3aa83319b` | True |
| all-in-one/sources/decoded-original/0289-FlgNet.xml | `5460dc0d52bafeeaee0cfd2d66476f7df582002f05a6a17fb4a0928b7e750165` | `fbacf4172f1e1383998a6af80388ecc96c24572b` | True |
| all-in-one/sources/decoded-original/0397-FlgNet.xml | `bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834` | `4ab8370493c4e28fc1eabeeebe2743d27f0c4021` | True |
| all-in-one/sources/decoded-original/0030-FlgNet.xml | `9252c9da764993de1edb8b2e44c46d6e9f9d4b6118e751a0dbeaa9ffd8ea721b` | `e74c70b751acdcdbc7a8b3b0c98aa773c2107cab` | True |
| all-in-one/sources/decoded-original/0150-FlgNet.xml | `829ca4aa3bd2bb6ee406f7f204add2987ec6159ef0fd6dd3dfc075592664a98e` | `b8130ae4a433018f7513d24bd8f0cf79a7897238` | True |
| all-in-one/sources/decoded-original/0411-FlgNet.xml | `282267b493e6b584959a5367d628bf86d15304d901a610614ecd2209d4d01884` | `c2143650e3de0e25c253e1652242e3cfdf4b394f` | True |
| all-in-one/sources/decoded-original/0452-FlgNet.xml | `9612aa97393d5039ea2e0601602a924d52688e89f2d18e507eb51bfa961185e4` | `6eff580e716134fce45db223457e201bc2d5d780` | True |
| all-in-one/sources/decoded-original/0048-IdentXmlPart.xml | `d8e8687de7271bd294c2b62b33d789700af9d5014d82b130141988c4d479253d` | `64fc5a7f1ad33f3b901b00f0d22d23578ffabff8` | True |
| all-in-one/sources/decoded-original/0047-IdentXmlPart.xml | `2e53bb895dd1ad2a74efaeb1ef16dfd61e62b1b2d7aa34cec8612f1b9cb0928e` | `3dc282f149a21fdf76d5521ef1c833be63b578b4` | True |
| all-in-one/sources/decoded-original/0562-IdentXmlPart.xml | `85aada44dd9a3e66835463c3fed400f1efe121f4f5bc5ab8f0ad49481ec0ea1c` | `1609802542a3e560baba3f2b73c306be281dfb23` | True |
| all-in-one/sources/decoded-original/0563-IdentXmlPart.xml | `86cf35b6baebc079cb5a092baf53ec3364c377ea7318eb263ab69c8b4550b4ad` | `6a10fc694f896cda16409804daf2554c91635654` | True |
| all-in-one/sources/decoded-original/0607-IdentXmlPart.xml | `9b76b53536a26e7b45961fecbf825ae1552e16c2fd9af5736864193c01d77f93` | `dbd4da513171f04cca9b1c1741d0293c3e38f98c` | True |
| all-in-one/sources/decoded-original/0608-IdentXmlPart.xml | `24adec2035b65c0c310d637bcea74374896875b6465a16aa2f2cfc8fd55fa4b8` | `cea8f4160d2da00023b1ecc5e591b561e4a08330` | True |
| all-in-one/sources/decoded-original/0609-IdentXmlPart.xml | `395de8ebb2168848cf96fe015bd7334d71107c114a4e441ef36346b8f22031db` | `ee2aab34c0116642dd9f4364b236426f78a876a3` | True |
| all-in-one/sources/decoded-original/0627-IdentXmlPart.xml | `08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb` | `61ebc0abbb2ca160e11e1da400a3f14a397d8bc5` | True |
| all-in-one/sources/decoded-original/0628-IdentXmlPart.xml | `9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd` | `170ca5c72599edc7ea7eefe651c3680ce325e76a` | True |
| all-in-one/sources/decoded-original/0629-IdentXmlPart.xml | `67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972` | `058129bb01e27f7a6a0d0293f332d745e5bab74e` | True |
| all-in-one/sources/decoded-original/0634-IdentXmlPart.xml | `af3fcb536a6270ffb9a19e5b3f2c284a38d67d465f5147961005c1c01d11299d` | `877d9e0734dc7f3e5a8cea789eeb58a208501f48` | True |
| all-in-one/sources/decoded-original/0635-IdentXmlPart.xml | `1a057d686446a3fdab7ac61bb09bc543c52f49646c9ca71ac323c10fcdffe457` | `95bfcad59cfb0c12b573e9e8face4262d1e94622` | True |
| all-in-one/sources/decoded-original/0636-IdentXmlPart.xml | `ec3d79f03e2748f8def4409ad676a97b98e28b9d8e68f6a64b3fe894466832ca` | `86114327ba1a010b2fcc01dd12b1bf86c01bc02c` | True |
| all-in-one/sources/decoded-original/0655-IdentXmlPart.xml | `38e9f323024fba19582b473f39b1ed03ffe6a0b390218894029a6edb0b1ff9fb` | `83b60b9de4541a3ffa6ee0db98205a372b525665` | True |
| all-in-one/sources/decoded-original/0656-IdentXmlPart.xml | `0dbc45e84732a8848f17b094ea08ab8578dbf240bfe15cd7086859395c27c592` | `9bfb9842e55901bab9a71d1ac03158467dfbb1bc` | True |
| all-in-one/sources/decoded-original/0657-IdentXmlPart.xml | `0f70cda60a6b1a17175876d58e25b2686952642de6cffb21213aeef8b347a22b` | `e625f3d8999c7be7d88c50eab0d93107117b58ec` | True |
| all-in-one/sources/decoded-original/0658-IdentXmlPart.xml | `998294c0c8a99e00ceb33c2c60def2cd4850e34328917ae506244c2be2df3831` | `de9a12a6be87466ef1bf05df71c54580c556a827` | True |
| all-in-one/sources/decoded-original/0688-IdentXmlPart.xml | `ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda` | `463585759f1ecd94f32362b4fefb000a152f5773` | True |
| all-in-one/sources/decoded-original/0692-IdentXmlPart.xml | `bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037` | `737785d03b5fad43c5b4d451955726d800edb1c0` | True |
| all-in-one/sources/decoded-original/0694-IdentXmlPart.xml | `757ccebdf32d0a168dd787bfa735fe6494eac4c4a9f7a5adc63898a88e8b152d` | `c45e8f3ca4129dc06734f6a12ef79e6ed6528a7d` | True |