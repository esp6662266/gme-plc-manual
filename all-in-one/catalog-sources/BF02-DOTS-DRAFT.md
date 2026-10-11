# BF02 백 필터 본체·세정 제어 원본 조사 초안

BF02는 BF01과 이름이 같은 별도 백 필터다. 원본의 BF02 세정 허가는 SC11·VR05의 **처리 응답이 모두 참**일 때 차압 비교 또는 공통 Forza_Lavaggio를 받는다. 비교 상대는 원문 그대로 **DP_02 <= DP_01_SOGLIA_1**이다. Forza에는 2시간/10분 타이머 외에 ON 가지가 병렬로 있다. 이를 “BF02 차압이 높을 때만 세정” 또는 “2시간마다 10분만 강제 세정”으로 단순화할 수 없다.

세정 출력 EV51~90은 Q18.0~Q22.7이다. 밸브 이름과 공통 순번은 같지 않다. EV51은 순번12, EV52는14, EV90은90이다. BF01·BF02가 공통 시간·순번을 쓰므로 BF02만의 독립 타이머/독립 스캔으로 설명하지 않는다. BF02_RUN은 세정 허가를 따르는 메모리 비트이며 백 필터의 실제 집진·밸브 작동·분진 배출 완료를 검출한 신호가 아니다.

이 문서는 작업3 자체 조사 산출물이다. 매뉴얼 통합·UI/기록·배포·TIA 컴파일·현재 CPU·현장 복구 완료가 아니다. BF02의 문서 작성으로 SC11·VR05·DP02·EV51~90의 완료를 상속하지 않는다.

## 작업 기준·범위·보존

- catalog_id BF02, 이름 백 필터, kind filter, 집진·석회, parent_id 없음, depth0, priority_key 없음. INVENTORY catalog[89], equipment[49]. 별칭 pr_bf02/pr_br02/bf_02/filter 2. BF01과 이름은 같으나 고유 ID가 다르다. pr_br02는 DP02에도 있으며 문자 검색의 중복이지 동일 실물 확정이 아니다.
- 작업3 네 번째 5개 묶음 중 BF02 한 개. TASK3-BATCH04-SCOPE.json의 중복·제외·부모 범위 검토 후 착수했다. 전체248 ID, 우선23행, 기존 제외90, 제외 부모 하위보류7, phase2 후보133을 변경하지 않는다. 로컬 2차133 통합 제외를 유지한다.
- 고정 읽기 원본 source-mv06, Git abcf31c5030bc7ef8749ed8e869a857f2387a28a, 프로그램 v1.12.0. 저장소 https://github.com/esp6662266/gme-plc-manual. 이후 main·현재 CPU·준공 상태와 동일하다고 전제하지 않는다.
- AGENTS.md, gme-equipment-rollout/SKILL.md와 source-map, GME-STD-1.0.0 WORK-STANDARD, WORK-ITEM-TEMPLATE, INVENTORY, 버전·인계·게시·진행 기록을 읽었다. 읽기 전용 preflight 종료0, inventory_matches=true. requirements-audit.json/all-in-one-data.json의 기존 source_byte_changes는 보존했다. 대장 일치는 설비 완료 판정이 아니다.
- 조사일 2026-10-11 UTC. 실행 모델/추론 수준의 런타임 증명은 별도 미확보. 작성·정적 자체 대조 완료, 별도 독립 검토는 대기다.
- 수정 범위는 이 초안과 extracts/BF02 아래 조사 추출·렌더·해시 파일뿐이다. 공용 declarations, 다른 초안, 원본, 공통 코드·버전·대장·배포·운영 기록을 수정하지 않았다.
- 시뮬레이터 작성·수정·생성·실행·행동 시험0, 실제 PLC·현장·보호값 변경0, SEJIN 프로그램·운영 자료·사진·이력 복제/통합0. 정적 XML 읽기와 PDF 렌더만 수행했다. 중지5자산은 해시만 확인했다.
- 부록 B의 파일 해시 수는 바이트 보존 검사 수다. 의미 검토 수와 별개다. 핵심 경로 의미 검토는 부록 A의 28개 고유 FlgNet에서 명시한 경로, EV40개 출력 가지, 원본 PDF18개 고유 페이지다. PDF 크롭/회전 렌더는 같은 페이지로 세었다. 28개 네트워크 전체 프로그램 의미나 PDF 전체 페이지를 완료 검토했다는 뜻이 아니다.

아래 0219 등 네 자리 번호는 all-in-one/sources/decoded-original/0219-FlgNet.xml이다. 선언0596은 같은 폴더의0596-IdentXmlPart.xml이다. LAD/document_id, index_order, NID는 다른 식별자다. XML이 한 줄인 선언은 RID/UID/NID/BAD/BO로 위치를 식별한다. 검색 색인은 탐색·LAD 대응에 쓰고 최종 조건은 실제 Part/Wire/ORef와 선언으로 대조했다.

## 7영역 적용표

| 영역 | 적용 상태 | 확보 범위 | 남은 경계 |
|---|---|---|---|
| 설비·자료 기준 | 적용 | BF02/독립 ID/공통·하위 소유/자료 시점 | 현행 명판·실물·승인 준공 동일성 |
| I/O·HMI | 적용, 일부 근거 미확보 | 세정 허가/순번/출력40/Word 전달/HMI 설정8행 | 실제 이벤트·쓰기 권한·실시간 주소·현재 값 |
| 제어 구조 | 적용 | 공통 Forza·시간·BF02 허가·순번·40개 출력·호출·다중 쓰기 | 스캔/컴파일/외부·간접 쓰기/현재 최종값 |
| 전기 전달 경로 | 적용, 일부 근거 미확보 | JB2 전원·모듈·EV51~53/90 끝점·DP02 경계·시공 케이블 상충 | EV54~89 부하 회로의 전수 핀 검토·현행 배선·단자 대응 |
| 알람·복구 | 적용 | 공유 MAX_DP_FILTER 3분 Set/Reset/Word0, BF02_OFR 인터페이스 | 모든 공통 알람 소비·사이렌·정지 영향/현장 복구 |
| 증상별 수리 | 적용, 관찰 설계 | 허가→순번→Q→계전기→부하·DP/표시 비교 | 실제 관찰·조치·재요청·복구 증거 없음 |
| 완료 기준 | 적용 | 정적 조사·충돌·부족자료·검증 상태 분리 | 독립 검토·통합/UI/게시/TIA/CPU/현장 별도 |

## 1. 본체·하위·주변 소유

1. P&ID PID_1684n002I.pdf p1의 BF-02에는 EV51~58/59~66/67~74/75~82/83~90의 다섯 섹터, DP-02, SC-11/M35, VR-05/M39가 함께 그려진다. SC11은3kW440V, VR05는0.55kW440V라는 도면 표기가 있다. 이것을 BF02 본체 모터 정격으로 복사하지 않는다.
2. 대장 SC11·VR05·DP02는 각각 독립 root ID다. EV51~90만 parent=BF02인40개 catalog ID다. 이 조사에서40개 PLC 출력 조건을 대조했어도 각 밸브의 현장/문서/UI 완료40건으로 세지 않는다. 전기 도면의5섹터×8개와 시공 분전함 JB02TB1~4의10개씩 묶음도 서로 다른 분류다.
3. BF02의 집진 성능·백 손상·누설·차압과 세정 출력은 다르다. 검토한 세정40개 가지에는 개별 밸브 실제 위치·펄스 압력·분진 배출 완료 피드백이 없다. 그런 센서가 현장에 전혀 없다는 단정은 하지 않는다.
4. 공통 Filter 블록 안의 FN04 시작속도/흡인제어(0213/0214), PV14 냉풍밸브 고장/제어(0215/0216)는 BF02 전용 기능으로 편입하지 않는다. 해당 부분은 검색·추출만 했고 BF02 핵심 의미 검토28개 수에서 제외했다. SC11/VR05 자체 운전·전용 고장도 해당 ID 소유다.
5. P&ID 원 작성06/04/2011, 도번1684n002, Apex I, 개정 I 15/01/2013을 타이틀과 실제 크롭에서 확인했다. 이 도면의 AIR6~8Bar, Max180℃, DP setpoint5~10mbar는 당시 도면 문구다. 현재 보호·운전 권장값으로 채택하지 않는다.
6. 원본 PLC 백업명 GME_20250506.zap18, 전기 개별 시트 기본일27.05.2024, 시공 first draft design24.11.11, P&ID 판I는 시점이 다르다. 파일명 Electrical_Rev2.pdf만으로 모든 시트의 Rev2를 주장하지 않는다.

## 2. I/O·선언·HMI

### 2.1 BF02·공통 세정 주요 선언

0596 GlobalAccess의 BO/AO는 bit offset이다. BAD2→0595 RID2 Data/TOD1, BAD7→0595 RID7 Coeff/TOD4, BAD303→0595 RID303 Inputs/TOD13을 대조했다. 아래 주소는 고정 백업 해석이며 현재 CPU 레이아웃 확인이 아니다.

| 신호 | 주소·형식 | 원본 위치 | 해석·미확정 |
|---|---|---|---|
| ON / OFF | M0.0 / M0.1 Bool | 0594 RID52 AO0 / RID1 AO1, SAD Memory | 실제 값·상시 참/거짓을 이름으로 단정하지 않음 |
| Abilita_lavaggio_BF02 | Local Bool, BO33 | 0598 RID65 NID29 UID46 Write, NID4 UID508 Read, NID10~17 다수Read | 필터 내부 허가. 물리 Q주소 아님 |
| Forza_Lavaggio | Local Bool, BO34 | 0598 RID57 NID3 UID437 Write, NID29 UID45 Read | 공통 강제 세정 조건. 현장 버튼·HMI명령으로 단정 금지 |
| BF02_RUN | M180.4 Bool | 0594 RID344 AO1444, NID29 UID79 Write | 허가연쇄의 일반 Coil. 실물 운전완료 감지 아님 |
| Inputs.FEEDBACKMOTOR SC-11 | DB13.DBX5.1 Bool | 0596 RID305 BO41, NID29 UID41 | 처리 응답. raw I5.1과 구분 |
| Inputs.VR05 Run | DB13.DBX5.6 Bool | 0596 RID319 BO46, NID29 UID42 | 처리 응답. raw I5.6과 구분 |
| SC-11_Fbk | I5.1 Bool | 0594 RID64 AO41, SAD Input, NID6 UID575/579 | OFF-Data.LAVA 선택은 처리값 대신 raw를 읽음 |
| Data.DP_02 | DB1.DBW242 Int | 0596 RID31 BO1936; NID29 UID43, NID2 UID464 등 | 차압 환산 결과. 현재 단위·계수 별도 |
| Coeff.DP_01_SOGLIA_1 | DB4.DBW138 Int | 0596 RID8 BO1104, NID29 UID44 | BF02 허가가 실제 읽는 DP01명 임계값 |
| Coeff.DP_02_SOGLIA_1~4 | DB4.DBW166/168/170/172 Int | 0596 RID32/37/41/45, BO1328/1344/1360/1376 | OFF 시간 선택 전용 비교 상대. 허가의 DP01상대와 다름 |
| Coeff.DP_02_PAUSA_SOGLIA_1~5 | DB4.DBW174/176/178/180/182 S5Time | 0596 RID34/39/43/47/50, BO1392~1456 | OFF 시간 선택의 다섯 pause 원본 |
| Coeff.DP_02_LAVORO_SOGLIA_1 | DB4.DBW184 S5Time | 0596 RID36 BO1472 | 다섯 단계 모두 이 동일 work 멤버를 읽음 |
| Data.LAVA | DB1.DBW230 Int | 0596 RID68 BO1840 | raw 응답에 따른0/1/2/3 다중 Move 대상 |
| Data.LAVA_START / END | DB1.DBW232 /234 Int | 0596 RID76/78 BO1856/1872 | OFF 범위 선택과 ON 11/90의 복수 쓰기 |
| Data.LAVA_PAUSA / LAVORO | DB1.DBW236 /238 Word | 0596 RID11/14 BO1888/1904 | DP01·DP02·ON 공통 시간의 복수 쓰기. 선언은 Word |
| Data.Ev_filter_on | DB1.DBW170 Int | 0596 RID3 BO1360 | 세정 순번. EV 번호·출력주소와 구분 |
| Data.VALVE_W / P | DB1.DBW318 /320 Int | 0596 RID291/290 BO2544/2560 | KF_KT 변환 입력. 현재 값·권한 미확인 |
| Coeff.DP_01_PAUSA/LAVORO_SOGLIA_1 | DB4.DBW146 /156 S5Time | 0596 RID10/13 BO1168/1248 | 공통 시간 네트워크가 BF02에도 사용하는 멤버 |
| Tag_129 / Tag_130 | T133 / T134 Timer | 0594 RID53/55 | 10분/2시간 SdCoil 대상. HMI태그 아님 |
| Tag_131 / Tag_132 | T1 / T2 Timer | 0594 RID60/61 | 공통 work/pause S5 타이머. BF02전용 아님 |
| PLS 50 3 | M50.3 Bool | 0594 RID89 AO403, NID27 UID31 RW | 순번증가 PBox의 edge 저장 비트 |
| EV51~90 | Q18.0~Q22.7 Bool | 0594 RID95~248 중 부록C의40개 실제 선언, SAD Output | 각 일반 Coil의 명령. 출력피드백 아님 |

### 2.2 입력·출력 Word 전달과 다중 쓰기

- 0397 LAD1070 hmi inputs/NID1: Move35.in←ORef36/RID10 Tag_180(W39), out1→ORef37/RID11(W40). 0627 Input/AO32 Word=%IW4, 0629 Word/AO32/BAD4, 0628 RID4 Inputs/TOD13이므로 IW4→DB13.DBW4다. I5.1/I5.6이 처리 DB13.DBX5.1/5.6 위치에 들어간다. Move22.eno→27.en(W34),27.eno→35.en(W41) 및 DisableENO 속성도 존재한다. 실제 실행 주기·ENO 결과는 확인하지 않았다.
- 0635 simulation 선언의 SC11 RID126/NID4 UID49와 VR05 RID134/NID4 UID65 처리값에 다른 Write가 존재한다. 정지 자산·원본 XML의 Writer 존재만 확인했으며 실행·행동 검증을 하지 않았다. Word Move 하나만 유일 Writer라고 설명하지 않는다.
- 0401 LAD356 hmi output/NID1은 **출력 영역을 읽어서 DB14에 쓰는** 전송이다. QW18→DB14.DBW18: ORef51/RID44 Tag_289→Move31.in W80, out1 W82→ORef52/RID58. QW20→DB14.DBW20: ORef53/RID46 Tag_290→Move32.in W83, out1 W84→ORef54/RID59. QW22→DB14.DBW22: ORef89/RID48 Tag_291→Move85.in W87, out1 W88→ORef90/RID49. 0632 SAD Output/AO144·160·176과0633 동일AO/BAD26,0064 RID26 Output/TOD14 대조. Q18~22의 Word 덮어쓰기로 오독하지 않는다.
- 단순 비트명 밖 영역겹침을 검색했다. 공개 선언 중 SAD Output·AK Write/RW에서 Q18.0~Q22.7 범위에 겹친 것은40개 EV Coil 선언이며 M180.4 범위는 BF02_RUN 선언이었다. 이는 해당 직접 선언 검색 결과다. 간접 주소·외부 HMI/통신·현재 CPU 강제·전체 DB 전송의 부재 증명은 아니다.
- MAX_DP_FILTER DB3.DBX9.5는 startup DB3.DBW8=0에도 포함된다(§5.2). BF02_OFR DB3.DBX24.5는 검토한 startup Word0~16 범위 밖이다. “시작 시 모든 BF02 알람이0”이라고 일반화하지 않는다.

### 2.3 HMI 설정8행과 이벤트 경계

sources/hmi_plc_tags.csv는 dde.cfg 설정이며 Access Name=PLC다. 명칭·선언·주소를 대조한 다음8행을 관련 설정으로 기록했다. 원본 화면의 실제 버튼·객체·쓰기 이벤트는 미확보다.

| 행 | 설정 태그 | 주소 | 내부 ID | 결속 범위 |
|---|---|---|---|---|
| 19 | BF02_RUN | MX180.4 | 00457 | M180.4와 직접주소 일치 |
| 17 | Allarmi_235 | DB3,X24.5 | 00459 | BF02_OFR의주소와 일치; 실제 표시문/확인동작 미확인 |
| 535 | Allarmi_78 | DB3,X9.5 | 0013F | 공유MAX_DP_FILTER주소 일치 |
| 218 | data_DB1_DBW170 | DB1,INT170 | 002BF | 공통 세정 순번주소 |
| 285 | data_DB1_DBW242 | DB1,INT242 | 00264 | DP02 환산결과주소 |
| 297 | data_DB1_DBW318 | DB1,INT318 | 00255 | VALVE_W주소 |
| 315 | data_DB1_DBW320 | DB1,INT320 | 00242 | VALVE_P주소 |
| 361 | Coeff_DB4_DBW138 | DB4,INT138 | 00205 | BF02허가가 읽는DP01임계값주소 |

HMI목록에 EV51~90 개별명이나 DB14.DBX18~22 개별비트 설정은 이 검색에서 찾지 못했다. DB14 전송을 확인했다고40개 HMI표시를 구현·검증했다고 세지 않는다. HMI창 검색에서도 BF02 객체/이벤트의 확정 경로를 확보하지 못했다. 설정주소 존재는 읽기/쓰기 권한이나 제어 사용 승인 근거가 아니다.

## 3. 제어 구조

### 3.1 BF02 세정 허가와 BF02_RUN

0219 LAD1886, filter index5/NID29. 원본0594·0596·0598을 해당NID/UID로 결속했다.

| 단계 | 원본 핀·선 | 정적 해석·경계 |
|---|---|---|
| 공통 | rail W47→Contact21; W48 ORef34/RID52 ON | ON이 첫조건 |
| SC11 | W49→Contact28.in; W61 ORef41/RID305→operand | 처리SC11응답 |
| VR05 | W62 Contact28.out→Contact29.in; W63 ORef42/RID319→operand | SC11·VR05 직렬 |
| 차압 | W64 Contact29.out→Le30.pre; W65 ORef43/RID31 DP02→in1; W66 ORef44/RID8 DP01_SOGLIA_1→in2 | Int DP02 <= DP01_SOGLIA_1. 이름/부등호 수정금지 |
| 강제 | 동일W64→Contact31.in; W68 ORef45/RID57 Forza→operand | Forza도상위 두 응답뒤에있음 |
| OR | W67 Le30.out→OR32.in1; W69 Contact31.out→in2 | 차압비교 OR Forza |
| 허가 | W70 OR32.out→Coil33.in; W71 ORef46/RID65→operand | Local허가일반Coil |
| 표시 | W76 Coil33.out→Coil78.in; W77 ORef79/RID344→operand | BF02_RUN=M180.4. 밸브피드백아님 |

정적 식: ON AND SC11 처리 응답 AND VR05 처리 응답 AND [(DP02 <= DP_01_SOGLIA_1) OR Forza_Lavaggio]. Forza가 SC11/VR05를 건너뛰는 식이 아니다. Coil.out 연결을 보존했으며 컴파일/현 CPU의 실제최종값은 별도다.

### 3.2 Forza_Lavaggio: 타이머 외 ON OR 가지

0200 LAD1885, index4/NID3. Contact451 ON(ORef429/RID52,W438)의 out W452가 네가지 분기로 나뉜다.

- NOT Tag129 Contact453(ORef431/RID53,W440)→W454→SdCoil418.in. value W439=ORef430/RID54 S5T#2H, operand W442=ORef432/RID55 Tag130(T134).
- Tag130 Contact455(ORef434,W444)→W456→SdCoil423.in. value W443=ORef433/RID56 S5T#10M, operand W446=ORef435/RID53 Tag129(T133).
- Tag130 Contact457(ORef436,W447)→W458→OR21.in1.
- **ON Contact460(ORef461/RID52,W463)→W22→OR21.in2.** W23 OR21.out→Coil428, W449 ORef437/RID57 Forza.

0597의2H 상수는 S5Time V14112,10M은V9728이다. “타이머를 기다려야만 Forza가 참”이라는 설명은 ON 병렬 가지를 누락한다. 논리적으로 ON이 참인 호출에서는 ON AND (Tag130 OR ON)이 Forza를 허가하는 구조다. 이는 PLC의 현재 값·실행 확인이나 임의우회 권고가 아니다.

### 3.3 시간변환·DP02 5단계·ON 공통 덮어쓰기

1. 0217 LAD1882 index1/NID25, CRef23→CRef32 ENO연쇄 W28. 내부 CodeBlock22/31 RID299는0056 KF_KT,0057 RID300 인터페이스 KF:Int/SEC:Bool/KT:Word다. CRef23.KF←ORef25 Data.VALVE_P(W24), SEC←ORef27 Bool0(W26), KT→ORef30 Coeff.DP_01_PAUSA_SOGLIA_1(W29). CRef32.KF←ORef34 VALVE_W(W33), SEC←ORef49 Bool0(W35), KT→ORef52 DP_01_LAVORO_SOGLIA_1(W51). BF02에도 쓰이는 공통 계수 생성이다.
2. live_index doc460/block_summary kf_kt의 원문STL·설명은 SEC=false일 때 입력을0.1초단위로 취급해S5형식으로 변환한다고 적는다. 원본 호출은 Bool0까지 결속했다. 고정수치의 현재 값, 실제 CPU단위·HMI문구·오버플로·컴파일 결과는 별도 확인하며 “현재pause=몇초”를 만들지 않는다.
3. 0199 LAD1884 index3/NID2의 첫허가는 **OFF** Contact559(ORef461/RID1,W500)이다. W560→Gt388.pre, W501 Ev_filter_on ORef462/RID3, W502 Int50 ORef463/RID30. 따라서 OFF AND Ev_filter_on>50 아래에서DP02다섯 범위를 검사한다.

| DP02범위 | 비교Part / 주요Wire | Pause출처→Data.LAVA_PAUSA | Work출처→Data.LAVA_LAVORO |
|---|---|---|---|
| DP02<S1 | Lt395; W504/505/506 | RID34 S1→Move398→ORef467 W509 | RID36 S1→Move401→ORef469 W512, ENO W510 |
| S1<=DP02<S2 | Ge407→Lt410; W513~518 | RID39 S2→Move413→ORef475 W521 | RID36 S1→Move416→ORef477 W524, ENO W522 |
| S2<=DP02<S3 | Ge422→Lt425; W525~530 | RID43 S3→Move428→ORef483 W533 | RID36 S1→Move431→ORef485 W536, ENO W534 |
| S3<=DP02<S4 | Ge437→Lt440; W537~542 | RID47 S4→Move443→ORef491 W545 | RID36 S1→Move446→ORef493 W548, ENO W546 |
| DP02>=S4 | Ge452; W549~551 | RID50 S5→Move455→ORef497 W554 | RID36 S1→Move458→ORef499 W557, ENO W555 |

S1~S4는 여기서DP02_SOGLIA_1~4다. 모든 Work 출처가DP02_LAVORO_SOGLIA_1이며2~5로 바꾸지 않는다. 임계값 정렬·현재 값이 검증되지 않아 범위의 실제배타성과최종Move결과를 가정하지 않는다.

4. 0198 LAD1883 index2/NID1에도 OFF Contact377→Lt206(Ev_filter_on<51,W319/320) 아래에서DP01시간을 같은LAVA_PAUSA/LAVORO에 쓴다. 첫Move216.out1 W327→ORef285, 다음Move219.out1 W330→ORef287이고 나머지단계도 같은목적지다. BF01의수치를복제한것이아니라 공통 Word다중 Writer존재를직접 확인했다.
5. **0201 LAD1887 index6/NID4는 ON만으로 다시쓴다.** Contact500 ON(ORef475,W486). W501→Move457.en와Move462.en. W487 ORef476/RID10 DP_01_PAUSA_SOGLIA_1→Move457.in, W488→ORef477/RID11 LAVA_PAUSA. W489 ORef478/RID13 DP_01_LAVORO_SOGLIA_1→Move462.in, W490→ORef479/RID14 LAVA_LAVORO. 두Move는허가OR보다앞에서별도 분기다.
6. 0201의허가OR25: BF01Contact22(ORef23/W21)→W24 in1, BF02Contact507(ORef508/W510)→W26 in2. W27 OR.out→NOT Tag131 Contact502(ORef481/W492)→W503 SdCoil468.in. value W491=Data.LAVA_PAUSA ORef480, operand W494=Tag132 ORef482. 별도ON상위에서Tag132Contact504(ORef484/W496)→W505 SdCoil473.in, value W495=Data.LAVA_LAVORO ORef483, operand W498=Tag131 ORef485.

두필터가공통 T1/T2와Word시간을사용한다. 네트워크 색인1→2→3→4→5→6순서와그복수 쓰기를보존하며, 현재 CPU스캔·분기활성·현재 최종값을정적색인만으로증명하지않는다. OFF뒤를무조건dead code로표시하지않는다. startup doc401원문은 “set s on; clr s off”이고0047 RID1/2의Write는NID1 UID24/27이다. OFF를Reset하는문장으로임의 수정하거나현재OFF=FALSE를단정하지 않는다.

### 3.4 세정 대상 범위·순번의 복수 쓰기

- 0202 LAD1888 index7/NID6: OFF Contact599 ORef569/W582 뒤 W600이 Move547(0→LAVA,W583/584), SC10 raw Contact601→Move553(1,W585/602/587/588), SC11 raw Contact603→Move559(2,W589/604/591/592), SC10Contact605→SC11Contact607→Move566(3,W593/606/594/608/596/597)로 갈라진다. 네 목적지는0596 RID68 UID571/574/577/581, Data.LAVA DB1.DBW230이다. 이것은처리 응답이아닌raw 입력 기준·복수 쓰기다.
- 0203 LAD1889 index8/NID7: OFF Contact780(ORef717,W742) 뒤 W781이 LAVA=0/1/2/3 Eq672/684/696/708을허가한다. 0→START0/END0,1→11/50,2→51/90,3→11/90. BF02선택2의핀이Eq696 W761/762→W763 Move699, ORef732 Int51 W765→out1 ORef733 START W766, ENO W767→Move702, ORef734 Int90 W768→out1 ORef735 END W769다.
- **0204 LAD1890 index9/NID8의ON은별도쓰기다.** Contact714(ORef703,W708) out W715→Move695/700.en. Int11 ORef704 W709→Move695.out1 W710 ORef705 START; Int90 ORef706 W711→Move700.out1 W712 ORef707 END. 이11~90은BF02단독 40개순번범위가아니라공통80개교대순번범위다.
- 0218 LAD1899 index18/NID27: ON Contact21→Tag132Contact22(W67/46)→PBox23(W45), edge bit ORef31/RID89 M50.3 W48. PBox.out W49가Add24.en·Lt25.pre·Gt27.pre를함께허가한다. Add24: Int1 ORef32 W50 + Ev_filter_on ORef33 W51→ORef34 W52. 현재순번<START이면Lt25 W53/54→Move26 W55, START ORef37 W56→순번ORef38 W57. 현재순번>END이면Gt27 W58/59→Move28 W60, START ORef41 W61→순번ORef42 W62.

증가·아래범위복귀·위범위복귀는같은순번에쓰는세가지경로다. 조건검사시점과실제최종값은실제컴파일/스캔검토가필요하다. 밸브출력8네트워크는색인10~17,순번증가는18에있다. Edge발생·실제 출력 유지 시간·전환시점이현장시험된것처럼쓰지 않는다.

### 3.5 BF02 EV40개의 고유 출력 가지

0205~0212 LAD1891~1898의각출력식은원본상 ON→Tag132→Int(Ev_filter_on=해당 순번)→Abilita_lavaggio_BF02→일반Coil이다. 예: EV51은0205/NID10 Contact1060 ON(W997)→Contact1062 Tag132(W998)→W1063 Eq894.pre, W1005 Ev_filter_on ORef961, W1006 Int12 ORef962/RID94, W1007→Contact1066 허가ORef963/RID65(W1008), W1067→Coil898, W1010 ORef964/RID95 EV51(Q18.0).

부록C는40개각각의 상수·핀·선·주소를별도대조한표다. 스크립트의구조대조40건은PLC동작시험이아니다. 모든출력의공통Tag132와ON직렬,해당허가Local,RID상수값을확인했고단순 등차 공식으로40개를만들지 않았다. BF01출력과교대하는공통 순번이므로EV51을순번51로설명하지않는다. 개별EV알람40개를새로만들지 않는다.

### 3.6 호출·전달·외부 Writer 경계

| 원본 | 결속한 호출 | 미확정 |
|---|---|---|
| 0549 LAD1620 main index9/NID7 | ONContact350 W348/W351→CRef322.en; CodeBlock339/RID70=0688 Filter, 0694 RID71인터페이스. 같은W351에Motors1 CRef319도있음 | 공유허가선은ENO직렬 실행순서를뜻하지않음. 현재 CPU호출·주기별도 |
| 0031 LAD1619 main index8/NID6 | ONContact282 W280/W283→Analog CRef261와Allarms3 CRef270 등; CodeBlock273/RID55,279/RID64=0688 | 환산·알람·Filter순서의고정색인과실제스캔분리 |
| 0030 LAD1613 main index2/NID19 | RecipesHandler CRef21.eno W32→HMI23.en, HMI.eno W33→HMIOutput25.en,25.eno W42→NOT Simulation Contact37→W43 HMIInputs28.en; Simulation ORef45/RID140 W44 | HMI표시·입력처리의실행시점/ENO결과미확인 |
| 0148 LAD403 startup | ON→DB3Word0해제(§5.2) | startup현재구성·보존값·재시작검증안함 |

현재 CPU와HMI외부쓰기·간접주소·강제값·입출력 모듈파라미터는미확보다. 원본 호출선이있다는것과현장동작확인은별개다.

### 3.7 주석 처리된 EV OR 집계와 실제 BF02_RUN 구분

sources/live_index.json _7ev doc1904의 SCL Code는 `(*`로 시작하고 `*)`로 끝나는 전체 주석이다. 그 안에 EV51~90을 OR한 뒤 BF02_RUN에true/false를 쓰는 문장이 있다. 이를 현재 실행되는 출력 집계로 세지 않았다. 이번에 핀까지 결속한 실제 BF02_RUN 쓰기는0219/NID29 Coil78, 즉 세정 허가 연쇄다. 주석 내용, LAD 허가 결과, 실제 개별EV 출력/공압작동은 세 층으로 구분한다. 현행 CPU에 다른 구현이 있는지는 별도 비교가 필요하다.

## 4. 전기 전달·도면 페이지·개정

Electrical_Rev2.pdf의11페이지, 시공PDF6페이지, P&ID1페이지를 실제 렌더로 확인했다. 전기 FG와 PDF페이지는180A/180B 같은 삽입 시트 때문에 같지 않다. 아래는 **인용한 각 시트의 개정란을 개별 시각 확인한 목록**이다.

### 4.1 인용 페이지와 footer

| 문서 | FG/도번 또는 D-page | 실제 PDF페이지 | 제목/검토 범위 | footer 판독 |
|---|---|---:|---|---|
| 전기 | FG169 | 170 | DIFFERENTIAL PRESSURE CONTROL, DP02경계 | DATA27.05.2024; 별도개정기재공란 |
| 전기 | FG172 | 173 | ANALOG INPUT MODULE, PEW400끝점 | DATA27.05.2024; 별도개정기재공란 |
| 전기 | FG181 | 184 | SUPPLY110Vac JB2 PLC MODULE | DATA27.05.2024; 별도개정기재공란 |
| 전기 | FG182 | 185 | CONFIGURATION PLC JB2 BOX | DATA27.05.2024; 별도개정기재공란 |
| 전기 | FG183 | 186 | CLEAN BAGS VALVES COMMAND, EV51~53 | DATA27.05.2024; 별도개정기재공란 |
| 전기 | FG196 | 199 | CLEAN BAGS VALVES COMMAND, EV90 | DATA27.05.2024; 별도개정기재공란 |
| 전기 | FG197 | 200 | DIGITAL OUTPUT MODULE, Q18 | DATA27.05.2024; 별도개정기재공란 |
| 전기 | FG198 | 201 | DIGITAL OUTPUT MODULE, Q19 | DATA27.05.2024; 별도개정기재공란 |
| 전기 | FG199 | 202 | DIGITAL OUTPUT MODULE, Q20 | DATA27.05.2024; 별도개정기재공란 |
| 전기 | FG200 | 203 | DIGITAL OUTPUT MODULE, Q21 | DATA27.05.2024; 별도개정기재공란 |
| 전기 | FG203 | 206 | DIGITAL INPUT/OUTPUT MODULE, Q22 | DATA27.05.2024; 별도개정기재공란 |
| 시공 | CANDC-CONS-E020-037, D-page20 | 37 | DUST ZONE03/JB02 공급·통신 | Rev1,24.11.11,first draft design; CHECKED/APPROVED공란 |
| 시공 | CANDC-CONS-E021-038, D-page21 | 38 | DUST ZONE04/JB02TB1→EV51~60 | Rev1,24.11.11,first draft design; CHECKED/APPROVED공란 |
| 시공 | CANDC-CONS-E024-041, D-page24 | 41 | DUST ZONE07/JB02TB4→EV81~90 | Rev1,24.11.11,first draft design; CHECKED/APPROVED공란 |
| 시공 | CANDC-CONS-C010-060, D-page10 | 60 | CABLE SCHEDULE9, JB02 공급·분기·통신 | Rev1,24.11.11,first draft design; CHECKED/APPROVED공란 |
| 시공 | CANDC-CONS-C011-061, D-page11 | 61 | CABLE SCHEDULE10, EV51~70/DP02 | Rev1,24.11.11,first draft design; CHECKED/APPROVED공란 |
| 시공 | CANDC-CONS-C012-062, D-page12 | 62 | CABLE SCHEDULE11, EV71~90 | Rev1,24.11.11,first draft design; CHECKED/APPROVED공란 |
| P&ID | 1684n002 ApexI | 1 | BF02·SC11·VR05·DP02·5섹터 | 원작성06/04/2011,개정I15/01/2013 |

공란은 이 페이지에서 추가개정을 판독하지 못했다는 의미다. 파일 전체에개정이없다는 뜻이 아니다. 원본 PDF의 다른페이지는 해시검사/문자검색만 했고 의미 검토페이지로 세지 않는다. 특히 EV54~89 부하 접점/단자를 전수 시각 검토했다는 주장은 하지 않는다.

### 4.2 BF02 본체 세정 전원·제어 끝점

| 경로 | 원본·실제 양 끝점 | 해석·미확정 |
|---|---|---|
| JB2 DC공급 | FG181/PDF184: 110Vac9.13(9/7)→X4:1, 0Vac9.9(9/7)→X4:2. 181QF1 6A 주접점1–2/3–4→181.1/181.2→181GD1 5A AC/DC. DC+181.3→181QF2 4A→+24Vdc181.5; DC−→−0Vdc181.4 | 정격은 도면 값. 현재 전압·보호설정·퓨즈선정 권고 아님 |
| 세정밸브AC공급 | FG181:110Vac9.12(9/6)→X4:3→181QF4 2A접점1–2→110Vac181.8(183/0), 0Vac9.9→183/0 | PLC릴레이코일DC공급과 EV부하AC공급을 구분 |
| JB2 인터페이스 | FG182/PDF185:182IM155 6ES7155-5AA01-0AB0, X80 1L+/1M/2L+/2M 표시; +24V181.5→2L+, −0V181.4→2M(1L+/1M은이도면에서외부연결선없음); X1P1/X1P2 PROFINET IO | 현행 네트워크명/IP·실제링크상태 미확인 |
| JB2 모듈 | FG182:182A1 POS2 DQ32×24VDC/0.5A HF 6ES7522-1BL01-0AB0;182A2 POS3 DI/DQ16×24VDC 6ES7523-1BL01-0AA0 | 도면 형번. 현재 설치·펌웨어·채널파라미터 미확인 |
| EV51 출력DC | FG197/PDF200 CPU515 MOD2 A18.0 단자1→183/3. FG183/PDF186 A18.0(197/1)→183KA1 A1, A2→−0V181.4 | XMLQ18.0과 도면A18.0 대응. 출력전압·릴레이실제 작동 별도 |
| EV51 부하AC | FG183:110Vac181.8→183KA1 **5–9**→183.1→X4:4 2A F5×20→183.2→EV51 A1; EV51 A2→X4:5→0Vac9.9 | 하단접점표1/5/9와 실제그린부하 접점5/9 구분. 밸브작동·공압완료피드백 아님 |
| EV52/53 부하 | 동일FG183:183KA2 5–9→X4:6/7→EV52 A1/A2, 명령A18.1.183KA3 5–9→X4:8/9→EV53 A1/A2, 명령A18.2 | 전용퓨즈는각2A F5×20. 다른EV에그대로복사하지 않음 |
| EV90 출력DC | FG203/PDF206 CPU515 MOD3 A22.7 단자28→196/3. FG196/PDF199 A22.7(203/1)→196KA1 A1; A2→−0V181.4 | EV90의Q22.7고유 끝점 |
| EV90 부하AC | FG196:110Vac181.8→196KA1 **5–9**→196.1→X4:82 2A F5×20→196.2→EV90 A1; A2→X4:83→0Vac9.9 | EV90개별 회로를원본 대조. 밸브막힘/백건전성까지확정불가 |

181QF3/181TM1/181EV1은 동일상자의 냉각회로다. 이를 세정밸브 공급차단기나 별도 BF02 공정밸브로 바꾸지 않는다. 아래 모듈핀은 각 원본렌더에서대조했다.

| 전기 FG/PDF | 출력 영역·EV | 모듈·신호단자 | 공급핀·퓨즈 |
|---|---|---|---|
| 197/200 | A18.0~7,EV51~58 | CPU515 MOD2,1~8 | +24V181.5→X23:5000 4A F5×20→197.1→9; −0V181.4→10 |
| 198/201 | A19.0~7,EV59~66 | CPU515 MOD2,11~18 | X23:5001 4A F5×20→198.1→19; −0V→20 |
| 199/202 | A20.0~7,EV67~74 | CPU515 MOD2,21~28 | X23:5002 4A F5×20→199.1→29; −0V→30 |
| 200/203 | A21.0~7,EV75~82 | CPU515 MOD2,31~38 | X23:5003 4A F5×20→200.1→39; −0V→40 |
| 203/206 | A22.0~7,EV83~90 | CPU515 MOD3,21~28 | X23:5020 4A IST.5×20→203.1→29(2L+); −0V→30(2M) |

PLC 출력40개와5개출력 뱅크 끝점은 대조했다. 개별 부하중 실제 렌더로5–9·X4 양끝까지확인한 것은 EV51/52/53/90 네회로다. EV54~89 부하 접점/단자는 하위 밸브 원본 검토의남은 범위로보존한다. 계전기·솔레노이드의 현재제조사/명판/보호값/토크·교체품은미확보이며 ABB 등으로추정하지 않는다.

### 4.3 DP02 연결과 JB1/JB2 소유 경계

- FG169/PDF170 오른쪽제목은 DIFFERENTIAL PRESSURE SWITCH BAGS FILTER BF-02다. DP02전원은110Vac152.8→X3:95(2A F5×20)→169.2, 0Vac9.9→X3:96. 센서상자내부표시는110Vac, OUTPUT4–20mA,0/50mbar다. 출력+→X3:97→+PEW400, 출력−→X3:98→−PEW400; Shield X3:99→169SCH2→172/5.
- FG172/PDF173에서 +PEW400→CPU515 MOD2 단자34 I7+, −PEW400→36 U7−/I7−, Shield169SCH2가그려진다. 이쪽 MOD2는 아날로그입력시트 문맥이고 JB2의182A1/MOD2 디지털출력과같은기기라고합치지 않는다.
- 0522 LAD1774 analog input conversion index44/NID41: ONContact1575(ORef1562,RID1,W1569)→CRef1556.en(W1576). CodeBlock1568/RID5는0672 Signal linearization,0680인터페이스. PR_BR02 ORef1564/RID300→Analog_input W1571, Coeff.COEFF_DP02 ORef1565/RID301→Coeff W1572, Coeff.ZERO_DP02 ORef1566/RID302→Zero W1573, OutValue W1574→ORef1567/RID303 Data.DP_02, Out_of_range W24→ORef23/RID430 BF02_OFR.
- 0678 PR_BR02는 Input/AO3200,16bit,SAM=Peripherie, 즉 %IW400:P. 0676 COEFF_DP02 BO976=DB4.DBW122, ZERO_DP02 BO960=DB4.DBW120, DP02=DB1.DBW242, BF02_OFR BO197=DB3.DBX24.5;0674 Data/Coeff/Allarm TOD1/4/3대조. 함수의 내부전체 환산·부호·현재 계수·단위는 DP02 독립 검토범위로남긴다. 0/50mbar 센서도면과 Int2800을곧바로같은단위로만들지 않는다.
- 시공p61의11_3/11_4는 BF01 JB01→BF02 JB01TB6의DP02전원/AI,11_27/11_28은 BF02 JB01TB6→DP02의전원/출력이다. DP02가BF02에있다는이유로모든전원·통신·AI를JB02소유로옮기지 않는다.

### 4.4 시공 케이블과 확인된 상충

시공도는기존원본자료를 읽은것이며 운영기록이나현장사진을복제한것이아니다. 도면당 승인란이공란인first draft여서준공·실측·현재 배선으로확정하지 않는다.

| 항목 | 시공원본의확인내용 | 남은경계 |
|---|---|---|
| 전원/통신번호 상충 | p37:10_16=DUS+BF02-JB02A(CVV4mm²4core),10_17=…JB02B(Profinet),10_18=DUS+BF01-JB01B(Profinet). p60:같은JB02A전원은10_17,JB02B통신10_18,JB02→JB01통신10_24 | 번호를임의 통일하지않음. 승인케이블 표·양끝 마킹확인필요 |
| JB02공급경로 | p60 10_17 CR→BF02/JB02 POWER(110V/110V/0V),AC CVV4G4.0,Route100→200→220→221→222RB→E100,Adjustment2,LEN98 | p37번호충돌우선해결. LEN98실측미터확정아님 |
| 통신경로 | p60 10_18 CR→BF02/JB02,Profinet,동일Route말단E200,LEN98.10_24 BF02/JB02→BF01/JB01,LEN11 | 실제네트워크구성·도통·주소미확인 |
| 분기함 | p60 10_19~10_22 JB02→JB02TB1~4,AC CVV25G1.0,SPARE4,EV51~60/61~70/71~80/81~90 | 전기도면5×8섹터와시공4×10분기함분류다름 |
| EV51현장케이블 | p38/61 11_5=DUS+BF02-EV51A,JB02TB1→EV51,AC CVV3G1.0,SPARE0,Route RAD1/E200→E400,Adjustment6,LEN6. p38분기4 Flexible16 | X4:4/5와JB02TB1현장단자 번호·코어의직접일대일표는미확보 |
| EV90현장케이블 | p41/62 12_20=DUS+BF02-EV90A,JB02TB4→EV90,AC CVV3G1.0,SPARE0,Route RAD1/E4200→E5200,Adjustment2,LEN2. p41분기52 Flexible16 | X4:82/83와JB02TB4의현재 단자대응미확보 |
| DP02교차패널 | p61 11_3=…BF01-JB01TB6A,11_4=…BF01-JB01TB6B는BF01/JB01→BF02/JB01TB6;11_27/28=…BF02-DP02A/B | BF02설치장소와BF01측공급·계측소유구분 |

Flexible16/22/28/36은관로표시이며전선굵기나단자 번호가아니다. p61/p62의다른EV케이블행은분기구조를검토했지만개별 40개전기 부하 핀·현재 길이를완료했다고세지 않는다.

## 5. 알람·복구·공통 경보 영향

### 5.1 공유 MAX_DP_FILTER의 실제 Set/Reset

0540 LAD1992, allarms3 index14/NID14. 이경보는BF01/02 차압공유이며 BF02전용 고장타이머가아니다. 0684 RID119 BO77/BAD10→0682 Allarm/TOD3=DB3.DBX9.5, 0686 RID118 Timer/AO114=Tag112 %T114, 0683 RID96 S5T#3M을대조했다.

- ONContact1204(ORef1153/W1173) 뒤 W1205가 네비교와Reset 분기를허가한다.
- Gt1121:DP01 ORef1154 W1174 > Int2800 ORef1155 W1175; W1176→OR1120.in1.
- Gt1124:DP02 ORef1156 W1177 > Int2800 ORef1157 W1178; W1179→OR.in2.
- Lt1127:DP01 ORef1158 W1180 < Int−100 ORef1159 W1181; W1182→OR.in3.
- Lt1130:DP02 ORef1160 W1183 < Int−100 ORef1161 W1184; W1185→OR.in4.
- W1186 OR.out가 SdCoil1136.in과Tag112 Contact1206.in을함께허가한다. value ORef1162 W1187=S5T#3M, timer ORef1163 W1188=T114. Contact1206 operand ORef1164 W1189, out W1207→SCoil1141, operand ORef1165/RID119 W1191.
- Reset: W1205→Contact1208 RESET_ALLARM(ORef1166/W1193)→W1209→Contact1210 현재MAX_DP_FILTER(ORef1167/W1194)→W1211→Lt1146(DP01<2500,W1195/1196)→W1197→Lt1149(DP02<2500,W1198/1199)→W1200 RCoil1152, operand ORef1172/RID119 W1202.

Set 조건은 ON AND (DP01>2800 OR DP02>2800 OR DP01<−100 OR DP02<−100)가T114의3분조건과함께충족하는구조다. Reset은 ON AND Reset요청 AND 기존경보 AND DP01<2500 AND DP02<2500이다. **Reset 분기에는하한 정상 조건이없다.** 따라서경보가해제됐다고 음수이상값·센서 단선·실제차압이정상이라는 증거가되지않는다. 2800/−100/2500은원본Int상수이며현재안전설정·실측mbar로추천하지않는다. TIA타이머 상태/실제지속시간/Set·Reset동시충족시최종값은미확인이다.

### 5.2 비트 Reset 이외의 startup Word0

0148 LAD403의ONContact329.out W330→Move267.en; W315=ORef293/RID54 INT#0→Move267.in, W316 Move267.out1→ORef294/RID32. 0048 RID54 Int0 NID3 UID293,0563 RID32 Word/AO64/BAD23 NID3 UID294 Write,0562 RID23 Allarm/TOD3이므로 **DB3.DBW8=0**이다. 바이트8/9를덮으므로MAX_DP_FILTER(DB3.DBX9.5)가포함된다. 이름검색만으로는놓칠수있는별도 Writer다.

같은startup검토범위는DB3.DBW0/2/4/6/8/10/12/14/16이다. BF02_OFR(DB3.DBX24.5)는해당범위 밖이다. 전원재시작을고장복구방법으로권고하지 않으며 현재 startup실행·retentivity·온라인값을시험하지않았다.

### 5.3 BF02_OFR 및 공통 새경보 감시 범위

BF02_OFR은0522의Signal linearization.Out_of_range가직접쓰는DB3.DBX24.5다. 이번 BF02 문서에서는인터페이스·주소·HMI Allarmi_235까지만결속했다. 함수내부범위판정·유지형여부·자동재해제·센서보호전략·모든 정지 영향은DP02독립 검토범위로남긴다. MAX_DP_FILTER와같은3분유지경보로취급하지않는다.

공통 allarm manager의두 네트워크에서 주소범위를직접 검토했다.

- 0151 LAD927/NID1: RESET_ALLARM Contact213/ RUN_HORN215/ STOP_HORN217가OR121에들어가고W212가9개Move를허가한다. Word8경로는W202 ORef181/RID21→Move147.in, W203 out1→ORef182/RID22 WorkData.W4다.0565 RID21 Word/AO64/BAD7→0564 Allarm/TOD3, RID22 WorkData.BO64/BAD9→0564 WorkData/TOD6이므로DB3.DBW8→DB6.DBW8이다. 이는Allarm을0으로쓰는경로가아니라관찰 스냅샷읽기다.
- 0152 LAD928/NID2: Ne203.in1 W252 ORef228/RID21 DB3.DBW8, in2 W253 ORef229/RID22 WorkData.W4. W254→OR190.in5. 전체9입력OR의범위는DB3.DBW0/2/4/6/8/10/12/14/16이다. W267 OR.out→NOT STOP_HORN Contact271(ORef238/W268), W272→Coil219, W270 ORef239/RID35 NEW_ALLARM(DB2.DBX6.3).

MAX_DP_FILTER는Word8변화 감시 범위에포함된다. BF02_OFR의X24.5는이두 네트워크의Word0~16감시 범위 밖이다. **이것은확인한공통 감시의범위 경계이며“BF02_OFR 경보가없다” 또는“전체 시스템에서사이렌이절대울리지않는다”는판정이아니다.** HMI직접표시설정은별도로존재한다. 이후실제 호른출력·별도HMI알람엔진·추가소비자의전체 경로는미확보다.

### 5.4 복구 판정 원칙

경보비트해제, 새경보확인/정음, BF02_RUN허가, 개별EV출력, 실제 세정압력, 차압회복, SC11/VR05분진 배출은다른관찰점이다. 현재 값·원인 제거·재요청·운전재개·지속관찰증거 없이복구 완료로표시하지않는다. 공통Reset을눌렀다는사실만으로필터백·밸브·센서가정상이라고쓰지 않는다.

## 6. 증상별 관찰·수리 초안

이표는승인된 안전 절차아래전문 담당자가수집할관찰 항목이다. 실제 조치실행기록이아니며무전원·잔류압력격리·접근 허가와현장 안전 절차를대체하지않는다. PLC강제출력·보호값변경·인터록우회·무단재기동은제시하지않는다.

| 증상 | 관찰 위치·비교 근거 | 원인 배제·필요 조치 근거 | 복구 증거 |
|---|---|---|---|
| BF02_RUN이켜지지 않음 | 0219 ON,DB13.X5.1/X5.6,DP02/DB4.W138,Forza와M180.4를같은시각기록 | raw I5.1/I5.6와처리값을분리;SC11/VR05담당기록과입력전송 조건비교 | 두응답·허가·각EV전환·실제공압상태를별도 확인 |
| RUN은켜지나 펄스가없음 | 허가Coil과주석OR집계구분;DB1.W170순번,T1/T2,W236/238,해당Q를동시기록 | 출력 명령 없음 / 모듈공급 없음 / 릴레이미작동/AC부하없음 / 공압문제를단계별배제 | 명령→릴레이→EV 동작·압력·차압 추세의승인된 관찰 |
| EV51이순번51에서안 켜짐 | 부록C순번12/Q18.0,0205Eq894및FG183/197비교 | 밸브번호=순번 오인을배제.순번·배선·섹터표식일치확인 | 올바른채널·순번의시간기록;강제출력시험대체아님 |
| 중간이후일부밸브만안됨 | Q18~22의뱅크,모듈2/3,퓨즈5000~5003/5020,시공4×10분기함과5×8섹터비교 | 공통 뱅크공급인지개별 부하인지분리.미검토EV54~89는각FG원본/현장단자자료 추가 | 영향채널전후 관찰과타채널보존증거 |
| pause/work설정과체감주기다름 | VALVE_P/W→KF_KT BoolSEC0→DP01공통 계수→Word236/238,OFF분기·ON덮어쓰기비교 | DP02개별계수만읽거나원본 값을초단위로단순 표기한오인을배제 | 실제 타임스탬프·호출주기·현재 최종값확보;값임의조정없음 |
| 차압이높거나음수·OFR표시 | DP02장치·전원·4–20mA·PEW400·계수/Zero·DB1.W242·X24.5·X9.5 | 도면0/50mbar와Int값단위연결자료 확보.센서·배관·집진 상태를구분 | 원인 제거·정상계측범위·추세·경보지속관찰 |
| Reset후경보가다시발생 | 0540하한 검사없음,두DP·3분타이머·Reset·startupWord8구분 | Reset성공을원인 제거로보지않음.이상음수·반복Set 조건검토 | 두DP상태·현재 경보·재발시간을기록하고지속회복확인 |
| 케이블번호가표마다다름 | p37대p60 10_16/17/18/24상충,기호명·FROM/TO·실물마킹비교 | 번호만믿고작업대상을선택하지않음.승인표·양끝 검증필요 | 수정승인 자료와두끝점식별사진/검사기록.공개저장소복사없음 |

관찰 기록필수 값:관찰자·시각/시간대·위치·값/단위·수집장치·현재프로젝트/CPU근거·비교원본판본·배제결과·승인조치·복구후증거. 0/빈칸/미측정을구분한다. 실제 사용자운영기록은작성·변경하지않았다.

## 7. 네 기능·완료 기준·인계

| 기능 | 적용·구현 상태 | 이번 실제 검증 |
|---|---|---|
| 도면·래더나란히보기 | BF02허가/EV출력/양끝점대조에적용가능;BF02전용 통합프로파일검증 대기 | 원본 직접정적 대조만.배포UI링크/강조/왕복미수행 |
| 백업·선택복원 | 향후BF02기록 지원구현시적용.독립catalog키·하위 키 보존필요 | 저장·재읽기·재열기/충돌/Quota/동시성미수행 |
| 전후기록비교 | 허가/순번/DP/공급/실물세정관찰의전후비교에적용가능 | 실제 사용자기록없음.비교도구검증 미수행 |
| 보고서/PDF | 본체·하위소유·신호/측정·자료상충분리필요 | 이MD조사만작성.정비보고서/PDF생성·UI출력미수행 |

### 필요한 자료와 판정 기준

1. 현행BF02명판·필터백/펄스밸브명세·공압도·승인P&ID/준공전기·케이블 표. 당시 설계범위/압력/온도를현재 정상설정으로대체하지않는다.
2. p37/p60케이블번호 상충의승인 정정자료와양끝 마킹. 일치하지 않으면배선동일성미확정유지.
3. EV54~89의개별 릴레이부하 접점·단자 끝점·현행코어 대응. 이번PLC40가지검토와개별 밸브완료를분리한다.
4. DP02독립환산·단위·계수/Zero·진단범위·현행 센서/모듈설정. BF02_OFR전체 소비·HMI알람엔진·공통 감시 범위차이는별도 검토.
5. 현재TIA프로젝트/CPU블록·호출순서·HMI이벤트/권한·통신Writer·온라인관찰자료. 독립된안전 승인없이는수집/조작하지않는다.
6. BF02전용7영역프로파일·도구 지원의독립 검토후통합. PC1280/모바일390·글자크기·검색/링크·백업보존·PDF·패키지/배포는해당승인통합작업에서검증한다.

| 구분 | 상태 | 근거·미확정 |
|---|---|---|
| documentation | draft_complete_with_gaps | BF02핵심세정·소유·알람·회로·충돌·누락작성;문서통합완료아님 |
| static_review | source_crosscheck_complete_independent_review_pending | 원본핀·선/선언·40출력가지·18PDF페이지자체대조;독립 검토대기 |
| ui_records | not_run | 기능통합/사용자기록변경없음 |
| publication | not_published | 코드·버전·배포변경없음 |
| tia_compile | not_performed | TIA/컴파일미수행 |
| live_cpu | not_performed | CPU다운로드·현재 값·실행미수행 |
| field_recovery | not_performed | 현장 관찰·작업·복구미수행 |

다음 한 작업은BF02독립원본검토다. 우선검토점은①ON우회Forza와DP01명허가상대②OFF/ON공통 Word 다중 쓰기③40개고유EV순번/출력과주석RUN④공유경보Reset하한/Word0 범위⑤FG별개정란과p37/p60케이블충돌이다. 승인대장/현장자료가 없으면빈칸을유지한다. 새현장자료 없이동일보류를반복조사하거나로컬2차통합을시작하지않는다.

## 부록 A. 핵심 경로 의미 검토 위치

아래28개 FlgNet의 문서에 명시한 경로를 검토했다. 전용 EV40개 가지를 포함하며, 28은 전체 프로그램 완전해석 수가 아니다. 0198은 공통 Word 대상,0151/0152는 공유 경보 Word 범위의 선택 경로다.

| XML | LAD | 블록 / 색인 | NID | 검토 범위 |
|---|---:|---|---:|---|
| 0030 | 1613 | main / 2 | 19 | 본문에 명시한 전달·호출 경로 |
| 0031 | 1619 | main / 8 | 6 | analog conversion and allarms |
| 0148 | 403 | startup only / 3 | 색인미결속(본문선언보완) | reset all flag allarms |
| 0151 | 927 | allarm manager / 1 | 1 | 본문에 명시한 전달·호출 경로 |
| 0152 | 928 | allarm manager / 2 | 2 | com_w3 bit11 (new_allarm) |
| 0198 | 1883 | filter / 2 | 1 | time work/pause by dp01 |
| 0199 | 1884 | filter / 3 | 2 | time work/pause by dp02 |
| 0200 | 1885 | filter / 4 | 3 | force wash minimum |
| 0201 | 1887 | filter / 6 | 4 | work pause times for filter valves |
| 0202 | 1888 | filter / 7 | 6 | filter work |
| 0203 | 1889 | filter / 8 | 7 | 본문에 명시한 전달·호출 경로 |
| 0204 | 1890 | filter / 9 | 8 | enable all the 80 valves when the filters are parallels |
| 0205 | 1891 | filter / 10 | 10 | a0.0 filter 1 valve bf01first sector |
| 0206 | 1892 | filter / 11 | 11 | wash filter |
| 0207 | 1893 | filter / 12 | 12 | wash filter |
| 0208 | 1894 | filter / 13 | 13 | wash filter |
| 0209 | 1895 | filter / 14 | 14 | wash filter |
| 0210 | 1896 | filter / 15 | 15 | wash filter |
| 0211 | 1897 | filter / 16 | 16 | wash filter |
| 0212 | 1898 | filter / 17 | 17 | wash filter |
| 0217 | 1882 | filter / 1 | 25 | 본문에 명시한 전달·호출 경로 |
| 0218 | 1899 | filter / 18 | 27 | next valve |
| 0219 | 1886 | filter / 5 | 29 | enabling sleeve washing |
| 0397 | 1070 | hmi inputs / 1 | 1 | 본문에 명시한 전달·호출 경로 |
| 0401 | 356 | hmi output / 1 | 1 | 본문에 명시한 전달·호출 경로 |
| 0522 | 1774 | analog input conversion / 44 | 41 | dp-02 |
| 0540 | 1992 | allarms 3 / 14 | 14 | max filter depressure |
| 0549 | 1620 | main / 9 | 7 | motors valve and burner |

추가 원문: live_index _7ev doc401(startup STL),460(KF_KT STL/설명),1904(전체 주석 SCL). 원문 문자와 호출·선언을 구분해 검토했다. 이3개는 FlgNet28개에 합산하지 않았다.


## 부록 B. 원본 SHA-256·Git blob·보존 검사

고정 커밋의 Git blob과 현재 읽기 원본의 SHA-256을 대조한 고유 파일은 94개이며 모두 일치했다. 중지5자산은 freeze 명세와도 일치했다. Git blob ID는 SHA-1 객체 ID, SHA-256은 파일 바이트 해시다. 두 해시 형식을 혼용하지 않는다. 94개는 바이트 동일성 수이며 의미 검토28개 경로/18페이지 수와 별개다. 대형 PLC 원본은 보존 해시 확인이며 전체 바이너리 의미 검토가 아니다.

원본의 검증 가능한 기준 URL: https://github.com/esp6662266/gme-plc-manual/tree/abcf31c5030bc7ef8749ed8e869a857f2387a28a . 아래경로는이기준커밋의저장소루트상대경로다.

| 원본 경로 | SHA-256 | Git blob ID |
|---|---|---|
| .agents/skills/gme-equipment-rollout/SKILL.md | fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b | 9aa820ea6ca15b4e136c9772423b78ed4df6a3d4 |
| .agents/skills/gme-equipment-rollout/references/source-map.md | 40612c5efb8f94608840c7bc0e9095ea840df54920861c388ae48ea34c7998dc | 49e50a7a8e56a16e2ec7f3607a03fd90adb8f1d3 |
| .agents/skills/gme-equipment-rollout/scripts/preflight.py | 395067d6da20af3e1d82a43b7936907a87a44d8d2e11e4ebc61b1fc441e2adb6 | 170679427250c36c3a68cf6c5c2291ffe0341b10 |
| AGENTS.md | 0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2 | 073164bc6efd5791032d62c71b03b4dab48cb6f8 |
| EXPANSION-WORK.md | ec624de9fd2fcfac861a67fd5e828b25ef46db50bfd7a37ff16e2cb54cd0f7e2 | 4c42d88ecc2d48269eb23e13a20ebf3721a092a1 |
| PUBLICATION_STATUS.md | efe4857aec598d90470322cf3962eb3fe1f64947630e1fdf71d1c90134de8740 | d76401cf291fc0be681acc51fa898ad3ce46ff78 |
| VERSION.json | 5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7 | fffb51663b7705aec91cb119ca80ee943a4ce758 |
| WORKSPACE-HANDOFF.md | 215096d997782e78e901dfae36c782937e49611fbeb677a0d3fa50cbecf8d074 | dd0b8989d2376c4415bba9bd826fe6754c6b1a12 |
| all-in-one/ACTIVE-WORK.md | eff3bbc08ecff41da3beff77f3fec48e7d148708192bcaaab00f34b6a721afc2 | 6eb947c629b5ddf9c759ef87649451303938864b |
| all-in-one/assets/program-model-data.js | 52f8199371e3399b7c0d44ab5469f0472aced79d56bbef2887f7625f5d2aff0f | 38f34b0caa380a16ccad6f6f1e234a2fdf23f327 |
| all-in-one/assets/simulator-workspace.js | 3a6dfc618ff7e7b238f2671dc85d65704f33093a18eac879d86081d92c31e8bc | 97c2c831c77a9699fff0e0960b3bc1b7d93d45b3 |
| all-in-one/assets/virtual-plc.js | 5f1876052dc0067b1f010af0dfc941946e37003167481731293615d9c1c36dbc | 0bd9eceb54365a91214a37c5601b5067c39a3f75 |
| all-in-one/registers/all-in-one-data.json | 63a46b36b6454bf1246d093300dbee11f2fcc287ad94991405369bf9f939a8fe | 15d62ac2a99c1c0eeb7579e03163f9c0319b50a4 |
| all-in-one/registers/equipment.json | 7870325dff32bbca90fa34507b301c4aad3347d669fddcd03b910343663996fa | acc42633033398216469064932c4b76987371606 |
| all-in-one/registers/program-model.json | 6203479c086b15bada12ac9d7e37db9280234ec26f1ea6091d7211dc09a577c5 | 9860b10f008d3a5ae714be50d77b703dfec32f3a |
| all-in-one/registers/requirements-audit.json | a10b773ff96e9b1c7a27cf409644c68d3eb59aedc5bcb5ca00199d602e63facb | 69e45bb8fe1abbcd2ba4eeb65e2f4445a367e238 |
| all-in-one/registers/simulator-freeze.json | bb93c1994effc5609939ba566b7802ce7ed55154a7310f02379b308ac2c8c835 | 808ffac14dbd1b4a7d797fa6cd0d647635d90b47 |
| all-in-one/registers/virtual-plc-test-results.json | a6b389f797f9a8b5ffe6928b8420f55c4cc459a327b0b48d716079d2eca6dd64 | 757dd50e45184568facb8ff62900b39d3ce848d1 |
| all-in-one/sources/Electrical_Can_Decoating_20241118.pdf | 3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd | 0ee6b6f8361c5790864dbba4bbd9d55e8e7c08f8 |
| all-in-one/sources/Electrical_Rev2.pdf | 5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6 | f610fd7c7ce14ae951b00cff57b969259bfb389d |
| all-in-one/sources/GME_20250506.zap18 | 00c79b6d986e68298f65b172c1807115bc5d9e450a74fcc989d0796d8d8a4ea8 | 211c4f604627a32f82a1124c2a9872c2fcf00865 |
| all-in-one/sources/PEData.plf | 647de7ea123daced41c27bec8f81aeb93c712cac714d4754d7da5c528abb016a | 65605ff8910f920109da731604aa5dc8d83fc956 |
| all-in-one/sources/PID_1684n002I.pdf | 2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b | 8c83a59fefd5b8b651ec3537ea4236a073f5e109 |
| all-in-one/sources/block_summary.json | 68253f9366908244a27ed461c66d465da7ec1723571f27deaa9a6f81a542de63 | 15b570a011645023dbfca2d5332a9e0ae3b0a7b6 |
| all-in-one/sources/can-decoating-page-text.json | d3b4c14945dd00f79c58ebab0cb8991c422dd1670e95e24d10779bd9e9d99bba | 2bebec2c719fa57ed6c9f8d4e541e8848dc0d732 |
| all-in-one/sources/decoded-original/0030-FlgNet.xml | 9252c9da764993de1edb8b2e44c46d6e9f9d4b6118e751a0dbeaa9ffd8ea721b | e74c70b751acdcdbc7a8b3b0c98aa773c2107cab |
| all-in-one/sources/decoded-original/0031-FlgNet.xml | 76385eab8f8f72b9faa16f7cf8905f395591b18c0a9ee9e6d7dd085a38c45c65 | 653d27572de6beedcf3eb6c95702bb119a8b567f |
| all-in-one/sources/decoded-original/0047-IdentXmlPart.xml | 2e53bb895dd1ad2a74efaeb1ef16dfd61e62b1b2d7aa34cec8612f1b9cb0928e | 3dc282f149a21fdf76d5521ef1c833be63b578b4 |
| all-in-one/sources/decoded-original/0048-IdentXmlPart.xml | d8e8687de7271bd294c2b62b33d789700af9d5014d82b130141988c4d479253d | 64fc5a7f1ad33f3b901b00f0d22d23578ffabff8 |
| all-in-one/sources/decoded-original/0056-IdentXmlPart.xml | c5ec45cd232c36d80f80487ec0dd284a876e326ba2286fc722ecc861a400232a | 1364306d64caf1f1f094c98dc163edf69cdc1afc |
| all-in-one/sources/decoded-original/0057-IdentXmlPart.xml | 1124275ab34e188b042b263d3c4b744abf5637ffd229af642b81a27f00a00c6b | 264d24445f42cf32706bc6942863f9f227eb797e |
| all-in-one/sources/decoded-original/0064-IdentXmlPart.xml | ce6afc4f7ca0a8059c2e3cab25d202f0faaa49a3bc6a2e9ee238964a76e9fc9d | 300d74239868f4f4595d4d5bbb848b4b58bbae76 |
| all-in-one/sources/decoded-original/0148-FlgNet.xml | 1d80e1bbf1c82dcc4dd18628c35935bbd55a17b5be9c1ca7bfb249600d154313 | 3069ae3b5fa16ed10a64c149b6cf5cb5ace423b3 |
| all-in-one/sources/decoded-original/0151-FlgNet.xml | 227627d165c6240a4c15b62fd4e4c8d7a621c15f35319cb424601df5cc52c904 | 8e8a9801d1f57180fc3747f6515c0353f38f7dc5 |
| all-in-one/sources/decoded-original/0152-FlgNet.xml | 2b6165460f06a52de56afcb4d65ed163d64320e24af1b194e934a4d7c6bfe49f | dd8e35b98043d9d0f230351352273eac1d783990 |
| all-in-one/sources/decoded-original/0198-FlgNet.xml | 95d631a1979b04f148bf6b71eebb8857e580511c523912d533814ed41dda871d | 965c744c3e216c3625c6ec414236d2db1b6ef6ce |
| all-in-one/sources/decoded-original/0199-FlgNet.xml | 005617b53ff1021c24dd11b19cae78c72ff535407999707d4c4636e493888b7c | ca1debbcfd0ca0a1555005886450db3e495d9772 |
| all-in-one/sources/decoded-original/0200-FlgNet.xml | 2bd1be34eb905a10d840c59aeb461464a1af418fa0ea3f2b8d0b3f88145eb27e | 31eb4f3df5596c004278ef7b3ccf158ae3878079 |
| all-in-one/sources/decoded-original/0201-FlgNet.xml | 77e7fdcb37e54b3d513aee760f3c142f7259990352dd0ad14a3c9a1a5f61da32 | 0268a83b49e442ee22406139e6bf5062b21bdc6a |
| all-in-one/sources/decoded-original/0202-FlgNet.xml | 8caa0c15a086ffb64f7857fb656b3baba3090a32948b9942ccecff6c730186bb | c8f6ed33f01b9c3cd126545969cd054ff298e086 |
| all-in-one/sources/decoded-original/0203-FlgNet.xml | 85510fca2cc0450d123d825e2c61e63d4d8c4ccbd354f58ee73d045e6967e7c9 | c8d01a1c97029d8bfc9f0be3513c34a94b398370 |
| all-in-one/sources/decoded-original/0204-FlgNet.xml | d34dd80c437e1ae8351dfbee61ce0db8f6c85ee3625ad2c09fa55d3aa64edc40 | 0f34353c5dc02e1e0f6bea231cd3e68e0b1e7165 |
| all-in-one/sources/decoded-original/0205-FlgNet.xml | 8003cb41dd3e68d51e5a91e1dee0726d98fd4ea3270a5ea93a4bfb871db67574 | 81ba42433699b834ab219990f172cf545d6f9aa6 |
| all-in-one/sources/decoded-original/0206-FlgNet.xml | 7eb7f0c937530eb553cb63ee40932230fda4222ef6678d34f0be3d47412bb603 | 0ed597ebe8e5e2c0e45f27cbde92dc93239d2d87 |
| all-in-one/sources/decoded-original/0207-FlgNet.xml | cfbf5535ee20794aaa138dd21a1c80fb3d246e0bf3303449d1eff49d3dca1377 | f847e614f1afd2c9226c94c7a5520fd4de0a16d3 |
| all-in-one/sources/decoded-original/0208-FlgNet.xml | b0c8b09146738898af5821fce9c80c9cf8af4c8728259b60577b54ae55a54d3d | 056e943ce5e82deb216c4b88ee67623c110e7f86 |
| all-in-one/sources/decoded-original/0209-FlgNet.xml | a120b9ed2abe7e65c896cf097dd4d85eb7fdc6726c5c4f5dff38ebafbf8c6801 | ee80c872f76ab1f333d1be6f0c231eec302448aa |
| all-in-one/sources/decoded-original/0210-FlgNet.xml | 80bf954b84e90fbec9a8c682a4f4097c47da3635e940008c88fc3df43463b677 | 50c08b684e06171ffafdfb4c213a3e433aa7cf15 |
| all-in-one/sources/decoded-original/0211-FlgNet.xml | d2d66556f622fc4f0264c638b22ed6a8add9bf3a55da6ecbfa344739703c1757 | a50f6d427472d8aacb2d0ec69a4735f25c6e6a37 |
| all-in-one/sources/decoded-original/0212-FlgNet.xml | f3dab4c2d6143637144daeecff0484ec546ab85e0c2ccab278ddcab8d72a1fc2 | a2a587f24d8f09ff0f63c760204fc10d4e048b22 |
| all-in-one/sources/decoded-original/0217-FlgNet.xml | cbff99bc9f5f8bbde0272c9541be1b26e48808865be58859ff6cef50b8eb9368 | 0a2ce467fd29315818de17b89093cf133e5742d8 |
| all-in-one/sources/decoded-original/0218-FlgNet.xml | 1cfcecebc32b8f69d30d2ea3946f13554acd79e3470e7d7b6358ac4f5e9e0481 | dc5271460b37bd944592574704ffde29b7ee1a7b |
| all-in-one/sources/decoded-original/0219-FlgNet.xml | 245409937abf7e28f25a24d4a6d311a801a4b2ee7293148be9b3d266352eb53a | d1c9ae9d9fe8a5a1ed605d09a3f9bd26c5632d0a |
| all-in-one/sources/decoded-original/0397-FlgNet.xml | bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834 | 4ab8370493c4e28fc1eabeeebe2743d27f0c4021 |
| all-in-one/sources/decoded-original/0401-FlgNet.xml | 60171c213e666de544077b7e4b497675813f7c0e75df85a3e76ab1def49b04ae | aadefbd35d305dd4a1146bf383b988a903802bf4 |
| all-in-one/sources/decoded-original/0522-FlgNet.xml | 4d40c7eba62351d26594cd810509e92bed51880a7545ac547ec9f29aee1a7e69 | 4a4db5284e4cc4963e3f933653946ca867cbd6d4 |
| all-in-one/sources/decoded-original/0540-FlgNet.xml | c05d5c1db35f1659992cae845cbcad515bbc34f00089169c0722076db9d77735 | 6b9a166d8fdf80bb52c63e90b794d69aaf34a919 |
| all-in-one/sources/decoded-original/0549-FlgNet.xml | 49f7169c33ed7f54559b0801e21a7d618584900972840e91cf51ad032e8febb1 | 985b5310b43b1015b5dee286aa0e42800564b94b |
| all-in-one/sources/decoded-original/0562-IdentXmlPart.xml | 85aada44dd9a3e66835463c3fed400f1efe121f4f5bc5ab8f0ad49481ec0ea1c | 1609802542a3e560baba3f2b73c306be281dfb23 |
| all-in-one/sources/decoded-original/0563-IdentXmlPart.xml | 86cf35b6baebc079cb5a092baf53ec3364c377ea7318eb263ab69c8b4550b4ad | 6a10fc694f896cda16409804daf2554c91635654 |
| all-in-one/sources/decoded-original/0564-IdentXmlPart.xml | 2aed17fa02d19b0a081023282841aa561d6a2dca3e393284da3622b967af00b1 | c4b1f2cb191970cfce1cce59cb290a9f1f934c37 |
| all-in-one/sources/decoded-original/0565-IdentXmlPart.xml | 0f7f970faa6c456f2bb032b1a2072a2f52db1e03fc77bd8d35d4583deeaf1149 | c2e3e2d57c94c5da864f6e172f0a7a925da942d6 |
| all-in-one/sources/decoded-original/0594-IdentXmlPart.xml | 88ad174a0d5ccdf636146b68e43aa578c449c77ceab074b7ced2580261b831cd | f38b7d9a52b3d5ae74953da8290f6b417758c1b5 |
| all-in-one/sources/decoded-original/0595-IdentXmlPart.xml | 10c8152d3ae704c00e5d4c2f6ef1629be5a65aaf5ef626e1ea6085b9204f8f52 | 1f24565efac58926dabf5b3fc54ad0e9537410b2 |
| all-in-one/sources/decoded-original/0596-IdentXmlPart.xml | a0d79c7c4971d16f0e176c0c7d7b459a6e6702035b01ec01fd83e95561839dc0 | c8b2d1a05727b4ca44e2e4bed9fb58ba2b717576 |
| all-in-one/sources/decoded-original/0597-IdentXmlPart.xml | 60e292145fe54912a1da7510c8641a4f4c85efe62e1b5206ee3d92794a28de20 | 2831597d1879bd83f239e838dd4cbe6b3dc64e77 |
| all-in-one/sources/decoded-original/0598-IdentXmlPart.xml | dc001c9370a691546c5dea79f5a1252d6d0a5564754703018c47df4bcc2522bb | 17a4c24ebc97eb13db483e4c64ac386d6a69125a |
| all-in-one/sources/decoded-original/0627-IdentXmlPart.xml | 08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb | 61ebc0abbb2ca160e11e1da400a3f14a397d8bc5 |
| all-in-one/sources/decoded-original/0628-IdentXmlPart.xml | 9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd | 170ca5c72599edc7ea7eefe651c3680ce325e76a |
| all-in-one/sources/decoded-original/0629-IdentXmlPart.xml | 67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972 | 058129bb01e27f7a6a0d0293f332d745e5bab74e |
| all-in-one/sources/decoded-original/0632-IdentXmlPart.xml | fd162c603476c2cac899010cee7a8ee382b6092c115135e3ac1007ae71c544e9 | 600935fa8d394c0d247ea20040d5dfff4f05b500 |
| all-in-one/sources/decoded-original/0633-IdentXmlPart.xml | 9e00aa275fa1b4e488b73983b309c6b73dcf4f3dd9be5dec13e9975d68f3c0fc | a1ab5ee12addbc92d04c9950d4437e2b564d6b5c |
| all-in-one/sources/decoded-original/0635-IdentXmlPart.xml | 1a057d686446a3fdab7ac61bb09bc543c52f49646c9ca71ac323c10fcdffe457 | 95bfcad59cfb0c12b573e9e8face4262d1e94622 |
| all-in-one/sources/decoded-original/0672-IdentXmlPart.xml | 6bfc2ba142d6270c39eb1f13b2886204865af6d46eadc5f410c26981b8da9222 | 2f2790dab4bb2357733112220e0acc41edb6feb6 |
| all-in-one/sources/decoded-original/0674-IdentXmlPart.xml | 4770702f519bacda69202bb2f7733d983074bda90964360c238f990d9d08fd84 | f210593944547b63eab10c667348711413600aab |
| all-in-one/sources/decoded-original/0676-IdentXmlPart.xml | c58427c5b0ac6c11cdb52e4c6d0461c7b191fae81ccace191048e9f175fcec59 | 1ed67265f69796a4e659f9438e551068037f33a4 |
| all-in-one/sources/decoded-original/0678-IdentXmlPart.xml | 51e637e0b9713c028810f2a717b5c3804a3a26c2f1be7e332a4d6bf277bfc382 | 7fafb2297bcdf739bf1d1dd68cebc0d74f2a40cc |
| all-in-one/sources/decoded-original/0680-IdentXmlPart.xml | fd551ad5d47bbd66c6bcdcc1949aaddf68cc086a3ddf6fb337adc767954c2b95 | c9049ced1eaed72c5e251a88601d46ddec8c3e50 |
| all-in-one/sources/decoded-original/0682-IdentXmlPart.xml | 25c7aeb1bfa29c178eaa396db33d4eb6d2d29b9a3f2eb965fa61fae8ce7f1092 | 61182411e912941161eccf4e90c1f174e5379f0a |
| all-in-one/sources/decoded-original/0683-IdentXmlPart.xml | 0c9b569d041cd5babbbeded8a3bdc5d3754927125756b6ac54b7cb991b22fc22 | 662acdb9a06c0ba1c0027e7dd215a28f07d3f02b |
| all-in-one/sources/decoded-original/0684-IdentXmlPart.xml | 6e9b3f173184adcddca503e81e2649022734b6ea3639c1d5ddaf0a08bac00208 | d67b98b5d5516e0330aae5cfdbee41a3e09206e1 |
| all-in-one/sources/decoded-original/0686-IdentXmlPart.xml | b450d8ff22f0fffd7a214b2a696af28a03a27834ebf862bfaa822dc9bfb3c8d4 | 8c152d926692a8e15973c980e08e338d29411814 |
| all-in-one/sources/decoded-original/0688-IdentXmlPart.xml | ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda | 463585759f1ecd94f32362b4fefb000a152f5773 |
| all-in-one/sources/decoded-original/0692-IdentXmlPart.xml | bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037 | 737785d03b5fad43c5b4d451955726d800edb1c0 |
| all-in-one/sources/decoded-original/0694-IdentXmlPart.xml | 757ccebdf32d0a168dd787bfa735fe6494eac4c4a9f7a5adc63898a88e8b152d | c45e8f3ca4129dc06734f6a12ef79e6ed6528a7d |
| all-in-one/sources/decoded-original/network-map.json | c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60 | 424430b6b953e43138e5d0a18ca40c949e21cfa1 |
| all-in-one/sources/electrical-page-text.json | 4b846819aab7e1306aebea617042f9f9ffe0c8aee1930e6f3db035bea3739153 | 1f48073c07b28e668d3d72d5ce49db263a5214e6 |
| all-in-one/sources/hmi-windows.csv | 15f8d69b5c43d4fdbe550f9cd2717f855fea877ed8146973054cb6dbcaa9892e | 8401dcfe5ba3e7e244eea0f501bb84a2e387da39 |
| all-in-one/sources/hmi_plc_tags.csv | a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404 | cf4c0650e7c7baac350dcb89909b808435704880 |
| all-in-one/sources/live_index.json | 14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1 | e35ccea1f841349c632666c29954b7bcd4f5839e |
| all-in-one/sources/source-manifest.json | 5af6e85994536897fd92f75972534a691e6eb0f067aafe07679c0788fd84e5bf | 38cf407491d52dc6128cf94ca8a4bddee350de6d |
| docs/equipment-standard/INVENTORY.json | 720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc | 587c3748ad9224718f95ba06463fee913dae231d |
| docs/equipment-standard/WORK-ITEM-TEMPLATE.md | 4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586 | e546f39535d2b589e80f97db869ac37ce4d05cfd |
| docs/equipment-standard/WORK-STANDARD.md | 05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99 | f76a570cc73098632e08759b17934000f7e3a253 |

## 부록 C. BF02 EV40개 고유 PLC 출력 경로

전체 행은0594의해당Output선언과0596 Ev_filter_on,0597비교상수,0598 Abilita_lavaggio_BF02를NID/UID로결속했다. 모든 행에서ON·Tag132의상위 직렬을확인했다. Wire열은순서대로상수→Eq.in2 / Eq.out→허가Contact.in / 허가Contact.out→Coil.in / 출력ORef→Coil.operand다. 각 행의EV번호·순번·Q주소는서로다른 항목이다. 이40가지PLC정적 검토로개별EV현장 완료를상속하지 않는다.

| 출력명 | 공통 순번 | 주소 | XML/NID | 출력 RID/ORef | Part 경로 | 핵심 Wire |
|---|---:|---|---|---|---|---|
| EV-51 | 12 | Q18.0 | 0205/10 | 95/964 | Eq894→Contact1066→Coil898 | W1006/1007/1067/1010 |
| EV-52 | 14 | Q18.1 | 0205/10 | 99/972 | Eq908→Contact1070→Coil912 | W1018/1019/1071/1022 |
| EV-53 | 16 | Q18.2 | 0205/10 | 103/980 | Eq922→Contact1074→Coil926 | W1030/1031/1075/1034 |
| EV-54 | 18 | Q18.3 | 0205/10 | 107/988 | Eq936→Contact1078→Coil940 | W1042/1043/1079/1046 |
| EV-55 | 20 | Q18.4 | 0205/10 | 111/996 | Eq950→Contact1082→Coil954 | W1054/1055/1083/1058 |
| EV-56 | 22 | Q18.5 | 0206/11 | 115/1100 | Eq1030→Contact1202→Coil1034 | W1142/1143/1203/1146 |
| EV-57 | 24 | Q18.6 | 0206/11 | 119/1108 | Eq1044→Contact1206→Coil1048 | W1154/1155/1207/1158 |
| EV-58 | 26 | Q18.7 | 0206/11 | 123/1116 | Eq1058→Contact1210→Coil1062 | W1166/1167/1211/1170 |
| EV-59 | 28 | Q19.0 | 0206/11 | 127/1124 | Eq1072→Contact1214→Coil1076 | W1178/1179/1215/1182 |
| EV-60 | 30 | Q19.1 | 0206/11 | 131/1132 | Eq1086→Contact1218→Coil1090 | W1190/1191/1219/1194 |
| EV-61 | 32 | Q19.2 | 0207/12 | 135/1236 | Eq1166→Contact1338→Coil1170 | W1278/1279/1339/1282 |
| EV-62 | 34 | Q19.3 | 0207/12 | 139/1244 | Eq1180→Contact1342→Coil1184 | W1290/1291/1343/1294 |
| EV-63 | 36 | Q19.4 | 0207/12 | 143/1252 | Eq1194→Contact1346→Coil1198 | W1302/1303/1347/1306 |
| EV-64 | 38 | Q19.5 | 0207/12 | 147/1260 | Eq1208→Contact1350→Coil1212 | W1314/1315/1351/1318 |
| EV-65 | 40 | Q19.6 | 0207/12 | 151/1268 | Eq1222→Contact1354→Coil1226 | W1326/1327/1355/1330 |
| EV-66 | 42 | Q19.7 | 0208/13 | 155/1372 | Eq1302→Contact1474→Coil1306 | W1414/1415/1475/1418 |
| EV-67 | 44 | Q20.0 | 0208/13 | 159/1380 | Eq1316→Contact1478→Coil1320 | W1426/1427/1479/1430 |
| EV-68 | 46 | Q20.1 | 0208/13 | 163/1388 | Eq1330→Contact1482→Coil1334 | W1438/1439/1483/1442 |
| EV-69 | 48 | Q20.2 | 0208/13 | 167/1396 | Eq1344→Contact1486→Coil1348 | W1450/1451/1487/1454 |
| EV-70 | 50 | Q20.3 | 0208/13 | 170/1404 | Eq1358→Contact1490→Coil1362 | W1462/1463/1491/1466 |
| EV-71 | 52 | Q20.4 | 0209/14 | 173/1508 | Eq1438→Contact1610→Coil1442 | W1550/1551/1611/1554 |
| EV-72 | 54 | Q20.5 | 0209/14 | 177/1516 | Eq1452→Contact1614→Coil1456 | W1562/1563/1615/1566 |
| EV-73 | 56 | Q20.6 | 0209/14 | 181/1524 | Eq1466→Contact1618→Coil1470 | W1574/1575/1619/1578 |
| EV-74 | 58 | Q20.7 | 0209/14 | 185/1532 | Eq1480→Contact1622→Coil1484 | W1586/1587/1623/1590 |
| EV-75 | 60 | Q21.0 | 0209/14 | 189/1540 | Eq1494→Contact1626→Coil1498 | W1598/1599/1627/1602 |
| EV-76 | 62 | Q21.1 | 0210/15 | 193/1644 | Eq1574→Contact1746→Coil1578 | W1686/1687/1747/1690 |
| EV-77 | 64 | Q21.2 | 0210/15 | 197/1652 | Eq1588→Contact1750→Coil1592 | W1698/1699/1751/1702 |
| EV-78 | 66 | Q21.3 | 0210/15 | 201/1660 | Eq1602→Contact1754→Coil1606 | W1710/1711/1755/1714 |
| EV-79 | 68 | Q21.4 | 0210/15 | 205/1668 | Eq1616→Contact1758→Coil1620 | W1722/1723/1759/1726 |
| EV-80 | 70 | Q21.5 | 0210/15 | 209/1676 | Eq1630→Contact1762→Coil1634 | W1734/1735/1763/1738 |
| EV-81 | 72 | Q21.6 | 0211/16 | 213/1780 | Eq1710→Contact1882→Coil1714 | W1822/1823/1883/1826 |
| EV-82 | 74 | Q21.7 | 0211/16 | 217/1788 | Eq1724→Contact1886→Coil1728 | W1834/1835/1887/1838 |
| EV-83 | 76 | Q22.0 | 0211/16 | 221/1796 | Eq1738→Contact1890→Coil1742 | W1846/1847/1891/1850 |
| EV-84 | 78 | Q22.1 | 0211/16 | 225/1804 | Eq1752→Contact1894→Coil1756 | W1858/1859/1895/1862 |
| EV-85 | 80 | Q22.2 | 0211/16 | 229/1812 | Eq1766→Contact1898→Coil1770 | W1870/1871/1899/1874 |
| EV-86 | 82 | Q22.3 | 0212/17 | 233/1916 | Eq1846→Contact2018→Coil1850 | W1958/1959/2019/1962 |
| EV-87 | 84 | Q22.4 | 0212/17 | 237/1924 | Eq1860→Contact2022→Coil1864 | W1970/1971/2023/1974 |
| EV-88 | 86 | Q22.5 | 0212/17 | 241/1932 | Eq1874→Contact2026→Coil1878 | W1982/1983/2027/1986 |
| EV-89 | 88 | Q22.6 | 0212/17 | 245/1940 | Eq1888→Contact2030→Coil1892 | W1994/1995/2031/1998 |
| EV-90 | 90 | Q22.7 | 0212/17 | 248/1948 | Eq1902→Contact2034→Coil1906 | W2006/2007/2035/2010 |

## 부록 D. 수행 검사와 인계 파일

- 읽기 전용 preflight.py: 종료0, inventory_matches=true. 로그는 extracts/BF02/preflight.json. 원본 source_byte_changes 두 항목은 기존 값으로 보존했다.
- 조사 전용 extract.py: 원본 XML을 읽어 이 작업의 extracts/BF02에만 선언·핀·선 목록을 저장했다. 원본 생성기나 PLC 실행기가 아니다.
- extract_ev_paths.py: 종료0. 40개 고유 EV의 선언→Coil→허가 Contact→Eq 상수→Tag132→ON 연결을 정적으로 확인했다. 결과 ev-paths.json, ev-paths-table.md. 동작·시뮬레이션 시험은 아니다.
- build_manifest.py: 종료0. 고정 Git blob과 파일 SHA-256 94개 일치, 중지5 freeze 일치. 결과 source-sha256.json. 원본 바이너리 전체 의미 검토와 구분한다.
- verify_draft.py: 종료0. 해시·고정 커밋·Git clean·EV40행·HMI8행·28개 선택 경로·18개 PDF페이지 수·주석 SCL·FG182 2L+/2M 표기·미기입 placeholder 부재를 확인했다. 결과 verification.json. 이 검사와 자체 검토는 외부 독립 검토를 대신하지 않는다.
- PDF 렌더: PyMuPDF로 실제 페이지를 렌더한 뒤 시각 확인했다. 추가 상세 크롭은 원본 페이지 수에 중복 합산하지 않았다. FG182는 상세 렌더에서 2L+/2M 공급을 재확인했다.
- 종료 Git 상태: source-mv06 변경0. 프로그램/문서 생성기, npm/브라우저 UI 시험, 패키지·배포, TIA·CPU·현장·사용자 운영 기록 작업은 실행하지 않았다.

완료 커밋은 없다. 새 Git 커밋·통합·배포를 수행하지 않은 읽기 전용 조사 초안이다. 최종 인계물은 이 MD, 검토를 재현할 원본 위치/해시, extracts/BF02의 정적 근거이며 사용자 전달은 상위 작업에서 진행한다.
