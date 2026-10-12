# TC05 온도 계측 — 고유 원본 조사 7영역 초안

## 핵심 확인·상충·공유 근거

- TC05 단독 자체 조사다. TC04와 같은 FN01 베어링 계측군이지만 고유 ID·입력·환산·경보를 별도로 확인했다. `%IW260:P` → `Data.Temp_TC05` DB1.DBW118과 HMI 원시 미러 DB13.DBW26을 구분한다.
- 고유 차이: 0482의 환산 EN은 **NOT 없는 OFF 접점85**다. IN0에는 ON을 전달한다. 이름을 보고 상시 환산이라고 보정하지 않는다. 0529의 MAX_TC05_TEMP Set에는 **ServiceBit M1000.0 접점22**가 추가 직렬이다. TC04 경보와 동일 조건으로 복제하면 안 된다.
- TC05 고온/저범위 경보는 T77/Tag_105의 S5T#1M 후 Set, 별도 RESET_ALLARM 가지로 Reset이다. FN01 공유 예고장 경로의 T130/S5T#1H_30M은 TC05 자체 경보 지연과 다르다.
- OEM FG79/PDF80 79KA2 Phoenix Contact 2864273, X1:205/206/207/208, FG104/PDF105 PEW260/262 경로를 실제 렌더로 확인했다. 두 쪽 각각 Rev2 17.03.2025, 기본 DATA 27.05.2024다.
- 상충: FG79 범위 -30…250°C와 FG104 TC05 설명 -30…350°C; live_index TC05 %IW260 주석은 TC04 -30…250°C, RESERVED TC05 %IW262는 TC05 -30…350°C. 주소·이름·설명을 분리 보존한다.
- 시공 PDF33의 8_23 케이블은 CVV-S 1.0/2, PDF58 같은 번호는 TC/KX 2S/1.0이다. OEM PT100 3선+실드 도식과 함께 설치/변환기/케이블 구간 상충으로 남긴다. 시공58의 8_8 행은 텍스트층에 남지만 실제 페이지에서 검게 가려져 있어 현행 유효 경로로 쓰지 않는다.
- 공유 재사용: TC03/BF01의 0291/0014 공통 선형화 해석은 같은 고정 원본 연결을 재사용하고 TC05 호출·고유 핀·경보·소비를 독립 확인했다. 기존 FN01/BR01의 소유 구분은 유지한다. 다른 설비를 같이 완료로 집계하지 않는다.
- 누락: 현행 CPU/명판/모듈 설정/입력 타입/교정/ON·OFF·ServiceBit 현재값/안전 승인 설정/HMI 화면·이벤트/복구 결과. 모델 런타임 증명도 미확인이다.

## 1. 설비·자료 기준

catalog_id TC05, 별칭 tc_05, sensor/계측, parent 없음, depth0, priority_key 없음, phase2/planned. INVENTORY catalog[16], 장비 대장 equipment index80의 역할은 “FN01 다른 베어링 PT100 온도”다. 같은 이름의 TC04·TC06 등과 동일 실물로 단정하지 않는다. 조사 범위는 TASK3-BATCH08-SCOPE.json 및 GME-CATALOG-OVERLAP-REVIEW.json의 TC05; 로컬 2차133 통합 제외를 유지한다.

고정 입력은 `gme-research/source-mv06`, Git `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, VERSION 1.12.0이다. 사용자 최신 게시 진술과 이 고정 원본 검토를 구분한다. 현재 CPU/게시 기능을 검증했다고 주장하지 않는다. AGENTS·배치지시·스킬/source-map·WORK-STANDARD·WORK-ITEM-TEMPLATE·INVENTORY·START-GPT61 및 VERSION/인계/게시/ACTIVE-WORK 최상단을 읽었다. 배치의 최신 5개 병렬 허용 범위를 따른다.

쓰기 범위는 `drafts/TC05-DOTS-DRAFT.md`, `extracts/TC05/`뿐이다. 원본/공통코드/대장/버전/게시/운영기록 변경0, PLC/보호값/현장/SEJIN 변경0. 시뮬레이터 작성·수정·생성·실행·행동시험0. 원본 build/test/generator 실행0. 새 Work/Codex·재위임·사용자 Mac·로컬 TIA 접근 없음.

이하 XML 경로는 `all-in-one/sources/decoded-original/NNNN-FlgNet.xml` 및 `NNNN-IdentXmlPart.xml`, CSV/PDF는 `all-in-one/sources/` 기준이다. document_id와 원래 NID, UID/RID를 구분한다. network-map은 탐색 보조이며 주장은 원본 XML의 선언·실제 핀으로 확인했다.

| 영역 | 적용 상태 | 확보와 경계 |
|---|---|---|
| 설비·자료 기준 | 적용 | 고유 ID/판본 확인, 실물 동일성 미확정 |
| I/O·HMI | 적용/일부 미확보 | 채널·Word 미러·CSV 확인, 실제 화면 이벤트 미확보 |
| 제어 | 적용 | OFF EN/ON IN0·환산·소유 확인, CPU 실행 미수행 |
| 전기 끝점 | 적용/일부 미확보 | OEM/시공 실제4쪽, 현재 배선·기기 미확정 |
| 알람·복구 | 적용/복구 미확보 | 비교·타이머·S/R·소비 확인, 복구 미수행 |
| 증상 관찰 | 적용 | 읽기 전용 비교 지침, 조작/운전시험 없음 |
| 완료·누락 | 적용 | 문서·자체검사·통합·현장 상태 분리 |

## 2. I/O·HMI

### 2.1 선언·주소·쓰기

SSD.AO/AOS.BO는 bit offset이다. BAD.BIRID의 DB 소유는 DepDBBlock.TOD와 대조했다: 0674 RID8→Coeff DB4, RID11→Data DB1, RID354→Allarm DB3;0628 RID4→Inputs DB13;0682 RID3/10/15→DB1/DB3/DB2.

| 신호 | 형식·주소 | 원본 선언/결속 |
|---|---|---|
| TC05 환산 입력 | Global Int IW260:P | 0678 RID457 AO2080 SAD Input SAM=Peripherie;NID2 UID74→0482 W81 66.Analog_input |
| TC05 HMI 미러 입력 | Global Int IW260 | 0627 RID158 AO2080 SAM=None;NID2 UID28→0398 Move27.in W31 |
| Inputs.TC_05 | Global Word DB13.DBW26 | 0629 RID159 AO208;NID2 UID29 Write;0398 W32 Move27.out1 |
| Coeff.ZERO_TC05/COEFF_TC05 | Global Int DB4.DBW112/114 | 0676 RID16/15 AO896/912;NID2 UID76/75→0482 W83/W82 Zero/Coeff |
| Data.Temp_TC05 | Global Int DB1.DBW118 | 0676 RID17 AO944;NID2 UID77 Write,0482 W84;0684 RID49 NID3 UID500/502/504 Read |
| Allarm.TC05_OFR | Global Bool DB3.DBX20.3 | 0676 RID357 AO163;NID2 UID23 Write;0482 W24 Out_of_range |
| Data.TC04_TC05_MAX_ALL | Global Int DB1.DBW84 | 0684 RID44 AO672;NID3 UID491/501 Read;공유 임계명, 현행값 미확정 |
| MAX_TC05_TEMP | Global Bool DB3.DBX9.3 | 0684 RID51 AO75;NID3 UID509/514 Write(S/R),513 Read;0604 RID106 NID21 UID664 및0585 RID37 NID5 UID241 소비 |
| Tag_105 | Global Timer T77 | 0686 RID50 SAD Timer AO77;NID3 UID507 Write/508 Read;HMI 태그가 아님 |
| ServiceBit | Global Bool M1000.0 | 0686 RID161 AO8000 Memory;NID3 UID28,0529 Contact22. 현재값/쓰기 소유 미확정 |
| Stop_Fan_FN01 | Local Bool BO2 | 0605 RID114, NID21 UID673 Write/NID22 UID694 Read. 물리 출력/TC05 전용 DB가 아님 |
| Tag_122 | Global Timer T130 | 0602 RID113 AO130;NID21 UID671 Write/672 Read;FN01 공유 타이머 |

### 2.2 HMI 원시값과 환산값 분리

`hmi_plc_tags.csv` 행738: `I_TC_05,"DB13,INT26",PLC,0005B`다. 이는 dde.cfg 기반 주소 설정이지 온라인 값이 아니다. 0398/NID2/document1071의 TC05 Move27은 선행 Move22.eno→W33→27.en, 원시 UID28→W31→27.in, W32→Inputs.TC_05 UID29로 간다. 후행 W40은 다음 Move34.en이다. 따라서 이 CSV 태그를 DB1.DBW118 환산 온도로 설명하거나 PLC Word 미러를 별도 측정 채널로 세지 않는다. HMI 표시 단위·스케일·알람 텍스트·팝업·Ack/Reset 이벤트와 실제 통신은 미확보다.

## 3. 제어 구조

### 3.1 고유 호출 조건

0482/document1732/NID2 `analog input conversion`: Powerrail W87→Contact85.in, OFF UID72/RID34→W79 operand, Contact85.out→W86 CRef66.en. Contact85에 Negated가 없다. ON UID73/RID1→W80 CRef66.IN0. `0678` ON은 M0.0, OFF는 M0.1로 선언된다. OFF라는 이름을 NOT ON이나 무조건 FALSE로 바꾸지 않는다.

CRef66 RefId351은 0680 BlockInterfaceInfo, nested CodeBlock78 RefId5는 0672 `Signal linearization` FC63, NID2 UID78 Call로 결속된다. IN0 Bool, Analog_input/Coeff/Zero Int, OutValue Int, Out_of_range Bool. UID74/75/76/77/23과 W81/82/83/84/24의 입력·출력 핀이 TC05 고유 결속이다.

보충 live_index `_7ev/401`의 startup STL은 `set s "on" clr s "off"`다. 현재 OFF=false가 확정된다는 뜻이 아니며 CLR 뒤 S를 R로 바꾸지 않는다. doc401을 0401-FlgNet과 혼동하지 않는다. TC05 환산의 OFF EN이 비활성일 가능성과 실제 호출/리텐션/현재값 확인 과제를 분리한다. ServiceBit의 Write는 이번 IdentXmlPart 탐색에서 직접 확인되지 않아 외부/다른 쓰기 경로를 단정하지 않는다.

### 3.2 공통 선형화와 결과 해석

TC03 초안의 같은 고정원본 0291/0014 연결을 재사용하며 실제 XML 주요 핀을 재확인했다. 0291 Contact255 IN0→W256, Gt258/Le161은 `raw > -1382 AND raw <= 32767`. Convert164/167/174 → Add170 → Mul177 → Div181 → Move185가 ENO 연쇄 W227/230/234/237/241/245를 따른다. DInt 계산 `(DInt(raw)+DInt(Zero))*DInt(Coeff)/28000`를 Int OutValue에 전달한다. Real 온도 계산이나 명판 선형성 보증이 아니다.

범위 이탈 `raw>32767 OR raw<=-1382`는 Gt190/Le259→OR47→Move193(-9999)→W253 OutValue; Move193.eno W21→Coil23→Out_of_range W22이다. OFR를 단순 비교 출력으로 축약하지 않는다. Int에서 상한초과 가지가 존재한다는 정적 사실과 실제 도달성은 별개다. 0014 NOT IN0 Contact171→W172 Move162(0)→W170 OutValue는 별도 쓰기다. EN 비활성, ENO 실패, 정수 오버플로/절삭, 마지막값 유지, scan 순서/재시작은 미검증이다.

live_index Coeff 저장 필드에 TC05 계수 후보가 있어도 현재 승인 교정값으로 채택하지 않는다. FG79/104 범위 상충 때문에 -30°C~250/350°C 중 하나를 임의 선정하거나 ZERO/COEFF/모듈 범위를 변경하지 않는다.

### 3.3 관련 소비와 소유

- 0252/document1950/NID21: MAX_TC05_TEMP UID664→W676 Contact695→W25 OR707.in2. 다른 가지는 MAX_TC04_TEMP, ZT01_FN01_Vibration, FN01 Run AND NOT VR-01 RUN, FN01 Run AND NOT VR02 Run이다. OR707.out W683은 Coil653 Prealarms_FN01, SdCoil656, Contact705.in으로 나뉜다. W685의 S5T#1H_30M(0606 RID112 UID670)→656.value, W686 T130/Tag_122→656.operand, W687→705.operand, W27→Coil661 Stop_Fan_FN01. 관련 소유는 FN01이며 TC05 자체 1분 경보와 90분 공유 타이머를 합치지 않는다.
- 0175/document1858/NID5: MAX_TC05_TEMP UID241(0585 RID37)→W259 Contact289, W290 OR219.in4→W267 Contact305(ON)→W306 OR213.in5→W270 RCoil232 Flag.Start_Burner, W272 UID250. BR01 시작 래치 Reset 소비 경계다. 화염/퍼지/외부 연소제어기의 안전순서·최종 밸브 상태를 TC05 고유 제어로 만들지 않는다.
- 센서 자체 모터 Run/Stop·정역 출력은 비해당이다. 관련 팬/버너 제어가 있다는 이유로 그 설비를 조사완료로 세지 않는다.

## 4. 전기 전달 경로와 실제 PDF

### 4.1 OEM FG79 = PDF80

`Electrical_Rev2.pdf`, 제목 PROBE PT100. 실제 렌더 `extracts/TC05/render/FG79.png`: footer FG79/TOT262, DATA27.05.2024, REV2/17.03.2025 확인. TC05는 우측 PROBE FAN FN-01 SUPPORT BEARINGS다. 좌측 TC04를 TC05 끝점에 합치지 않았다.

- TC05 세 센서선은 X1:205→79.4→79KA2:1, X1:206→79.5→79KA2:3, X1:207→79.6→79KA2:4. 실드 X1:208→79SCH3→접지 표기다. 현장 3선 결선/선색/RTD 정확도 등급은 확인하지 않았다.
- 79KA2는 도면 Phoenix Contact 2864273. 7+는 +24Vdc 10.7 (78/9→82/0), 8-는 도면 `0Vac 9.9` (74/9→80/0)다. 도면의 0Vac 표기를 DC로 임의 정정하지 않는다. 이는 아날로그 변환기 도식이며 릴레이 접점 5/9 규칙을 끌어오지 않는다.
- OUT U,I의 5+→+PEW260/104/5, GND1의 6-→-PEW260/104/5, 출력 실드79SCH4→104/4. 센서와 변환기 출력, 공급전원을 각각 분리한다. FG79 범위 -30…250°C.

### 4.2 OEM FG104 = PDF105

실제 렌더 FG104.png: ANALOG INPUT MODULE, FG104/TOT262, DATA27.05.2024, REV2/17.03.2025. 79/7의 +PEW260은 단자10/I2+ 및 분기14/I3+로, -PEW260은12/U2-/I2- 및16/U3-/I3-로 연결된다. 18 MANA는 상단 -0Vdc10.6(103/3→105/0). 79SCH4는 출력 실드 표기다. PEW260/PEW262 두 칸 모두 TC05 -30…350°C,4–20mA,CPU515/MOD2라고 쓰여 있다.

이 도면은 +/− 신호의 두 입력칸 연결을 보여주며 독립 센서 두 대의 증거가 아니다. 백업의 `%IW260` TC05와 `%IW262` reserved tc05를 구분한다. CPU515/MOD2 표기는 도면 식별이고 현행 CPU/모듈 형식·입력설정 확인은 아니다. FG79의 250°C, FG104의350°C 및 `%IW260` 주석의 TC04 명칭 혼재를 해소하지 않는다.

### 4.3 시공 PDF33·58의 고유 TC05 구간

`Electrical_Can_Decoating_20241118.pdf` 실제 렌더 두 쪽은 각각 CANDC-CONS-E016-033 (D-PAGE16,TOTAL33/64)와 CANDC-CONS-C008-058(D-PAGE8,TOTAL58/64). 둘 다 Rev1 `24.11.11 first draft design`, CHECKED/APPROVED 공란이다. 승인 준공도로 취급하지 않는다.

- PDF33 FLOW_B ZONE03 행17: Pipe16, Pull Box01 TC-05, LOC FN-01/TAG TC-05, 케이블 `8_23=FLB+FN01-TC05A`, CVV-S,1.0,2core.
- PDF58 행8_23: FROM CR→TO FN-01/TC-05, CurrentType TC,SPEC KX,CORE2S,SIZE1.0,SPARE0, ROUTE100→120RBD1→E1700,Adjustment18,LEN69. 단위 미표기 길이를 임의 m로 확정하지 않는다.
- 같은 번호의 CVV-S 대 KX 차이와 OEM PT100 3선+실드 대비2core 표기를 충돌로 남긴다. KX를 근거로 TC05를 열전대로 재분류하거나 접속구간을 발명하지 않는다. 현행 케이블명판/단자양끝/변환기명판/승인도면 필요.
- PDF58 텍스트층 8_8 `=FLB+FN01-FLO4TB3B`,TC05는 실제 렌더에서 검게 가려진 행이다. 별도 현재경로·삭제확정·배선완료로 사용하지 않는다.

## 5. 알람·복구

### 5.1 TC05 온도경보 고유 회로

0529/document1981/NID3. ON UID489→W515 Contact557→W558 비교기 pre. TC05는 Gt459(Temp_TC05 UID500 > shared MAX UID501), Gt462(UID502 >120 UID503), Lt465(UID504 < -60 UID505). W534/537/540→OR458.in1/2/3. 0683 상수 RID45/21의 Int120/-60, RID46의 S5Time `S5T#1M`을 실제 선언으로 구분한다.

OR458.out W541→SdCoil471.in 및 Contact561.in. W542 UID506→471.value;W543 UID507(Tag_105 T77)→471.operand;W544 UID508→561.operand. 이어 W25→Contact22.in, W27 UID28 ServiceBit M1000.0→22.operand, W26→SCoil476.in, W546 UID509→MAX_TC05_TEMP Set다. Contact22에 NOT이 없으므로 ServiceBit이 추가 참이어야 Set 경로가 통과한다. 이것은 TC04와 고유 차이다. 1분은 원본 S5Time 지연이며 현재 안전 승인 지연 또는 변경 지시가 아니다.

Reset은 같은 ON 전원 뒤 W548 RESET_ALLARM UID510→Contact563, W564→Contact567, W552 MAX_TC05_TEMP UID513→567.operand, W568→RCoil488, W554 UID514 MAX_TC05_TEMP다. 자동 온도 회복 히스테리시스가 있는 것처럼 만들지 않는다. 이 네트워크에서 Set과 Reset 두 쓰기가 있으며 실제 동시 조건·전체 호출순서·재발생·리텐션은 CPU 미검증이다. Reset 소거가 센서/배선/팬/버너의 현장 복구를 증명하지 않는다.

### 5.2 OFR·FN01·BR01 영향 경계

TC05_OFR DB3.DBX20.3은 선형화 CRef66.Out_of_range 출력이다. MAX_TC05_TEMP DB3.DBX9.3의 S/R과 같은 알람이 아니다. -9999 값이 유효 환산 경로로 기록되는 경우 낮은 범위 비교(<-60)와 연결 가능성이 있으나 OFF EN과 ServiceBit·타이머·현재값을 모두 관찰해야 한다. 이름만으로 단선 또는 과열 확정을 하지 않는다.

MAX_TC05_TEMP는 FN01 Prealarms 및 90분 타이머/Stop_Fan_FN01, BR01 Start_Burner Reset에 소비된다(3.3의 핀). 실제 정지/재기동 가능 조건, 외부 안전제어기 내부, 운전자 Ack와 Reset의 차이·재요청 이벤트는 미확보다. 보호값 변경, ServiceBit 토글, 강제입력, 시험운전 지시는 하지 않는다.

## 6. 증상별 관찰·수리 기록 지침

아래는 읽기 전용 조사·관찰의 비교표다. 실제 수리/현장시험을 수행한 결과가 아니다. 관찰 기록에는 관찰자·시각/시간대·위치·태그/주소·원시값/단위·프로젝트 식별·비교근거·원인배제·승인 조치·복구증거를 각각 둔다.

| 증상 | 확인할 읽기 전용 관찰 | 비교/경계 |
|---|---|---|
| HMI와 PLC 온도 불일치 | IW260:P/IW260,DB13W26,DB1W118,HMI I_TC_05 주소·표시·갱신시각 | 미러 원시와 환산값,Peripherie와 이미지 접근,통신/스케일 구분 |
| 환산값 정체 | OFF/ON 및 FC63 호출,raw/Zero/Coeff/OutValue,마지막 갱신시각 | OFF EN을 ON으로 임의 수정하지 않음. 리텐션/실행순서 미확정 |
| TC04는 경보·TC05는 무경보 | Temp/공유MAX,120/-60 비교,T77 경과,ServiceBit,Set/Reset 상태 | ServiceBit 추가 직렬 및고유 채널을 먼저 비교. 비트강제/보호임계 변경 금지 |
| -9999/OFR 또는 큰 오차 | raw·OFR·EN/IN0·계수,79KA2 전원/출력/기기식별의 승인 수집자료 | 단선/모듈/범위 불일치 후보를 구분. 접지·활선 측정은 여기서 실행하지 않음 |
| 온도경보 후 팬/버너 영향 | DB3X9.3,Prealarms_FN01,T130,Stop_Fan_FN01,Start_Burner 및외부상태의 동시각 | 1분경보와90분팬 타이머,버너 래치Reset 소유를 분리 |
| Reset 후 다시 발생 | RESET_ALLARM/TC05 S·R가지/원인 지속/ServiceBit·T77 타임라인 | 표시소거와 원인제거/운전복구·재기동을 구분 |

0과 빈값, 미지 필드와 과거기록, note/repair_observation/다른 설비/초안/저장키를 보존한다. generated_with/saved_with가 관찰 당시 CPU를 증명하지 않는다. 실제 운영기록·사진·SEJIN 자료를 복제하거나 공개하지 않는다.

## 7. 완료·누락·검증 상태

문서 근거는 complete_with_gaps 초안이다. 고유 의미검토는 0482 전체 호출,0529 TC05 비교/타이머/Set/Reset 및TC04 차이,0398 TC05 미러,0252 FN01 소비,0175 BR01 소비;공통0291/0014는 기존해석 연결+핵심 재대조다. 해시파일 수는 의미검토 수가 아니다. 추출 스크립트는 XML 파싱/문서근거만 수행했고 원본 프로그램 생성·실행은 하지 않았다.

| 상태 | 결과 |
|---|---|
| documentation | complete_with_gaps,TC05 자체초안 |
| static_review | 자체 XML assertion/해시/4쪽실제PDF 확인;부모 독립검토 대기 |
| ui_records | not_run;나란히보기/백업선택복원/전후비교/보고서 네기능의 제품통합·저장/재열기 미수행 |
| publication | not_published;버전·배포 변경 없음 |
| tia_compile | not_performed;추가TIA 접근권한 없음 |
| live_cpu | not_performed |
| field_recovery | not_performed |

다음은 부모가 초안 원본 결속·고유 조건·충돌을 독립 검토하는 것이다. 현장 누락은 승인 준공도/TC05·79KA2 명판/단자와실제 AI 모듈 범위/온도교정 성적서/현재 프로젝트 비교/ServiceBit 소유/운전자 이벤트의 새 자료가 있어야 해소된다. 새 자료 없이 동일 실물 보류 조사를 반복하지 않는다. TC04/FN01/BR01/하위 부품을 함께 완료로 계수하지 않는다.

### 실제 작업 단계 시각 (UTC)

- 2026-10-11T11:14:39Z — task_and_instructions_read
- 2026-10-11T11:15:23Z — first_xml_extraction_completed
- 2026-10-11T11:16:18Z — four_pdf_renders_visually_reviewed
- 2026-10-11T11:19:46Z — seven_area_draft_written
- 2026-10-11T11:20:53.077035+00:00 — static_assertions_fixed_blob_hashes_verified

### 선정 원본·맥락·중지 자산 해시 전체 목록

선정 55파일 SHA256와 고정 Git blob 내용 모두 일치. 중지5자산 freeze 일치, 원본Git 변경0. 이 수는 전체 의미검토 파일 수가 아니다. 검사 extracts/TC05/static-review.json, 해시 source-hashes.json, PDF pdf-review.json 참조.

| 원본 경로 | SHA256 | 고정 Git blob OID |
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
| `all-in-one/registers/equipment.json` | `7870325dff32bbca90fa34507b301c4aad3347d669fddcd03b910343663996fa` | `acc42633033398216469064932c4b76987371606` |
| `all-in-one/registers/program-model.json` | `6203479c086b15bada12ac9d7e37db9280234ec26f1ea6091d7211dc09a577c5` | `9860b10f008d3a5ae714be50d77b703dfec32f3a` |
| `all-in-one/registers/simulator-freeze.json` | `bb93c1994effc5609939ba566b7802ce7ed55154a7310f02379b308ac2c8c835` | `808ffac14dbd1b4a7d797fa6cd0d647635d90b47` |
| `all-in-one/registers/virtual-plc-test-results.json` | `a6b389f797f9a8b5ffe6928b8420f55c4cc459a327b0b48d716079d2eca6dd64` | `757dd50e45184568facb8ff62900b39d3ce848d1` |
| `all-in-one/sources/Electrical_Can_Decoating_20241118.pdf` | `3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd` | `0ee6b6f8361c5790864dbba4bbd9d55e8e7c08f8` |
| `all-in-one/sources/Electrical_Rev2.pdf` | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` | `f610fd7c7ce14ae951b00cff57b969259bfb389d` |
| `all-in-one/sources/GME_20250506.zap18` | `00c79b6d986e68298f65b172c1807115bc5d9e450a74fcc989d0796d8d8a4ea8` | `211c4f604627a32f82a1124c2a9872c2fcf00865` |
| `all-in-one/sources/PEData.plf` | `647de7ea123daced41c27bec8f81aeb93c712cac714d4754d7da5c528abb016a` | `65605ff8910f920109da731604aa5dc8d83fc956` |
| `all-in-one/sources/decoded-original/0014-FlgNet.xml` | `2e814adbaac6bab99bc668bfdab74f0fc90576324d0b88728951683869cfac30` | `4d164b074fcc13a8f97da9e24382cc169ef29555` |
| `all-in-one/sources/decoded-original/0047-IdentXmlPart.xml` | `2e53bb895dd1ad2a74efaeb1ef16dfd61e62b1b2d7aa34cec8612f1b9cb0928e` | `3dc282f149a21fdf76d5521ef1c833be63b578b4` |
| `all-in-one/sources/decoded-original/0175-FlgNet.xml` | `41279d6aaa157de3be963d010d6ca7dea94811a0ace519c8a3d8baa015f67f97` | `1626da00b3bbcb46f77720271ecf0f50db9dc63b` |
| `all-in-one/sources/decoded-original/0252-FlgNet.xml` | `66b8bf7c1e033f2e6710ab6959e1f5ec2cf27bd6e90c8780eb1bd6daebf76749` | `09de773eef5e5acc23c20f36e07ea6ddeca49c03` |
| `all-in-one/sources/decoded-original/0291-FlgNet.xml` | `fe0b92f074eba25148ce34084649af3d968962558d652727f1eea19f3e3c2550` | `1418fb2ed172c6df694a5eb8bf2dffd0b177653b` |
| `all-in-one/sources/decoded-original/0398-FlgNet.xml` | `4f092b18df4e44af98fd44e173f48dad213a4e80b71f46b0a5e8a700f5b0a747` | `67ebb54daa55093487ea7e780f23ae2cf193c397` |
| `all-in-one/sources/decoded-original/0482-FlgNet.xml` | `48234b3f06f523baa52a62340fa7117556016f7f153bb42f22a022e379b210cf` | `1fa9df6d64924638a054426757154e52fb9efe5b` |
| `all-in-one/sources/decoded-original/0529-FlgNet.xml` | `1309f69deb365b1fd63a45080ee1fb250a8de6c4d753a0d2bdc67f29be1b8815` | `023b04880893284d76f14c2ef66fb81985c3642b` |
| `all-in-one/sources/decoded-original/0582-IdentXmlPart.xml` | `41d4c2bd750392bbc2edc43995ec3a9da47a63c13ee86496df8f187492008951` | `82636dec064876d0f4cc714ef385b07d6e05efe0` |
| `all-in-one/sources/decoded-original/0585-IdentXmlPart.xml` | `e36ec18aa4abebea8f9160254522bb51ff722eae804c5a469790f85f02939184` | `16574d37ef3ca61b59ba396c400e269ab1dd3440` |
| `all-in-one/sources/decoded-original/0602-IdentXmlPart.xml` | `46ab21151eddaaf616469db520730c60423eb742aa491af194e6710c751b4caf` | `bcb12ab1ce8c476ff921baa1608f29d9822f76b4` |
| `all-in-one/sources/decoded-original/0604-IdentXmlPart.xml` | `b798d29c5499b5314a1ee3cff9139dae64c887533b86baa43b6e9a052373a6af` | `bb2c318788b97e7a4924a176275c12d805aa519d` |
| `all-in-one/sources/decoded-original/0605-IdentXmlPart.xml` | `0ff6e2228dbfbc9f657359fe1055083ce621365084ea24c4160e4969b3eaac8b` | `30e199288c147aa22d5ce8407178a391b89c6b1b` |
| `all-in-one/sources/decoded-original/0606-IdentXmlPart.xml` | `73d45f9e2a34bba8a25df1ed1f71e8f6404fc96a8d6481672652a48435b6a740` | `ced032fa747a8544abf17058ee5ebaa78ba9b23b` |
| `all-in-one/sources/decoded-original/0611-IdentXmlPart.xml` | `0d583915a261703954da22c176ba9f81338ad13ea2810e7cd5f7de8aa1bfa089` | `bad6b16fb32a32d47d882f48754994887457872b` |
| `all-in-one/sources/decoded-original/0612-IdentXmlPart.xml` | `95b545d4964d371ebfc107894ea90b8b1d0d7ab5d3a70e643f8ce539063c0f38` | `7cc782d33d07ef225c2104f3e7c9fbd31f7c7467` |
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
