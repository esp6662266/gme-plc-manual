# -*- coding: utf-8 -*-
"""Publish the manual work order and source-derived counts; no execution."""
from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parent
def load(name):
    return json.loads((ROOT / name).read_text())
def link(path, text):
    assert (ROOT / path.split('#')[0]).is_file(), path
    return f'<a href="{escape(path, quote=True)}">{escape(text)}</a>'

spec = load('registers/control-spec.json')
repair = load('registers/repair-decision.json')
forms = load('registers/repair-record-forms.json')
alarm = load('registers/alarm-recovery.json')
electrical = load('registers/electrical-trace.json')
hub = load('registers/evidence-review.json')
impact = load('registers/improvement-impact.json')
burner = load('registers/burner-interface.json')
process = load('registers/process-measurement.json')
sensor = load('registers/sensor-measurement.json')
regulation = load('registers/regulation-manual.json')
encoder = load('registers/encoder-position.json')
hmi_transfer = load('registers/hmi-transfer.json')
recipe_settings = load('registers/recipe-settings.json')
body_manual = load('registers/body-manual.json')
identity = load('registers/unresolved-identity.json')
motor = [p['id'] for p in alarm['profiles'] if p['family'] == 'motor']
actuator = [p['id'] for p in alarm['profiles'] if p['family'] != 'motor']
assert len(repair['records']) == forms['counts']['profiles'] == 23
assert alarm['simulator_development'] == 'stopped_by_user'

stages = [
    ('1', '설비·도면·태그 대응', '기본 작업지 연결 / 실물 확인 대기',
     '디코팅 배치도의 우선23개를 먼저 봅니다. 본체·구동 모터·전용 제어기를 구분하고 P&ID, OEM 회로, 추가 시공도면, PLC 백업을 연결합니다.',
     '태그와 주소의 출처·일치 근거·미확정 관계를 남깁니다. 실물 명판이나 현재 배선 없이 동일성을 확정하지 않습니다.',
     link('priority-guides/P01.html', 'BC01 대응 작업지') + ' · ' + link('construction-guide.html', '추가 시공도면')),
    ('2', 'PLC 동작·정지 근거', '우선 설비 상세 보강 중',
     '운전 요청 → 기동 허가 → 최종 출력 → 전기 전달 → 처리 응답 → 감시/정지/리셋을 원본 네트워크에서 추적합니다. 자동·수동과 공통 인터록, 복수 쓰기를 비교합니다.',
     '명령별 원본 조건·반전 접점·시간 선언·읽기/쓰기 위치를 연결합니다. 현재 호출 순서나 실제 값이 필요한 판단은 확인 대기로 남깁니다.',
     link('alarm-recovery.html', '14개 알람·복구 근거') + ' · ' + link('signal-trace.html', '신호 전달·복수 쓰기')),
    ('3', '증상별 수리·복구 매뉴얼', '기존 절차안 / 상세 보강 중',
     '기동 불가, 명령 후 무응답, 운전 중 정지, 리셋 후 재발을 비교합니다. 어느 신호·단자·래더를 어떤 순서로 확인할지 설명합니다.',
     '원인 후보, 배제할 근거, 필요한 자료와 다음 확인을 명시합니다. 알람 래치 해제·원인 해소·새 운전 요청·실제 응답을 따로 확인합니다.',
     link('repair-decision.html', '23개 수리 판단 작업지') + ' · ' + link('repair-guides/P02.html', 'FN04 수리 판단')),
    ('4', '현장 관찰·수리 기록', '입력·저장·백업 구현 / 실제 결과 확인 대기',
     '실물ID·현재 PLC 버전·최초 증상/알람·관찰값/시각·실제 조치·복구 근거를 설비별 기록에 남깁니다. 문서 작성과 함께 필요한 확인 항목을 수집합니다.',
     '실제 관찰과 문서의 원본 참고값을 구분합니다. 기록 저장만으로 수리 완료·설비 동일성·자료 불일치 해소 상태를 바꾸지 않습니다.',
     '<a href="index.html#view=repair-record&amp;equipment=P11&amp;scope=priority">BR01 수리 기록</a> · ' + link('evidence-review.html', '근거 검토·확인')),
    ('5', '프로그램 구조·개선 검토', '6개 후보 작업지 / 적용 전',
     '호출 관계, 공유 조건, 별칭, 복수 쓰기, 의심되는 설정이나 요청 분기의 영향을 분석합니다. 자료 확인 후 변경이 필요한지 판단합니다.',
     '현 구조·영향·대안·검증 조건을 문서로 남깁니다. 현재 PLC/TIA와 제작사 의도를 확인하기 전에는 오류 확정이나 PLC 변경으로 처리하지 않습니다.',
     link('improvement-review.html', '개선 검토 목록')),
    ('6', '통합 검증·배포용 묶음', '각 보완 후 반복',
     '올인원 HTML의 설비 선택·근거 이동·자료 링크를 확인하고, 원본과 보존 파일의 해시를 대조한 뒤 ZIP을 갱신합니다. 우선23개를 먼저 완성합니다. 전체248개는 그다음 필요 항목을 추가하며 현재 상세 확장을 진행하지 않습니다.',
     '문서·링크 확인과 실제 PLC/현장 확인 결과를 구분해 제공하며, 미확인 목록과 사용 안내를 함께 유지합니다.',
     link('ALL-IN-ONE.md', '올인원 사용법') + ' · ' + link('ACTIVE-WORK.md', '현재 작업 범위')),
]
rows = ''.join(f'<tr><td>{n}</td><td><strong>{title}</strong><p class="state">{status}</p></td><td>{work}</td><td>{criterion}</td><td>{links}</td></tr>' for n,title,status,work,criterion,links in stages)
counts = [
    ('미확정 설비 식별',str(identity['counts']['profiles'])+'개 / 원본4네트워크','웨잉호퍼1·배출컨베이어·2사이클론의 자료 후보·배제 근거·추가 확인을 연결합니다. GSS·85톤로는 다른 공정으로 관련 작업을 중단하고 MV04는 철거, SC12는 현장 없음, PV04는 사용 계획 없음으로 사용자 제공 상세 조사 제외합니다. EV01~EV90도 별도 요청 전 매뉴얼 작성에서 제외합니다.'),
    ('본체·공정 경계·증상 조사',str(body_manual['counts']['profiles'])+'개 본체 / '+str(body_manual['counts']['symptom_cases'])+'사례','CC01·AB01·HE01의 원본34네트워크·케이블32행·AB01 알람 발생/리셋을 대조합니다. 본체 직접 출력 배정·현재 설정·현장 복구는 확인 전입니다.'),
    ('전체 관리 항목', str(len(spec['specifications'])), '기본 자료를 보존한 항목 수입니다. 상세 수리 매뉴얼 완성 수가 아닙니다.'),
    ('우선 설비 작업지·기록 양식', str(len(repair['records'])), '역사 목록에는 PLC 대응 미확정5개와 본체 후보3개도 포함합니다. 미확정 중 GSS·85톤로2개는 현재 관련 작업에서 제외합니다. 현장 동일성 확인 전입니다.'),
    ('상세 알람·복구 근거 작업지', str(len(alarm['profiles'])), '모터·팬9개, 게이트·댐퍼5개입니다. 전체23개 설비의 수리 완료를 뜻하지 않습니다.'),
    ('원본 알람 래치', str(sum(len(p['alarms']) for p in alarm['profiles'])), '위14개 작업지에 연결한 백업의 원본 알람입니다. 현재 발생 알람 수가 아닙니다.'),
    ('BR01 외부 연동 상세', str(len(burner['selected_networks']))+'개 네트워크', '명령80곳·SD12곳·주요 신호32개·증상6개를 정적으로 대조했습니다. 전용 연소 제어기 내부·현재 운전은 확인 전입니다.'),
    ('계측·공정 정지 근거', str(len(process['channels']))+'개 입력 / '+str(len(process['outputs']))+'개 출력', '원본20개 네트워크와 공정 알람11개 이름을 대조했습니다. 발생·리셋10개, 쓰기 미확정1개이며 현재 보호값·복구는 확인 전입니다.'),
    ('온도·압력·산소 계측 작업지', str(len(sensor['channels']))+'개 채널', '도면15FG와 원본42네트워크의 핀·참조를 대조합니다. 현재 단위·설정·복구는 확인 전입니다.'),
    ('레시피·설정값·전원 복귀',str(recipe_settings['counts']['recipe_load_fields'])+'적용값 / '+str(recipe_settings['counts']['native_networks'])+'원본 LAD', '편집/저장/불러오기·설정의 다른 쓰기·초기화8증상을 연결합니다. 현재 배열 선언·Retain·화면 이벤트·OB 실행은 확인 전입니다.'),
    ('HMI 태그·설정·표시 확인', str(hmi_transfer['counts']['tags'])+'태그 / '+str(hmi_transfer['counts']['windows'])+'화면 메타데이터', '원본 LAD47과 주소 공유2그룹·범위 교차17쌍을 대조합니다. 현재 DB 멤버·화면 이벤트·통신은 확인 전입니다.'),
    ('엔코더·위치·교정 수리', str(len(encoder['channels']))+'개 밸브', '원본26네트워크·카운터5호출·환산5호출·교정2경로를 대조합니다. 실제 TM 주소·DB 유지·교정 적용은 확인 전입니다.'),
    ('주요 조절 루프 수리·구조', str(len(regulation['loops']))+'개 경로', '원본 LAD33네트워크·조절기5호출과 별도 STL/SCL색인10항목의 출처를 구분합니다. 현재 실행·튜닝은 확인 전입니다.'),
    ('전기 회로 작업지', str(len(electrical['devices'])), '원본 신호·단자·릴레이 경로의 검토 자료입니다. 현재 배선 확인 전입니다.'),
    ('개선 후보 상세 작업지', str(len(impact['items'])), '제안·검토 자료이며 실제 PLC 변경은0건입니다.'),
    ('근거 검토 항목', str(len(hub['items'])), '원본 불일치18·시공7·공통10·개선6·동일성23을 별도로 관리합니다.'),
]
count_rows = ''.join(f'<tr><td>{escape(t)}</td><td>{escape(n)}</td><td>{escape(note)}</td></tr>' for t,n,note in counts)
body = f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>현재 진행 순서와 완료 기준</title><link rel="stylesheet" href="assets/all-in-one.css"><style>main{{max-width:1320px;margin:auto;padding:24px}}td{{vertical-align:top;min-width:100px}}td p{{margin:.5em 0}}.state{{font-size:.9em;color:#475569}}section{{margin:28px 0}}@media print{{main{{padding:0}}.table-wrap{{overflow:visible}}}}</style></head><body><main>
<h1>현재 진행 순서와 완료 기준</h1><p>2026-10-09 기준 · 매뉴얼·수리·PLC 원본 구조 분석·개선 검토를 한곳에서 사용하기 위한 작업 순서입니다.</p>
<div class="notice info">현재는 통합 화면과 우선23개 기본 작업지를 갖춘 뒤, 설비별 상세 근거를 보강하는 단계입니다. 전체 완료율 대신 문서 구현·원본 대조·현장 확인을 구분합니다. 시뮬레이터 작성·수정·확장·행동 시험은 사용자의 별도 작성 요청 전까지 중지합니다.</div>
<section id="current"><h2>현재 상세 보완과 다음 작업</h2><p>모터·팬 {escape(' · '.join(motor))}, 게이트·댐퍼 {escape(' · '.join(actuator))}의 알람·복구 근거 작업지를 연결했습니다. 이는 원본 자료의 정적 대조 결과이며 현재 CPU나 현장 복구를 확인한 결과가 아닙니다.</p>
<p><strong>BR01 버너의 외부 연동·정지·복구 근거를 보강했습니다.</strong> 기동 허가에 연결된 팬/드럼 응답, 운전 요청과 출력의 관계, Lock Out 및 리셋 경로, MV03 세정/기동 요청을 원본에서 대조합니다. 가스·공기 입력4개·출력2개 환산과 공정 정지 알람11개 이름의 근거도 연결했습니다. 온도9·압력6·산소4개 채널의 도면·환산·값 쓰기·HMI 참고를 연결했습니다. 주요 조절 경로9개에서 LAD33네트워크와 STL/SCL색인10항목을 연결했습니다. 엔코더5개 밸브의 카운터·위치 환산·교정2경로·방향 누적 감시를 보강했습니다. HMI782태그·화면17개 메타데이터와 원본 LAD47의 설정/표시 전달 확인 작업지를 연결했습니다. 현재 DB 멤버·화면 이벤트·통신은 확인 전입니다. 레시피 적용값8개·LAD20개·SCL/STL색인7개와 설정의 다른 쓰기/전원 복귀8증상을 연결했습니다. 현재는 우선23개 완성에 집중하며 GSS·85톤로 제외21개를 진행합니다. 전체248개는 참고 목록으로 보존하고 우선 대상 완료 후 필요한 항목을 추가합니다. CC01·AB01·HE01 본체3개/12증상·P&ID 유로·케이블32행과 원본34네트워크를 보강했습니다. MV04는 사용자 제공 철거, SC12는 현장 없음, PV04는 사용 계획 없음으로 상세 조사에서 제외합니다. EV01~EV90도 별도 요청 전 매뉴얼 작성 제외입니다. GSS·85톤로 관련 작업도 중단하며, 다음은 미확정3설비의 식별·제어 주체 자료입니다. 원본16개 네트워크·명령80곳·SD12곳·주요 신호32개와 증상6개의 관찰·비교 순서를 연결했습니다. 전체 버너 제어·현장 복구 완료는 확인 전입니다.</p>
<p>GME PLC의 요청·응답 인터페이스와 버너 전용 제어기의 내부 연소 제어를 구분합니다. 전용010-390 도면과 제작사 자료가 없는 내부 점화·화염 보호 순서 및 보호값은 임의로 채우지 않습니다.</p>
<p>{link('body-manual.html', 'CC01·AB01·HE01 본체·증상별 수리')}</p>
<p>{link('recipe-settings.html', '레시피·설정값·전원 복귀 확인')}</p>
<p>{link('hmi-transfer.html', 'HMI 설정·표시·PLC 전달 확인')}</p>
<p>{link('encoder-position.html', '엔코더·위치·교정 수리')}</p>
<p>{link('regulation-manual.html', '주요 조절 루프 수리·구조')}</p>
<p>{link('sensor-measurement.html', '온도·압력·산소 계측 수리')}</p>
<p>{link('measurement-trace.html', '가스·공기 계측·환산·출력')} · {link('process-stop-alarms.html', '공정 알람·버너 정지 원인')}</p>
<p>{link('burner-interface.html', 'BR01 상세 연동·정지·복구 근거')} · {link('circuit-guides/BR01.html', 'BR01 외부 인터페이스 회로')} · {link('repair-guides/P11.html', 'BR01 기존 수리 판단')} · {link('common-guides/P11.html', '공통 자동 요청 근거')}</p>
<p>이후 나머지 우선23개의 누락 근거를 보완합니다. 본체 후보·미확정 설비는 식별 자료와 전용 제어기 근거를 확보하는 경로로 진행하며, 주변 설비 태그를 대신 배정하지 않습니다. 우선 범위의 상세 기준을 정리한 뒤 전체248개 항목으로 확대합니다.</p></section>
<section id="sequence"><h2>진행 순서</h2><p>아래 순서를 설비별로 반복합니다. 현장 확인 대기는 문서 분석과 병행해 관리하고, 검증은 각 보완 후 수행합니다.</p><div class="table-wrap"><table><thead><tr><th>순서</th><th>단계·상태</th><th>하는 작업</th><th>산출물·판단 기준</th><th>기존 자료</th></tr></thead><tbody>{rows}</tbody></table></div></section>
<section id="status"><h2>현재 산출물과 확인 경계</h2><div class="table-wrap"><table><thead><tr><th>산출물</th><th>수량</th><th>수량의 의미</th></tr></thead><tbody>{count_rows}</tbody></table></div><p>시험577개는 설계·미실행 상태, 현장 확인 대장1,060건은 확인 대기로 유지합니다. 기존 자료 불일치18건도 해소를 확정하지 않았습니다. 현재 PLC 통신·TIA 확인·실물 동일성·현장 수리 결과는 확인 전입니다.</p></section>
<a href="index.html">올인원 통합 현황으로 이동</a></main></body></html>'''
(ROOT / 'work-progress.html').write_text(body, encoding='utf-8')
print('Work order published from existing registers; no field status or simulator files changed.')
