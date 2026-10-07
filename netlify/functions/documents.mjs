import { getStore } from '@netlify/blobs';
import { getUser } from '@netlify/identity';
import { createDocumentsHandler } from '../../src/documents-service.mjs';

export default createDocumentsHandler({
  getUser,
  getStore: () => getStore({ name: 'gme-private-documents', consistency: 'strong' }),
});
export const config = { path: ['/api/documents', '/api/documents/:familyId/:id'], method: ['GET', 'POST'] };
