# Reflection — Nguyễn Năng Thịnh

> TV1 — Đội trưởng, Product Lead. Theo guide 5.3 và kế hoạch nhóm (Final · Reflection cá nhân).

1. **Vai trò + phần mình làm (trỏ tới file / commit):**
   - Mình chốt người dùng, pain, lát cắt và điều phối nhóm theo từng checkpoint.
   - **CP3** (PR #22, #26–#29):
     - Viết `evidence/summary.md` từ ba nguồn: data, khảo sát 20/22 phiếu hợp lệ, phỏng vấn P1–P3.
     - Viết `evidence/citation_check.py`. Kết quả ngược giả thuyết: thiếu mốc không làm học viên hỏi tiếp hay tua lùi nhiều hơn (50,6% so với 55,2%).
     - Chốt giả thuyết **đúng** (3/3), điền `spec.md` §0–§2, Impact 88,7 giờ / tháng (cận trên).
   - **CP4** (PR #39): 3 persona khớp P1–P3, quy mô 144 / 436 / 721. Kết luận **Go — thí điểm ở một bài** (`cost/cost-estimate.md` §3), sửa và dựng lại `demo-slides.pdf`.

2. **AI hỗ trợ mình thế nào (việc gì, công cụ gì, chỗ nào phải sửa lại output AI):**
   - Mình dùng Claude Code (Claude Opus 5.5) để viết script kiểm chéo, đếm khảo sát, soạn kịch bản phỏng vấn, viết nháp `summary.md`, `spec.md`, `cost-estimate.md` và dựng slide.
   - Mình đọc lại mọi thay đổi trước khi commit. Mình tự điền những gì AI không biết: kênh khảo sát, giờ phỏng vấn, xác nhận người ngoài nhóm, ảnh chụp màn hình.
   - Chỗ phải sửa:
     - Số đầu tiên AI tính lệch với TV2 (557 so với 576 lượt; F trung vị so với trung bình). Mình chỉ dùng số của `evidence/count.py`.
     - AI đề xuất quy mô 721 / 1.000 trước khi kiểm `simulate-2`, nên sẽ lệch bảng chi phí. Mình bỏ đề xuất đó.

3. **Một câu thử trượt của nhóm và mình học được gì từ nó:**
   - Câu B14 "Slide nêu ba năng lực nào cần rèn đối với kỹ sư AI?" trượt ở `run-3`. Câu trả lời đủ ba ý và ghi đúng `SL-30`, nhưng lặp lại tiền đề sai: slide 30 nói về **sinh viên kỹ thuật**, không phải kỹ sư AI.
   - Pain mình chọn là "không có đoạn căn cứ thì học viên không tự kiểm được". B14 cho thấy có mã đoạn là **cần nhưng chưa đủ**: thấy `SL-30` đúng, học viên dễ tin luôn phần sai.
   - Vì vậy kết luận Go chỉ là thí điểm, và thí điểm phải đo tỉ lệ đúng nội dung trên câu hỏi thật, không chỉ đếm câu có mã nguồn. Lần sau, khi viết pain, mình sẽ ghi ngay từ đầu những gì giải pháp **không** chặn được.
