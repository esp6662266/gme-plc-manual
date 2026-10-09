/* Data rules for local manual annotations; no source-register or PLC writes. */
((root) => {
  'use strict';
  function decodeNotes(raw, validEquipment) {
    const rows = JSON.parse(raw || '[]');
    if (!Array.isArray(rows) || rows.some(n => !n || typeof n !== 'object' || Array.isArray(n) ||
      ['id','title','text','equipment','updated'].some(k => typeof n[k] !== 'string') ||
      !validEquipment.has(n.equipment)) || new Set(rows.map(n => n.id)).size !== rows.length) {
      throw new Error('invalid_notes');
    }
    return rows;
  }
  function mergeNote(latest, original, next) {
    const current = latest.find(n => n.id === next.id);
    if (original ? !current || JSON.stringify(current) !== JSON.stringify(original) : current) {
      throw new Error('note_conflict');
    }
    return latest.filter(n => n.id !== next.id).concat({...current,...next});
  }
  function assertBase(original, raw) {
    if (original ? raw !== JSON.stringify(original) : raw) throw new Error('note_conflict');
  }
  function decodeDrafts(raw) {
    const value = JSON.parse(raw || '{}');
    if (!value || typeof value !== 'object' || Array.isArray(value)) throw new Error('invalid_drafts');
    return value;
  }
  function mergeDraft(raw, key, value, expected) {
    const latest = decodeDrafts(raw);
    if (value === null) {
      if (JSON.stringify(latest[key]) === expected) delete latest[key];
    } else {
      Object.defineProperty(latest,key,{value,enumerable:true,writable:true,configurable:true});
    }
    return latest;
  }
  const api = {decodeNotes,mergeNote,assertBase,decodeDrafts,mergeDraft};
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.GMENoteStore = api;
})(typeof window !== 'undefined' ? window : {});
