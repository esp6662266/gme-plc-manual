# ZT01 FN01 진동 계측 — 고유 원본 조사 7영역 초안

## 핵심 확인·상충·누락

- ZT01 한 개의 문서 조사다. OEM FG82/PDF83와 FG107/PDF108에서 SPARE 표시를 직접 확인했다. 시공 PDF33/58에는 별도 ZT01 배선 후보가 남아 있어 실제 설치·사용 여부는 보류한다.
- 환산 0494의 호출 EN은 `OFF` M0.1, 함수 입력 IN0는 `ON` M0.0이다. 둘을 같은 조건으로 바꾸지 않는다. 고유 경보 0536도 OFF 접점 아래에 있다. 시험용 원본을 정적으로 읽었을 뿐 어떤 신호 변경이나 행동시험도 하지 않았다.
- Int IW282:P → FC63 Signal linearization → Int DB1.DBW192. HMI 원시 미러는 일반 IW282 → Word DB13.DBW46으로 별도다. CSV의 DB13,INT46은 읽는 형식이며 환산값 주소가 아니다.
- 고유 경보는 `값>400 OR 값<-800`의 S5T#10S 타이머 뒤 Set, `이미 경보 AND 값<380`의 별도 Reset이다. 낮은 값 영역에서 S/R 조건이 겹치므로 안정적인 저범위 고장 래치라고 단정하지 않는다.
- ZT01 경보는 FN01의 다른 예경보와 OR 결합된다. FN01의 S5T#1H_30M 정지 경로는 ZT01 단독 타이머가 아니다. FN01 모터·VR01/VR02·TC04/TC05의 완료를 이 조사에 합산하지 않는다.
- 모델 런타임 증명·현재 CPU·실물·모듈 현행 설정·현장 보호값·복구 결과는 미확인이다. 시뮬레이터/원본 build/test/generator 실행0, PLC/현장/보호값/SEJIN 변경0.

공유 재사용: [BF01](BF01-DOTS-DRAFT.md), [TC04](TC04-DOTS-DRAFT.md), [TC09](TC09-DOTS-DRAFT.md)의 같은 고정 입력 FC63 공통 환산0291/0014, startup0148, 경보 Word0151/0152 및 호출0549 맥락을 연결 재사용한다. 이번에는 ZT01 환산·원시 미러·선언·경보·FN01 소비핀·PDF4쪽을 독립 확인했다. 해시 검사는 의미검토 개수와 별개이며, 신규 자료 없는 현장 보류를 반복 조사로 해결하지 않았다.

## 1. 설비·자료 기준

- catalog_id ZT01, 이름 FN01 진동 계측, kind sensor, group 계측, parent 없음/depth0/priority 없음. INVENTORY catalog[22], 범위 equipment_index97, phase2/planned이며 별도 ID다.
- 배정 근거: `progress/BATCH09-RESEARCH-INSTRUCTIONS.md`, `TASK3-BATCH09-SCOPE.json`, `GME-CATALOG-OVERLAP-REVIEW.json` 해당 행. 신규 자체조사이고 로컬 2차133 통합 제외를 유지한다. 기존 제외90로 SPARE를 임의 편입하지 않는다.
- 원본: `gme-research/source-mv06`, 고정 Git `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, v1.12.0. 최신 게시·현재 CPU·준공 상태와 같은 것으로 취급하지 않는다.
- root AGENTS, 확대 스킬/source-map, WORK-STANDARD, WORK-ITEM-TEMPLATE, INVENTORY, START-GPT61, VERSION/WORKSPACE-HANDOFF/PUBLICATION_STATUS/EXPANSION-WORK/ACTIVE-WORK의 시작 지시를 읽었다. 현재 배치 지시에 따라 원본 실행·편집 없이 자체 XML 파싱/해시/PDF 렌더만 수행했다.
- 쓰기 범위는 `drafts/ZT01-DOTS-DRAFT.md`, `extracts/ZT01/`뿐이다. 원본·공통 코드·타 설비 초안·버전·공개 대장·배포·운영 기록 변경0, 재위임/새 Work/Codex 생성0. TIA 추가 접근권한 없음.
- 이하 4자리 파일번호는 `all-in-one/sources/decoded-original/` 아래 파일을 뜻한다. LAD document_id, 원본 NID, RefId/RID, UID를 서로 구분한다. 같은 UID가 다른 블록에 존재하므로 UID만으로 연결하지 않는다.

| 영역 | 적용 상태 | 확보 및 경계 |
|---|---|---|
| 설비·자료 기준 | 적용 | 별도 ID·SPARE/시공 상충·고정판본; 실물 보류 |
| I/O·HMI | 적용/부분 미확보 | IW/PIW·Word/Int·환산/계수·HMI6행; 실제 화면/쓰기 미확인 |
| 제어 | 적용 | EN/IN0 구분·FC63·FN01 소비/정지 경로; 실행 미수행 |
| 전기 끝점 | 적용/부분 미확보 | OEM2쪽/시공2쪽 실제 렌더; 준공·심선 대응 미확인 |
| 알람·복구 | 적용/복구 미확보 | OFF·10초 S/R·Word 초기화·공통90분; 현장 복구 없음 |
| 증상 관찰 | 적용 | 읽기 전용 관찰계획; 수리나 운전시험 지시 아님 |
| 완료·누락 | 적용 | 문서/제품통합/UI/게시/TIA/CPU/현장 분리 |

## 2. I/O·HMI·백업 저장값

### 2.1 원본 선언 결속

SSD.AO와 AOS.BO는 bit offset이다. Int/Word는 AO÷8로 byte 주소를 산출하며 Timer AO는 타이머 번호다. Global과 Local을 구분한다. BAD BIRID는 해당 DepDBBlock의 TOD와 결속했다: 0674 Coeff RID8→DB4, Data RID11→DB1, Allarm RID354→DB3; 0628 Inputs RID4→DB13; 0682 Data RID3→DB1/Allarm RID10→DB3; 0603 Allarm RID5→DB3/Flag RID2→DB2/Inputs RID218→DB13.

| 신호 | 형식·백업 주소 | 선언 NID/RID/UID·용도 |
|---|---|---|
| ZT01 일반 입력 | Global Int IW282 | 0627 RID76, AO2256, SAD Input SAM=None, NID2 UID82 읽기 |
| ZT01 환산 입력 | Global Int IW282:P | 0678 RID91 AO2256, SAD Input SAM=Peripherie, NID14 UID424 읽기 |
| Inputs.ZT_01 | Global Word DB13.DBW46 | 0629 RID78 AO368, NID2 UID83 Write;0398 Move75 출력 |
| Coeff.ZERO_ZT01 | Global Int DB4.DBW32 | 0676 RID93 AO256, NID14 UID426 읽기 |
| Coeff.COEFF_ZT01 | Global Int DB4.DBW34 | 0676 RID92 AO272, NID14 UID425 읽기 |
| Data.ZT_01 | Global Int DB1.DBW192 | 0676 RID94 AO1536,NID14 UID427 Write;0684 RID89,NID10 UID871/873/880 읽기 |
| Allarm.ZT01_OFR | Global Bool DB3.DBX21.7 | 0676 RID383 AO175,NID14 UID23 Write |
| Allarm.ZT01_FN01_Vibration | Global Bool DB3.DBX9.0 | 0684 RID92 AO72,NID10 UID878 Set/879 Read/882 Reset;0604 RID107,NID21 UID665 읽기 |
| OFF / ON | Global Bool M0.1 / M0.0 | 0678 RID34/1 AO1/0,NID14 UID30/423;0686 OFF RID176,NID10 UID870 |
| Tag_110 | Global Timer T123 | 0686 RID91 AO123,NID10 UID876 Write/877 Read;S5T#10S의 대상 |
| Prealarms_FN01 | Global Bool DB3.DBX17.0 | 0604 RID111 AO136,NID21 UID669 Coil Write |
| Tag_122 | Global Timer T130 | 0602 RID113 AO130,NID21 UID671 Write/672 Read;S5T#1H_30M의 대상 |
| Stop_Fan_FN01 | Local Bool BO2 | 0605 RID114,NID21 UID673 Write/NID22 UID694 Read. DB/Q 주소를 부여하지 않음 |
| Flag.M_FN_01 | Global Bool DB2.DBX1.2 | 0604 RID117 AO10,NID22 UID697 Reset/698 Read |
| Start FN01 | Global Bool Q2.7 | 0602 RID118 AO23 Output,NID22 UID699 Coil Write. 실제 회전 증거 아님 |
| FN01/VR01/VR02 처리 Run | Global Bool DB13.X3.5/X3.4/X3.7 | 0604 RID250/251/252 AO29/28/31,NID21 UID666/667/668 |

### 2.2 HMI 원시 미러와 실제 표시 구분

0398 LAD1071 NID2: ORef82 ZT01→W94 Move75.in; Move75.out1→W95 ORef83 Inputs.ZT_01. Move75는 DisableENO=true 표기가 있고 EN은 선행 Move74.eno→W92→75.en이다. 따라서 단일 무조건 Move로 축약하지 않는다. 이 네트워크는 공통 HMI 입력 전달이며 ZT01 전용 환산 함수가 아니다.

`sources/hmi_plc_tags.csv`를 이름뿐 아니라 주소로 대조한 6개 설정행:

| 태그 | 설정주소 | Access/내부 ID |
|---|---|---|
| I_ZT_01 | DB13,INT46 | PLC / 00053 |
| data_DB1_DBW192 | DB1,INT192 | PLC / 002BE |
| Coeff_DB4_DBW32 | DB4,INT32 | PLC / 001FE |
| Coeff_DB4_DBW34 | DB4,INT34 | PLC / 001E2 |
| Allarmi_73 | DB3,X9.0 | PLC / 00144 |
| Allarmi_133 | DB3,X17.0 | PLC / 00108 |

DB3,X21.7(ZT01_OFR)의 정확한 주소행은 이 CSV에서 확보하지 못했다. 태그가 없다고 전체 HMI 경보 표시가 없다고 단정하지 않는다. CSV는 dde.cfg 설정 추출이며 실제 화면 연결, 공학 단위·소수점, 표시문구, 통신, ACK/쓰기 이벤트와 권한을 증명하지 않는다. Word를 HMI가 INT로 읽는 원문 차이를 유지한다.

### 2.3 저장된 값은 현행 보호값이 아님

`live_index.json` `_7ev/1604`의 이름/형식/값129개, `_7ev/1629`의162개 배열 길이를 검사해 대응했다. ZERO_ZT01=-3900, COEFF_ZT01=282, Data.ZT_01=-9999가 저장돼 있다. 이는 백업 추출 보조근거이며 현재 계수·측정값·교정값/안전값이 아니다. 도면 0/1000Hz를 이 계수와 동일한 공학단위 스케일로 강제 대응하지 않는다.

## 3. 제어 구조·호출·FN01 소유

### 3.1 ZT01 고유 환산 0494

LAD1744, NID14, CRef416 RID351, CodeBlock428 RID5. 0680 BlockInterfaceInfo RID351의 NID14 UID416, 0672 FCBlock RID5의 NID14 UID428→FC63 `Signal linearization`으로 직접 결속했다. 단지 색인의 7/7 해석률로 확인을 대체하지 않았다.

| 연결 | 원본 Part/Wire/핀 |
|---|---|
| 외부 호출 허가 | rail W437→Contact435.in; OFF ORef30 W29→435.operand;435.out W28→CRef416.en |
| 내부 함수 선택 입력 | ON ORef423 W430→416.IN0(Bool) |
| 원시/계수/제로 | ZT01 UID424 W431→Analog_input(Int); COEFF UID425 W432→Coeff(Int); ZERO UID426 W433→Zero(Int) |
| 환산 출력 | CRef416.OutValue(Int) W434→UID427 Data.ZT_01 |
| 범위오류 출력 | CRef416.Out_of_range(Bool) W24→UID23 ZT01_OFR |

OFF와 ON은 이름이 붙은 메모리 Bool이며 컴파일 상수라고 가정하지 않는다. `_7ev/401`의 startup 원문은 `set s "on" clr s "off"`이고 0401-FlgNet HMI 출력 미러와 다른 자료다. 이 텍스트만으로 현재 ON=true/OFF=false를 확정하거나 `CLR S OFF`를 임의로 `R OFF`로 고치지 않는다. 호출조건 false일 때 출력이 반드시 0/정상으로 갱신된다고 하지 않는다. 현재 실행/최종 저장값은 보류한다.

### 3.2 공통 환산 재사용 범위

동일 고정 0291/0014와 BF01/TC09 설명을 연결 재사용한다. IN0 활성 경로의 raw 조건은 `>-1382 AND <=32767`; Int→DInt Convert164/167/174, Add170/Mul177/Div181 ENO 연쇄, `(DInt(raw)+DInt(zero))*DInt(coeff)/28000`, Move185의 Int OutValue로 이어진다. 정수 처리·오버플로·ENO의 현재 CPU 결과는 검증하지 않았다.

범위외 `raw>32767 OR raw<=-1382`의 Move193(-9999)와 Out_of_range Coil23을 구분한다. Move193.eno W21→Coil23.in이므로 OFR를 단순 비교기 출력으로 치환하지 않는다. 0014 NOT IN0 Contact171→W172 Move162(0)→W170 OutValue는 별도 함수 내부 분기다. ZT01은 외부 EN=OFF, 내부 IN0=ON이므로 두 층을 모두 확인해야 한다. 0/-9999는 코드의 대체값이며 현장 안전 대체값이 아니다.

### 3.3 FN01 예경보와 후속 요청 Reset

0252 LAD1950 NID21는 **FN01 공통 예경보 소유**다. ON ORef662 W674→Contact691;691.out W692가 분기를 공급한다.

- TC04 MAX(UID663 W675→Contact693, out W694→OR707.in1), TC05 MAX(UID664 W676→695,out W25→707.in2), ZT01 진동경보(UID665 W677→697,out W698→707.in3)가 병렬이다.
- FN01 Run UID666 W678→Contact699,out W700에서 VR01 Run UID667/Contact701과 VR02 Run UID668/Contact703의 **Negated operand** 두 갈래다.701.out W702→707.in4,703.out W704→707.in5.
- 식의 요약은 ON AND [MAX_TC04 OR MAX_TC05 OR ZT01_alarm OR (FN01_Run AND NOT VR01_Run) OR (FN01_Run AND NOT VR02_Run)]이다. 처리 Run은 실물 상태 증명이 아니다.
- OR707.out W683은 Coil653(operand UID669 W684→Prealarms_FN01), SdCoil656, Contact705.in으로 함께 연결된다. S5T#1H_30M UID670 W685→656.value, T130 UID671 W686→656.operand. T130 UID672 W687→705.operand,705.out W27→Coil661,operand UID673 W689→Local Stop_Fan_FN01.

1시간30분은 FN01 공통 예경보 지속 경로이며 ZT01 고유10초와 다르다. 원본 선언 0606 RID112/NID21 UID670은 S5Time SV=S5T#1H_30M,V13632이다. 진동 보호에 90분이 안전하다고 권고하거나 현행 지연이라고 확정하지 않는다.

0253 LAD1951 NID22: ON Contact716.out W717→Contact720.in,Stop_Fan_FN01 UID694 W705→720.operand,720.out W721→OR676.in4,676.out W709→RCoil685,UID697 W711→Flag.M_FN_01. 다른 OR 가지는 FN_01_FAULT, FN01_INV, SET_PERC_VT01==0, HYDROGEN_BOX_FAULT AND NOT UNDER TESTING이다. 시험조건 NOT은 마지막 수소박스 가지에만 있고 Stop_Fan 분기를 우회하는 공통 조건으로 바꾸지 않는다. 같은 ON 가지에서 Flag.M_FN_01 UID698 W712→Contact726→W727 Coil689→W714 Start FN01 UID699이다. ZT01가 Q2.7을 직접 쓰는 구조가 아니라 FN01의 요청·출력 로직에 영향을 주는 구조다.

0549 공통 main의 ON 조건 병렬 호출 맥락은 기존 동일입력 조사를 재사용한다. 외부 Writer, 전체 OB 스캔순서, 호출 최종 실행·현재 CPU·팬 회전·현장 복구는 미확정이다.

## 4. 전기 전달 경로와 실제 PDF

렌더와 시각확인: OEM `sources/Electrical_Rev2.pdf` PDF83/108, 시공 `sources/Electrical_Can_Decoating_20241118.pdf` PDF33/58. 파일명 Rev2를 각 쪽 개정 증거로 대신하지 않고 footer를 쪽별로 확인했다.

| 실제 PDF / 도면 | footer·개정 | 직접 확인한 끝점 |
|---|---|---|
| OEM83 / FG82 | VIBRATION TRANSMITTER ZT-01; DATA27.05.2024, Rev2 17.03.2025, TOT262 | 점선 SPARE 안 ZT-01, SLD723C, OUTPUT4–20mA, 0/1000Hz. 79/9→+24Vdc10.7→X1:229(5×20 50mA F)→선82.1→ZT01 '+'; ZT01 '−'→X1:230→+PEW282→107/2. shield→X1:231→82SCH1→107/2. 전원은86/0으로 연속 |
| OEM108 / FG107 | ANALOG INPUT MODULE; DATA27.05.2024, Rev2 17.03.2025, TOT262 | SPARE 영역의82/2 +PEW282→PEW282 채널 단자26 I5+;82SCH1 shield. 단자28 U5−/I5−는0Vdc10.6 공통과 연결.25 Uv5/27 U5+는 도면상 해당 신호선 연결 없음. CPU515/MOD3 표기는 도면 표기이며 현행 하드웨어 모델 증명 아님 |
| 시공33 / CANDC-CONS-E016-033 | FLOW B ROUTE CONDUIT PIPING(3), D-PAGE16, TOTAL33/64; Rev1 24.11.11 first draft design | FN-01 ZT-01은18번 Pipe16 루트.8_24=FLB+FN01-ZT01A,CVV-S1.0/4;M22/M29·TC04/05와 별도 행 |
| 시공58 / CANDC-CONS-C008-058 | CABLE SCHEDULE(7),D-PAGE8,TOTAL58/64;Rev1 24.11.11 first draft design | 8_9=FLB+FN01-FLO4TB1C:CR→UC-01/FLO4TB1,description ZT01,TM/CVV-S4S1.0,route100→120RBD1→E200,조정3/LEN54.8_24=FLB+FN01-ZT01A:FN-01/FLO4TB1→FN-01/ZT-01,TM/CVV-S4S1.0,routeE400→120RBD1→E1800,조정15/LEN16 |

OEM FG107 모듈 전원은 +24Vdc10.7→X21:3001(5×20 500mA F)→선107.1→단자41 L+,0Vdc10.6→44 M이다. 센서 X1:229 50mA와 모듈 X21:3001 500mA를 혼동하지 않는다. 도면에 없는 현행 모듈 제조사/모델·실제 측정 모드·소프트웨어 설정은 채우지 않는다.

상충/누락: OEM은 SPARE인데 시공 초안에는 경로가 있다. 시공8_9의 TO LOC는 UC-01,8_24의 FROM LOC는 FN-01로 같은 FLO4TB1 명칭과 함께 적혀 있다. 텍스트를 임의 수정해 같은 실물함으로 단정하지 않는다. OEM X1 번호와 시공 FLO4TB1 심선별 대응, 실제 설치 승인·준공도·현장명판은 미확보다. 시공58의 검은 띠로 가려진8_5/8_7/8_8 행의 추출 텍스트를 활성 배선으로 채택하지 않았다. 관련 있는 인접 TC행은 ZT01 소유로 합치지 않는다.

SLD723C는 해당 도면의 모델 문자열이다. 현행 장치 제조사·모델·진동량(mm/s,g,변위)·감도·주파수 응답·교정성적서가 없으므로 0/1000Hz를 그대로 PLC 값의 단위나 경보400의 단위로 삼지 않는다. 이 입력 루트에는 부하 릴레이 접점이 핵심으로 나타나지 않으므로 다른 설비의5/9 또는 하단접점표1/5/9를 복제하지 않는다.

## 5. 고유 알람·복구와 Word 쓰기

0536 LAD1988 NID10. 모든 Gt/Lt는 SrcType Int이다. 0683 RID74 UID872=400, RID85 UID874=−800(SV부호표기,V64736),RID90 UID875=S5T#10S(V4352),RID93 UID881=380을 선언과 대조했다. unsigned64736을 경계값으로 사용하지 않는다.

| 기능 | 원본 핀·조건 |
|---|---|
| 공통 허가 | rail W910→Contact904.in;OFF UID870 W883→904.operand;904.out W905→Gt848.pre/Lt851.pre/Contact908.in |
| 상한 발생 | 값UID871 W884→Gt848.in1;400 UID872 W885→848.in2;848.out W886→OR847.in1 |
| 하한 발생 | 값UID873 W887→Lt851.in1;−800 UID874 W888→851.in2;851.out W889→OR847.in2 |
| 10초 지연 | OR847.out W890→SdCoil857.in 및 Contact906.in;S5T#10S UID875 W891→857.value;T123 UID876 W892→857.operand |
| 래치 Set | T123 UID877 W893→Contact906.operand;906.out W907→SCoil862.in;경보UID878 W895→862.operand |
| 자동 Reset 가지 | 기존 경보UID879 W897→Contact908.operand;908.out W909→Lt866.pre;값UID880 W898→866.in1,380 UID881 W899→866.in2;866.out W900→RCoil869.in,경보UID882 W902→869.operand |

비교는 strict >400/<−800/<380이고 등호를 추가하지 않는다. Reset 가지에도 OFF가 필요하며, 이 고유망에 RESET_ALLARM 버튼 접점이나 하한 정상복귀 비교는 없다. 특히 값<−800이면 <380도 만족해 Set/Reset 조건이 겹친다. −9999 대체값도 숫자상 이 구간에 든다. 동일 스캔 최종 래치·우선순위·다른 Writer를 실행으로 검증하지 않았으므로 “저범위면10초 후 계속 유지” 또는 “모든 범위 정상 때만 해제”라고 쓰지 않는다. 자동 Reset 조건 충족은 센서정상·팬안전·현장복구 증거가 아니다.

공통 startup0148 LAD403 NID3: ON Contact329→W330 Move267.en,Int0 UID293 W315→267.in,267.out1 W316→UID294.0563 RID32 AO64/BAD23 및0562 TOD3 결속으로 DB3.DBW8←0이며 DBX9.0 진동경보 비트와 겹친다. DB3.DBW16←0는 Move281.out1 W327→UID302,0563 RID40 AO128/NID3으로 Prealarms_FN01 DBX17.0와 겹친다. ZT01_OFR DBX21.7은 이 Word0~16 초기화 범위 밖이다.

공유0151/0152의 DB3.DBW8→WorkData.W4,DB3.DBW16→W18 경보 스냅샷/변화비교는 동일입력 공통근거를 재사용한다.0565 RID21,NID1 UID181/NID2 UID228의 DB3W8 읽기와 RID22 W4의UID182 Write/229 Read, RID33의DB3W16 UID189/236을 대조했다. 이 공통 경보전달이 ZT01 전용 HMI 문구·경적·ACK 완료나 안전 재기동을 증명하지는 않는다. 전체 간접/외부 Writer 부재도 보증하지 않는다.

## 6. 증상별 읽기 전용 관찰 계획

현재 수행한 현장 관찰·수리·조작이 아니다. 신호 주입, 보호값 변경, OFF/ON 강제, 경보해제, 팬 운전시험은 하지 않는다. 위험설비 접근은 별도 승인된 현장 자격·절차가 필요하다.

| 증상 | 같은 시각·같은 프로젝트에서 확보할 기록 | 원인 배제·복구 판단 경계 |
|---|---|---|
| 화면값과 PLC 값 불일치 | IW282와IW282:P,DB13W46,DB1W192,호출EN/IN0,ZERO/COEFF,HMI 주소·단위·갱신시각 | 원시 미러/환산값 혼동,프로세스이미지/주변부 읽기 차이,통신 지연을 구분 |
| 값이 고정/오래됨 | M0.1/M0.0,0494 호출상태,최종쓰기 시각,SPARE/설치 확인 | OFF 조건 미충족을 센서불량으로 확정하지 않음;강제실행 금지 |
| OFR/−9999 | 원시값·범위·EN/IN0·DB3X21.7·DB1W192·전원/단자 승인기록 | 단선·전원·모듈모드·범위외·비호출을 분리;−9999 자체는 단선 확정 아님 |
| 진동경보가 없거나 짧게 변함 | OFF,값,T123,DB3X9.0의동일시간 추이,Word초기화 시점 | <−800와<380 겹침·S/R·Word쓰기를 비교;경보 없음이 안전/정상 증거 아님 |
| FN01 예경보/정지 | ZT01경보,TC04/05경보,FN01/VR01/VR02처리Run,T130,LocalStop,DB2X1.2,Q2.7 | 공통90분원인·ZT01고유10초 분리;Q=1을 회전확인으로 쓰지 않음 |
| 도면상 있는데 실물 불명 | ZT01/FN01명판,현장위치,준공도,배선양끝·FLO4TB1/UC01/FN01표기 | OEM SPARE와 시공초안 상충을 승인자료로 해소;타설비계기 자동대입 금지 |

관찰기록 필수: 관찰자·실제 UTC/현지시간대·설비/단자·계기·값/단위·프로젝트/CPU 식별·원본판본·비교결과·배제근거·승인조치·전후·복구확인자. 실제 사용자 기록·사진·SEJIN 운영자료를 이번 산출물에 복제하지 않았다.

## 7. 완료 기준·누락·검증 경계

| 상태 | 이번 결과 |
|---|---|
| documentation | complete_with_gaps: ZT01 7영역 초안·정적 원본 근거·상충/누락 작성 |
| static_review | 고유 XML/선언·실제 PDF4쪽·선정 해시와 Gitblob 대조 완료. 부모 독립 검토는 별도 |
| ui_records | not_run: PC/모바일·저장·재열기·백업/복원·보고서 기능 시험 미수행 |
| publication | not_published: 통합·버전변경·배포 미수행 |
| tia_compile / live_cpu / field_recovery | 모두 not_performed |

네 기능: 도면/래더 비교에 쓸 고유 근거는 확보했으나 제품 UI 연결·원본 강조를 시험하지 않았다. 백업선택복원·전후비교·관찰보고서/PDF 구현과 실제 저장/재읽기/재열기는 미검증이다. 이 MD와 PDF원본 렌더를 제품 기능 검증으로 바꾸지 않는다. BC01 동등 구현 완료나 설치/수리 완료로 집계하지 않는다.

필요 자료와 판정:
1. 설치 승인/준공도·현장 명판/양끝 배선: OEM SPARE와 시공8_9/8_24,UC01/FN01 FLO4TB1 상충을 해소해야 실물 대응 가능.
2. 승인된 현재 프로젝트/CPU 비교: OFF/ON 실제 Writer·호출·간접쓰기·스캔/리텐션·S/R 최종 경로를 읽기 승인범위에서 확인. 이번 정적 판단으로 실행 승인하지 않음.
3. 제조사 원문·교정성적서·모듈구성: 진동량/단위/스케일·SLD723C 현행 설치·4–20mA 모드·계수−3900/282의 적합성 판단. 현행 보호설정 변경은 별도 범위.
4. 실제 HMI 화면/이벤트·주소·권한 자료: 원시/환산 표시·OFR/진동경보·ACK 경로 확인.
5. 문서 독립검토 후에도 TIA/CPU/실물/복구를 별도 상태로 유지. 새 현장자료 없이 이 보류를 반복 재검색하지 않는다.

## 실제 단계 시각 (UTC)

- 2026-10-11 11:24:27: 배정 수신·범위/공통지시 확인 시작.
- 11:24:30~11:24:58: 기준 지침·대장·고유 네트워크 색인 및 원본 탐색.
- 11:25:03~11:25:51: 고유 XML Part/Wire·선언 독립검토,OEM PDF83/108 렌더·시각확인.
- 11:25:58~11:26:27: 시공 경로/저장값 조사,PDF33/58 렌더·시각확인.
- 11:26:42~11:27:33: FN01 소비·상수·Word쓰기·보존자산·배열길이 대조.
- 이후 작성·자체 정적검사·해시 최종 시각은 아래 검사기록에 기록한다. 시각은 도구 호출/실제 기록이며 추정 투입시간이 아니다.

## 최종 자체 문서검사·선정 원본 해시 전체 목록

검사 시각: 2026-10-11T11:32:15.915665+00:00. 자체 XML 구조·주소·연결/고정 blob/중지5해시 검사 95건 모두 통과. 선정 파일 59개가 고정 Gitblob 내용과 일치했고 원본 Git 변경0이다. 검사 개수는 설비 의미검토 완료수나 원본 전체 파일의 완전해석 수가 아니다. 검사JSON `extracts/ZT01/static-review.json`,해시JSON `extracts/ZT01/source-hashes.json`,검사 소스 `extracts/ZT01/review_static.py`. 원본 프로그램이나 금지 시뮬레이터는 실행하지 않았다.

| 고정 저장소 상대경로 | SHA256 | Git blob (내용일치) |
|---|---|---|
| `.agents/skills/gme-equipment-rollout/SKILL.md` | `fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b` | `9aa820ea6ca15b4e136c9772423b78ed4df6a3d4` |
| `.agents/skills/gme-equipment-rollout/references/source-map.md` | `40612c5efb8f94608840c7bc0e9095ea840df54920861c388ae48ea34c7998dc` | `49e50a7a8e56a16e2ec7f3607a03fd90adb8f1d3` |
| `AGENTS.md` | `0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2` | `073164bc6efd5791032d62c71b03b4dab48cb6f8` |
| `EXPANSION-WORK.md` | `ec624de9fd2fcfac861a67fd5e828b25ef46db50bfd7a37ff16e2cb54cd0f7e2` | `4c42d88ecc2d48269eb23e13a20ebf3721a092a1` |
| `PUBLICATION_STATUS.md` | `efe4857aec598d90470322cf3962eb3fe1f64947630e1fdf71d1c90134de8740` | `d76401cf291fc0be681acc51fa898ad3ce46ff78` |
| `VERSION.json` | `5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7` | `fffb51663b7705aec91cb119ca80ee943a4ce758` |
| `WORKSPACE-HANDOFF.md` | `215096d997782e78e901dfae36c782937e49611fbeb677a0d3fa50cbecf8d074` | `dd0b8989d2376c4415bba9bd826fe6754c6b1a12` |
| `all-in-one/ACTIVE-WORK.md` | `eff3bbc08ecff41da3beff77f3fec48e7d148708192bcaaab00f34b6a721afc2` | `6eb947c629b5ddf9c759ef87649451303938864b` |
| `all-in-one/assets/program-model-data.js` | `52f8199371e3399b7c0d44ab5469f0472aced79d56bbef2887f7625f5d2aff0f` | `38f34b0caa380a16ccad6f6f1e234a2fdf23f327` |
| `all-in-one/assets/simulator-workspace.js` | `3a6dfc618ff7e7b238f2671dc85d65704f33093a18eac879d86081d92c31e8bc` | `97c2c831c77a9699fff0e0960b3bc1b7d93d45b3` |
| `all-in-one/assets/virtual-plc.js` | `5f1876052dc0067b1f010af0dfc941946e37003167481731293615d9c1c36dbc` | `0bd9eceb54365a91214a37c5601b5067c39a3f75` |
| `all-in-one/registers/program-model.json` | `6203479c086b15bada12ac9d7e37db9280234ec26f1ea6091d7211dc09a577c5` | `9860b10f008d3a5ae714be50d77b703dfec32f3a` |
| `all-in-one/registers/simulator-freeze.json` | `bb93c1994effc5609939ba566b7802ce7ed55154a7310f02379b308ac2c8c835` | `808ffac14dbd1b4a7d797fa6cd0d647635d90b47` |
| `all-in-one/registers/virtual-plc-test-results.json` | `a6b389f797f9a8b5ffe6928b8420f55c4cc459a327b0b48d716079d2eca6dd64` | `757dd50e45184568facb8ff62900b39d3ce848d1` |
| `all-in-one/sources/Electrical_Can_Decoating_20241118.pdf` | `3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd` | `0ee6b6f8361c5790864dbba4bbd9d55e8e7c08f8` |
| `all-in-one/sources/Electrical_Rev2.pdf` | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` | `f610fd7c7ce14ae951b00cff57b969259bfb389d` |
| `all-in-one/sources/GME_20250506.zap18` | `00c79b6d986e68298f65b172c1807115bc5d9e450a74fcc989d0796d8d8a4ea8` | `211c4f604627a32f82a1124c2a9872c2fcf00865` |
| `all-in-one/sources/PEData.plf` | `647de7ea123daced41c27bec8f81aeb93c712cac714d4754d7da5c528abb016a` | `65605ff8910f920109da731604aa5dc8d83fc956` |
| `all-in-one/sources/can-decoating-page-text.json` | `d3b4c14945dd00f79c58ebab0cb8991c422dd1670e95e24d10779bd9e9d99bba` | `2bebec2c719fa57ed6c9f8d4e541e8848dc0d732` |
| `all-in-one/sources/decoded-original/0014-FlgNet.xml` | `2e814adbaac6bab99bc668bfdab74f0fc90576324d0b88728951683869cfac30` | `4d164b074fcc13a8f97da9e24382cc169ef29555` |
| `all-in-one/sources/decoded-original/0148-FlgNet.xml` | `1d80e1bbf1c82dcc4dd18628c35935bbd55a17b5be9c1ca7bfb249600d154313` | `3069ae3b5fa16ed10a64c149b6cf5cb5ace423b3` |
| `all-in-one/sources/decoded-original/0151-FlgNet.xml` | `227627d165c6240a4c15b62fd4e4c8d7a621c15f35319cb424601df5cc52c904` | `8e8a9801d1f57180fc3747f6515c0353f38f7dc5` |
| `all-in-one/sources/decoded-original/0152-FlgNet.xml` | `2b6165460f06a52de56afcb4d65ed163d64320e24af1b194e934a4d7c6bfe49f` | `dd8e35b98043d9d0f230351352273eac1d783990` |
| `all-in-one/sources/decoded-original/0252-FlgNet.xml` | `66b8bf7c1e033f2e6710ab6959e1f5ec2cf27bd6e90c8780eb1bd6daebf76749` | `09de773eef5e5acc23c20f36e07ea6ddeca49c03` |
| `all-in-one/sources/decoded-original/0253-FlgNet.xml` | `2d35470eb44fff79916b93fcf57a597b2b9a03211e8493c2283706dc2c875154` | `6d5dc12df96c7fc47ad7f25eba6ba9a55a6755d0` |
| `all-in-one/sources/decoded-original/0291-FlgNet.xml` | `fe0b92f074eba25148ce34084649af3d968962558d652727f1eea19f3e3c2550` | `1418fb2ed172c6df694a5eb8bf2dffd0b177653b` |
| `all-in-one/sources/decoded-original/0398-FlgNet.xml` | `4f092b18df4e44af98fd44e173f48dad213a4e80b71f46b0a5e8a700f5b0a747` | `67ebb54daa55093487ea7e780f23ae2cf193c397` |
| `all-in-one/sources/decoded-original/0494-FlgNet.xml` | `0f680b953bfd9596cac6729058d077421ae87b0c075c9461162b6aacaea0d416` | `526bbd991246dbf6f0374720fefb69addc6fcf2e` |
| `all-in-one/sources/decoded-original/0536-FlgNet.xml` | `454017af81080fc9b14d7fafaffa833ca9e6750252ae99efe3c658963e74c625` | `7bf1879ebade729d7f36fe7b9bd69b8c114b9d47` |
| `all-in-one/sources/decoded-original/0549-FlgNet.xml` | `49f7169c33ed7f54559b0801e21a7d618584900972840e91cf51ad032e8febb1` | `985b5310b43b1015b5dee286aa0e42800564b94b` |
| `all-in-one/sources/decoded-original/0562-IdentXmlPart.xml` | `85aada44dd9a3e66835463c3fed400f1efe121f4f5bc5ab8f0ad49481ec0ea1c` | `1609802542a3e560baba3f2b73c306be281dfb23` |
| `all-in-one/sources/decoded-original/0563-IdentXmlPart.xml` | `86cf35b6baebc079cb5a092baf53ec3364c377ea7318eb263ab69c8b4550b4ad` | `6a10fc694f896cda16409804daf2554c91635654` |
| `all-in-one/sources/decoded-original/0564-IdentXmlPart.xml` | `2aed17fa02d19b0a081023282841aa561d6a2dca3e393284da3622b967af00b1` | `c4b1f2cb191970cfce1cce59cb290a9f1f934c37` |
| `all-in-one/sources/decoded-original/0565-IdentXmlPart.xml` | `0f7f970faa6c456f2bb032b1a2072a2f52db1e03fc77bd8d35d4583deeaf1149` | `c2e3e2d57c94c5da864f6e172f0a7a925da942d6` |
| `all-in-one/sources/decoded-original/0602-IdentXmlPart.xml` | `46ab21151eddaaf616469db520730c60423eb742aa491af194e6710c751b4caf` | `bcb12ab1ce8c476ff921baa1608f29d9822f76b4` |
| `all-in-one/sources/decoded-original/0603-IdentXmlPart.xml` | `e93969dfa281d75b49b24127793068e33472dadb19729c1c48fc4a8dad075ef8` | `3a92b304baf4dbf6147e944d9778d2da11285cb1` |
| `all-in-one/sources/decoded-original/0604-IdentXmlPart.xml` | `b798d29c5499b5314a1ee3cff9139dae64c887533b86baa43b6e9a052373a6af` | `bb2c318788b97e7a4924a176275c12d805aa519d` |
| `all-in-one/sources/decoded-original/0605-IdentXmlPart.xml` | `0ff6e2228dbfbc9f657359fe1055083ce621365084ea24c4160e4969b3eaac8b` | `30e199288c147aa22d5ce8407178a391b89c6b1b` |
| `all-in-one/sources/decoded-original/0606-IdentXmlPart.xml` | `73d45f9e2a34bba8a25df1ed1f71e8f6404fc96a8d6481672652a48435b6a740` | `ced032fa747a8544abf17058ee5ebaa78ba9b23b` |
| `all-in-one/sources/decoded-original/0627-IdentXmlPart.xml` | `08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb` | `61ebc0abbb2ca160e11e1da400a3f14a397d8bc5` |
| `all-in-one/sources/decoded-original/0628-IdentXmlPart.xml` | `9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd` | `170ca5c72599edc7ea7eefe651c3680ce325e76a` |
| `all-in-one/sources/decoded-original/0629-IdentXmlPart.xml` | `67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972` | `058129bb01e27f7a6a0d0293f332d745e5bab74e` |
| `all-in-one/sources/decoded-original/0672-IdentXmlPart.xml` | `6bfc2ba142d6270c39eb1f13b2886204865af6d46eadc5f410c26981b8da9222` | `2f2790dab4bb2357733112220e0acc41edb6feb6` |
| `all-in-one/sources/decoded-original/0674-IdentXmlPart.xml` | `4770702f519bacda69202bb2f7733d983074bda90964360c238f990d9d08fd84` | `f210593944547b63eab10c667348711413600aab` |
| `all-in-one/sources/decoded-original/0676-IdentXmlPart.xml` | `c58427c5b0ac6c11cdb52e4c6d0461c7b191fae81ccace191048e9f175fcec59` | `1ed67265f69796a4e659f9438e551068037f33a4` |
| `all-in-one/sources/decoded-original/0678-IdentXmlPart.xml` | `51e637e0b9713c028810f2a717b5c3804a3a26c2f1be7e332a4d6bf277bfc382` | `7fafb2297bcdf739bf1d1dd68cebc0d74f2a40cc` |
| `all-in-one/sources/decoded-original/0680-IdentXmlPart.xml` | `fd551ad5d47bbd66c6bcdcc1949aaddf68cc086a3ddf6fb337adc767954c2b95` | `c9049ced1eaed72c5e251a88601d46ddec8c3e50` |
| `all-in-one/sources/decoded-original/0682-IdentXmlPart.xml` | `25c7aeb1bfa29c178eaa396db33d4eb6d2d29b9a3f2eb965fa61fae8ce7f1092` | `61182411e912941161eccf4e90c1f174e5379f0a` |
| `all-in-one/sources/decoded-original/0683-IdentXmlPart.xml` | `0c9b569d041cd5babbbeded8a3bdc5d3754927125756b6ac54b7cb991b22fc22` | `662acdb9a06c0ba1c0027e7dd215a28f07d3f02b` |
| `all-in-one/sources/decoded-original/0684-IdentXmlPart.xml` | `6e9b3f173184adcddca503e81e2649022734b6ea3639c1d5ddaf0a08bac00208` | `d67b98b5d5516e0330aae5cfdbee41a3e09206e1` |
| `all-in-one/sources/decoded-original/0686-IdentXmlPart.xml` | `b450d8ff22f0fffd7a214b2a696af28a03a27834ebf862bfaa822dc9bfb3c8d4` | `8c152d926692a8e15973c980e08e338d29411814` |
| `all-in-one/sources/decoded-original/network-map.json` | `c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60` | `424430b6b953e43138e5d0a18ca40c949e21cfa1` |
| `all-in-one/sources/hmi_plc_tags.csv` | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` | `cf4c0650e7c7baac350dcb89909b808435704880` |
| `all-in-one/sources/live_index.json` | `14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1` | `e35ccea1f841349c632666c29954b7bcd4f5839e` |
| `all-in-one/sources/source-manifest.json` | `5af6e85994536897fd92f75972534a691e6eb0f067aafe07679c0788fd84e5bf` | `38cf407491d52dc6128cf94ca8a4bddee350de6d` |
| `docs/equipment-standard/INVENTORY.json` | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` | `587c3748ad9224718f95ba06463fee913dae231d` |
| `docs/equipment-standard/START-GPT61.md` | `35769e3146ccd707fea2b81b67b30376b76a0a19c7e662fe2bb4fdd382306f94` | `0d08cab3678df7e2625251b641b138ef4956483b` |
| `docs/equipment-standard/WORK-ITEM-TEMPLATE.md` | `4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586` | `e546f39535d2b589e80f97db869ac37ce4d05cfd` |
| `docs/equipment-standard/WORK-STANDARD.md` | `05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99` | `f76a570cc73098632e08759b17934000f7e3a253` |
