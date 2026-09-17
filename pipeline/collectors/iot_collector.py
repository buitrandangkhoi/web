"""
IELTS Online Tests (IOT) Collector
Extracts full 30-minute test audio (MP3), 3-passage Reading texts, and question banks
from ieltsonlinetests.com mock tests.
"""
import os
import re
import json
import requests
import bs4
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
IOT_DIR = BASE_DIR / "data" / "ielts_tests" / "ielts_online_tests"
LISTENING_AUDIO_DIR = IOT_DIR / "listening" / "audio"
LISTENING_TESTS_DIR = IOT_DIR / "listening" / "tests"
READING_TESTS_DIR = IOT_DIR / "reading" / "tests"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def sanitize_filename(name: str) -> str:
    name = re.sub(r"[^\w\s-]", "", name).strip()
    return re.sub(r"[-\s]+", "_", name).lower()

def download_file(url: str, dest: Path) -> bool:
    if dest.exists() and dest.stat().st_size > 10000:
        return True
    try:
        r = requests.get(url, headers=HEADERS, stream=True, timeout=40)
        r.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in r.iter_content(chunk_size=65536):
                if chunk:
                    f.write(chunk)
        print(f"  [Downloaded Audio] {dest.name} ({dest.stat().st_size // 1024} KB)")
        return True
    except Exception as e:
        print(f"  [Failed] {dest.name}: {e}")
        return False

def collect_iot_listening_test(test_slug: str, title: str):
    url = f"https://ieltsonlinetests.com/{test_slug}"
    print(f"[IOT Listening] Fetching {title} ({url})...")
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        soup = bs4.BeautifulSoup(r.content, "html.parser")
        
        # Find audio source
        audio_url = None
        for a in soup.find_all(["audio", "source"]):
            src = a.get("src") or a.get("data-src")
            if src and ".mp3" in src:
                audio_url = src
                break

        mp3_filename = f"{sanitize_filename(test_slug)}.mp3"
        local_audio_path = LISTENING_AUDIO_DIR / mp3_filename

        if audio_url:
            download_file(audio_url, local_audio_path)

        # Extract questions and directions
        inputs = soup.find_all(["input", "select"])
        paragraphs = [p.text.strip() for p in soup.find_all(["p", "div"]) if "Questions" in p.text and len(p.text.strip()) < 200]

        test_data = {
            "id": f"iot_lis_{sanitize_filename(test_slug)}",
            "title": title,
            "source": "IELTS Online Tests (ieltsonlinetests.com)",
            "test_type": "Listening (Computer-delivered format)",
            "audio_url": audio_url,
            "local_audio_file": f"ielts_tests/ielts_online_tests/listening/audio/{mp3_filename}" if local_audio_path.exists() else None,
            "duration_minutes": 30,
            "total_questions": len(inputs) if inputs else 40,
            "sections_guidance": list(set(paragraphs))[:4]
        }

        test_file = LISTENING_TESTS_DIR / f"{sanitize_filename(test_slug)}.json"
        with open(test_file, "w", encoding="utf-8") as f:
            json.dump(test_data, f, ensure_ascii=False, indent=2)

        print(f"  [Saved Listening Test] {test_file.name}")
        return test_data
    except Exception as e:
        print(f"  [Error] {e}")
        return None

def collect_iot_reading_test(test_slug: str, title: str):
    url = f"https://ieltsonlinetests.com/{test_slug}"
    print(f"[IOT Reading] Fetching {title} ({url})...")
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        soup = bs4.BeautifulSoup(r.content, "html.parser")

        # Extract passages
        raw_passages = soup.find_all("div", {"class": lambda c: c and "passage" in c.lower()})
        passages_data = []

        for idx, p in enumerate(raw_passages):
            txt = p.text.strip()
            if len(txt) > 300: # Genuine passage text
                first_line = txt.split("\n")[0][:80]
                passages_data.append({
                    "passage_number": len(passages_data) + 1,
                    "title": first_line,
                    "content": txt,
                    "word_count": len(txt.split())
                })

        test_data = {
            "id": f"iot_read_{sanitize_filename(test_slug)}",
            "title": title,
            "source": "IELTS Online Tests (ieltsonlinetests.com)",
            "test_type": "Academic Reading (3 Passages)",
            "total_passages": len(passages_data),
            "passages": passages_data
        }

        test_file = READING_TESTS_DIR / f"{sanitize_filename(test_slug)}.json"
        with open(test_file, "w", encoding="utf-8") as f:
            json.dump(test_data, f, ensure_ascii=False, indent=2)

        print(f"  [Saved Reading Test] {test_file.name} ({len(passages_data)} passages)")
        return test_data
    except Exception as e:
        print(f"  [Error] {e}")
        return None

def collect_iot_tests():
    LISTENING_AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    LISTENING_TESTS_DIR.mkdir(parents=True, exist_ok=True)
    READING_TESTS_DIR.mkdir(parents=True, exist_ok=True)

    print("[IOT Collector] Harvesting practice tests from IELTS Online Tests...")
    
    # Target representative tests from recent mock series
    listening_targets = [
        ("ielts-mock-test-2024-april-listening-practice-test-1", "IELTS Mock Test 2024 April - Listening Practice Test 1"),
        ("ielts-mock-test-2024-april-listening-practice-test-2", "IELTS Mock Test 2024 April - Listening Practice Test 2")
    ]

    reading_targets = [
        ("ielts-mock-test-2024-april-reading-practice-test-1", "IELTS Mock Test 2024 April - Reading Practice Test 1"),
        ("ielts-mock-test-2024-april-reading-practice-test-2", "IELTS Mock Test 2024 April - Reading Practice Test 2")
    ]

    results = {"listening": [], "reading": []}

    for slug, title in listening_targets:
        res = collect_iot_listening_test(slug, title)
        if res:
            results["listening"].append(res)

    for slug, title in reading_targets:
        res = collect_iot_reading_test(slug, title)
        if res:
            results["reading"].append(res)

    print(f"[IOT Collector] Done! Collected {len(results['listening'])} listening tests and {len(results['reading'])} reading tests.")
    return results

if __name__ == "__main__":
    collect_iot_tests()
