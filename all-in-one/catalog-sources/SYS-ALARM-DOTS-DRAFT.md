# SYS-ALARM 알람과 Reset 원본 조사 초안

## 핵심 확인과 남은 경계

- HMI ResetAlarms는 DB2.DBX13.4 요청이고 내부 RESET_ALLARM은 DB2.DBX6.0이다. TacitAlarms DB2.DBX13.5와 STOP_HORN DB2.DBX6.2도 별도다. 요청은 0158에서 소비되며 Reset/소음확인을 원인 제거·현장 복구로 판정하지 않는다.
- 알람 manager는 DB3.DBW0,2,4,6,8,10,12,14,16의 **9 Word 불일치**를 검사한다. 이는 모든 경보의 OR나 상승비트 전용 검출이 아니다. DB3.DBX19.0 이후의 인버터 경보 선언은 이 범위에 포함되지 않는다.
- PLC의 Siren=%Q7.6과 Blinking Ligh=%Q7.7을 확인했다. 그러나 실제 OEM FG17/143은 A7.6을 LAMPALARM 2/17HL2, A7.7을 LAMPALARM/17HL1으로 그린다. 이름만으로 실제 사이렌/점멸 장치 종류를 확정하지 않는다.
- STOP_HORN은 운전자 요청 외 온도 경보 복귀 가지에서도 Set된다. 내부 RESET_ALLARM도 자동 예열/생산 선언에 별도 Set 사용처가 있다. ACK와 Reset을 사람의 한 버튼에만 귀속시키지 않는다.
- 이번은 SYS-ALARM 한 catalog ID의 문서 초안이다. 개별 설비 전체 알람 재조사·로컬 2차133 통합·실물 확인·제품 배포가 아니다.
- 공유 근거는 [BF01](BF01-DOTS-DRAFT.md), [LD01](LD01-DOTS-DRAFT.md)의 입력 Word와 개별 경보, [CR01](CR01-DOTS-DRAFT.md)의 공통 입력/FG17, [TC01](TC01-DOTS-DRAFT.md)·[TC09](TC09-DOTS-DRAFT.md)의 온도 복귀 STOP_HORN을 연결 재사용했다. 신규 고유 핵심 0151~0155/0158/0005 및 대표 0457/0355/0539 핀과 FG17/135/143은 독립 대조했다.

## 1 설비와 자료 기준

대상은 INVENTORY catalog[35]의 SYS-ALARM, software, 공통 시스템, parent_id 없음, depth0, phase2/planned, priority_key 없음이다. 전기 FG17이 연관되지만 공통 기능을 별도 실물 장치 하나로 만들지 않는다. BC01 등 경보 소유자는 각각 유지한다. 별칭 resetalarms/reset_allarm/acknowledg/siren/blinking ligh는 탐색 키이며 모두 같은 신호의 동의어가 아니다.

고정 읽기 원본은 `gme-research/source-mv06`, Git `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, VERSION 1.12.0이다. 최신 사용자 보고 버전·현재 main·실제 CPU와 동등하다고 주장하지 않는다. 표준 GME-STD-1.0.0, BATCH11 지시/범위, AGENTS, rollout SKILL, WORK-STANDARD, WORK-ITEM-TEMPLATE, INVENTORY 및 현재 고정본 VERSION/인계/배포/ACTIVE-WORK 머리말을 확인했다. 런타임 모델·추론 설정 증명은 미확보다.

4자리 원본 약칭은 `all-in-one/sources/decoded-original/NNNN-FlgNet.xml` 또는 `NNNN-IdentXmlPart.xml`이다. LAD document_id, index_order와 원본 NID는 별도다. 파생 network-map은 길잡이이며 아래 주장은 원본 선언·Part/Wire/ORef/CRef로 한정한다. 특히 0401-FlgNet은 HMI 출력 미러이며 startup document401과 동일한 이름의 자료로 합치지 않는다.

|7영역|적용|확보와 누락|
|---|---|---|
|설비·자료 기준|적용|고유 기능 ID·고정 버전·타 설비 소유 경계; 현행 동일성 미확인|
|I/O·HMI|적용|요청/내부 bit/물리 I/Q/Word/타이머 형식; 화면 이벤트와 권한 미확인|
|제어 구조|적용|9 Word 차이·혼/경광등·Reset 소비·호출; 전 프로그램 실행 의미는 미해석|
|전기 전달|적용|FG17/135/143 양 끝점과 개정 시각검토; 준공·장치종류·하류 릴레이 부하 미확인|
|알람·복구|적용|대표 유지/Reset, 소음확인과 원인 제거 분리; 모든 개별 경보 검증 아님|
|증상 관찰|적용|관찰점·비교 근거·필요 기록 제시; 조치·시험 미수행|
|완료·누락|적용|문서와 정적검사만; UI/게시/TIA/CPU/현장 완료 아님|

## 2 I/O와 HMI 요청 및 저장 범위

주소는 SSD.AO/BO 비트 오프셋과 SAD 영역, BAD→DepDBBlock.TOD를 대조했다. 아래는 백업 선언 주소이며 현재값·현재 CPU 검증이 아니다.

|신호|형식·주소|원본 선언과 주요 참조|
|---|---|---|
|Flag.RESET_ALLARM|Global Bool DB2.DBX6.0|0565 RID2 AO48;0564 Flag RID1 TOD2; NID9 UID37 Set/NID4 UID246 Reset|
|Flag.RUN_HORN / STOP_HORN / NEW_ALLARM / M_HORN|Global Bool DB2.DBX6.1/.2/.3/.4|0565 RID3/4/35/40 AO49/50/51/52; M_HORN NID5 UID276은 Read|
|Flag.Reset_Allarms_HMI / Stop_horn_HMI|Global Bool DB2.DBX13.4/.5|0565 RID61/62 AO108/109; NID9 UID27/41 Read, UID43/59 Reset|
|Inputs.Reset_allarmi / Tacitazione|Global Bool DB13.DBX19.7/.6|0565 RID57/63 AO159/158, BAD56;0564 Inputs TOD13; NID9 UID24/34|
|원시 입력 Word|Global Word %IW18|0627 RID25 AO144 SAD Input SAM=None NID1 UID81; I19.6/.7 포함|
|입력 저장 Word|Global Word DB13.DBW18|0629 RID26 AO144 BAD4→0628 Inputs TOD13, NID1 UID82 Write|
|Siren / Blinking Ligh|Global Bool %Q7.6/.7|0567 RID44/39 AO62/63 SAD Output; NID5 UID279 Coil/281 Set; NID4 UID248 Reset|
|103A7 / Reset_Inverter|Global Bool %Q7.4/.5|0567 RID76/74 AO60/61; NID9 UID63/55 Coil|
|Tag_160 / Tag_161|Timer %T47/%T48|0567 RID38/43 AO47/48; S5 timer이며 HMI 태그 아님|
|Data.Siren_time|Global Int DB1.DBW322|0565 RID66 AO2576, BAD41→0564 Data TOD1, NID10 UID25|
|Data.SIREN_WORK_TIME|Global S5Time DB1.DBW88|0565 RID42 AO704, NID10 UID29 Write/NID5 UID277 Read|
|PLS M50.2|Global Bool %M50.2|0567 RID45 AO402 NID5 UID280 AK=RW, PBox의 bit 저장부; 주기 점멸 clock으로 단정 금지|

HMI CSV `hmi_plc_tags.csv`는 ResetAlarms="DB2,X13.4"(002E1), TacitAlarms="DB2,X13.5"(000DA)를 PLC 연결의 dde.cfg 설정으로 기록한다. CSV에 현재값이라고 써 있지 않으며 버튼 press/release, 모멘터리/토글, 권한, 실제 알람창 ACK 이벤트·히스토리 삭제와의 결속은 미확인이다. 따라서 이 문서의 ‘ACK/확인’은 직접 확인된 Tacitazione/STOP_HORN 소음확인 경로를 뜻한다. 모든 HMI 알람 acknowledgment 정책을 확인한 것이 아니다.

0397 NID1의 Word 전달은 P78 Move, W88 ORef81/RID25→in, W89 out1→ORef82/RID26이다. I19.6/19.7을 개별 Bool 코일로 옮기는 것이 아니라 IW18의 두 바이트 전체를 DB13.DBW18로 복사하므로 입력 응답은 해당 Word 쓰기/다른 writer·호출을 같이 보아야 한다. PIW 직접주변 접근으로 바꾸어 표기하지 않는다. 기존 BF01/LD01/CR01의 동일 고정 입력 전달 근거를 재사용한다.

### 2.1 알람 스냅샷 Word의 정확한 범위

0564 Allarm RID7 TOD3, WorkData RID9 TOD6. 0565의 무명 Global Word RID8/12/15/18/21/24/27/30/33은 AO0/16/32/48/64/80/96/112/128이다. 이름이 비어 있어도 DB와 오프셋으로 판별했다.

|DB3 원본 Word|스냅샷 이름과 DB6 주소|원본/저장 RID|0151 원본 UID→저장 UID|
|---|---|---|---|
|DBW0|W0, DBW0|8→10|173→174|
|DBW2|W1, DBW2|12→13|175→176|
|DBW4|W2, DBW4|15→16|177→178|
|DBW6|W3, DBW6|18→19|179→180|
|DBW8|W4, DBW8|21→22|181→182|
|DBW10|W15, DBW30|24→25|183→184|
|DBW12|W16, DBW32|27→28|185→186|
|DBW14|W17, DBW34|30→31|187→188|
|DBW16|W18, DBW36|33→34|189→190|

원본은 Word, WorkData 저장부는 Int이고 비교 Part의 SrcType도 Int다. W15 이름을 DBW15나 DBW10으로 잘못 바꾸지 않는다. 대상 DB3는 바이트0~17, 144bit 범위다. 0564 Allarm OD.S=208 선언 전체와 동일한 범위가 아니다. 0657 RID207 BC01_INV AO152(DB3.X19.0), RID210 RD01_INV AO153, RID215 MC04_INV AO154, RID218 VS01_INV AO155, RID221/224/227/231 AO156~159, RID238 Aux_INV AO160, RID246 ER01_run AO161은 이 9 Word 밖이다. 그 개별 경보가 무음이라고 단정할 수는 없지만 **이 비교 하나가 모든 경보를 포괄한다는 주장은 성립하지 않는다**. 다른 전달 경로와 화면 표시를 별도로 확인해야 한다.

## 3 제어 구조와 실제 핀

### 3.1 호출과 순서 경계

0033 LAD1622/main index11/NID9: ORef349/RID52 ON(%M0.0,0692)→P352 Contact(W351)→W353 CRef347.en. CRef347 RID92/CodeBlock350 RID91은 0688의 Allarm manager FC24 선언이다. main index8의 0031에서는 ON Contact282.out W283이 아날로그 환산 및 allarms1/2/3 CRef261/264/267/270.en에 병렬로 연결된다. 이 백업 색인의 main 순서를 기록했으며 현재 CPU의 실제 호출·인터럽트·최종 scan 우선순위는 미검증이다.

allarm manager의 index 순서는 0151(NID1),0152(NID2),0153(NID3),0158(NID9),0154(NID4),0005(NID10),0155(NID5),0156(NID6),0157(NID7)이다. XML 파일번호나 NID 숫자를 실행 순서로 정렬하지 않는다. 마지막 두 망은 보고 주기와 카운터 초기화이며 SYS-COUNTERS 관련 소유를 완료로 합산하지 않는다.

### 3.2 스냅샷과 변화 판별

- 0151 LAD927/NID1: RESET_ALLARM Contact213, RUN_HORN Contact215, STOP_HORN Contact217 → OR121(in1/in2/in3, W214/216/218). OR.out W212가 9 Move P127/132/137/142/147/152/157/162/167.en에 **병렬** 연결된다. 스냅샷은 ‘RESET 또는 RUN_HORN 또는 STOP_HORN’에서 갱신된다. DB3를 0으로 지우는 동작이 아니다. 각 Word 전송은 W194~211이며 예를 들어 W194 O173→P127.in, W195 P127.out1→O174이다.
- 0152 LAD928/NID2: Int Ne191/194/197/200/203/206/209/212/215가 DB3 Word와 위 스냅샷을 비교한다. W242/245/248/251/254/257/260/263/266 → OR190 9입력, W267→NOT STOP_HORN Contact271, W272→Coil219, W270 O239/RID35 NEW_ALLARM 쓰기다. 첫 비교 W240 O220/RID8→Ne191.in1, W241 O221/RID10→in2. 식은 ‘어느 Word라도 다름 AND NOT STOP_HORN’이다. 비트가 0→1인지 1→0인지 검사하는 마스크/상승검출은 이 망에 없다.
- 0153 LAD929/NID3: NEW_ALLARM Contact219 → NOT RESET_ALLARM Contact221 → NOT STOP_HORN Contact223 (W220/222) → W224 SCoil204 RUN_HORN(O211/RID3,W216)와 RCoil206 NEW_ALLARM(O212/RID35,W217). NEW_ALLARM은 0152 Coil과 여기 Reset의 복수 쓰기다. 스냅샷 갱신과 순서 영향 때문에 개별 시점의 값만으로 실제 소리 발생을 확정하지 않는다.

### 3.3 Reset 요청과 ACK 소비

0158 LAD930/index4/NID9의 두 가지는 분리된다.

1. Inputs.Reset_allarmi O24/RID57→Contact23(W22), HMI 요청 O27/RID61→Contact26(W25). W29/30→OR28. W38 OR28.out→SCoil33, RCoil40 및 TOF LRef64/73.IN. W36 O37/RID2가 내부 RESET_ALLARM을 Set하고 W42 O43/RID61은 HMI 요청을 Reset한다. 물리 버튼 입력은 이 코일로 지우지 않는다.
2. Tacitazione O34/RID63→Contact32(W31), Stop_horn_HMI O41/RID62→Contact39(W35). W45/46→OR44. W54→SCoil49 STOP_HORN(O53/RID4,W52) 및 RCoil56 HMI 소음확인 요청(O59/RID62,W58). 이 가지는 모든 Allarm bit의 Reset 코일에 직접 연결되어 있지 않다.
3. Reset OR28 출력의 두 TOF는 0568 Instruction RID77, 0569 Instance RID78/UID72=IEC_Timer_0_DB DB36, RID84/UID74=IEC_Timer_1_DB DB37이다. 0566 RID79는 **Time T#3s, V3000**이고 0158 W68/78→PT, W67/77의 Q→Coil48/60→Q7.4/Q7.5다. TOF를 3초 켜짐 지연 TON 또는 고정 3초 펄스로 바꾸어 쓰지 않는다. IN 유지시간과 떨어진 후 off-delay가 관련되며 실제 외부 복구 성공 신호는 아니다. EN/ENO=false이고 ET O71/76은 이름 미결속이다.
4. 0154 LAD931/index5/NID4: RESET_ALLARM Contact259 또는 STOP_HORN Contact261 → OR224 → W258 SdCoil229 및 timer Contact263. S5T#1S는 0566 RID37, W251→value; Tag160=%T47는 O244/RID38 W252→operand. OR 조건과 timer Contact263.out W264가 RCoil235 RESET_ALLARM, RCoil237 STOP_HORN, RCoil239 Q7.7을 Reset한다. **내부 명령 유지·정리용 1초와 외부 Q7.4/.5 TOF 3초는 다르다.**

### 3.4 혼 시간과 출력

0005 LAD932/index6/NID10: powerrail W21→CRef23.en, CodeBlock22/RID64는 0050 KF_KT FC109. O25/RID66 Data.Siren_time→KF(W24), O27/RID67 **Bool 0**→SEC(W26), KT→O29/RID42 SIREN_WORK_TIME(W28). 입력 Int, 출력 S5Time 형식이다. 이 조사에서는 FC109의 전체 변환 내부/잘림/범위오류를 다시 검증하지 않았으므로 Int 설정을 곧바로 ms나 현재 초 값으로 표기하지 않는다. 기존 BF01/LD01의 같은 FC109 형식 근거를 연결 재사용한다.

0155 LAD933/index7/NID5: RUN_HORN Contact296(O275/RID3,W284) 또는 M_HORN Contact298(O276/RID40,W285)→OR256(W297/299). W295 OR.out이 SdCoil261, Coil265, PBox268, timer Contact300의 입력으로 병렬 연결된다.

- Siren Q7.6은 Coil265, O279/RID44/W288로 직접 기록한다.
- S5Time Data.SIREN_WORK_TIME O277/RID42/W286이 timer261.value, T48 O278/RID43/W287이 operand다. T48 Contact300(O282/W292).out W301→RCoil274 RUN_HORN(O283/RID3,W294).
- PBox268의 bit W289/O280은 %M50.2 저장부다. out W290→SCoil270 Q7.7(O281/RID39,W291). 즉 여기서 확인한 것은 상승변화 저장을 이용한 **Set**이며 PLC에서 주기적으로 Q7.7을 토글하는 로직을 확인한 것이 아니다. Blinking이라는 이름을 그대로 점멸 주기 보증으로 해석하지 않는다.
- 이 망에 STOP_HORN을 Q7.6 Coil 직렬 차단하는 접점은 없다. STOP_HORN은 앞 스냅샷/NEW_ALLARM/요청 정리 및 다른 writer와 함께 검토해야 한다. 버튼을 누르면 즉시 Siren 출력이 0이 된다고 이 원문만으로 보증하지 않는다.
- M_HORN은 검색된 명명 선언에서 읽기만 발견했다. DB 초기화/Word쓰기/외부 HMI가 쓸 가능성까지 배제한 것은 아니며 수동 혼의 실제 조작원을 미확정으로 남긴다.

### 3.5 복수 쓰기와 초기화 경계

명명 선언 검색에서 0577 RESET_ALLARM RID16의 NID3 UID594/654 및 NID4 UID938/1003은 Write/Set 사용처다(0164 예열·0165 생산). SYS-AUTO 영역이므로 전체 기동 의미를 다시 조사하지 않았으며 ‘Reset은 항상 운전자가 요청한다’고 쓰지 않는다. 0684 STOP_HORN RID16도 NID1/2/4/5/11/13에 Write가 있다. 대표 0539 NID13에서 Lt1068→기존 MAX_TC09 Contact1177→W1178이 RCoil1076(MAX_TC09)와 SCoil1078(STOP_HORN, UID1118/RID16)을 동시에 구동하는 복귀 가지를 확인했다. 상세 온도·비교·히스테리시스 근거는 TC09 초안을 재사용한다.

0148 LAD403 startup only/index3은 9 Move의 정적 초기화 경계다. P329 ON.out W330에서 P250/P267/P281.en으로 나뉘고 P250→253→256→259, P267→270→273→276은 각각 ENO 연쇄(W306/309/312, W317/320/323)다. O285/287/.../301의 RID54는 0048 NID3 선언 Int#0. 파생 색인은 DB3.DBW0~16 목적지를 제시하나 이 조사에서는 모든 무명 목적지 선언/NID를 재결속하지 않았다. startup 기존 상세 근거를 재사용하며 현재 startup 호출, retentivity, 재시작 동작과 ‘모든 알람 초기화’ 완료는 미확인이다. 이 초기화도 운전자 Reset 버튼과 같은 이벤트로 병합하지 않는다.

## 4 전기 양 끝점과 도면 상충

원본 `all-in-one/sources/Electrical_Rev2.pdf`에서 3페이지를 새로 렌더하고 시각 확인했다. FG17=PDF18, FG135=PDF136, FG143=PDF144로 각각 실제 footer를 확인했다. 도면 기본일 27.05.2024, FG17과 FG143 개정란 Rev2/17.03.2025, FG135 개정란 공란이다. 파일명 Rev2를 모든 페이지 개정으로 복제하지 않는다.

|경로|실제 도면 끝점|해석·누락|
|---|---|---|
|소음확인 버튼|FG17 +24Vdc10.7→X20:2013→17SB1 YELLOW 접점13/14→X20:2014→E19.6→FG135 MOD12 단자37|Inputs.Tacitazione는 위 IW18/DB13W18를 거친 내부 신호; 버튼 실물·정상극성 미확인|
|Reset 버튼|같은 +24V/X20:2013 분기→17SB2 BLUE 13/14→X20:2015→E19.7→FG135 MOD12 단자38|Inputs.Reset_allarmi; 소음확인과 별개 물리 입력|
|Q7.6 경보 표시|FG143 MOD15 단자37 A7.6→FG17 X1:41(5x20 2A IST.)→17HL2 X1/X2→X1:43→0Vdc10.6|도면 제목 LAMPALARM 2, PLC 이름 Siren 상충. 실제 발성장치인지 미확인|
|Q7.7 경보 표시|FG143 MOD15 단자38 A7.7→FG17 X1:42(동일 퓨즈 표기)→17HL1→동일 X1:43/0V 귀로|LAMPALARM. 실제 자체점멸 장치/주기 미확인|
|Q7.4 Reset 출력|FG143 MOD15 단자35 A7.4, X21:3037 표시→FG17 17KA1 A1; A2→0V|릴레이 코일 구동. 하단 접점표의 1/5/9 등은 접점 위치 안내이며 이 페이지의 부하접점 핀으로 오독하지 않음|
|Q7.5 Reset 출력|FG143 MOD15 단자36 A7.5, X21:3038 표시→FG17 17KA2 A1; A2→0V|같은 경계. downstream inverter별 실제 부하접점·단자는 이번 미검토|

FG143 MOD15 공통전원은 +24Vdc10.8→X21:3039 퓨즈5x20 4A F→단자39, 단자40→0Vdc10.6로 그려 있다. FG135 MOD12는 +24Vdc10.7→X21:3027 퓨즈5x20 2A IST.→단자39, 단자40→0V다. 두 전원 표기를 110Vac 버튼 회로로 바꾸지 않는다. 표기된 정격은 도면 기록이며 현행 보호값 설정·교체품 승인으로 사용하지 않는다.

Q7.4의 PLC 이름 103A7과 FG17 inverter reset의 관계도 이름보다 해당 주소/코일로 추적했다. 상대참조 FG18/20/24/27, FG30/42/47의 모든 inverter 내부·현장 reset 조건은 이번 범위 밖이다. 이 문서는 릴레이를 동작시키거나 현장 복구를 지시하는 절차가 아니다.

## 5 원인 유지 확인과 복구

### 5.1 원인과 유지의 대표 직접 확인

0457 LAD1823/allarms1 index43/NID50 ‘presence110v’: 0657 RID248 Inputs.Presenza_110V DB13.X19.5, RID252 Allarm.110V_Fault DB3.X11.4. NOT Contact23의 O24(W22)→W41 SCoil27→O48(W47)가 경보를 Set한다. 별도 RESET_ALLARM Contact35(O38/RID13,W42)→W43 현재경보 Contact36(O39,W44)→W45 RCoil37(O40,W46)가 해제한다. 이 Reset 가지에 실제110V 복귀 확인 접점을 임의 추가하지 않는다. 타이머 Part는 없다. 원인 지속시 재Set 가능성과 같은 scan Set/Reset 우선순위는 현재 CPU 검증 대상이다. 원시 전압, 상태 접점, 내부 DB, 유지 경보는 별도 관찰값이다.

0540 공통 MAX_DP_FILTER의 상세는 BF01/BF02 초안을 재사용한다. 원본 독립 확인 범위는 OR1120(두 DP가 >2800 또는 <-100), SdCoil1136 S5T#3M(0683 RID96)/Tag112, SCoil1141, Reset Contact1208/현재경보Contact1210와 두 Lt1146/1149(<2500)→RCoil1152의 결속이다. 이는 SYS-ALARM의 단일 글로벌 Reset이 모든 개별 경보에 똑같은 복귀식을 강요하지 않음을 보여준다. 수치는 고정 프로그램 원문이며 현행 차압 설정/승인 안전값이 아니다.

### 5.2 통합 경보와 HMI 가공의 구별

0355 LAD331/NID1의 hmi standard motors 원본은 Local Bool Allarme1~5(Contact33/36/39/46/30)→OR41의 5입력(W42/43/44/48/49)→W57 Coil59 Comulativo_allarmi(O60/RID22,W58)다. 이는 **호출별 5입력 통합 경보 출력**이다. 0621/0622의 RID22는 S=Local, SSD.S=O인 인터페이스이며 전역 plant alarm bit가 아니다. 0621 IAD PN7과 0622 PN13의 중복 문맥은 호출 위치와 선언을 함께 봐야 한다. BC01/FN04/LD01 등의 실제 인수 매핑은 기존 해당 설비 초안을 재사용하고 전체 호출을 이번 완료로 세지 않는다.

개별 Allarm 래치, 호출별 Comulativo_allarmi, manager NEW_ALLARM 차이 판별, Q7.6/.7 표시, HMI 알람창 확인은 서로 다르다. 이번 확보 근거에는 이것들을 하나의 ‘전체 정상’ 비트로 보증하는 전역 식이 없다. HMI 목록이 비었거나 소리가 멈춘 사실만으로 원인 제거·안전재기동·현장복구를 인정하지 않는다.

### 5.3 복구 판정에 필요한 독립 증거

관찰 목적의 순서는 원시 원인/처리응답과 시각 → 해당 경보 발생/유지/Reset 식 → 요청 bit와 내부 bit 소비 → 전체 Word/스냅샷 차이 → 호출별 가공/물리 출력 → 실제 표시·소리 → 승인된 원인 제거와 재발 관찰을 분리하는 것이다. 이는 조작 실행 지시가 아니다. 온라인 프로젝트/CPU 일치, 현장 안전절차·작업 권한, 제조사 장치 복구 조건 없이 Reset/재시동·보호값 변경을 수행하지 않았다.

## 6 증상별 관찰과 필요한 기록

|증상|관찰 위치와 비교|판정 유의점|
|---|---|---|
|HMI Reset 누른 뒤 경보 유지|DB2.X13.4→DB2.X6.0, 해당 원인·래치, 개별 R조건, HMI 이벤트 시각|요청소비와 원인제거 별도; 0457/0540 복귀조건 차이를 보존|
|물리 Reset 반응 없음|17SB2/X20:2013·2015, I19.7, IW18, DB13W18/X19.7, FC24 호출, DB2X6.0|전기 작업은 승인 자격자; 원시입력과 처리Word 지연/다른 writer 구분|
|소음확인 후에도 Q7.6 유지|DB2.X13.5/.6.2, RUN_HORN/.6.1, M_HORN/.6.4, T48, DB1W88, Q7.6|0155에 STOP_HORN 직렬차단 없음. 즉시 정지 보증 금지|
|경보가 있는데 혼 요청 없음|경보 정확 주소, DB3W0~16와 DB6 스냅샷, STOP_HORN/NEW_ALLARM|DB3.X19.0 이후는 이 비교 범위 밖. 전체 경보 전송으로 일반화 금지|
|‘새 경보’처럼 반복 표시|9 Word 이전/현재값, 스냅샷 갱신 조건·순서, Reset/STOP_HORN|불일치 비교는 상승뿐 아니라 해제 변화도 가능|
|Q7.7=1인데 점멸 안 함|0155 PBox/Set,0154 Reset, FG143 A7.7/FG17 17HL1, 실물 모델|코일=점멸파형 증거 아님; 자체점멸 장치 여부 필요|
|Reset inverter 출력이 예상보다 길음|0158 OR28.IN 시각, TOF DB36/37 IN/Q/ET, Q7.4/.5|T#3s는 off-delay이며 눌림 유지시간과 구분; 외부고장해제 확인은 별도|
|HMI 통합경보와 혼이 다름|호출별 Local Allarme1~5→Comulativo, 경보주소 범위, 0152/0155|각 소유/가공 경로가 달라 같은 상태로 강제 일치시키지 않음|

기록에 관찰자, UTC/현지 시간대, CPU/프로젝트 식별, 신호 전체명·주소·값/형식, 수집 장치, 도면 페이지·단자, 비교 원본, 원인 배제 결과, 승인 조치, 복구 후 재발 관찰을 남긴다. 이번 실제 측정/조치/운전 시험·운영 사진 수집은 0이다. 기존 미지 note/repair_observation 필드는 임의 생성·완료 처리하지 않는다.

## 7 완료 상태와 누락 범위

문서 상태는 complete_with_gaps 초안이다. 자체 정적 문서검사는 원본 핀/선언·파일해시와 문서구조를 대상으로 하며 동작시험이나 TIA 컴파일을 대신하지 않는다. 원본 build/test/generator는 실행하지 않았다. 새 코드·시뮬레이터·PLC·현장·보호값·SEJIN·공통 대장·배포 기록 변경은 0이다. 쓰기 범위는 본 MD와 `extracts/SYS-ALARM/`뿐이다.

|상태|결과|
|---|---|
|documentation|complete_with_gaps, SYS-ALARM 1 ID 초안|
|static_review|핵심 원본 정적 대조·선정 해시·자체 문서 검사, 독립 제품 검토는 별도|
|ui_records|not_run; 도면/래더 비교 UI, 선택 복원, 전후 비교, 사용자 보고서/PDF 기능 통합 검증 없음|
|publication|not_published; 사용자 전달은 부모가 담당|
|tia_compile / live_cpu / field_recovery|모두 not_performed|

누락: 실제 HMI ACK 정책/화면 이벤트/로그, 현재 CPU/호출순서·리텐션·기동초기화, Word/간접/외부 writer 전체, FC109 내부 범위/환산, 실제 siren/램프 모델·명판·소리/점멸, inverter별 reset 부하접점·결과응답, 모든 개별 설비 알람 완전성. 새 자료가 없는 실물 보류를 반복 조사하지 않는다. 다음 필요한 자료는 현행 온라인 프로젝트/주소 내보내기와 승인 HMI 이벤트 목록, FG17 현장 단자/장치 명판 대응이다.

### 조사 계수와 의미 검토 범위

선언 명명 검색은 decoded-original XML 전체에 대해 수행했지만 검색계수는 의미 검토 완료수가 아니다. `named-declarations-search.json`에 파일수·선언 hit·NID/UID/AK를 보존했다. 별도 추출 18개 FlgNet 중 핵심 의미 대조는 0005,0031,0033,0151,0152,0153,0154,0155,0158,0355,0457의 11개, 대표/부분 대조는 0397,0539,0540의 3개다. 0148은 초기화/ENO 형태와 원문상수만 확인한 부분검토, 0401은 HMI 출력 미러 식별, 0156/0157은 보고/계수 소유 경계 식별이다. 선언 파일 전체 각 항목·모든 알람 망의 의미를 검토한 것으로 집계하지 않는다.

이름 기반 검색은 무명 절대주소·Word/블록전송·간접참조·HMI 외부 writer를 완전하게 찾는 검사가 아니다. 0577과 0684의 추가 Set 사용처는 범위 경고로 기록했으며 모두 재해석했다는 주장을 하지 않는다. 원본/중지 자산 해시는 보존 확인이고 그 파일들의 실행·의미검증이 아니다.

### 실제 단계 시각 UTC

- 2026-10-11 11:44:15 작업 배정 수신·BATCH11 지시/범위 읽기 시작.
- 11:44:25 고정 표준·기존 초안 인덱스 확인, 원본 선언 탐색.
- 11:45:32~11:45:55 0151~0155/0158·0005 선언/핀·타이머/Word 대조와 첫 FG17 렌더.
- 11:46:03 FG17 실제 이미지 확인, HMI·호출·복수 쓰기 검색.
- 11:47:04 FG135/FG143 렌더, 11:47:14 두 페이지 실제 이미지와 footer 검토.
- 11:48:17 DB3 범위 밖 인버터 경보 선언 대조 완료, 11:48:32 본문 작성 시작.

## 부록 선정 원본 SHA256과 고정 Git blob 목록

아래 전 항목은 고정 커밋의 blob 내용과 로컬 파일 바이트를 비교한다. stopped_asset_hash_only는 해시만 읽고 실행/행동검사하지 않았다. 전체 명명 검색 695 XML과 선정 근거 파일은 서로 다른 집계다. 해시 수는 의미검토 수가 아니다.

|원본 상대경로|SHA256|Git blob|내용일치/범위|
|---|---|---|---|
|`VERSION.json`|`5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7`|`fffb51663b7705aec91cb119ca80ee943a4ce758`|true / selected_evidence|
|`all-in-one/assets/program-model-data.js`|`52f8199371e3399b7c0d44ab5469f0472aced79d56bbef2887f7625f5d2aff0f`|`38f34b0caa380a16ccad6f6f1e234a2fdf23f327`|true / stopped_asset_hash_only|
|`all-in-one/assets/simulator-workspace.js`|`3a6dfc618ff7e7b238f2671dc85d65704f33093a18eac879d86081d92c31e8bc`|`97c2c831c77a9699fff0e0960b3bc1b7d93d45b3`|true / stopped_asset_hash_only|
|`all-in-one/assets/virtual-plc.js`|`5f1876052dc0067b1f010af0dfc941946e37003167481731293615d9c1c36dbc`|`0bd9eceb54365a91214a37c5601b5067c39a3f75`|true / stopped_asset_hash_only|
|`all-in-one/registers/program-model.json`|`6203479c086b15bada12ac9d7e37db9280234ec26f1ea6091d7211dc09a577c5`|`9860b10f008d3a5ae714be50d77b703dfec32f3a`|true / stopped_asset_hash_only|
|`all-in-one/registers/virtual-plc-test-results.json`|`a6b389f797f9a8b5ffe6928b8420f55c4cc459a327b0b48d716079d2eca6dd64`|`757dd50e45184568facb8ff62900b39d3ce848d1`|true / stopped_asset_hash_only|
|`all-in-one/sources/Electrical_Rev2.pdf`|`5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6`|`f610fd7c7ce14ae951b00cff57b969259bfb389d`|true / selected_evidence|
|`all-in-one/sources/decoded-original/0005-FlgNet.xml`|`10a9e0520c4a7f68768161eaea93e0b160a9ae694106b8424a046a330675ba24`|`f6a165cdda102a7aebd7099b38f36148c31c2c92`|true / selected_evidence|
|`all-in-one/sources/decoded-original/0031-FlgNet.xml`|`76385eab8f8f72b9faa16f7cf8905f395591b18c0a9ee9e6d7dd085a38c45c65`|`653d27572de6beedcf3eb6c95702bb119a8b567f`|true / selected_evidence|
|`all-in-one/sources/decoded-original/0033-FlgNet.xml`|`e7fc5601889297a84fcc6b5601a3e0acba420b9c9adb8b37c60277a0fb5cb108`|`b8a89efcb38999950739e0462830d03a94d57c08`|true / selected_evidence|
|`all-in-one/sources/decoded-original/0047-IdentXmlPart.xml`|`2e53bb895dd1ad2a74efaeb1ef16dfd61e62b1b2d7aa34cec8612f1b9cb0928e`|`3dc282f149a21fdf76d5521ef1c833be63b578b4`|true / selected_evidence|
|`all-in-one/sources/decoded-original/0048-IdentXmlPart.xml`|`d8e8687de7271bd294c2b62b33d789700af9d5014d82b130141988c4d479253d`|`64fc5a7f1ad33f3b901b00f0d22d23578ffabff8`|true / selected_evidence|
|`all-in-one/sources/decoded-original/0050-IdentXmlPart.xml`|`f7ceb0408380d3fad2df3bbf5c663c393b57d1ce156af7a587e14c6b1eb701e3`|`9a94a69077a225b05da86a8118b5ec1622dcc629`|true / selected_evidence|
|`all-in-one/sources/decoded-original/0148-FlgNet.xml`|`1d80e1bbf1c82dcc4dd18628c35935bbd55a17b5be9c1ca7bfb249600d154313`|`3069ae3b5fa16ed10a64c149b6cf5cb5ace423b3`|true / selected_evidence|
|`all-in-one/sources/decoded-original/0151-FlgNet.xml`|`227627d165c6240a4c15b62fd4e4c8d7a621c15f35319cb424601df5cc52c904`|`8e8a9801d1f57180fc3747f6515c0353f38f7dc5`|true / selected_evidence|
|`all-in-one/sources/decoded-original/0152-FlgNet.xml`|`2b6165460f06a52de56afcb4d65ed163d64320e24af1b194e934a4d7c6bfe49f`|`dd8e35b98043d9d0f230351352273eac1d783990`|true / selected_evidence|
|`all-in-one/sources/decoded-original/0153-FlgNet.xml`|`3d3a236a66a7a5c9b8e2d1e15da63cc943ba5cd266949583cbac6ffbb2f88bc6`|`d50223c45f5eb1d1c1d3530b41db1e79ad6c71f3`|true / selected_evidence|
|`all-in-one/sources/decoded-original/0154-FlgNet.xml`|`b0a163ffa382b722eaa34df4bdc4c3dd06039b296b791d26d68639a7b0502746`|`ce5ea87daabd1c234cd5b94dd1a3465d878f658b`|true / selected_evidence|
|`all-in-one/sources/decoded-original/0155-FlgNet.xml`|`fd669dc6d8bc9e2486fda4691bf91927c195fd5cb1b6ee57535b52ec9b40e3c6`|`f62a70e37c3ab5e979881280cb164461141f0ca5`|true / selected_evidence|
|`all-in-one/sources/decoded-original/0156-FlgNet.xml`|`67a008f612f8f278825b3f4f1b8298460272b653504e3c112415760ac28e4d2d`|`474e4c389087f414993bd362ba9bf093ce72d9b7`|true / selected_evidence|
|`all-in-one/sources/decoded-original/0157-FlgNet.xml`|`ba7e71fc52ea96bcc2faf598f00a38a7516a1bb0fa7a09b33fbce7ea57611bf7`|`fbbd16ae3a0fbc4ed3574ffa047738d2b12d6b05`|true / selected_evidence|
|`all-in-one/sources/decoded-original/0158-FlgNet.xml`|`d3f3adebc3d990b85c5d4c294906ae3bc3dafebb49d25b030bf9cc2ccf905651`|`233ccf8f9d82ffffa498e04cbdcd3de07115c1db`|true / selected_evidence|
|`all-in-one/sources/decoded-original/0355-FlgNet.xml`|`73592d33f8b3a71effeb36f25427c76e931485e7ce31f5c81f144ddae83c4247`|`54f7a267c9b44c325fd5af31ea78736049d8b1ef`|true / selected_evidence|
|`all-in-one/sources/decoded-original/0397-FlgNet.xml`|`bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834`|`4ab8370493c4e28fc1eabeeebe2743d27f0c4021`|true / selected_evidence|
|`all-in-one/sources/decoded-original/0401-FlgNet.xml`|`60171c213e666de544077b7e4b497675813f7c0e75df85a3e76ab1def49b04ae`|`aadefbd35d305dd4a1146bf383b988a903802bf4`|true / selected_evidence|
|`all-in-one/sources/decoded-original/0457-FlgNet.xml`|`498e0618c56b6a898373d4fa4745e749d0654da17b1f1cd148e9d9617dccb86d`|`dcba3137465522e263742251b0e00159b2be090d`|true / selected_evidence|
|`all-in-one/sources/decoded-original/0539-FlgNet.xml`|`d118d41f5007b112770c77fb33e8c84c2cb0e529e00d781d8837030196a015a5`|`11d48a289d9d3cc74088d9bbdbf230aca456179a`|true / selected_evidence|
|`all-in-one/sources/decoded-original/0540-FlgNet.xml`|`c05d5c1db35f1659992cae845cbcad515bbc34f00089169c0722076db9d77735`|`6b9a166d8fdf80bb52c63e90b794d69aaf34a919`|true / selected_evidence|
|`all-in-one/sources/decoded-original/0564-IdentXmlPart.xml`|`2aed17fa02d19b0a081023282841aa561d6a2dca3e393284da3622b967af00b1`|`c4b1f2cb191970cfce1cce59cb290a9f1f934c37`|true / selected_evidence|
|`all-in-one/sources/decoded-original/0565-IdentXmlPart.xml`|`0f7f970faa6c456f2bb032b1a2072a2f52db1e03fc77bd8d35d4583deeaf1149`|`c2e3e2d57c94c5da864f6e172f0a7a925da942d6`|true / selected_evidence|
|`all-in-one/sources/decoded-original/0566-IdentXmlPart.xml`|`a1914c7ae085acc1f949a649979824bec8b46fcd78a8055318272a1eb5a45265`|`348e6fccf44a8497f58f73e89ec98e892b2df436`|true / selected_evidence|
|`all-in-one/sources/decoded-original/0567-IdentXmlPart.xml`|`5d428b5d5a2b0f4649dbbbb4e4f060a9d89a107e9cf4b6139d8f003c4371347e`|`48d2fdc3a37b692bfda5234b3cd84c48269552f2`|true / selected_evidence|
|`all-in-one/sources/decoded-original/0568-IdentXmlPart.xml`|`4ea2540c76f86ab5b17a30c7c9182cc0026bc6b05e605eddcd4af6fc3b919f89`|`c3b9bb052c2200805c3d0af5237d41ebaafaaad5`|true / selected_evidence|
|`all-in-one/sources/decoded-original/0569-IdentXmlPart.xml`|`2e77bb83cf9a7aecd228dac33fe1c897e1149f2063786f4f4e54c66be618a2c7`|`d58446112989460d247fc9f2e1b39bb7e4ada67d`|true / selected_evidence|
|`all-in-one/sources/decoded-original/0577-IdentXmlPart.xml`|`511e01fae619dc385357908a1ac62030dbdfd5f5399bd4c22bc58bebbfc3bf47`|`a505ebf7efd05a85850dc29559a4f71242bacae3`|true / selected_evidence|
|`all-in-one/sources/decoded-original/0621-IdentXmlPart.xml`|`a63e2b97ea9eb2691cb478666afed77fc58a2da2f8170422dc09e24b102c88ee`|`844516839e55f8bf231a18630e010b912190664e`|true / selected_evidence|
|`all-in-one/sources/decoded-original/0622-IdentXmlPart.xml`|`f0b997f1246d76cff71de2160eb617caa936e6987bdf43c73f55cdcf77dccdb6`|`3b1ae1987950d0754aec37282960b314e9913cd3`|true / selected_evidence|
|`all-in-one/sources/decoded-original/0627-IdentXmlPart.xml`|`08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb`|`61ebc0abbb2ca160e11e1da400a3f14a397d8bc5`|true / selected_evidence|
|`all-in-one/sources/decoded-original/0628-IdentXmlPart.xml`|`9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd`|`170ca5c72599edc7ea7eefe651c3680ce325e76a`|true / selected_evidence|
|`all-in-one/sources/decoded-original/0629-IdentXmlPart.xml`|`67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972`|`058129bb01e27f7a6a0d0293f332d745e5bab74e`|true / selected_evidence|
|`all-in-one/sources/decoded-original/0632-IdentXmlPart.xml`|`fd162c603476c2cac899010cee7a8ee382b6092c115135e3ac1007ae71c544e9`|`600935fa8d394c0d247ea20040d5dfff4f05b500`|true / selected_evidence|
|`all-in-one/sources/decoded-original/0656-IdentXmlPart.xml`|`0dbc45e84732a8848f17b094ea08ab8578dbf240bfe15cd7086859395c27c592`|`9bfb9842e55901bab9a71d1ac03158467dfbb1bc`|true / selected_evidence|
|`all-in-one/sources/decoded-original/0657-IdentXmlPart.xml`|`0f70cda60a6b1a17175876d58e25b2686952642de6cffb21213aeef8b347a22b`|`e625f3d8999c7be7d88c50eab0d93107117b58ec`|true / selected_evidence|
|`all-in-one/sources/decoded-original/0664-IdentXmlPart.xml`|`68c614e1c6a7fcadeee3f0b2ddc54910c3b337e66074d7a113b9cbc834c271ed`|`7ce2f1315d5a21d6b77869a59fc9fcb2f17e90e6`|true / selected_evidence|
|`all-in-one/sources/decoded-original/0682-IdentXmlPart.xml`|`25c7aeb1bfa29c178eaa396db33d4eb6d2d29b9a3f2eb965fa61fae8ce7f1092`|`61182411e912941161eccf4e90c1f174e5379f0a`|true / selected_evidence|
|`all-in-one/sources/decoded-original/0683-IdentXmlPart.xml`|`0c9b569d041cd5babbbeded8a3bdc5d3754927125756b6ac54b7cb991b22fc22`|`662acdb9a06c0ba1c0027e7dd215a28f07d3f02b`|true / selected_evidence|
|`all-in-one/sources/decoded-original/0684-IdentXmlPart.xml`|`6e9b3f173184adcddca503e81e2649022734b6ea3639c1d5ddaf0a08bac00208`|`d67b98b5d5516e0330aae5cfdbee41a3e09206e1`|true / selected_evidence|
|`all-in-one/sources/decoded-original/0685-IdentXmlPart.xml`|`2003d5741a0d707755c5e6e8b737fa106414b87b5b431b97271d9f1a5d343448`|`86bda988d9efedba92ba2f3e4877497d9eb5230a`|true / selected_evidence|
|`all-in-one/sources/decoded-original/0686-IdentXmlPart.xml`|`b450d8ff22f0fffd7a214b2a696af28a03a27834ebf862bfaa822dc9bfb3c8d4`|`8c152d926692a8e15973c980e08e338d29411814`|true / selected_evidence|
|`all-in-one/sources/decoded-original/0688-IdentXmlPart.xml`|`ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda`|`463585759f1ecd94f32362b4fefb000a152f5773`|true / selected_evidence|
|`all-in-one/sources/decoded-original/0692-IdentXmlPart.xml`|`bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037`|`737785d03b5fad43c5b4d451955726d800edb1c0`|true / selected_evidence|
|`all-in-one/sources/decoded-original/identifier-declarations.json`|`0f74123ad80664acdeeb10c29f3e1e73a98d76e5d22169723977371a88768944`|`47e3fed72075945b05f7fc84112b5609551b6ef8`|true / selected_evidence|
|`all-in-one/sources/decoded-original/network-map.json`|`c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60`|`424430b6b953e43138e5d0a18ca40c949e21cfa1`|true / selected_evidence|
|`docs/equipment-standard/INVENTORY.json`|`720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc`|`587c3748ad9224718f95ba06463fee913dae231d`|true / selected_evidence|
|`hmi_plc_tags.csv`|`a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404`|`cf4c0650e7c7baac350dcb89909b808435704880`|true / selected_evidence|

선정 원본 55개 모두 고정 Git blob 내용 일치. 원본 sources 보존 인벤토리 712파일, XML 명명검색 695파일/29개 선언 hit. 이 숫자를 의미검토 완료수로 사용하지 않는다.

## 자체 검사 결과와 인계

2026-10-11 11:53:21 UTC 자체 XML/문서 검사 종료0, 단언124개 통과/실패0. 검사는 고정 HEAD·Git clean, Part 종류·핵심 Wire핀·NOT, 선언 AO/9 Word 범위, 7영역·선정55개 해시/고정 blob의 MD 포함, PDF 렌더 존재를 대상으로 했다. 실제 3페이지의 시각 확인은 위 단계 기록대로 별도 수행했다. 저장 파일은 `extracts/SYS-ALARM/self-check.json`, `source-hashes.json`, `source-preservation-inventory.json`, `named-declarations-search.json`과 자체 정적 추출/검사 스크립트·핀 원문·렌더다. 보존 인벤토리712파일은 말미 바이트 목록이며 의미분석712건이나 실행검사712건이 아니다. 선정55파일의 고정blob 내용일치와 source Git clean을 확인했다.

11:53:21 이후 최종 문서 읽기에서 HMI 이벤트 미확정, 9Word 범위 누락, Q7.6 도면상충, 추가 Reset/STOP_HORN writer, 미해석 범위를 다시 점검했다. 본 초안을 로컬 통합/독립검토에 전달하되 검증 미수행 영역과 기존 설비 소유를 보존한다.
