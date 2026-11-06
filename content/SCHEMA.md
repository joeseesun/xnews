# X News content schema

Daily updates (parent routine, Asia/Shanghai 08:00) should **fetch with X tools + WebFetch** (no scrapers in this repo), read [`EDITORIAL_PROMPT.md`](./EDITORIAL_PROMPT.md), rewrite text **and source media** into Qiaomu Chinese, then write one JSON file per article and rebuild.

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
  "original": {
    "lang": "en",
    "title": "original title or first line",
    "text_md": "full original text as Markdown (preserve line breaks; for X posts include full tweet text; for X Articles full article; for YouTube use title + description / transcript excerpt if available)",
    "media": [
      {"id": "media_stable_id", "type": "image|video|audio|youtube|x_video", "url": "https://...", "alt": "optional verified source alt", "poster": "optional source thumbnail"}
    ]
  },
  "body_md": "完整乔木风格中文正文（Markdown），不混入英文原文；媒体位置用 rewrite_media 描述。",
  "rewrite_media": [
    {
      "media_id": "media_stable_id",
      "placement": "after_body",
      "placement_note": "原文附带媒体；未核验其与具体段落的对应关系。",
      "evidence": "source_metadata_only"
    }
  ]
}
```

### `original` (required)

- Store and display the **source** text and any images / video / audio.
- `media` may be `[]` if none.
- Prefer durable HTTPS media URLs from X media / YouTube (no binary downloads into the repo unless tiny and necessary).
- Do **not** invent media. If a known attachment has no usable URL, preserve available metadata and account for it with an explicit `rewrite_media[].omit_reason`; never fabricate a URL.
- Keep `body_md` as the 乔木 Chinese rewrite only.

### `rewrite_media` (required for editorial output)

Ordered references to `original.media`, not a second copy of the asset. Use `[]` when the source has no media. The build fails if an available original attachment is silently missing, referenced twice, unknown, or imprecisely anchored. One source attachment is rendered at most once **per section**; the rewrite and original remain independently readable, including in RSS.

- Stable identity: `original.media[].id` if present (regex `[A-Za-z][A-Za-z0-9_-]{0,63}`); otherwise `m_` + the first 16 lowercase hexadecimal characters of SHA-256(`type + "\n" + url`, UTF-8). No array-position IDs. History backfill does not modify original objects. Preserve an explicit ID across URL refreshes.
- Known semantic position: `{ "media_id": "...", "placement": "after_paragraph", "after_md": "complete unique Markdown paragraph from body_md", "evidence": "source_position_verified" }`. The paragraph must match a whole Markdown block and appear exactly once; a change to the text must update its anchor. Multiple references at one anchor render in array order. Verified placement does not claim video/audio was viewed.
- Unknown semantic position: `{ "media_id": "...", "placement": "after_body", "placement_note": "原文附带媒体；未核验其与具体段落的对应关系。", "evidence": "source_metadata_only" }`. Render a clearly labeled source-media block after the complete Chinese body; do not infer scene/caption/paragraph relationships.
- Exceptional omission: `{ "media_id": "...", "omit_reason": "specific verified reason" }`; the reason is visible in the Chinese page and RSS, and the stored original remains intact. An empty reason is invalid. “It is in the original tab” is not a valid editorial reason.
- Keep every paragraph in `body_md`; do not duplicate body text into media references. Do not add unsupported Markdown placeholders.
- `image`, `video`, `x_video`, `audio`, `youtube` all participate. Unknown future media types retain their original URL as a link instead of disappearing.
- Native video/audio are manual-only (`controls`, `preload=none`); hidden tabs/closed sheets pause media and unload embeds. Always retain an original-open fallback. A poster or HTTP 200 is not evidence that playback worked.
- UI-only small image cache: `src/media-manifest.json` maps verified public source image/poster URLs to `public/media/`. Original JSON and RSS continue to use upstream HTTPS URLs; the build performs no network fetching.

The media backfill added only `rewrite_media` references to the current 13 stories: seven available source attachments, six media-free stories. A separately authorized fidelity edit then changed only Chinese `title`, `dek`, `body_md`; source text, source metadata, original media, IDs, dates and reference plans stayed intact. See [`EDITORIAL_QA.md`](./EDITORIAL_QA.md). No transcript or scene descriptions were invented.

## Build & deploy

```bash
cd /workspace/xnews
python3 scripts/build.py
# or: npm run build
# Use the existing authenticated Wrangler environment; never commit credentials.
npx wrangler deploy
```

Outputs: `public/index.html`, `public/a/<id>.html`, `public/feed.xml`, `public/articles.json`.

## Style

Read [`EDITORIAL_PROMPT.md`](./EDITORIAL_PROMPT.md) and its stable reviewed addon [`EDITORIAL_ADDON.md`](./EDITORIAL_ADDON.md) first. Its fidelity/natural-Chinese rules override generic style templates. The writing-style/tropes references may help expression, but do not require questions, analogies, short-line emphasis or grand endings. Show the Chinese body **with its source-media references**, then **原文** (unaltered original text + media), then 原文链接. The same reference plan renders the Chinese RSS section. Do not ship Chinese KOL digests here.
