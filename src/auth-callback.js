import { handleAuthCallback } from '@netlify/identity';
if (/access_token|confirmation_token|recovery_token|invite_token|email_change_token/.test(location.hash)) {
  try { const result = await handleAuthCallback(); if(result) location.replace('/library/' + (['recovery','invite'].includes(result.type) ? '#password' : '')); }
  catch { location.replace('/library/'); }
}
