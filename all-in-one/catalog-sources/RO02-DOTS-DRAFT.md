# RO02 산소 분석 채널 — 독립 원본 조사 초안

고정 읽기 원본: `gme-research/source-mv06`, Git `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, 프로그램 v1.12.0. 문서조사만 수행. 2차133 로컬 통합 제외를 유지하며 RO01/RO03/RO04·BR01·PV05/PV06 완료를 함께 집계하지 않는다. 실행 모델/추론 런타임 증명은 미확인. TIA 추가 접근·현재 CPU·현장 자료 없음.

## 먼저 볼 핵심 인계

- RO02 고유 입력은 R002=%IW354 Int이다. 환산 호출 0499/LAD1749는 **Peripherie 접근**, HMI 미러 0398/LAD1071은 **SAM=None 입력 접근**이다. 같은 주소라도 취득 경로와 갱신시점이 같다 단정하지 않는다.
- 0499는 OFF(M0.1) 접점으로 호출을 허가하고 별도 IN0에 ON(M0.0)을 연결한다. OFF라는 이름만으로 실행 불가능한 코드라 지우거나, startup 원문의 `clr s off`를 Reset으로 바꾸면 안 된다.
- 환산 결과 Data.Oxigen_RO02=DB1.DBW128(Int), 원시 미러 Inputs.RO_02=DB13.DBW70(Word), 범위오류 Allarm.RO02_OFR=DB3.DBX22.4(Bool)는 세 신호다. HMI에는 원시 I_RO_02 외에 data_DB1_DBW128도 존재한다.
- 0533/LAD1985는 RO01−RO02 Int 차이를 비교하며 ±20 밖·S5T#1M 경로가 **RO01_Signal_Fault**를 Set한다. 이름에 RO01이 있어도 비교 상대 RO02를 누락하면 안 된다. 실제 산소%·안전 한계로 20/650을 해석하지 않는다.
- 비교 알람의 BR01 영향은 0175의 Flag.Start_Burner Reset 가지까지 결속했다. RO02_OFR 자체를 동일 정지식으로 바꾸지 않는다. 질소 PV05/PV06은 별도 공통 출력과 외부 릴레이·타이머 회로이며 RO02가 직접 밸브를 연다는 경로는 확인하지 못했다.
- RO02 값은 0500에서 RO03 대체 Add 입력에도 쓰인다. `Data.RO03=Data.Oxigen_RO02+11` 쓰기이며 RO02에 +11을 쓰는 것이 아니다. 같은 네트워크의 RO03 환산 출력과 이중 쓰기를 구분한다.

### 상충·누락·공유 근거 구분

1. OEM FG80/PDF81는 80RO-02, OXIGEN OUTLET AB-01/SMOKE SAFETY DETECT를 표기한다. 시공 PDF56은 81RO-02(MV-03)에서 RO-2(HE-01)로 이어지는 케이블을 표기한다. 명칭/위치가 다르므로 실물 동일성·현행 개조를 확인할 때까지 병합하지 않는다.
2. HMI CSV는 dde.cfg에서 정리된 고정 설정 근거다. 실제 화면 오브젝트·입력 이벤트·쓰기 권한·읽기전용 여부·현재 값·HMI 산소 표시 스케일은 미확보다.
3. COEFF_R02/ZERO_R02의 현재 값과 산소 단위, H705 현행 명판·설명서·교정 성적, 센서 정상 극성, 현재 안전 설정, 복구 증거는 없음. 당초 도면 표기만 보존한다.
4. BF02 초안을 공통 ON/OFF·startup/Word 및 XML 대조 방법의 인덱스로 참고했다. 이번에 동일 원본 해시를 재확인하고 RO02 고유 0499/0398/0533/0500, 선언, OEM 2쪽과 시공1쪽을 직접 검토했다. 공통 환산0291/0014·호출0030/0031·startup0148도 원문을 다시 읽었다. 다른 설비의 항목 수·주소·계수·알람을 복제하지 않았다.
5. 추출기의 RID/UID/NID 검색은 다른 블록의 동일 숫자를 함께 잡을 수 있다. 본문 판정은 원래 블록의 선언 묶음으로 제한했다. 예: 0291 ORef41/RID25는0612의 -1382이며0631 Allarm1이 아니다; 0175 ORef249는0582 ON이며 다른 블록 Data가 아니다. 0148은 색인 NID 투표가 혼합되지만 startup0047/0048/0562/0563 및 doc403으로 NID3을 대조한다.

## 1. 설비·자료 기준

| 항목 | 적용과 원본 근거 | 미확정 경계 |
|---|---|---|
| 식별 | INVENTORY catalog[9] RO02, sensor/계측, parent=null, phase2 planned. 별칭 r0-02/r002/r0_02는 배정 scope 및 equipment 자료의 탐색 키 | 동일 이름 RO01/RO03/RO04는 별도 ID. 실물 일치 완료 아님 |
| 소유 | 센서소자→80RO-02 H705→PEW354→PLC 환산·비교 경로. BR01과 질소밸브는 관련 소비자/별도 소유 | RO02 자체 구동 Q·밸브 동작·버너 내부 안전시퀀스 발명 금지 |
| 원본 시점 | 전기 시트 27.05.2024, 시공24.11.11 first draft design, PLC GME_20250506.zap18 고정 백업 | 최신 설치/운전 프로젝트임을 증명하지 않음 |
| 작성 경계 | RO02 문서·선언·핀·전기 원문 정적 검토 및 누락 인계 | 기존 코드·대장·버전·게시·운영기록·SEJIN 자료 변경 없음 |

이 초안은 7영역 모두 적용하되 관찰·기능·현장 검증은 별도 미수행이다. BC01의36항목 등 수량을 목표로 삼지 않았다.

## 2. I/O·HMI

### 2.1 원본 선언과 주소

이하 XML 축약번호는 `all-in-one/sources/decoded-original/NNNN-IdentXmlPart.xml` 또는 `NNNN-FlgNet.xml`이다. AO/BO는 비트 오프셋이다. DB 번호는 BAD→DepDBBlock/TOD로 연결했다.

| 신호 | 형식·고정 주소 | 선언 및 사용 결속 | 해석 |
|---|---|---|---|
| R002 환산 입력 | Global Int, %IW354, SAM=Peripherie |0678 RID116 AO2832 SAD Input; NID19 UID524|직접 주변장치 읽기 지정. %IW 단어만 보고 HMI 미러와 동일 취득으로 취급하지 않음|
| R002 미러 입력 | Global Int, %IW354, SAM=None |0627 RID117 AO2832; NID2 UID154|0398 Move147.in 원천|
| Inputs.RO_02 |Global Word, DB13.DBW70|0629 RID118 AO560 BAD4→0628 Inputs TOD13; NID2 UID155 AK Write|HMI용 원시 저장, 산소 환산 결과 아님|
| Coeff.COEFF_R02 |Global Int, DB4.DBW50|0676 RID117 BO400 BAD8→0674 Coeff TOD4; NID19 UID525|현재 계수 미취득|
| Coeff.ZERO_R02 |Global Int, DB4.DBW48|0676 RID118 BO384 BAD8; NID19 UID526|현재 영점·부호 미취득|
| Data.Oxigen_RO02 |Global Int, DB1.DBW128|0676 RID119 BO1024 BAD11→0674 Data TOD1; NID19 UID527 Write/NID20 UID579 Read;0684 RID67 NID7 UID701 Read|환산 결과, RO03 대체와 비교 소비|
| Allarm.RO02_OFR |Global Bool, DB3.DBX22.4|0676 RID395 BO180 BAD354→0674 Allarm TOD3; NID19 UID23 Write|환산 함수의 범위 오류 출력|
| RO01-RO02control disable |Global Bool, M80.1|0686 RID65 AO641; NID7 UID697|0533 NOT 접점. 현재 상태 미확인|
| Allarm.RO01_Signal_Fault |Global Bool, DB3.DBX4.4|0684 RID72 BO36 BAD10→0682 Allarm TOD3; NID7 UID710 Set/713 Reset;0585 RID39 NID5 UID244 Read|두 채널 비교 알람; RO02_OFR와 다른 비트|
| Tag_107 |Global Timer T117|0686 RID71 AO117 SAD Timer; NID7 UID708 Write/709 Read|S5 delay용 PLC 타이머. HMI 태그 아님|
| Flag.RESET_ALLARM |Global Bool DB2.DBX6.0|0684 RID24 BO48 BAD15→0682 Flag TOD2; NID7 UID711|오류 원인 제거·재기동과 구분|
| Manage_TC1_2.PID_Ref_Temp |Global Real DB39.DBD2|0684 RID169 AO16 BAD168→0682 TOD39; NID7 UID698|RO01/RO02 비교 경로의650.0 비교 상대|
| Flag.Start_Burner |Global Bool DB2.DBX5.2|0585 RID19 BO42 BAD7→0584 Flag TOD2; NID5 UID250 Write|버너 요청 메모리 Reset 대상; 연소기 실제 정지 피드백 아님|
| ON/OFF |Global Bool M0.0/M0.1|0678 RID1/RID34 AO0/1; startup0047 및 live_index doc401|이름으로 실제 값을 단정하지 않음|

### 2.2 HMI 전달과 태그

0398/LAD1071 hmi inputs/NID2: W166 ORef154/RID117(R002)→Move147.in; W167 Move147.out1→ORef155/RID118(Inputs.RO_02). 앞단 Move146.eno→Move147.en은 W164이다. DisableENO 속성과 전체 Move chain이 있으므로 원시 값이 매 주기 반드시 갱신된다는 판단은 현재 호출·실행 확인 전 보류한다. 0030 main/LAD1613/NID19의 CRef25(HMI Output).eno→NOT Simulation(1) Part37→CRef28(HMI Inputs).en(W42/43), CodeBlock29/RID135가 호출 근거다. 중지된 시뮬레이터의 실행/행동 검증은 하지 않았다.

`all-in-one/sources/hmi_plc_tags.csv`에서 직접 확인한 설정:

| 행 | HMI명 | 설정 | 내부 ID |
|---:|---|---|---|
|773|I_RO_02|DB13,INT70 / PLC|0002F|
|381|data_DB1_DBW128|DB1,INT128 / PLC|001E8|
|217|Coeff_DB4_DBW48|DB4,INT48 / PLC|002C0|
|305|Coeff_DB4_DBW50|DB4,INT50 / PLC|0024C|
|348|Allarmi_218|DB3,X22.4 / PLC|00219|
|494|Allarmi_37|DB3,X4.4 / PLC|00168|

PLC 미러 선언 Word와 HMI INT 해석 차이를 보존한다. HMI의 DB1W128 태그 존재와 실제 화면 연결은 다르다. 이6행은 관련 주소 대응표이며 화면6개·알람6개·제어기능6개를 뜻하지 않는다. 설정명만으로 계수 입력 이벤트나 쓰기 권한을 부여하지 않는다.

## 3. 제어 구조·환산·다중 쓰기

### 3.1 호출과 RO02 고유 결속

0031/LAD1619 main/NID6: ON Part282.out W283이 CRef261(Analog input conversion),264(Allarms1),267(Allarms2),270(Allarms3)의 en으로 분기한다. 각 호출이 ENO 직렬이라는 설명은 틀리다. CodeBlock273/RID55·279/RID64는0688 선언에 AK Call이며 현재 실행 순서/주기/최종값은 정적 index만으로 확정하지 않는다.

0499/LAD1749 analog input conversion/NID19 원문:

| Part/CRef·핀 | Wire | ORef/RID·선언 | 의미 |
|---|---:|---|---|
|Contact535.operand|529|522/34,0678 OFF|호출 허가 접점, NOT 없음|
|535.out→CRef516.en|536|—|OFF 조건으로 FC호출|
|516.IN0|530|523/1,0678 ON|함수 내부 허가, 외부 en과 별개|
|516.Analog_input|531|524/116,0678 R002|Peripherie Int|
|516.Coeff / Zero|532 /533|525/117,526/118,0676|RO02 고유 DB4W50/W48|
|516.OutValue|534|527/119,0676|DB1W128 Write|
|516.Out_of_range|24|23/395,0676|DB3X22.4 Write|

CRef516 RID351→0680 BlockInterfaceInfo, CodeBlock528 RID5→0672 Signal linearization TOD63/FC, NID19 AK Call. 호출이 성립하지 않은 경우 새 값이 생성되는지/외부 쓰기가 있는지 현재 CPU 없이 확정하지 않는다.

### 3.2 공통 Signal linearization 원본 정적 해석

0291/LAD1658 NID1 +0014/LAD1659 NID2, 선언0611/0612를 원문으로 대조했다. IN0/Analog_input/Coeff/Zero/OutValue/Out_of_range는 **Local interface**이며 RO02 전역변수와 같지 않다. App3/App4/App5/App6는 Local DInt 임시값이다.

- IN0 접점255 뒤 Gt258(Analog_input > -1382), Le161(<=32767)을 직렬 검사한다. Wire30/31/25/27/28/26, RID3/25/29. Int 입력이므로 상한 비교의 타입 한계도 보존하며 이 구간을 승인 계측범위로 해석하지 않는다.
- Convert164(Int→DInt)로 App5, Convert167(Zero Int→DInt)로 App6, Add170(DInt)로 App3, Convert174(Coeff Int→DInt)로 App4, Mul177(DInt), Div181(DInt,28000), Move185→OutValue Int. 각각 en은 앞 연산 eno(W227/230/234/237/241/245)와 연결된다. 정적 산술 의도는 (raw+zero)×coeff/28000이나 정수 연산·오버플로·DInt→Int Move 경계가 있으므로 실수식/산소%로 치환하지 않는다. 분모28000을27648로 정정하지 않는다.
- 범위 밖은 Gt190(>32767) OR Le259(<=-1382)→O47→Move193(-9999)→OutValue; **Move193.eno W21→Coil23**가 Out_of_range를 쓴다. 비교 OR 자체가 직접 OFR 코일이라고 단순화하지 않는다. 정상 분기·IN0 FALSE일 때 ENO 및 출력 전달의 실제 실행 의미는 TIA 컴파일/현재 CPU 확인 전 보류한다.
- 0014는 NOT IN0 Part171→Move162(0)→OutValue(ORef167/RID19,W170)다. 이것은 함수 호출 자체가 꺼진 경우와 다르며 Out_of_range를 함께0으로 Move하는 네트워크가 아니다.
- startup live_index `_7ev` doc401 원문은 `set s "on" clr s "off"`이다. OFF Reset 명령으로 바꾸지 않고, 현재 OFF=FALSE·RO02 환산 항상 비활성으로 확정하지 않는다.

### 3.3 RO03 대체 가지 및 쓰기 범위

0500/LAD1750 NID20: OFF Part594.out W595는 RO03 환산 CRef558.en과 OFF Part596.in으로 분기한다. Part596.out W597→Add566.en, ORef579/RID119(Data.Oxigen_RO02) W590→in1, 580/RID126(Int11) W591→in2, W592 Add566.out→581/RID124(Data.RO03). RO03 환산 OutValue→576/RID124 W587도 별도 쓰기다. 이것을 RO02 보정 +11이나 RO03 독립 실물 확인으로 설명하지 않는다. RO02 값을 읽는 또 다른 경로는0533 비교 입력이다.

직접 이름/주소 선언 검색에서 DB1W128 직접 Write는0676 NID19 UID527, DB13W70는0629 NID2 UID155, DB3X22.4는0676 NID19 UID23을 확인했다. 이는 검토한 공개 직접선언 결과다. 외부 HMI/통신·간접주소·전체 DB 전송·온라인 강제의 부재 증명은 아니다.

## 4. 전기 끝점·개정·시공 상충

### 4.1 OEM RO02 전체 체인

Electrical_Rev2.pdf **실제 PDF81/FG80**, 제목 OXIGEN CONTROLTRANSMITTER RO-01/RO-02; footer DATA27.05.2024, DESIGN G.G., NORMA IEC, TOT262. 개별 시트에는 별도의 Rev2 개정행이 보이지 않아 파일명만으로 이 시트 Rev2라 하지 않는다. 실제 렌더를 확인했다.

| 구간 | 도면 양 끝점 | 의미·누락 |
|---|---|---|
|센서→변환기|RO-02 +S/−S/−T/+T→80.7/80.8/80.9/80.10→80RO-02 1+/2−/3−/4+, shield80SCH4|4선 프로브 체인. 선 색/현재 실물/교정 미확인|
|AC 전원|110Vac9.8(16/9)→X1:214 5×20 2A F→80.6→단자15; 단자16→X1:215→0Vac9.9; 단자17 GND|도면110Vac와 보호 표기일 뿐 현재 전원·퓨즈 권장값 아님|
|아날로그 출력+|H705 7+→X1:216→+PEW354(110/3)|4–20mA 표기|
|아날로그 출력−|H705 8−→X1:217→−PEW354(110/4)|+/− 선로, PLC 정상값/산소단위 아님|
|쉴드|X1:218→80SCH3(110/3)|실물 접지 방법 미확인|

Electrical_Rev2.pdf **실제 PDF111/FG110** ANALOG INPUT MODULE, footer DATA27.05.2024/G.G./IEC/TOT262. CPU515/MOD5의 PEW354 채널에서 +PEW354→**6 I1+**, −PEW354→**8 U1−/I1−**, 쉴드80SCH3. 단자5 Uv1/7 U1+를 신호 입력6/8로 바꾸지 않는다. MANA18은 도면 −0Vdc10.6에 연결된다. 이것은 도면의 CPU515 표기이며 현행 CPU모델을 확인한 것이 아니다.

### 4.2 시공 케이블 문서와 불일치

Electrical_Can_Decoating_20241118.pdf 실제 **PDF56**, footer CANDC-CONS-C006-056, Cable Schedule(5), D-PAGE6/TOTAL56/64, 개정행1 `24.11.11 first draft design`, traced J.W.Lee/designed J.H.Kim, checked/approved 빈칸을 렌더에서 확인. 승인 준공도라 부르지 않는다.

|행|케이블 번호|FROM→TO|원문 사양·길이|
|---|---|---|---|
|6_5|=FLA+MV03-81RO02A|CR→MV-03/81RO-02, PEW354|AI CVV-S 2S 1.0, spare0; route100LBD1/E800; adjustment9,LEN47|
|6_14|=FLA+MV03-81RO02B|MV-03/FLO1TB1→MV-03/81RO-02 AC|AC CVV 3G 1.0, spare0; LAD1 E400/LBD1/LAD1 E900; adjustment3,LEN4|
|6_22|=FLA+HE01-RO02A|MV-03/81RO-02→HE-01/RO-2|AI CVV-S 4S 1.0, spare0; LAD1 E1000/100LAD1/100LCD1/E800; adjustment15,LEN16|

원문 길이 칸 단위는 이 표만으로 덧붙이지 않는다. OEM의80RO-02와 시공81RO-02, AB-01 출구 설명과 HE-01 현장 태그 사이의 대응을 현재 도면으로 확정해야 한다. PEW354 공통 표기가 연결 후보를 강하게 뒷받침하지만 승인 없는 현행 동일성 증명은 아니다.

### 4.3 질소 밸브는 별도 소유

Electrical_Rev2.pdf 실제 **PDF97/FG96** NITROGEN VALVES BOX PV-05/PV-06, footer27.05.2024/G.G./IEC/TOT262를 직접 확인. A6.4(142/1)가96KA3 코일 A1, A2는−0Vdc10.6이며, 96KA3 **부하접점5–9**는 X1:368/369·X2:11/12 사이에 그려진다. 하단 접점표의1/5/9와 실제 부하5/9를 구별한다. PV05는 X2:13/14, PV06는 X2:15/16·96KT1 접점15/18 경로를 사용한다. 외부110V회로·비상버튼·96KA1도 포함되므로 Q 하나를 PV05/PV06 개별 직접 출력이라고 하지 않는다.

live_index `_7ev`1059는 start nitrogen=%Q6.4 Bool(옛 설명 a60.5),351은 Output 인터페이스 이름 목록이다. 검색한 FlgNet에서 RO02→start nitrogen Write를 직접 결속하지 못했다. 따라서 질소 자동 주입이 RO02 임계값으로 기동한다고 쓰지 않으며 Q6.4 생성 논리·외부박스 현행 회로는 별도 조사 대상이다. 이 자료는 RO02와 관련 계통 소유 경계를 설명하는 것이며 PV05/PV06 독립 완료가 아니다.

## 5. 알람·복구와 영향

### 5.1 RO01−RO02 비교 원본

0533/LAD1985 allarms3/NID7,0683 상수·0684 Global·0685 Local·0686 SimpleAccess 결속:

1. ON Part741→NOT RO01-RO02control disable Part743(W742/715/744)→Gt663 Real(Manage_TC1_2.PID_Ref_Temp,650.0; W716/717). 650.0은 해당 Real 기준이며 RO02 산소 임계값이 아니다.
2. Gt663.out W718이 Sub669.en, Lt676.pre, Gt679.pre에 분기한다. Sub669는 **Int** in1=RO01(ORef700 W719),in2=RO02(ORef701 W720),out→Local app01(ORef702 W721,0685 RID68 AK Write). 비교는 Sub.eno 직렬이 아니므로 오버플로/스캔 의미를 실수 절대값 비교로 바꾸지 않는다.
3. app01<−20(Lt676,W722/723) OR app01>20(Gt679,W725/726)→O675→SdCoil685.in(W728), value=S5T#1M(ORef707 RID46 W729),operand=T117(ORef708 RID71 W730).
4. 같은 W728은 Contact745.in으로도 가고 T117(ORef709 W731)을 거쳐 SCoil690→Allarm.RO01_Signal_Fault(ORef710 RID72 W733). 차이 조건과 타이머 접점이 모두 필요하다. 정확히±20은 이 비교식에서 범위 밖이 아니다. 이 상수는 백업 코드 사실이며 운전/안전 권장값이 아니다.
5. 별도 Reset 가지: ON→RESET_ALLARM Contact747→알람 자체 Contact749→RCoil695(ORef713 W739). Reset에는 현재 차이 정상이나650 이하라는 추가 접점이 없다. Set와 Reset이 동시에 참일 수 있는 구조를 보존하며 실행 순서/재Set/현장 복구 완료는 미확인이다.

### 5.2 버너와 공통 Word 경계

0175/LAD1858 burner control/NID5: RO01_Signal_Fault=0585 RID39 UID244→Contact295 W262→O219.in7 W296. O219.out W267→ON Contact305(0582 RID1 UID249)→O213.in5 W306→RCoil232→Flag.Start_Burner(0585 RID19 UID250 W272). 앞쪽 ON Part273 허가도 있다. 이것은 여러 이상 중 한 가지가 **버너 요청비트 Reset**에 참여함을 뜻한다. 외부 버너 점화·퍼지·연료차단 내부 동작이나 실제 정지 응답을 입증하지 않는다. 요청에는 다른 Set/Reset 원천이 있으므로0175만으로 유일 최종 Writer라 하지 않는다.

0148 startup/LAD403: ON→Move250/253/256/259 등으로 DB3 Word0~16을0으로 쓰는 원문. 비교 알람 DB3X4.4는 DB3W4 범위에 들어간다(Move256.out1 W311→ORef290/RID28,0563 AO32/BAD23→0562 Allarm TOD3의 DB3W4; 입력289/RID54는0048 Int0). **RO02_OFR DB3X22.4는 이 Word0~16 범위 밖**이다. 시작 시 모든 RO02 관련 알람이 지워진다고 확대하지 않는다. 0151/0152 공통 경보 관리자 Word 읽기·보관/비교는 개별 RO02 원인과 다른 공통 기능이다. 전체 경적·램프 소비경로 및 HMI 알람문구의 일대일 원문 결속은 미완료다.

0538/LAD1990은 질소탱크 준비 Inputs와 ServiceBit로 HYDROGEN_BOX_FAULT를 Set/Reset한다. 태그의 HYDROGEN 명칭을 RO02 산소 오류로 바꾸지 않는다. RO01 자체 산소 상하한 0530~0532는 별도 RO01값을 읽는 가지이며 이 초안의 RO02 직접 알람으로 복제하지 않았다.

### 5.3 복구 판정의 경계

범위 복귀, RO02_OFR 변경, 비교 알람 Reset, 버너 요청 재생성, 버너 실제 응답, 질소 밸브 실제 닫힘/열림은 서로 다른 확인이다. 실제 운영 조작·Reset·강제·보호 설정 변경·시험은 하지 않았다. 원인 제거 없이 단순 비트 해제를 복구 완료라고 기록하지 않는다.

## 6. 증상별 관찰 설계

아래는 안전한 읽기 관찰의 다음 항목이며 실제 관찰 기록·정비 지시·실행시험이 아니다. 전기 측정은 권한 있는 현장 담당자가 승인된 절차로 수행해야 한다.

|증상|같은 시각에 기록할 위치/값|대조와 원인 구분|복구 확인에 필요한 증거|
|HMI 원시값은 변하나 산소 결과 정체|H705표시·PEW354·IW354·DB13W70·DB1W128,ON/OFF와호출상태|Peripherie와이미지,미러와환산,OFF en과IN0를구분|동일프로젝트/타임스탬프에서호출·계수·값갱신 결속|
|RO02_OFR 또는 −9999|원시 Int,COEFF_R02/ZERO_R02,FC 출력/OFR|입력범위비교와Move.eno를나눠확인; 배선/전원/변환기표시와비교|원인별자료와범위복귀·출력/OFR 동시관찰|
|RO01_Signal_Fault 발생|RO01/RO02,Local app01에대응한진단값,T117,M80.1,DB39.DBD2,Reset|±20밖조건·1분지연·disable·온도참조를구분;단위가틀린채널비교가능성보류|차이원인해소·Reset/재발·버너요청·외부응답 분리기록|
|RO03 표시가RO02와연동|RO02,RO03,0500호출상태및두Write경로|+11쓰기대상은RO03; 독립센서결과인지대체인지현재활성경로확인|현재프로젝트와실제읽기값,화면표시경로|
|산소오류와버너/질소동작이동시발생|RO02_OFR,RO01_Signal_Fault,Start_Burner,Q6.4,탱크준비와외부상태|시간적동시성은인과증명아님;0175와FG96소유분리|버너요청·현장응답및별도질소명령근거;미확인시보류|
|도면과현장태그불일치|80RO-02/81RO-02 명판·설치위치·X1단자·케이블6_5/14/22 표찰|OEM80/시공81,AB출구/HE위치상충유지|현행승인도면·개조이력·사진·점검자서명|

기록 필수 필드: 관찰자/UTC와현지시간대/장치·위치/태그·원시와환산값·단위/프로젝트·CPU버전 근거/비교원본/원인배제/승인조치/후속결과. 0과빈칸·미확인을구별하며 사용자 운영기록이나사진을 새 공개자료로 복제하지 않는다.

## 7. 완료·누락·다음 인계

|구분|이번 상태|남은 자료/판정|
|documentation|complete_with_gaps, 자체 원본초안|부모 독립검토 전이며 로컬 매뉴얼 통합완료 아님|
|static_review|selected_native_paths_reviewed|핵심 XML·선언·4 PDF페이지 직접검토, 보존해시 일치. 전체 프로그램/간접쓰기 완전증명 아님|
|ui_records|not_run|도면·래더 비교,백업 선택복원,전후비교,보고서PDF의 RO02 구현/저장·재열기 미검증|
|publication|not_published|이 초안 외 코드·버전·배포 미변경|
|tia_compile|not_performed|로컬TIA 접근권한없음|
|live_cpu|not_performed|현재프로젝트·CPU/강제/DB현재값없음|
|field_recovery|not_performed|현재배선/명판/교정/설정/복구관찰없음|

다음 한 작업은 부모가 이 초안의 **0533 차이알람→0175 요청Reset·HMI 원시/환산 주소분리·80/81RO02 시공상충**을 독립 재검토하는 것이다. 현장 자료 없는 미확정은 추정하지 않고 보류한다. 원본/대장/버전/운영기록/SEJIN/보호값은 유지했고 simulator/build/test/generator는 실행하지 않았다. 원본 byte hash 검사는 문서·XML 자체 파싱과 Git blob 비교이며 제품 시험이 아니다.

## 부록 A. 실제 작업 단계 시각과 검토 범위

- 2026-10-11 10:40:22 UTC: 배정 수신 후 공통지시·scope 읽기 시작.
- 10:40:26~10:40:44 UTC: AGENTS/표준/템플릿/INVENTORY/버전·인계, 기존 BF02 인덱스 확인.
- 10:40:44~10:41:23 UTC: RO02 고유 원본 검색, 선언·0499/0533/0291/0398 등 XML 자체 추출 및 의미검토.
- 10:41:30~10:41:43 UTC: OEM PDF81/111 실제 렌더·footer·RO02 양 끝점 확인.
- 10:42:00~10:42:40 UTC: HMI·startup·질소경계·시공 검색, PDF97/시공56 실제 렌더 확인.
- 10:42:49~10:43:33 UTC: 호출·startup Word/공통 알람·선언충돌 보강.
- 10:43:58 UTC: 선정 원본 SHA256/Git blob/중지5 보존검사 최초 성공. 최종 검사시각은 아래 검사 부록에 실제 결과로 기록.

직접 의미검토 핵심:0499 RO02환산,0398 원시전달선택가지,0291/0014 공통함수,0500 RO03대체가지,0533 비교알람,0175 버너요청Reset가지,0030/0031 관련호출,0148 startup Word4선택가지.0151/0152/0538는공통소유경계선택검토;0530~0532/0185는인덱스·참조읽기이며RO02핵심의완전해석수로세지않는다. PDF4쪽은81/111/97및시공56. 실제 부하핀 검토는본문 명시범위다.

## 부록 B. 전체 원본 바이트 해시표

선정한 원본·기준·파생색인·중지 자산 78파일 모두 고정 Git blob 내용과 SHA256 일치. 중지5자산은 freeze 명세와도 일치. 이 수는 의미검토한 네트워크·페이지 수가 아니다. PLC 바이너리는 보존검사이며 전체 의미검토가 아니다.

기준: https://github.com/esp6662266/gme-plc-manual/tree/abcf31c5030bc7ef8749ed8e869a857f2387a28a

| 원본 상대경로 | SHA256 | Git blob | 내용일치 |
|---|---|---|---|
| .agents/skills/gme-equipment-rollout/SKILL.md | fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b | 9aa820ea6ca15b4e136c9772423b78ed4df6a3d4 | 일치 |
| AGENTS.md | 0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2 | 073164bc6efd5791032d62c71b03b4dab48cb6f8 | 일치 |
| EXPANSION-WORK.md | ec624de9fd2fcfac861a67fd5e828b25ef46db50bfd7a37ff16e2cb54cd0f7e2 | 4c42d88ecc2d48269eb23e13a20ebf3721a092a1 | 일치 |
| PUBLICATION_STATUS.md | efe4857aec598d90470322cf3962eb3fe1f64947630e1fdf71d1c90134de8740 | d76401cf291fc0be681acc51fa898ad3ce46ff78 | 일치 |
| VERSION.json | 5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7 | fffb51663b7705aec91cb119ca80ee943a4ce758 | 일치 |
| WORKSPACE-HANDOFF.md | 215096d997782e78e901dfae36c782937e49611fbeb677a0d3fa50cbecf8d074 | dd0b8989d2376c4415bba9bd826fe6754c6b1a12 | 일치 |
| all-in-one/ACTIVE-WORK.md | eff3bbc08ecff41da3beff77f3fec48e7d148708192bcaaab00f34b6a721afc2 | 6eb947c629b5ddf9c759ef87649451303938864b | 일치 |
| all-in-one/assets/program-model-data.js | 52f8199371e3399b7c0d44ab5469f0472aced79d56bbef2887f7625f5d2aff0f | 38f34b0caa380a16ccad6f6f1e234a2fdf23f327 | 일치 |
| all-in-one/assets/simulator-workspace.js | 3a6dfc618ff7e7b238f2671dc85d65704f33093a18eac879d86081d92c31e8bc | 97c2c831c77a9699fff0e0960b3bc1b7d93d45b3 | 일치 |
| all-in-one/assets/virtual-plc.js | 5f1876052dc0067b1f010af0dfc941946e37003167481731293615d9c1c36dbc | 0bd9eceb54365a91214a37c5601b5067c39a3f75 | 일치 |
| all-in-one/registers/equipment.csv | 725cebc853bf1c50f84ff32121ae3a0ab5872809ffef67bd47766199ee83e35f | 5e2dd2d2d27d65d90bf6e4c9836b81d2959c7a7a | 일치 |
| all-in-one/registers/program-model.json | 6203479c086b15bada12ac9d7e37db9280234ec26f1ea6091d7211dc09a577c5 | 9860b10f008d3a5ae714be50d77b703dfec32f3a | 일치 |
| all-in-one/registers/sensor-measurement.json | 4b8c357c803e7b429766d54a87bf49bb5dd25343a9797b44b5702df93440c7a3 | e032d23b1f3163dcf95390589c93e2e9dcda474e | 일치 |
| all-in-one/registers/simulator-freeze.json | bb93c1994effc5609939ba566b7802ce7ed55154a7310f02379b308ac2c8c835 | 808ffac14dbd1b4a7d797fa6cd0d647635d90b47 | 일치 |
| all-in-one/registers/virtual-plc-test-results.json | a6b389f797f9a8b5ffe6928b8420f55c4cc459a327b0b48d716079d2eca6dd64 | 757dd50e45184568facb8ff62900b39d3ce848d1 | 일치 |
| all-in-one/sources/Electrical_Can_Decoating_20241118.pdf | 3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd | 0ee6b6f8361c5790864dbba4bbd9d55e8e7c08f8 | 일치 |
| all-in-one/sources/Electrical_Rev2.pdf | 5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6 | f610fd7c7ce14ae951b00cff57b969259bfb389d | 일치 |
| all-in-one/sources/GME_20250506.zap18 | 00c79b6d986e68298f65b172c1807115bc5d9e450a74fcc989d0796d8d8a4ea8 | 211c4f604627a32f82a1124c2a9872c2fcf00865 | 일치 |
| all-in-one/sources/PEData.plf | 647de7ea123daced41c27bec8f81aeb93c712cac714d4754d7da5c528abb016a | 65605ff8910f920109da731604aa5dc8d83fc956 | 일치 |
| all-in-one/sources/block_summary.json | 68253f9366908244a27ed461c66d465da7ec1723571f27deaa9a6f81a542de63 | 15b570a011645023dbfca2d5332a9e0ae3b0a7b6 | 일치 |
| all-in-one/sources/can-decoating-page-text.json | d3b4c14945dd00f79c58ebab0cb8991c422dd1670e95e24d10779bd9e9d99bba | 2bebec2c719fa57ed6c9f8d4e541e8848dc0d732 | 일치 |
| all-in-one/sources/decoded-original/0014-FlgNet.xml | 2e814adbaac6bab99bc668bfdab74f0fc90576324d0b88728951683869cfac30 | 4d164b074fcc13a8f97da9e24382cc169ef29555 | 일치 |
| all-in-one/sources/decoded-original/0030-FlgNet.xml | 9252c9da764993de1edb8b2e44c46d6e9f9d4b6118e751a0dbeaa9ffd8ea721b | e74c70b751acdcdbc7a8b3b0c98aa773c2107cab | 일치 |
| all-in-one/sources/decoded-original/0031-FlgNet.xml | 76385eab8f8f72b9faa16f7cf8905f395591b18c0a9ee9e6d7dd085a38c45c65 | 653d27572de6beedcf3eb6c95702bb119a8b567f | 일치 |
| all-in-one/sources/decoded-original/0047-IdentXmlPart.xml | 2e53bb895dd1ad2a74efaeb1ef16dfd61e62b1b2d7aa34cec8612f1b9cb0928e | 3dc282f149a21fdf76d5521ef1c833be63b578b4 | 일치 |
| all-in-one/sources/decoded-original/0048-IdentXmlPart.xml | d8e8687de7271bd294c2b62b33d789700af9d5014d82b130141988c4d479253d | 64fc5a7f1ad33f3b901b00f0d22d23578ffabff8 | 일치 |
| all-in-one/sources/decoded-original/0056-IdentXmlPart.xml | c5ec45cd232c36d80f80487ec0dd284a876e326ba2286fc722ecc861a400232a | 1364306d64caf1f1f094c98dc163edf69cdc1afc | 일치 |
| all-in-one/sources/decoded-original/0057-IdentXmlPart.xml | 1124275ab34e188b042b263d3c4b744abf5637ffd229af642b81a27f00a00c6b | 264d24445f42cf32706bc6942863f9f227eb797e | 일치 |
| all-in-one/sources/decoded-original/0148-FlgNet.xml | 1d80e1bbf1c82dcc4dd18628c35935bbd55a17b5be9c1ca7bfb249600d154313 | 3069ae3b5fa16ed10a64c149b6cf5cb5ace423b3 | 일치 |
| all-in-one/sources/decoded-original/0151-FlgNet.xml | 227627d165c6240a4c15b62fd4e4c8d7a621c15f35319cb424601df5cc52c904 | 8e8a9801d1f57180fc3747f6515c0353f38f7dc5 | 일치 |
| all-in-one/sources/decoded-original/0152-FlgNet.xml | 2b6165460f06a52de56afcb4d65ed163d64320e24af1b194e934a4d7c6bfe49f | dd8e35b98043d9d0f230351352273eac1d783990 | 일치 |
| all-in-one/sources/decoded-original/0175-FlgNet.xml | 41279d6aaa157de3be963d010d6ca7dea94811a0ace519c8a3d8baa015f67f97 | 1626da00b3bbcb46f77720271ecf0f50db9dc63b | 일치 |
| all-in-one/sources/decoded-original/0185-FlgNet.xml | 2532fbe9602e3effc1f3992aaeb6749e93841072f0e4d797c4b7a369a849ab61 | a170ac1d41d838e80166fbdb4f843ce98e7de4ef | 일치 |
| all-in-one/sources/decoded-original/0291-FlgNet.xml | fe0b92f074eba25148ce34084649af3d968962558d652727f1eea19f3e3c2550 | 1418fb2ed172c6df694a5eb8bf2dffd0b177653b | 일치 |
| all-in-one/sources/decoded-original/0398-FlgNet.xml | 4f092b18df4e44af98fd44e173f48dad213a4e80b71f46b0a5e8a700f5b0a747 | 67ebb54daa55093487ea7e780f23ae2cf193c397 | 일치 |
| all-in-one/sources/decoded-original/0499-FlgNet.xml | 6526c8da7b45f38e72d8ebd8c177889a58f7e2db7265d1572db5a8c7dd6e0467 | bea1c6292c4ca6319180e18544905727a4cc7030 | 일치 |
| all-in-one/sources/decoded-original/0500-FlgNet.xml | ad3240f11b6e0d3cfd745938134be49443e9db731d04e092170b89451b1b7435 | f1ef6a49f6dcd6590e3e501a43a73f1d7ef29f92 | 일치 |
| all-in-one/sources/decoded-original/0530-FlgNet.xml | 9f20c55030b3127abfedce38de08e50d494885cdf61d75c85a2715b0d380eac5 | 8058859ea175ef384e9ffc63a1785af3f576ddae | 일치 |
| all-in-one/sources/decoded-original/0531-FlgNet.xml | d53b8ca1482c4365251a3b1d0f108ed32fa4e5b8f78848e2ceb48648f2d7095e | f6400b188f6f2363aabf50428046e42b8b95327a | 일치 |
| all-in-one/sources/decoded-original/0532-FlgNet.xml | 63b649820f729a693a38203c57eb79c1a25fbd4374e3e3aa79609b47f1c3c980 | cf51b7ff14d717691648ab811be51293af847ba3 | 일치 |
| all-in-one/sources/decoded-original/0533-FlgNet.xml | 3fd228af5f1eeb7c88b48cef59b9faa2e601cbe318498a26c8c339957fc01d58 | 7bdb10ef38a2f07e0e66f4e0f78e68ce82ab7347 | 일치 |
| all-in-one/sources/decoded-original/0538-FlgNet.xml | afb3c3104bb60b4b1310f62ed5fb2caf659afc514c2b3fd209ff71d2008686ce | 3372843d3fb58f402f82a6250588ffa90f7707dc | 일치 |
| all-in-one/sources/decoded-original/0562-IdentXmlPart.xml | 85aada44dd9a3e66835463c3fed400f1efe121f4f5bc5ab8f0ad49481ec0ea1c | 1609802542a3e560baba3f2b73c306be281dfb23 | 일치 |
| all-in-one/sources/decoded-original/0563-IdentXmlPart.xml | 86cf35b6baebc079cb5a092baf53ec3364c377ea7318eb263ab69c8b4550b4ad | 6a10fc694f896cda16409804daf2554c91635654 | 일치 |
| all-in-one/sources/decoded-original/0564-IdentXmlPart.xml | 2aed17fa02d19b0a081023282841aa561d6a2dca3e393284da3622b967af00b1 | c4b1f2cb191970cfce1cce59cb290a9f1f934c37 | 일치 |
| all-in-one/sources/decoded-original/0565-IdentXmlPart.xml | 0f7f970faa6c456f2bb032b1a2072a2f52db1e03fc77bd8d35d4583deeaf1149 | c2e3e2d57c94c5da864f6e172f0a7a925da942d6 | 일치 |
| all-in-one/sources/decoded-original/0582-IdentXmlPart.xml | 41d4c2bd750392bbc2edc43995ec3a9da47a63c13ee86496df8f187492008951 | 82636dec064876d0f4cc714ef385b07d6e05efe0 | 일치 |
| all-in-one/sources/decoded-original/0584-IdentXmlPart.xml | 3bff6c478e594bf97bb1730971944e96b0b5e2407199420fe6567d5fe609ea5d | 0f8dde829be66041bea79e40ccc4586d84ff1da7 | 일치 |
| all-in-one/sources/decoded-original/0585-IdentXmlPart.xml | e36ec18aa4abebea8f9160254522bb51ff722eae804c5a469790f85f02939184 | 16574d37ef3ca61b59ba396c400e269ab1dd3440 | 일치 |
| all-in-one/sources/decoded-original/0587-IdentXmlPart.xml | bab957ac7c180d9c91b4f904b29e9dbd5812c6ba8f7b9e0c7faf9708605b203e | 67e84e4b8d43b7c5864ec40fcc2c9fbc2222b436 | 일치 |
| all-in-one/sources/decoded-original/0611-IdentXmlPart.xml | 0d583915a261703954da22c176ba9f81338ad13ea2810e7cd5f7de8aa1bfa089 | bad6b16fb32a32d47d882f48754994887457872b | 일치 |
| all-in-one/sources/decoded-original/0612-IdentXmlPart.xml | 95b545d4964d371ebfc107894ea90b8b1d0d7ab5d3a70e643f8ce539063c0f38 | 7cc782d33d07ef225c2104f3e7c9fbd31f7c7467 | 일치 |
| all-in-one/sources/decoded-original/0627-IdentXmlPart.xml | 08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb | 61ebc0abbb2ca160e11e1da400a3f14a397d8bc5 | 일치 |
| all-in-one/sources/decoded-original/0628-IdentXmlPart.xml | 9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd | 170ca5c72599edc7ea7eefe651c3680ce325e76a | 일치 |
| all-in-one/sources/decoded-original/0629-IdentXmlPart.xml | 67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972 | 058129bb01e27f7a6a0d0293f332d745e5bab74e | 일치 |
| all-in-one/sources/decoded-original/0672-IdentXmlPart.xml | 6bfc2ba142d6270c39eb1f13b2886204865af6d46eadc5f410c26981b8da9222 | 2f2790dab4bb2357733112220e0acc41edb6feb6 | 일치 |
| all-in-one/sources/decoded-original/0674-IdentXmlPart.xml | 4770702f519bacda69202bb2f7733d983074bda90964360c238f990d9d08fd84 | f210593944547b63eab10c667348711413600aab | 일치 |
| all-in-one/sources/decoded-original/0675-IdentXmlPart.xml | b1902886927d8403fab736d9c8ffe73f2fbc8ce4b7ca7c345144964668b051c3 | d82a33b173c8dc0737fd890eb2a63a88a07d0831 | 일치 |
| all-in-one/sources/decoded-original/0676-IdentXmlPart.xml | c58427c5b0ac6c11cdb52e4c6d0461c7b191fae81ccace191048e9f175fcec59 | 1ed67265f69796a4e659f9438e551068037f33a4 | 일치 |
| all-in-one/sources/decoded-original/0678-IdentXmlPart.xml | 51e637e0b9713c028810f2a717b5c3804a3a26c2f1be7e332a4d6bf277bfc382 | 7fafb2297bcdf739bf1d1dd68cebc0d74f2a40cc | 일치 |
| all-in-one/sources/decoded-original/0680-IdentXmlPart.xml | fd551ad5d47bbd66c6bcdcc1949aaddf68cc086a3ddf6fb337adc767954c2b95 | c9049ced1eaed72c5e251a88601d46ddec8c3e50 | 일치 |
| all-in-one/sources/decoded-original/0682-IdentXmlPart.xml | 25c7aeb1bfa29c178eaa396db33d4eb6d2d29b9a3f2eb965fa61fae8ce7f1092 | 61182411e912941161eccf4e90c1f174e5379f0a | 일치 |
| all-in-one/sources/decoded-original/0683-IdentXmlPart.xml | 0c9b569d041cd5babbbeded8a3bdc5d3754927125756b6ac54b7cb991b22fc22 | 662acdb9a06c0ba1c0027e7dd215a28f07d3f02b | 일치 |
| all-in-one/sources/decoded-original/0684-IdentXmlPart.xml | 6e9b3f173184adcddca503e81e2649022734b6ea3639c1d5ddaf0a08bac00208 | d67b98b5d5516e0330aae5cfdbee41a3e09206e1 | 일치 |
| all-in-one/sources/decoded-original/0685-IdentXmlPart.xml | 2003d5741a0d707755c5e6e8b737fa106414b87b5b431b97271d9f1a5d343448 | 86bda988d9efedba92ba2f3e4877497d9eb5230a | 일치 |
| all-in-one/sources/decoded-original/0686-IdentXmlPart.xml | b450d8ff22f0fffd7a214b2a696af28a03a27834ebf862bfaa822dc9bfb3c8d4 | 8c152d926692a8e15973c980e08e338d29411814 | 일치 |
| all-in-one/sources/decoded-original/0688-IdentXmlPart.xml | ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda | 463585759f1ecd94f32362b4fefb000a152f5773 | 일치 |
| all-in-one/sources/decoded-original/0692-IdentXmlPart.xml | bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037 | 737785d03b5fad43c5b4d451955726d800edb1c0 | 일치 |
| all-in-one/sources/decoded-original/0694-IdentXmlPart.xml | 757ccebdf32d0a168dd787bfa735fe6494eac4c4a9f7a5adc63898a88e8b152d | c45e8f3ca4129dc06734f6a12ef79e6ed6528a7d | 일치 |
| all-in-one/sources/decoded-original/network-map.json | c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60 | 424430b6b953e43138e5d0a18ca40c949e21cfa1 | 일치 |
| all-in-one/sources/electrical-page-text.json | 4b846819aab7e1306aebea617042f9f9ffe0c8aee1930e6f3db035bea3739153 | 1f48073c07b28e668d3d72d5ce49db263a5214e6 | 일치 |
| all-in-one/sources/hmi-windows.csv | 15f8d69b5c43d4fdbe550f9cd2717f855fea877ed8146973054cb6dbcaa9892e | 8401dcfe5ba3e7e244eea0f501bb84a2e387da39 | 일치 |
| all-in-one/sources/hmi_plc_tags.csv | a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404 | cf4c0650e7c7baac350dcb89909b808435704880 | 일치 |
| all-in-one/sources/live_index.json | 14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1 | e35ccea1f841349c632666c29954b7bcd4f5839e | 일치 |
| all-in-one/sources/source-manifest.json | 5af6e85994536897fd92f75972534a691e6eb0f067aafe07679c0788fd84e5bf | 38cf407491d52dc6128cf94ca8a4bddee350de6d | 일치 |
| docs/equipment-standard/INVENTORY.json | 720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc | 587c3748ad9224718f95ba06463fee913dae231d | 일치 |
| docs/equipment-standard/WORK-ITEM-TEMPLATE.md | 4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586 | e546f39535d2b589e80f97db869ac37ce4d05cfd | 일치 |
| docs/equipment-standard/WORK-STANDARD.md | 05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99 | f76a570cc73098632e08759b17934000f7e3a253 | 일치 |

## 부록 C. 최종 자체 검사

2026-10-11T10:48:32.709081+00:00 실제 검사: 7영역·전체해시표·선정78파일 고정 Git blob/SHA256·중지5 freeze·원본 Git clean·재해시·핵심XML 파싱·렌더4파일 존재 모두 통과. 원문 대조에서 작성 중 발견한 W173→W164, burner ON 선언0587→0582, startup DB3W4 선언0057→0563/BAD0562 표기를 전달 전에 정정했다. 검사는 정적 문서 범위이며 사용자 UI/기록/TIA/CPU/현장·시뮬레이터 시험은 수행하지 않았다.
