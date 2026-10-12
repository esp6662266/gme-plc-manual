# CLIENT-CL06 · Belt conveyor B · 자체 원본 조사 초안

고정 원본 `source-mv06`, commit `abcf31c5030bc7ef8749ed8e869a857f2387a28a` / v1.12.0. 문서 조사 완료·자료 공백 유지. 로컬 기능 통합·게시·현장 완료를 의미하지 않는다.

## 1 설비·자료 기준

### 핵심 확인 / 상충 / 누락

- 독립 확인: RUN I13.0, FAULT I15.3, 경보 DB3.DBX14.6, 시간 DB9.DBW20/22, 고유 FC9 NID6 및 FC2 NID6/48의 Part/Wire/ORef/선언 결속.
- 실제 전기 렌더: FG89/PDF90, FG92/PDF93, FG129/PDF130, FG131/PDF132. RUN X1:294/295→모듈 단자11, FAULT X1:332/333→단자34.
- 출력 `start client motor 6` Q61.3은 백업 심볼 자료만 확보했다. 실행 쓰기·기동 허가·릴레이·외부 전력경로를 확보한 것으로 확대하지 않는다.
- 상충: live_index doc520의 RUN comment는 과거 `e 13.5`, 실제 Address는 I13.0. doc538 FAULT comment는 `e 18.3`, 실제 Address는 I15.3. 둘을 임의 수정·병합하지 않는다.
- 시간 HOUR는 ADD 누적이 아니라 **Move 1**이며 별도 NID48에서 0으로 쓴다. 장기 운전시간 저장 완료로 표현하지 않는다.
- 자료 누락: 외부 Belt conveyor B 제어반 내부 회로/프로그램·실물 식별·케이블 및 상대단자·HMI 이벤트·현재 CPU/정상극성/현행 보호설정·현장복구.

### 대상과 공유 근거 경계

`docs/equipment-standard/INVENTORY.json#/catalog/62`의 CLIENT-CL06, kind client, 외부 연동, phase2, parent 없음이 대상이다. 배정 scope의 aliases는 motor_client_06, client motor 6, cl06, belt conveyor b다. 이 이름은 공압 CYL-CL의 번호 공간과 다르므로 CL06이라는 이유로 실린더 또는 P&ID 기기를 병합하지 않는다. 주변 CLIENT-CL05/07 및 부모/하위 설비는 완료로 합산하지 않는다. 물리 실물 동일성은 미확정이다.

앞선 `CLIENT-CL04-DOTS-DRAFT.md`는 공통 FC9/FC2 호출, T13, HMI Word 복사 및 누락 경계의 인덱스로 재사용했다. `SYS-ALARM-DOTS-DRAFT.md`, `SYS-RUNHOURS-DOTS-DRAFT.md`, `SYS-PLC-IO-DOTS-DRAFT.md`는 공통 경보 집계·저장 핸드셰이크·입력 미러 상세의 연결 참고다. 본 채널의 0225/0297/0333과 선언, CSV 및 4쪽 전기 끝점은 직접 원본으로 다시 확인했다. 인덱스나 이전 채널의 숫자를 고유 증거로 복제하지 않았다.

이하 XML 경로 약기는 `all-in-one/sources/decoded-original/` 기준이다. live_index와 network-map은 탐색용 파생 자료이며 고유 제어식은 FlgNet+IdentXmlPart 원문으로 대조했다. 고정 백업의 선언시각은 현재 운전 프로젝트나 실물 구성의 증명이 아니다. 모델 런타임 증명 미확인. 원본코드·시뮬레이터·PLC·보호값·SEJIN·운영 기록 변경 및 실행 없음.

## 2 I/O와 HMI

|신호|고유 선언과 사용 문맥|주소·형식·해석|
|---|---|---|
|BELT CONVEYOR B RUN|0613 RID38 Global, NID6 UID370, SSD AO104, SAD Input SAM=None|I13.0 Bool 입력영상. 벨트가 실제 이동함을 독립 증명하지 않음|
|BELT CONVEYOR B FAULT|0599 RID16 Global, NID6 UID143/145, AO123, Input SAM=None|I15.3 Bool 입력영상, 정상극성 미확정|
|Allarm.motor_client_06_fault|0601 RID17 Global Bool AO118 BAD4→0600 RID4 TOD3; NID6 UID144/147 Write|DB3.DBX14.6, S/R 내부 유지경보|
|Flag.RESET_ALLARM|0601 RID7 Global Bool AO48 BAD6→0600 RID6 TOD2; NID6 UID146|DB2.DBX6.0 내부 Reset. HMI 버튼 자체가 아님|
|ON|0599 RID1 Global Memory AO0, NID6 UID142|M0.0 Bool. 이름을 true 상수로 치환하지 않음|
|CLIENT_MOTOR_6_MIN|0615 RID40 Global Int AO160 BAD5→0614 RID5 TOD9; NID6 UID371/373/374/379|DB9.DBW20, ADD 및 Move0 대상|
|CLIENT_MOTOR_6_HOUR|0615 RID42 Global Int AO176 BAD5; NID6 UID377, NID48 UID2653 Write|DB9.DBW22, Move1/Move0 대상|
|Tag_47 / Tag_48|0613 RID1 Timer AO13 / RID284 Timer AO17|T13 / T17. HMI 태그가 아닌 PLC 타이머|
|Flag_Aggiorna_DB|0613 RID13 Global Bool Memory AO15, NID6 UID380 Write|M1.7, 시간 갱신 플래그 Set|
|start client motor 6|live_index `_7ev` doc481, Name/Address/Datatype/Comment|Q61.3 Bool, comment `it should be free but it is used`; 실행 writer/단자 미결속|

고유 변수는 Global, 수치1·60·0 및 S5T#1M은 Constant다. 같은 RID/UID라도 블록·NID가 다르면 다른 문맥이다. 다른 장치 FB의 Local 핀을 CL06 선언으로 연결하지 않았다.

### RUN의 HMI 전달

`all-in-one/sources/hmi_plc_tags.csv`: `BELT_CONVEYOR_B_RUN`, 주소 `DB13,X13.0`, Access Name PLC, 내부 ID00400. 이는 설정 주소이며 현재 통신·실제 표시값·화면 이벤트는 미확정이다.

0397-FlgNet, HMI inputs doc1070 NID1: rail W21→Move60.en, ORef63/RID19→W70→Move60.in, out1 W72→ORef64/RID20. 0627 RID19 Tag_183은 Global Word, Input AO96, SAM=None=IW12. 0629 RID20은 Global Word AO96 BAD4→0628 RID4 TOD13=DB13.DBW12다. 따라서 **IW12 전체 Word를 DB13.DBW12로 복사**하며 바이트13의 I13.0도 포함한다. 별도 Bool 코일 또는 PIW 직접접근으로 바꾸지 않는다. Move60.eno W71→Move61.en도 유지한다. 상위 FC15 호출 및 스캔 최종값/복수 writer 완전성은 공통 자료의 미확정 경계다.

같은 CSV의 `Allarmi_119`, `DB3,X14.6`, ID00116은 위 내부 유지경보와 같은 주소다. 이름119는 외부 고장코드나 입력번호가 아니다. 이번 CSV에서 DB9 직접 태그는 없었다. 운전시간 화면 누적 처리·Q61.3 버튼·스크립트/쓰기 이벤트·권한은 확보하지 못했다. Q→DB14 공통 미러를 기동 writer로 바꾸지 않는다.

## 3 제어 구조

### 상위 호출

0549-FlgNet Main doc1620 NID7: rail W352→Contact350.in; ORef335/RID52 ON→W348→operand. 0692 RID52는 M0.0. Contact350.out W351은 CRef331.en과 CRef334.en 등으로 병렬 분기한다.

- CRef331 RefId80 안의 CodeBlock345 RefId79. 0688 RID79 `Motor/Alarm Client`, TOD9 FC, NID7 UID345 Call; 0694 RID80 NID7 UID331 TORID79.
- CRef334 RefId83 안의 CodeBlock347 RefId82. 0688 RID82 `time work motor`, TOD2 FC, NID7 UID347 Call; 0694 RID83 NID7 UID334 TORID82.

두 호출은 앞 FC의 ENO에 직렬 종속되는 배선이 아니다. 백업 Main 허가 구조만 확인했으며 실제 CPU 스캔주기·기동 시퀀스는 미확정이다.

### CL06 운전시간 가지: 0297-FlgNet, doc1007, FC2 NID6

1. rail W402→Contact398.in. ORef369/RID1 T13→W381→398.operand. 398.out W399→Contact400.in. ORef370/RID38 RUN I13.0→W382→400.operand.
2. 400.out W401은 Add352.en 및 Ge359.pre로 병렬 분기한다. Add352 SrcType Int: in1 W383/ORef371/RID40 MIN, in2 W384/ORef372/RID7 Int1, out W385/ORef373/RID40 MIN. 이 가지는 MIN := MIN+1.
3. Ge359 Int: in1 W386/ORef374 MIN, in2 W387/ORef375/RID8 Int60. out W388→Move362.en.
4. Move362.in W390/ORef376/RID7=1, out1 W391/ORef377/RID42=HOUR. 즉 HOUR := 1이며 HOUR+1이 아니다.
5. Move362.eno W392→Move365.en. in W393/ORef378/RID12=0; out1 W394/ORef379/RID40=MIN. Move365.eno W395→SCoil368.in; operand W396/ORef380/RID13=M1.7. ENO 체인과 플래그 Set을 생략하지 않는다.

상수는 0616 RID7(Int1), RID8(Int60), RID12(Int0)로 직접 확인했다. RUN 신호의 사용은 시간계수이며 이것만으로 모터 기동/정지 제어를 확보했다고 쓰지 않는다.

### 공유 타이머와 고유 HOUR Reset

0019-FlgNet FC2 NID58(doc1056): Contact3120 operand는 NOT T13(ORef3115/RID1/W3118), out W3121→SdCoil3112.in. value W3117/ORef3114/RID335=0616 S5Time `S5T#1M`, 인코딩 V5632. operand W3119/ORef3116=T13. 공유 분 타이머이며 CL06 무응답 고장 지연이 아니다. 실제 시간 정확도는 검증하지 않았다.

0333-FlgNet FC2 NID48(doc1046): ORef2651/RID284=T17→W2662→Contact2677. rail W2679와 Contact2677.out W2678→Move2636.en. in W2663/ORef2652/RID12=0, out1 W2664/ORef2653/RID42=HOUR(DB9.W22). 이 고유 가지가 HOUR := 0을 쓴다. Move2636.eno W2665는 다음 채널 Move2639.en으로 이어진다. 다른 채널은 이번 완료 범위가 아니다. T17/M1.7의 외부 저장·ACK는 공통 SYS-RUNHOURS 경계를 참고하며 백업 HOUR 0/1만으로 장기 저장 성공/분실을 확정하지 않는다.

### 실행 출력의 공백

IdentXmlPart 181개에서 CL06 명명 경계를 검색했고 고유 선언 원문5개를 확보했다. `start client motor 6`의 직접 XML 선언/쓰기 문맥을 못 찾았다. Output AO491(Q61.3) 및 Word 범위 후보 AO480/488의 선택 검색도 결속 0건이다. 이 결과는 절대주소·간접쓰기·블록 복사·외부 통신 writer 전체 부재 증명이 아니다. 기동/정지·수자동·허가·인터록의 전체 원문과 외부 제어반이 필요하다.

## 4 전기 전달 경로

`all-in-one/sources/Electrical_Rev2.pdf`를 실제 PDF90/93/130/132로 렌더해 고유 끝점·접점 기호·footer를 눈으로 확인했다. **네 페이지 각각 Rev2 17.03.2025, DATA 27.05.2024**다. 파일명만으로 개정란을 채우지 않았다.

|범위|직접 확인 끝점과 원본 위치|한계|
|---|---|---|
|RUN 외부 접점|FG89/PDF90, BELT CONVEYOR “B” RUN: +24Vdc10.7→5x20 2A F 퓨즈 표기 X1:294→선89.1→열린 접점 기호→X1:295→E13.0 /129/2|상대제어반 단자·접점기기번호·케이블번호/규격 미확보|
|RUN PLC 입력|FG129/PDF130: E13.0 상호참조89/1→입력 단자11. CPU515 / MOD11 표기|도면 표기이지 현재 CPU·설치 확인 아님|
|FAULT 외부 접점|FG92/PDF93: +24Vdc10.7→5x20 2A F 퓨즈 표기 X1:332→선92.5→열린 접점 기호→X1:333→E15.3 /131/4|외부 보호회로·접점의 정상상태/극성 미확정|
|FAULT PLC 입력|FG131/PDF132: E15.3 상호참조92/7→입력 단자34. CPU515 / MOD11|고유 고장코드·내부 트립원인 미확정|
|입력모듈 보조전원|FG129: +24Vdc10.7→X21:3012의 5x20 2A IST.→129.1→단자19; -0Vdc10.6→단자20. FG131: X21:3013→131.1→단자39, -0Vdc10.6→단자40|도면 정격만 기록. 현행 퓨즈/보호값 또는 변경 권고 아님|
|기동 출력|Q61.3은 심볼 자료. OEM 텍스트의 A61.3/CL06 고유 기동회로 미식별|출력모듈·릴레이 A1/A2·부하접점·단자·컨택터·외부 모터전력·보호기 미확보|

이 네 페이지의 관련 범위는 SPARE 점선으로 표시되어 있다. 이름과 백업 선언만으로 현재 실사용을 확정하지 않는다. 열린 접점 기호는 실제 정상극성·정전시 안전상태·고장접점 동작의 증거가 아니다. 이 범위는 릴레이 부하5/9 또는 하단접점표1/5/9를 판정하는 회로가 아니므로 다른 도면의 접점번호를 끼워넣지 않는다. 시공도/외부제어반 도면의 고유 경로와 현장 명판은 이번에 확보하지 않았으며 도면 전체 의미검토를 주장하지 않는다.

## 5 알람·복구

0225-FlgNet doc415, Motor/Alarm Client FC9 NID6의 직접 원문:

- ON ORef142/RID1→W148→Contact157. rail W165→157.in, 157.out W158이 Set/Reset 가지로 분기.
- Set: I15.3 ORef143/RID16→W149→Contact159. 159.out W160→SCoil136.in, operand W151/ORef144/RID17=DB3.X14.6. 발생식은 ON AND FAULT.
- Reset: I15.3 ORef145/RID16→W152→Contact161(operand Negated). out W162→Contact163.in. RESET_ALLARM ORef146/RID7→W153→163.operand. out W164→RCoil141.in, operand W155/ORef147/RID17=같은 경보. 해제식은 ON AND NOT FAULT AND RESET_ALLARM.

이 고유 알람 네트워크에는 타이머 Part가 없다. RUN=0이나 타 장치의 3초/5초 무응답 지연을 추가하지 않는다. 원인이 참이면 위 Reset 조건이 성립하지 않는다. 원인 소멸·PLC 래치 해제·HMI ACK·외부제어반 Reset·재기동·현장복구는 각각 다르다.

HMI Allarmi_119 주소 결속은 확인했으나 실제 표시 문자열·이력/소리·ACK 이벤트는 확보하지 못했다. 공통 DB3 집계·Reset 생성은 SYS-ALARM 연결 근거를 따른다. 이 한 비트가 외부 Belt conveyor B를 직접 정지시키는 실행 writer는 확인하지 못했으며 정지 인과를 발명하지 않는다.

## 6 증상별 읽기 전용 관찰

현장 조작법이 아니라 담당자가 제공할 관찰 자료를 비교하는 기준이다. 강제출력·바이패스·보호값 변경·활선 측정·Reset 실행을 제안하지 않는다.

|증상|동일 시각에 확보할 값/위치|비교 기준·판단 한계|
|---|---|---|
|시작 표시인데 벨트 정지|HMI 화면/이벤트, Q61.3과 writer, 외부 제어반 상태, I13.0, 프로젝트 판본|심볼 이름만으로 전력 출력과 결속하지 않음. 기동허가·상대회로 필요|
|외부 운전중인데 HMI RUN 없음|I13.0, IW12, DB13.W12/X13.0, ID00400와 통신시각|FG89 X1:294/295·FG129 단자11과 Word 복사 분리. 단선/통신/극성 중 하나로 단정 금지|
|외부 고장 해소 후 경보 유지|I15.3, M0.0, DB2.X6.0, DB3.X14.6, Allarmi_119|0225의 래치·NOT FAULT·Reset 조건 비교. 원인 소멸만으로 자동 Reset 식 아님|
|Reset 요청 후 계속 유지|HMI 요청/소비 로그와 내부 Reset 전후, FAULT 시각|HMI ACK와 PLC Reset 및 외부제어반 Reset 구분. 반복 재기동을 복구 증거로 쓰지 않음|
|운전시간 증가 없음 또는 1 유지|I13.0,T13,DB9.W20/W22,M1.7,T17,외부 저장내역|0297 MIN+1/HOUR Move1·0333 HOUR Move0를 구별. 시간 정확도·저장 성공 미확정|
|도면과 설명 주소 상충|현재 프로젝트 식별·I13.0/I15.3·X1/모듈 표찰·외부회로 판본|과거 comment e13.5/e18.3와 실제 Address를 별도 보존. 임의 배선/프로그램 변경 금지|

기록 필드는 관찰자, 실제시각/시간대, 위치/장치, 값/단위, 프로젝트·도면 개정, 사진/로그 출처, 비교결과, 미확정 사항이다. 이번에는 실제 운영/SEJIN 기록·사진을 복제하거나 작성하지 않았다.

## 7 완료·누락과 검증

|영역|문서 상태|남은 조건|
|---|---|---|
|설비·자료|적용, ID/별칭 경계 작성|실물 동일성·현재 설비명 미확정|
|I/O·HMI|적용, 입력/경보/시간·CSV 결속|Q61.3 writer·HMI 이벤트·현재 통신 미확보|
|제어|적용, FC9/FC2 고유 핀 검토|기동/정지·외부시퀀스·간접쓰기 전체 미확인|
|전기|입력 두 경로 4쪽 직접 렌더|출력·외부반·케이블·실물 미확보|
|알람·복구|고유 S/R 확인|ACK·외부Reset·현장복구 미확인|
|증상 관찰|읽기전용 비교기준 작성|현장 관찰값 미취득|
|완료 기준|문서와 구현/현장 분리|BC01 동등 기능·게시 완료 아님|

추가자료는 외부 Belt conveyor B 제어반 회로/프로그램·기동 허가표, 현행 GME Q61.3 교차참조(절대/간접/통신 writer 포함), X1:294/295/332/333 상대단자·케이블표, HMI 이벤트/스크립트, 설비 명판 및 RUN/FAULT 정상상태 증거다. 새 자료 없이 동일 실물 보류를 반복 조사하지 않는다.

백업 미리보기/선택복원, 기록 전후비교, 관찰보고서/PDF의 본 ID 전용 구현·저장/재읽기·화면재열기는 이번 조사에서 수행하지 않았다. 기존 note/repair_observation·미지필드·초안·저장키·다른 설비 기록은 불변이다.

최종 상태: documentation `complete_with_gaps`, static_review `selected_original_xml_and_pdf_reviewed`, ui_records `not_run`, publication `not_published`, tia_compile/live_cpu/field_recovery `not_performed`. 독립 부모 검토·첨부 대기. 현행 CPU·실물·극성·보호값·현장복구를 추정해 채우지 않았다.

### 실제 검토 범위

0225와0297 고유 전체 Part/Wire, 0333 CL06 HOUR Reset 가지, 0397 IW12 Word 전달, 0549 FC9/FC2 호출, 0019 공유 T13 및 선택 선언을 의미 대조했다. 181개 IdentXmlPart 명명검색은 경계 탐색이며 181개 전체 의미검토가 아니다. 4쪽 전기 렌더를 직접 확인했다. 아래 선정 원본 해시·Git blob 내용 비교는 byte 보존 검사이며 전체 내용의 의미검토 수와 같지 않다. 원본 생성기/build/test·시뮬레이터·TIA는 실행하지 않았다.

작업 실제시각(UTC): 배정 지시 읽기 2026-10-11 12:22:40 이후; 전기 4쪽 렌더 시각확인 12:23:44; 선언/핀·HMI 선택 대조 종료 12:24:38. 완료시각은 아래 검사에 추가한다. 산출물은 본 초안과 `../extracts/CLIENT-CL06/`의 원형발췌·선정검색·검사JSON뿐이다.

### 선정 원본 SHA256 + 고정 Git blob 전체 표

경로는 source-mv06 기준. Git blob은 고정 commit의 object ID이며 내용 일치는 로컬 byte와 해당 blob byte의 직접 비교다.

|원본 경로|SHA256|고정 Git blob|내용 일치|
|---|---|---|---|
|`AGENTS.md`|`0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2`|`073164bc6efd5791032d62c71b03b4dab48cb6f8`|일치|
|`.agents/skills/gme-equipment-rollout/SKILL.md`|`fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b`|`9aa820ea6ca15b4e136c9772423b78ed4df6a3d4`|일치|
|`docs/equipment-standard/WORK-STANDARD.md`|`05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99`|`f76a570cc73098632e08759b17934000f7e3a253`|일치|
|`docs/equipment-standard/WORK-ITEM-TEMPLATE.md`|`4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586`|`e546f39535d2b589e80f97db869ac37ce4d05cfd`|일치|
|`docs/equipment-standard/INVENTORY.json`|`720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc`|`587c3748ad9224718f95ba06463fee913dae231d`|일치|
|`VERSION.json`|`5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7`|`fffb51663b7705aec91cb119ca80ee943a4ce758`|일치|
|`WORKSPACE-HANDOFF.md`|`215096d997782e78e901dfae36c782937e49611fbeb677a0d3fa50cbecf8d074`|`dd0b8989d2376c4415bba9bd826fe6754c6b1a12`|일치|
|`PUBLICATION_STATUS.md`|`efe4857aec598d90470322cf3962eb3fe1f64947630e1fdf71d1c90134de8740`|`d76401cf291fc0be681acc51fa898ad3ce46ff78`|일치|
|`all-in-one/ACTIVE-WORK.md`|`eff3bbc08ecff41da3beff77f3fec48e7d148708192bcaaab00f34b6a721afc2`|`6eb947c629b5ddf9c759ef87649451303938864b`|일치|
|`EXPANSION-WORK.md`|`ec624de9fd2fcfac861a67fd5e828b25ef46db50bfd7a37ff16e2cb54cd0f7e2`|`4c42d88ecc2d48269eb23e13a20ebf3721a092a1`|일치|
|`all-in-one/sources/Electrical_Rev2.pdf`|`5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6`|`f610fd7c7ce14ae951b00cff57b969259bfb389d`|일치|
|`all-in-one/sources/hmi_plc_tags.csv`|`a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404`|`cf4c0650e7c7baac350dcb89909b808435704880`|일치|
|`all-in-one/sources/live_index.json`|`14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1`|`e35ccea1f841349c632666c29954b7bcd4f5839e`|일치|
|`all-in-one/sources/decoded-original/network-map.json`|`c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60`|`424430b6b953e43138e5d0a18ca40c949e21cfa1`|일치|
|`all-in-one/sources/decoded-original/0019-FlgNet.xml`|`a3301f4d07c2d36aefa6faa6c3559a1cff4565fc6de40cd17e54b548b30c0ce5`|`f78cfdbf5e717304114660ffbd3bb42cbed6d79d`|일치|
|`all-in-one/sources/decoded-original/0225-FlgNet.xml`|`9573adcd78d2bee51e36dddf664b9dd57656ffaa5bc3ba101c4f6f558f6a23eb`|`2a3a310f3954104c857e5449b4f3846cb6171f7f`|일치|
|`all-in-one/sources/decoded-original/0297-FlgNet.xml`|`cda29a4baea32238fc7023eda23d278b383078775a63129bd96c528f197676fc`|`6379510e517f6fe91083a879fcbbf34e757dac11`|일치|
|`all-in-one/sources/decoded-original/0333-FlgNet.xml`|`4031a340e2cf8e008bcf602413e0b71e067891985f0bd3befd7c23ff24cc0483`|`847746715ac2603cc6b84919e3f616073090f332`|일치|
|`all-in-one/sources/decoded-original/0397-FlgNet.xml`|`bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834`|`4ab8370493c4e28fc1eabeeebe2743d27f0c4021`|일치|
|`all-in-one/sources/decoded-original/0549-FlgNet.xml`|`49f7169c33ed7f54559b0801e21a7d618584900972840e91cf51ad032e8febb1`|`985b5310b43b1015b5dee286aa0e42800564b94b`|일치|
|`all-in-one/sources/decoded-original/0599-IdentXmlPart.xml`|`32a693fe12134febbd9f5c7da10c3469ef4d5b164ab8b6bd9ea3867c358936c1`|`493de77fc827d8f14192ced05d82df3a062f7965`|일치|
|`all-in-one/sources/decoded-original/0600-IdentXmlPart.xml`|`20c58ee0383d0b6c275bd2d96abd30af7c5d1f3fff59c7d5034cd758936b57d5`|`f22a7ededd0576cf379ee19908da067f08d45412`|일치|
|`all-in-one/sources/decoded-original/0601-IdentXmlPart.xml`|`04c9481f7381284de689ef5c7ff40d7aea93f2004cd877a4e4f27e47baa6d862`|`07bcf656fa58e4a305999456644acd24b3dc6bec`|일치|
|`all-in-one/sources/decoded-original/0613-IdentXmlPart.xml`|`09d3b1397a987898334218f37e025661af162438582e649f671e7abec443d3cb`|`c9d19a48e947098914f4d2de3348c05b4f6d37e8`|일치|
|`all-in-one/sources/decoded-original/0614-IdentXmlPart.xml`|`c6de26f74d75f5be858a406de75eaf6faf62ba9b89c8f9a085b5dd206e93d294`|`da0485aa033700f08c8695d30b93ebd2d377d6c7`|일치|
|`all-in-one/sources/decoded-original/0615-IdentXmlPart.xml`|`80f4544edca56c6e6bb2713c758c92ade9202255110074931e03fe34d0d0801a`|`49eb86fe01feb83de8c0864b21493d305aff8b20`|일치|
|`all-in-one/sources/decoded-original/0616-IdentXmlPart.xml`|`650b53354a0c8443d94adc5bd6a860d3c5313014a52e0fb98a5656a65b58cc0d`|`9f7fdd5f93ac149c139a054ebb34f63c632ef7fd`|일치|
|`all-in-one/sources/decoded-original/0627-IdentXmlPart.xml`|`08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb`|`61ebc0abbb2ca160e11e1da400a3f14a397d8bc5`|일치|
|`all-in-one/sources/decoded-original/0628-IdentXmlPart.xml`|`9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd`|`170ca5c72599edc7ea7eefe651c3680ce325e76a`|일치|
|`all-in-one/sources/decoded-original/0629-IdentXmlPart.xml`|`67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972`|`058129bb01e27f7a6a0d0293f332d745e5bab74e`|일치|
|`all-in-one/sources/decoded-original/0688-IdentXmlPart.xml`|`ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda`|`463585759f1ecd94f32362b4fefb000a152f5773`|일치|
|`all-in-one/sources/decoded-original/0692-IdentXmlPart.xml`|`bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037`|`737785d03b5fad43c5b4d451955726d800edb1c0`|일치|
|`all-in-one/sources/decoded-original/0694-IdentXmlPart.xml`|`757ccebdf32d0a168dd787bfa735fe6494eac4c4a9f7a5adc63898a88e8b152d`|`c45e8f3ca4129dc06734f6a12ef79e6ed6528a7d`|일치|

선정 33개 원본의 byte/Git 내용 일치. 초안 작성·해시검사 완료 실제시각: 2026-10-11T12:27:19.964870+00:00.
