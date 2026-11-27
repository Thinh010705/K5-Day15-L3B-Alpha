# Canvas — Alpha · Track A

| # | Dòng | Nhóm điền |
|---|---|---|
| 1 | Track + lát cắt dự kiến | Track A – EdTech, hướng A1 – Tutor cho LMS và trang pre-class. Lát cắt dự kiến: hỗ trợ học viên kiểm chứng câu trả lời bằng đoạn kiến thức tương ứng trong bài học. |
| 2 | Người dùng chính | Học viên AI20K K5 đang xem video pre-class và sử dụng trợ giảng dưới video khi gặp khái niệm chưa hiểu. |
| 3 | Pain một câu | Khi gặp một khái niệm chưa hiểu trong video pre-class, học viên phải tua lại hoặc hỏi thêm để tìm lời giải thích; nếu câu trả lời không chỉ rõ đoạn bài học làm căn cứ, họ khó tự kiểm chứng và mất thêm thời gian. |
| 4 | Bằng chứng đầu | Đào data pre-class BTC (13/11 → 25/11/2026): **231/576 lượt (40.1%)** trợ giảng trả lời không có mốc trích dẫn, vượt ngưỡng 20% đặt trước trong `evidence/hypothesis.md`; **58/86 người (67.4%)** nhận ít nhất 1 lần. Cách đếm và script: `evidence/data-mining.md`, `evidence/count.py`. Phỏng vấn ≥3 học viên ngoài nhóm đang làm. |
| 5 | Lát cắt MỘT CÂU | Một học viên AI20K đang xem video pre-class đặt một câu hỏi về nội dung bài → LessonLens truy xuất đoạn kiến thức liên quan và quyết định liệu bằng chứng có đủ để trả lời hay không → trả lời kèm mã đoạn nguồn nếu đủ căn cứ, hoặc từ chối nếu không đủ → học viên có thể tự kiểm chứng. |
| 6 | AI tự làm đến đâu + 1 dòng lý do | AI chỉ trả lời khi có đoạn nguồn đủ căn cứ, hỏi lại tối đa một lần khi câu hỏi mơ hồ và từ chối khi không tìm thấy nguồn phù hợp; không tự chấm điểm hoặc làm bài thay học viên vì câu trả lời sai có thể khiến người học hiểu sai kiến thức. |
| 7 | Phân công có tên | Nguyễn Năng Thịnh – Đội trưởng/Product Lead: quản lý sản phẩm và nghiên cứu người dùng; Hoàng Minh Quyền – Data & Research Lead: đào data, bằng chứng và Impact; Cao Minh Quang – AI Engineer / Backend Lead: thiết kế workflow và triển khai bản chạy thử; Nguyễn Quang Dũng – Evaluation & QA: benchmark và kiểm thử. |
| — | (CP2) Đã đổi gì so với CP1 | (1) Nguồn kiến thức cho bản chạy thử: chưa có transcript video pre-class nên dùng 11 đoạn viết lại từ slide AI20K *Tư duy Product cho người làm công nghệ thời đại AI*, mã `SL-<trang>`; lát cắt giữ nguyên, câu trả lời dẫn mã đoạn và trang slide. (2) Bằng chứng đầu chuyển từ giả thuyết sang số đào data (dòng 4). (3) Đổi vai Quang ↔ Quyền cho khớp `TEAMS.md`; đã có bộ 12 câu thử, 3 metric và chuẩn "đạt" ở `spec.md` §7. |
