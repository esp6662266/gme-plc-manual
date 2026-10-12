# TC04 FN01 베어링 온도 — 고유 원본 조사 7영역 초안

## 핵심 확인·상충·누락

- TC04 고유 문서 조사: Int `%IW256:P` → 0481 선형화 → Int `Data.Temp_TC04` DB1.DBW116. HMI 원시 미러 Word DB13.DBW24와 다르다.
- 0529의 온도경보는 `Temp>공유설정 OR Temp>120 OR Temp<-60`, T76 `S5T#1M` 후 Set이다. TC05 가지에 있는 ServiceBit은 TC04 가지에 없다. 저온·환산고장도 이 이름의 경보에 들어갈 수 있다.
- FN01 0252의 공통 Prealarm/T130 `S5T#1H_30M`과 TC04 자체 1분 지연을 분리했다. BR01 시작요청 Reset은 이 FN01 장시간 지연을 거치지 않는 별도 소비다. 운전 가능시간·안전 여유시간으로 해석하지 않는다.
- 실제 렌더: OEM FG79/PDF80 및 FG104/PDF105 모두 Rev2 17.03.2025, 최초 DATA 27.05.2024. TC04 PT100 3선→X1:201/202/203→79KA1(도면 PHOENIX CONTACT 2864273)→PEW256/258 병렬 도면이다. PLC 고유 입력은 IW256이며 IW258은 색인상 reserved TC04다.
- 고유 상충: 시공 PDF33은 동일 8_22 케이블 CVV-S 2심, PDF58은 Type TC/KX 2S; OEM은 3선 PT100이다. PDF58의 예전 8_7 FLO4TB3A/TC04 행은 실제 렌더에서 검게 가려져 있으므로 텍스트 추출만으로 현행 경로로 채택하지 않았다.
- 현행 센서/변환기 설정·실제 채널·교정·정상 극성·보호값·CPU·현장복구는 미확정. 도면의 0Vac 9.9가 79KA1 GND2에 연결되는 표기는 원문 유지하며 임의로 DC0V로 고치지 않는다.
- 공유 재사용: TC03/BF01의 0291/0014 선형화, 기존 FN01의 공통 정지·BR01 관련 소유를 탐색 인덱스로 사용했다. TC04 고유 0481/0529/0398/0252/0253/0175 및 실제 도면은 독립 재대조했다. 같은 원본이어도 TC05 결과로 TC04를 완료 처리하지 않는다.

## 1. 설비·자료 기준

catalog_id TC04, sensor/계측, parent 없음, depth0, 별칭 tc_04. INVENTORY catalog[15], equipment[79], phase2/planned. 대장 역할 FN01 베어링 PT100 온도. FN01 본체·TC05 다른 베어링·변환기 79KA1을 각각 고유 소유로 구분한다. 이름이 같은 다른 TC 항목과 병합하지 않는다.

고정 읽기 전용 원본 `gme-research/source-mv06`, commit `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, v1.12.0. BATCH08-RESEARCH-INSTRUCTIONS와 TASK3-BATCH08-SCOPE 및 고유 중복 검토 범위를 따른다. 로컬 2차133 통합 제외를 유지한다. 사용자가 보고한 최신 게시판의 현재 기능을 이 고정 백업으로 검증했다고 주장하지 않는다.

AGENTS.md, 저장소 스킬/SOURCE MAP, WORK-STANDARD, WORK-ITEM-TEMPLATE, INVENTORY, START-GPT61, VERSION/WORKSPACE-HANDOFF/PUBLICATION_STATUS/ACTIVE-WORK/EXPANSION-WORK 상단을 읽었다. 최신 배치 허용 범위가 과거 통합·최대2 병렬 지시보다 우선한다. 원본 생성기/build/test를 실행하지 않았다. 모델 런타임/추론 수준 증명 미확인. 새 Work/Codex·재위임·사용자 Mac·로컬 TIA 접근 없음.

쓰기 범위는 이 MD와 `extracts/TC04/`뿐이다. 원본/공통 코드/대장/버전/게시·운영 기록/SEJIN 수정0. 시뮬레이터 작성·수정·생성·실행·행동시험0, 실제 PLC/현장/보호값 변경0.

이하 짧은 `0481` 표기는 `all-in-one/sources/decoded-original/0481-FlgNet.xml`, 선언 번호는 `NNNN-IdentXmlPart.xml`이며 원본 루트는 source-mv06이다. LAD 문서번호와 NID, 파일번호를 구분한다.

| 7영역 | 상태 | 확보/미확정 |
|---|---|---|
| 설비·자료 기준 | 적용 | 고유 ID/판본, 현행 실물 동일성 미확인 |
| I/O·HMI | 적용/일부 미확보 | 선언/주소/원시·환산 구분, 실제 화면 이벤트 미확인 |
| 제어 | 적용 | 호출 핀/선형화/사용처, 현재 실행 순서 미확인 |
| 전기 끝점 | 적용/일부 미확보 | OEM/시공 4페이지 렌더, 3선/2심 상충 |
| 알람·복구 | 적용/복구 미확보 | 1분 Set/Reset·관련 소유, 실제 복구 미수행 |
| 증상 관찰 | 적용 | 읽기 전용 관찰 설계, 운전시험 없음 |
| 완료·누락 | 적용 | 문서/정적/현장 상태 분리 |

## 2. I/O·HMI

SSD.AO/AOS.BO는 bit offset. DB 번호는 0674 DepDBBlock RID8→DB4, RID11→DB1, RID354→DB3; 0682 RID3/10/15→DB1/3/2, 0628 RID4→DB13의 TOD와 연결한다.

| 신호 | 형식·백업 주소 | 고유 원본 선언·연결 |
|---|---|---|
| TC04 직접 입력 | Int IW256:P | 0678 RID456 AO2048 SAD Input SAM=Peripherie, NID1 UID54;0481 W61 |
| TC04 미러 원시 | Int IW256 | 0627 RID156 AO2048 SAM=None, NID2 UID25;0398 W23 |
| Inputs.TC_04 | Word DB13.DBW24 | 0629 RID157 AO192 NID2 UID26 Write;0398 Move22 W24 |
| Coeff.ZERO_TC04 / COEFF_TC04 | Int DB4.DBW108/110 | 0676 RID10/9 AO864/880, NID1 UID56/55;0481 W63/W62 |
| Data.Temp_TC04 | Int DB1.DBW116 | 0676 RID12 AO928 NID1 UID57 Write;0684 RID43 NID3 UID490/492/494 Read |
| TC04_OFR | Bool DB3.DBX20.2 | 0676 RID355 AO162 NID1 UID23 Write;0481 W24 |
| TC04_TC05_MAX_ALL | Int DB1.DBW84 | 0684 RID44 AO672 NID3 UID491/501 Read, 두 TC 공유 설정 |
| MAX_TC04_TEMP | Bool DB3.DBX9.2 | 0684 RID48 AO74 NID3 UID499 Set Write/UID511 Read/UID512 Reset Write |
| Tag_104 | Timer T76 | 0686 RID47 SAD Timer AO76, UID497 Write/498 Read;HMI 태그 아님 |
| RESET_ALLARM | Bool DB2.DBX6.0 | 0684 RID24 AO48 NID3 UID510 Read |
| Prealarms_FN01 | Bool DB3.DBX17.0 | 0604 RID111 AO136 NID21 UID669 Write, 관련 FN01 소유 |
| Stop_Fan_FN01 | Local Bool BO2 | 0605 RID114 NID21 UID673 Write/NID22 UID694 Read;전역 DB나 접점 출력으로 변경 금지 |
| Tag_122 | Timer T130 | 0602 RID113 AO130 NID21 UID671 Write/672 Read;관련 FN01 공통 지연 |

HMI `sources/hmi_plc_tags.csv`: PLC Access의 I_TC_04 DB13,INT24(00065), data_DB1_DBW116 DB1,INT116(001F8), data_DB1_DBW84 DB1,INT84(00299), Coeff_DB4_DBW108 DB4,INT108(002DC), Coeff_DB4_DBW110 DB4,INT110(00282), Allarmi_75 DB3,X9.2(00142), Allarmi_200 DB3,X20.2(002B3)를 주소로 대조했다. 이 7행은 dde.cfg 설정 추출이며 실제 표시/색/경보문구/버튼 쓰기 이벤트/권한/현재값·통신 상태를 입증하지 않는다. 입력 미러 Word를 CSV가 INT로 읽는 것도 원문 구분이다.

보충 live_index `_7ev/1604`는 이름/값129개가 정렬되어 zero_tc04 index54=0, coeff_tc04 index55=250; `_7ev/1629` 이름/값162개에서 tc04_tc05_max_all index42=120, temp_tc04 index58=4다. 백업 저장값으로만 기록한다. 실제 보호설정이나 측정 온도가 아니다. `_7ev/1697` 알람 목록은 이름204/값203으로 미정렬이므로 위치로 TC04 현재/초기 Bool을 추출하지 않았다. `_7ev/896`는 reserved tc04 %IW258 Int, `/1512`는 tc04 %IW256 Int. 중복 도면 채널이 별도 센서라는 증거가 아니다.

## 3. 제어 구조·관련 소유

### 3.1 고유 환산 호출

0481 LAD1731 NID1: rail W67→Contact65, ON ORef52 W59→operand, 65.out W66→CRef46.en. ON ORef53 W60→46.IN0. TC04 UID54 W61→Analog_input, COEFF UID55 W62→Coeff, ZERO UID56 W63→Zero, OutValue W64→UID57, Out_of_range W24→UID23. CRef46 RID351/0680 BlockInterfaceInfo는 CodeBlock58 RID5/0672의 FC63 Signal linearization이다. 동일 UID는 다른 파일/NID 문맥에 옮겨 쓰지 않는다.

공통 0291/0014는 같은 고정 입력의 앞선 분석을 연결 재사용하고 TC04 계수 핀과 대조했다. 0291 IN0 Contact255→W256, Gt258(raw>-1382)→Le161(raw<=32767)→Convert164가 정상범위 가지다. Int→DInt 변환164/167/174, Add170/Mul177/Div181 및 ENO W227/230/234/237/241/245를 통과해 `(DInt(raw)+DInt(zero))*DInt(coeff)/28000`를 Move185로 Int OutValue에 전달한다. Real 계산·소수 온도 표시와 같은 것으로 취급하지 않는다. 정수 절삭/오버플로·ENO/호출 비활성의 최종 보존 동작은 현 CPU 미검증이다.

raw>32767 OR raw<=-1382는 OR47→Move193(-9999)→OutValue W253. **Move193.eno W21→Coil23→Out_of_range**이며 OFR를 단순 비교 출력으로 줄이지 않는다. Int 상한 초과 비교의 실제 도달 가능성은 별도다. 0014는 NOT IN0 Contact171→Move162(0)→OutValue W170. -9999/0은 코드 대체값이지 안전 대체값 권고가 아니다.

백업 ZERO0/COEFF250만으로 도면 범위 -30…250°C와 올바른 교정이 성립한다고 보지 않는다. 하한 오프셋 및 송신기 실제 4–20mA 설정, PLC AI raw 범위를 함께 확보해야 한다. FG104는 4–20mA를 명시하지만 FG79 79KA1 출력은 OUT U,I라 실제 DIP 설정을 알 수 없다.

`live_index _7ev/401`에는 startup special flag initialization `SET S ON; CLR S OFF` 텍스트가 있다. 0401-FlgNet(출력 미러)와 다른 객체다. 백업 초기화 텍스트는 현재 ON 상태의 증명이 아니다. 0549의 ON 조건 여러 호출 구조는 공통 호출 맥락일 뿐 전체 OB 실행순서·다른 writer 부재를 보증하지 않는다.

### 3.2 FN01 지연 경로

0252 LAD1950 NID21: ON662/Contact691 이후 MAX_TC04 UID663/Contact693.out W694→OR707.in1. TC05, ZT01, FN01 Run AND NOT VR01 Run, FN01 Run AND NOT VR02 Run과 합친다. OR707.out W683은 Coil653→Prealarms_FN01 UID669(W684), SdCoil656에 병렬 공급한다. W685=UID670 `S5T#1H_30M`, W686=Tag_122 UID671/T130. Timer 접점705.out W27→Coil661→W689 Local Stop_Fan_FN01 UID673.

0253 LAD1951 NID22: Stop_Fan_FN01 UID694 W705→Contact720→W721 OR676.in4; OR676.out W709→RCoil685→Flag.M_FN_01 UID697 W711. ON 이후 M_FN_01 Contact726→W727 Coil689→Start FN01 UID699 W714. 이는 FN01 요청/명령 처리이며 TC04가 모터 전력단자를 직접 소유한다는 뜻이 아니다. 최종 물리 드라이브·정지시간·현장 안전성은 이 문서에서 확인하지 않는다.

### 3.3 BR01 별도 소비

0175 LAD1858 NID5: MAX_TC04_TEMP 0585 RID36 UID240→W258 Contact287.operand;287.out W288→OR219.in3, OR219.out W267→ON Contact305→W306 OR213.in5, OR213.out W270→RCoil232→Flag.Start_Burner UID250 W272. 앞단 ON273도 유지한다. TC04 경보는 버너 시작요청 Reset의 충분한 OR 가지이며 FN01 T130 만료를 기다리는 식이 아니다. 외부 연소제어기의 점화·퍼지·화염안전 내부 순서/복구를 발명하지 않는다.

## 4. 전기 끝점·실제 PDF

| 실제 자료 | 페이지·직접 끝점·개정 |
|---|---|
| Electrical_Rev2.pdf FG79/PDF80 | 제목 PROBE PT100, PROBE FAN FN-01 SUPPORT BEARINGS. TC04 세 선→X1:201/202/203, 선79.1/79.2/79.3→79KA1 단자1/3/4. 프로브 실드 X1:204→79SCH1 접지. 도면 PHOENIX CONTACT 2864273. +24Vdc10.7→7+, 0Vac9.9→8-/GND2. 출력5+/OUT U,I→+PEW256(104/2),6-/GND1→-PEW256(104/3), 실드79SCH2→104/2. 범위 -30…250°C. footer FG79/TOT262, DATA27.05.2024, Rev2 17.03.2025 |
| 같은 OEM FG104/PDF105 | +PEW256→단자2 I0+ 및6 I1+ 병렬; -PEW256→단자4 U0-/I0- 및8 U1-/I1- 병렬. 79SCH2 실드. PEW256/258 두 채널 모두 TC04 -30…250°C/(4–20mA) 표기. CPU515 MOD2, MANA18은 -0Vdc10.6. footer ANALOG INPUT MODULE,FG104/TOT262,DATA27.05.2024,Rev2 17.03.2025 |
| Electrical_Can_Decoating_20241118.pdf PDF33 | CANDC-CONS-E016-033, FLOW B ROUTE CONDUIT PIPING(3), 행16 Pipe16, LOC FN01/TAG TC04, cable8_22 =FLB+FN01-TC04A, CVV-S1.0/2심. Rev1 24.11.11 first draft design;CHECKED/APPROVED 공란 |
| 같은 시공 PDF58 | CANDC-CONS-C008-058,CABLE SCHEDULE(7),행8_22 CR→FN01/TC04, TypeTC/KX2S1.0/spare0, route100→120RBD1→E1600,Adjustment18/LEN69. Rev1 24.11.11 first draft design;CHECKED/APPROVED 공란 |

위 네 페이지는 실제 렌더 이미지로 확인했다. FG+1 규칙을 일반화하지 않았다. PDF58 텍스트에 남은 8_7 =FLB+FN01-FLO4TB3A TC04는 렌더상 검정 처리된 구간이므로 유효 회로 근거가 아니다. 8_22의 CVV-S 대 KX, 2심 대 OEM3선 PT100을 미해결 상충으로 보존한다. 준공도·양끝 사진·케이블표 승인판·변환기 위치/명판/DIP·배선 점검 없이 어느 쪽이 현행인지 판단하지 않는다.

FG104 우측 TC05 범위 -30…350°C와 FG79의 -30…250°C 차이는 이 시트의 관련 TC05 경계다. TC04는 두 OEM시트에서 -30…250°C로 일치하며 TC05 상충을 TC04 상충으로 옮기지 않는다. 79KA1은 이 도면상 아날로그 변환기이며 릴레이 부하5/9·하단접점표1/5/9를 복제할 이유가 없다. 현행 정확한 제조사 모델·허용값은 명판/승인 자료 확보 전까지 도면 표기로만 남긴다.

## 5. 알람·복구

0529 LAD1981 NID3의 TC04 식과 지연:

1. ON489 W515→Contact557,557.out W558은 Gt438/Gt441/Lt444의 pre에 공급된다.
2. UID490 Temp W516 vs UID491 공유설정 W517, Gt438.out W518→OR437.in1.
3. UID492 Temp W519 vs UID493 상수120 W520, Gt441.out W521→OR437.in2.
4. UID494 Temp W522 vs UID495 상수-60 W523, Lt444.out W524→OR437.in3.
5. OR437.out W525→SdCoil450.in 및Contact559.in, UID496 S5T#1M W526→450.value, UID497 T76 W527→450.operand. T76 UID498 W528→559.operand,559.out W560→SCoil455, MAX_TC04 UID499 W530→455.operand.
6. Reset은 ON557→Contact563(RESET_ALLARM UID510,W548)→W564 Contact565(MAX_TC04 UID511,W549)→W566 RCoil484→MAX_TC04 UID512(W551). TC04 reset 가지에 온도 정상 비교·hysteresis를 추가하지 않는다. Set/Reset 동시 성립의 현재 실행 우선순위·재발/유지 동작은 CPU 확인 전 확정하지 않는다.

TC05는 같은 네트워크의 별도 T77/ServiceBit Contact22 후 Set476이다. TC04에는 이 서비스 조건이 없으며 TC05 분석을 이름 치환하지 않았다. TC04_OFR DB3.X20.2와 MAX_TC04_TEMP DB3.X9.2는 별개 Bool이다. 환산 -9999가 Temp<-60 가지에 들어갈 수 있는 구조이나 실제 단선반응·측정범위·현재 경보 여부는 별도 관찰 대상이다.

120/-60/1분/1시간30분은 고정 백업 코드 또는 값일 뿐 승인된 현행 보호값·안전 대기시간·리셋 권고가 아니다. Reset 요청, Bool 해제, 원인 제거, FN01/BR01 재요청과 실제 복구는 서로 다른 사건이다. 반복 리셋이나 강제기동 지시를 제공하지 않는다.

## 6. 증상별 관찰·수리 기록 설계

| 증상 | 읽기 전용 관찰·비교 | 원인 배제/남은 근거 |
|---|---|---|
| HMI값과 온도 불일치 | 같은 시각 IW256:P·IW256·DB13.W24·DB1.W116, 화면 태그 주소/단위 기록 | raw/환산 구분, 다른 취득시각·통신·계수/zero 비교;실제 쓰기 금지 |
| -9999/OFR 또는 MAX경보 | raw·IN0/ON·OFR·MAX·T76·세 비교 입력을 나란히 기록 | 범위이탈과 실제 과열 분리, 단선/변환기 전원/AI 채널은 자격자 승인 점검 |
| FN01 경보 후 정지 관련 | MAX_TC04/TC05/ZT01·VR01/02 Run·Prealarms_FN01·T130·Local Stop·M_FN01·Start 타임라인 | 다른 OR 원인 배제, 지연을 운전허용으로 취급하지 않음 |
| 버너 요청 해제 | MAX_TC04,0175 다른 OR 조건,Start_Burner 및 외부 상태를 같은 시각 대조 | FN01 장시간 지연과 버너 Reset 경로 분리, 외부 안전순서 미추정 |
| reset 후 남음/재발 | RESET_ALLARM/MAX/세 비교/T76/ON와 실제 메시지 변화 기록 | 코드 Reset와 실제 원인제거 구분,동시 Set/Reset·다른 writer 조사 필요 |
| TC04/TC05 혼동·측정편차 | 센서 위치/명판,X1:201–204,79KA1,PEW256/258 채널,시공8_22 사진·승인판 | 3선/2심·KX/CVV-S 상충부터 해결,TC05와 실물 동일성 단정 금지 |

각 기록은 관찰자·시각/시간대·위치·원시값/단위·수집장치·프로젝트/CPU 근거·비교 원본·원인 배제·승인된 조치·복구 증거를 분리한다. 미지 필드/note/repair_observation/기존 초안·타 설비 기록·저장키를 보존한다. 실제 운영 기록·사진·SEJIN 내용을 공개 Git에 복제하지 않는다. 이번에는 관찰값·정비·현장시험을 만들지 않았다.

## 7. 완료 기준·누락·검사

| 상태 | 판정 |
|---|---|
| documentation | complete_with_gaps: TC04 7영역 초안 및 고유 소유·상충·미확정 |
| static_review | 자체 XML 핀/선언·해시·PDF 렌더 검사;부모/독립 검토 별도 |
| ui_records | not_run: TC04 구현·저장/재열기/선택복원/보고서 검증 아님 |
| publication | not_published: 원본·버전·공통코드·배포 변경 없음 |
| tia_compile | not_performed |
| live_cpu | not_performed |
| field_recovery | not_performed |

네 기능: 도면·래더 비교는 이 문서에 근거 쌍을 제공하지만 앱 기능 검증 아님. 백업·선택복원/전후 기록비교/보고서·PDF는 적용 후보이며 TC04 고유 구현·저장/재읽기/미지 필드 보존/PC1280·모바일390/큰글자·링크·오류·PDF 레이아웃 검사를 수행하지 않았다. 원본 PDF 렌더 검토와 앱 보고서 PDF 검증을 구분한다.

남은 자료: 승인 준공 회로/케이블표·PT100 실제 결선·79KA1 명판/설정·AI 모듈 채널 및 range·교정 성적, 현재 ZERO/COEFF/공유설정·프로젝트/CPU 비교, 실제 HMI 화면/경보/Reset 이벤트·권한·통신, 원인제거/복구 결과. 새 자료 없이 실물 미확정을 반복 조사하지 않는다. 다음 단계는 부모의 고유 근거 검토이며 통합/배포나 현장 작업 허가가 아니다.

자체 검사·원본 SHA256+고정 Git blob 일치 결과는 아래와 extracts/TC04/static-review.json 및 source-hashes.json에 남긴다. 해시 개수는 의미검토 개수와 다르다. 아카이브·중지자산은 보존 검사만 했고 실행하거나 디코딩 재생성하지 않았다.

### 실제 작업 단계 시각 (UTC)

- 2026-10-11T11:14:28Z — task_received_scope_started
- 2026-10-11T11:15:05Z — initial_xml_extraction_and_oem_render
- 2026-10-11T11:16:00Z — four_pdf_renders_visually_reviewed
- 2026-10-11T11:20:51.869420+00:00 — seven_area_draft_written
- 2026-10-11T11:21:39.879221+00:00 — static_assertions_fixed_blob_hashes_verified

### 원본·중지 자산 해시 전체 목록

선택 원본·맥락·보존 65파일 SHA-256와 고정 Git blob 내용이 모두 일치했다. 중지5자산 freeze도 일치, 원본 Git 변경0. 이 수는 전체 의미검토 수가 아니다. 고유/공통 검토 FlgNet은 10개, 문서 구조/핀검사 15개 통과, PDF 실제 렌더4쪽이다.

| 원본 경로 | SHA-256 | 고정 Git blob OID |
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
| `all-in-one/registers/simulator-freeze.json` | `bb93c1994effc5609939ba566b7802ce7ed55154a7310f02379b308ac2c8c835` | `808ffac14dbd1b4a7d797fa6cd0d647635d90b47` |
| `all-in-one/registers/virtual-plc-test-results.json` | `a6b389f797f9a8b5ffe6928b8420f55c4cc459a327b0b48d716079d2eca6dd64` | `757dd50e45184568facb8ff62900b39d3ce848d1` |
| `all-in-one/sources/Electrical_Can_Decoating_20241118.pdf` | `3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd` | `0ee6b6f8361c5790864dbba4bbd9d55e8e7c08f8` |
| `all-in-one/sources/Electrical_Rev2.pdf` | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` | `f610fd7c7ce14ae951b00cff57b969259bfb389d` |
| `all-in-one/sources/GME_20250506.zap18` | `00c79b6d986e68298f65b172c1807115bc5d9e450a74fcc989d0796d8d8a4ea8` | `211c4f604627a32f82a1124c2a9872c2fcf00865` |
| `all-in-one/sources/PEData.plf` | `647de7ea123daced41c27bec8f81aeb93c712cac714d4754d7da5c528abb016a` | `65605ff8910f920109da731604aa5dc8d83fc956` |
| `all-in-one/sources/decoded-original/0014-FlgNet.xml` | `2e814adbaac6bab99bc668bfdab74f0fc90576324d0b88728951683869cfac30` | `4d164b074fcc13a8f97da9e24382cc169ef29555` |
| `all-in-one/sources/decoded-original/0175-FlgNet.xml` | `41279d6aaa157de3be963d010d6ca7dea94811a0ace519c8a3d8baa015f67f97` | `1626da00b3bbcb46f77720271ecf0f50db9dc63b` |
| `all-in-one/sources/decoded-original/0252-FlgNet.xml` | `66b8bf7c1e033f2e6710ab6959e1f5ec2cf27bd6e90c8780eb1bd6daebf76749` | `09de773eef5e5acc23c20f36e07ea6ddeca49c03` |
| `all-in-one/sources/decoded-original/0253-FlgNet.xml` | `2d35470eb44fff79916b93fcf57a597b2b9a03211e8493c2283706dc2c875154` | `6d5dc12df96c7fc47ad7f25eba6ba9a55a6755d0` |
| `all-in-one/sources/decoded-original/0291-FlgNet.xml` | `fe0b92f074eba25148ce34084649af3d968962558d652727f1eea19f3e3c2550` | `1418fb2ed172c6df694a5eb8bf2dffd0b177653b` |
| `all-in-one/sources/decoded-original/0398-FlgNet.xml` | `4f092b18df4e44af98fd44e173f48dad213a4e80b71f46b0a5e8a700f5b0a747` | `67ebb54daa55093487ea7e780f23ae2cf193c397` |
| `all-in-one/sources/decoded-original/0401-FlgNet.xml` | `60171c213e666de544077b7e4b497675813f7c0e75df85a3e76ab1def49b04ae` | `aadefbd35d305dd4a1146bf383b988a903802bf4` |
| `all-in-one/sources/decoded-original/0481-FlgNet.xml` | `190354dc7d59686f17368b7186bbc782a67ccef603f65a13f10e631446ee5d7d` | `5f275350dad39b1eeccb61f10072768deb938461` |
| `all-in-one/sources/decoded-original/0529-FlgNet.xml` | `1309f69deb365b1fd63a45080ee1fb250a8de6c4d753a0d2bdc67f29be1b8815` | `023b04880893284d76f14c2ef66fb81985c3642b` |
| `all-in-one/sources/decoded-original/0549-FlgNet.xml` | `49f7169c33ed7f54559b0801e21a7d618584900972840e91cf51ad032e8febb1` | `985b5310b43b1015b5dee286aa0e42800564b94b` |
| `all-in-one/sources/decoded-original/0582-IdentXmlPart.xml` | `41d4c2bd750392bbc2edc43995ec3a9da47a63c13ee86496df8f187492008951` | `82636dec064876d0f4cc714ef385b07d6e05efe0` |
| `all-in-one/sources/decoded-original/0584-IdentXmlPart.xml` | `3bff6c478e594bf97bb1730971944e96b0b5e2407199420fe6567d5fe609ea5d` | `0f8dde829be66041bea79e40ccc4586d84ff1da7` |
| `all-in-one/sources/decoded-original/0585-IdentXmlPart.xml` | `e36ec18aa4abebea8f9160254522bb51ff722eae804c5a469790f85f02939184` | `16574d37ef3ca61b59ba396c400e269ab1dd3440` |
| `all-in-one/sources/decoded-original/0599-IdentXmlPart.xml` | `32a693fe12134febbd9f5c7da10c3469ef4d5b164ab8b6bd9ea3867c358936c1` | `493de77fc827d8f14192ced05d82df3a062f7965` |
| `all-in-one/sources/decoded-original/0602-IdentXmlPart.xml` | `46ab21151eddaaf616469db520730c60423eb742aa491af194e6710c751b4caf` | `bcb12ab1ce8c476ff921baa1608f29d9822f76b4` |
| `all-in-one/sources/decoded-original/0603-IdentXmlPart.xml` | `e93969dfa281d75b49b24127793068e33472dadb19729c1c48fc4a8dad075ef8` | `3a92b304baf4dbf6147e944d9778d2da11285cb1` |
| `all-in-one/sources/decoded-original/0604-IdentXmlPart.xml` | `b798d29c5499b5314a1ee3cff9139dae64c887533b86baa43b6e9a052373a6af` | `bb2c318788b97e7a4924a176275c12d805aa519d` |
| `all-in-one/sources/decoded-original/0605-IdentXmlPart.xml` | `0ff6e2228dbfbc9f657359fe1055083ce621365084ea24c4160e4969b3eaac8b` | `30e199288c147aa22d5ce8407178a391b89c6b1b` |
| `all-in-one/sources/decoded-original/0606-IdentXmlPart.xml` | `73d45f9e2a34bba8a25df1ed1f71e8f6404fc96a8d6481672652a48435b6a740` | `ced032fa747a8544abf17058ee5ebaa78ba9b23b` |
| `all-in-one/sources/decoded-original/0611-IdentXmlPart.xml` | `0d583915a261703954da22c176ba9f81338ad13ea2810e7cd5f7de8aa1bfa089` | `bad6b16fb32a32d47d882f48754994887457872b` |
| `all-in-one/sources/decoded-original/0612-IdentXmlPart.xml` | `95b545d4964d371ebfc107894ea90b8b1d0d7ab5d3a70e643f8ce539063c0f38` | `7cc782d33d07ef225c2104f3e7c9fbd31f7c7467` |
| `all-in-one/sources/decoded-original/0627-IdentXmlPart.xml` | `08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb` | `61ebc0abbb2ca160e11e1da400a3f14a397d8bc5` |
| `all-in-one/sources/decoded-original/0628-IdentXmlPart.xml` | `9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd` | `170ca5c72599edc7ea7eefe651c3680ce325e76a` |
| `all-in-one/sources/decoded-original/0629-IdentXmlPart.xml` | `67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972` | `058129bb01e27f7a6a0d0293f332d745e5bab74e` |
| `all-in-one/sources/decoded-original/0632-IdentXmlPart.xml` | `fd162c603476c2cac899010cee7a8ee382b6092c115135e3ac1007ae71c544e9` | `600935fa8d394c0d247ea20040d5dfff4f05b500` |
| `all-in-one/sources/decoded-original/0633-IdentXmlPart.xml` | `9e00aa275fa1b4e488b73983b309c6b73dcf4f3dd9be5dec13e9975d68f3c0fc` | `a1ab5ee12addbc92d04c9950d4437e2b564d6b5c` |
| `all-in-one/sources/decoded-original/0672-IdentXmlPart.xml` | `6bfc2ba142d6270c39eb1f13b2886204865af6d46eadc5f410c26981b8da9222` | `2f2790dab4bb2357733112220e0acc41edb6feb6` |
| `all-in-one/sources/decoded-original/0674-IdentXmlPart.xml` | `4770702f519bacda69202bb2f7733d983074bda90964360c238f990d9d08fd84` | `f210593944547b63eab10c667348711413600aab` |
| `all-in-one/sources/decoded-original/0676-IdentXmlPart.xml` | `c58427c5b0ac6c11cdb52e4c6d0461c7b191fae81ccace191048e9f175fcec59` | `1ed67265f69796a4e659f9438e551068037f33a4` |
| `all-in-one/sources/decoded-original/0678-IdentXmlPart.xml` | `51e637e0b9713c028810f2a717b5c3804a3a26c2f1be7e332a4d6bf277bfc382` | `7fafb2297bcdf739bf1d1dd68cebc0d74f2a40cc` |
| `all-in-one/sources/decoded-original/0680-IdentXmlPart.xml` | `fd551ad5d47bbd66c6bcdcc1949aaddf68cc086a3ddf6fb337adc767954c2b95` | `c9049ced1eaed72c5e251a88601d46ddec8c3e50` |
| `all-in-one/sources/decoded-original/0682-IdentXmlPart.xml` | `25c7aeb1bfa29c178eaa396db33d4eb6d2d29b9a3f2eb965fa61fae8ce7f1092` | `61182411e912941161eccf4e90c1f174e5379f0a` |
| `all-in-one/sources/decoded-original/0683-IdentXmlPart.xml` | `0c9b569d041cd5babbbeded8a3bdc5d3754927125756b6ac54b7cb991b22fc22` | `662acdb9a06c0ba1c0027e7dd215a28f07d3f02b` |
| `all-in-one/sources/decoded-original/0684-IdentXmlPart.xml` | `6e9b3f173184adcddca503e81e2649022734b6ea3639c1d5ddaf0a08bac00208` | `d67b98b5d5516e0330aae5cfdbee41a3e09206e1` |
| `all-in-one/sources/decoded-original/0686-IdentXmlPart.xml` | `b450d8ff22f0fffd7a214b2a696af28a03a27834ebf862bfaa822dc9bfb3c8d4` | `8c152d926692a8e15973c980e08e338d29411814` |
| `all-in-one/sources/decoded-original/0688-IdentXmlPart.xml` | `ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda` | `463585759f1ecd94f32362b4fefb000a152f5773` |
| `all-in-one/sources/decoded-original/0692-IdentXmlPart.xml` | `bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037` | `737785d03b5fad43c5b4d451955726d800edb1c0` |
| `all-in-one/sources/decoded-original/0694-IdentXmlPart.xml` | `757ccebdf32d0a168dd787bfa735fe6494eac4c4a9f7a5adc63898a88e8b152d` | `c45e8f3ca4129dc06734f6a12ef79e6ed6528a7d` |
| `all-in-one/sources/decoded-original/network-map.json` | `c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60` | `424430b6b953e43138e5d0a18ca40c949e21cfa1` |
| `all-in-one/sources/hmi_plc_tags.csv` | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` | `cf4c0650e7c7baac350dcb89909b808435704880` |
| `all-in-one/sources/live_index.json` | `14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1` | `e35ccea1f841349c632666c29954b7bcd4f5839e` |
| `all-in-one/sources/source-manifest.json` | `5af6e85994536897fd92f75972534a691e6eb0f067aafe07679c0788fd84e5bf` | `38cf407491d52dc6128cf94ca8a4bddee350de6d` |
| `docs/equipment-standard/INVENTORY.json` | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` | `587c3748ad9224718f95ba06463fee913dae231d` |
| `docs/equipment-standard/START-GPT61.md` | `35769e3146ccd707fea2b81b67b30376b76a0a19c7e662fe2bb4fdd382306f94` | `0d08cab3678df7e2625251b641b138ef4956483b` |
| `docs/equipment-standard/WORK-ITEM-TEMPLATE.md` | `4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586` | `e546f39535d2b589e80f97db869ac37ce4d05cfd` |
| `docs/equipment-standard/WORK-STANDARD.md` | `05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99` | `f76a570cc73098632e08759b17934000f7e3a253` |
