# Tổng hợp bằng chứng pain

> Điền ở guide bước 1.2, xong trước **CP3 10:00 Thứ Bảy 28/11**. Chấm ở rubric R1.
> Người tổng hợp: Nguyễn Năng Thịnh (TV1). Số đào data lấy từ `evidence/data-mining.md` (TV2, chạy lại: `python evidence/prepare_data.py` rồi `python evidence/count.py`). Kiểm chéo vế hậu quả của TV1: `python evidence/citation_check.py`.
> Phỏng vấn: 3 người (P1–P3), ghi chép ở `evidence/interviews/P1.md`–`P3.md`, kịch bản và quy tắc chốt ở `evidence/interviews/kich-ban.md`. Không làm P4.

## 1. Nguồn đã dùng

| Nguồn | Đạt ngưỡng? | File |
|---|---|---|
| Đào data (x/N, %, cách đếm chạy lại được, ≥5 ví dụ) | ☑ — M1 231/576 (40,1%), cách đếm ghi trước, script + 29 test, 6 ví dụ | `evidence/data-mining.md` · `evidence/count.py` · `evidence/citation_check.py` |
| Phỏng vấn (≥3 người ngoài nhóm, đúng người dùng) | ◐ — 3 người (P1–P3), mỗi người 1 file, cả 3 đã dùng trợ giảng dưới video trong tháng qua. Đạt khi đầu mỗi file ghi vai, ngày giờ, người hỏi và xác nhận người ngoài nhóm: [CẦN ĐIỀN] | `evidence/interviews/P1.md` · `P2.md` · `P3.md` |
| Khảo sát (≥20 người ngoài nhóm, đúng người dùng) | ☑ — 22 phiếu, **20/22** dùng trợ giảng dưới video trong 30 ngày qua (vừa đủ 20), tất cả là người ngoài nhóm. Gửi qua Discord AI20K, chốt 22:34 ngày 27/11 | `evidence/survey/questions.md` · `results.csv` · `tally.py` |

Nguồn chính: **đào data**. Nguồn kiểm lại: **khảo sát** (gặp bao nhiêu, mất bao lâu, xoay xở bằng gì) và **phỏng vấn P1–P3** (vì sao, kể một lần cụ thể).

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

**Phỏng vấn:** **3/3** người kể được một lần cụ thể trong tháng qua *(n nhỏ không ghi %)* · số lần dùng trợ giảng / tháng: P1 1–2, P2 3–5, P3 6–10 · lần đó mất: P1 5 phút, P2 khoảng 10 phút, P3 10–13 phút *(P3.md ghi 13 phút ở phần ghi chép, 10 phút ở phần số)* → trung vị **10 phút**

**Khảo sát** (27/11, Google Form ẩn danh, 22 phiếu). Số dưới đây chỉ tính 20 phiếu trả lời "Có" ở câu 1. Chạy lại: `python evidence/survey/tally.py`.

| Câu | Đếm gì | x / n | % |
|---|---|---|---|
| 3 | Gặp khó khi xác định đoạn bài giảng làm căn cứ — thường xuyên hoặc thỉnh thoảng | 15/20 | 75% |
| 3 | … chỉ "thường xuyên" | 4/20 | 20% |
| 4 | Mỗi lần mất thêm 2–10 phút | 10/20 | 50% |
| 4 | … mất thêm ≥10 phút | 7/20 | 35% |
| 5 | Khi chưa kiểm chứng được thì dùng **công cụ AI khác** | 12/20 | 60% |
| 5 | … tua lại video | 1/20 | 5% |
| 6 | Lần gần nhất chỉ hiểu một phần, không giúp ích hoặc khó hiểu hơn | 12/20 | 60% |
| 7 | Khó khăn lớn nhất: **câu trả lời không giải quyết đúng câu hỏi** | 7/20 | 35% |
| 7 | … không gặp khó khăn đáng kể | 6/20 | 30% |
| 7 | … câu trả lời khó hiểu hoặc chưa đủ chi tiết | 3/20 | 15% |
| 7 | … **khó xác định đoạn bài giảng làm căn cứ** | 2/20 | 10% |
| 7 | … trợ giảng chưa hiểu ngữ cảnh / phản hồi lâu | 1/20 · 1/20 | 5% · 5% |

Giới hạn: form chưa có logic bỏ câu, câu 3 dễ được trả lời "Thỉnh thoảng", câu 5 và 7 chỉ cho chọn một (chi tiết ở `evidence/survey/questions.md`). Trung vị câu 4 rơi vào nhóm 2–10 phút. T ở `spec.md` §2 đổi thành 10 phút theo trung vị phỏng vấn (quy tắc đặt trước); 10 phút nằm ở biên trên nhóm trung vị của khảo sát.

| | Vai | Gặp pain? | Số lần / 1 tháng qua | Lần gần nhất mất | Đang xoay xở bằng |
|---|---|---|---|---|---|
| P1 | Học viên AI20K K5 | Một phần — không biết đoạn căn cứ nhưng không cần ngay, đi hỏi AI khác | 1–2 lần dùng trợ giảng | 5 phút | Hỏi công cụ AI khác · vẫn dùng trợ giảng vì "tiện" |
| P2 | Học viên AI20K K5 | Có — câu trả lời chung chung, phải tua lại tìm ví dụ trong video | 3–5 lần dùng trợ giảng | khoảng 10 phút | Tua lại video · vẫn hỏi trợ giảng trước vì tiện |
| P3 | Học viên AI20K K5 | Có — bỏ qua, sau đó phải quay lại tìm đoạn khi tự lập kế hoạch | 6–10 lần dùng trợ giảng | 10–13 phút | Bỏ qua nội dung · vẫn dùng vì có sẵn ngay chỗ học |
| P4 | không làm | | | | |

Số lần **gặp chỗ vướng** trong tháng: cả 3 người đều không nhớ, nên cột trên là số lần dùng trợ giảng.

**Câu hỏi thật từ phỏng vấn** → chuyển TV4 làm câu thử `source = nguoi_dung` (bộ câu thử đang 0/12 câu từ người dùng / data thật, cần ≥ 1/3):
- P1: "RAG khác gì với việc đưa tài liệu thẳng vào prompt? Cho mình một ví dụ dễ hiểu."
- P2: "Trong ví dụ AI soạn phản hồi cho học viên, con người cần duyệt ở bước nào trước khi gửi?"
- P3: "Trong AI SDLC, nhóm nên xác định tiêu chí đánh giá từ lúc lên kế hoạch hay đợi làm xong bản thử rồi mới đánh giá?"

## 3. ≥5 trích dẫn hoặc ví dụ nguyên văn (có nguồn, bỏ tên)

Data không có câu chữ học viên viết (chỉ có độ dài), nên ví dụ data là **dòng metadata**, chọn tất định bằng `evidence/count.py` (khoá `vi_du` trong `evidence/data-mining-output.json`). Mã chat là mã BTC đã ẩn danh; không ghi mã học viên.

1. `C01187` — 13/11, hỏi trợ giảng dưới video `d06-r1-v01`: hỏi 92 ký tự → trả lời 600 ký tự, `moc_trich_dan = []`. *(M1)*
2. `C00882` — 13/11, dưới video `d05-r2-v06`: hỏi 18 ký tự → trả lời 220 ký tự, `moc_trich_dan = []`. *(M1)*
3. `C00983` — 05/11, dưới video `d01-r1-v05`: hỏi 29 ký tự → trả lời 182 ký tự, `missing_context = true`. *(M4)*
4. `C00992` — 08/11, dưới video `d02-r2-v01`: hỏi 34 ký tự → trả lời 298 ký tự, `missing_context = true`. *(M4)*
5. `C00581` — 05/11, dưới video `d01-r1-v02`: hỏi 82 ký tự; trong 5 phút sau câu trả lời hỏi tiếp cùng video. *(M5)*
6. `C00499` — 05/11, cùng video `d01-r1-v02`: hỏi 183 ký tự; lại hỏi tiếp trong 5 phút. *(M5)*

Trả lời nguyên văn khảo sát (số phiếu theo thứ tự thời gian trong `evidence/survey/results.csv`):

- "độ chính xác và nguồn rõ ràng của câu trả lời" — phiếu 12, câu 9 (điều muốn cải thiện nhất)
- "giải thích giúp tôi khái niệm này." — phiếu 21, câu 8 (câu từng hỏi trợ giảng)
- "Không cần cải thiện gì thêm" — phiếu 21, câu 9

Trích nguyên văn phỏng vấn (1–2 câu / người):

7. "Mình hiểu ý chính và xem tiếp video, nhưng vẫn chưa rõ vì sao không đưa hết tài liệu vào một prompt." — P1
8. "Mình đang hỏi cụ thể ai xem bản nháp và duyệt trước lúc gửi, nhưng câu trả lời không nói đến bước đó. Mình tua lại video để tìm ví dụ." — P2
9. "Mình vẫn không rõ tiêu chí đánh giá phải được đặt ra từ đầu hay chỉ bắt đầu nghĩ đến lúc có bản thử. Mình đọc rồi học tiếp, để câu đó lại." — P3

## 4. Các nguồn có khớp nhau không

**Data nói:** 40,1% câu trả lời của trợ giảng không kèm mốc nào trong bài giảng, rơi vào 67,4% người nhận trả lời; nhưng sau câu trả lời không có mốc, học viên **không** hỏi tiếp hay tua lùi nhiều hơn (50,6% so với 55,2%; tua lùi còn thấp hơn: 5,2% so với 14,1%). Câu trả lời không có mốc đi kèm câu hỏi thiếu ngữ cảnh nhiều hơn hẳn (16,0% so với 0,3%). Độ trễ thấp (trung vị 2,4 s) nên giả thuyết thay thế 4 (vấn đề là thời gian phản hồi) không được ủng hộ.

**Người dùng nói (khảo sát, n = 20):** khó xác định đoạn căn cứ là chuyện **hay gặp** (15/20 thường xuyên hoặc thỉnh thoảng), mỗi lần thường mất thêm 2–10 phút. Nhưng đó **hiếm khi là khó khăn lớn nhất** (2/20). Khó khăn lớn nhất hay được chọn là câu trả lời **không giải quyết đúng câu hỏi** (7/20). Khi chưa kiểm chứng được, 12/20 người chuyển sang công cụ AI khác, chỉ 1/20 tua lại video. Điều này khớp với data: sau câu trả lời không có mốc, tua lùi chỉ 5,2%. Học viên không quay lại bài giảng để kiểm mà rời trợ giảng đi hỏi chỗ khác.

**Người dùng nói (phỏng vấn, n = 3):**
- (a) **Có cần biết đoạn căn cứ không:** P2 và P3 cần, vì phải tự tìm lại đoạn đó trong video. P1 không cần ngay ("cần hiểu ý chính để đi tiếp").
- (b) **Khi không có thì làm gì, mất bao lâu:** P1 hỏi công cụ AI khác (5 phút). P2 tua lại video (khoảng 10 phút). P3 bỏ qua; về sau, khi tự lập kế hoạch cho một bản thử, phải quay lại tìm đoạn (10–13 phút).
- (c) **Tua lùi ít có phải vì bỏ qua không:** có, ở P3. P3 bỏ qua, chỉ nhận ra mình chưa hiểu đủ khi cần dùng kiến thức đó. P1 thì đi kiểm ở công cụ ngoài, nên data trợ giảng không thấy.
- **"Không giải quyết đúng câu hỏi" nghĩa là gì:** ở P2 và P3, trợ giảng trả lời **chung chung** (nêu định nghĩa, liệt kê giai đoạn) mà không trả lời ý cụ thể được hỏi. Không ai nói trợ giảng trả lời sai; P3 nói rõ là không khẳng định trợ giảng sai.

**Khớp / lệch, vì sao:** Data chỉ cho biết phản hồi không có mốc là phổ biến; data **không** cho thấy học viên mất thêm công vì thiếu mốc. Hai cách đọc: (1) học viên không cần mốc → pain yếu; (2) không có mốc thì học viên không có chỗ để tua tới nên bỏ qua, không kiểm → hiểu sai mà không biết. Khảo sát nghiêng về cách đọc (2), nhưng ở dạng khác: học viên không bỏ qua mà **ra ngoài kiểm** (12/20 dùng AI khác). Khảo sát cũng cho thấy một vấn đề lớn hơn thiếu mốc, là câu trả lời **lệch câu hỏi** (7/20). Mốc trích dẫn không tự sửa được lỗi lệch câu hỏi, nhưng giúp học viên thấy ngay câu trả lời dựa trên đoạn nào để biết nó có lệch không. Phỏng vấn ủng hộ cách đọc (2) và giải thích vì sao data không thấy hậu quả. Việc kiểm diễn ra **ngoài tầm nhìn của data**: P1 kiểm ở công cụ AI khác, P3 quay lại tìm đoạn muộn hơn nhiều so với cửa sổ 5 phút của `citation_check.py`. Chỉ P2 tua lại ngay. Phỏng vấn cũng cho biết "lệch câu hỏi" trong khảo sát chủ yếu là trả lời **chung chung**. Hai vấn đề đi cùng nhau: câu trả lời chung chung và không có đoạn căn cứ, nên học viên không tự kiểm được nó có trúng ý không.

## 5. Kết luận

Giả thuyết ở `evidence/hypothesis.md`: **đúng** theo cả hai tiêu chí đặt trước, kèm một điều chỉnh về cách hiểu pain (dòng cuối danh sách dưới).

- Tiêu chí data (≥20% phản hồi không có `moc_trich_dan`): **đạt** — 231/576 (40,1%); độ nhạy 194/538 (36,1%).
- Tiêu chí phỏng vấn (≥2/3 người kể được tình huống cụ thể trong tháng qua): **đạt — 3/3**. P1 chỉ được tính nhờ vế "đi kiểm ở chỗ khác" của quy tắc; không tính P1 thì vẫn 2/3.
- Phần hậu quả ("phải tua lại, hỏi tiếp hoặc tìm nguồn khác"): data **không** thấy (tỉ lệ hỏi tiếp / tua lùi trong 5 phút không cao hơn khi thiếu mốc), nhưng phỏng vấn cho thấy hậu quả nằm ngoài tầm data: hỏi công cụ khác (P1), bỏ qua rồi quay lại muộn (P3). Chỉ P2 tua lại ngay.
- Khảo sát (n = 20, người ngoài nhóm): pain **có thật nhưng không lớn nhất**. 15/20 gặp khó xác định đoạn căn cứ, mỗi lần thường mất 2–10 phút, nhưng chỉ 2/20 coi đó là khó khăn lớn nhất. Vế "tìm nguồn khác" của giả thuyết được ủng hộ: 12/20 dùng công cụ AI khác. Vế "tua lại" thì không: 1/20.
- Khó khăn lớn nhất theo khảo sát là câu trả lời **không giải quyết đúng câu hỏi** (7/20). Đây không phải pain đang chọn. Phỏng vấn cho thấy ý này chủ yếu là trả lời **chung chung**, không phải trả lời sai.
- Giả thuyết thay thế 4 (thời gian phản hồi): **không được ủng hộ** — M7 trung vị 2,4 s.
- Giả thuyết thay thế 2 (câu hỏi thiếu ngữ cảnh) có tín hiệu: thiếu mốc trùng với thiếu ngữ cảnh. MVP vẫn giữ bước hỏi lại khi mơ hồ.
- **Điều chỉnh:** giữ pain và lát cắt A1.1, nhưng hiểu rõ hơn: pain gây tốn thời gian khi câu trả lời **chung chung** và **không có đoạn căn cứ** cùng lúc (P2, P3). Không có đoạn thì học viên không biết câu trả lời có trúng ý không, cũng không biết tua về đâu. Hệ quả cho MVP: chỉ trả lời khi đoạn truy xuất trả lời đúng ý được hỏi, còn lại hỏi rõ hoặc từ chối. Hệ quả cho bộ câu thử: thêm câu hỏi cụ thể kiểu P2, P3 (đáp án chung chung = trượt). Ghi ở `spec.md` §10.

Quy tắc chốt (ghi trước khi đọc ghi chép phỏng vấn):
- ≥3/4 người kể được lần cụ thể muốn biết đoạn nào là căn cứ hoặc phải tự tìm lại → giữ A1.1, ghi **đúng**.
- 2/4 → giữ A1.1 nhưng ghi **phải đổi**: nhấn vào "kiểm chứng được", T lấy theo số người kể.
- ≤1/4 → ghi **sai**; xét chuyển trọng tâm sang A1.2 (hỏi lại khi mơ hồ), ghi lý do ở `spec.md` §10.
- Chỉ phỏng vấn được 3 người nên dùng quy tắc n = 3 ở `evidence/interviews/kich-ban.md` (viết trước cuộc phỏng vấn đầu tiên): ≥2/3 → **đúng**, theo ngưỡng của `hypothesis.md`.

**Điều vẫn chưa biết:** bao nhiêu trong 9,18 câu trả lời không có mốc / người / tháng thực sự làm mất thời gian. P1 cho thấy không phải lần nào cũng mất, nên Impact ở `spec.md` §2 (mỗi lần × 10 phút) là **cận trên**. T = 10 phút lấy từ 3 người, mỗi người kể 1 lần họ còn nhớ. Data không có câu chữ nên vẫn không kết luận được trợ giảng trả lời sai.

## Lịch hẹn (dùng cho CP2 — chỉ ghi vai và giờ, không tên)

| Vai | Giờ hẹn | Đã xong? |
|---|---|---|
| P1 · học viên AI20K K5 | | ☑ |
| P2 · học viên AI20K K5 | | ☑ |
| P3 · học viên AI20K K5 | | ☑ |
| P4 | không làm | — |
