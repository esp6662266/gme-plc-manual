# ZT05 — MV05 위치 계측 고유 원본 조사 초안

- 대상 catalog_id **ZT05 한 개**, sensor / 계측 / parent_id MV05 / depth1 / phase2. 부모 MV05 완료를 상속하지 않는다.
- 고정 읽기전용 기준: source-mv06, **abcf31c5030bc7ef8749ed8e869a857f2387a28a / v1.12.0**, GME-STD-1.0.0. 현재 게시 버전·CPU·실물을 확인한 문서가 아니다.
- 상태: documentation **complete_with_gaps**. 원본 정적 문서 조사이며 TIA/현장/조작/실행 검증 아님. 모델·추론수준 런타임 증명 미확인.

## 핵심 확인·상충·누락

1. OEM FG35/실제 PDF36은 **ZT-05 ENCODER**, FG147/PDF148은 **MV-05 ENCODER ZT-05**와 MOD17 CH1.A/B 단자11/12를 직접 명시한다. P&ID PDF1도 MV05/M15와 ZT05를 연결한다. 단지 ZT 이름으로 계측 종류를 추정한 것이 아니다.
2. 백업의 위치 후보 경로는 MV05_Encoder DB18 → ACT_CNTV3 DB91.DBD172 → DInt 합산/**100 나눗셈** → Encoder_CH03_10 DB8.DBW42 → FC63 → Data.Pot_MV05 DB1.DBW140이다. 도면 CH1과 소프트웨어 CH03은 다른 이름 공간이며 현재 기술 객체/하드웨어 채널 동일성은 미확정이다.
3. 0515는 **원시 MV05_Close I7.2**를 NOT 접점으로 사용한다. ZT04의 처리 Inputs.MV03 Close 경로를 복제하지 않는다. 부모 리미트와 위치 계측을 같은 센서로 합치지 않는다.
4. 시공 실제 PDF26의 장치 ZT05 행은 케이블 ZT06A, PDF56 incoming 6_6 설명은 ZT06, outgoing 6_20은 ZT05A/ZT05다. OEM ZT05와 함께 상충 그대로 보존하며 임의 정정하지 않는다.
5. HSC 21개 ORef에 RefId가 없다. ErrorAck/SetCountValue/상태·오류 주소·현재 HW 매핑·복구 완료를 발명하지 않는다. ZT05 직접 XML 이름과 ResetEncoderProcedure_MV05는 확인 검색 범위에서 없었다.
6. HMI CSV에 DB1,INT140(data_DB1_DBW140)과 DB3,X25.1(Allarmi_239)이 있다. 위치 OFR와 부모 MV_05_FAULT/150ms/±700 감시는 별개다. 실제 표시창/이벤트/알람문구/활성 상태는 미확정이다.
7. 공유근거는 MV05-DOTS-DRAFT.md 및 ZT02~04-DOTS-DRAFT.md를 색인으로 재사용했다. 고정입력 공통 FC63 설명은 재사용하고 대표핀/상수를 대조했다. 부모 구동·PID·공유인버터 전체를 반복조사하지 않았다. 새 보강은 0511 고유 저장 가지, HMI 두 주소, 명시한 상충·원시 입력 구분이며 이전 초안 전체 오류나 현재 현장 정정이라고 주장하지 않는다.

## 1. 설비·자료 기준 — 적용

INVENTORY.json catalog[116]의 ZT05는 planned/baseline/not_assessed이며 부모 MV05와 별도 ID다. 같은 이름 ZT02~06은 별도 catalog다. P&ID의 RO01 산소 제어 관계, MV05 모터 M15, LS15/16 리미트는 관련 소유이며 ZT05 전용 PLC 소유로 가져오지 않는다.

| 원본 | 실제 확인 위치·판본 | 의미와 경계 |
|---|---|---|
| all-in-one/sources/PID_1684n002I.pdf | PDF1, 도번1684n002, Apex I, 기본06/04/2011, I개정15/01/2013 REMOVED MC-05, CHANGED POWER OF FN-02 | MV05/M15 0.25kW 440V·LS15/16·ZT05 배치. 모터 정격은 ZT05 정격 아님 |
| all-in-one/sources/Electrical_Rev2.pdf | FG35/PDF36, FG39/PDF40, FG146/PDF147, FG147/PDF148; 네 쪽 DATA27.05.2024, 별도 개정 기입 공란 | FG35 ZT05, FG39 공유공급 경유, FG146/147 MOD17. 파일명 Rev2를 전 페이지 개정으로 복제 금지 |
| all-in-one/sources/Electrical_Can_Decoating_20241118.pdf | PDF26 CANDC-CONS-E009-026/D-PAGE9/TOTAL26/64; PDF56 CANDC-CONS-C006-056/D-PAGE6/TOTAL56/64; Rev1 24.11.11 first draft design | 설계/시공 참고. 승인 준공·실측 아님. 가림 6_7~6_10은 근거로 사용하지 않음 |
| decoded-original XML | 0509 LAD1759 NID48, 0515 LAD1765 NID33, 0511 LAD1761 NID30 | LAD번호는 network-map 탐색 색인, 직접 근거는 원형 Part/Wire와 Ident 선언 |

본문 네 자리 XML 번호는 all-in-one/sources/decoded-original/ 기준이다. NID/RID/UID는 파일·블록 문맥을 함께 사용한다. 원본 root AGENTS/rollout SKILL/WORK-STANDARD/WORK-ITEM-TEMPLATE/INVENTORY 및 재개문서 상단을 읽었다. 이번 권한은 문서만이며 원본 생성기·preflight·build/test를 실행하지 않았다.

## 2. I/O·HMI — 부분 적용, 현재 연결 미확정

독립 ZT05 IW/PIW 또는 4–20mA 입력은 확보되지 않았다. OEM은 엔코더 A/B, 백업은 HSC·DB 처리값이다. 부모 Q1.3/Q1.4는 방향 명령이며 ZT05 측정값이 아니다. FG147의 E21.3/4/5와 A9.2/3은 SPARE로 그려져 있으므로 ZT05 입력 비트로 배정하지 않는다.

| 대상 | 원본 선언·문맥 | 주소/형식·읽기/쓰기 |
|---|---|---|
| MV05_Encoder | 0673 AufDBBlock RID347 NID48 UID24 InstanceDB TOD18; 0679 Instruction RID330 NID48 UID23, FB1150 | DB18 High_Speed_Counter. 현재 HW 식별 미확보 |
| EM_OK | 0678 Global SimpleAccess RID173, NID48 UID26/NID33 UID1272/NID30 UID940; SAD Input AO156 | I19.4 Bool 읽기. 전체 안전성이나 현재 true 증명 아님 |
| MV05_Close | 0678 Global SimpleAccess RID447 NID33 UID22 SAD Input AO58 | **I7.2 원시 Bool 읽기**, 처리 DB13와 별도 |
| Simulation(1), ON | 0678 Global RID344 AO1440 Memory / RID1 AO0 Memory | M180.0 / M0.0 Bool. 원본 호출 경계만 읽었으며 관련 기능 실행 안 함 |
| SW_GATE3 | 0676 Global RID345 AO187 BAD177; NID33 UID1274 Write·1283 Read, NID48 UID27 Read | DB91.X23.3 Bool bit 쓰기/읽기 |
| ACT_CNTV3 | 0676 Global RID346 AO1376 BAD177; NID48 UID47 Write, NID33 UID1276 Read | DB91.DBD172 DInt |
| Encoder_CH03 | 0676 Global RID201 AO96 BAD191; NID30 UID948 Write, NID33 UID1275 Read/1287 Write | DB8.DBD12 DInt, 저장·0쓰기 복수 경로 |
| CNT_Act_3 | 0677 Local InterfaceAccess RID200 SSD S=D AO496; NID33 UID1277 Write/1278 Read, NID30 UID947 Read | Local DInt. 이를 DB 주소로 만들지 않음 |
| CNTV3_100 | 0677 Local RID348 S=D AO208 NID33 UID1280 Write/1281 Read | Local DInt |
| Encoder_CH03_10 | 0676 Global RID349 AO336 BAD191 NID33 UID1282/1285 Write·1290 Read | DB8.DBW42 Int. 이름 _10이어도 실제 Div는100 |
| COEFF_TRASM_MV05 / ZERO_TRASM_MV05 | 0676 Global RID155 AO624 / RID156 AO608 BAD8; NID33 UID1291/1292 | DB4.DBW78 / DB4.DBW76 Int 읽기. 현행 교정값 미확인 |
| Pot_MV05 | 0676 Global RID157 AO1120 BAD11, NID33 UID1293 Write | DB1.DBW140 Int. 개도%·포텐셔미터 실물 추정 금지 |
| Pot_MV05_OFR | 0676 Global RID438 AO201 BAD354 NID33 UID23 Write | DB3.X25.1 Bool, 부모 구동고장과 다름 |

DB 번호는 0674 DepDBBlock BAD177 fill_unit1/TOD91, BAD191 Memory encoder/TOD8, BAD8 Coeff/TOD4, BAD11 Data/TOD1, BAD354 Allarm/TOD3로 대조했다. AO는 비트 오프셋이며 형식에 맞게 byte/bit로 표기했다.

hmi_plc_tags.csv 직접 확인:
- 행239 data_DB1_DBW140, DB1,INT140, Access PLC, ID002A2.
- 행13 Allarmi_239, DB3,X25.1, Access PLC, ID0045D.
두 행은 dde.cfg 설정이며 현재값이나 실제 표시 단위/알람 발동 증거가 아니다. 부모 MV_05 LimitSwitchOpen/Close와 OutputOpen/Close의 DB11 표시들은 MV05 초안 §2에 연결 재사용한다. 표시 이벤트 전체와 버튼 쓰기, 화면상 ZT05 별칭은 확보하지 않았다.

## 3. 제어 구조 — 고유 3네트워크와 공통 환산

### 3.1 0509 HSC 호출: LAD1759 NID48

Powerrail W50 → **NOT Simulation(1) Contact21**(W51/ORef25 RID344) → W52 → EM_OK Contact22(W53/ORef26 RID173) → W54 → LRef23.en. LRef23 RID330/Instance24 RID347은 High_Speed_Counter/DB18이다.

- SwGate W55/ORef27 RID345 = SW_GATE3 DB91.X23.3 읽기.
- CountValue W75/ORef47 RID346 = ACT_CNTV3 DB91.DBD172 쓰기.
- 미결속21개: O28~46, O48/49. W56~74/76/77의 CaptureEnable, SyncEnable, ErrorAck, EventAck, SetCountValue, StatusHW, StatusGate, StatusUp/Down, CompResult0/1, SyncStatus, CaptureStatus, CapturedValue, ZeroStatus, PosOverflow/NegOverflow, Error, ErrorID, MeasuredValue, CompareMeasuredValue. RefId 없음은 FALSE/0/기본값/물리 단선이라는 뜻이 아니다.
- 0679는 SetCountValue를 InOut Bool, CountValue DInt, ErrorID Word, MeasuredValue Real로 선언한다. 현재 채널·Capture/Sync/진단·오버플로 처리 주소를 추정하지 않는다.

### 3.2 0515 취득값 처리: LAD1765 NID33

EM_OK Contact1321(W1295/O1272) → W1322에서 세 가지로 분기한다.

1. NOT raw MV05_Close Contact1323(W21/O22 RID447) → W1324 → **Coil1233 SW_GATE3**(operand W1297/O1274)와 Add1238.en. 이 bit 쓰기는 실제 축 이동 명령이 아니다.
2. DInt Add1238: in1 W1298/O1275 Encoder_CH03 + in2 W1299/O1276 ACT_CNTV3 → out W1300/O1277 Local CNT_Act_3. eno W1301→Div1242.en. in1 W1302/O1278 CNT_Act_3, in2 W1303/O1279 **DInt100**(0675 RID211) → out W1304/O1280 CNTV3_100. eno W1305→Move1246.en; in W1306/O1281→out1 W1307/O1282 DB8.DBW42. 마지막은 DInt→Int 폭 차이가 있으며 현재 오버플로 결과나 배율을 보증하지 않는다.
3. 같은 EM_OK 아래 **NOT SW_GATE3 Contact1325**(W1309/O1283) → W1326→Move1255/1260.en. Move1255 in W1310/O1284 Int0(0675 RID44) → W1311/O1285 Encoder_CH03_10. Move1260 in W1312/O1286 Int#0(RID327) → W1313/O1287 DInt Encoder_CH03. 0쓰기 두 개와 산술 저장을 단일 센서값으로 합치지 않는다.
4. W1322는 CRef1267.en으로도 직접 들어간다. CRef1267 RID351/CodeBlock1294 RID5 = 0672 FC63 Signal linearization. IN0 W1315/O1289 ON; Analog_input W1316/O1290 DB8.DBW42; Coeff W1317/O1291 DB4.DBW78; Zero W1318/O1292 DB4.DBW76; OutValue W1319/O1293 DB1.DBW140; Out_of_range W24/O23 DB3.X25.1.

EM_OK가 꺼져 호출되지 않는 조건, NOT rawClose 분기 조건, SW_GATE3의 bit 쓰기, 산술 ENO 체인을 구분한다. 현재 스캔순서·최종값·갱신주기는 미확정이다. ZT04의 처리 Close를 이 원시 I7.2 자리로 치환하지 않는다.

### 3.3 0511 별도 저장: LAD1761 NID30

NOT EM_OK Contact963(W951/O940 RID173) → W964 → **Move932.en**. in W958/O947 Local CNT_Act_3(RID200) → out1 W959/O948 Encoder_CH03(RID201) 쓰기. 해당 선언은 NID30 UID948 AK=Write이며 0515의 0쓰기와 별개다. 제목상 전원저장 의도와 실제 지역값 수명·호출순서·Retain·전원차단 시점 저장 보장은 구분한다. 다른 채널 Move는 재조사하지 않았다.

### 3.4 다른 쓰기·리셋 경계

0635 Global RID324 NID2 UID576/584에 Data.Pot_MV05 AO1120 Int Write 선언이 추가로 존재한다. 색인의 해당 문맥은 중지된 simulation 블록(0403)이다. 선언 존재만 기록하며 그 블록 본문 연구·생성·실행·수정·행동시험으로 확대하지 않았다. 따라서 0515를 유일 writer/현재 최종값이라고 주장하지 않는다.

XML695개 이름 탐색과 HMI CSV에서 ZT05/ZT-05/ZT_05 및 ResetEncoderProcedure_MV05 직접 선언을 찾지 못했다. 이는 전체 프로그램에 교정이 없다는 증명이 아니다. ZT02/04의 교정절차를 ZT05에 복사하지 않고 DB18 HSC 설정·현 HMI 이벤트·현재 프로젝트 확인을 요구한다. 0353은 MV03 전용임을 색인/본문으로 확인한 제외 경계이며 ZT05 제어로 채택하지 않았다.

## 4. 전기 양 끝점 — 직접 렌더 7쪽

| ZT05측 | 중간 선/단자 | 모듈측/근거 |
|---|---|---|
| B +24Vdc | X1/67 →35.1 →FG39 공유 분기 | FG146 MOD17/TM1 단자9 24VDC; FG35/PDF36→FG39/PDF40→FG146/PDF147 |
| C −0Vdc | X1/68 →35.2 →FG39 공유 분기 | 같은 MOD17 단자10 M |
| D | X1/69 →35.3 | FG147/PDF148 MOD17 CH1.A 단자11 |
| E | X1/70 →35.4 | FG147 MOD17 CH1.B 단자12 |
| 실드 | X1/71 →35SCH1 | FG147 실드 접지 표시. 실제 접지 시공·연속성 미확인 |
| CH1.N | 단자13에 현장선 표시 없음 | 도면의 미배선 표시와 실제 미사용 확정은 다름 |

FG39에서는 ZT04 B/C도 35.1/35.2에 연결되지만 A/B 신호는39.1/39.2로 별도다. 전원공유를 두 센서 동일성으로 해석하지 않는다. FG35 상단 +24Vdc10.7은 LS15/16 공급 경로이고 ZT05 B/C는 하단35.1/35.2 경유이므로 곧바로 같은 상단선으로 합치지 않는다.

FG147 별도 모듈전원은 +24Vdc10.7 → X21/3041 2A IST →147.1 →41 L+, 44 M→−0Vdc10.6. 모듈전원과 센서공급 단자9/10 및 A/B쌍을 분리한다. CPU515/MOD17/TM1은 도면 식별이며 현재 CPU·슬롯/모델·설정의 확인이 아니다.

LS15/16의 X1/72~75, 35.5/35.6, NC11–12와 E7.1/E7.2는 별도 끝단 감시다. 0515의 I7.2 사용은 위치연산에 영향을 주지만 ZT05 A/B 그 자체가 아니다. 부모 전력·접촉기·인버터는 MV05 초안 §4를 공유근거로 유지하고 본 범위에서 다시 전부 조사하지 않았다.

### 시공 p26/p56 상충과 중계함 경계

| 실제 위치 | 원문 경로/케이블 | 의미·상충 |
|---|---|---|
| p56 행6_6 | =FLA+MV05-FLO1TB2B, CR→MV05/FLO1TB2, 설명 **ZT-06**; TM CVV-S 4S 1.0 spare0; route100LAD1→E200, Adjustment10 LEN42 | OEM ZT05 및 outgoing 행과 상충. 현장 ZT06로 수정 금지 |
| p56 행6_20 | =FLA+MV05-**ZT05A**, MV05/FLO1TB2→MV05/ZT-05; TM CVV-S4S1.0 spare0; E230, Adjustment3 LEN4 | 센서 branch 행. LEN은 설계값 |
| p26 장치 ZT-05 행6_20 | **=FLA+MV05-ZT06A**, CVV-S1.0 core4 | p56의 ZT05A와 다름; 케이블 이름만 병합하지 않음 |
| p26 그림 | MV05측 M15·LS15/16·ZT05, 중계함 그림의 FLO1TB1 표기와 표의 MV05 FLO1TB2 | 그림/표 중계함 명칭도 함께 현장 확인 필요. 그림이 FLO1TB2라고 고쳐 쓰지 않음 |

OEM X1/67~71과 FLO1TB2 내부 단자별 결속표는 미확보다. 이 두 자료를 현재 검증된 준공 전구간으로 합치지 않는다. p56 검은 가림 행의 텍스트 복원은 하지 않았다.

## 5. 알람·타이머·복구 — 위치 OFR와 부모 고장 분리

### 5.1 공통 FC63 대표핀 직접 대조

0291 LAD1658/NID1: IN0 Contact255(W220/O196,0611 Local RID1) → W256; Analog_input Int >−1382 Gt258(W30/31,O32/33) →W25→≤32767 Le161(W27/28,O29/34)→W26 Convert164. Int→DInt Convert164/167, Add170(입력+Zero), Convert174(Coeff), Mul177, Div181(28000) 후 Move185 OutValue Int. ENO 체인 W227/230/234/237/241/245를 보존한다. 실수 연산이나 현재 기계% 식으로 바꾸지 않는다.

범위밖 >32767 Gt190 또는 ≤−1382 Le259 →OR47→W49→Move193, in W252/O218=−9999(0612 RID21 Int), out W253/O219=OutValue(0611 Local RID19). eno W21→일반 **Coil23**, operand W22/O24=Out_of_range(Local RID26). 선언 0612 RID25/29는 −1382/32767, RID17은 DInt28000이며 부호있는 SV를 사용했다. raw V의55537/4294965914를 양의 현장값으로 오독하지 않는다.

0014 LAD1659/NID2: NOT IN0 Contact171(W168/O165)→W172→Move162, in W169/O166 Int0(0612 RID23)→out W170/O167 OutValue. 이 네트워크 자체에 별도 알람 Reset Coil은 없다.

ZT05 후보 호출 결과는 0515 W24/O23의 **DB3.X25.1**, HMI Allarmi_239이다. 확인한 FC63/0515 경로에 전용 지연 타이머·S/R 래치는 없다. 전 프로그램 부재증명이나 즉시/정확한 현장 검출시간 보장은 아니다. 호출 생략·다른 쓰기·HMI 표시를 별도로 확인한다.

### 5.2 관련 소유와 복구 미확정

부모 MV05 초안의 0159 S5T#150MS/Tag_96 T15/S318/R358, 0351/0352 W31/W32 ±700은 접촉기 응답/방향명령 누적과 MV_05_FAULT DB3.X11.5에 해당한다. 이 값들을 ZT05 단선/엔코더 응답 타이머로 가져오지 않는다. 부모 제어식 전체는 공유근거이며 이번 전수 의미 재검토가 아니다.

HSC Error/ErrorID/ErrorAck/EventAck의 미결속 때문에 공통 RESET_ALLARM으로 ZT05 오류가 해제된다고 말할 수 없다. 0쓰기·HMI 알람변화·부모 Reset·실제 위치복구는 별개다. 영점 교정이나 보호값 조정을 지시하지 않는다.

## 6. 증상별 관찰 — 문서 적용, 조작 절차 아님

| 증상 | 승인된 읽기전용 관찰에서 대조할 위치 | 성급히 확정하지 말 것 |
|---|---|---|
| 위치값 고정 | 자료취득 시각·프로젝트 식별, EM_OK, raw I7.2, SW_GATE3, ACT_CNTV3, CH03/CH03_10, Pot_MV05 | 방향 Q나 접촉기 응답만으로 엔코더 정상/불량 |
| 0으로 급변 | 0515 NOT SW_GATE3 두 Move0, 0511 저장, FC63 NOT IN0, 다른 쓰기 | 닫힘완료/영점 교정 성공 |
| −9999/OFR | FC63 Int 입력·계수/Zero, DB3.X25.1·Allarmi_239 주소·시각 | 물리 단선/공통 구동고장과 동일시 |
| 종단과 위치 불일치 | LS16 raw I7.2와 처리 DB의 분리, 실제 위치·캠/장착 사진·A/B 준공 배선 | NC 도면만으로 현 정상극성 확정 |
| 전원복귀 뒤 값 변화 | Local CNT_Act_3 유효성, DB8 저장·Retain·호출순서 승인자료 | 제목 power-off만으로 위치보존 보장 |
| 센서/케이블 식별 안 맞음 | p26 ZT06A, p56 incoming ZT06/outgoing ZT05A, OEM X1/67~71, 중계함 양단 식별 | 문서 이름 하나로 실물/케이블 병합 |

관찰 필드: 관찰자·시각/시간대·설비사진·프로젝트/자료시점·값/자료형/단위·비교원본·배제결과·승인된 조치·이후 복구증거. 본 조사에서는 현재 현장 기록 수집, 강제 I/O, 배선우회, 교정/리셋 실행, 보호값 변경을 수행하거나 권고하지 않았다.

## 7. 완료·누락·다음 자료

| 영역 | 상태 | 경계 |
|---|---|---|
| 설비·자료 | 적용 | 한 ID 식별·판본/소유, 현재 실물 미확정 |
| I/O·HMI | 부분 적용 | 고유 선언·CSV 두주소, 실제 이벤트/TM 매핑 미확보 |
| 제어 | 부분 적용 | 0509/0515/0511 고유경로·FC63 대표핀, 현재 호출/유일writer 미확정 |
| 전기 | 부분 적용 | OEM4/P&ID1/시공2 실제 렌더, 상충·중계함 단자상세 미해결 |
| 알람·복구 | 부분 적용 | OFR와 부모 고장 분리, HSC진단/실제복구 미확정 |
| 증상관찰 | 문서 적용 | 관찰표만 작성, 현장/행동시험 미수행 |
| 완료기준 | 초안 complete_with_gaps | UI/게시/TIA/CPU/현장 완료 아님 |

필요 자료와 판정 기준:
1. 현 ZT05 명판·MV05 장착위치·현재 준공 P&ID: 문서 태그와 실제 장치 식별의 일치/차이.
2. 현재 기술 객체/DB18 HSC 설정과 MOD17 슬롯·CH1의 HW 식별: 도면 CH1↔소프트웨어 CH03/ACT_CNTV3 실제 대응. 이름만으로 확정하지 않음.
3. 준공 케이블·중계함 단자표와 양끝 사진: X1/67~71↔중계함↔ZT05 B/C/D/E/실드, ZT05A/06A와 FLO1TB1/2 상충 해결 근거.
4. 실제 HMI 표시/알람 이벤트 프로젝트: DB1.INT140·DB3.X25.1의 단위·읽기/쓰기·버튼·갱신 경로.
5. 현재 호출순서/추가 writer·보존설정·승인된 계수/Zero 자료와 취득시각, 적격 담당자의 실제 위치 비교/복구 기록.

새 자료가 없으면 현장 보류 유지. 부모 전체 반복조사·다른 하위 ID 집계·센서모델/보호설정 추정으로 확대하지 않는다. 도면·래더 비교의 근거는 제공했지만 앱 나란히 보기, 백업/선택복원, 기록전후 비교, 보고서/PDF UI 구현·시험은 모두 미수행이다. 원본·코드·버전·대장·운영/배포·SEJIN·다른 작업자 파일 변경 없음. 시뮬레이터 작성/수정/생성/실행/행동시험 없음.

### 실제 수행 시각

2026-10-11 UTC 13:04:35 지시/범위 확인 시작, 13:05:10~13:05:42 고유 XML/선언 파싱과 PDF 렌더, 13:05:53~13:06:41 PDF 끝점·개정/상충 시각확인, 13:06:54~13:07:19 HMI/공통환산/추가 writer 경계 확인. 마지막 해시/검사 시각은 아래 부록 및 extracts/ZT05/stages.json에 기록한다. 이 시각은 실제 도구 수행기록이며 추정 소요시간이 아니다.

## 부록 A. 선정 원본 SHA256 / 고정 Git blob 전체표

선정 27개 전부를 표시한다. 바이트 동일성은 의미 전수검토·현재 CPU 일치가 아니다. 0353은 제외 경계, 0635는 추가 Write 선언 경계만 검토했다. 공유 FC63과 부모 범위는 위 본문 한계를 따른다. 경로는 고정 저장소 기준이다.

| 원본 경로 | SHA256 | Git blob SHA1 | 고정내용 일치 |
|---|---|---|---|
| `AGENTS.md` | `0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2` | `073164bc6efd5791032d62c71b03b4dab48cb6f8` | Yes |
| `.agents/skills/gme-equipment-rollout/SKILL.md` | `fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b` | `9aa820ea6ca15b4e136c9772423b78ed4df6a3d4` | Yes |
| `docs/equipment-standard/WORK-STANDARD.md` | `05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99` | `f76a570cc73098632e08759b17934000f7e3a253` | Yes |
| `docs/equipment-standard/WORK-ITEM-TEMPLATE.md` | `4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586` | `e546f39535d2b589e80f97db869ac37ce4d05cfd` | Yes |
| `docs/equipment-standard/INVENTORY.json` | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` | `587c3748ad9224718f95ba06463fee913dae231d` | Yes |
| `all-in-one/sources/PID_1684n002I.pdf` | `2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b` | `8c83a59fefd5b8b651ec3537ea4236a073f5e109` | Yes |
| `all-in-one/sources/Electrical_Rev2.pdf` | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` | `f610fd7c7ce14ae951b00cff57b969259bfb389d` | Yes |
| `all-in-one/sources/Electrical_Can_Decoating_20241118.pdf` | `3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd` | `0ee6b6f8361c5790864dbba4bbd9d55e8e7c08f8` | Yes |
| `all-in-one/sources/hmi_plc_tags.csv` | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` | `cf4c0650e7c7baac350dcb89909b808435704880` | Yes |
| `all-in-one/sources/decoded-original/network-map.json` | `c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60` | `424430b6b953e43138e5d0a18ca40c949e21cfa1` | Yes |
| `all-in-one/sources/decoded-original/0509-FlgNet.xml` | `e1e870a86edd1878f8ba3963e984e67718be1b39255a3e3d5fc17dd61b90a5a8` | `0a41191a8e73c4e2c7d970418ca755ed3438d0a4` | Yes |
| `all-in-one/sources/decoded-original/0515-FlgNet.xml` | `504f68cf91ee6b33d6b29ab8549a013fed0d11b46212ad58f0aa377f33816ccf` | `d876759299a419e63c0b58d423e2c215ca40a146` | Yes |
| `all-in-one/sources/decoded-original/0511-FlgNet.xml` | `a4bf314bf817f0f666a0c9fdd26df134cedeed8666819c7a3e8e6438850eace6` | `2730bc98903fc1a89effa1911c5ac82ddd7b4957` | Yes |
| `all-in-one/sources/decoded-original/0353-FlgNet.xml` | `062854b25c5afacb34e53ce0ee7cd8c660cd9a0f5b79a02d8a5fbed89c794766` | `19b9493c88c95031ee327dc9e567bc7780fd4839` | Yes |
| `all-in-one/sources/decoded-original/0291-FlgNet.xml` | `fe0b92f074eba25148ce34084649af3d968962558d652727f1eea19f3e3c2550` | `1418fb2ed172c6df694a5eb8bf2dffd0b177653b` | Yes |
| `all-in-one/sources/decoded-original/0014-FlgNet.xml` | `2e814adbaac6bab99bc668bfdab74f0fc90576324d0b88728951683869cfac30` | `4d164b074fcc13a8f97da9e24382cc169ef29555` | Yes |
| `all-in-one/sources/decoded-original/0672-IdentXmlPart.xml` | `6bfc2ba142d6270c39eb1f13b2886204865af6d46eadc5f410c26981b8da9222` | `2f2790dab4bb2357733112220e0acc41edb6feb6` | Yes |
| `all-in-one/sources/decoded-original/0673-IdentXmlPart.xml` | `450ef74e2d2fb65dfbb5f6bad9e28ccacf6bf0caf64327a0e20aff84d6e40f58` | `1957bff7dd1beffcb6e2a40d6a541c1751753548` | Yes |
| `all-in-one/sources/decoded-original/0674-IdentXmlPart.xml` | `4770702f519bacda69202bb2f7733d983074bda90964360c238f990d9d08fd84` | `f210593944547b63eab10c667348711413600aab` | Yes |
| `all-in-one/sources/decoded-original/0675-IdentXmlPart.xml` | `b1902886927d8403fab736d9c8ffe73f2fbc8ce4b7ca7c345144964668b051c3` | `d82a33b173c8dc0737fd890eb2a63a88a07d0831` | Yes |
| `all-in-one/sources/decoded-original/0676-IdentXmlPart.xml` | `c58427c5b0ac6c11cdb52e4c6d0461c7b191fae81ccace191048e9f175fcec59` | `1ed67265f69796a4e659f9438e551068037f33a4` | Yes |
| `all-in-one/sources/decoded-original/0677-IdentXmlPart.xml` | `69922fcc5c67d00cdf1c5f712efa3db7638d20c88318d35fe6196467796ab1e3` | `b9437406a7e24f073ef88b8369cacc9ad4ecc5ac` | Yes |
| `all-in-one/sources/decoded-original/0678-IdentXmlPart.xml` | `51e637e0b9713c028810f2a717b5c3804a3a26c2f1be7e332a4d6bf277bfc382` | `7fafb2297bcdf739bf1d1dd68cebc0d74f2a40cc` | Yes |
| `all-in-one/sources/decoded-original/0679-IdentXmlPart.xml` | `d0fcb93e188c8ae2ae0c0423f0b78b129bf3c168e33a6855262d34b8682b9b56` | `e8d8a014609871082bf5cfca0f9ab9b78136e920` | Yes |
| `all-in-one/sources/decoded-original/0611-IdentXmlPart.xml` | `0d583915a261703954da22c176ba9f81338ad13ea2810e7cd5f7de8aa1bfa089` | `bad6b16fb32a32d47d882f48754994887457872b` | Yes |
| `all-in-one/sources/decoded-original/0612-IdentXmlPart.xml` | `95b545d4964d371ebfc107894ea90b8b1d0d7ab5d3a70e643f8ce539063c0f38` | `7cc782d33d07ef225c2104f3e7c9fbd31f7c7467` | Yes |
| `all-in-one/sources/decoded-original/0635-IdentXmlPart.xml` | `1a057d686446a3fdab7ac61bb09bc543c52f49646c9ca71ac323c10fcdffe457` | `95bfcad59cfb0c12b573e9e8face4262d1e94622` | Yes |

## 부록 B. 검사 결과

- 최종 검사 실제시각 2026-10-11T13:10:55.411050+00:00. 선정 27개 원본 fixed blob 일치, 전체 sources 712파일 및 중지5자산 fixed blob/해시 일치. Git status clean.
- XML 이름검색 695파일은 경계 탐색이며 전 네트워크 의미검토가 아니다. 고유 3네트워크 + 공통 FC 2개 대표핀, 선언/상수, HMI 두 주소, PDF7쪽 시각검토. HSC RefId 없는 ORef21개 유지.
- 7영역 구조와 원본바이트 보존 정적검사 통과. TIA/현재CPU/현장복구/시뮬레이터/생성기/앱UI/게시 검사 미수행.
- 별도 검사자료: extracts/ZT05/source-hashes.json, source-preservation-hashes.json, stopped-assets-preservation.json, static-review.json, search.json, stages.json. 원본은 그대로 보존했다.
