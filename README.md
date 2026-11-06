# X News

海外创始人长帖 / X Articles / 爆款 AI 视频 → **完整、自然的中文改写（含原媒体）**，附原文链接。

- Live: https://xnews.qiaomu.ai
- RSS: https://xnews.qiaomu.ai/feed.xml
- UI: D「影像刊」visual journal; design contract: [`DESIGN.md`](./DESIGN.md)
- Hosting: Cloudflare Worker `xnews` (assets only — no radio KV/R2/Queue)

## Develop

```bash
python3 scripts/build.py
npx wrangler deploy   # needs CLOUDFLARE_API_TOKEN
```

Content lives in [`content/articles/`](./content/articles/). Schema + daily ops: [`content/SCHEMA.md`](./content/SCHEMA.md).

## Daily update (parent routine)

1. Pick English founder posts / X Articles / viral AI videos.
2. Fetch with **existing X tools + WebFetch** (no crawler code in this repo).
3. Read [`content/EDITORIAL_PROMPT.md`](./content/EDITORIAL_PROMPT.md): rewrite text **and images/video/audio**, account for every attachment via `rewrite_media`, then write `content/articles/<id>.json`. Reviewed addon: [`content/EDITORIAL_ADDON.md`](./content/EDITORIAL_ADDON.md). Fidelity and natural Chinese override generic style quotas; audit evidence: [`content/EDITORIAL_QA.md`](./content/EDITORIAL_QA.md).
4. Run `npm test`; deploy only when the current task explicitly authorizes release. (`npx wrangler deploy` is the existing deployment command.)
5. Suggested schedule: **08:00 Asia/Shanghai**.

## Local QA

`npm run preview -- --port 33205` serves the actual site and the local-only iframe fixture at `http://127.0.0.1:33205/__qa/mobile`. The fixture lives outside `public/`, so it is never a deployment asset. See [`QA.md`](./QA.md) for the accepted release checks and explicit playback limitation.

## License

MIT
