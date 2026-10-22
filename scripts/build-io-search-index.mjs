import { readFile, writeFile } from 'node:fs/promises';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';
import { gunzipSync } from 'node:zlib';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
export const inputs = ['registers/all-in-one-data.json','registers/plc-symbols.csv','registers/signal-trace.json','registers/electrical-trace.json','registers/hmi-transfer.json'];
// RFC 4180 fields, including quoted commas, embedded newlines and doubled quotes.
export function csv(text) {
  const rows=[];let row=[],field='',quoted=false;
  for(let i=0;i<text.length;i++) {const c=text[i];
    if(c==='"'){if(quoted&&text[i+1]==='"'){field+='"';i++;}else quoted=!quoted;}
    else if(!quoted&&(c===','||c==='\n')){row.push(field.replace(/\r$/,''));field='';if(c==='\n'){rows.push(row);row=[];}}
    else field+=c;
  }
  if(field||row.length){row.push(field.replace(/\r$/,''));rows.push(row);}
  const header=rows.shift().map(x=>x.replace(/^\uFEFF/,''));
  return rows.filter(r=>r.some(Boolean)).map(r=>Object.fromEntries(header.map((h,i)=>[h,r[i]||''])));
}
export async function buildIndex(directory=root) {
  const contents=await Promise.all(inputs.map(p=>readFile(resolve(directory,'all-in-one',p),'utf8')));
  const [data,,trace,electrical,hmi]=contents.map((v,i)=>i===1?null:JSON.parse(v));
  const symbols=csv(contents[1]),equipment=new Map(data.equipment.map(e=>[e.id,e])),records=[],refs=new Map();
  for(const e of data.equipment)for(const key of ['inputs','outputs','internal'])for(const s of e[key]){
    const id=s['원본 심볼'].toLowerCase();if(!refs.has(id))refs.set(id,[]);if(!refs.get(id).includes(e.id))refs.get(id).push(e.id);
  }
  const overrides=JSON.parse(await readFile(resolve(directory,'docs/equipment-standard/SCOPE-OVERRIDES.json'),'utf8'));
  const statuses=new Map((data.equipment_status_notes||[]).filter(x=>x.id).map(x=>[x.id,x.label]));
  for(const e of overrides.equipment)statuses.set(e.catalog_id,e.reason);
  const decorate=r=>({...r,equipment_names:(r.equipment||[]).map(id=>id+' · '+(equipment.get(id)?.name||id)),status:(r.equipment||[]).map(id=>statuses.get(id)).filter(Boolean).join(' / ')});
  for(const [i,s]of symbols.entries()){
    const eq=refs.get(s['원본 심볼'].toLowerCase())||[];
    records.push(decorate({id:'plc-'+i,kind:'plc',address:s['백업 주소'].toUpperCase(),symbol:s['원본 심볼'],title:[s['백업 주소'].toUpperCase(),s['원본 심볼']].filter(Boolean).join(' · '),text:s['설명']||'원본 설명 없음 · 관련 신호·도면에서 기능을 확인하세요.',type:s['자료형'],equipment:eq,source:'보존 PLC 심볼 원장 · 문서 ID '+s['문서 ID'],links:[{url:'plc-symbols.html',label:'PLC 심볼 원장'},{url:'registers/plc-symbols.csv',label:'원본 추출 CSV'}],boundary:'백업 주소·원본 주석입니다. 설비 참조에는 공유 신호가 포함되며 현재 CPU·배선은 미확인입니다.'}));
  }
  for(const e of electrical.devices)for(const [i,p]of e.paths.entries()){
    const page=Number(p.fg)+(Number(p.fg)>5?1:0)+(Number(p.fg)>180?2:0);
    records.push(decorate({id:'circuit-'+e.id+'-'+i,kind:'circuit',address:p.backup||'',symbol:p.drawing||'',title:p.signal+' · '+(p.backup||p.drawing),text:['기능: '+p.signal,'도면 표기: '+p.drawing,'경로: '+p.nodes.join(' → '),'연결 설명: '+p.destination,'확인 사항: '+p.check,e.distinction].filter(Boolean).join('\n'),equipment:[e.id],source:'Electrical_Rev2.pdf · FG '+p.fg+' / PDF '+page+'쪽',links:[{url:electrical.source+'#page='+page,label:'전기도면 '+page+'쪽'},{url:'circuit-guides/'+e.id+'.html',label:'설비 회로 설명'},...(p.native_symbol_references||[]).slice(0,4).map(u=>({url:'networks/network-'+u.network+'.html',label:'LAD '+u.network}))],boundary:'기존 도면 정적 해석입니다. 과거 도면 표기와 백업 주소를 구분하며 정상 극성·현행 결선·복구를 확정하지 않습니다.'}));
  }
  for(const e of trace.devices)for(const [i,s]of e.signals.entries()){
    const usages=s.usages.filter(u=>!u.legacy_simulation_block);
    if(!usages.length)continue;
    records.push(decorate({id:'signal-'+e.id+'-'+i,kind:'signal',address:s.addresses.join(' / '),symbol:s.name,title:[s.addresses.join(' / '),s.name].filter(Boolean).join(' · '),text:usages.slice(0,14).map(u=>(u.scope||'미확정')+' · '+(u.role==='read'?'읽기':u.role==='write'?'쓰기':'방향 미확정')+' · LAD '+u.network+' · '+u.block+' · '+u.gate+'/'+u.pin+' · '+u.role_basis).join('\n'),equipment:[e.id],source:'보존 XML 핀·선언 정적 추적',links:[...new Set(usages.map(u=>u.network))].slice(0,6).map(n=>({url:'networks/network-'+n+'.html',label:'LAD '+n})).concat({url:'signal-guides/'+e.id+'.html',label:'신호 읽기·쓰기 근거'}),boundary:'원시 I/O와 처리된 내부 신호를 자동 연결하지 않습니다. Local 신호는 블록 문맥에서 확인하세요.'}));
  }
  for(const t of hmi.tags){const s=t.source;
    records.push(decorate({id:'hmi-'+t.index,kind:'hmi',address:s['설정 주소'],symbol:s['HMI 태그'],title:s['설정 주소']+' · '+s['HMI 태그'],text:'HMI 태그: '+s['HMI 태그']+'\nAccess Name: '+s['Access Name']+'\n'+s['근거와 한계'],equipment:t.existing_equipment_references||[],source:'dde.cfg 보존 설정 · '+t.anchor,links:[{url:'hmi-transfer.html#'+t.anchor,label:'HMI 주소 근거'},{url:'hmi-tags.html',label:'HMI 태그 원장'}],boundary:'HMI 설정 주소입니다. 현재 PLC 멤버 대응·화면 읽기/쓰기·현재값은 미확인입니다. EW/AW 등은 I/Q 주소와 합치지 않습니다.'}));
  }
  const documentBytes=await readFile(resolve(directory,'all-in-one/registers/document-search-data.json.gz'));
  const documents=JSON.parse(gunzipSync(documentBytes));
  const notesBytes=await readFile(resolve(directory,'all-in-one/registers/io-search-reference-notes.json'));
  const notes=JSON.parse(notesBytes);
  const digest=x=>createHash('sha256').update(x).digest('hex');
  await Promise.all(Object.entries({...documents.source_hashes,[notes.source]:notes.source_sha256}).map(async([path,hash])=>{
    if(!path.startsWith('sources/')&&!data.resources.includes(path))throw new Error('Non-public document source: '+path);
    if(digest(await readFile(resolve(directory,'all-in-one',path)))!==hash)throw new Error('Document search extraction is stale: '+path);
  }));
  const drawingBytes=await readFile(resolve(directory,'all-in-one/registers/drawing-search-pages.json'));
  const drawing=JSON.parse(drawingBytes);
  for(const [path,hash]of Object.entries(drawing.source_hashes))if(digest(await readFile(resolve(directory,'all-in-one',path)))!==hash)throw new Error('Drawing source stale: '+path);
  for(const p of drawing.pages){
    if(!data.resources.includes(p.image)||!data.resources.includes(p.data))throw new Error('Drawing page not public: '+p.key);
    const [bytes,imageBytes]=await Promise.all([readFile(resolve(directory,'all-in-one',p.data)),readFile(resolve(directory,'all-in-one',p.image))]);
    if(digest(bytes)!==p.data_sha256||digest(imageBytes)!==p.image_sha256)throw new Error('Drawing page stale: '+p.key);
    const page=JSON.parse(bytes);
    if(page.source!==p.source||page.page!==p.page||page.image!==p.image||page.source_sha256!==drawing.source_hashes[p.source])throw new Error('Drawing source/page mismatch: '+p.key);
    for(const word of [...page.words,...page.ocr])if(!Array.isArray(word.bbox)||word.bbox.length!==4||word.bbox.some(n=>!Number.isFinite(n)||n<0||n>1.001)||word.bbox[0]>=word.bbox[2]||word.bbox[1]>=word.bbox[3])throw new Error('Invalid drawing bbox: '+p.key);
    const tokens=[...new Set(page.ocr.filter(w=>w.confidence>=0.7).map(w=>w.text))];
    const original=documents.records.find(r=>r.kind==='source'&&r.links.some(l=>l.url===p.source+'#page='+p.page));
    if(original)original.text+='\nPDF 좌표 추출문: '+page.words.map(w=>w.text).join(' ');
    if(!tokens.length)continue;
    records.push({id:'ocr-'+p.key,kind:'ocr',address:'',symbol:'',title:'OCR 후보 · '+p.source.split('/').pop()+' · PDF '+p.page+'쪽',text:tokens.join(' · '),equipment:original?.equipment||[],equipment_names:original?.equipment_names||[],status:['OCR 자동 인식 · 기능 미확정',...(original?.equipment||[]).map(id=>statuses.get(id))].filter(Boolean).join(' / '),source:p.source+' · PDF '+p.page+'쪽 · Apple Vision 로컬 OCR · 신뢰도 0.7 이상',links:[{url:p.source+'#page='+p.page,label:'원본 도면 '+p.page+'쪽'}],boundary:'문자인식 후보입니다. 번호·위치를 원본과 대조하기 전 기능 설명이나 확정 배선으로 사용하지 마세요. 글자 누락·오인식이 있을 수 있습니다.'});
  }
  records.push(...[...notes.records,...documents.records].map(r=>({...r,status:[r.status,...(r.equipment||[]).map(id=>statuses.get(id))].filter(Boolean).join(' / ')})));
  return {schema_version:1,version:data.version,source_hashes:{...Object.fromEntries(inputs.map((p,i)=>[p,digest(contents[i])])), 'registers/drawing-search-pages.json':digest(drawingBytes),'registers/document-search-data.json.gz':digest(documentBytes),'registers/io-search-reference-notes.json':digest(notesBytes)},document_counts:documents.counts,scope_overrides_sha256:digest(await readFile(resolve(directory,'docs/equipment-standard/SCOPE-OVERRIDES.json'))),counts:Object.fromEntries(['plc','circuit','signal','hmi','reference','source','manual','ocr'].map(k=>[k,records.filter(r=>r.kind===k).length])),records};
}
if(process.argv[1]&&resolve(process.argv[1])===fileURLToPath(import.meta.url)){
  const index=await buildIndex();await writeFile(resolve(root,'all-in-one/registers/io-search-index.json'),JSON.stringify(index)+'\n');console.log('I/O 검색 색인:',index.counts);
}
