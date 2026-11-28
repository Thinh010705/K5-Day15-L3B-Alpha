# Chi phí khi dùng thật

## 1. Đầu vào

- 3 persona từ 144 người từng hỏi trợ giảng trong 21 ngày. Phiên/người/tháng lần lượt là 1,4 · 3,4 · 8,9. Tỉ trọng là 52,1% · 33,3% · 14,6%. Xem [personas.yaml](personas.yaml) và [kết quả đếm V3](../evidence/data-mining.md).
- Thấp 144 người từng hỏi, cơ sở 436 người có hoạt động, cao 721 tài khoản. Nguồn là log pre-class 05–25/11/2026 (P0–P2).
- Token do API Nemotron qua OpenRouter báo. Hai cột giá dùng mức Standard của Gemini 3.1 Flash-Lite và Gemini 2.5 Pro. Giá được áp vào lượng token Nemotron, nên chi phí của hai model Gemini là ước tính và số token có thể thay đổi nếu gọi trực tiếp. [Giá Gemini Developer API, xem 28/11/2026](https://aistudio.google.com/docs/pricing).
- Tỉ lệ đạt dùng tính chi phí là 28/30 (93,3%), lấy từ `run-3@20261127-222235` (chấm sơ bộ).

## 2. Kết quả

Lượt đo API trực tiếp [`simulate-1.csv`](simulate-1.csv), mã `simulate-1@20261128-092259`, 50 phiên, seed 42. OpenRouter hết hạn mức ngày và trả HTTP 429 ở 34/50 phiên. Bảng lấy trung bình trên 16 phiên hợp lệ, trong đó chỉ có một phiên của persona dùng nhiều. Xem [bảng gốc](simulate-1-summary.md).

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (144 người) | Chi phí / tháng — cơ sở (436 người) | Chi phí / tháng — cao (721 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| gemini-3.1-flash-lite (vào 0.25 · ra 1.5 $/1M) | $0.0019 | $0.0021 | $0.00060 | $0.9626 | $2.91 | $4.82 | $0.0067 |
| gemini-2.5-pro (vào 1.25 · ra 10.0 $/1M) | $0.0124 | $0.0132 | $0.0039 | $6.15 | $18.61 | $30.77 | $0.0427 |

Theo quy ước của khung, chi phí / task thành công lấy chi phí trung bình mỗi phiên chia cho tỉ lệ đạt của bộ thử. Cột chi phí / câu hỏi đạt chia thêm cho số lượt hỏi trung bình mỗi phiên.

Để kiểm độ nhạy, [lấy mẫu lại 50 phiên](replay-run-3-cp4.csv) bằng token API của các câu trong [Run 3](../eval/run-3.csv), cùng seed 42. Ở 436 người, phép tính này cho $2.69/tháng với Flash-Lite và $17.16/tháng với Pro. Mỗi câu dùng lại một lần đo token từ Run 3 nên phép tính này chưa phản ánh độ biến động khi gọi API nhiều lần.

## 3. So với impact

Cận trên của pain là 91,8 phút/tháng với mỗi học viên gặp vấn đề và 88,7 giờ/tháng trên 58 học viên trong tập log. Ở kịch bản cơ sở 436 người, chi phí model là $0.0067/người/tháng với Flash-Lite hoặc $0.0427/người/tháng với Pro. Đáng thử trên một bài có mốc nguồn để đo thời gian thực sự tiết kiệm được. Bảng hiện tính phần model. Chi phí tích hợp, vận hành và duyệt nội dung cần đo thêm.
