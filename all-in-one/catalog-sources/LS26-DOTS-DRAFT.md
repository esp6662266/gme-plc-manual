# LS26 — PV02 Gate A 닫힘 리미트 독립 원본 조사 초안

- 대상 LS26 하나, 부모 PV02, component/depth1/phase2, priority_key=null. INVENTORY catalog[239] 및 BATCH24 scope의 parent_child_separate 분류. 부모·동명이명 LS·CL05/06 완료를 상속하지 않는다.
- 고정 원본 source-mv06: abcf31c5030bc7ef8749ed8e869a857f2387a28a, v1.12.0. GME-STD-1.0.0, AGENTS·skill·WORK-STANDARD·WORK-ITEM-TEMPLATE 및 최신 인계 상단 적용. 2026-10-11 UTC. 실제 모델/추론 설정 UI 증명은 미확인.
- PV02와 CYL-CL05~08 초안은 탐색색인/공통근거로 재사용했다. 부모 전체 제어를 재조사하지 않고 LS26의 선언·핀·다른 쓰기·PDF 접속점/끝점/개정을 독립 확인했다. CL05 0288 W65/W67 operand 정정을 유지한다.
- 문서 초안 및 정적 검토만. 원본/공통코드/버전/대장/배포/운영/PLC/현장/보호값/SEJIN 변경0, 시뮬레이터 작성·수정·생성·실행·행동시험0, 원본 생성기/앱빌드0, 재위임/새 Work/Codex/업로드0. own draft/extracts만 작성했다.

## 1. 설비·자료 기준 — 적용

문서상 LS26은 PV02 Gate A CLOSE 리미트다. OEM E9.5 및 백업 EV04_Close I9.5를 결속했다. 명칭 ‘CLOSE’, 도면 NO13–14, 원시값, DB13 처리값, DB2 위치기억, DB11 HMI 표시는 서로 다른 계층이며 현재 정상극성/실제 완전폐쇄를 증명하지 않는다.

| 원본 | 직접 확인 위치·개정 | 해석과 경계 |
|---|---|---|
| all-in-one/sources/PID_1684n002I.pdf | PDF1 PV-02 Detail, 도면1684n002 Apex I, 기본06/04/2011, I개정15/01/2013, FG ‘−’ | LS26 리더는 CL05 몸체/피스톤 측 인접부, LS25는 로드 측. EV04 뒤 CL05/06 공유 공압 분기. 오른쪽 Gate A/B 도식과 대조하되 CL05 실물 독점소유·CL06 장착을 추정하지 않음 |
| all-in-one/sources/Electrical_Rev2.pdf | FG72/PDF73, LOAD DRUM CLAPPE VALVE PV-02, DATA27.05.2024, 개정란 공란 | LIMIT SWITCH GATE “A” CLOSE, LS26 NO13–14, X1/147·148/E9.5 |
| 같은 OEM | FG125/PDF126 DIGITAL INPUT MODULE, DATA27.05.2024, 개정란 공란 | CPU515 MOD10 단자16 E9.5, LIMIT SWITCH LS-26 GATE “A” CLOSED VALVE PV-02, 교차72/3 |
| all-in-one/sources/Electrical_Can_Decoating_20241118.pdf | PDF24/64 CANDC-CONS-E007-024, D-PAGE7, ROTARY ROUTE CONDUIT PIPING(1), Rev1 24.11.11 first draft design | ROT1TB1 분기6 LS26, 고유 전체 케이블ID 확인 |
| 같은 시공자료 | PDF55/64 CANDC-CONS-C005-055, D-PAGE5 CABLE SCHEDULE(4), Rev1 24.11.11 first draft design | LS26 고유5_5 행, PDF24 짧은 번호와 상충 |

파일명 Rev2를 FG72/125 개정번호로 전파하지 않았다. 실제 PDF5페이지 및 P&ID 상세/제목 확대를 직접 렌더·판독했다. 시공표는 승인 준공/실측으로 승격하지 않는다. CL05와 CLIENT-CL05는 다른 대장 ID이며 LS26 이름/번호만으로 합치지 않는다.

기존 all-in-one/devices/LS26.html의 I9.5 관련1개와 ‘직접 래더 식별 안 됨’은 파생 이름검색 한계다. 이번 원본 EV04_Close 경로를 보강하되 옛 주석 E29.7을 현행 백업 주소로 대체하지 않는다. 기존 페이지의 시뮬레이션 설계 문구는 중지 자산의 과거 기록이며 재개 승인/실행 실적이 아니다.

본문 네 자리 XML 번호는 all-in-one/sources/decoded-original/NNNN-FlgNet.xml 또는 명시한 NNNN-IdentXmlPart.xml. LAD는 network-map의 document_id, RID/NID/UID/Part/Wire는 동일 원본 문맥으로 대조한다.

## 2. I/O·HMI·기억값 — 적용 / HMI 결속 일부 미확보

| 계층 | 주소·형식 | 선언·문맥 |
|---|---|---|
| raw | EV04_Close I9.5 Bool | 0607 SimpleAccess RID137, SAD Input, SSD AO77, NID13 UID44 |
| 처리 | Inputs.PV-02 EV A CLOSE DB13.DBX9.5 Bool | 0609 GlobalAccess RID138, AO77/BAD86, NID13 UID45; 0608 Inputs RID86 TOD13 |
| raw word | Tag_181 IW8 Word | 0627 RID15 SAD Input AO64, NID1 UID47 |
| 처리 word writer | DB13.DBW8 Word | 0629 RID16 AO64/BAD4, NID1 UID48 AK Write; 0628 Inputs RID4 TOD13 |
| 부모 방향 출력 | PV-02 GATE A EV Q5.4 Bool | 0607 RID85 SAD Output AO44, NID13 UID43/47 읽기; NID8 UID733 쓰기. LS26 독립 출력 아님 |
| 부모 닫힘기억 | Flag.PV_02_GATE_A_MEM_CLOSE DB2.DBX8.4 Bool | 0609 RID139 AO68/BAD5, NID13 UID46 S/48 R; 0608 Flag RID5 TOD2 |
| 공통 전제 | ON M0.0 Bool | 0607 RID1 SAD Memory AO0, NID13 UID36; 상수 true로 치환하지 않음 |
| HMI 설정 | PV_02\GateA_Close DB11,X78.2, ID000A5, Access Name PLC | hmi_plc_tags.csv, dde.cfg 설정. LS26 raw/처리/기억과 주소가 다름 |

0392 LAD1216/NID40의 CRef22 RID716, CodeBlock23 RID715는 0624/0623 HMI PV_2Gate 호출이다. GateA_Close 입력은 W46/ORef25/RID735→CRef22.GateA_Close, 출력은 CRef22.HMI_GateA_Close→W59/ORef38/RID745. 두 실인수의 동일 문맥 선언 결속은 확보하지 못했다. 따라서 DB13.X9.5→DB11.X78.2의 완전한 전달·반전 여부를 확정하지 않는다. 부모 초안의 HMI17 미결속을 이름이나 인수 순서로 해소하지 않는다. CSV는 현재 화면·색·이벤트·쓰기·통신 정상 증거가 아니다.

## 3. 제어 구조 — 적용 / 정적 범위

### 3.1 raw→처리 word와 호출

0397 LAD1070 hmi inputs NID1: Move42.eno→W53→Move43.en, W55/ORef47/RID15→Move43.in, Move43.out1→W57/ORef48/RID16. 위 선언으로 IW8→DB13.DBW8을 확인했고 그 안에 I9.5/DB13.X9.5가 포함된다. bit NOT는 없으며 Move43에는 DisableENO=true, 원문 W56으로 Move43.eno→Move44.en 연결도 있다. 실행 의미를 임의 보정하지 않는다.

0030 LAD1613 main NID19: CRef25(HMI Output).eno→W42→Contact37.in, W44/ORef45/RID140→Contact37.operand(Negated), Contact37.out→W43→CRef28.en. 0692 RID140 Simulation(1) Memory AO1440=M180.0. 0694 RID136/NID19 UID28 TORID135 및 0688 RID135 HMI Inputs TOD15/CodeBlock29로 호출 결속한다. 현재 호출·M180.0·ENO·다른 writer가 미확인이므로 매 스캔 raw=처리라고 단정하지 않는다.

### 3.2 닫힘 위치기억: raw와 처리 OR 및 방향 조건

0288 LAD1923 r1 scraps gate 2 NID13:

- W49 powerrail→Contact21.in; W50/ORef36/RID1 ON→operand. Contact21.out W51은 여러 방향 가지로 분기한다.
- W63/ORef43/RID85 Q5.4→Contact29.operand는 Negated. Contact29.out→W64→Contact30/31.in.
- **W65/ORef44/RID137 EV04_Close→Contact30.operand**, Contact30.out→W66→OR32.in1.
- **W67/ORef45/RID138 Inputs.PV-02 EV A CLOSE→Contact31.operand**, Contact31.out→W68→OR32.in2.
- OR32.out→W69→SCoil33.in, W70/ORef46/RID139→SCoil33.operand DB2.X8.4.
- Q5.4는 W71/ORef47/RID85→비반전 Contact34.operand. Contact34.out→W72→RCoil35.in, W73/ORef48/RID139→RCoil35.operand DB2.X8.4.

정적 식: S MEM_CLOSE = ON AND NOT Q5.4 AND (I9.5 OR DB13.X9.5); R MEM_CLOSE = ON AND Q5.4. raw/처리 접점30/31에는 NOT가 없다. W65/W67은 전력 흐름이 아닌 operand선이며 W66/W68과 구분한다. 기억이 이미 S된 뒤 두 입력이0이 되는 것만으로 해제되는 직접 R가지는 이 네트워크에 없다. 따라서 MEM=1을 센서현재값=1 또는 실제 완전폐쇄의 증거로 쓰지 않는다. 부착 실린더 CL05의 독립 위치기억으로 소유를 바꾸지 않는다.

부모 요청→Q5.4→EV04→공압 구동은 PV02/CYL-CL05~06 공통근거로 참조한다. LS26을 별도 EV/닫힘코일/출력으로 추가하지 않는다. 부모 순서0의300ms 전이가 LS26 폐쇄확인 대기라는 뜻은 아니다. 부모 상태기계 전체는 이번에 반복 의미검토하지 않았다. 69KA/71KA EV 부하접점5–9 정정을 보존한다.

### 3.3 위치기억의 다른 쓰기: startup word와 S

0147 LAD402 startup only NID2는 같은 기억 주소를 포함한 word쓰기다. 0047 RID1 ON M0.0 NID2 UID167→W184→Contact208.operand. Contact208.out→W209→Move155.en. W196/ORef176/RID54→Move155.in의 0048 literal INT#0(NID2 UID176), Move155.out1→W197/ORef177/RID15의 0563 Word AO64/BAD6, 0562 Flag RID6 TOD2를 대조했다. 이는 DB2.DBW8 영쓰기이며 DB2.X8.4를 포함한다. 다른 word/간접 writer 전체를 검증했다는 뜻은 아니다.

0150 LAD405 startup only NID5: W328 powerrail→Contact326.in, W319/ORef313/RID1 ON(0047)→operand; out W327→SCoil303.in, W320/ORef314/RID49→SCoil303.operand. 0563 RID49 AO68/BAD6 및0562 Flag DB2로 MEM_CLOSE S를 확인했다. 이 S 경로에는 LS26 접점이 없다. startup 내 word초기화와 후속 S, 일반0288 S/R을 구분하며 현재 CPU 시작 호출·보존/초기상태·스캔 우선순위는 미확정이다.

### 3.4 DB13 처리값의 다른 writer — 보존 XML 정적 확인만

0411 LAD1091 simulation NID13은 기존 원문을 읽었을 뿐 작성/수정/생성/실행/행동시험하지 않았다.

Powerrail W21→Contact24.in, W42/ORef32/RID213 Q5.4→Contact24.operand(Negated); Contact24.out→W43→일반 Coil25.in; W44/ORef33/RID216→Coil25.operand. 0636 RID213 SAD Output AO44/NID13 UID32, 0635 RID216 AO77/BAD5 NID13 UID33 AK Write 및0634 Inputs RID5 TOD13으로 결속한다. 원문상 NOT Q5.4에 의한 DB13.X9.5 writer이며 물리 I9.5 writer나 실물 피드백이 아니다. 블록 이름만으로 현재 CPU에서 활성/비활성을 단정하지 않는다. 원시 word복사와 이 writer의 현재 실행순서·최종값·온라인 수정/외부 쓰기는 미확정이다.

## 4. 전기 전달 끝점 — 적용

FG72/PDF73 및 FG125/PDF126을 실제 렌더하여 접속점·NO접점·교차참조 양끝을 확인했다.

| 순서 | 원문 끝점 | 해석·미확정 |
|---|---|---|
| 공급 | +24Vdc10.7 수평선, 교차70/9→73/0에서 접속점 분기 | 센서 공급. EV04의110Vac 부하와 구분 |
| 보호·단자 | X1/147, 5×20 2A F → wire72.2 | 도면값이며 현행장착/교체 승인값 아님 |
| 센서 | LS26 NO13→14, Gate A CLOSE | NO도식과 실제 폐쇄 때 전기상태·캠/장착은 별개 |
| 입력 복귀 | LS26 14→X1/148→E9.5, FG125/5 교차 | LS25의 X1/145·146/E9.4와 혼합금지 |
| PLC 모듈 | FG125 상단72/3→E9.5→CPU515 MOD10 단자16 | 백업 도면 장치표기이며 실제 CPU모델/현재 채널 확인 아님 |
| 모듈 공통 공급 | +24Vdc10.7→X21/3010(5×20 2A IST.)→wire125.1→단자19; −0Vdc10.6→단자20 | LS26 접점의2심선과 모듈공급 경로를 구분 |

시공 PDF55의 LS26 고유 행은 **5_5 =ROT+PV02-LS26A, UC-01 ROT1TB1→PV-02 LS-26, DC CVV 2C SIZE1.0 SPARE0**, 경로 RDD1 E300 / 100 RDD1 / RDD1 E600, adjustment4, LEN13이다. 이는 설계길이이며 실측 아님. 공유5_1 =ROT+UC01-ROT1TB1A CR→UC-01 ROT1TB1은 LS25–32/PB16 묶음 DC CVV25G SIZE1.0 SPARE5, LEN52다. 공유함/간선이 LS26 소유 전체 설비를 뜻하지 않는다.

PDF24의 ROTARY SIDE01 도식 분기6은 LS26, 분기5는 LS25, 분기7은 EV04다. LS26 전체ID는 동일하지만 짧은 No.는 **5_4**, PDF55는 **5_5**로 다르다. PDF24 공유 ROT1TB1A CORE26 대 PDF55 25G도 상충이다. 짧은 번호만으로 결선하거나 번호·심수를 임의 정정하지 않는다. PDF55 LS27/28 추가행을 CL06 전용 리미트/LS26 병렬접점/예비로 추정하지 않는다. OEM X1/147·148↔ROT1TB1 개별단자/심선 매핑은 미확보다.

## 5. 알람·복구 — 부모 의존 / 독립 LS26 알람 미확보

LS26 독립 고장알람·타이머를 만들지 않는다. 관련 부모 PV02 A_NOT_CLOSE의 감시 입력이 raw LS26 자체가 아니라 MEM_CLOSE라는 점만 고유 경로로 재확인했다.

0451 LAD1817/NID44: ON Contact1656→W1657→NOT Q5.4 Contact1668(W1643/ORef1621/RID160), out W1669→NOT MEM_CLOSE Contact1683(W1686/ORef1684/RID164), out W23→SdCoil1599.in. 0658 RID160 Output AO44, 0657 RID164 AO68/BAD12 및0655 Flag RID12 TOD2 결속. SD value W1644/ORef1622/RID320는0656 NID44 UID1622 S5T#7S, operand W1645/ORef1623/RID186는0658 Tag_85 Timer AO108=T108.

부모 감시식은 ON AND NOT Q5.4 AND NOT MEM_CLOSE. Timer접점1670(W1646/ORef1624/RID186)→W24→SCoil1605, W1649/ORef1626/RID187는0657 Allarm.PV_02_GATE_A_NOT_CLOSE AO86/BAD10 +0655 Allarm TOD3 =DB3.X10.6. Reset은 ON→RESET_ALLARM Contact1674(W1651/ORef1627/RID13)→W1675→자기알람 Contact1676(W1652/ORef1628/RID187)→W1677→RCoil1610(W1654/ORef1629/RID187). 센서 회복만으로 래치가 자동 해제된다고 쓰지 않는다.

7초는 부모 백업 감시설정이며 LS26 센서응답시간/정격/현행 보호값이 아니다. startup S와 DB13 다른쓰기 때문에 알람/기억만으로 센서정상·실제폐쇄를 판정하지 않는다. 공통 Reset 생성과 전체 공정 영향은 PV02 초안 참조이며 이번에 부모 전체를 재검토하지 않았다. HMI Allarme1 통합표시와 개별DB3비트를 동일시하지 않는다. 강제출력·점퍼·센서우회·지연증대·무조건 Reset을 수행/권고하지 않는다.

## 6. 증상별 관찰 — 적용 / 현장조작 절차 아님

이미 승인된 관찰자료에서 시각/시간대·관찰자·수집장치·현재 프로젝트 식별·값/단위·물리위치·비교원본·조치/복구증거를 서로 분리하여 기록한다. 실제 운영자료는 공개 저장소에 복제하지 않는다.

| 증상 | 필요한 관찰·비교 | 판정 한계 |
|---|---|---|
| 닫혔다는데 I9.5=0 | 실물표찰/캠위치와 X1/147·148, E9.5 같은 시각의 승인 관찰 | 배선/접점/기구/극성을 데이터 없이 단정하지 않음 |
| raw와 DB13.X9.5 불일치 | IW8/DB13W8, HMI Inputs 호출·M180.0·writer 경로 | 현재 모드/실행순서 미확정; 변경시험 안 함 |
| DB2.X8.4=1인데 raw=0 | Q5.4, raw/처리 양측, startup 이력 및 기억전환 시각 | S/R 기억은 현재 센서값이 아님 |
| 부모 닫힘알람 지속 | Q5.4/MEM_CLOSE/T108/DB3.X10.6/Reset요청의 관찰 시각 | 7초 임의 변경/리셋 처방 금지 |
| HMI 닫힘표시만 다름 | DB11.X78.2 설정, 객체/통신/실인수 Export | CSV·핀만으로 화면 전달 완전확정 불가 |
| 케이블5_4/5_5 혼동 | 전체 =ROT+PV02-LS26A와 FROM/TO·승인준공도 | 짧은 No.만 연결 금지, 현장증거 없이 정정 안 함 |

## 7. 완료·누락 및 다음 한 작업

| 구분 | 상태·근거 |
|---|---|
| documentation | complete_with_gaps. 7영역 초안, 소유/실물/현행 경계·상충 보존 |
| static_review | 아래 선정원본 해시/Gitblob 및 지정 XML/CSV/PDF 직접 검토. 부모 독립검토 대기 |
| ui_records | not_run. 도면·래더 비교/백업·선택복원/전후기록/보고서PDF 네 기능 구현·저장·재열기 미검증 |
| publication | not_published. 부모 PV02 과거 게시실적을 LS26에 상속하지 않음 |
| tia_compile / live_cpu / field_recovery | not_performed 각각 유지 |

남은 자료: LS26 명판/장착·캠·정상극성/실제완전폐쇄 관계, 승인준공 OEM↔ROT1TB1 단자·심선표 및5_4/5_5·CORE26/25G 해결개정, 현재 PLC 프로젝트/CPU 호출·다중쓰기·보존초기값, HMI RID735/745 동일문맥 실인수 Export/객체이벤트·통신, 승인된 동시관찰과 실제원인제거·복구증거. 센서 모델·정격·보호값·정비주기·안전위치는 자료 없이 채우지 않는다.

다음 한 작업: 부모 검토자가 LS26 고유 W65/W67, startup word/S, 다른 DB writer, PDF5쪽 및 해시를 독립 대조한다. 원본·대장 변경이나 현장확인은 이번 산출물 완료와 별도다.

## 부록 A. 검증 범위와 추출

직접 의미검토: FlgNet8개(0030/0147/0150/0288/0392/0397/0411/0451)의 지정 경로와 Ident22개의 해당 선언, HMI CSV1개 지정행, PDF3파일의5페이지(PID1;OEM73/126;시공24/55). 전체파일 모든 명령·PLC 전체 writer를 검증한 것이 아니다. 대장/지침/기존 HTML/network-map은 배경·보존·탐색 근거다. 이름검색 및 파일 SHA 수를 의미검토 수에 합산하지 않는다.

own extracts/LS26에는 원문네트워크 사본, 선언검색/발췌JSON, PDF5페이지 PNG·text 및 PID 상세/제목 확대2개, source-integrity.json, checks.json을 보관했다. 기존 부모/실린더 초안은 파생 연구자료이며 고정 Gitblob 원본으로 위장하지 않는다. 원본 preflight/생성기는 실행하지 않았고 own 정적 대장·해시·핀검사로 범위를 제한했다.

## 부록 B. 선정 모든 원본 SHA256 / 고정 Gitblob

선정 48파일, SHA256 계산 48개, 고정 Gitblob 바이트 일치 48/48. Git 변경 0. 이는 CPU/실물 동일성 증거가 아니다.

| 원본 경로(source-mv06 기준) | SHA256 | 고정 Gitblob OID | 바이트 일치 |
|---|---|---|---|
| AGENTS.md | `0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2` | `073164bc6efd5791032d62c71b03b4dab48cb6f8` | True |
| .agents/skills/gme-equipment-rollout/SKILL.md | `fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b` | `9aa820ea6ca15b4e136c9772423b78ed4df6a3d4` | True |
| .agents/skills/gme-equipment-rollout/references/source-map.md | `40612c5efb8f94608840c7bc0e9095ea840df54920861c388ae48ea34c7998dc` | `49e50a7a8e56a16e2ec7f3607a03fd90adb8f1d3` | True |
| docs/equipment-standard/WORK-STANDARD.md | `05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99` | `f76a570cc73098632e08759b17934000f7e3a253` | True |
| docs/equipment-standard/WORK-ITEM-TEMPLATE.md | `4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586` | `e546f39535d2b589e80f97db869ac37ce4d05cfd` | True |
| docs/equipment-standard/INVENTORY.json | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` | `587c3748ad9224718f95ba06463fee913dae231d` | True |
| docs/equipment-standard/START-GPT61.md | `35769e3146ccd707fea2b81b67b30376b76a0a19c7e662fe2bb4fdd382306f94` | `0d08cab3678df7e2625251b641b138ef4956483b` | True |
| VERSION.json | `5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7` | `fffb51663b7705aec91cb119ca80ee943a4ce758` | True |
| WORKSPACE-HANDOFF.md | `215096d997782e78e901dfae36c782937e49611fbeb677a0d3fa50cbecf8d074` | `dd0b8989d2376c4415bba9bd826fe6754c6b1a12` | True |
| PUBLICATION_STATUS.md | `efe4857aec598d90470322cf3962eb3fe1f64947630e1fdf71d1c90134de8740` | `d76401cf291fc0be681acc51fa898ad3ce46ff78` | True |
| EXPANSION-WORK.md | `ec624de9fd2fcfac861a67fd5e828b25ef46db50bfd7a37ff16e2cb54cd0f7e2` | `4c42d88ecc2d48269eb23e13a20ebf3721a092a1` | True |
| all-in-one/ACTIVE-WORK.md | `eff3bbc08ecff41da3beff77f3fec48e7d148708192bcaaab00f34b6a721afc2` | `6eb947c629b5ddf9c759ef87649451303938864b` | True |
| all-in-one/devices/LS26.html | `32dd14ef0f102e2796d8b14392aede96312de6d0cdaff4340e77c9f8d4cef166` | `ec9ac648406bc11f16d05883522a2dd96562ae42` | True |
| all-in-one/sources/PID_1684n002I.pdf | `2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b` | `8c83a59fefd5b8b651ec3537ea4236a073f5e109` | True |
| all-in-one/sources/Electrical_Rev2.pdf | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` | `f610fd7c7ce14ae951b00cff57b969259bfb389d` | True |
| all-in-one/sources/Electrical_Can_Decoating_20241118.pdf | `3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd` | `0ee6b6f8361c5790864dbba4bbd9d55e8e7c08f8` | True |
| all-in-one/sources/hmi_plc_tags.csv | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` | `cf4c0650e7c7baac350dcb89909b808435704880` | True |
| all-in-one/sources/decoded-original/network-map.json | `c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60` | `424430b6b953e43138e5d0a18ca40c949e21cfa1` | True |
| all-in-one/sources/decoded-original/0030-FlgNet.xml | `9252c9da764993de1edb8b2e44c46d6e9f9d4b6118e751a0dbeaa9ffd8ea721b` | `e74c70b751acdcdbc7a8b3b0c98aa773c2107cab` | True |
| all-in-one/sources/decoded-original/0147-FlgNet.xml | `386513b215a8cc433f414b1b08279e9760e0efe209070ea95f8e445f674f428c` | `0027890eca158e714dd6260dc920a5d3aa83319b` | True |
| all-in-one/sources/decoded-original/0150-FlgNet.xml | `829ca4aa3bd2bb6ee406f7f204add2987ec6159ef0fd6dd3dfc075592664a98e` | `b8130ae4a433018f7513d24bd8f0cf79a7897238` | True |
| all-in-one/sources/decoded-original/0288-FlgNet.xml | `af4d15dcde4680ef5b788f88f198a47886857c8db7f7d9b550276fb5eea3c90e` | `a7b2995e8d87de3990a201969c0f7b9547e6d0ba` | True |
| all-in-one/sources/decoded-original/0392-FlgNet.xml | `067f6e3c2e5b4edd9c0cdb35734036534b3e2896dc51933c31300faaa6c60742` | `6348268e6c0b6108f9920cf43e8ace558dadda46` | True |
| all-in-one/sources/decoded-original/0397-FlgNet.xml | `bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834` | `4ab8370493c4e28fc1eabeeebe2743d27f0c4021` | True |
| all-in-one/sources/decoded-original/0411-FlgNet.xml | `282267b493e6b584959a5367d628bf86d15304d901a610614ecd2209d4d01884` | `c2143650e3de0e25c253e1652242e3cfdf4b394f` | True |
| all-in-one/sources/decoded-original/0451-FlgNet.xml | `8aeb19ab590824f4b357817cda08b46f962cec4eab5d967dcb0d829d44ca71e5` | `111d56c4bded1391beeff6073108ca1a5e2a19d2` | True |
| all-in-one/sources/decoded-original/0047-IdentXmlPart.xml | `2e53bb895dd1ad2a74efaeb1ef16dfd61e62b1b2d7aa34cec8612f1b9cb0928e` | `3dc282f149a21fdf76d5521ef1c833be63b578b4` | True |
| all-in-one/sources/decoded-original/0048-IdentXmlPart.xml | `d8e8687de7271bd294c2b62b33d789700af9d5014d82b130141988c4d479253d` | `64fc5a7f1ad33f3b901b00f0d22d23578ffabff8` | True |
| all-in-one/sources/decoded-original/0562-IdentXmlPart.xml | `85aada44dd9a3e66835463c3fed400f1efe121f4f5bc5ab8f0ad49481ec0ea1c` | `1609802542a3e560baba3f2b73c306be281dfb23` | True |
| all-in-one/sources/decoded-original/0563-IdentXmlPart.xml | `86cf35b6baebc079cb5a092baf53ec3364c377ea7318eb263ab69c8b4550b4ad` | `6a10fc694f896cda16409804daf2554c91635654` | True |
| all-in-one/sources/decoded-original/0607-IdentXmlPart.xml | `9b76b53536a26e7b45961fecbf825ae1552e16c2fd9af5736864193c01d77f93` | `dbd4da513171f04cca9b1c1741d0293c3e38f98c` | True |
| all-in-one/sources/decoded-original/0608-IdentXmlPart.xml | `24adec2035b65c0c310d637bcea74374896875b6465a16aa2f2cfc8fd55fa4b8` | `cea8f4160d2da00023b1ecc5e591b561e4a08330` | True |
| all-in-one/sources/decoded-original/0609-IdentXmlPart.xml | `395de8ebb2168848cf96fe015bd7334d71107c114a4e441ef36346b8f22031db` | `ee2aab34c0116642dd9f4364b236426f78a876a3` | True |
| all-in-one/sources/decoded-original/0623-IdentXmlPart.xml | `4acd00406ea92466169e57e59fc90b0da4d9ec55fd19e2e96c9556e939cb83a6` | `13b3af0459c8e6069bb9b2f1b16454bf479e08dc` | True |
| all-in-one/sources/decoded-original/0624-IdentXmlPart.xml | `24607c0827fbde428bccf8637ef4ae490798a69a7c2f3b87861d0749082d367a` | `02511fea47fc47981c101bba49dc40adde1cdcc3` | True |
| all-in-one/sources/decoded-original/0627-IdentXmlPart.xml | `08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb` | `61ebc0abbb2ca160e11e1da400a3f14a397d8bc5` | True |
| all-in-one/sources/decoded-original/0628-IdentXmlPart.xml | `9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd` | `170ca5c72599edc7ea7eefe651c3680ce325e76a` | True |
| all-in-one/sources/decoded-original/0629-IdentXmlPart.xml | `67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972` | `058129bb01e27f7a6a0d0293f332d745e5bab74e` | True |
| all-in-one/sources/decoded-original/0634-IdentXmlPart.xml | `af3fcb536a6270ffb9a19e5b3f2c284a38d67d465f5147961005c1c01d11299d` | `877d9e0734dc7f3e5a8cea789eeb58a208501f48` | True |
| all-in-one/sources/decoded-original/0635-IdentXmlPart.xml | `1a057d686446a3fdab7ac61bb09bc543c52f49646c9ca71ac323c10fcdffe457` | `95bfcad59cfb0c12b573e9e8face4262d1e94622` | True |
| all-in-one/sources/decoded-original/0636-IdentXmlPart.xml | `ec3d79f03e2748f8def4409ad676a97b98e28b9d8e68f6a64b3fe894466832ca` | `86114327ba1a010b2fcc01dd12b1bf86c01bc02c` | True |
| all-in-one/sources/decoded-original/0655-IdentXmlPart.xml | `38e9f323024fba19582b473f39b1ed03ffe6a0b390218894029a6edb0b1ff9fb` | `83b60b9de4541a3ffa6ee0db98205a372b525665` | True |
| all-in-one/sources/decoded-original/0656-IdentXmlPart.xml | `0dbc45e84732a8848f17b094ea08ab8578dbf240bfe15cd7086859395c27c592` | `9bfb9842e55901bab9a71d1ac03158467dfbb1bc` | True |
| all-in-one/sources/decoded-original/0657-IdentXmlPart.xml | `0f70cda60a6b1a17175876d58e25b2686952642de6cffb21213aeef8b347a22b` | `e625f3d8999c7be7d88c50eab0d93107117b58ec` | True |
| all-in-one/sources/decoded-original/0658-IdentXmlPart.xml | `998294c0c8a99e00ceb33c2c60def2cd4850e34328917ae506244c2be2df3831` | `de9a12a6be87466ef1bf05df71c54580c556a827` | True |
| all-in-one/sources/decoded-original/0688-IdentXmlPart.xml | `ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda` | `463585759f1ecd94f32362b4fefb000a152f5773` | True |
| all-in-one/sources/decoded-original/0692-IdentXmlPart.xml | `bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037` | `737785d03b5fad43c5b4d451955726d800edb1c0` | True |
| all-in-one/sources/decoded-original/0694-IdentXmlPart.xml | `757ccebdf32d0a168dd787bfa735fe6494eac4c4a9f7a5adc63898a88e8b152d` | `c45e8f3ca4129dc06734f6a12ef79e6ed6528a7d` | True |
