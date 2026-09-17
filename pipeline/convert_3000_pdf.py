"""
PDF to JSON / CSV Converter for 3000 Oxford Vocabulary by Topics
Scans 3000-tu-vung-tieng-anh-thong-dung-oxford-theo-chu-de.pdf,
extracts all 60 topics and vocabulary entries, cleans Vietnamese and IPA,
and exports to CSV and JSON formats.
"""
import os
import re
import csv
import json
import subprocess
from pathlib import Path
import fitz

BASE_DIR = Path(__file__).resolve().parent.parent
PDF_PATH = BASE_DIR / "3000-tu-vung-tieng-anh-thong-dung-oxford-theo-chu-de.pdf"
OUTPUT_DIR = BASE_DIR / "data" / "vocabulary"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CSV_FILE = OUTPUT_DIR / "3000_oxford_words_by_topic.csv"
JSON_FILE = OUTPUT_DIR / "3000_oxford_words_by_topic.json"
ROOT_CSV_FILE = BASE_DIR / "3000_oxford_words_by_topic.csv"
ROOT_JSON_FILE = BASE_DIR / "3000_oxford_words_by_topic.json"

# Load Vietnamese dictionary for word segmentation
vi_syllables = set()
hunspell_path = Path("/usr/share/hunspell/vi_VN.dic")
if hunspell_path.exists():
    with open(hunspell_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            w = line.strip().split("/")[0].lower()
            if w:
                vi_syllables.add(w)

def split_concatenated_vn(word: str) -> str:
    clean_w = word.strip(" ,;:.()[]{}\"'/-").lower()
    if not clean_w or clean_w in vi_syllables or len(clean_w) <= 2:
        return word

    for i in range(1, len(word)):
        left = word[:i]
        right = word[i:]
        if left.lower() in vi_syllables:
            if right.lower() in vi_syllables:
                return f"{left} {right}"
            for j in range(1, len(right)):
                mid = right[:j]
                last = right[j:]
                if mid.lower() in vi_syllables and last.lower() in vi_syllables:
                    return f"{left} {mid} {last}"
    return word

def clean_vietnamese_text(text: str) -> str:
    words = text.split()
    fixed_words = []
    for w in words:
        m = re.match(r"^([^a-zA-Zà-ỹÀ-Ỹ]*)([a-zA-Zà-ỹÀ-Ỹ]+)([^a-zA-Zà-ỹÀ-Ỹ]*)$", w)
        if m:
            pre, core, post = m.groups()
            fixed_core = split_concatenated_vn(core)
            fixed_words.append(f"{pre}{fixed_core}{post}")
        else:
            fixed_words.append(split_concatenated_vn(w))
    res = " ".join(" ".join(fixed_words).split())
    # Fix spacing around punctuation
    res = re.sub(r"\s+([,;.!?])", r"\1", res)
    return res

def fix_ipa(ipa: str) -> str:
    ipa = " ".join(ipa.split()).strip()
    if re.search(r"/\s*ˌ$", ipa) or ipa.endswith("ˌ"):
        clean = re.sub(r"/\s*ˌ$", "", ipa).strip(" /ˌ")
        parts = clean.split(" ")
        if len(parts) >= 2:
            ipa = f"/{parts[0]} ˌ{' '.join(parts[1:])}/"
        else:
            ipa = f"/ˌ{clean}/"
    elif re.search(r"^ˌ\s*/", ipa) or ipa.startswith("ˌ"):
        clean = re.sub(r"^ˌ\s*/", "", ipa).strip(" /ˌ")
        ipa = f"/ˌ{clean}/"
    return ipa

def extract_official_topics_from_toc() -> dict:
    """Extract standard topic names from Table of Contents on pages 2-3"""
    try:
        cmd = ["pdftotext", "-f", "2", "-l", "3", "-layout", str(PDF_PATH), "-"]
        toc_text = subprocess.check_output(cmd).decode("utf-8")
        topics_map = {}
        for line in toc_text.split("\n"):
            m = re.match(r"^(\d+)\.\s*(Từ vựng[^\.]+)", line.strip())
            if m:
                tid = int(m.group(1))
                tname = m.group(2).strip()
                topics_map[tid] = tname
        if len(topics_map) >= 50:
            return topics_map
    except Exception as e:
        print(f"[Warning] Failed extracting TOC via pdftotext: {e}")
    return {}

def convert_pdf():
    print(f"[Converter] Opening PDF: {PDF_PATH}...")
    doc = fitz.open(str(PDF_PATH))
    print(f"[Converter] Document contains {len(doc)} pages.")

    official_topics = extract_official_topics_from_toc()
    print(f"[Converter] Loaded {len(official_topics)} official topic titles from Table of Contents.")

    all_entries = []
    topics_catalog = {}
    current_topic_id = 1

    # Initialize catalog with official topics
    for tid, tname in official_topics.items():
        topics_catalog[tid] = {
            "topic_id": tid,
            "topic_name": tname,
            "words_count": 0,
            "words": []
        }

    for pno in range(3, len(doc)):
        page = doc[pno]
        text = page.get_text()

        # Check for topic heading (e.g. '1. Từ vựng về đồ dùng học tập')
        heading_match = re.search(r"(\d+)\.\s*Từ\s*vựng[^\n]+", text)
        if heading_match:
            current_topic_id = int(heading_match.group(1))
            if current_topic_id not in topics_catalog:
                raw_heading = heading_match.group(0).strip()
                tname = clean_vietnamese_text(re.sub(r"^\d+\.\s*", "", raw_heading))
                topics_catalog[current_topic_id] = {
                    "topic_id": current_topic_id,
                    "topic_name": tname,
                    "words_count": 0,
                    "words": []
                }

        topic_name = topics_catalog.get(current_topic_id, {}).get("topic_name", f"Chủ đề {current_topic_id}")

        tabs = page.find_tables()
        for tab in tabs.tables:
            for row in tab.extract():
                if not row or len(row) < 4:
                    continue
                w, pos, ipa, meaning = [c.strip() if c else "" for c in row[:4]]
                if not w or w.lower() in ["từ vựng", "từvựng", "word"]:
                    continue

                w_clean = " ".join(w.split())
                pos_clean = " ".join(pos.split())
                ipa_clean = fix_ipa(ipa)
                meaning_clean = clean_vietnamese_text(" ".join(meaning.split()))

                entry = {
                    "id": len(all_entries) + 1,
                    "topic_id": current_topic_id,
                    "topic": topic_name,
                    "word": w_clean,
                    "pos": pos_clean,
                    "ipa": ipa_clean,
                    "meaning": meaning_clean
                }

                all_entries.append(entry)
                
                if current_topic_id in topics_catalog:
                    topics_catalog[current_topic_id]["words_count"] += 1
                    topics_catalog[current_topic_id]["words"].append(entry)

    print(f"[Converter] Successfully extracted {len(all_entries)} vocabulary entries across {len(topics_catalog)} topics.")

    # 1. Export to CSV
    print(f"[Converter] Writing CSV...")
    fieldnames = ["id", "topic_id", "topic", "word", "pos", "ipa", "meaning"]
    for dest_csv in [CSV_FILE, ROOT_CSV_FILE]:
        with open(dest_csv, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for entry in all_entries:
                writer.writerow(entry)

    # 2. Export to JSON
    print(f"[Converter] Writing JSON...")
    json_payload = {
        "title": "3000 từ vựng tiếng Anh Oxford thông dụng theo chủ đề",
        "total_topics": len(topics_catalog),
        "total_words": len(all_entries),
        "topics": list(topics_catalog.values()),
        "all_words": all_entries
    }
    for dest_json in [JSON_FILE, ROOT_JSON_FILE]:
        with open(dest_json, "w", encoding="utf-8") as f:
            json.dump(json_payload, f, ensure_ascii=False, indent=2)

    print(f"[Converter] Files created successfully:")
    print(f"  - CSV: {CSV_FILE} ({CSV_FILE.stat().st_size // 1024} KB)")
    print(f"  - JSON: {JSON_FILE} ({JSON_FILE.stat().st_size // 1024} KB)")
    print(f"  - Root CSV: {ROOT_CSV_FILE}")
    print(f"  - Root JSON: {ROOT_JSON_FILE}")

    return json_payload

if __name__ == "__main__":
    convert_pdf()
