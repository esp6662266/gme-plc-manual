# P14 ‘2사이클론’ 식별 조사 초안

**판정: P14의 catalog_id는 미배정, 동일성은 미확정으로 유지한다.** P&ID에는 HE01과 FN01 사이에 병렬로 그려진 **CY01·CY03 두 본체**와, 별도 집진 유로에서 **CY02·CY04·CY05 세 본체가 SC01을 공용하는 군**이 있다. 이 사실은 숫자 ‘2’가 장치 번호·수량·단계를 뜻하는지 결정하지 않는다. CY02, CY01+CY03 또는 ‘2차 사이클론’으로 자동 배정하지 않는다.

원본 렌더, 전기·시공 실제 페이지, 원본 XML의 선언과 연결을 대조한 **우선23 식별 조사**다. CY01~05의 전체 매뉴얼 5건을 완료한 것이 아니며, 기존 SC01 조사와 중복되는 제어·복구 상세는 재사용 경계만 확인했다. 신규 작업3 후보의 후순위 보류를 해제하지 않는다.


## 작업 기준·보존

- 표준: GME-STD-1.0.0, .agents/skills/gme-equipment-rollout/SKILL.md, docs/equipment-standard/WORK-STANDARD.md, WORK-ITEM-TEMPLATE.md, INVENTORY.json.
- 대상: priority_key P14, 사용자 목록 이름 2사이클론, catalog_id null, mapping unknown, identity_verified false, queue_state identity_review.
- 원본: gme-research/source-mv06, Git abcf31c5030bc7ef8749ed8e869a857f2387a28a, 프로그램 v1.12.0. 원본 저장소는 읽기 전용이다. 조사일 2026-10-11 UTC, 시작 09:09 이후. 실제 실행 모델/추론 수준의 별도 런타임 확인 근거는 미확인.
- 원본 대장은 전체248, 우선23, 대응18, 기존 제외90, 부모범위보류7, phase2 133이다. 부모의 별도 연구범위 대조는 SYS-SIMULATION 제외를 추가해132, 그 안의 P03/P04/P14 중복위험 후보9를 보류한다. 이번 조사에서 원본 수량·배정·대장 또는 overlay 분모를 바꾸지 않는다.
- 읽기 전용 preflight: 종료0, inventory_matches=true. requirements-audit.json과 all-in-one-data.json의 기존 source_byte_changes 2건은 재확인했으며 이번 편집이 아니다.
- 생성·편집 범위: gme-research/drafts/P14-IDENTIFICATION-DRAFT.md와 gme-research/extracts/P14/만. 공통 코드·버전·대장·배포·운영자료·원본 저장소 수정 없음. 시뮬레이터 작성·수정·생성·실행·행동시험, 실제 PLC·현장·보호값·SEJIN 변경 없음.
- 아래 원본 상대경로는 별도 언급이 없으면 고정 저장소의 all-in-one/ 기준이다. 파생 색인은 탐색용이며 핵심 판단은 원본 PDF 렌더/XML로 대조했다.


## 7영역 적용표


| 영역 | 상태 | 확보한 것 | 남은 경계 |
| --- | --- | --- | --- |
| 설비·자료 기준 | 적용 | 두 공정군의 본체/배출 구동, 개별 catalog, 숫자2 가설 | 원 배치도 작성자의 의미·실물/현행 태그 |
| I/O·HMI | 본체 전용은 근거 미확보; 주변 구동은 적용 | VR01/02/03·SC01의 분리된 주소/선언/HMI, 공통 경보 출력 | P14 소유 신호는 배정하지 않음; 현행 HMI 이벤트 |
| 제어 구조 | 관계 식별에 적용 | VR별 독립 명령·고장, SC01의 VR03 응답 의존 | 본체 전용 로직·현재 호출/모든 Writer 미확인 |
| 전기 전달 경로 | 주변 장치에 적용; 본체 전용은 근거 미확보 | FG46/49/53/61 및 시공31/35/51/58/64 | 설치 양끝 단자, 현행 케이블, 표기 상충 |
| 알람·복구 | 주변 소유 경계에 적용 | VR별 고장 래치, SC01 자료 재사용, 17HL1 공통 경보 | 본체 분리성능/막힘 전용 알람·실제 복구 미확인 |
| 증상별 수리 | 식별·관찰 계획에 적용 | 가스/고형물 유로와 구동·표시를 나누는 관찰표 | 실제 관찰·승인 조치·복구 자료 없음 |
| 완료 기준 | 적용 | 확정에 필요한 최소 증거·상태 분리 | 현장 식별/통합/UI/게시/TIA/CPU 검증 모두 별도 |


## 1. 설비·자료 기준과 후보 판정


### 1.1 P&ID 실제 구조

sources/PID_1684n002I.pdf는1쪽이다. 이 조사는 원본을 가로 방향으로 렌더하고 전체도와 두 군의 확대부·표제부를 직접 확인했다. 문서번호1684n002, 판I, 기본일자06/04/2011, 최상단 개정I는15/01/2013이다. 현재 현장 준공도나 2026년 실물의 증명이 아니다.

- **열회수·순환 유로:** HE01 오른쪽에서 나온 공통선이 CY01과 CY03의 측면으로 분기하고, 두 본체 상부 출구선이 합류하여 FN01로 이어진다. 따라서 도면상 두 기는 병렬이다. CY01 하부는 VR01/M21, CY03 하부는 VR02/M23 및 각각의 수거부가 그려진다. 각 모터 표기는0.55 kW/440V다. 이 두 본체 하부를 SC01 공용배출로 그리면 원본과 달라진다.
- **집진 유로:** CY02·CY04·CY05의 측면 입력은 공통선에서 갈라지고 상부 출구도 공통선에 연결된다. 그 오른쪽에서 석회 투입과 PV14/TC09 주변 경계, BF01/BF02 및 FN04로 이어지는 별도 집진 계통을 확인한다. 세 본체 하부는 **공통 SC01/M28(3 kW/440V)**에 떨어지고, SC01 출구에 **VR03/M37(0.55 kW/440V)**이 있다. 기계적 연결은 세 본체 중 하나와 SC01의 동일성을 뜻하지 않는다.
- 본체 CY01~05에 별도 모터 기호가 붙은 것으로 읽지 않는다. 도면에서 M21/M23/M37은 VR, M28은 SC의 태그다. 본체의 분리성능·차압·막힘·실제 배출량이 접촉기 응답으로 검증된다고 쓰지 않는다.
- P&ID는 CY03 가까이에 LOCAL EMERGENCY WITH N2 IMMISSION + SIREN 표기를 보여주고, 시공31은 관련 주변 램프·버튼 위치를 CY02로 표기한다. 서로 다른 판본의 **근접 표기/설치 위치**이며 그 자체로 두 본체의 태그 교체 또는 동일성을 입증하지 않는다.
- P&ID 내 두 군을 직렬 ‘1차→2차’ 단계로 명명하는 문구는 확보하지 못했다. 도면의 순환·집진 기능과 숫자2를 단계 번호로 합치지 않는다.


### 1.2 다섯 후보의 지지·배제·미확정

‘배제’ 열은 근거 없는 해석을 배제한다는 뜻이다. 현장 동일성이 아직 없는 CY 후보를 영구 제외하는 판정이 아니다.


| 후보 | 원본에서 지지되는 식별 특징 | 배제해야 할 해석 | P14 대응 판정·필요 증거 |
| --- | --- | --- | --- |
| CY01 | HE01→FN01 병렬 두 본체 중 하나, 하부 VR01/M21 | CY01 하나를 숫자2 전체로 단정, VR01을 본체 모터로 병합 | 후보 유지. 본체 CY01 명판 및 상대편 CY03, 가스 분기/출구와 M21 배출의 한 장면 연결 필요 |
| CY03 | 같은 병렬 쌍의 다른 본체, 하부 VR02/M23 | 명칭2만으로 CY03 또는 ‘2차’ 확정 | 후보 유지. CY03 명판, VR02/M23, HE01/FN01 연결과 원 배치도 의미 필요 |
| CY02 | 태그에02가 있고, 별도 세 본체 군의 일원, 공통 SC01→VR03 | 숫자2=CY02; 시공 CY02 램프/버튼=본체 전용 I/O | 후보 유지. CY02 명판·SC01 공용배출·가스 유로, 숫자2가 번호라는 원 작성 근거 필요 |
| CY04 | CY02/CY05와 공통 SC01을 쓰는 별도 본체 | 번호가4라서 현장 후보에서 자동 제외; 세 기 중 임의 두 기 선택 | 현장 대응 미확정. 현행 태그·배치도 식별·공통배출 사진 필요 |
| CY05 | 같은 세 본체 군의 독립 본체, SC01 출구 가까이 배치 | 도면상 위치/원근으로 P14 또는2차라 확정 | 현장 대응 미확정. 현행 태그·위치·입출구와 배출 연결 증거 필요 |

- **수량2 가설:** CY01+CY03라는 실제 두 기 구조는 가설을 지지하지만, 원 배치도의 ‘2’가 수량이라는 원문 증거는 아니다. 두 ID를 하나로 병합하거나 P14의 단일 catalog_id에 임의 대입하지 않는다.
- **번호2 가설:** CY02라는 원본 태그의 존재만 확인됐다. 원 배치도와의 일대일 연결은 확보하지 못했다.
- **2차 가설:** 번호나 도면상 오른쪽/위아래 배치만으로 단계 의미를 만들지 않는다. 공정단계가 명시된 현행 PFD/P&ID 또는 작성자의 지칭이 필요하다.
- 다섯 후보를 모두 확정 또는 모두 무관으로 처리하지 않는다. 대응 확정 전에는 assigned_signals=[]를 유지하는 것이 타당하다.


### 1.3 catalog 부모와 기계적 하위 관계

registers/equipment.json과 INVENTORY.json에서 CY01~05는 모두 kind=passive, parent 빈값/null, depth0이고 각자 독립 ID다. 다섯 CY를 parent로 적은 별도 자식행은 확인되지 않는다. VR01/02/03와 SC01도 parent 빈값의 별도 motor ID다.

따라서 다음은 **P&ID의 기계적 연결**이지 대장에 이미 등록된 부모/자식 관계가 아니다.

- CY01 하부 배출 ↔ VR01/M21
- CY03 하부 배출 ↔ VR02/M23
- CY02·CY04·CY05 하부 공용 배출 ↔ SC01/M28 ↔ VR03/M37

본체 문서에서 모터를 참조할 수 있으나, VR/SC의 매뉴얼·알람·모터검증 완료를 CY 또는 P14에 상속하지 않는다. 다른 방향으로도 CY 식별 초안이 VR/SC 전체 초안 완료를 뜻하지 않는다.


### 1.4 원 배치도와 자료 시점

registers/priority-equipment.csv 행15와 대장 P14는 여전히 미배정이다. all-in-one-data.json.priority_source는 원 배치도 이름 ‘디코팅 시안’, 관찰2026-10-07, revision2026-09-30T21:57:30.103Z, layout_is_reference=true, edges_imported=false로 기록한다. P14의 x1970/y790은 참고 화면 좌표이며 실제 배관·거리·주변장치 동일성 근거로 쓰지 않는다. 원 SEJIN 페이지는 이 조사에서 재열람·수정·복제하지 않았다.

시공 PDF의 확인 페이지는24.11.11 first draft design, CHECKED/APPROVED 공란이다. 전기 Rev2의 개별 시트는 기본27.05.2024이며 일부17.03.2025 Rev2다. 파일명만으로 같은 개정·현재 설치 상태라 통합하지 않는다.


## 2. I/O·HMI와 제어 소유


### 2.1 본체 신호의 근거 한계

제공 decoded-original/*.xml 695파일과 hmi_plc_tags.csv 782데이터행에서 명시적 CY01~05/하이픈·공백 변형 및 cyclon 문자열을 검색했을 때 일치0이었다. 검색식과 범위는 extracts/P14/explicit-cy-name-search.json에 저장했다. 이는 **이 이름으로 된 직접 신호를 찾지 못했다**는 제한된 결과다. 현장에 전용 계측·별도 PLC·다른 별칭·통신 신호가 없음을 증명하지 않는다.

따라서 본체의 직접 I/O·HMI는 ‘근거 미확보’다. passive 분리 본체 자체의 모터기동 Coil을 새로 만드는 것은 기능 경계상 비해당이지만, 주변 배출 구동·계측 조사 전체가 비해당인 것은 아니다.


### 2.2 주변 구동의 별도 주소

아래 주소는 정적 원본 선언과 회로를 연결한 것이며, 현재 CPU 읽기 또는 현장 시험이 아니다. AO는 비트 오프셋이며 예컨대 Output AO22→Q2.6으로 대조했다.


| 소유 ID | 출력·물리 응답 | 원본 선언 위치 | 요청·처리 응답 | 본체와의 경계 |
| --- | --- | --- | --- | --- |
| VR01 | Start VR01 Q2.6 / VR01_Fbk I3.4 | 0602 RID104 Output AO22; 0613 RID176 Input AO28 | Flag.M_VR_01 DB2.DBX1.1; Inputs.VR-01 RUN DB13.DBX3.4 | CY01 하부의 별도 구동 |
| VR02 | Start VR02 Q3.0 / VR02_Fbk I3.7 | 0602 RID121 Output AO24; 0613 RID188 Input AO31 | Flag.M_VR_02 DB2.DBX1.3; Inputs.VR02 Run DB13.DBX3.7 | CY03 하부의 별도 구동 |
| SC01 | Start SC01 Q3.4 / SC01_Fbk I4.4 | 0602 RID137 Output AO28; 0613 RID212 Input AO36 | Flag.M_SC_01 DB2.DBX1.6; Inputs.FEEDBACKMOTOR SC-01 DB13.DBX4.4 | CY02/04/05 공용 스크루; 기존 SC01 초안 참조 |
| VR03 | Start VR03 Q4.3 / VR03_Fbk I5.4 | 0602 RID177 Output AO35; 0613 RID254 Input AO44 | Flag.M_VR_03 DB2.DBX2.5; Inputs.VR03 Run DB13.DBX5.4 | SC01 출구의 별도 구동 |

DB근거: 0603-IdentXmlPart.xml의 Flag TOD N2/Inputs TOD N13, 0604의 M_VR_01/02/03 RID103/120/176 BO9/11/21, Inputs RID251/252/219 BO28/31/44. 요청 비트·물리 출력·원시 입력·처리 입력은 서로 다른 위치다. 원시 입력의 처리 전달과 호출/다른 Writer는 실제 프로젝트에서 별도 확인해야 하며 이 식별 초안은 전체 입력 전달의 독립 완료 검증을 주장하지 않는다.


### 2.3 HMI 설정

sources/hmi_plc_tags.csv의 각 구동은 독립된 설정행이다. Access Name=PLC, 원문 한계는 dde.cfg 설정; 온라인 현재값 아님이다.


| ID | Flag | RispostaA | Allarme1 | CSV 실제 행 |
| --- | --- | --- | --- | --- |
| VR01 | DB2,X1.1 | DB11,X32.0 | DB11,X32.1 | 440 /164 /118 |
| VR02 | DB2,X1.3 | DB11,X36.0 | DB11,X36.1 | 29 /28 /30 |
| SC01 | DB2,X1.6 | DB11,X44.0 | DB11,X44.1 | 445 /410 /123 |
| VR03 | DB2,X2.5 | DB11,X58.0 | DB11,X58.1 | 452 /417 /129 |

DB11 표시를 물리 입력이나 DB3 직접 고장 비트로 치환하지 않는다. HMI 이벤트·버튼 쓰기 방식·화면 객체·통신·현재 결속은 미확인이다. 기존 SC01 초안의 LAD1199 결속 미확정도 유지한다. 이 표의12설정행을 P14 소유 HMI12개로 세지 않는다.


### 2.4 CY02 위치의 경보등

전기 FG17/PDF18·FG143/PDF144는17HL1을 LAMPALARM, A7.7, CPU515/MOD15 출력단자38 경로로 표시한다. 원본 선언 0567-IdentXmlPart.xml RID39 Blinking Ligh, Bool/Global Output AO63(Q7.7), NID5/UID281 Write가 LAD933 0155-FlgNet.xml의 SCoil270/Wire291과 결속된다. 같은 네트워크의 Siren은 RID44 Output AO62(Q7.6), UID279, Coil265/Wire288이다.

LAD933의 Flag.RUN_HORN(UID275/Part296)과 Flag.M_HORN(UID276/Part298)은 OR256으로 들어가며 Wire295가 타이머·Siren Coil·PBox 등에 분기한다. Blinking Ligh Set은 PBox268.out→Wire290→SCoil270이다. 따라서 명칭·원본 연결은 공통 경보 기능의 일부를 지지하며 **CY02 본체 고장전용 출력**이라는 근거가 아니다. 이전 네트워크의 다른 Write·전체 경보 집계/해제는 이 식별 범위에서 완결 분석하지 않았다. 시공31/58의 CY02라는 LOC만으로 PLC 소유를 옮기지 않는다.


## 3. 원본 제어 구조와 본체/구동 분리


### 3.1 VR01·VR02·VR03 명령은 독립돼 있다

각 네트워크의 Global/UID/RID/NID와 Wire를 직접 대조했다. 세 구동은 비슷한 구조지만 별도 피연산자·출력이다.


| 구동 | LAD·원본/NID | 요청 Reset 경로 | 출력 경로 |
| --- | --- | --- | --- |
| VR01 | 1949 / 0251-FlgNet.xml /20 | ON622→FAULT624→Wire625→RCoil604, ORef611/RID103 | ON622→M_VR_01 접점626→Wire627→Coil608, ORef613/RID104 |
| VR02 | 1952 / 0254-FlgNet.xml /23 | ON711→FAULT713→Wire714→RCoil693, ORef700/RID120 | ON711→M_VR_02 접점715→Wire716→Coil697, ORef702/RID121 |
| VR03 | 1966 / 0266-FlgNet.xml /36 | ON1038→FAULT1040→Wire1041→RCoil1020, ORef1027/RID176 | ON1038→M_VR_03 접점1042→Wire1043→Coil1024, ORef1029/RID177 |

즉 선택 네트워크의 정적식은 각각 ON AND 자기 FAULT → 자기 요청 Reset, 별도 ON AND 자기 요청 → 자기 Start Coil이다. 0602의 Start 선언과 0604의 요청/고장 선언이 일치한다. ON을 항상 참으로 가정하지 않으며, 다른 요청 Set·HMI·호출 순서·유지성·현재 스캔의 최종값은 이 식별 조사만으로 확정하지 않는다. 이 네트워크에 CY 본체 명령이 따로 들어 있다고 읽지 않는다.


### 3.2 SC01과 VR03 관계의 최소 재확인

기존 drafts/SC01-DOTS-DRAFT.md의 전체 재조사를 반복하지 않고, P14 후보군을 구별하는 LAD1956 0258-FlgNet.xml/NID27과 선언만 직접 재확인했다.

- ON Part819에서 SC_01_FAULT Part821→OR790.in1.
- 다른 가지는 NOT Inputs.VR03 Run Part22→NOT UNDER TESTING Part825→OR790.in2.
- OR790.out/Wire812→RCoil795→ORef804/RID136 Flag.M_SC_01 Reset.
- 별도 ON819→M_SC_01 접점827→Wire828→Coil799→ORef806/RID137 Start SC01.
- 0604 RID219/UID23은 Inputs.VR03 Run, 0602 RID4/UID803은 UNDER TESTING이며 두 부정 접점을 보존한다.

정적 Reset식은 (ON AND SC_01_FAULT) OR (ON AND NOT VR03_Run AND NOT UNDER_TESTING)이다. VR03 처리응답이 SC01 요청 해제에 기여하므로 물리 공용배출 연결과 일관되지만, 이것은 **CY02/04/05 각각의 배출센서** 또는 P14 동일성 근거가 아니다. UNDER TESTING을 바꾸거나 안전을 우회하는 조치를 제안하지 않는다.

SC01의 자동 Set, 원시→처리입력, HMI 결속, 2초 직접 고장, FN04 공유 예고장·90분 타이머, 시간 계수 특이점은 기존 SC01 초안의 해당 항목과 미확정을 그대로 참고한다. 이번 P14 초안의 독립적인 전체 재검증 완료 항목으로 세지 않는다.


## 4. 전기·시공 전달 경로


### 4.1 실제 확인 페이지와 판본


| 원본 | 실제 PDF 쪽 | 표제/FG·확인 범위 |
| --- | --- | --- |
| P&ID1684n002I | 1 | 위 두 공정군, 판I/15.01.2013 |
| Electrical Rev2 | 47/50/54/62 | FG46 VR01 /FG49 VR02 /FG53 SC01 /FG61 VR03, 기본27.05.2024 |
| Electrical Rev2 | 7/18/97/144 | FG6 비상버튼 /FG17 경보 /FG96 질소박스 /FG143 출력 모듈. FG17/143은 Rev2 17.03.2025 |
| Can Decoating | 31 | CANDC-CONS-E014-031, FLOW_B ZONE01, M21/M23와 CY02의17HL1/6SB03 |
| Can Decoating | 35 | CANDC-CONS-E018-035, DUST ZONE01, SC01/M28 경로 |
| Can Decoating | 50 | CANDC-CONS-G002-050, 케이블 표기법: LOC는 설비 부위, TAG는 전장품, DC는 직류 디지털 컨트롤 |
| Can Decoating | 51 | CANDC-CONS-C001-051, 전력 케이블1_16/17/22/23 |
| Can Decoating | 58 | CANDC-CONS-C008-058, CY02 경보등8_16, 가려진 행 유지 |
| Can Decoating | 64 | CANDC-CONS-C014-064, CY02 비상버튼14_5/14_6 |

FG번호와 PDF쪽은 다른 값이며 전 문서에 고정 +1 규칙을 적용하지 않는다. 확인한 실제 표제부를 기준으로 썼다. 렌더 PNG와 해당 페이지 텍스트는 extracts/P14/에 있다.


### 4.2 구동별 명령·전력·접촉기 응답


| 별도 구동 | 전력 경로 | 명령 경로 | 응답 경로 |
| --- | --- | --- | --- |
| VR01/M21 | 8.3L1/2/3→46QM1→46KM1→XM46U/V/W1→46QS1→M21 | A2.6(138/1)→XS31→46QS1 보조→XS32→46QM1 보조→46KM1 A1/A2→0V | +24Vdc10.7→46KM1 13–14→E3.4(119/5) |
| VR02/M23 | 8.3L1/2/3→49QM1→49KM1→XM49U/V/W1→49QS1→M23 | A3.0(139/1)→XS35→49QS1 보조→XS36→49QM1 보조→49KM1 A1/A2→0V | +24Vdc10.7→49KM1 13–14→E3.7(119/7) |
| SC01/M28 | 8.3L1/2/3→53QM1→53KM1→XM53U/V/W1→53QS1→M28 | A3.4(139/1)→XS43→53QS1 보조→XS44→53QM1 보조→53KM1 A1/A2→0V | +24Vdc10.7→53KM1 13–14→E4.4(120/5) |
| VR03/M37 | 8.3L1/2/3→61QM1→61KM1→XM61U/V/W1→61QS1→M37 | A4.3(140/1)→XS59→61QS1 보조→XS60→61QM1 보조→61KM1 A1/A2→0V | +24Vdc10.7→61KM1 13–14→E5.4(121/5) |

각 회로의 전력 접점은1–2/3–4/5–6이며 모터 U/V/W/PE가 표기된다. 보조 QS/QM의 개별 접점번호는 해당 렌더에 없는 것을 임의 채우지 않는다. 각 응답은 접촉기 상태를 보고하므로 축·로터리 내부·실제 분진 흐름 정상까지 뜻하지 않는다.

시공51의 전력 케이블은 각기 1_16 =FLB+VR01-M21A, 1_17 =FLB+VR02-M23A, 1_22 =DUS+SC01-M28A, 1_23 =DUS+VR03-M37A, FROM CR, TO 각 구동, GAC/CV/4심/1.5/spare0다. 위치/기능 태그가 독립인 사실을 지지하지만, 시공 케이블명에서 전기 도면의 특정 단자·심선까지 이어지는 준공 연결표는 미확보다. SC01의 전체 회로 상세는 기존 초안을 참조한다.

VR 세 회로의 QM 1.1–1.6A, 모터 0.55kW/1.25A 및 SC01 5.5–8A, 3kW/5.8A는 도면 정격/범위 표기다. 실제 보호 설정이나 변경 지시가 아니다. 현행 제조사·교체품·정비 토크·정상 극성은 명판/승인자료 없이 기입하지 않는다.


### 4.3 CY02 위치의17HL1은 본체 계측 채널이 아니다

- 시공31은100LDD1 경로에서 M21/VR01, M23/VR02,17HL1/CY02,6SB03/CY02를 각각 다른 행으로 표시한다. UC01 질소박스와 PV05/06도 별도 경로에 있다.
- 시공58 행8_16: =FLB+CY02-17HL1A, FROM UC01/FLO4TB1 → TO CY02/17HL1, DC/CVV/3G/1.0/spare0, 루트E300→120RBD1→100LDD1→E300, Adjustment20/LEN36 표기. LEN은 이 문서에서 현장 실측값으로 확정하지 않는다.
- FG17/PDF18: A7.7→X1/42의5×20 2A IST 퓨즈→선17.2→17HL1 X1/X2→X1/43→−0Vdc10.6. FG143/PDF144에서 CPU515/MOD15 단자38의 A7.7과17/5 참조가 대응한다.
- 시공의 접속함 FLO4TB1 내부 단자/심선과 이 회로의 X1/42·43을 끝까지 연결한 자료는 없다. 위치명을 근거로 현재 같은 경보등인지, 패널/원격 구성이 어떤지 단정하지 않는다.
- 원본 PLC 명칭은Q7.7 Blinking Ligh이며 별도 Q7.6 Siren도 있다. **CY02 위치표기와 전체 경보 표시소유는 구분한다.**


### 4.4 비상버튼·질소 경계와 보존할 상충

- 시공31의 CY02 버튼은 도식6SB3/표6SB03이다.14_5와14_6을 모두 =FLB+CY02-6SB3A로 적지만, 시공64는14_5=...6SB3A,14_6=...6SB3B다. 서로 다른 실제 케이블2개인지/오기인지 임의 수정하지 않는다.
- 시공64에서14_5는 UC01/NVBOX→CY02/6SB3,14_6은 CR→CY02/6SB3이며, 둘 다 DC/CVV/2C/0.75/spare0이다. 시공50은DC를 직류 디지털 컨트롤로 정의한다.
- FG6/PDF7의6SB3(PB3)는X1/364·365의13–14 접점과 별도21–22 접점(96/3.2 참조)을 구별한다. FG96/PDF97에는X2/5→X1/366→6SB3→X1/367→X2/8의 질소 비상분기,96KA1/96KA2·PV05/PV06·96KT1/96KA3가 존재한다.
- FG96의96T1은220V/110V이고 질소 분기 전원은 변압기 110V 측에 연결된다. **특히14_5(NVBOX→버튼)의 시공 DC 분류와 이 질소 접점 회로를 같은 회로로 연결하기 전에 양끝 단자와 적용 판본 확인이 필요하다.** 다른 접점의24V 경로와 섞어 전압·극성을 확정하지 않는다.
- 시공58에는8_5와8_7/8_8 위치가 검은 띠로 가려져 있다. 텍스트 층에서 보이는 삭제/가림 내용을 활성 배선으로 복원하지 않는다.
- CY02 LOC의 램프·버튼이 질소/비상 공통 기능과 접해 있다는 사실은 CY02 본체에 새로운 자동 안전제어·성능 알람을 부여하는 근거가 아니다. 질소·비상회로 내부 운전절차, 시험 및 변경은 이번 조사 범위 밖이다.


## 5. 알람과 복구의 소유 경계


### 5.1 VR 구동 고장은 별개다

각 원본 알람 네트워크는 아래 구조를 가진다. 타이머와 고장명을 CY01/03/02 등의 본체 고장으로 바꾸지 않는다.


| 구동 | LAD/원본/NID | 원시 명령·처리응답과 타이머 | 고장 Set/Reset |
| --- | --- | --- | --- |
| VR01 | 1797 / 0432 /19 | ON683→Start685→NOT RUN696→SdCoil647, Tag_62 ORef662/RID78, S5T#2S ORef661/RID28 | Timer접점687→SCoil653→FAULT665; ON→RESET691→FAULT693→RCoil658/FAULT668 |
| VR02 | 1799 / 0434 /21 | ON751→Start753→NOT RUN764→SdCoil715, Tag_64 ORef730/RID86, S5T#2S ORef729/RID28 | Timer접점755→SCoil721→FAULT733; ON→RESET759→FAULT761→RCoil726/FAULT736 |
| VR03 | 1810 / 0444 /32 | ON1125→Start1127→NOT RUN1138→SdCoil1089, Tag_75 ORef1104/RID131, S5T#2S ORef1103/RID28 | Timer접점1129→SCoil1095→FAULT1107; ON→RESET1133→FAULT1135→RCoil1100/FAULT1110 |

- 명령/Timer의 Global 선언은 0658, 처리RUN·고장·RESET_ALLARM은 0657, 상수는 0656-IdentXmlPart.xml의 같은 NID/UID로 결속했다. 상수 원문은S5Time S5T_x0023_2S, 저장값512이며512ms로 읽지 않는다.
- 선택 네트워크의 정적식: ON AND Start AND NOT 처리RUN이 타이머 입력, ON AND Start AND Timer접점이 고장 Set, ON AND RESET_ALLARM AND 자기FAULT가 Reset이다. Reset분기에 처리RUN 정상 확인은 없다. 따라서 고장 비트 해제만으로 결함 해결·실제 회전·안전 재기동·분진 배출 정상이라고 판정하지 않는다.
- 세 VR 고장이 자기 요청 Reset으로 연결된 것은3.1에서 확인했다. SC01 고장과 FN04 공유 예고장은 기존 SC01 초안의 별도 소유 항목이다.
- CY 본체의 차압·온도·막힘·분리효율 전용 알람·복구 기준은 미확보다. BF차압이나 인접 TC/RO/팬 고장을 CY 본체로 옮기지 않는다. 공통17HL1이 켜졌다는 사실만으로 어느 본체가 원인인지 알 수 없다.


## 6. 증상별 식별·관찰 계획

실제 현장 관찰·수리·조치를 수행한 기록이 아니다. 관찰은 자격 있는 담당자가 승인된 안전절차에 따라 수행하며, 회로 강제출력·보호값 조정·비상/질소 시험·안전 우회를 뜻하지 않는다. 고온·분진·잔류압력·회전체 접근은 현장 절차를 우선한다.


| 증상/상황 | 먼저 확보할 위치·값 | 비교 근거·배제해야 할 오해 | 복구/판정에 필요한 증거 |
| --- | --- | --- | --- |
| ‘2사이클론’이 어느 것인지 모름 | 원 배치도에서 표시한 전체 장면·지칭, 본체 태그, 입구/상부출구/하부배출 | CY01/03 병렬 쌍 vs CY02/04/05 공용SC01 군 | 작성자 의미 + 현재 태그/연결이 일치하는 증거 |
| 한 본체만 분진이 안 나옴 | 해당 본체 하부와 VR01/M21 또는 VR02/M23 연결, 가스 분기 | Q/I 정상은 접촉기 정상일 뿐 로터리 내부/실제 이송 정상과 다름 | 안전 확보 후 기계 연결·막힘 관찰 및 승인된 정상 배출 근거 |
| 세 본체 군에서 공통으로 배출 안 됨 | CY02/04/05→SC01→VR03 연결, M28/M37, 요청·출력·응답 동시각 | SC01 고장/VR03 응답상실과 개별 CY 이상 분리 | SC01 기존 관찰항목, VR03의 구동·기계 상태, 실제 배출 복귀 |
| 주변 경보등만 켜짐 | 17HL1 실물 위치/명판/케이블, Q7.7·HMI 최초 경보 | 위치CY02≠CY02 전용 고장; 공통 경보집계와 개별 고장 분리 | 같은 시각 실제 경보 목록·원인 비트·표시 경로 |
| 현장 버튼 또는 케이블명이 자료와 다름 | 6SB3 접점별 양끝/단자·케이블14_5/14_6·적용 개정 | A/B 접미어 상충, DC vs 질소110V 경로를 임의 연결하지 않음 | 승인 준공도·접점별 배선표·변경 이력; 식별만으로 시험 실행 금지 |
| 팬/온도/압력 이상을 사이클론 고장이라 부름 | 발생 위치, FN01 또는FN04 계통, 관련 센서의 실제 태그 | 순환과 집진 군 구분, 공유 계측을 본체 소유로 변경 금지 | 현재 P&ID/PFD와 계측 소유, 제조사 승인 정상범위 |

관찰 항목은 관찰자·시각/시간대·위치·태그·원시값/단위·자료/기기 개정·비교 근거·배제 결과·승인 조치·전후 결과를 분리한다. 누락을0/정상으로 채우지 않는다. 운영 사진·SEJIN 이력을 이 초안에 복사하지 않았다.


## 7. 완료 기준·필요 현장 증거·다음 조치


### 7.1 가장 작은 식별 증거 묶음

다음 세 묶음이 있으면 번호/수량/단계 가설을 실제로 구분할 수 있다. 지금 없는 증거는 ‘확보 예정’ 또는 ‘확인 완료’로 쓰지 않는다.

- **명칭 의미:** 원 배치도에서 P14 ‘2사이클론’을 표시한 장면과 작성자/사용자의 정확한 지칭. ‘2번’, ‘두 대’, ‘2차’ 중 의미가 명시된 설명과 자료 날짜.
- **실물 연결:** 각 대상 본체의 읽을 수 있는 태그/명판, 동일 대상임을 이어서 보여주는 전체도·입구·상부출구·하부배출. HE01/FN01와 연결되고 개별VR01/VR02인가, SC01/VR03을 공용하는가를 확인할 수 있어야 한다. 사진만으로 가려진 배관을 추정하지 않는다.
- **구동·전기 동일성:** M21/M23 또는M28/M37의 명판/현장표찰, 최신 P&ID/배치도·준공 단자/케이블심선표.17HL1/6SB3가 식별에 쓰일 경우14_5/14_6과8_16의 양끝, 접점/전원, 적용 판본도 필요하다.

확정 판단은 최소한 원 배치도 의미와 실물 태그/유로라는 서로 다른 증거가 일치해야 한다. 하나가 충돌하면 후보 상태를 유지하고 충돌을 기록한다. 두 기를 묶어 부른다는 결론이면 P14는 두 catalog ID와의 관계로 별도 설계해야 하며, 기존 두 ID/운영 기록을 병합하는 권한으로 쓰지 않는다.


### 7.2 네 기능과 기록 보존


| 기능 | 이번 범위 | 후속 조건 |
| --- | --- | --- |
| 도면·래더 나란히 비교 | 두 PID군↔VR/SC 회로·원본 링크 대상만 정리 | 미식별 P14에 타구동 신호를 소유로 표시하지 않는 설계·독립검토 |
| 백업·선택 복원 | 미수행 | P14 우선키와 확정 전 catalog키를 분리, 기존 note/repair_observation·미지 필드·초안·타설비 키 보존 |
| 기록 전후 비교 | 미수행 | 현장 식별근거/판본·시각을 보존하고 단순 이름 변경으로 기록 병합 금지 |
| 보고서/PDF | 초안 MD만 작성, 사용자용 보고서/PDF 생성 미수행 | 구현이 승인되면 독립 기능·렌더·기록 검증 수행 |


### 7.3 실제 상태


| 항목 | 상태 | 의미 |
| --- | --- | --- |
| documentation | identification_draft_complete_with_gaps | P14 식별 조사 7영역 초안; 설비 동일성·CY별 전체 매뉴얼 완료 아님 |
| identity | unresolved | catalog_id=null 유지 |
| static_review | source_review_performed; bounded_independent_review_complete | 고정 원본 해시·후보 분리·핵심 PDF 제한 검토 완료; PDF50 도면번호 정정 |
| ui_records | not_run | UI/저장/재열기/복원 구현·검사 안 함 |
| publication | not_published | 원본 코드·버전·배포 변경 없음 |
| tia_compile / live_cpu | not_performed | 현재 CPU/프로젝트 상태 추정하지 않음 |
| field_recovery | not_performed | 실물 동일성·복구 검증 없음 |

작업3의 CY01~05 보류는 유지한다. 같은 자료로 미식별 문제를 반복 조사하기보다 위 명칭·실물·유로 증거를 받아 P14 대응을 검토하는 것이 다음 한 작업이다. 본 초안을 ‘P14=CY02 해결’이나 신규CY5건 완료로 집계하지 않는다. 독립된 다른 작업은 이 현장 증거를 기다리며 중단할 필요가 없다.


### 7.4 수행한 정적 확인과 재현 범위

- Git HEAD와 v1.12.0, 읽기 전용 preflight 및 대장/parent/하위 필드 대조.
- 원본 PDF를 PyMuPDF로 렌더하여 위 확인 페이지와 PID 전체·확대·표제부 시각 검토. 원본 파일은 저장/수정하지 않음.
- ElementTree로 원본 선언 및8개 선택 네트워크(0155,0251,0254,0258,0266,0432,0434,0444)의 Part/Wire/ORef·같은NID/UID/RID 결속을 추출. 추출 JSON은 근거 탐색 파일이며 제어를 실행하는 프로그램이 아님.
- 명시적CY 검색은XML695파일/HMI782행에서 일치0. 검색 부재를 현장 장치 부재로 확대하지 않음.
- 기존 SC01 초안에서 관계 경계를 재사용했고 SC01 문서를 편집하지 않음.
- npm/build·UI·패키지·배포·TIA/CPU/현장·시뮬레이터 실행은 하지 않았다. 자체 정적자료 조사 이외 검증 완료를 표시하지 않음.


### 7.5 독립 최종 검토 정정

2026-10-11 UTC 독립 최종 검토에서 시공 PDF50의 표제부를 원본에서 3배 재렌더하고 텍스트층과 대조했다. §4.1의 도면번호 CANDC-CONS-C002-050은 오독이며 정확한 번호는 CANDC-CONS-G002-050이다. 기존 draft-qc의 “C002로 시각 확인했다”는 기록도 오독 이력으로 남기고 정정했다. 이 정정은 P14의 catalog_id=null·동일성 미확정·후보 분리·작업3 완료 미산입 판정을 바꾸지 않는다.

최종 검토는 고정 커밋·근거 SHA256, 세 식별 초안의 판정 경계와 핵심 PDF 몇 곳에 한정했다. 전체 로직 재조사, UI·현장·TIA·CPU·게시 또는 설비 동작 검증을 추가 수행한 결과가 아니다.


## 부록 A. 핵심 근거 SHA-256

다음 표는 조사에 사용한 고정 원본 및 입력 초안의 정확한 바이트 해시다. P14 초안 자체 해시는 별도 extracts/P14/P14-IDENTIFICATION-DRAFT.sha256에 있다.


| 원본 또는 입력 파일 | SHA-256 |
| --- | --- |
| AGENTS.md | 0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2 |
| .agents/skills/gme-equipment-rollout/SKILL.md | fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b |
| .agents/skills/gme-equipment-rollout/scripts/preflight.py | 395067d6da20af3e1d82a43b7936907a87a44d8d2e11e4ebc61b1fc441e2adb6 |
| VERSION.json | 5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7 |
| docs/equipment-standard/WORK-STANDARD.md | 05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99 |
| docs/equipment-standard/WORK-ITEM-TEMPLATE.md | 4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586 |
| docs/equipment-standard/INVENTORY.json | 720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc |
| all-in-one/registers/equipment.json | 7870325dff32bbca90fa34507b301c4aad3347d669fddcd03b910343663996fa |
| all-in-one/registers/priority-equipment.csv | 953c2c4df5b3a6e40d926d1f0f08f91900b7d6565e4dcd64191b548e438edeba |
| all-in-one/registers/all-in-one-data.json | 63a46b36b6454bf1246d093300dbee11f2fcc287ad94991405369bf9f939a8fe |
| all-in-one/registers/unresolved-identity.json | 28d15988a3c23ce56a6142636a409e65cdfaf6575662da71d9f0d4636646ea21 |
| all-in-one/registers/unresolved-identity-independent-review.json | c33c349d82e73f5e7055e2c909adc41f47f9279e2de228522fb229f4564b7f04 |
| all-in-one/sources/PID_1684n002I.pdf | 2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b |
| all-in-one/sources/Electrical_Rev2.pdf | 5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6 |
| all-in-one/sources/Electrical_Can_Decoating_20241118.pdf | 3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd |
| all-in-one/sources/hmi_plc_tags.csv | a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404 |
| all-in-one/sources/decoded-original/network-map.json | c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60 |
| all-in-one/sources/decoded-original/0155-FlgNet.xml | fd669dc6d8bc9e2486fda4691bf91927c195fd5cb1b6ee57535b52ec9b40e3c6 |
| all-in-one/sources/decoded-original/0251-FlgNet.xml | 6446b2b475b59f69889a408df794d2ed43cc6343f999045c00243b6d0663e017 |
| all-in-one/sources/decoded-original/0254-FlgNet.xml | 568a4cfb029a4f1a8babf2e3ad2c515d9ca52655890bf65446cca2f796859258 |
| all-in-one/sources/decoded-original/0258-FlgNet.xml | d585f05c02cf6d0579ece6f4081e9c52a3135fd8c4720f915f0dfdc0d510ac9b |
| all-in-one/sources/decoded-original/0266-FlgNet.xml | f11ba1455884c2b0a1085f1892445a86325760be78cd8c9cd70f8ede77f9a992 |
| all-in-one/sources/decoded-original/0432-FlgNet.xml | a002d92b22e40a8fc12270f2995291f329392f9b7894f09f3b607b11caeb4c65 |
| all-in-one/sources/decoded-original/0434-FlgNet.xml | 31c8de50439465d356d0735765fa0ab0983585e0f1fbfab6bf614b054566f3f9 |
| all-in-one/sources/decoded-original/0444-FlgNet.xml | 718076435066a62dc890a414988dc00824025a94d5757799a519071fb69b694c |
| all-in-one/sources/decoded-original/0565-IdentXmlPart.xml | 0f7f970faa6c456f2bb032b1a2072a2f52db1e03fc77bd8d35d4583deeaf1149 |
| all-in-one/sources/decoded-original/0567-IdentXmlPart.xml | 5d428b5d5a2b0f4649dbbbb4e4f060a9d89a107e9cf4b6139d8f003c4371347e |
| all-in-one/sources/decoded-original/0602-IdentXmlPart.xml | 46ab21151eddaaf616469db520730c60423eb742aa491af194e6710c751b4caf |
| all-in-one/sources/decoded-original/0603-IdentXmlPart.xml | e93969dfa281d75b49b24127793068e33472dadb19729c1c48fc4a8dad075ef8 |
| all-in-one/sources/decoded-original/0604-IdentXmlPart.xml | b798d29c5499b5314a1ee3cff9139dae64c887533b86baa43b6e9a052373a6af |
| all-in-one/sources/decoded-original/0613-IdentXmlPart.xml | 09d3b1397a987898334218f37e025661af162438582e649f671e7abec443d3cb |
| all-in-one/sources/decoded-original/0656-IdentXmlPart.xml | 0dbc45e84732a8848f17b094ea08ab8578dbf240bfe15cd7086859395c27c592 |
| all-in-one/sources/decoded-original/0657-IdentXmlPart.xml | 0f70cda60a6b1a17175876d58e25b2686952642de6cffb21213aeef8b347a22b |
| all-in-one/sources/decoded-original/0658-IdentXmlPart.xml | 998294c0c8a99e00ceb33c2c60def2cd4850e34328917ae506244c2be2df3831 |
| input:gme-research/progress/GME-CATALOG-OVERLAP-REVIEW.md | 51ecc3d631967fafdb75570ed989ccf8fa1759f3eaeb786b4f5dfa90bba352ca |
| input:gme-research/progress/GME-CATALOG-OVERLAP-REVIEW.json | 027c2d89b034f3681dced7db98146ffd77eecfad116a1a94cac035ccbd598967 |
| input:gme-research/drafts/SC01-DOTS-DRAFT.md | 9a9540d01cb9e0705572fe10d51d44281dcbae99569d12e6f0afbd722ad4a337 |

핵심 원본 해시 37개. input:은 고정 저장소 밖에서 제공받은 조사/대조 자료이며, 직접 원본 근거와 같은 등급으로 취급하지 않는다.
