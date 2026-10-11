# P04 웨잉호퍼배출컨베이어 — 식별 조사 초안


## 0. 결론과 작업 경계

**P04의 catalog_id는 미배정으로 유지한다.** CLIENT-CL18은 이름·고장 인터페이스 측면의 유력한 비교 대상이지만 P04와의 물리 동일성이 확인되지 않았다. BWF01/02는 별도 원격기동·운전/고장·계량 인터페이스이며, CLIENT-CL18=BWF02=P04 또는 BC01=P04로 병합할 근거가 없다. 후보를 지지하는 사실과 자동 배정을 배제하는 사실을 아래에 분리했다.

- 표준: GME-STD-1.0.0. 작업 단위: phase1 미확정 식별 P04.
- 기준: 읽기 전용 source-mv06, Git abcf31c5030bc7ef8749ed8e869a857f2387a28a, 프로그램 v1.12.0.
- 조사: 2026-10-11 UTC. 현재 모델·추론 수준은 별도 런타임 관측 근거가 없어 미확인으로 남긴다.
- 조사자: P04 읽기 전용 조사 작업. 독립 검토: 2026-10-11 핵심 근거 제한 범위 대조 완료. 저장소의 2026-10-09 기존 식별 검토는 참고 자료이며 이번 작업의 신규 독립 검토로 계산하지 않는다.
- 허용 산출물: gme-research/drafts/P04-IDENTIFICATION-DRAFT.md, gme-research/extracts/P04/의 정적 추출·렌더·검증 자료만 작성.
- 원본·공통 코드·대장·버전·배포·운영기록 변경0. 시뮬레이터 작성/수정/생성/실행/행동시험0. 실제 PLC·현재 CPU·현장 보호값·SEJIN 운영 자료 변경0.
- 후보 비교는 CLIENT-CL18, BWF01, BWF02를 중심으로 하며 CLIENT-CL17은 호퍼/컨베이어 경계, BC01은 이미 P01에 연결된 상하류 설비를 구분하기 위한 참고다. 후보 ID의 별도 7영역 매뉴얼 완료를 뜻하지 않는다.


### 이번에 확정한 자료 사실

- Electrical_Rev2.pdf FG94/PDF95는 HOPPER CONVEYOR 2 FAULT를 E16.5, X1:352–353으로 그린다. XML 원본 0235/0599/0601은 이를 client18 고장 래치에 연결한다.
- 같은 FG94/PDF95의 WEIGHTING HOPPER 2 FAULT는 E16.4, X1:350–351이다. 호퍼 채널과 배출컨베이어 채널이 도면·XML에서 분리돼 있다. P03의 “호퍼1” 또는 P04의 번호 없는 이름과 “2”가 같다는 증거는 없다.
- BWF01/02 원격기동은 FG84/PDF85의 A6.2/A6.3, 84KA3/84KA4, X1:236–237/238–239다. BWF 운전·고장은 FG86/87, client18 외부 고장은 FG94에 별도로 그려져 있다.
- P&ID의 BC01(M02)–PV01–CC01/RD01 연결과 시공도 ENTRY 구역의 BC01·M02·SS01·SSL01 배선은 확인된다. P04 또는 BWF01/02/client18을 이 위치에 붙이는 직접 태그는 확인되지 않는다.
- 원본 선택7네트워크의 ORef 75개를 UID/RID/NID·선언 파일·범위·Wire까지 대조했다. 선택 참조 미해석0은 **선택 범위의 선언 대조 결과**이며 전 프로그램 호출순서·현재 실행·실물 식별의 완료가 아니다.


## 1. 7영역 적용표


| 영역 | P04 적용 상태 | 작성 범위 | 미확정 경계 |
| --- | --- | --- | --- |
| 설비·자료 기준 | 적용, 식별 미확정 | 우선행·후보·부모/하위·위치·판본 대조 | 실물 태그, 본체/모터/감속기, 외부 제어반, “2”의 대응 미확인 |
| I/O·HMI | 근거 미확보 | 후보의 원시 I/O·내부 래치·HMI export를 분리 제시 | P04에 배정한 신호0. 이벤트·현재 통신·주소·정상 극성 미확인 |
| 제어 구조 | 근거 미확보 | client18 고장 래치와 BWF 요청/출력 경계를 원본으로 비교 | P04 기동·정지·모드·허가·피드백 소유 미확인 |
| 전기 전달 경로 | 근거 미확보 | 후보 외부 접점/출력, BC01 시공 위치의 자료상 양 끝점 | 후보 외부반 단자·현장 케이블·P04 모터까지의 연속 추적 미확보 |
| 알람·복구 | 근거 미확보 | client18 외부 고장과 BWF 자체 래치의 다른 입력·유지·해제 조건 | P04 최초 알람·실제 원인·정상 극성·재요청·복구 확인 없음 |
| 증상별 수리 | 적용, 식별 중심 초안 | 미기동/운전 중 정지/표시 불일치/배출 불능의 관찰·배제 순서 | 수치·토크·보호 설정·정비주기·가동 조작 절차를 만들지 않음 |
| 완료 기준 | 적용 | 필요한 자료·수집 위치·판정 조건·단계 상태 | 식별 완료/구현/게시/TIA/현재 CPU/현장 복구를 각각 별도 판정 |

자료 미확보를 비해당으로 바꾸지 않았다. P04를 외부 client 설비라고 확정하지 않았으므로 “물리 구동 회로 비해당”으로도 처리하지 않는다.


## 2. 원본·위치·부모/하위 대조


### 2.1 우선행과 catalog 경계

- all-in-one/registers/priority-equipment.csv 5행: P04, 웨잉호퍼배출컨베이어, plc_id 공란, match=unknown, identity_verified=False. 메모는 실제 컨베이어 태그·제어반·앞뒤 운전 신호 확인이다.
- 같은 CSV의 P03(x470,y1235), P04(x730,y1230), P01 BC01(x990,y1220), P05 PV01(x1250,y1235)는 화면 배치 순서 참고다. 이 좌표는 설계 좌표/실측 거리 또는 실제 물질 이동 방향의 증명이 아니다.
- INVENTORY의 CLIENT-CL17/18·BWF01/02는 각기 parent_id=null, phase2, priority_key=null이다. BC01은 P01, parent_id=null이다. 이번 조사에서 부모/자식 관계를 신설하지 않는다.
- equipment 대장에서 BC01의 직접 하위는 SS01이다. P&ID/시공도에 SSL01이 보인다고 신규 catalog ID를 만들거나 P04 하위로 가져오지 않는다.
- CLIENT-CL 이름 공간은 외부 모터/설비 채널이며 P&ID의 CYL-CL 공압 실린더와 다르다. 숫자18만으로 실린더·모터·호퍼를 병합하지 않는다.
- 작업3 overlap 검토의 후보9 합집합은 유지한다. P04 조사 결과로 CLIENT-CL18/BWF01/BWF02를 132 연구범위에서 삭제하거나 세 설비 완료로 올리지 않는다.


### 2.2 P&ID 실렌더

원본 all-in-one/sources/PID_1684n002I.pdf, PDF1. 도면번호1684n002, Apex I, 원도일06/04/2011, 마지막 개정란 I 15/01/2013. 렌더 extracts/P04/PID-page1.png, 확대 PID-entry-detail.png, 개정란 PID-title.png.

- 입구의 경사 컨베이어는 BC-01, 모터 M02, 도면상 4kW/440V로 표시된다. SS-01/SSL-01과 PV-01 투입부, CC-01/RD-01 본체 연결이 보인다.
- 입구 부근에 PARAMETERS COMING FROM BUYER'S MACHINES와 X-01~X-05가 있으나 이 기호가 BWF01/02 또는 client18과 대응하는 I/O cross-reference는 이 시트에서 확인되지 않는다.
- P04 한국어명·호퍼1·HOPPER CONVEYOR 2·BWF01/BWF02를 이 입구 컨베이어에 직접 대응시키는 태그가 확인되지 않는다. 이것은 이 판본/시트의 식별 한계이며 현장 설비의 부재 증명이 아니다.
- P&ID의 출력·전압 표시는 2013 자료 사실이다. 현행 모터·인버터·정격·사용 상태로 채택하지 않는다.


### 2.3 시공도 실제 페이지

원본 Electrical_Can_Decoating_20241118.pdf, 64쪽. 표지 PDF1은 FOR APPROVAL, 개정란 24.11.11 first draft design이며 승인란은 확인 서명이 없다. “승인된 준공도”로 취급하지 않는다.


| PDF 실제 쪽 | 도면/구역 | 렌더에서 확인한 내용 | P04 해석 경계 |
| --- | --- | --- | --- |
| 3 | CANDC-CONS-S003-003 / SPEC AREA | ENTRY·ROTARY 등 영역, BC01=M02, SS01/SSL01, ENT1TB1/ENT1TB2 목록 | 영역표는 P04 실물 위치 또는 외부반 소유를 주지 않음 |
| 21 | CANDC-CONS-E004-021 / ENTRY ZONE01 | Direct OProom→M02, BC01, 케이블1_1=ENT+BC01-M02A. SS01/SSL01은 ENT1TB1/2 경유 | BC01의 도면상 전달 범위. P04 모터 케이블로 전용 금지 |
| 50 | CANDC-CONS-G002-050 / HOW TO READ CABLE DRAWINGS | 케이블표 읽기 설명과 예시 행 | 여기의 예시 길이17을 시공 최종값으로 채택하지 않음 |
| 51 | CANDC-CONS-C001-051 / CABLE SCHEDULE (1) | 행1_1, CR→BC-01/M02, FEEDING ROTATION DRUM CONVEYON, PVC-S/4/2.5SB, 조정20·LEN22 | 실제 현장 케이블 길이·규격 확인 완료가 아니며 P04로 옮기지 않음 |
| 53 | CANDC-CONS-C003-053 / CABLE SCHEDULE (2) | 3_1 CR→BC01 ENT1TB1/SS01, 3_2 CR→BC01 ENT1TB2/SSL01, 3_18·3_19 하위 센서 경로 | 해당 표에 있는 BC01 소유·단자 경계를 유지. 가려진 3_5행은 복원하지 않음 |

시공 PDF 전체 추출 텍스트에서 BWF/hopper/weigh/호퍼/컨베이어 검색은 일치0이었다. PDF1/3/21/50/51/53을 실제 렌더로 대조했다. 검색 음성 결과는 그래픽·미수록·후속 개정의 부재를 보장하지 않는다. 현재 자료로 외부 계량/배출반의 현장 케이블 종점을 확정할 수 없다.


## 3. 후보 지지·배정 배제·미확정 판정


| 후보/관계 | 지지 근거 | 배제되는 판단 | 현재 판정/추가 증거 |
| --- | --- | --- | --- |
| P04 ↔ CLIENT-CL18 | FG94의 HOPPER CONVEYOR 2 FAULT, E16.5; XML425 client18 래치. 컨베이어 역할 명칭이 가깝다 | 이름·네트워크 제목만으로 동일성 확정, 고장 입력을 기동 출력으로 간주 | 역할 후보 유지. 번호2의 의미, P04 본체 태그, 외부반→X1:352/353 케이블 연속성 필요 |
| P04 ↔ BWF02 | 별도 원격기동·Run/Fault·계량 I/O가 있고 425 색인 제목에 bwf02 문자열이 있다 | 제목 bwf02를 동일성 선언으로 해석; E16.5를 BWF02 원시 Fault E12.0과 같은 주소로 처리 | 비교 후보 유지. 외부 도면에 BWF02와 hopper conveyor2의 기계/제어 관계가 명시돼야 함 |
| P04 ↔ BWF01 | BWF01도 BC01/RD01과 연동하는 외부 피더 후보 | “호퍼1→BWF01” 숫자 유추, P04에 BWF01 I/O 전체 복사 | 약한 역할 후보. 명판·배치도·원격신호 매트릭스 필요 |
| P04 ↔ BC01 | 둘 다 컨베이어 일반명, P&ID 입구 이송 역할 | 기존 P01과 P04를 편의상 같은 카드로 병합 | BC01은 P01 유지. P04와 같은 실물인지, 별도 상류 컨베이어인지 사진·태그 대조 필요 |
| P04 ↔ CLIENT-CL17 | FG94에서 호퍼2와 컨베이어2가 이웃하고 XML424/425가 나란함 | E16.4 호퍼 Fault를 배출컨베이어의 직접 Fault로 대체 | P03 경계 참고. 호퍼와 컨베이어 별개 채널을 유지하며 물리 부모/자식 미확정 |

“배정 배제”는 특정 잘못된 병합/치환을 금지한다는 뜻이다. 후보가 현장과 관계없다는 확정 판정이 아니다.


## 4. 후보 I/O·HMI 및 원본 선언


### 4.1 CLIENT-CL18과 주변 채널


| 신호 | 자료상 구분 | 원본 위치 | 읽은 사실/제한 |
| --- | --- | --- | --- |
| HOPPER CONVEYOR 2FAULT | Global 물리 Input, Bool, SSD AO133 | 0599-IdentXmlPart.xml RID40, NID18 UID359/361; 0235-FlgNet.xml | live_index 문서566 Address=%i16.5. Comment의 e19.7은 옛 주석이므로 현행 주소와 섞지 않음 |
| Allarm.motor_client_18_fault | Global DB 내부 래치, Bool, AO130 | 0601-IdentXmlPart.xml RID41, NID18 UID360/363, Write OID7/8 | 외부 물리 고장 입력 자체와 별개. catalog의 client18 명칭은 정규화된 ID이며 원본 PLC 태그가 아님 |
| Flag.RESET_ALLARM | Global DB 비트, Bool, AO48 | 0601 RID7, NID18 UID362 | 원본 래치 해제 조건의 일부. 외부반 Reset 출력·운전 재요청으로 해석하지 않음 |
| ON | Global Memory, Bool, AO0 | 0599 RID1, NID18 UID358 | 접점 이름이며 항상 참인 상수라고 가정하지 않음 |
| WEIGHTING HOPPER 2FAULT | Global Input AO132 | 0599 RID38, NID17 UID341/343; network424/0234 | live_index565 I16.4. P03 호퍼1 또는 P04에 배정하지 않음 |


### 4.2 별도 BWF 원시 입력과 처리 DB

- 0558-IdentXmlPart.xml의 SimpleAccess/SAD Input은 BWF01 OK AO89(%I11.1), BWF 01 RUN AO90(%I11.2), BWF01 FAULT AO91(%I11.3), BWF02 OK AO94(%I11.6), BWF 02 RUN AO95(%I11.7), BWF02 FAULT AO96(%I12.0)을 선언한다. 주소는 live_index/도면과 교차 대조할 대상으로 유지한다.
- 전기 FG86/PDF87·FG87/PDF88에서는 OK에 해당하는 I11.1/I11.6의 명칭이 **MANU STATUS**다. 이를 바로 “Ready가 정상”으로 번역하거나 정상=1이라고 확정하지 않는다.
- 0604의 Inputs.BWF01 OK, Inputs.BWF02 OK, Inputs.BC01 run 및 0657의 Inputs.BWF 01/02 RUN, Inputs.BWF01/02 FAULT는 GlobalAccess DB 처리 신호다. 같은 비트 오프셋 숫자가 있어도 SimpleAccess 물리 입력과 범위가 다르다.
- Consent Start BWF01/02는 0602의 Global SimpleAccess, SAD Output AO50/51, Bool이며 live_index의 Q6.2/Q6.3과 대응한다. BWF 요청 비트 Flag.M_BWF01/02와 실제 모터 Run은 별개다.
- BWF01/02 계량 아날로그는 FG85/PDF86에 별도 계통으로 표시된다: PAW298/300 속도·유량 설정, PEW264/266 유량, PEW268/270 레벨. 4–20mA 표시는 도면값이다. 환산·단위·범위·현재 모듈은 이 식별 조사에서 승인하지 않는다.


### 4.3 HMI export 후보 자료

all-in-one/sources/hmi_plc_tags.csv를 직접 읽었다. 다음은 후보 export 설정이며 P04의 확정 HMI가 아니다.


| 후보 | 원문 행 | 설정 |
| --- | --- | --- |
| BWF01 | 59,618–621,736–737 | Editor DB26,INT8; Risposta DB11,X70.1; StatusOK X70.0; Allarme1 X70.2; Flag DB2,X12.0; Level DB13,INT32; Flow DB13,INT28 |
| BWF02 | 60,651–654,733,735 | Editor DB26,INT10; Risposta DB11,X72.1; StatusOK X72.0; Allarme1 X72.2; Flag DB2,X12.5; Level DB13,INT34; Flow DB13,INT30 |

- export에는 Access Name PLC, “dde.cfg 설정; 온라인 현재값 아님”이 명시돼 있다.
- 이 CSV에서 hopper/client_18 직접 이름 행은 찾지 못했다. 공통 알람 화면의 간접 표시가 없다는 증명은 아니다.
- HMI network1213/1214는 색인에 BWF01/02 이름이 있으나 network-map의 inferred NID 및 resolved_operands가 비어 있다. 이번에는 실제 버튼 이벤트/쓰기 경로와 완전한 원본 선언 결속을 확인하지 않았으므로 설정 주소만으로 현재 동작을 확정하지 않는다.
- P04의 읽기/쓰기 권한·실제 화면·데이터 형식·전환 단위는 근거 미확보다. 기존 P04 기록키와 다른 설비 기록을 병합하지 않는다.


## 5. 제어 구조·알람 경계의 직접 XML 대조

선택 XML의 정적 연결만 기술한다. 프로그램 호출 조건·스캔·복수 쓰기 최종순서·현재 CPU 결과는 미검증이다. 전체 refs/Parts/Wires는 extracts/P04/native-evidence.json에 보존했다.


### 5.1 network425: 외부 client18 고장 래치

원본 0235-FlgNet.xml, NID18. 선언 0599/0601.

- Powerrail→Part373(ON)→Wire374에서 두 갈래.
- Set: Part375(HOPPER CONVEYOR 2FAULT)→Wire376→SCoil352. 대상은 ORef360/RID41 Allarm.motor_client_18_fault.
- Reset: Part377은 같은 외부 Fault의 **Negated operand**. 그 out→Wire378→Part379(Flag.RESET_ALLARM)→Wire380→RCoil357. 대상은 ORef363/RID41로 같은 내부 래치.
- 따라서 선택 정적 조건은 ON AND 외부 Fault → Set, ON AND NOT 외부 Fault AND RESET_ALLARM → Reset이다.
- 6 Part/11 Wire로 구성되며 이 네트워크에는 타이머, Ready, Run, 기동 Coil, 외부반 Reset 출력이 없다. 전 프로그램·외부반에도 없다고 확대하지 않는다.
- 물리 접점 정상 극성은 미확인이다. 원본 접점 반전 표시와 정상운전 상태는 다른 정보다. 알람 Reset은 원인 제거 또는 재기동 성공이 아니다.
- 425의 client motor 18 allarm bwf02---------------는 색인 제목이다. ORef/선언의 입력명은 HOPPER CONVEYOR 2FAULT이며, 제목만으로 P04 또는 BWF02 실물과 동일해지지 않는다.


### 5.2 network1932/1933: 별도 BWF 요청 Reset과 원격허가 출력

원본 0239/0240-FlgNet.xml, 각각 NID3/4. 0602/0604/0605/0606 선언을 대조했다.


| 항목 | BWF01 | BWF02 |
| --- | --- | --- |
| 여섯 조건 OR | Part97, Cardinality6 | Part135, Cardinality6 |
| 요청 Reset | RCoil109 → Flag.M_BWF01 | RCoil147 → Flag.M_BWF02 |
| 원격 출력 | Coil113 → Consent Start BWF01 | Coil151 → Consent Start BWF02 |
| 출력 선언 | ORef125/RID26, AO50 Output | ORef163/RID32, AO51 Output |
| 로컬 조건 | ORef121/RID16, Local Disable_Load_RD01 | ORef159/RID16, Local Disable_Load_RD01 |

ON을 앞에 둔 여섯 병렬 경로는 자기 BWF Fault, 자기 Fault_Control, SET_PERC=Int 0, NOT 처리 BWF OK, NOT 처리 BC01 run, Local Disable_Load_RD01이다. 이 OR가 요청 Reset에 연결된다. 별도 ON AND Flag.M_BWFxx 가지는 원격허가 일반 Coil로 간다.

- 0606의 비교 상수는 S=Constant, CB T=Int, SV=*x0030*, V=0이다. 임의 비율/시간으로 해석하지 않는다.
- 0605의 Disable_Load_RD01은 **motors 1 Local**이다. 같은 이름의 Global/다른 블록 Local과 합치지 않는다.
- 원격허가 출력은 외부반으로 보내는 접점 인터페이스다. 이 두 네트워크만으로 외부 모터의 실제 구동·브레이크·속도·정지 순서를 만들지 않는다.
- 같은 두 요청 비트에는 network1934(0241, NID5)의 추가 RCoil170/172/228/210이 있다. 그중 SdCoil164는 Tag_114/S5T#6M 선언을 쓴다. 따라서 1932/1933만을 유일한 정지/쓰기 경로로 주장하지 않는다. 그 타이머를 P04 지연값으로 가져오지 않는다.


### 5.3 BWF02의 별도 고장과 client18의 차이

network1783(0420-FlgNet.xml, NID3; 0656/0657/0658)은 Allarm.BWF02_FAULT를 대상으로 한다. client18의 Allarm.motor_client_18_fault와 다른 선언/쓰기 대상이다.

- ON→Consent Start BWF02 아래에서 NOT 처리 Run은 SdCoil147(Tag_50, S5T#10S)의 입력이다.
- Set Part156의 OR155 두 경로: ON AND Consent Start BWF02 AND Tag_50 AND NOT Inputs.BWF 02 RUN, 또는 ON AND Consent Start BWF02 AND Inputs.BWF02 FAULT.
- Reset Part162: ON AND Flag.RESET_ALLARM AND Allarm.BWF02_FAULT AND NOT Inputs.BWF02 FAULT.
- Tag_50은 Global Timer AO121이며 HMI 태그가 아니다. 10초 상수는 BWF02 후보 네트워크의 원문이며 P04 알람 지연으로 배정하지 않는다.
- BWF01 network1781(0418, NID1)도 별도 자기 Fault/Run/Tag_49의 선언·핀을 대조했다. 이 후보의 존재는 P04가 BWF01/02 중 어느 하나라는 결론을 주지 않는다.


## 6. 전기 전달 경로: 확인된 끝점과 끊긴 끝점

FG는 도면 우하단 번호, PDF는 파일의 1기준 실제 쪽이다. 원본 Electrical_Rev2.pdf를 직접 렌더해 아래 표를 확인했다. FG18·94·132의 개정란은 Rev2/17.03.2025, 원도일27.05.2024다. FG84/85/86/87/142는 원도일27.05.2024이며 검토한 해당 페이지 개정란은 비어 있다. 파일명 Rev2를 모든 페이지의 기입된 개정으로 확대하지 않는다.


| 경로 | 실제 도면 끝점 | 현재 미확정 |
| --- | --- | --- |
| client18 외부 고장 | FG94/PDF95: +24Vdc10.7→X1:352(5×20 2A F)→외부 접점기호/도체94.5→X1:353→E16.5(132/5) | 외부반 실제 접점번호·케이블번호·반대쪽 단자·정상 극성·P04 소유 |
| 입력 모듈 쪽 | FG132/PDF133: E16.5는 94/7에서 와 채널6에 HOPPER CONVEYOR 2 FAULT. 도면 표기 CPU515/MOD12 | 표기 CPU는 도면값이다. 현재 장착 CPU/모듈·하드웨어 주소 확인 아님 |
| BWF01 원격 | FG142/PDF143 A6.2(채널23)→FG84/PDF85 84KA3 A1; A2→-0Vdc10.6. 부하 접점5–9를 통해 X1:236–237 | 외부반 종점·실제 전압/부하·P04 기동 여부 |
| BWF02 원격 | FG142/PDF143 A6.3(채널24)→FG84/PDF85 84KA4 A1; A2→-0Vdc10.6. 부하 접점5–9를 통해 X1:238–239 | 마찬가지. Coil 출력과 실제 모터 운전은 별개 |
| BWF02 회신 | FG87/PDF88: X1:274–275 MANU STATUS/E11.6, 276–277 RUN/E11.7, 278–279 FAULT/E12.0 | 서로 다른 세 입력. E16.5와 같은 원시 입력이라고 합치지 않음 |
| BWF01 회신 | FG86/PDF87: X1:264–265 MANU STATUS/E11.1, 266–267 RUN/E11.2, 268–269 FAULT/E11.3 | 실제 Ready 의미·정상 극성은 별도 확인 |
| BC01 비교 | FG18/PDF19: M02/BC-01 및 18AS1 구동 회로, FEEDING ROTATION DRUM CONVEYOR. 시공21/51의 M02 케이블과 명칭 일치 | BC01 자료를 P04 전용 회로·인버터 모델·보호값으로 복사하지 않음 |

FG84의 릴레이 하단 요약에는 1/5/9 접점표가 있지만 실제 그린 원격 접점 부하는 **5–9**다. 번호1을 직렬 부하 끝점으로 읽지 않았다. 이 도면은 외부반 접점 인터페이스까지만 제공하므로 P04의 전원→보호→구동기→모터 전체 경로 완료로 표시하지 않는다.


## 7. 증상별 수리·관찰 초안

다음은 안전한 자료 수집·원인 배제 순서다. 실제 가동/정지·리셋·전원 투입·보호 우회·현장 측정 작업을 실행하거나 지시한 기록이 아니다. 외부반 제조사 절차·현장 안전 절차가 확보되기 전 강제출력·접점 점퍼·보호값 변경으로 확인하지 않는다.


| 증상 | 먼저 기록할 관찰 | 비교/배제 기준 | 필요한 추가 자료/복구 증거 |
| --- | --- | --- | --- |
| 배출컨베이어 미기동 | P04라고 부르는 본체 사진·태그, 발생시각/시간대, 외부반/VFD 최초 표시, 요청 화면 | 실제 기동 주체가 GME 출력인지 외부 계량반인지 먼저 구분. client18 Fault는 기동 명령이 아님 | 본체↔반↔케이블↔단자↔도면 태그의 연속 대응; 승인 운전 절차 및 실제 Run 확인 |
| 운전 중 정지 | 최초 정지/고장 순서, 상류 호퍼와 하류 BC01 상태, 외부반 기록 | client18 Fault E16.5, BWF02 Fault E12.0, BWF 요청 해제는 서로 다른 경계. 시간·출처 없이 원인 순서 추정 금지 | 동기화된 시각의 요청/허가/원시/처리/실제회전 기록과 최초 원인 해소 증거 |
| HMI 운전 표시와 실물 불일치 | 화면명·태그·값·수집장치와 실물 관찰을 분리 | BWF HMI Risposta는 export 주소일 뿐 P04 화면 확정 아님. DB 처리 Run과 원시 입력을 구분 | 정확한 HMI 이벤트/통신 경로·현재 프로젝트·외부반 Run의 주체 |
| 모터는 움직이나 배출 불능 | 식별된 본체의 투입·배출 지점, 막힘·벨트/기계 상태의 관찰 사진 | 계량 호퍼·컨베이어·후단 BC01/PV01을 한 설비 고장으로 묶지 않음 | 제조사 기계도/감속기·벨트 사양·안전한 점검 및 승인된 조치 후 물질 전달 확인 |
| Reset 뒤 다시 알람 | 원인 신호 상태·래치·Reset 요청 시각 | network425는 외부 Fault가 남아 있으면 Reset 조건이 성립하지 않음. BWF 자기 알람은 별도 식 | 확인된 외부 원인 제거→해당 래치 해제→승인 재요청→실제 응답·잔존 알람 확인 |

관찰 기록 필수: 관찰자, UTC 또는 명시된 현지 시간대, 정확한 위치/장치 태그, 값·단위, 수집 장치, 기준 프로젝트/도면 판본, 원본과 비교한 차이, 배제 결과, 승인된 조치, 실제 복구 증거. 현재 실물·정상 극성·설정값·토크·주기·부하 한계는 공란/미확인으로 유지한다.


## 8. 식별 완료에 필요한 최소 자료와 판정


| 우선 | 확보할 자료 | 수집 위치/대상 | 수용 기준 |
| --- | --- | --- | --- |
| 1 | P04 본체 및 모터/감속기 태그 사진, 호퍼에서 BC01까지의 연속 전경 | 사용자가 P04라고 지정한 위치 | 같은 프레임/표식으로 P03 호퍼, P04 배출부, P01 BC01을 구별. 번호1/2 의미를 기록 |
| 2 | 기동반/VFD/계량반 명판·도면명·기기목록 | P04를 실제 구동하는 제어반 | 본체 태그와 반 도면의 부하 태그가 연결되고 실제 제어 소유가 확인됨 |
| 3 | 외부반 인터페이스/케이블표 양 끝점 | 외부반과 GME X1:352/353, 후보236–239 | 케이블ID·심선·양단단자가 연속으로 일치. 실제 도면/사진에 CLIENT18·BWF01/02 관계 명시 |
| 4 | 최신 승인 배치도/P&ID/시공 또는 준공도·개조 내역 | 설비 담당의 현재 판본 | 원본2013 P&ID·2024 초안·2025 전기도면과의 변경점/적용일 설명 |
| 5 | 현재 엔지니어링 프로젝트와 외부반 I/O 매트릭스, HMI 이벤트 | 권한 있는 엔지니어의 읽기 전용 자료 | 원시 I/O/처리 DB/요청/허가/회신/알람의 소유·주소·극성·반영 순서가 연결됨 |
| 6 | 제조사 매뉴얼과 승인된 운전·복구 기록 | 식별된 본체·VFD·계량제어기 | 모델/판본이 명판과 같고 실제 조치·재요청·응답 증거가 있음 |

실물 동일성은 단일 이름이나 일치한 숫자만으로 판정하지 않는다. 최소한 본체 태그·연속 위치/유로·외부반 부하 태그·케이블 양 끝점이 상충 없이 연결돼야 한다. 새로운 근거가 복수 후보를 부분장치 관계로 보여주면 본체/구동/계량/연동을 따로 유지하고 catalog 병합을 자동 수행하지 않는다.


## 9. 네 기능과 기록 보존


| 기능 | 이번 상태 | 이유/다음 단계 |
| --- | --- | --- |
| 도면·래더 나란히 보기 | 후보 비교 근거만 준비, P04 구현 안 함 | FG94↔network425, FG84/142↔1932/1933는 후보 묶음으로만 사용 |
| 백업 미리보기/선택 복원 | not_run | P04 태그/프로파일 배정 전. 기존 P04와 BC01/BWF/CLIENT 키를 통합하지 않음 |
| 전후 기록 비교 | not_run | 실제 관찰 기록을 쓰지 않았다. 현장 자료가 생기면 시각·근거 판본 분리 |
| 관찰 보고서/PDF | 본 MD 조사 초안만 작성, UI/PDF 기능 검증 안 함 | 매뉴얼 생성·기록도구·업로드·게시 권한을 확대하지 않음 |

기존 note/repair_observation·미지 필드·초안·타설비 기록·저장키를 읽기/쓰기 변경하지 않았다. 원래 저장시점 generated_with/saved_with를 현행 CPU 증거로 바꾸지 않는다.


## 10. 정적 검증과 최종 상태

- 읽기 전용 preflight 종료0: inventory_matches=true. 23 우선행/248 ID/우선 대응18/기존 제외90/부모보류7/원본 phase2 133 일치. requirements-audit.json 및 all-in-one-data.json의 source_byte_changes는 기존 표준 snapshot 대비 바이트 차이며 이번 파일 수정이 아니다. 관련 대장·메타데이터 대응은 일치한다.
- 원본 선택7네트워크/75 참조를 UID/RID/NID·직접 선언에 결속해 정적 추출. 선택 참조 미해석0. XML에서 Global/Local/Constant·Input/Output/Memory/Timer·Int/S5Time·반전 접점·다른 RCoil을 보존했다.
- P&ID PDF1, 전기 PDF19/85/86/87/88/95/133/143, 시공 PDF1/3/21/50/51/53의 관련 부분을 실제 렌더로 확인했다. 렌더 파일은 extracts/P04에 있다. 추가로 만들어 둔 미열람 렌더는 검토 완료 쪽수에 포함하지 않는다.
- 원본 source-hashes.json은 판본·자료 파일 SHA256을 보존한다. 중지5자산의 저장소 freeze 해시와 실제 파일 일치5/5. Git tracked/untracked 변경0(읽기 전용 source-mv06 내부 기준).
- 신규 자동 배정0, catalog 삭제/병합0, 사용자 운영기록 작성0. 소스·코드·버전·배포 변경0.
- 미실행: 매뉴얼/시뮬레이터 생성, 동작 시험, UI/기록 저장·재열기, BC01 회귀·패키지 빌드, 게시 검증, TIA 컴파일, 현재 CPU/현장·외부반 동작 확인. 이번 식별-only 범위이며 기존 완료 상태를 바꾸지 않는다.


| 구분 | 상태 | 의미 |
| --- | --- | --- |
| documentation | identification_draft_ready | 확보 자료·판정·필요 증거를 7영역 틀로 정리 |
| identity | unresolved / catalog_id=null | P04 실물·제어 소유 미확정, assigned_signals=[] |
| static_review | selected_primary_evidence_checked | 선택 XML·도면·대장 대조. 신규 독립 검토는 별도 대기 |
| ui_records | not_run | 프로파일/기록 기능 구현·사용자 기록 변경 없음 |
| publication | not_published | 이번 초안 원본 통합·게시 없음 |
| tia_compile | not_performed | 실행 논리 검증 아님 |
| live_cpu | not_performed | 현행 프로젝트/주소 확인 아님 |
| field_recovery | not_performed | 안전 운전/복구 완료 아님 |


### 인계

- 부모는 초안의 후보 범위와 원본 대조를 독립 검토한 뒤 우선 P04 “식별 조사 초안 준비”와 “실물 미확정”을 함께 기록할 수 있다. CLIENT-CL18/BWF01/BWF02의 신규 설비 완료를 추가하지 않는다.
- 다음 조치는 P04 태그·상하류 연속 사진과 외부반 양단 케이블표 확보다. 새 자료 없이 동일한 식별 보류를 반복 조사하지 않는다. P03/P14 식별 조사 및 독립된 후속 설비 작업은 별도 진행할 수 있다.
- 완료 커밋 없음. 원본 고정 커밋은 유지됐고 변경은 별도 조사 산출물에만 있다.


## 11. 근거 목록과 해시

모든 저장소 경로는 고정 source-mv06 기준이다. 아래 PDF/XML이 핵심 원본이며 대장·색인·기존 보고서는 탐색/이력 자료로 구분한다. 전체36파일 SHA256은 extracts/P04/source-hashes.json, 선언·핀·배선은 native-evidence.json, 물리 선언은 physical-declarations.json, HMI 원문행은 hmi-candidate-rows.json, 대장 선택은 catalog-priority-selection.json에 있다. MD 자체 해시는 본문에 넣지 않고 별도 검증 결과에서 제공한다.


| 주요 원본 | SHA256 |
| --- | --- |
| all-in-one/sources/PID_1684n002I.pdf | 2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b |
| all-in-one/sources/Electrical_Rev2.pdf | 5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6 |
| all-in-one/sources/Electrical_Can_Decoating_20241118.pdf | 3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd |
| all-in-one/sources/decoded-original/0235-FlgNet.xml | 1a4913d7a151824d6318edcd43bd4d496bee11b83a75f1d8f5d4cb04dd01b71c |
| all-in-one/sources/decoded-original/0599-IdentXmlPart.xml | 32a693fe12134febbd9f5c7da10c3469ef4d5b164ab8b6bd9ea3867c358936c1 |
| all-in-one/sources/decoded-original/0601-IdentXmlPart.xml | 04c9481f7381284de689ef5c7ff40d7aea93f2004cd877a4e4f27e47baa6d862 |
| all-in-one/sources/decoded-original/0239-FlgNet.xml | dffeeb46b691879c647fefa334674c6e101595c06fab071bc00836fc8f712599 |
| all-in-one/sources/decoded-original/0240-FlgNet.xml | bc1f120c4121b45913d542a0b6dd1ac4801422997fc0cbf3717d50d576932d33 |
| all-in-one/sources/decoded-original/0241-FlgNet.xml | d421ef5ba9bdcd5aff218c47b1a5ab4663a23b6a0de9fdaa8b2a5dccc3cf15bd |
| all-in-one/sources/decoded-original/0420-FlgNet.xml | d99455768914d77d4233ea8fd95281f695674d44a7b9ca23d252e3b68e257a21 |
| all-in-one/sources/hmi_plc_tags.csv | a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404 |
