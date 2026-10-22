/* Search notation only; never converts current values or infers wiring. */
((root)=>{
  'use strict';
  const display=v=>String(v??'').normalize('NFKC');
  const normalize=v=>display(v).toUpperCase().replace(/%?DB\s*(\d+)\s*[.,]\s*(?:DB)?X\s*(\d+)\s*\.\s*(\d+)/g,'DB$1.DBX$2.$3').replace(/%?\b([IQM](?:B|W|D)?|T)\s*(\d+)(?:\s*\.\s*(\d+))?/g,(_,area,byte,bit)=>area+byte+(bit===undefined?'':'.'+bit));
  const escape=v=>display(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const terms=q=>normalize(q).trim().slice(0,160).split(/\s+/).filter(t=>t.length>=2).slice(0,12);
  function matcher(term){const p=term.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');return new RegExp(/\d/.test(term)?'(?<![A-Z0-9_.])'+p+'(?![A-Z0-9_.])':p,'i');}
  function search(records,query,{equipment='',kind=''}={}){
    const ts=terms(query);if(!ts.length)return [];
    const ms=ts.map(matcher),addresses=ts.every(t=>/^(?:[IQM](?:B|W|D)?\d+(?:\.\d+)?|T\d+|DB\d+\.DBX\d+\.\d+)$/.test(t));
    return records.filter(r=>(!equipment||(r.equipment||[]).includes(equipment))&&(!kind||r.kind===kind)).map(r=>{
      const text=normalize([r.title,r.text,r.source,...r.equipment_names].join('\n')),hits=ms.filter(m=>m.test(text));
      if(addresses?!hits.length:hits.length!==ms.length)return null;
      const exact=normalize(r.address).split(/\s*\/\s*/).some(a=>ts.includes(a.trim()));
      return {...r,score:(exact?1000:0)+(r.kind==='circuit'?300:0)+hits.length*10};
    }).filter(Boolean).sort((a,b)=>b.score-a.score||a.id.localeCompare(b.id));
  }
  // Highlight normalized notation, with all user/source text escaped before HTML.
  function highlight(value,query){let rest=display(value),out='',guard=0;const ms=terms(query).map(matcher);
    while(rest&&guard++<80){const hits=ms.map(m=>m.exec(rest)).filter(Boolean).sort((a,b)=>a.index-b.index);if(!hits.length)break;const h=hits[0];out+=escape(rest.slice(0,h.index))+'<mark>'+escape(h[0])+'</mark>';rest=rest.slice(h.index+h[0].length);}return out+escape(rest);
  }
  root.GMEIOSearchModel={normalize,escape,terms,search,highlight};
})(globalThis);
