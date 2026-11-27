# Khảo sát trải nghiệm trợ giảng dưới video pre-class AI20K

- **Hình thức:** Google Form, ẩn danh. Form không thu tên, email, SĐT hay mã học viên.
- **Kênh gửi:** [CẦN ĐIỀN: nhóm lớp nào]
- **Phiếu nhận:** 22 phiếu, phiếu đầu 27/11/2026 14:35, phiếu cuối 21:15 (GMT+7). Giờ chốt form: [CẦN ĐIỀN]
- **Người trả lời là người ngoài nhóm:** [CẦN XÁC NHẬN]
- **Kết quả:** `results.csv` là bản xuất nguyên từ form. Bản này chỉ có dấu thời gian và câu trả lời, không có cột nhận ra người trả lời.
- **Đếm:** `python evidence/survey/tally.py`

## Câu hỏi

| # | Câu hỏi | Kiểu trả lời |
|---|---|---|
| 1 | Bạn có sử dụng trợ giảng dưới video trong 30 ngày qua không? | Có · Không |
| 2 | Trong 30 ngày qua, bạn đã sử dụng trợ giảng dưới video khoảng bao nhiêu lần? | 1–2 · 3–5 · 6–10 · 11–20 · trên 20 lần |
| 3 | Bạn có từng gặp khó khăn khi xác định đoạn bài giảng làm căn cứ cho câu trả lời của trợ giảng không? | Thường xuyên · thỉnh thoảng · hiếm khi · chưa bao giờ · không nhớ |
| 4 | Mỗi lần gặp khó khăn đó, bạn mất thêm trung bình bao nhiêu phút? | Dưới 2' · 2–10' · 10–15' · 15–30' · trên 30' |
| 5 | Khi chưa hiểu hoặc chưa kiểm chứng được câu trả lời, bạn thường làm gì? | Chọn một (công cụ AI khác · Google · tua lại video · hỏi lại trợ giảng · hỏi bạn bè · bỏ qua) |
| 6 | Trong lần gần nhất sử dụng trợ giảng, câu trả lời có giúp bạn hiểu nội dung cần học không? | Hiểu phần lớn · chỉ hiểu một phần · không giúp ích · cảm thấy khó hiểu hơn |
| 7 | Khó khăn lớn nhất của bạn khi sử dụng trợ giảng dưới video là gì? | Chọn một |
| 8 | Bạn có thể viết lại một câu hỏi về kiến thức mà bạn từng hỏi hoặc muốn hỏi trợ giảng không? | Đoạn văn, không bắt buộc |
| 9 | Nếu chỉ được cải thiện một điểm của trợ giảng, bạn ưu tiên điều gì? | Đoạn văn, không bắt buộc |

## Giới hạn của form (ghi để đọc số cho đúng)

- **Không có logic bỏ câu sau câu 1.** 2 người trả lời "Không" ở câu 1 vẫn trả lời các câu sau. Số chính chỉ tính 20 phiếu trả lời "Có".
- **Câu 4 hỏi tất cả mọi người**, kể cả người chọn "Chưa bao giờ" hay "Hiếm khi" ở câu 3. Ví dụ có 1 phiếu chọn "Chưa bao giờ" mà vẫn chọn "15–30 phút".
- **Câu 3 hỏi "có từng gặp khó khăn"**, chưa hỏi về lần gần nhất, nên dễ được trả lời "Thỉnh thoảng".
- **Câu 5 và câu 7 chỉ cho chọn một.** Người gặp nhiều khó khăn chỉ ghi được khó khăn họ coi là lớn nhất.
- **Câu 8 và câu 9 không bắt buộc.** Chỉ 2 phiếu có nội dung ở câu 8, nên khảo sát chưa cho câu hỏi thật nào dùng được cho bộ câu thử.
