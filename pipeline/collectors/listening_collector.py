"""
Listening Collector for IELTS Learning Web
Collects audio and transcripts from BBC 6 Minute English and builds an extensive dictation dataset.
"""
import os
import re
import json
import requests
import xml.etree.ElementTree as ET
from pathlib import Path
from pipeline.config import LISTENING_DIR, FEEDS, DEFAULT_HEADERS

AUDIO_DIR = LISTENING_DIR / "bbc_6minute" / "audio"
TRANSCRIPT_DIR = LISTENING_DIR / "bbc_6minute" / "transcripts"
DICTATION_DIR = LISTENING_DIR / "dictation_sentences"

def sanitize_filename(name: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9_-]", "_", name)
    return re.sub(r"_+", "_", s).strip("_")[:50]

def clean_html(raw_html: str) -> str:
    clean = re.sub(r"<[^>]+>", " ", raw_html)
    return " ".join(clean.split())

def fetch_bbc_episodes(limit: int = 8):
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    TRANSCRIPT_DIR.mkdir(parents=True, exist_ok=True)
    DICTATION_DIR.mkdir(parents=True, exist_ok=True)

    print(f"[Listening] Fetching RSS feed from {FEEDS['listening']['bbc_6min']}...")
    resp = requests.get(FEEDS['listening']['bbc_6min'], headers=DEFAULT_HEADERS, timeout=15)
    resp.raise_for_status()

    root = ET.fromstring(resp.content)
    items = root.findall(".//item")
    print(f"[Listening] Found {len(items)} episodes available. Processing {limit} episodes...")

    processed = []
    dictation_pool = []

    for i, item in enumerate(items[:limit]):
        title_el = item.find("title")
        title = title_el.text.strip() if title_el is not None else f"Episode_{i+1}"
        
        enclosure = item.find("enclosure")
        audio_url = enclosure.get("url") if enclosure is not None else None
        
        desc_el = item.find("description")
        desc = clean_html(desc_el.text) if (desc_el is not None and desc_el.text) else ""
        
        pub_el = item.find("pubDate")
        pub_date = pub_el.text.strip() if pub_el is not None else ""

        file_slug = f"{i+1:02d}_{sanitize_filename(title).lower()}"
        mp3_filename = f"{file_slug}.mp3"
        mp3_path = AUDIO_DIR / mp3_filename
        json_path = TRANSCRIPT_DIR / f"{file_slug}.json"

        # Download audio file if not exists
        if audio_url and not mp3_path.exists():
            print(f"  [Downloading Audio {i+1}/{limit}] {title} -> {mp3_filename}")
            try:
                with requests.get(audio_url, headers=DEFAULT_HEADERS, stream=True, timeout=30) as r:
                    r.raise_for_status()
                    with open(mp3_path, "wb") as f:
                        for chunk in r.iter_content(chunk_size=65536):
                            if chunk:
                                f.write(chunk)
                print(f"  [Done] Audio saved: {mp3_path.stat().st_size // 1024} KB")
            except Exception as e:
                print(f"  [Warning] Audio download failed: {e}")
        elif mp3_path.exists():
            print(f"  [Cached Audio] {mp3_filename} ({mp3_path.stat().st_size // 1024} KB)")

        # Parse sentences for dictation
        sentences = [s.strip() for s in re.split(r"[.?!]", desc) if len(s.strip()) >= 15]

        episode_data = {
            "id": f"lis_bbc_{i+1:03d}",
            "skill": "listening",
            "source": "BBC 6 Minute English",
            "title": title,
            "topic": "General / Science / Culture / Academic",
            "level": "Intermediate / Upper-Intermediate (B2-C1)",
            "publication_date": pub_date,
            "audio_file": f"listening/bbc_6minute/audio/{mp3_filename}",
            "audio_source_url": audio_url,
            "summary": desc,
            "learning_points": [
                "British English natural connected speech and intonation",
                "Advanced idiomatic phrases and topic collocations",
                "Accurate auditory comprehension for IELTS Section 3 & 4"
            ],
            "sample_sentences": sentences
        }

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(episode_data, f, ensure_ascii=False, indent=2)

        processed.append(episode_data)

        # Populate dictation pool with more sentences per episode
        for idx, sentence in enumerate(sentences[:6]):
            words = sentence.split()
            word_count = len(words)
            if word_count < 10:
                level = "Easy"
            elif word_count <= 22:
                level = "Medium"
            else:
                level = "Challenging"

            first_word = words[0] if words else ""
            last_word = words[-1] if words else ""

            dictation_pool.append({
                "id": f"dict_{i+1}_{idx+1}",
                "episode_id": episode_data["id"],
                "episode_title": title,
                "level": level,
                "text": sentence,
                "word_count": word_count,
                "hint": f"{first_word} ... {last_word}"
            })

    # Save dictation pool
    dictation_file = DICTATION_DIR / "dictation_pool.json"
    with open(dictation_file, "w", encoding="utf-8") as f:
        json.dump({
            "total_sentences": len(dictation_pool),
            "sentences": dictation_pool
        }, f, ensure_ascii=False, indent=2)

    print(f"[Listening] Completed: {len(processed)} episodes processed, {len(dictation_pool)} dictation sentences extracted.")
    return processed

if __name__ == "__main__":
    fetch_bbc_episodes(8)
