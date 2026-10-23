# GME Component Reference Expansion Implementation Plan

> **Execution:** Follow the project instructions and existing user authorization. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Explain all 14KA1-14KA10 components and the directly relevant common emergency/power parts in unified search, with source-backed Korean roles and wiring paths.

**Architecture:** Extend the existing reviewed-reference register, preserving all six previous records and keeping shared components unassigned to exclusive equipment. Add per-record page/FG evidence, test exact-tag ranking and key source mappings, and reuse the v1.27 progressive search and drawing viewer.

**Tech Stack:** JSON content register, existing vanilla JavaScript search, Python/pypdf and full-page source renders, Node tests and current packaging pipeline.

**Spec:** User approved the next priority (component explanations) and explicitly requested goal mode in this chat. Scope is 14KA and its directly explanatory emergency/power context.

## Global Constraints

Preserve original PDFs, all six prior references, stopped simulator hashes, operational records/storage keys, excluded five assets and deferred drawing conflicts. No PLC/field/protection/SEJIN changes or simulator generation/execution. Source interpretation is distinct from current field safety/identity.

## Review Focus

- 14KA1 versus 14KA10 identifier boundaries must remain exact.
- Output14/13.5 and output24/13.6 coil groups must not be swapped.
- STO-related contact channels, actual drawing loads and parallel coil feeds require original page evidence.
- Common reference text must not assign a shared component exclusively to equipment.
- Original six references, OCR candidates and progressive loading behavior must remain intact.

### Task 1: Source review

**Files:** Read `all-in-one/sources/Electrical_Rev2.pdf`; existing full-page raster map. Write only parent-integrated evidence under `docs/io-search/v1.29.0/`.
**Interfaces:** Each reviewed tag has role, coil/power path, contact loads, PDF/FG pages and explicit unknowns.

- [x] Review complete source pages for 14KA1-10 and necessary 13KA1/15KA1/15KA2/transformer/coil-wire context; reconcile two independent read-only reports.

### Task 2: Register and validation

**Files:** `all-in-one/registers/io-search-reference-notes.json`, `tests/io-search.test.mjs`; generated index and version/data/manifest files.
**Interfaces:** Existing reference record schema with additive `evidence` metadata; exact `address` ranking and preserved shared `equipment: []`.

- [x] Add Korean reviewed explanations with source/FG references; retain existing six record bytes at record-content level.
- [x] Add meaningful regression assertions for tag ranking, coil groups, paired contacts, common scope, evidence links and old reference preservation; run tests.

### Task 3: Verified publication

**Files:** v1.29.0 version/package/manifest, ACTIVE-WORK, RELEASES, PUBLICATION_STATUS, WORKSPACE-HANDOFF and validation evidence.

- [ ] Rebuild only static manual, documents and search; pass mandatory14+2 checks, original/frozen hashes, ZIP CRC/all file hashes, npm tests/build and CSP checks.
- [ ] Check scoped search results and drawing opening on desktop/mobile; commit complete sparse-checkout changes, push fixed version tag and verify Netlify commit/ready, public assets and UI.
- [ ] Consult identifiable existing Dots target if available; record actual reply/unavailability, complete goal only when no required work remains.

## Workspace coordination

A separately authorized connection-tracing chat is writing v1.28.0 in the shared original checkout. This task uses an isolated Git worktree from d283760 and reserves v1.29.0 for source-backed explanation expansion. Integrate the other published change before final packaging; preserve its additive trace fields.
