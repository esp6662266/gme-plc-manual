# PSH03 압력 채널 원본 조사 초안

## 핵심 인계 요약

- **확인:** PSH03의 직접 환산 입력은 `IW320:P`(Peripherie), 결과는 `Data.PSH03 DB1.DBW24`, 범위 비트는 `Allarm.PSH03_OFR DB3.DBX22.2`다. HMI 입력 미러 `Inputs.PSH_03 DB13.DBW52`는 별도 `IW320` process-image 읽기를 복사한 **Word**다. 같은 주소 번호라도 환산값·직접 주변장치 값·HMI 미러를 합치지 않는다.
- **확인:** MV03 비교 제어는 SETPOINT−PSH03의 Local Int 오차에서 `>=5`와 `<-5`를 사용한다. SD T139의 S5T#4S와 SD T138의 S5T#10S, NOT T139 허가를 보존한다. 물리적인 압력 단위나 밸브 실제 동작시간으로 환산하지 않는다.
- **상충:** OEM FG75 오른쪽 기기는 PSH-03/PEW320인데 상단 제목은 PRESSURE CONTROL PSH-02다. 중앙 PSH-02/PEW286에는 OUTPUT MV-03이라고 되어 있다. FG108은 PSH-03/PEW320, PLC0497은 PSH03:P/IW320이다. 이름으로 두 센서를 병합하거나 배선을 수정하지 않는다.
- **상충/다른 쓰기:** 0344 비교의 M14.4/M14.5 외에 0479 CONT_S에도 같은 주소 출력 선언이 있다. OFF 접점과 “not used” 제목은 현재 실행 불가의 증명이 아니다.
- **누락:** 현재 계기·압력 취출점·교정, 온라인 CPU/호출순서, HMI 이벤트·권한·실제 단위/표시, 계수·제로·설정의 현재값, OFR의 실제 소리·차단·복구는 미확인이다. 이번 문서로 현장 안전 설정을 제시하지 않는다.
- **공유 근거:** 기존 MV03 초안은 압력 제어·다른 쓰기·호출·도면 탐색용 인덱스로 활용했다. BF01/BF02의 공통 선형화·Word 알람 구조와 보존 방식도 연결 재사용한다. PSH03의 0497/0398/0344, 선언 주소·OFR, OEM75/108, 시공56의 6_11은 이번 고정 원본에서 독립 대조했다. 타 PSH 태그·값·접점을 치환하지 않았다.

## 작업 기준·범위

- GME-STD-1.0.0, PSH03 sensor/계측, parent 없음, depth0, 별칭 psh_03. INVENTORY catalog[6], equipment[92], phase2 planned. 같은 이름의 PSH01/02와 별도 ID이며 실물 동일성 미확인이다.
- 작업3 자체조사 Batch05의 PSH03 한 개. `progress/TASK3-BATCH05-SCOPE.json`, `GME-CATALOG-OVERLAP-REVIEW.json` 해당 행 확인. PSH01/02·MV03·HE01·AB01의 완료 실적을 만들지 않는다. 로컬 2차133 통합 제외 유지.
- 고정 저장소 `source-mv06`, 커밋 `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, v1.12.0. 현재 main/온라인 CPU와 동일하다는 뜻이 아니다.
- AGENTS, 저장소 rollout 스킬, WORK-STANDARD, WORK-ITEM-TEMPLATE, INVENTORY 및 최신 인계/버전/게시/작업 머리말을 읽었다. 최신 Batch05 지시가 이 작업의 산출물·금지 범위를 우선한다. 실제 모델/추론 수준 런타임 증명은 미확인이다.
- 허용 쓰기는 `drafts/PSH03-DOTS-DRAFT.md`, `extracts/PSH03/`뿐. 원본·공통 코드·대장·버전·배포·운영 기록 변경0. 시뮬레이터 작성·수정·생성·실행·행동시험0. PLC·현장·보호값·SEJIN 변경0. 원본 build/test/generator/preflight 실행0; 자체 XML 파싱·해시 대조·PDF 렌더만 수행했다.
- 실제 시각 UTC: 착수/지시 읽기 2026-10-11 10:29:03, 핵심 XML·선언 추출 10:29:58, OEM/시공 실제 렌더 확인 10:30:03~10:30:10, 명명 선언·주소중첩 대조 10:30:24~10:31:34, 호출 경계 확인 10:32:14. 종료 시각은 검사 JSON에 기록한다. 추정 소요시간을 만들지 않는다.

본문 XML 경로 약칭은 `all-in-one/sources/decoded-original/NNNN-FlgNet.xml` 및 명시한 `NNNN-IdentXmlPart.xml`. LAD=document_id, NID=선언의 원본 네트워크 번호로 구분한다. 탐색색인 resolved_operands만으로 선언을 확정하지 않고 RID+NID+UID, SSD/AOS/TD, BAD→DepDBBlock TOD를 대조했다.

## 7영역 적용표

| 영역 | 상태 | 확보 범위 | 남은 범위 |
|---|---|---|---|
| 설비·자료 기준 | 적용 | 고유 ID, P&ID/시공/PLC 소유 분리 | 현재 실물·명판·취출점 |
| I/O·HMI | 적용/일부 미확보 | 2종 IW320 읽기, DB1/3/4/13, HMI6주소 | 화면 이벤트·현재값·단위·권한 |
| 제어 | 적용 | 환산·오차·타이머·출력요청·다른 쓰기·호출 | 현재 실행·최종값·간접쓰기 |
| 전기 끝점 | 적용 | X1 178/179/180→MOD4 2/4/18, 시공6_11 | 현행 준공·코어 식별·교정 |
| 알람·복구 | 적용/일부 미확보 | OFR 발생·ENO·일반 Coil·HMI주소 | 실제 경적/차단·복귀·재기동 |
| 증상 관찰 | 적용 | 원시/환산/미러/명령 구분 관찰안 | 실제 작업·수리·운전 확인 |
| 완료·누락 | 적용 | 문서와 제품/현장 상태 분리 | 독립 검토·제품통합·UI·게시 |

## 1. 설비·공정·자료 경계

P&ID `sources/PID_1684n002I.pdf` 실제 p1에서 PSH-03은 AB01 출구측 RO01/RO02와 MV03 overflow 가지 부근에 표기된다. 확대의 원문은 **Setpoint = +0.1 mbar**다. 이 도면의 과거 운전 표기를 DB1.DBW40 현재값이나 안전 권고값으로 변환하지 않는다. 도번1684n002, 원작성06/04/2011, 판I 15/01/2013이다. 개정 G 02/05/2012 행에 PSH-03 추가 표기가 있다. 도면 렌더 `render/PID-full.png`, `PID-PSH03.png`, `PID-title.png`를 확인했다.

시공 p56 6_11은 CR→HE-01 PSH-03으로 구역을 기입한다. P&ID의 AB01 출구·MV03 연결, 시공의 HE01 구역, PLC의 MV03 소비자는 서로 다른 종류의 관계다. 이를 catalog parent 변경·소유 확정·실물 중복 정리로 쓰지 않는다. PSH 명칭만으로 이산 압력스위치라 단정하지 않는다. 이 원본 경로는 아날로그 Int 입력과 4–20mA 회로다.

## 2. I/O·선언·HMI

### 2.1 직접 선언표

| 대상 | 원본 선언·NID/UID | 형식·주소 | 해석/미확정 |
|---|---|---|---|
| PSH03 직접 읽기 | 0678 RID106 NID17 UID484; SSD AO2560, SAD Input/Peripherie | Global Int IW320:P | 0497 환산 입력. 현재 모듈/CPU 증명 아님 |
| PSH03 HMI 읽기 | 0627 RID88 NID2 UID104; AO2560 SAD Input/SAM=None | Global Int IW320 | 0398 process-image 읽기. :P와 동시성 보장 아님 |
| Inputs.PSH_03 | 0629 RID89 NID2 UID105 Write, AO416 BAD4→0628 Inputs TOD13 | Global Word DB13.DBW52 | HMI raw 미러. Data.PSH03가 아님 |
| Data.PSH03 | 0676 RID109 NID17 UID487 Write AO192 BAD11→0674 Data TOD1; 0619 RID30 NID3 UID288 Read BAD28→0618 TOD1 | Global Int DB1.DBW24 | 환산 결과/오차 입력 |
| Coeff.Zero_PSH03 | 0676 RID448 NID17 UID486 AO1744 BAD8→0674 TOD4 | Global Int DB4.DBW108 | 읽기 선언. 실제값·설정 근거 미확인 |
| Coeff.Coeff_PSH03 | 0676 RID449 NID17 UID485 AO1760 BAD8→0674 TOD4 | Global Int DB4.DBW110 | 읽기 선언. 단위 스케일을 이름으로 추정하지 않음 |
| Allarm.PSH03_OFR | 0676 RID389 NID17 UID23 Write AO178 BAD354→0674 Allarm TOD3 | Global Bool DB3.DBX22.2 | 선형화 Out_of_range 수신 |
| Data.PSH03_SETPOINT | 0619 RID29 NID3 UID287 AO320 BAD28→0618 Data TOD1 | Global Int DB1.DBW40 | 오차 기준. 명명 선언에서 PLC Write 미발견≠쓰기 불가능 |
| ErrPSH03 | 0062 RID31 NID3 UID289 Write,297/300 Read; Local/BO144 | Local Int | 전역 DB 주소를 만들지 않음 |
| Tag_147 / Tag_148 | 0617 RID32/34 NID3; AO138/139, SAD Timer | Timer T138/T139 | S5Time 리터럴과 타이머 객체를 구분 |
| PID UP / down MV03 | 0617 RID39/37, AO116/117 NID3 UID302/299 Write | Global Bool M14.4/M14.5 | 물리 출력 아님. 0670 RID106/107 NID12 UID544/545도 Write |

선언명 검색·named global 주소범위 검색 결과는 `exact-declarations.json`, `address-overlap-review.json`에 남겼다. 이 검색은 모든 간접 주소·포인터·외부/HMI 쓰기를 증명하는 완전한 writer 분석이 아니다. 원시 Int와 목적 Word, bit OFR 쓰기를 구분했다.

### 2.2 HMI 주소와 실제 이벤트 경계

`sources/hmi_plc_tags.csv`의 설정 연결:

| 태그 | 주소 | 설정 ID |
|---|---|---|
| I_PSH_03 | DB13,INT52 | 00056 |
| data_DB1_DBW24 | DB1,INT24 | 0022C |
| data_DB1_DBW40 | DB1,INT40 | 0029B |
| Coeff_DB4_DBW108 | DB4,INT108 | 002DC |
| Coeff_DB4_DBW110 | DB4,INT110 | 00282 |
| Allarmi_216 | DB3,X22.2 | 0029E |

0398 LAD1071 NID2: ORef104/RID88→Wire115→Move98.in; Move98.out1→Wire117→ORef105/RID89. Move98 DisableENO=true, 입력선과 출력선을 그대로 확인했다. `Inputs.PSH_03`의 XML Word와 HMI INT 선언은 동일 비트를 다르게 해석할 가능성을 남긴다. 실제 음수 표시·스케일·소수점·권한·편집 이벤트·알람 문구·발생/해제 기록은 이 CSV로 확정할 수 없다. 특히 I_PSH_03를 압력 환산값으로 표시하지 않는다.

## 3. 고유 제어와 공통 함수

### 3.1 PSH03 환산 호출

0497 LAD1747 NID17, ON Contact495(operand Wire489/ORef482 RID1)→Wire496→CRef476.en. CRef476 RID351 내부 CodeBlock488 RID5는 0672 Signal linearization FC63 NID17 UID488 Call과 결속된다.

| 핀 | Wire·ORef·RID | 선언/해석 |
|---|---|---|
| IN0 | W490/O483/RID1 | ON, en과 별도의 함수 입력 |
| Analog_input | W491/O484/RID106 | PSH03:P IW320 |
| Coeff | W492/O485/RID449 | DB4.W110 |
| Zero | W493/O486/RID448 | DB4.W108 |
| OutValue | W494/O487/RID109 | DB1.W24 Write |
| Out_of_range | W24/O23/RID389 | DB3.X22.2 Write |

Call ENO 미연결을 실제 함수 성공·실패 처리로 채워 넣지 않는다. ON은 전역 심볼이며 이름만으로 고정 True를 증명하지 않는다.

### 3.2 공통 선형화: 연결 재사용 + PSH03 적용 독립 확인

기존 BF01/MV03에서 조사된 0291 LAD1658 NID1,0014 LAD1659 NID2를 같은 고정 원본에서 핀·형식 재대조했다. 0611의 Local Bool IN0 RID1, Int Analog_input RID3/Zero RID8/Coeff RID13/OutValue RID19, DInt App3 RID11/App4 RID14/App5 RID6/App6 RID9, Bool Out_of_range RID26을 구분한다.

- 정상 연산 허가: IN0 Contact255→W256→Gt258(Analog_input > -1382)→W25→Le161(<=32767)→W26→Convert164.
- Convert164 Int→DInt(입력), Convert167 Int→DInt(Zero), Add170 DInt, Convert174 Int→DInt(Coeff), Mul177 DInt, Div181 DInt(분모 28000), Move185→Int OutValue. 각 ENO 사슬 W227/230/234/237/241/245가 다음 en으로 이어진다. 요약식 `(raw + Zero) × Coeff / 28000`은 이 정수 연산과 저장 폭·ENO 조건을 생략한 설명일 뿐 부동소수점 실측 환산 보장이 아니다.
- 범위밖: Gt190 `>32767` 또는 Le259 `<=-1382`→OR47→W49 Move193.en; -9999 ORef218→W252→Move193.in; W253→OutValue219. **Move193.eno→W21→일반 Coil23.in**, W22/ORef24 Local Out_of_range. 단순 무조건 비교 결과와 동일시하지 않는다.
- 0014: NOT IN0 Contact171→W172 Move162.en; ORef166 0→W169 in; W170→ORef167 OutValue. 입력 허가가 없으면 0을 쓰는 별도 네트워크다. 이 네트워크에 OFR 전용 R 코일은 없다.
- 선언 Int의 상한과 `>32767` 원문 비교를 그대로 보존한다. 외부 아날로그의 실제 공학범위·단선 진단 전체를 이 비교만으로 규정하지 않는다. 오버플로/정수 절삭·CPU 동작시험은 수행하지 않았다.

### 3.3 MV03 압력 오차 소비

0344 LAD1705 NID3: ON Contact328(W303/ORef286)→W329 분기. Sub256.in1 W304/O287 RID29=DB1.W40, in2 W305/O288 RID30=DB1.W24, out W306/O289 RID31=Local ErrPSH03.

- NOT Tag147 Contact330 W308/O291→W331 SdCoil263. value W307/O290 0620 RID33 S5T#4S; operand W310/O292 Tag148=T139.
- Tag148 Contact332 W312/O294→W333 SdCoil268. value W311/O293 0620 RID35 S5T#10S; operand W314/O295 Tag147=T138.
- NOT Tag148 Contact334 W315/O296→W335→Ge276.pre/Lt282.pre.
- Ge276 in1 W316/O297 ErrPSH03, in2 W317/O298 RID185 Int5; out W318→Coil279; operand W320/O299→M14.5.
- Lt282 in1 W321/O300 ErrPSH03, in2 W322/O301 RID186 Int-5; out W323→Coil285; operand W325/O302→M14.4.

따라서 자동 압력요청은 ON과 NOT T139 아래 `error >=5`/`error <-5`인 **비대칭 경계**다. ±5 모두 같은 폐구간이라고 바꾸지 않는다. T139/T138을 단순 “4초 열고 10초 쉼”으로 번역하지 않는다. ON·타이머 실행 및 호출 관찰 없이 실제 주기를 보장할 수 없다.

0345 LAD1706 NID4에서 M14.4/M14.5는 자동 허가와 함께 소비된다. 열림 Auto507→UP509(W456/O420), 닫힘 Auto525→Down527(W472/O430). 수동·세정·버너 기동·교정·리미트·고장 경로도 있다. OR543→NOT ResetEncoderProcedure44→NOT InputsOpen523→Coil390(Start open MV03); OR544→NOT washing539→OR53(교정 경로 합류)→NOT InputsClose541→Coil407(Start close MV03). 이는 PSH03가 밸브 물리출력의 유일 결정자가 아니라는 경계 확인이며 MV03 전체 별도 매뉴얼 완료가 아니다. 전체 MV03 동력/리미트/버너 경로는 기존 MV03 초안의 별도 근거를 참조한다.

### 3.4 다른 쓰기·호출 순서의 한계

0479 LAD15 NID12는 `control pc02 moduling mv03 - not used` 제목이나 실제 OFF Contact583(W547/O529)→W584→LRef507 CONT_S.en이 있다. QLMNUP W577/O544, QLMNDN W578/O545가 0670 RID106/107의 M14.4/M14.5 Write다. 이를 PSH03 함수나 같은 센서로 병합하지 않는다. 지역 Real_PC02/Real_SPPC02의 현재 상류·DB25·OFF 값·현재 활성은 보류한다.

Main 0031 LAD1619 NID6: ON282→W283→CRef261.en; CodeBlock273 RID55는 0688 Analog input conversion FC3. 0032 LAD1621 NID8: ON352→W353→CRef341.en; CodeBlock347 RID85는 Valve Control loop FC14. 0030 LAD1613 NID19의 recipes/HMI/output ENO 사슬 W32/33/42→NOT Simulation(1) Contact37(W44/O45)→W43→CRef28 HMI Inputs FC15(CodeBlock29 RID135). 0688/0692/0694의 선언으로 결속했다. 실제 스캔·현재 호출표·CPU 비교를 수행하지 않았으며 이 원문 관찰은 금지된 시뮬레이터 실행이 아니다.

## 4. 전기 양 끝점·실제 렌더·개정

### 4.1 OEM FG75/PDF76

`sources/Electrical_Rev2.pdf` 실제 p76 footer: FG75, 기본일27.05.2024, IEC, 총262 표기. 별도 Rev2 행은 이 페이지에서 관찰되지 않는다. 오른쪽 PSH-03 가지:

`+24Vdc 10.7 → X1:178 (5×20, 50mA F) → wire75.3 → PSH03 +; PSH03 − → X1:179 → +PEW320 참조108/2; X1:180 → 75SCH3 실드 참조108/2`.

기기 원문 P-BADR, OUTPUT4–20mA, 0/10mbar는 도면 설계값이다. 현행 모델·퓨즈 설치·보호 설정·교정값이 아니다. 상단 PSH-02 제목과 하단 PSH-03의 상충을 보존한다. 옆 PSH02의 OUTPUT MV03/PEW286 가지를 PSH03에 복사하지 않았다.

### 4.2 OEM FG108/PDF109

실제 p109 footer: FG108, 기본일27.05.2024, **개정2 17.03.2025**. PSH03 압력 입력(4–20mA), CPU515/MOD4 표기:

- FG75/7 +PEW320 → MOD4 PEW320 채널 **단자2 I0+**.
- 단자4 U0−/I0−는 -0Vdc10.6 공통과 연결, 단자18 MANA도 같은 귀로.
- 75SCH3는 케이블 실드로 표시. 실드를 신호 마이너스나 임의 접지 단자로 대체하지 않는다.

이는 원본 도면 CPU 표기이며 현재 CPU 모델을 확정하지 않는다. PDF76과109는 이번 직접 렌더 결과로 지정했으며 FG+1 규칙을 전체 도면에 일반화하지 않는다. 이 PSH03 AI 경로에 릴레이 부하접점은 보이지 않으므로 타 설비5/9나 접점표1/5/9를 가져오지 않는다.

### 4.3 시공 PDF56 실제 6_11 행

`sources/Electrical_Can_Decoating_20241118.pdf` p56의 **6_11**, cable `=FLA+HE01-PSH03A`, FROM CR→TO HE-01 PSH-03, Current AI, CVV-S 4S 1.0, spare1, route 100 LBD1→LBD1→E900, adjustment8, LEN48을 직접 확인했다. 단위가 불명확한 LEN을 현재 실측 길이로 바꾸지 않는다.

footer CANDC-CONS-C006-056, D-PAGE6, total56/64, revision1 24.11.11 first draft design. DESIGNED J.W.Lee, CHECKED J.H.Kim, APPROVED 공란이다. 시공 완료/승인 준공도로 간주하지 않는다. p56의 일부 윗행은 실제 렌더에서 검게 가려져 있어 텍스트 추출로 보이는 그 내용을 실물 검증으로 사용하지 않았다. 대상6_11은 가림 아래에 실제 보인다. 이 표는 코어 색상·현장 단자 연결 자체의 확증이 아니다.

## 5. 알람·영향·복구

- PSH03 고유 확인 알람은 DB3.X22.2 OFR 한 비트다. 0497 CRef476.Out_of_range→W24/O23, 0676 RID389에서 Write. 내부는 0291의 범위밖 Move193 ENO→일반 Coil23이며 S/R 래치·지연 타이머가 아니다. 임의로 “압력고고 트립”을 만들지 않는다.
- HMI Allarmi_216=DB3,X22.2 설정이 존재한다. CSV만으로 문구·우선순위·음향·Ack·팝업·현장 차단·실제 복귀는 확인할 수 없다.
- 기존 BF01의 공통 Word알람 조사(0148 startup 및 관련 알람 Word0~16 경로)는 같은 고정 원본의 공유 근거다. PSH03 OFR byte22는 그 Word 범위 밖이므로 그 구조를 PSH03 전용 경적 경로로 복제하지 않는다. 다른 알림경로가 전혀 없다는 주장도 하지 않는다.
- 0344 오차 가지에 PSH03_OFR 차단 접점은 관찰되지 않았다. 따라서 -9999 대체값이 Data.PSH03에 쓰일 때 오차 비교의 입력이 달라질 수 있다는 정적 주의점은 있지만, 실제 밸브 방향·최종 출력·안전성을 예측하지 않는다. 현재 계수·SETPOINT·정수 연산·다른 쓰기·모드·호출 확인이 먼저다.
- 정상 범위 복귀가 입력/환산 오류 비트에 미치는 것과 운전 재기동 허가를 구분한다. 실제 복구는 원인 제거·정상 계측/환산/표시·명령과 실제 응답·알람 해제 기록을 같은 시각으로 확보해야 한다. 보호값 변경·강제출력·우회는 수행하지 않았다.

## 6. 증상별 관찰·배제 순서

아래는 실행 기록이 아닌 읽기 전용 관찰 설계다. 전기/압력 현장 작업은 승인된 담당자의 안전절차·격리·계측 권한에 따른다. 온라인 접속이나 시험을 이번에 승인받은 것으로 해석하지 않는다.

| 증상 | 관찰 위치·값 | 원본 비교·원인 구분 | 필요 복구 근거 |
|---|---|---|---|
| HMI 압력값과 제어가 다름 | 시각을 맞춘 IW320:P/IW320/DB13.W52/DB1.W24, 계수·Zero, HMI태그·단위 | 0398 raw Word 미러 vs0497 Int 환산, process image/:P 차이 | 현재 HMI화면·이벤트·스케일과 온라인 동일시각 기록 |
| OFR 또는 -9999 | DB3.X22.2/DB1.W24/raw 및 IN0/ON | 0291 strict >-1382/<=32767, ENO→Coil, 실제 mA/계기 진단은 별도 | 현장 계기·배선·전원·교정 원인 제거와 정상 복귀 증거 |
| 환산이 0에 멈춤 | 함수 호출·ON/IN0, raw·계수·Zero·DB1.W24 | NOT IN0의0쓰기, 계수/입력, 호출 누락을 분리 | 값0과 미수집 빈칸 구분; 호출·환산 재관찰 |
| MV03 자동 방향/주기 의문 | DB1.W40−W24, Local ErrPSH03, T138/139, M14.4/14.5·Auto | 0344 >=5/<-5 및 NOT T139,0479 중복Writer,0345 다른요청 | 요청/최종출력/위치응답·현재순서 확인; 주기시험 미실행 |
| 계기 태그/위치 혼동 | X1:178/179/180 표찰, PEW320 채널,6_11 케이블,명판·취출점 | FG75 PSH-02제목 vs PSH03본문,FG108 PSH03,시공HE01/P&ID AB01 출구 | 최신 준공 개정·현재프로젝트·위치사진의 일치 |
| OFR 표시되나 소리/정지 불명 | Allarmi_216 실제이벤트·시간·경적·상위정지 | 주소설정≠알림/정지 논리,Word0~16 범위밖 | 현재HMI알람설정·소리/차단경로·복귀이력 |

기록 필드: 관찰자, UTC 또는 현장 시간대 포함 시각, 위치/기기/CPU·프로젝트 버전, 읽은 정확한 DB/주소/형식/값/단위, 원본 비교점, 배제 결과, 승인된 조치, 전후 재관찰, 별도 재기동 허가. 운영기록·사진을 공개 소스에 복제하지 않는다.

## 7. 완료·누락·다음 작업

| 상태 축 | 이번 결과 |
|---|---|
| documentation | complete_with_gaps 초안, PSH03 한 개 |
| static_review | 직접 XML·선언·도면·해시 자체검토, 독립 검토 대기 |
| ui_records | not_run; 제품 통합·실제저장/재열기/복원 미수행 |
| publication | not_published; 사용자 전달은 부모가 별도 수행 |
| tia_compile | not_performed |
| live_cpu | not_performed |
| field_recovery | not_performed |

네 기능(도면/래더 나란히 보기, 백업/선택복원, 전후비교, 보고서/PDF)은 적용 요구가 있으나 이번은 MD초안과 원본증거다. 기능 구현·UI검증·기록보존 시험 통과로 표시하지 않는다. 원본90개 등의 해시 수량은 의미검토 수량이 아니다. 7개 핵심/경계 네트워크0497·0291·0014·0344·0345·0479·0398의 지정 범위와 호출0030/31/32를 읽었으며0398은 PSH03 Move98,0345는 압력소비/다른허가 경계,0479는 중복쓰기 경계 검토다. 모든 채널의 의미검토 완료가 아니다.

추가 확보가 필요한 자료:
1. PSH03 명판·압력 취출점·교정 성적·최신 승인 준공도 및 X1/모듈/케이블 코어 대응.
2. 현재 CPU 프로젝트의 FC3/14/15 호출·직접/간접/HMI쓰기·DB1/4 현행값과 저장 시점. 새 자료 없이 같은 실물 보류를 반복 조사하지 않는다.
3. HMI 원본 화면/이벤트·단위/스케일·쓰기권한·Allarmi_216 알림/Ack/해제 설정. DB3.X22.2와 이름 유사 타DB 비트를 혼합하지 않는다.
4. 원인 제거 후 승인된 현장 관찰·압력 안정·알람 해제·명령/응답의 전후 증거. 실물복구 미완료를 문서검사로 대체하지 않는다.

다음 한 작업은 부모의 독립 검토에서 0497→0344 연결, raw/Word/HMI INT 차이,0479 중복쓰기,FG75 제목상충과FG108 개정일을 확인하는 것이다. 추가자료 없는 현재 CPU/실물 보류는 그대로 인계한다.

## 근거·검사 파일

- `extracts/PSH03/network-evidence.json`: 탐색 네트워크 맵, 의미검토 완료 수와 별도.
- `NNNN-refs.json`/`NNNN-wires.txt`: 직접 원본 XML 추출; UID/RID만 같은 다른 선언 후보가 함께 존재할 수 있으므로 본문이 채택한 NID·선언파일로 한정한다.
- `exact-declarations.json`, `address-overlap-review.json`: PSH03 정확명/주소범위 선언. 간접주소·외부Writer 완전성은 보류.
- `pdf-review.json`: 4개 고유 PDF쪽 실제 렌더 확인과 개정 경계.
- `static-review.json`, `source-hashes.json`: 직접 정적검사·현재 보존 해시·고정 Git blob 대조. 중지자산 해시는 보존검사만이며 내용을 실행하지 않았다.

## 원본 파일 해시와 고정 Git blob 대조


선택 원본·맥락·보존 파일 56개는 SHA-256 및 고정커밋 Git blob 내용 일치. 중지5자산 freeze 해시 일치. 최종 원본 Git 변경0. 자체 정적단언 23개 통과, HMI6주소, 실제 PDF4쪽. 종료 2026-10-11T10:37:16.587715+00:00. 해시개수는 원본 전체나 의미검토 완료 개수가 아니다.

| 원본 경로 | SHA-256 | 고정 Git blob OID | 내용일치 |
|---|---|---|---|
| `.agents/skills/gme-equipment-rollout/SKILL.md` | `fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b` | `9aa820ea6ca15b4e136c9772423b78ed4df6a3d4` | true |
| `AGENTS.md` | `0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2` | `073164bc6efd5791032d62c71b03b4dab48cb6f8` | true |
| `VERSION.json` | `5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7` | `fffb51663b7705aec91cb119ca80ee943a4ce758` | true |
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
| `all-in-one/sources/PID_1684n002I.pdf` | `2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b` | `8c83a59fefd5b8b651ec3537ea4236a073f5e109` | true |
| `all-in-one/sources/decoded-original/0014-FlgNet.xml` | `2e814adbaac6bab99bc668bfdab74f0fc90576324d0b88728951683869cfac30` | `4d164b074fcc13a8f97da9e24382cc169ef29555` | true |
| `all-in-one/sources/decoded-original/0030-FlgNet.xml` | `9252c9da764993de1edb8b2e44c46d6e9f9d4b6118e751a0dbeaa9ffd8ea721b` | `e74c70b751acdcdbc7a8b3b0c98aa773c2107cab` | true |
| `all-in-one/sources/decoded-original/0031-FlgNet.xml` | `76385eab8f8f72b9faa16f7cf8905f395591b18c0a9ee9e6d7dd085a38c45c65` | `653d27572de6beedcf3eb6c95702bb119a8b567f` | true |
| `all-in-one/sources/decoded-original/0032-FlgNet.xml` | `070bb8efa33d03b18add5da81d3f670a47c12b288076b7bfee11ac87fe6fa7e4` | `e31cf9aeecfbfc0c264921ac217cbd15479c1f34` | true |
| `all-in-one/sources/decoded-original/0062-IdentXmlPart.xml` | `34f188168dc4fad0d6e2c813028045f37b84025636bcebd8aa1c7ffb4cfd9bcd` | `624eed3ba6cd1eb54e7e3f316f8c4c159ca3b4b5` | true |
| `all-in-one/sources/decoded-original/0291-FlgNet.xml` | `fe0b92f074eba25148ce34084649af3d968962558d652727f1eea19f3e3c2550` | `1418fb2ed172c6df694a5eb8bf2dffd0b177653b` | true |
| `all-in-one/sources/decoded-original/0344-FlgNet.xml` | `08eabc412b9457eb615d1cb01b92682987bef170cbeab78070dd4c705ab93576` | `76eef5bbbbee10b7ac3494d736b453b9a8120d42` | true |
| `all-in-one/sources/decoded-original/0345-FlgNet.xml` | `b278a319d4d8cb8d157f449a2365445ff8f172245ebd2a468aa3ee79dba60f93` | `25656c8d9f39b8eccb67300905545b4cbcec2bfd` | true |
| `all-in-one/sources/decoded-original/0398-FlgNet.xml` | `4f092b18df4e44af98fd44e173f48dad213a4e80b71f46b0a5e8a700f5b0a747` | `67ebb54daa55093487ea7e780f23ae2cf193c397` | true |
| `all-in-one/sources/decoded-original/0479-FlgNet.xml` | `112e55599a4dc705438c8c61b936da9a167c22d9bbd909eda11c45c9dc33e839` | `38df067a2f4f62edfba9c5027002feccb45e5142` | true |
| `all-in-one/sources/decoded-original/0497-FlgNet.xml` | `334a065d6dc7aac9e9652a1f705a31fdadea6a5d4760dd6aa2ed3283a8e4b665` | `c6039bdea3aaaaa2d40cca76e5c440a2c94d4c0c` | true |
| `all-in-one/sources/decoded-original/0611-IdentXmlPart.xml` | `0d583915a261703954da22c176ba9f81338ad13ea2810e7cd5f7de8aa1bfa089` | `bad6b16fb32a32d47d882f48754994887457872b` | true |
| `all-in-one/sources/decoded-original/0612-IdentXmlPart.xml` | `95b545d4964d371ebfc107894ea90b8b1d0d7ab5d3a70e643f8ce539063c0f38` | `7cc782d33d07ef225c2104f3e7c9fbd31f7c7467` | true |
| `all-in-one/sources/decoded-original/0617-IdentXmlPart.xml` | `10bcf85169cb2512f55acadaef299a3d46b4b4cecd88032d739cfeba23e94aa9` | `9527658ee6808be34bd513b1b2ebaf3a4a5a6f3e` | true |
| `all-in-one/sources/decoded-original/0618-IdentXmlPart.xml` | `0c6762de9cdf0e294317f7463bea3d8e6df5673d333d9b1826ebd17a7ded044c` | `9eec0dbd8abde4aa7295f77b63ad473f895f274b` | true |
| `all-in-one/sources/decoded-original/0619-IdentXmlPart.xml` | `85694bb5b696e31e6a1217431112e5b750516c4f94078d6e127d4394a8b80456` | `11f0502c84a1f319a21459a35c0dc1c6ce8e8f36` | true |
| `all-in-one/sources/decoded-original/0620-IdentXmlPart.xml` | `da97226a148a1a8babaea67db412761a718b7e7537212b7807e8ea27d000d2d3` | `dc88b5e87ad3331928f14fcf647673a26fb70b6b` | true |
| `all-in-one/sources/decoded-original/0627-IdentXmlPart.xml` | `08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb` | `61ebc0abbb2ca160e11e1da400a3f14a397d8bc5` | true |
| `all-in-one/sources/decoded-original/0628-IdentXmlPart.xml` | `9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd` | `170ca5c72599edc7ea7eefe651c3680ce325e76a` | true |
| `all-in-one/sources/decoded-original/0629-IdentXmlPart.xml` | `67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972` | `058129bb01e27f7a6a0d0293f332d745e5bab74e` | true |
| `all-in-one/sources/decoded-original/0665-IdentXmlPart.xml` | `50e88d5f50f555151b35cfb17225e766c34ef6b490bd3a48e0a4e335fd17e3dd` | `ea4a8a5013081f648722c5ebbde3bb1366787990` | true |
| `all-in-one/sources/decoded-original/0667-IdentXmlPart.xml` | `ef924ced3e0e2b17e9c8440eb4946cd50d55df644c6ec24a1c4fd288fa6b73a3` | `7f2e1798eb9f260d19d038a83369484d0f438856` | true |
| `all-in-one/sources/decoded-original/0668-IdentXmlPart.xml` | `2248e994a0a02cd37c5c5edaca199b3421068feea91e2e8616560e814ef9f6ed` | `fe0f30d1eaae37783b0f03cb090353b3a3de3600` | true |
| `all-in-one/sources/decoded-original/0669-IdentXmlPart.xml` | `754c513339d00918717010047b8f9d865d8674c6978a6f86c6f1fa5d683506e2` | `f5bf8f3c41d2a07ba9dcfd8f400548be8cf51cd3` | true |
| `all-in-one/sources/decoded-original/0670-IdentXmlPart.xml` | `e56f3f0c4f2a86dd18578dedd4453915c2a51cd25e2cd9feced8538171a00841` | `b9466007b14e5c4f5d353dca5734401317e2dc03` | true |
| `all-in-one/sources/decoded-original/0671-IdentXmlPart.xml` | `26cb51706305c372d512c19770648bb0dbb74df8bd2277b1e0da1b8c88cca293` | `e38a4e2c93ac8093e2b0b8e082a64688b5d9845e` | true |
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
| `docs/equipment-standard/WORK-ITEM-TEMPLATE.md` | `4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586` | `e546f39535d2b589e80f97db869ac37ce4d05cfd` | true |
| `docs/equipment-standard/WORK-STANDARD.md` | `05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99` | `f76a570cc73098632e08759b17934000f7e3a253` | true |
