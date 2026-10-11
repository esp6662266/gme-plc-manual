# RO01 산소 분석 채널 — 원본 조사 7영역 초안

## 먼저 읽을 핵심 인계

- 고유 RO01 한 개의 문서 조사다. RO02·RO03·RO04, MV05, BR01, PV05/PV06의 완료를 상속하지 않는다. 현행 산소 설정, 안전 한계, 정상 극성, 현장 복구값은 확정하지 않았다.
- 원시 신호 `R001`은 `%IW352`다. 환산 호출 0498에서는 `:P`/Peripherie 접근이며, HMI 원시 미러 0398에서는 같은 주소의 SAM=None 접근이다. `Inputs.RO_01` DB13.DBW68과 환산 `Data.Oxigen_RO01` DB1.DBW130은 다르다.
- **0498 환산 호출 EN은 OFF `%M0.1` 접점이다.** 내부 IN0에는 ON `%M0.0`을 전달한다. ON/OFF 이름을 현재 TRUE/FALSE로 단정하지 않는다. 호출이 안 되면 최신 측정값이라고 보장할 수 없다.
- 선형화는 Real 계산이 아니라 Int→DInt, `(raw+zero)*coeff/28000`의 DInt 연산과 Int OutValue 전달이다. 범위 고장값 -9999, IN0 반전 가지 0은 백업 함수의 코드값이다. 현장 안전 대체값으로 사용하면 안 된다. OFR 코일은 범위 비교 직접선이 아니라 -9999 Move의 **ENO**에서 받는다.
- RO01 신호차 알람은 RO01−RO02 차이와 온도·disable·1분 SdCoil 경로다. 단순 RO01 단선 알람이 아니다. 고산소·값범위·저산소 알람과 구분한다.
- **버너 0184의 산소 60 비교 가지 선행 상태 상수는 77이다.** 0586 RID128 CB V=77과 Eq1272.in2를 확인했다. 파생 설명의 상태7과 혼동하지 않는다. 이 가지는 BR01 소유다.
- 질소 계통 FG96의 Q6.4 공통 요청과 외부 96KA3/96KT1·PV05/PV06은 RO01의 전용 출력이 아니다. 이번 선언/네트워크 검색에서 RO01 산소 조건→Start Nitrogen Q6.4의 직접 Writer는 확인하지 못했다. 산소 고장 시 질소가 자동 주입된다고 보장하지 않는다.

### 상충·누락·공유 근거 구분

| 분류 | 내용 | 처리 |
|---|---|---|
| 상충 | OEM FG80 태그 80RO-01, 시공 p56 태그 81RO-01 | 동일성 후보를 유지하고 이름을 고치거나 병합하지 않음 |
| 상충 | OEM 설명 OXIGEN OUTLET AB-01, 시공 p56 송신기 위치 MV-03 / 프로브 HE-01 RO-1 | 도면 판본·물리 위치 차이를 그대로 남김 |
| 상충 | 기존 파생 제어 설명의 버너 상태7 vs XML 상태77 | 원본77을 본 초안에 명시; 기존 자료 미수정 |
| 누락 | 현재 ON/OFF·ServiceBit·disable·UNDER TESTING 값, 계수·제로·설정값, 현행 호출·통신·간접 Writer | 현재값·활성 여부 추정 금지 |
| 누락 | 승인 산소 단위/소수점, HMI 실제 화면 이벤트·쓰기 권한·경보 팝업, 교정·명판·프로브 부품 | INT값에 임의 % 또는 0.1% 환산을 붙이지 않음 |
| 공유 | BF01 초안의 공통 선형화 0291/0014 및 0401 출력미러 원칙 | 색인으로 참고하되 본 설비에 연결되는 원본 핀·선언을 재확인; 같은 고정 Git blob 일치 확인 |
| 독립 | 0498 입력/호출, 0530~0533 알람, 0184 산소 가지, 0475/0346 MV05 영향, FG80/110 및 시공 p56 | 본 작업에서 직접 XML·렌더 확인 |

## 1. 설비·자료 기준

- catalog_id RO01, 이름 산소 분석 채널, kind sensor, group 계측, parent 없음/depth0, priority_key 없음. INVENTORY catalog[8], equipment[86], phase2/planned. 별칭 r0-01/r001/r0_01. 같은 이름의 RO02~04는 별도 ID다.
- 범위는 `progress/TASK3-BATCH06-SCOPE.json` 및 `GME-CATALOG-OVERLAP-REVIEW.json` RO01 행. 고유 ID·현장 동일성 미확정을 유지한다. 자체 문서 조사 허용이며 로컬2차133 통합 제외는 유지한다.
- 기준 저장소 `source-mv06`, Git `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, VERSION v1.12.0. 저장소 URL https://github.com/esp6662266/gme-plc-manual . 현재 main/현재 CPU/현장 최신 도면을 의미하지 않는다.
- AGENTS, EXPANSION-WORK, VERSION/WORKSPACE-HANDOFF/PUBLICATION_STATUS/ACTIVE-WORK 최신 항목, 스킬/source-map, WORK-STANDARD/WORK-ITEM-TEMPLATE/INVENTORY/START-GPT61을 읽었다. 배치의 최신 병렬·읽기 전용 지시를 적용했다. 원본 생성기·preflight/test/build 실행 없이 자체 XML파서·해시 대조·PDF렌더만 수행했다.
- 쓰기 범위는 `drafts/RO01-DOTS-DRAFT.md`, `extracts/RO01/`뿐이다. 원본·코드·대장·버전·배포·운영기록·SEJIN 변경0. 시뮬레이터 작성/수정/생성/실행/행동시험0. PLC/현장/보호값 변경0. 새 Work/Codex/하위 재위임/사용자 Mac 접근0.
- 모델·추론 수준의 런타임 증명은 미확인이다. 로컬 TIA 추가 접근권한 없음. 문서에 모델을 적는 것으로 선택 확인을 대신하지 않는다.

이하 원본 경로 기본은 `source-mv06/all-in-one/`다. `0498` 등의 약칭은 `sources/decoded-original/0498-FlgNet.xml`; 선언 약칭은 `NNNN-IdentXmlPart.xml`이다. LAD 문서번호와 NID를 구분한다. 자동 refs 추출은 RID/UID/NID 후보를 모두 보존하여 동명이 참조가 섞일 수 있으므로, 아래 주장은 해당 블록 선언 파일을 직접 확인한 것만 사용했다.

| 7영역 | 상태 | 확보 범위 | 미확정 |
|---|---|---|---|
| 설비·자료 기준 | 적용 | 고유 채널·판본·소유·상충 | 현행 실물/프로브 동일성 |
| I/O·HMI | 적용/일부 미확보 | IW352:P, DB1/4/13, DB3 bits, HMI 설정 주소 | 현재 화면/단위/쓰기/값 |
| 제어 | 적용 | 선형화·호출·소비 블록·NOT·S/R | CPU 실행순서·활성·외부 Writer |
| 전기 끝점 | 적용 | 송신기/프로브/단자/AI·시공케이블, 질소 경계 | 현행 설치·승인 준공·교정 |
| 알람·복구 | 적용/복구 미확보 | 4개 알람식+OFR, BR01/MV05 영향 | 승인 복구절차·현장 결과 |
| 증상 관찰 | 적용 | 읽기 전용 비교점·기록 틀 | 실제 측정/조치 없음 |
| 완료·누락 | 적용 | 상태 분리·다음 자료 | 통합/UI/독립 검토/TIA/현장 |

## 2. I/O·HMI와 선언

### 2.1 직접 주소와 자료형

GlobalAccess의 BAD BIRID는 해당 DepDBBlock.TOD와 대조했다. 0674 RID8/11/354→Coeff DB4/Data DB1/Allarm DB3, 0682 RID3/10/15→DB1/3/2, 0628 RID4→Inputs DB13이다. SSD.AO는 bit offset이며 Word 주소와 혼동하지 않는다.

| 신호 | 형식·백업 주소 | 선언/NID·UID 및 용도 |
|---|---|---|
| R001 | Int `%IW352:P` | 0678 RID111 AO2816 Input SAM=Peripherie; NID18 UID504, 0498 W511→496.Analog_input |
| R001 원시 미러 읽기 | Int `%IW352` | 0627 RID111 AO2816 SAM=None; NID2 UID152, 0398 Move146.in |
| Inputs.RO_01 | Int DB13.DBW68 | 0629 RID113 AO544; NID2 UID153 Write, 0398 W165 |
| Data.Oxigen_RO01 | Int DB1.DBW130 | 0676 RID114 AO1040; NID18 UID507 Write. 소비 0684 RID52 NID4~7, 0585 RID129 NID14, 0668 RID4 NID15 |
| Coeff.ZERO_R01 | Int DB4.DBW44 | 0676 RID113 AO352; NID18 UID506→Zero |
| Coeff.COEFF_R01 | Int DB4.DBW46 | 0676 RID112 AO368; NID18 UID505→Coeff |
| Data.RO01_SETPOINT | Int DB1.DBW20 | 0668 RID2 AO160 NID15 UID27; 실수 임시값 변환 입력 |
| Data.RO01_MAX_SETPOINT | Int DB1.DBW26 | 0684 RID57 AO208 NID5 UID636/639/664 Read, UID37 Write |
| Allarm.Ro01_OFR | Bool DB3.DBX22.3 | 0676 RID393 AO179 NID18 UID23 Write, 0498 W24→Out_of_range |
| Allarm.Oxigen_Fault | Bool DB3.DBX9.6 | 0684 RID55 AO78 NID4 UID510 Set /516 Reset |
| Allarm.Oxigen_Too_high | Bool DB3.DBX9.7 | 0684 RID58 AO79 NID5 UID637 Set /644 Reset |
| Allarm.Oxigen_LOW | Bool DB3.DBX9.4 | 0684 RID64 AO76 NID6 UID625 Set /632 Reset |
| Allarm.RO01_Signal_Fault | Bool DB3.DBX4.4 | 0684 RID72 AO36 NID7 UID710 Set /713 Reset |
| RO01-RO02control disable | Bool `%M80.1` | 0686 RID65 AO641 NID7 UID697; 0533 Contact743는 NOT |
| ServiceBit | Bool `%M1000.0` | 0686 RID161 AO8000 NID4 UID23; 범위고장 Set 허가 |
| ON / OFF | Bool `%M0.0` / `%M0.1` | 0678 RID1/34 AO0/1, Memory; 현재 상수로 단정 금지 |
| Tag_106 / Tag_107 | Timer `%T68` / `%T117` | 0686 RID63/71; NID6 UID623/624 및 NID7 UID708/709; HMI 태그 아님 |
| Flag.RESET_ALLARM / STOP_HORN | Bool DB2.DBX6.0 / DB2.DBX6.2 | 0684 RID24/16 AO48/50; Reset 요청과 호른 플래그의 소유 분리 |
| app05 / app01 | Local Int | 0685 RID61 AO128 /RID68 AO16; 고산소 히스테리시스 임시값/채널차 임시값. 물리 IO 아님 |
| Real_SPO2 / Real_O2 | Local Real | 0669 RID3 BO128 /RID5 BO96; NID15 UID34/46 Write, NID2 UID138/139 Read |

Global DB 값과 Local 함수 임시변수는 동일 저장부가 아니다. 숫자자료형 Int 저장을 HMI 표시의 % 단위·소수점까지 확인한 것으로 표시하지 않는다. 형식에 따라 범위/반올림/오버플로가 달라지므로 일반 실수식으로만 설명하지 않는다.

### 2.2 HMI 설정과 원시값 전달

`sources/hmi_plc_tags.csv`는 dde.cfg 설정 추출이며 현재 화면 값이나 Write 이벤트 증거가 아니다. 주소를 기준으로 다음 행을 대조했다. 전체 원문 행은 `extracts/RO01/hmi-address-matches.json`에 보관했다.

| 태그 | 주소 | 내부 ID |
|---|---|---|
| data_DB1_DBW130 | DB1,INT130 | 00295 |
| data_DB1_DBW20 | DB1,INT20 | 0027D |
| data_DB1_DBW26 | DB1,INT26 | 00204 |
| Coeff_DB4_DBW44 | DB4,INT44 | 001ED |
| Coeff_DB4_DBW46 | DB4,INT46 | 002D6 |
| Allarmi_217 | DB3,X22.3 | 002B5 |
| Allarmi_37 | DB3,X4.4 | 00168 |
| Allarmi_79 | DB3,X9.6 | 0013E |
| Allarmi_80 | DB3,X9.7 | 0013D |
| Allarmi_77 | DB3,X9.4 | 00140 |
| I_RO_01 | DB13,INT68 | 0002E |

0398 LAD1071 NID2의 Move146은 W163 R001→in, W165 out1→Inputs.RO_01이다. 직전 Move145의 ENO가 W161을 거쳐 Move146.en에 연결된다. W164는 Move146.eno에서 다음 Move147.en으로 가는 선이다. 주 호출 0030 LAD1613 NID19의 HMI Inputs는 NOT Simulation(1) 접점 뒤에 있다. 이 연결은 백업 코드 구조이며 현재 스캔 실행·모든 값 갱신의 증명이 아니다. 시뮬레이션 블록은 선언 Writer 유무 검색만 하고 실행하지 않았다.

### 2.3 복수 Writer와 자료 한계

- 전체 181개 IdentXmlPart를 검색해 `Data.Oxigen_RO01`의 명시 Write는 0676 NID18 UID507을 확인했다. 다른 형식의 절대주소/블록전체/간접통신 쓰기, 외부 HMI 쓰기를 없다고 단정하지 않는다.
- `RO01_MAX_SETPOINT`는 HMI 연결주소 외에 0531의 100 상한 쓰기가 있다. HMI 입력값이 최종 유지값이라고 보장할 수 없다.
- 기존 파생 매뉴얼의 `RO01 open/close` `%M40.*`, `%M41.*` 명칭은 산소분석기 기계 개폐 출력의 증거로 채택하지 않는다. 이번 고유 채널과 직접 결속한 측정/소비 경로를 우선한다.
- 현재 CPU 값을 읽거나 산소계/계수/HMI/disable/ServiceBit를 변경하지 않았다.

## 3. 제어 구조와 영향 소유

### 3.1 RO01 선형화 호출

0498 LAD1748, analog input conversion NID18:

- Part515 Contact의 operand ORef502→0678 RID34 OFF. W517 powerrail→515.in, W516 515.out→CRef496.en.
- CRef496 RefId351, CodeBlock508 RefId5: signal linearization. W510 ORef503 ON→IN0. W511 R001→Analog_input, W512 계수→Coeff, W513 제로→Zero, W514 OutValue→DB1.DBW130, W24 Out_of_range→DB3.DBX22.3.
- OFF와 ON은 별도 메모리다. OFF 접점이 참일 때 호출되는 구조이며 호출이 없을 때 출력을 자동 0으로 만든다는 별도 근거는 이 네트워크에 없다.
- RO02 0499는 인접 독립 호출이다. 같은 이름·같은 함수 사용으로 센서 한 개로 합치지 않는다.

### 3.2 공통 함수의 환산·범위·ENO

0291 signal linearization NID1, 선언 0611/0612를 직접 재확인했다.

1. Local IN0(0611 RID1)을 Contact255로 검사. W256 뒤 Gt258·Gt190·Le259가 나뉜다.
2. 유효범위 가지: raw > -1382 (Gt258 W30/31) AND raw <=32767 (Le161 W27/28). -1382는 0612 RID25 CB `SV=_x002D_1382`, 저장 V=4294965914의 signed 표현이다. 32767은 RID29 CB V=32767이다.
3. Convert164 Int→DInt(raw), Convert167 Int→DInt(zero), Add170 DInt(raw+zero), Convert174 Int→DInt(coeff), Mul177 DInt, Div181 DInt /28000, Move185→OutValue. W227/230/234/237/241/245는 후속 en을 앞 연산 eno에 연결한다. 덧셈이므로 제로를 무조건 뺀다는 설명은 틀리다.
4. 0611 Local Analog_input/Zero/Coeff/OutValue는 Int, App3/4/5/6는 DInt다. 출력을 임의 Real·%로 바꾸지 않는다. DInt 나눗셈과 최종 Int 전달의 실제 오버플로/진단·스캔 결과는 미실행이다.
5. 범위이탈 가지: raw>32767 OR raw<=-1382→O47→Move193(-9999)→OutValue. **W21은 193.eno→Coil23.in**, W22는 Local Out_of_range operand다. 단순히 OR 비교값을 OFR에 직접 쓰는 회로가 아니다. 정상 가지에서 OFR이 반드시 어떻게 지워지는지 런타임까지 검증했다고 하지 않는다.
6. 0014 같은 함수 NID2: NOT IN0 Contact171→Move162(0)→OutValue (W168~173). 이 0은 함수 호출 시 IN0=false일 때의 내부 가지다. RO01 호출 EN=false일 때도 자동 실행된다고 확대하지 않는다.

상수 -1382/32767/28000/-9999/0은 원본 분석값이다. 시험 주입·안전 대체값·복구 권고가 아니다. 계수/제로 현재값과 제조사 교정 스케일이 없으므로 물리산소농도 환산표를 만들지 않았다.

### 3.3 산소 PID와 MV05 소유

- live_index `_7ex` doc4 STL Code는 `Data.RO01_SETPOINT → ITD → DTR → Real_SPO2`, `Data.Oxigen_RO01 → ITD → DTR → Real_O2`를 담는다. 이는 원본 보관 색인의 코드 텍스트이며 LAD 핀 원본과 동급인 완전 실행복원으로 세지 않는다. 0668 Global RID2/4와 0669 Local RID3/5 NID15 Write 선언이 입출력 저장부를 뒷받침한다. **나누기10 등 단위 변경은 이 코드 텍스트에 없다.**
- 0475 LAD5, cyc_int5 ogni 100ms NID2, CRef109 CONT_S/PID_MV05: ON→en(W189), Real_SPO2→SP_INT(W167), Real_O2→PV_IN(W168). T#100MS→CYCLE, QLMNUP→PID UP MV05(W182), QLMNDN→PID DOWN MV05(W183).
- COM_RST는 `NOT MV05_Auto OR (Oxigen_Fault AND NOT UNDER TESTING)`(Contact190/192/194, O98, W155). LMNR_HS/LS는 Inputs.MV05 open/Close의 NOT 접점이다. 자료상 파라미터 Gain2.0/TI1분/Deadband1.0/Pulse200ms/Break3초/Motor5초가 연결되어도 현행 튜닝·권고값으로 채택하지 않는다.
- 0346 LAD1708 NID6은 MV05 밸브 구동 소유다. **전단 Contact652가 NOT ON**, 수동 기억 초기화 가지 Contact654도 NOT ON이다(0617 RID1 UID24/22). 단순히 ON 운전회로라고 해석하면 안 된다.
- 그 뒤 MV05 fault 반전 허가와 개폐 상호잠금/리미트가 존재한다. 산소고장 관련으로 Open 가지는 `NOT Oxigen_Fault OR UNDER TESTING`(Contact678/680, O556), Close 가지에는 `Oxigen_Fault AND NOT UNDER TESTING`(694/696→O567.in3)이 있다. 출력 Coil561/576, Open/Close 상호NOT Contact682/698과 위치 Contact684/700까지 존재한다. 전체 허가조건을 무시한 “산소고장=밸브 즉시 닫힘”은 미확정이다.
- 이 경계 검토로 MV05 전체 모터·토크·엔코더·기계 위치를 완료하지 않는다.

### 3.4 버너와 투입 억제의 관련 소유

- 0175 LAD1858 NID5: RO01_Signal_Fault ORef244(0585 RID39)→Contact295→O219.in7(W296). O219→Contact305(해당 블록 ON 선언)→O213.in5→RCoil232 Flag.Start_Burner (W267/306/270/272). 다른 연소·온도·흡인·질소 준비계 고장과 병렬인 **BR01 시작요청 리셋**이다. 외부 버너 화염·퍼지·안전 내부회로의 동작 완료를 뜻하지 않는다.
- 0184 LAD1868 NID14의 CRef가 아닌 비교 가지: Eq1272.in1=WorkData.BR01_State, in2=**77**(ORef1435/RID128, 0586 CB V=77). W1573은 Eq.out→Ge1278.pre/Lt1286.pre. 산소 Data.Oxigen_RO01 >=60이면 Move1281 값7→BR01_State, <60이면 Move1289 값0→BR01_State. 60은 0586 RID130 V=60이다. 이때 앞단 ON/Enable start burner(1) 조건이 연결된다. 상태77 진입 여부/실행순서·현장 의미는 미확정이다.
- 같은 0184에는 별도 상태7 Eq1294 이후 Enable start burner Set, Open MV03 for washing Reset, Close MV03 for Burner Startup Set, 상태8 쓰기가 있다. **상태77 산소검사와 상태7 후속 단계는 같지 않다.** 공유 BR01 네트워크 전체를 RO01 자체 시퀀스로 세지 않는다.
- 0238 LAD1931 NID2: Oxigen_Fault(Contact97→O56.in2), Oxigen_Too_high(Contact99→O56.in3) 등 OR→Coil66 Local Disable_Load_RD01. 독립 RD01/투입 억제 소유다. RO01 물리출력으로 옮기지 않는다.

### 3.5 질소 밸브의 별도 경계

- PV05/PV06는 별도 catalog ID. FG96/PDF97은 외부 NITROGEN VALVES BOX 회로이며 공통 A6.4→96KA3 코일, 96KA3 접점5–9가 공통 공급경로에 들어간다. 하단 1/5/9 접점표와 실제 그려진 5–9 부하경로를 구분했다.
- PV05 X2:13/14, PV06 X2:15/16, 96KT1 타이머 외부 접점과 퓨즈가 별도다. 질소 준비는 96KA2 접점→E16.7. 원본 기재 전원·보호값은 현행 적용/조정 권고가 아니다. 타이머 현재값·실제 밸브 개방·가스 공급압력을 확인하지 않았다.
- 0555 RID53·0557 RID28·0558 RID36 `Start Nitrogen`은 Output AO52→Q6.4이며 선언 C는 Monitor다. 개별 PV05/PV06 출력 두 개라는 근거가 없다.
- 0538 LAD1990 NID12는 `ON AND NOT Inputs.NITROGEN TANK READY AND ServiceBit`→HYDROGEN_BOX_FAULT Set929, `ON AND RESET_ALLARM AND fault AND (ready OR NOT ServiceBit)`→Reset935. 이름 HYDROGEN과 입력 NITROGEN의 불일치를 보존한다. RO01 산소고장→질소주입 요청 Writer는 이번 명시선언/복원 LAD 검색에서 미확보이며, 없는 회로를 만들지 않는다.

## 4. 전기 전달 경로와 실제 PDF 확인

`Electrical_Rev2.pdf` 아래 세 페이지는 직접 렌더로 확인했다. 모두 DATA 27.05.2024, DISEGN G.G., NORMA IEC; 해당 페이지 footer에 별도 개정문구는 관찰되지 않았다. 파일명 Rev2를 각 페이지 현행 개정승인으로 확장하지 않는다.

| 근거 | 양 끝점·연결 | 해석/미확정 |
|---|---|---|
| FG80 / 실제 PDF81 | 110Vac 9.8→5x20 2A F→X1:209→80RO-01 terminal15, terminal16→X1:210→0Vac9.9, terminal17 GND | 송신기 표기 MOD.H705. 제조사·현행 모델·보호설정 미확인 |
| FG80 / PDF81 | 송신기7+→X1:211→+PEW352(110/2), 8−→X1:212→−PEW352(110/3); shield X1:213/80SCH1→110/2 | 4–20mA 원문 표기; 현장 극성·실제 전류 미확인 |
| FG80 / PDF81 | 송신기1+→선80.2→프로브+S, 2−→80.3→−S, 3−→80.4→−T, 4+→80.5→+T, shield80SCH2 | 프로브 RO-01과 송신기 구분. 실제 케이블/교정 상태 미확인 |
| FG110 / 실제 PDF111 | +PEW352→모듈 terminal2 I0+, −PEW352→terminal4 U0−/I0−; 80SCH1 shield, terminal18 MANA→−0Vdc10.6 | CPU515/MOD5 표기. 현행 CPU/AI 모듈 형번 확정 아님 |
| FG96 / 실제 PDF97 | Q6.4 표기 A6.4→96KA3, 외부 접점/96KT1/PV05/PV06, E16.7 준비 | 질소 관련 경계만 확인. RO01 전용 회로나 독립 완료 아님 |

시공 `Electrical_Can_Decoating_20241118.pdf` 실제 p56, 도번 CANDC-CONS-C006-056, CABLE SCHEDULE (5), D-PAGE6/TOTAL56/64. 개정1, 24.11.11, **first draft design**, TRACED J.W.Lee/DESIGNED J.H.Kim, CHECKED/APPROVED 공란. 승인 준공도라고 부르지 않는다.

| 케이블 행 | FROM→TO | 원문 사양·경로·길이 |
|---|---|---|
| 6_4 `=FLA+MV03-81RO01A` | CR→MV-03 /81RO-01, PEW352 AI | CVV-S 2S 1.0, SPARE0, route100 LBD1→E500, adjustment9, LEN47 |
| 6_13 `=FLA+MV03-81RO01B` | MV-03 FLO1TB1→MV-03 81RO-01 AC | CVV 3G 1.0, route LAD1 E400→LBD1→LAD1 E600, adjustment3, LEN4 |
| 6_21 `=FLA+HE01-RO01A` | MV-03 81RO-01→HE-01 RO-1 | CVV-S 4S 1.0, AI, route LAD1 E700→100 LAD1→100 LCD1→E700, adjustment15, LEN16 |

길이/사양은 설계 행의 숫자이며 새 발주·현장 케이블 길이 권고가 아니다. OEM80RO-01과 시공81RO-01의 prefix 차이, AB-01 출구 설명과 HE-01 위치 차이를 추적할 현장명판/배선표/준공도가 필요하다. 태그 이름을 맞추려고 원본 경로나 도면번호를 수정하지 않았다.

## 5. 알람·복구: 원본 발생식과 실제 안전복귀 분리

여기서 X=DB1.DBW130, MAX=DB1.DBW26, TEMP=Manage_TC1_2.PID_Ref_Temp다. 아래 수치는 백업의 비교상수이며 현행 보호값·안전설정으로 적용할 수 없다.

| 알람 | 원본 발생/유지·해제 구조 | 영향·주의 |
|---|---|---|
| Ro01_OFR DB3.X22.3 | 0498 호출 Out_of_range 핀←공통함수0291 Move193 ENO→Coil23 | OFF 호출조건, IN0, 원시범위/ENO 경계. 다른 알람과 별도 |
| Oxigen_Fault DB3.X9.6 | 0530 NID4: ON AND (X<=0 OR X>=200) AND ServiceBit→Set490. ON AND fault AND X>=5 AND X<=195→Reset501 및 STOP_HORN Set503 | Reset 가지에 ServiceBit/RESET_ALLARM 접점 없음. 0/200/5/195는 설정 권고 아님 |
| Oxigen_Too_high DB3.X9.7 | 0531 NID5: MAX>100이면 Move32→MAX=100. ON AND X>=MAX→Set628. ON AND fault 아래 Sub630(MAX−10)→Local app05; X<app05→Reset632/STOP_HORN Set633 | Sub.en과 Lt.pre는 W654 공통분기; ENO 직렬이라고 가정하지 않음. 등호 Reset 아님 |
| Oxigen_LOW DB3.X9.4 | 0532 NID6: OFF AND TEMP>650.0 AND X<=5→SdCoil599 S5T#1M, T68접점→Set604. OFF AND RESET_ALLARM AND fault AND (X>=20 OR TEMP<=650.0)→Reset616 | OFF gate 포함; 현재 활성 추정 금지. SdCoil을 모든 알람 공통1분으로 복제하지 않음 |
| RO01_Signal_Fault DB3.X4.4 | 0533 NID7: ON AND NOT M80.1 AND TEMP>650.0 아래 Sub669(X−RO02)→Local app01. app01<−20 OR >20→SdCoil685 S5T#1M; T117 접점→Set690. ON AND RESET_ALLARM AND fault→Reset695 | Sub.en/Lt.pre/Gt.pre W718 병렬. Reset은 차이정상/TEMP/disable을 재검사하는 가지가 아님. 반복발생 가능성·스캔순서 미검증 |

0530 W534, 0531 W660의 STOP_HORN Set는 호른 관련 플래그 쓰기다. 원인 제거·안전성 확인·전체 경보 해제·자동 재기동 완료를 증명하지 않는다. Reset 명령을 보내거나 질소/버너/MV05를 조작하지 않았다.

실제 복구 완료를 기록하려면 승인된 작업허가와 담당자 절차에 따라 원인/관찰값/교정·배선 확인, 원시값과 환산값의 동시 시각 비교, 알람 해제/재발 여부, 관련 설비 별도 허가/실제 상태를 확인해야 한다. 본 초안은 운전자가 수행할 안전시험이나 보호값 변경 절차가 아니다.

## 6. 증상별 읽기 전용 관찰·증거 틀

| 증상 | 우선 관찰점 | 비교·원인 배제 | 아직 하지 않은 일 |
|---|---|---|---|
| 표시값 고정/이상한 0 | IW352:P·IW352·Inputs.RO_01·Data.Oxigen_RO01, 시각, OFF/ON 및 호출 | 원시미러와 환산 갱신 분리; 호출 누락·IN0 가지·통신지연·스케일 차이를 구분 | 강제입력/설정 변경 없음 |
| -9999/OFR | 원시값·OFR·호출 EN/IN0·계수/제로 승인자료 | 범위검사/Move ENO의 조건과 센서전원·채널진단을 승인자료로 비교 | 단선 시험/신호 주입 없음 |
| 값 정상처럼 보여도 고장 알람 | X와 단위, ServiceBit, 범위고장/고산소/차이알람 각각 | 0530 히스테리시스/0531 MAX−10/0533 RO02 차이를 분리 | 리셋·알람 마스킹 없음 |
| RO01-RO02 차이 경보 | 두 원시/환산값·각 호출·온도·M80.1·T117 상태의 같은 시각 기록 | 채널 위치/교정 차이·갱신 정지·disable·1분 경로 검토 | RO02 정상값을 RO01 안전대체로 넣지 않음 |
| 버너가 허가되지 않음 | BR01_State, Start_Burner, RO01_Signal_Fault, 관련 허가 | 상태77 산소가지와 다른 병렬리셋 원인을 분리 | 버너 점화/퍼지/재기동시험 없음 |
| MV05 방향이 예상과 다름 | 전단 NOT ON, MV05 fault/Auto, 테스트비트, PID방향, 리미트, 개폐명령 | 0475 COM_RST와0346 출력허가를 분리 | 리미트 정상극성 추정·구동시험 없음 |
| 산소경보인데 질소주입이 확인되지 않음 | 현장 질소 준비·공통요청·외부박스 자료를 담당자 기록으로 확인 | RO01→Q6.4 직접 Writer 미확보와 외부회로/개별밸브의 차이를 명시 | 자동주입 보장·강제개방·타이머 설정 없음 |

관찰 행은 관찰자, 실제 시각/시간대, 설비/위치/단자, 값·단위·자료형, 측정/수집 도구, CPU/프로젝트 판본, 비교한 원본 위치, 원인 배제 근거, 승인 조치, 복구 증거를 별도로 받아야 한다. 미지값은 공란/미확인으로 남기고 0으로 대체하지 않는다. 사용자 운영사진·기록을 이 초안이나 공개 대장에 복제하지 않았다.

## 7. 완료·검증·누락과 인계

### 7.1 문서와 제품·현장 완료 상태

| 상태 | 결과 |
|---|---|
| documentation | draft_ready_with_gaps: RO01 7영역 초안 작성 |
| static_review | 고유 핵심7네트워크 전체 원본검토, 소비/경계8네트워크 선택검토, 자체정적단언16 통과; 독립검토 대기 |
| ui_records | not_run: PC/모바일/입력저장·재열기/실제 HMI 미검증 |
| publication | not_published: 기존 대장·버전·배포 수정 없음 |
| tia_compile | not_performed |
| live_cpu | not_performed |
| field_recovery | not_performed |

네 기능(도면·래더 비교, 백업·선택복원, 기록 전후비교, 관찰보고서/PDF)은 이 문서에 근거를 준비했으나 RO01 제품 적용/실제 저장·재읽기·재열기·합성QA/UI 구현 검증을 하지 않았다. 기존 note/repair_observation·미지필드·타설비·초안·저장키 보존. 본 문서 작성은 BC01 동등 기능 완료가 아니다.

### 7.2 의미검토 범위

- 전체 구조와 선언을 직접 본 핵심: 0498(RO01 호출), 0291/0014(공통 선형화), 0530/0531/0532/0533(4알람). 네트워크 목록·refs/wires는 extracts/RO01에 저장했다.
- 선택 소비/소유 경계: 0175 시작요청리셋, 0184 상태77 산소가지와상태7, 0475 PID입출력/Reset, 0346 전단/산소조건/개폐가지, 0238 투입억제, 0538 질소준비경보, 0398 원시미러, 0401 출력미러 방향. BR01/MV05 전체 분석 완료가 아니다.
- 0499/0474/0030/0031/0549는 인접/호출 탐색용으로 추출했고 해당 전체 의미검토 수에 넣지 않는다. 특히 0474는 MC04 설정 네트워크이며 RO01 PID 전처리 원본으로 잘못 연결하지 않았다.
- 181개 선언 파일은 관련 이름·명시 Writer를 검색/파싱한 범위다. 181개 전체 의미검토를 했다는 뜻이 아니다. 과거 다른 설비의 90개/96개 해시 검증 역시 의미검토 건수로 재사용하지 않았다.
- PDF 실제 시각 확인 4쪽: OEM81/111/97, 시공56. PDF 텍스트 추출만 한 시공27/28 등은 시각검토 완료로 세지 않는다. P&ID 텍스트 검색은 보조 탐색만 했고 이번 P&ID 실물검토 완료를 주장하지 않는다.
- 명시선언/핀 16개 자체 단언을 `review.py`로 검사했다. 첫 검사에서 -1382 signed 저장표현과 OFF RID 예상값이 어긋나 실패했다. 원본 CB V=4294965914/SV=-1382, 0532 ORef617 RID176→OFF를 재확인한 뒤 검사표현을 수정, 전부 통과했다. 원본이나 의미조건을 바꾸지 않았다.

### 7.3 단계별 실제 시각 (UTC, 2026-10-11)

| 시각 | 수행된 단계 |
|---|---|
| 10:40:13 | 배치 지시·범위 읽기 시작 |
| 10:40:21~10:40:38 | 원본 작업표준/판본/대장·기존 공유 인덱스 읽기 |
| 10:40:43~10:41:02 | RO01 고유 환산·알람/선언 추출 및 직접 핀 검토 |
| 10:41:13~10:41:37 | FG80/FG110 실제 렌더, HMI 주소·버너77 가지 확인 |
| 10:41:44 | 부모에게 OFF 호출·상태77 핵심 발견 보고 |
| 10:41:50~10:43:28 | MV05·투입/질소 경계, 시공p56·FG96 렌더, 선언 형식 검토 |
| 10:44:54 | 자체 정적단언 첫 실행, 2개 검사표현 오류 확인 |
| 10:45:01~10:45:08 | signed 상수/OFF RID 재확인, 16개 단언 통과·222개 해시 대조 완료 |

문서 저장/최종 검사 실제 시각은 아래 최종 인계에 추가한다. 시각은 위 도구 실행 관측값이며 예상 작업시간을 실제시간으로 적지 않았다.

### 7.4 남은 자료와 다음 한 작업

1. 현행 온라인 CPU/프로젝트 비교와 실제 호출·주소·ON/OFF·ServiceBit·disable·테스트비트·Write 경로를 허가된 담당자가 확인한 자료. 현재 태스크에서는 접근하지 않는다.
2. RO01/송신기 명판, 설치 위치·프로브 식별, 승인 준공도, 교정성적과 4–20mA 물리스케일/단위, 현행 계수/제로 근거. OEM80 vs 시공81 prefix 및 AB/HE 위치 상충 해결 자료.
3. HMI 화면·스케일·입력/알람 이벤트와 통신권한, 현재 설정 승인기록. 단순 CSV 주소 일치만으로 쓰기/팝업 완료로 세지 않는다.
4. RO01과 질소 공통주입 요청의 실제 논리 결속/외부박스 최신 회로, PV05/PV06 개별 실제 상태. 없으면 미확정 그대로 유지한다.
5. 다음 한 작업은 부모의 RO01 독립 스팟체크: 0498 OFF/Peripherie, 0291 DInt/ENO, 0531 병렬 Sub/비교, 0184 상태77, FG80↔110·시공p56 양 끝점을 대조 후 사용자 전달 판단. 새 현장 자료 없는 보류 재조사는 하지 않는다.

## 부록 A. 전체 선택 원본 해시·고정 Git blob 내용 대조

아래는 선택 근거·맥락·선언 검색코퍼스·보존자산 **222파일 전부**다. SHA-256은 로컬 읽기 원본과 고정 커밋 blob의 내용 SHA-256이 동일함을 확인했다. blob OID도 함께 제공한다. 중지5자산은 freeze 해시도 일치, 원본 Git 상태 변경0. 파일 수는 의미검토 수가 아니다. 개별 role/byte수/일치 결과는 `extracts/RO01/source-hashes.json`, 검사 결과는 `static-review.json`에 있다.

| 파일 | SHA-256 (로컬=고정 blob 내용) | Git blob OID |
|---|---|---|
| `.agents/skills/gme-equipment-rollout/SKILL.md` | `fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b` | `9aa820ea6ca15b4e136c9772423b78ed4df6a3d4` |
| `AGENTS.md` | `0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2` | `073164bc6efd5791032d62c71b03b4dab48cb6f8` |
| `VERSION.json` | `5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7` | `fffb51663b7705aec91cb119ca80ee943a4ce758` |
| `all-in-one/assets/program-model-data.js` | `52f8199371e3399b7c0d44ab5469f0472aced79d56bbef2887f7625f5d2aff0f` | `38f34b0caa380a16ccad6f6f1e234a2fdf23f327` |
| `all-in-one/assets/simulator-workspace.js` | `3a6dfc618ff7e7b238f2671dc85d65704f33093a18eac879d86081d92c31e8bc` | `97c2c831c77a9699fff0e0960b3bc1b7d93d45b3` |
| `all-in-one/assets/virtual-plc.js` | `5f1876052dc0067b1f010af0dfc941946e37003167481731293615d9c1c36dbc` | `0bd9eceb54365a91214a37c5601b5067c39a3f75` |
| `all-in-one/registers/equipment.json` | `7870325dff32bbca90fa34507b301c4aad3347d669fddcd03b910343663996fa` | `acc42633033398216469064932c4b76987371606` |
| `all-in-one/registers/program-model.json` | `6203479c086b15bada12ac9d7e37db9280234ec26f1ea6091d7211dc09a577c5` | `9860b10f008d3a5ae714be50d77b703dfec32f3a` |
| `all-in-one/registers/simulator-freeze.json` | `bb93c1994effc5609939ba566b7802ce7ed55154a7310f02379b308ac2c8c835` | `808ffac14dbd1b4a7d797fa6cd0d647635d90b47` |
| `all-in-one/registers/virtual-plc-test-results.json` | `a6b389f797f9a8b5ffe6928b8420f55c4cc459a327b0b48d716079d2eca6dd64` | `757dd50e45184568facb8ff62900b39d3ce848d1` |
| `all-in-one/sources/Electrical_Can_Decoating_20241118.pdf` | `3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd` | `0ee6b6f8361c5790864dbba4bbd9d55e8e7c08f8` |
| `all-in-one/sources/Electrical_Rev2.pdf` | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` | `f610fd7c7ce14ae951b00cff57b969259bfb389d` |
| `all-in-one/sources/GME_20250506.zap18` | `00c79b6d986e68298f65b172c1807115bc5d9e450a74fcc989d0796d8d8a4ea8` | `211c4f604627a32f82a1124c2a9872c2fcf00865` |
| `all-in-one/sources/PEData.plf` | `647de7ea123daced41c27bec8f81aeb93c712cac714d4754d7da5c528abb016a` | `65605ff8910f920109da731604aa5dc8d83fc956` |
| `all-in-one/sources/decoded-original/0014-FlgNet.xml` | `2e814adbaac6bab99bc668bfdab74f0fc90576324d0b88728951683869cfac30` | `4d164b074fcc13a8f97da9e24382cc169ef29555` |
| `all-in-one/sources/decoded-original/0030-FlgNet.xml` | `9252c9da764993de1edb8b2e44c46d6e9f9d4b6118e751a0dbeaa9ffd8ea721b` | `e74c70b751acdcdbc7a8b3b0c98aa773c2107cab` |
| `all-in-one/sources/decoded-original/0031-FlgNet.xml` | `76385eab8f8f72b9faa16f7cf8905f395591b18c0a9ee9e6d7dd085a38c45c65` | `653d27572de6beedcf3eb6c95702bb119a8b567f` |
| `all-in-one/sources/decoded-original/0035-IdentXmlPart.xml` | `3a1e3c8c96b30b843c6d75fc7d961972864571095dd972afa94a6b5c8c463b8b` | `c37a386e485291ed7b4387320b6eb5bfc8826183` |
| `all-in-one/sources/decoded-original/0036-IdentXmlPart.xml` | `d1b7556a1edcf20ecbe76769cd446f7960a5c50c1f464004f07acfe47c856091` | `0d48db4c91725bd3a13cf90bb6bd79144b0ed764` |
| `all-in-one/sources/decoded-original/0037-IdentXmlPart.xml` | `e92ae321d16be03fa669dc70d4703eb6dcdac4153427518e40cd7514c7bab06e` | `6070cd95a24ee9a635ef58d047310b89b57b740b` |
| `all-in-one/sources/decoded-original/0038-IdentXmlPart.xml` | `4c0347349822cbc9ac56fa868355893073215fc8fbefa094d1c7a37f236628b7` | `02dcccd2e0cdde35615e718f5ba2a53ec767f6d2` |
| `all-in-one/sources/decoded-original/0039-IdentXmlPart.xml` | `3ae955e5079c7e2f14f98035cffec43763714a9aa62d3b1defe86164aeb43486` | `00d088df9d43e85d53c2d4feab5b0364399642ae` |
| `all-in-one/sources/decoded-original/0040-IdentXmlPart.xml` | `4aa4f09101f827918ca2af003544aa0de8a70410cc4d69e738f2d6220669f182` | `dde9014e48da7a32dbb0cf9523dbdb6afcfd0bb3` |
| `all-in-one/sources/decoded-original/0041-IdentXmlPart.xml` | `f6879784dcb83569b01753a2986e4db4ddb411f64580d1e72c22c114dcdaae15` | `80b12f3b9be6cb015dacff8fc852ee4476768c0c` |
| `all-in-one/sources/decoded-original/0042-IdentXmlPart.xml` | `39a10a59ac8afcda3d1729f6b07dccea38c00227605c43cac46853fdc3e1b5e2` | `62cfa50ff1c308189542b805e9797f2294097407` |
| `all-in-one/sources/decoded-original/0043-IdentXmlPart.xml` | `c71c75f0b13763a806cc984f933fd0ec785f77a0fe6915267ebf7648189ddb33` | `f20ba4e4479e42f8496e637a0e755814fe1dac56` |
| `all-in-one/sources/decoded-original/0044-IdentXmlPart.xml` | `80ed7b8be0e4988ac52ac84cbc7e68a29a15755c821d9b0452247d9f362638c2` | `eb44635cb72b77f04dea4319e47d96ee68c09a58` |
| `all-in-one/sources/decoded-original/0045-IdentXmlPart.xml` | `334d3c31a4dc1084cd9e6d870058e32f5e96c17ece69e5fc52038965416a1c79` | `d455986215307b725280a4ff3beea011d8d37e25` |
| `all-in-one/sources/decoded-original/0046-IdentXmlPart.xml` | `1df29e9d0382743dcf42b287223f63f9880740616318769d8e23fdb8a68a97b1` | `8c7426049cdd9f9f00d96c6298af443d5a336e38` |
| `all-in-one/sources/decoded-original/0047-IdentXmlPart.xml` | `2e53bb895dd1ad2a74efaeb1ef16dfd61e62b1b2d7aa34cec8612f1b9cb0928e` | `3dc282f149a21fdf76d5521ef1c833be63b578b4` |
| `all-in-one/sources/decoded-original/0048-IdentXmlPart.xml` | `d8e8687de7271bd294c2b62b33d789700af9d5014d82b130141988c4d479253d` | `64fc5a7f1ad33f3b901b00f0d22d23578ffabff8` |
| `all-in-one/sources/decoded-original/0049-IdentXmlPart.xml` | `d4c49fa00735537ee8cce4baba526b0027e4fe25343074e83de5719cafd1bacc` | `50478b19d7a3d4af551c914f181fb25b6f809331` |
| `all-in-one/sources/decoded-original/0050-IdentXmlPart.xml` | `f7ceb0408380d3fad2df3bbf5c663c393b57d1ce156af7a587e14c6b1eb701e3` | `9a94a69077a225b05da86a8118b5ec1622dcc629` |
| `all-in-one/sources/decoded-original/0051-IdentXmlPart.xml` | `b43718d933537099d8ab3fac88b2012d088d46b69ca1d31ac1570bae4a62cd6c` | `2c7597408597e1cce84deca2d0a01c2465b72eb7` |
| `all-in-one/sources/decoded-original/0052-IdentXmlPart.xml` | `fbd673549a61f7da169e452e2221da4958b29b3e3c1c3699e9cad3d02577500a` | `9304a3d08ead7483362605eca3169e15518fa6b9` |
| `all-in-one/sources/decoded-original/0053-IdentXmlPart.xml` | `1d386f98f7bc842e474cf9448dbe37ff3f86775797644252b56d7407e1936c80` | `27c0527904f201efbdd33c50d1e94c08a3f4ecf4` |
| `all-in-one/sources/decoded-original/0054-IdentXmlPart.xml` | `32d9ad8334dc4c115b04e24702a02051de3155e007de26fba4e32b2d43a1e87f` | `ae93a5d3b602ba2e35990bcf904571009388757f` |
| `all-in-one/sources/decoded-original/0055-IdentXmlPart.xml` | `9baf3104be3c8a3457c3eea021f23fbd6a60c665e81a293bd7f2cae52c64be29` | `85d87193fda164b5c7282f6e40ec5f49b3383309` |
| `all-in-one/sources/decoded-original/0056-IdentXmlPart.xml` | `c5ec45cd232c36d80f80487ec0dd284a876e326ba2286fc722ecc861a400232a` | `1364306d64caf1f1f094c98dc163edf69cdc1afc` |
| `all-in-one/sources/decoded-original/0057-IdentXmlPart.xml` | `1124275ab34e188b042b263d3c4b744abf5637ffd229af642b81a27f00a00c6b` | `264d24445f42cf32706bc6942863f9f227eb797e` |
| `all-in-one/sources/decoded-original/0058-IdentXmlPart.xml` | `84db55242df6a85df73776bfd23bf16cc10e4da35fedca4942f4a43bc4cd1702` | `f13bf595dc1b216bb375b7374b8d849dc7db7c95` |
| `all-in-one/sources/decoded-original/0059-IdentXmlPart.xml` | `f02ef8f08f1c7ca7625bdbcf90a2c9365f12654d19e2e526fe8e5b0b742263d0` | `ccbe8f3e8aadc1c9a052629b674e47805371c84b` |
| `all-in-one/sources/decoded-original/0060-IdentXmlPart.xml` | `d61344a049baa2ce8a97335cd94e6c1753f8f8b7180d3def74d8631ff2cf21b9` | `8751e6aab7045a8f0a6f9d515197aeb5c81ba6dd` |
| `all-in-one/sources/decoded-original/0061-IdentXmlPart.xml` | `0861f9e3686b911262b7b7e108c51fc9fed9cb7080c72bcc4b3aae60750af1c7` | `736313f3bebebf3ba6ee674b058a43185520d391` |
| `all-in-one/sources/decoded-original/0062-IdentXmlPart.xml` | `34f188168dc4fad0d6e2c813028045f37b84025636bcebd8aa1c7ffb4cfd9bcd` | `624eed3ba6cd1eb54e7e3f316f8c4c159ca3b4b5` |
| `all-in-one/sources/decoded-original/0063-IdentXmlPart.xml` | `9dceae18963ead11293cfc3a70c2eac077faa53ebd28e23bb4e84bc3278c5034` | `9de78fc3f67460e61214d2bed3ec5b6e4e82bd92` |
| `all-in-one/sources/decoded-original/0064-IdentXmlPart.xml` | `ce6afc4f7ca0a8059c2e3cab25d202f0faaa49a3bc6a2e9ee238964a76e9fc9d` | `300d74239868f4f4595d4d5bbb848b4b58bbae76` |
| `all-in-one/sources/decoded-original/0065-IdentXmlPart.xml` | `c99a9960a364084a8e9f007803db72ebaf0ac0ea9126c1b0692da1e5337b33be` | `a427905d03fe4cf63cf6b9d0315a1be8d1bcd04d` |
| `all-in-one/sources/decoded-original/0066-IdentXmlPart.xml` | `13ff943033934043bb50d38d95e46706443a12b1eef70471cb0f35d3b0ade402` | `55adec8d054eb4d3b186c6498616457ad254c22f` |
| `all-in-one/sources/decoded-original/0067-IdentXmlPart.xml` | `0aa469d4f7a20bde2a5bccc6c91b3d9c48929460bd68ef32e0217d53f4d68628` | `455f00638f1618f194b1c83d9c0c2f157663a902` |
| `all-in-one/sources/decoded-original/0068-IdentXmlPart.xml` | `0a71d492e69760390b99f71a75f02ef684e271554b003d5de8bf64a26c64eeba` | `abf1e8cf672afee026f7945219fcee8ad62c9787` |
| `all-in-one/sources/decoded-original/0069-IdentXmlPart.xml` | `da5203cd92ccadfea2029aafb45a1e6e99443d7edbbcc2fd2f2927482564590d` | `26204ec172cabfadf54c1ad6a74013bfaae06a11` |
| `all-in-one/sources/decoded-original/0070-IdentXmlPart.xml` | `bac2852c85f039a342a0066b3c38df60c572d89b3358fb889b104126d530a447` | `061988f3b48be1073ca3fac3dbf335fc9e79b0fb` |
| `all-in-one/sources/decoded-original/0071-IdentXmlPart.xml` | `49d01eba491fe39ed64cb9b15719f3445f49979ddc73753cb398628075b0d6c3` | `6f3924a0d75ac7ee3820e83d2873109dd1291b33` |
| `all-in-one/sources/decoded-original/0072-IdentXmlPart.xml` | `4528729656e87a902d9be2ab85d2b890b2cb3c68df619b881781eff985eede27` | `7c5a73659e4eba679dd85c8774cc9cf6ce770b3b` |
| `all-in-one/sources/decoded-original/0175-FlgNet.xml` | `41279d6aaa157de3be963d010d6ca7dea94811a0ace519c8a3d8baa015f67f97` | `1626da00b3bbcb46f77720271ecf0f50db9dc63b` |
| `all-in-one/sources/decoded-original/0184-FlgNet.xml` | `a0a59597c73eb68e1cbdb2f41d640eabccfd05655c4e9c08624be6027974caf3` | `da94babe74df340b11b37560e94e04acfad1212a` |
| `all-in-one/sources/decoded-original/0238-FlgNet.xml` | `8f6a5537084e092c352552dc469bbe8469b33412971219e51bba211ef607dfa8` | `c1093180555a6a00486d0a7268bb3a059b7cbf9e` |
| `all-in-one/sources/decoded-original/0291-FlgNet.xml` | `fe0b92f074eba25148ce34084649af3d968962558d652727f1eea19f3e3c2550` | `1418fb2ed172c6df694a5eb8bf2dffd0b177653b` |
| `all-in-one/sources/decoded-original/0346-FlgNet.xml` | `7c782d799751476d88794a5d3d993e91878e03a39147d3b13233193dd3f6ce09` | `da4eb2f53c127242aeeca371ae3ee4d29228d4f1` |
| `all-in-one/sources/decoded-original/0398-FlgNet.xml` | `4f092b18df4e44af98fd44e173f48dad213a4e80b71f46b0a5e8a700f5b0a747` | `67ebb54daa55093487ea7e780f23ae2cf193c397` |
| `all-in-one/sources/decoded-original/0401-FlgNet.xml` | `60171c213e666de544077b7e4b497675813f7c0e75df85a3e76ab1def49b04ae` | `aadefbd35d305dd4a1146bf383b988a903802bf4` |
| `all-in-one/sources/decoded-original/0474-FlgNet.xml` | `a706b93232fdc7449a43265c3b953a3180fde5e5b46b05915ca8db7f4327ee4d` | `bff34142da23ea8cac1706f4193787237e261cf9` |
| `all-in-one/sources/decoded-original/0475-FlgNet.xml` | `ca3a5bf5bce9189b7c63dd27057b6b759e74a7793d34d2d050fe7e69951ae2b3` | `5d03d472dc65fb5dc6b0442caae0167b938bf57f` |
| `all-in-one/sources/decoded-original/0498-FlgNet.xml` | `88d25f691eb2199794f0013d98a91cd42bf6a9dec98d64b290014b72e7ab8fcd` | `d84c6cac73e0fefcbb4a100792235a21324f91fb` |
| `all-in-one/sources/decoded-original/0499-FlgNet.xml` | `6526c8da7b45f38e72d8ebd8c177889a58f7e2db7265d1572db5a8c7dd6e0467` | `bea1c6292c4ca6319180e18544905727a4cc7030` |
| `all-in-one/sources/decoded-original/0530-FlgNet.xml` | `9f20c55030b3127abfedce38de08e50d494885cdf61d75c85a2715b0d380eac5` | `8058859ea175ef384e9ffc63a1785af3f576ddae` |
| `all-in-one/sources/decoded-original/0531-FlgNet.xml` | `d53b8ca1482c4365251a3b1d0f108ed32fa4e5b8f78848e2ceb48648f2d7095e` | `f6400b188f6f2363aabf50428046e42b8b95327a` |
| `all-in-one/sources/decoded-original/0532-FlgNet.xml` | `63b649820f729a693a38203c57eb79c1a25fbd4374e3e3aa79609b47f1c3c980` | `cf51b7ff14d717691648ab811be51293af847ba3` |
| `all-in-one/sources/decoded-original/0533-FlgNet.xml` | `3fd228af5f1eeb7c88b48cef59b9faa2e601cbe318498a26c8c339957fc01d58` | `7bdb10ef38a2f07e0e66f4e0f78e68ce82ab7347` |
| `all-in-one/sources/decoded-original/0538-FlgNet.xml` | `afb3c3104bb60b4b1310f62ed5fb2caf659afc514c2b3fd209ff71d2008686ce` | `3372843d3fb58f402f82a6250588ffa90f7707dc` |
| `all-in-one/sources/decoded-original/0549-FlgNet.xml` | `49f7169c33ed7f54559b0801e21a7d618584900972840e91cf51ad032e8febb1` | `985b5310b43b1015b5dee286aa0e42800564b94b` |
| `all-in-one/sources/decoded-original/0552-IdentXmlPart.xml` | `d6cb81b6330e182c430061b494463a73065bd9a0945f39e9a15bb8de8d81703d` | `3b5cfce8d91f75b4d1a8130b79e031d6ab54fb8c` |
| `all-in-one/sources/decoded-original/0553-IdentXmlPart.xml` | `4bf2f2c613e81ee6bd92ac0f21252ea0ce4a1135818fcc404740a914aaae1317` | `ec2344a9d25560ef4d6e53951804ceaf21326c1d` |
| `all-in-one/sources/decoded-original/0554-IdentXmlPart.xml` | `4ae3e7d0bca0f78c9e94617abeb70bdd228d85d74bff2224174fa1bb0076e78c` | `cdb68b35a7287f6b5636c01ea3a01747d3d60e81` |
| `all-in-one/sources/decoded-original/0555-IdentXmlPart.xml` | `46c36333e249dd775c1db94a1f6e80a36cf1a5a9c998b7d0980ae01d862901e6` | `9a915a8b9a260b48402df151c1fe0bbcb2f4ea1c` |
| `all-in-one/sources/decoded-original/0556-IdentXmlPart.xml` | `065d71114e26c93af180265e0e6d59d2a190af1f2f0581c5265e7f4f67d6e23f` | `15ae569ff390ef5c791b0f76d96bd86d5ec6b938` |
| `all-in-one/sources/decoded-original/0557-IdentXmlPart.xml` | `536563da118493838d346a6b34b4367bed4185edbe150d79eb2b2042c3950bf0` | `f627dd27d001a8af1770fd43a5dc04ceb572d4e6` |
| `all-in-one/sources/decoded-original/0558-IdentXmlPart.xml` | `45d49d53b6b41312960bb2a329663e87d8803e28d7832308424a6bf5091e6d1b` | `a0b681bd15e9ae15f2e1437576a4486cc732fdf2` |
| `all-in-one/sources/decoded-original/0559-IdentXmlPart.xml` | `ec5c6d3f18cbedc2bf695fb1318c1d3a8d2a71c77fbd4ab30d286e2399a289d1` | `9431d19cf594838e7a451404e1116e4daa822f81` |
| `all-in-one/sources/decoded-original/0560-IdentXmlPart.xml` | `847792a7620ed331f784353ef8037be10ba1618b02c8693cd297585d2357089c` | `54cdd99a46efddab91d2724bae1e596239290968` |
| `all-in-one/sources/decoded-original/0561-IdentXmlPart.xml` | `ac8a4f7b366a262b9d488b5b78aabe8b2dea768753b58993fe7f846989dac0d7` | `0f8308086219f23c888dcb4ead96dd954842ed68` |
| `all-in-one/sources/decoded-original/0562-IdentXmlPart.xml` | `85aada44dd9a3e66835463c3fed400f1efe121f4f5bc5ab8f0ad49481ec0ea1c` | `1609802542a3e560baba3f2b73c306be281dfb23` |
| `all-in-one/sources/decoded-original/0563-IdentXmlPart.xml` | `86cf35b6baebc079cb5a092baf53ec3364c377ea7318eb263ab69c8b4550b4ad` | `6a10fc694f896cda16409804daf2554c91635654` |
| `all-in-one/sources/decoded-original/0564-IdentXmlPart.xml` | `2aed17fa02d19b0a081023282841aa561d6a2dca3e393284da3622b967af00b1` | `c4b1f2cb191970cfce1cce59cb290a9f1f934c37` |
| `all-in-one/sources/decoded-original/0565-IdentXmlPart.xml` | `0f7f970faa6c456f2bb032b1a2072a2f52db1e03fc77bd8d35d4583deeaf1149` | `c2e3e2d57c94c5da864f6e172f0a7a925da942d6` |
| `all-in-one/sources/decoded-original/0566-IdentXmlPart.xml` | `a1914c7ae085acc1f949a649979824bec8b46fcd78a8055318272a1eb5a45265` | `348e6fccf44a8497f58f73e89ec98e892b2df436` |
| `all-in-one/sources/decoded-original/0567-IdentXmlPart.xml` | `5d428b5d5a2b0f4649dbbbb4e4f060a9d89a107e9cf4b6139d8f003c4371347e` | `48d2fdc3a37b692bfda5234b3cd84c48269552f2` |
| `all-in-one/sources/decoded-original/0568-IdentXmlPart.xml` | `4ea2540c76f86ab5b17a30c7c9182cc0026bc6b05e605eddcd4af6fc3b919f89` | `c3b9bb052c2200805c3d0af5237d41ebaafaaad5` |
| `all-in-one/sources/decoded-original/0569-IdentXmlPart.xml` | `2e77bb83cf9a7aecd228dac33fe1c897e1149f2063786f4f4e54c66be618a2c7` | `d58446112989460d247fc9f2e1b39bb7e4ada67d` |
| `all-in-one/sources/decoded-original/0570-IdentXmlPart.xml` | `9fed133006458c3b43b1d5f2c15107a5a86b4fb7cdbaf3743bf88f0e5a105495` | `15e6452f424d6ef5f0fa2407ae4e4121dbca3044` |
| `all-in-one/sources/decoded-original/0571-IdentXmlPart.xml` | `4a9deeb65a22e497e284fe6d98929e1d201ef5939e4aeca5805b4eb7e007d398` | `1c37da5dfd669fc2606d5d8316dbb7df4978ab19` |
| `all-in-one/sources/decoded-original/0572-IdentXmlPart.xml` | `5ecd18f84e12d702bb46f759b23994dacfa2d97d50fe51e766ca0cf43f75bb4c` | `67fbbd3e804418687c2ceaaea357fbc3016d38b9` |
| `all-in-one/sources/decoded-original/0573-IdentXmlPart.xml` | `a22cc24a974e0c792f32e356a14b277a847e2bb204c91bce01c37d1714ddb56c` | `97541d25722c43abf428aa8e2197b1973149bde2` |
| `all-in-one/sources/decoded-original/0574-IdentXmlPart.xml` | `0773bc969180298193ed6affe56b485bd2141949f4467dcaf33afbb16ee496cf` | `49305a0a06bfcf6957d93ca1188676def23cb2b1` |
| `all-in-one/sources/decoded-original/0575-IdentXmlPart.xml` | `40e7b2caf89ab7f1ed9075547a7728bd02441e24451bdd8bf97c843637daad06` | `07d5d2548e8f36252a346d0b83341e27c3cb14ba` |
| `all-in-one/sources/decoded-original/0576-IdentXmlPart.xml` | `c8b5f9b9ead0e124f1f817b49d89611ed7b2ce04ecd91ddaa139f2ec89d48dbe` | `819b47160eaa6d08c212f71e5b5486ef5b55b6f2` |
| `all-in-one/sources/decoded-original/0577-IdentXmlPart.xml` | `511e01fae619dc385357908a1ac62030dbdfd5f5399bd4c22bc58bebbfc3bf47` | `a505ebf7efd05a85850dc29559a4f71242bacae3` |
| `all-in-one/sources/decoded-original/0578-IdentXmlPart.xml` | `0f9f41b5dee25ea17c7a29ab6f7b00503c13d0f265266acd660072baf061d32b` | `070a79fb12139898dd44a17ab2061e795956b9c6` |
| `all-in-one/sources/decoded-original/0579-IdentXmlPart.xml` | `ee35cf525388f2b38399787caef57a978b0bb17216a90e1a90ac4391e0e799fe` | `19d1039319ffeb150767d96fc36205326483b1c4` |
| `all-in-one/sources/decoded-original/0580-IdentXmlPart.xml` | `fa748a6c1890f579d694fd5e561b2304f717da79e5352ca32152cc20e877c6ff` | `9bd503f23708fada1a1f871e0e52b0eb75e9aacf` |
| `all-in-one/sources/decoded-original/0581-IdentXmlPart.xml` | `5d1d7372935d984aa2d701aa70bdb4555ee1e98d0b0c23806db7bda1ad9134c5` | `2614704e8c68a43d20f3fbb6b1d300b9f8b7199f` |
| `all-in-one/sources/decoded-original/0582-IdentXmlPart.xml` | `41d4c2bd750392bbc2edc43995ec3a9da47a63c13ee86496df8f187492008951` | `82636dec064876d0f4cc714ef385b07d6e05efe0` |
| `all-in-one/sources/decoded-original/0583-IdentXmlPart.xml` | `0a34a2b7ad17eba6198dbe53d5c6aa8e87710c7436b832b9d39a075074ab58a8` | `63a23c921a53805f135a0399ba076265907d0eda` |
| `all-in-one/sources/decoded-original/0584-IdentXmlPart.xml` | `3bff6c478e594bf97bb1730971944e96b0b5e2407199420fe6567d5fe609ea5d` | `0f8dde829be66041bea79e40ccc4586d84ff1da7` |
| `all-in-one/sources/decoded-original/0585-IdentXmlPart.xml` | `e36ec18aa4abebea8f9160254522bb51ff722eae804c5a469790f85f02939184` | `16574d37ef3ca61b59ba396c400e269ab1dd3440` |
| `all-in-one/sources/decoded-original/0586-IdentXmlPart.xml` | `f16c4c68bde8a737372c219a10b21501653dfd3ba8c59bd84b60ae6d62da8250` | `266989c590cf52f82e1553f8626a209b8c0b6e0b` |
| `all-in-one/sources/decoded-original/0587-IdentXmlPart.xml` | `bab957ac7c180d9c91b4f904b29e9dbd5812c6ba8f7b9e0c7faf9708605b203e` | `67e84e4b8d43b7c5864ec40fcc2c9fbc2222b436` |
| `all-in-one/sources/decoded-original/0588-IdentXmlPart.xml` | `def5646a0d1eacaae81518f0952c4ba8ada5ea38852463a1d463ff439f3d1905` | `07d012cdc3fb0662f8126f4c274a36288e3bfc9b` |
| `all-in-one/sources/decoded-original/0589-IdentXmlPart.xml` | `846630f3832df93ccdcb0bf86a029546886f8cdba51cd952eed63257ee4540e2` | `5de11972e1fb84f02e4585a53fab478d54e203d0` |
| `all-in-one/sources/decoded-original/0590-IdentXmlPart.xml` | `baff7271b3db646e8953c31d20b72f7b044b1154b689b15ca0fb38ebb44ad81c` | `5816a1fc640da97d27ec68c8c45f255a0bd60730` |
| `all-in-one/sources/decoded-original/0591-IdentXmlPart.xml` | `2e165c44fc9df852ea3729b3ddb33dc0a74e4f8826676f9c5c5626e1dce033f8` | `407456d55041d82dd19e551f904a217a11478289` |
| `all-in-one/sources/decoded-original/0592-IdentXmlPart.xml` | `d157e3d92df9e4a6ce46567b8611a51b0a10abf4dd7f9c4e613087b2df9583a8` | `09bbf459f42d75a973dad70dcfa6871c668b0851` |
| `all-in-one/sources/decoded-original/0593-IdentXmlPart.xml` | `504568b5b50bb25a6880e9da724f79438fbb07e7a311a9391681143d713499e9` | `f2447d339be5de33caf49e1dd56d970eecfd23a2` |
| `all-in-one/sources/decoded-original/0594-IdentXmlPart.xml` | `88ad174a0d5ccdf636146b68e43aa578c449c77ceab074b7ced2580261b831cd` | `f38b7d9a52b3d5ae74953da8290f6b417758c1b5` |
| `all-in-one/sources/decoded-original/0595-IdentXmlPart.xml` | `10c8152d3ae704c00e5d4c2f6ef1629be5a65aaf5ef626e1ea6085b9204f8f52` | `1f24565efac58926dabf5b3fc54ad0e9537410b2` |
| `all-in-one/sources/decoded-original/0596-IdentXmlPart.xml` | `a0d79c7c4971d16f0e176c0c7d7b459a6e6702035b01ec01fd83e95561839dc0` | `c8b2d1a05727b4ca44e2e4bed9fb58ba2b717576` |
| `all-in-one/sources/decoded-original/0597-IdentXmlPart.xml` | `60e292145fe54912a1da7510c8641a4f4c85efe62e1b5206ee3d92794a28de20` | `2831597d1879bd83f239e838dd4cbe6b3dc64e77` |
| `all-in-one/sources/decoded-original/0598-IdentXmlPart.xml` | `dc001c9370a691546c5dea79f5a1252d6d0a5564754703018c47df4bcc2522bb` | `17a4c24ebc97eb13db483e4c64ac386d6a69125a` |
| `all-in-one/sources/decoded-original/0599-IdentXmlPart.xml` | `32a693fe12134febbd9f5c7da10c3469ef4d5b164ab8b6bd9ea3867c358936c1` | `493de77fc827d8f14192ced05d82df3a062f7965` |
| `all-in-one/sources/decoded-original/0600-IdentXmlPart.xml` | `20c58ee0383d0b6c275bd2d96abd30af7c5d1f3fff59c7d5034cd758936b57d5` | `f22a7ededd0576cf379ee19908da067f08d45412` |
| `all-in-one/sources/decoded-original/0601-IdentXmlPart.xml` | `04c9481f7381284de689ef5c7ff40d7aea93f2004cd877a4e4f27e47baa6d862` | `07bcf656fa58e4a305999456644acd24b3dc6bec` |
| `all-in-one/sources/decoded-original/0602-IdentXmlPart.xml` | `46ab21151eddaaf616469db520730c60423eb742aa491af194e6710c751b4caf` | `bcb12ab1ce8c476ff921baa1608f29d9822f76b4` |
| `all-in-one/sources/decoded-original/0603-IdentXmlPart.xml` | `e93969dfa281d75b49b24127793068e33472dadb19729c1c48fc4a8dad075ef8` | `3a92b304baf4dbf6147e944d9778d2da11285cb1` |
| `all-in-one/sources/decoded-original/0604-IdentXmlPart.xml` | `b798d29c5499b5314a1ee3cff9139dae64c887533b86baa43b6e9a052373a6af` | `bb2c318788b97e7a4924a176275c12d805aa519d` |
| `all-in-one/sources/decoded-original/0605-IdentXmlPart.xml` | `0ff6e2228dbfbc9f657359fe1055083ce621365084ea24c4160e4969b3eaac8b` | `30e199288c147aa22d5ce8407178a391b89c6b1b` |
| `all-in-one/sources/decoded-original/0606-IdentXmlPart.xml` | `73d45f9e2a34bba8a25df1ed1f71e8f6404fc96a8d6481672652a48435b6a740` | `ced032fa747a8544abf17058ee5ebaa78ba9b23b` |
| `all-in-one/sources/decoded-original/0607-IdentXmlPart.xml` | `9b76b53536a26e7b45961fecbf825ae1552e16c2fd9af5736864193c01d77f93` | `dbd4da513171f04cca9b1c1741d0293c3e38f98c` |
| `all-in-one/sources/decoded-original/0608-IdentXmlPart.xml` | `24adec2035b65c0c310d637bcea74374896875b6465a16aa2f2cfc8fd55fa4b8` | `cea8f4160d2da00023b1ecc5e591b561e4a08330` |
| `all-in-one/sources/decoded-original/0609-IdentXmlPart.xml` | `395de8ebb2168848cf96fe015bd7334d71107c114a4e441ef36346b8f22031db` | `ee2aab34c0116642dd9f4364b236426f78a876a3` |
| `all-in-one/sources/decoded-original/0610-IdentXmlPart.xml` | `c58d07b1b9707dc8c6c2f06c34ee6142f72238a4cf3f376bee8502d1a9532f9d` | `1497b6bfd7fd9b8afe427b9c910d15e9cf888f9c` |
| `all-in-one/sources/decoded-original/0611-IdentXmlPart.xml` | `0d583915a261703954da22c176ba9f81338ad13ea2810e7cd5f7de8aa1bfa089` | `bad6b16fb32a32d47d882f48754994887457872b` |
| `all-in-one/sources/decoded-original/0612-IdentXmlPart.xml` | `95b545d4964d371ebfc107894ea90b8b1d0d7ab5d3a70e643f8ce539063c0f38` | `7cc782d33d07ef225c2104f3e7c9fbd31f7c7467` |
| `all-in-one/sources/decoded-original/0613-IdentXmlPart.xml` | `09d3b1397a987898334218f37e025661af162438582e649f671e7abec443d3cb` | `c9d19a48e947098914f4d2de3348c05b4f6d37e8` |
| `all-in-one/sources/decoded-original/0614-IdentXmlPart.xml` | `c6de26f74d75f5be858a406de75eaf6faf62ba9b89c8f9a085b5dd206e93d294` | `da0485aa033700f08c8695d30b93ebd2d377d6c7` |
| `all-in-one/sources/decoded-original/0615-IdentXmlPart.xml` | `80f4544edca56c6e6bb2713c758c92ade9202255110074931e03fe34d0d0801a` | `49eb86fe01feb83de8c0864b21493d305aff8b20` |
| `all-in-one/sources/decoded-original/0616-IdentXmlPart.xml` | `650b53354a0c8443d94adc5bd6a860d3c5313014a52e0fb98a5656a65b58cc0d` | `9f7fdd5f93ac149c139a054ebb34f63c632ef7fd` |
| `all-in-one/sources/decoded-original/0617-IdentXmlPart.xml` | `10bcf85169cb2512f55acadaef299a3d46b4b4cecd88032d739cfeba23e94aa9` | `9527658ee6808be34bd513b1b2ebaf3a4a5a6f3e` |
| `all-in-one/sources/decoded-original/0618-IdentXmlPart.xml` | `0c6762de9cdf0e294317f7463bea3d8e6df5673d333d9b1826ebd17a7ded044c` | `9eec0dbd8abde4aa7295f77b63ad473f895f274b` |
| `all-in-one/sources/decoded-original/0619-IdentXmlPart.xml` | `85694bb5b696e31e6a1217431112e5b750516c4f94078d6e127d4394a8b80456` | `11f0502c84a1f319a21459a35c0dc1c6ce8e8f36` |
| `all-in-one/sources/decoded-original/0620-IdentXmlPart.xml` | `da97226a148a1a8babaea67db412761a718b7e7537212b7807e8ea27d000d2d3` | `dc88b5e87ad3331928f14fcf647673a26fb70b6b` |
| `all-in-one/sources/decoded-original/0621-IdentXmlPart.xml` | `a63e2b97ea9eb2691cb478666afed77fc58a2da2f8170422dc09e24b102c88ee` | `844516839e55f8bf231a18630e010b912190664e` |
| `all-in-one/sources/decoded-original/0622-IdentXmlPart.xml` | `f0b997f1246d76cff71de2160eb617caa936e6987bdf43c73f55cdcf77dccdb6` | `3b1ae1987950d0754aec37282960b314e9913cd3` |
| `all-in-one/sources/decoded-original/0623-IdentXmlPart.xml` | `4acd00406ea92466169e57e59fc90b0da4d9ec55fd19e2e96c9556e939cb83a6` | `13b3af0459c8e6069bb9b2f1b16454bf479e08dc` |
| `all-in-one/sources/decoded-original/0624-IdentXmlPart.xml` | `24607c0827fbde428bccf8637ef4ae490798a69a7c2f3b87861d0749082d367a` | `02511fea47fc47981c101bba49dc40adde1cdcc3` |
| `all-in-one/sources/decoded-original/0625-IdentXmlPart.xml` | `17a9f9bd540bf0a54e9973391fa258d81e567248fd201ae4ff32c367359e69f9` | `047b29b8c09a15a666553bf04eb4fb00f00e1bf8` |
| `all-in-one/sources/decoded-original/0626-IdentXmlPart.xml` | `a9d7fbea345eca70325a8c2e44058c23e96add1b7207eabbb09445118b18188b` | `e0fc80d0c20f4db3eea31d35f578a2fa3c09f8e7` |
| `all-in-one/sources/decoded-original/0627-IdentXmlPart.xml` | `08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb` | `61ebc0abbb2ca160e11e1da400a3f14a397d8bc5` |
| `all-in-one/sources/decoded-original/0628-IdentXmlPart.xml` | `9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd` | `170ca5c72599edc7ea7eefe651c3680ce325e76a` |
| `all-in-one/sources/decoded-original/0629-IdentXmlPart.xml` | `67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972` | `058129bb01e27f7a6a0d0293f332d745e5bab74e` |
| `all-in-one/sources/decoded-original/0630-IdentXmlPart.xml` | `1526a89b425470fa6e874bb4a9b6c7bc8e58b740f80d018b9106b6916f402372` | `2d2963f05fe262504f7b8f72454b9f7bc6266a7d` |
| `all-in-one/sources/decoded-original/0631-IdentXmlPart.xml` | `8e5072374f8ef098de72fbf93965b2a7bb0965c0f803e397daa68588c0c38555` | `27aa5aef2b126820b4658362e4aad5ca6d709fee` |
| `all-in-one/sources/decoded-original/0632-IdentXmlPart.xml` | `fd162c603476c2cac899010cee7a8ee382b6092c115135e3ac1007ae71c544e9` | `600935fa8d394c0d247ea20040d5dfff4f05b500` |
| `all-in-one/sources/decoded-original/0633-IdentXmlPart.xml` | `9e00aa275fa1b4e488b73983b309c6b73dcf4f3dd9be5dec13e9975d68f3c0fc` | `a1ab5ee12addbc92d04c9950d4437e2b564d6b5c` |
| `all-in-one/sources/decoded-original/0634-IdentXmlPart.xml` | `af3fcb536a6270ffb9a19e5b3f2c284a38d67d465f5147961005c1c01d11299d` | `877d9e0734dc7f3e5a8cea789eeb58a208501f48` |
| `all-in-one/sources/decoded-original/0635-IdentXmlPart.xml` | `1a057d686446a3fdab7ac61bb09bc543c52f49646c9ca71ac323c10fcdffe457` | `95bfcad59cfb0c12b573e9e8face4262d1e94622` |
| `all-in-one/sources/decoded-original/0636-IdentXmlPart.xml` | `ec3d79f03e2748f8def4409ad676a97b98e28b9d8e68f6a64b3fe894466832ca` | `86114327ba1a010b2fcc01dd12b1bf86c01bc02c` |
| `all-in-one/sources/decoded-original/0637-IdentXmlPart.xml` | `3fb68f57dbe2a877c4ad5aa1b3316810cf84958f2d13b5b1d7d321e0915271c7` | `cb1d7fb76aa2afd96eb46984cc1e71b77f36395c` |
| `all-in-one/sources/decoded-original/0638-IdentXmlPart.xml` | `878e7b33a4adb054e172843a7519157e39a5e779a1984fc9ec88cc5c465d5d33` | `c5820897c6028dac5ac9955738be074b528c554b` |
| `all-in-one/sources/decoded-original/0639-IdentXmlPart.xml` | `ae39316c2b618c0783fc1b3889f47d12d8b2a53198c9a7e7b3c40070338c9539` | `c7e224166db0c7ce33275a788633ac549ade6781` |
| `all-in-one/sources/decoded-original/0640-IdentXmlPart.xml` | `2873e2c70eb4ce97c104b00b675c8f800a3ab9621f9d382718428d2d82025379` | `5b899bd63cac30e700a26932a3ffe889ecad8769` |
| `all-in-one/sources/decoded-original/0641-IdentXmlPart.xml` | `75c1f81d659331b8b62578f766e2f0336276caaf086201fdc383e61c195d01df` | `341bca78929061ab73560dd85fef3f4000127782` |
| `all-in-one/sources/decoded-original/0642-IdentXmlPart.xml` | `c922483c261c8ddb98c239a7b4dc3d7f73f9a45261dd5b4d669f39d6918a1c21` | `398f73b99c4a792a68387485fcb47048d166b2a1` |
| `all-in-one/sources/decoded-original/0643-IdentXmlPart.xml` | `ce7ff35daa71ee1728f4e7b5ac3234d0a31a3c71e953021e9c1f9a953783b6cb` | `84b3cfa219e1e1650664f02a67403b8b0e52654e` |
| `all-in-one/sources/decoded-original/0644-IdentXmlPart.xml` | `02ab863d23ad70420950737d07cf960a2c27bca1c7c011d18930f5bd2045e272` | `1b693ba6815fd9533c22684d0acd9d48becf069f` |
| `all-in-one/sources/decoded-original/0645-IdentXmlPart.xml` | `bd0d052cc926d4a9a66ffe9d12de4e5f064231d10a86bd0d3c6e97fd82c4e1d3` | `7280de0c33d0756d250fdb80f15435ecd876b4d1` |
| `all-in-one/sources/decoded-original/0646-IdentXmlPart.xml` | `46f5a677301ad9b0d20a2d9543a2042081ed6db8f0a8fd8d84f25c342c67a8b0` | `db0b2e38d819b6ea29ac980d84b410e864821c26` |
| `all-in-one/sources/decoded-original/0647-IdentXmlPart.xml` | `ffa253c00b62ccdd999f272d95f613caae3a68792ee5ea9d208253dad53e64be` | `d2cf63bd5fe432b0085690496566c9dbcc989352` |
| `all-in-one/sources/decoded-original/0648-IdentXmlPart.xml` | `afaa47ae737d9333fe831ffac2b1d1388f108bb6a2b23d03554fa862f7edb454` | `3dd5101419fbe16bbce7814398209efd6508db82` |
| `all-in-one/sources/decoded-original/0649-IdentXmlPart.xml` | `38f59e654ecfbc2066fa1f8beeb9ced952adc405f8a4fcf3ef233e9d5d026576` | `039bf2e14a610674a8c01d807805d2db9b4a4956` |
| `all-in-one/sources/decoded-original/0650-IdentXmlPart.xml` | `86f53657eb7afb0798da0e215ba226721076c2ab1b25b74eb83e7b3c4b2d8a2d` | `a3d80a76ef5b0d00009c0fc9a1fdeb1471d0b67b` |
| `all-in-one/sources/decoded-original/0651-IdentXmlPart.xml` | `549c09fb14ce6e9734a2ba604c78868647451f24d224ead0d17d209f66428111` | `08d5828b2ed490605da88f6fbb695db5427b6972` |
| `all-in-one/sources/decoded-original/0652-IdentXmlPart.xml` | `251bb1b3ce1bdf3686545062e5803152779de8a4961539d30e6951a2a10ab692` | `eee49f8301a6791748de9ab368159af8e8bc1585` |
| `all-in-one/sources/decoded-original/0653-IdentXmlPart.xml` | `2df91e2095f16613332cfc59d4c51f8a587183e5e75295a119431b61805c92a6` | `4f93c87d6f199d9f8ad16db16fd4df2192ee6d19` |
| `all-in-one/sources/decoded-original/0654-IdentXmlPart.xml` | `b36294f3aad24be72a052bef61c875ca4695d7e101c385cf55bdadec41d5097e` | `118bc3d5610beabdb92a541e19bf4de3ec148b41` |
| `all-in-one/sources/decoded-original/0655-IdentXmlPart.xml` | `38e9f323024fba19582b473f39b1ed03ffe6a0b390218894029a6edb0b1ff9fb` | `83b60b9de4541a3ffa6ee0db98205a372b525665` |
| `all-in-one/sources/decoded-original/0656-IdentXmlPart.xml` | `0dbc45e84732a8848f17b094ea08ab8578dbf240bfe15cd7086859395c27c592` | `9bfb9842e55901bab9a71d1ac03158467dfbb1bc` |
| `all-in-one/sources/decoded-original/0657-IdentXmlPart.xml` | `0f70cda60a6b1a17175876d58e25b2686952642de6cffb21213aeef8b347a22b` | `e625f3d8999c7be7d88c50eab0d93107117b58ec` |
| `all-in-one/sources/decoded-original/0658-IdentXmlPart.xml` | `998294c0c8a99e00ceb33c2c60def2cd4850e34328917ae506244c2be2df3831` | `de9a12a6be87466ef1bf05df71c54580c556a827` |
| `all-in-one/sources/decoded-original/0659-IdentXmlPart.xml` | `ec881805a45730533bccd780e152afb9c9d7c7c45ba7587538b92239f9cbd9d2` | `44d88b18c6b3e5cd5765463ab433ac2ba01d317a` |
| `all-in-one/sources/decoded-original/0660-IdentXmlPart.xml` | `0bf4f4c46531f55324602f4f7b1a1e0b9e63df2c6278126f6e5cf1bc9a06509f` | `915de9b3f968310c45682bef86a91adc1fa06e75` |
| `all-in-one/sources/decoded-original/0661-IdentXmlPart.xml` | `90672199fee355011f581d3287046894772f3f3b4cb78bbe0dd0d71bd488ac93` | `cea3653088f8fb5c77afcf715988039cb63e28ac` |
| `all-in-one/sources/decoded-original/0662-IdentXmlPart.xml` | `1838040bfee800fdb3f13b126eaf69a9d178b17cecc0d59ae03e9185216a48a5` | `ba624f3460dc05e8ade4956cdfc2ec621edb4f73` |
| `all-in-one/sources/decoded-original/0663-IdentXmlPart.xml` | `d3980b88d3cd3e49854439d0778c58ed131bae46a6bc3e65ab70e81f766ac03d` | `3051de9b670457991223a08c03f785747e687414` |
| `all-in-one/sources/decoded-original/0664-IdentXmlPart.xml` | `68c614e1c6a7fcadeee3f0b2ddc54910c3b337e66074d7a113b9cbc834c271ed` | `7ce2f1315d5a21d6b77869a59fc9fcb2f17e90e6` |
| `all-in-one/sources/decoded-original/0665-IdentXmlPart.xml` | `50e88d5f50f555151b35cfb17225e766c34ef6b490bd3a48e0a4e335fd17e3dd` | `ea4a8a5013081f648722c5ebbde3bb1366787990` |
| `all-in-one/sources/decoded-original/0666-IdentXmlPart.xml` | `19a9ccb83ad7070d23726250870d0ca0c33d797ab9ffe679c9d2c0d109cc95e6` | `b6130b32498b6fee0d9e4db7a04dc79f785e1fbb` |
| `all-in-one/sources/decoded-original/0667-IdentXmlPart.xml` | `ef924ced3e0e2b17e9c8440eb4946cd50d55df644c6ec24a1c4fd288fa6b73a3` | `7f2e1798eb9f260d19d038a83369484d0f438856` |
| `all-in-one/sources/decoded-original/0668-IdentXmlPart.xml` | `2248e994a0a02cd37c5c5edaca199b3421068feea91e2e8616560e814ef9f6ed` | `fe0f30d1eaae37783b0f03cb090353b3a3de3600` |
| `all-in-one/sources/decoded-original/0669-IdentXmlPart.xml` | `754c513339d00918717010047b8f9d865d8674c6978a6f86c6f1fa5d683506e2` | `f5bf8f3c41d2a07ba9dcfd8f400548be8cf51cd3` |
| `all-in-one/sources/decoded-original/0670-IdentXmlPart.xml` | `e56f3f0c4f2a86dd18578dedd4453915c2a51cd25e2cd9feced8538171a00841` | `b9466007b14e5c4f5d353dca5734401317e2dc03` |
| `all-in-one/sources/decoded-original/0671-IdentXmlPart.xml` | `26cb51706305c372d512c19770648bb0dbb74df8bd2277b1e0da1b8c88cca293` | `e38a4e2c93ac8093e2b0b8e082a64688b5d9845e` |
| `all-in-one/sources/decoded-original/0672-IdentXmlPart.xml` | `6bfc2ba142d6270c39eb1f13b2886204865af6d46eadc5f410c26981b8da9222` | `2f2790dab4bb2357733112220e0acc41edb6feb6` |
| `all-in-one/sources/decoded-original/0673-IdentXmlPart.xml` | `450ef74e2d2fb65dfbb5f6bad9e28ccacf6bf0caf64327a0e20aff84d6e40f58` | `1957bff7dd1beffcb6e2a40d6a541c1751753548` |
| `all-in-one/sources/decoded-original/0674-IdentXmlPart.xml` | `4770702f519bacda69202bb2f7733d983074bda90964360c238f990d9d08fd84` | `f210593944547b63eab10c667348711413600aab` |
| `all-in-one/sources/decoded-original/0675-IdentXmlPart.xml` | `b1902886927d8403fab736d9c8ffe73f2fbc8ce4b7ca7c345144964668b051c3` | `d82a33b173c8dc0737fd890eb2a63a88a07d0831` |
| `all-in-one/sources/decoded-original/0676-IdentXmlPart.xml` | `c58427c5b0ac6c11cdb52e4c6d0461c7b191fae81ccace191048e9f175fcec59` | `1ed67265f69796a4e659f9438e551068037f33a4` |
| `all-in-one/sources/decoded-original/0677-IdentXmlPart.xml` | `69922fcc5c67d00cdf1c5f712efa3db7638d20c88318d35fe6196467796ab1e3` | `b9437406a7e24f073ef88b8369cacc9ad4ecc5ac` |
| `all-in-one/sources/decoded-original/0678-IdentXmlPart.xml` | `51e637e0b9713c028810f2a717b5c3804a3a26c2f1be7e332a4d6bf277bfc382` | `7fafb2297bcdf739bf1d1dd68cebc0d74f2a40cc` |
| `all-in-one/sources/decoded-original/0679-IdentXmlPart.xml` | `d0fcb93e188c8ae2ae0c0423f0b78b129bf3c168e33a6855262d34b8682b9b56` | `e8d8a014609871082bf5cfca0f9ab9b78136e920` |
| `all-in-one/sources/decoded-original/0680-IdentXmlPart.xml` | `fd551ad5d47bbd66c6bcdcc1949aaddf68cc086a3ddf6fb337adc767954c2b95` | `c9049ced1eaed72c5e251a88601d46ddec8c3e50` |
| `all-in-one/sources/decoded-original/0681-IdentXmlPart.xml` | `318e0cf7cd23caadbd3d72d304358dcf978c4b207c04f58fb5b6ce3f31e344e3` | `371ff45e605de3ab1fefc98583d35ca0235d7ca5` |
| `all-in-one/sources/decoded-original/0682-IdentXmlPart.xml` | `25c7aeb1bfa29c178eaa396db33d4eb6d2d29b9a3f2eb965fa61fae8ce7f1092` | `61182411e912941161eccf4e90c1f174e5379f0a` |
| `all-in-one/sources/decoded-original/0683-IdentXmlPart.xml` | `0c9b569d041cd5babbbeded8a3bdc5d3754927125756b6ac54b7cb991b22fc22` | `662acdb9a06c0ba1c0027e7dd215a28f07d3f02b` |
| `all-in-one/sources/decoded-original/0684-IdentXmlPart.xml` | `6e9b3f173184adcddca503e81e2649022734b6ea3639c1d5ddaf0a08bac00208` | `d67b98b5d5516e0330aae5cfdbee41a3e09206e1` |
| `all-in-one/sources/decoded-original/0685-IdentXmlPart.xml` | `2003d5741a0d707755c5e6e8b737fa106414b87b5b431b97271d9f1a5d343448` | `86bda988d9efedba92ba2f3e4877497d9eb5230a` |
| `all-in-one/sources/decoded-original/0686-IdentXmlPart.xml` | `b450d8ff22f0fffd7a214b2a696af28a03a27834ebf862bfaa822dc9bfb3c8d4` | `8c152d926692a8e15973c980e08e338d29411814` |
| `all-in-one/sources/decoded-original/0687-IdentXmlPart.xml` | `fa50e7e0262c5d51eeca60e914fce4616fa39a05a3466aa14ec93ba375b04cb1` | `5f2b010c4bcc6e752c1952a7a65bf48dcd8e275c` |
| `all-in-one/sources/decoded-original/0688-IdentXmlPart.xml` | `ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda` | `463585759f1ecd94f32362b4fefb000a152f5773` |
| `all-in-one/sources/decoded-original/0689-IdentXmlPart.xml` | `f0cc6f770c2759b92a9a79f4e289dbfa0ca270d90e0e89496f94a13a8d839d51` | `8db940bdbab78ea27ffc280acba9375d2a93f587` |
| `all-in-one/sources/decoded-original/0690-IdentXmlPart.xml` | `fcd6af9e8af48f9737d4764d7765d2eebdf95bd5e0c8e7b4faf6d1ed4eba1541` | `36bd403f48ba8e364126837b19fb0419bbe78941` |
| `all-in-one/sources/decoded-original/0691-IdentXmlPart.xml` | `17cb7d9734d76b39e729e0daf0c89d9bdf74907aab2130c80453fa04e4cea1da` | `d38a1a394f3cf9612e2f344142609e376ef47953` |
| `all-in-one/sources/decoded-original/0692-IdentXmlPart.xml` | `bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037` | `737785d03b5fad43c5b4d451955726d800edb1c0` |
| `all-in-one/sources/decoded-original/0693-IdentXmlPart.xml` | `9315ddf43bdfbd7367ab0735a5bbfffcd81ced257d1907c1e2c08ae6b8bfa7ab` | `6ee2a128582aa9ceac710b82de14e5ec2c96771a` |
| `all-in-one/sources/decoded-original/0694-IdentXmlPart.xml` | `757ccebdf32d0a168dd787bfa735fe6494eac4c4a9f7a5adc63898a88e8b152d` | `c45e8f3ca4129dc06734f6a12ef79e6ed6528a7d` |
| `all-in-one/sources/decoded-original/network-map.json` | `c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60` | `424430b6b953e43138e5d0a18ca40c949e21cfa1` |
| `all-in-one/sources/hmi_plc_tags.csv` | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` | `cf4c0650e7c7baac350dcb89909b808435704880` |
| `all-in-one/sources/live_index.json` | `14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1` | `e35ccea1f841349c632666c29954b7bcd4f5839e` |
| `all-in-one/sources/source-manifest.json` | `5af6e85994536897fd92f75972534a691e6eb0f067aafe07679c0788fd84e5bf` | `38cf407491d52dc6128cf94ca8a4bddee350de6d` |
| `docs/equipment-standard/INVENTORY.json` | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` | `587c3748ad9224718f95ba06463fee913dae231d` |
| `docs/equipment-standard/WORK-ITEM-TEMPLATE.md` | `4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586` | `e546f39535d2b589e80f97db869ac37ce4d05cfd` |
| `docs/equipment-standard/WORK-STANDARD.md` | `05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99` | `f76a570cc73098632e08759b17934000f7e3a253` |

## 최종 인계

- 2026-10-11T10:50:20.250511+00:00 최종 자체검사 및 원본 Git 상태 변경0 재확인. HMI 연결 11행, 원본222파일 fixed blob 내용 일치, 중지5 freeze 일치, 핵심16단언 통과.
- RO01 7영역 문서 초안 완료, 독립검토/제품통합/현재CPU/실물/복구 미완료. 작성 파일은 본 MD와 extracts/RO01뿐. 최초 전달 이후 보강이 필요하면 이 원초안을 보존하고 별도 보강문서로 남긴다.
