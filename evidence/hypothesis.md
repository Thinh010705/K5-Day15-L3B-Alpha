# Giả thuyết — viết TRƯỚC khi tìm bằng chứng (5 phút, commit ngay)

> Điền ở guide bước 1.1. Ôn lại: ngày 2 · lab ngày 2.
> Viết **trước** khi đọc dòng data đầu tiên hay hỏi người đầu tiên, để không sửa cho khớp kết quả. Kết quả ngược giả thuyết vẫn đủ điểm nếu số là thật.

- Ngày giờ viết: 27/11/2026
- Người dùng chính: Học viên AI20K K5 đang sử dụng trợ giảng AI dưới video pre-class.

- Mình nghĩ: Một bộ phận học viên gặp khó khi kiểm chứng câu trả lời của trợ giảng với nội dung bài học vì câu trả lời có thể chưa chỉ rõ đoạn kiến thức làm căn cứ. Hậu quả là học viên phải tua lại video, hỏi tiếp hoặc tìm nguồn khác, làm tăng thời gian học và có nguy cơ hiểu sai.

- Có thể còn cách giải thích khác:
  1. Nội dung bài học khó hoặc chưa rõ ràng.
  2. Câu hỏi học viên thiếu ngữ cảnh.
  3. Trợ giảng đã có nguồn nhưng học viên chưa biết cách sử dụng.
  4. Vấn đề chính nằm ở thời gian phản hồi thay vì khả năng kiểm chứng.

- Mình đúng nếu thấy:
  1. Ít nhất 2/3 người được phỏng vấn kể được một tình huống cụ thể trong tháng qua mà họ không thể kiểm chứng câu trả lời hoặc phải tìm lại nội dung bài học.
  2. Ít nhất 20% phản hồi của trợ giảng trong tập dữ liệu được chọn không có mốc trích dẫn (`moc_trich_dan`) theo cách đếm đã định nghĩa.

  Đây là ngưỡng kiểm chứng do nhóm đề xuất, không phải ngưỡng bắt buộc của BTC. Phải giữ nguyên sau khi bắt đầu xem kết quả.

- Nguồn sẽ dùng:
  - [x] Đào data: `data/preclass/chat.csv` + `data/preclass/events.csv`.
  - [x] Phỏng vấn ít nhất 3 học viên ngoài nhóm, mục tiêu 4 người.
  - [ ] Khảo sát: chỉ thực hiện nếu còn đủ thời gian.

- Nguồn chính: Data mining từ nhật ký tương tác trợ giảng.
- Nguồn để kiểm lại: Phỏng vấn học viên P1–P4.
