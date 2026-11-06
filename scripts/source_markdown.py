"""Render saved upstream Markdown, resolving links without changing source text."""
import re
from urllib.parse import urljoin, urlsplit

from markdown_it import MarkdownIt
import nh3

PARSER = MarkdownIt("commonmark", {"html": True}).enable("table")
TAGS = {
    "a", "p", "div", "span", "br", "hr", "h1", "h2", "h3", "h4", "h5", "h6",
    "strong", "em", "b", "i", "s", "del", "blockquote", "ul", "ol", "li",
    "pre", "code", "img", "picture", "source", "table", "thead", "tbody", "tr", "th", "td",
    "details", "summary", "kbd", "sup", "sub",
}


def render_source_markdown(text: str, base_url: str) -> str:
    if urlsplit(base_url).scheme != "https" or not urlsplit(base_url).netloc:
        raise ValueError("original.markdown_base_url must be an absolute HTTPS source document URL")
    # README images must resolve to file bytes, while relative document links
    # remain navigable GitHub pages at the exact recorded revision.
    image_base = re.sub(r"^https://github\.com/([^/]+/[^/]+)/blob/", r"https://raw.githubusercontent.com/\1/", base_url)

    def resolve(value, image=False):
        url = urljoin(image_base if image else base_url, value)
        return url if urlsplit(url).scheme in ("http", "https", "mailto") else None

    def attribute(tag, name, value):
        if name == "href":
            return resolve(value)
        if name == "src":
            url = resolve(value, image=True)
            return url if url and urlsplit(url).scheme in ("http", "https") else None
        if name == "srcset":
            # Source README uses a plain URL. Reject complex lists rather than
            # misparse comma-containing URLs or permit unchecked candidates.
            if re.search(r"[\s,]", value):
                return None
            url = resolve(value, image=True)
            return url if url and urlsplit(url).scheme in ("http", "https") else None
        return value

    return nh3.clean(
        PARSER.render(text), tags=TAGS,
        attributes={"a": {"href", "title"}, "img": {"src", "alt", "width", "height"},
                    "source": {"srcset", "media"}, "th": {"colspan", "rowspan"},
                    "td": {"colspan", "rowspan"}, "ol": {"start"}},
        attribute_filter=attribute, url_schemes={"http", "https", "mailto"},
        clean_content_tags={"script", "style", "iframe", "object", "template"},
        link_rel="noopener noreferrer",
    ).strip()
