/* BC01 source comparison and local record tools. No PLC or source writes. */
((root) => {
  'use strict';
  const MAX_BYTES=8*1024*1024, MAX_NOTES=1000;
  const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const clone=v=>JSON.parse(JSON.stringify(v));
  const object=v=>v!==null && typeof v==='object' && !Array.isArray(v);
  function inspect(value,depth=0,budget={keys:0},limit=100000) {
    if(typeof value==='number'&&!Number.isFinite(value))throw new Error('유한한 숫자만 백업할 수 있습니다.');
    if(depth>30)throw new Error('파일의 중첩 구조가 너무 깊습니다.');
    if(value && typeof value==='object')for(const [key,item] of Object.entries(value)) {
      if(['__proto__','prototype','constructor'].includes(key))throw new Error('허용하지 않는 객체 항목이 있습니다.');
      if(++budget.keys>limit)throw new Error('파일의 항목이 너무 많습니다.');
      inspect(item,depth+1,budget,limit);
    }
  }
  function validateRecord(r,key='P01') {
    if(!object(r)||r.schema_version!==1||r.equipment!==key||!root.GMERepairRecords.statuses.includes(r.status))throw new Error(key+' 수리 기록의 형식·기록 구분이 올바르지 않습니다.');
    if(r.field_verified!==false||r.identity_confirmed!==false||r.repairs_completed!==0)throw new Error('이 백업의 현장·실물·수리 완료 표기는 현재 관찰 기록 형식과 다릅니다. 원본을 보존하고 확인하세요.');
    for(const key of ['time_zone','name','reference_plc_id'])if(r[key]!=null&&typeof r[key]!=='string')throw new Error('기록의 이름·시간대·참고 PLC 형식을 확인하세요.');
    for(const key of ['observations','decision_observations']) {
      if(!Array.isArray(r[key])||r[key].length>1000||r[key].some(x=>!object(x)||typeof x.id!=='string'||!x.id)||new Set(r[key].map(x=>x.id)).size!==r[key].length)throw new Error('신호 또는 비교 항목의 형식·ID를 확인하세요.');
    }
    for(const s of r.observations)for(const key of ['value','observed_at','evidence'])if(s[key]!=null && typeof s[key]!=='string')throw new Error('관찰값·시각·근거는 문자열이어야 합니다.');
    for(const s of r.observations) {
      for(const key of ['name','role'])if(s[key]!=null&&typeof s[key]!=='string')throw new Error('신호 이름·구분 형식을 확인하세요.');
      if(s.addresses!=null&&(!Array.isArray(s.addresses)||s.addresses.some(x=>typeof x!=='string')))throw new Error('신호 주소 목록의 형식을 확인하세요.');
      if(s.source_refs!=null&&(!Array.isArray(s.source_refs)||s.source_refs.some(x=>!object(x))))throw new Error('신호 원본 참조 목록의 형식을 확인하세요.');
    }
    for(const s of r.decision_observations)for(const key of ['observation','title','source_manual'])if(s[key]!=null&&typeof s[key]!=='string')throw new Error('비교 항목·결과의 형식을 확인하세요.');
    for(const [key] of (root.GMERepairRecords?.fields||[])) {
      const v=r[key];
      if(v!=null && typeof v!=='string' && !(Array.isArray(v)&&v.every(x=>typeof x==='string')))throw new Error('발생 상황·조치 항목의 형식을 확인하세요.');
    }
    return r;
  }
  function parseBackup(raw,decode,validEquipment,schema) {
    if(typeof raw!=='string'||new TextEncoder().encode(raw).length>MAX_BYTES)throw new Error('JSON 백업은 8MB 이하만 가져올 수 있습니다.');
    let data;try{data=JSON.parse(raw);}catch(_){throw new Error('JSON 파일을 읽지 못했습니다.');}
    inspect(data);
    if(!object(data)||data.application!=='GME All-in-One'||(Object.hasOwn(data,'schema_version')&&data.schema_version!==1))throw new Error('지원하는 GME 내보내기 파일을 선택하세요.');
    if(!schema || typeof schema.key!=='string')throw new Error('선택 설비의 기록 양식이 없습니다.');
    const key=schema.key;
    let all;
    if(Array.isArray(data.notes)) {
      if(data.schema_version!==1||data.notes.length>MAX_NOTES)throw new Error('지원하는 백업은 형식1, 최대1,000건입니다.');
      try{all=decode(JSON.stringify(data.notes),validEquipment);}catch(_){throw new Error('메모의 필수 항목·설비·중복 ID를 확인하세요.');}
    } else if(data.observation) {
      const record=validateRecord(data.observation,key);
      if(['note_id','title','updated'].some(k=>typeof data[k]!=='string'||!data[k]))throw new Error('개별 기록의 ID·제목·저장 시각을 확인하세요.');
      all=[{id:data.note_id,title:data.title,updated:data.updated,equipment:key,name:schema.name,
        kind:'수리·증상 기록',references:schema.manual,text:root.GMERepairRecords.summary(record),repair_observation:clone(record)}];
    } else throw new Error('백업의 메모 목록이나 수리 기록이 없습니다.');
    const eligible=all.filter(n=>n.equipment===key);
    for(const n of eligible) {
      if(!n.id||!n.title.trim()||n.id.length>500||n.title.length>10000||n.text.length>1000000||n.updated.length>1000)throw new Error('기록 ID·제목·내용의 크기를 확인하세요.');
      if(Object.hasOwn(n,'repair_observation'))validateRecord(n.repair_observation,key);
    }
    if(!eligible.length)throw new Error('이 파일에 가져올 '+(schema.reference_plc_id||key)+'('+key+') 기록이 없습니다.');
    return {notes:clone(eligible),skipped:all.length-eligible.length,total:all.length,generated_with:data.generated_with?clone(data.generated_with):null};
  }
  function planRestore(current,incoming) {
    const byId=new Map(current.map(n=>[n.id,n]));
    return incoming.map(note=>{const existing=byId.get(note.id);return {note,existing:existing||null,
      kind:!existing?'new':JSON.stringify(existing)===JSON.stringify(note)?'same':'conflict',
      action:existing?'skip':'add'};});
  }
  function preserveMerge(old,next) {
    if(object(old)&&object(next))return Object.fromEntries([...new Set([...Object.keys(old),...Object.keys(next)])].map(k=>[k,Object.hasOwn(next,k)?preserveMerge(old[k],next[k]):clone(old[k])]));
    if(Array.isArray(old)&&Array.isArray(next)&&old.concat(next).every(v=>object(v)&&typeof v.id==='string')) {
      return next.map(n=>preserveMerge(old.find(o=>o.id===n.id),n)).concat(old.filter(o=>!next.some(n=>n.id===o.id)).map(clone));
    }
    return next===undefined?old:clone(next);
  }
  function applyRestore(current,plan,choices,idFactory,key='P01') {
    const next=clone(current),ids=new Set(next.map(n=>n.id)),positions=new Map(next.map((n,i)=>[n.id,i]));let changed=0;
    for(let i=0;i<plan.length;i++) {
      const row=plan[i],action=choices[i]||row.action;
      if(action==='skip')continue;
      if(key!==null&&row.note.equipment!==key)throw new Error('선택 설비 밖의 기록은 복원할 수 없습니다.');
      const position=positions.get(row.note.id)??-1,existing=position<0?null:next[position];
      if(JSON.stringify(existing)!==JSON.stringify(row.existing))throw new Error('복원 대상이 변경되었습니다. 다시 미리보기를 확인하세요.');
      if(action==='add'&&row.kind==='new'&&position<0) {positions.set(row.note.id,next.length);next.push(clone(row.note));ids.add(row.note.id);changed++;}
      else if(action==='replace'&&row.kind==='conflict'&&existing?.equipment===row.note.equipment) {const merged=preserveMerge(existing,row.note);
        if(Object.hasOwn(row.note,'saved_with'))merged.saved_with=clone(row.note.saved_with);else delete merged.saved_with;
        const history=[];for(const source of [existing,row.note])if(Object.hasOwn(source,'backup_restore_history'))history.push(...(Array.isArray(source.backup_restore_history)?clone(source.backup_restore_history):[clone(source.backup_restore_history)]));
        if(Object.hasOwn(existing,'saved_with')&&JSON.stringify(existing.saved_with)!==JSON.stringify(row.note.saved_with))history.push({previous_updated:existing.updated,previous_saved_with:clone(existing.saved_with),incoming_updated:row.note.updated});
        if(history.length)merged.backup_restore_history=history;
        next[position]=merged;changed++;}
      else if(action==='copy'&&row.kind==='conflict') {
        const id=idFactory();if(typeof id!=='string'||!id||ids.has(id))throw new Error('새 기록 ID를 만들지 못했습니다.');
        positions.set(id,next.length);next.push({...clone(row.note),id});ids.add(id);changed++;
      } else throw new Error('복원 선택이 올바르지 않습니다.');
    }
    return {notes:next,changed};
  }
  function display(v){return v==null||v===''?'미기록':Array.isArray(v)?(v.length?v.map(display).join('\n'):'미기록'):typeof v==='object'?JSON.stringify(v,null,2):String(v);}
  function recordRows(note,schema) {
    const r=validateRecord(note.repair_observation,schema.key);
    const rows=[['title','기록 제목',note.title],['updated','브라우저 저장 시각',note.updated],['status','기록 구분',r.status],['time_zone','관찰 시간대',r.time_zone]];
    for(const [key,label] of [['application_version','저장에 사용한 매뉴얼 버전'],['source_bundle_sha256','저장 기준 자료 묶음 SHA256'],['saved_at','기록 저장 기준 시각']])rows.push(['saved_with:'+key,label,note.saved_with?.[key]]);
    for(const [key,label] of root.GMERepairRecords.fields)rows.push([key,label,r[key]]);
    for(const s of r.observations) {
      const label=s.name||root.GMERepairRecords.signalsFor(schema).find(x=>x.id===s.id)?.name||s.id;
      for(const [key,title] of [['name','저장된 태그명'],['addresses','저장된 주소'],['role','신호 구분'],['source_refs','저장된 원본 참조']])rows.push(['signal:'+s.id+':'+key,label+' · '+title,s[key]]);
      for(const [key,title] of [['value','관찰값'],['observed_at','관찰 시각'],['evidence','수집 근거']])rows.push(['signal:'+s.id+':'+key,label+' · '+title,s[key]]);
    }
    for(const s of r.decision_observations) {
      const label=s.title||schema.steps.find(x=>x.id===s.id)?.title||s.id;
      rows.push(['step:'+s.id,label+' · 관찰',s.observation],['step:'+s.id+':title',label+' · 저장된 제목',s.title],['step:'+s.id+':source_manual',label+' · 저장된 판단 근거',s.source_manual]);
    }
    return rows;
  }
  function comparisonRows(before,after,schema) {
    const left=recordRows(before,schema),right=recordRows(after,schema),a=new Map(left.map(r=>[r[0],r])),b=new Map(right.map(r=>[r[0],r]));
    return [...new Set([...a.keys(),...b.keys()])].map(k=>({key:k,label:a.get(k)?.[1]||b.get(k)[1],before:display(a.get(k)?.[2]),after:display(b.get(k)?.[2]),
      changed:JSON.stringify(a.get(k)?.[2]??null)!==JSON.stringify(b.get(k)?.[2]??null)}));
  }
  function referenceContext(data,key='P01') {
    return root.GMEEquipmentStandard.referenceContext(data,key);
  }
  function backupEnvelope(notes,data,exported=new Date().toISOString(),key='P01') {
    return {schema_version:1,application:'GME All-in-One',exported,
      generated_with:root.GMEEquipmentStandard.profile(data,key)?referenceContext(data,key):{application_version:data.version,reference_scope:key+' reference profile not implemented; observation-time evidence unknown',source_bundle_sha256:null,source_hashes:{}},notes:clone(notes)};
  }
  const MAX_UNIFIED_BYTES=64*1024*1024,MAX_UNIFIED_NOTES=50000;
  function parseUnifiedBackup(raw,decode,validEquipment,schemas=[]) {
    if(typeof raw!=='string'||new TextEncoder().encode(raw).length>MAX_UNIFIED_BYTES)throw new Error('통합 JSON 백업은 64MB 이하만 가져올 수 있습니다.');
    let data;try{data=JSON.parse(raw);}catch(_){throw new Error('JSON 파일을 읽지 못했습니다.');}
    inspect(data,0,{keys:0},2000000);
    if(!object(data)||data.application!=='GME All-in-One'||(Object.hasOwn(data,'schema_version')&&data.schema_version!==1))throw new Error('지원하는 GME 내보내기 파일을 선택하세요.');
    if(Object.hasOwn(data,'notes')&&Object.hasOwn(data,'observation'))throw new Error('메모 목록과 개별 관찰 기록이 함께 있는 파일은 형식을 확인하세요.');
    let notes;
    if(Object.hasOwn(data,'notes')) {
      if(!Array.isArray(data.notes))throw new Error('백업의 메모 목록은 배열이어야 합니다.');
      if(data.schema_version!==1||data.notes.length>MAX_UNIFIED_NOTES)throw new Error('통합 백업은 형식1, 최대50,000건입니다.');
      try{notes=decode(JSON.stringify(data.notes),validEquipment);}catch(_){throw new Error('메모의 필수 항목·설비·중복 ID를 확인하세요.');}
    }else if(Object.hasOwn(data,'observation')) {
      const key=data.observation?.equipment;if(!validEquipment.has(key))throw new Error('백업의 설비 키가 현재 대장에 없습니다.');
      const schema=schemas.find(s=>s.key===key),record=validateRecord(data.observation,key);
      if(['note_id','title','updated'].some(k=>typeof data[k]!=='string'||!data[k]))throw new Error('개별 기록의 ID·제목·저장 시각을 확인하세요.');
      notes=[{id:data.note_id,title:data.title,updated:data.updated,equipment:key,name:record.name??schema?.name??key,kind:'수리·증상 기록',references:schema?.manual||'',text:root.GMERepairRecords.summary(record),repair_observation:clone(record)}];
    }else throw new Error('백업의 메모 목록이나 수리 기록이 없습니다.');
    for(const n of notes) {
      if(!n.id||!n.title.trim()||n.id.length>500||n.title.length>10000||n.text.length>1000000||n.updated.length>1000)throw new Error('기록 ID·제목·내용의 크기를 확인하세요.');
      if(Object.hasOwn(n,'repair_observation'))validateRecord(n.repair_observation,n.equipment);
    }
    return {notes:clone(notes),total:notes.length,skipped:0,generated_with:data.generated_with?clone(data.generated_with):null};
  }
  function unifiedBackupEnvelope(notes,data,exported=new Date().toISOString()) {
    const keys=[...new Set(notes.map(n=>n.equipment))].sort(),references=Object.fromEntries(keys.map(key=>[key,backupEnvelope([],data,exported,key).generated_with]));
    return {schema_version:1,application:'GME All-in-One',backup_scope:'all_equipment',exported,
      generated_with:{application_version:data.version,reference_scope:'All equipment notes at generation; not observation-time proof',equipment_references:references},notes:clone(notes)};
  }
  function applyUnifiedRestore(current,plan,choices,idFactory) {return applyRestore(current,plan,choices,idFactory,null);}
  const api={parseUnifiedBackup,unifiedBackupEnvelope,applyUnifiedRestore,MAX_UNIFIED_BYTES,MAX_UNIFIED_NOTES,parseBackup,planRestore,applyRestore,preserveMerge,validateRecord,recordRows,comparisonRows,referenceContext,backupEnvelope,MAX_BYTES};
  if(typeof module!=='undefined'&&module.exports)module.exports=api;
  root.GMEBC01Tools=api;
  if(!root.document)return;
  let ctx,dialog=null,focusBefore=null,mode='',preview=null,generation=0,reportSnapshot='',printRefs=[];
  const status=text=>{const el=dialog?.querySelector('[data-tool-status]');if(el)el.textContent=text;};
  const selectedKey=()=>ctx.context().selected;
  const standard=()=>root.GMEEquipmentStandard.profile(ctx.data,selectedKey());
  const targetLabel=()=>standard()?.catalog_id || selectedKey();
  const schema=()=>ctx.data.repair_record_forms.profiles.find(p=>p.key===selectedKey());
  const active=()=>!!standard()?.tools && !!schema();
  const repairNotes=()=>ctx.snapshot().notes.filter(n=>n.equipment===selectedKey()&&n.repair_observation).sort((a,b)=>b.updated.localeCompare(a.updated));
  function download(value,name) {const url=URL.createObjectURL(new Blob([JSON.stringify(value,null,2)],{type:'application/json;charset=utf-8'}));const a=document.createElement('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}
  function close() {
    generation++;preview=null;reportSnapshot='';resetPrint();
    if(dialog){dialog.close();dialog.remove();dialog=null;}focusBefore?.isConnected&&focusBefore.focus({preventScroll:true});
  }
  function open(title,nextMode) {
    const opener=document.activeElement;close();focusBefore=opener?.isConnected?opener:document.activeElement;mode=nextMode;dialog=document.createElement('dialog');dialog.className='bc01-tool-dialog';
    if(ctx.context().text==='large')dialog.classList.add('bc01-tool-large');
    dialog.setAttribute('aria-labelledby','bc01-tool-title');
    dialog.innerHTML=`<header class="bc01-tool-header"><h2 id="bc01-tool-title">${esc(title)}</h2><button type="button" data-tool-close>닫기</button></header><p class="bc01-tool-boundary">${esc(targetLabel())} 보존 자료와 사용자 기록 · 현재 CPU·실물·현장 복구 확인 전</p><p data-tool-status role="status" aria-live="polite"></p><div data-tool-body></div>`;
    dialog.addEventListener('cancel',e=>{e.preventDefault();close();});document.body.append(dialog);dialog.showModal();return dialog.querySelector('[data-tool-body]');
  }
  function sources() {
    const s=standard(),allowed=new Set(ctx.data.resources);
    return s.source_locations.filter(p=>allowed.has(p.path.split('#')[0]));
  }
  function openSourceCompare() {
    const body=open('전기도면·원본 래더 나란히 보기','sources');
    const profile=ctx.data.drawing_workspace.profiles.find(p=>p.key===selectedKey()),paths=profile.circuit.paths;
    const initial=selectedKey()==='P01'&&ctx.context().view==='drawings'&&ctx.context().drawing==='oem-18'?'path-1':ctx.context().section==='circuits'?ctx.context().item:'path-0';
    const pathIndex=paths.findIndex((_,i)=>'path-'+i===initial);
    body.innerHTML=`<p>좌측은 보존 도면, 우측은 원본 XML의 Part·Wire 연결 자료입니다. TIA 화면 배치·실행 재현은 별도 확인입니다.</p><label>전기 전달 경로<select data-compare-path>${paths.map((p,i)=>`<option value="${i}" ${i===(pathIndex<0?0:pathIndex)?'selected':''}>${esc(p.signal)} · ${esc(p.backup)}</option>`).join('') || '<option value="">직접 전기 전달 경로 미확보</option>'}</select></label><p data-compare-boundary></p><div class="bc01-source-grid"><section><h3>보존 도면</h3><div class="inline-actions"><button data-tool-drawing-zoom="out">축소</button><button data-tool-drawing-zoom="reset">맞추기</button><button data-tool-drawing-zoom="in">확대</button><a data-compare-pdf target="_blank" rel="noopener">원본 PDF ↗</a></div><div class="bc01-source-image"><img data-compare-image alt="선택 경로의 보존 전기도면"></div></section><section><h3>원본 PLC 연결 자료</h3><label>비교할 원본 위치<select data-compare-lad></select></label><a data-compare-original target="_blank" rel="noopener">원본 따로 열기 ↗</a><iframe data-compare-frame title="${esc(targetLabel())} 원본 PLC 연결 자료"></iframe><p data-compare-empty hidden>선택한 경로의 직접 대응 LAD는 확보 자료에 없습니다. 자동으로 연결하지 않습니다.</p></section></div>`;
    dialog.querySelector('[data-compare-frame]').addEventListener('load',e=>{
      const frame=e.currentTarget;if(!dialog||frame.hidden||dialog.querySelector('[data-compare-frame]')!==frame)return;
      try{const sourceURL=frame.src,doc=frame.contentDocument;if(!doc)return;doc.querySelectorAll('body > header,body > footer').forEach(n=>n.style.setProperty('display','none','important'));
        doc.addEventListener('click',event=>{const link=event.target.closest('a[href]');if(!link)return;event.preventDefault();
          const url=new URL(link.getAttribute('href'),sourceURL),base=new URL(ctx.base);
          const path=url.pathname.startsWith(base.pathname)?decodeURIComponent(url.pathname.slice(base.pathname.length)):'';
          if(url.origin===base.origin&&ctx.data.resources.includes(path))root.open(url.href,'_blank','noopener');
        });
        if(dialog?.classList.contains('bc01-tool-large')){const style=doc.createElement('style');style.textContent='body,table,pre,code{font-size:18px!important}';doc.head.append(style);}
        const target=frame.dataset.sourceHash&&doc.getElementById(frame.dataset.sourceHash);
        if(target){const style=doc.createElement('style');style.textContent='.bc01-comparison-target{background:#e4f4ed!important;outline:2px solid #197365;outline-offset:-2px}';doc.head.append(style);target.classList.add('bc01-comparison-target');doc.defaultView.scrollTo(0,target.getBoundingClientRect().top+doc.defaultView.scrollY-doc.defaultView.innerHeight/2);}
      }catch(_){status('원본은 따로 열기 링크에서도 확인할 수 있습니다.');}
    });
    changePath();
  }
  function changePath() {
    const index=Number(dialog.querySelector('[data-compare-path]').value),profile=ctx.data.drawing_workspace.profiles.find(p=>p.key===selectedKey()),path=profile.circuit.paths[index];
    const sheet=path?profile.sheets.find(s=>s.id===(path.sheet_id||'oem-'+path.fg)):profile.sheets[0],img=dialog.querySelector('[data-compare-image]');
    const pdf=dialog.querySelector('[data-compare-pdf]');img.hidden=!sheet;pdf.hidden=!sheet;
    if(sheet){img.src=sheet.image;img.style.width='100%';img.alt=sheet.title;pdf.href=sheet.source+'#page='+sheet.page;}else{img.removeAttribute('src');img.alt='보존 도면 미확보';pdf.removeAttribute('href');}
    const sourcePair=path?standard().source_pairs.find(p=>p.signal===path.signal):standard().source_pairs.find(p=>p.path);
    const pair=sourcePair?.path?[sourcePair.path,sourcePair.label]:null;
    dialog.querySelector('[data-compare-boundary]').textContent=(path?'':'직접 전기 전달 경로는 미확보입니다. 보존 도면과 원본 위치를 각각 비교하며 실제 배선 대응을 확정하지 않습니다. ')+(sourcePair?.boundary || '직접 대응·실물 연결은 미확정입니다.');
    const options=sources().map(s=>[s.path,s.label||`LAD${s.network} · ${s.kind==='part'?'Part':'Wire'} ${s.uid}`]);
    if(pair){const match=options.find(o=>o[0]===pair[0]);if(match)match[1]=pair[1]+' · '+match[1];else options.unshift(pair);}
    const select=dialog.querySelector('[data-compare-lad]');select.innerHTML=options.map(([path,label])=>`<option value="${esc(path)}">${esc(label)}</option>`).join('');
    select.disabled=!pair;dialog.querySelector('[data-compare-frame]').hidden=!pair;dialog.querySelector('[data-compare-empty]').hidden=!!pair;dialog.querySelector('[data-compare-empty]').textContent=path?'선택한 경로의 직접 대응 LAD는 확보 자료에 없습니다. 자동으로 연결하지 않습니다.':'이 설비의 고유 원본 PLC 연결 자료는 확보되지 않았습니다. 자동으로 배정하지 않습니다.';dialog.querySelector('[data-compare-original]').hidden=!pair;
    if(pair){select.value=pair[0];changeLad();}else{const frame=dialog.querySelector('[data-compare-frame]');frame.removeAttribute('src');delete frame.dataset.sourceHash;dialog.querySelector('[data-compare-original]').removeAttribute('href');}
  }
  function changeLad() {
    const path=dialog.querySelector('[data-compare-lad]').value;
    const allowed=new Set(sources().map(s=>s.path).concat(standard().source_pairs.filter(p=>p.path).map(p=>p.path)));
    if(!allowed.has(path))return;
    const frame=dialog.querySelector('[data-compare-frame]'),url=new URL(path,ctx.base);
    dialog.querySelector('[data-compare-original]').href=url.href;frame.dataset.sourceHash=url.hash.slice(1);url.hash='';frame.src=url.href;
  }
  function openRestore() {
    const body=open(`${esc(targetLabel())} 기록 백업 가져오기·복원`,'restore');
    body.innerHTML=`<p>전체 메모 백업 또는 개별 수리 기록 JSON에서 ${esc(targetLabel())} 기록만 가져옵니다. 다른 설비·임시 작성 내용은 유지합니다.</p><label>JSON 백업 파일<input type="file" accept=".json,application/json" data-restore-file></label><div data-restore-preview></div>`;
    if(!navigator.locks?.request)status('이 브라우저는 기록 잠금을 지원하지 않아 미리보기만 제공합니다. 최신 브라우저에서 복원하세요.');
  }
  async function readImport(file) {
    if(!file)return;const token=++generation;preview=null;dialog.querySelector('[data-restore-preview]').innerHTML='';
    try{if(file.size>MAX_BYTES)throw new Error('JSON 백업은 8MB 이하만 가져올 수 있습니다.');
      const incoming=parseBackup(await file.text(),root.GMENoteStore.decodeNotes,ctx.validEquipment,schema());
      if(token!==generation||!dialog||mode!=='restore'||!active())return;
      const snapshot=ctx.snapshot();preview={selectedKey:selectedKey(),snapshot,incoming,plan:planRestore(snapshot.notes,incoming.notes),choices:{}};
      const rows=preview.plan;
      dialog.querySelector('[data-restore-preview]').innerHTML=`<p>${esc(targetLabel())} ${rows.length}건 · 다른 설비 ${incoming.skipped}건 제외. 아래 선택을 확인한 후 저장하세요.</p>${rows.map((r,i)=>`<article class="bc01-restore-row"><h3>${esc(r.note.title)}</h3><p>${r.kind==='new'?'새 기록':r.kind==='same'?'동일 기록 · 변경 없음':'같은 ID의 다른 기록'} · ${esc(r.note.updated)}</p><label>복원 선택<select data-restore-choice="${i}"><option value="skip">기존 유지 · 가져오지 않기</option>${r.kind==='new'?'<option value="add" selected>새 기록 추가</option>':r.kind==='conflict'?`${r.existing.equipment===selectedKey()?'<option value="replace">가져온 값으로 복원 · 기존 추가 항목 보존</option>':''}<option value="copy">새 ID로 둘 다 보존</option>`:''}</select></label><details><summary>기존·가져온 전체 기록 비교</summary><div class="bc01-import-grid"><div><h4>기존 기록</h4><pre>${esc(r.existing?JSON.stringify(r.existing,null,2):'없음')}</pre></div><div><h4>가져온 기록</h4><pre>${esc(JSON.stringify(r.note,null,2))}</pre></div></div></details></article>`).join('')}<div class="inline-actions"><button data-restore-backup>복원 전 전체 백업 다운로드</button><button data-restore-commit ${navigator.locks?.request?'':'disabled'}>선택한 ${esc(targetLabel())} 기록을 저장</button></div>`;
      status('미리보기입니다. 브라우저 기록은 아직 변경되지 않았습니다.');
      const imported=incoming.generated_with;
      if(imported&&typeof imported.application_version==='string') {
        const p=document.createElement('p');p.textContent='내보내기 생성 기준: 매뉴얼 v'+imported.application_version+' · 생성 기준: '+(typeof imported.reference_scope==='string'?imported.reference_scope:'자료 범위 미기록')+'. 관찰 당시 버전이나 현재 원본 일치를 자동 검증한 표시는 아닙니다.';
        dialog.querySelector('[data-restore-preview]').prepend(p);
      }
    }catch(error){if(token===generation&&dialog)status(error.message);}
  }
  async function commitRestore(button) {
    if(!preview||!active()||!navigator.locks?.request)return;
    button.disabled=true;dialog.querySelectorAll('[data-restore-choice]').forEach(el=>el.disabled=true);const saved=preview,token=generation,startedDialog=dialog,choicesBefore=JSON.stringify(preview.choices);
    const sameUI=()=>dialog===startedDialog&&token===generation&&preview===saved&&JSON.stringify(saved.choices)===choicesBefore;
    try{const result=applyRestore(saved.snapshot.notes,saved.plan,saved.choices,()=>crypto.randomUUID(),selectedKey());
      if(!result.changed){status('저장할 변경이 없습니다. 기존 기록을 유지했습니다.');return;}
      await ctx.restore(saved.snapshot.raw,result.notes,()=>sameUI()&&active()&&selectedKey()===saved.selectedKey);
      if(!sameUI())return;preview=null;dialog.querySelector('[data-restore-preview]').innerHTML=`<p>선택한 ${esc(targetLabel())} 기록 ${result.changed}건의 저장과 재읽기를 확인했습니다.</p><button data-restored-open>저장 목록 열기</button>`;
      status('복원했습니다. 임시 작성 내용은 유지했습니다.');
    }catch(error){if(sameUI()){status(error.message);dialog.querySelector('[data-restore-preview]').innerHTML='<p>복원 완료를 확인하지 못했습니다. 저장 목록과 복원 전 백업을 먼저 대조한 뒤 파일을 다시 선택하세요.</p>';preview=null;}}
    finally{if(button.isConnected){button.disabled=false;dialog?.querySelectorAll('[data-restore-choice]').forEach(el=>el.disabled=false);}}
  }
  function recordOptions(rows){return rows.map(n=>`<option value="${esc(n.id)}">${esc(n.title)} · ${esc(n.updated)}</option>`).join('');}
  function openRecords(nextMode) {
    const body=open(nextMode==='report'?`저장한 ${esc(targetLabel())} 관찰 결과 보고서`:`${esc(targetLabel())} 점검 전후 기록 비교`,nextMode);
    const rows=repairNotes();
    if(!rows.length){body.innerHTML=`<p>저장된 ${esc(targetLabel())} 수리 관찰 기록이 없습니다. 수리 기록에서 관찰 내용을 먼저 저장하세요.</p><button data-restored-open>수리 기록 열기</button>`;return;}
    body.innerHTML=nextMode==='report'?`<div class="bc01-no-print"><label>보고서 기록<select data-report-note>${recordOptions(rows)}</select></label><button data-report-load>보고서 미리보기</button></div><div data-report-preview></div>`:
      `<div class="bc01-record-pickers"><label>점검 전 기록<select data-compare-before>${recordOptions(rows)}</select></label><label>점검 후 기록<select data-compare-after>${recordOptions(rows)}</select></label><button data-record-compare>두 기록 비교</button></div><p>앞·뒤 순서는 직접 선택합니다. 값 차이는 자동 고장·복구 판정이 아닙니다.</p><div data-record-comparison></div>`;
    if(nextMode==='compare'&&rows.length>1)dialog.querySelector('[data-compare-before]').value=rows[1].id;
  }
  function compareRecords() {
    const rows=repairNotes(),a=rows.find(n=>n.id===dialog.querySelector('[data-compare-before]').value),b=rows.find(n=>n.id===dialog.querySelector('[data-compare-after]').value);
    if(!a||!b)throw new Error('기록 목록이 바뀌었습니다. 닫고 다시 선택하세요.');
    const changes=comparisonRows(a,b,schema());
    dialog.querySelector('[data-record-comparison]').innerHTML=`<p>${esc(a.title)} → ${esc(b.title)} · 표시 항목 차이 ${changes.filter(r=>r.changed).length}개${a.id===b.id?' · 같은 기록 선택':''}</p><div class="table-wrap"><table><thead><tr><th>관찰 항목</th><th>점검 전</th><th>점검 후</th></tr></thead><tbody>${changes.map(r=>`<tr class="${r.changed?'bc01-record-changed':''}"><th scope="row">${esc(r.label)}</th><td>${esc(r.before)}</td><td>${esc(r.after)}</td></tr>`).join('')}</tbody></table></div><details><summary>추가 항목을 포함한 전체 기록 원문</summary><div class="bc01-import-grid"><pre>${esc(JSON.stringify(a,null,2))}</pre><pre>${esc(JSON.stringify(b,null,2))}</pre></div></details>`;
    status('현재 저장된 두 기록을 읽었습니다. 저장 자료는 변경하지 않았습니다.');
  }
  function renderReport() {
    const snapshot=ctx.snapshot(),note=snapshot.notes.find(n=>n.id===dialog.querySelector('[data-report-note]').value&&n.equipment===selectedKey()&&n.repair_observation);
    if(!note)throw new Error('기록 목록이 바뀌었습니다. 닫고 다시 선택하세요.');
    const rows=recordRows(note,schema()),links=[schema().manual,...new Set(root.GMERepairRecords.signalsFor(schema()).flatMap(s=>s.refs.map(r=>'networks/network-'+r.network+'.html')))].filter(p=>ctx.data.resources.includes(p));
    reportSnapshot=JSON.stringify(note);
    const record=note.repair_observation,roles=root.GMERepairRecords.roles,generated=referenceContext(ctx.data,selectedKey());
    const generationHtml='<p data-report-version>보고서 생성 기준: 매뉴얼 v'+esc(generated.application_version)+` · ${esc(targetLabel())} 참고 자료 `+Object.keys(generated.source_hashes).length+'개<br>자료 묶음 SHA256: <code>'+esc(generated.source_bundle_sha256)+'</code><br>생성 시점의 참고 자료입니다. 과거 관찰 당시의 버전·자료 일치를 확정하지 않습니다.</p>';
    const refs=value=>(value||[]).map(r=>`LAD ${display(r.network)} · ORef ${display(r.oref)}${r.source?' · '+display(r.source):''}`).join('\n')||'미기록';
    const general=rows.filter(([key])=>!key.startsWith('signal:')&&!key.startsWith('step:'));
    dialog.querySelector('[data-report-preview]').innerHTML=`<article class="bc01-report"><h1>${esc(targetLabel())} 관찰 결과 보고서</h1><h2>${esc(note.title)}</h2><p>기록 ID: ${esc(note.id)}<br>기록 구분: ${esc(record.status)}<br>보고서 생성: ${esc(new Date().toLocaleString('ko-KR'))} · ${esc(Intl.DateTimeFormat().resolvedOptions().timeZone)}</p><p>사용자가 저장한 관찰·조치 기록입니다. 현재 CPU·실물 대응·복구 완료의 자동 검증 결과가 아닙니다. 미입력 항목은 미기록으로 표시합니다.</p><h2>발생 상황·조치·확인 대기</h2><dl>${general.map(([,label,value])=>`<div><dt>${esc(label)}</dt><dd>${esc(display(value))}</dd></div>`).join('')}</dl><h2>신호 관찰</h2><p>관찰 시각 기준: ${esc(display(record.time_zone))}</p><div class="table-wrap"><table class="bc01-report-signals"><thead><tr><th>저장된 신호·주소</th><th>관찰값</th><th>관찰 시각</th><th>수집 근거·원본 참조</th></tr></thead><tbody>${record.observations.map(r=>`<tr><th scope="row">${esc(r.name||r.id)}<br>${esc(roles[r.role]||display(r.role))}<br>${esc(display(r.addresses))}</th><td>${esc(display(r.value))}</td><td>${esc(display(r.observed_at))}</td><td>${esc(display(r.evidence))}${r.boundary?`<p>${esc(r.boundary)}</p>`:''}<details class="bc01-report-ref"><summary>저장된 원본 참조</summary><p>${esc(refs(r.source_refs))}</p></details></td></tr>`).join('')}</tbody></table></div><h2>증상별 관찰·비교</h2><dl>${record.decision_observations.map(r=>`<div><dt>${esc(r.title||r.id)}</dt><dd>${esc(display(r.observation))}<br><small>저장된 판단 근거: ${esc(display(r.source_manual))}</small></dd></div>`).join('')}</dl><section class="bc01-report-sources"><h2>참고 원본·점검 근거</h2><ul>${links.map(p=>`<li><a href="${esc(new URL(p,ctx.base).href)}" target="_blank" rel="noopener">${esc(p)}</a></li>`).join('')}</ul><p>추가 항목을 포함한 전체 저장 기록은 JSON으로 함께 보관할 수 있습니다.</p></section></article><div class="inline-actions bc01-no-print"><button data-report-print>이 결과 보고서 인쇄·PDF 저장</button><button data-report-json>전체 기록 JSON 다운로드</button></div>`;
    dialog.querySelector('.bc01-report h2').insertAdjacentHTML('afterend',generationHtml);
    status('저장된 기록의 보고서 미리보기입니다. 원본·기록을 변경하지 않습니다.');
  }
  function preparePrint() {
    const id=dialog.querySelector('[data-report-note]').value,note=ctx.snapshot().notes.find(n=>n.id===id);
    if(JSON.stringify(note)!==reportSnapshot)throw new Error('기록이 변경되었습니다. 보고서 미리보기를 다시 생성하세요.');
    if(document.body.classList.contains('bc01-printing'))return;
    printRefs=[...dialog.querySelectorAll('.bc01-report-ref')].map(el=>[el,el.open]);
    printRefs.forEach(([el])=>{el.open=true;});
    document.body.classList.add('bc01-printing');
  }
  function printReport(){preparePrint();window.print();}
  function resetPrint(){document.body.classList.remove('bc01-printing');printRefs.forEach(([el,open])=>{el.open=open;});printRefs=[];}
  api.attach=context=>{ctx=context;};
  api.close=close;
  api.openSelectedRestore=()=>{if(active())openRestore();};
  api.mount=host=>{
    if(!active()||!['manual','repair','repair-record','drawings','ladder','notes'].includes(ctx.context().view))return;
    const toolbar=document.createElement('section');toolbar.className='bc01-tools-bar';toolbar.setAttribute('aria-label',`${esc(targetLabel())} 자료 비교와 기록 보존`);
    toolbar.innerHTML=`<strong>${esc(targetLabel())} 자료·기록 도구</strong><div class="inline-actions"><button data-bc01-tool="sources">도면·래더 나란히</button><button data-bc01-tool="restore">통합 백업·복원</button><button data-bc01-tool="compare">점검 전후 비교</button><button data-bc01-tool="report">관찰 결과 보고서</button></div>`;toolbar.querySelectorAll('[data-bc01-tool]').forEach(b=>{b.hidden=!standard().tools[b.dataset.bc01Tool];});host.prepend(toolbar);
  };
  document.addEventListener('click',async e=>{
    const b=e.target.closest('button');if(!b)return;
    try {
      if(b.dataset.bc01Tool&&active()&&standard().tools[b.dataset.bc01Tool]){if(b.dataset.bc01Tool==='sources')openSourceCompare();else if(b.dataset.bc01Tool==='restore'){close();root.GMEUnifiedBackup.open();}else if(['compare','report'].includes(b.dataset.bc01Tool))openRecords(b.dataset.bc01Tool);return;}
      if(!dialog?.contains(b))return;
      if(b.hasAttribute('data-tool-close'))close();
      else if(b.dataset.toolDrawingZoom){const img=dialog.querySelector('[data-compare-image]'),old=parseFloat(img.style.width)||100;img.style.width=(b.dataset.toolDrawingZoom==='reset'?100:Math.max(50,Math.min(400,old+(b.dataset.toolDrawingZoom==='in'?25:-25))))+'%';}
      else if(b.hasAttribute('data-restore-backup')&&preview)download(backupEnvelope(preview.snapshot.notes,ctx.data,undefined,selectedKey()),`GME-before-${esc(targetLabel())}-restore.json`);
      else if(b.hasAttribute('data-restore-commit'))await commitRestore(b);
      else if(b.hasAttribute('data-restored-open')){close();ctx.openRecords();}
      else if(b.hasAttribute('data-record-compare'))compareRecords();
      else if(b.hasAttribute('data-report-load'))renderReport();
      else if(b.hasAttribute('data-report-print'))printReport();
      else if(b.hasAttribute('data-report-json')){const note=ctx.snapshot().notes.find(n=>n.id===dialog.querySelector('[data-report-note]').value);if(!note||JSON.stringify(note)!==reportSnapshot)throw new Error('기록이 변경되었습니다. 보고서 미리보기를 다시 생성하세요.');download(backupEnvelope([note],ctx.data,undefined,selectedKey()),`GME-${esc(targetLabel())}-observation-report.json`);}
    }catch(error){status(error.message);}
  });
  document.addEventListener('change',e=>{
    if(!dialog?.contains(e.target))return;
    if(e.target.hasAttribute('data-restore-file')) {
      const file=e.target.files[0];
      e.target.value='';
      readImport(file);
    }
    else if(e.target.hasAttribute('data-restore-choice')&&preview)preview.choices[e.target.dataset.restoreChoice]=e.target.value;
    else if(e.target.hasAttribute('data-compare-path'))changePath();
    else if(e.target.hasAttribute('data-compare-lad'))changeLad();
    else if(e.target.hasAttribute('data-report-note')){reportSnapshot='';dialog.querySelector('[data-report-preview]').innerHTML='';}
  });
  window.addEventListener('storage',e=>{if(dialog&&e.key==='gme-all-in-one-notes-v1'){reportSnapshot='';status('다른 탭에서 기록이 변경되었습니다. 미리보기·비교를 다시 확인하세요.');}});
  window.addEventListener('beforeprint',()=>{
    if(mode!=='report'||!dialog?.open||!reportSnapshot)return;
    try{preparePrint();}catch(error){resetPrint();status(error.message);}
  });
  window.addEventListener('afterprint',resetPrint);
})(typeof window!=='undefined'?window:globalThis);
