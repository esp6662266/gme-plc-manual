# LS40 — MV06 열림 종단 리미트 스위치 원본 조사 초안

- 대상 한 ID: LS40, component/하위 구성품, parent MV06, phase2. INVENTORY catalog[246], TASK3-BATCH25-SCOPE 및 GME-CATALOG-OVERLAP-REVIEW의 parent_child_separate 분류. LS34/35/40/41 ID를 보존하며 독립 실물 네 개라는 뜻은 아니다.
- 고정 원본: gme-research/source-mv06, abcf31c5030bc7ef8749ed8e869a857f2387a28a, v1.12.0. 표준 GME-STD-1.0.0. 2026-10-11 14:24 UTC 시작. 실제 모델/추론 설정 증명 미확인.
- AGENTS·rollout SKILL·WORK-STANDARD·WORK-ITEM-TEMPLATE·INVENTORY·시작 안내/소스맵 및 최신 인계 상단을 읽었다. MV06/ZT06/LS34는 공통 색인으로 재사용하고 아래 고유 선언/핀/도면은 고정 원본으로 대조했다. 부모 전체 재조사는 하지 않았다.
- own drafts/LS40-DOTS-DRAFT.md와 extracts/LS40만 작성. 원본/코드/버전/대장/배포/운영/PLC/현장/보호값/SEJIN 변경 없음. 새 Work/Codex·재위임·업로드·사용자전송 없음. 시뮬레이터 작성·수정·생성·실행·행동시험 및 원본 생성기/앱빌드 없음. 0403은 보존 XML의 다른 쓰기를 정적으로 열람한 것뿐이다.

## 핵심 결과

1. OEM FG33/PDF34는 LS-40을 LIMIT SWITCH VALVE OPEN으로 명시한다. X1/63 → 선번33.5 → NC11/12 → X1/64 → E6.7 → FG122/PDF123 MOD9 단자28을 양끝점 확인했다. 이는 문서상 열림 종단 경로이며 현재 현장 극성/작동점 증명이 아니다.
2. 백업 색인 live_index doc657의 mv06_open, Bool %i6.7, comment limit switch ls.40은 OEM과 대응한다. 다만 동명 원시 SimpleAccess 직접선언은 검색에서 미확보다. 가공 Inputs.MV06_Open DB13.X6.7 선언과 Word 복사는 독립 확인했다.
3. DB13.X6.7은 NOT 없는 Word 전달과 별도 보존 Writer가 있다. 출력허가의 NOT 접점947을 입력반전 또는 물리 NC 정상값으로 혼동하지 않는다. 수동 Flag.MV06_Open은 센서 기억값이 아니다.
4. P&ID/시공 LS34/35와 OEM LS40/41의 일대일 대응은 미확정이다. 시공8_19를 LS40 전용 케이블로 배정하지 않는다. HMI DB11.X28.3의 실인수 선언 결속도 미완료다.

## 1. 설비·자료 기준 — 적용, 실물 대응 미확정

OEM Electrical_Rev2.pdf 실제34쪽 FG33 제목 MOTORIZED VALVE MV-06, LS-40 열림·LS-41 닫힘·ZT-06 엔코더가 별 경로로 그려져 있다. FG33 기본일27.05.2024, 개정란 공란. 실제123쪽 FG122 DIGITAL INPUT MODULE는 기본일27.05.2024 및 Rev2 17.03.2025다. 파일명 Rev2를 FG33 개정으로 대입하지 않는다.

PID_1684n002I.pdf 실제1쪽 Overflow valve MV-06/M14 주위에는 LS-34, LS-35, ZT-06, 0.25kW 440V가 표시된다. LS40 표기로 동일화하지 않는다. 도면1684n002, Apex I, 기본일06/04/2011; H 01/08/2012 ADDED MV-06 및 MV-03 command instrument 수정; I 15/01/2013 MC-05 제거/FN-02 출력 변경. 실제 확대 렌더로 확인했다.

Electrical_Can_Decoating_20241118.pdf 실제33쪽 footer33/64, CANDC-CONS-E016-033/D-PAGE16, 실제58쪽 footer58/64, CANDC-CONS-C008-058/D-PAGE8. 두 쪽 Rev1 24.11.11 first draft design이다. 준공/현장 설치 확인으로 승격하지 않는다. 초기 축소화면에서58/76처럼 보인 후보는 원본3배 확대에서58/64로 해소했고 다른 초안은 수정하지 않았다.

LS40은 종단 위치 입력 구성품이며 M14 모터, 방향출력 Q1.1/Q1.2, 방향응답, 엔코더 ZT06, 공유30AS1 인버터와 구분한다. 현재 CPU·실물·현행 장치 모델·정상극성·보호설정·현장복구는 미확정이다.

## 2. I/O·HMI — 원시·가공·요청·표시 구분

이하 NNNN은 all-in-one/sources/decoded-original/NNNN-FlgNet.xml 또는 명시한 IdentXmlPart.xml. RID는 같은 선언문맥에서만 결속하며 NID는 원본 네트워크, UID/Part/Wire/ORef/CRef는 해당 파일 내부 위치다.

| 계층 | 원본·선언/주소 | 해석과 경계 |
|---|---|---|
| OEM LS40 입력 | FG33 X1/64 E6.7→FG122 MOD9 단자28, LS.40 | 도면 직접 끝점. 현행 배선/CPU 확인 아님 |
| 백업 원시 색인 | live_index.json segment_7ev i657, Name mv06_open, Address %i6.7, Bool, Comment limit switch ls.40 | 도면과 대응하는 색인. 동명 SimpleAccess 직접선언 미확보를 유지 |
| 가공 열림 |0619 Global RID181 AO55 BAD168;0618 DepDB RID168 Inputs TOD13 | Bool DB13.X6.7, NID9 UID840/856 Read. 다른 Write 때문에 raw와 항상 같다고 단정 불가 |
| 짝 가공 닫힘 |0619 RID182 AO56 BAD168 | DB13.X7.0. LS41쪽 경계이며 LS40 소유로 합치지 않음 |
| 수동 열림요청 |0619 RID94 AO85 BAD5;0618 Flag RID5 TOD2 | DB2.X10.5, NID9 UID843 Reset Write,845/852 Read. LS40 상태 기억이 아님 |
| 수동 닫힘요청 |0619 RID93 AO86 BAD5 | DB2.X10.6. 열림요청Reset OR의 한 조건 |
| 자동모드 |0619 RID81 AO53 BAD5 | DB2.X6.5. 센서 자체 상태 아님 |
| 방향출력 |0617 SimpleAccess RID98 Open MV06 Output AO9, NID9 UID857 Write | Q1.1, 모터 방향명령. 센서에 독립 출력/코일을 만들지 않음 |
| 반대 방향출력 |0617 RID97 Close MV06 Output AO10, NID9 UID855 Read/866 Write | Q1.2, 열림허가에 NOT으로 소비 |
| HMI 열림한계 |hmi_plc_tags.csv ID0040A MV_06\LimitSwitchOpen DB11,X28.3 | 설정 태그. DB13.X6.7과 주소가 다름; 현재 표시/이벤트 검증 아님 |
| HMI 닫힘한계 |동일0040B DB11,X28.4 | 짝 부모 표시; LS40로 통합 금지 |
| HMI 요청/고장 |0040C Flag_OPEN DB2,X10.5;0040D Flag_CLOSE DB2,X10.6;0040E Allarme1 DB11,X28.2 | 요청·고장·종단 응답을 구별 |

CSV 부모8행 중 OutputOpen00046 DB11,X28.0, OutputClose00312 DB11,X28.1, AutoMan00047 DB2,X6.5도 확인했다. LS40 이름 전용 HMI 태그와 독립 MEM_OPEN/CLOSE 래치는 미확보. 검색 음성결과는 전체 TIA·간접주소·바이너리의 부재 증명이 아니다.

0364 LAD1187 NID10: CRef23/RID639, CodeBlock22/RID130은0624 BlockInterfaceInfo/0623 FCBlock HMI Standard Motorized Valve FC10으로 결속된다. 입력 Limit_switch_Open은 W42/ORef43/RID703, Limiti_Switch_Close는 W44/ORef45/RID702. 출력 Limit_Switch_Open_HMI는 W54/ORef55/RID144, Close_HMI는 W56/ORef57/RID146이다. 방향과 Bool 인터페이스는 확인했으나 이 실인수의 같은 문맥 선언 미결속으로 DB13→DB11 전 전달은 확정하지 않는다. 다른 블록의 RID703/144를 번호만 보고 가져오지 않는다.

## 3. 제어 구조 — 열림 입력과 소비 경계

### 3.1 원시 Word→처리 Word

0397 LAD1070 NID1: Powerrail W21→Move42.en. in W52/ORef45/RID13은0627 SimpleAccess Tag_171 Word Input AO48=IW6. out1 W54/ORef46/RID14는0629 Global Word AO48/BAD4이며0628 DepDB RID4 Inputs TOD13으로 DB13.DBW6이다. 따라서 두 바이트에 I6.7와 I7.0이 포함되는 Word 전달이다. 이 복사에 NOT은 없다. DisableENO=true 및 W53의 다음 Move43.en 연결 원문도 보존하며 그 이후 가지의 실행의미는 이번 대상 판정에 이용하지 않았다.

0030 main 호출 조건/순서는 MV06 초안의 공통 근거를 재사용하고 이번에는 전체 호출 재검토를 주장하지 않는다. 현재 CPU 실행·다른 Writer·최종값은 미확정이다.

### 3.2 열림 입력 소비와 수동요청 Reset

0349 LAD1711 NID9:

- Powerrail W967→NOT ON Contact915(operand W27/ORef28/RID1)→W916→NOT ON Contact917(W21/ORef22/RID1)→W918. 0617 SimpleAccess RID1 ON Memory AO0=M0.0의 같은 값 두 번 부정접점을 보존한다. 정상 논리로 임의 수정하지 않는다.
- W918→양 접점919, operand W869/ORef840/RID181=DB13.X6.7. out W67→OR790.in1.
- OR790.in2는 Contact921 Flag.MV06_Close(W870/ORef841/RID93)→W922, in3는 Contact923 MV06_Auto(W871/ORef842/RID81)→W924. OR out W71→RCoil794, operand W874/ORef843/RID94=Flag.MV06_Open DB2.X10.5 Reset.
- 열림 명령 말단은 NOT Close MV06 Q1.2 Contact945(operand W894/ORef855/RID97)→W946→NOT Inputs.MV06_Open Contact947(operand W895/ORef856/RID181)→W948→일반 Coil821, operand W897/ORef857/RID98=Q1.1이다.

가공 열림값은 요청Reset 가지의 양 접점과 방향 출력허가의 부정 접점에서 소비된다. 접점947의 NOT은 0397 입력 Word 반전을 뜻하지 않는다. 실제 NC 열림/눌림/고장 상태의 0/1 및 작동점을 이 정적 식만으로 확정할 수 없다. 고장·자동/수동·압력/PID/Shot 허가의 전체 앞단은 부모 소유로 유지한다.

### 3.3 다른 Write — 보존0403 정적 근거

0403 LAD1083 NID2의 Ge632(Int) pre는 Powerrail W21, in1 W92/ORef94/RID327=Pot_MV06, in2 W93/ORef95/RID253=Int98, out W91→일반 Coil633, operand W684/ORef654/RID243이다.

0635 Global RID243 AO55 BAD5, NID2 UID654 AK=Write 및0634 DepDB RID5 Inputs TOD13이므로 이 목적지도 DB13.X6.7이다. 0635 RID327 AO1088/BAD247,0634 Data RID247 TOD1은 Pot_MV06 DB1.DBW136;0637 Literal RID253는 Int V98이다. 즉 보존 백업에는 Word 복사와 별도 일반 Coil Writer가 공존한다. S/R 방식 센서 기억 래치라고 쓰지 않는다.

이는 중지된 보존 블록의 텍스트 검토이며 실행/생성/행동시험 없음. ≥98을 실제 LS40 작동점·개도%·현재 설정값으로 채택하지 않는다. 현재 이 Writer의 활성/호출순서·전체 간접/외부쓰기 완전성은 미확정이다.

### 3.4 엔코더 경계

ZT06 초안에서 확인된0516의 NOT raw MV06_Close I7.0 gate는 LS41 쪽 종단 경계다. LS40 열림DB13.X6.7 또는 열림 원시I6.7로 치환하지 않는다. 엔코더 누적값·환산Pot·기억 저장은 종단 입력과 별개이며 이번 LS40에서는 그 전체 연산을 재조사하지 않았다.

## 4. 전기 전달 경로 — OEM 직접 양 끝점, 시공 대응 미확정

| 단계 | 실제 원본/핀·선번 | 확인·미확정 |
|---|---|---|
|공급|Electrical_Rev2.pdf FG33/PDF34 +24Vdc10.7 상단버스, 좌32/9→우34/3|LS40/41 분기 접속점 존재. 실제 전압측정 없음 |
|LS40 공급단자|X1/63, 5×20 2A F 인쇄→33.5|도면 표기이며 현행 퓨즈/교체값 승인 아님 |
|위치 접점|LIMIT SWITCH VALVE OPEN, LS-40 접점11/12 NC기호|현재 정상극성/현장 작동점 미확인 |
|회수 단자|접점12→X1/64→E6.7, crossref122/7|중간 접속선을 시각 확인 |
|PLC 끝점|FG122/PDF123 E6.7 crossref33/5→CPU515 MOD9 단자28 LIMIT SWITCH LS.40|원시I6.7 색인과 대응. 현재 모듈 설치/프로젝트 일치 미확인 |

FG33의 LS41 X1/65~66/E7.0과 ZT06 X1/58~62/33.1~4/33SCH1은 별 경로다. LS40과 공통 버스라는 이유로 동일 접점/펄스 회로로 합치지 않는다. LS40 독립 PLC 출력·모터/밸브코일·별도 보호설정을 만들지 않는다.

시공33 route13 branch1은 FLO4TB2→LS-34, Flexible16, MV-06,8_19 =FLB+MV06-LS34A,CVV1.0/2이다. branch2는 LS35의8_20이며 branch3는 ZT06의8_21이다. OEM의 LS40과 동일 실물인지 증거가 없으므로 어느 branch도 LS40 전용으로 배정하지 않는다.

시공58에는:
-8_19 FLO4TB2→LS-34, DC CVV2C1.0 spare0,E1310,Adjustment3,LEN3.
-8_20 FLO4TB2→LS-35, DC CVV2C1.0 spare0,E1320,Adjustment3,LEN3.
-8_17 UC01 FLO4TB1→MV06 FLO4TB2 LS34/35, =FLB+MV06-FLO4TB2A, DC CVV7G1.0 spare2,Adjustment8,LEN9.
-8_6 CR→MV06 FLO4TB2 ZT06, 같은 =FLB+MV06-FLO4TB2A, TM CVV-S4S1.0 spare0,Adjustment12,LEN63.

같은 ID의8_6/8_17은 시작점·신호·규격이 다르므로 하나로 합치지 않는다. FLO4TB2의 시공33 LOC UC01 표기 또한 부모소유 변경 근거가 아니다. X1/63~64와 FLO4TB2 내부 단자간 승인 결속표가 없으므로 준공 연결을 그리지 않는다. 검게 가린 행을 복원/활성경로로 가정하지 않았으며 LEN은 실측 길이가 아니다. 부모 공통 접촉기/인버터 및 EV 69KA/71KA의5–9 정정은 별 근거로 보존하고 LS40 소유로 복제하지 않는다.

## 5. 알람·복구 — 독립 전용 근거 미확보

LS40 독립 진단번호·도달타이머·Set/Reset 알람은 확보하지 못했다. MV06 초안의 MV_06_FAULT DB3.X11.6와 방향응답150ms/누적W19>2200,W20<−2200은 부모 공통고장이다. 이번 고유 조사에서 부모 알람 전체를 재검토하지 않았고 LS40 미도달/센서 자체 고장으로 복제하지 않는다.

HMI DB11.X28.3 한계표시, DB11.X28.2 부모고장, raw I6.7, 가공DB13.X6.7, 요청DB2.X10.5, 출력Q1.1은 별 관찰값이다. 요청Reset·알람소멸·접점변화·실제위치 복구는 같지 않다. 현재 고장이력·복구확인 증거 없음.

## 6. 증상별 관찰 — 읽기 전용 비교 기준

| 증상 | 필요한 기록/비교 | 판단 경계 |
|---|---|---|
|도면 LS40와 현장 LS34 이름 혼재|각 명판/부착위치·승인 대응표·FLO4TB2/X1 단자표|이름/부모 일치만으로 병합하거나 네 실물 확정 금지 |
|원시와 화면 열림표시 불일치|동일시각 I6.7,DB13.X6.7,DB11.X28.3 및 현재 프로젝트ID/호출|CSV만으로 표시 갱신·극성 확정 불가 |
|원시와 가공값 불일치|0397 Word 복사,0403 보존 Writer의 현재 활성/순서 자료|보존 Writer 존재만으로 현행 원인 확정 금지 |
|열림 요청 사라짐|0349 R794 앞단NOT ON·InputsOpen/FlagClose/Auto 조건|요청 해제를 실물 열림완료로 해석하지 않음 |
|열림 출력 억제|Q1.2와947 NOT DB13.X6.7 및 부모 다른 허가 기록|접점우회·강제출력·설정변경 제안 없음 |
|복구 판단 필요|권한있는 현장 관찰자·시간대/시각·실제위치·신호전후·프로젝트일치|문서검사/알람없음만으로 복구완료 불가 |

현재 관찰/운전시험/접점 조작은 수행하지 않았다. 보호값 변경 또는 시뮬레이션으로 누락을 채우지 않는다.

## 7. 완료·누락·인계

| 영역 | 적용 상태 | 남은 자료 |
|---|---|---|
|설비·자료 기준|적용/정적초안|LS40 실물 및 LS34/35 대응표 |
|I/O·HMI|적용/부분 미결속|원시 SimpleAccess 결속,현재 TIA/CPU,HMI 실인수/이벤트 |
|제어|적용/입력 전달·소비·다른쓰기 정적 검토|현재 호출순서/활성·간접쓰기 |
|전기 끝점|OEM 직접 적용/시공대응 미확정|FLO4TB2→X1 승인 단자표·배선/극성 |
|알람·복구|독립 전용 근거 미확보|전용진단 여부 및 실제복구기록 |
|증상관찰|적용/자료수집 기준|현재 값/관찰 없음 |
|완료기준|complete_with_gaps 문서 인계|통합자 독립검토 필요 |

문서/정적검토만 완료 범위다. 도면·래더 비교용 근거를 마련했지만 비교UI,백업 미리보기/선택복원,기록전후비교,보고서/PDF 도구는 미구현/미검증으로 BC01 동등 구현완료가 아니다. ui_records not_run, publication not_published, tia_compile/live_cpu/field_recovery not_performed. 원본 preflight·생성기·회귀·앱빌드는 실행하지 않았다. 이미 존재하는 사용자 메모·운영기록/미지필드/저장키는 건드리지 않았다.

다음 한 작업: 통합자가 LS40 OEM 열림경로와 XML 입출력/다른쓰기 경계 및 미결속 범위를 독립 검토한다. 현장 자료 없이는 LS34/35↔LS40/41 식별보류를 재검색으로 해소하지 않는다.

## 부록 A. 선정 원본 SHA256 / 고정 Git blob 바이트 대조

선정 33파일. 해시검사수는 의미검토수와 다르다. 경로는 source-mv06 기준이며 아래 전부 고정커밋과 바이트 일치다.

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
| `all-in-one/sources/live_index.json` | `14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1` | `e35ccea1f841349c632666c29954b7bcd4f5839e` | True |
| `all-in-one/sources/decoded-original/network-map.json` | `c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60` | `424430b6b953e43138e5d0a18ca40c949e21cfa1` | True |
| `all-in-one/sources/decoded-original/0349-FlgNet.xml` | `2f45af21543189d83f027afbae797532cae5d55935bac1fba3913825d741863b` | `7082fb0a8817f254ae1ac0087990478f2de30791` | True |
| `all-in-one/sources/decoded-original/0397-FlgNet.xml` | `bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834` | `4ab8370493c4e28fc1eabeeebe2743d27f0c4021` | True |
| `all-in-one/sources/decoded-original/0364-FlgNet.xml` | `c23a9952251a48105eedd1ed3c185f781b6163d094fb3bb396ac27415587de8a` | `dee7f6d4c8d0675deb1c4bb5c5eb78392ae43c57` | True |
| `all-in-one/sources/decoded-original/0403-FlgNet.xml` | `77b03e38aa857ac8dd404f2f66a56256939b4e7924b41334a7981b86089c1e6b` | `4c806e31eb65f00cbb7870c72896ac26a8bc3dd3` | True |
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

## 부록 B. 정적 검사 결과와 시각

- 검사 2026-10-11T14:30:04.964088+00:00 UTC. 선정 33파일, 전체 sources 712파일, 중지 5자산 모두 고정 Git blob과 바이트 일치. Git status clean. 이는 현재 CPU나 현장 동일성 검증이 아니다.
- XML 695파일 LS40 경계문자열 검색결과 0파일, HMI LS40 이름검색 0행. 전체 논리검토수가 아니다. raw mv06_open의 동명 SimpleAccess 미확보이며 live_index657은 색인근거로 구분했다.
- 의미검토 FlgNet4개는0349 소비/Reset/출력말단,0397 Word 전달,0364 HMI핀/미결속,0403 다른쓰기 한정. 관련 선언11개에서 해당RID를 확인. PDF5쪽 및 P&ID2개/시공58개정란 확대를 독립 시각 확인.
- extracts/LS40/source-hashes.json,source-preservation-hashes.json,stopped-assets-preservation.json,static-review.json에 검사기록. declaration-search.json과 live-index-657.json은 탐색/선언 발췌.
- 14:24 UTC 범위/표준 읽기 시작,14:25~14:26 PDF/선언/핀·끝점 대조,14:26 footer58/64 확대확인,14:29 초안과 보존검사. 부모 전체/다른 보류ID 재조사나 운영 변경 없음.
