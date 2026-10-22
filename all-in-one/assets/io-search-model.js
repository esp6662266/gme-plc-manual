/* Search notation only; never converts current values or infers wiring. */
((root)=>{
  'use strict';
  const display=v=>String(v??'').normalize('NFKC');
  const normalize=v=>display(v).toUpperCase().replace(/%?DB\s*(\d+)\s*[.,]\s*(?:DB)?X\s*(\d+)\s*\.\s*(\d+)/g,'DB$1.DBX$2.$3').replace(/%?\b([IQM](?:B|W|D)?|T)\s*(\d+)(?:\s*\.\s*(\d+))?/g,(_,area,byte,bit)=>area+byte+(bit===undefined?'':'.'+bit));
  const escape=v=>display(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const terms=q=>normalize(q).trim().slice(0,160).split(/\s+/).filter(t=>t.length>=2).slice(0,12);
  const textCache=new WeakMap();
  function matcher(term){const p=term.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');return new RegExp(/\d/.test(term)?'(?<![A-Z0-9_.])'+p+'(?![A-Z0-9_.])':p,'i');}
  function rawMatcher(term){
    let m=/^DB(\d+)\.DBX(\d+)\.(\d+)$/.exec(term),pattern;
    if(m)pattern='%?DB\\s*'+m[1]+'\\s*[,\\.]\\s*(?:DB)?X\\s*'+m[2]+'\\s*\\.\\s*'+m[3];
    else if((m=/^([IQM](?:B|W|D)?|T)(\d+)(?:\.(\d+))?$/.exec(term)))pattern='%?'+m[1]+'\\s*'+m[2]+(m[3]===undefined?'':'\\s*\\.\\s*'+m[3]);
    return pattern?new RegExp('(?<![A-Z0-9_.])'+pattern+'(?![A-Z0-9_.])','i'):matcher(term);
  }
  function search(records,query,{equipment='',kind=''}={}){
    const ts=terms(query);if(!ts.length)return [];
    const ms=ts.map(matcher),addresses=ts.every(t=>/^(?:[IQM](?:B|W|D)?\d+(?:\.\d+)?|T\d+|DB\d+\.DBX\d+\.\d+)$/.test(t));
    return records.filter(r=>(!equipment||(r.equipment||[]).includes(equipment))&&(!kind||r.kind===kind)).map(r=>{
      let text=textCache.get(r);if(text===undefined){text=normalize([r.title,r.text,r.source,...r.equipment_names].join('\n'));textCache.set(r,text);}const hits=ms.filter(m=>m.test(text));
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
  root.GMEIOSearchModel={normalize,escape,terms,search,highlight,snippet};
})(globalThis);
