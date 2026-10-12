# PV05 질소 주입 밸브 — 고정 원본 자체 조사 초안

## 먼저 보는 확인·상충·누락

- 대상은 catalog PV05 한 개다. PV06와 공통 별칭 `nitrogen`, PLC Q6.4 요청을 공유해도 동일 실물 또는 동일 완료 항목으로 합치지 않는다.
- **PV05 고유 경로:** FG96 실제 PDF97에서 96.12 → X2:13의 5×20 2A F 퓨즈 → 96.14 → PV-05 A1; A2 → X2:14 → 96.8. PV05 가지에는 96KT1 접점이 없다. 타이머 접점 15/18을 거치는 PV06의 X2:15/16 가지와 구별한다.
- **공통 요청과 준비는 별개:** A6.4/Q6.4는 96KA3 코일을 구동하는 공통 요청이다. E16.7/I16.7은 96KA2를 통한 탱크 준비 입력이다. 둘 모두 개별 밸브의 실제 열린 위치 피드백이 아니다.
- **이름 상충:** `Inputs.NITROGEN TANK READY`로 `Allarm.HYDROGEN_BOX_FAULT`를 만든다. 원문 HYDROGEN을 보존하며 수소 설비가 별도로 있다고 추정하지 않는다. 과거 색인 설명 E45.7/A60.5와 현재 고정 도면 E16.7/A6.4도 구별한다.
- **0538 알람은 무타이머 S/R:** ON AND NOT Ready AND ServiceBit로 Set, ON AND RESET_ALLARM AND Fault AND (Ready OR NOT ServiceBit)로 Reset. ServiceBit 우회 가지가 있으므로 알람 소거만으로 탱크 준비·안전 복구를 인정하지 않는다.
- **미확정:** Start Nitrogen 선언 세 곳은 모두 Monitor이고 직접 PLC Writer를 찾지 못했다. 자동 산소조건 → Q6.4의 완전한 실행 경로, HMI 클릭 이벤트, 현재 CPU·실물·정상 극성·실제 주입은 확정하지 않는다.
- **공유 근거:** 같은 abcf31c의 [RO01](RO01-DOTS-DRAFT.md), [RO02](RO02-DOTS-DRAFT.md), [BR01](BR01-DOTS-DRAFT.md)을 산소·버너 공통 영향과 입력 Word 전달의 색인으로 재사용했다. PV05 고유 전기 가지, 준비 선언·Word 전달, 0538 핀과 HMI 주소는 이번에 원본 독립 대조했다. 다른 설비의 전체 정적검토·완료를 상속하지 않는다.

## 1. 설비·자료 기준 — 적용

- 기준 저장소: `gme-research/source-mv06`, Git `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, VERSION 1.12.0. 현재 사용자 환경의 최신 기능이나 게시 상태를 이 자료로 검증했다고 주장하지 않는다.
- INVENTORY catalog[27]: PV05, nitrogen, 공압 밸브, phase2, parent 없음. 별도 BATCH09-SCOPE의 `physical_identity_verified=false` 유지. PV06는 별도 catalog[28]. 하위 부품·탱크·외부 박스를 함께 완료로 세지 않는다.
- P&ID `all-in-one/sources/PID_1684n002I.pdf` 실제 1쪽: N₂ FOR EMERGENCY의 PV-05와 PV-06 두 기호·110 Volt가 각각 있다. 도면 번호1684n002, Apex I, 최초06/04/2011; 개정 I 15/01/2013 `REMOVED MC-05, CHANGED POWER OF FN-02`를 제목란 렌더로 확인했다. 전기 도면과 작성 연대가 다르므로 현행 설치 동일성 증명이 아니다.
- 전기 `all-in-one/sources/Electrical_Rev2.pdf`: FG96/PDF97 제목 NITROGEN VALVES BOX PV-05/PV-06, 날짜27.05.2024, 별도 개정표 표기 없음. FG132/PDF133 DIGITAL INPUT MODULE에는 Rev2 17.03.2025. FG142/PDF143 DIGITAL OUTPUT MODULE에는 별도 개정표 표기 없음. 각 실제 footer를 확인했고 파일 이름 Rev2를 모든 쪽의 개정2로 대입하지 않았다.
- 실행 모델/추론 설정의 런타임 증명은 미확인. TIA 추가 접근·현장 자료 없음. 읽기 전용 원본 조사, 자체 XML 파싱·해시·PDF 렌더만 수행했다.

## 2. I/O·HMI — 적용, 현재값/이벤트 미확보

이하 XML 경로의 접두어는 `all-in-one/sources/decoded-original/`이다. 주소 AO와 BO는 비트 offset이며 Word/Bool을 구별한다.

| 신호 | 원본 결속 | 해석·경계 |
|---|---|---|
| Start Nitrogen | 0555-IdentXmlPart RID53, NID -2147483648 UID126; 0557 RID28 UID146; 0558 RID36 UID53; 모두 Global SimpleAccess Bool, Output AO52 | Q6.4. 세 개 출력이 아니라 동일 주소의 선언. C AK=Monitor로 직접 Write 증거 아님. 0557 SAM=Peripherie, 나머지 SAM=None 차이 유지 |
| 탱크 준비 raw | FG96 E16.7 ↔ FG132 단자8 E16.7, CPU515 MOD12 도면 표기 | I16.7 도면 신호. 도면의 CPU 번호로 현장 CPU를 특정하지 않음 |
| 준비 처리 bit | 0684 RID138 NID12 UID937/941, GlobalAccess Bool AO135, BAD135; 0682 DepDB RID135 TOD13 | Inputs.NITROGEN TANK READY = DB13.DBX16.7. 센서 raw와 처리값 분리 |
| 경보 bit | 0684 RID102 NID12 UID938 Write/OID7, UID940 read/OID1, UID942 Write/OID8; AO57 BAD10; 0682 RID10 TOD3 | Allarm.HYDROGEN_BOX_FAULT = DB3.DBX7.1. PV05 단독 열림실패 알람이 아님 |
| Reset | 0684 RID24 NID12 UID939, AO48 BAD15; 0682 RID15 TOD2 | Flag.RESET_ALLARM = DB2.DBX6.0. 물리 복구 명령이나 자동 재주입을 의미하지 않음 |
| ON / ServiceBit | 0686 RID1 / RID161, Memory Bool AO0 / AO8000 | M0.0 / M1000.0. ServiceBit의 운전정책·현재 상태·현장 사용 허가를 추정하지 않음 |

### Word 전달과 호출 경계

- 0397-FlgNet NID1 (색인 문서1070, hmi inputs): Move62.in ← Wire76/ORef67. 0627 RID23 Global Tag_275 Input Word AO128, SAM=None → IW16이다. `PIW16`으로 바꾸어 쓰지 않는다.
- Move62.out1 → Wire77/ORef68. 0629 RID24 Global Word AO128 BAD4; 0628 DepDB RID4 Inputs TOD13 → DB13.DBW16. 따라서 I16.7은 이 Word의 일부로 DB13.X16.7에 전달되는 경로가 있다.
- Move62.en은 Wire74의 Move61.eno에서 온다. Move60.en Powerrail Wire21 → Wire71 Move60.eno/Move61.en → Wire74 Move61.eno/Move62.en 순서이며 `DisableENO=true` 표기와 실제 eno 연결을 함께 보존한다. 전체 실행을 무조건 항상이라고 축약하지 않는다.
- 0030-FlgNet main: CRef21.en Wire31, CRef21.eno→CRef23.en Wire32, CRef23.eno→CRef25.en Wire33, CRef25.eno→Contact37.in Wire42; Contact37은 Negated operand, Wire44 ORef45/RID140 `Simulation(1)`. Wire43 Contact37.out→CRef28.en의 hmi inputs 호출 경계. 공통 BR01 조사와 연결 재사용하고 이번에도 핀 구조를 확인했다. 백업의 현재 활성 상태를 판단하지 않는다.
- 별도 쓰기 존재: 0415-FlgNet NID18의 Coil39.operand는 Wire38/ORef40→0635 RID352, UID40 Write/OID9, Inputs AO135. Contact23/ON→Wire29→Coil39.in이다. 이는 원본 simulation 블록에 남은 **정적 쓰기 흔적**으로만 기록한다. 만들거나 실행하거나 활성화하지 않았다. 현행 CPU에서 raw와 처리bit가 항상 같은지 확정할 수 없다.

### HMI 원본과 한계

`all-in-one/sources/hmi_plc_tags.csv`에서 다음을 직접 대조했다.

- 행515 `Allarmi_58`, 설정 `DB3,X7.1`, Access PLC, 내부ID00153: 경보 bit 주소와 일치한다. 실제 표시 문구·색상·ACK 이벤트·메시지 이력은 이 CSV만으로 미확정.
- 행647 `EB16`, 설정 EB16, ID000BE: raw 입력 byte 범위를 포함하는 설정. DB13 처리bit와 같은 태그로 합치지 않는다.
- 행746 `AB6`, 설정 AB6, ID00051: Q6.4를 포함하는 출력 byte 설정. 쓰기 클릭·수동 개방 버튼·설비별 HMI 명령이라는 증거가 아니다.
- `registers/hmi-transfer.json` 색인의 raw 심볼 I16.7 설명은 `e 45.7 nitrogen tankready`, Q6.4 설명은 `a 60.5 automatic immissionmotor command`로 남아 있다. 현재 고정 주소/FG와 과거 설명 번호가 상충한다. 파생 색인에서 직접 Writer가 빈 것만으로 PLC에 Writer가 영구 부재한다고 결론내리지 않는다.

## 3. 제어 구조·소유 — 적용, 자동 요청 Writer 미확정

1. 자동 측 공통 요청: Q6.4/A6.4 → 96KA3(A1/A2) → FG96에 그려진 부하 접점5–9 → 공통 96.12 공급. 소유는 질소 박스 요청이며 PV05 전용 PLC 출력이 아니다.
2. 비상 누름버튼 측: 도면 6SB1/2/3 접점21–22가 공통 96.10/96KA1 코일 쪽에 결속된다. 96KA1과 96KA3 모두 외부 공급선은 상단 **5**, 부하선은 하단 **9**에 연결된다. 심벌의 전환 가동편이 닿아 그려진 왼쪽1은 외부 공급선이 없는 가지다. 두 릴레이 하단 접점표1/5/9를 실제 부하 연결로 혼동하지 않는다. 버튼 정상 극성, 전원 상실 시 실제 안전 동작, 실제 절차를 이 회로만으로 확정하지 않는다.
3. PV05는 96.12에서 개별 퓨즈를 거쳐 직접 코일에 공급되는 가지다. 96KT1 코일도 96.12에 병렬로 그려져 있으나 **그 접점은 PV06 가지**에 위치한다. 따라서 96KT1의 지연을 PV05 PLC 타이머 또는 PV05 개방지연 값으로 가져오지 않는다.
4. Ready 경로는 X2:9/10 사이 외부 탱크 준비 회로 → 96KA2 코일 → 별도 24Vdc 접점 경로 → E16.7이다. 도면은 외부 탱크 내부 센서/임계·가스 압력·용량 판정 로직을 제공하지 않는다.
5. 전기 회로에 Ready 접점이 PV05 코일 전원과 직렬이라는 증거는 없다. PLC 알람 입력과 코일 전원을 연결해 가상의 인터록을 만들지 않는다.
6. RO01/RO02의 산소 고장·농도 및 BR01 버너 정지 영향은 이전 고정 원본 조사 참조. 질소 준비 알람은 BR01/부하/FN01 사용처를 갖지만 그 사용처는 각각 관련 설비 소유다. RO01 산소 경보가 곧 PV05 개방 요청이라는 명제는 직접 Writer 미확보로 보류한다.

## 4. 전기 전달 경로 — 적용, 실물/시공 최신본 미확보

| 구간 | 양 끝점·기기·원문 | 확인 한계 |
|---|---|---|
| 박스 전원 | FG96/PDF97 CLIENT SUPPLY 220V60Hz → X2:1/2, 96.1/96.2 → 96QF1 원문0.22–0.32A →96.4/96.5→96T1 220/110V 63VA→96.6/96.7→96QF2 1A→96.8/96.9 | 도면 기재값; 현행 보호설정·교체 선정·조정값 아님 |
| 비상 버튼 배선 | X2:3/4/5 → X1:358/362/366 → 6SB1/2/3(21–22) → X1:359/363/367 → X2:6/7/8 →96.10→96KA1 A1; A2→96.8 | 버튼 FG6 교차참조6/2,6/3,6/4. 실제 접점 상태·케이블 번호 미확보 |
| 자동 전달 | FG142/PDF143 A6.4, CPU515 MOD15, 단자25 → FG96/9 A6.4 →96KA3 A1; A2→−0Vdc10.6 | FG142 공급 +24Vdc10.9, X21:3034 4A F, 단자29/30. FG96의 +24Vdc10.7 준비회로와 다른 표기 보존 |
| 자동 부하 접점 | 공통110V 측 →X2:11→X1:368→96KA3 **5–9**→X1:369→X2:12→96.12 | 접점표1/5/9와 실제5–9 부하를 구별 |
| PV05 고유 가지 | 96.12 →5×20 2A F/X2:13→96.14→PV-05 A1; PV-05 A2→X2:14→96.8 | 독립 퓨즈·단자·코일. 실물 모델·정격·개방상태 미확보 |
| 탱크 준비 코일 | 공통공급→X2:9→외부 준비회로→X2:10→96.11→96KA2 A1; A2→96.8 | 외부 준비회로 내부 미제공 |
| 준비 접점/PLC | +24Vdc10.7→X1:370→X2:17→96KA2 **5–9**→X2:18→X1:371→E16.7↔FG132/PDF133 단자8 | 탱크 준비를 개별 밸브 열림 피드백으로 쓰지 않음 |

FG96 접점 확대 렌더 `../extracts/PV05/FG96-KA1-contact.png`, `FG96-KA2-contact.png`, `FG96-KA3-contact.png`에서 KA1/KA2/KA3 모두 상단 외부 공급선5–하단9를 재확인했다. 전환 심벌이1쪽에 닿아 그려진 것과 실제 외부 배선 끝점5–9를 구별한다. 최초 전체화면 판독의 KA1/KA2 1–9 해석은 확대 검토에서 오류로 확인하여 전달 전에 정정했다.

FG96 배선 문구 BLACK FS17 1.5mmq, RED FS17 1.5mmq는 도면 배선 사양이다. 실제 케이블 표찰·심선·준공 단자대와 현장 결속은 미확정이다. 가스 배관 주입점·밸브 타입·고장시 위치·압력 안전한계는 P&ID 기호와 원문 전기값만으로 정하지 않는다.

## 5. 알람·복구 — 적용, 현장 복구 미수행

### 0538-FlgNet, allarms3 NID12, 색인 문서1990

원문 제목 `hydrogen box not ready`, Part10/Wire18. 이 네트워크에는 SD/TON/TOF/TP 등 타이머와 시간상수가 없다.

- Set: Wire963 Powerrail→Contact953.in; Wire943 ORef936(ON)→953.operand; Wire954→Contact955.in; Wire944 ORef937(Ready)→955.operand **Negated**; Wire25→Contact27.in; Wire26 ORef28(ServiceBit)→27.operand; Wire29→SCoil929.in; Wire946 ORef938(Fault)→929.operand.
- 식: `ON AND NOT Ready AND ServiceBit → S Fault`.
- Reset: Wire954에서 Contact957(RESET_ALLARM, ORef939/W947) →Wire958→Contact959(Fault, ORef940/W948) →Wire30으로 분기. Contact961(Ready, ORef941/W949)→Wire962→O31.in1; Contact964(ServiceBit **Negated**, ORef36/W35)→Wire34→O31.in2. Wire33 O31.out→RCoil935.in, Wire951 ORef942(Fault)→935.operand.
- 식: `ON AND RESET_ALLARM AND Fault AND (Ready OR NOT ServiceBit) → R Fault`.
- O31은 OR Cardinality2. S/R별 쓰기 OID7/8과 Wire를 확인했다. ON·ServiceBit 상태가 미확인이라 현재 경보 발생/해제 가능성을 단정하지 않는다.
- 96KT1은 외부 전기 타이머이며 시간값이 이 FG96에 명시되지 않았다. PLC0538 무타이머 경보, 외부96KT1, PV05의 직접 공급 가지를 혼동하지 않는다.

### 영향·복구 경계

공통 참조 BR01의 0175/0585 NID5 UID248은 HYDROGEN_BOX_FAULT를 버너 정지 논리에 사용하는 근거다. 원본 색인에는 motors1 0238 NID2/0604 UID74, 0253 NID22/0604 UID695도 사용처로 나타나지만 이 초안에서 해당 설비 전체 로직을 재검증/완료하지 않는다. 실제 운전 영향·지연·재기동은 소유 설비 문서와 최신 프로젝트로 별도 판정해야 한다.

알람 Reset이 되더라도 실제 탱크 준비, 질소 잔량/압력, PV05 코일/밸브, 배관 주입 또는 안전 복구의 증거가 아니다. 본 조사는 버튼 조작, ServiceBit 변경, 출력 강제, 타이머/보호설정 변경 또는 질소 실제 주입을 승인하거나 실행하지 않았다.

## 6. 증상별 관찰·수리 자료 — 적용, 조작 지시 아님

| 증상 | 안전하게 확보할 관찰 기록 | 비교/원인 분리 | 완료로 인정하지 않는 것 |
|---|---|---|---|
| 준비 안 됨 경보 | 시각·프로젝트 ID, I16.7, DB13.X16.7, DB3.X7.1, M1000.0, Reset 요청 이력 | raw/Word 전달/별도 쓰기/ServiceBit 조건과 탱크측 승인 점검 결과를 분리 | 알람 소거만으로 준비 완료 |
| Q6.4 요청인데 PV05 상태 불명 | 승인된 기존 기록의 Q6.4, 96KA3/공통96.12 및 PV05 단자13/14 식별, 실제 밸브 확인 자료 | PLC 요청→외부 릴레이→PV05 독립 퓨즈·코일→실제 유량 각각 분리 | 출력1 또는 릴레이 표시만으로 개방/가스공급 |
| PV06만 지연 또는 PV05/PV06 차이 | 각 태그·단자·시각의 동시 기록 및 96KT1 승인 자료 | PV05 직접 가지와 PV06 타이머 가지의 구조 차이 우선 | 같은 Q6.4라고 두실물 동일 판정 |
| 경보는 없는데 Ready raw0 | ON·ServiceBit·처리bit·마지막 Reset 및 활성 프로젝트 근거 | S 조건 ServiceBit, 별도 쓰기 경계, HMI 주소 확인 | ServiceBit를 조작해 시험하거나 무경보를 정상 판정 |
| HMI 상태와 현장 불일치 | HMI 태그 ID·주소·화면/시각, raw·DB 처리bit·실물 표찰 | EB16/AB6 byte와 Allarmi_58 bit, 쓰기 이벤트 미확정 구분 | HMI animation을 실제 열림 위치 피드백으로 인정 |

관찰 기록 필드: 관찰자, 날짜/시각/시간대, 승인된 위치, 실제 값/단위, 수집장치·프로젝트/CPU 근거, 비교 원본, 배제 결과, 조치 주체/승인, 복구 증거. 실제 운영·정비·사진/SEJIN 기록을 생성·복제·공개 저장소에 넣지 않았다.

## 7. 완료·누락·검증 상태

| 구분 | 상태 | 이번 결과 |
|---|---|---|
| documentation | complete_with_gaps 초안 | 7영역 및 고유 전기/논리 경계 작성, 부모 독립검토 대상 |
| static_review | scoped_original_review_complete | 33개 선정 파일 SHA256/고정 Git blob 일치; 0538 Part10/Wire18/타이머0; 원본 Git dirty0 |
| ui_records | not_run | 화면/저장/복원/비교/PDF 보고서 미검증 |
| publication | not_published | 코드·버전·공개대장·배포 변경 없음 |
| tia_compile / live_cpu | not_performed | 프로젝트 컴파일/온라인 읽기/현재 CPU 비교 없음 |
| field_recovery | not_performed | 실물·정상극성·주입·복구 미확인 |

도면·래더 비교는 문서 근거를 준비한 상태이며 UI 기능 완료는 아니다. 백업·선택 복원, 기록 전후 비교, 관찰 보고서/PDF의 구현/저장/재읽기/화면 재열기는 이번 범위 밖이다. 기존 note/repair_observation/미지필드/초안/저장 키를 수정하지 않았다.

남은 자료와 판정 기준:
1. 승인된 최신 PLC 프로젝트: Q6.4 직접/Word/간접 Writer와 호출 활성, HMI 실제 쓰기 이벤트, ServiceBit 현재 소유. 확보 전 자동 주입 조건 미확정 유지.
2. 최신 질소 박스 준공도·명판·단자/케이블 표찰: PV05 X2:13/14와 현장 밸브의 동일성, 96KA1/2/3 실제 접점·전압 확인. 공유 Q6.4만으로 동일성 인정 금지.
3. 탱크 공급사 준비조건·96KT1 승인 설정자료·질소 계통 안전 운전/복구 절차. 현재 설정·실물 정상극성·안전한계는 새 자료 없이 채우지 않는다.
4. HMI 화면·알람 메시지/ACK·이벤트 원본. Allarmi_58 주소 일치와 실제 사용자 동작을 구별한다.
5. 현장 담당자의 적법한 관찰/복구 증거가 있을 때만 field_recovery 별도 갱신. 이번 문서로 실제 주입 시험을 요구하거나 권한을 확장하지 않는다.

## 수행 단계 실제 시각 (UTC, 2026-10-11)

- 11:24:39 배정 수신·범위/금지사항 검토 시작.
- 11:24:41~11:24:55 작업표준·시작기록·기존 RO01/BR01 연결 근거 검토, 원본 Git status 확인.
- 11:25:03 FG96/PDF97 렌더 생성; 11:25:10 실제 이미지 검토·선언 조사.
- 11:25:18~11:25:50 0538 선언·핀, 입력 Word 전달, ServiceBit·외부회로 확인.
- 11:26:01 FG132/PDF133·FG142/PDF143 실제 이미지 검토.
- 11:26:19~11:26:45 HMI CSV·DB 선언 대조 및 P&ID 전체 렌더 검토.
- 11:27:11 P&ID 제목/개정란 확대 렌더 검토.
- 11:27:34 자체 정적 검사와 33파일 SHA/Git blob 내용대조 완료. 원본 dirty0.
- 11:30:19 초안 작성 완료; 11:30:39 원본 INVENTORY·Simulation(1) 선언 최종 확인과 33파일 해시 재검사, dirty0 확인.
- 11:30:59 KA1/KA2/KA3 확대 렌더 검토: 모든 외부 배선5–9 확인, 전체화면에서의1측 오독 발견; 11:31:10 부모 독립검토와 일치 확인 후 전달 전 정정.
- 이 목록은 실제 관측 시각이며 순수 작업 소요시간 또는 모델 런타임 증명이 아니다.

## 선정 원본 해시 전체 목록

경로 기준은 고정 `source-mv06` 루트다. 아래 33개가 이번 선정 근거·보존 목록 전부다. 해시 일치는 파일 내용 보존이며 파일 전체/전설비 의미검토 완료를 뜻하지 않는다. 90개 의미검토나 전체 원본을 새로 완전 검토했다고 주장하지 않는다. 마지막 5개 중지 자산은 해시만 확인하고 실행하지 않았다. JSON 상세: `../extracts/PV05/source-hashes.json`, 검사 `../extracts/PV05/checks.json`.

| 원본 상대경로 | SHA256 | 고정 Git blob | 내용 일치 |
|---|---|---|---|
| `AGENTS.md` | `0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2` | `073164bc6efd5791032d62c71b03b4dab48cb6f8` | yes |
| `.agents/skills/gme-equipment-rollout/SKILL.md` | `fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b` | `9aa820ea6ca15b4e136c9772423b78ed4df6a3d4` | yes |
| `docs/equipment-standard/WORK-STANDARD.md` | `05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99` | `f76a570cc73098632e08759b17934000f7e3a253` | yes |
| `docs/equipment-standard/WORK-ITEM-TEMPLATE.md` | `4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586` | `e546f39535d2b589e80f97db869ac37ce4d05cfd` | yes |
| `docs/equipment-standard/INVENTORY.json` | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` | `587c3748ad9224718f95ba06463fee913dae231d` | yes |
| `VERSION.json` | `5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7` | `fffb51663b7705aec91cb119ca80ee943a4ce758` | yes |
| `all-in-one/registers/equipment.json` | `7870325dff32bbca90fa34507b301c4aad3347d669fddcd03b910343663996fa` | `acc42633033398216469064932c4b76987371606` | yes |
| `all-in-one/sources/Electrical_Rev2.pdf` | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` | `f610fd7c7ce14ae951b00cff57b969259bfb389d` | yes |
| `all-in-one/sources/PID_1684n002I.pdf` | `2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b` | `8c83a59fefd5b8b651ec3537ea4236a073f5e109` | yes |
| `all-in-one/sources/hmi_plc_tags.csv` | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` | `cf4c0650e7c7baac350dcb89909b808435704880` | yes |
| `all-in-one/sources/decoded-original/0030-FlgNet.xml` | `9252c9da764993de1edb8b2e44c46d6e9f9d4b6118e751a0dbeaa9ffd8ea721b` | `e74c70b751acdcdbc7a8b3b0c98aa773c2107cab` | yes |
| `all-in-one/sources/decoded-original/0397-FlgNet.xml` | `bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834` | `4ab8370493c4e28fc1eabeeebe2743d27f0c4021` | yes |
| `all-in-one/sources/decoded-original/0415-FlgNet.xml` | `7690a90cbad58f5e8474c94efc4a105e80522fb57e3516a720aab53e1146b07d` | `2cb9c21b425df9bfd0c36c0f8ab0257257a93a6e` | yes |
| `all-in-one/sources/decoded-original/0538-FlgNet.xml` | `afb3c3104bb60b4b1310f62ed5fb2caf659afc514c2b3fd209ff71d2008686ce` | `3372843d3fb58f402f82a6250588ffa90f7707dc` | yes |
| `all-in-one/sources/decoded-original/0555-IdentXmlPart.xml` | `46c36333e249dd775c1db94a1f6e80a36cf1a5a9c998b7d0980ae01d862901e6` | `9a915a8b9a260b48402df151c1fe0bbcb2f4ea1c` | yes |
| `all-in-one/sources/decoded-original/0557-IdentXmlPart.xml` | `536563da118493838d346a6b34b4367bed4185edbe150d79eb2b2042c3950bf0` | `f627dd27d001a8af1770fd43a5dc04ceb572d4e6` | yes |
| `all-in-one/sources/decoded-original/0558-IdentXmlPart.xml` | `45d49d53b6b41312960bb2a329663e87d8803e28d7832308424a6bf5091e6d1b` | `a0b681bd15e9ae15f2e1437576a4486cc732fdf2` | yes |
| `all-in-one/sources/decoded-original/0627-IdentXmlPart.xml` | `08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb` | `61ebc0abbb2ca160e11e1da400a3f14a397d8bc5` | yes |
| `all-in-one/sources/decoded-original/0628-IdentXmlPart.xml` | `9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd` | `170ca5c72599edc7ea7eefe651c3680ce325e76a` | yes |
| `all-in-one/sources/decoded-original/0629-IdentXmlPart.xml` | `67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972` | `058129bb01e27f7a6a0d0293f332d745e5bab74e` | yes |
| `all-in-one/sources/decoded-original/0635-IdentXmlPart.xml` | `1a057d686446a3fdab7ac61bb09bc543c52f49646c9ca71ac323c10fcdffe457` | `95bfcad59cfb0c12b573e9e8face4262d1e94622` | yes |
| `all-in-one/sources/decoded-original/0636-IdentXmlPart.xml` | `ec3d79f03e2748f8def4409ad676a97b98e28b9d8e68f6a64b3fe894466832ca` | `86114327ba1a010b2fcc01dd12b1bf86c01bc02c` | yes |
| `all-in-one/sources/decoded-original/0682-IdentXmlPart.xml` | `25c7aeb1bfa29c178eaa396db33d4eb6d2d29b9a3f2eb965fa61fae8ce7f1092` | `61182411e912941161eccf4e90c1f174e5379f0a` | yes |
| `all-in-one/sources/decoded-original/0684-IdentXmlPart.xml` | `6e9b3f173184adcddca503e81e2649022734b6ea3639c1d5ddaf0a08bac00208` | `d67b98b5d5516e0330aae5cfdbee41a3e09206e1` | yes |
| `all-in-one/sources/decoded-original/0686-IdentXmlPart.xml` | `b450d8ff22f0fffd7a214b2a696af28a03a27834ebf862bfaa822dc9bfb3c8d4` | `8c152d926692a8e15973c980e08e338d29411814` | yes |
| `all-in-one/sources/decoded-original/0692-IdentXmlPart.xml` | `bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037` | `737785d03b5fad43c5b4d451955726d800edb1c0` | yes |
| `all-in-one/sources/decoded-original/network-map.json` | `c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60` | `424430b6b953e43138e5d0a18ca40c949e21cfa1` | yes |
| `all-in-one/registers/hmi-transfer.json` | `235dec78a1a1d87d316df5339a18c19d279f7274d0e08912b5f4b2f0af0e7f9f` | `767fabb966bbb59dd9fffea5eb69bc654fcb3762` | yes |
| `all-in-one/build-program-model.py` | `8dc5478ae8ded7c1c47935c6ed950846811d97599e53cef7bafc558a4d87fbdd` | `834158b0fd89d8f6b0b5af9eb613c0c93a30f4b7` | yes |
| `all-in-one/assets/program-model-data.js` | `52f8199371e3399b7c0d44ab5469f0472aced79d56bbef2887f7625f5d2aff0f` | `38f34b0caa380a16ccad6f6f1e234a2fdf23f327` | yes |
| `all-in-one/assets/simulator-workspace.js` | `3a6dfc618ff7e7b238f2671dc85d65704f33093a18eac879d86081d92c31e8bc` | `97c2c831c77a9699fff0e0960b3bc1b7d93d45b3` | yes |
| `all-in-one/assets/virtual-plc.js` | `5f1876052dc0067b1f010af0dfc941946e37003167481731293615d9c1c36dbc` | `0bd9eceb54365a91214a37c5601b5067c39a3f75` | yes |
| `all-in-one/registers/program-model.json` | `6203479c086b15bada12ac9d7e37db9280234ec26f1ea6091d7211dc09a577c5` | `9860b10f008d3a5ae714be50d77b703dfec32f3a` | yes |