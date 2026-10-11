# CH01 냉각기 — Dots 독립 원본 조사 초안

> 작업3의 클라우드 조사초안. 로컬 2차133 통합·게시 대상에 추가하지 않는다. 문서의 정적 근거와 현재 CPU·실물·냉각 성능·현장 복구는 별개이다.

## 1. 설비·자료 기준

- 대상: catalog_id **CH01**, 냉각기, motor, 연소·열회수, 부모 없음, 우선 P키 없음. INVENTORY.json의 phase2/planned/baseline/not_assessed를 변경하지 않았다.
- 조사 기준: **v1.12.0 / abcf31c5030bc7ef8749ed8e869a857f2387a28a**, `source-mv06` 읽기 전용 사본. 작업 시작 2026-10-11 09:25 UTC. 이 초안이 이후 배포판의 상태를 보증하지 않는다.
- 작업3 분모는 전체248에서 우선대응18·기존제외90·부모하위보류7·영구중지1을 뺀132이다. 원본 phase2 133과 다른 조사 overlay이며 대장·분모·버전을 수정하지 않았다.
- 적용: GME-STD-1.0.0, 저장소 AGENTS.md, gme-equipment-rollout/SKILL.md, WORK-STANDARD.md, WORK-ITEM-TEMPLATE.md, INVENTORY.json 및 GME-CATALOG-OVERLAP-REVIEW.md. 고정 저장소에 INVENTORY.md는 없으며 실제 JSON을 확인했다.
- 이번 작성물은 이 초안과 CH01 전용 읽기 추출·렌더·해시 기록뿐이다. 공통 코드·공용 추출파일·대장·버전·배포·사용자 운영기록·SEJIN 자료·PLC·현장·보호값을 변경하지 않았다. 시뮬레이터 작성·수정·생성·실행·행동시험은 하지 않았다.
- 실행 모델/추론 설정은 조사 환경에서 별도 확인할 수 없어 미확인. 요청 모델을 실제 실행 모델로 추정해 적지 않는다.

### 1.1 이름과 제어 소유의 경계

1. Electrical_Rev2.pdf FG50/PDF51의 **CH-01/M24**는 3상 전원·접촉기 기동·접촉기 응답 회로이다. FG84/PDF85의 **CHILLER REMOTE START**는 별도 릴레이 접점이다. 이 둘을 하나의 Q 신호나 동일한 실행 확인으로 합치지 않는다.
2. P&ID 1684n002I PDF1은 CH-01과 FN-01 사이 배관, M24 및 M30/P2A를 표시한다. CH01 전원 공급, 원격 명령, 실제 냉각수 순환·냉각 성능은 서로 다른 관찰 대상이다. P&ID의 M30을 CH01의 새 PLC 출력으로 만들지 않는다.
3. `Memory encoder.Encoder_CH01`과 `Encoder_CH01_10`은 이름에 CH01이 있지만 원본 **0513, LAD1763, 제목 data management mv02**에서 MV02_Close·Coeff_TRASM_MV02·Pot_MV02로 연결된다. 냉각기 위치계·속도 피드백·PID로 가져오지 않는다. §3.6에 오배정 방지 근거를 남겼다.
4. FN01의 TC04/TC05·ZT01 및 FN01-FAN을 CH01 전용 센서·고장·구동으로 복제하지 않는다. 공정 연관은 소유 동일성의 증거가 아니다.

### 1.2 자료 시점과 충돌

| 자료 | 실제 확인 | 해석·미확정 |
|---|---|---|
| Electrical_Rev2.pdf FG50/PDF51 | 제목 CHILLER CH-01, 날짜27.05.2024, M24 `kW 6 A 11`, 50QM1 `10–16A` | 도면 표기이며 현재 명판·실제 차단기 설정값 미확인 |
| 같은 PDF FG120/PDF121, FG139/PDF140 | Rev2, 17.03.2025 | 전체 PDF 이름으로 다른 모든 페이지에 Rev2를 소급하지 않음 |
| 같은 PDF FG84/PDF85, FG142/PDF143 | 날짜27.05.2024, 별도 개정 기입 미확인 | 원격기동 페이지·출력 모듈 페이지의 관측 상태 |
| PID_1684n002I.pdf PDF1 | 도번1684n002, Apex I, 원도일06/04/2011, 최신 표시 I 15/01/2013. CH-01 **5 kW** | 전기도면의6 kW와 상충. 개조·동일성·현행 정격 미확정. P&ID TC04/05의70°C도 현재 설정·안전 한계로 적용하지 않음 |
| Electrical_Can_Decoating_20241118.pdf PDF32/51 | 24.11.11 first draft design, 승인란 완료 증거 없음 | 참고 설계·케이블 일정이다. 승인 as-built·실측 증거가 아님 |
| PLC 백업 | 고정 저장소 원본 XML 선언·핀 | 현재 CPU와 일치 확인, TIA 복원/컴파일, 실제 실행 미수행 |

### 1.3 7영역 적용표

| 영역 | 상태 | 작성 위치·남은 경계 |
|---|---|---|
| 설비·자료 기준 | 적용 | §1, 냉각기와MV02 이름 충돌 및 정격 상충 |
| I/O·HMI | 적용·일부 근거 미확보 | §2, 주소/Word전달/HMI 호출. 화면 이벤트·현재 통신 미확정 |
| 제어 구조 | 적용 | §3, ServiceBit·두 출력·자동 요청·호출·복수쓰기. 냉각기 내부 제어는 자료 미확보 |
| 전기 전달 경로 | 적용 | §4, 전원·명령·피드백·원격 접점·케이블 양 끝점. 현장 미확정 |
| 알람·복구 | 적용 | §5, 2초 SD와 Set/Reset. 실제 복구·상위 전체 영향 미확정 |
| 증상별 수리 | 적용 | §6, 읽기 관찰/배제 기준. 현장 조치 실행 없음 |
| 완료 기준 | 적용 | §7, 문서·정적·화면·게시·TIA·CPU·현장 상태 분리 |

## 2. I/O·HMI

이하 `D/`는 `all-in-one/sources/decoded-original/`이다. XML은 일부 한 줄 저장이므로 행 번호 대신 **파일·NID·RID·UID·Part·Wire·핀**을 사용한다. NID는 선언 내부 네트워크 식별자이며 화면 색인 순서와 다를 수 있다. AO는 비트 오프셋이며 Timer AO는 타이머 번호로 구분했다.

### 2.1 원본 선언 주소

| 신호·성격 | 원본 선언 | 정적 주소/형식 | 해석·미확정 |
|---|---|---|---|
| Flag.M_CH_01 기동 요청 | 0604 GlobalAccess RID123, AO12 Bool;0603 DepDBBlock Flag RID2/TOD N2. 0577 RID55에서 자동쓰기 | **DB2.DBX1.4 Bool** | 물리 출력·운전 확인이 아님 |
| Start CH01 | 0602 SimpleAccess RID124, Output AO25 Bool, NID24 UID749 Write | **Q3.1 Bool** | FG50의 A3.1과 대조. 과거 주석 `A53.4`를 주소로 쓰지 않음 |
| Enable start chiller | 0602 RID127, Output AO48 Bool, NID24 UID753 Write | **Q6.0 Bool** | 원격기동 릴레이용. Q3.1과 별도 |
| CH01_Fbk 원시 입력 | 0613 SimpleAccess RID194, Input AO32 Bool, NID32 UID1774 | **I4.0 Bool** | 도면상50KM1 보조접점. 실제 냉각 성능·물 유량의 직접 증거 아님 |
| Inputs.CH01 Run 처리 영역 | 0657 GlobalAccess RID288, AO32 Bool;0655 Inputs RID247/TOD N13 | **DB13.DBX4.0 Bool** | I4.0과 별도 저장영역. 전달·다른쓰기 확인 필요 |
| Allarm.CH_01_FAULT | 0657 RID92 AO12 Bool;0655 Allarm RID10/TOD N3 | **DB3.DBX1.4 Bool** | 래치 고장;HMI DB11.X38.1과 직접 동일 주소 아님 |
| ServiceBit | 0602 RID264, Memory AO8000 Bool, NID24 UID24 | **M1000.0 Bool** | 전단 허가 접점. 이름만으로 정비 모드·라이선스·항상TRUE라 확정하지 않음 |
| ON | 0602 RID1, Memory AO0 Bool;NID24 UID745 | **M0.0 Bool** | 심볼 이름이 상수TRUE라는 증거는 아님 |
| Tag_123 | 0602 RID126, Timer AO113, NID24 UID751 Write/752 Read | **T113 Timer** | 원격기동 SD, literal S5T#10S와 구별되는 타이머 자원 |
| Tag_65 | 0658 RID90, Timer AO70, NID22 UID764 Write/765 Read | **T70 Timer** | 운전응답 고장 SD, S5T#2S |
| hours motors.CH_01_MIN/HOUR | 0615 RID196 AO992 Int/RID198 AO1008 Int;0614 RID5/TOD N9 | **DB9.DBW124 / DB9.DBW126 Int** | 누적 방식은 §3.5. HOUR를 정상 가산계로 가정하지 않음 |

### 2.2 원시 입력의 Word 전달과 대체 쓰기

**0397-FlgNet.xml, LAD1070, NID1**:

- rail W21→Move22.en; Move22.eno W34→Move27.en; Move27.eno **W41→Move35.en**. 앞 Move의 ENO 연결을 지우고 Move35를 무조건 실행으로 쓰지 않는다.
- **ORef36/RID10 → W39 → Move35.in**:0627 SimpleAccess Tag_180, Input AO32, OD S16/Word, 즉 **IW4**.
- **Move35.out1 → W40 → ORef37/RID11**:0629 GlobalAccess Word AO32, BAD BIRID4;0628 Inputs DepDBBlock RID4/TOD N13. 즉 **DB13.DBW4**.
- 이 Word 범위 안에 I4.0과 DB13.DBX4.0이 포함된다. 이름만 대응한 것이 아니라 주소·Word폭·쓰기핀을 대조한 전송 근거다. 현재 실행주기·값 일치까지 보증하지 않는다.
- 기존 **0404-FlgNet.xml LAD1084, Part46/Coil, W61/ORef52**에도 `Inputs.CH01 Run` 쓰기가 있다(0635 RID100 AO32, NID3 UID52 Write;요청 Flag.M_CH_01은 UID51/RID117). **영구중지된 과거 simulation 블록의 정적 다른쓰기 존재만 기록**한다. 실행·활성 여부를 시험하거나 정상 현장 응답으로 사용하지 않았다.

main **0030 LAD1613/NID19**는 Recipes Handler21.eno W32→HMI23.en, HMI23.eno W33→HMI Output25.en, HMI Output25.eno W42→**Contact37 NOT Simulation(1)**, W43→HMI Inputs28.en이다. 0692 RID140 AO1440=**M180.0**이다. 0688 CodeBlock UID29/RID135/TOD N15가 HMI Inputs FC15를 확인한다. 화면의 단순 순서나 bool 이름만으로 현재 갱신을 보장하지 않는다.

### 2.3 출력 상태의 전달 방향

**0401 LAD356/NID1**은 출력 Word를 DB14 Output에 옮기는 경로다.

- 0632 RID28 Tag_281/Output AO16/Word(**QW2**) → ORef35/W59 → Move23.in → out1 W61/ORef36(0633 RID50 AO16/BAD BIRID26) → **DB14.DBW2**. Move23.en은 선행 Move22.eno W57.
- 0632 RID32 Tag_283/Output AO48/Word(**QW6**) → ORef39/W64 → Move25.in → out1 W66/ORef40(0633 RID52 AO48/BAD BIRID26) → **DB14.DBW6**. Move25.en은 rail W21.
- DB14는0064 DepDBBlock Output RID26/TOD N14. Q3.1·Q6.0의 표시용 Word 범위를 확인한 것이며 **DB14가 물리 Q를 쓰는 역방향 명령**으로 바꾸지 않는다.

### 2.4 HMI 설정과 원본 호출의 결속 한계

`all-in-one/sources/hmi_plc_tags.csv`의 실제 설정3행(Access Name PLC):

| 태그 | 설정주소 / 내부ID | 판정 |
|---|---|---|
| CH_01\Flag | DB2,X1.4 /0019C | Flag.M_CH_01 선언과 주소 범위 일치. 실제 버튼 이벤트·허용쓰기·사용 화면은 미확인 |
| CH_01\RispostaA | DB11,X38.0 /00304 | 표시 설정. 원시 I4.0이나 DB13 bit와 직접 동일하지 않음 |
| CH_01\Allarme1 | DB11,X38.1 /00348 | 표시 설정. Allarm.CH_01_FAULT DB3.X1.4와 직접 동일하지 않음 |

**0373 LAD1196/NID19**: rail W21→CRef22.en;CodeBlock UID23/RID1은0623 FCBlock **HMI Standard Motors, FC1**.0624 BlockInterfaceInfo RID638는 Ingresso_run·Allarme1~5=Input Bool, Risposta·Comulativo_allarmi=Output Bool를 확인한다.

| 호출핀 | XML 끝점 | 확인·한계 |
|---|---|---|
| Ingresso_run | W37/ORef24/RID673 | 0625의 Inputs DB13 부모 종속 참조는 확인;대상 멤버 선언·바이트의 직접 결속 미확정 |
| Allarme1 | W39/ORef26/RID260 | Allarm DB3 부모 종속 참조 확인;CH01_FAULT 멤버의 직접 결속 미확정. 다른 파일0638 NID16의 동UID/RID TON 후보는 이 호출과 네트워크가 달라 채택하지 않음 |
| Allarme2~5 | W40~43/ORef27~30/RID48 | 0626 LiteralConstant FALSE, NID19 일치 |
| Risposta | W46/ORef33/RID263 | 0625 Motors DB11 부모 쓰기UID33 확인;X38.0 멤버까지 직접 결속 미확정 |
| Comulativo_allarmi | W48/ORef35/RID265 | 같은 Motors DB11 부모 쓰기UID35 확인;X38.1 멤버까지 직접 결속 미확정 |

공통 FC1의0355 LAD331/0621 로컬 선언: Contact23(Ingresso_run, ORef24/W22)→W25→Coil27(Risposta,ORef28/W26); Allarme1~5의 Contact33/36/39/46/30→OR41.in1~5(W42/43/44/48/49)→W57→Coil59(Comulativo_allarmi,ORef60/W58). 이는 함수 내부 의미이며 CH01 호출의 미결속 멤버·원래 화면 이벤트·현재 통신을 대신 확정하지 않는다.

## 3. 제어 구조

### 3.1 CH01 고유 출력과 알람 시 요청 해제

**0255-FlgNet.xml LAD1953/NID24**, 선언0602/0604/0606:

| 핵심 경로 | Part·Wire·ORef 직접 근거 | 해석·미확정 |
|---|---|---|
| 공통 전단 | Contact767 ON(ORef745/W754).out W21→Contact23 ServiceBit(ORef24/W22).out W768 | `ON AND ServiceBit`. ServiceBit 값/작성 주체/현행 허가 의미 미확정 |
| 고장 시 요청 해제 | W768→Contact769 Allarm.CH_01_FAULT(ORef746/W755)→W770→**RCoil729**;operand ORef747/W757 Flag.M_CH_01 | `ON AND ServiceBit AND FAULT`일 때 요청 Reset. 알람이 있다고 모든 상태에서 무조건 Q를 끄는 독립안전회로로 설명하지 않음 |
| 전원 접촉기 명령 | W768→Contact771 Flag.M_CH_01(ORef748/W758)→W772→**Coil736**;operand ORef749/W759 Start CH01 | `Start CH01 = ON AND ServiceBit AND M_CH_01`의 정적 경로 |
| 원격기동 타이머 | 같은 W772→**SdCoil739.in**;value ORef750/W760;operand ORef751/W761 | 0606 RID125 S5Time, SV S5T_x0023_10S/V4352 → **S5T#10S**, Tag_123 T113. 출력 자체와 타이머 자원을 분리 |
| 원격기동 출력 | 같은 W772→Contact773 Tag_123(ORef752/W762)→W774→**Coil744**;operand ORef753/W764 Enable start chiller | `ON AND ServiceBit AND M_CH_01 AND T113` 정적 경로. Q6.0은 Q3.1의 단순 별칭이 아님 |

이 네트워크에 CH01 전용 수동 selector·local start 입력이나 별도 인버터 속도지령을 발견하지 못했다. 이는 전체 설비에 현장 수동 기능이나 냉각기 내부 인버터가 없다는 증명이 아니다. Q3.1·Q6.0의 직접 Bool 쓰기는 위 두 Coil로 식별했고, 같은 출력 영역의 Word 접근은 §2.3의 읽기다. 블록 미호출 시 출력 최종값, 프로그램 밖 HMI/강제/통신 쓰기와 현재 CPU는 미확정이다.

### 3.2 자동 시퀀스의 세 요청쓰기

| 네트워크 | 정확한 경로 | 원문 해석 |
|---|---|---|
| 0164 LAD1843/NID3 예열 | Contact785 ON(ORef588/W668)→W786→Contact22 **NOT Emergency_module_fault**(ORef23/W21)→W32→Eq400 Tipo_preset=1(ORef590/591,W670/671)→W33→Contact823 Auto_ON1(ORef824/W826)→W672→Eq509 Tempo_presetting=28(ORef635/636,W736/737)→W738→**RCoil517**,ORef26/W25 | 예열28은 **Reset**. 이름이 auto start라고 Set으로 고치지 않음 |
| 0165 LAD1844/NID4 생산 | Contact1145 ON(ORef932/W1017)→W1146→Contact1154 **NOT Emergency_module_fault**(ORef1155/W1157)→W21→Contact1147 Auto_ON1(ORef933/W1018)→W1148→Eq737 Tipo_preset=2(ORef934/935,W1019/1020)→W1021→Eq846 Tempo_presetting=46(ORef983/984,W1095/1096)→W1097→**SCoil854**,ORef987/W1100 | 생산46에서 요청 Set |
| 0166 LAD1847/NID5 전체정지 | Contact1095 Auto_ON1(ORef983/W1028)→W26→Eq881 Tipo_preset=5(ORef984/985,W1029/1030)→W1031→Eq901 Tempo_presetting=5(ORef992/993,W1040/1041) **OR** Contact1130 Emergency_module_fault(ORef1131/W1133);OR51.in1 W52/in2 W53→out W1042→**RCoil905**,ORef994/W1043 | `Auto_ON1 AND Tipo_preset=5 AND (Tempo_presetting=5 OR Emergency_module_fault)`에서 Reset. 이 분기에 ON 전단을 임의로 추가하지 않음 |

모든 대상은0577 GlobalAccess RID55 Flag.M_CH_01이다. 상수는0578의 RID8=1,52=28,78=2,85=46,22=5와 해당 NID/UID를 대조했다. 순번 값28/46/5를 독립 초 단위 지연으로 단정하지 않는다. DB2.X1.4의 HMI 설정이 별도 존재하므로 요청의 최종값은 주기·인터럽트·HMI 이벤트·다른쓰기 순서 확인이 필요하다.

### 3.3 호출·실행 순서 경계

- **0031 LAD1619/NID6:** Contact282 ON(ORef271/W280), W283→CRef264.en/CodeBlock275.0688 FCBlock RID58/TOD N4=**Allarms1 FC4**.
- **0549 LAD1620/NID7:** Contact350 ON(ORef335/W348), W351→CRef319.en/CodeBlock337.0688 RID67/TOD N7=**Motors1 FC7**. 동일 W351→CRef334.en/CodeBlock347, RID82/TOD N2=**time work motor FC2**.
- **0024 LAD1723/NID4:** Contact188 ON(ORef185/W187)→W189→CRef183.en/CodeBlock186.0067 RID39/TOD N30=**Auto start motors FC30**. 색인 블록명은 `cyc_int2 ogni 1s`이다. 블록명만으로 현재 하드웨어의 정확한1초 호출·우선순위를 검증했다고 쓰지 않는다.
- main 색인에서 알람/모터/시간 호출 순서를 볼 수 있지만 cyclic interrupt·호출 ENO·온라인 구성·실제 스캔 최종값은 미검증이다. 타이머2초와10초를 합산해서12초로 만들지 않는다.

### 3.4 읽기/쓰기 조사 요약

| 대상 | 발견한 직접 쓰기 | 유지할 경계 |
|---|---|---|
| Flag.M_CH_01 | 0164 R517,0165 S854,0166 R905,0255 R729 | HMI DB2.X1.4의 이벤트쓰기 미확정, 실행순서 미검증 |
| Start CH01 / Enable start chiller | 0255 Coil736/744 | 출력 Word mirror는 읽기. 온라인 강제·통신 쓰기 미확정 |
| Inputs.CH01 Run | 0397 Move35의DB13W4 범위, 과거0404 Coil46 | 입력전달 호출 조건 및 영구중지 블록 존재를 분리 |
| Allarm.CH_01_FAULT | 0435 S755/R760 | 같은 스캔 Set/Reset 우선·현재 결과 미검증 |
| CH_01_HOUR | 0318 Move1766,0338 Move2949 | Move1·Move0 사실 보존;누적 가산으로 대체 금지 |
| ServiceBit | 전체 IdentXmlPart 직접선언 검색에서M1000.0 Read만 발견 | 외부 설정·간접쓰기·현재값의 부재 증명이 아님 |

### 3.5 운전시간은 원시 I4.0을 읽으며 HOUR에 Move1을 쓴다

**0318 LAD1030/NID32**:

- Contact1802 Tag_47 T13(ORef1773/W1785)→W1803→Contact1804 CH01_Fbk I4.0(ORef1774/W1786)→W1805→Add1756.en 및 Ge1763.pre.
- Add1756.in1 W1787/ORef1775 CH_01_MIN, in2 W1788/ORef1776 literal1;out W1789/ORef1777 CH_01_MIN. Ge1763는 in1 W1790/ORef1778 MIN, in2 W1791/ORef1779 literal60.
- Ge1763.out W1792→Move1766.en;**in W1794/ORef1780 literal1 → out1 W1795/ORef1781 CH_01_HOUR**. 원본은 HOUR+1 Add가 아니라 **Move1**이다.
- Move1766.eno W1796→Move1769.en;in W1797/ORef1782 literal0→out1 W1798/ORef1783 MIN. Move1769.eno W1799→SCoil1772 Flag_Aggiorna_DB(ORef1784/W1800).
- **0338 LAD1051/NID53:** Contact2987 Tag_48 T17(ORef2961/W2972)→W2988→Move2946 VR_02_HOUR=0. 이 선행 Move의 **eno W2975**가 Move2949.en으로 간다. W2976/ORef2964 literal0→Move2949→W2977/ORef2965 CH_01_HOUR=0. CH01 전용 reset 버튼으로 설명하지 않는다.
- Tag_47/48은0613 RID1/AO13, RID284/AO17이다. 실제 펄스 주기, 시간 단위, 리텐션 및 현재 누적값은 이 네트워크만으로 확정하지 않았다. 원시접점이 들어와도 실제 냉각 공정 운전시간과 같다는 보장이 없다.

### 3.6 Encoder_CH01 오배정 방지

**0513 LAD1763/NID46**:

- EM_OK Contact21(ORef32/W54)→W55→Contact22 **NOT MV02_Close**(ORef56/W33;0678 RID444) 및 CRef30.en.
- Add24.in1 **W59/ORef35/RID195 Memory encoder.Encoder_CH01** + in2 W60/ORef36 fill_unit1.ACT_CNTV1 → out W62/CNT_Act_1. Div25는 W64/ORef39 literal100을 사용하고 Move26→**W68/ORef42 Encoder_CH01_10**.
- CRef30.Analog_input은 **W76/ORef49 Encoder_CH01_10**;Coeff W77/ORef50 **COEFF_TRASM_MV02**, Zero W78/ORef51 **ZERO_TRASM_MV02**, OutValue W79/ORef52 **Data.Pot_MV02**, Out_of_range W83/ORef82 **Allarm.Pot_MV02_OFR**.
- 0676 RID195 AO32 DInt→DB8.DBD4, RID228 AO304 Int→DB8.DBW38(0674 Memory encoder RID191/TOD N8). 냉각기의I4.0·Q3.1·Q6.0 경로와 다른 데이터 흐름이다.
- 0511 LAD1761/NID30의Move922.out1 W955/ORef944도 같은 Encoder_CH01 쓰기다. 이를 냉각기 정전복구 기능으로 가져오지 않는다. MV02 실제 설비/현재 엔코더의 동일성 확인은 해당 독립 조사와 현장 자료의 과제다.

## 4. 전기 전달 경로

원본 PDF 실제 렌더를 눈으로 확인했다. FG는 도면표제번호이고 PDF는1부터 시작하는 파일 페이지다. 도면 선과 원본 단자번호를 기록한 것이며 현장 작업 지시나 활선 측정 허가가 아니다.

### 4.1 주전원·보호·기기 전원

**Electrical_Rev2.pdf FG50/PDF51**:

`8.3L1/L2/L3 (49/9에서, 440V 60Hz 표기) → 50QM1 주접점1–2/3–4/5–6 → 50KM1 주접점1–2/3–4/5–6 → 50U1/50V1/50W1 → XM 50U1/50V1/50W1 → 50QS1 주접점1–2/3–4/5–6 → M24 U/V/W, CH-01`.

- M24의 PE 접속 표시, BLACK FS17 2.5mm², 50QM1 10–16A 및 M24 6kW/11A 도면 표기를 보존한다.
- 10–16A를 실제 설정값으로 정하거나11A에 맞추도록 지시하지 않는다. 현행 부품 모델, 정격, 설정·트립 특성, 배선·보호 협조는 명판/승인 자료가 필요하다.

### 4.2 Q3.1 접촉기 코일 명령

**FG139/PDF140 → FG50/PDF51**:

`+24Vdc10.9 → X21/3031 (4A F 5×20) → 139.1/출력모듈 공통39 → CPU515/MOD14의 A3.1 단자32 → FG50/4 A3.1 → XS37 → 50QS1 보조접점 → XS38 → 선50.1 → 50QM1 보조접점 → 50KM1 A1 → 코일 → A2 → -0Vdc10.6`.

- FG139 출력모듈 공통40의 -0Vdc 연결도 확인했다. 실제 장착 슬롯/모듈 형식은 별도 확인 대상이다.
- 50QS1·50QM1 보조접점의 번호가 그림에서 별도 확정되지 않아 임의13–14/95–96을 넣지 않는다. 전원 주접점번호와 코일A1/A2는 보조접점번호가 아니다.
- PLC Q3.1=1, 모듈 전압, 접촉기 여자, 주전원 전달은 각각 별도 증거이다.

### 4.3 접촉기 응답

**FG50/PDF51 → FG120/PDF121**:

`+24Vdc10.7 → 50KM1 보조접점13–14 → E4.0 (120/2) → CPU515/MOD9, 입력 단자1 → PLC CH01_Fbk I4.0`.

도면의 응답 접점은 접촉기 상태다. M24 실제 회전, 압축기 내부허가, 냉각수 유량·온도차, FN01 베어링 실제 냉각을 직접 측정하는 경로로 서술하지 않는다. 도면의 NO기호와 현장 정상 논리·단선 검출 기능을 동일시하지 않는다.

### 4.4 Q6.0 별도 원격기동

**FG142/PDF143 → FG84/PDF85**:

- 코일측: `+24Vdc10.9 → X21/3034(4A F5×20) →142.1/모듈공통29 → CPU515/MOD15 A6.0 단자21 → FG84/1 →84KA1 A1 →A2 →-0Vdc10.6`. 모듈공통30의0V 연결도 확인했다.
- 부하/외부 허가측: `CHILLER REMOTE START 상단 외부 끝점 → X1/232 → 선84.1 → 84KA1 접점 **5–9** → 선84.2 → X1/233 → 하단 외부 끝점`.
- 확대 렌더에서 접점1도 전환접점으로 그려져 있지만, X1/232로 연결된 단자는 **5**, X1/233로 연결된 공통은 **9**이다.1–9로 기록하지 않는다.
- ORANGE FS17 1.5mm²는 페이지 표기. 외부 냉각기 측 단자명·전압·케이블 전체 번호·접점 허용전류·내부 controller 조건은 이 페이지에서 확인되지 않았다.24V 코일이라는 이유로 외부 접점측도24V라고 추정하지 않는다.

### 4.5 참고 시공도 케이블

**Electrical_Can_Decoating_20241118.pdf**:

- **PDF51**, CANDC-CONS-C001-051, CABLE SCHEDULE(1), 행 **1_15**: `=FLB+CH01-M24A`, FROM **CR** → TO **CH-01 / M24 / CHILLER**, GAC, CV,4core,2.5,SPARE0. 경로100→120/RB→E600, Adjustment10, LEN60. 표의 길이 숫자를 실측치로 바꾸지 않는다.
- **PDF32**, CANDC-CONS-E015-032, FLOW_B ZONE02/CONDUIT PIPING(2), 행 **9**: Pipe22, PULL BOX/도착 M24, DEVICE CH-01/M24, `1_15=FLB+CH01-M24A`, CV2.5/4core. 왼쪽 도면의 분기9→M24와 표를 함께 확인했다.
- 두 표는 같은 케이블 식별자에 대한 일정·경로 표현이며 서로 다른 케이블2개로 세지 않는다. 외부 원격접점 X1/232–233의 장치측 케이블까지 이 전원 케이블에 합치지 않는다. 승인시공도·현장 마킹·현재 길이 확인 대기.

## 5. 알람·복구

### 5.1 CH_01_FAULT의2초 검출과 래치

**0435-FlgNet.xml LAD1800/NID22**, 선언0655/0656/0657/0658:

| 항목 | 직접 핀 근거 | 해석 |
|---|---|---|
| 기동 감시 전단 | Contact785 ON(ORef761/W771)→W786→Contact787 Start CH01(ORef762/W772)→W788 | Q6.0이 아니라 **Q3.1 Start CH01**을 읽는다 |
| 타이머 시작 | W788→Contact798 **NOT Inputs.CH01 Run**(Negated operand;ORef799/W801)→W21→**SdCoil749.in** | `ON AND Start CH01 AND NOT 처리응답`이 SD 입력 |
| 지연 자원·상수 | Sd749.value W773/ORef763,0656 RID28 SV S5T_x0023_2S/V512;operand W774/ORef764,0658 RID90 | **S5T#2S / T70 Tag_65**. 원격기동 T113 10초와 다른 타이머 |
| Set | W788→Contact789 Tag_65(ORef765/W775)→W22→**SCoil755**,operand W778/ORef767 Allarm.CH_01_FAULT | 정적 Set 식은 `ON AND Start CH01 AND T70`. NOT Run은 SD 입력에 있고, Set코일 직전 별도 직렬접점으로 복제하지 않음 |
| Reset | W786→Contact793 RESET_ALLARM(ORef768/W780)→W794→Contact795 FAULT(ORef769/W781)→W796→**RCoil760**,operand W783/ORef770 | `ON AND RESET_ALLARM AND FAULT`. 정상 응답이 되었다는 조건이 Reset 가지에 따로 없음 |

Reset은 냉각기 실제 고장 제거·정상 성능 확인·재기동 완료를 뜻하지 않는다. 조건이 남으면 재발 가능하며 동시에 Set/Reset되는 경우의 현재 우선순위를 실행하지 않고 단정하지 않는다. 이 직접 알람의 정지 영향은 §3.1의 조건부 요청 Reset까지 입증했다. 전체설비 강제정지나 안전회로의 완전성을 이 고장1개에서 추정하지 않는다.

### 5.2 Reset 요청의 공통 출처와 표시

- **0158 LAD930/NID9**: Contact23 `Inputs.Reset_allarmi`(0565 RID57, ORef24/W22)→W29→OR28.in1;Contact26 `Flag.Reset_Allarms_HMI`(RID61,ORef27/W25)→W30→OR28.in2. OR28.out W38→**SCoil33 Flag.RESET_ALLARM**(RID2,ORef37/W36), 같은 가지 RCoil40은 HMI Reset 요청을 해제(ORef43/W42).
- 이 호출의 공통 TOF3초/Reset_Inverter 출력은 CH01 고유 냉각기 reset 핀이라는 근거가 없어 복제하지 않는다. HMI 버튼 위치/이벤트·실제 물리 reset전달은 미확정이다.
- DB3.X1.4는 공통 알람 Word DB3.DBW0 범위에 있다. **0151 LAD927/NID1 Move127.in W194/ORef173**(0565 RID8, AO0 Word, Allarm 부모 참조)은 Word0를 WorkData.W0로 복사한다. **0152 LAD928/NID2 Ne191.in1 W240/ORef220**도 같은 Word0를 읽고 in2 W241/ORef221 WorkData.W0와 불일치(Ne)를 비교한다. 이는 공통 알람감시 연결이며 별도의 CH01 전용 horn·현장 reset 출력은 아니다.
- 직접 표시 주소는 §2.4. FC1 출력 멤버 결속 미확정을 유지하며 HMI에 실제 특정문구가 뜬다고 단정하지 않는다.

## 6. 증상별 수리·관찰 초안

실제 현장작업은 자격 있는 담당자의 정지·잠금/표찰·검전 및 현장 승인 절차에 따른다. 이 문서는 보호장치 우회, 강제출력, 임의설정·전압주입·재기동 지시를 제공하지 않는다. 아래는 이미 확보한 읽기 자료와 안전한 관찰 결과를 비교할 위치이다.

| 증상 | 관찰 위치·비교할 값 | 원인 배제 기준·남은 자료 | 복구 판정에 필요한 증거 |
|---|---|---|---|
| 요청해도 접촉기 명령이 없음 | HMI 요청 설정주소/이벤트, DB2.X1.4, M0.0, M1000.0, DB3.X1.4, Q3.1;0255/0164~166 | ServiceBit 실제 의미, 예열28 Reset·정지 요청·알람Reset과 HMI쓰기 시각 비교. 요청이1이라고 현장 고장부터 단정하지 않음 | 승인된 운전에서 요청→허가→Q3.1 순서를 같은 시계로 확보 |
| Q3.1 표시ON인데50KM1 응답없음 | FG139 단자32→FG50 XS37/38·50QS1/50QM1 보조접점·A1/A2 경로의 담당자 측정/관찰 | PLC값·모듈 상태·코일회로·보조접점·전원 장치 구분;보호기기 임의복귀·우회 금지 | 코일/접촉기/주전원/응답I4.0의 일치 및 보호원인 해결 근거 |
| 전원은 들어왔지만 원격기동이 없음 | Q3.1과 Q6.0, T113, M_CH_01·ServiceBit,84KA1/A1/A2/X1 232–233 | 10초 SD 미완료·허가상실·외부접점회로 단절·냉각기 내부허가 분리.2초 고장타이머와 혼동 금지 | Q6.0→릴레이상태→외부 실제 수신까지 양 끝점 자료 |
| CH_01_FAULT가 발생/재발 | Start CH01 Q3.1, I4.0, DB13.X4.0, T70, DB3.X1.4, Reset 요청 시각 | 원시입력과 처리Word전달·호출조건·다른쓰기 가능성을 분리. 원격기동 10초 전이라는 사실만으로 고장 로직 오류로 단정하지 않음 | 고장원인 제거, 응답전달 안정, Reset 이후 재발없음, 별도 정상운전 증거 |
| HMI 운전/알람과 PLC관찰이 다름 | 원시I4.0/처리DB13.X4.0/DB11.X38.0/.1, HMI통신·시각·품질 | 원래HMI 이벤트·FC1 멤버 결속·갱신주기·통신을 확인. 화면 색만으로 실제 운전 판단 금지 | 동일 시각 캡처와주소·프로젝트 기준의 일치 |
| 응답은 정상인데 냉각이 부족 | 접촉기 응답에 더해 유량/온도차/냉각기 내부 경보·명판·물배관 상태의 승인된 관찰 | I4.0은 접촉기 상태. FN01 TC04/05 또는MV02 Pot값을CH01 직접온도/위치로 바꾸지 않음.제조사 기준 미확보 | 현행 제조사·공정의 승인 성능기준, 실제측정값·안정화 관찰·담당자 확인 |
| 운전시간이 기대와 다름 | I4.0/T13, DB9W124/W126,T17,0318/0338 | HOUR Move1·공통 초기화 ENO 경로 보존.소프트웨어 오류라고 즉시 수정하지 않음 | 현재 승인 프로젝트와 실제운전시간 기록의 비교;정비 주기는 임의 산정하지 않음 |

관찰기록 필수: 관찰자·시각/시간대·CH01 실물ID/위치·프로젝트/CPU 식별·값/단위·수집장치·원본주소·비교시각·제외한 원인·승인된 조치·조치후값·재발여부. 값0과미측정/빈칸을 구분한다. 실제 운영기록·사진은 이 공개조사초안에 넣지 않았다.

## 7. 완료 기준·검증·다음 자료

### 7.1 네 기능과 기록 보존

| 기능 | 이번 상태 |
|---|---|
| 도면·래더 비교 | 조사 연결쌍:0255↔FG50/139,0255↔FG84/142,0435/0397↔FG50/120. 실제 UI에 추가·검증하지 않음 |
| 백업·선택 복원 | 기존 사용자 기록·저장키·미지필드·초안·타설비 기록 보존. CH01 전용 지원/저장·재읽기·재열기 검증 미수행 |
| 기록 전후 비교 | 관찰항목을 문서에 정의했으나 실제 기능구현·합성 QA 미수행 |
| 보고서/PDF | 이Markdown초안만 작성. 프로그램보고서·PDF내보내기·게시를 완료로 표시하지 않음 |

### 7.2 수행한 검증

- 읽기전용 preflight 종료0, **inventory_matches=true**, 고유catalog248/phase2 133 일치. source_byte_changes의 기존2파일은 기준표준대비 파생자료 차이이며 이번 수정이 아니다.
- 핵심 XML·선언·상수·CRef·Word전달·AK Write를 직접 읽고 대조했다. UID/RID가 다른 파일에서 우연히 같아도 NID·블록이 다르면 채택하지 않았다. 추출기의 복수후보는 자동확정 근거로 쓰지 않았다.
- Electrical 원본PDF5쪽(FG50/84/120/139/142), 참고시공원본PDF2쪽(32/51), P&ID원본1쪽 및CH01/개정란 확대를 실제 렌더·시각검토했다. 렌더는원본해시와구별되는 조사파생물이다.
- **78개 근거파일의 로컬 SHA256과 고정커밋 git blob의SHA256/바이트 전부 일치**. 원본 git status --short는 빈 문자열. 전체원본을 복원·컴파일 검증한 결과는 아니다.
- npm/생성기/웹UI/배포/TIA/CPU/현장/시뮬레이터 실행 없음. 중지자산·공통코드·원본/대장/버전·보호값 변경0.

### 7.3 미확정 자료와 수집 위치

1. **현장 식별·정격**: CH01/M24 및 외부 냉각기 controller 명판, 현재 회로·개조 내역. 구 P&ID 5kW/전기 6kW 충돌을 승인 자료로 해결한다.
2. **전원/원격/응답**: 현행 단자대·케이블 마킹, 50QS1/50QM1 보조접점 번호, 84KA1 실제 모델·외부 단자/전압·접점 정격, 승인 시공도. 정상 극성·연결을 사진/담당자 기록과 대조한다.
3. **현재 프로젝트/CPU**: v1.12 기준 백업과 현재 오프라인/온라인 프로젝트의 읽기 비교, 호출 주기/순서·HMI 쓰기·ServiceBit 작성자/의미·강제 상태. 본 조사를 실행 승인으로 확대하지 않는다.
4. **HMI 실제 화면**: 원래 HMI 프로젝트의 CH_01 버튼/표시 이벤트·FC1 멤버 결속·통신 품질·설정 주소. 부모 DB 참조만으로 멤버 바이트를 채우지 않는다.
5. **냉각기 내부/공정**: 제조사 정식 매뉴얼·유량/온도/내부 경보·정상 운전 기준. 외부 요청과 접촉기 응답 밖의 기능은 미확보이다.
6. **복구 증거**: 승인 조치 전후의 동시각 값·실제 성능·재발 여부. 알람 Reset만으로 field_recovery를 완료하지 않는다.

### 7.4 최종 상태

| 구분 | 상태 | 근거/경계 |
|---|---|---|
| documentation | **draft_complete_with_gaps** | CH01 한 개 7영역 원본 조사초안. 핵심 근거 제한 검토 완료; 사용자 독립검토 대기 |
| static_review | **source_reviewed; independent_review_pending** | XML 핀·PDF 실제 렌더·78해시 대조. 정적 문서 검토 범위 |
| ui_records | not_run | 구현/저장/복원/화면 시험 없음 |
| publication | not_published | 작업3 클라우드 초안, 로컬 2차 통합·게시 제외 유지 |
| tia_compile | not_performed | 실행 없음 |
| live_cpu | not_performed | 현재 프로젝트/실물 동일성 미확정 |
| field_recovery | not_performed | 현장 조치·냉각 성능·복구 미확인 |

다음 조치: 사용자 독립 검토에서 Q3.1/Q6.0 두 명령·2초/10초 분리·84KA1 5–9·P&ID 전력 상충·HMI 미결속·MV02 엔코더 오배정 경계를 우선 대조한다. 승인 없는 로컬 통합·게시·PLC 변경으로 이어가지 않는다.

## 부록 A. 재현 가능한 원본 링크와 해시

기준 저장소: [고정 커밋](https://github.com/esp6662266/gme-plc-manual/tree/abcf31c5030bc7ef8749ed8e869a857f2387a28a).

- [CH01 명령 XML](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0255-FlgNet.xml)
- [CH01 알람 XML](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/decoded-original/0435-FlgNet.xml)
- [전기도면 원본](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/Electrical_Rev2.pdf)
- [참고 시공도 원본](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/Electrical_Can_Decoating_20241118.pdf)
- [P&ID 원본](https://github.com/esp6662266/gme-plc-manual/blob/abcf31c5030bc7ef8749ed8e869a857f2387a28a/all-in-one/sources/PID_1684n002I.pdf)

모든 아래 SHA256은 로컬원본과 git blob 양쪽에서 독립계산해 일치했다. 경로는고정저장소루트기준이다.

| 원본 경로 | SHA256 |
|---|---|
| all-in-one/sources/decoded-original/0255-FlgNet.xml | ea2200a136d7b4e8b498107e8a53c5fa192e501beb039fbd17d1fb35e0277ada |
| all-in-one/sources/decoded-original/0435-FlgNet.xml | d99383db955418fcd854c8bee67f2c216c22affbf826300db50b05d15355c1c1 |
| all-in-one/sources/decoded-original/0318-FlgNet.xml | 95cb71fd6c81291ae7e1ff1e36cf7613a7d635615828120b4d595838a1459bb9 |
| all-in-one/sources/decoded-original/0338-FlgNet.xml | 762ab4b1520aa101efc897ff9e4b72a35f5591ff460a0b654dc87919849077a1 |
| all-in-one/sources/decoded-original/0373-FlgNet.xml | e3fc2a56ead2e3483535de14953be6ca810215ba70b1816279aee6b15f4c307b |
| all-in-one/sources/decoded-original/0164-FlgNet.xml | 15884b2b362842279b626b669a484b1daa269f5ecd99112b8391bb0387382491 |
| all-in-one/sources/decoded-original/0165-FlgNet.xml | 4513a5f6e77717c99c5e869105483be31f7f62ab280e271dc36cd7a2d3e3bb88 |
| all-in-one/sources/decoded-original/0166-FlgNet.xml | 0330a505877be92172f94bce83222a0bfc8d64aab700a69fc1fa2188010d3853 |
| all-in-one/sources/decoded-original/0511-FlgNet.xml | a4bf314bf817f0f666a0c9fdd26df134cedeed8666819c7a3e8e6438850eace6 |
| all-in-one/sources/decoded-original/0513-FlgNet.xml | 19107ffbb3144f4dc5dd070f0edb459166ae7a96c0715b65362f9a359c19412d |
| all-in-one/sources/decoded-original/0397-FlgNet.xml | bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834 |
| all-in-one/sources/decoded-original/0404-FlgNet.xml | ed02308b8d0b1c52fd734826cccb82d25709b8b9d65af07557c1b1e9c8de2570 |
| all-in-one/sources/decoded-original/0030-FlgNet.xml | 9252c9da764993de1edb8b2e44c46d6e9f9d4b6118e751a0dbeaa9ffd8ea721b |
| all-in-one/sources/decoded-original/0031-FlgNet.xml | 76385eab8f8f72b9faa16f7cf8905f395591b18c0a9ee9e6d7dd085a38c45c65 |
| all-in-one/sources/decoded-original/0549-FlgNet.xml | 49f7169c33ed7f54559b0801e21a7d618584900972840e91cf51ad032e8febb1 |
| all-in-one/sources/decoded-original/0024-FlgNet.xml | a463981da8db46dd7eeb44e592d38807704886d597e728bb652dba4c12cc8f67 |
| all-in-one/sources/decoded-original/0401-FlgNet.xml | 60171c213e666de544077b7e4b497675813f7c0e75df85a3e76ab1def49b04ae |
| all-in-one/sources/decoded-original/0355-FlgNet.xml | 73592d33f8b3a71effeb36f25427c76e931485e7ce31f5c81f144ddae83c4247 |
| all-in-one/sources/decoded-original/0151-FlgNet.xml | 227627d165c6240a4c15b62fd4e4c8d7a621c15f35319cb424601df5cc52c904 |
| all-in-one/sources/decoded-original/0152-FlgNet.xml | 2b6165460f06a52de56afcb4d65ed163d64320e24af1b194e934a4d7c6bfe49f |
| all-in-one/sources/decoded-original/0158-FlgNet.xml | d3f3adebc3d990b85c5d4c294906ae3bc3dafebb49d25b030bf9cc2ccf905651 |
| all-in-one/sources/decoded-original/0033-FlgNet.xml | e7fc5601889297a84fcc6b5601a3e0acba420b9c9adb8b37c60277a0fb5cb108 |
| all-in-one/sources/decoded-original/0575-IdentXmlPart.xml | 40e7b2caf89ab7f1ed9075547a7728bd02441e24451bdd8bf97c843637daad06 |
| all-in-one/sources/decoded-original/0576-IdentXmlPart.xml | c8b5f9b9ead0e124f1f817b49d89611ed7b2ce04ecd91ddaa139f2ec89d48dbe |
| all-in-one/sources/decoded-original/0577-IdentXmlPart.xml | 511e01fae619dc385357908a1ac62030dbdfd5f5399bd4c22bc58bebbfc3bf47 |
| all-in-one/sources/decoded-original/0578-IdentXmlPart.xml | 0f9f41b5dee25ea17c7a29ab6f7b00503c13d0f265266acd660072baf061d32b |
| all-in-one/sources/decoded-original/0602-IdentXmlPart.xml | 46ab21151eddaaf616469db520730c60423eb742aa491af194e6710c751b4caf |
| all-in-one/sources/decoded-original/0603-IdentXmlPart.xml | e93969dfa281d75b49b24127793068e33472dadb19729c1c48fc4a8dad075ef8 |
| all-in-one/sources/decoded-original/0604-IdentXmlPart.xml | b798d29c5499b5314a1ee3cff9139dae64c887533b86baa43b6e9a052373a6af |
| all-in-one/sources/decoded-original/0606-IdentXmlPart.xml | 73d45f9e2a34bba8a25df1ed1f71e8f6404fc96a8d6481672652a48435b6a740 |
| all-in-one/sources/decoded-original/0655-IdentXmlPart.xml | 38e9f323024fba19582b473f39b1ed03ffe6a0b390218894029a6edb0b1ff9fb |
| all-in-one/sources/decoded-original/0656-IdentXmlPart.xml | 0dbc45e84732a8848f17b094ea08ab8578dbf240bfe15cd7086859395c27c592 |
| all-in-one/sources/decoded-original/0657-IdentXmlPart.xml | 0f70cda60a6b1a17175876d58e25b2686952642de6cffb21213aeef8b347a22b |
| all-in-one/sources/decoded-original/0658-IdentXmlPart.xml | 998294c0c8a99e00ceb33c2c60def2cd4850e34328917ae506244c2be2df3831 |
| all-in-one/sources/decoded-original/0613-IdentXmlPart.xml | 09d3b1397a987898334218f37e025661af162438582e649f671e7abec443d3cb |
| all-in-one/sources/decoded-original/0614-IdentXmlPart.xml | c6de26f74d75f5be858a406de75eaf6faf62ba9b89c8f9a085b5dd206e93d294 |
| all-in-one/sources/decoded-original/0615-IdentXmlPart.xml | 80f4544edca56c6e6bb2713c758c92ade9202255110074931e03fe34d0d0801a |
| all-in-one/sources/decoded-original/0616-IdentXmlPart.xml | 650b53354a0c8443d94adc5bd6a860d3c5313014a52e0fb98a5656a65b58cc0d |
| all-in-one/sources/decoded-original/0621-IdentXmlPart.xml | a63e2b97ea9eb2691cb478666afed77fc58a2da2f8170422dc09e24b102c88ee |
| all-in-one/sources/decoded-original/0623-IdentXmlPart.xml | 4acd00406ea92466169e57e59fc90b0da4d9ec55fd19e2e96c9556e939cb83a6 |
| all-in-one/sources/decoded-original/0624-IdentXmlPart.xml | 24607c0827fbde428bccf8637ef4ae490798a69a7c2f3b87861d0749082d367a |
| all-in-one/sources/decoded-original/0625-IdentXmlPart.xml | 17a9f9bd540bf0a54e9973391fa258d81e567248fd201ae4ff32c367359e69f9 |
| all-in-one/sources/decoded-original/0626-IdentXmlPart.xml | a9d7fbea345eca70325a8c2e44058c23e96add1b7207eabbb09445118b18188b |
| all-in-one/sources/decoded-original/0627-IdentXmlPart.xml | 08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb |
| all-in-one/sources/decoded-original/0628-IdentXmlPart.xml | 9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd |
| all-in-one/sources/decoded-original/0629-IdentXmlPart.xml | 67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972 |
| all-in-one/sources/decoded-original/0064-IdentXmlPart.xml | ce6afc4f7ca0a8059c2e3cab25d202f0faaa49a3bc6a2e9ee238964a76e9fc9d |
| all-in-one/sources/decoded-original/0632-IdentXmlPart.xml | fd162c603476c2cac899010cee7a8ee382b6092c115135e3ac1007ae71c544e9 |
| all-in-one/sources/decoded-original/0633-IdentXmlPart.xml | 9e00aa275fa1b4e488b73983b309c6b73dcf4f3dd9be5dec13e9975d68f3c0fc |
| all-in-one/sources/decoded-original/0067-IdentXmlPart.xml | 0aa469d4f7a20bde2a5bccc6c91b3d9c48929460bd68ef32e0217d53f4d68628 |
| all-in-one/sources/decoded-original/0068-IdentXmlPart.xml | 0a71d492e69760390b99f71a75f02ef684e271554b003d5de8bf64a26c64eeba |
| all-in-one/sources/decoded-original/0652-IdentXmlPart.xml | 251bb1b3ce1bdf3686545062e5803152779de8a4961539d30e6951a2a10ab692 |
| all-in-one/sources/decoded-original/0688-IdentXmlPart.xml | ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda |
| all-in-one/sources/decoded-original/0692-IdentXmlPart.xml | bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037 |
| all-in-one/sources/decoded-original/0694-IdentXmlPart.xml | 757ccebdf32d0a168dd787bfa735fe6494eac4c4a9f7a5adc63898a88e8b152d |
| all-in-one/sources/decoded-original/0674-IdentXmlPart.xml | 4770702f519bacda69202bb2f7733d983074bda90964360c238f990d9d08fd84 |
| all-in-one/sources/decoded-original/0675-IdentXmlPart.xml | b1902886927d8403fab736d9c8ffe73f2fbc8ce4b7ca7c345144964668b051c3 |
| all-in-one/sources/decoded-original/0676-IdentXmlPart.xml | c58427c5b0ac6c11cdb52e4c6d0461c7b191fae81ccace191048e9f175fcec59 |
| all-in-one/sources/decoded-original/0677-IdentXmlPart.xml | 69922fcc5c67d00cdf1c5f712efa3db7638d20c88318d35fe6196467796ab1e3 |
| all-in-one/sources/decoded-original/0678-IdentXmlPart.xml | 51e637e0b9713c028810f2a717b5c3804a3a26c2f1be7e332a4d6bf277bfc382 |
| all-in-one/sources/decoded-original/0564-IdentXmlPart.xml | 2aed17fa02d19b0a081023282841aa561d6a2dca3e393284da3622b967af00b1 |
| all-in-one/sources/decoded-original/0565-IdentXmlPart.xml | 0f7f970faa6c456f2bb032b1a2072a2f52db1e03fc77bd8d35d4583deeaf1149 |
| all-in-one/sources/decoded-original/0566-IdentXmlPart.xml | a1914c7ae085acc1f949a649979824bec8b46fcd78a8055318272a1eb5a45265 |
| all-in-one/sources/decoded-original/0567-IdentXmlPart.xml | 5d428b5d5a2b0f4649dbbbb4e4f060a9d89a107e9cf4b6139d8f003c4371347e |
| all-in-one/sources/Electrical_Rev2.pdf | 5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6 |
| all-in-one/sources/Electrical_Can_Decoating_20241118.pdf | 3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd |
| all-in-one/sources/PID_1684n002I.pdf | 2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b |
| all-in-one/sources/hmi_plc_tags.csv | a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404 |
| all-in-one/sources/hmi-windows.csv | 15f8d69b5c43d4fdbe550f9cd2717f855fea877ed8146973054cb6dbcaa9892e |
| all-in-one/sources/block_summary.json | 68253f9366908244a27ed461c66d465da7ec1723571f27deaa9a6f81a542de63 |
| all-in-one/sources/live_index.json | 14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1 |
| docs/equipment-standard/INVENTORY.json | 720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc |
| all-in-one/registers/equipment.json | 7870325dff32bbca90fa34507b301c4aad3347d669fddcd03b910343663996fa |
| all-in-one/registers/equipment-networks.csv | 0dcd161bafe7fbc5fd31dd00ed031da3b01e4e46f1154b4c80698bdd766568e0 |
| all-in-one/registers/equipment-io.csv | a7a1f27dc453af25b2b729074cac5266d6dd53c0945a6a1a4afe2dd1e9153b6a |
| all-in-one/registers/equipment-hmi.csv | 2cdce600aa0138cc5025022e57d9d61a948afb237f70c70e2d11e8300e73286a |
| all-in-one/registers/all-networks.csv | 7b6a9fc46f56c1bec7c4c7136792e2fc470fd07c15aa885d4f411c478d5e5f7c |
| VERSION.json | 5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7 |


## 전달 전 핵심 근거 제한 검토

2026-10-11 조사 초안 취합 단계에서 핵심 출력/타이머/운전시간 또는 요청쓰기의 원본 Part/Wire를 표본 재대조하고, 도면 전달 끝점을 실제 렌더로 재확인했다. 인용 원본 SHA256도 전부 재계산하여 일치했다. 전체 원본의 의미 검토나 현재 CPU/현장/통합/게시 검증을 뜻하지 않는다. 사용자 독립 검토용 초안이며 미확정 경계는 유지한다.
