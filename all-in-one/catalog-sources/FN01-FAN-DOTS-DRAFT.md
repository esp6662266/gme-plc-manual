# FN01-FAN · FN01 모터 냉각팬 — 독립 구성품 조사 초안

## 핵심 확인·상충·누락 먼저

- **별도 catalog ID FN01-FAN**이다. 부모 FN01의 완료·주팬 M22·인버터·진동 ZT01·주팬 고장/기동시간을 이 구성품에 상속하지 않는다.
- **독립 잔존 I/O 있음:** 백업 `star fan fn01` `%Q3.5`, `fn01f_fbk` `%I4.5` Bool 선언을 확인했다. **직접 출력 기동 Coil/FB, 직접 피드백 접점은 복원 XML 이름 결속에서 미확보**다. 다만 `IW4→DB13.DBW4`, `QW2→DB14.DBW2` Word 미러에 해당 주소 범위가 포함되므로 “완전히 읽지 않음”으로 단정하지 않는다.
- **고유 잔존 논리:** 0166/LAD1847 NID5의 `Flag.M_FN_01_FAN` RCoil, 0339/LAD1052 NID54의 `hours motors.FN_01_FAN_HOUR` Int 0 쓰기를 독립 확인했다. 전자는 내부 요청 Reset이고 Q3.5 writer가 아니다. 후자는 운전시간 누적이 아니라 공통 시간 초기화 경로다.
- **상충 유지:** OEM FG54/PDF55 전체 SPARE, FG120/PDF121 E4.5 SPARE, FG139/PDF140 A3.5 SPARE. 세 페이지 모두 개정란 **Rev2, 17.03.2025**, 작성일 27.05.2024. 시공 PDF51에는 M29 케이블이 존재한다. 둘을 임의로 합쳐 설치/철거/사용 여부를 확정하지 않는다.
- **알람 이름 잔존:** live_index `_7ev/1697` interface에 `fn_01_fan_fault`가 있다. 이름 존재와 발생/지연/래치/ACK/복구 로직을 구분한다. 직접 알람 XML 근거와 독립 HMI 이벤트는 미확보다.
- `live_index` 1034 제목 `fn-01 fan deleted`, 1200 제목 `fn01 fan deleted`는 모두 레코드 `deleted:false`다. **제목의 deleted를 백업 레코드 삭제 플래그 또는 현장 철거 증명으로 바꾸지 않는다.** 두 레코드 values에 LADFBD Code 본문 없음, network-map에 복원 네트워크 연결 없음.
- 공유 근거: 고정본 `devices/signal-guides/circuit-guides/construction-guides/FN01-FAN.html`을 색인으로만 활용했다. `drafts/SYS-PLC-IO-DOTS-DRAFT.md`의 공통 호출/Word 미러 설명은 연결 재사용하되, 이번 구성품의 해당 Word 핀과 도면 5페이지는 직접 재확인했다. 기존 매뉴얼의 시뮬레이션·일반 진단 절차는 실행 승인이나 이번 결과가 아니다.

## 1. 설비·자료 기준

| 항목 | 확인 및 경계 |
|---|---|
| 대상 | `FN01-FAN`, FN01 모터 냉각팬, motor, 연소·열회수, parent=`FN01`, depth1, phase2 |
| 대장 | `docs/equipment-standard/INVENTORY.json` catalog[118], not_assessed/planned 상태 보존. 부모·하위 별도 집계 |
| 역할·별칭 | FN01 구동부 냉각 보조장치; `star fan fn01`, `fn01f`, `fn_01_fan`. FAN이라는 이름으로 FN01 주팬 전체를 가리키지 않음 |
| 읽기 전용 기준 | `gme-research/source-mv06`, commit `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, VERSION 1.12.0 |
| 직접 원본 | 아래 XML 선언·핀, live_index 백업 추출, HMI CSV, OEM 및 시공 PDF. 파생 HTML/network-map은 탐색/결속 보조 |
| 자료 시점 | 백업 심볼/복원문서/도면 시점의 증거. 현재 CPU·현재 설치·전원·보호 설정·정상 극성 증거 아님 |
| 실행 범위 | 문서·XML 정적 파싱, PDF 렌더, 파일 해시 비교만. TIA 컴파일/CPU접속/현장조작/시뮬레이터 작성·수정·생성·실행·행동시험 모두 미수행 |
| 모델 | 모델/추론 수준의 런타임 독립 증명 미확인 |

근거 경로의 `XML/`는 `all-in-one/sources/decoded-original/`, `S/`는 `all-in-one/sources/`를 뜻한다. UID/RID는 **해당 파일과 NID 문맥 안에서만** 연결한다.

## 2. I/O·HMI

| 신호 | 선언·주소·범위 | 직접 근거와 해석 |
|---|---|---|
| `star fan fn01` | Global Bool Output `%Q3.5` | `S/live_index.json` _7ev/997 Address `%q3.5`; Comment `a 53.5 fn-01 motorcommand cooling fan`. 설명의 A53.5를 주소로 사용하지 않음. XML0555 RID30, NID -2147483648 UID80 AK Monitor, AO29; XML0556 RID256 UID41 AK Monitor AO29. Monitor 선언은 실행 Coil 증거가 아님 |
| `fn01f_fbk` | Global Bool Input `%I4.5` | live_index1057; XML0556 RID257 NID -2147483648 UID40 AK Monitor AO37. 접촉기 응답 이름이며 실제 회전센서·정상값1로 단정하지 않음 |
| `Flag.M_FN_01_FAN` | Global Bool, DB2.DBX1.7 | XML0577 RID98, NID5 UID995 OID8 AK Write, BO/AO15 BS1, BAD3; XML0576 DepDBBlock Flag RID3 TOD2. RCoil907만 고유 이름으로 결속 확인 |
| `hours motors.FN_01_FAN_HOUR` | Global Int16, DB9.DBW142 | XML0615 RID222 NID54 UID3025 AK Write, AO1136 BS16 BAD5; XML0614 hours motors RID5 TOD9. 초기화 Writer 확인, 실제 누적 기능 미확보 |
| `Tag_48` | Global Timer `%T17` | XML0613 RID284 NID54 UID3023, Timer AO17; live_index108 Address `%t17`. 팬 기동/고장 타이머가 아닌 공통 운전시간 기록 후 Reset 타이머 |
| `fn_01_fan_min`, `fn_01_fan_fault` 등 | 백업 interface 이름 잔존 | live_index20 시간 멤버, 1697 알람 멤버, 351 `star fan fn01`, 1065 `feedbackmotor fn-01 fan`, 452 요청 멤버. interface 이름만으로 실행 핀·절대 주소·현재값을 보충하지 않음 |

### Word 전달은 직접 심볼 부재와 별개

- 입력: XML0397 / LAD1070 NID1, ORef36 RID10 `Tag_180` → Wire39 → Move35.in; Wire40 Move35.out1 → ORef37 RID11. XML0627 RID10 Global Word Input AO32 SAM=None=`IW4`; XML0629 RID11 Word AO32 BAD4 AK Write 및 XML0628 Inputs RID4 TOD13=`DB13.DBW4`. **I4.5를 포함하는 Word 원시 복사**이며 주변 비트와 공유한다. P35 `DisableENO=true`이나 Wire41은 P27.eno→P35.en 연결이다. 속성과 연결을 함께 보존한다.
- 출력 관찰: XML0401 / LAD356 NID1, ORef35 RID28 `Tag_281` → Wire59 → Move23.in; Wire61 Move23.out1 → ORef36 RID50. XML0632 RID28 Global Word Output AO16=`QW2`; XML0633 RID50 Word AO16 BAD26, XML0064 Output RID26 TOD14=`DB14.DBW2`. **Q3.5를 포함하는 출력 Word를 DB로 읽어 옮긴다. DB→Q 쓰기로 역해석하지 않는다.** P23 `DisableENO=true`, Wire57 P22.eno→P23.en, Wire60 P23.eno→P24.en.
- 공통 호출: XML0030 / LAD1613 NID19에서 Wire33 CRef23.eno→25.en, Wire42 CRef25.eno→Contact37.in; Wire44 ORef45/RID140 `Simulation(1)`의 NOT 접점, Wire43→CRef28.en. XML0688 FCBlock RID128 FC19 HMI Output / RID135 FC15 HMI Inputs, XML0692 RID140 Global Bool Memory AO1440=`M180.0`. 호출 ENO 및 현재 모드는 미확정. 중지된 기능의 실행을 뜻하지 않는다.
- HMI CSV 실제 행168 `I_W4`=`DB13,W4`, 행179 `O_W2`=`DB14,W2`, AccessName PLC. Word 관찰 설정이며 FAN 전용 화면/버튼/색상/ACK 이벤트는 미확인이다. 같은 CSV의 `FN_01\Flag` DB2.X1.2 등 **부모** 태그를 FAN 요청으로 옮기지 않는다. `FN01_Preathing_enable`도 FAN 직접 제어로 취급하지 않는다.

## 3. 제어 구조

### 3.1 FAN 내부 요청의 고유 Reset

원본 `XML/0166-FlgNet.xml`, LAD1847 auto start motors, 제목 `presetting sequence 5: complete engine stop`, NID5.

| 연결 | 원본 핀 및 의미 |
|---|---|
| 전단 허가 | Wire1097 rail→Contact1095.in; Wire1028 ORef983/RID4 `Flag.Auto_ON1`→operand; Wire26 out→Eq881.pre |
| preset 종류 | Wire1029 UID984/RID12 `Data.Tipo_preset`→881.in1, Wire1030 UID985/RID22 Int5→881.in2; Wire1031 881.out→Eq901.pre 및 Contact1130.in |
| 단계 비교 | Wire1040 UID992/RID7 `Data.Tempo_presetting`→901.in1, Wire1041 UID993/RID22 Int5→901.in2; Wire52 901.out→OR51.in1 |
| 공통 비상모듈 분기 | Wire1133 UID1131/RID108 `Allarm.Emergency_module_fault`→Contact1130.operand; Wire53 1130.out→OR51.in2 |
| FAN Reset | Wire1042 OR51.out→RCoil907.in (동일 분기에 CH01 905 및 부모FN01 909 있음); Wire1044 ORef995/RID98→907.operand |

XML0577은 Global Bool/Int 선언을, XML0578 RID22 NID5 UID985/993 `V=5`, Int16을 확인한다. 정적 식은 `Auto_ON1 AND Tipo_preset=5 AND (Tempo_presetting=5 OR Emergency_module_fault)`일 때 **M_FN_01_FAN을 Reset**한다. 여기의 5는 비교 정수로만 확인했으며 팬의 5초 기동지연으로 번역하지 않는다. RCoil은 Set/일반 Coil과 다르다. 이 가지에 NOT는 없다. 인접 부모 Reset을 FAN 전용 알람 또는 Q3.5 출력으로 합치지 않는다.

고유 이름의 Set·실제 Q3.5 Coil/호출 writer·I4.5 직접 사용·자동/수동 운전 우선순위는 확보하지 못했다. Word 및 간접 주소, 미복원/현재 프로젝트의 다른 Writer 가능성을 열어 둔다. 부재를 미사용/영구0/철거 완료로 단정하지 않는다.

### 3.2 시간 이름 잔존과 실제 0 쓰기

`XML/0339-FlgNet.xml`, LAD1052 time work motor index51, NID54:

- Wire3051 rail→Contact3049.in, Wire3034 ORef3023/RID284 `Tag_48`→operand.
- Wire3050 Contact3049.out→Move3008.en.
- Wire3035 ORef3024/RID12 Int0→Move3008.in; Wire3036 Move3008.out1→ORef3025/RID222 `hours motors.FN_01_FAN_HOUR`.
- XML0616 RID12 NID54 UID3024 `V=0` Int16을 확인했다. Wire3037 P3008.eno→다음 P3011.en은 LD01 등의 공유 초기화 체인이다. 다른 모터를 FAN 소유로 합치지 않는다.

별도 `XML/0341-FlgNet.xml` LAD1055 NID57 제목 `reset working hours after recording the data in the db`: ON Contact3147 및 Flag_Aggiorna_DB Contact3149→SCoil3110 MEM2_0; ON→MEM2_0 Contact3151→**NOT Flag_Aggiorna_DB** Contact3153→SdCoil3118. Wire3138 UID3128/RID334 `S5T#5S`→3118.value, Wire3141 UID3130/RID284 Tag_48→3118.operand. Wire3142 UID3131 Tag_48→Contact3155, Wire3156→RCoil3123, Wire3144 UID3132 MEM2_0 Reset. 이는 공통 DB기록 뒤 시간 Reset 지연이지 FAN 기동실패/회전감시 5초 근거가 아니다. ON은 이름의 신호이며 불변 TRUE로 치환하지 않는다. 실제 시간 누적·스캔순서·현재 DB값은 미검증.

## 4. 전기 전달 경로

직접 렌더 확인: `S/Electrical_Rev2.pdf` 실제55/121/140쪽, 각각 FG54/120/139. **각 페이지** Rev2 17.03.2025, 작성일27.05.2024 확인. CPU515·MOD 번호는 도면 표기이며 현재 하드웨어 증명 아님.

| 경로 | 실제 도면 끝점·구간 |
|---|---|
| 동력 | FG54/PDF55 `THREE-PHASE LINE 440V 60Hz`; 8.3L1/L2/L3 FG53/9→54QM1 주접점1-2/3-4/5-6→54KM1 주접점1-2/3-4/5-6→54U1/V1/W1→XM:54U1/54V1/54W1→54QS1 1-2/3-4/5-6→M29 FN-01 U/V/W 및 PE. 전원 연속참조 FG55/0. BLACK FS17 1.5mmq 표기 |
| 명령 출발 | FG139/PDF140 A3.5, 도면 CPU515 MOD14 **단자36**, SPARE 점선, 교차참조54/4→FG54 A3.5의139/1 참조 |
| 명령 직렬 경로 | A3.5→XS45→54QS1 보조접점→XS46→선54.1→54QM1 보조접점→54KM1 코일A1; A2→-0Vdc10.6. QS1/QM1 보조접점의 숫자는 이 렌더에서 미표기/미확정으로 남김 |
| 피드백 출발 | +24Vdc10.7→54KM1 보조접점13-14→E4.5→FG120/5 |
| 입력 도착 | FG120/PDF121 E4.5는54/6에서 들어오며 도면 CPU515 MOD9 **단자6**, SPARE 점선. 행 제목 FEEDBACK MOTOR FN-01은 FAN이라는 단어가 생략됐지만 FG54 교차참조 및 I4.5 백업과 연결. 부모 FN01 주팬 입력으로 바꾸지 않음 |
| 전원·보호 표기 | +24Vdc10.7/-0Vdc10.6 FG53/7→55/3. M29 표기는1.1kW·2.26A, 54QM1은2.2–3.2A 범위. **도면 원문값으로만 보존, 현행 보호 설정·조정 권고 아님** |

명령에서 밑의 접촉기 접점표를 별도의 부하 접점번호로 오독하지 않는다. 여기서 실제 그려진 부하 주접점은1-2/3-4/5-6, 실제 피드백 보조접점은13-14다. 다른 장치의 릴레이5/9 회로를 이 팬에 복제하지 않는다.

### 시공 문서와 SPARE 상충

`S/Electrical_Can_Decoating_20241118.pdf` 실제 p1 표지 FOR APPROVAL; p51 footer `CANDC-CONS-C001-051`, TOTAL-PAGE51/64, D-PAGE1, Rev1 24.11.11 `first draft design`을 직접 확인.

p51 행1_13 `=FLB+FN01-M29A`, FROM CR→TO FN-01/M29, 설명 COOLING FAN BLOWER FAN, CurrentType GAC, SPEC CV, CORE4, SIZE1.5, SPARE열0. Route1=`100`, Route2=`120 / RB`, Route3=`E1300`, Adjustment15, LEN65. Route2의120과RB를 별도의 순차 구간으로 발명하지 않는다. `SPARE=0`은 케이블 표의 심수 열이며 OEM 전체회로 `SPARE`와 같은 의미의 사용상태 플래그가 아니다. LEN65는 표 원문으로 실측길이로 취급하지 않는다. 바로 위 행1_12 M22는 **부모 주팬** 케이블이며 FAN 회로가 아니다.

도면 모터/케이블은 문서상 연결까지만 확인했다. 실제 명판·현재 양단 표찰·준공/승인본·설치/철거 기록은 미확보이며 반복검색하지 않는다.

## 5. 알람·복구

- 백업 interface `_7ev/1697`의 `fn_01_fan_fault` 이름 잔존은 기록한다. 이번 검색 695 XML에서 FAN 별칭 일치는 선언0555/0556, 요청0577, 시간0615 네 파일이었다. 직접 FAN 알람 생성·Set/Reset·지연·HMI ACK 호출은 결속되지 않았다. 이 수치는 검색 경계이며 695개 의미검토 완료가 아니다.
- `Emergency_module_fault`는 0166의 공통 정지 조건이다. FAN 자체 검출 경보가 아니다. 요청 Reset을 자체 고장 해제·접촉기 차단 확인·재기동 완료로 바꾸지 않는다.
- 부모 FN01의 inverter/absorbed current/진동 ZT01/주팬 기동 타이머와 HMI `FN_01\Allarme1`은 소유가 다르다. 이 초안에 팬 고장으로 복제하지 않는다.
- `Tag_48`의 S5T#5S는 공통 시간 Reset, FAN 자체 응답대기·재시동허가·안전 대기시간 근거가 아니다.
- 실제 원인 해소, 현재 알람 상태, ACK/RESET 입력, 운전 요청 잔존, 재기동 승인과 복구 결과는 모두 미확정. 시험·리셋·출력강제/보호값 변경을 지시하지 않는다.

## 6. 증상별 관찰 작업지

아래는 기존 자료/승인된 관찰 결과를 기록할 때의 비교 기준이며 조작·시험 절차가 아니다.

| 관찰 상황 | 구분하여 기록할 것 | 원인 단정 금지·필요자료 |
|---|---|---|
| FAN이 없거나 사용하지 않는다고 보고됨 | 보고시각·보고자, SPARE 원문, 명판/설치·철거 기록의 출처 | deleted 제목만으로 철거 판단 금지. 현재 승인 회로/설치대장 필요 |
| Q3.5=0 또는 제어 버튼이 없음 | 현재 프로젝트 버전·관찰 주소·모드, 직접 Q값과 DB14 Word 관찰값 | 복원 Coil 미확보를 고장 또는 자동 정지 증명으로 쓰지 않음. 승인된 현재 프로젝트의 writer 근거 필요 |
| Q3.5 관찰값과 접촉기 상태가 다름 | 동일시각 Q·DB14, XS45/46 및 KM1에 대한 이미 확보된 점검 기록 | 실제 회로 설치 확인 전 기동 시험 금지. 모터 회전과 코일/보조접점 응답 분리 |
| I4.5 표시가 다름 | 원시 I4.5와 DB13.DBW4, HMI I_W4의 시각/출처 | 정상극성 또는 실제 회전 증명으로 단정하지 않음. 공유 Word 호출·현장 접점 의미 필요 |
| 팬 운전시간이 0 | DB9.DBW142 및 Tag_48 관찰 근거, DB기록 시점 | 0339는0 쓰기이며 기동하지 않았다는 증거가 아님. 누적 writer는 미확보 |
| FAN fault가 언급됨 | 정확한 태그/주소·원문 메시지·시간, 부모FN01 경보와 분리 | 알람 이름 잔존만으로 검출시간·자동복귀 발명 금지 |

공통 기록 필드: 장치ID/관찰자/시각·시간대/자료버전/주소·형식/값·단위/도면FG·실제페이지/양단식별/판정근거/미확정. 실제 운영기록·사진을 생성하거나 공개저장소로 복사하지 않았다.

## 7. 완료·누락·인계

| 영역 | 이번 상태 | 남은 경계 |
|---|---|---|
| 설비·자료 기준 | 구성품 고유 문서 검토 | 현물/승인 설치 미확정 |
| I/O·HMI | 잔존I/O·내부요청·시간·공유Word 확인 | FAN 전용 HMI 이벤트/현재 writer 미확보 |
| 제어 | 요청 Reset·시간0·공유타이머 의미 검토 | 실제 FAN 기동/피드백 기반제어·호출순서 미확정 |
| 전기 | OEM3쪽 및 시공표지/케이블표 직접 확인 | 실제 배선·접점 극성·현재 보호/명판 미확정 |
| 알람·복구 | 이름잔존/공통정지/부모소유 분리 | 고유발생·지연·복구 근거 미확보 |
| 증상관찰 | 비조작형 비교표 작성 | 실측/관찰/복구 결과 없음 |
| 완료 | **구성품 문서조사 초안 준비** | 부모완료상속 없음; 현장/프로그램 적용 완료 아님 |

네 기능(도면·래더 비교, 선택 백업복원, 전후 기록 비교, 보고서/PDF)은 이 문서와 근거를 통합할 수 있는 후보이나 이번에 구현·UI/저장·재열기·출력검사를 수행하지 않았다. 기존 note/repair_observation/미지필드·타설비·초안·저장키를 변경하지 않았다.

상태: documentation=draft_ready; static_review=selected_source_review; ui_records=not_run; publication=not_published_by_this_work; tia_compile/live_cpu/field_recovery=not_performed. 시뮬레이터 행위0, 원본/프로그램/버전/공개대장/배포/PLC/보호설정/SEJIN 변경0. 업로드·사용자전송0.

실제 시각(UTC): 2026-10-11 13:05:03 착수; 13:05:16 배치/대장/AGENTS 열람; 13:06:16 OEM FG54와 시공51 렌더 판독; 13:07:04 OEM FG120/139 판독; 13:07:57 시공표지 판독 및 공통근거 대조; 13:08:46 선정39파일 해시·Git blob 비교. 시각은 실제 도구 수행/결과에 근거하며 소요시간 추정이 아니다.

검사 산출물: `gme-research/extracts/FN01-FAN/checks.json`, `selected-source-hashes.json`, `selected-live-index.json`, `network-index.json` 및 렌더PNG5개. 선택파일39개와 695 XML 별칭검색, 핵심5네트워크/호출부분 의미검토를 별도 계수한다. 원본 Git 작업트리 clean 확인. 원본 생성기/build/test/시뮬레이터 실행 없음.

다음 판단은 **새 승인자료가 들어올 때만** 현재 설치 여부·Q3.5 writer·알람 구현·HMI 이벤트·현장 복구를 대조하는 것이다. 새 자료 없이 같은 실물 보류를 재검색하지 않는다.

## 부록. 선정 원본 전체 SHA256 및 고정 Git blob 내용 일치

다음39개는 이 초안의 선정 원본/기준/색인이다. SHA256은 전체 파일 바이트, Git blob은 고정 abcf31c의 해당 파일 객체이며 `cat-file blob` 내용과 작업트리 바이트를 비교했다. 전체 저장소 모든 파일의 의미검토나 보호자산 전수 재검증 주장으로 확대하지 않는다.

| 원본 경로 (source-mv06 기준) | SHA256 | 고정 Git blob | 바이트 일치 |
|---|---|---|---|
| AGENTS.md | 0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2 | 073164bc6efd5791032d62c71b03b4dab48cb6f8 | True |
| .agents/skills/gme-equipment-rollout/SKILL.md | fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b | 9aa820ea6ca15b4e136c9772423b78ed4df6a3d4 | True |
| docs/equipment-standard/WORK-STANDARD.md | 05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99 | f76a570cc73098632e08759b17934000f7e3a253 | True |
| docs/equipment-standard/WORK-ITEM-TEMPLATE.md | 4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586 | e546f39535d2b589e80f97db869ac37ce4d05cfd | True |
| docs/equipment-standard/INVENTORY.json | 720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc | 587c3748ad9224718f95ba06463fee913dae231d | True |
| VERSION.json | 5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7 | fffb51663b7705aec91cb119ca80ee943a4ce758 | True |
| all-in-one/sources/Electrical_Rev2.pdf | 5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6 | f610fd7c7ce14ae951b00cff57b969259bfb389d | True |
| all-in-one/sources/Electrical_Can_Decoating_20241118.pdf | 3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd | 0ee6b6f8361c5790864dbba4bbd9d55e8e7c08f8 | True |
| all-in-one/sources/live_index.json | 14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1 | e35ccea1f841349c632666c29954b7bcd4f5839e | True |
| all-in-one/sources/hmi_plc_tags.csv | a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404 | cf4c0650e7c7baac350dcb89909b808435704880 | True |
| all-in-one/sources/block_summary.json | 68253f9366908244a27ed461c66d465da7ec1723571f27deaa9a6f81a542de63 | 15b570a011645023dbfca2d5332a9e0ae3b0a7b6 | True |
| all-in-one/sources/decoded-original/0064-IdentXmlPart.xml | ce6afc4f7ca0a8059c2e3cab25d202f0faaa49a3bc6a2e9ee238964a76e9fc9d | 300d74239868f4f4595d4d5bbb848b4b58bbae76 | True |
| all-in-one/sources/decoded-original/0030-FlgNet.xml | 9252c9da764993de1edb8b2e44c46d6e9f9d4b6118e751a0dbeaa9ffd8ea721b | e74c70b751acdcdbc7a8b3b0c98aa773c2107cab | True |
| all-in-one/sources/decoded-original/0166-FlgNet.xml | 0330a505877be92172f94bce83222a0bfc8d64aab700a69fc1fa2188010d3853 | 6b3062ae9ac2bc6ad8c2509d3fc4c15609a4b892 | True |
| all-in-one/sources/decoded-original/0339-FlgNet.xml | ce2c6279b55c8a5ac837a0f7c7a0945636df7dc52b68a1c3d6ec158234b37543 | df1b2a3dd9389a264ed6cebee9c4e3a7270fc6fb | True |
| all-in-one/sources/decoded-original/0341-FlgNet.xml | e9921cb52ecba4ef1df14758d29e4091fc510a8e792130e855b869dbab4a1c96 | 45dbda06a692b21380a52207a22094b2e0a9c5a3 | True |
| all-in-one/sources/decoded-original/0397-FlgNet.xml | bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834 | 4ab8370493c4e28fc1eabeeebe2743d27f0c4021 | True |
| all-in-one/sources/decoded-original/0401-FlgNet.xml | 60171c213e666de544077b7e4b497675813f7c0e75df85a3e76ab1def49b04ae | aadefbd35d305dd4a1146bf383b988a903802bf4 | True |
| all-in-one/sources/decoded-original/0555-IdentXmlPart.xml | 46c36333e249dd775c1db94a1f6e80a36cf1a5a9c998b7d0980ae01d862901e6 | 9a915a8b9a260b48402df151c1fe0bbcb2f4ea1c | True |
| all-in-one/sources/decoded-original/0556-IdentXmlPart.xml | 065d71114e26c93af180265e0e6d59d2a190af1f2f0581c5265e7f4f67d6e23f | 15ae569ff390ef5c791b0f76d96bd86d5ec6b938 | True |
| all-in-one/sources/decoded-original/0576-IdentXmlPart.xml | c8b5f9b9ead0e124f1f817b49d89611ed7b2ce04ecd91ddaa139f2ec89d48dbe | 819b47160eaa6d08c212f71e5b5486ef5b55b6f2 | True |
| all-in-one/sources/decoded-original/0577-IdentXmlPart.xml | 511e01fae619dc385357908a1ac62030dbdfd5f5399bd4c22bc58bebbfc3bf47 | a505ebf7efd05a85850dc29559a4f71242bacae3 | True |
| all-in-one/sources/decoded-original/0578-IdentXmlPart.xml | 0f9f41b5dee25ea17c7a29ab6f7b00503c13d0f265266acd660072baf061d32b | 070a79fb12139898dd44a17ab2061e795956b9c6 | True |
| all-in-one/sources/decoded-original/0613-IdentXmlPart.xml | 09d3b1397a987898334218f37e025661af162438582e649f671e7abec443d3cb | c9d19a48e947098914f4d2de3348c05b4f6d37e8 | True |
| all-in-one/sources/decoded-original/0614-IdentXmlPart.xml | c6de26f74d75f5be858a406de75eaf6faf62ba9b89c8f9a085b5dd206e93d294 | da0485aa033700f08c8695d30b93ebd2d377d6c7 | True |
| all-in-one/sources/decoded-original/0615-IdentXmlPart.xml | 80f4544edca56c6e6bb2713c758c92ade9202255110074931e03fe34d0d0801a | 49eb86fe01feb83de8c0864b21493d305aff8b20 | True |
| all-in-one/sources/decoded-original/0616-IdentXmlPart.xml | 650b53354a0c8443d94adc5bd6a860d3c5313014a52e0fb98a5656a65b58cc0d | 9f7fdd5f93ac149c139a054ebb34f63c632ef7fd | True |
| all-in-one/sources/decoded-original/0627-IdentXmlPart.xml | 08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb | 61ebc0abbb2ca160e11e1da400a3f14a397d8bc5 | True |
| all-in-one/sources/decoded-original/0628-IdentXmlPart.xml | 9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd | 170ca5c72599edc7ea7eefe651c3680ce325e76a | True |
| all-in-one/sources/decoded-original/0629-IdentXmlPart.xml | 67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972 | 058129bb01e27f7a6a0d0293f332d745e5bab74e | True |
| all-in-one/sources/decoded-original/0632-IdentXmlPart.xml | fd162c603476c2cac899010cee7a8ee382b6092c115135e3ac1007ae71c544e9 | 600935fa8d394c0d247ea20040d5dfff4f05b500 | True |
| all-in-one/sources/decoded-original/0633-IdentXmlPart.xml | 9e00aa275fa1b4e488b73983b309c6b73dcf4f3dd9be5dec13e9975d68f3c0fc | a1ab5ee12addbc92d04c9950d4437e2b564d6b5c | True |
| all-in-one/sources/decoded-original/0688-IdentXmlPart.xml | ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda | 463585759f1ecd94f32362b4fefb000a152f5773 | True |
| all-in-one/sources/decoded-original/0692-IdentXmlPart.xml | bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037 | 737785d03b5fad43c5b4d451955726d800edb1c0 | True |
| all-in-one/sources/decoded-original/network-map.json | c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60 | 424430b6b953e43138e5d0a18ca40c949e21cfa1 | True |
| all-in-one/devices/FN01-FAN.html | 7c2cc63189260b3f31aba9ef765b580d7e7f9a797cb3a6473a3dbbbe100804b3 | d831825f321204511272a46b5403d0c3a9cfc036 | True |
| all-in-one/signal-guides/FN01-FAN.html | 8a2fc904778228ff41e4b69387e1e8dd07455d357de555f5e6d3e49631298c7a | 012fdf822ac1a8a7235267d5f9be6d8b2bfd4e4b | True |
| all-in-one/circuit-guides/FN01-FAN.html | f4ca4afbfa1b462ccea6f24858d6bf1e5f3b772d65cddb2776aa2dbdf90b1cc3 | c7d821ac9fd6b377a82a966869af201711e472fa | True |
| all-in-one/construction-guides/FN01-FAN.html | a40acf3198eab6efeae7e47828e3e54e525c37bd56e8f4ef52f3a0752af83771 | 894d9b2275fd44e9d4d4aecf131d4922ab45cf1c | True |
