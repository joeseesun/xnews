"""Static discovery metadata shared by human readers and search crawlers."""
import html
import json
from xml.sax.saxutils import escape

SITE = 'https://xnews.qiaomu.ai'
PUBLISHER = {'@type': 'Organization', '@id': SITE + '/#publisher', 'name': 'X News', 'url': SITE + '/', 'description': '海外创始人长文与 AI 视频的中文改写选刊'}


def metadata(title, description, canonical, article=None, image=''):
    """Only describe recorded facts; do not manufacture modification timestamps."""
    url = SITE + canonical
    tags = ['<meta property="og:locale" content="zh_CN">', '<meta name="twitter:card" content="' + ('summary_large_image' if image else 'summary') + '">']
    for key, value in [('twitter:title', title), ('twitter:description', description)]:
        tags.append(f'<meta name="{key}" content="{html.escape(value, quote=True)}">')
    if image:
        image = SITE + image if image.startswith('/') else image
        tags += [f'<meta property="og:image" content="{html.escape(image, quote=True)}">', f'<meta name="twitter:image" content="{html.escape(image, quote=True)}">']
    graph = [PUBLISHER, {'@type': 'WebSite', '@id': SITE + '/#website', 'name': 'X News', 'url': SITE + '/', 'inLanguage': 'zh-CN', 'publisher': {'@id': SITE + '/#publisher'}}]
    page = {'@type': 'WebPage', '@id': url + '#page', 'url': url, 'name': title, 'description': description, 'inLanguage': 'zh-CN', 'isPartOf': {'@id': SITE + '/#website'}}
    if article:
        source = article['source']
        original = {'@type': 'CreativeWork', 'url': source['url'], 'name': source.get('title_en') or source.get('author') or article['title']}
        if article.get('published_at'):
            original['datePublished'] = article['published_at']
        node = {'@type': 'Article', '@id': url + '#article', 'url': url, 'mainEntityOfPage': {'@id': url + '#page'}, 'headline': article['title'], 'description': description, 'inLanguage': 'zh-CN', 'datePublished': article['date'], 'author': {'@id': SITE + '/#publisher'}, 'publisher': {'@id': SITE + '/#publisher'}, 'isBasedOn': original, 'citation': source['url'], 'keywords': article.get('tags', [])}
        if article.get('updated_at'):
            node['dateModified'] = article['updated_at']
        if image:
            node['image'] = [image]
        page['mainEntity'] = {'@id': url + '#article'}
        graph.append(node)
        tags.append(f'<meta property="article:published_time" content="{html.escape(article["date"], quote=True)}">')
    graph.append(page)
    data = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
    tags.append('<script type="application/ld+json">' + data + '</script>')
    return '\n'.join(tags)


def discovery_files(public, articles):
    urls = ['/', '/archive', '/about'] + ['/a/' + a['id'] for a in articles]
    # No lastmod from build time: rebuilding does not mean article content changed.
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap += '\n'.join('<url><loc>' + escape(SITE + u) + '</loc></url>' for u in urls) + '\n</urlset>\n'
    (public / 'sitemap.xml').write_text(sitemap, encoding='utf-8')
    (public / 'robots.txt').write_text('User-agent: *\nAllow: /\n\nSitemap: ' + SITE + '/sitemap.xml\n', encoding='utf-8')
    (public / '_headers').write_text('''/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
/static/*
  Cache-Control: public, max-age=31536000, immutable
/media/*
  Cache-Control: public, max-age=31536000, immutable
/a/*
  Cache-Control: public, max-age=300, stale-while-revalidate=3600
/
  Cache-Control: public, max-age=60, stale-while-revalidate=300
/archive
  Cache-Control: public, max-age=60, stale-while-revalidate=300
/feed.xml
  Cache-Control: public, max-age=300, stale-while-revalidate=600
/sitemap.xml
  Cache-Control: public, max-age=300
/robots.txt
  Cache-Control: public, max-age=300
/404
  X-Robots-Tag: noindex
''', encoding='utf-8')
