# SS09 이송 장치 감시 스위치 · Dots 원본 조사 초안

- 대상은 SS09 한 개, 유형 sensor, 부모 MC03, 별칭 mc03_torque다. SS01/SS10/SS11과 이름이 같아도 독립 catalog ID이며 부모 완료를 상속하지 않는다.
- 기준: GME-STD-1.0.0, BATCH16 승인 범위, source-mv06 Git abcf31c5030bc7ef8749ed8e869a857f2387a28a / v1.12.0. 최신 게시본·현재 CPU·현장 설치와 구별한다.
- 작업 시작: 2026-10-11 12:38:00 UTC. 모델 런타임/제품 선택 증명은 미확인. 조사자는 원본 읽기·자체 XML 파싱·PDF 렌더만 수행했다. 생성기/build/test/시뮬레이터/TIA/PLC/현장/보호값/SEJIN 실행·변경과 재위임은 하지 않았다.
- 문서 상태: draft_ready_with_gaps. 로컬 통합·게시·현장 완료가 아니다. 수정 범위는 이 MD와 extracts/SS09뿐이다.
- 약어: D/ = all-in-one/sources/decoded-original/, S/ = all-in-one/sources/, R/ = all-in-one/registers/. P/W/O/R은 각각 Part UID/Wire UID/ORef UID/RefId 또는 선언 RID다. ID와 NID는 해당 파일·블록 문맥 안에서만 결속한다.

## 핵심 확인·상충·누락

1. D/0556의 Global SimpleAccess MC03_torque, Bool, Input AO52는 %I6.4다. D/0397의 IW6→DB13.DBW6 Word 복사로 D/0657의 Inputs.MC03 torque DB13.X6.4와 연결된다. 원시 입력/복사된 비트/알람은 별도다.
2. D/0427 LAD1790 NID11은 OFF AND NOT torque에서 DB3.X3.4를 Set, OFF AND RESET_ALLARM AND torque AND 기존 TORQUE에서 Reset한다. SS09 토크 망에는 타이머가 없다. 인접 MC03 FAULT의 T53/S5T#2S를 SS09에 복제하지 않는다.
3. Electrical_Rev2 실제 PDF24/FG23: +24Vdc10.7 → X1:52 5×20 2A F → 23.2 → SS-09 11–12 → X1:53 → E6.4. 실제 PDF123/FG122: E6.4 → CPU515/MOD9 pin25, LIMIT SWITCH SS-09. 접점 번호와 소프트웨어 반전은 현장 정상극성·토크 설정의 증명이 아니다.
4. FG23 제목과 M05는 SPARE, FG122에는 SS09 채널만 SPARE 점선 밖이다. 서로 다른 표기를 보존하며 설치 여부를 결정하지 않는다. FG23 기본 날짜 27.05.2024/별도 개정란 공란, FG122 REV2 17.03.2025를 각각 읽었다.
5. MC03 토크 알람은 NOT UNDER TESTING 조건의 부모 요청 Reset에 쓰인다. 이 설정을 우회·복구 방법으로 제시하지 않는다. startup DB3.DBW2의 0쓰기도 같은 알람 비트에 겹친다.
6. SS09/MC03/spare 명명 HMI 대응행은 제공 CSV 두 파일에서 확보하지 못했다. 0360 spare motor 호출의 핀은 확인했으나 실제 피연산자의 NID/DB주소 결속은 미확정이다.
7. 남은 자료: 설치·기계 감지 방식·현행 센서 모델/정상극성·설정값·유효 케이블 양끝·HMI 이벤트·현재 프로젝트/CPU·원인 제거와 복구 증거. 회전/속도 센서라고 이름만으로 확정하지 않는다.

공유 근거: MC03-DOTS-DRAFT.md는 경로 탐색 색인으로 사용했다. MC03 모터 동력/출력·시간누적·시공 케이블표 전체를 SS09 소유로 복제하지 않았다. 고유 입력 선언, Word 복사, 토크 S/R, 부모 영향 분기, startup 겹침, HMI 호출 제한, PDF24/123은 원본을 독립 재대조했다. 공통 함수 HMI Standard Motors 내부 Local 논리와 MC03 전체 동력/시간 경로는 부모 초안 참조이며 이번 의미검토 수에 넣지 않는다.

## 1. 설비·자료 기준

### 1.1 식별과 범위

INVENTORY.json catalog index110은 SS09 / sensor / 계측 / parent_id MC03 / depth1 / phase2 / planned / baseline / not_assessed다. R/equipment.json index105는 fgs:[23], aliases:[mc03_torque], parent:MC03를 보관한다. scope 및 중복검토는 parent_child_separate, physical_identity_verified:false다. 이 문서 조사로 대장의 실물 확인 상태나 부모/하위 완료 수를 변경하지 않는다.

R/equipment.json의 pid:true는 색인 메타데이터다. 부모 조사에서 P&ID의 명시 MC03/SS09 대응 미확보를 기록했다. 이번에는 SS09 전기·PLC 끝점에 범위를 한정해 P&ID 새 식별 근거를 확보하지 않았으며 pid:true만으로 P&ID 위치를 발명하지 않는다.

PLC 심볼 CSV 519행(헤더 포함)은 mc03_torque,%i6.4,bool,limit switch ss-09, 문서936으로 기록한다. 이는 탐색/교차확인용이고 실제 신호 주소는 아래 원본 SimpleAccess에서 직접 확인했다. 도면 SS-09와 대장 SS09는 문서 대응이며 실물 동일성은 별도다. MC03 부모의 M05를 MC05나 SS11로 치환하지 않는다.

### 1.2 자료 시점

원본 HEAD와 clean 상태를 확인했다. VERSION/HANDOFF/PUBLICATION/ACTIVE-WORK/EXPANSION 최신 상단은 고정 v1.12.0 상태다. 사용자의 이후 게시 상태와 고정 조사 입력을 혼합하지 않는다. 0556 선언 MT 2025-01-31은 백업 메타데이터이며 실물 설치일·교정일이 아니다. 실제 PDF 페이지별 footer 확인 범위는 §4에 기록한다.

## 2. I/O·HMI

### 2.1 선언·형식·주소

| 소유/신호 | 주소·형식 | 원본 선언과 사용 UID | 해석·제한 |
|---|---|---|---|
| SS09 후보 원시 입력 MC03_torque | %I6.4 Bool | D/0556 SimpleAccess RID240, S=Global, SAD Input, SSD AO52; NID−2147483648 UID120 AK Monitor | 물리 입력 영역. Monitor 선언만으로 실행 reader 전체가 확인되는 것은 아님 |
| 입력 전송 Tag_171 | %IW6 Word | D/0627 RID13, SAD Input AO48; D/0397 NID1 O45 | PIW/Peripherie 직접접근으로 바꾸지 않음 |
| 입력 DB Word | DB13.DBW6 Word | D/0629 RID14 AO48/BIRID4; D/0628 DepDBBlock RID4 TOD N13, CID638561979615757134 | 두 byte6..7의 복사 목적지 |
| Inputs.MC03 torque | DB13.DBX6.4 Bool | D/0657 GlobalAccess RID273 AO52/BIRID247; D/0655 RID247 TOD DB13, 위와 동일 CID; NID11 O408/O411 | 처리된 입력. 원시 I6.4와 같은 주소 문자열로 합치지 않음 |
| Allarm.MC_03_TORQUE | DB3.DBX3.4 Bool | D/0657 RID52 AO28/BIRID10; D/0655 RID10 TOD DB3 CID638560457249431121; NID11 O409 Set/O412 Read/O413 Reset | 알람 래치. 물리 센서나 현재 토크값 아님 |
| Flag.RESET_ALLARM | DB2.DBX6.0 Bool | D/0657 RID13 AO48/BIRID12; D/0655 RID12 TOD DB2; NID11 O410 | 공통 Reset 요청. 버튼 이벤트와 별도 |
| OFF | %M0.1 Bool | D/0658 SimpleAccess RID46 Memory AO1; NID11 O407 | 명칭만으로 항상 FALSE라 단정 금지 |
| ON | %M0.0 Bool | D/0602 RID1, D/0692 RID52 Memory AO0 | 상위/부모 허가. OFF와 상호배타 상수라고 가정하지 않음 |
| UNDER TESTING | %M5.5 Bool | D/0602 RID4 Memory AO45; NID10 O324 | 부모 요청 Reset 분기 조건. 변경/강제 금지 |
| 부모 Flag.M_MC_03 | DB2.DBX0.3 Bool | D/0604 RID60 AO3/BIRID2; D/0603 RID2 TOD DB2 | SS09 자체 출력이 아니라 MC03 운전 요청 |
| 부모 Start Spare Motor | %Q0.3 Bool | D/0602 RID61 Output AO3; NID10 O327 Write | 부모 기동 출력. SS09는 센서 입력으로 분류 |

GlobalAccess의 AO는 bit offset이며 Bool/Word 자료형과 BIRID→DepDBBlock을 함께 읽었다. RID 숫자만 같은 다른 블록을 결속하지 않는다. Local 입출력은 HMI 공통 함수의 형식 인자이므로 위 Global 신호와 자동 병합하지 않는다. SS09 채널은 Bool 접점 경로로 확인했으며, 전용 아날로그 환산·속도 스케일·토크 공학단위·PID 소유 근거는 미확보다. 도면의 TORQUE CONTROL이라는 설명은 토크값 측정/설정 수치를 제공하지 않는다.

### 2.2 Word 전송과 실행 경계

D/0397 LAD1070 NID1에서 rail W21→P42 Move.en, O45/R13→W52→P42.in, P42.out1→W54→O46/R14다. P42 DisableENO=true가 있고 P42.eno는 W53으로 다음 Move43.en에 이어진다. 해당 P42 경로에 NOT나 환산은 없다. 입력 IW6의 I6.4가 DB13.DBW6의 X6.4에 포함됨을 형식과 bit offset으로 대조했다. 이 경로가 유일한 writer라는 증명은 아니다.

D/0030 LAD1613 NID19는 rail W31→CRef21.en, CRef21.eno W32→CRef23.en, CRef23.eno W33→CRef25.en, CRef25.eno W42→P37 반전 Contact.in, P37.out W43→CRef28.en이다. P37 operand W44/O45는 D/0692 RID140 Simulation(1), Memory AO1440(%M180.0). CRef28 RID136/CodeBlock29 RID135는 D/0688 HMI Inputs FC15와 D/0694 NID19 UID28/29로 결속된다. 따라서 실제 입력 복사는 상위 ENO 연쇄와 NOT Simulation(1) 경계를 갖는다. 이 원문 허가를 기록했을 뿐 중지 대상의 실행·시험·개발은 하지 않았다. 현재 DB13가 언제 갱신되는지는 미확정이다.

### 2.3 HMI의 확보 범위와 누락

직접 CSV 검색: S/hmi_plc_tags.csv 782 데이터행, R/equipment-hmi.csv 230 데이터행을 SS[-_ ]?09|MC.?03|spare로 검색해 0행. 파일 전체를 검색한 결과이며 전체 화면/태그/쓰기 부재의 증명은 아니다. 원 HMI 프로젝트·dde.cfg·화면 이벤트·알람 문구 내보내기가 필요하다.

D/0360 LAD1181 spare motor 호출에는 CRef23 RID638/CodeBlock22 RID1이 있고 D/0623의 HMI Standard Motors FC1, D/0624의 인터페이스 RID638이 존재한다. 호출 NID별 같은 UID가 반복되어 실제 피연산자 결속은 미확정으로 보존한다.

| 호출 핀 | 원본 Wire/ORef/RID | 확인 수준 |
|---|---|---|
| en | W21 Powerrail→CRef23.en | 핀 직접 확인 |
| Ingresso_run | W24/O25/R711 | 실제 Global 피연산자 결속 미완료 |
| Allarme1 | W28/O29/R59 | 다른 파일 RID59 MC03_TORQUE를 바로 붙이지 않음 |
| Allarme2 | W30/O31/R60 | 부모 색인상 토크 후보, 주소·NID 확정 아님 |
| Allarme3/4/5 | W32/O33, W34/O35, W36/O37, 모두 R48 | 상수/실제 인자 미결속 유지 |
| Risposta | W42/CRef23→O43/R57 | 목적지 DB 미결속 |
| Comulativo_allarmi | W46/CRef23→O47/R55 | 목적지 DB 미결속 |

부모 초안에 공통 함수 0355/0621 Local 입출력과 OR 처리가 있다. 이번에 그 전부를 재검토하지 않았고 SS09 전용 표시 주소·버튼·색상·ACK/RESET 이벤트로 승격하지 않는다.

## 3. 제어 구조·영향·다른 쓰기

### 3.1 부모 요청에 미치는 영향

D/0246 LAD1940 NID10을 직접 읽었다. P343 Contact ON(O319/W328/D0602 R1)의 out W344가 토크 분기 P351.in으로 이어진다. P351 operand O323/W333/D0604 R59는 Allarm.MC_03_TORQUE이며 AO28/BIRID5→D0603 Allarm DB3다. P351.out W352→반전 P353.in, P353 operand O324/W334/D0602 R4 UNDER TESTING, P353.out W354→OR306.in3, OR306.out W336→P314 RCoil.in, P314 operand O325/W338/D0604 R60 Flag.M_MC_03다.

즉 확인한 토크 영향은 ON AND TORQUE AND NOT UNDER TESTING일 때 부모 요청 DB2.X0.3 Reset이다. 같은 OR의 in1은 MC03_FAULT, in2는 NOT Inputs.MC04 run AND NOT Flag.STANDBY_ON이다. MC04 입력과 STANDBY 분기를 SS09 자체 입력으로 가져오지 않는다.

부모 출력 경로는 W344→P355 Contact 요청(O326/W339)→W356→P318 Coil(O327/W341)로 Q0.3을 쓴다. 토크 접점이 Q0.3 코일 앞에 직접 직렬로 있는 것이 아니라 요청 Reset을 거치는 구조다. SS09 래치 Reset은 운전요청 Set 또는 재기동 완료가 아니다. MC03 요청 Set 원천은 부모 조사에서도 미결속이며 이번 SS09 조사로 새 Set 절차를 만들지 않는다.

### 3.2 startup Word 쓰기와 Bit 쓰기의 중첩

D/0148 LAD403은 network-map NID 누락이 있어 선언의 CS NID3 UID287/288로 해당 경로를 결속한다. P250의 eno W306→P253.en, 상수 INT#0 O287/R54(D0048)→W307→P253.in, P253.out1→W308→O288/R26(D0563)이다. R26 Word AO16/BIRID23, D0562 R23 Allarm TOD DB3이므로 DB3.DBW2(byte2..3)에 0쓰기가 존재한다. 이는 TORQUE DB3.X3.4와 겹친다.

P250 앞단은 ON P329, operand W303/O284(D0047 R1), out W330이다. P253은 앞선 Move ENO를 거치므로 무조건 0쓰기라고 요약하지 않는다. startup이라는 블록명만으로 실제 시작 OB·Warm/Cold·Retain·현행 최종값을 확정하지 않는다. S/R 비트 쓰기만이 유일한 알람 writer라는 주장도 하지 않는다. 부모 요청 DB2.X0.3의 별도 Word 초기화는 MC03 초안 §3.4 공유 근거로 연결하며 SS09 독립 출력으로 세지 않는다.

### 3.3 상위 알람 호출

D/0031 LAD1619 NID6의 P282 ON Contact operand W280/O271(D0692 R52), rail W284→P282.in, P282.out W283→CRef264.en. CRef264 RID59/CodeBlock275 RID58은 D/0688 Allarms 1 FC4와 D/0694 NID6 UID264/275에 대응한다. 내부 SS09 토크망의 OFF 허가와 상위 ON 호출을 각각 보존한다. 이름만으로 두 값을 상수로 치환해 보호 활성/비활성이나 현재 안전 상태를 판단하지 않는다.

## 4. 전기 끝점·실제 PDF 대조

| 파일/실제 페이지 | 도면 footer·개정란 | 독립 확인 범위 |
|---|---|---|
| S/Electrical_Rev2.pdf PDF24 | FG23 / TOT262 / DATA27.05.2024 / SPARE, 별도 수정기록 공란 | SS09 공급·접점·X1 끝점·PLC 교차참조, 모터/피드백과 분리 |
| 같은 PDF123 | FG122 / TOT262 / DATA27.05.2024, REV2 17.03.2025 | E6.4, 모듈 pin25, LIMIT SWITCH SS-09와 인접 SPARE 범위 |

실제 렌더 두 페이지를 직접 보았으며 FG 번호로 페이지를 일괄 산술 변환하지 않았다. 파일명 Rev2를 FG23에 일괄 부여하지 않는다. 렌더는 extracts/SS09/electrical-p24.png 및 electrical-p123.png에 있다.

### 4.1 신호 전달의 양 끝점

PDF24/FG23 구역7: +24Vdc10.7 수평 공급선(좌22/7→우24/3)에서 X1:52 퓨즈단자 5×20 2A F → 도체23.2 → SS-09 접점11–12 → X1:53 → E6.4 화살표122/5.

PDF123/FG122 구역5: E6.4 화살표23/7 → pin25 → CPU:515 / MOD.:9 / E6.4 / LIMIT SWITCH SS-09. 원본 XML I6.4 주소와 E6.4 도면 표기가 교차 확인된다. 현행 CPU 명판·모듈 형번 또는 실제 단자 결선 확인은 아니다.

접점11–12는 도면 인쇄를 직접 읽은 번호다. 도면 심벌·입력 반전으로 실제 센서의 작동 정상극성, fail-safe 등급, 기계 작동점·토크 한계를 확정하지 않는다. 퓨즈2A F는 도면값이며 현재 퓨즈 확인 또는 교체·보호값 조정 권고가 아니다. SS09 케이블 번호·심수·규격·길이와 센서 모델·설치 위치는 이 두 페이지에서 확보되지 않았다. 23.2는 회로 도체 표기이며 완성 케이블 고유번호로 바꾸지 않는다.

### 4.2 인접 회로와 SPARE의 경계

FG23의 FEEDBACK MOTOR E0.5는 23KM1 보조접점13–14 경로이고 SS09/E6.4와 다르다. 기동 A0.3·XS7/8·23QS1/23QM1·23KM1 A1/A2는 부모 모터 제어 회로다. SS09를 모터 회전 피드백 E0.5나 기동 출력 Q0.3로 설명하지 않는다.

FG122 SPARE 점선은 E6.3/SSL-01, E6.5/SS10 및 E6.6/SS11을 감싼다. E6.4/SS09에는 이 점선이 없지만 FG23 전체 제목/M05는 SPARE다. 어느 표기 하나로 현재 설치·철거·예비 여부를 결정하지 않는다. 상위 전원10.7 생성 회로·부모 동력 전체·시공케이블표는 MC03 공유 문서 참조이고 이번 독립 렌더 수에 포함하지 않는다. 일반 릴레이 하단 접점표의 번호를 SS09 실제 접점 번호로 치환하지 않는다.

## 5. 알람·Reset·복구

### 5.1 SS09 고유 TORQUE 래치

D/0427 LAD1790 NID11 전체 지정망의 Part/Wire를 직접 확인했다.

| 단계 | 원본 경로 | 논리 의미 |
|---|---|---|
| 공통 허가 | rail W434→P424 Contact.in; operand W414/O407/D0658 R46; out W425 | OFF 값에 따른 두 가지 분기 |
| 발생 입력 | W425→P426 반전 Contact.in; operand W415/O408/D0657 R273 | NOT Inputs.MC03 torque |
| Set | P426.out W427→P400 SCoil.in; operand W417/O409/R52 | OFF AND NOT torque → TORQUE Set |
| Reset 요청 | W425→P428 Contact.in; operand W418/O410/R13; out W429→P430.in | RESET_ALLARM |
| Reset 입력 회복 조건 | P430 Contact operand W419/O411/R273; out W431→P432.in | torque 정극성 |
| 래치 확인·Reset | P432 operand W420/O412/R52; out W433→P406 RCoil.in; operand W422/O413/R52 | OFF AND RESET_ALLARM AND torque AND TORQUE → Reset |

NID11 O409/O413는 선언 AK Write이고 각각 SCoil/RCoil로 구분된다. 실시간 반복/Retain/상위 호출 중단의 실행 결과나 최종 스캔 우선순위는 시험하지 않았다. 이 망에는 타이머·속도 계산·회전 펄스 판정·명시 MC03 운전조건이 없다. 따라서 '운전 중 일정 시간 무회전이면 SS09 알람'이라는 설명은 현재 확보 원문으로 성립하지 않는다.

### 5.2 부모 FAULT와 분리

D/0426 LAD1789 NID10에는 P383 SdCoil, O398/R48 Tag_56(%T53), value W407/O397/D0656 R28 S5Time SV=S5T_x0023_2S/V512가 있다. 발생 경로는 OFF P419→StartSpare P421→반전 run P432→P383이며 이것은 부모 모터 운전 미응답용이다. S5Time 저장값512를 512초로 바꾸지 않는다. T53/S5T#2S를 인접 SS09 TORQUE 망의 필터·지연·복구대기로 복제하지 않는다.

### 5.3 복구 판정의 한계

알람 입력이 1이어도 래치 해제에는 OFF/상위호출/RESET_ALLARM/기존 TORQUE 조건과 다른 writer 영향을 봐야 한다. 알람 해제만으로 운전요청 재설정·실제 기계 정상화가 증명되지 않는다. 입력0은 원문상 Set 조건이지만 실제 원인은 센서 동작/단선/공급/퓨즈/단자/모듈/프로젝트 불일치 등 독립 자료가 필요하다. 원인·정상극성이 미확정인 상태에서 SS09 단락, 입력 강제, OFF/UNDER TESTING 변경, 보호값 조정, 임의 재기동을 복구 방법으로 제시하지 않는다.

## 6. 증상별 관찰 자료와 원인 배제

아래는 읽기 전용 비교를 위한 관찰 설계다. 현장 실행·활선측정·기계 작동 시험 또는 정비 승인 자체가 아니다.

| 증상 | 보존할 관찰 | 대조·배제 기준 | 필요한 다음 근거 |
|---|---|---|---|
| SS09 실물을 찾지 못함 | 현재 도면 개정, 반/기계 태그, 명판·위치 사진 시각 | SS09/M05/MC03 대응과 SPARE 상충, SS10/11과 분리 | 승인 준공/전용 변경서, 센서 모델·양끝 케이블 표찰 |
| I6.4와 DB13.X6.4가 다름 | 같은 시점 원시값·DB값, 프로젝트/CPU 식별, 입력복사 호출 허가 | 0397 IW6 Move, 0030 ENO/반전 허가, 다른 writer 존재 가능성 | 현행 read-only cross-reference·호출 관찰·타임스탬프 |
| 입력0인데 TORQUE가 안 생김 | ON/OFF, Allarms1 호출, DB13.X6.4, DB3.X3.4, startup 시점 | 0427 반전 Set와 0148 Word0 중첩, 현재 코드 불일치 | 동시 상태 기록·현재 프로젝트 대조. 보호가 정상이라고 단정 금지 |
| 입력1로 돌아왔는데 알람 유지 | DB13.X6.4, RESET_ALLARM, OFF, 기존 래치, HMI 동작 기록 | 0427 Reset 직렬 네 조건, 버튼이 실제 공통 요청을 쓰는지 미확정 | HMI 이벤트/태그·호출 시각, 원인 제거 증거 |
| 알람 발생 후 MC03 요청 해제 | DB3.X3.4, M5.5, ON, DB2.X0.3, Q0.3의 같은 시점 | 0246 토크 분기와 별도 FAULT/MC04/STANDBY 분기 구분 | 현재 허가/운전 순서·정식 재요청 경로 확인 |
| 화면 표시와 PLC 비트가 다름 | 화면/문구/시각, HMI 프로젝트 버전, 원시·DB·알람 값 | CSV 대응 미확보/0360 호출 결속 한계, 화면 주소를 발명하지 않음 | 원 HMI 프로젝트·알람/태그 내보내기·통신 상태 |

관찰 필드: 관찰자, 날짜·시간대, 설비ID, 위치/페이지/단자, 프로젝트 버전·CPU 식별, 값·단위·수집장치, 비교 원본, 배제 근거, 승인된 조치의 실제 내용, 원인 제거와 복구 증거. 실제 운영 데이터·미지 필드·기존 note/repair_observation/저장키는 작성하거나 변경하지 않았다.

## 7. 완료 기준·누락·검증 범위

| 영역 | 적용 판정 | 이번 결과 | 미완료 경계 |
|---|---|---|---|
| 설비·자료 | 적용 | SS09/MC03 별도 ID와 SPARE 상충 | 현재 실물/감지 종류/준공 대응 |
| I/O·HMI | 적용·일부 미확보 | I6.4→DB13.X6.4→DB3.X3.4, HMI 검색/핀 | 실제 화면·이벤트·통신 writer |
| 제어 | 적용 | S/R·입력 Word·호출·부모 영향·startup 중첩 | 현재값/최종 writer/실행 스캔 |
| 전기 끝점 | 적용·일부 미확보 | FG23 X1:52/53 11–12, FG122 pin25 | 케이블 양끝/센서 모델/공급 현황 |
| 알람·복구 | 적용 | 발생/유지/Reset 조건, 타이머 없음 | 기계 정상극성/원인 제거/실제 복구 |
| 증상 관찰 | 적용 | 여섯 증상별 자료·비교 순서 | 실제 관찰·조치 기록 |
| 완료 기준 | 적용 | 상태·선정해시·미확정 분리 | 독립검토/통합/UI/게시/TIA/현장 |

우선 필요한 자료는 ① SS09 현행 명판/설치 위치/기계 감지 방식과 승인 결선, ② 케이블/단자 양끝 및 퓨즈/입력모듈 식별, ③ 정상극성과 작동점의 제조사·승인 자료, ④ 현재 PLC 프로젝트/CPU 일치와 read-only cross-reference, ⑤ 원 HMI 태그·화면·Reset 이벤트, ⑥ 원인 제거·알람해제·승인 재요청·실제 기계 결과의 각각의 기록이다. 새 자료 없는 실물 보류 재검색은 반복하지 않는다.

네 기능은 도면/래더 비교에 사용할 독립 두 페이지와 핵심 XML을 확보했고, 백업/선택복원·기록전후비교·보고서/PDF에 필요한 관찰 필드를 정리한 단계다. 실제 UI 구현·링크·저장/재읽기/재열기·모바일·보고서 렌더 검증은 하지 않았다.

| 상태 | 결과 |
|---|---|
| documentation | draft_ready_with_gaps, SS09만 별도 초안 |
| static_review | scoped_source_review_done, 독립 2차검토 pending |
| ui_records | not_run |
| publication | not_published |
| tia_compile / live_cpu / field_recovery | 모두 not_performed |

검토 수는 바이트 해시 수와 다르다. 의미검토는 8개 FlgNet(0030/0031/0148/0246/0360/0397/0426/0427)의 위 지정 경로, 선택 선언과 CSV 검색, 실제 전기 PDF 2페이지다. 0360은 핀까지만이며 피연산자 결속은 미완료다. 전체 네트워크/전체 PLC 의미검토나 동작시험을 완료했다고 주장하지 않는다. 기본 원본 검사와 중지5자산은 바이트 보존만 확인하고 실행하지 않는다.

## 부록 A. 전체 선정 원본 SHA-256 / 고정 Git blob 내용 일치

아래 모든 경로는 source-mv06 루트 기준. SHA-256은 실제 파일, Git blob은 고정 abcf31c의 객체이며 git cat-file로 읽은 바이트와 직접 비교했다. 전체 선정 목록은 누락 없이 수록하되 해시 일치를 의미검토·현장 적합성으로 세지 않는다. 해시 JSON/정적 검사 JSON은 extracts/SS09에 있다. 중지5자산은 별도 보존 대조만 했으며 이 표의 의미검토 선정과 구별한다.

선정 원본 34파일 모두 고정 Git blob 바이트와 일치.

| 원본 경로 | SHA-256 | 고정 Git blob | 바이트 일치 / 범위 |
|---|---|---|---|
| `all-in-one/sources/decoded-original/0030-FlgNet.xml` | `9252c9da764993de1edb8b2e44c46d6e9f9d4b6118e751a0dbeaa9ffd8ea721b` | `e74c70b751acdcdbc7a8b3b0c98aa773c2107cab` | true / 지정 논리 경로; 0360 핀까지만 |
| `all-in-one/sources/decoded-original/0031-FlgNet.xml` | `76385eab8f8f72b9faa16f7cf8905f395591b18c0a9ee9e6d7dd085a38c45c65` | `653d27572de6beedcf3eb6c95702bb119a8b567f` | true / 지정 논리 경로; 0360 핀까지만 |
| `all-in-one/sources/decoded-original/0148-FlgNet.xml` | `1d80e1bbf1c82dcc4dd18628c35935bbd55a17b5be9c1ca7bfb249600d154313` | `3069ae3b5fa16ed10a64c149b6cf5cb5ace423b3` | true / 지정 논리 경로; 0360 핀까지만 |
| `all-in-one/sources/decoded-original/0246-FlgNet.xml` | `2b1bf0644447f15640214b451281aa3fa5389505936f2a6a1078a9508dfc9f04` | `c21879f1cdca1a8d47938a89ee9ea6a25c4f82bc` | true / 지정 논리 경로; 0360 핀까지만 |
| `all-in-one/sources/decoded-original/0360-FlgNet.xml` | `a2297a80a92fe385ff252f001f030a7fbde13510bdffaf156a9a6ed60733f31d` | `0985905a99514ab5b0bf77225735818775201d78` | true / 지정 논리 경로; 0360 핀까지만 |
| `all-in-one/sources/decoded-original/0397-FlgNet.xml` | `bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834` | `4ab8370493c4e28fc1eabeeebe2743d27f0c4021` | true / 지정 논리 경로; 0360 핀까지만 |
| `all-in-one/sources/decoded-original/0426-FlgNet.xml` | `8b03ce9bd6d85c9e0861abd5401f4cb61b199e06a1705fc8ecc9088ed39e5688` | `b2b036e5c9c59ab07c7045dff97a63e7d181615b` | true / 지정 논리 경로; 0360 핀까지만 |
| `all-in-one/sources/decoded-original/0427-FlgNet.xml` | `32e92066f26d542098b33dfaa7cc228f373bd3dcc331751ae0ce0ffdd8731816` | `cce340234f9ab69f06d05ec8708335e9be0aee6f` | true / 지정 논리 경로; 0360 핀까지만 |
| `all-in-one/sources/decoded-original/0047-IdentXmlPart.xml` | `2e53bb895dd1ad2a74efaeb1ef16dfd61e62b1b2d7aa34cec8612f1b9cb0928e` | `3dc282f149a21fdf76d5521ef1c833be63b578b4` | true / 지정 선언/문맥 대조 |
| `all-in-one/sources/decoded-original/0048-IdentXmlPart.xml` | `d8e8687de7271bd294c2b62b33d789700af9d5014d82b130141988c4d479253d` | `64fc5a7f1ad33f3b901b00f0d22d23578ffabff8` | true / 지정 선언/문맥 대조 |
| `all-in-one/sources/decoded-original/0556-IdentXmlPart.xml` | `065d71114e26c93af180265e0e6d59d2a190af1f2f0581c5265e7f4f67d6e23f` | `15ae569ff390ef5c791b0f76d96bd86d5ec6b938` | true / 지정 선언/문맥 대조 |
| `all-in-one/sources/decoded-original/0562-IdentXmlPart.xml` | `85aada44dd9a3e66835463c3fed400f1efe121f4f5bc5ab8f0ad49481ec0ea1c` | `1609802542a3e560baba3f2b73c306be281dfb23` | true / 지정 선언/문맥 대조 |
| `all-in-one/sources/decoded-original/0563-IdentXmlPart.xml` | `86cf35b6baebc079cb5a092baf53ec3364c377ea7318eb263ab69c8b4550b4ad` | `6a10fc694f896cda16409804daf2554c91635654` | true / 지정 선언/문맥 대조 |
| `all-in-one/sources/decoded-original/0602-IdentXmlPart.xml` | `46ab21151eddaaf616469db520730c60423eb742aa491af194e6710c751b4caf` | `bcb12ab1ce8c476ff921baa1608f29d9822f76b4` | true / 지정 선언/문맥 대조 |
| `all-in-one/sources/decoded-original/0603-IdentXmlPart.xml` | `e93969dfa281d75b49b24127793068e33472dadb19729c1c48fc4a8dad075ef8` | `3a92b304baf4dbf6147e944d9778d2da11285cb1` | true / 지정 선언/문맥 대조 |
| `all-in-one/sources/decoded-original/0604-IdentXmlPart.xml` | `b798d29c5499b5314a1ee3cff9139dae64c887533b86baa43b6e9a052373a6af` | `bb2c318788b97e7a4924a176275c12d805aa519d` | true / 지정 선언/문맥 대조 |
| `all-in-one/sources/decoded-original/0623-IdentXmlPart.xml` | `4acd00406ea92466169e57e59fc90b0da4d9ec55fd19e2e96c9556e939cb83a6` | `13b3af0459c8e6069bb9b2f1b16454bf479e08dc` | true / 지정 선언/문맥 대조 |
| `all-in-one/sources/decoded-original/0624-IdentXmlPart.xml` | `24607c0827fbde428bccf8637ef4ae490798a69a7c2f3b87861d0749082d367a` | `02511fea47fc47981c101bba49dc40adde1cdcc3` | true / 지정 선언/문맥 대조 |
| `all-in-one/sources/decoded-original/0627-IdentXmlPart.xml` | `08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb` | `61ebc0abbb2ca160e11e1da400a3f14a397d8bc5` | true / 지정 선언/문맥 대조 |
| `all-in-one/sources/decoded-original/0628-IdentXmlPart.xml` | `9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd` | `170ca5c72599edc7ea7eefe651c3680ce325e76a` | true / 지정 선언/문맥 대조 |
| `all-in-one/sources/decoded-original/0629-IdentXmlPart.xml` | `67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972` | `058129bb01e27f7a6a0d0293f332d745e5bab74e` | true / 지정 선언/문맥 대조 |
| `all-in-one/sources/decoded-original/0655-IdentXmlPart.xml` | `38e9f323024fba19582b473f39b1ed03ffe6a0b390218894029a6edb0b1ff9fb` | `83b60b9de4541a3ffa6ee0db98205a372b525665` | true / 지정 선언/문맥 대조 |
| `all-in-one/sources/decoded-original/0656-IdentXmlPart.xml` | `0dbc45e84732a8848f17b094ea08ab8578dbf240bfe15cd7086859395c27c592` | `9bfb9842e55901bab9a71d1ac03158467dfbb1bc` | true / 지정 선언/문맥 대조 |
| `all-in-one/sources/decoded-original/0657-IdentXmlPart.xml` | `0f70cda60a6b1a17175876d58e25b2686952642de6cffb21213aeef8b347a22b` | `e625f3d8999c7be7d88c50eab0d93107117b58ec` | true / 지정 선언/문맥 대조 |
| `all-in-one/sources/decoded-original/0658-IdentXmlPart.xml` | `998294c0c8a99e00ceb33c2c60def2cd4850e34328917ae506244c2be2df3831` | `de9a12a6be87466ef1bf05df71c54580c556a827` | true / 지정 선언/문맥 대조 |
| `all-in-one/sources/decoded-original/0688-IdentXmlPart.xml` | `ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda` | `463585759f1ecd94f32362b4fefb000a152f5773` | true / 지정 선언/문맥 대조 |
| `all-in-one/sources/decoded-original/0692-IdentXmlPart.xml` | `bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037` | `737785d03b5fad43c5b4d451955726d800edb1c0` | true / 지정 선언/문맥 대조 |
| `all-in-one/sources/decoded-original/0694-IdentXmlPart.xml` | `757ccebdf32d0a168dd787bfa735fe6494eac4c4a9f7a5adc63898a88e8b152d` | `c45e8f3ca4129dc06734f6a12ef79e6ed6528a7d` | true / 지정 선언/문맥 대조 |
| `all-in-one/sources/Electrical_Rev2.pdf` | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` | `f610fd7c7ce14ae951b00cff57b969259bfb389d` | true / PDF24/123 실제 렌더 |
| `docs/equipment-standard/INVENTORY.json` | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` | `587c3748ad9224718f95ba06463fee913dae231d` | true / SS09 대장 |
| `all-in-one/registers/equipment.json` | `7870325dff32bbca90fa34507b301c4aad3347d669fddcd03b910343663996fa` | `acc42633033398216469064932c4b76987371606` | true / SS09 대장 |
| `all-in-one/registers/plc-symbols.csv` | `a0334b390f06ddb515d6c09ca96a01d35d44029c1b726ef0ff53303ec04ff91f` | `cbc576c5d6e47498a3865304a1c23de9b4641d9f` | true / SS09 심볼행 |
| `all-in-one/sources/hmi_plc_tags.csv` | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` | `cf4c0650e7c7baac350dcb89909b808435704880` | true / 명명 검색 |
| `all-in-one/registers/equipment-hmi.csv` | `2cdce600aa0138cc5025022e57d9d61a948afb237f70c70e2d11e8300e73286a` | `aca60d300d26fd2bccd6d3970822c3aed2ecdb87` | true / 명명 검색 |

### 중지5자산 바이트 보존

내용 해석·실행 없이 고정 blob 및 freeze manifest와 비교했다.

| 경로 | SHA-256 | 고정 Git blob | 일치 |
|---|---|---|---|
| `all-in-one/registers/program-model.json` | `6203479c086b15bada12ac9d7e37db9280234ec26f1ea6091d7211dc09a577c5` | `9860b10f008d3a5ae714be50d77b703dfec32f3a` | blob True, freeze True |
| `all-in-one/assets/program-model-data.js` | `52f8199371e3399b7c0d44ab5469f0472aced79d56bbef2887f7625f5d2aff0f` | `38f34b0caa380a16ccad6f6f1e234a2fdf23f327` | blob True, freeze True |
| `all-in-one/assets/virtual-plc.js` | `5f1876052dc0067b1f010af0dfc941946e37003167481731293615d9c1c36dbc` | `0bd9eceb54365a91214a37c5601b5067c39a3f75` | blob True, freeze True |
| `all-in-one/assets/simulator-workspace.js` | `3a6dfc618ff7e7b238f2671dc85d65704f33093a18eac879d86081d92c31e8bc` | `97c2c831c77a9699fff0e0960b3bc1b7d93d45b3` | blob True, freeze True |
| `all-in-one/registers/virtual-plc-test-results.json` | `a6b389f797f9a8b5ffe6928b8420f55c4cc459a327b0b48d716079d2eca6dd64` | `757dd50e45184568facb8ff62900b39d3ce848d1` | blob True, freeze True |

### 실제 작업 시각과 최종 검사

- 2026-10-11T12:38:00Z: assigned
- 2026-10-11T12:38:13Z: instructions_and_parent_index_read
- 2026-10-11T12:38:46Z: pdf_render_visual_read
- 2026-10-11T12:39:54Z: raw_declaration_and_pin_comparison
- 2026-10-11T12:43:04Z: draft_body_written
- 2026-10-11T12:43:46.364795+00:00: verification

최종 검사: 선정34파일 Git blob 일치, 중지5자산 freeze/Git 일치, source-mv06 git status clean. XML 정적 Set/Reset/반전·핀 단언 통과. 실행·시뮬레이션·현장 시험 통과를 뜻하지 않는다. 원본/다른초안/대장/운영기록은 변경하지 않았다. 다음 단계는 이 고유 초안의 독립 검토와 부모 전달이며 실물/HMI 미확정은 계속 유지한다.
