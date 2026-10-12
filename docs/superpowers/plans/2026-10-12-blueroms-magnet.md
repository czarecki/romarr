# BlueRoms Magnet Resolution Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Pass BlueRoms PS4 releases to RDTClient as literal magnet URIs.

**Architecture:** Extend the Prowlarr search adapter with a narrowly scoped BlueRoms resolver. It validates the direct result URL, fetches the page, decodes the Base64 magnet, and lets the existing release and download-client pipeline continue unchanged.

**Tech Stack:** Python 3, requests, standard-library HTML parsing, pytest, Docker Compose

**Spec:** `docs/design/2026-10-12-blueroms-magnet-design.md`

## Global Constraints

- Affect only results whose indexer is BlueRoms.
- Fetch only HTTPS URLs on `blueroms.ws` or `www.blueroms.ws` under `/download/`.
- Never expose Prowlarr API keys or magnet contents in logs or browser responses.
- Preserve the existing Prowlarr download URL as fallback when resolution fails.

## Review Focus

- Malformed Base64 must not fail the whole search.
- Decoded non-magnet text must be rejected.
- A forged BlueRoms result must not cause an arbitrary server-side request.
- Other indexers must not incur an extra request or behavior change.
- A valid BlueRoms result must prefer the decoded magnet over the Prowlarr proxy URL.

---

### Task 1: Resolve BlueRoms magnets in the Prowlarr adapter

**Files:**
- Modify: `romarr/indexers.py`
- Modify: `tests/test_indexers.py`

**Interfaces:**
- Consumes: Prowlarr result dictionaries and the existing requests session.
- Produces: `Prowlarr.search()` releases whose `download_url` is a literal magnet for valid BlueRoms pages.

- [ ] **Step 1: Write failing regression and safety tests**
- [ ] **Step 2: Run `python -m pytest -q tests/test_indexers.py` and confirm the regression test fails because the proxy URL is retained**
- [ ] **Step 3: Implement the minimal allowlisted HTML/Base64 resolver and call it from `Prowlarr.search()`**
- [ ] **Step 4: Run the focused test and the complete pytest suite**
- [ ] **Step 5: Commit the tested source change**

### Task 2: Deploy and prove the live path

**Files:**
- Create: `/compose/romarr/patches/blueroms-magnet.patch`
- Modify: `/compose/romarr/Dockerfile`

**Interfaces:**
- Consumes: the reviewed Task 1 diff.
- Produces: a rebuilt `romarr-local` image running the tested resolver.

- [ ] **Step 1: Add the exact reviewed source diff as an image-build patch**
- [ ] **Step 2: Build and recreate only the ROMarr service**
- [ ] **Step 3: Verify health, search for the PS4 release, and confirm the held download URL is a literal magnet without printing it**
- [ ] **Step 4: Grab the selected release and confirm RDTClient accepts it**
