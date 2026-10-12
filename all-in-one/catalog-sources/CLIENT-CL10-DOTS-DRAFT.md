# CLIENT-CL10 Rotex screen 자체 원본 조사 초안

## 핵심 확인·상충·누락·공유 근거

- 대상은 CLIENT-CL10 외부 모터 채널 한 개다. 공압 CYL-CL10 및 다른 CLIENT 번호와 병합하지 않는다.
- 고유 원본으로 RUN **I13.4**, FAULT **I15.7**, 유지경보 **DB3.DBX15.2**, 시간 필드 **DB9.DBW36(MIN)/DBW38(HOUR)**를 확인했다.
- 출력 **Q61.6**은 live_index doc484의 `start client motore 10` 심볼이다. 원문 `motore`를 보존한다. 실행 XML writer·명령 허가·외부 출력 끝점은 확보하지 못했다. 앞 채널 번호에서 주소를 추산하지 않았다.
- RUN/FAULT 백업 comment의 `e 14.1`/`e 18.7`은 실제 Address I13.4/I15.7과 다르다. 과거 주석과 선언 주소를 구분한다.
- FC9 NID10은 ON AND FAULT에서 Set, ON AND NOT FAULT AND RESET_ALLARM에서 Reset하며 고유 네트워크에 타이머는 없다. FC2 NID10은 MIN+1, MIN≥60에서 **HOUR := 1**이며 NID48의 별도 writer가 **HOUR := 0**을 수행한다. 장기 누적 ADD로 바꾸지 않는다.
- 실제 OEM PDF90/94/130/132를 렌더해 고유 단자 및 개정란을 확인했다. 네 쪽 모두 SPARE 범위에 그려져 있으며, 이것만으로 현재 사용 여부·실물·정상극성·보호값을 확정하지 않는다.
- 공유 근거 인덱스: [CLIENT-CL09](CLIENT-CL09-DOTS-DRAFT.md)의 동일 고정입력 FC2/FC9/Main·Word 미러, [SYS-RUNHOURS](SYS-RUNHOURS-DOTS-DRAFT.md)의 저장 핸드셰이크, [SYS-ALARM](SYS-ALARM-DOTS-DRAFT.md)의 공통 Reset·집계, [SYS-HMI](SYS-HMI-DOTS-DRAFT.md)의 화면 이벤트 경계. 고유 선언·핀·전기 끝점은 이번에 직접 대조했다. CL09의 별도 I16.6 fault_doppio!는 CL10 근거로 복제하지 않았다.

## 1. 설비·자료 기준

- 대장: `docs/equipment-standard/INVENTORY.json#/catalog/66`, CLIENT-CL10, Rotex screen, kind client, 외부 연동, 부모 없음, phase2. 별칭 motor_client_10/client motor 10/cl10/rotex screen. 외부 제어반 원격 신호 및 내부 경보·계수 범위다.
- 고정 읽기전용 원본: `source-mv06`, Git `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, v1.12.0. 최근 사용자 로컬 통합·게시 상태를 이 백업으로 검증했다고 주장하지 않는다.
- 문서 약칭 NNNN은 `all-in-one/sources/decoded-original/NNNN-FlgNet.xml` 또는 해당 IdentXmlPart.xml이다. 파일번호/document_id/NID는 다르다. network-map/live_index는 탐색색인이며 XML이 있는 핵심은 원형 선언과 Wire로 확인했다.
- 실제 작업 시각(UTC): 착수 2026-10-11 12:31:07, 선언·고유 핀 조사 12:31~12:32 도구 기록, PDF 렌더 및 시각 검토 12:32:10~12:32:16, 선정 해시 확인 12:33:14.709620. 모델·추론 런타임 증명은 미확인.
- 원본 Git HEAD 일치·status 공란. 연구자 쓰기 범위는 본 초안과 `extracts/CLIENT-CL10/`뿐이다. 원본 코드·대장·PLC·현장·보호값·SEJIN·운영기록 변경 및 원본 build/test/generator·시뮬레이터·행동시험 실행 없음.

## 2. I/O·HMI

### 2.1 고유 선언과 자료형

|신호|원본 선언·결속|주소·해석|
|---|---|---|
|ROTEX SCREEN RUN|0613 RID62 Global, NID10 UID586; Bool, SSD AO108, SAD Input SAM=None|I13.4 원시 입력영상. 실제 회전/체 운동의 직접 증명 아님|
|ROTEX SCREENFAULT|0599 RID24 Global, NID10 UID215/217; Bool AO127, Input SAM=None|I15.7 원시 고장 입력. 정상극성 미확정|
|Allarm.motor_client_10_fault|0601 RID25 Global Bool AO122, BAD4→0600 RID4 TOD3; NID10 UID216/219 Write|DB3.DBX15.2 유지경보|
|Flag.RESET_ALLARM|0601 RID7 Global Bool AO48, BAD6→0600 RID6 TOD2; NID10 UID218|DB2.DBX6.0 공통 내부 Reset; HMI ACK/버튼과 별도|
|ON|0599 RID1 Global Bool AO0 Memory, NID10 UID214|M0.0. 이름만으로 상수 true로 치환하지 않음|
|CLIENT_MOTOR_10_MIN|0615 RID64 Global Int AO288, BAD5→0614 RID5 TOD9; NID10 UID587/589/590/595|DB9.DBW36. Add+1 및 Move0의 대상|
|CLIENT_MOTOR_10_HOUR|0615 RID66 Global Int AO304, 같은 BAD5; NID10 UID593, NID48 UID2661 Write|DB9.DBW38. Move1 및 Move0; 누적 Add 아님|
|Tag_47 / Tag_48|0613 RID1 Timer AO13 / RID284 Timer AO17, Global|T13/T17 공유 시간계수·저장 처리. CL10 기동감시용 고유 타이머 아님|
|Flag_Aggiorna_DB|0613 RID13 Global Bool AO15 Memory, NID10 UID596 Write|M1.7 저장 갱신 요청 관련 내부 Set 비트|
|start client motore 10|live_index `_7ev` doc484 Name, Bool Address `%q61.6`, comment `it should be free but it is used`|Q61.6 심볼 수준. 직접/간접 실행 쓰기와 물리 결속 미확보|

Int1/60/0은 0616 RID7/8/12의 Constant이며 Local 변수로 취급하지 않았다. RID와 UID는 블록·선언파일·NID 문맥 안에서만 결속했다. `live_index` doc524 RUN comment `e 14.1 rotex screen run`, doc542 FAULT comment `e 18.7 rotex screenfault`는 해당 Address와 다르다.

### 2.2 HMI 태그와 입력 Word 전달

`all-in-one/sources/hmi_plc_tags.csv`에서 `ROTEX_SCREEN_RUN`, `DB13,X13.4`, PLC, ID003FC와 `Allarmi_123`, `DB3,X15.2`, PLC, ID00112를 확인했다. CSV는 설정이며 온라인 현재값·화면 표시문구·버튼·권한·ACK 이벤트·스크립트·통신 성공의 증거가 아니다. CL10 전용 기동 HMI 이벤트와 DB9 시간 필드 직접 표시 연결은 미확보다.

0397 `HMI Inputs` NID1에서 전달은 bit Coil이 아닌 Word Move다.

|전달|선언·원본 핀|CL10 범위|
|---|---|---|
|IW12→DB13.DBW12|0627 RID19 Global Word AO96 Input SAM=None, ORef63; W70→Move60.in; rail W21→60.en; out1 W72→ORef64, 0629 RID20 Global Word AO96 BAD4→0628 RID4 TOD13|byte12~13 내 I13.4→DB13.X13.4 RUN 미러|
|IW14→DB13.DBW14|0627 RID21 Global Word AO112 Input, ORef65 W73→Move61.in; Move60.eno W71→61.en; out1 W75→ORef66, 0629 RID22 Word AO112 BAD4→DB13|I15.7→DB13.X15.7 원시 FAULT 미러. DB3.X15.2 래치와 별도|

Move60/61의 DisableENO=true와 원문 eno/en 연결을 모두 보존한다. 독립 bit 쓰기 또는 PIW/Peripherie 접근으로 설명하지 않는다. FC15 상위 호출·다른 writer·현재 스캔 최종값은 공통 조사 경계를 유지하며 해당 두 Word 경로만 재확인했다.

## 3. 제어 구조

### 3.1 상위 호출과 소유 경계

0549 Main document1620 NID7의 rail W352→Contact350.in, ORef335/RID52 W348→operand는 0692 ON(M0.0)이다. Contact350.out W351이 CRef331 및 CRef334의 en에 병렬 연결된다.

- CRef331 RefId80 내부 CodeBlock345 RefId79 → 0688 RID79 `Motor/Alarm Client` TOD9(FC9), 0694 RID80 NID7 UID331 TORID79.
- CRef334 RefId83 내부 CodeBlock347 RefId82 → 0688 RID82 `time work motor` TOD2(FC2), 0694 RID83 NID7 UID334 TORID82.

앞 FC의 ENO를 뒤 FC의 순차 허가로 바꾸지 않는다. 이것은 백업 호출 결속이며 현재 CPU에서 실행 중이라는 증거는 아니다. Q61.6을 제어하는 수자동·기동·정지·외부 허가 시퀀스는 확인하지 못했다.

### 3.2 RUN 기반 고유 시간계수

0301 document1011, FC2 NID10의 전체 고유 핀은 다음과 같다.

1. rail W618→Contact614.in; T13 ORef585/RID1 W597→operand. 614.out W615→Contact616.in; I13.4 ORef586/RID62 W598→616.operand.
2. 616.out W617→Add568.en 및 Ge575.pre. Add568 SrcType Int: MIN ORef587 W599→in1, Int1 ORef588/RID7 W600→in2, out W601→ORef589/RID64(MIN).
3. Ge575 SrcType Int: MIN ORef590 W602→in1, Int60 ORef591/RID8 W603→in2, out W604→Move578.en.
4. Int1 ORef592/RID7 W606→Move578.in, out1 W607→ORef593/RID66(HOUR). HOUR := 1이며 HOUR+1이 아니다.
5. Move578.eno W608→Move581.en; Int0 ORef594/RID12 W609→in, out1 W610→ORef595/RID64(MIN). Move581.eno W611→SCoil584.in, operand W612/ORef596/RID13=M1.7 Set. ENO 체인을 생략하지 않는다.

0333 document1046 FC2 NID48에는 HOUR를 지우는 다른 writer가 있다. T17 ORef2651/RID284 W2662→Contact2677.operand, rail W2679→in, out W2678→Move2636.en. 2636.eno W2665→2639.en, 2639.eno W2668→2642.en, 2642.eno W2671→2645.en, 2645.eno W2674→2648.en으로 이어진다. CL10 대상은 마지막 **Move2648**이다. Int0 ORef2660/RID12 W2675→in, out1 W2676→ORef2661/RID66(DB9.DBW38). 앞 CLIENT 필드도 보이지만 다른 catalog ID 완료로 집계하지 않는다.

### 3.3 공유 타이머와 검색 한계

0019 FC2 NID58: rail W3122→Contact3120.in, ORef3115/RID1(T13) W3118→Negated operand, out W3121→SdCoil3112.in. 0616 RID335 Constant S5Time `S5T#1M` V5632, ORef3114 W3117→value; ORef3116/RID1 W3119→operand(T13). 공유 분 계수 펄스 관련 구조이며 CL10 고장 지연/기동시간을 뜻하지 않는다. T17·M1.7·M2.0·외부 저장 ACK 전체 해석은 동일 원본 SYS-RUNHOURS에 연결한다. HOUR 0/1을 장기 누적 저장 성공이나 정확한 운전시간으로 판단하지 않는다.

IdentXmlPart 181개 이름 탐색에서 CL10 RUN/FAULT/유지경보/MIN/HOUR 5개 access를 확인했다. `start client motore 10` 이름 및 Output AO494(Q61.6)/AO488·480 범위 선언 후보는 미식별이다. 이 제한 검색은 모든 절대주소·간접주소·블록복사 writer 부재의 증명이 아니다. Q61.6 실제 교차참조와 현재 프로젝트가 필요하다.

## 4. 전기 전달 끝점

`all-in-one/sources/Electrical_Rev2.pdf` 실제 PDF90·94·130·132쪽을 각각 렌더해 시각 확인했다. 각 footer는 **Rev2 17.03.2025 / DATA 27.05.2024**다. FG는 아래와 같이 별도로 읽었다.

|고유 경로|FG / 실제 PDF 및 끝점|미확정 경계|
|---|---|---|
|RUN 외부 접점|FG89 / PDF90: +24Vdc10.7 → 5x20 2A F, X1:302 → 선89.5 → 그려진 열린 접점 → X1:303 → E13.4, 참조129/5|외부 제어반 상대 단자·접점기기번호·케이블번호/규격 없음|
|RUN PLC 입력|FG129 / PDF130: E13.4, 역참조89/7 → 입력 단자15, 표기 CPU515 MOD11|현재 CPU·장착모듈·실물배선 증거 아님|
|FAULT 외부 접점|FG93 / PDF94: +24Vdc10.7 → 5x20 2A F, X1:340 → 선93.4 → 열린 접점 → X1:341 → E15.7, 참조131/7|외부 고장 종류·정상극성·보호회로 미확정|
|FAULT PLC 입력|FG131 / PDF132: E15.7, 역참조93/6 → 입력 단자38, CPU515 MOD11|외부 보호값·고장 원인·복구와 별도|
|입력모듈 보조전원|FG129/PDF130: +24Vdc10.7→X21:3012, 5x20 2A IST.→129.1→19, -0Vdc10.6→20. FG131/PDF132: X21:3013, 2A IST.→131.1→39, -0Vdc10.6→40|도면 표기 정격이며 현행 퓨즈값 확인/추천 아님|
|기동 출력|Q61.6 심볼; OEM/시공 PDF 텍스트에서 A61.6/Q61.6 별도 끝점 미식별|PLC 출력모듈·릴레이 A1/A2·부하접점·단자·외부전력회로 미확보|

네 페이지의 해당 신호는 SPARE 점선 범위에 있다. PLC 백업의 사용처와 도면 SPARE 표기를 함께 보존하고 실제 예비/사용 여부를 추정하지 않는다. 열린 접점 그림은 현장 정상극성의 증명이 아니다. 이 회로에 다른 설비 릴레이 부하접점5/9 또는 하단 접점표1/5/9를 복제하지 않는다.

`Electrical_Can_Decoating_20241118.pdf` 텍스트에서도 rotex/A61.6/Q61.6 직접 결속을 찾지 못했다. 이 PDF는 경계 검색이며 실제 렌더/전수 의미검토를 수행한 문서로 표시하지 않는다. 외부 제어반 회로와 케이블표가 없으므로 원격 입력의 GME측 끝점까지만 문서화했다.

## 5. 알람·복구

0229 document419 `motor/alarm client`, FC9 NID10을 직접 확인했다.

- 공통 허가: rail W237→Contact229.in, ON ORef214/RID1 W220→operand; out W230이 Contact231/233.in으로 분기.
- Set: I15.7 ORef215/RID24 W221→Contact231.operand; out W232→SCoil208.in, operand W223/ORef216/RID25=DB3.X15.2. **ON AND I15.7 → Set**.
- Reset: I15.7 ORef217/RID24 W224→Contact233의 **Negated operand**; out W234→Contact235.in. DB2.X6.0 ORef218/RID7 W225→235.operand; out W236→RCoil213.in; operand W227/ORef219/RID25=같은 경보. **ON AND NOT I15.7 AND RESET_ALLARM → Reset**.

네트워크에는 Timer Part가 없다. RUN I13.4=0을 직접 알람 원인으로 추가하지 않는다. 원시 FAULT가 참인 동안 Reset 가지는 성립하지 않는다. 원인 소멸, PLC 유지경보 해제, HMI ACK, 외부 제어반 Reset, 재기동, 실물 정상복구는 각기 다른 상태다.

Allarmi_123은 경보 주소와 일치하나 현재 표시문구·ACK·경보이력은 미확정이다. 공통 DB3 집계/Reset 생성은 SYS-ALARM의 같은 고정입력을 참조한다. 이 경보가 Q61.6 또는 외부 설비를 직접 정지시키는 writer는 미확보이므로 정지 인과를 만들지 않는다.

## 6. 증상별 읽기 전용 관찰 기준

승인된 담당자가 제공한 자료를 동일 시각에 비교하는 기준이다. 현장 조작·강제출력·바이패스·활선 점검·보호값 변경·Reset 실행 지시가 아니다.

|증상|관찰할 값·자료|문서 비교와 경계|
|---|---|---|
|기동 표시인데 체 정지|현행 프로젝트, Q61.6 값·writer, HMI 이벤트, 외부 제어반 상태, I13.4|출력 심볼만으로 실제 전력회로 또는 운전허가 확정 불가|
|현장 RUN인데 화면 정지|I13.4, IW12, DB13.W12/X13.4, HMI003FC, 시각|X1:302/303→MOD11 단자15와 Word 미러 분리; 배선/통신 원인 임의 단정 금지|
|FAULT/경보 표시 불일치|I15.7, DB13.X15.7, DB3.X15.2, HMI00112|원시 입력·Word 미러·래치·화면 단계 구분|
|고장 소멸 뒤 경보 유지|ON, I15.7, DB2.X6.0, DB3.X15.2 전후|NOT FAULT 및 내부 Reset 조건; 외부 원인 해제와 내부 래치 해제 분리|
|시간값이 1에서 멈추거나 0으로 변경|I13.4,T13,T17,DB9.W36/W38,M1.7,승인된 저장 로그|0301 Move1 및 0333 Move0 구조; 누적 저장 성공 미확정|
|도면/주석/실제주소 불일치|백업판본, 현행 도면, 단자표찰·외부회로 사진|comment e14.1/e18.7과 선언 I13.4/I15.7 분리. 임의 주소 변경 금지|

관찰자·실제 시각/시간대·위치·값/단위·수집장치·프로젝트/도면 판본·사진/로그 출처·비교결과·배제결과·승인 조치·복구 근거를 별도로 기록해야 한다. 실제 관찰값·운영기록을 확보하거나 SEJIN 자료를 복제하지 않았다.

## 7. 완료·누락·검증 범위

|영역|현재 상태|잔여 자료|
|---|---|---|
|설비·자료 기준|적용, 한 catalog ID 문서 작성|Rotex 본체·외부 제어반 실물 동일성|
|I/O·HMI|고유 선언·주소·Word 미러 확인|Q61.6 실행 writer, 현행 화면 이벤트·통신|
|제어|고유 FC9/FC2 및 상위 호출 선택 확인|수자동·기동/정지·외부 허가 시퀀스|
|전기 끝점|RUN/FAULT GME측과 실제 렌더4쪽 확인|출력·상대 제어반 단자·케이블·현행 연결|
|알람·복구|고유 S/R·무타이머 확인|외부 보호 원인·ACK/Reset·현장복구|
|증상 관찰|읽기 전용 비교 기준|실제 동시각 관찰값|
|완료 기준|문서 complete_with_gaps|BC01 동등 구현·게시·현장 완료는 아님|

필요자료: 현행 CL10 외부 제어반 회로/프로그램, Q61.6 간접/절대주소 포함 교차참조, X1:302/303/340/341 상대 단자·케이블표, 실제 사용/예비 여부와 정상상태 증거, HMI 기동/ACK/Reset 이벤트, 명판·보호기 모델 및 현행 승인판본. 새 자료가 없으면 같은 실물 보류를 반복 조사하지 않는다.

네 기능 중 도면·래더 비교용 원본 위치만 준비했다. 백업·선택복원, 기록 전후비교, 보고서/PDF 기능의 구현·저장·재읽기·재열기·UI/게시 검사는 수행하지 않았다. note/repair_observation·미지 필드·기존초안·저장키·다른 설비를 변경하지 않았다.

최종 상태: documentation `complete_with_gaps`; static_review `selected_original_xml_and_pdf_reviewed`; ui_records `not_run`; publication `not_published`; tia_compile/live_cpu/field_recovery `not_performed`. 부모 독립 검토·첨부 대기. 로컬 통합은 사용자 Codex 범위다.

### 선정 검증과 의미검토의 구별

선정 원본34개 SHA256 및 고정 Git blob byte 일치는 34개 전체 의미검토를 뜻하지 않는다. 직접 의미검토는 0229/0301 고유 전체 핀, 0333 마지막 CL10 writer, 0397 IW12/14 미러, 0549 FC9/FC2 호출, 0019 T13 가지와 선택 선언이다. IdentXmlPart 181개 이름·주소 검색은 181개 논리 의미검토가 아니다. PDF 실제4쪽을 시각 검토했고 나머지 전기/시공 전체 검증은 수행하지 않았다.

검사·해시는 `../extracts/CLIENT-CL10/verification.json`, `source-hashes.json`, 선언검색·공유선언·출력검색 JSON 및 원형 XML 추출/PDF 렌더로 남겼다. 모든 선택 원본 byte가 고정 Git 내용과 일치하며 source Git status는 공란이다.

### 선정 원본 SHA256 + 고정 Git blob 전체 표

경로는 `source-mv06/` 기준이다. 각 byte를 `git show abcf31c:경로`와 직접 비교했다.

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
|`all-in-one/sources/decoded-original/0229-FlgNet.xml`|`2cc42ec7928f57e37ecc0fa27802463180c4456f2fde9d435b59640fac10fca2`|`19aca86c999e0dab3dbc3f72dd9d4ebb6a79a232`|일치|
|`all-in-one/sources/decoded-original/0301-FlgNet.xml`|`75bb192b2bf119d9a047203ad2c65595f637377376615a4362d6b8bc0607203f`|`4ef7775c5eb10ccf2564698b8416dff0ac500b8b`|일치|
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

초안 작성 완료 실제시각: 2026-10-11T12:35:26.038028+00:00
