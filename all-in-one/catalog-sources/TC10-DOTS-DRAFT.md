# TC10 예비 온도 입력 후보 — 고유 원본 7영역 조사 초안

## 핵심 확인·상충·누락과 공유 근거

- 0484 LAD1734 NID4의 호출 EN은 **OFF(M0.1) 정접점**이다. IN0는 별도 ON(M0.0). TC09의 ON 호출·경보·타이머를 복제하지 않는다.
- TC-10은 주변장치 입력 `%IW390:P` Int이며 Data.TC_10 DB1.DBW264와 TC10_OFR DB3.DBX20.5를 각각 출력한다. 전자는 Int 값, 후자는 Bool이다.
- OEM FG171은 실제 PDF172. PEW390/392에 모두 TC-10 SPARE(4–20mA)가 쓰였으나 TC10의 외부 센서/케이블/단자대 연결선은 보이지 않는다. 모듈의 인쇄된 단자표를 실제 연결 배선으로 표현하지 않는다. SPARE는 현재 부재/영구미사용의 증명이 아니다.
- 백업 ZERO_TC10=0, COEFF_TC10=0, TC_10=-9999. 현재 측정·승인된 환산계수·안전값이 아니다. TC09 계수1330이나 경보180/200을 이 채널에 적용하지 않는다.
- HMI 이름검색 결과가 비어도 주소 대조에서는 4개 태그가 확인된다. 실제 위젯·이벤트·ACK·권한·통신 정상은 미확인.
- 선언 원본의 TC10 고유 항목5개 및 대상 주소범위 검색에서 고유 출력 외 별도 읽기·겹친 Word 쓰기는 확보하지 않았다. 간접주소·외부 HMI Writer·현행 CPU 전체 부재를 단정하지 않는다.

공통 재사용: [TC09](TC09-DOTS-DRAFT.md), [TC03](TC03-DOTS-DRAFT.md)에서 같은 고정입력의 Signal linearization 0291/0014와 startup ON/OFF 보충 자료의 성격을 재사용한다. TC10 호출, 선언, HMI 주소, 저장값 배열, FG171 실제 렌더, 상위 FC3 호출핀은 독립 확인했다. TC09의 고유 MAX/MAX_MAX·PV14·FN04·BR01·RD01 관계는 TC10으로 가져오지 않는다.

## 1. 설비·자료 기준

- catalog_id TC10, 별칭 tc_10, sensor/계측, parent 없음/depth0. INVENTORY catalog[20], equipment[84], phase2/planned, specialist/not_assessed. 같은 이름의 다른 TC는 다른 ID이며 실물 동일성 미확인이다.
- 범위는 BATCH09 지시 및 TASK3-BATCH09-SCOPE의 TC10 행. 신규 자체 문서조사이며 로컬 2차133 통합 제외 유지. 문서 초안은 구현·게시 완료 집계가 아니다.
- 읽기전용 원본 `gme-research/source-mv06`, commit `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, v1.12.0. 사용자 보고 최신 게시 상태를 이 고정원본의 CPU 검증으로 바꾸지 않는다.
- AGENTS, rollout 스킬 및 source-map, WORK-STANDARD, WORK-ITEM-TEMPLATE, INVENTORY, VERSION/WORKSPACE-HANDOFF/PUBLICATION_STATUS/ACTIVE-WORK/EXPANSION-WORK 상단을 확인했다. 이번 배치의 최신 조사제한을 따른다.
- 모델 런타임 증명 미확인. 원본/공통코드/대장/버전/배포/운영기록 수정0, 새 Work/Codex 및 재위임0. 시뮬레이터 작성·수정·생성·실행·행동시험0, PLC/현장/보호값/SEJIN 변경0, 원본 build/test/generator 실행0.
- 원본 약칭 0484 등은 `all-in-one/sources/decoded-original/0484-FlgNet.xml`을 뜻한다. 선언 약칭은 같은 폴더의 `번호-IdentXmlPart.xml`. 문서번호/LAD1734와 파일번호/NID4는 서로 다르다.

| 영역 | 상태 | 근거 경계 |
|---|---|---|
| 설비·자료 | 적용 | 백업 예비채널, 현재 실물 미확정 |
| I/O·HMI | 적용/부분 미확보 | 주소·형식 확인, 실제 화면 이벤트 미확보 |
| 제어 | 적용 | OFF 호출, 공통 FC63, 현재 실행 미검증 |
| 전기 끝점 | 일부 적용/미확보 | 모듈 표만 확인, 외부 TC10 끝점 미확보 |
| 알람·복구 | 일부 적용/미확보 | OFR 출력 확인, 전용 고온경보·복구 근거 미확보 |
| 증상 관찰 | 적용 | 읽기전용 관찰계획, 조작/시험 지시 아님 |
| 완료·누락 | 적용 | 문서와 구현/현장 상태 분리 |

## 2. I/O·HMI·백업 저장값

### 선언 결속

SSD.AO는 bit offset이다. 아래 DB번호는0674 DepDBBlock RID8→DB4, RID11→DB1, RID354→DB3의 TOD.N으로 확인했다. 전부 Global이며 공통 FC63 내부 Local 임시변수에 DB주소를 부여하지 않는다.

| 대상 | 형식·주소 | 원본 결속 |
|---|---|---|
| TC-10 원시 | Int IW390:P | 0678 SimpleAccess RID24, AO3120, SAD Input/SAM Peripherie, NID4 UID114 |
| OFF / ON | Bool M0.1 / M0.0 | 0678 RID34/AO1/NID4 UID112, RID1/AO0/NID4 UID113; Memory/SAM None |
| ZERO_TC10 | Int DB4.DBW214 | 0676 RID26, AO1712, NID4 UID116 Read, BAD8 |
| COEFF_TC10 | Int DB4.DBW216 | 0676 RID25, AO1728, NID4 UID115 Read, BAD8 |
| Data.TC_10 | Int DB1.DBW264 | 0676 RID27, AO2112, NID4 UID117 AK Write, BAD11 |
| Allarm.TC10_OFR | Bool DB3.DBX20.5 | 0676 RID361, AO165, NID4 UID23 AK Write, BAD354 |

PIW/주변장치 직접 접근과 프로세스 이미지 IW의 갱신시점을 혼동하지 않는다. 백업 심볼 목록 `%iw390` 표기는0678의 Peripherie 및 network-map의 `tc-10:p`와 함께 읽는다. PEW392의 별도 TC10 환산 호출·센서 결속은 확보하지 않았다. 도면 두 채널을 평균/이중화/두 센서로 단정하지 않는다.

### HMI 설정주소 직접 대조

원본 `all-in-one/sources/hmi_plc_tags.csv`, Access Name 모두 PLC.

| HMI 태그 | 설정주소 | 내부 ID |
|---|---|---|
| data_DB1_DBW264 | DB1,INT264 | 00263 |
| Coeff_DB4_DBW214 | DB4,INT214 | 0020E |
| Coeff_DB4_DBW216 | DB4,INT216 | 001EC |
| Allarmi_203 | DB3,X20.5 | 0026B |

이는 dde.cfg 백업 설정이며 읽기/쓰기 이벤트 또는 표시 위젯의 증거는 아니다. 파생 sensor-measurement의 hmi_reference_rows 빈 배열은 이름기반 탐색 한계로 보완한다. 알람명 Allarmi_203을 PLC 비트번호203이나 확정 경보문장으로 바꾸지 않는다.

### 백업 저장값

`live_index.json` `_7ev/1554`: tc-10, int, %iw390, spare temperature. `_7ev/1604` 이름·형식·값129개 각각 길이일치, index107 ZERO_TC10=0/index108 COEFF_TC10=0. `_7ev/1629` 세 배열162개 길이일치, index132 TC_10=-9999. 형식 모두 Int. 검사는 extracts/TC10/backup-values.json.

이 자료는 백업 저장 내용이다. -9999 하나만으로 현재 단선 또는 경보 발생을 판정하지 않는다. 계수0은 현장 권장 설정이 아니며 실제 실행될 때 정수계산에 미치는 영향과 호출 비활성을 나눠 관찰해야 한다. 단위°C/소수점/현행 교정범위·열전대 타입·보상은 확인 전이다.

## 3. 제어 구조·호출·환산

### 고유망0484, LAD1734, NID4

| 원본 연결 | 해석 |
|---|---|
| Powerrail W127→Contact125.in; ORef112 RID34→W119 Contact125.operand | OFF 정접점. Negated 요소 없음 |
| Contact125.out W126→CRef106.en | 호출 활성은 OFF 조건. ON으로 치환하지 않음 |
| ORef113 RID1 W120→CRef106.IN0 | IN0는 별도 ON |
| ORef114 RID24 W121→Analog_input | TC-10 주변장치 입력 |
| ORef115 RID25 W122→Coeff / ORef116 RID26 W123→Zero | TC10 전용 계수/영점 |
| CRef106.OutValue W124→ORef117 RID27 | DB1.DBW264 Int 출력 |
| CRef106.Out_of_range W24→ORef23 RID361 | DB3.DBX20.5 Bool 출력 |

CRef106 RID351는0680 BlockInterfaceInfo의 NID4 UID106과 결속한다. CodeBlock118 RID5는0672 FCBlock Signal linearization/TOD.N63, NID4 UID118 AK Call로 FC63이다. 인터페이스 IN0 Bool, Analog_input/Coeff/Zero Int Input, OutValue Int/Out_of_range Bool Output. 고유망에는 Coil/SCoil/RCoil/Timer가 없고 호출 출력 연결만 있다.

상위 main0031 LAD1619 NID6: ON ORef271 RID52(0692 M0.0) W280→Contact282.operand, rail W284→in, out W283→CRef261.en 및264/267/270.en 병렬. CRef261 RID56/CodeBlock273 RID55는0694 및0688에서 Analog input conversion FC3으로 결속된다. 상위 ON과 하위 OFF를 모두 구분하며 병렬 호출을 ENO 직렬로 설명하지 않는다.

`live_index` `_7ev/401`의 startup 보충 STL은 `set s "on" clr s "off"`이다. 이를 OFF 채널이 예비로 억제될 의도와 양립하는 정황으로 읽되 현재 ON/OFF 값과 실행 여부는 미확정이다. 해당 doc401을0401-FlgNet HMI출력미러로 오인하지 않는다. OFF라는 이름만으로 상수 FALSE, 실행불가능, 현재 미사용을 확정하지 않는다.

### 공통 FC63 근거 재사용

0291 LAD1658 및0014 LAD1659, 선언0047/0048. 유효 범위 `raw > -1382 AND raw <= 32767`; Int→DInt Convert164/167/174와 Add170/Mul177/Div181 ENO 연쇄, `(DInt(raw)+DInt(zero))*DInt(coeff)/28000`, Move185→Int OutValue. Integer/DInt 경로이며 부동소수점 환산이라고 하지 않는다. 오버플로·절삭·ENO와 실제 스캔 결과는 실행 검증하지 않았다.

범위외 `raw > 32767 OR raw <= -1382`에서 Move193(-9999), Move193.eno W21→Coil23 Out_of_range. ENO 코일을 비교식 자체와 같다고 단순화하지 않는다. 0014 NOT IN0 Contact171→Move162(0)→OutValue 경로도 존재한다. TC10은 IN0=ON이나 호출EN=OFF이므로 둘을 한 조건으로 합치면 안 된다. 호출되지 않을 때 FC 내부 대체값 경로가 실행됐다고 쓰지 않는다. 0/-9999는 코드 대체값이며 안전 대체값의 승인 증거가 아니다.

## 4. 전기 전달 경로·실제 PDF

`all-in-one/sources/Electrical_Rev2.pdf` 실제172쪽을 pdftoppm으로 렌더하고 이미지로 확인했다. `extracts/TC10/FG171-PDF172.png`.

| 항목 | 직접 관찰 |
|---|---|
| footer | ANALOG INPUT MODULE; DATA27.05.2024; DISEGN G.G.; NORMA IEC; FG171/TOT262; 별도 개정기입 보이지 않음 |
| PEW390 | CPU515/MOD2, TC-10 SPARE(4–20mA). 단자9 Uv2,10 I2+,11 U2+,12 U2−/I2− 인쇄 |
| PEW392 | CPU515/MOD2, TC-10 SPARE(4–20mA). 단자13 Uv3,14 I3+,15 U3+,16 U3−/I3− 인쇄 |
| 공통 기준점 | MANA18→−0Vdc152.4 선,168/9→172/0 교차참조 |
| 외부 TC10 끝점 | 해당390/392 위 외부 연결선·센서기호·X3번호·케이블번호가 비어 있음. 인쇄된10/12 또는14/16을 실제 시공 연결핀으로 확정 불가 |
| 인접 TC09 | PEW386/388의 X3:100~104,171SCH1 및 센서 TC09 연결은 TC09 소유. TC10에 배정하지 않음 |

파생 sensor-measurement는 모듈 I2+10/I2−12,I3+14/I3−16을 module_pins로 요약하지만 이는 **단자 후보 표기** 수준이다. 원본 그림에는 그 핀의 TC10 케이블 연결이 그려져 있지 않다. 현재 모듈 주문번호/채널모드, 센서·변환기·배선·실드·극성·4–20mA 구간·실물 설치는 미확정. 도면 SPARE만으로 현재 부재라 결론내리지 않는다. 릴레이 부하5/9나 하단 접점표1/5/9는 이 입력 고유 회로의 근거가 없어 복제하지 않는다.

## 5. 알람·복구·쓰기 범위

- 직접 확인한 TC10 경보는0484의 FC63.Out_of_range→DB3.DBX20.5. 공통 FC63 ENO 코일의 계산 결과이며 TC09 MAX/MAX_MAX S/R와 별개다.
- 고유 선언명 TC10/TC_10/TC-10을 전체 decoded-original IdentXmlPart에서 검색: 0676의 영점/계수/값/OFR 4개와0678 원시1개. 값·OFR 선언 CS는 각각 NID4 UID117/23 Write 한 위치다. 별도 TC10 비교/지연·래치·RESET_ALLARM·STOP_HORN 소비 결속은 확보하지 못했다.
- 주소 범위 DB1 bits2112..2127 및 DB3 bit165와 겹치는 이름결속 GlobalAccess/SSD 범위도 검색했으며 두 고유 출력만 검출했다. 이 검사로 간접주소·무기명 absolute DB접근·통신 Writer까지 없다고 단정하지 않는다.
- 공통 startup0148 Word0~16 초기화는 TC10_OFR가 있는 byte20을 덮지 않는다(동일 원본의 TC09 공통 조사 재사용). 고유 Int DBW264와 Bool DBX20.5 쓰기를 Word 쓰기로 바꾸지 않는다.
- 고유망 타이머0은 전체 시스템에 샘플링/통신 지연이 없다는 뜻이 아니다. 현재 CPU 프로젝트·다운로드 이력·HMI 이벤트와 실제 원인제거/복구는 별도 증거가 필요하다.
- TC09 경보의 PV14/BR01/FN04/RD01 영향, MAX+5/MAX−2, 200/−60 상수, 수동 Reset을 TC10에 적용할 근거가 없다. OFR 해제나 값0은 안전재기동 승인 또는 센서 정상 증거가 아니다.

## 6. 증상별 읽기전용 관찰 계획

아래는 향후 승인된 현장 관찰의 기록항목이다. 현재 실행하거나 설정을 바꾸지 않았다.

| 증상 | 관찰·비교 위치 | 배제와 추가자료 |
|---|---|---|
| 값이 고정 | 현재 프로젝트/CPU 동일성, M0.0/M0.1, 상위 FC3/하위 FC63 호출, IW390:P/DB1W264의 같은 시각값 | 호출비활성·계수0·표시캐시·입력고정 구분. OFF를 켜서 시험하지 않음 |
| -9999 표시 | HMI 주소264와 PLC값, 원시값, 호출조건/OFR를 함께 기록 | 백업 저장값/실제 FC 대체값/현재 센서단선을 구분 |
| 값0 표시 | Coeff W216/Zero W214, ON·OFF, FC63 실행 여부 | 환산계수0와0014 대체0 경로는 서로 다른 원인 후보 |
| OFR와 표시 불일치 | DB3X20.5와 HMI Allarmi_203 주소·타임스탬프, 통신상태 | 경보문장·ACK·쓰기 이벤트 원본 필요. TC09 비트20.4와 혼동 배제 |
| 실물 채널 불명 | 명판, 모듈 채널구성, 승인준공도, X3/현장단자 양 끝점 사진 | PEW390/392의 실제 용도·센서/변환기 확인 전 배선 변경·교정 금지 |

관찰 기록은 관찰자/시각·시간대/위치/값·단위/수집장치/CPU프로젝트 근거/원본비교/배제결과/조치/복구증거를 분리한다. 사용자 운영자료와 사진은 공개 Git에 복제하지 않는다.

## 7. 완료·누락·인계

| 상태 | 판정 |
|---|---|
| documentation | complete_with_gaps: TC10 한 개 7영역 문서초안 |
| static_review | 자체 XML·주소·해시 대조, 독립 검토는 부모 대기 |
| ui_records | not_run; 기존 앱 기능의 TC10 지원 완료로 주장 안 함 |
| publication | not_published; 원본/버전/배포 무변경 |
| tia_compile / live_cpu / field_recovery | 모두 not_performed |

도면·래더 비교자료는 확보했으나 앱 나란히 보기·백업선택복원·기록전후비교·보고서/PDF 생성 기능의 실제 저장/재읽기/재열기 검증은 하지 않았다. 이번 PDF작업은 원본도면 페이지 렌더이며 보고서/UI 검증이 아니다. note/repair_observation/미지필드/타설비/운영기록/초안/저장키를 수정하지 않았다.

남은 자료: 현행 CPU·프로젝트 비교, 현재 ON/OFF와 호출상태, 실제 TC10 설치유무 및390/392 용도, 센서/변환기 명판·측정범위·보상, 채널 하드웨어설정·배선 양 끝점·준공도, HMI 위젯/쓰기/ACK/통신. 새 자료 없이 같은 실물 보류를 반복조사하지 않는다. 다음 조치는 부모의 고유 OFF 호출/외부배선 미확보/HMI주소 보강 독립 검토다.

### 실제 작업시각 (UTC)

- 2026-10-11T11:24:02Z — instructions and scope read began
- 2026-10-11T11:24:27Z — TC10 unique declaration and input/output mapping read
- 2026-10-11T11:24:45Z — FG171 PDF172 image visually inspected
- 2026-10-11T11:25:02Z — OFF call and missing external wiring reported to parent
- 2026-10-11T11:25:49Z — declaration range scan and backup arrays checked
- 2026-10-11T11:28:05Z — seven-area draft written
- 2026-10-11T11:28:52.865397+00:00 — document assertions and source hashes verified

착수부터 최종 대조까지 실제 경과 290.9초. 예상 작업시간으로 대체하지 않았다.

### 선정 원본 SHA256·고정 Git blob 전체 목록

43개 선정 원본/맥락/보존 파일 모두 고정 blob 바이트일치, 중지5자산 freeze일치, 원본 Git 변경0. 해시 일치 파일수를 의미검토 완료수로 세지 않는다. 중지자산은 해시 보존 확인만 했고 실행하지 않았다. 검사 JSON과 해시 JSON은 extracts/TC10/static-review.json 및 source-hashes.json.

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
| `all-in-one/registers/sensor-measurement.json` | `4b8c357c803e7b429766d54a87bf49bb5dd25343a9797b44b5702df93440c7a3` | `e032d23b1f3163dcf95390589c93e2e9dcda474e` |
| `all-in-one/registers/simulator-freeze.json` | `bb93c1994effc5609939ba566b7802ce7ed55154a7310f02379b308ac2c8c835` | `808ffac14dbd1b4a7d797fa6cd0d647635d90b47` |
| `all-in-one/registers/virtual-plc-test-results.json` | `a6b389f797f9a8b5ffe6928b8420f55c4cc459a327b0b48d716079d2eca6dd64` | `757dd50e45184568facb8ff62900b39d3ce848d1` |
| `all-in-one/sources/Electrical_Rev2.pdf` | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` | `f610fd7c7ce14ae951b00cff57b969259bfb389d` |
| `all-in-one/sources/GME_20250506.zap18` | `00c79b6d986e68298f65b172c1807115bc5d9e450a74fcc989d0796d8d8a4ea8` | `211c4f604627a32f82a1124c2a9872c2fcf00865` |
| `all-in-one/sources/PEData.plf` | `647de7ea123daced41c27bec8f81aeb93c712cac714d4754d7da5c528abb016a` | `65605ff8910f920109da731604aa5dc8d83fc956` |
| `all-in-one/sources/decoded-original/0014-FlgNet.xml` | `2e814adbaac6bab99bc668bfdab74f0fc90576324d0b88728951683869cfac30` | `4d164b074fcc13a8f97da9e24382cc169ef29555` |
| `all-in-one/sources/decoded-original/0031-FlgNet.xml` | `76385eab8f8f72b9faa16f7cf8905f395591b18c0a9ee9e6d7dd085a38c45c65` | `653d27572de6beedcf3eb6c95702bb119a8b567f` |
| `all-in-one/sources/decoded-original/0047-IdentXmlPart.xml` | `2e53bb895dd1ad2a74efaeb1ef16dfd61e62b1b2d7aa34cec8612f1b9cb0928e` | `3dc282f149a21fdf76d5521ef1c833be63b578b4` |
| `all-in-one/sources/decoded-original/0048-IdentXmlPart.xml` | `d8e8687de7271bd294c2b62b33d789700af9d5014d82b130141988c4d479253d` | `64fc5a7f1ad33f3b901b00f0d22d23578ffabff8` |
| `all-in-one/sources/decoded-original/0148-FlgNet.xml` | `1d80e1bbf1c82dcc4dd18628c35935bbd55a17b5be9c1ca7bfb249600d154313` | `3069ae3b5fa16ed10a64c149b6cf5cb5ace423b3` |
| `all-in-one/sources/decoded-original/0291-FlgNet.xml` | `fe0b92f074eba25148ce34084649af3d968962558d652727f1eea19f3e3c2550` | `1418fb2ed172c6df694a5eb8bf2dffd0b177653b` |
| `all-in-one/sources/decoded-original/0484-FlgNet.xml` | `200033a67b7cc1419eb793dafa7b11a6a2cd57170544cc600bc37c746c5a3670` | `fb1dffd055ca3acd94b7e0c2af95b626fdff55d7` |
| `all-in-one/sources/decoded-original/0562-IdentXmlPart.xml` | `85aada44dd9a3e66835463c3fed400f1efe121f4f5bc5ab8f0ad49481ec0ea1c` | `1609802542a3e560baba3f2b73c306be281dfb23` |
| `all-in-one/sources/decoded-original/0563-IdentXmlPart.xml` | `86cf35b6baebc079cb5a092baf53ec3364c377ea7318eb263ab69c8b4550b4ad` | `6a10fc694f896cda16409804daf2554c91635654` |
| `all-in-one/sources/decoded-original/0672-IdentXmlPart.xml` | `6bfc2ba142d6270c39eb1f13b2886204865af6d46eadc5f410c26981b8da9222` | `2f2790dab4bb2357733112220e0acc41edb6feb6` |
| `all-in-one/sources/decoded-original/0674-IdentXmlPart.xml` | `4770702f519bacda69202bb2f7733d983074bda90964360c238f990d9d08fd84` | `f210593944547b63eab10c667348711413600aab` |
| `all-in-one/sources/decoded-original/0676-IdentXmlPart.xml` | `c58427c5b0ac6c11cdb52e4c6d0461c7b191fae81ccace191048e9f175fcec59` | `1ed67265f69796a4e659f9438e551068037f33a4` |
| `all-in-one/sources/decoded-original/0678-IdentXmlPart.xml` | `51e637e0b9713c028810f2a717b5c3804a3a26c2f1be7e332a4d6bf277bfc382` | `7fafb2297bcdf739bf1d1dd68cebc0d74f2a40cc` |
| `all-in-one/sources/decoded-original/0680-IdentXmlPart.xml` | `fd551ad5d47bbd66c6bcdcc1949aaddf68cc086a3ddf6fb337adc767954c2b95` | `c9049ced1eaed72c5e251a88601d46ddec8c3e50` |
| `all-in-one/sources/decoded-original/0688-IdentXmlPart.xml` | `ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda` | `463585759f1ecd94f32362b4fefb000a152f5773` |
| `all-in-one/sources/decoded-original/0692-IdentXmlPart.xml` | `bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037` | `737785d03b5fad43c5b4d451955726d800edb1c0` |
| `all-in-one/sources/decoded-original/0694-IdentXmlPart.xml` | `757ccebdf32d0a168dd787bfa735fe6494eac4c4a9f7a5adc63898a88e8b152d` | `c45e8f3ca4129dc06734f6a12ef79e6ed6528a7d` |
| `all-in-one/sources/decoded-original/network-map.json` | `c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60` | `424430b6b953e43138e5d0a18ca40c949e21cfa1` |
| `all-in-one/sources/hmi_plc_tags.csv` | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` | `cf4c0650e7c7baac350dcb89909b808435704880` |
| `all-in-one/sources/live_index.json` | `14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1` | `e35ccea1f841349c632666c29954b7bcd4f5839e` |
| `all-in-one/sources/source-manifest.json` | `5af6e85994536897fd92f75972534a691e6eb0f067aafe07679c0788fd84e5bf` | `38cf407491d52dc6128cf94ca8a4bddee350de6d` |
| `docs/equipment-standard/INVENTORY.json` | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` | `587c3748ad9224718f95ba06463fee913dae231d` |
| `docs/equipment-standard/WORK-ITEM-TEMPLATE.md` | `4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586` | `e546f39535d2b589e80f97db869ac37ce4d05cfd` |
| `docs/equipment-standard/WORK-STANDARD.md` | `05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99` | `f76a570cc73098632e08759b17934000f7e3a253` |
