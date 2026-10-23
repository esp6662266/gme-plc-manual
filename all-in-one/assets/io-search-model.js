/* Search notation only; never converts current values or infers wiring. */
((root)=>{
  'use strict';
  const display=v=>String(v??'').normalize('NFKC');
  const normalize=v=>display(v).toUpperCase().replace(/(?<![A-Z0-9_.])(\d{1,3})[\s-]*([A-Z]{1,4})[\s-]*(\d{1,3})(?![A-Z0-9_.])/g,'$1$2$3').replace(/%?DB\s*(\d+)\s*[.,]\s*(?:DB)?X\s*(\d+)\s*\.\s*(\d+)/g,'DB$1.DBX$2.$3').replace(/%?\b([IQM](?:B|W|D)?|T)\s*(\d+)(?:\s*\.\s*(\d+))?/g,(_,area,byte,bit)=>area+byte+(bit===undefined?'':'.'+bit)).replace(/(?<![A-Z0-9_.])\d+(?:\s*\.\s*\d+)+(?![A-Z0-9_.])/g,v=>v.replace(/\s/g,''));
  const escape=v=>display(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const terms=q=>{let text=normalize(q).trim().slice(0,160);const intent=/^(?:용도|기능|쓰임새|무슨|뭐야|뭔가요|무엇인지|알려줘|찾아줘|검색|의)$/;if(/(?:\d+[A-Z]+\d+|[IQM]\d+\.\d+|\d+\.\d+)/.test(text))text=text.replace(/(\d)(용도|기능|쓰임새)/g,'$1 $2');const ts=text.split(/\s+/).filter(t=>t.length>=2);return (ts.some(t=>/\d/.test(t))?ts.filter(t=>!intent.test(t)):ts).slice(0,12);};
  const textCache=new WeakMap();
  function matcher(term){const p=term.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');return new RegExp(/\d/.test(term)?'(?<![A-Z0-9_.])'+p+'(?![A-Z0-9_.])':p,'i');}
  function rawMatcher(term){
    let m=/^DB(\d+)\.DBX(\d+)\.(\d+)$/.exec(term),pattern;
    if(m)pattern='%?DB\\s*'+m[1]+'\\s*[,\\.]\\s*(?:DB)?X\\s*'+m[2]+'\\s*\\.\\s*'+m[3];
    else if((m=/^(\d{1,3})([A-Z]{1,4})(\d{1,3})$/.exec(term)))pattern=m[1]+'[\\s-]*'+m[2]+'[\\s-]*'+m[3];
    else if((m=/^([IQM](?:B|W|D)?|T)(\d+)(?:\.(\d+))?$/.exec(term)))pattern='%?'+m[1]+'\\s*'+m[2]+(m[3]===undefined?'':'\\s*\\.\\s*'+m[3]);
    else if((m=/^(\d+)\.(\d+)$/.exec(term)))return new RegExp('(?<![A-Z0-9_.])(?<!\\d\\s*\\.\\s*)'+m[1]+'\\s*\\.\\s*'+m[2]+'(?![A-Z0-9_.]|\\s*\\.\\s*\\d)','i');
    return pattern?new RegExp('(?<![A-Z0-9_.])'+pattern+'(?![A-Z0-9_.])','i'):matcher(term);
  }
  function search(records,query,{equipment='',kind='',includeCommon=true}={}){
    const ts=terms(query);if(!ts.length)return [];
    const ms=ts.map(matcher),addresses=ts.every(t=>/^(?:[IQM](?:B|W|D)?\d+(?:\.\d+)?|T\d+|DB\d+\.DBX\d+\.\d+)$/.test(t));
    return records.filter(r=>(!equipment||(r.equipment||[]).includes(equipment)||(includeCommon&&!(r.equipment||[]).length))&&(!kind||r.kind===kind)).map(r=>{
      let text=textCache.get(r);if(text===undefined){text=normalize([r.title,r.text,r.source,...(r.equipment_names||[])].join('\n'));textCache.set(r,text);}const hits=ms.filter(m=>m.test(text));
      if(addresses?!hits.length:hits.length!==ms.length)return null;
      const exact=normalize(r.address).split(/\s*\/\s*/).some(a=>ts.includes(a.trim()));
      return {...r,score:(exact?1000:0)+(r.kind==='reference'?400:r.kind==='circuit'?300:0)+hits.length*10};
    }).filter(Boolean).sort((a,b)=>b.score-a.score||a.id.localeCompare(b.id));
  }
  // Highlight normalized notation, with all user/source text escaped before HTML.
  function highlight(value,query){let rest=display(value),out='',guard=0;const ms=terms(query).map(rawMatcher);
    while(rest&&guard++<80){const hits=ms.map(m=>m.exec(rest)).filter(Boolean).sort((a,b)=>a.index-b.index);if(!hits.length)break;const h=hits[0];out+=escape(rest.slice(0,h.index))+'<mark>'+escape(h[0])+'</mark>';rest=rest.slice(h.index+h[0].length);}return out+escape(rest);
  }
  function snippet(value,query,length=460){const text=display(value),hits=terms(query).map(t=>text.search(rawMatcher(t))).filter(i=>i>=0),start=Math.max(0,(hits.length?Math.min(...hits):0)-110);return (start?'…':'')+text.slice(start,start+length)+(start+length<text.length?'…':'');}
  const tagCache=new WeakMap();
  function suggest(records,query){
    const q=terms(query)[0]||'';if(!/^(?:\d+[A-Z]*\d*|[IQM]\d+(?:\.\d*)?)$/.test(q))return [];
    let tags=tagCache.get(records);if(!tags){tags=[...new Set(records.flatMap(r=>(normalize([r.address,r.title,r.text].join(' ')).match(/(?<![A-Z0-9_.])(?:\d{1,3}[A-Z]{1,4}\d{1,3}|[IQM]\d+\.\d+)(?![A-Z0-9_.])/g)||[])))].sort();tagCache.set(records,tags);}
    const distance=(a,b)=>{let row=Array.from({length:b.length+1},(_,i)=>i);for(let i=1;i<=a.length;i++){let next=[i];for(let j=1;j<=b.length;j++)next[j]=Math.min(next[j-1]+1,row[j]+1,row[j-1]+(a[i-1]===b[j-1]?0:1));row=next;}return row[b.length];};
    return tags.filter(t=>t!==q).map(t=>({tag:t,score:t.startsWith(q)?0:distance(q,t)})).filter(t=>t.score<=1).sort((a,b)=>a.score-b.score||a.tag.length-b.tag.length||a.tag.localeCompare(b.tag)).slice(0,6).map(t=>t.tag);
  }
  function locate(page,query,{method='all'}={}){const ms=terms(query).map(rawMatcher),hits=[];
    const words=method==='ocr'?[]:(page.words||[]),ocr=method==='pdf-text'?[]:(page.ocr||[]).filter(w=>Number.isFinite(w.confidence)&&w.confidence>=0.7);
    for(const w of [...words,...ocr]){const b=w.bbox;if(!Array.isArray(b)||b.length!==4||b.some(n=>!Number.isFinite(n)||n<0||n>1.001)||b[0]>=b[2]||b[1]>=b[3]||!ms.some(m=>m.test(display(w.text))))continue;
      if(hits.some(h=>normalize(h.text)===normalize(w.text)&&Math.min(h.bbox[2],b[2])>Math.max(h.bbox[0],b[0])&&Math.min(h.bbox[3],b[3])>Math.max(h.bbox[1],b[1])&&Math.abs((h.bbox[0]+h.bbox[2]-b[0]-b[2])/2)<.012&&Math.abs((h.bbox[1]+h.bbox[3]-b[1]-b[3])/2)<.012))continue;
      hits.push(w);
    }return hits.sort((a,b)=>a.bbox[1]-b.bbox[1]||a.bbox[0]-b.bbox[0]);
  }
  function nearest(hits,point){if(!Array.isArray(point)||point.length!==2||point.some(n=>!Number.isFinite(n)||n<0||n>1))return 0;let best=Infinity,index=0;hits.forEach((hit,i)=>{const b=hit.bbox,d=((b[0]+b[2])/2-point[0])**2+((b[1]+b[3])/2-point[1])**2;if(d<best){best=d;index=i;}});return index;}
  root.GMEIOSearchModel={normalize,escape,terms,search,highlight,snippet,suggest,locate,nearest};
})(globalThis);
