#!/usr/bin/env python3
"""
fetch_news.py — Crawl tin tức từ 3 API: Finnhub, GNews, NewsData.io
Chạy bởi GitHub Actions mỗi ngày lúc 07:00 giờ Việt Nam (00:00 UTC)
"""

import os
import json
import requests
from datetime import datetime, timezone

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
print("📡 Fetching Finnhub...")
for category in ["general", "forex", "merger"]:
    data = safe_get(
        "https://finnhub.io/api/v1/news",
        params={"category": category, "token": API_KEYS["finnhub"]},
        label=f"Finnhub/{category}",
    )
    if isinstance(data, list):
        for a in data[:10]:
            add({
                "title":     a.get("headline", "").strip(),
                "desc":      a.get("summary", "").strip()[:300],
                "url":       a.get("url", ""),
                "image":     a.get("image", ""),
                "source":    a.get("source", "Finnhub"),
                "cat":       "finance",
                "time":      datetime.fromtimestamp(
                                 a.get("datetime", 0), tz=timezone.utc
                             ).isoformat(),
                "sentiment": None,
            })


# ── 2. NewsData.io — Công nghệ & Doanh nghiệp ───────────────────────────────
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
        add({
            "title":     a.get("title", "").strip(),
            "desc":      (a.get("description") or "").strip()[:300],
            "url":       a.get("link", ""),
            "image":     (a.get("image_url") or ""),
            "source":    a.get("source_id", "NewsData.io"),
            "cat":       cat_ui,
            "time":      a.get("pubDate", ""),
            "sentiment": None,
        })


# ── 3. GNews — Chứng khoán, Công nghệ & Doanh nghiệp ───────────────────────
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
        add({
            "title":     a.get("title", "").strip(),
            "desc":      a.get("description", "").strip()[:300],
            "url":       a.get("url", ""),
            "image":     a.get("image", ""),
            "source":    (a.get("source") or {}).get("name", "GNews"),
            "cat":       cat_ui,
            "time":      a.get("publishedAt", ""),
            "sentiment": None,
        })


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

print(f"\n✅ Đã lưu {len(articles_clean)} bài vào data/news.json")
print(f"   Tài chính:    {sum(1 for a in articles_clean if a['cat']=='finance')}")
print(f"   Chứng khoán:  {sum(1 for a in articles_clean if a['cat']=='stock')}")
print(f"   Công nghệ:    {sum(1 for a in articles_clean if a['cat']=='tech')}")
print(f"   Doanh nghiệp: {sum(1 for a in articles_clean if a['cat']=='biz')}")
