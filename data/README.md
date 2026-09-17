# IELTS Study Data Architecture & Complete Oxford 3000 Vocabulary Suite

Thư mục `data/` được tổ chức theo cấu trúc chuẩn hóa cho ứng dụng luyện thi IELTS và phát âm tiếng Anh (Listening, Reading, Writing, Speaking / Pronunciation, và Từ vựng theo chủ đề).

---

## 1. Cấu Trúc Thư Mục Dữ Liệu (`data/`)

```text
data/
├── manifest.json                     # Chỉ mục tập trung (Metadata tổng hợp cho toàn bộ web app)
│
├── vocabulary/                       # BỘ DỮ LIỆU TỪ VỰNG THEO CHỦ ĐỀ
│   ├── 3000_oxford_words_by_topic.json # 1.760 từ vựng chia theo 60 chủ đề chính thức (JSON phân tầng)
│   └── 3000_oxford_words_by_topic.csv  # 1.760 từ vựng dạng bảng tính CSV (id, topic, word, pos, ipa, meaning)
│
├── pronunciation/                    # BỘ DỮ LIỆU PHÁT ÂM & BẢNG PHIÊN ÂM IPA
│   ├── ipa_chart/                    # BẢNG PHIÊN ÂM 44 ÂM IPA TIẾNG ANH ĐẦY ĐỦ FILE MP3
│   │   ├── ipa_chart_44.json         # Danh mục 44 âm: 12 nguyên âm đơn, 8 nguyên âm đôi, 24 phụ âm
│   │   ├── sounds/                   # 44 file .mp3 phát âm mẫu của chính từng âm IPA
│   │   └── examples/                 # 44 file .mp3 phát âm từ khóa đại diện (sheep, ship, think...)
│   └── us/                           # DỮ LIỆU TỪ ĐIỂN IPA GIỌNG MỸ (GENERAL AMERICAN)
│       ├── en_US_ipa.txt             # Kho 125.927 từ kèm ký âm IPA chuẩn Mỹ (CMUdict / open-dict-data)
│       ├── ielts_academic_ipa.json   # Bộ từ vựng học thuật & IELTS (IPA, số âm tiết, trọng âm)
│       ├── us_phonemes_guide.json    # Hướng dẫn âm vị Mỹ (Flap T, Rhoticity, Yod-Dropping)
│       └── audio/                    # File MP3 phát âm từ vựng học thuật
│
├── listening/                        # DỮ LIỆU KỸ NĂNG NGHE
│   ├── bbc_6minute/
│   │   ├── audio/                    # File âm thanh .mp3 thực tế (chuẩn giọng British BBC)
│   │   └── transcripts/              # File .json chi tiết từng tập (title, summary, câu thoại)
│   └── dictation_sentences/
│       └── dictation_pool.json       # Ngân hàng câu luyện chép chính tả (Listening Dictation)
│
├── reading/                          # DỮ LIỆU KỸ NĂNG ĐỌC
│   ├── academic_passages/            # Bài đọc IELTS phân đoạn học thuật [A], [B], [C]...
│   └── all_passages.json             # Tổng hợp toàn bộ bài đọc + câu hỏi + từ vựng AWL
│
├── writing/                          # DỮ LIỆU KỸ NĂNG VIẾT
│   ├── task1/
│   │   └── task1_bank.json           # Đề biểu đồ, mô tả, phân tích & bài mẫu Band 9.0
│   ├── task2/
│   │   └── task2_bank.json           # Đề nghị luận xã hội 5 dạng & bài mẫu Band 8.5 - 9.0
│   ├── phrasebank/
│   │   └── academic_phrasebank.json  # Mẫu câu học thuật (Manchester Academic Phrasebank)
│   └── band_descriptors.json         # Bảng tiêu chí chấm điểm IELTS Band 1 - 9 chính thức
│
├── ielts_tests/                      # KHO ĐỀ THI IELTS THỰC CHIẾN (IDP/BC, IOT, CAMBRIDGE/STUDY4)
│   ├── official_idp_bc/              # Đề thi chính thức từ IDP & British Council
│   │   ├── audio/                    # 9 File âm thanh .mp3 bài thi Listening thật
│   │   ├── reading/                  # Đề thi Reading dạng Academic & General Training (PDF)
│   │   ├── writing/                  # Đề Task 1 & Task 2 kèm bài viết mẫu & nhận xét giám khảo
│   │   ├── listening/                # Answer keys & phiếu câu hỏi Listening chính thức
│   │   └── idp_official_catalog.json # Toàn bộ danh mục liên kết và metadata đề thi chuẩn
│   ├── ielts_online_tests/           # Bộ đề Mock Test đầy đủ từ ieltsonlinetests.com
│   │   ├── audio/                    # File MP3 nghe 30 phút trọn vẹn (Test 1 & Test 2)
│   │   └── tests/                    # Cấu trúc câu hỏi 40 câu Listening & 3 Passages Reading (JSON)
│   └── cambridge_study4/             # Bộ đề chuẩn hóa theo cấu trúc Cambridge IELTS & Study4
│       ├── reading/                  # Dữ liệu Cambridge 18 Test 1 (Reading + giải thích đáp án + từ vựng)
│       └── STUDY4_INTEGRATION_GUIDE.md # Hướng dẫn cào dữ liệu có đăng nhập từ Study4.com
│
└── grammar/                          # KHO DỮ LIỆU NGỮ PHÁP TIẾNG ANH TOÀN DIỆN (4 NGUỒN UY TÍN)
    ├── manifest.json                 # Danh mục chỉ mục tổng thể các nguồn và chủ điểm ngữ pháp
    ├── all_grammar_quizzes.json      # Ngân hàng câu hỏi trắc nghiệm tự chấm điểm kèm giải thích
    ├── by_topic/                     # Phân loại chuyên đề (Tenses, Conditionals, Modals, Passive...)
    │   ├── tenses/                   # 12 thì tiếng Anh (công thức, cách dùng, ví dụ)
    │   ├── conditionals/             # Câu điều kiện 0, 1, 2, 3 và Mixed
    │   ├── parts_of_speech/          # 9 từ loại tiếng Anh (danh từ, động từ, tính từ...)
    │   └── ...
    └── by_source/                    # Dữ liệu phân tách theo từng trang web
        ├── perfect_english_grammar/  # 21 bài học lý thuyết & 24 file bài tập PDF có đáp án
        ├── englishclub/              # 9 Parts of speech, Sentence-level grammar
        ├── english_grammar_org/      # 12 bài học & câu đố ngữ pháp từ Jennifer Frost
        └── british_council/          # Chuẩn khung CEFR chuẩn châu Âu (A1-A2, B1-B2, C1)
```

---

## 2. Dữ Liệu 3000 Từ Vựng Oxford Theo Chủ Đề (Từ File PDF)

Tệp PDF gốc `3000-tu-vung-tieng-anh-thong-dung-oxford-theo-chu-de.pdf` (107 trang) đã được scan và trích xuất thành công:
- **Tổng số từ vựng**: **1.760 từ vựng**.
- **Tổng số chủ đề**: **60 chủ đề** (Đồ dùng học tập, Hành động, Hoạt động thường ngày, Mua sắm, Biển, Trường học, Bệnh viện, Thể thao, Ngân hàng...).
- **Định dạng trường dữ liệu**:
  - `id`: Mã số thứ tự từ 1 đến 1760.
  - `topic_id`: Mã chủ đề từ 1 đến 60.
  - `topic`: Tên chủ đề tiếng Việt chuẩn.
  - `word`: Từ vựng hoặc cụm từ tiếng Anh.
  - `pos`: Từ loại (`n`, `v`, `adj`, `adv`, `n. phr`, `v. phr`...).
  - `ipa`: Phiên âm quốc tế IPA (đã chuẩn hóa dấu trọng âm chính `ˈ` và phụ `ˌ`).
  - `meaning`: Nghĩa tiếng Việt (đã làm sạch khoảng trắng tự nhiên tiếng Việt).

---

## 3. Cách Tích Hợp Vào Giao Diện `Vocabulary Topics.html`

Tải dữ liệu từ vựng theo chủ đề:

```javascript
fetch('./data/vocabulary/3000_oxford_words_by_topic.json')
  .then(res => res.json())
  .then(data => {
    console.log("Tổng số chủ đề:", data.total_topics); // 60
    console.log("Tổng số từ:", data.total_words);     // 1760

    // Render danh sách chủ đề:
    data.topics.forEach(topic => {
      console.log(`Chủ đề ${topic.topic_id}: ${topic.topic_name} (${topic.words_count} từ)`);
    });

    // Lấy từ vựng của chủ đề đầu tiên:
    const firstTopicWords = data.topics[0].words;
  });
```
