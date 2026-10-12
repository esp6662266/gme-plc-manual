# ZT02 — MV01 위치 계측 고유 근거 조사 초안

- 대상: catalog_id ZT02 한 개. sensor / 계측 / parent_id MV01 / phase2 / INVENTORY catalog[113]. 부모 MV01의 완료를 상속하지 않는다.
- 고정 원본: `source-mv06`, commit `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, v1.12.0. 현재 CPU·준공 현황·최신 게시판을 검증한 문서가 아니다.
- 조사: 2026-10-11 UTC. 12:49:50 착수, 12:50:19 원본 PDF 추출, 12:50:58 고유 XML 추출, 12:52:23 선정 27원본 해시 확인. 종료·검사 시각은 부록 기록.
- 상태: 문서 `complete_with_gaps`; 지정 원본 정적 확인만 수행. 실행 모델/추론 수준의 런타임 증명 미확인.

## 핵심 확인·상충·누락

1. P&ID 실제 PDF1의 ZT-02는 MV-01/M20·LS23/24 옆에 있고, OEM FG45/실제 PDF46은 **ZT-02 ENCODER**라고 직접 명시한다. FG144/PDF145도 **MV-01 ENCODER ZT-02**, TM1 CH0.A/B를 직접 표기한다. 따라서 이는 이름만 비슷해서 묶은 후보가 아니라 **도면 내부의 명시 대응**이다. 다만 도면과 현재 실물/CPU의 동일성은 별도 미확정이다.
2. 시공 PDF57 두 ZT02 케이블 행은 **AI**로 분류한다. OEM의 A/B 엔코더 도면과 문서 분류가 상충한다. AI 표기를 4–20mA 규격이나 독립 IW 채널로 확대하지 않는다.
3. `0506` NID50 HSC → `fill_unit1.ACT_CNTV0`; `0512` NID31은 원시 I8.2 조건, DInt 합산과 **/100**, Int 저장, 선형화 → `Data.Pot_MV01`을 확인했다. `Pot` 이름은 포텐셔미터 실물 증거가 아니다.
4. HSC 호출은 23개 실인수 중 4핀의 선언 결속만 확보했다. 나머지 **19핀**은 ORef RefId가 없으므로 상태/오류 주소와 하드웨어 설정·완료를 발명하지 않는다.
5. `ResetEncoderProcedure_MV01`은 부모 출력 요청에도 들어가는 절차다. 단순 화면 초기화나 안전한 리셋 버튼으로 설명하지 않는다. 실행/교정은 하지 않았다.
6. 부모의 `MV01_FAULT`, 150ms 응답 타이머, W33/W34 명령 누적은 ZT02 전용 고장 검출로 옮기지 않는다. 위치 처리 OFR과 부모 구동 고장을 구분한다.
7. 공유 근거: `MV01-DOTS-DRAFT.md`를 색인으로 재사용했다. 부모 초안의 고정 커밋은 89570f7이지만 이번 선정 **27개 원본 SHA256 전부가 그 초안의 해시와 같고**, 현재 abcf31c Git blob과도 모두 일치한다. 그 사실은 부모 문서 전부를 재검증했다는 뜻이 아니다. 직접 재검토는 아래 위치 채널·선형화·리셋 영향·4개 PDF 페이지에 한정했다.

## 1. 설비·자료 기준

### 1.1 소유와 식별

`docs/equipment-standard/INVENTORY.json#/catalog/113`: ZT02, P&ID 밸브 위치 계측, 부모 MV01, depth1, planned, baseline, not_assessed. 인접 ZT03~06과 같은 명칭이어도 별도 ID다. 이번에는 ZT02만 작성한다. P&ID/OEM 도면의 위치 계측 대응과 백업의 MV01 엔코더 처리 경로를 연결하되, 온라인 TM 채널·실물 모델·동일성 확인 완료로 승격하지 않는다.

| 원본 | 직접 확인 위치·개정 | 확인 내용·한계 |
|---|---|---|
| `all-in-one/sources/PID_1684n002I.pdf` | 실제 PDF1, 도면1684n002, Apex I; 기본06/04/2011, I개정15/01/2013 `REMOVED MC-05, CHANGED POWER OF FN-02` | HE01 인접 MV-01, M20, LS23/24, ZT-02 배치. ZT02 모델·전기규격·PLC주소는 없음 |
| `all-in-one/sources/Electrical_Rev2.pdf` | FG45 / PDF46, 제목 MOTORIZED VALVE MV-01; 날짜27.05.2024, 개정란 공란 | ZT-02 ENCODER 단자 B/C/D/E와 X1/107~111 |
| 같은 OEM PDF | FG144 / PDF145, TECHNOLOGY MODULE TM1 TIMER; 날짜27.05.2024, 개정란 공란 | MOD16 CPU515 표기, CH0.A/B와 MV-01 ENCODER ZT-02 명시 |
| `all-in-one/sources/Electrical_Can_Decoating_20241118.pdf` | PDF57, CANDC-CONS-C007-057, D-PAGE7, TOTAL-PAGE57/64; Rev1 24.11.11 first draft design | 시공 케이블 설계표 AI 분류. 준공 실측 자료로 취급하지 않음 |

파일명 Rev2는 모든 페이지의 Rev2 개정 증거가 아니다. 위 두 OEM 페이지의 개정란은 각각 실제 렌더로 확인했다. P&ID 정격·공정 설정이나 주변 장치 수치는 ZT02 현행 설정으로 옮기지 않는다.

### 1.2 근거 표기

본문 `NNNN`은 `all-in-one/sources/decoded-original/NNNN-FlgNet.xml` 또는 명시한 `NNNN-IdentXmlPart.xml`이다. LAD(document_id)는 network-map의 탐색 색인, NID/RID/UID와 Part/Wire는 원본 문맥이다. RID·UID 번호만 같다는 이유로 다른 블록에 결속하지 않았다. 원본 XML은 백업 추출물이며 실행한 PLC 프로그램이 아니다.

## 2. I/O·HMI

### 2.1 물리 신호와 선언 구분

ZT02 이름으로 독립 아날로그 IW/PIW를 확보하지 않았다. 물리 신호는 도면상 TM A/B 경로이고, 백업은 MV01 HSC 인스턴스와 처리 DB 경로다. Q2.4/Q2.5는 부모 방향 명령이며 ZT02 입력주소가 아니다. E20.0/1/2는 FG144에서 SPARE로 표시되므로 ZT02 카운트 비트로 채택하지 않는다.

| 신호 | 원본 선언·문맥 | 주소/형식·읽기/쓰기 | 소유·미확정 |
|---|---|---|---|
| MV01_Encoder | 0673 AufDBBlock RID462, NID50 UID24 InstanceDB, TOD15 | DB15 인스턴스, High_Speed_Counter FB1150(0679 RID330) | MV01 엔코더 처리 인스턴스. 현재 HW 식별자/채널 설정은 미확보 |
| EM_OK | 0678 SimpleAccess Global RID173, NID31 UID1064 / NID50 UID26, SAD Input AO156 | I19.4 Bool 읽기 | 이름만으로 전체 안전 허가·현재 참값 단정 금지 |
| MV01_Close | 0678 Global RID205, NID31 UID1065, SAD Input AO66 | **I8.2 Bool 원시 입력** 읽기 | 처리 DB13와 구분. 도면 LS24 정상 극성·실제 캠 위치 미확정 |
| SW_GATE0 | 0676 Global RID207, NID31 UID1066 Write/1075 Read, NID50 UID27 Read; AO184 BAD177 | fill_unit1.CONTROL_SIGNALS.SW_GATE0, DB91.DBX23.0 Bool | 0674 RID177 TOD91 결속. bit 쓰기, 카운터 실측값 아님 |
| ACT_CNTV0 | 0676 Global RID209, NID50 UID47 Write, NID31 UID1068 Read; AO1184 BAD177 | fill_unit1.ACT_CNTV0, DB91.DBD148 DInt | HSC CountValue 출력. 실제 신호모드/배율 미확정 |
| Encoder_CH00 | 0676 Global RID192 AO0 BAD191; NID31 UID1067 Read/1079 Write | DB8.DBD0 DInt | 0674 RID191 TOD8. NID30 UID942에도 Write 선언 존재. 이번 NID31만이 유일 writer라 하지 않음 |
| CNT_Act_0 / CNTV0_100 | 0677 InterfaceAccess **Local** RID190/212; NID31 UID1069 Write/1070 Read, UID1072 Write/1073 Read | DInt 임시 지역값, SSD D AO400/112 | AO를 고정 전역 DB 주소로 발명하지 않음 |
| Encoder_CH00_10 | 0676 Global RID214 AO288 BAD191; NID31 UID1074/1077 Write,1082 Read | DB8.DBW36 Int | 이름 `_10`과 실제 **/100** 연산을 구분 |
| COEFF_TRASM_MV01 / ZERO_TRASM_MV01 | 0676 RID218/219 AO1648/1632 BAD8, NID31 UID1083/1084 | DB4.DBW206 / DB4.DBW204 Int 읽기 | 0674 RID8 TOD4. 현재 값·현장 교정은 미확보 |
| Data.Pot_MV01 | 0676 Global RID220 AO1184 BAD11, NID31 UID1085 Write | DB1.DBW148 Int | 0674 RID11 TOD1. 단위·개도%·센서형식은 이름으로 확정하지 않음 |
| Allarm.Pot_MV01_OFR | 0676 Global RID432 AO198 BAD354, NID31 UID23 Write | DB3.DBX24.6 Bool | 0674 RID354 TOD3. 위치 변환 출력, 부모 MV01_FAULT와 별도 |
| RESET_ALLARM | 0676 Global RID464 AO48 BAD463, NID50 UID30/31 | DB2.DBX6.0 Bool 읽기 | 0674 RID463 TOD2. HSC ErrorAck/EventAck 요청이지 성공 응답 아님 |
| ResetEncoderProcedure_MV01 | 0619 Global RID196 AO405 BAD190, NID14 UID27 Read/33 Write; NID1 UID24/274 Read | DB41.DBX50.5 Bool | 0618 HMI_DB TOD41. 리셋 절차/부모 구동 영향 |

DB91.DBD148와 DB1.DBW148은 같은 byte 번호지만 **다른 DB·다른 형식·다른 단계**다. Word/Int값 전달을 bit 래치와 섞지 않는다.

### 2.2 HMI 자료 범위

`hmi_plc_tags.csv`에는 `RESET_ENC_MV01 → DB41,X50.5`, ID00464가 있다. `MV_01\\LimitSwitchOpen/Close → DB11,X18.3/18.4`, `OutputOpen/Close → DB11,X18.0/18.1`, `Allarme1 → DB11,X18.2`는 부모 표시 계층이다. 이 설정표는 화면 이벤트·쓰기 권한·현재 연결·실값의 증거가 아니다.

지정 CSV의 `ZT[-_ ]?02`, `Pot_MV01`, `Encoder_CH00` 대응은 검색에서 확보하지 못했다. ZT02 전용 화면·수치표시·트렌드·버튼 이벤트는 미확정이다. DB11의 한계 표시는 ZT02 연속 카운트 자체가 아니다. 부모 초안 0367 HMI 핀 미결속을 재명명으로 해소하지 않았다.

## 3. 제어 구조

### 3.1 HSC 읽기 — 0506 / LAD1756 / NID50

`Contact21 NOT Simulation(1)` W51/ORef25 RID344(0678, M180.0) → W52 → Contact22 EM_OK W53/ORef26 → W54 → **LRef23.en**. LRef23 RID330은 0679 High_Speed_Counter이며 Instance24 RID462은 0673 MV01_Encoder DB15다. 호출 조건은 정적 접속만 확인했으며 시뮬레이터는 실행·수정하지 않았다.

| HSC 핀 | Wire / ORef / 선언 | 판정 |
|---|---|---|
| SwGate | W55 /27 /0676 RID207 | SW_GATE0 읽기 |
| ErrorAck | W58 /30 /0676 RID464 | RESET_ALLARM 읽기 |
| EventAck | W59 /31 /0676 RID464 | 같은 RESET_ALLARM 읽기 |
| CountValue | W75 /47 /0676 RID209, NID50 AK Write | ACT_CNTV0 DInt 쓰기 |

미결속 19핀: CaptureEnable(W56/O28), SyncEnable(W57/O29), SetCountValue(W60/O32), StatusHW(W61/O33), StatusGate(W62/O34), StatusUp(W63/O35), StatusDown(W64/O36), CompResult0(W65/O37), CompResult1(W66/O38), SyncStatus(W67/O39), CaptureStatus(W68/O40), CapturedValue(W69/O41), ZeroStatus(W70/O42), PosOverflow(W71/O43), NegOverflow(W72/O44), Error(W73/O45), ErrorID(W74/O46), MeasuredValue(W76/O48), CompareMeasuredValue(W77/O49). 각 ORef는 원본에 RefId가 없다. FALSE/0·인접 MV 채널·일반 DB offset으로 채우지 않는다. ErrorID 핀 형식 Word(0679 interface)라는 사실과 실제 저장 주소는 별개다.

### 3.2 값 처리 — 0512 / LAD1762 / NID31

1. EM_OK Contact1113 W1087/ORef1064 → W1114 → **NOT 원시 MV01_Close Contact1115** W1088/ORef1065 → W1116. 이 W1116이 Coil1025와 Add1030.en으로 분기한다. Coil1025 operand W1089/ORef1066은 SW_GATE0 bit를 쓴다.
2. Add1030 DInt: W1090/O1067 Encoder_CH00 + W1091/O1068 ACT_CNTV0 → W1092/O1069 Local CNT_Act_0.
3. Add.eno W1093 → Div1034.en; Div in1 W1094/O1070 CNT_Act_0, in2 W1095/O1071 **DInt100**(0675 RID211, NID31); out W1096/O1072 Local CNTV0_100.
4. Div.eno W1097 → Move1038.en; in W1098/O1073 DInt CNTV0_100 → out1 W1099/O1074 **Int Encoder_CH00_10**. 변환·정수 나눗셈·범위/잘림의 실행 결과를 임의 보정하지 않는다.
5. EM_OK 공통 W1114 → **NOT SW_GATE0 Contact1117** W1101/O1075 → W1118. Move1047 W1102/O1076 Int0(0675 RID44) → W1103/O1077 Encoder_CH00_10; 병렬 Move1052 W1104/O1078 INT#0(0675 RID327) → W1105/O1079 DInt Encoder_CH00. 이 두 쓰기와 Add/Div 가지를 구분한다.
6. EM_OK W1114는 별도로 **CRef1059.en**에 직결한다. CodeBlock1086 RID5(0672) / CRef RID351(0680)는 Signal linearization이다. Add/Div.eno에서 이 호출 en으로 가는 사슬이 아니므로, 선형화가 항상 새 계산값을 받는다고 단정하지 않는다.

| Signal linearization 핀 | Wire / ORef / RID | 값 |
|---|---|---|
| IN0 | W1107/O1081/R1 (0678) | ON M0.0 심볼 |
| Analog_input | W1108/O1082/R214 (0676) | Encoder_CH00_10 Int |
| Coeff | W1109/O1083/R218 | COEFF_TRASM_MV01 |
| Zero | W1110/O1084/R219 | ZERO_TRASM_MV01 |
| OutValue | W1111/O1085/R220 Write | Data.Pot_MV01 |
| Out_of_range | W24/O23/R432 Write | Allarm.Pot_MV01_OFR |

ON은 상수 TRUE라고 가정하지 않는다. LS24 NC 도면, raw I8.2, NOT 접점, SW_GATE0, 값0 쓰기는 서로 다른 계층이다. 기계 닫힘·입력 정상극성·게이트 하드웨어 상태·원점복구 완료를 하나의 사실로 묶지 않는다.

### 3.3 공유 선형화 직접 대조 — 0291/0014

0291 LAD1658 NID1: IN0 Contact255 → Gt258(Analog_input > −1382, W30/31) → Le161(≤32767, W27/28) 조건 아래 Convert164/167(Int→DInt App5/App6) → Add170 → Convert174(Coeff→DInt App4) → Mul177 → Div181(DInt28000) → Move185(OutValue Int). 각 Convert/Add/Mul/Div ENO 연쇄는 원본 Wire에 남아 있으며 실수 연속 비례식으로 대체하지 않는다. 개략 식은 `(Analog_input + Zero) × Coeff / 28000`이나 이것만으로 실제 정수 경계 동작·단위를 확정하지 않는다.

0611은 IN0 RID1 Bool, Analog_input RID3 Int, Zero RID8 Int, Coeff RID13 Int, OutValue RID19 Int, Out_of_range RID26 Bool의 **Local InterfaceAccess**다. 중간 App3/4/5/6은 DInt. 0612의 상수 RID17=28000 DInt, RID25 SV=−1382, RID29=32767, RID21 SV=−9999 Int를 문맥으로 결속했다. 원시 V=55537 같은 저장 표현을 양수 운전값으로 오독하지 않는다.

0014 LAD1659 NID2: NOT IN0 Contact171(W168/O165/R1) → W172 Move162.en; W169/O166/R23=0 → W170/O167/R19 OutValue. IN0=0 가지의 0출력과 센서 실측0을 분리한다.

### 3.4 리셋 절차·부모 구동 경계

0354 LAD1703 NID14: Contact21 ResetProc(W35/O27/R196) → Contact22 **Inputs.MV01 Close**(W37/O28/R173; DB13.DBX8.2, 원시 I8.2와 구분) → W38 Move23.en. W39/O29/R194=0(0620) → W41/O30/R201 `MV01_Encoder.NewCountValue`. Move23는 **DisableENO=true** 속성을 가지면서 원본 W40은 Move.eno→NOT SetCountValue Contact24(W42/O31/R202)를 연결한다. 실행 의미를 일반 ENO 가정으로 확정하지 않는다. W43 Coil25→W44/O32/R202 SetCountValue, Coil.out W45→RCoil26→W46/O33/R196 ResetProc.

0619 RID201은 DInt NewCountValue SSD S AO320, RID202는 Bool SetCountValue SSD IO AO288이다. 두 멤버를 뒤집거나 offset만으로 통신 절대주소를 확정하지 않는다. 0506 SetCountValue 실인수 O32의 RefId 미확보 때문에 이 사슬로 실제 하드웨어 count=0 완료를 증명할 수 없다.

0342 NID1의 ResetProc 읽기 위치를 직접 확인: NOT ResetProc Contact23 W22/O24→W25 열림 Coil143 경로; ResetProc Contact273 W276/O274→W21 OR151.in3는 닫힘 경로에 별도 합류한다. 부모 출력·접촉기/리미트/기계구동은 MV01 소유이며 ZT02 전용 출력으로 복제하지 않는다. 버튼 조작·기계 이동·교정을 안내하거나 수행하지 않았다.

### 3.5 다른 쓰기·검토 경계

0676 RID192에는 NID30 UID942 Write도 있다. 이번 고유 위치 처리 NID31 외 쓰기 존재를 보존하며 현재 최종값/전체 호출순서를 확정하지 않는다. 부모 문서에는 Data.Pot_MV01의 별도 simulation 블록 쓰기 선언도 기록되어 있다. 이는 공유 경계 참고이며 해당 중지 블록 본문을 새로 연구·실행하지 않았다. 외부 HMI/간접주소/현재 CPU의 모든 writer를 검증했다는 주장을 하지 않는다.

## 4. 전기 전달 경로

FG45/실제 PDF46 ↔ FG144/실제 PDF145를 직접 렌더로 대조했다.

| ZT-02 시작점 | FG45 중간 단자·선 | FG144 TM1 끝점 |
|---|---|---|
| B +24Vdc | X1/107, 선37.1, 교차37/2·144/5 | MOD16 단자9 24VDC 공급 |
| C −0Vdc | X1/108, 선37.2 | 단자10 M |
| D | X1/109, 선45.1, 교차144/2 | 단자1 CH0.A |
| E | X1/110, 선45.2, 교차144/2 | 단자2 CH0.B |
| 실드 | X1/111,45SCH1, 교차144/1 | 접지/실드 기호 |

CH0.N 단자3에는 이 ZT02 현장선이 그려져 있지 않다. 단자4/5/6의 E20.0/1/2와 단자7/8 A8.0/1은 SPARE로 적혀 있다. 도면에 CPU515라고 쓰여 있어도 현재 설치 CPU를 확인한 것이 아니다. A/B 분해능·전기 출력방식·N유무·방향·PNP/NPN·엔코더 형번은 미확보다.

같은 FG45의 LS23/24는 ZT02와 다른 장치다. LS24 NC11/12는 X1/114(+24V측 5×20 2A F)→45.4→LS24→X1/115→E8.2(참조124/3). ZT02 본체 단자와 혼합하지 않는다. FG124 전체는 이번에 재렌더하지 않았으며 부모 MV01 C4 경로를 공유 참조한다.

시공 PDF57의 고유 두 행:

| 행 | 케이블·FROM→TO | 설계표 기재 |
|---|---|---|
| 7_5 | `=FLA+HE01-FLO2TB1E`, CR → HE-01 FLO2TB1, description ZT02 | AI, CVV-S,4S,1.0,spare0, route100/110 LAD1/E100, adjustment5,LEN50 |
| 7_10 | `=FLA+MV01-ZT02A`, HE-01 FLO2TB1 → MV-01 ZT-02 | AI,CVV-S,4S,1.0,spare0,routeE330,adjustment5,LEN6 |

이 길이는 실측이 아니라 표 설계값이다. HE01 단자함을 경유한다고 ZT02의 부모를 HE01로 바꾸지 않는다. **AI 분류와 OEM 엔코더 A/B 회로 상충**은 유지한다. 준공 수정도, 양끝 단자함 결선표, 실물 형번·규격, 현재 TM 하드웨어 구성으로 해소해야 한다. 4심 차폐 케이블이라는 사실만으로 어느 신호규격인지 확정하지 않는다.

## 5. 알람·복구

### 5.1 고유 위치 범위 출력

0291 NID1에서 Analog_input >32767(Gt190 W36/37) 또는 ≤−1382(Le259 W38/39) → OR47 W49 → Move193: W252/O218=−9999 → W253/O219 OutValue. Move.eno W21 → 일반 Coil23 → W22/O24 Out_of_range. 이 호출의 반환 대상이 0512 W24/O23/R432의 DB3.DBX24.6이다.

이는 **일반 Coil 출력**이며 별도 S/R 유지 알람으로 임의 분류하지 않는다. 해당 경로 안에 지연 타이머를 확보하지 않았다. 입력형식은 Int이므로 >32767 상한 가지를 반드시 가능한 센서 물리 고장으로 설명하지 않는다. ≤−1382 처리 조건·−9999 결과와 실제 단선/전원상실/엔코더 미변화는 등치할 수 없다. 호출이 없거나 이전값이 남거나 다른 writer가 있을 때의 현장 표시·해제도 미확정이다.

### 5.2 부모 고장·타이머와 분리

부모 MV01 초안 E09/E10/E11의 공통 설명을 연결 재사용: MV01_FAULT DB3.DBX4.7은 Q/접촉기응답 불일치 Tag92=T4, S5T#150mS 및 방향 명령 누적 W33>2000/W34<−2000의 공통 래치다. W33/W34는 엔코더 CountValue가 아니다. 이 값·타이머를 ZT02 센서 미변화 검출·전행정 시간·전류 보호로 복제하지 않는다. 이번 고유 범위에서는 부모의 그 네트워크 전체를 다시 의미 검토하지 않았다.

HSC ErrorAck/EventAck가 RESET_ALLARM에 연결된 사실은 확인했다. Error/ErrorID·StatusGate·ZeroStatus의 실제 반환 주소는 미결속이다. 요청=성공·OFR해제=원점복구·ResetProc 해제=기계 정상으로 표시하지 않는다.

## 6. 증상별 관찰 문서

현장 조작 절차가 아니라 **이미 승인된 안전 관찰 자료의 수집 항목**이다. 활선 측정·강제출력·점퍼·리셋·원점이동·보호값 변경을 실행하거나 권고하지 않는다.

| 증상 | 구분해서 기록할 자료 | 판단 경계 |
|---|---|---|
| 위치 수치가 고정됨 | 실제 관찰시각, ZT02 명판/연결 사진, TM 채널 구성, ACT_CNTV0 DInt, Encoder_CH00, Local 계산값, Encoder_CH00_10, Pot_MV01 | HMI값 하나로 엔코더 고장을 단정하지 않음; HSC 호출허가/게이트/정수변환/표시경로 각각 확인 필요 |
| 0이 표시됨 | raw I8.2와 Inputs.DB13.X8.2를 분리, EM_OK,SW_GATE0,Move1047/1052 조건,IN0 | 실측0, 소프트웨어0쓰기, IN0차단0을 구분; 현재 정상극성 미확정 |
| −9999 또는 OFR | 정확한 DB1.W148/DB3.X24.6 값, 선형화 입력 Int, Coeff/Zero 백업·현재 버전, 호출시각 | 범위 처리값과 물리단선/아날로그 4–20mA 고장으로 단정 금지 |
| 리셋 후 움직임/값 변경 | ResetProc 요청·부모 Q2.4/Q2.5·리미트·SetCountValue/실제HSC 상태와 시각 | 구동영향 있음. 재실행이나 원점 교정을 권장하지 않음; 완료는 별도 증거 필요 |
| MV01_FAULT만 발생 | 부모 응답·방향 누적과 ZT02 위치채널을 별개 시계열로 기록 | 150ms/±2000을 ZT02 고장임계로 사용하지 않음 |
| 시공표와 실제 배선이 다름 | 케이블7_5/7_10 양끝 표찰, X1/107~111,TM1 단자1/2/9/10, 준공판본 | OEM/시공표 중 현재 우선 문서를 임의 선택하지 않음 |

관찰자·시각/시간대·자료 취득 위치·태그·주소·단위/미확정·CPU/프로젝트 판본·비교 문서·조치 승인·복구 증거를 따로 남긴다. 실제 사용자 운영 사진/자료를 공개 저장소에 복제하지 않는다.

## 7. 완료·누락·인계

| 영역 | 판정 | 남은 자료 |
|---|---|---|
| 설비·자료 기준 | 문서대응 확인, 실물 보류 | ZT02/MV01 명판·센서 모델·준공대응 |
| I/O·HMI | 백업 선언/도면 및 처리경로 확인 | HSC 19핀 결속, 현재채널, 전용 HMI 수치/이벤트 |
| 제어 구조 | 위치 처리·공유 선형화·리셋 영향 정적 확인 | 실제 호출순서·다른 writer·실행결과 |
| 전기 끝점 | FG45↔144 직접 확인, 시공AI 상충 유지 | 준공 배선·규격·단자함 양끝 |
| 알람·복구 | OFR 일반Coil/부모고장 분리 | 현재 HSC 상태/오류주소·복구 관찰 |
| 증상 관찰 | 증거수집 항목 작성 | 실제 승인 관찰기록 |
| 완료 기준 | 문서 complete_with_gaps | UI/현장/게시 등 별도 상태 |

### 한정 검색과 중단 기준

- `decoded-original/*.xml` **695개**에 대해 ZT[-_ ]?0?2 경계 문자열 검색: **0개**. 이것은 문자열 검색 결과이며 695개 논리 의미 검토 완료를 뜻하지 않는다. XML의 MV01 별칭·HSC 처리 연결은 위 0506/0512 및 선언으로 독립 확인했다.
- HMI CSV 지정 패턴 검색, 부모 MV01 색인, OEM FG45/144, P&ID1, 시공57, 선정 선언만을 중심으로 조사했다. 모든 모듈·전체 도면·PLC 모든 네트워크의 완전성을 주장하지 않는다.
- 고유 주소 부족을 이유로 부모 전체 재조사나 로컬 TIA 추가 접근으로 확대하지 않았다. 필요한 다음 한 작업은 **ZT02 실물 모델/준공 결선과 현재 TM1/HSC 설정 자료를 받아 문서 간 대응을 검토**하는 것이다. 새 자료 없이 같은 실물 보류를 반복 조사하지 않는다.

### 별도 완료 상태

| 상태 | 결과 |
|---|---|
| documentation | complete_with_gaps — 이 한 ID 초안 |
| static_review | scoped_completed — 지정 XML/선언·4 PDF페이지·27 해시 |
| ui_records | not_run; 비교화면/백업복원/전후기록/보고서 UI 미검증 |
| publication | not_published; 이 조사자는 첨부·통합·게시하지 않음 |
| tia_compile / live_cpu / field_recovery | not_performed |

원본·공용코드·대장·버전·운영 기록·부모 초안은 변경하지 않았다. 시뮬레이터 작성/수정/생성/실행/행동시험, 프로젝트 생성기/build/test, PLC/현장/보호값/SEJIN 변경, 새 Work/Codex·재위임은 하지 않았다. 네 기능의 구현·저장/재열기 검증을 하지 않았으므로 BC01 동등 기능 완료라고 표시하지 않는다.

## 부록 A. 선정 원본 SHA256·고정 Git blob 전체표

27개 모두 현재 파일의 Git blob 계산값이 고정 abcf31c의 해당 blob과 일치한다. SHA256은 부모 MV01 초안 표와도 27/27 일치했다. 해시 일치는 원본 보존/입력 동일성 검사이며 27파일 전체 의미 검토를 뜻하지 않는다. decoded-original의 지정 네트워크/선언만 의미 검토했다.

| 고정 원본 경로 | SHA256 | Git blob | 일치 |
|---|---|---|---|
| docs/equipment-standard/INVENTORY.json | 720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc | 587c3748ad9224718f95ba06463fee913dae231d | True |
| all-in-one/sources/PID_1684n002I.pdf | 2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b | 8c83a59fefd5b8b651ec3537ea4236a073f5e109 | True |
| all-in-one/sources/Electrical_Rev2.pdf | 5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6 | f610fd7c7ce14ae951b00cff57b969259bfb389d | True |
| all-in-one/sources/Electrical_Can_Decoating_20241118.pdf | 3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd | 0ee6b6f8361c5790864dbba4bbd9d55e8e7c08f8 | True |
| all-in-one/sources/hmi_plc_tags.csv | a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404 | cf4c0650e7c7baac350dcb89909b808435704880 | True |
| all-in-one/sources/decoded-original/network-map.json | c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60 | 424430b6b953e43138e5d0a18ca40c949e21cfa1 | True |
| all-in-one/sources/decoded-original/0506-FlgNet.xml | 71b9ac920eb891ec8965506c40ae3f1d050a2f8a899f79f6afdc81f669717fbe | 8e26b2cc02f4e38863022d2fb8da0f7322e2125f | True |
| all-in-one/sources/decoded-original/0512-FlgNet.xml | 9437caf0fc524d25925ca5beb3c3bf1a2a0709a478a2981e42e5abe1e4471795 | d0402898b8f7949733aa7d94af18d0978a766322 | True |
| all-in-one/sources/decoded-original/0354-FlgNet.xml | 626eb4d21b9409ae50ed32436972c8a4284fcc029c10db5c5529463544b2ffbd | b7ee6b7ad489e1f2853941aae23aefb3058475ef | True |
| all-in-one/sources/decoded-original/0342-FlgNet.xml | 9ef93abad16cc055509ef98c388417c716cb03d23cb02aed6d95888beb43bef8 | a9b1841964216331887d18f91c014c0534cc9df1 | True |
| all-in-one/sources/decoded-original/0291-FlgNet.xml | fe0b92f074eba25148ce34084649af3d968962558d652727f1eea19f3e3c2550 | 1418fb2ed172c6df694a5eb8bf2dffd0b177653b | True |
| all-in-one/sources/decoded-original/0014-FlgNet.xml | 2e814adbaac6bab99bc668bfdab74f0fc90576324d0b88728951683869cfac30 | 4d164b074fcc13a8f97da9e24382cc169ef29555 | True |
| all-in-one/sources/decoded-original/0611-IdentXmlPart.xml | 0d583915a261703954da22c176ba9f81338ad13ea2810e7cd5f7de8aa1bfa089 | bad6b16fb32a32d47d882f48754994887457872b | True |
| all-in-one/sources/decoded-original/0612-IdentXmlPart.xml | 95b545d4964d371ebfc107894ea90b8b1d0d7ab5d3a70e643f8ce539063c0f38 | 7cc782d33d07ef225c2104f3e7c9fbd31f7c7467 | True |
| all-in-one/sources/decoded-original/0617-IdentXmlPart.xml | 10bcf85169cb2512f55acadaef299a3d46b4b4cecd88032d739cfeba23e94aa9 | 9527658ee6808be34bd513b1b2ebaf3a4a5a6f3e | True |
| all-in-one/sources/decoded-original/0618-IdentXmlPart.xml | 0c6762de9cdf0e294317f7463bea3d8e6df5673d333d9b1826ebd17a7ded044c | 9eec0dbd8abde4aa7295f77b63ad473f895f274b | True |
| all-in-one/sources/decoded-original/0619-IdentXmlPart.xml | 85694bb5b696e31e6a1217431112e5b750516c4f94078d6e127d4394a8b80456 | 11f0502c84a1f319a21459a35c0dc1c6ce8e8f36 | True |
| all-in-one/sources/decoded-original/0620-IdentXmlPart.xml | da97226a148a1a8babaea67db412761a718b7e7537212b7807e8ea27d000d2d3 | dc88b5e87ad3331928f14fcf647673a26fb70b6b | True |
| all-in-one/sources/decoded-original/0672-IdentXmlPart.xml | 6bfc2ba142d6270c39eb1f13b2886204865af6d46eadc5f410c26981b8da9222 | 2f2790dab4bb2357733112220e0acc41edb6feb6 | True |
| all-in-one/sources/decoded-original/0673-IdentXmlPart.xml | 450ef74e2d2fb65dfbb5f6bad9e28ccacf6bf0caf64327a0e20aff84d6e40f58 | 1957bff7dd1beffcb6e2a40d6a541c1751753548 | True |
| all-in-one/sources/decoded-original/0674-IdentXmlPart.xml | 4770702f519bacda69202bb2f7733d983074bda90964360c238f990d9d08fd84 | f210593944547b63eab10c667348711413600aab | True |
| all-in-one/sources/decoded-original/0675-IdentXmlPart.xml | b1902886927d8403fab736d9c8ffe73f2fbc8ce4b7ca7c345144964668b051c3 | d82a33b173c8dc0737fd890eb2a63a88a07d0831 | True |
| all-in-one/sources/decoded-original/0676-IdentXmlPart.xml | c58427c5b0ac6c11cdb52e4c6d0461c7b191fae81ccace191048e9f175fcec59 | 1ed67265f69796a4e659f9438e551068037f33a4 | True |
| all-in-one/sources/decoded-original/0677-IdentXmlPart.xml | 69922fcc5c67d00cdf1c5f712efa3db7638d20c88318d35fe6196467796ab1e3 | b9437406a7e24f073ef88b8369cacc9ad4ecc5ac | True |
| all-in-one/sources/decoded-original/0678-IdentXmlPart.xml | 51e637e0b9713c028810f2a717b5c3804a3a26c2f1be7e332a4d6bf277bfc382 | 7fafb2297bcdf739bf1d1dd68cebc0d74f2a40cc | True |
| all-in-one/sources/decoded-original/0679-IdentXmlPart.xml | d0fcb93e188c8ae2ae0c0423f0b78b129bf3c168e33a6855262d34b8682b9b56 | e8d8a014609871082bf5cfca0f9ab9b78136e920 | True |
| all-in-one/sources/decoded-original/0680-IdentXmlPart.xml | fd551ad5d47bbd66c6bcdcc1949aaddf68cc086a3ddf6fb337adc767954c2b95 | c9049ced1eaed72c5e251a88601d46ddec8c3e50 | True |

## 부록 B. 실제 수행 검사

- 최종 검사시각: 2026-10-11T12:56:29.966769+00:00 UTC.
- 자체 XML 파서/정적 문서검사 12항목 통과. HSC 19 미결속, 직접 호출 en, ENO 사슬, Reset Move DisableENO 속성, 7영역, 27개 해시표를 대조했다.
- 고정 source tree 712파일 byte/Git blob 일치. 이것은 보존검사이며 전수 의미검토가 아니다. 원본 Git status 깨끗함.
- 중지5자산은 freeze SHA256과 5/5 일치하며 내용 연구·실행 없이 보존 해시만 확인했다.
- 초기 보조 스크립트 파일명이 Python 표준 inspect와 충돌하여 PDF모듈 로딩 1회 실패했고, 이름을 trace_extract로 바꾸어 재실행 성공했다. 원본 변경은 없었다.
- 보존 기록: extracts/ZT02/source-hashes.json, source-preservation.json, checks.json, literal-search.json 및 PDF 렌더. 전달·첨부는 부모 담당.
