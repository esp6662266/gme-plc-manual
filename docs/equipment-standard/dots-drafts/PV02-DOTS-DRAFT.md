# PV02 P07 고유 제어 근거와 설비 문서 초안

- 산출물: **PV02-DOTS-DRAFT.md / 1차 통합 검토용**, 2026-10-11 KST.
- 조사·작성: Dots 자체 환경에서 직접 수행. 대상은 PV02(P07) 한 개이며 기존 Codex가 로컬 반영·검증·게시를 담당한다.
- 기준: GME-STD-1.0.0, 공개 저장소 esp6662266/gme-plc-manual의 main/all-in-one/.
- 고정 원본: **5fac25b70389f38141774d35dce49f129eb1982f**, VERSION.json v1.9.1. 이것은 조사 시작점이며 PV02 게시 버전이 아니다.
- 적용: 저장소 AGENTS, gme-equipment-rollout 스킬, WORK-STANDARD·WORK-ITEM-TEMPLATE·INVENTORY의 7영역/근거 추적/완료 분리 방식을 적용했다. 제공 환경에서 tia-equipment-alarm-trace 로컬 스킬은 확보하지 못했다. 권한을 확장하지 않고 공개 원본 XML과 PDF 실제 렌더를 사용했다.
- 상태: 문서 초안 및 지정 원본 정적 대조. 현재 CPU·실물·정상 극성·현행 보호값·현장 복구는 미확정. UI/기록/PDF/배포 검증은 수행하지 않았다.
- 보존: 원본·기존 PV02 자료·기존 완료 설비와 원초안을 편집하지 않았다. 공통 코드·버전·대장·배포·운영기록 변경, 새 Work/Codex 작업 생성, 시뮬레이터 작성·수정·생성·실행·행동시험, PLC/현장/보호값 변경은 하지 않았다. 별도 세진 프로그램 데이터·코드를 사용하지 않았다.

## 먼저 확인할 PV02 고유 사항

1. 네 위치 알람의 원본 설정은 **모두 S5T#7S**다. A/B OPEN/CLOSE의 Tag84~87은 T107~T110으로 서로 다르다. 감시 대상은 raw 센서가 아니라 Flag의 위치 기억이다. [E13~E16]
2. 자동 순서 State0은 **300ms**, State3은 **800ms** 후 다음 상태로 간다. 두 분기에 MEM_CLOSE 직렬 접점은 없다. State1/4는 각각 B/A MEM_OPEN을 기다린다. 다른 게이트의 1초 값을 복사하지 않는다. [E08]
3. 자동 허용부는 MC04_Fbk OR Inputs.MC04 run OR Allarm.Maintenance_ON을 포함한다. MC04 물리 응답 하나가 항상 필수라는 설명은 틀리다. [E04,E18,E22]
4. Allarm.Maintenance_ON(DB3), Flag.Maintenance_ON(DB2), maintenance PV02(M80.6)는 이름이 비슷하지만 서로 다른 변수다. 공통 변환 쓰기와 PV02 최종 출력 읽기를 분리한다. [E03,E07,E18]
5. Q5.4/Q5.5의 최종 출력은 각각 local00/auto01/maintenance PV02 세 가지 OR다. 이 원본에는 OFF의 네 번째 가지가 없다. [E07]
6. R2_GATE_LOOP_ON은 RD01 및 RD01 팬 요청 해제 조건으로 전달된다. 단, STANDBY_ON과 UNDER TESTING의 반전 조건도 함께 있다. 단일 게이트 알람이 공정 전체를 무조건 정지시킨다고 일반화하지 않는다. [E20]
7. 시공 PDF24와 PDF55의 LS25/26 짧은 No.가 서로 다르다. 전체 케이블 ID와 FROM/TO로 대조해야 한다. 공유 간선의 EV03은 RD01 윤활 회로로 분리하며 PV02 밸브는 EV04/05다. [E25,E26]
8. HMI 호출 20핀 중 FALSE 3개를 원본 선언으로 결속했다. 나머지 17개는 실인수 선언 연결이 미확보이며, HMI 주소표나 색인 순서로 채우지 않는다. [E21]

## 1 설비와 자료 기준

### 1.1 대상 식별과 소유

INVENTORY의 P07은 catalog_id=PV02, mapping=tag, **identity_verified=false**다. 공압 게이트/분기 밸브, kind=gate, parent_id=null, phase1이다. “태그 대응”은 현장 본체 동일성이나 현재 구동기 확인 완료가 아니다. [E01]

자료상 역할은 드럼 배출측 이중 게이트다. 전기도면 기준 A는 EV04·Q5.4·LS25/26, B는 EV05·Q5.5·LS29/30으로 추적된다. P&ID PV-02 Detail에는 EV04→CL05/06와 EV05→CL07/08, LS25/26 및 LS29/30, Gate A/B 형상이 있다. 상하·실린더 행과 실물 기계의 일대일 동일성은 현장 도면/표찰 없이 확정하지 않는다. [E02,E23,E24,E26]

MC04는 PV02 자동 허용에 영향을 주는 연동 설비이지 PV02 소유 모터가 아니다. RD01 및 RD01 팬도 R2 loop를 소비하는 별도 설비다. PV02 자체 EV 제어에 모터 용량·인버터 속도·전류값·보호정격을 할당하지 않는다. 이번 대상에 모터 회로가 비해당이라는 것은 MC04/RD01의 공정 연관이 없다는 뜻이 아니다.

### 1.2 보존할 기존 자료

devices/PV02.html, control-specs/PV02.html, alarm-guides/PV02.html, circuit-guides/PV02.html, signal-guides/PV02.html, construction-guides/PV02.html, procedures/PV02.html의 완료 분석·부분 미확정·참조를 보존한다. 이번에 확인한 정적 순서·주소·핀만 보강하고, 기존 현장 미확인을 문서 검토로 완료시키지 않는다. [E27]

assets/HMI_DECOATER.png는 2026-10-07이 표시된 저장 화면이다. PV02 A/B와 인접 RD01·MC04의 화면상 배치를 확인했지만, 현재 운전·위치·Maintenance 상태나 실물 동일성은 입증하지 않는다. [E21]

### 1.3 근거 읽는 법

본문 네 자리 XML 번호는 all-in-one/sources/decoded-original/NNNN-FlgNet.xml, 선언 번호는 같은 폴더의 NNNN-IdentXmlPart.xml이다. LAD 번호는 network-map.json document_id다. NID는 선언의 원본 네트워크 식별자이며 index_order와 혼동하지 않는다. RID/UID/NID가 우연히 같은 다른 블록 후보는 분리하고 블록 선언 묶음·핀·색인을 교차 확인했다. 예: 0284의 UID26/RID109는 다른 블록의 BR01_GAS_SP 후보와 충돌하지만 PV02 블록 선언0609의 Data.PV_02B 및 같은 KF_KT 출력 결속으로 해석한다. HMI 실인수 미결속은 이 방식으로도 해결하지 못한 항목으로 남겼다.

## 2 I O와 HMI

### 2.1 물리 입력과 출력

주소는 **백업 선언**과 OEM 도면의 대응이다. E/A는 도면 표기, I/Q는 PLC 표기이며 현재 배선·다운로드·극성을 의미하지 않는다. [E02,E23,E24]

| 항목 | 원본 심볼 및 백업 주소 | 선언 근거 | 회로 끝점 |
| --- | --- | --- | --- |
| A 열림 | EV04_Open I9.4 Bool | 0607 RID135, SAD Input AO76, NID13 UID38 | LS25 13/14, X1/145→146→E9.4, FG125 MOD10 단자15 |
| A 닫힘 | EV04_Close I9.5 Bool | 0607 RID137, Input AO77, NID13 UID44 | LS26 13/14, X1/147→148→E9.5, FG125 단자16 |
| B 열림 | EV05_Open I9.6 Bool | 0607 RID140, Input AO78, NID14 UID38 | LS29 13/14, X1/149→150→E9.6, FG125 단자17 |
| B 닫힘 | EV05_Close I9.7 Bool | 0607 RID142, Input AO79, NID14 UID44 | LS30 13/14, X1/151→152→E9.7, FG125 단자18 |
| A 현장 요청 | Selector Op Gate A PV-02 I10.0 Bool | 0607 RID79, Input AO80, NID7 UID692 | PB16 72SB1→72SA1 A→X1/154→E10.0, FG126 단자21 |
| B 현장 요청 | Selector Op Gate B PV-02 I10.1 Bool | 0607 RID81, Input AO81, NID7 UID694 | PB16 72SB1→72SA1 B→X1/155→E10.1, FG126 단자22 |
| A EV 출력 | PV-02 GATE A EV Q5.4 Bool | 0607 RID85, Output AO44, NID8 UID733 Write | FG141 MOD15 단자15 A5.4→FG71 71KA1→EV04 |
| B EV 출력 | PV-02 GATE B EV Q5.5 Bool | 0607 RID84, Output AO45, NID8 UID729 Write | FG141 MOD15 단자16 A5.5→FG71 71KA2→EV05 |

AO는 비트 오프셋이다. 예:76=9×8+4,44=5×8+4. 기존 주석 E29.6/29.7/29.2/29.3, E45.4/45.5, A53.7/56.4는 보존할 과거 설명이며 위 선언 주소를 대체하지 않는다. LS27/28/31/32 시공 표기를 별도 네 PLC 입력으로 추가하지 않는다.

MC04 연동 입력은 별도 행으로 취급한다: 0607 RID51 MC04_Fbk Input AO6=I0.6, NID5 UID482. 처리 응답은 0609 RID87 Inputs.MC04 run AO6 및 0608 Inputs TOD13=DB13.DBX0.6이다. 두 신호가 OR로 사용되는 사실과 실제 동일값인지는 구분한다. [E04,E22]

### 2.2 내부 요청과 처리 변수

| 이름 | 백업 주소·형식 | 선언·소유 |
| --- | --- | --- |
| ON | M0.0 Bool | 0607 RID1, Memory AO0. 상수 true 아님 |
| PV-02 Gate ON | M12.2 Bool | 0607 RID57 AO98; 0280 Coil456 쓰기 |
| Open EV A 00 / B 00 PV-02 | M30.4 / M30.5 Bool | 0607 RID80/82 AO244/245; 0282 Coil686/690 쓰기 |
| Close EV A 01 / Open EV B 01 | M30.0 / M30.1 Bool | 0607 RID63/62 AO240/241; 자동 S/R |
| Close EV B 01 / Open EV A 01 | M30.2 / M30.3 Bool | 0607 RID64/61 AO242/243; 자동 S/R |
| maintenance PV02 | M80.6 Bool | 0607 RID83 AO646; 0283 읽기. 작성 경로는 미확보 |
| Flag.Enable_R2_GATE | DB2.DBX10.3 Bool | 0609 RID52 AO83+0608 Flag TOD2; 공통 자동/HMI 주소 참조 |
| Flag.R2_GATE_LOOP_ON | DB2.DBX10.4 Bool | 0609 RID58 AO84; 0280 Coil458 쓰기, RD01·팬 소비 |
| A_MEM_CLOSE / A_MEM_OPEN | DB2.DBX8.4 / 8.5 Bool | 0609 RID139/55 AO68/69 |
| B_MEM_CLOSE / B_MEM_OPEN | DB2.DBX8.6 / 8.7 Bool | 0609 RID144/56 AO70/71 |
| WorkData.W7 | DB6.DBW14 Int | 0609 RID60 AO112+0608 WorkData TOD6; 0280/0281 Move |
| Data.PV_02A / PV_02B | DB1.DBW304 / 306 Int | 0609 RID114/109 AO2432/2448+Data TOD1; KF 입력 |
| SET_PV02A_Open_time / B | DB1.DBW156 / 154 Word | 0609 RID76/113 AO1248/1232; KF_KT 출력→타이머 value |
| Inputs.PV-02 EV A OPEN / CLOSE | DB13.DBX9.4 / 9.5 Bool | 0609 RID136/138 AO76/77, Inputs TOD13 |
| Inputs.PV-02 GATE B OPEN / CLOSE | DB13.DBX9.6 / 9.7 Bool | 0609 RID141/143 AO78/79, Inputs TOD13 |

위 주소는 SAD/SSD/BAD와 DB TOD를 대조했다. 기존 내부 심볼 mem gate a open pv-02 M12.4, mem gate b open pv-02 M12.3을 실제 루프의 Flag DB 기억과 합치지 않는다. 이름만 비슷한 사용 미확정 태그는 기존 자료에 남긴다. [E03]

### 2.3 물리 입력에서 Inputs로 전달되는 범위

0397 LAD1070 hmi inputs/NID1에서 아래 Move를 확인했다. 선언0627의 Input Word와0629의 Word 목적지,0628 RID4 Inputs TOD13을 묶었다. [E22]

| 범위 | Part와 핀 | 선언 |
| --- | --- | --- |
| MC04 응답 I0.6 포함 IW0→DB13.DBW0 | Move22, W23/ORef25→in, out1→W24/ORef26 | 0627 RID3 Tag178 Input Word AO0;0629 RID5 AO0 BAD4 |
| PV02 위치 I9.4~9.7 포함 IW8→DB13.DBW8 | Move43, W55/ORef47→in, out1→W57/ORef48 | 0627 RID15 Tag181 Input Word AO64;0629 RID16 AO64 BAD4 |
| PV02 현장요청 I10.0/10.1 포함 IW10→DB13.DBW10 | Move44, W58/ORef49→in, out1→W59/ORef50 | 0627 RID17 Tag182 Input Word AO80;0629 RID18 AO80 BAD4 |

Move22.en은 W21 powerrail, Move43.en은 Move42.eno→W53, Move44.en은 Move43.eno→W56이다. Word 전달이 포함 비트를 보존하는 구조라는 것과 현재 raw/DB가 같은 값이라는 것은 다르다.

호출 경계 0030 LAD1613/NID19: CRef21 Recipes Handler.eno→W32→CRef23 HMI.en→W33→CRef25 HMI Output.en; 그 eno→W42→Contact37 **NOT Simulation(1)**(ORef45/W44)→W43→CRef28 HMI Inputs.en. 0688 RID120/124/128/135,0692 RID140(M180.0),0694 RID136 결속이다. 현재 M180.0·ENO·CPU호출·다른 DB 쓰기와 실제 값은 미확정이다. 중지된 시뮬레이터는 실행·수정·생성하지 않았다.

### 2.4 HMI 설정과 원본 호출

sources/hmi_plc_tags.csv의 Access Name은 PLC이며 다음 8개 PV02 설정을 확인했다. [E21]

| 태그 | 설정 주소 | 내부 ID | 역할·한계 |
| --- | --- | --- | --- |
| PV_02\Flag | DB2,X10.3 | 000A8 | Enable_R2_GATE와 백업 주소 일치, 객체 이벤트/쓰기 방식 미확정 |
| PV_02\GateA_Open | DB11,X78.1 | 000A6 | A 열림 표시 후보 |
| PV_02\GateA_Close | DB11,X78.2 | 000A5 | A 닫힘 표시 후보 |
| PV_02\GateB_Open | DB11,X78.3 | 00077 | B 열림 표시 후보 |
| PV_02\GateB_Close | DB11,X78.4 | 00076 | B 닫힘 표시 후보 |
| PV_02\Selector_GateA | DB11,X78.5 | 00075 | 현장 선택 상태 표시 후보, 독립 Q명령 아님 |
| PV_02\Selector_GateB | DB11,X78.6 | 00074 | 현장 선택 상태 표시 후보 |
| PV_02\Allarme1 | DB11,X78.0 | 00073 | 통합 알람 표시 후보, 특정 하나의 알람과 합치지 않음 |

공통 AbilitaMaintenance DB2,X7.5와 ResetAlarms DB2,X13.4는 PV02 전용 태그 수에 넣지 않는다. 공통 요청과 PV02 M80.6의 소유는 별도다.

0392 LAD1216는 CRef22(RID716) / CodeBlock23(RID715) HMI PV_2Gate 호출이다. 0624/0623의 **NID40**와 결속된다. 원본에 20개 ORef가 있고 0626 RID48/NID40 UID34/35/36은 FALSE, Allarm5/6/7 핀에 각각 연결된다. 나머지17개는 실인수 선언 결속을 확보하지 못했다. 색인에는 Inputs 위치/선택과 네 PV02 알람, Motors.pv_02 출력 이름이 있지만 그 순서만으로 핀을 확정하지 않는다. 전체 Wire/ORef/RID는 부록 B에 둔다.

공통 함수0400/LAD347의0631 LocalAccess는 위치/selector 입력→HMI 출력, Allarm1~7 OR→Total_Allarms 구조다. 공통 함수 구현을 확인해도0392의 미해결17개 인수나 DB11멤버 결속이 자동 증명되는 것은 아니다. HMI 현재 화면·통신·누르기 이벤트도 미확정이다.

## 3 제어 구조와 소유

다음 식과 표는 원본 정적 접점·코일 해석이다. 실행모델·시뮬레이션·행동시험을 작성하지 않았다. !는 operand Negated, S/R은 원본의 래치 쓰기다.

### 3.1 PV02 자동 허용

0280 LAD1916, 블록 r1 scraps gate 2, NID5: [E04]

C = MC04_Fbk OR Inputs.MC04 run OR Allarm.Maintenance_ON

P = ON AND C AND [(Enable_R2_GATE AND !A_NOT_OPEN AND !B_NOT_OPEN) OR (!Enable_R2_GATE AND A_MEM_OPEN AND B_MEM_OPEN)]

P는 PV-02 Gate ON과 Flag.R2_GATE_LOOP_ON 두 코일에 간다.

- Contact524 ON→W525→Contact526 MC04_Fbk / Contact22 Inputs.MC04 run / Contact29 Allarm.Maintenance_ON.
- W527/W24/W31→OR443 in1/2/3, out W502.
- 가지1: Enable530→W531→NOT A_NOT_OPEN532→W533→NOT B_NOT_OPEN534→W535→OR450 in1.
- 가지2: NOT Enable536→W537→A_MEM_OPEN538→W539→B_MEM_OPEN540→W541→OR450 in2.
- OR450.out W511→Coil456/458; W512/ORef490→0607RID57, W513/ORef491→0609RID58.
- 핵심 피연산자: MC04 raw ORef482/RID51 Input AO6; 처리ORef23/RID87; maintenanceORef30/RID156; EnableORef484/487 RID52; 알람ORef485/486 RID53/54; 위치기억ORef488/489 RID55/56.

NOT_CLOSE 알람 두 개는 이 직접 허용부에 없다. Allarm.Maintenance_ON 가지가 있으므로 “MC04 raw응답=1만이 유일한 전제”라고 설명하지 않는다. 그러나 이 가지의 존재를 현장 인터록 우회 허가로 해석하거나 사용하지 않는다.

### 3.2 허용 탈락 시 자동 요청 초기화

같은0280에서 ON 뒤 NOT PV-02 Gate ON Contact542, W515/ORef492→W543을 따라 Move466과 RCoil471/474/477/480을 구동한다. Move466.in W516/ORef493은0610 literal0; out1 W517/ORef494은0609 RID60 WorkData.W7이다. R 대상은 OpenA01/OpenB01/CloseA01/CloseB01, ORef495~498→0607RID61~64다. [E05]

이 구간은 auto01 네 요청과 W7을 초기화한다. local00(M30.4/.5)과 maintenance PV02(M80.6)를 지우는 코일은 여기 없다. Enable=0이면 모든 밸브 출력이 반드시0이 된다고 단정하지 않는다.

### 3.3 현장 요청과 최종 EV 출력

0282 LAD1919/NID7: ON Contact704/W696→W705. A selector Contact706(W697/ORef692)→W707→Coil686(W699/ORef693 OpenA00). B selector708(W700/ORef694)→W709→Coil690(W702/ORef695 OpenB00). [E06]

0283 LAD1920/NID8: [E07]

- Q5.4 = ON AND (OpenA00 OR OpenA01 OR maintenance PV02)
- Q5.5 = ON AND (OpenB00 OR OpenB01 OR maintenance PV02)

ON Contact748/W734→W749 공통전제. B는750/752/754→OR713→W738→Coil717, 대상W740/ORef729 RID84. A는756/758/760→OR720→W744→Coil724, 대상W746/ORef733 RID85. 각 입력의 operand W735/736/737 및 W741/742/743에 local/auto/maintenance가 결속된다.

이 출력 네트워크의 OR는 **각각3입력**이며 OFF추가분기는 없다. Enable/MC04응답/알람/MEM이 최종 Q 앞에 직접 직렬이라고 쓰지 않는다. 그 중 자동 허용부의 효과는 auto01 경유다. CloseA/B01은 순서상의 내부 요청이며 별도 닫힘 출력 코일로 사용되지 않는다. Q해제와 실물 닫힘·안전 위치는 구분한다.

### 3.4 PV02 고유 0부터5 순서

0281 LAD1918/NID6. 공통전제는 ON Contact898→Enable_R2_GATE900→PV-02 Gate ON902→W903이다. State는 WorkData.W7이며 Eq671/693/711/727/749/767로0~5를 비교한다. [E08]

| W7 | 해당 단계의 요청 쓰기 | 다음 상태 조건과 핀 |
| --- | --- | --- |
| 0 | S677 CloseA01, R680 OpenA01 | SD683 Tag167/T8, value W838/ORef788 **S5T#300MS**; Contact904 Tag167→W905→Move688(1→W7) |
| 1 | S699 OpenB01, R702 CloseB01 | Contact906 B_MEM_OPEN(W850/ORef797)→W907→Move706(2→W7) |
| 2 | 요청 유지 | SD717 Tag168/T9, value W858/ORef802 SET_PV02B_Open_time; Contact908→W909→Move722(3→W7) |
| 3 | S733 CloseB01, R736 OpenB01 | SD739 Tag169/T10, value W870/ORef811 **S5T#800MS**; Contact910 Tag169→W911→Move744(4→W7) |
| 4 | S755 OpenA01, R758 CloseA01 | Contact912 A_MEM_OPEN(W882/ORef820)→W913→Move762(5→W7) |
| 5 | 요청 유지 | SD773 Tag170/T11, value W890/ORef825 SET_PV02A_Open_time; Contact914→W915→Move778(0→W7) |

고정시간 근거는0610 RID65/NID6 UID788(S5T#300MS), RID72 UID811(S5T#800MS). Timer선언은0607 RID66/70/73/77, SAD Timer AO8/9/10/11이다. State0/3 전이 접점에는 각각의 MEM_CLOSE 확인이 없다. “닫힘 센서를 확인한 다음 다음 게이트를 연다”는 통상적인 설명으로 바꾸지 않는다. 고정 지연이 물리적으로 적절한지, 몇 스캔에 전이하는지, 실제 겹침/위험 여부는 현장 근거 없는 미확정이다. 값 변경이나 시험을 지시하지 않는다.

### 3.5 가변 체류 시간 변환

0284 LAD1917/NID9에서 KF_KT 두 호출이 연결된다.0060 RID121 KF_KT,0061 RID122 인터페이스. [E09]

| 호출 | 입력과 값 | 출력과 후속 |
| --- | --- | --- |
| CRef23/CodeBlock22 | KF W25/ORef26→Data.PV_02B RID109; SEC W27/ORef28→literal0 RID150 | KT W29/ORef30→SET_PV02B_Open_time RID113; eno W33→CRef32.en |
| CRef32/CodeBlock31 | KF W34/ORef35→Data.PV_02A RID114; SEC W36/ORef37→literal0 RID150 | KT W38/ORef39→SET_PV02A_Open_time RID76 |

입력은 Int, 출력은 Word다. 함수 몸체의 변환 단위·범위·SEC=0의 의미와 현재 DB값은 확보하지 못했다. A/B 체류 시간을300ms/800ms 또는7초로 대체하지 않는다. 이들은 서로 다른 목적의 설정이다. KF_KT 호출만으로 현재 체류를 초 단위 수치로 만들어 넣지 않는다.

### 3.6 위치 기억과 시작시 닫힘 기억

A 0288 LAD1923/NID13: [E10]

- S A_MEM_OPEN = ON AND Q_A AND (EV04_Open OR Inputs.PV-02 EV A OPEN).
- R A_MEM_OPEN = ON AND !Q_A.
- S A_MEM_CLOSE = ON AND !Q_A AND (EV04_Close OR Inputs.PV-02 EV A CLOSE).
- R A_MEM_CLOSE = ON AND Q_A.
- Part21 ON,22Q→23raw/24DB→OR25→S26(W58/59); NOT27→R28(W61/62). NOT29→30raw/31DB→OR32→S33(W69/70);34Q→R35(W72/73).

B 0289 LAD1924/NID14: [E11]

- S B_MEM_OPEN = ON AND Q_B AND (EV05_Open OR Inputs.PV-02 GATE B OPEN).
- R B_MEM_OPEN = ON AND !Q_B.
- S B_MEM_CLOSE = ON AND !Q_B AND (EV05_Close OR Inputs.PV-02 GATE B CLOSE).
- R B_MEM_CLOSE = ON AND Q_B.
- Part21ON,22Q→23raw/24DB→OR25→S26(W58/59); NOT27→R28(W84/62). NOT29→30raw/31DB→OR32→S33(W69/70);34Q→R35(W89/73).
- 출력 ORef83/86/88/91→0607RID84, raw ORef38/44→RID140/142, DB ORef39/45→0609RID141/143, MEM ORef40/42와46/48→RID56/144이다. 이 B 네트워크에 false AND close의 추가 가지는 없다.

두 네트워크의 S결과는 센서 순간값과 다른 **방향별 래치**다. raw와Inputs를 독립 관찰하고, 같은 이름의 HMI 표시와 동일시하지 않는다.

0150 LAD405 startup/NID5는 ON Contact326→W327에서 S303 A_MEM_CLOSE와 S305 B_MEM_CLOSE를 쓴다. W320/ORef314→0563RID49 AO68, W321/ORef315→0563RID50 AO70이다. 시작시 닫힘기억 Set은 실제 닫힌 것을 센서로 확인했다는 증거가 아니다. [E12]

### 3.7 유지보수와 공통 자동의 쓰기 소유

0237 LAD1930 motors1/NID1: ON Contact47(W42/ORef38)→Flag.Maintenance_ON Contact49(W43/ORef39)→W50→Coil34 UNDER TESTING와 Coil36 Allarm.Maintenance_ON. 대상은W44/ORef40(0602RID4 M5.5),W45/ORef41(0604RID6 DB3X7.5), 입력은0604RID3 DB2X7.5다.0603의Flag/Allarm TOD2/3으로 DB를 구분한다. [E18]

따라서 PV02 permit의 **Allarm.Maintenance_ON(DB3X7.5)**에는 공통 유지보수 전달 쓰기가 있다. 이것을 M80.6 maintenance PV02의 작성자라고 바꾸지 않는다. M80.6의 직접 작성은 이번 자료에서 확보하지 못했다. 현재 공통 모드/다른 쓰기/호출 순서도 미확정이다.

Enable_R2_GATE는 HMI설정주소 외에 두 공통 쓰기를 확인했다. [E19]

| 원본 | 쓰기 | 조건과 원본 증거 |
| --- | --- | --- |
| 0164 LAD1843 NID3 예열 | **R462** Enable | ON AND !Emergency_module_fault AND Tipo_preset=1 AND Auto_ON1 AND Tempo_presetting=17. Eq452 in1 W703/ORef612, in2 W704/ORef613(0578RID30=17); out W705→R462; W709/ORef617→0577RID34 |
| 0165 LAD1844 NID4 생산 | **S805** Enable | ON AND !Emergency_module_fault AND Auto_ON1 AND Tipo_preset=2 AND Tempo_presetting=27. Eq802 in1 W1063/ORef963, in2 W1064/ORef964(0578RID82=27); out W1065→S805; W1067/ORef965→0577RID34 |

17/27은 비교값이며 이 표만으로 초 단위를 확정하지 않는다. 예열은 Set이 아니라 Reset이다. 다른 설비의 예열 쓰기·정지 단계·1분 타이머를 PV02 Enable에 복제하지 않는다. 이것이 전역 쓰기 전체나 최종 우선순위라는 주장은 하지 않는다.

### 3.8 R2 loop에서 RD01로 전달되는 경계

0243 LAD1936/NID7에서 !R2_GATE_LOOP_ON AND !STANDBY_ON AND !UNDER TESTING은 ON 아래 RD01 요청 해제 OR의 한 가지다. Contact278NOT(W260/ORef247)→280NOT(W261/ORef248)→35NOT(W34/ORef36)→W37→OR28.in5, OR28.out W30→RCoil236 Flag.M_RD_01. 다른 OR가지에는 RD01FAULT·INV·설정0·팬응답 부재가 있어 loop 하나로 전체를 설명하지 않는다. [E20]

0245 LAD1939/NID9는 ON 아래 Contact311NOT R2loop(W297/ORef290)→313NOT Standby(W298/ORef291)→318NOT UnderTesting(W321/ORef319)→W22→OR278.in2, ORout W300→RCoil283 Flag.M_RD_01_FAN. 다른 in1은 RD_01_FAN_FAULT다. 두 네트워크의 나머지 모든 공정 제어는 이번 PV02 조사 범위로 재분석하지 않았다.

선언0604 RID46 R2loop는DB2X10.4, RID11 Standby는DB2X7.4,0602RID4 UnderTesting은M5.5다. PV02 loop상실이 요청 Reset분기로 전달된다는 정적 사실과 실제 현장 정지·재기동의 결과를 구분한다.

## 4 전기 전달 경로와 도면 끝점

### 4.1 페이지별 판본

all-in-one/sources/Electrical_Rev2.pdf의 파일명에서 모든 페이지 개정을 추정하지 않았다. PDF는1부터 센 실제 페이지다. [E23,E24,E26]

| FG | PDF | 실제 개정란 | 대조 범위 |
| --- | --- | --- | --- |
| 71 | 72 | 공란, 기본 DATE27.05.2024 | EV04/05·71KA1/2 출력 |
| 72 | 73 | 공란, 기본 DATE27.05.2024 | LS25/26/29/30, PB16 |
| 125 | 126 | 공란, 기본 DATE27.05.2024 | MOD10 E9.4~E9.7 |
| 126 | 127 | Rev2 17.03.2025 | MOD10 E10.0/E10.1 |
| 141 | 142 | Rev2 17.03.2025 | MOD15 A5.4/A5.5 |
| 21 | 22 | 공란, 기본 DATE27.05.2024 | EV03 소유 구분용 RD01 윤활 회로만 |

### 4.2 A와 B 밸브 출력

A PLC측: FG141 MOD15단자15 A5.4→FG71/3→71KA1코일 A1/A2→-0Vdc10.6.
A 부하측: 110Vac9.7→71KA1접점1/9→선71.1→X1/141(5×20,2A F 도면표기)→선71.2→EV04 A1; EV04 A2→X1/142→0Vac9.9. [E23]

B PLC측: FG141 MOD15단자16 A5.5→FG71/6→71KA2 A1/A2→-0Vdc10.6.
B 부하측: 110Vac9.7→71KA2접점1/9→선71.3→X1/143(5×20,2A F)→선71.4→EV05 A1; A2→X1/144→0Vac9.9.

PLC DC출력·릴레이코일과110VAC 밸브부하를 분리한다. 도면 퓨즈 표기는 현재 보호값·현장 실물 규격의 승인 근거가 아니다. 출력0이 실제 닫힘·정전안전위치라는 결론은 밸브 스풀/복귀방식·공압·실린더 자료 없이 낼 수 없다.

### 4.3 위치 센서와 PB16

FG72: +24Vdc10.7→X1/145,147,149,151 각2A F→LS25/26/29/30 접점13/14→X1/146,148,150,152→E9.4/.5/.6/.7→FG125 MOD10단자15/16/17/18이다. [E24]

현장 조작: +24Vdc10.7→X1/153 2A F→72SB1 GREEN PB16 접점13/14→선72.6→72SA1 WHITE PB16 Gate A/B 선택 접점→X1/154 E10.0 또는X1/155 E10.1→FG126 단자21/22.

접점 심벌은 도면상 표현이며 실제 정상극성·작동 위치·동시선택 가능성·현행 스위치 상태는 미확정이다. FG126의 다른 LS32/33 SPARE 표기를 PV02의 여섯 입력에 옮기지 않는다. 이 페이지의 PV02는 E10.0/E10.1 두 현장요청이다.

### 4.4 시공 케이블의 공유와 상충

Electrical_Can_Decoating_20241118.pdf 실제 PDF24/55를 확인했다. 제목란24.11.11 first draft design이며 현행 승인·준공·실물 결선 확인이 아니다. 이 공개 GME 원본에 고객명이 있더라도 별도 세진 앱 데이터·코드·운영기록을 혼합하지 않았다. [E25]

| PDF55 행 | 전체 케이블 ID | FROM→TO | 규격 원문 |
| --- | --- | --- | --- |
| 5_1 | =ROT+UC01-ROT1TB1A | CR→UC01 ROT1TB1, LS25–32/PB16 | DC CVV 25G 1.0 SPARE5 |
| 5_2 | =ROT+UC01-ROT1TB1B | CR→UC01 ROT1TB1, EV03/04/05 | AC CVV 12G 1.0 SPARE5 |
| 5_3 | =ROT+RD01-ROT1TB2A | UC01 ROT1TB1→RD01 ROT1TB2, EV03 | AC CVV 3G 1.0 SPARE0 |
| 5_4 / 5_5 | =ROT+PV02-LS25A / =ROT+PV02-LS26A | UC01 ROT1TB1→PV02 LS25/LS26 | DC CVV 2C 1.0 SPARE0 |
| 5_8 | =ROT+PV02-EV04A | UC01 ROT1TB1→PV02 EV04 | AC CVV 3G 1.0 SPARE0 |
| 5_9 / 5_10 | =ROT+PV02-LS29A / =ROT+PV02-LS30A | UC01 ROT1TB1→PV02 LS29/LS30 | DC CVV 2C 1.0 SPARE0 |
| 5_13 | =ROT+PV02-EV05A | UC01 ROT1TB1→PV02 EV05 | AC CVV 3G 1.0 SPARE0 |
| 5_14 | =ROT+PV02-PB16A | UC01 ROT1TB1→PV02 PB16 | DC CVV 5G 1.0 SPARE1 |
| 5_15 | =ROT+RD01-EV03A | RD01 ROT1TB2→RD01 EV03 | AC CVV 3G 1.0 SPARE0 |

PDF24에서는 LS25/26의 짧은 No.가5_3/5_4이고 전체ID는 각각 =ROT+PV02-LS25A/-LS26A다. PDF55에서는 그 ID의 행이5_4/5_5이며5_3은RD01-ROT1TB2A다. **No.만 연결하면 회로를 잘못 묶을 수 있다.** PDF24 첫 ROT1TB1A의 CORE26과 PDF55의25G 표기도 문서 차이로 남긴다. 심수·G/C와실제핀을 임의 환산하지 않는다.

PDF55에는 LS27/28 및 LS31/32 추가 가지가 있지만 원본 PV02 위치 입력은 LS25/26/29/30 네 개다. 추가 센서 실물·직렬/병렬·예비·기계역할은 미확보이며 PLC I/O를 늘리지 않는다. OEM X1/141~155와 ROT1TB1 개별 단자·심선의 일대일 대응표도 미확보다.

### 4.5 공압 및 EV03 소유 구분

P&ID PDF1의 PV-02 Detail은 EV04→CL05/06, EV05→CL07/08, LS25/26/29/30와Gate A/B 형상을 제시한다. 솔레노이드의스풀·스프링·실제복귀·압력/유량 설정은 이 상세도만으로 확정하지 않는다. [E26]

공유 ROT1TB1에서 분기한 EV03은 FG21/PDF22 제목 **ROTATING DRUM RD-01**, LUBRIFICATION VALVE로 표시된다. A5.1→21KA2,110Vac→접점→X1/50→EV03→X1/51→0Vac 경로이며 PV02의A5.4/.5와 별도다. 이 경계 확인만 수행했고 RD01 전체 조사·통합을 시작하지 않았다. EV03을 PV02 세 번째 밸브로 추가하지 않는다.

## 5 알람과 복구 경계

### 5.1 PV02 고유 네 위치 알람

한국어는 설명용 별칭이며 원본HMI 메시지ID·문구가확인되었다는 뜻은 아니다. Allarm 철자를 보존한다. PV_02\Allarme1과 아래개별비트를합치지 않는다. [E13~E16,E21]

| PLC 원문 | 설명 별칭 | 백업 주소 | Timer와고정설정 | 원본 SD / S / R |
| --- | --- | --- | --- | --- |
| Allarm.PV_02_GATE_A_NOT_OPEN | A 열림 미확인 | DB3.DBX10.5 | Tag84 T107 S5T#7S | 0451:1581 /1587 /1592 |
| Allarm.PV_02_GATE_A_NOT_CLOSE | A 닫힘 미확인 | DB3.DBX10.6 | Tag85 T108 S5T#7S | 0451:1599 /1605 /1610 |
| Allarm.PV_02_GATE_B_NOT_OPEN | B 열림 미확인 | DB3.DBX10.7 | Tag86 T109 S5T#7S | 0452:1645 /1651 /1656 |
| Allarm.PV_02_GATE_B_NOT_CLOSE | B 닫힘 미확인 | DB3.DBX11.0 | Tag87 T110 S5T#7S | 0452:1663 /1669 /1674 |

주소 근거:0657 RID185/187/189/191 AO85/86/87/88,AllarmDB3. Timer는0658RID184/186/188/190 SADTimerAO107/108/109/110. 특히 B_NOT_CLOSE는 DB3X11.0이지10.8이 아니다. 설정은0656RID320의S5T#7S이며 현재 보호·운전설정으로 승인하지 않는다.

### 5.2 타이머와 래치 조건의 분리

각 OPEN 감시는 ON AND 해당Q AND !MEM_OPEN, CLOSE감시는 ON AND !해당Q AND !MEM_CLOSE다. S알람은각각 ON AND Q방향조건 AND Timer접점으로 설정된다. 타이머입력과S코일입력을 구분한다.

- A OPEN 0451 NID44: ON1656→Q1658→NOTMEM1679→W21→SD1581; valueW1632/ORef1613,operandW1633/ORef1614;Timer접점1660→W22→S1587,대상W1637/ORef1617.
- A CLOSE: ON→NOTQ1668→NOTMEM1683→W23→SD1599;valueW1644/ORef1622,operandW1645/ORef1623;Timer접점1670→W24→S1605,대상W1649/ORef1626.
- B OPEN 0452 NID45: ON1720→Q1722→NOTMEM1743→W21→SD1645;valueW1696/ORef1677,operandW1697/ORef1678;Timer접점1724→W22→S1651,대상W1701/ORef1681.
- B CLOSE: ON→NOTQ1732→NOTMEM1747→W23→SD1663;valueW1708/ORef1686,operandW1709/ORef1687;Timer접점1734→W24→S1669,대상W1713/ORef1690.

Q0에서의닫힘감시를 “운전중에만발생”으로좁히지 않는다. MEM은raw와Inputs병렬입력및startupS의영향을받으므로 알람만으로센서고장·기계끼임·정상위치를확정하지 않는다. 여기서직접확인한네알람을PV02의모든공통공정알람총수로간주하지 않는다.

### 5.3 Reset와실제복구

각 R알람 조건은 **ON AND Flag.RESET_ALLARM AND 자기알람**이다.

- AOPEN Contact1664/1666→W1667→R1592,대상W1642/ORef1620.
- ACLOSE Contact1674/1676→W1677→R1610,대상W1654/ORef1629.
- BOPEN Contact1728/1730→W1731→R1656,대상W1706/ORef1684.
- BCLOSE Contact1738/1740→W1741→R1674,대상W1718/ORef1693.

공통 0158 LAD930/NID9: Inputs.Reset_allarmi Contact23(W22/ORef24)와Flag.Reset_Allarms_HMI Contact26(W25/ORef27)→OR28→W38→S33 Flag.RESET_ALLARM(W36/ORef37),동시에R40가HMI요청을해제(W42/ORef43). 선언0565와대조했다. 다른공통Reset작성·초기화와스캔순서는미확정이다. 이페이지의3초TOF를PV027초감시나복구대기시간으로복사하지않는다. [E17]

센서회복만으로자동래치해제된다고쓰지않는다. Reset후래치0과실제원인제거·기계안전·현장복구완료는별개다. 원인이남으면후속감시에서재설정될수있다. 강제출력·센서우회·지연값증대·무조건Reset을처방하지않는다.

## 6 증상별 수리 문서 초안

이 표는 승인된 현장 점검에 필요한 **관찰과 근거 대조 항목**이며, 직접 수리·통전·게이트 조작 절차가 아니다. 전기 및 공압 격리, 잔압·낙하·끼임 통제, 자격자의 승인 절차 없이 접근·조작하지 않는다. 실제 값·관찰·조치·복구는 이 초안에 기록하지 않았다.

| 증상 | 구분할관찰·첫불일치구간 | 원본근거 | 확보할자료 |
| --- | --- | --- | --- |
| 자동게이트불허 | MC04raw/Inputs,AllarmMaintenance,Enable,NOT_OPEN,MEM_OPEN을분리 | E04/E18/E19/E22 | 동일시각신호·현재호출/타쓰기,MC04응답전달근거 |
| Enable해제해도EV출력남음 | local00/auto01/M80.6와최종Q를분리 | E05~E07 | M80.6작성자,HMI이벤트,실제I10.0/.1 |
| A/B7초열림알람 | Q와MEM_OPEN,raw/DB,KA코일→접점→EV전원→공압→실린더/기계→LS | E10/E11/E13/E15/E23/E24 | 밸브정격/형식·현행결선·센서극성·실제이동시간 |
| 출력0에서닫힘알람 | NOTQ/MEM_CLOSE/startup,LS26/30실제상태 | E10~E12/E14/E16 | 복귀구조·잔압·실물닫힘·센서정상상태 |
| 순서0/3의빠른전이 | 300ms/800ms와MEM_CLOSE접점부재 | E08 | 승인설계의도·기계간섭/위험검토. 초안에서로직수정안함 |
| 순서1/4또는2/5대기 | 전자는MEM_OPEN,후자는가변체류타이머 | E08/E09 | 현재W7·DBInt/Word·KF_KT본문·호출/타이머상태 |
| PV02문제와RD01/팬정지동반 | R2loop/Standby/UnderTesting복합Reset분기와다른고장을구분 | E20 | 같은시각요청·알람·실제응답. 정지/재기동단정금지 |
| HMI위치와raw가다름 | rawI→Inputs→MEM과HMI DB11을따로추적 | E10/E11/E21/E22 | 0392미결속17인수·HMI이벤트/통신·다른DB쓰기 |
| 케이블번호가맞지않음 | PDF24/55의전체ID·FROM/TO·모듈/단자를대조 | E25/E26 | 준공단자표·양단표찰·LS추가분기·심선대응 |
| Reset후재발 | 래치해제와지속원인·초기화·복구증거를분리 | E12~E17 | 원인/배제/조치/회복기록·승인된재가동확인 |

기록 항목: 관찰자, 시간/시간대, 위치·설비 실물ID, CPU/프로젝트근거, 신호값과단위, 수집장치, 원본판본·페이지/핀, 비교대상, 최초불일치구간, 배제결과, 조치, 복구증거. 운영자료를 공개저장소에붙이지않고실제기록은사용자담당범위에서보존한다.

## 7 완료 기준과 통합 인계

### 7.1 7영역 적용

| 영역 | 상태 | 위치 | 미확보·비해당 경계 |
| --- | --- | --- | --- |
| 설비·자료 기준 | 적용 | §1 | 실물동일성·현재승인도면미확정 |
| I/O·HMI | 적용/부분미확보 | §2 | HMI17실인수·이벤트·현재값미확정 |
| 제어 구조 | 적용 | §3 | KF_KT본문·M80.6작성자·전체우선순위미확정 |
| 전기 전달 경로 | 적용/부분미확보 | §4 | 개별심선·현행결선·실물밸브미확정 |
| 알람·복구 | 적용 | §5 | 고유4위치알람과공통조건구분;현장복구미실행 |
| 증상별 수리 | 적용/관찰계획 | §6 | 실제원인·조치·관찰값없음 |
| 완료 기준 | 적용 | §7/부록 | 코드/UI/기록/PDF/게시검증담당자대기 |

모터/인버터 전용값은 PV02 EV 제어의 직접 근거가 없어 적용하지 않는다. 자료가 없다는 이유로 HMI결속·현장복구를 비해당 처리하지 않는다.

### 7.2 네 기능에 넘길 자료

- 도면·래더 비교: PV02고유원본·핀·주소·알람/전이·OEM5페이지와공유경계FG21·시공PDF24/55·P&ID를연결한다.
- 백업·선택 복원: PV02/P07키와다른설비키를이름만으로병합하지않는다. 원초안·이전값·미지필드·사용자편집을보존한다. 구현/동작검사는Codex담당이다.
- 기록 전후 비교: 요청/허용/출력/입력/MEM/HMI/실물상태를분리하여기록할수있게한다. 실제관찰0을완료증거로쓰지않는다.
- 보고서/PDF: 원본판본·핵심근거·미확정·관찰자료를구분해출력한다. A4가독성/페이지/링크와저장된내용일치는통합후검증한다.

기능이PV02에이미구현·통과했다고표시하지않으며다른설비의항목수·회로수·테스트수를복사하지않는다.

### 7.3 Codex의 좁은 재확인 목록

1. 0280의MC04raw/Inputs/**Allarm**Maintenance OR,NOT_OPEN두알람,허용탈락Reset를확인한다.
2. 0283의양쪽3입력OR와M80.6,OFF가지없음을확인한다.
3. 0281의300ms/800ms와T8~11,1/4MEM_OPEN,0284가변체류미확정을유지한다.
4. 0288/0289raw·Inputs병렬과startupS303/305,0451/0452의7초4알람을확인한다.
5. 0237의DB2Maintenance→DB3Maintenance와M80.6를분리한다. 예열17 **R462**/생산27 **S805**,RD01·팬의3중NOT경계를반영한다.
6. 0397 IW0/8/10전달·0030ENO/NOT Simulation호출과현재CPU미확정을분리한다.
7. 0392의FALSE3개와미결속17개,HMI설정주소/이벤트경계를유지한다. 필요하면이호출의실인수Export만추가확보한다.
8. 도면개정란을페이지별유지하고PDF24/55의No./CORE상충·EV03소유·추가LS의미확정을보존한다.

### 7.4 누락 자료

- **U01 현재CPU/실물:** 현재프로젝트·다운로드/변경이력·설비표찰이없어백업동일성미확정.
- **U02 정상극성/밸브복귀:** 센서정상상태·스풀/실린더형식·정전/공압상실동작·현행보호설정자료필요.
- **U03 가변체류:** KF_KT본문·SEC=0정의·허용범위·현재PV02A/B및변환Word·설정이력필요.
- **U04 HMI결속:** 0392의17실인수·MotorsDB11멤버·객체이벤트·쓰기방식필요.
- **U05 제어작성자:** M80.6와공통모드/Enable/Inputs의전체교차참조·실행순서·현재값필요.
- **U06 시공상충:** PDF24/55No.와25G/26표기개정본·OEM X1↔ROT1TB1심선표·LS27/28/31/32실제역할필요.
- **U07 현장복구:** 원인·관찰·조치·회복및승인된재가동근거필요. 문서검토로대체불가.

| 구분 | 상태 |
| --- | --- |
| documentation | 1차초안작성 |
| static_review | 지정원본/선언/핀·PDF정적대조수행,미확보분리 |
| ui_records | 미실행,사용자/Codex담당 |
| publication | PV02초안미게시 |
| tia_compile | not_performed |
| live_cpu | not_performed |
| field_recovery | not_performed |

이번 산출물은 PV02 한 개다. 승인 순서상 다음은 MV01(P19)이지만 이 초안에서 착수하거나 다른 설비를 합치지 않는다. 2차133후보는 제외한다.

## 부록 A 핵심 근거표

해시와 고정 공개 URL은 부록 C에 있다. 각 행의 정적 해석과 미확정 경계를 함께 보존한다. 소스 번호는 §1.3의 전체 경로 축약이다.

| ID | 주장 | 원본 위치와 핀·선언 | 해석 및 미확정 경계 |
| --- | --- | --- | --- |
| E01 | P07↔PV02 | docs/equipment-standard/INVENTORY.json priority P07/catalog PV02 | tag대응,identity_verified=false. 현장 본체·소유 미확정 |
| E02 | 입력6/출력2의 백업 주소 | 0607 RID135/137/140/142 Input AO76~79,RID79/81 AO80/81,RID85/84 Output AO44/45;0282/0283/0288/0289 | I9.4~9.7,I10.0/.1,Q5.4/.5. 과거 주석 주소 및 추가LS와 분리 |
| E03 | 내부 요청·메모리·DB 주소 | 0607 RID57/61~64/80/82/83;0609 RID52/55/56/58/60/76/109/113/114/136/138/139/141/143/144;0608 TOD | ON은 Memory,계산 주소는 백업. M12.3/.4와 Flag DB기억을 동일시하지 않음 |
| E04 | MC04/처리응답/유지보수 OR 허용 | 0280 LAD1916 NID5 Contact524,526/22/29→OR443(W527/24/31),530/532/534와536/538/540→OR450,Coil456/458(W511/512/513);0607RID51,0609RID87/156 | rawMC04 필수 단독조건 아님;NOT_OPEN두개와 Enable반전가지 보존. 현재 모드 미확정 |
| E05 | 자동 요청·W7 초기화 | 0280 Contact542NOT,W515/ORef492→W543 Move466/R471/474/477/480;W516/517/ORef493/494,0609RID60/0610상수0 | ON·!GateON일 때 auto01 Reset,W7=0. local00/M80.6까지 해제라고 확장 금지 |
| E06 | 현장 I10.0/.1→00 요청 | 0282 LAD1919 NID7 Contact704/706/708,Coil686/690;W697/699/700/702,ORef692~695→0607RID79~82 | 현장 요청과 위치/HMI명령은 별도. 실제 selector 상태 미확정 |
| E07 | 최종 양쪽3입력 OR | 0283 LAD1920 NID8 Contact748→W749;750/752/754→OR713→W738 Coil717/W740 ORef729;756/758/760→OR720→W744 Coil724/W746 ORef733 | local/auto/M80.6. OFF가지 없음. Q0는 닫힘완료 아님 |
| E08 | 0~5 순서와300/800ms | 0281 LAD1918 NID6 SD683/717/739/773,Move688/706/722/744/762/778;0610RID65/72 UID788/811;0607RID66/70/73/77 | T8~11,State0/3 고정지연,State1/4 MEM_OPEN,State2/5가변. 닫힘센서 직렬전이 없음;현장시간 미검증 |
| E09 | A/B 가변체류 KF_KT | 0284 LAD1917 NID9 CRef23/32 CodeBlock22/31;0060RID121,0061RID122;W25/27/29/33/34/36/38,0609RID109/114/113/76,0610RID150 | KF Int→KT Word 핀 결속. 함수본문/단위/현재값 미확보 |
| E10 | A MEM S/R | 0288 LAD1923 NID13 Parts21~35,W49~73;ORef38/44→0607RID135/137,ORef39/45→0609RID136/138,40/42/46/48→RID55/139 | raw OR Inputs와Q방향별래치. 센서순간값과기억분리 |
| E11 | B MEM S/R | 0289 LAD1924 NID14 Parts21~35,W49~73/82~91;ORef38/44→0607RID140/142,39/45→0609RID141/143,40/42/46/48→RID56/144 | raw OR Inputs. 추가false AND close가지없음. 현재값 미확정 |
| E12 | startup 닫힘기억 Set | 0150 LAD405 NID5 Contact326→W327→S303/305;W320/321 ORef314/315→0563RID49/50 AO68/70 | 시작시기억설정은 실물닫힘 확인 아님 |
| E13 | A NOT_OPEN 7초 | 0451 LAD1817 NID44 SD1581/S1587/R1592;W1632/1633/1637/1642;0656RID320,0658RID184 T107,0657RID185 DB3X10.5 | !MEM_OPEN감시,원인/현재보호값 미확정 |
| E14 | A NOT_CLOSE 7초 | 0451 SD1599/S1605/R1610;W1644/1645/1649/1654;0656RID320,0658RID186 T108,0657RID187 DB3X10.6 | !Q·!MEM_CLOSE감시,출력0과닫힘상태 분리 |
| E15 | B NOT_OPEN 7초 | 0452 LAD1818 NID45 SD1645/S1651/R1656;W1696/1697/1701/1706;0656RID320,0658RID188 T109,0657RID189 DB3X10.7 | 고유7초와위치기억;센서직접원인확정 금지 |
| E16 | B NOT_CLOSE 7초 | 0452 SD1663/S1669/R1674;W1708/1709/1713/1718;0656RID320,0658RID190 T110,0657RID191 DB3X11.0 | 네번째알람의바이트경계유지. 현재값/복구 미확정 |
| E17 | 개별Reset와공통요청 | 0451 R1592/1610,0452 R1656/1674;0158 LAD930 NID9 OR28→W38 S33/R40,W36/ORef37,W42/ORef43→0565 | ON·RESET·자기알람. HMI요청해제와현장복구는별개 |
| E18 | 세 유지보수 변수 구분 | 0237 LAD1930 NID1 Contact47/49→W50 Coil34/36;0602RID4,0603 TOD2/3,0604RID3/6;0280ORef30→0609RID156;0283ORef728/732→0607RID83 | DB2Flag→DB3Allarm 공통쓰기 확인. M80.6작성자 미확보 |
| E19 | Enable 예열Reset/생산Set | 0164 LAD1843 NID3 Eq452→W705 R462,W709/ORef617;0165 LAD1844 NID4 Eq802→W1065 S805,W1067/ORef965;0577RID34,0578RID30=17/RID82=27 | 조건 및S/R보존. 초단위/전체쓰기우선권 미확정 |
| E20 | R2loop와RD01·팬 Reset | 0243 LAD1936 NID7 NOT278/280/35→OR28.in5→R236;0245 LAD1939 NID9 NOT311/313/318→OR278.in2→R283;0604RID46/11,0602RID4 | loop·standby·underTesting의3중NOT가지. 실제전체정지나재가동 보장 아님 |
| E21 | HMI20핀·설정8개·과거화면 | 0392 LAD1216 CRef22/CodeBlock23→0624RID716/0623RID715 NID40;0626RID48 UID34~36 FALSE;0400/0631;hmi_plc_tags.csv,assets/HMI_DECOATER.png | FALSE3결속/17미결속. DB11X78.x설정과실인수·현재화면분리 |
| E22 | IW0/8/10→Inputs와호출 | 0397 LAD1070 Move22/43/44,W23/24/55/57/58/59;0627RID3/15/17,0629RID5/16/18,0628RID4 TOD13;0030 LAD1613 NID19 W32/33/42/44/43 Contact37NOT,CRef28 | MC04·PV02입력 포함범위. ENO/NOT Simulation경계와현재CPU미확정을같이표시 |
| E23 | EV04/05 출력회로 | Electrical_Rev2.pdf FG71/PDF72,FG141/PDF142;71KA1/2,A1/A2,접점1/9,X1/141~144,MOD15단자15/16 | DC릴레이와110VAC부하분리. FG71공란/141Rev2. 실제정격·복귀미확정 |
| E24 | 위치4·현장요청2 회로 | 같은PDF FG72/PDF73,X1/145~155,LS25/26/29/30,72SB1/SA1;FG125/PDF126 단자15~18,FG126/PDF127 단자21/22 | FG72/125공란,126Rev2. 접점심벌로정상극성확정 금지 |
| E25 | 시공No./CORE 상충 | Electrical_Can_Decoating_20241118.pdf PDF24/55,LS25/26 No.5_3/4 대5_4/5,ROT1TB1A CORE26대25G;행5_1~15 | 전체ID/FROM/TO유지. 개별심선·추가LS·승인준공미확정 |
| E26 | 공압묶음 및 EV03 별도소유 | PID_1684n002I.pdf PDF1 PV02Detail EV04/05·CL05~08·LS25/26/29/30;Electrical_Rev2.pdf FG21/PDF22 RD01 LUBRIFICATION VALVE | EV03은RD01윤활,PV02세번째밸브아님. 실제공압복귀/기계동일성미확정 |
| E27 | 기존결과·미확정 보존 | all-in-one/devices,control-specs,alarm-guides,circuit-guides,signal-guides,construction-guides,procedures의PV02.html | 각기존페이지보존,현장미확정삭제안함. 새로운UI/기록/게시완료실적아님 |

## 부록 B PV02 HMI 호출 핀 장부

0392-FlgNet.xml CRef22,0623/0624의 원본 NID40. 검색색인 순서에 따른 임의 실인수 연결을 하지 않는다. “미결속”은 원본 실인수 식별 선언이 확보되지 않은 구간이다.

| 핀 | 방향 | Wire | ORef UID | RefId | 상태 |
| --- | --- | --- | --- | --- | --- |
| GateA_Open | 입력 | 45 | 24 | 734 | 미결속, 해당 실인수 Export 필요 |
| GateA_Close | 입력 | 46 | 25 | 735 | 미결속, 해당 실인수 Export 필요 |
| GateB_Open | 입력 | 47 | 26 | 736 | 미결속, 해당 실인수 Export 필요 |
| GateB_Close | 입력 | 48 | 27 | 737 | 미결속, 해당 실인수 Export 필요 |
| Selector_GateA | 입력 | 49 | 28 | 738 | 미결속, 해당 실인수 Export 필요 |
| Selector_GateB | 입력 | 50 | 29 | 739 | 미결속, 해당 실인수 Export 필요 |
| Allarm1 | 입력 | 51 | 30 | 740 | 미결속, 해당 실인수 Export 필요 |
| Allarm2 | 입력 | 52 | 31 | 741 | 미결속, 해당 실인수 Export 필요 |
| Allarm3 | 입력 | 53 | 32 | 742 | 미결속, 해당 실인수 Export 필요 |
| Allarm4 | 입력 | 54 | 33 | 743 | 미결속, 해당 실인수 Export 필요 |
| Allarm5 | 입력 | 55 | 34 | 48 | 0626 RID48 NID40 FALSE |
| Allarm6 | 입력 | 56 | 35 | 48 | 0626 RID48 NID40 FALSE |
| Allarm7 | 입력 | 57 | 36 | 48 | 0626 RID48 NID40 FALSE |
| HMI_GateA_Open | 출력 | 58 | 37 | 744 | 미결속, 해당 실인수 Export 필요 |
| HMI_GateA_Close | 출력 | 59 | 38 | 745 | 미결속, 해당 실인수 Export 필요 |
| HMI_GateB_Open | 출력 | 60 | 39 | 746 | 미결속, 해당 실인수 Export 필요 |
| HMI_GateB_Close | 출력 | 61 | 40 | 747 | 미결속, 해당 실인수 Export 필요 |
| HMI_Selector_GateA | 출력 | 62 | 41 | 748 | 미결속, 해당 실인수 Export 필요 |
| HMI_Selector_GateB | 출력 | 63 | 42 | 749 | 미결속, 해당 실인수 Export 필요 |
| Total_Allarms | 출력 | 64 | 43 | 750 | 미결속, 해당 실인수 Export 필요 |

공통0400의 위치 전달은 Contact22→Coil23(W49),24→25(W52),69→70(W79),71→72(W82),Selector26→27(W55),84→85(W90)이다. Allarm1~7은 OR33→W67→Coil34 Total_Allarms(W68/ORef46)로 모인다. 0631 LocalAccess 결속은 공통 함수의 역할 근거이며0392의17실인수를 대신 확정하지 않는다.

## 부록 C 고정 원본 경로와 SHA256

고정 커밋5fac25b70389f38141774d35dce49f129eb1982f의 공개 원본 파일이다. 해시는 조사에 사용하거나 보존 기준으로 삼은 파일 바이트의 SHA256이며 현장CPU프로젝트의동일성 증거가 아니다. 이전 설비의 수량을 복사하지 않고 아래 실제 파일목록으로 계산했다.

원본·보존 기준 파일 **65개**.

| 원본 경로 | SHA256 |
| --- | --- |
| [.agents/skills/gme-equipment-rollout/SKILL.md](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/.agents/skills/gme-equipment-rollout/SKILL.md) | fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b |
| [docs/equipment-standard/WORK-STANDARD.md](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/docs/equipment-standard/WORK-STANDARD.md) | 05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99 |
| [docs/equipment-standard/WORK-ITEM-TEMPLATE.md](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/docs/equipment-standard/WORK-ITEM-TEMPLATE.md) | 4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586 |
| [docs/equipment-standard/INVENTORY.json](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/docs/equipment-standard/INVENTORY.json) | 720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc |
| [all-in-one/sources/decoded-original/0030-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/sources/decoded-original/0030-FlgNet.xml) | 9252c9da764993de1edb8b2e44c46d6e9f9d4b6118e751a0dbeaa9ffd8ea721b |
| [all-in-one/sources/decoded-original/0150-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/sources/decoded-original/0150-FlgNet.xml) | 829ca4aa3bd2bb6ee406f7f204add2987ec6159ef0fd6dd3dfc075592664a98e |
| [all-in-one/sources/decoded-original/0158-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/sources/decoded-original/0158-FlgNet.xml) | d3f3adebc3d990b85c5d4c294906ae3bc3dafebb49d25b030bf9cc2ccf905651 |
| [all-in-one/sources/decoded-original/0164-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/sources/decoded-original/0164-FlgNet.xml) | 15884b2b362842279b626b669a484b1daa269f5ecd99112b8391bb0387382491 |
| [all-in-one/sources/decoded-original/0165-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/sources/decoded-original/0165-FlgNet.xml) | 4513a5f6e77717c99c5e869105483be31f7f62ab280e271dc36cd7a2d3e3bb88 |
| [all-in-one/sources/decoded-original/0237-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/sources/decoded-original/0237-FlgNet.xml) | ad3721660c2f357e76c1a351f7898691271f35c341efe775e5780d749b2c4aa0 |
| [all-in-one/sources/decoded-original/0243-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/sources/decoded-original/0243-FlgNet.xml) | 4b3a77029b4d5901ff40f260d54189748e7697bb6077fca502165fa7cd5ea3b5 |
| [all-in-one/sources/decoded-original/0245-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/sources/decoded-original/0245-FlgNet.xml) | c89543f2a25028652f425fc8979bae3cde56cdcf8022b81beaadd49ab568abb6 |
| [all-in-one/sources/decoded-original/0280-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/sources/decoded-original/0280-FlgNet.xml) | 77f1860b8424319efcd8fa058eac4177fb6ba24d84d01d690c0e3c361a19f3ca |
| [all-in-one/sources/decoded-original/0281-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/sources/decoded-original/0281-FlgNet.xml) | aea69c322085151c21d95d7ac9d546f16ff7d27b2bace6d3ccdee326d07afcfb |
| [all-in-one/sources/decoded-original/0282-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/sources/decoded-original/0282-FlgNet.xml) | 2c76845365dbd235b7a8f8a1f17afd9bb7038a0ac6bdd7eedafb019e0913fd01 |
| [all-in-one/sources/decoded-original/0283-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/sources/decoded-original/0283-FlgNet.xml) | ab46cabcba6cbf8155c47075a66a1573d9f12e01de1f2faccc0eb8ed2cb69cc3 |
| [all-in-one/sources/decoded-original/0284-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/sources/decoded-original/0284-FlgNet.xml) | 5b073cab59c95093e1b0a9d0006f945e40d4c9aabcd05d03a4055b9d8b3d6607 |
| [all-in-one/sources/decoded-original/0288-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/sources/decoded-original/0288-FlgNet.xml) | af4d15dcde4680ef5b788f88f198a47886857c8db7f7d9b550276fb5eea3c90e |
| [all-in-one/sources/decoded-original/0289-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/sources/decoded-original/0289-FlgNet.xml) | 5460dc0d52bafeeaee0cfd2d66476f7df582002f05a6a17fb4a0928b7e750165 |
| [all-in-one/sources/decoded-original/0392-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/sources/decoded-original/0392-FlgNet.xml) | 067f6e3c2e5b4edd9c0cdb35734036534b3e2896dc51933c31300faaa6c60742 |
| [all-in-one/sources/decoded-original/0397-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/sources/decoded-original/0397-FlgNet.xml) | bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834 |
| [all-in-one/sources/decoded-original/0400-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/sources/decoded-original/0400-FlgNet.xml) | e2aa1de29bf6f95b0b2a79c3e8510a086e6d6c6990f3954cfc09f06211340d94 |
| [all-in-one/sources/decoded-original/0451-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/sources/decoded-original/0451-FlgNet.xml) | 8aeb19ab590824f4b357817cda08b46f962cec4eab5d967dcb0d829d44ca71e5 |
| [all-in-one/sources/decoded-original/0452-FlgNet.xml](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/sources/decoded-original/0452-FlgNet.xml) | 9612aa97393d5039ea2e0601602a924d52688e89f2d18e507eb51bfa961185e4 |
| [all-in-one/sources/decoded-original/0060-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/sources/decoded-original/0060-IdentXmlPart.xml) | d61344a049baa2ce8a97335cd94e6c1753f8f8b7180d3def74d8631ff2cf21b9 |
| [all-in-one/sources/decoded-original/0061-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/sources/decoded-original/0061-IdentXmlPart.xml) | 0861f9e3686b911262b7b7e108c51fc9fed9cb7080c72bcc4b3aae60750af1c7 |
| [all-in-one/sources/decoded-original/0563-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/sources/decoded-original/0563-IdentXmlPart.xml) | 86cf35b6baebc079cb5a092baf53ec3364c377ea7318eb263ab69c8b4550b4ad |
| [all-in-one/sources/decoded-original/0565-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/sources/decoded-original/0565-IdentXmlPart.xml) | 0f7f970faa6c456f2bb032b1a2072a2f52db1e03fc77bd8d35d4583deeaf1149 |
| [all-in-one/sources/decoded-original/0575-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/sources/decoded-original/0575-IdentXmlPart.xml) | 40e7b2caf89ab7f1ed9075547a7728bd02441e24451bdd8bf97c843637daad06 |
| [all-in-one/sources/decoded-original/0577-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/sources/decoded-original/0577-IdentXmlPart.xml) | 511e01fae619dc385357908a1ac62030dbdfd5f5399bd4c22bc58bebbfc3bf47 |
| [all-in-one/sources/decoded-original/0578-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/sources/decoded-original/0578-IdentXmlPart.xml) | 0f9f41b5dee25ea17c7a29ab6f7b00503c13d0f265266acd660072baf061d32b |
| [all-in-one/sources/decoded-original/0602-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/sources/decoded-original/0602-IdentXmlPart.xml) | 46ab21151eddaaf616469db520730c60423eb742aa491af194e6710c751b4caf |
| [all-in-one/sources/decoded-original/0603-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/sources/decoded-original/0603-IdentXmlPart.xml) | e93969dfa281d75b49b24127793068e33472dadb19729c1c48fc4a8dad075ef8 |
| [all-in-one/sources/decoded-original/0604-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/sources/decoded-original/0604-IdentXmlPart.xml) | b798d29c5499b5314a1ee3cff9139dae64c887533b86baa43b6e9a052373a6af |
| [all-in-one/sources/decoded-original/0607-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/sources/decoded-original/0607-IdentXmlPart.xml) | 9b76b53536a26e7b45961fecbf825ae1552e16c2fd9af5736864193c01d77f93 |
| [all-in-one/sources/decoded-original/0608-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/sources/decoded-original/0608-IdentXmlPart.xml) | 24adec2035b65c0c310d637bcea74374896875b6465a16aa2f2cfc8fd55fa4b8 |
| [all-in-one/sources/decoded-original/0609-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/sources/decoded-original/0609-IdentXmlPart.xml) | 395de8ebb2168848cf96fe015bd7334d71107c114a4e441ef36346b8f22031db |
| [all-in-one/sources/decoded-original/0610-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/sources/decoded-original/0610-IdentXmlPart.xml) | c58d07b1b9707dc8c6c2f06c34ee6142f72238a4cf3f376bee8502d1a9532f9d |
| [all-in-one/sources/decoded-original/0623-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/sources/decoded-original/0623-IdentXmlPart.xml) | 4acd00406ea92466169e57e59fc90b0da4d9ec55fd19e2e96c9556e939cb83a6 |
| [all-in-one/sources/decoded-original/0624-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/sources/decoded-original/0624-IdentXmlPart.xml) | 24607c0827fbde428bccf8637ef4ae490798a69a7c2f3b87861d0749082d367a |
| [all-in-one/sources/decoded-original/0626-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/sources/decoded-original/0626-IdentXmlPart.xml) | a9d7fbea345eca70325a8c2e44058c23e96add1b7207eabbb09445118b18188b |
| [all-in-one/sources/decoded-original/0627-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/sources/decoded-original/0627-IdentXmlPart.xml) | 08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb |
| [all-in-one/sources/decoded-original/0628-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/sources/decoded-original/0628-IdentXmlPart.xml) | 9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd |
| [all-in-one/sources/decoded-original/0629-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/sources/decoded-original/0629-IdentXmlPart.xml) | 67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972 |
| [all-in-one/sources/decoded-original/0631-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/sources/decoded-original/0631-IdentXmlPart.xml) | 8e5072374f8ef098de72fbf93965b2a7bb0965c0f803e397daa68588c0c38555 |
| [all-in-one/sources/decoded-original/0656-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/sources/decoded-original/0656-IdentXmlPart.xml) | 0dbc45e84732a8848f17b094ea08ab8578dbf240bfe15cd7086859395c27c592 |
| [all-in-one/sources/decoded-original/0657-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/sources/decoded-original/0657-IdentXmlPart.xml) | 0f70cda60a6b1a17175876d58e25b2686952642de6cffb21213aeef8b347a22b |
| [all-in-one/sources/decoded-original/0658-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/sources/decoded-original/0658-IdentXmlPart.xml) | 998294c0c8a99e00ceb33c2c60def2cd4850e34328917ae506244c2be2df3831 |
| [all-in-one/sources/decoded-original/0688-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/sources/decoded-original/0688-IdentXmlPart.xml) | ceb132457588eb1d4f7c6883240995ac923544aa74467e2686186767c017fcda |
| [all-in-one/sources/decoded-original/0692-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/sources/decoded-original/0692-IdentXmlPart.xml) | bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037 |
| [all-in-one/sources/decoded-original/0694-IdentXmlPart.xml](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/sources/decoded-original/0694-IdentXmlPart.xml) | 757ccebdf32d0a168dd787bfa735fe6494eac4c4a9f7a5adc63898a88e8b152d |
| [all-in-one/sources/decoded-original/network-map.json](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/sources/decoded-original/network-map.json) | c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60 |
| [all-in-one/sources/source-manifest.json](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/sources/source-manifest.json) | 5af6e85994536897fd92f75972534a691e6eb0f067aafe07679c0788fd84e5bf |
| [all-in-one/sources/Electrical_Rev2.pdf](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/sources/Electrical_Rev2.pdf) | 5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6 |
| [all-in-one/sources/Electrical_Can_Decoating_20241118.pdf](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/sources/Electrical_Can_Decoating_20241118.pdf) | 3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd |
| [all-in-one/sources/PID_1684n002I.pdf](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/sources/PID_1684n002I.pdf) | 2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b |
| [all-in-one/sources/hmi_plc_tags.csv](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/sources/hmi_plc_tags.csv) | a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404 |
| [all-in-one/assets/HMI_DECOATER.png](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/assets/HMI_DECOATER.png) | b84b888a2df87d23b514aeb790d2fc51f31c3b20486061a365380b28986f49af |
| [all-in-one/devices/PV02.html](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/devices/PV02.html) | dd4dec17608f34c8de0905d6b57617502e3637c84cef54fa54066680ef7d449a |
| [all-in-one/control-specs/PV02.html](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/control-specs/PV02.html) | 33860d0ee386782029e33def86a88f2c0fd9b2a2508a59a7eaf20e9df5033998 |
| [all-in-one/alarm-guides/PV02.html](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/alarm-guides/PV02.html) | 5c738e22195a5cd81cfdb7feea8ae591700353d0813503b11858a78ef4853e93 |
| [all-in-one/circuit-guides/PV02.html](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/circuit-guides/PV02.html) | b52eb4aa20dfe72fef32435cb0ea761951b11b749735cd1d3e9fc6e7b8175334 |
| [all-in-one/signal-guides/PV02.html](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/signal-guides/PV02.html) | 6b6e62ead9f20e464a88cbf95b55a1bf6e15fa2528f16bd22dc8e0cc01a56fe0 |
| [all-in-one/construction-guides/PV02.html](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/construction-guides/PV02.html) | 2e5ebf6fb17827d21c3f3119576a21cc20a4db6e512efed9b1626e71b00b09c4 |
| [all-in-one/procedures/PV02.html](https://github.com/esp6662266/gme-plc-manual/blob/5fac25b70389f38141774d35dce49f129eb1982f/all-in-one/procedures/PV02.html) | 6704a09b991fcc95f193f0ee8de822a644fdb5a923fe03e4466395c08b17c326 |

## 부록 D 수행 범위와 자체 점검

- 지정 XML·선언을 읽고 RID/NID/UID·SAD/SSD/BAD/TOD·Part/Wire pin을 대조했다. 시뮬레이터 및 논리 행동시험은 작성·생성·실행하지 않았다.
- OEM FG71/72/125/126/141과 소유경계FG21,시공PDF24/55,P&ID PV02 Detail,저장 HMI 이미지를 실제 렌더로 확인했다.
- 7영역·핵심 근거27개·HMI20핀 및 고정 원본 파일목록·해시를 확인했다. 기존 미확정과 원초안·다른 설비 결과는 보존했다.
- 원본 worktree Git수정 없음. 새 연구 초안만 별도 작성했다. 변경 전후 보호값·현장운영·사용자기록 작성은없다.
- 미실행: TIA compile,현재PLC/현장,시뮬레이터/행동시험,UI/저장·복원/동시성/PDF출력/패키지/배포검사. 통합 후 사용자/Codex의검증을 대체하지 않는다.

