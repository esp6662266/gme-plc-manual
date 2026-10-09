"""Regenerate manual/review UI while preserving the frozen simulator/model files."""
from pathlib import Path
import hashlib, json, runpy

ROOT=Path(__file__).resolve().parent
frozen=['registers/program-model.json','assets/program-model-data.js','assets/virtual-plc.js','assets/simulator-workspace.js','registers/virtual-plc-test-results.json']
before={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in frozen}
lock=ROOT/'registers/simulator-freeze.json'
if lock.exists():
    assert before==json.loads(lock.read_text())['files'],'Simulator freeze hashes differ; review the user-requested scope before rebuilding'
for script in ['build-all-in-one.py','build-circuit-guides.py','build-construction-guide.py','build-signal-guides.py','build-common-guides.py','build-repair-guides.py','build-detailed-procedures.py','build-review-guides.py','build-improvement-impact.py','build-evidence-review.py','build-alarm-recovery.py','build-burner-interface.py','build-process-measurement.py','build-sensor-measurement.py','build-regulation-manual.py','build-encoder-position.py','build-hmi-transfer.py','build-recipe-settings.py','build-body-manual.py','build-unresolved-identity.py','build-repair-records.py','build-work-progress.py','build-requirements-audit.py','build-all-in-one.py']:
    runpy.run_path(str(ROOT/script),run_name='__main__')
assert before=={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in frozen},'Frozen simulator files changed during manual build'
print('Manual/review workspace regenerated; five simulator/model/result files unchanged.')
