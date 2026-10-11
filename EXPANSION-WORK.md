# GME BC01 기반 확장 — 현재 작업과 인계

표준 **GME-STD-1.0.0** · 프로그램 기준 **v1.3.0** · 2026-10-11

## 최신 사용자 결정

- BC01 수준을 기준으로 우선 설비를 작성한 뒤 나머지 전체 대장으로 확장한다.
- 23개/233개를 그대로 합산하지 않고 **실제 대장 ID 중복 정리·기존 제외 유지**를 적용한다.
- 이 채팅은 작업표준과 전용 스킬까지만 완성한다.
- 완료 후 **GPT-6.1 Sol / Ultra 새 채팅을 만들어 실제 작업을 시작**하도록 인계한다. 이 지시는 기존 “정지” 지시에 이어 새 채팅에서의 시작을 승인한 최신 요청이다.

## 현재 상태

| 작업 | 상태 |
|---|---|
| 작업표준·스킬·원본 기반 대장 작성 | 작성 완료, 검증 결과는 docs/equipment-standard/VERIFICATION.md |
| 프로그램/설비 구현 | 이 표준 작성 작업에서는 변경하지 않음 |
| PREP-01 공통화와 BC01 회귀 | 미착수 — 후속 채팅 첫 작업 |
| FN04(P02) 시범 | 미착수 — PREP-01 이후 |
| 1차 | 우선23행: 기준BC01 포함21행, 다른 공정2제외 |
| 2차 | 우선 대응18·기존 제외90을 뺀140 중 부모 범위 보류7을 제외한133후보 |
| TIA/현재CPU/실물/현장복구 | 이 표준 작성으로 새 검증 없음 |

## 반드시 읽을 파일

1. [작업표준](docs/equipment-standard/WORK-STANDARD.md)
2. [GPT-6.1 Sol 실행 안내와 재개 문장](docs/equipment-standard/START-GPT61.md)
3. [23행·248 ID 전체 대장](docs/equipment-standard/INVENTORY.json)
4. [설비 작업 기록 양식](docs/equipment-standard/WORK-ITEM-TEMPLATE.md)
5. [전용 스킬](.agents/skills/gme-equipment-rollout/SKILL.md)
6. [원본 구현과 생성기 경계](.agents/skills/gme-equipment-rollout/references/source-map.md)

## 다음 한 작업: PREP-01

실제 Git 상태와 BC01 기준을 보존하고 BC01/P01 고정 데이터·화면·도구·검사를 설비별로 확장할 최소 변경을 설계한다. build-control-spec.py의 build-program-model.py 자동 호출을 먼저 정적으로 확인하고 금지 경로를 분리하기 전 실행하지 않는다. 기존 시뮬레이터/중지5자산은 변경·실행하지 않는다. 공통화 후 BC01 회귀를 통과시키고 FN04 시범으로 넘어간다.

새 채팅은 docs/equipment-standard/work-items/PREP-01.md부터 실제 진행 기록을 작성한다. 원본 폴더 all-in-one/의 v1.3.0 ACTIVE-WORK.md는 당시 구현 이력이며 이 확장 계획과 구분한다. 프로그램을 수정해 검증한 후에만 해당 ACTIVE-WORK/버전/게시 상태를 갱신한다.

## 보존과 인계 원칙

원본/완료분/미확정/브라우저 기록·초안·미지 필드는 보존한다. 실제 PLC/현장/보호값·SEJIN 변경은 하지 않는다. GitHub main이 최신 작업이며 다른 컴퓨터도 같은 표준·스킬·대장을 받는다. 개인 관찰 기록은 별도 JSON 이동이며 코드 저장소에 자동 업로드하지 않는다.

새 채팅 생성/시작 여부는 원래 채팅의 도구 결과로 확인한다. 새 작업이 시작되면 새 채팅만 이 저장소의 진행 상태를 쓴다.
