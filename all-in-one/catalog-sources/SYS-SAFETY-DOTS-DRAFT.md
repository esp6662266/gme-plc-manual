# SYS-SAFETY 비상정지·일반 안전 회로 — 고정 원본 7영역 초안

문서 상태: complete_with_gaps. 일반 PLC 관찰·허가 로직과 물리 비상정지 회로를 구분한 문서 조사이며, 안전 인증·현장 정상·복구·BC01 동등 구현 완료 판정이 아니다.

## 핵심 확인·상충·누락·공유 근거

- 물리 경로: FG12의 두 접점 경로·피드백 접점열 → FG13의 13KA1 → FG14/15 릴레이 코일 경로. 13KA1의 33–34는 E19.4 관찰 입력으로 이어진다. 일반 PLC의 EM_OK 읽기만으로 실제 에너지 차단이나 안전등급을 입증할 수 없다.
- PLC: I19.4 → IW18 Word 복사 → DB13.DBX19.4 Inputs.EM_OK → 0458 NOT 접점/SCoil과 별도 RESET/RCoil → DB3.DBX16.6. RESET 가지에는 EM_OK 회복 확인 접점이 없다. 알람 해제나 HMI 표시 변화는 물리 복구 증거가 아니다.
- 온도 허가 두 경로는 별개다. 0173의 Q6.6 Temperature Interlock OK는 TC09/TC01 경보 조건으로 99KA2에 출력한다. I28.4의 177T1_OK는 ER01 온도조절기 입력이며 0271에서 Q5.0 요청의 직렬 조건이다. 같은 온도라는 이름으로 병합하지 않는다.
- 페이지 함정: 범위 FG236은 실제 PDF239의 제어반 온도상승 계산서다. PDF237은 FG234 JB2 단자표다. 계산서의 39°C·36.93°C를 공정 안전 설정값으로 적용하지 않는다.
- 공유 근거: SYS-POWER의 IW18→Inputs, SYS-AUTO의 0168/정지 타입5, TC01의 공동 온도 선택기 미확정, BR01의 FG99 부하5–9 경계는 같은 고정 원본의 기존 조사와 연결한다. 이번에는 위 핵심 원본 핀/선언/실제 PDF를 독립 대조했다. 주변 설비·하위 항목을 같이 완료로 집계하지 않는다.
- 누락: 최신 승인 회로/실물 설치·안전 검증서·모듈 설정·현장 정상극성·외부 버너 내부 회로·현재 CPU 호출/다른 Writer·HMI 이벤트/문구·177T1 설정/명판/검교정. 누락을 추정으로 채우지 않는다.

## 1. 설비·자료 기준

- catalog_id SYS-SAFETY, kind software, 공통 시스템, parent null, phase2. INVENTORY catalog index45, equipment index237. em_ok 별칭 2회는 같은 ID 안의 중복 문자열이다. 독립 실물 2개가 아니다.
- 기준: `gme-research/source-mv06`, Git `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, v1.12.0. 사용자 보고 최신 게시나 로컬 기능 검증과 구별한다. 로컬2차133 통합 제외를 유지한다.
- AGENTS, 저장소 스킬, 작업표준/템플릿, INVENTORY, 최신 인계 최상단, 배치13 지시/범위 및 중복검토 해당 행을 읽었다. 이번 자체 문서조사 승인 범위만 적용했고 원본 코드·공개대장·버전·운영기록은 수정하지 않았다. 모델 런타임 증명 미확인.
- 실제 PDF 렌더 열람 11쪽: 13/14/15/16/97/100/136/143/178/237/239. PDF139는 탐색용 렌더 생성만 했으므로 시각 의미검토 수에서 제외한다. 핵심 LAD 6개와 보조 경계 핀 1개를 검토했다. 검색 hit 수·선정 원본43개 해시를 모든 프로그램 의미검토 수로 바꾸지 않는다.
- 이번 원본 위치의 XML 약칭은 모두 `all-in-one/sources/decoded-original/`, 도면은 `all-in-one/sources/Electrical_Rev2.pdf`, HMI 표는 `all-in-one/sources/hmi_plc_tags.csv`를 뜻한다.

## 2. I/O·HMI

| 구분 | 선언 NID/RID/UID·형식·주소 | 의미와 한계 |
|---|---|---|
| 원시 EM_OK | 0678 SimpleAccess, S=Global, RID173, NID30 UID940 등, Bool AO156, SAD Input SAM=None | %I19.4 프로세스 이미지. 안전 모듈 상태 관찰; 안전 기능 자체 아님 |
| 입력 Word | 0627 SimpleAccess RID25/NID1 UID81, Tag_276 Word AO144, Input SAM=None | %IW18. PIW 직접 접근이라고 쓰지 않음 |
| 내부 Word | 0629 GlobalAccess RID26/NID1 UID82 AK=Write, Word AO144 BAD4;0628 DepDBBlock RID4 TOD13 | DB13.DBW18. Word 복사로 DB13.X19.4 범위를 갱신 |
| 처리 EM_OK | 0657 GlobalAccess RID250/NID51 UID27, Bool AO156 BAD247;0655 Inputs RID247 TOD13 | Inputs.EM_OK=DB13.DBX19.4 읽기. 원시 I19.4와 동일 이름이어도 저장 위치가 다름 |
| 비상 모듈 경보 | 0657 RID253/NID51 UID49 Set,41 Reset AK=Write,40 read, Bool AO134 BAD10;0655 Allarm TOD3 | Allarm.Emergency_module_fault=DB3.DBX16.6 |
| Reset 요청 | 0657 RID13/NID51 UID39, Bool AO48 BAD12;0655 Flag TOD2 | DB2.DBX6.0. 물리 비상 회로 리셋 접점과 별도 |
| 온도 원시 입력 | 0627 SimpleAccess RID141/NID1 UID87, Bool AO228 Input SAM=None | 177T1_OK=%I28.4 |
| 온도 처리 비트 | 0629 RID148/NID1 UID126 Write, AO180 BAD4;0604 RID266/NID41 UID31 read | Inputs.177T1_OK=DB13.DBX22.4. raw byte28을 그대로 DB byte28이라고 간주하지 않음 |
| ER01 명령 | 0602 SimpleAccess RID185/NID41 UID1136 Write, Bool AO40 Output | Start ER-01=%Q5.0. 요청 출력이며 가열부 실동작 피드백 아님 |
| 버너 온도 허가 | 0582 SimpleAccess RID26/NID3 UID154 Write, Bool AO54 Output | Temperature Interlock OK=%Q6.6 |
| 온도 허가 원인 | 0585 RID24/NID3 UID152 AO71, RID25/NID3 UID153 AO65 | Allarm.MAX_MAX_TC09=DB3.X8.7, MAX_MAX_TC01_TEMP=DB3.X8.1 |
| 에지 기억 | 0575 SimpleAccess RID109/NID10 UID51 AK=RW, Bool AO725 Memory | Tag_292=%M90.5. HMI 태그나 타이머 아님 |

GlobalAccess와 SimpleAccess 모두 S=Global인 위 선언을 Local 임시 변수로 취급하지 않는다. SSD.AO는 위 Bool/Word에서 bit offset이며 byte/bit로 환산했다. 0628/0655/0576의 DepDBBlock TOD와 결속했다. UID는 파일·NID·RID 문맥 안에서만 연결한다.

HMI CSV에서는 `Allarmi_190,"DB3,X16.6",PLC,00407`이 비상 모듈 경보 주소에 대응한다. `Allarmi_140,"DB3,X17.4",PLC,00102`는 공동 TC1/2 EmergencyStopTC1_2의 주소이며 다른 경보다. EB19(00374), EB28(000BB)은 원시 입력 byte 설정이다. 이 주소표만으로 화면 버튼/ACK/Reset 스크립트·알람 메시지 문구·쓰기 권한이나 실제 통신 정상은 확인되지 않는다. Allarmi 숫자를 PLC 비트 번호로 그대로 읽지 않는다.

## 3. 제어 구조

### 3.1 원시 EM_OK의 Word 전달

0397-FlgNet, 색인 LAD1070/NID1. P78 Move(Cardinality1, DisableENO=true), W21 Powerrail→en, W88 ORef81/RID25→in, W90 out1→ORef82/RID26: IW18→DB13.DBW18. W89 eno→P79.en 연쇄도 보존한다. 일반 Word 복사이지 EM_OK 전용 코일이 아니다. CRef 호출 없음. 현행 호출순서와 ENO 실행 결과를 단편만으로 입증하지 않는다.

### 3.2 비상 모듈 알람 기억

0458-FlgNet, 색인 LAD1824, block allarms1 index44, 선언 NID51. index44를 선언 NID44로 바꾸지 않는다.

- ORef27/RID250→W25→Contact26.operand, Negated operand. W21 rail→26.in, W42 out→SCoil31.in, W48 ORef49/RID253→31.operand. `NOT Inputs.EM_OK`가 Set 경로다.
- 별도 W21 rail→Contact36.in. ORef39/RID13 Reset→W43→36.operand, W44→Contact37.in. ORef40/RID253 경보→W45→37.operand. W46→RCoil38.in, W47 ORef41/RID253→38.operand.
- Reset 경로는 RESET_ALLARM AND 현재 경보다. 이 가지에는 EM_OK 회복 접점이 없다. Set/R가 모두 성립하는 경우를 단일 OR 식으로 줄이지 않는다. 네트워크 출력 쓰기 순서/스캔/다른 Writer·현행 CPU는 별도 확인 사항이다. 이 LAD에는 타이머·환산·CRef가 없다.

### 3.3 비상 알람의 일반 자동 정지 요청

0168-FlgNet, LAD1846, NID10. PContact21.operand에 W50 ORef52/RID108 비상경보, bit에 W49 ORef51/RID109 Tag_292가 연결된다. 상승 에지 out→W48→Move22.en. W34의 literal0→in, W36 out1→ORef27/RID7 Data.Tempo_presetting. W35 eno→Move23.en, W37 literal5→in, W39 out1→ORef29/RID12 Data.Tipo_preset. W38 eno→SCoil24.in, W40 ORef30/RID4 Flag.Auto_ON1.

0577/0576: Tempo는 Int AO768=DB1.DBW96, Tipo는 Int AO784=DB1.DBW98, Auto는 Bool AO59=DB2.DBX7.3. Move22/23 DisableENO=true와 ENO 연쇄를 보존한다. Auto Set은 이 문맥에서 정지 타입5를 진행시키는 요청이다. 생산 자동재기동 승인으로 읽지 않는다. 전체 0164/65/66/69 조건/다른 쓰기는 SYS-AUTO 기존 문서 범위에 연결하고 여기에서 전부 검증했다고 주장하지 않는다.

### 3.4 버너 온도 허가 출력

0173-FlgNet, LAD1856/NID3. P160 Contact ON, P162 NOT MAX_MAX_TC09, P164 NOT MAX_MAX_TC01_TEMP, P150 Coil이다. W166 rail→160.in; W155 ORef151→160.operand; W161→162.in; W156 ORef152→162.operand; W163→164.in; W157 ORef153→164.operand; W165→150.in; W159 ORef154→150.operand.

이 네트워크의 Q6.6 식은 `ON AND NOT MAX_MAX_TC09 AND NOT MAX_MAX_TC01_TEMP`. ON은 0582 RID1/NID3 UID151 Memory AO0=%M0.0이며 literal TRUE로 바꾸지 않는다. 네트워크 제목 `a 56.3 max.temperaturefilter`는 선언 Q6.6 및 FG142 A6.6과 주소 표현이 상충한다. 원문 제목을 보존하고 현재 주소를 제목에서 추정하지 않는다. TC별 경보 임계·지연 생성은 해당 TC 문서 소유다.

### 3.5 177T1 입력과 ER01 출력

0397 P86 Contact→P125 Coil: W21 rail→86.in, W85 ORef87/RID141→operand, W129 out→125.in, W128 ORef126/RID148→operand. NOT 없음. I28.4가 DB13.X22.4로 bit 복사된다.

0271-FlgNet, LAD1971/NID41. W1159 rail→P1149(ON), W1150→P1157 Flag.M_ER01. W1145 ORef1135/RID192→1157.operand, W1158→P30.in, W29 ORef31/RID266 Inputs.177T1_OK→30.operand, W32→Coil1129.in, W1147 ORef1136/RID185→operand. 따라서 이 출력 가지는 ON AND M_ER01 AND Inputs.177T1_OK다.

다른 가지: ON 뒤 OFF(Contact1151), Allarm.ER01_run(Contact22), NOT Inputs.FN-05 RUN(Contact26) AND NOT UNDER TESTING(Contact1155)이 OR1120.in1/2/3로 모인다(W1152/24/1156). W1142 OR.out→RCoil1125, W1144 ORef1134/RID192 Flag.M_ER01. 요청 Reset과 현재 출력 허가는 별개다. 이 LAD에는 온도 숫자 설정이나 타이머가 없다. ER01 전력회로 전체·가열부 정상은 이번 범위에서 미확인이다.

### 3.6 EM_OK의 부수 사용과 조사 경계

0511-FlgNet NID30: ORef940/RID173 EM_OK→W951→NOT Contact963, W965 rail→in, W964 out→Move917/922/927/932/937.en. W952/953에서 CNT_Act_0→Memory encoder.Encoder_CH00, 이후 같은 네트워크의 W954~961로 CH01~04에 각각 저장한다. 제목 power-off라는 이유만으로 정전 전체 감지나 비휘발 보존을 보증하지 않는다.

0506에는 EM_OK ORef26/RID173→W53→P22 Contact.operand, P22.out→W54→TM 계열 LRef23.en 연결이 있다. SwGate는 별도 ORef27/RID207→W55로 연결되므로 EM_OK와 직접 동일시하지 않는다. 전체 TM 진단/환산은 SYS-PLC-IO와 개별 MV 소유다. 0507~0510,0512~0516은 검색 색인에서 EM_OK 사용처로 확인했지만 이번 전체 의미검토 대상이 아니다.

0635 NID18 UID43/RID353에 Inputs.EM_OK 추가쓰기 선언이 검색되었다. 중지 simulation 문맥의 흔적이므로 현재 실행 Writer로 인정하지 않는다. 해당 블록을 실행·수정·생성·행동시험하지 않았다. 0650의 Manage_TC1_2.EmergencyStop RID95와 Allarm.EmergencyStopTC1_2 RID96은 NID9 쓰기 선언이다. 기존 TC01 조사처럼 SCL 검색 색인과 실행 원본을 구분하고 이번에는 선언/별도 경계까지만 확인했다. 다른 일반 온도 알람을 물리 13KA1의 입력 조건으로 창작하지 않는다.

## 4. 전기 전달 경로

아래 페이지의 footer를 실제 렌더로 확인했다. FG12/13/14/15/96/99/135/142/177/234는 기본 DATA 27.05.2024, 개정란에 별도 Rev 기입을 보지 못했다. 파일명 Rev2만으로 모든 쪽을 Rev2라고 하지 않는다. FG236 계산서는 일반 회로 footer 양식/개정란이 없고 하단 번호236이다.

| FG / 실제 PDF | 실제 문서 경로·끝점 | 해석·미확정 |
|---|---|---|
|12 /13|12SB1 두 접점, X20 2003–2004·2005–2006, X1 1–4의12SB2(PB4),5–8의12SB3(PB5),9–12의12SB4(PB6); 이어 EMERGENCY AVAILABLE 단자 경로 X1 13~40; 12.1/12.2/12.23/12.24→13/0|실제 설치된 추가 비상장치 종류·단자 사용·점퍼 상태 미확인 |
|12 /13|12SH1 접점13–14, X20 2007–2008; 14KA1/2/3/4/5/9 및14KA6/7/8·15KA1/2·14KA10의31–32 접점열,12.37/12.38→13/3|물리 feedback/start 경로를 PLC RESET_ALLARM과 동일시하지 않음 |
|13 /14|13KA1 도면 표기 SIEMENS 3SK1111-1AB30. +24Vdc10.7→13FU1 1A→A1+, A2−→0Vdc10.6. T1/IN1 및 T2/IN2에12.1/.23/.2/.24, T3–IN3 도면 연결, T4/IN F/S에12.37/.38|도면 모델 표기이며 현장 모델·AUTO/MONITORED 선택 실제 위치·인증 증거 아님 |
|13 /14|110Vac9.8→13FU2 6A의 두 경로→13/23, 출력14→13.5(14/0),24→13.6(14/5). +24Vdc→33,34→E19.4(135/5)|부하 제어와 PLC 상태 관찰을 분리. 접점 동작·차단 성능·정상 극성 현장 미확인 |
|13 /14|41–42 접점 출력→13.7→X20 2009→12SH1 파랑 램프→0Vdc10.6|램프 상태만으로 모든 기계 안전확인 불가 |
|14 /15|13.5→14KA1/2/3/4/9 A1,13.6→14KA5/6/7/8/10 A1,각 A2→0Vac9.9|코일/하단접점표와 실제 개별 부하 회로는 별도; 전체 부하 차단 검증 아님 |
|15 /16|110Vac→15FU1 16A→14KA4의3–4와14KA8의3–4→15KA1 A1; 병렬 두 번째는 각각5–6→15KA2 A1; A2→0Vac|보호값은 원문 표기만. 현행 선정/보호 정정·변경 지시가 아님 |
|135 /136|E19.4←13/5, 도면 CPU515/MOD12 단자35 GENERAL EMERGENCY SAFETY MODULE OK|현재 CPU 형식/실제 장착 검증 아님. E19.5~19.7 전압/음소거/Reset와 다른 입력 |
|177 /178|+24Vdc152.5→X3:117 퓨즈2A F→177T1 접점11–12→X3:118→X22:4007→E28.4 단자5, Rack3 MOD4|THERMOSTAT ELECTRICAL RESISTANCE ER-01. 설정값/정상극성/검교정 미확인 |
|142 /143|A6.6 단자27→99/3, MAX.TEMPERATURE FILTER|선언 %Q6.6과 연결. 모듈 전원 X21:3034 4A F 및24Vdc10.9는 도면 값 |
|99 /100|A6.6→99KA2 A1,A2→0Vdc10.6; 외부 X/1/2→X1:390→99KA2 부하5–9→X1:391→X/1/4|외부 도면010-390/BP N300 참조. 외부 버너 내부 순서·안전등급 미확인 |
|99 /100|99KA1/3/4도 부하5–9,99KA5는1/5/9 전환 배선으로 X1:396/397/398|하단 접점표1/5/9를 모든 부하1–9로 읽지 않음. 다른 출력은 BR01 소유 |
|234 /237|QG–X23 PLC BOX JB2 TERMINAL BOARD, E30/31와A23 단자표|FG236 찾기 과정에서 확인한 다른 쪽. 비상정지 회로 근거로 채택하지 않음 |
|236 /239|CEI17-43 enclosure temperature-rise assessment, OVER TEMPERATURE CONTROL BOARD. Ambient25, maximum acceptable39, 계산 without cooling112.03/selected fan36.93,LEGRAND034863/2500m³h|설계 계산값이다. 실제 측정·공정 trip 값·인증·현장 정상 근거 아님 |

PDF97/FG96은 질소 수동 주입 EMERGENCY PUSH-BUTTON(6SB1~3)과96KA1, PV05/06,96KT1 경로였다. 이 장치들을 FG12 비상정지 접점열과 같은 기능으로 합치지 않는다. 기존 PV05/PV06 문서의 소유 경계에 남기며 이 문서에서는 PDF 탐색에서 확인한 구분만 기록한다.

## 5. 알람·복구

| 항목 | 문서상 발생/유지/영향 | 복구 판단 경계 |
|---|---|---|
|Emergency_module_fault|0458 NOT 처리EM_OK로 S; RESET 요청 AND 경보로 R, 타이머 없음;0168 상승에지 정지 타입5 요청|입력 회복, 경보 Reset, 물리13KA1 상태, 기계 정지, 재기동 승인 각각 별도 증거 필요 |
|온도 허가 Q6.6|0173 ON AND 두 상한 경보 부정.99KA2 외부허가|TC 원인 해소·일반 PLC 출력 변화만으로 버너 내부 안전 회복 확정 금지 |
|177T1_OK|0397 처리 후0271 ER01 명령 직렬 조건|177T1의실물 설정/온도/접점과 입력 비교 필요. 강제신호·접점우회·보호값변경 금지 |
|EmergencyStopTC1_2|공동 온도 선택기 별도 Bool, HMI DB3.X17.4|물리 비상정지와 이름만으로 병합 금지; SCL 원본/현재실행 미확정 |

운전자 알람 확인(ACK), 내부 요청 Reset, 물리 start/reset 및 재기동은 같은 작업이 아니다. 반복 Reset이나 시험 운전을 복구법으로 제안하지 않는다. 이 조사에는 실제 조치·복구 기록이 없다.

## 6. 증상별 관찰·수리 경계

| 증상 | 기록할 관찰점 | 비교 근거 / 필요한 다음 증거 |
|---|---|---|
|HMI 비상 경보가남음|시각, Allarmi_190,DB3.X16.6, DB13.X19.4,I19.4|0458 S/R과0397 Word 전달 대조. HMI 표시 지연/현재 프로젝트 결속은 별도 확인 |
|입력값은복귀했는데경보유지|원시와처리값,RESET 요청의 실제발생시각|기억형 S/R이므로 신호 복귀와 경보 해제 분리. 안전담당자의 승인 절차 없이 Reset/기동 지시하지 않음 |
|Auto_ON1이비상후Set됨|Tipo_preset,Tempo,Auto,M90.5|0168 정지 타입5 진행용 Set 여부와 전체정지 문맥 확인. 생산재개로 추정하지 않음 |
|버너온도허가가안나옴|ON(M0.0),DB3.X8.7/X8.1,Q6.6,외부허가응답 기록|0173→FG142/99. 외부010-390 확보 전 내부버너 고장을 단정하지 않음 |
|ER01요청은있는데출력없음|M_ER01,Inputs.177T1_OK,I28.4,Q5.0,FN05관련입력|0271 직렬조건/Reset 가지와FG177 대조.177T1 설정값 추정·변경 금지 |
|13KA1또는램프와PLC표시가다름|승인된안전관찰기록,도면판본,장치명판,시각|33–34/E19.4와41–42/램프는 별도접점. 활선측정/우회시험은 본문 범위 밖 |

관찰 기록 양식: 관찰자,시각·시간대,장치·위치,값/단위,수집방법,프로젝트/도면판본,비교근거,배제한원인,승인조치,후속복구증거. 현장 미지 필드를 0/정상으로 채우지 않고 운영기록은 공개원본에 복사하지 않는다.

## 7. 완료·누락·인계

- 문서: 7영역 초안 complete_with_gaps. 선택43개 원본 전체SHA256/고정Git blob내용 일치, 중지5자산 원래freeze 해시 일치, 원본Git dirty 없음.
- 정적 검토: 직접 핵심 0397/0458/0168/0173/0271/0511 및 선언,0506 경계핀만 확인. 11 PDF 실제 열람. 원본 전체 네트워크 전수 의미검토·TIA컴파일·실물시험으로 표현하지 않는다.
- 구현/화면/기록/게시: not_performed. 도면·래더 비교/백업선택복원/기록전후비교/보고서PDF 네 기능은 새 SYS-SAFETY 적용이나 저장·재열기 검증을 수행하지 않았다. 기존 데이터/미지필드/초안/저장키 그대로 보존.
- TIA/current CPU/field recovery: not_performed. 시뮬레이터실행·생성·수정·행동시험0,PLC/현장/보호값/SEJIN변경0. 원본 build/test/generator 미실행.
- 다음 필요한 자료: (1)최신 승인 안전회로와 장치/배선 as-built,13KA1 설정·명판·검증서 (2)외부버너010-390과허가/응답 결속 (3)177T1 모델·설정·검교정 (4)현재PLC호출/다른Writer와HMI이벤트 (5)승인된현장관찰·복구확인 기록. 새 자료가 없으면 동일 미확정 반복조사 대신 다음 독립ID 진행.
- 자체 산출물: `extracts/SYS-SAFETY/checks.json`, `source-hashes.json`, `declarations-selected.json`, 원본 PDF 렌더/텍스트와 선별 XML pretty 출력. 부모가 독립검토·첨부하며 이 초안은원본보존 후필요시별도보강한다.

## 실제 작업 시각 UTC

- 2026-10-11 12:12:04: 배정 지시/범위 읽기 시작.
- 2026-10-11 12:12:43: 고유 선언·네트워크 검색/추출 확보.
- 2026-10-11 12:12:57~12:14:54: 실제 PDF 렌더 순차 열람 및 페이지/끝점 대조.
- 2026-10-11 12:15:47: 원본43개 Git내용/SHA256 및 중지5자산 검사 완료.

## 전체 선정 원본 SHA256·Git blob 표

아래는 선정43개 파일의 전체목록이다. 선택해시 수는 의미검토 완료 수가 아니다. 중지 자산5개는 바이트 보존 확인만 수행했다.

| 원본 상대경로 | SHA256 | 고정 Git blob | 내용 일치 |
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
| `all-in-one/sources/decoded-original/0168-FlgNet.xml` | `6e69605abd053c1d85f668b8e29bf98975e7e6b9ec1903b017af2048602d4847` | `13262ff07cb094ffd38d9c00a5281c68f4c9ca2b` | True |
| `all-in-one/sources/decoded-original/0173-FlgNet.xml` | `b4f2002933f13ad38f8b8bc6daa3f3ef11a9181ea1c2f33f63ef7a3f7305dc07` | `a880d18b10887c0385745539ab80f8fb45e7647b` | True |
| `all-in-one/sources/decoded-original/0271-FlgNet.xml` | `7f913249a7879930d8443291b542374887e8cbbe89b55993a51233446008521b` | `9acac1bcf06da142b6d3f3d288788dbd7ab1c212` | True |
| `all-in-one/sources/decoded-original/0397-FlgNet.xml` | `bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834` | `4ab8370493c4e28fc1eabeeebe2743d27f0c4021` | True |
| `all-in-one/sources/decoded-original/0458-FlgNet.xml` | `681fb4a754ebd79a6446982b3203afa5e549607cfc1254ccebb0d591be49f5ca` | `8ede582e73514edef4d1762c7332ed46e08ce1ec` | True |
| `all-in-one/sources/decoded-original/0506-FlgNet.xml` | `71b9ac920eb891ec8965506c40ae3f1d050a2f8a899f79f6afdc81f669717fbe` | `8e26b2cc02f4e38863022d2fb8da0f7322e2125f` | True |
| `all-in-one/sources/decoded-original/0511-FlgNet.xml` | `a4bf314bf817f0f666a0c9fdd26df134cedeed8666819c7a3e8e6438850eace6` | `2730bc98903fc1a89effa1911c5ac82ddd7b4957` | True |
| `all-in-one/sources/decoded-original/0575-IdentXmlPart.xml` | `40e7b2caf89ab7f1ed9075547a7728bd02441e24451bdd8bf97c843637daad06` | `07d5d2548e8f36252a346d0b83341e27c3cb14ba` | True |
| `all-in-one/sources/decoded-original/0576-IdentXmlPart.xml` | `c8b5f9b9ead0e124f1f817b49d89611ed7b2ce04ecd91ddaa139f2ec89d48dbe` | `819b47160eaa6d08c212f71e5b5486ef5b55b6f2` | True |
| `all-in-one/sources/decoded-original/0577-IdentXmlPart.xml` | `511e01fae619dc385357908a1ac62030dbdfd5f5399bd4c22bc58bebbfc3bf47` | `a505ebf7efd05a85850dc29559a4f71242bacae3` | True |
| `all-in-one/sources/decoded-original/0582-IdentXmlPart.xml` | `41d4c2bd750392bbc2edc43995ec3a9da47a63c13ee86496df8f187492008951` | `82636dec064876d0f4cc714ef385b07d6e05efe0` | True |
| `all-in-one/sources/decoded-original/0585-IdentXmlPart.xml` | `e36ec18aa4abebea8f9160254522bb51ff722eae804c5a469790f85f02939184` | `16574d37ef3ca61b59ba396c400e269ab1dd3440` | True |
| `all-in-one/sources/decoded-original/0602-IdentXmlPart.xml` | `46ab21151eddaaf616469db520730c60423eb742aa491af194e6710c751b4caf` | `bcb12ab1ce8c476ff921baa1608f29d9822f76b4` | True |
| `all-in-one/sources/decoded-original/0603-IdentXmlPart.xml` | `e93969dfa281d75b49b24127793068e33472dadb19729c1c48fc4a8dad075ef8` | `3a92b304baf4dbf6147e944d9778d2da11285cb1` | True |
| `all-in-one/sources/decoded-original/0604-IdentXmlPart.xml` | `b798d29c5499b5314a1ee3cff9139dae64c887533b86baa43b6e9a052373a6af` | `bb2c318788b97e7a4924a176275c12d805aa519d` | True |
| `all-in-one/sources/decoded-original/0627-IdentXmlPart.xml` | `08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb` | `61ebc0abbb2ca160e11e1da400a3f14a397d8bc5` | True |
| `all-in-one/sources/decoded-original/0628-IdentXmlPart.xml` | `9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd` | `170ca5c72599edc7ea7eefe651c3680ce325e76a` | True |
| `all-in-one/sources/decoded-original/0629-IdentXmlPart.xml` | `67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972` | `058129bb01e27f7a6a0d0293f332d745e5bab74e` | True |
| `all-in-one/sources/decoded-original/0635-IdentXmlPart.xml` | `1a057d686446a3fdab7ac61bb09bc543c52f49646c9ca71ac323c10fcdffe457` | `95bfcad59cfb0c12b573e9e8face4262d1e94622` | True |
| `all-in-one/sources/decoded-original/0650-IdentXmlPart.xml` | `86f53657eb7afb0798da0e215ba226721076c2ab1b25b74eb83e7b3c4b2d8a2d` | `a3d80a76ef5b0d00009c0fc9a1fdeb1471d0b67b` | True |
| `all-in-one/sources/decoded-original/0655-IdentXmlPart.xml` | `38e9f323024fba19582b473f39b1ed03ffe6a0b390218894029a6edb0b1ff9fb` | `83b60b9de4541a3ffa6ee0db98205a372b525665` | True |
| `all-in-one/sources/decoded-original/0657-IdentXmlPart.xml` | `0f70cda60a6b1a17175876d58e25b2686952642de6cffb21213aeef8b347a22b` | `e625f3d8999c7be7d88c50eab0d93107117b58ec` | True |
| `all-in-one/sources/decoded-original/0678-IdentXmlPart.xml` | `51e637e0b9713c028810f2a717b5c3804a3a26c2f1be7e332a4d6bf277bfc382` | `7fafb2297bcdf739bf1d1dd68cebc0d74f2a40cc` | True |
| `all-in-one/sources/decoded-original/identifier-declarations.json` | `0f74123ad80664acdeeb10c29f3e1e73a98d76e5d22169723977371a88768944` | `47e3fed72075945b05f7fc84112b5609551b6ef8` | True |
| `all-in-one/sources/decoded-original/network-map.json` | `c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60` | `424430b6b953e43138e5d0a18ca40c949e21cfa1` | True |
| `all-in-one/sources/hmi_plc_tags.csv` | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` | `cf4c0650e7c7baac350dcb89909b808435704880` | True |
| `docs/equipment-standard/INVENTORY.json` | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` | `587c3748ad9224718f95ba06463fee913dae231d` | True |
| `docs/equipment-standard/WORK-ITEM-TEMPLATE.md` | `4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586` | `e546f39535d2b589e80f97db869ac37ce4d05cfd` | True |
| `docs/equipment-standard/WORK-STANDARD.md` | `05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99` | `f76a570cc73098632e08759b17934000f7e3a253` | True |

초안 작성 종료 실제 시각: 2026-10-11T12:18:56.850422+00:00
