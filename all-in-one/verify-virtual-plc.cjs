/* Behavioral checks against named source conditions, never field acceptance. */
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const loadedEngine = require('./assets/virtual-plc.js');
const E = loadedEngine.Machine ? loadedEngine : globalThis.GMEVirtualPLC;
const model = JSON.parse(fs.readFileSync(path.join(__dirname,'registers/program-model.json'),'utf8'));
const map = new Map(model.networks.map(n=>[n.id,n]));
const results=[];
function check(id, equipment, title, design, run) {
  try { const evidence=run();results.push({id,equipment,title,design,status:'passed',scope:'가상 모델 부분 시험',evidence}); }
  catch(error) { results.push({id,equipment,title,design,status:'failed',scope:'가상 모델 부분 시험',error:error.message}); }
}
const session=id=>new E.MotorSession(model.profiles[id],map);
const snap=s=>({networks:s.profile.networks,...s.machine.snapshot()});
for(const id of ['BC01','FN04']) {
  const p=model.profiles[id];
  check(id+'-V01',id,'정상 기동과 가상 피드백 응답',id+'-SIM-01',()=>{
    const s=session(id);s.start();s.advance(1000);
    assert.equal(s.machine.read(p.output),true);assert.equal(s.machine.read(p.feedback),true);
    assert.equal(s.machine.read(p.fault),false);return snap(s);
  });
  check(id+'-V02',id,'피드백 감시 시간 전후의 알람과 정지',id+'-SIM-02',()=>{
    const s=session(id);s.inject('no-feedback');s.start();s.step(0);s.advance(p.delay_ms);
    assert.equal(s.machine.read(p.fault),false,'감시 시간 도달 전');
    s.advance(100);assert.equal(s.machine.read(p.fault),true);assert.equal(s.machine.read(p.output),false);
    assert.equal(s.machine.read(p.command),false);return snap(s);
  });
  check(id+'-V03',id,'운전 중 인버터 이상 래치',id+'-SIM-03',()=>{
    const s=session(id);s.start();s.advance(1000);s.inject('inverter');s.advance(p.delay_ms+200);
    assert.equal(s.machine.read(p.inv_alarm),true);assert.equal(s.machine.read(p.output),false);return snap(s);
  });
  check(id+'-V04',id,'원인 해제만으로 래치 해소·재기동하지 않음',id+'-SIM-05',()=>{
    const s=session(id);s.inject('no-feedback');s.start();s.advance(p.delay_ms+300);s.inject('normal');s.advance(1000);
    assert.equal(s.machine.read(p.fault),true);assert.equal(s.machine.read(p.output),false);
    s.ack();assert.equal(s.machine.read(p.fault),false);assert.equal(s.machine.read(p.command),false);
    s.start();s.advance(1000);assert.equal(s.machine.read(p.output),true);assert.equal(s.machine.read(p.feedback),true);return snap(s);
  });
  check(id+'-V05',id,'미확인 기동 Flag를 0으로 단정하지 않음','',()=>{
    const s=session(id);s.machine.set(p.command,null);s.advance(100);
    assert.equal(s.machine.read(p.output),null);return snap(s);
  });
  check(id+'-V06',id,'정지 요청으로 가상 출력과 피드백 해제',id+'-SIM-03',()=>{
    const s=session(id);s.start();s.advance(1000);s.stop();s.advance(200);
    assert.equal(s.machine.read(p.output),false);assert.equal(s.machine.read(p.feedback),false);return snap(s);
  });
}
check('BC01-V07','BC01','세 허가 경로가 모두 없으면 출력 억제','BC01-SIM-04',()=>{
  const s=session('BC01');s.machine.set('Flag.R1_GATE_LOOP_ON',false);s.start();s.advance(1000);
  assert.equal(s.machine.read('Start BC01'),false);s.machine.set('Flag.Maintenance_ON',true);s.advance(1000);
  assert.equal(s.machine.read('Start BC01'),true);return snap(s);
});
check('BC01-V08','BC01','트립와이어 래치·조건부 리셋','BC01-SIM-03',()=>{
  const s=session('BC01');s.start();s.advance(1000);s.inject('tripwire');s.advance(100);
  assert.equal(s.machine.read('Allarm.BC_01_FC'),true);assert.equal(s.machine.read('Start BC01'),false);
  s.ack();assert.equal(s.machine.read('Allarm.BC_01_FC'),true);s.inject('normal');s.ack();
  assert.equal(s.machine.read('Allarm.BC_01_FC'),false);assert.equal(s.machine.read('Flag.M_BC_01'),false);return snap(s);
});
check('FN04-V07','FN04','풍량 설정 0과 TC09 상상한 조건에서 요청 해제','FN04-SIM-04',()=>{
  const s=session('FN04');s.machine.set('Data.SET_PERC_FN04',0);s.start();s.advance(100);
  assert.equal(s.machine.read('Start FN04'),false);s.machine.set('Data.SET_PERC_FN04',70);s.start();s.advance(1000);
  assert.equal(s.machine.read('Start FN04'),true);s.machine.set('Allarm.MAX_MAX_TC09',true);s.advance(100);
  assert.equal(s.machine.read('Start FN04'),false);return snap(s);
});
check('FN04-V08','FN04','관련 설비 피드백 상실의 90분 지연 정지','FN04-SIM-04',()=>{
  const s=session('FN04');s.start();s.advance(1000);s.machine.set('Inputs.VR03 Run',false);s.step(0);
  assert.equal(s.machine.read('Allarm.Prealarms_FN04'),true);
  s.advance(5399900,1000);assert.equal(s.machine.read('Start FN04'),true);
  s.advance(100);assert.equal(s.machine.read('Stop_Fan_FN04'),true);assert.equal(s.machine.read('Start FN04'),false);
  s.advance(100);assert.equal(s.machine.read('Flag.M_FN_04'),false);return snap(s);
});
check('SD-V01','','SD 시간 경계·입력 해제·다시 시작','',()=>{
  const n={id:'fixture',executable:true,actions:[{uid:'1',gate:'SdCoil',target:'t',name:'T',condition:{op:'read',key:'in'},preset:{op:'read',key:'pt'}}]};
  const m=new E.Machine([n],{in:true,pt:2000});m.scan(0);m.scan(1999);assert.equal(m.read('t'),false);
  m.set('pt',5000);m.scan(1);assert.equal(m.read('t'),true,'진행 중 PT는 시작 때 값');
  m.set('in',false);m.scan(0);assert.equal(m.read('t'),false);m.set('in',true);m.scan(0);m.scan(2000);
  assert.equal(m.read('t'),false);m.scan(3000);assert.equal(m.read('t'),true);return m.snapshot();
});
check('BOOL-V01','','미확인 조건의 3값 논리 진리표','',()=>{
  assert.equal(E.and([false,null]),false);assert.equal(E.and([true,null]),null);
  assert.equal(E.or([true,null]),true);assert.equal(E.or([false,null]),null);
  assert.equal(E.evaluate({op:'not',arg:{op:'read',key:'missing'}},{}),null);
  assert.equal(E.evaluate({op:'eq',left:{op:'const',value:0},right:{op:'const',value:false}},{}),null);
  return {truth_table:'unknown preserved; boolean and numeric types not coerced'};
});
check('BLOCK-V01','','미지원 네트워크는 시간·메모리 변경 전에 실행 보류','',()=>{
  const blocked=model.networks.find(n=>!n.executable);const m=new E.Machine([blocked]);
  assert.throws(()=>m.scan(100));assert.equal(m.time,0);assert.equal(m.scans,0);return {network:blocked.id,reasons:blocked.blockers};
});
const report={version:1,updated:new Date().toISOString(),engine_version:E.version,model_version:model.version,
  model_sha256:crypto.createHash('sha256').update(fs.readFileSync(path.join(__dirname,'registers/program-model.json'))).digest('hex'),
  passed:results.filter(r=>r.status==='passed').length,failed:results.filter(r=>r.status==='failed').length,
  full_design_tests_passed:0,plc_connected:false,tia_verified:false,
  scope:'지원 명령과 선택한 원본 네트워크의 가상 모델 행동 시험. 실제 Q/I 전달, 전체 호출, 전원 재시작과 현장 수락 시험은 포함하지 않음.',results};
fs.writeFileSync(path.join(__dirname,'registers/virtual-plc-test-results.json'),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify({passed:report.passed,failed:report.failed,failures:results.filter(r=>r.status==='failed')},null,2));
if(report.failed)process.exitCode=1;
