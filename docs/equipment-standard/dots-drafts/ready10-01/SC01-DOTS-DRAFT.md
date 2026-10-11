# SC01 사이클론 분진 스크루 원본 조사 초안

SC01은 CY02·CY04·CY05 하부 분진을 VR03 쪽으로 이송하는 스크루이며, 전기 원본에는 M28과 53KM1 직접기동 회로가 있다. PLC 원본은 SC01 고장 또는 VR03 처리 운전응답 부재로 운전 요청을 Reset하고, 출력 명령 뒤 SC01 처리 피드백이 없으면 2초 S5 타이머로 고장을 Set한다. **요청, 실제 출력, 접촉기 응답, 처리 피드백, HMI 표시는 서로 다른 관찰 지점**이다.

이 문서는 원본 조사와 후속 독립 검토용이다. 실제 매뉴얼 통합·게시·UI/기록 기능 완료나 현장 복구 완료를 뜻하지 않는다. 시뮬레이터 작성·수정·생성·실행·행동 시험, PLC/보호값/SEJIN 운영자료 변경은 하지 않았다.

## 작업 기준과 보존

- 표준: GME-STD-1.0.0, `WORK-STANDARD.md` 및 `WORK-ITEM-TEMPLATE.md`의 7영역 적용.
- 대상: catalog_id `SC01`, 우선 priority_key 없음, motor, 집진·석회, parent_id 없음, depth 0. 별칭 `sc-1`.
- 고정 읽기 원본: `source-mv06`, Git `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, 프로그램 v1.12.0. 작업 시작 시 Git 변경 없음.
- 작업 구분: 작업3번 첫 5개 중 SC01 cloud 독립 조사. 기존 대장에서는 phase2 후보지만, 이번 범위는 조사 초안만이며 로컬 phase2 133 통합·게시를 시작하지 않는다.
- 대장 검증: 읽기 전용 preflight 종료 0, `inventory_matches=true`. 전체248, 우선23, 우선 대응18, 제외90, 제외 부모 하위 보류7, phase2 133을 그대로 유지한다. SC01은 우선18과 중복되지 않고 제외/보류에도 속하지 않는다.
- preflight의 `source_byte_changes`는 `requirements-audit.json`, `all-in-one-data.json` 두 파일이다. 대장 필드/ID/분할 불일치는 없으며, 표준 생성 당시 해시와 현 v1.12.0 바이트가 다르다는 뜻이다. 이 조사에서 기존 대장이나 그 해시를 갱신하지 않았다.
- 작성자: SC01 독립 조사 작업자. 실제 실행 모델명·추론 수준의 런타임 확인 근거는 미확인. 조사일 2026-10-11 UTC. 핵심 근거 최종 문서 검토 완료; 사용자 독립 검토 대기.
- 작성 범위: `drafts/SC01-DOTS-DRAFT.md`, `extracts/SC01/`만. 공유 helper/선언 JSON, 원본 저장소, 공통 코드·버전·운영기록 편집 없음.
- 핵심 원본 SHA-256은 부록에 기록한다. 원본 위치는 이하 별도 설명이 없으면 고정 저장소의 `all-in-one/` 기준이다.

## 7영역 적용표

| 영역 | 상태 | 이 문서의 근거 | 남은 범위 |
|---|---|---|---|
| 설비·자료 기준 | 적용 | SC01/M28, CY02·04·05/VR03 경계, 자료 시점 | 명판·현장 배치·개정 동일성 |
| I/O·HMI | 적용, 일부 근거 미확보 | I4.4/Q3.4, DB13/DB2/DB3, HMI3행, HMI 호출핀 | HMI 이벤트·미해석 ORef4개·현행 주소 |
| 제어 구조 | 적용 | LAD1956/1803/1843/1844/1070, 호출/ENO, 시간 계수 | 실제 TIA 실행순서·현재 CPU·재시작 상태 |
| 전기 전달 경로 | 적용 | FG53/120/139, PDF54/121/140, 케이블1_22, BOM | 현장 단자·배선·실물 접점·설정·명판 |
| 알람·복구 | 적용 | SC_01_FAULT Set/Reset, 2초, FN04 공유 예고장 경계 | 실제 표시·정지·수동 재요청·복구 이력 |
| 증상별 수리 | 적용, 관찰 계획 | 명령/출력/접촉기/원시/처리/HMI 비교 | 실제 관찰·조치·복구 자료 없음 |
| 완료 기준 | 적용 | 독립 상태표·확인자료·후속 검토 항목 | 구현/UI/기록/게시/TIA/현장 모두 별도 |

## 1 설비와 자료의 소유 경계

1. `registers/equipment.json` SC01행은 사이클론 분진 스크루, motor, FG53, parent 빈값이다. P&ID p1 원본 렌더에서 CY-02·CY-04·CY-05가 SC-01로 합류하고 스크루 출구 쪽에 VR-03/M37이 그려져 있다. SC01/M28은 3 kW 440 V, VR03/M37은 0.55 kW 440 V 표기다. 설비 동일성의 문서 근거이며 현재 설치 전압/전력을 측정한 결과가 아니다.
2. `Electrical_Rev2.pdf` FG53/PDF54는 `DUST SCREW SC-1`, M28 `SC-01`, 3 kW/5.8 A를 표기한다. 상단 3상선은 440 V 60 Hz다. SC01 전용 인버터·속도 설정·아날로그 전류·엔코더는 확인한 직접 회로와 태그 목록에서 식별되지 않았다. 이 문서의 직접기동 경로에는 해당 제어가 비해당이며, 현장에 그러한 장비가 전혀 없다는 단정은 하지 않는다.
3. VR03 운전응답은 SC01의 정지 조건에 사용되지만 VR03 모터/고장을 SC01 소유로 병합하지 않는다. CY02/04/05 본체에도 SC01의 출력·알람을 신규 배정하지 않는다. 우선 P14의 ‘2사이클론’ 실물 식별 문제를 이 P&ID만으로 해결하지 않는다.
4. FN04 예고장은 SC01·VR03·SC10·VR04·SC11·VR05의 처리 응답을 함께 읽는다. 공유 타이머 90분은 SC01의 고장 지연 2초와 다른 기능이다.
5. 시공도 `DUS1TB1`의 LOC가 SC01이어도 ZS.O/C·PV14·TC09 케이블 경유 위치인 경우가 있다. 위치 이름을 근거로 SC01 모터 센서로 소유를 바꾸지 않는다.
6. 자료 시점: P&ID 1684n002 판 I p1의 2013년 자료와 전기 시트의 27.05.2024 기본 날짜, FG120/139의 Rev2 17.03.2025 표시를 구분한다. 시공도는 24.11.11 `first draft design`, CHECKED/APPROVED 공란이며 승인 준공도라고 쓰지 않는다. PLC 백업 파일명과 현재 CPU 동일성은 확인하지 않았다.

## 2 I O 및 HMI

### 2.1 직접 신호와 처리 메모리

| 신호 | 형식·주소 | 원본 근거 | 해석과 한계 |
|---|---|---|---|
| `SC01_Fbk` | Bool, `%I4.4` | `live_index.json` doc508; `0613-IdentXmlPart.xml` SimpleAccess RID212, NID35/UID1936, Input AO36 | 물리 입력. 회로상 53KM1 보조접점 응답이며 실제 축 회전/분진 이송 센서는 아님 |
| `Start SC01` | Bool, `%Q3.4` | doc1318; `0602-IdentXmlPart.xml` RID137, NID27/UID806 AK Write, Output AO28; `0658` RID102 NID25/UID864 | 출력 Coil. 설명에 남은 `a 49.3`은 과거 주석, 실제 Address와 FG139/53은 A3.4 |
| `Flag.M_SC_01` | Bool, DB2.DBX1.6 | `0604` RID136, AO14/BO14; `0603` DepDBBlock Flag TOD N2; `0577` RID23 | 자동 Set·고장/허가상실 Reset·HMI 요청주소 후보가 만나는 운전 요청. 실제 출력과 분리 |
| `Allarm.SC_01_FAULT` | Bool, DB3.DBX1.6 | `0657` RID105, AO14/BO14, NID25 UID869/871/872; `0603` Allarm TOD N3 | Set/Reset 유지 고장 비트. HMI DB11 상태주소와 다름 |
| `Inputs.FEEDBACKMOTOR SC-01` | Bool, DB13.DBX4.4 | `0657` RID292 BO36/AO36; `0603/0628` Inputs TOD N13; `0604` RID253 | 처리 응답. 원시 I4.4와 주소영역·쓰기 경로를 분리 |
| `Inputs.VR03 Run` | Bool, DB13.DBX5.4 | `0604` RID219 BO44, NID27 UID23 | SC01 Reset 조건에 쓰이는 별도 VR03 처리 응답 |
| `Tag_68` | Timer, `%T72` | doc1317; `0658` RID103 NID25 UID866 Write/867 Read, Timer AO72 | SC01 2초 고장 감시 타이머. HMI 태그가 아님 |
| `ON` | Bool, `%M0.0` | doc1556; `0602` RID1 NID27 UID800 | 원문에 접점으로 존재. 이름만으로 항상 TRUE라고 전제하지 않음 |
| `UNDER TESTING` | Bool, `%M5.5` | doc1906; `0602` RID4 NID27 UID803 | VR03 Run 부재 Reset 분기에만 부정 접점. 임의 변경/우회 금지 |
| `hours motors.SC_01_MIN` / `SC_01_HOUR` | Int, DB9.DBW136 / DB9.DBW138 | `0615` RID214 BO1088 / RID216 BO1104; `0614` hours motors TOD N9 | 문서상 시간 관련 저장부. HOUR에는 Add가 아닌 Move1이 있어 누적시간 확정 금지 |

DB 주소는 원본 선언의 DB 번호(TOD N)와 비트 오프셋(BO/AO)을 대조한 정적 대응이다. 현재 CPU에서의 값·유효성·최적화 여부를 검증하지 않았다.

### 2.2 원시 입력에서 처리 응답으로 가는 경로

- LAD1070 `0397-FlgNet.xml`: Part35 `Move`, 입력 ORef36/RID10 `Tag_180`, 출력 ORef37/RID11. Wire39가 입력 `in`, Wire40이 `out1`이다.
- `0627-IdentXmlPart.xml` RID10은 Word/Input AO32(비트 기준), NID1/UID36. doc1591의 `Tag_180=%IW4`와 맞는다.
- `0629-IdentXmlPart.xml` RID11은 Word, SSD AO32, BAD BIRID4. `0628` BIRID4의 DepDBBlock은 Inputs/DB13이므로 출력은 DB13.DBW4다. 해당 워드의 I4.4→DB13.DBX4.4가 SC01 처리 응답에 대응한다.
- Part35는 Part27.eno(Wire41), Part27은 Part22.eno(Wire34)를 통해 허가된다. Part22/27/35 모두 `DisableENO="true"`를 포함한다. 이 속성과 실제 TIA ENO 해석은 미검증이며, 선행 블록 및 호출이 유효하다는 전제 없이 ‘항상 복사’라고 쓰지 않는다.
- main LAD1613 `0030-FlgNet.xml`: CRef21 Recipes Handler → CRef23 HMI → CRef25 HMI Output의 ENO 연쇄 뒤, Part37의 `NOT Simulation(1)`을 통해 CRef28 HMI Inputs가 호출된다. Wire31/32/33/42/44/43, CodeBlock UID24/29와 `0688-IdentXmlPart.xml` RID124/135, `0692` RID140 NID19 UID45가 근거다.
- 다른 명칭 일치 자료에 simulation 블록 LAD1084의 처리 응답 Writer가 남아 있다. **기존 자료에 기록된 다른 Writer의 존재만 주의사항으로 보존**한다. 이 조사에서는 시뮬레이터를 작성·수정·생성·실행하거나 행동 시험하지 않았다. 현행 호출/다른 Writer의 활성 여부는 판단하지 않는다.

### 2.3 HMI 태그와 실제 호출핀 경계

`sources/hmi_plc_tags.csv`에서 SC01 직접 태그는 다음 3행이다. Access Name은 모두 PLC이며, 파일 자체가 `dde.cfg 설정; 온라인 현재값 아님`으로 명시한다.

| CSV 행 | 이름 | 설정 주소 | 내부 ID | 확정 범위 |
|---|---|---|---|---|
| 123 | `SC_01\Allarme1` | DB11,X44.1 | 00342 | HMI 설정행 존재 |
| 410 | `SC_01\RispostaA` | DB11,X44.0 | 001C1 | HMI 설정행 존재 |
| 445 | `SC_01\Flag` | DB2,X1.6 | 00199 | 요청 비트 주소와 일치 |

LAD1199 `0376-FlgNet.xml`, 제목 sc1은 CRef22/RID638 → CodeBlock23/RID1이다. `0623-IdentXmlPart.xml`에는 HMI Standard Motors 호출이, `0624`에는 같은 CRef의 호출 선언이 있다. 하지만 이 네트워크의 4개 데이터 ORef는 동일 UID/RID/해당 NID에 이름이 결속된 선언을 확보하지 못했다.

| Wire | 연결 | 상태 |
|---|---|---|
| 21 | Powerrail→CRef22.en | 원본 연결 확인 |
| 37 | ORef24/RID670→Ingresso_run | 검색 문자열은 Inputs.FEEDBACKMOTOR SC-01 후보, 선언 결속 미확보 |
| 39 | ORef26/RID292→Allarme1 | 검색 문자열은 Allarm.SC_01_FAULT 후보, 선언 결속 미확보 |
| 40/41/42/43 | ORef27/28/29/30 RID48→Allarme2/3/4/5 | `0626` FALSE 선언과 관련 호출기록 존재. 개별 원 네트워크 NID 확정은 별도 |
| 46 | Risposta→ORef33/RID295 | 검색 문자열 Motors.sc1.risposta 후보, 선언 결속 미확보 |
| 48 | Comulativo_allarmi→ORef35/RID297 | 검색 문자열 Motors.sc1.allarme_comulativo 후보, 선언 결속 미확보 |

원본 검색 doc1199와 XML의 위치·순서는 위 후보와 부합하지만, RID만 같다는 이유로 다른 블록 선언을 가져오지 않는다. HMI `Allarme1`이라는 이름을 DB3 고장 비트의 직접 주소로 바꾸거나 DB11,X44.1이 어떤 처리 출력인지 확정하지 않는다. HMI 버튼 이벤트, 누름/놓음, 토글·쓰기 권한, 실제 창 객체·스크립트, 고장 팝업/알람 목록은 추가 자료가 필요하다. DB2,X1.6 주소 일치는 HMI 버튼의 쓰기 동작까지 증명하지 않는다.

## 3 제어 구조와 원본 논리

### 3.1 운전 요청 Reset과 출력

LAD1956 `0258-FlgNet.xml`의 NID27 원본 경로:

- Part819(ON) → Part821(SC_01_FAULT) → OR790.in1.
- Part819(ON) → Part22(`NOT Inputs.VR03 Run`) → Part825(`NOT UNDER TESTING`) → OR790.in2.
- OR790.out → RCoil795.in → ORef804/RID136 `Flag.M_SC_01`.
- 별도 Part819(ON) → Part827(M_SC_01) → Coil799 → ORef806/RID137 `Start SC01`.

따라서 정적식은 다음과 같다.

- 요청 Reset 조건: `(ON ∧ SC_01_FAULT) ∨ (ON ∧ ¬VR03_Run ∧ ¬UNDER_TESTING)`.
- 출력 Coil 조건: `ON ∧ M_SC_01`.

주요 Wire: 820 공통 분기, 822 OR in1, 24/826 두 부정 접점 연쇄/OR in2, 812 Reset 입력, 814 Reset 피연산자, 815 요청 접점 피연산자, 828 출력 입력, 817 출력 피연산자. 선언: `0602` ON RID1/UID800, UNDER TESTING RID4/UID803, Start RID137/UID806; `0604` 고장 RID134/UID801, VR03 RID219/UID23, 요청 RID136/UID804·805.

`UNDER TESTING`은 자체 고장 분기를 면제하지 않는다. VR03 Run 조건을 출력 Coil 앞에 별도 직렬 접점처럼 다시 그려서도 안 된다. Reset 동작과 출력 쓰기의 관계는 원본 순서와 함께 보존하되, 실제 스캔 결과·다른 쓰기 우선순위를 정적 선만으로 완결하지 않는다. 이 네트워크만으로 안전회로 전체가 완성됐다고 판단하지 않는다.

### 3.2 자동 Set 두 경로

| LAD/원본 | 대상 | 실제 조건과 고유 UID |
|---|---|---|
| 1843 / `0164-FlgNet.xml`, NID3 | SCoil432 → ORef603/RID23 M_SC_01 | ON(785) ∧ NOT Emergency_module_fault(22) ∧ Tipo_preset=1(Eq400) ∧ Auto_ON1(823) ∧ Tempo_presetting=5(Eq428) |
| 1844 / `0165-FlgNet.xml`, NID4 | SCoil769 → ORef947/RID23 M_SC_01 | ON(1145) ∧ NOT Emergency_module_fault(1154) ∧ Auto_ON1(1147) ∧ Tipo_preset=2(Eq737) ∧ Tempo_presetting=6(Eq765) |

- 1843의 Wire686/687은 Eq428의 데이터/상수5, Wire688은 SC01/SC10/SC11 병렬 Set 입력, Wire689는 SC01만의 대상이다. 상수는 `0578` RID22, NID3/UID602, 값5. SC10/11을 SC01 소유로 복제하지 않는다.
- 1844의 Wire1035/1036은 Eq765의 데이터/상수6, Wire1037은 세 Set 입력, Wire1038은 SC01 대상이다. 상수는 `0578` RID79, NID4/UID946, 값6.
- 선언 `0577` RID23이 두 SC01 쓰기 NID3/UID603, NID4/UID947를 AK Write로 명시한다. 자동 Set2개와 LAD1956 Reset1개를 함께 검토해야 한다.
- LAD1841 `0162-FlgNet.xml`은 ON∧Auto_ON1에서 Part59 Add로 Tempo_presetting에1을 더하고, ON∧NOT Auto_ON1에서 Part66 Move0으로 초기화한다. LAD1723 `0024-FlgNet.xml`은 ON 접점188→CRef183.en, CodeBlock186/RID39 Auto start motors (`0067` 선언), cyclic interrupt 제목은 `cyclic interrupt 1 second`(doc1716)이다. 5/6은 비교 카운트이며, 이 문서가 현재 CPU에서 실제 5초/6초 지연을 계측한 것은 아니다.

### 3.3 호출과 여러 쓰기

- main LAD1619 `0031-FlgNet.xml`은 ON 아래 Allarms1을 호출한다. CRef264/CodeBlock275/RID58, `0688` NID6 UID275.
- main LAD1620 `0549-FlgNet.xml`은 ON Part350.out/Wire351을 Motors1 CRef319.en 및 time work motor CRef334.en 등으로 분기한다. CodeBlock337/RID67, 347/RID82, `0688` NID7 선언을 대조했다.
- main의 네트워크 나열은 HMI/입력전달→알람→모터/시간 순서의 정적 자료다. 별도 cyclic interrupt의 자동 요청 Set, HMI 쓰기, 스캔 중단, 전원 복귀, DB 유지속성을 확인하지 않았으므로 최종 쓰기·재기동 우선순위를 확정하지 않는다.
- 현재 단순 직접 신호 목록만으로는 aggregate DB/워드 쓰기 또는 외부 HMI 쓰기를 모두 배제할 수 없다. 현재 프로젝트 교차참조가 후속 검토 자료다.

### 3.4 운전시간 기록의 특이점

LAD1033 `0321-FlgNet.xml`, NID35:

1. Part1964 Tag_47와 Part1966 **원시 SC01_Fbk**가 직렬이며 Wire1967이 Add1918.en과 Ge1925.pre로 분기한다. 고장 감시의 처리 응답과 읽는 원천이 다르다.
2. Add1918: MIN(ORef1937/RID214)+1(ORef1938/RID7)→MIN(ORef1939). Wire1949/1950/1951.
3. Ge1925: MIN(ORef1940)>=60(ORef1941/RID8), Wire1952/1953. out/Wire1954→Move1928.en.
4. Move1928의 **입력은1**(ORef1942, `0616` RID7 CB V1), 출력은 HOUR(ORef1943/RID216), Wire1956/1957. HOUR+=1 연산이 아니다.
5. Move1928.eno/Wire1958→Move1931로 MIN=0(ORef1944/RID12→1945/RID214). 이어 eno/Wire1961→SCoil1934, Flag_Aggiorna_DB ORef1946.
6. LAD1051 `0338-FlgNet.xml`: SC01 HOUR는 Move2958.out1→ORef2971/RID216, 입력0=ORef2970. 직전 Move2955.eno/Wire2984가 허가다. 선행 Move2946은 Tag_48 접점2987 아래 있고 여러 설비 HOUR 초기화를 연쇄한다.
7. Tag_47 `%T13`의 LAD1056 `0019-FlgNet.xml`은 부정 접점3120→SdCoil3112, value ORef3114/RID335 `S5T#1M`이다. HOUR를 실제 누적 운전시간으로 신뢰하기 전, Move1의 목적·수집/누적 수신부·초기화 정책을 별도 확인해야 한다.

이상해 보이는 Move1을 Add1로 ‘정정’하지 않았다. 기존 원본과 자료를 그대로 보존한다.

## 4 전기 전달 경로

### 4.1 시트와 실제 PDF 페이지

| 도면 | 실제 PDF 페이지 | 시각 확인 내용 |
|---|---:|---|
| Electrical Rev2 FG53 | 54 | DUST SCREW SC-1, M28, 전력·명령·응답3경로. 기본 날짜27.05.2024, 개별 Rev 표시 없음 |
| FG120 | 121 | E4.4, CPU515/MOD9/단자5, 53/6 참조. Rev2 17.03.2025 |
| FG139 | 140 | A3.4, CPU515/MOD14/단자35, 53/4 참조. Rev2 17.03.2025 |
| FG252 | 255 | 53KM1·53QM1 BOM 시작. 날짜27.05.2024 |
| FG253 | 256 | 53QM1 BOM 이어짐. 날짜27.05.2024 |
| Can Decoating CANDC-CONS-E018-035 | 35/64 | DUST ZONE01, M28 RC 경로, DUS1TB1 경유선과 삭제 표시 |
| CANDC-CONS-C001-051 | 51/64 | 전력 케이블1_22, CR→SC01/M28 |
| CANDC-CONS-C010-060 | 60/64 | 10_4/10_5 경유선, 10_6 검은 띠, PV14/TC09 경로 |
| P&ID 1684n002 판 I | 1 | CY02/04/05→SC01/M28→VR03/M37 |

FG252가 PDF255인 것처럼 전 문서에 고정 +1 오프셋을 적용하지 않는다. 위 페이지는 각각 원본 렌더의 우측 하단 표제를 확인했다.

### 4.2 전력 경로

FG53/PDF54: 8.3L1/L2/L3(이전52/9, 다음54/0) → 53QM1 주접점1–2/3–4/5–6 → 53KM1 주접점1–2/3–4/5–6 → 53U1/V1/W1, XM의 같은 선명 → 53QS1 주접점1–2/3–4/5–6 → M28 U/V/W 및 PE → SC01 스크루.

- 도면의 패널 배선 표기: BLACK FS17 1.5 mm².
- 53QM1 `5.5–8 A`는 도면상 보호기 범위 표기다. M28 `5.8 A` 표기나 범위 상한을 실제 트립 설정으로 지시하지 않는다.
- 시공 PDF51 행1_22: `=DUS+SC01-M28A`, FROM CR, TO SC-01/M28, DUST SCREW, GAC, CV 4심 1.5, spare0, 경로100→200→210→211 RC→E100, Adjustment3, LEN110. LEN의 현장 실측 및 단위 확정은 별도다.
- 시공 PDF35: 경로211 RC, 1/Pipe16, M28, 1_22, CV1.5/4와 맞는다. 단자번호까지 이어지는 준공 단자대/케이블심선표는 확보하지 못했다. CV 외부 케이블과 FS17 내부 배선을 같은 규격으로 합치지 않는다.

### 4.3 출력 명령 경로

PLC 백업 Q3.4 ↔ FG139 A3.4, CPU515/MOD14/출력단자35 → FG53 139/1 참조 → XS43 → 53QS1 보조접점 → XS44 → 선53.1 → 53QM1 보조접점 → 53KM1 코일 A1, A2→−0Vdc10.6.

- FG53의 두 보조접점에는 이 렌더에서 개별 단자번호가 표시되지 않는다. 13/14 같은 번호를 임의 배정하지 않는다.
- FG139은 +24Vdc10.9 분기와 X21 3031의 F5×20 4A F, 모듈 공급단자39, 0V단자40을 표시한다. 이 4A 퓨즈를 SC01 모터 과부하 설정값으로 취급하지 않는다.
- Q3.4가1이어도 53QS1/53QM1 경로 또는 코일 회로의 상태 때문에 53KM1 흡입이 성립하지 않을 수 있다. 정적 회로 경로의 설명이며 현장 정상 극성/동작을 계측한 결론이 아니다.

### 4.4 피드백 경로

FG53 +24Vdc10.7 → 53KM1 보조접점 **13–14** → E4.4, 참조120/5 → FG120 E4.4, CPU515/MOD9/단자5 → PLC `%I4.4` → LAD1070의 IW4→DB13.DBW4 전달 → `Inputs.FEEDBACKMOTOR SC-01` → LAD1803 타이머/고장.

도면상의 개방 접점 그림은 53KM1 상태 접점 표기다. 현재 배선 정상극성이나 NC/NO의 현행 실물 접점을 확정하지 않는다. 모터 접촉기 응답만으로 커플링·감속기·스크루 축·실제 분진 흐름이 정상이라고 판단할 수 없다.

### 4.5 BOM와 장치 실물

- FG252/PDF255의 53KM1: Siemens `3RT2015-1BB41`, CONTACTOR 3 kW, 1L, DC24V, S00 VT; RC element `3RT2916-1CB00`.
- 53QM1은 FG252에 `3RV2901-1E` 보조접점, `3RA1921-1DA00` 결합부가 있고 FG253/PDF256 첫 행에 Wohner WR32433 어댑터와 Siemens `3RV2011-1HA10`, MAGNETOTHERMIC S00 5.5–8A가 이어진다.
- 이는 원본 BOM의 모델만 확인한 것이다. 현행 설치 모델/교체품 호환성/정비 토크/보호 설정/제조사 안전 성능은 명판·현행 제조사 자료 없이 기입하지 않는다. 인접 FN04의 ABB 인버터를 SC01의 장치로 가져오지 않는다.

### 4.6 SC01 위치명 케이블의 소유 상충

- PDF60의 10_4 `=DUS+SC01-DUS1TB1A`: BF-01/JB01→SC-01/DUS1TB1, 설명 ZS.O/C, DC CVV7G1.0 spare2.
- 10_5 `=DUS+SC01-DUS1TB1B`: 같은 양끝, 설명 PV14, AC CVV5G1.0 spare2.
- 이어 10_7/10_8은 SC01/DUS1TB1→PV14/DUS1TB2로 이어진다. 이 위치명이 SC01이라도 신호 기능은 PV14 경유로 보이며 SC01의 E4.4/Q3.4 전용 케이블로 확정할 수 없다.
- 텍스트 층에는 10_6 `=DUS+SC01-DUS1TB1C`/TC09가 남지만 **PDF60 실제 렌더에서 그 행은 검은 띠**다. PDF35에도 DUS1TB1 아래 `Delete / Delete / 0 / 0` 행이 있다. 활성 케이블로 복원하거나 현재 배선을 채워 넣지 않는다. 현재 발행/삭제 이력·원 CAD가 필요하다.
- PDF60의 10_9는 BF01/JB01→PV14/TC09, KX2S1.0 경로를 별도로 기록한다. TC09 소유를 SC01로 변경하지 않는다.

## 5 알람과 복구 경계

### 5.1 SC01 직접 고장

LAD1803 `0438-FlgNet.xml`, NID25:

| 동작 | Part/피연산자 | 정적 조건 | 주요 Wire |
|---|---|---|---|
| 2초 감시 | SdCoil851, Tag_68 ORef866/RID103 | ON887 ∧ Start889 ∧ NOT 처리응답900 | 888/890 분기, 903 반전 응답, 21 timer.in, 875 value, 876 operand |
| Set 고장 | SCoil857, FAULT ORef869/RID105 | ON887 ∧ Start889 ∧ Tag_68 접점891 | 877,22,880 |
| Reset 고장 | RCoil862, FAULT ORef872/RID105 | ON887 ∧ RESET_ALLARM895 ∧ FAULT897 | 882,896,883,898,885 |

상수 ORef865/RID28는 `0656-IdentXmlPart.xml` LiteralConstant, NID25/UID865, S5Time, `SV=S5T_x0023_2S`, `V=512`다. 원문은 **S5T#2S**이며 512를 밀리초로 해석하지 않는다. Tag_68은 `0658` Timer AO72로 `%T72`다. 현행 CPU에서의 실제 만료시간·리텐션·재호출 조건은 확인하지 않았다.

FAULT가 Set되면 LAD1956의 별도 Reset 경로가 운전 요청을 해제하는 연결이 있다. 고장 리셋 식에는 피드백 정상 접점이 없으므로 Reset 완료만으로 결함 해결·운전 허가·재기동 완료를 선언할 수 없다. 원인 해소, 알람 비트, 요청 재설정, 출력, 실제 회전/이송을 각각 확인할 자료가 필요하다.

### 5.2 FN04 공유 예고장에 미치는 영향

LAD1964 `0264-FlgNet.xml`, NID34은 ON1020∧Inputs.FN04 Run1022 아래, SC01 처리응답1024·VR03 Run1026·SC10 처리응답1028·VR04 Run1030·SC11 처리응답1032·VR05 Run1034를 각각 부정한 6분기 OR972다.

- OR972.out/Wire1012→Coil982(`Allarm.Prealarms_FN04`, ORef999), SdCoil985(`Tag_126`, ORef1001), 타이머 접점1036 입력.
- SdCoil985.value ORef1000/RID112: `0606` S5Time `S5T#1H_30M`, CB V13632. Tag_126은 `0602` RID169 Timer AO131, doc122 `%T131`.
- 접점1036(Tag126)→Coil990 local `Stop_Fan_FN04`, ORef1003/RID170, `0605` LocalAccess BO3.
- LAD1965 `0265-FlgNet.xml`에서는 그 local 비트를 Part1042/ORef1019로 읽어 OR1003→RCoil1010, `Flag.M_FN_04` ORef1021로 연결한다.

즉 SC01 처리 응답 부재가 FN04 공유 경고/정지 경로에 기여할 수 있다. 90분 타이머와 FN04 알람을 SC01 전용 항목이나 SC01 실제 복구 확인으로 바꾸지 않는다. 다른 5분기의 어느 하나가 원인일 수 있으므로 SC01 고장이라고 단정하지 않는다.

## 6 증상별 관찰과 수리 판단

아래는 향후 승인된 현장 진단에서 기록해야 할 비교 지점이다. 실제 관찰·조치·시험을 수행한 기록이 아니다. 전기·기계 확인은 자격 있는 담당자가 현장 안전절차와 잠금/표찰·잔류에너지 확인을 적용해야 하며, 문서가 임의 강제출력·안전 우회·보호값 변경을 허용하지 않는다.

| 증상 | 우선 관찰 위치 | 비교 근거와 원인 배제 | 복구 판단에 필요한 자료 |
|---|---|---|---|
| 자동 순서인데 요청이 안 켜짐 | ON, Auto_ON1, Tipo_preset, Tempo_presetting, Emergency_module_fault, M_SC_01 | LAD1843의1/5 또는1844의2/6 분기와 비교. VR03 부재/FAULT에 의한 Reset도 같은 시각 비교 | 현재 프로젝트 교차참조·호출 기록, 요청이 유지되는 근거 |
| 요청이 켜졌다 바로 꺼짐 | M_SC_01, SC_01_FAULT, VR03 처리Run, UNDER TESTING 상태 | LAD1956 두 Reset 분기 중 어느 쪽인지 구분. UNDER TESTING 변경으로 해결하지 않음 | 시간대 포함 추세와 적법한 원인조치, 허가 복귀 |
| Q3.4=1인데 접촉기가 안 붙음 | Q3.4, FG139 단자35, XS43/44, 53QS1/53QM1, 53KM1 A1/A2 | 출력 명령·전달·전원·접점·코일을 분리. PLC 화면의1만으로 전압 공급을 확정하지 않음 | 승인 절차에 따른 단자/전압/접점 검측, 실물 모델·배선 |
| 접촉기는 붙는데 2초 고장 | 53KM1 13–14, E4.4/I4.4, DB13.DBX4.4, Tag68, FAULT | 물리 응답, 입력 채널, 입력 전달 호출·ENO, 다른 Writer를 비교 | 같은 시각 원시/처리 응답과 출력, 배선·호출 원인 배제 |
| HMI 운전/고장 표시만 다름 | HMI DB11,X44.0/.1, DB3.DBX1.6, DB13.DBX4.4, HMI1199 핀 | HMI 미해석 결속/갱신 경로부터 확인. 표시 태그명을 직접 고장주소로 치환하지 않음 | HMI 원 프로젝트/창 이벤트·결속표·통신 상태 |
| 53KM1 응답은 정상인데 분진이 안 나감 | M28/감속기/커플링/스크루/CY02·04·05 출구/VR03 | 접촉기 피드백은 축 회전·이송량을 증명하지 않음. 기계 막힘/연결/VR03 경계 구분 | 안전 정지 후 기계 상태, 승인된 정상 이송 복귀 기록 |
| FN04 공유 예고장 발생 | SC01·VR03·SC10·VR04·SC11·VR05 처리응답 모두 | LAD1964 6분기 중 SC01만의 문제인지 확인. 90분을 SC01 고장타이머로 오인하지 않음 | 분기별 추세·FN04 예고장·타이머/정지 연결 |
| 시간 표시가1에서 반복되거나 0으로 돌아감 | SC_01_MIN/HOUR, Tag47, Tag48, Flag_Aggiorna_DB | LAD1033 Move1 및 LAD1051 ENO 연쇄 Move0를 원문 그대로 비교 | 시간 수집 수신부·누적 정책·리텐션/초기화 설계 |

관찰 1건에는 관찰자, 시각/시간대, 위치, 원시값/단위, 도구, 프로젝트/CPU 근거, 비교 원본, 원인 배제, 승인된 조치, 전후 결과를 각각 기록한다. 관찰 누락을 0이나 정상으로 채우지 않는다. 실제 운영 기록·사진·SEJIN 데이터를 이 초안에 복사하지 않았다.

## 7 기능 적용과 완료 기준

### 네 기능과 기록 보존

| 기능 | 후속 적용 근거 | 이번 구현/검증 |
|---|---|---|
| 도면·래더 나란히 보기 | FG53/PDF54↔LAD1956, FG120/139↔LAD1070/1803, P&ID↔VR03 소유 경계 | 초안의 대응만 제안. UI 구현/링크 강조 검증 안 함 |
| 백업 미리보기·선택 복원 | SC01 고유 키와 기존 미지 필드/다른 설비/초안 보존 필요 | 실행 안 함 |
| 기록 전후 비교 | 명령/원시/처리/HMI/실물 시각별 비교 | 실행 안 함 |
| 관찰 보고서/PDF | 위 관찰필드 및 원본 판본·해시 포함 | 생성/검증 안 함. 원본 PDF 렌더 검토와 다른 상태 |

BC01의 항목 수·알람 수·필드·공통 기록 지원을 SC01의 완료로 복제하지 않는다. 후속 구현이 승인되면 0과 빈칸, 기존 note/repair_observation, 알 수 없는 필드, SC01 외 기록, 초안과 저장 키를 보존해야 한다. 현재 조사만으로 저장·재읽기·재열기나 PC1280/모바일390 검증을 통과했다고 표시하지 않는다.

### 확인해야 할 자료와 판정

1. 현행 PLC 프로젝트/CPU 비교 및 TIA 교차참조: M_SC_01·Start SC01·처리응답·FAULT·HOUR의 모든 Writer, HMI/interrupt 호출, DisableENO 해석, 유지성 확인. **현재 수행 상태는 미수행**이다.
2. HMI 원본 결속/버튼 이벤트: LAD1199 미결속4개와 실제 DB11,X44.0/.1 대응, DB2,X1.6 쓰기 방식 확인. 이름/주소 일부 일치만으로 완료 처리하지 않는다.
3. 현장 명판/승인 도면: M28, 53QM1/KM1/QS1, E4.4/Q3.4 모듈/단자, 케이블1_22 심선, 정상 접점 상태, 실제 보호 설정을 원본과 비교. 기입값을 설정값으로 실행하지 않는다.
4. 시공도 삭제/현행 판본: 10_6 검은 행과 PDF35 Delete의 승인 변경 이력, DUS1TB1 경유선 실제 소유 확인.
5. 실제 복구 증거: 원인해소→알람해제→허가/요청→출력→접촉기→실제 회전·이송을 분리한 현장 기록. HMI 정상 표시만으로 완료하지 않는다.

### 수행 검증과 미수행 범위

- 읽기 전용 Git HEAD/status 확인, 표준/대장 읽기, preflight 종료0.
- 설비 직접 XML 및 선언의 UID/RID/NID·Part/Wire/PinName·상수형식 대조. 선행 ENO/공유 소유/미해석 핀을 그대로 남김.
- 원본 PDF9쪽 실제 렌더 검토: 전기5쪽(54,121,140,255,256), 시공3쪽(35,51,60), P&ID1쪽. P&ID SC01 부분을 추가 확대했다.
- 자체 `extracts/SC01/`에 읽기 전용 추출 스크립트, 원본 참조/트레이스, 렌더, 해시를 저장. 이는 PLC 실행 모델이나 시뮬레이터가 아니다.
- 원본 저장소·공통 helper·선언·버전·대장·운영 기록 변경 없음. 매뉴얼 생성기, npm/build, 시뮬레이터, TIA/CPU/현장 행동시험 실행 없음.
- 원본 재검토는 자체 검토이며 핵심 핀·도면·원본 해시를 최종 재검토했으며 사용자 독립 검토는 별도다. 기존18불일치/1060확인대기/577설계시험 수치를 이번 작업으로 해결·실행 완료로 바꾸지 않는다.

| 상태 | 결과 | 의미 |
|---|---|---|
| documentation | draft_complete_with_gaps | 7영역 조사 초안, 미결속/현장 공백 명시 |
| static_review | source_trace_checked_independent_review_pending | 자체 원본 정적 대조·PDF 검토, 별도 검토 대기 |
| ui_records | not_run | 구현·저장·복원·재열기·보고서 없음 |
| publication | not_published | 원본 repo·로컬 통합·게시 범위 밖 |
| tia_compile | not_performed | 수행 안 함 |
| live_cpu | not_performed | 수행 안 함 |
| field_recovery | not_performed | 수행 안 함 |

## 다음 작업

부모가 SC01 원본 추적을 독립 검토한다. 우선순위는 (1) LAD1956의 VR03 Reset 분기와2초 감시, (2) 입력전달 ENO/호출, (3) HMI 미결속4개, (4) HOUR Move1, (5) DUS1TB1/PV14 소유와 삭제행이다. 새 현장 자료 없이 미확정 부분을 반복 추정하지 않는다. 본 초안의 승인 자체가 SC01 로컬 통합·게시나 PLC/현장 변경 허가는 아니다.

## 부록 원본 SHA256

아래 해시는 고정 `abcf31c5030bc7ef8749ed8e869a857f2387a28a` 읽기 원본의 바이트 해시다. 탐색용 파생 JSON과 decoded XML/선언 및 PDF 원문을 구분해 기록한다. 상세 기계판독 목록은 `extracts/SC01/source-sha256.json`에 있다.

| 원본 경로 | SHA256 |
|---|---|
| `all-in-one/sources/decoded-original/0258-FlgNet.xml` | `d585f05c02cf6d0579ece6f4081e9c52a3135fd8c4720f915f0dfdc0d510ac9b` |
| `all-in-one/sources/decoded-original/0438-FlgNet.xml` | `ddf8f5c94a3c7c5e5134fece797f082aec3da59f8f755d8629d8091e170c1830` |
| `all-in-one/sources/decoded-original/0164-FlgNet.xml` | `15884b2b362842279b626b669a484b1daa269f5ecd99112b8391bb0387382491` |
| `all-in-one/sources/decoded-original/0165-FlgNet.xml` | `4513a5f6e77717c99c5e869105483be31f7f62ab280e271dc36cd7a2d3e3bb88` |
| `all-in-one/sources/decoded-original/0162-FlgNet.xml` | `892eab96a4f5c87cfafd35f8a2e2a04982a93ca23c777312101882e408b11deb` |
| `all-in-one/sources/decoded-original/0321-FlgNet.xml` | `8ebe3a4cfeea89e45286e45d219196561cd426e078d7126ceacb48d8a40f75db` |
| `all-in-one/sources/decoded-original/0338-FlgNet.xml` | `762ab4b1520aa101efc897ff9e4b72a35f5591ff460a0b654dc87919849077a1` |
| `all-in-one/sources/decoded-original/0376-FlgNet.xml` | `a92a4ff0e11221fbb449220d28d65e4c88e9a3329f6bf8e002cb99f3ca879fce` |
| `all-in-one/sources/decoded-original/0264-FlgNet.xml` | `9af15015b447731255eff81680aa71321fb4d0ebe2c28904f442146538ff030d` |
| `all-in-one/sources/decoded-original/0265-FlgNet.xml` | `f2471b6ab6169e4c082983ea2080a383cf8b13cba4503a9a07f83d0956fbf08a` |
| `all-in-one/sources/decoded-original/0397-FlgNet.xml` | `bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834` |
| `all-in-one/sources/decoded-original/0030-FlgNet.xml` | `9252c9da764993de1edb8b2e44c46d6e9f9d4b6118e751a0dbeaa9ffd8ea721b` |
| `all-in-one/sources/decoded-original/0031-FlgNet.xml` | `76385eab8f8f72b9faa16f7cf8905f395591b18c0a9ee9e6d7dd085a38c45c65` |
| `all-in-one/sources/decoded-original/0549-FlgNet.xml` | `49f7169c33ed7f54559b0801e21a7d618584900972840e91cf51ad032e8febb1` |
| `all-in-one/sources/decoded-original/0024-FlgNet.xml` | `a463981da8db46dd7eeb44e592d38807704886d597e728bb652dba4c12cc8f67` |
| `all-in-one/sources/decoded-original/0019-FlgNet.xml` | `a3301f4d07c2d36aefa6faa6c3559a1cff4565fc6de40cd17e54b548b30c0ce5` |
| `all-in-one/sources/decoded-original/0341-FlgNet.xml` | `e9921cb52ecba4ef1df14758d29e4091fc510a8e792130e855b869dbab4a1c96` |
| `all-in-one/sources/decoded-original/0355-FlgNet.xml` | `73592d33f8b3a71effeb36f25427c76e931485e7ce31f5c81f144ddae83c4247` |
| `all-in-one/sources/decoded-original/0067-IdentXmlPart.xml` | `0aa469d4f7a20bde2a5bccc6c91b3d9c48929460bd68ef32e0217d53f4d68628` |
| `all-in-one/sources/decoded-original/0575-IdentXmlPart.xml` | `40e7b2caf89ab7f1ed9075547a7728bd02441e24451bdd8bf97c843637daad06` |
| `all-in-one/sources/decoded-original/0577-IdentXmlPart.xml` | `511e01fae619dc385357908a1ac62030dbdfd5f5399bd4c22bc58bebbfc3bf47` |
| `all-in-one/sources/decoded-original/0578-IdentXmlPart.xml` | `0f9f41b5dee25ea17c7a29ab6f7b00503c13d0f265266acd660072baf061d32b` |
| `all-in-one/sources/decoded-original/0602-IdentXmlPart.xml` | `46ab21151eddaaf616469db520730c60423eb742aa491af194e6710c751b4caf` |
| `all-in-one/sources/decoded-original/0603-IdentXmlPart.xml` | `e93969dfa281d75b49b24127793068e33472dadb19729c1c48fc4a8dad075ef8` |
| `all-in-one/sources/decoded-original/0604-IdentXmlPart.xml` | `b798d29c5499b5314a1ee3cff9139dae64c887533b86baa43b6e9a052373a6af` |
| `all-in-one/sources/decoded-original/0605-IdentXmlPart.xml` | `0ff6e2228dbfbc9f657359fe1055083ce621365084ea24c4160e4969b3eaac8b` |
| `all-in-one/sources/decoded-original/0606-IdentXmlPart.xml` | `73d45f9e2a34bba8a25df1ed1f71e8f6404fc96a8d6481672652a48435b6a740` |
| `all-in-one/sources/decoded-original/0613-IdentXmlPart.xml` | `09d3b1397a987898334218f37e025661af162438582e649f671e7abec443d3cb` |
| `all-in-one/sources/decoded-original/0614-IdentXmlPart.xml` | `c6de26f74d75f5be858a406de75eaf6faf62ba9b89c8f9a085b5dd206e93d294` |
| `all-in-one/sources/decoded-original/0615-IdentXmlPart.xml` | `80f4544edca56c6e6bb2713c758c92ade9202255110074931e03fe34d0d0801a` |
| `all-in-one/sources/decoded-original/0616-IdentXmlPart.xml` | `650b53354a0c8443d94adc5bd6a860d3c5313014a52e0fb98a5656a65b58cc0d` |
| `all-in-one/sources/decoded-original/0621-IdentXmlPart.xml` | `a63e2b97ea9eb2691cb478666afed77fc58a2da2f8170422dc09e24b102c88ee` |
| `all-in-one/sources/decoded-original/0622-IdentXmlPart.xml` | `f0b997f1246d76cff71de2160eb617caa936e6987bdf43c73f55cdcf77dccdb6` |
| `all-in-one/sources/decoded-original/0623-IdentXmlPart.xml` | `4acd00406ea92466169e57e59fc90b0da4d9ec55fd19e2e96c9556e939cb83a6` |
| `all-in-one/sources/decoded-original/0624-IdentXmlPart.xml` | `24607c0827fbde428bccf8637ef4ae490798a69a7c2f3b87861d0749082d367a` |
| `all-in-one/sources/decoded-original/0625-IdentXmlPart.xml` | `17a9f9bd540bf0a54e9973391fa258d81e567248fd201ae4ff32c367359e69f9` |
| `all-in-one/sources/decoded-original/0626-IdentXmlPart.xml` | `a9d7fbea345eca70325a8c2e44058c23e96add1b7207eabbb09445118b18188b` |
| `all-in-one/sources/decoded-original/0627-IdentXmlPart.xml` | `08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb` |
| `all-in-one/sources/decoded-original/0628-IdentXmlPart.xml` | `9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd` |
| `all-in-one/sources/decoded-original/0629-IdentXmlPart.xml` | `67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972` |
| `all-in-one/sources/decoded-original/0635-IdentXmlPart.xml` | `1a057d686446a3fdab7ac61bb09bc543c52f49646c9ca71ac323c10fcdffe457` |
| `all-in-one/sources/decoded-original/0652-IdentXmlPart.xml` | `251bb1b3ce1bdf3686545062e5803152779de8a4961539d30e6951a2a10ab692` |
| `all-in-one/sources/decoded-original/0656-IdentXmlPart.xml` | `0dbc45e84732a8848f17b094ea08ab8578dbf240bfe15cd7086859395c27c592` |
| `all-in-one/sources/decoded-original/0657-IdentXmlPart.xml` | `0f70cda60a6b1a17175876d58e25b2686952642de6cffb21213aeef8b347a22b` |
| `all-in-one/sources/decoded-original/0658-IdentXmlPart.xml` | `998294c0c8a99e00ceb33c2c60def2cd4850e34328917ae506244c2be2df3831` |
| `all-in-one/sources/decoded-original/0688-IdentXmlPart.xml` | `ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda` |
| `all-in-one/sources/decoded-original/0692-IdentXmlPart.xml` | `bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037` |
| `all-in-one/sources/Electrical_Rev2.pdf` | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` |
| `all-in-one/sources/Electrical_Can_Decoating_20241118.pdf` | `3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd` |
| `all-in-one/sources/PID_1684n002I.pdf` | `2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b` |
| `all-in-one/sources/GME_20250506.zap18` | `00c79b6d986e68298f65b172c1807115bc5d9e450a74fcc989d0796d8d8a4ea8` |
| `all-in-one/sources/PEData.plf` | `647de7ea123daced41c27bec8f81aeb93c712cac714d4754d7da5c528abb016a` |
| `all-in-one/sources/live_index.json` | `14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1` |
| `all-in-one/sources/hmi_plc_tags.csv` | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` |
| `all-in-one/sources/decoded-original/network-map.json` | `c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60` |
| `all-in-one/registers/equipment.json` | `7870325dff32bbca90fa34507b301c4aad3347d669fddcd03b910343663996fa` |
| `docs/equipment-standard/INVENTORY.json` | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` |
| `docs/equipment-standard/WORK-STANDARD.md` | `05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99` |
| `docs/equipment-standard/WORK-ITEM-TEMPLATE.md` | `4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586` |
