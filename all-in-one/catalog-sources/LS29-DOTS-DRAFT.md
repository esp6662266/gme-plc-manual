# LS29 고유 구성품 조사 초안

- 대상: LS29 밸브 위치 리미트 스위치, 부모 PV02, phase2 / parent_child_separate.
- 기준: GME-STD-1.0.0, source-mv06 고정 abcf31c5030bc7ef8749ed8e869a857f2387a28a, VERSION v1.12.0. 조사일 2026-10-11 UTC. 실제 모델·추론 설정 관측 미확인.
- 범위: 원본 읽기 전용 정적 조사. PV02 및 CYL-CL05~08 초안은 탐색색인/공통근거로 재사용했다. LS29 고유 원시/처리/기억과 다른 DB 쓰기, 실제 PDF 접점·양 끝점·개정·시공 상충을 독립 확인했다.
- 쓰기: 이 초안과 extracts/LS29만. 원본·공통코드·대장·버전·배포·운영·PLC·현장·보호값·SEJIN 변경 없음. 시뮬레이터 작성·수정·생성·실행·행동시험, 원본 생성기·앱빌드·업로드 미수행.

## 1. 설비·자료 기준 — 적용

INVENTORY.json catalog[240]와 TASK3-BATCH24-SCOPE.json 및 GME-CATALOG-OVERLAP-REVIEW.json의 LS29 행은 부모 PV02, component, depth1, baseline/not_assessed, parent_child_separate로 분류한다. physical_identity_verified=false를 유지한다. 같은 이름의 LS25/26/30 등은 별도 ID다. 부모 문서·게시 완료는 LS29 완료/실물 검증을 뜻하지 않는다.

PID_1684n002I.pdf 실제 PDF1의 PV-02 Detail을 직접 회전·확대했다. EV05 뒤 공압 두 선이 CL07/CL08으로 공유 분기하고 LS29 리더는 CL07 로드 측으로 내려간다. LS30 리더는 다른 쪽에 있고 CL08에는 이 리더가 직접 닿지 않는다. 오른쪽 기계도는 Gate A/B를 나눈다. OEM FG72는 LS29를 LIMIT SWITCH GATE “B” OPEN으로 명시한다. 따라서 LS29는 PV02 Gate B 열림 위치 피드백으로 문서 연결되지만 CL07 독점 감시·CL08 독립 센서·실물 장착점·정상 극성까지 확정하지 않는다. CYL-CL07과 CLIENT-CL07은 별도 이름공간이며 외부 client 신호를 가져오지 않는다.

| 원본 | 실제 PDF / 도면 | 페이지별 판본 확인 |
|---|---|---|
| PID_1684n002I.pdf | PDF1 / 1684n002, FG ‘−’ | 기본06/04/2011, Apex I, 변경란15/01/2013; 상세·제목 확대 보존 |
| Electrical_Rev2.pdf | PDF73 / FG72 LOAD DRUM CLAPPE VALVE PV-02 | DATA27.05.2024, 해당 변경란 공란 |
| Electrical_Rev2.pdf | PDF126 / FG125 DIGITAL INPUT MODULE | DATA27.05.2024, 해당 변경란 공란 |
| Electrical_Can_Decoating_20241118.pdf | PDF24 CANDC-CONS-E007-024 / D-PAGE7; PDF25 E008-025 / D-PAGE8 | ROTARY ROUTE CONDUIT PIPING(1)/(2), 개정1 24.11.11 first draft design |
| 같은 시공자료 | PDF55 CANDC-CONS-C005-055 / D-PAGE5 | CABLE SCHEDULE(4), 개정1 24.11.11 first draft design |

파일명의 Rev2를 모든 페이지에 부여하지 않는다. 시공 초안을 승인 준공도/현행 설치로 승격하지 않는다. 부모 PV02의 EV부하71KA 5–9 정정 및 CYL-CL05의0288 W65/W67 operand 정정은 공통근거로 보존하며 LS29 독립 회로로 복제하지 않는다.

## 2. I/O·HMI — 적용 / 현재값·이벤트 미확정

이하 XML 약기는 all-in-one/sources/decoded-original/ 경로다. AO는 비트 오프셋이며 RID는 그 선언 묶음·NID에서만 유효하다.

| 층위 | 원본 신호·백업 주소 | 선언 및 결속 | 해석과 경계 |
|---|---|---|---|
| 원시 입력 | EV05_Open, I9.6 Bool | 0607 RID140 SAD Input AO78, NID14 UID38 | LS29의 OEM E9.6 대응, 현재 CPU/실물은 미확정 |
| 처리 DB | Inputs.PV-02 GATE B OPEN, DB13.DBX9.6 Bool | 0609 RID141 AO78 BAD86;0608 RID86 Inputs TOD13, NID14 UID39 | 원시와 별도 메모리이며 다른 writer 존재 |
| 위치 기억 | Flag.PV_02_GATE_B_MEM_OPEN, DB2.DBX8.7 Bool | 0609 RID56 AO71 BAD5;0608 RID5 Flag TOD2, NID14 UID40 Set/42 Reset | 센서 순간값·기계 위치와 별개 |
| 명령 조건 | PV-02 GATE B EV, Q5.5 Bool | 0607 RID84 SAD Output AO45, NID14 UID83/86 | 부모 EV05 공유 구동 명령, LS29 출력 아님 |
| 공통 조건 | ON, M0.0 Bool | 0607 RID1 SAD Memory AO0, NID14 UID36 | 이름 ON인 메모리, 상수 true 아님 |

LS30 I9.7/DB13.X9.7과 B_MEM_CLOSE DB2.X8.6은 반대방향의 별도 신호다. LS29를 이 닫힘 신호나 부모 Q5.5와 병합하지 않는다.

hmi_plc_tags.csv의 PV_02\GateB_Open = DB11,X78.3(ID00077), GateB_Close = DB11,X78.4(00076), Allarme1 = DB11,X78.0(00073), Flag = DB2,X10.3(000A8)을 확인했다. GateB_Open 설정주소는 I9.6, DB13.X9.6, DB2.X8.7과 다르다. LS29 단독 HMI 명령/이벤트는 확보되지 않았다. 부모 PV02 §2.4의0392/LAD1216/NID40 HMI PV_2Gate 호출17실인수 미결속을 그대로 유지한다. 설정 CSV만으로 실제 표시 원천·객체 이벤트·현행 통신·쓰기 권한을 확정하지 않는다.

## 3. 제어 구조 — 원시→DB→기억과 다른 쓰기 적용

### 3.1 입력 Word 복사

0397-FlgNet.xml LAD1070 hmi inputs/NID1의 Move43:
- W55/ORef47/RID15 → Move43.in. 0627 RID15 Tag_181, SAD Input Word AO64 = IW8.
- Move43.out1 → W57/ORef48/RID16. 0629 RID16 Word AO64 BAD4 및0628 RID4 Inputs TOD13 = DB13.DBW8.
- Move42.eno → W53 → Move43.en; Move43.eno → W56 → Move44.en. 원본 연결이고 ENO의 현재값을 추정하지 않는다.
- Word8에는 I9.6/DB13.X9.6이 포함된다. 이 Move는 반전 연산이 없는 Word 복사다. 원시/DB가 현재 항상 동일하다는 증거는 아니다.

호출 허가는 부모 PV02 §2.3 공통근거를 재사용한다: 0030 LAD1613/NID19, CRef25 HMI Output.eno→W42→Contact37 NOT Simulation(1)(W44/ORef45)→W43→CRef28 HMI Inputs.en. 해당0030 및0688/0692/0694 선언은 이번 직접 의미검토 수에 넣지 않았다. 현재 M180.0·ENO·호출순서·CPU 활성은 미확정이며 중지 자산을 실행하지 않았다.

### 3.2 LS29 원시/처리의 병렬 읽기와 기억

0289-FlgNet.xml LAD1924 r1 scraps gate 2/NID14의 직접 확인이다. 이 구간 CRef 호출은 없다.

- W49 powerrail→Contact21.in, W50/ORef36/RID1→21.operand(ON), out W51→Contact22 및27.in.
- W82/ORef83/RID84(Q5.5)→Contact22.operand, out W53→Contact23/24.in.
- 원시 LS29: W54/ORef38/RID140→Contact23.operand, 비반전. out W55→OR25.in1.
- 처리 입력: W56/ORef39/RID141→Contact24.operand, 비반전. out W57→OR25.in2.
- OR25(Cardinality2).out W58→SCoil26.in; W59/ORef40/RID56→26.operand = B_MEM_OPEN.
- Reset: W85/ORef86/RID84→Contact27.operand(Negated), out W84→RCoil28.in; W62/ORef42/RID56→28.operand.

정적 식은 Set B_MEM_OPEN = ON AND Q5.5 AND (I9.6 OR DB13.X9.6), Reset B_MEM_OPEN = ON AND NOT Q5.5다. LS29 원시와 처리 접점 자체는 비반전이다. Q가 사라지면 기억을 Reset하는 회로이지 실제 폐쇄 확인은 아니다. Set 조건이 사라졌다고 기억이 즉시 원시값으로 돌아간다고 설명하지 않는다. CLOSE 가지의 원시 LS30와 DB는 W65/O44 및 W67/O45이며 LS29에 복제하지 않는다.

부모 자동허가/순서 소비는0609 RID56의 NID5 UID489, NID6 UID797 및 PV02 §3 공통근거로 참조한다. 이번에는 부모 전체 순서를 재조사하지 않았다. LS29에 별도 독립 출력·밸브코일·자동순서를 만들지 않는다.

### 3.3 보존된 다른 DB 쓰기 — 실행 없이 정적 확인

0411-FlgNet.xml LAD1091 simulation/NID13은 원문 보존 분석만 수행했다. 작성·수정·생성·실행·행동시험 모두 금지 상태다.
- Powerrail W21→Contact26.in. W45/ORef34/RID214→26.operand; 0636 RID214 PV-02 GATE B EV SAD Output AO45 = Q5.5, NID13 UID34/36.
- Contact26은 비반전이며 out W46→일반 Coil27.in.
- W47/ORef35/RID217→Coil27.operand. 0635 RID217 AO78 BAD5, NID13 UID35 AK=Write;0634 RID5 Inputs TOD13 = DB13.X9.6.

따라서 이 보존 네트워크에는 Q5.5를 DB13.X9.6에 쓰는 별도 구조가 있다. I9.6을 쓰는 회로가 아니며 실제 LS29 접점·실제 열림의 증거가 아니다. 그 옆 NOT Q 가지는 다른 CLOSE writer이고 LS29 열림 writer에 반전을 붙이지 않는다. 블록 이름만으로 현재 활성/비활성을 단정하지 않는다. Word 복사와 이 writer의 실제 호출순서·외부/간접·바이트/워드 중첩쓰기·현재 CPU 최종값은 미확정이다.

decoded-original의695 XML 전체에서 EV05_Open, PV-02 GATE B OPEN, PV_02_GATE_B_MEM_OPEN 선언을 탐색한 뒤 위 원본들에 결속했다. 검색 범위/일치는 declaration-search.json 및 declaration-matches.txt에 보존한다. 이름 검색695개는 의미검토695개 또는 모든 가능한 writer 전수검증을 뜻하지 않는다.

### 3.4 시작 시 Word 중첩쓰기

0147-FlgNet.xml LAD402 startup/NID2의 Move155는 B_MEM_OPEN을 포함하는 DB2.DBW8에 INT#0을 쓴다. W196/ORef176/RID54→Move155.in은0048-IdentXmlPart.xml LiteralConstant RID54(NID2 UID176) INT_x0023_0이다. Move155.out1→W197/ORef177/RID15는0563 Word AO64 BAD6,0562 RID6 Flag TOD2 = DB2.DBW8이며 DB2.X8.7을 포함한다. en은 Contact208.out→W209→155.en이며 eno W198은 Move158.en으로 이어진다. 이 확인은 해당 Word/핀 범위다. 0289의 S/R만이 유일한 기억 쓰기라고 주장하지 않는다. startup의 실제 실행·호출순서·현재 최종값은 미확정이며 초기0쓰기를 실제닫힘/실제열림 증거로 보지 않는다.

## 4. 전기 전달 끝점 — 적용

FG72/PDF73 및 FG125/PDF126를 실제 렌더로 확인했다.

| 연결 | 원본 끝점·접속 | 한계 |
|---|---|---|
| 공급 | FG72 +24Vdc10.7 수평선의 접속점→X1/149 | 인접 LS30의151 분기와 분리 |
| 보호·선 | X1/149, 5×20 2A F 표기→wire72.3→LS29/13 | 도면 표기, 현행 보호정격·교체 승인값 아님 |
| 접점 | LS-29 NO13–14, LIMIT SWITCH GATE “B” OPEN | 도면상 NO와 실제 캠 작동·정상극성·안전 상태는 구별 |
| 복귀 | LS29/14→X1/150→E9.6, 교차125/6 | LS30/E9.7과 별도 |
| PLC | FG125 상단72/4→E9.6→CPU515 MOD10 단자17 | 현행 CPU모델·채널 구성·실물 단자 미확정 |
| 모듈 공통전원 | FG125 +24Vdc10.7→X21/3010(5×20 2A IST.)→125.1→단자19; −0Vdc10.6→20 | 센서 X1/149 보호기와 모듈전원을 혼동하지 않음 |

시공 PDF55의 Cable No.5_9, 전체ID =ROT+PV02-LS29A는 FROM UC-01 ROT1TB1 → TO PV-02 LS-29, DC CVV 2C 1.0 spare0이다. 경로표에는 RD01 E400→100 RDD1→RD01 E800, adjustment4, LEN13이 기재된다. 이들은 설계표 값이고 현장 길이/포설 확인이 아니다. PDF25 ROTARY SIDE02의 분기8 Flexible16 LS29와5_9/전체ID는 PDF55와 일치한다. PDF24 공통 conduit 표에도5_9/LS29A가 있다. OEM X1/149·150과 ROT1TB1의 개별 단자·심선 결속은 확보되지 않았다.

공통 시공 상충은 보존한다: PDF24의 ROT1TB1A CORE26 대 PDF55의25G. Gate A LS25/26 짧은 번호는 PDF24 5_3/5_4 대 PDF55 5_4/5_5이고 LS29의5_9 일치와 혼합하지 않는다. PDF55 LS27/28/31/32 추가행을 LS29 별칭·CL07/08 새 센서로 추정하지 않는다. LS29 모델/제조사·IP등급·접점 정격·선색·현행 보호기·정상 극성은 승인자료/실물 확인 필요다.

## 5. 알람·복구 — 부모 관련 적용 / 독립 알람 근거 미확보

LS29 독립 타이머·알람 선언을 확보하지 못했다. 부모 PV02 Gate B 열림 미확인 감시는0452-FlgNet.xml LAD1818/NID45다. CL07 초안 §5의0451/NID44 참조는 A측을 가리키므로 좁은 정정 보강문 CYL-CL07-ALARM-REFERENCE-SUPPLEMENT.md를 별도 작성했고 수신 초안은 수정하지 않았다.

LS29 관련 기억이 읽히는 직접 근거:
- 0452 W1746/ORef1744/RID167(0657 AO71 BAD12,0655 Flag TOD2)→Contact1743.operand Negated = NOT B_MEM_OPEN.
- ON1720→Q1722→NOT MEM1743→W21→SD1645.in. S5T#7S는 W1696/ORef1677→0656 RID320, timer W1697/ORef1678→0658 RID188 Tag_86 T109.
- Timer접점1724.out W22→S1651.in; W1701/ORef1681→0657 RID189 AO87 BAD10,0655 Allarm TOD3 = DB3.X10.7 PV_02_GATE_B_NOT_OPEN.
- 알람 Reset은 ON·RESET_ALLARM·자기알람 조건의 R1656(operand W1706/ORef1684/RID189)이며 실제 복구와 다르다. 부모 전체 공통 Reset 요청의 HMI 이벤트는 미확정 범위를 유지한다.

이는 부모 Gate B 감시7초이며 LS29 자체 고장확정 또는 LS29 전용7초 보호설정이 아니다. raw/DB OR·기억/명령의 영향으로 센서 이상, 공급·배선, 기계 지연, 구동 실패를 알람 하나로 구분할 수 없다. LS30 관련 B NOT_CLOSE는 같은0452의별도 T110/DB3.X11.0이고 LS29에 복제하지 않는다. 알람을 지웠다는 사실만으로 위치·공압·현장 안전·재기동 허가를 판정하지 않는다.

## 6. 증상별 관찰 — 적용 / 현장 조치 미수행

아래는 자격자 승인절차와 에너지 격리·잔압/끼임 위험 통제 아래 확보할 관찰자료 목록이다. 통전·작동·접근 허가나 강제출력/인터록 우회/타이머 변경 지시가 아니다.

| 증상 | 같은 시각에 비교할 자료 | 배제할 오판 |
|---|---|---|
| 기계 열림인데 raw0 | 실물 LS29 표찰·캠 위치, X1/149·72.3·13/14·150, E9.6/단자17 및 I9.6 | NO 도면만으로 고장·정상 극성 단정 금지 |
| I9.6과 DB13.X9.6 다름 | IW8→DB13.W8 호출/ENO·모드, 다른 DB writer, 현재 프로젝트 | DB를 현장 센서값과 자동 동일시 금지 |
| raw0인데 기억1 | Q5.5, 처리 DB13.X9.6, 이전 Set/Reset 시점, ON | 기억을 실물 열림 증거로 단정 금지 |
| 원시1인데 기억0 | ON/Q와 동일시각 raw/DB, 0289 Set/Reset 경로 | 센서 불량으로 즉시 단정 금지 |
| HMI만 열림 표시 | DB11.X78.3의 실제 객체·전송/실인수, I9.6/DB13/MEM 및 실제 위치 | HMI 설정 CSV를 현행 이벤트 증거로 삼지 않음 |
| Gate B 열림 알람 | Q5.5·T109·B_MEM_OPEN·DB3.X10.7 및 Gate B 실제 위치·EV05/CL07·08 상태 | LS29 단독 고장 확정/반복 Reset을 복구로 취급 금지 |

관찰 기록 필드: 관찰자·시각/시간대·장비와 프로젝트 식별·LS29 표찰/위치·신호/값/단위·수집장치·도면/단자 근거·원인배제·승인된 조치·복구 확인자/증거. 실제 사용자 운영기록·사진·SEJIN 데이터는 생성·복제하지 않았다.

## 7. 완료·누락 — 문서와 현장 분리

| 구분 | 상태·범위 |
|---|---|
| documentation | complete_with_gaps:7영역·핵심 원본·끝점·소유·미확정 작성 |
| static_review | 지정 원본 직접 대조 및 해시/Gitblob 검사 완료, 부모 독립검토 대기 |
| ui_records | not_run: 도면/래더 비교·선택복원·전후비교·보고서/PDF 네 기능의 구현/저장/재열기 확인 없음 |
| publication | not_published: 초안 업로드/게시 없음 |
| tia_compile / live_cpu / field_recovery | not_performed |

필요자료와 판정 조건:
1. LS29 실물 표찰·센서 모델·캠/장착 및 Gate B 설치도. P&ID의CL07 리더와 실제소유 확인 전 physical_identity_verified 변경 금지.
2. OEM X1/149·150 ↔ ROT1TB1 개별 단자/심선표, CORE26/25G 충돌을 해소한 승인 개정 및 정상극성/보호기 실물자료.
3. 현재 CPU 프로젝트/모드·호출·중첩/간접쓰기·온라인값을 일치시킨 승인된 읽기 자료. 백업 정적 구조는 현행 값이 아니다.
4. DB11.X78.3 HMI 객체/이벤트 및0392 미결속 실인수. 같은주소 또는 비슷한이름만으로 연결 금지.
5. 승인 조치 전후의 LS29 raw/DB/MEM/부모 알람과 실제 Gate B 위치 동시관찰. 문서검사만으로 복구완료 처리 금지.

다음 조치: 부모 검토자가 고유 LS29 선언/핀·PDF 끝점·다른 DB쓰기와 별도 CL07 참조정정을 검토한 뒤 허용된 통합에서 연결한다. 새로운 현장자료 없는 미확정 반복 추정은 하지 않는다.

## 부록 A. 검사 범위 및 선정 원본 무결성

직접 의미검토는 XML22파일의 지정 부분(0147,0289,0397,0411,0451,0452;0048,0562,0563,0607~0609,0627~0629,0634~0636,0655~0658), HMI CSV1파일의 부모행, PDF3파일6페이지(PID1;OEM73/126;시공24/25/55)다. 0451/0452와0655~0658은 LS29 부모알람 연결 및 CL07 참조정정에 한정한 검토다. 전체 부모/전파일 의미검토가 아니다. 지침·대장·버전·기존 초안·network-map은 배경/식별/탐색이며 XML695개 이름검색 및 선정파일 해시검사는 PLC 의미검토 수와 구별한다.

selected-xml.txt, declaration-matches.txt, alarm-declarations.txt, PDF별png/txt 및pid-detail/title.png를 extracts/LS29에 보존했다. source-integrity.json은 아래 선정 모든 원본의 SHA256, 고정 Gitblob OID, 바이트 일치를 기록한다. 파일동등성은 CPU/현장 동일성의 검증이 아니다. 파생 batch scope/overlap와 PV02·CYL 초안은 고정 Git 원본으로 표시하지 않는다.

선정 37파일/37파일 고정 Gitblob 바이트 일치, 원본 Git 변경0. XML 의미검토22파일, 실제 PDF6페이지와 구별한다.

| 원본 경로(source-mv06 기준) | SHA256 | 고정 Gitblob OID | 바이트 일치 |
|---|---|---|---|
| AGENTS.md | `0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2` | `073164bc6efd5791032d62c71b03b4dab48cb6f8` | True |
| .agents/skills/gme-equipment-rollout/SKILL.md | `fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b` | `9aa820ea6ca15b4e136c9772423b78ed4df6a3d4` | True |
| docs/equipment-standard/WORK-STANDARD.md | `05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99` | `f76a570cc73098632e08759b17934000f7e3a253` | True |
| docs/equipment-standard/WORK-ITEM-TEMPLATE.md | `4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586` | `e546f39535d2b589e80f97db869ac37ce4d05cfd` | True |
| docs/equipment-standard/INVENTORY.json | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` | `587c3748ad9224718f95ba06463fee913dae231d` | True |
| VERSION.json | `5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7` | `fffb51663b7705aec91cb119ca80ee943a4ce758` | True |
| EXPANSION-WORK.md | `ec624de9fd2fcfac861a67fd5e828b25ef46db50bfd7a37ff16e2cb54cd0f7e2` | `4c42d88ecc2d48269eb23e13a20ebf3721a092a1` | True |
| WORKSPACE-HANDOFF.md | `215096d997782e78e901dfae36c782937e49611fbeb677a0d3fa50cbecf8d074` | `dd0b8989d2376c4415bba9bd826fe6754c6b1a12` | True |
| PUBLICATION_STATUS.md | `efe4857aec598d90470322cf3962eb3fe1f64947630e1fdf71d1c90134de8740` | `d76401cf291fc0be681acc51fa898ad3ce46ff78` | True |
| all-in-one/ACTIVE-WORK.md | `eff3bbc08ecff41da3beff77f3fec48e7d148708192bcaaab00f34b6a721afc2` | `6eb947c629b5ddf9c759ef87649451303938864b` | True |
| all-in-one/sources/PID_1684n002I.pdf | `2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b` | `8c83a59fefd5b8b651ec3537ea4236a073f5e109` | True |
| all-in-one/sources/Electrical_Rev2.pdf | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` | `f610fd7c7ce14ae951b00cff57b969259bfb389d` | True |
| all-in-one/sources/Electrical_Can_Decoating_20241118.pdf | `3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd` | `0ee6b6f8361c5790864dbba4bbd9d55e8e7c08f8` | True |
| all-in-one/sources/hmi_plc_tags.csv | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` | `cf4c0650e7c7baac350dcb89909b808435704880` | True |
| all-in-one/sources/decoded-original/network-map.json | `c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60` | `424430b6b953e43138e5d0a18ca40c949e21cfa1` | True |
| all-in-one/sources/decoded-original/0147-FlgNet.xml | `386513b215a8cc433f414b1b08279e9760e0efe209070ea95f8e445f674f428c` | `0027890eca158e714dd6260dc920a5d3aa83319b` | True |
| all-in-one/sources/decoded-original/0289-FlgNet.xml | `5460dc0d52bafeeaee0cfd2d66476f7df582002f05a6a17fb4a0928b7e750165` | `fbacf4172f1e1383998a6af80388ecc96c24572b` | True |
| all-in-one/sources/decoded-original/0397-FlgNet.xml | `bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834` | `4ab8370493c4e28fc1eabeeebe2743d27f0c4021` | True |
| all-in-one/sources/decoded-original/0411-FlgNet.xml | `282267b493e6b584959a5367d628bf86d15304d901a610614ecd2209d4d01884` | `c2143650e3de0e25c253e1652242e3cfdf4b394f` | True |
| all-in-one/sources/decoded-original/0451-FlgNet.xml | `8aeb19ab590824f4b357817cda08b46f962cec4eab5d967dcb0d829d44ca71e5` | `111d56c4bded1391beeff6073108ca1a5e2a19d2` | True |
| all-in-one/sources/decoded-original/0452-FlgNet.xml | `9612aa97393d5039ea2e0601602a924d52688e89f2d18e507eb51bfa961185e4` | `6eff580e716134fce45db223457e201bc2d5d780` | True |
| all-in-one/sources/decoded-original/0048-IdentXmlPart.xml | `d8e8687de7271bd294c2b62b33d789700af9d5014d82b130141988c4d479253d` | `64fc5a7f1ad33f3b901b00f0d22d23578ffabff8` | True |
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

정적 구조 검사: 핵심 Wire10개 모두 원본 XML 연결 일치(10/10),7영역 제목 확인. static-checks.json 참조. 행동시험·실행모델 검증이 아니다.
