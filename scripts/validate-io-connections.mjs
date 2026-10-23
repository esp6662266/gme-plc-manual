import assert from 'node:assert/strict';

export function validateConnections(notes,{resources,pages}) {
  const allowed=new Set(resources),pageKeys=new Set(pages.map(p=>p.source+'#page='+p.page));
  const addresses=new Set(notes.records.map(r=>r.address));
  let routes=0,nodes=0;
  const node=n=>{
    assert.ok(['device','contact','coil','wire','terminal'].includes(n.kind),'Invalid connection node kind');
    for(const key of ['label','query','location_label'])assert.ok(typeof n[key]==='string'&&n[key].length>=2&&n[key].length<=180,'Missing connection '+key);
    assert.ok(Number.isInteger(n.page)&&n.page>0&&Number.isInteger(n.fg),'Connection page/FG missing');
    assert.equal(n.url,notes.source+'#page='+n.page,'Connection must use reviewed original PDF page');
    assert.ok(allowed.has(notes.source)&&pageKeys.has(n.url),'Connection source page is not public');
    if(n.focus)assert.ok(Array.isArray(n.focus)&&n.focus.length===2&&n.focus.every(x=>Number.isFinite(x)&&x>=0&&x<=1),'Invalid connection focus');
    nodes++;
  };
  for(const record of notes.records){
    const t=record.trace;if(!t)continue;
    assert.equal(record.kind,'reference','Only reviewed explanations may have connection traces');
    assert.equal(t.schema_version,1);assert.equal(t.basis,'original_drawing_visual_comparison');
    assert.equal(t.source_sha256,notes.source_sha256,'Connection source hash mismatch');
    assert.ok(['wire','component'].includes(t.kind)&&Array.isArray(t.routes)&&t.routes.length,'Missing connection routes');
    const ids=new Set();
    for(const route of t.routes){
      assert.match(route.id,/^[a-z0-9-]+$/);assert.ok(!ids.has(route.id),'Duplicate route ID');ids.add(route.id);
      assert.ok(typeof route.title==='string'&&route.title&&Array.isArray(route.nodes)&&route.nodes.length>=2,'Invalid route');
      route.nodes.forEach(node);routes++;
    }
    if(t.parallel){assert.ok(t.parallel.title&&Array.isArray(t.parallel.nodes)&&t.parallel.nodes.length>=2);t.parallel.nodes.forEach(node);node(t.parallel.return_node);}
    assert.ok(Array.isArray(t.related)&&t.related.every(a=>addresses.has(a)&&a!==record.address),'Invalid related connection address');
    assert.ok(Array.isArray(t.unknowns)&&t.unknowns.length,'Field unknowns must remain explicit');
    if(t.coil)assert.ok(t.coil.a1&&t.coil.a2&&Number.isInteger(t.coil.page));
  }
  return {routes,nodes};
}
