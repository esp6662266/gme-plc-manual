# LS24 — MV01 닫힘 위치 리미트 독립 원본 조사 초안

- 대상: LS24 하나, 부모 MV01, 하위 구성품/component, depth1, phase2, priority_key=null. INVENTORY catalog[237], TASK3-BATCH23-SCOPE 및 GME-CATALOG-OVERLAP-REVIEW의 parent_child_separate 분류를 대조했다. 부모·LS23·ZT02 완료를 상속하지 않는다.
- 원본: source-mv06, 고정 commit abcf31c5030bc7ef8749ed8e869a857f2387a28a, v1.12.0. 2026-10-11 UTC 조사. GME-STD-1.0.0, 원본 AGENTS·skill·WORK-STANDARD·WORK-ITEM-TEMPLATE·최신 인계 상단 적용. 런타임 모델/추론 UI 증명은 미확인.
- 상태: documentation=complete_with_gaps, 독립 통합검토 전. 변경은 이 MD 및 extracts/LS24에 한정. 원본·공통코드·대장·PLC·현장·보호값·SEJIN 변경0, 시뮬레이터 작성/수정/생성/실행/행동시험0, 원본 생성기/앱 빌드0, 재위임/새 Work/Codex/업로드0.
- 부모 MV01·ZT02 초안은 탐색색인/공통근거로 재사용했다. 이번에는 고유 LS24 원시/처리 입력, 사용 핀, 전기 양끝점, 다른 writer를 재확인했으며 부모 전체 제어를 반복하지 않았다.

## 1. 설비·자료 기준 — 적용

**문서상 LS24는 MV01의 닫힘측 리미트, OEM E8.2와 PLC 원시 I8.2에 대응한다.** ‘닫힘’ 명칭, NC11–12 접점, raw I8.2, 처리 DB13.DBX8.2, 논리 NOT, HMI DB11 표시는 다른 계층이다. 이 자료만으로 0/1과 실제 완전폐쇄의 대응·현재 정상극성을 확정하지 않는다.

| 원본 | 직접 확인 위치·페이지별 판본 | 고유 대응·한계 |
|---|---|---|
| all-in-one/sources/PID_1684n002I.pdf | 실제 PDF1 확대; 도면1684n002 Apex I, 기본06/04/2011, I개정15/01/2013 REMOVED MC-05, CHANGED POWER OF FN-02 | HE01 우측 유로의 MV-01/M20에 LS-23/LS-24, 별도 ZT-02. M20의 2.2kW 440V는 LS24 정격 아님 |
| all-in-one/sources/Electrical_Rev2.pdf | FG45/실제 PDF46, MOTORIZED VALVE MV-01, 날짜27.05.2024, 개정란 공란 | LIMIT SWITCH VALVE CLOSING LS-24, NC11/12, X1/114·115, E8.2 명시 |
| 같은 OEM PDF | FG124/실제 PDF125, DIGITAL INPUT MODULE, 기본27.05.2024, **Rev2 17.03.2025** | CPU515/MOD10 단자3, E8.2, LIMIT SWITCH LS-24; 45/7 교차참조 |
| all-in-one/sources/Electrical_Can_Decoating_20241118.pdf | 실제 PDF57, CANDC-CONS-C007-057, D-PAGE7, TOTAL-PAGE57/64, Rev1 24.11.11 first draft design | 케이블7_9 HE01 FLO2TB1→MV01 LS24. 설계자료이며 준공·실측 아님 |

OEM 파일명 Rev2를 FG45의 개정번호로 복제하지 않았다. P&ID 위치/선과 OEM 제목·리미트 명칭·채널 대응은 독립 확인했다. HE01 단자함 경유가 소유를 HE01로 바꾸지 않는다. 이름 같은 다른 LS를 실물 중복으로 병합하지 않는다. EV69KA/71KA 부하5–9 정정은 보존하되 LS24 회로에 해당 릴레이를 추가하지 않는다.

본문 네 자리 번호는 all-in-one/sources/decoded-original/NNNN-FlgNet.xml 또는 명시한 NNNN-IdentXmlPart.xml이다. LAD는 network-map의 document_id 색인, NID/RID/UID/Part/Wire는 원문 문맥이다. 각 RID는 같은 블록/NID/UID와 결속하며 다른 블록의 같은 번호를 빌리지 않는다.

## 2. I/O·HMI·기억값 — 적용 / HMI 일부 미확보

| 층 | 주소·형식 | 선언·고유 핀 근거 |
|---|---|---|
| 원시 입력 | MV01_Close, I8.2 Bool | 0678 SimpleAccess Global RID205, SAD Input, SSD AO66; NID31 UID1065. 도면 E8.2 대응이며 온라인 값 아님 |
| 원시 word | Tag_181, IW8 Word | 0627 RID15, NID1 UID47, SAD Input AO64 |
| 처리 word | Inputs DB13.DBW8 Word | 0629 RID16, NID1 UID48 AK Write, SSD AO64/BAD4 + 0628 DepDBBlock RID4 Inputs TOD13 |
| 처리 리미트 | Inputs.MV01 Close, DB13.DBX8.2 Bool | 0619 GlobalAccess RID173 AO66/BAD168, NID1 UID163/182, NID14 UID28; 0618 Inputs RID168 TOD13 |
| PID 문맥의 같은 처리비트 | DB13.DBX8.2 Bool | 0668 RID126 AO66/BAD118, NID8 UID396; 0666 Inputs RID118 TOD13 |
| 다른 처리비트 writer | DB13.DBX8.2 Bool | 0635 RID256 AO66/BAD5, NID2 UID164 AK Write; 0634 Inputs RID5 TOD13. §3.5 |
| HMI 설정 | MV_01\LimitSwitchClose = DB11,X18.4, ID00315 | hmi_plc_tags.csv, Access Name PLC, dde.cfg 설정. Inputs/원시와 다른 주소 |
| 수동 닫힘 요청 | Flag.M_MV01_Close DB2.DBX3.4 | 0619 RID6 AO28/BAD5, NID1 UID166 Write; 0618 Flag RID5 TOD2. LS24 기억 상태가 아닌 부모 요청 |
| 원점절차 요청 | HMI_DB.ResetEncoderProcedure_MV01 DB41.DBX50.5 | 0619 RID196 AO405/BAD190; 0618 HMI_DB RID190 TOD41. LS24 독립 리셋 아님 |

LS24 전용 MEM_CLOSE/MEM_OPEN이나 S/R 위치기억을 확보하지 않았다. DB13 처리 메모리·부모 요청·DB8 엔코더 기억을 LS24 위치기억으로 복제하지 않는다. 한정 검토이므로 ‘PLC 전체에 기억값이 없다’고 단정하지도 않는다.

0367 LAD1190의 HMI 호출: CRef22/RID639, CodeBlock23/RID130는 0624/0623의 HMI Standard Motorized Valve를 공유 참조한다. 고유 닫힘 핀은 **W57/ORef34/RID690→Limiti_Switch_Close**, **Limit_Switch_Close_HMI→W65/ORef42/RID431**다. 핀 자체는 직접 확인했지만 이 호출의 NID/690·431 실인수 선언을 동일 문맥으로 결속하지 못했다. 따라서 Inputs.DB13.X8.2→DB11.X18.4의 완전한 전달/반전 여부는 미확정이다. 인접 MV 호출·RID숫자만으로 채우지 않는다. CSV로 실제 화면 이벤트·통신 상태·쓰기 권한을 증명하지 않는다.

## 3. 제어 구조 — 적용 / 지정 정적 경로

### 3.1 원시 word 전달과 호출

0397 LAD1070 hmi inputs NID1: 앞 Move42.eno→W53→Move43.en; W55/ORef47/RID15→Move43.in; Move43.out1→W57/ORef48/RID16. 위 선언으로 **IW8→DB13.DBW8**를 결속했다. 해당 Move는 비트 반전이 없고 DisableENO=true 속성이 있으며 원문에 뒤 Move44.en으로 가는 W56도 있다. 이 구조를 일반적인 ENO 실행 가정으로 보정하지 않는다.

0030 LAD1613 main NID19: HMI Output CRef25.eno→W42→Contact37.in, Contact37 operand는 NOT이며 W44/ORef45/RID140; Contact37.out→W43→CRef28.en. 0692 RID140은 Simulation(1), Memory AO1440=M180.0. CRef28 RID136은 0694 BlockInterfaceInfo NID19 UID28/TORID135, CodeBlock29 RID135는 0688 FCBlock HMI Inputs TOD15로 결속한다. 부모의 recipes/HMI ENO 사슬은 공통근거로 참조하며, DB13이 모든 스캔에 무조건 raw와 같은 값이라고 주장하지 않는다. 중지 자산 실행은 하지 않았다.

### 3.2 부모 닫힘 출력 및 수동 요청 해제

0342 LAD1702 Valve Control loop NID1:

- **닫힘출력의 반전 조건:** W221/ORef182/RID173→Contact270.operand(Negated). 앞 NOT Qopen Contact268.out→W269→Contact270.in, out→W271→Coil156.in. Coil156 operand W223/ORef183/RID14는 0617 SimpleAccess Output AO21, Q2.5 Start Close MV-01이다. 따라서 처리 DB13.X8.2의 NOT가 닫힘 출력 최종 직렬 조건 중 하나다. 이것만으로 출력을 요청하거나 허가하지 않는다.
- **수동 닫힘 요청의 정조건 해제:** W192/ORef163/RID173→Contact236.operand(비반전), 앞 ON 경로 W229→Contact236.in; out→W237→OR122.in1; OR122.out→W195→RCoil126.in; W197/ORef166/RID6→RCoil126.operand = DB2.X3.4. 이 OR에는 Open요청/Auto도 들어간다. LS24 신호만이 유일 해제 원인이 아니다.
- 부모 MV01 초안 §3.2의 전체 허가·상호차단·ResetProc 닫힘 OR 가지를 공유근거로 유지한다. Q2.4/Q2.5 및 44KM1/2는 MV01 소유, LS24 독립 출력/코일이 아니다. 전체 호출·현재 스캔 우선순위·실물 방향은 별도 자료가 필요하다.

### 3.3 PID 하한 입력: 원시 NOT와 다른 비반전 처리 경로

0477 LAD11 cyc_int5 ogni 100ms NID8, LRef366/RID113 CONT_S(0671), Instance412/RID71 PIDMV01 DB21(0665):

- ON Contact473 operand W424/ORef395/RID17(0670 Memory AO0); out W474가 Contact475 및 OFF Contact477로 분기한다.
- Contact475 operand **W425/ORef396/RID126 = Inputs.MV01 Close**, 비반전. out W476→OR357.in1.
- OFF Contact477 operand W426/ORef397/RID53(0670 Memory AO1). out W478→Le361.pre; W427/ORef398/RID66 = Data.Pot_MV01(0668), W428/ORef399/RID69 = Int10(0667 NID8 UID399). Le361.out W429→OR357.in2.
- OR357.out **W431→CONT_S.LMNR_LS**. 정적 접속은 `(ON AND Inputs.MV01 Close) OR (ON AND OFF AND Pot_MV01 ≤ 10)`이다. LS 입력에 NOT는 없다. ON/OFF 심볼을 현재 상수로 대체하지 않는다.

10을 현행 개도%/보호값으로 해석하거나 바꾸지 않는다. PID 9개 실인수 미결속·현재 인스턴스 동작은 부모의 미확정을 유지한다. LS24를 독립 PID로 만들지 않는다.

### 3.4 엔코더 게이트와 원점절차에 미치는 영향

0512 LAD1762 NID31은 **원시 I8.2**를 직접 읽는다. EM_OK Contact1113.out→W1114→Contact1115.in, W1088/ORef1065/RID205→Contact1115.operand(Negated). Contact1115.out W1116은 Coil1025.in 및 Add1030.en으로 분기한다. Coil1025 operand W1089/ORef1066/RID207, 0676 AO184/BAD177 + 0674 TOD91 = DB91.DBX23.0 fill_unit1.CONTROL_SIGNALS.SW_GATE0. 이는 처리 DB13.X8.2와 다른 입력 경로다.

같은 NID31에서 EM_OK W1114→NOT SW_GATE0 Contact1117→W1118→Move1047/1052의 en. W1102/O1076/R44→W1103/O1077은 0→Encoder_CH00_10, W1104/O1078/R327→W1105/O1079는 INT#0→Encoder_CH00이다(0675 상수 RID44/327, NID31 UID1076/1078). DB8.W36/DB8.DBD0에 쓰는 엔코더 처리이며 LS24 위치기억이 아니다. Add/Div·선형화·HSC 연결 세부는 ZT02 초안 §3.1–3.3을 공통 참조한다. SW_GATE0 해제·소프트웨어0쓰기·실제 count=0·실제 완전폐쇄는 등치하지 않는다.

0354 LAD1703 NID14는 **처리 DB13.X8.2**를 읽는다. ResetProc Contact21(W35/O27/R196)→W36→Contact22, W37/O28/R173→Contact22.operand(비반전), out W38→Move23.en. W39/O29/R194=0(0620)→Move23.in, out1 W41/O30/R201→MV01_Encoder.NewCountValue. Move23에는 DisableENO=true지만 W40 Move.eno→NOT SetCountValue Contact24→W43 Coil25→W45 RCoil26가 원문에 있다. Coil25 W44/O32/R202, RCoil26 W46/O33/R196. 실제 ENO 실행·HSC 접수/완료를 추정하지 않는다.

NewCountValue는 0619 RID201 DInt SSD S AO320, SetCountValue는 RID202 Bool SSD IO AO288이며 일반 절대 DB offset으로 치환하지 않는다. ZT02 초안의 HSC SetCountValue 실인수 미결속과 부모 ResetProc의 닫힘 구동 영향은 그대로 남긴다. 리셋 조작·원점이동·교정을 실행/권고하지 않았다.

### 3.5 보존 XML의 다른 DB 쓰기 — 정적 대조만

0403 LAD1083 simulation NID2의 LS24 writer만 보존 원문으로 확인했다. 작성·수정·생성·실행·행동시험을 하지 않았다.

- Powerrail W21→Le348.pre. W153/ORef158/RID248→Le348.in1; 0635 RID248 Int AO1184/BAD247, 0634 Data TOD1 = DB1.DBW148 Data.Pot_MV01.
- W157/ORef159/RID254→Le348.in2; 0637 LiteralConstant RID254 NID2 UID159, Int V2.
- Le348.out→W162→일반 Coil349.in; W163/ORef164/RID256→Coil349.operand, **DB13.DBX8.2**.
- 보존문서의 이 writer는 Pot_MV01 ≤ 2의 비교 출력이다. 물리 I8.2에 쓰는 회로가 아니며 실물 극성을 입증하지 않는다. 블록 이름만으로 현재 활성/비활성을 확정하지 않는다. 원시 word복사와 이 DB writer의 실제 실행순서·외부/간접쓰기·현재 CPU 최종값은 미확정이다.

## 4. 전기 전달 끝점 — 적용

실제 렌더에서 접속점·연속선·NC접점·교차참조 양끝을 확인했다.

| 순서 | FG45/PDF46 → FG124/PDF125 연결 | 해석·경계 |
|---|---|---|
| 공급 | +24Vdc 10.7 수평선(44/9→46/3)에서 접속점으로 LS24 분기 | ZT02 B단자의 37.1/37.2 공급과 다른 가지 |
| 단자·보호 표기 | X1/114, 5×20 2A F → 선45.4 | 도면상 표기. 실제 장착 퓨즈/현재 보호값을 확인한 것 아님 |
| 센서 접점 | LS-24 NC11–12 | LIMIT SWITCH VALVE CLOSING. 캠 작동/기계 폐쇄에서의 접점 상태는 미확정 |
| 복귀 | LS24 12→X1/115→E8.2, 교차124/3 | X1/113/E8.1은 LS23이므로 혼합 금지 |
| PLC 쪽 끝점 | FG124의 E8.2, 상단45/7→CPU515 MOD10 **단자3** | LIMIT SWITCH LS-24. 현재 CPU형식·채널 구성·실물 일치 미확정 |

이 입력 접점은 부모 전력회로의 직렬 하드웨어 차단 접점이라고 단정하지 않는다. FG44의 모터 전력/접촉기 인터록은 부모 공통근거이며 이번 LS24 직접 경로는 FG45/124다.

시공 PDF57의 고유/공유 행:

| 행 | 케이블 및 FROM→TO | 설계 기재 |
|---|---|---|
| 7_9 고유 | =FLA+MV01-LS24A, HE-01 FLO2TB1 → MV-01 LS-24 | DC, CVV, 2C, SIZE1.0, SPARE0, ROUTE E120, adjustment5, LEN5 |
| 7_1 공유 | =FLA+HE01-FLO2TB1A, CR → HE-01 FLO2TB1 | LS17/18/23/24/21A/22A/21B/22B 묶음, DC CVV25G SIZE1.0 SPARE8, routes100/110 LAD1/E100, adjustment5, LEN50 |

고유 2심케이블과 공유25심 묶음을 구분했다. 길이는 설계 표 값이며 실측으로 보고하지 않는다. 시공표에 OEM X1/114·115와 대응하는 단자함 양끝 번호/심선색은 없다. 준공 결선표·단자함 표찰·센서 모델 자료가 필요하다. 인접 ZT02 AI/OEM A-B 상충은 ZT02 초안의 별도 쟁점으로 유지하며 LS24를 AI로 재분류하지 않는다.

## 5. 알람·복구 — 부모 의존 / 고유 알람 미확보

이번 LS24 범위에서 독립 고장비트·지연 타이머·고유 S/R 알람을 확보하지 않았다. 확인한 기능은 닫힘 출력 차단조건·부모 수동요청 해제·PID 하한·엔코더 게이트·원점절차의 조건이다. 개별 LS 고장이 반드시 별도 알람으로 잡힌다고 약속하지 않는다.

MV01 초안 §3.4–3.6 및 알람 영역의 MV01_FAULT DB3.X4.7, Tag92=T4 S5T#150mS 응답 불일치와 W33>2000/W34<−2000 명령 누적은 **부모 공통근거**다. LS24의 센서 지연/행정시간/보호값으로 복제하지 않았다. Pot_MV01_OFR는 ZT02 위치 선형화 출력이며 LS24 독립 알람이 아니다. 이번에는 부모 알람 전체를 의미 재검토하지 않았다.

LS24 입력 또는 HMI 표시가 변했다는 사실만으로 실제 폐쇄/고장 해제/복구 완료를 승인하지 않는다. ResetProc 해제·SetCountValue 쓰기·0표시는 서로 다른 사건이다. 현행 보호값 변경, 강제입력/출력, 점퍼, 리셋·원점이동을 수행하거나 지시하지 않는다.

## 6. 증상별 관찰 — 안전한 증거 수집 항목

아래는 이미 승인된 관찰자료의 기록 기준이며 현장 조작 절차가 아니다.

| 증상 | 구분해서 확보할 자료 | 판정 경계 |
|---|---|---|
| 닫힘 표시가 실제와 다름 | 관찰시각, 기계위치 근거, LS24 표찰/캠/모델, I8.2, DB13.X8.2, DB11.X18.4 | NC명칭 또는 비트1만으로 실제 폐쇄 판단 금지 |
| raw는 변하나 처리 DB는 그대로 | IW8/DB13.W8, main 호출조건 M180.0, 0397 경로와 다른writer 자료 | 시뮬레이터를 켜거나 시험하지 않음; 현재 스캔/프로젝트 판본 필요 |
| 수동 닫힘이 유지되지 않음 | DB2.X3.4, Auto/Open 요청, DB13.X8.2, Q2.5 시계열 | LS만의 문제로 단정하지 않음; OR 해제와 기타 허가 구분 |
| PID와 닫힘 표시가 다름 | DB13.X8.2, ON/OFF, Pot_MV01, LMNR_LS 결속/현재 인스턴스 | ≤10 보조비교와 물리 LS 구분, 설정변경 금지 |
| 위치계값이0 또는 고정 | raw I8.2, EM_OK, SW_GATE0, DB8.W36/DB8.DBD0, ZT02값 | LS24·엔코더·소프트웨어0쓰기 중 하나로 성급히 단정하지 않음 |
| 원점절차 후 이상 | 승인된 절차 기록, ResetProc/처리 LS/부모 Q/SetCountValue와 실제 HSC 응답 | ResetProc를 표시 초기화로 취급하지 않음; 재실행 권고 없음 |
| 배선 자료가 다름 | X1/114·115, MOD10 단자3, 7_9와 공유7_1 양끝 표찰/준공도 | 설계문서 중 현재 우선판본을 임의 선택하지 않음 |

관찰자·시각/시간대·자료 취득 위치·태그/주소/형식·값/단위·CPU/프로젝트 판본·비교 문서·조치 승인·복구 증거를 별도 기록한다. 개인/실제 운영 사진·기록을 공개 원본 저장소에 복제하지 않는다.

## 7. 완료·누락·인계 — 문서 범위 완료, 현장 미확정

| 7영역 | 판정 | 남은 자료 |
|---|---|---|
| 설비·자료 기준 | 적용, 문서대응 확인 | 현재 실물 모델/캠 위치/준공판본 |
| I/O·HMI | 적용, 원시/처리 선언 확보 | HMI 닫힘 2핀 동일 문맥 결속·현재 표시경로 |
| 제어 | 적용, 지정8개 네트워크의 LS 관련 경로 | 전체 호출/스캔순서·간접/외부 writer·현재 CPU |
| 전기 끝점 | 적용, FG45/124 및 시공57 확인 | 단자함 양끝/심선표·현재채널/퓨즈/정상극성 |
| 알람·복구 | 부모 의존, LS 독립항목 미확보 | 현재 고장 진단과 승인된 복구 관찰 |
| 증상 관찰 | 적용, 수집항목 문서화 | 실제 관찰과 승인된 조치 기록 |
| 완료 기준 | documentation complete_with_gaps | 독립 검토·UI·게시·TIA/현장 상태 분리 |

- 원문 XML695개를 LS[-_ .]?0?24 경계 패턴으로 검색했으며 문자열 직접 일치0개였다. 이는 검색수이지695개 의미검토 완료가 아니다. 원시 MV01_Close 및 Inputs.MV01 Close 선언·핀은 독립 대조했다. 이름 직접 일치0을 신호 부재로 해석하지 않는다.
- 직접 의미 검토: FlgNet8파일의 LS 관련 경로(0030/0342/0354/0367/0397/0403/0477/0512), 선언의 지정 RID/NID/UID, 실제 PDF4페이지(P&ID1/OEM46·125/시공57). 각 파일 전체/부모 전체를 의미검토한 수량이 아니다.
- preflight 읽기 전용 대장 일치 검사 통과. 해시검사와 의미검토는 구분했다. 모든 선정 원본의 전체 SHA256 및 고정 Git blob 바이트 일치는 부록 A/검사JSON에 있다.
- 도면·래더 비교, 백업·선택복원, 기록 전후비교, 보고서/PDF의 네 UI 기능은 **구현/저장/재열기 미검증**. 문서 분석을 BC01 동등 기능 완료로 표시하지 않는다.

| 상태 | 결과 |
|---|---|
| documentation | complete_with_gaps, LS24 한 ID 초안 |
| static_review | scoped_completed, 지정 원문/실제 PDF·해시 대조 |
| ui_records | not_run |
| publication | not_published, 첨부·통합은 부모 담당 |
| tia_compile / live_cpu / field_recovery | not_performed |

다음 필요한 한 작업은 **LS24 실물·캠/준공 단자함 자료 및 현재 프로젝트/HMI export를 확보해 정상극성과 두 표시핀 결속을 검토**하는 것이다. 새 자료 없이 같은 현장 보류를 반복하지 않는다. 이번 조사에서는 원본/중지 자산을 변경하거나 실행하지 않았고, 원본 Git status는 깨끗했다.

## 부록 A. 선정 원본 전체 SHA256 / 고정 Git blob 바이트일치

선정 39개 전부 고정 커밋의 blob와 byte-for-byte 일치한다. 이 수는 파일 보존검사수이며 전수 의미검토수 또는 문서 완료 설비수가 아니다.

| 원본 경로 | SHA256 | Git blob (고정/현재 동일) | 바이트 일치 |
|---|---|---|---|
| docs/equipment-standard/INVENTORY.json | 720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc | 587c3748ad9224718f95ba06463fee913dae231d | true |
| all-in-one/sources/PID_1684n002I.pdf | 2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b | 8c83a59fefd5b8b651ec3537ea4236a073f5e109 | true |
| all-in-one/sources/Electrical_Rev2.pdf | 5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6 | f610fd7c7ce14ae951b00cff57b969259bfb389d | true |
| all-in-one/sources/Electrical_Can_Decoating_20241118.pdf | 3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd | 0ee6b6f8361c5790864dbba4bbd9d55e8e7c08f8 | true |
| all-in-one/sources/hmi_plc_tags.csv | a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404 | cf4c0650e7c7baac350dcb89909b808435704880 | true |
| all-in-one/sources/decoded-original/network-map.json | c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60 | 424430b6b953e43138e5d0a18ca40c949e21cfa1 | true |
| all-in-one/sources/decoded-original/0030-FlgNet.xml | 9252c9da764993de1edb8b2e44c46d6e9f9d4b6118e751a0dbeaa9ffd8ea721b | e74c70b751acdcdbc7a8b3b0c98aa773c2107cab | true |
| all-in-one/sources/decoded-original/0342-FlgNet.xml | 9ef93abad16cc055509ef98c388417c716cb03d23cb02aed6d95888beb43bef8 | a9b1841964216331887d18f91c014c0534cc9df1 | true |
| all-in-one/sources/decoded-original/0354-FlgNet.xml | 626eb4d21b9409ae50ed32436972c8a4284fcc029c10db5c5529463544b2ffbd | b7ee6b7ad489e1f2853941aae23aefb3058475ef | true |
| all-in-one/sources/decoded-original/0367-FlgNet.xml | 7e1a0c6776177463d5ffe7307a991484f97e8e5c5863f00d9597950458482bc5 | fc6017ddea1f08526c317d5f76b3ae3ca98c02e4 | true |
| all-in-one/sources/decoded-original/0397-FlgNet.xml | bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834 | 4ab8370493c4e28fc1eabeeebe2743d27f0c4021 | true |
| all-in-one/sources/decoded-original/0403-FlgNet.xml | 77b03e38aa857ac8dd404f2f66a56256939b4e7924b41334a7981b86089c1e6b | 4c806e31eb65f00cbb7870c72896ac26a8bc3dd3 | true |
| all-in-one/sources/decoded-original/0477-FlgNet.xml | e7b5b0cb95c60d1112081f6129a3127f8413e1b1d2a4c67d0e203d36ea0a711a | 8bc2088bf4bb5eb8d51e0d9186879fc61d2c27df | true |
| all-in-one/sources/decoded-original/0512-FlgNet.xml | 9437caf0fc524d25925ca5beb3c3bf1a2a0709a478a2981e42e5abe1e4471795 | d0402898b8f7949733aa7d94af18d0978a766322 | true |
| all-in-one/sources/decoded-original/0617-IdentXmlPart.xml | 10bcf85169cb2512f55acadaef299a3d46b4b4cecd88032d739cfeba23e94aa9 | 9527658ee6808be34bd513b1b2ebaf3a4a5a6f3e | true |
| all-in-one/sources/decoded-original/0618-IdentXmlPart.xml | 0c6762de9cdf0e294317f7463bea3d8e6df5673d333d9b1826ebd17a7ded044c | 9eec0dbd8abde4aa7295f77b63ad473f895f274b | true |
| all-in-one/sources/decoded-original/0619-IdentXmlPart.xml | 85694bb5b696e31e6a1217431112e5b750516c4f94078d6e127d4394a8b80456 | 11f0502c84a1f319a21459a35c0dc1c6ce8e8f36 | true |
| all-in-one/sources/decoded-original/0620-IdentXmlPart.xml | da97226a148a1a8babaea67db412761a718b7e7537212b7807e8ea27d000d2d3 | dc88b5e87ad3331928f14fcf647673a26fb70b6b | true |
| all-in-one/sources/decoded-original/0623-IdentXmlPart.xml | 4acd00406ea92466169e57e59fc90b0da4d9ec55fd19e2e96c9556e939cb83a6 | 13b3af0459c8e6069bb9b2f1b16454bf479e08dc | true |
| all-in-one/sources/decoded-original/0624-IdentXmlPart.xml | 24607c0827fbde428bccf8637ef4ae490798a69a7c2f3b87861d0749082d367a | 02511fea47fc47981c101bba49dc40adde1cdcc3 | true |
| all-in-one/sources/decoded-original/0627-IdentXmlPart.xml | 08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb | 61ebc0abbb2ca160e11e1da400a3f14a397d8bc5 | true |
| all-in-one/sources/decoded-original/0628-IdentXmlPart.xml | 9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd | 170ca5c72599edc7ea7eefe651c3680ce325e76a | true |
| all-in-one/sources/decoded-original/0629-IdentXmlPart.xml | 67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972 | 058129bb01e27f7a6a0d0293f332d745e5bab74e | true |
| all-in-one/sources/decoded-original/0634-IdentXmlPart.xml | af3fcb536a6270ffb9a19e5b3f2c284a38d67d465f5147961005c1c01d11299d | 877d9e0734dc7f3e5a8cea789eeb58a208501f48 | true |
| all-in-one/sources/decoded-original/0635-IdentXmlPart.xml | 1a057d686446a3fdab7ac61bb09bc543c52f49646c9ca71ac323c10fcdffe457 | 95bfcad59cfb0c12b573e9e8face4262d1e94622 | true |
| all-in-one/sources/decoded-original/0637-IdentXmlPart.xml | 3fb68f57dbe2a877c4ad5aa1b3316810cf84958f2d13b5b1d7d321e0915271c7 | cb1d7fb76aa2afd96eb46984cc1e71b77f36395c | true |
| all-in-one/sources/decoded-original/0665-IdentXmlPart.xml | 50e88d5f50f555151b35cfb17225e766c34ef6b490bd3a48e0a4e335fd17e3dd | ea4a8a5013081f648722c5ebbde3bb1366787990 | true |
| all-in-one/sources/decoded-original/0666-IdentXmlPart.xml | 19a9ccb83ad7070d23726250870d0ca0c33d797ab9ffe679c9d2c0d109cc95e6 | b6130b32498b6fee0d9e4db7a04dc79f785e1fbb | true |
| all-in-one/sources/decoded-original/0667-IdentXmlPart.xml | ef924ced3e0e2b17e9c8440eb4946cd50d55df644c6ec24a1c4fd288fa6b73a3 | 7f2e1798eb9f260d19d038a83369484d0f438856 | true |
| all-in-one/sources/decoded-original/0668-IdentXmlPart.xml | 2248e994a0a02cd37c5c5edaca199b3421068feea91e2e8616560e814ef9f6ed | fe0f30d1eaae37783b0f03cb090353b3a3de3600 | true |
| all-in-one/sources/decoded-original/0670-IdentXmlPart.xml | e56f3f0c4f2a86dd18578dedd4453915c2a51cd25e2cd9feced8538171a00841 | b9466007b14e5c4f5d353dca5734401317e2dc03 | true |
| all-in-one/sources/decoded-original/0671-IdentXmlPart.xml | 26cb51706305c372d512c19770648bb0dbb74df8bd2277b1e0da1b8c88cca293 | e38a4e2c93ac8093e2b0b8e082a64688b5d9845e | true |
| all-in-one/sources/decoded-original/0674-IdentXmlPart.xml | 4770702f519bacda69202bb2f7733d983074bda90964360c238f990d9d08fd84 | f210593944547b63eab10c667348711413600aab | true |
| all-in-one/sources/decoded-original/0675-IdentXmlPart.xml | b1902886927d8403fab736d9c8ffe73f2fbc8ce4b7ca7c345144964668b051c3 | d82a33b173c8dc0737fd890eb2a63a88a07d0831 | true |
| all-in-one/sources/decoded-original/0676-IdentXmlPart.xml | c58427c5b0ac6c11cdb52e4c6d0461c7b191fae81ccace191048e9f175fcec59 | 1ed67265f69796a4e659f9438e551068037f33a4 | true |
| all-in-one/sources/decoded-original/0678-IdentXmlPart.xml | 51e637e0b9713c028810f2a717b5c3804a3a26c2f1be7e332a4d6bf277bfc382 | 7fafb2297bcdf739bf1d1dd68cebc0d74f2a40cc | true |
| all-in-one/sources/decoded-original/0688-IdentXmlPart.xml | ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda | 463585759f1ecd94f32362b4fefb000a152f5773 | true |
| all-in-one/sources/decoded-original/0692-IdentXmlPart.xml | bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037 | 737785d03b5fad43c5b4d451955726d800edb1c0 | true |
| all-in-one/sources/decoded-original/0694-IdentXmlPart.xml | 757ccebdf32d0a168dd787bfa735fe6494eac4c4a9f7a5adc63898a88e8b152d | c45e8f3ca4129dc06734f6a12ef79e6ed6528a7d | true |

## 부록 B. 실제 검사 기록

- 2026-10-11 UTC, `extracts/LS24/check_static.py`의 원문 XML 구조·문서 정적 검사 **17/17 통과**. 원시/처리 입력의 반전 차이, PID LMNR_LS 핀, Move DisableENO, 다른 writer Coil·비교식, HMI 두 닫힘핀, 7영역·전체 해시표·원본 Git 상태·preflight를 대조했다.
- 선정39원본 전부 SHA256 계산 및 고정 commit Git blob/원본 바이트39/39 일치. 해시검사 범위는 선정39개이며 원본 트리 전체 의미검토가 아니다.
- 보존·검사 JSON: `extracts/LS24/source-hashes.json`, `checks.json`, `preflight.json`, `literal-search.json`, `catalog-review.json`. 선언 부분 추출과8개 FlgNet 정적 보기, 실제 PDF4페이지 및 P&ID 확대 이미지를 같은 전용 폴더에 보관했다.
- 검사 스크립트는 원문을 파싱·단언하는 문서 검증일 뿐 PLC 논리의 실행·모델 생성·시뮬레이터·행동시험이 아니다. 원본 생성기·앱 빌드·PLC/현장 조작을 수행하지 않았다.
