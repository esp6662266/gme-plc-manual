# LS09 — PV03 열림 위치 입력 7영역 조사 초안

- 작업3번·22차·phase2, 2026-10-11 UTC. 대상 LS09 하나, 부모 PV03. 기준 GME-STD-1.0.0.
- 고정 원본 `source-mv06`, commit `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, VERSION 1.12.0. 버전은 조사 자료 시점이며 LS09 통합·게시 버전이 아니다.
- 적용: 원본 AGENTS, 저장소 skill, WORK-STANDARD, WORK-ITEM-TEMPLATE, INVENTORY 및 최신 인계 상단. BATCH22 지침의 이전 대상 문구는 현재 scope LS09/PV03 행으로 한정했다. 실제 모델 선택값은 별도 검증하지 않았다.
- 이번 수정은 이 초안과 `extracts/LS09/`뿐이다. 원본·공통 코드·버전·대장·배포·PLC·현장·보호값·SEJIN 변경 없음. 원본 생성기·앱 빌드·시뮬레이터 작성/수정/생성/실행/행동시험 없음.
- PV03 및 CYL-CL09 초안은 공통 탐색색인으로 재사용했다. 아래 LS09 끝점·리더·선언·입력전달·기억 소비·다른 쓰기는 원본을 직접 대조했다. 부모의 완료 상태를 상속하지 않는다.

## 1. 설비·자료 기준

### 식별과 소유

INVENTORY `catalog[224]`: LS09, 밸브 위치 리미트 스위치, component/하위 구성품, parent_id PV03, depth1, priority_key null, phase2/planned, existing_detail baseline, acceptance not_assessed. equipment.json `[212]`의 id LS09, parent PV03, FG73, aliases ls-09/ls.09와 대조했다. `GME-CATALOG-OVERLAP-REVIEW.json`은 parent_child_separate이며 alias duplicate false, physical_identity_verified false다. 이름이 같은 LS10 등과 병합하지 않는다.

P&ID `all-in-one/sources/PID_1684n002I.pdf` 실제 PDF1, 도번1684n002, Apex I/15.01.2013(기본06.04.2011)의 PV-03 Detail을 렌더·확대했다. compressed air→EV06→CL09/CL10 공통 분기, LS10 리더는 CL09 몸체 쪽, **LS09 리더는 CL09 로드 쪽**에 연결된다. LS09 리더를 CL10에 배정하지 않는다. 대장 부모는 PV03이며 리더가 CL09에 닿는다는 사실만으로 catalog 소유를 CYL-CL09로 변경하지 않는다. 실물 장착, 행정방향, 배출방향, 정상극성은 아직 미확정이다.

FG73의 LIMIT SWITCH DEVIATOR OPEN, LS-09, E10.2와 백업의 Deviator Open PV-03/I10.2가 대응한다. 이는 자료 간 태그·주소 대응이며 현재 실물 동일성 검증이 아니다. P&ID 2013년/전기2024~2025년/PLC 백업의 시간 차이를 보존한다.

### 원본 표기 규칙

이하 XML NNNN는 `all-in-one/sources/decoded-original/NNNN-IdentXmlPart.xml` 또는 명시한 FlgNet이다. RID 숫자는 파일·블록·NID/UID 문맥 안에서만 결속한다. SSD AO는 비트 오프셋이며 AO82=10×8+2. BAD의 BIRID를 같은 선언묶음 DepDBBlock TOD와 연결한다. LAD는 부모 색인 이름이며 원문 핀/선언을 대신하지 않는다.

## 2. I/O·HMI

| 계층 | 원본 선언/소유 | 주소·형식 | 해석과 경계 |
|---|---|---|---|
| LS09 원시 입력 | 0607 SimpleAccess RID146, N=Deviator Open PV-03, NID15 UID34, SAD Input/SSD AO82 | I10.2 Bool | LS09 전기 E10.2와 대응; 현재 입력값 아님 |
| LS10 비교 원시 | 0607 RID148, NID15 UID39, Input AO83 | I10.3 Bool | 닫힘 입력; LS09와 독립 |
| PV03 처리 열림 | 0609 GlobalAccess RID154, NID15 UID78, AO82/BAD86→0608 Inputs RID86 TOD13 | DB13.DBX10.2 Bool | raw와 다른 저장영역 |
| PV03 처리 닫힘 | 0609 RID151, NID15 UID64, AO83/BAD86 | DB13.DBX10.3 Bool | LS10 연계, LS09 전용 값 아님 |
| 열림 기억 | 0609 RID147, NID15 UID35 Set/37 Reset, AO73/BAD5→0608 Flag RID5 TOD2 | DB2.DBX9.1 Bool | 센서 실도달 증명 아님 |
| 닫힘 기억 | 0609 RID149, NID15 UID40 Set/42 Reset, AO72/BAD5 | DB2.DBX9.0 Bool | 부모 상태이며 startup 쓰기는 공통색인 참조 |
| 부모 요청 | 0609 RID153, NID15 UID81/74, AO90/BAD5 | DB2.DBX11.2 Bool | M_PV03; 센서 입력 아님 |
| 부모 EV 출력 | 0607 RID145, NID15 UID33/36/38/41, Output AO46 | Q5.6 Bool | EV06 공통 출력, LS09 구동 출력 아님 |
| ON | 0607 RID1, NID15 UID32, Memory AO0 | M0.0 Bool | 상수 true로 치환하지 않음 |

### 원시 Word→처리 DB와 반전 구분

`0397-FlgNet.xml`/LAD1070/NID1의 Move44.in←W58/ORef49 RID17, out1→W59/ORef50 RID18. 0627 RID17 Tag_182 Input Word AO80=IW10, 0629 RID18 Word AO80/BAD4→0628 Inputs RID4 TOD13=DB13.DBW10이다. 따라서 I10.2를 포함하는 **IW10→DB13.DBW10** Word 전달을 확인했다. Move44.en←W56/Move43.eno이며 이 전달에 LS09 전용 NOT/Negated는 없다.

동일0397에 있는 Not142/150은 각각 0627 RID152/154(MV03_Open/Close, I7.5/I7.6)→0629 RID153/155(DB13X7.5/X7.6)이다. 이 반전을 LS09에 복사하지 않는다. 선택한 전달망에서 반전 없음은 실제 접점의 정상/장애극성 또는 전체 프로젝트의 최종값 검증과 다르다.

부모 PV03 공통색인 §2.3의 main0030/NID19: HMI CRef23→HMI Output CRef25→NOT Simulation(1) Contact37→HMI Inputs CRef28.en 경계를 유지한다. 이번에 이 main 호출망 전체를 재검토하지 않았으므로 항상 갱신·현재 활성·최종 스캔값을 주장하지 않는다.

### 다른 DB 쓰기: 중지 보존원문 정적 확인만

`0407-FlgNet.xml`/LAD1087/NID6에는 Contact23(W22/ORef24)→W29→Coil31, operand W30/ORef32가 있다. 0635 RID159 M_PV03 AO90/BAD1→0634 Flag TOD2; RID162 Inputs.Deviator Open PV-03 AO82/BAD5→0634 Inputs TOD13, UID32 Write다. 따라서 **DB13X10.2에 요청 기반의 별도 쓰기가 존재**한다. 닫힘 Coil38/W37/ORef39 RID163은 Contact33의 Negated operand W34/ORef35 RID159에서 W36으로 온다. LS09 원시 I10.2에 쓰는 것이 아니다.

이는 보존 중지 simulation 블록의 문서 교차참조이며 실행·생성·수정·행동시험하지 않았다. 현재 호출·실행 활성·최종 쓰기 순서는 미확정이다. raw와 Inputs가 언제나 동일하다고 쓰지 않는다.

### HMI 설정과 미결속

원본 `hmi_plc_tags.csv` 719~723행: PV_03\\Flag DB2,X11.2; LS_Open DB11,X80.0; LS_Close DB11,X80.1; Allarme1 DB11,X80.3; Selector DB11,X80.2, Access PLC. LS09 원시 I10.2·처리 DB13X10.2·기억 DB2X9.1·표시 DB11X80.0는 네 계층이다. CSV는 설정 주소이며 객체 이벤트·쓰기권한·현재 통신/값이 아니다.

PV03 공통색인 §2.4의 `0393`/LAD1217 CRef23 RID752(NID41, FC16)에는 12개 ORef 중 FALSE3개 결속/9개 미결속이 남아 있다. LS_Open 입력 W24/ORef25 RID753, HMI_LS_Open 출력 W40/ORef41 RID758을 CSV 주소 또는 색인 순서로 임의 결속하지 않는다. 이 호출을 LS09 전용 CRef로 만들지 않았고 공통 HMI 함수 전체는 이번 의미검토수에 포함하지 않았다.

## 3. 제어 구조

### LS09 소비 핀과 위치 기억

직접 대조 `0290-FlgNet.xml`/LAD1925/NID15:

- ON Contact21: operand W44/ORef32 RID1. out W45→Q5.6 Contact22.in, operand W46/ORef33 RID145.
- Contact22.out W75는 세 가지 Contact23/77/80.in에 병렬 공급된다.
- **LS09 raw** Contact23.operand W48/ORef34→0607 RID146. Contact23.out W85→OR82.in1. Contact23에는 Negated 없음.
- **처리 열림** Contact77.operand W76/ORef78→0609 RID154. out W83→OR82.in2. Negated 없음.
- **요청** Contact80.operand W79/ORef81→0609 RID153. out W84→OR82.in3. Negated 없음.
- OR82.out W86→SCoil24.in; operand W50/ORef35→0609 RID147 MEM_OPEN.
- ON 뒤 Negated Q Contact25(W51/ORef36)→W52→RCoil26; operand W53/ORef37→동일 RID147.

정적 연결식: MEM_OPEN Set = ON AND Q5.6 AND (I10.2 OR DB13X10.2 OR M_PV03), Reset = ON AND NOT Q5.6. 실행 시험 결과가 아니다. **M_PV03만으로도 OR 가지가 성립할 수 있어 MEM_OPEN=1은 LS09 접점 동작 확인이 아니다.**

비교 경계: MEM_CLOSE Set은 ON AND NOT Q5.6 AND (I10.3 OR DB13X10.3 OR NOT M_PV03). Contact27 Negated→W55→28/63/69→W57/66/72→OR65→W67→SCoil29; 대상 W58/ORef40 RID149. raw28 operand W56/ORef39 RID148, DB63 W62/ORef64 RID151, 요청69 W73/ORef74 RID153이며 요청69만 Negated다. 닫힘 Reset은 Contact30 Q→W60→RCoil31, 대상 W61/ORef42 RID149. 닫힘 요청의 NOT을 LS09 raw 반전으로 오해하지 않는다.

### 부모 출력·startup 재사용 경계

PV03 공통색인 §3.1의0272/LAD1972 출력식 ON AND (M_PV03 OR Inputs.PV03 Local Selector), Coil1147/W1162/ORef1153→0602 RID195 Q5.6은 부모 EV06 구동이다. LS09 독립 출력·타이머를 생성하지 않는다. 공통색인 §3.3 startup0150의 MEM_CLOSE Set은 LS10/LS09 실물 도달 확인이 아니다. 이 두 망은 이번 직접 의미검토3망에 포함하지 않았다.

## 4. 전기 끝점 및 실제 PDF 확인

| 원본 | 실제 PDF | FG/제목 | 페이지별 개정 |
|---|---:|---|---|
| Electrical_Rev2.pdf | 74 | FG73 DEVIATOR DISCH SCREEN VALVE PV-03 | 기본27.05.2024, 개정칸 공란 |
| Electrical_Rev2.pdf | 127 | FG126 DIGITAL INPUT MODULE | Rev2 17.03.2025, 기본27.05.2024 |
| PID_1684n002I.pdf | 1 | 도번1684n002 PV-03 Detail | Apex I 15.01.2013, 기본06.04.2011 |

세 페이지 실제 렌더와 P&ID 상세/표제 확대를 시각 확인했다. FG 번호와 PDF 페이지를 구분하고 파일명 Rev2를 전 페이지 개정일로 사용하지 않는다.

**LS09 공급→접점→입력 양 끝점**:

1. FG73 +24Vdc10.7(시트72/9→74/0 연속 전원선)의 접속점→X1/158, 도면5×20 2A F→선73.3→LS-09 단자13.
2. 도면 LS09 접점13–14(그려진 열린 접점)→X1/159→E10.2, 교차126/3.
3. FG126/PDF127 E10.2, 역참조73/4→MOD10 단자23, CPU515 표기, 설명 LIMIT SWITCH LS-09. 126/3과73/4는 각 시트 그리드 참조이며 같은 문자열일 필요가 없다.
4. 이 끝점은0607 RID146 Input AO82/I10.2와 대응한다. 센서 케이블명·심선 색/번호·현장 중간접속·실물 단자·센서 모델은 이번 원본에서 일대일 확정하지 않았다. 도면2A F는 현행 보호값이나 교체 권고값이 아니다.

옆 LS10은 X1/160→73.4→13/14→X1/161→E10.3→MOD10 단자24다. 이를 LS09와 교환하지 않는다. LS09 리더와 열림 명칭은 자료상 대응이나 실제 로드 신장/수축과 배출방향의 0/1 대응을 확정하지 않는다.

FG73에서 함께 확인한 73KA1의 EV06 부하 접점은 **5–9**다. 110Vac9.7→5–9→73.1→X1/156→73.2→EV06 A1, A2→X1/157→0Vac9.9. 위1 단자는 부하 연결이 아니며 하단 접점표와 구분한다. LS09의24V 입력을 이110Vac EV 부하와 혼동하지 않는다. 기존69KA/71KA의5–9 정정도 변경하지 않았다.

부모 PV03의 시공 PDF34/59 케이블·LS11/12 표기와 PB17 상충은 미해결 공통 경계로 유지한다. 이번에 시공도 전체를 재검토하지 않았으며 그 번호를 LS09 현행 케이블 확정에 사용하지 않았다. 실제 결속은 최신 승인 I/O 목록·케이블대장·현장 식별사진이 필요하다.

## 5. 알람·복구

LS09 고유 독립 알람·타이머·Reset은 이번 선정 근거에서 확보하지 못했다. 부모 PV03 도달감시는 부모 공통색인 §5 및0453/LAD1819의 T111/T112, S5T#5S와 MEM 기반 피드백이다. 이 부모 타이머를 LS09 타이머로 복제하지 않았고 이번 직접 의미검토수에 넣지 않았다.

LS09 단선·고착 전용 진단 또는 두LS 모순 전용 알람을 확인했다는 주장을 하지 않는다. 부모 알람 없음/기억1/HMI 열림은 LS09 실도달·배선정상·CL09 이동 완료의 증거가 아니다. Reset 요청 수신, 알람 래치 해제, 승인 재요청, raw 변화, 실물 도달 및 재발 없음은 별도 증거가 필요하다. 현재 고장·조치·복구 증거는 없으며 현장 리셋·강제출력·우회·보호값 변경을 수행하지 않았다.

## 6. 증상별 관찰 초안

승인된 기존 관찰자료를 정리하기 위한 항목이며 통전측정·동작시험·정비 지시가 아니다. 실제 작업은 유자격자의 승인된 정지·전원/잔류압 격리 절차가 필요하다.

| 증상 | 같은 시각에 구분해 기록 | 비교 근거·배제 경계 | 추가 필요 자료 |
|---|---|---|---|
| 실물 열림인데 I10.2가0 | 실물 위치·센서표찰·접점/배선 기록·I10.2 | FG73 X1/158~159와 FG126 단자23; 정상극성 미확정 상태에서 단선 단정 금지 | 현행 배선·센서명판·정상 위치별 승인 기록 |
| raw와 DB13 처리값 불일치 | I10.2, DB13X10.2, CPU/프로젝트·시각 | IW10 Word 전달의 호출/ENO와 다른 DB쓰기 분리 | 현재 CPU 일치 및 승인된 온라인 스냅샷 |
| MEM=1이나 raw=0 | M_PV03,Q5.6,raw/DB/MEM | 0290 요청 OR 존재; LS09가 동작했다고 단정 금지 | 실제 위치와 동일시점 자료 |
| HMI 열림과 실제 상태 불일치 | DB11X80.0와 raw/DB13/DB2 각각 | CSV 설정 및0393 미결속9개 경계 | 현행 HMI 객체 이벤트·PLC 태그 결속 |
| LS09/10 모두0 또는 모두1 | 양 raw·양 처리·실물·이동시각 | 이동중/센서/배선/표기 교환 등 후보 분리; 정상진리표 미확정 | 실제 설치·기구도·정상 상태 기준 |
| 부모 알람 반복 또는 알람 없음 | 정확한 부모 알람·요청·Q·MEM·raw·시각 | MEM 기반 감시와 LS09 원시 반응을 분리 | 부모 알람/Reset 동시점 관찰 |

양식: 관찰자, 시각/시간대, 표찰/위치, 자료 수집 장치, CPU·프로젝트 식별, raw/처리/기억/HMI/실물값, 비교 원본·개정, 배제한 사실, 승인된 조치, 전후 자료, 복구 증거. 미측정은 공란으로 두며0으로 채우지 않는다. 센서 모델·정격·접점 수명·정비주기·장착간극·토크는 제조사/명판 근거 확보 전 미확정이다.

## 7. 완료·누락 및 검증

| 영역 | 적용 상태 | 남은 경계 |
|---|---|---|
| 설비·자료 | 적용 | PV03 소유/CL09 리더 확인, 실물 동일성 미확정 |
| I/O·HMI | 적용·일부 미확보 | raw/처리/MEM/표시 분리, HMI 이벤트·9핀 미결속 |
| 제어 | 입력 소비에 적용 | 전달·기억·다른DB쓰기 확인, 전체 CPU 최종값 미검증 |
| 전기 | 적용 | 두 시트 끝점 확인, 실제 케이블/모델/정상극성 미확정 |
| 알람·복구 | 부모 연계 적용·고유 미확보 | 독립 알람 신규 부여 없음, 복구 미수행 |
| 증상 관찰 | 적용 | 기록항목 초안, 실제 진단/수리 없음 |
| 완료·누락 | 적용 | 문서/정적과 UI·CPU·현장을 구분 |

### 검증 범위와 수량

- 선정 원본 **25개 전체** SHA256/고정 Git blob ID/고정blob SHA256/바이트25/25 일치. 아래 전체표 및 `extracts/LS09/source-verification.json`. 전체730원본 보존검사를 수행했다는 뜻은 아니다.
- 직접 의미검토는 **FlgNet3개**(0290 기억,0397 전달 및 타설비 반전 구분,0407 보존원문 다른DB쓰기), **선언XML8개**(0607/0608/0609/0627/0628/0629/0634/0635)의 해당 선언·DB소유, **PDF3페이지**, HMI CSV5행, 두 원본 대장 LS09행이다. 지침·인계의 읽기/해시 수는 제어망 의미검토수와 다르다.
- 정적 원문 추출, PDF 렌더·시각 확인, SHA/Git show 비교, JSON 재읽기, Wire 참조 구조검사 및 Git status 확인을 수행했다. 부모 공통망의 인용은 새 직접검사 수에 포함하지 않았다.
- 시뮬레이터/행동시험/원본 생성기/앱 빌드/TIA/CPU/현장/실운영 변경 및 업로드 미수행.

| 네 기능 | 이번 결과 |
|---|---|
| 도면·래더 비교 | FG73/126와0290/0397 연결 근거 제공; UI 구현·왕복검증 없음 |
| 백업·선택 복원 | 기존 note/repair_observation·미지필드·저장키 변경 없음; 저장/재읽기 미검증 |
| 전후 기록 비교 | 관찰양식만; 실제 기록·저장·재열기 미검증 |
| 보고서/PDF | 앱 보고서 생성·검증 없음; 원본 PDF 렌더와 구분 |

| 상태 | 결과 |
|---|---|
| documentation | draft_complete_with_gaps |
| static_review | self_review_complete; independent_review_pending |
| ui_records | not_run |
| publication | not_published_by_this_task |
| tia_compile | not_performed |
| live_cpu | not_performed |
| field_recovery | not_performed |

다음 좁은 확인: 부모의 독립 검토에서 LS09 원시/처리/기억/표시와 P&ID 리더·FG73/126 끝점을 확인한다. 현장 추가자료는 LS09 명판·장착사진·승인 I/O 및 케이블대장·위치별 정상극성·현재CPU 일치자료다. 없는 현장 자료를 새 조사 없이 반복 보류 해제로 바꾸지 않는다. 현재 CPU·실물·정상극성·현행보호값·현장복구는 미확정으로 유지한다.

## 부록 A. 선정 전체 원본 SHA256 / 고정 Git blob

경로는 source-mv06 기준, commit abcf31c5030bc7ef8749ed8e869a857f2387a28a의 전체 blob 바이트와 비교했다. 부모 초안·배정/중복 검토 JSON은 범위/탐색자료이며 아래 원본25개에 포함하지 않는다.

| 원본 상대경로 | 전체 SHA256 | 고정 Git blob | 바이트 |
|---|---|---|---|
| `AGENTS.md` | `0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2` | `073164bc6efd5791032d62c71b03b4dab48cb6f8` | PASS |
| `.agents/skills/gme-equipment-rollout/SKILL.md` | `fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b` | `9aa820ea6ca15b4e136c9772423b78ed4df6a3d4` | PASS |
| `docs/equipment-standard/WORK-STANDARD.md` | `05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99` | `f76a570cc73098632e08759b17934000f7e3a253` | PASS |
| `docs/equipment-standard/WORK-ITEM-TEMPLATE.md` | `4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586` | `e546f39535d2b589e80f97db869ac37ce4d05cfd` | PASS |
| `docs/equipment-standard/INVENTORY.json` | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` | `587c3748ad9224718f95ba06463fee913dae231d` | PASS |
| `all-in-one/registers/equipment.json` | `7870325dff32bbca90fa34507b301c4aad3347d669fddcd03b910343663996fa` | `acc42633033398216469064932c4b76987371606` | PASS |
| `VERSION.json` | `5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7` | `fffb51663b7705aec91cb119ca80ee943a4ce758` | PASS |
| `EXPANSION-WORK.md` | `ec624de9fd2fcfac861a67fd5e828b25ef46db50bfd7a37ff16e2cb54cd0f7e2` | `4c42d88ecc2d48269eb23e13a20ebf3721a092a1` | PASS |
| `WORKSPACE-HANDOFF.md` | `215096d997782e78e901dfae36c782937e49611fbeb677a0d3fa50cbecf8d074` | `dd0b8989d2376c4415bba9bd826fe6754c6b1a12` | PASS |
| `PUBLICATION_STATUS.md` | `efe4857aec598d90470322cf3962eb3fe1f64947630e1fdf71d1c90134de8740` | `d76401cf291fc0be681acc51fa898ad3ce46ff78` | PASS |
| `all-in-one/ACTIVE-WORK.md` | `eff3bbc08ecff41da3beff77f3fec48e7d148708192bcaaab00f34b6a721afc2` | `6eb947c629b5ddf9c759ef87649451303938864b` | PASS |
| `all-in-one/sources/Electrical_Rev2.pdf` | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` | `f610fd7c7ce14ae951b00cff57b969259bfb389d` | PASS |
| `all-in-one/sources/PID_1684n002I.pdf` | `2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b` | `8c83a59fefd5b8b651ec3537ea4236a073f5e109` | PASS |
| `all-in-one/sources/hmi_plc_tags.csv` | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` | `cf4c0650e7c7baac350dcb89909b808435704880` | PASS |
| `all-in-one/sources/decoded-original/0607-IdentXmlPart.xml` | `9b76b53536a26e7b45961fecbf825ae1552e16c2fd9af5736864193c01d77f93` | `dbd4da513171f04cca9b1c1741d0293c3e38f98c` | PASS |
| `all-in-one/sources/decoded-original/0608-IdentXmlPart.xml` | `24adec2035b65c0c310d637bcea74374896875b6465a16aa2f2cfc8fd55fa4b8` | `cea8f4160d2da00023b1ecc5e591b561e4a08330` | PASS |
| `all-in-one/sources/decoded-original/0609-IdentXmlPart.xml` | `395de8ebb2168848cf96fe015bd7334d71107c114a4e441ef36346b8f22031db` | `ee2aab34c0116642dd9f4364b236426f78a876a3` | PASS |
| `all-in-one/sources/decoded-original/0627-IdentXmlPart.xml` | `08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb` | `61ebc0abbb2ca160e11e1da400a3f14a397d8bc5` | PASS |
| `all-in-one/sources/decoded-original/0628-IdentXmlPart.xml` | `9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd` | `170ca5c72599edc7ea7eefe651c3680ce325e76a` | PASS |
| `all-in-one/sources/decoded-original/0629-IdentXmlPart.xml` | `67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972` | `058129bb01e27f7a6a0d0293f332d745e5bab74e` | PASS |
| `all-in-one/sources/decoded-original/0634-IdentXmlPart.xml` | `af3fcb536a6270ffb9a19e5b3f2c284a38d67d465f5147961005c1c01d11299d` | `877d9e0734dc7f3e5a8cea789eeb58a208501f48` | PASS |
| `all-in-one/sources/decoded-original/0635-IdentXmlPart.xml` | `1a057d686446a3fdab7ac61bb09bc543c52f49646c9ca71ac323c10fcdffe457` | `95bfcad59cfb0c12b573e9e8face4262d1e94622` | PASS |
| `all-in-one/sources/decoded-original/0290-FlgNet.xml` | `616ae571a3a19d97d71137ac539cc6e5c8b1db13b0e2b78ae8c1f9401098bc0f` | `2383f3b0c4a515bf25f7d0656a3bf61acbc81803` | PASS |
| `all-in-one/sources/decoded-original/0397-FlgNet.xml` | `bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834` | `4ab8370493c4e28fc1eabeeebe2743d27f0c4021` | PASS |
| `all-in-one/sources/decoded-original/0407-FlgNet.xml` | `ba022010d6f83dcebd6cce8dbd50ab2ad3744e078ad661934af970db81023927` | `2a00538bb8d3378252d671f0a5749237617b27dc` | PASS |

## 부록 B. 자체 추출·검사

- extracts/LS09/source-verification.json: 선정25개 전체 SHA256/Gitblob/바이트 결과.
- extracts/LS09/declarations.json: 해당8선언파일의 RID 원문. RID 결속은 본문의 파일/NID 문맥으로 제한.
- extracts/LS09/0290-trace.xml,0397-trace.xml,0407-trace.xml: XML 정적 정렬본이며 실행모델 아님.
- extracts/LS09/INVENTORY-row.json,equipment-row.json: 두 원본 대장 해당행.
- extracts/LS09/static-review.json: 직접 의미검토·Wire 참조 검사·금지 실행 미수행 상태.
- extracts/LS09/Electrical_Rev2-p74.png,p127.png 및 PID_1684n002I-p1.png,pid-detail.png,pid-title.png: 실제 PDF 렌더/상세 확대. p127의 전체 파일명은 Electrical_Rev2-p127.png.
