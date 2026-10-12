# PV06 질소 주입 밸브 — 원본 조사 7영역 초안

## 핵심 확인·상충·누락

- PV06는 고유 catalog ID 한 개다. PV05와 `nitrogen` 별칭·Q6.4 공통 요청을 공유해도 같은 실물이나 개별 출력 두 개로 합치지 않는다. P&ID와 FG96 모두 PV-05/PV-06을 별도로 그린다.
- **고유 PV06 부하:** Electrical_Rev2 실제 PDF97/FG96의 96.12 → 외부 96KT1 접점18–15 → 96.13 → X2:15의 5×20 2A F 퓨즈 → 96.15 → PV-06 A1/A2 → X2:16 → 96.8. PV05는 X2:13/14 별도 가지이며 본 초안 완료에 포함하지 않는다.
- **공통 요청:** `%Q6.4`/도면 `A6.4` → 96KA3 코일. 실제 부하의 96KA3 접점은 **5–9**이며 하단 접점표1/5/9와 구분한다. 96KA3와 외부96KA1 경로가 공통96.12를 공급한다. PLC출력만으로 PV06 개방·유량을 보증하지 않는다.
- **준비와 알람:** `%I16.7`/E16.7은 탱크 준비다. PV06 개방 피드백이 아니다. `Inputs.NITROGEN TANK READY`와 `Allarm.HYDROGEN_BOX_FAULT`의 NITROGEN/HYDROGEN 명칭 불일치를 보존한다.
- **쓰기 주의:** 0397의 IW16→DB13.DBW16 Word 복사와 별도로 0415의 `simulation` 원본 네트워크에는 준비 Bool 쓰기가 있다. 읽기 전용 확인만 했고 작성·수정·생성·실행·행동시험은 하지 않았다. 현재 호출/순서가 확인되지 않아 DB13.DBX16.7을 실제 탱크 상태와 무조건 동일시하지 않는다.
- **타이머 구분:** 0538 준비경보는 S/R 논리이며 지연 타이머가 없다. 외부96KT1은 PV06 밸브 부하의 시간지연 장치다. 설정시간·현행기종·정상위치·재시도시간을 임의 부여하지 않는다.
- 공통 재사용: [RO01 초안](RO01-DOTS-DRAFT.md), [RO02 초안](RO02-DOTS-DRAFT.md), [BR01 초안](BR01-DOTS-DRAFT.md)의 산소/버너 관련 소유 경계와 공통 해석을 연결 참조했다. 이번에는 PV06 고유 접점·단자·PDF/footer, 준비 쓰기, 경보 S/R, 출력 선언을 원본으로 독립 재확인했다. RO01/02 산소값이 Q6.4를 직접 생성한다는 Writer는 확보하지 못했다.

## 1. 설비·자료 기준

| 항목 | 이번 조사 결과 / 경계 |
|---|---|
| 대상 | PV06, 질소 주입 밸브, nitrogen, 공압 밸브, phase2, parent 없음, priority 없음. INVENTORY catalog[28], equipment[32]. |
| 작업 범위 | 자체 문서조사 초안만. 신규 Work/Codex·재위임·사용자 컴퓨터/TIA 접근 없음. 로컬 2차133 통합 제외 유지. |
| 고정 기준 | `gme-research/source-mv06`, `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, v1.12.0. 현행 게시본이나 현재 CPU를 검증했다는 뜻이 아니다. |
| 보호 | 원본·공통 코드·버전·공개대장·배포·운영기록·SEJIN 변경 없음. 금지 원본 생성기/build/test 실행 없음. |
| 실제 모델 | 모델/추론 수준 런타임 증명 미확인. 문서의 요청 모델을 실제 실행 증명으로 쓰지 않는다. |
| P&ID | `all-in-one/sources/PID_1684n002I.pdf` 실제 PDF1, 도면1684n002, Apex I. footer 원일자06/04/2011, 개정I15/01/2013(REMOVED MC-05, CHANGED POWER OF FN-02). PV05/PV06 각각110 V60 Hz, N₂ FOR EMERGENCY ONLY. 실제 설치/배관 목적지 현장검증은 별도. |
| 전기도면 | `all-in-one/sources/Electrical_Rev2.pdf` 실제 PDF97/FG96, PDF133/FG132, PDF143/FG142 직접 렌더. 아래 각 footer를 따로 구분한다. |
| 소유 구분 | PV06 코일/퓨즈/타이머 접점 가지는 고유. 탱크준비·96KA1/KA2/KA3·96KT1 코일/공급·공통주입출력은 계통 공유. BR01/FN01/RD01 관련 영향은 해당 소비자 소유. |

자료에서 확보한 설계 표시와 현행 보호설정·현장 안전범위는 다른 것이다. 이 초안은 질소 주입 방법이나 안전 인터록 우회 절차가 아니다.

## 2. I/O·HMI

이하 `D/`는 고정 원본의 `all-in-one/sources/decoded-original/`을 뜻한다. XML NID는 해당 Ident 문맥과 원본 Wire를 묶어 확인했으며 UID만으로 다른 블록을 결속하지 않는다.

| 신호 | 원본 선언·주소·형식 | 해석·누락 |
|---|---|---|
| Start Nitrogen | D/0555-IdentXmlPart.xml RID53, C NID−2147483648 UID126 AK=Monitor; D/0557 RID28 UID146 Monitor; D/0558 RID36 UID53 Monitor. 모두 SimpleAccess, S=Global, Bool, SSD AO52, SAD R=Output. | AO52bit→Q6.4. 0555/0558 SAM=None, 0557 SAM=Peripherie로 접근 형식을 구분. Monitor는 명령을 생성하는 Writer가 아니다. |
| 출력 인덱스 | live_index `_7ev`1059 Name=start nitrogen, Address=%q6.4, bool, Comment=`a 60.5 automatic immissionmotor command`. | 주소Q6.4와 옛 Comment a60.5가 다르다. 실제 도면A6.4와 주소는 일치하지만 옛 설명을 현주소로 대체하지 않는다. |
| 탱크 준비 원시 입력 | live_index `_7ev`1074 `%i16.7`, Bool, nitrogen tank ready, Comment=`e 45.7 nitrogen tankready`. FG132 E16.7. | 옛 e45.7 설명 불일치 유지. 도면/백업 원시 주소는16.7. 별도 PV06 개방/닫힘 센서 선언은 확보하지 못했다. |
| 처리 준비 | D/0684 GlobalAccess RID138, AO135, AOS Inputs BO0→NITROGEN TANK READY BO135/BS1; NID12 UID937·941. DB13 선언 D/0628 RID4 TOD N13. | DB13.DBX16.7 Bool. 입력Word복사와 별도Bool 쓰기가 겹칠 수 있다. |
| 준비경보 | D/0684 GlobalAccess RID102, Allarm.HYDROGEN_BOX_FAULT AO57/BS1. C NID12 UID938 Write/OID7, UID940 read/OID1, UID942 Write/OID8. D/0682 RID10 TOD N3. | DB3.DBX7.1, Set/Reset 기억비트. HMI 이름은 아래 태그와 연결되지만 PV06 고유 알람으로 바꾸지 않는다. |
| 서비스 조건 | D/0686 SimpleAccess RID161, ServiceBit, Memory AO8000, Bool; NID12 UID28·36. | M1000.0. 현행 값·운영 정책 미확인. 강제 변경 금지. |
| 공통 리셋 | D/0684 RID24 Flag.RESET_ALLARM AO48/BS1; NID12 UID939. D/0682 RID15 TOD N2. | DB2.DBX6.0. 이 요청비트만으로 현장 복구·자동 재시작을 증명하지 않는다. |
| ON 조건 | D/0686의 ON Global 선언과 0538 RID1/UID936 결속; Memory AO0. | M0.0. 이름ON을 항상 참으로 가정하지 않는다. |
| HMI 경보 태그 | `all-in-one/sources/hmi_plc_tags.csv` 행515: Allarmi_58, `DB3,X7.1`, AccessName PLC, ID00153. | dde.cfg 설정 경로. 실제 화면 객체·이벤트/번역문·승인 동작은 미확인. 질소 밸브 개방 HMI 버튼/직접쓰기 경로는 미확보. |

### 2.1 입력 Word 전달 원본

- D/0397-FlgNet.xml, hmi inputs, live_index 문서1070, NID1. Part62 Move, DisableENO=true.
- D/0627 RID23 `Tag_275`, Global Word, Input AO128, SAM=None, C NID1 UID67 → `%IW16`.
- Wire76: ORef67/RID23 → Part62.in. Wire77: Part62.out1 → ORef68/RID24.
- D/0629 RID24, Global Word, AO128, BAD BIRID4, C NID1 UID68 AK=Write; D/0628 RID4 Inputs TOD DB13 → DB13.DBW16.
- Wire74는 앞 Part61.eno→Part62.en을 연결한다. Word 복사와 Bool 개별쓰기·실제 외부 입력을 분리하고 DisableENO 표시만으로 항상 실행한다고 하지 않는다. 0398은 아날로그 전달 네트워크로 이 디지털 준비 복사의 근거가 아니다.

### 2.2 출력 미러 방향

- D/0401-FlgNet.xml, hmi output, 문서356/NID1. Part25 Move, DisableENO=true.
- D/0632 RID32 Tag_283, Global Word, Output AO48, SAM=None, C UID39 → QW6 읽기.
- Wire64 ORef39→Part25.in; Wire66 Part25.out1→ORef40/RID52. D/0633 RID52 Word AO48, BAD BIRID26, C UID40 Write; D/0064 RID26 Output TOD DB14 → DB14.DBW6 쓰기.
- Wire21 rail→Part25.en, Wire65 Part25.eno→Part26.en. 따라서 Q6.4 상태는 DB14.DBX6.4에 포함되는 미러 범위이며 **DB14→Q6.4 출력 생성 명령이 아니다**. 전용 HMI 태그/화면 결속은 확인하지 못했다.

## 3. 제어 구조

### 3.1 계통 요청과 PV06 실제 전달

1. GME의 공통 요청 후보는 Start Nitrogen Q6.4이다. 이름/Monitor 선언만으로 발생 원인을 확정할 수 없다.
2. FG142 A6.4→FG96 96KA3 코일 A1, A2→−0Vdc10.6. PLC24V 제어와 PV06의110V 부하전원을 분리한다.
3. 96KA3 부하5–9가 X2:11/X1:368에서 X1:369/X2:12로 공급을 연결하는 가지다. 96KA1 병렬 가지와 만나 공통96.12가 된다.
4. 96KT1 코일은96.12에서 구동되며 PV06 가지는96KT1 18–15 접점을 거친다. 제목 TIME DELAY START NITROGEN VALVE는 외부 시간지연 경로를 뒷받침하지만 설정초·현행 동작형식·실제 배선검증은 없다.
5. 탱크준비96KA2→I16.7은 공급준비 관련 피드백이며 코일작동/밸브위치/실제질소유량의 증거가 아니다.

PV05와 같은 Start Nitrogen이라고 같은 실물로 확정하지 않는다. P&ID의 두 질소관 및110V60Hz 표기는 설계 도면 사실이며 유량/개방시점 실측이 아니다.

### 3.2 준비 신호 복수 쓰기와 실행 경계

D/0415-FlgNet.xml은 원본 제목 `simulation`, 문서1080/NID18이다. D/0636 RID347 ON(M0.0) ORef24→Part23 Contact. Wire29 Part23.out이 Part39.in 등을 공급하고 Wire38은 ORef40/RID352→Part39.operand다. D/0635 GlobalAccess RID352, Inputs.NITROGEN TANK READY AO135/BS1, C NID18 UID40 OID9 AK=Write이므로 일반 Coil Bool 쓰기다. Local 변수가 아니다.

이 원본의 존재만 읽었다. 해당 블록의 현재 호출·활성상태·스캔 순서는 미확인이다. 그 결과 0397 입력Word복사와 최종값이 어느 순서로 결정되는지는 보류한다. 금지된 시뮬레이터/PLC 시험은 수행하지 않았다.

### 3.3 공통 알람 소비자와 소유

- BR01: D/0175 문서1858/NID5의 HYDROGEN_BOX_FAULT ORef248/RID43(D/0585)이 버너 정지 OR에 들어가 Flag.Start_Burner Reset로 이어진다. [BR01](BR01-DOTS-DRAFT.md)의 전체 허가/상태/정지 분석을 연결 재사용한다. UID249는 다른 Ident 문맥과 충돌할 수 있어 이름만으로 DB39 Data를 결속하지 않는다.
- RD01 투입 억제: D/0238 문서1931/NID2, ORef74/RID13(D/0604)→Wire85 Part105.operand, Part105.out→Wire106 Part56.in6, Part56.out→Wire88 Part66.in, Wire90 ORef77/RID16→Part66.operand. D/0605 RID16 **Local** Disable_Load_RD01 일반 Coil. 질소경보 가지가 투입억제에 참여하지만 이 Local을 PV06 출력으로 바꾸지 않는다.
- FN01: D/0253 문서1951/NID22, ORef695/RID13(D/0604)→Wire706 Part722.operand; Wire723→Part724(UNDER TESTING, Negated operand), Wire725→Part676 OR.in5, Wire709→Part685 RCoil, Wire711 ORef697/RID117 Flag.M_FN_01. 즉 질소경보 AND NOT UNDER TESTING 가지가 FN01 요청 Reset에 참여한다. UNDER TESTING은 D/0602 RID4 Memory AO45=M5.5이며 현재상태 미확인. 같은 네트워크 별도 Part726→Coil689는 Start FN01을 작성한다. FN01 고유설비 완료나 PV06 직접출력으로 집계하지 않는다.
- RO01/02: 산소 측정/비교와 버너·투입 영향은 이전 조사와 연결한다. 확보한 선언·FlgNet 범위에서 산소조건→Start Nitrogen의 직접Writer를 확인하지 못했다. 비상질소가 산소경보만으로 자동 주입된다고 보장하지 않는다.

## 4. 전기 전달 경로

실제 렌더 산출물은 `../extracts/PV06/FG96-PDF97.png`, `FG132-PDF133.png`, `FG142-mediabox.png`, `PID-landscape.png`, `PID-footer.png`, `PID-valves.png`에 있다. PDF page는 1-based이다. FG=PDF−1이라고 일반화하지 않고 해당 쪽을 확인했다.

| 페이지/footer | 읽은 표시 | 경계 |
|---|---|---|
| Electrical 실제PDF97 / FG96 | NITROGEN VALVES BOX PV-05/PV-06, DATA27.05.2024, DISEGN G.G., NORMA IEC, TOT262. 별도 개정번호/개정표 기재를 확인하지 못함. | 파일명Rev2를 이 페이지의 별도 Rev2 기재로 바꾸지 않는다. |
| 실제PDF133 / FG132 | DIGITAL INPUT MODULE, DATA27.05.2024/G.G./IEC/TOT262, 별도 개정란 **2 / 17.03.2025**. | E16.7, CPU515/MOD12, 단자8, NITROGEN TANK READY, 역참조96/8. |
| 실제PDF143 / FG142 | DIGITAL OUTPUT MODULE, DATA27.05.2024/G.G./IEC/TOT262. 별도 개정번호 기재를 확인하지 못함. | A6.4, CPU515/MOD15, 단자25, AUTOMATIC IMMISSION MOTOR COMMAND NITROGEN START, 역참조96/9. |

### 4.1 고유 부하·공통전원 양 끝점

- 고객전원 X2:1/2 `POWER CLIENT SUPPLY220V60Hz` → 96QF1(도면0.22–0.32A) → 96T1(220V/110V63VA) → 96QF2(도면1A) →96.9/96.8. 색상/선종 표시 BLACK/RED FS17 1.5mmq가 해당 전원 부분에 있다. 이 값을 현행설정이나 PV06 외부 케이블 전체 규격으로 확대하지 않는다.
- 공통96.12→96KT1 접점 **18–15**→96.13→X2:15 퓨즈5×20 2A F→96.15→PV-06 코일A1; A2→X2:16→96.8. 96KT1 접점16은 도면 전환접점의 다른 단자이며 PV06 직렬 가지와 동일시하지 않는다.
- PV05는96.12→X2:13 퓨즈→96.14→PV-05→X2:14→96.8로 다르다. 비교 목적만, PV05 문서 완료를 상속하지 않는다.
- 96KT1 코일 A1은96.12, A2는96.8. 전기타이머와 PLC의T주소가 같다는 근거가 없다. 개별 밸브 위치스위치나 개폐피드백은 FG96에서 확인하지 못했다.

### 4.2 공통 요청 양 끝점

FG142 A6.4 단자25↔FG96 A6.4(142/1)→96KA3 A1; A2→−0Vdc10.6. FG142 출력모듈의 공급은 +24Vdc10.9→X21:3034(5×20 4A F)→142.1 및29/30 표시와 공통−0Vdc10.6이다. 이 공급보호는 PV06의X2:15 2A F와 별개다.

FG96의 자동요청 부하: 공통110V 상단→X2:11→X1:368→96KA3 **5–9**→X1:369→X2:12→96.12. 코일A1/A2와 부하5/9, 하단접점표1/5/9를 구분한다. 확대원본에서 96KA1·96KA2·96KA3 모두 외부 공급선은 오른쪽 단자5, 하류선은9에 연결된다. 왼쪽1은 비배선 전환가지이며 심벌의 비여자 접촉모양을 외부 부하배선1–9로 오독하지 않는다. 96KA1도 공통 공급에 연결되어 있으므로 PLC요청만이 유일한 주입경로라고 단정하지 않는다.

### 4.3 준비 입력·외부 버튼

- +24Vdc10.7→X1:370→X2:17→96KA2 접점5–9→X2:18→X1:371→E16.7(132/7)→FG132 단자8/CPU515 MOD12.
- 탱크준비 회로 상단공통→X2:9/10 외부연결→96.11→96KA2 A1/A2→96.8. X2:9/10 외부 접점/탱크의 구체적 생성조건·정상극성·현장내부회로는 미확인.
- 비상버튼 6SB1/2/3은 각각X2:3/6·4/7·5/8 및 X1:358/359·362/363·366/367, 접점21/22, 공통96.10→96KA1 코일에 연결된다. 도면의 병렬 접점구성을 그대로 보존한다. 버튼 실제조작·우회·현행복구순서 시험은 하지 않았다.
- 전체 외부 케이블 식별/심선색·현행 단자마킹·밸브 제조사/모델·가스측 배관 말단은 추가 승인도/현장자료가 필요하다.

## 5. 알람·복구

### 5.1 HYDROGEN_BOX_FAULT S/R를 원본 핀으로 확인

D/0538-FlgNet.xml, `allarms3`, 문서1990/NID12:

| 기능 | 핀/전선 근거 | 식 |
|---|---|---|
| Set | Wire963 rail→Part953.in; Wire943 ORef936(ON)→953.operand; Wire954 953.out→955.in; Wire944 ORef937(ready)→955.operand, **Negated**; Wire25→Part27.in; Wire26 ORef28(ServiceBit)→27.operand; Wire29→SCoil929.in; Wire946 ORef938(fault)→929.operand. | ON AND NOT ready AND ServiceBit → fault Set |
| Reset | 공통953.out→Part957.in; Wire947 ORef939(RESET_ALLARM)→957.operand; Wire958→959.in; Wire948 ORef940(fault)→959.operand; Wire30→Part961.in/964.in; Wire949 ORef941(ready)→961.operand; Wire35 ORef36(ServiceBit)→964.operand, **Negated**; Wire962→OR31.in1, Wire34→OR31.in2, Wire33→RCoil935.in; Wire951 ORef942(fault)→935.operand. | ON AND RESET_ALLARM AND fault AND (ready OR NOT ServiceBit) → fault Reset |

Part953/955/27/957/959/961/964 Contact, Part31 OR, Part929 SCoil, Part935 RCoil. 타이머/환산/아날로그 비교는 이 네트워크에 없다. Reset코일은 오류기억을 지우는 조건이지 실제 탱크준비 회복·PV06작동확인·재기동명령이 아니다.

### 5.2 표시·영향·복구 미확정

DB3.DBX7.1→HMI Allarmi_58 설정주소는 확인했다. 경보 문구는 백업 인터페이스 Comment `hydrogen box not ready`와 네트워크 제목을 근거로 하며 실제 HMI 현재화면 표시검증은 안 했다. BR01 요청Reset/RD01투입억제/FN01 요청Reset 참여는 관련 소유다. 다른 장치의 타이머·지연을 이 경보에 가져오지 않는다.

96KT1의 현재 지연, 타이머 재기동 방식, 전원상실시 동작, 밸브 고장안전상태, 승인된 현장복구절차, 공통리셋 실제 HMI 이벤트, 현재ServiceBit/UNDER TESTING 상태가 미확인이다. 설정 변경·강제비트·접점점퍼·질소방출 시험은 승인 범위가 아니며 수행하지 않았다.

## 6. 증상 관찰 틀

아래는 허용된 기록/문서 비교 위치다. 활선 측정이나 설비 조작을 지시하는 절차가 아니다. 관찰자·시각/시간대·현장위치·프로젝트버전·수집장치·값/단위·비교근거·배제결과·승인조치·복구증거를 함께 남기며 이번 실제 관찰값은 없다.

| 증상 | 비교할 독립 관찰 | 원인/완료를 성급히 단정하지 않는 기준 |
|---|---|---|
| 준비경보 지속 | 승인된 기존 관찰의 탱크준비 접점/96KA2, I16.7, DB13.DBX16.7, DB3.DBX7.1, ServiceBit, 리셋요청의 같은시각값 | raw와DB 차이는0397 Word/0415 Bool 쓰기·호출순서 구분. 준비경보를 PV06코일 단선으로 단정하지 않음. |
| Q6.4 요청은 보이나 PV06 미응답 | 출력미러와Q6.4,96KA3,96.12,96KT1,고유X2:15/16,실제 위치/유량 기록 | Q6.4/DB14 미러는 개방증명 아님. 외부타이머/공급/퓨즈/코일/가스측을 별도 증거로 구분. |
| PV05와PV06 응답시점 다름 | 각 코일·단자·시간,96KT1 명판/기존설정기록, 공통96.12 | PV06만 지연접점 가지다. 승인된 기대지연/현행회로 없이 고장 또는 정상 판정하지 않음. |
| 리셋했는데 재발 | ready·ServiceBit·ON·Reset·fault와발생시각 | Set/Reset식과 비교. 임의 리셋반복/ServiceBit변경으로 복구처리하지 않음. |
| 버너/투입/FN01 정지와 동시 경보 | 해당 요청비트·다른경보·UNDER TESTING·발생순서 기록 | 공통경보 소비가 원인 후보지만 PV06 출력/질소주입이 직접원인이라고 단정하지 않음. |

## 7. 완료·누락·검증

| 영역 | 상태 | 근거/누락 |
|---|---|---|
| 설비·자료 | 적용, 초안완료/누락유지 | 독립 PV06, 고정자료와 현행 분리. 실물동일성 확인은 보류. |
| I/O·HMI | 적용, 근거확인 | 원시/DB/미러/경보 태그 구분. 전용조작 이벤트·현재화면 미확인. |
| 제어 | 적용, 부분확인 | 준비/경보/관련소유 확인. Q6.4 실제 Writer·현재호출순서 미확정. |
| 전기 | 적용, 문서확인 | PV06 고유부하·공통요청·준비 양끝점/PDF4쪽. 현행배선·명판·단자·보호설정 미확인. |
| 알람·복구 | 적용, 문서확인 | PLC S/R 무타이머와 외부96KT1 구분. 현장복구 미확인. |
| 증상 | 관찰틀 작성 | 실제 관찰·조치·복구 기록0. |
| 완료 기준 | complete_with_gaps 초안 | 아래 상태를 독립 유지. |

- documentation: draft_complete_with_gaps. static_review: 고유XML/선언/핀/실제PDF 정적 대조 수행; 독립 검토자 검토는 부모 단계.
- ui_records: not_run. 도면·래더 나란히 보기, 통합백업/선택복원, 전후비교, 관찰보고서/PDF의 PV06 구현·저장·재읽기·재열기 검증은 하지 않았다. 원본PDF 렌더는 이 UI 기능검증과 다르다.
- publication: not_published_by_this_task. TIA_compile/live_cpu/field_recovery: not_performed.
- 작업의 원본56파일 SHA256와 고정 Git blob 바이트동일성 확인. 금지5자산 freeze 해시 일치. 원본Git status clean. 해시검증 대상수는 의미검토 완료수/전체 원본90개 검토수와 다르다. 본 조사 고유 핵심은 위에 적힌 네트워크/핀/페이지이며 전체 XML/원본90 파일 의미검토 완료라고 주장하지 않는다.
- 검증코드/결과: `../extracts/PV06/review_and_hash.py`, `assertion-check.json`, `source-hashes.json`. 자체XML파싱·해시비교·PDF렌더만 수행. 원본 프로그램 생성기/build/test 실행0.

### 필요한 다음 자료와 판정

1. 현재 승인도/단자대표·PV06/96KT1 명판 및 허가된 기존 설정기록: 고유전원·퓨즈·타이머접점·밸브 실제 위치/고장안전상태를 확인한다. 새 자료 없이 반복 보류조사하지 않는다.
2. 현행 프로젝트의 Q6.4 직접쓰기와 현재 블록호출/스캔순서 자료: Word복사와0415 쓰기의실제 활성/우선순위, 자동주입 요청 발생식을 확인한다. 현재 TIA접근추가권한 없음.
3. 탱크준비 외부원리·I16.7 정상극성·HMI 리셋/주입조작 이벤트·승인복구 절차를 확보한다. 값 추정으로 채우지 않는다.
4. 사용자 관찰/현장복구는 별도 비공개 운영기록으로 남긴다. 본 초안이나 공개Git으로 운영자료를 복제하지 않는다.

### 실제 작업 단계 시각 (UTC)

| 시각 | 실제 수행 단계 |
|---|---|
| 2026-10-11 11:24:53 | PV06 한 개 배정 수신, 공통/범위 지시 읽기 시작 |
| 11:25:15 | 고정HEAD/clean·시작자료·이전 RO01/02 공통경계 확인 |
| 11:25:38 | 질소 선언 추출과 FG96/PDF97 렌더 생성 완료 |
| 11:26:25 | PV06 고유접점/무PLC타이머 중간결과 부모보고 |
| 11:26:51 | FG132/FG142 렌더 및 입력/출력Word 핀 대조 |
| 11:28:24 | P&ID PV05/PV06 및 footer I 개정확대 렌더 확인 |
| 11:28:39 | 준비 Word/Bool 복수쓰기 경계 부모보고 |
| 11:29:04.543222 | 원본56파일 고정Git바이트 일치·중지5해시·clean 검증 |
| 11:32:47 | 부모 접점확대와 원본을 대조, KA1/KA2/KA3 외부선5–9 확인 |
| 11:32:57 | 최종선언 재대조에서 ON 파일명을0686으로 바로잡음 |

## 부록 A. 선정 원본 전체 SHA256 / Git blob 목록

아래 경로는 `gme-research/source-mv06/` 상대경로다. 각 행은 고정커밋의 blob 내용과 디스크 파일을 바이트 비교하여 일치했다. SHA256과 Git blob OID는 서로 다른 해시 형식이다. 역할이 문서/인덱스/원본/보존자산인 파일을 한 목록으로 기록하되 인덱스나 보존용 파일을 모두 의미검토했다고 세지 않는다. 원본/중지자산은 읽기·해시만 수행했다.

| 원본 상대경로 | SHA256 | 고정 Git blob |
|---|---|---|
| `.agents/skills/gme-equipment-rollout/SKILL.md` | `fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b` | `9aa820ea6ca15b4e136c9772423b78ed4df6a3d4` |
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
| `all-in-one/sources/Electrical_Rev2.pdf` | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` | `f610fd7c7ce14ae951b00cff57b969259bfb389d` |
| `all-in-one/sources/GME_20250506.zap18` | `00c79b6d986e68298f65b172c1807115bc5d9e450a74fcc989d0796d8d8a4ea8` | `211c4f604627a32f82a1124c2a9872c2fcf00865` |
| `all-in-one/sources/PEData.plf` | `647de7ea123daced41c27bec8f81aeb93c712cac714d4754d7da5c528abb016a` | `65605ff8910f920109da731604aa5dc8d83fc956` |
| `all-in-one/sources/PID_1684n002I.pdf` | `2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b` | `8c83a59fefd5b8b651ec3537ea4236a073f5e109` |
| `all-in-one/sources/decoded-original/0064-IdentXmlPart.xml` | `ce6afc4f7ca0a8059c2e3cab25d202f0faaa49a3bc6a2e9ee238964a76e9fc9d` | `300d74239868f4f4595d4d5bbb848b4b58bbae76` |
| `all-in-one/sources/decoded-original/0175-FlgNet.xml` | `41279d6aaa157de3be963d010d6ca7dea94811a0ace519c8a3d8baa015f67f97` | `1626da00b3bbcb46f77720271ecf0f50db9dc63b` |
| `all-in-one/sources/decoded-original/0238-FlgNet.xml` | `8f6a5537084e092c352552dc469bbe8469b33412971219e51bba211ef607dfa8` | `c1093180555a6a00486d0a7268bb3a059b7cbf9e` |
| `all-in-one/sources/decoded-original/0253-FlgNet.xml` | `2d35470eb44fff79916b93fcf57a597b2b9a03211e8493c2283706dc2c875154` | `6d5dc12df96c7fc47ad7f25eba6ba9a55a6755d0` |
| `all-in-one/sources/decoded-original/0397-FlgNet.xml` | `bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834` | `4ab8370493c4e28fc1eabeeebe2743d27f0c4021` |
| `all-in-one/sources/decoded-original/0398-FlgNet.xml` | `4f092b18df4e44af98fd44e173f48dad213a4e80b71f46b0a5e8a700f5b0a747` | `67ebb54daa55093487ea7e780f23ae2cf193c397` |
| `all-in-one/sources/decoded-original/0401-FlgNet.xml` | `60171c213e666de544077b7e4b497675813f7c0e75df85a3e76ab1def49b04ae` | `aadefbd35d305dd4a1146bf383b988a903802bf4` |
| `all-in-one/sources/decoded-original/0415-FlgNet.xml` | `7690a90cbad58f5e8474c94efc4a105e80522fb57e3516a720aab53e1146b07d` | `2cb9c21b425df9bfd0c36c0f8ab0257257a93a6e` |
| `all-in-one/sources/decoded-original/0538-FlgNet.xml` | `afb3c3104bb60b4b1310f62ed5fb2caf659afc514c2b3fd209ff71d2008686ce` | `3372843d3fb58f402f82a6250588ffa90f7707dc` |
| `all-in-one/sources/decoded-original/0555-IdentXmlPart.xml` | `46c36333e249dd775c1db94a1f6e80a36cf1a5a9c998b7d0980ae01d862901e6` | `9a915a8b9a260b48402df151c1fe0bbcb2f4ea1c` |
| `all-in-one/sources/decoded-original/0557-IdentXmlPart.xml` | `536563da118493838d346a6b34b4367bed4185edbe150d79eb2b2042c3950bf0` | `f627dd27d001a8af1770fd43a5dc04ceb572d4e6` |
| `all-in-one/sources/decoded-original/0558-IdentXmlPart.xml` | `45d49d53b6b41312960bb2a329663e87d8803e28d7832308424a6bf5091e6d1b` | `a0b681bd15e9ae15f2e1437576a4486cc732fdf2` |
| `all-in-one/sources/decoded-original/0582-IdentXmlPart.xml` | `41d4c2bd750392bbc2edc43995ec3a9da47a63c13ee86496df8f187492008951` | `82636dec064876d0f4cc714ef385b07d6e05efe0` |
| `all-in-one/sources/decoded-original/0584-IdentXmlPart.xml` | `3bff6c478e594bf97bb1730971944e96b0b5e2407199420fe6567d5fe609ea5d` | `0f8dde829be66041bea79e40ccc4586d84ff1da7` |
| `all-in-one/sources/decoded-original/0585-IdentXmlPart.xml` | `e36ec18aa4abebea8f9160254522bb51ff722eae804c5a469790f85f02939184` | `16574d37ef3ca61b59ba396c400e269ab1dd3440` |
| `all-in-one/sources/decoded-original/0602-IdentXmlPart.xml` | `46ab21151eddaaf616469db520730c60423eb742aa491af194e6710c751b4caf` | `bcb12ab1ce8c476ff921baa1608f29d9822f76b4` |
| `all-in-one/sources/decoded-original/0603-IdentXmlPart.xml` | `e93969dfa281d75b49b24127793068e33472dadb19729c1c48fc4a8dad075ef8` | `3a92b304baf4dbf6147e944d9778d2da11285cb1` |
| `all-in-one/sources/decoded-original/0604-IdentXmlPart.xml` | `b798d29c5499b5314a1ee3cff9139dae64c887533b86baa43b6e9a052373a6af` | `bb2c318788b97e7a4924a176275c12d805aa519d` |
| `all-in-one/sources/decoded-original/0605-IdentXmlPart.xml` | `0ff6e2228dbfbc9f657359fe1055083ce621365084ea24c4160e4969b3eaac8b` | `30e199288c147aa22d5ce8407178a391b89c6b1b` |
| `all-in-one/sources/decoded-original/0606-IdentXmlPart.xml` | `73d45f9e2a34bba8a25df1ed1f71e8f6404fc96a8d6481672652a48435b6a740` | `ced032fa747a8544abf17058ee5ebaa78ba9b23b` |
| `all-in-one/sources/decoded-original/0627-IdentXmlPart.xml` | `08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb` | `61ebc0abbb2ca160e11e1da400a3f14a397d8bc5` |
| `all-in-one/sources/decoded-original/0628-IdentXmlPart.xml` | `9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd` | `170ca5c72599edc7ea7eefe651c3680ce325e76a` |
| `all-in-one/sources/decoded-original/0629-IdentXmlPart.xml` | `67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972` | `058129bb01e27f7a6a0d0293f332d745e5bab74e` |
| `all-in-one/sources/decoded-original/0632-IdentXmlPart.xml` | `fd162c603476c2cac899010cee7a8ee382b6092c115135e3ac1007ae71c544e9` | `600935fa8d394c0d247ea20040d5dfff4f05b500` |
| `all-in-one/sources/decoded-original/0633-IdentXmlPart.xml` | `9e00aa275fa1b4e488b73983b309c6b73dcf4f3dd9be5dec13e9975d68f3c0fc` | `a1ab5ee12addbc92d04c9950d4437e2b564d6b5c` |
| `all-in-one/sources/decoded-original/0635-IdentXmlPart.xml` | `1a057d686446a3fdab7ac61bb09bc543c52f49646c9ca71ac323c10fcdffe457` | `95bfcad59cfb0c12b573e9e8face4262d1e94622` |
| `all-in-one/sources/decoded-original/0636-IdentXmlPart.xml` | `ec3d79f03e2748f8def4409ad676a97b98e28b9d8e68f6a64b3fe894466832ca` | `86114327ba1a010b2fcc01dd12b1bf86c01bc02c` |
| `all-in-one/sources/decoded-original/0682-IdentXmlPart.xml` | `25c7aeb1bfa29c178eaa396db33d4eb6d2d29b9a3f2eb965fa61fae8ce7f1092` | `61182411e912941161eccf4e90c1f174e5379f0a` |
| `all-in-one/sources/decoded-original/0683-IdentXmlPart.xml` | `0c9b569d041cd5babbbeded8a3bdc5d3754927125756b6ac54b7cb991b22fc22` | `662acdb9a06c0ba1c0027e7dd215a28f07d3f02b` |
| `all-in-one/sources/decoded-original/0684-IdentXmlPart.xml` | `6e9b3f173184adcddca503e81e2649022734b6ea3639c1d5ddaf0a08bac00208` | `d67b98b5d5516e0330aae5cfdbee41a3e09206e1` |
| `all-in-one/sources/decoded-original/0686-IdentXmlPart.xml` | `b450d8ff22f0fffd7a214b2a696af28a03a27834ebf862bfaa822dc9bfb3c8d4` | `8c152d926692a8e15973c980e08e338d29411814` |
| `all-in-one/sources/decoded-original/network-map.json` | `c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60` | `424430b6b953e43138e5d0a18ca40c949e21cfa1` |
| `all-in-one/sources/hmi_plc_tags.csv` | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` | `cf4c0650e7c7baac350dcb89909b808435704880` |
| `all-in-one/sources/live_index.json` | `14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1` | `e35ccea1f841349c632666c29954b7bcd4f5839e` |
| `all-in-one/sources/source-manifest.json` | `5af6e85994536897fd92f75972534a691e6eb0f067aafe07679c0788fd84e5bf` | `38cf407491d52dc6128cf94ca8a4bddee350de6d` |
| `docs/equipment-standard/INVENTORY.json` | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` | `587c3748ad9224718f95ba06463fee913dae231d` |
| `docs/equipment-standard/WORK-ITEM-TEMPLATE.md` | `4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586` | `e546f39535d2b589e80f97db869ac37ce4d05cfd` |
| `docs/equipment-standard/WORK-STANDARD.md` | `05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99` | `f76a570cc73098632e08759b17934000f7e3a253` |
