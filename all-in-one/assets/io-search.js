(() => {
  'use strict';
  const M=window.GMEIOSearchModel,esc=M.escape;
  const kinds={plc:'PLC 주소·심볼',circuit:'기능·전기 회로',signal:'신호 읽기·쓰기',hmi:'HMI 설정',reference:'도면 대조 설명',source:'도면 원문',manual:'매뉴얼 본문',ocr:'OCR 후보 · 원본 확인 필요'};
  const loader=window.GMEIOSearchLoader.create();
  let dispose=null;
  function cleanup(){dispose?.();dispose=null;}
  function attach(host,{data,onRouteChange}){
    cleanup();let active=true,timer=null,limit=30,lastTraceQuery=null;const selectedRoutes=new Map(),traceExpanded=new Map();
    const sidebar=document.querySelector('.sidebar'),menu=document.createElement('button');
    menu.type='button';menu.className='io-mobile-menu';menu.textContent='메뉴·설비 펼치기';menu.setAttribute('aria-expanded','false');
    menu.addEventListener('click',()=>{const open=sidebar.classList.toggle('io-menu-open');menu.setAttribute('aria-expanded',String(open));menu.textContent=open?'메뉴·설비 접기':'메뉴·설비 펼치기';});
    sidebar?.insertBefore(menu,sidebar.querySelector('nav'));
    dispose=()=>{active=false;clearTimeout(timer);unsubscribe();menu.remove();sidebar?.classList.remove('io-menu-open');window.GMEIODrawingViewer?.close();};
    const params=new URLSearchParams(location.hash.slice(1));
    let query=(params.get('q')||'').slice(0,160),equipment=params.get('search-equipment')||'',kind=params.get('search-kind')||'',includeCommon=params.get('search-common')!=='0';
    const equipmentMap=new Map(data.equipment.map(e=>[e.id,e]));
    if(!equipmentMap.has(equipment))equipment='';if(!kinds[kind])kind='';
    host.innerHTML=`<section class="panel io-search-panel" aria-labelledby="io-search-title"><h2 id="io-search-title">통합검색 · I/O·부품·선번</h2><p>부품 태그·선번·PLC 주소·기능명으로 도면과 매뉴얼 전체를 찾습니다. 확인된 기능 설명과 원문 문맥을 함께 보여줍니다.</p><form role="search" class="io-search-form"><label for="io-query">찾을 부품 태그·선번·주소·기능</label><div class="io-search-bar"><input id="io-query" name="q" type="search" maxlength="160" autocomplete="off" placeholder="예: 14KA6, 14KA10, 8.9, 8.10, 13.6, Q0.0" value="${esc(query)}"><button type="submit">검색</button></div><div class="io-search-filters"><label for="io-equipment">설비 범위<select id="io-equipment"><option value="">전체 설비 + 공통 도면·본문</option>${data.equipment.map(e=>'<option value="'+esc(e.id)+'">'+esc(e.id+' · '+e.name)+'</option>').join('')}</select></label><label for="io-kind">자료 구분<select id="io-kind"><option value="">전체 자료</option>${Object.entries(kinds).map(([k,v])=>'<option value="'+k+'">'+v+'</option>').join('')}</select></label></div><label class="io-common-label"><input id="io-common" type="checkbox"> 선택 설비 + 공통 회로·미배정 자료 함께</label></form><div class="io-examples" aria-label="검색 예시"><span>바로 검색</span>${['14KA6','14KA8','14KA10','8.9','8.10','13.6','Q0.0'].map(q=>'<button type="button" data-io-query="'+esc(q)+'">'+esc(q)+'</button>').join('')}</div><p class="io-index-status" role="status"></p></section><div class="io-result-status" role="status" aria-live="polite"></div><div class="io-search-suggestions"></div><div class="io-search-results"></div><div class="io-search-more"></div><section class="panel io-search-help"><h2>검색 결과를 읽는 방법</h2><p><strong>기능·회로 설명과 원본 표기를 함께 확인하세요. 도면 대조 설명은 원본 페이지를 읽고 정리한 자료이며, 도면 원문·매뉴얼 본문은 검색어 주변 문맥입니다.</strong> %Q0.0과 Q0.0, DB11,X0.0과 DB11.DBX0.0은 검색에서 같은 표기로 찾습니다. 여러 I/Q/M 주소는 공백으로 나누어 한 번에 찾을 수 있습니다.</p><p>백업 주소·과거 도면 주소·HMI 설정 주소는 각각 표시합니다. EW/AW와 I/Q, 원시 입력과 내부 처리 신호를 임의로 합치지 않습니다. 설비 연결은 기존 문서·페이지의 참조이며 공유 신호를 포함할 수 있습니다. 설비 필터에서도 공통 회로·미배정 자료를 기본으로 함께 찾습니다. 선택 설비만 볼 때는 체크를 해제하세요. 14KA6·14 KA6·14-KA6은 같은 태그로 찾으며 다른 번호는 합치지 않습니다.</p><p>현재값·현재 CPU 대응·현장 배선·정상 극성·복구 상태는 확인되지 않았습니다. 전체 도면에 OCR 검색을 보강했습니다. OCR 후보는 자동 인식 자료이며 기능이 확인된 설명이 아닙니다. 선번·세로 표기·스캔은 여전히 누락·오인식될 수 있습니다. “위치 보기”를 누르면 도면에서 검색어를 강조합니다. 검색 0건이 도면상 부재를 뜻하지 않습니다.</p></section>`;
    const $=s=>host.querySelector(s),input=$('#io-query'),eq=$('#io-equipment'),type=$('#io-kind'),common=$('#io-common');eq.value=equipment;type.value=kind;common.checked=includeCommon;common.disabled=!equipment;
    function save(){const p=new URLSearchParams(location.hash.slice(1));for(const [k,v]of [['q',query],['search-equipment',equipment],['search-kind',kind],['search-common',includeCommon?'':'0']]){if(v)p.set(k,v);else p.delete(k);}history.replaceState(null,'','#'+p);onRouteChange?.(p.toString());}
    const allowed=new Set(data.resources);
    function link(l,key,kind){const path=String(l.url||'').split('#')[0];if(!allowed.has(path))return '';return (path.endsWith('.pdf')&&/#page=\d+/.test(l.url)?'<button type="button" class="io-location-button" data-io-drawing="'+esc(l.url)+'" data-io-location-key="'+esc(key)+'" data-io-location-method="'+(kind==='ocr'?'ocr':'all')+'">'+esc(l.label.replace('원본 도면','도면').replace('전기도면','도면'))+' · 위치 보기</button>':'')+'<button type="button" data-doc="'+esc(l.url)+'">'+esc(l.label)+'</button>'; }
    const trace=r=>window.GMEIOConnections.render(r,{selectedRoute:selectedRoutes.get(r.id),expanded:traceExpanded.get(r.id),hash:location.hash,allowed,query});
    function restoreTraceFocus(prior){if(!prior||prior.isConnected)return;const focusKey=prior.dataset.ioFocusKey,key=prior.dataset.ioLocationKey,route=prior.dataset.ioTraceRoute;if(!focusKey&&!key&&!route)return;const replacement=Array.from(host.querySelectorAll(focusKey?'[data-io-focus-key]':key?'[data-io-location-key]':'[data-io-trace-route]')).find(el=>focusKey?el.dataset.ioFocusKey===focusKey:key?el.dataset.ioLocationKey===key:el.dataset.ioTraceRoute===route);(replacement||input).focus({preventScroll:true});}
    function draw(){
      if(!active||!host.isConnected)return;
      const traceQuery=M.normalize(query);if(traceQuery===lastTraceQuery)host.querySelectorAll('details[data-io-trace]').forEach(el=>traceExpanded.set(el.dataset.ioTrace,el.open));else traceExpanded.clear();lastTraceQuery=traceQuery;
      const {core,manual}=loader.states,index=core.value,needsManual=!kind||kind==='manual';
      const unavailable=core.status!=='ready'||(needsManual&&manual.status!=='ready');
      const loading=core.status==='loading'||(needsManual&&manual.status==='loading');
      $('.io-index-status').innerHTML=(index?Object.entries(index.counts).filter(([k])=>k!=='manual'||manual.status==='ready').map(([k,n])=>kinds[k]+' '+n.toLocaleString()+'건').join(' · '):'도면·I/O 검색 자료를 준비합니다.')+(needsManual&&manual.status==='loading'?' <strong>매뉴얼 본문을 추가로 불러오는 중입니다. 도착한 결과부터 표시합니다.</strong>':'')+(['core',...(needsManual?['manual']:[])].filter(k=>loader.states[k].status==='error').map(k=>' <span>'+(k==='core'?'도면·I/O':'매뉴얼 본문')+' 자료를 불러오지 못했습니다. '+esc(loader.states[k].error?.message||'')+'</span> <button type="button" data-io-retry="'+k+'">실패한 자료 다시 불러오기</button>').join(''));
      if(!M.terms(query).length){$('.io-result-status').textContent='주소·태그·기능을 2자 이상 입력하거나 위 예시를 누르세요.';$('.io-search-results').innerHTML='';$('.io-search-suggestions').innerHTML='';$('.io-search-more').innerHTML='';return;}
      const records=loader.records(kind),results=M.search(records,query,{equipment,kind,includeCommon});
      const suggestions=(!results.length||/^\d{1,3}[A-Z]{1,4}$/.test(M.normalize(query).trim()))?M.suggest(records,query):[];$('.io-search-suggestions').innerHTML=suggestions.length?'<p>등록된 태그 중 찾으시는 번호가 있나요? 번호를 확인하고 선택하세요.</p><div class="io-examples">'+suggestions.map(q=>'<button type="button" data-io-query="'+esc(q)+'">'+esc(q)+'</button>').join('')+'</div>':'';
      $('.io-result-status').textContent='“'+query+'” '+(unavailable?'현재 불러온 자료에서 ':'검색 결과 ')+results.length.toLocaleString()+'건'+(results.length>limit?' · '+limit+'건 표시':'')+(unavailable?(loading?' · 추가 자료 확인 중':' · 일부 자료 확인 필요'):'');
      const priorFocus=document.activeElement;
      $('.io-search-results').innerHTML=results.slice(0,limit).map(r=>`<article class="panel io-search-result"><div class="io-result-meta"><span class="badge">${esc(kinds[r.kind])}</span><span>${esc(r.equipment_names.join(' / ')||'공통·설비 미배정 자료')}</span></div><h3>${M.highlight(r.title,query)}</h3>${r.type?'<p class="io-result-type">자료형: '+esc(r.type)+'</p>':''}<p class="io-result-text">${M.highlight(['source','manual','ocr'].includes(r.kind)?M.snippet(r.text,query):r.text,query)}</p>${trace(r)}<p class="io-result-source">근거: ${esc(r.source)}</p>${r.status?'<p class="notice">'+esc(r.status)+'</p>':''}<p class="io-result-boundary">${esc(r.boundary)}</p><div class="inline-actions">${r.links.map((l,i)=>link(l,r.id+':source:'+i,r.kind)).join('')}${r.equipment.map(id=>{const p=data.priority.find(p=>p.plc_id===id),key=p?.key||id;return '<button type="button" data-view="io" data-equipment="'+esc(key)+'">'+esc(id)+' I/O·HMI 보기</button>';}).join('')}</div></article>`).join('')||(unavailable?'<section class="panel io-search-empty"><p>'+(loading?'검색 자료가 도착하면 결과가 이어서 표시됩니다.':'불러오지 못한 자료가 있습니다. 위의 다시 불러오기를 이용하세요.')+'</p></section>':'<section class="panel io-search-empty"><h3>일치하는 자료를 찾지 못했습니다.</h3><p>설비·자료 범위를 전체로 바꾸거나 원본의 번호와 표기를 확인해 주세요. 등록되지 않은 번호의 기능은 추정하지 않습니다.</p></section>');
      restoreTraceFocus(priorFocus);
      $('.io-search-more').innerHTML=results.length>limit?'<button type="button" data-io-more>결과 30건 더 보기</button>':'';
    }
    function run(){clearTimeout(timer);query=input.value.trim().slice(0,160);equipment=eq.value;kind=type.value;includeCommon=common.checked;common.disabled=!equipment;limit=30;save();draw();ensure();}
    $('form').addEventListener('submit',e=>{e.preventDefault();run();});
    input.addEventListener('input',e=>{if(e.isComposing)return;clearTimeout(timer);timer=setTimeout(run,180);});
    input.addEventListener('compositionend',()=>{clearTimeout(timer);timer=setTimeout(run,180);});
    eq.addEventListener('change',run);type.addEventListener('change',run);common.addEventListener('change',run);
    host.addEventListener('click',onClick);
    host.addEventListener('change',onTraceChange);
    host.addEventListener('toggle',onTraceToggle,true);
    const priorDispose=dispose;dispose=()=>{priorDispose();host.removeEventListener('click',onClick);host.removeEventListener('change',onTraceChange);host.removeEventListener('toggle',onTraceToggle,true);};
    function onTraceToggle(e){if(active&&host.contains(e.target)&&e.target.matches('details[data-io-trace]'))traceExpanded.set(e.target.dataset.ioTrace,e.target.open);}
    function onTraceChange(e){const select=e.target.closest('[data-io-trace-route]');if(!select)return;const id=select.dataset.ioTraceRoute,r=loader.states.core.value?.records.find(r=>r.id===id);if(!r)return;selectedRoutes.set(id,select.value);const container=select.closest('[data-io-trace]');traceExpanded.set(id,container.open);container.outerHTML=trace(r);restoreTraceFocus(select);}
    function onClick(e){const b=e.target.closest('button');if(!b)return;
      if(b.hasAttribute('data-io-drawing'))window.GMEIODrawingViewer.open({url:b.dataset.ioDrawing,query:b.dataset.ioLocationQuery||query,allowed,method:b.dataset.ioLocationMethod||'all',label:b.dataset.ioLocationLabel,focus:b.dataset.ioLocationFocus?.split(',').map(Number)});
      if(b.hasAttribute('data-io-query')){input.value=b.dataset.ioQuery;run();input.focus({preventScroll:true});}
      if(b.hasAttribute('data-io-more')){limit+=30;draw();}
      if(b.hasAttribute('data-io-retry'))loader.load(b.dataset.ioRetry,data.version).catch(()=>{});
    }
    function ensure(){if(!active)return;if(loader.states.core.status==='idle')loader.load('core',data.version).catch(()=>{});if(M.terms(query).length&&(!kind||kind==='manual')&&loader.states.core.status==='ready'&&loader.states.manual.status==='idle')loader.load('manual',data.version).catch(()=>{});}
    const unsubscribe=loader.subscribe(()=>{draw();ensure();});
    draw();ensure();
  }
  window.GMEIOSearch={attach,cleanup};
})();
