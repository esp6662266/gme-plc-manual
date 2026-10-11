# PSL05 압축공기 저압 스위치 — 원본 조사 초안

## 핵심 확인·상충·인계

- 고유 PSL05는 OEM FG76/실제 PDF77의 압축공기 접점 계기다. +24Vdc → X1:184(5×20, 2A F) → 선76.2 → PSL-05 접점11/12 → X1:185 → E11.0 → FG127/PDF128 MOD10 단자31 경로를 직접 렌더 확인했다. 제조사·현재 정상극성·실물 배선·현행 보호값은 미확정이다.
- `%IW10 → DB13.DBW10` Word 복사 안의 I11.0/DB13.DBX11.0이 관련 입력이다. 이름상 저압이라는 이유로 입력1=저압으로 해석하지 않는다. 원본 알람은 **ON AND NOT 입력**에서 DB3.DBX5.4 Set이다.
- Reset은 **ON AND RESET_ALLARM AND 기존알람 AND 입력**이다. 타이머는 해당 0160 네트워크에 없다. 원인 제거·안전확인·재기동은 별도이며 현장 Reset을 수행하지 않았다.
- 직접 하류 소유는 `0175`의 `Flag.Start_Burner` Reset 가지다. PSL05를 게이트 명령의 직접 차단 소유자로 바꾸거나 게이트/버너 전체 안전순서를 설명하지 않는다.
- 상충: live_index `_7ev/i945` Address는 `%i11.0`이나 Comment는 `e 41.4 psl-05 ...`; `_7ev/i1227` 제목은 `psl-04 low air pressure`다. 주소·선언·도면 결속과 낡은 주석/제목을 구별하고 원본을 수정하지 않았다.
- 다른 Writer: DB13 입력 Word 복사 외에 기존 백업의 0415/NID18에 DB13.X11.0 개별 bit 쓰기가 존재한다. 정적 문서 확인만 했으며 시뮬레이터 작성·수정·생성·실행·행동시험은 하지 않았다. 현재 모드/호출/최종값 미확정이다.
- 독립 고유검토: 0160 알람 S/R, 0175 버너 요청Reset, 0397의 IW10 Word, 0573/0585/0627~0629 선언, OEM 두 쪽 실제 렌더. 공유근거: BF01의 공통 Word 경보·startup/Reset과 LD01의 입력전달/호출 설명은 인덱스로만 이용하고 해당 PSL05 bit 구간을 원본에서 따로 대조했다. 79개 선택 근거의 고정 Git blob 내용일치를 확인했다. 해시 수는 의미검토 수가 아니다.
- 남은 자료: 현행 스위치 명판·제조사 매뉴얼·설정/히스테리시스 승인자료, 준공 단자/케이블표, 현재 CPU 교차참조/호출·HMI 이벤트, 실제 압력과 전기신호의 동시 관찰. 새 자료 없는 현장 보류를 반복 조사하지 않는다.

## 작업 기준

GME-STD-1.0.0. 고정 원본 `gme-research/source-mv06`, `abcf31c5030bc7ef8749ed8e869a857f2387a28a` / v1.12.0. catalog PSL05, sensor/계측, parent 없음, depth0, phase2, priority 없음. INVENTORY catalog[7], 배정 scope equipment_index108, 별칭 low pressure air/psl-05. 신규132 자체조사 한 대상이며 로컬2차133 통합 제외 유지. 다른 계기·게이트·BR01을 함께 완료 집계하지 않는다.

AGENTS, 저장소 스킬, WORK-STANDARD, WORK-ITEM-TEMPLATE, INVENTORY, VERSION, WORKSPACE-HANDOFF, PUBLICATION_STATUS, ACTIVE-WORK/EXPANSION-WORK 최신 항목, START-GPT61 및 source-map 관련 범위를 읽었다. 배정의 문서전용 제한이 우선이며 원본 preflight/build/test/generator는 실행하지 않았다. 모델/추론수준 런타임 증명 미확인. TIA 추가접근권한 없음.

쓰기 범위는 `drafts/PSL05-DOTS-DRAFT.md`, `extracts/PSL05/`뿐이다. 원본·코드·버전·대장·운영기록·배포·SEJIN 수정 없음. PLC/현장/보호값 변경과 동작시험 없음. 재위임·새 Work/Codex 생성 없음. 아래 축약 XML 경로는 고정 원본 `all-in-one/sources/decoded-original/`이다.

| 7영역 | 상태 | 확보/누락 |
|---|---|---|
| 설비·자료 기준 | 적용 | 고유 ID·도면/백업 시점; 현재 실물 동일성 미확정 |
| I/O·HMI | 적용/일부 미확보 | Word/bit·알람주소·HMI 태그; 이벤트·현재값 미확정 |
| 제어 구조 | 적용/일부 미확보 | S/R·버너 요청·호출·다른 Writer; 실제 스캔/직접 게이트 영향 미확정 |
| 전기 끝점 | 적용/일부 미확보 | X1·접점·E11.0·MOD10; 실제 케이블/모델/극성 미확정 |
| 알람·복구 | 적용/일부 미확보 | 저압 S/R·공통 경보·초기화; 현장 복구 없음 |
| 증상 관찰 | 적용 | 비교 위치·판정 경계; 실제 측정/정비 없음 |
| 완료·누락 | 적용 | 문서·정적·UI/게시/TIA/CPU/현장 분리 |

## 1. 설비·자료 기준

OEM 자료명 `Electrical_Rev2.pdf`; FG76/PDF77은 PSL-05 LOW AIR PRESSURE SWITCH와 옆 PC-01 PRESSURE CONTROL을 서로 다른 회로로 표시한다. PC01의 4–20mA, ±200mbar, 50mA F, PEW322/76SCH1은 PSL05 규격이나 신호가 아니다. PSL05에는 압력 숫자 설정이 그려져 있지 않다.

실제 렌더 두 장의 footer를 각각 판독했다. FG76/PDF77: DATA27.05.2024, DISENG.G.G., NORMA IEC, TOT262, 제목 PRESSURE CONTROL, 별도 개정 기록 미관찰. FG127/PDF128: DATA27.05.2024, DISENG.G.G., IEC, TOT262, DIGITAL INPUT MODULE, 별도 개정 기록 미관찰. PDF 파일 이름 Rev2만으로 모든 개별 페이지가 Rev2 개정됐다고 쓰지 않는다. 이 자료는 현행 준공 일치의 증명이 아니다.

시공 PDF 전체 텍스트에서 PSL05/PSL-05/PSL 05 문자열을 찾지 못했다. P&ID 텍스트 추출에서도 PSL 관련 문자열을 찾지 못했으나 이는 이미지/비텍스트 기호 부재의 증명이 아니다. 이 두 자료의 PSL05 시각적 실물 대응은 확보하지 못했고 다른 계기의 시공 케이블을 전용해 채우지 않았다.

## 2. I/O·HMI

| 신호 | 형식·주소 | 원본 선언/결속 | 해석·미확정 |
|---|---|---|---|
| Tag_182 | Global Word Input %IW10, SAM=None | 0627 RID17 SSD.AO80, NID1 UID49 | 프로세스 이미지 Word; PIW/Peripherie와 혼동 금지 |
| 입력 Word 목적지 | Global Word DB13.DBW10 | 0629 RID18 SSD.AO80 BAD4→0628 Inputs TOD13, NID1 UID50 Write | I11.0을 포함하는 16비트 복사; 개별 PSL05 코일 아님 |
| Inputs.Low Pressure Air | Global Bool DB13.DBX11.0 | 0573 RID71 AO88 BAD58→0572 Inputs TOD13; NID2 UID270/274 Read | 처리/미러 입력, 물리 극성 보증 아님 |
| Allarm.PSL_AIR_LOW | Global Bool DB3.DBX5.4 | 0573 RID40 AO44 BAD10→0572 Allarm TOD3; NID2 UID271 S/273 Read/275 R | 유지 알람 bit |
| ON | Global Bool M0.0 | 0570 RID1 AO0 SAD.Memory, NID2 UID269 | 명칭만으로 상시 TRUE 단정 금지 |
| Flag.RESET_ALLARM | Global Bool DB2.DBX6.0 | 0573 RID38 AO48 BAD37→0572 Flag TOD2, UID272 | 공통 Reset 요청; 재기동 아님 |
| Flag.Start_Burner | Global Bool DB2.DBX5.2 | 0585 RID19 AO42 BAD7→0584 Flag TOD2, NID5 UID250 Write | 버너 요청 메모리; 물리 밸브 출력 아님 |
| 다른 입력 Writer | Global Bool DB13.DBX11.0 | 0635 RID350 AO88 BAD5→0634 Inputs TOD13, NID18 UID34 Write | 기존 백업의 별도 bit 쓰기, 현재 활성 미확정 |

### 2.1 원시 Word 전달

0397/LAD1070, HMI Inputs NID1: ORef49/RID17 → W58 → Move44.in; Move44.out1 → W59 → ORef50/RID18. Move43.eno→Move44.en은 W56이고 선행 Move42.eno→Move43.en은 W53이다. Move42의 en은 rail W21이다. 모두 DisableENO=true 표기를 보존하며 ENO 핀을 데이터 out1과 바꾸지 않는다. 앞 두 Move와 성공/실제 실행상태까지 추정하지 않는다.

이 경로는 입력 Word 전체의 복사다. I11.0이 포함되어 DB13.X11.0으로 대응하는 근거이지 별도의 직접 물리 Bool 선언이 이 네트워크에 있다는 뜻은 아니다. physical tag live_index i945의 Address `%i11.0` 및 OEM E11.0과 대조했다. 주석 `e41.4`와는 상충 상태를 유지한다.

### 2.2 HMI 주소 설정

`sources/hmi_plc_tags.csv` 실제 행502: `Allarmi_45`, `DB3,X5.4`, Access Name PLC, 내부ID00160. PSL 저압 유지 알람 주소와 일치한다. 행103 `BR_01\Flag`, `DB2,X5.2`, 내부ID00386은 버너 요청 주소의 HMI 설정이며 PSL05 전용 제어태그가 아니다. 태그 CSV에는 PSL 이름 기반 전용 입력 표시를 찾지 못했다. 주소 설정은 HMI 경보 문구·확인/소거 이벤트·통신권한·현재값·실제 화면 재현의 증명이 아니다.

## 3. 제어 구조·직접 소유

### 3.1 저압 감지와 유지

0160/LAD1227, allarms2 NID2의 직접 핀:

- rail W296→Contact286.in; ORef269 ON→W276→operand. Contact286.out W287은 Set와 Reset 가지를 함께 공급한다.
- ORef270 입력→W277→Contact288.operand는 Negated다. Contact288.out→W289→SCoil262.in, SCoil262.operand W279→ORef271 알람.
- Reset 가지: ORef272 RESET→W280→Contact290.operand, 290.out W291→Contact292.in. ORef273 기존알람→W281→292.operand. 292.out W293→Contact294.in, ORef274 입력→W282→294.operand. 294.out W295→RCoil268.in, operand W284→ORef275 알람.

식: Set = ON AND NOT DB13.X11.0. Reset = ON AND RESET_ALLARM AND DB3.X5.4 AND DB13.X11.0. 물리 스위치가 정상 압력에서 어떤 접점 상태가 되는지, 압력이 얼마에서 전환되는지 이 식만으로 확정하지 않는다. 이 네트워크에는 TON/S5 타이머·환산·데드밴드 계산이 없다. 압력복귀만으로 유지알람을 자동해제하는 식도 아니다.

### 3.2 BR01 요청 Reset 영향

0175/LAD1858, burner control NID5: 0585 RID42=Allarm.PSL_AIR_LOW, ORef247→W265→Contact301.operand; ON Contact273의 out W274가 Contact301.in을 공급한다. 301.out→W302→OR219.in10. OR219는 12분기이며 out W267→Contact305.in, ORef249=0582 RID1 ON→W268→305.operand, 305.out W306→OR213.in5. OR213의 out W270→RCoil232.in, operand W272→ORef250=Flag.Start_Burner.

따라서 PSL 알람이 이 버너 요청Reset OR분기에 참여한다. 다른 분기는 FN03·온도·산소·흡인·외부 연소상태 등의 각 소유이다. 이 가지 하나로 버너 외부 제어기의 가스밸브/화염/퍼지/안전시퀀스나 게이트 모든 명령을 직접 소유한다고 확대하지 않는다. 자동 식별 결과의 UID249에는 다른 블록 Data도 충돌 후보로 나타났지만 0582/0585의 burner-control 선언 그룹과 ON 재참조로 수동 판별했다.

### 3.3 호출·다른 Writer·초기화

- 0031/LAD1619 NID6의 ON Contact282.out W283은 CRef267(Allarms2 FC5, CodeBlock277/RID61, 0688/0694).en을 다른 호출들과 병렬로 공급한다. 직렬 ENO 호출이 아니다.
- 0030 NID19: Recipes Handler CRef21.eno W32→HMI CRef23.en; HMI.eno W33→HMI Output CRef25.en; 25.eno W42→NOT Contact37.in; ORef45=0692 RID140 Simulation(1), Bool M180.0, W44→37.operand; 37.out W43→HMI Inputs FC15 CRef28.en(CodeBlock29/RID135). 입력복사의 호출 조건·선행 ENO를 누락하지 않는다.
- 기존 백업 0415/LAD1080 NID18은 ON Contact23.out W29→Coil33.in, ORef34/RID350 W25→Coil33.operand로 같은 DB13.X11.0에 쓴다. 이는 숨은 Writer 존재의 문서적 확인이다. 해당 기존 로직·실행환경을 수정/작성/실행하지 않았고 현재 활성·스캔최종값은 미확정이다.
- startup only 0148/LAD403 원본 선언 NID3: 0048 RID54 Int0 ORef289→W310→Move256.in; Move256.out1 W311→ORef290/0563 RID28 Word AO32 BAD23→0562 Allarm DB3. 즉 DB3.DBW4←0에 알람 X5.4가 포함된다. 앞 Move253.eno W309→256.en; 이 Writer는 평상시 전용 RCoil과 다른 startup Word 초기화다. 파생 network-map NID=null을 원본 NID3 대신 쓰지 않는다.
- 명명된 PSL 알람 사용은 0573/0585와 위 Word 범위를 확인했다. 전체 선언 텍스트 검색은 간접 포인터·블록복사·통신·현재 CPU의 모든 Writer를 배제하는 증명이 아니다. 게이트 직접 인터록/단독 안전기능은 확보하지 못했다.

## 4. 전기 끝점

| 실제 렌더 | 전달 구간 | 판독 및 미확정 |
|---|---|---|
| FG76/PDF77 | +24Vdc10.7, 75/9→77/0 수평전원 → X1:184 → 선76.2 | 5×20 2A F는 도면 표기이며 현행 퓨즈를 확인/변경한 것이 아님 |
| FG76/PDF77 | PSL-05 압력기호 p< 및 접점11/12 → X1:185 → E11.0 → 127/2 | 접점 번호와 심볼은 판독; 현재 NO/NC·정상압력극성·실제 결선 미확정 |
| FG127/PDF128 | 상호참조76/4 → E11.0 → 단자31, CPU515/MOD10 | 디지털 입력 채널 표기; 현재 CPU 모델/모듈 주문번호가 확인된 것은 아님 |
| FG127/PDF128 | +24Vdc10.7 → X21:3011 5×20 2A IST. → 선127.1 → 단자39; −0Vdc10.6→단자40 | 모듈 공급과 신호단자31 구별 |

전기 도면상 위 경로에 중간 출력 릴레이나 구동부하 접점은 없다. 릴레이 5/9 관례나 다른 게이트 EV 회로를 추가하지 않는다. 스위치 현장 케이블 ID·길이·심색·정션박스·모델·설정/복귀압력·배관 탭 위치는 이 두 페이지에서 미확정이다. 자료의 전원/퓨즈값을 현장 작업지시로 사용하지 않는다.

## 5. 알람·공통 경보·복구 경계

저압 bit는 DB3.X5.4이고 공통 Word DB3.W4 범위에 속한다. BF01에서 검토된 공통 논리를 공유하되 PSL 구간을 독립 결속했다.

- 0151/LAD927 NID1: 0565 RID15 ORef177 DB3.W4→W198→Move137.in, out1 W199→ORef178/RID16 WorkData.W2(DB6.W4, Int). 0564의 Allarm TOD3/WorkData TOD6를 대조했다. EN은 RESET_ALLARM/RUN_HORN/STOP_HORN의 OR121.out W212이다.
- 0152/LAD928 NID2: ORef224 DB3.W4 W246→Ne197.in1; ORef225 WorkData.W2 W247→Ne197.in2; out W248→OR190.in3. 전체 Word변화 OR190.out W267→NOT STOP_HORN Contact271→W272→Coil219 NEW_ALLARM. 복사와 비교는 알람 bit 자체를 Reset하는 행위가 아니다.
- 0153/LAD929 NID3: NEW_ALLARM Contact219→NOT RESET_ALLARM221→NOT STOP_HORN223, W224에서 RUN_HORN Set204와 NEW_ALLARM Reset206을 분기한다. 출력경적 실물/스피커/이벤트로그는 미확인이다.
- 0158/LAD930 NID9: Inputs.Reset_allarmi Contact23 또는 Flag.Reset_Allarms_HMI Contact26→OR28.out W38→SCoil33 RESET_ALLARM 및 RCoil40 Reset_Allarms_HMI. 이것은 공통 요청 경로다. 승인된 실제 버튼/화면·주소 동작은 아직 확인하지 않았다.

운영 복구 판정에는 승인된 정상압력 확보, 실제 압력과 스위치/단자/I11.0/DB13.X11.0의 동시 확인, 알람 원인 배제, 승인된 Reset 후 DB3.X5.4/HMI/경보의 확인, 별도 버너 요청/허가/응답 확인이 필요하다. 이를 이 문서에서 수행·완료했다고 표시하지 않는다. 압력 공급 정상, 알람 소거, 버너 재요청, 실제 운전복귀는 각각 다른 사실이다.

## 6. 증상별 관찰 준비

아래는 읽기 전용 증거 수집 항목이다. 강제입출력·보호값 변경·우회·운전시험·압력스위치 조정 지시가 아니다. 전기·공압 접근은 현장 안전절차/격리/담당자 승인 이후 수행해야 한다.

| 증상 | 같은 시각의 관찰 | 비교/원인 구분 | 완료에 필요한 추가 증거 |
|---|---|---|---|
| 압력은 있어 보이나 저압알람 유지 | 승인 계측압력·스위치 상태·X1:184/185·I11.0·DB13.X11.0·DB3.X5.4 | 압력 표시만으로 스위치/배선 정상 단정 금지; 입력 복귀와 Reset 별개 | 명판·설정/히스테리시스·교정·동시측정 |
| I11.0과 처리 bit 불일치 | IW10/DB13W10·호출조건 M180.0·다른 Writer·시각 | Word복사 호출/ENO와 개별 bit쓰기 구별 | 현재 프로젝트 교차참조/스캔관찰 |
| 입력 복귀했지만 알람 안 꺼짐 | ON·Reset요청·알람·입력 및 호출시각 | 4개 Reset 조건을 구별; 실제 압력안전은 별도 | 승인된 Reset 기록/이벤트 |
| 버너 요청이 꺼짐 | PSL bit·Start_Burner·기타 0175 OR조건 | PSL은 다수 Reset원인 중 하나; 출력/화염과 다른 계층 | 현재 BR01 요청/허가/응답 로그 |
| 게이트가 움직이지 않음 | 관련 게이트 원시위치/요청/EV·실제 공급압력 | 공압부족 가능성과 PLC 직접인터록을 구별 | 해당 게이트 독립 제어·배선·공압 자료 |
| HMI와 PLC 알람이 다름 | Allarmi_45 DB3X5.4·통신시각·화면 경보ID | 태그주소 설정과 이벤트/ACK는 별도 | 현행 HMI 경보표/통신/화면 관찰 |

관찰 기록 필수: 관찰자, 실제 시각/시간대, 위치, 값/단위, 장치/프로젝트 근거, 비교 원본 판본, 배제 결과, 승인 조치, 복구 증거. 운영 기록/사진을 이 공개 조사자료에 복제하지 않았다.

## 7. 완료·누락·검증

문서 조사 범위는 complete_with_gaps, 원본 핵심 정적 검토는 완료했으나 부모의 독립 재검토는 별도다. UI/기록저장/재열기/선택복원/보고서·PDF 기능, 게시, TIA 컴파일, 현재CPU, 실물/현장복구는 not_performed다. BC01 동등 기능 표준화 또는 통합 완료로 표시하지 않는다.

네 기능: 도면·래더 병렬비교는 원본 좌표를 확보했지만 앱 기능 검증 미수행; 백업·선택복원, 전후기록 비교, 관찰 보고서/PDF는 대상 기능지원·보존 검증 미수행. 기존 note/repair_observation·미지필드·초안·다른설비 저장키는 건드리지 않았다. 이 MD와 PDF원본 렌더는 관찰보고서 기능의 실행증거가 아니다.

검사: 자체 XML 파싱/선언·핀·Wire 추출, 입력과 알람 Word구간 확인, HMI CSV 2행, OEM 실제 2페이지/footer 판독, 선택79파일 SHA256/고정 Git blob 내용일치, Git 상태 확인. 원본730파일 전체 또는 과거90개 모든 의미검토를 했다는 주장은 하지 않는다. 자동 추출은 NID/RID/UID 충돌 후보를 유지하며 핵심은 수동으로 블록/선언그룹 결속했다. source-hashes.json와 static-review.json 및 추출물은 extracts/PSL05에 있다.

다음 한 작업: 부모가 입력Word 전체쓰기/다른Writer와 0160 S/R·0175 요청Reset 경로 및 FG76/127 양끝점을 독립 검토하고 초안을 전달한다. 현행 확인은 위 누락자료 확보 후 승인 범위에서 별도로 진행한다.

### 실제 작업 단계 시각(UTC)

| 시각 | 실제 수행 단계 |
|---|---|
| 2026-10-11 10:40:03 | 배정 수신·공통 지시/범위 읽기 시작 |
| 10:40:14~10:40:32 | 표준·스킬·기준 상태/기존초안 인덱스 및 선언 검색 |
| 10:40:41~10:41:17 | 고유 선언/네트워크 추출·알람/버너/입력 Word 원본 검토 |
| 10:41:26~10:41:36 | OEM PDF77/128 렌더 및 시각/개정란 판독 |
| 10:41:43 | 부모에게 고유핵심 중간보고 |
| 10:41:52~10:42:23 | HMI·주석상충·공통경보/startup/다른Writer 독립 결속 |
| 10:42:48 | 선택79파일 고정 Git blob 내용/SHA256 일치 검사 완료 |
| 10:42:57 | P&ID/시공 문자열 미검출 한계·호출/Writer 확인 |
| 2026-10-11T10:46:08.940242+00:00 | 초안 작성 후 SHA/blob 재검사·Git상태 확인·검사JSON 작성 |

## 부록 A. 선택 원본 전체 해시표

79개 모두 고정 Git blob과 바이트 내용 일치. 중지5자산은 보존 확인용 해시만 읽었고 실행하지 않았다. 각 파일별 git_blob_sha256은 아래 SHA256과 같으며 JSON에도 전부 보관한다. 이는 전체 프로그램 의미검토 목록이 아니다.

| 원본 경로(저장소 기준) | SHA256 | 고정 Git blob OID | 일치 |
|---|---|---|---|
| .agents/skills/gme-equipment-rollout/SKILL.md | fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b | 9aa820ea6ca15b4e136c9772423b78ed4df6a3d4 | true |
| .agents/skills/gme-equipment-rollout/references/source-map.md | 40612c5efb8f94608840c7bc0e9095ea840df54920861c388ae48ea34c7998dc | 49e50a7a8e56a16e2ec7f3607a03fd90adb8f1d3 | true |
| AGENTS.md | 0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2 | 073164bc6efd5791032d62c71b03b4dab48cb6f8 | true |
| EXPANSION-WORK.md | ec624de9fd2fcfac861a67fd5e828b25ef46db50bfd7a37ff16e2cb54cd0f7e2 | 4c42d88ecc2d48269eb23e13a20ebf3721a092a1 | true |
| PUBLICATION_STATUS.md | efe4857aec598d90470322cf3962eb3fe1f64947630e1fdf71d1c90134de8740 | d76401cf291fc0be681acc51fa898ad3ce46ff78 | true |
| VERSION.json | 5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7 | fffb51663b7705aec91cb119ca80ee943a4ce758 | true |
| WORKSPACE-HANDOFF.md | 215096d997782e78e901dfae36c782937e49611fbeb677a0d3fa50cbecf8d074 | dd0b8989d2376c4415bba9bd826fe6754c6b1a12 | true |
| all-in-one/ACTIVE-WORK.md | eff3bbc08ecff41da3beff77f3fec48e7d148708192bcaaab00f34b6a721afc2 | 6eb947c629b5ddf9c759ef87649451303938864b | true |
| all-in-one/assets/program-model-data.js | 52f8199371e3399b7c0d44ab5469f0472aced79d56bbef2887f7625f5d2aff0f | 38f34b0caa380a16ccad6f6f1e234a2fdf23f327 | true |
| all-in-one/assets/simulator-workspace.js | 3a6dfc618ff7e7b238f2671dc85d65704f33093a18eac879d86081d92c31e8bc | 97c2c831c77a9699fff0e0960b3bc1b7d93d45b3 | true |
| all-in-one/assets/virtual-plc.js | 5f1876052dc0067b1f010af0dfc941946e37003167481731293615d9c1c36dbc | 0bd9eceb54365a91214a37c5601b5067c39a3f75 | true |
| all-in-one/registers/program-model.json | 6203479c086b15bada12ac9d7e37db9280234ec26f1ea6091d7211dc09a577c5 | 9860b10f008d3a5ae714be50d77b703dfec32f3a | true |
| all-in-one/registers/simulator-freeze.json | bb93c1994effc5609939ba566b7802ce7ed55154a7310f02379b308ac2c8c835 | 808ffac14dbd1b4a7d797fa6cd0d647635d90b47 | true |
| all-in-one/registers/virtual-plc-test-results.json | a6b389f797f9a8b5ffe6928b8420f55c4cc459a327b0b48d716079d2eca6dd64 | 757dd50e45184568facb8ff62900b39d3ce848d1 | true |
| all-in-one/sources/Electrical_Can_Decoating_20241118.pdf | 3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd | 0ee6b6f8361c5790864dbba4bbd9d55e8e7c08f8 | true |
| all-in-one/sources/Electrical_Rev2.pdf | 5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6 | f610fd7c7ce14ae951b00cff57b969259bfb389d | true |
| all-in-one/sources/GME_20250506.zap18 | 00c79b6d986e68298f65b172c1807115bc5d9e450a74fcc989d0796d8d8a4ea8 | 211c4f604627a32f82a1124c2a9872c2fcf00865 | true |
| all-in-one/sources/PEData.plf | 647de7ea123daced41c27bec8f81aeb93c712cac714d4754d7da5c528abb016a | 65605ff8910f920109da731604aa5dc8d83fc956 | true |
| all-in-one/sources/PID_1684n002I.pdf | 2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b | 8c83a59fefd5b8b651ec3537ea4236a073f5e109 | true |
| all-in-one/sources/decoded-original/0030-FlgNet.xml | 9252c9da764993de1edb8b2e44c46d6e9f9d4b6118e751a0dbeaa9ffd8ea721b | e74c70b751acdcdbc7a8b3b0c98aa773c2107cab | true |
| all-in-one/sources/decoded-original/0031-FlgNet.xml | 76385eab8f8f72b9faa16f7cf8905f395591b18c0a9ee9e6d7dd085a38c45c65 | 653d27572de6beedcf3eb6c95702bb119a8b567f | true |
| all-in-one/sources/decoded-original/0033-FlgNet.xml | e7fc5601889297a84fcc6b5601a3e0acba420b9c9adb8b37c60277a0fb5cb108 | b8a89efcb38999950739e0462830d03a94d57c08 | true |
| all-in-one/sources/decoded-original/0047-IdentXmlPart.xml | 2e53bb895dd1ad2a74efaeb1ef16dfd61e62b1b2d7aa34cec8612f1b9cb0928e | 3dc282f149a21fdf76d5521ef1c833be63b578b4 | true |
| all-in-one/sources/decoded-original/0048-IdentXmlPart.xml | d8e8687de7271bd294c2b62b33d789700af9d5014d82b130141988c4d479253d | 64fc5a7f1ad33f3b901b00f0d22d23578ffabff8 | true |
| all-in-one/sources/decoded-original/0148-FlgNet.xml | 1d80e1bbf1c82dcc4dd18628c35935bbd55a17b5be9c1ca7bfb249600d154313 | 3069ae3b5fa16ed10a64c149b6cf5cb5ace423b3 | true |
| all-in-one/sources/decoded-original/0151-FlgNet.xml | 227627d165c6240a4c15b62fd4e4c8d7a621c15f35319cb424601df5cc52c904 | 8e8a9801d1f57180fc3747f6515c0353f38f7dc5 | true |
| all-in-one/sources/decoded-original/0152-FlgNet.xml | 2b6165460f06a52de56afcb4d65ed163d64320e24af1b194e934a4d7c6bfe49f | dd8e35b98043d9d0f230351352273eac1d783990 | true |
| all-in-one/sources/decoded-original/0153-FlgNet.xml | 3d3a236a66a7a5c9b8e2d1e15da63cc943ba5cd266949583cbac6ffbb2f88bc6 | d50223c45f5eb1d1c1d3530b41db1e79ad6c71f3 | true |
| all-in-one/sources/decoded-original/0158-FlgNet.xml | d3f3adebc3d990b85c5d4c294906ae3bc3dafebb49d25b030bf9cc2ccf905651 | 233ccf8f9d82ffffa498e04cbdcd3de07115c1db | true |
| all-in-one/sources/decoded-original/0160-FlgNet.xml | b8c51aaea425c5c696a1d2f2a84985c32c21a46394a238f901c248193a5f83db | 7cacd4467070d286f4e22a2b8bff0fcb636274ed | true |
| all-in-one/sources/decoded-original/0175-FlgNet.xml | 41279d6aaa157de3be963d010d6ca7dea94811a0ace519c8a3d8baa015f67f97 | 1626da00b3bbcb46f77720271ecf0f50db9dc63b | true |
| all-in-one/sources/decoded-original/0200-FlgNet.xml | 2bd1be34eb905a10d840c59aeb461464a1af418fa0ea3f2b8d0b3f88145eb27e | 31eb4f3df5596c004278ef7b3ccf158ae3878079 | true |
| all-in-one/sources/decoded-original/0219-FlgNet.xml | 245409937abf7e28f25a24d4a6d311a801a4b2ee7293148be9b3d266352eb53a | d1c9ae9d9fe8a5a1ed605d09a3f9bd26c5632d0a | true |
| all-in-one/sources/decoded-original/0397-FlgNet.xml | bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834 | 4ab8370493c4e28fc1eabeeebe2743d27f0c4021 | true |
| all-in-one/sources/decoded-original/0415-FlgNet.xml | 7690a90cbad58f5e8474c94efc4a105e80522fb57e3516a720aab53e1146b07d | 2cb9c21b425df9bfd0c36c0f8ab0257257a93a6e | true |
| all-in-one/sources/decoded-original/0540-FlgNet.xml | c05d5c1db35f1659992cae845cbcad515bbc34f00089169c0722076db9d77735 | 6b9a166d8fdf80bb52c63e90b794d69aaf34a919 | true |
| all-in-one/sources/decoded-original/0562-IdentXmlPart.xml | 85aada44dd9a3e66835463c3fed400f1efe121f4f5bc5ab8f0ad49481ec0ea1c | 1609802542a3e560baba3f2b73c306be281dfb23 | true |
| all-in-one/sources/decoded-original/0563-IdentXmlPart.xml | 86cf35b6baebc079cb5a092baf53ec3364c377ea7318eb263ab69c8b4550b4ad | 6a10fc694f896cda16409804daf2554c91635654 | true |
| all-in-one/sources/decoded-original/0564-IdentXmlPart.xml | 2aed17fa02d19b0a081023282841aa561d6a2dca3e393284da3622b967af00b1 | c4b1f2cb191970cfce1cce59cb290a9f1f934c37 | true |
| all-in-one/sources/decoded-original/0565-IdentXmlPart.xml | 0f7f970faa6c456f2bb032b1a2072a2f52db1e03fc77bd8d35d4583deeaf1149 | c2e3e2d57c94c5da864f6e172f0a7a925da942d6 | true |
| all-in-one/sources/decoded-original/0566-IdentXmlPart.xml | a1914c7ae085acc1f949a649979824bec8b46fcd78a8055318272a1eb5a45265 | 348e6fccf44a8497f58f73e89ec98e892b2df436 | true |
| all-in-one/sources/decoded-original/0567-IdentXmlPart.xml | 5d428b5d5a2b0f4649dbbbb4e4f060a9d89a107e9cf4b6139d8f003c4371347e | 48d2fdc3a37b692bfda5234b3cd84c48269552f2 | true |
| all-in-one/sources/decoded-original/0570-IdentXmlPart.xml | 9fed133006458c3b43b1d5f2c15107a5a86b4fb7cdbaf3743bf88f0e5a105495 | 15e6452f424d6ef5f0fa2407ae4e4121dbca3044 | true |
| all-in-one/sources/decoded-original/0572-IdentXmlPart.xml | 5ecd18f84e12d702bb46f759b23994dacfa2d97d50fe51e766ca0cf43f75bb4c | 67fbbd3e804418687c2ceaaea357fbc3016d38b9 | true |
| all-in-one/sources/decoded-original/0573-IdentXmlPart.xml | a22cc24a974e0c792f32e356a14b277a847e2bb204c91bce01c37d1714ddb56c | 97541d25722c43abf428aa8e2197b1973149bde2 | true |
| all-in-one/sources/decoded-original/0582-IdentXmlPart.xml | 41d4c2bd750392bbc2edc43995ec3a9da47a63c13ee86496df8f187492008951 | 82636dec064876d0f4cc714ef385b07d6e05efe0 | true |
| all-in-one/sources/decoded-original/0584-IdentXmlPart.xml | 3bff6c478e594bf97bb1730971944e96b0b5e2407199420fe6567d5fe609ea5d | 0f8dde829be66041bea79e40ccc4586d84ff1da7 | true |
| all-in-one/sources/decoded-original/0585-IdentXmlPart.xml | e36ec18aa4abebea8f9160254522bb51ff722eae804c5a469790f85f02939184 | 16574d37ef3ca61b59ba396c400e269ab1dd3440 | true |
| all-in-one/sources/decoded-original/0594-IdentXmlPart.xml | 88ad174a0d5ccdf636146b68e43aa578c449c77ceab074b7ced2580261b831cd | f38b7d9a52b3d5ae74953da8290f6b417758c1b5 | true |
| all-in-one/sources/decoded-original/0596-IdentXmlPart.xml | a0d79c7c4971d16f0e176c0c7d7b459a6e6702035b01ec01fd83e95561839dc0 | c8b2d1a05727b4ca44e2e4bed9fb58ba2b717576 | true |
| all-in-one/sources/decoded-original/0597-IdentXmlPart.xml | 60e292145fe54912a1da7510c8641a4f4c85efe62e1b5206ee3d92794a28de20 | 2831597d1879bd83f239e838dd4cbe6b3dc64e77 | true |
| all-in-one/sources/decoded-original/0598-IdentXmlPart.xml | dc001c9370a691546c5dea79f5a1252d6d0a5564754703018c47df4bcc2522bb | 17a4c24ebc97eb13db483e4c64ac386d6a69125a | true |
| all-in-one/sources/decoded-original/0604-IdentXmlPart.xml | b798d29c5499b5314a1ee3cff9139dae64c887533b86baa43b6e9a052373a6af | bb2c318788b97e7a4924a176275c12d805aa519d | true |
| all-in-one/sources/decoded-original/0617-IdentXmlPart.xml | 10bcf85169cb2512f55acadaef299a3d46b4b4cecd88032d739cfeba23e94aa9 | 9527658ee6808be34bd513b1b2ebaf3a4a5a6f3e | true |
| all-in-one/sources/decoded-original/0627-IdentXmlPart.xml | 08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb | 61ebc0abbb2ca160e11e1da400a3f14a397d8bc5 | true |
| all-in-one/sources/decoded-original/0628-IdentXmlPart.xml | 9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd | 170ca5c72599edc7ea7eefe651c3680ce325e76a | true |
| all-in-one/sources/decoded-original/0629-IdentXmlPart.xml | 67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972 | 058129bb01e27f7a6a0d0293f332d745e5bab74e | true |
| all-in-one/sources/decoded-original/0634-IdentXmlPart.xml | af3fcb536a6270ffb9a19e5b3f2c284a38d67d465f5147961005c1c01d11299d | 877d9e0734dc7f3e5a8cea789eeb58a208501f48 | true |
| all-in-one/sources/decoded-original/0635-IdentXmlPart.xml | 1a057d686446a3fdab7ac61bb09bc543c52f49646c9ca71ac323c10fcdffe457 | 95bfcad59cfb0c12b573e9e8face4262d1e94622 | true |
| all-in-one/sources/decoded-original/0636-IdentXmlPart.xml | ec3d79f03e2748f8def4409ad676a97b98e28b9d8e68f6a64b3fe894466832ca | 86114327ba1a010b2fcc01dd12b1bf86c01bc02c | true |
| all-in-one/sources/decoded-original/0648-IdentXmlPart.xml | afaa47ae737d9333fe831ffac2b1d1388f108bb6a2b23d03554fa862f7edb454 | 3dd5101419fbe16bbce7814398209efd6508db82 | true |
| all-in-one/sources/decoded-original/0662-IdentXmlPart.xml | 1838040bfee800fdb3f13b126eaf69a9d178b17cecc0d59ae03e9185216a48a5 | ba624f3460dc05e8ade4956cdfc2ec621edb4f73 | true |
| all-in-one/sources/decoded-original/0664-IdentXmlPart.xml | 68c614e1c6a7fcadeee3f0b2ddc54910c3b337e66074d7a113b9cbc834c271ed | 7ce2f1315d5a21d6b77869a59fc9fcb2f17e90e6 | true |
| all-in-one/sources/decoded-original/0678-IdentXmlPart.xml | 51e637e0b9713c028810f2a717b5c3804a3a26c2f1be7e332a4d6bf277bfc382 | 7fafb2297bcdf739bf1d1dd68cebc0d74f2a40cc | true |
| all-in-one/sources/decoded-original/0683-IdentXmlPart.xml | 0c9b569d041cd5babbbeded8a3bdc5d3754927125756b6ac54b7cb991b22fc22 | 662acdb9a06c0ba1c0027e7dd215a28f07d3f02b | true |
| all-in-one/sources/decoded-original/0684-IdentXmlPart.xml | 6e9b3f173184adcddca503e81e2649022734b6ea3639c1d5ddaf0a08bac00208 | d67b98b5d5516e0330aae5cfdbee41a3e09206e1 | true |
| all-in-one/sources/decoded-original/0686-IdentXmlPart.xml | b450d8ff22f0fffd7a214b2a696af28a03a27834ebf862bfaa822dc9bfb3c8d4 | 8c152d926692a8e15973c980e08e338d29411814 | true |
| all-in-one/sources/decoded-original/0688-IdentXmlPart.xml | ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda | 463585759f1ecd94f32362b4fefb000a152f5773 | true |
| all-in-one/sources/decoded-original/0692-IdentXmlPart.xml | bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037 | 737785d03b5fad43c5b4d451955726d800edb1c0 | true |
| all-in-one/sources/decoded-original/0694-IdentXmlPart.xml | 757ccebdf32d0a168dd787bfa735fe6494eac4c4a9f7a5adc63898a88e8b152d | c45e8f3ca4129dc06734f6a12ef79e6ed6528a7d | true |
| all-in-one/sources/decoded-original/network-map.json | c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60 | 424430b6b953e43138e5d0a18ca40c949e21cfa1 | true |
| all-in-one/sources/hmi-windows.csv | 15f8d69b5c43d4fdbe550f9cd2717f855fea877ed8146973054cb6dbcaa9892e | 8401dcfe5ba3e7e244eea0f501bb84a2e387da39 | true |
| all-in-one/sources/hmi_plc_tags.csv | a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404 | cf4c0650e7c7baac350dcb89909b808435704880 | true |
| all-in-one/sources/live_index.json | 14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1 | e35ccea1f841349c632666c29954b7bcd4f5839e | true |
| all-in-one/sources/source-manifest.json | 5af6e85994536897fd92f75972534a691e6eb0f067aafe07679c0788fd84e5bf | 38cf407491d52dc6128cf94ca8a4bddee350de6d | true |
| docs/equipment-standard/INVENTORY.json | 720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc | 587c3748ad9224718f95ba06463fee913dae231d | true |
| docs/equipment-standard/START-GPT61.md | 35769e3146ccd707fea2b81b67b30376b76a0a19c7e662fe2bb4fdd382306f94 | 0d08cab3678df7e2625251b641b138ef4956483b | true |
| docs/equipment-standard/WORK-ITEM-TEMPLATE.md | 4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586 | e546f39535d2b589e80f97db869ac37ce4d05cfd | true |
| docs/equipment-standard/WORK-STANDARD.md | 05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99 | f76a570cc73098632e08759b17934000f7e3a253 | true |
