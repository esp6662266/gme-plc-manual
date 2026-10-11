/* One local JSON backup for all saved equipment notes. No PLC/source writes. */
((root)=>{
  'use strict';
  if(!root.document)return;
  const tools=root.GMEBC01Tools;
  const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  let ctx,dialog=null,preview=null,generation=0,opener=null,page=0;
  const message=text=>{const el=dialog?.querySelector('[data-unified-message]');if(el)el.textContent=text;};
  const name=key=>{const item=ctx.data.priority.find(p=>p.key===key)||ctx.data.equipment.find(p=>p.id===key);return (item?.name||key)+' · '+key;};
  function close(){generation++;preview=null;if(dialog){dialog.close();dialog.remove();dialog=null;}opener?.isConnected&&opener.focus({preventScroll:true});}
  function download(notes){const value=tools.unifiedBackupEnvelope(notes,ctx.data),payload=JSON.stringify(value,null,2);tools.parseUnifiedBackup(payload,root.GMENoteStore.decodeNotes,ctx.validEquipment,ctx.data.repair_record_forms.profiles);const url=URL.createObjectURL(new Blob([payload],{type:'application/json;charset=utf-8'}));const a=document.createElement('a');a.href=url;a.download='GME-all-equipment-backup-'+new Date().toISOString().slice(0,10)+'.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}
  function open(){
    root.GMEBC01Tools.close();const previous=document.activeElement;close();opener=previous;dialog=document.createElement('dialog');dialog.className='bc01-tool-dialog gme-unified-backup';dialog.setAttribute('aria-labelledby','gme-unified-title');
    dialog.innerHTML='<header class="bc01-tool-header"><h2 id="gme-unified-title">모든 설비 통합 백업·복원</h2><button type="button" data-unified-close>닫기</button></header><p>이 브라우저에 저장한 모든 설비의 메모·수리 기록을 JSON 파일 하나로 보관하고 옮깁니다. 작성 중인 초안은 현재 브라우저에 유지합니다.</p><p data-unified-message role="status" aria-live="polite"></p><section class="panel"><h3>1. 전체 기록을 한 파일로 백업</h3><p data-unified-count></p><button type="button" data-unified-export>모든 설비 통합 JSON 다운로드</button></section><section class="panel"><h3>2. 통합 파일 가져오기</h3><p>기존 전체 백업과 개별 JSON도 가져올 수 있습니다. 미리보기에서 충돌 선택 후 저장합니다. 기존에만 있는 기록과 추가 항목은 보존하며, 저장할 기록을 삭제하지 않습니다.</p><label>통합 JSON 백업 파일<input type="file" accept=".json,application/json" data-unified-file></label><p>최대64MB / 50,000건. 복원은 저장한 메모·수리 기록에 적용합니다.</p><div data-unified-preview></div></section>';
    dialog.addEventListener('cancel',e=>{e.preventDefault();close();});document.body.append(dialog);dialog.showModal();
    const snap=ctx.snapshot(),keys=new Set(snap.notes.map(n=>n.equipment));dialog.querySelector('[data-unified-count]').textContent=keys.size+'개 설비 · '+snap.notes.length+'건 · 설비 선택과 관계없이 전체를 포함합니다.';
    if(!navigator.locks?.request)message('이 브라우저는 기록 잠금을 지원하지 않아 백업·미리보기만 제공합니다.');
  }
  const actionAt=(p,i)=>p.choices[i]||p.plan[i].action;
  function renderPreview(){
    if(!preview||!dialog)return;
    const p=preview,filter=dialog.querySelector('[data-unified-equipment]')?.value||'',kind=dialog.querySelector('[data-unified-kind]')?.value||'',counts={add:0,replace:0,copy:0,skip:0};
    p.plan.forEach((_,i)=>counts[actionAt(p,i)]++);
    const matched=p.plan.map((row,i)=>({row,i})).filter(({row})=>(!filter||row.note.equipment===filter)&&(!kind||row.kind===kind));page=Math.min(page,Math.max(0,Math.ceil(matched.length/50)-1));const shown=matched.slice(page*50,page*50+50),keys=[...new Set(p.plan.map(r=>r.note.equipment))].sort();
    dialog.querySelector('[data-unified-preview]').innerHTML='<h3>3. 복원 미리보기 · '+p.plan.length+'건</h3><p>추가 '+counts.add+' · 가져온 값 복원 '+counts.replace+' · 새 ID 복사 '+counts.copy+' · 기존 유지 '+counts.skip+'</p><p><strong>저장 대상은 위 선택 합계입니다.</strong> 아래 필터는 목록 표시만 바꿉니다. 충돌 기록은 기본으로 기존 값을 유지합니다. 가져온 값으로 복원하면 가져온 저장 근거를 사용하며, 기존 저장 근거는 별도 이력으로 보존합니다.</p><div class="inline-actions"><label>표시 설비<select data-unified-equipment><option value="">모든 설비</option>'+keys.map(k=>'<option value="'+esc(k)+'" '+(k===filter?'selected':'')+'>'+esc(name(k))+'</option>').join('')+'</select></label><label>표시 기록<select data-unified-kind><option value="">전체 기록</option>'+[['new','새 기록'],['conflict','충돌 기록'],['same','동일 기록']].map(([k,t])=>'<option value="'+k+'" '+(k===kind?'selected':'')+'>'+t+'</option>').join('')+'</select></label><button type="button" data-unified-keep '+(p.busy?'disabled':'')+'>모두 기존 유지</button><button type="button" data-unified-add '+(p.busy?'disabled':'')+'>새 기록 모두 추가</button></div><p>'+shown.filter(({i})=>actionAt(p,i)!=='skip').length+'건 현재 페이지 선택 · '+(counts.add+counts.replace+counts.copy-shown.filter(({i})=>actionAt(p,i)!=='skip').length)+'건 다른 페이지·필터에서 선택 · '+matched.length+'건 표시 대상 · '+(matched.length?page+1:0)+' / '+Math.ceil(matched.length/50)+'페이지</p>'+shown.map(({row:r,i})=>'<article class="bc01-restore-row"><h4>'+esc(name(r.note.equipment))+' · '+esc(r.note.title)+'</h4><p>'+esc(r.note.updated)+' · '+({new:'새 기록',same:'동일 기록',conflict:'같은 ID의 다른 기록'}[r.kind])+'</p><label>복원 선택<select data-unified-choice="'+i+'" '+(p.busy?'disabled':'')+'><option value="skip">기존 유지</option>'+(r.kind==='new'?'<option value="add">새 기록 추가</option>':r.kind==='conflict'?(r.existing.equipment===r.note.equipment?'<option value="replace">가져온 값으로 복원 · 추가 항목 보존</option>':'')+'<option value="copy">새 ID로 둘 다 보존</option>':'')+'</select></label><details><summary>전체 저장 내용 비교</summary><div class="bc01-import-grid"><pre>'+esc(r.existing?JSON.stringify(r.existing,null,2):'기존 기록 없음')+'</pre><pre>'+esc(JSON.stringify(r.note,null,2))+'</pre></div></details></article>').join('')+'<div class="inline-actions"><button type="button" data-unified-page="prev" '+(page?'':'disabled')+'>이전50건</button><button type="button" data-unified-page="next" '+((page+1)*50<matched.length?'':'disabled')+'>다음50건</button></div><div class="inline-actions"><button type="button" data-unified-before>복원 전 전체 통합 백업</button><button type="button" data-unified-save '+(!navigator.locks?.request||p.busy||!(counts.add+counts.replace+counts.copy)?'disabled':'')+'>선택한 전체 설비 기록 '+(counts.add+counts.replace+counts.copy)+'건 저장</button></div>';
    dialog.querySelectorAll('[data-unified-choice]').forEach(el=>el.value=actionAt(p,Number(el.dataset.unifiedChoice)));
  }
  async function read(file){
    if(!file)return;const token=++generation,currentDialog=dialog;preview=null;page=0;dialog.querySelector('[data-unified-preview]').innerHTML='';
    try{
      if(file.size>tools.MAX_UNIFIED_BYTES)throw new Error('통합 JSON 백업은 64MB 이하만 가져올 수 있습니다.');
      const incoming=tools.parseUnifiedBackup(await file.text(),root.GMENoteStore.decodeNotes,ctx.validEquipment,ctx.data.repair_record_forms.profiles);
      if(token!==generation||dialog!==currentDialog)return;
      const snapshot=ctx.snapshot();preview={snapshot,incoming,plan:tools.planRestore(snapshot.notes,incoming.notes),choices:{},busy:false};renderPreview();message('미리보기입니다. 브라우저 기록은 아직 변경되지 않았습니다.');
    }catch(error){if(token===generation&&dialog===currentDialog)message(error.message);}
  }
  async function save(){
    if(!preview||preview.busy||!navigator.locks?.request)return;
    const p=preview,token=generation,currentDialog=dialog,choices=JSON.stringify(p.choices),isCurrent=()=>dialog===currentDialog&&preview===p&&generation===token&&JSON.stringify(p.choices)===choices;
    p.busy=true;renderPreview();
    try{
      const result=tools.applyUnifiedRestore(p.snapshot.notes,p.plan,p.choices,()=>crypto.randomUUID());
      if(!result.changed){message('저장할 변경이 없습니다. 기존 기록을 유지했습니다.');return;}
      await ctx.restoreAll(p.snapshot.raw,result.notes,isCurrent);
      if(!isCurrent())return;preview=null;dialog.querySelector('[data-unified-preview]').innerHTML='<p>전체 설비에서 선택한 '+result.changed+'건을 저장하고 재읽기로 확인했습니다. 기존에만 있는 기록·초안·추가 항목은 유지했습니다.</p><button type="button" data-unified-open-notes>현재 설비 저장 목록 열기</button>';message('통합 복원을 완료했습니다. 파일은 하나로 보관하세요.');
    }catch(error){if(isCurrent()){preview=null;dialog.querySelector('[data-unified-preview]').innerHTML='<p>복원 완료를 확인하지 못했습니다. 저장 목록과 복원 전 통합 백업을 대조한 뒤 파일을 다시 선택하세요.</p>';message(error.message);}}
    finally{p.busy=false;if(preview===p&&dialog===currentDialog)renderPreview();}
  }
  const api={attach:c=>{ctx=c;},open,close,download:()=>download(ctx.snapshot().notes)};root.GMEUnifiedBackup=api;
  document.addEventListener('click',async e=>{
    const b=e.target.closest('button');if(!b)return;
    try{
      if(b.hasAttribute('data-unified-backup')){open();return;}
      if(!dialog?.contains(b))return;
      if(b.hasAttribute('data-unified-close'))close();
      else if(b.hasAttribute('data-unified-open-notes')){close();ctx.openNotes();}
      else if(b.hasAttribute('data-unified-export'))download(ctx.snapshot().notes);
      else if(b.hasAttribute('data-unified-before')&&preview)download(preview.snapshot.notes);
      else if(b.hasAttribute('data-unified-save'))await save();
      else if(b.dataset.unifiedPage){page+=b.dataset.unifiedPage==='next'?1:-1;renderPreview();}
      else if(preview&&!preview.busy&&(b.hasAttribute('data-unified-keep')||b.hasAttribute('data-unified-add'))){if(b.hasAttribute('data-unified-keep'))preview.choices=Object.fromEntries(preview.plan.map((r,i)=>[i,'skip']));else preview.plan.forEach((r,i)=>{if(r.kind==='new')preview.choices[i]='add';});renderPreview();}
    }catch(error){message(error.message);}
  });
  document.addEventListener('change',e=>{
    if(!dialog?.contains(e.target))return;
    if(e.target.hasAttribute('data-unified-file')){const file=e.target.files[0];e.target.value='';read(file);}
    else if(preview&&e.target.hasAttribute('data-unified-choice')&&!preview.busy){preview.choices[e.target.dataset.unifiedChoice]=e.target.value;renderPreview();}
    else if(e.target.hasAttribute('data-unified-equipment')||e.target.hasAttribute('data-unified-kind')){page=0;renderPreview();}
  });
  window.addEventListener('storage',e=>{if(dialog&&e.key==='gme-all-in-one-notes-v1')message('다른 탭에서 기록이 변경되었습니다. 저장 전에 파일을 다시 선택해 대조하세요.');});
})(typeof window!=='undefined'?window:globalThis);
