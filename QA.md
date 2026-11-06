# Performance and search release · 2026-11-06 (Asia/Shanghai)

Scope explicitly requested: optimize and publish **xnews.qiaomu.ai** loading speed, SEO and GEO; separately register its RSS in 乔木精选. Coordinated with the UI release chat and started editing only after it became idle and the checkout was clean at `4ed2ec3` (UI/content base `ddff8be`, 15 articles).

## Changes and evidence

- Fingerprinted CSS/JS under `/static/` and content-addressed media use one-year immutable browser caching. HTML uses short freshness windows (home/archive 60 seconds, articles 300 seconds); RSS 300 seconds. Old `/app.css` and `/app.js` remain for compatibility. Keep older fingerprinted assets while old HTML may still reference them.
- Hover/keyboard intent prefetches at most two same-origin article requests concurrently and shares the response with the reader. No bulk article or media preloading; save-data/2G skip speculative requests. Failed/mismatched responses never enter the cache; explicit reading still works.
- Build generates `robots.txt`, an 18-URL canonical sitemap (15 articles + home/archive/about), Article/WebPage/WebSite/publisher JSON-LD, article source references and sharing images. 404 is noindex with no misleading canonical. No invented `lastmod` or modification timestamps. Publisher/original-author roles and date meaning are visible in the article/about page; original content and media are unchanged.
- Before: public robots/sitemap returned 404; CSS/JS used `max-age=0, must-revalidate`. Terminal sample TTFB: home 0.517s, article 0.760s; browser observed ~1.54s CSS/JS fetches and a reader still loading after 5 seconds. Browser before runs did not yield a stable aggregate; they must not be presented as field Core Web Vitals.
- Controlled Chrome comparison (600ms added article latency, 850ms hover lead, 3 runs each): baseline click-to-article 824/817/826ms; intent prefetch 34/35/41ms. This isolates the prefetch benefit, not a population-wide speed claim. `.qa-ui/speed-seo/performance-lab.json` contains raw results.
- Verification: 29 Python + 24 reader state tests passed; 39 real Chrome checks passed on identical candidate sources, including desktop/mobile layout and accessibility. Desktop reader screenshot inspected. Original `content/` and `articles.json` unchanged. Wrangler dry run passed.

## Search documentation checked

Reviewed 2026-11-06: [Cloudflare asset headers](https://developers.cloudflare.com/workers/static-assets/headers/), [Google Article markup](https://developers.google.com/search/docs/appearance/structured-data/article), [Google AI search foundations](https://developers.google.com/search/docs/appearance/ai-features), [OpenAI crawler distinctions](https://developers.openai.com/api/docs/bots). Scope is live/code/rendered inventory of this small site; no Search Console property, indexing, rankings, real-user performance distributions or AI citations were available. Sitemap publication and valid markup are not evidence of search-engine processing. Search/AI citation outcomes require later platform data; do not fabricate a universal GEO score.

Published code `c4b889730693e6d6ae35f1f3bd7487f8e67526d4` as Cloudflare Worker version **`3a041cd7-1201-4179-ba5c-806019d0b056`**, 2026-11-06 around 16:49 Asia/Shanghai. Source review: [PR #1](https://github.com/joeseesun/xnews/pull/1). Used the documented OAuth deployment command `env -u CLOUDFLARE_API_TOKEN wrangler deploy`.

Final live HTTP verification: across the bounded runs, **23 unique routes matched local bytes exactly** (all 18 indexable HTML pages, RSS, robots, sitemap, CSS and JS). `public/_headers` is deployment configuration, not a public route. Fingerprinted assets returned one-year immutable caching; home/article returned their configured short TTLs; an unknown path returned genuine HTTP 404 with noindex. Raw evidence: `.qa-ui/production-speed-seo.json`, `.qa-ui/live-inventory.json`, and saved responses. The sitemap timed out in the later batch but had already matched in the earlier batch; never treat a timeout as a passing request. LA server normal curl independently returned the expected homepage and cache headers. Python urllib from that server returned 403; this alone does not establish that named verified search crawlers are blocked.

**Verification limits:** production browser navigation remained intermittently stuck before HTML arrived (empty title, zero cards/scripts, only the document request pending), and local curl also intermittently timed out. No stable post-release cold-load aggregate or successful post-release live browser walkthrough was obtained. Local Chrome checks on the identical deployed sources passed (39); screenshots of desktop and 320px reader were inspected. Cache/prefetch gains are implemented and headers are live, but this release does not claim to fix every geographic network path or prove field Core Web Vitals. Recheck cold navigation and repeat-view resource transfer sizes on a stable connection; then observe actual traffic/search data over 7–14 days before attributing any outcome to this change.

Umami retains exactly one unchanged script/property on every page; preceding UI release ingestion was independently verified earlier the same day (record below). This follow-up did not obtain a new ingestion event because browser navigation failed, so ingestion is not newly re-certified. No network/privacy settings or access controls were changed.

RSS integration in the separate reader is verified live: `xnews` enabled, optIn false, autoRewrite false, status ok, **15 entries**. Rollback baseline: Cloudflare Worker version `2d8c75ee-d16b-46cd-bbfe-d39da9236a2b`. No temporary worktree created.

---

# Production release · 2026-11-06

User authorized publication with “上线啊”. Release baseline: `801d1918e00d3ddba9865793e0b144d4daa524a6`; remote main matched before staging. This release includes the completed brand/interaction refinement below, the explicit Cloudflare account ID verified against the qiaomu.ai zone, and restoration of the domain’s existing Umami property `31e0098c-6852-46b6-899c-11eed5ed16e1`.

Umami is restricted to `xnews.qiaomu.ai`; search/query strings and fragments are excluded, so typing filters and switching versions do not generate duplicate pageviews or transmit search terms. Local preview traffic is excluded. All generated HTML pages have exactly one validated tracking script. The existing dashboard label still reads “AI 大V电台”; its configured domain is xnews.qiaomu.ai and no property, ownership or stored data was changed.

Release regression: **26 Python + 21 DOM/state tests passed**. The 39 Chrome checks and visual QA from the preceding implementation remain recorded below. Publishing uses the existing Wrangler OAuth identity: the shell API token is valid for the domain but lacks Worker access and must not shadow OAuth (`env -u CLOUDFLARE_API_TOKEN wrangler deploy`). No credentials are committed.

During publication, remote main advanced to `71944ac` with CaptureFlow and checkwash articles, source licences and a media asset. That commit was merged intact; only conflicting generated home/archive/RSS files were regenerated from the combined sources. The final corpus is **15 articles**, and all 47 regression tests passed again. Discovery tests now derive the article count from the content index rather than assuming 13. The initial 13-article upload (`46b917e0-768b-4583-8acb-ba3a11323d6c`) is superseded by the integrated release recorded below. Final deployment: **`2d8c75ee-d16b-46cd-bbfe-d39da9236a2b`**, source **`ddff8be`**, published to **https://xnews.qiaomu.ai/**. Main was pushed successfully after integrating `71944ac`. Production Chrome verification passed: 15-article homepage, search, CaptureFlow reader, original-version switch, return preserving query/focus, and reset.

**Umami ingestion verified:** the real-browser QA visit to the intentional 404 path `/__qa-release-20261106-ddff8be` appeared in this exact property at **2026-11-06 16:43:53 Asia/Shanghai**, alongside homepage and article visits. Search terms/fragments were absent as configured. Local screenshots: `.qa-ui/production-live-ddff8be.png`, `.qa-ui/umami-release-ddff8be.png`. Structured evidence: `qa/production-release.json`.

**Verification limit:** bulk terminal HTTP comparison could not finish: urllib returned 403/connection closures and curl timed out. Do not interpret this as a successful byte-for-byte public-asset comparison, or conflate it with the successful real Chrome site/interaction checks. No production routing or security policy was weakened. Safari/iOS, screen-reader and actual media playback remain unverified.

**Next-chat handoff:** this checkout is ready for the separately authorized speed/SEO/GEO work after the documentation commit. Use the final remote main as the base, preserve both newly merged stories, and use `env -u CLOUDFLARE_API_TOKEN wrangler deploy` with the existing OAuth at `/Users/joe/Library/Preferences/.wrangler/config/default.toml`. The inherited shell token is DNS-scoped and shadows the working OAuth; do not copy tokens into files. No temporary worktree was created. Temporary speed candidates from another chat were not included. All earlier “local only” statements below describe the pre-release stage.

---

# Local brand and interaction refinement · 2026-11-06 (Asia/Shanghai)

Current scope: the homepage → search/filter → full article → original/rewrite → return flow, archive scan mode, and shared header/theme. Stack remains Python-generated static HTML, plain CSS and vanilla JS. Conventions inspected: `DESIGN.md`, `README.md`, `QA.md`, source schema and existing tests; no repository AGENTS.md or CLAUDE.md was present. Earlier handoffs below are historical and do not authorize a release in this chat.

## Completed outcome

- Original geometric X mark + serif News wordmark + matching favicon; consistent masthead spacing and quieter metadata. Reused the existing paper/olive palette and system fonts.
- Lead headline precedes its cover; desktop opening spread stays asymmetric, later rows have three equal columns. Visible 1440px lead title moved from roughly 940px down the old page to 484px in the new page. All real titles, source images and chronological ordering remain intact.
- Search, text/video filters, URL-backed state, recoverable empty state and a text-only scan mode. Archive defaults to scan mode. Mobile keeps the archive navigation entry visible.
- Approximate Chinese reading time (excludes video duration); per-version reading progress; keyboard Space activation; arrow focus preserves scroll. Close/Back/Forward preserve query, layout, focus and reading positions.
- Rem typography, wrapping controls, image outlines, deliberate light/dark contrast surfaces, reduced-motion handling and instantaneous theme swaps.

## Interface coverage

| Domain | Evidence inspected | Result |
| --- | --- | --- |
| Accessibility | `src/site.js`, native buttons/links/progress, keyboard article flow, axe audits on desktop light/dark, article, 320px home/reader | No automated WCAG violations in five inspected states; VoiceOver not verified |
| Layout | `src/site.css`, actual Chrome screenshots and geometry at 320/390/768/1440/1920px, equivalent 200% zoom viewport, 200% root font size | No tested page/reader horizontal overflow; native browser zoom and RTL mirror not verified |
| Writing | `scripts/build.py` discovery/reader copy, empty/loading/error/retry states, source/kind labels | Actions and recovery paths explicit; duplicate X Article label removed; editorial JSON unchanged |
| Typography | Wordmark, cover author names, headlines, prose and metadata in `src/site.css` | Chinese tracking preserved; Latin optical tracking scoped; rem text sizes and numeric alignment |
| Colors | Source tokens, actual rendered light/dark screenshots and axe contrast checks | Primary text 16.84:1 light / 13.70:1 dark; secondary 5.71:1 / 8.45:1; input boundaries 3.73:1 / 5.00:1 |
| UI polish | SVG mark/icons, image outlines, selected controls, hover/focus styles, reduced motion and theme switch | Consistent states in inspected views; no native Safari/real touch-device verification |

## Resolved findings and design changes

| Severity | Domain | Location | Before | After | Why |
| --- | --- | --- | --- | --- | --- |
| HIGH | Accessibility | `src/site.js:237` | Tab anchors had manual ARIA roles but Space did not activate them | Space activates the focused version; arrow keys use preventScroll focus | Complete the expected keyboard tab interaction and preserve reading context |
| MEDIUM | Layout | `scripts/build.py:433`; `src/site.css:88` | Oversized opening cover pushed its title near the bottom of the first desktop screen | Title-first opening story, shorter cover, single-row span | Readers can identify the lead story immediately |
| MEDIUM | Layout | `src/site.css:250` | Archive entry disappeared on mobile | Visible archive entry with wrapping header | Preserve the same navigation path across widths |
| MEDIUM | Typography | `src/site.css:20`; `src/site.css:174` | Fixed pixel typography and fixed-height bar | Rem typography and a flexible, wrapping reader bar | Respect text enlargement without losing controls |
| LOW | Writing | `scripts/build.py:467` | Repeated “X Article” source/type label | Single source/type description | Reduce redundant metadata |

The new wordmark, discovery tools and darker card surfaces are requested product improvements, not retroactive claims that the prior aesthetic was inherently wrong.

## Verification and reproduction

- `npm test`: **25 Python tests + 21 reader DOM/state tests passed**. Covers all 13 static article routes, full Chinese/original/media RSS, source locks, no-JS structure, retry/races, history/focus and the new discovery behavior.
- `XNEWS_BROWSER_CHANNEL=chrome npm run test:browser`: **39 real Chrome checks passed** on Chrome 157. Tests start/stop their own loopback server. Includes combined filters, reset/focus, theme persistence, separate reading offsets, Escape/Forward, progress to 100%, responsive geometry, archive default, fetch-failure retry and no-JS fallback.
- Browser evidence: `.qa-ui/verification.json`, `.qa-ui/accessibility.json` and `.qa-ui/*.png`; generated locally and gitignored, never deployed. Screenshots were visually inspected for desktop light/dark, mobile, scan mode and the 320px reader.
- `node --check src/site.js`, `python3 -m py_compile scripts/build.py`, `git diff --check` passed. `content/` and `public/articles.json` have no diff. RSS article contents are unchanged; only the build timestamp is regenerated.
- Color ratios above were calculated using WCAG relative luminance from the declared opaque token pairs; automated browser contrast checks supplement those calculations.
- Not verified: VoiceOver, Safari/iOS native behavior, RTL, native browser-chrome zoom, external video/audio playback. Browser UI tests block off-origin requests; this is not a playback validation. No production deployment or remote push was performed.

Verdict: **Approve for the inspected local homepage/archive/reader surfaces.** Unverified assistive-technology/platform behavior remains explicitly outside that verdict. Local preview: `npm run preview -- --port 33205`. Changes are in the main checkout `/Users/joe/Documents/ChatGPT/qiaomu-xnews`; no temporary worktree or task branch was created.

---

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
