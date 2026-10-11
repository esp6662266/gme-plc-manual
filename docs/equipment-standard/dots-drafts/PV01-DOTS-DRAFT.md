# PV01 P05 설비 고유 근거와 문서 초안

- 문서: **PV01-DOTS-DRAFT.md / 1차 조사·통합 검토용**
- 작성: 2026-10-11 KST, Dots 자체 조사. 대상은 PV01(P05) 한 개.
- 기준: GME-STD-1.0.0. 공개 esp6662266/gme-plc-manual의 main/all-in-one/.
- 고정 조사 커밋: **f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f**, 프로그램 v1.8.0. FN06 게시 상태는 사용자 확인 보고이며 이 초안의 게시 실적이 아니다.
- 수신자: 사용자 및 기존 GME Codex 검토·통합 담당. 이 파일은 승인된 연구 초안이며 현장 운전·정비 지시서가 아니다.
- 결과: 원본 선언과 Part/Wire로 PV01의 두 출력, 위치 기억, 0~5 순서, A 4초/B 7초 알람 및 공통 제어 소유를 추적했다. HMI 호출의 개별 실인수 결속, 현행 CPU/정상 극성/현재 설정/현장 복구는 미확정이다.
- 접근: 공개 저장소 표준·템플릿·INVENTORY와 원본 XML/PDF를 직접 사용했다. 제공 환경에서 tia-equipment-alarm-trace 로컬 스킬은 확보하지 못했고 권한 확장은 하지 않았다. PDF 원본을 렌더링하여 실제 페이지·개정란을 확인했다. Mac 전용 인계 파일은 이 조사에 사용하지 않았다.
- 변경: 이 MD만 산출한다. 공통 코드·버전·대장·배포·운영 기록 및 기존 PV01 자료는 편집하지 않았다. 시뮬레이터·생성기·행동시험·실제 PLC·현장·보호값 변경은 수행하지 않았다.

## 먼저 검토할 핵심

1. **PV01 A 감시는 4초, B 감시는 7초**다. 다른 게이트의 값으로 통일하면 안 된다. 감시 대상은 원시 센서 자체가 아니라 Flag.PV_01_GATE_*_MEM_OPEN/CLOSE다. [E12~E15]
2. 자동 순서의 A 닫기→B 열기, B 닫기→A 열기 사이에는 각각 **1초 타이머**가 있다. 해당 전이 접점에 닫힘 기억 조건이 없으므로 “닫힘 센서 확인 후 다음 게이트 열림”이라고 쓰면 원본과 다르다. [E08]
3. 최종 Q5.2/Q5.3에는 자동 명령 외에 현장 요청과 maintenance PV01 병렬 경로가 있다. B 출력에는 OFF **비반전 접점**도 있다. ON/OFF는 M0.0/M0.1 메모리이며 참/거짓 상수가 아니다. [E04,E07]
4. Enable_R1_GATE=0만으로 모든 명령을 차단한다고 단정할 수 없다. 자동·현장·유지보수 경로와 출력 소유를 따로 표시한다. 자동 허용부는 NOT_OPEN 두 알람을 직접 사용하며 NOT_CLOSE까지 같은 위치에 있다고 합치지 않는다. [E05~E07,E19]
5. FG124의 LS02/I8.7에는 **SPARE** 표시가 있지만 FG70의 LS02 회로와 원본 입력 선언은 존재한다. 삭제·미설치·극성 확정 근거가 아니다. [E02,E22]
6. P&ID의 EV01→CL01/02, EV02→CL03/04 묶음은 읽을 수 있다. 같은 상세도의 GATE A/B 기계 배치 문자만으로 전기도면의 A/B를 실물 상·하 게이트에 확정 배정하지 않는다. [E01,E24]
7. 도면 파일명이 Electrical_Rev2여도 모든 페이지가 Rev2는 아니다. **FG69·70·125 개정란 공란, FG124·141 Rev2/17.03.2025**를 각각 기록한다. [E20~E23]

## 1 설비와 자료 기준

### 1.1 대상과 관계

INVENTORY의 P05는 catalog_id PV01, mapping tag, **identity_verified=false**다. 역할은 드럼 투입측 A/B 공압 게이트이며 설비 분류는 gate, parent_id=null이다. “태그 대응”과 “현장 본체 동일성 확인”을 구분한다. [E01]

- 전기 제어 기준 A: PV-01 Gate a Q5.2 → 69KA1 → EV01, 위치 LS01/LS02.
- 전기 제어 기준 B: PV-01 GATE B EV Q5.3 → 69KA2 → EV02, 위치 LS05/LS06.
- P&ID는 compressed air와 EV01/02, CL01~04를 그린다. 원본 블록의 r1 scraps gate 2 또는 기존 유압 관련 서술만으로 유압 구동을 확정하지 않는다.
- 독립 모터·인버터 전류/회전수·모터 보호 설정은 이 PV01 EV 제어 회로에 해당하지 않는다. 타 설비 모터 데이터를 이 게이트에 복제하지 않는다. 공압 손실·밸브 스풀·실린더·기계 끼임은 별도의 미확인 현장 원인이다.
- BC01은 PV01과 연동되는 상류 설비이며 PV01의 하위 모터가 아니다. R1_GATE_LOOP_ON이 BC01 시작 요청에 쓰이는 범위만 연결한다. [E19]

### 1.2 기존 자료 보존

all-in-one/PV01-detail/의 매뉴얼 rev0.1, I/O·HMI·내부 태그·verification CSV, evidence JSON, 과거 HMI 이미지와 기존 unresolved 항목을 보존한다. 이번에 해소한 것은 일부 **정적 논리 결속**이다. 기존 문서의 현장 확인 필요 사항을 “완료”로 바꾸지 않는다. 과거 simulation-tests CSV를 포함한 중지 자산은 실행·편집하지 않았다. [E25]

과거 HMI HMI_DECOATER.png에는 2026-10-07 시각과 PV01 A/B 도형이 보인다. 이는 저장 이미지의 표시에 한정되며 현재 CPU 운전·Maintenance 활성·현장 위치가 아니다. 이미지의 다른 설비와 숫자는 PV01 운전 근거로 전용하지 않는다. [E18]

### 1.3 원본 읽기 규칙

본문에서 0449 등 네 자리 번호는 all-in-one/sources/decoded-original/0449-FlgNet.xml, 0607 등 선언 번호는 같은 폴더의 0607-IdentXmlPart.xml을 뜻한다. LAD 번호는 network-map.json의 document_id다. NID는 원본 선언 CS의 네트워크 식별자이고 문서의 index_order와 다를 수 있다. UID/RID만 같다고 다른 블록 선언을 합치지 않았다. 미결속 실인수는 후보로 남겼다. 고정 URL·SHA-256은 부록에 있다.

## 2 I O와 HMI

### 2.1 PV01 물리 주소와 도면 끝점

모든 주소는 **백업 선언 주소**다. 현재 다운로드 주소나 실물 정상 극성으로 확정하지 않는다. [E02~E04,E20~E23]

| 구분 | 백업 심볼·주소 | 원본 선언 | OEM 도면 끝점 |
| --- | --- | --- | --- |
| A 열림 | EV01_Open / I8.6 Bool | 0607 RID124, SAD Input AO70, NID11 UID38 | LS01 13/14, X1 130/131, FG70→FG124 MOD10 단자7 |
| A 닫힘 | EV01_Close / I8.7 Bool | 0607 RID126, Input AO71, NID11 UID44 | LS02 13/14, X1 132/133, FG70→FG124 MOD10 단자8; SPARE 상충 |
| B 열림 | EV02_Open / I9.0 Bool | 0607 RID129, Input AO72, NID12 UID40 | LS05 13/14, X1 134/135, FG70→FG125 MOD10 단자11 |
| B 닫힘 | EV02_Close / I9.1 Bool | 0607 RID131, Input AO73, NID12 UID42/48 | LS06 13/14, X1 136/137, FG70→FG125 MOD10 단자12 |
| A 현장 요청 | EV01_Sel_Open / I9.2 Bool | 0607 RID43, Input AO74, NID3 UID349 | 70SB1→70SA1 A→X1/139→FG125 MOD10 단자13 |
| B 현장 요청 | EV02_Sel_Open / I9.3 Bool | 0607 RID45, Input AO75, NID3 UID351 | 70SB1→70SA1 B→X1/140→FG125 MOD10 단자14 |
| A 열림 출력 | PV-01 Gate a / Q5.2 Bool | 0607 RID50, Output AO42, NID4 UID394 Write | FG141 MOD15 단자13 A5.2→69KA1 A1/A2→접점1/9→EV01 |
| B 열림 출력 | PV-01 GATE B EV / Q5.3 Bool | 0607 RID49, Output AO43, NID4 UID390 Write | FG141 MOD15 단자14 A5.3→69KA2 A1/A2→접점1/9→EV02 |

I/O의 AO는 비트 오프셋이다. 70=8×8+6, 42=5×8+2로 주소를 대조했다. 도면의 E/A 표기는 PLC I/Q와 교차 대조한다. 오래된 주석 A57.0, A48.4를 현행 Q 주소로 사용하지 않는다.

### 2.2 처리 Inputs와 원시 입력의 차이

0286/0287은 위치 기억 설정 때 원시 입력과 Inputs DB 멤버를 **병렬 OR**로 읽는다. 명칭이 같아도 서로 다른 읽기 경로다. [E03,E10,E11]

- 0608 DepDBBlock RID86 Inputs, TOD N13.
- 0609 RID125 Inputs.FC GATE A OPEN AO70 → DB13.DBX8.6.
- RID127 Inputs.LIMIT SWITCH LS-02GATE A CLOSEDVALVE PV-01 AO71 → DB13.DBX8.7.
- RID132 Inputs.PV-01 GATE B OPEN AO72 → DB13.DBX9.0.
- RID133 Inputs.LIMIT SWITCH LS-06GATE B CLOSEDVALVE PV-01 AO73 → DB13.DBX9.1.

추가로 0397(LAD1070) **Move43**의 in은 W55/ORef47→0627 RID15 Tag_181, Word/Input AO64 = IW8이다. out1은 W57/ORef48→0629 RID16 Word/AO64/BAD BIRID4, 0628 RID4 Inputs TOD13 = DB13.DBW8이다. 즉 백업에는 **IW8→Inputs DB13 Word8** 전달이 있다. Word8 범위가 위치 4비트를 포함한다. Move42.eno→W53→Move43.en, Move43.eno→W56→Move44.en 연결도 보존한다.

호출 경계는 0030(LAD1613, 원본 NID19): Recipes Handler CRef21.eno→W32→HMI CRef23.en→W33→HMI Output CRef25.en; 그 eno→W42→NOT Contact37(Simulation(1) ORef45/W44)→W43→HMI Inputs CRef28.en이다. 선언은 0688 RID120/124/128/135와 0692 RID140(M180.0), 인터페이스 0694 RID136이다. **이는 백업의 호출 조건만 확인한 것**이다. 현재 M180.0·ENO·CPU 스캔·다른 DB 쓰기·실제 입력값은 미확정이다. 중지된 시뮬레이터를 실행하거나 복구하지 않았다. [E03]

### 2.3 내부 주소와 소유

| 심볼 | 백업 주소·형식 | 선언과 쓰기/읽기 |
| --- | --- | --- |
| ON / OFF / UNDER TESTING | M0.0 / M0.1 / M5.5 Bool | 0607 RID1/48/4; 메모리 읽기이며 상수 아님 |
| Open EV A 00 / B 00 PV-01 | M20.0 / M20.1 Bool | 0607 RID44/46; 0278 Coil343/347 쓰기, 0279 읽기 |
| Close EV A 01 / Open EV B 01 | M21.0 / M21.1 Bool | 0607 RID22/21; 자동 S/R와 permit 탈락 Reset |
| Close EV B 01 / Open EV A 01 | M21.2 / M21.3 Bool | 0607 RID23/20; 자동 S/R와 permit 탈락 Reset |
| R1 Gate ON | M10.5 Bool | 0607 RID12; 0276 Coil115 쓰기, 자동순서 읽기 |
| maintenance PV01 | M80.5 Bool | 0607 RID47 AO645; 0279 병렬 읽기. 이번 자료에서 독립 작성 경로 미확보 |
| Flag.Enable_R1_GATE | DB2.DBX5.0 Bool | 0609 RID6 AO40 +0608 Flag TOD2; HMI 주소 및 공통 자동 S/R 경쟁 |
| Flag.R1_GATE_LOOP_ON | DB2.DBX4.7 Bool | 0609 RID13 AO39; 0276 Coil117 쓰기, BC01 읽기 |
| A_MEM_CLOSE / A_MEM_OPEN | DB2.DBX8.0 / 8.1 Bool | 0609 RID128/10 AO64/65, startup·위치 기억 S/R |
| B_MEM_CLOSE / B_MEM_OPEN | DB2.DBX8.2 / 8.3 Bool | 0609 RID134/11 AO66/67, startup·위치 기억 S/R |
| WorkData.R1State | DB6.DBW20 Int | 0609 RID18 AO160, 0608 WorkData TOD6; 0276/0277 Move 쓰기 |
| Data.PV-01a / PV_01B | DB1.DBW300 / 302 Int | 0609 RID119/115 AO2400/2416; KF_KT의 KF 입력 |
| SET_EVR1A_Open_time / B | DB1.DBW16 / 44 Word | 0609 RID40/31 AO128/352; KF_KT 출력, 순서 타이머 value 읽기 |

기존 CSV의 mem gate a open pv-01 M10.7, mem gate b open pv-01 M10.6 및 00/02 닫기 태그를 위 Flag DB 기억과 동일한 변수로 합치지 않는다. 이번 0276~0287 원본이 직접 사용하는 이름·주소를 기준으로 연결하고, 나머지는 기존 미해석 태그로 보존한다. [E04,E25]

### 2.4 HMI 명령과 표시 경계

PV01-hmi-map.csv 및 sources/hmi_plc_tags.csv에 다음 설정 주소가 있다. 8개 PV01 항목과 2개 공통 항목을 분리한다. [E17,E18]

| HMI 이름 | 설정 주소 | 초안 표기 |
| --- | --- | --- |
| PV_01\Flag | DB2.DBX5.0 | 백업 Enable_R1_GATE와 주소 일치. 버튼 이벤트·순간/유지 동작·쓰기 권한은 미확정 |
| PV_01\Allarme1 | DB11.DBX76.0 | 통합 알람 표시 후보. 개별 알람 이름이 아님 |
| PV_01\GateA_Open / GateA_Close | DB11.DBX76.1 / 76.2 | A 위치 표시 후보 |
| PV_01\GateB_Open / GateB_Close | DB11.DBX76.3 / 76.4 | B 위치 표시 후보 |
| PV_01\Selector_GateA / Selector_GateB | DB11.DBX76.5 / 76.6 | 현장 요청 상태 표시 후보. HMI 직접 Q 명령으로 해석 금지 |
| AbilitaMaintenance | DB2.DBX7.5 | 공통 Maintenance_ON 참조. M80.5 maintenance PV01과 자동 동일시 금지 |
| ResetAlarms | DB2.DBX13.4 | 공통 HMI Reset 요청, 실제 alarm manager 전달부 별도 |

0391 LAD1215는 HMI PV_2Gate CRef32/CodeBlock31 호출이고 20개 ORef가 있다. **network-map의 resolved_operands는 비어 있다. 추가 선언 대조로 Allarm5~7의 FALSE 세 개는 결속했으나 나머지 17개 실인수는 미해결**이다. CRef32는0624 RID716/NID39, CodeBlock31은0623 RID715/NID39와 일치한다. 검색 색인의 이름 순서만으로 20개를 확정하지 않는다. 확보된 것은 핀과 W/ORef 연결이며 부록 B에 전부 보존한다.

공통 함수 0400 LAD347/선언0631에는 GateA/B Open/Close, Selector A/B의 입력→HMI 출력과 Allarm1~7→Total_Allarms 결합이 있다. 하지만 이것만으로 PV01 호출 인수나 DB11 멤버 바인딩을 확정할 수 없다. 색인에는 네 PV01 알람 이름이 보이지만 이름과 핀의 결속은 후보로 남긴다. Allarm5~7의 ORef54/56/58은0626 RID48/NID39의 FALSE로 직접 결속했다. 원본 호출 Export·멤버 오프셋·HMI 객체 이벤트를 확보하면 이 **좁은 결속 구간**만 재확인하면 된다. HMI Allarme1을 A_NOT_OPEN 별칭으로 합치지 않는다.

## 3 제어 구조와 제어 소유

아래 논리식은 XML 접점·코일의 정적 설명이며 실행 모델이나 행동시험이 아니다. !는 XML operand Negated, S/R은 래치 쓰기다. ON 값·호출 주기·타 쓰기는 온라인으로 검증하지 않았다.

### 3.1 자동 허용과 탈락 처리

0276 LAD1911/NID1의 원본 형태를 보존하면 다음과 같다. [E05]

P = ON AND (ON OR UNDER TESTING) AND [(Enable_R1_GATE AND !A_NOT_OPEN AND !B_NOT_OPEN) OR (!Enable_R1_GATE AND A_MEM_OPEN AND B_MEM_OPEN)]

- P→Coil115 R1 Gate ON 및 Coil117 Flag.R1_GATE_LOOP_ON.
- Contact186 ON 뒤 W187로 Contact188 ON/Contact192 UNDER TESTING 병렬, OR104.
- W164 이후 Enable194→NOT A_NOT_OPEN196→NOT B_NOT_OPEN198과 NOT Enable200→A_MEM_OPEN202→B_MEM_OPEN204가 OR109로 합쳐진다.
- OR109.out W173→115/117, operand W174/ORef150 및 W175/ORef151.
- ON→NOT R1GateON Contact206/W177→W207에서 Move125가 State=0을 쓰고 RCoil130/133/136/139가 OpenA01/OpenB01/CloseA01/CloseB01을 해제한다.

중복 ON 표현을 임의로 제거하거나 UNDER TESTING 하나로 허용된다고 바꾸지 않는다. NOT_CLOSE 두 알람은 이 허용부 직접 접점에 없다. 허용 탈락은 자동 01 요청과 상태를 초기화하지만 현장 00·maintenance PV01의 작성값까지 지우는 코일은 이 네트워크에서 확인되지 않는다.

### 3.2 현장 요청과 최종 출력

0278 LAD1914/NID3은 ON과 I9.2/I9.3을 각각 읽어 OpenA00(M20.0)/OpenB00(M20.1)을 일반 코일343/347로 쓴다. ORef348 ON,349/351 selector,350/352 대상이다. [E06]

0279 LAD1915/NID4의 최종 출력은 다음과 같다. [E07]

- Q5.2 = ON AND (OpenA00 OR OpenA01 OR maintenance PV01)
- Q5.3 = ON AND (OpenB00 OR OpenB01 OR maintenance PV01 OR OFF)

B: Contact410 ON→W411→412/414/416/418; OR372 in1~4→W400→Coil377; W402/ORef390→0607 RID49 Output AO43.
A: 같은 ON→420/422/424; OR380 in1~3→W406→Coil384; W408/ORef394→0607 RID50 Output AO42.

OFF 접점418은 비반전이다. 이름 때문에 false로 치환하지 않는다. maintenance PV01는 두 OR에 공통으로 들어간다. 최종 출력식에 Enable, R1GateON, 개별 NOT_OPEN/NOT_CLOSE가 직접 직렬로 들어있다고 쓰면 안 된다. 자동 허용부의 효과는 Open01 경유이며 다른 요청 경로와 구분한다. Close01은 이 출력 네트워크의 별도 닫힘 솔레노이드 출력이 아니다. Q=0은 전기 명령 해제이지 기계 닫힘 확인이 아니다.

### 3.3 PV01 자동 순서 0부터 5

0277 LAD1913/NID2. 공통 pre조건은 Contact555 ON→557 Enable_R1_GATE→559 R1GateON, W560이다. 상태는 0609 RID18 WorkData.R1State이다. 아래는 해당 분기의 정적 전이 조건이다. **한 스캔에 몇 단계 진행되는지, 실제 공정 시간, 현장 순서는 검증하지 않았다.** [E08]

| State | 요청 쓰기 | 다음 상태 조건과 원본 핀 |
| --- | --- | --- |
| 0 | S334 CloseA01, R337 OpenA01 | SD340 Tag163/T100 value=S5T#1S(W495/ORef445), Contact561 Tag163→W562→Move345(1→State); A_MEM_CLOSE 직렬 접점 없음 |
| 1 | S356 OpenB01, R359 CloseB01 | Contact563 B_MEM_OPEN(W507/ORef454)→W564→Move363(2→State) |
| 2 | 명령 유지 | SD374 Tag164/T56 value=SET_EVR1B_Open_time(W515/ORef459); Contact565 Tag164→W566→Move379(3→State) |
| 3 | S390 CloseB01, R393 OpenB01 | SD396 Tag165/T102 value=S5T#1S(W527/ORef468); Contact567 Tag165→W568→Move401(4→State); B_MEM_CLOSE 직렬 접점 없음 |
| 4 | S412 OpenA01, R415 CloseA01 | Contact569 A_MEM_OPEN(W539/ORef477)→W570→Move419(5→State) |
| 5 | 명령 유지 | SD430 Tag166/T57 value=SET_EVR1A_Open_time(W547/ORef482); Contact571 Tag166→W572→Move435(0→State) |

타이머 선언0607 RID25/32/35/41의 SAD Timer AO100/56/102/57을 확인했다. “각 게이트가 닫혔는지 확인하고 다음 게이트를 연다”는 일반적인 설명으로 대체하지 않는다. 1초 전이는 해당 원본이 그렇게 작성되어 있다는 의미이지 안전상 적정함이나 현재 보호 설정의 승인 의미가 아니다.

### 3.4 체류 시간 변환

0285 LAD1912/NID10, 0060 KF_KT RID121과 0061 인터페이스 RID122. [E09]

- CRef35: W37/ORef38 Data.PV_01B→KF, W39/ORef40 literal 0→SEC, W41/KT→ORef42 SET_EVR1B_Open_time.
- CRef35.eno→W45→CRef44.en.
- CRef44: W46/ORef47 Data.PV-01a→KF, W48/ORef49 literal 0→SEC, W50/KT→ORef51 SET_EVR1A_Open_time.

두 입력은 Int, 출력은 Word 선언이다. KF_KT 본체의 변환 규칙·범위·SEC=0의 단위 선택과 현재 DB값은 확보하지 못했다. 호출 이름이나 다른 설비의 설정값을 근거로 A/B 체류를 몇 초라고 채우지 않는다. 위의 고정 1초, A/B 알람 4/7초와 이 가변 체류 시간을 구분한다.

### 3.5 위치 기억과 초기화

A 0286 LAD1921/NID11: [E10]

- S A_MEM_OPEN = ON AND Q_A AND (EV01_Open OR Inputs.FC GATE A OPEN).
- R A_MEM_OPEN = ON AND !Q_A.
- S A_MEM_CLOSE = ON AND !Q_A AND (EV01_Close OR Inputs.LS02 closed).
- R A_MEM_CLOSE = ON AND Q_A.
- 근거: 21 ON,22 Q,23/24 raw/DB→OR25→S26(W58,대상W59/ORef40); NOT27→R28(W61/62). NOT29→30/31→OR32→S33(W69/70);34Q→R35(W72/73).

B 0287 LAD1922/NID12: [E11]

- S B_MEM_OPEN = ON AND Q_B AND [EV02_Open OR (false AND EV02_Close) OR Inputs.PV01 GATE B OPEN].
- R B_MEM_OPEN = ON AND !Q_B.
- S B_MEM_CLOSE = ON AND !Q_B AND (EV02_Close OR Inputs.LS06 closed).
- R B_MEM_CLOSE = ON AND Q_B.
- 근거: 21ON,22Q,23rawopen/24false→25rawclose/26DBopen→OR27→S28(W66/67). NOT29→R30(W90/70), NOT31→32rawclose/33DBclose→OR34→S35(W77/78);36Q→R37(W95/81).
- 0610 RID130/NID12 UID41이 **literal false**다. OFF(M0.1)와 다르다. false 분기는 백업에서 불성립하지만 원시 open·DBopen 경로까지 없다는 뜻은 아니다.

0150 LAD405 startup/NID5는 ON Contact326→W327→S307 A_MEM_CLOSE, S309 B_MEM_CLOSE를 갖는다. W322/ORef316, W323/ORef317의 선언과 일치한다. **시작시 닫힘 기억을 설정하는 코드는 물리적으로 닫혔다는 증거가 아니다.** 알람 해석에 초기화·래치 상태·실제 센서·출력 명령을 구분한다. [E16]

### 3.6 공통 자동과 상충

PV01 전용 루프가 Enable을 단독 소유하지 않는다. HMI DB2X5.0 외에 다음 공통 쓰기가 있다. [E19]

| 원본 | Enable_R1_GATE 쓰기 | 조건·경계 |
| --- | --- | --- |
| 0164 LAD1843 NID3 예열 | S506, ORef29/W28; 뒤 S34가 MemoCMD_PV1_Startup 설정 | ON AND !Emergency_module_fault AND Tipo_preset=1 AND Auto_ON1 AND Tempo_presetting=26; Eq503 in2 W732/ORef633 literal26 |
| 같은 0164 | R837 Enable, R838 MemoCMD_PV1_Startup | 같은 예열 종류 전제 아래 Enable Contact833 AND MemoCMD Contact834→W849→TON835.IN; PT W850/ORef841 T#1M; Q W851→R837→W854→R838. 이 분기에는 Auto_ON1 접점823을 통과하지 않는 W33 가지가 있음 |
| 0165 LAD1844 NID4 생산 | S1158, W1161/ORef1159 | ON AND !Emergency_module_fault AND Auto_ON1 AND Tipo_preset=2 AND Tempo_presetting=40; Eq834→W1087 |
| 0166 LAD1847 NID5 정지 | R941, W1064/ORef1009 | Auto_ON1 AND Tipo_preset=5 AND (Tempo_presetting=15 OR Emergency_module_fault); OR42→W1062 |

선언0577 RID51가 같은 Enable 쓰기, 0575 RID110가 MemoCMD_PV1_Startup(M180.6)이다. TON 인스턴스는0580 RID117 T_Reset_Startup_PV1이며 A/B 이동감시 타이머가 아니다. 해당 조건을 “26초/40초/15초”라고 단위 확정하지 않고 비교값으로 보존한다.

0242 LAD1935에서 BC01의 Start BC01은 ON, Flag.M_BC_01 및 (R1_GATE_LOOP_ON OR MemoCMD_BC01_Startup OR Maintenance_ON) 경로를 사용한다. Contact242/W36/ORef37→OR43 in1, Contact41→in2, Contact26→in3, W45→Coil202. 이 관계는 “PV01 허용만으로 BC01 전체가 항상 정지/운전”이라는 뜻이 아니다. BC01 전체 재조사는 하지 않았다.

상충·미확정: HMI/공통 자동 S/R, startup/위치 기억 S/R, 물리/DB 입력 병렬, 최종 출력 local/auto/maintenance/OFF가 함께 존재한다. 스캔 순서·블록 호출 여부·다른 쓰기와 현재값이 없으므로 최종 우선권과 현재 상태는 미확정이다. M80.5의 작성자도 미확보다.

## 4 전기 전달 경로와 회로 끝점

### 4.1 실제 페이지와 개정

파일은 all-in-one/sources/Electrical_Rev2.pdf. PDF 페이지는 1부터 세며 FG와 구분한다. 해당 페이지 전체 및 제목·개정란을 직접 확인했다. [E20~E23]

| FG | PDF 페이지 | 해당 페이지 개정란 | 사용 근거 |
| --- | --- | --- | --- |
| 69 | 70 | 공란, 기본 DATE 27.05.2024 | EV01/02와 69KA1/2 출력 회로 |
| 70 | 71 | 공란, 기본 DATE 27.05.2024 | LS01/02/05/06 및 PB15 현장 조작 |
| 124 | 125 | Rev2, 17.03.2025 | MOD10 E8.6/E8.7, LS02 SPARE |
| 125 | 126 | 공란, 기본 DATE 27.05.2024 | MOD10 E9.0~E9.3 |
| 141 | 142 | Rev2, 17.03.2025 | MOD15 A5.2/A5.3 |

### 4.2 A 출력 경로

FG141 MOD15 단자13 A5.2(Q5.2)→FG69/3→69KA1 코일 A1, A2→-0Vdc 10.6. 이것은 PLC 릴레이 구동측이다.

별도 부하측: 110Vac 9.7→69KA1 접점1/9→선69.1→X1/126(5×20,2A F 도면표기)→선69.2→EV01 A1; EV01 A2→X1/127→0Vac 9.9. PLC DC 출력과 EV AC 전원을 혼동하지 않는다. 접점 실제 폐로·퓨즈 실물·코일 정격·현행 배선은 확인하지 않았다. [E20,E23]

### 4.3 B 출력 경로

FG141 MOD15 단자14 A5.3(Q5.3)→FG69/6→69KA2 A1/A2→-0Vdc 10.6.

110Vac 9.7→69KA2 접점1/9→선69.3→X1/128(5×20,2A F)→선69.4→EV02 A1; A2→X1/129→0Vac 9.9. 출력 해제 시 밸브·실린더의 복귀 방향, 잔압·스프링·스풀 구조는 이 회로만으로 확정하지 않는다. [E20,E23]

### 4.4 위치 및 현장 선택 경로

FG70의 위치 입력 네 줄은 +24Vdc 10.7→각 퓨즈 단자→LS 접점13/14→복귀 단자→PLC 입력이다. A/B별 X1 번호와 모듈 단자는 §2.1 참조. 도면 접점 심벌의 작동 전/후 물리 위치와 정상값 0/1은 현장 근거 없이 채우지 않는다. [E21,E22]

현장 요청은 +24Vdc→X1/138(2A F)→70SB1 GREEN PB15 접점13/14→선70.6→70SA1 WHITE PB15의 Gate A/B 선택 접점→X1/139 E9.2 또는X1/140 E9.3이다. 단순히 독립된 두 HMI OPEN 버튼이라고 쓰지 않는다. 동시 선택 가능 여부·selector 실제 구조는 현행 부품 근거가 필요하다.

LS02는 FG70에 A CLOSED 회로가 그려져 있고 FG124 E8.7에는 SPARE 점선 표기가 있다. 원본은 EV01_Close I8.7과 DB13X8.7을 사용한다. 세 근거를 모두 남기고 하나를 삭제하여 맞추지 않는다.

### 4.5 시공도면 보완과 기계 경계

Electrical_Can_Decoating_20241118.pdf 실제 PDF21/53 확인. 표제 24.11.11 first draft design을 현행 승인·준공으로 승격하지 않는다. 공개 GME 저장소에 포함된 원본만 사용했으며 별도 세진 프로그램 자료를 복제하지 않았다. [E24]

PDF53 케이블 일정의 PV01 선택 행:

| 행 | 케이블 식별자 | FROM→TO | 원문 규격·경로 |
| --- | --- | --- | --- |
| 3_8 | =ENT+PV01-ENT2TB2A | CC01 ENT2TB1→PV01 ENT2TB2, LS01/02/03/04 | DC CVV 12G 1.0 SPARE3; RBD1/E210 |
| 3_9 | =ENT+PV01-ENT2TB2B | ENT2TB1→ENT2TB2, EV01 | AC CVV 3G 1.0 SPARE0; RBD1/E310 |
| 3_10 | =ENT+PV01-ENT2TB3A | ENT2TB1→ENT2TB3, LS05/06/07/08 | DC CVV 12G 1.0 SPARE3; RBD1/E220 |
| 3_11 | =ENT+PV01-ENT2TB3B | ENT2TB1→ENT2TB3, EV02 | AC CVV 3G 1.0 SPARE0; RBD1/E320 |
| 3_20 / 3_21 | =ENT+PV01-LS01A / -LS02A | ENT2TB2→LS01 / LS02 | DC CVV 2C 1.0; E211/E212 |
| 3_24 | =ENT+PV01-EV01A | ENT2TB2→EV01 | AC CVV 3G 1.0; E213 |
| 3_25 / 3_26 | =ENT+PV01-LS05A / -LS06A | ENT2TB3→LS05 / LS06 | DC CVV 2C 1.0; E221/E222 |
| 3_29 | =ENT+PV01-EV02A | ENT2TB3→EV02 | AC CVV 3G 1.0; E323 |

PDF21은 ENT2TB1→ENT2TB2→LS01/LS02/EV01의 배관·배선 경로를 그린다. PDF53의 LS03/04/07/08 추가 표기를 백업의 여덟 개 PLC 위치 입력으로 만들지 않는다. ENT2TB3행 FROM 설명에도 PV-01 A GATE가 반복되어 있어 이름만으로 B 게이트의 실물 위치를 확정하지 않는다. OEM X1번호와 시공 ENT2TB 번호 사이 개별 심선·단자 대응표는 미확보다.

P&ID PID_1684n002I.pdf PDF1 PV-01 Detail에서 compressed air→EV01→CL01/CL02와 EV02→CL03/CL04, LS01/LS02 및 LS05/LS06를 시각 확인했다. 기계도 GATE A/B 문자는 형상에 부착되지만 각 전기 EV와 형상 사이의 일대일 결속·상하 방향을 문자 위치만으로 확정하지 않는다. 클램프·링크·실린더와 게이트의 실제 동일성 자료가 필요하다.

## 5 알람과 복구 경계

### 5.1 네 고유 알람과 별칭

알람 DB명은 원문의 Allarm 철자를 보존한다. 다음 네 PLC 알람이 직접 확인된 PV01 위치감시다. 이것을 “PV01 알람 전체는 반드시 네 개”라는 전역 완결 선언으로 사용하지 않는다. 공통 비상·공정 정지·HMI 통합표시는 별도다. [E12~E15,E17]

| 원문 알람 | 설명용 한국어 별칭 | 백업 주소 | 감시 타이머·설정 | 래치 S/R |
| --- | --- | --- | --- | --- |
| Allarm.PV_01_GATE_A_NOT_OPEN | A 열림 미확인 | DB3.DBX10.1 | Tag80 T103 / S5T#4S | 0449 S1459 / R1464 |
| Allarm.PV_01_GATE_A_NOT_CLOSE | A 닫힘 미확인 | DB3.DBX10.2 | Tag81 T104 / S5T#4S | 0449 S1477 / R1482 |
| Allarm.PV_01_GATE_B_NOT_OPEN | B 열림 미확인 | DB3.DBX10.3 | Tag82 T105 / S5T#7S | 0450 S1523 / R1528 |
| Allarm.PV_01_GATE_B_NOT_CLOSE | B 닫힘 미확인 | DB3.DBX10.4 | Tag83 T106 / S5T#7S | 0450 S1541 / R1546 |

주소 근거: 0657 RID177/179/181/183 AO81/82/83/84, Allarm DB3 선언과 결속. 0658 Timer RID176/178/180/182 SAD Timer AO103/104/105/106. 한국어는 문서 설명 별칭이며 HMI 원문 메시지 ID·문구가 확인되었다는 뜻이 아니다. PV_01\Allarme1은 별도의 통합 표시 후보다.

### 5.2 원본 타이머 입력과 래치

A 열림: ON Contact1528→Q_A1530→NOT A_MEM_OPEN1551→W21→SD1453. value W1504/ORef1485는0656 RID322 S5T#4S; timer operand W1505/ORef1486는0658 RID176. 별도 Q_A 뒤 timer Contact1532→W22→S1459, 대상 W1509/ORef1489(0657RID177).

A 닫힘: ON→NOT Q_A1540→NOT A_MEM_CLOSE1555→W23→SD1471. value W1516/ORef1494 같은4초, operand W1517/ORef1495 Tag81. NOT Q_A 뒤 Contact1542 Tag81→W24→S1477, 대상W1521/ORef1498(RID179).

B 열림: ON1592→Q_B1594→NOT B_MEM_OPEN1615→W21→SD1517. value W1568/ORef1549는0656RID320 S5T#7S; operandW1569/ORef1550 Tag82. timer Contact1596→W22→S1523, 대상W1573/ORef1553(RID181).

B 닫힘: ON→NOT Q_B1604→NOT B_MEM_CLOSE1619→W23→SD1535. valueW1580/ORef1558 같은7초, operandW1581/ORef1559 Tag83. timer Contact1606→W24→S1541, 대상W1585/ORef1562(RID183).

따라서 타이머의 NOT MEM 조건과 S코일의 timer접점을 나눠 설명한다. NOT Q의 닫힘 감시는 “운전 중에만”으로 좁힐 수 없다. MEM 래치는 순간 센서 값과 다를 수 있고 startup S도 영향을 준다.

### 5.3 Reset의 의미

각 알람 R코일은 ON AND Flag.RESET_ALLARM AND 해당 알람 조건이다. A열림 W1511 RESET/ORef1490→Contact1536→자기알람1538→W1539→R1464; A닫힘1546/1548→W1549→R1482. B열림1600/1602→W1603→R1528; B닫힘1610/1612→W1613→R1546. “센서가 정상으로 돌아오면 자동 해제”라고 쓰지 않는다.

공통 0158 LAD930/NID9는 Inputs.Reset_allarmi Contact23와 Flag.Reset_Allarms_HMI Contact26를 OR28로 묶는다. W38→S33 Flag.RESET_ALLARM(W36/ORef37), 동시에 R40가 HMI Reset요청을 해제한다(W42/ORef43). 공통 Reset 변수의 다른 초기화·쓰기는 별도이므로 영구 유지나 정확한 펄스 폭을 이 부분만으로 확정하지 않는다. 동일 페이지의3초 TOF는 다른 출력 Reset 경로이며 **PV01 감시 지연 4/7초나 복구 대기시간으로 복사하지 않는다**. [E16]

알람 래치 해제는 실물 복구 완료가 아니다. 원인이 남아 있으면 후속 호출에서 다시 감시·설정될 수 있다. Reset 클릭·강제 출력·센서 우회·지연값 증대를 처방하지 않는다.

## 6 증상별 수리 문서 초안

아래는 수리 실행 순서가 아니라 **승인된 현장 점검에 필요한 관찰 항목과 원본 대조표**다. 전기·공압 격리, 잔압과 낙하·끼임 위험 통제, 자격자의 현장 절차가 확보되지 않은 상태에서 게이트를 조작하거나 접근하지 않는다. 현재 보호·복귀 설정을 바꾸지 않는다.

| 증상 | 문서에서 나누어 확인할 항목 | 관련 근거 | 아직 필요한 자료 |
| --- | --- | --- | --- |
| A/B가 열리지 않음 | HMI명령/Enable, local00, auto01, M80.5, ON/OFF, Q, KA코일, 접점, EV전원, 공압/실린더, 위치센서를 분리 | E02~E11,E20~E23 | 같은 시각의 요청·Q·센서·MEM·알람 기록, 현행 단자·정격·공압 계통 |
| A 4초 또는 B 7초 열림알람 | Q=1 상태와 MEM_OPEN 경로, raw/DB 입력차이, 실제 게이트위치 | E03,E10~E15 | 센서 정상극성, 래치/초기화, 실제 이동시간과 고장원인 |
| 출력이 꺼져 있는데 닫힘알람 | NOT Q 닫힘감시, MEM_CLOSE, LS02 SPARE 상충, 기계 복귀 여부 | E10~E16,E22 | 실린더·스풀·잔압/스프링, LS02/LS06 실제 설치·결선 |
| 자동순서 멈춤 | State1/4의 MEM_OPEN 대기와 State2/5 가변시간을 구분 | E08,E09 | 현재 State·KF입력·변환Word·타이머 상태, KF_KT 본체/범위 |
| 닫힘 확인 전 다음 단계로 보임 | State0/3은 1초 전이이며 닫힘기억 접점이 없음 | E08 | 현장 설계 의도, 기계 간섭·위험평가, 승인된 변경 검토. 이 초안에서 로직 변경 안 함 |
| Enable 해제해도 출력이 남음 | local00/maintenance/OFF 병렬 및 공통 자동 S/R | E05~E07,E19 | M80.5 작성자, HMI 이벤트, 모든 현재 쓰기와 스캔 순서 |
| 센서는 바뀌는데 HMI/MEM이 다름 | rawI·InputsDB·MEM·HMI DB11 각각 별도 비교 | E03,E10,E11,E17,E18 | CRef32 실인수 결속, 현재 호출조건·DB쓰기·HMI통신 |
| Reset 후 재발 | alarm R과 원인 제거·MEM회복·물리복구를 구분 | E12~E16 | 원인·조치·회복 증거, 자격자 확인 및 승인된 재가동 절차 |

관찰 기록 양식에는 관찰자·시간/시간대·설비 실물ID·CPU/프로젝트 근거·자료 판본·신호값/단위·수집장치·원본과의 차이·최초 불일치 구간·배제한 원인·조치·복구 증거를 둔다. 여기에는 실제 관찰값을 작성하지 않았다. 사용자의 운영 기록/사진을 공개 저장소에 복사하지 않는다.

## 7 완료 기준과 통합 인계

### 7.1 7영역 적용표

| 표준 영역 | 적용 상태 | 이 문서 | 미확보 경계 |
| --- | --- | --- | --- |
| 설비·자료 기준 | 적용 | §1,E01,E24,E25 | 실물 동일성/기계 A/B·현행 자료 |
| I/O·HMI | 적용, 부분 미확보 | §2,E02~E04,E17,E18 | HMI 실인수·이벤트·현재값 |
| 제어 구조 | 적용 | §3,E05~E11,E19 | KF_KT 본체·모든 작성자·현행 스캔 |
| 전기 전달 경로 | 적용, 부분 미확보 | §4,E20~E24 | OEM↔시공 개별심선·현재 결선·극성 |
| 알람·복구 | 적용 | §5,E12~E16 | 현재 설정/복구·HMI 메시지 ID |
| 증상별 수리 | 적용, 관찰 계획 | §6 | 실제 원인·조치·복구 미실행 |
| 완료 기준 | 적용 | §7,부록 | 통합/UI/기록/PDF/게시 담당자 검증 대기 |

### 7.2 네 기능에 넘길 자료

| 기능 | 이 초안에서 제공 | 통합 담당 검증 |
| --- | --- | --- |
| 도면·래더 비교 | PV01 고유 I/O·핀·조건·5개 OEM 페이지·시공/P&ID끝점 | P05 링크·선택 회로·검색 결과와 원본 대조 |
| 백업·선택 복원 | 기록 필드에 필요한 구분 및 원본 보존 요구 | PV01키·이전/미지 필드·타설비 격리·재열기 검증 |
| 기록 전후 비교 | 실제 관찰 없이 비교할 변수·소유·미확정 항목 | 저장/동시성/실패·선택복원 및 사용자 편집 보존 |
| 보고서/PDF | 7영역·근거표·회로·미확정 경계 | A4의 가독성·페이지넘김·링크/기록누락 실제 확인 |

위 기능이 PV01에 구현되었다고 주장하지 않는다. 다른 설비의 항목 수·회로 수·통과 수를 PV01에 복사하지 않는다.

### 7.3 Codex의 좁은 재확인 목록

1. E07 최종 두 출력의 OR와 **B OFF 비반전**·maintenance공통을 원본핀으로 재확인한다.
2. E08 State0/3의 고정1초, State1/4의 MEM_OPEN, E09 가변시간미확정을 보존한다.
3. E10/E11 raw/DB병렬·false literal·startup 닫힘기억과 E12~E15 A4초/B7초를 재확인한다.
4. E03 IW8→DB13W8 및 main ENO/NOT Simulation 호출 경계는 현재 CPU와 구분한다.
5. E19 Enable 공통 S/R·예열1분 TON·BC01연동을 과도한 안전인터록 주장 없이 반영한다.
6. E17의 20핀 중 미결속17개는 색인순서로 확정하지 않는다. FALSE 세 개와 구분한다. 필요하면 CRef32 실인수 Export와 HMI 이벤트만 추가 확보한다.
7. E20~E24의 각 FG개정란·LS02 SPARE·110VAC/DC분리·ENT2TB3설명 상충을 유지한다.
8. 기존 PV01 원초안·미확정·기록 필드를 보존하면서 코드통합/UI/기록/PDF/게시를 담당한다. Dots 조사를 처음부터 다시 할 필요는 없다.

### 7.4 누락 근거와 보류

- **U01** 현행 CPU/프로젝트/다운로드 동일성: 현재 백업·온라인 대조·변경이력 필요. 원본 해시만으로 현장 확정 불가.
- **U02** LS02 실물/극성 및 SPARE: 현행 승인 도면, 센서·표찰·결선 증거 필요. 기존 명칭만으로 삭제 안 함.
- **U03** HMI0391 20개 중 미결속17개 실인수와 DB11멤버: 해당 네트워크 Export·접근 선언·객체 이벤트 필요.
- **U04** KF_KT 본체/단위/범위·가변 시간 현재값: 함수원본·DB 스냅샷·설정이력 필요.
- **U05** M80.5,ON/OFF/UNDER TESTING,DB처리 입력과Enable의 전체 작성자·실행 순서: 현재 전체 교차참조와 호출흐름 필요.
- **U06** EV01/02 밸브형식·정전/공압상실 복귀·실린더/기계 A/B 동일성: 제조사 도면·명판·현장식별 필요.
- **U07** OEM X1↔ENT2TB2/3 개별심선·LS03/04/07/08 관계: 준공 단자표·케이블 양단 표찰 필요.
- **U08** 실제 원인/복구/보호값 적합성: 자격자 승인 점검과 관찰·조치·복구 증거 필요. 초안으로 대체 불가.

| 완료 구분 | 이 초안 상태 |
| --- | --- |
| documentation | 1차 초안 작성, 기존자료 보존 |
| static_review | 지정 XML·선언·핀·도면 정적 대조 수행; 미결속/미확보 명시 |
| ui_records | 미실행, 사용자/Codex 담당 |
| publication | PV01 초안 미게시, 사용자/Codex 담당 |
| tia_compile | not_performed |
| live_cpu | not_performed |
| field_recovery | not_performed |

다음 승인 순서는 PV02(P07)이나, **이번 조사·산출물은 PV01 한 개로 종료**한다. 2차133후보는 제외한다. 공통 코드·대장·버전·운영기록 편집 및 신규 코딩 작업 생성은 하지 않는다.

## 부록 A 핵심 주장 근거표

고정 원본 경로의 축약은 §1.3을 따른다. 모든 XML·PDF의 SHA-256 및 고정 커밋 링크는 부록 C에 있다. 각 행의 해석은 백업 범위이고 미확정 열을 함께 표시해야 한다.

| ID | 핵심 주장 | 원본 경로와 정확한 위치 | 해석과 미확정 경계 |
| --- | --- | --- | --- |
| E01 | PV01=P05 태그 대응, 실물 확인 아님 | docs/equipment-standard/INVENTORY.json priority P05/catalog PV01; sources/PID_1684n002I.pdf PDF1 PV-01 Detail | mapping=tag, identity_verified=false; EV01/02와 CL01~04 관계는 자료상 근거, 실물 A/B 미확정 |
| E02 | 원시 입력6개 | 0607 RID124/126/129/131/43/45, SAD Input AO70~75; 0286 NID11 ORef38/44,0287 NID12 ORef40/42/48,0278 NID3 ORef349/351 | I8.6~I9.3. LS03/04/07/08을 추가 PLC입력으로 만들지 않음 |
| E03 | IW8→Inputs DB13W8와 호출 경계 | 0397/LAD1070 Move43, W53/55/56/57, ORef47/48; 0627RID15 Input Word AO64,0629RID16 Word AO64 BAD4,0628RID4 TOD13;0030/LAD1613 NID19 CRef21/23/25/28,37NOT,W32/33/42/44/43,0688/0692/0694 선언 | static 전달 경로. 현재 M180.0/ENO·CPU·타쓰기 미확정 |
| E04 | 내부/출력 주소와 상수 구분 | 0607 RID1/4/12/20~23/44/46~50,0608 DB TOD,0609 RID6/10/11/13/18/31/40/115/119/128/134 | ON/OFF는Memory, false만Literal; DB/SAD/AO 대조, 현재값 미확정 |
| E05 | permit와 자동 요청 초기화 | 0276/LAD1911 NID1 Part186/188/192 OR104,194/196/198,200/202/204 OR109,Coil115/117,W164/173/174/175;206NOT→W207 Move125/R130/133/136/139 | 두 NOT_OPEN 직접조건, NOT_CLOSE를 덧붙이지 않음; 현장/maintenance 요청 차단 확정 아님 |
| E06 | 현장 셀렉터→00 요청 | 0278/LAD1914 NID3 Coil343/347;ORef348~352→0607RID1/43/44/45/46 | ON과 I9.2/I9.3 경로. 현재 버튼 상태·스위치 구조 미확정 |
| E07 | 최종 Q A/B의 병렬 소유 | 0279/LAD1915 NID4 ON410,W411,OR372→W400→Coil377/W402 ORef390 RID49;OR380→W406→Coil384/W408 ORef394 RID50;maintenanceORef388/393,OFF389 | B OFF 비반전, local/auto/maintenance 별도. Q0≠실물닫힘 |
| E08 | State0~5의 고유 전이·타이머4개 | 0277/LAD1913 NID2 Eq328/350/368/384/406/424;SD340/374/396/430,Move345/363/379/401/419/435;W495/515/527/547,0607TimerRID25/32/35/41,0610상수 | State0/3 1초,State1/4 MEM_OPEN,State2/5가변. 닫힘센서 확인 후 전이라고 단정하지 않음; 실제순서 미확정 |
| E09 | KF_KT 두 가변 체류 변환 | 0285/LAD1912 NID10 CRef35/44,0060RID121,0061RID122;W37/39/41/45/46/48/50;0609RID115/119/31/40,0610literal0 | KF/SEC/KT핀 결속. 함수몸체·단위·현재값 미확보 |
| E10 | A 위치기억 | 0286/LAD1921 NID11 Part21~35,W49~73;0607RID50/124/126,0609RID125/127/10/128 | raw OR DB 처리 입력, Q방향별S/R; 순간센서와래치 다름 |
| E11 | B 위치기억과 false 분기 | 0287/LAD1922 NID12 Part21~37,W53~81/88~97;ORef41→0610RID130 false;0607RID49/129/131,0609RID132/133/11/134 | false AND EV02Close만 불성립. B rawopen/DBopen 경로 보존 |
| E12 | A NOT_OPEN 4초 | 0449/LAD1815 NID42 SD1453,S1459,R1464;W1504/1505/1509/1514,0656RID322,0658RID176,0657RID177 | 타이머 ON·Q·!MEM_OPEN,래치 ON·Q·Tag80. 현재설정/극성 아님 |
| E13 | A NOT_CLOSE 4초 | 0449 NID42 SD1471,S1477,R1482;W1516/1517/1521/1526,0656RID322,0658RID178,0657RID179 | ON·!Q·!MEM_CLOSE 감시. 출력0에서도 감시 경로 |
| E14 | B NOT_OPEN 7초 | 0450/LAD1816 NID43 SD1517,S1523,R1528;W1568/1569/1573/1578,0656RID320,0658RID180,0657RID181 | A와 시간 다름. 위치메모리 감시이며 원시센서 직접 단정 금지 |
| E15 | B NOT_CLOSE 7초 | 0450 NID43 SD1535,S1541,R1546;W1580/1581/1585/1590,0656RID320,0658RID182,0657RID183 | RESET과자기알람의R,물리복구와 분리 |
| E16 | startup CLOSE기억 및 공통Reset | 0150/LAD405 NID5 Contact326→W327→S307/309,W322/323 ORef316/317→0563RID51/52;0158/LAD930 NID9 OR28→W38→S33/R40,W36/42 ORef37/43→0565 | 초기닫힘기억은실물확인아님. Reset요청경로만확인,모든작성자/복구미확정 |
| E17 | HMI 호출 20핀 중17미결속 | 0391/LAD1215 CRef32 RID716/CodeBlock31 RID715→0624/0623 NID39;W33~71,0626RID48 FALSE3개;0400/LAD347 NID1 0631 LocalAccess | 함수내 신호전달과호출실인수별도. HMI통합알람은단일고장별칭아님 |
| E18 | HMI 설정/과거화면 | sources/hmi_plc_tags.csv,PV01-detail/PV01-hmi-map.csv,assets/HMI_DECOATER.png | DB2X5.0/DB11X76.x 설정과과거도형. 현재화면·CPU·버튼이벤트미확정 |
| E19 | 공통Enable 소유와BC01연동 | 0164/LAD1843 S506/S34,R837/R838,TON835 PTW850;0165/LAD1844 S1158;0166/LAD1847 R941;0577RID51,0575RID110,0580RID117;0242/LAD1935 Contact242→OR43→Coil202 | 예열26/생산40/정지15비교·예열1분리셋. 같은Enable의복수쓰기;현재우선권미확정 |
| E20 | EV01/02 AC부하 및DC릴레이 | sources/Electrical_Rev2.pdf FG69/PDF70,69KA1/2 A1/A2·접점1/9,X1/126~129,EV01/02 A1/A2 | 110Vac/0Vac와PLC출력코일회로분리. 개정란공란. 실제밸브/보호값미확인 |
| E21 | LS/PB15 신호 끝점 | 같은PDF FG70/PDF71,X1/130~140,LS01/02/05/06 13/14,70SB1/70SA1 | 위치4+현장요청2. 개정란공란,정상극성미확정 |
| E22 | MOD10 주소와LS02 SPARE | 같은PDF FG124/PDF125 단자7/8 E8.6/E8.7,FG125/PDF126 단자11~14 E9.0~E9.3 | FG124Rev2,FG125공란. SPARE와원본활용을둘다보존 |
| E23 | MOD15 출력 두끝점 | 같은PDF FG141/PDF142 단자13/14 A5.2/A5.3→FG69/3,/6 | Rev2 17.03.2025. Q출력과접점/EV/기계응답은다른단계 |
| E24 | 시공·공압의 범위 | sources/Electrical_Can_Decoating_20241118.pdf PDF21/53 행3_8~11,3_20/21/24~29;PID_1684n002I.pdf PDF1 PV01Detail | 24.11.11firstdraft,ENT2TB/LS추가와OEM연결미확정;P&ID기계A/B이름만으로소유확정금지 |
| E25 | 기존자료/원초안·미확정 보존 | PV01-detail/PV01-manual.md,PV01-io-map.csv,PV01-internal-tags.csv,PV01-verification.csv,sources/pv01-evidence.json | 이번정적확인으로현장미확인을덮지않음. 과거중지시험자료를실행하지않음 |

## 부록 B HMI 호출의 실인수 핀 장부

0391-FlgNet.xml의 CRef32 기준이다. 아래에서 “미결속”은 원본 ORef RID와 블록 내 실인수 선언 연결이 확보되지 않았다는 뜻이다. 검색 색인 문장 순서를 바인딩으로 대신하지 않았다. Call 자체의 NID39는0623/0624 선언으로 확인했다.

| 핀 | 방향 | Wire | ORef UID | RefId | 결속 상태 |
| --- | --- | --- | --- | --- | --- |
| GateA_Open | 입력 | 33 | 34 | 717 | 미결속, 실인수 Export 필요 |
| GateA_Close | 입력 | 35 | 36 | 718 | 미결속, 실인수 Export 필요 |
| GateB_Open | 입력 | 37 | 38 | 719 | 미결속, 실인수 Export 필요 |
| GateB_Close | 입력 | 39 | 40 | 720 | 미결속, 실인수 Export 필요 |
| Selector_GateA | 입력 | 41 | 42 | 721 | 미결속, 실인수 Export 필요 |
| Selector_GateB | 입력 | 43 | 44 | 722 | 미결속, 실인수 Export 필요 |
| Allarm1 | 입력 | 45 | 46 | 723 | 미결속, 실인수 Export 필요 |
| Allarm2 | 입력 | 47 | 48 | 724 | 미결속, 실인수 Export 필요 |
| Allarm3 | 입력 | 49 | 50 | 725 | 미결속, 실인수 Export 필요 |
| Allarm4 | 입력 | 51 | 52 | 726 | 미결속, 실인수 Export 필요 |
| Allarm5 | 입력 | 53 | 54 | 48 | 0626 RID48 NID39 Literal FALSE |
| Allarm6 | 입력 | 55 | 56 | 48 | 0626 RID48 NID39 Literal FALSE |
| Allarm7 | 입력 | 57 | 58 | 48 | 0626 RID48 NID39 Literal FALSE |
| HMI_GateA_Open | 출력 | 59 | 60 | 728 | 미결속, 실인수 Export 필요 |
| HMI_GateA_Close | 출력 | 61 | 62 | 727 | 미결속, 실인수 Export 필요 |
| HMI_GateB_Open | 출력 | 63 | 64 | 729 | 미결속, 실인수 Export 필요 |
| HMI_GateB_Close | 출력 | 65 | 66 | 730 | 미결속, 실인수 Export 필요 |
| HMI_Selector_GateA | 출력 | 67 | 68 | 731 | 미결속, 실인수 Export 필요 |
| HMI_Selector_GateB | 출력 | 69 | 70 | 732 | 미결속, 실인수 Export 필요 |
| Total_Allarms | 출력 | 71 | 72 | 733 | 미결속, 실인수 Export 필요 |

공통 0400은 A열림 Contact22→Coil23(W49), A닫힘24→25(W52), B열림69→70(W79), B닫힘71→72(W82), SelectorA26→27(W55),SelectorB84→85(W90), 알람 OR33(in1~7)→W67→Coil34(Total_Allarms,W68/ORef46)다. 원본0631 LocalAccess 이름과 결속한다. 이것은 공통 함수의 역할 근거이며 PV01의17개 미결속을 대신 해결하지 않는다.

## 부록 C 원본 경로와 SHA256

원본은 아래 고정 커밋의 파일이다. 링크는 공개 GitHub이며 all-in-one/을 원본으로 유지했다. 해시는 내려받은 파일 바이트의 SHA-256이다. 생성된 초안 자체 해시나 현재 현장 프로젝트 해시가 아니다. 동일 자료를 다른 설비의 완료 숫자로 계산하지 않는다.

이 표의 파일은 **61개**다.

| 원본 경로 | SHA-256 |
| --- | --- |
| [.agents/skills/gme-equipment-rollout/SKILL.md](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/.agents/skills/gme-equipment-rollout/SKILL.md) | fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b |
| [docs/equipment-standard/WORK-STANDARD.md](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/docs/equipment-standard/WORK-STANDARD.md) | 05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99 |
| [docs/equipment-standard/WORK-ITEM-TEMPLATE.md](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/docs/equipment-standard/WORK-ITEM-TEMPLATE.md) | 4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586 |
| [docs/equipment-standard/INVENTORY.json](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/docs/equipment-standard/INVENTORY.json) | 720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc |
| [all-in-one/sources/decoded-original/0030-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/all-in-one/sources/decoded-original/0030-FlgNet.xml) | 9252c9da764993de1edb8b2e44c46d6e9f9d4b6118e751a0dbeaa9ffd8ea721b |
| [all-in-one/sources/decoded-original/0150-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/all-in-one/sources/decoded-original/0150-FlgNet.xml) | 829ca4aa3bd2bb6ee406f7f204add2987ec6159ef0fd6dd3dfc075592664a98e |
| [all-in-one/sources/decoded-original/0158-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/all-in-one/sources/decoded-original/0158-FlgNet.xml) | d3f3adebc3d990b85c5d4c294906ae3bc3dafebb49d25b030bf9cc2ccf905651 |
| [all-in-one/sources/decoded-original/0164-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/all-in-one/sources/decoded-original/0164-FlgNet.xml) | 15884b2b362842279b626b669a484b1daa269f5ecd99112b8391bb0387382491 |
| [all-in-one/sources/decoded-original/0165-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/all-in-one/sources/decoded-original/0165-FlgNet.xml) | 4513a5f6e77717c99c5e869105483be31f7f62ab280e271dc36cd7a2d3e3bb88 |
| [all-in-one/sources/decoded-original/0166-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/all-in-one/sources/decoded-original/0166-FlgNet.xml) | 0330a505877be92172f94bce83222a0bfc8d64aab700a69fc1fa2188010d3853 |
| [all-in-one/sources/decoded-original/0242-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/all-in-one/sources/decoded-original/0242-FlgNet.xml) | aca0cbc07c04fae72012760899cba246fe65c78ae234cef59e6439dc1172b715 |
| [all-in-one/sources/decoded-original/0276-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/all-in-one/sources/decoded-original/0276-FlgNet.xml) | 408314ae1159ee5e24a124bbb00847dd29de8c3caf572d3f8afcf8dfa20a9fd2 |
| [all-in-one/sources/decoded-original/0277-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/all-in-one/sources/decoded-original/0277-FlgNet.xml) | df78505599829ed4b7c718c8eee4b362492c598da6fa0505c0170c1a90179d56 |
| [all-in-one/sources/decoded-original/0278-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/all-in-one/sources/decoded-original/0278-FlgNet.xml) | ef79acf030d84e4b67e257f43967a31bc362a7a7f3cbb7d120224eb3c475bac9 |
| [all-in-one/sources/decoded-original/0279-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/all-in-one/sources/decoded-original/0279-FlgNet.xml) | 4ae9c9ae70987b778a159c896b88fa4e34cf6f597903a0c68e630708b5f1bfd1 |
| [all-in-one/sources/decoded-original/0285-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/all-in-one/sources/decoded-original/0285-FlgNet.xml) | b12d8c7e630489ebc4f68a5f06988019b9556f1f1dcad15983ceb02e7e49ee79 |
| [all-in-one/sources/decoded-original/0286-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/all-in-one/sources/decoded-original/0286-FlgNet.xml) | dca38f0104a47f95095b88a86400e379d653dd26b0e2fc88e1b3d17612268828 |
| [all-in-one/sources/decoded-original/0287-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/all-in-one/sources/decoded-original/0287-FlgNet.xml) | 885e0619ad4a49a2a873b4f0f069eafc62b350f4a12f060e4def9c020f3fe616 |
| [all-in-one/sources/decoded-original/0391-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/all-in-one/sources/decoded-original/0391-FlgNet.xml) | 0129ecbb6949e9e609da2a5ef789a2200bcf677f0d87d677b1dd52c1fcb45700 |
| [all-in-one/sources/decoded-original/0397-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/all-in-one/sources/decoded-original/0397-FlgNet.xml) | bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834 |
| [all-in-one/sources/decoded-original/0400-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/all-in-one/sources/decoded-original/0400-FlgNet.xml) | e2aa1de29bf6f95b0b2a79c3e8510a086e6d6c6990f3954cfc09f06211340d94 |
| [all-in-one/sources/decoded-original/0449-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/all-in-one/sources/decoded-original/0449-FlgNet.xml) | bec235318e26bfcb3346e70c0d47ade995bd411c3d5719be1d61ce7ba9c73791 |
| [all-in-one/sources/decoded-original/0450-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/all-in-one/sources/decoded-original/0450-FlgNet.xml) | ee257645cb8e8e590c75677163871bc7a40646fc4635692fd0abb26dec4c6afa |
| [all-in-one/sources/decoded-original/0060-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/all-in-one/sources/decoded-original/0060-IdentXmlPart.xml) | d61344a049baa2ce8a97335cd94e6c1753f8f8b7180d3def74d8631ff2cf21b9 |
| [all-in-one/sources/decoded-original/0061-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/all-in-one/sources/decoded-original/0061-IdentXmlPart.xml) | 0861f9e3686b911262b7b7e108c51fc9fed9cb7080c72bcc4b3aae60750af1c7 |
| [all-in-one/sources/decoded-original/0563-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/all-in-one/sources/decoded-original/0563-IdentXmlPart.xml) | 86cf35b6baebc079cb5a092baf53ec3364c377ea7318eb263ab69c8b4550b4ad |
| [all-in-one/sources/decoded-original/0565-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/all-in-one/sources/decoded-original/0565-IdentXmlPart.xml) | 0f7f970faa6c456f2bb032b1a2072a2f52db1e03fc77bd8d35d4583deeaf1149 |
| [all-in-one/sources/decoded-original/0567-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/all-in-one/sources/decoded-original/0567-IdentXmlPart.xml) | 5d428b5d5a2b0f4649dbbbb4e4f060a9d89a107e9cf4b6139d8f003c4371347e |
| [all-in-one/sources/decoded-original/0575-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/all-in-one/sources/decoded-original/0575-IdentXmlPart.xml) | 40e7b2caf89ab7f1ed9075547a7728bd02441e24451bdd8bf97c843637daad06 |
| [all-in-one/sources/decoded-original/0577-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/all-in-one/sources/decoded-original/0577-IdentXmlPart.xml) | 511e01fae619dc385357908a1ac62030dbdfd5f5399bd4c22bc58bebbfc3bf47 |
| [all-in-one/sources/decoded-original/0578-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/all-in-one/sources/decoded-original/0578-IdentXmlPart.xml) | 0f9f41b5dee25ea17c7a29ab6f7b00503c13d0f265266acd660072baf061d32b |
| [all-in-one/sources/decoded-original/0580-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/all-in-one/sources/decoded-original/0580-IdentXmlPart.xml) | fa748a6c1890f579d694fd5e561b2304f717da79e5352ca32152cc20e877c6ff |
| [all-in-one/sources/decoded-original/0607-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/all-in-one/sources/decoded-original/0607-IdentXmlPart.xml) | 9b76b53536a26e7b45961fecbf825ae1552e16c2fd9af5736864193c01d77f93 |
| [all-in-one/sources/decoded-original/0608-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/all-in-one/sources/decoded-original/0608-IdentXmlPart.xml) | 24adec2035b65c0c310d637bcea74374896875b6465a16aa2f2cfc8fd55fa4b8 |
| [all-in-one/sources/decoded-original/0609-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/all-in-one/sources/decoded-original/0609-IdentXmlPart.xml) | 395de8ebb2168848cf96fe015bd7334d71107c114a4e441ef36346b8f22031db |
| [all-in-one/sources/decoded-original/0610-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/all-in-one/sources/decoded-original/0610-IdentXmlPart.xml) | c58d07b1b9707dc8c6c2f06c34ee6142f72238a4cf3f376bee8502d1a9532f9d |
| [all-in-one/sources/decoded-original/0623-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/all-in-one/sources/decoded-original/0623-IdentXmlPart.xml) | 4acd00406ea92466169e57e59fc90b0da4d9ec55fd19e2e96c9556e939cb83a6 |
| [all-in-one/sources/decoded-original/0624-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/all-in-one/sources/decoded-original/0624-IdentXmlPart.xml) | 24607c0827fbde428bccf8637ef4ae490798a69a7c2f3b87861d0749082d367a |
| [all-in-one/sources/decoded-original/0626-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/all-in-one/sources/decoded-original/0626-IdentXmlPart.xml) | a9d7fbea345eca70325a8c2e44058c23e96add1b7207eabbb09445118b18188b |
| [all-in-one/sources/decoded-original/0627-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/all-in-one/sources/decoded-original/0627-IdentXmlPart.xml) | 08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb |
| [all-in-one/sources/decoded-original/0628-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/all-in-one/sources/decoded-original/0628-IdentXmlPart.xml) | 9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd |
| [all-in-one/sources/decoded-original/0629-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/all-in-one/sources/decoded-original/0629-IdentXmlPart.xml) | 67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972 |
| [all-in-one/sources/decoded-original/0631-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/all-in-one/sources/decoded-original/0631-IdentXmlPart.xml) | 8e5072374f8ef098de72fbf93965b2a7bb0965c0f803e397daa68588c0c38555 |
| [all-in-one/sources/decoded-original/0656-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/all-in-one/sources/decoded-original/0656-IdentXmlPart.xml) | 0dbc45e84732a8848f17b094ea08ab8578dbf240bfe15cd7086859395c27c592 |
| [all-in-one/sources/decoded-original/0657-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/all-in-one/sources/decoded-original/0657-IdentXmlPart.xml) | 0f70cda60a6b1a17175876d58e25b2686952642de6cffb21213aeef8b347a22b |
| [all-in-one/sources/decoded-original/0658-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/all-in-one/sources/decoded-original/0658-IdentXmlPart.xml) | 998294c0c8a99e00ceb33c2c60def2cd4850e34328917ae506244c2be2df3831 |
| [all-in-one/sources/decoded-original/0688-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/all-in-one/sources/decoded-original/0688-IdentXmlPart.xml) | ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda |
| [all-in-one/sources/decoded-original/0692-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/all-in-one/sources/decoded-original/0692-IdentXmlPart.xml) | bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037 |
| [all-in-one/sources/decoded-original/0694-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/all-in-one/sources/decoded-original/0694-IdentXmlPart.xml) | 757ccebdf32d0a168dd787bfa735fe6494eac4c4a9f7a5adc63898a88e8b152d |
| [all-in-one/sources/decoded-original/network-map.json](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/all-in-one/sources/decoded-original/network-map.json) | c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60 |
| [all-in-one/sources/Electrical_Rev2.pdf](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/all-in-one/sources/Electrical_Rev2.pdf) | 5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6 |
| [all-in-one/sources/Electrical_Can_Decoating_20241118.pdf](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/all-in-one/sources/Electrical_Can_Decoating_20241118.pdf) | 3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd |
| [all-in-one/sources/PID_1684n002I.pdf](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/all-in-one/sources/PID_1684n002I.pdf) | 2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b |
| [all-in-one/sources/hmi_plc_tags.csv](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/all-in-one/sources/hmi_plc_tags.csv) | a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404 |
| [all-in-one/PV01-detail/PV01-manual.md](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/all-in-one/PV01-detail/PV01-manual.md) | 744ac30e18e288d75755bec9edb608893343d696e354e8623fedd81644ebbed7 |
| [all-in-one/PV01-detail/PV01-io-map.csv](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/all-in-one/PV01-detail/PV01-io-map.csv) | 8fc56817ab3106310597e135d67432b1159c33d36d8c3f3a45f8816fedea6319 |
| [all-in-one/PV01-detail/PV01-hmi-map.csv](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/all-in-one/PV01-detail/PV01-hmi-map.csv) | 741dc6046067c027d1aec9c7fc44faa2876bb81d458e6c56acfc66004d83efd1 |
| [all-in-one/PV01-detail/PV01-internal-tags.csv](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/all-in-one/PV01-detail/PV01-internal-tags.csv) | a82127ae6e123df250ab3976f3d8dce0d11907ba97541af52549e63cd7151fc3 |
| [all-in-one/PV01-detail/PV01-verification.csv](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/all-in-one/PV01-detail/PV01-verification.csv) | af2f0c050fead885100ac86a70a05a4e5091ab00b3b3da1ca3d3e33ece8f6b34 |
| [all-in-one/PV01-detail/sources/pv01-evidence.json](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/all-in-one/PV01-detail/sources/pv01-evidence.json) | 5a344c04c01144e441c75635eb30cb381051109e89e03428b845b9661edf2640 |
| [all-in-one/PV01-detail/assets/HMI_DECOATER.png](https://github.com/esp6662266/gme-plc-manual/blob/f0abee0d2182d7c89394d7aa0ccfd91ea92d7e5f/all-in-one/PV01-detail/assets/HMI_DECOATER.png) | b84b888a2df87d23b514aeb790d2fc51f31c3b20486061a365380b28986f49af |

## 부록 D 자체 점검 범위

- 지정 XML은 텍스트/구조로 읽고 선언 RID·NID·UID·SAD/SSD/TOD와 Wire의 pin을 대조했다. 논리 실행·시뮬레이터 생성·행동시험은 하지 않았다.
- OEM FG69/70/124/125/141, 시공PDF21/53, P&ID PV01 Detail 및 저장 HMI 이미지를 실제 렌더로 확인했다.
- 이 초안의 7영역·25개 핵심 근거 행·HMI20개 핀의 누락 여부, 고정 원본 파일·해시를 확인한다. 원본 호출·미확정 경계는 위 표 그대로 유지한다.
- 공개 원본 worktree의 Git 수정 없음. 기존 PV01 자료 및 사용자 원초안·다른 설비 초안은 수정하지 않았다.
- 미실행: TIA compile, PLC/현장, 시뮬레이터·행동시험, UI/저장·복원/동시성/PDF출력/패키지/배포 검사. 뒤 항목은 사용자/Codex 통합 단계에서 담당한다.
