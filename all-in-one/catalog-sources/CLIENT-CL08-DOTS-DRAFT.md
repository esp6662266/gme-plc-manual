# CLIENT-CL08 Shredder vibration feeder 자체 원본 조사 초안

## 핵심 확인·상충·누락

- 고유 대상은 CLIENT-CL08 한 개다. 외부 파쇄기 진동공급기 채널이며 CYL-CL08 공압 실린더나 CLIENT-CL03 Impact vibration feeder와 병합하지 않는다.
- RUN I13.2, FAULT I15.5를 고유 XML 선언, HMI 주소 및 실제 OEM PDF90/94/130/132에서 독립 확인했다. RUN은 X1:298/299, 선89.3, PLC 모듈 단자13; FAULT는 X1:336/337, 선93.2, PLC 단자36이다.
- **출력 선언과 실행을 분리:** `start client motor 8`는 백업 심볼 Q61.4다. 현재 확보한 XML에서 그 이름의 호출·쓰기와 Q61.4의 전기 출력 끝점은 식별하지 못했다. 명명만으로 실제 기동 명령·허가·정지 제어를 완성하지 않는다.
- **상충 보존:** 심볼 설명의 과거 `e 13.7`/`e 18.5`는 실제 백업 주소 I13.2/I15.5와 다르다. 확인 도면 네 페이지에는 SPARE 범위가 있다. 이름과 회로 도해만으로 실제 연결·사용중임을 단정하지 않는다.
- **시간계수의 의미:** 0299는 MIN+1과 HOUR:=1이며 HOUR 누적 ADD가 아니다. 별도 0333은 HOUR:=0이다. 외부 저장·누적 성공은 미확정이다.
- 공통 근거는 동일 고정입력의 [CLIENT-CL04](CLIENT-CL04-DOTS-DRAFT.md)를 인덱스로, [SYS-RUNHOURS](SYS-RUNHOURS-DOTS-DRAFT.md)의 공통 분 타이머·저장 핸드셰이크, [SYS-ALARM](SYS-ALARM-DOTS-DRAFT.md)의 공통 Reset/집계, [SYS-PLC-IO](SYS-PLC-IO-DOTS-DRAFT.md)와 [SYS-HMI](SYS-HMI-DOTS-DRAFT.md)의 호출·이벤트 경계를 연결 재사용했다. CL08 고유 선언·핀·HMI 주소·실제 전기 끝점은 직접 확인했다.

## 1. 설비·자료 기준

`docs/equipment-standard/INVENTORY.json#/catalog/64`: CLIENT-CL08, Shredder vibration feeder, kind client, 외부 연동, 부모 없음, phase2, physical identity 미확정. 공정 본체·외부 모터·보호반의 동일성은 아직 증명되지 않았다. 주변 Shredder 1이나 다른 feeder를 이 ID의 하위 완료로 세지 않는다.

고정 원본은 읽기 전용 `source-mv06`, Git `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, 프로그램 v1.12.0이다. 이후 Codex 통합·게시를 이 문서의 검증으로 주장하지 않는다. NNNN 약칭은 `all-in-one/sources/decoded-original/NNNN-FlgNet.xml` 또는 지정한 `NNNN-IdentXmlPart.xml`이다. document_id, NID, 파일번호는 별개다. live_index/network-map은 원본 추출 색인이며 실행·현재값이 아니다.

실제 작업 시각(UTC): 착수 2026-10-11 12:23:05; XML 선언 추출 12:23:24~12:23:50; 실제 PDF 렌더 확인 12:24:02~12:24:09; 해시·핀 검사 12:25:28.157437. 최종 문서 검사 시각은 검사 JSON에 추가한다. 실행 모델/추론 런타임 증명은 미확인이다.

원본 AGENTS/스킬/WORK-STANDARD/WORK-ITEM-TEMPLATE/INVENTORY 및 최신 기록의 고정 스냅샷을 읽었다. 원본 Git 상태는 빈 출력이며 원본·공통 코드·공개대장·현장·보호값·SEJIN·운영기록 변경이 없다. 원본 generator/build/test, 시뮬레이터 작성·실행·행동시험, TIA/CPU 접속을 수행하지 않았다.

## 2. I/O·HMI

### 고유 선언과 주소

|신호|선언·NID/RID/UID 근거|주소/형식·해석|
|---|---|---|
|SHREDDER VIBRATIONFEEDER RUN|0613 Global RID50, NID8 UID478, SSD AO106, SAD Input SAM=None|I13.2 Bool 입력영상. 실제 진동·투입량 자체를 증명하지 않음|
|SHREDDER VIBRATIONFEEDER FAULT|0599 Global RID20, NID8 UID179/181, AO125, Input SAM=None|I15.5 Bool 원시 고장 입력. 정상극성 미확정|
|start client motor 8|live_index `_7ev` doc482 Name/Address/Datatype/Comment|Q61.4 Bool, `it should be free but it is used`; 심볼 선언 수준, XML writer 미확보|
|Allarm.motor_client_08_fault|0601 Global RID21, AO120, BAD4→0600 RID4 TOD3, NID8 UID180/183 Write|DB3.DBX15.0 Bool 유지경보. 물리 FAULT와 별개|
|Flag.RESET_ALLARM|0601 Global RID7, AO48, BAD6→0600 RID6 TOD2, NID8 UID182|DB2.DBX6.0 Bool 공통 내부 Reset. HMI 버튼 그 자체가 아님|
|ON|0599 Global RID1, AO0, Memory, NID8 UID178|M0.0 Bool. 이름을 상수 true로 치환하지 않음|
|CLIENT_MOTOR_8_MIN|0615 Global RID52, AO224, BAD5→0614 RID5 TOD9; NID8 UID479/481/482/487|DB9.DBW28 Int, ADD 및 Move0 writer|
|CLIENT_MOTOR_8_HOUR|0615 Global RID54 AO240 BAD5; NID8 UID485 및 NID48 UID2657 Write|DB9.DBW30 Int, Move1과 Move0, 누적시간 ADD 아님|
|Tag_47 / Flag_Aggiorna_DB|0613 Global RID1 Timer AO13 / RID13 Bool Memory AO15; NID8 UID477/488|T13 / M1.7 공통 시간계수·저장 요청|
|Tag_48|0613 Global RID284 Timer AO17; NID48 UID2651|T17, CL08 HOUR 초기화 조건에 사용|

해당 핵심 접근은 Global이며 Int 1/60/0 및 S5T#1M은 Constant다. 다른 블록 Local 선언 또는 동일 숫자의 RID/UID를 이름만으로 결속하지 않았다. DB 주소는 bit offset AO와 BAD→TOD를 함께 확인해 계산했다.

### HMI 전달과 한계

`all-in-one/sources/hmi_plc_tags.csv`의 `SHREDDER_VIBRATIONFEEDER_RUN`은 `DB13,X13.2`, Access Name PLC, ID003FE다. `Allarmi_121`은 `DB3,X15.0`, PLC, ID00114다. 이 ID는 CSV 내부 식별자이며 121을 외부 장치 오류코드로 바꾸지 않는다.

0397 HMI Inputs NID1의 Move60이 IW12→DB13.DBW12를 **Word 전체** 복사하므로 I13.2가 DB13.X13.2 범위에 포함된다. 0627 RID19/UID63 Tag_183는 Word Input AO96, SAM=None이며 PIW/Peripherie 접근이 아니다. 0629 RID20/UID64는 Global Word AO96, BAD4→0628 TOD13이다. W21 rail→Move60.en; ORef63→W70→Move60.in; Move60.out1→W72→ORef64. Move60에는 DisableENO=true 속성이 있으면서 W71의 eno→Move61.en 연결도 보존되어 있다. 이를 지우거나 CL08 전용 Bool 코일로 설명하지 않는다. 상위 FC15 호출 및 다른 writer/현재 스캔 최종값은 공통 근거 범위다.

CSV 설정은 현재 통신·표시 문자열·클릭 이벤트·권한·ACK 처리를 증명하지 않는다. DB9 직접 태그와 Q61.4 기동 이벤트는 이번 검색에서 식별되지 않았다. 0401 HMI 출력미러를 Q61.4의 실제 기동 writer로 대체하지 않는다.

## 3. 제어 구조

### 공통 호출, CL08 소유 경계

0549 Main document1620 NID7: W352 rail→Contact350.in; ORef335/RID52(0692 ON=M0.0)→W348→operand; out W351은 CRef331.en과 CRef334.en 등에 병렬 분기한다. 0688 RID79는 Motor/Alarm Client FC9, NID7 UID345 Call; 0694 RID80/NID7 UID331은 해당 인터페이스, 0549 CRef331/RefId80 내부 CodeBlock345/RefId79와 결속한다. 0688 RID82는 time work motor FC2, UID347 Call; 0694 RID83/UID334 및 CRef334/CodeBlock347도 직접 대조했다. 앞 FC의 ENO로 다음 FC가 직렬 허가되는 구조가 아니다.

백업에서 확인한 CL08 직접 경로는 고장 관찰·래치와 RUN 기반 시간계수다. 별도 모터 FB의 기동/정지 호출, 수자동·외부 준비·허가·인터록·실제 출력 연결은 미확정으로 남긴다.

### 0299 시간계수 고유 핀

FC2, document1009, NID8:

1. W510 rail→Contact506. T13 ORef477/RID1→W489→506.operand. 506.out→W507→Contact508.in. RUN ORef478/RID50(I13.2)→W490→508.operand. 508.out W509는 Add460.en과 Ge467.pre로 분기한다.
2. Add460은 SrcType Int: MIN ORef479/RID52→W491→in1; Int1 ORef480/RID7→W492→in2; out→W493→ORef481/RID52(MIN). MIN:=MIN+1.
3. Ge467 SrcType Int: MIN ORef482→W494→in1, Int60 ORef483/RID8→W495→in2; out W496→Move470.en.
4. Int1 ORef484/RID7→W498→Move470.in; out1 W499→ORef485/RID54(HOUR). **HOUR:=1이며 HOUR+1이 아니다.**
5. Move470.eno W500→Move473.en; Int0 ORef486/RID12→W501→Move473.in; out1 W502→ORef487/RID52(MIN). Move473.eno W503→SCoil476.in; operand W504/ORef488/RID13는 M1.7을 Set한다. ENO 의존을 보존한다.

Constant 1/60/0은 0616 RID7/8/12, 각각 NID8 UID480·484/483/486에서 확인했다. 시간계수는 진동 크기·속도·무응답 보호값 환산이 아니다.

### 공통 타이머 및 별도 초기화

0019 FC2 NID58: Contact3120의 operand NOT는 T13 ORef3115/RID1/W3118. out W3121→SdCoil3112.in; value W3117/ORef3114/RID335는 0616의 S5Time `S5T#1M`(V5632); operand W3119/ORef3116은 T13이다. 공통 분 시간계수용 원문을 확인했으며 CL08 기동 지연/고장 지연으로 복제하지 않는다. CPU 주기·실시간 정확도는 미확인이다.

0333 FC2 document1046, NID48: T17 ORef2651/RID284→W2662→Contact2677, out W2678→Move2636.en. Move2636.eno W2665→Move2639.en, Move2639.eno W2668→Move2642.en. CL08 가지는 Int0 ORef2656/RID12→W2669→Move2642.in, out1 W2670→ORef2657/RID54(HOUR). 따라서 HOUR:=0이라는 다른 writer가 있다. 뒤쪽 ENO는 다른 채널로 이어지나 그 채널까지 완료로 세지 않는다. T17/M1.7/M2.0의 저장 핸드셰이크·외부 ACK는 SYS-RUNHOURS 공통 상세를 재사용한다. 0/1 변화만으로 외부 장기누적 저장 성공/실패를 판정하지 않는다.

### Q61.4 미확정의 검색 경계

IdentXmlPart 181개를 채널 이름으로 검색해 5개 선언 항목을 확보했다. start client motor 8의 이름 선언은 이 XML 집합에서 찾지 못했고 Output AO492(Q61.4 bit offset), 범위 후보 AO480/488도 선택 검색에서 나오지 않았다. live_index doc482의 Q61.4 심볼 존재는 확실하지만 실제 쓰기 부재가 완전히 증명된 것은 아니다. 간접주소·절대주소·블록 복사·외부 통신 writer 및 현재 프로젝트 교차참조는 별도 필요하다. 이 미확정을 기동기능 없음 또는 정상동작으로 단정하지 않는다.

## 4. 전기 전달 경로

원본 `all-in-one/sources/Electrical_Rev2.pdf` 실제 PDF90/94/130/132를 각각 렌더하여 확인했다. **FG89/93/129/131이며 네 페이지 모두 Rev2 17.03.2025, DATA 27.05.2024**를 개정란에서 읽었다. PDF/FG를 별개로 보존한다.

|구간|실제 도면에서 확인한 끝점|불확실성|
|---|---|---|
|RUN 외부 접점|FG89/PDF90: +24Vdc10.7→X1:298(5x20 2A F 표시)→선89.3→그려진 열린 접점→X1:299→E13.2 /129/3|외부 기기번호·상대 제어반 단자·케이블 식별 미확보|
|RUN PLC 입력|FG129/PDF130: E13.2, 참조89/4→모듈 단자13, CPU515/MOD11 표기, SHREDDER VIBRATION FEEDER RUN|현재 CPU 종류·실물 채널·정상극성 증명이 아님|
|FAULT 외부 접점|FG93/PDF94: +24Vdc10.7→X1:336(5x20 2A F)→선93.2→그려진 열린 접점→X1:337→E15.5 /131/5|고장일 때 접점 실제 동작·외부 보호 논리 미확정|
|FAULT PLC 입력|FG131/PDF132: E15.5, 참조93/3→모듈 단자36, CPU515/MOD11 표기|외부 고장 코드와 직접 동치로 만들지 않음|
|모듈 보조전원|FG129: +24Vdc10.7→X21:3012의5x20 2A IST.→선129.1→단자19; -0Vdc10.6→20. FG131: X21:3013→선131.1→39, -0Vdc10.6→40|도면 정격과 현행 퓨즈·보호값은 별도|
|기동 출력|Q61.4는 백업 심볼만 확인. 실제 A61.4/Q61.4 출력 회로 끝점 미식별|릴레이·코일·부하접점·단자·컨택터·모터전력·보호기 미확보|

네 페이지의 해당 입력 범위에는 SPARE 점선이 있다. 열린 접점 도해로 정상극성·단선 시 안전동작·실제 사용을 추정하지 않는다. 이 경로에는 별도 릴레이 부하접점5/9가 확인되지 않았으므로 다른 설비의 하단 접점표1/5/9를 복제하지 않는다.

전체 OEM265쪽과 시공 `Electrical_Can_Decoating_20241118.pdf`64쪽의 텍스트에서 Q/A61.4·SHREDDER VIBRATION·CL08 경계를 검색했다. OEM은 위 네 쪽이 hit이고 시공도 hit는 없었다. 이는 전체 도면 의미검토나 모든 그림문자 검색 성공을 뜻하지 않는다. 시공도 실제 렌더는 수행하지 않았으며 외부 제어반 도면 미확보를 유지한다.

## 5. 알람·복구

0227 Motor/Alarm Client FC9, document417, NID8의 전체 고유 가지를 대조했다.

- 공통 허가: W201 rail→Contact193.in; ON ORef178/RID1→W184→operand. Contact193.out W194가 Set와 Reset 가지로 갈린다.
- Set: FAULT ORef179/RID20→W185→Contact195.operand; out W196→SCoil172.in; operand W187/ORef180/RID21=DB3.X15.0. 즉 **ON AND I15.5 → Set 경보**.
- Reset: FAULT ORef181/RID20→W188→Contact197.operand(명시 Negated); out W198→Contact199.in; RESET_ALLARM ORef182/RID7→W189→operand; out W200→RCoil177.in; operand W191/ORef183/RID21=같은 경보. 즉 **ON AND NOT I15.5 AND DB2.X6.0 → Reset 경보**.

이 네트워크에는 타이머 Part가 없다. RUN=0을 직접 고장 원인으로 치환하지 않으며 다른 모터의 무응답 지연을 붙이지 않는다. 원시 FAULT가 사라져도 Reset 조건까지 충족되어야 래치가 해제된다. 원인이 계속 참이면 이 Reset 가지는 성립하지 않는다.

Allarmi_121의 DB3.X15.0 설정만 직접 결속했다. 표시문구·경보이력·소리·ACK 이벤트는 미확보다. 공통 경보집계/Reset 생성은 SYS-ALARM에서 다루며 CL08 단일 경보의 외부모터 직접 정지 writer는 확인하지 못했다. 외부 원인 소멸, PLC 래치 해제, HMI ACK, 외부 제어반 Reset, 재기동, 현장복구를 구분한다. 복구 실행·시험은 하지 않았다.

## 6. 증상별 읽기 전용 관찰 기준

아래는 승인된 담당자가 제공할 자료의 비교 기준이며 활선작업·강제출력·바이패스·보호값 변경·Reset 실행 지시가 아니다.

|증상|동일 시각에 필요한 관찰|판별 경계|
|---|---|---|
|시작 표시지만 공급기 정지|HMI 버튼 이벤트, 현재 프로젝트 식별, Q61.4 값과 writer 교차참조, 외부반 상태, I13.2|Q61.4 이름만으로 모터전력까지 연결하지 않음. 외부회로·명판 필요|
|실제 동작인데 RUN 미표시|I13.2, IW12, DB13.W12/X13.2, HMI ID003FE, 자료시각|X1:298/299→모듈13과0397 Word 전달·통신을 나눠 비교. 단선/통신 이상을 추측 확정하지 않음|
|FAULT 소멸 후 경보 유지|I15.5, M0.0, DB2.X6.0, DB3.X15.0, Allarmi_121|0227의 S/R 래치·NOT 조건과 HMI ACK 구분|
|Reset 요청 후 계속 경보|원시 FAULT, 내부 Reset 전후, HMI 요청·소비 기록, 외부반 진단|내부 Reset 도달 여부 및 원인 잔존 비교. 반복 재기동을 해결책으로 제시하지 않음|
|시간값이1에 머묾/누적 안 됨|I13.2,T13,DB9.W28/W30,M1.7,T17,외부 저장내역|HOUR Move1/Move0와 외부 누적 분리. 저장 손실·정비주기 도달 추정 금지|
|도면과 설명 주소 불일치|CPU 프로젝트, 도면 개정, X1/모듈 표찰, 상대반 케이블표|과거 e13.7/e18.5와 I13.2/I15.5 별도 보존. 임의 배선 변경 금지|

관찰자·실제시각/시간대·위치·값/단위·수집장치·프로젝트·도면판본·원본비교·배제 결과·미확정 및 복구증거를 남긴다. 실제 운영/SEJIN 기록·현장 사진을 이번 문서에 복제하지 않았다.

## 7. 완료 기준·누락

|영역|적용 상태|남은 조건|
|---|---|---|
|설비·자료|적용, 고정백업 문서 작성|현재 설비/명판 동일성 미확정|
|I/O·HMI|입력/경보/시간 선언 및 CSV 주소 확인|출력 writer, HMI 이벤트·현재 통신 필요|
|제어|0227/0299와0333 CL08 가지, 공통 호출·분 타이머 확인|기동/정지·수자동·외부 시퀀스 미확보|
|전기|입력2개 끝점과 전원 실제4페이지 확인|출력·케이블·상대반·현물 확인 필요|
|알람·복구|고유 S/R 정적 대조|외부 Reset·ACK·현장 복구 미확인|
|증상 관찰|읽기 전용 비교표 작성|관찰값 미취득|
|완료/누락|문서와 구현/게시/현장을 분리|BC01 동등 기능완료·게시완료 아님|

다음 필요한 자료는 현재 GME 프로젝트의 Q61.4 교차참조(간접쓰기 포함), 외부 Shredder vibration feeder 제어반 회로/프로그램/기동허가표, X1:298/299/336/337 상대 단자 및 케이블표, 현행 HMI 이벤트/스크립트, 현행 명판·도면·RUN/FAULT 정상상태 증거다. 새 자료 없이 동일 실물 보류를 반복 조사하지 않는다.

네 기능 중 도면·래더 비교용 근거만 준비했다. 선택 백업·복원, 기록 전후비교, 관찰보고서/PDF의 CL08 전용 구현·저장·재읽기·화면 재열기 검증은 하지 않았다. note/repair_observation/미지필드/초안/저장키는 변경하지 않았다.

상태: documentation `complete_with_gaps`; static_review `selected_original_xml_and_pdf_reviewed`; ui_records `not_run`; publication `not_published`; tia_compile/live_cpu/field_recovery `not_performed`. 부모 독립 검토·첨부 대기이며 로컬통합은 별도 작업이다. 현장 극성·현행보호값·현재 CPU·실제 복구를 채우지 않았다.

### 검증 범위와 산출물

선정 원본34개는 SHA256 및 고정 Git blob 전체 byte 일치를 확인했다. 이는34개 모든 내용의 의미검토 완료가 아니다. 직접 의미검토는 0227/0299의 CL08 고유 전체 핀, 0333의 CL08 초기화 가지, 0397의 IW12 전달, 0549 FC9/FC2 호출, 0019 T13 및 선택 선언이다. 181개 XML 명명검색·PDF 전체 텍스트검색과 실제 도면4쪽 렌더 의미검토를 구분한다. 별도 검증은 문서용 XML 핀 단언6개이며 PLC 행동시험이 아니다.

검사·해시·검색·원형 발췌는 `../extracts/CLIENT-CL08/verification.json`, `source-hashes.json`, `declaration-search.json`, `output-search.json`, `pdf-search.json` 및 readable XML/PNG다. 자신의 extracts와 본 초안만 작성했다. 원본/중지 자산은 건드리지 않았으며 원본 Git 상태가 비어 있음을 확인했다. 전 원본/중지5자산의 별도 전수 해시검사를 이번 선정34개 검사로 대신했다고 주장하지 않는다.

### 선정 원본 SHA256 + 고정 Git blob 전체 표

경로는 `source-mv06/` 기준. 내용 일치는 파일 byte와 `git show abcf31c5030bc7ef8749ed8e869a857f2387a28a:경로`의 비교다.

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
|`all-in-one/sources/decoded-original/0227-FlgNet.xml`|`17b3b042d39c98ee18eff641e82a5a46008c716c2429075df2c253e868e0d249`|`6213b8a2bb667fee6451069cdd878954f92b87d6`|일치|
|`all-in-one/sources/decoded-original/0299-FlgNet.xml`|`290c11c2038a3ef43b5480127768643161d18fc3ae973f49308883fb02ef166d`|`7c1c5146dde6694df2386b85272cd0737519d813`|일치|
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
