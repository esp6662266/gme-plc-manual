import { readdir, readFile, writeFile, rm } from 'node:fs/promises';
import { join, relative } from 'node:path';
import { createHash } from 'node:crypto';
const legacy="default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'self'; form-action 'self'";
export async function buildHeaders(destination) {
  const oldFiles=[], hashes=new Set();
  async function walk(folder) {
    for (const entry of await readdir(folder,{withFileTypes:true})) {
      const f=join(folder,entry.name); if(entry.isDirectory()) await walk(f);
      else {
        const path=relative(destination,f).replaceAll('\\','/');
        if(!path.startsWith('all-in-one/') && path!=='_headers') oldFiles.push(path);
        else if(path.endsWith('.html')) {
          const html=await readFile(f,'utf8');
          for(const m of html.matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script\s*>/gi)) {
            if(!/\bsrc\s*=/i.test(m[1])) hashes.add("'sha256-"+createHash('sha256').update(m[2]).digest('base64')+"'");
          }
        }
      }
    }
  }
  await walk(destination);
  const rules=new Set(['/','/index.html','/index','/manual','/library','/library/','/library/*']);
  for(const file of oldFiles) { rules.add('/'+file); if(file.endsWith('.html')) rules.add('/'+file.slice(0,-5)); }
  const own="default-src 'self'; script-src 'self' "+[...hashes].sort().join(' ')+"; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'self'; form-action 'self'";
  const entries=[...['/all-in-one/','/all-in-one/*','/all-in-one'].map(route=>({route,policy:own,cache:'no-cache'})),...[...rules].sort().map(route=>({route,policy:legacy}))];
  const begin='# BEGIN GENERATED GME CSP', end='# END GENERATED GME CSP';
  const configFile=join(destination,'..','netlify.toml');
  let config=await readFile(configFile,'utf8');
  const beginAt=config.indexOf(begin),endAt=config.indexOf(end);
  if(beginAt>=0 && endAt>=beginAt) config=config.slice(0,beginAt)+config.slice(endAt+end.length);
  const block=entries.map(({route,policy,cache})=>'[[headers]]\n  for = '+JSON.stringify(route)+'\n  [headers.values]\n    Content-Security-Policy = '+JSON.stringify(policy)+(cache?'\n    Cache-Control = '+JSON.stringify(cache):'')).join('\n\n');
  const nextConfig=config.trimEnd()+'\n\n'+begin+'\n'+block+'\n'+end+'\n';
  if(process.env.NETLIFY==='true' && nextConfig!==await readFile(configFile,'utf8')) throw new Error('CSP generation changed: run npm run build locally and commit netlify.toml before deploying.');
  await writeFile(configFile,nextConfig);
  // A single committed config avoids remerging stale publish-folder rules.
  await rm(join(destination,'_headers'),{force:true});
  console.log(`CSP: ${hashes.size} exact inline script hashes; ${entries.length} scoped policies in netlify.toml; legacy policy retained`);
}
