# SecondSelf — Edge Cases & Corner Scenarios

This document catalogs edge cases, failure modes, and corner scenarios for the SecondSelf project. Use it during **Phase 7 (Local Edge & QA Test)** and before **Phase 8 (Deploy)**.

**Related docs:** [architecture.md](./architecture.md) · [Implementation-plan.md](./Implementation-plan.md) · [problemstatement.md](./problemstatement.md)

---

## How to Use This Document

| Column | Meaning |
|--------|---------|
| **ID** | Reference code for bugs/tests |
| **Priority** | `P0` = must handle before deploy · `P1` = should handle · `P2` = nice to have |
| **Component** | Which module is affected |
| **Expected Behavior** | What the system should do |
| **Mitigation** | How to implement or test the fix |

---

## 1. Capture Pipeline (`capture.py`)

### 1.1 Input Validation

| ID | Scenario | Priority | Expected Behavior | Mitigation |
|----|----------|----------|-------------------|------------|
| CAP-01 | Empty note text (`python capture.py note ""`) | P0 | Reject with clear error: "Note text cannot be empty" | Validate before writing; exit code 1 |
| CAP-02 | Whitespace-only note (`"   "`) | P0 | Treat as empty; reject | Strip whitespace before validation |
| CAP-03 | Missing subcommand (no `note`/`link`/`file`) | P1 | Print usage help via argparse | Use `argparse` with required subparsers |
| CAP-04 | Invalid URL (no scheme, malformed) | P1 | Reject or warn: "Invalid URL format" | Basic regex: must start with `http://` or `https://` |
| CAP-05 | URL with trailing spaces or quotes | P1 | Strip and save clean URL | `url.strip().strip('"').strip("'")` |
| CAP-06 | File path does not exist | P0 | Error: "File not found: {path}" | `Path.exists()` check before copy |
| CAP-07 | File path is a directory | P1 | Error: "Path is a directory, not a file" | `Path.is_file()` check |
| CAP-08 | File with no read permission | P1 | Error: "Permission denied" | Catch `PermissionError` |
| CAP-09 | Very long note (50,000+ chars) | P2 | Capture succeeds; may truncate in LLM later | Log warning if > 10k chars; no hard block |
| CAP-10 | Note with special characters / emoji / Unicode | P1 | Save correctly as UTF-8 | Always open files with `encoding="utf-8"` |
| CAP-11 | Note with newlines in shell (multiline) | P2 | Support via heredoc or `@file` input | Document: `python capture.py note "$(cat note.txt)"` |
| CAP-12 | Duplicate capture of same content | P2 | Allow — each gets unique ID | By design; dedup is optional future feature |

### 1.2 File Handling

| ID | Scenario | Priority | Expected Behavior | Mitigation |
|----|----------|----------|-------------------|------------|
| CAP-13 | Large file (> 50 MB) | P1 | Warn or reject with size limit | Config: `MAX_FILE_SIZE_MB = 50` |
| CAP-14 | Binary file (`.exe`, `.zip`) | P2 | Copy binary; classify may fail gracefully | Store as-is; classify extracts filename only |
| CAP-15 | Image file (`.png`, `.jpg`) | P2 | Copy file; no OCR in v1 | meta.json type=file; body = filename + optional caption |
| CAP-16 | PDF file | P1 | Copy PDF; extract text in classify phase | Use `pypdf` in `classify.py`, not capture |
| CAP-17 | Filename with spaces or special chars | P1 | Sanitize filename on copy | Use `Path.name`; avoid path traversal |
| CAP-18 | Path traversal attempt (`../../etc/passwd`) | P0 | Resolve to absolute path; reject if outside allowed dir | `Path.resolve()` + boundary check |
| CAP-19 | Same file captured twice | P2 | Two separate captures with different IDs | Expected behavior |
| CAP-20 | File deleted after capture reference | P1 | N/A at capture time | Only applies if referencing external path |

### 1.3 ID & Storage

| ID | Scenario | Priority | Expected Behavior | Mitigation |
|----|----------|----------|-------------------|------------|
| CAP-21 | UUID collision (extremely rare) | P2 | Regenerate UUID | Loop until unique folder name |
| CAP-22 | `raw/` directory does not exist | P0 | Auto-create on first capture | `RAW_DIR.mkdir(parents=True, exist_ok=True)` |
| CAP-23 | Disk full during write | P1 | Catch `OSError`; print clear error | try/except around file writes |
| CAP-24 | Invalid/corrupt `meta.json` from manual edit | P2 | Skip or error in classify with message | Validate JSON schema in classify |
| CAP-25 | Capture folder missing `content.txt` | P1 | classify skips with warning | Check required files before processing |

---

## 2. Auto-Classification (`classify.py`)

### 2.1 LLM & API

| ID | Scenario | Priority | Expected Behavior | Mitigation |
|----|----------|----------|-------------------|------------|
| CLS-01 | Missing `GROQ_API_KEY` | P0 | Clear error: "Set GROQ_API_KEY in .env" | Check env at startup; fail fast |
| CLS-02 | Invalid/expired API key | P0 | Error: "Authentication failed" | Catch 401 from Groq SDK |
| CLS-03 | Groq rate limit (429) | P1 | Retry with backoff (3 attempts) | `time.sleep(2 ** attempt)` |
| CLS-04 | Groq service down / timeout | P1 | Error with retry suggestion | Timeout 30s; catch network errors |
| CLS-05 | LLM returns non-JSON text | P1 | Retry once; fallback to default category | Regex extract JSON block; fallback `Resources` |
| CLS-06 | LLM returns invalid category | P1 | Map to nearest PARA or default `Resources` | Validate against allowed list |
| CLS-07 | LLM returns empty tags/summary | P1 | Use defaults: tags=[], summary=first line of content | Post-process LLM response |
| CLS-08 | Very long content exceeds token limit | P1 | Truncate to first ~4000 chars + note in prompt | Config: `MAX_CLASSIFY_CHARS` |
| CLS-09 | Content in non-English language | P2 | Classify anyway; tags may be English | Prompt: "Preserve language in summary" |
| CLS-10 | Empty/minimal content ("hi", single URL) | P1 | Still classify; likely `Resources` or `Archives` | No crash on short input |

### 2.2 PDF & File Extraction

| ID | Scenario | Priority | Expected Behavior | Mitigation |
|----|----------|----------|-------------------|------------|
| CLS-11 | PDF with no extractable text (scanned image) | P1 | Use filename + "No text extracted" as content | Graceful fallback message in wiki body |
| CLS-12 | Corrupt PDF | P1 | Skip text extraction; classify from filename | Catch `pypdf` errors |
| CLS-13 | Password-protected PDF | P2 | Error message; classify from filename only | Catch encryption error |
| CLS-14 | Empty PDF (0 pages) | P2 | Classify from filename | Handle empty page list |

### 2.3 Idempotency & State

| ID | Scenario | Priority | Expected Behavior | Mitigation |
|----|----------|----------|-------------------|------------|
| CLS-15 | Re-run classify on same raw capture | P0 | Skip already-processed (wiki note exists) | Check `wiki/**/*/{id}.md` before processing |
| CLS-16 | Wiki note exists but raw was deleted | P2 | Leave wiki intact | No action needed |
| CLS-17 | Raw capture with unknown `type` in meta.json | P1 | Attempt text read; default type `note` | Validate type enum |
| CLS-18 | PARA folder missing (e.g. `wiki/Projects/`) | P0 | Auto-create category subdirs | `mkdir(parents=True)` before write |
| CLS-19 | LLM assigns wrong PARA category | P2 | Accept — user can manually move file later | Document as known limitation |
| CLS-20 | Concurrent classify runs | P2 | File lock or warn "already running" | Optional lockfile for v1 |

---

## 3. Auto-Linking (`link.py`)

### 3.1 Embeddings

| ID | Scenario | Priority | Expected Behavior | Mitigation |
|----|----------|----------|-------------------|------------|
| LNK-01 | First note in empty wiki | P0 | No links created; embedding cached | Handle empty comparison set |
| LNK-02 | Single note only | P0 | No self-link | Exclude same note_id from candidates |
| LNK-03 | Note with empty body | P1 | Embed summary + tags only | Concat available fields |
| LNK-04 | Embedding model download fails (offline) | P1 | Clear error with network hint | Catch HF download errors |
| LNK-05 | `embeddings.pkl` corrupt/missing | P1 | Rebuild cache from all wiki notes | Validate pickle load; rebuild if fail |
| LNK-06 | Embedding model version changed | P1 | Recompute all embeddings | Store `embedding_version` in frontmatter |
| LNK-07 | Very short note ("ok") | P2 | Low-quality embedding; may false-link | Consider min char threshold for linking |

### 3.2 Similarity & Linking Logic

| ID | Scenario | Priority | Expected Behavior | Mitigation |
|----|----------|----------|-------------------|------------|
| LNK-08 | Threshold too low (0.50) | P2 | Too many spurious links | Default 0.75; document tuning |
| LNK-09 | Threshold too high (0.95) | P2 | Almost no links | Document tuning range 0.70–0.80 |
| LNK-10 | Duplicate/similar notes | P1 | Should link to each other | Test with near-identical captures |
| LNK-11 | Unrelated notes same topic word | P2 | May false-link on shared keyword | Rely on semantic embedding, not keywords |
| LNK-12 | Re-run link on already-linked notes | P0 | No duplicate `[[links]]` | Dedupe links before write |
| LNK-13 | Bidirectional link (A→B, B→A) | P1 | Both notes updated | `link_note()` updates both files |
| LNK-14 | Link to non-existent note ID | P1 | Skip invalid target; log warning | Verify target exists in wiki |
| LNK-15 | More than 5 similar notes | P1 | Link only top 5 by similarity | `MAX_LINKS_PER_NOTE = 5` |
| LNK-16 | Circular links (A→B→C→A) | P2 | Allowed — valid graph structure | No special handling needed |

### 3.3 Performance

| ID | Scenario | Priority | Expected Behavior | Mitigation |
|----|----------|----------|-------------------|------------|
| LNK-17 | 100+ notes — slow linking | P2 | Acceptable delay (< 2 min) | Batch embedding; cache aggressively |
| LNK-18 | 500+ notes | P2 | May need FAISS/ChromaDB (future) | Document scale limit for v1 |

---

## 4. Graph Builder (`build_graph.py`)

### 4.1 Data Parsing

| ID | Scenario | Priority | Expected Behavior | Mitigation |
|----|----------|----------|-------------------|------------|
| GRPH-01 | Empty `wiki/` folder | P0 | Export `{nodes: [], edges: []}` | No crash; empty graph valid |
| GRPH-02 | Wiki note with invalid YAML frontmatter | P1 | Skip note; log warning | try/except around frontmatter parse |
| GRPH-03 | Wiki note missing `id` in frontmatter | P1 | Use filename as id fallback | Derive id from filename stem |
| GRPH-04 | `[[link]]` to non-existent note | P1 | Edge still created OR skip with warning | Prefer skip + log for clean graph |
| GRPH-05 | Duplicate edges (A→B and B→A) | P2 | Both edges OK or dedupe to one | Document choice; vis-network handles both |
| GRPH-06 | Self-loop edge (A→A) | P1 | Skip self-loops | Filter `from == to` |
| GRPH-07 | Orphan node (no edges) | P1 | Still appear in graph | All notes → nodes regardless of links |
| GRPH-08 | Note with very long content | P1 | Truncate `content_preview` to 200 chars | Slice in builder |
| GRPH-09 | Special chars in label break JSON | P1 | Proper JSON escaping | Use `json.dump()` not manual string |
| GRPH-10 | Markdown link format variants (`[[id]]` vs `[[id|label]]`) | P1 | Parse both formats | Regex: `\[\[([^\]|]+)(?:\|[^\]]+)?\]\]` |

### 4.2 Graph Scale

| ID | Scenario | Priority | Expected Behavior | Mitigation |
|----|----------|----------|-------------------|------------|
| GRPH-11 | Single node graph | P0 | Renders one node centered | vis-network handles n=1 |
| GRPH-12 | 50+ nodes dense graph | P2 | Usable but cluttered | Limit label length; physics tuning |
| GRPH-13 | Disconnected subgraphs | P2 | All components visible | Force-directed shows clusters |
| GRPH-14 | `graph.json` missing when app loads | P0 | Show "Run build_graph.py first" | Check file exists in app.py |

---

## 5. Interactive Graph (vis-network / Streamlit)

### 5.1 Rendering

| ID | Scenario | Priority | Expected Behavior | Mitigation |
|----|----------|----------|-------------------|------------|
| VIS-01 | Graph JSON too large for iframe | P2 | Slow load; still works | Lazy load or limit preview text |
| VIS-02 | Hover on node with empty summary | P1 | Show id + "No summary" | Fallback tooltip text |
| VIS-03 | Node label overlap (many nodes) | P2 | Readable enough at zoom | vis-network physics + font size |
| VIS-04 | Browser without JavaScript | P2 | Graph won't render | Acceptable for v1 |
| VIS-05 | Streamlit component height too small | P1 | Set min height 500px+ | `height=600` in `st.components.v1.html` |
| VIS-06 | JSON injection in note content | P1 | Escape HTML/JS in tooltips | Sanitize content before embedding in HTML |

### 5.2 Interaction

| ID | Scenario | Priority | Expected Behavior | Mitigation |
|----|----------|----------|-------------------|------------|
| VIS-07 | Drag node off screen | P2 | User can zoom/pan back | Reset view button (optional) |
| VIS-08 | Double-click / rapid zoom | P2 | No crash | Default vis-network behavior |
| VIS-09 | Mobile/touch device | P2 | Basic pan/zoom works | vis-network touch support |

---

## 6. RAG Q&A (`ask.py`)

### 6.1 Retrieval

| ID | Scenario | Priority | Expected Behavior | Mitigation |
|----|----------|----------|-------------------|------------|
| ASK-01 | Question with no matching notes | P0 | "I don't have information about that in your notes." | Check max similarity < threshold |
| ASK-02 | Empty question | P0 | Reject: "Please enter a question" | Validate in CLI and Streamlit |
| ASK-03 | Very vague question ("tell me stuff") | P1 | Best-effort from top-K notes | Lower confidence message |
| ASK-04 | Question in different language than notes | P2 | Retrieve by embedding; answer in question language | Multilingual embedding model helps |
| ASK-05 | Question about future/external facts | P0 | Answer only from notes; no hallucination | Strict RAG prompt guardrails |
| ASK-06 | All retrieved notes low similarity (< 0.3) | P1 | Say insufficient context | Set retrieval min threshold |
| ASK-07 | Empty wiki / no embeddings | P0 | "No notes indexed yet" | Check wiki count before ask |
| ASK-08 | Question matches many notes (20+) | P1 | Return top-K=5 only | Config `RAG_TOP_K = 5` |
| ASK-09 | Duplicate info across retrieved notes | P2 | LLM synthesizes without repetition | Prompt: "Consolidate duplicate info" |

### 6.2 LLM Synthesis

| ID | Scenario | Priority | Expected Behavior | Mitigation |
|----|----------|----------|-------------------|------------|
| ASK-10 | LLM hallucinates facts not in notes | P0 | Prompt forbids; cite sources | "Answer ONLY from context" + show sources |
| ASK-11 | LLM API failure during ask | P1 | Show error; don't crash app | try/except in ask(); Streamlit error banner |
| ASK-12 | Context window exceeded (many long notes) | P1 | Truncate each note to ~500 chars in prompt | Trim retrieved content |
| ASK-13 | Question asks to compare two topics | P1 | Synthesize across multiple sources | top_k >= 5 for comparison queries |
| ASK-14 | Question about specific note ID | P2 | Direct lookup if ID mentioned | Optional ID regex bypass retrieval |

### 6.3 Citations

| ID | Scenario | Priority | Expected Behavior | Mitigation |
|----|----------|----------|-------------------|------------|
| ASK-15 | Sources list empty but answer given | P0 | Never — always show sources used | Attach sources to AskResponse |
| ASK-16 | Source note deleted after indexing | P2 | Skip missing; warn in sources | Verify path exists when displaying |

---

## 7. Streamlit App (`app.py`)

### 7.1 Startup & State

| ID | Scenario | Priority | Expected Behavior | Mitigation |
|----|----------|----------|-------------------|------------|
| APP-01 | Fresh clone — no data files | P0 | Empty state UI with setup instructions | Check paths; show onboarding message |
| APP-02 | `graph.json` out of sync with wiki | P1 | Stale graph shown | Sidebar "Rebuild Graph" button |
| APP-03 | User clicks Ask repeatedly / double submit | P1 | Disable button during processing | `st.session_state` loading flag |
| APP-04 | Streamlit session reload | P2 | State resets; graph reloads | Expected Streamlit behavior |
| APP-05 | Missing `.env` on Streamlit Cloud | P0 | Use Streamlit secrets; clear error if missing | `st.secrets["GROQ_API_KEY"]` with fallback |

### 7.2 UI Edge Cases

| ID | Scenario | Priority | Expected Behavior | Mitigation |
|----|----------|----------|-------------------|------------|
| APP-06 | Very long answer text | P2 | Scrollable answer panel | `st.container()` with expander |
| APP-07 | Answer contains markdown/code | P1 | Render safely | `st.markdown()` with escaped user input where needed |
| APP-08 | Sidebar stats with 0 notes | P0 | Show zeros, not crash | Default counts to 0 |
| APP-09 | Concurrent users on public deploy | P2 | Read-only demo OK; no shared write | Document: v1 is single-user read-only on cloud |

---

## 8. Deployment & Environment

### 8.1 Streamlit Cloud / HF Spaces

| ID | Scenario | Priority | Expected Behavior | Mitigation |
|----|----------|----------|-------------------|------------|
| DEP-01 | `sentence-transformers` slow cold start | P1 | First ask delayed 30–60s | Pre-bundle `embeddings.pkl`; skip model load if cache exists |
| DEP-02 | Model download blocked on cloud | P1 | Ship precomputed embeddings in repo | Commit `data/embeddings.pkl` |
| DEP-03 | Repo too large (model + data) | P2 | Use Git LFS or precompute only | Keep raw/ out of deploy repo |
| DEP-04 | API key in committed `.env` | P0 | Never commit; use secrets | `.gitignore` + pre-push check |
| DEP-05 | Build fails — missing dependency | P0 | Pin requirements.txt | Test `pip install -r requirements.txt` clean |
| DEP-06 | Python version mismatch | P1 | Specify 3.10+ in README | Add `.python-version` or `runtime.txt` |
| DEP-07 | App sleeps on free tier | P2 | Cold start on first visit | Document for demo viewers |
| DEP-08 | Personal notes exposed publicly | P0 | User choice: sanitize demo data | README warning; optional demo subset |

### 8.2 Local vs Cloud Divergence

| ID | Scenario | Priority | Expected Behavior | Mitigation |
|----|----------|----------|-------------------|------------|
| DEP-09 | New capture locally not on cloud | P1 | Expected — cloud is snapshot | Document: push wiki + rebuild after local capture |
| DEP-10 | Windows paths vs Linux deploy | P1 | Use `pathlib.Path` everywhere | Never hardcode `\` or `/` |
| DEP-11 | Line ending differences (CRLF/LF) | P2 | No functional impact | `.gitattributes` optional |

---

## 9. Security & Privacy

| ID | Scenario | Priority | Expected Behavior | Mitigation |
|----|----------|----------|-------------------|------------|
| SEC-01 | API key logged to console | P0 | Never log secrets | Redact in logging |
| SEC-02 | Note content sent to Groq | P1 | User aware — documented | README privacy section |
| SEC-03 | XSS via note content in graph HTML | P1 | Escape HTML in tooltips | `html.escape()` before inject |
| SEC-04 | Path traversal in file capture | P0 | Reject paths outside cwd | Resolve + validate |
| SEC-05 | Sensitive data in public repo | P0 | `.gitignore` raw/ or sanitize | Don't commit personal raw/ to public repo |

---

## 10. Data Integrity & Recovery

| ID | Scenario | Priority | Expected Behavior | Mitigation |
|----|----------|----------|-------------------|------------|
| DAT-01 | Manual edit breaks wiki frontmatter | P1 | classify/link skip with error | Validate on read |
| DAT-02 | Delete wiki note but links remain | P2 | Orphan edges in graph | build_graph skips missing targets |
| DAT-03 | Delete raw/ but keep wiki/ | P2 | Wiki remains valid | raw/ is archive; wiki is source of truth post-classify |
| DAT-04 | Full pipeline re-run from scratch | P2 | Idempotent except new captures | Document reset procedure |
| DAT-05 | Corrupt `graph.json` | P1 | App shows error; rebuild fixes | Validate JSON on load |
| DAT-06 | Backup / restore | P2 | Copy `raw/`, `wiki/`, `data/` | Document manual backup |

---

## 11. Cross-Pipeline Edge Cases

| ID | Scenario | Priority | Expected Behavior | Mitigation |
|----|----------|----------|-------------------|------------|
| XPL-01 | Capture → classify without link → ask | P1 | Ask works; graph has no similarity edges | link optional for ask |
| XPL-02 | Capture → classify → link → ask (skip graph) | P1 | Ask works independently | Modular pipeline |
| XPL-03 | New note added; graph not rebuilt | P1 | Stale graph until rebuild | Sidebar refresh button |
| XPL-04 | classify run mid-link run | P2 | Partial state OK | Run sequentially: classify then link |
| XPL-05 | End-to-end with 1 item only | P0 | All stages complete | Minimum viable brain |
| XPL-06 | End-to-end with 50+ items | P2 | Performance acceptable | Phase 7 load test |

---

## 12. Phase 7 Test Matrix

Use this checklist when running Phase 7 QA. Mark pass/fail for each.

### Capture (Phase 1)

- [ ] CAP-01 Empty note rejected
- [ ] CAP-06 Missing file rejected
- [ ] CAP-10 Unicode/emoji saved correctly
- [ ] CAP-16 PDF captured successfully

### Classification (Phase 2)

- [ ] CLS-01 Missing API key handled
- [ ] CLS-05 Malformed LLM JSON handled
- [ ] CLS-15 Re-run is idempotent
- [ ] CLS-11 Scanned PDF fallback works

### Linking (Phase 3)

- [ ] LNK-01 First note — no crash
- [ ] LNK-10 Similar notes link
- [ ] LNK-12 No duplicate links on re-run
- [ ] LNK-15 Max 5 links enforced

### Graph (Phase 4)

- [ ] GRPH-01 Empty wiki → empty graph
- [ ] GRPH-07 Orphan nodes visible
- [ ] GRPH-11 Single node renders
- [ ] GRPH-14 Missing graph.json handled in app

### Ask (Phase 5)

- [ ] ASK-01 No-match question handled
- [ ] ASK-02 Empty question rejected
- [ ] ASK-05 No hallucination on external facts
- [ ] ASK-10 Sources always shown

### App & Deploy (Phases 5–8)

- [ ] APP-01 Empty state UI
- [ ] APP-03 Double-submit prevented
- [ ] DEP-04 No secrets in repo
- [ ] DEP-08 Privacy warning in README

---

## 13. Known Limitations (v1)

Document these as accepted trade-offs for the 4-week build:

1. **No OCR** — image captures store file only; no text extraction
2. **No URL fetching** — links store URL string only (no page content scrape)
3. **No real-time sync** — cloud deploy is a snapshot; local captures require manual push/rebuild
4. **Single-user** — no auth or multi-tenant support
5. **English-biased** — PARA/tags may be English even for non-English notes
6. **Scale limit** — optimized for ~15–100 notes, not thousands
7. **No edit UI** — notes edited by hand in filesystem only
8. **No deduplication** — identical captures create separate notes

---

## 14. Priority Fix Order (Before Deploy)

Fix in this order if time is limited:

1. **P0 security:** SEC-01, SEC-04, SEC-05, DEP-04, DEP-08
2. **P0 crashes:** CAP-01, CAP-06, CLS-01, GRPH-01, GRPH-14, ASK-01, ASK-07, APP-01, APP-05
3. **P0 data integrity:** CLS-15, LNK-12, ASK-10, ASK-15
4. **P1 UX:** Remaining P1 items in sections 1–8
5. **P2 polish:** As time permits

---

## Related Documents

- [architecture.md](./architecture.md) — system design and data models
- [Implementation-plan.md](./Implementation-plan.md) — Phase 7 references this file for QA
- [problemstatement.md](./problemstatement.md) — weekly acceptance criteria
