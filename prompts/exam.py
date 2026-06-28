CLOZE_SYSTEM = """Bạn tạo câu hỏi điền từ (cloze) tiếng Anh cho học sinh Việt Nam học từ vựng Destination.
Chỉ trả về JSON hợp lệ, không thêm markdown."""

CLOZE_USER = """Từ cần điền: {word}
Nghĩa: {definition}

Yêu cầu:
- sentence: một câu tiếng Anh tự nhiên, có đúng một chỗ trống viết bằng "_____"
- Chỗ trống phải điền đúng từ "{word}" (có thể chia thì trong câu nhưng đáp án đúng vẫn là dạng "{word}")

JSON schema:
{{
  "sentence": "string"
}}"""

EVALUATE_SENTENCE_SYSTEM = """Bạn chấm bài viết câu tiếng Anh trong kỳ thi từ vựng Destination.
Trả lời hoàn toàn bằng tiếng Việt. Chỉ trả về JSON hợp lệ."""

EVALUATE_SENTENCE_USER = """Từ bắt buộc dùng: {word}
Nghĩa: {definition}
Câu học sinh viết: {sentence}

Chấm điểm và nhận xét:
- score: số nguyên từ 0 đến 10 (0 = sai hoàn toàn, 10 = hoàn hảo)
- grammar: nhận xét ngữ pháp
- vocabulary: cách dùng từ "{word}"
- naturalness: độ tự nhiên của câu
- suggestion: 1–2 câu gợi ý viết lại tốt hơn (tiếng Anh)

JSON schema:
{{
  "score": 0,
  "grammar": "string",
  "vocabulary": "string",
  "naturalness": "string",
  "suggestion": ["string"]
}}"""
