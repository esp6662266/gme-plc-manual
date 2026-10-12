# LS10 — PV03 닫힘 위치 리미트 스위치 7영역 조사 초안

- 작성: 2026-10-11 UTC, 작업3 / 22차, GME-STD-1.0.0.
- 고정 원본: `source-mv06`, commit `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, 원본 프로그램 v1.12.0. 이번 LS10 게시 버전이 아니다.
- 범위: LS10 한 ID. `TASK3-BATCH22-SCOPE.json` 및 `GME-CATALOG-OVERLAP-REVIEW.json`의 parent_child_separate / parent PV03 / new_research_scope=true 확인. 부모 완료를 상속하지 않는다.
- AGENTS, 저장소 skill, WORK-STANDARD, WORK-ITEM-TEMPLATE, INVENTORY와 VERSION/최신 인계·게시·확장·ACTIVE-WORK 상단을 읽었다. 기준 원본 Git 상태는 시작/종료 clean. 원본 사전검사/생성기는 실행하지 않고 배정된 고정 원본과 선택 근거의 바이트 검사를 수행했다.
- PV03 및 CYL-CL09 초안을 공통 탐색색인으로 재사용했다. LS10 고유 입력 선언·연결·기억 쓰기·다른 DB 쓰기·실제 PDF 끝점은 독립 대조했다. 부모 전체 출력/알람/HMI 호출은 반복조사하지 않았다.
- 수정 범위: `drafts/LS10-DOTS-DRAFT.md`, `extracts/LS10/`뿐. 원본·공통코드·대장·버전·PLC·현장·보호값·SEJIN 변경 없음. 시뮬레이터 작성·수정·생성·실행·행동시험, 원본 생성기·앱빌드·업로드·새 Work/Codex·재위임 없음.
- 문서 초안이며 현재 CPU/실물/정상극성/현행 보호설정/실제 복구는 미확정. 실제 실행 모델 선택값은 이 산출물에서 독립 관측하지 않았다.

## 핵심 결과

1. FG73/PDF74의 LS-10은 `LIMIT SWITCH DEVIATOR CLOSE`, X1/160→선73.4→13/14→X1/161→E10.3이다. FG126/PDF127의 MOD10 단자24 E10.3과 일치한다.
2. PLC raw `Deviator Close PV-03`는 **I10.3 Bool**, 0607 RID148 / NID15 UID39. LAD1925의 Part28은 비반전이다. `Inputs.Close` DB13X10.3, `MEM_CLOSE` DB2X9.0 및 HMI DB11X80.1은 서로 다른 신호다.
3. LAD1925에서 `MEM_CLOSE Set = ON AND !Q5.6 AND (I10.3 OR Inputs.Close OR !M_PV03)`이다. 요청 반전 가지가 있으므로 MEM_CLOSE=1은 LS10이 실제 작동했다는 증거가 아니다. Startup도 센서 없이 이 기억을 Set한다.
4. P&ID PDF1의 LS-10 리더는 PV-03 Detail의 CL09 몸체 쪽에 이어진다. 대장 부모는 PV03이며 이를 CL09 전용 PLC 소유 또는 실제 수축/배출방향 확정으로 바꾸지 않는다.
5. 처리 DB에는 IW10 Word 전달 외에 보존된 중지 블록의 다른 쓰기가 있다. 원문 정적 교차참조만 확인했으며 실행 여부·현재 최종값은 미확정이다.

## 1. 설비·자료 기준

INVENTORY `/catalog/225`: LS10, 밸브 위치 리미트 스위치, component / 하위 구성품, parent_id=PV03, depth=1, priority_key=null, phase=phase2, queue_state=planned, existing_detail=baseline, bc01_standard_acceptance=not_assessed. equipment.json의 LS10행은 aliases `ls-10`, `ls.10`, fgs=[73], parent=PV03다. 같은 일반 이름을 가진 다른 LS들과 중복 ID로 합치지 않는다. [S01]

P&ID `PID_1684n002I.pdf`, 실제 PDF1, 도번1684n002 Apex I(15/01/2013), 기본06/04/2011: PV-03 Detail에서 압축공기→EV06 이후 CL09/CL10 병렬 구동이 그려지고 LS10/LS09 두 리더는 CL09 기호의 몸체 쪽/로드 쪽을 각각 가리킨다. CL10 기호에는 별도 LS 리더가 확인되지 않지만 실제 CL10 센서 부재를 뜻하지 않는다. 아래 기계 링크 스케치는 장착 치수나 실물 방향을 확정하지 않는다. [S02]

전기도면은 기본2024년/해당 페이지 일부2025년 개정이다. 2013 P&ID와 같은 시점의 승인 준공 자료라고 가정하지 않는다. 태그·주소 대조는 문서상 대응이며 현장 표찰, 최신 승인도, 제조사/모델, 정상/고장극성, 케이블/심선표와 현행 CPU 비교가 필요하다.

## 2. I/O·HMI

아래 `NNNN`는 `all-in-one/sources/decoded-original/NNNN-IdentXmlPart.xml`이며 FlgNet은 별도 표시한다. RID는 선언 묶음과 NID/UID를 함께 사용하며 다른 문맥의 같은 숫자를 결속하지 않는다.

| 층/신호 | 백업 주소·형식 | 선언과 LS10 연계 | 경계 |
|---|---|---|---|
| raw Deviator Close PV-03 | I10.3 Bool | 0607 SimpleAccess RID148, Input AO83, NID15 UID39 | 전기도면 E10.3와 대응; 현장 현재값 아님 |
| 비교 raw Open | I10.2 Bool | 0607 RID146 Input AO82, NID15 UID34 | LS09, LS10과 별개 |
| 처리 Inputs.Close | DB13.DBX10.3 Bool | 0609 RID151 AO83 BAD86→0608 Inputs RID86 TOD13; NID15 UID64 | raw와 별도 DB 저장 |
| 처리 Inputs.Open | DB13.DBX10.2 Bool | 0609 RID154 AO82 BAD86; NID15 UID78 | LS09 처리 대응 |
| Flag.PV_03_GATE_MEM_CLOSE | DB2.DBX9.0 Bool | 0609 RID149 AO72 BAD5→0608 Flag RID5 TOD2; NID15 UID40/42 | Set/Reset 기억값 |
| Flag.PV_03_GATE_MEM_OPEN | DB2.DBX9.1 Bool | 0609 RID147 AO73 BAD5; NID15 UID35/37 | 비교 기억값 |
| Flag.M_PV03 | DB2.DBX11.2 Bool | 0609 RID153 AO90 BAD5; NID15 UID74/81 | 상위 요청; LS10 신호 아님 |
| PV-03 GATE EV | Q5.6 Bool | 0607 RID145 Output AO46; NID15 UID33/36/38/41 | 공통 EV06 출력 피연산자 |
| ON | M0.0 Bool | 0607 RID1 Memory AO0; NID15 UID32 | 상수 true로 치환 금지 |

AO83=10×8+3, AO72=9×8+0이다. DB2X11.2 요청과 같은 숫자의 다른 DB 비트를 합치지 않는다. [S03]

### 2.1 raw→처리 Word 전달

`0397-FlgNet.xml`, 부모 색인 LAD1070 / hmi inputs / NID1: Move44.in←Wire58/ORef49 RID17; 0627 RID17 Tag_182의 Word/Input/AO80은 IW10. Move44.out1→Wire59/ORef50 RID18; 0629 RID18 Word/AO80/BAD4→0628 Inputs RID4 TOD13은 DB13.DBW10이다. **IW10→DB13.DBW10** 전달에 I10.3/DB13X10.3이 포함된다. 이 선택 경로에는 LS10 개별 NOT가 없다. [S04]

Move44.en은 Wire56을 통해 Move43.eno와 연결된다. 부모 PV03 공통 조사에서 main `0030` LAD1613/NID19의 HMI Inputs CRef28.en 앞에 NOT Simulation(1) 조건, 앞선 호출 ENO 연결을 기록했다. 이 호출 전체는 이번 재조사 대상 밖이며 처리 DB가 매 스캔 항상 최신이라는 결론은 내리지 않는다.

### 2.2 다른 DB 쓰기: 중지 원문 정적 검토만

보존 `0407-FlgNet.xml`, 부모 색인 LAD1087 / NID6에서 닫힘 처리값의 Coil38.operand는 Wire37/ORef39 RID163이다. 0635 RID163 AO83 BAD5→0634 Inputs RID5 TOD13, NID6 UID39 AK=Write이므로 대상은 **DB13X10.3**이다. raw I10.3 쓰기로 바꾸지 않는다. Coil38.in은 Wire36을 통해 Negated Contact33.out에 연결된다. Contact33.operand는 Wire34/ORef35 RID159이며 0635 RID159의 Flag.M_PV03 AO90/BAD1→0634 Flag RID1 TOD2, NID6 UID24/35와 결속된다. 따라서 보존 원문은 요청 M_PV03를 열림 처리값으로, 반전 요청을 닫힘 처리값으로 쓰는 구조이며 실제 raw 접점의 반전과 다르다. 열림도 Coil31/Wire30/ORef32 RID162→DB13X10.2의 별도 쓰기가 있다. [S05]

이는 중지 블록의 보존 바이트에서 찾은 다른 쓰기 경계다. 해당 자산 또는 시뮬레이터를 작성·수정·생성·실행하거나 행동시험하지 않았다. 현재 CPU 호출/활성 여부/최종 쓰기 순서를 관측하지 않았다.

### 2.3 HMI

`hmi_plc_tags.csv` 719~723행: PV_03\Flag=DB2,X11.2, LS_Open=DB11,X80.0, **LS_Close=DB11,X80.1**(내부ID0006F), Allarme1=DB11,X80.3, Selector=DB11,X80.2, Access Name=PLC. CSV는 dde.cfg 설정이며 실제 화면 이벤트·권한·통신·현재값이 아니다. LS_Close라는 이름만으로 I10.3 또는 MEM_CLOSE와 동일하게 묶지 않는다. [S06]

부모 공통색인 LAD1217 `0393` CRef23/RID752 HMI PV_1gate 호출은 12 ORef 중 FALSE3개만 결속/나머지9개 미해결이다. LS_Close 입력 W26/ORef27/RID754 및 HMI_LS_Close 출력 W42/ORef43/RID759의 실인수는 부모 문서에서도 미확정이다. 공통 함수 이름·CSV 주소·나열 순서만으로 이 공백을 채우지 않는다. LS10 독립 HMI 버튼·알람 객체는 이번 자료에서 확보하지 못했다.

## 3. 제어 구조

### 3.1 닫힘 위치 기억의 정확한 핀 경로

직접 대조 `0290-FlgNet.xml`, LAD1925, NID15. 아래는 정적 연결 해석이며 동작시험 결과가 아니다. [S03]

- ON Contact21 operand W44/ORef32/RID1→out W45.
- W45→Negated Q Contact27.in; operand W54/ORef38/RID145(Q5.6); out W55가 Contact28/63/69 입력으로 분기.
- **raw Close Contact28(비반전)**: operand W56/ORef39/RID148(I10.3), out W57→OR65.in1.
- **Inputs.Close Contact63(비반전)**: operand W62/ORef64/RID151(DB13X10.3), out W66→OR65.in2.
- **M_PV03 Contact69(반전)**: operand W73/ORef74/RID153(DB2X11.2), out W72→OR65.in3.
- OR65.out→W67→SCoil29.in; operand W58/ORef40/RID149(MEM_CLOSE).
- 별도 Reset: W45→Contact30(비반전 Q), operand W59/ORef41/RID145; out W60→RCoil31.in; operand W61/ORef42/RID149.

따라서 **Set = ON AND !Q5.6 AND (I10.3 OR DB13X10.3 OR !M_PV03)**, **Reset = ON AND Q5.6**이다. raw/처리 Close 자체가 반전된 것이 아니라 Q와 요청에 반전이 있는 구조다. MEM_CLOSE는 LS10의 단순 복사값이 아니다.

비교 열림 Set은 ON AND Q5.6 AND (I10.2 OR DB13X10.2 OR M_PV03), Reset은 ON AND !Q5.6. Part22→W75→23/77/80→W85/83/84→OR82→W86→SCoil24, 대상 W50/ORef35/RID147; Reset Part25→W52→RCoil26, 대상 W53/ORef37/RID147이다. 두 raw 모두0/1인 상태를 기억값만 보고 정상·이상 또는 실물 위치로 확정하지 않는다.

### 3.2 Startup 쓰기

`0150-FlgNet.xml`, LAD405 / NID5: Contact326 operand W319/ORef313→0047 RID1 ON M0.0, out W327→SCoil311.in. 대상 W324/ORef318→0563 RID53 AO72/BAD6→0562 Flag RID6 TOD2, **DB2X9.0 MEM_CLOSE**다. 센서 LS10 접점 없이 기억을 Set하는 원문이다. 실제 닫힘 명령·센서 확인·재시작 후 안전위치 확인을 뜻하지 않는다. Warm/Cold/Retain 및 현재 Startup 실행결과는 미확정이다. [S07]

### 3.3 부모 구동 경계

PV03 초안의 공통 출력식은 LAD1972/0272의 `ON AND (M_PV03 OR Inputs.PV03 Local Selector)→Q5.6`이다. 이번에는 부모 출력망 전체를 재조사하지 않았으며 LS10 독립 출력·밸브코일·허가·구동방향으로 복제하지 않는다. LS10은 PV03의 위치 응답 구성품이다. 출력/요청/기억/HMI와 실제 이동/접점 상태를 분리한다.

## 4. 전기 끝점 및 실제 PDF 검토

| 원본 | 실제 PDF | FG/도면 | 페이지별 개정 |
|---|---:|---|---|
| PID_1684n002I.pdf | 1 | 1684n002 PV-03 Detail | Apex I, 15/01/2013; 기본06/04/2011 |
| Electrical_Rev2.pdf | 74 | FG73 DEVIATOR DISCH SCREEN VALVE PV-03 | 개정칸 공란; 기본27.05.2024 |
| Electrical_Rev2.pdf | 127 | FG126 DIGITAL INPUT MODULE | Rev2 17.03.2025; 기본27.05.2024 |

원본을 자체 렌더해 전체3페이지와 P&ID 상세/표제를 시각 확인했다. 파일명 Rev2를 FG73의 개정일로 확대하지 않는다. [S02,S08]

### LS10 양 끝점

FG73의 +24Vdc10.7(왼쪽72/9→오른쪽74/0 공통선)에 접속점이 있으며, 그 분기→**X1/160, 5×20 2A F 도면표기**→선**73.4**→**LS-10 접점13/14**→**X1/161**→**E10.3, 교차126/4**다. FG126은 **E10.3 / MOD10 / 단자24 / LIMIT SWITCH LS-10**, 역참조 **73/5**로 대응한다. 각 시트 그리드 참조라서 126/4와73/5 문자열이 같아야 하는 것은 아니다.

도면의 LS10은 DEVIATOR CLOSE, LS09는 OPEN이다. LS09 별도 분기는 X1/158→73.3→13/14→X1/159→E10.2→FG126 MOD10 단자23이다. LS10/LS09의 번호나 방향을 서로 바꾸지 않는다. LS10에 110Vac가 직접 공급되는 도면이 아니다.

접점은 도면에서 13/14 개방기호로 그려져 있으나 실제 기계 위치별 작동상태·정상/장애극성·현행 센서 유형과 동일하다고 확정하지 않는다. 2A F는 도면값이며 교체/현행 보호설정 권고가 아니다. CPU515는 도면 표기이며 현재 설치 CPU 관측이 아니다. 케이블 번호·심선·색상·센서 제조사/모델·단선진단·모듈 현행 모델은 미확정이다.

같은 FG73 EV06 부하는 73KA1 **5–9**→73.1→X1/156→73.2→EV06 A1, A2→X1/157→0Vac9.9로 보인다. 미연결 상단1과 하단 접점표를 부하1–9로 읽지 않는다. 이는 LS10 입력회로와 별개다. 기존69KA/71KA 5–9 정정도 유지하며 이번에 그 부모 도면을 다시 검토한 수량에 포함하지 않는다.

PB17의 부모 공통자료 상충(FG73/126의73SA1/E10.4, 전면배치/시공도 다른 번호·주소)은 해결되지 않았다. 이번 LS10 확정 끝점이 PB17 상충까지 해결한 것은 아니다.

## 5. 알람·복구

- LS10 전용 독립 알람·타이머·Reset 선언을 확보하지 못했다. 부모 PV03의 닫힘/열림 도달알람을 LS10 독립 항목으로 복제하지 않는다.
- 부모 공통색인에서 PV03 도달감시는 MEM을 소비하며 Tag_88/T111 및 Tag_89/T112, 5초 계열로 조사되어 있다. 이번 의미검토 수에 부모 알람망 재검토를 포함하지 않는다. 181 Ident 파일의 정확한 Close/MEM_CLOSE 이름검색에서 0657 RID174의 소비 참조를 찾았지만 검색 한 건을 알람망 전체 검토로 세지 않는다.
- §3의 !M_PV03 OR와 Startup Set 때문에 알람 없음 또는 MEM_CLOSE=1만으로 LS10 정상, 밸브 닫힘, 센서 도달 또는 복구완료를 판정할 수 없다.
- Reset 요청/부모 알람 해제/요청 재발생/출력/실물 이동/센서·raw·DB·HMI 일치/복구확인은 별도 증거다. 승인된 현재 CPU 자료, 시각 일치 관찰과 원인별 조치 기록이 필요하다. 강제출력·우회·보호설정 변경·현장 동작/리셋 시험은 수행하지 않았다.

## 6. 증상별 관찰

아래는 승인된 관찰자료를 비교할 항목이며 통전측정·동작시험·정비 지시가 아니다. 실제 값은 수집되지 않았으며 미관측을0으로 채우지 않는다.

| 증상 | 필요한 동시점 관찰 | 비교 및 원인 배제 경계 |
|---|---|---|
| 실물 닫힘처럼 보이지만 raw=0 | LS10 표찰/장착/작동상태, 승인 전기기록 X1/160·161와 모듈24, I10.3 | 잘못된 센서 식별·기계 미도달·전원/배선/접점/입력 경계를 구분; 센서 불량 즉단 금지 |
| raw I10.3와 DB13X10.3 불일치 | CPU/프로젝트 식별, 원시/Word/처리값 및 시각, 호출 근거 | IW10 전달·ENO/호출·다른 DB쓰기 경계; 현행 활성은 미확인 |
| MEM_CLOSE=1이지만 raw=0 | Q5.6, M_PV03, DB13X10.3, MEM, 재시작 이력 | !요청 OR/처리 OR/Startup으로 설명 가능한 정적 경로; 현장 원인 확정 아님 |
| HMI 닫힘과 raw/MEM 불일치 | DB11X80.1·통신·HMI 객체/호출 실인수, raw/DB13/DB2 각각 | 표시 주소를 직접 raw로 합치지 않음; 미해결9개 실인수 확인 필요 |
| LS09/LS10 둘 다0 또는 둘 다1 | 정확한 장착 위치·두 raw·처리·MEM 및 실제 분기상태 | 이동중/장착/배선/표시/요청경로를 분리; 타이밍·정상 조합 미확정 |
| 부모 닫힘알람 반복 | 부모 정확한 알람·시각·요청/Q/raw/DB/MEM·승인 조치전후 | 상위 구동·공압·기계·입력전달을 구분; LS10 단독 고장 단정 금지 |

기록 필드: 관찰자, 시각/시간대, 장치/단자/물리 위치, 값·단위, CPU/프로젝트 근거, 비교 원본·개정, 확인·배제한 사실, 승인 조치, 전후 증거 및 복구 판정. 개인 운영기록·사진·SEJIN 데이터는 복제하지 않았다.

## 7. 완료·누락·검증

| 영역 | 적용 판단 | 확보/미확정 |
|---|---|---|
| 설비·자료 | 적용 | LS10 대장·P&ID 리더·부모 PV03; 실물 미확정 |
| I/O·HMI | 적용 | I10.3/DB13/MEM/HMI 분리; 객체 실인수 미확정 |
| 제어 | 적용 | 비반전 센서 입력·요청반전 OR·Startup·다른 DB쓰기 |
| 전기 | 적용 | FG73→126 양 끝점, 실제3 PDF페이지·개정 |
| 알람·복구 | 부모 연계 적용/독립 미확보 | 부모알람 소유 유지; 현장복구 미수행 |
| 증상 관찰 | 적용 | 분리 기록항목 제공; 실제진단 미수행 |
| 완료·누락 | 적용 | 상태와 수량을 분리 |

### 검사수와 의미검토수

- 선정 원본24개 SHA256·고정 Git blob·blob SHA256 및 전체바이트 **24/24 일치**. 전체730 원본을 이번에 재검사했다는 뜻이 아니다.
- 의미검토: FlgNet4개(0290 위치망, 0397 선택 Word경로, 0407 다른쓰기 선택경로, 0150 Startup 선택경로), 관련 선언XML11개(0607/0608/0609/0627/0628/0629/0634/0635/0563/0562/0047)의 선택 RID, 실제PDF3페이지(원본PDF2파일), HMI CSV5행, 대장2행 및 분류행.
- 별도 검색: IdentXmlPart181개에서 정확한 Close/MEM_CLOSE 이름 참조6개. 검색 수는 의미검토 수가 아니며 신호/알람 부재 증명이 아니다.
- 자체 정적검사: Wire 참조가 각 문서 Part/ORef에 존재하는지, 선택 선언/주소/반전/소유/도면 끝점/개정을 재확인. `static-review.json`에 수량·결과·미실행 경계 기록. 원본 생성기·빌드·행동시험·시뮬레이터 미실행.
- 부모 출력·알람·HMI 호출/공통 호출의 상세는 공통색인 재사용이며 이번 직접 의미검토와 분리했다. 독립 검토는 부모 인계 후 필요하다.

| 기능 | 실제 상태 |
|---|---|
| 도면·래더 나란히 보기 | 연결할 파일/페이지/핀 제공; UI 구현·검증 안 함 |
| 백업 미리보기·선택 복원 | note/repair_observation/미지필드/키 불변; 저장·재읽기 미검증 |
| 기록 전후 비교 | 비교항목 제안; 기능시험 미수행 |
| 관찰 보고서/PDF | 앱 보고서 생성·출력 미검증; 원본PDF 렌더와 별개 |

| 상태 | 결과 |
|---|---|
| documentation | draft_complete_with_gaps |
| static_review | self_review_complete; independent_review_pending |
| ui_records | not_run |
| publication | not_published_by_this_task |
| tia_compile | not_performed |
| live_cpu | not_performed |
| field_recovery | not_performed |

다음 필요한 자료는 LS10 현행 표찰·장착 위치와 접점/케이블/단자 승인도, 현재 CPU 일치 근거, HMI 호출 실인수/객체 이벤트와 같은 시각의 raw·DB13·MEM·HMI·실물 기록이다. 정상극성·출구방향·현재 보호값·복구완료는 자료 확보 전 미확정 유지.

## 근거 묶음 및 자체 산출물

- S01: INVENTORY.json catalog/225, equipment.json LS10행, classification.json.
- S02: PID_1684n002I.pdf 실제1쪽; own 전체/상세/표제 렌더.
- S03: 0290-FlgNet +0607/0608/0609 선언.
- S04: 0397-FlgNet 선택Move44 +0627/0628/0629 선언.
- S05: 0407-FlgNet 정적 다른쓰기 +0634/0635 선언.
- S06: hmi_plc_tags.csv 719~723행.
- S07: 0150-FlgNet +0047/0562/0563 선언.
- S08: Electrical_Rev2.pdf 실제74/127쪽, FG73/126.
- `extracts/LS10/xml-evidence.json`: 직접 선택 선언 및4망 원문.
- `extracts/LS10/source-verification.json`: 전체 선정 SHA256/Git blob/바이트일치 검사.
- `extracts/LS10/signal-search.json`: 정확한 신호명 검색6참조와 범위.
- `extracts/LS10/static-review.json`: 자체 검사·의미검토/검색/해시 구분.
- `extracts/LS10/*png`: 실제 원본PDF3페이지 및P&ID 상세/표제.

## 부록 A. 선정 전체 원본 SHA256 / 고정 Git blob

원본 상대경로는 source-mv06 기준. 초안/배정/부모문서는 탐색 자료이며 원본 검사수에 합산하지 않았다. 아래 고정blob과 로컬바이트를 직접 비교했다.

| 원본 상대경로 | 전체 SHA256 | 고정 Git blob | 바이트일치 |
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
| `all-in-one/sources/decoded-original/0607-IdentXmlPart.xml` | `9b76b53536a26e7b45961fecbf825ae1552e16c2fd9af5736864193c01d77f93` | `dbd4da513171f04cca9b1c1741d0293c3e38f98c` | PASS |
| `all-in-one/sources/decoded-original/0608-IdentXmlPart.xml` | `24adec2035b65c0c310d637bcea74374896875b6465a16aa2f2cfc8fd55fa4b8` | `cea8f4160d2da00023b1ecc5e591b561e4a08330` | PASS |
| `all-in-one/sources/decoded-original/0609-IdentXmlPart.xml` | `395de8ebb2168848cf96fe015bd7334d71107c114a4e441ef36346b8f22031db` | `ee2aab34c0116642dd9f4364b236426f78a876a3` | PASS |
| `all-in-one/sources/decoded-original/0627-IdentXmlPart.xml` | `08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb` | `61ebc0abbb2ca160e11e1da400a3f14a397d8bc5` | PASS |
| `all-in-one/sources/decoded-original/0628-IdentXmlPart.xml` | `9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd` | `170ca5c72599edc7ea7eefe651c3680ce325e76a` | PASS |
| `all-in-one/sources/decoded-original/0629-IdentXmlPart.xml` | `67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972` | `058129bb01e27f7a6a0d0293f332d745e5bab74e` | PASS |
| `all-in-one/sources/decoded-original/0634-IdentXmlPart.xml` | `af3fcb536a6270ffb9a19e5b3f2c284a38d67d465f5147961005c1c01d11299d` | `877d9e0734dc7f3e5a8cea789eeb58a208501f48` | PASS |
| `all-in-one/sources/decoded-original/0635-IdentXmlPart.xml` | `1a057d686446a3fdab7ac61bb09bc543c52f49646c9ca71ac323c10fcdffe457` | `95bfcad59cfb0c12b573e9e8face4262d1e94622` | PASS |
| `all-in-one/sources/decoded-original/0563-IdentXmlPart.xml` | `86cf35b6baebc079cb5a092baf53ec3364c377ea7318eb263ab69c8b4550b4ad` | `6a10fc694f896cda16409804daf2554c91635654` | PASS |
| `all-in-one/sources/decoded-original/0562-IdentXmlPart.xml` | `85aada44dd9a3e66835463c3fed400f1efe121f4f5bc5ab8f0ad49481ec0ea1c` | `1609802542a3e560baba3f2b73c306be281dfb23` | PASS |
| `all-in-one/sources/decoded-original/0047-IdentXmlPart.xml` | `2e53bb895dd1ad2a74efaeb1ef16dfd61e62b1b2d7aa34cec8612f1b9cb0928e` | `3dc282f149a21fdf76d5521ef1c833be63b578b4` | PASS |
| `all-in-one/sources/decoded-original/0290-FlgNet.xml` | `616ae571a3a19d97d71137ac539cc6e5c8b1db13b0e2b78ae8c1f9401098bc0f` | `2383f3b0c4a515bf25f7d0656a3bf61acbc81803` | PASS |
| `all-in-one/sources/decoded-original/0397-FlgNet.xml` | `bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834` | `4ab8370493c4e28fc1eabeeebe2743d27f0c4021` | PASS |
| `all-in-one/sources/decoded-original/0407-FlgNet.xml` | `ba022010d6f83dcebd6cce8dbd50ab2ad3744e078ad661934af970db81023927` | `2a00538bb8d3378252d671f0a5749237617b27dc` | PASS |
| `all-in-one/sources/decoded-original/0150-FlgNet.xml` | `829ca4aa3bd2bb6ee406f7f204add2987ec6159ef0fd6dd3dfc075592664a98e` | `b8130ae4a433018f7513d24bd8f0cf79a7897238` | PASS |
