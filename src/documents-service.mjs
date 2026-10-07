import { createHash, randomUUID } from 'node:crypto';

export const MAX_FILE_SIZE = 4 * 1024 * 1024;
const categories = new Set(['manual', 'reference', 'report', 'backup', 'other']);
const extensions = new Set(['pdf','md','txt','csv','json','png','jpg','jpeg','webp','zip','zap18','ap18']);
const uuid = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
const headers = { 'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff' };
const json = (body, status=200) => Response.json(body, { status, headers });
const fail = (message, status) => json({ error: message }, status);
export function createDocumentsHandler(dependencies) {
  return async function documents(request) {
    try {
      const user = await dependencies.getUser();
      if (!user?.id) return fail('자료실 로그인이 필요합니다.', 401);
      const store = dependencies.getStore();
      const owner = encodeURIComponent(user.id);
      const prefix = `users/${owner}/families/`;
      const url = new URL(request.url);
      if (request.method === 'GET') {
        if (url.pathname === '/api/documents') {
          const { blobs } = await store.list({ prefix });
          const families = await Promise.all(blobs.map(blob => store.get(blob.key, { type: 'json' })));
          const documents = families.filter(Boolean).flatMap(family => family.versions);
          documents.sort((a,b) => b.createdAt.localeCompare(a.createdAt));
          return json({ documents });
        }
        const match = url.pathname.match(/^\/api\/documents\/([^/]+)\/([^/]+)$/);
        if (!match || !uuid.test(match[1]) || !uuid.test(match[2])) return fail('자료가 없습니다.', 404);
        const family = await store.get(prefix + match[1], { type: 'json' });
        const record = family?.versions.find(version => version.id === match[2]);
        if (!record) return fail('자료가 없습니다.', 404);
        const data = await store.get(`users/${owner}/files/${record.id}`, { type: 'arrayBuffer' });
        if (!data) return fail('파일을 찾지 못했습니다.', 404);
        return new Response(data, { headers: {
          ...headers, 'Content-Type': 'application/octet-stream',
          'Content-Disposition': `attachment; filename="document"; filename*=UTF-8''${encodeURIComponent(record.filename)}`,
          'Content-Security-Policy': 'sandbox',
        } });
      }
      if (request.method !== 'POST' || url.pathname !== '/api/documents') return fail('지원하지 않는 요청입니다.', 405);
      if (request.headers.get('origin') !== url.origin) return fail('다른 사이트에서 보낸 저장 요청은 허용되지 않습니다.', 403);
      const contentLength = Number(request.headers.get('content-length') || 0);
      if (contentLength > MAX_FILE_SIZE + 64 * 1024) return fail('파일은 최대 4MB까지 저장할 수 있습니다.', 413);
      const form = await request.formData();
      const title = String(form.get('title') || '').trim();
      const category = String(form.get('category') || 'other');
      const note = String(form.get('note') || '').trim();
      const previous = String(form.get('previousId') || '');
      const file = form.get('file');
      if (!title || title.length > 120 || note.length > 2000 || !categories.has(category)) return fail('제목·분류·변경 내용을 확인해 주세요.', 400);
      if (!(file instanceof File) || !file.size) return fail('저장할 파일을 선택해 주세요.', 400);
      if (file.size > MAX_FILE_SIZE) return fail('파일은 최대 4MB까지 저장할 수 있습니다.', 413);
      const filename = file.name.split(/[\\/]/).pop().replace(/[\u0000-\u001f\u007f]/g, '').slice(0,200);
      if (!extensions.has(filename.split('.').pop().toLowerCase())) return fail('지원하는 자료 형식이 아닙니다.', 400);
      let familyId = randomUUID(), existing = null;
      if (previous) {
        if (!uuid.test(previous)) return fail('개정할 자료를 확인해 주세요.', 400);
        familyId = previous;
        existing = await store.getWithMetadata(prefix + familyId, { type: 'json' });
        if (!existing?.data) return fail('개정할 자료가 없습니다.', 404);
        const expected = Number(form.get('previousVersion'));
        if (expected !== existing.data.versions.at(-1).version) return fail('다른 개정본이 먼저 저장됐습니다. 목록을 새로고침해 주세요.', 409);
      }
      const contents = await file.arrayBuffer();
      const record = {
        id: randomUUID(), familyId, version: existing ? existing.data.versions.at(-1).version + 1 : 1,
        title, category, note, filename, sizeBytes: contents.byteLength,
        sha256: createHash('sha256').update(Buffer.from(contents)).digest('hex'), createdAt: new Date().toISOString(),
      };
      const key = `users/${owner}/files/${record.id}`;
      await store.set(key, contents, { onlyIfNew: true });
      const family = { versions: [...(existing?.data.versions || []), record] };
      try {
        const result = await store.setJSON(prefix + familyId, family, existing ? { onlyIfMatch: existing.etag } : { onlyIfNew: true });
        if (!result.modified) {
          await store.delete(key);
          return fail('다른 개정본이 먼저 저장됐습니다. 목록을 새로고침해 주세요.', 409);
        }
      } catch (error) {
        await store.delete(key);
        throw error;
      }
      return json({ document: record, version: record.version }, 201);
    } catch {
      return fail('서버 자료실에 연결하지 못했습니다. 잠시 후 다시 확인해 주세요.', 503);
    }
  };
}
