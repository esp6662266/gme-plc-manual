/* One workspace; existing source documents stay preserved as separate resources. */
(() => {
  'use strict';
  const data = window.GME_APP_DATA;
  if (!data) return;
  const $ = id => document.getElementById(id);
  const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const deviceMap = new Map(data.equipment.map(d => [d.id, d]));
  const priorityMap = new Map(data.priority.map(p => [p.key, p]));
  const resourceSet = new Set(data.resources);
  const drawingKinds=[['OEM 전기','전기·제어 도면'],['P&ID','P&ID·공정'],['시공·케이블','시공·케이블'],['HMI 참고','HMI 참고']];
  const drawingLastByKind=new Map();
  let photoViewer=null;
  const drawingMap = new Map((data.drawing_workspace?.profiles || []).map(p=>[p.key,p]));
  const reviewItems = data.evidence_review?.items || [];
  const reviewMap = new Map(reviewItems.map(r => [r.id,r]));
  const reviewKinds = {source:'원본 불일치',construction:'시공 검토',common:'공통 확인',improvement:'개선 후보',identity:'설비 동일성'};
  const noteStore = window.GMENoteStore;
  const repairRecords = window.GMERepairRecords;
  const repairRecordMap = new Map((data.repair_record_forms?.profiles || []).map(p=>[p.key,p]));
  const repairWorkspaceKeys = new Set(['P01','P02']);
  const bc01Sections=[['overview','설비·자료 기준'],['io','I/O·HMI'],['control','제어 구조'],['circuits','전기 전달 경로'],['alarms','알람·복구'],['repair','증상별 수리'],['completion','완료 기준']];
  const bc01LastItems=new Map();
  const validNoteEquipment = new Set([...deviceMap.keys(),...priorityMap.keys()]);
  const base = new URL('./', location.href);
  const views = new Set(['overview','priority','summary','manual','repair','repair-record','io','spec','ladder','structure','drawings','simulator','tests','checks','conflicts','notes','resources','doc','review']);
  const deviceViews = new Set(['summary','manual','repair','repair-record','io','spec','ladder','structure','drawings','simulator','tests','checks','review']);
  const tabs = [['summary','설비 요약'],['manual','매뉴얼'],['repair','진단·수리'],['io','I/O·HMI'],['spec','제어 명세'],['ladder','래더'],['drawings','도면'],['simulator','시뮬레이터 · 영구 중지'],['tests','시험'],['checks','확인 대장']];
  tabs.splice(6,0,['structure','호출·신호 구조']);
  tabs.splice(3,0,['repair-record','수리 기록']);
  const labels = Object.fromEntries(tabs.concat([['overview','통합 현황'],['priority','공정 배치도·설비카드'],['notes','개선·작업 메모'],['resources','전체 자료'],['doc','자료 보기'],['conflicts','자료 불일치'],['review','근거 검토·확인']]));
  const state = {view:'overview', selected:'P01', scope:'priority', doc:'', listQuery:'', group:'', tableQuery:'', tableDevice:'', reviewKind:'', layoutMode:'map', layoutZoom:0.85, layoutQuery:'', layoutScroll:[0,0], renderId:0, drawing:'', drawingZoom:1, drawingWide:false, repairSymptom:'', bc01Section:'overview', bc01Item:'', bc01AlarmStep:'set', bc01Text:'standard', bc01Check:'',bc01MediaGroup:'belt',bc01Photo:'photo-01',bc01Find:'',bc01Relation:'request'};
  const manualStateKeys=['bc01Section','bc01Item','bc01AlarmStep','bc01Text','bc01Check','bc01MediaGroup','bc01Photo','bc01Find','bc01Relation','standardWide'];
  const manualDefaults=Object.fromEntries(manualStateKeys.map(k=>[k,state[k]]));
  const manualStates=new Map();
  let lastRenderedRoute = null;
  let bc01Wide = false;
  const NOTES_KEY = 'gme-all-in-one-notes-v1';
  const DRAFT_KEY = 'gme-all-in-one-drafts-v1';
  const legacyAnchors = new Set(['purpose','equipment','scope','method','read','workflow','program','conflicts','drawing']);
  let notes = [];
  let drafts = {};
  let storageError = '';
  let savingNote = false;
  try {
    notes = noteStore.decodeNotes(localStorage.getItem(NOTES_KEY),validNoteEquipment);
    drafts = noteStore.decodeDrafts(localStorage.getItem(DRAFT_KEY));
  } catch (_) { storageError = '저장된 메모를 읽지 못했습니다. 다운로드한 메모 백업을 확인해 주세요.'; }

  function selection(key = state.selected) {
    const p = priorityMap.get(key);
    const d = deviceMap.get(p ? p.plc_id : key);
    return {p, d, name:p ? p.name : (d?.name || '미선택'), id:d?.id || '', key};
  }
  function equipmentStatus(id) { return data.equipment_status_notes?.find(n => n.id === id); }
  function matchText(p) {
    return p.match === 'tag' ? '태그명 일치 · 실물 확인 필요' : p.match === 'candidate' ? 'PLC 대응 후보' : 'PLC 대응 미확정';
  }
  function button(text, view, key = state.selected, extra = '') {
    return `<button type="button" data-view="${esc(view)}" data-equipment="${esc(key)}" ${extra}>${esc(text)}</button>`;
  }
  function docButton(text, path) { return `<button type="button" data-doc="${esc(path)}">${esc(text)}</button>`; }
  function table(headers, rows) {
    return `<div class="table-wrap"><table><thead><tr>${headers.map(h => `<th scope="col">${esc(h)}</th>`).join('')}</tr></thead><tbody>${rows.length ? rows.map(row => `<tr>${row.map(v => `<td>${v}</td>`).join('')}</tr>`).join('') : `<tr><td colspan="${headers.length}">해당 자료가 없습니다.</td></tr>`}</tbody></table></div>`;
  }
  function panel(title, body) { return `<section class="panel"><h2>${esc(title)}</h2>${body}</section>`; }
  function pdfPage(fg) {
    if (String(fg) === '5A') return 6;
    if (String(fg) === '180A') return 182;
    if (String(fg) === '180B') return 183;
    const n = Number(fg); return n + (n > 5 ? 1 : 0) + (n > 180 ? 2 : 0);
  }
  function validDoc(path) {
    if (typeof path !== 'string' || path.length > 2000) return false;
    const relative = path.split('#')[0];
    return relative !== 'index.html' && resourceSet.has(relative);
  }
  function route(view, selected = state.selected, doc = '', review = '') {
    if (!views.has(view)) view = 'overview';
    if (!deviceMap.has(selected) && !priorityMap.has(selected)) selected = 'P01';
    const nextScope = selected === state.selected ? state.scope : (priorityMap.has(selected) ? 'priority' : 'all');
    const manual=selected===state.selected?state:{...manualDefaults,...manualStates.get(selected)};
    const params = new URLSearchParams({view, equipment:selected, scope:nextScope});
    if (doc && validDoc(doc)) params.set('doc', doc);
    if(selected===state.selected && repairWorkspaceKeys.has(selected) && repairRecordMap.get(selected)?.steps.some(s=>s.id===state.repairSymptom)) params.set('symptom',state.repairSymptom);
    if(view==='manual' && selected==='P01') {if(manual.bc01Find)params.set('find',manual.bc01Find.slice(0,160));if(manual.bc01Section==='control' && manual.bc01Item==='request')params.set('relation',manual.bc01Relation);params.set('section',manual.bc01Section);if(manual.bc01Item)params.set('item',manual.bc01Item);if(manual.bc01Section==='alarms')params.set('alarmStep',manual.bc01AlarmStep);if(manual.bc01Section==='overview' && manual.bc01Item==='media'){params.set('media',manual.bc01MediaGroup);params.set('photo',manual.bc01Photo);}if(manual.bc01Text==='large')params.set('text','large');if(manual.bc01Section==='completion' && bc01CompletionTasks(manual.bc01Item).some(t=>t.id===manual.bc01Check))params.set('check',manual.bc01Check);}
    if(view==='manual' && selected!=='P01' && window.GMEEquipmentStandard.profile(data,selected)){params.set('section',manual.bc01Section);if(manual.bc01Item)params.set('item',manual.bc01Item);if(manual.bc01Text==='large')params.set('text','large');if(manual.bc01Find)params.set('find',manual.bc01Find);}
    if(view==='drawings' && selected===state.selected && drawingMap.get(selected)?.sheets.some(s=>s.id===state.drawing)) params.set('drawing',state.drawing);
    if (view === 'review' && reviewMap.has(review)) params.set('review',review);
    const hash = '#' + params.toString();
    if (location.hash !== hash) { lastRenderedRoute = null; location.hash = hash; }
    readRoute();
  }
  function readRoute() {
    const raw = location.hash.slice(1);
    if (raw === lastRenderedRoute) return;
    lastRenderedRoute = raw;
    if (legacyAnchors.has(raw)) { route('doc', state.selected, 'manual-catalog.html#' + raw); return; }
    const params = new URLSearchParams(raw);
    const nextView = views.has(params.get('view')) ? params.get('view') : 'priority';
    if (nextView !== state.view || params.get('equipment') !== state.selected) {
      state.tableQuery = ''; state.tableDevice = '';
    }
    if(nextView!==state.view || params.get('equipment')!==state.selected) state.drawingZoom=1;
    if(state.view==='manual')manualStates.set(state.selected,Object.fromEntries(manualStateKeys.map(k=>[k,state[k]])));
    const oldSelected=state.selected;
    state.view = nextView;
    const key = params.get('equipment');
    state.selected = deviceMap.has(key) || priorityMap.has(key) ? key : 'P01';
    if(state.selected!==oldSelected)Object.assign(state,manualDefaults,manualStates.get(state.selected));
    const repairSchema=repairWorkspaceKeys.has(state.selected)?repairRecordMap.get(state.selected):null;
    state.repairSymptom=repairSchema?.steps.find(s=>s.id===params.get('symptom'))?.id || (state.view==='repair' && repairSchema?repairSchema.steps[0]?.id:'') || '';
    if(state.view==='manual' && state.selected==='P01') {
      state.bc01Section=bc01Sections.some(s=>s[0]===params.get('section'))?params.get('section'):'overview';
      const items=bc01Items(state.bc01Section);
      state.bc01Item=items.find(x=>x.id===params.get('item'))?.id || items[0]?.id || '';
      state.bc01AlarmStep=['set','reset','restart'].includes(params.get('alarmStep'))?params.get('alarmStep'):'set';
      state.bc01Text=params.get('text')==='large'?'large':'standard';state.bc01Find=(params.get('find') || '').trim().slice(0,160);state.bc01Relation=data.bc01_standard.relationships.nodes.find(n=>n.id===params.get('relation'))?.id || 'request';
      const checks=state.bc01Section==='completion'?bc01CompletionTasks(state.bc01Item):[];
      state.bc01Check=checks.find(t=>t.id===params.get('check'))?.id || checks[0]?.id || '';
      if(state.bc01Section==='overview' && state.bc01Item==='media')bc01NormalizeMedia(params.get('media'),params.get('photo'));
      bc01LastItems.set(state.bc01Section,state.bc01Item);
    }
    if(state.view==='manual' && state.selected!=='P01' && window.GMEEquipmentStandard.profile(data,state.selected))Object.assign(state,window.GMEEquipmentStandard.normalize(data,state.selected,params));
    state.doc = validDoc(params.get('doc')) ? params.get('doc') : '';
    state.drawing = params.get('drawing') || '';
    if (state.view === 'review' && reviewMap.has(params.get('review'))) {
      state.tableQuery = params.get('review'); state.tableDevice = ''; state.reviewKind = '';
    }
    const requestedScope = params.get('scope');
    state.scope = ['priority','all'].includes(requestedScope) ? requestedScope : (priorityMap.has(state.selected) ? 'priority' : 'all');
    syncScope();
    renderList();
    render();
    if(photoViewer) {
      if(state.view!=='drawings' || state.selected!==photoViewer.profile.key)closePhotoViewer();
      else {const sheet=photoViewer.profile.sheets.find(s=>s.id===state.drawing);if(sheet && sheet.id!==photoViewer.sheet.id)showPhoto(sheet);}
    }
  }
  function syncScope() {
    document.querySelectorAll('[data-scope]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.scope === state.scope)));
    const groups = state.scope === 'priority' ? [...new Set(data.priority.map(p => p.phase))] : [...new Set(data.equipment.map(d => d.group))];
    if (!groups.includes(state.group)) state.group = '';
    $('equipment-group').innerHTML = '<option value="">전체 영역</option>' + groups.map(g => `<option value="${esc(g)}">${esc(g)}</option>`).join('');
    $('equipment-group').value = state.group;
  }
  function renderList() {
    const source = state.scope === 'priority' ? data.priority : data.equipment;
    const q = state.listQuery.toLocaleLowerCase();
    const shown = source.filter(item => {
      const search = state.scope === 'priority' ? `${item.name} ${item.plc_id} ${item.note} ${deviceMap.get(item.plc_id)?.search || ''}` : item.search;
      return (!q || search.toLocaleLowerCase().includes(q)) && (!state.group || (item.phase || item.group) === state.group);
    });
    $('equipment-count').textContent = `${shown.length} / ${source.length}`;
    $('equipment-list').innerHTML = shown.map(item => {
      const key = item.key || item.id;
      const name = item.key ? item.name : `${item.id} · ${item.name}`;
      const sub = equipmentStatus(key)?.label || (item.key ? (item.plc_id ? `${item.plc_id} · ${item.match === 'candidate' ? '대응 후보' : '동일성 검토 중'}` : 'PLC 대응 확인 필요') : item.group);
      return `<button type="button" class="equipment-item ${state.selected === key ? 'active' : ''}" data-select="${esc(key)}" aria-pressed="${state.selected === key}">${esc(name)}<small>${esc(sub)}</small></button>`;
    }).join('') || '<p class="muted">검색 결과가 없습니다.</p>';
  }
  function renderContext() {
    const {p, d, name} = selection();
    $('context-kicker').textContent = p ? `디코팅 시안 · 우선 설비 ${p.key}` : `${d?.group || '전체 자료'} · ${d?.id || ''}`;
    $('context-title').textContent = name;
    $('context-meta').textContent = p ? `${matchText(p)}${p.plc_id ? ' · 참고 PLC 자료 ' + p.plc_id : ''}${p.note ? ' · ' + p.note : ''}` : (equipmentStatus(d?.id) ? equipmentStatus(d.id).label + ' · 상세 조사 제외 · 과거 자료 보존' : d?.evidence_status || '');
    if (equipmentStatus(p?.key || d?.id)) $('context-meta').textContent = equipmentStatus(p?.key || d?.id).label + ' · '+(equipmentStatus(p?.key || d?.id).label.includes('사용자 제공')?'':'사용자 제공 · ')+'과거 자료 보존';
    $('device-tabs').innerHTML = tabs.map(([v,label]) => button(label,v,state.selected,`class="${state.view === v ? 'active' : ''}" aria-current="${state.view === v ? 'page' : 'false'}"`)).join('');
    document.querySelectorAll('.primary-nav button').forEach(b => b.classList.toggle('active', b.dataset.view === state.view || (b.dataset.view === 'tests' && ['checks','conflicts'].includes(state.view))));
    document.title = `${labels[state.view]} · ${name} | GME 올인원`;
  }
  function unknownPanel() {
    const {p} = selection();
    if (equipmentStatus(p?.key)) return panel('현재 작업 대상에서 제외', '<p>'+esc(equipmentStatus(p.key).label)+' · 사용자 제공(2026-10-09)</p><p>관련 조사·분석·매뉴얼 보강은 중단합니다. 기존 배치도와 과거 자료만 보존하며 현재 대상에 PLC 태그를 새로 연결하지 않습니다.</p>');
    return panel('설비 대응을 먼저 확인합니다', `<p>${esc(p?.note || '현재 원본 자료에서 직접 대응을 확인하지 못했습니다.')}</p><div class="notice">이 설비는 우선 23개 범위에 포함되어 있습니다. SEJIN 설비 카드, 명판, 제어반과 도면을 대조한 뒤 PLC 태그를 연결합니다.</div><div class="inline-actions">${button('대응표 보기','priority')}${button('확인 메모 작성','notes')}${button('전체 PLC 자료 찾기','resources')}</div>`);
  }
  function renderOverview() {
    return `<section class="hero"><div><span class="eyebrow">GME / DECOATING WORKSPACE</span><h2>설비를 선택하고, 근거를 따라 확인합니다.</h2><p>매뉴얼부터 수리 진단, PLC 로직과 시험 자료까지 한곳에서 사용합니다. 우선23개를 먼저 완성합니다. 다른 공정2개를 제외한 현재21개에 집중하고, 전체248개 대장을 보존하며, 우선 대상 뒤에 중복·기존 제외·부모 보류를 뺀133후보를 순서대로 작성합니다.</p></div><div class="hero-actions">${button('우선 23개 보기','priority')}${button('BC01 시작','summary','P01')}</div></section>
      <div class="stats">${[['23','우선 설비'],['248','전체 관리 항목'],['426','원본 LAD 네트워크'],['577','시험 설계 · 실행 0'],['18','자료 불일치 · 해소 미확정']].map(([n,t]) => `<div class="stat"><strong>${n}</strong><span>${t}</span></div>`).join('')}</div>
      <div class="columns">${panel('지금 사용할 수 있는 기능', '<div class="status-row"><span>설비별 매뉴얼·수리 절차안</span><span class="badge good">자료 연결</span></div><div class="status-row"><span>I/O·HMI·제어 명세</span><span class="badge good">탐색 가능</span></div><div class="status-row"><span>전기도면·P&ID·원본 래더</span><span class="badge good">탐색 가능</span></div><div class="status-row"><span>시험·확인 대장·작업 메모</span><span class="badge good">통합 화면</span></div>')}
      ${panel('검증을 이어갈 항목', '<div class="status-row"><span>현재 대상21개 설비의 실제 PLC 대응</span><span class="badge pending">동일성 확인</span></div><div class="status-row"><span>상세 수리 절차·호출 구조</span><span class="badge pending">구조 추적 지원</span></div><div class="status-row"><span>시뮬레이터</span><span class="badge pending">개발·행동 시험 중지</span></div><div class="status-row"><span>TIA 실행·현장 프로그램 일치</span><span class="badge pending">미검증</span></div>')}</div>
      ${panel('현재 작업 순서', `<div class="steps">${[['01','설비·도면·태그 대응','우선23개 · 본체·구동부·제어기 구분'],['02','PLC 동작·정지 근거','요청·허가·출력·응답·알람·리셋 추적'],['03','증상별 수리·복구 절차','확인 위치·원인 후보·배제 근거'],['04','현장 관찰·수리 기록','자료 차이·실제 조치·복구 근거 수집'],['05','구조·개선 검토','호출·복수 쓰기·영향·대안 확인'],['06','통합 검증·전체 확대','근거 링크·원본 보존·ZIP 갱신']].map(([n,t,p]) => `<div class="step"><span>STEP ${n}</span><b>${t}</b><p>${p}</p></div>`).join('')}</div><p class="muted">우선 23개 수리 기록에 점검 단계별 근거를 연결했습니다. 개선 후보6건의 영향 작업지와 모터·팬9개와 게이트·댐퍼5개의 알람 발생·리셋·재기동 근거를 연결했습니다. BR01 버너의 외부 연동·정지·복구와 MV03 요청 근거를 보강했습니다. 가스·공기 입력4개/출력2개 환산과 공정 정지 알람11개 이름의 원본 근거도 연결했습니다. 온도9·압력6·산소4개 채널의 도면·환산·복수 쓰기·HMI 참고를 보강했습니다. 주요 조절 경로9개에서 LAD33네트워크와 STL/SCL색인10항목을 구분해 수리 근거를 보강했습니다. 엔코더5개 밸브의 카운터·위치 환산·교정2경로·방향 누적 감시를 보강했습니다. HMI782태그·화면17개 메타데이터와 원본 LAD47의 설정/표시 전달 확인 작업지를 연결했습니다. 현재 DB 멤버·화면 이벤트·통신은 확인 전입니다. 레시피 적용값8개·LAD20개·SCL/STL색인7개와 전원 복귀 초기화·설정의 다른 쓰기8증상을 연결했습니다. CC01·AB01·HE01 본체3개·증상12개와 P&ID 유로·시공 케이블32행·알람 경계를 추가했습니다. MV04는 철거, SC12는 현장 없음, PV04는 사용 계획 없음으로 사용자 제공 상세 조사 제외합니다. EV01~EV90도 별도 요청 전 매뉴얼 작성에서 제외합니다. 과거 원본은 보존합니다. GSS·85톤로는 다른 공정으로 관련 작업을 중단합니다. 미확정3설비(웨잉호퍼1·배출컨베이어·2사이클론)의 식별 자료를 보강합니다. 문서 구현·원본 대조·현장 확인을 구분합니다. 별도 작성 요청 전까지 시뮬레이터 개발·수정·시험은 중지하며 매뉴얼·수리·구조 분석을 진행합니다.</p><div class="quick-links">${button('FN04 상세 자료','repair','P02')}${docButton('구조 개선 검토 '+(data.review_counts?.improvement_candidates || 0)+'건','improvement-review.html')}${docButton('모터·밸브 알람·복구 '+(data.review_counts?.alarm_guides || 0)+'개','alarm-recovery.html')}${docButton('전기 회로 추적','electrical-trace.html')}${button('18개 불일치 확인','conflicts')}${docButton('레시피·설정값·전원 복귀','recipe-settings.html')}${docButton('HMI 설정·표시 전달 확인','hmi-transfer.html')}${docButton('엔코더·위치·교정 수리','encoder-position.html')}${docButton('주요 조절 루프 수리·구조','regulation-manual.html')}${docButton('온도·압력·산소 계측','sensor-measurement.html')}${docButton('가스·공기 환산·출력','measurement-trace.html')}${docButton('공정 알람·버너 정지','process-stop-alarms.html')}${docButton('BR01 외부 연동·정지·복구','burner-interface.html')}${docButton('미확정3설비 식별·자료 후보','unresolved-identity.html')}${docButton('CC01·AB01·HE01 본체·수리','body-manual.html')}${docButton('작성 상태·누락·다음 작업','requirements-audit.html')}${docButton('사용 안내','operator-guide.html')}${docButton('진행 순서·완료 기준','work-progress.html')}${docButton('현재 작업 범위','ACTIVE-WORK.md')}${docButton('기존 전체 매뉴얼','manual-catalog.html')}</div>`)}
      ${panel('보존한 시뮬레이터 · 개발 중지',`<p>원본 LAD 426개 중 ${data.program_counts?.executable || 0}개가 독립 네트워크 시험을 지원합니다. BC01·FN04는 가상 장치 응답과 고장 주입을 연결했습니다.</p><p>개발 중지 전 기록: 부분 행동 시험 ${data.virtual_results?.passed || 0}개 통과. 기존 모델과 결과를 보존하며 새 개발·행동 시험을 진행하지 않습니다.</p><div class="inline-actions">${button('기존 시험 기록','tests')}${button('프로그램 호출 구조','structure')}</div>`)}
      <div class="notice info">가상 메모리의 값은 시뮬레이터에서 확인합니다. 자료의 HMI 이미지와 SEJIN 상태는 현재 PLC 운전값이 아닙니다.</div>`;
  }
  // The reference layout is navigation, never a live HMI or PLC model.
  function layoutIcon(p) {
    const id=p.plc_id || '';
    const paths=id.startsWith('FN') ? '<circle cx="24" cy="24" r="18"/><circle cx="24" cy="24" r="4"/><path d="M24 20c-16-17-22 4-5 5M28 24c17-16-4-22-5-5M24 28c16 17 22-4 5-5M20 24c-17 16 4 22 5 5"/>'
      : id.startsWith('MV') || id.startsWith('PV') ? '<path d="M6 14l18 10L6 34V14zm36 0L24 24l18 10V14zM24 24V6m-8 0h16"/>'
      : id==='RD01' ? '<rect x="4" y="14" width="40" height="20" rx="9"/><path d="M14 15v18m20-18v18M10 38h28"/>'
      : id==='BC01' || p.key==='P04' ? '<rect x="4" y="18" width="40" height="13" rx="6"/><circle cx="12" cy="24" r="3"/><circle cx="36" cy="24" r="3"/><path d="M8 36h32m-25-4v4m18-4v4"/>'
      : id==='BR01' || id==='AB01' ? '<path d="M24 4c3 12 14 14 14 26a14 14 0 01-28 0c0-8 6-11 8-18 0 9 4 8 6-8z"/>'
      : id==='HE01' ? '<rect x="7" y="7" width="34" height="34" rx="4"/><path d="M16 11v26m8-26v26m8-26v26M2 17h5m34 14h5"/>'
      : p.key==='P03' || p.key==='P14' ? '<path d="M9 5h30v16L27 36h-6L9 21V5zM21 36v7h6v-7M9 14h30"/>'
      : '<rect x="7" y="9" width="34" height="30" rx="5"/><path d="M14 17h20m-20 8h20m-20 8h12"/>';
    return `<svg viewBox="0 0 48 48" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">${paths}</svg>`;
  }
  function layoutBadge(p) {
    if (equipmentStatus(p.key)) return '현재 작업 제외';
    return p.match==='unknown' ? '식별 자료 필요' : p.match==='candidate' ? 'PLC 대응 후보' : '태그 참고 · 실물 확인 전';
  }
  function renderEquipmentCard() {
    const {p,d,name}=selection();
    if(!p) return panel('우선 설비를 선택하세요','<p>배치도에서 현재 대상 설비를 선택하면 자료가 함께 연결됩니다.</p>');
    const excluded=equipmentStatus(p.key) || equipmentStatus(d?.id);
    const alarmDoc=d ? (resourceSet.has('alarm-guides/'+d.id+'.html') ? 'alarm-guides/'+d.id+'.html' : d.id==='BR01' ? 'burner-interface.html' : ['CC01','AB01','HE01'].includes(d.id) ? 'body-manual.html#body-'+d.id : 'control-specs/'+d.id+'.html#fault') : '';
    const description=excluded ? '다른 공정으로 현재 상세 작업에서 제외합니다. 기존 자료는 보존합니다.' : d?.role || p.note;
    return `<aside class="equipment-detail-card" aria-labelledby="layout-card-title">
      <div class="card-topline"><span>선택 설비 · ${esc(p.key)}</span><span class="badge ${p.match==='unknown'?'pending':''}">${esc(layoutBadge(p))}</span></div>
      <div class="card-identity"><span class="equipment-symbol">${layoutIcon(p)}</span><div><span class="eyebrow">${esc(p.phase)}</span><h2 id="layout-card-title" tabindex="-1">${esc(name)}</h2><span class="card-plc">${esc(d?.id ? '참고 PLC · '+d.id : 'PLC 태그 미확정')}</span></div></div>
      <p class="card-description">${esc(description)}</p>
      ${excluded ? '<div class="card-boundary">사용자 제공 제외 상태입니다. 상세 조사·새 매뉴얼 보강을 진행하지 않습니다.</div>'+button('제외 안내 보기','summary',p.key) : `<div class="card-boundary">${esc(matchText(p))}. 현재 운전값·알람 상태는 연결되어 있지 않습니다.</div>
      <div class="card-metrics">${[[d?.inputs.length ?? '—','입력 참조'],[d?.outputs.length ?? '—','출력 참조'],[d?.networks.length ?? '—','원본 LAD'],[d?.hmi.length ?? '—','HMI 태그']].map(([n,label])=>`<div><strong>${n}</strong><span>${label}</span></div>`).join('')}</div>
      <div class="card-drawing-entry">${button('설비별 도면 작업실','drawings',p.key,'class="card-primary-action"')}</div><h3>점검·수리 시작</h3><div class="card-main-actions">${button(d?'증상별 수리':'식별·점검 작업지','repair',p.key,'class="card-primary-action"')}${d?docButton('알람·리셋',alarmDoc):docButton('필요한 식별 자료','unresolved-identity.html#identity-'+p.key)}</div>
      <h3>이 설비의 자료</h3><div class="card-document-actions">${button('매뉴얼','manual',p.key)}${d?button('I/O·HMI','io',p.key)+button('제어 명세','spec',p.key)+button('원본 래더','ladder',p.key):''}${button('도면·HMI 참고','drawings',p.key)}${button('수리 관찰 기록','repair-record',p.key)}</div>
      ${['CC01','AB01','HE01'].includes(d?.id)?'<div class="card-body-link">'+docButton('본체·계측·증상별 근거','body-manual.html#body-'+d.id)+'</div>':''}
      <details class="card-evidence-detail"><summary>근거와 추가 확인</summary><p>${esc(p.note || '태그명을 참고해 연결한 PLC 자료입니다. 명판·현행 배선·현재 프로그램과의 동일성을 확인해야 합니다.')}</p><p>전기도면 FG: ${esc(d?.electrical_fgs.join(', ') || '설비 대응 확인 후 연결')}</p>${docButton('작성 상태·다음 확인','requirements-audit.html#priority-'+p.key)}${button('설비 요약 전체 보기','summary',p.key)}</details>`}
      <button type="button" class="card-return" data-layout-return>배치도·카드 목록으로 돌아가기</button>
      <p class="card-footnote">원본 분석 · 현장 확인 · 실제 복구를 구분합니다.</p></aside>`;
  }
  function renderPriority() {
    const q=state.layoutQuery.trim().toLocaleLowerCase();
    const shown=data.priority.filter(p=>!q || `${p.name} ${p.plc_id} ${p.key}`.toLocaleLowerCase().includes(q));
    const node=p=>`<button type="button" class="layout-node ${state.selected===p.key?'selected':''} ${p.match==='unknown'?'unidentified':''} ${equipmentStatus(p.key)?'excluded':''}" data-layout-select="${esc(p.key)}" aria-label="${esc(p.name+' 설비카드')}" aria-pressed="${state.selected===p.key}" style="left:${Math.round((p.x-470)*0.47+25)}px;top:${Math.round((p.y-470)*0.47+42)}px"><span class="node-top">${esc(p.plc_id || p.key)}<span>${equipmentStatus(p.key)?'제외':p.match==='unknown'?'미확정':p.match==='candidate'?'후보':'참고'}</span></span><span class="node-main">${layoutIcon(p)}<strong>${esc(p.name)}</strong></span></button>`;
    return `<section class="process-heading"><div><span class="eyebrow">DECOATING / EQUIPMENT WORKSPACE</span><h2>디코팅 설비 작업실</h2><p>설비를 눌러 수리 절차와 원본 근거를 확인하세요.</p></div><div class="process-count"><strong>21</strong> 현재 대상 <span>원래 목록 23 · 다른 공정 2 제외</span></div></section>
      <div class="process-workspace"><section class="process-navigation" aria-label="디코팅 설비 배치도">
      <div class="process-toolbar"><label class="layout-search"><span class="sr-only">배치도 설비 검색</span><input type="search" id="layout-search" placeholder="설비명 · PLC 태그 검색" value="${esc(state.layoutQuery)}"></label><div class="layout-mode-switch" role="group" aria-label="설비 보기 방식"><button type="button" data-layout-mode="map" aria-pressed="${state.layoutMode==='map'}">배치도</button><button type="button" data-layout-mode="cards" aria-pressed="${state.layoutMode==='cards'}">카드 목록</button></div></div>
      <div class="layout-legend"><span><i></i>태그 참고</span><span><i class="candidate-dot"></i>대응 후보</span><span><i class="unknown-dot"></i>식별 필요</span><span><i class="excluded-dot"></i>다른 공정 제외</span></div>
      ${state.layoutMode==='map'?`<div class="layout-map-controls"><span>배치도 안에서 좌우로 이동할 수 있습니다.</span><div><button type="button" data-layout-zoom="out" aria-label="배치도 축소">−</button><output id="layout-zoom-value">${Math.round(state.layoutZoom*100)}%</output><button type="button" data-layout-zoom="in" aria-label="배치도 확대">＋</button><button type="button" data-layout-zoom="fit">전체 보기</button></div></div>
      <div class="layout-viewport" id="layout-viewport" tabindex="0" aria-label="설비 배치도 이동 영역"><div class="layout-scaled" style="width:${1220*state.layoutZoom}px;height:${660*state.layoutZoom}px"><div class="layout-canvas" style="transform:scale(${state.layoutZoom})"><span class="layout-zone zone-air">팬 · 댐퍼</span><span class="layout-zone zone-heat">연소 · 열회수</span><span class="layout-zone zone-material">원료 · 제품 이송</span>${shown.map(node).join('')}${shown.length?'':'<p class="layout-empty">검색 결과가 없습니다.</p>'}</div></div></div>`
      :`<div class="equipment-card-grid">${shown.map(p=>`<button type="button" class="equipment-grid-card ${state.selected===p.key?'selected':''} ${equipmentStatus(p.key)?'excluded':''}" data-layout-select="${esc(p.key)}" aria-label="${esc(p.name+' 설비카드')}" aria-pressed="${state.selected===p.key}"><span class="grid-card-icon">${layoutIcon(p)}</span><span class="eyebrow">${esc(p.plc_id || p.key)}</span><strong>${esc(p.name)}</strong><small>${esc(layoutBadge(p))}</small></button>`).join('') || '<p>검색 결과가 없습니다.</p>'}</div>`}
      <div class="layout-reference"><p>디코팅 시안의 위치를 참고한 탐색 화면입니다. 실제 배관·신호 연결은 P&ID와 전기도면에서 확인합니다.</p><a href="${esc(data.priority_source.url)}" target="_blank" rel="noopener">SEJIN 원본 배치도 ↗</a>${docButton('P&ID 원본','sources/PID_1684n002I.pdf#page=1')}${docButton('기본 HMI','assets/HMI_DECOATER.png')}</div></section>${renderEquipmentCard()}</div>`;
  }
  function rememberLayoutScroll() {
    const viewport=$('layout-viewport');
    if(viewport) state.layoutScroll=[viewport.scrollLeft,viewport.scrollTop];
  }
  function restoreLayoutScroll() {
    const viewport=$('layout-viewport');
    if(viewport) [viewport.scrollLeft,viewport.scrollTop]=state.layoutScroll;
  }
  function renderSummary() {
    const {p,d} = selection();
    if (!d) return unknownPanel()+(equipmentStatus(p?.key) ? '<div class="notice">'+esc(equipmentStatus(p.key).label)+' · 관련 조사·분석·매뉴얼 보강 중단. 기존 배치도 자료만 보존합니다.</div>' : docButton('식별·원본 후보·필요 자료','unresolved-identity.html#identity-'+p.key))+'<div class="inline-actions">'+docButton('작성 상태·다음 확인','requirements-audit.html#priority-'+p.key)+'</div>';
    if (equipmentStatus(d.id)?.exclude_from_current_detailed_analysis) return panel('현재 상세 작업에서 제외', '<p>'+esc(d.id+' · '+equipmentStatus(d.id).label)+'(2026-10-09)</p><p>관련 상세 조사·분석·새 매뉴얼 보강을 중단했습니다. 원본 백업·도면·기존 문서·불일치는 보존합니다. 사용자 제공 상태이며 부모 현장 검증 결과가 아닙니다.</p><div class="quick-links">'+docButton('보존된 기존 매뉴얼','devices/'+d.id+'.html')+docButton('보존된 제어 명세','control-specs/'+d.id+'.html')+docButton('보존된 수리 절차','procedures/'+d.id+'.html')+docButton('작성 상태·제외 범위','requirements-audit.html#equipment-'+d.id)+'</div>');
    const children = data.equipment.filter(v => v.parent === d.id);
    return `${equipmentStatus(d.id) ? '<div class="notice">'+esc(equipmentStatus(d.id).label)+' · 상세 조사 제외. 아래는 과거 백업·도면 자료입니다.</div>' : ''}${p ? '<div class="notice">'+esc(matchText(p))+' · 아래 내용은 '+esc(d.id)+' PLC 자료입니다. SEJIN 설비와의 대응을 확정한 결과는 아닙니다.</div>' : ''}
      ${panel('설비 역할과 자료 상태', `<p>${esc(d.role)}</p><p class="muted">${esc(d.installation_status)} · ${esc(d.evidence_status)}</p>${d.note ? `<div class="notice">${esc(d.note)}</div>` : ''}<div class="quick-links">${docButton('작성 상태·다음 확인','requirements-audit.html#'+(p?'priority-'+p.key:'equipment-'+d.id))}${['CC01','AB01','HE01'].includes(d.id)?docButton('본체·계측 경계·증상별 수리','body-manual.html#body-'+d.id):''}${button('매뉴얼 읽기','manual')}${button('증상별 진단','repair')}${button('동작 조건 확인','spec')}${button('개선·확인 메모','notes')}</div>`)}
      <div class="stats">${[[d.inputs.length,'입력 참조'],[d.outputs.length,'출력 참조'],[d.hmi.length,'HMI 설정'],[d.networks.length,'관련 원본 LAD'],[d.test_count,'시험 설계']].map(([n,t]) => `<div class="stat"><strong>${n}</strong><span>${t}</span></div>`).join('')}</div>
      <div class="columns">${panel('근거 연결', `<div class="status-row"><span>PLC 태그</span><code>${esc(d.id)}</code></div><div class="status-row"><span>전기도면 FG</span><span>${esc(d.electrical_fgs.join(', ') || '직접 회로 미식별')}</span></div><div class="status-row"><span>직접 대상 정적 경로</span><span>${d.direct_rule_count}개</span></div><div class="status-row"><span>상태·단계 경로</span><span>${d.state_path_count}개</span></div><div class="inline-actions">${button('I/O·HMI','io')}${button('래더 목록','ladder')}${button('도면 보기','drawings')}</div>`)}
      ${panel('확인할 내용', `<ul>${d.pending.map(v => `<li>${esc(v)}</li>`).join('')}</ul><p class="muted">원본 정적 해석과 실제 PLC 실행 결과는 구분합니다. 공유 네트워크 참조는 전용 소유를 뜻하지 않습니다.</p><div class="inline-actions">${button('확인 대장','checks')}${button('시험 항목','tests')}</div>`)}</div>
      ${children.length || d.parent ? panel('상위·하위 설비', `<div class="inline-actions">${d.parent ? button('상위 '+d.parent,'summary',d.parent) : ''}${children.map(c => button(c.id+' · '+c.name,'summary',c.id)).join('')}</div>`) : ''}`;
  }
  function renderIO() {
    const {d,p} = selection();
    const hmiLink=docButton('HMI 설정·표시·PLC 전달 확인','hmi-transfer.html'+(p?'#profile-'+p.key:'#tags'));
    if (!d) return unknownPanel()+(equipmentStatus(p?.key) ? '<div class="notice">'+esc(equipmentStatus(p.key).label)+' · 관련 조사·분석·매뉴얼 보강 중단. 기존 배치도 자료만 보존합니다.</div>' : docButton('식별·원본 후보·필요 자료','unresolved-identity.html#identity-'+p.key))+'<div class="inline-actions">'+hmiLink+'</div>';
    const signals = (title, rows) => panel(title, table(['주소','원본 심볼','자료형','원본 설명'], rows.map(v => [`<code>${esc(v['백업 주소'].toUpperCase())}</code>`,esc(v['원본 심볼']),esc(v['자료형']),esc(v['설명'])])));
    return `<h2>I/O와 HMI · ${esc(d.id)}</h2><div class="inline-actions">${hmiLink}</div><div class="notice info">현재값은 연결되어 있지 않습니다. 백업 주소와 과거 주석 주소를 구분하며, 관련 신호에는 공유 참조가 포함될 수 있습니다.</div>${signals('물리 입력',d.inputs)}${signals('물리 출력',d.outputs)}${signals('내부 심볼',d.internal)}${panel('HMI 설정',table(['태그','설정 주소','Access Name','내부 ID'],d.hmi.map(h => ['HMI 태그','설정 주소','Access Name','내부 ID'].map(k => esc(h[k])))))}`;
  }
  function renderLadder() {
    const {d} = selection(); if (!d) return unknownPanel();
    return `<h2>원본 래더 · ${esc(d.id)}</h2><p class="muted">관련 네트워크 목록입니다. 목록 순서는 실행·호출 순서가 아닙니다.</p>${table(['블록','제목','네트워크','식별한 피연산자'],d.networks.map(n => [esc(n['블록']),esc(n['제목']),docButton('네트워크 '+n['문서 ID'],'networks/network-'+n['문서 ID']+'.html'),esc(n['해석 피연산자']+'/'+n['전체 피연산자'])]))}<div class="inline-actions">${docButton('PLC 전체 네트워크','plc-networks.html')}${button('제어 명세의 조건식','spec')}</div>`;
  }
  function renderDrawings() {
    const {p,d,name}=selection();
    const profile=drawingMap.get(p?.key);
    if(!profile) return renderReferenceDrawings();
    const sheet=profile.sheets.find(s=>s.id===state.drawing) || profile.sheets[0];
    state.drawing=sheet.id;
    drawingLastByKind.set(profile.key+':'+sheet.kind,sheet.id);
    const circuit=profile.circuit;
    const paths=sheet.kind==='OEM 전기' ? (circuit?.paths || []).filter(r=>String(r.fg)===String(sheet.fg)) : [];
    const source=sheet.source+(sheet.page?'#page='+sheet.page:'');
    const groups=[sheet.kind];
    const guideLinks=d?`${validDoc('circuit-guides/'+d.id+'.html')?docButton('단자·전체 경로','circuit-guides/'+d.id+'.html'):''}${validDoc('construction-guides/'+d.id+'.html')?docButton('케이블·접속함 근거','construction-guides/'+d.id+'.html'):''}`:'';
    return `<div class="drawing-heading"><div><span class="eyebrow">DRAWING / SOURCE EVIDENCE</span><h2>${esc(name)} · 도면 작업실</h2><p>도면을 선택하고 단자·케이블·PLC 근거를 함께 확인하세요.</p></div>${button('배치도·설비카드','priority',p.key)}</div>
      <p class="drawing-boundary">${esc(matchText(p))}. 관련 도면의 공유 참조이며 현재 CPU·실제 접속·복구 상태는 확인 전입니다.</p>
      <div class="drawing-kind-tabs" role="group" aria-label="도면 종류">${drawingKinds.map(([kind,label])=>{const count=profile.sheets.filter(s=>s.kind===kind).length;return `<button type="button" data-drawing-kind="${esc(kind)}" aria-pressed="${sheet.kind===kind}" ${count?'':'disabled'}><strong>${esc(label)}</strong><span>${count}개 참조</span></button>`;}).join('')}</div><p class="drawing-kind-help">선택한 종류의 도면만 표시합니다. 공유 참고 페이지를 포함한 목록입니다.</p>
      <div class="drawing-workspace ${state.drawingWide?'drawing-wide':''}"><nav class="drawing-library" aria-label="설비 관련 도면 목록">${groups.map(kind=>`<section><h3>${esc(kind)}</h3>${profile.sheets.filter(s=>s.kind===kind).map(s=>`<button type="button" data-drawing="${esc(s.id)}" aria-pressed="${s.id===sheet.id}">${s.image?`<img src="${esc(s.image)}" alt="" loading="lazy">`:''}<span><strong>${esc(s.title)}</strong><small>${esc(s.extent)}</small></span></button>`).join('')}</section>`).join('')}</nav>
      <section class="drawing-main" aria-label="선택한 도면"><div class="drawing-title"><span class="eyebrow">${esc(sheet.kind)}</span><h3>${esc(sheet.title)}</h3><p>${esc(sheet.source.split('/').pop())} · ${esc(sheet.revision)}</p></div>
      <div class="drawing-toolbar"><div role="group" aria-label="도면 확대 조절"><button type="button" data-drawing-zoom="out" aria-label="도면 축소" ${state.drawingZoom<=1?'disabled':''}>−</button><output id="drawing-zoom-value">${Math.round(state.drawingZoom*100)}%</output><button type="button" data-drawing-zoom="in" aria-label="도면 확대" ${state.drawingZoom>=4?'disabled':''}>＋</button><button type="button" data-drawing-zoom="fit">전체 보기</button></div><div>${`<button type="button" data-drawing-wide aria-pressed="${state.drawingWide}">${state.drawingWide?'근거 함께 보기':'도면 넓게 보기'}</button>`}<button type="button" data-open-photo>전체 창으로 보기</button>${docButton('원본 페이지 열기',source)}</div></div>
      <div class="drawing-viewport" id="drawing-viewport" tabindex="0" aria-label="도면 확대·이동 영역">${sheet.image?`<img id="drawing-image" src="${esc(sheet.image)}" alt="${esc(sheet.title+' · '+sheet.extent)}" style="width:${state.drawingZoom*100}%;max-width:none">`:'<p>미리보기 없이 원본 PDF 페이지로 확인하는 자료입니다.</p>'}</div>
      <p class="drawing-caption">${esc(sheet.extent)}. 확대 후 도면 안에서 가로·세로로 이동할 수 있습니다.</p><p class="drawing-source-status">${esc(sheet.status)}</p>
      ${profile.warnings.length?`<div class="drawing-warnings"><strong>원본 대조 · 추가 확인</strong>${profile.warnings.map(w=>`<p>${esc(w)}</p>`).join('')}</div>`:''}</section>
      <aside class="drawing-evidence" aria-label="선택 도면의 관련 근거"><h3>도면과 신호 경로</h3>${circuit?`<p>${esc(circuit.equipment)}</p><p class="drawing-evidence-boundary">${esc(circuit.distinction)}</p>`:'<p>본체·주변 설비 참고 또는 식별 자료입니다. 직접 I/O 대응을 새로 배정하지 않습니다.</p>'}
      ${paths.length?paths.map(r=>`<details class="drawing-signal" open><summary>${esc(r.signal)} · ${esc(r.drawing)}</summary><p class="drawing-address">${esc(r.backup)}</p><ol>${r.nodes.map(n=>`<li>${esc(n)}</li>`).join('')}</ol><p>${esc(r.destination)}</p><p class="muted">${esc(r.check)}</p><div class="inline-actions">${(r.native_symbol_references || []).map(n=>docButton('LAD '+n.network+' · UID '+n.uid,'networks/network-'+n.network+'.html')).join('')}</div></details>`).join(''):`<p class="muted">${sheet.kind==='OEM 전기'?'이 페이지의 직접 신호 경로 요약은 기존 작업지에서 확인합니다. 인접 페이지 경로는 전체 회로 근거로 이동하세요.':sheet.kind==='시공·케이블'?'공유 배치·케이블 페이지입니다. 보이는 행과 가림 행의 경계는 케이블·접속함 근거에서 확인하세요.':'공정 위치와 주변 관계를 확인하는 참고 화면입니다.'}</p>`}
      <div class="drawing-guide-links">${guideLinks}${docButton('미완료 항목·완료 기준','requirements-audit.html#open-'+p.key)}${button(d?'증상별 수리':'식별·점검 작업지','repair',p.key)}${d?button('원본 래더','ladder',p.key):''}${d&&validDoc('alarm-guides/'+d.id+'.html')?docButton('알람·리셋 근거','alarm-guides/'+d.id+'.html'):['CC01','AB01','HE01'].includes(d?.id)?docButton('본체·알람 근거','body-manual.html#body-'+d.id):d?.id==='BR01'?docButton('버너 연동 근거','burner-interface.html'):''}</div>
      ${circuit?`<details class="drawing-pending"><summary>원본 작업지의 확인 대기 ${circuit.pending.length}항목</summary><ul>${circuit.pending.map(t=>`<li>${esc(t)}</li>`).join('')}</ul></details>`:''}</aside></div>`;
  }
  function closePhotoViewer() {
    if(!photoViewer)return;
    const dialog=photoViewer.dialog;
    if(document.fullscreenElement===dialog) document.exitFullscreen?.().catch(()=>{});
    dialog.close();dialog.remove();photoViewer=null;
    document.querySelector('[data-open-photo]')?.focus({preventScroll:true});
  }
  function layoutPhoto(reset=false) {
    const v=photoViewer;if(!v || !v.image.naturalWidth)return;
    const stage=v.stage,w=stage.clientWidth,h=stage.clientHeight;
    if(!w || !h)return;
    const ratio=Math.min(w/v.image.naturalWidth,h/v.image.naturalHeight);
    const iw=v.image.naturalWidth*ratio*v.zoom,ih=v.image.naturalHeight*ratio*v.zoom;
    const center=[(stage.scrollLeft+w/2)/(v.canvas.offsetWidth || w),(stage.scrollTop+h/2)/(v.canvas.offsetHeight || h)];
    v.canvas.style.width=Math.max(w,iw)+'px';v.canvas.style.height=Math.max(h,ih)+'px';
    v.image.style.width=iw+'px';v.image.style.height=ih+'px';
    stage.scrollLeft=reset?(Math.max(w,iw)-w)/2:center[0]*Math.max(w,iw)-w/2;
    stage.scrollTop=reset?(Math.max(h,ih)-h)/2:center[1]*Math.max(h,ih)-h/2;
    v.dialog.querySelector('[data-photo-value]').textContent=Math.round(v.zoom*100)+'%';
    v.dialog.querySelector('[data-photo="out"]').disabled=v.zoom<=1;
    v.dialog.querySelector('[data-photo="in"]').disabled=v.zoom>=6;
    stage.classList.toggle('photo-pannable',v.zoom>1);
  }
  function showPhoto(sheet) {
    const v=photoViewer;if(!v)return;
    v.sheet=sheet;v.zoom=1;
    const sameKind=v.profile.sheets.filter(s=>s.kind===sheet.kind),index=sameKind.findIndex(s=>s.id===sheet.id);
    v.dialog.querySelector('[data-photo-title]').textContent=selection(v.profile.key).name+' · '+sheet.title;
    v.dialog.querySelector('[data-photo-counter]').textContent=sheet.kind+' · '+(index+1)+' / '+sameKind.length;
    v.dialog.querySelector('[data-photo-description]').textContent=sheet.source.split('/').pop()+' · '+sheet.revision+' · '+sheet.extent+' · '+sheet.status;
    v.dialog.querySelector('[data-photo="previous"]').disabled=index===0;
    v.dialog.querySelector('[data-photo="next"]').disabled=index===sameKind.length-1;
    v.image.alt=sheet.title+' · '+sheet.extent;
    v.image.onload=()=>layoutPhoto(true);v.image.src=sheet.image;
    v.dialog.querySelector('[data-photo-value]').textContent='100%';
    if(v.image.complete)layoutPhoto(true);
  }
  function openPhotoViewer() {
    const profile=drawingMap.get(selection().p?.key),sheet=profile?.sheets.find(s=>s.id===state.drawing);
    if(!sheet?.image)return;
    closePhotoViewer();
    const dialog=document.createElement('dialog');dialog.className='drawing-photo-viewer';
    dialog.setAttribute('aria-labelledby','photo-title');
    dialog.innerHTML=`<header class="photo-header"><div><h2 id="photo-title" data-photo-title></h2><span data-photo-counter></span></div><button type="button" data-photo="close" aria-label="포토뷰어 닫기">닫기 ×</button></header>
      <div class="photo-toolbar"><div><button type="button" data-photo="previous" aria-label="이전 도면">← 이전</button><button type="button" data-photo="next" aria-label="다음 도면">다음 →</button></div><div><button type="button" data-photo="out" aria-label="포토뷰어 축소">−</button><output data-photo-value>100%</output><button type="button" data-photo="in" aria-label="포토뷰어 확대">＋</button><button type="button" data-photo="fit">화면에 맞춤</button></div><div><button type="button" data-photo="fullscreen">브라우저 전체화면</button><button type="button" data-photo="source">원본 페이지</button></div></div>
      <div class="photo-stage" tabindex="0" aria-label="포토뷰어 도면 이동 영역"><div class="photo-canvas"><img draggable="false" alt=""></div></div><footer class="photo-footer"><p data-photo-description></p><span>휠로 확대 · 확대 후 드래그로 이동 · ←/→ 도면 · Esc 닫기</span><p data-photo-message role="status"></p></footer>`;
    document.body.appendChild(dialog);
    photoViewer={dialog,profile,sheet,zoom:1,stage:dialog.querySelector('.photo-stage'),canvas:dialog.querySelector('.photo-canvas'),image:dialog.querySelector('img')};
    dialog.addEventListener('cancel',e=>{e.preventDefault();closePhotoViewer();});
    dialog.addEventListener('keydown',e=>{
      const action=e.key==='ArrowLeft'?'previous':e.key==='ArrowRight'?'next':e.key==='+' || e.key==='='?'in':e.key==='-'?'out':e.key==='0'?'fit':'';
      if(action){e.preventDefault();photoAction(action);}
    });
    const stage=photoViewer.stage;
    stage.addEventListener('wheel',e=>{e.preventDefault();photoAction(e.deltaY<0?'in':'out');},{passive:false});
    let drag=null;
    stage.addEventListener('pointerdown',e=>{if(e.button!==0 || photoViewer?.zoom<=1)return;drag=[e.clientX,e.clientY,stage.scrollLeft,stage.scrollTop];stage.setPointerCapture(e.pointerId);stage.classList.add('photo-dragging');});
    stage.addEventListener('pointermove',e=>{if(!drag)return;stage.scrollLeft=drag[2]-(e.clientX-drag[0]);stage.scrollTop=drag[3]-(e.clientY-drag[1]);});
    const endDrag=()=>{drag=null;stage.classList.remove('photo-dragging');};
    stage.addEventListener('pointerup',endDrag);stage.addEventListener('pointercancel',endDrag);stage.addEventListener('lostpointercapture',endDrag);
    dialog.addEventListener('fullscreenchange',()=>{dialog.querySelector('[data-photo="fullscreen"]').textContent=document.fullscreenElement===dialog?'전체화면 해제':'브라우저 전체화면';layoutPhoto(true);});
    const resize=new ResizeObserver(()=>layoutPhoto());resize.observe(stage);
    dialog.addEventListener('close',()=>resize.disconnect(),{once:true});
    dialog.showModal();showPhoto(sheet);stage.focus({preventScroll:true});
  }
  async function photoAction(action) {
    const v=photoViewer;if(!v)return;
    if(action==='close'){closePhotoViewer();return;}
    if(['in','out','fit'].includes(action)){v.zoom=action==='fit'?1:Math.max(1,Math.min(6,v.zoom+(action==='in'?0.5:-0.5)));layoutPhoto(action==='fit');return;}
    if(action==='previous' || action==='next') {
      const sheets=v.profile.sheets.filter(s=>s.kind===v.sheet.kind),i=sheets.findIndex(s=>s.id===v.sheet.id)+(action==='next'?1:-1);
      if(!sheets[i])return;
      state.drawing=sheets[i].id;state.drawingZoom=1;route('drawings',v.profile.key);if(photoViewer===v && v.sheet.id!==sheets[i].id)showPhoto(sheets[i]);return;
    }
    if(action==='source'){const path=v.sheet.source+(v.sheet.page?'#page='+v.sheet.page:'');closePhotoViewer();openEmbedded(path,v.profile.key);return;}
    if(action==='fullscreen') {
      try {if(document.fullscreenElement===v.dialog)await document.exitFullscreen();else if(v.dialog.requestFullscreen)await v.dialog.requestFullscreen();else throw new Error('unavailable');}
      catch(_){if(photoViewer===v)v.dialog.querySelector('[data-photo-message]').textContent='이 브라우저에서는 전체화면 전환이 지원되지 않습니다. 전체 창 보기에서 계속 사용할 수 있습니다.';}
    }
  }
  function renderReferenceDrawings() {
    const {d} = selection();
    const construction = data.construction_reference;
    return `<h2>도면과 기본 HMI</h2><div class="doc-buttons">${docButton('기존 DECOATER HMI','assets/HMI_DECOATER.png')}${docButton('P&ID 원본','sources/PID_1684n002I.pdf#page=1')}${docButton('기존 OEM 전기도면','sources/Electrical_Rev2.pdf#page=1')}${docButton('추가 시공도면 · 배관·케이블','construction-guide.html')}${d ? (validDoc(`circuit-guides/${d.id}.html`)?docButton('단자·릴레이 회로 추적',`circuit-guides/${d.id}.html`):'')+[...new Set([...(d.circuit_fgs || []),...d.electrical_fgs])].map(f => docButton('FG '+f+' / PDF '+pdfPage(f),'sources/Electrical_Rev2.pdf#page='+pdfPage(f))).join('') : ''}</div>${construction ? panel('추가 시공도면 · 현재 승인·배선 확인 전', `<p>Can-Decoating_20241118.pdf · 64페이지. 설비 배치·접속함·배관·케이블 양단을 기존 회로·PLC 근거와 함께 봅니다. 표지 FOR APPROVAL, 개정란 24.11.11 first draft design입니다.</p><div class="inline-actions">${docButton('64페이지 색인·확인 대기 '+construction.new_review_items+'건','construction-guide.html')}${docButton('시공도면 원본',construction.source+'#page=1')}${d && validDoc(`construction-guides/${d.id}.html`) ? docButton(d.id+' 케이블·접속함 추적',`construction-guides/${d.id}.html`) : ''}${d ? (d.construction_pages || []).map(p => docButton('시공도면 PDF '+p,construction.source+'#page='+p)).join('') : ''}</div><p class="muted">가림 행은 배선 근거에서 제외합니다. 전체 PLC 대응 미확정 설비는 자동 연결하지 않습니다.</p>`) : ''}<img class="source-image" src="assets/HMI_DECOATER.png" alt="제공된 기존 DECOATER HMI 화면"><p class="diagram-caption">제공된 HMI 이미지입니다. 표시값은 촬영 당시 값이며 현재값이 아닙니다. 설비 선택은 왼쪽 목록에서 유지됩니다.</p>${!d ? unknownPanel() : ''}`;
  }
  function renderSimulator() {
    return panel('시뮬레이터 · 영구 중지','<div class="notice">사용자 지시에 따라 작성·수정·생성·실행·행동 시험을 하지 않습니다. 기존 자산과 과거 시험 기록은 보존 자료입니다.</div>');
  }
  function renderStructure() {
    const m = window.GME_PROGRAM_MODEL;
    if (!m) return panel('프로그램 구조', '<p>분석 자료가 없습니다.</p>');
    const {d,p} = selection();
    const ids = new Set(m.equipment[d?.id]?.networks || []);
    const related = new Set(m.networks.filter(n=>ids.has(n.id)).map(n=>n.block));
    const calls = m.calls.filter(c=>c.caller==='main' || related.has(c.caller) || related.has(String(c.callee || '').toLowerCase()));
    const refs = m.accesses.filter(a=>ids.has(a.network));
    const names = new Set(refs.map(a=>a.signal));
    const multi = m.multiple_writers.filter(a=>names.has(a.signal));
    return `<h2>PLC 호출·신호 구조 · ${esc(d?.id || '전체')}</h2><div class="notice info">원본 XML의 호출 위치·연결과 신호 접근을 추적합니다. 색인 순서와 XML Parts 순서는 TIA 실행 순서 확인 전입니다. 호출 인자의 읽기·쓰기 방향은 인터페이스 검증이 필요한 경우 단정하지 않습니다.</div>
      <div class="stats">${[[m.counts.calls,'전체 호출 위치'],[m.counts.resolved_calls,'이름·블록 대응 호출'],[m.counts.accesses,'네트워크별 신호 참조'],[m.counts.executable,'독립 실행 지원 네트워크'],[multi.length,'관련 복수 쓰기 신호']].map(([n,t])=>`<div class="stat"><strong>${n}</strong><span>${t}</span></div>`).join('')}</div>
      <div class="inline-actions">${d && validDoc(`signal-guides/${d.id}.html`) ? docButton(d.id+' 신호 전달·복수 쓰기',`signal-guides/${d.id}.html`) : ''}${docButton('전체 신호 분석 목록','signal-trace.html')}${docButton('공통 허가·자동 요청·알람·리셋','common-control.html')}${p ? docButton(p.key+' 공통 제어·복구 확인',`common-guides/${p.key}.html`) : ''}</div>
      ${panel('main과 선택 설비 관련 호출', table(['호출 블록 → 대상','근거','상태·인자'], calls.map(c=>[`${esc(c.caller)} → <strong>${esc(c.callee || '대상 미해석')}</strong>`,docButton('네트워크 '+c.network,'networks/network-'+c.network+'.html'),`${c.callee_found?'블록명 대응':'인터페이스·대상 확인 필요'}${Object.keys(c.bindings).length?'<br>'+esc(Object.entries(c.bindings).map(([k,v])=>k+' = '+v.join(', ')).join(' / ')):''}`])))}
      ${panel('선택 설비의 신호 읽기·쓰기', table(['원본 신호','역할','블록·근거'],refs.map(a=>[`<code>${esc(a.name)}</code>`,esc(a.role),`${esc(a.block)} · ${docButton(String(a.network),'networks/network-'+a.network+'.html')}`])))}
      ${panel('여러 네트워크가 쓰는 관련 신호',table(['신호','쓰기 위치'],multi.map(a=>[`<code>${esc(a.signal)}</code>`,a.locations.map(l=>`${esc(l.block)} · ${docButton(String(l.network),'networks/network-'+l.network+'.html')}`).join(' / ')])))}
      ${panel('검토할 개선', `<ul><li>같은 신호에 대한 HMI 요청·자동 시퀀스·알람 정지 쓰기를 호출 순서와 함께 대조합니다.</li><li>이전 주소와 현재 출력 주소가 다른 설비는 실제 Q까지의 전달 경로를 확인합니다.</li><li>시뮬레이션 블록의 호출 조건과 현장 입력을 대체하는 경계를 확인합니다.</li><li>정지·고장 후 요청 Flag와 리셋·재기동의 관계를 원본과 현재 자료로 대조할 항목으로 남깁니다.</li></ul><div class="inline-actions">${docButton('개선 후보 검토','improvement-review.html')}${button('검토 결과 기록','notes')}${docButton('전체 구조 원본 데이터','registers/program-model.json')}</div>`)}${!d?unknownPanel():''}`;
  }
  function renderModelResults() {
    const r = data.virtual_results;
    if (!r) return '';
    const {d} = selection();
    const rows = r.results.filter(t=>!d || !t.equipment || t.equipment===d.id);
    return panel(`가상 모델 행동 시험 · ${r.passed} 통과 / ${r.failed} 실패`, `<p>${esc(r.scope)}</p><p class="muted">기존 577개 시험의 전체 합격은 0건입니다. 아래 시험은 관련 조건의 부분 검증이며 실제 Q/I 전달·전체 호출·전원 재시작은 검증 전입니다.</p><p class="muted">FN04의 설정0 시험은 모터 제어에 값을 직접 주입합니다. 원본1689의 5~100 제한과 전체 호출 순서는 포함하지 않으며, 공통 인버터에 연결된 두 모터의 실제 응답도 따로 확인해야 합니다.</p>${table(['시험','내용','연결 설계','결과'],rows.map(t=>[esc(t.id),esc(t.title),esc(t.design || '엔진 동작 검증'),esc(t.status==='passed'?'가상 모델 통과':'실패')]))}${docButton('입력·쓰기·시간 증거 보기','registers/virtual-plc-test-results.json')}`);
  }
  function filterUI(kind) {
    const {d} = selection();
    const options = [['','전체 설비'],['selected','선택 설비'+(d ? ' · '+d.id : ' · 대응 미확정')]];
    return `<div class="inline-actions">${button('시험 설계','tests')}${button('확인 대장','checks')}${button('자료 불일치 18건','conflicts')}</div><div class="filters"><label class="sr-only" for="table-search">${kind} 검색</label><input type="search" id="table-search" placeholder="ID·상황·내용 검색" value="${esc(state.tableQuery)}"><label class="sr-only" for="table-device">시험·확인 범위</label><select id="table-device">${options.map(([v,t]) => `<option value="${v}" ${state.tableDevice === v ? 'selected' : ''}>${esc(t)}</option>`).join('')}</select><span id="table-count" class="count"></span></div><div id="register-table"></div>`;
  }
  function renderRegister() {
    const {d} = selection();
    const checks = state.view === 'checks';
    const source = checks ? data.verification : data.tests;
    const q = state.tableQuery.toLocaleLowerCase();
    const rows = source.filter(r => (!q || Object.values(r).join(' ').toLocaleLowerCase().includes(q)) && (state.tableDevice !== 'selected' || r['설비 ID'] === d?.id));
    $('table-count').textContent = `${rows.length} / ${source.length}건`;
    const cols = checks ? ['확인 ID','항목','확인 작업','상태'] : ['시험 ID','상황','주입 조건','확인할 결과','상태'];
    $('register-table').innerHTML = table(['설비',...cols,...(checks?[]:['가상 부분 시험'])], rows.map(r => [button(r['설비 ID'],'summary',r['설비 ID'],'class="table-link"'),...cols.map(k => esc(r[k])),...(checks?[]:[esc((data.virtual_results?.results || []).filter(t=>t.design===r['시험 ID']).map(t=>t.id+' · '+(t.status==='passed'?'부분 통과':'실패')).join(' / ') || '미실행')])]));
  }
  function renderConflicts() {
    return `<h2>자료 불일치 · 18건</h2><p class="muted">문서 내용은 대조했으며 원인·해소는 미확정입니다. 개선·작업 메모는 별도 기록으로 보관하고 원본 상태를 덮어쓰지 않습니다.</p><div class="inline-actions">${button('확인 대장','checks')}${button('검토 메모','notes')}</div>${table(['ID','항목·자료 내용','관련 범위','다음 검증','상태'],data.conflicts.map(c => [esc(c.ID),`<strong>${esc(c['항목'])}</strong><br>${esc(c['자료 내용'])}`,esc(c['관련 범위']),esc(c['다음 검증']),esc(c['해소 상태'])]))}`;
  }
  function renderReview() {
    return `<h2>근거 검토·확인 · ${reviewItems.length}항목</h2><div class="notice info">원본 불일치 18 · 시공 검토 7 · 공통 확인 10 · 개선 후보 6 · 설비 동일성 23개를 구분합니다. 원본 확인 대장 1,060건과 시험 설계 577건은 별도 대장입니다. 항목 메모는 사용자 기록이며 원인 해소·실물 확인·PLC 적용 상태를 변경하지 않습니다.</div>
      <div class="inline-actions">${docButton('인쇄용 전체 검토 목록','evidence-review.html')}${button('기존 불일치 18건','conflicts')}${button('확인 대장 1,060건','checks')}</div>
      <div class="filters"><label for="review-search">검토 검색<input type="search" id="review-search" value="${esc(state.tableQuery)}" placeholder="ID·설비·신호·관찰 내용"></label><label for="review-kind">종류<select id="review-kind"><option value="">전체 종류</option>${Object.entries(reviewKinds).map(([k,v])=>`<option value="${k}" ${state.reviewKind===k?'selected':''}>${esc(v)} · ${data.evidence_review?.counts[k] || 0}</option>`).join('')}</select></label><label for="review-scope">범위<select id="review-scope"><option value="">전체 항목</option><option value="selected" ${state.tableDevice==='selected'?'selected':''}>선택 설비·공통 자료</option></select></label><span id="review-count" class="count"></span></div>
      <p class="muted">전체 공통 자료와 신호 참조 연관은 해당 설비의 직접 제어·전용 소유·실물 동일성을 뜻하지 않습니다. 대응 미확정 설비에는 태그를 새로 부여하지 않습니다.</p><div id="review-table"></div>`;
  }
  function renderReviewRows() {
    const {p,d}=selection();
    const q=state.tableQuery.toLocaleLowerCase();
    const rows=reviewItems.filter(r=>(!state.reviewKind || r.kind===state.reviewKind) &&
      (!q || [r.id,r.title,r.observation,r.next_check,...r.equipment_ids,...r.related_equipment_ids,...r.priority_keys].join(' ').toLocaleLowerCase().includes(q)) &&
      (state.tableDevice!=='selected' || r.global_scope || r.priority_keys.includes(p?.key) || r.equipment_ids.includes(d?.id) || r.related_equipment_ids.includes(d?.id)));
    $('review-count').textContent=`${rows.length} / ${reviewItems.length}항목`;
    $('review-table').innerHTML=table(['검토 항목·원본 상태','자료·관찰과 다음 확인','검토 범위·근거','사용자 기록'],rows.map(r=>{
      const linked=notes.filter(n=>n.review_id===r.id);
      const scope=r.global_scope?'전체 공통 자료':r.declared_scope.join(' / ') || '설비 식별 전';
      return [
        `<span class="badge pending">${esc(reviewKinds[r.kind])}</span><h3>${esc(r.source_id)} · ${esc(r.title)}</h3><p>${esc(r.source_status)}</p>`,
        `<p>${esc(r.observation)}</p><strong>다음 확인</strong><p>${esc(r.next_check)}</p>`,
        `<p>${esc(scope)}</p>${r.related_equipment_ids.length?`<p>신호 참조 연관: ${esc(r.related_equipment_ids.join(' / '))}</p>`:''}<div class="quick-links">${r.links.map(x=>docButton(x.label,x.path)).join('')}${r.priority_keys.map(key=>docButton(key+' 수리 판단',`repair-guides/${key}.html`)).join('')}</div>`,
        `<button type="button" data-review-note="${esc(r.id)}">항목 메모 작성</button><p>연결 메모 ${linked.length}건 · 원본 상태 보존</p>${linked.map(n=>`<button type="button" data-edit-note="${esc(n.id)}">${esc(n.title)}</button>`).join('')}`
      ];
    }));
  }
  function clearReviewFocus() {
    const params=new URLSearchParams(location.hash.slice(1));
    if(params.has('review')){params.delete('review');history.replaceState(null,'','#'+params.toString());}
  }
  function storeDraft(key,value,expected) {
    const next=noteStore.mergeDraft(localStorage.getItem(DRAFT_KEY),key,value,expected);
    const serialized=JSON.stringify(next); localStorage.setItem(DRAFT_KEY,serialized);
    if(localStorage.getItem(DRAFT_KEY)!==serialized) throw new Error('draft_save_not_confirmed');
    return next;
  }
  function startReviewNote(id) {
    const item=reviewMap.get(id); if(!item)return;
    const {p,d}=selection();
    const currentRelated=item.global_scope || item.priority_keys.includes(p?.key) || item.equipment_ids.includes(d?.id) || item.related_equipment_ids.includes(d?.id);
    const primaryKey=item.kind==='identity'?item.source_id: data.priority.find(p=>p.plc_id===item.equipment_ids[0])?.key || item.equipment_ids[0] || item.priority_keys[0];
    const key=currentRelated?state.selected:primaryKey || state.selected;
    let fresh={};
    try { fresh=noteStore.decodeDrafts(localStorage.getItem(DRAFT_KEY)); }
    catch (_) { $('app-message').textContent='저장된 임시 메모를 읽지 못했습니다. 기존 내용을 보존하고 메모 백업을 확인해 주세요.'; return; }
    const existing=drafts[key] || fresh[key];
    if(existing?.noteId || existing?.title || existing?.text) {
      drafts[key]=existing; route('notes',key);
      $('app-message').textContent=existing.review_id===id?'작성 중인 항목 메모를 다시 엽니다.':'작성 중인 메모를 보존했습니다. 기존 메모를 저장한 뒤 새 항목 메모를 선택해 주세요.';
      return;
    }
    const draft={noteId:'',base_note:'',review_id:id,title:item.source_id+' · '+item.title,
      kind:'확인 사항',references:item.id+' / '+item.source_file,text:''};
    try { drafts=storeDraft(key,draft); }
    catch (_) { drafts[key]=draft; $('app-message').textContent='임시 메모 저장을 확인하지 못했습니다. 작성 내용은 복사해 보관해 주세요.'; }
    route('notes',key);
  }
  function renderNotes() {
    const {name} = selection();
    const draft = drafts[state.selected] || {};
    const linkedReview=reviewMap.get(draft.review_id);
    const own = notes.filter(n => n.equipment === state.selected).sort((a,b) => b.updated.localeCompare(a.updated));
    return `<h2>개선·작업 메모 · ${esc(name)}</h2>${linkedReview ? `<div class="notice info">연결 검토: ${esc(linkedReview.id)} · ${esc(linkedReview.title)}<br>원본 상태: ${esc(linkedReview.source_status)} · 사용자 메모는 현재 설비의 기록 컨텍스트이며 실물 동일성 확정이 아닙니다.<button type="button" data-review-focus="${esc(linkedReview.id)}">이 검토 항목 보기</button></div>` : ''}<div class="inline-actions">${button('근거 검토·확인','review')}${docButton('원본 구조 개선 검토 '+(data.review_counts?.improvement_candidates || 0)+'건','improvement-review.html')}${docButton('현재 작업 범위','ACTIVE-WORK.md')}</div><div class="notice info">이 메모는 현재 브라우저에 저장됩니다. SEJIN 작업 이력이나 원본 명세를 변경하지 않습니다. 브라우저 데이터 삭제 전 JSON 백업을 다운로드해 주세요.</div>${storageError ? `<div class="notice">${esc(storageError)}</div>` : ''}
      <div class="columns">${panel('메모 작성', `<form id="note-form" class="note-form"><input type="hidden" name="noteId" value="${esc(draft.noteId || '')}"><input type="hidden" name="base_note" value="${esc(draft.base_note || '')}"><input type="hidden" name="review_id" value="${esc(draft.review_id || '')}"><div class="form-row"><label>제목<input name="title" required maxlength="160" value="${esc(draft.title || '')}" placeholder="예: FN04 출력 주소 확인"></label><label>구분<select name="kind">${['확인 사항','수리·증상 기록','개선 후보','프로그램 분석'].map(v => `<option ${draft.kind === v ? 'selected' : ''}>${v}</option>`).join('')}</select></label></div><label>근거 위치<input name="references" maxlength="500" value="${esc(draft.references || '')}" placeholder="도면 FG, 래더 네트워크, I/O 주소"></label><label>내용<textarea name="text" required maxlength="30000" placeholder="관찰한 내용, 원인 후보, 확인할 작업과 결과를 기록합니다.">${esc(draft.text || '')}</textarea></label><div class="inline-actions"><button type="submit">브라우저에 저장</button><button type="button" data-export-notes>모든 설비 통합 JSON 백업 (${notes.length})</button></div><p class="muted">작성 중 내용도 이 브라우저에 임시 보관합니다. 메모 저장은 시험 합격·수리 완료 처리가 아닙니다.</p></form>`)}
      ${panel(`저장된 메모 · ${own.length}건`, own.length ? own.map(n => `<article class="saved-note"><span class="badge">${esc(n.kind)}</span><h3>${esc(n.title)}</h3><small>${esc(n.updated)}${reviewMap.has(n.review_id) ? ' · 연결 검토 ' + esc(n.review_id) : ''}${n.references ? ' · '+esc(n.references) : ''}</small><p>${esc(n.text)}</p><button type="button" ${n.repair_observation?'data-edit-repair':'data-edit-note'}="${esc(n.id)}">${n.repair_observation?'이 수리 기록 수정':'이 메모 수정'}</button></article>`).join('') : '<div class="empty">이 설비에 저장된 메모가 없습니다.</div>')}</div>`;
  }
  function bc01SourceButton(label,network,kind,uid) {
    const source=data.bc01_standard.source_locations?.find(r=>r.network===Number(network) && r.kind===kind && r.uid===String(uid));
    return docButton(label,source?.path || 'networks/network-'+network+'.html');
  }
  function bc01AddressCards(names) {
    const records=(data.bc01_standard.address_evidence || []).filter(r=>names.includes(r.name));
    if(!records.length)return '';
    return `<section class="bc01-address-evidence"><h4>PLC 선언과 HMI 주소의 정적 대응</h4><p class="bc01-signal-boundary">백업의 DB 번호·비트 오프셋·자료형과 DDE 설정을 대조했습니다. 현재 화면의 표시·쓰기 이벤트, CPU·접속·정전 후 유지 여부는 확인 전입니다.</p><div class="bc01-evidence-grid">${records.map(r=>`<article class="bc01-address-card" data-bc01-address="${esc(r.name)}"><span class="badge">백업 주소 대조 완료</span><h5>${esc(r.backup_address)} · ${esc(r.type)}</h5><code>${esc(r.name)}</code><dl><dt>HMI 설정 태그</dt><dd><code>${esc(r.hmi['HMI 태그'])}</code></dd><dt>DDE 설정 주소</dt><dd><code>${esc(r.hmi['설정 주소'])}</code></dd><dt>접근 영역</dt><dd>${esc(r.access_mode)} · 현재 연결 확인 전</dd></dl><details><summary>원본 주소 선언 보기</summary><div class="bc01-source-actions">${r.declarations.map(d=>docButton('RID '+d.rid+(d.db_number?' · DB '+d.db_number:' · offset '+d.offset_bits+' bit / '+d.width_bits+' bit'),d.file)).join('')}${docButton('보존 HMI 통신 설정','sources/hmi_plc_tags.csv')}</div></details></article>`).join('')}</div></section>`;
  }
  function bc01Supplement(section) {
    const record=data.bc01_standard.supplemental_evidence?.find(r=>r.section===section);
    if(!record)return '';
    const content={
      speed:{lead:'설정값을 읽는 계산 경로와 출력에 쓰는 위치를 함께 확인합니다.',cards:[['읽는 설정값','HMI_DB.SET_PERC_BC01','Int · 설정값 자체를 읽음'],['원본 계산 명령','설정값 × Int 272','Mul · 원본 상수272'],['쓰는 출력','102A5_SPARE0 · %QW288','Word · Peripherie 출력 선언']],boundary:'272의 단위, 출력 신호 형식·현재 ABB 입력·실제 속도는 확인 전입니다. 설정 제한 Move와 Mul의 실행 순서·최종값을 이 카드로 확정하지 않습니다.'},
      other:{lead:'같은 BC_01_MIN에 값을 쓰는 서로 다른 두 경로를 구분합니다.',cards:[['증가 쓰기 · Add','BC_01_MIN + Int 1 → BC_01_MIN','Tag_47 타이머 참조·BC01_Fbk 접점의 직렬 연결'],['0 쓰기 · 별도 Move','Int 0 → BC_01_MIN','Move1118.eno → Move1121.en · 기존 미해석 경로']],boundary:'두 카드는 실행 순서가 아닙니다. 실제 분 단위·증가 주기·ENO 동작·다른 쓰기·최종값은 확인 전입니다.'},
      alarms:{lead:'Signal linearization 호출의 값 출력과 범위 출력을 기존 3개 래치 알람과 구분합니다.',cards:[['호출 입력','102A3_SPARE0 / Coeff 10 / Zero 0','보존 원본 인자 · IN0는 ON에 연결'],['값 출력 · OutValue','HMI_DB.Amp_BC01','Int · 실제 단위·HMI 표시 확인 전'],['범위 출력 · Out_of_range','Allarm.BC01_Absorbption_OFR','Bool · 기존 3개 Set/Reset 래치와 별도']],boundary:'입출력 연결만 확인했습니다. 내부 구현 후보와 BC01 호출의 동일성, 발생 임계값·정지 영향·리셋·실제 복구는 확인 전입니다. 네 번째 확정 고장으로 추가하지 않습니다.'}
    }[section];
    const body=`<section class="bc01-supplement" data-bc01-supplement="${esc(record.id)}"><div class="status-row"><h4>${esc(record.title)}</h4><span class="badge">보존 원본의 연결 확인</span></div><p class="bc01-lead">${content.lead}</p><p class="bc01-signal-boundary">자료의 읽기·쓰기 연결입니다. 현재값·명령 실행 순서·현장 동작을 표시한 그림이 아닙니다.</p><div class="bc01-evidence-grid">${content.cards.map(([title,value,note])=>`<article class="bc01-calculation-card"><h5>${title}</h5><code>${value.replaceAll('.','.<wbr>')}</code><p>${note}</p></article>`).join('')}</div><div class="bc01-unknown">${content.boundary}</div><div class="bc01-source-actions">${bc01SourceButton('원본 명령 위치 · LAD '+record.network+' / '+record.gate+' '+record.part,record.network,'part',record.part)}${section==='other'?bc01SourceButton('0 쓰기 Move1121의 원본 위치',1018,'part','1121'):''}</div><details class="bc01-original"><summary>핀·배선·식별 선언 대조</summary><p>허가 접점 참조: ${record.enable_refs.map(r=>'<code>'+esc(r.name)+' · '+esc(r.type)+'</code>').join(' / ')} · ${bc01SourceButton('허가 연결 Wire '+record.enable_wire,record.network,'wire',record.enable_wire)}</p>${table(['방향·핀','원본 이름·자료형','배선·선언'],record.refs.map(r=>[esc(r.role==='write'?'쓰기':'읽기')+' · '+esc(r.pin),'<code>'+esc(r.name)+'</code><br>'+esc(r.type+' · '+r.scope),bc01SourceButton('Wire '+r.wire,record.network,'wire',r.wire)+'<br>'+docButton('ORef '+r.oref+' · RID '+r.rid+' / NID '+r.nid,r.identifier_file)]))}${docButton('복원 원본 XML',record.file)}</details></section>`;
    return section==='alarms'?`<details class="bc01-supplement-note"><summary>별도 계측 범위 출력 · 기존 3개 래치와 구분</summary>${body}</details>`:body;
  }
  function bc01Items(section) {
    const spec=data.bc01_standard?.specification, alarms=data.bc01_standard?.alarm, circuit=drawingMap.get('P01')?.circuit;
    if(!spec)return [];
    if(section==='overview')return [{id:'identity',title:'설비 식별·역할'},{id:'baseline',title:'자료·개정 기준'},{id:'boundary',title:'확인 범위와 미확정'},{id:'media',title:'사진·부품·도면 대응'}];
    if(section==='io')return [...spec.inputs.map((raw,i)=>({id:'input-'+i,title:raw['백업 주소'].toUpperCase()+' · '+raw['원본 심볼'],raw,role:'물리 입력'})),...spec.outputs.map((raw,i)=>({id:'output-'+i,title:raw['백업 주소'].toUpperCase()+' · '+raw['원본 심볼'],raw,role:'물리 출력'})),...spec.internal.map((raw,i)=>({id:'memory-'+i,title:raw['백업 주소'].toUpperCase()+' · '+raw['원본 심볼'],raw,role:'내부 기억'})),...spec.hmi.map((raw,i)=>({id:'hmi-'+i,title:raw['HMI 태그'],raw,role:'HMI 저장 태그'}))];
    if(section==='control')return [{id:'request',title:'자동 단계·운전 요청',networks:[1843,1844,1847]},{id:'output',title:'최종 출력의 OR 허가',networks:[1935]},{id:'reset',title:'고장에 따른 요청 해제',networks:[1935]},{id:'speed',title:'속도 설정·다른 쓰기',networks:[1692]},{id:'other',title:'응답·시간·다른 관련 쓰기'}];
    if(section==='circuits')return (circuit?.paths || []).map((path,i)=>({id:'path-'+i,title:path.signal,path}));
    if(section==='alarms')return (alarms?.alarms || []).map((alarm,i)=>({id:'alarm-'+i,title:({'Allarm.BC_01_FAULT':'운전 응답 고장','Allarm.BC01_INV':'인버터 이상','Allarm.BC_01_FC':'트립와이어 감시'})[alarm.name] || alarm.name,alarm}));
    if(section==='repair')return repairRecordMap.get('P01').steps.map(step=>({id:step.id,title:step.title,step}));
    return [{id:'documentation',title:'문서·근거 표준'},{id:'cpu',title:'현재 PLC·HMI 대응'},{id:'field',title:'실물·접속·정상 극성'},{id:'recovery',title:'복구·재기동 증거'},{id:'scope',title:'중단·제외 작업'}];
  }
  function staticCondition(node) {
    if(!node)return '[조건 추가 확인]';
    if(node.op==='const')return String(node.literal??(typeof node.value==='boolean'?Number(node.value):node.value));
    if(node.op==='read')return node.name;
    if(node.op==='not')return 'NOT ('+staticCondition(node.arg)+')';
    if(['and','or'].includes(node.op))return '('+node.args.map(staticCondition).join(node.op==='and'?' AND ':' OR ')+')';
    if(['eq','ne','gt','ge','lt','le'].includes(node.op))return '('+staticCondition(node.left)+' '+({eq:'=',ne:'<>',gt:'>',ge:'>=',lt:'<',le:'<='}[node.op])+' '+staticCondition(node.right)+')';
    return '[미해석: '+(node.reason || node.op)+']';
  }
  const bc01SignalLabels={
    'on':'ON 공통 조건', 'start bc01':'BC01 기동 출력', 'flag.m_bc_01':'BC01 운전 요청',
    'inputs.bc01 run':'처리된 운전 응답', 'inputs.bc01_all_inv':'처리된 인버터 이상',
    'inputs.bc01 trip wire':'처리된 트립와이어 감시', 'tag_51':'기동 감시 타이머 비트',
    'flag.reset_allarm':'공통 알람 리셋 요청', 'allarm.bc_01_fault':'운전 응답 고장 래치',
    'allarm.bc01_inv':'인버터 이상 래치', 'allarm.bc_01_fc':'트립와이어 래치',
    'hmi_db.set_perc_bc01':'BC01 속도 설정값', 'flag.maintenance_on':'정비 모드 신호'
  };
  function bc01SignalLabel(name) {return bc01SignalLabels[String(name).toLowerCase()] || name;}
  function bc01ConditionTree(node) {
    if(!node)return '<p class="bc01-unknown">조건 추가 확인</p>';
    if(['and','or'].includes(node.op)) {
      const flatten=n=>n.op===node.op?n.args.flatMap(flatten):[n];
      const terms=flatten(node), constants=terms.filter(n=>node.op==='and' && n.op==='const' && n.value===true);
      const visible=terms.filter(n=>!(node.op==='and' && n.op==='const' && n.value===true));
      return `<section class="bc01-logic-group" data-logic-op="${node.op}"><h5>${node.op==='and'?'모두 충족해야 함':'아래 경로 중 하나 이상 충족'} <span>${node.op.toUpperCase()}</span></h5>${constants.length?'<small class="bc01-constant" data-logic-constant="true">원본 시작 상수 1(TRUE)'+(constants.length>1?' × '+constants.length:'')+'</small>':''}<ul>${visible.map((n,i)=>'<li>'+(node.op==='or'?'<p class="bc01-branch-title">경로 '+(i+1)+'</p>':'')+bc01ConditionTree(n)+'</li>').join('')}</ul></section>`;
    }
    const negated=node.op==='not' && node.arg?.op==='read', read=negated?node.arg:node;
    if(read.op==='read')return `<div class="bc01-contact" data-logic-op="${negated?'not':'read'}"><div><strong>${esc(bc01SignalLabel(read.name))}</strong><code>${esc(read.name)}</code></div><span class="bc01-required">${negated?'0 · 거짓 / NOT':'1 · 참'}</span></div>`;
    if(node.op==='not')return `<section class="bc01-logic-group" data-logic-op="not"><h5>아래 조건 전체를 반전 <span>NOT</span></h5>${bc01ConditionTree(node.arg)}</section>`;
    if(['eq','ne','gt','ge','lt','le'].includes(node.op))return `<div class="bc01-comparison" data-logic-op="${node.op}"><strong>${({eq:'같음',ne:'같지 않음',gt:'보다 큼',ge:'이상',lt:'보다 작음',le:'이하'})[node.op]} 비교</strong><code>${esc(staticCondition(node))}</code></div>`;
    if(node.op==='const')return `<div class="bc01-comparison" data-logic-op="const"><strong>원본 상수</strong><code>${esc(staticCondition(node))}</code></div>`;
    return '<div class="bc01-unknown" data-logic-op="unknown">미해석 조건 · '+esc(node.reason || node.op)+'</div>';
  }
  function bc01ConditionPanel(condition, original) {
    return `<p class="bc01-logic-caption">보존 백업의 조건 · 1은 참, 0은 거짓 · 현재값 표시 아님</p>${condition?bc01ConditionTree(condition):'<p class="bc01-unknown">구조화 조건 추가 확인 · 아래 보존 조건식 전문을 확인합니다.</p>'}<details class="bc01-original"><summary>정적 조건식 전문 보기</summary><p class="bc01-condition"><code>${esc(original || staticCondition(condition))}</code></p></details>`;
  }
  function bc01ReadingGuide() {
    return `<details class="bc01-reading-guide"><summary>조건식 읽는 법 · 1/0, AND/OR, Set/Reset</summary><dl><dt>1 · 참 / 0 · 거짓</dt><dd>조건에서 요구하는 PLC 논리값입니다. 현재값 표시가 아니며 현장 접점의 정상 극성은 별도 확인합니다.</dd><dt>AND · 모두 충족</dt><dd>같은 묶음의 모든 조건이 참이어야 합니다.</dd><dt>OR · 하나 이상 충족</dt><dd>표시된 경로 중 한 경로가 참이면 됩니다. 경로 내부의 AND 조건은 모두 필요합니다.</dd><dt>NOT · 반전</dt><dd>뒤에 있는 조건을 반대로 읽습니다. 신호명만으로 실제 접점의 정상/고장을 확정하지 않습니다.</dd><dt>Set / Reset</dt><dd>기억 비트를 설정(1)하거나 해제(0)하는 경로입니다. 원인 해소·새 운전 요청·실제 복구는 별도 단계입니다.</dd></dl><p>같은 AND/OR는 묶어 표시하고, 원본 시작 상수 1(TRUE)는 묶음 위에 남깁니다. 조건을 계산하거나 PLC를 실행하지 않습니다.</p></details>`;
  }
  function bc01GateExplanation(gate) {
    return ({SCoil:'조건 충족 시 대상 기억 비트를 설정(1)하는 경로입니다. 발생 조건이 사라져도 별도 Reset 경로를 확인해야 합니다.',RCoil:'조건 충족 시 대상 기억 비트를 해제(0)하는 경로입니다. 해제만으로 기동이나 실제 복구가 완료되는 것은 아닙니다.',Coil:'이 네트워크의 조건 참/거짓을 출력 코일에 반영하는 경로입니다. 실제 기동과 응답은 별도로 확인합니다.',Move:'조건 충족 시 입력값을 대상에 쓰는 경로입니다. 같은 대상의 다른 쓰기도 확인합니다.'})[gate] || '보존 원본의 정적 동작 경로입니다. 현재 호출·실행은 별도 확인합니다.';
  }
  function bc01PinEvidence(rule) {
    const evidence=data.bc01_standard.pin_evidence?.[rule.rule_id];
    if(!evidence)return '';
    const source=evidence.source, target=evidence.target;
    const command=p=>p.gate==='Move'?'MOVE · 상수 '+p.value.name+' → '+p.target.name:'Set 코일 · '+p.target.name;
    const refs=[source.target,target.target,source.value,target.value].filter(Boolean);
    const files=[...new Set(refs.map(r=>r.identifier_file))];
    return `<section class="bc01-pin-evidence" data-pin-rule="${esc(rule.rule_id)}"><h4>원본에서 확인한 연결</h4><p class="muted">아래는 정적 핀 배선입니다. 현재값·실행 결과는 확인 전입니다.</p><ol class="bc01-path"><li><strong>선행 명령</strong><p>${esc(command(source))}</p></li><li><strong>명령 사이 연결</strong><p><code>UID ${esc(source.uid)}.${esc(source.pin)} → UID ${esc(target.uid)}.${esc(target.pin)}</code></p></li><li><strong>다음 명령의 대상</strong><p>${esc(command(target))}</p></li></ol><details><summary>Wire·ORef·선언 근거 확인</summary><p>LAD ${esc(evidence.network)} · Wire ${esc(evidence.wire)}</p>${refs.map(r=>'<p><code>'+esc(r.name)+'</code><br>ORef '+esc(r.oref)+' · RID '+esc(r.ref_id)+' · NID '+esc(r.nid)+' · '+esc(r.scope)+'</p>').join('')}<div class="bc01-source-actions">${bc01SourceButton('선행 명령의 원본 위치',evidence.network,'part',source.uid)}${bc01SourceButton('다음 명령의 원본 위치',evidence.network,'part',target.uid)}${bc01SourceButton('명령 사이 Wire '+evidence.wire,evidence.network,'wire',evidence.wire)}</div>${docButton('원본 XML 핀 배선',evidence.file)} ${files.map(f=>docButton('식별 선언 '+f.split('/').pop(),f)).join(' ')}</details><div class="notice">추가 확인: ENO/out의 실제 전달 상태, 현재 블록 호출·다른 쓰기와의 순서, 대상 값 변화가 필요합니다. 핀 연결을 선행 접점 조건과 동일하게 계산하거나 실제 운전·복구로 판정하지 않습니다.</div></section>`;
  }
  function bc01RuleCards(rules) {
    return bc01ReadingGuide()+rules.map(r=> {
      const action=data.bc01_standard.control_conditions[r.rule_id]?.action;
      return `<article class="bc01-rule"><div class="status-row"><strong>${esc(r['동작'])} · ${esc(bc01SignalLabel(r['대상']))}</strong><span class="badge">LAD ${esc(r['네트워크 문서'])} · UID ${esc(r['Part UID'])}</span></div><code class="bc01-target">${esc(r['대상'])}</code><p class="bc01-explanation">${esc(bc01GateExplanation(r['동작']))}</p>${r.opaque?'<div class="bc01-unknown">선행 명령의 ENO/out 연결 · 동작 해석 대기. 이 경로를 완전한 조건 묶음으로 표시하지 않습니다.</div><p class="bc01-condition"><code>'+esc(r['정적 조건식'].replace('(블록 동작 확인)','(원본 핀 연결 · 실행 의미 확인 전)'))+'</code></p>'+bc01PinEvidence(r):bc01ConditionPanel(action?.condition,r['정적 조건식'])}<p>${esc(r['내용'])}</p><p class="muted">${esc(r.execution_status)}${r.opaque?' · 미해석 요소 포함':''}</p>${bc01SourceButton('이 조건의 원본 래더',r['네트워크 문서'],'part',r['Part UID'])}</article>`;
    }).join('');
  }
  function bc01AlarmBody(alarm, profile) {
    const descriptions={
      'Allarm.BC_01_FAULT':['운전 응답 고장','공통 ON 조건·기동 출력·기동 감시 타이머 비트가 모두 1인데, 처리된 운전 응답은 0일 때 알람을 기억하는 경로입니다.','공통 ON 조건·리셋 요청·해당 알람 기억이 모두 1이면 알람 기억을 지우는 경로입니다. 이 Reset에는 운전 응답 정상화 접점이 직접 포함되지 않습니다.'],
      'Allarm.BC01_INV':['인버터 이상','공통 ON 조건·기동 출력·기동 감시 타이머 비트가 모두 1이고, 처리된 인버터 이상도 1일 때 알람을 기억하는 경로입니다.','공통 ON 조건·리셋 요청·해당 알람 기억이 모두 1이면 알람 기억을 지우는 경로입니다. 이 Reset에는 인버터 이상 해소 접점이 직접 포함되지 않습니다.'],
      'Allarm.BC_01_FC':['트립와이어 감시','공통 ON 조건과 처리된 트립와이어 신호가 모두 1일 때 알람을 기억하는 경로입니다.','공통 ON 조건·리셋 요청·해당 알람 기억이 모두 1이고, 처리된 트립와이어 신호는 0일 때 알람 기억을 지우는 경로입니다. 거짓(0)의 실제 정상 극성은 현장 확인 전입니다.']
    };
    const description=descriptions[alarm.name], step=state.bc01AlarmStep;
    const actions=alarm.actions.filter(a=>step==='set'?a.gate==='SCoil':step==='reset'?a.gate==='RCoil':false);
    let body=`<code class="bc01-target">${esc(alarm.name)}</code><p class="muted bc01-signal-boundary">Inputs.*는 보존 백업의 처리 신호입니다. 원시 I/O와의 연결·현재 쓰기/호출은 확인 전이며 실제 센서값으로 단정하지 않습니다.</p><div class="bc01-alarm-steps" role="group" aria-label="알람 확인 단계">${[['set','1. 발생 조건'],['reset','2. 리셋 조건'],['restart','3. 재기동 확인']].map(([id,label])=>`<button type="button" data-bc01-alarm-step="${id}" aria-pressed="${step===id}">${label}</button>`).join('')}</div>`;
    if(step==='restart')body+=`<section class="bc01-explanation"><h4>알람 해제와 재기동을 따로 확인합니다</h4><p>원인 신호의 정상화 → 알람 래치 해제 → 운전 요청·허가 → Q0.0·현장 DI1 → 실제 운전 응답·연동 영향의 증거를 각각 확인합니다. 리셋은 새 운전 요청이나 실제 복구를 보장하지 않습니다.</p></section><ol class="bc01-path">${['최초 알람·원인 입력과 관찰 시각을 기록','원인 정상화 근거와 알람 래치 해제를 각각 확인','요청과 최종 출력의 별도 조건·다른 쓰기 확인','현장 기동 전달·실제 응답·재발 여부 기록'].map(s=>'<li>'+s+'</li>').join('')}</ol><button type="button" data-bc01-jump="control/output">출력·허가 조건 확인</button> ${button('관찰 근거 기록','repair-record')}`;
    else {
      body+=`<p class="bc01-explanation">${esc(description?.[step==='set'?1:2] || bc01GateExplanation(actions[0]?.gate))}</p>${step==='reset'?'<div class="notice">원인 해소와 래치 해제는 다른 확인입니다. 아래는 백업의 Reset 조건이며, 실제 수리 완료나 재기동 허가를 뜻하지 않습니다.</div>':''}${bc01ReadingGuide()}${actions.map(action=>`<article class="bc01-rule"><div class="status-row"><strong>${step==='set'?'발생 시 알람을 기억 · Set (1)':'알람 기억을 해제 · Reset (0)'}</strong><span class="badge">LAD ${action.network} · UID ${esc(action.uid)}</span></div>${bc01ConditionPanel(action.condition)}${bc01SourceButton('원본 접점·배선 확인',action.network,'part',action.uid)}</article>`).join('')}`;
      if(step==='set')body+=profile.timers.filter(t=>actions.some(a=>a.network===t.network)).map(t=>`<details class="bc01-timer"><summary>Tag_51의 기동 감시 조건 · ${esc(staticCondition(t.preset))}</summary><p>보존 원본의 시간 선언입니다. 실제 경과시간·현재 타이머 상태는 확인 전입니다.</p>${bc01ConditionPanel(t.condition)}${bc01SourceButton('타이머 원본 LAD '+t.network+' · UID '+t.uid,t.network,'part',t.uid)}</details>`).join('');
    }
    return body+`<details><summary>알람 간 Reset 차이와 원본 참조 ${alarm.usages.length}개</summary><p>${esc(profile.note)}</p>${table(['원본 위치','읽기/쓰기 · 신호'],alarm.usages.map(u=>[bc01SourceButton('LAD '+u.network+' · Part '+u.part+' / ORef '+u.oref,u.network,'part',u.part),esc(u.scope+' · '+u.role+' · '+u.name)]))}</details>`;
  }
  function bc01CompletionTasks(item) {
    const schema=repairRecordMap.get('P01'), plan=schema?.evidence_plan;
    if(!plan)return [];
    if(item==='cpu')return [{id:'baseline',title:'자료 기준',evidence:plan.preflight},...['request','permit','response','stop'].map(id=>({id,title:({request:'요청·HMI',permit:'출력·허가',response:'입력·처리',stop:'정지·시간'})[id],evidence:plan.steps.find(s=>s.step_id===id)}))];
    if(item==='field')return [{id:'baseline',title:'실물 식별'},...(drawingMap.get('P01')?.circuit?.paths || []).map((path,i)=>({id:'path-'+i,title:path.signal,path}))];
    return [];
  }
  function bc01EvidenceRequirements(requirements) {
    return `<div class="bc01-evidence-requirements">${requirements.map((r,i)=>`<article class="bc01-evidence-requirement"><div class="status-row"><strong>${String(i+1).padStart(2,'0')} · ${esc(r.owner)}</strong><span class="badge">자료 필요</span></div><p class="bc01-required-work">${esc(r.work)}</p></article>`).join('')}</div>`;
  }
  function bc01PendingReviews(reviews) {
    return `<details class="bc01-pending-reviews"><summary>기존 검토 항목 · ${reviews.length}건 · 원본 상태 유지</summary>${reviews.map(r=>`<article class="bc01-pending-review" data-review-source="${esc(r.id)}"><h5>${esc(r.title)}</h5><p><span class="badge">${esc(r.status)}</span> <code>${esc(r.id)}</code></p><p>${esc(r.observation)}</p><p><strong>다음 확인</strong> · ${esc(r.next_check)}</p><div class="bc01-source-actions">${r.links.filter(l=>validDoc(l.path)).map(l=>docButton(l.label,l.path)).join('')}</div></article>`).join('')}<p class="muted">보존 대장의 요구 사항입니다. 시뮬레이터·행동 시험과 실제 PLC 변경은 현재 중단 범위를 유지합니다.</p></details>`;
  }
  function bc01EvidenceSources(links) {
    if(!links.length)return '<p class="muted">이 경로에 직접 배정된 원본 래더 참조는 없습니다. 도면과 현재 입력 전달 위치를 별도로 대조합니다.</p>';
    return `<details class="bc01-check-sources"><summary>비교할 원본 · ${links.length}개 참조</summary><div class="bc01-source-actions">${links.filter(l=>validDoc(l.path)).map(l=>docButton(l.label,l.path)).join('')}</div></details>`;
  }
  function bc01CompletionWorkspace(item,spec,schema,drawing) {
    const plan=schema.evidence_plan, circuit=drawing.circuit, tasks=bc01CompletionTasks(item);
    const current=tasks.find(t=>t.id===state.bc01Check) || tasks[0];
    let body=`<div class="bc01-completion-status"><strong>현장 확인 준비 · 확인 대기</strong><p>현재 CPU·실물·복구 증거는 아직 확인되지 않았습니다. 아래 자료 요청과 원본 비교를 관찰 결과로 자동 판정하지 않습니다.</p></div><div class="bc01-print-actions"><button type="button" data-bc01-proof-preview>현재 작업지 인쇄 미리보기</button><p class="muted">선택한 작업의 자료 요청·원본·미확정 사항을 펼쳐 인쇄합니다. PDF 저장은 브라우저 인쇄 창에서 선택합니다.</p></div>`;
    if(tasks.length)body+=`<nav class="bc01-check-tabs" aria-label="BC01 확인 작업 선택">${tasks.map(t=>`<button type="button" data-bc01-check="${esc(t.id)}" aria-pressed="${current.id===t.id}">${esc(t.title)}</button>`).join('')}</nav>`;
    if(item==='cpu') {
      const evidence=current.evidence;
      body+=`<section class="bc01-evidence-task" data-check-task="${current.id}"><h4>${esc(current.title)} · 현행 자료와 대조</h4><p class="bc01-explanation">${current.id==='baseline'?'비교할 백업·현재 프로젝트·CPU와 설비를 먼저 식별합니다.':'필요한 자료를 모은 뒤 해당 신호의 현재 호출·다른 쓰기·관찰 시각을 원본과 비교합니다.'}</p><h5>필요한 자료 · ${evidence.requirements.length}항목</h5>${bc01EvidenceRequirements(evidence.requirements)}`;
      if(current.id==='baseline')body+=`<details><summary>보존 제어 명세의 미확정 ${spec.pending.length}항목</summary><ul>${spec.pending.map(p=>'<li>'+esc(p)+'</li>').join('')}</ul></details>`;
      else body+=`<details><summary>요청·출력·처리 응답의 백업 참조</summary>${table(['역할','원본 신호·백업 주소','원본 위치'],schema.signals.map(s=>[esc(({requests:'운전 요청',outputs:'최종 PLC 출력',responses:'처리된 응답'})[s.role] || s.role),'<code>'+esc(s.name)+'</code><br>'+esc(s.addresses.join(' / ') || '주소·현재 DB 대응 추가 확인'),s.refs.map(r=>docButton('LAD '+r.network+' · ORef '+r.oref,'networks/network-'+r.network+'.html')).join(' ')]))}<p class="muted">원시 I/O→처리 Inputs 전달·반전은 미확정이며 HMI 저장 태그와 임의로 연결하지 않습니다.</p></details>`;
      body+=bc01EvidenceSources(evidence.source_links || [{label:'원본 불일치 대장',path:'registers/source-conflict-review.csv'},{label:'실물 대응 작업지',path:'priority-guides/P01.html'}])+bc01PendingReviews(evidence.reviews)+'</section>';
    } else if(item==='field') {
      body+=`<section class="bc01-evidence-task" data-check-task="${current.id}"><h4>${esc(current.title)} · 실물·접속 확인</h4>`;
      if(current.id==='baseline')body+=bc01EvidenceRequirements(plan.preflight.requirements.filter(r=>r.owner==='현장·설비 자료'))+`<h5>현장 응답·제작사 자료 · 기존 요구 ${plan.steps.find(s=>s.step_id==='response').requirements.length}항목</h5><details><summary>구동기·센서·입력 전달 자료 요청 보기</summary>${bc01EvidenceRequirements(plan.steps.find(s=>s.step_id==='response').requirements)}</details>`+bc01EvidenceSources([{label:'실물 대응 작업지',path:'priority-guides/P01.html'},{label:'회로·단자 전체 근거',path:'circuit-guides/BC01.html'},{label:'시공·케이블 원본 근거',path:'construction-guides/BC01.html'}]);
      else {
        const path=current.path;
        body+=`<div class="status-row"><span class="badge">보존 도면 ${esc(path.drawing)} · ${esc(path.backup)}</span><span>FG${esc(path.fg)} · PDF${pdfPage(path.fg)}</span></div><article class="bc01-evidence-requirement"><h5>현장에서 확인할 항목</h5><p class="bc01-required-work">${esc(path.check)}</p></article><article class="bc01-evidence-requirement"><h5>도착점과 미확정 경계</h5><p>${esc(path.destination)}</p></article><details><summary>비교할 도면상 경로</summary><ol class="bc01-path">${path.nodes.map(n=>'<li>'+esc(n)+'</li>').join('')}</ol></details><div class="bc01-source-actions"><button type="button" data-drawing="oem-${esc(path.fg)}">해당 도면 크게 확인</button><button type="button" data-bc01-jump="circuits/${esc(current.id)}">전기 전달 경로 전체 확인</button></div>`+bc01EvidenceSources(path.native_symbol_references.map(r=>({label:'LAD '+r.network+' · ORef '+r.uid,path:'networks/network-'+r.network+'.html'})));
      }
      body+=`<details><summary>회로 작업지의 확인 대기 · ${circuit.pending.length}항목</summary><ul>${circuit.pending.map(p=>'<li>'+esc(p)+'</li>').join('')}</ul></details>${drawing.warnings.map(w=>'<div class="notice">기존 기록상 불일치 · '+esc(w)+'</div>').join('')}</section>`;
    } else {
      const evidence=plan.steps.find(s=>s.step_id==='recovery'), step=schema.steps.find(s=>s.id==='recovery');
      body+=`<section class="bc01-evidence-task" data-check-task="recovery"><h4>복구 결과를 판정할 증거</h4><p class="bc01-explanation">리셋·새 요청·출력·실제 운전 응답의 증거를 따로 남깁니다. 관찰하지 않은 값과 원인 후보는 확인 결과로 바꾸지 않습니다.</p><ol class="repair-steps">${[['관찰·시각 기록',step.observe],['원본과 비교',step.compare],['복구 판단의 경계',step.next]].map(([title,text])=>'<li><h5>'+esc(title)+'</h5><p>'+esc(text)+'</p></li>').join('')}</ol><h5>필요한 자료 · ${evidence.requirements.length}항목</h5>${bc01EvidenceRequirements(evidence.requirements)}<details><summary>복구 증거를 빠짐없이 확인</summary><ol class="bc01-path">${['최초 알람·원인 입력·관찰 기준 시각','원인 해소 및 실물/처리 신호의 정상화 근거','알람 래치 해제와 기동 허가의 확인','승인된 새 요청·Q0.0·DI1·실제 운전 응답','연동 영향·재발 여부·조치 및 후속 확인'].map(s=>'<li>'+esc(s)+'</li>').join('')}</ol></details>${bc01EvidenceSources(evidence.source_links)}${bc01PendingReviews(evidence.reviews)}</section>`;
    }
    return body+`<section class="bc01-proof-guide"><h4>근거를 남긴 뒤 대조합니다</h4><p>자료명·개정/버전·신호/단자·관찰값·시각·사진/화면 위치와 남은 차이를 기존 수리 기록에 남깁니다. 이 작업판은 자료 안내이며 입력값을 채우거나 확인 완료로 전환하지 않습니다.</p>${button('BC01 수리 관찰 기록','repair-record')} ${docButton('BC01 미완료 항목·완료 기준','requirements-audit.html#open-P01')}</section>`;
  }
  function closeBC01ProofPreview() {
    const dialog=document.getElementById('bc01-proof-preview');
    if(dialog) {dialog.close();dialog.remove();}
    document.body.classList.remove('bc01-proof-printing');
  }
  function openBC01ProofPreview() {
    if(state.view!=='manual' || state.selected!=='P01' || state.bc01Section!=='completion')return;
    const task=document.querySelector('.bc01-evidence-task'), status=document.querySelector('.bc01-completion-status');
    if(!task || !status)return;
    closeBC01ProofPreview();
    const dialog=document.createElement('dialog');
    dialog.id='bc01-proof-preview';dialog.className='bc01-proof-preview';
    dialog.setAttribute('aria-labelledby','bc01-proof-title');
    const printStyle=document.createElement('style');
    printStyle.textContent='@page {size:A4;margin:14mm 12mm;@bottom-center{content:"BC01 · 확인 대기  |  " counter(page) " / " counter(pages);font:9pt system-ui,sans-serif;color:#52677a}}';
    dialog.innerHTML='<div class="bc01-proof-toolbar"><strong>인쇄 미리보기 · 선택한 BC01 작업</strong><div><button type="button" data-bc01-proof-print>인쇄 / PDF 저장</button><button type="button" data-bc01-proof-close>닫기</button></div></div><article class="bc01-proof-paper"><header><p>GME / BC01 · 현장 자료 요청·확인 작업지</p><h1 id="bc01-proof-title"></h1><p class="bc01-proof-baseline">보존 백업 GME_20250506.zap18 기준 · 현재 CPU·실물·복구 미확인</p></header></article>';
    dialog.querySelector('#bc01-proof-title').textContent=document.getElementById('bc01-content-title').textContent+' / '+task.querySelector('h4').textContent;
    const paper=dialog.querySelector('.bc01-proof-paper');
    paper.append(status.cloneNode(true),task.cloneNode(true));
    paper.querySelectorAll('details').forEach(d=>d.open=true);
    paper.querySelectorAll('button').forEach(b=> {
      let path=b.dataset.doc;
      if(b.dataset.drawing) {
        const sheet=drawingMap.get('P01').sheets.find(s=>s.id===b.dataset.drawing);
        path=sheet?sheet.source+(sheet.page?'#page='+sheet.page:''):'';
      }
      if(path && validDoc(path)) {
        const a=document.createElement('a');a.className='bc01-proof-source';
        a.href=new URL(path,document.baseURI).href;a.target='_blank';a.rel='noopener';
        a.textContent=b.textContent+' · '+path;b.replaceWith(a);
      } else b.remove();
    });
    const notes=document.createElement('section');notes.className='bc01-proof-notes';
    notes.innerHTML='<h2>자료 수집 메모 · 자동 저장 없음</h2><p>자료명·개정/버전, 확인자·일시, 사진/화면 위치를 남깁니다. 실제 관찰은 기존 수리 기록에 별도로 입력합니다.</p>';
    ['자료명·개정/버전','확인자·일시·시간대','신호/단자·관찰값·사진/화면 위치','원본과의 차이·미확정 사항·후속 확인'].forEach(label=> {
      const row=document.createElement('div');row.className='bc01-proof-note-row';
      const title=document.createElement('strong');title.textContent=label;
      row.append(title,document.createElement('span'));notes.append(row);
    });
    const boundary=document.createElement('section');boundary.className='bc01-proof-context';
    const heading=document.createElement('h2');heading.textContent='설비·회로의 미확정 경계';boundary.append(heading);
    document.querySelectorAll('.bc01-evidence .panel:last-child p, .bc01-evidence .panel:last-child .notice').forEach(n=>boundary.append(n.cloneNode(true)));
    paper.append(boundary,notes);
    const footer=document.createElement('p');footer.className='bc01-proof-boundary';
    footer.textContent='자료 수집은 원인 확정·수리 완료·재기동 승인 판정이 아닙니다. 시뮬레이터 실행·실제 PLC·현장 설정·보호값 변경은 수행하지 않습니다.';
    paper.append(footer);
    dialog.addEventListener('close',()=>{document.body.classList.remove('bc01-proof-printing');document.querySelector('[data-bc01-proof-preview]')?.focus({preventScroll:true});dialog.remove();});
    dialog.append(printStyle);document.body.append(dialog);dialog.showModal();document.body.classList.add('bc01-proof-printing');
  }
  function bc01NormalizeMedia(group,photo) {
    const media=data.bc01_standard.media_evidence;
    state.bc01MediaGroup=media.groups.some(g=>g.id===group)?group:media.groups[0].id;
    const photos=media.photos.filter(p=>p.group===state.bc01MediaGroup);
    state.bc01Photo=photos.find(p=>p.id===photo)?.id || photos[0].id;
  }
  function bc01MediaBody() {
    const media=data.bc01_standard.media_evidence;
    bc01NormalizeMedia(state.bc01MediaGroup,state.bc01Photo);
    const photos=media.photos.filter(p=>p.group===state.bc01MediaGroup), photo=photos.find(p=>p.id===state.bc01Photo), ref=media.references[state.bc01MediaGroup];
    const pathButtons=ids=>ids.map(i=>`<button type="button" data-bc01-jump="circuits/path-${i}">${esc(drawingMap.get('P01').circuit.paths[i].signal)} · 도면 경로</button>`).join('');
    const kinds={photograph:'현장 사진 참고',historical_photograph:'이전 등록 사진',test_graphic:'TEST 그래픽',technical_drawing_image:'부품 도면 이미지',unidentified_3d:'동일성 미확인 3D'};
    return `<p class="bc01-lead">부품별 자료 선택 → 보이는 내용 → 관련 도면 → 추가 확인</p><p>SEJIN의 BC-01(벨트) 카드 자료12장을 분류했습니다. 사진 원본은 SEJIN에서 열며, 현재 실물 동일성·촬영 시점·고장·복구 상태는 확인 전입니다.</p><div class="bc01-media-groups" role="group" aria-label="사진 자료 종류">${media.groups.map(g=>`<button type="button" data-bc01-media-group="${g.id}" aria-pressed="${g.id===state.bc01MediaGroup}"><strong>${esc(g.title)}</strong><small>${media.photos.filter(p=>p.group===g.id).length}개 자료</small></button>`).join('')}</div><div class="bc01-media-cards" role="group" aria-label="선택 종류의 사진 자료">${photos.map(p=>`<button type="button" data-bc01-photo="${p.id}" aria-pressed="${p.id===photo.id}"><span class="badge">자료 ${String(p.source_order).padStart(2,'0')} · ${esc(kinds[p.kind])}</span><strong>${esc(p.title)}</strong></button>`).join('')}</div><article class="bc01-media-detail" aria-label="선택 사진 근거"><p class="eyebrow">선택한 자료 ${String(photo.source_order).padStart(2,'0')} / 12</p><h4>${esc(photo.title)}</h4><span class="badge">${esc(kinds[photo.kind])}</span><section><h5>사진·이미지에서 보이는 내용</h5><p>${esc(photo.observation)}</p><a class="button-link" href="${esc(photo.original_url)}" target="_blank" rel="noopener noreferrer">SEJIN 원본 이미지 열기 ↗</a><p class="muted">외부 원본 링크 · 사진 파일을 복제하거나 원본 등록을 변경하지 않습니다.</p></section><section><h5>부품·도면을 비교할 위치</h5><p>${esc(ref.description)}</p><div class="bc01-source-actions">${ref.documents.map(d=>docButton(d[0],d[1])).join('')}${pathButtons(ref.paths)}</div></section><section class="notice"><h5>추가 확인</h5><p>${esc(photo.pending)}</p></section>${state.bc01MediaGroup==='chain' || photo.kind==='technical_drawing_image'?`<div class="notice info"><strong>스프로킷 사양·개정 경계</strong><p>${esc(media.part_revision_boundary)}</p></div>`:''}</article><details class="bc01-media-missing"><summary>추가로 필요한 명판·보호장치 사진 3종</summary>${media.missing.map(m=>`<article><h4>${esc(m.title)}</h4><p>${esc(m.text)}</p><div class="bc01-source-actions">${pathButtons(m.paths)}</div></article>`).join('')}</details><p class="muted">확인 기준: 2026-10-11 읽기 전용 원본 화면·이미지 관찰. 등록 태그를 정상·고장·복구 판정으로 사용하지 않습니다.</p>`;
  }
  function bc01SourceNavigation() {
    const source=data.bc01_standard.source_navigation;
    return `<section class="bc01-source-navigation" aria-label="SEJIN 원본 자료"><div><h4>현장 자료는 SEJIN 원본에서</h4><p>사양·사진·작업이력은 SEJIN에서 관리하고, 여기서는 PLC·도면 근거와 점검 순서를 확인합니다.</p><p class="muted">열린 카드에서 작업이력·사진 탭을 선택하세요. 과거 등록 사양과 현재 실물은 구분해 확인합니다.</p></div><a class="bc01-source-link" href="${esc(source.url)}" target="_blank" rel="noopener noreferrer">SEJIN BC01 원본·작업이력 보기 ↗</a></section>`;
  }
  function bc01DiagnosticMap(schema,circuit) {
    const output=schema.signals.find(s=>s.name==='Start BC01'),response=schema.signals.find(s=>s.name==='Inputs.BC01 run');
    const raw=bc01Items('io').find(i=>i.role==='물리 입력' && i.raw['백업 주소'].toUpperCase()==='%I0.0');
    const start=circuit.paths[0],feedback=circuit.paths[1];
    const refs=items=>items.map(r=>docButton('LAD '+r.network+' · ORef '+(r.oref || r.uid),'networks/network-'+r.network+'.html')).join('');
    const cards=[
      {id:'plc-output',title:'PLC 최종 출력',tag:output.name+' · '+output.addresses.join(' / '),where:'현재 CPU에서 출력 비트와 수집 시각을 확인할 위치입니다.',known:'백업에서 식별한 출력 주소입니다. 출력 비트와 현장 기동 입력을 따로 관찰합니다.',pending:'현재 CPU 주소·값·호출 순서·다른 쓰기는 확인 전입니다.',actions:'<button type="button" data-bc01-jump="control/output">출력 허가 조건</button>',sources:refs(output.refs)},
      {id:'field-start',title:'현장 기동 전달',tag:'FG19 / PDF20 · FG18 / PDF19',where:'보존 도면상 위치: '+start.nodes.slice(2).join(' → '),known:'보존 도면의 도착점: '+start.destination,pending:'현재 ABB 모델·단자·배선은 확인 전입니다. Q0.0=1만으로 DI1 전달을 확인할 수 없습니다.',actions:'<button type="button" data-bc01-jump="circuits/path-0">단자·접점 경로</button>',sources:''},
      {id:'raw-response',title:'원시 운전 응답',tag:raw.raw['원본 심볼']+' · '+raw.raw['백업 주소'].toUpperCase(),where:'보존 도면상 위치: '+feedback.nodes.join(' → '),known:'RUNNING 출력과 PLC 입력의 관찰값·시각을 따로 기록합니다.',pending:'현재 릴레이 출력 기능·정상 극성·배선은 확인 전입니다.',actions:'<button type="button" data-bc01-jump="circuits/path-1">운전 응답 회로</button><button type="button" data-bc01-jump="io/'+raw.id+'">원시 I/O 근거</button>',sources:refs(feedback.native_symbol_references)},
      {id:'processed-response',title:'처리된 운전 응답',tag:response.name+' · 주소 추가 확인',where:'처리 신호와 운전 응답 고장 래치를 따로 확인할 위치입니다.',known:'백업 알람의 입력 참조이며, 원시 I0.0에서 이 신호까지의 전달은 확인 전입니다.',pending:'원시 입력과 같은 값으로 간주하지 않습니다. 래치 해제·새 요청·실제 복구도 별도로 확인합니다.',actions:'<button type="button" data-bc01-jump="alarms/alarm-0">발생·리셋·재기동</button>'+docButton('처리 신호·다른 쓰기','signal-guides/BC01.html'),sources:refs(response.refs)}
    ];
    return `<section class="bc01-diagnostic-map" aria-labelledby="bc01-observation-title"><h4 id="bc01-observation-title">관찰 위치 길찾기</h4><p>각 구간의 값·시각·수집 위치를 따로 기록하고, 차이가 시작되는 구간의 근거를 여세요. 아래 네 구역은 비교 위치이며 현재 실행 순서를 뜻하지 않습니다.</p><p class="muted">도면 단자는 보존 자료의 표기입니다. 현재 ABB 모델·단자·배선과 정상 극성은 확인 전입니다.</p><div class="bc01-observation-grid">${cards.map((c,i)=>`<article class="bc01-observation-card" data-bc01-observation="${c.id}"><header><span class="bc01-observation-number">${i+1}</span><h5>${esc(c.title)}</h5></header><code>${esc(c.tag)}</code><p class="bc01-observation-location">${esc(c.where)}</p><p>${esc(c.known)}</p><details><summary>추가로 확인할 경계</summary><p>${esc(c.pending)}</p></details><div class="inline-actions">${c.actions}</div>${c.sources?'<details><summary>백업 원본 참조</summary><div class="inline-actions">'+c.sources+'</div></details>':''}</article>`).join('')}</div><div class="notice">미확정 전달: %I0.0 → Inputs.BC01 run. 값·시각을 각각 관찰한 뒤 전달 위치와 현재 호출 근거를 확보합니다.</div></section>`;
  }
  function bc01JumpButton(label,section,item,extra='') {
    return `<button type="button" data-bc01-jump="${esc(section+'/'+item)}" ${extra}>${esc(label)}</button>`;
  }
  function bc01Navigate(section,item,options={}) {
    if(!bc01Sections.some(s=>s[0]===section) || !bc01Items(section).some(i=>i.id===item))return false;
    state.bc01Section=section;state.bc01Item=item;
    if(section==='alarms')state.bc01AlarmStep=['set','reset','restart'].includes(options.alarmStep)?options.alarmStep:'set';
    if(section==='completion')state.bc01Check=bc01CompletionTasks(item).find(t=>t.id===options.check)?.id || bc01CompletionTasks(item)[0]?.id || '';
    if(section==='overview' && item==='media')bc01NormalizeMedia(options.media,options.photo);
    if(section==='control' && item==='request')state.bc01Relation=data.bc01_standard.relationships.nodes.find(n=>n.id===options.relation)?.id || 'request';
    route('manual');document.getElementById('bc01-content-title')?.focus({preventScroll:true});document.querySelector('.bc01-content')?.scrollIntoView({block:'start'});return true;
  }
  function bc01RelationshipBody() {
    const relation=data.bc01_standard.relationships, spec=data.bc01_standard.specification;
    const current=relation.nodes.find(n=>n.id===state.bc01Relation) || relation.nodes[0];
    const rules=spec.direct_rules.filter(r=>current.rule_ids.includes(r.rule_id));
    const groups=[['request','운전 요청·기억'],['output','출력·감시'],['alarm','알람 기억·해제']];
    let detail=bc01RuleCards(rules);
    if(current.id==='timer') {const t=data.bc01_standard.alarm.timers[0];detail=`<article class="bc01-rule"><h5>Tag_51 · ${esc(t.gate)} · ${esc(staticCondition(t.preset))}</h5><p>운전 응답 고장과 인버터 이상 감시가 공유하는 원본 타이머 비트입니다. 트립와이어 알람에는 이 비트의 직접 접점이 없습니다.</p>${bc01ConditionPanel(t.condition)}${bc01SourceButton('타이머 원본 위치',t.network,'part',t.uid)}</article>`;}
    return `<section class="bc01-relationships" aria-labelledby="bc01-relationship-title"><h4 id="bc01-relationship-title">기동·정지·복구 근거 관계도</h4><p>관계 카드를 선택하면 실제 읽기·쓰기 조건과 원본이 나타납니다. 아래 배치는 실행 순서나 현재 상태를 표시하지 않습니다.</p><div class="bc01-relation-map">${groups.map(([id,title])=>`<section><h5>${esc(title)}</h5>${relation.nodes.filter(n=>n.group===id).map(n=>`<button type="button" data-bc01-relation="${esc(n.id)}" aria-pressed="${n.id===current.id}"><strong>${esc(n.title)}</strong><span>${esc(n.caption)}</span></button>`).join('')}</section>`).join('')}</div><details class="bc01-relation-links"><summary>원본에서 확인된 연결 ${relation.edges.length}개</summary>${table(['읽는 신호 → 쓰는 대상','관계·추가 확인','원본 위치'],relation.edges.map(e=>['<code>'+esc(e.from.join(' / '))+' → '+esc(e.to)+'</code>',esc(e.note),e.rules.map(key=>{const [network,uid]=key.split(':');return bc01SourceButton('LAD '+network+' · UID '+uid,Number(network),'part',uid);}).join(' ')]))}<p>연결 목록은 접점 읽기와 코일 쓰기의 참조입니다. 각 AND/OR·NOT 조건은 선택한 원본 조건에서 확인합니다.</p></details><article class="bc01-relation-detail" data-relation-detail="${esc(current.id)}"><h5>${esc(current.title)} · 선택한 근거</h5><p>${esc(current.note)}</p>${detail}</article><div class="notice">원시 I0.0/I0.1/I6.2 → 처리 Inputs 전달은 확인 전입니다. 리셋 → 운전 요청 Set 또는 실제 재기동으로 연결하지 않습니다.</div></section>`;
  }
  function bc01RemainingRepairCards(step) {
    const cards=data.bc01_standard.repair_navigation[step.id];if(!cards)return '';
    return `<section class="bc01-diagnostic-map" aria-labelledby="bc01-observation-title"><h4 id="bc01-observation-title">${esc(step.title)} · 관찰 위치 길찾기</h4><p>값·변화 시각·수집 위치를 각각 기록하고 비교할 근거를 선택하세요. 표시 신호와 조건은 보존 자료 기준입니다.</p><div class="bc01-observation-grid">${cards.map((c,i)=>`<article class="bc01-observation-card" data-bc01-observation="${esc(step.id+'-'+c.id)}"><header><span class="bc01-observation-number">${i+1}</span><h5>${esc(c.title)}</h5></header><code>${esc(c.signals)}</code><p class="bc01-observation-location">${esc(c.observe)}</p><p>${esc(c.compare)}</p><details><summary>추가로 확인할 경계</summary><p>${esc(c.pending)}</p></details><div class="inline-actions">${c.targets.map(t=>bc01JumpButton(t.label,t.section,t.item,t.alarmStep?'data-bc01-jump-alarm="'+esc(t.alarmStep)+'"':'')).join('')}</div><details><summary>백업 원본 위치</summary><div class="inline-actions">${c.rules.map(key=>{const [network,uid]=key.split(':');return bc01SourceButton('LAD '+network+' · UID '+uid,Number(network),'part',uid);}).join('')}</div></details></article>`).join('')}</div><p class="muted">현재 CPU·정상 극성·현행 ABB 접속·원시→처리 전달·실제 복구는 확인 전입니다. 이 안내는 관찰값이나 고장 판정을 생성하지 않습니다.</p></section>`;
  }
  function bc01InverterComparison() {
    return `<section class="bc01-inverter-comparison"><h4>보존 도면과 현재 ABB의 대응 확인</h4><p>현재 제작사 ABB는 2026-10-11 사용자 확인입니다. 모델·정격·단자는 보존 도면과 현재 실물을 나누어 봅니다.</p><div class="bc01-comparison-grid">${data.bc01_standard.inverter_comparison.map(c=>`<article><h5>${esc(c.aspect)}</h5><dl><dt>보존 자료</dt><dd>${esc(c.saved)}</dd><dt>현재 확인 상태</dt><dd>${esc(c.current)}</dd><dt>대조에 필요한 자료</dt><dd>${esc(c.needed)}</dd></dl><div class="inline-actions">${c.targets.map(t=>bc01JumpButton(t.label,t.section,t.item)).join('')}</div></article>`).join('')}</div><p class="muted">구버전 미쓰비시·과거 교체 이력은 SEJIN 원본에서 해당 시점의 기록으로 확인합니다. 과거 정격·단자·보호값을 현재 장착품으로 적용하지 않습니다.</p></section>`;
  }
  let bc01SearchCollecting=false,bc01SearchIndex=null,bc01SearchLimit=20;
  function bc01SearchNormalize(value) {return String(value || '').normalize('NFKC').toLowerCase().replace(/[\s%_.:\-/()]+/g,'');}
  function bc01BuildSearchIndex() {
    if(bc01SearchIndex)return bc01SearchIndex;
    const saved={...state},records=[];bc01SearchCollecting=true;
    try {
      for(const [section,sectionTitle] of bc01Sections)for(const item of bc01Items(section)) {
        let choices=[{}];
        if(section==='alarms')choices=['set','reset','restart'].map(alarmStep=>({alarmStep,label:({set:'발생 조건',reset:'리셋 조건',restart:'재기동 확인'})[alarmStep]}));
        if(section==='overview' && item.id==='media')choices=data.bc01_standard.media_evidence.photos.map(p=>({media:p.group,photo:p.id,label:p.title}));
        if(section==='completion' && ['cpu','field'].includes(item.id))choices=bc01CompletionTasks(item.id).map(t=>({check:t.id,label:t.title}));
        if(section==='control' && item.id==='request')choices=data.bc01_standard.relationships.nodes.map(n=>({relation:n.id,label:n.title}));
        for(const choice of choices) {
          state.bc01Section=section;state.bc01Item=item.id;state.bc01AlarmStep=choice.alarmStep || 'set';state.bc01Check=choice.check || '';state.bc01Relation=choice.relation || 'request';
          if(choice.photo)bc01NormalizeMedia(choice.media,choice.photo);
          const template=document.createElement('template');template.innerHTML=renderBC01Manual();
          const content=template.content.querySelector('.bc01-content');
          content.querySelectorAll('.bc01-item-nav,.bc01-source-navigation,.bc01-check-tabs,.bc01-media-groups,.bc01-media-cards').forEach(n=>n.remove());
          if(choice.relation){const selected=content.querySelector('.bc01-relation-detail');content.replaceChildren(selected);}
          const walker=document.createTreeWalker(content,NodeFilter.SHOW_TEXT),pieces=[];while(walker.nextNode())pieces.push(walker.currentNode.textContent);const refs=new Set();content.querySelectorAll('[data-doc]').forEach(button=>{const match=(button.dataset.doc || '').match(/^networks\/network-(\d+)\.html#bc01-part-(\d+)$/);if(match)refs.add('원본 링크 LAD '+match[1]+' UID '+match[2]);});pieces.push(...refs);const text=pieces.join(' ').replace(/\s+/g,' ').trim();
          records.push({section,item:item.id,sectionTitle,title:item.title,choice,text,normalized:bc01SearchNormalize(text)});
        }
      }
    } finally {Object.assign(state,saved);bc01SearchCollecting=false;}
    bc01SearchIndex=records;return records;
  }
  function bc01SearchSnippet(record,query) {
    const terms=query.split(/[\s,]+/).map(bc01SearchNormalize).filter(Boolean),positions=[];let normalized='',offset=0;
    for(const ch of record.text){const part=bc01SearchNormalize(ch);normalized+=part;for(let i=0;i<part.length;i++)positions.push(offset);offset+=ch.length;}
    const term=terms.find(t=>normalized.includes(t)) || '',match=term?normalized.indexOf(term):-1;
    const position=match>=0?positions[match]:0,end=match>=0?positions[match+term.length-1]+1:0;
    const start=Math.max(0,position-48),finish=Math.max(start+200,end+25),snippet=record.text.slice(start,finish),at=match>=0?position-start:-1;
    return (start?'…':'')+(at<0?esc(snippet):esc(snippet.slice(0,at))+'<mark>'+esc(snippet.slice(at,end-start))+'</mark>'+esc(snippet.slice(end-start)))+(finish<record.text.length?'…':'');
  }
  function bc01SearchResultsHTML(matches,query) {
    const groups=new Map();for(const r of matches.slice(0,bc01SearchLimit)){const key=r.section+'/'+r.item;if(!groups.has(key))groups.set(key,[]);groups.get(key).push(r);}
    return Array.from(groups.values()).map(records=>`<section class="bc01-search-group"><h4>${esc(records[0].sectionTitle+' › '+records[0].title)}</h4><div>${records.map(r=>`<button type="button" data-bc01-search-result="${r.index}"><strong>${esc(r.choice.label || r.title)}</strong><span>${bc01SearchSnippet(r,query)}</span></button>`).join('')}</div></section>`).join('');
  }
  function bc01SearchPanel() {
    if(bc01SearchCollecting)return '';
    const query=state.bc01Find || '',terms=query.split(/[\s,]+/).map(bc01SearchNormalize).filter(Boolean);
    const index=query?bc01BuildSearchIndex():[],matches=index.map((r,i)=>({...r,index:i})).filter(r=>terms.length && terms.every(t=>r.normalized.includes(t)));
    return `<section class="bc01-manual-search" aria-label="BC01 매뉴얼 내부 검색"><form data-bc01-search><label for="bc01-find">BC01 매뉴얼 내부 검색</label><div><input id="bc01-find" type="search" maxlength="160" value="${esc(query)}" placeholder="태그·주소·알람·본문·LAD/UID"><button type="submit">찾기</button><button type="button" data-bc01-find-clear>지우기</button></div></form><p class="muted">36개 항목과 알람 단계·사진·현장 작업지의 세부 내용을 찾습니다. 예: Q0.0, Tag_51, S5T#2S, 리셋, ABB</p>${query?`<details open class="bc01-search-results"><summary>검색 결과 ${matches.length}개 · ${esc(query)}</summary><div aria-live="polite">${matches.length?bc01SearchResultsHTML(matches,query):'<p>일치하는 내용이 없습니다. 원본 태그·주소 또는 짧은 단어로 다시 찾아보세요.</p>'}</div>${matches.length>bc01SearchLimit?'<button type="button" data-bc01-find-more>검색 결과 더 보기</button>':''}<p class="muted">검색은 문서 탐색이며 현재 PLC값·운전 결과를 조회하거나 계산하지 않습니다.</p></details>`:''}</section>`;
  }

  function renderBC01Manual() {
    const standard=data.bc01_standard;
    if(!standard)return panel('BC01 표준 자료','<p>자료를 다시 불러와 주세요.</p>');
    const spec=standard.specification, alarm=standard.alarm, schema=repairRecordMap.get('P01'), drawing=drawingMap.get('P01'), circuit=drawing.circuit;
    const items=bc01Items(state.bc01Section), current=items.find(i=>i.id===state.bc01Item) || items[0];
    const links=paths=>`<div class="bc01-source-actions">${paths.filter(p=>validDoc(p[1])).map(p=>docButton(p[0],p[1])).join('')}</div>`;
    let body='', sources=[];
    if(state.bc01Section==='overview') {
      if(current.id==='identity')body=`<p class="bc01-lead">${esc(spec.role)}</p>${table(['구분','자료에서 확인한 내용'],[['현장 카드 명칭',esc(selection().p.name)],['PLC 참조 태그','BC01'],['백업 설비 이름',esc(spec.name)],['계통·역할',esc(spec.group)+' · '+esc(spec.kind)],['모터·구동기',esc(circuit.equipment)],['설비 동일성','태그명 일치 · 실물/명판/위치 확인 전']])}<div class="notice">${esc(circuit.distinction)}</div>`;
      else if(current.id==='baseline')body=`<p>매뉴얼의 조건과 주소는 아래 보존 자료를 기준으로 합니다. 현재 CPU·준공도·현장 상태와의 일치 여부는 별도 확인합니다.</p>${table(['자료','식별 기준·한계'],[['PLC','보존 백업/복원 XML · 현재 프로젝트와 비교 필요'],['OEM 전기','Electrical_Rev2.pdf · FG18/19 = PDF19/20 · 개정란은 원본에서 확인'],['시공·케이블','Electrical_Can_Decoating_20241118.pdf · FOR APPROVAL · 24.11.11 first draft design'],['P&ID','PID_1684n002I.pdf · 전체 공정 참고'],['HMI','보존된 DDE 태그 설정 · 현재 표시/요청/쓰기 대응 미확정']])}<details><summary>사용한 대장과 SHA256</summary>${table(['입력 대장','SHA256'],Object.entries(standard.source_hashes).map(([path,hash])=>[esc(path),'<code>'+esc(hash)+'</code>']))}</details>`;
      else if(current.id==='media')body=bc01MediaBody();
      else body=`<div class="bc01-status-cards"><article><strong>원본·정적 근거</strong><p>보존 자료에 연결</p></article><article><strong>현재 PLC·TIA</strong><p>미검증</p></article><article><strong>실물·현장 복구</strong><p>미확인</p></article></div><ul>${spec.pending.map(p=>'<li>'+esc(p)+'</li>').join('')}</ul><div class="notice">문서·UI 표준화와 실제 수리 완료를 구분합니다. 다른 설비로의 확대는 사용자 요청으로 보류합니다.</div>`;
      sources=[['기존 설비 자료','devices/BC01.html'],['실물 대응 작업지','priority-guides/P01.html'],['현행 백업 확인','requirements-audit.html#open-P01']];
    } else if(state.bc01Section==='io') {
      const raw=current.raw, hmi=current.role==='HMI 저장 태그';
      body=`<span class="badge">${esc(current.role)}</span>${table(['항목','원본 설정'],hmi?[['HMI 태그',esc(raw['HMI 태그'])],['설정 주소',esc(raw['설정 주소'])],['Access Name',esc(raw['Access Name'])],['내부 태그 ID',esc(raw['내부 ID'])]]:[['심볼',esc(raw['원본 심볼'])],['백업 주소',esc(raw['백업 주소'].toUpperCase())],['자료형',esc(raw['자료형'])],['원본 설명',esc(raw['설명'] || '원본 설명 없음')],['심볼 문서 ID',esc(raw['문서 ID'])]])}<div class="notice info">현재값·정상 극성·현재 CPU 주소는 미취득/미확정입니다. HMI 저장 주소, 원시 I/O와 처리된 Inputs를 임의로 같은 신호로 연결하지 않습니다.</div>`;
      const path=circuit.paths.find(p=>p.backup.split(' / ')[0].toUpperCase()===(raw['백업 주소'] || '').toUpperCase());
      if(path)body+=`<h4>연관 도면의 전달 경계</h4><p>${esc(path.destination)}</p><p>${esc(path.check)}</p>`;
      body+=`<details><summary>별도로 식별한 처리 응답·요청</summary>${table(['역할','원본 이름','참조'],schema.signals.map(s=>[esc(s.role),'<code>'+esc(s.name)+'</code>',s.refs.map(r=>docButton('LAD '+r.network+' · ORef '+r.oref,'networks/network-'+r.network+'.html')).join(' ')]))}</details>`;
      sources=[['원시/처리 신호·복수 쓰기','signal-guides/BC01.html'],['HMI 전달 근거','hmi-transfer.html#profile-P01'],['전체 I/O·주소','devices/BC01.html']];
    } else if(state.bc01Section==='control') {
      let rules=spec.direct_rules;
      if(current.id==='request')rules=rules.filter(r=>current.networks.includes(Number(r['네트워크 문서'])));
      else if(current.id==='output')rules=rules.filter(r=>r['네트워크 문서']==='1935' && r['동작']==='Coil');
      else if(current.id==='reset')rules=rules.filter(r=>r['네트워크 문서']==='1935' && r['동작']==='RCoil');
      else if(current.id==='speed')rules=rules.filter(r=>r['네트워크 문서']==='1692');
      else rules=rules.filter(r=>![1843,1844,1847,1935,1692,1785,1786].includes(Number(r['네트워크 문서'])));
      body=`<p class="bc01-lead">정적 조건을 확인하고 같은 대상의 다른 쓰기·현재 호출 순서를 함께 대조합니다.</p>${current.id==='request'?'<div class="notice">종류·카운터 24/43/13은 원본 비교값입니다. 실제 시간이나 현재 단계로 확정하지 않습니다.</div>':''}${current.id==='output'?'<div class="notice">요청 Set, 최종 Q0.0, 현장 DI1 기동 입력과 실제 운전은 각각 별도 단계입니다.</div>':''}${current.id==='speed'?'<div class="notice">원본 설정 제한 쓰기입니다. 현장 권장값이나 보호값 변경 지시가 아닙니다.</div>':''}${current.id==='other'?'<div class="notice">보존 백업의 simulation 블록 참조는 현재 호출·응답 쓰기 확인 대상입니다. 시뮬레이터를 실행하거나 변경하지 않습니다.</div>':''}${['speed','other'].includes(current.id)?bc01Supplement(current.id):''}${current.id==='speed'?bc01AddressCards(['HMI_DB.SET_PERC_BC01','102A5_SPARE0']):current.id==='request'?bc01AddressCards(['Flag.M_BC_01']):''}${bc01RuleCards(rules)}<details><summary>관련 네트워크 목록 ${spec.networks.length}개</summary>${table(['블록·제목','문서·원본'],spec.networks.map(n=>[esc(n['블록']+' · '+n['제목']),docButton('LAD '+n['문서 ID'],'networks/network-'+n['문서 ID']+'.html')+'<br>'+esc(n['원본 XML'])]))}</details>`;
      sources=[['전체 제어 명세','control-specs/BC01.html'],['요청·출력의 상세 근거','repair-guides/P01.html#output-evidence'],['설정값의 다른 쓰기','recipe-settings.html#profile-P01']];
    } else if(state.bc01Section==='circuits') {
      const path=current.path;
      body=`<div class="status-row"><span class="badge">${esc(path.drawing)} · ${esc(path.backup)}</span><strong>FG${esc(path.fg)} · PDF${pdfPage(path.fg)}</strong></div><p class="bc01-lead">${esc(path.signal)}의 도면상 전달 경로</p><ol class="bc01-path">${path.nodes.map(node=>'<li>'+esc(node)+'</li>').join('')}</ol><section class="bc01-check"><h4>도착점과 전달 경계</h4><p>${esc(path.destination)}</p><h4>관찰·비교할 항목</h4><p>${esc(path.check)}</p><p class="muted">각 구간의 값·시각·자료 위치를 기록합니다. 현재 접속과 정상 극성은 확인 전입니다.</p></section><button type="button" data-drawing="oem-${esc(path.fg)}">해당 도면 크게 확인</button>${path.native_symbol_references.length?links(path.native_symbol_references.map(r=>['LAD '+r.network+' · ORef '+r.uid,'networks/network-'+r.network+'.html'])):'<p class="muted">이 경로에 직접 배정된 원본 심볼 참조는 없습니다. 물리 입력→처리 신호 전달은 추가 확인합니다.</p>'}`;
      sources=[['단자·기동·응답 전체 회로','circuit-guides/BC01.html'],['시공·케이블 근거','construction-guides/BC01.html'],['해당 원본 PDF',drawing.sheets.find(s=>s.id==='oem-'+path.fg).source+'#page='+pdfPage(path.fg)]];
    } else if(state.bc01Section==='alarms') {
      const a=current.alarm;
      body=bc01AlarmBody(a,alarm)+bc01Supplement('alarms');
      sources=[['알람 발생·해제 원본 근거','alarm-guides/BC01.html'],['재기동 판단 작업지','repair-guides/P01.html#recovery'],['공통 리셋·다른 쓰기','common-control.html#checks']];
    } else if(state.bc01Section==='repair') {
      const step=current.step, evidence=schema.evidence_plan.steps.find(s=>s.step_id===step.id);
      body=`${step.id==='response'?bc01DiagnosticMap(schema,circuit):bc01RemainingRepairCards(step)}<ol class="repair-steps">${[['먼저 관찰·기록',step.observe],['원본과 비교',step.compare],['차이와 다음 판단',step.next]].map(([title,text])=>'<li><h4>'+esc(title)+'</h4><p>'+esc(text)+'</p></li>').join('')}</ol><button type="button" data-bc01-diagnose="${esc(step.id)}" class="card-primary-action">이 증상으로 진단·수리 시작</button><details><summary>이 증상에 필요한 자료 ${evidence.requirements.length}항목</summary>${evidence.requirements.map(r=>'<h4>'+esc(r.owner)+'</h4><p>'+esc(r.work)+'</p>').join('')}</details>`;
      sources=[['선택 증상의 상세 판단',schema.manual+'#'+step.common],...evidence.source_links.map(s=>[s.label,s.path])];
    } else {
      if(current.id==='documentation')body='<p>BC01 한 설비의 화면·문서 표준 기준입니다. 원본 정적 대조, 현재 CPU 확인과 실제 수리 완료는 각각 구분합니다.</p>'+table(['표준 항목','완료 기준'],[['찾기·가독성','종류별 선택·세부 항목 목록·본문·근거 분리'],['근거 추적','신호/조건/단자마다 원본 문서·FG/PDF·LAD/UID 연결'],['수리 판단','증상→관찰 위치·값/시각→비교 원본→차이·추가 증거→복구 확인'],['모호한 자료','주소·극성·시공 차이를 확인 대기로 유지'],['검증','최신 파일의 필수 검사·링크·PC/모바일·기록 보존 확인']]);
      else if(['cpu','field','recovery'].includes(current.id))body=bc01CompletionWorkspace(current.id,spec,schema,drawing);
      else body='<div class="notice">BC01 기준을 보존하고 승인된 설비별 확장을 진행합니다. 제외·부모 보류 범위와 현장 미확정은 유지합니다.</div><p>시뮬레이터는 이 프로젝트에서 영구 중지입니다. 전체 작업 완료 후에도 자동 재개하지 않습니다. 작성·수정·실행/행동시험, 실제 PLC·현장 설정·보호값 변경은 수행하지 않습니다. 기존 시뮬레이션 확인 항목과 시험 설계는 보존 자료이며 이번 완료 기준에서 제외합니다.</p>';
      sources=[['BC01 미완료 항목·완료 기준','requirements-audit.html#open-P01'],['현행 자료·실물 대응','priority-guides/P01.html'],['진행 범위','ACTIVE-WORK.md']];
    }
    if(state.bc01Section==='control' && current.id==='request')body=bc01RelationshipBody()+'<details><summary>요청·기억 전체 규칙과 주소</summary>'+body+'</details>';
    if(state.bc01Section==='overview' && current.id==='baseline')body+=bc01InverterComparison();
    if((state.bc01Section==='overview' && ['identity','baseline'].includes(current.id)) || state.bc01Section==='circuits' || (state.bc01Section==='completion' && current.id==='field'))body+=`<div class="notice info bc01-inverter-revision"><strong>인버터 자료의 개정 구분</strong><p>2026-10-11 사용자 확인: 현재 인버터 제작사는 ABB이며, SEJIN의 미쓰비시 등록 자료는 구버전입니다.</p><p class="muted">사용자 확인과 원본 도면 표기를 구분합니다. 현재 ABB의 정확한 모델·정격·단자 배선은 명판·현행 접속도 확인 전이며, 구버전 사양을 현재 설정으로 적용하지 않습니다.</p></div>`;
    const itemIndex=items.findIndex(i=>i.id===current.id), sectionTitle=bc01Sections.find(s=>s[0]===state.bc01Section)[1];
    const itemNav=`<div class="bc01-item-nav"><span><b>${itemIndex+1} / ${items.length}</b> · ${esc(sectionTitle)}</span><div><button type="button" data-bc01-move="prev" ${itemIndex===0?'disabled':''}>이전 항목</button><button type="button" data-bc01-move="next" ${itemIndex===items.length-1?'disabled':''}>다음 항목</button></div></div>`;
    const fieldPath=state.bc01Section==='completion' && current.id==='field'?bc01CompletionTasks('field').find(t=>t.id===state.bc01Check)?.path:null;
    const ioPath=state.bc01Section==='io' && ['물리 입력','물리 출력'].includes(current.role)?circuit.paths.find(p=>p.backup.split('/')[0].trim().toUpperCase()===String(current.raw['백업 주소'] || '').trim().toUpperCase()):null;
    const selectedPath=current.path || fieldPath || ioPath, fg=selectedPath?.fg || 19, preview=drawing.sheets.find(s=>s.id==='oem-'+fg);
    const drawingContext=selectedPath?esc(selectedPath.signal)+' · '+esc(selectedPath.backup)+' · 기존 회로 작업지의 도면 참조':'FG19 / PDF20은 기동 회로의 대표 참고 자료입니다. 선택한 항목의 전용 도면·직접 신호 대응을 확정한 표시가 아닙니다.';
    return `<div class="bc01-standard${bc01Wide?' bc01-wide':''}${state.bc01Text==='large'?' bc01-large-text':''}"><div class="bc01-heading"><div><p class="eyebrow">BC01 / STANDARD MANUAL V1</p><h2>BC-01 · 표준 매뉴얼 작업실</h2><p>한 설비를 기준으로 매뉴얼·수리·제어 구조·근거를 정리합니다.</p></div><div class="inline-actions bc01-reader-controls"><div role="group" aria-label="본문 글자 크기"><button type="button" data-bc01-text="standard" aria-pressed="${state.bc01Text==='standard'}">기본 글자</button><button type="button" data-bc01-text="large" aria-pressed="${state.bc01Text==='large'}">큰 글자</button></div><button type="button" data-bc01-wide aria-pressed="${bc01Wide}">${bc01Wide?'목록·근거 함께 보기':'본문 넓게 보기'}</button>${button('도면 작업실','drawings')}</div></div><div class="notice info">BC01 기준 보존 · 설비별 확장 진행 · 현재 CPU/실물/현장 복구 확인 전</div>${bc01SearchPanel()}<div class="bc01-kinds" role="group" aria-label="BC01 매뉴얼 종류">${bc01Sections.map(([id,title])=>`<button type="button" data-bc01-section="${id}" aria-pressed="${state.bc01Section===id}"><strong>${esc(title)}</strong><small>${bc01Items(id).length}개 세부 항목</small></button>`).join('')}</div><p class="bc01-mobile-hint">세부 항목 목록을 좌우로 밀어 선택하세요. 본문의 이전·다음 항목 버튼도 사용할 수 있습니다.</p><div class="bc01-layout"><nav class="bc01-library" aria-label="BC01 세부 항목"><h3>${esc(bc01Sections.find(s=>s[0]===state.bc01Section)[1])}</h3>${items.map((i,index)=>`<button type="button" data-bc01-item="${esc(i.id)}" aria-pressed="${current.id===i.id}"><span class="bc01-item-number">${String(index+1).padStart(2,'0')}</span> ${esc(i.title)}</button>`).join('')}</nav><section class="bc01-content">${itemNav}<p class="eyebrow">선택한 항목 · 보존 원본의 정적 근거</p><h3 id="bc01-content-title" tabindex="-1">${esc(current.title)}</h3>${body}${bc01SourceNavigation()}<details class="bc01-inline-sources"><summary>이 항목의 원본·관련 근거 열기</summary>${links(sources)}</details>${itemNav}</section><aside class="bc01-evidence"><section class="panel"><h3>원본·관련 근거</h3>${links(sources)}</section><section class="panel bc01-drawing-evidence" data-bc01-drawing-context="${selectedPath?'path':'reference'}"><h3>${selectedPath?'선택 경로의 전기도면':'대표 참고 전기도면'}</h3><p class="muted">${drawingContext}</p><button type="button" data-drawing="${esc(preview.id)}" class="bc01-preview"><img src="${esc(preview.image)}" alt="BC01 FG${fg} 원본 페이지 미리보기"><span>${esc(preview.title)} · 도면 작업실에서 확대</span></button><p class="muted">개정·단자·현재 접속은 원본과 현장 자료를 대조합니다.</p></section><section class="panel"><h3>미확정 경계</h3><p>${esc(circuit.distinction)}</p>${drawing.warnings.map(w=>'<div class="notice">'+esc(w)+'</div>').join('')}${button('관찰 근거 기록','repair-record')}${button('기존 진단·수리','repair')}</section></aside></div></div>`;
  }
  function renderRepairWorkspace() {
    const schema=repairRecordMap.get(state.selected), step=schema?.steps.find(s=>s.id===state.repairSymptom);
    if(!step)return unknownPanel();
    const plan=schema.evidence_plan, evidence=plan?.steps.find(s=>s.step_id===step.id);
    const drawing=drawingMap.get(state.selected);
    const roles=[['requests','운전 요청'],['outputs','최종 PLC 출력'],['responses','처리된 응답']];
    const links=(items=[])=>items.filter(x=>validDoc(x.path)).map(x=>docButton(x.label,x.path)).join('');
    return `<div class="repair-workspace">
      <div class="view-heading"><div><p class="eyebrow">REPAIR / SOURCE EVIDENCE</p><h2>${esc(schema.name)} · 진단·수리 작업실</h2><p>증상을 선택하고 점검 순서와 원본 근거를 확인하세요.</p></div>${button('도면 작업실','drawings')}${state.selected==='P01'?button('BC01 표준 매뉴얼','manual'):''}</div>
      <div class="notice info">기존 백업의 정적 근거를 연결한 점검 안내입니다. 실물 동일성·현재 CPU 동작·현장 복구 상태는 확인 전입니다.</div>
      <section class="panel repair-selector"><h3>1. 현재 증상 선택</h3><div class="repair-symptoms" role="group" aria-label="진단 증상">${schema.steps.map((s,i)=>`<button type="button" data-repair-symptom="${esc(s.id)}" aria-pressed="${s.id===step.id}"><span class="repair-number">${i+1}</span><span>${esc(s.title)}</span></button>`).join('')}</div></section>
      <div class="repair-columns"><div class="repair-main">
      <section class="panel"><p class="eyebrow">선택한 증상의 점검 순서</p><h3 id="repair-step-title">${esc(step.title)}</h3><ol class="repair-steps">${[['먼저 관찰·기록',step.observe],['원본과 비교',step.compare],['차이와 다음 판단',step.next]].map(([title,text])=>`<li><h4>${esc(title)}</h4><p>${esc(text)}</p></li>`).join('')}</ol><div class="inline-actions">${docButton('이 증상의 상세 근거',schema.manual+'#'+step.common)}${button('관찰 결과 기록','repair-record',state.selected,'class="card-primary-action"')}</div></section>
      <section class="panel"><h3>요청 → 출력 → 처리 응답</h3><p class="muted">아래 이름과 주소는 백업 참조입니다. 현재값은 관찰 후 기록하며, 처리 응답을 원시 센서 또는 실제 동작으로 간주하지 않습니다.</p><div class="repair-signals">${roles.map(([role,title])=>`<article><h4>${esc(title)}</h4>${schema.signals.filter(s=>s.role===role).map(s=>`<div class="repair-signal"><code>${esc(s.name)}</code><p>${esc(s.addresses.join(' / ') || 'DB/주소 추가 확인')}</p><details><summary>원본 참조 ${s.refs.length}개</summary><div class="repair-source-links">${s.refs.map(r=>docButton('LAD '+r.network+' · ORef '+r.oref,'networks/network-'+r.network+'.html')).join('')}</div></details></div>`).join('')}</article>`).join('')}</div>${button('I/O·HMI 참조 확인','io')}</section>
      <section class="panel"><h3>추가로 확보할 자료</h3>${(evidence?.requirements || []).map(r=>`<div class="repair-requirement"><span class="badge">${esc(r.owner)}</span><p>${esc(r.work)}</p></div>`).join('') || '<p>기존 상세 작업지에서 필요한 자료를 확인하세요.</p>'}</section>
      </div><aside class="repair-evidence">
      <section class="panel"><h3>2. 관련 근거 열기</h3><div class="repair-primary-links">${button('관련 도면·단자·케이블','drawings')}${docButton('알람 발생·리셋·재기동','alarm-guides/'+schema.reference_plc_id+'.html')}${button('원본 래더 목록','ladder')}${docButton('전체 진단 작업지',schema.manual)}</div>${drawing?.circuit?`<p>${esc(drawing.circuit.equipment)}</p><p class="muted">${esc(drawing.circuit.distinction)}</p>`:''}${(drawing?.warnings || []).map(w=>`<div class="notice">${esc(w)}</div>`).join('')}<details><summary>선택 증상의 세부 근거 ${evidence?.source_links.length || 0}개</summary><div class="repair-source-links">${links(evidence?.source_links)}</div></details></section>
      <section class="panel"><h3>점검 전 자료 확인</h3>${(plan?.preflight.requirements || []).map(r=>`<p><strong>${esc(r.owner)}</strong><br>${esc(r.work)}</p>`).join('')}<div class="inline-actions">${docButton('실물 대응·점검 작업지','priority-guides/'+schema.key+'.html')}${docButton('미완료 항목·완료 기준','requirements-audit.html#open-'+schema.key)}</div></section>
      <section class="panel"><h3>관련 미확정 사항</h3><p class="muted">기존 확인 대장의 상태를 그대로 표시합니다.</p>${(evidence?.reviews || []).length?`<details><summary>확인 대기·불일치 ${evidence.reviews.length}항목</summary>${evidence.reviews.map(r=>`<article class="repair-review"><h4>${esc(r.title)}</h4><span class="badge pending">${esc(r.status)}</span><p>${esc(r.next_check)}</p><div class="repair-source-links">${links(r.links)}</div></article>`).join('')}</details>`:'<p>상세 작업지의 확인 대기를 참고하세요.</p>'}${button('근거 검토·확인 대장','review')}</section>
      <section class="panel"><h3>3. 결과 기록과 복구 확인</h3><p>관찰값·시각·근거를 기존 기록 양식에 남깁니다. 원인 해소, 알람 해제, 기동 허가, 실제 응답과 연동 영향을 각각 확인합니다.</p>${button('수리 관찰 기록 열기','repair-record',state.selected,'class="card-primary-action"')}<p class="muted">증상 선택은 입력값을 채우거나 수리 완료를 처리하지 않습니다.</p></section>
      </aside></div></div>`;
  }
  function renderRepairRecord() {
    if (equipmentStatus(state.selected)?.status==='other_process_excluded_user_reported') return panel('현재 작업 대상에서 제외','<p>'+esc(equipmentStatus(state.selected).label)+' · 관련 조사·분석·보강 중단. 기존 기록 양식 데이터는 보존합니다.</p>');
    const schema=repairRecordMap.get(state.selected);
    if(!schema)return `<h2>수리 관찰 기록</h2><p>상세 기록 양식은 디코팅 우선23개에 연결되어 있습니다. 전체 목록의 기본 자료와 일반 작업 메모는 계속 사용할 수 있습니다.</p>${button('우선 설비 선택','priority')}${button('일반 작업 메모','notes')}`;
    const draft=drafts[repairRecords.keyFor(state.selected)] || {};
    const own=notes.filter(n=>n.equipment===state.selected && n.repair_observation).sort((a,b)=>b.updated.localeCompare(a.updated));
    const step=repairWorkspaceKeys.has(state.selected)?schema.steps.find(s=>s.id===state.repairSymptom):null;
    const context=step?`<div class="notice info repair-context"><p>진단에서 선택한 증상: <strong>${esc(step.title)}</strong></p><p>관찰한 값과 결과를 아래 양식에 직접 기록하세요.</p>${button('선택 증상의 점검 순서로 돌아가기','repair')}</div>`:'';
    return context+(storageError?`<div class="notice">${esc(storageError)}</div>`:'')+repairRecords.render(schema,draft,own);
  }
  function renderResources() {
    const resources = [
      ['미확정3설비 식별·자료 후보','웨잉호퍼1·배출컨베이어·2사이클론 · 주소 배정 없이 경계 비교','unresolved-identity.html'],
      ['CC01·AB01·HE01 본체 매뉴얼','본체3개 · 증상12개 · 공정/계측/구역 경계 · 원본34네트워크','body-manual.html'],
      ['작성 상태·누락·다음 작업','248개 기본/상세 자료 · 우선23개 · 미확정·후속 작업','requirements-audit.html'],
      ['사용 안내','설비 선택·근거 비교·관찰 기록·JSON 보관·검증 범위','operator-guide.html'],
      ['진행 순서·완료 기준','현재 상세 보완·다음 작업 · 문서/원본/현장 상태 구분','work-progress.html'],
      ['기존 전체 매뉴얼','248개 설비와 원본 자료 안내','manual-catalog.html'],
      ['전체 제어 명세','입출력·조건·순서·이상 처리','control-spec.html'],
      ['근거 검토·확인 목록','원본18 · 시공7 · 공통10 · 개선6 · 동일성23','evidence-review.html'],
      ['수리 판단·공통 영향',(data.review_counts?.repair_guides || 0)+'개 우선 작업지 · 요청·출력·응답·알람·복구 근거','repair-decision.html'],
      ['모터·밸브 알람·복구 비교',(data.review_counts?.alarm_guides || 0)+'개 작업지 · 발생·리셋·감시 시간·원본 접점과 요청 해제','alarm-recovery.html'],
      ['레시피·설정값·전원 복귀','편집/저장/불러오기 · 8적용값 · 원본 LAD20 · 색인7 · 다른 쓰기/초기화8증상','recipe-settings.html'],
      ['HMI 설정·표시·PLC 전달 확인','782태그 · 17화면 메타데이터 · 원본 LAD47 · 주소 공유/범위 대조 후보','hmi-transfer.html'],
      ['엔코더·위치·교정 수리','5개 밸브 · 원본26네트워크 · 카운터5호출·위치 환산·교정2경로','encoder-position.html'],
      ['주요 조절 루프 수리·구조','9개 경로 · 원본 LAD33 · 조절기5호출 · STL/SCL10항목을 별도 대조','regulation-manual.html'],
      ['온도·압력·산소 계측 수리','19개 채널 · 도면15FG·원본42네트워크 · 다른 쓰기·표시값 출처 확인','sensor-measurement.html'],
      ['가스·공기 계측·환산·출력','입력4·출력2 · 정수 연산·후속 제한·원본 계수·실제값 확인 전','measurement-trace.html'],
      ['공정 알람·버너 정지 원인','공정11개 이름 · 발생/리셋10개 · 쓰기 미확정1개 · 최초 원인과 후속 정지 구분','process-stop-alarms.html'],
      ['BR01 외부 연동·정지·복구','원본16개 네트워크 · 두 Enable·리셋·MV03 연동 · 전용 연소제어 내부 확인 전','burner-interface.html'],
      ['구조 개선 검토','원본 구조 후보 '+(data.review_counts?.improvement_candidates || 0)+'건 · 수정 필요성 확인 전','improvement-review.html'],
      ['전기 회로 추적',(data.review_counts?.electrical_devices || 0)+'개 항목 · '+(data.review_counts?.electrical_paths || 0)+'개 신호 경로 · '+(data.review_counts?.electrical_sheets || 0)+'개 도면','electrical-trace.html'],
      ['신호 전달·복수 쓰기 분석',(data.review_counts?.signal_guides || 0)+'개 작업지 · 원본 핀 '+(data.review_counts?.signal_pin_usages || 0)+'곳 · 현재 호출 확인 전','signal-trace.html'],
      ['공통 허가·자동 요청·알람·리셋',(data.review_counts?.common_guides || 0)+'개 우선 작업지 · 카운터 단계·요청과 출력 구분 · 확인 대기10건','common-control.html'],
      ['추가 시공도면 · 배관·케이블','64페이지 · 선택 동력17행·제어34행 · 확인 대기7건','construction-guide.html'],
      ['현재 작업 범위','별도 작성 요청 전 시뮬레이터 개발·시험 중지 · 매뉴얼·수리·구조 분석','ACTIVE-WORK.md'],
      ['PLC 네트워크','전체 색인 457개 / 원본 LAD 426개','plc-networks.html'],
      ['PLC 심볼','789개 주소·자료형·원문 설명','plc-symbols.html'],
      ['HMI 설정','782개 설정과 PLC 주소','hmi-tags.html'],
      ['P&ID','1684n002 Rev.I · 1페이지','sources/PID_1684n002I.pdf#page=1'],
      ['전기도면','IMPIANTO COREA Rev.2 · 265페이지','sources/Electrical_Rev2.pdf#page=1'],
      ['시공도면 원본','Can-Decoating_20241118 · FOR APPROVAL · 승인·준공 미확인','sources/Electrical_Can_Decoating_20241118.pdf#page=1'],
      ['PV01 기존 세부편','배선·원본 분석 초기 검토본','PV01-detail/index.html'],
      ['프로젝트 목적','매뉴얼·수리·분석·올인원 작업 기준','PROJECT-PURPOSE.md'],
      ['우선 23개 대응표','태그명 일치·대응 후보·미확정 분리','registers/priority-equipment.csv'],
    ].filter(r => validDoc(r[2]));
    return `<h2>전체 자료를 같은 작업실에서 봅니다</h2><div class="resource-grid">${resources.map(([title,description,path]) => `<button type="button" data-doc="${esc(path)}"><strong>${esc(title)}</strong><small>${esc(description)}</small></button>`).join('')}</div>
      ${panel('원본·대장 다운로드', '<p class="muted">원본 백업과 표는 그대로 보존합니다. 다운로드할 때 전체 폴더와 자료를 함께 보관하세요.</p><div class="inline-actions">'+[['PLC 원본 백업','sources/GME_20250506.zap18'],['설비 대장 CSV','registers/equipment.csv'],['시험 설계 CSV','registers/simulation-tests.csv'],['확인 대장 CSV','registers/verification.csv'],['제어 명세 JSON','registers/control-spec.json'],['올인원 자료 JSON','registers/all-in-one-data.json']].map(([t,path]) => `<a href="${esc(path)}" download>${esc(t)}</a>`).join(' · ')+'</div>')}`;
  }
  function showDocument(path, label) {
    if (!validDoc(path)) {
      $('workspace-content').innerHTML += '<div class="notice">자료 경로를 확인할 수 없습니다.</div>'; return;
    }
    const source = new URL(path, base);
    $('document-label').textContent = label || path;
    $('document-source').href = source.href;
    const extension = path.split('#')[0].split('.').pop().toLowerCase();
    if (['md','csv','json','xml'].includes(extension) && location.protocol !== 'file:') {
      const currentRender = state.renderId;
      $('workspace-content').innerHTML += '<pre id="source-preview" class="source-text">자료를 읽고 있습니다…</pre>';
      fetch(source).then(response => { if (!response.ok) throw new Error('read failed'); return response.text(); }).then(text => {
        if (currentRender === state.renderId && $('source-preview')) $('source-preview').textContent = text;
      }).catch(() => {
        if (currentRender === state.renderId && $('source-preview')) $('source-preview').textContent = '자료를 읽지 못했습니다. 전체 자료 메뉴에서 원본을 확인해 주세요.';
      });
      return;
    }
    $('document-workspace').hidden = false;
    $('document-frame').src = source.href;
    $('document-frame').title = label || '통합 자료 보기';
  }
  function render() {
    window.GMEBC01Tools?.close();
    window.GMEUnifiedBackup?.close();
    closeBC01ProofPreview();
    window.GMESimulatorWorkspace?.cleanup();
    $('workspace-content').onclick = null;
    $('workspace-content').onchange = null;
    state.renderId++;
    document.body.dataset.view=state.view;
    renderContext();
    $('document-workspace').hidden = true;
    const host = $('workspace-content');
    const {d} = selection();
    const funcs = {overview:renderOverview,priority:renderPriority,summary:renderSummary,io:renderIO,ladder:renderLadder,structure:renderStructure,drawings:renderDrawings,simulator:renderSimulator,conflicts:renderConflicts,notes:renderNotes,resources:renderResources,review:renderReview,'repair-record':renderRepairRecord};
    if(state.view==='manual' && state.selected==='P01'){host.innerHTML=renderBC01Manual();const rail=host.querySelector('.bc01-library'), selected=rail?.querySelector('[aria-pressed="true"]');if(rail && selected && rail.scrollWidth>rail.clientWidth)rail.scrollLeft=Math.max(0,selected.offsetLeft-rail.offsetLeft-12);}
    else if(state.view==='manual' && window.GMEEquipmentStandard.profile(data,state.selected)){host.innerHTML=window.GMEEquipmentStandard.render(data,state.selected,state);window.GMEEquipmentStandard.highlight(host,state.bc01Find);}
    else if(state.view==='repair' && repairWorkspaceKeys.has(state.selected)) host.innerHTML=renderRepairWorkspace();
    else if (funcs[state.view]) { host.innerHTML = funcs[state.view](); if(state.view==='review')renderReviewRows(); if(state.view==='priority')restoreLayoutScroll(); }
    else if (state.view === 'tests' || state.view === 'checks') {
      host.innerHTML = `<h2>${state.view === 'tests' ? '시험 설계 · 577건 / 전체 검증 전' : '확인 대장 · 1,060건'}</h2><p class="muted">원본 대장의 상태를 그대로 표시합니다. 부분 가상 시험은 아래 별도 결과에서 확인합니다.</p>` + (state.view==='tests'?renderModelResults():'') + filterUI(state.view === 'tests' ? '시험' : '확인');
      renderRegister();
    } else if (state.view === 'doc') {
      host.innerHTML = '';
      if (state.doc) showDocument(state.doc);
      else host.innerHTML = renderResources();
    } else if (d) {
      host.innerHTML = state.view === 'repair' ? `<div class="notice info">원본 조건에 연결한 진단 작업지입니다. 상세 단자·정상 극성과 현재 현장 복구 조건은 추가 확인이 필요합니다.</div><div class="inline-actions">${button('알람·리셋 조건','spec',state.selected,'data-anchor="fault"')}${button('I/O 추적','io')}${button('전기도면','drawings')}${button('관련 근거 검토','review')}${selection().p?docButton('실물 대응·점검 작업지',`priority-guides/${selection().p.key}.html`):''}</div>` : '';
      const path = state.view === 'spec' ? `control-specs/${d.id}.html` : state.view==='repair' ? (selection().p ? `repair-guides/${selection().p.key}.html` : `procedures/${d.id}.html`) : `devices/${d.id}.html`;
      const anchor = '';
      showDocument(path + anchor, `${d.id} · ${labels[state.view]}`);
    } else if (selection().p && ['repair','manual'].includes(state.view)) {
      host.innerHTML = '<div class="notice">PLC 대응을 확인하기 위한 설비 점검·자료 수집 작업지입니다.</div>';
      showDocument(`${state.view==='repair'?'repair':'priority'}-guides/${selection().p.key}.html`);
    } else host.innerHTML = unknownPanel();
    // Preserve the loaded frame for same-document anchors; clearing src first
    // can leave a pending about:blank navigation that overrides the anchor.
    if ($('document-workspace').hidden) $('document-frame').removeAttribute('src');
    if (state.view==='simulator') window.GMESimulatorWorkspace?.mount(host,render);
    window.GMEBC01Tools?.mount(host);
  }
  function openEmbedded(path, key = state.selected) {
    if (path === 'index.html' || path.startsWith('index.html#')) path = path.replace(/^index\.html/, 'manual-catalog.html');
    if (!validDoc(path)) return;
    const equipmentDoc = /^(?:devices|control-specs|procedures|circuit-guides|construction-guides|signal-guides)\/([\w-]+)\.html(?:#.*)?$/.exec(path);
    const priorityDoc = /^(?:priority|common|repair)-guides\/(P\d{2})\.html(?:#.*)?$/.exec(path);
    if (priorityDoc && priorityMap.has(priorityDoc[1])) {
      key = priorityDoc[1];
    } else if (equipmentDoc && deviceMap.has(equipmentDoc[1]) && selection(key).d?.id !== equipmentDoc[1]) {
      const priority = state.scope === 'priority' ? data.priority.find(p => p.plc_id === equipmentDoc[1]) : null;
      key = priority?.key || equipmentDoc[1];
    }
    route('doc',key,path);
  }
  const preparedDocuments = new WeakSet();
  $('document-frame').addEventListener('load', () => {
    if ($('document-workspace').hidden) return;
    try {
      const doc = $('document-frame').contentDocument;
      if (!doc?.body || preparedDocuments.has(doc)) return;
      preparedDocuments.add(doc);
      const style = doc.createElement('style');
      style.textContent = 'body>header,body>footer{display:none!important}.layout{max-width:none!important}main{padding:22px!important}h2{scroll-margin-top:20px!important}.toc{top:0!important;max-height:95vh!important;width:190px!important}@media(max-width:650px){.toc{display:none!important}main{padding:14px!important}}';
      doc.head.appendChild(style);
      const sourceLocation=data.bc01_standard?.source_locations?.find(r=>r.path===state.doc);
      if(sourceLocation && state.selected==='P01') {
        if(state.bc01Text==='large') {
          const readingStyle=doc.createElement('style');
          readingStyle.textContent='main p,main td,main th,main code,main .muted{font-size:18px!important;line-height:1.8!important}';
          doc.head.appendChild(readingStyle);
        }
        const row=doc.getElementById('bc01-'+sourceLocation.kind+'-'+sourceLocation.uid);
        if(row){row.setAttribute('tabindex','-1');row.focus({preventScroll:true});row.scrollIntoView({block:'center'});}
      }
      doc.addEventListener('click', e => {
        const a = e.target.closest('a[href]');
        if (!a || a.hasAttribute('download') || e.ctrlKey || e.metaKey || e.shiftKey || e.button !== 0) return;
        const url = new URL(a.href, doc.baseURI);
        if (url.origin !== base.origin || !url.pathname.startsWith(base.pathname)) return;
        let path;
        try { path = decodeURIComponent(url.pathname.slice(base.pathname.length)) + url.hash; } catch (_) { return; }
        if(url.pathname===base.pathname || url.pathname.slice(base.pathname.length)==='index.html'){
          const params=new URLSearchParams(url.hash.slice(1));
          if(params.get('view')==='drawings' && drawingMap.has(params.get('equipment'))){e.preventDefault();const requested=params.get('drawing');if(drawingMap.get(params.get('equipment')).sheets.some(s=>s.id===requested))state.drawing=requested;route('drawings',params.get('equipment'));return;}
          if(params.get('view')==='repair-record' && repairRecordMap.has(params.get('equipment'))){e.preventDefault();route('repair-record',params.get('equipment'));return;}
          if(params.get('view')==='repair' && repairWorkspaceKeys.has(params.get('equipment'))){e.preventDefault();route('repair',params.get('equipment'));return;}
          if(params.get('view')==='manual' && params.get('equipment')==='P01'){e.preventDefault();state.bc01Section=bc01Sections.some(s=>s[0]===params.get('section'))?params.get('section'):'overview';state.bc01Item=bc01Items(state.bc01Section).find(i=>i.id===params.get('item'))?.id || '';state.bc01Check=bc01CompletionTasks(state.bc01Item).find(t=>t.id===params.get('check'))?.id || '';state.bc01Find=(params.get('find') || '').trim().slice(0,160);state.bc01Relation=data.bc01_standard.relationships.nodes.find(n=>n.id===params.get('relation'))?.id || 'request';if(params.has('text'))state.bc01Text=params.get('text')==='large'?'large':'standard';if(params.has('alarmStep'))state.bc01AlarmStep=['set','reset','restart'].includes(params.get('alarmStep'))?params.get('alarmStep'):'set';route('manual','P01');return;}
          if(params.get('view')==='review' && priorityMap.has(params.get('equipment'))){e.preventDefault();route('review',params.get('equipment'),'',params.get('review') || '');return;}
        }
        if (path.startsWith('index.html')) path = path.replace(/^index\.html/,'manual-catalog.html');
        if (!validDoc(path)) return;
        e.preventDefault();
        openEmbedded(path);
      });
    } catch (_) { /* PDF viewers and file:// frames may deny DOM access. */ }
  });

  document.addEventListener('click', e => {
    const b = e.target.closest('button'); if (!b) return;
    if(state.view==='manual' && state.selected!=='P01' && window.GMEEquipmentStandard.profile(data,state.selected)) {
      const library=window.GMEEquipmentStandard;
      if(b.dataset.standardSection){state.bc01Section=b.dataset.standardSection;state.bc01Item=library.items(data,state.selected,state.bc01Section)[0]?.id||'';route('manual');return;}
      if(b.dataset.standardItem){state.bc01Item=b.dataset.standardItem;route('manual');return;}
      if(b.dataset.standardJump){const [section,item]=b.dataset.standardJump.split('/');state.bc01Section=section;state.bc01Item=item;route('manual');return;}
      if(b.dataset.standardText){state.bc01Text=b.dataset.standardText;route('manual');return;}
      if(b.hasAttribute('data-standard-wide')){state.standardWide=!state.standardWide;render();return;}
      if(b.hasAttribute('data-standard-clear')){state.bc01Find='';lastRenderedRoute=null;route('manual');return;}
      if(b.dataset.standardMove){const items=library.items(data,state.selected,state.bc01Section),i=items.findIndex(x=>x.id===state.bc01Item),next=items[i+(b.dataset.standardMove==='next'?1:-1)];if(next){state.bc01Item=next.id;route('manual');document.getElementById('standard-content-title')?.focus({preventScroll:true});}return;}
    }
    if(b.hasAttribute('data-bc01-proof-close')) {closeBC01ProofPreview();return;}
    if(b.hasAttribute('data-bc01-proof-print')) {if(document.getElementById('bc01-proof-preview')?.open)window.print();return;}
    if(state.view==='manual' && state.selected==='P01') {
      if(b.hasAttribute('data-bc01-proof-preview')) {openBC01ProofPreview();return;}
      if(b.dataset.bc01Text && ['standard','large'].includes(b.dataset.bc01Text)) {state.bc01Text=b.dataset.bc01Text;route('manual');document.querySelector(`[data-bc01-text="${state.bc01Text}"]`)?.focus({preventScroll:true});return;}
      if(b.dataset.bc01AlarmStep && ['set','reset','restart'].includes(b.dataset.bc01AlarmStep)) {state.bc01AlarmStep=b.dataset.bc01AlarmStep;route('manual');document.querySelector(`[data-bc01-alarm-step="${state.bc01AlarmStep}"]`)?.focus({preventScroll:true});return;}
      if(b.dataset.bc01MediaGroup) {if(state.selected==='P01' && state.bc01Section==='overview' && state.bc01Item==='media'){bc01NormalizeMedia(b.dataset.bc01MediaGroup,'');route('manual');}return;}
      if(b.dataset.bc01Photo) {if(state.selected==='P01' && state.bc01Section==='overview' && state.bc01Item==='media'){bc01NormalizeMedia(state.bc01MediaGroup,b.dataset.bc01Photo);route('manual');}return;}
      if(b.dataset.bc01Check) {if(state.selected==='P01' && state.bc01Section==='completion' && bc01CompletionTasks(state.bc01Item).some(t=>t.id===b.dataset.bc01Check)){state.bc01Check=b.dataset.bc01Check;route('manual');document.querySelector('.bc01-check-tabs [aria-pressed="true"]')?.focus({preventScroll:true});}return;}
      if(b.dataset.bc01Move) {const items=bc01Items(state.bc01Section), i=items.findIndex(item=>item.id===state.bc01Item), next=items[i+(b.dataset.bc01Move==='prev'?-1:1)];if(next){state.bc01Item=next.id;route('manual');document.querySelector('.bc01-content')?.scrollIntoView({block:'start'});document.getElementById('bc01-content-title')?.focus({preventScroll:true});}return;}
      if(b.dataset.bc01Jump) {const [section,item]=b.dataset.bc01Jump.split('/');bc01Navigate(section,item,{alarmStep:b.dataset.bc01JumpAlarm});return;}
      if(b.dataset.bc01Relation && data.bc01_standard.relationships.nodes.some(n=>n.id===b.dataset.bc01Relation)){state.bc01Relation=b.dataset.bc01Relation;route('manual');document.querySelector('.bc01-relation-detail')?.scrollIntoView({block:'start'});document.querySelector('.bc01-relation-detail h5')?.setAttribute('tabindex','-1');document.querySelector('.bc01-relation-detail h5')?.focus({preventScroll:true});return;}
      if(b.hasAttribute('data-bc01-find-clear')){state.bc01Find='';bc01SearchLimit=20;route('manual');document.getElementById('bc01-find')?.focus({preventScroll:true});return;}
      if(b.hasAttribute('data-bc01-find-more')){bc01SearchLimit+=20;render();document.querySelector('[data-bc01-find-more]')?.focus({preventScroll:true});return;}
      if(b.hasAttribute('data-bc01-search-result')){const index=Number(b.dataset.bc01SearchResult),r=Number.isInteger(index)?bc01BuildSearchIndex()[index]:null;if(r)bc01Navigate(r.section,r.item,r.choice);return;}
    }
    if(b.hasAttribute('data-bc01-wide') && state.selected==='P01'){bc01Wide=!bc01Wide;render();document.querySelector('[data-bc01-wide]')?.focus({preventScroll:true});return;}
    if(b.dataset.bc01Section) {
      if(state.selected!=='P01' || !bc01Sections.some(s=>s[0]===b.dataset.bc01Section))return;
      state.bc01Section=b.dataset.bc01Section;state.bc01Item=bc01LastItems.get(state.bc01Section) || bc01Items(state.bc01Section)[0].id;route('manual');
      document.querySelector(`[data-bc01-section="${state.bc01Section}"]`)?.focus({preventScroll:true});return;
    }
    if(b.dataset.bc01Item) {
      if(state.selected!=='P01' || !bc01Items(state.bc01Section).some(i=>i.id===b.dataset.bc01Item))return;
      state.bc01Item=b.dataset.bc01Item;route('manual');document.querySelector(`[data-bc01-item="${state.bc01Item}"]`)?.focus({preventScroll:true});return;
    }
    if(b.dataset.bc01Diagnose) {
      if(state.selected!=='P01' || !repairRecordMap.get('P01').steps.some(s=>s.id===b.dataset.bc01Diagnose))return;
      state.repairSymptom=b.dataset.bc01Diagnose;route('repair');return;
    }
    if(b.dataset.repairSymptom) {
      if(!repairWorkspaceKeys.has(state.selected) || !repairRecordMap.get(state.selected)?.steps.some(s=>s.id===b.dataset.repairSymptom))return;
      state.repairSymptom=b.dataset.repairSymptom;route('repair');
      document.querySelector(`[data-repair-symptom="${state.repairSymptom}"]`)?.focus({preventScroll:true});return;
    }
    if(b.dataset.photo) {photoAction(b.dataset.photo);return;}
    if(b.hasAttribute('data-open-photo')) {openPhotoViewer();return;}
    if(b.dataset.drawingKind) {
      const profile=drawingMap.get(selection().p?.key),kind=b.dataset.drawingKind;
      const sheets=profile?.sheets.filter(s=>s.kind===kind) || [];
      if(!sheets.length || sheets.some(s=>s.id===state.drawing))return;
      state.drawing=sheets.find(s=>s.id===drawingLastByKind.get(profile.key+':'+kind))?.id || sheets[0].id;
      state.drawingZoom=1;route('drawings');
      document.querySelector(`[data-drawing-kind="${kind}"]`)?.focus({preventScroll:true});
    } else if(b.dataset.drawing) {
      if(!drawingMap.get(selection().p?.key)?.sheets.some(s=>s.id===b.dataset.drawing))return;
      if(state.drawing===b.dataset.drawing)return;
      state.drawing=b.dataset.drawing; state.drawingZoom=1; route('drawings');
      document.querySelector(`[data-drawing="${state.drawing}"]`)?.focus({preventScroll:true});
    } else if(b.hasAttribute('data-drawing-wide')) {
      state.drawingWide=!state.drawingWide;render();document.querySelector('[data-drawing-wide]')?.focus({preventScroll:true});
    } else if(b.dataset.drawingZoom) {
      const image=$('drawing-image'), viewport=$('drawing-viewport');if(!image || !viewport)return;
      const action=b.dataset.drawingZoom;state.drawingZoom=action==='fit'?1:Math.max(1,Math.min(4,state.drawingZoom+(action==='in'?0.5:-0.5)));
      image.style.width=state.drawingZoom*100+'%';$('drawing-zoom-value').textContent=Math.round(state.drawingZoom*100)+'%';
      document.querySelector('[data-drawing-zoom="out"]').disabled=state.drawingZoom<=1;
      document.querySelector('[data-drawing-zoom="in"]').disabled=state.drawingZoom>=4;
      if(action==='fit'){viewport.scrollLeft=0;viewport.scrollTop=0;}
    } else if (b.dataset.layoutSelect) {
      rememberLayoutScroll(); route('priority',b.dataset.layoutSelect);
      if (window.matchMedia('(max-width:1100px)').matches) {
        $('layout-card-title')?.focus({preventScroll:true});
        document.querySelector('.equipment-detail-card')?.scrollIntoView({block:'start'});
      } else document.querySelector(`[data-layout-select="${state.selected}"]`)?.focus({preventScroll:true});
    } else if (b.hasAttribute('data-layout-return')) {
      document.querySelector('.process-navigation')?.scrollIntoView({block:'start'});
      document.querySelector(`[data-layout-select="${state.selected}"]`)?.focus({preventScroll:true});
    } else if (b.dataset.layoutMode) {
      const mode=b.dataset.layoutMode; state.layoutMode=mode; render();
      document.querySelector(`[data-layout-mode="${mode}"]`)?.focus({preventScroll:true});
    } else if (b.dataset.layoutZoom) {
      const viewport=$('layout-viewport');
      if(!viewport)return;
      const old=state.layoutZoom;
      const action=b.dataset.layoutZoom;
      state.layoutZoom=action==='fit'?Math.max(0.15,Math.min(1,viewport.clientWidth/1220)):Math.max(0.2,Math.min(1.4,old+(action==='in'?0.15:-0.15)));
      state.layoutScroll=action==='fit'?[0,0]:[viewport.scrollLeft*state.layoutZoom/old,viewport.scrollTop*state.layoutZoom/old];render();
      document.querySelector(`[data-layout-zoom="${action}"]`)?.focus({preventScroll:true});
    } else if (b.dataset.scope) {
      state.scope = b.dataset.scope; state.group = ''; state.listQuery = ''; $('equipment-search').value = ''; syncScope(); renderList();
      const params = new URLSearchParams({view:state.view,equipment:state.selected,scope:state.scope});
      if (state.doc) params.set('doc',state.doc);
      if(state.view==='drawings' && drawingMap.get(state.selected)?.sheets.some(s=>s.id===state.drawing)) params.set('drawing',state.drawing);
      history.replaceState(null,'','#'+params.toString());
    } else if (b.dataset.select) {
      const view = deviceViews.has(state.view) ? state.view : 'summary';
      route(view,b.dataset.select);
    } else if (b.dataset.view) {
      if (b.dataset.anchor && selection().d) openEmbedded(`control-specs/${selection().d.id}.html#${b.dataset.anchor}`);
      else route(b.dataset.view,b.dataset.equipment || state.selected);
    } else if (b.dataset.doc) openEmbedded(b.dataset.doc);
    else if (b.dataset.editRepair) {
      const note=notes.find(n=>n.id===b.dataset.editRepair);
      const schema=repairRecordMap.get(note?.equipment);
      if(!schema || !note.repair_observation)return;
      const draft={...repairRecords.fromRecord(note.repair_observation,schema),noteId:note.id,base_note:JSON.stringify(note),title:note.title};
      const key=repairRecords.keyFor(note.equipment);
      try{drafts=storeDraft(key,draft);}catch(_){drafts[key]=draft;}
      if(window.GMEEquipmentStandard.profile(data,note.equipment))lastRenderedRoute=null;
      route('repair-record',note.equipment);
    } else if (b.dataset.exportRepair) {
      let latest;
      try{latest=noteStore.decodeNotes(localStorage.getItem(NOTES_KEY),validNoteEquipment);}catch(_){$('app-message').textContent='저장된 자료를 읽지 못했습니다. 기존 기록을 보존하고 확인해 주세요.';return;}
      const note=latest.find(n=>n.id===b.dataset.exportRepair);
      if(!note?.repair_observation)return;
      const payload=window.GMEBC01Tools.backupEnvelope([note],data,undefined,note.equipment);
      const url=URL.createObjectURL(new Blob([JSON.stringify(payload,null,2)],{type:'application/json;charset=utf-8'}));
      const a=document.createElement('a');a.href=url;a.download=`GME-repair-${note.equipment}-${note.id}.json`;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
    }
    else if (b.dataset.reviewNote) startReviewNote(b.dataset.reviewNote);
    else if (b.dataset.reviewFocus) route('review',state.selected,'',b.dataset.reviewFocus);
    else if (b.hasAttribute('data-export-notes')) {
      try { window.GMEUnifiedBackup.download(); }
      catch(error){$('app-message').textContent=error.message;}
    } else if (b.dataset.editNote) {
      const note = notes.find(n => n.id === b.dataset.editNote); if (!note) return;
      const draft={noteId:note.id,base_note:JSON.stringify(note),review_id:note.review_id || '',title:note.title,kind:note.kind,references:note.references,text:note.text};
      try { drafts=storeDraft(note.equipment,draft); } catch (_) { drafts[note.equipment]=draft; }
      route('notes',note.equipment);
    }
  });
  $('equipment-search').addEventListener('input', e => { state.listQuery = e.target.value; renderList(); });
  $('equipment-group').addEventListener('change', e => { state.group = e.target.value; renderList(); });
  $('context-summary').addEventListener('click', () => route('summary'));
  document.querySelector('.brand').addEventListener('click', e => { e.preventDefault(); route('overview'); });
  document.querySelector('.skip').addEventListener('click', e => { e.preventDefault(); $('workspace').focus(); $('workspace').scrollIntoView(); });
  $('document-print').addEventListener('click', () => {
    try { $('document-frame').contentWindow.focus(); $('document-frame').contentWindow.print(); }
    catch (_) { $('app-message').textContent = '자료 따로 열기에서 브라우저 인쇄를 사용해 주세요.'; }
  });
  function updateLayoutSearch(input) {
    const caret=input.selectionStart; state.layoutQuery=input.value; rememberLayoutScroll(); render();
    const search=$('layout-search'); search.focus({preventScroll:true}); search.setSelectionRange(caret,caret);
  }
  document.addEventListener('compositionend', e => {
    if(e.target.id==='layout-search') updateLayoutSearch(e.target);
  });
  document.addEventListener('input', e => {
    if(e.target.id==='layout-search') {
      if(!e.isComposing) updateLayoutSearch(e.target);
      return;
    }
    if (e.target.id === 'table-search') { state.tableQuery = e.target.value; renderRegister(); }
    if (e.target.id === 'review-search') { clearReviewFocus(); state.tableQuery = e.target.value; renderReviewRows(); }
    const form=e.target.closest('#note-form, #repair-record-form');
    if (form) {
      const fields = new FormData(form);
      const key=form.id==='repair-record-form'?repairRecords.keyFor(state.selected):state.selected;
      drafts[key] = Object.fromEntries(fields.entries());
      try { drafts=storeDraft(key,drafts[key]); } catch (_) { $('app-message').textContent = '임시 기록 저장 공간을 사용할 수 없습니다. 내용을 복사해 보관해 주세요.'; }
    }
  });
  document.addEventListener('change', e => {
    if (e.target.id === 'table-device') { state.tableDevice = e.target.value; renderRegister(); }
    if (e.target.id === 'review-scope') { clearReviewFocus(); state.tableDevice = e.target.value; renderReviewRows(); }
    if (e.target.id === 'review-kind') { clearReviewFocus(); state.reviewKind = e.target.value; renderReviewRows(); }
  });
  document.addEventListener('submit', async e => {
    if(e.target.matches('[data-standard-search]')){e.preventDefault();state.bc01Find=e.target.querySelector('input').value.trim().slice(0,160);route('manual');return;}
    if(e.target.matches('[data-bc01-search]') && state.view==='manual' && state.selected==='P01'){e.preventDefault();state.bc01Find=e.target.querySelector('input').value.trim().slice(0,160);bc01SearchLimit=20;route('manual');document.getElementById('bc01-find')?.focus({preventScroll:true});return;}
    if (!['note-form','repair-record-form'].includes(e.target.id)) return;
    e.preventDefault();
    if(savingNote)return;
    const isRepair=e.target.id==='repair-record-form';
    const fields = new FormData(e.target);
    const title = String(fields.get('title') || '').trim();
    const oldId = fields.get('noteId');
    const original = notes.find(n => n.id === oldId && n.equipment === state.selected);
    if (equipmentStatus(state.selected)?.status==='other_process_excluded_user_reported') return panel('현재 작업 대상에서 제외','<p>'+esc(equipmentStatus(state.selected).label)+' · 관련 조사·분석·보강 중단. 기존 기록 양식 데이터는 보존합니다.</p>');
    const schema=repairRecordMap.get(state.selected);
    if(isRepair && (!schema || !String(fields.get('first_symptom') || '').trim())){$('app-message').textContent='최초 증상을 입력해 주세요.';return;}
    const observation=isRepair?repairRecords.collect(schema,Object.fromEntries(fields.entries()),original?.repair_observation):null;
    const text = isRepair?repairRecords.summary(observation):String(fields.get('text') || '').trim();
    if (!title || !text) { $('app-message').textContent = '제목과 내용을 입력해 주세요.'; return; }
    const key=isRepair?repairRecords.keyFor(state.selected):state.selected;
    const draftBefore=drafts[key];
    const note = {id:original?.id || (crypto.randomUUID ? crypto.randomUUID() : `note-${Date.now()}-${Math.random().toString(36).slice(2)}`), equipment:state.selected,
      name:selection().name, title:title.slice(0,160), text:text.slice(0,30000),
      kind:isRepair?'수리·증상 기록':String(fields.get('kind') || '확인 사항'), references:isRepair?schema.manual:String(fields.get('references') || '').slice(0,500),
      review_id:reviewMap.has(fields.get('review_id'))?String(fields.get('review_id')):(original?.review_id || ''),updated:new Date().toISOString()};
    if(isRepair)note.repair_observation=observation;
    if(window.GMEEquipmentStandard.profile(data,state.selected)){const evidence=window.GMEEquipmentStandard.referenceContext(data,state.selected);note.saved_with={...original?.saved_with,...evidence,saved_at:note.updated,reference_scope:evidence.reference_scope.replace('generation','saving')};}
    savingNote=true;
    const submitButton=e.target.querySelector('button[type="submit"]');
    if(submitButton)submitButton.disabled=true;
    try {
      if(oldId && !original)throw new Error('note_conflict');
      noteStore.assertBase(original,String(fields.get('base_note') || ''));
      const save=()=>{
        const latest=noteStore.decodeNotes(localStorage.getItem(NOTES_KEY),validNoteEquipment);
        const next=noteStore.mergeNote(latest,original,note);
        const serialized=JSON.stringify(next);localStorage.setItem(NOTES_KEY,serialized);
        if(localStorage.getItem(NOTES_KEY)!==serialized)throw new Error('save_not_confirmed');
        notes=next;
      };
      if(navigator.locks?.request)await navigator.locks.request('gme-manual-notes-v1',save);else save();
      let cleanupFailed=false;
      if(drafts[key]===draftBefore){
        try { drafts=storeDraft(key,null,JSON.stringify(draftBefore)); }
        catch (_) { cleanupFailed=true; }
      }
      render(); $('app-message').textContent=`${note.name} ${isRepair?'수리 기록을':'메모를'} 이 브라우저에 저장했습니다.${cleanupFailed?' 임시 기록 정리는 확인 전입니다.':''}`;
    } catch (error) {
      $('app-message').textContent=error.message==='note_conflict'?`다른 탭에서 이 ${isRepair?'수리 기록이':'메모가'} 변경되었습니다. 작성 내용은 보존했습니다. 최신 기록을 다시 열어 비교해 주세요.`:'기록 저장을 확인하지 못했습니다. 작성 내용은 보존했습니다. 새 기록을 만들기 전 저장 목록을 확인해 주세요.';
    } finally {
      savingNote=false;
      if(submitButton?.isConnected)submitButton.disabled=false;
    }
  });
  const recordSnapshot=()=>{const raw=localStorage.getItem(NOTES_KEY);return {raw,notes:noteStore.decodeNotes(raw,validNoteEquipment)};};
  async function restoreRecords(expected,next,isCurrent,selectedKey=null){
    if(savingNote||!navigator.locks?.request)throw new Error('다른 저장 작업을 마친 후 다시 시도하세요.');
    savingNote=true;
    try{await navigator.locks.request('gme-manual-notes-v1',()=>{
      if(!isCurrent())throw new Error('복원 미리보기가 바뀌거나 닫혔습니다. 파일을 다시 선택하세요.');
      if(selectedKey!==null&&state.selected!==selectedKey)throw new Error('선택 설비가 바뀌었습니다. 해당 설비에서 다시 복원하세요.');
      if(localStorage.getItem(NOTES_KEY)!==expected)throw new Error('미리보기 이후 다른 탭에서 기록이 변경되었습니다. 파일을 다시 선택해 대조하세요.');
      const current=noteStore.decodeNotes(expected,validNoteEquipment);
      if(selectedKey!==null&&JSON.stringify(current.filter(n=>n.equipment!==selectedKey))!==JSON.stringify(next.filter(n=>n.equipment!==selectedKey)))throw new Error('다른 설비 기록의 변경을 차단했습니다.');
      const envelope=window.GMEBC01Tools.unifiedBackupEnvelope(next,data);
      window.GMEBC01Tools.parseUnifiedBackup(JSON.stringify(envelope,null,2),noteStore.decodeNotes,validNoteEquipment,data.repair_record_forms.profiles);
      const serialized=JSON.stringify(next);localStorage.setItem(NOTES_KEY,serialized);
      if(localStorage.getItem(NOTES_KEY)!==serialized)throw new Error('복원 저장을 확인하지 못했습니다. 새 복원 전 저장 목록과 백업을 대조하세요.');
      notes=noteStore.decodeNotes(localStorage.getItem(NOTES_KEY),validNoteEquipment);storageError='';lastRenderedRoute=null;
      $('app-message').textContent='기록 복원과 저장 후 재읽기를 확인했습니다. 임시 작성 내용은 유지했습니다.';
    });}catch(error){$('app-message').textContent=error.message;throw error;}finally{savingNote=false;}
  }
  window.GMEUnifiedBackup?.attach({data,validEquipment:validNoteEquipment,snapshot:recordSnapshot,restoreAll:restoreRecords,openNotes:()=>route('notes',state.selected)});
  window.GMEBC01Tools?.attach({data,base,validEquipment:validNoteEquipment,
    context:()=>({selected:state.selected,view:state.view,section:state.bc01Section,item:state.bc01Item,drawing:state.drawing,text:state.bc01Text}),
    snapshot:recordSnapshot,
    openRecords:()=>route('repair-record',state.selected),
    restore:async(expected,next,isCurrent)=>{
      const selectedKey=state.selected;
      if(!window.GMEEquipmentStandard.profile(data,selectedKey)?.tools.restore)throw new Error('선택 설비의 복원 도구가 없습니다.');
      await restoreRecords(expected,next,isCurrent,selectedKey);
    }
  });
  window.addEventListener('hashchange',readRoute);
  readRoute();
})();
