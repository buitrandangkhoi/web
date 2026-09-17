#!/usr/bin/env python3
"""
Download MP3 pronunciation for Oxford 3000 vocabulary words using gTTS.
Chạy: python3 download_vocab_audio.py

Yêu cầu: pip install gtts
"""

import json, os, time, re, sys
from pathlib import Path

# ── Cấu hình đường dẫn ──
BASE_DIR  = Path(__file__).parent  # thư mục chứa script này
JSON_IN   = BASE_DIR / "data" / "vocabulary" / "3000_oxford_words_by_topic.json"
JSON_OUT  = BASE_DIR / "data" / "vocabulary" / "3000_oxford_words_by_topic.json"  # ghi đè
AUDIO_DIR = BASE_DIR / "data" / "vocabulary" / "audio"

AUDIO_DIR.mkdir(parents=True, exist_ok=True)

# ── Kiểm tra gTTS ──
try:
    from gtts import gTTS
except ImportError:
    print("Cần cài gTTS: pip install gtts")
    sys.exit(1)

# ── Đọc JSON ──
if not JSON_IN.exists():
    print(f"Không tìm thấy file JSON: {JSON_IN}")
    sys.exit(1)

with open(JSON_IN, encoding="utf-8") as f:
    data = json.load(f)

# ── Chuẩn bị danh sách từ ──
def safe_filename(word_id, word):
    safe = re.sub(r"[^\w\s-]", "", word.lower())
    safe = re.sub(r"\s+", "_", safe.strip())
    return f"w{word_id:04d}_{safe}.mp3"

total = sum(t["words_count"] for t in data["topics"])
print(f"Tổng số từ: {total}")
print(f"Lưu audio vào: {AUDIO_DIR}")
print(f"Bắt đầu download...\n")

ok = skip = fail = 0
failed_words = []

for topic in data["topics"]:
    for w in topic["words"]:
        filename = safe_filename(w["id"], w["word"])
        dest = AUDIO_DIR / filename
        rel_path = f"data/vocabulary/audio/{filename}"
        w["audio_file"] = rel_path

        idx = w["id"]

        if dest.exists():
            skip += 1
            if idx % 200 == 0:
                print(f"[{idx}/{total}] Đã có: {w['word']}")
            continue

        try:
            tts = gTTS(text=w["word"], lang="en", tld="com", slow=False)
            tts.save(str(dest))
            ok += 1
            if ok % 50 == 0 or ok <= 3:
                print(f"[{idx}/{total}] ✓ {w['word']}")
            time.sleep(0.25)  # tránh bị rate limit

        except Exception as e:
            fail += 1
            failed_words.append(w["word"])
            print(f"[{idx}/{total}] ✗ {w['word']}: {e}", file=sys.stderr)
            time.sleep(1.5)

# ── Lưu JSON đã cập nhật ──
with open(JSON_OUT, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n{'='*50}")
print(f"✓ Thành công: {ok} | Đã có: {skip} | Lỗi: {fail}")
print(f"JSON đã cập nhật: {JSON_OUT}")
if failed_words:
    print(f"\nCác từ bị lỗi ({len(failed_words)}):")
    for w in failed_words[:20]:
        print(f"  - {w}")
print("\nXong! Bây giờ có thể Netlify Drop hoặc git push.")
