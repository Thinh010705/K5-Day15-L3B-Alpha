# Data card — dữ liệu bản chạy thử dùng

> Điền ở guide bước 2.4 (bản đầu ở CP2, đủ ở CP3). Ôn lại: ngày 6 · lab ngày 6. Chấm ở rubric R4.
> Người phụ trách: Hoàng Minh Quyền (TV2 — Data & Research Lead). **Bản đầu CP2**, 27/11/2026.
> Không commit nguyên tài liệu khoá, dữ liệu cá nhân thật hay nguyên file data BTC cấp — chỉ đoạn trích ngắn, bản viết lại, hoặc số đã tổng hợp.

## Dataset 1 · Nhật ký pre-class AI20K K5 (data pack BTC `preclass/`)

| | |
|---|---|
| Dùng để làm gì | **đào bằng chứng pain** và Impact (`evidence/data-mining.md`); số lượt / phiên cho persona chi phí (`cost/personas.yaml`); gợi ý tình huống cho bộ câu thử (chỉ metadata — data không có câu chữ) |
| Từ đâu | data BTC cấp (`data/preclass/` trong repo đề). Trong repo này để ở `data-btc/` — **đã .gitignore, không commit** |
| Xử lý những bước gì | **chuẩn hoá** (`evidence/prepare_data.py`): bỏ BOM UTF-8, đổi CRLF → LF, cắt khoảng trắng 7 ô của `event_types.csv`, sửa tên file cũ `tra_loi.csv` → `answers.csv` trong mô tả `answer_submitted`; không đổi giá trị nào khác (đã so từng ô: 8 ô đổi, đều ở `event_types.csv`) · **kiểm**: số dòng 7/7 file khớp README BTC, số dòng 38 loại việc khớp `event_types.csv` · **lọc / nối** (`evidence/count.py`): chỉ lượt trợ giảng (`agent_id = teaching_assistant`), nối `events.ref_id = chat.id = answers.ref`, M1 chỉ tính từ 13/11 (ngày bắt đầu ghi `moc_trich_dan`) · **ẩn danh**: BTC đã thay mã; repo chỉ chứa số tổng hợp và mã dòng ví dụ |
| Số dòng / số đoạn | learners 721 · events 107.709 · chat 1.260 · answers 3.776 · class_events 849 · completed_items 2.472 · rewards 228. Dùng chính: 1.153 lượt trợ giảng của 144 người (trong 436 người có hoạt động) |
| Phiên bản / ngày lấy | bản BTC phát cho hackathon, data 05/11 → 25/11/2026 (UTC), Day01–Day13; chuẩn hoá 27/11/2026. sha256 sau chuẩn hoá: `chat.csv` 69409f3a…c1191 · `events.csv` f5a66abe…971ee (đủ ở `data-btc/MANIFEST.txt`) |
| Nhãn | **thật** (hành vi thật của học viên khoá, BTC đã ẩn danh). Riêng `rubric_*` trong `answers.csv` là nhãn **giám khảo AI** tự chấm, không có người kiểm lại |
| Giới hạn | không có câu chữ câu hỏi / câu trả lời (chỉ độ dài) · `moc_trich_dan` chỉ có từ 13/11, `verdict` 46 dòng, `learning_mode` / `prompt_version` chỉ 25/11 · giờ UTC, `occurred_at` theo đồng hồ máy học viên · chỉ 144/436 người có hoạt động từng hỏi trợ giảng, vài người hỏi rất nhiều (max 72 lượt) → lệch về người hỏi nhiều · một khoá, một trang pre-class |

## Dataset 2 · Data pack BTC `training-ops/` (lịch, phòng, phân công — giả lập)

| | |
|---|---|
| Dùng để làm gì | **không dùng** cho lát cắt A1 (bộ này phục vụ hướng A5 / A2). Chỉ chuẩn hoá vị trí cùng bộ trên |
| Từ đâu | data BTC cấp, để ở `data-btc/training-ops/` (không commit) |
| Xử lý những bước gì | chép nguyên 2 file `.xlsx` và README (không đổi) |
| Nhãn | `synthetic` (BTC ghi rõ người, email, ngày đều giả) |
| Giới hạn | BTC ghi rõ: không phải bằng chứng pain |

## Dataset 3 · Kho đoạn bài học có mã đoạn (nguồn cho `search_lesson`, `get_passage`)

| | |
|---|---|
| Dùng để làm gì | nguồn cho công cụ `search_lesson` / `get_passage` của bản chạy thử; mã đoạn dùng để chấm metric trích dẫn đúng |
| Từ đâu | **chưa có** — TV3 dựng ở CP3 từ một bài pre-class (trích ngắn / viết lại, không chép nguyên tài liệu khoá) |
| Xử lý những bước gì | __ (TV3 điền: bài nào, chia đoạn thế nào, mã đoạn dạng gì) |
| Số dòng / số đoạn | __ (kế hoạch: 8–12 đoạn) |
| Phiên bản / ngày lấy | __ |
| Nhãn | __ (nhóm tự viết lại / trích) |
| Giới hạn | __ |

**Data `synthetic` (nhóm tự sinh):** chưa có. Nếu sinh thêm (vd câu hỏi mẫu cho benchmark): ghi cách sinh (prompt / script), seed, người kiểm, số dòng đã kiểm tay. Data tự dựng **không phải bằng chứng pain**.
