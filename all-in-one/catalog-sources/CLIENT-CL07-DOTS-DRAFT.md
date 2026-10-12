# CLIENT-CL07 · Shredder 1 · 7영역 자체 원본 조사 초안

고정 기준: `source-mv06`, Git `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, v1.12.0. 작성일 2026-10-11 UTC. 이 문서는 신규132개 중 **CLIENT-CL07 한 ID**의 문서 조사이며 별도 Codex의 로컬 통합·구현·게시 결과가 아니다.

## 핵심 확인·상충·누락 요약

- 독립 확인: RUN `I13.1`, FAULT `I15.4`, 내부 유지경보 `DB3.DBX14.7`, 분 계수 `DB9.DBW24`, 시간 전달필드 `DB9.DBW26`. 0226 알람 NID7, 0298 시간 NID7, 0333 시간 Reset NID48의 고유 Part/Wire/선언을 직접 결속했다.
- 전기 실제 렌더: FG89/PDF90 RUN X1:296/297 → FG129/PDF130 입력 단자12. FG93/PDF94 FAULT X1:334/335 → FG131/PDF132 입력 단자35. 네 페이지 각각 Rev2 17.03.2025, DATA 27.05.2024 확인.
- 출력 결속 금지: live_index에 존재하는 Q61.2/3/4/5/6은 각각 CL04/06/08/09/10 기동 심볼이다. **CL07 start 심볼·실행 출력 쓰기·전기 출력 끝점은 이번 자료 검색에서 미확보**다. 인접 번호라는 이유로 Q61.4를 CL07에 부여하지 않는다.
- 주소 상충: live_index doc521의 RUN Comment는 과거 `e 13.6`, doc539 FAULT Comment는 `e 18.4`지만 해당 Address는 I13.1/I15.4이며 고유 XML·OEM 회로가 이 Address와 일치한다. 과거 설명을 현재 주소로 치환하지 않는다.
- 시간 처리: MIN에 Int +1, MIN≥60일 때 HOUR에 **Move 1**, MIN에 Move 0, M1.7 Set. 별도 HOUR Move 0도 존재한다. HOUR를 시간 누적 `HOUR+1`로 설명하지 않는다.
- 공통근거 재사용: [CLIENT-CL04](CLIENT-CL04-DOTS-DRAFT.md)의 FC9/FC2 호출, IW12 Word 미러, T13 분 타이머를 색인으로 참고했다. 그 공통 원본의 해당 핀을 다시 확인했으며 CL04 고유 주소·도면·알람을 복제하지 않았다. 공통 저장 핸드셰이크와 경보 집계는 [SYS-RUNHOURS](SYS-RUNHOURS-DOTS-DRAFT.md), [SYS-ALARM](SYS-ALARM-DOTS-DRAFT.md), [SYS-PLC-IO](SYS-PLC-IO-DOTS-DRAFT.md)의 범위와 미확정 사항을 유지한다.
- 외부 Shredder 1 제어반 프로그램·동력회로·상대 단자·케이블·실물 동일성·정상극성·현행 보호값·HMI 이벤트·현장 복구 미확정. 공압 CYL-CL07과 다른 이름 공간이며 합치지 않는다.

## 1. 설비·자료 기준

`docs/equipment-standard/INVENTORY.json#/catalog/63`은 CLIENT-CL07, Shredder 1, kind=client, group=외부 연동, parent_id=null, phase2/planned, baseline으로 분류한다. BATCH14 범위의 별칭은 motor_client_07 / client motor 7 / cl07 / shredder 1이다. 이는 PLC 외부 설비 채널의 문서 식별이며 실제 파쇄기의 제작사·명판·설비 수량·실물 동일성을 증명하지 않는다. Primary Shredder(CL19), Shredder 2(CL14), Shredder vibration feeder(CL08)와도 구분한다.

원본 경로 약칭은 이하 `XML/`=`all-in-one/sources/decoded-original/`, `SRC/`=`all-in-one/sources/`이다. network-map/live_index는 위치 탐색·심볼 백업 근거이며 핵심 논리는 XML 선언과 Part/Wire로 확인한다. 본문 끝의 해시 표는 선정 원본 파일 전체의 byte 동일성 표이지 그 파일 모든 내용을 의미 검토했다는 뜻이 아니다.

2026-10-11T12:22:51+00:00 조사 시작, 12:23:47+00:00 전기 4쪽 시각검토 완료. root AGENTS·rollout SKILL·WORK-STANDARD·WORK-ITEM-TEMPLATE·INVENTORY 및 고정 버전/작업 인계 최상단을 읽었다. 사용자 승인 범위는 자체 읽기 전용 조사이며 현재 TIA나 사용자의 컴퓨터에 추가 접근하지 않았다. 모델 런타임 선택 증명은 미확인이다.

## 2. I/O·HMI

|분류·대상|원본 선언과 교차참조|해석 및 경계|
|---|---|---|
|SHREDDER 1 RUN|XML/0613 RID44 Global Bool, SSD AO105, SAD Input SAM=None; NID7 UID424|I13.1 입력영상. 기계 회전·부하 흐름의 직접 증명이 아님|
|SHREDDER 1 FAULT|XML/0599 RID18 Global Bool, AO124, SAD Input SAM=None; NID7 UID161/163|I15.4 입력영상. 외부 고장코드·보호기 종류는 미확보|
|Allarm.motor_client_07_fault|XML/0601 RID19 Global Bool AO119 BAD4 →0600 RID4 TOD3; NID7 UID162/165 AK=Write|DB3.DBX14.7 S/R 유지경보. 입력 복사와 구분|
|Flag.RESET_ALLARM|0601 RID7 Global Bool AO48 BAD6 →0600 RID6 TOD2; NID7 UID164|DB2.DBX6.0 내부 공통 Reset. HMI 버튼 자체와 구분|
|ON|0599 RID1 Global Bool AO0 SAD Memory; NID7 UID160|M0.0. 이름만 보고 상수 true로 간주하지 않음|
|CLIENT_MOTOR_7_MIN|0615 RID46 Global Int AO192 BAD5 →0614 RID5 TOD9; NID7 UID425/427/428/433|DB9.DBW24; +1 및 0쓰기|
|CLIENT_MOTOR_7_HOUR|0615 RID48 Global Int AO208 BAD5; NID7 UID431 Write, NID48 UID2655 Write|DB9.DBW26; 1쓰기와 0쓰기. 장기 누계 확정 금지|
|Tag_47|0613 RID1 Global Timer AO13, NID7 UID423/NID58 UID3115/3116|T13 공통 분 타이머, HMI 태그 아님|
|Flag_Aggiorna_DB|0613 RID13 Global Bool Memory AO15; NID7 UID434 Write|M1.7 저장 갱신 신호. 외부 저장 성공 증명 아님|
|Tag_48|0613 RID284 Global Timer AO17, NID48 UID2651|T17 공통 HOUR 초기화 가지 허가|
|직접 기동 출력|181개 IdentXmlPart 명명 검색 및 live_index start client 심볼 검토에서 CL07 선언 미확보|Q61.x 인접 심볼을 배정하지 않음. 절대·간접쓰기 전체 부재를 증명한 것은 아님|

직접 선택 대상은 Global과 Constant이며 Local FB 인자를 같은 RID/UID 숫자로 결속하지 않았다. RID는 해당 블록 선언군에 한정한다. 상수 1/60/0은 XML/0616 RID7/8/12, Scope=Constant, Int다.

### HMI 전달과 출력 선언의 경계

SRC/hmi_plc_tags.csv 82행: `SHREDDER_1_RUN,"DB13,X13.1",PLC,003FF`. 577행: `Allarmi_120,"DB3,X14.7",PLC,00115`. CSV는 dde.cfg 설정이며 온라인 현재값·실제 화면 문구·버튼 이벤트·통신 성공 증거가 아니다. Allarmi_120은 태그 이름이고 외부 파쇄기의 오류번호가 아니다.

XML/0397 NID1 HMI Inputs: Powerrail W21→Move60.en; ORef63 RID19(0627 Tag_183 Global Word AO96 Input SAM=None=IW12)→W70→Move60.in; Move60.out1→W72→ORef64 RID20(0629 Global Word AO96 BAD4, 0628 RID4 TOD13=DB13.DBW12). 이 **Word 전체 복사**는 I12.*와 I13.*를 포함하므로 I13.1→DB13.X13.1의 전달 근거가 된다. 별도 bit coil 쓰기나 PIW 직접접근으로 바꾸지 않는다. Move60.eno→W71→Move61.en이 존재하며 별도 후속 Word 전송과 구분한다. 상위 호출·다른 writer·스캔 최종값은 공통 SYS-PLC-IO 경계를 유지한다.

CL07 기동의 HMI 버튼/스크립트·요청 DB·허가·Q writer는 미확보다. live_index _7ev doc480~484의 Name/Address는 CL04 Q61.2, CL06 Q61.3, CL08 Q61.4, CL09 Q61.5, CL10 Q61.6이며 Comment `it should be free but it is used`가 붙는다. 이것도 심볼 선언 수준이다. XML 실행 쓰기 및 전기 결속이 없는데 명칭만으로 출력 구동이 있다고 단정하지 않는다.

## 3. 제어 구조

### 공통 호출을 직접 대조한 범위

XML/0549 Main document1620 NID7: W352 rail→Contact350.in, ORef335 RID52(0692 ON Global M0.0)→W348→350.operand. 350.out W351은 CRef331.en과 CRef334.en 등에 병렬 분기한다.

- CRef331 RefId80, 내부 CodeBlock345 RefId79 →0688 RID79 `Motor/Alarm Client` FC9, NID7 UID345 AK=Call; 0694 RID80 TORID79, NID7 UID331.
- CRef334 RefId83, 내부 CodeBlock347 RefId82 →0688 RID82 `time work motor` FC2, NID7 UID347 AK=Call; 0694 RID83 TORID82, NID7 UID334.

앞 FC의 ENO를 통과해야 다음 FC가 허가되는 직렬 회로가 아니다. 이 호출 근거는 일반 PLC 문서의 실행 허가이며 현재 CPU에서 실제 스캔되고 있음을 확인하지 않았다. 전용 CL07 모터 제어 FB 호출을 별도로 발견했다고 주장하지 않는다.

### RUN 시간계수 고유 전체 가지

XML/0298, document1008, FC2 NID7:

1. W456 rail→Contact452.in. ORef423/RID1 T13→W435→452.operand; 452.out W453→Contact454.in. ORef424/RID44 I13.1→W436→454.operand.
2. 454.out W455→Add406.en 및 Ge413.pre. Add406 SrcType=Int; ORef425/RID46 MIN→W437/in1; ORef426/RID7 Int1→W438/in2; out W439→ORef427/RID46 MIN. 해당 허가 때 MIN+1.
3. Ge413 Int in1 W440/ORef428=MIN, in2 W441/ORef429/RID8=60. out W442→Move416.en.
4. Move416.in W444/ORef430/RID7=1, out1 W445→ORef431/RID48=HOUR. **HOUR := 1**. HOUR ADD는 이 가지에 없다.
5. Move416.eno W446→Move419.en; in W447/ORef432/RID12=0, out1 W448→ORef433/RID46=MIN. Move419.eno W449→SCoil422.in; operand W450/ORef434/RID13=M1.7을 Set한다. ENO 연결은 생략하지 않는다.

XML/0333 document1046, FC2 NID48: T17 ORef2651/RID284→W2662→Contact2677. rail W2679, out W2678→Move2636.en(다른 채널). Move2636.eno W2665→Move2639.en; Move2639.in W2666/ORef2654/RID12=Int0; out1 W2667→ORef2655/RID48=CL07 HOUR. 따라서 DB9.W26에는 별도 0 writer가 있다. 이후 ENO W2668은 다른 채널 Move2642로 가지만 그 채널을 본 문서 완료로 세지 않는다.

XML/0019 document1056 FC2 NID58: Contact3120은 ORef3115/RID1 T13, W3118 operand를 **Negated**. out W3121→SdCoil3112.in; value W3117/ORef3114/RID335=0616 S5Time `S5T#1M`(V5632); operand W3119/ORef3116=T13. 공유 분 타이머를 CL07 기동지연/무응답 경보 타이머로 바꾸지 않는다. T17/M1.7/M2.0 외부 저장·ACK와 최종 시간 누적은 SYS-RUNHOURS의 미확정 범위다. 실제 분주 정확도나 데이터 저장 성공은 미확인이다.

### 요청→허가→출력 경계

확인된 가지는 외부 RUN/FAULT 수신 후 HMI·경보·시간 처리다. CL07 기동 요청·수자동·정지 인터록·준비응답·모터 전력 출력의 전체 사슬은 원본 미확보이며 주변 채널을 끼워 완성하지 않는다. 다중 writer/간접주소/블록 복사 전체를 분석한 것이 아니므로 출력 기능이 절대 없다는 결론도 내리지 않는다.

## 4. 전기 전달 경로

SRC/Electrical_Rev2.pdf의 실제 PDF90/94/130/132를 직접 렌더하여 확인했다. 각각 footer FG89/93/129/131, Rev2 17.03.2025, DATA 27.05.2024다. FG=PDF−1이 이번 네 장에서는 맞지만 일반 규칙으로 모든 페이지에 적용하지 않는다.

|경로|직접 렌더 확인한 양 끝점·표기|미확정|
|---|---|---|
|RUN 외부 접점|FG89/PDF90 SHREDDER 1 RUN: +24Vdc10.7 → X1:296 부근 5x20 2A F 퓨즈 → 선89.2 → 그려진 열린 접점 → X1:297 → E13.1, /129/2|상대 제어반 접점 기기명/단자·케이블·정상극성 미확보|
|RUN PLC 입력|FG129/PDF130 E13.1, 상호참조89/3 → 모듈 단자12; CPU515/MOD11 표기|현재 CPU 모델·실제 모듈/배선 설치 확인 아님|
|RUN 모듈 보조전원|FG129: +24Vdc10.7→X21:3012, 5x20 2A IST.→선129.1→단자19; -0Vdc10.6→단자20|도면 정격이며 현행 퓨즈/보호값 권고가 아님|
|FAULT 외부 접점|FG93/PDF94 SHREDDER 1 FAULT: +24Vdc10.7 → X1:334 부근 5x20 2A F 퓨즈 → 선93.1 → 그려진 열린 접점 → X1:335 → E15.4, /131/5|외부 보호 원인·전원상실시 의미·접점 극성 미확보|
|FAULT PLC 입력|FG131/PDF132 E15.4, 상호참조93/1 → 모듈 단자35; CPU515/MOD11|실제 접점 상태 및 입력 정상값 미확정|
|FAULT 모듈 보조전원|FG131: +24Vdc10.7→X21:3013, 5x20 2A IST.→선131.1→단자39; -0Vdc10.6→단자40|현재 보호설정·현장 정격 미검증|
|기동/동력 출력|CL07 전용 기동 Q/릴레이/전력 경로를 확보하지 못함|코일 A1/A2·부하접점·컨택터·모터·보호기/인버터·외부 제어반 전체 미확보|

네 장의 해당 입력 영역에 SPARE 점선 표기가 있다. 설비명·주소가 있어도 실제 설치와 사용을 확정하지 않는다. 열린 접점 도형과 PLC 논리의 양극성 사용은 문서 사실이며 운전 중 정상극성/실물 안전상태를 증명하지 않는다. 이 입력 경로에는 다른 출력 회로의 부하접점5/9와 하단 접점표1/5/9를 가져오지 않는다.

SRC/Electrical_Can_Decoating_20241118.pdf는 텍스트 변환 후 shredder/cl07/client motor 7 검색에서 고유 결속을 찾지 못했다. 그 PDF의 도면 전수 의미검토·실렌더를 했다는 뜻이 아니다. 자료 없는 외부 제어반을 OCR 부재만으로 존재하지 않는다고 판단하지 않는다.

## 5. 알람·복구

XML/0226 document416, `Motor/Alarm Client` FC9 NID7을 직접 확인했다.

- 공통 허가: rail W183→Contact175.in, ON ORef160/RID1→W166→175.operand. 175.out W176은 Set/Reset 가지로 분기한다.
- Set: I15.4 ORef161/RID18→W167→Contact177.operand, 177.out W178→SCoil154.in; operand W169/ORef162/RID19=DB3.X14.7. 식은 `ON AND FAULT`.
- Reset: I15.4 ORef163/RID18→W170→Contact179.operand **NOT**; 179.out W180→Contact181.in. RESET_ALLARM ORef164/RID7→W171→181.operand; out W182→RCoil159.in; operand W173/ORef165/RID19=같은 경보. 식은 `ON AND NOT FAULT AND RESET_ALLARM`.

이 네트워크는 Contact4 + SCoil/RCoil이며 지연 타이머가 없다. RUN=0이나 분 타이머 T13을 이 알람 발생 원인으로 바꾸지 않는다. FAULT가 유지되면 이 Reset 식은 만족하지 않는다. 원인이 사라져도 Reset 조건 없이는 래치가 자동 해제된다고 설명하지 않는다.

Allarmi_120(DB3.X14.7) 연결은 주소 확인까지다. HMI ACK와 내부 Reset 생성, 외부 제어반 Reset, 원인 해소, 기동 허가 재성립, 재운전·현장 복구는 서로 다른 상태다. 이 경보 비트가 직접 파쇄기 모터를 정지하는 출력 writer는 확인하지 못했다. 외부 보호회로·안전기능·현장 복구 순서를 발명하지 않는다.

## 6. 증상별 읽기 전용 관찰

다음은 승인된 담당자가 제공할 자료의 비교 기준이며 실제 조작·Reset 실행·활선 검사·강제출력·바이패스·보호값 변경 지시가 아니다.

|증상|동일 시각에 확보할 관찰 자료|비교 기준·판단 한계|
|---|---|---|
|화면에서 기동했지만 파쇄기 정지|현재 프로젝트 식별, 버튼 이벤트/요청값, 실제 Q writer 교차참조, 외부제어반 상태, I13.1|CL07 전용 출력 미확보. Q61.4를 임의 배정하거나 미운전을 GME 고장으로 단정하지 않음|
|외부 RUN인데 HMI 표시 없음|I13.1, IW12, DB13.W12/X13.1, HMI SHREDDER_1_RUN ID003FF 및 통신시각|FG89 X1:296/297→FG129 단자12와 0397 Word 전달을 나눠 비교. 실제 극성·단선 확정 금지|
|FAULT 소멸 후 경보 유지|I15.4, ON M0.0, DB2.X6.0, DB3.X14.7, Allarmi_120|0226 유지 및 Reset 허가 조건과 HMI ACK를 분리|
|Reset 요청 뒤에도 유지|요청 이벤트·소비 로그, 내부 Reset 전후값, 동시 FAULT 상태|NOT FAULT가 필요하다. 버튼 조작이 내부 Reset 도달을 보장하지 않음|
|시간이 증가하지 않거나 HOUR가 1/0 반복|I13.1,T13,DB9.W24/W26,M1.7,T17,외부 저장 기록의 시각|0298 MIN+1/HOUR Move1 및0333 Move0 비교. 외부 장기누계/저장 성공 미확정|
|회로 주소와 설명이 다름|도면 개정, 프로젝트 Address/Comment, X1/모듈 표찰 사진·외부회로|과거 e13.6/e18.4와 백업 I13.1/I15.4를 분리 기록. 배선 변경으로 해결하지 않음|

관찰자·실제시각/시간대·위치·값/단위·프로젝트/도면 판본·장치·사진/로그 출처·비교결과·미확정 사항을 남긴다. 실제 운영/SEJIN 데이터나 사진을 복제하지 않았다.

## 7. 완료·누락 및 검증

|영역|문서 상태|남은 조건|
|---|---|---|
|설비·자료 기준|적용·고정원본/독립ID 확인|Shredder 1 실물 동일성/명판 미확정|
|I/O·HMI|적용·RUN/FAULT/경보/시간 선언 및 HMI 주소 대조|기동요청·출력·이벤트/현행 통신 미확보|
|제어|적용·고유0226/0298/0333 및 공통 호출·T13 확인|외부 기동·정지·허가/저장 프로그램 미확보|
|전기 끝점|적용·입력 두 경로 실제 렌더4쪽|상대 제어반·케이블·출력/동력·실물 미확보|
|알람·복구|적용·S/R 식 확인|ACK·외부Reset·현장복구 미확인|
|증상 관찰|적용·읽기 전용 비교 기준 작성|현장 관찰값 미취득|
|완료·누락|문서조사 complete_with_gaps|UI/저장/게시/TIA/현장 미수행|

추가로 필요한 것은 현행 외부 Shredder 1 제어반 회로/프로그램·기동 허가표, GME 프로젝트의 CL07 출력 writer 전체 교차참조(절대/간접 포함), X1:296/297/334/335 상대 단자와 케이블표, HMI 이벤트·스크립트, 현재 CPU/모듈/파쇄기 명판·정상극성 승인 근거·현행 보호값 확인 자료다. 새 자료 없이 동일 실물 보류를 반복 조사하지 않는다.

백업 미리보기·선택복원·기록 전후비교·관찰보고서/PDF의 CL07 전용 기능 구현/저장/재읽기/재열기는 실행하지 않았다. 기존 note/repair_observation·미지필드·초안·저장키·다른 설비를 수정하지 않았다. 최종 상태 documentation=`complete_with_gaps`, static_review=`selected_original_xml_and_pdf_reviewed`, ui_records=`not_run`, publication=`not_published`, tia_compile/live_cpu/field_recovery=`not_performed`다. BC01 동등 기능완료·현재 CPU 검증·현장 복구완료와 구분한다.

### 검사 범위와 산출물

181개 IdentXmlPart 명명 검색에서 고유 선언요소5개가 검색되었다. 이는 181개 본문 의미검토가 아니다. 직접 의미대조는 0226/0298 전체 고유 핀, 0333 CL07 HOUR Reset 가지, 0397 IW12 Word 경로, 0549 FC9/FC2 호출, 0019 T13 가지 및 해당 선언이다. 시공 PDF는 제한 텍스트 검색이고 OEM 실제 렌더는4쪽이다.

선정 원본34개 SHA256 및 고정 Git blob 전체 내용 비교는 모두 일치. 원본 Git status는 조사 시작과 검사 시점 모두 clean이다. 원본 build/test/generator·시뮬레이터·PLC/TIA·현장·SEJIN 변경/실행은 없으며 배정 extracts와 본 MD만 작성했다. 원본/중지 자산 수정은 하지 않았다. 해시 일치는 의미검토 완료 수와 구분한다.

검사·원형 발췌: `../extracts/CLIENT-CL07/verification.json`, `source-hashes.json`, `declaration-search.json`, `live-index-selection.json`, 원형 XML readable 파일, OEM 렌더4장. 해당 디렉터리의 자체 Python은 정적 XML 탐색·해시 비교만 하며 원본의 생성기/시험기는 실행하지 않는다.

### 선정 원본 SHA256 + 고정 Git blob 전체 표

경로는 source-mv06 기준. 내용 일치는 `git show abcf31c5030bc7ef8749ed8e869a857f2387a28a:경로`의 전체 byte와 비교했다.

|선정 원본 경로|SHA256|고정 Git blob|내용 일치|
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
|`all-in-one/sources/Electrical_Can_Decoating_20241118.pdf`|`3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd`|`0ee6b6f8361c5790864dbba4bbd9d55e8e7c08f8`|일치|
|`all-in-one/sources/hmi_plc_tags.csv`|`a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404`|`cf4c0650e7c7baac350dcb89909b808435704880`|일치|
|`all-in-one/sources/live_index.json`|`14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1`|`e35ccea1f841349c632666c29954b7bcd4f5839e`|일치|
|`all-in-one/sources/decoded-original/network-map.json`|`c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60`|`424430b6b953e43138e5d0a18ca40c949e21cfa1`|일치|
|`all-in-one/sources/decoded-original/0019-FlgNet.xml`|`a3301f4d07c2d36aefa6faa6c3559a1cff4565fc6de40cd17e54b548b30c0ce5`|`f78cfdbf5e717304114660ffbd3bb42cbed6d79d`|일치|
|`all-in-one/sources/decoded-original/0226-FlgNet.xml`|`6f7ef7c6a70818abea03a8d4e1b3fae926800d6c6173da9ee1f1d1c46aecd1cc`|`81576e30e591a1a276b669e43f7ca8243e307a7d`|일치|
|`all-in-one/sources/decoded-original/0298-FlgNet.xml`|`4c6e59241d4da79ef0b9cac72a56088d2dfdb5faa9a1dca8b6116a43b8ff0d7d`|`9ebc17249325ff3f0062c1b7f14cce7e5a14dace`|일치|
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

초안 작성 완료 실제시각: 2026-10-11T12:27:42.104877+00:00
