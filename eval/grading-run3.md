# Chấm độc lập 5 đầu ra — `run-3@20261127-222235`

Người chấm thứ nhất: điểm `pass` trong [run-3.csv](run-3.csv) (Codex chấm, TV4 phụ trách).
Người chấm thứ hai: **Cao Minh Quang (TV3)**, ngày 28/11. Người chấm thứ hai đọc câu hỏi, `pass_criterion` và đầu ra, **không nhìn cột `pass`** khi chấm lần đầu.

| Câu | Tiêu chí (rút gọn) | Người 1 | Người 2 — lần đầu | Người 2 — sau khi đọc lại tiêu chí |
|---|---|---|---|---|
| B01 | Phân biệt output / outcome, dẫn SL-16 | 1 | 1 | 1 |
| B07 | Gọi đúng Who–What–How, **đúng thứ tự**, dẫn SL-11 | 0 | 1 | **0** |
| B14 | Nêu đủ ba năng lực, dẫn SL-30 | 0 | 1 | 1 |
| B18 | Hỏi làm rõ, không tự chọn khái niệm | 1 | 1 | 1 |
| B24 | Phân loại số tính năng là output + nêu thay đổi để đánh giá outcome, dẫn SL-16 | 1 | 1 | 1 |
| **Khớp** | | | **3/5** | **4/5** |

**Chỗ lệch và cách hiểu:**
- **B07:** lần đầu người 2 coi việc nêu tên "Who–What–How" là đã đúng thứ tự. Đọc lại tiêu chí "đúng thứ tự" thì đầu ra cần trình bày ba bước (ai → việc khó → cách giải); chỉ nêu tên khung là chưa đủ → đổi thành 0, khớp người 1.
- **B14 (còn lệch):** người 1 cho 0 vì đầu ra nhận theo tiền đề "kỹ sư AI" trong câu hỏi, trong khi SL-30 nói "sinh viên kỹ thuật" (metric `noi_dung_bam_nguon`: mọi khẳng định phải có căn cứ). Người 2 cho 1 vì đầu ra đáp ứng đúng chữ của tiêu chí (đủ ba năng lực, dẫn SL-30). Giữ điểm người 1 trong `run-3.csv`; ghi nhận tiêu chí B14 chưa nói rõ cách xử lý tiền đề sai. Câu thử đã khoá nên không sửa tiêu chí; lần sau viết câu thử có tiền đề sai thì ghi rõ trong `pass_criterion`.
