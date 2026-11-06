# D 影像刊 · latest refinement handoff

## Accepted release gate (2026-11-06, 中国标准时间)

- Actual site, same port as previous QA: **http://127.0.0.1:33205/**
- **Local-only mobile fixture: http://127.0.0.1:33205/__qa/mobile**
- Fixture file: `qa/mobile.html`, outside deployed `public/`. It uses six genuine iframes: homepage + article at 320, 390, 768px. Article selector switches between Amjad long article, DeepSeek original, Cursor rewrite video, Karpathy rewrite image and Levelsio portrait video. Each frame is unscaled, loads the actual same-origin route and site CSS/JS, and scrolls independently. Optional overflow readout measures its real DOM; it is not an automated screenshot or a mobile device test. Test browser history on the normal top-level page, not joint iframe history.
- Server restarted on the **same 33205 port** for the local fixture route; refresh old pages. New live route returned HTTP 200. The fixture route exists only in `scripts/preview.py`; Cloudflare assets remain `directory = "public"`.
- **Parent final browser QA accepted release at 08:49 中国标准时间.** Desktop 1920×1113 and actual homepage + Cursor article iframes at 320/390/768px passed: no overflow, true local source images loaded, tabs/source/return accessible. The executor also read the supplied desktop screenshot; it did not perform an independent browser run.
- **Explicit playback limitation:** manual browser playback was attempted, but `video.twimg.com` returned HTTP 403. The unavailable message and original-source fallback worked. This is NOT playback success. The 403 will not be bypassed; videos stay external and all Chinese/original media retain source fallback.
- Accepted desktop screenshot (local evidence, not uploaded to the repository): `/cursor/stores/user/grok-bot/agents/788adcbb-338e-4d41-a21e-0b95169edd01/assets/5e991953af660a352c6f1a633b2b0401f64333344942b4e0ac897e828076edc9.png`.
- Source publication and Worker `xnews` deployment are explicitly authorized. This document records the accepted pre-publication checks; actual commit/version/live verification is reported after release.

## Public media investigation

Normal unauthenticated curl only: no browser automation, cookies, tokens, alternate blocked endpoint or access-control circumvention. All seven stored image/poster URLs returned HTTP 200 `image/jpeg`, then passed image decoding/format verification. Original bytes were copied unchanged; no generated replacement news imagery or screenshot substitute. Total **339920 bytes (~332 KiB)**, largest 107280 bytes. Provenance, original HTTPS URLs, dimensions and SHA-256 live in `src/media-manifest.json`; raw read-only investigation scratch is ignored at `.media-qa/`.

| Local rendering asset | Dimensions | Bytes | Upstream result |
|---|---:|---:|---|
| `/media/karpathy-hackertube-image-cca841bfb0.jpg` | 1200 × 697 | 107280 | 200 image/jpeg |
| `/media/levelsio-300-month-expenses-image-6e1d7a11c2.jpg` | 1199 × 592 | 43818 | 200 image/jpeg |
| `/media/levelsio-bf1942-web-poster-fdbc2233d7.jpg` | 675 × 1200 | 64351 | 200 image/jpeg |
| `/media/deepseek-super-agent-harness-poster-32294b3993.jpg` | 640 × 480 | 43712 | 200 image/jpeg |
| `/media/cursor-live-apps-poster-d4045da567.jpg` | 1200 × 675 | 21347 | 200 image/jpeg |
| `/media/openai-gpt6-cyber-poster-d795be1590.jpg` | 1200 × 675 | 47191 | 200 image/jpeg |
| `/media/tibo-dropbox-launch-video-poster-839d50e043.jpg` | 480 × 360 | 12221 | 200 image/jpeg |

- All four native video source URLs (Cursor, OpenAI, Levelsio BF1942, Tibo) accepted a bounded normal `Range: bytes=0-0` GET: HTTP 206 `video/mp4`, one byte each. Cursor advertised 1513678 total bytes. No full video was downloaded or bundled.
- The public `youtube-nocookie.com/embed/OrcsMi2-IcM` HEAD returned HTTP 200 `text/html`. **This only checks an HTTP response, not playback, embedding success or browser reachability.**
- Earlier curl availability does not establish browser playback: final manual browser video requests returned HTTP 403. No access-control bypass or retry through another endpoint was attempted. Local images remove that external image hop. Videos remain external with visible original-open fallback, no autoplay, `preload=none` for native media, and honest error/buffering recovery. Cross-origin iframe loading cannot reliably establish player state; no false claim that a loaded iframe equals playable video.

## Layout, metadata and media behavior

- Text-card type-cover minimum 125→90px, compact card gaps/padding, regular title cap 27→23px / featured 38→34px. Text cards size to content instead of stretching; card footer no longer pushes to the bottom of a blank flexible body. Featured cover can absorb residual height while its text stays naturally sized; mobile restores fixed aspect-ratio sizing.
- Primary nav 14→15px desktop / 14px mobile; card dates/authors and article metadata 12→14px. Source actions, source footer, recovery labels and captions enlarged; narrow low-priority actions stay at 13px. Full titles/content are retained.
- Real images and native posters use durable `/media/...` URLs **only in HTML rendering**. Original media objects remain exact, including URL/poster/alt, and RSS uses upstream URLs, never relative `/media/` paths.
- On native media error the player is hidden, its true cached poster is available, the accurate cannot-play message and source link remain. After a user play request stalls for ten seconds, a conditional recovery message appears without claiming permanent failure; playing/pause clears it. No timer is armed by an idle unopened player.

## User-added multimodal and editorial requirements

- Reusable project prompt: **`content/EDITORIAL_PROMPT.md`**; stable byte-for-byte reviewed addon: **`content/EDITORIAL_ADDON.md`**. Schema: `content/SCHEMA.md`. Both instruct full-text/media coverage, stable source media IDs, ordered references, precise placement only when supported, a labeled source-media block otherwise, explicit omissions, no fabricated transcript/caption, no autoplay, full RSS and acceptance tests.
- Backfilled all 13 articles with `rewrite_media`: **7 source attachments included, 0 omitted; 6 media-free stories remain empty.** Existing original/source objects were not changed. Unknown placement remains `after_body` + `source_metadata_only`, not invented semantic precision. UI rewrite and RSS Chinese sections share one renderer/plan; source media is deduplicated within each section. Both tabs now pause/unload on hide/close.
- Integrated the provided anti-AI editorial addon into the prompt, above generic style templates. **Audited all 13 against stored originals and changed only the authorized Chinese `title/dek/body_md`.** Restored full Amjad/Victor long-form evidence and limits rather than turning them into summaries. Complete per-article coverage/corrections and the checked Sarah sample are in **`content/EDITORIAL_QA.md`**. Research files remain unmodified.
- DeepSeek: removed invented 30-task count, fixed podcast/interview attribution, fixed “enabled = 30% fewer” comparison base, restored prototype/non-official status, 17.5× range, 6.4→1.6s, worker/mode/benchmark/security limits. Levelsio: fixed annual service denominators vs monthly costs, Photo AI exclusion, all six savings entries and missing Sume/.io values. Sarah uses only the checked proposed title/dek/body. Removed editor-added fake contrasts, questions and grand endings throughout.
- **Evidence gap, not external disproof:** Anthropic/OpenAI/Cursor/Vercel/Schedules contained detailed additions not supported by the stored short source text. Those were removed rather than assumed true from a `related_url`; we did not reopen/retain the full linked articles in this round. Current Chinese fully covers the saved announcement, not an unseen article/transcript.
- Unchanged protected fields: `id/date/published_at/tags/source/original`, deep-compared to the pre-round snapshots and locked by SHA-256 in `qa/editorial-source-lock.json`. All seven media IDs/reference order/evidence levels stay intact through the subsequent copy edit. Generated index titles/deks and RSS Chinese text intentionally update to the corrected fields.
- Remaining metadata flag: Victor's existing `source.title_en` says ARR while stored original says annualized gross revenue. Chinese is corrected to 年化总收入; source metadata was not silently changed. Parent can decide a separate metadata correction.

## Passed checks (non-visual)

- `npm test`: current build of 13 articles, **25 Python source/static/RSS/editorial/HTTP tests + 17 reader DOM/state/parser tests = 42 passed**.
- JS syntax for source/generated assets; Python compilation; `git diff --check` pass.
- Real HTTP fixture and all thirteen clean article routes return 200; seven JPEGs return 200 with matching bytes / correct content type. Unknown local route remains 404. Fixture exclusion from public assets checked.
- Full Chinese and stored original texts, stable links/GUIDs, media URLs and fallbacks verified in RSS; native audio and semantic paragraph placement covered by explicitly synthetic unit fixtures (there is no invented audio article in the deployed content).
- Coverage, duplicate/unknown/missing references, explicit omission, unique paragraph anchors and ordered same-anchor media tests pass. Hash tests preserve original/source/media/IDs/dates. Reader history, independent scroll, focus, hidden iframe unloading and rewrite/original native pause pass with new media in both tabs. Native stalled/error recovery is tested as DOM state, not real playback.

## Accepted scope and publication checks

1. Parent completed the requested final desktop and actual narrow-iframe checks above; no further browser QA is requested as a release prerequisite.
2. Keep the explicit video HTTP 403 / no-success limitation, no autoplay, source fallback and no-bypass policy.
3. Run the full tests/build and original/source/ID/tag/date preservation checks, then one cohesive normal commit/push to `joeseesun/xnews` main and deploy the existing Worker `xnews`.
4. Verify the live homepage, stable article routes, actual local JPEG asset, corrected Sarah sample and valid full Chinese/original/media RSS. Verify `/__qa/mobile` is not publicly deployed. Do not make unrelated editorial, DNS or routing changes.
5. Original curl response checks and the 08:44 pre-release verification snapshot remain historical network/static evidence, not claims of browser playback.

## This round's files

Exact source/support/media paths (including all 13 content JSONs and seven local JPEGs) are listed in `qa/refinement-manifest.txt`. New support files: prompt, editorial ledger, media manifest, local fixture, source lock, HTTP/editorial tests. Changed sources: build/preview, CSS/JS, build/reader tests, schema, README, DESIGN, QA, ignore rules. Generated current output: homepage/archive/articles, app CSS/JS, full RSS and article index; other existing static output regenerated normally. Pre-existing dirty Phase-3 implementation and `design-previews/` were retained; no reset/stash/rebase/remote writes.

---

# Historical initial implementation handoff (superseded where the latest round differs)


## Preview / release gate

- Local implementation: http://127.0.0.1:33205/
- Long article: http://127.0.0.1:33205/a/amasad-managed-cloud-agents
- Original deep link: http://127.0.0.1:33205/a/deepseek-super-agent-harness#original
- Restart: `npm run preview -- --port 0` prints a new local URL. Current preview is a read-only Python static server with clean-route support; production still uses existing Cloudflare assets configuration.
- **Pending parent visual pass. No browser automation, screenshots, visual verification, production deploy, git commit or push was performed by this executor.**

## Implemented

Selected D anchor is `.dir-d` in the existing four-direction preview; design decisions are in `DESIGN.md`. Bright paper, high-contrast media/type composition, asymmetric responsive grid, no sidebar, quiet RSS/Archive/About chrome, persisted optional dark mode. Covers use stored source media/posters, never generated news imagery or mock headlines. The actual stored titles are used, including the correct Levelsio website-cost title (not the old preview's “生活成本”).

Cards remain real `/a/<id>` anchors. JS progressively opens full HTML in a full-viewport dialog; modified clicks and standalone routes remain native. Browser Back/Forward and Close/Escape return to the list's recorded scroll/focus. Request cancellation, stale-response guards, loading/error/retry, standalone fallback and original link are present. Tabs are accessible manual-activation controls with deep-link fragments and separate saved positions. Without JS both complete bodies and semantic section links remain in the document. Hidden/closing media is paused; iframe sources are unloaded and restored without autoplay. Lazy media has original-link recovery. DeepSeek's saved video text is explicitly an excerpt, not a complete transcript, in the reader and RSS.

## Concurrent routine / preservation

At task start only `design-previews/` was untracked. During implementation the daily routine landed commit `3008be3` and added five stories (Cursor Apps, GPT-6 Cyber, Anthropic vault, Tibo video, Rauch Schedules), bringing the current total to **13**. No reset, checkout, stash, rebase or content rewrite was used. Builds always loaded current filesystem content. All eight pre-existing content JSON SHA-256 values stayed identical; `git diff --exit-code -- content/articles public/articles.json` passed against the fresh daily HEAD.

Important integration detail: the daily routine ran while the presentation generator was being changed. Current HEAD already contains regenerated home/archive and five new article pages using the D templates; these therefore do not all appear as dirty files now. Do not interpret their absence from `git diff` as missing D work, and do not roll back the routine's fresh content. Review the whole current generated site before the later cohesive commit/deploy. This executor made no remote changes.

Every old RSS item's title, link, GUID, publication date, author, rewrite, stored original and media is preserved exactly; the only per-item addition is the explicit DeepSeek availability note. Full RSS tests cover all 13 current stories. Feed build time is regenerated normally. No content JSON, article IDs, URLs or source/related links were deliberately altered.

## Passed checks (non-visual)

- `npm test`: build of 13 stories; **11 Python build/content/RSS/static tests + 14 DOM/state/parser tests** passed.
- `node --check src/site.js` / generated JS; Python compilation passed.
- Actual local HTTP smoke: `/`, `/archive`, `/about`, CSS, JS, RSS, articles JSON and all 13 clean `/a/id` routes returned 200. Unknown article returned custom 404.
- HTML5 parse of all generated HTML: no parse errors. CSS syntax parsed without runtime stylesheet errors.
- State tests cover real-link interception, original/rewrite independent offsets, tab/permalink hash, Back/Forward, close/focus restoration, cache, Escape/focus loop, modified clicks, error/retry, aborted late responses, media errors/pause/unload, direct hash routes, blocked storage, wrong-article rejection and missing native-dialog fallback.
- Source CSS/JS equal their generated assets, so subsequent routine builds retain D instead of reverting it. RSS handles CDATA/ampersands and image/video/audio paths. Responsive/reduced-motion CSS checks passed. None of this is claimed as visual/layout geometry verification.

## Parent visual checklist / blocking release gate

1. Desktop 1440 and 1920: lead title visible early, intentional media emphasis, no awkward grid holes/huge stretches, full stored titles, correct chronological keyboard order.
2. Mobile 320/390 and tablet 768: masthead/nav wrapping, single-column cards, no horizontal page overflow, touch targets, reader bars/tabs and source actions fit.
3. Open Amjad's long article from mid-list; read/scroll both panels, switch repeatedly, close/Escape/Back; confirm list scroll/focus. Forward should restore the reader. Test browser refresh/direct URL and independent page link with `#original`.
4. Light and dark: contrast, selected tabs, text-cover colors, image captions. Disable JS and open direct article URLs; both complete sections and source links must remain usable.
5. Actual media: manual-only video/audio, portrait media proportions, Youtube load, failed network/image fallback, no playback continuing behind a hidden panel/closed reader. Check Safari/mobile scroll lock and native dialog focus with real browser behavior.
6. If needed refine only a few high-impact visual issues, then rerun `npm test`. Deploy/push only after this parent visual pass. No claim is made that production currently reflects these local changes.

## Exact worktree file manifest

Tracked files currently changed relative to the concurrent daily HEAD:
- `.gitignore`
- `package.json`
- `public/404.html`
- `public/a/amasad-managed-cloud-agents.html`
- `public/a/deepseek-super-agent-harness.html`
- `public/a/karpathy-hackertube.html`
- `public/a/levelsio-300-month-expenses.html`
- `public/a/levelsio-bf1942-web.html`
- `public/a/rauchg-vercel-security-review.html`
- `public/a/sarah-guo-personal-software.html`
- `public/a/victor-slash-supersmb.html`
- `public/about.html`
- `public/app.css`
- `public/app.js`
- `public/feed.xml`
- `scripts/build.py`

New implementation/support files:
- `DESIGN.md`
- `QA.md`
- `package-lock.json`
- `scripts/preview.py`
- `src/site.css`
- `src/site.js`
- `tests/test_build.py`
- `tests/reader-state.test.cjs`

Generated/verified current output files (some already part of concurrent daily HEAD):
- `public/index.html`
- `public/archive.html`
- `public/about.html`
- `public/404.html`
- `public/app.css`
- `public/app.js`
- `public/feed.xml`
- `public/articles.json`
- `public/a/amasad-managed-cloud-agents.html`
- `public/a/anthropic-vault-claude.html`
- `public/a/cursor-live-apps.html`
- `public/a/deepseek-super-agent-harness.html`
- `public/a/karpathy-hackertube.html`
- `public/a/levelsio-300-month-expenses.html`
- `public/a/levelsio-bf1942-web.html`
- `public/a/openai-gpt6-cyber.html`
- `public/a/rauchg-agent-schedules.html`
- `public/a/rauchg-vercel-security-review.html`
- `public/a/sarah-guo-personal-software.html`
- `public/a/tibo-dropbox-launch-video.html`
- `public/a/victor-slash-supersmb.html`

The pre-existing `design-previews/` directory is retained, not rewritten in Phase 3. `src/worker.js`, `wrangler.toml`, the content schema and all content JSON remain untouched by this executor.
