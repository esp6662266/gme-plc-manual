# CLIENT-CL14 Shredder 2 — 7영역 원본 조사 초안

## 핵심 확인·상충·누락

- 외부 모터 채널 CLIENT-CL14 한 개만 조사했다. CYL-CL 공압 실린더, Shredder 1, Primary shredder와 동일 실물로 병합하지 않는다.
- RUN **I13.6**, FAULT **I16.1**, 내부 유지경보 **DB3.DBX15.6**, 시간 **DB9.DBW52/54**를 고유 XML 선언·NID·RID·UID·Part/Wire로 독립 확인했다.
- OEM FG90/94/129/132 = 실제 PDF91/95/130/133을 직접 렌더·확인했다. RUN X1:306/307→MOD11 입력17, FAULT X1:344/345→MOD12 입력2. 모두 해당 회로에 **SPARE** 표시가 있다. 이름과 배선도의 존재가 실제 사용을 증명하지 않는다.
- 0231 경보는 ON AND FAULT Set / ON AND NOT FAULT AND RESET_ALLARM Reset이며 고유 타이머가 없다. 0303 시간값은 MIN+1, MIN≥60에서 **HOUR := 1**, MIN := 0이며 0334의 **HOUR := 0** writer가 별도로 있다. 누적 HOUR+1로 바꾸지 않는다.
- `start client motor 14` 명명 출력은 live_index와 XML 선언 검색에서 식별하지 못했다. 인접 채널 Q61.x를 순번으로 배정하지 않는다. 기동·정지 출력, 외부 제어반 내부 허가·보호·순서, 현장 정상극성·현재 CPU는 미확정이다.
- RUN의 과거 comment `e 14.5` 및 FAULT의 `e19.3`과 실제 Address I13.6/I16.1을 구분한다.
- 공통근거 색인은 [CLIENT-CL09](CLIENT-CL09-DOTS-DRAFT.md), [CLIENT-CL04](CLIENT-CL04-DOTS-DRAFT.md), [SYS-RUNHOURS](SYS-RUNHOURS-DOTS-DRAFT.md), [SYS-ALARM](SYS-ALARM-DOTS-DRAFT.md), [SYS-HMI](SYS-HMI-DOTS-DRAFT.md)다. 같은 고정입력의 상위 호출/공유 타이머/Word 미러/저장 경계를 연결 재사용하며 이 설비 고유 주소·핀·끝점은 재확인했다.

## 1. 설비·자료 기준

대상은 `docs/equipment-standard/INVENTORY.json#/catalog/68`, CLIENT-CL14, Shredder 2, client, 외부 연동, 부모 없음, phase2이다. GME PLC가 받는 외부 RUN/FAULT 및 그 처리 범위의 문서다. 외부 파쇄기 본체·모터·드라이브·제어반의 실물 동일성, 제조사·명판·안전인증을 확인한 문서가 아니다. 다른 CLIENT 또는 부품 완료를 함께 집계하지 않는다.

기준은 읽기 전용 `source-mv06`, Git **abcf31c5030bc7ef8749ed8e869a857f2387a28a**, **v1.12.0**. 새 로컬 통합/게시 결과의 검증이 아니다. NNNN은 `all-in-one/sources/decoded-original/NNNN-FlgNet.xml` 또는 `NNNN-IdentXmlPart.xml` 약칭이다. XML 파일번호·document_id·NID는 별개이며 같은 UID라도 다른 문맥을 연결하지 않는다.

- 실제 착수/지시 읽기: 2026-10-11 12:31:42 UTC
- 고유 선언/논리 선택 검토: 12:32:00~12:32:21 UTC 도구 실행 기록
- PDF 렌더 및 실제 시각 검토: 12:32:31~12:32:37 UTC
- 상위 호출/선언·미러·타이머 재확인: 12:32:47~12:33:14 UTC
- 실행 모델/추론 런타임 증명: 미확인
- 원본 HEAD 일치, Git 상태 공란 확인. 원본·중지 자산·PLC·현장·보호값·SEJIN·공용대장 변경 없음. 원본 generator/build/test, 시뮬레이터, 행동시험 실행 없음. 작성 범위는 배정 MD와 extracts뿐이다.

## 2. I/O·HMI

### 2.1 선언과 주소

|대상|고유 선언/문맥|주소·해석|
|---|---|---|
|SHREDDER 2 RUN|0613 RID86 Global Bool, SSD AO110, SAD Input SAM=None; NID14 UID802|I13.6 원시 입력영상. 실제 파쇄기 회전/생산 증명과 구분|
|SHREDDER 2FAULT|0599 RID32 Global Bool AO129, Input SAM=None; NID14 UID287/289|I16.1 원시 고장 입력. 외부 고장 종류·현장 정상극성 미확정|
|Allarm.motor_client_14_fault|0601 RID33 Global Bool AO126, BAD4→0600 RID4 TOD3; NID14 UID288/291 Write|DB3.DBX15.6 유지경보|
|Flag.RESET_ALLARM|0601 RID7 Global Bool AO48, BAD6→0600 RID6 TOD2; NID14 UID290|DB2.DBX6.0 공통 내부 Reset. HMI ACK/외부 Reset과 별개|
|ON|0599 RID1 Global Bool Memory AO0; NID14 UID286|M0.0, 이름만으로 항상 true 상수 취급 금지|
|CLIENT_MOTOR_14_MIN|0615 RID88 Global Int AO416, BAD5→0614 RID5 TOD9; NID14 UID803/805/806/811|DB9.DBW52, Add1 및 Move0 writer|
|CLIENT_MOTOR_14_HOUR|0615 RID90 Global Int AO432 BAD5; NID14 UID809, NID49 UID2721 Write|DB9.DBW54, Move1과 Move0 별도 writer|
|Tag_47 / Tag_48|0613 RID1/RID284 Global Timer AO13/AO17|T13/T17, 시간계수/저장용 공유 PLC 타이머. HMI 태그나 CL14 기동감시 아님|
|Flag_Aggiorna_DB|0613 RID13 Global Bool Memory AO15; NID14 UID812 Write|M1.7, 저장 갱신 요청 관련 내부 Set|

선정 선언의 신호는 Global이며 0616의 Int1(RID7), Int60(RID8), Int0(RID12), S5T#1M(RID335)은 Constant다. Local 변수나 이전 설비의 RID로 바꾸지 않았다. 별도의 아날로그 환산/스케일링은 이 고유 Bool 입력 논리에서 확인하지 못했으며 시간 Int 연산을 아날로그 환산으로 분류하지 않는다.

`live_index.json` `_7ev` doc526은 RUN `%i13.6`, comment `e 14.5 shredder 2 run`; doc562는 FAULT `%i16.1`, comment `e19.3 shredder 2fault`다. 설명 속 옛 주소로 실제 선언 주소를 교체하지 않는다.

### 2.2 HMI 및 Word 미러

`hmi_plc_tags.csv`: `SHREDDER_2_RUN` = `DB13,X13.6`, PLC, ID003FA. `Allarmi_127` = `DB3,X15.6`, PLC, ID0010E. CSV는 dde.cfg 태그 설정이며 현재 화면·통신·버튼 이벤트·권한·ACK/경보이력 검증이 아니다. CL14 기동 이벤트, 외부 Reset 이벤트, 시간 DB9 직접 HMI 결속은 미확보다.

0397 HMI Inputs NID1의 **Word 복사**를 직접 확인했다.

- RUN 포함: 0627 RID19 `Tag_183`, Word AO96, Input SAM=None → IW12. ORef63 W70→Move60.in, rail W21→en, out1 W72→ORef64/0629 RID20 Word AO96 BAD4→0628 RID4 TOD13 → DB13.DBW12. 이 byte12~13 복사에 I13.6이 포함된다.
- FAULT 포함: 0627 RID23 `Tag_275`, Word AO128 → IW16. ORef67 W76→Move62.in, out1 W77→ORef68/0629 RID24 Word AO128→DB13.DBW16. I16.1이 포함된다.
- Move60.eno W71→Move61.en, Move61.eno W74→Move62.en이다. Move60/61/62의 `DisableENO=true` 속성과 실제 eno/en 배선을 모두 보존한다. 중간 IW14/DB13.W14도 같은 체인에 있으나 이를 CL14 전용 입력으로 소유시키지 않는다.

I16.1의 DB13 raw 미러와 DB3.X15.6 유지경보는 주소·의미가 다르다. Bool별 Coil 쓰기 또는 PIW/Peripherie 직접 접근으로 바꾸지 않는다. FC15 상위 호출과 다른 writer/최종 스캔값 미확정 경계는 기존 공통근거를 유지한다.

## 3. 제어 구조

### 3.1 상위 호출과 소유

0549 Main NID7(색인 doc1620): rail W352→Contact350.in, ORef335/RID52 W348→operand(0692 ON M0.0), out W351→CRef331.en 및 CRef334.en **병렬** 연결이다. CRef331 RefId80/CodeBlock345 RefId79→0688 RID79 Motor/Alarm Client TOD9 FC; 0694 RID80 NID7 UID331 TORID79. CRef334 RefId83/CodeBlock347 RefId82→0688 RID82 time work motor TOD2 FC; 0694 RID83 NID7 UID334 TORID82. 앞 FC의 ENO를 뒤 FC의 순차 허가로 해석하지 않는다. 현재 CPU 실행·주기·TIA 컴파일은 미수행이다.

외부 RUN/FAULT 관찰, 유지경보, 시간계수가 확인된 직접 소유다. `start client motor 14`는 XML IdentXmlPart 181개와 live_index 명명 검색에서 미식별이다. 이 검색은 절대주소·간접쓰기·블록복사 부재 증명이 아니다. Q61.x를 번호로 배정하거나 내부 경보가 외부 모터를 정지시킨다고 단정할 수 없다. 수자동·기동/정지·상호허가·외부 제어기 보호 순서는 미확정이다.

### 3.2 RUN 시간 처리: 0303, FC2 NID14, document1013

1. rail W834→Contact830.in; T13 ORef801/RID1 W813→operand. Contact830.out W831→Contact832.in; RUN ORef802/RID86 W814→operand.
2. Contact832.out W833은 Add784.en과 Ge791.pre에 분기한다. Add784 SrcType Int: MIN ORef803/RID88 W815→in1, Int1 ORef804/RID7 W816→in2, out W817→MIN ORef805/RID88. MIN := MIN+1.
3. Ge791 SrcType Int: MIN ORef806 W818→in1, Int60 ORef807/RID8 W819→in2. out W820→Move794.en.
4. Move794.in W822/ORef808/RID7=Int1; out1 W823/ORef809/RID90→HOUR. **HOUR := 1**, HOUR+1이 아니다.
5. Move794.eno W824→Move797.en; in W825/ORef810/RID12=Int0; out1 W826/ORef811/RID88→MIN. Move797.eno W827→SCoil800.in, operand W828/ORef812/RID13=M1.7. ENO 체인을 생략하지 않는다.

0334 FC2 NID49(document1047)는 다른 writer다. rail W2741→Contact2739; T17 ORef2713/RID284 W2724→operand, out W2740→Move2698.en. Move2698.eno W2727→Move2701.en→eno W2730→Move2704.en→eno W2733→Move2707.en. Move2707.in W2734/ORef2720/RID12=Int0, out1 W2735/ORef2721/RID90=CL14 HOUR(DB9.W54). 주변 11/12/13/15 필드의 존재를 별도 catalog 설비 완료로 세지 않는다.

### 3.3 공유 시간 및 저장 경계

0019 FC2 NID58: rail W3122→Contact3120.in, operand는 Negated T13(ORef3115/RID1/W3118). out W3121→SdCoil3112.in; value W3117/ORef3114/RID335=0616 S5Time S5T#1M(V5632); operand W3119/ORef3116=T13. 분 계수 공유 타이머이며 CL14 고장 지연·재기동 대기 시간으로 사용하지 않는다.

T17/M1.7/외부 저장 핸드셰이크는 동일 고정입력 SYS-RUNHOURS 문서의 공통근거를 연결한다. HOUR가 0/1로 움직인다는 사실로 외부 장기누적 성공, 정확한 실제 운전시간, 저장 ACK까지 확인했다고 할 수 없다. 보호값·주기 권고는 작성하지 않는다.

## 4. 전기 전달 끝점

원본 `all-in-one/sources/Electrical_Rev2.pdf` 실제 4쪽을 직접 렌더했다. 각 footer를 개별 확인: **FG90/PDF91, FG94/PDF95, FG129/PDF130, FG132/PDF133 모두 Rev2 17.03.2025, DATA 27.05.2024**, NORMA IEC, TOT262. FG 번호를 실제 PDF 페이지와 혼동하지 않는다.

|경로|실제 도면 끝점|미확정 경계|
|---|---|---|
|RUN 외부 입력|FG90/PDF91: +24Vdc10.7→5x20 2A F/X1:306→선90.2→그려진 열린 접점→X1:307→E13.6 /129/6|상대 외부 제어반 단자·접점기기 식별·케이블번호/규격 없음|
|RUN PLC 입력|FG129/PDF130: E13.6 역참조90/3→입력단자17, CPU515 MOD11 표기|현재 CPU/실제 장착 모듈/결선 확인 아님|
|FAULT 외부 입력|FG94/PDF95: +24Vdc10.7→5x20 2A F/X1:344→선94.1→열린 접점→X1:345→E16.1 /132/2|고장 종류·외부 보호기·현장 극성·상대단자 미확정|
|FAULT PLC 입력|FG132/PDF133: E16.1 역참조94/1→입력단자2, CPU515 MOD12 표기|입력회로가 외부 보호회로 전체를 설명하지 않음|
|RUN 입력 모듈 보조전원|FG129: +24Vdc10.7→X21:3012 5x20 2A IST.→129.1→단자19, -0Vdc10.6→단자20|설계도 표기 정격이며 현행 퓨즈/보호 설정 추천 아님|
|기동/정지 출력|CL14 고유 출력 선언·실제 writer·전기 릴레이 끝점 미확보|PLC 출력모듈/릴레이 코일·부하접점·외부 제어반 기동단자·전력회로 필요|

FG90 전체 RUN 묶음, FG94 왼쪽 FAULT 묶음, FG129 입력 묶음, FG132 E16.0~3 묶음의 SPARE 경계를 시각 확인했다. 현재 사용 여부·실물 존재를 이름으로 확정하지 않는다. 열린 접점 도면을 현장 정상상태로 추정하지 않는다. 이 입력회로에는 타 설비의 릴레이 부하5/9나 하단 접점표1/5/9를 가져오지 않았다.

`Electrical_Can_Decoating_20241118.pdf`는 텍스트에서 SHREDDER 2 이름 일치 0건이었다. 이 PDF는 이번 시각 검토 대상이 아니며 전수 의미검토·외부 제어반 부재 증명이 아니다. 실제 모터 명판/외부 제어반·케이블표·현행 배선사진이 추가되어야 끝점을 완성할 수 있다.

## 5. 알람·복구

0231 `motor/alarm client`, FC9 NID14, document421:

- 공통 전단: rail W309→Contact301.in, ON ORef286/RID1 W292→operand, out W302가 Contact303/305.in으로 분기.
- Set: FAULT I16.1 ORef287/RID32 W293→Contact303.operand; out W304→SCoil280.in; operand W295/ORef288/RID33=DB3.X15.6. **ON AND I16.1 → Set**.
- Reset: I16.1 ORef289/RID32 W296→Contact305.operand(**Negated**), out W306→Contact307.in; RESET_ALLARM ORef290/RID7 W297→operand; out W308→RCoil285.in; operand W299/ORef291/RID33=같은 DB3.X15.6. **ON AND NOT I16.1 AND DB2.X6.0 → Reset**.

이 네트워크에는 타이머 Part, RUN=0 조건 또는 기동실패 감시가 없다. T13/T17을 경보 지연으로 복제하지 않는다. I16.1이 참이면 이 Reset 가지는 성립하지 않는다. 원시 원인 소멸, PLC 유지경보 해제, HMI Allarmi_127 ACK, 외부 제어반 Reset, 재기동, 현장 정상복구는 서로 다른 상태다.

공통 DB3 집계/RESET_ALLARM 생성의 의미는 SYS-ALARM 동일 원본 근거를 연결한다. 실제 표시문구·경보 이력·소리·ACK 버튼, 외부 파쇄기의 복구/안전 순서는 미확정이다. 이 비트가 외부 기동 출력을 직접 끊는 writer는 확보하지 못했으므로 정지 인과를 만들지 않는다.

## 6. 증상별 읽기 전용 관찰 기준

현장 조작 지침이 아니라 승인된 담당자가 제공하는 기록의 비교 위치다. 강제출력·바이패스·활선 점검·보호값 변경·Reset 실행을 제안하지 않는다.

|증상|동일 시각의 관찰 항목|비교 근거·판정 경계|
|---|---|---|
|기동 표시인데 파쇄기 정지|현재 프로젝트 식별, 실제 출력/writer와 외부 제어반 상태, I13.6, HMI 이벤트|기동 출력 자체 미확정. CL 번호로 Q61.x를 배정 금지|
|현장 RUN인데 HMI 표시 다름|I13.6, IW12, DB13.W12/X13.6, SHREDDER_2_RUN|FG90 X1:306/307→FG129 단자17와 0397 Word 미러를 구분|
|FAULT 입력과 화면 경보 차이|I16.1, IW16, DB13.W16/X16.1, DB3.X15.6, Allarmi_127|원시 미러와 유지경보는 별개. 외부 고장 상태를 문구만으로 확정 금지|
|고장 소멸 후 경보 유지|ON M0.0, I16.1, DB2.X6.0, DB3.X15.6의 시각별 값|0231 S/R 조건을 비교. HMI ACK가 PLC Reset이라는 가정 금지|
|시간값이 1/0으로 보임|T13/T17, RUN, DB9.W52/W54, M1.7, 저장 로그|0303 Move1/0334 Move0 구조. 누적시간 불량이나 저장 성공을 단독 판정 금지|
|도면과 주소/명칭 다름|현행 도면·프로젝트 판본, X1/모듈 표찰, 실물 기록|옛 comment e14.5/e19.3 및 SPARE 표기 보존. 임의 결선 변경 금지|

관찰자·실제 시각/시간대·위치·값/단위·장치·프로젝트/도면 판본·사진/로그 출처·비교/배제 결과·승인된 조치와 복구 증거를 별도로 남긴다. 실제 운영/SEJIN 기록·사진은 이번 산출물에 복제하지 않았다.

## 7. 완료·누락·검증 범위

|영역|상태|남은 자료|
|---|---|---|
|설비·자료 기준|적용, 문서 작성|Shredder 2 실물/명판/외부 제어반 동일성|
|I/O·HMI|입력·경보·시간·Word 미러 확인|기동 출력·HMI 이벤트·현재 통신|
|제어 구조|고유 FC9/FC2와 선택 공통 호출 확인|실제 기동/정지·수자동·외부 허가/보호/순서|
|전기 끝점|OEM 4쪽의 두 입력 끝점 확인|외부 상대단자/접점기기·케이블/출력/전력회로|
|알람·복구|고유 Set/Reset 및 무타이머 확인|현장 원인·ACK·외부 Reset·안전 복구 증거|
|증상 관찰|읽기 전용 비교 기준 작성|실제 값과 관찰기록 미취득|
|완료·누락|documentation complete_with_gaps|UI·게시·TIA·CPU·현장 완료 아님|

추가자료: 외부 파쇄기 제어반의 현행 회로/프로그램·명판, X1:306/307/344/345 상대단자와 케이블표, SPARE 현재 사용 여부, 기동/정지의 절대/간접주소 교차참조, HMI 화면 이벤트/ACK·스크립트, 현장 정상극성과 보호·복구의 승인 자료. 새 증거 없는 동일 보류 재검색은 하지 않는다.

도면·래더 비교의 원본 위치만 준비했다. 백업 미리보기/선택복원, 기록 전후비교, 관찰 보고서/PDF 구현·저장·재읽기·재열기, PC/모바일 UI·회귀·게시 검사는 미수행이다. note/repair_observation 미지 필드·초안·저장키와 기존 완료분은 변경하지 않았다. 로컬 통합은 사용자 Codex 담당이며 이 문서는 통합 완료 증거가 아니다.

최종 상태: documentation `complete_with_gaps`; static_review `selected_original_xml_and_pdf_reviewed`; ui_records `not_run`; publication `not_published`; tia_compile/live_cpu/field_recovery `not_performed`. 부모 독립 검토·첨부 대기.

### 검증 범위의 정확한 구분

원본 명명 선언 181개 검색은 검색 경계이며 181개 논리 전수 의미검토가 아니다. 직접 의미 검토는 0231/0303 전체 고유 핀, 0334 CL14 zero writer와 전단 ENO, 0397 IW12/IW16 Word 미러, 0549 관련 호출, 0019 T13 및 선택 선언이다. PDF는 실제 4쪽 시각 확인만 완료했다. SHA256/Git blob 내용 일치는 파일 byte 검증이며 모든 본문 의미검토/현재 현장 일치의 증명이 아니다.

검사·해시·선언검색·정렬 XML·렌더를 `../extracts/CLIENT-CL14/`에 저장했다. 해시 시각과 최종 선정 개수는 아래 표 및 verification.json에 기록한다.

### 선정 원본 SHA256 + 고정 Git blob 전체 표

경로는 source-mv06 기준. 각 원본 byte를 고정 Git blob 내용과 직접 비교했다.

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
|`all-in-one/sources/Electrical_Can_Decoating_20241118.pdf`|`3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd`|`0ee6b6f8361c5790864dbba4bbd9d55e8e7c08f8`|일치|
|`all-in-one/sources/hmi_plc_tags.csv`|`a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404`|`cf4c0650e7c7baac350dcb89909b808435704880`|일치|
|`all-in-one/sources/live_index.json`|`14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1`|`e35ccea1f841349c632666c29954b7bcd4f5839e`|일치|
|`all-in-one/sources/decoded-original/network-map.json`|`c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60`|`424430b6b953e43138e5d0a18ca40c949e21cfa1`|일치|
|`all-in-one/sources/decoded-original/0231-FlgNet.xml`|`80c86d9cff3f9cc6042fbbbb4fd75530b7e05c0a3787a517e8e73151013103e5`|`267788b122668724b01c1285a35b2f84e7e5b39d`|일치|
|`all-in-one/sources/decoded-original/0303-FlgNet.xml`|`33ca0f156e3afa2e758203fd1ec594c8f95f34682659cb747acbf8168007d88b`|`a688d6b81bbb0969fc6ea3973fbc00ee15b9b93d`|일치|
|`all-in-one/sources/decoded-original/0334-FlgNet.xml`|`d76007d20f67bcb8f127fef6e7050e0973619a35ef4f5c34c367dc3b3c38932e`|`7310cc3d9a1324fa17c3c7ea7b8ffe1c62be96fa`|일치|
|`all-in-one/sources/decoded-original/0397-FlgNet.xml`|`bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834`|`4ab8370493c4e28fc1eabeeebe2743d27f0c4021`|일치|
|`all-in-one/sources/decoded-original/0019-FlgNet.xml`|`a3301f4d07c2d36aefa6faa6c3559a1cff4565fc6de40cd17e54b548b30c0ce5`|`f78cfdbf5e717304114660ffbd3bb42cbed6d79d`|일치|
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

선정 원본 **34개** 전체 byte 일치. 실제 해시/검사 시각: 2026-10-11T12:35:52.615211+00:00.
