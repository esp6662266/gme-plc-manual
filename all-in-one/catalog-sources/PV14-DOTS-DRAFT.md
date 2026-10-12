# PV14 필터 냉풍 유입 밸브 원본 조사 초안

## 핵심 확인·상충·공유 근거

- 직접 출력은 Q17.0, 현장 위치입력은 I28.0 OPEN/I28.1 CLOSE, 처리입력은 DB13.DBX22.0/22.1이다. HMI의 PV_14 LS_Open/Close는 DB11.X74.0/74.1로 별개 주소이며 이 조사에서 결속하지 못했다.
- 고유 위치불일치 경보는 T20, S5T#20S, Fault_PV14 DB3.DBX13.4의 Set/Reset이다. TC09 온도 경보의 무타이머 망을 복제하지 않는다.
- Q17.0 = ON AND (M_PV14 OR Open false air OR MAX_TC09 OR MAX_MAX_TC09 OR Emergency_module_fault). Fault_PV14는 M_PV14만 Reset하며 나머지 OR 가지의 공통 차단 접점이 아니다.
- OEM FG168/PDF169의 168KA1 부하접점은 5–9, 코일은 A1/A2다. 하단 참조표의1/5/9를 부하1–9로 읽지 않았다. 위치접점 공급은 OEM110Vac인데 시공p60은 ZS.O/C를 DC로 분류한다. 현장 공급·모듈 타입·준공 결속이 미확정이다.
- P&ID TC09 Open170°C/Close160°C 표기, TC09 백업 MAX=180 및 코드 MAX−2 회복은 서로 다른 자료시점·조건이다. 어느 것도 현행 승인 보호값으로 채택하지 않는다.
- 공유 재사용: [TC09](TC09-DOTS-DRAFT.md)의 0539 온도 요청·경보/0483 환산·공통0291, [BF01](BF01-DOTS-DRAFT.md)·[BF02](BF02-DOTS-DRAFT.md)의 집진공정/공통호출·전원 경계를 같은 고정입력에서 연결 재사용한다. 아래 PV14 고유0215/0216/0397·선언 및 실제 PDF6쪽은 독립 대조했다. 주변 설비·CL12를 PV14와 함께 완료 집계하지 않는다.

## 1. 설비·자료 기준

- catalog_id PV14, 이름 필터 냉풍 유입 밸브, gate/공압 밸브, parent 없음, depth0, priority 없음, phase2/planned. INVENTORY catalog[29], equipment[33], 별칭 false air/cold air. 실제 동일성 확인 완료가 아니다.
- BATCH10-RESEARCH-INSTRUCTIONS, TASK3-BATCH10-SCOPE의 PV14 및 중복 검토 범위. 로컬2차133 통합 제외 유지. P&ID CL12는 관련 구동부 표기이며 별도 ID를 완료로 상속하지 않는다.
- 고정 읽기 원본 source-mv06, commit abcf31c5030bc7ef8749ed8e869a857f2387a28a, v1.12.0. 현재 게시본·현재CPU·준공 상태와 동일하다고 주장하지 않는다.
- AGENTS, gme-equipment-rollout 스킬/source-map, WORK-STANDARD/WORK-ITEM-TEMPLATE/INVENTORY/START-GPT61, VERSION/WORKSPACE-HANDOFF/PUBLICATION_STATUS/EXPANSION-WORK/ACTIVE-WORK 상단을 읽었다. 배치 최신 제한을 우선한다. 원본 preflight/build/test/generator 실행0.
- 작성자 PV14 조사자, 2026-10-11 UTC. 모델 런타임 증명 미확인. 수정은 이 초안과 extracts/PV14/뿐. 원본/공통코드/대장/버전/배포/운영기록·타초안 변경0. 신규 Work/Codex/재위임0. 시뮬레이터 작성·수정·생성·실행·행동시험0, PLC/현장/보호값/SEJIN 변경0.
- 아래 XML 약칭은 all-in-one/sources/decoded-original/<번호>-FlgNet.xml 또는 <번호>-IdentXmlPart.xml. LAD 문서번호·NID·UID/RID는 다르며 블록 문맥과 함께 읽는다. 색인은 탐색/문서 대응 근거이고 XML Part/Wire/선언을 대신하지 않는다.

| 7영역 | 상태 | 경계 |
|---|---|---|
| 설비·자료 기준 | 적용 | 실물 동일성·현재 프로젝트 미확인 |
| I/O·HMI | 적용/일부 미확보 | HMI 위치표시 주소와 실제 입력 결속 미확정 |
| 제어 | 적용 | 고유 요청·출력·위치 불일치; 현재 스캔/다중 Writer 미확인 |
| 전기 끝점 | 적용/부분 미확보 | OEM/시공 공급 분류 상충, 현행 단자/공압경로 미확정 |
| 알람·복구 | 적용/복구 미확보 | 고유20초·Set/Reset; 실제 복구 없음 |
| 증상 관찰 | 적용 | 읽기 전용 관찰 설계이며 시험/조작 아님 |
| 완료·누락 | 적용 | 문서·제품기능·TIA/CPU·실물 상태 분리 |

P&ID PID_1684n002I.pdf 실제p1: PV14/CL12는 TC09 부근에서 BF01/BF02로 갈라지는 공통 유입 덕트에 외기를 유입하는 가지다. BF01 전용 세정밸브나 BF02의 하위 EV로 합치지 않는다. 도번1684n002, 원작성06/04/2011, 판I15/01/2013(REMOVED MC-05, CHANGED POWER OF FN-02)을 footer에서 확인했다. BF 유입 Max180°C와 TC09 Open170°C/Close160°C는 해당 도면의 표기일 뿐 현재 안전값이 아니다.

## 2. I/O·HMI·선언

Global은 전역 선언, Local 임시변수와 구분한다. SSD AO는 Bool/Word에서 bit offset이며 Timer AO20은 T20이다. 0595 DepDBBlock RID253→Flag DB2,274→Allarm DB3,303→Inputs DB13;0628 RID4→Inputs DB13의 TOD N을 직접 확인했다.

| 대상 | 형식·주소 | 고유 선언과 참조 |
|---|---|---|
| PV-14 | Global Bool Q17.0 | 0594 SimpleAccess RID268 AO136 Output SAM=None;NID20 UID1998/2000 Read,NID21 UID2021 Write |
| PV-14 OPEN | Global Bool I28.0 | 0627 RID35 AO224 Input SAM=None;NID1 UID109 |
| PV-14 CLOSE | Global Bool I28.1 | 0627 RID33 AO225;NID1 UID102 |
| Inputs.PV-14 OPEN | Global Bool DB13X22.0 | 0629 RID36 AO176 UID113 Write NID1;0596 RID313 UID1999 Read NID20 |
| Inputs.PV-14 CLOSE | Global Bool DB13X22.1 | 0629 RID34 AO177 UID106 Write NID1;0596 RID315 UID24 Read NID20 |
| Tag_134 | Global Timer T20 | 0594 RID273 SAD Timer AO20;NID20 UID2003 Write/2004 Read |
| S5T#20S | Constant S5Time | 0597 RID317,NID20 UID2002,SV S5T_x0023_20S,V4608 |
| Allarm.Fault_PV14 | Global Bool DB3X13.4 | 0596 RID275 AO108;NID20 UID2005 Set/2008 Reset/2007 Read,NID21 UID2014 Read |
| Flag.M_PV14 | Global Bool DB2X13.1 | 0596 RID277 AO105;NID21 UID2016 Reset/2017 Read |
| Flag.RESET_ALLARM | Global Bool DB2X6.0 | 0596 RID276 AO48;NID20 UID2006 |
| Open false air | Global Bool M2.1 | 0594 RID278 AO17 Memory;NID21 UID2018 |
| MAX_TC09/MAX_MAX_TC09 | Global Bool DB3X8.6/8.7 | 0596 RID279/280 AO70/71;NID21 UID2019/2020 |
| Emergency_module_fault | Global Bool DB3X16.6 | 0596 RID312 AO134;NID21 UID23 |
| ON | Global Bool M0.0 | 0594 RID52 AO0 Memory;NID20 UID1997,NID21 UID2013. 이름만으로 현재TRUE 단정 금지 |

### 2.1 원시 입력 → 처리 입력

0397 LAD1070 hmi inputs NID1은 이름이 hmi여도 실제 PLC 입력 전달 망이다. W21 rail이 Contact101/108.in에 연결된다.

- CLOSE: ORef102(RID33) W100→Contact101.operand;101.out W103→Coil105.in;Coil105 operand W104→ORef106(RID34,DB13X22.1).
- OPEN: ORef109(RID35) W107→Contact108.operand;108.out W110→Coil112.in;Coil112 operand W111→ORef113(RID36,DB13X22.0).
- 두 Contact에 Negated가 없고 Coil은 일반 Coil이다. 실제 정상 접점극성·기계적 개폐 위치는 도면·현재 신호 대조 전에는 확정하지 않는다. 두 비트는 PV01/02의 MEM_OPEN/CLOSE 래치가 아니다.

### 2.2 HMI 백업 주소

sources/hmi_plc_tags.csv는 dde.cfg 파생 설정이다. PV_14\\Flag→DB2,X13.1(000B5)는 M_PV14와 주소 일치. PV_14\\LS_Open→DB11,X74.0(000B3), LS_Close→DB11,X74.1(000B2)는 DB13X22.0/1과 다르다. 모든 decoded-original 선언의 AO592/593 후보를 검색했으나 PV14 위치의 DB11 직접 GlobalAccess/전달을 확보하지 못했다. 이름만으로 HMI 표시가 처리입력을 읽는다고 합치지 않는다.

Allarmi_109→DB3,X13.4(00120)는 Fault_PV14 주소와 일치;Allarmi_190→DB3,X16.6(00407)는 비상모듈 경보 소비 주소와 일치. TC09 Allarmi_71/72는 기존 TC09 초안의 DB3X8.6/8.7 근거를 재사용한다. CSV의 ResetAlarms→DB2,X13.4(002E1)는 RESET_ALLARM DB2X6.0과 다르다. 이름만으로 고유 경보 Reset 버튼 경로라 단정하지 않는다.

실제 화면 위젯, 누름/떼기 이벤트, 수동요청 Set 방식, 권한·통신상태·경보문장·현재값은 미확보. HMI 주소 확인은 실행 UI/쓰기 검증이 아니다.

## 3. 요청·출력·호출·소유

### 3.1 PV14 직접 출력

0216 LAD1903 filter NID21. rail W2049→Contact2035.in;ON ORef2013 W2022→2035.operand;2035.out W2036이 아래 가지에 병렬 공급한다.

| 가지 | ORef·Wire·Part | 결과 |
|---|---|---|
| 고장 시 수동요청 해제 | Fault UID2014 W2023→Contact2037;out W25→RCoil2004;operand W2026→M_PV14 UID2016 | DB2X13.1 Reset |
| 수동요청 | M_PV14 UID2017 W2027→Contact2041;out W2042→OR2007.in1 | 출력 요청1 |
| 온도 냉풍요청 | M2.1 UID2018 W2028→Contact2043;out W2044→OR.in2 | 출력 요청2 |
| MAX 경보 | UID2019 W2029→Contact2045;out W2046→OR.in3 | 출력 요청3 |
| MAX_MAX 경보 | UID2020 W2030→Contact2047;out W2048→OR.in4 | 출력 요청4 |
| 비상모듈 경보 | UID23 W21→Contact22;out W24→OR.in5 | 출력 요청5 |

OR2007 Card5.out W2031→Coil2012.in, operand W2033→PV-14 UID2021/Q17.0. 모든 다섯 접점은 비반전. Fault_PV14는 출력 앞 직렬 허가가 아니다. 따라서 경보가 수동요청을 지워도 온도/비상 요청이 별도로 존재할 수 있는 구조다. 이는 현재 동작/안전성 시험 결과가 아니라 정적 연결 해석이다. Q17.0 참은 전압·릴레이·솔레노이드·밸브개방 완료 증명이 아니다.

### 3.2 TC09 관련 소유

TC09 초안의 0539 LAD1991 NID13·0683~0686 선언을 같은 고정입력에서 재사용한다. Temp>MAX에서 M2.1 Set, Temp<MAX−2에서 Reset. MAX_TC09는 Temp>MAX+5에서 Set, Temp<MAX−2 및 기존 MAX 조건으로 Reset/STOP_HORN Set. MAX_MAX는 Temp>MAX_MAX OR Temp>200 OR Temp<−60에서 Set, RESET_ALLARM 및 기존MAX_MAX로 Reset이다. 이 망에 Timer가 없는 것과 PV14 위치불일치20초는 별개다.

백업 저장 MAX180/MAX_MAX200, P&ID170/160, 코드 히스테리시스2를 한 현행 설정으로 합치지 않는다. TC09 환산 고장·FN04/BR01/RD01 소비 및 각 설비 고장·복구는 TC09/관련 설비 소유다. PV14 조사로 완료 집계하지 않는다. 비상모듈 경보의 발생·외부 안전회로 전체도 PV14 범위의 고유 경보로 복제하지 않는다.

### 3.3 호출·다른 쓰기 경계

공통 main0549 LAD1620 NID7의 ON Contact350.out W351→Filter CRef322.en은 BF01/TC09의 같은 고정 근거를 재사용한다. 병렬 호출을 ENO 직렬 호출로 바꾸지 않는다. 0147/0148 startup 공통Word 초기화는 아래5절에서 PV14 겹치는 대상만 대조했다.

network-map에서0409 LAD1089, block simulation NID8에 동일 처리입력의 대체쓰기 후보가 검색된다. 운영 제어의 활성 경로로 채택하지 않았으며 시뮬레이션을 작성·생성·실행·시험하지 않았다. 실제 호출/활성 상태·전체 간접/외부Writer·현재 스캔 순서를 이 문서로 확정하지 않는다. 원본020초와 실제 응답시간/현재 타이머상태는 별도다.

## 4. 전기 전달 끝점·실제 PDF

실제 PDF6개 고유 페이지를 렌더·시각 확인했다. 크롭/회전은 별도 페이지 수로 세지 않았다. 이미지 extracts/PV14/render/. 아래 도면 전압/퓨즈는 원문 표기이며 현행 측정값·승인 보호설정이 아니다.

### 4.1 OEM Electrical_Rev2.pdf

| FG / 실제PDF | 끝점·경로 | 실제 footer |
|---|---|---|
| FG168 / p169 | Q/A17.0,참조180/1→168KA1 A1;A2→−0Vdc152.4. 110Vac152.8(167/9→169/0)→168KA1 실제 부하5–9→168.1→X3:84 5×20 2A F→168.2→PV14 A1;PV14 A2→X3:85→0Vac9.9 | PNEUMATIC VALVE,27.05.2024,FG168/TOT262,별도개정기입 관찰없음 |
| FG168 / p169 | OPEN:110Vac152.8→X3:86 5×20 2A F→168.3→ZS.O PV14 접점13/14→X3:87→E28.0 참조177/2. CLOSE:110Vac→X3:88 2A F→168.4→ZS.C13/14→X3:89→E28.1 참조177/2 | 같은 페이지. +24Vdc152.5 선도 있으나 위치 접점 가지는110Vac선에서 내려옴 |
| FG177 / p178 | E28.0,참조168/4→모듈단자1;E28.1,참조168/5→단자2. CPU515/MOD4/Rack3. OPEN/CLOSED 설명과 일치 | DIGITAL INPUT/OUTPUT MODULE,27.05.2024,FG177/TOT262,별도개정기입 관찰없음 |
| FG180 / p181 | 모듈단자31 A17.0→참조168/3→168KA1. CPU515/MOD4/Rack3. 공급+24Vdc152.5→X22:4027 5×20 4A IST.→180.1→단자39 3L+;단자40 3M→−0Vdc152.4 | DIGITAL INPUT/OUTPUT MODULE,27.05.2024,FG180/TOT262,별도개정기입 관찰없음. 하단확대 별도 확인 |

168KA1의 하단 접점 참조표1/5/9와 상부 실제 부하5/9를 구분했다. 밸브 A1/A2는110Vac 부하,168KA1 A1/A2는24Vdc 구동계통으로 문서상 구분한다. 현재 제조사·릴레이모델·PLC 입력전압 정격·정상극성은 별도 명판/구성 확인 필요. FG180 다음에180B가 있으므로 다른 FG에서도 PDF=FG+1이라 일반화하지 않는다.

### 4.2 시공 Electrical_Can_Decoating_20241118.pdf

p35 실제 footer DUST ROUTE CONDUIT PIPING(1),CANDC-CONS-E018-035,D-PAGE18,35/64. p60 CABLE SCHEDULE(9),CANDC-CONS-C010-060,D-PAGE10,60/64. 두 쪽 Rev1 24.11.11 first draft design, CHECKED/APPROVED 공란. 현행 승인준공도 아니다.

| 행 | 양끝·분류·케이블 | 경로·설계길이 |
|---|---|---|
| 10_4 | =DUS+SC01-DUS1TB1A;BF01/JB01→SC01/DUS1TB1 ZS.O/C;DC,CVV7G1.0,spare2 | E500→222RE→222LAP1→212LAP1→211RB→E100,LEN16 |
| 10_5 | =DUS+SC01-DUS1TB1B;동일전후단,PV14;AC,CVV5G1.0,spare2 | 같은 경유→E200,LEN16 |
| 10_7 | =DUS+PV14-DUS1TB2A;SC01/DUS1TB1→PV14/DUS1TB2 ZS.O/C;DC,CVV7G1.0,spare2 | E110,LEN11 |
| 10_8 | =DUS+PV14-DUS1TB2B;같은 양끝 PV14;AC,CVV3G1.0,spare0 | E110,LEN11 |
| 10_10 | =DUS+PV14-ZS.OA;PV14/DUS1TB2→PV14/ZS.O;DC,CVV2C1.0 | E121,LEN3 |
| 10_11 | =DUS+PV14-ZS.CA;PV14/DUS1TB2→PV14/ZS.C;DC,CVV2C1.0 | E122,LEN3 |
| 10_12 | =DUS+PV14-PV14A;PV14/DUS1TB2→PV14/PV14;AC,CVV3G1.0 | E123,LEN3 |

p35 그림은211RB→DUS1TB1→DUS1TB2→ZS.O/ZS.C/PV14의 가지를 보여준다. TC09의10_9 KX2S1.0 직행 경로는 별도 온도계 소유다. p60의10_6 행은 실제 렌더에서 검게 가려졌고 p35 대응은 Delete이므로 텍스트층의 숨은 내용을 활성배선으로 채택하지 않는다. 설계 LEN은 실측길이 아니다.

상충: OEM ZS 공급110Vac와 시공 DC를 병합할 근거가 없다. 시공은 단자대 이름/경유는 있으나 OEM X3:84~89와 현장 DUS 단자별 심선 번호의1:1 결속이 미확보다. 승인 준공도·현장 전압/모듈타입을 확보하기 전 정상 전압·정상극성·안전위치·실제 공압압력을 추정하지 않는다.

## 5. 고유 알람·Reset·Word 겹침

0215 LAD1902 filter NID20. ON UID1997 W2009→Contact2028,rail W2044→2028.in;out W2029이 불일치 두 가지와 Reset 가지에 공급된다.

| 단계 | 실제 Part/Wire/ORef 결속 | 해석 |
|---|---|---|
| 개방 불일치 | Q17.0 UID1998 W2010→Contact2030;out W2031→NOT Contact2032(OPEN UID1999 W2011);out W2033→OR1979.in1 | 출력참 AND 처리OPEN거짓 |
| 폐쇄 불일치 | NOT Contact2034(Q17.0 UID2000 W2013);out W21→NOT Contact2036(CLOSE UID24 W23);out W22→OR1979.in2 | 출력거짓 AND 처리CLOSE거짓 |
| 시간 설정 | OR1979.out W2016→SdCoil1986.in;S5Time UID2002 W2017→1986.value;T20 UID2003 W2018→1986.operand | ON AND 두불일치OR를20초 SdCoil에 전달 |
| 경보 Set | 같은 OR.out W2016→Contact2038.in;T20 UID2004 W2019→2038.operand;out W2039→SCoil1991;Fault UID2005 W2021→operand | 불일치 조건과 T20접점으로 DB3X13.4 Set |
| 경보 Reset | RESET_ALLARM UID2006 W2023→Contact2040;out W2041→Contact2042(Fault UID2007 W2024);out W2043→RCoil1996;operand W2026→Fault UID2008 | ON AND Reset요청 AND 기존Fault. 위치정상확인 접점은 이 가지에 없음 |

두 위치가 동시에참이면 명령별 기대입력이 충족되어 위 불일치 조건은 성립하지 않을 수 있다. 별도 동시참/기구충돌 전용 경보를 이 망에서 찾지 못했다. 두 입력거짓은 출력상태와 관계없이 해당 기대방향 불일치가 성립하는 구조다. 이를 현장 진단시험으로 실행하지 않았다. Reset 자체가 원인제거·안전복구가 아니며 원인 지속시 재Set·스캔 우선순위·타이머 리텐션은 현재 CPU 확인 대상이다.

### 추가 Word 쓰기

- startup0147 LAD402 NID2: Move161.out1 W203→UID181.0563 Global RID19 AO96 Word/BAD6→0562 Flag DB2이므로 DB2.DBW12 쓰기가 M_PV14 DB2X13.1을 덮는다.
- startup0148 LAD403 NID3: Move273.out1 W322→UID298.0563 RID36 AO96 Word/BAD23→0562 Allarm DB3이므로 DB3.DBW12 쓰기가 Fault_PV14 DB3X13.4를 덮는다.
- 두망의 ON 조건 및0 초기화는 같은 고정 공통근거를 재사용했다. 0048 Constant RID54 Int0의 NID2 UID180/W202→Move161.in, NID3 UID297/W321→Move273.in을 확인했다. 각 enable은 직전 Move158.ENO/W201, Move270.ENO/W320이므로 ENO 연쇄를 무시한 무조건쓰기라고 하지 않는다. 고유 S/R만 유일Writer라 하지 않는다. startup doc401을0401-FlgNet HMI출력미러로 대체하지 않는다.

경보의 HMI 표시는 Allarmi_109 주소까지만 확인. 소리·문장·ACK·재요청 버튼·발생이력은 미확보이며 TC09 STOP_HORN Set을 PV14 고유자동복구로 가져오지 않는다.

## 6. 증상별 읽기 전용 관찰 계획

실제 리셋·강제출력·신호주입·탈거·시험·보호값 변경 지시가 아니다. 위험설비 접근은 승인된 현장 자격/절차로 제한한다.

| 증상 | 같은 시각 관찰할 값/위치 | 비교 및 원인 배제에 필요한 증거 |
|---|---|---|
| 수동요청 꺼지거나 유지 안 됨 | DB2X13.1,Fault DB3X13.4,ON,요청 UI 이벤트,시작Word쓰기 | Fault가 요청만Reset하는지;HMI쓰기/초기화/다른Writer 구분 |
| 수동요청0인데 Q17.0참 | M2.1,MAX/MAX_MAX,Emergency_module_fault,ON,Q17.0 | 다섯 OR소유 분리. 요청0을 자동안전폐쇄로 해석하지 않음 |
| 출력참인데 개방확인 없음 | Q17.0,168KA1 코일/접점·X3:84/85·PV14,공압/기구상태,I28.0,DB13X22.0,T20 | 전기/솔레노이드/기구/센서/입력전달을 나누고 현재 안전한 관찰방법 승인 필요 |
| 출력0인데 폐쇄확인 없음 | I28.1,DB13X22.1,ZS.C/X3:88/89,T20,Fault | 복귀 방식·fail-position·공압 상실시동작 미확정;출력0만으로폐쇄완료 단정 안 함 |
| 위치경보20초 전후 | 명령·양입력·T20·Fault·Reset요청의시각/신선도 |20초가온도경보지연아님;원인제거와Reset분리, 실제 타임라인 없으면 복구 미완료 |
| HMI와 PLC 위치 불일치 | DB11X74.0/1,DB13X22.0/1,I28.0/1,실제화면태그·통신시각 | 미확정 HMI결속/주소판본부터 확인;태그이름으로센서불량확정금지 |
| 양위치동시참 또는전압상충 |두원시/처리값,접점명판,DI모듈주문번호/전압,승인준공도 |이망은동시참검출전용아님;OEM110Vac/시공DC 차이를실물증거로해소 |
| 온도내려왔으나출력유지 | TC09값·MAX/MAX_MAX·M2.1·다른OR요청 | 히스테리시스/래치Reset과별개요청구분;실제안전임계추정금지 |

관찰 기록 필드: 관찰자,실제시각/시간대,위치,태그/주소,값/단위,신선도,수집장치,현재프로젝트/CPU ID,비교원본·개정,원인배제결과,승인된조치,별도복구확인. 실제 운영기록·사진을 새로 만들거나 공개 복제하지 않았다.

## 7. 완료·누락·인계

| 상태 축 | 결과 | 경계 |
|---|---|---|
| documentation | complete_with_gaps 초안 | PV14 7영역·고유핀·원본PDF6쪽·상충·누락 |
| static_review | 자체문서검사,독립검토대기 | 정적 파싱/핀·해시·고정blob;동작시험 아님 |
| ui_records | not_run | 도면·래더나란히,통합백업·선택복원,기록전후비교,보고서/PDF기능의 구현·저장·재읽기·재열기 미검증 |
| publication | not_published | 코드/기능통합·버전·게시수행안함 |
| tia_compile | not_performed | 로컬TIA추가권한없음 |
| live_cpu | not_performed | 현재CPU·활성Writer·통신·현행보호값미확인 |
| field_recovery | not_performed | 실물동일성·정상극성·공압/안전위치·복구미확인 |

기존 note/repair_observation/미지필드/다른설비/초안/저장키를 변경하지 않았다. BC01 동등 기능완료·현재정상으로 세지 않는다. 선정파일 전체해시수와 고유의미검토 범위는 별개다. 고유 의미검토는0215/0216/0397의 명시한 가지,0147/0148의 PV14 Word겹침,해당선언,PDF6쪽이며 공통TC09전체/모든소스전수의미검토가 아니다.

필요자료: 현재CPU·프로젝트/호출순서/Writer,실제HMI화면·이벤트·DB11전달,승인준공 단자심선목록,현행DI모듈주문번호·입력전압,168KA1/솔레노이드/ZS명판,액추에이터/밸브제조사·CL12대응/공압회로·안전위치,현행승인 온도한계/복구절차,관찰시간선·원인제거/복구증거. 새 자료 없이 실물보류 재검색을 반복하지 않는다.

다음 한 작업은 부모의 독립 원본 검토와 순차 초안 전달이다. 출력/리셋/설정 변경의 승인으로 해석하지 않는다.

### 실제 단계 시각 (UTC)

- 2026-10-11T11:34:54Z — scope and instructions read
- 2026-10-11T11:35:27Z — OEM FG168 render inspected
- 2026-10-11T11:36:04.124819+00:00 — unique declarations and render preparation
- 2026-10-11T11:36:56Z — six unique PDF pages visually reviewed, footer crops checked
- 2026-10-11T11:40:39Z — seven-area draft written
- 2026-10-11T11:42:02.200406+00:00 — static assertions and selected source hash verification started
- 2026-10-11T11:42:02.518009+00:00 — static assertions, fixed Git blob and freeze checks passed

### 선정 원본 SHA256·고정 Git blob 전체 목록

51개 선정 원본/맥락/보존파일 모두 고정blob 내용일치. 중지5자산 freeze일치, 원본Git변경0. 해시수는 의미검토수와 다르다. 자체검사JSON: extracts/PV14/static-review.json, 해시JSON: extracts/PV14/source-hashes.json. 프로그램/시뮬레이터 실행검사는 하지 않았다.

| 원본 경로 | SHA256 | 고정 Git blob OID |
|---|---|---|
| .agents/skills/gme-equipment-rollout/SKILL.md | fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b | 9aa820ea6ca15b4e136c9772423b78ed4df6a3d4 |
| .agents/skills/gme-equipment-rollout/references/source-map.md | 40612c5efb8f94608840c7bc0e9095ea840df54920861c388ae48ea34c7998dc | 49e50a7a8e56a16e2ec7f3607a03fd90adb8f1d3 |
| AGENTS.md | 0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2 | 073164bc6efd5791032d62c71b03b4dab48cb6f8 |
| EXPANSION-WORK.md | ec624de9fd2fcfac861a67fd5e828b25ef46db50bfd7a37ff16e2cb54cd0f7e2 | 4c42d88ecc2d48269eb23e13a20ebf3721a092a1 |
| PUBLICATION_STATUS.md | efe4857aec598d90470322cf3962eb3fe1f64947630e1fdf71d1c90134de8740 | d76401cf291fc0be681acc51fa898ad3ce46ff78 |
| VERSION.json | 5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7 | fffb51663b7705aec91cb119ca80ee943a4ce758 |
| WORKSPACE-HANDOFF.md | 215096d997782e78e901dfae36c782937e49611fbeb677a0d3fa50cbecf8d074 | dd0b8989d2376c4415bba9bd826fe6754c6b1a12 |
| all-in-one/ACTIVE-WORK.md | eff3bbc08ecff41da3beff77f3fec48e7d148708192bcaaab00f34b6a721afc2 | 6eb947c629b5ddf9c759ef87649451303938864b |
| all-in-one/assets/program-model-data.js | 52f8199371e3399b7c0d44ab5469f0472aced79d56bbef2887f7625f5d2aff0f | 38f34b0caa380a16ccad6f6f1e234a2fdf23f327 |
| all-in-one/assets/simulator-workspace.js | 3a6dfc618ff7e7b238f2671dc85d65704f33093a18eac879d86081d92c31e8bc | 97c2c831c77a9699fff0e0960b3bc1b7d93d45b3 |
| all-in-one/assets/virtual-plc.js | 5f1876052dc0067b1f010af0dfc941946e37003167481731293615d9c1c36dbc | 0bd9eceb54365a91214a37c5601b5067c39a3f75 |
| all-in-one/registers/equipment.json | 7870325dff32bbca90fa34507b301c4aad3347d669fddcd03b910343663996fa | acc42633033398216469064932c4b76987371606 |
| all-in-one/registers/program-model.json | 6203479c086b15bada12ac9d7e37db9280234ec26f1ea6091d7211dc09a577c5 | 9860b10f008d3a5ae714be50d77b703dfec32f3a |
| all-in-one/registers/simulator-freeze.json | bb93c1994effc5609939ba566b7802ce7ed55154a7310f02379b308ac2c8c835 | 808ffac14dbd1b4a7d797fa6cd0d647635d90b47 |
| all-in-one/registers/virtual-plc-test-results.json | a6b389f797f9a8b5ffe6928b8420f55c4cc459a327b0b48d716079d2eca6dd64 | 757dd50e45184568facb8ff62900b39d3ce848d1 |
| all-in-one/sources/Electrical_Can_Decoating_20241118.pdf | 3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd | 0ee6b6f8361c5790864dbba4bbd9d55e8e7c08f8 |
| all-in-one/sources/Electrical_Rev2.pdf | 5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6 | f610fd7c7ce14ae951b00cff57b969259bfb389d |
| all-in-one/sources/GME_20250506.zap18 | 00c79b6d986e68298f65b172c1807115bc5d9e450a74fcc989d0796d8d8a4ea8 | 211c4f604627a32f82a1124c2a9872c2fcf00865 |
| all-in-one/sources/PEData.plf | 647de7ea123daced41c27bec8f81aeb93c712cac714d4754d7da5c528abb016a | 65605ff8910f920109da731604aa5dc8d83fc956 |
| all-in-one/sources/PID_1684n002I.pdf | 2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b | 8c83a59fefd5b8b651ec3537ea4236a073f5e109 |
| all-in-one/sources/decoded-original/0047-IdentXmlPart.xml | 2e53bb895dd1ad2a74efaeb1ef16dfd61e62b1b2d7aa34cec8612f1b9cb0928e | 3dc282f149a21fdf76d5521ef1c833be63b578b4 |
| all-in-one/sources/decoded-original/0048-IdentXmlPart.xml | d8e8687de7271bd294c2b62b33d789700af9d5014d82b130141988c4d479253d | 64fc5a7f1ad33f3b901b00f0d22d23578ffabff8 |
| all-in-one/sources/decoded-original/0147-FlgNet.xml | 386513b215a8cc433f414b1b08279e9760e0efe209070ea95f8e445f674f428c | 0027890eca158e714dd6260dc920a5d3aa83319b |
| all-in-one/sources/decoded-original/0148-FlgNet.xml | 1d80e1bbf1c82dcc4dd18628c35935bbd55a17b5be9c1ca7bfb249600d154313 | 3069ae3b5fa16ed10a64c149b6cf5cb5ace423b3 |
| all-in-one/sources/decoded-original/0215-FlgNet.xml | 723789a5daf72bba1d49751963bc6517739761ae3a4122b875b8a66ea0de3a14 | 096f3482463759a7a506433e7b3266e3f13d3f14 |
| all-in-one/sources/decoded-original/0216-FlgNet.xml | 3a7fa8b0a095f054c543f90d0ffab84a8cd0c60ff1b5ec0101b112dc8f4ff37d | 97280ef67131ab7a480c8b0030d74de765c14c65 |
| all-in-one/sources/decoded-original/0397-FlgNet.xml | bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834 | 4ab8370493c4e28fc1eabeeebe2743d27f0c4021 |
| all-in-one/sources/decoded-original/0539-FlgNet.xml | d118d41f5007b112770c77fb33e8c84c2cb0e529e00d781d8837030196a015a5 | 11d48a289d9d3cc74088d9bbdbf230aca456179a |
| all-in-one/sources/decoded-original/0549-FlgNet.xml | 49f7169c33ed7f54559b0801e21a7d618584900972840e91cf51ad032e8febb1 | 985b5310b43b1015b5dee286aa0e42800564b94b |
| all-in-one/sources/decoded-original/0562-IdentXmlPart.xml | 85aada44dd9a3e66835463c3fed400f1efe121f4f5bc5ab8f0ad49481ec0ea1c | 1609802542a3e560baba3f2b73c306be281dfb23 |
| all-in-one/sources/decoded-original/0563-IdentXmlPart.xml | 86cf35b6baebc079cb5a092baf53ec3364c377ea7318eb263ab69c8b4550b4ad | 6a10fc694f896cda16409804daf2554c91635654 |
| all-in-one/sources/decoded-original/0594-IdentXmlPart.xml | 88ad174a0d5ccdf636146b68e43aa578c449c77ceab074b7ced2580261b831cd | f38b7d9a52b3d5ae74953da8290f6b417758c1b5 |
| all-in-one/sources/decoded-original/0595-IdentXmlPart.xml | 10c8152d3ae704c00e5d4c2f6ef1629be5a65aaf5ef626e1ea6085b9204f8f52 | 1f24565efac58926dabf5b3fc54ad0e9537410b2 |
| all-in-one/sources/decoded-original/0596-IdentXmlPart.xml | a0d79c7c4971d16f0e176c0c7d7b459a6e6702035b01ec01fd83e95561839dc0 | c8b2d1a05727b4ca44e2e4bed9fb58ba2b717576 |
| all-in-one/sources/decoded-original/0597-IdentXmlPart.xml | 60e292145fe54912a1da7510c8641a4f4c85efe62e1b5206ee3d92794a28de20 | 2831597d1879bd83f239e838dd4cbe6b3dc64e77 |
| all-in-one/sources/decoded-original/0627-IdentXmlPart.xml | 08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb | 61ebc0abbb2ca160e11e1da400a3f14a397d8bc5 |
| all-in-one/sources/decoded-original/0628-IdentXmlPart.xml | 9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd | 170ca5c72599edc7ea7eefe651c3680ce325e76a |
| all-in-one/sources/decoded-original/0629-IdentXmlPart.xml | 67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972 | 058129bb01e27f7a6a0d0293f332d745e5bab74e |
| all-in-one/sources/decoded-original/0683-IdentXmlPart.xml | 0c9b569d041cd5babbbeded8a3bdc5d3754927125756b6ac54b7cb991b22fc22 | 662acdb9a06c0ba1c0027e7dd215a28f07d3f02b |
| all-in-one/sources/decoded-original/0684-IdentXmlPart.xml | 6e9b3f173184adcddca503e81e2649022734b6ea3639c1d5ddaf0a08bac00208 | d67b98b5d5516e0330aae5cfdbee41a3e09206e1 |
| all-in-one/sources/decoded-original/0685-IdentXmlPart.xml | 2003d5741a0d707755c5e6e8b737fa106414b87b5b431b97271d9f1a5d343448 | 86bda988d9efedba92ba2f3e4877497d9eb5230a |
| all-in-one/sources/decoded-original/0686-IdentXmlPart.xml | b450d8ff22f0fffd7a214b2a696af28a03a27834ebf862bfaa822dc9bfb3c8d4 | 8c152d926692a8e15973c980e08e338d29411814 |
| all-in-one/sources/decoded-original/0688-IdentXmlPart.xml | ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda | 463585759f1ecd94f32362b4fefb000a152f5773 |
| all-in-one/sources/decoded-original/0692-IdentXmlPart.xml | bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037 | 737785d03b5fad43c5b4d451955726d800edb1c0 |
| all-in-one/sources/decoded-original/0694-IdentXmlPart.xml | 757ccebdf32d0a168dd787bfa735fe6494eac4c4a9f7a5adc63898a88e8b152d | c45e8f3ca4129dc06734f6a12ef79e6ed6528a7d |
| all-in-one/sources/decoded-original/network-map.json | c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60 | 424430b6b953e43138e5d0a18ca40c949e21cfa1 |
| all-in-one/sources/hmi_plc_tags.csv | a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404 | cf4c0650e7c7baac350dcb89909b808435704880 |
| docs/equipment-standard/INVENTORY.json | 720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc | 587c3748ad9224718f95ba06463fee913dae231d |
| docs/equipment-standard/START-GPT61.md | 35769e3146ccd707fea2b81b67b30376b76a0a19c7e662fe2bb4fdd382306f94 | 0d08cab3678df7e2625251b641b138ef4956483b |
| docs/equipment-standard/WORK-ITEM-TEMPLATE.md | 4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586 | e546f39535d2b589e80f97db869ac37ce4d05cfd |
| docs/equipment-standard/WORK-STANDARD.md | 05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99 | f76a570cc73098632e08759b17934000f7e3a253 |
