# MC04(P08) 조사·문서 1차 초안

- 상태: 원본 대조를 포함한 문서 초안. 코드 반영·검증·게시 전이며 현장 수리 완료 문서가 아니다.
- 대상: catalog_id MC04, priority_key P08, 금속 컨베이어, 분류 motor/원료 이송. 본체·모터·제어기의 동일성은 별도 판정한다.
- 표준: GME-STD-1.0.0. 기준은 공개 저장소 main/all-in-one/.
- 고정 기준: main 10051ddf45f6fd740d057bda51bee3db5a57382e, VERSION v1.7.0. 사용자가 FN03 검증·게시 완료를 전달했으며 dot이 배포 검사를 다시 실행한 것은 아니다.
- 조사자: 사용자의 dot, 자체 환경에서 직접 원본 조사·초안 작성. 실행 모델/추론 수준의 관측값은 미확인. 후속 코드 통합·검증·게시 담당은 사용자가 지정한 기존 Codex(GPT-6.1 Sol / High).
- 조사: 2026-10-11 05:31 UTC/14:31 KST 이후. 초안 저장 시각은 부록에 기록한다.
- 수정 범위: 이 MD 하나. 저장소 공통 코드·버전·완료대장·운영기록·배포는 수정하지 않았다. 실제 PLC·현장·보호값 변경, 시뮬레이터 작성·수정·생성·실행·행동시험은 하지 않았다.
- 세진 설비관리 프로그램의 데이터·코드·사진·작업이력은 사용하지 않았다. 아래 시공 참고 PDF는 GME 공개 저장소에 이미 포함된 자료이며 표제란의 고객명과 별개로 이번 조사 원본으로만 읽었다.

## 표준 적용과 접근 경계

저장소 .agents/skills/gme-equipment-rollout/SKILL.md, docs/equipment-standard/WORK-STANDARD.md, WORK-ITEM-TEMPLATE.md, INVENTORY.json의 7영역·원본 선언/핀 추적·현행/원본/해석 분리 방식을 적용했다. 사용자 역할 제한이 우선이므로 자동 코드 반영·대장 갱신·2차133후보 조사는 하지 않는다. 자체 환경의 PDF 읽기/렌더 기능을 사용했다. 별도 tia-equipment-alarm-trace는 제공된 로컬 스킬 영역에서 찾지 못했으며 권한을 확장하지 않았다. Mac 인계 파일은 읽지 못했다. 사용자의 최신 지시대로 Codex 창 ID 연결을 재시도하지 않고 이 대화에 파일로 전달한다.

S/는 all-in-one/sources/decoded-original/, R/는 all-in-one/registers/를 뜻한다. LAD 번호는 검색/문서 ID이며 원본 선언 NID와 다르다. 아래 네 자리 XML 번호는 모두 S/ 아래 실제 파일이다. ORef UId→RefId→선언 RID와 CS/C의 NID·UID를 함께 맞췄다. 다른 파일에서 숫자가 같은 선언을 자동 합치지 않았다.

[고정 커밋 원본](https://github.com/esp6662266/gme-plc-manual/tree/10051ddf45f6fd740d057bda51bee3db5a57382e/all-in-one). 실제 바이트 SHA-256은 끝에 제공한다.

## 후속 검토자가 먼저 볼 핵심

1. MC04는 FG24/PDF25에서 M09, 11kW·19.3A, 24AS1 인버터 회로다. 도면의 ACS355 15kW와 모터 11kW는 서로 다른 장치 표기다. 현재 명판·설정 확인으로 대신하지 않는다.
2. 자체 감시는 LAD1791의 Tag_57 %T54, SdCoil Part437, S5T#5S다. FAULT와 INV가 같은 타이머를 공유한다. 다른 팬의 2초/35초·태그·항목 수를 쓰지 않는다.
3. 요청 해제는 ON AND (MC_04_FAULT OR MC04_INV OR (NOT Inputs.VS01 run AND NOT Allarm.Maintenance_ON)). 유지보수 조건은 마지막 VS01 분기에만 있다. 고장 전체를 우회하는 식으로 표시하면 틀린다.
4. Allarm.Maintenance_ON은 Flag.Maintenance_ON과 같은 변수가 아니다. 원본 LAD1930에는 ON과 Flag의 직렬 접점을 통해 Allarm 쪽을 쓰는 별도 Coil이 있다. 읽기/쓰기와 호출 시점을 유지한다.
5. 원시 I0.6/I0.7/I6.5→Inputs DB13 비트의 Word 전송 원본을 확인했다. 다만 Main 호출은 앞선 ENO와 NOT Simulation(1) 조건에 매이며 현재 CPU 실행·정상극성·최종값은 미확인이다.
6. 토크 알람 LAD1792는 제목 mc04 deleted이지만 원본에는 OFF 조건의 Set/Reset이 남아 있다. FG25/122는 SS10을 SPARE로 표시한다. “정상 사용 중 토크 보호”나 “코드 완전 삭제” 어느 쪽도 확정하지 않는다.
7. MC04 속도 출력은 LAD1693에서 SET_PERC_MC04를 10~100으로 제한하고 272와 곱해 102A5_SPARE3 %QW294로 기록한다. 이름이 SPARE여도 FG112의 PAW294는 MC04 4–20mA→FG24 AI1이다. 현재 드라이브 파라미터·속도 단위는 확인하지 않았다.
8. 전류 표시 LAD1769는 실제로 MV04_M18A %IW324를 읽어 Amp_MC04와 MC04_Absorbption_OFR로 보낸다. 기존 MV04-MC04 불일치를 보존한다. 계수100을 “100A 전류센서 확정”으로 바꾸지 않는다.
9. HMI 설정 3행과 호출 핀은 있으나 LAD1182의 실제 MC04 피연산자 바인딩은 미해석이다. DB11,X8.1을 MC_04_FAULT 단독 알람이라고 단정하지 않는다.
10. 운전시간 LAD1022의 HOUR는 원본상 Move 상수1이다. MIN Add1과 구분하며 일반적인 시간 누적식으로 고쳐 설명하지 않는다.

## 7영역 적용표

| 영역 | 상태 | 이 초안의 범위 | 남은 경계 |
| --- | --- | --- | --- |
| 설비·자료 기준 | 적용 | P08/MC04/M09, PV02→MC04→VS01 관계, 기존 불일치·시점 | 실제 본체/모터 동일성·현행 모델 |
| I/O·HMI | 적용, 일부 미확보 | 4 디지털 I/O, QW294 별칭, IW324 상충, DB 전송, HMI 3행/핀 | HMI 인스턴스·이벤트·온라인 연결·공학 단위 |
| 제어 구조 | 적용 | 요청 Set/Reset, 최종 Q, VS01 조건, 유지보수 쓰기, PV02 소비 경로, 시간 | 실제 호출/쓰기 순서·현재 값·전원복귀 |
| 전기 전달 경로 | 적용 | FG24/25/112/116/122/136 및 14/17 실제 렌더, 시공34/51/59 | 준공·현재 단자·안전회로 성능·보호설정 |
| 알람·복구 | 적용 | FAULT/INV 공유5초, OFF 토크, 범위초과 출력·리셋 구분 | 정상극성·실제 고장 원인·재기동/복구 |
| 증상별 수리 | 적용, 관찰 초안 | 증상별 비교 위치·자료·판정 경계 | 실제 측정/조치/복구 미수행 |
| 완료 기준 | 적용 | 근거표·누락·Codex 핵심 확인·상태 분리 | 코드/UI/게시·TIA·CPU·현장 검증 |

# 1. 설비·자료 기준

## 1.1 관리 식별과 공정·소유

INVENTORY의 P08은 MC04 태그 대응이지만 identity_verified:false, catalog parent_id:null, existing_detail:symptom, bc01_standard_acceptance:not_assessed다. 이름만으로 실물 확인 완료나 본체/모터 병합을 하지 않는다.

원본 sources/PID_1684n002I.pdf PDF1(Rev.I)을 실제 렌더로 확인했다. MC-04/M09 11kW·440V 및 SS-10이 PV-02 배출과 VS-01 사이에 배치된다. 전기 FG24/PDF25의 MC-04/M09와 태그가 대응한다. 공정상 하류 VS01이나 상류 PV02는 MC04의 하위 모터나 직접 Q 소유가 아니다. MC05/M10, VS01 M06/M07, MC03 spare를 MC04에 합치지 않는다.

## 1.2 원본 시점·기존 자료 보존

- 전기도면 FG24/25/112/116/122/136: 기본 일자 27.05.2024, 해당 표제란 REV2/17.03.2025. FG14는 같은 개정 표시를 임의로 채우지 않는다.
- 시공 Electrical_Can_Decoating_20241118.pdf는 24.11.11 first draft design 표제란을 가진 참고 자료다. 준공도·현재 배선 확인으로 승격하지 않는다.
- 기존 procedures/MC04.html, devices/MC04.html과 control/alarm/electrical/signal 파생 자료를 읽었다. 기존 ADDRESS, MV04-MC04, SOURCE-XML 및 현장 미확정은 지우지 않는다.
- 백업 파일명/내부 프로젝트 날짜 차이, P&ID와 전기 세대 차이도 기존 대로 남긴다. 이 초안은 현재 CPU 다운로드본을 확보한 결과가 아니다.
- 기존 문서의 시뮬레이터 링크·시험 설계는 과거 보존 자료다. 이번 완료 범위나 실행 근거로 세지 않으며 재작성/재실행하지 않는다.

# 2. I/O·HMI와 주소·변환

## 2.1 물리·내부·아날로그 구분

| 대상 | 주소/형식 | 근거 | 해석 및 미확정 |
| --- | --- | --- | --- |
| MC04_Fbk | %I0.6 Bool | 0613 RID146/NID24 UID1342, SAD Input AO6; R/plc-symbols.csv 문서958; FG116 | MC04 RUN 원시 입력. 실제 회전/정상극성은 별도 |
| mc04_all_inv | %I0.7 Bool | R/plc-symbols.csv 문서916; FG24 ALARM→FG116 E0.7; Word 전송 아래 | CSV 설명 feedback motor mc-04와 ALARM 표기 차이 보존. 단독 원시 심볼 선언 연결은 미확보 |
| MC04_torque | %I6.5 Bool | 0558 RID40, Monitor UID60, SAD Input AO53; FG25/122 SS10 | 도면 SPARE와 OFF 네트워크 구분. 설치·사용 상태 미확정 |
| Start MC04 | %Q0.4 Bool | 0602 RID66/NID11 UID352, SAD Output AO4; 0247 W365; FG136 | 설명의 옛 A49.1을 현재 출력 주소로 쓰지 않음 |
| Tag_57 | %T54 Timer | 0658 RID54/NID12 UID452/453, SAD Timer AO54 | 공유 PLC 타이머. HMI/물리 입력으로 분류하지 않음 |
| Flag.M_MC_04 | DB member Bool AO4 | 0604 RID65/NID11 UID350/351; 0577 RID33/NID3/4/5 | 운전 요청·기억. Q 자체가 아님 |
| Inputs.MC04 run / MC04_All_inv / MC04 torque | Inputs DB13, bit6/7/53 | 0657 RID274/275/276 및 0655 DepDB RID247, TOD13 | 각각 DB13 0.6/0.7/6.5. 원시 I와 영역 분리 |
| 102A5_SPARE3 | %QW294 Word | 0664 RID145/NID18 UID39, SAD Output AO2352; 0474 W55 | MC04 속도 경로와 도면 PAW294 대조. 별칭 이름 그대로 보존 |
| MV04_M18A | %IW324 Int, peripheral | 0678 RID472/NID52 UID26, AO2592, SAM Peripherie; R/plc-symbols.csv 문서1726 | 원문 설명 MV-04 position M18A. MC04 전류로 단정 금지 |
| HMI_DB.SET_PERC_MC04 | Int 멤버, AO432 | 0662 RID149/NID18 UID29/32/33/36/37 | 10~100 클램프·272 곱셈. 현재 HMI 조작 이벤트/단위는 별도 |
| HMI_DB.Amp_MC04 | 멤버 AO464 | 0676 RID473/NID52 UID29, Write | 변수명은 전류 의도 단서. 실제 전류 센서/단위 확정 아님 |
| Allarm.MC04_Absorbption_OFR | Bool AO142 | 0676 RID474/NID52 UID30, Write | 철자 Absorbption 원문 유지. 범위초과 함수 출력 |

AO가 bit offset인 선언은 영역·자료형과 함께 읽었다. 같은 숫자의 AO를 가진 Flag/Allarm/Inputs를 같은 메모리로 합치지 않는다.

## 2.2 원시 입력 → DB 처리 응답의 정적 전달

S/0397-FlgNet.xml HMI Inputs/LAD1070, NID1:

| 입력 Word | 원본 입력 선언 | Move 및 Wire | 목적지 선언 | MC04 관련 비트 |
| --- | --- | --- | --- | --- |
| Tag_178 / IW0 | 0627 RID3, UID25, Word/SAD Input/AO0 | Part22.in W23 ORef25; out1 W24 ORef26 | 0629 RID5, UID26, Word AO0/BIRID4 | I0.6/0.7→DB13 0.6/0.7 |
| Tag_171 / IW6 | 0627 RID13, UID45, Word/SAD Input/AO48 | Part42.in W52 ORef45; out1 W54 ORef46 | 0629 RID14, UID46, Word AO48/BIRID4 | I6.5→DB13 6.5 |

0628-IdentXmlPart.xml DepDBBlock RID4는 Inputs, TOD N13, CID638561979615757134다. 0655 RID247도 같은 Inputs/DB13/CID이므로 0657의 MC04 세 멤버의 BIRID와 연결된다. 이름·오프셋의 유사성만이 아니라 Word Move와 DB 종속 선언을 통해 정적 경로를 확인했다.

목적지는 Inputs DB13이다. Part22와 Part42의 en은 Wire21 Powerrail에 연결된다. 이 두 Word Move 경로에는 비트 반전이 없다. 다만 원본 Move의 DisableENO="true"와 다른 Move들의 ENO 연결을 보존하며 TIA 실행 의미를 임의 보완하지 않는다.

Main 0030-FlgNet.xml LAD1613/NID19은 Recipes Handler CRef21→W32 ENO→HMI CRef23→W33 ENO→HMI Output CRef25→W42 ENO→반전 Contact37→W43→HMI Inputs CRef28.en 순으로 연결된다. Contact37.operand=W44/ORef45/0692 RID140 Simulation(1) (%M180.0). 0688 RID135/NID19 UID29와 0694 RID136/TORID135가 호출을 뒷받침한다. 즉 앞선 ENO 조건과 NOT Simulation(1)의 정적 호출 경계가 있다. 해당 메모리의 현행 값·현재 CPU 실행·호출 주기·다른 쓰기로 덮인 최종값은 확인하지 않았다. 이 설명은 시뮬레이터 실행/재개 지시가 아니다.

## 2.3 HMI 설정과 실제 호출 바인딩 경계

sources/hmi_plc_tags.csv 및 R/equipment-hmi.csv:

| 태그 | 설정 주소 | Access Name | ID |
| --- | --- | --- | --- |
| MC_04\Allarme1 | DB11,X8.1 | PLC | 0043A |
| MC_04\RispostaA | DB11,X8.0 | PLC | 00324 |
| MC_04\Flag | DB2,X0.4 | PLC | 001B0 |

설정 추출 행이지 현재 HMI 이벤트/온라인 상태의 증거가 아니다. MC04 호출 0361-FlgNet.xml LAD1182는 CRef23/RefId638, CodeBlock22/RefId1이며 다음 핀을 보존한다.

| 핀 | Wire | ORef UID/RID | 확인 상태 |
| --- | --- | --- | --- |
| en | 21 | Powerrail | 정적 직접 연결 |
| Ingresso_run | 24 | 25/710 | 실제 대상 선언·NID 바인딩 미해석 |
| Allarme1 | 28 | 29/76 | 미해석 |
| Allarme2 | 30 | 31/20 | FALSE 후보 포함, 해당 호출 NID 확정 전 보류 |
| Allarme3 | 32 | 33/78 | 미해석 |
| Allarme4 | 34 | 35/48 | FALSE 후보 포함, NID 보류 |
| Allarme5 | 36 | 37/48 | FALSE 후보 포함, NID 보류 |
| Risposta | 42 | 43/70 | 미해석 |
| Comulativo_allarmi | 46 | 47/72 | 미해석 |

공통 0355-FlgNet.xml/0621 Local 선언의 Ingresso_run→Risposta와 5개 알람 OR→Comulativo_allarmi 구조는 함수 수준 사실이다. 0623 FCBlock RID1 및 0624 BlockInterfaceInfo RID638 후보만으로 MC04 인스턴스의 8개 실제 피연산자를 확정하지 않는다. DB11,X8.1과 MC_04_FAULT·MC04_INV·MC_04_TORQUE의 정확한 합산/표시 관계는 미확정이다. HMI 원본 프로젝트·dde.cfg 원본·화면 이벤트·해당 NID 선언·DB 레이아웃이 필요하다.

## 2.4 속도 출력: SPARE 이름과 실제 도면 경로

LAD1693 0474-FlgNet.xml, NID18:

- Contact22의 ON(0664 RID1 UID28) out=W42는 Lt23.pre, Gt25.pre, Mul27.en으로 분기한다.
- Lt23: W43/ORef29 SET_PERC_MC04, W44/ORef30 상수10. out W45→Move24.en, in W46/ORef31=10, out1 W47/ORef32=SET_PERC_MC04.
- Gt25: W48/ORef33=SET_PERC_MC04, W49/ORef34=100. out W50→Move26.en, in W51/ORef35=100, out1 W52/ORef36=SET_PERC_MC04.
- Mul27(Int): W53/ORef37 SET_PERC_MC04 × W54/ORef38 상수272 → W55/ORef39 102A5_SPARE3.
- 선언 0662 RID149; 0661 RID146=10, RID12=100, RID16=272; 0664 RID145=Output AO2352(%QW294). 모두 NID18 UID 일치로 대조했다.

정적 원문 산술은 SET_PERC_MC04 × 272다. 일반적인 다른 아날로그 스케일 값으로 바꾸지 않는다. ON과 클램프·곱셈이 같은 분기에서 수행되므로 현행 스캔 순서/타입 변환 검증 없이 모든 상태에서 출력 범위를 보장한다고 말하지 않는다. 도면 FG112/PDF113의 MC04 PAW294 4–20mA와 FG24 AI1 연결은 아래에서 확인했다. 10이 현장 최소 Hz나 안전 운전 한계라는 근거는 없다.

## 2.5 전류 표시·범위 알람의 MV04 상충

LAD1769 0526-FlgNet.xml, NID52, CRef22/RID351, CodeBlock23/RID5. 0672 RID5/NID52 UID23은 Signal linearization이다.

- Contact21 operand W32/ORef24=ON, out W33→CRef22.en.
- IN0 W34/ORef25=ON(0678 RID1).
- Analog_input W35/ORef26=MV04_M18A(0678 RID472/%IW324, peripheral).
- Coeff W36/ORef27=100(0675 RID42), Zero W37/ORef28=0(0675 RID44).
- OutValue W38/ORef29→HMI_DB.Amp_MC04(0676 RID473).
- Out_of_range W39/ORef30→Allarm.MC04_Absorbption_OFR(0676 RID474).

제목과 출력은 MC04인데 입력 심볼/주석은 MV04 위치다. 기존 MV04-MC04 불일치와 동일한 원본 연결이며 이번에 해소하지 않았다. 실제 센서·모듈 채널·배선·프로젝트 변경 승인 자료가 필요하다.

공통 함수 자체도 0291-FlgNet.xml LAD1658/NID1 및 0014-FlgNet.xml LAD1659/NID2를 읽었다. Local 선언은 0611, 상수는 0612다.

- 유효 계산 분기: IN0 Contact255 → Gt258(Analog_input > -1382) → Le161(Analog_input <= 32767) → Convert164/167 → Add170 → Convert174 → Mul177 → Div181 → Move185. DInt 중간값과 각 ENO를 거친다. 산술 의도는 (Analog_input + Zero) × Coeff / 28000이며 OutValue는 Int 출력이다. 정수 나눗셈·변환·오버플로 실행은 미검증이다.
- 범위 분기: Gt190(Analog_input >32767)와 Le259(Analog_input <=-1382)가 OR47로 모여 W49→Move193.en. W252/ORef218은 원문 -9999. Move193.out1 W253/ORef219→OutValue, eno W21→Coil23.in, operand W22/ORef24→Out_of_range.
- 따라서 OFR은 위 범위 분기에서 Move193의 ENO를 거친 Coil이지 MC04 운전 고장 래치와 같은 Set/Reset은 아니다. Int 입력에서 >32767 분기가 실제 성립하는지 임의 가정하지 않고 원본 그대로 남긴다.
- IN0 반전 분기는 0014 Contact171→Move162(상수0)→OutValue다. MC04 호출 자체의 en도 ON에 묶여 있으므로 ON=0에서 함수가 실행되어 0으로 초기화된다고 단정하지 않는다.
- 상수 원문/부호를 보존한다. 0612의 RID25(-1382)는 저장 V4294965914, RID21(-9999)는 V55537이며 이를 양수 공학 값으로 읽지 않는다.

# 3. 제어 구조·복수 쓰기·소유 경계

## 3.1 최종 기동 출력과 요청 해제

LAD1941 0247-FlgNet.xml, NID11:

ON AND (Allarm.MC_04_FAULT OR Allarm.MC04_INV OR (NOT Inputs.VS01 run AND NOT Allarm.Maintenance_ON)) → RCoil340 Flag.M_MC_04

- Contact367(ON) out W368가 세 해제 분기와 출력 경로로 분기한다.
- FAULT Contact369→W370→OR333.in1. ORef346/RID62, 0604.
- INV Contact22→W24→OR333.in2. ORef23/RID205, 0604.
- NOT VS01 Contact26→W28→NOT Maintenance Contact380→W29→OR333.in3. ORef27/RID224와 ORef381/RID6, 0604.
- OR333.out W360→RCoil340.in; operand W362/ORef350→Flag.M_MC_04,0604 RID65/Write.
- 출력은 ON 후 Contact377(Flag.M_MC_04) out W378→Coil344, operand W365/ORef352→Start MC04,0602 RID66/Output Q0.4.

유지보수 조건은 VS01 미응답 분기에만 영향을 준다. FAULT/INV가 참이면 별도의 해제 분기는 남는다. 요청 Reset과 물리 출력 Coil은 구분한다. 논리 경로를 확인한 것이며 현재 CPU 스캔 내 최종 우선순위/동시 Set·Reset 결과는 확인하지 않았다.

## 3.2 유지보수 두 변수의 원본 연결

LAD1930 0237-FlgNet.xml NID1: ON Contact47.out W48→Flag.Maintenance_ON Contact49.out W50→Coil34 및 Coil36. MC04가 읽는 것은 Coil36 operand W45/ORef41의 Allarm.Maintenance_ON이다. 0604 RID3/NID1 UID39는 Flag, RID6/NID1 UID41 Write는 Allarm이다. 같은 AO61이라도 서로 다른 DB다. 이 원본은 ON AND Flag.Maintenance_ON → Allarm.Maintenance_ON의 별도 쓰기를 보여준다. 현재 실행 시점·다른 쓰기·온라인 일치 확인 없이 두 이름을 치환하지 않는다.

## 3.3 자동 요청의 MC04 자체 Set/Reset

| 근거 | 동작 | 정적 조건과 MC04 핀 | 미확정 |
| --- | --- | --- | --- |
| 0164 LAD1843/NID3 | RCoil460 | ON AND NOT Emergency_module_fault AND Tipo_preset=1 AND Auto_ON1 AND Tempo_presetting=17; W708/ORef616→0577 RID33 | 예열 단계에서 MC04는 Reset이다. 다른 팬 Set을 복제하지 않음 |
| 0165 LAD1844/NID4 | SCoil799 | ON AND NOT Emergency_module_fault AND Auto_ON1 AND Tipo_preset=2 AND Tempo_presetting=24; W1062/ORef962→0577 RID33 | 생산 요청. 실제 단계 시간 단위·현재 레시피 미확인 |
| 0166 LAD1847/NID5 | RCoil954 | Auto_ON1 AND Tipo_preset=5 AND (Tempo_presetting=19 OR Emergency_module_fault); W1075/ORef1015→0577 RID33 | 이 네트워크에는 별도 ON 직렬 접점을 임의 추가하지 않음 |
| 0247 LAD1941/NID11 | RCoil340 | 자체 FAULT/INV 및 VS01/유지보수 분기 | 자동 Set과 다른 위치의 요청 해제 |

원본 비교 상수 17/24/19는 0578 RID30/44/35, 각 CS/C NID3 UID613·NID4 UID961·NID5 UID1014로 확인한다. 숫자를 검증 없이 “17초/24초/19초”로 바꾸지 않는다. HMI 설정에 Flag 주소가 존재하지만 실제 쓰기 이벤트는 미확정이므로 위 네 정적 쓰기만으로 모든 writer를 다 찾았다고 주장하지 않는다.

## 3.4 연결 설비의 소비 경로는 MC04 출력 소유가 아님

- PV02 gate: 0280-FlgNet.xml LAD1916/NID5의 Contact524(ON)→W525 세 분기. Contact526=원시 MC04_Fbk(0607 RID51/UID482/W500), Contact22=Inputs.MC04 run(0609 RID87/UID23/W21), Contact29=Allarm.Maintenance_ON(0609 RID156/UID30/W28). W527/W24/W31이 OR443의 세 입력이다. 따라서 gate 쪽 앞단은 ON AND (raw MC04_Fbk OR Inputs.MC04 run OR Allarm.Maintenance_ON)이며 두 응답을 AND로 합치면 틀린다. 이후 Enable_R2_GATE·위치/기억 조건을 거쳐 Part456/458이 gate 상태를 쓴다. 이는 MC04 응답을 소비하는 PV02 네트워크이며 StartMC04의 writer가 아니다. PV02 전체 조사/튜닝은 이번 대상이 아니다.
- MC03 spare: 0246-FlgNet.xml LAD1940은 Inputs.MC04 run을 소비하지만 자체 대상은 M_MC_03/Start Spare Motor다. 0604 RID259/NID10 UID321을 MC04 제어 소유로 바꾸지 않는다.
- VS01은 0247의 해제 조건에서 소비되는 응답이다. MC04의 단일 M09와 VS01의 여러 모터 구성을 섞지 않는다.

## 3.5 호출 경계와 시간 기록

Main 0031 LAD1619/NID6은 ON 후 Analog input conversion CRef261/CodeBlock273 및 Allarms1 CRef264/CodeBlock275를 연결한다. 0549 LAD1620/NID7은 ON 후 Motors1 CRef319/CodeBlock337, R1 scraps gate2 CRef325/CodeBlock341, time work motor CRef334/CodeBlock347 등을 연결한다. 0032 LAD1621/NID8의 ON Contact352/W353→CRef344/CodeBlock349가 Analog output conversion을 호출한다. 0688 RID55/58/67/73/82/88의 블록명·NID·UID를 대조했다. 나열을 현재 온라인 호출·스캔 우선순위 보증으로 바꾸지 않는다. Auto start motors는 0067 RID39/NID4 UID186의 호출 선언이 있으나 전체 상위 호출/레시피 실행은 추가 확인 대상이다.

운전시간은 MC04 자신의 원본을 별도 확인했다.

- 0312 LAD1022/NID24: Tag47 Contact1370→MC04_Fbk Contact1372→W1373. Add1324는 MIN + 상수1을 MIN에 기록(W1355~1357). Ge1331은 MIN>=60(W1358/1359). out W1360→Move1334.en, in W1362/ORef1348=상수1, out1 W1363/ORef1349=MC_04_HOUR. **HOUR를 기존값+1로 더하는 Add가 아니다.**
- Move1334.eno W1364→Move1337.en, in W1365/ORef1350=0, out1 W1366/ORef1351=MIN. eno W1367→SCoil1340 Flag_Aggiorna_DB.
- 선언 0613 RID146=MC04_Fbk; 0615 RID148=MIN,RID150=HOUR; 0616 RID7=1,RID8=60,RID12=0, NID24/UID 대조.
- 0336 LAD1049/NID51: Tag48에서 시작하는 연속 Move의 Part2828.eno W2857→Part2831.en. in W2858/ORef2844=0, out1 W2859/ORef2845=MC_04_HOUR(0615 RID150). 다른 모터와 같은 초기화 네트워크에 있더라도 MC04 외의 값을 소유 항목으로 복제하지 않는다.
- Tag47/48 실제 생성 주기·전원복귀·HOUR 의도·현재 누적 정상성은 확인하지 않았다.

# 4. 전기 전달 경로 — 실제 PDF 페이지 대조

FG는 인쇄 도면 번호, PDF는 1부터 센 파일 페이지다. 아래 FG14/17/24/25/112/116/122/136을 원본 PDF에서 렌더해 실제 선·접점·단자 양 끝점을 보았다. 도면 CPU:515 표기는 현행 CPU 형번·장착 상태로 확정하지 않는다.

## 4.1 전원과 구동기·모터

FG24/PDF25: 3상 440V 60Hz, 6.2L1/L2/L3→24QM1 주접점→24R1/S1/T1→24AS1 U1/V1/W1. 24AS1 표기 ACS 355-03E-31A0-4 kW15. 출력 U2/V2/W2→24U1/V1/W1(실드24SCH1)→24QS1 주접점→M09/MC-04 U/V/W 및 PE. 모터 표기는 11kW·19.3A다.

24QM1에는 49–59A, RATING52A가 그려져 있다. 이는 도면 표기이며 현재 보호기 설정이나 적정 보호값을 검증한 것이 아니다. 15kW/11kW/52A를 하나의 모터 정격으로 섞지 않는다. 제조사 선정·조정 지시를 만들지 않으며 현행 명판/승인 설계/설정 기록이 필요하다.

## 4.2 기동 Q → 릴레이 → 드라이브 DI1

1. FG136/PDF137: A0.4 MC-04 MOTOR COMMAND, 도면 MOD14 단자5→FG25/2.
2. FG25/PDF26: A0.4→XS9→24QS1 보조접점→XS10→24QM1 보조접점→25KA1 코일 A1, A2→-0Vdc10.6.
3. FG24/PDF25: 24AS1 단자9 +24V→25KA1 접점1/9→단자12 DI1 START(선24.2).

PLC Q가 켜졌다는 사실만으로 25KA1 여자·DI1 수신·모터 운전을 확정할 수 없다. QS/QM 보조접점은 도면에 표시된 별도 전달 조건이다. 원본에 없는 단자 접점 번호나 현재 정상 상태는 보충하지 않는다.

## 4.3 RUN/ALARM 입력 양 끝점

- RUN: FG24에서 +24Vdc10.7→24AS1 RUNNING 단자17, 응답 단자19→E0.6/FG116/6. FG116/PDF117은 E0.6 FEEDBACK MOTOR MC-04, MOD8 단자7이다.
- ALARM: FG24에서 +24Vdc10.7→ALARM 단자20, 단자21→E0.7/FG116/7. FG116 MOD8 단자8이 ALARM MOTOR-MC-04다. FG24 단자22와 GND10/DCOM11의 -0V 공통 연결도 보존한다.
- 드라이브 출력 접점/출력의 실제 파라미터 기능·NO/NC 정상극성·단선 시 논리값은 이 도면과 변수명만으로 확정하지 않는다. 백업의 Inputs.MC04_All_inv는 알람 조건에서 비반전으로 읽히지만 실제 전기 정상상태와 같은 진술이 아니다.

## 4.4 속도 아날로그 출력 양 끝점

FG112/PDF113: MC04 PAW294, MOD7. +PAW294가 QV3/QI3 단자13, -PAW294가 MANA 단자16으로 연결되고 24SCH2 실드가 FG24/6으로 간다. FG24/PDF25에서는 +PAW294→24AS1 AI1+ 단자2, -PAW294→GND- 단자3, 24SCH2→SCR 단자1. 도면 4–20mA와 S1의 mA 위치 표기를 확인했다. 현행 스위치/파라미터·실측 전류·주파수 환산은 미확인이다.

## 4.5 토크 SS10, 리셋, STO를 구분

- FG25/PDF26의 점선 SPARE LIMIT SWITCH TORQUE CONTROL: +24Vdc10.7→X1/54 퓨즈5×20 2A F→SS-10 접점11/12→X1/55→E6.5. FG122/PDF123 MOD9 단자26=E6.5/SS-10, SPARE 표시. MC04 RUN E0.6과 다른 회로다.
- 인버터 리셋: FG24 단자9 +24V→17KA1 접점3/11→단자15 DI4 RESET(선24.7). FG17/PDF18에서 17KA1 코일 A1은 A7.4, A2는-0Vdc10.6. 같은 페이지의 17SB2 RESET ALARMS는 E19.7로 간다. PLC Flag.RESET_ALLARM의 실제 writer와 A7.4 전달을 이번에 끝까지 확인하지 않았으므로 버튼·Flag·드라이브 DI4를 같은 신호로 합치지 않는다.
- STO: FG24 X1C의 OUT1(1)→14KA1 접점5/6→IN1(3), OUT2(2)→14KA5 접점5/6→IN2(4). FG14/PDF15에서 14KA1/14KA5 코일은 각각13.5/13.6 계통과0Vac9.9에 연결되고 교차참조24/6·24/7이 보인다. 이는 도면상 회로 끝점 확인 범위다. 상위 비상회로 전체의 안전성/성능 등급·현장 동작·정상극성·현재 배선은 검증하지 않았다. 우회·점퍼·설정 변경 지시를 만들지 않는다.

## 4.6 시공 참고: 모터와 SS10 표기 충돌 보존

sources/Electrical_Can_Decoating_20241118.pdf:

| 실제 페이지/행 | 확인한 원문 | 해석·미확정 |
| --- | --- | --- |
| PDF34, EXIT ZONE01 / CONDUIT, D-page17, 도면034 | M09/MC-04, 케이블1_18=EXI+MC04-M09A, CV 16/4core, EXI1TB1→Pipe28→M09 | 배관 참고 경로. PDF51의 PVC-S/16SB와 표기 차이 보존 |
| PDF51 row1_18 | =EXI+MC04-M09A, CR→MC-04/M09, METALLIC CONVEYOR, DAC, PVC-S,4core,16SB,SPARE0 | route100→120→121→122→EXI1TB1→E100,Adjustment15,LEN87. 단위·실시공 길이 임의 확정 안 함 |
| PDF34 SS10 행 | 장치 LOC가 MC-05, TAG SS-10, cable9_7=EXI+MC04-SS10A,CVV1.0/2core | 케이블명MC04와 LOC MC05 상충을 삭제하지 않음 |
| PDF59 row9_7 | =EXI+MC04-SS10A, FROM MC-05/EXI1TB2→TO MC-04/SS-10,DC,CVV,2C,1.0,SPARE0,E351,Adjustment3,LEN3 | 접속함 위치와 장치 소유 구분. MC05 본체에 SS10을 자동 귀속하지 않음 |

전기도면의 SPARE와 시공 참고의 실제 케이블 행이 함께 존재한다. 이것만으로 현재 SS10 설치/활성을 확정할 수 없다. 승인 준공도·접속함/센서 태그 사진·현재 회로 변경 기록이 필요하다.

# 5. 알람·복구 — 자체 발생·해제·영향

## 5.1 FAULT/INV 공유 5초 감시

LAD1791 0428-FlgNet.xml, NID12:

ON AND Start MC04 AND (Inputs.MC04_All_inv OR NOT Inputs.MC04 run) → SD Tag_57, S5T#5S

- ON Contact473/W459 ORef449(0658 RID1)→W474→Start Contact475/W460 ORef450(0658 RID53).
- Start.out W476→All_inv Contact496/W499 ORef497(0657 RID275) 및 NOT run Contact500/W503 ORef501(0657 RID274). W23/W33→OR32.in1/in2→W34→SdCoil437.in.
- SdCoil437.value W461/ORef451→0656 RID175/NID12 UID451, S5Time 원문S5T#5S, stored V1280. 이것은1280ms가 아니다.
- operand W462/ORef452→0658 RID54/NID12 UID452 Timer Tag_57 AO54(%T54). 타이머 접점 Contact477는 W463/ORef453의 같은 선언을 읽는다.

| 알람 | Set 원본 | Reset 원본 | 영향·경계 |
| --- | --- | --- | --- |
| Allarm.MC_04_FAULT | ON AND Start AND Tag57 AND NOT Inputs.MC04 run→SCoil443; W480/in,W466/operand ORef455,0657 RID56 | ON AND Flag.RESET_ALLARM AND own_FAULT→RCoil448; W484/in,W471/operand ORef458 | 0247에서 운전 요청 Reset. 원시 I가 아닌 DB run을 읽음 |
| Allarm.MC04_INV | ON AND Start AND Tag57 AND Inputs.MC04_All_inv→SCoil487; W29/in,W493/operand ORef489,0657 RID215 | ON AND Flag.RESET_ALLARM AND own_INV→RCoil495; W26/in,W27/operand ORef28 | 같은 타이머의 다른 분기. 드라이브 구체 오류 코드는 별도 자료 |

Reset 입력은 0657 RID13/NID12 UID456(Flag.RESET_ALLARM)이다. 두 Reset에는 “원인 입력이 정상”이라는 추가 직렬 접점을 임의 삽입하지 않는다. 알람 비트 해제, 인버터 자체 오류 해제, Flag 재요청, 실제 기동/응답 회복은 별도 단계다. 두 알람이 동시에 성립할 가능성과 동일 스캔 Set/Reset 우선순위는 코드 호출/현재 실행 자료 없이 임의 결정하지 않는다. FAULT→요청 해제→Start 저하→타이머 입력 변화의 정적 연결은 있으나 실제 시퀀스 시간을 시험하지 않았다.

## 5.2 토크: OFF·deleted·SPARE 경계

0429-FlgNet.xml LAD1792, NID13:

- Set: OFF Contact478→NOT Inputs.MC04 torque Contact480→W36→SCoil454. operand W37/ORef38→Allarm.MC_04_TORQUE.
- Reset: OFF→Flag.RESET_ALLARM Contact482→Inputs.MC04 torque Contact484→own_TORQUE Contact486→W487→RCoil460. operand W476/ORef467.
- OFF는 0658 RID46/NID13 UID35이며 검색 중 다른 파일의 동일 RID/UID에 있는 BWF01_FlowRate로 잘못 해석하지 않았다. TORQUE는 0657 RID58; torque는RID276; RESET는RID13.

이 네트워크는 제목만 삭제된 것이 아니라 실제 OFF 신호로 gating된 원본을 갖는다. OFF의 현행 값·설치/사용 상태를 확보하지 않았으므로 “절대 실행 안 됨”도 단정하지 않는다. 현재 MC04 최종 요청 해제 식 0247에는 TORQUE가 직접 포함되지 않는다. 따라서 토크를 FAULT/INV와 동일한 직접 정지 알람으로 자동 추가하지 않는다. HMI 누적 알람에 들어가는지 역시1182 미해석 상태다.

## 5.3 범위초과·명칭·복구 구분

Allarm.MC04_Absorbption_OFR은 0526/0291의 변환 함수 출력으로 위 2.5를 따른다. MC_04_FAULT, MC04_INV, MC_04_TORQUE, MC04_Absorbption_OFR의 철자와 밑줄을 원문대로 보존한다. HMI Allarme1이라는 이름과 일대일로 합치지 않는다. 이번 추적은 확인된 알람 경로의 범위이며 “현장 MC04 총 알람이 정확히4개”라는 완전성 주장으로 쓰지 않는다.

현장 복구 완료는 실제 원인 제거·입력/출력/드라이브 상태·승인된 재요청·후속 연동·관찰 시각의 증거가 있어야 판정한다. 이 조사에서는 그런 조치를 수행하지 않았고 repairs_completed=0이다.

# 6. 증상별 수리·관찰 초안

아래는 자료를 구분해 기록하는 틀이다. 실제 작업·활선 측정·강제 출력·보호 변경을 지시하거나 수행한 기록이 아니다. 현장 담당자는 승인된 정지·전원 격리·작업 절차를 우선한다.

| 증상 | 필요한 같은 시각의 관찰 | 비교 원본 | 구분해야 할 원인/한계 | 복구 판정에 필요한 기록 |
| --- | --- | --- | --- | --- |
| 요청이 곧 해제됨 | Flag.M_MC_04,FAULT,INV,Inputs.VS01 run,Allarm/Flag Maintenance 각각 | 0247/0237,0164~0166 | VS01 분기와 자체 고장, 자동 Reset 단계, 실제 호출 순서 | 원인·요청 재설정·출력·실제 응답과 시각 |
| Q0.4는 있지만 안 움직임 | Q상태,QS/QM 전달,25KA1,DI1,드라이브 상태·STO 표시,실제 회전 | FG136→25→24,FG14 | PLC 명령과 전기 허가·드라이브 수신은 다름 | 승인된 점검·조치·회전/응답 회복 증거 |
| 약5초 후 FAULT/INV | Start,Tag57,raw I0.6/0.7,DB13 run/inv,최초 드라이브 코드 | 0428/0397,FG24/116 | 응답 지연·인버터 이상·원시/DB 전달·최초/후속 고장 | 정확한 발생/해제 시각과 각 신호·드라이브 기록 |
| SS10/토크 알람 설명이 맞지 않음 | 실제 SS10 설치표지,준공도,I6.5/DB6.5,OFF,알람 | 0429,FG25/122,시공34/59 | SPARE/삭제제목/OFF gating,MC05 접속함 표기 | 승인된 사용 여부·배선·설정 근거 확보 |
| 속도 설정과 실제 속도 불일치 | HMI설정값,SET_PERC_MC04,QW294,AI1설정·관찰값,드라이브주파수 | 0474,FG112/24 | 10~100 제한·272곱셈·SPARE별칭·HMI이벤트·현장환산 | 단위/파라미터/시각을 포함한 비교·복구 |
| 전류값/OFR이 이상함 | IW324 채널 출처,Amp_MC04,OFR,현장 센서와모듈명 | 0526/0291/0014,기존 MV04-MC04 불일치 | 값 자체를 MC04전류로 전제하지 않음 | 센서·배선·채널·현재프로젝트 목적 확인 |
| 운전시간이 누적되지 않음 | MIN/HOUR,Tag47/48,전원복귀/초기화 이력 | 0312/0336 | HOUR Move1과분Add,ENO·초기화·실주기 | 기능명세·현재값과 승인된 조사 결과 |
| HMI만 이상/Reset해도재발 | HMI주소·이벤트,DB11값,PLC알람,FlagRESET,A7.4,DI4각각 | 0361/0355,CSV,0428,FG17/24 | 합산표시·PLCReset·드라이브Reset·원인회복 분리 | 실제바인딩·통신·상태전환 근거 |

관찰 양식: 관찰자 / 날짜·시간·시간대 / 설비·위치 / 프로젝트·도면 판본 / 모드·단계 / 원시·DB·HMI·출력 각각의 값과 단위 / 최초 증상·알람 / 계측기·수집 방법 / 비교 근거 / 배제한 원인 / 승인 조치 / 복구 증거. 실운영 기록은 공개 Git에 넣지 않는다.

# 7. 핵심 근거표·미확정·인계

## 7.1 근거표

| ID | 핵심 주장 | 원본 위치·선언/핀 | 원문 해석 | 미확정 경계 |
| --- | --- | --- | --- | --- |
| E01 | P08↔MC04 | INVENTORY priority P08/catalog MC04 | 태그 대응/identity_verified:false | 실물·본체/모터 관계 |
| E02 | M09·인버터 회로 | Electrical FG24/PDF25,PID PDF1 | 모터11kW19.3A/드라이브15kW 구분 | 현행 명판·보호 설정 |
| E03 | 3디지털 입력·Q | R/plc-symbols.csv 916/958/1097/1335;0613RID146,0558RID40,0602RID66 | I0.6/0.7/I6.5,Q0.4 | 원시inv 단독선언·주석주소 차이 |
| E04 | 입력 Word 전송 | 0397 Parts22/42,W23/24/52/54;0627RID3/13,0629RID5/14,0628RID4;0655RID247 | Inputs DB13 0.6/0.7/6.5 연결 | 현재 호출·다른쓰기·최종값 |
| E05 | 입력 호출 경계 | 0030 CRef21/23/25/28,Contact37,W32/33/42/43/44;0688RID135,0692RID140,0694RID136 | ENO 및 NOT Simulation(1) | 현행 실행·메모리값 |
| E06 | HMI설정3행 | sources/hmi_plc_tags.csv,R/equipment-hmi.csv | DB11X8.1/X8.0,DB2X0.4 | 실제이벤트·인스턴스 |
| E07 | HMI호출 미해석 | 0361 CRef23/CodeBlock22,W24/28/30/32/34/36/42/46;0623/0624후보 | 8피연산자 실제바인딩 보류 | 해당NID·원본HMI필요 |
| E08 | 공유5초타이머 | 0428 Part437,W34/461/462;0656RID175/NID12UID451;0658RID54 | SD S5T#5S,Tag57/T54 | 온라인 타이밍·리셋·호출 |
| E09 | FAULT/INV Set | 0428 Part443/487,W466/493,ORef455/489;0657RID56/215 | run반전과inv비반전 구분 | 실제 정상극성·드라이브 코드 |
| E10 | FAULT/INV Reset | 0428 Part448/495,W471/27;0657RID13/56/215 | ON&RESET&own알람 | 원인회복·재기동 별도 |
| E11 | 요청Reset 분기 | 0247 Part340,OR333,W360/362;0604RID62/205/224/6/65 | FAULT∨INV∨(!VS01&!Maintenance) | 실행순서·다중쓰기 |
| E12 | Q최종소유 | 0247 Part344,W378/365,ORef352;0602RID66 | ON&Flag→StartMC04 | 전기전달·현장운전 |
| E13 | Maintenance 두DB | 0237 Contact47/49,Coil36,W43/45/50;0604RID3/6 | Flag를읽어Allarm을별도쓰기 | 현행순서·다른쓰기 |
| E14 | 자동Set/Reset | 0164Part460/W708,0165Part799/W1062,0166Part954/W1075;0577RID33;0578RID30/44/35 | 단계17Reset/24Set/19또는EmergencyReset | 단계시간단위·HMI다른쓰기 |
| E15 | 토크조건 | 0429 Part454/460,W37/476;0658RID46/NID13UID35;0657RID58/276 | OFF조건Set/Reset | deleted/SPARE/활성·실물 |
| E16 | 속도클램프·Mul | 0474Part24/26/27,W43~55;0661RID146/12/16,0662RID149,0664RID145 | 10~100,×272→QW294 | 현행환산·주파수·안전한계 |
| E17 | MC04표시/MV04입력 충돌 | 0526CRef22,W35~39;0678RID472,0675RID42/44,0676RID473/474 | IW324→AmpMC04/OFR | 실제센서·단위·소유 |
| E18 | 선형화·OFR 함수 | 0291Part258/161/190/259/193/23,W21/22/49/252/253;0611Local,0612constants;0014 | 범위/정수연산/ENO, -9999/0 분기 | 실행타입변환·물리정상범위 |
| E19 | PV02는응답소비자 | 0280 OR443,W527/24/31,0607RID51,0609RID87/156 | raw∨DBrun∨Maintenance | PV02전체로직 별도대상 |
| E20 | MC03spare소유분리 | 0246,0604RID259/NID10UID321 | MC04run읽기≠MC04출력쓰기 | spare현행상태 |
| E21 | HOUR Move1 | 0312Part1324/1334/1337,W1362/1363/1364/1366;0615RID148/150,0616RID7/8/12 | MINAdd/HOURMove분리 | 주기·의도·실누적 |
| E22 | HOUR초기화 | 0336Part2831,W2857/2858/2859;0615RID150 | ENO후상수0 | 전원복귀·Tag48조건 |
| E23 | 호출원본 | 0031/0549/0032,0688RID55/58/67/73/82/88 | ON분기와각CRef | 온라인호출·최종쓰기순서 |
| E24 | 기동회로끝점 | FG136/PDF137단자5→FG25/PDF26XS9/10,QS/QM,25KA1→FG24DI1단자12 | Q→릴레이→드라이브 | 실제접점·단자·드라이브상태 |
| E25 | RUN/ALARM/속도 | FG24/PDF25,FG116/PDF117단자7/8,FG112/PDF113단자13/16 | I0.6/I0.7·PAW294 양끝점 | 정상극성·파라미터 |
| E26 | SS10·Reset·STO | FG25/122,FG17/24,FG14/24 | 별도센서·DI4·STO회로 | 현행설치·안전성·리셋전달 |
| E27 | 시공경로·상충 | construction PDF34/51row1_18/59row9_7 | 모터케이블과SS10/MC05표기보존 | 준공/실시공·본체소유 |

## 7.2 필요한 추가 자료

| 누락 | 필요한 자료/수집 위치 | 판정 기준 | 현재 상태 |
| --- | --- | --- | --- |
| G01 | 현행 PLC 프로젝트·온라인비교·승인변경내역 | 이백업과다운로드본·호출·다중쓰기·전원복귀의일치 | live_cpu미수행 |
| G02 | 원본HMI프로젝트/dde.cfg/화면이벤트/MC04호출NID·DB배치 | DB11표시·알람집계·DB2요청이실제어떤신호를읽고쓰는지 | 설정3행/핀만확인 |
| G03 | M09/MC04·24AS1 명판,승인도면·배선·파라미터기록 | 실제모터/드라이브·보호값·DI/RUN/ALARM·AI1 | 도면상경로만확인 |
| G04 | IW324 모듈채널·배선·센서·변경승인 | MV04위치와MC04전류중현행목적 | 상충보존 |
| G05 | SS10 실물·접속함·준공도·OFF현행값 | SPARE/삭제표제/MC05LOC/MC04TO의사용경계 | 설치·활성미확정 |
| G06 | 시간기록기능명세·Tag47/48·현재누적값 | HOUR Move1/초기화의도와실주기 | 정상누적미확정 |
| G07 | 승인된관찰·원인조치·복구기록 | 입력복구·알람Reset·드라이브Reset·재요청·실운전분리 | 수리완료0 |
| G08 | 실제안전회로승인자료·현재리셋경로 | STO상위회로와FlagRESET→A7.4/DI4관계 | 도면부분경로만확인 |

## 7.3 네 기능 반영 제안과 기존 기록 보존

| 기능 | MC04에서 필요한 내용 | dot 수행 상태 |
| --- | --- | --- |
| 도면·래더 비교 | 0247/0428↔FG24/25/116/136,0474↔FG112,0526상충,SS10SPARE | 문서근거만작성;UI코드미수정 |
| 백업·선택복원 | MC04/P08기존키·미지필드·다른설비·미확정·과거기록보존 | 실제데이터복원시험안함 |
| 기록전후비교 | raw/DB/HMI/Q/아날로그/드라이브각각,시각·단위·근거판본 | 기록구조제안만 |
| 보고서/PDF | 7영역·상충·근거·관찰/수리완료구분 | 앱PDF생성/시험안함 |

기존 완료 설비·전체불일치·확인대기·과거설계시험의 상태/집계를 이번 초안으로 바꾸지 않는다. 기존 MC04 문서를 보강할 때도 현재 미확정을 보존하며 시뮬레이터 관련 새 내용·실행을 만들지 않는다.

## 7.4 수행·미실행과 최종 상태

| 구분 | 상태 | 범위 |
| --- | --- | --- |
| documentation | draft_ready | 이MD의7영역·27근거행 |
| static_review | original_sources_reviewed_partial | 핵심XML/선언/핀·실제PDF대조.독립Codex재확인전 |
| ui_records | not_run | 앱화면/저장/복원/보고서미검증 |
| publication | not_published_by_dot | 코드통합·버전·게시담당아님 |
| tia_compile | not_performed | TIA접속/컴파일안함 |
| live_cpu | not_performed | 현재CPU조회/쓰기안함 |
| field_recovery | not_performed | 실측·조치·복구안함 |
| simulator | permanently_stopped | 작성/수정/생성/실행/행동시험0 |

수행 작업은 공개Git 읽기, 문서/CSV/JSON/XML 정적 읽기·노드/선언/핀 추출, PDF 렌더/시각대조, 해시확인, 이 MD 작성이다. 정적 보조 스크립트는 XML 연결을 인쇄할 뿐 PLC 상태전이·타이머 실행·출력 시뮬레이션을 구현하지 않는다. 원본 저장소 생성기/npm/PLC/TIA/시뮬레이터 시험을 실행하지 않았다.

## 7.5 Codex 인계 — 재조사는 핵심 위치로 한정

1. 실제 반영 시 현재 main과 이 초안 고정 커밋의 MC04 관련 원본 차이만 먼저 확인한다. FN06과MC04를동시에중복조사하지않는다.
2. E08~E15: Tag57/T54/S5T5S·공유FAULT/INV·Reset조건·VS01/유지보수분기·자동단계·OFF토크를 재확인한다.
3. E04~E05: Word입력→InputsDB13과호출ENO/NOT Simulation(1)의원본연결을 재확인한다. raw와DB변수는분리표시한다.
4. E16~E18: QW294 SPARE별칭·272곱셈·IW324→AmpMC04/OFR상충을 보존한다. 값/이름을추측으로수정하지않는다.
5. E07: HMI1182미해석바인딩은미확정으로유지한다. 새로확보한선언/실제HMI원본이있을때만그부분을좁혀확인한다.
6. E24~E27: 실제PDF에서Q→릴레이→DI1,RUN/ALARM,PAW294,SS10,Reset/STO·시공끝점을확인한다. 보호값/정상극성/현장복구를자동채우지않는다.
7. E21~E22: HOUR Move1과ENO/초기화를원문그대로표시한다. 의도개선은별도승인주제이며PLC수정을하지않는다.
8. MC04자체근거에맞게UI항목·검색·기록키·PDF를반영/검증한다.다른팬수량을맞추지않는다.코드·공통회귀·버전·완료대장·배포는사용자/지정Codex만담당한다.

## 다음 대상·중지 경계

FN06 초안은 별도 파일로 전달했고, 이번 후속 한 대상 MC04 초안을 작성했다. 최신 사용자 지시대로 MC04 한 개 범위를 유지한다. **VS01 또는 2차133후보로 자동 진행하지 않는다.** FN06/MC04에 새 근거·질문이 오면 필요한 부분만 보강하며 코드 통합·게시 결과를 조사 완료와 혼동하지 않는다.

## 부록: 원본 지문

SHA-256은 이 초안 고정 커밋의 파일 바이트 기준이다. 현재CPU/현장동일성의증거가아니다.

| 경로 | SHA-256 |
| --- | --- |
| docs/equipment-standard/INVENTORY.json | 720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc |
| docs/equipment-standard/WORK-STANDARD.md | 05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99 |
| docs/equipment-standard/WORK-ITEM-TEMPLATE.md | 4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586 |
| .agents/skills/gme-equipment-rollout/SKILL.md | fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b |
| all-in-one/sources/Electrical_Rev2.pdf | 5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6 |
| all-in-one/sources/PID_1684n002I.pdf | 2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b |
| all-in-one/sources/Electrical_Can_Decoating_20241118.pdf | 3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd |
| all-in-one/sources/hmi_plc_tags.csv | a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404 |
| all-in-one/registers/equipment-hmi.csv | 2cdce600aa0138cc5025022e57d9d61a948afb237f70c70e2d11e8300e73286a |
| all-in-one/registers/plc-symbols.csv | a0334b390f06ddb515d6c09ca96a01d35d44029c1b726ef0ff53303ec04ff91f |
| all-in-one/procedures/MC04.html | cae4342692a2b1945dd8a886aeb7c53ec19f01c4f5b24bef764361002d81be4e |
| all-in-one/sources/decoded-original/0014-FlgNet.xml | 2e814adbaac6bab99bc668bfdab74f0fc90576324d0b88728951683869cfac30 |
| all-in-one/sources/decoded-original/0030-FlgNet.xml | 9252c9da764993de1edb8b2e44c46d6e9f9d4b6118e751a0dbeaa9ffd8ea721b |
| all-in-one/sources/decoded-original/0031-FlgNet.xml | 76385eab8f8f72b9faa16f7cf8905f395591b18c0a9ee9e6d7dd085a38c45c65 |
| all-in-one/sources/decoded-original/0032-FlgNet.xml | 070bb8efa33d03b18add5da81d3f670a47c12b288076b7bfee11ac87fe6fa7e4 |
| all-in-one/sources/decoded-original/0164-FlgNet.xml | 15884b2b362842279b626b669a484b1daa269f5ecd99112b8391bb0387382491 |
| all-in-one/sources/decoded-original/0165-FlgNet.xml | 4513a5f6e77717c99c5e869105483be31f7f62ab280e271dc36cd7a2d3e3bb88 |
| all-in-one/sources/decoded-original/0166-FlgNet.xml | 0330a505877be92172f94bce83222a0bfc8d64aab700a69fc1fa2188010d3853 |
| all-in-one/sources/decoded-original/0237-FlgNet.xml | ad3721660c2f357e76c1a351f7898691271f35c341efe775e5780d749b2c4aa0 |
| all-in-one/sources/decoded-original/0246-FlgNet.xml | 2b1bf0644447f15640214b451281aa3fa5389505936f2a6a1078a9508dfc9f04 |
| all-in-one/sources/decoded-original/0247-FlgNet.xml | 104690938ac2ebe32d668f237255a3e957e0af9930bfc6587b9e6624bedf13a1 |
| all-in-one/sources/decoded-original/0280-FlgNet.xml | 77f1860b8424319efcd8fa058eac4177fb6ba24d84d01d690c0e3c361a19f3ca |
| all-in-one/sources/decoded-original/0291-FlgNet.xml | fe0b92f074eba25148ce34084649af3d968962558d652727f1eea19f3e3c2550 |
| all-in-one/sources/decoded-original/0312-FlgNet.xml | c871fcc3e52da6fdc937f4891428750ee644e2f545df772f22e2efdbefce9122 |
| all-in-one/sources/decoded-original/0336-FlgNet.xml | 1be4f76dba11e6cceea057743c8b15b8a4bea4edfe87c19ef0581d7b65ffe56a |
| all-in-one/sources/decoded-original/0355-FlgNet.xml | 73592d33f8b3a71effeb36f25427c76e931485e7ce31f5c81f144ddae83c4247 |
| all-in-one/sources/decoded-original/0361-FlgNet.xml | 485836309d8e52ddf1f6937fba80bd405a6d36363c95e71b0f24491f8cd7a04c |
| all-in-one/sources/decoded-original/0397-FlgNet.xml | bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834 |
| all-in-one/sources/decoded-original/0428-FlgNet.xml | cb7015f543d0deb26fe0bf23d045dc787b7c9cbc3d02c2c5623c0283709fa69a |
| all-in-one/sources/decoded-original/0429-FlgNet.xml | 092dd3ac8f08d5934b6ffdd27e3b649a06e23c3b95900f70aadb0e1d4f592572 |
| all-in-one/sources/decoded-original/0474-FlgNet.xml | a706b93232fdc7449a43265c3b953a3180fde5e5b46b05915ca8db7f4327ee4d |
| all-in-one/sources/decoded-original/0526-FlgNet.xml | 9cdd52426bf6bc8a8b49a5a292be30d8dcfe854e3f72ef2654ab60d63ecb4bda |
| all-in-one/sources/decoded-original/0549-FlgNet.xml | 49f7169c33ed7f54559b0801e21a7d618584900972840e91cf51ad032e8febb1 |
| all-in-one/sources/decoded-original/0067-IdentXmlPart.xml | 0aa469d4f7a20bde2a5bccc6c91b3d9c48929460bd68ef32e0217d53f4d68628 |
| all-in-one/sources/decoded-original/0558-IdentXmlPart.xml | 45d49d53b6b41312960bb2a329663e87d8803e28d7832308424a6bf5091e6d1b |
| all-in-one/sources/decoded-original/0577-IdentXmlPart.xml | 511e01fae619dc385357908a1ac62030dbdfd5f5399bd4c22bc58bebbfc3bf47 |
| all-in-one/sources/decoded-original/0578-IdentXmlPart.xml | 0f9f41b5dee25ea17c7a29ab6f7b00503c13d0f265266acd660072baf061d32b |
| all-in-one/sources/decoded-original/0602-IdentXmlPart.xml | 46ab21151eddaaf616469db520730c60423eb742aa491af194e6710c751b4caf |
| all-in-one/sources/decoded-original/0604-IdentXmlPart.xml | b798d29c5499b5314a1ee3cff9139dae64c887533b86baa43b6e9a052373a6af |
| all-in-one/sources/decoded-original/0607-IdentXmlPart.xml | 9b76b53536a26e7b45961fecbf825ae1552e16c2fd9af5736864193c01d77f93 |
| all-in-one/sources/decoded-original/0609-IdentXmlPart.xml | 395de8ebb2168848cf96fe015bd7334d71107c114a4e441ef36346b8f22031db |
| all-in-one/sources/decoded-original/0611-IdentXmlPart.xml | 0d583915a261703954da22c176ba9f81338ad13ea2810e7cd5f7de8aa1bfa089 |
| all-in-one/sources/decoded-original/0612-IdentXmlPart.xml | 95b545d4964d371ebfc107894ea90b8b1d0d7ab5d3a70e643f8ce539063c0f38 |
| all-in-one/sources/decoded-original/0613-IdentXmlPart.xml | 09d3b1397a987898334218f37e025661af162438582e649f671e7abec443d3cb |
| all-in-one/sources/decoded-original/0615-IdentXmlPart.xml | 80f4544edca56c6e6bb2713c758c92ade9202255110074931e03fe34d0d0801a |
| all-in-one/sources/decoded-original/0616-IdentXmlPart.xml | 650b53354a0c8443d94adc5bd6a860d3c5313014a52e0fb98a5656a65b58cc0d |
| all-in-one/sources/decoded-original/0621-IdentXmlPart.xml | a63e2b97ea9eb2691cb478666afed77fc58a2da2f8170422dc09e24b102c88ee |
| all-in-one/sources/decoded-original/0623-IdentXmlPart.xml | 4acd00406ea92466169e57e59fc90b0da4d9ec55fd19e2e96c9556e939cb83a6 |
| all-in-one/sources/decoded-original/0624-IdentXmlPart.xml | 24607c0827fbde428bccf8637ef4ae490798a69a7c2f3b87861d0749082d367a |
| all-in-one/sources/decoded-original/0627-IdentXmlPart.xml | 08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb |
| all-in-one/sources/decoded-original/0628-IdentXmlPart.xml | 9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd |
| all-in-one/sources/decoded-original/0629-IdentXmlPart.xml | 67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972 |
| all-in-one/sources/decoded-original/0655-IdentXmlPart.xml | 38e9f323024fba19582b473f39b1ed03ffe6a0b390218894029a6edb0b1ff9fb |
| all-in-one/sources/decoded-original/0656-IdentXmlPart.xml | 0dbc45e84732a8848f17b094ea08ab8578dbf240bfe15cd7086859395c27c592 |
| all-in-one/sources/decoded-original/0657-IdentXmlPart.xml | 0f70cda60a6b1a17175876d58e25b2686952642de6cffb21213aeef8b347a22b |
| all-in-one/sources/decoded-original/0658-IdentXmlPart.xml | 998294c0c8a99e00ceb33c2c60def2cd4850e34328917ae506244c2be2df3831 |
| all-in-one/sources/decoded-original/0661-IdentXmlPart.xml | 90672199fee355011f581d3287046894772f3f3b4cb78bbe0dd0d71bd488ac93 |
| all-in-one/sources/decoded-original/0662-IdentXmlPart.xml | 1838040bfee800fdb3f13b126eaf69a9d178b17cecc0d59ae03e9185216a48a5 |
| all-in-one/sources/decoded-original/0664-IdentXmlPart.xml | 68c614e1c6a7fcadeee3f0b2ddc54910c3b337e66074d7a113b9cbc834c271ed |
| all-in-one/sources/decoded-original/0672-IdentXmlPart.xml | 6bfc2ba142d6270c39eb1f13b2886204865af6d46eadc5f410c26981b8da9222 |
| all-in-one/sources/decoded-original/0675-IdentXmlPart.xml | b1902886927d8403fab736d9c8ffe73f2fbc8ce4b7ca7c345144964668b051c3 |
| all-in-one/sources/decoded-original/0676-IdentXmlPart.xml | c58427c5b0ac6c11cdb52e4c6d0461c7b191fae81ccace191048e9f175fcec59 |
| all-in-one/sources/decoded-original/0678-IdentXmlPart.xml | 51e637e0b9713c028810f2a717b5c3804a3a26c2f1be7e332a4d6bf277bfc382 |
| all-in-one/sources/decoded-original/0688-IdentXmlPart.xml | ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda |
| all-in-one/sources/decoded-original/0692-IdentXmlPart.xml | bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037 |
| all-in-one/sources/decoded-original/0694-IdentXmlPart.xml | 757ccebdf32d0a168dd787bfa735fe6494eac4c4a9f7a5adc63898a88e8b152d |

초안 저장: 2026-10-11T05:46:43.996693+00:00 (UTC).
