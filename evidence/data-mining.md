# Đào data — cách đếm và kết quả

> Điền ở guide bước 1.2. Ôn lại: ngày 2, ngày 6 · lab ngày 2, lab ngày 6.
> Script đếm: `evidence/count.py` (chỉ thư viện chuẩn). Người khác chạy lại phải ra cùng số.
> Repo chỉ chứa số đã tổng hợp và vài mã dòng làm ví dụ — không chép lại nguyên file data.
> Người phụ trách: TV2 (Data & Research Lead). Mục 1 viết và commit **trước** khi chạy script đếm.

## 1. Cách đếm — viết TRƯỚC khi chạy

- **Data dùng:** data pack pre-class BTC cấp (AI20K Level 3-4, khoá 5), đã chuẩn hoá bằng `python evidence/prepare_data.py` → `data-btc/preclass/` (không commit; sha256 ở `data-btc/MANIFEST.txt`). File: `events.csv`, `chat.csv`, `answers.csv`, `learners.csv`. Khoảng thời gian: **05/11/2026 → 25/11/2026 (giờ UTC)**, Day01 → Day13, 21 ngày lịch.
- **Script:** `python evidence/count.py` → in bảng số và ghi `evidence/data-mining-output.json` (chỉ số tổng hợp).
- **Nối bảng:** `events.ref_id` (dòng `chat_sent` / `agent_replied`) = `chat.id` = `answers.ref` (dòng `nguon = chat`). "Trợ giảng" = `chat.agent_id = teaching_assistant` (bỏ các bạn học AI `classmate_*`).
- **Đơn vị:** một **lượt** = một dòng `chat.csv` (một câu học viên nhắn + một câu AI trả lời). Một **người** = một mã `hv` duy nhất.

### Các tập người (mẫu số cho số "bao nhiêu người")

| Mã | Tập | Cách lấy |
|---|---|---|
| P0 | Tài khoản | mọi dòng `learners.csv` |
| P1 | Người có hoạt động | `hv` duy nhất có ≥1 dòng `events.csv` với `actor = learner` |
| P2 | Người hỏi trợ giảng | `hv` duy nhất có ≥1 lượt trợ giảng trong `chat.csv` |

### Các số sẽ đếm

| Mã | Hướng | Đếm gì (x) | Mẫu số (N) | Lọc / cửa sổ |
|---|---|---|---|---|
| **M1** | A1.1 — kiểm chứng nguồn | lượt trợ giảng có `moc_trich_dan = []` (danh sách rỗng) | lượt trợ giảng **có ghi khoá** `moc_trich_dan` trong `agent_replied.data` | từ 00:00 UTC của ngày đầu tiên có dòng `agent_replied` ghi khoá `moc_trich_dan` (script tự tìm) đến hết data |
| M1-người | A1.1 | người nhận ≥1 lượt M1 | người có ≥1 lượt trong mẫu số M1 | như M1 |
| M2 | Giả thuyết thay thế 3 — có dùng nguồn không | lượt có mốc trích dẫn (danh sách không rỗng) mà trong **10 phút** sau câu trả lời, cùng học viên có `video_seeked` với `by = link` | lượt trợ giảng có `moc_trich_dan` không rỗng | như M1; độ nhạy: 30 phút |
| M3 | Pain "phải tua lại" | lượt hỏi dưới video mà trong **5 phút** sau câu trả lời, cùng học viên tua **lùi** (`by = player`, `to < from`) trong **cùng video** | lượt trợ giảng `channel = video_question` có tên video | cả 21 ngày; tách riêng lượt có / không có mốc trích dẫn trong cửa sổ M1 |
| **M4** | A1.2 — câu hỏi mơ hồ | lượt trợ giảng có `missing_context = true` | lượt trợ giảng có ghi khoá `missing_context` | cả 21 ngày |
| M5 | A1.2 — hỏi tiếp | lượt hỏi dưới video mà cùng học viên hỏi trợ giảng tiếp về **cùng video** trong **5 phút** sau câu trả lời | lượt trợ giảng `channel = video_question` | cả 21 ngày |
| **M6** | A1.3 — câu ngoài bài | câu nhắn trợ giảng được giám khảo AI chấm `rubric_bam_bai = 0` ("không liên quan bài") | dòng `answers.csv` `nguon = chat`, `trang_thai_cham = da_cham`, nối được tới lượt trợ giảng | cả 21 ngày |
| M7 | Giả thuyết thay thế 4 — chờ lâu | trung vị, p90 của `latency_ms`; lượt chờ > 10 giây | lượt trợ giảng có `cached = false` | cả 21 ngày |
| V1 | Khối lượng (cho Impact, persona) | số lượt trợ giảng / người: trung vị, p75, p90, lớn nhất | P2 | cả 21 ngày; đổi ra / tháng = × 30/21 *(ngoại suy tuyến tính)* |
| V2 | Khối lượng | số **phiên hỏi** / người và số lượt / phiên; một phiên = chuỗi lượt trợ giảng của cùng học viên cách nhau ≤ 30 phút *(ngưỡng nhóm tự chọn)* | P2 | cả 21 ngày |

Với M1, M4, M6 còn đếm **số người** gặp (≥1 lần) và **số lần trung bình / người gặp** → dùng làm N và F cho bảng Impact (`spec.md` §2). T (phút mất mỗi lần) **không có trong data** — lấy từ phỏng vấn.

### Mẫu số — vì sao chọn như vậy

- **Không** dùng 721 tài khoản làm mẫu số: chỉ người có hoạt động (P1) hoặc người hỏi trợ giảng (P2) mới có thể gặp vấn đề.
- **M1 chỉ tính dòng có ghi khoá `moc_trich_dan`.** Khoá này không có trong dòng ghi trước ngày bắt đầu ghi (README BTC: "mỗi loại dữ liệu bắt đầu ghi từ ngày khác nhau; ô trống trước ngày đó không có nghĩa là học viên không làm"). Dòng không ghi khoá **không** bị tính là "không trích dẫn". Dòng trong cửa sổ mà vẫn không ghi khoá (u) báo riêng, kèm khoảng chặn: thấp = x/(N+u), cao = (x+u)/(N+u).
- Lượt `cached = true` (dùng lại câu trả lời cũ) vẫn tính vì học viên vẫn thấy câu trả lời đó; báo tách riêng.
- Ngưỡng giả thuyết (`evidence/hypothesis.md`, commit trước khi xem data): M1 **≥ 20%** thì ủng hộ giả thuyết. Giữ nguyên ngưỡng này dù kết quả ra sao.

### Những điều cách đếm này KHÔNG trả lời được

- Data không có câu chữ câu hỏi / câu trả lời → không kết luận trợ giảng trả lời **sai** hay **bịa**; "không có mốc trích dẫn" chỉ là thiếu căn cứ để học viên tự kiểm.
- M2, M3, M5 là **dấu vết hành vi** (proxy) — tua lại / hỏi tiếp có thể vì lý do khác. Chỉ dùng để so sánh, không kết luận nguyên nhân.
- `by = link` trong `video_seeked` được hiểu là tua do bấm một đường link (nhiều khả năng là mốc trích dẫn trong câu trả lời). Từ điển BTC không giải thích giá trị này → script kiểm thêm: bao nhiêu lần `by = link` xảy ra ngay sau một câu trả lời có mốc trích dẫn.

## 2. Đọc trước, đếm sau

Đã đọc: `README.md` của data pack, toàn bộ `column_dictionary.csv` (71 dòng) và `event_types.csv` (38 loại việc), 5 dòng đầu mỗi file, cấu trúc khoá JSON trong cột `data` của `chat_sent` (1.260 dòng) và `agent_replied` (1.260 dòng). Các *kiểu* hành vi thấy được (trước khi định nghĩa thứ cần đếm):

- Học viên hỏi trợ giảng ngay dưới video (`chat.channel = video_question`), hỏi bằng cách bôi đen chữ trên slide (`slide_text_asked`), hoặc nhắn với bạn học AI trong khung thảo luận (`video_discussion_reply`). Chỉ có **độ dài** câu hỏi / câu trả lời, không có câu chữ.
- Mỗi câu trả lời của AI có `agent_replied` trong `events.csv`: `missing_context` (thiếu ngữ cảnh), `moc_trich_dan` (danh sách mốc dạng `DayNN/dNN-....txt@giây` hoặc chỉ `@giây`, có khi rỗng `[]`), `latency_ms`, `cached`, `model`; ít dòng hơn có `verdict` (`correct` / `partial` / `incorrect`) và `reply_kind`.
- **Các khoá bắt đầu ghi vào những ngày khác nhau:** `missing_context`, `latency_ms` có từ 05/11; `moc_trich_dan`, `ngu_canh` chỉ từ **13/11**; `verdict` chỉ 46 dòng (08–20/11); `reply_kind` 169 dòng; `prompt_version`, `guidance_ids`, `learning_mode` chỉ ngày 25/11 → `verdict` và `reply_kind` quá ít để làm mẫu số chính.
- Học viên tua video (`video_seeked`) bằng thanh video (`by = player`) hoặc bằng link (`by = link`, rất ít dòng) — tua lùi và tua tới đều có.
- Câu nhắn AI của học viên được giám khảo AI chấm 3 tiêu chí 0–2 trong `answers.csv` (`rubric_bam_bai`, `rubric_y_moi`, `rubric_dung_ngu_canh`) — điểm do máy chấm, không có người kiểm lại.
- Câu hỏi dưới video có `lesson_id` gần như luôn trống; ngày học lấy từ `transcript` (`DayNN/...`). Giờ ghi theo UTC (giờ Việt Nam = UTC + 7).

## 3. Kết quả

*(điền sau khi chạy `python evidence/count.py` — commit riêng)*

| Đếm gì | x / N | % | Ghi chú |
|---|---|---|---|
| | | | |

## 4. ≥5 ví dụ cụ thể (mã dòng / mã đã ẩn danh, không đoán ai là ai)

1.
2.
3.
4.
5.

## 5. Giới hạn của data

Data cho biết người ta **làm gì**, không cho biết **vì sao**. Thiếu gì, lệch về phía nào: __
→ Kiểm lại bằng phỏng vấn / khảo sát nào: __
