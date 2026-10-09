import { readdir, readFile, writeFile } from 'node:fs/promises';
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
        if(!path.startsWith('all-in-one/')) oldFiles.push(path);
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
  let text='# Generated; legacy authentication documents retain their original CSP.\n';
  for(const route of [...rules].sort()) text+=route+'\n  Content-Security-Policy: '+legacy+'\n\n';
  for(const route of ['/all-in-one','/all-in-one/*']) text+=route+'\n  Content-Security-Policy: '+own+'\n  Cache-Control: no-cache\n\n';
  await writeFile(join(destination,'_headers'),text);
  console.log(`CSP: ${hashes.size} exact inline script hashes; legacy policy retained`);
}
