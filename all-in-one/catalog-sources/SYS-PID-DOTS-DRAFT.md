# SYS-PID — 온도·압력·산소·비율 제어 7영역 자체 조사 초안

## 핵심 확인·상충·누락·공유 근거

- SYS-PID 한 catalog ID의 문서 조사다. 온도계·밸브·버너·SYS-AUTO 전체를 함께 완료로 집계하지 않는다. 원본 고정 `abcf31c5030bc7ef8749ed8e869a857f2387a28a / v1.12.0`이며 현행 CPU/로컬 최신 게시판본 증명이 아니다.
- 두 주기 OB의 이름/색인과 실제 0024·0028 호출 핀을 구별했다. 이름 1s/100ms 및 PID CYCLE 인자가 현행 CPU 인터럽트 주기·우선순위·실시간 응답을 보장하지 않는다.
- 0195 비율 CONT_C: COM_RST는 NOT Inputs.High Flame Gas이고 MAN_ON은 `ON AND ((NOT High Flame Gas AND Disable masses) OR OFF)` 접속이다. ON/OFF는 M0.0/M0.1 Global Bool이며 상수 true/false가 아니다. 고화염 응답을 실제 화염 검출·안전허가로 대체하지 않는다.
- 0194 이론 가스곡선은 0,5,…95의 **20개 독립 ≥ 비교와 같은 Local Int 목적지 쓰기**다. 제목의 구간명을 배타적 CASE나 보간 계산으로 바꾸지 않는다. 실행순서·음수 입력에서 Local 값의 유효성은 별도 확인 대상이다.
- TC01/02 선택 SCL1719의 TC02-only 가지에도 TC01_OFR/EnableTC01이 적혀 있다. 오류처럼 보여도 원문을 정정하지 않는다. SCL/STL 색인과 선언을 대조했으나 별도 원형 실행 본문/현재 CPU는 미확보다.
- 0478 VT02Manuale에는 OR의 세 번째 ON 가지가 있다. ON이 참이면 수동 비트가 참이 되는 접속이며, 단순히 MV04_Auto/FN02 조건만으로 자동 전환한다고 쓰지 않는다. 제외 MV04를 새 조사·완료 대상에 넣지 않았다.
- 출력은 CONT_S의 M-bit, CONT_C의 Local Real, DB1 설정 Word, PQW308/310을 구분한다. 0468 Mul.eno→Move22.en과 PQW쓰기/QW읽기의 접근 차이를 보존했다.
- 공유 인덱스: [MV01](MV01-DOTS-DRAFT.md)·[MV03](MV03-DOTS-DRAFT.md)·[MV06](MV06-DOTS-DRAFT.md)의 방향/한계/복수쓰기, [PSH01](PSH01-DOTS-DRAFT.md)·[PC02](PC02-DOTS-DRAFT.md)의 압력 공급원, [TC01](TC01-DOTS-DRAFT.md)·[TC02](TC02-DOTS-DRAFT.md)·[TC03](TC03-DOTS-DRAFT.md)의 환산/선택/경보, [TC11](TC11-DOTS-DRAFT.md)의 PLC 미식별, [BR01](BR01-DOTS-DRAFT.md)의 버너 끝점, [SYS-AUTO](SYS-AUTO-DOTS-DRAFT.md)·[SYS-ALARM](SYS-ALARM-DOTS-DRAFT.md)·[SYS-HMI](SYS-HMI-DOTS-DRAFT.md)의 공통 기능 경계를 연결 재사용했다. 각 설비 전체 논리를 다시 검토했다는 뜻은 아니다.

## 1. 설비·자료 기준

INVENTORY catalog[40]: SYS-PID, software, 공통 시스템, parent=null, depth0, phase2/planned, priority=null, baseline. 별칭 tc_pid_ref/stechiometro는 검색어이며 센서 두 개 또는 단일 실물이라는 뜻이 아니다. electrical_fgs=[]이며 직접 물리 단자는 비해당, 관련 출력 끝점은 §4에 한정한다.

BATCH12 지시/범위, overlap 대상, root AGENTS·rollout SKILL·WORK-STANDARD·WORK-ITEM-TEMPLATE·INVENTORY, 버전/인계/게시/ACTIVE-WORK/EXPANSION 최신 머리말을 읽었다. 런타임 모델·추론 수준 증명 미확인. 작업 시작 관측 2026-10-11 11:55:55 UTC. 허용된 자체 파싱·해시·PDF 렌더만 수행했다. 원본 스크립트/build/test/generator, 새 Work/Codex, 재위임, TIA·PLC·시뮬레이터·현장·보호값·SEJIN 변경은 0이다. 산출 쓰기는 이 MD와 `extracts/SYS-PID/`뿐이다.

약칭 XML 번호는 `all-in-one/sources/decoded-original/NNNN-FlgNet.xml` 또는 `NNNN-IdentXmlPart.xml`; live_index 및 CSV/PDF는 `all-in-one/sources/` 기준이다. doc/LAD 번호, 파일번호, 원본 NID, UID/RID는 서로 다른 식별자다. UID/RID 전역 일치만으로 결속하지 않고 블록·NID·선언종류·AO·핀을 함께 확인했다.

대표 의미검토는 0194~0197의 비율 분기/제한, 0023/0024/0028/0416/0417의 호출·버너 전달, 0475~0480의 선택된 PID/모드/최저설정, 0187/0467/0468의 출력 경계다. 추출한 핀 전체와 선언은 JSON에 보존했지만 모든 네트워크 전체 실행 의미, 전체 Writer 우선순위, 모든 PID 인스턴스 내부 구현을 검증한 것은 아니다.

## 2. I/O·HMI — Global, Local, Word, bit 구분

|관찰점|원본 선언·주소·형식|소유/경계|
|---|---|---|
|TC 선택 enable|0650 RID75/76 AO0/1, 0648 DB39|DB39.X0.0/.1 Bool. 실제 HMI 클릭·권한 미확인|
|PID_Ref_Temp|0650 RID91 AO16 Real, DB39|DB39.DBD2; NID9 UID4019/3796/3709 Write, NID7 UID36 Read|
|EmergencyStop/공통전달|0650 RID95 AO48, RID96 AO140|DB39.X6.0 → DB3.X17.4 관련 선택기 출력. 실제 안전 정지 장치 증명 아님|
|Flag AutoBurner|0652 RID10 Memory AO120 Bool|M15.0. 수동 Local은 STL 색인의 NOT 관계|
|Burner_PID_Result|0650 RID33 AO96 Int, 0648 DB6|DB6.DBW12, 0416/0023 복수쓰기|
|Burner_Panel_SetPoint / Air_Out|0650 RID6/41 AO176/144 Int, DB1|DB1.DBW22/18. 0187 전달·0417 증감·0467 제한/환산|
|Burner_Gas_Out|0591 RID99 AO2016 Int, 0590 Data DB1|DB1.DBW252. 비율 합산 색인·0196/0468 제한 쓰기|
|MASSICO_FLOW_AIR/GAS|0591 RID67/69 AO1696/1680 Int, DB1|DB1.DBW212/210. PIW 자체 아닌 환산값; 공급원0505/0504는 BR01 공유근거|
|Set_stechio / Real_stechio|0591 RID73/72 AO0/32 Real,0590 DB5|DB5.DBD0/4. 설정과 계산비율 분리|
|PID_GAIN / PID_TI / PID_TD|0591 RID89/90/91 AO64/96/128|DB5.DBD8 Real, DBD12/16 Time. Time32를 Real 튜닝값으로 변환하지 않음|
|Limite_min / MAX|0591 RID95/94 AO160/192 Real|DB5.DBD20/24. 현행값·안전한계 미확인|
|Sign_lim_min / MAX|0591 RID103/104 AO224/225 Bool|DB5.X28.0/.1, 일반 Coil 출력이며 래치 경보가 아님|
|High Flame Gas|0591 RID124 AO143 Bool,0590 DB13|DB13.X17.7 처리 응답. 직접 raw I/화염 검출과 구분|
|Disable masses / ON / OFF|0588 RID77/1/78 AO640/0/1|M80.0/M0.0/M0.1 Global Bool|
|Stechio_attuale / SetPoint_Stechio|0589 Local RID71/74 AO208/240 Real|NID2 생산 → NID3 UID685/684 소비. AO를 DB 주소로 만들지 않음|
|Correzione_Stechio|0589 Local RID97 AO64 Real|0195 LMN→UID701 Write, NID4 UID499 및 NID6 UID600/603 Read|
|Portata_Presunta_GAS|0589 Local RID9 AO112 Int|0194 NID1 UID533…609 다수 Write; NID4 UID511 Read|

Global DB 주소는 DepDBBlock TOD와 BAD/이름 문맥으로 확인했다. 같은 RID91도 0650은 PID_Ref_Temp, 0591은 PID_TD다. 같은 UID249도 0417의 Air_Out operand이고 다른 블록의 선언/CallRef와 병합할 수 없다. 0023 ORef179는 원본 RefId35이며 0649 Constant RID35 NID3 UID179의 0과 결속된다. 파생 network-map에서 이름이 비어 있어도 원본 RefId/선언이 없다는 뜻은 아니다.

### HMI CSV 직접 주소 대조

|CSV 이름|주소·ID|판단|
|---|---|---|
|TC_PID_REF|DB39,REAL2 /001C0|선택온도 주소와 일치|
|Stechiometro / Stechio_ratio|DB5,REAL4 /00421, DB5,REAL0 /003F6|현재계산비율/설정비율 주소|
|Stechio_GAIN|DB5,REAL8 /000E5|Real 설정주소|
|Stechio_TI / Stechio_TD|DB5,D12 /003F4, DB5,D16 /003F5|CSV D 표기와 PLC Time 선언을 구분|
|Stechio_min_limit / MAX_limit|DB5,REAL20 /000E2, DB5,REAL24 /001D9|제한값 설정주소|

모두 Access Name PLC, dde.cfg 설정 추출이다. 화면 위젯·쓰기 이벤트·초/밀리초 표시변환·통신·온라인 값은 검증하지 않았다. SYS-HMI의 공통 주소/이벤트 한계를 재사용한다.

## 3. 제어 구조 — 호출, 선택, 수자동, 제한, 출력

### 3.1 OB와 호출 경계

live_index `_7ev/1716`은 cyc_int2 ogni 1s/cyclic interrupt, `_7ev/1232`는 ob_cyclic 값32다. `_7ex/1`은 cyc_int5 ogni 100ms, `_7ev/1367`은 ob_cyclic 값35다. 이는 백업 명칭/색인이다.

- 0024 NID4: ON ORef185→W187 Contact188.operand, W189→CRef183.en, CodeBlock186/RID39. 0067 FCBlock Auto start motors TOD FC30, NID4 UID186 Call. SYS-AUTO의 FC 제목 1ms/호출자 이름1s 상충을 보존한다.
- 0028 NID13: ON ORef26→W25 Contact513; W24→CRef508.en, CodeBlock511 RID109. 0069 FCBlock Control_stechio TOD FC13, NID13 UID511 Call. 100ms를 현재 하드웨어 인터럽트 설정 확인으로 확대하지 않는다.
- 0195 NID3 LRef663 RID112는 0593 CONT_C, Instance664 RID86은 0055 PID_Stechio DB40이다. CRef 호출과 LRef 라이브러리 호출을 혼동하지 않는다.
- PID-BURNER는 0647 DB20/NID7 UID71 InstanceDB, 0653 CONT_C RID46/NID7 UID70·72 Call 선언이다. 라이브러리 선언의 S7300/S7400/S71500 대상 목록은 현재 CPU 모델의 증명이 아니다.

### 3.2 TC 선택과 버너 PID: 색인 근거의 명확한 한계

`live_index _7ev/1719 SCL Code`와 0650 NID9 선언:

1. 두 enable 참, 두 OFR 거짓이면 TC01/TC02 평균을 PID_Ref_Temp에 쓴다.
2. 두 enable 참에서 TC01_OFR이면 EnableTC01=false, elsif TC02_OFR이면 EnableTC02=false; 그 가지 EmergencyStop=false.
3. TC01-only는 Temp_TC01을 선택하고 TC01_OFR이면 EnableTC01=false.
4. TC02-only는 Temp_TC02를 선택하지만 **TC01_OFR이면 EnableTC01=false라는 원문**을 그대로 보존한다.
5. 둘 다 비활성이면 EmergencyStop=true, 뒤에서 Allarm.EmergencyStopTC1_2로 대입한다.

이는 TC01/02 공동 기능이며 TC11의 PLC 미식별을 임의 채워 넣지 않는다. enable 변경 뒤 같은 scan 재평가, 실패 시 PID값 유지, 타입 승격은 현재 근거로 확정하지 않는다. 해당 원형 SCL 실행본문/동일 NID FlgNet 미확보다.

`_7ev/1720 STL Code`는 TC01_SETPOINT·Burner_Panel_SetPoint·MAX_PRC_BR1을 ITD→DTR로 Local sp/man/max에 전달하고, 이미 Real인 PID_Ref_Temp는 변환 명령이 주석 처리된 채 ProcValue에 전달한다. Manuale=NOT Flag AutoBurner. CONT_C DB20의 COM_RST=false, MAN_ON=Manuale, CYCLE=T#1S, GAIN=1.35, TI=T#6M, TD/TM_LAG=T#5S, DEADB_W=2.0, LMN_HLM=MaxValue, LMN_LLM=5.0, LMN=OutValue 뒤 RND→I_Outvalue다. 숫자는 **색인에 적힌 백업 인자**, 현행 튜닝/안전 설정/권고값이 아니다. 선언0651 NID7 Write와 0653 호출은 색인의 문맥을 지지하지만 원본 실행 명령 복원·실제 실행의 증명이 아니다. 빈 PV_PER/I_ITLVAL/DISV 등 인자를 0/기본값으로 메우지 않는다.

### 3.3 버너 결과→공기 설정의 복수쓰기

0416 NID2는 OFF Contact194 앞단에서 Manuale Contact196→Move165 I_FFWD(W186/187) 또는 NOT Manuale Contact198→Add171(0+I_Outvalue,W190~192)를 DB6.DBW12에 쓴다. 0023 NID3는 ON Contact186→Add174(0+I_Outvalue,W183~185)로 같은 DB6.DBW12를 쓴다. Local I_FFWD가 이 자료에서 유효하게 계산된다고 가정하지 않는다.

0187 NID17 Flag AutoBurner ORef1180/Contact1188 W1189→Add1176.en; WorkData.Burner_PID_Result W1185 +0 W1186→W1187/ORef1183 Data.Burner_Panel_SetPoint. 0417 NID5 ON Contact273→Gt230(Panel>AIR)와 Lt239(Panel<AIR) 비교; Add233 Air+1 W262~264, Add242 Air−1 W269~271→같은 Air_Out. 개별 분기는 원본 Int 연산이며 실행횟수당 증감이지 현행 초당 변화속도 확정이 아니다. 선택한 경로 밖의 설정 Writer와 OB 간 최종 우선순위는 미완료다.

### 3.4 Control_stechio 고유 핵심

0194 NID1 ON Contact732 W733에서 20개의 Ge(Int) 비교 pre로 분기한다. 대표 0:Ge371 W611/612→W613 Move374.en, Stechio.Gas_crv0_4 ORef532/W615→W616 Local ORef533; 다음5:Ge379 W617/618→Move382 W621/622; 마지막95:Ge523→Move526→ORef609. 모두 같은 Local RID9 Portata_Presunta_GAS에 쓴다. 0591 곡선은 DB5.DBW50부터88까지 2byte 간격 Int이고 문턱은0592 Constant다. `0_4` 같은 이름은 저장 태그명이며 실제 비교는 ≥ 하나씩이다. 동시에 참인 여러 분기와 미일치 시 Local 상태를 보존하며 보간/배타적 선택/최종값을 발명하지 않는다.

`_7ev/1831 STL`는 Data.MASSICO_FLOW_AIR/GAS를 ITD→DTR, Local AIR_FLOW/GAS_FLOW, `/R`→Stechio_attuale→DB5.Real_stechio, Set_stechio→Local SetPoint_Stechio 순서를 담는다. 원형 STL 미확보이며 이 색인 범위에는 0분모 방어가 명시되지 않는다. 따라서 안전한 나눗셈이나 전체 프로그램 방어 부재를 확정하지 않는다.

0195 NID3의 대표 핀 대조:

|핀|실제 Part/Wire/ORef|선언 및 해석|
|---|---|---|
|en|Powerrail W637→LRef663.en|FC 호출 조건과 내부 LRef enable은 별도|
|COM_RST|HighFlame UID672/RID124 W721→NOT Contact657→W722|NOT DB13.X17.7|
|MAN_ON|ON673/W723→Contact658; NOT HighFlame674→Contact659→Disable766 Contact765; OFF676 Contact661; OR662→W731|ON AND ((NOT HighFlame AND M80.0) OR M0.1)|
|PVPER_ON, P/I/D_SEL|W732/733/734/737, UID677/678/679/682|OFF, ON, ON, ON 심볼. 상수 대신 현재 bit값 필요|
|CYCLE|W738 UID683/RID87|0592 Time T#100MS|
|SP_INT / PV_IN|W739/740 UID684/685|0589 Local SetPoint_Stechio/Stechio_attuale Real|
|MAN|W742 UID687/RID88|0592 Real0.0|
|GAIN/TI/TD|W743/744/745 UID688/689/690|0591 DB5 Real8,Time12,Time16|
|TM_LAG / DEADB_W|W746/747 UID691/692|0592 T#1M / Real0.1|
|LMN_HLM / LLM|W748/749 UID693/694|DB5.DBD24/20 Real|
|PV_FAC/OFF, LMN_FAC/OFF, DISV|W750~753/755|1.0,0.0,1.0,0.0,1.0 원본 상수|
|LMN|W756→UID701/RID97 Write|Local Correzione_Stechio Real|

ORef680/681/686/699/702~709는 RefId가 없다(INT_HOLD/I_ITL_ON/PV_PER/I_ITLVAL 및 LMN_PER/QLMN_HLM/QLMN_LLM/LMN_P/I/D/PV/ER). 저장 인스턴스값·미사용·0·기본값을 보충하지 않았다. 입력모드와 COM_RST를 운전자 전체 Alarm Reset으로 설명하지 않는다.

`_7ev/1833 STL`의 RND→Local Correzione_calcolata_int, Portata_Presunta_GAS +I 보정→Data.Burner_Gas_Out는 색인 및0589/0591 NID4 선언 근거다. 0196 NID5 ON600→Lt563 Gas<0→Move566 0(W591/592), Gt571 Gas>100→Move574 100(W597/598), 두 Word쓰기를 실제 XML로 확인했다. 이 소프트웨어 제한이 실제 연소 안전 범위를 의미하지 않는다.

0197 NID6 ON618 W619→Le589 Local correction≤Limite_min→Coil592 W611 UID602, Ge595 correction≥Limite_MAX→Coil598 W616 UID605. 출력 DB5.X28.0/.1은 일반 Coil이며 지연·Set/Reset 래치가 없다. 이를 새로운 버너정지 알람으로 만들지 않는다.

### 3.5 산소·압력·TC03 PID 대표 대조와 공유 소유

|네트워크·인스턴스|입력/수자동·제한 핵심|출력·미확정|
|---|---|---|
|0475 NID2 LRef109/Instance149,0665 RID20 DB22 PID_MV05|ON188→en; NOT Auto190 OR (Oxigen_Fault192 AND NOT UNDER TESTING194)→OR98 COM_RST W155. NOT Inputs.MV05 open/close196/198→HS/LS. W167/168 Local Real_SPO2/Real_O2|W182/183 UID147/148,0670 RID28/29→M13.0/.1. RO01/OFR 공급과 밸브 최종출력 별도소유|
|0476 NID4 LRef172/Instance210,0665 RID38 DB23 PID_MV-02|ON245→en, NOT Auto247→COM_RST W248; NOT 처리한계249/251. W224/225 Local Real_SPPC01/Real_PC01|W239/240 UID208/209,0670 RID43/44→M14.0/.1. PSH01→Press_PC01와 PC01 IW322를 병합하지 않음|
|0477 NID8 LRef366/Instance412 DB21 PIDMV01|ON463→en, NOT Auto465→COM_RST; Local TC03 SP/PV W442/443. 한계 Inputs 및 ON/OFF/위치100·10 분기|M12.0/.1. 상세 방향/한계/9미결속핀은 MV01 공유근거; 물리 Q 아님|
|0479 NID12 LRef507/Instance546 DB25 PID_MV03|OFF583→en; NOT Auto585 OR washing587→COM_RST; NOT 처리한계589/591; Local PC02 SP/PV W562/563|W577/578→M14.4/.5. 0344 PSH03 경로도 같은주소 Writer: PC02/MV03 초안 공유. not used 제목≠비실행 증명|

0475/0476/0477/0479는 각각 9개의 RefId 없는 ORef를 유지한다. 수동 내부핀 LMNS_ON/LMNUP/LMNDN을 정해진 값으로 채우지 않는다. 각 호출 CYCLE=T#100MS는 현재 OB 주기 증명이 아니다. 예:0476 GAIN−0.22(0667 RID39), TI2S(RID40), BREAK2S_500MS(RID41), MTR18S(RID42)는 이 경로의 인자이지 다른 밸브에 복제할 표준 튜닝이 아니다.

0478 NID9: ON375 W376 뒤 NOT MV04_Auto377, NOT Start_FN02379, ON381의 세 가지→OR358→W372 Coil362, W374 Local VT02Manuale UID367(0669). ON이 참일 때 세 번째 가지로 수동 요청이 참인 정적 접속이다. 실제 ON값·현재 실행을 확인하지 않고 항상 수동이라고 단정하지 않는다. `_7ex/13` CONT_C PID_VT02 DB30은 원형 STL 미확보, NID10 선언 및 색인 수준이다. LMN_HLM100.0/LLM35.0와 주석 50%/100%가 다르고, 출력 주석의 100..0에도 식은 0.0+OutVT02→RND다. 주석대로 역산식을 발명하지 않는다.

0480 NID16 Lt22( TC03_SETPOINT<200 ) W27/28→Move32 W33; Constant200 W34→W35 UID37 Data.TC03_SETPOINT. Move32 DisableENO=true. `_7ex/9` TC03_SETPOINT +(-15)는 주석 “−30°C”와 상충한다. `_7ex/10` +0→ITD/DTR→MV01용 Local SP/PV와 함께 TC03 초안 공유. 200이나 −15를 현재 안전 설정으로 옮기지 않는다. MV06의 PID 이름 M13.2/.3은0347 오차/타이머/비교 방식이라는 기존 조사와 분리하며 여기 CONT_S 결과로 바꾸지 않는다.

### 3.6 아날로그 출력과 ENO

0467 NID8 ON582: Air_Out<0/ >100 비교→Move523/531에 0/100; 같은 W583는 Mul536.en에도 연결된다. Mul536(Int) Air_Out×272 W574/575→W576 Local Calcolo_Aria; 별도 ON584→W585 Move543.en, W579 Local→W580 UID560 BR01_AIR_SP. 0664 RID61 Output AO2480 SAM=Peripherie, PQW310. 범위제한과 연산은 XML 접속상 병렬 가지이므로 현재 실행순서 보장으로 확대하지 않는다.

0468 NID9 ON626과628 뒤 Mul590(Int) Gas_Out×285 W622/623→W624 UID606 BR01_GAS_SP(0664 RID67 Output AO2464 SAM=Peripherie=PQW308). **W23 Mul590.eno→Move22.en**; W24 UID26은 같은 AO2464라도 RID109 SAM=None Output QW308 읽기이고 W25 UID27은0663 InterfaceAccess Local test_out이다. ENO를 일반 out 데이터선으로 설명하거나 Local test_out을 별도 물리 출력으로 만들지 않는다. Gas 제한 Move576/584는0196과 같은 DB1.DBW252에 쓰는 다른 경로다.

## 4. 전기 전달 끝점 — 대표 버너 AO만 직접 렌더

Electrical_Rev2.pdf 실제 PDF101=FG100, PDF115=FG114 두 쪽을 렌더하여 확인했다. 각각 footer DATA27.05.2024, DISEGN G.G., NORMA IEC, TOT262, 보이는 개정기입란 공란이다. 파일명 Rev2를 각 페이지 개정값으로 복제하지 않는다. PNG는 extracts/SYS-PID에 있다.

|경로|FG100/PDF101|FG114/PDF115|
|---|---|---|
|가스변조|+PAW308→GME X1:401→버너 X1/2/3, REGULATION GAS SERVOMOTOR 4–20mA|MOD8 PAW308 단자9 QV2/QI2; −100.1→단자12 MANA, 교차참조100/2·111/2|
|공기변조|+PAW310→GME X1:405→버너 X1/3/3, REGULATION AIR SERVOMOTOR 4–20mA|MOD8 PAW310 단자13 QV3/QI3; −100.2→단자16 MANA, 교차참조100/5·111/3|
|응답과유량|가스재전송+PEW360 X1:399/400, 공기+PEW362 X1:403/404; FIT2001 PEW364 X1:407/408, FIT3001 PEW366 X1:410/411|AI 모듈 FG111은 BR01 기존근거 연결, 이번 추가렌더 범위 아님|

FG114 CPU515 문자만으로 현재 CPU 모델·실슬롯을 확정하지 않는다. FG100 상단은 외부 010-390 ELECTRIC PANEL BURNER COMMAND TYPE BP N300 참조이며 외부 상세도는 미확보다. 전류 반환과 차폐100SCH1/2를 합치지 않는다. 이 AO는 릴레이 접점5/9 경로가 아니다. BR01 FG99/143 릴레이와 하단접점표1/5/9는 공유 초안의 별도 회로이며 여기 복제하지 않는다.

MV01/03/06·PSH01·TC01/02/03의 전기/시공/현장상충은 해당 초안에 연결한다. 모든 PID 관련 설비 전기페이지나 모든 I/O를 이번에 렌더·의미검토했다는 주장은 하지 않는다. 승인 준공도·외부 버너 내부순서·실물 모델·튜닝·현재 교정·정상극성은 미확인이다.

## 5. 알람·복구 경계

- PID COM_RST, HMI Alarm Reset, 내부 RESET_ALLARM, 실제 보호복구를 구분한다. 0195는 고화염 응답 반전,0475는 Auto/산소Fault/UNDER TESTING,0479는 Auto/washing의 PID 입력이다.
- 0197 제한 도달 신호는 일반 Coil이고 현재값 표시 후보다. 안전차단, 경보등, 혼, 유지·ACK로 이어지는 고유 경로는 이번에 확정하지 않았다.
- TC 선택 EmergencyStopTC1_2, TC01/02 비교·MAX/MAXMAX, TC03 온도/OFR 및 BR01 정지 소비는 각각 기존 소유 초안 공유다. SYS-ALARM의 공통 ACK/RESET/Word 비교를 PID 자체 알람으로 복제하지 않는다.
- ON/OFF 및 출력수동 비트의 이름만으로 안전모드·차단완료·재기동허가를 판정하지 않는다. 실제 복구 관찰·안전 승인·제조사 절차가 없으므로 강제값/보호값변경/자동재시작/시험 지시를 제공하지 않는다.

## 6. 증상별 관찰 설계 — 실행한 현장시험 아님

|증상|읽어 비교할 관찰점|구분·추가 필요자료|
|---|---|---|
|선택온도가 예상과 다름|TC01/02 환산값, DB39 enable/OFR/PID_Ref_Temp, SCL1719 분기|TC02-only 원문 이상을 그대로 기록; 현행 SCL/TIA 읽기자료 필요|
|버너 출력이 고정/수동처럼 보임|M15.0, Local Manuale·OutValue, DB6W12, DB1W22/W18/W252|0416/0023/0187·OB주기·다른 Writer를 함께 확인; PID게인 변경을 첫조치로 삼지 않음|
|비율 값이 비정상|DB1W212/W210, Local AIR/GAS, DB5D4/D0, OFR·원시값|0분모/환산실패/단위·유량계 자료; 임의 정상범위 판정 금지|
|비율보정이 최소/최대에 붙음|DB13X17.7,M80.0,M0.0/.1, DB5D20/24, Local correction, DB5X28.0/.1|COM_RST/MAN_ON/한계도달 분리; 경보래치나 화염검출로 오독 금지|
|자동 밸브 방향이 안 나옴|각 Auto/COM_RST/리미트/M-bit와 해당 밸브 최종출력|PC02 M14.4/.5의 복수Writer, MV02 하류NOT ON, MV06 별도방식 고려|
|DB 설정과 전기출력이 다름|DB1W18/W252,×272/×285, PQW310/308, QW308/test_out, 실제4–20mA|PIO직접접근/이미지읽기/Local분리. 현장 측정은 승인자·기기·시각·단자·안전절차 필요|

관찰기록 틀: 관찰자·시각/시간대·프로젝트/CPU 증거·값/형식/단위·수집위치·OB/Writer 문맥·비교원본·배제결과·승인조치·복구증거. 실제 운영자료·사진은 작성/복제하지 않았다.

## 7. 완료·누락·다음 단계

|영역|상태|근거/누락|
|---|---|---|
|설비·자료기준|적용·문서범위완료|한 software ID/고정원본/소유경계|
|I/O·HMI|적용·누락포함|대표 선언·CSV 대조, 실제 이벤트·권한·현재값 미확보|
|제어|적용·대표핵심정적대조|원형 SCL/STL·모든 Writer 우선순위·라이브러리 내부·현재호출 미확보|
|전기|직접단자 비해당·관련대표 적용|FG100/114 실제렌더; 타설비전기 전수검토 아님|
|알람·복구|적용·경계작성|공통소유 연결, 현장복구 미수행|
|증상관찰|적용·관찰안작성|실제 시험/정비/관찰이력 없음|
|완료기준|문서초안 complete_with_gaps|정적자체검사만, 제품통합/게시/실물완료 아님|

네 기능(도면·래더 비교, 백업·선택복원, 전후기록비교, 보고서/PDF)은 이번 코드 미수정으로 SYS-PID 구현·저장·재열기 검증을 하지 않았다. ui_records=not_run, publication=not_published, tia_compile/live_cpu/field_recovery=not_performed. 문서의 PDF **원본 렌더 검사**를 사용자 보고서 생성·화면 검증으로 대체하지 않는다.

다음 필요한 자료: 승인된 동일프로젝트 원형 SCL/STL/정식 Export와 OB32/35 실제 설정·호출/쓰기 교차참조; DB20/21/22/23/25/30/40 인스턴스 현재/초기값; HMI 원형 이벤트·단위; 버너010-390 및 현행 루프/단자/교정자료. 없는 현장자료를 재검색 반복하지 않고 이 초안의 미확정을 유지한다. 보호값·튜닝 변경은 조사 범위가 아니다.

## 자체검사·실제시각

- 최종 자체검사 시각: 2026-10-11T12:04:10.908286+00:00. 선정 69파일 SHA256와 고정 Git blob 내용 모두 일치, 원본 Git status 빈 출력. sources 전체 712파일은 보존해시만 기록했으며 의미전수검토 수가 아니다. 중지5자산은 freeze SHA와 일치, 읽기해시 외 실행/변경 없음.
- 실제 XML 파싱 18 FlgNet 및 문맥 선언; 의미검토는 본문에서 명시한 대표 가지에 한정. 자체정적검사 통과는 독립 검토/TIA/CPU/게시 완료가 아니다.
- 추출: pins-declarations.json, selected-declarations-complete.json, selected-live-index.json, wires-readable.txt, hmi-selected.json, shared-evidence-check.json, selected-source-hashes.json, self-check.json, stages.json. 단계별 시각은 실제 관측이며 추정 소요시간을 넣지 않았다.

## 선정 원본 전체 SHA256·고정 Git blob 목록

고정 저장소 상대경로다. SHA256는 현재 읽은 바이트, Git blob은 고정 커밋의 원본이며 모든 행의 바이트 비교가 true다. 중지자산은 보존해시 전용이고 논리조사/실행 대상이 아니다.

|경로|SHA256|Git blob|내용일치|
|---|---|---|---|
|`.agents/skills/gme-equipment-rollout/SKILL.md`|`fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b`|`9aa820ea6ca15b4e136c9772423b78ed4df6a3d4`|true|
|`AGENTS.md`|`0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2`|`073164bc6efd5791032d62c71b03b4dab48cb6f8`|true|
|`EXPANSION-WORK.md`|`ec624de9fd2fcfac861a67fd5e828b25ef46db50bfd7a37ff16e2cb54cd0f7e2`|`4c42d88ecc2d48269eb23e13a20ebf3721a092a1`|true|
|`PUBLICATION_STATUS.md`|`efe4857aec598d90470322cf3962eb3fe1f64947630e1fdf71d1c90134de8740`|`d76401cf291fc0be681acc51fa898ad3ce46ff78`|true|
|`VERSION.json`|`5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7`|`fffb51663b7705aec91cb119ca80ee943a4ce758`|true|
|`WORKSPACE-HANDOFF.md`|`215096d997782e78e901dfae36c782937e49611fbeb677a0d3fa50cbecf8d074`|`dd0b8989d2376c4415bba9bd826fe6754c6b1a12`|true|
|`all-in-one/ACTIVE-WORK.md`|`eff3bbc08ecff41da3beff77f3fec48e7d148708192bcaaab00f34b6a721afc2`|`6eb947c629b5ddf9c759ef87649451303938864b`|true|
|`all-in-one/assets/program-model-data.js`|`52f8199371e3399b7c0d44ab5469f0472aced79d56bbef2887f7625f5d2aff0f`|`38f34b0caa380a16ccad6f6f1e234a2fdf23f327`|true|
|`all-in-one/assets/simulator-workspace.js`|`3a6dfc618ff7e7b238f2671dc85d65704f33093a18eac879d86081d92c31e8bc`|`97c2c831c77a9699fff0e0960b3bc1b7d93d45b3`|true|
|`all-in-one/assets/virtual-plc.js`|`5f1876052dc0067b1f010af0dfc941946e37003167481731293615d9c1c36dbc`|`0bd9eceb54365a91214a37c5601b5067c39a3f75`|true|
|`all-in-one/registers/program-model.json`|`6203479c086b15bada12ac9d7e37db9280234ec26f1ea6091d7211dc09a577c5`|`9860b10f008d3a5ae714be50d77b703dfec32f3a`|true|
|`all-in-one/registers/simulator-freeze.json`|`bb93c1994effc5609939ba566b7802ce7ed55154a7310f02379b308ac2c8c835`|`808ffac14dbd1b4a7d797fa6cd0d647635d90b47`|true|
|`all-in-one/registers/virtual-plc-test-results.json`|`a6b389f797f9a8b5ffe6928b8420f55c4cc459a327b0b48d716079d2eca6dd64`|`757dd50e45184568facb8ff62900b39d3ce848d1`|true|
|`all-in-one/sources/Electrical_Rev2.pdf`|`5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6`|`f610fd7c7ce14ae951b00cff57b969259bfb389d`|true|
|`all-in-one/sources/decoded-original/0023-FlgNet.xml`|`868f9cce5f0759fac0fb4a1a23599fa166ffa29978b430c84d1b8cf03bb3d347`|`494766f2d1f6bf7035b433fb2e21f5d9ecfbc7bf`|true|
|`all-in-one/sources/decoded-original/0024-FlgNet.xml`|`a463981da8db46dd7eeb44e592d38807704886d597e728bb652dba4c12cc8f67`|`379ccbabf7692e1df137b99bab1992dea22cc1f0`|true|
|`all-in-one/sources/decoded-original/0028-FlgNet.xml`|`c369213b6556d0fcecac67ee7f12585fc0aa46845d70fedcbd461eb32b05c62a`|`333f0abc950f871ed0b3f1fce3036979a5762c84`|true|
|`all-in-one/sources/decoded-original/0055-IdentXmlPart.xml`|`9baf3104be3c8a3457c3eea021f23fbd6a60c665e81a293bd7f2cae52c64be29`|`85d87193fda164b5c7282f6e40ec5f49b3383309`|true|
|`all-in-one/sources/decoded-original/0067-IdentXmlPart.xml`|`0aa469d4f7a20bde2a5bccc6c91b3d9c48929460bd68ef32e0217d53f4d68628`|`455f00638f1618f194b1c83d9c0c2f157663a902`|true|
|`all-in-one/sources/decoded-original/0069-IdentXmlPart.xml`|`da5203cd92ccadfea2029aafb45a1e6e99443d7edbbcc2fd2f2927482564590d`|`26204ec172cabfadf54c1ad6a74013bfaae06a11`|true|
|`all-in-one/sources/decoded-original/0187-FlgNet.xml`|`0d4e4dd53c729f48c4ad275eba51d89fab582958032f9eae6f722daff808e027`|`bdd37d42a721e2e6f648f750a26951f8ffa4b2b5`|true|
|`all-in-one/sources/decoded-original/0194-FlgNet.xml`|`489de0d7673d1551b77ddf892ea74eee784ac6e5f5ea9860bd2fcaeb9b0c2851`|`f6427c5503ccb0877de69973b0dcfa4423c35395`|true|
|`all-in-one/sources/decoded-original/0195-FlgNet.xml`|`fc40707c4c248625ff2a5ec39a7451e02ee2cd9670d41e0354021027d3cc5ea7`|`92e4ff1c178e8e2c814785895ee71474c659afb3`|true|
|`all-in-one/sources/decoded-original/0196-FlgNet.xml`|`8dfab60a56115bbf67249db39505dc288e4da875314579c66f7e2f5f1702a274`|`ebecf3fa32ecdf5e6f0a0ce65fdf11a05cd65ccb`|true|
|`all-in-one/sources/decoded-original/0197-FlgNet.xml`|`61aedd67b7ec771ea30fe601d5e715c68e6fe5981060da8de7ce4719e5c66e4d`|`e87e5c7a9d4e8e5b2f2939ce2eec72d9a3397153`|true|
|`all-in-one/sources/decoded-original/0416-FlgNet.xml`|`1838d3c52dbc3319af0d7aabbb6477af9e862075b12a990412e6bd69a1d1cd0d`|`b92a1ed55be7ec175d801a9f15938ed04519475a`|true|
|`all-in-one/sources/decoded-original/0417-FlgNet.xml`|`1b9c7e4adf52f72f896b3c93753c76869a5aa0f85a9b40c9b7d168f1ef14b7f8`|`d5b28352ef3f0cfc7806b3981c8ba0139c1f1f8a`|true|
|`all-in-one/sources/decoded-original/0467-FlgNet.xml`|`126749547e09ee8f0584da5892a8c4025d85555c21bba40a4a5ad25e2a7591a8`|`05f3a3148c141002052bcdbd29478e004169863b`|true|
|`all-in-one/sources/decoded-original/0468-FlgNet.xml`|`4e29e6dd5cb60e64a7116f3f66bf51d8f476aa6cff6de3542689a50996c2015b`|`5bf7c148b94866e77f6e4791ad926dcb91038b8d`|true|
|`all-in-one/sources/decoded-original/0475-FlgNet.xml`|`ca3a5bf5bce9189b7c63dd27057b6b759e74a7793d34d2d050fe7e69951ae2b3`|`5d03d472dc65fb5dc6b0442caae0167b938bf57f`|true|
|`all-in-one/sources/decoded-original/0476-FlgNet.xml`|`0f9c48dddf61987d61094de9368ab534b56ec6c30e898dc2e4d81b64e86fa55a`|`6201c68a4d81417c8aa970bdcc7de6dea3899260`|true|
|`all-in-one/sources/decoded-original/0477-FlgNet.xml`|`e7b5b0cb95c60d1112081f6129a3127f8413e1b1d2a4c67d0e203d36ea0a711a`|`8bc2088bf4bb5eb8d51e0d9186879fc61d2c27df`|true|
|`all-in-one/sources/decoded-original/0478-FlgNet.xml`|`aa056d368ec6c7089c5accab25e7350e67a6235cd8cc766a30bb51d87e5a823a`|`1099572e537f6d44bad257ba01e7b3fecfa36381`|true|
|`all-in-one/sources/decoded-original/0479-FlgNet.xml`|`112e55599a4dc705438c8c61b936da9a167c22d9bbd909eda11c45c9dc33e839`|`38df067a2f4f62edfba9c5027002feccb45e5142`|true|
|`all-in-one/sources/decoded-original/0480-FlgNet.xml`|`c14d2fee14b38b7c597edb46626676f0cf550b5831668884cb2fac341b559273`|`d17dfbf4a5e25e09c25b13721d6a81636ad62ad9`|true|
|`all-in-one/sources/decoded-original/0582-IdentXmlPart.xml`|`41d4c2bd750392bbc2edc43995ec3a9da47a63c13ee86496df8f187492008951`|`82636dec064876d0f4cc714ef385b07d6e05efe0`|true|
|`all-in-one/sources/decoded-original/0585-IdentXmlPart.xml`|`e36ec18aa4abebea8f9160254522bb51ff722eae804c5a469790f85f02939184`|`16574d37ef3ca61b59ba396c400e269ab1dd3440`|true|
|`all-in-one/sources/decoded-original/0586-IdentXmlPart.xml`|`f16c4c68bde8a737372c219a10b21501653dfd3ba8c59bd84b60ae6d62da8250`|`266989c590cf52f82e1553f8626a209b8c0b6e0b`|true|
|`all-in-one/sources/decoded-original/0587-IdentXmlPart.xml`|`bab957ac7c180d9c91b4f904b29e9dbd5812c6ba8f7b9e0c7faf9708605b203e`|`67e84e4b8d43b7c5864ec40fcc2c9fbc2222b436`|true|
|`all-in-one/sources/decoded-original/0588-IdentXmlPart.xml`|`def5646a0d1eacaae81518f0952c4ba8ada5ea38852463a1d463ff439f3d1905`|`07d012cdc3fb0662f8126f4c274a36288e3bfc9b`|true|
|`all-in-one/sources/decoded-original/0589-IdentXmlPart.xml`|`846630f3832df93ccdcb0bf86a029546886f8cdba51cd952eed63257ee4540e2`|`5de11972e1fb84f02e4585a53fab478d54e203d0`|true|
|`all-in-one/sources/decoded-original/0590-IdentXmlPart.xml`|`baff7271b3db646e8953c31d20b72f7b044b1154b689b15ca0fb38ebb44ad81c`|`5816a1fc640da97d27ec68c8c45f255a0bd60730`|true|
|`all-in-one/sources/decoded-original/0591-IdentXmlPart.xml`|`2e165c44fc9df852ea3729b3ddb33dc0a74e4f8826676f9c5c5626e1dce033f8`|`407456d55041d82dd19e551f904a217a11478289`|true|
|`all-in-one/sources/decoded-original/0592-IdentXmlPart.xml`|`d157e3d92df9e4a6ce46567b8611a51b0a10abf4dd7f9c4e613087b2df9583a8`|`09bbf459f42d75a973dad70dcfa6871c668b0851`|true|
|`all-in-one/sources/decoded-original/0593-IdentXmlPart.xml`|`504568b5b50bb25a6880e9da724f79438fbb07e7a311a9391681143d713499e9`|`f2447d339be5de33caf49e1dd56d970eecfd23a2`|true|
|`all-in-one/sources/decoded-original/0647-IdentXmlPart.xml`|`ffa253c00b62ccdd999f272d95f613caae3a68792ee5ea9d208253dad53e64be`|`d2cf63bd5fe432b0085690496566c9dbcc989352`|true|
|`all-in-one/sources/decoded-original/0648-IdentXmlPart.xml`|`afaa47ae737d9333fe831ffac2b1d1388f108bb6a2b23d03554fa862f7edb454`|`3dd5101419fbe16bbce7814398209efd6508db82`|true|
|`all-in-one/sources/decoded-original/0649-IdentXmlPart.xml`|`38f59e654ecfbc2066fa1f8beeb9ced952adc405f8a4fcf3ef233e9d5d026576`|`039bf2e14a610674a8c01d807805d2db9b4a4956`|true|
|`all-in-one/sources/decoded-original/0650-IdentXmlPart.xml`|`86f53657eb7afb0798da0e215ba226721076c2ab1b25b74eb83e7b3c4b2d8a2d`|`a3d80a76ef5b0d00009c0fc9a1fdeb1471d0b67b`|true|
|`all-in-one/sources/decoded-original/0651-IdentXmlPart.xml`|`549c09fb14ce6e9734a2ba604c78868647451f24d224ead0d17d209f66428111`|`08d5828b2ed490605da88f6fbb695db5427b6972`|true|
|`all-in-one/sources/decoded-original/0652-IdentXmlPart.xml`|`251bb1b3ce1bdf3686545062e5803152779de8a4961539d30e6951a2a10ab692`|`eee49f8301a6791748de9ab368159af8e8bc1585`|true|
|`all-in-one/sources/decoded-original/0653-IdentXmlPart.xml`|`2df91e2095f16613332cfc59d4c51f8a587183e5e75295a119431b61805c92a6`|`4f93c87d6f199d9f8ad16db16fd4df2192ee6d19`|true|
|`all-in-one/sources/decoded-original/0661-IdentXmlPart.xml`|`90672199fee355011f581d3287046894772f3f3b4cb78bbe0dd0d71bd488ac93`|`cea3653088f8fb5c77afcf715988039cb63e28ac`|true|
|`all-in-one/sources/decoded-original/0662-IdentXmlPart.xml`|`1838040bfee800fdb3f13b126eaf69a9d178b17cecc0d59ae03e9185216a48a5`|`ba624f3460dc05e8ade4956cdfc2ec621edb4f73`|true|
|`all-in-one/sources/decoded-original/0663-IdentXmlPart.xml`|`d3980b88d3cd3e49854439d0778c58ed131bae46a6bc3e65ab70e81f766ac03d`|`3051de9b670457991223a08c03f785747e687414`|true|
|`all-in-one/sources/decoded-original/0664-IdentXmlPart.xml`|`68c614e1c6a7fcadeee3f0b2ddc54910c3b337e66074d7a113b9cbc834c271ed`|`7ce2f1315d5a21d6b77869a59fc9fcb2f17e90e6`|true|
|`all-in-one/sources/decoded-original/0665-IdentXmlPart.xml`|`50e88d5f50f555151b35cfb17225e766c34ef6b490bd3a48e0a4e335fd17e3dd`|`ea4a8a5013081f648722c5ebbde3bb1366787990`|true|
|`all-in-one/sources/decoded-original/0666-IdentXmlPart.xml`|`19a9ccb83ad7070d23726250870d0ca0c33d797ab9ffe679c9d2c0d109cc95e6`|`b6130b32498b6fee0d9e4db7a04dc79f785e1fbb`|true|
|`all-in-one/sources/decoded-original/0667-IdentXmlPart.xml`|`ef924ced3e0e2b17e9c8440eb4946cd50d55df644c6ec24a1c4fd288fa6b73a3`|`7f2e1798eb9f260d19d038a83369484d0f438856`|true|
|`all-in-one/sources/decoded-original/0668-IdentXmlPart.xml`|`2248e994a0a02cd37c5c5edaca199b3421068feea91e2e8616560e814ef9f6ed`|`fe0f30d1eaae37783b0f03cb090353b3a3de3600`|true|
|`all-in-one/sources/decoded-original/0669-IdentXmlPart.xml`|`754c513339d00918717010047b8f9d865d8674c6978a6f86c6f1fa5d683506e2`|`f5bf8f3c41d2a07ba9dcfd8f400548be8cf51cd3`|true|
|`all-in-one/sources/decoded-original/0670-IdentXmlPart.xml`|`e56f3f0c4f2a86dd18578dedd4453915c2a51cd25e2cd9feced8538171a00841`|`b9466007b14e5c4f5d353dca5734401317e2dc03`|true|
|`all-in-one/sources/decoded-original/0671-IdentXmlPart.xml`|`26cb51706305c372d512c19770648bb0dbb74df8bd2277b1e0da1b8c88cca293`|`e38a4e2c93ac8093e2b0b8e082a64688b5d9845e`|true|
|`all-in-one/sources/decoded-original/network-map.json`|`c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60`|`424430b6b953e43138e5d0a18ca40c949e21cfa1`|true|
|`all-in-one/sources/hmi_plc_tags.csv`|`a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404`|`cf4c0650e7c7baac350dcb89909b808435704880`|true|
|`all-in-one/sources/live_index.json`|`14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1`|`e35ccea1f841349c632666c29954b7bcd4f5839e`|true|
|`docs/equipment-standard/INVENTORY.json`|`720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc`|`587c3748ad9224718f95ba06463fee913dae231d`|true|
|`docs/equipment-standard/WORK-ITEM-TEMPLATE.md`|`4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586`|`e546f39535d2b589e80f97db869ac37ce4d05cfd`|true|
|`docs/equipment-standard/WORK-STANDARD.md`|`05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99`|`f76a570cc73098632e08759b17934000f7e3a253`|true|

최종 재대조 2026-10-11T12:04:47.983209+00:00: 0194 Ge20개·Move526, 0195 NOT657/659·미결속12개, CONT_S별 미결속9개, 0468 ENO W23, 0023 ORef179 RefId35를 명시 단언으로 확인했다. 파생색인 이름 누락을 원본핀 미결속으로 오독한 초안 문장을 전달 전에 정정했다.
