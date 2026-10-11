# DP02 백 필터 차압 독립 원본 조사 초안

## 핵심 인계 요약

- DP02는 BF02 차압 계측의 고유 ID다. DP01과 같은 이름, BF02와 겹치는 별칭 `pr_br02`는 동일 실물·완료 병합 근거가 아니다.
- 고유 원본 재확인: PR_BR02는 **Int %IW400:P, Peripherie 접근**이다. DB1.DBW242 DP_02는 환산 결과이며 원시 입력·HMI 표시·BF02_RUN과 다르다.
- FG169/PDF170의 DP02는 X3:95/96 전원,97/98 아날로그,99 실드다. FG172/PDF173의 PEW400은 채널7,34 I7+/36 U7−·I7−다. **BF02 설치 장소지만 JB1 전원·AI 경로**다. BF02의 JB2 세정 출력 모듈로 옮기지 않는다.
- 환산은 Int 입력과 Zero를 DInt로 바꾸고 `(raw + Zero) × Coeff / 28000`을 DInt 연산한 뒤 Int OutValue로 Move한다. Zero를 빼거나 분모를27648로 바꾸지 않는다. 범위 밖은−9999, Out_of_range는 Move.eno→일반 Coil이다. 3분 유지 경보와 구분한다.
- 백업 저장값은 ZERO_DP02=0, COEFF_DP02=500, DP02 단계 임계값·시간=0이며, 세정 허가는 별도로 DP_01_SOGLIA_1(백업50)을 읽는다. 현재 설정·사용 권장값이 아니다.
- 상충·누락: OEM 센서0/50mbar, 백업계수500, P&ID의5÷10mbar, 알람 Int2800/−100/2500을 동일 단위로 확정할 근거가 없다. 실제 채널 파라미터·HMI 소수점·센서 명판·현재 계수를 확보해야 한다.
- BF02 초안 공유 근거: 공통 Forza/세정 시간/알람·startup Word/호출 경계는 기존 BF02 자료를 연결 재사용했다. DP02 고유0522·0291·0014·선언·계수·FG169/172·시공p61은 원본에서 별도로 다시 대조했다. 단순 DP01 이름 치환이 아니다.

문서 상태는 complete_with_gaps인 자체 조사 초안이다. 로컬2차133 통합 제외를 유지하며 UI·기록·배포·TIA·CPU·현장 복구를 완료로 표시하지 않는다. DP02 작성으로 BF02/DP01/하위 밸브 완료를 상속하지 않는다.

## 1. 설비·자료 기준

| 구분 | 확인 내용 | 미확정 경계 |
|---|---|---|
| 대장 | INVENTORY catalog[1], DP02, sensor, 계측, parent_id=null, depth0, phase2; equipment[96] | 대장 분류는 실물 동일성 완료가 아님 |
| 별칭/범위 | dp_02,pr_br02; BF02 차압 감시; BATCH05-SCOPE 해당 행과 OVERLAP-REVIEW의 독립 신규 조사 분류 | BF02 별칭 충돌·DP01 동명 유지 |
| 고정 입력 | source-mv06, abcf31c5030bc7ef8749ed8e869a857f2387a28a / v1.12.0 | 최신 main/현재 CPU/현행 준공도와 동일하다고 전제하지 않음 |
| 자료 시점 | PLC 백업 GME_20250506.zap18, OEM 전기 기본일27.05.2024, 시공24.11.11 first draft, P&ID 판I | 서로 다른 자료 시점; 승인된 현행 통합본 아님 |
| 독립 경계 | P&ID p1 BF02 옆 DP-02와 두 취출 경로 확인. SC11/VR05/EV51~90은 주변 독립 대상 | 취출구 고저압 배관·현장 정상 극성·교정상태 미확인 |

AGENTS.md, 스킬/SOURCE MAP, VERSION/WORKSPACE-HANDOFF/PUBLICATION_STATUS/EXPANSION/ACTIVE-WORK, WORK-STANDARD, WORK-ITEM-TEMPLATE, INVENTORY와 묶음 지시를 읽었다. 최신 자체 조사 지시의 원본 생성기·시험 금지와 허용 출력 범위를 우선했다. 모델/추론 수준의 런타임 증명은 미확인이다.

수정은 이 MD와 extracts/DP02 아래뿐이다. 원본·공용 추출·다른 초안·코드·버전·공개 대장·운영 기록은 보존했다. 시뮬레이터 작성/수정/생성/실행/행동시험, PLC/현장/보호값/SEJIN 변경, 새 Work/Codex, 재위임, 사용자 Mac·TIA 접근은 수행하지 않았다.

아래 네 자리 XML번호는 all-in-one/sources/decoded-original/ 아래 파일이다. NID는 블록별이므로 RID/UID 숫자만으로 다른 블록 선언을 합치지 않는다. 실제로0291의 ORef41/RID25/NID1은 다른 블록 Allarm1 후보와 숫자가 겹쳤으나, 이 블록0612의 Int−1382 상수 선언·비교핀·원문 doc1658을 대조하여 구별했다. 추출 파일은 후보를 보존하며 자동 결속의 무오류를 주장하지 않는다.

## 7영역 적용표

| 영역 | 상태 | 작성 범위/누락 |
|---|---|---|
| 설비·자료 기준 | 적용 | 독립 ID, BF02 위치/JB1 전기 소유, 고정 판본; 현물 확인 없음 |
| I/O·HMI | 적용/일부 근거 미확보 | 원시·결과·계수·알람 형식/주소; 실제 이벤트·소수점·현재 값 없음 |
| 제어 | 적용 | 호출/환산/범위·일반 Coil/공통 세정 소비; 현CPU 실행 없음 |
| 전기 끝점 | 적용 | 전원→X3→센서→채널7, 실드·시공 교차패널; 현행 단자 마킹 없음 |
| 알람·복구 | 적용 | BF02_OFR와공유MAX_DP 구별,3분S/R·Word경계; 복구증거 없음 |
| 증상 관찰 | 적용 | 안전한 관찰·비교 설계; 실제 수리·조작 안 함 |
| 완료·누락 | 적용 | 정적 조사와 독립검토/UI/게시/현장 분리 |

## 2. I/O·HMI·저장 계수

### 2.1 직접 선언

0674의 BAD BIRID8=Coeff/TOD4,11=Data/TOD1,354=Allarm/TOD3를 결속했다. AO/BO는 bit offset이며 byte 주소로 환산했다. 기본 타입을 이름으로 추정하지 않았다.

| 신호 | 타입/주소 | 원본 선언 및 호출 위치 | 의미 |
|---|---|---|---|
| PR_BR02 | Int, Input AO3200, SAM=Peripherie → %IW400:P | 0678 RID300/NID41 UID1564 | 직접 주변장치 입력. 단순 IW400 process-image 읽기와 구분 |
| ZERO_DP02 | Int, DB4.DBW120 | 0676 RID302 BO960/BAD8, NID41 UID1566 | 환산에 더하는 offset |
| COEFF_DP02 | Int, DB4.DBW122 | 0676 RID301 BO976/BAD8, NID41 UID1565 | 환산 배율 |
| DP_02 | Int, DB1.DBW242 | 0676 RID303 BO1936/BAD11, NID41 UID1567 Write | 환산 결과, 직접 물리값 아님 |
| BF02_OFR | Bool, DB3.DBX24.5 | 0676 RID430 BO197/BAD354, NID41 UID23 Write | Signal linearization.Out_of_range |
| MAX_DP_FILTER | Bool, DB3.DBX9.5 | 0684 RID119 BO77/BAD10,0682 Allarm/TOD3 | DP01/DP02 공유 유지 경보 |
| ON | Bool,M0.0 | 0678 RID1, NID41 UID1562/1563 | 호출 EN과함수 IN0 양쪽에 연결; 이름으로 현재 TRUE 확정 안 함 |

Local 함수 인터페이스0611: RID1 IN0 Bool,3 Analog_input Int,8 Zero Int,13 Coeff Int,19 OutValue Int,26 Out_of_range Bool. 임시 App5 RID6/App6 RID9/App3 RID11/App4 RID14는 DInt다. Global 데이터와 Local 연산 임시영역을 구분한다.

### 2.2 HMI 설정과 실제 이벤트 경계

hmi_plc_tags.csv(dde.cfg 설정, Access Name=PLC)에서 주소를 직접 읽었다.

| 파일행 | 태그 | 설정주소 | 내부ID | 원본 결속 |
|---:|---|---|---|---|
|17|Allarmi_235|DB3,X24.5|00459|BF02_OFR|
|251|Coeff_DB4_DBW120|DB4,INT120|00291|ZERO_DP02|
|277|Coeff_DB4_DBW122|DB4,INT122|0026E|COEFF_DP02|
|285|data_DB1_DBW242|DB1,INT242|00264|DP_02|
|361|Coeff_DB4_DBW138|DB4,INT138|00205|허가가 실제 읽는 DP_01_SOGLIA_1|
|535|Allarmi_78|DB3,X9.5|0013F|공유 MAX_DP_FILTER|

이 설정은 온라인 값·쓰기 가능·버튼 동작·경보 확인 이벤트 증명이 아니다. HMI 객체, 화면 소수점/단위, 쓰기 권한, 알람표 이벤트, 원시 %IW400:P 표시 객체는 미확보다. BF02_RUN 설정 M180.4는 세정 허가 표시이며 DP02 센서 정상 진단이 아니다.

### 2.3 백업 저장값의 제한된 의미

live_index.json `_7ev` doc1604의 InterfaceMember_Name/Datatype/Value는 각각129토큰으로 정렬된다. 대소문자 정규화 검색 후 선언 주소·형식과 대조했고 extracts/DP02/backup-values.json에 보존했다.

- index60 zero_dp02 Int0 / index61 coeff_dp02 Int500.
- index69 dp_01_soglia_1 Int50. DP02허가가 읽는 이름은 원문 그대로 DP01이다.
- index83~86 dp_02_soglia_1~4 Int0.
- index87~91 dp_02_pausa_soglia_1~5 S5Time s5t#0ms.
- index92~96 dp_02_lavoro_soglia_1~5 S5Time s5t#0ms.

이것은 추출된 백업 저장값이며 현재 CPU 값·운전 정상값·권장 설정이 아니다. 원본 Int500과 센서0/50mbar를 보고 0.1mbar/단위라고 추정할 수는 있지만 HMI 스케일·채널범위·교정자료가 없어 이 초안은 확정 단위를 붙이지 않는다. DP02의0 임계값/시간도 설정 오류라고 단정하거나 수정하지 않는다.

직접 선언 검색에서 DP_02 Write는0522, BF02_OFR Write도0522로 결속됐다. DP_02 Read는0596 NID2/29의 단계/허가와0684 NID14의공유경보다. 이 이름검색 결과는 간접주소·외부 HMI·통신·전체 DB/Word쓰기·현CPU 강제의 부재 증명이 아니다.

## 3. 제어 구조와 고유 환산

### 3.1 호출 0522 LAD1774 / index44 / NID41

| 경로 | 실제 원본 핀·선 |
|---|---|
| EN | rail W1577→Contact1575; ON ORef1562/RID1→operand W1569; out W1576→CRef1556.en |
| 블록/IN0 | CodeBlock1568/RID5=0672 Signal linearization, CRef1556/RID351=0680 인터페이스. ON ORef1563→IN0 W1570 |
| 입력 | ORef1564/RID300 PR_BR02→Analog_input W1571 |
| 계수 | ORef1565/RID301→Coeff W1572; ORef1566/RID302→Zero W1573 |
| 결과 | CRef1556.OutValue W1574→ORef1567/RID303 DP_02 |
| 범위오류 | CRef1556.Out_of_range W24→ORef23/RID430 BF02_OFR |

0031 main LAD1619/NID6의ON Contact282/W280→W283이 Analog CRef261와Allarms3 CRef270 등을 허가한다. CodeBlock273/RID55 및279/RID64와0688을 대조했다. 이 호출과 Filter0549의후속 호출은 BF02 공유 근거를 재사용한다. 같은 전선·네트워크 색인만으로 현재 스캔 최종값이나 ENO 성공을 보장하지 않는다.

### 3.2 0291 LAD1658 / signal linearization index1 / NID1

범위 허가: IN0 ORef196/RID1 W220→Contact255, rail W257. W256은 Gt258/Lt가 아닌 Le259/Gt190 분기에 공급된다. 정상 가지는 Gt258(raw>−1382, ORef32/33 W30/31)→W25→Le161(raw≤32767, ORef29/34 W27/28)→W26→Convert164.en이다.

| 단계 | 실제 Part/Wire/ORef | 형식·해석 |
|---|---|---|
| raw 확장 | W225 ORef199→Convert164.in; W226 out→ORef200 App5 | Int→DInt |
| Zero 확장 | Convert164.eno W227→Convert167.en; W228 ORef201→in; W229 out→ORef202 App6 | Int→DInt |
| 합산 | Convert167.eno W230→Add170.en; W231 App5/W232 App6→in1/in2; W233→App3 ORef205 | DInt raw+Zero. 빼기 아님 |
| Coeff 확장 | Add170.eno W234→Convert174.en; W235 ORef206→in; W236→App4 ORef207 | Int→DInt |
| 곱셈 | Convert174.eno W237→Mul177.en; App3/App4 W238/239; out W240→App3 ORef210 | DInt 곱셈 |
| 나눗셈 | Mul177.eno W241→Div181.en; App3 W242, DInt28000 ORef212/RID17 W243; out W244→App3 ORef213 | DInt 나눗셈, Real 연산 아님 |
| 결과 Move | Div181.eno W245→Move185.en; App3 ORef214 W246→in; out1 W247→OutValue ORef215/RID19 | DInt 임시값에서 Int 출력 목적지로 Move; 폭/오버플로·컴파일 미검증 |

따라서 범위 내 계산 구조는 `(raw+Zero)×Coeff/28000`이다. 양자화·오버플로·현재 실행 결과는 시험하지 않았다. 0612 상수의 원문 signed표기와 타입을 보존했다: RID25 Int−1382(SV `_x002D_1382`, V4294965914), RID29 Int32767, RID17 DInt28000. V의 큰 양수 문자열만 보고 unsigned 임계값으로 해석하지 않는다.

### 3.3 범위 밖과 함수 비활성 쓰기

- 0291 Gt190: raw ORef42 W36 > Int32767 ORef43 W37 → W35 OR47.in1.
- Le259: raw ORef40 W38 ≤ Int−1382 ORef41 W39 → W48 OR47.in2.
- OR47.out W49→Move193.en. Int−9999 ORef218/RID21 W252→in; out1 W253→OutValue ORef219/RID19. RID21 SV−9999/V55537은16bit signed표기다.
- **Move193.eno W21→Coil23.in; ORef24/RID26 Out_of_range W22→operand.** 일반 Coil이며 Set/Reset이나3분 지연이 아니다. OR.out를 곧바로OFR에배선한것처럼 생략하지 않는다. ENO·미실행 출력의 실제 PLC의미는 컴파일/온라인검증이 필요하다.
- 다음0014 LAD1659/index2/NID2는 NOT IN0 Contact171(ORef165/RID1,W168)→W172 Move162.en; Int0 ORef166/RID23 W169→in; out1 W170→OutValue ORef167/RID19다. 비활성의0쓰기이지 OFR명시Reset은 아니다. DP02호출은 EN과IN0 둘다ON이므로 이 내부 가지가 현장에서항상실행돼출력이0으로된다고주장하지않는다.

−9999는 실제 음의 압력 측정으로 읽지 말고 원본의 범위 밖 대체값 가능성을 먼저 구별한다. raw32767보다큰조건은Int포트로선언돼있다는점도보존한다. 다른형식이나통신변환을추정해상한분기삭제/수정하지않는다.

### 3.4 DP02 소비: BF02 허가와 공통 세정 시간

0219 LAD1886/NID29의 고유 DP02 가지를 다시 대조했다. ON Contact21(W48)→SC11 처리응답 Contact28(W61)→VR05 처리응답 Contact29(W63)→W64가 Le30.pre와Forza Contact31.in에병렬공급된다. Le30.in1은 DP_02 ORef43/RID31 W65, in2는 **DP_01_SOGLIA_1 ORef44/RID8 W66**. Le30.out W67→OR32.in1,Forza ORef45/RID57 W68→Contact31.out W69→in2. OR.out W70→Local허가 Coil33, operand ORef46/RID65 W71; out W76→BF02_RUN Coil78, operand ORef79/RID344 W77.

정적식은 ON AND SC11처리응답 AND VR05처리응답 AND (DP02≤DP01_S1 OR Forza)다. DP02 센서·BF02 본체·처리응답·메모리 RUN을 서로의 실제 피드백으로 바꾸지 않는다.

공통근거 BF02 초안 §3.2/3.3와 원본0200/0199/0201을 재사용·핵심대조했다.

- 0200의Forza는2시간T134/10분T133 외에 ON Contact460→OR21.in2 W22가있다. 따라서 주기타이머만으로 제한되는 설명은 틀린다. Forza도SC11/VR05위응답을우회하지않는다.
- 0199/NID2는OFF AND Ev_filter_on>50 뒤 DP02_S1~S4에 따라5단계Pause를선택한다. Lt395/Ge407→Lt410/Ge422→Lt425/Ge437→Lt440/Ge452, Pause Move398/413/428/443/455, Work Move401/416/431/446/458. 모든Work는동일DP02_LAVORO_SOGLIA_1 RID36이다.
- 0596의DP02_S1~4는DB4.W166/168/170/172, Pause1~5는W174/176/178/180/182, Work1은W184다. 목적지LAVA_PAUSA/LAVORO는DB1.W236/W238 **Word**이며원본S5Time출처와구분한다.
- 0201/NID4의ON Contact500은 허가OR보다 앞에서Move457/462를따로허가하여DP01의Pause1/Work1을동일Word에쓴다. DP02 단계표가현재최종세정주기를독점한다고설명하지않는다.
- 공유T1/T2와EV출력의전체 경로는 BF02초안의검토결과를연결하며 이번DP02의고유출력/알람수로다시집계하지않는다. OFF를현재FALSE/dead code로단정하지않는다. startup live_index doc401은STL이고0401-FlgNet(HMI출력미러)와다른자료다.

## 4. 전기 양 끝점·실제 PDF·개정

원본 PDF를 직접 렌더하여 시각 대조한 고유페이지는6개다. 회전·확대 크롭은 중복 합산하지 않았다. FG를PDF번호에서일괄감산하는방식으로정하지않았다.

| 원본 PDF | FG/도번 | 실제페이지 | 제목/확인범위 | 실제 footer |
|---|---|---:|---|---|
| Electrical_Rev2.pdf | FG152 |153|SUPPLY 110Vac JB1 PLC MODULE|DATA27.05.2024,추가개정란기재공란|
| Electrical_Rev2.pdf | FG153 |154|CONFIGURATION PLC JB1 BOX|DATA27.05.2024,추가개정란기재공란|
| Electrical_Rev2.pdf | FG169 |170|DIFFERENTIAL PRESSURE CONTROL|DATA27.05.2024,추가개정란기재공란|
| Electrical_Rev2.pdf | FG172 |173|ANALOG INPUT MODULE|DATA27.05.2024,추가개정란기재공란|
| Electrical_Can_Decoating_20241118.pdf | CANDC-CONS-C011-061,D-page11 |61|CABLE SCHEDULE10,DP02의4행|Rev1,24.11.11,first draft design,CHECKED/APPROVED공란|
| PID_1684n002I.pdf |1684n002,ApexI|1|BF02 차압 취출/DP02/타이틀|원작성06/04/2011,개정I15/01/2013|

### 4.1 JB1 공급·DP02 고유 신호 양 끝점

| 경로 | 원본 양 끝점·표기 | 경계 |
|---|---|---|
|110Vac 분기|FG152:9.10(9/4)→X3:3→152QF4 2A 주접점1–2→110Vac152.8;0Vac9.9→X3:2→하류공통|도면정격이며현행보호설정추천아님|
|DP02 전원|FG169:110Vac152.8(168/9)→X3:95(5×20,2AF)→169.2→DP02 110Vac입력;0Vac9.9→X3:96→다른전원단자|DP01 X3:90/91과구별. DP02단자내부번호는도면에안보임|
|DP02 출력+|FG169:센서OUTPUT4–20mA의+→X3:97→+PEW400(172/5);FG172:+PEW400(169/8)→단자34 I7+|물리계기범위0/50mbar,설치정상극성은현장확인필요|
|DP02 출력−|FG169:센서−→X3:98→−PEW400;FG172:단자36 U7−/I7−|34/36이며DP01채널6의30/32로복제안함|
|실드|FG169:X3:99→169SCH2(172/5),FG172의169SCH2(169/8)실드표기|X3실드와원본접지기호보존;현행접지연속성미확인|
|AI전원|FG172:+24Vdc152.5→X22:4000(5×20,500mAF)→172.1→41 L+;−0Vdc152.4→44 M|도면에는42 L+/43 M도표시되나그핀에동일외부선을임의추가안함|
|JB1 AI구성|FG153:153A1 POS2 AI8×U/R/RTD/TC ST,6ES7531-7KF00-0AB0;FG172 CPU515/MOD2|현재설치형번·펌웨어·4–20mA채널파라미터미확인|
|JB1 인터페이스|FG153:153IM155 6ES7155-5AA01-0AB0,X1P1/P2 PROFINET;152.5/152.4 공급은X80의2L+/2M에그려짐|1L+/1M과구분;주소·네트워크실시간상태미확인|

152QF1/152GD1/152QF2는JB1 DC공급이고152QF3/TM1/EV1은냉각가지다. DP02 센서110Vac와AI24Vdc를하나의전원으로합치지않는다. 이계측회로에는EV부하릴레이5/9같은경로를붙이지않는다. BF02 세정출력릴레이의하단접점표1/5/9 및실부하5/9 검토는BF02공유문서범위다.

### 4.2 시공 케이블과 소유 경계

시공p61에서 다음4행을 직접 확인했다. 번호/기기명/장소를 원문대로 보존한다.

| 행/케이블 | FROM→TO | 종류/코어/단면·경로 | 남은경계 |
|---|---|---|---|
|11_3 =DUS+BF01-JB01TB6A|BF-01/JB01→BF-02/JB01TB6,DP-02 POWER|AC,CVV,3G,1.0,SPARE0;E300→222→223RD→E100,Adjustment2,LEN23|BF02설치지만JB01에서옴. LEN은설계표값|
|11_4 =DUS+BF01-JB01TB6B|같은양끝,DP-02 AI|AI,CVV-S,2S,1.0,SPARE0;같은Route/Adjustment/LEN|차압출력케이블이며전원케이블과분리|
|11_27 =DUS+BF02-DP02A|BF-02/JB01TB6→BF-02/DP-02,IN POWER|AC,CVV,3G,1.0,SPARE0;E100,Adjustment1,LEN2|OEM X3:95/96와현장코어별단자일대일표미확보|
|11_28 =DUS+BF02-DP02B|BF-02/JB01TB6→BF-02/DP-02,OUTPUT|AI,CVV-S,2S,1.0,SPARE0;E100,Adjustment1,LEN2|OEM X3:97/98/99와현행접속마킹미확보|

이자료는first draft design이며준공도/실측결과가아니다. JB01TB6을BF02위치라는이유로JB02TB6으로고치지않는다. BF02초안의JB02 전원/통신 케이블번호 상충은 별도세정회로범위이며 DP02의이4행을해결했다는증거가아니다.

## 5. 알람·복구

### 5.1 BF02_OFR와 공유 MAX_DP_FILTER의 구별

BF02_OFR는0522→0291의범위검사결과이며DB3.X24.5이다. MAX_DP_FILTER는0540 LAD1992/NID14,DP01/DP02공유DB3.X9.5다. 0683 Int상수·S5Time3M,0686 Tag112 Timer AO114=%T114와0684선언을대조했다.

- ON Contact1204(ORef1153,W1173)→W1205는4개비교와Reset가지에공급.
- DP02 고유상한: Gt1124.in1 DP02 ORef1156/RID116 W1177,in2 Int2800 ORef1157 W1178,out W1179→OR1120.in2.
- DP02 고유하한: Lt1130.in1 DP02 ORef1160/RID116 W1183,in2 Int−100 ORef1161 W1184,out W1185→OR1120.in4.
- DP01 Gt1121(>2800)/Lt1127(<−100)이같은OR의in1/in3에있다. 어느센서발생인지공유경보비트만으로구별안됨.
- OR.out W1186→SdCoil1136.in와T114 Contact1206.in. S5T#3M ORef1162 W1187→value,T114 ORef1163 W1188→operand. Contact1206 operand W1189,out W1207→SCoil1141;ORef1165/RID119 W1191→MAX_DP_FILTER.
- Reset: ON→RESET_ALLARM Contact1208(W1193)→현재경보 Contact1210(W1194)→Lt1146 DP01<2500→Lt1149 DP02<2500(W1198/1199)→W1200 RCoil1152,operand ORef1172/RID119 W1202.

Reset에는하한정상조건이없다. 그러므로−9999범위밖대체값이DP02에있더라도단순경보해제가센서정상·차압회복을증명하지않는다. 타이머시간/Set·Reset동시최종값/현재호출상태는미확인이다. 원본Int상수를mbar보호권장값으로재명명하지않는다.

### 5.2 비트 외 Word쓰기·알람관리 공유 근거

BF02 초안 §5.2/5.3의원본0148/0151/0152 경계를연결재사용했다. 0148의DB3.W8=0경로는이번에도원본핀으로대조했다: ON Contact329→W330 Move267.en;Int0 ORef293/RID54 W315→in;out1 W316→ORef294/RID32.0048 Int0,0563 Word AO64/BAD23,0562 Allarm/TOD3가DB3.DBW8을구성한다. 따라서X9.5는startup Word0의영향을받지만X24.5는확인한Word0~16범위밖이다.

공통0151은DB3.W0~16을DB6스냅샷에복사하고0152는이를비교하여NEW_ALLARM을쓴다. 이범위는MAX_DP_FILTER를포함하지만BF02_OFR를포함하지않는다. 이것을시스템전체BF02_OFR표시/사이렌없음으로확대하지않는다. HMI Allarmi_235 직접설정은별도로확인했다. 전체정지/호른/통신소비자는미확보이며센서고장이자동으로모든공정을정지시킨다고쓰지않는다.

### 5.3 복구 관찰 기준

범위오류해제,공유S/R경보해제,정음,세정허가,RUN표시,실제필터차압,계기교정은서로다르다. 원인제거와승인된관찰시간·실제값·재요청/복구확인없이는복구완료로표시하지않는다. 전원재시작·PLC강제·보호임계값변경으로경보를없애는조치를제안하지않는다.

## 6. 증상별 관찰·수리 초안

다음은안전절차와접근권한을갖춘담당자가수집할관찰설계다. 활선접촉·배관개방·압력주입·우회/강제출력을지시하지않는다. 실제수리기록은없다.

| 증상 | 같은시각에기록할항목 | 원인구별/비교근거 | 복구판정에필요한증거 |
|---|---|---|---|
|HMI값−9999|PR_BR02원시값,DB1.W242,DB3.X24.5,ON,계수,모듈진단|0291범위밖대체값과실제음압구별;취출관/계기전원/아날로그루프상태는승인절차로검사|정상범위raw·OFR·독립차압기준·시간추세,센서/배선확인|
|HMI값항상0|원시%IW400:P,ON/호출,DB4.W120/W122,DB1.W242,HMI주소|0014 NOT IN0의0쓰기·통신표시·실제0차압을구분. EN=OFF일때함수실행을가정안함|동일시각CPU/표시/독립기준의일치와호출근거|
|값크기/단위이상|현재계수와백업0/500,채널범위,센서0/50mbar명판,HMI소수점|분모28000·Zero더하기·DInt/Int변환을대조;계수를임의변경안함|승인된스케일/교정문서와단위변환표|
|BF02정상인데MAX_DP발생|DP01/DP02둘다,공유T114,3분지속기록,OFR들|공유OR라서DP02단독원인으로단정안함;비트Reset과하한정상구별|두채널정상범위·원인제거·경보재발없는관찰|
|차압낮은데세정허가이상|DP02,DP01_S1,SC11/VR05처리응답,Forza,ON,BF02_RUN|0219의DP01명임계값·≤비교·Forza병렬·상위직렬대조|허가와실제세정·차압회복을별도관찰|
|DP02무응답/배선혼동|FG169 X3:95~99,FG17234/36,JB01TB6현장마킹,설계4케이블|BF02설치와JB1공급을구별. DP01채널6/398와DP02채널7/400대조|승인준공도·담당자확인·무전원검사기록/교정기록|

각기록에관찰자·시각/시간대·위치·값/단위·수집장치·프로젝트/CPU근거·비교원본·배제결과·승인조치·복구근거를남긴다. 0과빈칸,미지필드·이전근거·다른설비·초안·저장키를보존하며사용자운영사진/이력을공개Git에복제하지않는다.

## 7. 완료·누락·검사·인계

### 7.1 남은자료와판정

1. 센서명판/제조사매뉴얼/교정성적서,고저압취출및현행준공접속표:0/50mbar범위와극성·전원·출력기능을현물검증한다. 모델·정상극성·정비주기·토크·교체품을지어내지않는다.
2. 현재TIA프로젝트/하드웨어구성/AI채널파라미터와현재CPU비교:Peripherie주소400,채널7,계수·현재값·보존속성·범위오류/ENO·폭변환·실제호출을권한하에별도검증한다. 이번에추가접근권한없음.
3. HMI원본객체/이벤트/알람정의:설정주소만아닌실제화면·단위·쓰기경로·확인행위를확인한다.
4. 공유경보의정지·호른·추가소비자전체경로,간접/통신/Word쓰기목록:단순태그검색의한계를해소한다.
5. 새현장자료없는동일보류반복조사하지않고DP02의문서누락으로보존한다.

### 7.2 네기능/완료상태

| 기능/상태 | 결과 |
|---|---|
| 도면·래더 비교 | 연결할원본쌍0522/FG169·172,0291/0611·0612 제시; 실제UI미구현/미검증 |
| 백업·선택복원 | 사용자기록조작없음,저장/재읽기/재열기미수행 |
| 기록전후비교 | 위관찰스키마설계뿐,기능/격리QA미수행 |
| 보고서/PDF | 이MD와원본렌더근거작성;관찰보고서생성·앱PDF미검증 |
| documentation | complete_with_gaps,자체초안 |
| static_review | selected_original_paths_checked,자체정적대조완료;별도독립검토대기 |
| ui_records | not_run |
| publication | not_published,통합/버전/새커밋없음 |
| tia_compile / live_cpu / field_recovery | 모두not_performed |

### 7.3 실제작업시각·수행검사

- 2026-10-11 10:28:33 UTC:배정수신·묶음지시읽기착수.
- 10:28:36~10:28:49 UTC:표준/고정상태/대장·공유BF02근거확인. Gitstatus출력변경0.
- 10:28:53~10:30:15 UTC:XML파싱·핀/선언·계수/HMI·도면6페이지렌더와시각대조. 이는관측된실제도구호출시간이며예상소요시간이아니다.
- 10:30:57 UTC:98개원본파일SHA256와고정Git blob전체일치·중지5freeze일치검사.
- extract.py는읽기전용XML파싱후이설비출력폴더에만추출한다. 원본build/test/generator/preflight·시뮬레이터를실행하지않았다.
- 독립핵심대조네트워크는0014/0291/0522/0540/0219/0200/0199/0201/0031/0148의10개선택경로다. 공통BF02근거목록의98파일해시검사는98개파일전체의미검토가아니다. 전체바이너리·PDF전페이지·모든EV를검토했다고세지않는다.
- 자체검사결과와최종시각은extracts/DP02/verification.json. 이검사는독립검토·TIA동작시험을대신하지않는다.

원본내용을수정한완료커밋은없다. 다음한작업은DP02초안의독립검토(특히DInt→Int Move/ENO·단위미확정과JB1소유경계)다. 사용자첨부/전송은부모가수행한다. 신규원본이나현장증거가생기기전에는현재보류를완료로바꾸지않는다.

## 부록 A. 고정 원본 SHA-256와 Git blob 전체 목록

98개 바이트 일치. BF02 공유 근거 목록을 보존 검사용으로 재사용하고 DP02 고유 환산 원본4개를 추가했다. 이 수는 의미 검토 수가 아니다. 모든 행은 고정 commit `abcf31c5030bc7ef8749ed8e869a857f2387a28a`의 blob 내용 SHA-256과 일치한다. 중지5자산은 freeze 명세와도 일치한다. 원본 기준 URL: https://github.com/esp6662266/gme-plc-manual/tree/abcf31c5030bc7ef8749ed8e869a857f2387a28a

| 원본 상대경로 | SHA-256 | Git blob |
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
| all-in-one/sources/decoded-original/0014-FlgNet.xml | 2e814adbaac6bab99bc668bfdab74f0fc90576324d0b88728951683869cfac30 | 4d164b074fcc13a8f97da9e24382cc169ef29555 |
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
| all-in-one/sources/decoded-original/0291-FlgNet.xml | fe0b92f074eba25148ce34084649af3d968962558d652727f1eea19f3e3c2550 | 1418fb2ed172c6df694a5eb8bf2dffd0b177653b |
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
| all-in-one/sources/decoded-original/0611-IdentXmlPart.xml | 0d583915a261703954da22c176ba9f81338ad13ea2810e7cd5f7de8aa1bfa089 | bad6b16fb32a32d47d882f48754994887457872b |
| all-in-one/sources/decoded-original/0612-IdentXmlPart.xml | 95b545d4964d371ebfc107894ea90b8b1d0d7ab5d3a70e643f8ce539063c0f38 | 7cc782d33d07ef225c2104f3e7c9fbd31f7c7467 |
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
