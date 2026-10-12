# SS01 이송 장치 감시 스위치 — 7영역 원본 조사 초안

- 대상: catalog SS01 / sensor / 계측 / 부모 BC01 / phase2. 부모 완료를 상속하지 않은 별도 조사다.
- 고정 읽기전용 원본: `source-mv06`, Git `abcf31c5030bc7ef8749ed8e869a857f2387a28a`, v1.12.0. 아래 원본 경로는 이 루트 기준이다.
- 실제 착수 2026-10-11 12:37:49 UTC; 원본·PDF 핵심 대조 12:38~12:40 UTC; 해시/검사 기록 12:41:05 UTC. 모델 런타임 증명 미확인.
- 문서 조사만 수행했다. TIA/현재 CPU/실물/현장 복구/보호값/SEJIN 변경 및 시뮬레이터 실행·수정·생성·행동시험은 수행하지 않았다.

## 먼저 볼 핵심 확인·상충·누락

1. 실제 OEM 도면은 **SS-01 트립와이어**와 **SSL-01 R.P.M. CONTROL SWITCH의 SPARE 회로**를 구분한다. 대장 별칭 `bc01_tripwire`, `bc01_prox`, `ssl-01`이 하나의 설치된 실물이라는 뜻은 아니다.
2. SS-01의 기동 직렬 접점 **11/12**와 PLC 감시 접점 **13/14**는 점선 기계연동으로 그려져 있다. 전기적으로 동일 접점이나 동일 신호가 아니다.
3. 원본 1786 / `0423-FlgNet.xml`에서 FC 알람은 처리 입력=1일 때 Set, 처리 입력=0·Reset·기존 알람일 때 Reset이다. **이 네트워크에는 타이머가 없다.** 부모 BC01의 Tag_51/%T39·S5T#2S를 SS01 지연으로 복제하지 않는다.
4. `UNDER TESTING`은 원본 1935의 FC에 의한 소프트웨어 운전요청 Reset 분기에만 나타난다. 현장 직렬 접점을 대체·우회할 수 있다는 뜻이 아니다. 어떠한 조작 절차도 제안하지 않는다.
5. HMI CSV는 부모 BC01의 응답·종합알람 주소를 제공하지만 SS01 전용 화면/이벤트를 확정하지 못한다. 0357 호출의 Allarme2 연결은 XML 핀과 색인 후보를 분리해 기록한다.
6. 시공 케이블표 3_19의 ENT1TB2 설명에는 `PV-01 A GATE`가 남아 있다. BC01/SSL01 태그와 설명 상충을 보존하며 임의 수정하지 않는다. 시공표 존재는 OEM SPARE의 실제 설치를 증명하지 않는다.

공유 근거: 고정 원본의 `all-in-one/signal-guides/BC01.html`, `control-specs/BC01.html`, `registers/electrical-trace.csv`, `construction-cables.csv`를 색인으로 재사용했다. 고유 알람·하위 입력·부모 정지분기·HMI 경계·실제 PDF 4쪽은 SS01에서 독립 대조했다. 파생 표에 쓰인 ‘회전 감시 예비’는 도면 표제와 SPARE 범위일 뿐 현재 센서 종류/설치 확정이 아니다.

## 1. 설비·자료 기준 — 적용, 실물 미확정

`docs/equipment-standard/INVENTORY.json#/catalog/109`는 SS01을 BC01 하위 sensor로 분류한다. 별도 catalog ID이므로 BC01과 합산·동일물 병합하지 않는다. 배치 범위와 중복검토의 `parent_child_separate`, physical_identity_verified=false를 유지한다. SS09/SS10/SS11은 같은 한국어 이름을 갖지만 별도 ID다.

PLC 백업명 GME_20250506.zap18과 내부 프로젝트 날짜, 도면 날짜, 실제 설치 날짜는 다르다. 이번 조사는 고정 저장소 내용만 증명하며 현재 CPU와 최신 로컬 기능을 검증했다고 주장하지 않는다. 원본 AGENTS/작업표준/스킬/템플릿을 읽되 이번 승인 범위인 문서 조사만 적용했다. 원본 생성기·build/test·preflight 스크립트는 실행하지 않았다.

## 2. I/O·HMI — 적용, 주소와 표시 소유 구분

### 입력과 처리값

| 신호 | 원본 위치·형식 | 해석·경계 |
|---|---|---|
| `bc01_tripwire` | `sources/live_index.json` _7ev i952, Name/Address `%i6.2`, Bool, Comment `limit switch ss-01`; `registers/plc-symbols.csv` 일치 | OEM E6.2와 대응하는 백업 원시 디지털 입력. 현재 접점 정상극성/실제 전압은 미확정 |
| `bc01_prox` | 같은 원본 i973, `%i6.3`, Bool, `limit switch ssl-01` | OEM SPARE SSL-01의 별도 입력. 이름으로 펄스/속도 계산을 만들지 않는다 |
| `Tag_171` | 같은 원본 i1600 `%iw6`, Word; `0627-IdentXmlPart.xml` Global SimpleAccess RID13, NID1 UID45, Input AO48, 16bit | I6/I7 영역 Word 읽기. PIW/주변장치 직접 접근이라고 바꾸지 않는다 |
| `Inputs.BC01 trip wire` | `0657-IdentXmlPart.xml` Global RID266, NID6 UID242/245, Bool, AO50/BO50 | DB Inputs의 bit offset50, 즉 byte6 bit2 처리 입력. 원시 심볼과 이름은 다르다 |
| `Allarm.BC_01_FC` | `0657` Global RID33, NID6 UID243/246/247, Bool AO26; UID243/247 Write | bit offset26의 Set/Reset 기억 알람. 센서의 실물 복구 상태가 아님 |
| `Flag.RESET_ALLARM` | `0657` Global RID13, NID6 UID244, Bool AO48 | 내부 Reset 조건. 원시 `%I19.7 reset_allarm`과 직접 동일 신호로 합치지 않는다 |

원본 1070 / `0397-FlgNet.xml`: Part42 Move, Wire52 ORef45(RID13)→42.in, Wire54 42.out1→ORef46(RID14). `0629-IdentXmlPart.xml` RID14는 Global Word 16bit AO48, NID1 UID46 AK=Write. 색인 network-map의 절대주소 `%DB13.DBW6`와 Word 목적 오프셋48이 부합하며, 처리 trip wire의 BO50이 이 범위에 든다. 이 연결은 개별 Bool Coil이 아닌 **Word 쓰기**다. 첨부 전 2026-10-11 12:45:14 UTC 좁은 범위 추가 확인: `0629` RID14의 BAD BIRID4→`0628-IdentXmlPart.xml` DepDBBlock RID4, Name Inputs, TOD N13/BT DB, ID 목록에14 포함, NID1 UID46 Write가 일치한다. 처리 입력은 `0657` RID266의 BAD BIRID247→`0655-IdentXmlPart.xml` DepDBBlock RID247, Name Inputs, TOD N13/BT DB, ID 목록에266 포함, NID6 UID242/245가 일치한다. 두 DepDBBlock은 CID638561979615757134 및 TRKG5076ccf4-a9e8-4624-861d-1a2b9f16ecaf도 같아 **각자 올바른 문맥에서 동일 DB13**에 결속된다. 따라서 Word 목적 `%DB13.DBW6`와 처리값 `%DB13.DBX6.2`를 원형 선언으로 확인했다. RID 숫자만으로 두 문맥을 섞지 않았다. 다른 Word/대체 writer의 모든 실행 순서를 검증한 것은 아니다.

### HMI

`all-in-one/sources/hmi_plc_tags.csv`에는 `BC_01\RispostaA=DB11,X0.0`, `BC_01\Flag=DB2,X0.0`, `BC_01\Allarme1=DB11,X0.1`가 있다. 이는 dde.cfg 설정 추출이며 온라인 값이 아니다. 검색한 CSV에서 SS01/SSL01/트립와이어 전용 HMI 태그는 확보하지 못했다.

원본 1178 / `0357-FlgNet.xml`: CRef23 RefId638 / CodeBlock22 RefId1; Wire30 ORef31 RefId16→23.Allarme2, Wire40 23.Comulativo_allarmi→ORef41 RefId773. network-map의 index_code는 Allarme2 입력 후보를 Allarm.BC_01_FC로 제시하지만 이 호출의 resolved_operand_count=0이며 대응 Global 선언이 본 검토에서 결속되지 않았다. 이를 확정된 SS01 전용 HMI 알람이라고 표현하지 않는다.

공통 함수 원본 331 / `0355-FlgNet.xml`과 `0621-IdentXmlPart.xml`: 입력 Allarme1~5는 **Local InterfaceAccess**다. Allarme2 RID19/NID1 UID37→Part36 operand(Wire35), Part36.out→OR Part41.in2(Wire43). OR41은 5입력, out Wire57→Coil59.in, Wire58 ORef60/RID22→59.operand=Local Comulativo_allarmi. Local 파라미터를 Global DB11의 개별 SS01 bit로 직접 등치하지 않는다. 화면 버튼/ACK/스크립트/알람 이벤트 텍스트는 추가 원본이 필요하다.

## 3. 제어 구조 — 적용, 입력 호출과 소프트웨어 정지 경계

### 고유 트립 감시

원본 1786, allarms 1 NID6, `0423-FlgNet.xml`:

- ORef241/RID1=ON (`0658` Global SimpleAccess), Part258 Contact. Wire248 operand, Wire268 Powerrail→258.in.
- Wire259: 258.out이 Part260 및 Part262의 in으로 분기.
- ORef242/RID266=처리 trip wire, Wire249→Part260.operand. Wire261 260.out→SCoil234.in. Wire251 ORef243/RID33→234.operand=FC.
- Reset 가지: ORef244/RID13 Wire252→Part262.operand=Reset. Wire263→Part264.in; ORef245/RID266 Wire253→Part264.operand에 **Negated** 지정. Wire265→Part266.in; ORef246/RID33 Wire254→Part266.operand=기존FC. Wire267→RCoil240.in; Wire256 ORef247/RID33→240.operand=FC.

따라서 저장된 식은 Set=`ON AND Inputs.BC01 trip wire`; Reset=`ON AND Flag.RESET_ALLARM AND NOT Inputs.BC01 trip wire AND Allarm.BC_01_FC`. 물리 접점의 정상/고장 전압을 이름만으로 이 식에 덧붙이지 않는다.

### 입력 전달 호출

원본 1613 / `0030-FlgNet.xml`는 CRef21.eno→CRef23.en(Wire32), CRef23.eno→CRef25.en(Wire33), CRef25.eno→Contact37.in(Wire42), ORef45/RID140 Simulation(1)→37.operand(Wire44, Negated), 37.out→CRef28.en(Wire43). 색인의 CRef28 후보는 HMI inputs다. 실행 호출조건/ENO 결과는 현재 CPU에서 확인하지 않았다. 0397 Move에는 DisableENO=true 표시가 있으므로 그림의 eno 연결을 무조건 성공이라고 단정하지 않는다. 기존 백업 호출 경계만 읽었으며 중지된 시뮬레이터 내용 분석·실행은 하지 않았다.

### 부모 BC01에 미치는 영향

원본 1935, motors1 NID6 / `0242-FlgNet.xml`:

- `0604` Global RID39/UID206=Allarm.BC_01_FC. Wire215→Part233.operand.
- Part233.out Wire38→Part237.in; `0602` Global RID4/UID208=UNDER TESTING, Wire218→Part237.operand **Negated**.
- Part237.out Wire238→OR190.in3. 다른 in1은 BC_01_FAULT(Part229), in2는 BC01_INV(Part22). ON Part227.out Wire228이 세 가지에 공통 공급.
- OR190.out Wire220→RCoil198.in; Wire222 ORef209/RID41→198.operand=Global Flag.M_BC_01 (`0604`, NID6 UID209 Write).
- 결과는 ON AND [FAULT OR INV OR (FC AND NOT UNDER TESTING)]일 때 부모 운전요청 Reset이다.
- 별도 출력: Part239=Flag.M_BC_01; OR43에 R1_GATE_LOOP_ON/ MemoCMD_BC01_Startup/ Maintenance_ON 세 갈래; Wire45→Coil202.in, Wire225 ORef211/RID42→202.operand=Start BC01. `0602` NID6 UID211 Write, 원시 심볼 `%Q0.0`.

SS01이 모터명령 자체를 직접 쓰는 것은 아니다. 부모 요청에는 다른 Set/Reset writer도 있어 위 식만으로 전체 최종출력·재시작 순서를 확정할 수 없다. 원본 심볼 설명의 옛 A48.1과 실제 Address Q0.0은 별도로 보존한다.

## 4. 전기 전달 경로 — 실제 PDF 렌더 4쪽 대조

PDF 쪽수는 1부터 센 실제 페이지다. 모든 FG를 ‘PDF−1’로 일반화하지 않는다. 이번 직접 대조에서만 FG18=PDF19, FG19=PDF20, FG122=PDF123을 확인했다.

| 원본/판본·실제 페이지 | 직접 확인한 끝점 | 경계 |
|---|---|---|
| `sources/Electrical_Rev2.pdf` FG19/PDF20, 제목 FEEDING ROTATION DRUM CONVEYOR BC-01, DATA27.05.2024, Rev2 17.03.2025 | +24Vdc10.7→X1:46(5×20, 2A F)→SS-01 13/14→X1:47→E6.2→122/3 | 감시 접점 회로. 2A F는 도면 표기이며 현행 보호값 검증/변경 권고가 아님 |
| 같은 FG19/PDF20 | A0.0(136/1)→X1:44(2A F)→SS-01 11/12→X1:45→XS:1→18QS1 보조접점→XS:2→18QM1 보조접점→19KA1 코일 A1/A2→0Vdc10.6 | SS-01 접점13/14와 점선 기계연동. PLC 입력과 독립된 기동 직렬 회로 |
| 같은 FG19/PDF20 | +24Vdc10.7→X1:48(2A F)→SSL-01 13/14→X1:49→E6.3→122/4 | 점선 SPARE 상자 내 R.P.M. CONTROL SWITCH BELT CONVEYOR. 실제 설치/속도/타이밍은 미확정 |
| 같은 FG122/PDF123, DIGITAL INPUT MODULE, DATA27.05.2024, Rev란 공란 | E6.2/19/3→단자23, E6.3/19/4→단자24; CPU515 MOD9 표기; E6.3 SPARE | 백업/도면 모듈 표기만 확인. 현재 CPU 형식/슬롯 검증 아님 |
| 같은 FG18/PDF19, DATA27.05.2024, Rev2 17.03.2025 | 18AS1 +24Vdc 단자9→19KA1 부하접점5/9→단자12 DI1 START, 도선18.1/18.2 | 실제 그린 부하 경로는5/9. FG19 하단 접점표1/5/9와 혼동하지 않는다. ABB 모델 표기는 부모 범위이며 현재 모델/설정 검증 아님 |
| `sources/Electrical_Can_Decoating_20241118.pdf` 실제PDF53, CANDC-CONS-C003-053, footer53/64 D-PAGE3, Rev1 24.11.11 first draft design | 3_1 CR→BC01 ENT1TB1 SS01, CVV7G1.0; 3_18 ENT1TB1 ENTRY joint box→BC01 SS-01, CVV5G1.0, E100 | 시공 계획 케이블 끝점과 현장 결선 확인은 다름 |
| 같은 PDF53 | 3_2 CR→BC01 ENT1TB2 SSL01, CVV3G1.0; 3_19 ENT1TB2→BC01 SSL-01, CVV2C1.0, E100 | 3_19 설명 PV-01 A GATE 상충 보존. 설치 확정 불가 |

실제 렌더 PNG·페이지 텍스트는 extracts/SS01에 별도 보관했다. 출력 FG136의 PLC 모듈 끝점은 FG19 교차참조로만 남기고 이번에 직접 렌더 확인했다고 주장하지 않는다. 감시 입력 끝점 FG122는 직접 확인했다.

## 5. 알람·복구 — 적용, 현장 복구 미확정

- 고유 FC 발생/유지는 0423의 SCoil234/RCoil240에 근거한다. 입력이 사라지는 것만으로 기억 알람이 자동 Reset되는 식이 아니다.
- 이 FC 네트워크에는 TON/SD/TP 또는 시간 상수가 없다. 부모 1785 / `0422-FlgNet.xml`의 Tag_51 타이머·S5T#2S는 BC_01_FAULT/BC01_INV 검출 범위다. SS01 감시 지연으로 상속하지 않는다. 광범위 모든 네트워크에 지연이 없다고 주장하는 것은 아니다.
- 0242의 FC Reset 영향과 FG19의 하드웨어 기동 차단 접점은 서로 다른 계층이다. 소프트웨어 알람 해제, 물리 접점 복귀, 실제 운전 재요청, 모터 운전 확인을 하나의 ‘복구’로 묶지 않는다.
- SS01 전용 ACK/HMI 경보 문구와 PLC Reset 요청 발생원 전체는 미결속이다. 현재 정상극성·현장 래치/복귀 방식·와이어 장력/설치 규격·승인된 복귀절차 자료가 필요하다. 이름이나 회로 접점기호만으로 수동 조작 순서를 만들지 않는다.

## 6. 증상별 관찰 — 문서상 관찰 위치만, 시험·조작 미수행

| 증상 | 기록할 관찰값/근거 | 배제해야 할 오인·추가자료 |
|---|---|---|
| FC 알람이 남음 | 같은 시각의 원시I6.2, 처리 Inputs bit50, FC bit26, 내부 Reset bit48 및 현재 프로젝트 식 | 원시 입력=처리값, 원인소거=Reset 완료라고 단정 금지. 호출/Word 전달·현장 입력 대조 필요 |
| BC01 요청은 있으나 모터 기동 안 됨 | 승인된 기존 관찰 자료의 Q0.0, X1:44/45, SS-01 11/12, XS1/2, 19KA1 상태, 18AS1 DI1 | 출력 요청=현장 허가로 등치 금지. 유자격자 승인 절차의 관찰자료 필요; 점퍼·강제출력 제안 없음 |
| HMI 종합알람만 보임 | DB11 X0.1 표시 시각과 FC/FAULT/INV 개별 기록, 호출/화면 정의 | 종합알람 이름 Allarme1을 SS01 단독 알람으로 오인 금지 |
| E6.3 값이 없거나 변함 | SSL01 설치 유무·명판/현장사진, FG19/122 SPARE, 케이블3_19 양끝 자료 | 예비 입력을 회전 정상 신호나 안전대체 입력으로 지정 금지 |
| 트립 처리값과 현장 상태 불일치 | 도면 개정·실배선과 원시/처리 값·시각/프로젝트 근거 | 접점 정상극성·스캔·ENO·대체쓰기 확인 필요. 소프트웨어 이름만으로 현장 고장 판정 금지 |

실제 운영자료는 수집/복제하지 않았다. 향후 관찰 기록에는 관찰자·시간대·위치·값/단위·수집 장치·프로젝트/도면판본·비교근거·조치 승인 및 복구 증거를 구분한다.

## 7. 완료·누락·인계

| 항목 | 상태 |
|---|---|
| documentation | complete_with_gaps: SS01 고유 7영역 문서 조사 초안 |
| static_review | selected_source_review: 핵심 핀/선언·4쪽 PDF·41선정파일 해시 확인, 독립 검토 대기 |
| ui_records / publication | not_run / not_published: 화면·저장·복원·게시 작업 없음 |
| tia_compile / live_cpu / field_recovery | not_performed / not_performed / not_performed |

필요 자료: SS-01/SSL-01 실제 명판·위치·승인 as-built/접점동작표, 정상전압/복귀조건의 유자격자 확인 자료, OEM SPARE의 실제 설치 여부, 현행 CPU 프로젝트 비교, HMI 호출 선언/화면/경보 이벤트, 3_19 설명 상충 해명. 새 자료 없이 실물 보류를 반복 조사하거나 완료로 바꾸지 않는다.

BC01의 네 기능(도면·래더 나란히 보기, 백업/선택복원, 전후기록 비교, 보고서/PDF)은 SS01에 구현/검증하지 않았다. 원본 사용자 note/repair_observation·미지필드·다른 설비/초안/저장키 변경 없음. 이 MD 전달은 해당 기능 또는 통합/게시 완료가 아니다.

검사 산출물: `extracts/SS01/verification.json`, `source-hashes.json`, `xml-inspection.json`, `symbol-selection.json`, `catalog-selection.json`. XML 18개 파싱은 문법/추출 확인 수이며 18개 전체 논리 의미 검토 완료 수가 아니다. 핵심 의미 검토는 위에 인용한 네트워크/선언/핀으로 한정한다. 41파일 해시는 선정 근거+표준+공유색인+중지5 보존목록이며 원본 전체 의미 검토 수가 아니다. 원본 Git 상태 clean, 선정 전부 고정 Git 내용 동일, 중지5 해시 일치. 원본 수정0.

### 전체 선정 원본 해시표

아래 Git blob은 고정 커밋의 blob ID다. SHA256는 읽은 파일 바이트로 별도 계산했으며 Git show 바이트와 전부 일치했다. 중지5 파일은 해시만 확인했고 읽어 실행하거나 분석 대상으로 삼지 않았다.

| 원본 경로 | SHA256 | 고정 Git blob SHA1 | 내용 일치 |
|---|---|---|---|
| `AGENTS.md` | `0bdd77713c49fe21f60de00994be4805db90719857c4326a946bb1b93d15c2c2` | `073164bc6efd5791032d62c71b03b4dab48cb6f8` | 일치 |
| `.agents/skills/gme-equipment-rollout/SKILL.md` | `fb917fe49dbdafed32c7360bc015179d75008a90d8b2ddd8d1dcf68f5100510b` | `9aa820ea6ca15b4e136c9772423b78ed4df6a3d4` | 일치 |
| `docs/equipment-standard/WORK-STANDARD.md` | `05a57f4525bc1d59dab35ef841b64b0138a6ff08b10760ade64d9a688ee15e99` | `f76a570cc73098632e08759b17934000f7e3a253` | 일치 |
| `docs/equipment-standard/WORK-ITEM-TEMPLATE.md` | `4239b60b02270cd0db344b6f664395733f2587cf4d81c16ae629886b5a92c586` | `e546f39535d2b589e80f97db869ac37ce4d05cfd` | 일치 |
| `docs/equipment-standard/INVENTORY.json` | `720fa0066b926acd519f8aa0746f0c20acf3f02bac5b7a2fa5a8be43b77743dc` | `587c3748ad9224718f95ba06463fee913dae231d` | 일치 |
| `VERSION.json` | `5eda2586eb97d69cf158683579043910ad4735dcc731cc7e3ad940985f1adef7` | `fffb51663b7705aec91cb119ca80ee943a4ce758` | 일치 |
| `all-in-one/sources/Electrical_Rev2.pdf` | `5ee22a177bb3feebde85a326ee0272d8b7d8198a2bd7147f8d120ff8858636f6` | `f610fd7c7ce14ae951b00cff57b969259bfb389d` | 일치 |
| `all-in-one/sources/Electrical_Can_Decoating_20241118.pdf` | `3963f137b7a1a5a8ab6525c9e002046f8aa5ebbdee4799f41b0a0bad664a4dbd` | `0ee6b6f8361c5790864dbba4bbd9d55e8e7c08f8` | 일치 |
| `all-in-one/sources/live_index.json` | `14c1b5e9c5f96147f149693f79e9d94ed78363ec5d8fe27353fd53354647ffb1` | `e35ccea1f841349c632666c29954b7bcd4f5839e` | 일치 |
| `all-in-one/sources/hmi_plc_tags.csv` | `a5a22b082cb03aca20097f87bbfcb5f75b6f87e13d501f82282c514a9037d404` | `cf4c0650e7c7baac350dcb89909b808435704880` | 일치 |
| `all-in-one/sources/decoded-original/network-map.json` | `c2cab276545dc5d07c1a94ed746e7f4a8d4d725b8a962a1b27fe46c9b71c8f60` | `424430b6b953e43138e5d0a18ca40c949e21cfa1` | 일치 |
| `all-in-one/registers/plc-symbols.csv` | `a0334b390f06ddb515d6c09ca96a01d35d44029c1b726ef0ff53303ec04ff91f` | `cbc576c5d6e47498a3865304a1c23de9b4641d9f` | 일치 |
| `all-in-one/registers/equipment-io.csv` | `a7a1f27dc453af25b2b729074cac5266d6dd53c0945a6a1a4afe2dd1e9153b6a` | `d042a15edd5f2550dbbef40203f927da3360fe32` | 일치 |
| `all-in-one/registers/electrical-trace.csv` | `feebc37f6a506b97d1ae930f87659f89660898bc5476e171a37278ee47dc2a98` | `94e50f5e39f230477c4b3b8d03c5a33fc556846e` | 일치 |
| `all-in-one/registers/construction-cables.csv` | `a697a92c6e3df8fd4ba087f0ddc9478f46fd52d900ec81f4735ad25073adf51e` | `516bc49f30092e9d18d88596cb9dafb0d3c2e643` | 일치 |
| `all-in-one/signal-guides/BC01.html` | `36385ae65216db8cffc0ba73f544f6aee470f59b4a97c210728c5cf97063c11a` | `5a5d82e2433d88d14d26e7b71dfb6327e564bf06` | 일치 |
| `all-in-one/control-specs/BC01.html` | `9133b4497d73673097d0cc16bf1179df8adc0445ed0f8a73ba0898d3ecc0d7be` | `8bd3f428318347b397e751ad9e44310e7de10827` | 일치 |
| `all-in-one/registers/simulator-freeze.json` | `bb93c1994effc5609939ba566b7802ce7ed55154a7310f02379b308ac2c8c835` | `808ffac14dbd1b4a7d797fa6cd0d647635d90b47` | 일치 |
| `all-in-one/sources/decoded-original/0628-IdentXmlPart.xml` | `9f3778ffa85590a78f2f3844b08471385e95bd158820908d1add8e03f8f5c5bd` | `170ca5c72599edc7ea7eefe651c3680ce325e76a` | 일치 |
| `all-in-one/sources/decoded-original/0655-IdentXmlPart.xml` | `38e9f323024fba19582b473f39b1ed03ffe6a0b390218894029a6edb0b1ff9fb` | `83b60b9de4541a3ffa6ee0db98205a372b525665` | 일치 |
| `all-in-one/sources/decoded-original/0423-FlgNet.xml` | `b6567e6973d935866d943406a7113191c7767ebac658293fb15c742104903cb3` | `879e621ee6fb8d1d98893490c13aaa3643540770` | 일치 |
| `all-in-one/sources/decoded-original/0242-FlgNet.xml` | `aca0cbc07c04fae72012760899cba246fe65c78ae234cef59e6439dc1172b715` | `da672cbc6b0cad93f3b23e4ca65eae37b9630280` | 일치 |
| `all-in-one/sources/decoded-original/0397-FlgNet.xml` | `bc2eb353109f9585236d6083084613aa31623c8301866a3f72bb7ec682528834` | `4ab8370493c4e28fc1eabeeebe2743d27f0c4021` | 일치 |
| `all-in-one/sources/decoded-original/0030-FlgNet.xml` | `9252c9da764993de1edb8b2e44c46d6e9f9d4b6118e751a0dbeaa9ffd8ea721b` | `e74c70b751acdcdbc7a8b3b0c98aa773c2107cab` | 일치 |
| `all-in-one/sources/decoded-original/0357-FlgNet.xml` | `a0334f249d3b026599a24ab6e59645e045302e802f70ed0ecf7be8d830d46d3c` | `190480a9be7c3bc231442791aa3675c59c3778d4` | 일치 |
| `all-in-one/sources/decoded-original/0355-FlgNet.xml` | `73592d33f8b3a71effeb36f25427c76e931485e7ce31f5c81f144ddae83c4247` | `54f7a267c9b44c325fd5af31ea78736049d8b1ef` | 일치 |
| `all-in-one/sources/decoded-original/0422-FlgNet.xml` | `8ad017c574a431ebffe033d268fe85fb61b1492ec10e7a26b29f2b7f850d7f4f` | `62c00e2348748a980a0c4094bf4acc4695bcf4f4` | 일치 |
| `all-in-one/sources/decoded-original/0657-IdentXmlPart.xml` | `0f70cda60a6b1a17175876d58e25b2686952642de6cffb21213aeef8b347a22b` | `e625f3d8999c7be7d88c50eab0d93107117b58ec` | 일치 |
| `all-in-one/sources/decoded-original/0658-IdentXmlPart.xml` | `998294c0c8a99e00ceb33c2c60def2cd4850e34328917ae506244c2be2df3831` | `de9a12a6be87466ef1bf05df71c54580c556a827` | 일치 |
| `all-in-one/sources/decoded-original/0602-IdentXmlPart.xml` | `46ab21151eddaaf616469db520730c60423eb742aa491af194e6710c751b4caf` | `bcb12ab1ce8c476ff921baa1608f29d9822f76b4` | 일치 |
| `all-in-one/sources/decoded-original/0604-IdentXmlPart.xml` | `b798d29c5499b5314a1ee3cff9139dae64c887533b86baa43b6e9a052373a6af` | `bb2c318788b97e7a4924a176275c12d805aa519d` | 일치 |
| `all-in-one/sources/decoded-original/0627-IdentXmlPart.xml` | `08363fd28518a9c79f2c5b463956580c770614473d970f910a24dc7da423cefb` | `61ebc0abbb2ca160e11e1da400a3f14a397d8bc5` | 일치 |
| `all-in-one/sources/decoded-original/0629-IdentXmlPart.xml` | `67453a4e499c3e02693e018bfe70a0ba3d7c5ca48b320cc67f6592558ade8972` | `058129bb01e27f7a6a0d0293f332d745e5bab74e` | 일치 |
| `all-in-one/sources/decoded-original/0621-IdentXmlPart.xml` | `a63e2b97ea9eb2691cb478666afed77fc58a2da2f8170422dc09e24b102c88ee` | `844516839e55f8bf231a18630e010b912190664e` | 일치 |
| `all-in-one/sources/decoded-original/0656-IdentXmlPart.xml` | `0dbc45e84732a8848f17b094ea08ab8578dbf240bfe15cd7086859395c27c592` | `9bfb9842e55901bab9a71d1ac03158467dfbb1bc` | 일치 |
| `all-in-one/sources/decoded-original/0692-IdentXmlPart.xml` | `bc84fe2952bd5542eb2308e88836998cd8daa4e1a82f6501830375987aede037` | `737785d03b5fad43c5b4d451955726d800edb1c0` | 일치 |
| `all-in-one/registers/program-model.json` | `6203479c086b15bada12ac9d7e37db9280234ec26f1ea6091d7211dc09a577c5` | `9860b10f008d3a5ae714be50d77b703dfec32f3a` | 일치 |
| `all-in-one/assets/program-model-data.js` | `52f8199371e3399b7c0d44ab5469f0472aced79d56bbef2887f7625f5d2aff0f` | `38f34b0caa380a16ccad6f6f1e234a2fdf23f327` | 일치 |
| `all-in-one/assets/virtual-plc.js` | `5f1876052dc0067b1f010af0dfc941946e37003167481731293615d9c1c36dbc` | `0bd9eceb54365a91214a37c5601b5067c39a3f75` | 일치 |
| `all-in-one/assets/simulator-workspace.js` | `3a6dfc618ff7e7b238f2671dc85d65704f33093a18eac879d86081d92c31e8bc` | `97c2c831c77a9699fff0e0960b3bc1b7d93d45b3` | 일치 |
| `all-in-one/registers/virtual-plc-test-results.json` | `a6b389f797f9a8b5ffe6928b8420f55c4cc459a327b0b48d716079d2eca6dd64` | `757dd50e45184568facb8ff62900b39d3ce848d1` | 일치 |
