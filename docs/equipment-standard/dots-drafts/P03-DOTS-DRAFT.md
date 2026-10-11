# P03 웨잉호퍼1 식별 조사 초안


## 결론

**P03의 catalog_id는 미배정, mapping은 unknown, identity_verified는 false로 유지한다.** 고정 원본에서 CLIENT-CL17은 ‘호퍼2 고장’ 입력이며, BWF01·BWF02는 외부 피더의 별도 신호 집합이다. 어느 것도 사용자가 부르는 ‘웨잉호퍼1’과 실물 일대일 대응된다는 근거가 없다. 이 문서는 후보를 구별할 수 있도록 작성한 식별 조사 결과이며, P03을 세 후보 중 하나에 배정하거나 후보별 표준 매뉴얼을 작성 완료한 결과가 아니다.

확인된 중요한 구분은 다음과 같다.

- Electrical_Rev2.pdf FG94/PDF95와 FG132/PDF133은 **E16.4 = WEIGHTING HOPPER 2 FAULT**로 일치한다. PLC 원본 선언도 **WEIGHTING HOPPER 2FAULT / Input / AO132 = %I16.4**다. CLIENT-CL17의 근거를 ‘호퍼1’로 이름만 바꾸어 사용할 수 없다.
- BWF01에는 %Q6.2 원격 기동 허가, %I11.1~%I11.5 상태·고장·레벨, %IW264 유량, %IW268 레벨, %QW298 유량 속도 설정의 서로 구분되는 자료가 있다. BWF02에도 별도 채널이 있다. 호퍼 관련 기능은 지지하지만 P03의 실물 번호·제어 주체는 확정하지 않는다.
- P&ID 원본 1쪽을 회전 렌더하여 전체와 원료 투입 영역을 시각 확인했다. BC01 → PV01 → CC01/RD01 관계와 ‘PARAMETERS COMING FROM BUYER’S MACHINES’ 표기는 보이나, 해당 도면에서 ‘웨잉호퍼1’ 또는 BWF01/02와 연결되는 실물 태그를 확인하지 못했다. 무명 기호나 외부 경계 표기를 P03으로 지정하지 않는다.
- 시공도는 ‘FOR APPROVAL’, ‘24.11.11 first draft design’인 자료다. 전체 64쪽의 추출 가능 텍스트에는 hopper/weigh/weight/BWF/호퍼/계량이 없고, 시각 확인한 배치·ENTRY·케이블표에서는 BC01/PV01/CC01/RD01 등의 위치와 케이블만 확인됐다. 이것은 **이 자료에서 연결 근거를 확보하지 못했다**는 의미이며, 현장에 호퍼가 없다는 뜻이 아니다.


## 작업 기준과 보존 범위

- 표준: GME-STD-1.0.0, WORK-STANDARD.md 및 WORK-ITEM-TEMPLATE.md의 7영역
- 작업: phase1 / 미확정 우선행 식별 조사
- 대상: priority_key P03, 원래 이름 ‘웨잉호퍼1’, catalog_id null
- 검토 후보: CLIENT-CL17, BWF01, BWF02. CLIENT-CL18은 인접 배출컨베이어와 혼동을 막기 위한 경계 참조만 수행
- 고정 소스: v1.12.0 / abcf31c5030bc7ef8749ed8e869a857f2387a28a
- 자료 루트: ../source-mv06/ (이 문서 기준 상대경로)
- 조사·기록 일자: 2026-10-11 UTC
- 실행 모델·추론 수준: 실제 런타임 모델 설정의 독립 관측 근거 없음. 저장소의 요청 모델을 실제 사용 확인으로 기재하지 않음
- 작업자: P03 식별 조사 담당. 독립 최종 검토: 2026-10-11 핵심 근거 제한 범위 대조 완료; 실물 식별은 미확정
- 수정 범위: 본 초안과 ../extracts/P03/ 내부의 텍스트·XML 추출, PDF 렌더, 해시·정적 검증 기록만 생성
- 원본 저장소, 공통 코드, 대장, 버전, 배포·운영 기록은 변경하지 않음
- 시뮬레이터 작성·수정·생성·실행·행동 시험 없음. 실제 PLC·현장·보호값·SEJIN 운영자료 변경 없음


## 7영역 적용표


| 영역 | 판정 | 이번 작성 범위 | 남은 경계 |
| --- | --- | --- | --- |
| 설비·자료 기준 | 적용, 실물 대응 근거 미확보 | 후보별 근거·반증, P&ID·시공도·부모/하위 관계 구분 | P03의 실물 태그와 호퍼 번호, 외부 제어반 소유자 |
| I/O·HMI | 적용, P03 귀속 근거 미확보 | 후보의 원본 선언 주소·자료형, HMI 설정 주소 구분 | 후보의 신호를 P03 신호로 표시 불가. HMI 실제 이벤트·현행 바인딩 미검증 |
| 제어 구조 | 적용, P03 귀속 근거 미확보 | CLIENT-CL17 고장 Set/Reset과 BWF 원격 허가의 정적 경계 | 외부 계량기 내부 제어·로드셀·배출 순서 미확보 |
| 전기 전달 경로 | 적용, 외부 측 끝점 근거 미확보 | GME 도면 단자·모듈·신호 대응 및 시공도 탐색 | 외부 반의 상대 단자·케이블명·호퍼1 실물까지의 연결 |
| 알람·복구 | 적용, P03 귀속 근거 미확보 | 호퍼2 원시 고장과 GME 기억 알람의 분리 | 현행 원인·정상 극성·실제 복구 및 P03 알람 소유 |
| 증상별 수리 | 적용, 식별을 위한 관찰 항목만 | 혼동 원인 배제를 위한 자료 수집 표 | P03 식별 전 부품 교체·설정 변경·재기동 처방 불가 |
| 완료 기준 | 적용 | 식별 확정 조건, 부족 자료, 검토·게시·현장 상태 분리 | unknown 해제 증거 미확보 |

‘근거 미확보’를 ‘비해당’으로 바꾸지 않는다. 외부 기계라는 후보 분류만으로 P03의 직접 I/O나 고장 기능이 비해당이라고 판단하지 않는다.


## 1 설비와 후보 동일성


### 1.1 후보별 지지와 배제 근거


| 후보 | 지지하는 자료 | 현재 배정을 막는 자료·공백 | 판정과 추가로 필요한 자료 |
| --- | --- | --- | --- |
| CLIENT-CL17 | 원본 입력과 전기도면 모두 호퍼 고장 신호. 대장 이름 Weighing hopper 2, 별칭 motor_client_17 | 원문은 번호2이고 P03은 번호1. 호퍼 본체·계량 제어·기동·중량값은 이 채널에서 확인되지 않음 | **P03으로 자동 배정 배제, 실물 후보 자체는 미확정 유지.** 번호 변경/통칭 대응표와 X1 350/351의 외부 상대 단자·호퍼 명판 필요 |
| BWF01 | 외부 피더용 원격 허가·유량·레벨, PLC 선언의 COEFF_BWF1_HOPPER_LEVEL 등 계량/호퍼 관련 기능 근거 | ‘01’과 ‘호퍼1’의 동일성, 호퍼 본체/피더/컨베이어의 설비 경계, P&ID 실물 위치가 연결되지 않음 | **기능 후보 지지, 동일성 미확정.** BWF01 외부 장비 명판·제어반 I/O표·배치도에서 호퍼1 대응 필요 |
| BWF02 | BWF01과 구분되는 외부 피더 I/O와 호퍼 레벨 계수. 원료 이송 제어와 관련 | ‘02’가 장비 번호/라인 번호인지 불명. P04·CLIENT-CL18과도 후보가 겹침 | **기능 후보만 유지.** BWF02·호퍼1·배출컨베이어의 관계를 제어반 도면·물리 배치로 확인해야 함 |
| CLIENT-CL18 | 인접한 호퍼 컨베이어2 고장 %I16.5, 별도 Allarm.motor_client_18_fault | 호퍼 본체와 다른 신호. N425 제목의 ‘bwf02’만으로 BWF02나 P04 동일성 확정 불가 | **P03 본체 직접 배정 근거 없음.** 인접설비 경계로만 참조하며 P04 담당 조사와 공유 |

이 표의 ‘배제’는 **현재 자료만으로 하는 자동 대응을 배제**한다는 뜻이다. 현장 번호가 바뀌었다는 승인 자료가 향후 나오면 재검토할 수 있으며, 후보 ID를 대장에서 영구 삭제하지 않는다.


### 1.2 원본 대장과 부모·하위 관계

- INVENTORY.json의 P03: catalog_id null / mapping unknown / identity_verified false / queue_state identity_review. priority-equipment.csv 4행도 같은 상태다.
- BWF01, BWF02, CLIENT-CL17, CLIENT-CL18은 현재 대장에서 모두 parent 없음·depth0·kind client다. 이 네 ID를 부모/자식으로 연결하는 원본 catalog 관계는 없다. 네 ID를 부모로 갖는 catalog 하위 항목도 발견되지 않았다.
- BC01, PV01, CC01, RD01은 각각 별도 catalog ID다. P&ID의 물질 흐름·근접 배치와 대장의 parent 필드는 다른 관계다. P03을 BC01의 부품, CC01의 다른 이름, PV01의 호퍼로 추가하지 않는다.
- P&ID의 PV01 상세 CL01~04는 공압 실린더 이름 공간이다. 외부 채널 CLIENT-CL17의 CL을 공압 실린더 번호와 합치지 않는다.
- 전체 중복 대조 보고서가 정한 P03/P04/P14 후보9개 보류는 유지한다. 이번 조사는 P03→ID 대응을 새로 확정하지 않았으므로 132 연구분모·9개 보류·우선/신규 고유 ID 집계 변경 근거가 없다.


### 1.3 P&ID와 시공도 시각 확인


| 자료 | 실제 확인 위치 | 확인 사실 | 해석 한계 |
| --- | --- | --- | --- |
| PID_1684n002I.pdf | PDF1 전체, 회전 렌더의 좌하 원료 투입 영역 | BC01/M02가 PV01 쪽으로 이어지고 CC01/RD01 투입부가 따로 표시됨. 외부 기계 파라미터 상자가 존재 | 그림에 없는 BWF·호퍼 번호를 외부 파라미터 기호에 임의 대입하지 않음. 텍스트 추출 0문자이므로 검색 불일치를 부재 근거로 쓰지 않음 |
| Electrical_Can_Decoating_20241118.pdf | PDF1 표지, PDF2 색인 | FOR APPROVAL, 첫 초안 설계 24.11.11. 완공/준공 승인 증거 없음 | 파일명 20241118과 표지의 24.11.11을 같은 날짜로 덮어쓰지 않음 |
| 같은 시공도 | PDF3, CANDC-CONS-S003-003 | ENTRY/ROTARY 등 구역과 BC01, PV01, CC01, RD01 등의 목록·배치 | 외부 피더와 P03의 번호 대응 미확보 |
| 같은 시공도 | PDF21, CANDC-CONS-E004-021, ENTRY ROUTE CONDUIT PIPING (1) | BC01 M02, ENT1TB1/2, PV01 LS01/02·EV01 등의 배관/케이블표 | BC01 M02 케이블을 P03 계량기 또는 배출컨베이어 케이블로 복제하지 않음 |
| 같은 시공도 | PDF51, CANDC-CONS-C001-051, CABLE SCHEDULE (1) | 1_1 =ENT+BC01-M02A는 CR→BC01 M02, FEEDING ROTATION DRUM CONVEYON 표기 | P03 외부 반의 상대 단자·로드셀·계량제어기 도면이 아님 |

시공도 전체 64쪽 텍스트 검색은 101,742문자 범위에서 위 후보명/호퍼 관련 검색어 0건이다. PDF1·2·3·21·51은 실제 렌더로 확인했다. 모든 페이지를 시각 전수 검토했다고 주장하지 않는다.


## 2 후보 I/O와 HMI 경계


### 2.1 직접 PLC 선언으로 확인한 구분

원본 XML 경로는 all-in-one/sources/decoded-original/ 아래다. AO는 선언의 bit offset이며 Bool은 byte.bit, 16비트는 byte 주소로 풀었다. SAD의 Input/Output/Memory, SAM Peripherie/None도 별도 속성으로 보존한다.


| 대상 | 원문 이름 | 주소·형식 | 원본 선언 위치 | P03 관련 해석 |
| --- | --- | --- | --- | --- |
| CLIENT-CL17 후보 | WEIGHTING HOPPER 2FAULT | %I16.4, Bool, Input, AO132 | 0599, RID38, NID17 UID341/343 | 호퍼2 고장 입력. P03 실물 대응 없음 |
| 인접 CLIENT-CL18 | HOPPER CONVEYOR 2FAULT | %I16.5, Bool, Input, AO133 | 0599, RID40, NID18 UID359/361 | 별도 컨베이어2 고장 입력 |
| BWF01 | BWF01 OK / BWF 01 RUN / BWF01 FAULT / min LEV BWF01 / MAX LEV BWF01 | %I11.1 / .2 / .3 / .4 / .5, 각 Bool | 0558, RID19~23, AO89~93 | 도면은 I11.1을 MANU STATUS라고 부름. ‘OK=자동허가’로 정상 의미 단정 금지 |
| BWF02 | BWF02 OK / BWF 02 RUN / BWF02 FAULT / min LEV BWF02 / MAX LEV BWF02 | %I11.6 / .7 / %I12.0 / .1 / .2, 각 Bool | 0558, RID24~28, AO94~98 | I11.6도 도면 MANU STATUS와 PLC OK 명칭 차이 보존 |
| BWF01 | Consent Start BWF01 | %Q6.2, Bool, Output, AO50 | 0602, RID26, NID3 UID125 AK Write | 외부 피더 원격 허가 출력. 호퍼 모터 직접 출력으로 바꾸지 않음 |
| BWF02 | Consent Start BWF02 | %Q6.3, Bool, Output, AO51 | 0602, RID32, NID4 UID163 AK Write | BWF01과 다른 출력 |
| BWF01 | BWF01_FlowRate / BWF01_Level | byte264 / byte268, Int 입력, AO2112/2144 | 0678 RID30 NID5 UID216 / RID56 NID7 UID284, SAM Peripherie | 유량/레벨 명칭이다. 로드셀 원시 중량 또는 kg로 확정하지 않음 |
| BWF02 | BWF02_FlowRate / BWF02_Level | byte266 / byte270, Int 입력, AO2128/2160 | 0678 RID46 NID6 UID291 / RID61 NID8 UID304, SAM Peripherie | BWF01의 채널·환산·단위를 복제하지 않음 |
| BWF01 | BWF01_SP_FlowRate | byte298, Word 출력, AO2384, SAM Peripherie | 0664 RID17, NID3 UID260/334 AK Write | 도면 PAW298, 검색표 %QW298. 실제 출력 범위·속도 물리단위 미확정 |
| BWF02 | BWF02_SP_FlowRate | byte300, Word 출력, AO2400, SAM Peripherie | 0664 RID34, NID4 UID296 / NID5 UID405 AK Write | 원본에 쓰기 참조가 여러 개 존재. 단일 경로라고 단정하지 않음 |

0678의 원시 아날로그 참조와 0627의 HMI 입력 전달 참조는 SAM이 일부 다르다. 예를 들어 BWF02_FlowRate와 두 Level 참조는 0627에서 SAM None, 0678에서 Peripherie다. 같은 바이트 번호라도 주변장치 직접 읽기와 다른 참조의 읽기 방식을 없애지 않는다. 현재 실행 호출·CPU 값·원시 디지털 입력의 Inputs 구조체 전달을 이번 식별 초안에서 검증 완료하지 않았다.


### 2.2 내부 상태와 원시 입력

- Allarm.motor_client_17_fault는 0601의 GlobalAccess, RID39, Allarm 내부 AO129, Bool이다. NID17의 UID342/345가 Write다. 원시 Input AO132와 다른 주소 공간이다.
- Allarm.motor_client_18_fault는 같은 파일 RID41, Allarm 내부 AO130이다. 다른 채널로 보존한다.
- Flag.M_BWF01 및 Flag.M_BWF02는 0604의 GlobalAccess이며 Flag 내부 AO96·AO101이다. 실제 운전 피드백이나 물리 출력 그 자체가 아니다.
- Inputs.BWF01 OK, Inputs.BWF02 OK, Inputs.BC01 run은 구조체 접근이다. 원시 I주소와 이름이 비슷하다는 이유만으로 전달 완료나 현재 정상 상태를 가정하지 않는다.
- ‘ON’은 0599에서 Memory Bool AO0로 선언된다. 명칭만으로 모든 조건에서 참이라고 축약하지 않는다.


### 2.3 HMI 설정에서 확인한 후보 이름

sources/hmi_plc_tags.csv의 후보 행은 dde.cfg에서 추출한 설정 자료이며 온라인 값이 아니다.


| 후보 | 설정 태그와 주소 | 위치 | 한계 |
| --- | --- | --- | --- |
| BWF01 | Editor_BWF01: DB26,INT8 | CSV59행 | 편집값의 적용 이벤트·실제 쓰기 경로 미검증 |
| BWF01 | Risposta DB11,X70.1 / StatusOK X70.0 / Allarme1 X70.2 / Flag DB2,X12.0 | CSV618~621행 | 이름을 P03 화면으로 치환하지 않음 |
| BWF02 | Editor_BWF02: DB26,INT10 | CSV60행 | BWF01과 별도 편집 설정 |
| BWF02 | Risposta DB11,X72.1 / StatusOK X72.0 / Allarme1 X72.2 / Flag DB2,X12.5 | CSV651~654행 | 이름만으로 외부 장치 동일성 입증 불가 |
| BWF01/02 | I_Level_BWF01 DB13,INT32 / I_Level_BWF02 INT34; I_Flow_rate_BWF01 INT28 / BWF02 INT30 | CSV733·735~737행 | 계량 단위·영점/교정값·실제 표시 이벤트 미확정 |

N1213/1214의 HMI 네트워크 0389/0390-FlgNet.xml은 존재하지만 현재 network-map의 resolved_operands가 비어 있다. RefId만 있는 원문을 이름으로 억지 결속하지 않는다. P03 전용 HMI 화면과 실제 버튼 이벤트는 근거 미확보다.


## 3 제어 구조의 식별 경계


### 3.1 CLIENT-CL17은 GME 측 고장 수신·기억 채널

N424, motor/alarm client, 0234-FlgNet.xml을 0599/0601 선언의 RID·UID·NID와 대조했다.


| 원본 연결 | 정적 해석 | 범위 |
| --- | --- | --- |
| Contact355(ON) → Contact357(원시 I16.4) → SCoil334; ORef340/341/342, Wire346/347/349/358 | ON AND WEIGHTING HOPPER 2FAULT이면 Allarm.motor_client_17_fault Set | 원시 고장 수신과 기억. 호퍼1 귀속 불가 |
| Contact355 → Contact359(operand Negated, 원시 I16.4) → Contact361(Flag.RESET_ALLARM) → RCoil339; ORef343/344/345, Wire350/351/353/360/362 | ON AND NOT 원시고장 AND RESET_ALLARM이면 같은 기억 Reset | 입력 해제와 리셋 요청이 분리됨. 외부 제어반 고장 원인 제거·재기동 완료를 증명하지 않음 |

해당 네트워크에서 타이머·기동출력·중량 측정·배출 시퀀스는 확인되지 않는다. 이는 이 네트워크의 기능 경계이며 전체 외부 호퍼의 제어 기능 부재를 뜻하지 않는다. 실제 외부 고장 접점의 정상 극성, 단선 시 반응, 상위 호출·다른 쓰기는 추가 증거가 필요하다.

N425/0235는 별도 %I16.5·motor_client_18_fault Set/Reset 채널이다. 제목에 bwf02가 들어 있으나 원본 선언의 주소·저장 필드는 CL17 및 BWF 별도 알람과 구분된다. 제목만으로 같은 설비로 병합할 수 없다.


### 3.2 BWF01·BWF02는 BC01 운전 등의 허가 조건을 참조

N1932/0239의 Part97은 OR6, Part109는 Flag.M_BWF01 Reset, Part113은 Consent Start BWF01 Coil이다. NID3의 0602/0604/0605/0606 선언과 대조했다.

- ON 아래 OR6 분기: Allarm.BWF01_FAULT, Allarm.BWF01_Fault_Control, Data.SET_PERC_BWF01 == Int 0, NOT Inputs.BWF01 OK, NOT Inputs.BC01 run, **Local** Disable_Load_RD01
- 이 OR 경로가 Flag.M_BWF01을 Reset하는 연결이며, 별도 ON → Flag.M_BWF01 Contact159 → Coil113은 %Q6.2에 쓰는 연결이다.
- N1933/0240에는 BWF02 전용 선언을 사용하는 유사 구조가 실제로 존재한다. 독립 원문 Part135 OR6/147 Reset/151 Coil과 %Q6.3을 대조했으며 BWF01 내용을 단순 이름 치환하여 생성한 것이 아니다.
- 두 네트워크 모두 Inputs.BC01 run을 조건에 사용하는 사실은 **제어 의존성**을 지지한다. BWF의 실제 토출 지점이 BC01이라고 확인하거나 BWF가 BC01의 하위 부품이라고 단정하는 근거는 아니다.
- Disable_Load_RD01은 0605의 InterfaceAccess/S Local이다. 전역 태그 또는 현장 입력으로 잘못 분류하지 않는다.
- N1934/0241 등에서 같은 Flag의 다른 쓰기가 확인되므로 위 연결만으로 최종 스캔값·모드·자동 운전 전체를 확정하지 않는다.

원본 N1737/0487 및 N1738/0488에는 각각 COEFF_BWF1_HOPPER_LEVEL / COEFF_BWF2_HOPPER_LEVEL과 ZERO 계수 이름이 있다. 이는 호퍼 레벨 관련 기능을 뒷받침하지만 외부 계량기의 로드셀 수량, 중량 단위, 제로/스팬 값, 계량 알고리즘을 제공하지 않는다. 해당 값을 P03 설정으로 제안하지 않는다.


## 4 전기 전달 경로

다음은 GME 도면상 경로다. 실제 설치·정상 전압·모델·보호값의 현행 확인이 아니다. FG와 PDF 페이지를 분리하며 도면의 24V·4~20mA 표기를 현장 측정값으로 취급하지 않는다.


| 후보 경로 | 외부 경계 및 GME 단자 | GME 모듈 쪽 | 원본 페이지·개정 | 아직 없는 끝점 |
| --- | --- | --- | --- | --- |
| 호퍼2 고장 | +24Vdc 10.7 → X1 350(5×20 2A F 표기) → 외부 접점 경로 → X1 351 → E16.4 | FG132 E16.4, 단자5, CPU515/MOD12 표기 | FG94/PDF95, FG132/PDF133: 두 페이지 Rev2 17.03.2025; 기본 DATA27.05.2024 | 외부 반의 접점·단자명·케이블명·호퍼 명판. 그려진 접점으로 실물 정상 극성 추정 금지 |
| BWF01 원격 허가 | A6.2 → 84KA3 코일 A1/A2, 귀환 -0Vdc10.6; 릴레이 접점5–9 → X1 236/237 | FG142 A6.2 단자23, CPU515/MOD15 | FG84/PDF85, FG142/PDF143: 기본 DATA27.05.2024, 표시 개정란 공란 | 외부 반이 이 무전압 접점을 해석하는 방식·기동 내부회로 |
| BWF02 원격 허가 | A6.3 → 84KA4 코일; 접점5–9 → X1 238/239 | FG142 A6.3 단자24 | FG84/PDF85, FG142/PDF143 | BWF02 명판과 호퍼/컨베이어 경계 |
| BWF01 상태·고장·레벨 | X1 264/265,266/267,268/269,270/271,272/273 → E11.1~E11.5 | FG127 단자32~36 | FG86/PDF87, FG127/PDF128: 기본 DATA27.05.2024, 표시 개정란 공란 | I11.1의 MANU STATUS↔BWF01 OK 의미와 외부 신호 정상 상태 |
| BWF02 상태·고장·레벨 | X1 274/275,276/277,278/279,280/281,282/283 → E11.6,11.7,12.0,12.1,12.2 | FG127 단자37/38 및 FG128 단자1/2/3 | FG87/PDF88, FG127/PDF128, FG128/PDF129; FG128은 Rev2 17.03.2025 | BWF01과 별도 외부 측 단자·장비 확인 |
| BWF01 유량/레벨 입력 | X1 252/253/254(+/−/shield) → PEW264; X1 258/259/260 → PEW268 | FG105 MOD2의 PEW264 I4+/I4− 22/24, PEW268 I6+/I6− 30/32 | FG85/PDF86, FG105/PDF106, 4~20mA 표기 | 외부 변환기/계량기 단자·현재 스케일·단위 |
| BWF02 유량/레벨 입력 | X1 255/256/257 → PEW266; X1 261/262/263 → PEW270 | FG105 MOD2 PEW266 I5+/I5− 26/28, PEW270 I7+/I7− 34/36 | FG85/PDF86, FG105/PDF106 | 외부 계량기와 P03/P04의 관계 |
| BWF01/02 속도 설정 | PAW298 → X1 243/244/245, PAW300 → X1 246/247/248 | FG113 MOD7 PAW298 QV5/QI5 25·S5−27, PAW300 QV6/QI6 29·S6−31 | FG85/PDF86, FG113/PDF114, 4~20mA 표기 | 외부 구동기 수신 단자·해석 범위 |

BWF 경로는 GME 단자에서 외부 장비 경계까지다. 계량 본체·로드셀·접속함·계량 인디케이터·배출 모터·인버터의 외부 회로는 이번 원본에서 P03으로 연결되지 않았다. 시공도에 있는 BC01/PV01 케이블을 대신 사용하면 잘못된 수리 위치로 이어질 수 있으므로 미확보로 남긴다.


## 5 알람과 복구

- CLIENT-CL17의 원시 고장 %I16.4와 Allarm.motor_client_17_fault 기억은 구분한다. N424의 Reset식은 위 3.1에 그대로 제시했다.
- BWF01/BWF02에는 별도 BWFxx_FAULT, BWFxx_Fault_Control, min/MAX LEVEL 등의 이름과 N1781~1784 전용 네트워크가 있다. 이를 P03의 알람 목록으로 상속하지 않는다.
- 후보 네트워크에 있는 S5T#10S 등의 시간 상수는 후보별 소유와 원문이 확정되어도 **P03의 지연값 또는 현장 보호값이 아니다**. 본 초안에서 P03 타이머를 만들지 않았다.
- ‘알람 기억 Reset 가능’과 ‘외부 계량기 고장 해소’, ‘기동 허가 회복’, ‘실제 재기동’, ‘계량 정확도 복구’를 별도 확인 항목으로 둔다.
- 현장 관찰·고장 원인·정상 극성·복구 완료·외부 안전 내부 순서는 모두 미확보다. 임의 리셋·강제 출력·인터록 우회·보호값 변경을 조사 방법으로 제시하지 않는다.


## 6 증상별 식별과 자료 수집

실제 고장 신고가 없으므로 다음은 수리 실행표가 아닌, 서로 다른 후보를 혼동하지 않기 위한 관찰 요청 표다.


| 현상 또는 질문 | 확보할 관찰·기존 자료 | 비교 근거 | 배제할 잘못된 해석 | 확인 완료 조건 |
| --- | --- | --- | --- | --- |
| 현장에서는 호퍼1인데 문서는 호퍼2라고 함 | 해당 본체 명판·번호표와 주변 전체 사진, 번호 변경 이력·현장 설비대장 | FG94/132, 원본 WEIGHTING HOPPER 2FAULT | 단순 오탈자로 판단해 P03→CL17 배정 | 현장 번호와 도면/태그 사이의 승인된 대응 근거 |
| 계량값이 표시됨 | 화면 전체, 단위·태그 주소, 외부 계량기 모델/입출력표·회로도 | BWF flow/level 채널 및 HMI CSV | level/flow를 곧바로 kg 중량으로 바꿈 | 센서·변환기·채널·환산·단위까지 연결 |
| 호퍼와 아래 컨베이어가 함께 멈춤 | 각 장비 명판·전원반·제어반 식별, 기존 인터페이스표 | CL17 I16.4 vs CL18 I16.5, BWF 별도 허가 | 동시 정지하므로 같은 설비라는 판단 | 기계 경계와 제어 의존성을 따로 기록 |
| BWF01 신호를 찾았으니 호퍼1인지 질문 | BWF01 라벨이 있는 외부 반의 도면과 호퍼1 사진의 연결 | X1 236/237,264~273,243~245,252~254,258~260 | 01 숫자만으로 동일성 확정 | 동일 외부 장비가 물리·전기 두 축에서 연결 |
| 알람을 지웠는데 설비가 움직이지 않음 | 조작 없이 확보 가능한 기존 시각별 화면/알람 이력·외부 제어 상태 | 고장 입력, 기억, 원격 허가가 별도라는 원문 | GME 알람 Reset = 현장 복구 완료 | 실제 고장 제거·허가·응답·계량 정상 근거 별도 확보 |

관찰을 받을 때는 관찰자·시각/시간대·장비 위치·표시 이름·값/단위·수집 방법·프로젝트/백업 날짜를 함께 보존한다. 아직 관찰하지 않은 칸은 unknown으로 둔다. 사진·운영 기록을 공개 저장소에 복사하지 않는다.


## 7 완료 기준과 추가 자료


### 7.1 가장 먼저 필요한 자료

- **P03 위치 식별**: ‘웨잉호퍼1’을 표시한 주변 전체 사진 또는 배치도, 본체의 번호표·명판. P04 배출컨베이어와 BC01의 상대 위치가 함께 보이면 후보를 크게 줄일 수 있다.
- **번호와 제어반 연결**: 해당 호퍼의 외부 계량제어반 회로도/I/O표/단자표와 제조사·모델. 기존 문서에서 BWF01/BWF02/호퍼2가 어느 실물을 뜻하는지 표시된 자료가 필요하다.
- **1↔2 불일치 해소**: 현장 번호 변경 이력이나 설비대장. CLIENT-CL17 후보라면 GME X1 350/351 ↔ 외부 상대 단자 ↔ 실물 호퍼가 같은 장비라는 연결이 필요하다.

새 자료 요청은 최종 검토에서 P04/P14 결과와 묶어 사용자에게 전달할 수 있다. 현장 측정은 실행하지 않았다. 기존 승인 자료·사진을 우선하며, 가동 설비를 열거나 출력/센서를 조작하는 시험은 이 조사 범위가 아니다.


### 7.2 unknown을 해제하는 판정 기준

- P03 실물 이름/번호/위치와 하나의 catalog ID 또는 새로 확인되는 외부 장비가 자료로 연결되어야 한다.
- 동일성을 뒷받침하는 물리 식별과 전기/제어 연결을 확보하고, 현재 모순인 번호1↔2·피더↔호퍼↔컨베이어 경계를 해결해야 한다.
- 사진 한 장의 숫자 또는 네트워크 제목 하나만으로 결론내리지 않는다. P03/P04 양쪽에 같은 catalog ID를 중복 배정하지 않는다.
- 후보가 실제 복합 장비이면 호퍼 본체·피더 구동·계량제어기·외부 통신을 구분해 소유자를 기록한다. 새 ID 생성은 원본 근거와 최종 대장 검토 뒤에만 결정한다.
- 이후에 해당 ID의 7영역 매뉴얼을 작성·검토한다. 이번 식별 자료만으로 BWF01/BWF02/CLIENT-CL17의 완전한 제어 분석·UI·기록·게시 완료를 선언하지 않는다.


## 네 기능 적용과 기록 보존


| 기능 | 적용 판단 | 이번 결과 |
| --- | --- | --- |
| 도면·래더 나란히 보기 | 식별 후 적용 검토. 지금은 후보별 근거 쌍을 분리 참조 | FG94/PDF95 ↔ N424가 CL17 후보 쌍. P03에 기능 연결하지 않음 |
| 백업·선택 복원 | P03 기록키와 미지 필드 보존 대상 | 구현/시험/기존 기록 접근·변경 없음. 후보 ID로 저장키 변환 금지 |
| 기록 전후 비교 | 관찰 대상이 같다는 식별이 먼저 필요 | 구현·실제 비교 없음 |
| 보고서/PDF | 식별 초안을 독립 자료로 남김 | 요청 형식 Markdown만 작성. 운영 보고서·PDF UI 검증 없음 |


## 검증과 독립 검토

- 고정 커밋 및 Git status --short를 확인했고 원본 저장소는 시작·종료 모두 clean이다.
- 저장소 preflight.py 읽기 전용 실행 결과 inventory_matches true, 원본 phase2_candidates 133이다. source_byte_changes 두 항목은 requirements-audit.json/all-in-one-data.json으로 기존 중복 대조 보고서와 일치한다. 대장을 수정하지 않았다.
- PyMuPDF로 원본 PDF를 렌더했다. P&ID 1쪽, Electrical_Rev2 PDF85/86/87/88/95/106/114/128/129/133/143, 시공도 PDF1/2/3/21/51의 **고유17쪽**을 실제 시각 확인했다. 렌더만 생성한 다른 쪽을 시각 확인 수에 넣지 않았다.
- N424·425와 N1932·1933은 XML Parts/Wires, 원본 선언의 Global/Local·RID/UID/NID·주소·형식을 대조했다. 나머지 후보 네트워크 목록과 추출은 후속 분석의 시작점이며 전 로직 완료를 뜻하지 않는다.
- SHA256 근거 60개는 ../extracts/P03/P03-SOURCES-SHA256.json 및 .txt에 전체 목록으로 기록했다. 원본 묶음 source-manifest의 9파일, 추가 원본 3파일, 중지5자산의 해시는 별도 읽기 전용 검증에 포함한다. 해시 확인은 설비 동작·현장 동일성 검증이 아니다.
- 읽기 전용 검증 스크립트: ../extracts/P03/collect_evidence.py. 결과: ../extracts/P03/P03-READONLY-VERIFICATION.json.
- 별도 독립 검토 전이며, 미실행 항목은 UI/기록/BC01 회귀/npm/test/build/패키지·배포/TIA/현재CPU/현장이다. 이번에 원본·공통 코드·기록 기능을 변경하지 않아 실행하지 않았으며, 시뮬레이터 실행·시험은 영구 중지 범위다.


## 최종 상태


| 구분 | 상태 | 의미 |
| --- | --- | --- |
| identity | unknown | catalog_id null, identity_verified false 유지 |
| documentation | identification_draft_complete_with_gaps | P03 식별 7영역과 필요한 자료 작성. 설비 고유 ID 매뉴얼 완료 아님 |
| static_review | bounded_source_review_complete; bounded_independent_review_complete | 선언·핵심 연결·17쪽 시각·해시 대조. 핵심 근거 제한 범위 독립 검토 완료 |
| ui_records | not_run | 화면·저장·복원·재열기 시험 없음 |
| publication | not_published | 원본·버전·GitHub·Netlify 변경 없음 |
| tia_compile | not_performed | TIA 미수행 |
| live_cpu | not_performed | 현재 CPU/프로젝트 일치 미검증 |
| field_recovery | not_performed | 실물 확인·현장 복구 미수행 |


## 다음 작업

P03은 **새 식별 자료를 받은 뒤 한 번 재개**한다. 그 전에는 현재 후보를 다시 반복 조사하거나 임의 배정하지 않는다. 최종 검토에서는 본 초안의 CL17 번호 불일치와 BWF 분리 경계를 독립 검토하고, P04/P14의 식별 요청과 묶어 필요한 사진·외부 제어반 자료를 정리할 수 있다. 다른 독립된 설비 조사는 이 보류와 분리해 진행한다.

재개 시 먼저 읽을 자료: 이 초안, GME-CATALOG-OVERLAP-REVIEW.md/json, INVENTORY.json P03행, FG94/PDF95·FG132/PDF133, 0234/0599/0601 원본 XML. 완료 커밋은 없음(독립 조사 파일만 작성).


## SHA256 핵심 근거

전체 60개 파일의 상대경로·바이트·SHA256은 동봉된 P03-SOURCES-SHA256.json/.txt가 기준이다. 다음은 식별 판정의 주요 원본이다.


| 원본 파일 | SHA256 |
| --- | --- |
| docs/equipment-standard/INVENTORY.json | 720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc |
| all-in-one/registers/priority-equipment.csv | 953c2c4df5b3a6e40d926d1f0f08f91900b7d6565e4dcd64191b548e438edeba |
| all-in-one/registers/equipment.json | 7870325dff32bbca90fa34507b301c4aad3347d669fddcd03b910343663996fa |
| all-in-one/sources/PID_1684n002I.pdf | 2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b |
| all-in-one/sources/Electrical_Rev2.pdf | 5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6 |
| all-in-one/sources/Electrical_Can_Decoating_20241118.pdf | 3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd |
| all-in-one/sources/decoded-original/0234-FlgNet.xml | 4fa899449ab66d4a852be7c21085590393a8ad11c65d265222c3bfcd649dfc64 |
| all-in-one/sources/decoded-original/0599-IdentXmlPart.xml | 32a693fe12134febbd9f5c7da10c3469ef4d5b164ab8b6bd9ea3867c358936c1 |
| all-in-one/sources/decoded-original/0601-IdentXmlPart.xml | 04c9481f7381284de689ef5c7ff40d7aea93f2004cd877a4e4f27e47baa6d862 |
| all-in-one/sources/decoded-original/0239-FlgNet.xml | dffeeb46b691879c647fefa334674c6e101595c06fab071bc00836fc8f712599 |
| all-in-one/sources/decoded-original/0240-FlgNet.xml | bc1f120c4121b45913d542a0b6dd1ac4801422997fc0cbf3717d50d576932d33 |
| all-in-one/sources/decoded-original/0602-IdentXmlPart.xml | 46ab21151eddaaf616469db520730c60423eb742aa491af194e6710c751b4caf |
| all-in-one/sources/decoded-original/0604-IdentXmlPart.xml | b798d29c5499b5314a1ee3cff9139dae64c887533b86baa43b6e9a052373a6af |
| all-in-one/sources/decoded-original/0605-IdentXmlPart.xml | 0ff6e2228dbfbc9f657359fe1055083ce621365084ea24c4160e4969b3eaac8b |
| all-in-one/sources/decoded-original/0678-IdentXmlPart.xml | 51e637e0b9713c028810f2a717b5c3804a3a26c2f1be7e332a4d6bf277bfc382 |
| all-in-one/sources/hmi_plc_tags.csv | a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404 |
