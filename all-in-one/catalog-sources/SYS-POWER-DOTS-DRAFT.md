# SYS-POWER 주전원·보조전원·제어반 — 고정 원본 7영역 조사 초안

문서 범위 complete_with_gaps. 현행 보호설정, 현재 CPU, 실물 설치, 현장 복구 또는 BC01 동등 구현·게시 완료를 뜻하지 않는다.

## 핵심 확인·상충·누락·공유 근거

- 표지 FG1/PDF1은 440Vac/60Hz/463kW/782A/보조24Vdc다. FG6/7/8 실제 렌더의 상단은 440V, 하단 회로 제목은 400V이며 FG7 램프 설명도 400V다. 문서 내부 차이를 보존하며 400을 OCR 오류로 지우거나 현장 전압을 확정하지 않는다.
- 110Vac는 FG9의 9T1 440/110V, 24Vdc는 FG10의 고객 UPS 3상 공급→10GD1 경로다. 직접출력10.8/비상조건 출력10.9/입력10.7/CPU10.10을 구분한다.
- FG11 냉각은 11TM1→11KA1→11EV1~5의 전기 경로다. 이 팬들을 별도 PLC 출력이나 CH01 냉각기와 동일시하지 않는다.
- FG84 서비스 84KA1~4는 각 부하접점5–9, 코일 A1/A2, Q6.0~6.3과 외부 명령 단자 쌍을 구별한다. 특히 Start CH01(%Q3.1)과 Enable start chiller(%Q6.0)는 같은 출력이 아니다. 서비스 예시의 10초는 후자 허가 경로의 원본 타이머 값이며 현장 조작 대기시간이 아니다.
- 공통 근거: [CR01 초안](CR01-DOTS-DRAFT.md)의 FG9/10/16·E19.5→IW18→Inputs→110V_Fault 경로를 연결 재사용했다. 이번에는 해당 PDF와 0397 Word 분기·0457 S/R·선언을 독립 재대조했다. CR01/QG/JB01 실물 동일성은 그대로 미확정이다. CR01의 FG17 조작버튼 및 0635 추가쓰기 후보는 재연구 없이 기존 범위와 미확정을 참조한다.
- 누락: 승인 최신 회로, 실물 보호기기·UPS·팬·반 명판/배선, 정상극성·보호정정, 현행 호출순서/모든 Writer, HMI 이벤트, CH/LIW/BWF 외부 장치의 내부 인터록·응답·복구. SYS-POWER 한 ID만 작성하며 연결된 장치까지 함께 완료로 세지 않는다.

## 1. 설비·자료 기준

- catalog_id SYS-POWER, kind software, 공통 시스템, parent_id null, phase2. INVENTORY catalog42(0-based), equipment index236. 별칭 presence 110v / presence voltage. 소프트웨어·전원 경계 묶음이며 독립 실물 한 대라는 뜻이 아니다.
- 고정 읽기 전용 `gme-research/source-mv06`, commit `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, v1.12.0. 이후 사용자가 보고한 최신 게시·로컬 기능을 이 백업으로 검증하지 않는다. 로컬2차133 통합 제외 유지.
- root AGENTS, 스킬, WORK-STANDARD, WORK-ITEM-TEMPLATE, INVENTORY, 배치12 지시·범위·중복 검토 해당 행, 버전·최신 인계 최상단을 읽었다. 이번 사용자 승인 조사 범위가 과거 구현·생성 지시보다 우선한다. 모델/추론 런타임 증명 미확인.
- 원본 회로 `all-in-one/sources/Electrical_Rev2.pdf`의 실제 렌더 열람은 PDF1,7,8,9,10,11,12,17,85,136,143의 11쪽. 대응 FG1,6,7,8,9,10,11,16,84,135,142. 각 footer 기본 일자27.05.2024, 해당 페이지 개정란 공란을 확인했다. 파일명 Rev2가 모든 페이지 개정란에 Rev2가 있다는 뜻은 아니다.
- 실제 PDF6은 목록 페이지이며 텍스트 추출·렌더 파일 생성만 했고 회로 의미검토로 세지 않는다. 범위 JSON의6/7/8/9/10/11/16/84는 electrical_fgs이며 실제 PDF 번호와 구별했다. 전체262 FG/전체 PDF를 읽었다고 주장하지 않는다.

## 2. I/O·HMI

### 2.1 공통 전압 상태의 입력·내부·표시 구분

원본 XML 경로는 모두 `all-in-one/sources/decoded-original/` 아래다.

| 구분 | 원본 선언·주소·형식 | 해석·경계 |
|---|---|---|
| 도면 전압 상태 | FG16/PDF17 9QF2 보조접점→E19.5, FG135/PDF136 CPU515 MOD12 단자36 | 보조접점의 상태 입력. 실제110V 정밀계측/정상극성 증거 아님 |
| 원시 Word | 0627 SimpleAccess RID25/NID1/UID81, Tag_276, Word, AO144, SAD Input SAM=None | %IW18 프로세스 이미지. 직접 PIW 접근 아님 |
| 내부 Word 쓰기 | 0629 GlobalAccess RID26/NID1/UID82 AK=Write, Word AO144 BAD4;0628 Inputs RID4 TOD13 | DB13.DBW18에 Word 쓰기. I19.5 범위 포함 |
| 처리 Bool | 0657 GlobalAccess RID248/NID50/UID24, Inputs.Presenza_110V AO157 BAD247;0655 Inputs TOD13 | DB13.DBX19.5 읽기. Word 복사와 Bool 코일 쓰기를 혼동하지 않음 |
| 전압고장 기억 | 0657 GlobalAccess RID252/NID50/UID39 read,40/48 write AO92 BAD10;0655 Allarm TOD3 | DB3.DBX11.4, Allarm.110V_Fault |
| 공통 Reset 요청 | 0657 GlobalAccess RID13/NID50/UID38 AO48 BAD12;0655 Flag TOD2 | DB2.DBX6.0, Flag.RESET_ALLARM. 요청과 복구 별개 |
| HMI 설정 대응 | hmi_plc_tags.csv: Allarmi_93,"DB3,X11.4",PLC,00130 | 백업 DDE 주소 대응. 이름 Allarmi_110은 DB3.X13.5로 다른 비트다. 실제 화면 이벤트/알람문구/ACK·Reset 쓰기 미결속 |

위 핵심은 Global 또는 SimpleAccess S=Global이다. Local 임시값·물리 입력·HMI 태그를 한 종류로 합치지 않는다. CR01에 기록된 0635의 동일 입력 주소 추가쓰기 후보는 보존하며 현행 실행 증거로 채택하지 않는다. 해당 중지 영역은 이번에 실행·시험·수정하지 않았다.

### 2.2 서비스 출력의 선언 독립 대조

0602 SimpleAccess 전부 Bool / SAD Output / SAM=None / S=Global이다.

| 원문 이름 | RID / NID / UID | AO→주소 | FG84와의 관계 |
|---|---|---|---|
| Start CH01 |124 /24 /749 Write|25→%Q3.1|84KA1 직접출력으로 연결 금지 |
| Enable start chiller |127 /24 /753 Write|48→%Q6.0|FG142 A6.0 단자21→84KA1 A1 |
| START LIW FEEDER |198 /43 /1222 Write,1223 read,1229 Write|49→%Q6.1|단자22→84KA2 A1; S/R 복수쓰기 선언 존재 |
| Consent Start BWF01 |26 /3 /125 Write|50→%Q6.2|단자23→84KA3 A1 |
| Consent Start BWF02 |32 /4 /163 Write|51→%Q6.3|단자24→84KA4 A1 |

같은 주소 48을 가진 0632의 Tag_283은 Word Output이므로 %QW6 읽기 문맥이다. 같은 숫자 AO만으로 Bool Writer로 바꾸지 않는다. 0555의 Enable start chiller RID49 UID118 AK=Monitor는 감시 참조이며 쓰기 아님. UID753도 0255/NID24/RID127 문맥 안에서만 연결한다. LIW/BWF 전체 요청·운전·고장 로직은 해당 설비 소유로 남기며 이 문서는 선언과 전기 끝점까지만 확정한다.

## 3. 제어 구조

### 3.1 공통 Word 전달

0397-FlgNet.xml, 색인 LAD1070/NID1, P78 Move Cardinality1 DisableENO=true. W21 Powerrail→P78.en, W88 ORef81/RID25→P78.in, W90 P78.out1→ORef82/RID26. 따라서 IW18→DB13.DBW18의 Word 복사 분기를 직접 확인했다. W89 P78.eno→P79.en 연결도 있으나 DisableENO·ENO 존재와 실행 결과는 별개다. 이 분기에는 CRef 호출이 없다. 현행 호출순서·다른쓰기를 이 분기 하나로 완결하지 않는다.

### 3.2 CH 서비스 릴레이 대표 고유 경로

0255-FlgNet.xml, 색인 LAD1953 motors1 index24, NID24. CH01 상세 전체를 SYS-POWER 소유로 가져오지 않고 서비스 출력 분기를 독립 확인한다.

- W775 rail→P767 Contact, W754 ORef745/RID1→operand. 0602 ON AO0 Memory = M0.0.
- W21 P767.out→P23.in, W22 ORef24/RID264→P23.operand. 0602 ServiceBit AO8000 Memory = M1000.0. 이름 ON을 상수 TRUE로, ServiceBit을 현장 안전허가로 추정하지 않는다.
- W768 P23.out은 P769와 P771로 분기. P769는 W755 ORef746/RID122 Allarm.CH_01_FAULT, W770→P729 RCoil, W757 ORef747/RID123 Flag.M_CH_01. 0604 AO12/BAD5·BAD2 및0603 DB3·DB2 선언으로 각 DB3.DBX1.4와DB2.DBX1.4 구별.
- P771 operand W758 ORef748/RID123, W772→P736 Coil·P739 SdCoil·P773 Contact. W759 ORef749/RID124는 P736.operand→Start CH01 Q3.1.
- W760 ORef750/RID125→P739.value, 0606 LiteralConstant S5Time SV=S5T_x0023_10S V4352. W761 ORef751/RID126→P739.operand는 Tag_123 Timer SAD Timer AO113(%T113).
- W762 ORef752/RID126→P773.operand;W774 P773.out→P744 Coil.in;W764 ORef753/RID127→P744.operand가 Enable start chiller Q6.0이다.

따라서 원본에서 Start CH01과 지연된 Enable start chiller가 별도 출력을 가진다. 해당 네트워크는 일반 Coil과 Reset Coil 및 SD 타이머를 포함하며 ENO/수치 환산/CRef 호출은 없다. 서비스 출력 활성화가 외부 chiller의 실제 가동·냉각 완료를 증명하지 않는다. 리셋과 동일 스캔 분기의 최종값·타 블록 쓰기·외부회로 상태는 미확정이다. 10초를 현재 CPU 설정이나 조작·복구 절차로 제시하지 않는다.

### 3.3 반 냉각 및 안전회로의 소유

FG11은 전기상 11TM1의5(L)/7(N)/3→11KA1 코일과 팬 전원 접점이다. 11TM1 내부 알고리즘·설정온도·PLC 신호는 이 회로에서 확보되지 않았다. FG6 누전/트립 장치 및 FG8/9/10의14KA·15KA 접점은 하드웨어 전원 경계이며 PLC 소프트웨어 논리와 동등한 안전증명으로 취급하지 않는다. FG13~15 전체 안전모듈 회로는 이번 직접 의미검토 범위 밖이다.

## 4. 전기 전달 경로

아래 전압·전류·기기 표기는 모두 원본 도면 기재다. 보호 설정 변경값, 현재 설치 정격, 적합성 판정, 활선 작업 지침이 아니다. 모든 행의 원본은 Electrical_Rev2.pdf, footer27.05.2024/개정란공란이다.

| FG / 실제PDF | 양 끝점·중간 경로 | 소유·미확정 |
|---|---|---|
|1 /1|NOMINAL VOLTAGE440Vac,60Hz,463kW,782A,AUXILIARY24Vdc|표지 설계값; 현행 측정/설정 아님 |
|6 /7|6.1L1/L2/L3→6QF1→6WB2 flexible bar→6WB3→6TO1 관통→6.2L1/L2/L3(7/0). 6WB1 접지바 별도|6QF1 400–1000A,bar1250A/원문 3//240mmq; 실제설정 미확인 |
|6 /7|6TO1:1/2/3/4→차폐쌍선→6D1 DOSSENA DER3/2IMCC:1/2/3/4;전원23(+24V10.7)/24(0V10.6),TRIP7/8/9,ALARM10/11/12 표시. X20:2000/2001/2002 및6SB1~3,X1:356/357·360/361·364/365 트립 관련선|PV05/06 비상질소 박스 명칭은 관련경계. 외부 보호기 문구 Id0.5–1A TypeB by customer를 승인 현행 설정·적합성으로 전환 금지. 트립 조작/복구 절차 제시 안 함 |
|7 /8|6.2L1/2/3→7FU1→7HL1 삼상 표시→7FC1;별도7FU2→7D1 V1/V2/V3,7TA1~3→I1/I2/I3/COM. +24V10.7→7FU3→7D1 A2(+),A1(-)→0V10.6|7TA1~3 원문1000/5A;전압표시와 전력계 분리. EXP10 12 통신 단자 그림은 있으나 실제 통신 연결·주소 미확인 |
|8 /9|6.2L1/2/3→8QF1→15KA1→15KA2→8WB1→8.3L1/2/3(22/0) DIRECT MOTORS AND SOFTSTARTER|15KA 코일·안전조건 전체는 범위 밖 |
|8 /9|6.2L2/L3 분기→8QF2→8T1 440/230V535W→14KA9·14KA10의 양극 접점→X1:419/420,230V60Hz CONTROL BOARD BURNER TYPE BP N300|버너 제어반 공급이며 버너 내부 점화/안전순서 아님 |
|9 /10|6.2L1/L2(8/9)→9QF1→9T1 440/110V3600VA→9QF2→110Vac9.8/0Vac9.9;14KA4·14KA8 직렬경로→110Vac9.7(21/0)|직접110V와 비상조건분기 구분. 원문9QF2 32A는 현행설정 아님 |
|9 /10|9QF3→X1:413/110Vac9.10 VALVES;9QF4→414/9.11 FAN+PLC;415/0Vac9.9 (JB1).9QF5→416/9.12;9QF6→417/9.13;418/0Vac9.9 (JB2)|JB1/JB2 전원공급 연결, CR01=JB1/JB2 근거 아님 |
|10 /11|UPS CLIENT 3상440V60Hz XL:1/2/3→10QF1→10GD1 AC/DC20A→10QF2→+24V10.7 INPUTS PLC;음극→0V10.6|고객UPS 경계 별도. 원문10QF1 2.2–3.2A 및 RATING2.5A는 문서표기 |
|10 /11|10QF3→+24V10.8 DIRECT OUTPUTS;14KA3·14KA7→+24V10.9 OUTPUTS UNDER EMERGENCY;10QF4→+24V10.10 CPU|네 전원분기를 합치지 않음. 비상전원이라는 문구를 UPS 지속공급으로 오독하지 않음 |
|11 /12|110Vac9.8→11QF1→11TM1:5(L);7(N)→0Vac9.9;3→11KA1:A1,A2→0Vac9.9|전기 제어경로;11TM1 제조사·설정 미확보 |
|11 /12|110Vac9.8→11QF2→11KA1접점1–2→X20:2016→11EV1~5 병렬→X20:2017→0Vac9.9|이 접점은1–2. FG84의5–9를 다른릴레이에 일괄복제 금지. 팬모터 자체 단자1/2 |
|16 /17|110Vac9.8→X20:2010→16HL1(WHITE)X1/X2→X20:2011→0Vac9.9. +24V10.10→X20:2012→16HL2→0V10.6|110V 표시와 CPU24V 표시 분리; 실제CPU 정상동작 증명 아님 |
|16 /17→135 /136|+24V10.7→9QF2 보조접점→E19.5(135/5)→CPU515 MOD12 단자36|도면CPU 표기이지 현재CPU 식별 결과 아님 |
|142 /143→84 /85|+24V10.9→X21:3034(4A F)→MOD15 전원;A6.0/6.1/6.2/6.3 단자21/22/23/24→84KA1/2/3/4 A1,A2→0V10.6|비상조건출력 전원 소유. 후단외부전압과코일전압을혼동하지 않음 |
|84 /85|CHILLER X1:232→84KA1접점5–9→233;LIW X1:234→84KA2 5–9→235;BWF01 X1:236→84KA3 5–9→237;BWF02 X1:238→84KA4 5–9→239|부하선84.1~84.8,ORANGE FS17 1.5mmq. 외부 입력의 전압/전원원천은 이쪽 그림에 명시 안 됨. 하단1/5/9 접점표와실제5/9 부하경로 구분 |

FG142의 A6.7 표기에 관한 다른 회로까지 일반화하지 않는다. 이번 핵심은 단자21~24이고, 나머지모듈 채널·전체출력 안전회로의 완전성 검토를 주장하지 않는다. 시공도 전체·제조사 매뉴얼·실물 사진은 이번 신규 직접 검토에 포함하지 않았다.

## 5. 알람·복구

0457-FlgNet.xml, LAD1823 allarms1 index43, NID50, title presence110v:

- W21 rail→P23/P35. P23 Contact의 operand Negated, W22 ORef24/RID248→P23.operand. W41 P23.out→P27 SCoil.in, W47 ORef48/RID252→P27.operand. NOT Inputs.Presenza_110V가110V_Fault Set 분기다.
- P35 Contact W42 ORef38/RID13(RESET_ALLARM);W43 P35.out→P36.in;W44 ORef39/RID252(Fault)→P36.operand;W45 P36.out→P37 RCoil.in;W46 ORef40/RID252→P37.operand.
- 이 네트워크에 타이머·CRef 호출은 없다. 단순 Fault=NOT Presence가 아니라 Set/Reset 기억구조다. Reset 분기에 Presence 복귀 확인 접점이 있다고 만들지 않는다. 동시 S/R·호출·다른 Writer의 스캔 최종우선 미검증.

HMI Allarmi_93은 주소 연결까지만 확인했다. 공통 ACK/Reset 전체 경로, 공정 정지 영향, 외부릴레이 동작·실제 전원복귀는 별도 증거가 필요하다. CR01의 공통 FG17 버튼 경로는 공유참조이며 이번에 독립 렌더한 페이지 수에 포함하지 않는다. 110V고장과 주전원 전체상실/CPU24V상실/팬고장/CH고장을 동일 알람으로 만들지 않는다. 차단기 재투입, 보호설정 조정, 인터록 우회, 전원 활선측정, 자동재기동은 지시하지 않는다.

## 6. 증상별 관찰·원인 분리

현장수리 미수행. 아래는 승인된 담당자가 제공할 기존 관찰·점검기록의 항목이며 직접 조작 순서가 아니다. 시각/시간대·관찰자·프로젝트판본·명판·기록위치·값/단위·비교원본·조치·복구확인을 구분한다.

| 증상 | 비교할 문서·기존 관찰 | 단정하지 않을 사항 |
|---|---|---|
|주전원 표시/계기만 이상|FG7 7HL1 회로와7D1 별도퓨즈/전류변성기·보조전원 기록|표시 하나로삼상전체·계기고장·보호설정오류 단정 금지 |
|110V 표시와 알람 불일치|16HL1,9QF2 접점/E19.5,IW18,DB13.DBX19.5,DB3.DBX11.4의동일시각 기록|표시등·상태접점·Word복사·기억알람은각각다름 |
|CPU 표시는 있고 출력기기 반응 없음|16HL2/10.10,출력10.8/10.9 및FG142 전원기록|CPU전원으로출력10.9/외부반전원을증명불가 |
|제어반 팬 미동작|11TM1 식별·11KA1 상태·11EV1~5 개별기록·11QF1/2 경로와대조|설정온도·PLC명령·CH01고장으로즉시단정불가 |
|Chiller 원격명령 불일치|Q3.1 vsQ6.0,0255 P739 T113,84KA1/X1:232–233 및외부응답기록|두출력을합치거나명령만으로실제가동판정금지 |
|전압400/440 표기가 다름|표지/FG6~8 상하제목·승인 최신도면·명판·전원공급자료|현재전압/정정설정값으로선택하지 않음 |

## 7. 완료·누락·검증

| 영역 | 이번 상태 |
|---|---|
|설비·자료기준|고정한 SYS-POWER ID·문서판본·소유경계 적용 |
|IO/HMI|공통110V Word/Bool/HMI 주소와서비스4출력 선언 확인;화면이벤트 미확보 |
|제어|0397 분기·0457 S/R·0255 서비스 대표분기 직접확인;LIW/BWF 전체논리·전체호출 미검토 |
|전기끝점|필요FG8개+표지·입출력끝점2개 실제렌더확인;실물·현행승인 미확보 |
|알람/복구|110V 기억식 원본확인;실제복구 미수행 |
|증상관찰|기록항목만정의;현장값·보호판정·정비조치 없음 |
|완료/누락|documentation complete_with_gaps;static self_review 문서범위;부모독립검토 대기 |

- 네 기능: 도면·래더 비교 근거만 준비. 백업/선택복원·전후기록비교·보고서/PDF 구현·UI저장/재읽기/재열기 검증은 not_run. 원본 PDF 렌더를 제품 보고서 기능 시험과 혼동하지 않는다.
- publication not_published(이번초안), tia_compile/live_cpu/field_recovery not_performed. 원본 build/test/generator 실행0, 시뮬레이터 작성·수정·생성·실행·행동시험0, PLC/현장/보호값/SEJIN 변경0. 새 Work/Codex·로컬TIA·사용자Mac 접근·재위임0.
- 추가자료: 최신 승인전기도면/개정대장, UPS·전원·반·팬·보호기 명판과 전기전문가의 기존점검기록, 현행PLC I/O/호출/Writer교차참조, HMI 화면·이벤트, 서비스 외부설비 회로/응답. 이 자료 없이 실물 보류를 반복검색하지 않는다.
- 검색/파싱/해시 수량은 의미검토 수량과 다르다. 직접핵심 논리3 XML(0397선별분기,0457전체,0255전체)과 각선언·HMI한주소·회로11페이지를 의미검토했다. 선언파일 나머지 본문·색인검색 일치전체·원본전체를 검증했다고 주장하지 않는다.

### 실제 작업 시각 UTC

- 2026-10-11 11:56:23 착수, 배치 지시·범위 읽기.
- 11:56:27~11:56:41 표준·기존 CR01 공통근거·고정 버전/원본 상태 확인.
- 11:56:49 PDF 텍스트/렌더 생성;11:56:57 필요11쪽 중 첫10쪽 열람·400/440차이와 냉각·서비스접점 확인.
- 11:57:14~11:57:46 XML/HMI·서비스출력 선언·0255/0457 핀 및FG142 실제 렌더 추가대조.
- 11:57:59 공통Word·타이머/DB선언대조;11:58:33 선정34파일 SHA256/고정blob전부일치·중지5보존 확인.
- 초안 작성후 자체검사 완료시각과결과는 extracts/SYS-POWER/self-check.json에 기록한다. 예상시간을 실제시간으로 기재하지 않는다.

### 전체 선정 원본 SHA256 / 고정 Git blob 목록

아래34파일은 이번 선정 전부이며 모두 내용 일치다. 표준/인계는 범위확인, 원본문서/선언은 위 선별 의미검토, 중지5는 해시전용이다. 고정입력 전수 의미검토34를 뜻하지 않는다. 원본 Git clean 확인과 중지5 기준해시 일치는 검사JSON에 보존했다.

| 원본 상대경로 | SHA256 | 고정 Git blob | 일치 |
|---|---|---|---|
| `.agents/skills/gme-equipment-rollout/SKILL.md` | `fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b` | `9aa820ea6ca15b4e136c9772423b78ed4df6a3d4` | True |
| `AGENTS.md` | `0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2` | `073164bc6efd5791032d62c71b03b4dab48cb6f8` | True |
| `EXPANSION-WORK.md` | `ec624de9fd2fcfac861a67fd5e828b25ef46db50bfd7a37ff16e2cb54cd0f7e2` | `4c42d88ecc2d48269eb23e13a20ebf3721a092a1` | True |
| `PUBLICATION_STATUS.md` | `efe4857aec598d90470322cf3962eb3fe1f64947630e1fdf71d1c90134de8740` | `d76401cf291fc0be681acc51fa898ad3ce46ff78` | True |
| `VERSION.json` | `5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7` | `fffb51663b7705aec91cb119ca80ee943a4ce758` | True |
| `WORKSPACE-HANDOFF.md` | `215096d997782e78e901dfae36c782937e49611fbeb677a0d3fa50cbecf8d074` | `dd0b8989d2376c4415bba9bd826fe6754c6b1a12` | True |
| `all-in-one/ACTIVE-WORK.md` | `eff3bbc08ecff41da3beff77f3fec48e7d148708192bcaaab00f34b6a721afc2` | `6eb947c629b5ddf9c759ef87649451303938864b` | True |
| `all-in-one/assets/program-model-data.js` | `52f8199371e3399b7c0d44ab5469f0472aced79d56bbef2887f7625f5d2aff0f` | `38f34b0caa380a16ccad6f6f1e234a2fdf23f327` | True |
| `all-in-one/assets/simulator-workspace.js` | `3a6dfc618ff7e7b238f2671dc85d65704f33093a18eac879d86081d92c31e8bc` | `97c2c831c77a9699fff0e0960b3bc1b7d93d45b3` | True |
| `all-in-one/assets/virtual-plc.js` | `5f1876052dc0067b1f010af0dfc941946e37003167481731293615d9c1c36dbc` | `0bd9eceb54365a91214a37c5601b5067c39a3f75` | True |
| `all-in-one/registers/program-model.json` | `6203479c086b15bada12ac9d7e37db9280234ec26f1ea6091d7211dc09a577c5` | `9860b10f008d3a5ae714be50d77b703dfec32f3a` | True |
| `all-in-one/registers/simulator-freeze.json` | `bb93c1994effc5609939ba566b7802ce7ed55154a7310f02379b308ac2c8c835` | `808ffac14dbd1b4a7d797fa6cd0d647635d90b47` | True |
| `all-in-one/registers/virtual-plc-test-results.json` | `a6b389f797f9a8b5ffe6928b8420f55c4cc459a327b0b48d716079d2eca6dd64` | `757dd50e45184568facb8ff62900b39d3ce848d1` | True |
| `all-in-one/sources/Electrical_Rev2.pdf` | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` | `f610fd7c7ce14ae951b00cff57b969259bfb389d` | True |
| `all-in-one/sources/decoded-original/0255-FlgNet.xml` | `ea2200a136d7b4e8b498107e8a53c5fa192e501beb039fbd17d1fb35e0277ada` | `df34ee6126786ed6e62c1f5b800f93679bd4c393` | True |
| `all-in-one/sources/decoded-original/0397-FlgNet.xml` | `bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834` | `4ab8370493c4e28fc1eabeeebe2743d27f0c4021` | True |
| `all-in-one/sources/decoded-original/0457-FlgNet.xml` | `498e0618c56b6a898373d4fa4745e749d0654da17b1f1cd148e9d9617dccb86d` | `dcba3137465522e263742251b0e00159b2be090d` | True |
| `all-in-one/sources/decoded-original/0555-IdentXmlPart.xml` | `46c36333e249dd775c1db94a1f6e80a36cf1a5a9c998b7d0980ae01d862901e6` | `9a915a8b9a260b48402df151c1fe0bbcb2f4ea1c` | True |
| `all-in-one/sources/decoded-original/0602-IdentXmlPart.xml` | `46ab21151eddaaf616469db520730c60423eb742aa491af194e6710c751b4caf` | `bcb12ab1ce8c476ff921baa1608f29d9822f76b4` | True |
| `all-in-one/sources/decoded-original/0603-IdentXmlPart.xml` | `e93969dfa281d75b49b24127793068e33472dadb19729c1c48fc4a8dad075ef8` | `3a92b304baf4dbf6147e944d9778d2da11285cb1` | True |
| `all-in-one/sources/decoded-original/0604-IdentXmlPart.xml` | `b798d29c5499b5314a1ee3cff9139dae64c887533b86baa43b6e9a052373a6af` | `bb2c318788b97e7a4924a176275c12d805aa519d` | True |
| `all-in-one/sources/decoded-original/0606-IdentXmlPart.xml` | `73d45f9e2a34bba8a25df1ed1f71e8f6404fc96a8d6481672652a48435b6a740` | `ced032fa747a8544abf17058ee5ebaa78ba9b23b` | True |
| `all-in-one/sources/decoded-original/0627-IdentXmlPart.xml` | `08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb` | `61ebc0abbb2ca160e11e1da400a3f14a397d8bc5` | True |
| `all-in-one/sources/decoded-original/0628-IdentXmlPart.xml` | `9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd` | `170ca5c72599edc7ea7eefe651c3680ce325e76a` | True |
| `all-in-one/sources/decoded-original/0629-IdentXmlPart.xml` | `67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972` | `058129bb01e27f7a6a0d0293f332d745e5bab74e` | True |
| `all-in-one/sources/decoded-original/0632-IdentXmlPart.xml` | `fd162c603476c2cac899010cee7a8ee382b6092c115135e3ac1007ae71c544e9` | `600935fa8d394c0d247ea20040d5dfff4f05b500` | True |
| `all-in-one/sources/decoded-original/0655-IdentXmlPart.xml` | `38e9f323024fba19582b473f39b1ed03ffe6a0b390218894029a6edb0b1ff9fb` | `83b60b9de4541a3ffa6ee0db98205a372b525665` | True |
| `all-in-one/sources/decoded-original/0657-IdentXmlPart.xml` | `0f70cda60a6b1a17175876d58e25b2686952642de6cffb21213aeef8b347a22b` | `e625f3d8999c7be7d88c50eab0d93107117b58ec` | True |
| `all-in-one/sources/decoded-original/network-map.json` | `c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60` | `424430b6b953e43138e5d0a18ca40c949e21cfa1` | True |
| `all-in-one/sources/hmi-windows.csv` | `15f8d69b5c43d4fdbe550f9cd2717f855fea877ed8146973054cb6dbcaa9892e` | `8401dcfe5ba3e7e244eea0f501bb84a2e387da39` | True |
| `all-in-one/sources/hmi_plc_tags.csv` | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` | `cf4c0650e7c7baac350dcb89909b808435704880` | True |
| `docs/equipment-standard/INVENTORY.json` | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` | `587c3748ad9224718f95ba06463fee913dae231d` | True |
| `docs/equipment-standard/WORK-ITEM-TEMPLATE.md` | `4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586` | `e546f39535d2b589e80f97db869ac37ce4d05cfd` | True |
| `docs/equipment-standard/WORK-STANDARD.md` | `05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99` | `f76a570cc73098632e08759b17934000f7e3a253` | True |