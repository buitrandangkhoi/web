"""
IDP Official IELTS Materials Collector
Downloads official sample tests, audio recordings, question papers, and answer keys
from ielts.idp.com (Co-owner of IELTS with British Council & Cambridge English).
"""
import os
import re
import json
import requests
import bs4
import urllib.parse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
IDP_DIR = BASE_DIR / "data" / "ielts_tests" / "official_idp_bc"
LISTENING_AUDIO_DIR = IDP_DIR / "listening" / "audio"
LISTENING_PDF_DIR = IDP_DIR / "listening" / "pdfs"
READING_PDF_DIR = IDP_DIR / "reading" / "pdfs"
WRITING_PDF_DIR = IDP_DIR / "writing" / "pdfs"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def sanitize_filename(name: str) -> str:
    name = re.sub(r"[^\w\s-]", "", name).strip()
    return re.sub(r"[-\s]+", "_", name)

def download_file(url: str, dest: Path) -> bool:
    if dest.exists() and dest.stat().st_size > 1000:
        return True
    try:
        r = requests.get(url, headers=HEADERS, stream=True, timeout=25)
        r.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in r.iter_content(chunk_size=65536):
                if chunk:
                    f.write(chunk)
        print(f"  [Saved] {dest.name} ({dest.stat().st_size // 1024} KB)")
        return True
    except Exception as e:
        print(f"  [Failed] {dest.name}: {e}")
        return False

def collect_idp_materials():
    LISTENING_AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    LISTENING_PDF_DIR.mkdir(parents=True, exist_ok=True)
    READING_PDF_DIR.mkdir(parents=True, exist_ok=True)
    WRITING_PDF_DIR.mkdir(parents=True, exist_ok=True)

    print("[IDP Collector] Scraping and downloading official IELTS materials from ielts.idp.com...")

    manifest_entries = {
        "listening": {"audio": [], "pdfs": []},
        "reading": {"pdfs": []},
        "writing": {"pdfs": []}
    }

    # 1. Listening Materials
    try:
        url = "https://ielts.idp.com/prepare/all-test-types/listening"
        r = requests.get(url, headers=HEADERS, timeout=15)
        soup = bs4.BeautifulSoup(r.content, "html.parser")
        
        # Audio links
        audios = set()
        pdfs = set()
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if ".mp3" in href:
                audios.add((href, a.text.strip() or Path(href.split("?")[0]).stem))
            elif ".pdf" in href:
                pdfs.add((href, a.text.strip() or Path(href.split("?")[0]).stem))

        print(f"[IDP Listening] Found {len(audios)} audio tracks and {len(pdfs)} PDFs.")
        for audio_url, label in audios:
            fname = sanitize_filename(label) + ".mp3"
            dest = LISTENING_AUDIO_DIR / fname
            if download_file(audio_url, dest):
                manifest_entries["listening"]["audio"].append({
                    "title": label,
                    "url": audio_url,
                    "local_path": f"ielts_tests/official_idp_bc/listening/audio/{fname}"
                })

        for pdf_url, label in pdfs:
            fname = sanitize_filename(label) + ".pdf"
            dest = LISTENING_PDF_DIR / fname
            if download_file(pdf_url, dest):
                manifest_entries["listening"]["pdfs"].append({
                    "title": label,
                    "url": pdf_url,
                    "local_path": f"ielts_tests/official_idp_bc/listening/pdfs/{fname}"
                })
    except Exception as e:
        print(f"[IDP Listening Error] {e}")

    # 2. Reading Materials
    try:
        url = "https://ielts.idp.com/prepare/all-test-types/reading"
        r = requests.get(url, headers=HEADERS, timeout=15)
        soup = bs4.BeautifulSoup(r.content, "html.parser")
        pdfs = set()
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if ".pdf" in href:
                pdfs.add((href, a.text.strip() or Path(href.split("?")[0]).stem))

        print(f"[IDP Reading] Found {len(pdfs)} official PDFs.")
        for pdf_url, label in pdfs:
            fname = sanitize_filename(label) + ".pdf"
            dest = READING_PDF_DIR / fname
            if download_file(pdf_url, dest):
                manifest_entries["reading"]["pdfs"].append({
                    "title": label,
                    "url": pdf_url,
                    "local_path": f"ielts_tests/official_idp_bc/reading/pdfs/{fname}"
                })
    except Exception as e:
        print(f"[IDP Reading Error] {e}")

    # 3. Writing Materials
    try:
        url = "https://ielts.idp.com/prepare/all-test-types/writing"
        r = requests.get(url, headers=HEADERS, timeout=15)
        soup = bs4.BeautifulSoup(r.content, "html.parser")
        pdfs = set()
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if ".pdf" in href:
                pdfs.add((href, a.text.strip() or Path(href.split("?")[0]).stem))

        print(f"[IDP Writing] Found {len(pdfs)} official PDFs.")
        for pdf_url, label in pdfs:
            fname = sanitize_filename(label) + ".pdf"
            dest = WRITING_PDF_DIR / fname
            if download_file(pdf_url, dest):
                manifest_entries["writing"]["pdfs"].append({
                    "title": label,
                    "url": pdf_url,
                    "local_path": f"ielts_tests/official_idp_bc/writing/pdfs/{fname}"
                })
    except Exception as e:
        print(f"[IDP Writing Error] {e}")

    # Save summary manifest
    meta_path = IDP_DIR / "idp_official_catalog.json"
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(manifest_entries, f, ensure_ascii=False, indent=2)

    print(f"[IDP Collector] Completed! Catalog saved at {meta_path}")
    return manifest_entries

if __name__ == "__main__":
    collect_idp_materials()
