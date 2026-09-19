#!/usr/bin/env python3
"""
fetch_news.py — Crawl tin tức từ 3 API: Finnhub, GNews, NewsData.io
               Lưu cả desc (tóm tắt) và content (nội dung đầy đủ từ API)
Chạy bởi GitHub Actions mỗi ngày lúc 07:00 giờ Việt Nam (00:00 UTC)
"""

import os
import re
import json
import urllib.request
import requests
from html.parser import HTMLParser
from datetime import datetime, timezone


class _TextExtractor(HTMLParser):
    """Pull readable text from an article page; skip nav/footer/scripts."""
    _SKIP = {'script', 'style', 'noscript', 'nav', 'header', 'footer', 'aside',
             'figure', 'figcaption', 'form', 'button', 'select', 'textarea'}

    def __init__(self):
        super().__init__()
        self.parts = []
        self._depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in self._SKIP:
            self._depth += 1

    def handle_endtag(self, tag):
        if tag in self._SKIP and self._depth > 0:
            self._depth -= 1

    def handle_data(self, data):
        if self._depth == 0:
            t = data.strip()
            if len(t) > 40:
                self.parts.append(t)


def scrape_article(url: str, timeout: int = 12) -> str:
    """Fetch an article URL and extract its main text. Returns '' on failure."""
    try:
        req = urllib.request.Request(
            url, headers={'User-Agent': 'Mozilla/5.0 (compatible; newsbot/1.0)'}
        )
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read(500_000).decode('utf-8', errors='replace')
        parser = _TextExtractor()
        parser.feed(raw)
        text = ' '.join(parser.parts)
        return re.sub(r'\s+', ' ', text).strip()[:4000]
    except Exception as exc:
        print(f"    scrape failed {url[:60]}: {exc}")
        return ''


def strip_html(text: str) -> str:
    """Xóa HTML tags, giữ khoảng trắng hợp lý giữa các phần tử."""
    if not text:
        return ""
    # Thêm space trước khi xóa block tags để các từ không dính nhau
    text = re.sub(r'</(p|li|div|h\d|br)[^>]*>', ' ', text, flags=re.IGNORECASE)
    text = re.sub(r'<br\s*/?>', ' ', text, flags=re.IGNORECASE)
    # Xóa mọi tag còn lại
    text = re.sub(r'<[^>]+>', '', text)
    # Decode HTML entities phổ biến
    text = (text
            .replace('&amp;', '&')
            .replace('&lt;', '<')
            .replace('&gt;', '>')
            .replace('&nbsp;', ' ')
            .replace('&#39;', "'")
            .replace('&quot;', '"')
            .replace('&ldquo;', '"')
            .replace('&rdquo;', '"')
            .replace('&lsquo;', "'")
            .replace('&rsquo;', "'")
            .replace('&mdash;', '—')
            .replace('&ndash;', '–'))
    # Chuẩn hóa whitespace
    return re.sub(r'\s+', ' ', text).strip()


# ── API keys từ GitHub Secrets ──────────────────────────────────────────────
API_KEYS = {
    "finnhub":  os.environ.get("FINNHUB_KEY", ""),
    "gnews":    os.environ.get("GNEWS_KEY", ""),
    "newsdata": os.environ.get("NEWSDATA_KEY", ""),
}

articles = []
seen_titles = set()


def add(article: dict):
    key = article.get("title", "").strip().lower()[:80]
    if key and key not in seen_titles and article.get("url"):
        seen_titles.add(key)
        articles.append(article)


def safe_get(url, params=None, headers=None, label=""):
    try:
        r = requests.get(url, params=params, headers=headers, timeout=15)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"  ⚠️  {label}: {e}")
        return {}


# ── 1. Finnhub — Tài chính & thị trường ─────────────────────────────────────
# Finnhub trả về summary khá đầy đủ (200-800 từ), dùng làm content
print("📡 Fetching Finnhub...")
for category in ["general", "forex", "merger"]:
    data = safe_get(
        "https://finnhub.io/api/v1/news",
        params={"category": category, "token": API_KEYS["finnhub"]},
        label=f"Finnhub/{category}",
    )
    if isinstance(data, list):
        for a in data[:10]:
            full_text = strip_html(a.get("summary", ""))
            add({
                "title":   a.get("headline", "").strip(),
                "desc":    full_text[:300],
                "content": full_text,          # dùng summary làm content đầy đủ
                "url":     a.get("url", ""),
                "image":   a.get("image", ""),
                "source":  a.get("source", "Finnhub"),
                "cat":     "finance",
                "time":    datetime.fromtimestamp(
                               a.get("datetime", 0), tz=timezone.utc
                           ).isoformat(),
                "sentiment": None,
            })


# ── 2. NewsData.io — Công nghệ & Doanh nghiệp ───────────────────────────────
# NewsData trả về cả description lẫn content (thường 300-800 ký tự)
print("📡 Fetching NewsData.io...")
for cat_api, cat_ui in [("technology", "tech"), ("business", "biz"), ("science", "tech")]:
    data = safe_get(
        "https://newsdata.io/api/1/news",
        params={
            "apikey":   API_KEYS["newsdata"],
            "category": cat_api,
            "language": "en",
            "size":     10,
        },
        label=f"NewsData/{cat_api}",
    )
    for a in (data.get("results") or []):
        desc_text    = strip_html(a.get("description") or "")
        content_text = strip_html(a.get("content") or a.get("full_description") or "")
        # Nếu content ngắn hơn desc, dùng desc làm content
        full_text = content_text if len(content_text) > len(desc_text) else desc_text
        add({
            "title":   a.get("title", "").strip(),
            "desc":    desc_text[:300],
            "content": full_text,
            "url":     a.get("link", ""),
            "image":   (a.get("image_url") or ""),
            "source":  a.get("source_id", "NewsData.io"),
            "cat":     cat_ui,
            "time":    a.get("pubDate", ""),
            "sentiment": None,
        })


# ── 3. GNews — Chứng khoán, Công nghệ & Doanh nghiệp ───────────────────────
# GNews có trường content (thường 500-1500 ký tự kể cả [+ N chars])
print("📡 Fetching GNews...")
for topic, cat_ui in [("business", "biz"), ("technology", "tech"), ("finance", "stock")]:
    data = safe_get(
        "https://gnews.io/api/v4/top-headlines",
        params={
            "token": API_KEYS["gnews"],
            "topic": topic,
            "lang":  "en",
            "max":   10,
        },
        label=f"GNews/{topic}",
    )
    for a in (data.get("articles") or []):
        desc_text = strip_html(a.get("description", ""))
        # GNews content thường có "[+NNN chars]" ở cuối — xóa đi
        raw_content = strip_html(a.get("content", ""))
        content_text = re.sub(r'\[\+\d+\s+chars?\].*$', '', raw_content).strip()
        full_text = content_text if len(content_text) > len(desc_text) else desc_text
        add({
            "title":   a.get("title", "").strip(),
            "desc":    desc_text[:300],
            "content": full_text,
            "url":     a.get("url", ""),
            "image":   a.get("image", ""),
            "source":  (a.get("source") or {}).get("name", "GNews"),
            "cat":     cat_ui,
            "time":    a.get("publishedAt", ""),
            "sentiment": None,
        })


# ── Scrape full content for articles that got nothing from APIs ───────────────
print("🔍 Scraping content for articles with missing/short content...")
scraped_count = 0
for a in articles:
    if len(a.get("content", "")) < 200 and a.get("url"):
        text = scrape_article(a["url"])
        if len(text) > 200:
            a["content"] = text
            scraped_count += 1
print(f"   Scraped {scraped_count} articles from source URLs")

# ── Lọc & sắp xếp ────────────────────────────────────────────────────────────
articles_clean = [
    a for a in articles
    if a.get("title") and len(a["title"]) > 10 and a.get("url")
]
articles_clean.sort(key=lambda a: a.get("time") or "", reverse=True)

# ── Ghi ra JSON ───────────────────────────────────────────────────────────────
output_path = os.path.join(os.path.dirname(__file__), "..", "data", "news.json")
output = {
    "updated":  datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "count":    len(articles_clean),
    "articles": articles_clean,
}
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

have_content = sum(1 for a in articles_clean if len(a.get("content","")) > 100)
print(f"\n✅ Đã lưu {len(articles_clean)} bài vào data/news.json")
print(f"   Có nội dung đầy đủ: {have_content}/{len(articles_clean)} bài")
print(f"   Tài chính:    {sum(1 for a in articles_clean if a['cat']=='finance')}")
print(f"   Chứng khoán:  {sum(1 for a in articles_clean if a['cat']=='stock')}")
print(f"   Công nghệ:    {sum(1 for a in articles_clean if a['cat']=='tech')}")
print(f"   Doanh nghiệp: {sum(1 for a in articles_clean if a['cat']=='biz')}")
