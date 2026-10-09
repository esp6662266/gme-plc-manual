/* Deterministic, three-valued LAD subset. No network or real PLC interface. */
(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.GMEVirtualPLC = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';
  const key = name => String(name).replace(/"/g, '').toLowerCase();
  const bool = v => typeof v === 'boolean' ? v : null;
  const and = values => values.some(v => v === false) ? false : values.every(v => v === true) ? true : null;
  const or = values => values.some(v => v === true) ? true : values.every(v => v === false) ? false : null;
  function evaluate(ast, values) {
    if (!ast || typeof ast !== 'object') return null;
    if (ast.op === 'const') return ast.value;
    if (ast.op === 'read') return Object.hasOwn(values, ast.key) ? values[ast.key] : null;
    if (ast.op === 'unknown') return null;
    if (ast.op === 'and' || ast.op === 'or') return (ast.op === 'and' ? and : or)(ast.args.map(a => bool(evaluate(a, values))));
    if (ast.op === 'not') { const v = bool(evaluate(ast.arg, values)); return v === null ? null : !v; }
    const a = evaluate(ast.left, values), b = evaluate(ast.right, values);
    if (a === null || b === null || typeof a !== typeof b || (typeof a !== 'boolean' && (typeof a !== 'number' || !Number.isFinite(a) || !Number.isFinite(b)))) return null;
    if (ast.op === 'eq') return a === b;
    if (ast.op === 'ne') return a !== b;
    if (typeof a !== 'number') return null;
    if (ast.op === 'lt') return a < b;
    if (ast.op === 'le') return a <= b;
    if (ast.op === 'gt') return a > b;
    if (ast.op === 'ge') return a >= b;
    return null;
  }
  class Machine {
    constructor(networks, initial = {}) {
      this.networks = networks;
      this.values = {};
      for (const [name, value] of Object.entries(initial)) this.values[key(name)] = value;
      this.timers = {}; this.time = 0; this.scans = 0; this.trace = []; this.writes = [];
    }
    read(name) { return Object.hasOwn(this.values, key(name)) ? this.values[key(name)] : null; }
    set(name, value) {
      if (value !== null && typeof value !== 'boolean' && (typeof value !== 'number' || !Number.isFinite(value))) throw new Error('Only BOOL, finite numbers or unknown are allowed');
      this.values[key(name)] = value;
    }
    scan(dt = 0) {
      if (!Number.isFinite(dt) || dt < 0) throw new Error('Virtual time must be non-negative');
      const blocked = this.networks.filter(n => !n.executable);
      if (blocked.length) throw new Error('Blocked networks: ' + blocked.map(n => n.id).join(', '));
      this.time += dt; this.scans++; this.writes = [];
      for (const n of this.networks) {
        for (const a of n.actions) {
          const condition = bool(evaluate(a.condition, this.values));
          const before = this.read(a.target);
          let value = before;
          if (a.gate === 'Coil') value = condition;
          else if (a.gate === 'SCoil') value = condition === true ? true : condition === null && before !== true ? null : before;
          else if (a.gate === 'RCoil') value = condition === true ? false : condition === null && before !== false ? null : before;
          else if (a.gate === 'Move') {
            const candidate = evaluate(a.value, this.values);
            value = condition === true ? candidate : condition === null && candidate !== before ? null : before;
          } else if (a.gate === 'SdCoil') {
            const preset = evaluate(a.preset, this.values);
            const prev = this.timers[a.target];
            if (condition === false) {
              this.timers[a.target] = {active:false, since:null, preset:null, elapsed:0, network:n.id, uid:a.uid}; value = false;
            } else if (condition === null || typeof preset !== 'number' || !Number.isFinite(preset) || preset < 0) {
              this.timers[a.target] = {active:null, since:null, preset:null, elapsed:null, network:n.id, uid:a.uid}; value = null;
            } else {
              const since = prev?.active === true ? prev.since : this.time;
              const capturedPreset = prev?.active === true ? prev.preset : preset;
              const elapsed = this.time - since;
              this.timers[a.target] = {active:true, since, preset:capturedPreset, elapsed, network:n.id, uid:a.uid}; value = elapsed >= capturedPreset;
            }
          } else throw new Error('Unsupported action ' + a.gate);
          this.values[a.target] = value;
          const record = {time:this.time, scan:this.scans, network:n.id, uid:a.uid, gate:a.gate, name:a.name, condition, before, value};
          this.writes.push(record);
          if (value !== before) this.trace.push(record);
        }
      }
      this.trace = this.trace.slice(-500);
      return this.values;
    }
    snapshot() { return JSON.parse(JSON.stringify({time:this.time, scans:this.scans, values:this.values, timers:this.timers, writes:this.writes, trace:this.trace})); }
  }
  class MotorSession {
    constructor(profile, networkMap) {
      this.profile = profile;
      const initial = {...profile.defaults};
      for (const name of [profile.command, profile.output, profile.feedback, profile.inverter, profile.reset, profile.fault, profile.inv_alarm, profile.timer]) initial[name] = false;
      this.machine = new Machine(profile.networks.map(n => networkMap.get(n)), initial);
      this.fault = 'normal'; this.commandSince = null; this.feedbackStuck = false;
      this.machine.scan(0);
    }
    start() { this.machine.set(this.profile.command, true); }
    stop() { this.machine.set(this.profile.command, false); }
    ack() { this.machine.set(this.profile.reset, true); this.step(0); this.machine.set(this.profile.reset, false); }
    inject(fault) {
      this.fault = fault;
      this.feedbackStuck = this.machine.read(this.profile.feedback);
      this.machine.set(this.profile.inverter, fault === 'inverter');
      if (Object.hasOwn(this.profile.defaults, 'Inputs.BC01 trip wire')) this.machine.set('Inputs.BC01 trip wire', fault === 'tripwire');
    }
    step(dt) {
      if (!Number.isFinite(dt) || dt < 0) throw new Error('Virtual time must be non-negative');
      const m = this.machine, p = this.profile, nextTime = m.time + dt;
      const output = m.read(p.output);
      if (output === true && this.commandSince === null) this.commandSince = m.time;
      if (output !== true) this.commandSince = null;
      let feedback = output === null ? null : output === true && nextTime - this.commandSince >= 500;
      if (this.fault === 'no-feedback' || this.fault === 'inverter') feedback = false;
      if (this.fault === 'feedback-stuck') feedback = this.feedbackStuck;
      m.set(p.feedback, feedback);
      return m.scan(dt);
    }
    advance(ms, quantum = 100) {
      if (!Number.isFinite(ms) || ms < 0 || !Number.isFinite(quantum) || quantum <= 0 || ms / quantum > 100000) throw new Error('Invalid virtual advance');
      let remaining = ms;
      if (!remaining) this.step(0);
      while (remaining > 0) { const dt = Math.min(remaining, quantum); this.step(dt); remaining -= dt; }
      return this.machine.snapshot();
    }
  }
  return {version:'0.1.0', key, bool, and, or, evaluate, Machine, MotorSession};
});
