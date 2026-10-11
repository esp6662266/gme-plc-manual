#!/usr/bin/env python3
"""Read GME registers and check the committed rollout inventory. Never run generators."""
import argparse
import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

INPUTS = (
    'all-in-one/registers/equipment.json',
    'all-in-one/registers/priority-equipment.csv',
    'all-in-one/registers/requirements-audit.json',
    'all-in-one/registers/all-in-one-data.json',
)
SNAPSHOT = 'docs/equipment-standard/INVENTORY.json'


def unique(rows, key, label):
    values = [row[key] for row in rows]
    if any(not v for v in values) or len(values) != len(set(values)):
        raise ValueError(f'{label}: empty or duplicate {key}')
    return {row[key]: row for row in rows}


def identity_flag(value):
    if value is True or value == 'True' or value == 'true':
        return True
    if value is False or value == 'False' or value == 'false':
        return False
    raise ValueError('invalid identity_verified value')


def read_inventory(root):
    hashes = {}
    for name in INPUTS:
        path = root / name
        if path.is_symlink() or not path.is_file():
            raise ValueError(f'missing or symlink source: {name}')
        hashes[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    equipment = json.loads((root / INPUTS[0]).read_text(encoding='utf-8-sig'))
    with (root / INPUTS[1]).open(encoding='utf-8-sig', newline='') as source:
        priority = list(csv.DictReader(source))
    audit = json.loads((root / INPUTS[2]).read_text(encoding='utf-8-sig'))
    app = json.loads((root / INPUTS[3]).read_text(encoding='utf-8-sig'))
    by_id = unique(equipment, 'id', 'catalog')
    priority_by_key = unique(priority, 'key', 'priority')
    audit_ids = unique(audit['equipment'], 'id', 'audit')
    app_ids = unique(app['equipment'], 'id', 'app catalog')
    if set(by_id) != set(audit_ids) or set(by_id) != set(app_ids):
        raise ValueError('catalog/audit/app ID sets differ')
    for ident, row in by_id.items():
        for label, derived in [('audit', audit_ids[ident]), ('app', app_ids[ident])]:
            for field in ['name', 'kind', 'group', 'parent']:
                if (row.get(field) or '') != (derived.get(field) or ''):
                    raise ValueError(f'{label} catalog metadata differs: {ident}.{field}')
    for label, derived_rows in [('audit', audit['priority']), ('app', app['priority'])]:
        derived = unique(derived_rows, 'key', f'{label} priority')
        if set(derived) != set(priority_by_key):
            raise ValueError(f'{label} priority key sets differ')
        for key, row in priority_by_key.items():
            for field in ['name', 'plc_id', 'match', 'note']:
                if (row[field] or '') != (derived[key][field] or ''):
                    raise ValueError(f'{label} priority mapping differs: {key}.{field}')
            if identity_flag(row['identity_verified']) != identity_flag(derived[key]['identity_verified']):
                raise ValueError(f'{label} priority identity differs: {key}')
    rank = {}
    for row in equipment:
        seen = {row['id']}
        parent = row.get('parent', '')
        depth = 0
        while parent:
            if parent not in by_id or parent in seen:
                raise ValueError(f'unknown or cyclic parent: {row["id"]} -> {parent}')
            seen.add(parent)
            depth += 1
            parent = by_id[parent].get('parent', '')
        rank[row['id']] = depth
    notes = {n['id']: n for n in app['equipment_status_notes'] if n.get('id')}
    excluded = {i for i, n in notes.items() if i in by_id and n.get('exclude_from_current_detailed_analysis')}
    # Assert every declared range is represented by source status notes; never invent missing IDs.
    for definition in app['manual_exclusion_ranges']:
        if not definition.get('exclude_from_current_detailed_analysis'):
            continue
        prefix = definition['prefix']
        for ident in by_id:
            suffix = ident.removeprefix(prefix)
            if ident.startswith(prefix) and suffix.isdigit() and definition['start'] <= int(suffix) <= definition['end']:
                if ident not in excluded:
                    raise ValueError(f'exclusion range missing status note: {ident}')
    excluded_priority = set(app['excluded_priority'])
    if not excluded_priority.issubset({p['key'] for p in priority}):
        raise ValueError('excluded priority key absent from register')
    matched = {}
    for p in priority:
        ident = p['plc_id']
        if ident:
            if ident not in by_id or ident in matched:
                raise ValueError(f'unknown or duplicate priority target: {ident}')
            matched[ident] = p
        if p['match'] not in {'tag', 'candidate', 'unknown'} or bool(ident) != (p['match'] != 'unknown'):
            raise ValueError(f'inconsistent identity mapping: {p["key"]}')
    held = {}
    for row in equipment:
        if row['id'] in excluded:
            continue
        parent = row.get('parent', '')
        while parent:
            if parent in excluded:
                held[row['id']] = parent
                break
            parent = by_id[parent].get('parent', '')
    priority_rows = []
    for p in priority:
        state = ('excluded' if p['key'] in excluded_priority else
                 'reference_baseline' if p['plc_id'] == 'BC01' else
                 'identity_review' if p['match'] != 'tag' else 'planned')
        priority_rows.append({
            'priority_key': p['key'], 'name': p['name'], 'catalog_id': p['plc_id'] or None,
            'mapping': p['match'], 'identity_verified': identity_flag(p['identity_verified']),
            'queue_state': state, 'note': p['note'],
        })
    catalog_rows = []
    for row in sorted(equipment, key=lambda x: (rank[x['id']], x['group'], x['id'])):
        ident = row['id']
        p = matched.get(ident)
        state = ('excluded' if ident in excluded else 'parent_scope_hold' if ident in held else
                 'reference_baseline' if ident == 'BC01' else
                 'identity_review' if p and p['match'] == 'candidate' else 'planned')
        phase = 'excluded' if ident in excluded else 'hold' if ident in held else 'phase1' if p else 'phase2'
        catalog_rows.append({
            'catalog_id': ident, 'name': row['name'], 'kind': row['kind'], 'group': row['group'],
            'parent_id': row.get('parent') or None, 'depth': rank[ident],
            'priority_key': p['key'] if p else None, 'phase': phase, 'queue_state': state,
            'hold_parent': held.get(ident), 'exclusion_reason': notes[ident]['label'] if ident in excluded else None,
            'existing_detail': audit_ids[ident]['detail_level'],
            'bc01_standard_acceptance': 'reference_only' if ident == 'BC01' else 'not_assessed',
        })
    counts = dict(
        catalog=len(equipment), root_assets=sum(not e.get('parent') for e in equipment),
        child_assets=sum(bool(e.get('parent')) for e in equipment), priority_rows=len(priority),
        priority_excluded=len(excluded_priority), priority_in_scope=len(priority)-len(excluded_priority),
        priority_mapped=len(matched), priority_tag=sum(p['match']=='tag' for p in priority),
        priority_candidate=sum(p['match']=='candidate' for p in priority),
        priority_unmapped=sum(not p['plc_id'] for p in priority),
        catalog_excluded=len(excluded), excluded_parent_hold=len(held),
        phase1_catalog=sum(r['phase']=='phase1' for r in catalog_rows),
        phase2_candidates=sum(r['phase']=='phase2' for r in catalog_rows),
        symptom_reference_assets=sum(bool(r['symptom_detail']) for r in audit['equipment']),
        remaining_without_symptom_reference=sum(not r['symptom_detail'] for r in audit['equipment']),
    )
    if sum(Counter(r['phase'] for r in catalog_rows).values()) != len(by_id):
        raise ValueError('catalog partition mismatch')
    return {'schema_version': 1, 'standard_version': '1.0.0',
            'policy': 'deduplicate_actual_ids_keep_existing_exclusions',
            'source_sha256': hashes, 'counts': counts,
            'priority': priority_rows, 'catalog': catalog_rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[4])
    parser.add_argument('--emit-json', action='store_true', help='print a derived inventory; writes no files')
    args = parser.parse_args()
    try:
        root = args.repo.resolve()
        current = read_inventory(root)
        if args.emit_json:
            print(json.dumps(current, ensure_ascii=False, indent=2))
            return 0
        saved = json.loads((root / SNAPSHOT).read_text(encoding='utf-8'))
        drift = [k for k in current if k != 'source_sha256' and current[k] != saved.get(k)]
        if drift:
            raise ValueError('inventory drift; review before assigning work: ' + ', '.join(drift))
        changed_hashes = [p for p, sha in current['source_sha256'].items() if saved['source_sha256'].get(p) != sha]
        print(json.dumps({'inventory_matches': True, 'counts': current['counts'],
                          'source_byte_changes': changed_hashes,
                          'meaning': 'queue consistency only; no document, UI, TIA or field acceptance'}, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f'GME preflight failed: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
