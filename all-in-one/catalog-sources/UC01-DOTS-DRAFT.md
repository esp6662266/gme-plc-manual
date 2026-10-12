# UC01 드럼 배출실 — 고유 원본 조사 7영역 초안

## 핵심 확인·상충·누락

- P&ID 실제 PDF1에서 UC-01 표기는 RD-01 출구 본체, 하부 PV-02 및 MC-04측 배출 경로와 인접한다. 상부 가스 경로의 PSH-02·RO-03·TC-03 및 PV-05/06 질소 주입을 확인했다. 공정 연결이지 같은 PLC 제어 소유나 실물 동일성 확정이 아니다.
- 시공 PDF3/5의 FLOW_B / UC-01은 위치코드다. PSH02/PV05·06/TC03/RO03가 나열되지만 독립 UC01 제어반·전용 제어기·전용 알람을 뜻하지 않는다.
- 고유 이름·변형을 decoded-original XML695개와 보충5파일에서 검색했으나 일치 파일0개였다. 이는 검색 범위 내 미확보이며, UC01 신호가 실제로 없다는 증명이 아니다.
- 시공 PDF32 행10의 TC03 위치 FN-01과 PDF58 행8_18의 UC-01이 상충한다. 같은 케이블 이름을 근거로 한쪽을 임의 정정하지 않는다.
- 추가 상충: PDF32의 8_4 케이블은 CORE12, PDF58의 8_4는9G로 기재된다. 현행 심수로 어느 한쪽을 선정하지 않는다.
- PDF58의 8_5/8_7/8_8 행은 실제 렌더에서 검게 가려져 있다. 텍스트 추출에 남은 행 내용을 유효 배선으로 되살리지 않는다.
- P&ID PSH02 `+0.2mBar`, TC03 `550–610°C` 표기는 과거 도면 설계문구다. 현행 보호설정·안전 한계·조정 권고가 아니다.

### 공유 근거 재사용과 이번 고유 확인

[TC03 초안](TC03-DOTS-DRAFT.md)의 계측 채널/알람/전기 경계, [PV02 초안](PV02-DOTS-DRAFT.md)의 게이트 제어, [RD01 초안](RD01-DOTS-DRAFT.md)의 드럼 제어, [RO03 초안](RO03-DOTS-DRAFT.md), [PSH02 초안](PSH02-DOTS-DRAFT.md), [PV05 초안](PV05-DOTS-DRAFT.md), [PV06 초안](PV06-DOTS-DRAFT.md)을 같은 고정 원본의 공유 참조로 연결한다. 주변 설비의 조건·타이머·안전 로직을 UC01 고유 항목으로 복제하지 않는다. 이번에는 UC01 P&ID 위치·시공 위치/케이블 및 검색 범위를 직접 확인하고, TC03 호출/선언 일부를 소유 분리의 교차증거로만 독립 대조했다. 공유 상세를 모두 새로 의미 검토했다는 뜻이 아니다.

## 1. 설비·자료 기준

- catalog_id UC01, 이름 드럼 배출실, passive / 공정 본체, parent 없음, depth0, priority_key 없음, phase2/planned. INVENTORY catalog[34], equipment[9]. 로컬2차133 통합 제외 유지. 부모·하위·별칭을 함께 완료로 세지 않는다.
- 고정 원본 `gme-research/source-mv06`, commit `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, v1.12.0. 사용자 보고 최신 게시판이나 현재 CPU를 검증한 것이 아니다.
- 배치10 지시/범위 및 overlap의 UC01 행, AGENTS, 저장소 스킬·source-map, 작업표준/템플릿/INVENTORY/START-GPT61, 버전/인계/게시/ACTIVE/확장 기록의 최신 항목을 읽었다. 배치의 제한된 문서조사 지시를 적용한다.
- 실행 모델·추론 수준 런타임 증명 미확인. 로컬 TIA 추가 권한 없음. 새 Work/Codex/재위임/사용자 컴퓨터 접근 없음.
- 쓰기 범위: 이 초안과 `extracts/UC01/`만. 원본·공통 코드·버전·대장·배포·운영·SEJIN·PLC·현장·보호값 변경0. 시뮬레이터 작성/수정/생성/실행/행동시험0. 원본 build/test/generator 실행0.

| 영역 | 상태 | 범위 |
|---|---|---|
| 설비·자료 기준 | 적용 | P&ID 및 대장, 실제 설치 동일성 미확정 |
| I/O·HMI | 본체 전용 근거 미확보 | 한정 검색 및 관련 계측 소유 구분 |
| 제어 | 본체 전용 근거 미확보 | 공정 연결과 주변 제어 분리 |
| 전기 끝점 | 관련 위치 자료 적용 / 본체 고유 미확보 | 시공 케이블 양 끝 위치; 전용 I/O·단자 미확정 |
| 알람·복구 | 본체 전용 근거 미확보 | 관련 알람 연결, 실제 복구 미수행 |
| 증상 관찰 | 적용 | 비침습적 기록 계획; 실제 관찰·조작 없음 |
| 완료·누락 | 적용 | 문서/자체검사/제품/현장 상태 별도 |

### P&ID 판본과 공정 경계

원본 `all-in-one/sources/PID_1684n002I.pdf`, 실제 PDF1(총1쪽), 제목 UBC AND SCRAPS DECOATER 10 Ton/h / P&I, Drawing1684n002, Apex I. 표제 최초 날짜06/04/2011, 개정I 15/01/2013 `REMOVED MC-05, CHANGED POWER OF FN-02`, FG란 `-`다. FG를 임의 PDF-1로 만들지 않는다. PDF 메타데이터 작성일과 표제/개정일은 다른 정보다.

UC-01 본체 표기, RD-01과의 접속, 하부 PV-02 및 배출측 MC-04를 실제 렌더로 확인했다. 상부 가스 배관에는 RO-03/TC-03, PSH-02 취출과 PV-05/PV-06 `N₂ FOR EMERGENCY ONLY` 주입 표시가 있다. 선 교차의 점/점프 표시는 연결 여부 판단에 중요하며 공간상 인접만으로 모든 선이 연결되었다고 하지 않는다. 질소 주입을 UC01 자체 자동비상 시퀀스나 안전 승인으로 해석하지 않는다. 도면상 흐름과 실제 운전 흐름·누설·내부 기구·재질·씰 구조는 별도다.

## 2. I/O·HMI와 한정 검색

검색 정규식은 대소문자 무시 `(?<![A-Za-z0-9])UC[ _-]?0?1(?![0-9])|unload.{0,20}chamber|camera.{0,20}scarico`이다. decoded-original XML695개, live_index.json/hmi_plc_tags.csv/hmi-windows.csv/block_summary.json/existing-website-manual.md 5개를 검색했고 일치0개였다. 파일별 검색 결과는 `extracts/UC01/search.json`이다.

이 검색은 텍스트 철자 검색이다. 바이너리 백업 전체 해석, 별칭 전수 확인, 현재 프로젝트/CPU, 외부 제어기, 현장 로컬 계측 전체를 조사한 것이 아니다. 695개 XML 검색을 695개 논리 의미 검토로 쓰지 않는다. UC01의 전용 입력/출력·HMI 명령·설정·내부 상태·타이머 주소는 현재 근거 미확보다. 이름이 없는 공통 DB·가공 상태·화면 객체로 표시될 수 있으므로 본체 HMI가 없다고 단정하지 않는다.

기존 `devices/UC01.html`, `control-specs/UC01.html`, `procedures/UC01.html` 역시 직접 태그/원본 경로를 미식별로 표시하는 파생 자료다. 그 0개 표시를 물리 장치 부재나 무알람 판정으로 확대하지 않는다. 기존 시뮬레이션 설계/검증 항목 문구는 과거 자료이며 영구 중지 정책에 따라 재개하지 않는다.

### 관련 TC03 채널의 원본 교차증거: UC01 전용 신호가 아님

다음은 원본 `all-in-one/sources/decoded-original/` 파일들이다.

| 선언 | 실제 원본 위치 | 해석/경계 |
|---|---|---|
| TC03 원시 입력 | 0678 SimpleAccess Global RID76, NID11 UID364, Int, AO2208, Input/SAM Peripherie | IW276:P 직접 주변장치 접근. UC01 전용 입력으로 이름 변경 금지 |
| Data.Temp_TC03 | 0676 Global RID79, NID11 UID367 AK=Write, Int, AO896, BIRID11;0674 RID11 TOD N1 | DB1.DBW112, 환산 결과 Int 쓰기. 입력 원시 Word/HMI 미러와 다름 |
| Allarm.TC03_OFR | 0676 Global RID377,NID11 UID23 AK=Write,Bool,AO172,BIRID354;0674 RID354 TOD N3 | DB3.DBX21.4 단일 bit 쓰기. UC01 본체 경보 아님 |
| Coeff.COEFF_TC03 / ZERO_TC03 | 0676 Global RID77/78,NID11 UID365/366,Int,AO176/160;0674 RID8 TOD N4 | DB4.DBW22/20 읽기. 현재 계수·제로가 아님 |

단어 전체를 옮기는 공통 HMI/DB 전달과 이 bit/Int 쓰기는 구별한다. 위 항목들은 Global 선언이며 UC01 Local 선언을 새로 만들지 않는다. AO는 비트 오프셋이고 단순 숫자를 DB byte 주소로 오독하지 않는다. HMI 실제 이벤트·화면 주소·통신 신선도·현재 값은 미확정이다.

## 3. 제어 구조와 소유

UC01 본체의 요청→허가→출력→전달→응답, 자동/수동·기동·정지·리셋·상태전이·지연·복수 쓰기는 직접 결속 근거 미확보다. RD01 회전/투입 금지, PV02 A/B 게이트 기억/EV, 팬 기동이나 MV01·MV06 동작을 본체 로직으로 복사하지 않는다.

관련 TC03의 `0491-FlgNet.xml` NID11 원본은 다음만 직접 재확인했다. ORef362 ON(RID1)→W369→Part375 Contact.operand, Contact.out W376→CRef356.en. 별도 ORef363 ON→W370→356.IN0. ORef364 TC03→W371→Analog_input, ORef365/366→W372/373→Coeff/Zero, CRef356.OutValue→W374→ORef367, Out_of_range→W24→ORef23다. CRef356 RefId351, 내부 CodeBlock368 RefId5는 호출 참조이며 UC01 선언이 아니다. ON은 이름으로 현재 TRUE를 보장하지 않는다.

공통 선형화의 ENO·정수 환산·범위이탈과 내부 IN0 반전, LOW/HIGH/MAX_MAX 알람의 S/R·히스테리시스·타이머는 [TC03 초안 3/5영역](TC03-DOTS-DRAFT.md)에 연결재사용한다. 이번 본체 문서에 별도 타이머·환산식·S/R을 창작하지 않는다. P&ID의 계측 표시나 과거 설정문구가 PLC 타이머/조건의 근거는 아니다. 동일 UID도 다른 선언/NID 문맥과 혼합하지 않는다.

## 4. 전기 끝점·실제 렌더

직접 UC01 I/O/릴레이/퓨즈/단자 양 끝점을 입증한 OEM 회로는 이번 본체 범위에서 미확보다. 아래는 위치가 UC01인 관련 회로의 시공 근거이며 본체 소유표가 아니다.

| 원본 Electrical_Can_Decoating_20241118.pdf | 실제 렌더 확인 |
|---|---|
| PDF3, CANDC-CONS-S003-003, D-PAGE3, 3/64 | SETTING THE CONSTRUCTION AREA. FLOW_B UC-01 행: PSH02/PV05·06/TC03/RO03; ROT1TB1/FLO3TB1/FLO4TB1/NVBOX/81RO03 위치 목록. 모터 칸으로 UC01 전용 모터를 식별하지 못함 |
| PDF5, CANDC-CONS-S005-005, D-PAGE5,5/64 | CONTROL AND SENSOR MAP. FLOW_B UC-01의 센서/솔레노이드 목록을 재확인. RD01/PV02는 ROTARY 위치의 다른 행 |
| PDF32, CANDC-CONS-E015-032, D-PAGE15,32/64 | FLOW B ROUTE CONDUIT PIPING(2). 행10 TC03,LOC FN-01,케이블8_18 `=FLB+UC01-TC03A`,KX1.0/2심. 행2 Delete 표기는 보존 |
| PDF58, CANDC-CONS-C008-058, D-PAGE8,58/64 | CABLE SCHEDULE(7). 아래 양 끝점/케이블, 가려진 행을 구분 |

네 페이지 하단 모두 Rev1 24.11.11 `first draft design`, CHECKED/APPROVED 공란을 실제 렌더로 확인했다. 파일명20241118과 개정표 날짜를 같은 날짜로 치환하지 않는다. 준공 승인도나 현행 실측 자료라고 표현하지 않는다.

PDF58 관련 위치 연결의 제한된 상세:
- 8_1 `=FLB+UC01-NVBOXA`: CR→UC-01/NVBOX,POWER(220V),AC CVV3G1.5. 8_2/8_3은 같은 위치 NVBOX의96KA3 Contact/96KA2 Contact, AC/DC 별도 경로다. 기재가 본체 고유 출력 또는 실물 릴레이 접점 핀을 증명하지 않는다.
- 8_10 `=FLB+UC01-PSH02A`: CR→UC-01/PSH-02,AI CVV-S4S1.0,spare1,route100→120RBD1→E800,LEN55.
- 8_11/8_12: CR→UC-01/81RO-03,각 AI CVV-S2S1.0 / AC CVV3G1.0,LEN61. 신호/전원은 별개다.
- 8_13 `=FLB+UC01-FLO3TB1A`: UC-01/NVBOX→UC-01/FLO3TB1,PV05/06,AC CVV7G1.0. 8_14/15는 FLO3TB1→PV05/PV06,각 AC CVV3G1.0. 두 밸브와 위치가 같다고 하나의 실물로 병합하지 않는다.
- 8_18 `=FLB+UC01-TC03A`: CR→UC-01/TC-03,TC KX2S1.0,spare0,route100→120RBD1→E1000,Adjustment8,LEN59. PDF32 LOC와 상충을 유지한다.
- 8_25 `=FLB+81RO03-RO03A`: UC-01/81RO-03→UC-01/RO-03,AI CVV-S4S1.0,route의 `?` 보존. 누락 경로를 추정하지 않는다.

LEN은 설계 표 값이고 실측 길이가 아니다. TC/KX구간과 TC03 OEM4–20mA 송신기 구간은 [TC03 초안 4영역](TC03-DOTS-DRAFT.md)으로 연결하되 본체 단자로 복제하지 않는다. 릴레이 부하5/9·하단접점표1/5/9를 이 시공 Contact 문자만으로 채울 근거가 없다. 현재 보호값·단자 극성·계기 형식·센서 설치/보상선·방폭/기밀 등은 미확정이다.

## 5. 알람·복구

UC01 이름으로 직접 결속한 전용 알람·Reset·재기동 허가를 확보하지 못했다. TC03 온도/OFR, RO03 산소, PSH02 압력, PV02·질소밸브·팬 관련 경보는 각각의 소유와 공통 소비를 별도로 확인해야 한다. 위치코드 UC-01에 연결된 기기가 많다는 이유로 모든 경보를 UC01 알람목록으로 만들지 않는다.

알람 소거·HMI ACK·STOP_HORN·래치 Reset·물리 원인 소멸·안전 재시작·현장 복구는 서로 다르다. P&ID의 N₂ FOR EMERGENCY ONLY가 자동 질소주입의 충분조건, 복구 또는 정상상태를 증명하지 않는다. 본체 리셋 절차·인터록 우회·강제 출력·보호값 조정·운전 시험은 제공하거나 실행하지 않는다.

## 6. 증상별 읽기 전용 관찰 계획

아래는 문서/기존 관찰자료 비교 계획이며 현장 접근·개방·탈거·회로 주입·조작 지시가 아니다. 실제 관찰자·시간·값·사진은 아직 없다.

| 증상/질문 | 함께 남길 근거 | 판정 경계 |
|---|---|---|
| 배출 정체 의심 | UC01 위치 사진/명판, RD01 출구/PV02/MC04 연결, 최초 시각, 각 설비의 요청/출력/피드백·경보 이력 | 챔버 막힘, 게이트 미동작, 후단 정체는 후보로 분리. 명령비트만으로 실물 개방 판정 금지 |
| 온도/압력 이상 또는 누설 의심 | 계기 태그·위치·시간/단위·갱신시각, TC03/PSH02 측정자료와 현재 승인 P&ID | 과거 설계문구를 안전 정상값으로 사용 금지. 본체 결함과 계측 고장을 구분 |
| 질소/산소 관련 경보 | PV05/06·RO03·NVBOX의 개별 태그/이력, 승인된 경보/원인대응표 | UC01 자동 복구 로직 발명 금지. 질소 질식 위험·공정 안전은 승인 현장 절차로 판단 |
| HMI UC01 표시와 도면 불일치 | 실제 화면 이름·객체/주소 매핑·버전, 현재 PLC 프로젝트 식별 | 가공/공통 표시일 가능성과 전용 I/O를 구분 |
| TC03 위치가 서로 다름 | PDF32 행10/PDF58 행8_18, 최신 승인 배선도와 현장 태그 증거 | FN01↔UC01 어느 쪽도 추정 정정 금지 |

관찰 양식: 관찰자, 실제시각/시간대, 위치·태그·주소, 값/단위·신선도, 수집장치, 도면/프로젝트 버전, 비교 근거, 원인배제 결과, 승인 조치, 별도 복구증거. 실제 운영 자료나 SEJIN 기록을 복제하지 않았다.

## 7. 완료·누락·검증

| 구분 | 상태 |
|---|---|
| documentation | draft_complete_with_gaps; UC01 한 개 7영역, 소유·미확보 기록 |
| static_review | 한정 텍스트검색·고유 PDF5쪽 실제 렌더·관련 XML4파일 일부 의미 대조·선정 SHA/Git blob 확인; 부모 독립검토 대기 |
| ui_records | not_run; 화면·저장·재읽기·재열기·네 도구 구현 미검증 |
| publication | not_published; 이번 제품 통합/게시 없음 |
| tia_compile / live_cpu / field_recovery | 각각 not_performed |

도면·래더 비교는 원본 링크/문서 대조만 수행했다. 선택 백업복원, 기록 전후비교, 관찰 보고서/PDF의 실제 UI 기능은 이번에 구현·검증하지 않았다. BC01 동등 기능완료라고 쓰지 않는다. 이번 PDF 렌더는 근거 원본 열람이지 관찰 보고서 제품기능 검증이 아니다.

필요 자료와 재개 조건:
1. UC01 명판/위치/출입구·RD01/PV02/MC04 접속이 확인되는 승인된 최신 배치/기계도 및 비침습적 현장 식별 자료.
2. 현행 UC01 별칭·공통 기능을 포함하는 PLC 심볼/블록 교차참조 및 HMI 객체/주소/이벤트 매핑. 현재 CPU와 백업 비교 증거.
3. 최신 승인 전기·케이블·접속함/단자대 도면. 특히 TC03 위치 상충, 가려진/삭제 행의 개정 이력, RO03 경로 `?` 해소 자료.
4. 본체 제작사/검사 자료: 재질·씰·허용 조건·정비와 접근 기준, 승인된 경보/원인대응/안전 복구 절차. 현행 보호값을 추정 입력하지 않는다.

새 자료 없이 실물 보류 전검색을 반복하지 않는다. 다음 단계는 부모의 문서 독립검토와 필요한 자료 수집이다. 사용자 전송/첨부는 부모가 수행한다.

### 검사와 실제 단계 시각

자체 스크립트는 XML파싱·텍스트검색·해시/고정Git blob 비교·PDF렌더만 수행했다. 712개 `all-in-one/sources/` 파일의 바이트 보존 검사는 전체 논리 의미 검토가 아니다. XML검색695개+보충5개, 선정 근거17개, 관련XML4개 부분 의미검토, PDF5개 실제페이지(확대이미지는 별도페이지로 세지 않음)를 구분한다. 원본 전체 저장소의 보존 판정은 Git 상태와 함께 확인한다. 세부JSON은 `extracts/UC01/search.json`, `selected-source-hashes.json`, `preservation.json`, `self-check.json`, `stage-times.json`이다.


| 실제 단계 | UTC |
|---|---|
| assignment_received | 2026-10-11T11:35:39Z |
| instructions_and_identity_read | 2026-10-11T11:35:58Z |
| PDF_render_generated | 2026-10-11T11:36:37.429561+00:00 |
| PDF_five_pages_and_title_visually_reviewed | 2026-10-11T11:36:52Z |
| bounded_search_and_hash_completed | 2026-10-11T11:37:48Z |
| draft_seven_areas_written | 2026-10-11T11:40:28Z |
| final_self_check_started | 2026-10-11T11:41:02.654486+00:00 |

## 선정 근거 전체 SHA256 · 고정 Git blob 목록

아래17개는 이번 선정 근거 전체다. 모든 SHA256은 현재 읽기전용 파일, blob은 위 고정 커밋의 객체이며 내용일치=true를 확인했다. XML695개 검색목록은 search.json, sources712개 보존목록은 preservation.json에 별도 보존한다. 해시 수를 의미검토 수로 해석하지 않는다.

| 원본경로 (source-mv06 기준) | SHA256 | Git blob | 내용일치 |
|---|---|---|---|
| docs/equipment-standard/INVENTORY.json | 720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc | 587c3748ad9224718f95ba06463fee913dae231d | true |
| all-in-one/registers/equipment.json | 7870325dff32bbca90fa34507b301c4aad3347d669fddcd03b910343663996fa | acc42633033398216469064932c4b76987371606 | true |
| all-in-one/sources/PID_1684n002I.pdf | 2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b | 8c83a59fefd5b8b651ec3537ea4236a073f5e109 | true |
| all-in-one/sources/Electrical_Can_Decoating_20241118.pdf | 3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd | 0ee6b6f8361c5790864dbba4bbd9d55e8e7c08f8 | true |
| all-in-one/sources/can-decoating-page-text.json | d3b4c14945dd00f79c58ebab0cb8991c422dd1670e95e24d10779bd9e9d99bba | 2bebec2c719fa57ed6c9f8d4e541e8848dc0d732 | true |
| all-in-one/sources/live_index.json | 14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1 | e35ccea1f841349c632666c29954b7bcd4f5839e | true |
| all-in-one/sources/hmi_plc_tags.csv | a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404 | cf4c0650e7c7baac350dcb89909b808435704880 | true |
| all-in-one/sources/hmi-windows.csv | 15f8d69b5c43d4fdbe550f9cd2717f855fea877ed8146973054cb6dbcaa9892e | 8401dcfe5ba3e7e244eea0f501bb84a2e387da39 | true |
| all-in-one/sources/block_summary.json | 68253f9366908244a27ed461c66d465da7ec1723571f27deaa9a6f81a542de63 | 15b570a011645023dbfca2d5332a9e0ae3b0a7b6 | true |
| all-in-one/sources/existing-website-manual.md | 3a758744dfece259ed883c5d9968b00c37cd78bb422eb07b6c23d3384a4b56cd | 36e82a78aed1fcc5f59c187df4c476ed4bd82e83 | true |
| all-in-one/sources/decoded-original/0491-FlgNet.xml | f7395b1dc4f33553114a108c61691cb24b830d2152b31e6e9cd9f7718ecc9b1d | a2eb014c107e824cd0ab6285d61b70ce4f03781a | true |
| all-in-one/sources/decoded-original/0674-IdentXmlPart.xml | 4770702f519bacda69202bb2f7733d983074bda90964360c238f990d9d08fd84 | f210593944547b63eab10c667348711413600aab | true |
| all-in-one/sources/decoded-original/0676-IdentXmlPart.xml | c58427c5b0ac6c11cdb52e4c6d0461c7b191fae81ccace191048e9f175fcec59 | 1ed67265f69796a4e659f9438e551068037f33a4 | true |
| all-in-one/sources/decoded-original/0678-IdentXmlPart.xml | 51e637e0b9713c028810f2a717b5c3804a3a26c2f1be7e332a4d6bf277bfc382 | 7fafb2297bcdf739bf1d1dd68cebc0d74f2a40cc | true |
| all-in-one/devices/UC01.html | 3207755ac7ac89f94bef10644e3bb2524b8460f9ab5f77e41a639fb31f2efb4e | 6b25ccbb6258b9f542ea060f15017c5301f36b8c | true |
| all-in-one/control-specs/UC01.html | 1283d3d10c1648b937027937b38acb26e42f746d08522bcec0d73d09da9897da | 90f878cf20fbee5be6cd26246eb6adf5d6f4f008 | true |
| all-in-one/procedures/UC01.html | 04256a6cb1bc782912b3382cb7bc8a8702e373ecccd4881f081cc88a7330b3f5 | 2cb8e68361c4d4dca4916c0f4cb966c5828dea14 | true |

### 영구 중지5자산 보존 확인

내용을 실행·변경하지 않고 해시만 대조했다.

| 원본경로 (all-in-one 기준) | SHA256 | 고정 Git blob | 동결해시일치 |
|---|---|---|---|
| registers/program-model.json | 6203479c086b15bada12ac9d7e37db9280234ec26f1ea6091d7211dc09a577c5 | 9860b10f008d3a5ae714be50d77b703dfec32f3a | true |
| assets/program-model-data.js | 52f8199371e3399b7c0d44ab5469f0472aced79d56bbef2887f7625f5d2aff0f | 38f34b0caa380a16ccad6f6f1e234a2fdf23f327 | true |
| assets/virtual-plc.js | 5f1876052dc0067b1f010af0dfc941946e37003167481731293615d9c1c36dbc | 0bd9eceb54365a91214a37c5601b5067c39a3f75 | true |
| assets/simulator-workspace.js | 3a6dfc618ff7e7b238f2671dc85d65704f33093a18eac879d86081d92c31e8bc | 97c2c831c77a9699fff0e0960b3bc1b7d93d45b3 | true |
| registers/virtual-plc-test-results.json | a6b389f797f9a8b5ffe6928b8420f55c4cc459a327b0b48d716079d2eca6dd64 | 757dd50e45184568facb8ff62900b39d3ce848d1 | true |
