"""
Main CLI for IELTS Data Pipeline & US IPA Pronunciation Suite
Usage:
    python3 data_pipeline.py --all
    python3 data_pipeline.py --skill listening --limit 5
    python3 data_pipeline.py --skill reading --limit 3
    python3 data_pipeline.py --skill writing
    python3 data_pipeline.py --skill pronunciation
    python3 data_pipeline.py --reindex
"""
import argparse
import sys
from pathlib import Path

# Ensure root directory is in sys.path
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from pipeline.collectors.listening_collector import fetch_bbc_episodes
from pipeline.collectors.reading_collector import fetch_reading_articles
from pipeline.collectors.writing_collector import fetch_writing_data
from pipeline.collectors.pronunciation_collector import run_pronunciation_pipeline
from pipeline.indexer import build_manifest

def main():
    parser = argparse.ArgumentParser(description='Automated IELTS Data Downloader & Manager')
    parser.add_argument('--all', action='store_true', help='Download and process data for all modules')
    parser.add_argument('--skill', choices=['listening', 'reading', 'writing', 'pronunciation'], help='Process a specific module')
    parser.add_argument('--limit', type=int, default=3, help='Limit the number of items fetched per source')
    parser.add_argument('--reindex', action='store_true', help='Rebuild data/manifest.json without downloading')

    args = parser.parse_args()

    if not any([args.all, args.skill, args.reindex]):
        print("No action specified. Running with --all --limit 3 by default.\n")
        args.all = True

    if args.reindex:
        build_manifest()
        return

    if args.all or args.skill == 'listening':
        print("\n=== [1/4] PROCESSING LISTENING DATA ===")
        fetch_bbc_episodes(limit=args.limit)

    if args.all or args.skill == 'reading':
        print("\n=== [2/4] PROCESSING READING DATA ===")
        fetch_reading_articles(limit_per_source=args.limit)

    if args.all or args.skill == 'writing':
        print("\n=== [3/4] PROCESSING WRITING DATA ===")
        fetch_writing_data()

    if args.all or args.skill == 'pronunciation':
        print("\n=== [4/4] PROCESSING US IPA PRONUNCIATION DATA ===")
        run_pronunciation_pipeline()

    print("\n=== BUILDING UNIFIED MANIFEST ===")
    build_manifest()
    print("\n>>> [SUCCESS] All requested data pipelines have finished successfully!")

if __name__ == '__main__':
    main()
