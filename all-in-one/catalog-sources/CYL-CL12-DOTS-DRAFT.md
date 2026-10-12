# CYL-CL12 공압 실린더 고유 원본 조사 초안

- 대상 한 개: CYL-CL12, 부모 PV14, component/phase2/planned, parent_child_separate. 표준 GME-STD-1.0.0.
- 읽기 원본 source-mv06, 고정 commit abcf31c5030bc7ef8749ed8e869a857f2387a28a, VERSION v1.12.0. 작성 2026-10-11 UTC. 실제 모델/추론 설정 관측 미확인.
- BATCH21 지침·범위·중복검토, AGENTS, 저장소 스킬/source-map, WORK-STANDARD/WORK-ITEM-TEMPLATE/INVENTORY/START-GPT61 및 최신 인계 상단을 읽었다. PV14 부모 초안은 탐색색인·공통근거로 재사용하고 부모 전체를 반복 조사하지 않았다. CYL01~10 공통 경계 및 CL05 0288 W65/W67 operand 정정을 보존한다.
- 수정 범위는 이 MD와 extracts/CYL-CL12뿐. 원본/공통코드/대장/버전/배포/운영/PLC/현장/보호값/SEJIN 변경0. 시뮬레이터 작성·수정·생성·실행·행동시험0, 원본 생성기/앱 빌드0, 재위임/새 Work/Codex/업로드/사용자 전송0.

## 1. 설비·자료 기준 — 적용

INVENTORY catalog[212] 및 equipment[207]은 CYL-CL12를 PV14 하위 공압 실린더로 분류한다. 대장상의 별도 ID가 독립 PLC 출력이나 실물 검증을 뜻하지 않는다. 중복검토의 physical_identity_verified=false/confirmed_alias_duplicate=false를 유지한다. CLIENT-CL12 외부 모터와 다른 이름 공간이며 숫자12를 근거로 합치지 않는다.

PID_1684n002I.pdf 실제 PDF1을 렌더하고 회전·확대했다. **CL-12 리더는 PV-14 가지의 액추에이터 도식으로 이어진다.** 외기 화살표→PV14 밸브→BF01/BF02 공통 유입 덕트의 연결과 TC09 인접 관계를 확인했다. 다른 PV01/02/03의 독립 상세도와 달리 이 위치에는 CL12 전용 EV 번호·LS 번호·공압 공급 튜브 양 끝점이 표기되지 않았다. P&ID의 구동 관계와 대장 부모 관계는 부합하지만 CL12 실물 제조사/보어/스트로크/포트/로드 결합/설치 방향/복귀 방식/안전 위치는 미확보다. 전기 도면의 PV14 솔레노이드와 CL12 공압 포트 사이를 새 배관 번호로 메우지 않는다.

P&ID Setpoint Open170°C/Close160°C, 유입 Max180°C는 구도면 표기이며 현재 승인 보호값이 아니다. 부모 PV14/TC09의 백업 온도값·히스테리시스와 같은 조건으로 합치지 않는다. 인접 EV51~58 등은 필터 세정 계통이며 CL12 구동 EV 번호가 아니다.

| 선정 PDF | 직접 렌더·시각 확인 | 해당 쪽 제목·개정 |
|---|---|---|
| PID_1684n002I.pdf | 실제p1, CL12 확대와 제목란 | Drawing1684n002, FG ‘−’, 원작성06/04/2011, Apex I 15/01/2013 |
| Electrical_Rev2.pdf | 실제p169=FG168 | PNEUMATIC VALVE, 27.05.2024, 개정란 별도 기입 없음 |
| 같은 PDF | 실제p178=FG177 | DIGITAL INPUT/OUTPUT MODULE, 27.05.2024, 개정란 별도 기입 없음 |
| 같은 PDF | 실제p181=FG180 | DIGITAL INPUT/OUTPUT MODULE, 27.05.2024, 개정란 별도 기입 없음 |
| Electrical_Can_Decoating_20241118.pdf | 실제p35/64 | DUST ROUTE CONDUIT PIPING(1), CANDC-CONS-E018-035, D-PAGE18, Rev1 24.11.11 first draft design |
| 같은 PDF | 실제p60/64 | CABLE SCHEDULE(9), CANDC-CONS-C010-060, D-PAGE10, Rev1 24.11.11 first draft design |

시공도 CHECKED/APPROVED 공란. 파일명 Rev2를 모든 OEM 페이지의 개정번호로 일괄 적용하지 않는다. 실제 6개 고유 페이지를 확인했으며 크롭은 추가 페이지로 세지 않는다. PDF1은 텍스트 추출이 비어 있어 래스터 시각검토를 근거로 삼았다.

## 2. I/O·HMI — 부모 연결 적용 / 자식 독립 소유 미확보

아래 XML 약칭은 all-in-one/sources/decoded-original/<번호>-IdentXmlPart.xml 또는 -FlgNet.xml이다. Bool AO는 비트 오프셋이다. 선언의 Global/주소를 확인했으며 아래 신호는 모두 **부모 PV14의 구동·위치 문맥**, CL12 전용 신호가 아니다.

| 신호·형식 | 주소 | 원본 선언/참조 |
|---|---|---|
| PV-14 Global Bool | Q17.0 | 0594 RID268 SSD AO136 SAD Output; NID21 ORef2021 Write |
| PV-14 OPEN/CLOSE Global Bool | I28.0/I28.1 | 0627 RID35/33, AO224/225 SAD Input; NID1 ORef109/102 |
| Inputs.PV-14 OPEN/CLOSE Global Bool | DB13.DBX22.0/22.1 | 0629 RID36/34 AO176/177 BAD4; 0628 DepDBBlock RID4 TOD13; NID1 ORef113/106 Write |
| Flag.M_PV14 Global Bool | DB2.DBX13.1 | 0596 RID277 AO105 BAD253; 0595 RID253 TOD2; NID21 ORef2016 Reset/2017 Read |
| ON / Open false air Global Bool | M0.0 / M2.1 | 0594 RID52 AO0 / RID278 AO17 SAD Memory; NID21 ORef2013/2018 |
| Allarm.MAX_TC09/MAX_MAX_TC09 | DB3.DBX8.6/8.7 | 0596 RID279/280 AO70/71 BAD274; 0595 RID274 TOD3; NID21 ORef2019/2020 |
| Allarm.Emergency_module_fault | DB3.DBX16.6 | 0596 RID312 AO134 BAD274; NID21 ORef23 |
| Allarm.Fault_PV14 | DB3.DBX13.4 | 0596 RID275 AO108 BAD274; NID21 ORef2014; 부모 위치경보 |

0397 LAD1070/hmi inputs 원본 NID1의 PV14 두 가지를 직접 확인했다. 이름이 hmi여도 실제 입력 전달 망이다.
- OPEN: rail W21→Contact108.in; ORef109/RID35 W107→108.operand;108.out W110→Coil112.in;112.operand W111→ORef113/RID36.
- CLOSE: rail W21→Contact101.in; ORef102/RID33 W100→101.operand;101.out W103→Coil105.in;105.operand W104→ORef106/RID34.
- 두 접점에 Negated 없음, 출력은 일반 Coil. 이 연결은 정상극성·실제 위치·CL12 로드 종단을 독립 확인하지 않는다. PV01/02의 MEM_OPEN/CLOSE를 이 실린더에 복제하지 않는다.

hmi_plc_tags.csv 행655~657: PV_14\\Flag=DB2,X13.1(000B5), LS_Open=DB11,X74.0(000B3), LS_Close=DB11,X74.1(000B2). 행566 Allarmi_109=DB3,X13.4(00120). HMI 위치 주소는 처리 DB13X22.0/1과 다르며 부모 조사에서 미결속인 상태를 유지한다. CL12 전용 UI·누름/떼기 이벤트·권한·현재 통신/값은 미확보다. 행188 ResetAlarms=DB2,X13.4는 부모 RESET_ALLARM DB2X6.0과 다르므로 이름만으로 Reset 경로를 확정하지 않는다.

decoded-original XML695개를 (?:CYL[-_ ]*)?CL[-_ ]*12\b, 대소문자 무시로 이름 검색해0건. 검사JSON cl12-search.json. 검색은 별칭/간접주소까지 신호 부재를 증명하지 않으며 695 의미검토로 집계하지 않는다.

## 3. 제어 구조 — 부모 전달 경계 적용

0216 LAD1903/filter 원본 NID21(색인 index_order22와 구분)을 고유 연결 증거로 재확인했다. CRef 없음.

Q17.0 = ON AND (M_PV14 OR Open false air OR MAX_TC09 OR MAX_MAX_TC09 OR Emergency_module_fault).

| 핀 경로 | 해석 |
|---|---|
| rail W2049→Contact2035.in; ORef2013 W2022→2035.operand; out W2036→각 요청 접점 in | ON은 메모리이며 TRUE 상수 아님 |
| ORef2017 W2027→Contact2041.operand; out W2042→OR2007.in1 | 부모 수동요청 |
| ORef2018 W2028→Contact2043.operand; out W2044→OR.in2 | 냉풍요청 |
| ORef2019 W2029→Contact2045.operand; out W2046→OR.in3 | TC09 MAX |
| ORef2020 W2030→Contact2047.operand; out W2048→OR.in4 | TC09 MAX_MAX |
| ORef23 W21→Contact22.operand; out W24→OR.in5 | 비상모듈 경보 |
| OR2007 Card5.out W2031→Coil2012.in; operand W2033→ORef2021/RID268 | 부모 Q17.0 쓰기 |
| ORef2014 W2023→Contact2037.operand; out W25→RCoil2004.in; operand W2026→ORef2016/RID277 | ON AND Fault_PV14에서 수동요청만 Reset |

다섯 요청 접점은 비반전이다. Fault_PV14가 전체 OR 출력의 공통 차단 접점인 것은 아니다. 수동요청0 또는 Fault Reset만으로 Q17.0이 반드시0이라고 하지 않는다. 물리 전달 범위는 Q17.0→168KA1→PV14 솔레노이드→미확정 공압 배관/액추에이터→CL12/PV14 기구다. Q=0을 닫힘완료·잔압소거·접근안전과 같게 하지 않는다.

부모 PV14 §3·5의 호출/추가Writer·startup DBW 겹침·시뮬레이션 대체쓰기 후보는 공통 조사로 재사용한다. 이 문서는 0216과0397의 선택 가지를 확인했으며 부모 전체/모든 Writer/현재 스캔을 재검증하지 않았다. 금지 자산은 해시 보존만 수행했다.

## 4. 전기 전달 끝점 — 부모 경로 적용 / 공압 양 끝점 미확보

직접 렌더한 OEM PDF에서 다음을 확인했다. 전압·퓨즈값은 원문이며 현행 승인 설정이나 측정치가 아니다.

| FG/실제 PDF | 양 끝점·전달 |
|---|---|
| FG180/p181→FG168/p169 | CPU515 MOD4 Rack3 단자31 A17.0→168/3→168KA1 A1; A2→−0Vdc152.4. 모듈39 3L+는 +24Vdc152.5→X22:4027 5×20 4A IST.→180.1,40 3M→−0Vdc |
| FG168/p169 부하 | 110Vac152.8→168KA1 **5–9**→168.1→X3:84 5×20 2A F→168.2→PV14 A1; PV14 A2→X3:85→0Vac9.9 |
| FG168/p169 OPEN | 110Vac152.8→X3:86 2A F→168.3→ZS.O PV14 접점13/14→X3:87→E28.0 참조177/2 |
| FG168/p169 CLOSE | 110Vac152.8→X3:88 2A F→168.4→ZS.C PV14 접점13/14→X3:89→E28.1 참조177/2 |
| FG177/p178 입력 | E28.0 참조168/4→단자1; E28.1 참조168/5→단자2. CPU515 MOD4 Rack3, PV14 OPEN/CLOSED 설명 |

168KA1 코일 A1/A2와 실제 부하5–9 및 하단 참조표1/5/9를 구분했다. EV의69KA/71KA 5–9 정정을 유지하며 타 부모 접점번호를 CL12에 복제하지 않는다. PV14 ZS.O/C는 부모 밸브 위치 표기다. 실린더 부착 센서 모델·설치 위치 또는 새 LS12 번호를 추정하지 않는다.

시공 p35의 211RB→DUS1TB1→DUS1TB2→ZS.O/ZS.C/PV14 가지와 p60 케이블 표:

| 행/케이블 | From→To·규격 | 경계 |
|---|---|---|
| 10_4 =DUS+SC01-DUS1TB1A | BF01/JB01→SC01/DUS1TB1 ZS.O/C, DC CVV7G1.0 spare2 | E500→222RE→222LAP1→212LAP1→211RB→E100, LEN16 |
| 10_5 =DUS+SC01-DUS1TB1B | 같은 양끝 PV14, AC CVV5G1.0 spare2 | 같은 경유→E200, LEN16 |
| 10_7 =DUS+PV14-DUS1TB2A | SC01/DUS1TB1→PV14/DUS1TB2 ZS.O/C, DC CVV7G1.0 spare2 | E110 LEN11 |
| 10_8 =DUS+PV14-DUS1TB2B | 같은 양끝 PV14, AC CVV3G1.0 spare0 | E110 LEN11 |
| 10_10 =DUS+PV14-ZS.OA | PV14/DUS1TB2→PV14/ZS.O, DC CVV2C1.0 | E121 LEN3 |
| 10_11 =DUS+PV14-ZS.CA | PV14/DUS1TB2→PV14/ZS.C, DC CVV2C1.0 | E122 LEN3 |
| 10_12 =DUS+PV14-PV14A | PV14/DUS1TB2→PV14/PV14, AC CVV3G1.0 | E123 LEN3 |

p60의10_6은 검게 가려지고 p35 대응은 Delete이므로 숨은 텍스트를 활성 결선으로 읽지 않는다. TC09 10_9는 별도 온도센서 경로. LEN은 설계 길이이며 실측이 아니다.

**상충과 미결속:** OEM 위치접점 공급110Vac 대 시공 ZS.O/C DC 분류가 상충한다. X3:84~89와 현장 DUS 단자별 심선1:1, 실제 입력모듈 정격, 솔레노이드→CL12 공압 포트가 미결속이다. 이를 전기/공압의 완전한 현행 경로로 표시하지 않는다. 필요한 자료는 승인 준공도·단자심선표·모듈/솔레노이드/액추에이터 명판·공압회로 및 튜브 양 끝점이다.

## 5. 알람·복구 — 부모 영향 참조 / 자식 독립 항목 미확보

CL12 독립 경보/타이머 선언은 확보하지 못했다. 부모 PV14 §5의0215 LAD1902/filter NID20, T20 S5T#20S 및 Fault_PV14 DB3X13.4 Set/Reset은 공통 근거로 참조한다. **부모20초를 실린더 정격 응답시간·정비기준·독립 CL12 타이머로 복제하지 않는다.** 부모 불일치식은 ON AND ((Q17.0 AND NOT 처리OPEN) OR (NOT Q17.0 AND NOT 처리CLOSE))이며 별도 동시참 진단까지 증명하지 않는다. 이 경보를 CL12 기계고장 확정으로 해석할 수 없다.

원인 후보는 출력/릴레이/솔레노이드/공압/기구/센서/입력전달 단계로 구분해야 한다. Reset 요청은 원인 제거·현장 안전·실제 복구의 증거가 아니다. 경보문장/ACK/현장 복귀절차/현재 보호값은 미확보다. 부모 전체 경보 망을 여기서 재분석하거나 새 Reset 동작을 수행하지 않았다.

## 6. 증상별 읽기 전용 관찰 — 적용

실제 조작·강제출력·신호주입·탈거·시험 지시가 아니다. 위험설비 접근·계측은 승인된 자격/절차가 필요하다.

| 증상 | 같은 시각 수집할 증거 | 배제/판정 경계 |
|---|---|---|
| CL12가 움직이지 않는 것으로 보임 | 부모 Q17.0,168KA1/부하,PV14 명판·표시,공압/로드 위치,원시I28.0/1 | 출력참만으로 실린더 전기/공압 전달을 확정하지 않음 |
| HMI는 열림인데 로드 위치 불명 | HMI 실제 태그/시각,DB11X74.0/1,DB13X22.0/1,I28.0/1,센서 실제 설치 위치 | HMI 미결속과 센서 소유부터 확인; CL12 위치 피드백으로 자동 승격 금지 |
| 수동요청0인데 출력 유지 | M_PV14,다른4개 OR 요청,ON,현재 프로젝트/Writer | 요청 Reset과 실제 출력 차단 구분 |
| 위치경보 발생 | 명령·양원시/처리입력·부모T20/Fault 시각 | 기구/공압/센서/배선 원인 분리; 자식 고장확정 금지 |
| 출력0인데 닫힘/안전 불명 | 승인 안전위치·액추에이터 복귀형식·잔압/기계상태 기록 | 복귀 방식 미확정; 출력0만으로 접근 허가 불가 |
| 도면 전압과 관찰 불일치 | 모듈 주문번호·명판·준공도·승인 계측 기록 | OEM110Vac/시공DC 상충을 임의 절충하지 않음 |

기록 필드: 관찰자·실제시각/시간대·위치·주소·값/단위·신선도·수집장치·현재CPU/프로젝트·비교원본/개정·배제결과·승인조치·별도복구확인. 운영기록이나 사진을 생성/복제하지 않았다.

## 7. 완료·누락·검사 — 적용

| 상태 축 | 결과 | 경계 |
|---|---|---|
| documentation | complete_with_gaps 초안 | 고유CL12 리더·부모 구동 경계·7영역·6쪽 원본·상충 명시 |
| static_review | 자체 정적검사 완료 / 부모 독립검토 대기 | XML 주소/선택 핀·PDF·선정 해시, 동작검사 아님 |
| ui_records | not_run | 4기능 구현·저장·재읽기·재열기·PDF 검증 안 함 |
| publication | not_published | 통합/버전/배포 없음 |
| tia_compile | not_performed | 실행 없음 |
| live_cpu | not_performed | 현재CPU/극성/Writer/보호값 미확인 |
| field_recovery | not_performed | 실물/공압/센서 설치·원인제거·복구 미확인 |

네 기능: 도면·래더 비교는 문서상 참조만 작성, 통합백업·선택복원/기록 전후 비교/보고서·PDF는 이번 구현 비범위이고 실행 검증 미수행. 기존 note/repair_observation/미지필드/타설비/초안/저장키 보존. BC01 동등 기능완료 또는 현장 완료로 세지 않는다.

누락 우선순위: (1) CL12/PV14 실물 표찰·명판·기계 연결, (2) 공압 공급/포트/튜브 끝점과 복귀·안전위치, (3) ZS.O/C 실제 설치와 정상극성, (4) OEM/시공 전압 상충 및 X3↔DUS 심선 결속, (5) 현재CPU/HMI 이벤트·DB11 전달·Writer, (6) 승인 복구절차와 실제 관찰 시간선. 새 자료 없이 같은 보류를 반복 조사하지 않는다. 다음 한 작업은 부모의 독립 원본 검토다.

### 검사 범위

고유 의미검토는 P&ID CL12/PV14 위치와 제목, OEM3쪽·시공2쪽의 선택 전달 경로, 0216 요청/출력 및0397 PV14 입력 가지, 관련6개 선언XML의 선택 RID, HMI 선택5행이다. XML695 이름 검색·원본 해시수는 의미검토수와 다르다. 원본 생성기/preflight/앱/시뮬레이터는 실행하지 않았다. 명령은 정적 XML 파싱, PDF 렌더, SHA256, git show/cat-file/status와 자체 문서검사에 한정했다.

### 선정 원본 SHA256·고정 Git blob 바이트일치

아래 원본 경로는 source-mv06 기준. 각각 고정 commit의 git show 바이트와 현재 파일을 직접 비교했다. 부모 공통알람 전체 의미검토 대신 부모 초안의 근거를 명시하여 재사용한다. 부모 공통근거 0215/0597도 보존 해시에 포함했으나 이번 고유 의미검토 수에 포함하지 않는다. 해시/검사 상세는 extracts/CYL-CL12/source-integrity.json 및 verification.json. 조사 산출물/지침 해시는 별도 research-input-hashes.json이며 Git 원본과 구분한다.
| 원본 경로 | 전체 SHA256 | 고정 Git blob OID | 바이트일치 |
|---|---|---|---|
| .agents/skills/gme-equipment-rollout/SKILL.md | fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b | 9aa820ea6ca15b4e136c9772423b78ed4df6a3d4 | PASS |
| .agents/skills/gme-equipment-rollout/references/source-map.md | 40612c5efb8f94608840c7bc0e9095ea840df54920861c388ae48ea34c7998dc | 49e50a7a8e56a16e2ec7f3607a03fd90adb8f1d3 | PASS |
| AGENTS.md | 0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2 | 073164bc6efd5791032d62c71b03b4dab48cb6f8 | PASS |
| EXPANSION-WORK.md | ec624de9fd2fcfac861a67fd5e828b25ef46db50bfd7a37ff16e2cb54cd0f7e2 | 4c42d88ecc2d48269eb23e13a20ebf3721a092a1 | PASS |
| PUBLICATION_STATUS.md | efe4857aec598d90470322cf3962eb3fe1f64947630e1fdf71d1c90134de8740 | d76401cf291fc0be681acc51fa898ad3ce46ff78 | PASS |
| VERSION.json | 5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7 | fffb51663b7705aec91cb119ca80ee943a4ce758 | PASS |
| WORKSPACE-HANDOFF.md | 215096d997782e78e901dfae36c782937e49611fbeb677a0d3fa50cbecf8d074 | dd0b8989d2376c4415bba9bd826fe6754c6b1a12 | PASS |
| all-in-one/ACTIVE-WORK.md | eff3bbc08ecff41da3beff77f3fec48e7d148708192bcaaab00f34b6a721afc2 | 6eb947c629b5ddf9c759ef87649451303938864b | PASS |
| all-in-one/assets/program-model-data.js | 52f8199371e3399b7c0d44ab5469f0472aced79d56bbef2887f7625f5d2aff0f | 38f34b0caa380a16ccad6f6f1e234a2fdf23f327 | PASS |
| all-in-one/assets/simulator-workspace.js | 3a6dfc618ff7e7b238f2671dc85d65704f33093a18eac879d86081d92c31e8bc | 97c2c831c77a9699fff0e0960b3bc1b7d93d45b3 | PASS |
| all-in-one/assets/virtual-plc.js | 5f1876052dc0067b1f010af0dfc941946e37003167481731293615d9c1c36dbc | 0bd9eceb54365a91214a37c5601b5067c39a3f75 | PASS |
| all-in-one/registers/equipment.json | 7870325dff32bbca90fa34507b301c4aad3347d669fddcd03b910343663996fa | acc42633033398216469064932c4b76987371606 | PASS |
| all-in-one/registers/program-model.json | 6203479c086b15bada12ac9d7e37db9280234ec26f1ea6091d7211dc09a577c5 | 9860b10f008d3a5ae714be50d77b703dfec32f3a | PASS |
| all-in-one/registers/simulator-freeze.json | bb93c1994effc5609939ba566b7802ce7ed55154a7310f02379b308ac2c8c835 | 808ffac14dbd1b4a7d797fa6cd0d647635d90b47 | PASS |
| all-in-one/registers/virtual-plc-test-results.json | a6b389f797f9a8b5ffe6928b8420f55c4cc459a327b0b48d716079d2eca6dd64 | 757dd50e45184568facb8ff62900b39d3ce848d1 | PASS |
| all-in-one/sources/Electrical_Can_Decoating_20241118.pdf | 3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd | 0ee6b6f8361c5790864dbba4bbd9d55e8e7c08f8 | PASS |
| all-in-one/sources/Electrical_Rev2.pdf | 5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6 | f610fd7c7ce14ae951b00cff57b969259bfb389d | PASS |
| all-in-one/sources/PID_1684n002I.pdf | 2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b | 8c83a59fefd5b8b651ec3537ea4236a073f5e109 | PASS |
| all-in-one/sources/decoded-original/0215-FlgNet.xml | 723789a5daf72bba1d49751963bc6517739761ae3a4122b875b8a66ea0de3a14 | 096f3482463759a7a506433e7b3266e3f13d3f14 | PASS |
| all-in-one/sources/decoded-original/0216-FlgNet.xml | 3a7fa8b0a095f054c543f90d0ffab84a8cd0c60ff1b5ec0101b112dc8f4ff37d | 97280ef67131ab7a480c8b0030d74de765c14c65 | PASS |
| all-in-one/sources/decoded-original/0397-FlgNet.xml | bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834 | 4ab8370493c4e28fc1eabeeebe2743d27f0c4021 | PASS |
| all-in-one/sources/decoded-original/0594-IdentXmlPart.xml | 88ad174a0d5ccdf636146b68e43aa578c449c77ceab074b7ced2580261b831cd | f38b7d9a52b3d5ae74953da8290f6b417758c1b5 | PASS |
| all-in-one/sources/decoded-original/0595-IdentXmlPart.xml | 10c8152d3ae704c00e5d4c2f6ef1629be5a65aaf5ef626e1ea6085b9204f8f52 | 1f24565efac58926dabf5b3fc54ad0e9537410b2 | PASS |
| all-in-one/sources/decoded-original/0596-IdentXmlPart.xml | a0d79c7c4971d16f0e176c0c7d7b459a6e6702035b01ec01fd83e95561839dc0 | c8b2d1a05727b4ca44e2e4bed9fb58ba2b717576 | PASS |
| all-in-one/sources/decoded-original/0597-IdentXmlPart.xml | 60e292145fe54912a1da7510c8641a4f4c85efe62e1b5206ee3d92794a28de20 | 2831597d1879bd83f239e838dd4cbe6b3dc64e77 | PASS |
| all-in-one/sources/decoded-original/0627-IdentXmlPart.xml | 08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb | 61ebc0abbb2ca160e11e1da400a3f14a397d8bc5 | PASS |
| all-in-one/sources/decoded-original/0628-IdentXmlPart.xml | 9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd | 170ca5c72599edc7ea7eefe651c3680ce325e76a | PASS |
| all-in-one/sources/decoded-original/0629-IdentXmlPart.xml | 67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972 | 058129bb01e27f7a6a0d0293f332d745e5bab74e | PASS |
| all-in-one/sources/decoded-original/network-map.json | c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60 | 424430b6b953e43138e5d0a18ca40c949e21cfa1 | PASS |
| all-in-one/sources/hmi_plc_tags.csv | a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404 | cf4c0650e7c7baac350dcb89909b808435704880 | PASS |
| docs/equipment-standard/INVENTORY.json | 720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc | 587c3748ad9224718f95ba06463fee913dae231d | PASS |
| docs/equipment-standard/START-GPT61.md | 35769e3146ccd707fea2b81b67b30376b76a0a19c7e662fe2bb4fdd382306f94 | 0d08cab3678df7e2625251b641b138ef4956483b | PASS |
| docs/equipment-standard/WORK-ITEM-TEMPLATE.md | 4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586 | e546f39535d2b589e80f97db869ac37ce4d05cfd | PASS |
| docs/equipment-standard/WORK-STANDARD.md | 05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99 | f76a570cc73098632e08759b17934000f7e3a253 | PASS |

선정 34개 전부 고정 blob 바이트일치, 중지5자산 freeze 일치. 원본 Git status --short 공란. 의미검토 범위와 별개다.
