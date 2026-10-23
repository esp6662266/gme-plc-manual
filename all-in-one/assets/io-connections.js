/* Display-only reviewed drawing paths. No live values or inferred connections. */
((root)=>{
  'use strict';
  const M=root.GMEIOSearchModel,esc=M.escape;
  const kinds={device:'기기',contact:'접점',coil:'코일',wire:'선번',terminal:'단자대·단자'};
  function relatedHash(hash,query){
    const p=new URLSearchParams(String(hash||'').replace(/^#/,''));
    for(const key of ['search-kind','search-equipment','search-common'])p.delete(key);
    p.set('view','io-search');p.set('q',query);return '#'+p;
  }
  function sourceNode(n,key,allowed,query){
    const source=String(n.url||'').split('#')[0],valid=allowed.has(source)&&source.endsWith('.pdf')&&/#page=[1-9]\d*$/.test(n.url);
    const text=`<span class="io-trace-node-kind">${esc(kinds[n.kind]||'도면 표기')}</span><span class="io-trace-node-main"><strong>${M.highlight(n.label,query)}</strong>${n.terminals?'<span class="io-trace-pins">'+esc(n.terminals)+'</span>':''}${n.detail?'<small>'+esc(n.detail)+'</small>':''}</span><span class="io-trace-node-source">FG ${esc(n.fg)} · PDF ${esc(n.page)}쪽<small>${esc(n.location_label)}</small></span>`;
    return valid?`<button type="button" data-io-drawing="${esc(n.url)}" data-io-location-query="${esc(n.query)}" data-io-location-method="all" data-io-location-label="${esc(n.label+(n.terminals?' · '+n.terminals:'')+' · '+n.location_label)}" data-io-location-key="${esc(key)}"${n.focus?' data-io-location-focus="'+esc(n.focus.join(','))+'"':''} aria-label="${esc(n.label+(n.terminals?' '+n.terminals:'')+' · PDF '+n.page+'쪽 '+n.location_label)}">${text}</button>`:`<span class="io-trace-unavailable">${text}</span>`;
  }
  function render(record,{selectedRoute='',expanded,hash='',allowed=new Set(),query=''}={}){
    const t=record.trace;if(record.kind!=='reference'||t?.basis!=='original_drawing_visual_comparison'||!t.routes?.length)return '';
    const route=t.routes.find(r=>r.id===selectedRoute)||t.routes[0],key=record.id,id='io-trace-'+key;
    const branch=t.parallel,open=expanded??M.terms(query).includes(M.normalize(record.address));
    return `<details class="io-trace-disclosure" data-io-trace="${esc(key)}"${open?' open':''}><summary data-io-focus-key="${esc(key)}:summary">${esc(record.address)} · 연결 경로 ${t.routes.length}개</summary><section class="io-trace" aria-labelledby="${esc(id)}"><div class="io-trace-heading"><h4 id="${esc(id)}">단자·선번 연결 추적</h4><span>${t.kind==='wire'?'선번':'부품'} · 보존 도면 대조</span></div>${t.coil?'<p class="io-trace-coil">코일 <b>A1</b> '+esc(t.coil.a1)+' <span>·</span> <b>A2</b> '+esc(t.coil.a2)+' <small>FG '+esc(t.coil.fg)+' · PDF '+esc(t.coil.page)+'쪽</small></p>':''}${t.routes.length>1?'<label class="io-trace-route-picker" for="'+esc(id)+'-route">볼 연결 경로<select id="'+esc(id)+'-route" data-io-trace-route="'+esc(key)+'">'+t.routes.map(r=>'<option value="'+esc(r.id)+'"'+(r.id===route.id?' selected':'')+'>'+esc(r.title)+'</option>').join('')+'</select></label>':'<h5 class="io-trace-route-title">'+esc(route.title)+'</h5>'}${route.description?'<p class="io-trace-description">'+esc(route.description)+'</p>':''}<p class="io-trace-note">각 항목을 누르면 원본 도면의 태그·선번 위치가 열립니다.</p><ol class="io-trace-path" aria-label="${esc(route.title+' 연결 순서')}">${route.nodes.map((n,i)=>'<li>'+sourceNode(n,key+':'+route.id+':'+i,allowed,query)+'</li>').join('')}</ol>${branch?'<section class="io-trace-parallel"><h5>'+esc(branch.title)+'</h5><p>아래 코일은 각각 병렬 분기입니다. 각 코일 A1은 13.6, A2는 공통 귀환에 연결됩니다.</p><ul aria-label="코일 병렬 분기">'+branch.nodes.map((n,i)=>'<li>'+sourceNode(n,key+':branch:'+i,allowed,query)+'</li>').join('')+'</ul><p class="io-trace-return">공통 귀환</p>'+sourceNode(branch.return_node,key+':return',allowed,query)+'</section>':''}<p class="io-trace-note">연결 순서는 보존 도면의 배선 경로를 나타냅니다. 위치 버튼은 도면에 인쇄된 태그·선번을 강조합니다.</p><nav class="io-trace-related" aria-label="관련 번호 전체 검색"><span>관련 번호 전체 검색</span>${t.related.map(q=>'<a href="'+esc(relatedHash(hash,q))+'">'+esc(q)+'</a>').join('')}</nav><details class="io-trace-unknown"><summary data-io-focus-key="${esc(key)}:unknown">현장 미확인 항목</summary><ul>${t.unknowns.map(text=>'<li>'+esc(text)+'</li>').join('')}</ul></details></section></details>`;
  }
  root.GMEIOConnections={render,relatedHash};
})(globalThis);
