# CYL-CL10 공압 실린더 고유 원본 조사 초안

- 대상: CYL-CL10 한 개. 부모 PV03, phase2, component, parent_child_separate.
- 표준 GME-STD-1.0.0. 기준 source-mv06 고정 commit abcf31c5030bc7ef8749ed8e869a857f2387a28a / VERSION v1.12.0. 작성 2026-10-11 UTC.
- 범위: 읽기 전용 원본 조사와 이 MD 및 extracts/CYL-CL10만 작성. 부모 PV03 및 CYL-CL05 초안은 탐색색인·공통 근거로 재사용했다. 부모 전체의 알람/호출/공통 전원을 다시 조사하거나 자식 완료로 상속하지 않았다.
- 원본·공통 코드·대장·버전·게시·운영·PLC·현장·보호값·SEJIN 변경 없음. 시뮬레이터 작성·수정·생성·실행·행동시험, 원본 생성기와 앱 빌드 실행 없음. 업로드·전송·별도 Work/Codex 생성 없음.
- 실제 모델·추론 설정은 이 산출물에서 관측 미확인. 문서 초안과 현장 검증을 구분한다.

## 1. 설비·자료 기준 — 적용

### 고유 확인

INVENTORY.json catalog[210]의 CYL-CL10은 PV03 하위 공압 실린더다. CLIENT-CL10은 부모 없는 외부 연동 Rotex screen이며 다른 이름 공간이다. GME-CATALOG-OVERLAP-REVIEW.json catalog_rows의 CYL-CL10은 physical_identity_verified=false, confirmed_alias_duplicate=false다. 대장 별도 ID가 독립 PLC 출력/센서 소유 또는 현장 실물 확인을 뜻하지 않는다. 하위 EV06의 independent-manual excluded 상태도 유지한다. 본문 EV06은 CL10에 이르는 전달 경로의 증거로만 사용한다.

PID_1684n002I.pdf 실제 PDF1의 PV-03 Detail을 직접 회전·확대 렌더했다. COMPRESSED AIR→EV-06 뒤 공압선이 CL-09와 CL-10 도식으로 분기한다. CL10은 상세도 아래쪽 실린더다. LS-10/LS-09의 리더는 위쪽 CL09 도식 양쪽 위치를 가리킨다. 아래 CL10에는 별도 LS 번호 리더가 보이지 않는다. **LS10과 CL10의 숫자10은 독립 센서 소유를 입증하지 않는다.** CL10의 실제 위치를 LS10만으로 확인했다고 쓰지 않는다.

P&ID의 병렬 도식은 공통 EV06 구동관계를 입증하지만, 양 실린더 동기 이동·로드 결합·설치 방향·기계적 공통 축·포트별 배관·스풀/복귀 방식·안전 위치는 입증하지 않는다. CL10 모델·보어·스트로크·압력·정비 주기·토크는 미확보다. 현장 표찰/명판·설치도·튜브 양 끝점 자료가 필요하다.

### 판본과 실제 페이지

| 원본 | 이번 실제 렌더·시각검토 | 페이지별 판본 |
|---|---|---|
| all-in-one/sources/PID_1684n002I.pdf | PDF1 및 PV03 상세/제목 확대 | Drawing1684n002, Apex I, 기본06/04/2011, 변경I 15/01/2013, FG ‘−’ |
| all-in-one/sources/Electrical_Rev2.pdf | PDF74=FG73 | 기본27.05.2024, 개정란 공란 |
| 같은 PDF | PDF127=FG126, PDF142=FG141 | 각각 기본27.05.2024, Rev2 17.03.2025 |
| all-in-one/sources/Electrical_Can_Decoating_20241118.pdf | PDF34/64=CANDC-CONS-E017-034, D-PAGE17; PDF59/64=CANDC-CONS-C009-059, D-PAGE9 | 각각 No.1 24.11.11 first draft design, APPROVED 공란 |

RD01-PV03-DOTS-CORRECTIONS-20261011.md의 FG141 Rev2 정정을 반영했으며 직접 footer도 재확인했다. 파일명 Rev2를 FG73에 일괄 적용하지 않는다. 시공도는 참고 설계이며 준공·승인·현행 결선으로 승격하지 않는다.

기존 devices/CYL-CL10.html의 직접 I/O·내부·HMI·래더0은 이름 기반 미식별 상태다. 해당 페이지의 과거 SIM 설계·미실행 이력은 보존하고 최신 영구 금지 지침을 우선한다. 실행 또는 새로운 시험 설계에 사용하지 않았다.

## 2. I/O·HMI — 부모 연관 적용 / 독립 소유 미확보

XML 경로 약기는 all-in-one/sources/decoded-original/이다. 아래는 백업의 PV03 공유 구동군이며 CL10 전용 목록이 아니다. 모든 행 Bool, AO는 비트 오프셋이다.

| 신호 | 백업 주소 | 선언·사용 결속 | 경계 |
|---|---|---|---|
| PV-03 GATE EV | Q5.6 | 0602 RID195 SAD Output AO46, NID42 UID1153 Write; 0607 RID145 NID15 UID33/36/38/41 Read | EV06→CL09/10 공통 명령 |
| Deviator Open PV-03 | I10.2 | 0607 RID146 SAD Input AO82, NID15 UID34 | OEM LS09, CL10 독립 위치 아님 |
| Deviator Close PV-03 | I10.3 | 0607 RID148 Input AO83, NID15 UID39 | OEM LS10, P&ID 리더는 CL09 |
| Inputs.Deviator Open/Close PV-03 | DB13.DBX10.2/10.3 | 0609 RID154/151 AO82/83 BAD86; 0608 Inputs RID86 TOD13; NID15 UID78/64 | raw와 별도 처리값 |
| Flag.M_PV03 | DB2.DBX11.2 | 0604 RID193 AO90 BAD2; 0603 Flag RID2 TOD2; NID42 UID1150/1151. 기억부는0609 RID153 BAD5 NID15 UID81/74 | 요청, 센서 아님 |
| Inputs.PV03 Local Selector | DB13.DBX10.4 | 0604 RID256 AO84 BAD218; 0603 Inputs RID218 TOD13; NID42 UID1152 | 부모 local 선택 처리값 |
| Flag.PV_03_GATE_MEM_OPEN/CLOSE | DB2.DBX9.1/9.0 | 0609 RID147/149 AO73/72 BAD5; 0608 Flag RID5 TOD2; NID15 UID35/37 및40/42 | 부모 위치 기억, 실물 아님 |
| ON / OFF | M0.0 / M0.1 | 0602 RID1/33 Memory AO0/1; NID42 UID1148/1149. 기억부 ON은0607 RID1 NID15 UID32 | 명칭이 ON/OFF인 메모리, 상수 아님 |

hmi_plc_tags.csv의 PV_03 전용 설정5개를 직접 읽었다: Flag=DB2,X11.2(00072), LS_Open=DB11,X80.0(00070), LS_Close=DB11,X80.1(0006F), Allarme1=DB11,X80.3(0006E), Selector=DB11,X80.2(0006D). CL10 전용 HMI 설정/조작 이벤트는 확보하지 못했다. 부모 PV03 §2.4의 LAD1217 호출9실인수 미결속을 유지한다. CSV 일치는 현재 통신·화면 이벤트·raw/MEM 결속 또는 CL10 독점 소유의 증거가 아니다.

부재 검색: decoded-original XML695개에서 정규식 (?:CYL[-_ ]*)?CL[-_ ]*10\b, 대소문자 무시로 검색해0건. 검색 파일수·패턴·결과는 cl10-xml-search.json에 기록했다. 이는 이름 검색 범위의 결과로서 별칭으로 존재할 모든 신호의 부재를 증명하지 않는다. 695 검색을695 의미검토로 집계하지 않는다.

## 3. 제어 구조 — 부모 전달 경계 적용

### 출력과 요청 Reset 직접 확인

0272-FlgNet.xml, LAD1972, motors1, 원본 선언 NID42(색인 index_order43과 구분):

Q5.6 = ON AND (M_PV03 OR Inputs.PV03 Local Selector).

- Part1164 Contact operand W1154/ORef1148→0602 RID1. out W1165가 OFF1166, 요청1168, local1170의 in으로 분기한다.
- Contact1168 operand W1158/ORef1151→0604 RID193, out W1169→OR1144.in1.
- Contact1170 operand W1159/ORef1152→0604 RID256, out W1171→OR1144.in2.
- OR1144(Card2).out W1160→Coil1147.in; operand W1162/ORef1153→0602 RID195 Q5.6.
- OFF1166 operand W1155/ORef1149→0602 RID33; out W1167→RCoil1141.in; operand W1157/ORef1150→0604 RID193. ON AND OFF에서 M_PV03 Reset이다.
- 이 네트워크에는 CRef 호출이 없고 CL10 독립 닫힘 코일도 없다. OFF가 요청을 Reset해도 local OR 가지가 남으면 출력이 반드시 꺼진다는 뜻이 아니다. 부모 전체 공정의 보호/인터록 부재로 확대하지 않는다.

물리 전달은 Q5.6→73KA1→EV06→CL09/CL10 공압 분기다. Q=0을 CL10 닫힘·잔압 소거·접근 안전으로 치환할 근거가 없다.

### 부모 기억이 CL10 실위치를 대신하지 못하는 이유

0290-FlgNet.xml LAD1925/r1 scraps gate2/NID15도 직접 확인했다.

| 쓰기 | 접점·핀 경로 | 정적 의미 |
|---|---|---|
| MEM_OPEN Set | ON21 out W45→Q22; Q22 out W75→Contact23/77/80; out W85/83/84→OR82.in1/2/3; out W86→SCoil24; operand W50/ORef35→RID147 | ON AND Q AND (raw Open OR Inputs.Open OR M_PV03) |
| MEM_OPEN Reset | NOT Q Contact25→W52→RCoil26; operand W53/ORef37→RID147 | ON AND NOT Q |
| MEM_CLOSE Set | ON→NOT Q27 out W55→Contact28/63/NOT69; out W57/66/72→OR65.in1/2/3; out W67→SCoil29; operand W58/ORef40→RID149 | ON AND NOT Q AND (raw Close OR Inputs.Close OR NOT M_PV03) |
| MEM_CLOSE Reset | Q30→W60→RCoil31; operand W61/ORef42→RID149 | ON AND Q |

열림 입력 operands는 W48/ORef34/RID146, W76/ORef78/RID154, W79/ORef81/RID153. 닫힘은 W56/ORef39/RID148, W62/ORef64/RID151, W73/ORef74/RID153이며 Contact69만 요청에 Negated가 있다. Q operands33/36/38/41은0607 RID145, ON32는RID1이다. 해당 경로에 CRef 호출은 없다.

요청/NOT 요청만으로 기억 조건이 성립할 수 있는 정적 구조이므로 MEM 정상은 LS 정상·CL09 위치·CL10 위치를 입증하지 않는다. 현행 CPU에서 실제 우회가 발생했다는 판정은 아니다. 부모 startup 닫힘 기억 Set, Word 전달/호출/다른 쓰기 경계는 PV03 §2.3·3.3을 공통 참조한다. 이번에 전체 호출과 모든 쓰기를 다시 검증한 것으로 세지 않는다.

## 4. 전기·공압 끝점 — 부모 연관 적용 / CL10 전용 끝점 미확보

실제 도면의 접속점·교차를 확인했다. FG141/PDF142 CPU515 MOD15 terminal17 A5.6→교차73/3→FG73/PDF74 73KA1 A1, A2→−0Vdc10.6. A2선은0Vac9.9를 지나지만 그 교차에 접속점이 없고 −0Vdc10.6에는 점이 있다. 모듈 공급은 +24Vdc10.9→X21/3033 5×20 4A F→141.1→terminal19, terminal20→−0Vdc10.6이다. 현재 CPU 모델·전압·보호기 확인이 아니다.

EV06 부하는 별도110Vac 회로다: 110Vac9.7→73KA1 접점5–9→73.1→X1/156(5×20 2A F)→73.2→EV06 A1→A2→X1/157→0Vac9.9. 상단 미연결1단자 및 하단 접점표1/5/9를 부하1–9로 읽지 않는다. 기존 PV01 69KA/PV02 71KA의5–9 정정도 보존하며 이 CL10 전달에는73KA1만 직접 연결한다.

부모 위치 입력:
- OPEN: +24Vdc10.7→X1/158(2A F)→73.3→LS09 13–14→X1/159→E10.2→FG126/PDF127 MOD10 terminal23.
- CLOSE: +24Vdc10.7→X1/160(2A F)→73.4→LS10 13–14→X1/161→E10.3→FG126 terminal24.
- PB17: +24Vdc10.7→X1/162(2A F)→73.5→73SA1 13–14→X1/163→E10.4→FG126 terminal25.

전기상 LS09/10 명칭은 DEVIATOR OPEN/CLOSE이며 P&ID 리더는 CL09 쪽이다. 접점13–14 그림을 실제 정상 극성이나 안전 등급으로 확정하지 않는다. X1 단자를 CL10 전용 단자로 재명명하지 않는다.

### 시공자료 교차와 공백

PDF34 도해 EXI1TB1→EXI1TB3→LS09/LS10/EV06, 별도PB17을 확인했다. PDF59 Cable Schedule(8)은 다음과 같다.

| 케이블 | 양 끝점 / 사양 | 경계 |
|---|---|---|
|9_4 =EXI+PV03-EXI1TB3A|EXIT EXI1TB1→PV03 EXI1TB3, DC CVV12G1.0|LS09/10/11/12 표기 공통 간선|
|9_5 =EXI+PV03-EXI1TB3B|EXIT EXI1TB1→PV03 EXI1TB3, AC CVV3G1.0|EV06 공통 부하 간선|
|9_9 =EXI+PV03-LS09A|PV03 EXI1TB3→LS09, DC CVV2C1.0, E361|CL10 전용으로 소유 안 함|
|9_10 =EXI+PV03-LS10A|PV03 EXI1TB3→LS10, DC CVV2C1.0, E362|숫자10 대응 금지|
|9_13 =EXI+PV03-EV06A|PV03 EXI1TB3→EV06, AC CVV3G1.0, E362|CL09/10 공유 구동|
|9_11/9_12 =EXI+PV03-LS11A/LS12A|PV03 EXI1TB3→LS11/LS12, DC CVV2C1.0, route공란|선정 OEM/P&ID에서 대응 CL10 위치 근거 미확보|

시공표에 LS11/12 행이 있다고 CL10에 붙는 두 센서로 채우지 않는다. PDF34에는 LS09/10/EV06만 그려져 있고 원본 FG73도 두 리미트다. 현장 설치 여부와 개정 차이를 확인할 자료가 필요하다. PDF59 PB17의68.4/E8.5와 OEM73SA1/E10.4 상충은 유지한다. 부모에서 보고한 FG244 전면68SA1은 기존 공통 근거이며 이번 직접 렌더 범위는 아니다.

OEM X1/156~163↔EXI1TB3 개별 단자·심선 일대일 결속표 미확보. EV06 공압 포트↔CL10 두 챔버 튜브 번호도 없다. 전기 케이블표로 공압 끝점 공백을 해결하지 않는다. 도면2A F/4A F는 현재 교체·설정 권고가 아니다.

## 5. 알람·복구 — 부모 참조 적용 / 독립 항목 미확보

CL10 고유 알람 선언·타이머·복구 시퀀스 근거는 확보하지 못했다. 부모 PV03 §5의 LAD1819/0453 및0655~0658 선언에 근거한 T111/T112, S5T#5S 도달 감시와 Reset을 공통 참조한다. 이번에 해당 알람 XML 의미검토를 반복한 것으로 집계하지 않는다. 이5초를 CL10 독립 알람으로 복제하거나 인접 LIW의15분과 합치지 않는다.

부모 감시가 MEM을 사용한다는 공통 근거와 이번 직접 확인한 MEM의 요청 OR 구조 때문에, 알람 없음/기억 정상만으로 CL10 정상 이동을 승인할 수 없다. EV06·릴레이·공압 공급·CL09/10·게이트 기구·부모 LS/처리/기억을 분리해야 한다. Reset은 기계 원인 해제·CL10 실물 복구와 다르다. 강제출력·접점 우회·타이머 연장·반복 Reset을 처방하지 않는다.

## 6. 증상별 관찰 — 적용, 실제 수리 미수행

아래는 승인된 자격자가 격리·잔압·중력/끼임 위험 통제 절차 아래 수집할 자료다. 통전·접근·운전 지시가 아니다.

| 증상 | 동일 시각에 구분해 관찰할 근거 | 오판 방지 |
|---|---|---|
| CL10 움직임 없음 | 요청/local→Q5.6→73KA1 제어/5–9 부하→EV06 전원→공압 분기→CL10 실제 위치 | Q1을 전압/압력/이동 완료로 간주하지 않음 |
| CL09는 움직이나 CL10 불명 | 두 실물 표찰·위치, 튜브 양 끝점, 승인된 기계 링크 자료 | 공통 EV 하나만으로 동기성 단정 금지 |
| LS09/10 또는 MEM은 정상 | raw I10.2/10.3, DB13 처리, M_PV03, DB2 기억, CL09와 CL10 실물 위치 | LS10을 CL10 센서로 오인하지 않음; 요청 OR 기억을 실물로 대체 금지 |
| M_PV03 해제 후 출력 유지 | ON, OFF, Inputs local, Q를 비교 | local OR 가지를 먼저 분리하고 고착이라고 단정하지 않음 |
| 부모 도달 알람 발생/없음 | 부모 MEM·타이머·알람과 두 실물 관찰을 별도로 비교 | 부모 알람을 CL10 고유 진단/복구 판정으로 복제 안 함 |
| 출력0 이후 상태 불명 | Q·EV 전원과 현행 공압회로·비접촉 위치 관찰 | 닫힘/무압/접근 안전을 추정하지 않음 |

관찰 기록: 관찰자·시각/시간대·CL10/CL09 표찰 위치·프로젝트 식별·값/단위와 미측정 빈칸·수집장치·승인 자료·비교 FG/PDF/LAD/Part·배제 결과·승인 조치·개별 복구 확인자. 실제 운영기록/사진을 생성·복제하지 않았다.

## 7. 완료·누락·인계 — 문서 초안

| 영역 | 적용 상태 | 남은 자료 |
|---|---|---|
|설비·자료 기준|적용|CL10 표찰·명판·설치도, 실물 동일성|
|I/O·HMI|부모 연관 적용 / 전용 근거 미확보|현행 프로젝트·실인수·이벤트, 전용 센서 존재 여부|
|제어|부모 전달 경계 적용|현재 CPU 실행·다중쓰기·기억과 실물 비교|
|전기·공압 끝점|부모 연관 적용 / 직접 끝점 미확보|X1↔EXI1TB3 단자/심선, EV06↔CL10 튜브/포트|
|알람·복구|부모 참조 적용|CL10 고유 진단 근거, 원인 해제·실물 복구 증거|
|증상 관찰|적용|승인된 관찰값·실제 조치/결과|
|완료 기준|적용|독립 검토·UI/기록·통합·게시·현장 검증|

모터 속도/전류/PID·엔코더 교정은 이 실린더 직접 기능으로 비해당이다. 공압 모델·압력·정비 정보는 비해당이 아닌 미확보다.

네 기능: 도면·래더 비교(이번 정적 원본 연결), 백업·선택 복원, 기록 전후 비교, 관찰 보고서/PDF는 적용 후보이며 구현/저장/재읽기/재열기/UI 검증은 모두 not_run이다. 원본 PDF 렌더는 보고서 생성/UI 검증과 다르다. 기존 note/repair_observation·미지 필드·타설비·초안·저장 키를 보존하고 saved_with/generated_with를 관찰 당시 CPU 증거로 소급하지 않는다.

| 최종 상태 | 결과 |
|---|---|
|documentation|complete_with_gaps 초안|
|static_review|선정 원본 바이트 및 지정 XML/PDF 정적 대조 완료, 독립 검토 대기|
|ui_records|not_run|
|publication|not_published|
|tia_compile / live_cpu / field_recovery|모두 not_performed|

다음 한 작업: 검토자가 CL10 고유 공압 분기, CL09 쪽 LS 리더와 CL10 관찰 공백, 부모 기억 요청 OR 및73KA1 접점5–9/리턴, 페이지별 개정과 선정 해시를 독립 확인한다. 새 현장 자료 없이 정상 극성·보호값·현장 복구 완료를 채우지 않는다.

## 부록 A. 수행·검증 범위

- 직접 의미검토: PLC XML8개(0272/0290 및0602/0603/0604/0607/0608/0609의 관련 선언·핀), PDF3파일 실제6페이지(PID1;OEM74/127/142;시공34/59), HMI CSV1개. 대장/지침/기존 HTML/색인은 별도 배경 확인이다.
- PDF 실제6쪽 렌더에 PID 상세/제목 확대2개를 더한 PNG8개. 각 원본 페이지 텍스트6개도 자신의 추출 폴더에 보관했다.
- 이름 검색695 XML0건은 의미검토 수가 아니다. 해시 검사25파일도25개 전체 의미검토를 뜻하지 않는다.
- selected-xml.txt는 직접 원본에서 추출한 선언과2개 네트워크 전문이다. network-selection.json은 탐색색인2행이며 단독 의미 근거로 사용하지 않았다.
- 원본 고정 HEAD 확인, Git status clean. 자체 읽기 전용 해시/바이트 검사 종료0. 원본 스크립트/생성기/앱빌드/preflight는 실행하지 않고 대장 지정행을 직접 읽었다.
- source-integrity.json: 선정25파일 SHA256 및 고정 Gitblob 바이트25/25 일치. 이 검사는 현재 CPU/실물 동일성 증거가 아니다.
- 조사 초기 source-mv06를 루트에서 찾지 못한 읽기 실패 후 gme-research/source-mv06 경로를 확인했다. 원본 변경이나 실패 은폐 없이 경로를 바로잡았다.

공통 파생 참조: PV03-DOTS-DRAFT.md, RD01-PV03-DOTS-CORRECTIONS-20261011.md, CYL-CL05-DOTS-DRAFT.md, BATCH20-RESEARCH-INSTRUCTIONS.md, TASK3-BATCH20-SCOPE.json, GME-CATALOG-OVERLAP-REVIEW.json. 이 파일은 고정 Gitblob 원본으로 위장하지 않는다.

## 부록 B. 선정 모든 원본 SHA256 및 고정 Gitblob 바이트 확인

MD 표와 extracts/CYL-CL10/source-integrity.json은 같은25파일 검사 결과다.

| 원본 경로(source-mv06 기준) | SHA256 | 고정 Gitblob OID | 바이트 일치 |
|---|---|---|---|
| AGENTS.md | 0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2 | 073164bc6efd5791032d62c71b03b4dab48cb6f8 | True |
| .agents/skills/gme-equipment-rollout/SKILL.md | fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b | 9aa820ea6ca15b4e136c9772423b78ed4df6a3d4 | True |
| docs/equipment-standard/WORK-STANDARD.md | 05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99 | f76a570cc73098632e08759b17934000f7e3a253 | True |
| docs/equipment-standard/WORK-ITEM-TEMPLATE.md | 4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586 | e546f39535d2b589e80f97db869ac37ce4d05cfd | True |
| docs/equipment-standard/INVENTORY.json | 720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc | 587c3748ad9224718f95ba06463fee913dae231d | True |
| VERSION.json | 5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7 | fffb51663b7705aec91cb119ca80ee943a4ce758 | True |
| WORKSPACE-HANDOFF.md | 215096d997782e78e901dfae36c782937e49611fbeb677a0d3fa50cbecf8d074 | dd0b8989d2376c4415bba9bd826fe6754c6b1a12 | True |
| PUBLICATION_STATUS.md | efe4857aec598d90470322cf3962eb3fe1f64947630e1fdf71d1c90134de8740 | d76401cf291fc0be681acc51fa898ad3ce46ff78 | True |
| all-in-one/ACTIVE-WORK.md | eff3bbc08ecff41da3beff77f3fec48e7d148708192bcaaab00f34b6a721afc2 | 6eb947c629b5ddf9c759ef87649451303938864b | True |
| EXPANSION-WORK.md | ec624de9fd2fcfac861a67fd5e828b25ef46db50bfd7a37ff16e2cb54cd0f7e2 | 4c42d88ecc2d48269eb23e13a20ebf3721a092a1 | True |
| all-in-one/devices/CYL-CL10.html | 8514754e1729c977afc6b709cdb3f1d753cccd3415debaad4960ee70913b4313 | 059f8c3e64a564d131a8c480659b7465134ba54a | True |
| all-in-one/devices/CLIENT-CL10.html | af32ced8f1114d6b52c221d17db8965fb4545250e3365e136c45868ad7727ae3 | 42c7e6cb86c4dccf3b8bb1d5f3982b13d4069778 | True |
| all-in-one/sources/PID_1684n002I.pdf | 2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b | 8c83a59fefd5b8b651ec3537ea4236a073f5e109 | True |
| all-in-one/sources/Electrical_Rev2.pdf | 5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6 | f610fd7c7ce14ae951b00cff57b969259bfb389d | True |
| all-in-one/sources/Electrical_Can_Decoating_20241118.pdf | 3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd | 0ee6b6f8361c5790864dbba4bbd9d55e8e7c08f8 | True |
| all-in-one/sources/hmi_plc_tags.csv | a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404 | cf4c0650e7c7baac350dcb89909b808435704880 | True |
| all-in-one/sources/decoded-original/network-map.json | c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60 | 424430b6b953e43138e5d0a18ca40c949e21cfa1 | True |
| all-in-one/sources/decoded-original/0272-FlgNet.xml | 654fbd1c537044693d242b4d806ea8304db9bd83f2655b2566468812103c3357 | bc961d4d53cb324d92159d6c455d770b7cb87304 | True |
| all-in-one/sources/decoded-original/0290-FlgNet.xml | 616ae571a3a19d97d71137ac539cc6e5c8b1db13b0e2b78ae8c1f9401098bc0f | 2383f3b0c4a515bf25f7d0656a3bf61acbc81803 | True |
| all-in-one/sources/decoded-original/0602-IdentXmlPart.xml | 46ab21151eddaaf616469db520730c60423eb742aa491af194e6710c751b4caf | bcb12ab1ce8c476ff921baa1608f29d9822f76b4 | True |
| all-in-one/sources/decoded-original/0603-IdentXmlPart.xml | e93969dfa281d75b49b24127793068e33472dadb19729c1c48fc4a8dad075ef8 | 3a92b304baf4dbf6147e944d9778d2da11285cb1 | True |
| all-in-one/sources/decoded-original/0604-IdentXmlPart.xml | b798d29c5499b5314a1ee3cff9139dae64c887533b86baa43b6e9a052373a6af | bb2c318788b97e7a4924a176275c12d805aa519d | True |
| all-in-one/sources/decoded-original/0607-IdentXmlPart.xml | 9b76b53536a26e7b45961fecbf825ae1552e16c2fd9af5736864193c01d77f93 | dbd4da513171f04cca9b1c1741d0293c3e38f98c | True |
| all-in-one/sources/decoded-original/0608-IdentXmlPart.xml | 24adec2035b65c0c310d637bcea74374896875b6465a16aa2f2cfc8fd55fa4b8 | cea8f4160d2da00023b1ecc5e591b561e4a08330 | True |
| all-in-one/sources/decoded-original/0609-IdentXmlPart.xml | 395de8ebb2168848cf96fe015bd7334d71107c114a4e441ef36346b8f22031db | ee2aab34c0116642dd9f4364b236426f78a876a3 | True |
