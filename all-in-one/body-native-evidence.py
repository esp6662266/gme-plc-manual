"""Read native XML pins/declarations without evaluating logic or writing sources."""
from collections import defaultdict
from functools import cache
import re,xml.etree.ElementTree as ET
TAG=lambda x:x.tag.rsplit('}',1)[-1]
UNESC=lambda s:re.sub(r'_x([0-9a-fA-F]{4})_',lambda m:chr(int(m[1],16)),str(s))
def collect(root,nets,mapping,declarations,source_hash):
    by_key=defaultdict(list)
    for d in declarations:by_key[(d['uid'],d['rid'],d['nid'],d['name'])].append(d)
    @cache
    def entries(path):
        source_hash(path)
        return list(ET.parse(root/path).getroot())
    def declaration(d):
        path='sources/decoded-original/'+d['file']
        for entry in entries(path):
            ident=next((x for x in entry if TAG(x)=='ID'),None)
            if ident is None or ident.get('RID')!=d['rid']:continue
            occurrence=next((x for x in ident.iter() if TAG(x)=='C' and x.get('UID')==d['uid'] and x.get('NID')==d['nid']),None)
            if occurrence is None:continue
            name=UNESC(ident.get('N','')) or '.'.join(UNESC(x.get('N')) for x in entry.iter() if TAG(x)=='AO' and x.get('N'))
            constants=[dict(x.attrib) for x in entry.iter() if TAG(x)=='CB']
            if not name and constants:name=UNESC(constants[0].get('SV',constants[0].get('V','')))
            assert name==d['name'],(path,name,d)
            return dict(**d,scope=ident.get('S'),occurrence=dict(occurrence.attrib),types=[dict(x.attrib) for x in entry.iter() if TAG(x)=='TD'],constants=constants)
        raise AssertionError(('Missing declaration',d))
    def native(i):
        n=nets[i];r=ET.parse(root/n['file']).getroot();nid=mapping[i]['inferred_original_nid']
        parts=[dict(uid=x.get('UId'),gate=x.get('Gate'),attributes=dict(x.attrib),negated=[dict(c.attrib) for c in x if TAG(c)=='Negated'],templates=[dict(attributes=dict(c.attrib),value=c.text) for c in x if TAG(c)=='TemplateValue']) for x in r.iter() if TAG(x)=='Part']
        references={}
        for x in r.iter():
            if TAG(x)!='ORef':continue
            uid=x.get('UId');rid=x.get('RefId');indexed=n['refs'].get(uid)
            assert indexed and indexed['ref_id']==rid,(i,uid)
            name=indexed.get('name');matches=by_key[(uid,rid,nid,name)]
            references[uid]=dict(uid=uid,rid=rid,nid=nid,name=name,declarations=[declaration(d) for d in matches],unresolved=name is None or not matches)
        wires=[dict(uid=x.get('UId'),endpoints=[dict(kind=TAG(c),attributes=dict(c.attrib)) for c in x]) for x in r.iter() if TAG(x)=='Wire']
        # Call/instance nodes are preserved as raw native trees, including uninterpreted refs.
        def tree(x):return dict(tag=TAG(x),attributes=dict(x.attrib),text=x.text,children=[tree(c) for c in x])
        calls=[tree(x) for x in r.iter() if TAG(x) in ['CRef','LRef']]
        return dict(network=i,inferred_nid=nid,parts=parts,references=references,wires=wires,call_nodes=calls)
    return native
