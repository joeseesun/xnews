#!/usr/bin/env python3
"""Build X News static site from content/articles/*.json → public/."""
from __future__ import annotations

import html
import hashlib
import json
import re
from datetime import datetime, timezone, timedelta
from email.utils import format_datetime
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content" / "articles"
PUBLIC = ROOT / "public"
SITE_URL = "https://xnews.qiaomu.ai"
SITE_NAME = "X News"
UMAMI_WEBSITE_ID = "31e0098c-6852-46b6-899c-11eed5ed16e1"
if not re.fullmatch(r"[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}", UMAMI_WEBSITE_ID):
    raise ValueError("A valid production Umami website ID is required")
SITE_SUB = "海外创始人长文 · AI 视频 · 乔木中文改写"
TZ_SH = timezone(timedelta(hours=8))

# Presentation sources; public assets are regenerated from these files.
CSS = (ROOT / "src" / "site.css").read_text(encoding="utf-8")
JS = (ROOT / "src" / "site.js").read_text(encoding="utf-8")
# Verified, rendering-only copies of small public images; never rewrite content or RSS URLs.
MEDIA_MANIFEST = json.loads((ROOT / "src" / "media-manifest.json").read_text(encoding="utf-8")) if (ROOT / "src" / "media-manifest.json").exists() else {"assets": []}
LOCAL_MEDIA = {asset["source_url"]: asset["local_url"] for asset in MEDIA_MANIFEST.get("assets", [])}


def local_media_url(url: str) -> str:
    local = LOCAL_MEDIA.get(url, "")
    if local.startswith("/media/") and (PUBLIC / local.lstrip("/")).is_file():
        return local
    return url



def md_to_html(md: str) -> str:
    lines = md.replace("\r\n", "\n").split("\n")
    out: list[str] = []
    i = 0
    in_ul = in_ol = False
    para: list[str] = []

    def flush_para():
        nonlocal para
        if para:
            out.append("<p>" + inline(" ".join(para).strip()) + "</p>")
            para = []

    def close_lists():
        nonlocal in_ul, in_ol
        if in_ul:
            out.append("</ul>"); in_ul = False
        if in_ol:
            out.append("</ol>"); in_ol = False

    def inline(s: str) -> str:
        s = html.escape(s)
        s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
        s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", s)
        s = re.sub(
            r"\[([^\]]+)\]\((https?://[^)\s]+)\)",
            r'<a href="\2" target="_blank" rel="noopener noreferrer">\1</a>',
            s,
        )
        return s

    while i < len(lines):
        line = lines[i]
        if not line.strip():
            flush_para(); close_lists(); i += 1; continue
        if re.match(r"^#{1,3}\s", line):
            flush_para(); close_lists()
            m = re.match(r"^(#{1,3})\s+(.*)$", line)
            out.append(f"<h{len(m.group(1))}>{inline(m.group(2))}</h{len(m.group(1))}>")
            i += 1; continue
        if line.strip() in ("---", "***"):
            flush_para(); close_lists(); out.append("<hr>"); i += 1; continue
        if line.startswith("> "):
            flush_para(); close_lists()
            q = [line[2:]]; i += 1
            while i < len(lines) and lines[i].startswith("> "):
                q.append(lines[i][2:]); i += 1
            out.append("<blockquote><p>" + inline(" ".join(q)) + "</p></blockquote>")
            continue
        m_ul = re.match(r"^[-*]\s+(.*)$", line)
        if m_ul:
            flush_para()
            if in_ol: out.append("</ol>"); in_ol = False
            if not in_ul: out.append("<ul>"); in_ul = True
            out.append(f"<li>{inline(m_ul.group(1))}</li>"); i += 1; continue
        m_ol = re.match(r"^(\d+)\.\s+(.*)$", line)
        if m_ol:
            flush_para()
            if in_ul: out.append("</ul>"); in_ul = False
            if not in_ol: out.append("<ol>"); in_ol = True
            out.append(f"<li>{inline(m_ol.group(2))}</li>"); i += 1; continue
        para.append(line.strip()); i += 1
    flush_para(); close_lists()
    return "\n".join(out)


def load_articles() -> list[dict]:
    items = []
    for path in sorted(CONTENT.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        data["_file"] = path.name
        items.append(data)
    items.sort(key=lambda a: a.get("published_at") or a["date"], reverse=True)
    return items


def fmt_date(date: str) -> str:
    try:
        d = datetime.strptime(date, "%Y-%m-%d")
        week = "一二三四五六日"[d.weekday()]
        return f"{d.year}年{d.month}月{d.day}日 · 周{week}"
    except ValueError:
        return date


def parse_dt(a: dict) -> datetime:
    raw = a.get("published_at") or f"{a['date']}T12:00:00+08:00"
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return datetime.strptime(a["date"], "%Y-%m-%d").replace(tzinfo=TZ_SH)


def shell(title: str, body_main: str, *, description: str = "", active: str = "home", canonical: str = "/") -> str:
    desc = html.escape(description or SITE_SUB)
    canon = SITE_URL.rstrip("/") + canonical
    is_list = active in ("home", "archive") and canonical in ("/", "/archive")
    dialog = '''<dialog class="reader-sheet" id="reader-sheet" aria-labelledby="sheet-label">
  <header class="sheet-bar"><button type="button" class="sheet-close" data-close-sheet><span aria-hidden="true">×</span>返回选刊</button><span class="sheet-brand" id="sheet-label">X News · 阅读</span><a href="/" data-sheet-permalink target="_blank" rel="noopener noreferrer">独立页面 ↗</a></header>
  <div class="sheet-scroll" tabindex="-1"></div>
</dialog>''' if is_list else ""
    def current(route):
        return ' aria-current="page"' if active == route else ""
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{desc}">
<meta name="color-scheme" content="light dark">
<meta name="theme-color" content="#fffefa">
<meta property="og:type" content="{'article' if canonical.startswith('/a/') else 'website'}">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{html.escape(canon)}">
<link rel="canonical" href="{html.escape(canon)}">
<link rel="alternate" type="application/rss+xml" title="{SITE_NAME}" href="/feed.xml">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='-7 -7 58 58'%3E%3Crect x='-7' y='-7' width='58' height='58' rx='5' fill='%231b1d18'/%3E%3Cpath fill='%23fffefa' d='M2 0h11l29 44H31zM32 0h10L26 18l-5-7zM17 26l5 7-10 11H2z'/%3E%3C/svg%3E">
<script>try{{var t=localStorage.getItem('xn.theme');if(t==='light'||t==='dark')document.documentElement.dataset.theme=t}}catch(e){{}}</script>
<link rel="stylesheet" href="/app.css">
<script src="/app.js" defer></script>
<script defer src="https://umami.qiaomu.ai/script.js" data-website-id="{UMAMI_WEBSITE_ID}" data-domains="xnews.qiaomu.ai" data-exclude-search="true" data-exclude-hash="true"></script>
</head>
<body>
<a class="skip" href="#main">跳到正文</a>
<header class="site-header">
  <a class="brand" href="/" aria-label="X News 海外发现首页"><span class="brand-wordmark" aria-hidden="true"><svg class="brand-mark" viewBox="0 0 44 44" fill="currentColor"><path d="M2 0h11l29 44H31zM32 0h10L26 18l-5-7zM17 26l5 7-10 11H2z"/></svg><span class="brand-name">News<span class="brand-period">.</span></span></span><span class="brand-sub">海外发现<span>英文原作 · 中文视角</span></span></a>
  <div class="header-side"><nav class="site-nav" aria-label="主导航"><a href="/"{current('home')}>精选</a><a class="archive-nav" href="/archive"{current('archive')}>往期</a><a href="/feed.xml" aria-label="订阅全文 RSS">订阅 RSS <span aria-hidden="true">↗</span></a></nav><button type="button" class="icon-button" id="theme-btn" aria-label="切换为暗色主题" aria-pressed="false"><svg viewBox="0 0 24 24" width="19" height="19" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><circle cx="12" cy="12" r="8"/><path d="M12 4a8 8 0 0 1 0 16Z" fill="currentColor" stroke="none"/></svg></button></div>
</header>
<main class="site-main" id="main">
{body_main}
</main>
<footer class="site-footer"><span>海外创始人长文 · 乔木中文改写<br>每日 08:00 更新 · 中国标准时间（UTC+8）</span><nav class="footer-links" aria-label="页尾导航"><a href="/feed.xml">全文 RSS ↗</a><a href="/archive">全部文章</a><a href="/about">关于</a></nav></footer>
{dialog}
</body>
</html>
'''


def source_label(src: dict) -> str:
    t = src.get("type", "link")
    if t == "x_post":
        return f"X · @{src.get('handle','')}"
    if t == "x_article":
        return f"X Article · @{src.get('handle','')}"
    if t == "youtube":
        return "YouTube"
    return src.get("author") or "原文"




def youtube_id(url: str) -> str:
    m = re.search(r"(?:v=|youtu\.be/|embed/)([A-Za-z0-9_-]{6,})", url or "")
    return m.group(1) if m else ""


def original_notice(a: dict) -> str:
    """Describe availability, never turn stored video excerpts into claimed transcripts."""
    original = a.get("original") or {}
    if original.get("completeness") in ("excerpt", "partial") or a["id"] == "deepseek-super-agent-harness":
        return "视频原文摘录，非完整逐字稿；请以原视频为准。" if a["source"].get("type") == "youtube" else "当前保留的是原文摘录，完整内容请查看原文链接。"
    if not original.get("text_md"):
        return "此条目暂未保存原文文字；媒体与原文链接仍可查看。"
    return ""


def media_id(media: dict) -> str:
    """Persist explicit IDs for new media; existing source objects need not be rewritten."""
    explicit = media.get("id")
    if explicit:
        if not isinstance(explicit, str) or not re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]{0,63}", explicit):
            raise ValueError("Invalid original media ID")
        return explicit
    identity = media.get("type", "") + "\n" + media.get("url", "")
    return "m_" + hashlib.sha256(identity.encode()).hexdigest()[:16]


def rewrite_media_plan(a: dict) -> tuple[dict, list]:
    """Fail closed on silent media loss, fabricated references or ambiguous placement."""
    available = {}
    for media in (a.get("original") or {}).get("media") or []:
        mid = media_id(media)
        if mid in available and available[mid] != media:
            raise ValueError(f"{a['id']}: media ID collision {mid}")
        available[mid] = media
    references = a.get("rewrite_media", [])
    if not isinstance(references, list):
        raise ValueError(f"{a['id']}: rewrite_media must be an ordered array")
    seen = set()
    blocks = re.split(r"\n\s*\n", a["body_md"].strip())
    for ref in references:
        mid = ref.get("media_id")
        if mid not in available or mid in seen:
            raise ValueError(f"{a['id']}: unknown or repeated rewrite media {mid}")
        seen.add(mid)
        if "omit_reason" in ref:
            if not isinstance(ref["omit_reason"], str) or not ref["omit_reason"].strip():
                raise ValueError(f"{a['id']}: omission needs an explicit reason")
            continue
        if not available[mid].get("url"):
            raise ValueError(f"{a['id']}: missing URL needs an explicit omission reason")
        if ref.get("evidence") not in ("source_metadata_only", "source_position_verified"):
            raise ValueError(f"{a['id']}: reference must state its placement evidence")
        if ref.get("placement") not in ("after_body", "after_paragraph"):
            raise ValueError(f"{a['id']}: invalid rewrite media placement")
        if ref.get("placement") == "after_body" and not (ref.get("placement_note") or "").strip():
            raise ValueError(f"{a['id']}: uncertain placement must be labeled")
        if ref.get("placement") == "after_paragraph":
            if ref.get("evidence") != "source_position_verified":
                raise ValueError(f"{a['id']}: precise placement requires source-position evidence")
            anchor = ref.get("after_md", "")
            if not anchor or blocks.count(anchor) != 1 or md_to_html(a["body_md"]).count(md_to_html(anchor)) != 1:
                raise ValueError(f"{a['id']}: placement paragraph must be complete and unique")
    if set(available) != seen:
        raise ValueError(f"{a['id']}: original media missing from rewrite_media: {sorted(set(available) - seen)}")
    return available, references


def render_rewrite(a: dict, *, rss: bool = False) -> str:
    available, refs = rewrite_media_plan(a)
    body = md_to_html(a["body_md"])
    groups = {}
    omissions = []
    for ref in refs:
        if "omit_reason" in ref:
            omissions.append(f'<p class="completeness-note">原文媒体未在改写中展示：{html.escape(ref["omit_reason"])}</p>')
            continue
        key = (ref["placement"], ref.get("after_md", ""))
        groups.setdefault(key, []).append((available[ref["media_id"]], ref.get("placement_note", "")))
    appended = []
    for (placement, anchor), entries in groups.items():
        media = [entry[0] for entry in entries]
        note = " ".join(dict.fromkeys(entry[1] for entry in entries if entry[1]))
        rendered = rss_media_html(media) if rss else render_media_html(media, a["source"]["url"])
        label = "原文附带媒体" if placement == "after_body" else "原文媒体"
        notice = f'<p class="completeness-note">{html.escape(note)}</p>' if note else ""
        block = f'<section class="rewrite-source-media" aria-label="{label}"><h3 class="source-media-heading">{label}</h3>{notice}{rendered}</section>'
        if placement == "after_paragraph":
            anchor_html = md_to_html(anchor)
            body = body.replace(anchor_html, anchor_html + block, 1)
        else:
            appended.append(block)
    return body + "\n" + "\n".join(appended + omissions)


def render_media_html(media: list, source_url: str = "") -> str:
    if not media:
        return ""
    parts = ['<div class="original-media">']
    seen = set()
    for m in media:
        mid = media_id(m)
        if mid in seen:
            continue
        seen.add(mid)
        t = (m or {}).get("type") or ""
        url = (m or {}).get("url") or ""
        if not url:
            continue
        u = html.escape(url, quote=True)
        alt = html.escape((m or {}).get("alt") or "原帖配图", quote=True)
        poster = (m or {}).get("poster") or ""
        fallback = html.escape(source_url or url, quote=True)
        if t == "image":
            rendered = f'<img src="{html.escape(local_media_url(url), quote=True)}" data-original-src="{u}" alt="{alt}" loading="lazy" decoding="async" referrerpolicy="no-referrer">'
            label = "原帖图片"
        elif t in ("video", "x_video"):
            poster_attr = f' poster="{html.escape(local_media_url(poster), quote=True)}" data-original-poster="{html.escape(poster, quote=True)}"' if poster else ""
            rendered = f'<video controls playsinline preload="none" src="{u}"{poster_attr} aria-label="原帖视频"></video>'
            if poster:
                rendered += f'<img class="video-poster-fallback" data-video-fallback src="{html.escape(local_media_url(poster), quote=True)}" alt="原视频封面" loading="lazy" hidden>'
            label = "原帖视频 · 外部播放"
        elif t == "audio":
            rendered = f'<audio controls preload="none" src="{u}" aria-label="原帖音频"></audio>'
            label = "原帖音频"
        elif t == "youtube" and youtube_id(url):
            vid = html.escape(youtube_id(url), quote=True)
            rendered = (f'<div class="yt"><iframe src="https://www.youtube-nocookie.com/embed/{vid}" '
                        'title="原视频（需手动播放）" allow="encrypted-media; picture-in-picture; fullscreen" '
                        'referrerpolicy="strict-origin-when-cross-origin" allowfullscreen loading="lazy"></iframe></div>')
            label = "外部播放器 · 需手动播放"
        else:
            parts.append(f'<p><a href="{u}" target="_blank" rel="noopener noreferrer">打开原始媒体 ↗</a></p>')
            continue
        parts.append(f'''<figure class="media-figure" data-media-id="{html.escape(mid, quote=True)}"><div class="media-frame">{rendered}<p class="media-error" role="status" hidden>媒体未能载入，请通过下方原文链接查看。</p></div><figcaption><span>{label}</span><a href="{fallback}" target="_blank" rel="noopener noreferrer">无法显示？去原文查看 ↗</a></figcaption></figure>''')
    parts.append("</div>")
    return "\n".join(parts) if len(parts) > 2 else ""


def render_original_section(a: dict) -> str:
    orig = a.get("original") or {}
    text = (orig.get("text_md") or "").strip()
    title = (orig.get("title") or "").strip()
    title_html = f'<h3 class="original-title">{html.escape(title)}</h3>' if title else ""
    notice = original_notice(a)
    notice_html = f'<p class="completeness-note">{html.escape(notice)}</p>' if notice else ""
    body = md_to_html(text) if text else ""
    lang = html.escape(orig.get("lang") or "en", quote=True)
    return f'''<section class="reader-panel" id="original" data-reader-panel="original" aria-label="原文">
<h2 class="section-heading">原文</h2>{notice_html}{title_html}
{render_media_html(orig.get('media') or [], a['source']['url'])}
<div class="prose" lang="{lang}">{body}</div>
</section>'''


def rss_media_html(media: list) -> str:
    """Upstream media URLs, once per section; no local-path leakage into RSS."""
    parts, seen = [], set()
    for m in media:
        mid = media_id(m)
        if mid in seen:
            continue
        seen.add(mid)
        url = m.get("url") or ""
        if not url:
            continue
        u = html.escape(url, quote=True)
        alt = html.escape(m.get("alt") or "", quote=True)
        t = m.get("type", "")
        poster = m.get("poster") or ""
        poster_attr = f' poster="{html.escape(poster, quote=True)}"' if poster else ""
        if t == "image":
            rendered = f'<img src="{u}" alt="{alt}">'
        elif t in ("video", "x_video"):
            rendered = f'<video controls playsinline preload="none" src="{u}"{poster_attr}></video>'
        elif t == "audio":
            rendered = f'<audio controls preload="none" src="{u}"></audio>'
        elif t == "youtube" and youtube_id(url):
            vid = html.escape(youtube_id(url))
            rendered = f'<iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/{vid}" title="原视频（手动播放）" loading="lazy" allowfullscreen></iframe>'
        else:
            rendered = ""
        parts.append(f'<figure data-media-id="{html.escape(mid)}">{rendered}<figcaption><a href="{u}">打开原始媒体 ↗</a></figcaption></figure>')
    return "\n".join(parts)



def cover_asset(a: dict) -> tuple[str, str]:
    for media in (a.get("original") or {}).get("media") or []:
        if media.get("type") == "image" and media.get("url"):
            return local_media_url(media["url"]), media.get("alt") or "原帖配图"
        if media.get("poster"):
            return local_media_url(media["poster"]), "原视频封面"
        if media.get("type") == "youtube" and youtube_id(media.get("url") or ""):
            return f'https://i.ytimg.com/vi/{youtube_id(media["url"])}/hqdefault.jpg', "原视频封面"
    return "", ""


def story_type(a: dict) -> str:
    source_type = a["source"].get("type")
    if source_type == "youtube":
        return "视频"
    if source_type == "x_article":
        return "X Article"
    if any(m.get("type") in ("video", "x_video", "youtube") for m in (a.get("original") or {}).get("media") or []):
        return "长帖 / 视频"
    return "长帖" if source_type == "x_post" else "文章"


def cover_word(a: dict) -> str:
    # Use stored names or numbers from the actual title, not invented editorial claims.
    if "$300" in a["title"]:
        return "$300"
    name = a["source"].get("author") or a["source"].get("handle") or SITE_NAME
    if "/" in name:
        name = a["source"].get("handle") or name.split("/")[0]
    return name.split()[0] if name.split() else SITE_NAME


def reading_minutes(a: dict) -> int:
    """Approximate Chinese reading time; video duration is deliberately excluded."""
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", a.get("body_md") or "")
    units = len(re.findall(r"[\u3400-\u9fff]|[A-Za-z0-9]+", text))
    return max(1, (units + 299) // 300)


def discovery_tools(articles: list[dict], *, archive: bool = False) -> str:
    videos = sum("视频" in story_type(a) for a in articles)
    return f'''<section class="discovery" data-discovery data-default-view="{'list' if archive else 'journal'}" aria-label="查找文章" hidden>
<div class="discovery-top"><div class="filter-group" role="group" aria-label="内容类型">
<button type="button" data-filter="all" aria-pressed="true">全部 <span>{len(articles)}</span></button>
<button type="button" data-filter="text" aria-pressed="false">图文 <span>{len(articles) - videos}</span></button>
<button type="button" data-filter="video" aria-pressed="false">含视频 <span>{videos}</span></button></div>
<div class="search-field"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 5 5"/></svg><label class="sr-only" for="story-search">搜索标题、作者或主题</label><input id="story-search" type="search" name="q" placeholder="搜索标题、作者或主题" autocomplete="off" aria-controls="news-grid"><button type="button" data-clear-search aria-label="清除搜索" hidden>×</button></div></div>
<div class="discovery-bottom"><p data-result-count role="status" aria-live="polite" aria-atomic="true"></p><div class="view-switch" role="group" aria-label="浏览方式"><button type="button" data-layout="journal" aria-pressed="true"><svg viewBox="0 0 18 18" width="15" height="15" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M2 2h5v14H2zM11 2h5v5h-5zM11 11h5v5h-5z"/></svg>影像刊</button><button type="button" data-layout="list" aria-pressed="false"><svg viewBox="0 0 18 18" width="15" height="15" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M2 3h14M2 9h14M2 15h14"/></svg>速览</button></div></div>
</section>'''


def discovery_empty() -> str:
    return '''<section class="search-empty" data-search-empty hidden><p class="empty-symbol" aria-hidden="true">↳</p><h2>没有找到匹配的文章</h2><p data-empty-description></p><button class="reset-button" type="button" data-reset-filters>查看全部文章</button></section>'''


def build_feed_items(articles: list[dict]) -> str:
    if not articles:
        return '<section class="empty-state"><h2>还没有文章</h2><p>稍后再来，或先订阅 <a href="/feed.xml">全文 RSS</a>。</p></section>'
    rows = []
    for index, a in enumerate(articles):
        src = a["source"]
        image, alt = cover_asset(a)
        slug = html.escape(a["id"], quote=True)
        kind = story_type(a)
        author = html.escape(src.get("author") or src.get("handle") or "原作者")
        classes = ["news-card", "card--media" if image else "card--text"]
        if index == 0 and image:
            classes.append("is-featured")
        if not image:
            classes.append("tone-ink" if index % 3 == 1 else "tone-sage" if index % 3 == 2 else "tone-paper")
        word = html.escape(cover_word(a))
        if image:
            badge = f'<span class="cover-badge">▶ {html.escape(kind)}</span>' if "视频" in kind else ""
            cover = f'''<div class="cover" data-cover><div class="cover-fallback" aria-hidden="true"><span class="cover-word">{word}</span></div><img src="{html.escape(image, quote=True)}" alt="{html.escape(alt, quote=True)}" loading="{'eager' if index == 0 else 'lazy'}" decoding="async" {'fetchpriority="high"' if index == 0 else ''} referrerpolicy="no-referrer">{badge}</div>'''
        else:
            cover = f'<div class="type-cover" aria-hidden="true"><span class="type-index">{index + 1:02d} / VOICES</span><span class="cover-word">{word}<span class="type-dot">.</span></span></div>'
        search = html.escape(' '.join([a['title'], a.get('dek') or '', src.get('author') or '', src.get('handle') or '', ' '.join(a.get('tags') or [])]), quote=True)
        card_body = f'''<div class="card-body"><div class="card-meta"><span>{html.escape(kind)} / {author}</span><time datetime="{html.escape(a['date'], quote=True)}">{html.escape(a['date'][5:].replace('-', '.'))}</time></div>
<h2 class="card-title">{html.escape(a['title'])}</h2><p class="card-dek">{html.escape(a.get('dek') or '')}</p><div class="card-end"><span>中文约 {reading_minutes(a)} 分钟</span><span class="card-read">阅读全文 <span class="card-arrow" aria-hidden="true">→</span></span></div></div>'''
        # Lead with the headline, keeping source and visual reading order identical.
        card_content = card_body + cover if "is-featured" in classes else cover + card_body
        rows.append(f'''<article class="{' '.join(classes)}" id="story-{slug}" data-kind="{'video' if '视频' in kind else 'text'}" data-search="{search}">
<a class="card-link" href="/a/{slug}" id="read-{slug}" data-open-reader data-source-url="{html.escape(src['url'], quote=True)}">
{card_content}
</a><a class="cover-error-link" href="{html.escape(src['url'], quote=True)}" target="_blank" rel="noopener noreferrer">封面未能显示 · 去原文查看 ↗</a>
</article>''')
    return '\n'.join(rows)


def render_article(a: dict) -> str:
    src = a["source"]
    source_url = html.escape(src["url"], quote=True)
    source = source_label(src)
    kind = story_type(a)
    kicker = source if kind in source else f"{source} / {kind}"
    related = f'<a href="{html.escape(src["related_url"], quote=True)}" target="_blank" rel="noopener noreferrer">相关链接 ↗</a>' if src.get("related_url") else ""
    return f'''<article class="article-reader" data-article-id="{html.escape(a['id'], quote=True)}">
<a class="article-back" href="/">← 返回选刊</a>
<header class="article-header"><p class="article-kicker">{html.escape(kicker)}</p><h1>{html.escape(a['title'])}</h1><p class="article-dek">{html.escape(a.get('dek') or '')}</p><div class="article-meta"><time datetime="{html.escape(a['date'], quote=True)}">{fmt_date(a['date'])}</time><span>{html.escape(src.get('author') or '')}</span><span>{' · '.join(html.escape(t) for t in a.get('tags') or [])}</span></div></header>
<nav class="reader-tabs" aria-label="文章版本与来源"><div data-tabs><a href="#rewrite" id="tab-rewrite" data-view="rewrite">乔木改写</a><a href="#original" id="tab-original" data-view="original">原文</a></div><a class="reader-source" href="{source_url}" target="_blank" rel="noopener noreferrer">原文链接 ↗</a><div class="reading-position" hidden><progress max="100" value="0" aria-label="当前版本阅读进度"></progress><span data-reading-percent aria-hidden="true">0%</span></div></nav>
<section class="reader-panel" id="rewrite" data-reader-panel="rewrite" aria-label="乔木改写"><h2 class="section-heading">乔木改写</h2><div class="prose">{render_rewrite(a)}</div></section>
{render_original_section(a)}
<footer class="source-box"><span>内容来自原作者；中文为乔木风格改写，非逐字翻译。</span><div><a href="{source_url}" target="_blank" rel="noopener noreferrer">打开原文 ↗</a>{related}</div></footer>
</article>'''


def rss_full_html(a: dict) -> str:
    """Full article HTML for RSS readers (description + content:encoded)."""
    src = a["source"]
    body = render_rewrite(a, rss=True)
    parts = []
    dek = (a.get("dek") or "").strip()
    if dek:
        parts.append(f"<p><em>{html.escape(dek)}</em></p>")
    parts.append("<h2>乔木改写</h2>")
    parts.append(body)
    orig = a.get("original") or {}
    otext = (orig.get("text_md") or "").strip()
    omedia = orig.get("media") or []
    if otext or omedia:
        parts.append("<h2>原文</h2>")
        notice = original_notice(a)
        if notice:
            parts.append(f"<p>{html.escape(notice)}</p>")
        otitle = (orig.get("title") or "").strip()
        if otitle:
            parts.append(f"<p><em>{html.escape(otitle)}</em></p>")
        media_html = rss_media_html(omedia)
        if media_html:
            parts.append(media_html)
        if otext:
            parts.append(md_to_html(otext))
    parts.append(
        "<p><strong>原文链接：</strong>"
        f'<a href="{html.escape(src["url"])}">{html.escape(src["url"])}</a></p>'
    )
    if src.get("related_url"):
        parts.append(
            "<p><strong>相关链接：</strong>"
            f'<a href="{html.escape(src["related_url"])}">{html.escape(src["related_url"])}</a></p>'
        )
    return "\n".join(parts)


def build_rss(articles: list[dict]) -> str:
    items = []
    for a in articles:
        link = f"{SITE_URL}/a/{a['id']}"
        dt = parse_dt(a)
        full = rss_full_html(a)
        # CDATA so readers get full HTML; escape any ]]> in body
        cdata = full.replace("]]>", "]]]]><![CDATA[>")
        items.append(f"""    <item>
      <title>{xml_escape(a['title'])}</title>
      <link>{xml_escape(link)}</link>
      <guid isPermaLink="true">{xml_escape(link)}</guid>
      <pubDate>{format_datetime(dt.astimezone(timezone.utc))}</pubDate>
      <author>{xml_escape(a['source'].get('author',''))}</author>
      <description><![CDATA[{cdata}]]></description>
      <content:encoded><![CDATA[{cdata}]]></content:encoded>
    </item>""")
    now = datetime.now(timezone.utc)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/">
  <channel>
    <title>{xml_escape(SITE_NAME)}</title>
    <link>{SITE_URL}/</link>
    <description>{xml_escape(SITE_SUB)}</description>
    <language>zh-CN</language>
    <lastBuildDate>{format_datetime(now)}</lastBuildDate>
    <atom:link href="{SITE_URL}/feed.xml" rel="self" type="application/rss+xml"/>
{chr(10).join(items)}
  </channel>
</rss>
"""


def build() -> None:
    articles = load_articles()
    if not articles:
        raise SystemExit("No articles in content/articles/")

    PUBLIC.mkdir(parents=True, exist_ok=True)
    (PUBLIC / "a").mkdir(exist_ok=True)
    (PUBLIC / "app.css").write_text(CSS, encoding="utf-8")
    (PUBLIC / "app.js").write_text(JS, encoding="utf-8")
    (PUBLIC / "feed.xml").write_text(build_rss(articles), encoding="utf-8")
    (PUBLIC / "articles.json").write_text(
        json.dumps(
            [
                {
                    "id": a["id"],
                    "date": a["date"],
                    "title": a["title"],
                    "dek": a.get("dek"),
                    "url": f"/a/{a['id']}",
                    "source_url": a["source"]["url"],
                    "tags": a.get("tags", []),
                }
                for a in articles
            ],
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    latest = articles[0]["date"]
    heading = f'''<section class="edition-line"><div><p class="edition-kicker">THE EDIT <span aria-hidden="true">/</span> 近期精选</p><h1 tabindex="-1">看见世界的新想法。</h1><p class="edition-description">创始人的思考，正在发生的 AI。长帖、文章与影像，一起读。</p></div><div class="edition-meta"><span class="edition-label">最新收录</span><time datetime="{html.escape(latest, quote=True)}">{html.escape(latest.replace('-', '.'))}</time><span class="edition-note">乔木选编 · 保留原文与媒体</span></div></section>'''
    home = heading + discovery_tools(articles) + f'<section class="news-grid" id="news-grid" data-news-grid aria-label="海外发现选刊">{build_feed_items(articles)}</section>' + discovery_empty()
    (PUBLIC / "index.html").write_text(
        shell(f"{SITE_NAME} · 海外发现", home, description=SITE_SUB, active="home", canonical="/"), encoding="utf-8",
    )
    archive = f'''<section class="edition-line"><div><h1 tabindex="-1">全部文章</h1><p>按发布时间倒序，乔木改写与原文一起保留。</p></div><p class="edition-meta">共 {len(articles)} 篇</p></section>''' + discovery_tools(articles, archive=True) + f'<section class="news-grid" id="news-grid" data-news-grid aria-label="全部文章">{build_feed_items(articles)}</section>' + discovery_empty()
    (PUBLIC / "archive.html").write_text(
        shell(f"全部文章 · {SITE_NAME}", archive, active="archive", canonical="/archive"), encoding="utf-8",
    )
    about = f'''<article class="about-copy prose"><h1>关于 {SITE_NAME}</h1><p>从英文世界的创始人长帖、X Articles 与 AI 视频中，挑出值得读的内容，改写成乔木风格的中文。</p><p>每篇都保留已有原文、图片或视频，以及可直接打开的来源链接。中文是改写，不是逐字翻译；视频摘录不等于完整逐字稿，原作以来源页面为准。</p><p>每日 08:00（中国标准时间，UTC+8）更新。你可以在网页阅读，也可以<a href="/feed.xml">订阅全文 RSS</a>；RSS 包含中文改写、已保存的原文和媒体，不只提供摘要。</p><p><a href="/archive">全部文章</a> · <a href="https://github.com/joeseesun/xnews" target="_blank" rel="noopener noreferrer">项目源码 ↗</a></p></article>'''
    (PUBLIC / "about.html").write_text(shell(f"关于 · {SITE_NAME}", about, active="about", canonical="/about"), encoding="utf-8")
    (PUBLIC / "404.html").write_text(
        shell(f"未找到 · {SITE_NAME}", '<section class="empty-state"><p>404 / 未找到</p><h1>这篇内容不在这里。</h1><p>链接可能不完整，或内容已经移动。<a href="/">返回选刊</a>，或去<a href="/archive">全部文章</a>找找。</p></section>', active="", canonical="/404"), encoding="utf-8",
    )
    for a in articles:
        (PUBLIC / "a" / f"{a['id']}.html").write_text(
            shell(f"{a['title']} · {SITE_NAME}", render_article(a), description=a.get("dek") or a["title"], active="article", canonical=f"/a/{a['id']}"), encoding="utf-8",
        )

    print(f"Built {len(articles)} articles → {PUBLIC}")


if __name__ == "__main__":
    build()
