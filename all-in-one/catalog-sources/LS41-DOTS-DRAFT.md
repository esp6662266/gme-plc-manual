# LS41 — MV06 닫힘 위치 리미트 스위치 고유 조사 초안

- 대상: catalog_id LS41, component/하위 구성품, parent_id MV06, phase2. 부모·하위 별도 분류이며 부모 완료를 상속하지 않는다.
- 고정 원본: source-mv06, abcf31c5030bc7ef8749ed8e869a857f2387a28a, v1.12.0. 조사 2026-10-11 UTC, GME-STD-1.0.0. 모델 실행 설정은 미확인.
- AGENTS, rollout SKILL/source-map, WORK-STANDARD, WORK-ITEM-TEMPLATE, INVENTORY와 최신 BATCH25 실제 scope/중복 검토를 적용했다. 과거 차수 문구는 현재 대상으로 적용하지 않았다.
- MV06/ZT06/LS34 초안은 탐색색인과 부모 공통 범위로 재사용했다. 아래 핵심 XML 선언·Part/Wire·핀과 실제 PDF5쪽/확대2개는 원본에서 독립 확인했다. 부모 전체 재조사는 아니다.
- 원본·공통코드·버전·대장·배포·운영·PLC·현장·보호값·SEJIN 변경 없음. 시뮬레이터 작성·수정·생성·실행·행동시험, 원본 생성기·앱빌드·행동시험 없음. 자신의 초안 및 extracts/LS41만 작성했다.

## 먼저 확인할 결과

1. OEM FG33/PDF34가 LS-41을 LIMIT SWITCH VALVE CLOSING으로 직접 표기한다. +24Vdc10.7→X1/65(5×20 2A F 인쇄)→33.6→LS41 NC11/12→X1/66→E7.0이다. FG123/PDF124의 CPU515 MOD9 단자31까지 연결된다. 도면 NC기호와 현장 정상 극성은 구분한다.
2. 원시 I7.0, 처리 Inputs.MV06 Close DB13.X7.0, 수동요청 Flag.MV06_Close DB2.X10.6, HMI LimitSwitchClose DB11.X28.4는 서로 다른 층이다. 요청 Reset을 위치 기억이나 실제 닫힘 완료로 표시하지 않는다.
3. 0349는 처리입력을 양 접점으로 요청 Reset에, NOT 접점으로 닫힘 방향허가 말단에 쓴다. 0516 엔코더 게이트는 NOT raw I7.0을 쓴다. 이 두 읽기는 주소·처리층이 다르다.
4. 0397의 IW6→DB13.DBW6 외에 보존된 중지 블록0403의 Pot_MV06≤Int2→DB13.X7.0 일반 Coil Write가 존재한다. 정적 존재만 확인했으며 실행/생성/변경하지 않았다. 2를 LS41 실제 작동점이나 보호값으로 사용하지 않는다.
5. P&ID/시공 LS34/35와 OEM LS40/41의 일대일 동일성은 미확정이다. 네 ID를 유지하되 독립 4실물도 확정하지 않는다. LS35 시공 케이블을 LS41에 배정하지 않는다.

## 1. 설비·자료 기준 — 적용, 실물 대응 미확정

INVENTORY catalog/247은 LS41, parent MV06, baseline/planned/not_assessed다. TASK3-BATCH25-SCOPE는 parent_child_separate/new_research_pending, physical_identity_verified=false로 기록한다. 이는 문서 분류이지 실물 개수 확인이 아니다.

P&ID all-in-one/sources/PID_1684n002I.pdf 실제1쪽은 Overflow valve MV-06, M14, ZT-06, LS-34/35, 0.25kW440V를 표시한다. LS41이라는 식별은 이 MV06 주변에 없다. 도면1684n002 Apex I, 기본일06/04/2011, H 01/08/2012의 MV-06 추가/MV-03 command instrument 변경, I 15/01/2013의 MC-05 제거/FN-02 출력 변경을 실제 확대에서 확인했다. M14 모터와 ZT06 연속계측, LS 종단접점은 별 기능이다.

OEM Electrical_Rev2.pdf FG33/실제34쪽 제목 MOTORIZED VALVE MV-06, 기본일27.05.2024, 개정란 공란. FG123/실제124쪽 DIGITAL INPUT MODULE은 기본일27.05.2024, Rev2 17.03.2025다. 파일명 Rev2를 전 페이지 개정으로 복제하지 않는다.

시공 Electrical_Can_Decoating_20241118.pdf 실제33/64(CANDC-CONS-E016-033/D-PAGE16), 실제58/64(CANDC-CONS-C008-058/D-PAGE8)는 Rev1 24.11.11 first draft design이다. 준공·승인 결선·현재 설치로 승격하지 않는다.

## 2. I/O·HMI — 원시·가공·요청·표시 구별

NNNN은 all-in-one/sources/decoded-original/NNNN-FlgNet.xml 또는 명시한 IdentXmlPart.xml이다. RID는 선언문맥, NID는 원본 네트워크, Part/Wire/ORef/CRef UID는 해당 파일 내부 식별이다. AO는 bit offset이며 현재 CPU 주소 검증이 아니다.

|항목|원본 선언/연결|형식·주소·경계|
|---|---|---|
|OEM 닫힘 종단|FG33 LS41→E7.0, FG123 단자31|도면 직접 경로. 실제 시공 대응은 미확정|
|원시 MV06_Close|0678 SimpleAccess RID260, Input AO56, NID35 UID1481|Bool I7.0. 0516에서 raw 읽기|
|가공 Inputs.MV06 Close|0619 Global RID182, AO56 BAD168;0618 DepDB RID168 Inputs TOD13|Bool DB13.X7.0. NID9 UID844/865 Read|
|닫힘 수동요청|0619 Global RID93, AO86 BAD5;0618 RID5 Flag TOD2|Bool DB2.X10.6. UID847 Reset Write/861 Read. 위치 기억 아님|
|반대 열림요청|0619 RID94, AO85 BAD5|Bool DB2.X10.5, UID845 Read 등|
|자동모드|0619 RID81 AO53 BAD5|Bool DB2.X6.5, UID846 Read 등|
|닫힘 방향출력|0617 SimpleAccess RID97, Output AO10, UID866 Write|Bool Q1.2, 부모 구동 출력. LS41 전용 코일 아님|
|반대 방향출력|0617 RID98 Output AO9, UID864 Read|Bool Q1.1|
|HMI 닫힘 한계|hmi_plc_tags.csv MV_06\LimitSwitchClose ID0040B|DB11,X28.4. raw/DB13과 같은 주소 아님|
|HMI 요청·표시|Flag_CLOSE ID0040D DB2,X10.6; OutputClose ID00312 DB11,X28.1|CSV 설정이며 이벤트·쓰기권한·현재값 미입증|

나머지 부모 HMI는 LimitSwitchOpen0040A DB11.X28.3, Flag_OPEN0040C DB2.X10.5, Allarme1 0040E DB11.X28.2, AutoMan00047 DB2.X6.5, OutputOpen00046 DB11.X28.0이다. 8행 모두 부모 기능이며 LS41 전용 화면/알람으로 복제하지 않는다. LS41 전용 MEM_OPEN/CLOSE 래치는 확보하지 못했다.

0364 LAD1187 NID10 CRef23/RID639 및 CodeBlock22/RID130은 0624 BlockInterfaceInfo와0623 FCBlock HMI Standard Motorized Valve FC10 선언으로 결속한다. Limiti_Switch_Close 입력은 W44/ORef45/RID702, Limit_Switch_Close_HMI 출력은 W56/ORef57/RID146이다. 열림 입력 W42/ORef43/RID703, 출력 W54/ORef55/RID144와 별도다. 실인수 RID702/146의 같은 문맥 주소 선언은 미결속이므로 DB13.X7.0→DB11.X28.4 전체 전달을 확정하지 않는다. 타 블록의 동번호 RID를 가져와 결속하지 않았다.

## 3. 제어 구조 — 전달·소비·다른 쓰기

### 3.1 원시 Word 전달

0397 LAD1070 NID1: Powerrail W21→Move42.en, W52/ORef45/RID13→in, out1→W54/ORef46/RID14. 0627 RID13 Tag_171 Word Input AO48=IW6;0629 Global RID14 Word AO48 BAD4 및0628 Inputs RID4 TOD13=DB13.DBW6이다. I7.0이 포함된 Word 복사이며 이 Move42에는 반전이 없다. 온라인 값 일치·현재 호출순서·모든 다른 쓰기를 입증하지 않는다. main 호출의 부모 검토는 MV06 색인으로 유지했고 이번 문서에서 전체 프로그램 완전성은 주장하지 않는다.

### 3.2 처리 닫힘 입력 소비 — 0349 LAD1711 NID9

- Contact925(비반전) operand W875/ORef844/RID182=DB13.X7.0 → W70→OR797.in1. 다른 입력은 Contact927(W876/ORef845/RID94=열림요청)→W928→in2, Contact929(W877/ORef846/RID81=자동모드)→W930→in3이다.
- OR797.out→W72→RCoil801.in. operand W880/ORef847/RID93=Flag.MV06_Close(DB2.X10.6)를 Reset Write한다. 센서 기억 래치가 아니다.
- 앞단은 Powerrail W967→NOT ON Contact915(operand W27/ORef28/RID1)→W916→NOT ON Contact917(operand W21/ORef22/RID1)→W918이다. 0617 RID1은 같은 ON M0.0이다. NOT ON 중복을 정상 논리로 임의 수정하지 않는다.
- 닫힘 방향허가 말단은 OR966.out W908→NOT 반대열림Q Contact961(operand W909/ORef864/RID98 Q1.1)→W962→NOT 처리닫힘 Contact963(operand W910/ORef865/RID182 DB13.X7.0)→W964→일반 Coil837. operand W912/ORef866/RID97 Q1.2를 Write한다.
- 따라서 같은 처리닫힘 비트가 요청 Reset과 방향 출력 제한에 상반된 접점 형태로 쓰인다. 실제 닫힘/정상극성/NO·NC 현장 적합성을 이 식만으로 결론 내리지 않는다. 앞단 모드·고장·압력·Shot 전체는 부모 MV06 공통근거이며 LS41 독립 제어로 복제하지 않는다.

### 3.3 raw 닫힘 소비 — 0516 LAD1766 NID35

EM_OK Contact1529 operand W1503/ORef1480/RID173(0678 Input AO156=I19.4)→W1530→NOT raw MV06_Close Contact1531 operand W1504/ORef1481/RID260(I7.0)→W1532→Coil1441 및 Add1446.en이다. Coil1441 operand W1505/ORef1482/RID261은0676 Global AO188 BAD177,0674 fill_unit1 RID177 TOD91에 의해 SW_GATE4 DB91.X23.4다.

이 경로는 DB13.X7.0을 읽지 않는다. SW_GATE4는 소프트웨어 게이트이며 LS41 위치 기억이 아니다. 같은 네트워크 NOT SW_GATE4 Contact1533와 Move1463/1468 및 CRef1475의 환산은 ZT06 범위다. 여기서 LS41을 엔코더 펄스나 Pot값으로 동일화하거나 교정 절차를 만들지 않는다.

### 3.4 다른 DB Write — 보존 중지 원문 정적검토만

0403 LAD1083 NID2의 Le634(Int)는 Powerrail W21→pre, in1 W97/ORef100/RID327=Data.Pot_MV06, in2 W98/ORef110/RID254=Int2, out W96→일반 Coil635, operand W688/ORef657/RID242=Inputs.MV06 Close다. 0635 RID327 AO1088 BAD247와0634 Data RID247 TOD1은 DB1.DBW136;0637 RID254의 CB T=Int V=2를 확인했다. 0635 RID242 AO56 BAD5, NID2 UID657 AK=Write와0634 Inputs RID5 TOD13은 DB13.X7.0이다.

보존된 중지 블록의 정적 식은 Pot_MV06≤2다. S/R 기억 래치, 물리 LS41 작동점, 개도 단위%, 현재 설정 또는 현재 실행이라고 주장하지 않는다. 해당 블록을 생성·수정·실행하거나 행동시험하지 않았다. 원시 Word 전달 외 다른 쓰기가 있으므로 모든 시점에 raw=처리값이라고 단정하지 않는다. 간접/외부 쓰기 완전성 및 현행 호출은 미확정이다.

## 4. 전기 전달 경로 — 끝점·접점·개정 독립 확인

|원본/실제페이지|시작→끝|해석/미확정|
|---|---|---|
|OEM FG33/PDF34|+24Vdc10.7 공급선→X1/65(5×20 2A F)→33.6→LS-41 NC11/12→X1/66→E7.0, crossref123/2|VALVE CLOSING 인쇄. 도면 사양이며 현행 퓨즈/접점극성 확인 아님|
|OEM FG123/PDF124|crossref33/7→E7.0→CPU515 MOD9 단자31|LIMIT SWITCH LS-41 인쇄, Rev2 17.03.2025. 실제 CPU 형식/장착 확인 아님|
|시공33 route13 branch2|FLO4TB2→LS-35, cable8_20 =FLB+MV06-LS35A, Flexible16 CVV1.0/2|LS35 직접 자료. LS41 대응으로 사용 금지|
|시공58 행8_20|MV-06 FLO4TB2→MV-06 LS-35, DC CVV2C1.0 spare0 E1320 Adjustment3 LEN3|LS35 전용 branch. 설계길이이며 실측 아님|
|시공58 행8_17|UC-01 FLO4TB1→MV-06 FLO4TB2 LS34/35, =FLB+MV06-FLO4TB2A DC CVV7G1.0 spare2 Adjustment8 LEN9|공동 trunk, LS41 준공 결속 미확보|
|시공58 행8_6|CR→MV-06 FLO4TB2 ZT06, 같은 =FLB+MV06-FLO4TB2A TM CVV-S4S1.0 spare0 Adjustment12 LEN63|8_17과 ID 중복, 신호/시작점/규격 다름. 하나로 합치지 않음|

시공58 행8_4는 CR→UC-01 FLO4TB1 LS34/35/17HL1, =FLB+UC01-FLO4TB1A DC CVV9G1.0 spare2 LEN54다. LS41 직접 식별 경로가 아니다. 검게 가린8_5/8_7/8_8은 복원하거나 활성 경로로 가정하지 않았다. 시공33 표의 FLO4TB2 LOC=UC-01도 부모를 UC01로 재배정할 근거가 아니다.

OEM X1/65~66와 시공 FLO4TB2 내부단자의 승인 대응표가 없다. LS35와LS41을 동일시하거나 P&ID 배치만으로 두 쌍을 매칭하지 않는다. 별도 LS41 PLC출력·밸브코일·보호설정을 만들지 않았다. 공통 인버터·M14 전력회로 및 EV69KA/71KA의5–9 정정은 부모/기존 범위에 보존하고 LS41 소유로 복제하지 않는다.

## 5. 알람·복구 — 독립 전용 근거 미확보

LS41 전용 알람번호·타이머·지연·Set/Reset 진단은 직접 확보하지 못했다. 부모 MV06 초안의 MV_06_FAULT DB3.X11.6 및 150ms 방향응답/누적감시는 부모 공통 고장이다. LS41 미도달시간이나 센서 독립고장으로 계수하지 않는다. 이번에는 해당 부모 타이머 전체를 재검토하지 않았다.

0349의 RCoil801은 수동요청 Reset이며 알람 Reset 또는 실제 복구 완료가 아니다. HMI Allarme1 DB11.X28.2와 LimitSwitchClose DB11.X28.4, DB13.X7.0, raw I7.0을 분리한다. 현장 정상극성·고장이력·현재 CPU·실제 위치 및 복구 관찰은 없다.

## 6. 증상별 관찰 — 읽기 전용 확인 기준

|증상|필요한 기록/비교|판정 경계|
|---|---|---|
|닫힘 표시와 실제 위치 불일치|LS41 명판/기계 부착위치, OEM/시공 승인 대응, 동일시각 I7.0·DB13.X7.0·DB11.X28.4|NC그림 또는 닫힘 이름만으로 정상극성 확정 금지|
|원시와 처리값 불일치|0397 Word 전달,0403 다른 Write의 현행 활성/호출순서 및 CPU/프로젝트 식별|보존 블록 존재만으로 현재 원인 확정 금지|
|닫힘 요청이 사라짐|R801의 InputsClose/FlagOpen/Auto 및 NOT ON 두 접점 상태|요청Reset을 실제 닫힘완료로 보지 않음|
|닫힘 출력 제한|Contact963 처리입력,Contact961 반대Q 및 부모 앞단 허가|접점 우회·출력강제·보호값변경 제안 없음|
|엔코더값과 종단값이 다름|0516 raw I7.0,EM_OK,SW_GATE4와 ZT06 관찰 기록|연속계측/종단접점을 같은 센서로 취급하지 않음|
|케이블 식별/복구가 불명|FLO4TB2 준공 단자표, X1/65~66 대응, 관찰자/시각·시간대/수집장치·값/실제위치 전후기록|동명·문서검사·알람없음만으로 결선/교체/복구 완료 판정 금지|

현장 관찰·접점 조작·운전시험은 수행하지 않았다. 운영 사진/이력/개인자료를 복제하지 않았다.

## 7. 완료·누락·인계

|영역|상태|남은 자료|
|---|---|---|
|설비·자료|적용/정적초안|LS34/35↔LS40/41 승인 대응, LS41 실물|
|I/O·HMI|적용/일부미결속|HMI 실인수 선언·이벤트, 현재 CPU/입력표|
|제어|적용/정적검토|현재 호출·외부/간접쓰기·온라인 동시값|
|전기 끝점|OEM 적용/시공 대응 미확정|FLO4TB2↔X1 승인단자표·정상극성|
|알람·복구|독립근거 미확보|전용진단 여부/현장복구 기록|
|증상 관찰|수집기준 적용|실제 관찰값 없음|
|완료 기준|complete_with_gaps 초안|통합자 독립검토 필요|

문서와 도면·래더 비교 근거만 준비했다. 백업·선택복원/기록전후비교/보고서UI는 미구현·미검증이다. documentation=draft_complete_with_gaps, static_review=performed_with_gaps, ui_records/publication/TIA_compile/live_cpu/field_recovery=not_performed. BC01 동등 구현완료나 게시완료가 아니다. preflight·원본 생성기·앱빌드·회귀·행동시험은 이번 제한된 조사범위에서 실행하지 않았다.

새 자료 없이 보류된 동일성을 반복 조사하거나 다른 ID를 병합하지 않는다. 필요한 다음 자료는 LS34/35와LS40/41 승인 대응표, FLO4TB2/X1 준공단자표, 현재 TIA/CPU/HMI 동일성, 정상극성/실제 위치 및 복구 기록이다.

## 부록 A. 선정 원본 SHA256 / 고정 Gitblob 바이트 대조

선정36파일 전부 아래 기록. 해시검사 수와 의미검토 수는 다르다. 핵심 의미검토는 FlgNet5개 내 명시 가지와 선언, CSV8행, PDF5쪽 및 P&ID 확대2개다. 712개 원본 전체 해시는712개 전체 의미검토가 아니다. 경로는 source-mv06 기준.

|원본 경로|SHA256|Gitblob|바이트일치|
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
|`all-in-one/sources/decoded-original/0674-IdentXmlPart.xml`|`4770702f519bacda69202bb2f7733d983074bda90964360c238f990d9d08fd84`|`f210593944547b63eab10c667348711413600aab`|True|
|`all-in-one/sources/decoded-original/0676-IdentXmlPart.xml`|`c58427c5b0ac6c11cdb52e4c6d0461c7b191fae81ccace191048e9f175fcec59`|`1ed67265f69796a4e659f9438e551068037f33a4`|True|

## 부록 B. 검사·작업 기록

- 2026-10-11 14:24 UTC 시작: 범위·표준·고정점/Git clean 확인. 14:25~14:26 UTC PDF 실제 렌더/접점·끝점·개정과 XML 선언/Part/Wire 대조. 14:26 UTC 선정36·sources712·중지5 고정 Gitblob 바이트일치 확인.
- XML695개의 선언 검색은 이름 탐색이며 전체 논리 완전성 검사가 아니다. 선언 발췌는 declaration-search.json 및 selected-declarations.json.
- 검사자료: extracts/LS41/source-hashes.json, source-preservation-hashes.json, stopped-assets-preservation.json, static-review.json. 원본 Git 상태 clean, 실행·생성·배포·현장 변경0.
