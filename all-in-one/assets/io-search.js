(() => {
  'use strict';
  const M=window.GMEIOSearchModel,esc=M.escape;
  const kinds={plc:'PLC 주소·심볼',circuit:'기능·전기 회로',signal:'신호 읽기·쓰기',hmi:'HMI 설정'};
  let cached=null,pending=null,dispose=null;
  async function load(){
    if(cached)return cached;
    if(!pending)pending=fetch('registers/io-search-index.json').then(r=>{if(!r.ok)throw new Error('HTTP '+r.status);return r.json();}).then(x=>{if(x.schema_version!==1||!Array.isArray(x.records))throw new Error('검색 자료 형식 오류');cached=x;return x;}).finally(()=>{pending=null;});
    return pending;
  }
  function cleanup(){dispose?.();dispose=null;}
  function attach(host,{data}){
    cleanup();let active=true,timer=null,index=cached,failed=false,limit=30;
    dispose=()=>{active=false;clearTimeout(timer);};
    const params=new URLSearchParams(location.hash.slice(1));
    let query=(params.get('q')||'').slice(0,160),equipment=params.get('search-equipment')||'',kind=params.get('search-kind')||'';
    const equipmentMap=new Map(data.equipment.map(e=>[e.id,e]));
    if(!equipmentMap.has(equipment))equipment='';if(!kinds[kind])kind='';
    host.innerHTML=`<section class="panel io-search-panel" aria-labelledby="io-search-title"><h2 id="io-search-title">I/O·기능 검색</h2><p>주소·태그·기능명을 입력하면 설명과 관련 설비, 전기도면·LAD 근거를 함께 찾습니다.</p><form role="search" class="io-search-form"><label for="io-query">찾을 주소·태그·기능</label><div class="io-search-bar"><input id="io-query" name="q" type="search" maxlength="160" autocomplete="off" placeholder="예: Q0.0, IW394, bc01_fbk, 기동 명령" value="${esc(query)}"><button type="submit">검색</button></div><div class="io-search-filters"><label for="io-equipment">설비 범위<select id="io-equipment"><option value="">전체 설비 + 미배정 심볼</option>${data.equipment.map(e=>'<option value="'+esc(e.id)+'">'+esc(e.id+' · '+e.name)+'</option>').join('')}</select></label><label for="io-kind">자료 구분<select id="io-kind"><option value="">전체 자료</option>${Object.entries(kinds).map(([k,v])=>'<option value="'+k+'">'+v+'</option>').join('')}</select></label></div></form><div class="io-examples" aria-label="검색 예시"><span>바로 검색</span>${['Q0.0','I0.0','IW394','DB11,X0.0','bc01_fbk','기동 명령','19KA1'].map(q=>'<button type="button" data-io-query="'+esc(q)+'">'+esc(q)+'</button>').join('')}</div><p class="io-index-status" role="status"></p></section><div class="io-result-status" role="status" aria-live="polite"></div><div class="io-search-results"></div><div class="io-search-more"></div><section class="panel io-search-help"><h2>검색 결과를 읽는 방법</h2><p><strong>기능·회로 설명과 원본 표기를 함께 확인하세요.</strong> %Q0.0과 Q0.0, DB11,X0.0과 DB11.DBX0.0은 검색에서 같은 표기로 찾습니다. 여러 I/Q/M 주소는 공백으로 나누어 한 번에 찾을 수 있습니다.</p><p>백업 주소·과거 도면 주소·HMI 설정 주소는 각각 표시합니다. EW/AW와 I/Q, 원시 입력과 내부 처리 신호를 임의로 합치지 않습니다. 설비 연결은 기존 자료의 참조이며 공유 신호를 포함할 수 있습니다.</p><p>현재값·현재 CPU 대응·현장 배선·정상 극성·복구 상태는 확인되지 않았습니다. 텍스트로 등록되지 않은 스캔 도면의 표기는 검색되지 않을 수 있습니다.</p></section>`;
    const $=s=>host.querySelector(s),input=$('#io-query'),eq=$('#io-equipment'),type=$('#io-kind');eq.value=equipment;type.value=kind;
    function save(){const p=new URLSearchParams(location.hash.slice(1));for(const [k,v]of [['q',query],['search-equipment',equipment],['search-kind',kind]]){if(v)p.set(k,v);else p.delete(k);}history.replaceState(null,'','#'+p);}
    const allowed=new Set(data.resources);
    function link(l){const path=String(l.url||'').split('#')[0];return allowed.has(path)?'<button type="button" data-doc="'+esc(l.url)+'">'+esc(l.label)+'</button>':'';}
    function draw(){
      if(!active||!host.isConnected)return;
      $('.io-index-status').innerHTML=failed?'검색 자료를 불러오지 못했습니다. <button type="button" data-io-retry>다시 불러오기</button>':!index?'검색 자료를 불러오는 중입니다.':Object.entries(index.counts).map(([k,n])=>kinds[k]+' '+n.toLocaleString()+'건').join(' · ');
      if(!M.terms(query).length){$('.io-result-status').textContent='주소·태그·기능을 2자 이상 입력하거나 위 예시를 누르세요.';$('.io-search-results').innerHTML='';$('.io-search-more').innerHTML='';return;}
      if(!index){$('.io-result-status').textContent=failed?'자료를 다시 불러온 뒤 검색할 수 있습니다.':'“'+query+'” 검색 준비 중';return;}
      const results=M.search(index.records,query,{equipment,kind});
      $('.io-result-status').textContent='“'+query+'” 검색 결과 '+results.length.toLocaleString()+'건'+(results.length>limit?' · '+limit+'건 표시':'');
      $('.io-search-results').innerHTML=results.slice(0,limit).map(r=>`<article class="panel io-search-result"><div class="io-result-meta"><span class="badge">${esc(kinds[r.kind])}</span><span>${esc(r.equipment_names.join(' / ')||'설비 미배정 · 공통 원장')}</span></div><h3>${M.highlight(r.title,query)}</h3>${r.type?'<p class="io-result-type">자료형: '+esc(r.type)+'</p>':''}<p class="io-result-text">${M.highlight(r.text,query)}</p><p class="io-result-source">근거: ${esc(r.source)}</p>${r.status?'<p class="notice">'+esc(r.status)+' · 과거 자료 참조</p>':''}<p class="io-result-boundary">${esc(r.boundary)}</p><div class="inline-actions">${r.links.map(link).join('')}${r.equipment.map(id=>{const p=data.priority.find(p=>p.plc_id===id),key=p?.key||id;return '<button type="button" data-view="io" data-equipment="'+esc(key)+'">'+esc(id)+' I/O·HMI 보기</button>';}).join('')}</div></article>`).join('')||'<section class="panel io-search-empty"><h3>일치하는 자료를 찾지 못했습니다.</h3><p>설비·자료 범위를 전체로 바꾸거나 원본의 번호와 표기를 확인해 주세요. 등록되지 않은 번호의 기능은 추정하지 않습니다.</p></section>';
      $('.io-search-more').innerHTML=results.length>limit?'<button type="button" data-io-more>결과 30건 더 보기</button>':'';
    }
    function run(){clearTimeout(timer);query=input.value.trim().slice(0,160);equipment=eq.value;kind=type.value;limit=30;save();draw();}
    $('form').addEventListener('submit',e=>{e.preventDefault();run();});
    input.addEventListener('input',e=>{if(e.isComposing)return;clearTimeout(timer);timer=setTimeout(run,180);});
    input.addEventListener('compositionend',()=>{clearTimeout(timer);timer=setTimeout(run,180);});
    eq.addEventListener('change',run);type.addEventListener('change',run);
    host.addEventListener('click',onClick);
    const priorDispose=dispose;dispose=()=>{priorDispose();host.removeEventListener('click',onClick);};
    function onClick(e){const b=e.target.closest('button');if(!b)return;
      if(b.hasAttribute('data-io-query')){input.value=b.dataset.ioQuery;run();input.focus({preventScroll:true});}
      if(b.hasAttribute('data-io-more')){limit+=30;draw();}
      if(b.hasAttribute('data-io-retry')){failed=false;draw();fetchIndex();}
    }
    async function fetchIndex(){try{const value=await load();if(active){index=value;failed=false;draw();}}catch{if(active){failed=true;draw();}}}
    draw();if(!index)fetchIndex();
  }
  window.GMEIOSearch={attach,cleanup};
})();
