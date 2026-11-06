# X News

海外创始人长帖 / X Articles / 爆款 AI 视频 → **完整、自然的中文改写（含原媒体）**，附原文链接。

- Live: https://xnews.qiaomu.ai
- RSS: https://xnews.qiaomu.ai/feed.xml
- UI: D「影像刊」visual journal; design contract: [`DESIGN.md`](./DESIGN.md)
- Hosting: Nginx static files on `qiaomu-hostinger`; Worker `xnews` is a fallback. See [`DEPLOYMENT.md`](./DEPLOYMENT.md).

## Develop

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
npm install
npm test
npm run preview
```

Content lives in [`content/articles/`](./content/articles/). Schema + daily ops: [`content/SCHEMA.md`](./content/SCHEMA.md).

## Daily update (parent routine)

1. Pick English founder posts / X Articles / viral AI videos.
2. Fetch with **existing X tools + WebFetch** (no crawler code in this repo).
3. Read [`content/EDITORIAL_PROMPT.md`](./content/EDITORIAL_PROMPT.md): rewrite text **and images/video/audio**, account for every attachment via `rewrite_media`, then write `content/articles/<id>.json`. Reviewed addon: [`content/EDITORIAL_ADDON.md`](./content/EDITORIAL_ADDON.md). Fidelity and natural Chinese override generic style quotas; audit evidence: [`content/EDITORIAL_QA.md`](./content/EDITORIAL_QA.md).
4. Run `npm test`, commit the tested source and generated `public/`, then push. Run `npm run deploy` when release is authorized; it publishes the clean committed tree without rebuilding. Verify the public release header and content as described in [`DEPLOYMENT.md`](./DEPLOYMENT.md).
5. Suggested schedule: **08:00 Asia/Shanghai**.

## Local QA

`npm run preview -- --port 33205` serves the actual site and the local-only iframe fixture at `http://127.0.0.1:33205/__qa/mobile`. The fixture lives outside `public/`, so it is never a deployment asset. See [`QA.md`](./QA.md) for the accepted release checks and explicit playback limitation.

## License

MIT


## Interaction and brand refinement

The homepage keeps the visual-journal direction with an original X mark, serif wordmark, headline-first opening spread, light/dark palette and responsive reading controls. Search by title, author or topic, filter by video presence, or switch to a text-only scan view. `/archive` defaults to scan view. Filter state is shareable in the URL and survives opening/closing the reader. All article content and full RSS remain generated from the existing source files.

```bash
source .venv/bin/activate
npm install
npm test
npm run preview -- --port 33205

# Real Chrome interaction, layout and accessibility checks (local Chrome installed):
XNEWS_BROWSER_CHANNEL=chrome npm run test:browser
# Or install Playwright Chromium and use the default:
npx playwright install chromium
npm run test:browser
```

Browser evidence is written to ignored `.qa-ui/`, outside deployment assets. Release status, production verification and remaining limits are recorded at the top of `QA.md`. `npm run deploy:worker` explicitly refreshes the fallback Worker using the existing OAuth identity; it does not publish the primary site.
