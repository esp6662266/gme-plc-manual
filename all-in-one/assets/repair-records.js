/* Source-linked user observations, deliberately separate from execution state. */
((root) => {
  'use strict';
  const fields=[
    ['timestamp','관찰 기준 시각','datetime-local'],['observer','기록자','text'],
    ['actual_equipment_id','확인한 실물 설비 ID','text'],['location','위치·본체와 구동부','text'],
    ['control_owner','제어반·전용 제어기','text'],['current_plc_version','현재 PLC 프로젝트·버전 근거','text'],
    ['mode','관찰 당시 모드·공정 단계','text'],['first_symptom','최초 증상','textarea'],
    ['first_alarm','최초 알람·발생 시각','textarea'],['identity_evidence','명판·사진·카드 등 대응 근거','textarea'],
    ['cause_candidates','원인 후보와 배제 근거','textarea'],['work_performed','실제로 수행한 조치·시각','textarea'],
    ['recovery_evidence','복구 관찰·알람·응답·연동 증거','textarea'],['unresolved','미확인 조건·후속 확인','textarea']
  ];
  const statuses=['관찰 기록','조치 기록','추가 확인 필요'];
  const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const keyFor=k=>'repair:'+k;
  const relationshipLabels={identity:'선택 설비의 식별 항목',declared:'원본 대장에 명시된 설비 범위',related:'원본 신호 참조로 연관된 자료',global:'전체 공통 자료'};
  const docLinks=links=>(links||[]).map(r=>`<button type="button" data-doc="${esc(r.path)}">${esc(r.label)}</button>`).join(' ');
  function evidenceRequirements(section){
    if(!section)return '';
    return `<div class="repair-evidence"><h4>확인할 근거·기록할 내용</h4><ul>${section.requirements.map(r=>`<li><strong>${esc(r.owner)}</strong> · ${esc(r.work)}</li>`).join('')}</ul>${section.source_links?.length?`<div class="inline-actions">${docLinks(section.source_links)}</div>`:''}
      ${section.reviews.length?`<details class="repair-review-list"><summary>관련 미확정 근거 · ${section.reviews.length}항목</summary><p class="muted">각 항목은 자료 확인 대상입니다. 신호 참조 연관·공통 자료는 이 설비의 직접 제어 조건 또는 실물 동일성을 뜻하지 않습니다.</p>${section.reviews.map(r=>`<article><h4>${esc(r.id)} · ${esc(r.title)}</h4><p class="muted">${esc(relationshipLabels[r.relationship]||r.relationship)} · ${esc(r.status)}</p><p>${esc(r.observation)}</p><p><strong>다음 확인</strong> · ${esc(r.next_check)}</p><div class="inline-actions"><button type="button" data-review-focus="${esc(r.id)}">이 검토 항목·메모 보기</button>${docLinks(r.links)}</div></article>`).join('')}</details>`:''}</div>`;
  }
  function evidencePreflight(plan){
    if(!plan)return '';
    return `<section class="panel repair-preflight"><h2>점검 순서·필요한 자료</h2><p>실물과 현재 자료를 먼저 식별한 뒤, 아래 증상별 비교에서 해당 근거를 확인하고 관찰 결과를 기록합니다. 확인 순서는 자료 수집 안내이며 새 운전 조건이나 자동 완료 판정이 아닙니다.</p>
      ${plan.circuit_equipment?`<p><strong>OEM 회로의 참고 구성</strong> · ${esc(plan.circuit_equipment)}</p><p>${esc(plan.circuit_distinction)}</p><div class="inline-actions">${docLinks(plan.circuit_pages)}</div>`:'<p>본체·전용 제어기 또는 PLC 대응을 확인해야 합니다. 직접 제어 신호는 배정하지 않습니다.</p>'}
      ${plan.construction_boundary?`<details><summary>시공 자료의 연결 경계·페이지</summary><p>${esc(plan.construction_boundary)}</p><p class="muted">추가 시공도면은 승인·준공·현재 배선 확인 전입니다.</p><div class="inline-actions">${docLinks(plan.construction_pages)}</div></details>`:''}
      <details><summary>점검 전 확보할 근거</summary>${evidenceRequirements(plan.preflight)}<p>확인한 실물·현재 자료 근거는 아래 발생 상황에, 미확인 사항은 후속 확인란에 기록합니다.</p></details></section>`;
  }
  function fromRecord(record,schema){
    if(!record || record.equipment!==schema.key)throw new Error('invalid_repair_record');
    const result={time_zone:record.time_zone||''};
    for(const [key] of fields)result[key]=Array.isArray(record[key])?record[key].join('\n'):record[key]||'';
    result.record_status=statuses.includes(record.status)?record.status:statuses[0];
    for(const s of schema.signals){
      const old=(record.observations||[]).find(r=>r.id===s.id);
      for(const name of ['value','observed_at','evidence'])result[s.id+'_'+name]=old?.[name]||'';
    }
    for(const s of schema.steps)result['step_'+s.id]=(record.decision_observations||[]).find(r=>r.id===s.id)?.observation||'';
    return result;
  }
  function collect(schema,values,previous){
    if(previous && previous.equipment!==schema.key)throw new Error('invalid_repair_record');
    const text=k=>String(values[k]??'').trim().slice(0,30000);
    const record={...previous,schema_version:1,equipment:schema.key,name:schema.name,reference_plc_id:schema.reference_plc_id,
      status:statuses.includes(text('record_status'))?text('record_status'):statuses[0],
      field_verified:false,identity_confirmed:false,repairs_completed:0};
    record.time_zone=text('time_zone')||previous?.time_zone||null;
    for(const [key] of fields)record[key]=text(key)||null;
    record.cause_candidates=text('cause_candidates').split('\n').filter(Boolean);
    record.recovery_evidence=text('recovery_evidence').split('\n').filter(Boolean);
    record.unresolved=text('unresolved').split('\n').filter(Boolean);
    const oldSignals=previous?.observations||[];
    record.observations=schema.signals.map(s=>({...oldSignals.find(r=>r.id===s.id),id:s.id,
      name:s.name,role:s.role,addresses:s.addresses,source_refs:s.refs,
      value:text(s.id+'_value')||null,observed_at:text(s.id+'_observed_at')||null,evidence:text(s.id+'_evidence')||null}));
    record.observations.push(...oldSignals.filter(s=>!schema.signals.some(r=>r.id===s.id)));
    const oldSteps=previous?.decision_observations||[];
    record.decision_observations=schema.steps.map(s=>({...oldSteps.find(r=>r.id===s.id),id:s.id,title:s.title,
      source_manual:schema.manual+'#'+s.common,observation:text('step_'+s.id)||null}));
    record.decision_observations.push(...oldSteps.filter(s=>!schema.steps.some(r=>r.id===s.id)));
    return record;
  }
  function summary(record){
    return fields.filter(([key])=>record[key] && (!Array.isArray(record[key]) || record[key].length)).map(([key,label])=>label+'：'+(Array.isArray(record[key])?record[key].join('\n'):record[key])).concat(
      record.observations.filter(s=>s.value||s.observed_at||s.evidence).map(s=>s.name+'：'+(s.value||'미기록')+' / '+(s.observed_at||'시각 미기록')+' / '+(s.evidence||'근거 미기록')),
      record.decision_observations.filter(s=>s.observation).map(s=>s.title+'：'+s.observation)).join('\n\n');
  }
  function render(schema,draft,own){
    const zone=draft.time_zone||Intl.DateTimeFormat().resolvedOptions().timeZone;
    const input=(key,label,type='text')=>`<label>${esc(label)}${type==='textarea'?`<textarea name="${esc(key)}" maxlength="30000" ${key==='first_symptom'?'required':''}>${esc(draft[key]||'')}</textarea>`:`<input name="${esc(key)}" type="${type}" ${type==='datetime-local'?'step="1"':''} maxlength="${key==='title'?160:1000}" ${key==='title'?'required':''} value="${esc(draft[key]||'')}">`}</label>`;
    const roles={requests:'요청',outputs:'최종 출력',responses:'처리 응답'};
    return `<h2>수리 관찰 기록 · ${esc(schema.name)}</h2><div class="notice info">선택 항목 ${esc(schema.key)} · 참고 PLC ${esc(schema.reference_plc_id||'대응 미확정')} · 실물 동일성 확인 전. 직접 관찰한 값·시각·근거를 입력합니다. 이 기록은 현재 브라우저에 저장되며 원본 대장·PLC·수리 완료 상태를 변경하지 않습니다.</div>
      <div class="inline-actions"><button data-view="repair">수리 판단 근거</button><button data-view="review">관련 근거 검토</button><button data-view="notes">일반 작업 메모</button></div>${evidencePreflight(schema.evidence_plan)}
      <p class="muted">관찰 시각은 ${esc(zone)} 기준의 현지 시각이며 초 단위까지 입력할 수 있습니다. 다른 시스템의 알람 시각은 시각 기준을 근거에 함께 적습니다.</p><form id="repair-record-form" class="note-form repair-record-form"><input type="hidden" name="time_zone" value="${esc(zone)}"><input type="hidden" name="noteId" value="${esc(draft.noteId||'')}"><input type="hidden" name="base_note" value="${esc(draft.base_note||'')}">
      <section class="panel"><h2>1. 발생 상황·실물과 제어 경계</h2>${input('title','기록 제목')}<div class="form-row">${fields.slice(0,7).map(([k,l,t])=>input(k,l,t)).join('')}</div>${fields.slice(7,10).map(([k,l,t])=>input(k,l,t)).join('')}</section>
      <section class="panel"><h2>2. 신호 관찰 · ${schema.signals.length}개 참고 신호</h2><p>자료의 태그·주소는 관찰 대상을 찾기 위한 참고입니다. 실제 값·시각·수집 방법을 따로 기록하고 미확인 값은 비워 둡니다. 내부 요청·처리 응답만으로 물리 동작을 확정하지 않습니다.</p>${schema.signals.length?schema.signals.map(s=>`<details><summary>${esc(roles[s.role]||s.role)} · ${esc(s.name)} ${esc(s.addresses.join(', '))}</summary><p>${s.refs.map(r=>`<button type="button" data-doc="networks/network-${r.network}.html">원본 ${r.network} · ORef ${esc(r.oref)}</button>`).join(' ')}</p><div class="form-row">${input(s.id+'_value',s.name+' 관찰값')}${input(s.id+'_observed_at',s.name+' 관찰 시각','datetime-local')}</div>${input(s.id+'_evidence',s.name+' 수집 방법·근거 위치')}</details>`).join(''):'<p>PLC 대응을 확인하기 전입니다. 전용 제어기의 자료·실물 증상을 기록하고 다른 장치의 태그를 대신 사용하지 않습니다.</p>'}</section>
      <section class="panel"><h2>3. 증상별 비교·다음 확인</h2>${schema.steps.map(s=>`<details><summary>${esc(s.title)}</summary><p>${esc(s.observe)}</p><p>${esc(s.compare)}</p><p>${esc(s.next)}</p><button type="button" data-doc="${esc(schema.manual+'#'+s.common)}">판단 근거 열기</button>${evidenceRequirements(schema.evidence_plan?.steps.find(r=>r.step_id===s.id))}${input('step_'+s.id,s.title+' 관찰·비교 결과','textarea')}</details>`).join('')}</section>
      <section class="panel"><h2>4. 원인 후보·조치·복구와 후속 확인</h2>${fields.slice(10).map(([k,l,t])=>input(k,l,t)).join('')}<label>기록 구분<select name="record_status">${statuses.map(s=>`<option ${draft.record_status===s?'selected':''}>${s}</option>`).join('')}</select></label><p>관찰 기록·조치 기록·추가 확인 필요는 사용자 기록의 구분입니다. 현재 CPU·실물·복구 증거는 별도 확인 대상이며 이 화면에서 자동으로 수리 완료 처리하지 않습니다.</p><div class="inline-actions"><button type="submit">수리 기록을 브라우저에 저장</button><button type="button" data-export-notes>전체 메모·수리 기록 백업</button></div></section></form>
      <section class="panel"><h2>저장된 수리 기록 · ${own.length}건</h2>${own.length?own.map(n=>`<article class="saved-note"><h3>${esc(n.title)}</h3><small>${esc(n.updated)} · ${esc(n.repair_observation.status)}</small><p>${esc(n.text)}</p><button data-edit-repair="${esc(n.id)}">이 수리 기록 수정</button> <button data-export-repair="${esc(n.id)}">이 수리 기록 JSON</button></article>`).join(''):'<p>저장된 수리 관찰 기록이 없습니다.</p>'}</section>`;
  }
  root.GMERepairRecords={fields,statuses,keyFor,fromRecord,collect,summary,render};
})(typeof window!=='undefined'?window:{});
