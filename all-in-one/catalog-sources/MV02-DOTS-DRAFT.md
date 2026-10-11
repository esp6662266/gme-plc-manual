# MV02 독립 원본 조사 초안

- 문서 상태: **cloud 조사 초안, 문서화 complete_with_gaps / 통합·게시 미수행**
- 작성일: 2026-10-11 UTC. 표준: GME-STD-1.0.0.
- 대상: MV02, 모터 구동 밸브, motorvalve, 제어 밸브, 부모 없음. 우선23행의 priority_key 없음. 전체248 ID 대장의 고유 ID로 한 번만 조사한다.
- 고정 원본: `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, 프로그램 v1.12.0. 저장소 `https://github.com/esp6662266/gme-plc-manual`.
- 작업표준의 phase2 표기는 대장 분류다. 이번 산출물은 사용자가 승인한 첫5개 병렬 cloud 조사 중 MV02만이며, 로컬 목표의 133후보 통합·게시 범위를 늘리지 않는다.
- 변경 파일: 이 초안과 `gme-research/extracts/MV02/`의 읽기 전용 추출·도면 렌더·검증 자료만. 원본 저장소, 공통 코드/버전/대장/배포/운영기록 변경 없음.
- 자료시점: PLC 백업 GME_20250506.zap18 / decoded-original, 전기도면 Electrical_Rev2.pdf, P&ID PID_1684n002I.pdf, 시공 참고 Electrical_Can_Decoating_20241118.pdf. 현재 CPU·현장과 동일하다는 증거는 없다.
- 실행 모델/추론 수준: 이 조사 실행에서 모델명·실제 UI 설정은 관측하지 못했으므로 미확인. 지정 표준을 실제 실행 설정으로 기록하지 않는다.

## 0. 먼저 전달할 결론

1. MV02의 전용 구동기는 M16이며, 공유 인버터 30AS1은 MV02/MV05/MV06의 공통 전원이다. 전용 접촉기·리미트·엔코더까지 독립 확인했다. 다른 MV의 모터 정격·타이머·리미트·교정회로를 복제하지 않았다.
2. **LAD1704에는 ON(%M0.0)의 반전 접점이 실제로 있다.** main LAD1621은 같은 ON의 정접점으로 Valve Control loop를 호출한다. 이 호출 경로와 내부 반전은 중요한 원본 검토 경계다. 현재 실행 경로·다른 호출·온라인 값을 모르는 상태에서 삭제, 상시 정지, 정상 동작으로 단정하지 않는다.
3. MV02 명령/응답 불일치 알람은 LAD1226의 Tag_93(%T21), **S5T#150MS**이다. LAD1714의 명령 누적감시는 W35 > 1000 / W36 < -1000으로 별도다. 이를 150초 또는 실제 1000초 타임아웃으로 바꾸지 않는다.
4. `MV_02\OutputOpen/Close`는 HMI 설정 주소명이며 실제 Q1.5/Q1.6 명령과 같은 신호라고 증명되지 않았다. HMI LAD1189는 CRef와 14개 피연산자 UID/RID의 직접 선언 결속이 미완료다.
5. PID 제목은 PC01이지만 실제 계측 원문은 PSH01(%IW284:P) → Data.Press_PC01이다. PC01이라는 제목만 보고 다른 압력 채널을 연결하지 않는다.
6. 엔코더는 ZT03, TM의 CH1.A/B, 소프트웨어 `fill_unit1.ACT_CNTV1` / MV02_Encoder(DB16) 경로다. 전용 MV02 교정 네트워크는 이번 원본 검색에서 확보되지 않았다. 다른 MV의 ResetEncoderProcedure를 배정하지 않는다.

## 1. 7영역 적용표

| 영역 | 상태 | 이 초안의 위치 | 누락·경계 |
|---|---|---|---|
| 설비·자료 기준 | 적용 | §2 | M16/공유30AS1/LS17·18/ZT03/PSH01 소유 구분. 실물·현행 도면 미확인 |
| I/O·HMI | 적용 + 일부 근거 미확보 | §3 | 물리 I/O·DB13 처리·DB2 요청·HMI DB11 분리. HMI 호출 선언 및 실제 버튼 이벤트 미결속 |
| 제어 구조 | 적용 + 실행 미검증 | §4 | 요청→조건→방향 출력, ON 반전·호출, 펄스, 엔코더, PID. 현재 호출·쓰기 우선순위 미확인 |
| 전기 전달 경로 | 적용 | §5 | 공유 인버터·전용 모터·DO/DI·리미트·엔코더·PSH01의 도면 양 끝점. 현행 제조사·보호 설정 미확인 |
| 알람·복구 | 적용 + 일부 근거 미확보 | §6 | 150ms 불일치, ±1000 명령 누적, OFR, 공유 인버터 경계. 실제 복구·재기동 미검증 |
| 증상별 수리 | 적용 | §7 | 관찰 위치·비교·배제·필요 자료. 강제 출력/보호 우회/현장 조치 수행 없음 |
| 완료 기준 | 적용 | §8~10 | 문서/정적/UI/게시/TIA/현재CPU/현장복구를 분리 |

## 2. 설비·자료·소유 범위

### 2.1 대장 중복과 하위 항목

`docs/equipment-standard/INVENTORY.json`에서 MV02는 phase2, depth0, parent_id=null, priority_key=null, planned, existing_detail=specialist이다. 기존 specialist 자료는 문서 탐색 시작점이며 BC01 표준 수락 완료를 의미하지 않는다. 대조표의 MV02 고유 행을 유지한다. 하위 ZT03·LS17·LS18은 각각 별도 고유 대장 항목이다. 이번 MV02 문서에 연결 근거를 쓰는 것과 이 하위 항목의 별도 문서를 완료하는 것을 합산하지 않는다. 기존 제외 MV04와 그 하위 범위는 재개하지 않는다.

### 2.2 실제 원본의 역할

- P&ID 1쪽을 실제 렌더해 MV-02, M16, LS-17, LS-18, ZT-03, PSH-01을 확인했다. MV02는 HE01 주변 경로에서 CM-02/ATM으로 향하는 분기에 있다. 도면의 `SetPoint=+2÷+5mBar`, `0.75 kW 440V`는 참고 설계 표기이며 현재 운전 설정·안전 허용 범위가 아니다.
- Electrical FG36/PDF37에서 M16 MV-02, 0.75 kW, 1.67 A; 36QM1 범위 1.4–2 A가 표시된다. 현행 명판·실제 설정값은 미확인이다.
- 30AS1 인버터와 30QM1·31KA1은 공유 전원/명령 경로다. MV02 전용은 FG36의 36QM1, 36KM1/2, 36QS1과 M16이다.
- LS17/18은 물리 종단 위치 회로, 36KM1/2의 보조접점은 방향 접촉기 응답이다. 어느 하나를 다른 하나의 실물 위치 증거로 바꾸지 않는다.
- PSH01은 압력 계측·PID 경로이며 ZT03은 MV02 위치 엔코더다. 다른 센서이므로 주소/단위/장애를 합치지 않는다.
- 시공 PDF의 제목란은 Rev1, 24.11.11, first draft design. 승인 시공도나 현장 준공 증거가 아니다. 이 파일을 읽은 것은 공개 작업 원본의 참고자료 조사이며 SEJIN 운영 기록·프로그램·사진/이력을 변경하거나 복제한 작업이 아니다.

### 2.3 근거 등급

- 직접 원본: decoded-original의 FlgNet/IdentXmlPart, 원본 PDF의 실제 렌더.
- 원본 검색색인/설정 추출: live_index.json, hmi_plc_tags.csv. 현재 컴파일 결과나 온라인 값은 아니다.
- 파생 탐색: network-map.json, control-spec.json, encoder-position.json, regulation-manual.json 및 기존 대장. 핵심 논리는 직접 Part/Wire/ORef 및 선언으로 재대조했다.
- field_verified / tia_verified: 이번 조사에서 false, not_performed.

## 3. I/O·메모리·HMI

### 3.1 물리/처리/요청 주소

| 구분 | 원문 신호 | 백업/도면 주소 | 직접 근거 및 해석 |
|---|---|---|---|
| 방향 출력 | Open MV02 | Q1.5 | 0343 ORef259/RID25, 0617 SimpleAccess Output AO13, Coil227/W295. FG137/PDF138 단자16 → FG36/PDF37 A1.5 |
| 방향 출력 | Close MV02 | Q1.6 | 0343 ORef267/RID24, 0617 Output AO14, Coil240/W307. FG137 단자17 → FG36 A1.6 |
| 공통 출력 | Start Aux INV | Q1.0 | SimpleAccess Output AO8; FG137 단자11 → FG31/PDF32 A1.0. MV02 전용 명령으로 소유권 축소 금지 |
| 접촉기 원시 입력 | mv02_fbk_opening / closing | I2.2 / I2.3 | 심볼색인499/882 및 FG36의 KM1/KM2 13–14 → FG118/PDF119 단자23/24 |
| 처리 응답 | Inputs.MV02 RUN_Opening / RUN_Closing | DB13.DBX2.2 / 2.3 | 0573 RID61/62 SSD AO18/19, 0572 Inputs TOD N13. 원시 입력과 별도 메모리 위치 |
| 리미트 원시 입력 | mv02_open / mv02_close | I7.3 / I7.4 | 심볼색인659/1514. FG37 LS17/18 → E7.3/7.4 → FG123/PDF124 단자34/35 |
| 리미트 처리 입력 | Inputs.MV02 Open / Close | DB13.DBX7.3 / 7.4 | 0619 RID169/170 SSD AO59/60, 0618의 Inputs DB13 결속. 원시 입력의 정상극성과 현재 전달은 별도 확인 |
| 엔코더 원점 처리의 원시 접점 | MV02_Close | I7.4 | 0513 ORef56/RID444; 0678 SimpleAccess Input AO60. 위 DB13 처리 Close와 구별 |
| 공유 공급 응답/알람 | mv02_05_06_power_ok / mv02_05_06_inv_all | I1.4 / I1.5 | 심볼색인494/915; FG30 E1.4/E1.5 → FG117/PDF118 단자15/16. 공통 인버터 소유 |
| 자동 요청 | Flag.MV02_Auto | DB2.DBX6.7 | 0619 RID19 AO55, 0618 Flag DB2; HMI AutoMan 설정과 주소 일치 |
| 수동 요청 | Flag.M_MV02_CLOSE / OPEN | DB2.DBX9.5 / 9.6 | 0619 RID18/20 AO77/78. RCoil210/203의 대상이며 HMI Flag_CLOSE/OPEN 설정과 주소 일치 |
| PID 방향 | PID MV02 UP / Down | M14.0 / M14.1 | 0617 RID23/26 AO112/113; 0476 ORef208/209, 0670 RID43/44 |
| 공통 동작 펄스 | MV WORK PULSE | M10.0 | 0617 RID13 AO80. LAD1712 Coil823 → ORef832/W844 |
| 공통 게이트 | ON | M0.0 | 0617 RID1 및 0692 RID52 모두 Memory AO0. 이름을 상수 TRUE로 치환하지 않음 |
| 정지 인터페이스 | EM_OK | I19.4 | 0678 RID173 Input AO156. 엔코더/환산 호출 게이트. 안전 기능의 충분성을 이 한 비트로 확정하지 않음 |
| 명령 누적 | WorkData.W35 / W36 | DB6.DBW70 / DBW72, Int | 0619 RID115/117 AO560/576, 0618 WorkData TOD N6. 실제 위치 카운터와 별도 |
| 알람 해제 요청 | Flag.RESET_ALLARM | DB2.DBX6.0 | 0573 RID38 AO48, 0572 Flag TOD N2. 원인 해소와 별도 |
| MV02 고장 | Allarm.MV02_FAULT | DB3.DBX4.0 | 0573 RID16 / 0619 RID22 AO32, Allarm DB3; 복수 Set 및 Reset 존재 |
| 위치값 | Data.Pot_MV02 | DB1.DBW142, Int | 0676 RID339 AO1136, 0674 Data TOD N1. 단위/0–100 유효 범위의 현재 교정 미확인 |
| 위치 범위 오류 | Allarm.Pot_MV02_OFR | DB3.DBX24.7 | 0676 RID434 AO199, 0513 CRef30.Out_of_range → W83/ORef82 |
| 압력 원시 입력 | PSH01 | IW284:P | 0678 RID96 Input AO2272, SAM=Peripherie. FG75/107 PEW284 |
| 압력 환산값 | Data.Press_PC01 | DB1.DBW134, Int | 0676 RID99 AO1072; LAD1745 CRef436.OutValue → W454/ORef447. 이름만으로 PC01 원시채널이라고 보지 않음 |

주소 계산은 SSD.AO의 bit offset과 해당 DepDBBlock.TOD.N을 함께 사용했다. Timer의 AO는 byte/bit로 나누지 않고 타이머 번호로 읽었다. 입력/출력 E/A는 도면 표기, I/Q는 PLC 백업 표기다.

`open mv02 pid` M11.6 / `close mv02 pid` M11.7도 기존 심볼 대장에 있으나, LAD1704 최종 방향식에서 확인한 피연산자는 M14.0/14.1의 `PID MV02 UP/Down`이다. 동명 유사성을 이유로 두 쌍을 합치지 않는다.

### 3.2 원시 입력 → DB13 전달

LAD1070 `0397-FlgNet.xml`, hmi inputs NID1:

- Part22 Move, ORef25(Tag_178) → W23/in, W24/out1 → ORef26(RID5). 0627 Input AO0=IW0; 0629 대상 GlobalAccess AO0, BAD BIRID4로 DB13.DBW0.
- Part27 Move, ORef28(Tag_179) → W31/in, W32/out1 → ORef29(RID9). 0627 Input AO16=IW2; 대상 AO16=DB13.DBW2. 따라서 I2.2/2.3이 담긴 word의 전달 근거다.
- Part42 Move, ORef45(Tag_171) → W52/in, W54/out1 → ORef46(RID14). 0627 Input AO48=IW6; 대상 AO48=DB13.DBW6. 따라서 I7.3/7.4가 담긴 word의 전달 근거다.
- 0628의 RID4 DepDBBlock/TOD N13과 0629의 BAD BIRID4를 함께 확인한다. 첫 Move의 ENO가 다음 Move로 이어지는 부분과 독립 powerrail 분기를 보존한다.
- main LAD1613 `0030-FlgNet.xml`: Recipes Handler(CRef21) ENO→HMI(CRef23) ENO→HMI Output(CRef25) ENO→Part37 **NOT Simulation(1)**→HMI Inputs(CRef28). Simulation(1)은 0692 Memory AO1440=M180.0. 원시 입력 복사가 무조건 실행된다고 쓰지 않는다.
- main LAD1614/1615의 Word_inputs.word1~7은 별도 DB/재배치 복사다. 이것만으로 DB13 처리 응답 경로라고 주장하지 않는다.

실제 CPU의 스캔·다른 쓰기·메모리 갱신 시점은 미확인이다. 중지된 시뮬레이터를 실행하거나 행동시험하여 이 경계를 확인하지 않았다.

### 3.3 HMI 설정 8개와 원본 호출의 경계

| HMI 태그 | 설정 주소 | 내부 ID | 분류 |
|---|---|---|---|
| MV_02\OutputOpen | DB11,X20.0 | 00350 | 표시 설정; Q1.5 명령과 등치하지 않음 |
| MV_02\OutputClose | DB11,X20.1 | 0030A | 표시 설정; Q1.6 명령과 등치하지 않음 |
| MV_02\Allarme1 | DB11,X20.2 | 00317 | HMI 상태 묶음; DB3.DBX4.0과 별도 |
| MV_02\LimitSwitchOpen | DB11,X20.3 | 001A9 | HMI 상태 주소 |
| MV_02\LimitSwitchClose | DB11,X20.4 | 001A8 | HMI 상태 주소 |
| MV_02\AutoMan | DB2,X6.7 | 0034F | 자동/수동 요청 주소 후보 |
| MV_02\Flag_CLOSE | DB2,X9.5 | 00041 | 수동 닫기 요청 주소 후보 |
| MV_02\Flag_OPEN | DB2,X9.6 | 00040 | 수동 열기 요청 주소 후보 |

출처: `sources/hmi_plc_tags.csv`, Access Name=PLC. 버튼 MouseDown/MouseUp, 설정/해제 이벤트, 권한·통신 성공, 현재 HMI 태그 사용 여부는 이 CSV만으로 알 수 없다.

LAD1189 `0366-FlgNet.xml`에는 CRef22/RID639, CodeBlock23/RID130과 다음 물리 핀이 존재한다.

- W47: ORef24/RID697 → Ingresso_run_Opening
- W48: ORef25/RID696 → Ingresso_run_Closing
- W49: ORef26/RID192 → Allarme1
- W50~53: ORef27~30 → Allarme2~5
- W56/57: ORef33/RID695,34/RID694 → Limit_switch_Open / Limiti_Switch_Close
- W62/63: Risposta_Opening/Closing → ORef39/RID204,40/RID205
- W64/65: Limit_Switch_Open_HMI/Close_HMI → ORef41/RID206,42/RID207
- W68: Comulativo_allarmi → ORef45/RID210

검색색인 원문은 Inputs.MV02 RUN_Opening/Closing, Allarm.MV02_FAULT, false 네 개, Inputs.MV02 Open/Close, Motors.MV02의 응답/리미트/고장 필드를 순서대로 제시한다. 그러나 이 네트워크의 NID를 직접 확정하지 못했고 14개 피연산자의 UID/RID 선언 결속이 모두 확보되지 않았다. 따라서 이름은 **검색색인상 대응 후보**이며 직접 연결 완료로 세지 않는다. generic HMI standard motorized valve(LAD336/0356)에는 두 응답의 직접 전달·리미트 직접 전달·Allarme1~5 OR 집계가 있으나, generic 함수 의미를 이용해 이 호출 결속의 빈틈을 메우지 않는다.

압력 관련 HMI 설정은 Editor_PSH01=DB26,INT16 및 I_PSH_01=DB13,INT48이다. PID가 읽는 Data.PSH01_SETPOINT/Data.Press_PC01과 각각 주소가 다르므로 HMI→recipe/data 전달을 미검증으로 남긴다.

## 4. 제어 구조와 직접 원본 논리

### 4.1 LAD1704 방향/수동요청 해제

파일 `0343-FlgNet.xml`, block Valve Control loop, NID2. 선언은 0617(SimpleAccess), 0619(GlobalAccess), 상수/블록 선언은 해당 주변 IdentXmlPart. 아래 약어는 설명용이며 PLC 태그를 생성한 것이 아니다.

- N=ON; A=Flag.MV02_Auto; MO=Flag.M_MV02_OPEN; MC=Flag.M_MV02_CLOSE
- LO=Inputs.MV02 Open; LC=Inputs.MV02 Close; F=Allarm.MV02_FAULT
- U/D=PID MV02 UP/Down; P=MV WORK PULSE; QO/QC=Open/Close MV02

| 대상/Part | 원본상 정적 경로 | 핵심 Wire/ORef |
|---|---|---|
| MO Reset, RCoil203 | NOT N(Part310) AND NOT N(312) AND (NOT LO OR MC OR A) | W27/25의 ORef28/26=ON; ORef243/244/245→314/316/318→OR199→W273→203; W275/ORef246=MO |
| MC Reset, RCoil210 | NOT N(310) AND NOT N(312) AND (NOT LC OR MO OR A) | ORef247/248/249→320/322/324→OR206→W279→210; W281/ORef250=MC |
| QO Coil227 | NOT N AND NOT F AND ((A AND U) OR MO) AND (P OR N) AND NOT QC AND LO | Part326/F→OR221→OR222→NOT338/QC→340/LO→W22→227; W295/ORef259=Q1.5 |
| QC Coil240 | NOT N AND NOT F AND ((A AND D) OR MC) AND (P OR N) AND NOT QO AND LC | Part326/F→OR234→OR235→NOT352/QO→354/LC→W24→240; W307/ORef267=Q1.6 |

반전 접점은 원문 그대로 보존했다. LO/LC는 이름에 Open/Close가 있어도 최종 출력 경로에서는 정접점이다. 전기도면의 LS17/18(11–12)과 관계를 비교할 수 있지만, 현장 정상 극성이나 ‘1이면 완전 열림/닫힘’을 단정하지 않는다.

### 4.2 호출 게이트와 순서 경계

main LAD1621 `0032-FlgNet.xml` NID8: W354 Powerrail→Part352 Contact.in, ORef345/RID52 ON→W350 operand, Part352.out→W353→CRef341.en / CRef344.en. CRef341/RID86 안의 CodeBlock347/RID85는 0688의 FCBlock `Valve Control loop`(TOD N14)다. ON은 0692 RID52 Memory AO0=M0.0이며 LAD1704의 0617 RID1과 같은 절대주소다.

확인한 main 호출은 ON 정조건, LAD1704 내부는 ON 부조건이다. 이를 지운 정리식만 제시하지 않고 원문 이중 반전 접점도 보존한다. 이 정적 대조만으로 다른 호출, 인터럽트, ON 실행 중 쓰기, 사용하지 않는 구회로, 현재 CPU 차이를 판정할 수 없다.

main LAD1619 `0031-FlgNet.xml`은 ON 정조건으로 Analog input conversion/Allarms1/2/3을 호출한다. 여러 네트워크의 Set/Reset 최종값은 저장 백업의 참조·순서와 현재 CPU의 실행 증거를 분리해서 판단해야 한다.

### 4.3 공통 동작 펄스와 명령 누적 펄스

- LAD1712 `0350`: Part813 SdCoil, S5T#200MS(ORef825/W834)→Tag_155; Part818 SdCoil, S5T#2S(ORef828/W838)→Tag_154; Part823 Coil, NOT Tag_155를 거쳐 MV WORK PULSE(ORef832/W844)로 쓴다. ON 정조건, Tag_154 부조건, Tag_155 정/부접점이 분기마다 존재한다. PID의 200ms/2.5s 파라미터나 150ms 고장 감시와 합치지 않는다.
- LAD1713 `0351`: Part1225/1230 SdCoil은 각각 S5T#10MS. Tag_157(%T119)/Tag_156(%T118), NOT Tag_157→PBox1235(PLS 50 7)을 사용한다. 실측 주기, CPU 스캔 의존성, 경과 초 환산은 미검증이다.
- MV02 분기는 Part1653 ON, Part1655 Open MV02, Part1657 Close MV02다.
  - Open 분기 W1656→Add1282 / Move1288. W35+1(ORef1466/1467, W1559/1560)→W35(ORef1468/W1561), 동시에 0→W36(ORef1469/1470, W1562/1563).
  - Close 분기 W1658→Sub1297 / Move1303. W36−1(ORef1472/1473, W1566/1567)→W36(ORef1474/W1568), 동시에 0→W35(ORef1475/1476, W1569/1570).
- 이는 **출력 명령의 누적**이며 ZT03의 실제 회전 펄스·이동량이 아니다. 정지 중 유지, 오버플로, 재기동 초기값은 별도 자료가 필요하다.

### 4.4 MV02 엔코더 읽기

LAD1757 `0507-FlgNet.xml`, NID45.

- Part74는 NOT Simulation(1), Part21은 EM_OK다. W76/50으로 High_Speed_Counter의 en에 연결된다.
- LRef22/RID330은 0679 `High_Speed_Counter`. Instance23/RID332는 0673 `MV02_Encoder`, TOD DB16이다.
- SwGate: W51/ORef25/RID222→fill_unit1.CONTROL_SIGNALS.SW_GATE1. 0676 AO185, 0674 fill_unit1 DB91이므로 DB91.DBX23.1이다.
- CountValue: W71/LRef22.CountValue→ORef45/RID224 fill_unit1.ACT_CNTV1. 0676 AO1248, DInt, DB91.DBD156이다.
- CaptureEnable/SyncEnable/ErrorAck/EventAck/SetCountValue, 각 status/error 등에는 RefId 없는 ORef가 있다. 미결선/생략 핀을 FALSE/0 또는 정상으로 임의 보완하지 않는다.
- 도면의 ZT03 CH1.A/B와 소프트웨어 CH01/DB16은 자료상 대응 후보다. TM의 현행 하드웨어 ID, 기술 객체 할당, 엔코더 형식/분해능/방향은 미확인이다.

### 4.5 MV02 데이터 관리·닫힘단 메모리 처리

LAD1763 `0513-FlgNet.xml`, NID46.

1. Part21 EM_OK 뒤에 Part22 **NOT MV02_Close(I7.4)**가 있다.
2. Part23 Coil → W58/ORef34, SW_GATE1(DB91.DBX23.1). 같은 분기에서 Add24가 Memory encoder.Encoder_CH01 + ACT_CNTV1을 CNT_Act_1로 출력한다(W59/60/62).
3. Add24.eno→Div25.en(W61). CNT_Act_1 / literal100 → CNTV1_100(W63/64/66). Div25.eno→Move26.en(W65), CNTV1_100→Encoder_CH01_10(W67/68). 이름은 `_10`이지만 원문의 나누는 수는 100이다.
4. 별도 분기 Part27 **NOT SW_GATE1** → Move28/29. 0→Encoder_CH01_10, INT#0→Encoder_CH01(W69~74). 메모리 영역 쓰기이며 HSC 실제 카운터 Reset을 증명하지 않는다.
5. EM_OK에서 W55→CRef30.en. CodeBlock31/RID5는 0672 `Signal linearization`, CRef 선언은 0680 RID351이다.
6. IN0←ON(W75/ORef48), Analog_input←Encoder_CH01_10(W76/ORef49), Coeff←COEFF_TRASM_MV02(W77/ORef50), Zero←ZERO_TRASM_MV02(W78/ORef51). OutValue→Data.Pot_MV02(W79/ORef52), Out_of_range→Allarm.Pot_MV02_OFR(W83/ORef82).

| 값 | 선언/저장 위치 |
|---|---|
| Memory encoder.Encoder_CH01 | 0676 RID195 AO32, DB8.DBD4의 DInt |
| Memory encoder.Encoder_CH01_10 | 0676 RID228 AO304, DB8.DBW38의 Int |
| CNT_Act_1 | 0677 InterfaceAccess RID194, Local DInt, AO432 |
| CNTV1_100 | 0677 InterfaceAccess RID226, Local DInt, AO144 |
| COEFF_TRASM_MV02 / ZERO_TRASM_MV02 | 0676 RID337/338 AO656/640, DB4.DBW82 / DBW80, Int |

Add24/Div25의 SrcType은 DInt이며 CNTV1_100도 Local DInt다. Move26의 목적지 Encoder_CH01_10은 Int이므로 데이터 폭이 다르다. 넘침·절삭/변환의 실제 결과를 이 정적 연결만으로 확정하지 않는다. 현재 계수·제로·기계 스트로크·백분율 표시의 교정값은 미확인이다. LAD1703/1707의 다른 MV 교정을 MV02에 배정하지 않는다. MV02 전용 ResetEncoderProcedure를 원문 검색에서 확보하지 못했다는 사실을 ‘교정 불필요’로 바꾸지 않는다.

### 4.6 PSH01 계측과 MV02 PID

- LAD1745 `0495` CRef436 Signal linearization: ON으로 en, IN0도 ON이다. W451/ORef444=PSH01, 0678 Input AO2272/SAM Peripherie=IW284:P. Coeff=DB4.DBW38, Zero=DB4.DBW36. OutValue→Data.Press_PC01(DB1.DBW134), Out_of_range→Allarm.PSH01_OFR(DB3.DBX22.0).
- source live_index의 STL document6: Data.PSH01_SETPOINT를 ITD/DTR하여 Local Real_SPPC01로, Data.Press_PC01을 ITD/DTR하여 Local Real_PC01로 옮긴다는 원문이다. 검색색인 텍스트이며 컴파일된 명령열로 검증하지 않았다.
- LAD7 `0476`, NID4: LRef172/RID113=CONT_S(0671), Instance210/RID38=PID_MV-02(0665 TOD DB23). Part245 ON→en(W246). Part247 NOT Flag.MV02_Auto→COM_RST(W248). Part249 NOT Inputs.MV02 Open→LMNR_HS(W250), Part251 NOT Inputs.MV02 Close→LMNR_LS(W252).

| 핀 | 원문 값 | Wire/ORef 및 선언 |
|---|---|---|
| CYCLE | T#100MS | W223/ORef198 RID21, 0667 |
| SP_INT / PV_IN | Real_SPPC01 / Real_PC01 | W224/225, ORef199/200, 0669 RID31/33 |
| GAIN | -0.22 | W228/ORef201 RID39, 0667 |
| TI | T#2S | W229/ORef202 RID40 |
| DEADB_W | 2.0 | W230/ORef203 RID22 |
| PULSE_TM | T#200MS | W235/ORef204 RID25 |
| BREAK_TM | T#2S_500MS | W236/ORef205 RID41 |
| MTR_TM | T#18S | W237/ORef206 RID42 |
| DISV | 1.0 | W238/ORef207 RID24 |
| QLMNUP / QLMNDN | PID MV02 UP / Down | W239/240→ORef208/209, 0670 RID43/44, M14.0/14.1 |

LMNS_ON/LMNUP/LMNDN/PVPER_ON/PV_PER/PV_FAC/PV_OFF/PV/ER는 RefId 없는 ORef를 포함한다. 기본값이나 유효 상태를 추정하지 않는다. -0.22 등은 저장 원문의 값이며 조정 권장값이 아니다. 현재 인스턴스 값·방향·루프 안정성·단위는 미확인이다.

### 4.7 시작 시 자동 설정·다른 쓰기

LAD404 `0149` Part297 SCoil은 ON 조건으로 Flag.MV02_Auto를 Set한다. HMI AutoMan과 같은 DB2.DBX6.7을 취급하므로 수동 선택이 계속 유지된다는 전제를 두지 않는다. LAD396 `0146`에는 OFF(Part92) 조건에서 Add61이 Data.Pot_MV02+1→같은 위치값을 쓰는 경로(W82~84), OFF AND Data.Pot_MV02 >100에서 Move70이 0을 쓰는 별도 경로(W85~90)도 있다. 현재 실행 여부와 최종값은 미검증이다. 시험용 제목의 기록을 본운전 유효 제어로 간주하지 않고 다른 쓰기 경계로 보존한다.

공유 Q1.0의 별도 쓰기 원본은 LAD1186 `0363-FlgNet.xml`: Powerrail W21→Part63 **반전 접점**→W40→Coil64→W41/ORef44 RID776다. 0063 SimpleAccess의 NID9 UID44 AK=Write, Output AO8로 Start Aux INV를 직접 확인했다. 앞단 피연산자는 W38/ORef39 RID120이며 CRef23.Comulativo_allarmi 출력도 W46/ORef47 RID120에 연결된다. 다만 RID120의 직접 선언 결속이 없어 `Motors.aux_inv.allarme_comulativo`는 색인상 후보로만 남긴다. 이 가드를 이름까지 확정한 정상 시작식으로 제시하지 않는다.

## 5. 전기 전달 경로와 PDF 실제 렌더

아래 FG는 도면 번호, PDF 페이지는 1부터 시작하는 별도 번호다. Electrical_Rev2의 총 페이지는 265다. FG30/107/117/118/123/137은 Rev2 17.03.2025, FG31/36/37/75/145는 개별 Rev 행이 없고 기본 날짜 27.05.2024임을 눈으로 확인했다. PDF 파일명만으로 모든 페이지의 개정을 같게 만들지 않는다.

### 5.1 공유 인버터→전용 M16

- FG30/PDF31: 삼상선 6.2L1/L2/L3(도면 표기 440V 60Hz)→30QM1→30AS1 U1/V1/W1. 30QM1에 5.5–8 A/RATING6.9 A, 30AS1에 ABB ACS355-03E-04A1-4, 1.5 kW가 표시된다.
- 30AS1 U2/V2/W2→30U1/30V1/30W1. FG32→FG34→FG36으로 이어지는 도면 참조를 보존한다.
- FG36/PDF37: 30U1/V1/W1→36QM1(1.4–2 A)→36KM1/36KM2 삼상 반전 배선→36U1/V1/W1→XM 동명 단자→36QS1→M16 U/V/W. PE·실드 30SCH1 경로도 있다.
- BLACK FS17 1.5 mm²는 해당 도면 구간의 배선 사양이다. 현장 전체 구간의 케이블 사양으로 일반화하지 않는다. 0.75 kW/1.67 A는 M16 도면 표기이며 다른 MV 정격과 바꾸지 않는다.

### 5.2 방향 DO→코일→DI

- FG137/PDF138: CPU515 MOD14, 단자16=A1.5, 17=A1.6. X21:3029의 4 A F 5×20, 24Vdc10.9 공급 표기를 확인했다.
- Open: A1.5→상대 36KM2 NC31–32→36KM1 A1. Close: A1.6→36KM1 NC31–32→36KM2 A1.
- 두 코일 A2는 36.3→36QM1 보조접점(63–64)→36.4→XS23→36QS1 보조접점→XS24→0Vdc10.6으로 이어진다.
- 접촉기 응답: +24Vdc10.7→36KM1 NO13–14→E2.2(118/3); KM2 NO13–14→E2.3(118/4). FG118/PDF119 CPU515 MOD8, 단자23/24가 두 신호의 받는 끝점이다.
- PLC의 반대 Q 반전 조건과 전기회로의 상대 KM NC는 다른 층의 인터록이다. 한쪽 자료만으로 기계 안전·현장 기능이 성립한다고 판정하지 않는다.

### 5.3 LS17/18 양 끝점

- FG37/PDF38: +24Vdc10.7→X1:81, 2 A F 5×20→37.5→LS17 11–12→X1:82→E7.3(123/4).
- Close: +24Vdc10.7→X1:83, 2 A F 5×20→37.6→LS18 11–12→X1:84→E7.4(123/5).
- FG123/PDF124: CPU515 MOD9, E7.3=단자34, E7.4=단자35. LS17/18 명칭도 실제 페이지에서 확인했다.
- 도면 NC 기호, 입력 논리값, 실제 기계 끝단 상태는 나누어 관찰한다. 단선/극성/위치 어긋남을 HMI 표시만으로 판단하지 않는다.

### 5.4 ZT03 양 끝점

- FG37: ZT03 B(+24V)→X1:76→37.1, C(0V)→X1:77→37.2, D→X1:78→37.3, E→X1:79→37.4, 실드→X1:80→37SCH1.
- FG37의 37.1/37.2 참조는 `45/1`, 37.3/37.4/37SCH1은 `145/3`으로 인쇄되어 있다. 앞의 참조를 근거 없이 145/1로 수정하지 않는다.
- FG145/PDF146: 37.3→CPU515 MOD16 단자11 CH1.A, 37.4→단자12 CH1.B, 37SCH1→실드 접지. 단자13 CH1.N에는 이 페이지에서 37 계열 입력선이 확인되지 않았다.
- 같은 페이지의 전원은 X21:3040, 2 A IST 5×20→145.1→41 L+, 44 M→0V다. 전원 참조의 미확정 부분을 다른 페이지 추측으로 해결하지 않는다.
- 현재 엔코더 형식, A/B 상순서, 펄스 수, 케이블 말단, TM 형식/설정, 하드웨어 ID가 부족하다.

### 5.5 공유 시작/응답/알람

- FG31/PDF32: Q1.0/A1.0→30QM1 보조접점→31KA1 A1, A2→0V. FG30에서는 30AS1 terminal9(+24V)→31KA1 접점→terminal12 DI1 START다.
- 30AS1 RUNNING 단자17/18/19의 접점에서 E1.4, ALARM 단자20/21/22에서 E1.5를 낸다. 도면상 +24V 공급은20, 0V는22, E1.5는21, RUN쪽 E1.4는19에 연결된다.
- FG117/PDF118, CPU515 MOD8 단자15=E1.4,16=E1.5가 받는다. MV02/MV05/MV06의 공유 상태다.
- FG30에 17KA2 RESET과 14KA2/14KA6 STO 회로가 있다. 이 조사에서 STO나 보호를 변경·우회·시험하지 않았다. 현재 ABB 단자/형식/파라미터는 명판과 승인 자료가 필요하다.

### 5.6 PSH01 양 끝점

FG75/PDF76: PSH01 P-BADR 0/10mbar, 4–20mA라는 도면 표기다. +24Vdc10.7→X1:172/50mA F 5×20→PSH01+, PSH01−→X1:173→+PEW284(107/4). 실드 X1:174→75SCH1(107/3). FG107/PDF108에서 +PEW284→CPU515 MOD3 단자30 I6+, 32 U6−/I6−의 0V 연결을 확인했다. 도면 범위·단위를 현재 교정 증명으로 사용하지 않는다.

### 5.7 시공 참고 케이블 양 끝점

Electrical_Can_Decoating_20241118.pdf의 실제 렌더를 확인했다.

| PDF/행 | 케이블 | FROM→TO | 표기 사양/경계 |
|---|---|---|---|
| p51,1_8 | =FLO+MV02-M16A | CR→MV-02 M16 | PVC-S4심 1.5SB, spare0, route100→110/LAD1→E800, Adjustment8.5, LEN55. 현장 실측 길이 미확인 |
| p57,7_1 | =FLA+HE01-FLO2TB1A | CR→HE-01 FLO2TB1 | LS17/18/23/24/21A/22A/21B/22B 공용, CVV25G 1.0, spare8 |
| p57,7_6 | =FLA+HE01-FLO2TB1F | CR→HE-01 FLO2TB1 | ZT03, AI 표기, CVV-S4S 1.0, spare0. 전기도면 TM 엔코더 방식과 차이를 보존 |
| p57,7_11 | =FLA+MV02-LS17A | HE-01 FLO2TB1→MV-02 LS17 | DC/CVV2C 1.0, spare0, LEN12 |
| p57,7_12 | =FLA+MV02-LS18A | HE-01 FLO2TB1→MV-02 LS18 | DC/CVV2C 1.0, spare0, LEN12 |
| p57,7_13 | =FLA+MV02-ZT03A | HE-01 FLO2TB1→MV-02 ZT03 | AI/CVV-S4S 1.0, spare0, LEN12. TM/AI 표기 차이 미해결 |

p30 경로 행에도 M16의 1_8이 있으나 같은 케이블의 경로 참고이며 별도의 전원 본수가 아니다. p30 PSH01 케이블은 2심, p57의 7_7은4S 표기이므로 시공 참고 내부 사양 차이를 유지하고 MV02의 현재 사양으로 확정하지 않는다.

## 6. 알람·정지·복구

### 6.1 방향 명령/접촉기 응답 불일치

LAD1226 `0159`, NID1.

- ON 공통 Part513→MV02 분기 Part525 ON.
- 열기: Part527/Open MV02 AND Part531/NOT Inputs.MV02 RUN_Opening.
- 닫기: Part529/Close MV02 AND Part26/NOT Inputs.MV02 RUN_Closing.
- OR28(W29/W30)→W532→SdCoil265.in 및 Part533.in.
- SdCoil265.value←W442/ORef376/RID8, 0571 LiteralConstant `S5T#150MS`. operand←W443/ORef377/RID15, 0570 Timer AO21=`Tag_93`(%T21).
- 타이머 접점 Part533, ORef378/W444가 성립하면 W534→SCoil270, W446/ORef379→Allarm.MV02_FAULT(DB3.DBX4.0)를 Set한다.
- 해제는 같은 네트워크의 ON→Flag.RESET_ALLARM→Allarm.MV02_FAULT 접점→RCoil346, ORef416이 같은 비트를 Reset한다. 원인 해소나 재기동을 증명하는 동작은 아니다.

이 불일치는 접촉기 보조 응답을 감시한다. 리미트 도달 시간·축 회전·ZT03 변화의 직접 감시와 구별해야 한다.

### 6.2 명령 누적의 별도 Set

LAD1714 `0352`, NID12.

- ON(Part1943)→ON(Part1947)→Gt1624: W35 >1000. W1865→SCoil1630, W1866/ORef1793=MV02_FAULT. 동시에 Move1633이 0→W35(W1867/1868)를 쓴다.
- 같은 ON 분기→Lt1638: W36 <−1000. W1872→SCoil1644, W1873/ORef1798=MV02_FAULT. 동시에 Move1647이 0→W36(W1874/1875)를 쓴다.
- 부등호는 엄격한 `>`와 `<`다. 1000/−1000과 같은 시점에 발생하는 조건으로 바꾸지 않는다.
- 10ms 선언을 더해 1000×10ms 등의 확정 시간을 만들지 않는다. Tag156/157/PBox의 유효 주기·스캔/호출은 미검증이다.
- Set 원인이 여러 개여도 최종 HMI Allarme1이 원인을 구분해 준다고 단정할 수 없다. 이력을 새로 만들지 않고 향후 관찰에서 불일치 분기/누적 분기/OFR를 따로 기록한다.

### 6.3 OFR 및 공유 인버터

- Allarm.Pot_MV02_OFR는 위치 Signal linearization의 Out_of_range 쓰기다. Allarm.PSH01_OFR는 압력 Signal linearization의 Out_of_range 쓰기다. MV02_FAULT 래치/Reset과 같은 동작으로 단정하지 않는다.
- LAD1704 직접 출력 조건에는 MV02_FAULT가 있다. 이번에 제시한 최종식에는 위치 OFR/PSH01_OFR/공유 Aux_INV의 직접 접점이 없다. 다른 상위 영향도 없다는 뜻은 아니다.
- 공유 LAD1821 `0455`에는 Aux_Inv_Run TON의 T#2S, Aux_Inverter_Fault/Aux_INV Set/Reset이 있다. 다만 Part1837 Start Aux INV 바로 뒤에 Part22 **NOT 같은 Start Aux INV**가 직렬로 있으며, 그 뒤로 RUN 결여와 Aux_Inv_All 분기가 이어진다. 이를 생략하여 단순히 ‘Q1.0 뒤2초 고장’으로 설명하지 않는다.
- Reset만으로 접촉기 동작, 리미트 극성, 엔코더 변화, PID 추종의 복구를 증명할 수 없다. 실제 복구 증거는 없다.

## 7. 증상별 관찰·분리안

후속 기록용 확인안이다. 현장 작업이나 보호 변경을 수행한 것이 아니며 전원/접촉기/단자 실측·점검은 담당자의 안전 절차와 격리 조건이 필요하다.

| 증상 | 관찰 위치/값 | 원본 비교·원인 분리 순서 | 복구 판정에 부족한 증거 |
|---|---|---|---|
| 자동에서도 안 움직임 | main FC14 호출, M0.0, DB2.X6.7, M14.0/14.1, Q1.5/1.6, DB3.X4.0 | main ON정/내부 ON부를 먼저 대조. PID 요청 없음, 방향 조건 불성립, 호출 없음을 구별 | 현재 CPU 블록/호출, 시각 포함 온라인 관찰 |
| 수동 요청이 사라짐 | DB2.X9.5/9.6, RCoil203/210, Auto, DB13.X7.3/7.4 | HMI 실제 이벤트→요청값→Reset 분기. 누름/뗌 동작을 추정하지 않음 | HMI 이벤트/권한/통신, 같은 시각의 요청·출력 변화 |
| Q가 나와도 M16이 안 돎 | Q1.0, 공유 RUN/FAULT, Q1.5/1.6, KM1/2, 36QM1/QS1 | 공유30AS1 공급, 전용 반전 접촉기, 보조 응답, 실제 부하를 분리 | 현행 회로/명판, 적절하게 수집한 접촉기/축 실측 |
| 150ms 고장 | Q1.5/1.6, I2.2/2.3, DB13.X2.2/2.3, T21, DB3.X4.0 | 명령/KM 응답, raw→DB13, 호출/ENO를 구별. 끝단 센서 고장으로 단정하지 않음 | 원인 제거 뒤 명령/응답 일치, 재발 없음 |
| 누적 고장 | W35/W36, PBox1235, 출력 지속, LO/LC | ±1000 엄격 비교와 반대 방향 카운터0 쓰기. 회전 펄스와 구별 | 현재 누적값/주기/리미트·기계 상태 |
| 전개/전폐 표시 반대, 출력 멈춤 | LS17/18 실제 위치, I7.3/7.4, DB13, HMI DB11 | NC11–12 회로·raw/처리/표시 순서. 명칭으로 정상 극성 판단 금지 | 실위치 대응표, 도통/입력/HMI가 같은 시각에 일치하는 증거 |
| 위치0/점프/갱신 안 됨 | M180.0, EM_OK, I7.4, SW_GATE1, DB16, ACT_CNTV1, 메모리, DB1.W142 | 읽기 허가→카운터→나눔100→Zero/Coeff→다른 Move0를 구별 | TM 설정, A/B 배선/방향, 현재 계수와 스트로크 |
| 압력 PID 추종 안 됨 | IW284:P, Data.Press_PC01, Local Real_PC01, DB23, M14.0/14.1 | PSH01/PC01 제목 차이, HMI 설정 전달, PID 리셋/리미트, 최종 출력식 | 현재 단위/교정/설정값, 동작 방향, 실제 루프 응답 |
| Reset 후 재발 | RESET_ALLARM, fault 각 Set 분기, OFR, 공유 Fault | 래치 해제와 원인 잔존·재요청을 구별. 복구 조작 자체를 완료 증거로 삼지 않음 | 원인 소멸, 필요한 재요청 뒤 정상 응답, 재발 없음 |

기록란은 관찰자, 날짜/시각/시간대, 설비 ID, 관찰점, 값/단위, 수집 기기/방법, 백업/현재 CPU 식별, 비교 원본, 배제한 원인, 승인된 실제 조치, 전후 차이, 복구 증거를 나눈다. 과거 운전값·사진을 만들어 채우지 않는다.

## 8. 소유·상충·누락 목록

| ID | 내용 | 처리/필요 자료 |
|---|---|---|
| MV02-G01 | main ON정과1704 ON부 | 원문 극성 유지. 현재 CPU·전체 호출/ON쓰기, 블록 사용 여부 필요 |
| MV02-G02 | HMI1189 14개 피연산자 선언 미결속 | 검색색인 후보 유지. 실제 TIA에서 일반 함수/개별 호출 대조 |
| MV02-G03 | HMI OutputOpen 명칭과 실제 Q명령 | DB11 응답/표시와 Q1.5 명령 구별. 버튼 이벤트/직접 연결 필요 |
| MV02-G04 | PID 제목PC01과 실제PSH01/IW284 | 실제 핀 경로 우선, 제목도 보존. 현장 계기/화면 대응 확인 |
| MV02-G05 | DB26 HMI 설정과 Data DB1 PID입력 | recipe/데이터 전달·현재 설정 미검증 |
| MV02-G06 | 원시 입력과 DB13 갱신 | LAD1070/1613 허가와 ENO 보존. 현재 호출·다른 쓰기 미검증 |
| MV02-G07 | 물리ZT03과 소프트CH01/DB16 | 자료상 대응 후보. TM 할당/하드웨어ID/분해능 미확인 |
| MV02-G08 | Encoder_CH01_10과 나누는 수100 | 명칭 보존, 원문 Div100 채택. 현재 단위·반올림/범위 미검증 |
| MV02-G09 | MV02 전용 교정 회로 미확보 | 다른 MV 교정 전용(轉用) 금지. 제조사/현재TIA/교정 절차 필요 |
| MV02-G10 | 위치 읽기/관리/주기 시험이 같은 위치값에 영향 | 시간 순서·호출·덮어쓰기의 온라인 증거 필요 |
| MV02-G11 | 명령 누적±1000과 실제 이동 시간 | 초/회전 수로 환산 금지. 유효 주기와 기계 조건 필요 |
| MV02-G12 | 공유Aux_INV의 같은 명칭 정/부 직렬접점 | 단순2초 알람 설명 금지. 호출/현재 원본 대조 |
| MV02-G13 | FG37 전원45/1, 신호145/3 참조 | 인쇄값 보존. 전원 끝점 추적 미완료 |
| MV02-G14 | 시공ZT03 AI와 전기도면TM 입력 | 참고 설계 차이 유지. 승인 케이블표/실물 필요 |
| MV02-G15 | p30 PSH01 2심과p57 4S | 참고 자료 내부 사양 차이. 현재 케이블 추정 금지 |
| MV02-G16 | 접촉기 응답/LS 끝단/엔코더 위치 | 3종류를 같은 상태로 합치지 않음 |
| MV02-G17 | 공유30AS1과 M16 전용 보호 | 다른 MV에서 오는 공유 영향을 분리. 공통 설비의 MV02 독점 소유 배정 금지 |
| MV02-G18 | 모터·인버터 도면과 현재 실물 | 명판/현행 도면/보호값/ABB 판본별 자료 필요 |
| MV02-G19 | Local DInt CNTV1_100→Int Encoder_CH01_10 | 원문 데이터 폭 차이 보존. 실제 변환/넘침 처리 미검증 |
| MV02-G20 | 공유 Q1.0 쓰기의 앞단 RID120 미결속 | LAD1186 Coil64 출력은 직접 확인, 가드 명칭은 색인 후보 |

## 9. 네 기능과 기록 보존 인계

| 기능 | 준비한 근거 | 구현·검증 상태 |
|---|---|---|
| 도면·래더 나란히 보기 | §4/5 원본 대조. FG36↔1704/1226, FG37/145↔1757/1763, FG75/107↔1745/7 | 원본 참조만. MV02 전용 UI 통합·강조·너비 미구현/미검증 |
| 백업·선택 복원 | 안정 ID MV02, 원본 판본/미확정 경계 | 저장키/기존 기록 변경0. 저장/재읽기/재열기/충돌시험 미수행 |
| 전후 기록 비교 | §7 관찰 항목안 | 합성QA 포함 미수행. 구형/미지 필드·다른 설비 기록 보존 요건 유지 |
| 보고서/PDF | 이 MD, 원본PDF 시각 근거 | MV02 보고서 생성/배포/공개·A4 검증 미수행. 원본PDF 확인과 보고서 기능 완료 구별 |

## 10. 검증 및 최종 상태

- preflight.py의 내용을 확인한 뒤 읽기 전용 실행했다. inventory_matches=true, catalog248 / phase2_candidates133 / catalog_excluded90 / excluded_parent_hold7을 유지한다. source_byte_changes는 기존 표준 시점과의 차이로 결과에 저장하고 이번 원본 변경과 혼동하지 않는다.
- 0343/0159/0350/0351/0352/0507/0513/0476/0495/0397/0030/0031/0032 등을 XML로 읽고 Part/Wire/ORef/CRef/LRef/Instance와 선언의 UID/RID/NID를 대조했다.
- RID/UID/NID는 블록 사이에 중복된다. 예: 0343 ORef249/RID19/NID2에는 다른 블록의 Flag.Start_Burner 후보, 0476 ORef208/RID43/NID4에는 Word_outputs.WORD8 후보가 있다. 해당 블록 선언 파일 집합·색인 원문으로 배제했고 같은 정수만으로 채택하지 않았다.
- Electrical11쪽, 시공 참고3쪽, P&ID1쪽을 실제 렌더했다. 주장에 사용한 각 페이지/부분을 눈으로 확인했으며 텍스트 추출을 시각 확인으로 대신하지 않았다.
- 새 산출물은 추출 JSON/TXT, 읽기 보조 스크립트, 원본 PDF의 PNG 렌더, 이 MD뿐이다. 시뮬레이터 작성/수정/생성/실행/행동시험0, 실제 PLC·현장·보호값 변경0.
- 프로그램 생성기, npm test/build, verify:manual, BC01 회귀, UI조작, 기록 시험, Git push/배포/게시를 수행하지 않았다. cloud 조사만인 이번 범위를 지키기 위한 구분이다.

| 구분 | 상태 | 경계 |
|---|---|---|
| documentation | complete_with_gaps(독립 조사 MD) | 통합 검토 전, G01~G20 유지 |
| static_review | partial_original_checked | 수작업 원문/선언/도면 대조. 제품 정적 테스트 미수행 |
| ui_records | not_run | 코드/저장/화면 변경0 |
| publication | not_published | 외부 업로드/게시0 |
| tia_compile | not_performed | TIA환경/CPU접속 미사용 |
| live_cpu | not_performed | 2025백업과 현재값 구별 |
| field_recovery | not_performed | 실물/작업/복구 미확인 |

다음 작업은 독립 검토에서 ON 반전/호출, HMI 미결속, PC01 제목과 PSH01 실제 경로, ZT03/CH01과 도면45/1 참조, 공유Aux_INV 상충을 확인하는 것이다. 이번 cloud 조사 완료를 로컬133개 확대 착수나 게시 승인으로 바꾸지 않는다. 새 자료 없이 현장 보류를 반복 조사하지 않는다.

## 11. 재현 가능한 조사 파일

- `gme-research/extracts/MV02/preflight.json`: 읽기 전용 대장 검사의 실제 결과.
- 같은 디렉터리 `*-refs.json`: FlgNet·후보 선언·블록 판정·원래 map. `block_file_supported=false` 후보를 무조건 채택하지 않는다.
- `*-trace.txt`: Wire 끝점 목록. `?`는 미결속 또는 명시적 RefId 부재이며 0/false를 뜻하지 않는다.
- `declarations.json`, `db-declarations.json`: 선언 트리 및 DB번호 선언 추출. 원본 XML 재읽기를 위한 부속자료다.
- `render/`: 실제 페이지 PNG와 P&ID MV02 부분 표시. Electrical의 FG는 파일명의 PDF페이지 번호로 기계적으로 추정하지 않고 도면란에서 확인한다.
- `SOURCE-SHA256.json`: 참조한 고정 커밋 원본의 SHA256, 바이트 수, git blob 일치 결과.
- `VALIDATION.json`: 최종 Git 상태, 원본 해시 재검사, 미실행 항목.

아래 원본 파일은 고정 커밋 상대경로다. 사용한 선언/네트워크·PDF·색인을 SHA256으로 식별한다. 해시 일치는 원본과 현재 CPU/현장이 같다는 증명이 아니다.

### 11.1 원본 SHA256

고정 커밋의 실제 파일 97개를 SHA256 및 git blob 바이트로 대조했다. 모두 일치했다. 전체 목록은 부속 SOURCE-SHA256.json에도 있다.

| 고정 커밋 상대경로 | SHA256 |
|---|---|
| `.agents/skills/gme-equipment-rollout/SKILL.md` | `fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b` |
| `VERSION.json` | `5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7` |
| `all-in-one/registers/all-in-one-data.json` | `63a46b36b6454bf1246d093300dbee11f2fcc287ad94991405369bf9f939a8fe` |
| `all-in-one/registers/control-spec.json` | `1e495b32f1f11b910919fbd2945e842a019fce9a27a6a0d7298041a7fab00079` |
| `all-in-one/registers/encoder-position.json` | `2f73fa3245f3bb3af1a90b7244247bf422993b8868768a2dfbf127732c336e05` |
| `all-in-one/registers/equipment-io.csv` | `a7a1f27dc453af25b2b729074cac5266d6dd53c0945a6a1a4afe2dd1e9153b6a` |
| `all-in-one/registers/equipment.json` | `7870325dff32bbca90fa34507b301c4aad3347d669fddcd03b910343663996fa` |
| `all-in-one/registers/plc-symbols.csv` | `a0334b390f06ddb515d6c09ca96a01d35d44029c1b726ef0ff53303ec04ff91f` |
| `all-in-one/registers/regulation-manual.json` | `3b5309ec06f35610ab57e6ef85bd7eb6f7c83ec7db149db1b881b9b65bce91fe` |
| `all-in-one/sources/Electrical_Can_Decoating_20241118.pdf` | `3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd` |
| `all-in-one/sources/Electrical_Rev2.pdf` | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` |
| `all-in-one/sources/GME_20250506.zap18` | `00c79b6d986e68298f65b172c1807115bc5d9e450a74fcc989d0796d8d8a4ea8` |
| `all-in-one/sources/PEData.plf` | `647de7ea123daced41c27bec8f81aeb93c712cac714d4754d7da5c528abb016a` |
| `all-in-one/sources/PID_1684n002I.pdf` | `2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b` |
| `all-in-one/sources/can-decoating-page-text.json` | `d3b4c14945dd00f79c58ebab0cb8991c422dd1670e95e24d10779bd9e9d99bba` |
| `all-in-one/sources/decoded-original/0030-FlgNet.xml` | `9252c9da764993de1edb8b2e44c46d6e9f9d4b6118e751a0dbeaa9ffd8ea721b` |
| `all-in-one/sources/decoded-original/0031-FlgNet.xml` | `76385eab8f8f72b9faa16f7cf8905f395591b18c0a9ee9e6d7dd085a38c45c65` |
| `all-in-one/sources/decoded-original/0032-FlgNet.xml` | `070bb8efa33d03b18add5da81d3f670a47c12b288076b7bfee11ac87fe6fa7e4` |
| `all-in-one/sources/decoded-original/0039-IdentXmlPart.xml` | `3ae955e5079c7e2f14f98035cffec43763714a9aa62d3b1defe86164aeb43486` |
| `all-in-one/sources/decoded-original/0041-IdentXmlPart.xml` | `f6879784dcb83569b01753a2986e4db4ddb411f64580d1e72c22c114dcdaae15` |
| `all-in-one/sources/decoded-original/0042-IdentXmlPart.xml` | `39a10a59ac8afcda3d1729f6b07dccea38c00227605c43cac46853fdc3e1b5e2` |
| `all-in-one/sources/decoded-original/0047-IdentXmlPart.xml` | `2e53bb895dd1ad2a74efaeb1ef16dfd61e62b1b2d7aa34cec8612f1b9cb0928e` |
| `all-in-one/sources/decoded-original/0063-IdentXmlPart.xml` | `9dceae18963ead11293cfc3a70c2eac077faa53ebd28e23bb4e84bc3278c5034` |
| `all-in-one/sources/decoded-original/0146-FlgNet.xml` | `c01421db51d744b648eeb19953a93b9d09bc6ea8eb8615ba5862be8220b08c75` |
| `all-in-one/sources/decoded-original/0149-FlgNet.xml` | `bc2519cdad49a7268006b194e8e5e1160744ff221f04b83e710f31f57bc617f9` |
| `all-in-one/sources/decoded-original/0159-FlgNet.xml` | `5598abbad86ed26fa8dd17fc3eca3e1c0b7941a2798db6ae1e2472a7ca448d2a` |
| `all-in-one/sources/decoded-original/0332-FlgNet.xml` | `c677499004010aba2746412a08e32f3e4206e9212d481fc08ee1c6023326cef7` |
| `all-in-one/sources/decoded-original/0343-FlgNet.xml` | `a2f41d7cce7c4d944f0cebdcacc964a1298962198a20f9471558902b39685d68` |
| `all-in-one/sources/decoded-original/0350-FlgNet.xml` | `3f426a4ba9455160b8113df968b1052752a7b72cdfca8e57bdfd466340d691ff` |
| `all-in-one/sources/decoded-original/0351-FlgNet.xml` | `1448cd179747074ae5ac3647c52e47950d18e0d90fa2f1cb155dbb24af50a7f6` |
| `all-in-one/sources/decoded-original/0352-FlgNet.xml` | `03e2d68dda289fcb7e7738c2f52e675890b252f5b526cab1ec2049323ab30d75` |
| `all-in-one/sources/decoded-original/0356-FlgNet.xml` | `5fdf9fada8777584ffcac96cc99cc532625d867754e0d6cdd03690e3fb9bff44` |
| `all-in-one/sources/decoded-original/0363-FlgNet.xml` | `90fc22646d834bfd3139806680e708b449798516cf0d7c0c65eaf86a2ab80d5a` |
| `all-in-one/sources/decoded-original/0366-FlgNet.xml` | `79ce47fc6656105cefa0ee138a30e85283bc9d481d432ca720fdca0668dda7e2` |
| `all-in-one/sources/decoded-original/0397-FlgNet.xml` | `bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834` |
| `all-in-one/sources/decoded-original/0455-FlgNet.xml` | `4d49d7acd2ef56ecb47252305453bae589897ab69315fc0cef32e1e156da1325` |
| `all-in-one/sources/decoded-original/0476-FlgNet.xml` | `0f9c48dddf61987d61094de9368ab534b56ec6c30e898dc2e4d81b64e86fa55a` |
| `all-in-one/sources/decoded-original/0480-FlgNet.xml` | `c14d2fee14b38b7c597edb46626676f0cf550b5831668884cb2fac341b559273` |
| `all-in-one/sources/decoded-original/0495-FlgNet.xml` | `0ff8eb8cf4b147a9077e5bcd88620216cea558cdf2cbb2c336c07b91014abfa4` |
| `all-in-one/sources/decoded-original/0507-FlgNet.xml` | `c73e066c3ff24d3a367b4f7e3b41b762747a6b3cb76f949ca1fea375392a8c02` |
| `all-in-one/sources/decoded-original/0513-FlgNet.xml` | `19107ffbb3144f4dc5dd070f0edb459166ae7a96c0715b65362f9a359c19412d` |
| `all-in-one/sources/decoded-original/0544-FlgNet.xml` | `7eea2ea628a9c9ba7b9df66e20f7bab670da7dc7a155084d80119943ed45e6ca` |
| `all-in-one/sources/decoded-original/0545-FlgNet.xml` | `a03d835805d14368bf07d1eed1520d90f7a1de7d70a52c5f70ccc800fb3f5641` |
| `all-in-one/sources/decoded-original/0563-IdentXmlPart.xml` | `86cf35b6baebc079cb5a092baf53ec3364c377ea7318eb263ab69c8b4550b4ad` |
| `all-in-one/sources/decoded-original/0570-IdentXmlPart.xml` | `9fed133006458c3b43b1d5f2c15107a5a86b4fb7cdbaf3743bf88f0e5a105495` |
| `all-in-one/sources/decoded-original/0571-IdentXmlPart.xml` | `4a9deeb65a22e497e284fe6d98929e1d201ef5939e4aeca5805b4eb7e007d398` |
| `all-in-one/sources/decoded-original/0572-IdentXmlPart.xml` | `5ecd18f84e12d702bb46f759b23994dacfa2d97d50fe51e766ca0cf43f75bb4c` |
| `all-in-one/sources/decoded-original/0573-IdentXmlPart.xml` | `a22cc24a974e0c792f32e356a14b277a847e2bb204c91bce01c37d1714ddb56c` |
| `all-in-one/sources/decoded-original/0585-IdentXmlPart.xml` | `e36ec18aa4abebea8f9160254522bb51ff722eae804c5a469790f85f02939184` |
| `all-in-one/sources/decoded-original/0613-IdentXmlPart.xml` | `09d3b1397a987898334218f37e025661af162438582e649f671e7abec443d3cb` |
| `all-in-one/sources/decoded-original/0615-IdentXmlPart.xml` | `80f4544edca56c6e6bb2713c758c92ade9202255110074931e03fe34d0d0801a` |
| `all-in-one/sources/decoded-original/0616-IdentXmlPart.xml` | `650b53354a0c8443d94adc5bd6a860d3c5313014a52e0fb98a5656a65b58cc0d` |
| `all-in-one/sources/decoded-original/0617-IdentXmlPart.xml` | `10bcf85169cb2512f55acadaef299a3d46b4b4cecd88032d739cfeba23e94aa9` |
| `all-in-one/sources/decoded-original/0618-IdentXmlPart.xml` | `0c6762de9cdf0e294317f7463bea3d8e6df5673d333d9b1826ebd17a7ded044c` |
| `all-in-one/sources/decoded-original/0619-IdentXmlPart.xml` | `85694bb5b696e31e6a1217431112e5b750516c4f94078d6e127d4394a8b80456` |
| `all-in-one/sources/decoded-original/0620-IdentXmlPart.xml` | `da97226a148a1a8babaea67db412761a718b7e7537212b7807e8ea27d000d2d3` |
| `all-in-one/sources/decoded-original/0621-IdentXmlPart.xml` | `a63e2b97ea9eb2691cb478666afed77fc58a2da2f8170422dc09e24b102c88ee` |
| `all-in-one/sources/decoded-original/0622-IdentXmlPart.xml` | `f0b997f1246d76cff71de2160eb617caa936e6987bdf43c73f55cdcf77dccdb6` |
| `all-in-one/sources/decoded-original/0623-IdentXmlPart.xml` | `4acd00406ea92466169e57e59fc90b0da4d9ec55fd19e2e96c9556e939cb83a6` |
| `all-in-one/sources/decoded-original/0624-IdentXmlPart.xml` | `24607c0827fbde428bccf8637ef4ae490798a69a7c2f3b87861d0749082d367a` |
| `all-in-one/sources/decoded-original/0626-IdentXmlPart.xml` | `a9d7fbea345eca70325a8c2e44058c23e96add1b7207eabbb09445118b18188b` |
| `all-in-one/sources/decoded-original/0627-IdentXmlPart.xml` | `08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb` |
| `all-in-one/sources/decoded-original/0628-IdentXmlPart.xml` | `9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd` |
| `all-in-one/sources/decoded-original/0629-IdentXmlPart.xml` | `67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972` |
| `all-in-one/sources/decoded-original/0654-IdentXmlPart.xml` | `b36294f3aad24be72a052bef61c875ca4695d7e101c385cf55bdadec41d5097e` |
| `all-in-one/sources/decoded-original/0656-IdentXmlPart.xml` | `0dbc45e84732a8848f17b094ea08ab8578dbf240bfe15cd7086859395c27c592` |
| `all-in-one/sources/decoded-original/0657-IdentXmlPart.xml` | `0f70cda60a6b1a17175876d58e25b2686952642de6cffb21213aeef8b347a22b` |
| `all-in-one/sources/decoded-original/0658-IdentXmlPart.xml` | `998294c0c8a99e00ceb33c2c60def2cd4850e34328917ae506244c2be2df3831` |
| `all-in-one/sources/decoded-original/0659-IdentXmlPart.xml` | `ec881805a45730533bccd780e152afb9c9d7c7c45ba7587538b92239f9cbd9d2` |
| `all-in-one/sources/decoded-original/0660-IdentXmlPart.xml` | `0bf4f4c46531f55324602f4f7b1a1e0b9e63df2c6278126f6e5cf1bc9a06509f` |
| `all-in-one/sources/decoded-original/0665-IdentXmlPart.xml` | `50e88d5f50f555151b35cfb17225e766c34ef6b490bd3a48e0a4e335fd17e3dd` |
| `all-in-one/sources/decoded-original/0667-IdentXmlPart.xml` | `ef924ced3e0e2b17e9c8440eb4946cd50d55df644c6ec24a1c4fd288fa6b73a3` |
| `all-in-one/sources/decoded-original/0668-IdentXmlPart.xml` | `2248e994a0a02cd37c5c5edaca199b3421068feea91e2e8616560e814ef9f6ed` |
| `all-in-one/sources/decoded-original/0669-IdentXmlPart.xml` | `754c513339d00918717010047b8f9d865d8674c6978a6f86c6f1fa5d683506e2` |
| `all-in-one/sources/decoded-original/0670-IdentXmlPart.xml` | `e56f3f0c4f2a86dd18578dedd4453915c2a51cd25e2cd9feced8538171a00841` |
| `all-in-one/sources/decoded-original/0671-IdentXmlPart.xml` | `26cb51706305c372d512c19770648bb0dbb74df8bd2277b1e0da1b8c88cca293` |
| `all-in-one/sources/decoded-original/0672-IdentXmlPart.xml` | `6bfc2ba142d6270c39eb1f13b2886204865af6d46eadc5f410c26981b8da9222` |
| `all-in-one/sources/decoded-original/0673-IdentXmlPart.xml` | `450ef74e2d2fb65dfbb5f6bad9e28ccacf6bf0caf64327a0e20aff84d6e40f58` |
| `all-in-one/sources/decoded-original/0674-IdentXmlPart.xml` | `4770702f519bacda69202bb2f7733d983074bda90964360c238f990d9d08fd84` |
| `all-in-one/sources/decoded-original/0675-IdentXmlPart.xml` | `b1902886927d8403fab736d9c8ffe73f2fbc8ce4b7ca7c345144964668b051c3` |
| `all-in-one/sources/decoded-original/0676-IdentXmlPart.xml` | `c58427c5b0ac6c11cdb52e4c6d0461c7b191fae81ccace191048e9f175fcec59` |
| `all-in-one/sources/decoded-original/0677-IdentXmlPart.xml` | `69922fcc5c67d00cdf1c5f712efa3db7638d20c88318d35fe6196467796ab1e3` |
| `all-in-one/sources/decoded-original/0678-IdentXmlPart.xml` | `51e637e0b9713c028810f2a717b5c3804a3a26c2f1be7e332a4d6bf277bfc382` |
| `all-in-one/sources/decoded-original/0679-IdentXmlPart.xml` | `d0fcb93e188c8ae2ae0c0423f0b78b129bf3c168e33a6855262d34b8682b9b56` |
| `all-in-one/sources/decoded-original/0680-IdentXmlPart.xml` | `fd551ad5d47bbd66c6bcdcc1949aaddf68cc086a3ddf6fb337adc767954c2b95` |
| `all-in-one/sources/decoded-original/0688-IdentXmlPart.xml` | `ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda` |
| `all-in-one/sources/decoded-original/0690-IdentXmlPart.xml` | `fcd6af9e8af48f9737d4764d7765d2eebdf95bd5e0c8e7b4faf6d1ed4eba1541` |
| `all-in-one/sources/decoded-original/0692-IdentXmlPart.xml` | `bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037` |
| `all-in-one/sources/decoded-original/0694-IdentXmlPart.xml` | `757ccebdf32d0a168dd787bfa735fe6494eac4c4a9f7a5adc63898a88e8b152d` |
| `all-in-one/sources/decoded-original/network-map.json` | `c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60` |
| `all-in-one/sources/electrical-page-text.json` | `4b846819aab7e1306aebea617042f9f9ffe0c8aee1930e6f3db035bea3739153` |
| `all-in-one/sources/hmi-windows.csv` | `15f8d69b5c43d4fdbe550f9cd2717f855fea877ed8146973054cb6dbcaa9892e` |
| `all-in-one/sources/hmi_plc_tags.csv` | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` |
| `all-in-one/sources/live_index.json` | `14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1` |
| `docs/equipment-standard/INVENTORY.json` | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` |
| `docs/equipment-standard/WORK-ITEM-TEMPLATE.md` | `4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586` |
| `docs/equipment-standard/WORK-STANDARD.md` | `05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99` |
