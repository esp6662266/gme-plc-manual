# FN05 석회 계통 송풍기 — 7영역 원본 조사 초안

- 표준: GME-STD-1.0.0 / WORK-ITEM-TEMPLATE 구조 적용.
- 대상: catalog_id `FN05`, kind `motor`, group `집진·석회`, parent_id 없음, depth 0, priority_key 없음.
- 작업 구분: 사용자 작업 3의 첫 배치 클라우드 사전조사. 전체248/우선23을 실제 ID로 대조한 신규 후보의 조사 초안이다. 로컬 목표의 **2차133 통합·게시 제외는 그대로 유지**한다.
- 읽기 전용 고정 기준: `source-mv06`, Git `abcf31c5030bc7ef8749ed8e869a857f2387a28a`; VERSION.json `1.12.0`. 로컬 Git에는 태그 참조가 없어 exact-match tag 검사는 불가했다. v1.12.0은 VERSION.json의 선언이며, 이번 작업에서 배포 태그/현행 게시물을 재검증한 것은 아니다.
- 조사 시각: 2026-10-11 08:56 UTC 착수, 09:09 UTC 초안/자체 정적검토 종료. 실행 모델/추론 수준은 이 조사 세션에서 독립 관측 불가하여 미확인으로 기록한다.
- 작성 범위: 이 MD와 `gme-research/extracts/FN05/`만. 원본 repo·공통 스크립트·공유 declarations.json·버전·대장·운영 기록은 수정하지 않았다.
- 검토 상태: 원본 구조 자체 대조와 정적 검사는 수행, **핵심 근거 최종 문서 검토 완료; 사용자 독립 검토 대기**. TIA 컴파일·현재 CPU·실물·현장 복구·UI/기록·게시 검증은 미수행.
- 시뮬레이터 작성/수정/생성/실행/행동 시험, 실제 PLC/현장/보호값 변경, SEJIN 프로그램/운영 자료 변경 없음. 원본에 남아 있는 중지 경로의 존재와 해시만 보존한다.

## 먼저 확인할 결론

1. FN05는 대장상 독립 root이며 우선 대응18·제외90·부모보류7·SYS-SIMULATION와 별개다. FN04 조건이 FN05 네트워크에 있다는 이유로 FN04 하위 또는 중복 설비로 합치지 않는다. ER01 역시 독립 root다.
2. FN05 직접 출력은 `Start FN05 %Q4.7`, 원시 피드백은 `FN05_Fbk %I6.0`, 처리 응답은 `Inputs.FN-05 RUN DB13.DBX6.0`이다. 세 신호와 HMI 응답 DB11.DBX66.0을 분리한다.
3. LAD1970의 FN05 요청 Reset은 `ON AND (FN_05_FAULT OR (NOT FN04 Run AND NOT UNDER TESTING))`다. FN04의 처리 Run이 정지 조건에 들어간다. 출력 코일 자체는 `ON AND M_FN_05`이며, 같은 네트워크의 선행 Reset과 실제 스캔/다른 쓰기를 분리해 읽어야 한다.
4. 고유 FAULT는 LAD1814에서 `Start FN05`와 처리 Run의 불일치를 `Tag_79 %T96 / S5T#2S`로 감시하고 Set/Reset한다. FN03의 35초, FN06 별칭 알람 등 다른 팬 자료를 복제하지 않았다.
5. FG65/PDF66은 24Vdc 접촉기 직접기동 M41 회로다. **FG65의 5.5 kW·10.3 A와 PID의 6.3 kW가 상충**, 보호기 표기 **FG65 10–16A와 재료표 FG254/PDF257 11–16A가 상충**한다. 실물 정격·보호 설정·교체 품번은 확정하지 않는다.
6. HMI 3개 설정 태그는 확보했으나 FN05 호출의 핵심 ORef 4개 선언 연결과 실제 화면 이벤트는 미확정이다. DB2.DBX3.1 요청 태그와 Q4.7 실제 출력을 같은 태그로 쓰지 않는다.

## 7영역 적용표

| 영역 | 적용 판정 | 작성 위치 | 한계 |
|---|---|---|---|
| 설비·자료 기준 | 적용 | 1 | 이름·공정·관계는 백업/도면 기준. 실물 동일성 미확인 |
| I/O·HMI | 적용, 일부 근거 미확보 | 2 | 물리/DB/Timer/HMI 분리. HMI 객체 이벤트·일부 핀 결속 부족 |
| 제어 구조 | 적용 | 3 | Part/Wire/ORef/RID/NID로 직접 대조. 현재 실행·다른 쓰기·최종값 미확인 |
| 전기 전달 경로 | 적용 | 4 | PDF 실제 렌더 7페이지/상세영역 검토. 현행 시공·정격·보호값 상충 |
| 알람·복구 | 적용 | 5 | 고유 FAULT·2초·Set/Reset 확보. 재요청·실제 복구는 미검증 |
| 증상별 수리 | 적용, 관찰 설계 | 6 | 관찰 위치/비교/배제 기준만 작성. 실수리·시험 미실시 |
| 완료 기준 | 적용 | 7 | 조사 문서·정적·UI·게시·TIA·CPU·현장을 분리 |

## 근거 읽는 법

별도 표시가 없으면 경로는 고정 repo의 `all-in-one/` 아래다. `D/`는 `sources/decoded-original/`의 약칭이다. XML이 한 줄인 경우 불안정한 행 번호 대신 **파일 + Part/Wire UID + ORef/RefId + 선언 RID/NID**로 재현한다. LAD 숫자는 검색 문서 ID이며, 블록 내부 NID와 다르다. 예: LAD1970=NID40, LAD1814=NID36.

`network-map.json`, 네트워크 HTML, CSV/제어명세는 탐색·색인 자료다. 아래 핵심 논리는 해당 XML과 IdentXmlPart 원문을 직접 대조했다. 해시 전문은 부록과 `extracts/FN05/source-hashes.json`에 있다. PDF페이지는 1기준이고, FG는 도면 인쇄번호다. **모든 페이지에 FG+1을 적용하면 안 된다.** 재료표 PDF257의 인쇄번호는 FG254다.

## 1. 설비·자료 기준

### 1.1 대상 대조와 소유 경계

- `docs/equipment-standard/INVENTORY.json`의 FN05는 `phase2/planned/baseline/not_assessed`, 부모·우선키·제외사유·보류부모 없음이다. 동일 대장에서 ER01은 `전기 히터/heater/집진·석회`, 부모 없는 별도 ID다.
- 읽기 전용 preflight 결과 `inventory_matches=true`: 248 ID, root108/child140, 우선23행/대응18, 제외90, 부모보류7, phase2 133 유지. `requirements-audit.json`, `all-in-one-data.json`의 과거 저장 해시와 현재 바이트 차이는 보고되어 있으나 ID/상태/대응 집계는 일치했다. 그 바이트 차이를 이번 FN05 수정이나 완료 실적으로 계산하지 않는다.
- `equipment-networks.csv`는 LAD1970을 FN04·FN05·SYS-SIMULATION에 함께 색인한다. 이것은 참조 검색 결과이며 FN05 소유 이전이나 중지 설비 분류의 근거가 아니다. 직접 출력과 FAULT의 소유는 아래 XML 선언으로 확인한다.
- FG65/PDF66: 제목 BLOWER FAN FN-05, 모터 M41. PID PDF1 상세: M41/FN-05 → ER-01 → VR-06/LD-01 투입 연결부와 공통 덕트로 이어지는 표시가 보인다. 배관상 연결을 PLC 소유/부모관계 또는 운전순서 확정으로 확대하지 않는다.
- 시공 참조 PDF36/51은 FN05 위치에 M41과 ER01을 함께 묶어 적는다. M41 케이블 1_27과 ER01 케이블 1_28은 별도다. 이 위치 표기를 catalog_id 병합 사유로 쓰지 않는다.

### 1.2 자료 시점과 충돌

| 자료 | 표시/근거 | 사용 경계 |
|---|---|---|
| GME_20250506.zap18 / PEData.plf | 원본 파일·해시 보존; decoded XML의 복원 바이트 위치 추적 | 파일명 날짜를 현행 CPU 백업 시점으로 보증하지 않음 |
| Electrical_Rev2.pdf FG65 | DATA 27.05.2024, 개정란 별도 값 미표시 | M41 5.5 kW/10.3 A, 65QM1 10–16A는 도면 표시 |
| 동일 PDF FG122 | Rev2 17.03.2025, DATA 27.05.2024 | 입력 모듈 설계 표기; 현재 CPU/모듈 입증 아님 |
| 동일 PDF FG140 | DATA 27.05.2024, 개정란 별도 값 미표시 | 출력 모듈 및 전원 연결 설계 |
| 동일 PDF FG254/PDF257 | DATA 27.05.2024, MATERIAL LIST | 65QM1 설명11–16A와 FG65 상충; 현재 부품 확정 불가 |
| PID_1684n002I.pdf PDF1 | 도면번호1684n002, 원도06/04/2011, Rev I 15/01/2013, M41 6.3 kW/440V | FG65의5.5kW와 상충; 최종 정격 아님 |
| Electrical_Can_Decoating_20241118.pdf PDF36/51 | `24.11.11 first draft design`; 승인칸 공란 | 경로·케이블 참고 설계. 승인 시공/현장 길이로 확정하지 않음 |

### 1.3 비해당·미확보를 구별

- FG65의 직접기동 회로에는 인버터/소프트스타터/속도 지령 블록이 없다. **이 도면 경로에 인버터 파라미터·속도 환산을 적용하는 것은 비해당**이다.
- FN05 전용 전류/속도/PID·진동센서의 추가 설비 존재 여부, 실제 모터 제조사/명판/토크·정비주기는 **근거 미확보**다. 자료 부재를 현장 부재로 단정하지 않는다.
- ER01의 온도 설정, VR06/LD01 제어·고장, FN04 자체 보호회로는 그 설비의 소유이며 FN05 항목 수를 늘리는 데 복제하지 않는다.

## 2. I/O·HMI

### 2.1 선언·주소·역할

주소의 byte.bit는 원문 SSD.AO bit offset과 SAD 영역, 또는 DepDBBlock.TOD의 DB 번호를 함께 대조했다. 백업 주소만 확인했으며 현재 온라인 매핑은 미확인이다.

| 구분/이름 | 백업 주소·형식 | 직접 원본 근거 | 역할/주의 |
|---|---|---|---|
| `Start FN05` | %Q4.7, Bool | D/0602 RID190, SAD Output/AO39; NID40 UID1113 AK=Write. D/0658 RID146, NID36 UID1238. live_index doc1299 | PLC 출력. doc1299 주석 `a 60.0 fn-05 motorcommand`를 실제 주소로 쓰지 않음; FG65/140은 A4.7 |
| `FN05_Fbk` | %I6.0, Bool | D/0613 RID278, SAD Input/AO48, NID46 UID2530; live_index doc518 | 원시 물리 피드백. 접촉기 보조접점이며 독립 축속도/풍량센서 아님 |
| `Inputs.FN-05 RUN` | DB13.DBX6.0, Bool | D/0604 RID225 / D/0657 RID304 AO48; D/0603 RID218 / D/0655 RID247 TOD N13 | 처리 응답. 원시 I6.0과 구분, 호출 조건이 있음 |
| `Flag.M_FN_05` | DB2.DBX3.1, Bool | D/0604 RID189 AO25, BAD BIRID2; D/0603 RID2 TOD N2 | 운전 요청 메모리. LAD1970 RCoil과 Contact, Q4.7 자체가 아님 |
| `Allarm.FN_05_FAULT` | DB3.DBX3.1, Bool | D/0604 RID188 / D/0657 RID149 AO25; D/0603 RID5 / D/0655 RID10 TOD N3 | 고유 래치 고장. HMI의 DB11.DBX66.1과 분리 |
| `Tag_79` | %T96, Timer | D/0658 RID147 SAD Timer/AO96; live_index doc1298 | PLC SD 타이머. HMI 태그 아님 |
| `Inputs.FN04 Run` | DB13.DBX22.2, Bool | D/0604 RID270 AO178, NID40 UID23 | FN05 정지 조건에서 읽는 다른 팬 처리 응답. FN05 피드백으로 바꾸지 않음 |
| `ON` | %M0.0, Bool | D/0602 RID1 SAD Memory/AO0, live_index doc1556 | 네트워크/호출 허가 접점. 이름만으로 항시1 가정 금지 |
| `UNDER TESTING` | %M5.5, Bool | D/0602 RID4 SAD Memory/AO45, live_index doc1906 | FN04 미응답 Reset 분기에만 반전 접점. 현장에서 켜라는 지침 아님 |
| `Flag.RESET_ALLARM` | DB2.DBX6.0, Bool | D/0657 RID13 AO48; D/0655 RID12 TOD N2 | 고장 해제 요청, 기동 요청 아님 |
| `hours motors.FN_05_MIN/HOUR` | DB9.DBW180/182, Int | D/0615 RID280 AO1440 / RID282 AO1456; D/0614 RID5 TOD N9 | MIN은 Add1, HOUR는 Move1. 누적 가동시간으로 단정 금지 |

### 2.2 원시 입력 → 처리 응답

LAD1070 `D/0397-FlgNet.xml`의 Part42 Move는 Wire21 Powerrail→42.en, Wire52 ORef45→42.in, Wire54 42.out1→ORef46이다.

- ORef45/RID13 = D/0627 `Tag_171`, Word, SAD Input/AO48 = %IW6.
- ORef46/RID14 = D/0629 GlobalAccess, Word, AO48/BAD BIRID4. D/0628 RID4 DepDBBlock Inputs/TOD N13 = DB13.DBW6.
- 따라서 백업의 해당 Word 복사 구조는 `%IW6 → DB13.DBW6`. FN05의 I6.0과 DB13.DBX6.0은 같은 위치의 bit0 연결 근거를 가진다. 원시 물리입력이 처리 응답에 반영되는 **구조**를 확인한 것이지, 현재 호출/값/갱신 시각을 확인한 것은 아니다.
- Part42 `DisableENO=true`도 원문에 있다. 후행 Wire53의 42.eno→43.en을 일반적인 실행 순서로 확대 해석하지 않는다. FN05의 직접 out1 연결과 별개로 보존한다.
- LAD1613 `D/0030-FlgNet.xml`: Recipes Handler CRef21 → ENO로 HMI CRef23 → ENO로 HMI Output CRef25 → Wire42→Part37(반전 Simulation(1)) → Wire43→HMI Inputs CRef28.en. 함수 이름은 D/0688의 UID22/24/26/29, CRef는 D/0694, 반전접점 ORef45는 D/0692 RID140로 대조했다. 입력 복사를 무조건 매 스캔 실행된다고 쓰지 않는다.
- 참고 의존성: 같은 LAD1070의 FN04_Fbk ORef38/D0627 RID139는 %I28.2이며, Part33 Contact→Wire116→Part118 Coil, ORef119/D0629 RID146로 FN04 Run DB13.DBX22.2에 쓴다. FN05의 정지 조건에서 읽는 것은 이 처리 비트다.
- 중지 simulation 원본에 처리 Run 쓰기 참조가 남아 있다는 사실은 선언 검색에 나타난다. 이번 작업은 해당 블록을 작성/변경/생성/실행/행동시험하지 않았고 활성 상태를 추정하지 않았다. 중지 경로를 현재 피드백 설명으로 사용하지 않는다.

### 2.3 HMI 설정 태그와 실제 이벤트의 간격

`sources/hmi_plc_tags.csv`(헤더 포함 행133/421/456)의 추출 원문은 다음과 같다.

| HMI 이름 | 설정 주소 | 내부 ID | 지금 확인 가능한 것 |
|---|---|---|---|
| FN_05\Allarme1 | DB11,X66.1 | 0032C | PLC Access 설정 Bool bit; 실제 쓰기/표시 이벤트 미확인 |
| FN_05\RispostaA | DB11,X66.0 | 001B6 | PLC Access 응답 표시 후보; I6.0 자체 아님 |
| FN_05\Flag | DB2,X3.1 | 0018E | PLC 요청 멤버의 백업 주소와 일치. 버튼의 Set/Reset/Toggle 방식 미확인 |

이 CSV는 dde.cfg 설정 추출본이며 원본 런타임 현재값/스크린샷이 아니다. 실제 dde.cfg/화면 객체 이벤트·권한·동작 시점은 추가 자료가 필요하다. 파생 `hmi-transfer.json`도 세 태그 모두 current_mapping_verified=false, screen_read_write_verified=false를 유지한다.

LAD1210 `D/0386-FlgNet.xml`의 실제 호출 배선:

| Wire | 핀 | ORef / RID | 결속 상태 |
|---|---|---|---|
| 21 | CRef22.en | Powerrail | 연결 확인 |
| 37 | Ingresso_run | 24 / 658 | 해당 선언 UID/RID 결속 미확보 |
| 39 | Allarme1 | 26 / 392 | 해당 선언 UID/RID 결속 미확보 |
| 40/41/42/43 | Allarme2/3/4/5 | 27/28/29/30 / 48 | D/0626 FALSE 후보, 반복 UID/NID 주의 |
| 46 | Risposta 출력 | 33 / 395 | 대상 선언 결속 미확보 |
| 48 | Comulativo_allarmi 출력 | 35 / 397 | 대상 선언 결속 미확보 |

CodeBlock23/RID1은 D/0623 `HMI Standard Motors` 호출군, CRef22/RID638은 D/0624로 이어진다. 같은 UID를 여러 네트워크에서 재사용하고 FN05 호출의 NID 추정도 null이므로, UID/RID만 맞는 다른 설비 선언을 끌어오지 않는다. 검색 doc1210은 `Inputs.FN-05 RUN`, `Allarm.FN_05_FAULT`, `Motors.FN05.Risposta/Allarme_comulativo`라는 후보명을 제공하지만 **미결속 4개를 확정하는 원본 선언 증거로는 부족하다**.

공통 함수 LAD331 `D/0355` 및 D/0621 Local 선언에는 Ingresso_run→Risposta, Allarme1..5→O(5입력)→Comulativo_allarmi 구조가 있다. 공통 함수의 Local 핀 구조를 FN05 실제 대상 주소의 증명으로 바꾸지 않는다. FN05 직접 고유 FAULT와 HMI 종합표시의 완전한 결속은 보류다.

범용 HMI `EB6`와 `AB4`는 각각 I6.0/Q4.7을 포함하는 byte-span 후보다. 독립 FN05 명령/센서가 두 개 더 있다는 뜻이 아니며, 범용 byte의 쓰기 권한도 확인하지 않았다.

## 3. 제어 구조

### 3.1 호출과 순서의 경계

- LAD1619 `D/0031`: Part282 ON → Wire283로 Allarms1 CRef264.en 등 병렬 연결. CodeBlock275/D0688 RID58은 Allarms1이다.
- LAD1620 `D/0549`: Part350 ON → Wire351로 Motors1 CRef319.en, time work motor CRef334.en 등 병렬 연결. CodeBlock337/D0688 RID67=Motors1, CodeBlock347/RID82=time work motor.
- ON이 거짓이거나 호출되지 않을 때의 출력 보존/초기화는 이 구조만으로 판정하지 않는다. 검색 index_order와 내부 NID는 다르며, TIA 프로젝트의 OB 호출·실행순서·온라인 블록 일치 확인을 완료하지 않았다.

### 3.2 FN05 요청 Reset: LAD1970 / 0270 / 내부 NID40

원본 식을 해석 편의로 펼치면 다음과 같다. 이는 정적 접점 경로이며 실행 시험 결과가 아니다.

- Reset `Flag.M_FN_05`: `ON AND (Allarm.FN_05_FAULT OR ((NOT Inputs.FN04 Run) AND (NOT UNDER TESTING)))`
- Coil `Start FN05`: `ON AND Flag.M_FN_05`

| 부분 | Part·Wire·ORef 근거 |
|---|---|
| 공통 ON | Part1126 Contact, Wire1136 전원, ORef1107/RID1→Wire1114. Wire1127에서 고장·FN04응답·출력요청의 세 경로 분기 |
| 고장 Reset 분기 | Part1128 Contact, ORef1108/RID188→Wire1115, Wire1129→O1097.in1 |
| FN04 미응답 분기 | Part22의 operand Negated, ORef23/RID270→Wire21; Wire24→Part1132, operand Negated, ORef1110/RID4→Wire1117; Wire1133→O1097.in2 |
| 요청 Reset 끝점 | O1097 2입력 → Wire1119→Part1102 RCoil; Wire1121→ORef1111/RID189. D/0604 NID40 UID1111 AK=Write |
| 출력 끝점 | Part1134 Contact, Wire1122→ORef1112/RID189; Wire1135→Part1106 Coil; Wire1124→ORef1113/RID190. D/0602 NID40 UID1113 AK=Write |

중요한 읽기 제한:

- UNDER TESTING 반전은 FN04 미응답 분기에만 있으며 고장 분기 전체를 우회하는 조건이 아니다.
- 이 FN05 네트워크에는 OFF 접점이 직접 없다. 그렇다고 설비 전체에 정지 기능이 없다고 결론 내리지 않는다. 요청의 다른 경로·전원/현장 보호·HMI 동작·호출 조건이 별도다.
- 소유 선언을 검색한 범위에서 M_FN_05의 명시적 PLC 쓰기는 이 RCoil이고, 같은 멤버에 대한 Set 코일은 확인하지 못했다. HMI Flag 설정과 일치하나 실제 요청을 1로 쓰는 이벤트/간접·Word 쓰기를 모두 확인한 것은 아니므로 **수동전용·자동요청 없음**으로 확정하지 않는다.
- Reset→출력의 정적 구조는 원문대로 보존한다. 같은 스캔의 실제 최종값·HMI와 PLC 쓰기 경쟁은 온라인 Trace/호출 증거가 필요하다.

### 3.3 후단 ER01에 대한 영향, 소유는 ER01 유지

LAD1971 `D/0271`, NID41에서 ORef27/RID225(Inputs.FN-05 RUN)는 Wire25→Part26 반전 접점, Wire28→Part1155 UNDER TESTING 반전, Wire1156→O1120.in3, Wire1142→Part1125 RCoil(Flag.M_ER01)로 이어진다.

따라서 `ON AND NOT FN05 처리 Run AND NOT UNDER TESTING`은 ER01 요청 Reset의 한 분기다. 나머지 OFF·Allarm.ER01_run 분기도 원문에 있으므로 이 분기만 전체 ER01 식처럼 쓰지 않는다. ER01 출력에는 별도 요청/177T1_OK 조건과 고유 Q주소가 있고 FN05 출력이 아니다. 이 영향은 FN05→ER01 의존관계로만 기록하며 ER01 완료 문서를 대신하지 않는다.

### 3.4 가동시간: 원시 피드백 사용, HOUR에 Move1

LAD1044 `D/0331`, NID46:

1. Part2558 Contact(Tag_47 %T13, ORef2529/RID1) → Wire2559 → Part2560 Contact(FN05_Fbk %I6.0, ORef2530/RID278) → Wire2561에서 Add2512.en과 Ge2519.pre로 분기한다.
2. Add2512: ORef2531/RID280 MIN(in1, Wire2543), ORef2532/RID7 `1`(in2, Wire2544), out Wire2545→ORef2533/RID280 MIN.
3. Ge2519: ORef2534/RID280 MIN(Wire2546)와 ORef2535/RID8 `60`(Wire2547)을 비교하고, out Wire2548→Move2522.en.
4. Move2522.in은 ORef2536/RID7 `1`(Wire2550), out1 Wire2551→ORef2537/RID282 HOUR다. **HOUR+=1이 아니라 HOUR에1을 쓰는 원문**이다.
5. Wire2552는 Move2522.eno→Move2525.en, ORef2538/RID12 `0`(Wire2553)→Move2525.in, out1 Wire2554→ORef2539/RID280 MIN. Wire2555의 ENO가 SCoil2528로 이어지고 Wire2556/ORef2540가 Flag_Aggiorna_DB를 Set한다.
6. D/0616 LiteralConstant의 V=1/60/0와 NID46/UID2532,2535,2536,2538를 대조했다. 함수의 ENO와 비교기 pre 연결을 생략하지 않는다.

LAD1054 `D/0018`, NID56: Part3085 Contact(Tag_48 %T17, ORef3079/RID284) → Wire3086→Move3076.en; Wire3083/ORef3080/RID12 `0` → Move.in, Wire3084→ORef3081/RID282 HOUR. 별도의 HOUR 초기화/해제 쓰기다.

공통 시간 기준:

- LAD1056 `D/0019`: Part3120의 Tag_47 반전접점 → Wire3121→SdCoil3112; S5T#1M은 ORef3114/RID335, Tag_47 operand는 ORef3116/RID1. 선언은 D/0613 T13, D/0616 원문 S5T_x0023_1M.
- LAD1055 `D/0341`: ON/Flag_Aggiorna_DB로 MEM2_0을 Set하고, MEM2_0 AND NOT Flag_Aggiorna_DB에서 Tag_48 SdCoil3118에 S5T#5S를 넣으며, Tag_48 접점으로 MEM2_0을 Reset하는 공통 구조다. D/0613 T17, D/0616 RID334가 시간값이다.
- 제목의 'recording the data in the DB'만으로 실제 외부 기록 저장 성공을 증명하지 않는다. MIN/HOUR의 값은 백업 로직 변수이지 확인된 누적 운전·정비시간이 아니다. FN05 전용 HMI 시간 표시 태그/외부 저장 수신부도 미확보다.

## 4. 전기 전달 경로

### 4.1 실제 렌더 대조와 페이지

다음은 PDF 텍스트 추출뿐 아니라 PNG로 실제 확인했다. PNG는 읽기 전용 원본 렌더이며 회로 변경이 아니다.

| 원본 | 실제 페이지 / 인쇄 번호 | 검토 결과와 추출 이미지 |
|---|---|---|
| Electrical_Rev2.pdf | PDF66 / FG65 | 전력·명령·피드백, M41 정격/날짜. `FG65-PDF66.png` |
| 동일 | PDF123 / FG122 | E6.0 입력단자21, CPU515/MOD9, 개정2. `FG122-PDF123.png` |
| 동일 | PDF141 / FG140 | A4.7 출력단자8, CPU515/MOD15, 출력공통전원. `FG140-PDF141.png` |
| 동일 | PDF257 / **FG254** | 65KM1/65QM1 재료표. `BOM-FG254-PDF257.png` |
| 시공 참조 PDF | PDF36 / D-PAGE19, TOTAL36/64 | DUST ZONE02, M41/ER01 각 경로. `Construction-PDF36.png` |
| 시공 참조 PDF | PDF51 / D-PAGE1, TOTAL51/64 | 케이블1_27/1_28 실제 행. `Construction-PDF51.png` |
| PID_1684n002I.pdf | PDF1 /1684n002 RevI | M41/FN05와 ER01/석회 투입 관계,6.3kW. `PID-PDF1.png`, `PID-FN05-detail.png`, `PID-title-detail.png` |

### 4.2 전력 경로: 전원 → 보호 → 접촉기 → 단자 → 개폐기 → 모터

FG65/PDF66의 3상 440V 60Hz 표시 회로:

`8.3L1/L2/L3 (64/9에서 도착, 66/0으로 연속)` → `65QM1` 주극1/3/5→2/4/6 → `65KM1` 주극1/3/5→2/4/6 → `65U1/65V1/65W1` → `XM65U1/XM65V1/XM65W1` → `65QS1` 주극1/3/5→2/4/6 → `M41/FN-05 U/V/W`, 별도 PE 표시.

- 도면의 BLACK FS17 2.5mm²는 내부 배선 표기다. 시공 PDF의 외부 CV4×2.5 케이블과 같은 항목으로 합치지 않는다.
- M41 아래 도면 정격 표기5.5kW/10.3A와 PID6.3kW가 일치하지 않는다. 여기에 맞춰 보호치를 조정하거나 교체 모터를 선정하는 것은 금지한다.
- 현재 상전압·상순서·접촉기 실제 단자·QS/QM 실물 위치·PE 연속성은 조사하지 않았다.

### 4.3 PLC 출력 → 실제 코일의 양 끝점

`Start FN05 %Q4.7` ↔ 도면 `A4.7` ↔ FG140/PDF141 `CPU515 MOD15 단자8` ↔ 교차참조 `65/4` ↔ FG65/PDF66 `140/1` → `XS67` → `65QS1 보조접점(65/1)` → `XS68` → 도체65.1 → `65QM1 보조접점(65/1)` → `65KM1 A1`, `A2 → -0Vdc10.6`.

- FG65의 제어 코일은 24Vdc 회로이며 M41의 440V 전력회로와 다르다.
- FG140 모듈 공통의 +24Vdc10.9는 X21/3032 5×20 4A F 퓨즈를 지나고 단자9/10 영역에 연결되어 있다. 단자9/10의 정확한 핀 기능을 사진 없이 임의로 확정하지 않는다.
- 65QS1/QM1 보조접점의 해당 제어 경로에는 숫자 단자쌍이 명확히 표기되지 않아 접점번호를 만들지 않는다. 하단 KM 접점표를 QS/QM의 단자로 복사하지 않는다.
- Q4.7이1이어도 이 하드웨어 경로가 이어졌다는 증거는 아니다. 보호·현장 개폐·코일·0V·주접점은 별도 관찰 대상이다.

### 4.4 실제 보조접점 → PLC 입력 → 처리 응답의 양 끝점

FG65/PDF66 `+24Vdc10.7` → `65KM1 보조접점13–14 (65/4)` → `E6.0` 교차참조 `122/2` → FG122/PDF123 `65/6`/`E6.0, CPU515 MOD9 단자21` → 백업 `%I6.0 FN05_Fbk` → LAD1070 `%IW6→DB13.DBW6` → `Inputs.FN-05 RUN`.

도면의 접점은 열린 형태의 보조접점 기호다. 이것을 현장 정상극성·반전 배선 없음·실제 모터 회전/풍량의 보증으로 사용하지 않는다. 모터/팬이 기계적으로 회전하지 않아도 접촉기 보조접점만 동작할 수 있으므로 독립된 현장 운전 증거가 필요하다.

### 4.5 시공 참조와 ER01 분리

PDF51 행1_27:

- 식별자 `=DUS+FN05-M41A`; FROM LOC `CR`(FROM TAG 공란) → TO LOC `FN-05`, TAG `M41`, BLOWER FAN.
- Current Type `GAC`, SPEC `CV`, CORE4, SIZE2.5, SPARE0.
- 경로 `100 → 200 → 210 → 211 → 212 LB → E100`, Adjustment3, LEN115. 표에 나타난 값만 보존하며 길이의 현장 실측/단위 확정은 하지 않는다.
- PDF36에서 M41은 212LB, Pipe28, Pull Box01 FN-05로 표시되고 같은 케이블1_27을 CV/2.5/4로 적는다. 접속 단자 번호·심선별 매핑은 이 표에 없어 FG65 XM단자와 물리 동일성은 추가 시공자료가 필요하다.
- 바로 아래 행1_28 `=DUS+FN05-ER01`, TO ER01/ELECTRICAL RESISTANCE, CV/4/4, LEN115는 다른 케이블이다. 위치가 FN05여도 팬 모터 전력선으로 합치지 않는다.

### 4.6 부품표의 사용 한계

FG254/PDF257의 65KM1 행에는 Siemens 3RT2017-1BB41(5.5KW,1L,DC24V,S00)와 3RT2916-1CB00 RC 소자가 있다. 65QM1 그룹에는 3RV2901-1E, 3RA1921-1DA00, WR32433, 3RV2011-4AA10(11–16A) 등이 적힌다. 이는 자료의 BOM 항목이지 **현행 장착 확인·승인 교체품·조정 설정값**이 아니다. 특히 FG65의10–16A와 차이가 있으므로 명판/승인 개정/검수 기록 전에는 어느 쪽도 수정 기준으로 삼지 않는다.

## 5. 알람·복구

### 5.1 FN05 고유 FAULT와 지연

LAD1814 `D/0448`, NID36. 고유 타이머/알람 관계:

| 동작 | 원문 접점 경로 | 직접 근거 |
|---|---|---|
| Tag_79 SD 기동 | ON AND Start FN05 AND NOT Inputs.FN-05 RUN | Part1261→1263→1274(operand Negated)→SdCoil1225; Wire1264/21; ORef1275 RID304→Wire1277 |
| 시간값 | S5T#2S | ORef1239 RID28→Wire1249→1225.value; D/0656 LiteralConstant NID36 UID1239, T=S5Time, SV=S5T_x0023_2S,V512 |
| 타이머 대상 | Tag_79 %T96 | ORef1240 RID147→Wire1250→1225.operand; D/0658 NID36 UID1240 AK=Write |
| FAULT Set | ON AND Start FN05 AND Tag_79 | Part1265 Contact(ORef1241 RID147, Wire1251)→Wire22→SCoil1231; Wire1254→ORef1243 RID149 |
| FAULT Reset | ON AND Flag.RESET_ALLARM AND FN_05_FAULT | Part1269→1271→RCoil1236; ORef1244/RID13 Wire1256, ORef1245/RID149 Wire1257, Wire1272, 출력ORef1246/RID149 Wire1259 |

D/0657 RID149의 Set UID1243와 Reset UID1246는 둘 다 AK=Write이고, UID1245는 읽기다. 명칭만으로 auto reset으로 바꾸지 않는다. SD의 실제 시간경과/재기동·Set/Reset 동시성/스캔 우선순위는 TIA/CPU 확인 전이다.

### 5.2 영향과 해제 후 재요청

- 고장 비트는 LAD1970의 FN05 요청 Reset에 사용된다. 요청이0이 되면 직접 출력 코일 경로는 거짓이 되는 구조다. 실제 출력 차단 시각·코일 탈락·모터 정지는 미확인이다.
- FN05 처리 Run 저하는 ER01 요청 Reset의 별도 분기에 사용된다. FN05 고장 발생이 항상/즉시 전체 공정정지를 일으킨다는 증거까지 확보한 것은 아니다.
- Reset 요청은 FAULT를 지우는 경로이고 M_FN_05를 Set하는 경로가 아니다. **알람 해제, 새 운전 요청, 출력, 접촉기 피드백, 실제 회전/송풍**을 각각 확인해야 한다.
- FN04 처리 Run이0인 원인이 남으면 일반 운전 조건의 FN05 요청은 다시 Reset될 수 있다. UNDER TESTING을 켜서 우회하는 복구법은 제안하지 않는다.
- HMI 표시/확인음/공통 사이렌의 실제 이벤트와 전달 대상은 미확정이다. FN05 전용 공통정지/사이렌 우선순위·메시지 언어를 추정하지 않는다.

### 5.3 복구 완료에 필요한 별도 증거

권한 있는 현장 담당자가 승인된 안전절차로 수집한 동일 시간대의 요청/출력/I6.0/DB13.DBX6.0/T96/FAULT/Reset/FN04 Run 기록, 접촉기·보호기·QS 상태, 실제 송풍 확인, 원인 조치 내역, 재발 여부가 필요하다. 현재 CPU와 백업의 일치, HMI 경로 일치를 먼저 확인해야 비교가 유효하다. 이번 초안은 실제 복구 또는 수리를 수행했다는 기록이 아니다.

## 6. 증상별 수리·관찰 설계

다음은 점검자가 모을 자료와 비교 순서다. 실제 장비 조작·전압 인가·보호설정 변경·우회·시험 운전을 지시하거나 수행한 것이 아니다. 활선 측정/정비는 자격 있는 담당자가 현장 승인·차단/잠금 절차에 따라 별도로 수행해야 한다.

| 증상 | 같은 시각에 기록할 값/위치 | 원본과 비교·원인 배제 | 다음 자료/복구 판정 |
|---|---|---|---|
| 요청이 바로 풀림 | HMI Flag/DB2.X3.1, ON, DB3.X3.1, FN04 DB13.X22.2, UNDER TESTING | LAD1970의 고장 OR(FN04 미응답 AND 비시험) 분기를 분리. HMI 이벤트가 애초에 요청을 기록했는지 비교 | 원인 분기와 실제 쓰기 주체가 확인되고, 승인된 재요청 후 요청·출력이 유지되는 별도 기록 |
| 요청은 있으나 Q4.7이 없음 | DB2.X3.1/Q4.7/ON, Motors1 호출, scan/다른 쓰기 | 코일의 ON AND 요청, 같은 네트워크 Reset, 호출 조건을 구별 | 백업/현재CPU 일치 및 Trace. 'HMI가 켜짐=출력이 켜짐' 판정 금지 |
| Q4.7은 있으나 접촉기/모터 미동작 | FG140 단자8, XS67/68, QS/QM 상태, KM A1/A2, 전력경로 관찰 기록 | 출력 bit→모듈→QS/QM→코일→주접점/모터를 나눠 비교. 보호기 트립과 PLC 미출력을 혼동하지 않음 | 승인 절차의 전기/기계 점검 보고. 현행명판·보호값 상충 해소 전 임의 설정 금지 |
| 기동 후 FAULT 발생 | Q4.7, I6.0, DB13.X6.0, T96, DB3.X3.1 시각 | LAD1814의2초와 맞는 미응답인지. 접촉기13–14/모듈21/원시입력/Word복사 호출을 순서대로 비교 | 물리 피드백과 처리 응답 차이를 먼저 확인. 타이머 증가로 증상 숨김 금지 |
| I6.0은 변하나 화면/처리응답이 다름 | I6.0/IW6/DB13.W6, HMI 호출·DB11.X66.0/66.1 | LAD1070 복사와 LAD1613 호출 조건, HMI 미결속4개를 구분. 표시를 원시값으로 취급하지 않음 | 원본 HMI 프로젝트·스크립트·태그 연결·현재 런타임 통신 증거 |
| 팬은 도는 듯한데 ER01이 정지 | FN05 처리 Run, ER01 요청/알람/기타 허가 별도 | LAD1971의 FN05 반전 분기는 한 조건일 뿐. 팬 보조접점과 실제 송풍이 같다고 가정하지 않음 | ER01 전용 문서/고유 회로 검토로 인계; FN05 표준 완료로 ER01까지 완료 처리 금지 |
| 가동시간이1/0으로 바뀌거나 누계가 맞지 않음 | DB9.W180/182, T13/T17, Flag_Aggiorna_DB와 외부 저장 수신 기록 | LAD1044의 HOUR Move1 및 LAD1054의 Move0, 공통 시간처리 확인 | 외부 누계/저장 수신부와 실제 기록을 확보. PLC HOUR를 누적시간으로 임의 해석 금지 |

관찰 기록 필수 필드: 관찰자, UTC/현지 시간대 포함 시각, 위치/주소, 값/단위, 수집 장치, 현재 프로젝트 식별자, 비교할 원본 해시, 원인 배제 결과, 실제 조치, 복구 증거. 입력값0과 미수집 빈칸, 원시/처리/HMI 값을 분리한다. 실제 운영 기록이나 사진은 이 조사 파일에 복사하지 않았다.

## 7. 완료 기준·인계

### 7.1 남은 자료와 판정 기준

| 부족 자료 | 수집 위치/제공 주체 | 통과 기준 |
|---|---|---|
| 현재 CPU/프로젝트 일치 | 승인된 TIA 백업·온라인 비교 보고 | 블록/심볼/호출/주소/시간값이 조사 기준과 같은지 차이 문서화. 컴파일과 현장 운전은 각각 별도 |
| HMI 4개 미결속·실제 버튼 이벤트 | HMI 원본 프로젝트, dde.cfg, 객체 스크립트, 런타임 화면 | UID/RID 또는 현재 프로젝트 선언으로 호출 대상·DB11 멤버·요청 이벤트와 쓰기권한 확인 |
| FN05 요청 쓰기 전체 경로 | PLC cross-reference 및 HMI/간접·Word 쓰기 목록 | Reset뿐 아니라 요청 Set/해제 주체, 동시쓰기와 최종값의 실제 근거 확보 |
| M41 정격 상충 | 실물 명판, 승인 최종 전기도면/PID/교체 기록 | 5.5kW 대6.3kW 중 현행 실물·설계판본 판정; 미확정 자료 보존 |
| 보호기 상충 | 65QM1 명판·설정사진·승인 보호계산/개정 | 10–16 대11–16A 표기 의미와 현행부품/승인값 확인. 자료만으로 설정 변경하지 않음 |
| 케이블/단자 일치 | 승인 as-built·시공 검수·단자대 사진 |1_27/CR→M41과 XM/XS/심선 양끝점 대응, 현장 경로·길이 확인 |
| 실제 정상극성/회전·송풍/복구 | 자격 있는 현장 담당자의 승인 관찰 | 원시·처리·화면·기계상태 일치, 원인 조치·재발 없음. 접촉기 접점만으로 통과 불가 |
| 시간 누계 소유 | DB 기록 수신 프로그램/원본 기록 | HOUR Move1/Move0와 외부 누계 관계, 데이터 유실·저장 성공 여부 설명 |

### 7.2 네 기능 적용과 기록 보존

| 기능 | FN05 적용 판단 | 이번 실제 상태 |
|---|---|---|
| 도면·래더 비교 | 적용 가능: FG65/140↔LAD1970, FG65/122↔LAD1814, 입력전달↔LAD1070, PID/시공↔설비관계 | 원본 비교 자료 준비만. FN05 화면 통합·링크/선택 강조 미검증 |
| 백업 미리보기·선택 복원 | FN05 기록키·다른 설비 분리·미지필드 보존 필요 | 구현 지원 여부 미판정. 실제 저장/복원 미실행 |
| 기록 전후 비교 | 요청/출력/원시/처리/알람/상충 자료시점 분리 필요 | 관찰 설계만, 운영 기록 생성0 |
| 보고서/PDF | 조사근거·상충·사진 출처·현재CPU 미확인 표시 필요 | 이 MD 초안만. 사용자 관찰보고서/PDF 생성·렌더 검증 미실행 |

후속 구현이 승인되어도 note/repair_observation의 기존/미지 행·필드·다른 설비·초안·저장키를 보존해야 한다. 생성/저장 시점의 근거는 현재CPU·관찰 당시 상태의 증명이 아니다. 이번 조사에서 기록 도구의 정상 작동이나 BC01 동등 표준화 완료를 선언하지 않는다.

### 7.3 수행 검사와 미수행 검사

- 사전 `git status --short` 빈 출력, HEAD 확인. 끝 검사에서도 고정 repo clean 유지.
- 스킬 preflight의 소스가 read-only임을 읽고 실행. 종료0, `inventory_matches=true`; 로그 `extracts/FN05/preflight.json`.
- FN05 격리 추출 스크립트는 ElementTree로 선언/연결을 읽고 자체 폴더에만 파생표를 쓴다. 공통 추출 스크립트와 공유 declarations.json은 실행/수정하지 않았다.
- `extracts/FN05/check-static.py` 종료0. **29개 구조/식별/해시 검사 통과**: FN05 독립 root/대장 수, 핵심 반전/코일/OR 구조, 0270/0448/0271/0331/0018 UID-RID-NID 단일후보, HMI 핵심 미결속4개 보존, source-manifest9 파일해시, 중지5 해시만 대조, Git clean/HEAD. 이는 제어 실행시험이 아니다.
- PDF는 pdftotext로 후보 페이지를 찾고 pdftoppm으로 위7페이지 및 PID 상세영역 렌더 후 시각 확인했다. PDF 출력물의 FG254와 파일 이름 추정을 바로잡았다.
- 미실행: 매뉴얼/제어 생성기, npm test/build, verify:manual, BC01/UI/기록/ZIP/배포 회귀, TIA/CPU/현장검사. 이번 범위는 원본조사 MD이며 소스·기능 통합을 하지 않으므로 불필요한 생성/운영시험은 하지 않았다.
- 미해결18/확인대기1060/설계시험577 등 기존 집계는 갱신하지 않았다. 과거 검증을 이번 실행 실적으로 소급하지 않는다.

### 7.4 최종 상태

| 구분 | 상태 | 근거/미확정 |
|---|---|---|
| documentation | draft_complete_with_gaps | FN05 7영역 초안. 핵심 근거 최종 문서 검토 완료; 사용자 독립 검토 대기, 로컬 통합 아님 |
| static_review | self_checked; independent_review_pending | 원본 XML/선언/PDF와29개 정적 구조·해시 검사 |
| ui_records | not_run | 화면·저장·재읽기·재열기·동시성·PDF 보고서 미검증 |
| publication | not_published | 조사 초안만, Git/버전/대장/배포 수정0 |
| tia_compile | not_performed | 승인된 TIA 환경 검사 없음 |
| live_cpu | not_performed | 현재 프로젝트·CPU/실제값 미확인 |
| field_recovery | not_performed | 실물 정격·보호값·극성·케이블·정비/복구 미확인 |

### 7.5 다음 한 작업

부모가 고정 원본에서 FN05의 ①FN04 미응답 Reset 분기, ②Tag79/T96/2초 및 Reset, ③I6.0→DB13X6.0 전달, ④FG65/122/140 끝점, ⑤PID6.3/전기도5.5kW와 보호범위 상충, ⑥HMI4개 미결속을 독립 대조한다. 그 결과만 초안 검토에 반영하며, 로컬2차133 통합/게시로 자동 전환하지 않는다. 완료 커밋은 없음.

## 부록 A. 직접 근거 위치 색인

| 근거 | 파일/원본 위치 | 재현 정보 |
|---|---|---|
| FN05 직접 제어 | D/0270-FlgNet.xml | LAD1970, NID40, PLF복원 offset2817203, object key16102200ca11000000000000 |
| FN05 고유 알람 | D/0448-FlgNet.xml | LAD1814, NID36, offset3064790, key161022007462000000000000 |
| HMI FN05 호출 | D/0386-FlgNet.xml | LAD1210, NID미확정, offset2970744, key16102200b716000000000000 |
| 입력Word 전달 | D/0397-FlgNet.xml | LAD1070, NID1, offset2982554, key16102200e916000000000000 |
| 시간처리 | D/0331-FlgNet.xml | LAD1044,NID46,offset2896906,key161022005012000000000000 |
| 시간변수 초기화 | D/0018-FlgNet.xml | LAD1054,NID56,offset2907633,key161022006412000000000000 |
| FN05→ER01 영향 | D/0271-FlgNet.xml | LAD1971,NID41, Part26/1155/1125 |
| 호출 조건 | D/0030,0031,0549-FlgNet.xml | LAD1613/1619/1620, CRef/CodeBlock 선언과 Wire 연계 |
| 공통시간 | D/0019,0341-FlgNet.xml | LAD1056/1055, Tag47/T13 1M·Tag48/T17 5S |
| 공통HMI 배선 | D/0355-FlgNet.xml + D/0621-IdentXmlPart.xml | LAD331 Local 핀, FN05 실제 대상 미결속과 분리 |
| 태그/주소 보조 | sources/live_index.json | docs518/956/1298/1299/1556/1906; 주소는 XML SAD/SSD와 재대조 |
| HMI 설정 | sources/hmi_plc_tags.csv | 행133/421/456(헤더 포함), 내부ID0032C/001B6/0018E |

`extracts/FN05/*-refs.json`은 UID/RID/NID 후보와 원문 XML 조각을 보관한다. 이름 후보가 중복되거나 미결속이면 JSON 그대로 남겼고, 후보 수가1이라는 사실만으로 실행 의미를 보증하지 않는다. `*-pins.txt`는 Part/Wire 구조의 읽기용 전개다. 원본 XML을 대체하는 새 제어 명세가 아니다.

## 부록 B. SHA-256 근거 목록

아래 해시는 고정 원본 파일 바이트의 SHA-256이다. 자체 추출/렌더는 원본 해시와 구별하여 `extracts/FN05/artifact-hashes.json`에 기록한다.

| 원본 경로 | SHA-256 |
|---|---|
| .agents/skills/gme-equipment-rollout/SKILL.md | `fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b` |
| .agents/skills/gme-equipment-rollout/scripts/preflight.py | `395067d6da20af3e1d82a43b7936907a87a44d8d2e11e4ebc61b1fc441e2adb6` |
| AGENTS.md | `0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2` |
| VERSION.json | `5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7` |
| all-in-one/registers/equipment-networks.csv | `0dcd161bafe7fbc5fd31dd00ed031da3b01e4e46f1154b4c80698bdd766568e0` |
| all-in-one/registers/equipment.json | `7870325dff32bbca90fa34507b301c4aad3347d669fddcd03b910343663996fa` |
| all-in-one/registers/hmi-transfer.json | `235dec78a1a1d87d316df5339a18c19d279f7274d0e08912b5f4b2f0af0e7f9f` |
| all-in-one/registers/priority-equipment.csv | `953c2c4df5b3a6e40d926d1f0f08f91900b7d6565e4dcd64191b548e438edeba` |
| all-in-one/registers/simulator-freeze.json | `bb93c1994effc5609939ba566b7802ce7ed55154a7310f02379b308ac2c8c835` |
| all-in-one/sources/Electrical_Can_Decoating_20241118.pdf | `3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd` |
| all-in-one/sources/Electrical_Rev2.pdf | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` |
| all-in-one/sources/GME_20250506.zap18 | `00c79b6d986e68298f65b172c1807115bc5d9e450a74fcc989d0796d8d8a4ea8` |
| all-in-one/sources/PEData.plf | `647de7ea123daced41c27bec8f81aeb93c712cac714d4754d7da5c528abb016a` |
| all-in-one/sources/PID_1684n002I.pdf | `2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b` |
| all-in-one/sources/decoded-original/0018-FlgNet.xml | `7dcd2474e1adda43a4ef2fdd089554ed1506c309c1606772f408bbb69c269344` |
| all-in-one/sources/decoded-original/0019-FlgNet.xml | `a3301f4d07c2d36aefa6faa6c3559a1cff4565fc6de40cd17e54b548b30c0ce5` |
| all-in-one/sources/decoded-original/0030-FlgNet.xml | `9252c9da764993de1edb8b2e44c46d6e9f9d4b6118e751a0dbeaa9ffd8ea721b` |
| all-in-one/sources/decoded-original/0031-FlgNet.xml | `76385eab8f8f72b9faa16f7cf8905f395591b18c0a9ee9e6d7dd085a38c45c65` |
| all-in-one/sources/decoded-original/0270-FlgNet.xml | `0ffebd8949ab7f08f1019abe21a3243f95a05749ccadae353a992053f54f431c` |
| all-in-one/sources/decoded-original/0271-FlgNet.xml | `7f913249a7879930d8443291b542374887e8cbbe89b55993a51233446008521b` |
| all-in-one/sources/decoded-original/0331-FlgNet.xml | `ddd1ed85b11ff4338bdca0eed85766c5cd890bc84d851fae0463a98034ee0f19` |
| all-in-one/sources/decoded-original/0341-FlgNet.xml | `e9921cb52ecba4ef1df14758d29e4091fc510a8e792130e855b869dbab4a1c96` |
| all-in-one/sources/decoded-original/0355-FlgNet.xml | `73592d33f8b3a71effeb36f25427c76e931485e7ce31f5c81f144ddae83c4247` |
| all-in-one/sources/decoded-original/0386-FlgNet.xml | `27415801483242234b51071071ca826cef27cedc34944408687d522084e8d43f` |
| all-in-one/sources/decoded-original/0397-FlgNet.xml | `bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834` |
| all-in-one/sources/decoded-original/0448-FlgNet.xml | `0f355bc4479e17db55a5f09b34ef4f959a60f129a38024556705978020f408b7` |
| all-in-one/sources/decoded-original/0549-FlgNet.xml | `49f7169c33ed7f54559b0801e21a7d618584900972840e91cf51ad032e8febb1` |
| all-in-one/sources/decoded-original/0602-IdentXmlPart.xml | `46ab21151eddaaf616469db520730c60423eb742aa491af194e6710c751b4caf` |
| all-in-one/sources/decoded-original/0603-IdentXmlPart.xml | `e93969dfa281d75b49b24127793068e33472dadb19729c1c48fc4a8dad075ef8` |
| all-in-one/sources/decoded-original/0604-IdentXmlPart.xml | `b798d29c5499b5314a1ee3cff9139dae64c887533b86baa43b6e9a052373a6af` |
| all-in-one/sources/decoded-original/0613-IdentXmlPart.xml | `09d3b1397a987898334218f37e025661af162438582e649f671e7abec443d3cb` |
| all-in-one/sources/decoded-original/0614-IdentXmlPart.xml | `c6de26f74d75f5be858a406de75eaf6faf62ba9b89c8f9a085b5dd206e93d294` |
| all-in-one/sources/decoded-original/0615-IdentXmlPart.xml | `80f4544edca56c6e6bb2713c758c92ade9202255110074931e03fe34d0d0801a` |
| all-in-one/sources/decoded-original/0616-IdentXmlPart.xml | `650b53354a0c8443d94adc5bd6a860d3c5313014a52e0fb98a5656a65b58cc0d` |
| all-in-one/sources/decoded-original/0621-IdentXmlPart.xml | `a63e2b97ea9eb2691cb478666afed77fc58a2da2f8170422dc09e24b102c88ee` |
| all-in-one/sources/decoded-original/0623-IdentXmlPart.xml | `4acd00406ea92466169e57e59fc90b0da4d9ec55fd19e2e96c9556e939cb83a6` |
| all-in-one/sources/decoded-original/0624-IdentXmlPart.xml | `24607c0827fbde428bccf8637ef4ae490798a69a7c2f3b87861d0749082d367a` |
| all-in-one/sources/decoded-original/0626-IdentXmlPart.xml | `a9d7fbea345eca70325a8c2e44058c23e96add1b7207eabbb09445118b18188b` |
| all-in-one/sources/decoded-original/0627-IdentXmlPart.xml | `08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb` |
| all-in-one/sources/decoded-original/0628-IdentXmlPart.xml | `9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd` |
| all-in-one/sources/decoded-original/0629-IdentXmlPart.xml | `67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972` |
| all-in-one/sources/decoded-original/0655-IdentXmlPart.xml | `38e9f323024fba19582b473f39b1ed03ffe6a0b390218894029a6edb0b1ff9fb` |
| all-in-one/sources/decoded-original/0656-IdentXmlPart.xml | `0dbc45e84732a8848f17b094ea08ab8578dbf240bfe15cd7086859395c27c592` |
| all-in-one/sources/decoded-original/0657-IdentXmlPart.xml | `0f70cda60a6b1a17175876d58e25b2686952642de6cffb21213aeef8b347a22b` |
| all-in-one/sources/decoded-original/0658-IdentXmlPart.xml | `998294c0c8a99e00ceb33c2c60def2cd4850e34328917ae506244c2be2df3831` |
| all-in-one/sources/decoded-original/0688-IdentXmlPart.xml | `ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda` |
| all-in-one/sources/decoded-original/0692-IdentXmlPart.xml | `bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037` |
| all-in-one/sources/decoded-original/0694-IdentXmlPart.xml | `757ccebdf32d0a168dd787bfa735fe6494eac4c4a9f7a5adc63898a88e8b152d` |
| all-in-one/sources/decoded-original/network-map.json | `c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60` |
| all-in-one/sources/hmi_plc_tags.csv | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` |
| all-in-one/sources/live_index.json | `14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1` |
| all-in-one/sources/source-manifest.json | `5af6e85994536897fd92f75972534a691e6eb0f067aafe07679c0788fd84e5bf` |
| docs/equipment-standard/INVENTORY.json | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` |
| docs/equipment-standard/WORK-ITEM-TEMPLATE.md | `4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586` |
| docs/equipment-standard/WORK-STANDARD.md | `05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99` |

원본 해시 55개. 원본 source-manifest9와 중지5는 별도의 정적 검사 결과에서 대조했으며, 이 표의 수를 설비 항목 수·완료 실적으로 세지 않는다.
