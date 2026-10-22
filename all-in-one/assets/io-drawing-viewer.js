/* Search-only full-page viewer. Coordinates never change the original PDF. */
(() => {
  'use strict';
  const M=window.GMEIOSearchModel,esc=M.escape;
  let dialog=null,returnFocus=null,generation=0,manifest=null;
  const pages=new Map();
  async function json(path){const r=await fetch(path);if(!r.ok)throw new Error('HTTP '+r.status);return r.json();}
  function close(){generation++;const focus=returnFocus;returnFocus=null;dialog?.close();dialog?.remove();dialog=null;if(focus?.isConnected)focus.focus({preventScroll:true});}
  async function open({url,query,allowed}){
    close();const token=++generation;returnFocus=document.activeElement;
    const [source,fragment='']=String(url).split('#'),page=Number(new URLSearchParams(fragment).get('page'));
    if(!allowed.has(source)||!Number.isInteger(page)||page<1)return;
    const d=document.createElement('dialog');dialog=d;d.className='io-drawing-dialog';d.setAttribute('aria-labelledby','io-drawing-title');
    d.innerHTML=`<div class="io-drawing-head"><div><h2 id="io-drawing-title">${esc(query)} · 도면 위치</h2><p>${esc(source.split('/').pop())} · PDF ${page}쪽</p></div><button type="button" data-drawing-close aria-label="도면 위치 닫기">닫기</button></div><div class="io-drawing-tools" role="group" aria-label="도면 확대와 일치 위치"><button type="button" data-drawing-action="previous" aria-label="이전 일치 위치">이전</button><button type="button" data-drawing-action="next" aria-label="다음 일치 위치">다음</button><button type="button" data-drawing-action="out" aria-label="도면 축소">−</button><button type="button" data-drawing-action="in" aria-label="도면 확대">+</button><button type="button" data-drawing-action="fit">전체 보기</button><a href="${esc(source+'#page='+page)}" target="_blank" rel="noopener">원본 PDF 열기 ↗</a></div><p class="io-drawing-status" role="status" aria-live="polite">도면과 글자 위치를 불러오는 중입니다.</p><div class="io-drawing-viewport" tabindex="0" aria-label="확대 도면. 가로·세로 스크롤, 더하기·빼기 확대, N 다음 위치"><div class="io-drawing-sheet"></div></div><p class="io-drawing-note">노란색은 검색어 위치입니다. OCR 위치는 오인식·오차가 있을 수 있으므로 원본을 확인하세요. +/− 확대 · N/P 다음/이전 · 0 전체 · Esc 닫기</p>`;
    document.body.append(d);d.showModal();
    d.querySelector('[data-drawing-close]').addEventListener('click',close);
    d.addEventListener('cancel',e=>{e.preventDefault();close();});
    const status=d.querySelector('.io-drawing-status'),viewport=d.querySelector('.io-drawing-viewport'),sheet=d.querySelector('.io-drawing-sheet');
    let hits=[],current=0,width=0,pageData=null;
    function center(){if(!hits.length)return;const b=hits[current].bbox;viewport.scrollTo({left:Math.max(0,(b[0]+b[2])/2*width-viewport.clientWidth/2),top:Math.max(0,(b[1]+b[3])/2*sheet.offsetHeight-viewport.clientHeight/2)});}
    function paint(){
      sheet.style.width=width+'px';sheet.querySelectorAll('.io-drawing-hit').forEach(x=>x.remove());
      hits.forEach((h,i)=>{const box=document.createElement('span'),b=h.bbox;box.className='io-drawing-hit'+(i===current?' is-current':'');box.style.left=Math.max(0,b[0]-.002)*100+'%';box.style.top=Math.max(0,b[1]-.003)*100+'%';box.style.width=(b[2]-b[0]+.004)*100+'%';box.style.height=(b[3]-b[1]+.006)*100+'%';box.setAttribute('aria-hidden','true');sheet.append(box);});
      status.textContent=hits.length?`${current+1} / ${hits.length}개 위치 · ${hits[current].text} · ${hits[current].method==='pdf-text'?'PDF 텍스트 위치':'OCR 후보 위치 · 원본 확인 필요'} · ${Math.round(width/pageData.width*100)}%`:'이 쪽에서 검색어 좌표를 확인하지 못했습니다. 전체 도면과 원본 PDF를 확인하세요.';
      for(const b of d.querySelectorAll('[data-drawing-action="previous"],[data-drawing-action="next"]'))b.disabled=hits.length<2;
    }
    function action(name){if(!pageData)return;
      if(name==='next'||name==='previous'){if(hits.length)current=(current+(name==='next'?1:hits.length-1))%hits.length;paint();center();}
      else if(name==='fit'){width=Math.max(240,Math.min(viewport.clientWidth-24,(viewport.clientHeight-24)*pageData.width/pageData.height));paint();viewport.scrollTo(0,0);}
      else {width=Math.max(240,Math.min(8000,width*(name==='in'?1.3:1/1.3)));paint();center();}
    }
    d.addEventListener('click',e=>{const name=e.target.closest('[data-drawing-action]')?.dataset.drawingAction;if(name)action(name);});
    d.addEventListener('keydown',e=>{const names={'+':'in','=':'in','-':'out','0':'fit','n':'next','N':'next','p':'previous','P':'previous'};if(names[e.key]){e.preventDefault();action(names[e.key]);}});
    try{
      if(!manifest)manifest=await json('registers/drawing-search-pages.json');if(token!==generation)return;
      const entry=manifest.pages.find(p=>p.source===source&&p.page===page);
      if(!entry||!allowed.has(entry.image)||!allowed.has(entry.data))throw new Error('Drawing location unavailable');
      pageData=pages.get(entry.key)||await json(entry.data);if(token!==generation)return;
      if(pageData.source!==source||pageData.page!==page||pageData.image!==entry.image)throw new Error('Page mismatch');pages.set(entry.key,pageData);
      hits=M.locate(pageData,query);
      const img=document.createElement('img');img.alt=`${source.split('/').pop()} PDF ${page}쪽 전체 도면`;img.src=entry.image;sheet.append(img);await img.decode();if(token!==generation)return;
      width=hits.length?Math.max(1800,Math.min(3200,viewport.clientWidth*2.6)):Math.max(240,Math.min(viewport.clientWidth-24,(viewport.clientHeight-24)*pageData.width/pageData.height));
      paint();requestAnimationFrame(()=>{if(token===generation)center();});
    }catch{if(token===generation){status.textContent='도면 위치를 불러오지 못했습니다. 위의 원본 PDF 열기를 이용하세요.';sheet.replaceChildren();}}
  }
  window.GMEIODrawingViewer={open,close};
})();
