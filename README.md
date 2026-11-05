# X News

海外创始人长帖 / X Articles / 爆款 AI 视频 → **乔木风格中文改写**，附原文链接。

- Live: https://xnews.qiaomu.ai
- RSS: https://xnews.qiaomu.ai/feed.xml
- UI: reading site inspired by [黑客书架](https://hackerbooks.qiaomu.ai/) (topbar / sidebar / theme)
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
3. Rewrite to Qiaomu Chinese; write `content/articles/<id>.json`.
4. `python3 scripts/build.py && npx wrangler deploy`.
5. Suggested schedule: **08:00 Asia/Shanghai**.

## License

MIT
