# VR03 로터리 밸브 원본 조사 초안

VR03은 P&ID에서 CY02·CY04·CY05의 분진을 모으는 SC01 출구의 로터리 밸브 VR-03/M37로 표시된다. 전기 원본은 61KM1 접촉기를 이용한 직접기동 회로이며, PLC 명령은 Q4.3, 원시 응답은 I5.4다. **I5.4는 61KM1의 13–14 보조접점 응답으로, 축 회전·분진 배출 완료를 직접 검출하는 신호로 확인되지 않았다.**

PLC 원본은 운전 요청 M_VR_03을 출력에 연결하고, 명령이 있는데 처리 응답이 없으면 전용 S5 2초 타이머로 고장을 Set한다. VR03 처리 응답은 별도로 SC01 요청 Reset과 FN04의 공유 예고장·지연 정지에 쓰인다. 시간 기록의 HOUR 경로에는 Add가 아닌 **Move 상수 1**이 있으므로 단순 누적 운전시간으로 설명하면 안 된다.

이 문서는 원본 조사·후속 독립 검토용이다. 매뉴얼 통합, UI·기록 구현, 게시, TIA 컴파일, 현재 CPU 또는 실물 복구를 완료했다는 뜻이 아니다.

## 작업 기준과 보존

- 대상: catalog_id `VR03`, kind `motor`, group `집진·석회`, parent_id 없음, depth 0, priority_key 없음. 이름은 로터리 밸브이며 다른 VR의 값·조건을 복제하지 않았다.
- 작업3 전체248 중 중복·기존 제외·부모보류·SYS-SIMULATION 영구중지를 반영한 자체 연구분모132의 두 번째 5개 묶음에 속하는 1개 조사다. 원본 phase2 후보133은 보존하며 로컬 2차133 통합·게시 제외 지시는 유지한다.
- 고정 읽기 원본: `source-mv06`, Git `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, v1.12.0. 참고 저장소는 `https://github.com/esp6662266/gme-plc-manual`이다. 이후 main·현장 상태를 이 스냅샷과 같다고 보지 않는다.
- 표준: GME-STD-1.0.0. `AGENTS.md`, 저장소 `gme-equipment-rollout` 스킬, WORK-STANDARD/WORK-ITEM-TEMPLATE/INVENTORY, 기존 진행·중복 검토를 읽었다.
- 읽기 전용 preflight 종료 0, `inventory_matches=true`. 전체248/우선23/대응18/제외90/제외부모 하위보류7/phase2 133이 일치한다. `source_byte_changes`는 requirements-audit.json과 all-in-one-data.json 두 파일로, 표준 생성 당시 바이트와 이 고정 버전의 차이다. 이번 조사에서 변경하거나 해시를 갱신하지 않았다.
- 조사일: 2026-10-11 UTC. 작성자: VR03 원본 조사 작업자. 실제 모델명·추론 설정의 런타임 증명은 별도 확보하지 않았다.
- 작성 범위: 이 MD 및 `extracts/VR03/`의 정적 추출·검토 결과. 원본 저장소, 공용 declarations.json, 다른 설비 초안, 공통 코드·버전·대장·배포를 수정하지 않았다.
- 근거·보존 확인70파일은 작업 파일 SHA-256과 고정 커밋 Git blob SHA-256이 모두 같다. 중지5자산은 freeze 명세 해시와도 모두 일치한다. 시작·종료 원본 Git 변경0. 파일별 해시는 부록에 있다.
- 시뮬레이터 작성·수정·생성·실행·행동 시험0. 금지 생성기·시험을 실행하지 않았다. 실제 PLC·현장·보호값·SEJIN 프로그램/운영자료/사진·이력을 변경하거나 통합하지 않았다.

이하 원본 경로는 특별한 설명이 없으면 고정 저장소의 `all-in-one/` 아래이며, `0266` 같은 축약은 `sources/decoded-original/0266-FlgNet.xml`을 뜻한다. `0604` 선언 축약은 `sources/decoded-original/0604-IdentXmlPart.xml`이다. LAD 번호는 원본 문서 ID, NID는 선언의 네트워크 식별자, 색인 순서는 별도다.

## 7영역 적용표

| 영역 | 적용 상태 | 확보한 근거 | 남은 범위 |
|---|---|---|---|
| 설비·자료 기준 | 적용 | VR03/M37, SC01/CY02·04·05 관계, 원본 버전·시점 | 현행 실물·명판·배치 동일성 |
| I/O·HMI | 적용, 일부 근거 미확보 | I5.4/Q4.3, DB13/DB2/DB3/DB9, HMI3행 | HMI 4개 데이터 ORef 결속·이벤트·온라인 주소 |
| 제어 구조 | 적용 | 출력/요청, 2초 고장, 자동 Set·Reset, SC01/FN04 영향, 호출·다른 쓰기 | 실제 실행순서·주기·전원 재시작·외부 쓰기 |
| 전기 전달 경로 | 적용 | FG61/121/140/254, 시공도 p35/51, P&ID p1 실제 렌더 | 현장 단자·정상 극성·설정·승인 준공도 |
| 알람·복구 | 적용 | VR_03_FAULT Set/Reset·요청 해제, 공유 예고장 경계 | 실제 표시·재요청·복구 증거 |
| 증상별 수리 | 적용, 관찰 지침만 | 요청→Q→접촉기→I→DB→HMI의 비교 지점 | 실제 관찰·원인 배제·조치·복구 기록 없음 |
| 완료 기준 | 적용 | 검사·미검사·부족자료·후속 검토 분리 | 통합/UI·기록/게시/TIA/CPU/현장 별도 |

## 1 설비와 자료의 소유 경계

1. `registers/equipment.json`의 VR03행은 motor, FG61, parent 빈값, 별칭 빈 배열이다. P&ID `PID_1684n002I.pdf` p1 실제 렌더는 CY-02·CY-04·CY-05 하부가 SC-01로 모이고 그 출구에 VR-03/M37이 붙은 관계를 보여 준다. M37 표기는 0.55 kW 440 V다. 이 도면 관계를 VR03이 특정 CY 본체의 PLC 소유자라는 증거로 바꾸지 않는다. P14 ‘2사이클론’ 실물 식별도 해결하지 않는다.
2. `Electrical_Rev2.pdf` FG61/PDF62의 제목은 `ROTARY VALVE VR-03`, 모터는 M37, 0.55 kW/1.25 A다. 상단은 THREE-PHASE LINE 440V 60Hz다. 직접기동 회로에 전용 인버터·속도 지령·아날로그 전류/PID·엔코더는 나타나지 않는다. **검토한 직접기동 경로에서 해당 제어는 비해당**이며 현장에 추가 장치가 전혀 없다는 단정은 아니다.
3. SC01은 별도 모터 M28, VR03은 M37이다. SC01이 VR03의 처리 응답을 읽어 요청을 해제하는 의존성은 있으며, 두 모터·고장을 한 장치로 병합할 근거는 아니다.
4. FN04 예고장은 여섯 처리 응답을 공동으로 읽는다. Tag_126 90분은 VR03 전용 고장 지연 Tag_75 2초와 기능·소유가 다르다. FN04의 속도·인버터·보호값을 VR03에 배정하지 않는다.
5. P&ID 도번1684n002의 원 작성일은 06/04/2011, 판 I 변경일은 15/01/2013이다. 전기 검토 시트에는 기본 날짜27.05.2024가 있다. 해당 FG61/121/140/254의 하단에서 별도 Rev2 날짜를 확인하지 않았으므로 파일명 Rev2만으로 각 시트에 Rev2 17.03.2025를 붙이지 않는다.
6. `Electrical_Can_Decoating_20241118.pdf` p35는 `24.11.11 first draft design`, CHECKED/APPROVED 공란이다. 문서상 경로·견적성 길이 근거이며 승인 준공도·실제 설치 길이로 확정하지 않는다. PLC 백업·P&ID·전기·시공도는 서로 시점이 다르다.

## 2 I O 및 HMI

### 2.1 직접 신호와 처리 메모리

| 신호 | 원본 형식·주소 | 선언·위치 | 해석과 한계 |
|---|---|---|---|
| `VR03_Fbk` | Bool, `%I5.4` | live_index doc517; `0613` SimpleAccess RID254, NID42 UID2314, SAD Input/AO44 | 물리 입력. FG61의 61KM1 보조접점 응답. 회전·배출 완료 검출로 해석하지 않음 |
| `Start VR03` | Bool, `%Q4.3` | doc1307; `0602` SimpleAccess RID177, NID36 UID1029 AK Write, Output/AO35; `0658` RID130 UID1102 | 출력 명령. 설명의 `a 52.7`은 과거 주석이고 실제 Address·도면은 Q4.3/A4.3 |
| `Flag.M_VR_03` | Bool, DB2.DBX2.5 | `0604` RID176 BO21/AO21 BAD2, `0603` Flag TOD N2; `0577` RID19 | 운전 요청·기억 비트. HMI 요청주소와 일치하나 Q출력/실물 상태와 별도 |
| `Allarm.VR_03_FAULT` | Bool, DB3.DBX2.5 | `0604` RID175; `0657` RID133 BO21, NID32 UID1107/1109/1110, `0655` Allarm TOD N3 | Set/Reset 유지 고장. HMI DB11,X58.1과 별도 영역 |
| `Inputs.VR03 Run` | Bool, DB13.DBX5.4 | `0604` RID219 BO44, NID27 UID23/NID34 UID994; `0657` RID300 NID32 UID1139; `0603/0655` Inputs TOD N13 | 처리 응답. 원시 I5.4와 다르며 워드 전달·다른 쓰기 영향을 받음 |
| `Tag_75` | Timer, `%T84` | doc1306; `0658` SimpleAccess RID131 Timer/AO84, NID32 UID1104 Write/1105 Read | VR03 고장 감시 S5 타이머. HMI 태그로 분류하지 않음 |
| `Flag.RESET_ALLARM` | Bool, DB2.DBX6.0 | `0657` RID13 BO48/AO48, NID32 UID1108; DepDB `0655` RID12 TOD N2 | 공통 Reset 요청. 원인 제거·재기동과 같은 의미가 아님 |
| `ON` | Bool, `%M0.0` | doc1556; `0602` RID1, NID36 UID1025; `0658` RID1 UID1101 | 원문 접점. 이름만으로 항상 TRUE라 전제하지 않음 |
| `hours motors.VR_03_MIN` | Int, DB9.DBW164 | `0615` RID256 BO1312, NID42 UID2315/2317/2318/2323; `0614` DB9 | Add1 및 Move0 대상. 실제 시간 단위·유효 누계는 실행·상위 저장 확인 필요 |
| `hours motors.VR_03_HOUR` | Int, DB9.DBW166 | `0615` RID258 BO1328, NID42 UID2321 및 NID55 UID3089 | Move1 및 공통 Move0 대상. 누적시간 Add라고 설명 금지 |
| `Tag_47` / `Tag_48` | Timer, `%T13` / `%T17` | doc107/108; `0613` RID1 Timer/AO13 및 RID284 Timer/AO17 | 각각 1분 명칭 타이밍·기록 후 Reset 관련 공통 시간부 |
| `Flag_Aggiorna_DB` | Bool, `%M1.7` | `0613` RID13 Memory/AO15, NID42 UID2324 SCoil | 여러 모터가 공유하는 업데이트 요청. DB 영구 저장 완료 신호라고 확정하지 않음 |

주소 환산은 원본 SAD 영역, SSD/AO·멤버 BO의 비트 오프셋, DepDBBlock TOD N을 대조했다. 현재 CPU·최적화 DB 설정·실제 I/O 주소·온라인 값을 검증한 결과는 아니다.

### 2.2 원시 입력과 처리 응답 전달

- LAD1070 `0397`, hmi inputs 색인1/NID1: Part35 Move의 `in`은 ORef36/RID10 `Tag_180`, `out1`은 ORef37/RID11이다. Wire39가 in, Wire40이 out1 연결이다.
- `0627` RID10은 Word/Input/AO32이며 doc1591의 `%IW4`와 대조된다. `0629` RID11은 Word/AO32, BAD BIRID4이고, `0628` DepDBBlock RID4는 Inputs/DB13이다. 따라서 해당 Move는 IW4→DB13.DBW4로 확인된다. 같은 워드 내 I5.4가 DB13.DBX5.4 위치로 전달되는 대응이다.
- 앞단 Part22.eno→Part27.en은 Wire34, Part27.eno→Part35.en은 Wire41이다. Part22/27/35에는 `DisableENO="true"`가 있다. 선 연결·속성은 확인했지만 해당 TIA 판본의 실제 ENO 실행 의미와 현재 호출 유효성을 검증하지 않았다. 무조건 매 스캔 복사된다고 쓰지 않는다.
- main LAD1613 `0030`, 색인2/NID19: CRef21 Recipes Handler → CRef23 HMI → CRef25 HMI Output의 ENO 연쇄(W31/32/33), CRef25.eno→Part37 `NOT Simulation(1)`(W42/44), Part37.out→CRef28 HMI Inputs.en(W43). CodeBlock29/RID135는 `0688`의 HMI Inputs, ORef45/RID140은 `0692`의 Simulation(1)이다.
- `0635`에는 `Inputs.VR03 Run` RID130, NID4/UID61 AK Write가 있다. 기존 네트워크 색인의 simulation LAD1085에 대응하는 **정지된 자료 안의 다른 Writer 존재**만 보존한다. 활성 여부를 판단하거나 시뮬레이터를 실행·시험하지 않았다. 비트 이름 검색만으로 ‘처리 응답 Writer는 Move 하나뿐’이라고 결론내리지 않는다.

### 2.3 HMI 설정과 원본 호출의 결속 한계

`sources/hmi_plc_tags.csv`는 `dde.cfg 설정; 온라인 현재값 아님`이라고 명시한다. VR03의 직접 설정행은 아래 3개이며 모두 Access Name=PLC다.

| 파일 행 | HMI 태그 | 설정 주소 | 내부 ID | 확정 범위 |
|---|---|---|---|---|
| 129 | `VR_03\Allarme1` | DB11,X58.1 | 00334 | 설정행 존재. DB3 고장 비트와 동일 주소가 아님 |
| 417 | `VR_03\RispostaA` | DB11,X58.0 | 001BA | 표시 응답 주소 설정. 원시 I5.4와 별도 |
| 452 | `VR_03\Flag` | DB2,X2.5 | 00192 | M_VR_03 선언 주소와 일치. 실제 버튼 이벤트·권한·쓰기 시점은 미확정 |

LAD1206 `0382`는 hmi 색인29/제목vr03이다. CRef23/RID638 내부 CodeBlock22/RID1은 `0623`의 HMI Standard Motors 호출 선언과 대응한다. `0624`에는 CRef의 호출 인터페이스가 있다. 다만 network-map의 inferred_original_nid는 null이고 데이터 ORef4개를 UID/RID/해당 NID에 일치하는 이름 선언으로 결속하지 못했다. 검색 문자열을 선언 확정으로 승격하지 않았다.

| Wire | 실제 원본 핀 연결 | 해석 상태 |
|---|---|---|
| 21 | Powerrail→CRef23.en | 호출 허가 선 확인 |
| 24 | ORef25/RID662→CRef23.Ingresso_run | 검색 문자열은 Inputs.VR03 Run 후보. 일치 이름 선언 미확보 |
| 28 | ORef29/RID348→CRef23.Allarme1 | 검색 문자열은 Allarm.VR_03_FAULT 후보. 일치 이름 선언 미확보 |
| 30/32/34/36 | ORef31/33/35/37, 모두 RID48→Allarme2/3/4/5 | `0626` LiteralConstant RID48 FALSE 선언·UID 호출 기록 존재. 네트워크 NID 최종 결속은 별도 |
| 42 | CRef23.Risposta→ORef43/RID352 | 검색 문자열은 Motors.VR03.Risposta 후보. 이름·주소 결속 미확보 |
| 46 | CRef23.Comulativo_allarmi→ORef47/RID354 | 검색 문자열은 Motors.VR03.Allarme_comulativo 후보. 이름·주소 결속 미확보 |

HMI3설정행, 원본 함수 호출핀, PLC DB11 상태 레이아웃, 화면 이벤트의 네 단계를 분리한다. 이 조사만으로 DB3.DBX2.5가 DB11.DBX58.1에 실제 갱신된다고 확정하지 않는다. HMI 4개 데이터 ORef의 원 프로젝트 선언, DB11 구조와 함수 내부, 화면 스크립트/이벤트·온라인 비교가 남아 있다.

## 3 제어 구조와 다른 쓰기

### 3.1 직접 요청 해제와 출력

LAD1966 `0266`, motors 1 색인37/NID36. Part5개, Wire9개는 모두 대상 선언과 대조했다.

| 구분 | 원본 연결과 선언 | 정적 해석 | 미확정 경계 |
|---|---|---|---|
| 공통 허가 | W1044 rail→Contact1038.in, W1030 ORef1025/RID1 ON→operand | ON 접점이 아래 두 분기를 허가 | ON의 실제 값·블록 호출 여부 |
| 고장으로 요청 해제 | W1039 1038.out→Contact1040.in, W1031 ORef1026/RID175 fault→operand, W1041 1040.out→RCoil1020.in, W1033 ORef1027/RID176 M_VR_03→operand | ON AND VR_03_FAULT이면 요청 Reset | 같은 사이클의 다른 Set·HMI 쓰기·실제 우선순위 |
| 출력 명령 | W1039 1038.out→Contact1042.in, W1034 ORef1028/RID176 M_VR_03→operand, W1043 1042.out→Coil1024.in, W1036 ORef1029/RID177 Start VR03→operand | ON AND M_VR_03을 일반 Coil 출력으로 연결 | 명령이 코일 전압·접촉기·회전에 도달했는지는 별도 |

출력 분기에 `NOT fault` 접점이 직렬로 들어 있는 형태가 아니다. 별도 RCoil로 요청을 해제하는 구조다. 이 네트워크에 전용 Local/Auto 선택·Maintenance·축속도 허가가 없다고 해서 전체 설비의 안전조건이 없다고 결론내리지 않는다. 상위 호출·자동 요청·하드웨어 보호 경로가 따로 있다.

### 3.2 자동 요청의 Set과 Reset

`0577` GlobalAccess RID19의 M_VR_03 선언은 NID3 UID598 Set, NID4 UID942 Set, NID5 UID1018 Reset의 Write를 담는다. motors 1의 RID176 NID36 UID1027 Reset과 함께 네 개 LAD 쓰기 위치를 확인했다. HMI DB2,X2.5의 외부 쓰기 가능성은 별도다.

| 기능 | 원본 조건·핀·상수 | M_VR_03 쓰기 | 경계 |
|---|---|---|---|
| 예열 | LAD1843 `0164` 색인3/NID3. ON Contact785→NOT Emergency Contact22→Eq400(Tipo_preset=1)→Auto_ON1 Contact823. W672에서 Eq416.pre로, ORef596=Tempo_presetting와 ORef597/RID18 Int3 비교, W681 | Eq416.out→SCoil420.in, W682 ORef598/RID19→operand | Tempo 값3이란 원문. 실제 3초 경과라고 단정하지 않음 |
| 생산 | LAD1844 `0165` 색인4/NID4. ON1145→NOT Emergency1154→Auto_ON1 1147→Eq737(Tipo_preset=2). Eq753.pre로 W1021, ORef940 Tempo와 ORef941/RID18 Int3 비교, W1030 | Eq753.out→SCoil757.in, W1031 ORef942/RID19→operand | 동일한 시점값3이나 예열과 상위 모드 조건이 다름 |
| 전체 정지 시퀀스 | LAD1847 `0166` 색인7/NID5. Auto_ON1 Contact1095→Eq881(Tipo_preset=5). W1031가 Eq957.pre와 Emergency Contact1106.in을 허가. Eq957은 ORef1016 Tempo와 ORef1017/RID102 Int20 비교. W34/35에서 Eq957.out OR Emergency Contact1106.out→O33, W1078 | O33.out→RCoil961.in, W1079 ORef1018/RID19→operand | Auto_ON1 AND Tipo5 AND (Tempo20 OR Emergency)의 해당 분기. Emergency가 모든 모드에서 무조건 이 Reset을 한다는 해석 금지 |
| 직접 고장 | LAD1966 `0266`, ON AND VR_03_FAULT | RCoil1020 | 출력 조건·다른 Writer와 함께 검토 |

상수 `0578` RID8/UID591 V1, RID78/UID935 V2, RID22/UID985 V5, RID18/UID597·941 V3, RID102/UID1017 V20을 각각 대조했다. Tipo_preset는 `0577` RID12 Int/BO784=DB1.DBW98, Tempo_presetting는 RID7 Int/BO768=DB1.DBW96, Auto_ON1은 RID4 Bool/BO59=DB2.DBX7.3, Emergency_module_fault는 RID108 Bool/BO134=DB3.DBX16.6이며 DB번호는 `0576`의 종속 선언과 대조한다. 이러한 저장부의 현재 값·변경 경로와 실제 시간성은 별도 확인한다.

### 3.3 SC01과 FN04에 미치는 영향

- **SC01:** LAD1956 `0258` 색인27/NID27에서 ON819 뒤, fault821.out→OR790.in1(W822), `NOT Inputs.VR03 Run` Contact22.out→`NOT UNDER TESTING` Contact825.in(W24)→OR790.in2(W826)다. OR790.out→RCoil795.in(W812), ORef804/RID136 M_SC_01→operand(W814). 식은 ON AND [SC_01_FAULT OR (NOT VR03 처리Run AND NOT UNDER TESTING)]→SC01 요청 Reset이다. VR03 센서가 SC01 자체 센서인 것은 아니다. UNDER TESTING은 이 분기의 원문 조건이며 임의 우회 권고가 아니다.
- **FN04 공유 예고장:** LAD1964 `0264` 색인35/NID34. ON Contact1020→Inputs.FN04 Run Contact1022 뒤에 SC01/VR03/SC10/VR04/SC11/VR05의 각각 부정 접점1024/1026/1028/1030/1032/1034가 OR972.in1~6로 들어간다. VR03 경로는 ORef994/RID219(W1007)→Contact1026 NOT→OR972.in2(W1027)다.
- OR972.out(W1012)는 Coil982 `Allarm.Prealarms_FN04`(ORef999/W1013), SdCoil985, Tag_126 Contact1036을 함께 허가한다. 타이머 value ORef1000/RID112/W1014는 `0606`의 `S5T#1H_30M`(V13632), operand ORef1001/W1015 및 접점 ORef1002/W1016은 `0602` RID169 Timer/AO131=`%T131`이다. Contact1036.out→Coil990.in(W1037), ORef1003/W1018=`Stop_Fan_FN04`.
- **FN04 요청 해제까지의 연결:** `0605`의 Stop_Fan_FN04는 InterfaceAccess RID170, NID34 UID1003 Write/NID35 UID1019 Read다. LAD1965 `0265`에서 ON1038 뒤 Contact1042가 이 Local을 읽고(W1029), W1043→OR1003.in4, W1031→RCoil1010.in, W1033 ORef1021 Flag.M_FN_04 Reset으로 연결된다. 여러 정지 원인 중 하나이며 VR03 하나의 전용 FAN 고장으로 표시하지 않는다.

이 영향은 원본 선과 선언의 정적 해석이다. 실제 타이머 진행·선행 정지·PLC 호출·발생 시각·현재 필드 동작은 미확인이다.

### 3.4 호출과 실행순서의 경계

| 원본 | 확인한 호출 허가 | 선언 근거 | 확정하지 않은 사항 |
|---|---|---|---|
| main LAD1619 `0031` 색인8/NID6 | ON Contact282.out(W283)→CRef264.en, CodeBlock275/RID58 Allarms1 | `0688` RID58 NID6 UID275 AK Call | 실제 CPU에서 알람 실행·전후 인터럽트 |
| main LAD1620 `0549` 색인9/NID7 | ON Contact350.out(W351)→CRef319.en Motors1, CRef334.en time work motor | `0688` RID67 UID337, RID82 UID347 | 원본 색인상 앞 알람/뒤 모터 관계와 실제 실행 우선순위·현재 순서 |
| cyc_int2 ogni1s LAD1723 `0024` 색인5/NID4 | ON Contact188.out(W189)→CRef183.en, CodeBlock186/RID39 Auto start motors | `0067` RID39 UID186; ON은 `0068` | 블록명만으로 현재 인터럽트 주기 1초를 검증한 것이 아님 |
| main LAD1613 `0030` | Recipes Handler→HMI→HMI Output ENO 및 NOT Simulation(1)→HMI Inputs | `0688/0692`, W31/32/33/42/43/44 | ENO 실행·원시 전달의 현재 유효성 |

LAD1966의 Reset과 출력 Coil, LAD1810의 Set/Reset, 자동 Set/Reset과 HMI 쓰기가 공존한다. 네트워크 선·색인과 실제 최종값·재시작·복구 완료를 분리한다. 현재 프로젝트의 교차참조 및 온라인/오프라인 실행 검토가 필요하며 이 작업에서 실행 시험하지 않았다.

## 4 전기 전달 경로

전기 PDF62/122/141/257, 시공 PDF35/51, P&ID p1을 실제 렌더해 끝점·접점·기호를 확인했다. PDF 번호와 FG는 같지 않다. 아래 6개 연결은 BC01 개수를 복제한 목표가 아니라 VR03에서 확보한 문서 경로다.

| 경로 | 원본 FG와 PDF | 확인한 양 끝점·중간 경로 | 남은 경계 |
|---|---|---|---|
| 3상 주회로 | FG61/PDF62 | 8.3L1/L2/L3(58/9)→61QM1 1/3/5–2/4/6→61KM1 1/3/5–2/4/6→61U1/V1/W1 및 XM61U1/V1/W1→61QS1 1/3/5–2/4/6→M37 U/V/W, PE | 실제 공급·상순서·정상 회전·모터/감속기 명판 미확인 |
| PLC 출력의 모듈 끝점 | FG140/PDF141 | CPU515, MOD15, A4.3 단자4→참조61/4→FG61 A4.3. 출력측 전원 +24Vdc10.9→X21 3032 4A F 5×20→140.1→단자10, 0Vdc10.6→단자9 | 모듈 형번·실제 설치·전원/출력 전압 미확인 |
| 접촉기 제어 | FG61/PDF62 | A4.3(140/1)→XS59→61QS1 보조접점→XS60→선61.1→61QM1 보조접점→61KM1 A1; A2→−0Vdc10.6 | QS/QM 보조접점 숫자 단자는 렌더에서 명확히 확인되지 않음. 코일/접점 정상극성·실물 결속 미확인 |
| 원시 피드백 | FG61/PDF62와 FG121/PDF122 | +24Vdc10.7→61KM1 보조13–14→E5.4(121/5)→FG121의 E5.4, CPU515 MOD9 단자15, 역참조61/6 | 접촉기 보조응답. 축회전·분진 실제 흐름을 보증하지 않음 |
| 입력 모듈 전원 | FG121/PDF122 | +24Vdc10.7→X21 3008 2A IST.5×20→121.1→단자20; −0Vdc10.6→단자19 | 이 전원이 살아 있는지·실제 퓨즈와 배선은 별도 |
| 현장 모터 케이블 | 시공 PDF35/51 | 케이블1_23 `=DUS+VR03-M37A`, CR→VR-03/M37. p35 DUST ZONE01, Route211 RA→Pipe16→M37. p51 CV4심1.5, 경로100→200→210→211RA→E100 | 승인 준공·실제 길이·코어 단자대 번호·시공 변경 미확인 |

### 4.1 정격 표기와 부품 목록

- FG61에 M37 0.55 kW/1.25 A, 61QM1 범위1.1–1.6 A, 패널 배선 BLACK FS17 1.5 mm²가 적혀 있다. 이것은 도면의 정격·범위 표기다. 현행 보호기 설정을 1.25 A 또는 범위 내 임의값으로 바꾸라는 지침이 아니다.
- FG254/PDF257 BOM: 61KM1 `3RT2015-1BB41`, CONTACTOR3KW/1L/DC24V/S00; 부속 `3RT2916-1CB00` RC; 61QM1 표기 아래 `3RV2901-1E` 보조접점, `3RA1921-1DA00`, `WR32433`, `3RV2011-1AA10` MAGNETOTHERMIC1.1–1.6A가 이어진다. 수량열은 각각1이다. 첫 61QM1 행이 보조접점 부품인 점을 보존하고 그 행 하나를 차단기 본체 형번으로 읽지 않는다.
- 원본 제조사 표시는 Siemens 및 어댑터 Whoner다. 현행 설치 모델·대체품·ABB 대응·토크·안전한 보호설정은 명판·승인자료·해당 제조사 원문 없이 채우지 않았다.
- p51 케이블1_23은 Current Type GAC, CV, CORE4, SIZE1.5, SPARE0, adjustment3, LEN101로 표시된다. p35의 Pipe16은 관로 표기이며 단면적·접점번호로 읽지 않는다. 길이101의 단위·준공 측정값은 추가 자료 없으므로 문서 열값만 보존한다.

### 4.2 도면 관계에서 오해하지 말아야 할 항목

- A4.3은 출력 명령이며 +24Vdc10.7은 별도 피드백 전원선이다. 둘을 같은 전압 관찰점으로 합치지 않는다.
- 61KM1 A1/A2 코일과 13/14 보조접점, 주접점1/2·3/4·5/6을 구별한다. 13–14를 모터 주전류 경로로 설명하지 않는다.
- 61QS1의 주회로 및 별도 제어 보조접점, 61QM1의 주회로 보호 및 제어 보조접점을 각각 보존한다. 도면상 기호 존재로 현장 정상극성·실제 손상 원인을 확정하지 않는다.
- 시공도에서 같은 DUST ZONE에 있는 PV14/ZS.O/ZS.C/TC09나 DUS1TB1·DUS1TB2를 VR03 부속 PLC 신호로 배정하지 않는다. 이들의 관로 경유 관계와 설비 소유는 다르다.

## 5 알람과 복구

### 5.1 VR03 전용 고장

LAD1810 `0444`, allarms1 색인30/NID32. 원본 9 Part/17 Wire를 대조했다.

| 단계 | 원본 Part·Wire·ORef | 해석 |
|---|---|---|
| 공통 허가 | rail W1137→ON Contact1125, operand ORef1101/RID1 W1111 | ON이 Start 감시 및 Reset 가지를 허가 |
| 감시 시작 | Contact1125.out W1126→Start Contact1127, ORef1102/RID130 W1112 | 명령이 켜진 상태 |
| 응답 부재 | Start1127.out W1128→Contact1138 NOT, ORef1139/RID300 처리Run W1141, W21→SdCoil1089.in | ON AND Start VR03 AND NOT Inputs.VR03 Run |
| 시간과 타이머 | ORef1103/RID28 W1113→1089.value, ORef1104/RID131 W1114→1089.operand | `0656` S5Time `S5T#2S` V512, `0658` Tag75 Timer84. VR03 전용 2초 |
| 고장 Set | Start1127.out W1128→Tag75 Contact1129, ORef1105/RID131 W1115, W22→SCoil1095.in; ORef1107/RID133 W1118 | ON AND Start VR03 AND Tag75 접점 결과→VR_03_FAULT Set |
| 고장 Reset | ON1125.out W1126→Reset Contact1133, ORef1108/RID13 W1120→fault Contact1135(W1134), ORef1109/RID133 W1121, W1136→RCoil1100.in; ORef1110/RID133 W1123 | ON AND RESET_ALLARM AND VR_03_FAULT→동일 고장 Reset |

타이머 구동의 NOT 처리Run은 고장 Set 코일의 직렬 접점이 아니라 타이머 입력 가지에 있다. Set은 Start와 타이머 접점으로 연결된다. 임의로 `NOT Run`을 Set 식에 추가·삭제해 새 논리를 만들지 않는다. 선언의 S5Time V512는 인코딩된 원문 값이며 512ms로 해석하지 않는다.

### 5.2 고장 해제와 운전 복구의 차이

고장은 LAD1966에서 M_VR_03 Reset 원인이다. Reset 버튼으로 고장 비트가 내려가는 것과 운전 요청이 다시 생성되는 것은 별도다. 요청은 자동 Set 위치·HMI 외부 쓰기·실제 실행순서와 대조해야 한다. 현장에서는 원인 제거, 보호·전원·접촉기·실제 기계 상태, 명령/응답/표시의 일치를 확인한 뒤 현장 절차에 따른 재요청과 복구 증거가 필요하다. 이 초안은 Reset이나 재기동을 직접 수행하거나 승인하지 않는다.

같은 네트워크에 Set과 Reset 쓰기가 모두 있다. 동시 조건의 최종값, 요청 재Set과 고장 Reset의 스캔 경계, 전원 재시작 시 잔존 요청은 TIA/현재 CPU 검증 전이다. 타이머·알람 비트만 잠시 해제된 상황을 복구 완료로 기록하지 않는다.

### 5.3 공유 예고장과 시간 기록

VR03 Run 부재가 FN04의 OR 입력 중 하나에 해당할 수 있다. 그러나 FN04 예고장과 90분 지연 정지는 FN04 Run 및 다른 다섯 응답과 함께 판단해야 한다. VR03 전용 고장2초와 합산하거나 ‘VR03는90분 뒤 고장’으로 쓰지 않는다.

운전시간 LAD1040 `0327`의 핵심은 다음과 같다.

1. Tag47 Contact2342와 원시 VR03_Fbk Contact2344 직렬. W2345는 Add2296.en과 Ge2303.pre를 함께 허가한다. 시간 계수는 처리Run DB13보다 원시 I5.4를 읽는 경로다.
2. Add2296은 Int 타입. `in1` ORef2315/RID256 MIN(W2327), `in2` ORef2316/RID7 Int1(W2328), `out` ORef2317/RID256 MIN(W2329). 분 저장값+1 쓰기다.
3. Ge2303은 Int MIN ORef2318(W2330)와 Int60 ORef2319/RID8(W2331) 비교. `out`→Move2306.en(W2332).
4. Move2306.`in`은 ORef2320/RID7 **상수1**(W2334), `out1`→ORef2321/RID258 HOUR(W2335). HOUR+1 Add 경로가 아니다.
5. Move2306.eno→Move2309.en(W2336), Move2309.in ORef2322/RID12 Int0(W2337), out1 ORef2323/RID256 MIN(W2338), eno→SCoil2312.in(W2339), operand ORef2324 Flag_Aggiorna_DB(W2340).
6. `0616` RID7(V1)/RID8(V60)/RID12(V0)의 NID42/해당 UID를 대조했다. Add와 비교의 스캔 평가·ENO·데이터 저장은 실행 검증하지 않았다.
7. LAD1053 `0340` 색인52/NID55: Tag48 Contact3111→Move3070(FN04 HOUR0)의 en; Move3070.eno W3099→Move3073.en. Move3073.in은 ORef3088/RID12 Int0(W3100), out1 ORef3089/RID258 VR03_HOUR(W3101). VR03 HOUR0 쓰기는 첫 Move의 ENO 뒤이며 단독 초기화 Coil로 설명하지 않는다.
8. LAD1056 `0019` 색인55/NID58: `NOT Tag47` Contact3120.out W3121→SdCoil3112.in, value ORef3114/RID335=`S5T#1M`, operand ORef3116 Tag47. 이름/원문 타이머가1분이지만 실제 펄스 주기·누락·현재 값은 미확인이다.
9. LAD1055 `0341` 색인54/NID57: ON3147 뒤 Flag_Aggiorna_DB3149→SCoil3110 MEM2_0; MEM2_0 Contact3151 뒤 NOT Flag_Aggiorna_DB3153→SdCoil3118(value ORef3128/RID334 S5T#5S, operand Tag48). 같은 MEM2_0 뒤 Tag48 Contact3155→RCoil3123 MEM2_0. 제목은 ‘DB에 데이터 기록 후 시간 Reset’이지만 DB 기록 완료의 실제 handshake·HMI 누계·영구 저장을 이 제목만으로 확인하지 않는다.

HOUR0/1과 MIN값만으로 총 누적시간·정비주기·가동률을 계산하지 않는다. 외부 누적 처리와 값 변경 이력을 확보해야 한다. 원본의 Move1을 오타로 추정해 Add로 고치거나 제어 로직을 변경하지 않았다.

## 6 증상별 관찰과 수리 판단

아래는 검토할 관찰점이다. 실제 고장 진단·전기 작업 지시·보호 우회·라이브 시험이 아니다. 활선 측정·분해·강제 출력 없이 현장 자격자와 승인 절차로 확인한다.

| 증상 | 먼저 비교할 관찰점 | 원인 배제에 필요한 근거 | 복구 확인의 경계 |
|---|---|---|---|
| HMI 요청이 있는데 출력이 없음 | HMI DB2,X2.5, M_VR_03, ON, VR_03_FAULT, 자동 Set/Reset 모드·Tempo, Q4.3 | HMI 이벤트 실제 Write, LAD1966 RCoil, LAD1847 전체정지와 동일 시각 교차참조 | 버튼 표시만으로 PLC 요청·출력 확정 금지 |
| Q4.3 명령은 있는데 모터가 안 돎 | FG140 단자4, XS59/60, QS1/QM1 경로, KM1 A1/A2, 주회로/모터 상태 | 도면과 실물 단자·안전한 전압 확인, 접촉기/보호기·기계부 상태 | Q=1을 코일 여자·회전 완료로 기록 금지 |
| 기동 뒤 VR03 FAULT 발생 | Start, Tag75, I5.4, DB13.DBX5.4, 접촉기13/14, 감시/Reset 시각 | 명령이 있었는지, 2초 타이머 조건, 원시/처리 전달·다른 Writer·호출 경계 | 알람 Reset만으로 원인 제거·복구 완료 금지 |
| I5.4는 켜졌는데 처리Run/HMI가 다름 | IW4→DB13.DBW4, HMI Inputs 허가·ENO, HMI의 DB11,X58.0/58.1 | 실제 DB 구조, 미결속 HMI4 ORef, 통신 및 화면 이벤트·현재 프로젝트 | HMI 표시 문제를 곧바로 기계 고장으로 확정하지 않음 |
| VR03 문제와 함께 SC01이 멈춤 | VR03 처리Run, SC01 fault/M_SC_01/Q3.4, UNDER TESTING 읽기값 | LAD1956 OR와 NOT 조건, 발생 순서·두 모터 실제 상태 | VR03 고장을 SC01 고장으로 병합하지 않음 |
| FN04 예고장 또는 후속 정지 | FN04 Run, 여섯 처리 응답, Prealarms_FN04, Tag126, Stop_Fan_FN04, M_FN_04 | LAD1964→1965 연결, 90분 타이머와 다른 정지 원인 | VR03 한 신호만으로 FAN 정지 원인을 확정하지 않음 |
| 운전시간이0/1로 보이거나 증가가 이상함 | 원시 Fbk, Tag47, MIN164/HOUR166, Flag_Aggiorna_DB, Tag48, 외부 누계 | LAD1040 Move1/1053 Move0/1055 handshake, 저장 이력 | HOUR값을 실제 누적시간·정비기한으로 바로 사용 금지 |

관찰 기록에는 관찰자, 시각·시간대, 장치/프로젝트 버전, 안전한 수집 방법, 실제 위치, 값·단위, 비교한 원본, 배제한 원인과 근거, 수행한 승인 조치, 재발 여부 및 복구 증거를 남긴다. 미관찰 칸을 정상값으로 채우지 않는다. 사진·사용자 운영 기록은 이 공개 소스 초안에 복제하지 않는다.

## 7 누락 자료와 완료 기준

### 7.1 우선 확보할 자료

| 필요한 자료 | 수집 위치 | 판단하려는 사항 |
|---|---|---|
| 현재 PLC 프로젝트·교차참조·DB 구조 | 승인된 TIA/엔지니어링 백업 | 고정 원본과 동일성, 호출·주기·다른 Writer, 최종 실행순서 |
| HMI 함수/화면 이벤트·DB11 구조 | HMI 원 프로젝트·PLC 인터페이스 | 0382의 미결속 ORef4개와 DB11 표시주소, Flag 쓰기 연결 |
| 원시/처리/표시 동시 관찰 | 승인된 현장 관찰 기록 | I5.4↔DB13.DBX5.4↔DB11/HMI 차이와 시간 경계 |
| M37/61KM1/61QM1/61QS1 명판·배선 사진 | 현장 담당자·승인 설비 기록 | 현재 모델·단자·정격·보호설정·접점극성, 도면 동일성 |
| 모터·밸브·SC01 실제 배치와 기계 자료 | 현장 배치도·정비 승인 자료 | P&ID 관계와 실물, 회전/배출 확인 수단 |
| 케이블1_23 준공 경로·양끝 단자 | 승인 준공도·단자대/케이블 마킹 | CV4×1.5·101 열값과 실제 시공의 차이 |
| 시간 저장·누계 처리 자료 | 외부 기록부/HMI/DB 저장 설계 | HOUR Move1·공통Reset의 의미, 총 운전시간 산출 여부 |
| 고장·조치·복구 이력 | 승인된 수리 관찰 기록 | 원인 제거·재요청·정상 배출과 재발 여부 |

### 7.2 네 기능과 기록 보존

| 기능 | 이번 적용 | 실제 확인 상태 |
|---|---|---|
| 도면·래더 비교 | 원본 끝점과 XML핀을 이 문서에 연결 | 문서 조사만. VR03 전용 UI 구현/동작검사 미수행 |
| 백업·선택 복원 | 후속 구현 시 기존 키·초안·미지필드·다른 설비 기록 보존 필요 | 새 저장/복원·재열기 검사 미수행 |
| 기록 전후 비교 | 관찰 시각·프로젝트·원본·값을 분리하도록 항목 제시 | 비교 기능의 VR03 지원 미검증 |
| 보고서/PDF | 요청된 MD 조사초안 작성 | 사용자 운영 보고서/PDF 생성·저장 기능 미구현/미검증 |

### 7.3 수행 검사와 미수행 검사

- 수행: 저장소 고정 커밋/버전/Git 상태 읽기, 읽기전용 preflight, 선언·상수·Part/Wire/ORef/CRef/CodeBlock 대조, 선택 근거70파일의 SHA-256↔고정 Git blob 비교, 중지5파일 freeze해시 비교, 원본 PDF7개 페이지 실제 렌더 및 관련 확대부 시각 검토, MD 자체 검토.
- 전기7개 페이지는 Electrical_Rev2 PDF62/122/141/257, 시공PDF35/51, P&ID p1이다. 탐색용으로 추가 렌더한 색인·배치 페이지를 핵심회로 독립검토 완료 수에 더하지 않는다.
- 수행 결과: 해시70/70 일치, 중지5/5 일치, 원본 Git 변경0. XML Gate/NOT/Wire·선언 주소/상수·live index·파일 존재/해시159개 정적 단언 통과(제어 실행·시뮬레이션 아님). preflight는 inventory_matches=true. 기계/전기 현장 정상 여부를 판정한 것이 아니다.
- 미수행: 프로그램 생성기, npm test/build, BC01 회귀·필수14검사, UI/검색/기록/복원/ZIP/CSP/배포 검사. 코드·매뉴얼 통합을 하지 않은 독립 조사초안이므로 해당 완료를 주장하지 않는다.
- 미수행: TIA 복원/컴파일·오프라인 실행, 현재 CPU 비교, 현장 측정·운전·복구. 시뮬레이터 관련 시험은 영구 중지여서 계획/미실행의 오래된 색인을 재개하지 않는다.

### 7.4 상태

| 구분 | 상태 | 의미 |
|---|---|---|
| documentation | draft_complete_with_gaps | 원본 조사초안 준비. 핵심 근거 제한 대조 완료; 사용자 독립 검토 대기 |
| static_review | source_reviewed | 선언/선/주소·PDF 렌더·해시 자체 대조. 독립 통합 검증 아님 |
| ui_records | not_run | 전용 기능 구현·저장/재열기 검증 없음 |
| publication | not_published | 이번 초안의 매뉴얼/GitHub/Netlify 게시 없음 |
| tia_compile | not_performed | 원본 복원·컴파일 미수행 |
| live_cpu | not_performed | 현재 프로그램·온라인 값 미대조 |
| field_recovery | not_performed | 실물·정상극성·복구 미검증 |
| simulator | permanently_stopped | 작성·수정·생성·실행·행동시험0 |

## 다음 검토 한 작업

이 VR03 초안의 핵심 세 경로, 즉 `0266` 요청해제/출력, `0444` 2초 Set/Reset, FG61↔FG121/140 전기 끝점을 독립 검토한 뒤 초안준비로 수신 여부를 결정한다. 0382의 미결속 HMI 데이터4개와 현재 실물·시간 누계의 미확정은 그대로 남긴다. 사용자 승인 없는 로컬 2차133 통합·게시로 넘어가지 않는다.

## 부록 A 근거 파일 해시

모든 해시는 고정 커밋 abcf31c5030bc7ef8749ed8e869a857f2387a28a의 Git blob 바이트를 별도로 읽어 대조했다. 아래 경로는 저장소 루트 기준이다. 상세 바이트수·Git blob SHA-256·일치 결과는 함께 만든 `extracts/VR03/source-hashes.json`에도 기록했다. 원본 파일 해시는 파생 추출물·이 MD의 해시와 구분한다.

| 파일 | SHA-256 | Git blob 대조 |
|---|---|---|
| `AGENTS.md` | `0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2` | 일치 |
| `VERSION.json` | `5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7` | 일치 |
| `all-in-one/assets/program-model-data.js` | `52f8199371e3399b7c0d44ab5469f0472aced79d56bbef2887f7625f5d2aff0f` | 일치 |
| `all-in-one/assets/simulator-workspace.js` | `3a6dfc618ff7e7b238f2671dc85d65704f33093a18eac879d86081d92c31e8bc` | 일치 |
| `all-in-one/assets/virtual-plc.js` | `5f1876052dc0067b1f010af0dfc941946e37003167481731293615d9c1c36dbc` | 일치 |
| `all-in-one/registers/all-in-one-data.json` | `63a46b36b6454bf1246d093300dbee11f2fcc287ad94991405369bf9f939a8fe` | 일치 |
| `all-in-one/registers/equipment-hmi.csv` | `2cdce600aa0138cc5025022e57d9d61a948afb237f70c70e2d11e8300e73286a` | 일치 |
| `all-in-one/registers/equipment.json` | `7870325dff32bbca90fa34507b301c4aad3347d669fddcd03b910343663996fa` | 일치 |
| `all-in-one/registers/plc-symbols.csv` | `a0334b390f06ddb515d6c09ca96a01d35d44029c1b726ef0ff53303ec04ff91f` | 일치 |
| `all-in-one/registers/program-model.json` | `6203479c086b15bada12ac9d7e37db9280234ec26f1ea6091d7211dc09a577c5` | 일치 |
| `all-in-one/registers/simulator-freeze.json` | `bb93c1994effc5609939ba566b7802ce7ed55154a7310f02379b308ac2c8c835` | 일치 |
| `all-in-one/registers/virtual-plc-test-results.json` | `a6b389f797f9a8b5ffe6928b8420f55c4cc459a327b0b48d716079d2eca6dd64` | 일치 |
| `all-in-one/sources/Electrical_Can_Decoating_20241118.pdf` | `3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd` | 일치 |
| `all-in-one/sources/Electrical_Rev2.pdf` | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` | 일치 |
| `all-in-one/sources/PID_1684n002I.pdf` | `2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b` | 일치 |
| `all-in-one/sources/decoded-original/0019-FlgNet.xml` | `a3301f4d07c2d36aefa6faa6c3559a1cff4565fc6de40cd17e54b548b30c0ce5` | 일치 |
| `all-in-one/sources/decoded-original/0024-FlgNet.xml` | `a463981da8db46dd7eeb44e592d38807704886d597e728bb652dba4c12cc8f67` | 일치 |
| `all-in-one/sources/decoded-original/0030-FlgNet.xml` | `9252c9da764993de1edb8b2e44c46d6e9f9d4b6118e751a0dbeaa9ffd8ea721b` | 일치 |
| `all-in-one/sources/decoded-original/0031-FlgNet.xml` | `76385eab8f8f72b9faa16f7cf8905f395591b18c0a9ee9e6d7dd085a38c45c65` | 일치 |
| `all-in-one/sources/decoded-original/0067-IdentXmlPart.xml` | `0aa469d4f7a20bde2a5bccc6c91b3d9c48929460bd68ef32e0217d53f4d68628` | 일치 |
| `all-in-one/sources/decoded-original/0068-IdentXmlPart.xml` | `0a71d492e69760390b99f71a75f02ef684e271554b003d5de8bf64a26c64eeba` | 일치 |
| `all-in-one/sources/decoded-original/0164-FlgNet.xml` | `15884b2b362842279b626b669a484b1daa269f5ecd99112b8391bb0387382491` | 일치 |
| `all-in-one/sources/decoded-original/0165-FlgNet.xml` | `4513a5f6e77717c99c5e869105483be31f7f62ab280e271dc36cd7a2d3e3bb88` | 일치 |
| `all-in-one/sources/decoded-original/0166-FlgNet.xml` | `0330a505877be92172f94bce83222a0bfc8d64aab700a69fc1fa2188010d3853` | 일치 |
| `all-in-one/sources/decoded-original/0258-FlgNet.xml` | `d585f05c02cf6d0579ece6f4081e9c52a3135fd8c4720f915f0dfdc0d510ac9b` | 일치 |
| `all-in-one/sources/decoded-original/0264-FlgNet.xml` | `9af15015b447731255eff81680aa71321fb4d0ebe2c28904f442146538ff030d` | 일치 |
| `all-in-one/sources/decoded-original/0265-FlgNet.xml` | `f2471b6ab6169e4c082983ea2080a383cf8b13cba4503a9a07f83d0956fbf08a` | 일치 |
| `all-in-one/sources/decoded-original/0266-FlgNet.xml` | `f11ba1455884c2b0a1085f1892445a86325760be78cd8c9cd70f8ede77f9a992` | 일치 |
| `all-in-one/sources/decoded-original/0327-FlgNet.xml` | `ee431cdc1e4e1708d37b58c1c2df1c3e0bba13f45fea4c1c41f35f158df35769` | 일치 |
| `all-in-one/sources/decoded-original/0340-FlgNet.xml` | `00acb073128337e7d7b95bbedeb50cd0e72c89772d835bdf392da17b3e2d0add` | 일치 |
| `all-in-one/sources/decoded-original/0341-FlgNet.xml` | `e9921cb52ecba4ef1df14758d29e4091fc510a8e792130e855b869dbab4a1c96` | 일치 |
| `all-in-one/sources/decoded-original/0382-FlgNet.xml` | `cbd9118996006b8199d27778d150c5e842162a4845bbb92902afb8667335cd86` | 일치 |
| `all-in-one/sources/decoded-original/0397-FlgNet.xml` | `bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834` | 일치 |
| `all-in-one/sources/decoded-original/0444-FlgNet.xml` | `718076435066a62dc890a414988dc00824025a94d5757799a519071fb69b694c` | 일치 |
| `all-in-one/sources/decoded-original/0549-FlgNet.xml` | `49f7169c33ed7f54559b0801e21a7d618584900972840e91cf51ad032e8febb1` | 일치 |
| `all-in-one/sources/decoded-original/0575-IdentXmlPart.xml` | `40e7b2caf89ab7f1ed9075547a7728bd02441e24451bdd8bf97c843637daad06` | 일치 |
| `all-in-one/sources/decoded-original/0576-IdentXmlPart.xml` | `c8b5f9b9ead0e124f1f817b49d89611ed7b2ce04ecd91ddaa139f2ec89d48dbe` | 일치 |
| `all-in-one/sources/decoded-original/0577-IdentXmlPart.xml` | `511e01fae619dc385357908a1ac62030dbdfd5f5399bd4c22bc58bebbfc3bf47` | 일치 |
| `all-in-one/sources/decoded-original/0578-IdentXmlPart.xml` | `0f9f41b5dee25ea17c7a29ab6f7b00503c13d0f265266acd660072baf061d32b` | 일치 |
| `all-in-one/sources/decoded-original/0602-IdentXmlPart.xml` | `46ab21151eddaaf616469db520730c60423eb742aa491af194e6710c751b4caf` | 일치 |
| `all-in-one/sources/decoded-original/0603-IdentXmlPart.xml` | `e93969dfa281d75b49b24127793068e33472dadb19729c1c48fc4a8dad075ef8` | 일치 |
| `all-in-one/sources/decoded-original/0604-IdentXmlPart.xml` | `b798d29c5499b5314a1ee3cff9139dae64c887533b86baa43b6e9a052373a6af` | 일치 |
| `all-in-one/sources/decoded-original/0605-IdentXmlPart.xml` | `0ff6e2228dbfbc9f657359fe1055083ce621365084ea24c4160e4969b3eaac8b` | 일치 |
| `all-in-one/sources/decoded-original/0606-IdentXmlPart.xml` | `73d45f9e2a34bba8a25df1ed1f71e8f6404fc96a8d6481672652a48435b6a740` | 일치 |
| `all-in-one/sources/decoded-original/0613-IdentXmlPart.xml` | `09d3b1397a987898334218f37e025661af162438582e649f671e7abec443d3cb` | 일치 |
| `all-in-one/sources/decoded-original/0614-IdentXmlPart.xml` | `c6de26f74d75f5be858a406de75eaf6faf62ba9b89c8f9a085b5dd206e93d294` | 일치 |
| `all-in-one/sources/decoded-original/0615-IdentXmlPart.xml` | `80f4544edca56c6e6bb2713c758c92ade9202255110074931e03fe34d0d0801a` | 일치 |
| `all-in-one/sources/decoded-original/0616-IdentXmlPart.xml` | `650b53354a0c8443d94adc5bd6a860d3c5313014a52e0fb98a5656a65b58cc0d` | 일치 |
| `all-in-one/sources/decoded-original/0623-IdentXmlPart.xml` | `4acd00406ea92466169e57e59fc90b0da4d9ec55fd19e2e96c9556e939cb83a6` | 일치 |
| `all-in-one/sources/decoded-original/0624-IdentXmlPart.xml` | `24607c0827fbde428bccf8637ef4ae490798a69a7c2f3b87861d0749082d367a` | 일치 |
| `all-in-one/sources/decoded-original/0626-IdentXmlPart.xml` | `a9d7fbea345eca70325a8c2e44058c23e96add1b7207eabbb09445118b18188b` | 일치 |
| `all-in-one/sources/decoded-original/0627-IdentXmlPart.xml` | `08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb` | 일치 |
| `all-in-one/sources/decoded-original/0628-IdentXmlPart.xml` | `9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd` | 일치 |
| `all-in-one/sources/decoded-original/0629-IdentXmlPart.xml` | `67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972` | 일치 |
| `all-in-one/sources/decoded-original/0635-IdentXmlPart.xml` | `1a057d686446a3fdab7ac61bb09bc543c52f49646c9ca71ac323c10fcdffe457` | 일치 |
| `all-in-one/sources/decoded-original/0652-IdentXmlPart.xml` | `251bb1b3ce1bdf3686545062e5803152779de8a4961539d30e6951a2a10ab692` | 일치 |
| `all-in-one/sources/decoded-original/0655-IdentXmlPart.xml` | `38e9f323024fba19582b473f39b1ed03ffe6a0b390218894029a6edb0b1ff9fb` | 일치 |
| `all-in-one/sources/decoded-original/0656-IdentXmlPart.xml` | `0dbc45e84732a8848f17b094ea08ab8578dbf240bfe15cd7086859395c27c592` | 일치 |
| `all-in-one/sources/decoded-original/0657-IdentXmlPart.xml` | `0f70cda60a6b1a17175876d58e25b2686952642de6cffb21213aeef8b347a22b` | 일치 |
| `all-in-one/sources/decoded-original/0658-IdentXmlPart.xml` | `998294c0c8a99e00ceb33c2c60def2cd4850e34328917ae506244c2be2df3831` | 일치 |
| `all-in-one/sources/decoded-original/0688-IdentXmlPart.xml` | `ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda` | 일치 |
| `all-in-one/sources/decoded-original/0692-IdentXmlPart.xml` | `bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037` | 일치 |
| `all-in-one/sources/decoded-original/0694-IdentXmlPart.xml` | `757ccebdf32d0a168dd787bfa735fe6494eac4c4a9f7a5adc63898a88e8b152d` | 일치 |
| `all-in-one/sources/decoded-original/network-map.json` | `c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60` | 일치 |
| `all-in-one/sources/hmi_plc_tags.csv` | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` | 일치 |
| `all-in-one/sources/live_index.json` | `14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1` | 일치 |
| `all-in-one/sources/source-manifest.json` | `5af6e85994536897fd92f75972534a691e6eb0f067aafe07679c0788fd84e5bf` | 일치 |
| `docs/equipment-standard/INVENTORY.json` | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` | 일치 |
| `docs/equipment-standard/WORK-ITEM-TEMPLATE.md` | `4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586` | 일치 |
| `docs/equipment-standard/WORK-STANDARD.md` | `05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99` | 일치 |


### 전달 전 핵심 근거 제한 대조
2026-10-11 원본0266/0444/0327의 Part/Wire 연결을 다시 추출·대조하고 FG61/PDF62 실제 렌더의 구동·응답 끝점을 재확인했다. 인용 원본70개의 SHA256 재계산도 일치했다. 전체 XML 의미검토나 현재 CPU/현장/통합/게시 검증을 뜻하지 않는다.
