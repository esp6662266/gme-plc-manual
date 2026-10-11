/* Equipment profiles and reference metadata; no PLC execution or storage writes. */
((root) => {
  'use strict';
  const clone=v=>JSON.parse(JSON.stringify(v));
  function profile(data,key) {
    const entry=data.equipment_standards?.profiles.find(p=>p.priority_key===key);
    if(!entry)return null;
    return {...(entry.source_key ? data[entry.source_key] : entry),...entry};
  }
  function referenceContext(data,key='P01') {
    const p=profile(data,key);
    if(!p)throw new Error('이 설비의 자료·기록 도구는 아직 구현되지 않았습니다.');
    return {application_version:data.version,reference_scope:p.catalog_id+'('+key+') reference materials at generation; not observation-time proof',
      source_bundle_sha256:p.source_bundle_sha256,source_hashes:clone(p.source_hashes)};
  }
  const sections=[['overview','설비·자료 기준'],['io','I/O·HMI'],['control','제어 구조'],['circuits','전기 전달 경로'],['alarms','알람·복구'],['repair','증상별 수리'],['completion','완료 기준']];
  const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const list=values=>'<ul>'+values.map(v=>'<li>'+esc(v)+'</li>').join('')+'</ul>';
  const table=(headers,rows)=>'<div class="table-wrap"><table><thead><tr>'+headers.map(h=>'<th>'+esc(h)+'</th>').join('')+'</tr></thead><tbody>'+rows.map(r=>'<tr>'+r.map(v=>'<td>'+v+'</td>').join('')+'</tr>').join('')+'</tbody></table></div>';
  const detail=(title,data)=>'<details><summary>'+esc(title)+'</summary><pre class="standard-data">'+esc(JSON.stringify(data,null,2))+'</pre></details>';
  function items(data,key,section) {
    const p=profile(data,key);if(!p||p.source_key)return [];
    const drawing=data.drawing_workspace.profiles.find(p=>p.key===key),form=data.repair_record_forms.profiles.find(p=>p.key===key),s=p.specification,q=p.presentation;
    const make=(id,title,type,value,links=[])=>({id,title,type,value,links});
    if(section==='overview')return [make('identity',q.identity_title,'identity',s,[['설비 대응','priority-guides/'+key+'.html'],['기본 매뉴얼','devices/'+p.catalog_id+'.html']]),make('baseline','보존 자료·개정과 근거 묶음','baseline',p.source_hashes),make('boundary','확인 범위·불일치와 자료 대기','boundary',p.completion,[['미완료 항목','requirements-audit.html#open-'+key],['시공 자료','construction-guides/'+p.catalog_id+'.html']])];
    if(section==='io')return [['inputs','물리 입력'],['outputs','물리 출력'],['internal','내부·처리·기억 신호'],['hmi','HMI 보존 태그·주소']].map(([id,title])=>make(id,title,id,id==='internal'?p.signal_trace.signals.filter(s=>s.name.startsWith('Inputs.')||s.name.startsWith('Flag.')||p.internal_names.includes(s.name)):s[id],[['원시·처리/다른 쓰기','signal-guides/'+p.catalog_id+'.html'],['HMI 전달','hmi-transfer.html#profile-'+key]]));
    if(section==='control')return s.direct_rules.map(r=>make('rule-'+r.rule_id,r.rule_id+' · '+r['대상'],'rule',r)).concat([make('regulation',q.control_title,'regulation',p.control_reference,q.control_links)]);
    if(section==='circuits')return drawing.circuit.paths.map((path,i)=>make('path-'+i,path.signal,'circuit',{...path,destination:q.circuit_destination_by_signal?.[path.signal]??path.destination},[['회로·양단 근거','circuit-guides/'+p.catalog_id+'.html'],['시공·케이블','construction-guides/'+p.catalog_id+'.html']]));
    if(section==='alarms')return p.alarm.alarms.map((a,i)=>make('alarm-'+i,a.name+' · 발생/해제','alarm',a,[['알람 원본 분석','alarm-guides/'+p.catalog_id+'.html']])).concat([make('timer',q.timer_title,'timer',p.alarm.timers),make('related',q.related_title,'related',p.related_alarm_boundary,q.related_links)]);
    if(section==='repair')return form.steps.map(step=>make(step.id,step.title,'repair',{step,evidence:form.evidence_plan.steps.find(s=>s.step_id===step.id)},[['수리 판단 근거',form.manual],['기존 공통 쓰기','common-guides/'+key+'.html']]));
    if(section==='completion')return [make('document','문서·원본 연결과 부족 자료','document',p.completion),make('cpu','현재 PLC·HMI 대응','cpu',form.evidence_plan),make('field',q.field_title,'field',drawing),make('recovery','조치·원인 해소·재요청/실제 복구','recovery',form.evidence_plan),make('excluded','중지·제외 범위','excluded',null)];
    return [];
  }
  function normalize(data,key,params) {
    const section=sections.some(([s])=>s===params.get('section'))?params.get('section'):'overview',all=items(data,key,section);
    return {bc01Section:section,bc01Item:all.find(i=>i.id===params.get('item'))?.id||all[0]?.id||'',bc01Text:params.get('text')==='large'?'large':'standard',bc01Find:(params.get('find')||'').trim().slice(0,160)};
  }
  function condition(node) {
    if(!node)return '원문 조건 자료 대기';
    if(node.op==='read')return node.name||node.key;
    if(node.op==='const')return node.literal||String(node.value);
    if(node.op==='not')return 'NOT ['+condition(node.arg)+']';
    if(['and','or'].includes(node.op))return '('+node.args.map(condition).join(node.op==='and'?' AND ':' OR ')+')';
    if(node.op==='cmp')return '('+condition(node.left)+' '+node.cmp+' '+condition(node.right)+')';
    return JSON.stringify(node);
  }
  function searchValue(item,p,drawing,form) {
    const v=item.value;
    if(item.type==='identity')return [p.catalog_id,p.priority_key,p.specification.name,p.specification.group,p.specification.kind,p.specification.role,p.completion.boundary,drawing.circuit.equipment,drawing.circuit.distinction];
    if(['boundary','document'].includes(item.type))return [v.existing_notes,v.existing_pending,v.existing_review.map(r=>[r.title,r.next_check,r.source_status])];
    if(item.type==='regulation')return [v.chain,v.repair,v.pending,v.native_refs,v.native];
    if(item.type==='cpu')return v.preflight.requirements.filter(r=>r.owner!=='현장·설비 자료');
    if(item.type==='field')return [v.circuit.equipment,v.circuit.distinction,v.circuit.pending,v.warnings];
    if(item.type==='recovery')return v.steps.find(s=>s.step_id==='recovery');
    if(item.type==='excluded')return '시뮬레이터 영구 중지 실제 PLC 현장 보호값 SEJIN 변경 금지 MV04 SC12 PV04 EV87 GSS 85톤로 부모 보류7';
    return v;
  }
  function render(data,key,state) {
    const p=profile(data,key),s=p.specification,q=p.presentation,drawing=data.drawing_workspace.profiles.find(p=>p.key===key),form=data.repair_record_forms.profiles.find(p=>p.key===key);
    const available=new Set(data.resources),link=(label,path)=>available.has(path.split('#')[0])?'<button type="button" data-doc="'+esc(path)+'">'+esc(label)+'</button>':'<p>'+esc(label)+' · 자료 대기</p>';
    const links=rows=>'<div class="inline-actions">'+rows.map(([title,path])=>link(title,path)).join('')+'</div>';
    const routeButton=(title,view)=>'<button type="button" data-view="'+view+'" data-equipment="'+esc(key)+'">'+esc(title)+'</button>';
    const location=(network,kind,uid)=>p.source_locations.find(r=>r.network===Number(network)&&r.kind===kind&&r.uid===String(uid));
    const original=(network,uid)=>{const loc=location(network,'part',uid),n=s.networks.find(n=>Number(n['문서 ID'])===Number(network));return links([['LAD'+network+' · Part '+uid,loc?.path||'networks/network-'+network+'.html'],['원본 XML',loc?.xml||'sources/decoded-original/'+n?.['원본 XML']]]);};
    const action=a=>'<article class="bc01-rule"><h4>'+esc(a.gate+' · '+a.name)+'</h4><p><code>'+esc(condition(a.condition))+'</code></p>'+original(a.network,a.uid)+detail('Part·Wire·ORef/RID와 원본 참조',a)+'</article>';
    const all=items(data,key,state.bc01Section),current=all.find(i=>i.id===state.bc01Item)||all[0],v=current.value;let body='';
    if(current.type==='identity')body='<p>'+esc(s.role)+'</p>'+table(['구분','보존 자료·한계'],[['선택키 / PLC 태그',esc(key+' / '+p.catalog_id)],['백업 분류',esc(s.group+' · '+s.kind)],['관리 관계',esc(p.completion.boundary)],['도면 구동부',esc(drawing.circuit.equipment)],['실물 동일성',esc(q.identity_pending)]])+'<p>'+esc(drawing.circuit.distinction)+'</p>';
    else if(current.type==='baseline')body=table(['자료','기준·한계'],[['PLC','보존 백업과 복원 XML·UID/RID/NID 선언. 현재 프로젝트/CPU 비교 전'],['OEM 도면',esc(q.oem_baseline)],['시공 도면',esc(q.construction_baseline)],['P&ID','PID_1684n002I.pdf · 전체 공정 참고'],['HMI','보존 DDE 태그·주소 · 현재 이벤트/읽기/쓰기 확인 전']])+'<p>생성 시점의 참고 자료 묶음 SHA256: <code>'+esc(p.source_bundle_sha256)+'</code></p>'+table(['원본/대장','SHA256'],Object.entries(v).map(([path,hash])=>[link(path,path),'<code>'+hash+'</code>']));
    else if(current.type==='boundary'||current.type==='document')body=list(v.existing_notes.concat(v.existing_pending))+table(['차이/확인 항목','다음 근거','현재 상태'],v.existing_review.map(r=>[esc(r.title),esc(r.next_check),esc(r.source_status)]))+'<p>현재 자료·실물·복구 완료는 문서/정적 검사와 별도입니다.</p>';
    else if(current.type==='internal')body='<p>처리·요청·기억 신호와 Local 정지의 원본 범위를 구분합니다. Global 쓰기/Local 이름의 동일성·현재 전달·호출 순서는 미확정입니다.</p>'+v.map(signal=>'<article class="bc01-rule"><h4>'+esc(signal.name)+'</h4><p>'+esc(signal.addresses.join(' / ')||'주소 확인 대기')+'</p>'+table(['범위/역할','블록·LAD·핀','원본 Wire/선언'],signal.usages.map(u=>[esc(u.scope+' / '+u.role+' / '+u.role_basis),esc(u.block+' · LAD'+u.network+' · '+u.gate+'.'+u.pin),link('Wire'+u.wire,location(u.network,'wire',u.wire)?.path||'networks/network-'+u.network+'.html')+' '+link('원본 XML',u.file)+' '+u.declarations.map(d=>link(d.kind+' · '+d.scope,d.file)).join(' ')]))+detail('기존 신호 추적 원문·미해석 경계',signal)+'</article>').join('');
    else if(['inputs','outputs','hmi'].includes(current.type)){const fields=[...new Set(v.flatMap(r=>Object.keys(r)))];body='<p>물리/원시·처리·내부 요청·HMI를 구분합니다. 주소는 보존 대장값이며 현재 CPU/HMI 이벤트·읽기/쓰기·정상 극성은 확인 전입니다.</p>'+table(fields,v.map(row=>fields.map(f=>esc(typeof row[f]==='object'?JSON.stringify(row[f]):row[f]))));}
    else if(current.type==='rule')body=(v['블록']==='simulation'?'<div class="notice">보존 원본의 simulation 블록 정적 참조입니다. 물리 입력 전달·현장 응답의 증명이 아니며 실행하지 않습니다.</div>':'')+table(['항목','원본 정적 근거'],[['블록·규칙',esc(v['블록']+' / '+v.rule_id)],['대상·쓰기',esc(v['대상']+' / '+v['동작'])],['조건식','<code>'+esc(v['정적 조건식'])+'</code>'],['해석/경계',esc(v['내용']+' / '+v.execution_status)],['미해석',v.opaque?'ENO/out·호출 의미 미해석 유지':'직접 Wire 기반 연결 · 현재 실행 확인 전']])+original(v['네트워크 문서'],v['Part UID'])+detail('기존 직접 규칙 원문',v);
    else if(current.type==='regulation')body=list(v.chain)+'<h4>관찰·원인 배제</h4>'+list(v.repair)+'<h4>자료 대기</h4>'+list(v.pending)+detail('기존 원본 네트워크/텍스트 참조',v.native_refs)+links(v.native.map(n=>['LAD'+n,'networks/network-'+n+'.html']));
    else if(current.type==='circuit'){const sheet=drawing.sheets.find(s=>s.id==='oem-'+v.fg);body='<p>'+esc(v.drawing+' / '+v.backup)+'</p><ol>'+v.nodes.map(n=>'<li>'+esc(n)+'</li>').join('')+'</ol><p>'+esc(v.destination)+'</p><div class="notice">'+esc(v.check)+'</div>'+links([['FG'+v.fg+' · PDF'+sheet.page,sheet.source+'#page='+sheet.page]])+'<button type="button" data-drawing="'+esc(sheet.id)+'" class="bc01-preview"><img src="'+esc(sheet.image)+'" alt="'+esc(sheet.title)+'"><span>'+esc(sheet.title)+'</span></button>'+links(v.native_symbol_references.map(r=>['LAD'+r.network+' · ORef '+r.uid,'networks/network-'+r.network+'.html']))+detail('도면 신호의 원본 XML 참조',v.native_symbol_references);}
    else if(current.type==='alarm')body='<p>'+esc(p.alarm.note)+'</p>'+v.actions.map(action).join('')+'<h4>원인 제거·리셋·재요청·실제 응답을 나누어 확인</h4><p>'+esc(q.alarm_recovery)+'</p>';
    else if(current.type==='timer')body='<p>'+esc(p.alarm.note)+'</p>'+v.map(a=>'<p>보존 시간 원문: <code>'+esc(condition(a.preset))+'</code></p>'+action(a)).join('');
    else if(current.type==='related')body='<p>'+esc(v)+'</p>';
    else if(current.type==='repair')body=table(['단계','확인 작업'],[['관찰',esc(v.step.observe)],['비교·배제',esc(v.step.compare)],['다음 확인',esc(v.step.next)]])+table(['자료 수집 위치','필요 근거'],v.evidence.requirements.map(r=>[esc(r.owner),esc(r.work)]))+links(v.evidence.source_links.map(r=>[r.label,r.path]))+detail('관련 확인 대기·불일치',v.evidence.reviews)+routeButton('이 설비의 관찰 기록','repair-record');
    else if(current.type==='cpu')body=table(['수집 위치','대조할 자료'],v.preflight.requirements.filter(r=>r.owner!=='현장·설비 자료').map(r=>[esc(r.owner),esc(r.work)]))+'<p>현재 백업/온라인 프로젝트·호출·OB 주기·원시→처리·HMI 이벤트·복수쓰기 최종값을 비교한 자료가 필요합니다. 이 Mac 문서 검사는 TIA 컴파일/현재 CPU 검사가 아닙니다.</p>';
    else if(current.type==='field')body='<p>'+esc(v.circuit.equipment)+'</p><p>'+esc(v.circuit.distinction)+'</p>'+list(v.circuit.pending)+list(v.warnings)+links([['현행 설비·명판 대응','priority-guides/'+key+'.html'],['양단/케이블 차이','construction-guides/'+p.catalog_id+'.html']]);
    else if(current.type==='recovery'){const e=v.steps.find(s=>s.step_id==='recovery');body=table(['수집 위치','필요 근거'],e.requirements.map(r=>[esc(r.owner),esc(r.work)]))+links(e.source_links.map(r=>[r.label,r.path]))+'<p>기록자·시각/시간대·값/단위·측정장치·프로젝트·원본 위치·배제/조치·복구 증거를 남깁니다. 저장 기록은 자동 수리 완료 판정이 아닙니다.</p>'+routeButton('복구 관찰 기록','repair-record');}
    else if(current.type==='excluded')body='<p>시뮬레이터 작성·수정·생성·실행·행동 시험은 영구 중지입니다. 실제 PLC·현장·보호값 및 SEJIN 운영 자료를 변경하지 않습니다. MV04·SC12·PV04·실존 EV87·GSS/85톤로 제외와 부모 범위 보류7을 유지합니다.</p>';
    const index=all.indexOf(current),nav='<div class="bc01-item-nav"><span>'+esc((index+1)+' / '+all.length)+'</span>'+['prev','next'].map((dir,i)=>'<button type="button" data-standard-move="'+dir+'" '+(all[index+(i?1:-1)]?'':'disabled')+'>'+(i?'다음 항목':'이전 항목')+'</button>').join('')+'</div>';
    const query=state.bc01Find.normalize('NFKC').toLocaleLowerCase(),searchable=sections.flatMap(([section])=>items(data,key,section).map(item=>({section,...item}))),found=query?searchable.filter(i=>(i.title+' '+JSON.stringify(searchValue(i,p,drawing,form))).normalize('NFKC').toLocaleLowerCase().includes(query)):[];
    const search='<section class="bc01-search-panel"><form data-standard-search><label for="standard-find">'+esc(p.catalog_id)+' 매뉴얼 내부 검색</label><div class="inline-actions"><input id="standard-find" type="search" maxlength="160" value="'+esc(state.bc01Find)+'"><button type="submit">찾기</button><button type="button" data-standard-clear>지우기</button></div></form>'+(query?'<p>'+found.length+'개 일치 항목</p>'+found.map(i=>'<button type="button" data-standard-jump="'+esc(i.section+'/'+i.id)+'">'+esc(i.title)+'</button>').join(''):'<p>이 설비의 원본 태그·주소·조건·수리 내용을 찾습니다. 예: '+esc(q.search_examples)+'</p>')+'</section>';
    return '<div class="bc01-standard'+(state.standardWide?' bc01-wide':'')+(state.bc01Text==='large'?' bc01-large-text':'')+'"><div class="bc01-heading"><div><p class="eyebrow">'+esc(p.catalog_id)+' / GME-STD-1.0.0</p><h2>'+esc(p.catalog_id)+' · 표준 매뉴얼 작업실</h2><p>기존 완료 분석을7영역으로 연결합니다. 현재 CPU·실물·현장 복구는 확인 전입니다.</p></div><div class="inline-actions"><button data-standard-text="standard" aria-pressed="'+(state.bc01Text==='standard')+'">기본 글자</button><button data-standard-text="large" aria-pressed="'+(state.bc01Text==='large')+'">큰 글자</button><button data-standard-wide aria-pressed="'+!!state.standardWide+'">'+(state.standardWide?'목록·근거 함께 보기':'본문 넓게 보기')+'</button>'+routeButton('도면 작업실','drawings')+'</div></div>'+search+'<div class="bc01-kinds" role="group" aria-label="'+esc(p.catalog_id)+' 매뉴얼 종류">'+sections.map(([id,title])=>'<button data-standard-section="'+id+'" aria-pressed="'+(state.bc01Section===id)+'"><strong>'+esc(title)+'</strong><small>'+items(data,key,id).length+'개 세부 항목</small></button>').join('')+'</div><p class="bc01-mobile-hint">세부 항목 목록을 좌우로 밀어 선택하세요.</p><div class="bc01-layout"><nav class="bc01-library" aria-label="'+esc(p.catalog_id)+' 세부 항목"><h3>'+esc(sections.find(([id])=>id===state.bc01Section)[1])+'</h3>'+all.map(i=>'<button data-standard-item="'+esc(i.id)+'" aria-pressed="'+(i.id===current.id)+'">'+esc(i.title)+'</button>').join('')+'</nav><section class="bc01-content">'+nav+'<h3 id="standard-content-title" tabindex="-1">'+esc(current.title)+'</h3>'+body+links(current.links)+nav+'</section><aside class="bc01-evidence"><section class="panel"><h3>이 설비의 근거·기록</h3>'+links([['기본 자료','devices/'+p.catalog_id+'.html'],['제어 명세','control-specs/'+p.catalog_id+'.html'],['알람 분석','alarm-guides/'+p.catalog_id+'.html'],['자료 대기','requirements-audit.html#open-'+key]])+routeButton('관찰 기록','repair-record')+'</section><section class="panel"><h3>확인 경계</h3><p>'+esc(drawing.circuit.distinction)+'</p><p>문서·정적 근거·화면/저장·게시·TIA·현재CPU·현장복구 상태를 나누어 확인합니다.</p></section></aside></div></div>';
  }

  function highlight(host,query) {
    if(!query)return;
    const content=host.querySelector('.bc01-content'),walker=document.createTreeWalker(content,NodeFilter.SHOW_TEXT),nodes=[];
    while(walker.nextNode())if(!walker.currentNode.parentElement.closest('button,input,textarea,script,style,mark'))nodes.push(walker.currentNode);
    const needle=query.toLocaleLowerCase();
    for(const node of nodes){const text=node.textContent,lower=text.toLocaleLowerCase();if(!lower.includes(needle))continue;const frag=document.createDocumentFragment();let start=0,pos;while((pos=lower.indexOf(needle,start))>=0){frag.append(document.createTextNode(text.slice(start,pos)));const mark=document.createElement('mark');mark.textContent=text.slice(pos,pos+query.length);frag.append(mark);start=pos+query.length;}frag.append(document.createTextNode(text.slice(start)));node.replaceWith(frag);}
  }
  const api={profile,referenceContext,sections,items,normalize,render,highlight};
  root.GMEEquipmentStandard=api;
  if(typeof module!=='undefined'&&module.exports)module.exports=api;
})(typeof window!=='undefined'?window:globalThis);
