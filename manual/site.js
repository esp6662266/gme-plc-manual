
'use strict';
const chapterSearch=document.querySelector('#chapter-search');
if(chapterSearch){
  const cards=[...document.querySelectorAll('.chapter-card')];
  chapterSearch.addEventListener('input',()=>{
    const q=chapterSearch.value.trim().toLocaleLowerCase();let count=0;
    for(const card of cards){const show=card.dataset.search.toLocaleLowerCase().includes(q);card.hidden=!show;if(show)count++;}
    document.querySelector('#search-count').textContent=count+'개 장을 표시합니다.';
    document.querySelector('#empty-result').hidden=count>0;
  });
}
const manualSearch=document.querySelector('#manual-search');
if(manualSearch){
  const article=document.querySelector('#manual-content');let index=-1;let marks=[];let lastQuery='';
  function clearMarks(){for(const mark of marks){mark.replaceWith(document.createTextNode(mark.textContent));}article.normalize();marks=[];index=-1;}
  function goNext(){if(!marks.length)return;index=(index+1)%marks.length;marks[index].scrollIntoView({behavior:'smooth',block:'center'});document.querySelector('#manual-count').textContent=(index+1)+' / '+marks.length+'개 결과';}
  function search(){
    clearMarks();const q=manualSearch.value.trim();lastQuery=q;const status=document.querySelector('#manual-count');
    if(!q){status.textContent='브라우저의 Ctrl+F로도 검색할 수 있습니다.';return;}
    const needle=q.toLocaleLowerCase();const walker=document.createTreeWalker(article,NodeFilter.SHOW_TEXT);const nodes=[];
    while(walker.nextNode()){const node=walker.currentNode;if(!node.parentElement.closest('script,style'))nodes.push(node);}
    for(const node of nodes){
      const value=node.nodeValue;const lower=value.toLocaleLowerCase();let pos=0;let next=lower.indexOf(needle);if(next<0)continue;
      const fragment=document.createDocumentFragment();
      while(next>=0){fragment.append(document.createTextNode(value.slice(pos,next)));const mark=document.createElement('mark');mark.textContent=value.slice(next,next+q.length);fragment.append(mark);marks.push(mark);pos=next+q.length;next=lower.indexOf(needle,pos);}
      fragment.append(document.createTextNode(value.slice(pos)));node.replaceWith(fragment);
    }
    status.textContent=marks.length+'개 결과';
  }
  let debounce;manualSearch.addEventListener('input',()=>{clearTimeout(debounce);debounce=setTimeout(search,180);});
  manualSearch.addEventListener('keydown',event=>{if(event.key==='Enter'){clearTimeout(debounce);if(manualSearch.value.trim()!==lastQuery)search();goNext();}});
  document.querySelector('#search-next').addEventListener('click',()=>{clearTimeout(debounce);if(!marks.length)search();goNext();});
  document.querySelector('#search-clear').addEventListener('click',()=>{clearTimeout(debounce);manualSearch.value='';search();manualSearch.focus();});
  const links=[...document.querySelectorAll('.reader-toc a')];
  const observer=new IntersectionObserver(entries=>{for(const entry of entries){if(entry.isIntersecting){for(const link of links)link.classList.toggle('active',link.hash==='#'+entry.target.id);}}},{rootMargin:'-100px 0px -65% 0px'});
  document.querySelectorAll('.chapter').forEach(section=>observer.observe(section));
}
