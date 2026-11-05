#!/usr/bin/env python3
"""Build X News static site from content/articles/*.json → public/."""
from __future__ import annotations

import html
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
SITE_SUB = "海外创始人长文 · AI 视频 · 乔木中文改写"
TZ_SH = timezone(timedelta(hours=8))

CSS = r"""
:root {
  color-scheme: light;
  --bg: #ffffff;
  --surface: #ffffff;
  --surface-2: #f5f5f3;
  --text: #121212;
  --text-2: #4a4a4a;
  --muted: #767676;
  --faint: #b4b4b4;
  --border: #e2e2e2;
  --rule: #121212;
  --divider: #e5e5e2;
  --accent: #121212;
  --accent-ink: #ffffff;
  --focus: #121212;
  --topbar-h: 60px;
  --side-w: 220px;
  --sans: -apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Noto Sans SC", sans-serif;
  --serif: "Noto Serif SC", "Songti SC", "STSong", "Source Han Serif SC", Georgia, serif;
  --latin: Georgia, "Times New Roman", "Noto Serif SC", serif;
  --ease: cubic-bezier(0.23, 1, 0.32, 1);
  --max-prose: 40em;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    color-scheme: dark;
    --bg: #121212; --surface: #121212; --surface-2: #1c1c1c;
    --text: #ececea; --text-2: #b9b9b6; --muted: #8a8a87; --faint: #555553;
    --border: #2c2c2c; --rule: #ececea; --divider: #2c2c2c;
    --accent: #ececea; --accent-ink: #121212; --focus: #ececea;
  }
}
:root[data-theme="dark"] {
  color-scheme: dark;
  --bg: #121212; --surface: #121212; --surface-2: #1c1c1c;
  --text: #ececea; --text-2: #b9b9b6; --muted: #8a8a87; --faint: #555553;
  --border: #2c2c2c; --rule: #ececea; --divider: #2c2c2c;
  --accent: #ececea; --accent-ink: #121212; --focus: #ececea;
}
* { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; scroll-padding-top: calc(var(--topbar-h) + 12px); }
body { margin: 0; background: var(--bg); color: var(--text); font: 15px/1.7 var(--sans); -webkit-font-smoothing: antialiased; }
a { color: inherit; text-decoration: none; }
a:hover { text-decoration: underline; text-underline-offset: 0.22em; text-decoration-thickness: 1px; }
:focus-visible { outline: 2px solid var(--focus); outline-offset: 2px; }
.sr-only, .skip:not(:focus) { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); }
.skip:focus { position: fixed; z-index: 100; top: 8px; left: 8px; background: var(--text); color: var(--bg); padding: 6px 12px; }

.topbar {
  position: sticky; top: 0; z-index: 30; height: var(--topbar-h);
  display: flex; align-items: center; gap: 6px; padding: 0 24px;
  background: var(--bg); border-bottom: 1px solid var(--border);
}
.icon-btn {
  flex: none; width: 36px; height: 36px; display: grid; place-items: center;
  border: 0; background: transparent; color: var(--text-2); cursor: pointer;
}
.icon-btn:hover { color: var(--text); }
.icon-btn svg { width: 20px; height: 20px; fill: none; stroke: currentColor; stroke-width: 1.6; stroke-linecap: round; stroke-linejoin: round; }
.logo { display: flex; align-items: baseline; gap: 10px; flex: none; margin: 0 14px 0 4px; }
.logo:hover { text-decoration: none; }
.logo-text { font: 700 22px/1 var(--serif); letter-spacing: 0.06em; }
.logo-sub { color: var(--muted); font-size: 12.5px; }
.top-spacer { flex: 1; }
.i-moon { display: none; }
:root[data-theme="dark"] .i-sun { display: none; }
:root[data-theme="dark"] .i-moon { display: block; }
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) .i-sun { display: none; }
  :root:not([data-theme="light"]) .i-moon { display: block; }
}

.layout { display: flex; align-items: flex-start; min-height: calc(100vh - var(--topbar-h) - 100px); }
.sidebar {
  position: sticky; top: var(--topbar-h); flex: none; width: var(--side-w);
  max-height: calc(100vh - var(--topbar-h)); overflow-y: auto;
  padding: 22px 16px 28px 24px; border-right: 1px solid var(--border);
}
.nav { list-style: none; margin: 0; padding: 0; }
.nav a {
  display: flex; align-items: center; gap: 10px; padding: 6px 0;
  color: var(--text-2); font-size: 15px; font-weight: 500;
}
.nav a:hover { color: var(--text); text-decoration: none; }
.nav a.active { color: var(--text); font-weight: 700; }
.nav a svg { width: 18px; height: 18px; flex: none; fill: none; stroke: var(--muted); stroke-width: 1.75; stroke-linecap: round; stroke-linejoin: round; }
.nav a:hover svg, .nav a.active svg { stroke: var(--text); }
.nav-h {
  margin: 26px 0 8px; padding-top: 24px; border-top: 1px solid var(--divider);
  font: 13px/1 var(--latin); letter-spacing: 0.04em; color: var(--muted);
}
.tag-list { list-style: none; margin: 0; padding: 0; }
.tag-list a { display: block; padding: 4px 0; color: var(--text-2); font-size: 14px; }
.tag-list a:hover { color: var(--text); text-decoration: none; }
.main { flex: 1; min-width: 0; padding: 32px 40px 56px; }
.scrim { display: none; }

.page-h { margin-bottom: 8px; padding-top: 10px; }
.page-h h1 { font: 700 clamp(28px, 3.2vw, 40px)/1.25 var(--serif); letter-spacing: 0.02em; }
.sub { color: var(--text-2); margin: 10px 0 0; max-width: 46em; font-size: 15.5px; }
.meta-line { margin: 14px 0 0; color: var(--muted); font-size: 13.5px; display: flex; flex-wrap: wrap; gap: 8px 16px; }

.feed { list-style: none; margin: 28px 0 0; padding: 0; max-width: 760px; }
.feed-item { padding: 22px 0; border-top: 1px solid var(--divider); }
.feed-item:first-child { border-top: 1px solid var(--rule); }
.feed-item a.item-link { display: block; color: inherit; }
.feed-item a.item-link:hover { text-decoration: none; }
.feed-item .date { color: var(--muted); font: 13px var(--latin); letter-spacing: 0.02em; }
.feed-item h2 {
  margin: 8px 0 8px; font: 650 clamp(20px, 2.4vw, 26px)/1.35 var(--serif);
  text-decoration-line: underline; text-decoration-color: transparent;
  text-underline-offset: 0.18em; transition: text-decoration-color 160ms var(--ease);
}
.feed-item a.item-link:hover h2 { text-decoration-color: currentColor; }
.feed-item .dek { margin: 0; color: var(--text-2); font-size: 15.5px; line-height: 1.7; max-width: 42em; }
.feed-item .byline { margin: 10px 0 0; color: var(--muted); font-size: 13px; }

.article { max-width: var(--max-prose); padding-top: 10px; }
.article .kicker { color: var(--muted); font-size: 13px; letter-spacing: 0.04em; }
.article h1 { font: 700 clamp(28px, 3.4vw, 40px)/1.28 var(--serif); letter-spacing: 0.01em; margin: 10px 0 12px; }
.article .dek { color: var(--text-2); font-size: 17px; line-height: 1.7; margin: 0 0 18px; }
.article .meta { display: flex; flex-wrap: wrap; gap: 8px 18px; padding: 14px 0; border-top: 1px solid var(--border); border-bottom: 1px solid var(--border); color: var(--muted); font-size: 13.5px; margin-bottom: 28px; }
.article .meta a { color: var(--text); font-weight: 500; text-decoration: underline; text-decoration-color: var(--border); text-underline-offset: 0.22em; }
.article .meta a:hover { text-decoration-color: currentColor; }
.prose p { margin: 0 0 1.05em; color: var(--text); font-size: 16.5px; line-height: 1.85; }
.prose strong { font-weight: 700; }
.prose a { color: var(--text); font-weight: 500; text-decoration: underline; text-decoration-color: var(--border); text-underline-offset: 0.22em; }
.prose a:hover { text-decoration-color: currentColor; }
.prose ul, .prose ol { margin: 0 0 1.1em; padding-left: 1.3em; }
.prose li { margin: 0.35em 0; color: var(--text); font-size: 16.5px; line-height: 1.75; }
.prose blockquote {
  margin: 1.2em 0; padding: 0.2em 0 0.2em 1em;
  border-left: 2px solid var(--rule); color: var(--text-2);
}
.prose blockquote p { margin: 0; font-size: 16.5px; }
.prose h2 { font: 700 22px var(--serif); margin: 1.6em 0 0.6em; }
.prose hr { border: 0; border-top: 1px solid var(--divider); margin: 1.8em 0; }
.source-box {
  margin-top: 36px; padding: 16px 0 0; border-top: 1px solid var(--rule);
  display: flex; flex-wrap: wrap; gap: 10px 22px; align-items: center;
}
.source-box .lbl { color: var(--muted); font-size: 13.5px; }
.source-box a {
  font-weight: 600; text-decoration: underline; text-underline-offset: 0.22em;
}
.back { display: inline-block; margin-top: 28px; color: var(--text-2); font-size: 14px; }

.footer { border-top: 1px solid var(--divider); padding: 26px 40px 56px; color: var(--muted); font-size: 13.5px; }
.foot-cols { display: flex; flex-wrap: wrap; gap: 18px 56px; max-width: 1100px; }
.foot-brand { font: 700 18px var(--serif); color: var(--text); letter-spacing: 0.04em; }
.foot-about { flex: 1 1 360px; max-width: 46em; }
.foot-about p { margin: 0 0 6px; }
.foot-links { display: flex; flex-direction: column; gap: 6px; }
.foot-links a { color: var(--text-2); font-weight: 500; }

@media (max-width: 899px) {
  .topbar { padding: 0 10px; }
  .sidebar {
    position: fixed; z-index: 40; top: var(--topbar-h); bottom: 0; left: 0;
    background: var(--bg); transform: translateX(-102%); transition: transform .22s var(--ease);
    border-right: 1px solid var(--rule);
  }
  body.drawer-open .sidebar { transform: none; }
  body.drawer-open .scrim { display: block; position: fixed; inset: var(--topbar-h) 0 0 0; z-index: 35; background: rgba(0,0,0,.45); }
  .main { padding: 22px 16px 44px; }
  .logo-sub { display: none; }
  .footer { padding: 22px 16px 44px; }
}
"""

JS = r"""
(function () {
  try {
    var t = localStorage.getItem('xn.theme');
    if (t === 'light' || t === 'dark') document.documentElement.dataset.theme = t;
  } catch (e) {}

  function ready(fn) {
    if (document.readyState !== 'loading') fn();
    else document.addEventListener('DOMContentLoaded', fn);
  }

  ready(function () {
    var themeBtn = document.getElementById('theme-btn');
    if (themeBtn) {
      themeBtn.addEventListener('click', function () {
        var cur = document.documentElement.dataset.theme;
        var next;
        if (cur === 'dark') next = 'light';
        else if (cur === 'light') next = 'dark';
        else next = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'light' : 'dark';
        document.documentElement.dataset.theme = next;
        try { localStorage.setItem('xn.theme', next); } catch (e) {}
      });
    }
    var menu = document.getElementById('menu-btn');
    var scrim = document.getElementById('scrim');
    function close() {
      document.body.classList.remove('drawer-open');
      if (menu) menu.setAttribute('aria-expanded', 'false');
    }
    if (menu) {
      menu.addEventListener('click', function () {
        var open = document.body.classList.toggle('drawer-open');
        menu.setAttribute('aria-expanded', open ? 'true' : 'false');
      });
    }
    if (scrim) scrim.addEventListener('click', close);
  });
})();
"""


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


ICON_HOME = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8"/><path d="M3 10a2 2 0 0 1 .709-1.528l7-5.999a2 2 0 0 1 2.582 0l7 5.999A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/></svg>'
ICON_ARCH = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 22h16"/><path d="M16 4H8a2 2 0 0 0-2 2v14h12V6a2 2 0 0 0-2-2Z"/><path d="M10 10h4M10 14h4"/></svg>'
ICON_RSS = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 11a9 9 0 0 1 9 9"/><path d="M4 4a16 16 0 0 1 16 16"/><circle cx="5" cy="19" r="1"/></svg>'
ICON_ABOUT = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/></svg>'


def shell(title: str, body_main: str, *, description: str = "", active: str = "home", canonical: str = "/") -> str:
    desc = html.escape(description or SITE_SUB)
    canon = SITE_URL.rstrip("/") + canonical
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{desc}">
<meta name="color-scheme" content="light dark">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{html.escape(canon)}">
<link rel="canonical" href="{html.escape(canon)}">
<link rel="alternate" type="application/rss+xml" title="{SITE_NAME}" href="/feed.xml">
<meta name="theme-color" content="#121212">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' fill='%23121212'/%3E%3Ctext x='16' y='22' text-anchor='middle' font-size='14' fill='%23fff' font-family='serif'%3EX%3C/text%3E%3C/svg%3E">
<script>try{{var t=localStorage.getItem('xn.theme');if(t==='light'||t==='dark')document.documentElement.dataset.theme=t}}catch(e){{}}</script>
<link rel="stylesheet" href="/app.css">
</head>
<body>
<a class="skip" href="#main">跳到正文</a>
<header class="topbar">
  <button id="menu-btn" class="icon-btn" aria-label="切换导航栏" aria-controls="sidebar" aria-expanded="false">
    <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 6h16M4 12h16M4 18h16"/></svg>
  </button>
  <a class="logo" href="/" aria-label="{SITE_NAME} 首页">
    <span class="logo-text">{SITE_NAME}</span>
    <span class="logo-sub">海外发现</span>
  </a>
  <div class="top-spacer"></div>
  <a class="icon-btn" href="/feed.xml" aria-label="RSS" title="RSS">
    {ICON_RSS}
  </a>
  <button id="theme-btn" class="icon-btn" aria-label="切换明暗主题" title="切换主题">
    <svg class="i-sun" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg>
    <svg class="i-moon" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg>
  </button>
</header>
<div class="scrim" id="scrim"></div>
<div class="layout">
  <nav id="sidebar" class="sidebar" aria-label="主导航">
    <ul class="nav">
      <li><a href="/" class="{"active" if active=="home" else ""}" data-route="home">{ICON_HOME}今日精选</a></li>
      <li><a href="/archive" class="{"active" if active=="archive" else ""}" data-route="archive">{ICON_ARCH}全部文章</a></li>
      <li><a href="/feed.xml">{ICON_RSS}RSS</a></li>
      <li><a href="/about" class="{"active" if active=="about" else ""}">{ICON_ABOUT}关于</a></li>
    </ul>
    <div class="nav-h">说明</div>
    <p style="margin:0;color:var(--muted);font-size:13px;line-height:1.55">英文长帖 / X Article / 海外 AI 视频 → 乔木中文改写，并附原文链接。</p>
  </nav>
  <main id="main" class="main">
{body_main}
  </main>
</div>
<footer class="footer">
  <div class="foot-cols">
    <div class="foot-about">
      <div class="foot-brand">{SITE_NAME}</div>
      <p style="margin-top:8px">{SITE_SUB}</p>
      <p>内容来自公开 X 帖文、X Articles 与 YouTube；中文为向阳乔木风格改写，非机器直译。</p>
    </div>
    <div class="foot-links">
      <a href="/feed.xml">RSS /feed.xml</a>
      <a href="https://github.com/joeseesun/xnews" target="_blank" rel="noopener">GitHub</a>
      <a href="https://hackerbooks.qiaomu.ai/" target="_blank" rel="noopener">黑客书架</a>
      <a href="https://xnews.qiaomu.ai/">xnews.qiaomu.ai</a>
    </div>
  </div>
</footer>
<script src="/app.js"></script>
</body>
</html>
"""


def source_label(src: dict) -> str:
    t = src.get("type", "link")
    if t == "x_post":
        return f"X · @{src.get('handle','')}"
    if t == "x_article":
        return f"X Article · @{src.get('handle','')}"
    if t == "youtube":
        return "YouTube"
    return src.get("author") or "原文"


def build_feed_items(articles: list[dict]) -> str:
    rows = []
    for a in articles:
        src = a["source"]
        rows.append(f"""<li class="feed-item">
  <a class="item-link" href="/a/{html.escape(a['id'])}">
    <div class="date">{fmt_date(a['date'])}</div>
    <h2>{html.escape(a['title'])}</h2>
    <p class="dek">{html.escape(a.get('dek',''))}</p>
    <div class="byline">{html.escape(source_label(src))} · {html.escape(src.get('author',''))}</div>
  </a>
</li>""")
    return "\n".join(rows)


def rss_full_html(a: dict) -> str:
    """Full article HTML for RSS readers (description + content:encoded)."""
    src = a["source"]
    body = md_to_html(a["body_md"])
    parts = []
    dek = (a.get("dek") or "").strip()
    if dek:
        parts.append(f"<p><em>{html.escape(dek)}</em></p>")
    parts.append(body)
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

    # homepage
    home = f"""
<section class="page-h">
  <h1>今日精选</h1>
  <p class="sub">挑海外创始人长帖、X Article 和爆款 AI 视频，改写成乔木中文，并附上原文链接。风格接近 Ben's Bites，阅读界面接近黑客书架。</p>
  <div class="meta-line"><span>{len(articles)} 篇</span><span><a href="/feed.xml">订阅 RSS</a></span></div>
</section>
<ul class="feed">
{build_feed_items(articles)}
</ul>
"""
    (PUBLIC / "index.html").write_text(
        shell(f"{SITE_NAME} · 海外发现", home, description=SITE_SUB, active="home", canonical="/"),
        encoding="utf-8",
    )

    archive = f"""
<section class="page-h">
  <h1>全部文章</h1>
  <p class="sub">按发布时间倒序。每篇都有中文改写正文和原文链接。</p>
</section>
<ul class="feed">
{build_feed_items(articles)}
</ul>
"""
    (PUBLIC / "archive.html").write_text(
        shell(f"全部文章 · {SITE_NAME}", archive, active="archive", canonical="/archive"),
        encoding="utf-8",
    )

    about = f"""
<article class="article prose">
  <h1>关于 {SITE_NAME}</h1>
  <p>{SITE_NAME} 关注英文世界里值得读的创始人长帖、X Articles，以及海外传播开的 AI 视频。我们用已有的 X / WebFetch 能力取原文，再改写成向阳乔木风格的中文，并始终保留原文链接。</p>
  <p>站点是静态生成：内容放在 <code>content/articles/*.json</code>，本地 <code>npm run build</code> 后用 Wrangler 部署到 Cloudflare Worker <code>xnews</code>（域名 xnews.qiaomu.ai）。</p>
  <p>每日更新由例行任务在 Asia/Shanghai 早上 8 点抓取与改写，然后提交 JSON 并重新 build + deploy。本仓库不包含爬虫。</p>
  <p><a href="/feed.xml">RSS</a> · <a href="https://github.com/joeseesun/xnews" target="_blank" rel="noopener">GitHub</a></p>
</article>
"""
    (PUBLIC / "about.html").write_text(
        shell(f"关于 · {SITE_NAME}", about, active="about", canonical="/about"),
        encoding="utf-8",
    )

    (PUBLIC / "404.html").write_text(
        shell(
            f"未找到 · {SITE_NAME}",
            '<section class="page-h"><h1>页面不存在</h1><p class="sub"><a href="/">返回首页</a></p></section>',
            active="",
            canonical="/404",
        ),
        encoding="utf-8",
    )

    for a in articles:
        src = a["source"]
        body = md_to_html(a["body_md"])
        related = ""
        if src.get("related_url"):
            related = f' · <a href="{html.escape(src["related_url"])}" target="_blank" rel="noopener noreferrer">相关链接</a>'
        main = f"""
<article class="article">
  <div class="kicker">{html.escape(source_label(src))}</div>
  <h1>{html.escape(a['title'])}</h1>
  <p class="dek">{html.escape(a.get('dek',''))}</p>
  <div class="meta">
    <span>{fmt_date(a['date'])}</span>
    <span>{html.escape(src.get('author',''))}</span>
    <span>{' · '.join(html.escape(t) for t in a.get('tags', []))}</span>
  </div>
  <div class="prose">
{body}
  </div>
  <div class="source-box">
    <span class="lbl">原文链接</span>
    <a href="{html.escape(src['url'])}" target="_blank" rel="noopener noreferrer">{html.escape(src['url'])}</a>{related}
  </div>
  <a class="back" href="/">← 返回今日精选</a>
</article>
"""
        (PUBLIC / "a" / f"{a['id']}.html").write_text(
            shell(
                f"{a['title']} · {SITE_NAME}",
                main,
                description=a.get("dek") or a["title"],
                active="archive",
                canonical=f"/a/{a['id']}",
            ),
            encoding="utf-8",
        )

    print(f"Built {len(articles)} articles → {PUBLIC}")


if __name__ == "__main__":
    build()
