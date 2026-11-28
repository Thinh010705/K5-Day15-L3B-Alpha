# Reflection — Hoàng Minh Quyền

> TV2 — Data & Research Lead. Theo guide 5.3 và kế hoạch nhóm (Final · Reflection cá nhân). Hạn 23:59 Thứ Bảy 28/11.

1. **Vai trò + phần mình làm (trỏ tới file / commit):**
   - Đào data pre-class BTC để chứng minh pain bằng số. Chuẩn hoá data (`evidence/prepare_data.py`, PR #1) → viết cách đếm **trước khi chạy** (`evidence/data-mining.md` §1, PR #2) → script đếm chạy lại được + test (`evidence/count.py`, `evidence/tests/`, PR #3).
   - Số chính: **231/576 (40,1%)** câu trả lời của trợ giảng không có mốc trích dẫn, rơi vào **58/86 người**. Từ đó ra N, F cho bảng Impact ở `spec.md` §2 (PR #4, #6).
   - Data Card (`data/DATA_CARD.md`, PR #5). Persona chi phí lấy từ data (`cost/personas.yaml`, PR #8). Giá model + mô phỏng chi phí (PR #33). Rà lại Impact và nguồn số (PR #34).
   - Sửa logic theo kế hoạch gốc: PR #9, #10, #12.

2. **AI hỗ trợ mình thế nào (việc gì, công cụ gì, chỗ nào phải sửa lại output AI):**
   - Claude Code (Claude Opus 5.5) viết script, test, bản nháp tài liệu; chạy đếm; kiểm chéo M1, M4 bằng một cách đếm độc lập (`docs/ai-usage.md`).
   - Chỗ phải sửa output AI:
     - M2 ban đầu đếm mọi lần bấm link, không chỉ link vào video được trích (sửa ở PR #9). Sau đó bỏ hẳn vì không có trong cách đo của kế hoạch §5.1 (PR #12).
     - AI ghi persona V3 là "đặt trước", trong khi cách chia được chọn sau khi xem data → sửa lại.
     - AI tự thêm đề xuất ngoài kế hoạch (chọn bài / video cho TV3, gợi ý câu thử cho TV4). TV3 hỏi nguồn thì mới thấy → bỏ ở PR #12.
   - Kiểm tay: __ *(Quyền điền: số dòng đã tự đối chiếu với data, khớp bao nhiêu — cùng số ở `docs/ai-usage.md`)*

3. **Một câu thử trượt của nhóm và mình học được gì từ nó:**
   - Câu: __ *(Quyền chọn một câu trượt).* Sự kiện để đối chiếu: B18 "Giải thích tiếp ý đoạn vừa rồi" trượt ở `run-1` và `run-2`. Model tự đoán khái niệm (FDE / Who–What–How) thay vì hỏi lại (`eval/report.md` §2). Data có dạng câu này: 100/1.138 lượt (8,8%) trợ giảng ghi thiếu ngữ cảnh (M4).
   - Mình học được: __ *(Quyền tự viết, 3–6 dòng)*
