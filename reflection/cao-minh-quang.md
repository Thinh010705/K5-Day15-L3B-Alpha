# Reflection — Cao Minh Quang

> TV3 — AI Engineer / Backend Lead. Theo guide 5.3.

1. **Vai trò + phần mình làm (trỏ tới file / commit):**
   Mình phụ trách bản chạy thử LessonLens: luồng cố định chặn trước → `search_lesson` → `get_passage` → model trả JSON → kiểm mã nguồn.
   - Code ở `codebase/agent.py`, `codebase/tools.py`, `codebase/ai.py`. Nối model thật qua OpenRouter (`nvidia/nemotron-3-ultra-550b-a55b:free`), chạy `eval --try` và `simulate --try`, quay video 30 giây.
   - Kho 11 đoạn viết lại từ slide AI20K (`data/lesson_product_ai20k.json`), đối chiếu 11/11 với PDF và sửa câu chữ SL-19, SL-30 (PR #20).
   - Spec §4 (sơ đồ khớp code, PR #17, #32) và §9 Rủi ro & an toàn (PR #31).
   - Cải tiến lượt 2 cho nhóm lỗi B18 (PR #24), chạy `run-3` (PR #25): 26/30 → 28/30, đạt chuẩn. Chạy `simulate-2` 50/50 phiên sau khi `simulate-1` lỗi 429 (PR #36). Chấm độc lập 5 đầu ra `run-3`, khớp 4/5 (`eval/grading-run3.md`).

2. **AI hỗ trợ mình thế nào (việc gì, công cụ gì, chỗ nào phải sửa lại output AI):**
   - Codex viết khung CP2 của ba file code và prompt `SYSTEM`; Claude Code thêm nhánh OpenRouter, bước chặn câu mơ hồ, bản sửa B18, các lượt chạy và phần lớn câu chữ spec. Mình chọn lát cắt, hình dạng workflow, nhà cung cấp model và nhóm lỗi để sửa; đọc lại ba file code (`docs/ai-usage.md`).
   - Chỗ phải sửa: bản Codex chặn câu mơ hồ bằng độ dài (`len < 8`) nên câu "Cái đó là gì vậy?" lọt qua → đổi sang kiểm câu chỉ có đại từ / từ đệm. Bản đầu luật B18 bắt nhầm câu ngoài bài "Lịch nộp bài tuần trước đó…" thành câu hỏi lại → siết điều kiện trước khi chạy `run-3`.
   - AI cũng ghi sai trong khai báo (ghi đã thử 14 câu với model thật, thực tế 6; sai ngày) và đoán sai hạn mức OpenRouter (50 lượt/ngày, thực tế 1000 với tài khoản có nạp tiền) — mình kiểm lại bằng số thật rồi mới giữ.

3. **Một câu thử trượt của nhóm và mình học được gì từ nó:**
   - B18 "Bạn giải thích tiếp ý ở đoạn vừa rồi được không?" trượt ở cả `run-1` và `run-2`: trợ giảng không có lịch sử hội thoại nhưng vẫn gọi model, model tự đoán hai khái niệm (FDE, Who–What–How) và hỏi lại kèm hai lựa chọn đó.
   - Bài học: thứ hệ thống *không biết* (ở đây là lượt trước) phải được chặn bằng code trước khi tới model; prompt "nếu mơ hồ thì hỏi lại" không đủ vì model vẫn cố tỏ ra hữu ích bằng cách đoán. Sau khi sửa, B18 đạt và nhóm làm rõ lên 3/3.
   - Bài học thứ hai: B03 cũng chuyển sang đạt ở `run-3` nhưng không nhờ bản sửa — model trả lời khác giữa các lần chạy. Một lượt chạy chưa đủ để kết luận một câu đã "được sửa"; muốn chắc phải chạy nhiều lần mỗi câu.
