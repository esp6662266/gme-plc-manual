"""Validate static impact scope and native pins/call declarations, without execution."""
from pathlib import Path
from collections import Counter
import hashlib, json, xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parent
(ROOT/'improvement-impact-verification.json').write_text(json.dumps(dict(status='checking',scope='Current static source checks; no execution'))+'\n')
load=lambda f:json.loads((ROOT/f).read_text())
impact=load('registers/improvement-impact.json')
issues={r['id']:r for r in load('registers/improvement-review.json')['items']}
trace=load('registers/signal-trace.json')
native=load('registers/program-model.json')
nets={n['id']:n for n in native['networks']}
source_map={n['document_id']:n for n in load('sources/decoded-original/network-map.json')}
repair=load('registers/repair-decision.json')['records']
local=lambda x:x.tag.rsplit('}',1)[-1]
canon=lambda x:str(x).replace('"','').casefold()
xmls={n:ET.parse(ROOT/r['file']).getroot() for n,r in nets.items()}
assert len(impact['items'])==len(issues)==6
assert {r['id'] for r in impact['items']}==set(issues)
assert impact['changes_applied']==impact['field_verified']==impact['tia_verified']==0
assert impact['simulator_development']=='stopped_by_user' and impact['simulator_behavior_tests']=='not_rerun'
for f,digest in impact['sources'].items():assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==digest,f
pin_keys=set();call_keys=set();routes=set();proof_parts=0
for item in impact['items']:
    issue=issues[item['id']]
    assert item['original']==issue
    assert not item['field_verified'] and not item['tia_verified'] and item['changes_applied']==0
    assert item['simulator_behavior_tests']=='not_rerun'
    assert (ROOT/item['guide']).is_file()
    routes.add(item['guide'])
    owners={nets[n]['block'] for n in issue['networks']}
    for signal in item['signals']:
        assert signal['scope'] in ['Global','Local']
        expected=[r for r in trace['usages'] if r['scope']==signal['scope'] and canon(r['name'])==canon(signal['name']) and (signal['scope']!='Local' or r['block']==signal['block'])]
        assert expected==signal['usages'] and expected
        others=[r for r in trace['usages'] if canon(r['name'])==canon(signal['name']) and not (r['scope']==signal['scope'] and (signal['scope']!='Local' or r['block']==signal['block']))]
        assert signal['other_scope_usages']==others
        assert all(r['identity']==signal['identity'] for r in expected)
        assert signal['counts']==Counter(r['role'] for r in expected)
        assert signal['seed_uses']==[r for r in expected if r['network'] in issue['networks']]
        assert bool(signal['seed_uses']) or (item['id']=='IMP-03' and signal['name']=='Flag.Maintenance_ON')
        if signal['scope']=='Local':assert signal['name']=='Stop_Fan_FN04' and signal['block']=='motors 1'
        assert signal['shared_program_signal']==(signal['name']=='ON')
        if not signal['shared_program_signal']:owners.update(r['block'] for r in expected)
        for r in expected:
            pin_keys.add((r['network'],r['wire'],r['oref'],r['part'],r['pin']))
            assert r['file'] in impact['sources']
            assert all(d['file'] in impact['sources'] for d in r['declarations'])
            routes.add('networks/network-'+str(r['network'])+'.html')
        for r in others:
            assert r['file'] in impact['sources'] and all(d['file'] in impact['sources'] for d in r['declarations'])
            routes.add('networks/network-'+str(r['network'])+'.html')
    assert item['known_source_blocks']==sorted(owners)
    known=set(map(canon,owners))
    while True:
        expected_calls=[c for c in native['calls'] if c['callee'] and canon(c['callee']) in known]
        extended=known|{canon(c['caller']) for c in expected_calls}
        if extended==known:break
        known=extended
    assert Counter((c['network'],c['uid']) for c in expected_calls)==Counter((c['network'],c['uid']) for c in item['direct_calls_and_known_ancestors'])
    for call in item['direct_calls_and_known_ancestors']:
        n=nets[call['network']]
        original=next(c for c in expected_calls if c['network']==call['network'] and c['uid']==call['uid'])
        assert all(call[k]==v for k,v in original.items())
        assert call['source_file']==n['file'] and call['source_network_index']==n['index']==source_map[n['id']]['index_order']
        assert call['source_file'] in impact['sources']
        cref=next(x for x in xmls[n['id']].iter() if local(x)=='CRef' and x.get('UId')==call['uid'])
        code=next(x for x in cref if local(x)=='CodeBlock')
        assert code.get('UId')==call['block_uid'] and code.get('RefId')==call['block_ref_id'] and cref.get('RefId')==call['cref_ref_id']
        assert call['native_declarations']
        for d in call['native_declarations']:
            path='sources/decoded-original/'+d['file'];assert path in impact['sources']
            assert d['uid']==code.get('UId') and d['rid']==code.get('RefId') and d['name']==call['callee']
            assert d['nid']==source_map[n['id']]['inferred_original_nid']
            matched=False
            for node in ET.parse(ROOT/path).getroot():
                for ident in node:
                    if local(ident)=='ID' and ident.get('RID')==d['rid'] and ident.get('N')==d['name']:
                        if local(node)==d['kind'] and any(local(c)=='C' and c.get('UID')==d['uid'] and c.get('NID')==d['nid'] for c in ident.iter()):matched=True
            assert matched,(item['id'],call['network'],d)
            routes.add(path)
        call_keys.add((call['network'],call['uid']))
        routes.add('networks/network-'+str(call['network'])+'.html')
    assert item['unresolved_calls']==[c for c in native['calls'] if c['caller'] in owners and not c['callee']]
    assert [p['network'] for p in item['seed_evidence']]==issue['networks']
    for proof in item['seed_evidence']:
        n=nets[proof['network']];root=xmls[n['id']]
        assert proof['file']==n['file'] and proof['block']==n['block'] and proof['source_network_index']==n['index']
        assert hashlib.sha256((ROOT/proof['file']).read_bytes()).hexdigest()==proof['sha256']
        wanted={r['part'] for s in item['signals'] for r in s['seed_uses'] if r['network']==n['id']}
        assert {p['uid'] for p in proof['parts']}==wanted
        for p in proof['parts']:
            native_part=next(x for x in root.iter() if local(x)=='Part' and x.get('UId')==p['uid'])
            assert p['gate']==native_part.get('Gate')
            assert p['negated_pins']==[x.get('PinName') for x in native_part if local(x)=='Negated']
            connected=[w for w in root.iter() if local(w)=='Wire' and any(local(x)=='PCon' and x.get('UId')==p['uid'] for x in w)]
            assert [w['wire'] for w in p['connections']]==[w.get('UId') for w in connected]
            for w,original in zip(p['connections'],connected):
                for endpoint,x in zip(w['endpoints'],original):
                    assert len(w['endpoints'])==len(original)
                    assert (endpoint['kind'],endpoint['uid'],endpoint['pin'])==(local(x),x.get('UId'),x.get('PinName'))
                    if local(x)=='OCon':
                        operand=next(v for v in root.iter() if local(v)=='ORef' and v.get('UId')==x.get('UId'))
                        assert endpoint['ref_id']==operand.get('RefId') and endpoint['name']==n['refs'][x.get('UId')]['name']
            proof_parts+=1
        routes.add(proof['file'])
    primary=issue['equipment'].split('·')
    names={canon(s['name']) for s in item['signals'] if s['scope']=='Global' and not s['shared_program_signal']}
    assert item['primary_priority_keys']==[r['key'] for r in repair if r['plc_id'] in primary]
    assert item['reference_related_priority_keys']==[r['key'] for r in repair if r['plc_id'] and r['plc_id'] not in primary and any(canon(b['name']) in names for b in r['bindings'])]
    for key in item['primary_priority_keys']+item['reference_related_priority_keys']:routes.add('repair-guides/'+key+'.html')
    assert set(item['review_plan'])=={'baseline','documentation','plc_review','preserve','evidence','criteria'}
    assert all(item['review_plan'][k] for k in item['review_plan'])

# Specific ambiguities that must survive static analysis.
by_id={r['id']:r for r in impact['items']}
tag=next(s for s in by_id['IMP-01']['signals'] if s['name']=='Tag_66')
assert {(r['network'],r['part']) for r in tag['usages'] if r['role']=='write'}=={(1801,'854'),(1801,'908')}
for p in by_id['IMP-01']['seed_evidence'][0]['parts']:
    if p['uid'] in ['854','908']:
        operands=[x for w in p['connections'] for x in w['endpoints'] if x['kind']=='OCon']
        assert any(x['name']=='Tag_66' and x['ref_id']=='95' for x in operands)
        assert any(x['name']=='S5T#35S' for x in operands)
mv={p['uid']:p for p in by_id['IMP-02']['seed_evidence'][0]['parts']}
assert mv['915']['negated_pins']==mv['917']['negated_pins']==['operand']
maint={s['name']:s for s in by_id['IMP-03']['signals'] if s['name'].endswith('Maintenance_ON')}
assert maint['Allarm.Maintenance_ON']['identity']!=maint['Flag.Maintenance_ON']['identity']
assert not maint['Flag.Maintenance_ON']['seed_uses']
fn04=by_id['IMP-06'];calls=fn04['direct_calls_and_known_ancestors']
assert any(c['caller']=='main' and c['callee']=='Motors 1' and c['source_network_index']==9 for c in calls)
assert any(c['caller']=='main' and c['callee']=='Filter' and c['source_network_index']==9 for c in calls)
assert any(c['caller']=='main' and c['callee']=='Analog output conversion' and c['source_network_index']==10 for c in calls)
assert all((ROOT/r).is_file() for r in routes)
freeze=load('registers/simulator-freeze.json')
assert all(hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==digest for f,digest in freeze['files'].items())
report=dict(status='passed',date='2026-10-08',guides=6,selected_signals=sum(len(r['signals']) for r in impact['items']),
    impact_sha256=hashlib.sha256((ROOT/'registers/improvement-impact.json').read_bytes()).hexdigest(),
    unique_pin_references=len(pin_keys),unique_named_call_sites=len(call_keys),native_parts_checked=proof_parts,
    other_scope_references_preserved=sum(len(s['other_scope_usages']) for i in impact['items'] for s in i['signals']),
    source_hashes_checked=len(impact['sources']),document_routes=len(routes),
    field_verified=False,tia_verified=False,plc_changes=0,simulator_development='stopped_by_user',simulator_behavior_tests='not_rerun',
    scope='Exact source scope, native pin/wire/ref identities and call declarations; not execution')
(ROOT/'improvement-impact-verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
