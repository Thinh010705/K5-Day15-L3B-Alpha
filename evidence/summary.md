# Tổng hợp bằng chứng pain

> Điền ở guide bước 1.2, xong trước **CP3 10:00 Thứ Bảy 28/11**. Chấm ở rubric R1.
> Người tổng hợp: Nguyễn Năng Thịnh (TV1). Số đào data lấy từ `evidence/data-mining.md` (TV2, chạy lại: `python evidence/prepare_data.py` rồi `python evidence/count.py`). Kiểm chéo vế hậu quả của TV1: `python evidence/citation_check.py`.
> Ô ghi **[CHỜ P_]** là chỗ chưa có ghi chép phỏng vấn — điền từ `evidence/interviews/P_.md`, không điền khi chưa phỏng vấn.

## 1. Nguồn đã dùng

| Nguồn | Đạt ngưỡng? | File |
|---|---|---|
| Đào data (x/N, %, cách đếm chạy lại được, ≥5 ví dụ) | ☑ — M1 231/576 (40,1%), cách đếm ghi trước, script + 29 test, 6 ví dụ | `evidence/data-mining.md` · `evidence/count.py` · `evidence/citation_check.py` |
| Phỏng vấn (≥3 người ngoài nhóm, đúng người dùng) | ☐ — [CHỜ P1–P4] | `evidence/interviews/P1.md`… |
| Khảo sát (≥20 người ngoài nhóm, đúng người dùng) | — không làm | — |

Nguồn chính: **đào data**. Nguồn kiểm lại: **phỏng vấn P1–P4** (vì sao, mất bao lâu).

## 2. Số chính

**Đào data** — data pre-class BTC, 05/11–25/11/2026 (UTC). 144/436 người có hoạt động (33,0%) từng hỏi trợ giảng; 1.153 lượt trợ giảng.

| Mã | Đếm gì | x / N | % | Ghi chú |
|---|---|---|---|---|
| M1 | Lượt trợ giảng **không có mốc trích dẫn** (13/11–25/11) | 231/576 | 40,1% | ≥ ngưỡng 20% của giả thuyết; khoảng chặn 39,6% … 40,8% |
| M1 | … bỏ lượt AI ghi thiếu ngữ cảnh (độ nhạy) | 194/538 | 36,1% | vẫn ≥ 20% |
| M1 | Người nhận ≥1 câu trả lời không có mốc | 58/86 | 67,4% | TB 3,98 lần / 13 ngày ≈ 9,2 lần / tháng |
| M4 | Lượt trợ giảng ghi thiếu ngữ cảnh | 100/1.138 | 8,8% | 50/142 người |
| M5 | Câu hỏi dưới video → hỏi tiếp cùng video ≤5 phút | 520/1.091 | 47,7% | dấu vết hành vi, không phải nguyên nhân |
| M7 | Độ trễ trợ giảng (trung vị / p90) | 2,4 s / 4,6 s | — | chờ > 10 s: 1/1.138 → loại giả thuyết thay thế 4 |
| TV1 | Hỏi tiếp **hoặc** tua lùi cùng video ≤5 phút — lượt **không** có mốc | 117/231 | 50,6% | so với 180/326 (55,2%) lượt có mốc → **không cao hơn** |
| TV1 | Tua lùi cùng video ≤5 phút — lượt **không** có mốc | 12/231 | 5,2% | so với 46/326 (14,1%) lượt có mốc |
| TV1 | AI ghi thiếu ngữ cảnh — lượt **không** có mốc | 37/231 | 16,0% | so với 1/326 (0,3%) lượt có mốc |

Ba dòng TV1 chỉ tính câu hỏi dưới video (557 lượt có ghi khoá mốc, 13/11–25/11), định nghĩa hỏi tiếp giống M5.

**Phỏng vấn:** [CHỜ P1–P4] __/4 người gặp *(n nhỏ không ghi %)* · số lần / tháng: P1 __, P2 __, P3 __, P4 __ · mỗi lần mất __–__ phút

**Khảo sát:** không làm.

| | Vai | Gặp pain? | Số lần / 1 tháng qua | Lần gần nhất mất | Đang xoay xở bằng |
|---|---|---|---|---|---|
| P1 | [CHỜ P1] | | | | |
| P2 | [CHỜ P2] | | | | |
| P3 | [CHỜ P3] | | | | |
| P4 | [CHỜ P4] | | | | |

Khi phỏng vấn, xin thêm **câu hỏi thật** người đó từng hỏi trợ giảng (bỏ thông tin cá nhân) → chuyển TV4 làm câu thử `source = nguoi_dung` (bộ câu thử CP2 đang 0/12 câu từ người dùng / data thật, cần ≥ 1/3).

## 3. ≥5 trích dẫn hoặc ví dụ nguyên văn (có nguồn, bỏ tên)

Data không có câu chữ học viên viết (chỉ có độ dài), nên ví dụ data là **dòng metadata**, chọn tất định bằng `evidence/count.py` (khoá `vi_du` trong `evidence/data-mining-output.json`). Mã chat là mã BTC đã ẩn danh; không ghi mã học viên.

1. `C01187` — 13/11, hỏi trợ giảng dưới video `d06-r1-v01`: hỏi 92 ký tự → trả lời 600 ký tự, `moc_trich_dan = []`. *(M1)*
2. `C00882` — 13/11, dưới video `d05-r2-v06`: hỏi 18 ký tự → trả lời 220 ký tự, `moc_trich_dan = []`. *(M1)*
3. `C00983` — 05/11, dưới video `d01-r1-v05`: hỏi 29 ký tự → trả lời 182 ký tự, `missing_context = true`. *(M4)*
4. `C00992` — 08/11, dưới video `d02-r2-v01`: hỏi 34 ký tự → trả lời 298 ký tự, `missing_context = true`. *(M4)*
5. `C00581` — 05/11, dưới video `d01-r1-v02`: hỏi 82 ký tự; trong 5 phút sau câu trả lời hỏi tiếp cùng video. *(M5)*
6. `C00499` — 05/11, cùng video `d01-r1-v02`: hỏi 183 ký tự; lại hỏi tiếp trong 5 phút. *(M5)*

Trích nguyên văn phỏng vấn (1–2 câu / người):

7. "…" — [CHỜ P1]
8. "…" — [CHỜ P2]
9. "…" — [CHỜ P3]
10. "…" — [CHỜ P4]

## 4. Các nguồn có khớp nhau không

**Data nói:** 40,1% câu trả lời của trợ giảng không kèm mốc nào trong bài giảng, rơi vào 67,4% người nhận trả lời; nhưng sau câu trả lời không có mốc, học viên **không** hỏi tiếp hay tua lùi nhiều hơn (50,6% so với 55,2%; tua lùi còn thấp hơn: 5,2% so với 14,1%). Câu trả lời không có mốc đi kèm câu hỏi thiếu ngữ cảnh nhiều hơn hẳn (16,0% so với 0,3%). Độ trễ thấp (trung vị 2,4 s) nên giả thuyết thay thế 4 (vấn đề là thời gian phản hồi) không được ủng hộ.

**Người dùng nói:** [CHỜ P1–P4 — kiểm lại 3 điều: (a) họ có cần biết đoạn nào trong bài làm căn cứ không; (b) khi không có, họ làm gì và mất bao nhiêu phút; (c) tua lùi ít hơn có phải vì họ **bỏ qua, không kiểm** chứ không phải vì đã hiểu.]

**Khớp / lệch, vì sao:** Data chỉ cho biết phản hồi không có mốc là phổ biến; data **không** cho thấy học viên mất thêm công vì thiếu mốc. Hai cách đọc: (1) học viên không cần mốc → pain yếu; (2) không có mốc thì học viên không có chỗ để tua tới nên bỏ qua, không kiểm → hiểu sai mà không biết. Phỏng vấn phải phân xử hai cách đọc này.

## 5. Kết luận

Giả thuyết ở `evidence/hypothesis.md`: **đúng một phần, chờ phỏng vấn để chốt**.

- Tiêu chí data (≥20% phản hồi không có `moc_trich_dan`): **đạt** — 231/576 (40,1%); độ nhạy 194/538 (36,1%).
- Tiêu chí phỏng vấn (≥2/3 người kể được tình huống cụ thể trong tháng qua): [CHỜ P1–P4].
- Phần hậu quả ("phải tua lại, hỏi tiếp") **chưa được data ủng hộ**: tỉ lệ hỏi tiếp / tua lùi không cao hơn khi thiếu mốc.
- Giả thuyết thay thế 4 (thời gian phản hồi): **không được ủng hộ** — M7 trung vị 2,4 s.
- Giả thuyết thay thế 2 (câu hỏi thiếu ngữ cảnh) có tín hiệu: thiếu mốc trùng với thiếu ngữ cảnh. MVP vẫn giữ bước hỏi lại khi mơ hồ.

Quy tắc chốt (ghi trước khi đọc ghi chép phỏng vấn):
- ≥3/4 người kể được lần cụ thể muốn biết đoạn nào là căn cứ hoặc phải tự tìm lại → giữ A1.1, ghi **đúng**.
- 2/4 → giữ A1.1 nhưng ghi **phải đổi**: nhấn vào "kiểm chứng được", T lấy theo số người kể.
- ≤1/4 → ghi **sai**; xét chuyển trọng tâm sang A1.2 (hỏi lại khi mơ hồ), ghi lý do ở `spec.md` §10.

**Điều vẫn chưa biết:** mỗi lần thiếu căn cứ học viên mất bao nhiêu phút (T); học viên có hiểu sai vì phản hồi không có mốc không (data không có câu chữ nên không kết luận được trợ giảng trả lời sai).

## Lịch hẹn (dùng cho CP2 — chỉ ghi vai và giờ, không tên)

| Vai | Giờ hẹn | Đã xong? |
|---|---|---|
| P1 · học viên L3 (TV1 hỏi) | | ☐ |
| P2 · học viên L3 (TV2 hỏi) | | ☐ |
| P3 · học viên L3 (TV3 hỏi) | | ☐ |
| P4 · học viên L3 (TV4 hỏi) | | ☐ |
