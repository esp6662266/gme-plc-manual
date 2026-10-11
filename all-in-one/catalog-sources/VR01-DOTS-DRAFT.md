# VR01 로터리 밸브: 원본 근거 조사 초안

작성일: 2026-10-11 (UTC) · 문서 상태: 조사 초안, 현장 미확인 · 표준: GME-STD-1.0.0

## 0. 작업 범위와 핵심 결론

- 대상은 **VR01 한 ID**다. 우선23의 특정 P키를 새로 배정하지 않는다. 원본 INVENTORY.json은 phase2/planned, motor, depth 0, parent_id=null이다. 이번 자체 클라우드 조사132의 하나이며 원본 phase2 133과 로컬 통합·게시 제외는 유지한다.
- 기준 저장소는 [고정 커밋 abcf31c](https://github.com/esp6662266/gme-plc-manual/tree/abcf31c5030bc7ef8749ed8e869a857f2387a28a), VERSION.json v1.12.0이다. 원본 all-in-one/을 읽고 이 초안과 조사용 추출물만 저장했다. 다른 VR 설비의 수치·알람·단자·정비 기준을 복제하지 않았다.
- **출력 Start VR01=%Q2.6, 원시 입력 VR01_Fbk=%I3.4, 처리 입력 Inputs.VR-01 RUN=DB13.DBX3.4는 서로 다른 관찰점**이다. FG46/PDF47의 피드백은 46KM1 보조접점13–14에서 온다. 모터축 회전·로터 막힘 없음·실제 분진 배출을 직접 검출하는 신호로 취급할 수 없다.
- 전용 FAULT는 **ON ∧ Start VR01 ∧ ¬Inputs.VR-01 RUN → Tag_62(%T63), SdCoil S5T#2S** 경로다. FAULT Set/Reset, 요청 Reset, 출력 Coil을 분리했다. 알람 해제는 재기동 또는 기계 복구 완료와 다르다.
- 자동 요청은 예열 Tipo_preset=1/Tempo_presetting=28에서 Set, 생산2/46에서 Set, 정지5/(11 또는 Emergency_module_fault)에서 Reset이다. 숫자는 우선 원문 Int 비교값이다. 주기·경합·현재 CPU를 확인하지 않고 실제 경과시간을 보증하지 않는다.
- P&ID 실제 렌더에는 **CY-01 하부에 VR-01/M21**이 보인다. 역사 도면의 기계적 배치 관계이며, 현재 CY 실물 동일성·PLC 소유·P14 대응 또는 catalog 부모 변경의 근거로 확대하지 않는다. CY-02와 이름만으로 묶지 않는다.
- HMI 설정3행은 확보했지만 1193/0370의 외부 피연산자8개는 원본 선언 결속이 미완료다. DB11 상태주소와 DB3 FAULT를 같은 비트로 취급하지 않는다.
- **시뮬레이터 작성·수정·생성·실행·행동시험0, 실제 PLC/현장/보호값·SEJIN·공통코드·버전·대장·배포 변경0.** 기존 simulation 원본은 다른 쓰기 위치를 식별하기 위해 읽기만 했다.

### 작성·검증 경계

수정 산출물: drafts/VR01-DOTS-DRAFT.md 및 extracts/VR01/ 아래 정적 추출·PDF 렌더·해시 대조. 공용 declarations.json은 수정하지 않았다. 실행 모델/추론 설정은 이번 초안에서 독립적으로 확인하지 못했으므로 미확인이다. AGENTS.md, 작업 스킬, WORK-STANDARD, WORK-ITEM-TEMPLATE, 실제 INVENTORY.json과 GME-CATALOG-OVERLAP-REVIEW를 읽었다. INVENTORY.md는 고정 원본에 없으며 JSON을 기준으로 삼았다.

## 1. 7영역 적용표

| 영역 | 판정 | 확보한 내용 | 남은 경계 |
|---|---|---|---|
| 설비·자료 기준 | 적용 | VR01/M21, 전용 FG46, 고정 백업, P&ID 배치 | 현재 실물·CY 동일성·명판·개조 이력 |
| I/O·HMI | 적용, HMI 일부 미확보 | Q2.6/I3.4, DB2/3/13, HMI 설정3행, Word 전달 | HMI 외부8피연산자·실제 이벤트·온라인 전달 |
| 제어 구조 | 적용 | 요청4쓰기, 출력, FAULT, Main/주기 블록 호출, 운전시간 | 실제 실행 순서·외부/간접 쓰기·ENO 동작 |
| 전기 전달 경로 | 적용 | 전력·명령·피드백·모듈 양 끝점, 시공 케이블 | 현행 접점/케이블/모터·실제 공급·설정 |
| 알람·복구 | 적용 | 2초 FAULT, Reset, 요청 제거, FN01 상위영향 | 최초 원인·실제 복구·재요청 증거 |
| 증상별 수리 | 적용, 관찰 절차 초안 | 단계별 관찰점·배제할 원인·수집 양식 | 현장 작업·수리 실적·안전 작업 승인은 별도 |
| 완료 기준 | 적용 | 문서/정적/현장/게시 분리, 누락 목록 | UI·기록 도구·게시·TIA·CPU·실물 미수행 |

전용 인버터/PID/엔코더/밸브 OPEN-CLOSE 위치제어는 확인한 VR01 직접기동 회로와 전용 XML에 근거가 없다. 이번 직접기동 제어 설명에는 비해당이며, 현재 설치에 추가 장치가 절대로 없다는 주장은 아니다. 토크·주기·제조사 현행 모델·안전 한계는 자료 미확보다.

## 2. 설비·자료 기준과 소유 경계

| 근거 | 정확한 위치 | 확인 사실·해석 | 미확정 |
|---|---|---|---|
| registers/equipment.json | id=VR01 | 로터리 밸브, motor, 집진·석회, parent 빈값, fgs=[46] | 일반 역할 설명만으로 특정 CY 소유를 확정하지 않음 |
| docs/equipment-standard/INVENTORY.json | catalog_id=VR01 | phase2, depth0, priority_key=null, parent_id=null | 원본 대장 수정 없음 |
| sources/Electrical_Rev2.pdf | FG46/PDF47, 제목 ROTARY VALVE VR-01 | M21, 0.55kW/1.25A 표기, 3상440V60Hz, 46QM1/46KM1/46QS1 | 도면 표기이며 현재 명판·설정값 아님 |
| sources/PID_1684n002I.pdf | PDF1, CY-01 하부 VR-01/M21 | 0.55kW440V의 로터리밸브가 CY-01 하부 배출부에 그려짐 | 현재 실물 확인, 제어권·catalog 부모·P14 배정은 별도 |
| 같은 P&ID | 제목란 1684n002, Apex I | 원도06/04/2011, 최신표시 I=15/01/2013 | 2024~2025 전기·2025 PLC와 자료시점 다름 |
| Electrical_Can_Decoating_20241118.pdf | PDF3/31/51 | FLOW_B VR-01 M21, 케이블1_16 | 계획/시공 참고 자료, 현장 준공검증 아님 |

고정 백업명 GME_20250506.zap18과 내부 프로젝트명/자료시점 차이는 기존 미확정으로 유지한다. 현재 CPU와 백업의 동일성을 정적 파일 해시로 대신하지 않는다. 공개 원본 안에 있는 시공 PDF를 참고했을 뿐 SEJIN 운영자료·사진·이력을 새로 복제하거나 통합하지 않았다.

## 3. I/O·HMI와 데이터 전달

아래 XML 이름은 모두 sources/decoded-original/ 아래이며, RID는 파일별 지역 식별자다. 다른 Ident 파일의 같은 RID만으로 연결하지 않고 UID/NID 및 대상 선언을 함께 대조했다. AO/BO는 비트 오프셋으로 해석하고 DB 번호는 DepDBBlock/TOD로 확인했다.

| 신호 | 형식/주소·방향 | 원본 선언·사용 핀 | 해석·주의 |
|---|---|---|---|
| Start VR01 | Bool, Output AO22 → %Q2.6 | 0602 RID104, NID20 UID613 AK=Write; 0251 Coil608.operand←ORef613/R104, W620 | PLC 명령. 실제 접촉기·회전 보증 아님 |
| VR01_Fbk | Bool, Input AO28 → %I3.4 | 0613 RID176 NID29 UID1612; 0315 Contact1642.operand W1624 | 시간계수는 원시입력을 읽음 |
| Inputs.VR-01 RUN | Bool, DB13.DBX3.4 | 0657 RID284/AO28, BAD247→0655 Inputs TOD13; 0432 ORef697/R284→Contact696.operand W699 | FAULT 감시는 처리 DB를 읽음 |
| Flag.M_VR_01 | Bool, DB2.DBX1.1 | 0604 RID103/AO9, BAD2→0603 Flag TOD2; 0577 RID53/AO9 | HMI·자동·고장처리가 관여하는 운전 요청 |
| Allarm.VR_01_FAULT | Bool, DB3.DBX1.1 | 0657 RID80/AO9, BAD10→0655 Allarm TOD3 | PLC FAULT 래치, HMI DB11과 별도 |
| Flag.RESET_ALLARM | Bool, DB2.DBX6.0 | 0657 RID13/AO48; 0432 ORef666→Contact691.operand W678 | 공통 Reset 요청; 원인 제거·재요청 아님 |
| Tag_62 | Timer, %T63 | 0658 RID78, SAD Timer, AO63; UID662 쓰기/663 읽기 NID19 | HMI 태그가 아닌 PLC S5 타이머 |
| VR_01_MIN / VR_01_HOUR | Int, DB9.DBW112 / DBW114 | 0615 RID178/AO896, RID180/AO912; 0614 hours motors TOD9 | 운전시간 처리용 내부값; 영구 누적시간으로 단정 금지 |
| Data.Tempo_presetting / Tipo_preset | Int, DB1.DBW96 / DBW98 | 0577 RID7/AO768, RID12/AO784; 0576 Data TOD1 | 자동순서 비교값 |
| Flag.Auto_ON1 | Bool, DB2.DBX7.3 | 0577 RID4/AO59; 0576 Flag TOD2 | 자동순서 활성 요청 |

### 3.1 I3.4 → 처리 DB13.X3.4의 Word 경로

1070/0397-FlgNet.xml NID1에서 Move27.in←ORef28/RID8(W31), Move27.out1→ORef29/RID9(W32)이다. 0627 RID8 Tag_179는 Word/Input/AO16이므로 **IW2**이고, 0629 RID9는 Word/AO16/BAD4, 0628 RID4 Inputs/TOD13이므로 **DB13.DBW2**다. 따라서 같은 Word의 후반 바이트 I3.4는 DB13.X3.4에 대응한다는 정적 주소 경로가 성립한다.

그러나 Move27.en은 Powerrail 직접 연결이 아니라 **Move22.eno→W34→Move27.en**이다. Move22와27에는 DisableENO=true도 함께 있다. 실제 TIA ENO 처리·호출·값 갱신은 추가 확인이 필요하다. 단순히 I3.4와 DB13.X3.4가 매 스캔 항상 같다고 선언하지 않는다.

Main1613/0030의 호출은 Recipes Handler(CRef21)→ENO W32→HMI(CRef23)→ENO W33→HMI Output(CRef25)→ENO W42→Contact37(negated operand Simulation(1), ORef45/R140 W44)→W43→HMI Inputs(CRef28). 0688 RID135 CodeBlock29/AK=Call이 HMI Inputs이며 0692 RID140이 Simulation(1)이다. 이 호출 ENO·모드가 DB13 갱신의 경계다. 원시입력과 처리입력이 어긋나면 이 경로부터 분리 관찰한다.

### 3.2 HMI 설정과 미결속

sources/hmi_plc_tags.csv 원본 추출 설정의 118/164/440행:

| HMI 설정 태그 | 주소 | Access/내부 ID | 판정 |
|---|---|---|---|
| VR_01\\Allarme1 | DB11,X32.1 | PLC / 0034C | 표시용 설정 주소. DB3.X1.1과 동일 비트 아님 |
| VR_01\\RispostaA | DB11,X32.0 | PLC / 00306 | 상태용 설정 주소. I3.4/DB13.X3.4와 구분 |
| VR_01\\Flag | DB2,X1.1 | PLC / 0019E | 요청 비트 주소는 Flag.M_VR_01 선언과 부합. 클릭/토글/쓰기 이벤트는 미확보 |

1193/0370-FlgNet.xml은 CRef22/R638, CodeBlock23/R1, en W21의 호출이며 핀은 다음과 같다.

| Wire | 외부 참조 | CRef22 핀 | 결속 상태 |
|---|---|---|---|
| W37 | ORef24/R676 | Ingresso_run 입력 | 대상 선언 미결속 |
| W39 | ORef26/R230 | Allarme1 입력 | 대상 선언 미결속 |
| W40/41/42/43 | ORef27/28/29/30, 모두 R48 | Allarme2/3/4/5 입력 | 유사 선언 FALSE 후보는 있으나 동일 네트워크 NID 결속 미확정 |
| W46 | ORef33/R236 | Risposta 출력 | 대상 선언 미결속 |
| W48 | ORef35/R240 | Comulativo_allarmi 출력 | 대상 선언 미결속 |

0623의 RID1은 HMI Standard Motors, 0624 RID638은 그 Bool 인터페이스를 보여준다. 하지만 0370은 network-map의 inferred_original_nid=null, resolved_operand_count=0/8이다. 일반 함수 이름·핀 모양 또는 다른 VR 호출을 근거로 이8개를 VR01 입출력에 자동 결속하지 않는다. HMI 원본 화면/스크립트/태그 사용 이벤트·TIA 호출 파라미터 확인이 필요하다.

백업 심볼 설명에는 Start VR01의 옛 주소 `a 53.2`가 남아 있다(registers/plc-symbols.csv, 문서1330). 실제 선언 Q2.6과 FG46/138의 A2.6을 우선 대조하되, 설명 충돌을 삭제하거나 A53.2를 현행으로 쓰지 않는다.

## 4. 제어 구조, 다른 쓰기와 호출

### 4.1 전용 모터 로직: 1949/0251, motors 1 NID20

- Powerrail W628→Contact622(ON, ORef609/R1 W614). Contact622.out/W623에서 두 갈래로 분기한다.
- **고장 요청 제거:** Contact624(Allarm.VR_01_FAULT, ORef610/R102 W615)→W625→RCoil604.in, operand W617→ORef611/R103 Flag.M_VR_01. 식은 **ON ∧ FAULT → Reset 요청**이다.
- **출력:** Contact626(Flag.M_VR_01, ORef612/R103 W618)→W627→Coil608.in, operand W620→ORef613/R104 Start VR01. 식은 **ON ∧ 요청 → 출력 Coil**이다.
- 이 전용 출력 rung 안에 피드백, FAULT NC, Maintenance, 방향 인터록, 속도/PID가 추가로 직렬 연결돼 있지는 않다. FAULT는 앞의 요청 Reset을 통해 영향을 준다. 현재 실행 순서·다른 쓰기·외부 HMI와의 경합을 확인하지 않고 최종 Q값이나 정지시간을 보장하지 않는다.

### 4.2 자동 요청: 서로 다른 Set 두 곳과 Reset 한 곳

| 구간 | 정확한 원본 핀·선언 | 원문에서 읽은 조건 | 제한 |
|---|---|---|---|
| 예열 Set | 1843/0164 NID3, Contact785 ON→W786→Contact22 neg Emergency→W32→Eq400.pre; Eq400.in1 O590/R12(W670), in2 O591/R8=1(W671); Eq400.out W33→Contact823 Auto_ON1 O824/R4 W826; W672→Eq509.pre; Eq509.in1 O635/R7(W736), in2 O636/R52=28(W737); out W738→SCoil513.in; operand W739→O637/R53 | ON ∧ ¬Emergency_module_fault ∧ Tipo_preset=1 ∧ Auto_ON1 ∧ Tempo_presetting=28 → Set Flag.M_VR_01 | 동일 출력 분기 VR02/CH01을 VR01에 소유 이전하지 않음 |
| 생산 Set | 1844/0165 NID4, Contact1145 ON→W1146→Contact1154 neg Emergency(O1155/R108 W1157)→W21→Contact1147 Auto_ON1(O933/R4 W1018)→W1148→Eq737.pre; O934/R12, O935/R78=2(W1019/1020); W1021→Eq846.pre; O983/R7, O984/R85=46(W1095/1096); out W1097→SCoil850.in, operand W1098→O985/R53 | ON ∧ ¬Emergency_module_fault ∧ Auto_ON1 ∧ Tipo_preset=2 ∧ Tempo_presetting=46 → Set 요청 | 예열28과 혼용 금지 |
| 정지 Reset | 1847/0166 NID5, Contact1095 Auto_ON1(O983/R4 W1028)→W26→Eq881.pre; O984/R12, O985/R22=5(W1029/1030); W1031→Eq913.pre 및 Contact1126.in; Eq913.in1 O997/R7(W1047), in2 O998/R99=11(W1048); out W49→OR48.in1; Contact1126 Emergency O1127/R108 W1129→W50→OR48.in2; out W1049→RCoil917.in; operand W1050→O999/R53 | Auto_ON1 ∧ Tipo_preset=5 ∧ (Tempo_presetting=11 ∨ Emergency_module_fault) → Reset 요청 | Emergency만으로 독립된 무조건 Reset이라고 축약 금지 |

선언: ON은0575, Flag/Data/Allarm은0577, 상수는0578. 0577 RID53의 Write는 정확히 NID3/UID637, NID4/UID985, NID5/UID999다. 0604 RID103 NID20/UID611 고장Reset을 더하면 확인한 **명명된 PLC 요청 쓰기4곳**이다. HMI DB2.X1.1 설정도 별도 외부쓰기 가능성을 남긴다. 현재 프로젝트의 간접/DB영역 일괄쓰기까지 모두 배제했다는 의미는 아니다.

1841/0162 NID1: Contact88 ON→Contact90 Auto_ON1→W91→Add59.en; W80/81의 Data.Tempo_presetting와1을 더해 W82/O73에 쓴다. 별도 neg Contact92 Auto_ON1→Move66가0을 같은 변수에 쓴다(W85/86). 1723/0024의 주기블록 제목은 `cyc_int2 ogni 1s`이며 ON Contact188→W189→CRef183.en/CodeBlock186이 Auto start motors를 호출한다(0067 RID39 TOD FC30, NID4/UID186 AK=Call). 이는 1초 의도의 근거이나 현재 OB 설정·실제 인터럽트 주기·경합은 확인 전이다.

### 4.3 Main 호출과 실행 범위

- 1619/0031: ON ORef271/R52(W280)→Contact282→W283으로 CRef264.en에 전달, CodeBlock275/R58=Allarms 1(0688 NID6 UID275 AK=Call). 같은 ON 분기에 Analog input conversion/Allarms2/3도 있다.
- 1620/0549: ON ORef335/R52(W348)→Contact350→W351으로 Motors 1(CRef319, CodeBlock337/R67) 및 time work motor(CRef334, CodeBlock347/R82) 등에 전달한다(0688 NID7).
- XML 분기 연결과 백업 색인 순서는 확인했으나 현재 OB 실제 주기·블록 실행 순서·전원 복귀·리테인·HMI 경쟁쓰기를 실행 검증한 것은 아니다. ON 이름만으로 실제 항상1을 가정하지 않는다.

### 4.4 다른 쓰기: 처리입력과 운전시간

1. DB13.X3.4는 위1070의 IW2→DB13.DBW2 Word 쓰기에 포함된다.
2. 영구중지 대상의 **기존**1084/0404 NID3에는 Contact30(Flag.M_VR_01 O31/R110, W29)→W32→Coil34, operand W33→O35/R94 Inputs.VR-01 RUN 쓰기가 있다. 선언0635의 AK=Write이다. 실제 활성 여부를 증명하지 않으며, 이번에는 정적 읽기만 했다. DB13 RUN을 원시/실제 응답과 무조건 동일시하지 않아야 할 이유다. 이 자산의 실행·수정·생성·시험은 하지 않는다.
3. 시간계수1027/0315 NID29: Tag_47 Contact1640(O1611/R1 W1623)→W1641→VR01_Fbk Contact1642(O1612/R176 W1624). W1643은 Add1594.en과 Ge1601.pre에 병렬로 들어간다. Add.in1=MIN(O1613/R178 W1625), in2=Int1(O1614/R7 W1626), out=MIN(O1615/R178 W1627). Ge.in1=MIN(O1616 W1628), in2=60(O1617/R8 W1629).
4. Ge1601.out→W1630→Move1604.en, **입력1(O1618/R7 W1632)을 HOUR(O1619/R180 W1633)에 Move**한다. HOUR=HOUR+1 Add가 아니다. Move1604.eno→W1634→Move1607.en; 입력0(O1620/R12 W1635)→MIN(O1621 W1636). Move1607.eno→W1637→SCoil1610 Flag_Aggiorna_DB(O1622/R13 W1638). Add의 out/ENO와 Ge를 직렬 연결한 것으로 바꾸지 않는다.
5. 1050/0337 NID52에서 HOUR는 다시0을 쓴다: 앞선 Move2884→ENO W2913→Move2887→ENO W2916→Move2890→ENO W2919→Move2893.en; O2906/R12=0→W2920→in, out1 W2921→O2907/R180. 처음 허가는 Tag_48 Contact2925(O2899/R284 W2910)→W2926→Move2884.en이다. VR01만의 독립 초기화 조건으로 축약할 수 없다.
6. 1056/0019 NID58의 neg Tag_47 Contact3120→W3121→SdCoil3112.in, value W3117/O3114/R335=S5T#1M, operand W3119/O3116/R1=Tag_47(%T13). 1055/0341 NID57은 ON·Flag_Aggiorna_DB로 MEM2_0 Set, ON·MEM2_0·¬Flag_Aggiorna_DB로 Tag_48(%T17) S5T#5S(SdCoil3118; value W3138/O3128/R334), Tag_48 접점으로 MEM2_0 Reset의 공유 처리다. 기록 완료 핸드셰이크·외부 저장과 ENO를 확인하기 전 장기 누적 운전시간으로 사용하지 않는다.

## 5. 전기 전달 경로: 실제 PDF 렌더 확인

원본 Electrical_Rev2.pdf는265쪽이다. **FG46=PDF47, FG119=PDF120, FG138=PDF139**이며 FG와 PDF쪽을 섞지 않았다. FG46·119의 제목란 날짜는27.05.2024, 추가 개정 표시는 확인되지 않았다. FG138은 날짜27.05.2024와 **Rev2/17.03.2025**가 함께 보인다. PDF 전체 파일명 Rev2를 모든 페이지의 개별 개정으로 바꾸지 않는다.

| 경로 | 실제 렌더에서 확인한 양 끝점과 경유 | 판정·미확정 |
|---|---|---|
| 3상 동력 | FG46 상단8.3L1/L2/L3(44/9에서 와49/0으로 계속)→46QM1 주접점1-2/3-4/5-6→46KM1 주접점1-2/3-4/5-6→46U1/V1/W1→XM:46U1/46V1/46W1→46QS1 1-2/3-4/5-6→M21 U/V/W, PE | 440V60Hz, M21 0.55kW/1.25A, 내부선 BLACK FS17 1.5mm² 표기. 46QM1의1.1–1.6A는 도면 표시 범위이며 현장 보호 설정값 아님 |
| 기동 명령 | FG138/PDF139 CPU515/MOD14의 단자27 A2.6→46/4→FG46 A2.6/138/1→XS31→46QS1 보조접점(46/1)→XS32→46.1→46QM1 보조접점(46/1)→46KM1 A1→코일→A2→-0Vdc10.6 | PLC Q2.6과 도면 A2.6 일치. QS/QM 보조접점의 단자 번호는 이 회로에서 읽히지 않아 추정 금지. 중간 별도 KA/인버터가 있는 것으로 복제하지 않음 |
| 접촉기 응답 | +24Vdc10.7→46KM1 보조접점13–14(46/4)→E3.4/119/5→FG119/PDF120 단자35, CPU515/MOD8 E3.4 | **접촉기 보조접점 응답**. 모터 회전/기계 전달/실제 배출은 별도 현장 관찰 필요 |
| 입력 모듈 보조전원 | FG119 +24Vdc10.7→X21/3007 5×20 2A IST.→119.1→단자39; -0Vdc10.6→단자40 | 도면의 전원 경로. 2A를 모터 보호값으로 사용하지 않음 |
| 출력 모듈 보조전원 | FG138 +24Vdc10.9→X21/3030 5×20 4A F→138.1→단자29; -0Vdc10.6→단자30 | 출력모듈 전원과 모터 주전원·접촉기 반환을 구분 |
| 시공 케이블 | 시공PDF51, CANDC-CONS-C001-051, 행1_16: `=FLB+VR01-M21A`, FROM LOC CR, TO LOC VR-01/TAG M21, ROTARY VALVE, GAC/CV, CORE4/SIZE1.5/SPARE0, ROUTE 첫칸100 LDD1·다음E100, Adjustment5, LEN52 | FROM 상세 TAG/DESCRIPTION 공란. LEN 단위를 해당 행에 새로 만들어 쓰지 않음. 실제 시공길이·도체색·단자 매칭 미확인 |
| 시공 말단 | 시공PDF31, CANDC-CONS-E014-031, FLOW_B ZONE01 상단 첫 행:100 LDD1, Flexible16, M21, VR-01/M21, `1_16=FLB+VR01-M21A`, CV/SIZE1.5/CORE4 | PDF51의 케이블 식별자와 대조. CY-02의17HL1/6SB3가 같은 페이지에 있다는 이유로 VR01 제어 소유에 합치지 않음 |

시공PDF3/31/51의 개정란은 `24.11.11 first draft design`, CHECKED/APPROVED는 비어 있다. 최종 승인 시공도/준공 상태로 격상하지 않는다. P&ID는 Rev I/15.01.2013, 전기도면·시공자료와 시점이 다르다. 현행 제조사/ABB 모델, 차단기 실제 설정, 코일 정격, 현장 배선·정상 극성은 명판/승인자료/현장 측정 확인 전이다.

## 6. 알람·복구와 FN01 상위 영향

### 6.1 VR01 전용 FAULT: 1797/0432, allarms 1 NID19

| 단계 | 정확한 핀·선언 | 식·해석 | 미확정 |
|---|---|---|---|
| 지연 시작 | ON O659/R1 W669→Contact683; W684→Start VR01 Contact685(O660/R77 W670); W686→neg Contact696(Inputs.VR-01 RUN O697/R284 W699); out W21→SdCoil647.in; value W671→O661/R28=S5T#2S; operand W672→O662/R78 Tag_62 | ON∧Q명령∧¬처리RUN으로 T63 지연 | 현재 타이머값·호출주기·정상 극성은 미확인 |
| 래치 Set | Contact685.out W686→Contact687(Tag_62 O663/R78 W673)→W22→SCoil653.in, operand W676→O665/R80 | ON∧Start VR01∧T63 접점 → DB3.X1.1 Set | 타이머 시간만으로 기계 원인 확정 금지 |
| 래치 Reset | Contact683.out W684→Contact691 RESET_ALLARM(O666/R13 W678)→W692→Contact693 FAULT(O667/R80 W679)→W694→RCoil658.in, operand W681→O668/R80 | ON∧Reset∧FAULT → 동일 FAULT Reset | 조건이 계속되면 이후 재발 가능; Reset은 원인 제거가 아님 |
| 출력 영향 | 1949의 RCoil604 및 Coil608 | FAULT가 요청을 Reset; 출력은 ON∧요청 | 같은 주기 Set/Reset 경합·외부 요청은 추가 확인 |

0656 RID28의 LiteralConstant는 S5Time `S5T#2S`; 0658 RID78은 %T63 Timer다. 조사한 원본 선언에서 T63 별칭/다른 명명된 쓰기는 추가 발견하지 않았다. 이는 현재 전체 프로젝트의 간접 쓰기 부재 보증이 아니다. VR01 별도 인버터FAULT, 역회전, 위치감시·막힘 알람을 새로 만들지 않는다.

### 6.2 FN01 Prealarm은 VR01 전용 FAULT와 별도

1950/0252, motors1 NID21의 ON Contact691(O662/R1 W674) 아래에 OR707(Card5)가 있다. 다섯 갈래는 MAX_TC04_TEMP(Contact693→W694/in1), MAX_TC05_TEMP(Contact695→W25/in2), ZT01_FN01_Vibration(Contact697→W698/in3), **Inputs.FN01 Run(Contact699)∧¬Inputs.VR-01 RUN(Contact701→W702/in4)**, FN01 Run∧¬Inputs.VR02 Run(Contact703→W704/in5)다.

VR01 갈래의 원본은 Contact699.operand O666/R250 W678, out W700→Contact701.in, Contact701 neg operand O667/R251 W679이다. OR707.out W683이 Coil653(Allarm.Prealarms_FN01, O669/R111 W684), SdCoil656(Tag_122, O671/R113 W686), Contact705.in으로 동시에 전달된다. 타이머 value W685/O670/R112는 **S5T#1H_30M**; Tag_122는0602 Timer/AO130=%T130이다. Contact705(Tag_122 O672/R113 W687)→W27→Coil661 Stop_Fan_FN01(Local, O673/R114 W689)이다.

이것은 VR01 RUN 상실이 FN01의 공유 예비경보·정지 요청에 영향을 줄 수 있다는 근거다. **VR01의2초 타이머와 FN01의90분 타이머를 합치거나 VR01의 보호시간으로 부여하지 않는다.** Stop_Fan_FN01은 해당 블록 Local이며 현재 최종 FN01 정지·기계상태까지 이 초안으로 보장하지 않는다. CY 본체 전용알람으로도 재분류하지 않는다.

### 6.3 복구 판정

원인 확인→전기/기계 상태 확보→처리입력/원시입력 비교→FAULT/요청/출력 잔류 확인→승인된 재요청→별도 회전·배출 확인을 서로 다른 증거로 남긴다. 이 초안은 실제 Reset·재기동·운전 또는 위험한 전기 측정의 지시/승인이 아니다. 강제출력·보호 우회·타이머/보호값 변경을 권하지 않는다.

## 7. 증상별 관찰·수리 검토 초안

현장 작업은 자격 있는 담당자의 승인된 정지·격리·잔류에너지 해소 절차 아래 수행한다. 아래는 관찰·원인분리 체크리스트이며 실제 수리 완료 기록이 아니다.

| 증상 | 먼저 구분할 관찰점 | 비교 근거·배제 순서 | 조치/복구 증거의 미확정 |
|---|---|---|---|
| 요청 자체가 없음 | HMI VR_01\\Flag 설정, DB2.X1.1, Auto_ON1/Tipo/Tempo, FAULT, 모드 | HMI 실제 이벤트→예열28/생산46 Set→정지11/Emergency·고장Reset4쓰기→현재 호출순서 | HMI 설정주소만으로 버튼 작동 확정 금지 |
| 요청1인데 Q2.6 없음 | ON·현재 실행블록·출력 Coil608·같은 주소 다른쓰기 | 1949 출력 rung, Main1620 호출, 현재 CPU/백업 일치 | 프로그래밍 변경 없이 실제 관찰 필요 |
| Q2.6 있는데 KM 미응답 | 출력단자27·XS31/32·46QS1/46QM1 보조접점·46KM1 A1/A2·반환 | 명령단과 실제 코일/보조접점 전달을 구간별 분리; 접촉기/주전원/격리 상태 구분 | 도면 보호범위를 임의 설정값으로 적용 금지 |
| 2초 FAULT 발생 | I3.4와 DB13.X3.4, T63, 최초 명령/응답/알람 시각 | 실제46KM1 접점→입력단자35→원시I3.4→IW2/DB13W2→호출ENO·모드→0432 | 양 신호 불일치는 배선 고장으로 단정하지 않음 |
| RUN 표시1인데 배출 없음 | KM 보조접점, 실제축/감속기/커플링/로터·상하류 상태 | RUN은접촉기 접점; 기계 전달·막힘·공기차단·분진흐름은 별도 근거 | 회전부 접근/개방·청소는 승인 격리절차 필요 |
| VR01 이후 FN01 경보/정지 | VR01 처리RUN, FN01 RUN, 다른4갈래, Prealarms_FN01/T130 | 1950 OR5갈래와90분; VR01 2초FAULT와 최초발생 구분 | FN01 직접 원인이라고 단정하거나 타이머 변경 금지 |
| Reset해도 재발 또는 재기동 안 됨 | 원인 입력, FAULT 래치, 요청DB2.X1.1, Q2.6 | Reset658은 FAULT만;604가 요청을 이미 지웠을 가능성; 재요청 경로 별도 | 경보창 소거가 복구완료 아님 |
| 시간값 불연속/0/1 반복 | raw I3.4, T13, MIN112/HOUR114, T17, Flag_Aggiorna_DB, 외부저장 | HOUR Move1 및 ENO연쇄0초기화; 영구누적과 순간전달 구분 | 값 정정·카운터 강제변경·정비주기 추정 금지 |

관찰 기록 최소 항목: 관찰자, 시각·시간대, 설비/모터/반·단자 위치, 프로젝트·CPU 근거, 모드, 요청/출력/raw/처리RUN/FAULT/타이머/시간계수의 값·단위, 수집장치, 비교 원본, 배제 결과, 승인 조치, 재확인 시각, 실제 회전·배출 증거. 미지값은 빈칸 또는 미확인으로 남기며 공개 초안에 운영 기록·사진을 붙이지 않는다.

## 8. 네 기능과 완료 기준

| 기능 | 이번 적용 상태 | 후속 필요 |
|---|---|---|
| 도면·래더 비교 | 문서상 FG/PDF·원본핀 연결, 실제 PDF 렌더 완료 | VR01 선택 화면·강조·링크 구현은 별도 승인 범위 |
| 백업·선택 복원 | 구현/시험 안 함 | VR01 기록키, 미지필드·타설비·초안 보존을 통합 담당자가 별도 검증 |
| 기록 전후 비교 | 구현/시험 안 함 | 운영 관찰값·버전 비교 기능 검증 |
| 보고서/PDF | 이 MD 조사초안만 작성 | 보고서 UI/PDF 생성·게시 안 함 |

| 상태 축 | 상태 | 근거 |
|---|---|---|
| documentation | draft_complete_with_gaps | 7영역 조사, 미확정 보존, 독립 검토 전 |
| static_review | original_pin_and_pdf_review_complete | 원본 선언/핀·해시/Git blob·PDF 렌더, 실제 실행 아님 |
| ui_records | not_run | 코드·운영기록 변경 없음 |
| publication | not_published | 로컬2차133 통합·게시 제외 유지 |
| tia_compile | not_performed | 현재 TIA 환경으로 컴파일하지 않음 |
| live_cpu | not_performed | 온라인 CPU 확인 없음 |
| field_recovery | not_performed | 전기/기계 실측·수리·복구 없음 |
| simulator | permanently_stopped | 생성·변경·실행·행동시험0 |

### 남은 자료와 판정 기준

1. 현재 VR01/M21 명판·설치 위치·CY01 배출 연결·도면 개정/개조 이력. 역사 P&ID 배치와 현재 실물 동일성 분리.
2. 현재 프로젝트에서 Q2.6/I3.4·DB13.X3.4 및 HMI3주소, 호출파라미터/실제 버튼 이벤트, 1193의8피연산자 결속.
3. 현재 OB/FC 호출 주기·순서·ON/Simulation(1) 상태, ENO/DisableENO 실제 의미, 외부/간접·일괄 쓰기와 리테인.
4. 46QM1/46KM1/46QS1 현행 모델·보조접점 번호/극성·코일·단자와 케이블1_16 말단 대조. 현장 보호설정은 읽기 자료로 확인하며 변경하지 않음.
5. 원시입력/처리입력·FAULT·요청·출력의 시간상관과 접촉기/모터/분진배출의 별도 복구 증거.
6. 운전시간의 외부 저장/핸드셰이크, HOUR=1/0 전송 동작과 실제 누적 기록의 관계.
7. 통합/게시가 향후 별도 승인되면 기존 완료설비·원본·미지필드·저장키를 보존한 UI/기록/회귀/배포 검증. 현재 초안만으로 완료 수나 실제게시 수를 늘리지 않음.

새 현장 자료 없이 같은 미확정을 반복 조사하거나 제어값을 추정하지 않는다. 다음 단계는 사용자 독립 검토이며, 새 Work/Codex 또는 로컬 통합·게시를 이 초안이 허가하지 않는다.

## 9. 재현·보존 검증

- 시작 Git HEAD=abcf31c5030bc7ef8749ed8e869a857f2387a28a, VERSION=1.12.0, git status --short 빈값.
- 읽기전용 preflight.py 결과 inventory_matches=true. 전체248/부모없음108/하위140/우선23/대응18/기존제외90/부모보류7/phase2 133 유지. source_byte_changes는 기존 requirements-audit.json/all-in-one-data.json 두 파일이며 이번 변경이 아님.
- 정적 XML 파싱·선언/핀 탐색, PDF8쪽(전기4, 시공3, P&ID1)의 실제 렌더 및 P&ID 상세영역 확대를 수행했다. 렌더는 원본을 수정하지 않는다.
- 파일 SHA256은 아래 목록 및 extracts/VR01/source-sha256.json에 기록했다. 각 파일을 고정 커밋의 git show blob과 바이트·SHA256으로 대조했다. XML·PDF만이 아니라 사용한 주소/HMI/색인/대장도 포함한다.
- 미실행: simulator 생성/실행/시험, TIA/CPU/현장, npm/웹UI/기록쓰기/패키지/배포. 조사초안 범위에 필요하지 않으며 금지/미승인 작업을 실행하지 않았다.


### 원본 SHA256 / Git blob 대조

검사 파일 68개 전부 파일 바이트 및 SHA256 = 고정 커밋 Git blob. 종료 Git status: clean.

| 파일 (고정 저장소 상대경로) | SHA256 | Git blob |
|---|---|---|
| AGENTS.md | `0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2` | 일치 |
| VERSION.json | `5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7` | 일치 |
| WORKSPACE-HANDOFF.md | `215096d997782e78e901dfae36c782937e49611fbeb677a0d3fa50cbecf8d074` | 일치 |
| PUBLICATION_STATUS.md | `efe4857aec598d90470322cf3962eb3fe1f64947630e1fdf71d1c90134de8740` | 일치 |
| EXPANSION-WORK.md | `ec624de9fd2fcfac861a67fd5e828b25ef46db50bfd7a37ff16e2cb54cd0f7e2` | 일치 |
| all-in-one/ACTIVE-WORK.md | `eff3bbc08ecff41da3beff77f3fec48e7d148708192bcaaab00f34b6a721afc2` | 일치 |
| .agents/skills/gme-equipment-rollout/SKILL.md | `fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b` | 일치 |
| .agents/skills/gme-equipment-rollout/references/source-map.md | `40612c5efb8f94608840c7bc0e9095ea840df54920861c388ae48ea34c7998dc` | 일치 |
| .agents/skills/gme-equipment-rollout/scripts/preflight.py | `395067d6da20af3e1d82a43b7936907a87a44d8d2e11e4ebc61b1fc441e2adb6` | 일치 |
| docs/equipment-standard/WORK-STANDARD.md | `05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99` | 일치 |
| docs/equipment-standard/WORK-ITEM-TEMPLATE.md | `4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586` | 일치 |
| docs/equipment-standard/INVENTORY.json | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` | 일치 |
| all-in-one/registers/equipment.json | `7870325dff32bbca90fa34507b301c4aad3347d669fddcd03b910343663996fa` | 일치 |
| all-in-one/registers/plc-symbols.csv | `a0334b390f06ddb515d6c09ca96a01d35d44029c1b726ef0ff53303ec04ff91f` | 일치 |
| all-in-one/registers/control-spec.json | `1e495b32f1f11b910919fbd2945e842a019fce9a27a6a0d7298041a7fab00079` | 일치 |
| all-in-one/sources/hmi_plc_tags.csv | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` | 일치 |
| all-in-one/sources/decoded-original/network-map.json | `c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60` | 일치 |
| all-in-one/sources/Electrical_Rev2.pdf | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` | 일치 |
| all-in-one/sources/Electrical_Can_Decoating_20241118.pdf | `3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd` | 일치 |
| all-in-one/sources/PID_1684n002I.pdf | `2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b` | 일치 |
| all-in-one/sources/decoded-original/0019-FlgNet.xml | `a3301f4d07c2d36aefa6faa6c3559a1cff4565fc6de40cd17e54b548b30c0ce5` | 일치 |
| all-in-one/sources/decoded-original/0024-FlgNet.xml | `a463981da8db46dd7eeb44e592d38807704886d597e728bb652dba4c12cc8f67` | 일치 |
| all-in-one/sources/decoded-original/0030-FlgNet.xml | `9252c9da764993de1edb8b2e44c46d6e9f9d4b6118e751a0dbeaa9ffd8ea721b` | 일치 |
| all-in-one/sources/decoded-original/0031-FlgNet.xml | `76385eab8f8f72b9faa16f7cf8905f395591b18c0a9ee9e6d7dd085a38c45c65` | 일치 |
| all-in-one/sources/decoded-original/0162-FlgNet.xml | `892eab96a4f5c87cfafd35f8a2e2a04982a93ca23c777312101882e408b11deb` | 일치 |
| all-in-one/sources/decoded-original/0164-FlgNet.xml | `15884b2b362842279b626b669a484b1daa269f5ecd99112b8391bb0387382491` | 일치 |
| all-in-one/sources/decoded-original/0165-FlgNet.xml | `4513a5f6e77717c99c5e869105483be31f7f62ab280e271dc36cd7a2d3e3bb88` | 일치 |
| all-in-one/sources/decoded-original/0166-FlgNet.xml | `0330a505877be92172f94bce83222a0bfc8d64aab700a69fc1fa2188010d3853` | 일치 |
| all-in-one/sources/decoded-original/0251-FlgNet.xml | `6446b2b475b59f69889a408df794d2ed43cc6343f999045c00243b6d0663e017` | 일치 |
| all-in-one/sources/decoded-original/0252-FlgNet.xml | `66b8bf7c1e033f2e6710ab6959e1f5ec2cf27bd6e90c8780eb1bd6daebf76749` | 일치 |
| all-in-one/sources/decoded-original/0315-FlgNet.xml | `ee681be380623ee8d2e3d5eb524d8462c61c38f52fd15fe7c1884d65491df5f6` | 일치 |
| all-in-one/sources/decoded-original/0337-FlgNet.xml | `403f3a0e9218bbe81fb00cb93fb9f6bd3570af2df157abccd878a3a1f60f2580` | 일치 |
| all-in-one/sources/decoded-original/0341-FlgNet.xml | `e9921cb52ecba4ef1df14758d29e4091fc510a8e792130e855b869dbab4a1c96` | 일치 |
| all-in-one/sources/decoded-original/0370-FlgNet.xml | `ccf6117d6bd9dfbf7e54915f590e6354ae17575a893ecb931d997008c0d214fd` | 일치 |
| all-in-one/sources/decoded-original/0397-FlgNet.xml | `bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834` | 일치 |
| all-in-one/sources/decoded-original/0404-FlgNet.xml | `ed02308b8d0b1c52fd734826cccb82d25709b8b9d65af07557c1b1e9c8de2570` | 일치 |
| all-in-one/sources/decoded-original/0549-FlgNet.xml | `49f7169c33ed7f54559b0801e21a7d618584900972840e91cf51ad032e8febb1` | 일치 |
| all-in-one/sources/decoded-original/0067-IdentXmlPart.xml | `0aa469d4f7a20bde2a5bccc6c91b3d9c48929460bd68ef32e0217d53f4d68628` | 일치 |
| all-in-one/sources/decoded-original/0555-IdentXmlPart.xml | `46c36333e249dd775c1db94a1f6e80a36cf1a5a9c998b7d0980ae01d862901e6` | 일치 |
| all-in-one/sources/decoded-original/0575-IdentXmlPart.xml | `40e7b2caf89ab7f1ed9075547a7728bd02441e24451bdd8bf97c843637daad06` | 일치 |
| all-in-one/sources/decoded-original/0576-IdentXmlPart.xml | `c8b5f9b9ead0e124f1f817b49d89611ed7b2ce04ecd91ddaa139f2ec89d48dbe` | 일치 |
| all-in-one/sources/decoded-original/0577-IdentXmlPart.xml | `511e01fae619dc385357908a1ac62030dbdfd5f5399bd4c22bc58bebbfc3bf47` | 일치 |
| all-in-one/sources/decoded-original/0578-IdentXmlPart.xml | `0f9f41b5dee25ea17c7a29ab6f7b00503c13d0f265266acd660072baf061d32b` | 일치 |
| all-in-one/sources/decoded-original/0602-IdentXmlPart.xml | `46ab21151eddaaf616469db520730c60423eb742aa491af194e6710c751b4caf` | 일치 |
| all-in-one/sources/decoded-original/0603-IdentXmlPart.xml | `e93969dfa281d75b49b24127793068e33472dadb19729c1c48fc4a8dad075ef8` | 일치 |
| all-in-one/sources/decoded-original/0604-IdentXmlPart.xml | `b798d29c5499b5314a1ee3cff9139dae64c887533b86baa43b6e9a052373a6af` | 일치 |
| all-in-one/sources/decoded-original/0605-IdentXmlPart.xml | `0ff6e2228dbfbc9f657359fe1055083ce621365084ea24c4160e4969b3eaac8b` | 일치 |
| all-in-one/sources/decoded-original/0606-IdentXmlPart.xml | `73d45f9e2a34bba8a25df1ed1f71e8f6404fc96a8d6481672652a48435b6a740` | 일치 |
| all-in-one/sources/decoded-original/0613-IdentXmlPart.xml | `09d3b1397a987898334218f37e025661af162438582e649f671e7abec443d3cb` | 일치 |
| all-in-one/sources/decoded-original/0614-IdentXmlPart.xml | `c6de26f74d75f5be858a406de75eaf6faf62ba9b89c8f9a085b5dd206e93d294` | 일치 |
| all-in-one/sources/decoded-original/0615-IdentXmlPart.xml | `80f4544edca56c6e6bb2713c758c92ade9202255110074931e03fe34d0d0801a` | 일치 |
| all-in-one/sources/decoded-original/0616-IdentXmlPart.xml | `650b53354a0c8443d94adc5bd6a860d3c5313014a52e0fb98a5656a65b58cc0d` | 일치 |
| all-in-one/sources/decoded-original/0623-IdentXmlPart.xml | `4acd00406ea92466169e57e59fc90b0da4d9ec55fd19e2e96c9556e939cb83a6` | 일치 |
| all-in-one/sources/decoded-original/0624-IdentXmlPart.xml | `24607c0827fbde428bccf8637ef4ae490798a69a7c2f3b87861d0749082d367a` | 일치 |
| all-in-one/sources/decoded-original/0625-IdentXmlPart.xml | `17a9f9bd540bf0a54e9973391fa258d81e567248fd201ae4ff32c367359e69f9` | 일치 |
| all-in-one/sources/decoded-original/0626-IdentXmlPart.xml | `a9d7fbea345eca70325a8c2e44058c23e96add1b7207eabbb09445118b18188b` | 일치 |
| all-in-one/sources/decoded-original/0627-IdentXmlPart.xml | `08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb` | 일치 |
| all-in-one/sources/decoded-original/0628-IdentXmlPart.xml | `9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd` | 일치 |
| all-in-one/sources/decoded-original/0629-IdentXmlPart.xml | `67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972` | 일치 |
| all-in-one/sources/decoded-original/0634-IdentXmlPart.xml | `af3fcb536a6270ffb9a19e5b3f2c284a38d67d465f5147961005c1c01d11299d` | 일치 |
| all-in-one/sources/decoded-original/0635-IdentXmlPart.xml | `1a057d686446a3fdab7ac61bb09bc543c52f49646c9ca71ac323c10fcdffe457` | 일치 |
| all-in-one/sources/decoded-original/0652-IdentXmlPart.xml | `251bb1b3ce1bdf3686545062e5803152779de8a4961539d30e6951a2a10ab692` | 일치 |
| all-in-one/sources/decoded-original/0655-IdentXmlPart.xml | `38e9f323024fba19582b473f39b1ed03ffe6a0b390218894029a6edb0b1ff9fb` | 일치 |
| all-in-one/sources/decoded-original/0656-IdentXmlPart.xml | `0dbc45e84732a8848f17b094ea08ab8578dbf240bfe15cd7086859395c27c592` | 일치 |
| all-in-one/sources/decoded-original/0657-IdentXmlPart.xml | `0f70cda60a6b1a17175876d58e25b2686952642de6cffb21213aeef8b347a22b` | 일치 |
| all-in-one/sources/decoded-original/0658-IdentXmlPart.xml | `998294c0c8a99e00ceb33c2c60def2cd4850e34328917ae506244c2be2df3831` | 일치 |
| all-in-one/sources/decoded-original/0688-IdentXmlPart.xml | `ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda` | 일치 |
| all-in-one/sources/decoded-original/0692-IdentXmlPart.xml | `bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037` | 일치 |


## 전달 전 핵심 근거 제한 검토

2026-10-11 조사 초안 취합 단계에서 핵심 출력/타이머/운전시간 또는 요청쓰기의 원본 Part/Wire를 표본 재대조하고, 도면 전달 끝점을 실제 렌더로 재확인했다. 인용 원본 SHA256도 전부 재계산하여 일치했다. 전체 원본의 의미 검토나 현재 CPU/현장/통합/게시 검증을 뜻하지 않는다. 사용자 독립 검토용 초안이며 미확정 경계는 유지한다.
