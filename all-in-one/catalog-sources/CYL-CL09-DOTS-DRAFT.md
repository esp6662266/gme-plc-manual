# CYL-CL09 공압 실린더 — 고유 원본 조사와 7영역 초안

- 작업: 작업3번 20차, phase2 고유 하위 구성품 1개. 작성일 2026-10-11 UTC.
- 기준: GME-STD-1.0.0, `source-mv06` 고정 커밋 `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, 프로그램 v1.12.0. 원본 Git 상태는 조사 시작과 종료에 clean 확인. 현재 CPU나 이 실린더의 게시 버전이라는 뜻이 아니다.
- 읽은 지침: AGENTS.md, 저장소 gme-equipment-rollout/SKILL.md, WORK-STANDARD.md, WORK-ITEM-TEMPLATE.md, INVENTORY.json, VERSION/WORKSPACE-HANDOFF/PUBLICATION_STATUS/ACTIVE-WORK/EXPANSION-WORK 최신 상단, BATCH20-RESEARCH-INSTRUCTIONS와 TASK3-BATCH20-SCOPE 및 중복 검토 해당 행.
- 부모 PV03 초안과 CYL-CL01~05 계열의 공통 조사 방식은 탐색색인으로 재사용한다. 부모 전체 조사를 반복하지 않고 CL09 고유 도식·리더·상위 출력/응답의 선택 원본만 직접 대조했다. 이 문서는 부모나 형제 실린더 완료를 상속하지 않는다.
- 수정 범위: 이 초안 및 `extracts/CYL-CL09/`만. 원본·공통코드·대장·버전·배포·운영/사용자 기록·보호값·PLC·SEJIN 변경 없음. 시뮬레이터 작성·수정·생성·실행·행동시험, 앱 빌드·원본 생성기 실행 없음. 분석 스크립트는 XML/JSON/PDF 정적 읽기 및 선정 해시 비교만 수행했다.
- 실행 모델/추론 수준의 실제 선택값은 이 문서에서 검증하지 못했다. 자체 정적 검토 결과이며 독립 검토는 인계 후 필요하다.

## 핵심 결과

1. P&ID 실제 PDF1의 PV-03 Detail에서 EV06 공통 분기가 CL09와 CL10 두 실린더 기호에 이어진다. CL09는 위쪽 기호이며 LS10 리더는 몸체 쪽, LS09 리더는 로드 쪽이다. 이 도식이 실제 설치위치·정상극성·기계 행정을 입증하지는 않는다.
2. CL09 전용 출력/코일/알람은 확보하지 못했다. 백업 Q5.6은 PV03/EV06의 공통 구동 출력이다. 이름이 같은 숫자인 CLIENT-CL09 외부 모터와 구분한다.
3. PV03 위치 기억 Set에는 센서 외에 요청 M_PV03/NOT M_PV03 가지가 있다. MEM_OPEN/CLOSE나 HMI 표시만으로 CL09 또는 CL10 실제 이동 완료를 판정하지 않는다.
4. 실제 렌더한 FG73/PDF74의 EV06 부하 접점은 73KA1 **5–9**다. 24Vdc PLC 릴레이 제어와 110Vac EV06 부하, EV06 이후 공압 실린더 경계를 구분한다. 기존 69KA/71KA 5–9 정정을 되돌리지 않는다.

## 1. 설비·자료 기준

### 1.1 분류와 소유 경계

`docs/equipment-standard/INVENTORY.json#/catalog/209`: CYL-CL09, 공압 실린더, component, 하위 구성품, parent_id=PV03, depth=1, phase=phase2, priority_key=null, queue_state=planned, existing_detail=baseline, bc01_standard_acceptance=not_assessed. `all-in-one/registers/equipment.json`의 index204는 parent=PV03, pid=true, fgs=[], aliases=[], “외부 모터 CLIENT-CL09과 별개다”라고 한다. 이 분류가 실물 동일성 확인서는 아니다.

중복 검토 및 20차 범위 행은 parent_child_separate, physical_identity_verified=false, confirmed_alias_duplicate=false다. 부모와 별도 문서 대상이나 독립 PLC 소유라는 뜻은 아니다. LS09/LS10도 부모 PV03 하위 센서이며 번호 일치로 CL09 자체와 병합하지 않는다. EV06 독립 작성 제외는 유지하고 여기서는 전달 끝점으로만 참조한다.

### 1.2 고유 P&ID 직접 관찰

`all-in-one/sources/PID_1684n002I.pdf` 실제 PDF1, 도번1684n002, 표제 UBC AND SCRAPS DECOATER 10 Ton/h / P&I, Apex I, 개정 I 15/01/2013, 기본06/04/2011, FG ‘–’. 자체 렌더 `PID-p1.png`, `pid-detail.png`, `pid-title.png`로 확인했다.

- COMPRESSED AIR→EV-06→두 실린더 도식 CL-09/CL-10가 연결된다. CL09와 CL10를 PV01/PV02의 A/B 별도 출력 구성으로 바꾸지 않는다.
- LS-10 리더는 CL09 몸체 쪽 끝점, LS-09 리더는 로드 쪽 끝점에 이어진다. 아래 CL10 기호에는 별도의 센서 리더를 확인하지 못했다. 이로부터 실제 CL10에 센서가 없다고 확정하지 않는다.
- 상세 박스 아래 분기 기구 스케치는 링크 형태 참고다. 두 실린더와 개별 기계 장착지의 일대일 실물 대응·호스/포트 번호·연동 기구 치수는 미확보다.
- 주공정 PV03는 VS01 하류 분기 위치에 표시된다. P&ID는 2013년, 전기도면은 기본2024년/일부2025년 개정이므로 자동으로 같은 시점의 승인 준공 상태라고 보지 않는다.

## 2. I/O·HMI

XML 약칭 `NNNN`는 `all-in-one/sources/decoded-original/NNNN-IdentXmlPart.xml` 또는 명시한 FlgNet이다. 주소는 SSD AO 비트 오프셋+SAD 영역 또는 BAD→DepDBBlock TOD로 대조했다. 아래는 백업 자료이며 현재 CPU 주소/값 검증이 아니다.

| 신호 | 선언·NID·UID | 백업 주소/형식 | CL09에 대한 의미 |
|---|---|---|---|
| PV-03 GATE EV | 0602 RID195, Output AO46; NID42 UID1153 Write. 응답망은0607 RID145, NID15 UID33/36/38/41 | Q5.6 Bool | EV06 공통 출력, CL09 전용 아님 |
| Deviator Open PV-03 | 0607 RID146, Input AO82; NID15 UID34 | I10.2 Bool | 전기 LS09 응답; CL09 독립 행정 측정값 아님 |
| Deviator Close PV-03 | 0607 RID148, Input AO83; NID15 UID39 | I10.3 Bool | 전기 LS10 응답 |
| Flag.M_PV03 | 0604 RID193 AO90 BAD2→0603 Flag RID2 TOD2; NID42 UID1150/1151. 0609 RID153 BAD5→0608 Flag RID5 TOD2; NID15 UID74/81 | DB2.DBX11.2 Bool | 상위 요청/기억, 물리센서 아님 |
| Inputs.PV03 Local Selector | 0604 RID256 AO84 BAD218→0603 Inputs RID218 TOD13; NID42 UID1152 | DB13.DBX10.4 Bool | 출력 OR의 처리 입력; CL09 전용 선택 아님 |
| Inputs.Deviator Open/Close PV-03 | 0609 RID154 AO82 / RID151 AO83; BAD86→0608 Inputs RID86 TOD13; NID15 UID78/64 | DB13.DBX10.2 / DB13.DBX10.3 Bool | 원시 I와 구분되는 처리 경로 |
| Flag.PV_03_GATE_MEM_OPEN/CLOSE | 0609 RID147 AO73 / RID149 AO72, BAD5→0608 Flag RID5 TOD2; NID15 UID35/37 및40/42 | DB2.DBX9.1 / DB2.DBX9.0 Bool | 위치 기억. 두 실린더 실제 위치 확인과 다름 |
| ON / OFF | 0602 RID1/33, Memory AO0/1, NID42 UID1148/1149; 응답망 ON은0607 RID1 UID32 | M0.0 / M0.1 Bool | 상수 true/false로 치환 금지 |

AO46=5×8+6, AO82=10×8+2, AO90=11×8+2로 환산했다. 다른 블록의 RID 숫자만 일치한다고 같은 선언으로 연결하지 않는다.

### HMI·직접 이름 검색의 한계

`all-in-one/sources/hmi_plc_tags.csv` 719~723행은 PV_03\\Flag=DB2,X11.2, LS_Open=DB11,X80.0, LS_Close=DB11,X80.1, Allarme1=DB11,X80.3, Selector=DB11,X80.2(Access PLC)를 갖는다. 원시 I10.2/10.3, 처리 DB13, 위치기억 DB2와 표시 DB11을 합치지 않는다. CSV는 설정 주소이며 화면 버튼 이벤트·쓰기 권한·실제 온라인 값은 아니다.

부모 PV03 문서의 HMI LAD1217/0393 CRef23, 12개 ORef 중 FALSE 3개 결속/9개 미결속 경계를 공통색인으로 유지한다. 이번 CL09 작업은 그 호출 전체를 재조사하지 않았고 CL09 전용 호출로 바꾸지 않았다. CRef 소유를 CL09에 신규 부여하지 않는다.

695개 decoded-original XML과 HMI CSV에서 `(?:CYL[-_ ]*)?CL[-_ ]*0?9(?!\d)` 대소문자 무시 검색의 직접 일치는 0이다(`signal-search.json`). 695는 어휘검색 수이지 의미검토 수나 PLC 신호 부재 증명 수가 아니다. 별칭/누락 자료/외부 장치 존재는 배제하지 않는다.

## 3. 제어 구조

### 3.1 상위 요청→Q5.6

직접 대조 원본 `0272-FlgNet.xml`, 부모 탐색색인 LAD1972, 선언 NID42:

- ON Contact1164의 operand W1154/ORef1148→0602 RID1. 1164.out→W1165는 Contact1166/1168/1170.in으로 분기한다.
- OFF1166 operand W1155/ORef1149→RID33; out W1167→RCoil1141.in. 대상 operand W1157/ORef1150→0604 RID193 M_PV03다. 정적 Reset 조건은 ON AND OFF다.
- M_PV03 Contact1168 operand W1158/ORef1151→RID193; out W1169→OR1144.in1.
- 처리 Local Selector Contact1170 operand W1159/ORef1152→0604 RID256; out W1171→OR1144.in2.
- OR1144.out→W1160→Coil1147.in; operand W1162/ORef1153→0602 RID195 Q5.6.

따라서 이 rung의 정적 식은 **Q5.6 = ON AND (M_PV03 OR Inputs.PV03 Local Selector)**다. Local Selector가 OR에 남으면 요청 Reset만으로 Q가 반드시 꺼지는 것은 아니다. 이 선택망에는 CL09/CL10 별도 코일이나 CRef가 없다. 출력 rung의 직접 알람 차단접점 부재를 공정 전체 보호 부재로 확대하지 않는다. Q=0을 CL09 수축·특정 출구 선택·닫힘 실물 확인으로 바꾸지 않는다.

### 3.2 원시/처리/요청→위치 기억

직접 대조 `0290-FlgNet.xml`, 부모 색인 LAD1925, NID15. `!`는 원문 Negated operand이며 다음은 동작시험 결과가 아닌 정적 연결 해석이다.

| 쓰기 | 조건 | Part/Wire/ORef |
|---|---|---|
| MEM_OPEN Set | ON AND Q5.6 AND (I10.2 OR DB13X10.2 OR M_PV03) | ON21→W45→Q22→W75→23/77/80→W85/83/84→OR82→W86→S24; 대상 W50/ORef35 RID147 |
| MEM_OPEN Reset | ON AND !Q5.6 | Negated25→W52→R26; 대상 W53/ORef37 RID147 |
| MEM_CLOSE Set | ON AND !Q5.6 AND (I10.3 OR DB13X10.3 OR !M_PV03) | Negated27→W55→28/63/Negated69→W57/66/72→OR65→W67→S29; 대상 W58/ORef40 RID149 |
| MEM_CLOSE Reset | ON AND Q5.6 | Contact30→W60→R31; 대상 W61/ORef42 RID149 |

열림 operand는 raw23 W48/ORef34 RID146, DB77 W76/ORef78 RID154, 요청80 W79/ORef81 RID153. 닫힘 operand는 raw28 W56/ORef39 RID148, DB63 W62/ORef64 RID151, 요청69 W73/ORef74 RID153이며 마지막 요청만 Negated다. Q 접점22/25/27/30의 operand는 각각 W46/51/54/59, ORef33/36/38/41→0607 RID145다.

**요청 조건만으로도 위치 기억 Set이 성립할 수 있는 가지**를 확인했다. 실제 현장에서 센서가 우회됐다는 사건 판정은 아니다. 두 원시 입력이0 또는 모두1일 때도 MEM만으로 실물 위치를 판정할 수 없다. 부모 startup, 입력Word 전달, 다른 쓰기와 호출/ENO 경계는 부모 공통 연구에 남기며 이번 선택망이 전체 최종 쓰기를 입증한다고 쓰지 않는다.

## 4. 전기 끝점·공압 전달

### 4.1 실제 렌더 및 페이지별 개정

| 파일 | 실제 PDF 페이지 | FG/표제 | 해당 페이지 개정 |
|---|---:|---|---|
| PID_1684n002I.pdf | 1 | 도번1684n002 / PV-03 Detail | Apex I, 15/01/2013; 기본06/04/2011 |
| Electrical_Rev2.pdf | 74 | FG73 DEVIATOR DISCH SCREEN VALVE PV-03 | 개정칸 공란; 기본27.05.2024 |
| 같은 파일 | 127 | FG126 DIGITAL INPUT MODULE | Rev2 17.03.2025; 기본27.05.2024 |
| 같은 파일 | 142 | FG141 DIGITAL OUTPUT MODULE | Rev2 17.03.2025; 기본27.05.2024 |

실제 PDF4페이지 렌더와 고유 상세/표제 확대를 확인했다. 파일명 Rev2를 모든 시트의 개정일로 확장하지 않는다.

### 4.2 구동 전기→EV06→CL09/CL10

1. FG141/PDF142 +24Vdc10.9→X21/3033(도면5×20 4A F)→선141.1→MOD15 공급단자19, 단자20→−0Vdc10.6. MOD15 단자17 A5.6→교차73/3→FG73의73KA1 A1, A2→−0Vdc10.6. CPU515/MOD15는 도면 표기이며 현재 설치 CPU 관측이 아니다.
2. FG73/PDF74 110Vac9.7→73KA1 **접점5–9**→선73.1→X1/156(5×20 2A F 표기)→선73.2→EV06 A1. EV06 A2→X1/157→0Vac9.9. 위쪽1 단자는 이 부하선에 연결되지 않으며 하단 접점표1/5/9를 부하경로1–9로 읽지 않는다.
3. P&ID PDF1의 EV06 이후 공압 분기→CL09/CL10다. EV06 코일은 전기 끝점, CL09는 공압 구동체다. CL09에110Vac가 직접 인가된다고 쓰지 않는다.
4. EV06 포트/스풀·튜브 번호→CL09 양 포트, 복귀 방식·잔압·실제 코일명판·호스 경로·공압 설정은 미확정이다. 퓨즈2A/4A는 도면값이며 현재 보호설정이나 교체 권고값으로 확정하지 않는다.

### 4.3 LS09/LS10과 선택입력 끝점

- LS09: FG73 +24Vdc10.7→X1/158(5×20 2A F)→선73.3→LS09 13/14→X1/159→E10.2, 교차126/3. FG126/PDF127 MOD10 단자23 E10.2, 설명 LIMIT SWITCH LS-09. PLC I10.2 선언과 대조된다.
- LS10: +24Vdc10.7→X1/160(2A F)→선73.4→LS10 13/14→X1/161→E10.3, 교차126/4. FG126 MOD10 단자24 E10.3, 설명 LIMIT SWITCH LS-10. PLC I10.3과 대조된다.
- PB17: +24Vdc10.7→X1/162(2A F)→선73.5→73SA1 접점13/14→X1/163→E10.4 교차126/5→FG126 단자25. 출력식에서는 DB13X10.4 처리입력을 사용한다.
- FG126 쪽의 역방향 교차표기는 E10.2=73/4, E10.3=73/5, E10.4=73/6이며 각 시트의 그리드 참조다. FG73에 적힌126/3~5와 같은 문자열이어야 한다고 강제하지 않는다.
- P&ID의 LS 리더와 전기도면의 Deviator open/close를 함께 확인했으나 센서 실물 장착방식·실린더 행정방향·배출방향·정상/장애극성은 확인되지 않았다. 접점13/14 표기만으로 물리 위치별0/1을 확정하지 않는다.

부모 PV03 초안에 기록된 PB17의 전면배치/시공도 번호·주소 상충은 해결되지 않은 공통 경계로 유지한다. 이번에는 FG73/126/141의 CL09 구동·응답 관련 부분만 직접 검토했으며 다른 시공도 전체를 재검사하거나 어느 자료를 현행이라고 선택하지 않았다.

## 5. 알람·복구

- 직접 이름검색과 선택망에서는 CL09 고유 타이머·알람·리셋·HMI 객체의 독립 선언을 확보하지 못했다. 고유 신호가 물리적으로 존재하지 않는다는 뜻은 아니다.
- 부모 PV03 도달감시·유지·Reset과 타이머는 부모 공통 근거를 재사용한다. 이번 초안은 부모 알람/타이머 전체를 재조사하지 않았으며 CL09_NOT_OPEN 같은 독립 항목으로 복제하지 않는다.
- 부모 알람 또는 HMI 표시 하나로 CL09 불량을 확정하지 않는다. EV06·공압공통·CL10·센서·입력전달·위치기억·기계 링크를 분리할 관찰이 필요하다. 특히 §3.2의 요청 OR 경계 때문에 알람 없음/기억 있음도 실린더 이동 완료의 증명이 아니다.
- Reset 성공, 요청 재발생, PLC 출력 변화, 실제 코일/공압 전달, 실물 이동, 센서 반응, 복구완료는 각각 별개다. 현재 원인·조치·복구증거는 없다. 현장 리셋·강제출력·우회·보호값 변경·동작시험은 수행하지 않았다.

## 6. 증상별 관찰과 필요한 수리 근거

다음은 승인된 관찰자료가 있을 때 기록할 비교 항목이다. 통전측정·움직임 시험·임의 정비 지시가 아니다. 미관측 값은 공란이며0으로 채우지 않는다.

| 증상 | 구분해 기록할 자료 | 비교/배제 경계 | 필요한 자료 |
|---|---|---|---|
| CL09/CL10 모두 반응 없음 | 같은 시각의 M_PV03, 처리Selector, Q5.6, EV06 상태, 공급 관측 | 0272 출력 OR, FG141→73KA1→EV06, P&ID 공통 분기; 실린더 고장 즉시 단정 금지 | 승인 배선·공압 계측기록, 현행 도면 |
| CL10 움직임과 CL09 불일치 | 두 실린더 식별·장착 위치, 링크, 관찰 시각 | 공통 EV/Q만으로 개별 행정/저항 판단 불가 | 명판·공압포트/호스·기계조립도 |
| 위치기억은 바뀌지만 CL09 실제 이동 불명 | 원시I10.2/10.3, 처리DB13, 요청, MEM, HMI 및 실물 각각 | 0290 요청 OR가 있어 기억 변화는 센서 확인과 다름 | 동일시점 온라인/현장 기록과 현재 CPU 일치 확인 |
| LS09/10와 HMI 방향 불일치 | 센서 설치위치/상태, 단자·원시/처리/표시 각각 | P&ID 리더≠정상극성 증명; DB11과 원시I 분리 | 승인 I/O 목록·HMI 실제 이벤트/결속·배출방향표 |
| 부모 알람 반복 또는 해제 후 재발 | 정확한 부모 알람명, 발생·해제시각, 요청/Q/raw/DB/MEM | 부모알람을 CL09 소유로 변경하지 않음 | 부모 알람 원본 및 동시점 현장자료 |

관찰자·시각/시간대·장치/위치·프로젝트/CPU 식별근거·값/단위·비교원본/개정·배제한 사실·승인된 조치·전후자료·복구증거를 남긴다. 실린더 제조사/모델/보어/행정/압력/씰/토크/윤활·정비주기는 명판 및 해당 제조사 자료 확보 전 미확정이다.

## 7. 완료·누락 및 검증

### 7.1 7영역 적용 판정

| 영역 | 판정 | 이번 확보/누락 |
|---|---|---|
| 설비·자료 기준 | 적용 | CL09 고유 P&ID와 부모/형제/센서 관계; 실물 미확정 |
| IO/HMI | 상위 연계 적용·전용 미확보 | 선언/주소/CSV; 독립 실린더 신호로 변경 안 함 |
| 제어 | 상위 구동·응답 적용 | 출력망/위치기억 선택망2개; 전체 CPU 실행 미검증 |
| 전기 끝점 | 전기→공압 경계 적용 | EV/릴레이/LS/모듈 끝점; 실제 호스·심선·현행 부품 미확정 |
| 알람/복구 | 상위 연계·전용 미확보 | 부모 복제 없음; 실제 복구 미수행 |
| 증상 관찰 | 적용 | 공동/개별 원인을 나눌 기록항목; 실제 진단 미수행 |
| 완료/누락 | 적용 | 문서·정적·UI·게시·CPU·현장 상태 분리 |

### 7.2 수행검사와 수량 구분

- 선정 원본17개 전체 SHA256, 고정 Git blob ID 및 blob 바이트 SHA256 계산, 로컬 바이트와17/17 일치. 전체 저장소730원본 보존검사를 새로 수행했다는 뜻은 아니다.
- 의미 검토: P&ID 실제1페이지, 전기 실제3페이지, FlgNet2개(0272/0290), 선언XML6개(0602/0603/0604/0607/0608/0609)의 해당 선언/DB/핀, HMI CSV5행, 두 대장 CL09 해당 행. 지침 문서 읽기/해시 검사는 제어망 의미검토수에 포함하지 않는다.
- XML695개 어휘검색은 별도 검색 범위다. 일치0을 현장 신호 부재로 승격하지 않는다.
- 수행: own `extract.py`(XML/JSON 정적 추출·해시/Git show 비교), PyMuPDF 실제PDF 렌더, 이미지 시각검토, JSON 재읽기, Git 상태 확인. 원본 생성기·앱빌드·행동시험·시뮬레이터 미실행.
- 자체 검토에서 CL09 전용 PLC 소유를 부여하지 않는지, MEM 요청 OR, 73KA1 5–9, 센서 끝점, 페이지별 개정을 재확인했다. 독립 검토 미수행.

### 7.3 네 기능 및 상태

| 기능 | 범위/실제 결과 |
|---|---|
| 도면·래더 나란히 보기 | 연결할 원본·핀·PDF페이지 제공; UI 구현/링크검사 미실행 |
| 백업 미리보기·선택 복원 | 저장키·미지필드·기존note/repair_observation 수정 없음; 구현·재읽기 미검증 |
| 전후 기록 비교 | 관찰 항목만 제안; 저장·재열기·비교 기능 미검증 |
| 관찰 보고서/PDF | 앱 보고서 생성·출력 미검증; 원본 PDF 렌더와 별개 |

| 상태 | 결과 |
|---|---|
| documentation | draft_complete_with_gaps |
| static_review | self_review_complete; independent_review_pending |
| ui_records | not_run |
| publication | not_published_by_this_task |
| tia_compile | not_performed |
| live_cpu | not_performed |
| field_recovery | not_performed |

다음 좁은 확인은 CL09 명판·장착위치·EV06에서 각 포트까지의 호스와 LS09/LS10 실제 위치를 승인된 현행 도면/사진으로 대조하는 것이다. 추가자료 없이 같은 미확정을 반복 조사하지 않는다. 현재 CPU·실물 동일성·정상극성·보호설정·현장복구는 미확정으로 유지한다.

## 부록 A. 선정 전체 원본 SHA256 / 고정 Git blob

경로는 `source-mv06/` 기준이며 commit `abcf31c5030bc7ef8749ed8e869a857f2387a28a`의 blob 전체 바이트와 비교했다. 부모 초안 및 배정/중복 검토 JSON은 탐색·범위 자료로 사용하며 아래 원본17개 검사수에 포함하지 않았다. 최신 인계/버전 문서는 시점·보존맥락으로 읽었으며 선정 제어근거집합과 구분한다.

| 원본 상대경로 | 전체 SHA256 | Git blob | 로컬/고정blob 바이트 |
|---|---|---|---|
| `AGENTS.md` | `0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2` | `073164bc6efd5791032d62c71b03b4dab48cb6f8` | PASS |
| `.agents/skills/gme-equipment-rollout/SKILL.md` | `fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b` | `9aa820ea6ca15b4e136c9772423b78ed4df6a3d4` | PASS |
| `docs/equipment-standard/WORK-STANDARD.md` | `05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99` | `f76a570cc73098632e08759b17934000f7e3a253` | PASS |
| `docs/equipment-standard/WORK-ITEM-TEMPLATE.md` | `4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586` | `e546f39535d2b589e80f97db869ac37ce4d05cfd` | PASS |
| `docs/equipment-standard/INVENTORY.json` | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` | `587c3748ad9224718f95ba06463fee913dae231d` | PASS |
| `all-in-one/registers/equipment.json` | `7870325dff32bbca90fa34507b301c4aad3347d669fddcd03b910343663996fa` | `acc42633033398216469064932c4b76987371606` | PASS |
| `all-in-one/sources/PID_1684n002I.pdf` | `2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b` | `8c83a59fefd5b8b651ec3537ea4236a073f5e109` | PASS |
| `all-in-one/sources/Electrical_Rev2.pdf` | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` | `f610fd7c7ce14ae951b00cff57b969259bfb389d` | PASS |
| `all-in-one/sources/hmi_plc_tags.csv` | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` | `cf4c0650e7c7baac350dcb89909b808435704880` | PASS |
| `all-in-one/sources/decoded-original/0602-IdentXmlPart.xml` | `46ab21151eddaaf616469db520730c60423eb742aa491af194e6710c751b4caf` | `bcb12ab1ce8c476ff921baa1608f29d9822f76b4` | PASS |
| `all-in-one/sources/decoded-original/0603-IdentXmlPart.xml` | `e93969dfa281d75b49b24127793068e33472dadb19729c1c48fc4a8dad075ef8` | `3a92b304baf4dbf6147e944d9778d2da11285cb1` | PASS |
| `all-in-one/sources/decoded-original/0604-IdentXmlPart.xml` | `b798d29c5499b5314a1ee3cff9139dae64c887533b86baa43b6e9a052373a6af` | `bb2c318788b97e7a4924a176275c12d805aa519d` | PASS |
| `all-in-one/sources/decoded-original/0607-IdentXmlPart.xml` | `9b76b53536a26e7b45961fecbf825ae1552e16c2fd9af5736864193c01d77f93` | `dbd4da513171f04cca9b1c1741d0293c3e38f98c` | PASS |
| `all-in-one/sources/decoded-original/0608-IdentXmlPart.xml` | `24adec2035b65c0c310d637bcea74374896875b6465a16aa2f2cfc8fd55fa4b8` | `cea8f4160d2da00023b1ecc5e591b561e4a08330` | PASS |
| `all-in-one/sources/decoded-original/0609-IdentXmlPart.xml` | `395de8ebb2168848cf96fe015bd7334d71107c114a4e441ef36346b8f22031db` | `ee2aab34c0116642dd9f4364b236426f78a876a3` | PASS |
| `all-in-one/sources/decoded-original/0272-FlgNet.xml` | `654fbd1c537044693d242b4d806ea8304db9bd83f2655b2566468812103c3357` | `bc961d4d53cb324d92159d6c455d770b7cb87304` | PASS |
| `all-in-one/sources/decoded-original/0290-FlgNet.xml` | `616ae571a3a19d97d71137ac539cc6e5c8b1db13b0e2b78ae8c1f9401098bc0f` | `2383f3b0c4a515bf25f7d0656a3bf61acbc81803` | PASS |

## 부록 B. 자체 증거 산출물

- `extracts/CYL-CL09/source-verification.json`: 선정17개 전체 SHA256/고정blob/바이트 대조.
- `extracts/CYL-CL09/static-review.json`: 선택2망 Wire 참조 해소(0272 12개/0290 29개), 시각검토·의미검토 범위와 미실행 상태.
- `extracts/CYL-CL09/xml-evidence.json`: 선택2망 원문 및6선언 XML의 직접 관련 RID 원문.
- `extracts/CYL-CL09/signal-search.json`: XML695개 이름검색 및 PV03 HMI5행.
- `extracts/CYL-CL09/catalog-row.json`: 두 대장의 CL09 행.
- `extracts/CYL-CL09/PID-p1.png`, `pid-detail.png`, `pid-title.png`: 실제PDF1 및 CL09 상세/개정 확대.
- `extracts/CYL-CL09/Ele-p74.png`, `Ele-p127.png`, `Ele-p142.png`: 실제 전기PDF3페이지.

CL09 자체의 고유 RID/NID/Part/Wire/ORef/CRef는 근거 미확보이며 부모 번호로 창작하지 않았다.
