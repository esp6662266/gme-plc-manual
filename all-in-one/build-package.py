"""Package a checked local workspace, verify hashes and CRC before replacing ZIP."""
from pathlib import Path
import hashlib, json, shutil, zipfile, subprocess, sys
from datetime import datetime,timezone

ROOT=Path(__file__).resolve().parent
manifest=ROOT/'all-in-one-package-manifest.json'
archive=ROOT.parent/'GME-All-In-One-20261007.zip'
baseline=ROOT.parent/'GME-All-In-One-20261007-v0.3.zip'

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
# A previously saved passing report cannot authorize packaging new files.
# Run the source/link checks now and stop before archive mutation on failure.
verification_runs=[]
for verifier in ['verify-improvement-impact.py','verify-alarm-recovery.py','verify-burner-interface.py','verify-process-measurement.py','verify-sensor-measurement.py','verify-regulation-manual.py','verify-encoder-position.py','verify-hmi-transfer.py','verify-recipe-settings.py','verify-unresolved-identity.py','verify-body-manual.py','verify-requirements-audit.py','verify-all-in-one.py','verify-package.py']:
    run=subprocess.run([sys.executable,str(ROOT/verifier)],cwd=ROOT,text=True,capture_output=True)
    if run.returncode:
        print(run.stdout);print(run.stderr,file=sys.stderr);run.check_returncode()
    verification_runs.append(dict(script=verifier,script_sha256=sha(ROOT/verifier),finished_at_utc=datetime.now(timezone.utc).isoformat(),status='passed'))
prior=json.loads(manifest.read_text())
prior_files=prior if isinstance(prior,list) else prior['files']
source_files=[f for f in prior_files if f['file'].startswith(('sources/','PV01-detail/')) or f['file']=='assets/HMI_DECOATER.png']
assert source_files
for item in source_files:
    assert sha(ROOT/item['file'])==item['sha256'],item['file']
for name in ['all-in-one-verification.json','verification-result.json','improvement-impact-verification.json','alarm-recovery-verification.json','burner-interface-verification.json','process-measurement-verification.json','sensor-measurement-verification.json','regulation-manual-verification.json','encoder-position-verification.json','hmi-transfer-verification.json','recipe-settings-verification.json','unresolved-identity-verification.json','body-manual-verification.json','requirements-audit-verification.json']:
    assert json.loads((ROOT/name).read_text())['status']=='passed',name
assert json.loads((ROOT/'improvement-impact-verification.json').read_text())['impact_sha256']==sha(ROOT/'registers/improvement-impact.json')
assert json.loads((ROOT/'alarm-recovery-verification.json').read_text())['alarm_recovery_sha256']==sha(ROOT/'registers/alarm-recovery.json')
assert json.loads((ROOT/'burner-interface-verification.json').read_text())['burner_interface_sha256']==sha(ROOT/'registers/burner-interface.json')
assert json.loads((ROOT/'process-measurement-verification.json').read_text())['process_measurement_sha256']==sha(ROOT/'registers/process-measurement.json')
assert json.loads((ROOT/'sensor-measurement-verification.json').read_text())['sensor_measurement_sha256']==sha(ROOT/'registers/sensor-measurement.json')
assert json.loads((ROOT/'regulation-manual-verification.json').read_text())['regulation_manual_sha256']==sha(ROOT/'registers/regulation-manual.json')
assert json.loads((ROOT/'encoder-position-verification.json').read_text())['encoder_position_sha256']==sha(ROOT/'registers/encoder-position.json')
assert json.loads((ROOT/'hmi-transfer-verification.json').read_text())['hmi_transfer_sha256']==sha(ROOT/'registers/hmi-transfer.json')
assert json.loads((ROOT/'recipe-settings-verification.json').read_text())['recipe_settings_sha256']==sha(ROOT/'registers/recipe-settings.json')
assert json.loads((ROOT/'requirements-audit-verification.json').read_text())['requirements_audit_sha256']==sha(ROOT/'registers/requirements-audit.json')
assert json.loads((ROOT/'body-manual-verification.json').read_text())['body_manual_sha256']==sha(ROOT/'registers/body-manual.json')
lock=json.loads((ROOT/'registers/simulator-freeze.json').read_text())
for file,digest in lock['files'].items():assert sha(ROOT/file)==digest,file

files=[dict(file=str(p.relative_to(ROOT)),sha256=sha(p),bytes=p.stat().st_size) for p in sorted(ROOT.rglob('*')) if p.is_file() and p!=manifest and not any(part in ('__pycache__','.git') for part in p.parts) and p.name!='.DS_Store']
additional=json.loads((ROOT/'registers/additional-source-manifest.json').read_text())
for item in additional:assert sha(ROOT/item['file'])==item['sha256']
record=dict(fresh_verification_runs=verification_runs,version='0.4.0',date='2026-10-09',entry='index.html',simulator_development='stopped_by_user',simulator_behavior_tests='not_rerun',original_files_unchanged=len(source_files),additional_sources_verified=len(additional),field_verified=False,tia_verified=False,files=files)
manifest.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
temporary=archive.with_name('.GME-All-In-One-20261007.pending.zip')
with zipfile.ZipFile(temporary,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for item in files:z.write(ROOT/item['file'],ROOT.name+'/'+item['file'])
    z.write(manifest,ROOT.name+'/'+manifest.name)
with zipfile.ZipFile(temporary) as z:
    assert z.testzip() is None
    assert len(z.namelist())==len(files)+1
    for item in files:
        assert hashlib.sha256(z.read(ROOT.name+'/'+item['file'])).hexdigest()==item['sha256'],item['file']
    assert z.read(ROOT.name+'/'+manifest.name)==manifest.read_bytes()
if archive.exists() and isinstance(prior,list) and not baseline.exists():shutil.copy2(archive,baseline)
temporary.replace(archive)
report=dict(fresh_verifiers=len(verification_runs),finished_at_utc=datetime.now(timezone.utc).isoformat(),status='passed',archive=archive.name,version='0.4.0',files=len(files)+1,original_files_unchanged=len(source_files),additional_sources_verified=len(additional),simulator_development='stopped_by_user',simulator_behavior_tests='not_rerun',bytes=archive.stat().st_size,sha256=sha(archive),crc_checked=True,all_file_hashes_checked=True,field_verified=False,tia_verified=False)
(ROOT.parent/'GME-All-In-One-20261007.package-verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
