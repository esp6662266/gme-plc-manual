# PV03 고유 제어 근거와 7영역 문서 초안

- 산출물: PV03-DOTS-DRAFT.md, 작업3번 독립 원본 조사 초안, 2026-10-11 UTC.
- 기준: GME-STD-1.0.0. 고정 원본 저장소 `source-mv06`, 커밋 **abcf31c5030bc7ef8749ed8e869a857f2387a28a**, 프로그램 **v1.12.0**. 이 버전은 조사 기준이며 PV03 게시 버전이 아니다.
- 범위: PV03 한 ID의 읽기 전용 원본 조사와 별도 초안. 이번 작업은 독립 root 대조를 마친 대상의 cloud 조사이며 로컬 phase2 133개 통합·게시를 수행하거나 승인한 결과가 아니다.
- 적용 문서: AGENTS.md, gme-equipment-rollout/SKILL.md, WORK-STANDARD.md, WORK-ITEM-TEMPLATE.md, INVENTORY.json 및 최신 인계 상단. 표준의 병행 인원 기본값보다 이번 사용자의 5개씩 독립 조사 지시를 우선한 배정이다.
- 작업자: PV03 독립 조사자. 실제 실행 모델/추론 선택값은 이 산출물에서 별도 검증하지 않았다. 핵심 핀·도면·원본 해시를 최종 재검토했으며 사용자 독립 검토는 인계 후 필요하다.
- 수정 범위: `extracts/PV03/`와 이 초안뿐. 원본 저장소, 공통 코드·버전·대장·배포·운영 기록, 공유 선언 추출본·helper는 편집하지 않았다. 시뮬레이터 작성·수정·생성·실행·행동시험, 실제 PLC·현장·보호값·별도 SEJIN 자료 변경은 수행하지 않았다.
- 상태: 원본 XML/선언/주소/도면 렌더 대조를 마친 **문서 초안, 미확정 포함**. 현재 CPU, 실물, 정상 극성, 현재 설정·보호값, 실제 복구는 미확인. UI·기록·통합·게시 완료가 아니다.

## 먼저 확인할 PV03 고유 결과

1. **출력은 `ON AND (Flag.M_PV03 OR Inputs.PV03 Local Selector)`**다. LAD1972에는 PV01/PV02의 A/B 순서, MC04 허가, maintenance 출력 가지, PV03 알람의 직접 차단 접점이 없다. 이 네트워크 범위를 넘어 공정 전체 보호 부재를 단정하지 않는다. [E03]
2. **위치 기억은 실물 센서 증명이 아니다.** LAD1925 열림 Set은 raw 열림/Inputs 열림/**M_PV03**의 OR, 닫힘 Set은 raw 닫힘/Inputs 닫힘/**NOT M_PV03**의 OR다. 요청만으로 기억 조건이 성립할 수 있으므로 MEM과 raw를 반드시 분리한다. [E04]
3. PV03 도달 감시는 **Tag_88=T111, Tag_89=T112, 둘 다 S5T#5S**다. 감시 피드백은 LS 원시 입력이 아니라 MEM이다. 15분은 인접 LIW feeder의 별도 타이머이며 PV03 동작시간이 아니다. [E05,E08]
4. FG73/PDF74를 실제 렌더하여 확인한 **73KA1 부하 연결은 5–9**다. 상단 미연결 1단자 및 하단 1/5/9 접점표를 부하선으로 읽지 않는다. 24Vdc PLC 릴레이 코일과 110Vac EV06 부하를 분리한다. [E11]
5. HMI 호출 LAD1217은 **12개 ORef 중 FALSE 3개만 선언 결속**, 다른 9개 실인수는 미해결이다. CSV의 DB11 표시 주소나 색인 순서로 누락 핀 이름을 채우지 않는다. [E07]
6. **PB17의 표기 상충**을 보존한다. FG73/126은 73SA1/E10.4, FG244/PDF247 전면 배치는 68SA1, 시공 PDF59는 68.4/E8.5다. 실제 배선을 조사하지 않고 어느 쪽을 현행으로 확정하지 않는다. [E11,E12,E14,E15]
7. PV03는 우선23행의 대응 ID가 아니며 대장에는 phase2/root로 한 번 존재한다. 하위 EV06의 독립 매뉴얼 제외 상태는 유지하고, PV03 출력 끝점 증거로만 다룬다. [E01]

## 1. 설비·자료 기준

### 1.1 식별, 역할, 소유 경계

INVENTORY: catalog_id=PV03, 이름=공압 게이트/분기 밸브, kind=gate, group=공압 밸브, parent_id=null, depth=0, priority_key=null, phase=phase2, queue_state=planned, existing_detail=baseline, bc01_standard_acceptance=not_assessed. 우선23행에서 대응 중복은 없다. 읽기 전용 preflight 결과 `inventory_matches=true`; 전체248/우선23/대응18/제외90/부모보류7/phase2후보133이다. requirements-audit.json·all-in-one-data.json의 이전 바이트 변화는 기존 기준과의 차이이며 이번 조사 변경이 아니다. 대장 구조는 동일하다. [E01]

P&ID 1684n002 **Rev.I, 개정일15/01/2013**, 기본 날짜06/04/2011, 단일 PDF1의 PV-03 Detail은 compressed air→EV06→병렬 CL09/CL10, CL09 주변 LS10/LS09 및 배출 분기 기구를 그린다. 주공정 PV03는 VS01 하류 분기 위치에 나타난다. EV06 한 출력으로 제어되는 분기밸브이며, 실린더 두 개를 PV01/PV02의 A/B 두 독립 게이트와 동일시하지 않는다. [E10]

- 하위 CYL-CL09/CYL-CL10, LS09/LS10는 대장상 PV03 하위 phase2 항목이다. 이번 PV03 문서가 각각의 독립 검증 완료를 뜻하지 않는다.
- EV06은 PV03 하위이나 독립 매뉴얼 작성 excluded를 유지한다. 제어 전달 경로에서 언급해도 제외를 해제하지 않는다.
- VS01/MC04와 BWF/LIW feeder는 공정 연동 또는 인접 설비다. 그 모터·인버터·15분 타이머·전류·속도·보호값을 PV03 소유로 가져오지 않는다.
- PLC/도면 태그 일치와 현재 현장 본체 동일성은 구분한다. 현장 표찰·명판·최신 승인도·현재 CPU 비교가 미확보다.

### 1.2 기존 자료 보존 및 누락

고정 원본에는 `devices/PV03.html`, `control-specs/PV03.html`, `procedures/PV03.html`가 있다. 기존의 부분해석·미확정·과거 시뮬레이션 설계 이력을 보존한다. 같은 위치에서 PV03 전용 alarm-guides/circuit-guides/signal-guides/construction-guides HTML은 발견하지 못했다. 없는 파일을 구현 완료로 표시하지 않는다. [E16]

기존 카드의 “내부 심볼0”은 명칭 기반 분류 결과이며, 이번 원본에서 확인한 DB2의 M_PV03/MEM 3개가 없다는 의미가 아니다. 기존 HMI 호출0/12 결속 표시는 FALSE3개를 새로 결속해 보강할 수 있다. 기존 일반형 A/B 순서 점검문은 PV03 고유 순서가 확인됐다는 근거로 사용하지 않는다. 기존 SIM 항목은 과거 설계·미실행 상태를 그대로 유지하며 실행 대상으로 제안하지 않는다.

### 1.3 근거 식별 규칙

네 자리 번호는 `all-in-one/sources/decoded-original/NNNN-FlgNet.xml` 또는 `NNNN-IdentXmlPart.xml`이다. LAD는 network-map의 document_id이며 index_order와 원본 NID를 분리한다. 심볼 주소는 SAD 영역 + SSD AO(비트 오프셋) + 형식 + DB의 TOD를 결합한다. Timer의 AO111/112는 T111/T112로 읽으며 비트주소로 나누지 않는다.

181개 IdentXmlPart 파일의 선언을 탐색하고 고유·공통14개 네트워크를 정적 대조했다. 단순 RID/UID는 블록 간 충돌하므로 NID, 소속 선언 묶음, Local/Global, BIID.TORID/DB BAD를 함께 확인했다. network-map의 이름과 program-model 등 파생 자료는 탐색용이며 원문 핀을 대신하지 않는다. 예: 공통0399의 RID1/UID24/NID1은 다른 블록의 ON 후보와 겹치지만0630 LocalAccess LS_Open을 사용한다.

## 2. I/O·HMI

### 2.1 물리 신호와 전기 끝점

| 항목 | 백업 심볼·주소·형식 | 원본 선언/색인 | 전기 끝점 |
|---|---|---|---|
| 열림 원시 입력 | Deviator Open PV-03, I10.2 Bool | 0607 RID146, Input AO82, NID15 UID34; live_index879 | +24Vdc10.7→X1/158(5×20,2A F)→LS09 13/14→X1/159→E10.2→FG126 MOD10 단자23 |
| 닫힘 원시 입력 | Deviator Close PV-03, I10.3 Bool | 0607 RID148, Input AO83, NID15 UID39; live_index880 | +24Vdc10.7→X1/160(2A F)→LS10 13/14→X1/161→E10.3→FG126 MOD10 단자24 |
| 현장 선택 원시 입력 | PV03 Local Selector, I10.4 Bool | live_index881의 Address; 직접 SimpleAccess는 이 소비 경로에서 미확보. IW10 Word 전달 및 Inputs 선언을 별도 확인 | +24Vdc10.7→X1/162(2A F)→73SA1/PB17 13/14→X1/163→E10.4→FG126 MOD10 단자25 |
| EV 출력 | PV-03 GATE EV, Q5.6 Bool | 0602 RID195, Output AO46, NID42 UID1153 Write; live_index1293 | FG141 MOD15 단자17 A5.6→FG73 73KA1 A1; A2→-0Vdc10.6 |

I/Q는 백업 주소, E/A는 도면 표기다. 백업 설명에 남은 E29.4/E29.5/E65.7/A56.5를 현재 주소로 사용하지 않는다. 원문상 접점 기호13/14가 있더라도 정상·운전·장애 극성을 현장 검증 없이 확정하지 않는다. CPU515/MOD10·15 역시 도면 표기이며 현재 설치 CPU 모델의 관측이 아니다. [E02,E11,E12,E13]

### 2.2 내부 신호 및 알람 주소

| 변수 | 백업 주소·형식 | 선언 결속 | 구분 |
|---|---|---|---|
| ON / OFF | M0.0 / M0.1 Bool | 0602 RID1/33, SAD Memory AO0/1 | 심볼이며 true/false 상수로 대체 금지 |
| Flag.M_PV03 | DB2.DBX11.2 Bool | 0604 RID193 AO90 +0603 Flag RID2 TOD2; 0609 RID153도 동일 AO | 요청/기억 신호, 물리 센서 아님 |
| Flag.PV_03_GATE_MEM_CLOSE | DB2.DBX9.0 Bool | 0609 RID149 AO72 +0608 Flag RID5 TOD2 | 닫힘 기억, startup 및 정상 로직 쓰기 |
| Flag.PV_03_GATE_MEM_OPEN | DB2.DBX9.1 Bool | 0609 RID147 AO73 +0608 Flag TOD2 | 열림 기억 |
| Inputs.Deviator Open PV-03 | DB13.DBX10.2 Bool | 0609 RID154 AO82 +0608 Inputs RID86 TOD13 | 처리 입력 |
| Inputs.Deviator Close PV-03 | DB13.DBX10.3 Bool | 0609 RID151 AO83 +0608 Inputs TOD13 | 처리 입력 |
| Inputs.PV03 Local Selector | DB13.DBX10.4 Bool | 0604 RID256 AO84 +0603 Inputs RID218 TOD13 | 최종 출력의 OR 입력 |
| Allarm.PV_03_GATE_NOT_OPEN1 | DB3.DBX11.1 Bool | 0657 RID193 AO89 +0655 Allarm RID10 TOD3 | 열림 실패 래치 |
| Allarm.PV_03_GATE_NOT_CLOSE1 | DB3.DBX11.2 Bool | 0657 RID195 AO90 +0655 Allarm TOD3 | 닫힘 실패 래치 |
| Tag_88 / Tag_89 | T111 / T112 Timer | 0658 RID192/194 SAD Timer AO111/112 | PLC S5Time 타이머, HMI 태그 아님 |
| Flag.RESET_ALLARM | DB2.DBX6.0 Bool | 0657 RID13 AO48 +0655 Flag RID12 TOD2 | 공통 내부 Reset |
| Flag.Reset_Allarms_HMI | DB2.DBX13.4 Bool | 0565 RID61 AO108 +0564 Flag RID1 TOD2 | HMI Reset 요청, 위 내부 Reset과 별개 |

주소 계산 예: AO90=11×8+2, AO73=9×8+1. DB2X11.2 요청과 DB3X11.2 닫힘 알람은 다른 DB다. [E03~E06,E09]

### 2.3 raw→Inputs 전달과 다른 쓰기

LAD1070 `0397`, hmi inputs, NID1: Move44의 in←W58/ORef49(RID17), out1→W59/ORef50(RID18). 0627 RID17 Tag_182는 Input Word AO80=IW10, 0629 RID18은 Word AO80/BAD BIRID4, 0628 RID4 Inputs TOD13이므로 **IW10→DB13.DBW10**이다. I10.2/10.3/10.4와 DB13X10.2/10.3/10.4가 포함된다. Move44.en은 W56을 통해 Move43.eno에서 온다. Word 전달 구조를 확인했을 뿐 현재 raw와 DB의 값 일치를 확인한 것은 아니다. [E06]

main LAD1613 `0030`/NID19: Recipes Handler CRef21.eno→W32→HMI CRef23.en; HMI.eno→W33→HMI Output CRef25.en; 그 eno→W42→Contact37의 **NOT Simulation(1)**(ORef45/W44, 0692 RID140 Memory AO1440=M180.0)→W43→HMI Inputs CRef28.en. 0694 BIID RID121/125/129/136의 TORID를0688 FC RID120/124/128/135와 대조했다. ENO/호출 조건/현재 M180.0를 건너뛰어 Inputs가 항상 최신이라고 쓰지 않는다.

보존 원본 LAD1087 `0407`, simulation 블록/NID6에는 Inputs 열림·닫힘의 다른 Coil 쓰기(31/38, 0635 RID162/163, UID32/39)가 있다. 이는 정적 교차참조로만 발견한 충돌 경계다. 해당 원본·시뮬레이터는 실행·수정·생성·행동시험하지 않았다. 실제 활성 여부·최종 쓰기 순서도 확인하지 않았다.

### 2.4 HMI CSV와 실제 호출 경계

| HMI 태그 | 설정 주소 / 내부ID | 확인 범위 |
|---|---|---|
| PV_03\Flag | DB2,X11.2 /00072 | M_PV03 백업 주소와 일치. 실제 객체 클릭·쓰기 이벤트 미확보 |
| PV_03\LS_Open | DB11,X80.0 /00070 | 열림 표시 설정, raw/MEM과 동일 신호로 합치지 않음 |
| PV_03\LS_Close | DB11,X80.1 /0006F | 닫힘 표시 설정 |
| PV_03\Selector | DB11,X80.2 /0006D | 현장 선택 표시 설정 |
| PV_03\Allarme1 | DB11,X80.3 /0006E | 통합 알람 표시 설정. DB3의 단일 알람과 합치지 않음 |
| Allarmi_90 / Allarmi_91 | DB3,X11.1 /00133, DB3,X11.2 /00132 | 백업 PV03 두 래치 주소와 일치하는 공통 알람 태그 |
| ResetAlarms | DB2,X13.4 /002E1 | 공통 HMI Reset 요청 |

PV03 전용 태그는5개이며 공통 알람·Reset을 더해 “PV03 전용8개”라고 세지 않는다. CSV Access Name=PLC, dde.cfg 설정이고 온라인 값/색/이벤트 권한의 증거가 아니다. [E07]

LAD1217 `0393`의 CRef23 RID752는0624의 **NID41**, BIID.TORID751→0623 RID751 HMI PV_1gate(FC16)와 결속된다. 원본 선언은 출력 `HMI_Selectoor` 철자까지 보존한다. 12개 ORef 중 다음3개는0626 RID48 FALSE로 결속된다.

| 방향/핀 | Wire | ORef UID/RID | 결속 상태 |
|---|---|---|---|
| 입력 LS_Open |24|25/753|미해결|
| 입력 LS_Close |26|27/754|미해결|
| 입력 Selector |28|29/755|미해결|
| 입력 Allarm1 |30|31/756|미해결|
| 입력 Allarm2 |32|33/757|미해결|
| 입력 Allarm3 |34|35/48|FALSE,0626 NID41 UID35|
| 입력 Allarm4 |36|37/48|FALSE,0626 NID41 UID37|
| 입력 Allarm5 |38|39/48|FALSE,0626 NID41 UID39|
| 출력 HMI_LS_Open |40|41/758|미해결|
| 출력 HMI_LS_Close |42|43/759|미해결|
| 출력 Total_Allarms |44|45/760|미해결|
| 출력 HMI_Selectoor |46|47/761|미해결|

LAD341 `0399`/0630 LocalAccess는 LS_Open→Coil66/HMI_LS_Open, LS_Close→Coil62/HMI_LS_Close, Selector→Coil58/HMI_Selectoor, Allarm1~5→OR42→Coil54/Total_Allarms를 확인한다. 이 공통 함수 구현이0393의 미결속9개 실인수나 DB11 멤버를 대신 입증하지 않는다. 색인에는 Inputs·PV03 두 알람·Motors.pv_03 멤버가 있지만 순서만으로 결속하지 않는다.

보존 화면 assets/HMI_DECOATER.png에는 2026-10-07 날짜와 하단 PV03, F/G 및 To furnace/To ground 표시가 보인다. 이는 배치·라벨 참고이며 현재 운전, 출구방향과 Q의 극성, 클릭 이벤트, 통신 정상의 증거가 아니다.

## 3. 제어 구조

아래 식은 원본 접점·Wire·코일의 정적 표현이다. 실행모델이나 시뮬레이터를 만들거나 시험한 결과가 아니다. `!`는 원본 Negated, S/R은 원문 래치 쓰기다.

### 3.1 명령→출력: LAD1972 /0272/NID42

- Part1164 ON 접점→W1165 공통 분기.
- OFF 접점1166→W1167→RCoil1141; operand W1157/ORef1150,0604 RID193: **`ON AND OFF`일 때 M_PV03 Reset**.
- M_PV03 접점1168(operand W1158/ORef1151)→W1169→OR1144.in1.
- Inputs.PV03 Local Selector 접점1170(W1159/ORef1152)→W1171→OR1144.in2.
- OR1144.out→W1160→Coil1147; operand W1162/ORef1153,0602 RID195 Q5.6.

**Q5.6 = ON AND (M_PV03 OR Inputs.PV03 Local Selector)**.

M_PV03의 PLC 쓰기로 확인한 것은 이 Reset이며, Set/토글 원인은 HMI 주소와 객체 이벤트를 대조해야 한다. local 선택이 OR에 남으면 M_PV03 Reset만으로 Q가 반드시 꺼지는 것은 아니다. OFF는 M0.1 심볼로, PV03 전체 출력을 직접 차단하는 별도 직렬 접점이 아니다. 확인한 출력 rung에 알람·공기압·MC04·VS01 허가가 없다는 사실을 공정 전체의 인터록/안전회로 부재로 확대하지 않는다. [E03]

### 3.2 실제 입력과 위치 기억: LAD1925 /0290/NID15

| 대상 | 원본 정적 Set/Reset 식 | Part/Wire/ORef 근거 |
|---|---|---|
| MEM_OPEN Set | ON AND Q5.6 AND (I10.2 OR Inputs.Open OR M_PV03) | ON21→W45→Q22→W75→Contact23/77/80→W85/83/84→OR82→W86→SCoil24; operand W50/ORef35 RID147 |
| MEM_OPEN Reset | ON AND !Q5.6 | Negated Contact25→W52→RCoil26; operand W53/ORef37 RID147 |
| MEM_CLOSE Set | ON AND !Q5.6 AND (I10.3 OR Inputs.Close OR !M_PV03) | Negated Q27→W55→Contact28/63/Negated69→W57/66/72→OR65→W67→SCoil29; operand W58/ORef40 RID149 |
| MEM_CLOSE Reset | ON AND Q5.6 | Contact30→W60→RCoil31; operand W61/ORef42 RID149 |

열림 OR의 원시/처리/요청 operand는 ORef34/RID146,78/RID154,81/RID153이다. 닫힘 OR은 ORef39/RID148,64/RID151,74/RID153이며 Contact69만 요청에 대한 Negated다. **M_PV03 요청 가지가 센서 확인을 우회하는 구조적 가능성**을 그대로 남긴다. 현재 CPU에서 실제로 우회됐거나 보호가 고장났다는 판정은 하지 않는다. 두 센서가0 또는 둘 다1인 경우의 실물 상태를 MEM만 보고 판정하지 않는다. [E04]

### 3.3 startup 및 호출 경계

LAD405 `0150`/NID5: ON Contact326(W319/ORef313,0047 RID1)→W327→PV03 SCoil311, operand W324/ORef318/0563 RID53,DB2X9.0. 따라서 startup의 닫힘 기억 Set은 LS10 확인이나 밸브 실제 닫힘 명령이 아니다. Warm/Cold/Retain·실제 Startup OB 결속·CPU 재시작 결과는 미확인이다. [E09]

main LAD1619 `0031`/NID6의 ON282→W283은 Analog input/Allarms1/2/3 호출에 병렬 en을 준다. Allarms1 CRef264/RID59→0694 TORID58→0688 FC4를 확인했다. main LAD1620 `0549`/NID7의 ON350→W351은 Motors1 CRef319/RID68(FC7), R1 scraps gate2 CRef325/RID74(FC99)와 다른 호출에 병렬 en을 준다. 두 블록을 ENO 직렬 연결로 표현하지 않는다. 색인에서 알람 호출 index8, 동작 호출 index9 순서를 확인하지만 그것만으로 현재 CPU 전체 스캔·최종값·원자적 동시성을 단정하지 않는다. [E17]

### 3.4 외부 소유 연동: LIW feeder

LAD1973 `0273`/motors1/NID43에서 Q5.6은 **소비되는 신호**다.

- ON1251 AND (Inputs.BWF01 RUN1253 OR Inputs.BWF02 RUN1255)→OR1190.out/W1233.
- 이 지점은 SdCoil1196(Tag_127=T126, S5T#15M)과 Q5.6 Contact1257 입력에 **병렬**로 연결된다.
- Q5.6 Contact1257.out→W1258→SCoil1201 `START LIW FEEDER` Q6.1(0602 RID198 AO49, ORef1222/W1238).
- 따라서 “15분 후 PV03 또는 LIW를 켠다”로 해석하면 틀리다. Set 분기에 T126 완료 접점이 없다.
- START LIW FEEDER AND !BWF01 RUN AND !BWF02 RUN은 SdCoil1210/Tag_128=T127/S5T#15M에 연결된다. START LIW FEEDER AND T127은 RCoil1215로 Q6.1을 Reset한다.
- S5T#15M은0606 RID196, UID1219/1224, 원문 SV=S5T_x0023_15M/V10496. BWF처리신호는0604 RID257 AO90=DB13X11.2, RID258 AO95=DB13X11.7이다.

이는 별도 feeder의 요청·타이머 경계다. PV03 밸브 수·위치 도달시간·직접 알람으로 합산하지 않으며 feeder 전체 안전·공정 소유는 별도 조사 대상이다. [E08]

## 4. 전기 전달 경로 및 도면 실제 렌더

### 4.1 FG73/PDF74: 출력·코일·부하·센서

원본 Electrical_Rev2.pdf의 **FG73 / PDF74**, 제목 `DEVIATOR DISCH SCREEN VALVE PV-03`, 기본 날짜27.05.2024를 직접 렌더해 확인했다. 이 페이지의 개정칸은 공란이므로 파일명 Rev2를 근거로 이 시트에 임의의 개정일을 넣지 않는다. [E11]

1. **PLC 제어측**: FG141/PDF142의 MOD15 A5.6 단자17→교차73/3→73KA1 A1, A2→-0Vdc10.6. Q=1 자체가 실제 코일 전압/릴레이 동작 확인은 아니다.
2. **EV 부하측**: 110Vac9.7(71/9에서 들어와74/0로 연속)→73KA1 **5–9** 접점→선73.1→X1/156의5×20 2A F→선73.2→EV06 A1; EV06 A2→X1/157→0Vac9.9. 위쪽1단자는 부하선에 연결되지 않는다. 하단 접점표73/1의1/5/9와 실제 배선선을 분리했다.
3. **LS09**: +24Vdc10.7→X1/158 퓨즈2A F→선73.3→LS09 13/14→X1/159→E10.2,126/3.
4. **LS10**: +24Vdc10.7→X1/160 퓨즈2A F→선73.4→LS10 13/14→X1/161→E10.3,126/4.
5. **PB17**: +24Vdc10.7→X1/162 퓨즈2A F→선73.5→73SA1 선택접점13/14→X1/163→E10.4,126/5. 도면0/1 조작 위치와 실제 운전방향은 별도 확인한다.

여기서2A F·4A F 등은 **도면 표기**다. 현재 퓨즈/보호기 정격·설정으로 확정하거나 교체값을 권고하지 않는다. 110Vac 부하를 PLC24Vdc 출력이 EV에 직접 공급한다고 설명하지 않는다.

### 4.2 모듈·공통 전원 끝점

- **FG126/PDF127**: DIGITAL INPUT MODULE, CPU515/MOD10. E10.2/10.3/10.4는 단자23/24/25, 교차73/4·73/5·73/6. 개정란 **2 /17.03.2025**, 기본 날짜27.05.2024. LS32/33·PV04 선택입력의 SPARE 표시는 인접 PV04 범위이며 PV03 입력에 적용하지 않는다. [E12]
- **FG141/PDF142**: DIGITAL OUTPUT MODULE, CPU515/MOD15. A5.6/EV06=17. 출력 모듈 공급 +24Vdc10.9→X21/3033 5×20 4A F→선141.1→단자19, 단자20→-0Vdc10.6. 이 시트 개정란은 공란. A5.7/EV07 SPARE는 PV04 범위다. [E13]
- **FG9/PDF10**: 440V60Hz→9QF1(도면7–10A)→9T1(440/110V,3600VA)→9QF2(32A) 공통 보조전원. 14KA4/14KA8 접점 경로 뒤가110Vac9.7, 공통 귀환0Vac9.9. 이는 공통 회로이며 모든 단자·비상정지 기능을 PV03 전용으로 소유시키지 않는다. [E18]
- **FG10/PDF11**: UPS client 전원→10QF1→10GD1 AC/DC(20A 표기); 입력 공급10QF2→+24Vdc10.7, 출력 전원10QF3·14KA3·14KA7 경로→+24Vdc10.9, 귀환-0Vdc10.6. 실제 보호설정·전압·안전등급·현재 접점 상태는 관측하지 않았다. [E18]

### 4.3 시공 케이블: 참고 설계와 승인 상태 분리

Electrical_Can_Decoating_20241118.pdf PDF34 `CANDC-CONS-E017-034`, PDF59 `CANDC-CONS-C009-059`를 실제 렌더했다. 두 페이지 개정1/24.11.11 first draft design, APPROVED란 공란이다. 문서 표지는 FOR APPROVAL이며 현장 승인 시공도 또는 준공 배선 확인으로 표시하지 않는다. [E15]

| No. / 전체 케이블ID | FROM→TO | 원문 사양·경계 |
|---|---|---|
|9_1 =EXI+EXIT-EXI1TB1A|CR→EXIT EXI1TB1|DC CVV25G1.0, DESCRIPTION SS10/11·LS09-12·PB17; 공통 간선|
|9_2 =EXI+EXIT-EXI1TB1B|CR→EXIT EXI1TB1|AC CVV5G1.0,EV06|
|9_4 =EXI+PV03-EXI1TB3A|EXIT EXI1TB1→PV03 EXI1TB3|DC CVV12G1.0,LS09/10/11/12|
|9_5 =EXI+PV03-EXI1TB3B|EXIT EXI1TB1→PV03 EXI1TB3|AC CVV3G1.0,EV06|
|9_6 =EXI+PV03-PB17A|EXIT EXI1TB1→PV03 PB17|DC CVV5G1.0,원문68.4/E8.5 상충 유지|
|9_9 =EXI+PV03-LS09A|PV03 EXI1TB3→PV03 LS09|DC CVV2C1.0,route E361|
|9_10 =EXI+PV03-LS10A|PV03 EXI1TB3→PV03 LS10|DC CVV2C1.0,route E362|
|9_11 /9_12 =EXI+PV03-LS11A/LS12A|PV03 EXI1TB3→LS11/LS12|DC CVV2C1.0;케이블표 존재,route공란;현재 PLC/FG73 두 센서와 불일치|
|9_13 =EXI+PV03-EV06A|PV03 EXI1TB3→PV03 EV06|AC CVV3G1.0,route E362|

PDF34의 실선 도해는 EXI1TB1→EXI1TB3→LS09/LS10/EV06과 별도PB17을 나타낸다. PDF59의 LS11/LS12 행을 근거로 LS11/LS12가 현재 설치됐거나 추가 PLC 입력을 사용한다고 만들지 않는다. OEM X1/156~163과 시공 EXI1TB3의 **개별 코어·단자 일대일 결속표는 미확보**다. 전체 케이블ID/양 끝점 수준으로 연결하며 단자번호를 복제하지 않는다.

### 4.4 보존할 상충 및 빠진 자료

| 항목 | 확인한 상충·누락 | 필요한 증거 |
|---|---|---|
|PB17 번호·주소|FG73·126:73SA1/E10.4;FG244/PDF247:68SA1;시공PDF59:68.4/E8.5;백업 주석E65.7|최신 승인 접속도·PB17표찰·현재 I/O 목록|
|위치센서 수|P&ID/FG73/백업은LS09/10;시공표는LS11/12도 포함|현재 실린더/센서 설치도,입력 모듈·코어 대조|
|실린더별 감지|P&ID Detail CL09에LS09/10, CL10에는 별도LS 태그가 그려지지 않음|각 실린더·링크·센서 부착 사진/도면|
|정상 극성/기계 방향|Q,MEM,HMI F/G와 실제 furnace/ground 방향의 현장 대조 없음|승인 운전 정의·실물 위치 기록|
|부품 모델/정비값|EV06·CL09/10·LS09/10·73KA1의 현행 명판·제조사 자료 미확보|모델·코일정격·배관·최신 제조사 매뉴얼|
|공기압|P&ID 공장 compressed air 요구와 현장 PV03 사용 압력은 별개|승인 공압도/현장 설정 기록;임의6bar 적용 금지|

FG244/PDF247은 PB17 앞면 도면과 ELFIN080C0909-8P1 표기가 있지만, 이를 현재 구매/설치 모델로 단정하지 않는다. 페이지 번호247과 FG244는 일치하지 않으므로 다른 도면의 +1 오프셋을 전부 적용하지 않는다. [E10~E15]

## 5. 알람·복구

### 5.1 PV03 전용 두 도달 감시

LAD1819 `0453`/allarms1, index_order39, **원본NID46**. ON Contact1784의 출력W1785가 네 분기에 공급된다. [E05]

|대상|정적 식/지연|원본 Part·Wire·선언|
|---|---|---|
|열림 감시 T111|ON AND Q5.6 AND !MEM_OPEN, S5T#5S|Q1786→W1787→Negated1807→W21→SdCoil1709;value W1760/ORef1741 RID175;timer W1761/ORef1742 RID192|
|열림 알람 Set|ON AND Q5.6 AND T111|Contact1788(T111,W1762/ORef1743)→W22→SCoil1715;W1765/ORef1745 RID193|
|열림 알람 Reset|ON AND RESET_ALLARM AND 열림알람|Contact1792→W1793→1794→W1795→RCoil1720;W1770/ORef1748 RID193|
|닫힘 감시 T112|ON AND !Q5.6 AND !MEM_CLOSE, S5T#5S|Negated1796→W1797→Negated1811→W23→SdCoil1727;value W1772/ORef1750 RID175;timer W1773/ORef1751 RID194|
|닫힘 알람 Set|ON AND !Q5.6 AND T112|Contact1798(T112,W1774/ORef1752)→W24→SCoil1733;W1777/ORef1754 RID195|
|닫힘 알람 Reset|ON AND RESET_ALLARM AND 닫힘알람|Contact1802→W1803→1804→W1805→RCoil1738;W1782/ORef1757 RID195|

상수는0656 LiteralConstant RID175, NID46 UID1741/1750, 형식S5Time, **SV=S5T_x0023_5S / V1280**다. 0658 RID192/194는 Timer AO111/112다. 이 타이머 종류·단위를 일반 TON/ms설정이나 다른 밸브의7초로 바꾸지 않는다. 원본 SdCoil/타이머 완료 접점의 연결을 확인했으며 현재 타이머 누적값·정확한 CPU 시간 동작을 시험하지 않았다.

래치 Reset 분기에는 원인 소멸 접점이 직렬로 없다. 따라서 Reset을 원인 제거·실제 닫힘·정상 재기동으로 표시하지 않는다. 조건이 지속되면 재발 또는 Set/Reset 경쟁을 관찰해야 하며 최종값·복구 완료는 CPU의 실제 호출/스캔과 현장 상태를 대조해야 한다.

MEM이 요청 자체로 Set될 수 있으므로 “5초 동안 물리LS 미도달이면 반드시 알람”이라고 표현하면 부정확하다. 알람이 없거나 MEM이1인 것만으로 실물 센서·밸브가 정상이라는 판정도 금지한다. 반대로 이번 정적 결과만으로 현장 안전기능이 고장났다고 단정하지 않는다.

### 5.2 공통 Reset 전달

- HMI ResetAlarms(DB2X13.4)→Flag.Reset_Allarms_HMI(0565RID61) 주소 대응.
- LAD930 `0158`/NID9: Inputs.Reset_allarmi Contact23 OR HMI Reset Contact26→OR28→W38→SCoil33 Flag.RESET_ALLARM(W36/ORef37 RID2), 동시에 RCoil40 HMI 요청(W42/ORef43 RID61).
- 처리 실물 Reset은0565 RID57 AO159=DB13X19.7이며 DB13 TOD는0564RID56으로 확인했다. raw 물리 버튼·I19.7 현장 전달 전체를 이번 범위에서 검증한 것은 아니다.
- LAD931 `0154`/NID4: RESET_ALLARM OR STOP_HORN→OR224→SdCoil229 Tag_160(T47),S5T#1S; 완료Contact263→W264→RCoil235 RESET_ALLARM 해제. 공통 Reset의1초는 PV03 도달 감시5초와 다르다.
-0158의 T#3s/외부 리셋 출력은 공통 인버터·외부 장치 경로이며 PV03 코일 또는 EV 타이머로 분류하지 않는다. 자동 순서의 다른 RESET_ALLARM Set도 선언상 존재하므로 위 흐름을 유일 쓰기로 단정하지 않는다.

공통 Reset 요청 처리와 PV03 알람 Reset/재요청·현장 원인 해제는 별도 단계다. HMI 버튼의 누름 이벤트와 현재 통신을 확인하지 않아 실제 Reset 클릭이 항상 도달한다고 표시하지 않는다. [E19]

## 6. 증상별 수리·관찰 초안

실제 점검은 유자격자가 승인된 정지·잠금/표찰·전원/잔류압 격리 절차로 수행할 영역이다. 이 문서는 강제출력, 보호값 변경, 인터록 우회, 운전 중 조작을 지시하지 않는다. 아래는 **관찰·원인 배제 순서**이며 실제 수리/복구 실적이 아니다.

|증상|같은 시각에 기록할 위치·값|비교·배제할 원인|복구 판정 근거|
|---|---|---|---|
|HMI 요청 뒤 움직임 없음|HMI PV_03 Flag 설정,DB2X11.2,DB13X10.4,ON/OFF,Q5.6|HMI 이벤트/통신→요청 쓰기/Reset→OR 출력→릴레이/부하 전달을 단계별 분리|승인된 운전에서 실제 분기 위치와rawLS·Q·HMI를 대조한 기록|
|M_PV03가0인데 출력 유지|DB13X10.4,I10.4,PB17 상태,Q5.6|local OR 가지·Word전달/다른쓰기·표기상충을 확인;M Reset만으로 정지 확정 금지|현장 선택/요청/출력이 일치하는 승인 관찰|
|Q는1인데 EV가 응답하지 않음|Q5.6,MOD15 단자17,73KA1 제어측과5–9 부하측,EV06/공압부|24Vdc 제어/110Vac 부하/공기/기계 고착을 분리;Q만으로 전압단정 금지|전기·공압·기계별 승인 점검 및LS 실도달 증거|
|MEM/HMI는정상인데 실제위치 불명|I10.2/10.3,DB13X10.2/10.3,DB2X9.0/9.1,M_PV03,Q,HMI표시|요청 OR와 startup 기억·HMI미결속/다른 쓰기 가능성;센서 정상으로 단정하지 않음|실물 위치와 원시입력,기억·표시의 일치/차이를 분리 기록|
|열림/닫힘 실패 알람|DB3X11.1/11.2,T111/T112,Q,MEM,rawLS,Reset|5초 감시 입력·현재CPU값·실제 원인·Reset효과 구분;다른PV시간복사 금지|원인 해제→래치 해제→승인 재요청→도달/재발 없음 각각 증거|
|두LS 모두 0 또는 1|raw·처리값과실물 위치,센서표찰,X1끝점|이동 중/단선/접점/배선/기구와 기억 우회 분리;이번 원문에서 별도 모순 알람을 확인하지 못함|실제 정상 극성·센서 위치 기준 확보 후 판정|
|전원 복귀 후 닫힘 표시|startup이력,MEM_CLOSE,rawLS10,M_PV03/Q|startupSet을실제 닫힘으로오인했는지,Retain·호출·HMI표시 구분|현장 위치·현재 프로젝트·재시작 관찰 근거|
|LIW동작이PV03와 다름|Q5.6,DB13X11.2/11.7,START LIW Q6.1,T126/T127|LIW 소유 S/R,15분 타이머 병렬/직렬 경계;PV03 알람으로 합치지 않음|별도feeder 담당의 연동 기록·승인 동작 대조|

관찰 양식: 관찰자 / UTC 또는 현장 시간대를 포함한 시각 / 설비와 실물 표찰 / 수집 장치 / 현재 CPU·프로젝트 식별 / 모드·요청 / raw I / Inputs DB / M_PV03 / MEM / Q / 릴레이·EV·기계 위치 / 타이머·알람 / 비교 원본 FG·PDF·LAD·Part / 원인 후보별 배제 / 승인 조치 / Reset·재요청·실물 도달의 개별 증거. 값 0과 미측정 빈칸을 구분하고 실제 운영 사진·이력을 공개 저장소에 복제하지 않는다.

## 7. 적용·완료 기준과 인계

### 7.1 7영역 적용표

|영역|상태|작성위치|누락·비해당 경계|
|---|---|---|---|
|설비·자료기준|적용|1|현재 실물·명판·최신 승인도 미확보|
|I/O·HMI|적용/일부근거미확보|2|HMI 9개 실인수·객체 이벤트·현재 통신 미결속|
|제어구조|적용|3|현재 CPU 전체 호출·복수 쓰기 최종값·현장 동작 미검증|
|전기전달|적용/일부근거미확보|4|코어/현장 단자의 일대일 결속·정상 극성·실부품 미확보|
|알람·복구|적용|5|타이머 현재값·실물 원인·복구 결과 미확보|
|증상별수리|적용(관찰초안)|6|실제 조치·현장 승인·복구 실적 없음|
|완료기준|적용|7|통합·화면·기록·배포·TIA·CPU·현장 미수행|

모터 전력/속도/전류/PID·엔코더교정은 이번 PV03 직접 제어에 비해당이다. 공압부품 모델·압력·정비주기는 비해당이 아니라 근거 미확보다. 두 실린더를 모터 또는 두 독립PLC게이트로 만들지 않는다.

### 7.2 네 기능 적용 및 기록 보존

|기능|적용 근거·제안|실제 검증|
|---|---|---|
|도면·래더 비교|FG73↔LAD1972 출력·1925 기억·1819 알람, FG126↔1070 입력 전달|원본 정적 대조만. UI 구현/강조/왕복 미검증|
|백업·선택복원|PV03 기록 키·기존 기록/초안/알 수 없는 필드/다른 설비 분리 필요|읽기/쓰기·저장·재읽기·재열기 미실행|
|기록전후비교|동일 위치·주소·시간대·원본 버전·raw/DB/MEM/Q 구분|합성 QA 포함 미실행|
|관찰보고서/PDF|6절의 관찰·원인 배제·조치·개별 복구 증거|설비 보고서 생성/렌더 미실행. 원본도면 렌더와 구분|

이 초안을 받은 날짜나 saved_with/generated_with는 현장 CPU·관찰 시점의 근거로 소급 적용하지 않는다. 사용자 note/repair_observation·알 수 없는 행/필드·다른 설비·초안·저장 키를 보존한다. 현재 통합/UI의 수용 여부는 부모가 별도 권한/범위에서 판단할 일이며 이번 phase2 초안 전달 자체로 게시를 시작하지 않는다.

### 7.3 수행 검증과 상태

- Git HEAD와VERSION 확인: abcf31c5030bc7ef8749ed8e869a857f2387a28a /v1.12.0. 조사시 Git status는 clean.
- 스킬 preflight 읽기 전용 실행: 종료0, inventory_matches=true. 결과 extracts/PV03/preflight.json.
- XML 구조·선언 탐색:181 IdentXmlPart,2938선언행. 이 초안 고유·공통14개 네트워크를 정적대조. unresolved/다른 블록 충돌을 보존한다.
- 원본도면 렌더·시각검토:Electrical PDF10/11/74/127/142/247,시공 PDF34/59,P&ID PDF1의 **9쪽**. P&ID의 PV03상세/타이틀 추가확대 포함. HMI 저장PNG1개 시각검토.
- 조사 근거71개 파일의SHA256 저장·재확인. 아래 부록과 extracts/PV03/source-sha256.json/tsv가 기준.
- 미실행: 생성기,시뮬레이터, 행동시험, TIA 컴파일, 현재 CPU 접속, 현장 측정/복구,UI/모바일/큰글자,백업복원/동시성/Quota,BC01회귀,패키징/배포. 읽기 전용 초안 범위이므로 불필요한 실행을 하지 않았다.

|구분|상태|범위|
|---|---|---|
|documentation|draft_complete_with_gaps|PV03 독립 원본 초안, 통합 아님|
|static_review|source_cross_checked; independent_review_pending|핵심 근거 재검토 완료; 사용자 독립 검토 필요,문서의 정적 범위만|
|ui_records|not_run|구현·저장 검증 없음|
|publication|not_published|phase2 로컬 통합·게시 범위 밖|
|tia_compile|not_performed|실행 금지 범위 유지|
|live_cpu|not_performed|백업과 현재 CPU의 동일성 미확인|
|field_recovery|not_performed|정상 극성/현재 설정/실물 복구 미확인|

### 7.4 다음 필요한 한 작업

부모가 **PV03 초안의 독립 원본 검토**를 수행한다. 우선 다음 다섯 항목을 확인한다.

1. LAD1925 M_PV03/NOT 분기의 MEM 우회 경계
2. LAD1819 T111/T112의 원문 5초
3. FG73 부하 접점 5–9
4. PB17의 표기 상충
5. LAD1217의 미결속 9개 핀

검토가 끝나도 현장 미확인, EV06 제외, phase2 로컬 게시 제외는 유지한다. 현재 자료가 없는 부분은 보류로 남기며 다른 독립 설비 조사를 막지 않는다.

## 부록 A. 핵심 근거표

모든 경로는 고정 원본 저장소 기준이다. XML/선언은 `all-in-one/sources/decoded-original/` 아래에 있다. 각 파일의 원문 바이트 해시는 부록 B에 있다.

|근거|파일·위치|확인내용·경계|
|---|---|---|
|E01|docs/equipment-standard/INVENTORY.json;preflight출력|PV03 root/phase2/우선대응없음,하위분리·EV06제외|
|E02|sources/live_index.json _7ev879/880/881/1293;0607선언|I10.2/10.3/10.4,Q5.6;과거주석분리|
|E03|0272-FlgNet;0602/0603/0604-IdentXmlPart|LAD1972/NID42 출력·OFF Reset·DB소유|
|E04|0290-FlgNet;0607/0608/0609-IdentXmlPart|LAD1925/NID15 두MEM의S/R와raw/처리/요청OR|
|E05|0453-FlgNet;0655/0656/0657/0658-IdentXmlPart|LAD1819/NID46,S5T5S,T111/112,알람S/R|
|E06|0397-FlgNet;0627/0628/0629;0030;0688/0692/0694|IW10→DB13W10,mainHMI호출·NOT M180.0|
|E07|sources/hmi_plc_tags.csv719~723,공통Allarmi90/91·ResetAlarms;0393/0399;0623/0624/0626/0630;assets/HMI_DECOATER.png|5PV태그,3FALSE확정/9실인수미결속,공통함수로직,저장화면|
|E08|0273-FlgNet;0602/0603/0604/0606|LAD1973/NID43,LIW소유Q6.1와T126/127,S5T15M병렬분기|
|E09|0150-FlgNet;0047/0562/0563|startupLAD405/NID5,MEM_CLOSE Set|
|E10|sources/PID_1684n002I.pdf1|PV03 Detail,EV06,CL09/10,LS09/10,Rev.I15/01/2013|
|E11|sources/Electrical_Rev2.pdf74/FG73|73KA1부하 5–9,EV06,X1/156~163,LS와PB17|
|E12|동PDF127/FG126|E10.2/10.3/10.4,MOD10단자23/24/25,Rev2 17.03.2025|
|E13|동PDF142/FG141|A5.6 MOD15단자17,+24V10.9공급·단자19/20|
|E14|동PDF247/FG244|PB17전면68SA1,ELFIN표기,현장 모델 미확정|
|E15|sources/Electrical_Can_Decoating_20241118.pdf34/59|배선루트·케이블양끝,LS11/12·PB17상충,설계참고|
|E16|devices/PV03.html,control-specs/PV03.html,procedures/PV03.html|기존 완료분·미확정·과거 설계 보존,전용 4개 가이드 미확보|
|E17|0031/0549;0688/0692/0694|mainNID6/7 ON병렬호출,FC4/7/99소유|
|E18|Electrical_Rev2.pdf10/11,FG9/10|공통110Vac·24Vdc기원;현장보호값 아님|
|E19|0158/0154;0564/0565/0566/0567|공통 Reset 요청·내부 Reset·1초 해제,PV03 도달 타이머와 분리|
|E20|0407-FlgNet;0634/0635|보존원본의Inputs다른 쓰기 존재만 정적 확인;중지 자산 실행 없음|

## 부록 B. 원본과 조사 기준 SHA256

아래는 원본 XML·선언·PDF·보존 기존 자료·읽은 기준 문서71개 파일의SHA256이다. 추출 JSON/PNG는 읽기 전용 파생물이며 원본을 대체하지 않는다. 별도 `extracts/PV03/source-sha256.json`에는 bytes와 고정 커밋을 함께 기록했다.

| 파일 | SHA256 |
|---|---|
| .agents/skills/gme-equipment-rollout/SKILL.md | fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b |
| .agents/skills/gme-equipment-rollout/scripts/preflight.py | 395067d6da20af3e1d82a43b7936907a87a44d8d2e11e4ebc61b1fc441e2adb6 |
| AGENTS.md | 0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2 |
| EXPANSION-WORK.md | ec624de9fd2fcfac861a67fd5e828b25ef46db50bfd7a37ff16e2cb54cd0f7e2 |
| PUBLICATION_STATUS.md | efe4857aec598d90470322cf3962eb3fe1f64947630e1fdf71d1c90134de8740 |
| VERSION.json | 5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7 |
| WORKSPACE-HANDOFF.md | 215096d997782e78e901dfae36c782937e49611fbeb677a0d3fa50cbecf8d074 |
| all-in-one/ACTIVE-WORK.md | eff3bbc08ecff41da3beff77f3fec48e7d148708192bcaaab00f34b6a721afc2 |
| all-in-one/assets/HMI_DECOATER.png | b84b888a2df87d23b514aeb790d2fc51f31c3b20486061a365380b28986f49af |
| all-in-one/control-specs/PV03.html | 52c110479eadb021520766b5c89790bd73d8c3afde11821560320fd41b931f4f |
| all-in-one/devices/PV03.html | 6f6486743801b128137da706857487874330efa41fd059e7de5c4ba763093fdc |
| all-in-one/procedures/PV03.html | ed43269c63f10d73e4d2bc0fd4413a0cc6805a760db7f22c2c360f5cb18050b5 |
| all-in-one/sources/Electrical_Can_Decoating_20241118.pdf | 3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd |
| all-in-one/sources/Electrical_Rev2.pdf | 5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6 |
| all-in-one/sources/GME_20250506.zap18 | 00c79b6d986e68298f65b172c1807115bc5d9e450a74fcc989d0796d8d8a4ea8 |
| all-in-one/sources/PEData.plf | 647de7ea123daced41c27bec8f81aeb93c712cac714d4754d7da5c528abb016a |
| all-in-one/sources/PID_1684n002I.pdf | 2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b |
| all-in-one/sources/block_summary.json | 68253f9366908244a27ed461c66d465da7ec1723571f27deaa9a6f81a542de63 |
| all-in-one/sources/can-decoating-page-text.json | d3b4c14945dd00f79c58ebab0cb8991c422dd1670e95e24d10779bd9e9d99bba |
| all-in-one/sources/decoded-original/0030-FlgNet.xml | 9252c9da764993de1edb8b2e44c46d6e9f9d4b6118e751a0dbeaa9ffd8ea721b |
| all-in-one/sources/decoded-original/0031-FlgNet.xml | 76385eab8f8f72b9faa16f7cf8905f395591b18c0a9ee9e6d7dd085a38c45c65 |
| all-in-one/sources/decoded-original/0047-IdentXmlPart.xml | 2e53bb895dd1ad2a74efaeb1ef16dfd61e62b1b2d7aa34cec8612f1b9cb0928e |
| all-in-one/sources/decoded-original/0150-FlgNet.xml | 829ca4aa3bd2bb6ee406f7f204add2987ec6159ef0fd6dd3dfc075592664a98e |
| all-in-one/sources/decoded-original/0154-FlgNet.xml | b0a163ffa382b722eaa34df4bdc4c3dd06039b296b791d26d68639a7b0502746 |
| all-in-one/sources/decoded-original/0158-FlgNet.xml | d3f3adebc3d990b85c5d4c294906ae3bc3dafebb49d25b030bf9cc2ccf905651 |
| all-in-one/sources/decoded-original/0272-FlgNet.xml | 654fbd1c537044693d242b4d806ea8304db9bd83f2655b2566468812103c3357 |
| all-in-one/sources/decoded-original/0273-FlgNet.xml | 48cc05ab4fb2778e2878b53993f10a31250dfeadd8b56024af4647a1e1da7f31 |
| all-in-one/sources/decoded-original/0290-FlgNet.xml | 616ae571a3a19d97d71137ac539cc6e5c8b1db13b0e2b78ae8c1f9401098bc0f |
| all-in-one/sources/decoded-original/0393-FlgNet.xml | 4fd48bb847e05d1c0acde816355e9af52e938674ba10cfe79405bf7210ddd307 |
| all-in-one/sources/decoded-original/0397-FlgNet.xml | bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834 |
| all-in-one/sources/decoded-original/0399-FlgNet.xml | b50c835a4574fc753570fb7121b2475fc5feaf48f48edc2e8137531b359d809c |
| all-in-one/sources/decoded-original/0407-FlgNet.xml | ba022010d6f83dcebd6cce8dbd50ab2ad3744e078ad661934af970db81023927 |
| all-in-one/sources/decoded-original/0453-FlgNet.xml | 6568f1de0c71ba481a06ceda596a574746330d2971b735029a127582344d911d |
| all-in-one/sources/decoded-original/0549-FlgNet.xml | 49f7169c33ed7f54559b0801e21a7d618584900972840e91cf51ad032e8febb1 |
| all-in-one/sources/decoded-original/0562-IdentXmlPart.xml | 85aada44dd9a3e66835463c3fed400f1efe121f4f5bc5ab8f0ad49481ec0ea1c |
| all-in-one/sources/decoded-original/0563-IdentXmlPart.xml | 86cf35b6baebc079cb5a092baf53ec3364c377ea7318eb263ab69c8b4550b4ad |
| all-in-one/sources/decoded-original/0564-IdentXmlPart.xml | 2aed17fa02d19b0a081023282841aa561d6a2dca3e393284da3622b967af00b1 |
| all-in-one/sources/decoded-original/0565-IdentXmlPart.xml | 0f7f970faa6c456f2bb032b1a2072a2f52db1e03fc77bd8d35d4583deeaf1149 |
| all-in-one/sources/decoded-original/0566-IdentXmlPart.xml | a1914c7ae085acc1f949a649979824bec8b46fcd78a8055318272a1eb5a45265 |
| all-in-one/sources/decoded-original/0567-IdentXmlPart.xml | 5d428b5d5a2b0f4649dbbbb4e4f060a9d89a107e9cf4b6139d8f003c4371347e |
| all-in-one/sources/decoded-original/0602-IdentXmlPart.xml | 46ab21151eddaaf616469db520730c60423eb742aa491af194e6710c751b4caf |
| all-in-one/sources/decoded-original/0603-IdentXmlPart.xml | e93969dfa281d75b49b24127793068e33472dadb19729c1c48fc4a8dad075ef8 |
| all-in-one/sources/decoded-original/0604-IdentXmlPart.xml | b798d29c5499b5314a1ee3cff9139dae64c887533b86baa43b6e9a052373a6af |
| all-in-one/sources/decoded-original/0606-IdentXmlPart.xml | 73d45f9e2a34bba8a25df1ed1f71e8f6404fc96a8d6481672652a48435b6a740 |
| all-in-one/sources/decoded-original/0607-IdentXmlPart.xml | 9b76b53536a26e7b45961fecbf825ae1552e16c2fd9af5736864193c01d77f93 |
| all-in-one/sources/decoded-original/0608-IdentXmlPart.xml | 24adec2035b65c0c310d637bcea74374896875b6465a16aa2f2cfc8fd55fa4b8 |
| all-in-one/sources/decoded-original/0609-IdentXmlPart.xml | 395de8ebb2168848cf96fe015bd7334d71107c114a4e441ef36346b8f22031db |
| all-in-one/sources/decoded-original/0623-IdentXmlPart.xml | 4acd00406ea92466169e57e59fc90b0da4d9ec55fd19e2e96c9556e939cb83a6 |
| all-in-one/sources/decoded-original/0624-IdentXmlPart.xml | 24607c0827fbde428bccf8637ef4ae490798a69a7c2f3b87861d0749082d367a |
| all-in-one/sources/decoded-original/0626-IdentXmlPart.xml | a9d7fbea345eca70325a8c2e44058c23e96add1b7207eabbb09445118b18188b |
| all-in-one/sources/decoded-original/0627-IdentXmlPart.xml | 08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb |
| all-in-one/sources/decoded-original/0628-IdentXmlPart.xml | 9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd |
| all-in-one/sources/decoded-original/0629-IdentXmlPart.xml | 67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972 |
| all-in-one/sources/decoded-original/0630-IdentXmlPart.xml | 1526a89b425470fa6e874bb4a9b6c7bc8e58b740f80d018b9106b6916f402372 |
| all-in-one/sources/decoded-original/0634-IdentXmlPart.xml | af3fcb536a6270ffb9a19e5b3f2c284a38d67d465f5147961005c1c01d11299d |
| all-in-one/sources/decoded-original/0635-IdentXmlPart.xml | 1a057d686446a3fdab7ac61bb09bc543c52f49646c9ca71ac323c10fcdffe457 |
| all-in-one/sources/decoded-original/0655-IdentXmlPart.xml | 38e9f323024fba19582b473f39b1ed03ffe6a0b390218894029a6edb0b1ff9fb |
| all-in-one/sources/decoded-original/0656-IdentXmlPart.xml | 0dbc45e84732a8848f17b094ea08ab8578dbf240bfe15cd7086859395c27c592 |
| all-in-one/sources/decoded-original/0657-IdentXmlPart.xml | 0f70cda60a6b1a17175876d58e25b2686952642de6cffb21213aeef8b347a22b |
| all-in-one/sources/decoded-original/0658-IdentXmlPart.xml | 998294c0c8a99e00ceb33c2c60def2cd4850e34328917ae506244c2be2df3831 |
| all-in-one/sources/decoded-original/0688-IdentXmlPart.xml | ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda |
| all-in-one/sources/decoded-original/0692-IdentXmlPart.xml | bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037 |
| all-in-one/sources/decoded-original/0694-IdentXmlPart.xml | 757ccebdf32d0a168dd787bfa735fe6494eac4c4a9f7a5adc63898a88e8b152d |
| all-in-one/sources/decoded-original/network-map.json | c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60 |
| all-in-one/sources/electrical-page-text.json | 4b846819aab7e1306aebea617042f9f9ffe0c8aee1930e6f3db035bea3739153 |
| all-in-one/sources/hmi_plc_tags.csv | a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404 |
| all-in-one/sources/live_index.json | 14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1 |
| all-in-one/sources/source-manifest.json | 5af6e85994536897fd92f75972534a691e6eb0f067aafe07679c0788fd84e5bf |
| docs/equipment-standard/INVENTORY.json | 720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc |
| docs/equipment-standard/WORK-ITEM-TEMPLATE.md | 4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586 |
| docs/equipment-standard/WORK-STANDARD.md | 05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99 |

## 부록 C. 재검토 산출물

- extracts/PV03/*-trace.txt: 원본 Part/Gate/Negated, ORef/CRef의 RID/UID/NID 선언 후보 및 모든 Wire 끝점. 다른 블록 충돌 후보는 자동 확정하지 않으며 본문에서 실제 사용한 선언 묶음을 지정했다.
- extracts/PV03/*-refs.json, networks.json: 별도 PV03 원본 추적 자료. 공유 declarations.json은 변경하지 않았다.
- extracts/PV03/FG73-PDF74.png 및 ELEC/CON/PID 렌더: 실제 시각검토 근거.
- extracts/PV03/inventory-selection.json,preflight.json,source-sha256.json/tsv: 대상·대장·원본 해시 확인.
- 완료 커밋 없음: 원본 저장소에 변경·커밋·게시하지 않은 초안이다.
