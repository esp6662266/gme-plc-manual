# LS34 — MV06 하위 리미트 스위치 고유 원본 조사

- 대상: LS34 한 ID, component/하위 구성품, parent MV06, phase2. INVENTORY catalog[244] 및 TASK3-BATCH24-SCOPE와 GME-CATALOG-OVERLAP-REVIEW의 parent_child_separate 분류를 따른다.
- 고정 원본: gme-research/source-mv06, abcf31c5030bc7ef8749ed8e869a857f2387a28a / v1.12.0. 표준 GME-STD-1.0.0. 시작 2026-10-11 13:54 UTC. 실행 모델/추론 설정 UI 증명 미확인.
- AGENTS·rollout SKILL·WORK-STANDARD·WORK-ITEM-TEMPLATE·INVENTORY 및 최신 인계 상단을 읽었다. MV06/ZT06 초안은 탐색 색인과 공통 근거로 재사용했다. 부모 전체 제어를 반복 조사하지 않았다.
- 원본·코드·대장·PLC·현장·보호값·SEJIN 변경 없음. 새 Work/Codex·업로드·재위임 없음. 시뮬레이터 작성/수정/생성/실행/행동시험과 생성기/앱빌드는 하지 않았다. 0403은 보존된 백업 XML의 다른 쓰기만 정적 열람했다.

## 핵심 결과

1. P&ID와 시공도에는 LS34가 MV06 주변 위치 스위치로 존재한다. 그러나 OEM에는 열림 LS40, 닫힘 LS41이다. LS34=LS40 또는 LS34=I6.7을 확정하지 않는다. LS34/35/40/41 네 catalog ID를 유지하며 독립 실물 네 개라는 뜻도 아니다.
2. LS34에 직접 결속된 원시 입력 선언과 HMI 태그는 이번 검색에서 미확보다. 부모 MV06 열림 경로의 DB13.X6.7은 후보 공통 근거이며 LS34 소유 주소가 아니다.
3. 부모 입력 Word 전달에는 반전이 없지만, MV06_Open 소비 접점947에는 NOT이 있다. 입력 가공 반전과 출력 허가 접점 반전을 혼동하지 않는다.
4. 부모 DB13.X6.7에는 0397 Word 복사 외에 0403 일반 Coil633의 Write가 존재한다. 이 보존된 중지 블록의 식 Pot_MV06≥98을 물리 LS34 작동점이나 현행 보호값으로 사용하지 않는다.

## 1. 설비·자료 기준 — 적용, 실물 대응 미확정

P&ID 원본 all-in-one/sources/PID_1684n002I.pdf 실제1쪽의 Overflow valve MV-06 주변에 M14, ZT-06, LS-34/35, 0.25kW 440V가 표시된다. LS34는 M14 위쪽, LS35는 아래쪽이지만 이 배치만으로 각각 열림/닫힘 방향을 배정할 수 없다. M14 모터, ZT06 연속 위치 계측, LS 위치 접점은 별 기능이다. 도면1684n002, Apex I, 기본일06/04/2011, 개정H 01/08/2012는 MV-06 추가/MV-03 command instrument 변경, I 15/01/2013은 MC-05 제거/FN-02 출력 변경이다. 현재 설치 확인이 아니다.

시공 Electrical_Can_Decoating_20241118.pdf 실제33/64는 FLOW_B ZONE03, CANDC-CONS-E016-033/D-PAGE16, 실제58/64는 CANDC-CONS-C008-058/D-PAGE8이다. 두 쪽 개정1, 24.11.11, first draft design. 시공 설계 자료이며 준공 결선·승인 완료로 승격하지 않는다.

OEM Electrical_Rev2.pdf FG33/PDF34는 MOTORIZED VALVE MV-06, LS40/41을 명시한다. 기본일27.05.2024이며 개정란 공란. FG122/PDF123 및 FG123/PDF124는 기본일27.05.2024, 개정2 17.03.2025. 파일명 Rev2를 모든 페이지 개정값으로 적용하지 않는다.

## 2. I/O·HMI — 부모 후보와 LS34 직접 근거 분리

이하 NNNN은 all-in-one/sources/decoded-original/NNNN-FlgNet.xml 또는 명시한 IdentXmlPart.xml이다. RID는 선언문맥 내 식별자, NID는 원본 네트워크, UID/Part/Wire는 해당 파일 내부 위치다. 주소는 백업 선언이며 현재 CPU 검증이 아니다.

| 계층 | 원본·선언/핀 | 확인 사실과 경계 |
|---|---|---|
| LS34 직접 PLC | decoded-original XML695개에서 LS[._ -]?34 경계 문자열검색0 | 텍스트 미확보. 간접주소·바이너리·전체 TIA에 신호가 없다는 증거 아님 |
| 부모 열림 원시 후보 | OEM FG33 E6.7→FG122 단자28 LS.40 | LS40 도면 경로. LS34 주소로 배정 금지; 동명 원시 SimpleAccess 직접결속 미확보 |
| 부모 가공 열림 | 0619 Global RID181, AO55, BAD168;0618 DepDB RID168 Inputs TOD13 | Bool DB13.X6.7. NID9 UID840/856 Read |
| 부모 가공 닫힘 | 0619 Global RID182 AO56, BAD168 | DB13.X7.0. LS34에 배정하지 않음 |
| 부모 수동 열림 요청 | 0619 RID94 AO85, BAD5;0618 RID5 Flag TOD2 | DB2.X10.5. NID9 UID843 Reset Write,845/852 Read. 센서/위치 기억이 아님 |
| 부모 수동 닫힘 요청 | 0619 RID93 AO86, BAD5 | DB2.X10.6. NID9 UID847 Reset Write. 센서가 아님 |
| 부모 raw 닫힘 | 0678 SimpleAccess RID260, Input AO56, NID35 UID1481 | I7.0. 엔코더 gate 경로 전용 사용을 확인; LS34 raw로 전용 금지 |
| HMI 부모 열림 한계 | hmi_plc_tags.csv MV_06\\LimitSwitchOpen ID0040A DB11,X28.3 | 부모 표시 태그. DB13.X6.7과 같은 주소 아님 |
| HMI 부모 닫힘 한계 | 동일 ID0040B DB11,X28.4 | LS34와 직접 태그 대응 미확보 |
| HMI 부모 요청 | ID0040C Flag_OPEN DB2,X10.5;0040D Flag_CLOSE DB2,X10.6 | CSV만으로 버튼 이벤트/쓰기 권한/현재값 입증 불가 |

CSV의 부모8행 중 나머지는 Allarme1 DB11.X28.2(0040E), OutputClose DB11.X28.1(00312), AutoMan DB2.X6.5(00047), OutputOpen DB11.X28.0(00046)다. LS34 전용 태그로 복제하지 않는다. LS34 전용 MEM_OPEN/CLOSE 기억 비트도 확보하지 못했다.

0364 LAD1187 NID10: CRef23/RID639, CodeBlock22/RID130은 0624 BlockInterfaceInfo 및0623 FCBlock HMI Standard Motorized Valve FC10와 결속한다. W42/ORef43/RID703→Limit_switch_Open, W44/ORef45/RID702→Limiti_Switch_Close, Limit_Switch_Open_HMI→W54/ORef55/RID144, Close_HMI→W56/ORef57/RID146을 확인했다. 이 실인수의 같은 문맥 선언은 미결속이다. 다른 블록의 동번호 RID를 가져와 DB13→DB11 전체 전달을 확정하지 않는다.

## 3. 제어 구조 — 입력 전달·소비·다른 쓰기

### 3.1 Word 전달

0397 LAD1070 NID1: Powerrail W21→Move42.en, in W52/ORef45=0627 SimpleAccess RID13 Tag_171 Word Input AO48(IW6), out1 W54/ORef46=0629 Global RID14 Word AO48 BAD4. 0628 DepDB RID4 Inputs TOD13이므로 DB13.DBW6으로 복사한다. 이 복사에 NOT은 없다. IW6의 두 바이트는 부모 I6.7/I7.0을 포함하지만 온라인 값 동일성·다른 Writer·현재 호출은 별도다. 0030의 main 호출조건은 부모 초안을 공통 색인으로 유지하고 이번 LS34 문서에서 전체 호출 검증을 주장하지 않는다.

### 3.2 부모 열림 가공 입력의 소비

0349 LAD1711 NID9:

- Contact919(반전 없음) operand W869/ORef840/RID181=Inputs.MV06_Open →W67→OR790.in1. OR790의 다른 두 가지는 Flag.MV06_Close(Contact921 W870/O841 RID93)와 MV06_Auto(Contact923 W871/O842 RID81)다. OR 출력W71→RCoil794, operand W874/ORef843/RID94=Flag.MV06_Open Reset.
- 이 요청 해제의 공통 앞단은 NOT ON Contact915(W27/O28 RID1) →W916→NOT ON Contact917(W21/O22 RID1)→W918이다. 같은 0617 SimpleAccess RID1 ON M0.0이며 원문 상충을 임의 수정하지 않는다.
- 방향 출력 말단은 NOT 반대Q Contact945→W946→NOT Inputs.MV06_Open Contact947(operand W895/ORef856/RID181)→W948→Coil821, W897/ORef857=0617 RID98 Open MV06 Output AO9(Q1.1).
- 따라서 열림가공값은 요청Reset의 양 접점과 방향허가의 부정 접점에서 서로 다르게 소비된다. 센서 NO/NC·현장 정상극성·현재 열린 상태는 이 식만으로 결정할 수 없다. 외곽 NOT ON/고장·모드/자동 압력/Shot 등 앞단 전체는 MV06 초안 범위를 재사용하고 LS34 제어 소유로 합치지 않는다.

### 3.3 다른 Write: 중지된 보존 XML 정적 검사만

0635 Global RID243 AO55 BAD5는 Inputs.MV06_Open, NID2 UID654 AK=Write다. 0634 DepDB RID5 Inputs TOD13으로 DB13.X6.7을 다시 확인했다. 해당0403 LAD1083 NID2에는 Ge632(Int), W92/ORef94/RID327=Data.Pot_MV06, W93/ORef95/RID253=Int98(0637 상수), out W91→일반 Coil633, operand W684/ORef654/RID243이 있다. Ge632.pre는 W21 Powerrail이다. S/R 센서 기억 래치가 아니다.

짝 닫힘 Writer는 Le634(Int), in1 W97/ORef100 RID327, in2 W98/ORef110 RID254=Int2(0637), W96→Coil635, W688/ORef657/RID242=DB13.X7.0이다. 0635 RID327 Pot_MV06 AO1088/BAD247 및0634 RID247 Data TOD1은 DB1.DBW136이다. 정적 식 ≥98 / ≤2를 실제 스위치 위치/단위%/현행 설정으로 쓰지 않는다. 중지 블록이 현재 실행된다는 주장도 없다. 전체 외부/간접 DB 쓰기 완전성은 미확정이다.

### 3.4 엔코더 경계

0516 LAD1766 NID35에서 Contact1531은 NOT raw MV06_Close이며 operand W1504/ORef1481=0678 RID260 I7.0이다. 앞단EM_OK Contact1529→W1530, 출력W1532→Coil1441 SW_GATE4와Add1446.en. 이것은 LS34 또는 가공 DB13.X6.7을 읽는 경로가 아니다. 연속 위치·엔코더 저장과 LS 종단 입력을 혼합하지 않는다. 상세 HSC·환산·0 Write는 ZT06 초안의 별도 소유로 둔다.

## 4. 전기 전달 경로 — 도면 끝점과 상충

### LS34 직접 시공 경로

| 실제PDF/행 | 시작→끝 | 원문 사양·해석 |
|---|---|---|
|시공33 route13 branch1|FLO4TB2→LS-34|Flexible16, device MV-06 LS-34, cable8_19 =FLB+MV06-LS34A, CVV/1.0/2 |
|시공58 행8_19|MV-06 FLO4TB2→MV-06 LS-34|DC,CVV,2C,1.0,spare0,E1310,Adjustment3,LEN3 |
|시공58 행8_17|UC-01 FLO4TB1→MV-06 FLO4TB2 LS34/35|=FLB+MV06-FLO4TB2A,DC,CVV,7G,1.0,spare2,Adjustment8,LEN9 |
|시공58 행8_6|CR→MV-06 FLO4TB2 ZT06|동일 =FLB+MV06-FLO4TB2A,TM,CVV-S,4S,1.0,spare0,Adjustment12,LEN63 |

8_6/8_17은 ID가 같아도 신호·시작점·규격이 달라 하나의 케이블로 합치지 않는다. 시공33 표에는 FLO4TB2의 LOC가 UC-01로 적힌 중계행도 있다. 물리 부모를 UC01로 재배정할 근거가 아니다. 시공58 행8_4는 CR→UC01 FLO4TB1 LS34/35/17HL1(=FLB+UC01-FLO4TB1A,DC,CVV9G1.0,spare2,LEN54)으로 나타난다. LS34/35 공동 trunk이며 LS34 전용회로로 세지 않는다. LEN/Adjustment는 인쇄 설계값이지 실측 길이가 아니다. 검게 가린8_5/7/8은 복원하거나 활성경로로 가정하지 않았다.

### OEM 부모 후보 끝점 — LS34 동일성 미확정

| 분기 | 공급·접점·현장단자 | PLC 도면 끝점 |
|---|---|---|
|열림 LS40|FG33 +24Vdc10.7 →X1/63(2A F 인쇄)→33.5→LS40 NC11/12→X1/64→E6.7|FG122/PDF123 CPU515 MOD9 단자28, crossref33/5, LIMIT SWITCH LS.40 |
|닫힘 LS41|같은+24V→X1/65(2A F)→33.6→LS41 NC11/12→X1/66→E7.0|FG123/PDF124 CPU515 MOD9 단자31,crossref33/7,LIMIT SWITCH LS-41 |

FG33 표기와 양끝점은 실제 렌더로 확인했다. NC기호는 현장 정상극성 확인이 아니다. X1/63~66와 시공 FLO4TB2 내부 단자의 승인 결속표가 없으므로 LS34-8_19와 LS40-X1/63~64를 연결된 준공회로로 그리지 않는다. LS34 전용 PLC 출력/밸브코일/보호기/퓨즈 설정은 만들지 않는다. 부모 공통 인버터·M14 전력 경로와 EV 69KA/71KA의5–9 접점 정정은 유지하되 LS34 소유로 복제하지 않는다.

## 5. 알람·복구 — 직접 전용 근거 미확보

LS34 전용 알람번호·타이머·Set/Reset 또는 진단형식은 직접 확보하지 못했다. 부모 MV06 초안의 MV_06_FAULT DB3.X11.6(0159의150ms 방향응답,0352의W19>2200/W20<−2200)은 부모 공통 고장이다. LS34 미도달 시간·센서 자체 고장으로 복제하지 않는다. 이번에는 부모 타이머 전체를 재검토하지 않았고 LS34 독립 알람으로 계수하지 않는다.

부모 HMI 한계표시 DB11.X28.3과 고장표시DB11.X28.2, raw 후보I6.7, 가공DB13.X6.7, 수동요청DB2.X10.5는 서로 다르다. 요청Reset·알람소멸·접점상태변화·실제 위치복구는 별도 관찰이다. 현재 CPU/극성/고장이력/현장 복구 증거는 없다.

## 6. 증상별 관찰 — 읽기 전용 자료 요청

| 증상 | 필요한 기록·비교 | 판단 경계 |
|---|---|---|
|LS34와 화면 열림표시 불일치|LS34 명판/기계부착 위치·승인 LS34↔LS40 대응·HMI 이벤트/태그 및 동일시각 원시/DB13/DB11|LS34를 I6.7로 강제 대응하지 않음 |
|가공값이 원시값과 다름|0397 Word Write·0403 다른 Write의 현재 활성여부/호출순서·프로젝트 식별|중지 블록 존재만으로 현재 원인 확정 금지 |
|열림요청이 사라짐|0349 R794 조건,NOT ON 두접점·InputsOpen/FlagClose/Auto|요청값 소멸을 실제 개방 완료로 보지 않음 |
|출력이 제한됨|0349 Contact947 NOT 처리입력과 다른 앞단 허가 기록|접점우회·출력강제·보호값 변경 제안 없음 |
|케이블/부품 식별 불명|8_19 현장표찰,FLO4TB2 승인단자표,LS34/35↔40/41 정정문서|중복ID만으로 결선/교체 지시 금지 |
|복구 확인 필요|권한있는 현장 관찰자·시각/시간대·실제 위치·신호 전후값·프로젝트 일치|알람없음이나 문서검사만으로 복구완료 불가 |

현재 그런 현장 관찰은 수행하지 않았다. 센서 접점 조작·운전시험·설정 변경·시뮬레이션을 수행하거나 제안하지 않는다.

## 7. 완료·누락·인계

| 영역 | 상태 | 남은 자료 |
|---|---|---|
|설비·자료 기준|적용/정적 초안|LS34 실물 및 LS40과의 승인 대응 |
|I/O·HMI|부모 후보만 적용/LS34 직접 미확보|현재 TIA 선언·입력표·HMI 이벤트 |
|제어|부모 입력소비/다른쓰기 정적검토|현재 호출·간접쓰기·CPU 일치 |
|전기 끝점|시공 직접/부모 OEM 후보 적용|FLO4TB2 준공 단자표·현재 배선/극성 |
|알람·복구|독립 근거 미확보|직접 전용진단 여부·현장복구 기록 |
|증상 관찰|적용/자료수집 기준|현재 관찰값 없음 |
|완료 기준|complete_with_gaps 문서 인계|통합자 독립검토 필요 |

문서·정적 대조만 수행했다. 도면·래더 비교 근거는 마련했지만 백업/선택복원·기록전후비교·보고서UI는 미구현/미검증이며 BC01 동등 구현완료가 아니다. ui_records/publication/TIA/live_cpu/field_recovery는 미수행이다. 원본 preflight/생성기/회귀/앱빌드는 이번 own 정적분석 범위에서 실행하지 않았다. 실제 모델 설정 증거 없음.

필요한 다음 자료는 승인된 LS34/35와 LS40/41 대응표, FLO4TB2 현장 단자·케이블표, 현재 프로젝트/CPU 일치, HMI 미결속 실인수 선언, 정상극성 및 실제 위치 기록이다. 새 자료 없이 부모 전체를 다시 조사하거나 이름만으로 ID를 병합하지 않는다.

## 부록 A. 선정 원본 전체 SHA256 / 고정 Git blob

선정 34파일 전부 아래 기록. 해시 수는 의미검토 수가 아니다. 아래 경로는 source-mv06 기준이다.

| 원본 경로 | SHA256 | Git blob | 바이트일치 |
|---|---|---|---|
| `AGENTS.md` | `0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2` | `073164bc6efd5791032d62c71b03b4dab48cb6f8` | True |
| `.agents/skills/gme-equipment-rollout/SKILL.md` | `fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b` | `9aa820ea6ca15b4e136c9772423b78ed4df6a3d4` | True |
| `.agents/skills/gme-equipment-rollout/references/source-map.md` | `40612c5efb8f94608840c7bc0e9095ea840df54920861c388ae48ea34c7998dc` | `49e50a7a8e56a16e2ec7f3607a03fd90adb8f1d3` | True |
| `docs/equipment-standard/WORK-STANDARD.md` | `05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99` | `f76a570cc73098632e08759b17934000f7e3a253` | True |
| `docs/equipment-standard/WORK-ITEM-TEMPLATE.md` | `4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586` | `e546f39535d2b589e80f97db869ac37ce4d05cfd` | True |
| `docs/equipment-standard/START-GPT61.md` | `35769e3146ccd707fea2b81b67b30376b76a0a19c7e662fe2bb4fdd382306f94` | `0d08cab3678df7e2625251b641b138ef4956483b` | True |
| `docs/equipment-standard/INVENTORY.json` | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` | `587c3748ad9224718f95ba06463fee913dae231d` | True |
| `VERSION.json` | `5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7` | `fffb51663b7705aec91cb119ca80ee943a4ce758` | True |
| `WORKSPACE-HANDOFF.md` | `215096d997782e78e901dfae36c782937e49611fbeb677a0d3fa50cbecf8d074` | `dd0b8989d2376c4415bba9bd826fe6754c6b1a12` | True |
| `PUBLICATION_STATUS.md` | `efe4857aec598d90470322cf3962eb3fe1f64947630e1fdf71d1c90134de8740` | `d76401cf291fc0be681acc51fa898ad3ce46ff78` | True |
| `EXPANSION-WORK.md` | `ec624de9fd2fcfac861a67fd5e828b25ef46db50bfd7a37ff16e2cb54cd0f7e2` | `4c42d88ecc2d48269eb23e13a20ebf3721a092a1` | True |
| `all-in-one/ACTIVE-WORK.md` | `eff3bbc08ecff41da3beff77f3fec48e7d148708192bcaaab00f34b6a721afc2` | `6eb947c629b5ddf9c759ef87649451303938864b` | True |
| `all-in-one/sources/Electrical_Rev2.pdf` | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` | `f610fd7c7ce14ae951b00cff57b969259bfb389d` | True |
| `all-in-one/sources/Electrical_Can_Decoating_20241118.pdf` | `3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd` | `0ee6b6f8361c5790864dbba4bbd9d55e8e7c08f8` | True |
| `all-in-one/sources/PID_1684n002I.pdf` | `2f873ec59562c244d547f862978f23cdfd44d57cc10db6dbae247c1b27c29c0b` | `8c83a59fefd5b8b651ec3537ea4236a073f5e109` | True |
| `all-in-one/sources/hmi_plc_tags.csv` | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` | `cf4c0650e7c7baac350dcb89909b808435704880` | True |
| `all-in-one/sources/decoded-original/network-map.json` | `c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60` | `424430b6b953e43138e5d0a18ca40c949e21cfa1` | True |
| `all-in-one/sources/decoded-original/0349-FlgNet.xml` | `2f45af21543189d83f027afbae797532cae5d55935bac1fba3913825d741863b` | `7082fb0a8817f254ae1ac0087990478f2de30791` | True |
| `all-in-one/sources/decoded-original/0397-FlgNet.xml` | `bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834` | `4ab8370493c4e28fc1eabeeebe2743d27f0c4021` | True |
| `all-in-one/sources/decoded-original/0364-FlgNet.xml` | `c23a9952251a48105eedd1ed3c185f781b6163d094fb3bb396ac27415587de8a` | `dee7f6d4c8d0675deb1c4bb5c5eb78392ae43c57` | True |
| `all-in-one/sources/decoded-original/0403-FlgNet.xml` | `77b03e38aa857ac8dd404f2f66a56256939b4e7924b41334a7981b86089c1e6b` | `4c806e31eb65f00cbb7870c72896ac26a8bc3dd3` | True |
| `all-in-one/sources/decoded-original/0516-FlgNet.xml` | `382738875d4fe8ebcf38f878eafd6486047e3cdd6de7a98bebcafc2afd124c8f` | `06030b0a2ec9e27ee53298e46584373ec92ab97b` | True |
| `all-in-one/sources/decoded-original/0617-IdentXmlPart.xml` | `10bcf85169cb2512f55acadaef299a3d46b4b4cecd88032d739cfeba23e94aa9` | `9527658ee6808be34bd513b1b2ebaf3a4a5a6f3e` | True |
| `all-in-one/sources/decoded-original/0618-IdentXmlPart.xml` | `0c6762de9cdf0e294317f7463bea3d8e6df5673d333d9b1826ebd17a7ded044c` | `9eec0dbd8abde4aa7295f77b63ad473f895f274b` | True |
| `all-in-one/sources/decoded-original/0619-IdentXmlPart.xml` | `85694bb5b696e31e6a1217431112e5b750516c4f94078d6e127d4394a8b80456` | `11f0502c84a1f319a21459a35c0dc1c6ce8e8f36` | True |
| `all-in-one/sources/decoded-original/0623-IdentXmlPart.xml` | `4acd00406ea92466169e57e59fc90b0da4d9ec55fd19e2e96c9556e939cb83a6` | `13b3af0459c8e6069bb9b2f1b16454bf479e08dc` | True |
| `all-in-one/sources/decoded-original/0624-IdentXmlPart.xml` | `24607c0827fbde428bccf8637ef4ae490798a69a7c2f3b87861d0749082d367a` | `02511fea47fc47981c101bba49dc40adde1cdcc3` | True |
| `all-in-one/sources/decoded-original/0627-IdentXmlPart.xml` | `08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb` | `61ebc0abbb2ca160e11e1da400a3f14a397d8bc5` | True |
| `all-in-one/sources/decoded-original/0628-IdentXmlPart.xml` | `9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd` | `170ca5c72599edc7ea7eefe651c3680ce325e76a` | True |
| `all-in-one/sources/decoded-original/0629-IdentXmlPart.xml` | `67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972` | `058129bb01e27f7a6a0d0293f332d745e5bab74e` | True |
| `all-in-one/sources/decoded-original/0634-IdentXmlPart.xml` | `af3fcb536a6270ffb9a19e5b3f2c284a38d67d465f5147961005c1c01d11299d` | `877d9e0734dc7f3e5a8cea789eeb58a208501f48` | True |
| `all-in-one/sources/decoded-original/0635-IdentXmlPart.xml` | `1a057d686446a3fdab7ac61bb09bc543c52f49646c9ca71ac323c10fcdffe457` | `95bfcad59cfb0c12b573e9e8face4262d1e94622` | True |
| `all-in-one/sources/decoded-original/0637-IdentXmlPart.xml` | `3fb68f57dbe2a877c4ad5aa1b3316810cf84958f2d13b5b1d7d321e0915271c7` | `cb1d7fb76aa2afd96eb46984cc1e71b77f36395c` | True |
| `all-in-one/sources/decoded-original/0678-IdentXmlPart.xml` | `51e637e0b9713c028810f2a717b5c3804a3a26c2f1be7e332a4d6bf277bfc382` | `7fafb2297bcdf739bf1d1dd68cebc0d74f2a40cc` | True |

## 부록 B. 검사 결과·시각

- 검사시각 2026-10-11T13:59:56.210045+00:00 UTC. 선정 34파일 및 전체 sources 712파일, 중지5자산은 고정 Git blob과 바이트 일치. Git status clean. 검사는 의미해석 또는 현행 설치검증을 뜻하지 않는다.
- 핵심 의미검토는 FlgNet5개 중 명시한 LS/부모 경계 가지 및 관련 선언이다. XML695개의 이름검색은695개 전체 논리검토가 아니다. 실제 PDF6쪽과 P&ID2개 확대를 시각 확인했다.
- 검사JSON은 extracts/LS34/source-hashes.json, source-preservation-hashes.json, stopped-assets-preservation.json, static-review.json. 정적검색결과는 declaration-search.json.
- 13:54 UTC 시작/표준·범위읽기,13:55 PDF6쪽 및 선언·다른쓰기 확인,13:56 상세접점/문맥 확인,13:59 초안작성 및 보존검사.
- 첫 수집 스크립트명이 Python inspect 모듈을 가려 PDF 수집이 한 번 실패했다. own 스크립트명을 collect_static.py로 바꿔 정적 수집을 재실행했고 PDF6쪽을 정상 렌더했다. 원본 변경 없음.
