# Anthropic agent memory / dreaming editorial receipt

Review date: 2026-11-07 (Asia/Shanghai). Content-only release under the calibrated researcher/discoverer brief. Do not modify site UI/code/tests/deploy scripts/schema.

## Selection and scope

- Selected: Anthropic Engineering research/methods post **The components of agent memory** (full public article body + figure alts), discovered via official Anthropic X post.
- Discovery: https://x.com/AnthropicAI/status/2118814753154064501 (2026-11-06T21:16:17Z).
- Full article: https://www.anthropic.com/research/components-of-agent-memory (Published Nov 6, 2026; Team: Engineering).
- Authorship: Written by **Lance Martin** with editorial guidance from Caitlin Love, Tom Chivers, Rebecca Hiscott, Jake Eaton, and Blake Wilson; broader acknowledgements retained in Chinese. Attribute as Anthropic Engineering / Lance Martin. **Do not invent a personal X handle for Lance** (not verified for Anthropic authorship this round).
- Valid under brief: concrete evals (CL-Bench numbers, Pokémon file counts/badges, Stainless wiki scaling, Harvey LAB criteria, dreaming correction runs)—substance, not empty product marketing. Not a personal researcher X thread.
- Dedup: source URLs absent from existing `content/articles/*.json` before this write. New id `anthropic-agent-memory-dreaming`.
- `published_at`: X announce time `2026-11-06T21:16:17+00:00`; `date`: 2026-11-06. Source type `x_post` with `related_url` to anthropic.com (vault pattern).

## Media inventory

- Cover/og `6ab2663a…-1200x630.jpg` verified HTTP 200; **not** embedded (optional only if used in article body; body figures are Fig 1–15).
- Page hero decorative illustration `31b7b06…` not treated as a numbered research figure; omitted as non-Figure asset.
- Figures 1–15: durable CDN URLs HEAD/GET verified 200 (no-referrer). Prefer brief mapping: sanity.io for Fig1–5, www-cdn for Fig6–15. Stable ids `media_fig_01` … `media_fig_15`.
- Alts: English alts copied from page `<img alt>` (full text). No invented scene descriptions beyond caption/alt. Playback N/A.
- Placement: editorial mapping Fig1–15 ↔ Chinese sections was verified against the article body/alts. Published `rewrite_media` uses `after_body` + `source_metadata_only` in Figure order because current corpus regressions require contiguous `md_to_html(body_md)` / `body_md` substrings in page/RSS (mid-body `after_paragraph` inserts break those checks). Content-only release cannot change tests/build. Paragraph correspondence remains recorded in the coverage ledger below and in each placement_note.

## Coverage ledger (highlights)

| Source block | Chinese location | Preserved details |
|---|---|---|
| Intro / Kierkegaard / hippocampus / sleep-time compute / dreaming def | Opening | Letta + UC Berkeley sleep-time compute; dreaming corrects/creates/builds/shapes preload |
| Agent memory definition + exclusions | 什么叫智能体记忆 | excludes weights, in-context learning, compaction |
| CL-Bench learning loop + model progression | 记忆有时是在预测… | Sonnet 4.6 theories; Opus 4.7 consolidated; Sonnet 5 confirmed/corrections; Opus 5 first closed loop; Opus/Sonnet 5.5 closed loop |
| Fig3 bar numbers | Same + a3 | Opus 5.5 0.655/0.838; Sonnet 5.5 0.644/0.833; Opus 5 0.564/0.828; Opus 4.7 0.383/0.700; Sonnet 5 0.306/0.610; Sonnet 4.6 0.330/0.364; ~30-question running mean |
| Pokémon salience | 判断什么值得记住 | ~10k steps; Sonnet 3.7: 413 files / 225 folders / 1 badge; Fable 5: 9 files + global.md / 4 badges; alt 977,930 vs 43,406 chars; step 10k +17 steps 6 create/9 delete/no game actions; Magikarp 7 balls quote; Opus 5.5 beat game |
| Steering | 该告诉 Claude… | record-only-failures hurts Opus 5/4.7; Fig5 Sonnet 4.6 0.330/0.364/0.641; Δ −0.234/−0.150/−0.020; Sonnet 5 reads 9/10; Sonnet 4.6 <½ |
| Mt Moon dreaming correction | Dreaming 可以纠正 | wrong PokéCenter east; quotes; three ledge drops; Pewter retreat; Cerulean at action 1935; raw/no-memory fail |
| Wiki / Stainless | 构建新的记忆表征 | ~350k files / ~420M tokens; May Stainless acquisition; 25 Q; 128 Opus 5 sessions; 13%→48%; wiki+search 54%→61%; search alone 53%; wiki alone best 48%; ~20k tokens saved/Q; Fig10 2M→128M tokens; 103/766 → 222/12893 |
| LAB / Borges | Same | 24 Q wiki 87% vs search 73%; single-doc LAB no clear gain; oversized wiki 10 docs/115KB → 68 pages/255 links/203KB =1.77×; Borges On Exactitude in Science |
| Inject hierarchy / Claude Code | 推上记忆层级 | MEMORY.md first 200 lines or 25 KB; longer instructions reduce adherence |
| Goal-focused wiki | 围绕特定目标 | shared provisions.md 41/57 (72%) → per-contract verbatim 57/57 (100%) |
| Second pass | 补上缺口 | 9 missing links; +3 pages incl. index; 38/225 → 41/278; escrow-agreement → buyer-form-escrow-agreement |
| Open questions + acknowledgements | 仍未解决的问题 / 致谢 | when to write vs dream; update cadence; transcript search foundation; full name list + Monika Tuchowska figures + David Hershey Pokémon |

Second pass: finished Chinese checked against WebFetch article body + HTML alts (not only a prior draft). No Qiaomu first-person; Anthropic/Lance Martin attributed. No empty foreshadowing / fake reversals added. Numbers unit/denominator preserved. English quotes in Chinese rendered as attributed paraphrase or retained short English where the source uses CLI-style rules.

## Seed identity notes (this run)

- AK = `@_akhaliq` Ahsen Khaliq (verified prior editorial)—not Karpathy.
- Andrew Ng = `@AndrewYNg`.
- Ben’s Bites creator = `@bentossell` Ben Tossell.
- Anthropic researchers checked in prior/this chain context: alexalbert__, jackclarkSF, AmandaAskell, catherineols, EthanJPerez, `_sholtodouglas` (Scaling RL @AnthropicAI).
- OpenAI: `polynoamial` Noam Brown Research Scientist @OpenAI; `_jasonwei` now Meta (past OpenAI)—mark current employer if cited.
- This article’s public author is Lance Martin via Anthropic Engineering page; no personal Lance X handle asserted.

## Rejected / deferred this run

- Clocktower already published (`clocktower-astra-detection`).
- CaptureFlow / checkwash: user previously uninterested; do not re-publish.
- TailSteer / Muir / LoCo papers from AK: defer abstract-only without full interactive/media audit.
- Ben Tossell book timeline: video-led without full AV transcript—defer.
- OpenAI GPT-6 Cyber already published; BioBasicsBench / cyber framework: thinner official announcements—skip this round.
- Official Anthropic science-modeling blog: skip; prioritize memory post.

## Release plan

1. Confirm git clean aside from new content/editorial (+ generated public after build).
2. `source .venv/bin/activate`; install requirements if needed.
3. `npm test` must pass; do not edit tests/code to pass.
4. Review generated `public/` (index, `a/anthropic-agent-memory-dreaming`, read fingerprint, feed.xml).
5. `git add content public` (and editorial); commit; `git push origin main`.
6. If SSH `qiaomu-hostinger` works and workspace clean: `npm run deploy` (Nginx VPS). Never wrangler for main site.
7. Verify live `X-XNews-Release` matches commit SHA; homepage, article URL, feed item present.
