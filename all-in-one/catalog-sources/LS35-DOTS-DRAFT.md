# LS35 — MV06 하위 위치 리미트 스위치 고유 조사

- 대상 LS35 / phase2 / component / parent MV06. INVENTORY catalog[245], TASK3-BATCH25-SCOPE 및 GME-CATALOG-OVERLAP-REVIEW의 parent_child_separate 분류를 확인했다. 부모 완료를 상속하지 않는다.
- 원본 gme-research/source-mv06, 고정 abcf31c5030bc7ef8749ed8e869a857f2387a28a / v1.12.0. 표준 GME-STD-1.0.0. 시작 2026-10-11 14:24 UTC. 실행 모델/추론 설정 UI 증명은 미확인.
- AGENTS, rollout SKILL, WORK-STANDARD, WORK-ITEM-TEMPLATE, INVENTORY, 최신 인계 상단과 source-map/START를 읽었다. MV06/ZT06/LS34는 탐색 색인·공통 근거로만 재사용하고 아래 LS35 고유 경로와 부모 후보의 핵심 가지를 원본에서 독립 대조했다.
- 원본·공통코드·버전·대장·배포·운영·PLC·현장·보호값·SEJIN 변경 없음. 시뮬레이터 작성/수정/생성/실행/행동시험, 생성기/앱빌드, 새 Work/Codex, 업로드·사용자 전송·재위임 없음. 0403은 보존 XML의 다른 쓰기를 읽기만 했다.

## 핵심 결과

LS35는 P&ID의 MV06 위치 스위치 표기이며, 시공도 고유 케이블은 8_20 =FLB+MV06-LS35A, FLO4TB2→LS-35이다. OEM 도면의 닫힘은 LS41/E7.0이다. LS35=LS41 또는 LS35=I7.0을 확정할 대응표는 없다. LS34/35와 LS40/41 네 catalog ID를 유지하지만 독립 실물 네 개로 확정하지도 않는다.

LS35 직접 PLC/HMI 선언은 검색 범위에서 미확보다. 부모의 닫힘 원시 I7.0, 가공 DB13.X7.0, HMI DB11.X28.4, 수동요청 DB2.X10.6은 서로 다른 계층이며 LS35 소유 주소로 재배정하지 않는다. 가공값은 Word 복사 외 보존 XML의 별도 일반 Coil 쓰기가 있고, 제어에서는 양접점 요청 Reset과 NOT 방향허가로 다르게 소비된다.

## 1. 설비·자료 기준 — 적용, 실물 동일성 미확정

all-in-one/sources/PID_1684n002I.pdf 실제1쪽을 렌더하고 MV06 및 title을 확대했다. Overflow valve MV-06 주변에 ZT-06, M14, LS-34, LS-35, 0.25kW 440V가 있다. 도면을 정상 방향으로 읽으면 LS34가 M14 위, LS35가 아래다. 이 배치는 개방/폐쇄 방향의 직접 지정이 아니다. M14 구동모터와 ZT06 연속위치 계측을 LS35 접점과 합치지 않는다.

P&ID 도면번호1684n002/Apex I, 기본일06/04/2011. H 01/08/2012는 MV06 추가/MV03 command instrument 변경, I 15/01/2013은 MC05 제거/FN02 power 변경이다. 현행 설치 증거로 승격하지 않는다.

시공 Electrical_Can_Decoating_20241118.pdf는 실제64쪽이다. 실제33쪽 footer33/64, D-PAGE16, CANDC-CONS-E016-033; 실제58쪽 footer58/64, D-PAGE8, CANDC-CONS-C008-058을 각각 4배 확대 재확인했다. 둘 다 개정1 24.11.11 first draft design이며 준공 확인이 아니다. OEM Electrical_Rev2.pdf FG33/실제34쪽은 기본일27.05.2024, 개정란 공란이다. FG122/실제123 및 FG123/실제124는 기본일27.05.2024, 개정2 17.03.2025다. 파일명 Rev2를 전체 페이지 개정으로 쓰지 않는다.

## 2. I/O·HMI — LS35 직접 결속과 부모 후보 분리

아래 NNNN은 all-in-one/sources/decoded-original/NNNN-FlgNet.xml 또는 명시한 IdentXmlPart.xml이다. RID는 선언문맥 안에서만 유효하다. NID/LAD는 network-map 색인, Part/Wire/ORef/CRef는 실제 XML로 확인했다. 주소는 백업 근거이며 현재 CPU와의 일치 증거가 아니다.

| 계층 | 원본 선언·사용 위치 | 확인과 경계 |
|---|---|---|
|LS35 직접 PLC/HMI|decoded-original XML695개 및 hmi_plc_tags.csv의 LS[._ -]?35 경계검색|문자열 일치0. 간접주소/바이너리/전체 TIA에 신호가 없다고 결론 내리지 않음 |
|부모 raw 닫힘|0678 SimpleAccess RID260 MV06_Close, SAD Input AO56 Bool; NID35 UID1481|I7.0. OEM LS41 경로와 주소상 부합하지만 LS35 실물 연결은 미확정 |
|부모 가공 닫힘|0619 Global RID182, AO56 BAD168;0618 DepDB RID168 Inputs TOD13|DB13.X7.0. NID9 UID844/865 Read |
|부모 가공 열림|0619 RID181 AO55 BAD168|DB13.X6.7. LS35 방향으로 배정하지 않음 |
|부모 닫힘 요청|0619 RID93 AO86 BAD5;0618 RID5 Flag TOD2|DB2.X10.6. NID9 UID841/861 Read,847 Reset Write. 위치 기억/센서가 아님 |
|부모 열림 요청|0619 RID94 AO85 BAD5|DB2.X10.5. 닫힘 요청 해제 조건으로도 읽음 |
|부모 HMI 닫힘 한계|hmi_plc_tags.csv MV_06\\LimitSwitchClose, ID0040B|DB11,X28.4. DB13.X7.0와 다른 주소 |
|부모 HMI 열림 한계|동일 LimitSwitchOpen,0040A|DB11,X28.3. LS35 직접 태그 아님 |
|부모 HMI 요청|Flag_CLOSE0040D / Flag_OPEN0040C|DB2,X10.6 / DB2,X10.5. 버튼 이벤트·현재값·쓰기 권한은 CSV로 입증 불가 |

같은 CSV 부모8행의 나머지는 Allarme1 0040E=DB11,X28.2, OutputClose00312=DB11,X28.1, OutputOpen00046=DB11,X28.0, AutoMan00047=DB2,X6.5다. LS35 전용 MEM_OPEN/CLOSE 기억 비트·독립 센서 진단은 확보하지 못했다.

0364 LAD1187 NID10의 CRef23/RID639, CodeBlock22/RID130은 0624 BlockInterfaceInfo 및0623 FCBlock HMI Standard Motorized Valve FC10 선언과 결속한다. 닫힘 입력핀 Limiti_Switch_Close←W44/ORef45/RID702, 출력핀 Limit_Switch_Close_HMI→W56/ORef57/RID146이다. 열림은 Limit_switch_Open←W42/ORef43/RID703, Limit_Switch_Open_HMI→W54/ORef55/RID144다. 같은 호출문맥 실인수 선언을 끝까지 결속하지 못했으므로 다른 블록의 같은 RID를 가져와 DB13→DB11 전달이나 LS35 화면 소유를 확정하지 않는다.

## 3. 제어 구조 — 정적 부모 후보 가지, LS35 소유 미확정

### 3.1 입력 Word 전달

0397 LAD1070 NID1에서 Powerrail W21→Move42.en, in W52/ORef45/RID13, out1 W54/ORef46/RID14이다. 0627 SimpleAccess RID13 Tag_171 Word Input AO48은 IW6, 0629 Global RID14 Word AO48 BAD4 및0628 DepDB RID4 Inputs TOD13은 DB13.DBW6이다. 즉 IW6→DB13.DBW6 복사이며 해당 Move에 NOT은 없다. I6.7/I7.0는 이 두 바이트에 포함된다. 이 구조를 LS35 입력 직접 결속 또는 현재 원시/가공값 항상 동일하다는 증거로 쓰지 않는다. main 호출 및 순서 전체는 MV06 공통 조사 범위이고 이번에 재검증 완료로 계수하지 않았다.

### 3.2 가공 닫힘 입력의 두 소비

0349 LAD1711 NID9:

- Contact925 양접점 operand W875/ORef844/RID182=Inputs.MV06 Close →W70→OR797.in1. 다른 입력은 Contact927 W876/ORef845/RID94=Flag.MV06_Open→W928/in2, Contact929 W877/ORef846/RID81=MV06_Auto→W930/in3이다. OR797.out W72→RCoil801.in, operand W880/ORef847/RID93=Flag.MV06_Close Reset이다.
- 공통 앞단 Powerrail W967→NOT ON Contact915(operand W27/O28 RID1)→W916→NOT ON Contact917(W21/O22 RID1)→W918이다. 같은0617 SimpleAccess RID1 ON, Memory AO0=M0.0이다. 이름과 부정접점의 긴장을 원문대로 남기며 임의 정상화하지 않는다.
- 닫힘 출력 말단은 OR966.out W908→NOT 반대출력 Contact961(operand W909/ORef864/RID98 Open MV06 Q1.1)→W962→NOT Inputs.MV06 Close Contact963(operand W910/ORef865/RID182)→W964→일반Coil837, operand W912/ORef866/RID97 Close MV06이다. 0617 RID97 Output AO10=Q1.2.
- 따라서 동일 가공 닫힘 비트가 요청Reset 양접점과 출력허가 부정접점에서 다르게 쓰인다. 입력 Word 복사의 반전과 소비 접점 NOT을 혼동하지 않는다. 부모 모드/압력/Shot/고장 등 외곽 제어는 MV06 초안의 공통 범위이며 LS35 고유 제어로 복제하지 않는다. 이 논리만으로 센서 NO/NC, 정상극성, 실제 닫힘, 현재 출력허가를 확정할 수 없다.

### 3.3 다른 쓰기 — 보존된 중지 XML 정적 열람

0403 LAD1083 NID2의 Le634(Int) pre는 Powerrail W21, in1 W97/ORef100/RID327, in2 W98/ORef110/RID254, out W96→일반Coil635.in, operand W688/ORef657/RID242다. 0635 RID327 Pot_MV06 AO1088 BAD247,0634 RID247 Data TOD1은 DB1.DBW136이다. 0637 LiteralConstant RID254=Int2. 0635 RID242 AO56 BAD5 및0634 RID5 Inputs TOD13, UID657 AK=Write로 DB13.X7.0 쓰기를 확인했다. 식 Pot_MV06≤2의 일반 Coil이며 S/R 위치 기억 래치가 아니다.

짝 열림은 Ge632(Int), in1 W92/ORef94 RID327, in2 W93/ORef95 RID253=Int98, out W91→Coil633, operand W684/ORef654 RID243=DB13.X6.7이다. ≥98/≤2는 보존 XML의 정적 비교값으로만 기록한다. 실제 LS35 작동점·단위%·현행 보호설정·실행 중인 블록으로 간주하지 않는다. 전체 간접/외부 Writer의 완전성은 미확정이다. 실행·생성·수정·행동시험을 하지 않았다.

### 3.4 원시 닫힘과 연속위치 경계

0516 LAD1766 NID35 Contact1531은 NOT raw MV06_Close, operand W1504/ORef1481=0678 RID260 I7.0이다. 앞단 EM_OK Contact1529→W1530, out W1532→Coil1441.in 및 Add1446.en이다. 부모 encoder gate 경로에서 읽는 값은 raw I7.0이며 DB13.X7.0가 아니다. ZT06 공통 색인의 SW_GATE4/HSC/환산은 별 소유로 유지한다. 이 원시 소비를 LS35 직접 사용 또는 엔코더가 LS35라는 증거로 쓰지 않는다.

## 4. 전기 끝점 — LS35 직접 시공과 OEM 부모 후보

| 원본 실제쪽/행 | 시작→끝 | 원문·해석 |
|---|---|---|
|시공33 route13 branch2|FLO4TB2→LS-35|Flexible16, device LOC MV-06 TAG LS-35, cable8_20 =FLB+MV06-LS35A, CVV1.0/2 |
|시공58 행8_20|MV-06 FLO4TB2→MV-06 LS-35|DC,CVV,2C,1.0,spare0,E1320,Adjustment3,LEN3 |
|시공58 행8_17|UC-01 FLO4TB1→MV-06 FLO4TB2 LS34/35|=FLB+MV06-FLO4TB2A,DC,CVV,7G,1.0,spare2,Adjustment8,LEN9 |
|시공58 행8_4|CR→UC01 FLO4TB1 LS34/35/17HL1|=FLB+UC01-FLO4TB1A,DC,CVV,9G,1.0,spare2,Adjustment3,LEN54 |
|시공58 행8_6|CR→MV06 FLO4TB2 ZT06|=FLB+MV06-FLO4TB2A,TM,CVV-S,4S,1.0,spare0,Adjustment12,LEN63 |

시공33의 FLO4TB2 중계행 LOC는 UC-01로 인쇄되어 있다. 표기 상충으로 남기고 LS35 부모를 UC01로 바꾸지 않는다. 8_6/8_17 케이블 ID는 같아도 시작점·신호·규격이 다르므로 단일 케이블로 병합하지 않는다. LS34 전용8_19(E1310)와 LS35 전용8_20(E1320), ZT06 전용8_21(E1330)을 구분했다. 검게 가린8_5/7/8을 텍스트 추출만으로 복원·활성경로 취급하지 않는다. LEN/Adjustment는 인쇄 설계값이며 실측이 아니다.

OEM Electrical_Rev2.pdf FG33/실제34에서 닫힘 후보는 +24Vdc10.7→X1/65(5×20,2A F 인쇄)→33.6→LS41 NC11/12→X1/66→E7.0(123/2)이다. 실제124/FG123에서 E7.0 crossref33/7→CPU515 MOD9 단자31, LIMIT SWITCH LS-41 양끝점을 확인했다. 공급모듈 옆의 X21/3009 및123.1은 같은 실제124쪽에 표시되지만 LS35 전용 보호기/퓨즈로 재배정하지 않는다.

열림 후보는 같은 FG33 +24V→X1/63(2A F)→33.5→LS40 NC11/12→X1/64→E6.7(122/7), 실제123/FG122 E6.7 crossref33/5→CPU515 MOD9 단자28, LIMIT SWITCH LS.40이다. NC11/12 기호는 설치된 센서의 정상극성 확인이 아니다.

LS35-8_20-FLO4TB2 내부 단자와 OEM LS41-X1/65~66의 승인 결속표가 없으므로 둘을 연결된 준공회로로 그리지 않는다. LS35 전용 출력·밸브코일·보호값을 만들지 않는다. 부모 공통 M14 전력/인버터 및 EV69KA/71KA 부하5–9 정정은 유지하되 LS35 소유로 복제하지 않는다.

## 5. 알람·복구 — 직접 전용 근거 미확보

LS35 직접 알람번호·미도달 타이머·진단 Set/Reset은 확보하지 못했다. MV06 공통 초안의 MV_06_FAULT DB3.X11.6 및 방향응답/엔코더 편차 알람은 부모 기능으로 유지한다. 이번에 부모 타이머 전체를 반복 의미검토하거나 LS35 고장으로 재분류하지 않았다.

raw 후보I7.0, 가공DB13.X7.0, 요청DB2.X10.6, HMI한계DB11.X28.4, HMI고장DB11.X28.2는 서로 다르다. 요청Reset, 알람소멸, 접점변화, 실제 닫힘/현장복구는 별도 증거가 필요하다. 현재 CPU·정상극성·현장 관찰·복구 기록은 없다.

## 6. 증상별 관찰 — 읽기 전용 자료 수집 기준

| 증상 | 확인할 자료 | 판단 경계 |
|---|---|---|
|LS35와 닫힘표시 불일치|명판·실제 기계위치·승인 LS35↔LS41 대응표, 같은 시각 I7.0/DB13.X7.0/DB11.X28.4|LS35를 I7.0로 먼저 지정하지 않음 |
|원시/가공 불일치|0397 Word복사와0403 다른Write의 현재 호출·순서·프로젝트 식별|백업에 Writer가 있다는 사실만으로 현행 원인 확정 금지 |
|닫힘 요청 소멸|0349 R801의 InputsClose/FlagOpen/Auto 및 두NOT ON 조건 기록|요청 해제를 실제 닫힘 완료로 해석하지 않음 |
|닫힘 출력 제한|NOT Q1.1/NOT InputsClose 및 외곽 허가의 읽기 기록|접점우회·출력강제·시험운전·보호설정 변경 없음 |
|케이블 식별 불명|8_20 표찰,FLO4TB2 내부 승인 단자표,8_6/17 중복ID 정정|이름만으로 결선·교체 지시하지 않음 |
|복구 확인 요청|권한있는 관찰자의 시각/시간대·실제위치·전후신호·현재프로젝트 근거|알람없음/문서검사만으로 복구완료 불가 |

현장 관찰은 수행하지 않았다. 이 표는 자료 요청 기준이며 센서 조작·운전/행동시험 지시가 아니다.

## 7. 완료·누락·인계

| 영역 | 상태 | 부족 자료 |
|---|---|---|
|설비·자료 기준|적용/정적 문서|LS35 실물/설치 및 LS40/41 대응 |
|IO/HMI|부모 후보 적용,직접 미확보|현재 입력표·TIA·HMI 실인수/이벤트 |
|제어 구조|입력전달·소비·다른쓰기 정적검토|현재 호출순서·전체 간접쓰기·CPU 일치 |
|전기 끝점|직접 시공/부모 OEM 후보 적용|FLO4TB2 준공 단자표·표찰·정상극성 |
|알람·복구|독립 근거 미확보|LS35 직접진단 여부·현장복구 기록 |
|증상 관찰|적용/자료 수집 기준|현재 관찰값 없음 |
|완료 기준|complete_with_gaps 초안|통합자 독립검토 필요 |

도면·래더 비교용 근거는 마련했다. 백업·선택복원, 기록 전후비교, 보고서/PDF 및 비교UI는 미구현/미검증이며 BC01 동등 구현완료가 아니다. documentation=complete_with_gaps; static_review=own_static_review_completed; ui_records=not_run; publication=not_published; tia_compile/live_cpu/field_recovery=not_performed. 원본 preflight/회귀/생성기/앱빌드는 이번 읽기 전용 범위에서 실행하지 않았다.

다음 필요한 자료는 LS34/35↔LS40/41 승인 대응표, FLO4TB2 현재 단자·케이블표, 현재 CPU/프로젝트 일치, HMI 미결속 실인수 선언과 정상극성·실제위치 기록이다. 새 자료 없는 식별 보류9개는 다시 검색하지 않았다. 부모 전체 재조사·ID 병합·4실물 확정 없이 인계한다.

## 부록 A. 선정 원본 SHA256 / 고정 Git blob 바이트 대조

선정 34파일 전체다. 경로는 source-mv06 기준이며 해시검사 수와 의미검토 수는 다르다.

|원본경로|SHA256|고정 Git blob|바이트일치|
|---|---|---|---|
|`AGENTS.md`|`0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2`|`073164bc6efd5791032d62c71b03b4dab48cb6f8`|True|
|`.agents/skills/gme-equipment-rollout/SKILL.md`|`fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b`|`9aa820ea6ca15b4e136c9772423b78ed4df6a3d4`|True|
|`.agents/skills/gme-equipment-rollout/references/source-map.md`|`40612c5efb8f94608840c7bc0e9095ea840df54920861c388ae48ea34c7998dc`|`49e50a7a8e56a16e2ec7f3607a03fd90adb8f1d3`|True|
|`docs/equipment-standard/WORK-STANDARD.md`|`05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99`|`f76a570cc73098632e08759b17934000f7e3a253`|True|
|`docs/equipment-standard/WORK-ITEM-TEMPLATE.md`|`4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586`|`e546f39535d2b589e80f97db869ac37ce4d05cfd`|True|
|`docs/equipment-standard/START-GPT61.md`|`35769e3146ccd707fea2b81b67b30376b76a0a19c7e662fe2bb4fdd382306f94`|`0d08cab3678df7e2625251b641b138ef4956483b`|True|
|`docs/equipment-standard/INVENTORY.json`|`720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc`|`587c3748ad9224718f95ba06463fee913dae231d`|True|
|`VERSION.json`|`5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7`|`fffb51663b7705aec91cb119ca80ee943a4ce758`|True|
|`WORKSPACE-HANDOFF.md`|`215096d997782e78e901dfae36c782937e49611fbeb677a0d3fa50cbecf8d074`|`dd0b8989d2376c4415bba9bd826fe6754c6b1a12`|True|
|`PUBLICATION_STATUS.md`|`efe4857aec598d90470322cf3962eb3fe1f64947630e1fdf71d1c90134de8740`|`d76401cf291fc0be681acc51fa898ad3ce46ff78`|True|
|`EXPANSION-WORK.md`|`ec624de9fd2fcfac861a67fd5e828b25ef46db50bfd7a37ff16e2cb54cd0f7e2`|`4c42d88ecc2d48269eb23e13a20ebf3721a092a1`|True|
|`all-in-one/ACTIVE-WORK.md`|`eff3bbc08ecff41da3beff77f3fec48e7d148708192bcaaab00f34b6a721afc2`|`6eb947c629b5ddf9c759ef87649451303938864b`|True|
|`all-in-one/sources/Electrical_Rev2.pdf`|`5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6`|`f610fd7c7ce14ae951b00cff57b969259bfb389d`|True|
|`all-in-one/sources/Electrical_Can_Decoating_20241118.pdf`|`3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd`|`0ee6b6f8361c5790864dbba4bbd9d55e8e7c08f8`|True|
|`all-in-one/sources/PID_1684n002I.pdf`|`2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b`|`8c83a59fefd5b8b651ec3537ea4236a073f5e109`|True|
|`all-in-one/sources/hmi_plc_tags.csv`|`a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404`|`cf4c0650e7c7baac350dcb89909b808435704880`|True|
|`all-in-one/sources/decoded-original/network-map.json`|`c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60`|`424430b6b953e43138e5d0a18ca40c949e21cfa1`|True|
|`all-in-one/sources/decoded-original/0349-FlgNet.xml`|`2f45af21543189d83f027afbae797532cae5d55935bac1fba3913825d741863b`|`7082fb0a8817f254ae1ac0087990478f2de30791`|True|
|`all-in-one/sources/decoded-original/0397-FlgNet.xml`|`bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834`|`4ab8370493c4e28fc1eabeeebe2743d27f0c4021`|True|
|`all-in-one/sources/decoded-original/0364-FlgNet.xml`|`c23a9952251a48105eedd1ed3c185f781b6163d094fb3bb396ac27415587de8a`|`dee7f6d4c8d0675deb1c4bb5c5eb78392ae43c57`|True|
|`all-in-one/sources/decoded-original/0403-FlgNet.xml`|`77b03e38aa857ac8dd404f2f66a56256939b4e7924b41334a7981b86089c1e6b`|`4c806e31eb65f00cbb7870c72896ac26a8bc3dd3`|True|
|`all-in-one/sources/decoded-original/0516-FlgNet.xml`|`382738875d4fe8ebcf38f878eafd6486047e3cdd6de7a98bebcafc2afd124c8f`|`06030b0a2ec9e27ee53298e46584373ec92ab97b`|True|
|`all-in-one/sources/decoded-original/0617-IdentXmlPart.xml`|`10bcf85169cb2512f55acadaef299a3d46b4b4cecd88032d739cfeba23e94aa9`|`9527658ee6808be34bd513b1b2ebaf3a4a5a6f3e`|True|
|`all-in-one/sources/decoded-original/0618-IdentXmlPart.xml`|`0c6762de9cdf0e294317f7463bea3d8e6df5673d333d9b1826ebd17a7ded044c`|`9eec0dbd8abde4aa7295f77b63ad473f895f274b`|True|
|`all-in-one/sources/decoded-original/0619-IdentXmlPart.xml`|`85694bb5b696e31e6a1217431112e5b750516c4f94078d6e127d4394a8b80456`|`11f0502c84a1f319a21459a35c0dc1c6ce8e8f36`|True|
|`all-in-one/sources/decoded-original/0623-IdentXmlPart.xml`|`4acd00406ea92466169e57e59fc90b0da4d9ec55fd19e2e96c9556e939cb83a6`|`13b3af0459c8e6069bb9b2f1b16454bf479e08dc`|True|
|`all-in-one/sources/decoded-original/0624-IdentXmlPart.xml`|`24607c0827fbde428bccf8637ef4ae490798a69a7c2f3b87861d0749082d367a`|`02511fea47fc47981c101bba49dc40adde1cdcc3`|True|
|`all-in-one/sources/decoded-original/0627-IdentXmlPart.xml`|`08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb`|`61ebc0abbb2ca160e11e1da400a3f14a397d8bc5`|True|
|`all-in-one/sources/decoded-original/0628-IdentXmlPart.xml`|`9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd`|`170ca5c72599edc7ea7eefe651c3680ce325e76a`|True|
|`all-in-one/sources/decoded-original/0629-IdentXmlPart.xml`|`67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972`|`058129bb01e27f7a6a0d0293f332d745e5bab74e`|True|
|`all-in-one/sources/decoded-original/0634-IdentXmlPart.xml`|`af3fcb536a6270ffb9a19e5b3f2c284a38d67d465f5147961005c1c01d11299d`|`877d9e0734dc7f3e5a8cea789eeb58a208501f48`|True|
|`all-in-one/sources/decoded-original/0635-IdentXmlPart.xml`|`1a057d686446a3fdab7ac61bb09bc543c52f49646c9ca71ac323c10fcdffe457`|`95bfcad59cfb0c12b573e9e8face4262d1e94622`|True|
|`all-in-one/sources/decoded-original/0637-IdentXmlPart.xml`|`3fb68f57dbe2a877c4ad5aa1b3316810cf84958f2d13b5b1d7d321e0915271c7`|`cb1d7fb76aa2afd96eb46984cc1e71b77f36395c`|True|
|`all-in-one/sources/decoded-original/0678-IdentXmlPart.xml`|`51e637e0b9713c028810f2a717b5c3804a3a26c2f1be7e332a4d6bf277bfc382`|`7fafb2297bcdf739bf1d1dd68cebc0d74f2a40cc`|True|

## 부록 B. 검사 결과와 작업 기록

- 검사시각 2026-10-11T14:29:28.691590+00:00 UTC. 선정34파일/전체 sources712파일/중지5자산 모두 고정 Git blob과 바이트 일치, Git status clean. 보존 검사가 현재 CPU·실물이나 전체 원본의 의미검토를 뜻하지 않는다.
- 의미검토는 FlgNet5개에서 명시한 부모 입력전달/닫힘소비/다른쓰기/HMI핀/원시 gate 가지와 관련 선언이다. XML695개 이름검색은 전체695개 논리검토가 아니다. 실제 PDF6쪽 및 P&ID2확대/시공footer2확대를 시각 확인했다.
- extracts/LS35/source-hashes.json, source-preservation-hashes.json, stopped-assets-preservation.json, static-review.json, declaration-search.json, static-xml-evidence.json에 검사/정적 추출 근거가 있다.
- 14:24 UTC 범위·표준·고정자료 읽기;14:25 PDF6쪽/원본 선언·Part/Wire 대조;14:26 P&ID·footer 확대 및 케이블 상충 확인;14:27–14:29 초안 작성·SHA/Gitblob 보존검사. 원본 앱·생성기·시뮬레이터·행동시험은 실행하지 않았다.
