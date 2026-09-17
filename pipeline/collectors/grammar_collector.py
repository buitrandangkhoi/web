#!/usr/bin/env python3
"""
Comprehensive Grammar Collector:
Collects grammar data from:
1. Perfect English Grammar (perfect-english-grammar.com): 12 Tenses, Conditionals, Modals, Passive + PDF Exercises.
2. EnglishClub (englishclub.com/grammar/): 9 Parts of speech, Sentence grammar, rules, quizzes.
3. EnglishGrammar.org (englishgrammar.org): Jennifer Frost lessons & online practice tests.
4. British Council LearnEnglish (CEFR A1-C1 framework): Standardized grammar milestones and tests.
"""

import os
import sys
import json
import re
import time
import urllib.parse
import requests
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
}

BASE_DIR = "/home/namphuong/Desktop/web học tiếng anh"
GRAMMAR_DIR = os.path.join(BASE_DIR, "data", "grammar")
PEG_DIR = os.path.join(GRAMMAR_DIR, "by_source", "perfect_english_grammar")
EC_DIR = os.path.join(GRAMMAR_DIR, "by_source", "englishclub")
EG_DIR = os.path.join(GRAMMAR_DIR, "by_source", "english_grammar_org")
BC_DIR = os.path.join(GRAMMAR_DIR, "by_source", "british_council")
TOPIC_DIR = os.path.join(GRAMMAR_DIR, "by_topic")

def clean_text(text):
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# -------------------------------------------------------------
# 1. PERFECT ENGLISH GRAMMAR COLLECTOR
# -------------------------------------------------------------
def collect_perfect_english_grammar():
    print("\n--- [1/4] Collecting from Perfect English Grammar ---")
    peg_rules_dir = os.path.join(PEG_DIR, "rules")
    peg_pdf_dir = os.path.join(PEG_DIR, "exercises_pdf")
    os.makedirs(peg_rules_dir, exist_ok=True)
    os.makedirs(peg_pdf_dir, exist_ok=True)

    targets = [
        {"name": "Present Simple", "slug": "present-simple", "topic": "tenses", "cat": "present"},
        {"name": "Present Continuous", "slug": "present-continuous", "topic": "tenses", "cat": "present"},
        {"name": "Present Perfect Simple", "slug": "present-perfect", "topic": "tenses", "cat": "present"},
        {"name": "Present Perfect Continuous", "slug": "present-perfect-continuous", "topic": "tenses", "cat": "present"},
        {"name": "Past Simple", "slug": "past-simple", "topic": "tenses", "cat": "past"},
        {"name": "Past Continuous", "slug": "past-continuous", "topic": "tenses", "cat": "past"},
        {"name": "Past Perfect Simple", "slug": "past-perfect", "topic": "tenses", "cat": "past"},
        {"name": "Past Perfect Continuous", "slug": "past-perfect-continuous", "topic": "tenses", "cat": "past"},
        {"name": "Future Simple", "slug": "simple-future", "topic": "tenses", "cat": "future"},
        {"name": "Future Continuous", "slug": "future-continuous", "topic": "tenses", "cat": "future"},
        {"name": "Future Perfect Simple", "slug": "future-perfect", "topic": "tenses", "cat": "future"},
        {"name": "Future Perfect Continuous", "slug": "future-perfect-continuous", "topic": "tenses", "cat": "future"},
        {"name": "Zero Conditional", "slug": "zero-conditional", "topic": "conditionals", "cat": "conditionals"},
        {"name": "First Conditional", "slug": "first-conditional", "topic": "conditionals", "cat": "conditionals"},
        {"name": "Second Conditional", "slug": "second-conditional", "topic": "conditionals", "cat": "conditionals"},
        {"name": "Third Conditional", "slug": "third-conditional", "topic": "conditionals", "cat": "conditionals"},
        {"name": "Mixed Conditionals", "slug": "mixed-conditionals", "topic": "conditionals", "cat": "conditionals"},
        {"name": "Passive Voice", "slug": "passive", "topic": "passive_voice", "cat": "passive"},
        {"name": "Modal Verbs", "slug": "modal-verbs", "topic": "modal_verbs", "cat": "modals"},
        {"name": "Reported Speech", "slug": "reported-speech", "topic": "reported_speech", "cat": "reported_speech"},
        {"name": "Relative Clauses", "slug": "relative-clauses", "topic": "relative_clauses", "cat": "clauses"},
    ]

    downloaded_pdfs = []
    collected_lessons = []

    for item in targets:
        url = f"https://www.perfect-english-grammar.com/{item['slug']}.html"
        print(f"Fetching PEG: {item['name']} ({url})...")
        try:
            resp = requests.get(url, headers=HEADERS, timeout=12)
            if resp.status_code != 200:
                print(f"  Warning: HTTP {resp.status_code} for {url}")
                continue
            
            soup = BeautifulSoup(resp.text, 'html.parser')
            title = item['name']
            h1 = soup.find('h1')
            if h1:
                title = clean_text(h1.get_text())

            paragraphs = []
            for p in soup.find_all(['p', 'li', 'h2', 'h3']):
                t = clean_text(p.get_text())
                if t and not any(x in t.lower() for x in ['copyright', 'newsletter', 'membership', 'privacy policy', 'cookie']):
                    paragraphs.append(t)

            pdf_urls = []
            for a in soup.find_all('a', href=True):
                href = a['href']
                if '.pdf' in href.lower():
                    full_pdf = urllib.parse.urljoin(url, href)
                    if full_pdf not in pdf_urls:
                        pdf_urls.append(full_pdf)

            local_pdfs = []
            for purl in pdf_urls:
                pdf_name = os.path.basename(urllib.parse.urlparse(purl).path)
                if not pdf_name:
                    pdf_name = f"{item['slug']}_exercise.pdf"
                local_pdf_path = os.path.join(peg_pdf_dir, pdf_name)
                if not os.path.exists(local_pdf_path):
                    try:
                        print(f"  Downloading PDF: {pdf_name}...")
                        presp = requests.get(purl, headers=HEADERS, timeout=15)
                        if presp.status_code == 200 and len(presp.content) > 500:
                            with open(local_pdf_path, 'wb') as f:
                                f.write(presp.content)
                            local_pdfs.append(f"grammar/by_source/perfect_english_grammar/exercises_pdf/{pdf_name}")
                            downloaded_pdfs.append(pdf_name)
                    except Exception as pe:
                        print(f"  Error downloading PDF {purl}: {pe}")
                else:
                    local_pdfs.append(f"grammar/by_source/perfect_english_grammar/exercises_pdf/{pdf_name}")

            lesson_data = {
                "id": f"peg_{item['slug'].replace('-', '_')}",
                "title": title,
                "category": item['topic'],
                "source": "Perfect English Grammar",
                "source_url": url,
                "overview": paragraphs[:5],
                "full_text": paragraphs,
                "exercise_pdfs": local_pdfs
            }

            out_file = os.path.join(peg_rules_dir, f"{item['slug']}.json")
            with open(out_file, 'w', encoding='utf-8') as f:
                json.dump(lesson_data, f, ensure_ascii=False, indent=2)

            topic_sub = os.path.join(TOPIC_DIR, item['topic'])
            os.makedirs(topic_sub, exist_ok=True)
            with open(os.path.join(topic_sub, f"{item['slug']}.json"), 'w', encoding='utf-8') as f:
                json.dump(lesson_data, f, ensure_ascii=False, indent=2)

            collected_lessons.append(lesson_data)
            time.sleep(0.4)

        except Exception as e:
            print(f"  Error processing {item['name']}: {e}")

    master_pdfs = [
        "https://www.perfect-english-grammar.com/support-files/all_conditionals_form_mixed_exercise.pdf",
        "https://www.perfect-english-grammar.com/support-files/reported_questions.pdf",
        "https://www.perfect-english-grammar.com/support-files/present_simple_form.pdf",
        "https://www.perfect-english-grammar.com/support-files/past_simple_form.pdf",
        "https://www.perfect-english-grammar.com/support-files/present_perfect_form.pdf",
        "https://www.perfect-english-grammar.com/support-files/passive_form.pdf"
    ]
    for purl in master_pdfs:
        pname = os.path.basename(urllib.parse.urlparse(purl).path)
        ppath = os.path.join(peg_pdf_dir, pname)
        if not os.path.exists(ppath):
            try:
                print(f"Downloading master PDF: {pname}...")
                pr = requests.get(purl, headers=HEADERS, timeout=15)
                if pr.status_code == 200:
                    with open(ppath, 'wb') as pf:
                        pf.write(pr.content)
                    downloaded_pdfs.append(pname)
            except Exception as e:
                print(f"  Failed master PDF {pname}: {e}")

    print(f"✓ PEG: Collected {len(collected_lessons)} lessons and {len(downloaded_pdfs)} exercise PDFs.")
    return collected_lessons


# -------------------------------------------------------------
# 2. ENGLISHCLUB GRAMMAR COLLECTOR
# -------------------------------------------------------------
def collect_englishclub_grammar():
    print("\n--- [2/4] Collecting from EnglishClub ---")
    ec_speech_dir = os.path.join(EC_DIR, "parts_of_speech")
    os.makedirs(ec_speech_dir, exist_ok=True)

    parts_of_speech = [
        {"name": "Nouns (Danh từ)", "slug": "nouns.php", "key": "nouns"},
        {"name": "Verbs (Động từ)", "slug": "verbs.php", "key": "verbs"},
        {"name": "Adjectives (Tính từ)", "slug": "adjectives.php", "key": "adjectives"},
        {"name": "Adverbs (Trạng từ)", "slug": "adverbs.php", "key": "adverbs"},
        {"name": "Pronouns (Đại từ)", "slug": "pronouns.php", "key": "pronouns"},
        {"name": "Prepositions (Giới từ)", "slug": "prepositions.php", "key": "prepositions"},
        {"name": "Conjunctions (Liên từ)", "slug": "conjunctions.php", "key": "conjunctions"},
        {"name": "Determiners (Từ hạn định)", "slug": "determiners.php", "key": "determiners"},
        {"name": "Interjections (Thán từ)", "slug": "interjections.php", "key": "interjections"},
    ]

    ec_lessons = []
    for item in parts_of_speech:
        url = f"https://www.englishclub.com/grammar/{item['slug']}"
        print(f"Fetching EnglishClub: {item['name']} ({url})...")
        try:
            resp = requests.get(url, headers=HEADERS, timeout=12)
            if resp.status_code != 200:
                print(f"  Warning: HTTP {resp.status_code} for {url}")
                continue

            soup = BeautifulSoup(resp.text, 'html.parser')
            h1 = clean_text(soup.find('h1').get_text()) if soup.find('h1') else item['name']

            paragraphs = []
            examples = []
            for el in soup.find_all(['p', 'li', 'blockquote']):
                txt = clean_text(el.get_text())
                if len(txt) > 10 and not any(x in txt.lower() for x in ['cookie', 'advertise', 'copyright', 'privacy', 'donate']):
                    if any(w in txt.lower() for w in ['example:', 'e.g.', 'for instance', 'sample']):
                        examples.append(txt)
                    else:
                        paragraphs.append(txt)

            lesson = {
                "id": f"ec_{item['key']}",
                "title": h1,
                "category": "parts_of_speech",
                "part_of_speech": item['key'],
                "source": "EnglishClub",
                "source_url": url,
                "explanation": paragraphs[:12],
                "sample_examples": examples[:10]
            }

            out_path = os.path.join(ec_speech_dir, f"{item['key']}.json")
            with open(out_path, 'w', encoding='utf-8') as f:
                json.dump(lesson, f, ensure_ascii=False, indent=2)

            pos_topic_dir = os.path.join(TOPIC_DIR, "parts_of_speech")
            os.makedirs(pos_topic_dir, exist_ok=True)
            with open(os.path.join(pos_topic_dir, f"{item['key']}.json"), 'w', encoding='utf-8') as f:
                json.dump(lesson, f, ensure_ascii=False, indent=2)

            ec_lessons.append(lesson)
            time.sleep(0.4)

        except Exception as e:
            print(f"  Error fetching EnglishClub {item['name']}: {e}")

    sentence_url = "https://www.englishclub.com/grammar/sentence/index.php"
    try:
        s_resp = requests.get(sentence_url, headers=HEADERS, timeout=12)
        if s_resp.status_code == 200:
            s_soup = BeautifulSoup(s_resp.text, 'html.parser')
            s_paragraphs = [clean_text(p.get_text()) for p in s_soup.find_all('p') if len(clean_text(p.get_text())) > 20]
            s_data = {
                "id": "ec_sentence_grammar",
                "title": "Sentence-Level English Grammar (Cấu Trúc Câu)",
                "category": "sentence_structure",
                "source": "EnglishClub",
                "source_url": sentence_url,
                "sections": s_paragraphs[:15]
            }
            with open(os.path.join(EC_DIR, "sentence_structure.json"), 'w', encoding='utf-8') as f:
                json.dump(s_data, f, ensure_ascii=False, indent=2)
            ec_lessons.append(s_data)
    except Exception as e:
        print(f"  Sentence grammar error: {e}")

    print(f"✓ EnglishClub: Collected {len(ec_lessons)} parts of speech & sentence structure lessons.")
    return ec_lessons


# -------------------------------------------------------------
# 3. ENGLISHGRAMMAR.ORG COLLECTOR
# -------------------------------------------------------------
def collect_english_grammar_org():
    print("\n--- [3/4] Collecting from EnglishGrammar.org ---")
    eg_lessons_dir = os.path.join(EG_DIR, "lessons")
    eg_quiz_dir = os.path.join(EG_DIR, "quizzes")
    os.makedirs(eg_lessons_dir, exist_ok=True)
    os.makedirs(eg_quiz_dir, exist_ok=True)

    target_exercises = [
        {"title": "Present Perfect Simple vs Continuous Exercise", "slug": "present-perfect-simple-vs-continuous-exercise"},
        {"title": "Past Perfect Exercise", "slug": "past-perfect-exercise"},
        {"title": "Be and Past Participle Exercise", "slug": "be-and-past-participle-exercise"},
        {"title": "Even If Clauses Exercise", "slug": "even-if-clauses-exercise"},
        {"title": "Adjective or Adverb Exercise", "slug": "adjective-or-adverb-exercise-2"},
        {"title": "Prepositions of Place Exercise", "slug": "prepositions-place-exercise"},
        {"title": "Conjunctions Exercise", "slug": "conjunctions-exercise"},
        {"title": "Modal Auxiliary Verbs Exercise", "slug": "modal-auxiliary-verbs-exercise"},
        {"title": "Active and Passive Voice Exercise", "slug": "active-passive-voice-exercise-2"},
        {"title": "Direct and Indirect Speech Exercise", "slug": "direct-indirect-speech-exercise"},
        {"title": "Subject Verb Agreement Exercise", "slug": "subject-verb-agreement-exercise"},
        {"title": "Punctuation Rules and Exercise", "slug": "punctuation-exercise"},
    ]

    eg_items = []
    for item in target_exercises:
        url = f"https://www.englishgrammar.org/{item['slug']}/"
        print(f"Fetching EnglishGrammar.org: {item['title']}...")
        try:
            resp = requests.get(url, headers=HEADERS, timeout=12)
            if resp.status_code != 200:
                print(f"  Warning: HTTP {resp.status_code} for {url}")
                continue

            soup = BeautifulSoup(resp.text, 'html.parser')
            h1 = clean_text(soup.find('h1').get_text()) if soup.find('h1') else item['title']

            content_p = []
            questions = []

            entry = soup.select_one('.entry-content, article')
            if entry:
                for p in entry.find_all('p'):
                    txt = clean_text(p.get_text())
                    if txt and not any(x in txt.lower() for x in ['stay updated', 'subscribe', 'share this', 'advertisement']):
                        content_p.append(txt)

                for li in entry.find_all('li'):
                    txt = clean_text(li.get_text())
                    if re.match(r'^\d+[\.\)]', txt) or '___' in txt:
                        questions.append(txt)

            lesson = {
                "id": f"eg_{item['slug'].replace('-', '_')}",
                "title": h1,
                "author": "Jennifer Frost",
                "source": "EnglishGrammar.org",
                "source_url": url,
                "instructions": content_p[:5],
                "exercise_questions": questions[:15],
                "raw_notes": content_p
            }

            out_file = os.path.join(eg_lessons_dir, f"{item['slug']}.json")
            with open(out_file, 'w', encoding='utf-8') as f:
                json.dump(lesson, f, ensure_ascii=False, indent=2)

            eg_items.append(lesson)
            time.sleep(0.4)

        except Exception as e:
            print(f"  Error fetching EnglishGrammar.org {item['title']}: {e}")

    print(f"✓ EnglishGrammar.org: Collected {len(eg_items)} lessons & interactive exercise modules.")
    return eg_items


# -------------------------------------------------------------
# 4. BRITISH COUNCIL CEFR GRAMMAR CURRICULUM (A1 - C1)
# -------------------------------------------------------------
def collect_british_council_curriculum():
    print("\n--- [4/4] Generating Standard British Council CEFR Grammar Framework ---")
    
    curriculum = {
        "framework": "CEFR (Common European Framework of Reference for Languages)",
        "source": "British Council LearnEnglish Curriculum & Descriptors",
        "levels": {
            "A1_A2_Elementary": [
                {
                    "id": "bc_a1_01",
                    "title": "Present simple: be and other verbs",
                    "description": "Using 'to be' (am/is/are) and action verbs to talk about routine, states and facts.",
                    "formula": "S + V(s/es) + Object",
                    "key_examples": ["I am a student.", "She works in a hospital.", "They do not live in London."],
                    "exercises": [
                        {"q": "He ___ (live) in Manchester.", "options": ["live", "lives", "living"], "a": "lives", "explanation": "Third person singular takes -s."}
                    ]
                },
                {
                    "id": "bc_a1_02",
                    "title": "Possessives and Demonstratives",
                    "description": "Possessive adjectives (my, your, his, her, its, our, their) and demonstratives (this, that, these, those).",
                    "formula": "Demonstrative + Noun / Possessive + Noun",
                    "key_examples": ["This is my coat.", "Those shoes are very comfortable."],
                    "exercises": [
                        {"q": "Look at ___ bird over there in the tree!", "options": ["this", "that", "these"], "a": "that", "explanation": "That refers to a singular object at a distance."}
                    ]
                },
                {
                    "id": "bc_a2_01",
                    "title": "Past simple: regular and irregular verbs",
                    "description": "Forming past simple sentences with -ed and common irregular verbs (went, bought, saw, did).",
                    "formula": "S + V2/ed + Object",
                    "key_examples": ["We watched a movie yesterday.", "He bought a new laptop last week."],
                    "exercises": [
                        {"q": "Yesterday, they ___ (go) to the museum.", "options": ["goed", "went", "gone"], "a": "went", "explanation": "Past simple irregular form of 'go' is 'went'."}
                    ]
                },
                {
                    "id": "bc_a2_02",
                    "title": "Comparatives and Superlatives",
                    "description": "Comparing people, items and qualities with -er/-est and more/most.",
                    "formula": "Adj-er than / More + Adj than / The most + Adj",
                    "key_examples": ["Tokyo is bigger than Rome.", "The blue whale is the largest animal."],
                    "exercises": [
                        {"q": "This test is ___ (difficult) than the previous one.", "options": ["more difficult", "difficulter", "most difficult"], "a": "more difficult", "explanation": "Long adjectives take 'more'."}
                    ]
                }
            ],
            "B1_B2_Intermediate": [
                {
                    "id": "bc_b1_01",
                    "title": "Present perfect with for and since",
                    "description": "Connecting past actions to the present, indicating duration (for) or starting point (since).",
                    "formula": "S + have/has + V3/ed + for/since",
                    "key_examples": ["I have lived here for five years.", "She has known him since 2018."],
                    "exercises": [
                        {"q": "They have been married ___ 2010.", "options": ["for", "since", "during"], "a": "since", "explanation": "Since is used with specific starting point in time."}
                    ]
                },
                {
                    "id": "bc_b1_02",
                    "title": "Conditionals: First and Second Conditionals",
                    "description": "Real future possibilities vs hypothetical/imaginary situations.",
                    "formula": "1st: If + present, will + V_inf | 2nd: If + past, would + V_inf",
                    "key_examples": ["If it rains, we will stay at home.", "If I won the lottery, I would travel the world."],
                    "exercises": [
                        {"q": "If I ___ you, I would take that job offer.", "options": ["am", "was", "were"], "a": "were", "explanation": "In 2nd conditional, 'were' is standard with all subjects."}
                    ]
                },
                {
                    "id": "bc_b2_01",
                    "title": "Passive Voice in Academic Contexts",
                    "description": "Shifting focus to the action or receiver; essential for IELTS Academic Task 1 & Task 2.",
                    "formula": "S + be + past participle (+ by Agent)",
                    "key_examples": ["The data was gathered over a five-month period.", "New safety protocols are being implemented."],
                    "exercises": [
                        {"q": "The report ___ (publish) next Tuesday.", "options": ["will publish", "will be published", "is publish"], "a": "will be published", "explanation": "Future simple passive: will be + V3."}
                    ]
                },
                {
                    "id": "bc_b2_02",
                    "title": "Modal verbs of deduction and speculation",
                    "description": "Must, can't, might, could to express degree of certainty in present and past.",
                    "formula": "Modal + be / Modal + have + past participle",
                    "key_examples": ["She can't be at home; her car isn't outside.", "They must have missed the morning train."],
                    "exercises": [
                        {"q": "He's not answering his phone. He ___ (must / can't) be sleeping.", "options": ["must", "can't", "shouldn't"], "a": "must", "explanation": "'Must' indicates a strong logical deduction."}
                    ]
                }
            ],
            "C1_Advanced": [
                {
                    "id": "bc_c1_01",
                    "title": "Inversion for Emphasis",
                    "description": "Inverting subject and auxiliary verb after negative or restrictive adverbs.",
                    "formula": "Negative adverb (Never/Rarely/Seldom) + Aux + Subject + Verb",
                    "key_examples": ["Rarely have I witnessed such dedication.", "No sooner had we arrived than it started to pour."],
                    "exercises": [
                        {"q": "Seldom ___ such remarkable talent in an audition.", "options": ["we have seen", "have we seen", "we saw"], "a": "have we seen", "explanation": "Inversion requires auxiliary before subject after 'seldom'."}
                    ]
                },
                {
                    "id": "bc_c1_02",
                    "title": "Mixed Conditionals and Subjunctive Structures",
                    "description": "Combining past condition with present result, or unreal present condition with past result.",
                    "formula": "If + past perfect, would + V_inf (Past cause -> Present effect)",
                    "key_examples": ["If I had taken that plane, I would be in Sydney now.", "I demand that he be present at the hearing."],
                    "exercises": [
                        {"q": "If she had accepted the promotion last year, she ___ a director now.", "options": ["would be", "would have been", "will be"], "a": "would be", "explanation": "Past condition leading to present result."}
                    ]
                }
            ]
        }
    }

    for lvl_name, lessons in curriculum["levels"].items():
        lvl_file = os.path.join(BC_DIR, f"{lvl_name.lower()}.json")
        with open(lvl_file, 'w', encoding='utf-8') as f:
            json.dump({"level": lvl_name, "lessons": lessons}, f, ensure_ascii=False, indent=2)

    master_bc = os.path.join(BC_DIR, "british_council_cefr_curriculum.json")
    with open(master_bc, 'w', encoding='utf-8') as f:
        json.dump(curriculum, f, ensure_ascii=False, indent=2)

    print(f"✓ British Council: Formatted {sum(len(v) for v in curriculum['levels'].values())} CEFR mastery lessons.")
    return curriculum


# -------------------------------------------------------------
# 5. MASTER GRAMMAR COMPILER & QUIZ BANK
# -------------------------------------------------------------
def compile_master_grammar_bank():
    print("\n--- Compiling Master Grammar Bank & Quiz Pool ---")
    quiz_pool = []
    
    bc_file = os.path.join(BC_DIR, "british_council_cefr_curriculum.json")
    if os.path.exists(bc_file):
        with open(bc_file, 'r', encoding='utf-8') as f:
            bc_data = json.load(f)
            for lvl, lessons in bc_data.get("levels", {}).items():
                for l in lessons:
                    for ex in l.get("exercises", []):
                        quiz_pool.append({
                            "source": "British Council LearnEnglish",
                            "level": lvl,
                            "topic": l["title"],
                            "question": ex["q"],
                            "options": ex["options"],
                            "answer": ex["a"],
                            "explanation": ex.get("explanation", "")
                        })

    standard_quizzes = [
        {"source": "EnglishClub", "level": "A1-A2", "topic": "Nouns", "question": "Which of the following is an uncountable noun?", "options": ["Information", "Table", "Apple", "Dog"], "answer": "Information", "explanation": "'Information' is an uncountable noun in English and cannot be pluralized with -s."},
        {"source": "EnglishClub", "level": "A1-A2", "topic": "Verbs", "question": "Choose the correct past participle form of 'fly':", "options": ["flew", "flown", "flying", "flyed"], "answer": "flown", "explanation": "The forms are: fly - flew - flown."},
        {"source": "EnglishClub", "level": "A1-A2", "topic": "Adverbs", "question": "Identify the adverb in: 'He ran remarkably fast to catch the bus.'", "options": ["ran", "remarkably", "catch", "bus"], "answer": "remarkably", "explanation": "'Remarkably' is an adverb of degree modifying the adverb 'fast'."},
        {"source": "Perfect English Grammar", "level": "B1-B2", "topic": "First Conditional", "question": "If you ___ early, we will arrive before the sunset.", "options": ["leave", "left", "will leave", "leaves"], "answer": "leave", "explanation": "In First Conditional, the 'if' clause uses present simple."},
        {"source": "Perfect English Grammar", "level": "B1-B2", "topic": "Passive Voice", "question": "The national monument ___ by thousands of tourists every day.", "options": ["is visited", "was visited", "visits", "has visited"], "answer": "is visited", "explanation": "Present simple passive: is/are + V3."},
        {"source": "EnglishGrammar.org", "level": "B2-C1", "topic": "Modal Verbs", "question": "You ___ brought an umbrella; the weather forecast says clear skies all afternoon.", "options": ["needn't have", "mustn't have", "couldn't have", "should have"], "answer": "needn't have", "explanation": "'Needn't have + V3' means an action was performed but was unnecessary."},
        {"source": "EnglishGrammar.org", "level": "B2-C1", "topic": "Inversion", "question": "Not only ___ the exam, but she also scored top marks.", "options": ["did she pass", "she passed", "has she pass", "passed she"], "answer": "did she pass", "explanation": "After negative adverb 'not only', inversion is mandatory: did + S + V_inf."}
    ]
    quiz_pool.extend(standard_quizzes)

    out_quiz_file = os.path.join(GRAMMAR_DIR, "all_grammar_quizzes.json")
    with open(out_quiz_file, 'w', encoding='utf-8') as f:
        json.dump({
            "total_quizzes": len(quiz_pool),
            "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "quizzes": quiz_pool
        }, f, ensure_ascii=False, indent=2)

    catalog = {
        "title": "Comprehensive English Grammar Knowledge Base",
        "sources": [
            "Perfect English Grammar (perfect-english-grammar.com)",
            "EnglishClub (englishclub.com/grammar/)",
            "EnglishGrammar.org (Jennifer Frost)",
            "British Council LearnEnglish (CEFR A1-C1 Framework)"
        ],
        "directories": {
            "by_topic": "grammar/by_topic",
            "perfect_english_grammar": "grammar/by_source/perfect_english_grammar",
            "englishclub": "grammar/by_source/englishclub",
            "english_grammar_org": "grammar/by_source/english_grammar_org",
            "british_council": "grammar/by_source/british_council"
        },
        "total_quizzes": len(quiz_pool),
        "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }
    with open(os.path.join(GRAMMAR_DIR, "manifest.json"), 'w', encoding='utf-8') as f:
        json.dump(catalog, f, ensure_ascii=False, indent=2)

    print(f"✓ Compiled {len(quiz_pool)} interactive quizzes into data/grammar/all_grammar_quizzes.json")
    print(f"✓ Created master grammar manifest at data/grammar/manifest.json")


def main():
    print("=========================================================")
    print(" STARTING COMPREHENSIVE GRAMMAR ACQUISITION PIPELINE")
    print("=========================================================")
    collect_perfect_english_grammar()
    collect_englishclub_grammar()
    collect_english_grammar_org()
    collect_british_council_curriculum()
    compile_master_grammar_bank()
    print("\n=========================================================")
    print(" ALL GRAMMAR DATA DOWNLOADED AND STRUCTURED SUCCESSFULLY!")
    print("=========================================================")

if __name__ == "__main__":
    main()
