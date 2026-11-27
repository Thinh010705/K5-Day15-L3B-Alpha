# Dữ liệu cho bộ câu thử — TV2 bàn giao cho TV4 (và TV3)

> Đầu việc TV2 · CP3 "Cung cấp dữ liệu cho benchmark". Người phụ trách: Hoàng Minh Quyền (TV2).
> Số lấy từ `python evidence/count.py` → khoá `phan_ra`, `vi_du` trong `evidence/data-mining-output.json`. Data 05/11 → 25/11/2026, chỉ lượt trợ giảng.
> File này **không sửa** `eval/benchmark.csv` (TV4 chủ trì) — chỉ đưa số để TV4 chọn câu.

## 1. Nên dựng kho đoạn cho bài nào (TV3)

| Ngày học | Lượt trợ giảng | Không có mốc trích dẫn (13–25/11) | Thiếu ngữ cảnh |
|---|---|---|---|
| **Day01** (`ai-llm-foundation`) | **355/1.153 (30.8%)** | 49/155 (31.6%) | 39/351 (11.1%) |
| Day03 | 146 | 4/32 (12.5%) | 7/145 (4.8%) |
| Day04 | 146 | 11/39 (28.2%) | 12/146 (8.2%) |
| Day02 | 116 | 23/51 (45.1%) | 16/113 (14.2%) |
| Day08 | 94 | 52/94 (55.3%) | 10/92 (10.9%) |
| Day07 | 77 | 52/77 (67.5%) | 6/72 (8.3%) |
| (các ngày khác) | ≤ 85 mỗi ngày | | |

Video bị hỏi nhiều nhất: `d01-r1-v02` (124 lượt) · `d01-r1-v01` (93) · `d01-r1-v05` (68) · `d02-r2-v01` (54) · `d01-r1-v03` (45).

**Đề xuất:** dựng kho 8–12 đoạn cho **bài Day01**, ưu tiên video `d01-r1-v02` và `d01-r1-v01` — nơi học viên hỏi nhiều nhất, nên bản chạy thử chạm đúng chỗ có nhiều người dùng nhất. Day07 / Day08 có tỉ lệ không mốc cao nhất nhưng ít lượt hơn (77, 94) — phương án dự phòng.

## 2. Hình dạng câu hỏi thật (chỉ có độ dài, không có chữ)

| Độ dài câu hỏi (ký tự) | Lượt | Thiếu ngữ cảnh | Không có mốc trích dẫn |
|---|---|---|---|
| 1–20 | 187 (16.2%) | 23/187 (12.3%) | 36/73 (49.3%) |
| 21–60 | 416 (36.1%) | 46/411 (11.2%) | 59/191 (30.9%) |
| 61–150 | 515 (44.7%) | 27/505 (5.3%) | 133/301 (44.2%) |
| > 150 | 35 (3.0%) | 4/35 (11.4%) | 3/11 (27.3%) |

→ Gần **1/6 câu hỏi chỉ ≤ 20 ký tự** và nhóm này bị ghi thiếu ngữ cảnh gấp ~2,3 lần nhóm 61–150 ký tự. Bộ câu thử nên có **câu rất ngắn** (vài từ, thậm chí 1–2 ký tự như ví dụ `C01056`) để kiểm hành vi hỏi lại.

## 3. Tỉ lệ gợi ý cho bộ câu thử (từ data)

| Hành vi cần kiểm (`spec.md` §5) | Data nói gì | Gợi ý cho benchmark |
|---|---|---|
| Trả lời kèm mã đoạn nguồn (`thuong`) | 40.1% câu trả lời hiện tại không có mốc trích dẫn (M1) | mọi câu `thuong` phải có `pass_criterion` kiểm **mã đoạn đúng** |
| Hỏi lại khi mơ hồ (`kho`) | 8.8% lượt thiếu ngữ cảnh (M4); 16.2% câu ≤ 20 ký tự | ≥ 2 câu mơ hồ, trong đó ≥ 1 câu rất ngắn |
| Từ chối khi không có trong bài (`tu_choi`) | 21.7% câu hỏi bị chấm "không bám bài" (M6, máy chấm) | ≥ 2 câu ngoài bài |
| Câu nối tiếp / hỏi tiếp | 47.7% câu hỏi dưới video có câu hỏi tiếp trong 5 phút (M5) | ≥ 1 câu kiểu "giải thích thêm ý vừa rồi" (mơ hồ nếu đứng một mình) |
| Câu cần kết hợp nhiều đoạn | câu trả lời có mốc dẫn 1–6 mốc (13% chỉ 1 mốc *(đếm ở review, `count.py` chưa in)*), có khi ở **video khác** (ví dụ `C00394` dẫn cả `d06-r1-v02` lẫn `d06-r1-v04`) | ≥ 1 câu cần 2 đoạn |

## 4. Ghi `source` cho đúng

- Data BTC **không có câu chữ** câu hỏi → câu nhóm tự viết theo hình dạng ở trên vẫn là **`tu_viet`** (có thể ghi chi tiết, vd `tu_viet: mô phỏng độ dài / video của data_that C00983`). **Không** ghi `data_that` cho câu nhóm tự đặt chữ.
- `run.py check` cần ≥ 1/3 câu `nguoi_dung` / `data_that` → nguồn thật khả thi nhất là **câu hỏi thật học viên kể trong phỏng vấn P1–P4** (`nguoi_dung: P_`). Khi phỏng vấn, xin người được hỏi đọc lại nguyên văn 2–3 câu họ từng hỏi trợ giảng.

## 5. Mã dòng có thể trỏ tới trong `ghi_chu` / `spec.md` §5

`C01187`, `C00882` (trả lời không mốc) · `C00551` (có mốc, học viên bấm link tới đúng mốc) · `C00394` (có mốc, học viên vẫn tua lùi) · `C00983` (câu 29 ký tự, thiếu ngữ cảnh, không bám bài) · `C01056` (câu 2 ký tự). Chi tiết: `evidence/data-mining.md` mục 4.
