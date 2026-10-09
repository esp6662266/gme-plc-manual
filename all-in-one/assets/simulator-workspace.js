/* Isolated source-network workbench plus two explicit virtual motor scenarios. */
(() => {
  'use strict';
  const model = window.GME_PROGRAM_MODEL, engine = window.GMEVirtualPLC;
  if (!model || !engine) return;
  const networkMap = new Map(model.networks.map(n => [n.id, n]));
  const sessions = new Map(), chosen = new Map(), modes = new Map();
  let timer = null, active = null;
  const esc = x => String(x ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const val = x => x === true ? '1' : x === false ? '0' : x === null || x === undefined ? '미확인' : String(x);
  const doc = (id, label) => `<button type="button" data-doc="networks/network-${id}.html">${esc(label || '원본 '+id)}</button>`;
  const table = (headers, rows) => `<div class="table-wrap"><table><thead><tr>${headers.map(h=>`<th>${esc(h)}</th>`).join('')}</tr></thead><tbody>${rows.map(row=>`<tr>${row.map(c=>`<td>${c}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;
  function cleanup() { if (timer !== null) clearInterval(timer); timer = null; active = null; }
  function numbers(ast, set = new Set()) {
    if (!ast || typeof ast !== 'object') return set;
    if (['eq','ne','gt','ge','lt','le'].includes(ast.op)) {
      if (ast.left?.op === 'read' && typeof ast.right?.value === 'number') set.add(ast.left.key);
      if (ast.right?.op === 'read' && typeof ast.left?.value === 'number') set.add(ast.right.key);
    }
    for (const v of Object.values(ast)) if (typeof v === 'object') { if (Array.isArray(v)) v.forEach(a=>numbers(a,set)); else numbers(v,set); }
    return set;
  }
  function machineFor(id, n) {
    const sk = id+':network:'+n.id;
    if (!sessions.has(sk)) sessions.set(sk, new engine.Machine([n]));
    return sessions.get(sk);
  }
  function motorFor(id) {
    const sk = id+':motor';
    if (!sessions.has(sk)) sessions.set(sk, new engine.MotorSession(model.profiles[id], networkMap));
    return sessions.get(sk);
  }
  function render(selection) {
    cleanup();
    const d = selection.d;
    if (!d) return `<h2>시뮬레이터 · ${esc(selection.name)}</h2><div class="notice">PLC 대응이 확인되지 않은 설비입니다. 임의의 모터·버너 로직을 대신 실행하지 않습니다. 대응 태그·제어 주체·연동 신호를 확인한 뒤 모델을 연결합니다.</div><button data-view="priority" type="button">대응표 보기</button>`;
    const profile = model.profiles[d.id];
    const mode = modes.get(d.id) || (profile ? 'motor' : 'network');
    const ids = model.equipment[d.id]?.networks || [];
    const normalized = x=>String(x).toLowerCase().replace(/[^a-z0-9]/g,'');
    if (!chosen.has(d.id)) chosen.set(d.id, profile?.networks.at(-1) || ids.find(id=>normalized(networkMap.get(id)?.title)===normalized(d.id)) || ids[0]);
    const n = networkMap.get(chosen.get(d.id));
    active = {id:d.id, profile, mode, n, host:null};
    return `<h2>가상 PLC 시뮬레이터 · ${esc(d.id)}</h2><div class="notice info">원본 LAD의 지원 명령을 가상 메모리에서 실행합니다. 전체 PLC 프로그램과 실제 장치 동작의 검증은 별도입니다. 미확인 신호는 0으로 바꾸지 않고 ‘미확인’으로 전달합니다.</div>
      ${selection.p ? `<div class="notice">${esc(selection.p.match==='candidate' ? '설비 대응 후보의 PLC 자료입니다.' : '태그명으로 연결한 PLC 자료입니다.')} 실물 동일성 확인 전입니다.</div>` : ''}
      <div class="inline-actions">${profile ? `<button type="button" data-sim-mode="motor" aria-pressed="${mode==='motor'}">가상 모터·고장 재현</button>` : ''}<button type="button" data-sim-mode="network" aria-pressed="${mode==='network'}">원본 네트워크 독립 시험</button><button type="button" data-view="structure">호출·신호 구조</button><button type="button" data-sim="export">실행 기록 다운로드</button></div>
      ${mode==='motor' && profile ? `<section class="panel"><h2>기본 HMI · 가상 ${esc(d.id)}</h2><div id="sim-status"></div><div class="inline-actions"><button type="button" data-sim="start">기동 요청</button><button type="button" data-sim="stop">정지 요청</button><button type="button" data-sim="ack">알람 리셋 펄스</button><button type="button" data-sim="tick">1초 진행</button><button type="button" data-sim="ten">20초 진행</button>${d.id==='FN04'?'<button type="button" data-sim="ninety">90분 진행 · 1초 간격</button>':''}<button type="button" data-sim="play">가상 시간 연속 진행</button><button type="button" data-sim="pause">일시 정지</button><button type="button" data-sim="reset">시험 초기 상태</button></div><label class="sim-fault">가상 장치 응답<select id="sim-fault">${[['normal','정상 응답 · 500ms 가정'],['no-feedback','운전 피드백 없음'],['inverter','인버터 이상 신호'],['feedback-stuck','운전 피드백 고착'],...(d.id==='BC01' ? [['tripwire','트립와이어 신호']] : [])].map(([v,t])=>`<option value="${v}">${t}</option>`).join('')}</select></label><p class="muted">복구 순서: 이상 주입 해제 → 필요한 외부 조건 복원 → 알람 리셋 → 기동 요청. 원본 리셋이 지속 고장 조건에서 동작하는지도 아래 기록으로 확인합니다.</p></section>
      <section class="panel"><h2>선택한 원본과 모델 범위</h2><div class="inline-actions">${profile.networks.map(id=>doc(id,`${networkMap.get(id).block} / ${id}`)).join('')}</div><ul>${profile.assumptions.map(s=>`<li>${esc(s)}</li>`).join('')}</ul><a href="${esc(model.semantics_sources[0].url)}" target="_blank" rel="noopener">Siemens SD 타이머 동작 근거 ↗</a></section>` : `<section class="panel"><h2>관련 원본 네트워크 선택</h2><p class="muted">공유·연관 네트워크도 포함됩니다. 목록의 모든 로직이 선택 설비 전용인 것은 아닙니다. 설비 제목과 실제 쓰기 대상을 함께 확인합니다.</p><label>네트워크<select id="sim-network">${ids.map(id=>{const x=networkMap.get(id);return `<option value="${id}" ${n?.id===id?'selected':''}>${esc(`${id} · ${x.block} · ${x.title || '제목 없음'} · ${x.executable?'독립 실행 지원':'실행 보류'}`)}</option>`}).join('')}</select></label>${n ? `<div class="inline-actions">${doc(n.id)}<button type="button" data-sim="scan" ${n.executable?'':'disabled'}>1회 평가</button><button type="button" data-sim="tick" ${n.executable?'':'disabled'}>1초 후 평가</button><button type="button" data-sim="zeros" ${n.executable?'':'disabled'}>0 시험 초기값 적용</button><button type="button" data-sim="reset">미확인 초기 상태</button></div><div class="notice">${n.executable ? '이 네트워크의 명령 부분집합을 독립 평가합니다. 입력은 사용자가 만든 시험 조건이며, 호출 문맥·네트워크 내부 쓰기 순서·다른 블록의 쓰기는 TIA 검증 전입니다.' : esc(n.blockers.join(' / ') || '실행 대상 쓰기 명령 없음')}</div><div id="sim-status"></div>` : '<p>직접 대응하는 원본 네트워크를 찾지 못했습니다.</p>'}</section>`}
      ${n || mode==='motor' ? `<section class="panel"><h2>시험 메모리 · 입력 조건 직접 주입</h2><p class="muted">BOOL의 0·1·미확인 또는 수치값을 지정합니다. 내부 Flag와 알람도 가상 시험을 위해 직접 주입할 수 있습니다. 실제 I/O와 온라인 값이 아닙니다.</p><div id="sim-inputs"></div></section><section class="panel"><h2>출력·타이머·쓰기 추적</h2><div id="sim-outputs"></div><div id="sim-timers"></div><div id="sim-trace"></div></section>`:''}`;
  }
  function current() {
    if (!active) return {};
    const session = active.mode==='motor' ? motorFor(active.id) : null;
    const machine = session?.machine || (active.n ? machineFor(active.id,active.n) : null);
    return {session,machine};
  }
  function paint() {
    if (!active?.host?.isConnected) return;
    const {machine:m,session:s} = current(); if (!m) return;
    const host = active.host, find = id=>host.querySelector('#'+id);
    const p = active.profile;
    const state = s ? m.read(p.fault)===true || m.read(p.inv_alarm)===true ? '알람 래치' : m.read(p.output)===true ? m.read(p.feedback)===true ? '가상 운전' : '피드백 대기' : m.read(p.output)===null ? '조건 미확인' : '정지' : '독립 네트워크 평가';
    const running = s && m.read(p.output)===true;
    find('sim-status').innerHTML = `<div class="sim-dashboard"><div class="sim-machine ${running?'running':''}"><span>✣</span></div><div><strong>${esc(state)}</strong><p>가상 시간 ${(m.time/1000).toFixed(1)}초 · 평가 ${m.scans}회 · ${timer===null?'일시 정지':'시간 진행 중'}</p>${s ? `<p>요청 ${val(m.read(p.command))} → Start ${val(m.read(p.output))} → 피드백 ${val(m.read(p.feedback))}</p>`:''}</div></div>`;
    const nets = s ? p.networks.map(id=>networkMap.get(id)) : [active.n];
    const allNames = new Map();
    for (const n of nets) for (const r of Object.values(n.refs)) if (r.name && !/^([+-]?\d+(\.\d+)?|(?:S5T|T|TIME)#|(?:2|8|10|16)#|TRUE$|FALSE$)/i.test(r.name)) allNames.set(engine.key(r.name),r.name);
    if (timer===null || !find('sim-inputs').querySelector('table')) find('sim-inputs').innerHTML = table(['원본 신호','시험값','주입'],[...allNames].map(([k,name])=>{
      const value=m.read(k),kind=value===null?'unknown':typeof value==='boolean'?'bool':'number';
      return [`<code>${esc(name)}</code>`, `<span class="sim-value ${value===true?'on':''}">${esc(val(value))}</span>`, `<div class="sim-inject"><select data-sim-input="${esc(k)}" aria-label="${esc(name)} 시험값">${[['unknown','미확인'],['false','BOOL 0'],['true','BOOL 1'],['number','수치값']].map(([v,t])=>`<option value="${v}" ${(kind==='unknown'&&v==='unknown'||kind==='number'&&v==='number'||value===true&&v==='true'||value===false&&v==='false')?'selected':''}>${t}</option>`).join('')}</select><input type="number" step="any" data-sim-number="${esc(k)}" aria-label="${esc(name)} 수치" value="${typeof value==='number'?value:''}" placeholder="수치"></div>`];
    }));
    find('sim-outputs').innerHTML = table(['네트워크·명령','쓰기 대상','조건','결과'],m.writes.map(w=>[doc(w.network,`${w.network} · ${w.gate}`),`<code>${esc(w.name)}</code>`,val(w.condition),`<strong>${esc(val(w.value))}</strong>`]));
    find('sim-timers').innerHTML = table(['타이머','시작 조건','경과 / 설정'],Object.entries(m.timers).map(([k,t])=>[`<code>${esc(k)}</code>`,val(t.active),`${t.elapsed===null?'미확인':(t.elapsed/1000).toFixed(1)+'초'} / ${t.preset===null?'미확인':t.preset/1000+'초'}`]));
    find('sim-trace').innerHTML = `<h3>최근 변화 · 최대 500건</h3>`+table(['가상 초','근거','신호 변화'],m.trace.slice(-40).reverse().map(w=>[(w.time/1000).toFixed(1),doc(w.network,`${w.network} / Part ${w.uid}`),`${esc(w.name)} · ${val(w.before)} → ${val(w.value)}`]));
    if (s && find('sim-fault')) find('sim-fault').value=s.fault;
  }
  function download() {
    const {machine,session}=current(); if(!machine)return;
    const payload={schema_version:1,model_version:model.version,engine_version:engine.version,equipment:active.id,scope:active.mode,network_ids:machine.networks.map(n=>n.id),exported:new Date().toISOString(),fault:session?.fault || '',plc_connected:false,tia_verified:false,assumptions:session?.profile.assumptions || ['독립 네트워크 평가 / XML Parts 쓰기 순서 가정'],snapshot:machine.snapshot()};
    const url=URL.createObjectURL(new Blob([JSON.stringify(payload,null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download=`GME-virtual-${active.id}-${active.mode}-${Date.now()}.json`;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
  }
  function mount(host, rerender) {
    if(!active)return;active.host=host;paint();
    host.onclick=e=>{
      const b=e.target.closest('button');if(!b)return;
      if(b.dataset.simMode){modes.set(active.id,b.dataset.simMode);rerender();return;}
      if(!b.dataset.sim)return;
      const {session:s,machine:m}=current();if(!m)return;
      const act=b.dataset.sim;
      try {
        if(act==='export')download();
        else if(act==='start'){s?.start();s?.step(0);}
        else if(act==='stop'){s?.stop();s?.step(0);}
        else if(act==='ack')s?.ack();
        else if(act==='scan')m.scan(0);
        else if(act==='tick')s?s.advance(1000):m.scan(1000);
        else if(act==='ten')s?.advance(20000);
        else if(act==='ninety')s?.advance(5400000,1000);
        else if(act==='play' && s && timer===null)timer=setInterval(()=>{s.advance(100);paint();},100);
        else if(act==='pause'){if(timer!==null)clearInterval(timer);timer=null;}
        else if(act==='reset'){if(timer!==null)clearInterval(timer);timer=null;sessions.delete(active.id+(s?':motor':':network:'+active.n.id));}
        else if(act==='zeros'){
          const nums=numbers(active.n.actions);const initial={};for(const name of [...active.n.reads,...active.n.writes])initial[name]=nums.has(name)?0:false;
          sessions.set(active.id+':network:'+active.n.id,new engine.Machine([active.n],initial));
        }
        paint();
      }catch(error){host.querySelector('#sim-status').textContent='평가 보류: '+error.message;}
    };
    host.onchange=e=>{
      if(e.target.id==='sim-network'){chosen.set(active.id,Number(e.target.value));rerender();return;}
      const {session:s,machine:m}=current();if(!m)return;
      if(e.target.id==='sim-fault'){s?.inject(e.target.value);s?.step(0);paint();return;}
      const name=e.target.dataset.simInput || e.target.dataset.simNumber;if(!name)return;
      if(e.target.dataset.simInput){const v=e.target.value;m.set(name,v==='true'?true:v==='false'?false:v==='number'?(typeof m.read(name)==='number'?m.read(name):0):null);}
      else {const input=e.target;const v=input.value.trim();m.set(name,v!==''&&Number.isFinite(Number(v))?Number(v):null);}
      paint();
    };
  }
  window.GMESimulatorWorkspace={render,mount,cleanup,model,networkMap};
})();
