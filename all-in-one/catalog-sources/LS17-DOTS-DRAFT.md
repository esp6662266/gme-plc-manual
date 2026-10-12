# LS17 독립 원본 조사 초안

- 작성: 2026-10-11 UTC · GME-STD-1.0.0 · documentation=complete_with_gaps, 독립 검토 전 초안.
- 고정 읽기 전용 원본: `source-mv06`, commit `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, v1.12.0. PLC 백업 GME_20250506.zap18에서 추출된 XML이며 현재 CPU와 일치 여부는 미확인.
- 대상 LS17 하나. 부모 MV02, 하위 구성품, depth1, phase2, priority_key=null, baseline, parent_child_separate. `INVENTORY.json#/catalog/228`과 TASK3-BATCH22-SCOPE/중복검토의 LS17행을 대조했다. MV02·LS18·ZT03 완료를 상속하거나 합산하지 않는다.
- 원본 AGENTS·저장소 skill·WORK-STANDARD·WORK-ITEM-TEMPLATE·최신 인계 상단을 읽었다. 이전 PV/실린더 관련 배치 문구보다 실제 scope의 MV02 부모를 우선했다. 모델/추론 UI 설정은 관측하지 못했으므로 미확인.
- 변경은 이 MD와 `extracts/LS17/`만. 원본·공통코드·대장·배포·PLC·현장·보호값·SEJIN 운영자료 변경0. 시뮬레이터 작성·수정·생성·실행·행동시험0, 앱 빌드/원본 생성기0, 업로드0, 재위임0.

## 1. 설비·자료 기준 — 적용

핵심 결론은 **LS17=MV02 개방측 리미트의 문서상 대응, E7.3/I7.3 → DB13.DBX7.3**다. ‘개방’이라는 명칭을 곧바로 1=완전 개방으로 바꾸지 않는다. 동작식에서는 같은 처리비트가 정접점과 반전접점 양쪽으로 쓰인다.

P&ID `sources/PID_1684n002I.pdf` 실제1쪽의 MV-02 분기 확대에서 M16, LS-17, LS-18, ZT-03을 시각 확인했다. MV02는 HE01 부근에서 CM02/ATM 방향으로 향하는 가지에 있다. LS17/18 타원은 M16 옆 두 위치 리미트이고 ZT03는 별도 엔코더다. 제목란 1684n002, Apex I, 기본일 06/04/2011, 최신 표시행 I 15/01/2013(REMOVED MC-05, CHANGED POWER OF FN-02)을 확인했다. P&ID 자체만으로 각 LS의 PLC 주소나 정상극성을 정하지 않는다.

직접 전기 근거는 `Electrical_Rev2.pdf` FG37/PDF38의 MOTORiZED VALVE MV-02와 LIMIT SWITCH VALVE OPEN의 LS-17, FG123/PDF124의 LS-17/E7.3다. 부모 공통 구동·인버터·알람은 MV02 초안, 엔코더 전원/카운트는 ZT03 초안을 탐색색인으로 재사용하고 이번 LS17 조사에서 전체를 복제하지 않는다. EV69KA/71KA 부하5–9 정정은 유지하며 본 LS 회로에 관계없는 릴레이를 추가하지 않는다.

## 2. I/O·HMI·기억값 — 적용 / HMI 결속 일부 미확보

| 층 | 주소·정체 | 직접 근거와 경계 |
|---|---|---|
| 실물 원시 입력 | E7.3/I7.3, Bool | FG37 LS17→FG123 CPU515 MOD9 단자34. `registers/plc-symbols.csv` document659 `mv02_open,%i7.3,bool,limit switch ls-17`. 심볼 CSV는 백업 색인이고 실물 현재값 아님 |
| 원시 word | IW6, Tag_171 | `0627-IdentXmlPart.xml` SimpleAccess RID13, NID1 UID45, Word, SAD Input, SSD AO48. I7.3은 이 word의 포함 비트 |
| 처리 word | DB13.DBW6 | `0629` GlobalAccess RID14, NID1 UID46 AK Write, Word AO48/BAD BIRID4 + `0628` DepDBBlock RID4 Inputs TOD N13 |
| 처리 리미트 | Inputs.MV02 Open, DB13.DBX7.3 | `0619` GlobalAccess RID169 Bool AO59, NID2 UID243/258, BAD168 + `0618` DepDBBlock RID168 Inputs TOD N13. 원시 I7.3과 별도 저장위치 |
| PID 문맥의 같은 처리값 | DB13.DBX7.3 | `0668` RID121 Bool AO59, NID4 UID196/BAD118 + `0666` Inputs RID118/TOD N13. 다른 문맥 RID169와 동일 RID라고 연결하지 않음 |
| HMI 설정 | MV_02\LimitSwitchOpen = DB11,X20.3, ID001A9 | `sources/hmi_plc_tags.csv` Access Name PLC. 원시/처리값과 다른 주소. 버튼/화면 이벤트·현재 태그 사용·통신성공은 CSV로 입증 못 함 |
| 다른 writer | DB13.DBX7.3에 Coil | `0635` RID237 AO59/NID2 UID386 AK Write + `0634` Inputs RID5/TOD N13; §3.4 참조 |

LS17 고유 위치기억 Set/Reset 태그나 전용 래치 선언은 이번 한정 원본 검색에서 확보되지 않았다. DB13는 처리 메모리이며 PV계 MEM_OPEN/CLOSE나 ZT03의 DB8 엔코더 기억을 LS17 고유 기억값으로 복제하지 않는다. ‘기억값이 전혀 없다’는 전체 PLC 부재 주장도 하지 않는다.

### HMI 호출 경계

`0366-FlgNet.xml` LAD1189 hmi mv02에는 CRef22/RID639, CodeBlock23/RID130, W56 ORef33/RID695→Limit_switch_Open, W64 Limit_Switch_Open_HMI→ORef41/RID206이 있다. 원본 핀 자체를 확인했으나 이 호출의 NID 및 RID695/206의 동일 문맥 선언 결속을 확보하지 못했다. 따라서 Inputs.MV02 Open→DB11.DBX20.3 완전 연결로 승인하지 않는다. 부모 초안의 HMI 미결속을 유지했다. HMI 이름/검색순서만으로 직접 배선을 보완하지 않는다.

## 3. 제어 — 적용 / 정적 경로 한정

### 3.1 원시 입력 전달과 호출

`0397-FlgNet.xml` LAD1070, hmi inputs NID1: Powerrail W21→Move42.en, W52 ORef45/RID13→Move42.in, W54 Move42.out1→ORef46/RID14. 위 선언으로 **IW6→DB13.DBW6**를 직접 대조했다. 이 Move에는 반전이 없고 다음 Move43.en은 Move42.eno의 W53에 연결된다. 원시 bit 포함관계와 PLC word 전송을 구분한다.

`0030-FlgNet.xml` LAD1613 main NID19: CRef25(HMI Output).eno→W42→Contact37.in; Contact37은 Negated operand, W44 ORef45/RID140; W43→CRef28(HMI Inputs).en. `0692` RID140은 Simulation(1), Memory AO1440=M180.0이다. 따라서 호출조건이 있고 DB13 갱신을 무조건 실행으로 설명하지 않는다. Recipes Handler→HMI→HMI Output ENO 사슬은 부모 공통 근거로 유지한다.

### 3.2 MV02 방향제어에서 LS17의 서로 다른 극성

`0343-FlgNet.xml` LAD1704, Valve Control loop NID2:

- **정접점**: ORef258/RID169→W293→Contact340.operand. NOT 반대방향 출력의 Contact338.out→W21→Contact340.in; Contact340.out→W22→Coil227.in; Coil227 operand는 W295/ORef259/RID25. `0617` RID25 Output AO13이므로 Q1.5 Open MV02다. 즉 DB13.DBX7.3은 개방출력의 마지막 직렬 조건이다. 이 조건 하나만으로 출력이 켜지는 것은 아니다.
- **반전접점**: ORef243/RID169→W270→Contact314.operand(Negated). Contact314.out→W315→OR199.in1→W273→RCoil203.in, W275 ORef246/RID20 operand. `0619` RID20 AO78/BAD5 + `0618` Flag DB2로 M_MV02_OPEN=DB2.DBX9.6이다. 반전 LS 조건은 수동 요청 해제 OR의 한 가지이며 MC 또는 Auto 가지도 있다.
- 원문 공통 조건: 310/312는 ON의 반전접점이다. 정리된 개방 식은 NOT ON AND NOT FAULT AND ((Auto AND PID_UP) OR ManualOpen) AND (PULSE OR ON) AND NOT QClose AND Inputs.MV02 Open. LS17 영향만 분리할 때 다른 조건을 삭제해 ‘LS17이면 개방’으로 쓰지 않는다.
- `0032-FlgNet.xml` LAD1621 main NID8는 ON 정접점352: W350 ORef345/RID52→operand, W354 Powerrail→in, W353 out→CRef341.en. `0692` RID52 Memory AO0, `0688` RID85 FC Valve Control loop/TOD14를 확인했다. 이 호출 정조건과 내부 ON 반전은 원문 경계다. 현재 CPU·다른 호출·스캔 중 쓰기를 모르므로 동작불가/정상/삭제대상으로 단정하지 않는다.

### 3.3 PID 상한 입력

`0476-FlgNet.xml` LAD7, cyc_int5 ogni 100ms NID4: ORef196/RID121→W213→Contact249.operand(Negated), W253 Powerrail→249.in, W250 249.out→LRef172.LMNR_HS. `0671` Instruction RID113 CONT_S, `0665` Instance210/RID38 PID_MV-02 TOD DB23. 따라서 **LMNR_HS = NOT Inputs.MV02 Open**의 정적 연결이다. 개방 명칭, 방향출력 정조건, PID 반전 상한핀을 모두 유지한다. CONT_S의 현재 동작·안전 상한·현행 보호값을 이 연결만으로 정하지 않는다.

### 3.4 보존 XML의 별도 쓰기 — 실행 금지

중지 simulation 블록의 보존 원문 `0403-FlgNet.xml` LAD1083, NID2에서 LS17 처리비트 writer만 정적으로 읽었다. 재생성·편집·실행·행동시험은 하지 않았다.

- W21 Powerrail→Lt364.pre; W87 ORef89/RID301→in1, W88 ORef90/RID253→in2.
- `0635` RID301 Data.Pot_MV02 Int AO1136/BAD247 + `0634` Data RID247 TOD N1 = DB1.DBW142. `0637` LiteralConstant RID253 NID2 UID90, Int V98.
- Lt364.out→W86→Coil365.in; Coil365.operand←W416/ORef386/RID237 = DB13.DBX7.3.
- 보존 XML상 조건은 Pot_MV02 < 98이다. 이는 실물 LS17 원시입력의 극성이나 현재 LS 상태가 아니다. 제목으로 현재 비활성/활성을 판정하지 않으며 전체 호출·우선순위 미확정으로 둔다. 부모의 위치word 복수writer와도 별도 층이다.

## 4. 전기 전달 끝점 — 적용

직접 PDF4쪽을 새로 렌더하고 P&ID 영역/표제를 확대했다. FG와 1-based 실제 PDF쪽을 구분했다.

| 경로 | 직접 판독 | 개정·경계 |
|---|---|---|
| 공급→센서 | FG37/PDF38 +24Vdc10.7 수평선의 접속점→X1:81, 5×20 2A F 퓨즈 표기→도선37.5→LS17 접점11–12 | MOTORiZED VALVE MV-02, 기본27.05.2024, 개별 Rev행 없음. 2A는 도면표기이며 현행설정/교체권고 아님 |
| 센서→PLC | LS17 12측→X1:82→E7.3 하향참조123/4; FG123/PDF124 E7.3 상향참조37/5→CPU515 MOD9 단자34, 설명 LIMIT SWITCH LS-17 | FG123 DIGITAL INPUT MODULE, Rev2 17.03.2025/기본27.05.2024. 서로 다른 쪽의 참조좌표 보존 |
| 모듈 공급 | FG123 +24Vdc10.7→X21:3009, 5×20 2A IST→123.1→단자39; -0Vdc10.6→단자40 | LS17 현장 직렬 퓨즈 X1:81과 모듈 공급 X21:3009를 같은 것으로 합치지 않음 |
| 인접 구분 | LS18은 별도 X1:83/84와E7.4, ZT03는 X1:76~80 | LS17의 추가 채널·기억·실물 소유로 계산하지 않음 |

LS17 접점11–12의 그림과 정/반전 사용은 확보했지만 정지/개방/폐쇄 시 실제 접점 상태·센서 설치방향·캠·단선 거동·전기 정상극성은 미확인이다. 공급10.7의 발생원 전체를 이번에 반복 추적하지 않았다. 끝점 확인은 센서와 DI 단자 양끝 문서 범위이며 실측 도통/전압 검증이 아니다.

시공 참고 `Electrical_Can_Decoating_20241118.pdf` 실제57/64쪽, 표제 CABLE SCHEDULE(6), D-PAGE7, DWG CANDC-CONS-C007-057, Rev1 24.11.11 first draft design:

- 행7_11 `=FLA+MV02-LS17A`: FROM HE-01/FLO2TB1→TO MV-02/LS-17, DC, CVV, 2C, 1.0, spare0, route LAD1 E300→LAD1→E500, Adjustment12, LEN12.
- 행7_1 `=FLA+HE01-FLO2TB1A`: FROM CR→HE-01/FLO2TB1, LS17/18/23/24/21A/22A/21B/22B 공통 묶음, DC CVV25G1.0 spare8, LEN50.

이 표는 중간 단자함/케이블 경로 참고이며 OEM X1:81/82와의 승인된 코어별 대응표는 없다. 케이블 사양/길이를 실물 실측·준공으로 확정하지 않고 SEJIN 운영자료를 복제하거나 통합하지 않는다.

## 5. 알람·복구 — 일부 근거 미확보

LS17 전용 고장비트·전용 타이머·ACK/Reset 루프는 이번 고유 이름/주소 선언 검색과 관련 7네트워크에서 확보하지 못했다. 부모 MV02의 FAULT, 접촉기 명령불일치와 Tag93 T21의 S5T#150MS, 방향명령 누적±1000은 부모 초안 공통 색인에 남기며 LS17 독립알람으로 복제하지 않는다. 이번에 그 부모 전체 알람 논리를 다시 의미검토한 것은 아니다.

LS17는 출력의 허가조건, 수동요청 해제조건, PID 상한핀에 영향을 주는 자료상 연결이다. 이 사실만으로 LS17 단선진단/안전정지 보장/자동 복구를 주장하지 않는다. 원인 제거, 처리값 재갱신, HMI 표시회복, 부모알람 해제, 정상 재요청 후 실제 위치 일치는 각각 다른 증거가 필요하다. 현장 복구·강제출력·보호우회·설정조정은 수행하지 않았다.

## 6. 증상별 관찰 — 적용, 실행 지시 아님

| 증상 | 같은시각에 비교할 승인된 관찰자료 | 분리할 원인/필요 증거 |
|---|---|---|
| 열림 표시가 실제와 다름 | 실제 기계위치, LS17 접점상태, I7.3, DB13.DBX7.3, DB11.DBX20.3, 관찰시간 | 실물 극성·배선·원시갱신·별도writer·HMI 결속을 분리. 명판/캠 위치/승인접점표 필요 |
| 개방 명령이 나오지 않음 | LS17 처리값, ON, FAULT, Auto/PID_UP/ManualOpen, PULSE, QClose, Q1.5 | 정접점340뿐 아니라 호출 및 전단조건을 비교. 현재CPU 교차참조/승인 관찰 필요 |
| 수동 개방 요청이 사라짐 | DB2.DBX9.6, DB13.DBX7.3, MC/Auto, ON과 스캔시간 | RCoil203 OR199/반전314와다른writer를 구분. 실물 리미트 작동으로 단정하지 않음 |
| PID 상한 상태가 예상과 다름 | DB13.DBX7.3, DB23 LMNR_HS, 실제 MV02 위치, ZT03 표시 | W250 반전과 현재인스턴스/호출, 엔코더 별도계를 비교. 보호값 조정 금지 |
| 원시와처리값 불일치 | I7.3/IW6, DB13.DBW6/DBX7.3, M180.0, DB1.DBW142와 같은시각/CPU식별 | 0397 호출,0403 보존writer, 전체교차참조를 정적으로 대조. 중지 자산 실행으로 검증하지 않음 |

관찰자는 실제 시각/시간대·관찰점·값·단위·수집장치·CPU/프로젝트 식별·원본판본·원인배제·승인조치·전후변화·복구증거를 남겨야 한다. 이 문서에는 합성값이나 실제 운영기록을 만들지 않았다.

## 7. 완료·누락·검증

남은자료: 현행 LS17 명판/접점표/설치위치·캠/양끝 단자사진, 승인 결선도와 코어별 케이블표, 현재CPU 프로젝트·전체교차참조/호출·쓰기순서·보존 속성, HMI 실제 객체/이벤트와 RID 결속, 승인된 동시각 관찰/복구기록. 새자료가 없으면 보류를 반복 재조사하지 않는다.

- 정적 의미검토: 관련7네트워크(0030,0032,0343,0366,0397,0403,0476)의 본문에 열거한 부분과 선언. 7전체 네트워크의 모든 회로를 완전히 해석했다는 뜻이 아니다. 전체 Ident 검색은 후보발견이지 전부 의미검토가 아니다.
- 실제PDF 검토: 원본4쪽(전기38/124, P&ID1, 시공57) 및 P&ID 두 확대. 접점/접속점/끝점/페이지별개정 확인. 제품 보고서 PDF/UI 시험과 다르다.
- 읽기전용 preflight exit0, inventory_matches=true. source_byte_changes는 requirements-audit/all-in-one-data 두 파일로 보고되며 현재 고정 커밋 바이트와일치한다. 대장 snapshot의 예전 바이트기준 차이를이번변경으로 해석하지 않는다.
- 선정전체 SHA256/Gitblob/고정 커밋 byte검사와 XML 구조 단언은 `extracts/LS17/VALIDATION.json`, `SOURCE-SHA256.json`. 해시 검사수와 의미검토수를 구별한다.

| 기능/상태 | 결과 |
|---|---|
| 도면·래더 비교 | FG37/123↔0397/0343/0476 근거 준비; UI통합/강조시험 안 함 |
| 백업·선택복원 | 안정ID LS17, note/repair_observation/미지필드·초안·저장키/타설비 변경0; 기능 시험 안 함 |
| 기록 전후비교 | 관찰틀만 준비, 실제 운영기록/합성QA생성0 |
| 보고서/PDF | MD/원본렌더만. 제품 A4/보고서 기능 미검증 |
| documentation | complete_with_gaps, 독립검토 전 |
| static_review | partial_original_checked, 자체 정적검사만 |
| ui_records / publication | not_run / not_published |
| tia_compile / live_cpu / field_recovery | 모두 not_performed |

다음 한 작업: 부모의 LS17 독립검토. 부모/엔코더 기존 초안은 수정하지 않았다.

## 부록 A. 선정 원본 전체 SHA256 / Git blob

고정 커밋 상대경로. 중지5자산은 보존 해시만 계산했고 실행·생성·수정하지 않았다. 해시는 문서/백업 동일성을 확인하며 현장 동일성을 증명하지 않는다.

선정 49파일 전체 고정바이트 일치, 자체 정적단언 15개 통과. 의미검토7네트워크 부분/실제PDF4쪽과 다른 집계다.

| 원본 상대경로 | SHA256 | Git blob | 고정바이트 |
|---|---|---|---|
| `.agents/skills/gme-equipment-rollout/SKILL.md` | `fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b` | `9aa820ea6ca15b4e136c9772423b78ed4df6a3d4` | 일치 |
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
| `all-in-one/sources/decoded-original/0688-IdentXmlPart.xml` | `ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda` | `463585759f1ecd94f32362b4fefb000a152f5773` | 일치 |
| `all-in-one/sources/decoded-original/0692-IdentXmlPart.xml` | `bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037` | `737785d03b5fad43c5b4d451955726d800edb1c0` | 일치 |
| `all-in-one/sources/decoded-original/network-map.json` | `c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60` | `424430b6b953e43138e5d0a18ca40c949e21cfa1` | 일치 |
| `all-in-one/sources/hmi_plc_tags.csv` | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` | `cf4c0650e7c7baac350dcb89909b808435704880` | 일치 |
| `docs/equipment-standard/INVENTORY.json` | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` | `587c3748ad9224718f95ba06463fee913dae231d` | 일치 |
| `docs/equipment-standard/WORK-ITEM-TEMPLATE.md` | `4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586` | `e546f39535d2b589e80f97db869ac37ce4d05cfd` | 일치 |
| `docs/equipment-standard/WORK-STANDARD.md` | `05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99` | `f76a570cc73098632e08759b17934000f7e3a253` | 일치 |
