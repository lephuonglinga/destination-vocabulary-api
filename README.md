# Destination Vocabulary API

Backend API cho ứng dụng Flutter **Worduno** — cung cấp dữ liệu từ vựng sách Destination và AI Coach (Gemini free tier).

**Live docs:** [destination-vocabulary-api.onrender.com/docs](https://destination-vocabulary-api.onrender.com/docs)

## Tính năng

| Nhóm | Mô tả |
|------|--------|
| **Vocabulary** | Đọc level, unit, term từ file tĩnh (B1, B2, C1&C2) |
| **AI Coach** | Feedback từ vựng và đánh giá câu học sinh viết (tiếng Việt) |
| **Exam AI** | Sinh câu Cloze và chấm Sentence Writing (score 0–10) |

Không có đăng nhập, không đồng bộ dữ liệu học tập — progress lưu cục bộ trên Flutter client.

## API Endpoints

### Vocabulary (GET)

| Method | Path | Mô tả |
|--------|------|--------|
| `GET` | `/` | Health message |
| `GET` | `/api` | Danh sách level: `b1`, `b2`, `c1&c2` |
| `GET` | `/api/{level}` | Trả về tên level |
| `GET` | `/api/{level}/units` | Danh sách unit trong level |
| `GET` | `/api/{level}/units/{unit_name}` | Danh sách term + definition trong unit |

`unit_name` hỗ trợ URL encode (ví dụ khoảng trắng, `&`).

**Ví dụ response term:**

```json
[
  { "term": "blow up", "definition": "nổ tung" },
  { "term": "add up", "definition": "tính tổng số" }
]
```

### AI Coach (POST)

Cần cấu hình `GEMINI_API_KEY`. Client gửi `word` và `definition` (vì cùng một từ có thể khác nghĩa ở từng level).

#### `POST /api/coach/explain`

Feedback từ vựng: khi nào dùng, hoàn cảnh, ví dụ.

**Request:**

```json
{
  "word": "blow up",
  "definition": "nổ tung"
}
```

**Response:**

```json
{
  "usage": "Giải thích ngắn bằng tiếng Việt...",
  "contexts": ["Hoàn cảnh 1", "Hoàn cảnh 2"],
  "examples": [
    {
      "sentence": "The building blew up last night.",
      "note": "Nghĩa đen: vụ nổ"
    }
  ]
}
```

- `contexts`: 1–2 phần tử  
- `examples`: 1–2 phần tử (câu tiếng Anh + ghi chú tiếng Việt)

#### `POST /api/coach/evaluate`

Feedback câu học sinh viết trong Coach session. **Không chấm điểm.**

**Request:**

```json
{
  "word": "blow up",
  "sentence": "The bomb blew up the bridge."
}
```

**Response:**

```json
{
  "grammar": "Nhận xét ngữ pháp...",
  "vocabulary": "Nhận xét cách dùng từ...",
  "naturalness": "Câu có tự nhiên không...",
  "suggestion": [
    "They plan to blow up the bridge.",
    "The bomb could destroy the bridge."
  ]
}
```

- `suggestion`: 1–2 câu gợi ý viết lại (tiếng Anh)

### Exam AI (POST)

Cần `GEMINI_API_KEY`. Tách riêng với Coach.

#### `POST /api/exam/cloze`

Sinh câu điền từ (Cloze AI). Server xáo thứ tự 4 đáp án trước khi trả về.

**Request:**

```json
{
  "word": "blow up",
  "definition": "nổ tung",
  "level": "b1"
}
```

- `level`: `b1`, `b2`, hoặc `c1&c2`
- Server tự chọn 3 distractor ngẫu nhiên từ toàn bộ từ trong level

**Response:**

```json
{
  "sentence": "The old factory _____ last night.",
  "options": ["add up", "blow up", "give up", "break down"],
  "correct_answer": "blow up"
}
```

- Câu và 4 đáp án: tiếng Anh  
- `options` đã được server shuffle  
- `correct_answer` và `options` không có nhãn loại từ `(n)`, `(v)`, ...

#### `POST /api/exam/evaluate-sentence`

Chấm bài Sentence Writing trong Exam. Có điểm số.

**Request:**

```json
{
  "word": "blow up",
  "definition": "nổ tung",
  "sentence": "The bomb blew up the bridge."
}
```

**Response:**

```json
{
  "score": 8,
  "grammar": "Nhận xét ngữ pháp...",
  "vocabulary": "Nhận xét cách dùng từ...",
  "naturalness": "Câu có tự nhiên không...",
  "suggestion": [
    "They plan to blow up the bridge."
  ]
}
```

- `score`: số nguyên **0–10**  
- Feedback tiếng Việt  
- `suggestion`: 1–2 câu gợi ý (tiếng Anh)

## Cấu trúc project (MVC)

```
├── app.py                          # FastAPI app, mount routers
├── config.py                       # Biến môi trường
├── models/                         # Pydantic request/response
├── controllers/                    # Route handlers
├── services/                       # Business logic, gọi LLM
├── prompts/                        # Prompt templates
└── data/                           # b1.txt, b2.txt, c1&c2.txt
```

## Chạy local

### 1. Cài dependency

```bash
pip install -r requirements.txt
```

### 2. Cấu hình môi trường

```bash
copy .env.example .env
```

Chỉnh `.env`:

```env
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-2.5-flash-lite
```

Lấy API key miễn phí: [Google AI Studio](https://aistudio.google.com/apikey)

**Model khuyến nghị (free tier):**

| Model | Ghi chú |
|-------|---------|
| `gemini-2.5-flash-lite` | Mặc định — quota cao nhất |
| `gemini-2.5-flash` | Thay thế nếu cần |

> Không dùng `gemini-2.0-flash` — đã hết quota free tier.

### 3. Chạy server

```bash
uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

Nếu port 8000 bị chiếm, đổi sang `8001` hoặc tắt process cũ.

### 4. Thử API

- Swagger UI: http://127.0.0.1:8000/docs  
- Vocabulary hoạt động không cần API key  
- Coach cần `GEMINI_API_KEY` hợp lệ

## Deploy (Render)

File `render.yaml` đã cấu hình sẵn. Trên Render dashboard, thêm environment variable:

| Biến | Bắt buộc | Mô tả |
|------|----------|--------|
| `GEMINI_API_KEY` | Có (cho Coach & Exam AI) | Key từ Google AI Studio |
| `GEMINI_MODEL` | Không | Mặc định `gemini-2.5-flash-lite` |

## Lỗi thường gặp

| Lỗi | Nguyên nhân | Cách xử lý |
|-----|-------------|------------|
| `503` — GEMINI_API_KEY chưa cấu hình | Thiếu key trong `.env` | Thêm key và restart server |
| `429` — Hết quota | Model cũ hoặc gọi quá nhanh | Đổi sang `gemini-2.5-flash-lite`, đợi ~1 phút |
| `WinError 10013` | Port đã bị chiếm | Đổi port hoặc tắt process Python cũ |

## Stack

- Python, FastAPI, Uvicorn  
- Pydantic (validation)  
- Google Generative AI (Gemini)  
- Dữ liệu từ vựng: file text UTF-8 trong `data/`

## Client

Flutter app **Worduno** gọi API này cho màn Home (vocabulary), Coach (explain / evaluate) và Exam (cloze / evaluate-sentence).
