"""Original XML/declaration, identity, scope, freeze and link checks; no PLC execution."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote,parse_qs
import json,hashlib,xml.etree.ElementTree as ET,re
R=Path(__file__).resolve().parent
sha=lambda f:hashlib.sha256((R/f).read_bytes()).hexdigest()
load=lambda f:json.loads((R/f).read_text())
tag=lambda n:n.tag.rsplit('}',1)[-1]
b=load('registers/unresolved-identity.json')
for f,h in b['sources'].items():assert sha(f)==h,f
assert b['counts']==dict(profiles=3,candidates=3,native_networks=4,assigned_signals=0,identity_verified=0)
assert {p['key'] for p in b['profiles']}=={'P03','P04','P14'}
assert {n['id'] for n in b['native']}=={424,425,1932,1933}
assert all(not p['plc_id'] and p['match']=='unknown' and not p['assigned_signals'] and not p['identity_verified'] and not p['field_verified'] for p in b['profiles'])
assert all(not c['assigned_to_priority'] and not c['identity_verified'] for c in b['candidates'])
assert not b['field_verified'] and not b['tia_verified'] and b['plc_changes']==0
review=load(b['independent_review']);assert review['confirmed_errors']==0 and review['reviewed_networks']==[424,425,1932,1933]
for f,h in review['source_hashes'].items():assert sha(f)==h
for f,h in load('registers/simulator-freeze.json')['files'].items():assert sha(f)==h,f
# Compare every exported native Part/Wire against the actual XML and every exact declaration occurrence.
for n in b['native']:
 proof=n['evidence'];tree=ET.parse(R/n['file']);parts={x.get('UId'):x for x in tree.iter() if tag(x)=='Part'};wires={x.get('UId'):x for x in tree.iter() if tag(x)=='Wire'}
 assert len(parts)==len(proof['parts']) and len(wires)==len(proof['wires'])
 for p in proof['parts']:
  x=parts[p['uid']];assert p['attributes']==dict(x.attrib) and p['negated']==[dict(c.attrib) for c in x if tag(c)=='Negated'] and p['templates']==[dict(attributes=dict(c.attrib),value=c.text) for c in x if tag(c)=='TemplateValue']
 for w in proof['wires']:assert w['endpoints']==[dict(kind=tag(c),attributes=dict(c.attrib)) for c in wires[w['uid']]]
 for ref in proof['references'].values():
  assert not ref['unresolved']
  for d in ref['declarations']:
   entries=ET.parse(R/'sources/decoded-original'/d['file']).getroot()
   entry=next(x for x in entries if any(tag(c)=='ID' and c.get('RID')==d['rid'] for c in x))
   ident=next(c for c in entry if tag(c)=='ID')
   occ=next(c for c in ident.iter() if tag(c)=='C' and c.get('UID')==d['uid'] and c.get('NID')==d['nid'])
   assert dict(occ.attrib)==d['occurrence'] and ident.get('S')==d['scope']
   assert d['constants']==[dict(c.attrib) for c in entry.iter() if tag(c)=='CB']
# Independently assert critical actual endpoints, negation and physical declaration offsets.
def original(f):return ET.parse(R/'sources/decoded-original'/f).getroot()
def wire(root,uid,*ends):
 x=next(x for x in root.iter() if tag(x)=='Wire' and x.get('UId')==uid)
 assert set(ends)<=set((tag(c),c.get('UId'),c.get('PinName')) for c in x),(uid,ends)
def declaration(file,rid,nid,uid,scope,area,offset):
 entry=next(x for x in original(file) if any(tag(c)=='ID' and c.get('RID')==rid for c in x));ident=next(c for c in entry if tag(c)=='ID')
 assert ident.get('S')==scope and any(c.get('UID')==uid and c.get('NID')==nid for c in ident.iter() if tag(c)=='C')
 assert any(c.get('R')==area for c in entry.iter() if tag(c)=='SAD') and any(c.get('AO')==offset for c in entry.iter() if tag(c)=='SSD')
for file,nid,oref,rid,ao,neg,setuid,resetuid,ws,wr,wreset in [('0234-FlgNet.xml','17','341','38','132','359','334','339','358','360','362'),('0235-FlgNet.xml','18','359','40','133','377','352','357','376','378','380')]:
 root=original(file);part=next(x for x in root.iter() if tag(x)=='Part' and x.get('UId')==neg);assert any(tag(x)=='Negated' and x.get('PinName')=='operand' for x in part)
 assert all(x.get('Gate') in ['Contact','SCoil','RCoil'] for x in root.iter() if tag(x)=='Part')
 wire(root,ws,('PCon',setuid,'in'));wire(root,wr,('PCon',neg,'out'));wire(root,wreset,('PCon',resetuid,'in'))
 declaration('0599-IdentXmlPart.xml',rid,nid,oref,'Global','Input',ao)
for file,nid,outuid,rid,ao,orgate,orwire,reset,output,neg4,neg5 in [('0239-FlgNet.xml','3','125','26','50','97','138','109','113','22','26'),('0240-FlgNet.xml','4','163','32','51','135','176','147','151','22','26')]:
 root=original(file)
 for uid in [neg4,neg5]:assert any(tag(c)=='Negated' for x in root.iter() if tag(x)=='Part' and x.get('UId')==uid for c in x)
 wire(root,'30',('PCon',orgate,'in4'));wire(root,'28',('PCon',orgate,'in5'));wire(root,orwire,('PCon',orgate,'out'),('PCon',reset,'in'))
 declaration('0602-IdentXmlPart.xml',rid,nid,outuid,'Global','Output',ao)
 assert sum(1 for w in root.iter() if tag(w)=='Wire' for c in w if tag(c)=='PCon' and c.get('UId')==orgate and c.get('PinName','').startswith('in'))==6
# Human supplied status does not imply field proof, and original inventory remains unchanged.
notes=load('registers/body-manual.json')['equipment_status_notes'];assert {n['id'] for n in notes}==({'MV04','SC12','PV04','P22','P23'} | ({'EV'+str(i).zfill(2) for i in range(1,91)} & {v['id'] for v in json.loads((R/'registers/control-spec.json').read_text())['specifications']}))
assert all(n['source_kind']=='user_statement' and n['exclude_from_current_detailed_analysis'] and not n['field_verified'] and n['historical_sources_preserved'] for n in notes)
assert load('registers/evidence-review.json')['counts']['source']==18
forms=load('registers/repair-record-forms.json')
for p in b['profiles']:
 f=next(x for x in forms['profiles'] if x['key']==p['key']);assert not f['signals'] and not f['identity_confirmed']
 assert f['evidence_plan']['sources']['registers/unresolved-identity.json']==sha('registers/unresolved-identity.json')
 assert all(any(x['path']=='unresolved-identity.html#identity-'+p['key'] for x in s['source_links']) for s in f['evidence_plan']['steps'])
 assert 'unresolved-identity.html#identity-'+p['key'] in (R/'repair-guides'/(p['key']+'.html')).read_text()
class Tags(HTMLParser):
 def __init__(self):super().__init__();self.ids=set();self.refs=[]
 def handle_starttag(self,t,a):
  a=dict(a)
  if 'id' in a:self.ids.add(a['id'])
  if 'href' in a:self.refs.append(a['href'])
def html(f):p=Tags();p.feed((R/f).read_text());return p
page=html('unresolved-identity.html')
assert {'identity-'+p['key'] for p in b['profiles']}|{'candidate-'+c['id'] for c in b['candidates']}|{'candidates','native'}<=page.ids
for path in page.refs:
 u=urlsplit(path);f=unquote(u.path) or 'unresolved-identity.html';assert (R/f).is_file(),path
 if u.fragment and f.endswith('.html'):
  if f=='index.html' and '=' in u.fragment:assert parse_qs(u.fragment)['equipment'][0] in ['P03','P04','P14']
  else:assert unquote(u.fragment) in html(f).ids,path
result=dict(status='passed',json_sha256=sha('registers/unresolved-identity.json'),html_sha256=sha('unresolved-identity.html'),profiles=3,native_networks=4,source_hashes=len(b['sources']),links=len(page.refs),original_xml_checked=True,critical_pins_and_declarations_checked=True,identity_assigned=0,scope_exclusions_checked=['MV04','SC12','PV04','P22','P23'],simulator_files_unchanged=True,simulator_behavior_tests='not_rerun',field_verified=False)
(R/'unresolved-identity-verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False))
