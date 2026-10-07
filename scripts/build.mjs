import { mkdir, cp, readFile, writeFile, readdir, stat } from 'node:fs/promises';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { build } from 'esbuild';
const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const source = resolve(root, 'manual');
const destination = resolve(root, 'dist');
await mkdir(destination, { recursive: true });
await cp(source, destination, { recursive: true });
for (const name of ['index.html', 'manual.html']) {
  const filename = resolve(destination, name);
  let html = await readFile(filename, 'utf8');
  html = html.replace('</nav>', '<a href="/library/">서버 자료실</a></nav>');
  html = html.replace('이 홈페이지는 저장된 문서를 보여주는 파일이며', '이 홈페이지는 기술 자료를 제공하며');
  html = html.replace('</body>', '<script type="module" src="/auth-callback.js"></script></body>');
  await writeFile(filename, html);
}
await mkdir(resolve(destination, 'library'), { recursive: true });
await cp(resolve(root, 'src/library.html'), resolve(destination, 'library/index.html'));
await cp(resolve(root, 'src/library.css'), resolve(destination, 'library/library.css'));
await build({ entryPoints: [resolve(root, 'src/library.js')], outfile: resolve(destination, 'library/library.js'), bundle: true, format: 'esm', platform: 'browser', target: 'es2022', minify: true });
await build({ entryPoints: [resolve(root, 'src/auth-callback.js')], outfile: resolve(destination, 'auth-callback.js'), bundle: true, format: 'esm', platform: 'browser', target: 'es2022', minify: true });
let count = 0;
async function walk(folder) { for (const item of await readdir(folder)) { const path = resolve(folder, item); if ((await stat(path)).isDirectory()) await walk(path); else count++; } }
await walk(destination);
console.log(`GME 매뉴얼 홈페이지: ${count}개 공개 파일 준비 완료`);
