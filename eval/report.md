# Báo cáo đánh giá — lượt 1 → một cải tiến → lượt 2

> Điền ở guide bước 4.1. Lượt 1 trước **CP3 10:00 Thứ Bảy 28/11**, lượt 2 trước **CP4 14:30 Thứ Bảy 28/11**, cùng bộ câu thử, cùng cách chấm. Chấm ở rubric R5.
> Số lấy từ `python run.py score eval/run-1.csv` (và `run-2.csv`) sau khi điền cột `pass`. **Kết quả thấp ghi thật vẫn đủ điểm.**
> Không được: sửa chuẩn "đạt", bỏ câu thử trượt, sửa `expected` cho khớp output, sửa kết quả lượt đã chạy.

## 1. Kết quả

Run 1 dùng `gemini-3.5-flash-lite` và khoảng nghỉ 2 giây giữa các câu. Model `gemini-3.8-flash` trả HTTP 503 khi kiểm tra kết nối. Codex chấm từng đầu ra theo tiêu chí CP2. Điểm đang chờ người chấm thứ hai đối chiếu.

| Lượt | Run ID | Đạt / tổng | % | thuong | kho | tu_choi | So với chuẩn "đạt" |
|---|---|---|---|---|---|---|---|
| 1 | `run-1@20261127-212409` | 25/30 | 83,3% | 10/13 | 10/12 | 5/5 | Chưa đạt |
| Chạy lại qua OpenRouter | `run-2@20261127-213001` | 26/30 | 86,7% | 11/13 | 10/12 | 5/5 | Chưa đạt |

Kết quả và trace của Run 1 nằm ở `eval/run-1.csv` và `traces/run-1.jsonl`.

Lượt chạy lại dùng `nvidia/nemotron-3-ultra-550b-a55b:free` qua OpenRouter, nghỉ 4 giây giữa các câu. Có 0 lỗi API. Bộ câu thử, code và ngưỡng chấm giữ nguyên. Lưu ở `eval/run-2.csv` và `traces/run-2.jsonl`. Codex chấm sơ bộ hai lượt, đang chờ đối chiếu độc lập.

| Metric CP2 | Run 1 | Chạy lại qua OpenRouter | Ngưỡng |
|---|---|---|---|
| Trích đúng nguồn | 19/22 (86,4%) | 20/22 (90,9%) | ≥90% |
| Nội dung bám nguồn | 18/22 (81,8%) | 19/22 (86,4%) | ≥80% |
| Làm rõ đúng ranh giới | 2/3 (66,7%) | 2/3 (66,7%) | ≥80% |
| Từ chối đúng ranh giới | 5/5 (100%) | 5/5 (100%) | 100% |

Lượt OpenRouter đạt ở B21, B24, B26 và B28. B03, B07 và B14 chuyển sang trượt. B18 vẫn trượt vì tự giới hạn câu hỏi làm rõ vào hai khái niệm khi người học chưa nêu ngữ cảnh. Chi tiết nằm trong cột `ghi_chu`.

## 2. Lỗi lượt 1 — gom thành nhóm có tên

| Nhóm lỗi | Số câu | Câu |
|---|---|---|
| Mã nguồn có thêm số trang trong JSON | 2 | B26, B28 |
| Tự thu hẹp câu hỏi thiếu ngữ cảnh | 1 | B18 |
| Thiếu ý bắt buộc | 1 | B24 |
| Lỗi kỹ thuật do giới hạn API | 1 | B21 |

**≥3 lỗi cụ thể:**

| Câu | Input | Output | Vì sao sai |
|---|---|---|---|
| B18 | Giải thích tiếp ý đoạn vừa rồi | Hỏi lại nhưng chỉ đưa FDE và Who–What–How làm lựa chọn | Đầu vào thiếu ngữ cảnh để giới hạn vào hai khái niệm đó |
| B21 | FDE đưa phần nào về sản phẩm chung? | Đầu ra rỗng, HTTP 429 | Một câu lỗi kỹ thuật được tính `pass = 0` và giữ trong mẫu số |
| B24 | Bàn giao nhiều tính năng, cần xem gì để biết có outcome? | Nêu thay đổi có giá trị, dẫn SL-16 | Thiếu phân loại rõ số tính năng bàn giao là output |
| B26 | Nhanh hơn, rẻ hơn, thao tác đơn giản hơn thuộc nhóm nào? | Trợ giảng từ chối | Trace cho thấy model trả đúng nội dung nhưng ghi `SL-19, trang 19` thay cho mã thuần `SL-19`, nên kiểm tra mã loại đầu ra |
| B28 | Bước ngay trước khi chọn tính năng trong Impact Mapping là gì? | Trợ giảng từ chối | Trace ghi `SL-22, trang 22` trong JSON nên kiểm tra mã loại đầu ra |

## 3. Một lần cải tiến

- Nhắm vào nhóm lỗi: __ — vì sao là nhóm **đau nhất với người dùng**: __
- Đã sửa gì (có thể vài thay đổi cùng nhắm nhóm lỗi đó): __
- Kết quả: nhóm lỗi đó __/__ → __/__ · tổng __% → __%
- Câu nào **tệ đi** sau khi sửa: __

## 4. Còn lại

- Lỗi chưa sửa + nguy hiểm thế nào: __
- Nếu có thêm 1 tuần: __
