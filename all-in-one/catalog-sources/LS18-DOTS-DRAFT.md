# LS18 독립 원본 조사 초안

- 작성일 2026-10-11 UTC, 조사 시작 13:44 UTC. GME-STD-1.0.0. documentation=complete_with_gaps, 독립 검토 전.
- 읽기 전용 입력 `gme-research/source-mv06`, 고정 commit `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, 프로그램 v1.12.0. PLC는 GME_20250506.zap18 백업 유래 XML이며 현재 CPU와의 일치 미확인.
- 대상은 LS18 하나, 부모 MV02, component/depth1/phase2/planned/baseline, priority_key=null. INVENTORY catalog[229]와 TASK3-BATCH23-SCOPE·GME-CATALOG-OVERLAP-REVIEW의 parent_child_separate 대조. 부모/LS17/ZT03 완료를 상속하지 않는다.
- AGENTS, 저장소 skill, WORK-STANDARD, WORK-ITEM-TEMPLATE, INVENTORY와 최신 인계 상단을 읽었다. 이전 배치 설명의 다른 부모보다 실제 scope의 MV02를 우선한다. 실행 모델·추론 수준의 UI 증명은 미확인이다.
- 변경은 이 MD와 `extracts/LS18/`만. 원본·공통코드·대장·배포·PLC·현장·보호값·SEJIN 운영자료 변경0. 시뮬레이터 작성/수정/생성/실행/행동시험0, 앱 빌드/원본 생성기0, 업로드0, 재위임0.

## 1. 설비·자료 기준 — 적용

**LS18는 문서상 MV02 닫힘측 위치 리미트: E7.4/I7.4 → DB13.DBX7.4.** 그러나 닫힘 명칭을 1=완전 닫힘으로 해석하지 않는다. 처리값은 닫힘 출력에서 정접점, 수동요청 해제와 PID 하한핀에서 반전접점이다. 엔코더는 처리값 대신 원시 I7.4를 반전하여 사용한다.

P&ID `all-in-one/sources/PID_1684n002I.pdf` 실제1쪽과 MV02 확대를 새로 렌더해 MV-02/M16 옆 LS-17·LS-18, 별도 ZT-03, CM-02/ATM 가지를 확인했다. 제목란 도번1684n002, Apex I, 기본일06/04/2011, I행15/01/2013 `REMOVED MC-05, CHANGED POWER OF FN-02`다. P&ID에는 PLC 주소·접점 정상극성·현행 설치 검증이 없다.

OEM `Electrical_Rev2.pdf` FG37/PDF38의 제목 MOTORiZED VALVE MV-02와 LS-18 `LIMIT SWITCH VALVE CLOSING`, FG123/PDF124의 LS-18/E7.4가 직접 대응 근거다. LS17와 ZT03는 별도 부품이며 LS18의 추가 채널/기억값으로 합산하지 않는다. 구동 Q1.6·접촉기·부모알람은 MV02 소유다.

공통구조는 [MV02 초안](MV02-DOTS-DRAFT.md), [LS17 초안](LS17-DOTS-DRAFT.md), [ZT03 초안](ZT03-DOTS-DRAFT.md)을 탐색 색인으로 재사용했다. LS18 고유 선언·접점/핀·원시 입력 엔코더 분기·별도 writer와 실제 PDF4쪽을 직접 대조했다. 부모의 공유 인버터/전체 구동/계측환산/알람을 반복조사하지 않는다. EV69KA/71KA 부하5–9 정정은 보존하며 LS18 회로에 배정하지 않는다.

## 2. IO·HMI·기억값 — 적용 / HMI 결속 일부 미확보

이하 XML은 `all-in-one/sources/decoded-original/` 상대경로. SSD.AO는 비트 오프셋이며 각 문맥의 BAD.BIRID→DepDBBlock TOD.N으로 주소를 결속했다. 다른 블록의 동일 RID를 같은 선언으로 취급하지 않았다.

| 층 | 주소·역할 | 직접 선언/근거와 경계 |
|---|---|---|
| 원시 접점입력 | E7.4/I7.4 Bool | FG37→FG123 CPU515 MOD9 단자35. plc-symbols.csv 693행 `mv02_close,%i7.4,bool,limit switch ls-18`, document1514. CSV는 백업 색인, 현재값 아님 |
| 엔코더에서 원시 읽기 | MV02_Close I7.4 | 0678 SimpleAccess RID444, NID46 UID56, SAD Input, AO60 Bool. DB13과 별도 공간 |
| 원시 word | Tag_171 IW6 | 0627 SimpleAccess RID13, NID1 UID45 Word, SAD Input AO48. I7.4를 포함하는 word |
| 처리 word | DB13.DBW6 | 0629 GlobalAccess RID14 NID1 UID46 AK Write Word AO48/BAD4 + 0628 Inputs RID4 TOD13 |
| 처리 리미트 | Inputs.MV02 Close DB13.DBX7.4 | 0619 RID170 Bool AO60, NID2 UID247/266, BAD168 + 0618 Inputs RID168 TOD13 |
| PID 문맥 | 같은 DB13.DBX7.4 | 0668 RID122 Bool AO60, NID4 UID197/BAD118 + 0666 Inputs RID118 TOD13. RID170과 이름만으로 결속한 것이 아님 |
| HMI 설정 | MV_02\LimitSwitchClose DB11,X20.4, ID001A8 | hmi_plc_tags.csv 433행, Access Name PLC. 원시/처리주소와 다른 위치 |
| 별도 writer | DB13.DBX7.4 Coil367 | 0635 RID235, NID2 UID389 AK Write Bool AO60/BAD5 + 0634 Inputs RID5 TOD13 |
| 수동 요청 | M_MV02_CLOSE DB2.DBX9.5 | 0619 RID18 AO77/BAD5 + 0618 Flag RID5 TOD2. 센서 기억이나 실제 닫힘 증명 아님 |
| 엔코더 gate/기억 | DB91.DBX23.1 / DB8.DBW38 / DB8.DBD4 | 0676 RID222 AO185/BAD177, RID228 AO304/BAD191, RID195 AO32/BAD191 + 0674 TOD91/8. ZT03/MV02 계측 소유이며 LS18 자체 래치 아님 |

LS18 고유 MEM_OPEN/CLOSE, 전용 위치 래치, 독립 고장 선언은 한정 Ident 검색과 관련 네트워크에서 확보되지 않았다. 검색 범위는 decoded-original Ident 파일들의 ID/AO 이름이며 결과는 `LS18-DECLARATION-SEARCH.json`이다. 전체 PLC에 없다는 부재 증명이 아니다.

### HMI 호출의 남은 경계

0366-FlgNet LAD1189 hmi mv02, CRef22/RID639(CodeBlock23/RID130): W57 ORef34/RID694→`Limiti_Switch_Close`, W65 `Limit_Switch_Close_HMI`→ORef42/RID207. 이 핀 철자와 연결은 직접 확인했다. 이 호출의 NID와 RID694/207 동일 문맥 선언을 결속하지 못했으므로 Inputs.MV02 Close→DB11.DBX20.4 완전 연결로 승인하지 않는다. 실제 HMI 객체·이벤트·버튼 쓰기·표시반전·통신품질도 미확인이다.

## 3. 제어 구조 — 적용 / 정적 경로만

### 3.1 원시→처리 word 전송 및 조건부 호출

0397-FlgNet LAD1070 hmi inputs NID1: W21 Powerrail→Move42.en, W52 ORef45/RID13→42.in, W54 42.out1→ORef46/RID14. 위 선언에서 IW6→DB13.DBW6 전송이며 이 Move에 반전은 없다. W53의 42.eno→43.en도 보존한다. LS18 bit는 word에 포함되며 별도의 물리 LS18 쓰기 명령이 아니다.

0030-FlgNet LAD1613 main NID19: CRef25(HMI Output).eno→W42→반전 Contact37.in; W44 ORef45/RID140→37.operand; W43 37.out→CRef28/RID136(CodeBlock29/RID135 HMI Inputs).en. 0692 RID140은 Simulation(1), Memory AO1440=M180.0. 따라서 DB13 갱신을 무조건 수행한다고 쓰지 않는다. 전단 ENO사슬 전체는 LS17/MV02 공통 조사 색인을 유지한다.

### 3.2 처리 Close의 방향출력 정조건과 수동요청 Reset 반전

0343-FlgNet LAD1704 Valve Control loop NID2:

- 정접점354: W305 ORef266/RID170→354.operand; 반전 Open 출력 Contact352.out→W23→354.in; W24 354.out→Coil240.in; W307 ORef267/RID24→240.operand. 0617 RID24 Output AO14=Q1.6 `Close MV02`. **처리 Close는 닫힘 출력 직전 정조건**이며 그 비트만으로 출력이 켜진다는 뜻이 아니다.
- 닫힘 가지 전단: 반전 ON Contact310, 반전 FAULT326, Auto342→PID Down344 또는 ManualClose346의 OR234, PULSE348 또는 ON350의 OR235, 반전 QOpen352를 거친다. 0617 RID26은 PID MV02 Down Memory AO113=M14.1, RID13 PULSE AO80=M10.0, RID1 ON AO0=M0.0. 0619 RID19 Auto AO55/BAD5, RID22 FAULT AO32/BAD10. 식의 범위는 `NOT ON AND NOT FAULT AND ((Auto AND PID_Down) OR ManualClose) AND (PULSE OR ON) AND NOT QOpen AND Inputs.Close`다.
- 수동요청 해제: W276 ORef247/RID170→반전 Contact320.operand; W321 320.out→OR206.in1; OR의 다른 가지는 ManualOpen322와 Auto324; W279 OR206.out→RCoil210.in; W281 ORef250/RID18→210.operand. 전단310/312는 모두 ON 반전이며 W311/313 연결이다. `NOT Inputs.Close`는 Reset 가지 중 하나, 실제 닫힘 완료를 단독 판정하는 래치가 아니다.
- 0032-FlgNet LAD1621 main NID8의 정접점352는 W350 ORef345/RID52 ON→operand, W354 Powerrail→in, W353 out→CRef341/RID86(CodeBlock347/RID85 Valve Control loop FC14). 0692 RID52 M0.0 / 0688 RID85 TOD14. **상위 ON 정조건과 내부 ON 반전이 함께 존재**한다. 현재 다른 호출/스캔 내 쓰기/CPU를 모르므로 정상·동작불가·삭제대상으로 단정하지 않는다.

### 3.3 PID 하한핀은 처리 Close 반전

0476-FlgNet LAD7 cyc_int5 ogni 100ms NID4: W214 ORef197/RID122→Contact251.operand(Negated); W253 Powerrail→251.in; W252 251.out→LRef172.LMNR_LS. 0671 Instruction RID113 CONT_S와 0665 Instance210/RID38 PID_MV-02 TOD23을 결속했다. **LMNR_LS = NOT DB13.DBX7.4**의 정적 핀 연결이다. 센서명 Close, 출력 정조건, PID 반전을 모두 유지한다. 실제 CONT_S 운전/하한 보호/현행 설정은 확인하지 않았다.

### 3.4 원시 I7.4가 별도로 엔코더 gate와 기억 0쓰기에 참여

0513-FlgNet LAD1763, Analog input conversion NID46에서:

- W53 Powerrail→Contact21; W54 ORef32/RID173 EM_OK(I19.4)→21.operand. W55 21.out→Contact22.in 및 Contact27.in, CRef30.en.
- W33 ORef56/RID444 **원시 I7.4**→Contact22.operand(Negated). W57 22.out→Coil23.in 및 Add24.en. W58 ORef34/RID222→Coil23.operand는 fill_unit1.SW_GATE1 DB91.DBX23.1. 정적 gate 식은 EM_OK AND NOT I7.4다. 여기 입력을 DB13.Close로 치환하면 잘못이다.
- W69 ORef43/RID222→Contact27.operand(Negated), W70 27.out→Move28/29.en. W71 ORef44/RID44(Int0)→28.in, W72 28.out1→ORef45/RID228(DB8.DBW38). W73 ORef46/RID327(Int0)→29.in, W74 29.out1→ORef47/RID195(DB8.DBD4). 0675 RID44/327 NID46 UID44/46의 상수0을 직접 확인했다.
- 따라서 EM_OK 조건하의 `NOT SW_GATE1` 가지는 엔코더 기억/처리값 0쓰기다. 접점입력이 실제 닫힘임이 증명되지 않은 상태에서 'LS18 작동=교정완료'라 쓰지 않는다. DB8 엔코더 기억은 LS18 전용 기억이 아니다. 전체 카운트/환산/다른 기억 writer와 상위 FC3 호출은 ZT03 공통 색인을 유지하며 이번에 반복검토하지 않았다.

### 3.5 중지 블록의 보존 XML에 처리값 별도 writer

0403-FlgNet LAD1083 simulation NID2는 **보존 원문 읽기만 수행**했다. 생성/편집/실행/행동시험하지 않았다.

W21 Powerrail→Gt366.pre; W82 ORef84/RID301→366.in1, W83 ORef85/RID254→366.in2; W81 366.out→Coil367.in; W420 ORef389/RID235→367.operand. 0635 RID301 Data.Pot_MV02 Int AO1136/BAD247 + 0634 Data RID247 TOD1=DB1.DBW142; 0637 RID254 NID2 UID85 Int V2. 위 RID235는 DB13.DBX7.4다. 저장 XML에는 **Pot_MV02 > 2의 결과를 처리 Close에 쓰는 경로**가 존재한다. 원시 I7.4의 정상극성이나 현재값을 뜻하지 않는다. 제목만으로 현재 활성/비활성을 단정하지 않으며 전체 호출·최종 writer·우선순위는 미확인이다.

## 4. 전기 전달 양 끝점 — 적용

| 경로 | 실제 렌더에서 확인한 끝점/참조 | 페이지별 개정·경계 |
|---|---|---|
| 공급→접점 | FG37/PDF38 +24Vdc10.7 접속점→X1:83, 5×20 2A F 표기→도선37.6→LS-18 접점11–12 | MOTORiZED VALVE MV-02, 기본27.05.2024, 별도 Rev행 없음. 도면퓨즈 표기를 현행설정/교체지시로 해석 안 함 |
| 접점→DI | LS18 12측→X1:84→E7.4 하향123/5. FG123/PDF124 E7.4 상향37/7→CPU515 MOD9 단자35, LIMIT SWITCH LS-18 | FG123 DIGITAL INPUT MODULE 기본27.05.2024, **Rev2 17.03.2025**. 양쪽 좌표는 각 페이지의 참조위치이며 동일 숫자로 고치지 않음 |
| 모듈 공급 | FG123 +24Vdc10.7→X21:3009 5×20 2A IST→123.1→단자39; -0Vdc10.6→단자40 | 현장 센서 공급 X1:83과 모듈공급 X21:3009를 합치지 않음 |
| 인접 부품 | LS17 X1:81/82 E7.3, ZT03 X1:76~80 | LS18의 추가 입력이나 엔코더 전원으로 재배정 안 함 |

접점 기호와 11/12를 판독했으나 정지/개방/폐쇄시 실제 접점상태, 캠·설치방향, 단선 거동·정상극성은 미확인이다. 공급10.7 전체 발생원은 부모 공통 근거를 유지한다. 이 끝점 대조는 문서 연결이며 실측 도통·전압 검증이 아니다.

시공참고 `Electrical_Can_Decoating_20241118.pdf` 실제57/64쪽 CABLE SCHEDULE(6), D-PAGE7, DWG CANDC-CONS-C007-057, Rev1 24.11.11 first draft design:

- 행7_12 `=FLA+MV02-LS18A`: FROM HE-01/FLO2TB1 → TO MV-02/LS-18, DC, CVV 2C 1.0, spare0, route LAD1 E300→LAD1→E600, Adjustment12/LEN12.
- 행7_1 `=FLA+HE01-FLO2TB1A`: CR→HE-01/FLO2TB1, LS17/18/23/24/21A/22A/21B/22B 묶음, DC CVV25G1.0 spare8, LEN50.

OEM X1:83/84와 시공참고의 코어별 승인 대응표는 확보되지 않았다. 길이·케이블 사양은 참고 설계 표기로만 보존하고 준공/실물/SEJIN 운영기록으로 승격하지 않는다.

## 5. 알람·복구 — 일부 근거 미확보

LS18 전용 고장비트·타이머·ACK/Reset 루프는 이번 고유 검색과 관련 네트워크에서 확보하지 못했다. 부모 FAULT, 접촉기 명령불일치의 Tag93 T21 S5T#150MS, ±1000 방향명령 누적은 MV02 초안 공통 색인이다. 이번에 부모 전체 알람을 다시 의미검토하지 않았고 LS18 독립 알람으로 복제하지 않는다.

원시 LS18는 엔코더 gate, 처리 LS18는 방향출력·수동요청 Reset·PID 하한에 연결된다. 이것만으로 단선진단/안전정지 보장/자동 복구를 주장하지 않는다. 원인 제거, 원시/처리갱신, HMI 회복, 부모알람 해제, 재요청, 실제 위치 일치는 각각 별도 증거다. 강제출력·보호우회·설정변경·현장복구는 수행하지 않았다.

## 6. 증상별 관찰 — 적용, 현장 실행 지시 아님

| 증상 | 같은 시각에 비교할 승인된 관찰자료 | 분리할 원인/필요 자료 |
|---|---|---|
| 닫힘 표시와 실물 불일치 | 실제 위치·LS18 접점·I7.4·DB13.DBX7.4·DB11.DBX20.4·CPU/시각 | 설치극성/배선/word갱신/별도writer/HMI 미결속. 승인 접점표·단자사진 |
| 닫힘 명령이 안 나옴 | ON·FAULT·Auto/PIDDown/ManualClose·PULSE·QOpen·처리 Close·Q1.6 | 정접점354 이전조건과 호출모순경계. 현재 프로젝트 교차참조 |
| 수동 닫힘 요청 소실 | DB2.DBX9.5·처리 Close·ManualOpen·Auto·ON | RCoil210 OR206·반전320·다른 요청 writer. 실물 완료로 단정 안 함 |
| PID 하한상태 예상과 다름 | DB13.DBX7.4·DB23 LMNR_LS·실제위치·ZT03 위치 | 반전251과 인스턴스/호출·현행보호설정. 설정 조정 안 함 |
| 엔코더값이 0 또는 gate 변동 | I7.4·I19.4·DB91.DBX23.1·DB8.DBW38/DBD4·DB13.Close | 원시 직접분기와 처리분기 분리. 0513 0쓰기·ZT03의 다른writer·순서 검토 |
| 원시/처리값 불일치 | I7.4/IW6·DB13W6/X7.4·M180.0·DB1.DBW142 | 0397 조건부 갱신과0403 보존 writer. 중지자산 실행으로 검증하지 않음 |

관찰 기록에는 관찰자·시각/시간대·관찰점·값/단위·수집장치·CPU/프로젝트·자료판본·원인배제·승인조치·전후변화·복구증거가 필요하다. 실제 운영기록 또는 합성 QA값은 만들지 않았다.

## 7. 완료·누락·검증 — 적용

남은 자료: LS18 현행 명판/접점표/설치·캠·단자 양끝사진, 승인 결선/케이블 코어표, 현재 CPU 프로젝트 전체 호출/쓰기 교차참조, HMI 실제 객체/이벤트 및 선언결속, 승인된 동시각 관찰/복구기록. 새 자료 없이는 실물 보류를 반복조사하지 않는다.

- 정적 의미검토는 8네트워크 0030/0032/0343/0366/0397/0403/0476/0513의 위에 명시한 부분과 선언이다. 8개 전체 회로 해석이나 전체 PLC 의미검토가 아니다.
- 실제 원본 PDF4쪽: 전기38/124, P&ID1, 시공57. P&ID 확대2개는 같은 쪽의 보조 렌더이며 페이지수에 중복 합산하지 않는다.
- 읽기 전용 preflight exit0, inventory_matches=true. source_byte_changes는 requirements-audit/all-in-one-data 두 파일이며 현재 고정commit과 바이트가 일치한다. 예전 대장 snapshot 기준차이를 이번 원본수정으로 보지 않는다.
- 선정전체 SHA256/Gitblob/고정바이트 표는 부록A, 검사JSON은 `extracts/LS18/SOURCE-SHA256.json`과 `VALIDATION.json`. 해시검사 파일수·XML 구조단언수·의미검토 범위는 서로 다른 집계다.

| 기능/상태 | 결과 |
|---|---|
| 도면·래더 비교 | FG37/123↔0397/0343/0476/0513 준비. UI 통합·강조시험 안 함 |
| 백업·선택복원 | 안정ID LS18, note/repair_observation/미지필드·초안·저장키·타설비 변경0. 기능시험 안 함 |
| 기록 전후비교 | 관찰틀만. 실제 운영·합성QA 생성0 |
| 보고서/PDF | MD/원본렌더만. 제품 보고서/A4 기능 미검증 |
| documentation | complete_with_gaps, 독립검토 전 |
| static_review | partial_original_checked, 자체 정적검사 |
| ui_records / publication | not_run / not_published |
| tia_compile / live_cpu / field_recovery | 모두 not_performed |

다음 한 작업: 부모의 LS18 독립검토. 기존 MV02·LS17·ZT03 초안은 수정하지 않았다.

## 부록 A. 선정 원본 전체 SHA256 / Git blob

고정commit 상대경로다. 중지5자산은 보존해시만 검사했으며 실행/수정/생성하지 않았다. 해시는 백업 동일성이고 현장 동일성 증거가 아니다.

선정 56파일 전체 고정바이트 일치, 자체 정적단언 22개 통과. 의미검토8네트워크 부분/실제PDF4쪽과 다른 집계다.

| 원본 상대경로 | SHA256 | Git blob | 고정바이트 |
|---|---|---|---|
| `.agents/skills/gme-equipment-rollout/SKILL.md` | `fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b` | `9aa820ea6ca15b4e136c9772423b78ed4df6a3d4` | 일치 |
| `.agents/skills/gme-equipment-rollout/references/source-map.md` | `40612c5efb8f94608840c7bc0e9095ea840df54920861c388ae48ea34c7998dc` | `49e50a7a8e56a16e2ec7f3607a03fd90adb8f1d3` | 일치 |
| `.agents/skills/gme-equipment-rollout/scripts/preflight.py` | `395067d6da20af3e1d82a43b7936907a87a44d8d2e11e4ebc61b1fc441e2adb6` | `170679427250c36c3a68cf6c5c2291ffe0341b10` | 일치 |
| `AGENTS.md` | `0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2` | `073164bc6efd5791032d62c71b03b4dab48cb6f8` | 일치 |
| `EXPANSION-WORK.md` | `ec624de9fd2fcfac861a67fd5e828b25ef46db50bfd7a37ff16e2cb54cd0f7e2` | `4c42d88ecc2d48269eb23e13a20ebf3721a092a1` | 일치 |
| `PUBLICATION_STATUS.md` | `efe4857aec598d90470322cf3962eb3fe1f64947630e1fdf71d1c90134de8740` | `d76401cf291fc0be681acc51fa898ad3ce46ff78` | 일치 |
| `VERSION.json` | `5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7` | `fffb51663b7705aec91cb119ca80ee943a4ce758` | 일치 |
| `WORKSPACE-HANDOFF.md` | `215096d997782e78e901dfae36c782937e49611fbeb677a0d3fa50cbecf8d074` | `dd0b8989d2376c4415bba9bd826fe6754c6b1a12` | 일치 |
| `all-in-one/ACTIVE-WORK.md` | `eff3bbc08ecff41da3beff77f3fec48e7d148708192bcaaab00f34b6a721afc2` | `6eb947c629b5ddf9c759ef87649451303938864b` | 일치 |
| `all-in-one/assets/program-model-data.js` | `52f8199371e3399b7c0d44ab5469f0472aced79d56bbef2887f7625f5d2aff0f` | `38f34b0caa380a16ccad6f6f1e234a2fdf23f327` | 일치 |
| `all-in-one/assets/simulator-workspace.js` | `3a6dfc618ff7e7b238f2671dc85d65704f33093a18eac879d86081d92c31e8bc` | `97c2c831c77a9699fff0e0960b3bc1b7d93d45b3` | 일치 |
| `all-in-one/assets/virtual-plc.js` | `5f1876052dc0067b1f010af0dfc941946e37003167481731293615d9c1c36dbc` | `0bd9eceb54365a91214a37c5601b5067c39a3f75` | 일치 |
| `all-in-one/registers/all-in-one-data.json` | `63a46b36b6454bf1246d093300dbee11f2fcc287ad94991405369bf9f939a8fe` | `15d62ac2a99c1c0eeb7579e03163f9c0319b50a4` | 일치 |
| `all-in-one/registers/equipment.json` | `7870325dff32bbca90fa34507b301c4aad3347d669fddcd03b910343663996fa` | `acc42633033398216469064932c4b76987371606` | 일치 |
| `all-in-one/registers/plc-symbols.csv` | `a0334b390f06ddb515d6c09ca96a01d35d44029c1b726ef0ff53303ec04ff91f` | `cbc576c5d6e47498a3865304a1c23de9b4641d9f` | 일치 |
| `all-in-one/registers/priority-equipment.csv` | `953c2c4df5b3a6e40d926d1f0f08f91900b7d6565e4dcd64191b548e438edeba` | `69c17fe3eb671e896ad15914c81fae7f307aebdf` | 일치 |
| `all-in-one/registers/program-model.json` | `6203479c086b15bada12ac9d7e37db9280234ec26f1ea6091d7211dc09a577c5` | `9860b10f008d3a5ae714be50d77b703dfec32f3a` | 일치 |
| `all-in-one/registers/requirements-audit.json` | `a10b773ff96e9b1c7a27cf409644c68d3eb59aedc5bcb5ca00199d602e63facb` | `69e45bb8fe1abbcd2ba4eeb65e2f4445a367e238` | 일치 |
| `all-in-one/registers/simulator-freeze.json` | `bb93c1994effc5609939ba566b7802ce7ed55154a7310f02379b308ac2c8c835` | `808ffac14dbd1b4a7d797fa6cd0d647635d90b47` | 일치 |
| `all-in-one/registers/virtual-plc-test-results.json` | `a6b389f797f9a8b5ffe6928b8420f55c4cc459a327b0b48d716079d2eca6dd64` | `757dd50e45184568facb8ff62900b39d3ce848d1` | 일치 |
| `all-in-one/sources/Electrical_Can_Decoating_20241118.pdf` | `3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd` | `0ee6b6f8361c5790864dbba4bbd9d55e8e7c08f8` | 일치 |
| `all-in-one/sources/Electrical_Rev2.pdf` | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` | `f610fd7c7ce14ae951b00cff57b969259bfb389d` | 일치 |
| `all-in-one/sources/PID_1684n002I.pdf` | `2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b` | `8c83a59fefd5b8b651ec3537ea4236a073f5e109` | 일치 |
| `all-in-one/sources/decoded-original/0030-FlgNet.xml` | `9252c9da764993de1edb8b2e44c46d6e9f9d4b6118e751a0dbeaa9ffd8ea721b` | `e74c70b751acdcdbc7a8b3b0c98aa773c2107cab` | 일치 |
| `all-in-one/sources/decoded-original/0032-FlgNet.xml` | `070bb8efa33d03b18add5da81d3f670a47c12b288076b7bfee11ac87fe6fa7e4` | `e31cf9aeecfbfc0c264921ac217cbd15479c1f34` | 일치 |
| `all-in-one/sources/decoded-original/0343-FlgNet.xml` | `a2f41d7cce7c4d944f0cebdcacc964a1298962198a20f9471558902b39685d68` | `a882a5b83ff68c500114dd48e15397a35ee8c454` | 일치 |
| `all-in-one/sources/decoded-original/0366-FlgNet.xml` | `79ce47fc6656105cefa0ee138a30e85283bc9d481d432ca720fdca0668dda7e2` | `3e50c5bc6b7a1a0b83a3e8660a8b8aa3cbd9661f` | 일치 |
| `all-in-one/sources/decoded-original/0397-FlgNet.xml` | `bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834` | `4ab8370493c4e28fc1eabeeebe2743d27f0c4021` | 일치 |
| `all-in-one/sources/decoded-original/0403-FlgNet.xml` | `77b03e38aa857ac8dd404f2f66a56256939b4e7924b41334a7981b86089c1e6b` | `4c806e31eb65f00cbb7870c72896ac26a8bc3dd3` | 일치 |
| `all-in-one/sources/decoded-original/0476-FlgNet.xml` | `0f9c48dddf61987d61094de9368ab534b56ec6c30e898dc2e4d81b64e86fa55a` | `6201c68a4d81417c8aa970bdcc7de6dea3899260` | 일치 |
| `all-in-one/sources/decoded-original/0513-FlgNet.xml` | `19107ffbb3144f4dc5dd070f0edb459166ae7a96c0715b65362f9a359c19412d` | `42f9e21fdcc81ed3664bb2c5421a3b7f6108f89f` | 일치 |
| `all-in-one/sources/decoded-original/0617-IdentXmlPart.xml` | `10bcf85169cb2512f55acadaef299a3d46b4b4cecd88032d739cfeba23e94aa9` | `9527658ee6808be34bd513b1b2ebaf3a4a5a6f3e` | 일치 |
| `all-in-one/sources/decoded-original/0618-IdentXmlPart.xml` | `0c6762de9cdf0e294317f7463bea3d8e6df5673d333d9b1826ebd17a7ded044c` | `9eec0dbd8abde4aa7295f77b63ad473f895f274b` | 일치 |
| `all-in-one/sources/decoded-original/0619-IdentXmlPart.xml` | `85694bb5b696e31e6a1217431112e5b750516c4f94078d6e127d4394a8b80456` | `11f0502c84a1f319a21459a35c0dc1c6ce8e8f36` | 일치 |
| `all-in-one/sources/decoded-original/0627-IdentXmlPart.xml` | `08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb` | `61ebc0abbb2ca160e11e1da400a3f14a397d8bc5` | 일치 |
| `all-in-one/sources/decoded-original/0628-IdentXmlPart.xml` | `9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd` | `170ca5c72599edc7ea7eefe651c3680ce325e76a` | 일치 |
| `all-in-one/sources/decoded-original/0629-IdentXmlPart.xml` | `67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972` | `058129bb01e27f7a6a0d0293f332d745e5bab74e` | 일치 |
| `all-in-one/sources/decoded-original/0634-IdentXmlPart.xml` | `af3fcb536a6270ffb9a19e5b3f2c284a38d67d465f5147961005c1c01d11299d` | `877d9e0734dc7f3e5a8cea789eeb58a208501f48` | 일치 |
| `all-in-one/sources/decoded-original/0635-IdentXmlPart.xml` | `1a057d686446a3fdab7ac61bb09bc543c52f49646c9ca71ac323c10fcdffe457` | `95bfcad59cfb0c12b573e9e8face4262d1e94622` | 일치 |
| `all-in-one/sources/decoded-original/0637-IdentXmlPart.xml` | `3fb68f57dbe2a877c4ad5aa1b3316810cf84958f2d13b5b1d7d321e0915271c7` | `cb1d7fb76aa2afd96eb46984cc1e71b77f36395c` | 일치 |
| `all-in-one/sources/decoded-original/0665-IdentXmlPart.xml` | `50e88d5f50f555151b35cfb17225e766c34ef6b490bd3a48e0a4e335fd17e3dd` | `ea4a8a5013081f648722c5ebbde3bb1366787990` | 일치 |
| `all-in-one/sources/decoded-original/0666-IdentXmlPart.xml` | `19a9ccb83ad7070d23726250870d0ca0c33d797ab9ffe679c9d2c0d109cc95e6` | `b6130b32498b6fee0d9e4db7a04dc79f785e1fbb` | 일치 |
| `all-in-one/sources/decoded-original/0668-IdentXmlPart.xml` | `2248e994a0a02cd37c5c5edaca199b3421068feea91e2e8616560e814ef9f6ed` | `fe0f30d1eaae37783b0f03cb090353b3a3de3600` | 일치 |
| `all-in-one/sources/decoded-original/0671-IdentXmlPart.xml` | `26cb51706305c372d512c19770648bb0dbb74df8bd2277b1e0da1b8c88cca293` | `e38a4e2c93ac8093e2b0b8e082a64688b5d9845e` | 일치 |
| `all-in-one/sources/decoded-original/0674-IdentXmlPart.xml` | `4770702f519bacda69202bb2f7733d983074bda90964360c238f990d9d08fd84` | `f210593944547b63eab10c667348711413600aab` | 일치 |
| `all-in-one/sources/decoded-original/0675-IdentXmlPart.xml` | `b1902886927d8403fab736d9c8ffe73f2fbc8ce4b7ca7c345144964668b051c3` | `d82a33b173c8dc0737fd890eb2a63a88a07d0831` | 일치 |
| `all-in-one/sources/decoded-original/0676-IdentXmlPart.xml` | `c58427c5b0ac6c11cdb52e4c6d0461c7b191fae81ccace191048e9f175fcec59` | `1ed67265f69796a4e659f9438e551068037f33a4` | 일치 |
| `all-in-one/sources/decoded-original/0678-IdentXmlPart.xml` | `51e637e0b9713c028810f2a717b5c3804a3a26c2f1be7e332a4d6bf277bfc382` | `7fafb2297bcdf739bf1d1dd68cebc0d74f2a40cc` | 일치 |
| `all-in-one/sources/decoded-original/0688-IdentXmlPart.xml` | `ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda` | `463585759f1ecd94f32362b4fefb000a152f5773` | 일치 |
| `all-in-one/sources/decoded-original/0692-IdentXmlPart.xml` | `bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037` | `737785d03b5fad43c5b4d451955726d800edb1c0` | 일치 |
| `all-in-one/sources/decoded-original/network-map.json` | `c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60` | `424430b6b953e43138e5d0a18ca40c949e21cfa1` | 일치 |
| `all-in-one/sources/hmi_plc_tags.csv` | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` | `cf4c0650e7c7baac350dcb89909b808435704880` | 일치 |
| `docs/equipment-standard/INVENTORY.json` | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` | `587c3748ad9224718f95ba06463fee913dae231d` | 일치 |
| `docs/equipment-standard/START-GPT61.md` | `35769e3146ccd707fea2b81b67b30376b76a0a19c7e662fe2bb4fdd382306f94` | `0d08cab3678df7e2625251b641b138ef4956483b` | 일치 |
| `docs/equipment-standard/WORK-ITEM-TEMPLATE.md` | `4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586` | `e546f39535d2b589e80f97db869ac37ce4d05cfd` | 일치 |
| `docs/equipment-standard/WORK-STANDARD.md` | `05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99` | `f76a570cc73098632e08759b17934000f7e3a253` | 일치 |
