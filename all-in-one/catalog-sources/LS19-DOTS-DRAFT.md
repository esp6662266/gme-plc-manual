# LS19 — MV03 개방측 리미트 독립 원본 조사 초안

- 2026-10-11 UTC, GME-STD-1.0.0, 고정 원본 `source-mv06` commit `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, v1.12.0. documentation=complete_with_gaps, 통합 전 독립 검토용.
- 대상은 LS19 하나. `INVENTORY.json#/catalog/230`, TASK3-BATCH23-SCOPE와 GME-CATALOG-OVERLAP-REVIEW의 parent_child_separate 분류에 따라 부모 MV03, component/depth1/phase2, baseline/planned, priority_key=null. 부모 완료·우선순위를 상속하지 않는다.
- 원본 AGENTS, gme-equipment-rollout SKILL, WORK-STANDARD, WORK-ITEM-TEMPLATE, 최신 인계/진행 상단을 읽었다. 실제 모델·추론 설정 UI는 미관측이다. MV03·ZT04 초안은 탐색색인·부모 공통근거로 재사용했다.
- 수정 범위는 이 MD와 `extracts/LS19/`뿐. 원본/공통코드/버전/대장/배포/PLC/현장/보호값/SEJIN 변경0, 시뮬레이터 작성·수정·생성·실행·행동시험0, 원본 생성기/앱 빌드0, 업로드/새 Work·Codex/재위임0.

## 1. 설비·자료 기준 — 적용

**LS19는 문서상 MV03 개방측 리미트, 원시 I7.5 → 별도 NOT → 처리 DB13.DBX7.5이다.** NC 접점 도면, 소프트웨어 반전, 부모 제어의 정·반전 접점은 서로 다른 증거다. ‘개방’ 명칭만으로 현재 1=완전 개방이라고 정하지 않는다.

P&ID `all-in-one/sources/PID_1684n002I.pdf` 실제1쪽 원본 렌더와 MV03 확대에서 Overflow valve MV-03에 M17, LS-19, LS-20, ZT-04가 연결됨을 확인했다. 도면1684n002 Apex I, 기본일06/04/2011, 개정 I 15/01/2013 REMOVED MC-05, CHANGED POWER OF FN-02; H 01/08/2012 ADDED MV-06, AND MODIFIED MV-03 COMMAND INSTRUMENT. P&ID는 식별 근거이며 각 접점의 전기주소·현행 설치물 동일성 증명은 아니다.

OEM `Electrical_Rev2.pdf` FG39/실제PDF40의 MOTORiZED VALVE MV-03, LIMIT SWITCH VALVE OPEN, LS-19와 FG123/실제PDF124 E7.5의 LIMIT SWITCH LS-19가 직접 전기 근거다. 부모 모터 정격 상충, 방향출력/접촉기, 압력제어는 MV03 초안을 재사용하고 전체를 재조사하지 않았다. LS20 닫힘·ZT04 엔코더·접촉기 응답 I2.4/I2.5는 LS19와 별개다. 공유함 FLO1TB1이 LS15/16/19/20을 경유한다는 이유로 모든 센서를 MV03 소유로 옮기지 않는다.

EV 69KA/71KA 부하접점5–9 정정은 유지한다. 관련 없는 EV 회로를 이 LS 문서에 추가하지 않는다. 현재 CPU·실물·정상극성·현행보호설정·현장복구는 모두 미확정이다.

## 2. I/O·HMI·기억값 — 적용 / HMI 최종 결속 미확보

NNNN XML은 `all-in-one/sources/decoded-original/` 아래 `NNNN-FlgNet.xml` 또는 `NNNN-IdentXmlPart.xml`이다. RID는 선언 문맥, NID는 네트워크, UID는 Part/ORef/Wire별 식별자다. 서로 다른 블록의 같은 번호를 동일 선언으로 합치지 않는다.

| 층 | 주소·자료형 | 선언·직접 근거 | 경계 |
|---|---|---|---|
| 물리 원시 | I7.5 Bool / 도면 E7.5 | 0627 SimpleAccess RID152 MV03_Open, NID1 UID132, SAD Input, AO61. plc-symbols.csv document887 mv03_open,%i7.5,bool,limit switch ls-19 | 현재 입력값 아님 |
| 포함 원시 word | IW6 Word | 0627 RID13 Tag_171, NID1 UID45, Input AO48 | bit I7.5가 포함되는 word |
| 처리 word | DB13.DBW6 Word | 0629 RID14 NID1 UID46 Write, AO48/BAD4; 0628 RID4 Inputs TOD13 | 원시 word 복사 후 bit 추가쓰기와 구분 |
| 처리 LS19 | DB13.DBX7.5 Bool | 0629 RID153 NID1 UID148 Write, AO61/BAD4 | 0397 NOT 결과 |
| 부모 제어 읽기 | 같은 DB13.DBX7.5 | 0619 RID175 NID4 UID23/30, AO61/BAD168; 0618 RID168 Inputs TOD13 | 최종출력 차단/수동요청 해제의 서로 다른 극성 |
| PID 경로 읽기 | 같은 DB13.DBX7.5 | 0668 RID127 NID12 UID532 AO61/BAD118; 0666 RID118 Inputs TOD13 | LMNR_HS로 반전 전달 |
| 버너 경로 읽기 | 같은 DB13.DBX7.5 | 0585 RID231 NID14 UID24 AO61/BAD217; 0584 RID217 Inputs TOD13 | 버너 소유 순서조건 |
| 별도 쓰기 | 같은 DB13.DBX7.5 | 0635 RID239 NID2 UID520 Write AO61/BAD5; 0634 RID5 Inputs TOD13 | 보존된 simulation 블록의 정적 쓰기, 현재 실행 미확정 |
| HMI 설정 | MV_03\LimitSwitchOpen = DB11,X22.3 | hmi_plc_tags.csv ID00043, Access Name PLC | DB13·I7.5와 다른 주소, 실제 이벤트/통신 미검증 |

LS19 전용 MEM_OPEN/CLOSE 또는 고유 위치 Set/Reset 래치 선언은 이번 한정 검색에서 확보되지 않았다. 처리 DB13는 저장위치지만 실제 종단 도달을 독립 보존하는 센서기억으로 단정하지 않는다. 부모 수동요청 Flag.M_MV03_OPEN DB2.X9.7과 ZT04 계열 DB8 엔코더 기억은 LS19 전용 위치기억이 아니다. 전체 PLC에 기억값이 없다는 부재 증명도 하지 않는다.

### HMI 미결속 경계

0369, LAD1191 hmi mv03: CRef22/RID639, CodeBlock23/RID130; W56 ORef33/RID687 → Limit_switch_Open, W64 Limit_Switch_Open_HMI → ORef41/RID451. 호출 네트워크의 단일 NID와 이 두 RID의 동일문맥 선언을 확보하지 못했다. 전 선언에서 찾은 0676 RID451은 NID40 UID1545의 Int이며 이 Bool 호출 선언으로 채택하지 않았다. 따라서 I7.5→DB13.X7.5→HMI DB11.X22.3 전구간 결속 완료라고 하지 않는다. 부모 초안의 0623/0624 호출이름 색인과 미결속 상태를 유지한다.

## 3. 제어 — LS19 고유 가지 정적 검토

### 3.1 word 전달 뒤 별도 NOT

0397 LAD1070 hmi inputs NID1:

1. Powerrail W21 → Move42.en. W52 ORef45/RID13 → in, W54 out1 → ORef46/RID14: IW6→DB13.DBW6. Move42에는 DisableENO=true 속성이 있고 eno W53이 다음 Move43.en에 연결된다. 속성과 연결을 함께 보존하며 실제 실행 의미는 CPU 미검증이다.
2. raw Contact127 operand W122/ORef132/RID152 → W137 Not142.in → W145 Coil147.in → operand W146/ORef148/RID153. **처리 DB13.X7.5 = NOT 원시 I7.5**라는 별도 쓰기다. Word 복사만 기록하거나 두 값을 같은 극성으로 기술하면 안 된다.
3. 0030 LAD1613 main NID19: HMI Output CRef25.eno W42 → NOT Contact37(operand W44/ORef45/RID140) → W43 HMI Inputs CRef28.en. 0692 RID140은 Simulation(1), Memory AO1440=M180.0. 상류 ENO와 조건부 호출이 있으며 무조건 갱신 보장이 아니다. 가상 실행 없이 원본 연결만 확인했다.

### 3.2 부모 방향출력 차단과 수동요청 해제

0345 LAD1706 valve control loop NID4에서 두 읽기는 같은 0619 RID175에 결속된다.

- **반전 최종 조건:** NOT ResetEncoderProcedure Contact44.out → W47 → NOT 처리Open Contact523.in; operand W29/ORef30/RID175. W28 → Coil390, operand W470/ORef428/RID47. 0617 RID47 Start open MV03 Output AO15이므로 Q1.7. 처리Open은 개방출력의 마지막 반전 조건이며 이것 하나만으로 출력이 결정되지는 않는다.
- **정접점 요청 해제:** ON Contact491.out → W492 → 처리Open Contact493, operand W22/ORef23/RID175; W21 → OR358.in1, OR358.out W444 → RCoil362; operand W446/ORef413/RID43. 0619 RID43 Flag.M_MV03_OPEN AO79/BAD5 + 0618 RID5 Flag TOD2로 DB2.X9.7 해제다. OR 다른 가지는 수동Close/Auto이며, 요청 Reset은 알람Reset/현장복구가 아니다.
- 전체 개방식은 부모 재사용 근거: ON AND NOT MV03_FAULT AND [자동UP/수동Open/세정Open 합류] AND NOT 교정요청 AND NOT 처리Open. 자동/수동 가지는 PULSE OR ON을 포함한다. 부모의 상세 Part 목록을 반복 복제하지 않는다.
- 이 최종경로에서 반대 Q 접점은 확인되지 않았다. FG38 하드웨어 상대접촉기 NC31/32와 구분하는 기존 부모 정정을 유지한다.
- 0032 LAD1621 main NID8: ON Contact352(operand W350/ORef345/RID52, 0692 AO0=M0.0) → W353 CRef341.en. CodeBlock347/RID85는 0688 Valve Control loop FC14다. 호출과 내부 경로 모두 현재 CPU에서 실행된다는 증거는 아니다.

### 3.3 PID와 버너의 추가 읽기: 소유와 극성 분리

0479 LAD15 NID12, 제목 control pc02 moduling mv03 - not used:

- ORef532/RID127 → W551 → **NOT** Contact589 → W590 LRef507.LMNR_HS.
- 0671 RID113 CONT_S, NID12 UID507 Call; Instance546/RID104는 0665 PID_MV03 DB25. OFF Contact583(operand W547/ORef529/RID53) → W584 en. OFF는 0670 Memory AO1=M0.1 심볼이며 제목만으로 비활성 확정하지 않는다.
- 이 경로의 NOT는 0397 raw→처리 NOT와 별도 층이다. 현재 호출/활성·출력 쓰기 순서 없이 두 반전을 현장극성으로 일반화하지 않는다. PID 설정 전체·부모 UP/DOWN 다른 쓰기는 MV03 초안을 재사용한다.

0184 LAD1868 burner control NID14:

- State2 Eq1184.out → NOT Contact1642, operand W23/ORef24/RID231 → W22 Move1188.en; in W1518/ORef1396/RID113=Int3, out1 W1519/ORef1397/RID100=WorkData.BR01_State.
- 따라서 처리Open을 정접점으로 기다리는 식으로 역해석하지 않는다. 0585/0584 결속은 위 표와 같고 상태/상수는 0585 RID100 AO176/BAD47, 0584 RID47 WorkData TOD6 및 0586 Literal RID113 Int3다.
- 순서와 상태는 버너 블록 소유이며 LS19 고유 알람/타이머로 복제하지 않는다. 스캔 순서·현재 호출·연소안전·기구 정상성은 미확정이다.

### 3.4 다른 writer: 보존된 중지 블록의 정적 사실만

0403 LAD1083 simulation, NID2의 기존 원문을 읽기만 했다. Powerrail W21→Lt498.pre; in1 W76/ORef79/RID314=Data.Pot_MV03 Int, in2 W77/ORef80/RID253=Int98; out W75→Coil499, operand W550/ORef520/RID239=Inputs.MV03 open DB13.X7.5.

선언: 0635 RID314 AO1152/BAD247 + 0634 Data TOD1=DB1.DBW144. 0637 RID253은 Int Literal SV `_x0039_8`, V98. 이 **Pot_MV03<98** 비교 쓰기는 0397 raw 반전과 다른 원천이다. 98은 기존 블록의 상수이며 실제 개도·센서 설정·보호한계가 아니다. 생성·수정·실행·시뮬레이션 또는 행동시험을 수행하지 않았고 현재 활성/최종 writer라고도 하지 않는다. 간접주소/HMI/외부쓰기 전체를 열거한 결과가 아니므로 단일 writer 보장을 하지 않는다.

## 4. 전기 전달 경로 — 실제 PDF 4쪽 시각 검토

| 원본 / 인쇄FG / 실제PDF | 페이지별 판본·확인 |
|---|---|
| Electrical_Rev2 / FG39 / 40 | 기본일27.05.2024, 개정란 공란; LS19 NC11/12와 전선 끝점 확인 |
| Electrical_Rev2 / FG123 / 124 | 기본일27.05.2024, **Rev2 17.03.2025**; E7.5/단자36/LS19 확인 |
| PID_1684n002I / 1 | Apex I, 위 §1의 개정란·MV03 리더 확대 확인 |
| Electrical_Can_Decoating_20241118 / 56 of64 | CANDC-CONS-C006-056, D-PAGE6, Rev1 24.11.11 first draft design |

### 센서 공급부터 PLC까지

1. FG39 +24Vdc10.7 버스의 접속점 → X1/90, 5×20 2A F → 선39.3 → LS-19 **11–12 NC** → X1/91 → E7.5, 교차참조123/5.
2. FG123 E7.5의 반대 교차참조39/5 → **CPU515 MOD9 단자36**, 표제 LIMIT SWITCH LS-19.
3. 같은 페이지 모듈 전원은 +24Vdc10.7 → X21/3009 5×20 2A IST → 선123.1 → 단자39, −0Vdc10.6 → 단자40. 센서 퓨즈X1/90과 모듈공급X21/3009는 별개다.
4. LS20은 X1/92/93 E7.6 단자37, ZT04는 X1/85~89 별도 배선이다. LS19용 코일/독립PLC출력/별도 아날로그 입력을 만들지 않는다.

NC는 도면 기호와 번호의 해석이다. 현장 캠 눌림위치·기계 회전방향·접점 설치·단선시 동작·정상값·접지·현재 퓨즈 및 정격/보호설정은 확인하지 않았다. 2A 표기를 현장 교체규격 지시로 사용하지 않는다.

### 시공 케이블 고유 행과 결속 누락

| PDF56 행 | 케이블 ID | FROM→TO | 표기 |
|---|---|---|---|
|6_1|=FLA+MV03-FLO1TB1A|CR→MV-03 FLO1TB1 LS15/16/19/20|DC CVV12G1.0, spare3;100 LBD1→E100;Adjustment7,LEN44|
|6_15|=FLA+MV03-LS19A|MV-03 FLO1TB1→MV-03 LS-19|DC CVV2C1.0, spare0;LAD1 E300→LAD1→E1200;Adjustment5,LEN5|

공유 trunk와 LS19 branch는 다른 행이다. LEN은 설계길이이며 실제 측정치가 아니다. OEM X1/90/91과 FLO1TB1 내부 단자 번호를 서로 결속하는 상세는 이 표에 없다. 따라서 전 구간 준공 연속성 확인으로 합치지 않는다. 검게 가린6_7~6_10행은 근거로 사용하지 않았다. 별도 SEJIN 운영자료를 조사/변경한 것이 아니다.

## 5. 알람·복구 — 부모 소유와 센서 상태 분리

직접 검토한 LS19 가지에는 전용 LS19 fault S/R·전용 타이머를 확보하지 못했다. 원시/처리 불일치는 이미 NOT가 명시되어 있으므로 불일치만으로 고장판정을 하지 않는다. 추가 writer/호출조건도 함께 고려해야 한다.

부모 MV03 초안의 0159 LAD1226 NID1은 Qopen/close와 **접촉기 응답**을 비교하고 SD281 value W453/ORef384, 0571 RID83 **S5T#150S**, Tag94=T3를 거쳐 MV03_FAULT DB3.X4.3을 Set하는 공통근거다. LS19 종단 검출 지연 또는 150ms로 복제하지 않는다. 0351/0352 명령 누적 감시, ZT04 위치 OFR DB3.X25.0 역시 별도 부모/계측 경로이며 이번 LS19 의미검토 수에 포함하지 않는다.

처리Open에 의한 수동요청 RCoil362, 부모 fault reset, HMI 표시변경, ZT04 교정요청 해제, 물리 위치복구는 서로 다르다. 현재 fault 발생·복구 성공·안전 재기동을 확인하지 않았다. 리미트 우회/강제입력/점퍼/보호값변경/재기동·교정 실행을 이 문서로 지시하지 않는다.

## 6. 증상별 관찰 — 실행/조작 절차 아님

| 증상 | 승인된 기존 기록에서 확보할 읽기 전용 비교 | 성급한 결론 배제 |
|---|---|---|
| HMI 열림 표시와 실제 위치 불일치 | 같은시각 I7.5, DB13.X7.5, DB11.X22.3, 프로젝트ID·화면태그/갱신경로, 현 위치사진 | HMI가 raw 입력과 같은 주소/극성이라는 가정 금지 |
| 개방 명령이 사라짐 | 처리Open, 교정요청, Auto/수동/세정요청, 부모Fault, Q1.7과 접촉기응답 기록 | LS19만으로 모든 출력 조건 설명 금지 |
| 수동열림 요청이 유지 안 됨 | 0345 정접점493 및 Close/Auto OR 가지, DB2.X9.7 쓰기 시각 | 요청Reset=센서고장/현장복구 완료 아님 |
| 처리값이 raw 반전과 일치하지 않음 | 취득시각/스캔, 0030 호출, word/bit 쓰기 및 0403 포함 현재 writer 목록 | 즉시 배선·센서불량 확정 금지 |
| 버너 순서가 예상과 다름 | 0184 State2와 NOT 처리Open, 상태 이동시각, 현재 호출자료 | LS19만으로 연소안전/순서 정상 판단 금지 |
| 종단 근처 간헐 표시 | 승인된 준공도·캠/기계결합 자료·기존 위치별 입력기록, X1/90/91/FLO1TB1 구간 사진 | NC그림만으로 정상극성/채터·단선 원인 확정 금지 |

관찰 필드: 관찰자·시각/시간대·물리위치·태그사진·값/형식/단위·취득장치·현재 프로젝트 식별·비교원본·원인배제·승인 조치·이후 복구증거. 현장 신규 값·사진·운영 이력을 생성하거나 변경하지 않았다.

## 7. 완료·누락·다음 한 단계

| 영역 | 상태 | 경계 |
|---|---|---|
|설비·자료 기준|적용|LS19/MV03 문서상 연결, 실물 동일성 미확정|
|I/O·HMI|부분 적용|raw/word/반전/DB/기억 분리, HMI 호출 선언 미결속|
|제어|적용|8네트워크 중 관련 부분 정적검토, 현재 호출·최종값 미검증|
|전기|부분 적용|실제4쪽 시각확인, FLO1TB1 내부/준공 연속성 미확정|
|알람·복구|부분 적용|부모소유 분리, 센서 전용 알람 및 현장복구 미확보|
|증상 관찰|문서 적용|관찰표만 작성, 조작/시험 미수행|
|완료 기준|초안 complete_with_gaps|독립 검토·앱 통합·게시 완료 아님|

- documentation=complete_with_gaps; static_review=own_static_checks_passed(독립 검토 전); ui_records=not_run; publication=not_published; tia_compile/live_cpu/field_recovery=not_performed.
- 도면·래더 비교자료는 작성했다. 앱 내 백업·선택복원/전후비교/보고서·PDF 기능은 LS19용으로 구현하거나 시험하지 않았다. 기존 note/repair_observation/미지필드/저장키를 변경하지 않았다.
- 다음 필요자료: (1) LS19 명판·MV03 장착/캠·준공 P&ID, (2) X1/90/91↔FLO1TB1↔LS19 11/12 준공 단자 상세, (3) 현 프로젝트 식별·호출순서/다른쓰기/입력극성자료, (4) HMI 0369 동일문맥 선언과 DB11.X22.3 실제 표시경로, (5) 적격 담당자가 제공하는 위치별 원시/처리/표시 동시기록과 승인 복구결과.
- 통과기준은 이 자료로 각 물리·프로그램 끝점을 결속하고 실제 관찰 증거와 비교하는 것이다. 자료가 없으면 현장 보류를 유지하고 부모 전체 반복조사·새 시뮬레이터로 대체하지 않는다.

## 부록 A. 검사와 보존 범위

자체 XML 파싱/선언검색/PDF 렌더/해시·Gitblob 비교와 읽기전용 preflight만 수행했다. 네트워크8개는 0030/0032/0345/0369/0397/0403/0479/0184의 LS19 관련 부분이며 전체 네트워크 의미검토를 주장하지 않는다. 선언검색은 MV03 이름/멤버의 탐색이며 695 XML 전체 동작검토가 아니다. HMI 후보검색에서 다른 NID/형식의 RID451을 배제했다. 원본/중지5자산 보존 검사는 실행시험이 아니다. 아래 선정 전체표와 검사JSON의 검사수는 의미검토수·시각검토4쪽과 별도 집계다.

preflight는 inventory_matches=true. source_byte_changes는 requirements-audit.json/all-in-one-data.json 두 파일이며 고정 v1.12.0에서 대장 snapshot의 이전 해시와 다른 상태다. 이번 고정 Gitblob 비교는 두 파일 모두 일치하며, 그 차이를 이번 작업 원본 변경으로 오인하지 않는다. 대장 분류 불일치 없음.

검사시각 2026-10-11T13:50:13.479019+00:00; 선정 59파일 고정바이트 일치, 자체 정적단언 17개 통과. 원본 Git clean. 중지5자산 기준 SHA 일치. JSON: `extracts/LS19/SOURCE-SHA256.json`, `VALIDATION.json`, `preflight.json`.

## 부록 B. 선정 전체 SHA256 / 고정 Gitblob 표

| 원본 상대경로 | SHA256 | Git blob SHA1 | 고정바이트 |
|---|---|---|---|
| `.agents/skills/gme-equipment-rollout/SKILL.md` | `fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b` | `9aa820ea6ca15b4e136c9772423b78ed4df6a3d4` | 일치 |
| `.agents/skills/gme-equipment-rollout/references/source-map.md` | `40612c5efb8f94608840c7bc0e9095ea840df54920861c388ae48ea34c7998dc` | `49e50a7a8e56a16e2ec7f3607a03fd90adb8f1d3` | 일치 |
| `.agents/skills/gme-equipment-rollout/scripts/preflight.py` | `395067d6da20af3e1d82a43b7936907a87a44d8d2e11e4ebc61b1fc441e2adb6` | `170679427250c36c3a68cf6c5c2291ffe0341b10` | 일치 |
| `AGENTS.md` | `0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2` | `073164bc6efd5791032d62c71b03b4dab48cb6f8` | 일치 |
| `EXPANSION-WORK.md` | `ec624de9fd2fcfac861a67fd5e828b25ef46db50bfd7a37ff16e2cb54cd0f7e2` | `4c42d88ecc2d48269eb23e13a20ebf3721a092a1` | 일치 |
| `PUBLICATION_STATUS.md` | `efe4857aec598d90470322cf3962eb3fe1f64947630e1fdf71d1c90134de8740` | `d76401cf291fc0be681acc51fa898ad3ce46ff78` | 일치 |
| `VERSION.json` | `5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7` | `fffb51663b7705aec91cb119ca80ee943a4ce758` | 일치 |
| `WORKSPACE-HANDOFF.md` | `215096d997782e78e901dfae36c782937e49611fbeb677a0d3fa50cbecf8d074` | `dd0b8989d2376c4415bba9bd826fe6754c6b1a12` | 일치 |
| `all-in-one/ACTIVE-WORK.md` | `eff3bbc08ecff41da3beff77f3fec48e7d148708192bcaaab00f34b6a721afc2` | `6eb947c629b5ddf9c759ef87649451303938864b` | 일치 |
| `all-in-one/assets/program-model-data.js` | `52f8199371e3399b7c0d44ab5469f0472aced79d56bbef2887f7625f5d2aff0f` | `38f34b0caa380a16ccad6f6f1e234a2fdf23f327` | 일치 |
| `all-in-one/assets/simulator-workspace.js` | `3a6dfc618ff7e7b238f2671dc85d65704f33093a18eac879d86081d92c31e8bc` | `97c2c831c77a9699fff0e0960b3bc1b7d93d45b3` | 일치 |
| `all-in-one/assets/virtual-plc.js` | `5f1876052dc0067b1f010af0dfc941946e37003167481731293615d9c1c36dbc` | `0bd9eceb54365a91214a37c5601b5067c39a3f75` | 일치 |
| `all-in-one/registers/all-in-one-data.json` | `63a46b36b6454bf1246d093300dbee11f2fcc287ad94991405369bf9f939a8fe` | `15d62ac2a99c1c0eeb7579e03163f9c0319b50a4` | 일치 |
| `all-in-one/registers/equipment.json` | `7870325dff32bbca90fa34507b301c4aad3347d669fddcd03b910343663996fa` | `acc42633033398216469064932c4b76987371606` | 일치 |
| `all-in-one/registers/plc-symbols.csv` | `a0334b390f06ddb515d6c09ca96a01d35d44029c1b726ef0ff53303ec04ff91f` | `cbc576c5d6e47498a3865304a1c23de9b4641d9f` | 일치 |
| `all-in-one/registers/priority-equipment.csv` | `953c2c4df5b3a6e40d926d1f0f08f91900b7d6565e4dcd64191b548e438edeba` | `69c17fe3eb671e896ad15914c81fae7f307aebdf` | 일치 |
| `all-in-one/registers/program-model.json` | `6203479c086b15bada12ac9d7e37db9280234ec26f1ea6091d7211dc09a577c5` | `9860b10f008d3a5ae714be50d77b703dfec32f3a` | 일치 |
| `all-in-one/registers/requirements-audit.json` | `a10b773ff96e9b1c7a27cf409644c68d3eb59aedc5bcb5ca00199d602e63facb` | `69e45bb8fe1abbcd2ba4eeb65e2f4445a367e238` | 일치 |
| `all-in-one/registers/simulator-freeze.json` | `bb93c1994effc5609939ba566b7802ce7ed55154a7310f02379b308ac2c8c835` | `808ffac14dbd1b4a7d797fa6cd0d647635d90b47` | 일치 |
| `all-in-one/registers/virtual-plc-test-results.json` | `a6b389f797f9a8b5ffe6928b8420f55c4cc459a327b0b48d716079d2eca6dd64` | `757dd50e45184568facb8ff62900b39d3ce848d1` | 일치 |
| `all-in-one/sources/Electrical_Can_Decoating_20241118.pdf` | `3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd` | `0ee6b6f8361c5790864dbba4bbd9d55e8e7c08f8` | 일치 |
| `all-in-one/sources/Electrical_Rev2.pdf` | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` | `f610fd7c7ce14ae951b00cff57b969259bfb389d` | 일치 |
| `all-in-one/sources/PID_1684n002I.pdf` | `2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b` | `8c83a59fefd5b8b651ec3537ea4236a073f5e109` | 일치 |
| `all-in-one/sources/decoded-original/0030-FlgNet.xml` | `9252c9da764993de1edb8b2e44c46d6e9f9d4b6118e751a0dbeaa9ffd8ea721b` | `e74c70b751acdcdbc7a8b3b0c98aa773c2107cab` | 일치 |
| `all-in-one/sources/decoded-original/0032-FlgNet.xml` | `070bb8efa33d03b18add5da81d3f670a47c12b288076b7bfee11ac87fe6fa7e4` | `e31cf9aeecfbfc0c264921ac217cbd15479c1f34` | 일치 |
| `all-in-one/sources/decoded-original/0184-FlgNet.xml` | `a0a59597c73eb68e1cbdb2f41d640eabccfd05655c4e9c08624be6027974caf3` | `da94babe74df340b11b37560e94e04acfad1212a` | 일치 |
| `all-in-one/sources/decoded-original/0345-FlgNet.xml` | `b278a319d4d8cb8d157f449a2365445ff8f172245ebd2a468aa3ee79dba60f93` | `25656c8d9f39b8eccb67300905545b4cbcec2bfd` | 일치 |
| `all-in-one/sources/decoded-original/0369-FlgNet.xml` | `f64e35330b3816e761ce72575977878d5cad6317191297c2a64107629a611806` | `487c75b5e66b32d1f7dda78eb750abea855f365a` | 일치 |
| `all-in-one/sources/decoded-original/0397-FlgNet.xml` | `bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834` | `4ab8370493c4e28fc1eabeeebe2743d27f0c4021` | 일치 |
| `all-in-one/sources/decoded-original/0403-FlgNet.xml` | `77b03e38aa857ac8dd404f2f66a56256939b4e7924b41334a7981b86089c1e6b` | `4c806e31eb65f00cbb7870c72896ac26a8bc3dd3` | 일치 |
| `all-in-one/sources/decoded-original/0479-FlgNet.xml` | `112e55599a4dc705438c8c61b936da9a167c22d9bbd909eda11c45c9dc33e839` | `38df067a2f4f62edfba9c5027002feccb45e5142` | 일치 |
| `all-in-one/sources/decoded-original/0584-IdentXmlPart.xml` | `3bff6c478e594bf97bb1730971944e96b0b5e2407199420fe6567d5fe609ea5d` | `0f8dde829be66041bea79e40ccc4586d84ff1da7` | 일치 |
| `all-in-one/sources/decoded-original/0585-IdentXmlPart.xml` | `e36ec18aa4abebea8f9160254522bb51ff722eae804c5a469790f85f02939184` | `16574d37ef3ca61b59ba396c400e269ab1dd3440` | 일치 |
| `all-in-one/sources/decoded-original/0586-IdentXmlPart.xml` | `f16c4c68bde8a737372c219a10b21501653dfd3ba8c59bd84b60ae6d62da8250` | `266989c590cf52f82e1553f8626a209b8c0b6e0b` | 일치 |
| `all-in-one/sources/decoded-original/0617-IdentXmlPart.xml` | `10bcf85169cb2512f55acadaef299a3d46b4b4cecd88032d739cfeba23e94aa9` | `9527658ee6808be34bd513b1b2ebaf3a4a5a6f3e` | 일치 |
| `all-in-one/sources/decoded-original/0618-IdentXmlPart.xml` | `0c6762de9cdf0e294317f7463bea3d8e6df5673d333d9b1826ebd17a7ded044c` | `9eec0dbd8abde4aa7295f77b63ad473f895f274b` | 일치 |
| `all-in-one/sources/decoded-original/0619-IdentXmlPart.xml` | `85694bb5b696e31e6a1217431112e5b750516c4f94078d6e127d4394a8b80456` | `11f0502c84a1f319a21459a35c0dc1c6ce8e8f36` | 일치 |
| `all-in-one/sources/decoded-original/0623-IdentXmlPart.xml` | `4acd00406ea92466169e57e59fc90b0da4d9ec55fd19e2e96c9556e939cb83a6` | `13b3af0459c8e6069bb9b2f1b16454bf479e08dc` | 일치 |
| `all-in-one/sources/decoded-original/0624-IdentXmlPart.xml` | `24607c0827fbde428bccf8637ef4ae490798a69a7c2f3b87861d0749082d367a` | `02511fea47fc47981c101bba49dc40adde1cdcc3` | 일치 |
| `all-in-one/sources/decoded-original/0627-IdentXmlPart.xml` | `08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb` | `61ebc0abbb2ca160e11e1da400a3f14a397d8bc5` | 일치 |
| `all-in-one/sources/decoded-original/0628-IdentXmlPart.xml` | `9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd` | `170ca5c72599edc7ea7eefe651c3680ce325e76a` | 일치 |
| `all-in-one/sources/decoded-original/0629-IdentXmlPart.xml` | `67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972` | `058129bb01e27f7a6a0d0293f332d745e5bab74e` | 일치 |
| `all-in-one/sources/decoded-original/0634-IdentXmlPart.xml` | `af3fcb536a6270ffb9a19e5b3f2c284a38d67d465f5147961005c1c01d11299d` | `877d9e0734dc7f3e5a8cea789eeb58a208501f48` | 일치 |
| `all-in-one/sources/decoded-original/0635-IdentXmlPart.xml` | `1a057d686446a3fdab7ac61bb09bc543c52f49646c9ca71ac323c10fcdffe457` | `95bfcad59cfb0c12b573e9e8face4262d1e94622` | 일치 |
| `all-in-one/sources/decoded-original/0637-IdentXmlPart.xml` | `3fb68f57dbe2a877c4ad5aa1b3316810cf84958f2d13b5b1d7d321e0915271c7` | `cb1d7fb76aa2afd96eb46984cc1e71b77f36395c` | 일치 |
| `all-in-one/sources/decoded-original/0665-IdentXmlPart.xml` | `50e88d5f50f555151b35cfb17225e766c34ef6b490bd3a48e0a4e335fd17e3dd` | `ea4a8a5013081f648722c5ebbde3bb1366787990` | 일치 |
| `all-in-one/sources/decoded-original/0666-IdentXmlPart.xml` | `19a9ccb83ad7070d23726250870d0ca0c33d797ab9ffe679c9d2c0d109cc95e6` | `b6130b32498b6fee0d9e4db7a04dc79f785e1fbb` | 일치 |
| `all-in-one/sources/decoded-original/0668-IdentXmlPart.xml` | `2248e994a0a02cd37c5c5edaca199b3421068feea91e2e8616560e814ef9f6ed` | `fe0f30d1eaae37783b0f03cb090353b3a3de3600` | 일치 |
| `all-in-one/sources/decoded-original/0670-IdentXmlPart.xml` | `e56f3f0c4f2a86dd18578dedd4453915c2a51cd25e2cd9feced8538171a00841` | `b9466007b14e5c4f5d353dca5734401317e2dc03` | 일치 |
| `all-in-one/sources/decoded-original/0671-IdentXmlPart.xml` | `26cb51706305c372d512c19770648bb0dbb74df8bd2277b1e0da1b8c88cca293` | `e38a4e2c93ac8093e2b0b8e082a64688b5d9845e` | 일치 |
| `all-in-one/sources/decoded-original/0676-IdentXmlPart.xml` | `c58427c5b0ac6c11cdb52e4c6d0461c7b191fae81ccace191048e9f175fcec59` | `1ed67265f69796a4e659f9438e551068037f33a4` | 일치 |
| `all-in-one/sources/decoded-original/0688-IdentXmlPart.xml` | `ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda` | `463585759f1ecd94f32362b4fefb000a152f5773` | 일치 |
| `all-in-one/sources/decoded-original/0692-IdentXmlPart.xml` | `bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037` | `737785d03b5fad43c5b4d451955726d800edb1c0` | 일치 |
| `all-in-one/sources/decoded-original/network-map.json` | `c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60` | `424430b6b953e43138e5d0a18ca40c949e21cfa1` | 일치 |
| `all-in-one/sources/hmi_plc_tags.csv` | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` | `cf4c0650e7c7baac350dcb89909b808435704880` | 일치 |
| `docs/equipment-standard/INVENTORY.json` | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` | `587c3748ad9224718f95ba06463fee913dae231d` | 일치 |
| `docs/equipment-standard/START-GPT61.md` | `35769e3146ccd707fea2b81b67b30376b76a0a19c7e662fe2bb4fdd382306f94` | `0d08cab3678df7e2625251b641b138ef4956483b` | 일치 |
| `docs/equipment-standard/WORK-ITEM-TEMPLATE.md` | `4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586` | `e546f39535d2b589e80f97db869ac37ce4d05cfd` | 일치 |
| `docs/equipment-standard/WORK-STANDARD.md` | `05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99` | `f76a570cc73098632e08759b17934000f7e3a253` | 일치 |
