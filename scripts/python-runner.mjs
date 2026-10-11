import { spawn, spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { resolve } from 'node:path';

const versionCode='import sys,json; print(json.dumps(list(sys.version_info[:3])))';
export function findPython({env=process.env,platform=process.platform,probe=spawnSync}={}) {
  const explicit=env.GME_PYTHON;
  const candidates=explicit ? [[explicit,[]]] : [...(platform==='win32' ? [['py',['-3']]] : []),['python3',[]],['python',[]]];
  const failures=[];
  for(const [command,prefix] of candidates) {
    const result=probe(command,[...prefix,'-X','utf8','-c',versionCode],{env,encoding:'utf8',timeout:5000,windowsHide:true,shell:false});
    let version;
    try {version=JSON.parse(result.stdout || '');} catch {}
    if(!result.error && result.status===0 && Array.isArray(version) && version[0]===3 && version[1]>=10) return {command,prefix,version};
    failures.push(command+': '+(Array.isArray(version) ? version.join('.') : '실행 또는 버전 확인 실패'));
  }
  throw new Error('Python 3.10 이상이 필요합니다. Python을 설치하거나 GME_PYTHON에 실행 파일 경로를 지정하세요. '+failures.join('; '));
}
export async function runPython(args,{env=process.env,...options}={}) {
  const python=findPython({env,...options});
  if(args.length===1 && args[0]==='--check') {console.log('Python 준비 완료: '+python.command+' · '+python.version.join('.'));return 0;}
  const child=spawn(python.command,[...python.prefix,'-X','utf8',...args],{stdio:'inherit',env:{...env,PYTHONUTF8:'1',PYTHONOPTIMIZE:'0'},windowsHide:true,shell:false});
  const handlers=new Map(['SIGINT','SIGTERM'].map(signal=>[signal,()=>{if(!child.killed)child.kill(signal);}]));
  for(const [signal,handler] of handlers)process.on(signal,handler);
  try {return await new Promise((resolve,reject)=>{child.once('error',reject);child.once('exit',(code,signal)=>resolve(code ?? (signal==='SIGINT'?130:143)));});}
  finally {for(const [signal,handler] of handlers)process.off(signal,handler);}
}
if(process.argv[1] && resolve(process.argv[1])===fileURLToPath(import.meta.url)) {
  try {process.exitCode=await runPython(process.argv.slice(2));}catch(error){console.error(error.message);process.exitCode=1;}
}
