# GME Search Usability Implementation Plan

> **Execution:** Follow the project instructions and existing user authorization. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Find a component or wire despite spelling differences, keep common circuits in scope, and show its location in preserved drawings with OCR candidates.

**Architecture:** Extend the existing vanilla search model and controls. Generate an offline source-hashed page map with native word coordinates, local Apple Vision OCR candidates and full-page previews; a separate lazy dialog displays matching boxes without modifying original PDFs.

**Tech Stack:** Vanilla JavaScript/CSS, Python pdfplumber/pypdfium2/Pillow, macOS Vision (offline generation only), Node test runner.

**Spec:** User approval of the four search improvements in this chat; existing search evidence in `docs/io-search/v1.25.0/`.

## Global Constraints

Preserve original PDF hashes, unknown/draft data, stopped simulator assets and existing history. No simulator execution, PLC/field/protection/SEJIN changes. OCR candidates remain distinct from reviewed functional explanations. Parent integrates all changes.

## Review Focus

- Spaced/hyphenated tags must retain whole-number boundaries and original display spelling.
- Equipment filtering must preserve common records by default and allow explicit exclusion.
- Empty or incorrect tags get explicit suggestions without automatic substitution.
- OCR failures, missing coordinates and image errors must retain original PDF access.
- Narrow screens, keyboard navigation, dialog close and return focus must work.

### Task 1: Search matching and scope

**Files:** `assets/io-search-model.js`, `assets/io-search.js`, `assets/io-search.css`, `assets/all-in-one.js` under `all-in-one/`; `tests/io-search.test.mjs`.
**Interfaces:** `search(records, query, {equipment, kind, includeCommon})`, `suggest(records, query)`; persisted `search-common=0`.

- [x] Add alias/boundary, common scope toggle and suggestion tests, implement matching and controls, run Node tests.

### Task 2: Drawing locations and OCR

**Files:** `scripts/build-drawing-search.py`, `scripts/drawing-ocr.swift`; `all-in-one/registers/drawing-search-pages.json`, page JSON and preview PNG directories; search builder; new viewer JS/CSS; generator entry.
**Interfaces:** source/page-keyed manifest, normalized top-left boxes, source and generated asset SHA256; `GMEIODrawingViewer.open({url, query, allowed})` and `close()`.

- [x] Generate all 330 preserved PDF pages locally; retain native upright words and confidence >=0.7 OCR identifier tokens with raw text/method.
- [x] Add OCR candidate records, verify source/asset hashes and boxes; implement accessible lazy viewer with automatic focus, zoom, match traversal and original link.
- [x] Check 8.9, 8.10, 13.6, 14KA6 and mobile UI against rendered originals.

### Task 3: Publish verified release

**Files:** version files, manifests, release/handoff/publication docs and evidence in `docs/io-search/v1.26.0/`.

- [x] Rebuild static manual/documents/search, run required package checks, original/frozen hashes, ZIP CRC/all hashes, npm tests/build and CSP checks.
- [ ] Commit complete sparse-checkout changes, push version tag, verify Netlify commit/ready and public files/UI, then record evidence.
- [ ] Check identifiable Dots availability; record actual result without inventing consultation or field completion.
