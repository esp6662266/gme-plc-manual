# GPT-6.1 Sol / Ultra 실행·재개 안내

표준 GME-STD-1.0.1 · 확인일 2026-10-12.

## 모델과 스킬

Codex의 모델 설정에서 **GPT-6.1 Sol**, 추론 수준 **Ultra**를 선택한다. 모델 ID는 gpt-6.1-sol이다. Ultra가 표시되지 않으면 Settings → Configuration의 Ultra 표시 설정과 해당 계정/클라이언트 지원을 확인한다. 스킬이나 프롬프트에 모델명을 쓰는 것만으로 현재 모델이 바뀌지는 않는다. 실제 선택 결과가 보이지 않으면 실행 기록에는 미확인이라고 쓴다. [공식 모델 안내](https://learn.chatgpt.com/docs/models)

저장소의 .agents/skills/gme-equipment-rollout/가 공유 스킬 원본이다. Codex에서 이 Git 저장소 폴더 또는 그 하위 폴더를 열면 저장소 스킬 탐색 범위에 들어간다. 부모의 “무제 폴더”만 연 채로 하위 스킬 자동 발견을 가정하지 않는다. 새 채팅의 시작 프롬프트에도 정확한 SKILL.md 경로를 전달한다. [공식 스킬 위치 안내](https://learn.chatgpt.com/docs/build-skills)

별도 사용자 전역 스킬을 복제하지 않아 컴퓨터마다 다른 판본이 남는 것을 피한다. 목록에 보이지 않으면 저장소를 다시 열고 SKILL.md 경로를 명시하여 읽도록 한다. 이 표준 작성에서는 파일 생성/검증을 확인하며 UI 선택 목록 표시 여부는 별도다.

## 새 컴퓨터

Git, Node.js24, Python3.10+를 준비한다. 프로그램을 바꾸기 전에 원본 줄바꿈을 보존한다.

    git -c core.autocrlf=false clone https://github.com/esp6662266/gme-plc-manual.git
    cd gme-plc-manual
    git config core.autocrlf false
    git status --short
    git log -1 --oneline

기존 clone은 dirty 확인/보존 후 fetch → main → pull --ff-only로 받는다. 강제 reset은 하지 않는다. 고정 v1.3.0 태그 대신 최신 main에서 작업한다.

먼저 EXPANSION-WORK.md, 이 표준과 최신 설비 기록을 읽는다. Python 실행 파일명은 환경에 맞게 선택한다.

    python3 .agents/skills/gme-equipment-rollout/scripts/preflight.py

Windows:

    py -3 .agents/skills/gme-equipment-rollout/scripts/preflight.py

이 명령은 대장 일치만 검사하며 설비 작성 완료를 검사하지 않는다. --emit-json은 대장 JSON을 표준 출력으로 만들 뿐 파일은 쓰지 않는다. 대상 정책 변경 또는 정상적인 후속 작성으로 원본 대장의 이름·작성 수준·집계 등이 바뀌면 변경 근거와 출력 diff를 검토하고 INVENTORY.json을 갱신한다. 제외/대응 관계의 변경은 사용자 범위와 원본 근거가 필요하다. 단순 검사 통과를 위해 차이를 덮어쓰지 않는다. 원본 바이트만 달라진 경우 source_byte_changes를 검토해 설명을 남긴다.

프로그램 구현 시 필요한 설치/검증은 WORKSPACE-HANDOFF.md와 작업표준에 따른다. 프로그램 원본은 all-in-one/이며 현재PC 옛 폴더나 옛 ZIP을 사용하지 않는다.

## 처음 시작할 문장

다음을 GPT-6.1 Sol / Ultra로 설정한 채팅에 전달한다.

> $gme-equipment-rollout 이 저장소의 .agents/skills/gme-equipment-rollout/SKILL.md, AGENTS.md, EXPANSION-WORK.md와 docs/equipment-standard/WORK-STANDARD.md·INVENTORY.json·WORK-ITEM-TEMPLATE.md를 읽고 현재 Git 상태부터 확인해. 사용자가 승인한 실제 대장 중복 정리·기존 제외 유지 기준으로 BC01 기반 확장을 시작해. 먼저 PREP-01 공통화·금지 생성기 호출 분리·BC01 회귀를 완료하고, FN04(P02) 한 설비를 시범으로 작성·검증해. 그 뒤 표준의 1차 순서와 현재2차125개 대상(RO01~04미사용 및 CC01/TC11/CM01/CM02/UC01철거 제외·이력보존)를 설비 한 개씩 진행해. 원본·기존 완료 자료·브라우저 기록을 보존하고 최대2개 읽기 전용 조사자와 병행하되 부모만 공통 파일을 편집해. 시뮬레이터와 실제 PLC/현장/보호값 및 SEJIN 변경은 하지 마. 미확정 자료는 남기고 문서·화면·TIA/CPU·현장 상태를 나눠 기록해. 매 작업의 검증·버전·GitHub 인계 상태와 다음 작업을 저장해.

## 중단 후 이어갈 문장

> $gme-equipment-rollout 최신 main과 EXPANSION-WORK.md, 마지막 work-items 기록을 확인하고 이미 끝난 작업은 보존해. 아직 미완료인 다음 한 작업부터 같은 표준과 제외 범위로 이어서 진행해. 새 근거 없이 보류된 실물/현장 항목을 임의 완료하지 말고 진행 가능한 다음 설비를 처리해.

## 새 채팅 자동 인계

사용자가 새 채팅 생성과 시작을 명시하면 Codex create_thread에 모델 gpt-6.1-sol, 추론 ultra, 이 저장소 경로와 시작 문장을 전달한다. 기존 채팅의 모델을 바꿨다고 표시하지 않는다. 생성된 실제 threadId와 시작 상태를 확인하고, 기존 채팅에서는 같은 파일의 병행 수정을 멈춘다.

새 채팅의 검증 결과는 실제 수행 후 기록한다. 채팅 생성 자체를 PREP-01·FN04 또는 전체 확장 완료로 표시하지 않는다.
