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
  const validNoteEquipment = new Set([...deviceMap.keys(),...priorityMap.keys()]);
  const base = new URL('./', location.href);
  const views = new Set(['overview','priority','summary','manual','repair','repair-record','io','spec','ladder','structure','drawings','simulator','tests','checks','conflicts','notes','resources','doc','review']);
  const deviceViews = new Set(['summary','manual','repair','repair-record','io','spec','ladder','structure','drawings','simulator','tests','checks','review']);
  const tabs = [['summary','설비 요약'],['manual','매뉴얼'],['repair','진단·수리'],['io','I/O·HMI'],['spec','제어 명세'],['ladder','래더'],['drawings','도면'],['simulator','시뮬레이터 · 개발 중지'],['tests','시험'],['checks','확인 대장']];
  tabs.splice(6,0,['structure','호출·신호 구조']);
  tabs.splice(3,0,['repair-record','수리 기록']);
  const labels = Object.fromEntries(tabs.concat([['overview','통합 현황'],['priority','공정 배치도·설비카드'],['notes','개선·작업 메모'],['resources','전체 자료'],['doc','자료 보기'],['conflicts','자료 불일치'],['review','근거 검토·확인']]));
  const state = {view:'overview', selected:'P01', scope:'priority', doc:'', listQuery:'', group:'', tableQuery:'', tableDevice:'', reviewKind:'', layoutMode:'map', layoutZoom:0.85, layoutQuery:'', layoutScroll:[0,0], renderId:0, drawing:'', drawingZoom:1, drawingWide:false};
  let lastRenderedRoute = null;
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
    const params = new URLSearchParams({view, equipment:selected, scope:nextScope});
    if (doc && validDoc(doc)) params.set('doc', doc);
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
    state.view = nextView;
    const key = params.get('equipment');
    state.selected = deviceMap.has(key) || priorityMap.has(key) ? key : 'P01';
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
    return `<section class="hero"><div><span class="eyebrow">GME / DECOATING WORKSPACE</span><h2>설비를 선택하고, 근거를 따라 확인합니다.</h2><p>매뉴얼부터 수리 진단, PLC 로직과 시험 자료까지 한곳에서 사용합니다. 우선23개를 먼저 완성합니다. 다른 공정2개를 제외한 현재21개에 집중하고, 전체248개는 참고 목록으로 보존합니다. 우선 대상 완료 후 필요한 항목을 추가합니다.</p></div><div class="hero-actions">${button('우선 23개 보기','priority')}${button('BC01 시작','summary','P01')}</div></section>
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
    if (window.GMESimulatorWorkspace) return window.GMESimulatorWorkspace.render(selection());
    const {d} = selection();
    return `<h2>시뮬레이터 · 같은 설비 명세로 준비합니다</h2><div class="notice">실행 엔진은 아직 구현하지 않았습니다. 이 화면은 연결 자료와 모델 준비 상태를 보여 줍니다. 운전·센서 주입·알람 재현은 동작 모델 검증 후 구현합니다.</div>
      <div class="trace"><span>입력·운전 요청</span><i>→</i><span>허가·인터록</span><i>→</i><span>상태·타이머</span><i>→</i><span>출력·장치 응답</span><i>→</i><span>피드백·알람</span></div>
      ${d ? panel(d.id+' · 준비 자료', `<div class="status-row"><span>I/O·HMI 참조</span><span class="badge good">연결됨</span></div><div class="status-row"><span>정적 조건 경로</span><span>${d.direct_rule_count}개</span></div><div class="status-row"><span>시험 설계</span><span>${d.test_count}개 · 미실행</span></div><div class="status-row"><span>실행 가능한 동작 모델</span><span class="badge pending">미구현</span></div><div class="status-row"><span>TIA·현장 실행 검증</span><span class="badge pending">미검증</span></div><div class="inline-actions">${button('동작 조건·순서 확인','spec')}${button('고장·복구 자료 확인','repair')}${button('시험 설계 확인','tests')}</div>`) : unknownPanel()}
      ${panel('첫 구현 대상', `<p>BC01·FN04의 정상 기동, 기동 피드백 없음, 인버터 이상, 운전 중 정지를 검토합니다. 원본 타이머·호출 순서·정상 극성을 먼저 확인하고 장치 응답 가정과 구분합니다.</p><div class="inline-actions">${button('BC01 준비 자료','simulator','P01')}${button('FN04 준비 자료','simulator','P02')}</div>`)}`;
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
      <div class="columns">${panel('메모 작성', `<form id="note-form" class="note-form"><input type="hidden" name="noteId" value="${esc(draft.noteId || '')}"><input type="hidden" name="base_note" value="${esc(draft.base_note || '')}"><input type="hidden" name="review_id" value="${esc(draft.review_id || '')}"><div class="form-row"><label>제목<input name="title" required maxlength="160" value="${esc(draft.title || '')}" placeholder="예: FN04 출력 주소 확인"></label><label>구분<select name="kind">${['확인 사항','수리·증상 기록','개선 후보','프로그램 분석'].map(v => `<option ${draft.kind === v ? 'selected' : ''}>${v}</option>`).join('')}</select></label></div><label>근거 위치<input name="references" maxlength="500" value="${esc(draft.references || '')}" placeholder="도면 FG, 래더 네트워크, I/O 주소"></label><label>내용<textarea name="text" required maxlength="30000" placeholder="관찰한 내용, 원인 후보, 확인할 작업과 결과를 기록합니다.">${esc(draft.text || '')}</textarea></label><div class="inline-actions"><button type="submit">브라우저에 저장</button><button type="button" data-export-notes>전체 메모 백업 (${notes.length})</button></div><p class="muted">작성 중 내용도 이 브라우저에 임시 보관합니다. 메모 저장은 시험 합격·수리 완료 처리가 아닙니다.</p></form>`)}
      ${panel(`저장된 메모 · ${own.length}건`, own.length ? own.map(n => `<article class="saved-note"><span class="badge">${esc(n.kind)}</span><h3>${esc(n.title)}</h3><small>${esc(n.updated)}${reviewMap.has(n.review_id) ? ' · 연결 검토 ' + esc(n.review_id) : ''}${n.references ? ' · '+esc(n.references) : ''}</small><p>${esc(n.text)}</p><button type="button" ${n.repair_observation?'data-edit-repair':'data-edit-note'}="${esc(n.id)}">${n.repair_observation?'이 수리 기록 수정':'이 메모 수정'}</button></article>`).join('') : '<div class="empty">이 설비에 저장된 메모가 없습니다.</div>')}</div>`;
  }
  function renderRepairRecord() {
    if (equipmentStatus(state.selected)?.status==='other_process_excluded_user_reported') return panel('현재 작업 대상에서 제외','<p>'+esc(equipmentStatus(state.selected).label)+' · 관련 조사·분석·보강 중단. 기존 기록 양식 데이터는 보존합니다.</p>');
    const schema=repairRecordMap.get(state.selected);
    if(!schema)return `<h2>수리 관찰 기록</h2><p>상세 기록 양식은 디코팅 우선23개에 연결되어 있습니다. 전체 목록의 기본 자료와 일반 작업 메모는 계속 사용할 수 있습니다.</p>${button('우선 설비 선택','priority')}${button('일반 작업 메모','notes')}`;
    const draft=drafts[repairRecords.keyFor(state.selected)] || {};
    const own=notes.filter(n=>n.equipment===state.selected && n.repair_observation).sort((a,b)=>b.updated.localeCompare(a.updated));
    return (storageError?`<div class="notice">${esc(storageError)}</div>`:'')+repairRecords.render(schema,draft,own);
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
    if (funcs[state.view]) { host.innerHTML = funcs[state.view](); if(state.view==='review')renderReviewRows(); if(state.view==='priority')restoreLayoutScroll(); }
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
      route('repair-record',note.equipment);
    } else if (b.dataset.exportRepair) {
      let latest;
      try{latest=noteStore.decodeNotes(localStorage.getItem(NOTES_KEY),validNoteEquipment);}catch(_){$('app-message').textContent='저장된 자료를 읽지 못했습니다. 기존 기록을 보존하고 확인해 주세요.';return;}
      const note=latest.find(n=>n.id===b.dataset.exportRepair);
      if(!note?.repair_observation)return;
      const payload={application:'GME All-in-One',exported:new Date().toISOString(),note_id:note.id,title:note.title,updated:note.updated,observation:note.repair_observation};
      const url=URL.createObjectURL(new Blob([JSON.stringify(payload,null,2)],{type:'application/json;charset=utf-8'}));
      const a=document.createElement('a');a.href=url;a.download=`GME-repair-${note.equipment}-${note.id}.json`;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
    }
    else if (b.dataset.reviewNote) startReviewNote(b.dataset.reviewNote);
    else if (b.dataset.reviewFocus) route('review',state.selected,'',b.dataset.reviewFocus);
    else if (b.hasAttribute('data-export-notes')) {
      try { notes=noteStore.decodeNotes(localStorage.getItem(NOTES_KEY),validNoteEquipment); }
      catch (_) { $('app-message').textContent='저장된 메모를 읽지 못해 백업을 만들지 않았습니다. 기존 저장 자료를 보존하고 확인해 주세요.'; return; }
      const payload = JSON.stringify({schema_version:1, application:'GME All-in-One', exported:new Date().toISOString(), notes}, null, 2);
      const url = URL.createObjectURL(new Blob([payload],{type:'application/json;charset=utf-8'}));
      const a = document.createElement('a'); a.href = url; a.download = `GME-work-notes-${new Date().toISOString().slice(0,10)}.json`; a.click();
      setTimeout(() => URL.revokeObjectURL(url),1000);
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
  window.addEventListener('hashchange',readRoute);
  readRoute();
})();
