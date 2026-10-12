# CLIENT-CL15 Belt conveyor D 자체 원본 조사 초안

## 핵심 확인·상충·누락·공유근거

- 조사 단위는 CLIENT-CL15 한 개다. 외부 연동 Belt conveyor D이며 공압 CYL-CL 번호와 다른 이름 공간이다.
- 고유 XML에서 RUN **I13.7**, FAULT **I16.2**, 유지경보 **DB3.DBX15.7**, 시간 필드 **DB9.DBW56/58**을 선언·NID·RID·UID 및 실제 Part/Wire/ORef로 독립 확인했다.
- 0232 경보는 ON AND FAULT에서 Set, ON AND NOT FAULT AND RESET_ALLARM에서 Reset이다. 고유 경보 네트워크에는 지연 타이머가 없다.
- 0304 시간계수는 MIN+1, MIN≥60에서 **HOUR:=1**, MIN:=0이며 0334의 별도 writer가 HOUR:=0을 쓴다. HOUR를 누적 Add로 바꾸지 않았다.
- RUN/FAULT 도면은 FG90/PDF91·FG94/PDF95·FG129/PDF130·FG132/PDF133에서 확인했다. 고유 회로에 SPARE가 표시되어 현장 사용 여부는 미확정이다.
- 이름 검색에서 CL15 기동 출력 심볼/실행 writer를 식별하지 못했다. CL05~09의 Q61.x 주소를 숫자 순서로 복제하지 않는다. 외부 제어반 내부 기동·보호·전력 회로와 상대 케이블/단자는 미확보다.
- live_index RUN comment의 e14.6, FAULT comment의 e19.4는 실제 Address I13.7/I16.2와 다른 과거 설명이다. COVEYOR 철자도 원문 보존한다.
- 공통근거 색인은 [CLIENT-CL04](CLIENT-CL04-DOTS-DRAFT.md), [CLIENT-CL09](CLIENT-CL09-DOTS-DRAFT.md), [SYS-RUNHOURS](SYS-RUNHOURS-DOTS-DRAFT.md), [SYS-ALARM](SYS-ALARM-DOTS-DRAFT.md), [SYS-HMI](SYS-HMI-DOTS-DRAFT.md)다. 동일 고정 원본의 저장 핸드셰이크·공통 Reset·상위 호출 경계를 연결 재사용했다. 아래 고유 선언·핀·도면은 CL15 원본을 직접 대조했다.

## 1. 설비·자료 기준

대상 `docs/equipment-standard/INVENTORY.json#/catalog/69`: CLIENT-CL15, Belt conveyor D, kind client, 외부 연동, 부모 없음, phase2. PLC 외부 상태 채널 문서이며 벨트 본체·모터·감속기·외부 제어반 실물 동일성을 확정하지 않는다. 조사 지시와 TASK3-BATCH15-SCOPE.json의 해당 행을 읽고 기존 제외/보류를 유지했다.

고정 기준은 읽기 전용 `source-mv06`, Git `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, v1.12.0이다. 최신 로컬 통합·게시 기능의 검증이 아니다. NNNN XML 약칭은 `all-in-one/sources/decoded-original/NNNN-FlgNet.xml` 또는 동일 번호 IdentXmlPart.xml이다. document_id·파일번호·NID는 서로 다르며 UID/RID도 해당 블록 문맥을 유지한다. network-map/live_index는 탐색 색인이다.

실제 작업 기록(UTC): 착수 2026-10-11 12:31:53, 고유 선언·XML 대조 12:32:15~12:33:18, PDF 렌더·4쪽 시각 검토 12:32:34~12:32:49, 선정 원본 해시 대조 12:33:37. 런타임 모델/추론 설정 증명은 미확인이다. 원본 Git status 공란을 확인했고 원본 코드·대장·다른 초안·운영/SEJIN 기록·PLC/보호값을 수정하지 않았다. build/test/generator, 시뮬레이터 및 행동시험은 실행하지 않았다.

## 2. I/O·HMI

### 고유 선언과 내부 주소

|신호|원본 선언·문맥·주소|해석 및 미확정|
|---|---|---|
|BELT CONVEYOR  D RUN|0613 RID92 Global, NID15 UID856, Bool SSD AO111, SAD Input SAM=None → I13.7|원시 입력영상, 실제 벨트 운동 증명 아님|
|BELT COVEYOR  D FAULT|0599 RID34 Global, NID15 UID305/307, Bool AO130 Input SAM=None → I16.2|고유 래치 입력. 정상극성/외부 원인 미확정|
|Allarm.motor_client_15_fault|0601 RID35 Global, NID15 UID306/309 Write, Bool AO127 BAD4→0600 RID4 TOD3 → DB3.DBX15.7|Set/Reset 내부 경보, 원시 FAULT와 구분|
|Flag.RESET_ALLARM|0601 RID7 Global, NID15 UID308, Bool AO48 BAD6→0600 RID6 TOD2 → DB2.DBX6.0|공통 내부 Reset, HMI ACK와 별개|
|ON|0599 RID1 Global, NID15 UID304, Bool AO0 Memory → M0.0|심볼명만으로 상수 true로 치환하지 않음|
|hours motors.CLIENT_MOTOR_15_MIN|0615 RID94 Global Int AO448 BAD5→0614 RID5 TOD9, NID15 UID857/859/860/865 → DB9.DBW56|Add1 및 Move0 대상|
|hours motors.CLIENT_MOTOR_15_HOUR|0615 RID96 Global Int AO464 BAD5, NID15 UID863 / NID49 UID2723 Write → DB9.DBW58|Move1·Move0의 두 writer|
|Tag_47 / Tag_48|0613 RID1/RID284 Global Timer AO13/AO17 → T13/T17|공유 시간계수/저장 관련 타이머. HMI 태그·기동감시 지연 아님|
|Flag_Aggiorna_DB|0613 RID13 Global Bool Memory AO15, NID15 UID866 Write → M1.7|저장갱신 요청 관련 내부 Set|

이 고유 참조는 Global이며 Local 입력으로 오인하지 않는다. 0616 RID7/8/12는 Constant Int 1/60/0, RID335는 Constant S5Time S5T#1M(V5632)이다. 값의 저장 형식과 단위를 보존한다. live_index `_7ev` doc527은 Address `%i13.7`·comment `e 14.6 belt conveyor "d"run`, doc563은 `%i16.2`·comment `e19.4 belt coveyor "d"fault`다. 주석 주소를 실행 주소로 사용하지 않는다.

### HMI와 Word 미러

`all-in-one/sources/hmi_plc_tags.csv` line88: BELT_CONVEYOR_D_RUN, DB13,X13.7, PLC, ID003F9. line585: Allarmi_128, DB3,X15.7, PLC, ID0010D. 이는 dde.cfg의 태그 설정이며 실제 화면 표시/통신/ACK·버튼 이벤트/스크립트 검증이 아니다. CL15 기동 HMI 이벤트와 DB9 직접 화면 결속은 미확보다.

0397 HMI Inputs NID1을 직접 대조했다. bit Coil이 아니라 Word Move다.

|전달|선언과 핀|CL15 결속|
|---|---|---|
|IW12→DB13.DBW12|0627 RID19 Tag_183 Word AO96 Input SAM=None; ORef63 W70→Move60.in; rail W21→en; out1 W72→ORef64/0629 RID20 Word AO96 BAD4→0628 RID4 TOD13|byte12~13 범위의 I13.7→DB13.X13.7|
|IW16→DB13.DBW16|0627 RID23 Tag_275 Word AO128; ORef67 W76→Move62.in; out1 W77→ORef68/0629 RID24 Word AO128 BAD4|I16.2→DB13.X16.2 원시 FAULT 미러. DB3.X15.7 유지경보와 별개|

Move60.eno W71→Move61.en, Move61.eno W74→Move62.en 중간 체인과 DisableENO=true 속성을 모두 보존한다. IW14 Move61도 사이에 있으나 CL15 고유 입력은 아니다. Input SAM=None를 PIW/Peripherie 직접접근으로 바꾸지 않는다. FC15 호출/다른 writer/현재 스캔 최종값은 공통 문서의 미확정 경계를 유지한다.

## 3. 제어 구조

### 상위 호출과 제어 소유

0549 Main document1620 NID7: rail W352→Contact350.in, ORef335/RID52 W348→operand. 0692 RID52는 Global ON M0.0이며 NID7 UID335를 명시한다. Contact350.out W351은 CRef331 및 CRef334의 en에 병렬 결속한다. CRef331 RefId80/CodeBlock345 RefId79는 0688 RID79 Motor/Alarm Client TOD9 FC 및 0694 RID80 NID7 UID331 TORID79와 일치한다. CRef334 RefId83/CodeBlock347 RefId82는 0688 RID82 time work motor TOD2 FC 및 0694 RID83 NID7 UID334 TORID82와 일치한다. 한 FC의 ENO를 다른 FC의 순차 허가로 추정하지 않는다. 현재 CPU의 실행주기/실행 여부는 미확인이다.

요청→허가→기동 출력→외부 벨트라는 경로는 CL15 자료에서 확보되지 않았다. 확보된 경로는 외부 접점→I13.7/I16.2→HMI 미러·시간계수·고장 유지경보다. 이름 검색은 181개 IdentXmlPart와 live_index 범위의 경계 탐색이다. 기동 이름 미식별을 모든 간접주소·블록복사·절대쓰기 부재의 증명으로 확대하지 않는다. 외부 수자동/정지/안전/기동 시퀀스를 새로 만들어 넣지 않는다.

### 고유 시간계수: 0304 document1014, FC2 NID15

1. rail W888→Contact884.in; T13 ORef855/RID1 W867→operand. Contact884.out W885→Contact886.in; RUN I13.7 ORef856/RID92 W868→operand.
2. 886.out W887은 Add838.en 및 Ge845.pre로 분기한다. Add838 SrcType Int: MIN ORef857/RID94 W869→in1, Int1 ORef858/RID7 W870→in2, out W871→ORef859/RID94 MIN.
3. Ge845 Int: MIN ORef860 W872→in1, Int60 ORef861/RID8 W873→in2; out W874→Move848.en.
4. Move848.in W876←ORef862/RID7 Int1, out1 W877→ORef863/RID96 HOUR. 즉 HOUR:=1이며 HOUR+1이 아니다.
5. Move848.eno W878→Move851.en; Int0 ORef864/RID12 W879→in, out1 W880→ORef865/RID94 MIN. Move851.eno W881→SCoil854.in, operand W882←ORef866/RID13 M1.7. ENO 연결을 삭제한 단순 독립 대입으로 해석하지 않는다.

### 다른 writer: 0334 document1047, FC2 NID49

T17 ORef2713/RID284 W2724→Contact2739.operand, rail W2741→in, out W2740→Move2698.en. Move2698.eno W2727→2701.en, 2701.eno W2730→2704.en, 2704.eno W2733→2707.en, 2707.eno W2736→2710.en. 마지막 Move2710의 in W2737←ORef2722/RID12 Int0, out1 W2738→ORef2723/RID96 HOUR이므로 DB9.DBW58:=0을 쓴다. 앞 writer들의 필드는 다른 CLIENT 소유이며 이 문서에서 같이 완료로 집계하지 않는다.

공유 0019 FC2 NID58: Contact3120 operand Negated, T13 ORef3115 W3118; out W3121→SdCoil3112.in, S5T#1M ORef3114/RID335 W3117→value, operand W3119←ORef3116/T13. 이는 공유 분 계수 타이머이며 CL15 경보/기동 지연이 아니다. T17/M1.7/M2.0 저장요청·외부 ACK 상세는 SYS-RUNHOURS의 동일 원본 근거를 재사용한다. HOUR 0/1만으로 장기누적 저장 성공이나 운전시간 정확성을 확정하지 않는다.

## 4. 전기 전달 끝점

`all-in-one/sources/Electrical_Rev2.pdf` 실제 PDF91·95·130·133쪽을 직접 렌더하고 각 footer를 시각 확인했다. 네 쪽 모두 Rev2 17.03.2025 / DATA 27.05.2024이며 FG는 각각90·94·129·132다. 아래 도면 기재는 현행 정격/설정 추천이 아니다.

|경로|실제 끝점·역참조|남은 경계|
|---|---|---|
|RUN 외부 접점|FG90/PDF91: +24Vdc10.7→5x20 2A F, X1:308→선90.3→그려진 열린 접점→X1:309→E13.7 /129/7|상대 제어반 단자·접점기기번호·케이블번호/규격 미확보|
|RUN PLC 입력|FG129/PDF130: E13.7, 역참조90/4→입력단자18, CPU515 MOD11|현재 CPU·실장 모듈·배선증거 아님|
|FAULT 외부 접점|FG94/PDF95: +24Vdc10.7→5x20 2A F, X1:346→선94.2→그려진 열린 접점→X1:347→E16.2 /132/3|외부 보호기/고장종류/정상극성 미확정|
|FAULT PLC 입력|FG132/PDF133: E16.2, 역참조94/3→입력단자3, CPU515 MOD12|외부 전력/보호회로와 별개|
|선정 RUN 입력 보조전원|FG129/PDF130: +24Vdc10.7→X21:3012 5x20 2A IST.→129.1→단자19; -0Vdc10.6→단자20|MOD12 별도 전원 상세를 이 페이지로 복제하지 않음|
|기동/정지 출력|CL15 전용 출력·릴레이·외부 모터 전력 경로 미식별|출력 주소·코일 A1/A2·부하접점·케이블을 다른 CLIENT에서 복제하지 않음|

RUN은 FG90 및129의 SPARE 구획에, FAULT는 FG94와 FG132의 해당 SPARE 구획에 포함된다. 특히 FG132는 E16.0~3 SPARE 구획과 E16.6 별도 SPARE가 나뉘며 CL15는 E16.2다. 열린 접점 그림을 현장 정상극성 또는 고장 시 실제 동작으로 확정하지 않는다. 이 입력 접점 회로에는 다른 릴레이의 부하5/9 또는 하단 접점표1/5/9 번호를 이식하지 않는다. 외부 벨트 전력/보호회로 및 승인 시공도와의 최종 대조는 근거 미확보다.

## 5. 알람·복구

0232 document422, FC9 NID15의 모든 고유 핀을 확인했다.

|가지|Part/Wire/ORef/RID|정적 조건|
|---|---|---|
|공통 허가|rail W327→Contact319.in; ON ORef304/RID1 W310→operand; out W320→Contact321/323.in|ON M0.0이 두 가지에 공통|
|Set|FAULT ORef305/RID34 W311→Contact321.operand; out W322→SCoil298.in; ORef306/RID35 W313→operand|ON AND I16.2 → Set DB3.X15.7|
|Reset|FAULT ORef307/RID34 W314→Contact323.operand, operand Negated; out W324→Contact325.in; RESET ORef308/RID7 W315→operand; out W326→RCoil303.in; ORef309/RID35 W317→operand|ON AND NOT I16.2 AND DB2.X6.0 → Reset DB3.X15.7|

네트워크에 타이머 Part는 없다. RUN=0을 고장원인에 추가하거나 T13 S5T#1M를 경보 지연으로 사용하지 않는다. FAULT가 참이면 위 Reset 가지는 성립하지 않는다. 원인 소멸, 내부 유지비트 해제, HMI ACK, 외부 제어반 자체 Reset, 재기동 및 현장 정상복구는 각각 다른 상태다.

Allarmi_128 주소는 래치 비트와 일치한다. 실제 표시 문구·ACK 이벤트·소리·이력/통신은 미확정이다. 공통 경보집계/Reset 생성은 SYS-ALARM 참조 범위를 유지한다. DB3.X15.7이 외부 Belt conveyor D를 직접 정지시키는 writer는 확인하지 못했으므로 직접 정지 인과를 만들지 않는다. 이 문서는 현장 Reset 실행/보호값 변경 절차가 아니다.

## 6. 증상별 읽기 전용 관찰 기준

승인된 담당자가 제공하는 자료의 비교 위치다. 강제출력·바이패스·활선 점검·시뮬레이터·Reset 실행을 제안하지 않는다.

|증상|같은 시각의 관찰 자료|비교 근거·한계|
|---|---|---|
|외부 벨트 RUN인데 화면 정지|I13.7, IW12, DB13.W12/X13.7, HMI ID003F9, 외부 상태|FG90 X1:308/309→FG129 단자18 및0397 Word 미러. 배선/통신/극성 원인 단정 금지|
|FAULT 표시 불일치|I16.2, IW16, DB13.X16.2, DB3.X15.7, Allarmi_128|원시입력/미러/유지경보를 분리, FG94 X1:346/347→FG132 단자3|
|원인이 사라져도 경보 유지|ON, I16.2, DB2.X6.0, DB3.X15.7의 시각별 자료|0232 NOT FAULT와 내부 Reset 조건을 비교. HMI ACK와 동치 아님|
|Reset 요청인데 경보 지속|실제 HMI 이벤트, 내부 Reset 생성, 입력과 경보 전후|고장 입력이 참이면 Reset 조건 불성립; 외부 보호기 복구 증거 별도|
|시간값 1 또는0으로 변경|I13.7,T13,T17,DB9.W56/W58,M1.7,저장 요청/ACK 로그|0304 Move1·0334 Move0. 장기누적 성공/손실을 숫자만으로 판단 금지|
|기동 요구인데 정지|현행 외부 제어반 회로/프로그램, 모드·허가·기동 이벤트와 RUN|전용 출력 주소 미확보. 다른 CLIENT Q61.x를 시험 주소로 삼지 않음|
|도면 SPARE와 실제 사용 상충|현행 승인 도면·단자표찰·명판·외부회로 판본|고정 백업과 현행 설치를 별도로 식별, 과거 주석으로 배선수정 금지|

관찰자·실제 시각/시간대·위치·값/단위·수집장치·프로젝트/도면 판본·자료 출처·비교/배제 결과·승인된 조치·복구 증거를 따로 기록한다. 실제 사용자 운영기록·사진·SEJIN 데이터를 복제하지 않았다.

## 7. 완료·누락·검증 범위

|영역|상태|남은 자료|
|---|---|---|
|설비·자료 기준|적용, 문서작성|외부 Belt conveyor D 실물/현행 동일성|
|I/O·HMI|고유 선언·원시/미러/유지비트 분리 확인|기동 출력, 현재 화면/통신/이벤트|
|제어|고유 래치/시간·다른 writer/상위 호출 선택검토|외부 모드·허가·기동/정지 시퀀스|
|전기 끝점|4쪽 실제 렌더·footer·입력 양끝점 확인|외부 상대 단자·케이블·전력/보호회로|
|알람·복구|고유 S/R와 무타이머 구조 확인|외부 보호원인·ACK/Reset·현장 복구|
|증상 관찰|읽기 전용 비교 기준 작성|실제 관찰값 미취득|
|완료·누락|문서 complete_with_gaps|BC01 동등 구현·게시·현장완료 아님|

필요자료는 현행 CL15 외부 제어반 회로/프로그램·모드와 허가표, 기동/정지 출력 전체 교차참조, X1:308/309/346/347 상대 단자·케이블표, SPARE의 현행 사용 여부, RUN/FAULT 정상상태 증거, HMI 이벤트/스크립트와 외부 시간저장 ACK 자료다. 새 자료 없이 실물 보류를 반복 조사하지 않는다.

도면·래더 비교에 필요한 원본 위치를 준비했지만, 이 ID의 백업 미리보기/선택복원·기록 전후비교·보고서/PDF 기능 구현이나 저장/재읽기/재열기는 실행하지 않았다. 기존 note/repair_observation·미지 필드·다른 설비·초안·저장키를 변경하지 않았다. documentation=complete_with_gaps, static_review=selected_original_xml_and_pdf_reviewed, ui_records=not_run, publication=not_published, tia_compile/live_cpu/field_recovery=not_performed. 로컬 통합은 별도 사용자 Codex 범위이며 부모의 독립 검토/첨부를 기다린다.

### 조사량과 보존 검사

직접 의미 대조는 0232/0304 고유 전체 핀, 0334 CL15 HOUR reset 가지와 선행 ENO 체인, 0397 IW12/IW16 Word 미러, 0549 상위 FC 호출, 0019 T13 가지 및 해당 선언이다. 181개 IdentXmlPart 명명 탐색은 181개 의미검토가 아니다. 실제 PDF4쪽을 시각 검토했다. 아래 선정33파일 전체 byte 해시 및 Git 내용 일치도 33파일 전체 논리/전체 페이지 검토를 뜻하지 않는다.

검사·원형 추출·렌더: `../extracts/CLIENT-CL15/verification.json`, `source-hashes.json`, `declarations.json`, `xml-pins.json`, `live-search.json`, `pdf-91.png`, `pdf-95.png`, `pdf-130.png`, `pdf-133.png`. 쓰기 범위는 본 MD와 배정 extracts뿐이다.

### 선정 원본 SHA256 + 고정 Git blob 전체 표

경로는 `source-mv06/` 기준이다. 각 파일 byte와 `git show abcf31c5030bc7ef8749ed8e869a857f2387a28a:경로` 내용을 직접 비교했다.

|선정 원본 경로|SHA256|고정 Git blob|내용 일치|
|---|---|---|---|
|AGENTS.md|0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2|073164bc6efd5791032d62c71b03b4dab48cb6f8|일치|
|.agents/skills/gme-equipment-rollout/SKILL.md|fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b|9aa820ea6ca15b4e136c9772423b78ed4df6a3d4|일치|
|docs/equipment-standard/WORK-STANDARD.md|05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99|f76a570cc73098632e08759b17934000f7e3a253|일치|
|docs/equipment-standard/WORK-ITEM-TEMPLATE.md|4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586|e546f39535d2b589e80f97db869ac37ce4d05cfd|일치|
|docs/equipment-standard/INVENTORY.json|720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc|587c3748ad9224718f95ba06463fee913dae231d|일치|
|VERSION.json|5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7|fffb51663b7705aec91cb119ca80ee943a4ce758|일치|
|WORKSPACE-HANDOFF.md|215096d997782e78e901dfae36c782937e49611fbeb677a0d3fa50cbecf8d074|dd0b8989d2376c4415bba9bd826fe6754c6b1a12|일치|
|PUBLICATION_STATUS.md|efe4857aec598d90470322cf3962eb3fe1f64947630e1fdf71d1c90134de8740|d76401cf291fc0be681acc51fa898ad3ce46ff78|일치|
|all-in-one/ACTIVE-WORK.md|eff3bbc08ecff41da3beff77f3fec48e7d148708192bcaaab00f34b6a721afc2|6eb947c629b5ddf9c759ef87649451303938864b|일치|
|EXPANSION-WORK.md|ec624de9fd2fcfac861a67fd5e828b25ef46db50bfd7a37ff16e2cb54cd0f7e2|4c42d88ecc2d48269eb23e13a20ebf3721a092a1|일치|
|all-in-one/sources/Electrical_Rev2.pdf|5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6|f610fd7c7ce14ae951b00cff57b969259bfb389d|일치|
|all-in-one/sources/hmi_plc_tags.csv|a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404|cf4c0650e7c7baac350dcb89909b808435704880|일치|
|all-in-one/sources/live_index.json|14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1|e35ccea1f841349c632666c29954b7bcd4f5839e|일치|
|all-in-one/sources/decoded-original/network-map.json|c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60|424430b6b953e43138e5d0a18ca40c949e21cfa1|일치|
|all-in-one/sources/decoded-original/0019-FlgNet.xml|a3301f4d07c2d36aefa6faa6c3559a1cff4565fc6de40cd17e54b548b30c0ce5|f78cfdbf5e717304114660ffbd3bb42cbed6d79d|일치|
|all-in-one/sources/decoded-original/0232-FlgNet.xml|7df6da026fe6991b4a4ca212082829aa5263c3094bb4fe81ebd5c7c0d18a1148|102e93d57e5d6bfb042787237c5d42e2f77b87d5|일치|
|all-in-one/sources/decoded-original/0304-FlgNet.xml|fe6cf41278da9b0fa31a16e8db4a8437bf1db30cc29737ba72f0c05746c66b0b|3020b0f271d5d9d08457a0a8bb1daea790d5b7f1|일치|
|all-in-one/sources/decoded-original/0334-FlgNet.xml|d76007d20f67bcb8f127fef6e7050e0973619a35ef4f5c34c367dc3b3c38932e|7310cc3d9a1324fa17c3c7ea7b8ffe1c62be96fa|일치|
|all-in-one/sources/decoded-original/0397-FlgNet.xml|bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834|4ab8370493c4e28fc1eabeeebe2743d27f0c4021|일치|
|all-in-one/sources/decoded-original/0549-FlgNet.xml|49f7169c33ed7f54559b0801e21a7d618584900972840e91cf51ad032e8febb1|985b5310b43b1015b5dee286aa0e42800564b94b|일치|
|all-in-one/sources/decoded-original/0599-IdentXmlPart.xml|32a693fe12134febbd9f5c7da10c3469ef4d5b164ab8b6bd9ea3867c358936c1|493de77fc827d8f14192ced05d82df3a062f7965|일치|
|all-in-one/sources/decoded-original/0600-IdentXmlPart.xml|20c58ee0383d0b6c275bd2d96abd30af7c5d1f3fff59c7d5034cd758936b57d5|f22a7ededd0576cf379ee19908da067f08d45412|일치|
|all-in-one/sources/decoded-original/0601-IdentXmlPart.xml|04c9481f7381284de689ef5c7ff40d7aea93f2004cd877a4e4f27e47baa6d862|07bcf656fa58e4a305999456644acd24b3dc6bec|일치|
|all-in-one/sources/decoded-original/0613-IdentXmlPart.xml|09d3b1397a987898334218f37e025661af162438582e649f671e7abec443d3cb|c9d19a48e947098914f4d2de3348c05b4f6d37e8|일치|
|all-in-one/sources/decoded-original/0614-IdentXmlPart.xml|c6de26f74d75f5be858a406de75eaf6faf62ba9b89c8f9a085b5dd206e93d294|da0485aa033700f08c8695d30b93ebd2d377d6c7|일치|
|all-in-one/sources/decoded-original/0615-IdentXmlPart.xml|80f4544edca56c6e6bb2713c758c92ade9202255110074931e03fe34d0d0801a|49eb86fe01feb83de8c0864b21493d305aff8b20|일치|
|all-in-one/sources/decoded-original/0616-IdentXmlPart.xml|650b53354a0c8443d94adc5bd6a860d3c5313014a52e0fb98a5656a65b58cc0d|9f7fdd5f93ac149c139a054ebb34f63c632ef7fd|일치|
|all-in-one/sources/decoded-original/0627-IdentXmlPart.xml|08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb|61ebc0abbb2ca160e11e1da400a3f14a397d8bc5|일치|
|all-in-one/sources/decoded-original/0628-IdentXmlPart.xml|9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd|170ca5c72599edc7ea7eefe651c3680ce325e76a|일치|
|all-in-one/sources/decoded-original/0629-IdentXmlPart.xml|67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972|058129bb01e27f7a6a0d0293f332d745e5bab74e|일치|
|all-in-one/sources/decoded-original/0688-IdentXmlPart.xml|ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda|463585759f1ecd94f32362b4fefb000a152f5773|일치|
|all-in-one/sources/decoded-original/0692-IdentXmlPart.xml|bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037|737785d03b5fad43c5b4d451955726d800edb1c0|일치|
|all-in-one/sources/decoded-original/0694-IdentXmlPart.xml|757ccebdf32d0a168dd787bfa735fe6494eac4c4a9f7a5adc63898a88e8b152d|c45e8f3ca4129dc06734f6a12ef79e6ed6528a7d|일치|
