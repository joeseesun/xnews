# X News content schema

Daily updates (parent routine, Asia/Shanghai 08:00) should **fetch with X tools + WebFetch** (no scrapers in this repo), rewrite into Qiaomu Chinese, then write one JSON file per article and rebuild.

## File

`content/articles/<id>.json`

`id`: kebab-case slug, unique. Example: `karpathy-hackertube`.

## Fields

```json
{
  "id": "karpathy-hackertube",
  "date": "2026-11-01",
  "published_at": "2026-11-01T18:14:46+00:00",
  "source": {
    "type": "x_post | x_article | youtube | web",
    "url": "https://x.com/... or https://www.youtube.com/watch?v=...",
    "author": "Display name",
    "handle": "karpathy",
    "title_en": "Original English title or first line",
    "related_url": "optional secondary link"
  },
  "title": "中文标题",
  "dek": "一句话导读",
  "tags": ["AI coding", "product"],
  "body_md": "乔木风格中文正文（Markdown）。文末不要另附来源注释；原文链接由 source.url 渲染。"
}
```

## Build & deploy

```bash
cd /workspace/xnews
python3 scripts/build.py
# or: npm run build
source /home/box/.cf_aitv.env   # CLOUDFLARE_API_TOKEN + ACCOUNT_ID
npx wrangler deploy
```

Outputs: `public/index.html`, `public/a/<id>.html`, `public/feed.xml`, `public/articles.json`.

## Style

Read `/home/box/agent-data/workflows/qiaomu-writer/references/writing-style.md` and `tropes.md` before rewriting. Show Chinese body + 原文链接. Do not ship Chinese KOL digests here.
