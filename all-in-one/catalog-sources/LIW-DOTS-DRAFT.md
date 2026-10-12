# LIW — 외부 LIW 피더 자체 원본 조사 초안

## 핵심 확인·상충·누락·공유근거

- LIW 한 catalog ID만 조사했다. BWF01/02, PV03, WEIGHTING HOPPER 2 또는 CLIENT-CL17과 실물·완료 실적을 병합하지 않는다.
- 고유 명령은 START LIW FEEDER Q6.1과 LIW_SP_SPEED QW302이다. 입력 I14.1은 LIW SYSTEMAUTOREADER로 선언되나 OEM FG90/PDF91·FG130/PDF131에 SPARE 표시가 함께 있다. 이름만으로 Ready/Run/Fault 의미·현재 결선을 확정할 수 없다.
- **15분 기동 지연으로 오독하지 않는다.** 0273의 Tag_127(T126) SdCoil은 Set 경로와 병렬이다. Set은 ON·(BWF01 RUN 또는 BWF02 RUN)·PV03 출력 조건이다. 두 BWF RUN이 모두 사라진 뒤 Tag_128(T127)의 S5T#15M 조건으로 Reset하는 별도 경로가 있다.
- **운전시간 17과 고장 17은 다른 소유다.** LIW 입력은 0306의 CLIENT_MOTOR_17_MIN/HOUR에 쓰이지만 0234의 Allarm.motor_client_17_fault는 WEIGHTING HOPPER 2FAULT(I16.4)에 연결된다. 이를 LIW 전용 Fault로 가져오지 않는다.
- **아날로그 값과 실행허가 핀을 분리한다.** 0472 Mul905.eno는 Move909.en이며 값은 app05→Move909.in이다. 출력은 SAM=Peripherie QW302 접근이다. 181배 정수식은 확인했지만 4–20mA 물리 보정·단위·현재 설정은 미확정이다.
- 공유근거: [SYS-PLC-IO](SYS-PLC-IO-DOTS-DRAFT.md)의 입력/출력 Word 미러와 0401 Q→DB14 방향, [SYS-RUNHOURS](SYS-RUNHOURS-DOTS-DRAFT.md)의 공통 T13/T17·외부 저장 ACK 미확정, [SYS-ALARM](SYS-ALARM-DOTS-DRAFT.md)의 공통 ACK/Reset 경계를 같은 고정입력 연결로 재사용한다. 본 초안의 LIW 고유 핀·선언·전기 6쪽은 독립 재확인했다.
- 누락: 외부 LIW 제어반 내부도·명판·단자 양끝 케이블대장·현재 CPU/HMI·외부 실제 Ready/Run/Fault 정의 및 안전/복구 절차. 새 현장자료 없이 동일 보류를 반복 검색하지 않는다.

## 1. 설비·자료 기준 — 적용

대장 `docs/equipment-standard/INVENTORY.json#/catalog/74`: LIW, 외부 LIW 피더, client/외부 연동, 부모 없음, phase2. 배치16 범위 및 중복검토의 별칭 liw/autoreader를 탐색에 사용했다. 별칭은 실물 동일성 증거가 아니다.

읽기전용 기준은 source-mv06, Git abcf31c5030bc7ef8749ed8e869a857f2387a28a, v1.12.0이다. 이 초안은 후속 로컬 게시판본·현재 CPU 상태를 검증하지 않는다. 모델 런타임/추론수준 증명 미확인. 조사 시작 2026-10-11 12:37:24 UTC. 정적 종료시각은 부록 검사기록 참조.

이하 NNNN XML은 `all-in-one/sources/decoded-original/` 경로다. doc는 색인 문서ID, NID는 해당 선언 블록 내 네트워크, RID/UID는 파일 문맥 내 식별자이다. AO/BO는 비트 오프셋이며, 이름이나 같은 UID만으로 다른 선언과 결속하지 않는다. 모든 PDF 쪽수는 1부터 세었다.

## 2. I/O·HMI — 적용, 현장/화면 이벤트 미확정

|항목|직접 원본 선언|주소·소유·경계|
|---|---|---|
|LIW SYSTEMAUTOREADER|0613 SimpleAccess RID104, Global Bool, Input AO113, SAM=None; NID17 UID964|I14.1 입력영상. 0306 운전시간 접점. Ready/실제 Run/Fault 셋으로 분해 불가. 심볼 설명 E15.0은 백업주소 I14.1과 불일치하여 옛 주석으로 별도 보존|
|START LIW FEEDER|0602 RID198, Global Bool, Output AO49; NID43 UID1222 Set/1223 read/1229 Reset|Q6.1 원격 시작 요청. 실제 구동/공급 완료 응답 아님. 심볼 주석 A61.1과 현재 백업주소/도면 A6.1 구별|
|LIW_SP_SPEED|0664 RID104, Global Word, Output AO2416, SAM=Peripherie; NID16 UID919 Write|QW302 주변장치 직접 접근(:P). 단순 출력영상 쓰기와 구별. 외부 LIW 속도/유량 설정용 4–20mA 도면 연결|
|Inputs.BWF 01 RUN / BWF 02 RUN|0604 Global RID257/258 Bool AO90/95; 0603 Inputs RID218 TOD13|DB13.DBX11.2/11.7. BWF의 가공 입력 비트이며 LIW의 RUN 응답이 아님|
|PV-03 GATE EV|0602 RID195 Global Bool Output AO46; NID43 UID1221 read|Q5.6 출력명령 접점. 물리 게이트 열림 확인 센서로 쓰지 않음|
|ON|0602 RID1·0664 RID1, 0692 RID52; Memory AO0|M0.0. 명칭만으로 상시 True 가정 금지|
|Tag_127/128|0602 RID197/199 Timer AO126/127|T126/T127. PLC S5 Timer이며 HMI Bool 또는 실제 경과시간 측정값 아님|
|Tag_158/159|0664 RID93 Word Memory AO560 / RID96 Timer AO128|MW70 보관값 / T128 갱신지연. 직접 HMI 명령과 구별|
|Data2.Set_TH|0662 RID4 Global Int AO0, 0660 Data2 RID3 TOD10|DB10.DBW0. 아날로그 출력을 위한 상위 공통 설정이며 LIW 전용 HMI 버튼이라고 단정 불가|
|App04 / app05|0663 InterfaceAccess RID99/102, Local DInt AO96/128, NID16 UID914/915 및917/918|FC 내부 DInt 작업변수. Global DB 또는 HMI 태그가 아님|
|CLIENT_MOTOR_17_MIN/HOUR|0615 RID106/108 Global Int AO512/528; 0614 hours motors RID5 TOD9|DB9.DBW64/66. LIW 입력을 계수에 사용하지만 CLIENT 고장17과 동일성이 아님|

HMI `hmi_plc_tags.csv` 393행에는 Set_TH, DB10,W0, PLC, 001D6이 있다. 이는 선언 DB10.W0과 주소 대응한다. LIW/autoreader 직접 이름 검색에서는 전용 태그를 찾지 못했다. BWF01/02의 Risposta/StatusOK/Allarme1 및 Editor_BWF01/02는 별도 BWF 소유다. `Set_TH`의 실제 위젯·스크립트·입력범위·단위·권한·이벤트 writer는 CSV만으로 확정하지 않는다. 원본의 0401 출력 관찰 Word 미러는 Q→DB14이며 미러 쓰기를 물리출력명령으로 뒤집지 않는다.

## 3. 제어 구조 — 고유 정적 경로 적용

### 3.1 호출 경계

0549(doc1620, Main NID7): ORef335/RID52 ON→W348 Contact350.operand, W351 Contact350.out에서 CRef319.en(FC7 Motors 1, CodeBlock337/RID67) 및 CRef334.en(FC2 time work motor, CodeBlock347/RID82) 등으로 병렬 허가한다. 0688 FCBlock 선언 TOD7/TOD2, NID7 UID337/347 Call과 맞췄다.

0032(doc1621, Main NID8): ORef345/RID52 ON→W350 Contact352.operand, W353→CRef344.en; CodeBlock349/RID88은 0688 TOD18 Analog output conversion이다. UID347은 이 문맥에서는 다른 호출이다. 현행 OB 주기·스캔순서·통신·TIA 컴파일은 미검증이다.

### 3.2 LIW 원격 시작/유지/Reset: 0273(doc1973, Motors 1, NID43)

- W1230 ORef1216/RID1→Contact1251.operand; ON 후 W1252가 BWF 두 접점 및 자기출력 접점으로 갈라진다.
- W1231/1232는 ORef1217/RID257 BWF01, ORef1218/RID258 BWF02를 Contact1253/1255.operand에 연결. W1254/1256→OR1190.in1/in2.
- W1233 OR1190.out은 SdCoil1196.in과 Contact1257.in을 **병렬** 공급한다. SdCoil1196.value는 W1234 ORef1219/RID196 S5T#15M, operand는 W1235 ORef1220/RID197 T126이다. 0606의 Constant S5Time SV=S5T_x0023_15M, V10496를 확인했다. T126 완료 접점은 이 LIW Set 가지에 없다.
- W1236 ORef1221/RID195 PV03 Q5.6→Contact1257.operand; W1258→SCoil1201.in, W1238 ORef1222/RID198→SCoil1201.operand. 따라서 Set 조건은 ON AND (BWF01 RUN OR BWF02 RUN) AND PV03 출력이다.
- 자기출력 ORef1223/RID198→W1240 Contact1259.operand. W1260이 이후 지연조건과 Reset 확인 가지로 갈라진다. Contact1261/1263의 operand에는 각각 BWF01/BWF02의 명시적 Negated가 있다(W1242/1243). W1264→SdCoil1210.in; W1241 value=S5T#15M, W1245 operand=T127.
- W1246 ORef1228/RID199 T127→Contact1265.operand; W1266→RCoil1215.in; W1248 ORef1229/RID198→Reset 대상 Q6.1. Reset 식은 ON AND Q6.1 AND T127이고 T127 입력은 ON AND Q6.1 AND NOT BWF01 RUN AND NOT BWF02 RUN이다.
- 본 네트워크에서 ON=0 또는 PV03=0 자체를 Q6.1의 즉시 Reset으로 그리지 않는다. S/R 출력이므로 조건 소실과 해제는 다르다. 다른 전체출력/CPU 정지·재기동·retain 영향, 현장 비상정지 의미는 미확정이며 강제/시험하지 않았다.

### 3.3 아날로그 갱신과 출력: 0471/0472

0471(doc1690, NID15, 색인 제목 salt system): ON Contact889→Ne856.pre. W879/880이 Data2.Set_TH(RID4 UID871)와 Tag_158(RID93 UID872)을 Int 비교한다. W881 Ne856.out→SdCoil862.in 및 Contact891.in. W882 상수 RID95 UID873=S5T#15M, W883 T128 RID96 UID874. W884 T128 접점 UID875→Contact891.operand, W892→Move867.en; W886 Data2.Set_TH UID876→Move867.in, W887→Tag_158 UID877. 차이가 유지되어 T128이 성립해야 보관값이 갱신되는 정적 경로다. 이를 운전시동 타이머 T126/T127과 혼동하지 않는다.

0472(doc1691, NID16): W931 ON Contact930.out→Move899.en 및 Mul905.en. W921 Tag_158 UID913→Move899.in, W922→Local App04 UID914. W923 App04 UID915→Mul905.in1, W924 Constant DInt181(0661 RID101 UID916)→in2. Mul905 SrcType=DInt, W925 out→Local app05 UID917. W926 **Mul905.eno→Move909.en**, W927 app05 UID918→Move909.in, W928 Move909.out1→LIW_SP_SPEED UID919. ENO는 출력값이 아니다. Word→Local DInt→DInt×181→Word 주변출력 변환이며 음수/오버플로/Word 절단·물리 mA 범위·현행 채널 파라미터는 미검증이다. 본 0472에는 Q6.1 또는 I14.1 접점이 없으므로 출력 요청과 아날로그 전송을 하나의 Run 연동식으로 합치지 않는다. Set_TH에는 다른 writer도 선언되어 있어 이 경로가 상위값의 유일 소유자라고 하지 않는다.

### 3.4 시간 관찰과 다른 writer

0306(doc1016, NID17): Tag_47(T13) ORef963/RID1→W975 Contact992.operand, I14.1 ORef964/RID104→W976 Contact994.operand. W995→Add946.en 및 Ge953.pre. Add946 Int in1=MIN(UID965, W977), in2=1(UID966,W978), out=MIN(UID967,W979). Ge953 Int in1=MIN UID968/W980, in2=60 UID969/W981. 성립 시 W982→Move956.en, W984 in=1 UID970, W985 out1=HOUR UID971. **HOUR+1 Add가 아니라 1 Move**다. W986 ENO→Move959.en; W987 in=0 UID972, W988 out1=MIN UID973. W989 ENO→SCoil962.in, W990 대상 Flag_Aggiorna_DB UID974/M1.7.

0335(doc1048,NID50)의 T17 접점2801에서 Move2760.eno→W2789 Move2763.en, W2790 in=0 UID2778/RID12, W2791 out1→HOUR UID2779/RID108로 별도 0 쓰기가 있다. 공통 T13/T17 발생 및 외부 저장 성공/ACK 부재는 SYS-RUNHOURS 연결을 재사용한다. 이 값만으로 평생 누적운전시간·정비주기를 확정하지 않는다.

## 4. 전기 전달 경로 — 실제 PDF 6쪽 직접 렌더 확인

원본 `all-in-one/sources/Electrical_Rev2.pdf`. 아래 페이지 footer DATA는 모두 27.05.2024, DISEGN G.G., NORMA IEC, TOT262이다. 파일명 Rev2를 모든 페이지 개정란에 강제로 적용하지 않았다. 공통 모듈 CPU515 표기는 도면 표기이며 현재 CPU 식별 증거가 아니다.

|FG / 실제 PDF|제목·개정란|LIW 끝점과 전달 경로|
|---|---|---|
|FG84 / PDF85|SERVICE RELAYS, 개정란 공란|LIW FEEDER REMOTE START: X1:234→선84.3→84KA2 접점 **5–9**→선84.4→X1:235. ORANGE FS17 1.5mm². 코일 A1은 A6.1(142/1), A2는 -0Vdc10.6. 하단 접점표1/5/9와 실제 부하5/9를 구분. 외부 접점 부하전압·외부반 목적지 미표시|
|FG142 / PDF143|DIGITAL OUTPUT MODULE, 개정란 공란|CPU515 MOD15 A6.1 단자22→FG84/3→84KA2 A1. 모듈 공급 L+/M 29/30, X21:3034 5×20 4A F/+24Vdc10.9와 -0Vdc10.6. 퓨즈는 도면 표기이며 현행 보호값 승인 아님|
|FG85 / PDF86|ANALOG IN/OUT TO/FROM CLIENT MACHINE, 개정란 공란|FLOW RATE SET LIW FEEDER 4–20mA: X1:249=+PAW302, X1:250=-PAW302, X1:251=85SCH4(차폐 경로). 세 선은 FG113/0으로. BWF01/02 PAW298/300 및 BWF 유량/레벨 입력은 별도이며 LIW 피드백이 아님|
|FG113 / PDF114|ANALOG OUTPUT MODULE, 개정란 공란|CPU515 MOD7 PAW302: +→QV7/QI7 단자33, -→MANA 단자36, 차폐85SCH4가 도면 실드 접지 경로. S7+34/S7-35는 도면상 이 두 출력선과 혼동하지 않음. L+41/42, M43/44 및 X21:3004 500mA F 표기. 현물 모듈 모델/구성/전류값 미확정|
|FG90 / PDF91|DIGITAL INPUT FROM CLIENT MACHINE, Rev2 17.03.2025|LIW SYSTEM AUTO READER가 SPARE 점선 범위. +24Vdc10.7→5×20 2A F/X1:312→선90.5 및 그려진 접점→X1:313→E14.1(130/2). 접점 기호로 현장 정상극성이나 장치 설치를 확정하지 않음|
|FG130 / PDF131|DIGITAL INPUT MODULE, Rev2 17.03.2025|CPU515 MOD11 E14.1 단자22, 90/7 참조. LIW SYSTEM AUTOREADER 이름과 SPARE 표시가 공존. 인접 E14.3 CONSENT AVAILABLE, E14.4/5 BWF high speed, E14.6/7 다른 장치 Fault를 LIW ready/fault로 가져오지 않음|

카탈로그 전기 FG85–95 범위만 따라가면 시작 릴레이 FG84와 모듈 FG113/130/142를 놓친다. 그래서 실제 상호참조로 확대해 확인했다. 외부 LIW반 경계는 GME X1:234/235,249/250/251,312/313 이후다. 외부 케이블번호·반내 단자·수신기·동력/안전회로·제조사 규격은 확보하지 못했다. `Electrical_Can_Decoating_20241118.pdf` 전체 텍스트 LIW 검색에서 직접 일치 없음은 검색결과일 뿐 시공도 전체 의미검토 완료가 아니다.

## 5. 알람·복구 — LIW 고유 Fault/Ready는 근거 미확보

- 0273의 T126/T127은 운전 요청 관련 타이머다. LIW 고장 발생/ACK/Reset 알람으로 재명명하지 않는다. T128은 설정값 갱신지연이며 고장 타이머가 아니다.
- 별도 LIW ready·run·fault 선언/끝점 세트를 확보하지 못했다. I14.1을 실제 Run이라고 확정하거나 인접 CONSENT AVAILABLE을 LIW Ready로 차용하지 않는다. 외부반에서 이 입력을 어떻게 생성하는지와 SPARE 표기의 현행 유효성을 먼저 확인해야 한다.
- 오배정 배제용 원본: 0234(doc424, motor/alarm client NID17) W347 ORef341/RID38→Contact357.operand, W358→SCoil334.in, W349 ORef342/RID39→고장 Set. 0599 RID38 Global Input AO132=I16.4 이름은 WEIGHTING HOPPER 2FAULT; 0601 RID39은 Allarm.motor_client_17_fault, AO129이다. Reset 가지는 NOT 해당 fault(Contact359, W350)와 Flag.RESET_ALLARM(Contact361,W351)을 거쳐 RCoil339(W353 UID345)다. **이 네트워크는 LIW 고장/복구가 아니다.**
- LIW 자체 알람 부재를 안전/정상 판정으로 쓰지 않는다. 공통 정지·비상정지·상위 인터록 영향은 별도 공통 소유로 두며 외부반 복구 절차는 승인 OEM/현장 자료가 필요하다. 원인 해소·요청 Reset·재기동·실제 공급 확인은 각각 다른 증거다.

## 6. 증상별 관찰 — 조작·강제·복구시험 없는 문서 체크리스트

|증상|기록할 관찰값·원본 비교|원인 확정 전 경계|
|---|---|---|
|원격 시작 요청이 안 보임|동일시각 ON, DB13.X11.2/11.7, PV03 Q5.6, Q6.1 및 0273 Set 핀|BWF RUN과 PV03는 LIW 실물 운전 확인이 아님. T126 15분 대기를 자동 처방하지 않음|
|Q6.1은 있는데 피더 무응답|관찰권한 있는 기록으로 Q6.1, 도면 A6.1 단자22, 84KA2 코일/부하 경로 및 외부반 수신상태 비교|접점 5/9 및 X1:234/235, 외부반 인터록·로컬 모드 자료 필요. 결선 변경/점퍼/강제 지시 없음|
|BWF 정지 뒤 LIW 요청이 남음|두 BWF 가공 RUN 소실 시각, T127 입력/완료 상태, Q6.1 Reset 가지|S5T#15M 정적 의미와 실제 CPU 경과시간 구분. 현재 설정/타이머 강제 금지|
|유량/속도 설정 반영이 늦음|HMI 표시 Set_TH와 DB10.W0, MW70, T128, app04/app05, QW302:P를 같은 시각 비교|상위 다중writer·15분 차이 지속 조건·Word/DInt 변환. 181을 임의 mA 보정계수로 변경하지 않음|
|I14.1 또는 시간계수 의심|FG90 SPARE·X1:312/313·FG130 단자22의 문서대응, I14.1, MIN/HOUR, M1.7 및 외부 기록 근거|I14.1의 실제 신호의미/설치 여부 미확정. HOUR 1/0 쓰기를 고장17 경보와 혼합하지 않음|
|LIW라고 표시된 client17 알람|표시 문자열/주소, I16.4, 0234의 UID341/342, 외부반 알람 코드 비교|현 원본은 호퍼2 fault. 태그 숫자만으로 LIW 배정/리셋하지 않음|

실제 관찰자료는 관찰자, 날짜/시간대, 위치, 값/단위, CPU 프로젝트·모듈/계측기 식별, 비교 판본, 원인 배제 결과, 승인된 조치, 복구 전후 증거를 분리해 수집한다. 본 문서는 현장 조치를 수행하거나 복구 완료로 기록하지 않았다.

## 7. 완료 기준·누락·검증 경계

|영역|문서 상태|남은 증거|
|---|---|---|
|설비·자료 기준|적용|LIW 제조사/명판/실물 및 BWF/호퍼의 독립 경계|
|I/O·HMI|고유선언 적용, 이벤트 미확보|실제 Ready/Run/Fault 정의, SPARE 유효성, HMI 이벤트·입력범위·권한|
|제어|선택 8네트워크 정적 핵심 검토|현행 전체 writer/호출/재시작·retain 영향, 외부반 인터록|
|전기|선택 PDF6쪽 렌더 직접 확인|외부반 내부도, 케이블 양끝 번호·설치확인, 현행 모듈 구성|
|알람·복구|타이머·오배정 배제 적용|LIW 고유 알람명/원인/해제/외부반 복구 OEM 자료|
|증상관찰|체크리스트 적용|현재값·실측·승인 조치·복구 증거|
|완료판정|문서 complete_with_gaps|TIA/CPU/현장·UI·게시 별도 미수행|

도면·래더 나란히보기, 선택 백업/복원, 전후 기록 비교, 관찰 보고서/PDF의 LIW 전용 구현·저장·재읽기·화면 재열기는 검증하지 않았다. note/repair_observation/미지 필드·기존 초안·사용자 기록은 수정하지 않았다. publication not_published(본 초안), ui_records not_run, tia_compile/live_cpu/field_recovery not_performed. BC01 동등 구현 완료 또는 안전 적합/현장 복구 완료라는 결론은 없다.

수행은 읽기전용 Git 상태/선정해시·원본 XML 직접 파싱·CSV 검색·PDF 텍스트 검색 및 6쪽 렌더/시각 대조뿐이다. 원본 build/test/generator·시뮬레이터·PLC·보호값·현장·SEJIN 변경/실행은 0. 원본 Git 상태는 clean이다. 중지 자산을 실행하거나 수정하지 않았으며 공통 보존 검사는 부모 관리 범위다. 선정 파일 수는 해시검사 수로, 모든 본문 의미검토 수가 아니다. 전체 90개 의미검토를 주장하지 않는다.

다음 작업은 외부 LIW반 승인 I/O 정의와 SPARE 표시의 현행 유효성 확인자료 확보다. 자료 없이는 실물/안전/복구 상태를 진전시키지 않는다. 이번 수정경로는 extracts/LIW와 drafts/LIW-DOTS-DRAFT.md뿐이다.

## 부록 A. 직접 원본 선정 해시 및 고정 Git 내용 일치 전체 목록

정적 검사시각: 2026-10-11T12:43:05.695341+00:00. 총 34개 파일 SHA256 및 고정 Git blob 바이트 대조 전부 일치. `extracts/LIW/source-hashes.json`, `static-review.json`에 원시 검사기록을 저장했다. 아래는 생략 없는 선정 목록이며 전체 저장소 의미검토 선언이 아니다.

|원본 상대경로|SHA256|고정 Git blob|내용일치|
|---|---|---|---|
|`all-in-one/sources/decoded-original/0032-FlgNet.xml`|`070bb8efa33d03b18add5da81d3f670a47c12b288076b7bfee11ac87fe6fa7e4`|`e31cf9aeecfbfc0c264921ac217cbd15479c1f34`|일치|
|`all-in-one/sources/decoded-original/0234-FlgNet.xml`|`4fa899449ab66d4a852be7c21085590393a8ad11c65d265222c3bfcd649dfc64`|`3d36e5c03ca8c97d344b13e2817cbb1a9eb69bda`|일치|
|`all-in-one/sources/decoded-original/0273-FlgNet.xml`|`48cc05ab4fb2778e2878b53993f10a31250dfeadd8b56024af4647a1e1da7f31`|`5d095330ba82be077e57e023785dafd2a46bc7db`|일치|
|`all-in-one/sources/decoded-original/0306-FlgNet.xml`|`a8d53cbb5eca6037686459d44efa3f5dc7d01e0278eec7b004bbdc6c10b89401`|`13d8edc06c75cd2420621208e410af43585cde18`|일치|
|`all-in-one/sources/decoded-original/0335-FlgNet.xml`|`6f0214de436cfaac95750cc25ba3d6f306d33174472618754fac38ad4caf4781`|`6f065e48bd456e656557f1f94896597028f42c5f`|일치|
|`all-in-one/sources/decoded-original/0471-FlgNet.xml`|`8a4f3d9aed1eea2d2127d9dadee839eab7f97e755c2055c04c46bd2551578d96`|`b661ee5c10732cd56c64e69e876392adb3c70eaf`|일치|
|`all-in-one/sources/decoded-original/0472-FlgNet.xml`|`903cd4c143ad8020796f3bd2e309d7aee9c537aab9be7ac7a20cc00fdb2ac413`|`d5c635c4a6f4b615c1ac18df5e6d169496747f0f`|일치|
|`all-in-one/sources/decoded-original/0549-FlgNet.xml`|`49f7169c33ed7f54559b0801e21a7d618584900972840e91cf51ad032e8febb1`|`985b5310b43b1015b5dee286aa0e42800564b94b`|일치|
|`all-in-one/sources/decoded-original/0555-IdentXmlPart.xml`|`46c36333e249dd775c1db94a1f6e80a36cf1a5a9c998b7d0980ae01d862901e6`|`9a915a8b9a260b48402df151c1fe0bbcb2f4ea1c`|일치|
|`all-in-one/sources/decoded-original/0599-IdentXmlPart.xml`|`32a693fe12134febbd9f5c7da10c3469ef4d5b164ab8b6bd9ea3867c358936c1`|`493de77fc827d8f14192ced05d82df3a062f7965`|일치|
|`all-in-one/sources/decoded-original/0601-IdentXmlPart.xml`|`04c9481f7381284de689ef5c7ff40d7aea93f2004cd877a4e4f27e47baa6d862`|`07bcf656fa58e4a305999456644acd24b3dc6bec`|일치|
|`all-in-one/sources/decoded-original/0602-IdentXmlPart.xml`|`46ab21151eddaaf616469db520730c60423eb742aa491af194e6710c751b4caf`|`bcb12ab1ce8c476ff921baa1608f29d9822f76b4`|일치|
|`all-in-one/sources/decoded-original/0603-IdentXmlPart.xml`|`e93969dfa281d75b49b24127793068e33472dadb19729c1c48fc4a8dad075ef8`|`3a92b304baf4dbf6147e944d9778d2da11285cb1`|일치|
|`all-in-one/sources/decoded-original/0604-IdentXmlPart.xml`|`b798d29c5499b5314a1ee3cff9139dae64c887533b86baa43b6e9a052373a6af`|`bb2c318788b97e7a4924a176275c12d805aa519d`|일치|
|`all-in-one/sources/decoded-original/0606-IdentXmlPart.xml`|`73d45f9e2a34bba8a25df1ed1f71e8f6404fc96a8d6481672652a48435b6a740`|`ced032fa747a8544abf17058ee5ebaa78ba9b23b`|일치|
|`all-in-one/sources/decoded-original/0613-IdentXmlPart.xml`|`09d3b1397a987898334218f37e025661af162438582e649f671e7abec443d3cb`|`c9d19a48e947098914f4d2de3348c05b4f6d37e8`|일치|
|`all-in-one/sources/decoded-original/0614-IdentXmlPart.xml`|`c6de26f74d75f5be858a406de75eaf6faf62ba9b89c8f9a085b5dd206e93d294`|`da0485aa033700f08c8695d30b93ebd2d377d6c7`|일치|
|`all-in-one/sources/decoded-original/0615-IdentXmlPart.xml`|`80f4544edca56c6e6bb2713c758c92ade9202255110074931e03fe34d0d0801a`|`49eb86fe01feb83de8c0864b21493d305aff8b20`|일치|
|`all-in-one/sources/decoded-original/0616-IdentXmlPart.xml`|`650b53354a0c8443d94adc5bd6a860d3c5313014a52e0fb98a5656a65b58cc0d`|`9f7fdd5f93ac149c139a054ebb34f63c632ef7fd`|일치|
|`all-in-one/sources/decoded-original/0660-IdentXmlPart.xml`|`0bf4f4c46531f55324602f4f7b1a1e0b9e63df2c6278126f6e5cf1bc9a06509f`|`915de9b3f968310c45682bef86a91adc1fa06e75`|일치|
|`all-in-one/sources/decoded-original/0661-IdentXmlPart.xml`|`90672199fee355011f581d3287046894772f3f3b4cb78bbe0dd0d71bd488ac93`|`cea3653088f8fb5c77afcf715988039cb63e28ac`|일치|
|`all-in-one/sources/decoded-original/0662-IdentXmlPart.xml`|`1838040bfee800fdb3f13b126eaf69a9d178b17cecc0d59ae03e9185216a48a5`|`ba624f3460dc05e8ade4956cdfc2ec621edb4f73`|일치|
|`all-in-one/sources/decoded-original/0663-IdentXmlPart.xml`|`d3980b88d3cd3e49854439d0778c58ed131bae46a6bc3e65ab70e81f766ac03d`|`3051de9b670457991223a08c03f785747e687414`|일치|
|`all-in-one/sources/decoded-original/0664-IdentXmlPart.xml`|`68c614e1c6a7fcadeee3f0b2ddc54910c3b337e66074d7a113b9cbc834c271ed`|`7ce2f1315d5a21d6b77869a59fc9fcb2f17e90e6`|일치|
|`all-in-one/sources/decoded-original/0688-IdentXmlPart.xml`|`ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda`|`463585759f1ecd94f32362b4fefb000a152f5773`|일치|
|`all-in-one/sources/decoded-original/0692-IdentXmlPart.xml`|`bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037`|`737785d03b5fad43c5b4d451955726d800edb1c0`|일치|
|`docs/equipment-standard/INVENTORY.json`|`720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc`|`587c3748ad9224718f95ba06463fee913dae231d`|일치|
|`all-in-one/sources/decoded-original/network-map.json`|`c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60`|`424430b6b953e43138e5d0a18ca40c949e21cfa1`|일치|
|`all-in-one/sources/Electrical_Rev2.pdf`|`5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6`|`f610fd7c7ce14ae951b00cff57b969259bfb389d`|일치|
|`all-in-one/sources/Electrical_Can_Decoating_20241118.pdf`|`3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd`|`0ee6b6f8361c5790864dbba4bbd9d55e8e7c08f8`|일치|
|`all-in-one/registers/plc-symbols.csv`|`a0334b390f06ddb515d6c09ca96a01d35d44029c1b726ef0ff53303ec04ff91f`|`cbc576c5d6e47498a3865304a1c23de9b4641d9f`|일치|
|`all-in-one/registers/equipment-io.csv`|`a7a1f27dc453af25b2b729074cac5266d6dd53c0945a6a1a4afe2dd1e9153b6a`|`d042a15edd5f2550dbbef40203f927da3360fe32`|일치|
|`all-in-one/registers/signal-usages.csv`|`90360d9243ec875b0bf6818b9334d4d4516179d0d61a863eaea9aba50cc6611e`|`c32dd9e990ac1c697db404954c25f5219e0a765e`|일치|
|`hmi_plc_tags.csv`|`a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404`|`cf4c0650e7c7baac350dcb89909b808435704880`|일치|
