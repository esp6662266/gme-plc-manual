import { getUser, login, logout, signup, handleAuthCallback, requestPasswordRecovery, updateUser, getSettings } from '@netlify/identity';
const $ = id => document.getElementById(id);
const labels = { manual:'매뉴얼', reference:'참조 자료', report:'점검 기록', backup:'백업 자료', other:'기타' };
let records = [], busy = false;
const size = n => n >= 1048576 ? `${(n/1048576).toFixed(2)} MB` : `${(n/1024).toFixed(1)} KB`;
function status(message='') { $('status').textContent = message; }
function error(message='') { $('error').textContent = message; $('error').hidden = !message; }
function latest() { const map = new Map(); for (const record of records) if (!map.has(record.familyId) || map.get(record.familyId).version < record.version) map.set(record.familyId, record); return [...map.values()]; }
function node(tag, text, className) { const element = document.createElement(tag); element.textContent = text; if(className) element.className = className; return element; }
function render() {
  const families = latest(); $('record-count').textContent = families.length;
  const selected = $('previous-id').value; $('previous-id').replaceChildren(new Option('새 자료로 등록',''));
  for(const record of families) $('previous-id').add(new Option(`${record.title} · V${record.version}의 개정본`,record.familyId));
  if (families.some(record => record.familyId === selected)) $('previous-id').value = selected;
  const query = $('query').value.toLocaleLowerCase(), category = $('category').value;
  const visible = ($('history').checked ? records : families).filter(record => (category === 'all' || category === record.category) && `${record.title} ${record.filename} ${record.note}`.toLocaleLowerCase().includes(query));
  $('documents').replaceChildren(); $('empty').textContent = visible.length ? '' : (records.length ? '조건에 맞는 자료가 없습니다.' : '등록한 자료가 없습니다. 첫 자료를 저장해 보세요.');
  for(const record of visible) {
    const article = node('article','','document-card'); const meta = node('div','','document-meta');
    meta.append(node('span',labels[record.category]),node('span',`V${record.version}`),node('time',new Date(record.createdAt).toLocaleString('ko-KR')));
    article.append(meta,node('h3',record.title)); if(record.note) article.append(node('p',record.note,'document-note'));
    article.append(node('p',`${record.filename} · ${size(record.sizeBytes)}`,'document-file'));
    const details = node('details',''); details.append(node('summary','파일 무결성 확인'),node('p',`SHA-256: ${record.sha256}`)); article.append(details);
    const download = node('a','파일 내려받기','button document-download'); download.href = `/api/documents/${record.familyId}/${record.id}`; article.append(download); $('documents').append(article);
  }
}
async function refresh() {
  $('refresh').disabled = true; error();
  try { const response = await fetch('/api/documents',{cache:'no-store'}); const data = await response.json(); if(!response.ok) throw new Error(data.error || '목록을 읽지 못했습니다.'); records = data.documents; render(); }
  catch(e) { error(e.message); } finally { $('refresh').disabled = false; }
}
async function session() {
  const user = await getUser(); $('auth-panel').hidden = Boolean(user); $('signed-in').hidden = !user;
  if(user) { $('account').textContent = `${user.email} 계정의 자료실`; await refresh(); }
  else { records = []; $('documents').replaceChildren(); }
}
async function action(fn) { if(busy)return; busy=true; error(); for(const button of document.querySelectorAll('button')) button.disabled = true; try{await fn();}catch(e){error(e.name === 'MissingIdentityError' ? '자료실 로그인 서비스가 아직 준비되지 않았습니다. 관리자에게 문의해 주세요.' : e.message);}finally{busy=false; for(const button of document.querySelectorAll('button')) button.disabled=false;} }
$('login-form').addEventListener('submit',event => {event.preventDefault();void action(async()=>{await login($('email').value,$('password').value);$('password').value='';status();await session();});});
$('signup').addEventListener('click',()=>void action(async()=>{if(!$('login-form').reportValidity())return;await signup($('email').value,$('password').value);$('password').value='';status('등록 이메일의 확인 링크를 열어 계정을 확인해 주세요.');await session();}));
$('recovery').addEventListener('click',()=>void action(async()=>{if(!$('email').reportValidity())return;await requestPasswordRecovery($('email').value);status('비밀번호 설정 안내 메일을 확인해 주세요.');}));
$('logout').addEventListener('click',()=>void action(async()=>{await logout();status('로그아웃했습니다.');await session();}));
$('password-form').addEventListener('submit',event=>{event.preventDefault();void action(async()=>{await updateUser({password:$('new-password').value});$('new-password').value='';$('password-panel').hidden=true;status('비밀번호를 저장했습니다.');await session();});});
$('refresh').addEventListener('click',()=>void refresh());for(const id of ['query','category','history'])$(id).addEventListener('input',render);
$('upload-form').addEventListener('submit',event=>{event.preventDefault();void action(async()=>{
  const form=event.currentTarget, data=new FormData(form); const file=data.get('file');
  if(!file?.size || file.size>4*1024*1024)throw new Error('파일은 최대 4MB까지 저장할 수 있습니다.');
  const previous=latest().find(record=>record.familyId===data.get('previousId')); if(previous)data.set('previousVersion',String(previous.version));
  status('서버에 저장하는 중입니다…');const response=await fetch('/api/documents',{method:'POST',body:data});const result=await response.json();if(!response.ok){status();throw new Error(result.error||'저장하지 못했습니다.');}
  form.reset();status(`서버에 V${result.version} 자료를 저장했습니다.`);await refresh();
});});
try {
  const callback=await handleAuthCallback();
  if(callback?.type==='recovery'||callback?.type==='invite'||location.hash==='#password')$('password-panel').hidden=false;
  const settings=await getSettings();$('signup').hidden=settings.disableSignup;
  await session();
} catch(e) { error(e.name==='MissingIdentityError'?'자료실 로그인 서비스가 아직 준비되지 않았습니다. 관리자에게 문의해 주세요.':e.message); }
