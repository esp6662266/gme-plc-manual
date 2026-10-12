# ZT03 — MV02 위치 계측 독립 조사 초안

- 상태: **문서화 complete_with_gaps / 원본 정적 검토 부분 완료 / 통합·게시·현장 미수행**
- 고유 ID ZT03, 계측 sensor, 부모 MV02, depth1, phase2, baseline. 대장 inventory index114이며 부모 완료를 상속하지 않는다.
- 고정 입력: `gme-research/source-mv06`, `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, v1.12.0. GME-STD-1.0.0 적용. PLC 자료는 2025-05-06 백업 유래이며 현재 CPU/실물과의 일치는 미확인이다.
- 연구 범위: ZT03 고유 위치 경로와 필요한 공통 호출·환산, 전기 양 끝점. MV02 전체 제어의 반복조사나 다른 하위 ID 완료를 포함하지 않는다.
- 시작 기록 2026-10-11 12:50:41 UTC, 원본/정적 검사 12:54:02 UTC. 단계 실제시각은 `extracts/ZT03/STAGES.json`에 보존한다. 모델명·추론수준의 런타임 증명은 미확인이다.

## 핵심 확인·상충·누락부터

1. P&ID 실제 p1은 MV-02/M16에 ZT-03을 붙인다. OEM 전기도 FG37/실제 PDF38은 **ZT-03 ENCODER**, FG145/PDF146은 **MV-02 ENCODER ZT-03**, CH1.A/B 단자11/12를 명시한다. 단지 ZT 이름이나 부모 Q주소에서 계측 종류를 유추한 것이 아니다.
2. **새 보강:** FG37의 37.1/37.2→45/1은 그대로 유효한 문서 참조다. 실제 FG45/PDF46에서 37 계열 전원선이 ZT02 B/C 분기와 접속점으로 이어지고 FG144/PDF145의 MOD16 단자9(24 VDC)/10(M)으로 연결된다. 기존 MV02 G13의 문서 연결 공백을 추가 렌더로 좁혔다. 기존 원초안 오류로 단정하거나 원문을 수정하지 않았으며, 현행 실물 공통전원·모듈 내부 동작의 증명은 아니다.
3. PLC의 직접 이름은 ZT03이 아니라 `MV02_Encoder` DB16, `fill_unit1.ACT_CNTV1` DB91.DBD156, `Memory encoder.Encoder_CH01` 계열, `Data.Pot_MV02` DB1.DBW142이다. OEM CH1과 소프트웨어 CH01 사이의 자료상 대응은 강하지만 현재 하드웨어 ID/기술 객체/실물 동일성은 여전히 미확인이다.
4. 시공 참고 p57은 ZT03을 AI/CVV-S4S로 표기한다. OEM A/B 엔코더 배선과 함께 보존하며 독립 4–20mA 채널·별도 센서를 발명하지 않는다. PLC 선정 XML/CSV 697파일에서 `ZT[-_ ]?0?3` 문자열 직접 선언은 찾지 못했다.
5. `_CH01_10`이라는 이름과 달리 원문 Div25는 **DInt 100으로 나눈다**. 이후 DInt→Int 폭 차이가 있고 FC63 정수 환산을 거친다. 현재 분해능·% 스케일·교정·오버플로 결과는 미검증이다.
6. 위치 메모리에는 닫힘단 연관 0 쓰기(0513), NOT EM_OK일 때 Local 값을 저장하는 0511, 최종 위치 DB에 OFF 조건의 별도 쓰기(0146)가 있다. 명령·리미트·위치값·저장값을 같은 상태로 합치지 않는다.
7. 고유 OFR는 DB3.DBX24.7이고 HMI 설정은 Allarmi_237이다. FC 호출의 ErrorAck 핀에는 RefId가 없으므로 다른 MV의 RESET_ALLARM 연결을 복제하지 않는다. 부모 150ms 타이머나 ±1000 명령 누적을 ZT03 측정 타이머로 배정하지 않는다.

공유근거는 [MV02 초안](MV02-DOTS-DRAFT.md) §3~6을 탐색 색인으로, [ZT01 초안](ZT01-DOTS-DRAFT.md)의 같은 고정입력 FC63 환산을 공통 설명 색인으로 재사용한다. 이번에는 0507/0513/0511/0146과 선언·호출/환산 대표핀, HMI 두 주소, PDF6쪽의 고유 위치/끝점/개정란을 원본에서 독립 대조했다. 부모 MV02의 구동·PID·접촉기 전체를 재조사한 것이 아니다. 공유문서 보존 및 추가근거 설명은 `extracts/ZT03/MV02-ZT03-POWER-SUPPLEMENT.md`에도 있다.

## 1. 설비·자료 기준

| 구분 | 근거/판정 | 미확정 경계 |
|---|---|---|
| 대장 | INVENTORY.json catalog ZT03, parent_id MV02, phase2/planned/baseline/not_assessed | 문서 작성이 실물 검증이나 BC01 동등 UI 수락을 뜻하지 않음 |
| P&ID | PID_1684n002I.pdf 실제 p1, MV-02/M16 주변 ZT-03, LS-17/18, CM-02→ATM | ZT03의 제조사·모델·단자·주소는 P&ID에 없음 |
| P&ID 개정 | 도번1684n002, INDEX I, 기본일 06/04/2011, I행15/01/2013 `REMOVED MC-05, CHANGED POWER OF FN-02` | 2013 공정자료를 2025 CPU/현재 설치와 동일하다고 하지 않음 |
| OEM 전기도 | Electrical_Rev2.pdf, FG37/45/144/145 실제 p38/46/145/146, 기본 DATA 27.05.2024, 이 네 쪽에 별도 Rev2 날짜행 없음 | 파일명 Rev2를 모든 쪽의 개정란으로 복제하지 않음 |
| 시공 참고 | Electrical_Can_Decoating_20241118.pdf 실제 p57, CANDC-CONS-C007-057, D-PAGE7, TOTAL57/64, Rev1 24.11.11 first draft design | 준공도·현재 실측자료가 아니며 원래 포함된 참고자료만 읽음 |
| PLC 근거 | decoded-original FlgNet + IdentXmlPart. 네트워크 색인은 경로 탐색에만 사용 | 같은 UID/RID라도 다른 블록 선언과 합치지 않음 |
| 소유 | ZT03 위치 계측. LS17/18은 별도 끝단 스위치, MV02는 구동/명령·고장, PSH01은 압력 계측 | 계측명으로 부모 출력 Q1.5/1.6이나 다른 계기의 원시 입력 소유를 가져오지 않음 |

### 7영역 적용

| 영역 | 상태 | 해당 절 / 경계 |
|---|---|---|
| 설비·자료 | 적용 | §1, 판본과 현행 분리 |
| IO·HMI | 적용+근거 미확보 | §2, 직접 ZT03 심볼·현행 TM 설정 없음 |
| 제어 | 적용+실행 미검증 | §3, 7개 핵심/공유 네트워크의 관련 경로 |
| 전기 끝점 | 적용 | §4, FG45 경유 보강 포함 |
| 알람·복구 | 적용+근거 미확보 | §5, OFR와 부모 고장 구분 |
| 증상관찰 | 적용 | §6, 승인된 관찰 자료 요구만 기재 |
| 완료·누락 | 적용 | §7, 실물/TIA/화면/게시 독립 상태 |

## 2. IO·HMI: 원시 신호와 처리 주소

아래 모든 XML 경로는 `all-in-one/sources/decoded-original/` 아래다. GlobalAccess SSD.AO는 비트 오프셋이며 BAD.BIRID를 **같은 블록 0674 DepDBBlock TOD.N**에 결속했다. Local InterfaceAccess는 DB주소로 환산하지 않았다.

| 신호/역할 | 선언과 정확한 위치 | 소유·해석 |
|---|---|---|
| MV02_Encoder | 0673 AufDBBlock RID332, NID45 UID23 InstanceDB, TOD.N16, Global | DB16 고속카운터 인스턴스. DB16 번호가 센서의 물리 채널 주소는 아님 |
| High_Speed_Counter | 0679 Instruction RID330, NID45 UID22, IUS FB1150 | CountValue DInt, SwGate Bool. 현재 모듈 매핑 설정 별도 필요 |
| SW_GATE1 | 0676 RID222, NID45 UID25 읽기 / NID46 UID34 쓰기·43 읽기; Global Bool AO185, BAD177→DB91 | DB91.DBX23.1 비트 쓰기. PLC 출력 Q가 아님 |
| ACT_CNTV1 | 0676 RID224, NID45 UID45 Write / NID46 UID36 Read; Global DInt AO1248, BAD177 | DB91.DBD156 실제 호출 CountValue 출력 수신 위치 |
| Encoder_CH01 | 0676 RID195, Global DInt AO32 BAD191→DB8; NID30 UID944 Write, NID46 UID35 Read/47 Write | DB8.DBD4 저장/기준 위치. 두 쓰기 경로 보존 |
| CNT_Act_1 | 0677 RID194, Local DInt AO432, NID46 UID37 Write/38 Read, NID30 UID943 Read | Local 변수. 유지·초기화·유효 시점은 정적 연결만으로 확정 불가 |
| CNTV1_100 | 0677 RID226, Local DInt AO144, NID46 UID40 Write/41 Read | Div 결과. DB91 필드로 오분류하지 않음 |
| Encoder_CH01_10 | 0676 RID228, Global Int AO304 BAD191; NID46 UID42/45 Write,49 Read | DB8.DBW38. 이름 `_10`을 나누는 수10으로 해석 금지 |
| Coeff / Zero | 0676 RID337/338, Global Int AO656/640 BAD8→DB4; NID46 UID50/51 | DB4.DBW82 / DBW80. 저장 계수 주소이며 현행 교정값 미확인 |
| Pot_MV02 | 0676 RID339, Global Int AO1136 BAD11→DB1, NID46 UID52 Write | DB1.DBW142 처리 위치. 독립 아날로그 IW 채널 선언이 아님 |
| Pot_MV02_OFR | 0676 RID434, Global Bool AO199 BAD354→DB3, NID46 UID82 Write | DB3.DBX24.7 범위오류 출력 |
| EM_OK | 0678 RID173, SimpleAccess Input Bool AO156, NID45 UID24 / NID46 UID32 / NID30 UID940 | I19.4. 일반 PLC 관찰/허가이며 안전 회로 성능 증거가 아님 |
| MV02_Close | 0678 RID444, SimpleAccess Input Bool AO60, NID46 UID56 | I7.4 원시 입력. 부모 DB13 처리 Close와 별도. 정상극성 추정 금지 |
| ON | 0678 RID1, Global Memory Bool AO0, NID46 UID48 | M0.0. 이름을 상수 TRUE로 치환하지 않음 |
| Simulation(1) | 0678 RID344, Global Memory Bool AO1440, NID45 UID75 | M180.0의 원본 반전접점만 읽음. 중지 시뮬레이터 실행·수정 없음 |

### 2.1 HMI 설정과 직접 선언의 경계

`all-in-one/sources/hmi_plc_tags.csv`:

- 261행 `data_DB1_DBW142`, 주소 `DB1,INT142`, Access Name PLC, 내부ID00285. 선언의 DB1.DBW142와 주소 대응은 확인했다.
- 15행 `Allarmi_237`, 주소 `DB3,X24.7`, Access Name PLC, 내부ID0045B. 선언의 Pot_MV02_OFR와 주소 대응은 확인했다.
- MV_02 OutputOpen/Close, LimitSwitchOpen/Close 등은 부모 상태 태그이며 위치 Int와 같지 않다. 버튼 이벤트·화면객체·경보 메시지 문구·이력 시간·통신품질·읽기/쓰기 권한은 CSV에서 입증하지 못했다.
- 695개 decoded-original XML + 이 CSV + plc-symbols.csv = 697파일에 대한 한정 문자열 검색에서 ZT03 직접 이름은 0파일. 반면 위 후보 이름은 5개 선언파일에 등장한다. 이는 검색 경계 기록이지 PLC에 센서가 없다는 증명이나 697파일 의미검토 완료가 아니다.
- 원시 카운트의 현행 PIW/IW 베이스주소, TM 기술객체 하드웨어 ID/채널 파라미터, 엔코더 종류·PPR·기어비는 현재 확보 자료에서 직접 확인하지 못했다. Pot라는 이름만으로 potentiometer나 4–20mA 입력을 만들지 않는다.

## 3. 제어 구조: 엔코더 읽기→메모리→환산

### 3.1 상위 호출

0031-FlgNet, LAD1619, main NID6: ORef271/RID52 ON→W280→Contact282. W283은 Contact282.out에서 CRef261.en 등으로 분기한다. CRef261/RID56 안 CodeBlock273/RID55는 0688 `Analog input conversion` TOD.N3(FC3)이며 0692 ON은 Memory AO0=M0.0이다. FC3 호출은 저장 원본에서 ON 정조건이다. 호출 주기·현재 CPU·다른 호출·동일 스캔 다른 쓰기는 미검증이다.

### 3.2 읽기 — 0507, LAD1757, NID45

- W48 Powerrail→Part74(in), W77 ORef75/RID344→74.operand. Part74는 **NOT Simulation(1)**.
- W76은 74.out→Part21.in, W49 ORef24/RID173=EM_OK→21.operand. W50은 21.out→LRef22.en.
- LRef22/RID330=High_Speed_Counter; Instance23/RID332=MV02_Encoder DB16. 선언 CS의 NID45/UID22·23과 대조했다.
- W51: ORef25/RID222 SW_GATE1→SwGate. W71: CountValue→ORef45/RID224 ACT_CNTV1. 이 경로가 현재 HSC 센서값 갱신 성공을 증명하는 것은 아니다.
- CaptureEnable/SyncEnable/ErrorAck/EventAck/SetCountValue 및 StatusHW/StatusGate/StatusUp/StatusDown/CompResult/SyncStatus/CaptureStatus/CapturedValue/ZeroStatus/PosOverflow/NegOverflow/Error/ErrorID/MeasuredValue/CompareMeasuredValue는 RefId 없는 ORef를 포함한다. 미결선·미사용·기본값을 정적으로 구별할 자료가 없으므로 FALSE/0/정상으로 채우지 않는다.
- 특히 ErrorAck W54→ORef28에는 RefId가 없다. 이 채널에 다른 MV의 Flag.RESET_ALLARM을 복제하지 않는다.

### 3.3 처리 — 0513, LAD1763, NID46

| 단계 | Part/Wire/ORef | 해석·주의 |
|---|---|---|
| 게이트 | EM_OK ORef32→W54→Contact21; W55→Contact22/27와 CRef30.en | 0513에는0507의 Simulation 반전 가드가 따로 없음. 호출조건을 섞지 않음 |
| Gate bit | Part22 NOT MV02_Close(ORef56/W33)→W57→Coil23; W58/ORef34 | EM_OK 뒤 반전된 원시 I7.4 조건으로 SW_GATE1 비트 쓰기. 물리 닫힘의 정상극성은 미확인 |
| 합산 | 같은 W57→Add24.en; W59 ORef35 Encoder_CH01→in1, W60 ORef36 ACT_CNTV1→in2; W62 out→ORef37 CNT_Act_1 | SrcType DInt. 보존 메모리+카운트 조합 |
| 나눗셈 | Add24.eno→W61→Div25.en; W63 CNT_Act_1→in1, W64 ORef39/RID211 literal DInt100→in2; W66→CNTV1_100 | 정수 100. 이름·단위에서 추정한 분해능 아님 |
| 폭 변경 | Div25.eno→W65→Move26.en; W67 Local CNTV1_100→in; W68 out1→ORef42 Encoder_CH01_10 | DInt에서 Int 목적지. 실제 절삭/넘침/부호 처리는 미시험 |
| Gate 비활성 경로 | Part27 NOT SW_GATE1(ORef43/W69)→W70→Move28/29 | EM_OK 가드 아래의 별도 분기 |
| 두 메모리 0 쓰기 | W71 ORef44 literal0→Move28→W72 ORef45 Encoder_CH01_10; W73 ORef46 INT#0→Move29→W74 ORef47 Encoder_CH01 | 0675 상수 및0676 목적지 확인. HSC 하드웨어 counter reset 명령으로 단정하지 않음 |
| 환산 호출 | CRef30/RID351, CodeBlock31/RID5 Signal linearization FC63(0672/0680); W75 ON→IN0 | 외부 en=EM_OK, 내부 IN0=ON 두 층 구분 |
| 환산 입력 | W76 Encoder_CH01_10→Analog_input; W77 COEFF_TRASM_MV02→Coeff; W78 ZERO_TRASM_MV02→Zero | 입력/계수/제로 Int |
| 환산 출력 | W79 OutValue→ORef52 Pot_MV02; W83 Out_of_range→ORef82 Pot_MV02_OFR | Int word와 Bool bit 별도 출력 |

### 3.4 메모리 저장의 두 번째 writer — 0511, LAD1761, NID30

원문 제목은 `store current position value at power-off`다. Part963은 NOT EM_OK, ORef940/RID173→W951, Part963.out→W964로 여러 Move.en을 병렬 허가한다. MV02 분기만 조사했다:

- W954 ORef943/RID194 **Local CNT_Act_1**→Move922.in.
- W955 Move922.out1→ORef944/RID195 **Global DB8.DBD4 Encoder_CH01**.
- 0677은 Local 변수, 0676은 Global 메모리이며 양쪽 NID30 UID943/944 일치. 정적 네트워크에는 타이머나 edge Part가 없다.

따라서 제목을 ‘전원 끄면 항상 안전하게 최신 위치 저장’으로 번역하지 않는다. 실제 전원 차단 시 실행 시간, Local 값의 유효성·초기화·갱신 순서, DB 유지 속성·재시작 복원은 미확인이다. EM_OK가 꺼져 있을 때 매 호출 영향 여부도 현재 실행환경 증거가 필요하다. 이 writer와0513의0쓰기를 모두 보존해야 한다.

### 3.5 공통 FC63 환산과 결과의 별도 writer

0291 LAD1658 NID1 / 0014 LAD1659 NID2, 선언0611/0612는 같은 고정원본의 공통 근거를 연결 재사용하고 대표 Part/Wire를 재대조했다.

- IN0 활성 경로: `Analog_input > -1382 AND Analog_input <= 32767`. Convert164/167/174는 Int→DInt, Add170→Mul177→Div181의 ENO 연쇄로 `(DInt(input)+DInt(zero))*DInt(coeff)/28000`, Move185→Int OutValue.
- 여기서 input은 DB8.DBW38의 가공된 카운트다. ZT03 원시 4–20mA/27648 채널이라고 바꾸지 않는다. 물리 스케일을 이 식만으로 정할 수 없다.
- 범위외 `>32767 OR <=-1382`는 Move193(-9999), 그리고 **Move193.eno W21→Coil23.in**으로 Out_of_range를 쓴다. OFR를 비교기 논리와 단순 등치하지 않는다.
- 0014 Part171 NOT IN0→W172→Move162(0)→W170 OutValue. 호출 EN이 false인 것과 내부 IN0가 false인 것을 합치지 않는다. 미호출 시 ‘반드시0’이라고 말할 수 없다.
- 0146 LAD396 `for test trends`, NID1은 OFF(M0.1,0039 RID1 UID73) Contact92→W93→Add61 및Gt67.pre. W82/83은 Data.Pot_MV02+1, W84는 같은 word 출력. Pot_MV02>100일 때 Move70 literal0→W90 같은 word. 0040 Data DB1,0041 RID5 AO1136 UID74/76/77/80,0042 literal1/100/0을 직접 대조했다. **같은 DB1.DBW142의 별도 writer**이며 실행/시험하지 않았다. 제목으로 활성 여부를 판단하지 않는다.

## 4. 전기 전달 경로·페이지·개정

아래는 실제 PDF를 새로 렌더해 본 결과다. 각 쪽의 표제/개정란도 확인했다. E/A는 도면 표기이며 PLC I/Q와 구분한다.

### 4.1 ZT03 신호 양 끝점

| 시작 | 경유 | 끝점 | 직접 원본 |
|---|---|---|---|
| ZT-03 D | X1:78 →37.3,145/3 | CPU515 MOD16 terminal11 CH1.A | FG37/PDF38 ↔ FG145/PDF146 |
| ZT-03 E | X1:79 →37.4,145/3 | 같은 MOD16 terminal12 CH1.B | 같은 두 페이지 |
| ZT-03 실드 | X1:80→37SCH1,145/3 | FG145 실드/접지 기호 | 같은 두 페이지; 양 끝 실제 접지 방식 미확인 |
| CH1.N | terminal13 표기 | 37계열 입력선 연결 없음 | FG145/PDF146만의 관찰. 실물 미사용 확정 아님 |

FG145 표제는 `TECNOLOGY MODULE TM TIMER`, 채널 설명은 `MODULATION VALVE MV-02 ENCODER ZT-03`이다. 모델/상품번호·전기신호 규격·PPR은 이 표기만으로 확정하지 않는다. 주변 SPARE A8.2/A8.3/E20.3~E20.5를 ZT03 고유 I/O로 추가하지 않는다.

### 4.2 새로 좁힌 전원 참조 — FG45 경유

1. FG37/PDF38: ZT03 B(+24Vdc)→X1:76→37.1→**45/1**, C(-0Vdc)→X1:77→37.2→**45/1**. 인쇄된45/1을145/1로 수정하지 않는다.
2. FG45/PDF46: 하단 37.1/37.2가 왼쪽 `37/2` 참조에서 들어와 오른쪽 `144/5`로 이어진다. 그림상 접속점은 각각 ZT02 B→X1:107, C→X1:108의 수직선과 연결된다. ZT02 자체 신호 채널을 ZT03 소유로 조사·완료한 것은 아니다.
3. FG144/PDF145: 37.1(참조45/3)→CPU515 MOD16 **terminal9 24 VDC**, 37.2(45/3)→**terminal10 M**. 이것으로 문서상 전원 도선의 끝점을 연결했다.
4. FG145/PDF146의 모듈 공급은 별도: +24Vdc10.7→X21:3040/5×20 2A IST→145.1→terminal41 L+; -0Vdc10.6→terminal44 M. 9/10과41/44의 모듈 내부 관계는 외부도면만으로 확정하지 않는다.

이 확인은 기존 MV02 초안의 ‘전원 끝점 추적 미완료’에 대한 **추가근거 보강**이다. 기존 문서/원본을 수정하지 않았고 현장 도통/전압/공유 전원 정상성은 입증하지 않았다. FG45·144를 관련 두 쪽으로 한정하여 확인했다.

### 4.3 별도 리미트와 시공 참고 상충

- FG37 LS17 경로 +24Vdc10.7→X1:81(2A F5×20)→LS17 접점11–12→X1:82→E7.3(123/4). LS18은X1:83→LS18 11–12→X1:84→E7.4(123/5). 이는 ZT03 A/B 측정선과 별도이며 두 LS의 별도 완료로 집계하지 않는다. 접점 기호를 정상극성 증명으로 사용하지 않는다.
- 시공 p57 행7_6: `=FLA+HE01-FLO2TB1F`, FROM CR→TO HE-01/FLO2TB1, DESCRIPTION ZT03, AI, CVV-S,4S,1.0,spare0, route100→110 LAD1→E100, Adjustment5, LEN50.
- 같은 p57 행7_13: `=FLA+MV02-ZT03A`, FROM HE-01/FLO2TB1→MV-02/ZT-03, AI,CVV-S,4S,1.0,spare0, route LAD1 E400→LAD1→E700, Adjustment12,LEN12.
- AI라는 분류·케이블 표만으로 아날로그 센서나 독립 IW 주소를 정하지 않는다. 승인 결선도/케이블표/현장 명판·단자사진이 있어야 OEM A/B 엔코더 경로와 현재 연결을 판정할 수 있다. 길이도 설계 수치이며 실측값이 아니다.

## 5. 알람·타이머·복구 경계

| 항목 | 확인 내용 | ZT03에 대해 하지 않는 결론 |
|---|---|---|
| 고유 위치 범위 오류 | 0513 CRef30.Out_of_range→W83→ORef82/RID434→DB3.DBX24.7, HMI Allarmi_237 | 현재 장애·확정 문구·안전 트립이라고 단정하지 않음 |
| 함수 내부 OFR | 0291 Coil23, Move193 ENO 경로. SCoil/RCoil 아님 | 공통 ACK/Reset만으로 원인 해소·재시작이 보장된다고 하지 않음 |
| HSC 진단/해제 | 0507 Error/ErrorID 등 RefId 없는 출력, ErrorAck도RefId 없음 | 진단정상, 오류없음, 자동해제 또는 RESET_ALLARM 직결이라고 채우지 않음 |
| 전용 타이머 | 고유 읽기0507·처리0513·저장0511에 Timer/SdCoil Part 없음 | 정적 파일 범위의 부재일 뿐 전체 PLC의 ‘ZT03 타이머 없음’을 증명하지 않음 |
| 부모 고장/타이머 | MV02 초안의 LAD1226/0159 Tag93 T21 S5T#150MS 및1714 명령누적±1000은 구동 명령/접촉기 관련 공유 인덱스 | ZT03의 주기·지연·PPR·실제 이동시간으로 전용하지 않음; 이번 타이머 의미 재검토/전체 복제 안 함 |
| 메모리 초기화 | 0513 0 쓰기,0511 Local 저장,0146 위치word 별도 쓰기 | 실제 센서 교정·카운터 HW Reset·현장복구 완료와 구별 |

원인 제거, OFR 해제, HSC 진단, HMI 갱신, 실제 기계 위치 일치, 정상 재요청 후 재발 여부는 서로 다른 확인 항목이다. 확인되지 않은 제조사 복구 절차나 보호값 조정을 제안하지 않는다. 현재 ZT03 전용 교정/ResetEncoderProcedure는 이 한정검색 및 부모색인에서 확보되지 않았다. MV01/MV03용 교정 네트워크를 복제하지 않는다.

## 6. 증상별 관찰·자료 요청

아래는 읽기 전용 관찰 항목안이다. 실제 시험·현장 조작 지시나 가공된 관측값이 아니다.

| 증상 | 비교할 관찰 위치 | 원인 배제를 위한 근거/추가 자료 |
|---|---|---|
| 표시 위치가 멈춤 | HMI data_DB1_DBW142, DB1.DBW142, DB8.DBW38, ACT_CNTV1, SW_GATE1, EM_OK, ON, M180.0의 승인된 같은시각 값 | 호출 미실행·게이트·원시값 정지·환산·HMI 갱신을 단계별 분리. 현재 CPU 교차참조와 TM 진단 필요 |
| 닫힘 부근에서0 또는 점프 | 원시 I7.4, DB13 처리 Close, SW_GATE1, DB8.DBD4/DBW38, 두 writer 시간순서 | 0513 반전 조건과0쓰기를 비교. ‘닫힘=1’ 가정 금지. 정상 접점표/기계위치 증거 필요 |
| 재기동 뒤 위치가 다름 | 0511 직전 CNT_Act_1와 DB8.DBD4, 현재 DB 유지 속성·기동 기록 | Local값 유효성, EM_OK 변동, 저장/처리 순서. 현재값 없이 power-off 저장 성공 주장 금지 |
| OFR 또는 -9999 | DB8.DBW38와 Coeff/Zero, DB1.DBW142, DB3.DBX24.7, HMI 표시 시간 | 0291 범위/ENO, 형식 폭 차이, 다른writer를 구분. 현행 교정성적서 및 원본 프로젝트 필요 |
| 모터 이동과 위치표시 불일치 | 부모 방향명령/접촉기 응답, LS17/18, ZT03 위치값을 각각 기록 | 명령=이동=실제위치라는 가정 배제. 현장 명판·기계결합/케이블·엔코더 규격 자료 필요 |
| 전원 관련 의심 | FG37→45→144 단자문서, FG14541/44 모듈 공급과 진단자료 | 그림의 공유 분기와 실제 전압/도통을 구별. 자격자 승인 절차로 수집된 측정자료만 사용 |

기록 필수: 관찰자·실제 날짜/시각/시간대·대상 ZT03·관찰점/값/단위/품질·수집 방법·현재CPU/백업 식별·원본 비교·배제 결과·승인된 조치·전후 차이·복구 증거. 공개 원본에 운영기록/사진/SEJIN 자료를 복제하지 않는다.

## 7. 완료·누락·검증

### 7.1 남은 자료와 판정 기준

| ID | 누락·상충 | 다음 필요한 자료/판정 |
|---|---|---|
| ZT03-G01 | P&ID/OEM ZT03와현재TM/DB16 동일성 | 현행 TIA 하드웨어·기술객체/채널 할당·명판/승인 결선도. 이름/CH번호만으로 병합 금지 |
| ZT03-G02 | 시공AI 대 OEM A/B 엔코더 | 현행 승인 케이블표·센서규격·단자 양끝 사진. 어느 판본이 실제인지 판정 |
| ZT03-G03 | 전원 경유 문서는 연결됨, 현장·내부모듈 관계 미확인 | FG37→45→144 및14541/44를 보존하고 현행 문서와 대조. ‘전원 공백 해결’은 문서 범위만 |
| ZT03-G04 | PPR/기어비/방향/영점/스트로크·%단위 | 제조사 해당 모델 원문과 승인 교정자료. 저장coeff/zero를 조정 권장값으로 쓰지 않음 |
| ZT03-G05 | Local DInt→Global Int와복수writer | 현재 전체 교차참조·실제 호출/스캔·보존 속성. 0511·0513·0146 실행 우선순위 확인 |
| ZT03-G06 | HSC 오류/해제핀,전용교정·복구 | 현행 FB1150/DB16 파라미터·진단·교정절차. 빈 RefId를FALSE로 보완하지 않음 |
| ZT03-G07 | HMI 설정주소만 확인 | 실제 HMI 프로젝트의 객체·이벤트·알람문구·통신·권한. 표시태그→현장 복구 판정 금지 |
| ZT03-G08 | 현재CPU/현장자료 없음 | 현행 프로젝트 및 승인된 관찰자료가 올 때만 재검토. 새자료 없는 반복전검색 안 함 |

### 7.2 이번 수행 검사

- 원본 고정 커밋/버전과 Git clean 확인. 선택48파일의 SHA256, Git blob ID, 고정 커밋 blob 바이트 전부 일치. 중지5자산은 simulator-freeze의 기존SHA에도 일치. 중지자산은 보존 해시만 계산하고 실행/분석 소스로 사용하지 않았다.
- 의미검토 범위는 7개 네트워크의 이 문서에 적은 관련 경로와 선언/원본 PDF6쪽이다. **48해시=48전체 의미검토, 697검색=697완전분석이 아니다.** 부모 전체 네트워크·모든 호출·모든 writer 완전성을 주장하지 않는다.
- 자체 읽기 전용 XML 파싱 검사12개 통과: 음극성4, HSC CountValue/환산 ENO/OFR/저장/호출 Wire 등을 확인. 상세 `extracts/ZT03/VALIDATION.json`, `NETWORK-TRACES.json`, `DECLARATIONS.json`, `SEARCH.json`.
- 자체 PDF 렌더: Electrical p38/46/145/146, 시공p57, P&IDp1. P&ID 페이지 전체 및 MV02/표제 확대 확인. PDF 변환은 문서 관찰용이며 보고서 기능의 UI/PDF 검증은 아니다.
- 시뮬레이터 작성·수정·생성·실행·행동시험0, PLC/현장/보호값/SEJIN 변경0. 원본 build/test/generator 실행0, TIA접근0, 재위임0. 로컬 통합·공유대장·게시 수정0.

### 7.3 네 기능·상태 분리

| 기능/상태 | 결과 |
|---|---|
| 도면·래더 비교 | FG37/145↔0507/0513, FG45/144 전원보강 근거 준비. UI 통합/강조 미검증 |
| 백업·선택복원 | 안정 ID ZT03 유지, 기존 note/repair_observation/미지 필드/다른설비/초안/저장키 변경0. 기능 시험 안 함 |
| 전후 비교 | §6 기록 항목만 준비. 실제 사용자 기록 생성·수정/합성시험0 |
| 보고서/PDF | 이 MD와 원본 렌더만. 제품 보고서/A4 출력 기능 미구현·미검증 |
| documentation | complete_with_gaps, 독립검토·부모 첨부 전 초안 |
| static_review | partial_original_checked, 자체 원본검사12통과. 제품정적검사/BC01 회귀 안 함 |
| ui_records / publication | not_run / not_published |
| tia_compile / live_cpu / field_recovery | 모두 not_performed |

다음 한 단계: 부모의 독립 문서검토와 ZT03 초안 첨부. MV02 원초안은 그대로 두고 전원 연결 보강자료를 필요한 통합 담당에게 별도 전달한다. 실물 보류는 필요한 새 자료가 도착할 때만 재개한다.

## 부록 A. 선정 원본 SHA256 / 고정 Git blob 전체표

고정 커밋 `abcf31c5030bc7ef8749ed8e869a857f2387a28a` 상대경로다. 선택48파일 전부의 해시/바이트 일치 표이며, 중지5개는 보존 확인용으로만 포함했다. SHA256/Git blob 일치는 현재CPU나현장검증이 아니다.

| 고정 원본 상대경로 | SHA256 | Git blob | 바이트 일치 |
|---|---|---|---|
| `.agents/skills/gme-equipment-rollout/SKILL.md` | `fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b` | `9aa820ea6ca15b4e136c9772423b78ed4df6a3d4` | 일치 |
| `AGENTS.md` | `0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2` | `073164bc6efd5791032d62c71b03b4dab48cb6f8` | 일치 |
| `EXPANSION-WORK.md` | `ec624de9fd2fcfac861a67fd5e828b25ef46db50bfd7a37ff16e2cb54cd0f7e2` | `4c42d88ecc2d48269eb23e13a20ebf3721a092a1` | 일치 |
| `PUBLICATION_STATUS.md` | `efe4857aec598d90470322cf3962eb3fe1f64947630e1fdf71d1c90134de8740` | `d76401cf291fc0be681acc51fa898ad3ce46ff78` | 일치 |
| `VERSION.json` | `5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7` | `fffb51663b7705aec91cb119ca80ee943a4ce758` | 일치 |
| `WORKSPACE-HANDOFF.md` | `215096d997782e78e901dfae36c782937e49611fbeb677a0d3fa50cbecf8d074` | `dd0b8989d2376c4415bba9bd826fe6754c6b1a12` | 일치 |
| `all-in-one/ACTIVE-WORK.md` | `eff3bbc08ecff41da3beff77f3fec48e7d148708192bcaaab00f34b6a721afc2` | `6eb947c629b5ddf9c759ef87649451303938864b` | 일치 |
| `all-in-one/assets/program-model-data.js` | `52f8199371e3399b7c0d44ab5469f0472aced79d56bbef2887f7625f5d2aff0f` | `38f34b0caa380a16ccad6f6f1e234a2fdf23f327` | 일치 |
| `all-in-one/assets/simulator-workspace.js` | `3a6dfc618ff7e7b238f2671dc85d65704f33093a18eac879d86081d92c31e8bc` | `97c2c831c77a9699fff0e0960b3bc1b7d93d45b3` | 일치 |
| `all-in-one/assets/virtual-plc.js` | `5f1876052dc0067b1f010af0dfc941946e37003167481731293615d9c1c36dbc` | `0bd9eceb54365a91214a37c5601b5067c39a3f75` | 일치 |
| `all-in-one/registers/plc-symbols.csv` | `a0334b390f06ddb515d6c09ca96a01d35d44029c1b726ef0ff53303ec04ff91f` | `cbc576c5d6e47498a3865304a1c23de9b4641d9f` | 일치 |
| `all-in-one/registers/program-model.json` | `6203479c086b15bada12ac9d7e37db9280234ec26f1ea6091d7211dc09a577c5` | `9860b10f008d3a5ae714be50d77b703dfec32f3a` | 일치 |
| `all-in-one/registers/simulator-freeze.json` | `bb93c1994effc5609939ba566b7802ce7ed55154a7310f02379b308ac2c8c835` | `808ffac14dbd1b4a7d797fa6cd0d647635d90b47` | 일치 |
| `all-in-one/registers/virtual-plc-test-results.json` | `a6b389f797f9a8b5ffe6928b8420f55c4cc459a327b0b48d716079d2eca6dd64` | `757dd50e45184568facb8ff62900b39d3ce848d1` | 일치 |
| `all-in-one/sources/Electrical_Can_Decoating_20241118.pdf` | `3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd` | `0ee6b6f8361c5790864dbba4bbd9d55e8e7c08f8` | 일치 |
| `all-in-one/sources/Electrical_Rev2.pdf` | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` | `f610fd7c7ce14ae951b00cff57b969259bfb389d` | 일치 |
| `all-in-one/sources/PID_1684n002I.pdf` | `2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b` | `8c83a59fefd5b8b651ec3537ea4236a073f5e109` | 일치 |
| `all-in-one/sources/decoded-original/0014-FlgNet.xml` | `2e814adbaac6bab99bc668bfdab74f0fc90576324d0b88728951683869cfac30` | `4d164b074fcc13a8f97da9e24382cc169ef29555` | 일치 |
| `all-in-one/sources/decoded-original/0031-FlgNet.xml` | `76385eab8f8f72b9faa16f7cf8905f395591b18c0a9ee9e6d7dd085a38c45c65` | `653d27572de6beedcf3eb6c95702bb119a8b567f` | 일치 |
| `all-in-one/sources/decoded-original/0039-IdentXmlPart.xml` | `3ae955e5079c7e2f14f98035cffec43763714a9aa62d3b1defe86164aeb43486` | `00d088df9d43e85d53c2d4feab5b0364399642ae` | 일치 |
| `all-in-one/sources/decoded-original/0040-IdentXmlPart.xml` | `4aa4f09101f827918ca2af003544aa0de8a70410cc4d69e738f2d6220669f182` | `dde9014e48da7a32dbb0cf9523dbdb6afcfd0bb3` | 일치 |
| `all-in-one/sources/decoded-original/0041-IdentXmlPart.xml` | `f6879784dcb83569b01753a2986e4db4ddb411f64580d1e72c22c114dcdaae15` | `80b12f3b9be6cb015dacff8fc852ee4476768c0c` | 일치 |
| `all-in-one/sources/decoded-original/0042-IdentXmlPart.xml` | `39a10a59ac8afcda3d1729f6b07dccea38c00227605c43cac46853fdc3e1b5e2` | `62cfa50ff1c308189542b805e9797f2294097407` | 일치 |
| `all-in-one/sources/decoded-original/0146-FlgNet.xml` | `c01421db51d744b648eeb19953a93b9d09bc6ea8eb8615ba5862be8220b08c75` | `c9e197bafee0d047b1924b1190f84598b1b568fb` | 일치 |
| `all-in-one/sources/decoded-original/0291-FlgNet.xml` | `fe0b92f074eba25148ce34084649af3d968962558d652727f1eea19f3e3c2550` | `1418fb2ed172c6df694a5eb8bf2dffd0b177653b` | 일치 |
| `all-in-one/sources/decoded-original/0507-FlgNet.xml` | `c73e066c3ff24d3a367b4f7e3b41b762747a6b3cb76f949ca1fea375392a8c02` | `c78b6887d049ece10a960bb12b00667745944ca2` | 일치 |
| `all-in-one/sources/decoded-original/0511-FlgNet.xml` | `a4bf314bf817f0f666a0c9fdd26df134cedeed8666819c7a3e8e6438850eace6` | `2730bc98903fc1a89effa1911c5ac82ddd7b4957` | 일치 |
| `all-in-one/sources/decoded-original/0513-FlgNet.xml` | `19107ffbb3144f4dc5dd070f0edb459166ae7a96c0715b65362f9a359c19412d` | `42f9e21fdcc81ed3664bb2c5421a3b7f6108f89f` | 일치 |
| `all-in-one/sources/decoded-original/0611-IdentXmlPart.xml` | `0d583915a261703954da22c176ba9f81338ad13ea2810e7cd5f7de8aa1bfa089` | `bad6b16fb32a32d47d882f48754994887457872b` | 일치 |
| `all-in-one/sources/decoded-original/0612-IdentXmlPart.xml` | `95b545d4964d371ebfc107894ea90b8b1d0d7ab5d3a70e643f8ce539063c0f38` | `7cc782d33d07ef225c2104f3e7c9fbd31f7c7467` | 일치 |
| `all-in-one/sources/decoded-original/0635-IdentXmlPart.xml` | `1a057d686446a3fdab7ac61bb09bc543c52f49646c9ca71ac323c10fcdffe457` | `95bfcad59cfb0c12b573e9e8face4262d1e94622` | 일치 |
| `all-in-one/sources/decoded-original/0672-IdentXmlPart.xml` | `6bfc2ba142d6270c39eb1f13b2886204865af6d46eadc5f410c26981b8da9222` | `2f2790dab4bb2357733112220e0acc41edb6feb6` | 일치 |
| `all-in-one/sources/decoded-original/0673-IdentXmlPart.xml` | `450ef74e2d2fb65dfbb5f6bad9e28ccacf6bf0caf64327a0e20aff84d6e40f58` | `1957bff7dd1beffcb6e2a40d6a541c1751753548` | 일치 |
| `all-in-one/sources/decoded-original/0674-IdentXmlPart.xml` | `4770702f519bacda69202bb2f7733d983074bda90964360c238f990d9d08fd84` | `f210593944547b63eab10c667348711413600aab` | 일치 |
| `all-in-one/sources/decoded-original/0675-IdentXmlPart.xml` | `b1902886927d8403fab736d9c8ffe73f2fbc8ce4b7ca7c345144964668b051c3` | `d82a33b173c8dc0737fd890eb2a63a88a07d0831` | 일치 |
| `all-in-one/sources/decoded-original/0676-IdentXmlPart.xml` | `c58427c5b0ac6c11cdb52e4c6d0461c7b191fae81ccace191048e9f175fcec59` | `1ed67265f69796a4e659f9438e551068037f33a4` | 일치 |
| `all-in-one/sources/decoded-original/0677-IdentXmlPart.xml` | `69922fcc5c67d00cdf1c5f712efa3db7638d20c88318d35fe6196467796ab1e3` | `b9437406a7e24f073ef88b8369cacc9ad4ecc5ac` | 일치 |
| `all-in-one/sources/decoded-original/0678-IdentXmlPart.xml` | `51e637e0b9713c028810f2a717b5c3804a3a26c2f1be7e332a4d6bf277bfc382` | `7fafb2297bcdf739bf1d1dd68cebc0d74f2a40cc` | 일치 |
| `all-in-one/sources/decoded-original/0679-IdentXmlPart.xml` | `d0fcb93e188c8ae2ae0c0423f0b78b129bf3c168e33a6855262d34b8682b9b56` | `e8d8a014609871082bf5cfca0f9ab9b78136e920` | 일치 |
| `all-in-one/sources/decoded-original/0680-IdentXmlPart.xml` | `fd551ad5d47bbd66c6bcdcc1949aaddf68cc086a3ddf6fb337adc767954c2b95` | `c9049ced1eaed72c5e251a88601d46ddec8c3e50` | 일치 |
| `all-in-one/sources/decoded-original/0688-IdentXmlPart.xml` | `ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda` | `463585759f1ecd94f32362b4fefb000a152f5773` | 일치 |
| `all-in-one/sources/decoded-original/0692-IdentXmlPart.xml` | `bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037` | `737785d03b5fad43c5b4d451955726d800edb1c0` | 일치 |
| `all-in-one/sources/decoded-original/0694-IdentXmlPart.xml` | `757ccebdf32d0a168dd787bfa735fe6494eac4c4a9f7a5adc63898a88e8b152d` | `c45e8f3ca4129dc06734f6a12ef79e6ed6528a7d` | 일치 |
| `all-in-one/sources/decoded-original/network-map.json` | `c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60` | `424430b6b953e43138e5d0a18ca40c949e21cfa1` | 일치 |
| `all-in-one/sources/hmi_plc_tags.csv` | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` | `cf4c0650e7c7baac350dcb89909b808435704880` | 일치 |
| `docs/equipment-standard/INVENTORY.json` | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` | `587c3748ad9224718f95ba06463fee913dae231d` | 일치 |
| `docs/equipment-standard/WORK-ITEM-TEMPLATE.md` | `4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586` | `e546f39535d2b589e80f97db869ac37ce4d05cfd` | 일치 |
| `docs/equipment-standard/WORK-STANDARD.md` | `05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99` | `f76a570cc73098632e08759b17934000f7e3a253` | 일치 |
