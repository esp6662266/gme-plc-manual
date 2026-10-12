# TC07 온도 계측 — 고유 원본 조사 7영역 초안

## 핵심 확인·상충·누락

- TC07 환산 호출 0493/LAD1743/NID13은 **OFF(M0.1) 접점415가 EN을 허가하고 IN0에는 ON(M0.0)**을 전달한다. 다른 TC의 ON→EN 회로를 복사하지 않았다. 이름만으로 현재 OFF=False나 호출 비활성을 확정하지 않는다.
- 원시 `%IW280:P` Int → FC63 → `Data.TC_07` DB1.DBW190 Int와 별도 `%IW280` → `Inputs.TC_07` DB13.DBW44 Word HMI 미러가 공존한다. OFR는 DB3.DBX21.6이다.
- OEM FG78/PDF79와 FG107/PDF108에 TC07 관련 SPARE가 실제 보인다. 그러나 PLC/HMI 주소와 시공 PDF3/30/56의 TC07 배치·케이블이 존재한다. SPARE만으로 미설치·철거·현재 사용중지·제외대상 편입을 단정하지 않는다.
- FG78 도면은 4–20mA·0/750°C이나 백업 계수 색인 doc1604는 ZERO=0, COEFF=1330이다. 공통 계산 분모28000과 결합해도 현행 0/750°C 교정 일치를 입증하지 못한다. 승인 교정·현재 설정 추가자료가 필요하다.
- 시공 PDF3은 FLOW_A/AB-01의 센서 TC-07, PDF30/56 케이블은 `6_25=FLA+MV02-TC07A`, TO LOC=FLA다. AB01·MV02와 동일 실물/전용 제어소유라고 합치지 않는다. OEM 송신출력 4–20mA와 시공 KX/TC 구간의 경계·실제 프로브/송신기 위치·열전대 타입/보상은 미확정이다.
- 고유 온도 상·하한 S/R 경보나 지연 타이머는 명명 선언·사용처 조사에서 확인하지 못했다. TC01/02/03의 비교·온도 경보나 3초 타이머를 복사하지 않는다. OFR 외 안전 기능이 없다는 결론도 아니다.

공유 근거: 같은 고정 입력의 BF01/BF02 공통 호출·startup Word쓰기 경계와 TC03의 0291/0014 선형화 분석을 연결 재사용했다. 고유0493·0398 TC07 가지, 해당 선언/핀, HMI5행, OEM2쪽·시공3쪽은 독립 재확인했다. 다른 초안 원문은 수정하지 않았다.

## 1. 설비·자료 기준

catalog_id=TC07, 온도 계측(sensor/계측), parent 없음/depth0/priority_key 없음, 별칭 tc_07, phase2/planned. INVENTORY catalog[18], 파생 equipment[82] 및 BATCH08-SCOPE/OVERLAP 해당 행은 유입 가스 온도·예비/운영 상태 확인으로 분류한다. 신규 조사대상이고 기존 명시제외90로 임의 편입하지 않는다. TC06/AB01/CC01/MV02 및 다른 TC를 함께 완료 집계하지 않는다.

고정 읽기전용 원본 `gme-research/source-mv06`, commit `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, VERSION 1.12.0. 사용자가 보고한 최신 실제 게시 상태나 현재 CPU를 검증한 것이 아니다. AGENTS, rollout 스킬/source-map, WORK-STANDARD/WORK-ITEM-TEMPLATE/INVENTORY/START-GPT61 및 VERSION/EXPANSION-WORK/WORKSPACE-HANDOFF/PUBLICATION_STATUS/ACTIVE-WORK 최상단을 읽었다. 최신 배치의 5개 병렬 자체조사·로컬2차133 통합제외 범위를 적용한다.

실행 모델·추론 런타임 증명 미확인. 로컬 TIA 추가권한·새 Work/Codex·재위임·사용자 Mac 접근 없음. 쓰기는 본 초안 및 `extracts/TC07/`뿐이다. 원본·공유코드·대장·버전·배포·운영기록·SEJIN 변경0, 시뮬레이터 작성/수정/생성/실행/행동시험0, PLC/현장/보호값 변경0. build/test/generator는 실행하지 않았다.

이하 경로 기본은 `source-mv06/all-in-one/`. `0493`은 `sources/decoded-original/0493-FlgNet.xml`; 선언은 별도 `NNNN-IdentXmlPart.xml`. LAD 문서번호와 원본 NID는 다른 식별자다. RID/UID의 전역 충돌을 피하고 해당 선언 블록·NID 문맥으로 결속했다.

| 7영역 | 적용 | 미확정 경계 |
|---|---|---|
| 설비·자료 | 적용 | 현행 실물·예비/사용 상태 |
| IO/HMI | 적용 | 실제 화면·쓰기 이벤트·통신 |
| 제어 | 적용 | 호출·현재 ON/OFF·최종값/간접 Writer |
| 전기끝점 | 적용/일부 미확보 | 설치·송신기/프로브·보상/교정 |
| 알람/복구 | OFR 적용/고유 타이머 미확보 | 현재 알림·안전기능·복구 |
| 증상관찰 | 적용 | 실제 관찰·정비·운전시험 미수행 |
| 완료/누락 | 적용 | 제품통합·독립검토·현장 별도 |

## 2. IO/HMI

### 2.1 원본 선언·주소

SSD.AO/AOS.BO는 bit offset이다. 0674 DepDBBlock RID8/11/354의 TOD N=4/1/3으로 DB4/DB1/DB3를, 0628 RID4 TOD13으로 Inputs DB13을 확인했다. 주소 표는 백업 기준이다.

| 역할·신호 | 형식·주소 | 원본 선언·접속 |
|---|---|---|
| 환산 원시 TC07 | Global Int IW280:P | 0678 SimpleAccess RID86, AO2240, SAD Input/SAM=Peripherie, NID13 UID404 |
| HMI 원시 읽기 TC07 | Global Int IW280 | 0627 RID73 AO2240 Input/SAM=None, NID2 UID80 |
| Inputs.TC_07 | Global Word DB13.DBW44 | 0629 RID75 AO352 BAD4, NID2 UID81 Write |
| Coeff.ZERO_TC07 | Global Int DB4.DBW28 | 0676 RID88 AO224 BAD8, NID13 UID406 Read |
| Coeff.COEFF_TC07 | Global Int DB4.DBW30 | 0676 RID87 AO240 BAD8, NID13 UID405 Read |
| Data.TC_07 | Global Int DB1.DBW190 | 0676 RID89 AO1520 BAD11, NID13 UID407 Write |
| Allarm.TC07_OFR | Global Bool DB3.DBX21.6 | 0676 RID381 AO174 BAD354, NID13 UID23 Write |
| ON / OFF | Global Bool M0.0 / M0.1 | 0678 RID1/34, Memory AO0/1; NID13 UID403/402 |

TC07 고유 Local 선언은 이번 명명 검색에서 확인하지 못했다. 공통 FC 내부 Local Int/DInt·Bool은 함수의 임시값/인터페이스이지 TC07 전용 DB나 타이머가 아니다. 전체 이름 검색과 직접 절대주소 겹침 검사는 간접 포인터·블록복사·통신 Writer 부재를 보장하지 않는다.

### 2.2 HMI 5행

`sources/hmi_plc_tags.csv`(dde.cfg 설정 추출, Access Name=PLC):

| 태그 | 설정 주소 | 내부 ID | 의미 |
|---|---|---|---|
| I_TC_07 | DB13,INT44 | 00052 | PLC Word 원시 미러를 HMI INT 설정으로 읽음 |
| data_DB1_DBW190 | DB1,INT190 | 002D1 | 환산 결과 주소 |
| Coeff_DB4_DBW28 | DB4,INT28 | 002AF | 제로 주소 |
| Coeff_DB4_DBW30 | DB4,INT30 | 00225 | 계수 주소 |
| Allarmi_212 | DB3,X21.6 | 002C6 | OFR 비트 주소 |

주소행 존재는 화면 가시성·°C 소수점·사용자 조작·설정 쓰기·ACK·온라인 값·통신 정상 증거가 아니다. 시공 SPARE와 HMI 존재를 서로 취소하는 근거로 쓰지 않는다.

0398/LAD1071/NID2의 Move74(DisableENO=true)는 ORef80/RID73→W91→in, out1→W93→ORef81/RID75이다. TC06 Move73.eno→W89→Move74.en, Move74.eno→W92→Move75.en의 직렬 연결도 보존한다. 0398은 TC07 온도 환산이 아니라 raw 전달이다. 앞 Move들로부터 이어지는 전원/ENO 조건과 main HMI Inputs 호출 조건을 무조건 실행으로 바꾸지 않는다.

## 3. 제어 구조·소유

### 3.1 고유 호출 전체 핀

0493/LAD1743/NID13: rail→W417→Contact415.in. OFF ORef402/RID34→W409→415.operand(반전 없음), 415.out→W416→CRef396.en. ON ORef403/RID1→W410→396.IN0. CRef396 RefId351은 0680 BlockInterfaceInfo와 결속하고, 자식 CodeBlock408 RefId5는 0672 `Signal linearization`, FC63 선언과 결속한다.

| Wire | 핀/대상 |
|---|---|
| W411 | ORef404 TC07:P → CRef396.Analog_input |
| W412 | ORef405 COEFF_TC07 → Coeff |
| W413 | ORef406 ZERO_TC07 → Zero |
| W414 | OutValue → ORef407 Data.TC_07 |
| W24 | Out_of_range → ORef23 Allarm.TC07_OFR |

EN=OFF와 IN0=ON은 별도 조건이다. OFF=0이면 함수 호출을 건너뛸 가능성과 함수가 호출되어 IN0=0인 경우의 0014 Move0을 구분한다. EN 비활성 때 결과나 OFR가 반드시0이라는 해석은 하지 않는다.

### 3.2 공통 함수 연결 재사용 및 핵심 대조

0291의 IN0 ORef196→W220 Contact255→W256. 유효범위 Gt258 `raw>-1382` 뒤 Le161 `raw<=32767`→Convert164. Int raw/Zero/Coeff를 Convert164/167/174로 DInt로 바꾸고 Add170/Mul177/Div181(상수28000) 및 Move185로 OutValue(Int)에 전달한다. 식은 `(DInt(raw)+DInt(zero))*DInt(coeff)/28000`; Real 연산이나 단순 raw/10 온도 환산으로 바꾸지 않는다. W227/230/234/237/241/245는 ENO 연쇄다. 절삭·오버플로·ENO 실패·현재 스캔의 최종값은 CPU에서 시험하지 않았다.

범위 이탈 Gt190(raw>32767) OR Le259(raw<=-1382)→O47→Move193(-9999)→W253 OutValue. **W21 Move193.eno→Coil23.in**, W22→Out_of_range다. OFR는 범위 비교 결과를 곧바로 S latch한 비트가 아니다. raw Int 상한보다 큰 비교가지의 정적 존재와 실제 도달가능성은 구분한다.

0014는 Contact171의 operand NOT IN0→W172→Move162(0)→W170 OutValue. 호출이 실제 실행된다는 전제가 필요하다. -9999나0은 원본 대체값이며 현장 안전온도나 복구 판정값이 아니다. 공통 함수의 Local/상수 선언은 추출 refs의 해당 블록 파일로 확인하고 동일 RID의 다른 블록 후보를 채택하지 않았다.

### 3.3 호출·ON/OFF·저장값

공유0031/LAD1619/NID6은 ON Contact282의 out W283을 Analog input conversion CRef261 및 Allarms1/2/3에 각각 en 분기한다. 0688 RID55 CodeBlock273=FC3, 0694 호출 인터페이스 연결이다. TC07 고유 OFF 조건은 그 안의0493에 별도로 남아 있다. 0030 HMI Inputs CRef28의 main 허가/Simulation 반전 경계도 같은 고정원본 공통근거를 재사용한다. 실제 OB/호출 실행·주기·현재 CPU 일치는 미확정이다.

보충 `live_index.json` _7ev/doc401은 `set s "on" clr s "off"`라는 STL 검색텍스트다. 0047 ON/OFF Write 선언과 공통 BF01 근거를 연결하되 CLR 다음 S를 R로 고쳐 읽지 않고 현재 OFF=False 고정도 선언하지 않는다. doc401은 0401-FlgNet(HMI 출력 미러)과 다르다.

보충 snapshot doc1604 이름/형/값 129/129/129 일치: ZERO_TC07 Int0, COEFF_TC07 Int1330. doc1629는162/162/162 일치: TC_07 Int−9999. 이것은 백업 저장값이며 현재 설정·교정·경보 활성이나 설치 부재를 증명하지 않는다. OEM 0/750°C와 계수1330의 차이는 범위/교정 확인 항목으로 남긴다. 승인되지 않은 계수 변경 권고를 하지 않는다.

TC07는 문서상 센서/계측 채널이다. 독립 Q 출력·버너 정지·댐퍼 출력·모터 Run을 직접 소유한다고 확인하지 않았다. 시공 AB01/MV02/FLA는 관련 위치/케이블 명칭으로만 유지한다. 주변 설비나 공통 FC를 TC07 하위완료로 집계하지 않는다.

## 4. 전기 끝점·실제 PDF

PDF 원본을 pdftoppm으로 렌더하고 내용과 footer를 직접 확인했다. FG와 실제 PDF 순번을 각각 기록한다. 파일명 Rev2를 모든 시트 개정으로 복제하지 않는다.

| 원본·실제쪽 | 제목·footer | 고유 끝점 |
|---|---|---|
| Electrical_Rev2.pdf FG78/PDF79 | THERMOCOUPLE; DATA27.05.2024; **Rev2 17.03.2025** | TC07 SPARE 점선, SAFETY TEMPERATURE CONTROL INPUT SMOKE,4–20mA,0/750°C |
| 동일 FG107/PDF108 | ANALOG INPUT MODULE; DATA27.05.2024; **Rev2 17.03.2025** | SPARE점선 TC07/인접ZT01, PEW280, CPU515/MOD3 표기 |
| 시공 PDF3 | CANDC-CONS-S003-003,D-page3,total3/64;Rev1 24.11.11 first draft design | FLOW_A/AB-01/TC-07 배치표 |
| 시공 PDF30 | CANDC-CONS-E013-030,D-page13,total30/64;동일Rev1 | FLOW_A ZONE05,행17 Pipe16,LOC FLA/TAG TC-07,KX1.0/2 |
| 시공 PDF56 | CANDC-CONS-C006-056,D-page6,total56/64;동일Rev1 | 행6_25 CR→FLA/TC-07,TC/KX2S1.0,경로100→110LAD1→E1700,길이60 |

시공도 Checked/Approved란은 위 세 렌더에서 공란이다. 이를 승인 준공도로 부르지 않는다. PDF56 상부 검은 덮개로 가려진 행은 텍스트 추출에 TC07 관련 문자열이 나와도 현행 가시 행/확정 경로로 채택하지 않았다. 고유 케이블 증거는 실제 보이는6_25이다.

FG78 오른쪽 TC07: +24Vdc10.7(77/9→79/0)→5×20 50mA F/X1:198→선78.2→TC07 +5. TC07 −6→X1:199→+PEW280/107/1. 실드78SCH2는 X1:200을 통해107/1로 이어진다. X1:198/199/200을 왼쪽 TC06의195/196/197과 섞지 않는다.

FG107: +PEW280(78/5)→AI 단자22 I4+. 78SCH2(78/5)는 실드 경로이며 I4−와 같은 도체라고 쓰지 않는다. 24 U4−/I4−는 공통선으로 −0Vdc10.6에 연결되고 28/32/36과 함께 그려진다. 모듈 공급은 +24Vdc10.7→X21:3001/5×20 500mA F→선107.1→41 L+, 공통→44 M. 21 Uv4/23 U4+ 등의 인접 단자는 본 경로에서 접속을 임의 추가하지 않는다. CPU515/MOD3는 도면 표기이며 현행 CPU 식별 증명이 아니다.

OEM 송신기 단자 +5/−6와 4–20mA 출력, 시공 TC/KX 케이블은 서로 다른 계측 구간일 수 있다. 프로브·송신기 배치·센서 타입·냉접점 보상·보상선/연장선 결선·현행 AI 설정 및 모델은 자료 미확정이다. TC07에는 이 검토에서 릴레이 부하5/9 경로를 확인하지 않았으므로 다른 설비 릴레이접점을 복사하지 않는다.

## 5. 알람·복구

- 고유 범위출력:0493 CRef396.Out_of_range W24→ORef23/RID381→DB3.DBX21.6. 0291에서는 Move193 ENO로 Coil23을 구동한다. 온도 상한 비교 SCoil/RCoil과 구분한다.
- 명명 선언·사용처 전체 검색에서 TC07 전용 HIGH/LOW/MAX, S/R 유지·재요청·지연 타이머를 찾지 못했다. 타 TC의3초/1분이나 버너의 타이머를 TC07 것으로 작성하지 않는다. 도면 제목 SAFETY만으로 SIL·안전 차단·자동복귀·버너 인터록을 발명하지 않는다.
- 공통 startup0148의 Allarm Word0~16 쓰기는 Byte21.6의 OFR를 포함하지 않는다. 공통 Word경보 집계0~16 범위를 TC07의 경적/정지 증거로 확대하지 않는다. HMI Allarmi_212 주소 존재와 실제 팝업·ACK·소리·상위 안전소비는 별개다.
- 이름 및 주소범위 검색에서 고유 Data.TC_07/OFR의 추가 직접 Writer를 확인하지 못한 범위와 외부 HMI/간접·통신 쓰기 가능성을 구분한다. 현재 EN/IN0·호출비활성·리텐션·오류 해제와 실제 현장복구는 미확정이다.
- OFR 해제, 실제 온도 정상, 원인 제거, 재운전 허가, 설비 복구 완료는 각각 증거가 필요하다. 이번에는 Reset·Force·온라인 변경·시동을 수행하지 않았다.

## 6. 증상별 관찰

아래는 승인된 읽기 전용 관찰자료 수집표다. 센서탈거·회로주입·전원작업·Reset·Force·보호값 변경 지시가 아니다.

| 증상 | 같은 시각에 확보할 값·자료 | 비교 및 원인배제 |
|---|---|---|
| SPARE인데 HMI값 존재 | 현행 준공도·명판/설치 위치·화면주소·CPU프로젝트 식별 | 도면상 예비와 주소잔존/실제운영을 구분;값만으로 설치여부 판정금지 |
| raw와 환산값 다름 | IW280:P/IW280,DB13W44,DB1W190,DB4W28/30,시각/신선도 | Peripherie/None,Word/Int,raw/환산,호출EN/IN0 차이 분리 |
| 값 고정 또는−9999 | OFF M0.1,ON M0.0,FC3/FC63 호출·OFR,raw·계수·제로 | 호출미실행과 계산범위/MoveENO·저장잔존을 구분;단선으로 즉시 단정금지 |
| 도면 750°C와 값범위 불일치 | 송신기/프로브 명판·교정기록·AI설정·실제 계수 | 도면0/750과 snapshot1330의 불일치를 승인자료로 확인;임의 계수조정금지 |
| OFR/HMI표시와 경적반응 다름 | DB3X21.6,Allarmi_212 이벤트·ACK설정,집계범위,기록시각 | 태그주소와 실제 경보소비·표시·소리 분리 |
| AB01/MV02 소유 혼동 | PDF3/30/56,케이블6_25,실제 구간·사진 | 케이블 MV02 이름과 LOC FLA/배치 AB01을 보존하고 동일실물 추정금지 |

기록 필드: 관찰자, 실제 시각/시간대, 위치·태그·주소, 값/단위·갱신시각, 수집장치, 프로젝트·CPU 식별, 원본판본, 비교·배제 결과, 승인조치, 별도 복구 확인. 실제 운영기록·사진을 복제하거나 생성하지 않았다.

## 7. 완료·검사·누락

| 구분 | 상태 |
|---|---|
| documentation | draft_complete_with_gaps: 고유7영역 작성 |
| static_review | 고유핀·선언·HMI5행·PDF5쪽 대조;독립검토는 부모 인계 |
| ui_records | not_run |
| publication | not_published;제품통합 없음 |
| tia_compile / live_cpu / field_recovery | 모두 not_performed |

네 기능: 도면·래더 나란히 비교는 원본위치 준비만, 앱 구현/실제 링크동작 미검증. 백업·선택복원·기록 전후비교·보고서/PDF의 TC07 지원과 저장/재읽기/재열기는 시험하지 않았다. 원본 PDF 렌더를 관찰보고서 출력시험으로 세지 않는다. 기존 note/repair_observation·미지필드·타 설비·초안·저장키 보존.

직접 의미검토 범위는0493 전체 TC07 호출,0398 Move74의 고유 raw 전달,0291/0014 환산·OFR 핵심,관련 선언/주소와 실제 도면5쪽이다. 공통 main/startup은 기존 고정근거 연결과 관련 핀/범위 대조이며 전체 네트워크 의미완료가 아니다. 해시파일 수와 의미검토 건수는 다르다.

남은 자료: 승인 준공도 및 현재 SPARE/설치/사용상태, 실제 송신기·프로브·열전대·보상/교정,현재 CPU프로젝트·호출·ON/OFF·간접Writer,현행 스케일/설정,실제 HMI 표시·쓰기/ACK·안전기능,현장 관찰·승인조치·복구 증거. 새자료 없이 실물보류 전검색을 반복하지 않는다. 다음 한 작업은 부모의 OFF→EN 및 PDF 개정/단자·범위상충 독립검토다. 이 초안은 TC07 제품통합·PLC 변경·현장복구 승인이 아니다.

### 실제 단계 시각 (UTC)

- 2026-10-11T11:15:07Z — instructions_scope_read
- 2026-10-11T11:15:35Z — TC07_declarations_extracted
- 2026-10-11T11:16:01Z — OEM_PDF2_visually_reviewed
- 2026-10-11T11:16:27Z — construction_PDF3_visually_reviewed
- 2026-10-11T11:17:26Z — supplemental_HMI_and_snapshot_verified
- 2026-10-11T11:20:09Z — seven_area_draft_written
- 2026-10-11T11:21:14.797818+00:00 — XML_assertions_source_blob_hashes_verified

### 원본 SHA256·고정 Git blob 전체 목록

선택 근거/맥락/보존 48파일 모두 고정 blob 바이트 일치. 중지5자산 freeze 일치. 원본 Git 변경0. 해시 개수는 전체 의미검토 수가 아니다. `extracts/TC07/source-hashes.json`과 `static-review.json`으로 재검토할 수 있다.

| 원본 경로 | SHA256 | 고정 Git blob OID | 일치 |
|---|---|---|---|
| `.agents/skills/gme-equipment-rollout/SKILL.md` | `fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b` | `9aa820ea6ca15b4e136c9772423b78ed4df6a3d4` | true |
| `.agents/skills/gme-equipment-rollout/references/source-map.md` | `40612c5efb8f94608840c7bc0e9095ea840df54920861c388ae48ea34c7998dc` | `49e50a7a8e56a16e2ec7f3607a03fd90adb8f1d3` | true |
| `AGENTS.md` | `0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2` | `073164bc6efd5791032d62c71b03b4dab48cb6f8` | true |
| `EXPANSION-WORK.md` | `ec624de9fd2fcfac861a67fd5e828b25ef46db50bfd7a37ff16e2cb54cd0f7e2` | `4c42d88ecc2d48269eb23e13a20ebf3721a092a1` | true |
| `PUBLICATION_STATUS.md` | `efe4857aec598d90470322cf3962eb3fe1f64947630e1fdf71d1c90134de8740` | `d76401cf291fc0be681acc51fa898ad3ce46ff78` | true |
| `VERSION.json` | `5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7` | `fffb51663b7705aec91cb119ca80ee943a4ce758` | true |
| `WORKSPACE-HANDOFF.md` | `215096d997782e78e901dfae36c782937e49611fbeb677a0d3fa50cbecf8d074` | `dd0b8989d2376c4415bba9bd826fe6754c6b1a12` | true |
| `all-in-one/ACTIVE-WORK.md` | `eff3bbc08ecff41da3beff77f3fec48e7d148708192bcaaab00f34b6a721afc2` | `6eb947c629b5ddf9c759ef87649451303938864b` | true |
| `all-in-one/assets/program-model-data.js` | `52f8199371e3399b7c0d44ab5469f0472aced79d56bbef2887f7625f5d2aff0f` | `38f34b0caa380a16ccad6f6f1e234a2fdf23f327` | true |
| `all-in-one/assets/simulator-workspace.js` | `3a6dfc618ff7e7b238f2671dc85d65704f33093a18eac879d86081d92c31e8bc` | `97c2c831c77a9699fff0e0960b3bc1b7d93d45b3` | true |
| `all-in-one/assets/virtual-plc.js` | `5f1876052dc0067b1f010af0dfc941946e37003167481731293615d9c1c36dbc` | `0bd9eceb54365a91214a37c5601b5067c39a3f75` | true |
| `all-in-one/registers/equipment.json` | `7870325dff32bbca90fa34507b301c4aad3347d669fddcd03b910343663996fa` | `acc42633033398216469064932c4b76987371606` | true |
| `all-in-one/registers/program-model.json` | `6203479c086b15bada12ac9d7e37db9280234ec26f1ea6091d7211dc09a577c5` | `9860b10f008d3a5ae714be50d77b703dfec32f3a` | true |
| `all-in-one/registers/simulator-freeze.json` | `bb93c1994effc5609939ba566b7802ce7ed55154a7310f02379b308ac2c8c835` | `808ffac14dbd1b4a7d797fa6cd0d647635d90b47` | true |
| `all-in-one/registers/virtual-plc-test-results.json` | `a6b389f797f9a8b5ffe6928b8420f55c4cc459a327b0b48d716079d2eca6dd64` | `757dd50e45184568facb8ff62900b39d3ce848d1` | true |
| `all-in-one/sources/Electrical_Can_Decoating_20241118.pdf` | `3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd` | `0ee6b6f8361c5790864dbba4bbd9d55e8e7c08f8` | true |
| `all-in-one/sources/Electrical_Rev2.pdf` | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` | `f610fd7c7ce14ae951b00cff57b969259bfb389d` | true |
| `all-in-one/sources/GME_20250506.zap18` | `00c79b6d986e68298f65b172c1807115bc5d9e450a74fcc989d0796d8d8a4ea8` | `211c4f604627a32f82a1124c2a9872c2fcf00865` | true |
| `all-in-one/sources/PEData.plf` | `647de7ea123daced41c27bec8f81aeb93c712cac714d4754d7da5c528abb016a` | `65605ff8910f920109da731604aa5dc8d83fc956` | true |
| `all-in-one/sources/decoded-original/0014-FlgNet.xml` | `2e814adbaac6bab99bc668bfdab74f0fc90576324d0b88728951683869cfac30` | `4d164b074fcc13a8f97da9e24382cc169ef29555` | true |
| `all-in-one/sources/decoded-original/0030-FlgNet.xml` | `9252c9da764993de1edb8b2e44c46d6e9f9d4b6118e751a0dbeaa9ffd8ea721b` | `e74c70b751acdcdbc7a8b3b0c98aa773c2107cab` | true |
| `all-in-one/sources/decoded-original/0031-FlgNet.xml` | `76385eab8f8f72b9faa16f7cf8905f395591b18c0a9ee9e6d7dd085a38c45c65` | `653d27572de6beedcf3eb6c95702bb119a8b567f` | true |
| `all-in-one/sources/decoded-original/0047-IdentXmlPart.xml` | `2e53bb895dd1ad2a74efaeb1ef16dfd61e62b1b2d7aa34cec8612f1b9cb0928e` | `3dc282f149a21fdf76d5521ef1c833be63b578b4` | true |
| `all-in-one/sources/decoded-original/0148-FlgNet.xml` | `1d80e1bbf1c82dcc4dd18628c35935bbd55a17b5be9c1ca7bfb249600d154313` | `3069ae3b5fa16ed10a64c149b6cf5cb5ace423b3` | true |
| `all-in-one/sources/decoded-original/0291-FlgNet.xml` | `fe0b92f074eba25148ce34084649af3d968962558d652727f1eea19f3e3c2550` | `1418fb2ed172c6df694a5eb8bf2dffd0b177653b` | true |
| `all-in-one/sources/decoded-original/0398-FlgNet.xml` | `4f092b18df4e44af98fd44e173f48dad213a4e80b71f46b0a5e8a700f5b0a747` | `67ebb54daa55093487ea7e780f23ae2cf193c397` | true |
| `all-in-one/sources/decoded-original/0493-FlgNet.xml` | `991673aed363870b817d18e14865ffb8c89a955e3780331e5a3b25dfe8595a38` | `52f0a875224e5725f00162de4cfa9211828b7a4a` | true |
| `all-in-one/sources/decoded-original/0611-IdentXmlPart.xml` | `0d583915a261703954da22c176ba9f81338ad13ea2810e7cd5f7de8aa1bfa089` | `bad6b16fb32a32d47d882f48754994887457872b` | true |
| `all-in-one/sources/decoded-original/0612-IdentXmlPart.xml` | `95b545d4964d371ebfc107894ea90b8b1d0d7ab5d3a70e643f8ce539063c0f38` | `7cc782d33d07ef225c2104f3e7c9fbd31f7c7467` | true |
| `all-in-one/sources/decoded-original/0627-IdentXmlPart.xml` | `08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb` | `61ebc0abbb2ca160e11e1da400a3f14a397d8bc5` | true |
| `all-in-one/sources/decoded-original/0628-IdentXmlPart.xml` | `9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd` | `170ca5c72599edc7ea7eefe651c3680ce325e76a` | true |
| `all-in-one/sources/decoded-original/0629-IdentXmlPart.xml` | `67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972` | `058129bb01e27f7a6a0d0293f332d745e5bab74e` | true |
| `all-in-one/sources/decoded-original/0672-IdentXmlPart.xml` | `6bfc2ba142d6270c39eb1f13b2886204865af6d46eadc5f410c26981b8da9222` | `2f2790dab4bb2357733112220e0acc41edb6feb6` | true |
| `all-in-one/sources/decoded-original/0674-IdentXmlPart.xml` | `4770702f519bacda69202bb2f7733d983074bda90964360c238f990d9d08fd84` | `f210593944547b63eab10c667348711413600aab` | true |
| `all-in-one/sources/decoded-original/0676-IdentXmlPart.xml` | `c58427c5b0ac6c11cdb52e4c6d0461c7b191fae81ccace191048e9f175fcec59` | `1ed67265f69796a4e659f9438e551068037f33a4` | true |
| `all-in-one/sources/decoded-original/0678-IdentXmlPart.xml` | `51e637e0b9713c028810f2a717b5c3804a3a26c2f1be7e332a4d6bf277bfc382` | `7fafb2297bcdf739bf1d1dd68cebc0d74f2a40cc` | true |
| `all-in-one/sources/decoded-original/0680-IdentXmlPart.xml` | `fd551ad5d47bbd66c6bcdcc1949aaddf68cc086a3ddf6fb337adc767954c2b95` | `c9049ced1eaed72c5e251a88601d46ddec8c3e50` | true |
| `all-in-one/sources/decoded-original/0688-IdentXmlPart.xml` | `ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda` | `463585759f1ecd94f32362b4fefb000a152f5773` | true |
| `all-in-one/sources/decoded-original/0692-IdentXmlPart.xml` | `bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037` | `737785d03b5fad43c5b4d451955726d800edb1c0` | true |
| `all-in-one/sources/decoded-original/0694-IdentXmlPart.xml` | `757ccebdf32d0a168dd787bfa735fe6494eac4c4a9f7a5adc63898a88e8b152d` | `c45e8f3ca4129dc06734f6a12ef79e6ed6528a7d` | true |
| `all-in-one/sources/decoded-original/network-map.json` | `c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60` | `424430b6b953e43138e5d0a18ca40c949e21cfa1` | true |
| `all-in-one/sources/hmi_plc_tags.csv` | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` | `cf4c0650e7c7baac350dcb89909b808435704880` | true |
| `all-in-one/sources/live_index.json` | `14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1` | `e35ccea1f841349c632666c29954b7bcd4f5839e` | true |
| `all-in-one/sources/source-manifest.json` | `5af6e85994536897fd92f75972534a691e6eb0f067aafe07679c0788fd84e5bf` | `38cf407491d52dc6128cf94ca8a4bddee350de6d` | true |
| `docs/equipment-standard/INVENTORY.json` | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` | `587c3748ad9224718f95ba06463fee913dae231d` | true |
| `docs/equipment-standard/START-GPT61.md` | `35769e3146ccd707fea2b81b67b30376b76a0a19c7e662fe2bb4fdd382306f94` | `0d08cab3678df7e2625251b641b138ef4956483b` | true |
| `docs/equipment-standard/WORK-ITEM-TEMPLATE.md` | `4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586` | `e546f39535d2b589e80f97db869ac37ce4d05cfd` | true |
| `docs/equipment-standard/WORK-STANDARD.md` | `05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99` | `f76a570cc73098632e08759b17934000f7e3a253` | true |
