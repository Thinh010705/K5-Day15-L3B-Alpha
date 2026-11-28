# Reflection — Hoàng Minh Quyền

> TV2 — Data & Research Lead. Theo guide 5.3 và kế hoạch nhóm (Final · Reflection cá nhân).
> **BẢN NHÁP do Claude Code soạn từ lịch sử repo — Quyền sửa lại bằng lời của mình và xoá dòng này trước khi merge.**

1. **Vai trò + phần mình làm (trỏ tới file / commit):**
   Mình phụ trách đào data pre-class BTC để chứng minh pain bằng số.
   - Trước tiên mình chuẩn hoá data (`evidence/prepare_data.py`, PR #1). Data gốc có BOM, CRLF và ô thừa khoảng trắng; đã kiểm số dòng 7/7 file khớp README BTC.
   - Sau đó mình viết cách đếm **trước khi chạy** (`evidence/data-mining.md` §1, PR #2) và script chạy lại được kèm 29 test (`evidence/count.py`, PR #3).
   - Số chính: **231/576 (40,1%)** câu trả lời của trợ giảng không có mốc trích dẫn, rơi vào 58/86 người. Từ đó ra N, F cho Impact 88,7 giờ / tháng ở `spec.md` §2 (PR #4, #6).
   - Mình làm thêm Data Card (PR #5), persona chi phí từ data (`cost/personas.yaml`, PR #8), kịch bản cao 1.000 người (PR #37), rà lại Impact (PR #34). Mình cũng sửa và cắt phần thừa theo kế hoạch gốc (PR #9, #10, #12).

2. **AI hỗ trợ mình thế nào (việc gì, công cụ gì, chỗ nào phải sửa lại output AI):**
   - Mình dùng Claude Code (Claude Opus 5.5) để viết script, test, bản nháp tài liệu, chạy đếm, và kiểm chéo M1, M4 bằng một cách đếm độc lập.
   - Chỗ phải sửa:
     - M2 ban đầu đếm mọi lần bấm link thay vì chỉ link vào video được trích (PR #9).
     - Persona V3 bị ghi là "đặt trước" dù cách chia được chọn sau khi xem data.
     - Nặng nhất: AI tự thêm đề xuất ngoài kế hoạch, như chọn bài Day01 cho TV3 và gợi ý câu thử cho TV4. Khi Quang hỏi "cái này nằm ở đâu trong kế hoạch" mình mới thấy, rồi bỏ hết ở PR #12.
   - Từ đó mình đặt luật: thêm mục nào cũng phải trỏ được về một dòng trong kế hoạch hoặc một con số trong data.
   - Kiểm tay: __ dòng, khớp __ *(Quyền điền)*.

3. **Một câu thử trượt của nhóm và mình học được gì từ nó:**
   - Câu B18 "Giải thích tiếp ý đoạn vừa rồi" trượt ở cả `run-1` và `run-2`. Trợ giảng không biết "đoạn vừa rồi" là đoạn nào nên tự đoán, đưa ra hai lựa chọn FDE (SL-06) và Who–What–How (SL-11), thay vì hỏi lại người học muốn hỏi khái niệm nào (`eval/report.md` §2). TV3 thêm luật chặn câu chỉ nhắc lượt trước (PR #24) và B18 đạt ở `run-3`.
   - Điều mình học: dạng lỗi này **đã có sẵn trong data của mình** từ CP2. 100/1.138 lượt (8,8%) trợ giảng thật ghi câu hỏi thiếu ngữ cảnh (M4), và 37/231 câu trả lời không có mốc đi kèm câu hỏi thiếu ngữ cảnh. Nhưng mình chỉ báo con số, chưa biến nó thành câu thử hay quy tắc cho luồng sớm. Vì vậy lỗi phải đợi đến lượt 1 mới lộ ra.
   - Lần sau, mỗi con số pain mình tìm ra sẽ đi kèm ít nhất một câu thử cụ thể bàn giao cho người làm benchmark. Đúng như kế hoạch dặn: "không để TV2 chỉ thống kê".
