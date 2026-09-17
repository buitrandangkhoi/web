"""
Data Indexer for IELTS Web App, Pronunciation Suite & IELTS Mock Tests
Scans the data/ folder and generates a centralized manifest.json for frontend/backend consumption.
"""
import json
import datetime
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from pipeline.config import DATA_DIR, LISTENING_DIR, READING_DIR, WRITING_DIR, MANIFEST_FILE

PRONUNCIATION_DIR = DATA_DIR / "pronunciation"
US_DIR = PRONUNCIATION_DIR / "us"
IPA_CHART_DIR = PRONUNCIATION_DIR / "ipa_chart"
VOCAB_DIR = DATA_DIR / "vocabulary"
IELTS_TESTS_DIR = DATA_DIR / "ielts_tests"

def build_manifest():
    print("[Indexer] Scanning data directory to build manifest.json...")
    manifest = {
        "version": "1.3.0",
        "generated_at": datetime.datetime.now().isoformat(),
        "summary": {
            "listening_episodes": 0,
            "dictation_sentences": 0,
            "reading_passages": 0,
            "writing_prompts": 0,
            "oxford_3000_topics": 60,
            "oxford_3000_words": 1760,
            "ipa_chart_phonemes": 44,
            "ipa_chart_audio_files": 0,
            "us_ipa_total_vocabulary": 125927,
            "us_ipa_curated_words": 0,
            "us_audio_pronunciations": 0,
            "ielts_mock_tests_total": 0,
            "ielts_official_audio_tracks": 0,
            "ielts_official_pdfs": 0
        },
        "skills": {
            "listening": {
                "bbc_6minute": [],
                "dictation_pool": []
            },
            "reading": {
                "passages": []
            },
            "writing": {
                "task1": [],
                "task2": [],
                "phrasebank_categories": [],
                "band_descriptors_available": False
            },
            "vocabulary_oxford_3000": {
                "title": "3000 từ vựng tiếng Anh Oxford thông dụng theo chủ đề",
                "total_topics": 60,
                "total_words": 1760,
                "json_file": "vocabulary/3000_oxford_words_by_topic.json",
                "csv_file": "vocabulary/3000_oxford_words_by_topic.csv"
            },
            "ipa_chart_44": {
                "data_file": "pronunciation/ipa_chart/ipa_chart_44.json",
                "total_phonemes": 44,
                "monophthongs": 12,
                "diphthongs": 8,
                "consonants": 24,
                "sounds_directory": "pronunciation/ipa_chart/sounds/",
                "examples_directory": "pronunciation/ipa_chart/examples/"
            },
            "pronunciation_us": {
                "dialect": "General American (US)",
                "raw_dataset_file": "pronunciation/us/en_US_ipa.txt",
                "total_vocabulary_entries": 125927,
                "curated_academic_file": "pronunciation/us/ielts_academic_ipa.json",
                "phonemes_guide_file": "pronunciation/us/us_phonemes_guide.json",
                "audio_directory": "pronunciation/us/audio/",
                "curated_words": []
            },
            "ielts_mock_tests": {
                "official_idp_bc": {
                    "source": "IDP IELTS & British Council Official",
                    "catalog_file": "ielts_tests/official_idp_bc/idp_official_catalog.json",
                    "listening_audio": [],
                    "listening_pdfs": [],
                    "reading_pdfs": [],
                    "writing_pdfs": []
                },
                "ielts_online_tests": {
                    "source": "IELTS Online Tests (ieltsonlinetests.com)",
                    "listening_tests": [],
                    "reading_tests": []
                },
                "cambridge_study4": {
                    "source": "Cambridge IELTS / Study4 Equivalent",
                    "reading_tests": ["ielts_tests/cambridge_study4/reading/cam18_test1_reading.json"]
                }
            }
        }
    }

    # 1. Index Listening
    transcripts_dir = LISTENING_DIR / "bbc_6minute" / "transcripts"
    if transcripts_dir.exists():
        for json_file in sorted(transcripts_dir.glob("*.json")):
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    ep = json.load(f)
                    summary = ep.get("summary", "")
                    manifest["skills"]["listening"]["bbc_6minute"].append({
                        "id": ep.get("id"),
                        "title": ep.get("title"),
                        "level": ep.get("level"),
                        "audio_file": ep.get("audio_file"),
                        "summary": summary[:120] + "..." if len(summary) > 120 else summary,
                        "file_path": str(json_file.relative_to(DATA_DIR))
                    })
            except Exception as e:
                print(f"Error reading {json_file}: {e}")

    dictation_file = LISTENING_DIR / "dictation_sentences" / "dictation_pool.json"
    if dictation_file.exists():
        try:
            with open(dictation_file, "r", encoding="utf-8") as f:
                ddata = json.load(f)
                manifest["skills"]["listening"]["dictation_pool"] = ddata.get("sentences", [])
        except Exception as e:
            print(f"Error reading dictation pool: {e}")

    # 2. Index Reading
    passages_dir = READING_DIR / "academic_passages"
    if passages_dir.exists():
        for p_file in sorted(passages_dir.glob("passage_*.json")):
            try:
                with open(p_file, "r", encoding="utf-8") as f:
                    p = json.load(f)
                    manifest["skills"]["reading"]["passages"].append({
                        "id": p.get("id"),
                        "title": p.get("title"),
                        "source": p.get("source"),
                        "category": p.get("category"),
                        "word_count": p.get("word_count"),
                        "difficulty": p.get("difficulty"),
                        "questions_count": len(p.get("questions", [])),
                        "academic_vocab_count": len(p.get("academic_vocabulary", [])),
                        "file_path": str(p_file.relative_to(DATA_DIR))
                    })
            except Exception as e:
                print(f"Error reading {p_file}: {e}")

    # 3. Index Writing
    t1_file = WRITING_DIR / "task1" / "task1_bank.json"
    if t1_file.exists():
        try:
            with open(t1_file, "r", encoding="utf-8") as f:
                manifest["skills"]["writing"]["task1"] = json.load(f).get("prompts", [])
        except Exception as e:
            print(f"Error reading Task 1 bank: {e}")

    t2_file = WRITING_DIR / "task2" / "task2_bank.json"
    if t2_file.exists():
        try:
            with open(t2_file, "r", encoding="utf-8") as f:
                manifest["skills"]["writing"]["task2"] = json.load(f).get("prompts", [])
        except Exception as e:
            print(f"Error reading Task 2 bank: {e}")

    phrasebank_file = WRITING_DIR / "phrasebank" / "academic_phrasebank.json"
    if phrasebank_file.exists():
        try:
            with open(phrasebank_file, "r", encoding="utf-8") as f:
                pb = json.load(f)
                manifest["skills"]["writing"]["phrasebank_categories"] = list(pb.keys())
        except Exception as e:
            print(f"Error reading phrasebank: {e}")

    band_file = WRITING_DIR / "band_descriptors.json"
    manifest["skills"]["writing"]["band_descriptors_available"] = band_file.exists()

    # 4. Index Pronunciation (US IPA)
    curated_ipa_file = US_DIR / "ielts_academic_ipa.json"
    if curated_ipa_file.exists():
        try:
            with open(curated_ipa_file, "r", encoding="utf-8") as f:
                cdata = json.load(f)
                words = cdata.get("words", [])
                manifest["skills"]["pronunciation_us"]["curated_words"] = [
                    {"word": w["word"], "us_ipa": w["us_ipa"], "audio": w.get("audio_file", "")}
                    for w in words
                ]
                manifest["summary"]["us_ipa_curated_words"] = len(words)
        except Exception as e:
            print(f"Error reading curated IPA file: {e}")

    us_audio_dir = US_DIR / "audio"
    if us_audio_dir.exists():
        manifest["summary"]["us_audio_pronunciations"] = len(list(us_audio_dir.glob("*.mp3")))

    # 5. Index 44 IPA Chart Audio
    if IPA_CHART_DIR.exists():
        chart_sounds = list((IPA_CHART_DIR / "sounds").glob("*.mp3"))
        chart_examples = list((IPA_CHART_DIR / "examples").glob("*.mp3"))
        manifest["summary"]["ipa_chart_audio_files"] = len(chart_sounds) + len(chart_examples)

    # 6. Index IELTS Mock Tests
    idp_catalog_file = IELTS_TESTS_DIR / "official_idp_bc" / "idp_official_catalog.json"
    if idp_catalog_file.exists():
        try:
            with open(idp_catalog_file, "r", encoding="utf-8") as f:
                cat = json.load(f)
                manifest["skills"]["ielts_mock_tests"]["official_idp_bc"]["listening_audio"] = cat.get("listening", {}).get("audio", [])
                manifest["skills"]["ielts_mock_tests"]["official_idp_bc"]["listening_pdfs"] = cat.get("listening", {}).get("pdfs", [])
                manifest["skills"]["ielts_mock_tests"]["official_idp_bc"]["reading_pdfs"] = cat.get("reading", {}).get("pdfs", [])
                manifest["skills"]["ielts_mock_tests"]["official_idp_bc"]["writing_pdfs"] = cat.get("writing", {}).get("pdfs", [])
                
                manifest["summary"]["ielts_official_audio_tracks"] = len(manifest["skills"]["ielts_mock_tests"]["official_idp_bc"]["listening_audio"])
                manifest["summary"]["ielts_official_pdfs"] = (
                    len(manifest["skills"]["ielts_mock_tests"]["official_idp_bc"]["listening_pdfs"]) +
                    len(manifest["skills"]["ielts_mock_tests"]["official_idp_bc"]["reading_pdfs"]) +
                    len(manifest["skills"]["ielts_mock_tests"]["official_idp_bc"]["writing_pdfs"])
                )
        except Exception as e:
            print(f"Error reading IDP catalog: {e}")

    iot_lis_dir = IELTS_TESTS_DIR / "ielts_online_tests" / "listening" / "tests"
    if iot_lis_dir.exists():
        for jf in sorted(iot_lis_dir.glob("*.json")):
            try:
                with open(jf, "r", encoding="utf-8") as f:
                    manifest["skills"]["ielts_mock_tests"]["ielts_online_tests"]["listening_tests"].append(json.load(f))
            except Exception as e:
                print(f"Error reading IOT listening test: {e}")

    iot_read_dir = IELTS_TESTS_DIR / "ielts_online_tests" / "reading" / "tests"
    if iot_read_dir.exists():
        for jf in sorted(iot_read_dir.glob("*.json")):
            try:
                with open(jf, "r", encoding="utf-8") as f:
                    manifest["skills"]["ielts_mock_tests"]["ielts_online_tests"]["reading_tests"].append(json.load(f))
            except Exception as e:
                print(f"Error reading IOT reading test: {e}")

    manifest["summary"]["ielts_mock_tests_total"] = (
        len(manifest["skills"]["ielts_mock_tests"]["ielts_online_tests"]["listening_tests"]) +
        len(manifest["skills"]["ielts_mock_tests"]["ielts_online_tests"]["reading_tests"]) +
        len(manifest["skills"]["ielts_mock_tests"]["cambridge_study4"]["reading_tests"])
    )

    # 7. Index Comprehensive Grammar Suite
    grammar_dir = DATA_DIR / "grammar"
    if grammar_dir.exists():
        manifest["summary"]["grammar_sources"] = 4
        peg_pdf_dir = grammar_dir / "by_source" / "perfect_english_grammar" / "exercises_pdf"
        if peg_pdf_dir.exists():
            manifest["summary"]["grammar_exercise_pdfs"] = len(list(peg_pdf_dir.glob("*.pdf")))

        grammar_quiz_file = grammar_dir / "all_grammar_quizzes.json"
        if grammar_quiz_file.exists():
            try:
                with open(grammar_quiz_file, "r", encoding="utf-8") as qf:
                    manifest["summary"]["grammar_interactive_quizzes"] = json.load(qf).get("total_quizzes", 0)
            except Exception:
                pass

        manifest["skills"]["grammar"] = {
            "title": "Comprehensive English Grammar Knowledge Base",
            "manifest_file": "grammar/manifest.json",
            "quizzes_file": "grammar/all_grammar_quizzes.json",
            "sources": {
                "perfect_english_grammar": {
                    "rules_directory": "grammar/by_source/perfect_english_grammar/rules/",
                    "exercises_pdf_directory": "grammar/by_source/perfect_english_grammar/exercises_pdf/"
                },
                "englishclub": {
                    "parts_of_speech_directory": "grammar/by_source/englishclub/parts_of_speech/",
                    "sentence_structure_file": "grammar/by_source/englishclub/sentence_structure.json"
                },
                "english_grammar_org": {
                    "lessons_directory": "grammar/by_source/english_grammar_org/lessons/"
                },
                "british_council": {
                    "curriculum_file": "grammar/by_source/british_council/british_council_cefr_curriculum.json"
                }
            }
        }

    # Base summaries
    manifest["summary"]["listening_episodes"] = len(manifest["skills"]["listening"]["bbc_6minute"])
    manifest["summary"]["dictation_sentences"] = len(manifest["skills"]["listening"]["dictation_pool"])
    manifest["summary"]["reading_passages"] = len(manifest["skills"]["reading"]["passages"])
    manifest["summary"]["writing_prompts"] = len(manifest["skills"]["writing"]["task1"]) + len(manifest["skills"]["writing"]["task2"])

    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f"[Indexer] Manifest updated successfully at {MANIFEST_FILE}")
    print(f"  IELTS Official Audio Tracks: {manifest['summary']['ielts_official_audio_tracks']}")
    print(f"  IELTS Official PDFs: {manifest['summary']['ielts_official_pdfs']}")
    print(f"  IELTS Mock Tests Total: {manifest['summary']['ielts_mock_tests_total']}")
    print(f"  Grammar Exercise PDFs: {manifest['summary'].get('grammar_exercise_pdfs', 0)}")
    print(f"  Grammar Interactive Quizzes: {manifest['summary'].get('grammar_interactive_quizzes', 0)}")
    return manifest

if __name__ == "__main__":
    build_manifest()
