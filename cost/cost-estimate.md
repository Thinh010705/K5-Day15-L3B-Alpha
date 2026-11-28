# Chi phí khi dùng thật

## 1. Đầu vào

- 3 persona từ 144 người từng hỏi trợ giảng trong 21 ngày. Phiên/người/tháng lần lượt là 1,4 · 3,4 · 8,9. Tỉ trọng là 52,1% · 33,3% · 14,6%. Xem [personas.yaml](personas.yaml) và [kết quả đếm V3](../evidence/data-mining.md).
- Ba persona (TV1 mô tả, mỗi persona gần với một người phỏng vấn):

  | Persona | Tỉ lệ | Phiên / tháng | Là ai | Gần với |
  |---|---|---|---|---|
  | `dung_it` | 75/144 (52,1%) | 1,4 | Hỏi khi gặp một chỗ không hiểu rồi xem tiếp | P1: 1–2 lần / tháng, chưa chắc thì hỏi AI khác (5 phút) |
  | `dung_vua` | 48/144 (33,3%) | 3,4 | Hỏi vài lần mỗi tuần học, câu trả lời lệch ý thì quay lại video | P2: 3–5 lần / tháng, tua lại khoảng 10 phút |
  | `dung_nhieu` | 21/144 (14,6%) | 8,9 | Hỏi gần như mỗi buổi pre-class, hay để lại chỗ chưa chắc rồi phải quay lại | P3: 6–10 lần / tháng, quay lại tìm đoạn khoảng 10 phút |

  Khảo sát câu 2 (n = 20) lệch về người dùng nhiều (1–2 lần chỉ 3/20, 3–5 lần 9/20), do mẫu tự chọn, nên tỉ lệ persona giữ theo data.
- Thấp 144 người từng hỏi, cơ sở 436 người có hoạt động, cao 721 tài khoản. Nguồn là log pre-class 05–25/11/2026 (P0–P2). TV1 chốt giữ ba mức này: `simulate-2` đã chạy với chúng, và 721 tài khoản khớp quy mô thật của lớp L3 ở đề track A ("Lớp L3 hơn 700 học viên"). Kịch bản cao giả định mọi tài khoản dùng với tần suất như người đang hỏi (hiện 144/721 = 20,0%), nên là cận trên. Nếu dùng cho **cả khoá (hơn 1.000 học viên, guide 4.2)**, chi phí tăng tuyến tính theo số người vì chi phí / người / tháng không đổi: 1.000 người ≈ **$5.77 / tháng** (Flash-Lite) và ≈ **$36.64 / tháng** (Pro), tính từ cột kịch bản cao của `simulate-2` ($4.16 và $26.42 cho 721 người) × 1.000 / 721; không chạy thêm mô phỏng.
- Token do API Nemotron qua OpenRouter báo. Hai cột giá dùng mức Standard của Gemini 3.1 Flash-Lite và Gemini 2.5 Pro. Giá được áp vào lượng token Nemotron, nên chi phí của hai model Gemini là ước tính và số token có thể thay đổi nếu gọi trực tiếp. [Giá Gemini Developer API, xem 28/11/2026](https://aistudio.google.com/docs/pricing).
- Tỉ lệ đạt dùng tính chi phí là 28/30 (93,3%), lấy từ `run-3@20261127-222235` (chấm sơ bộ).

## 2. Kết quả

Lượt đo API trực tiếp [`simulate-2.csv`](simulate-2.csv), mã `simulate-2@20261128-093944` (TV3 chạy, key OpenRouter có nạp tiền), 50 phiên, seed 42, **0/50 phiên lỗi**: 28 phiên dùng ít · 18 dùng vừa · 4 dùng nhiều. Xem [bảng gốc](simulate-2-summary.md).

Lượt trước [`simulate-1.csv`](simulate-1.csv) (`simulate-1@20261128-092259`, cùng cấu hình) bị OpenRouter trả HTTP 429 (hết hạn mức ngày của key) ở 34/50 phiên, chỉ 16 phiên hợp lệ và 1 phiên dùng nhiều, nên chạy lại thành lượt mới; `simulate-1` giữ nguyên. Số của `simulate-1` (Flash-Lite $0.0021 / task, $2.91 / tháng cơ sở) gần với `simulate-2`.

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (144 người) | Chi phí / tháng — cơ sở (436 người) | Chi phí / tháng — cao (721 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| gemini-3.1-flash-lite (vào 0.25 · ra 1.5 $/1M) | $0.0017 | $0.0019 | $0.00054 | $0.8313 | $2.52 | $4.16 | $0.0058 |
| gemini-2.5-pro (vào 1.25 · ra 10.0 $/1M) | $0.0111 | $0.0119 | $0.0035 | $5.28 | $15.98 | $26.42 | $0.0366 |

**Cả khoá (đề track A: "hơn 1.000 học viên"):** chi phí tỉ lệ thuận với số người vì tỉ lệ persona giữ nguyên. Lấy chi phí / tháng cơ sở ÷ 436 × 1.000: Flash-Lite ≈ **$5.78 / tháng**, Pro ≈ **$36.65 / tháng**. Số này suy ra từ bảng trên, không phải một lượt mô phỏng riêng.

Theo quy ước của khung, chi phí / task thành công lấy chi phí trung bình mỗi phiên chia cho tỉ lệ đạt của bộ thử. Cột chi phí / câu hỏi đạt chia thêm cho số lượt hỏi trung bình mỗi phiên.

Để kiểm độ nhạy, [lấy mẫu lại 50 phiên](replay-run-3-cp4.csv) bằng token API của các câu trong [Run 3](../eval/run-3.csv), cùng seed 42. Ở 436 người, phép tính này cho $2.69/tháng với Flash-Lite và $17.16/tháng với Pro. Mỗi câu dùng lại một lần đo token từ Run 3 nên phép tính này chưa phản ánh độ biến động khi gọi API nhiều lần.

## 3. So với impact

Cận trên của pain là 91,8 phút/tháng với mỗi học viên gặp vấn đề và 88,7 giờ/tháng trên 58 học viên trong tập log. Bảng hiện tính phần model. Chi phí tích hợp, vận hành và duyệt nội dung cần đo thêm.

**So trên cùng mẫu số (TV1).** Chi phí ở bảng tính trên mọi người dùng, nên giá trị cũng chia cho mọi người dùng trợ giảng: 5.324 phút / tháng (`spec.md` §2) ÷ 86 người nhận trả lời trong cùng cửa sổ ≈ **61,9 phút / người dùng / tháng** (cận trên, T = 10 phút). Nếu giữ T = 3 phút: ≈ 18,6 phút.

| | Flash-Lite ($0.0058 / người / tháng) | Pro ($0.0366 / người / tháng) |
|---|---:|---:|
| Chi phí / giờ học viên tiết kiệm — giá trị cận trên (61,9 phút) | ≈ $0.006 | ≈ $0.035 |
| Chi phí / giờ học viên tiết kiệm — T = 3 phút (18,6 phút) | ≈ $0.019 | ≈ $0.118 |

Chi phí / người / tháng như nhau ở cả ba kịch bản vì tỉ lệ persona giữ nguyên; kịch bản chỉ đổi tổng tiền.

**Quy tắc kết luận** (TV1 viết trước khi xem số mô phỏng và điểm Run 3):

| Kết luận | Khi nào |
|---|---|
| **Go** (thí điểm ở một lớp) | Lượt cải tiến đạt chuẩn "đạt" ở cả 4 metric của `spec.md` §7 **và** chi phí / giờ tiết kiệm ≤ 1 USD ở model mạnh với T = 3 phút *(ngưỡng 1 USD / giờ: tự đặt)* |
| **Iterate** | Chi phí đạt ngưỡng nhưng còn ≥1 metric chưa đạt chuẩn, hoặc metric từ chối (an toàn) dưới 100% |
| **Stop** | Chi phí / giờ tiết kiệm > 1 USD ngay cả ở model rẻ, hoặc lượt cải tiến làm giảm metric từ chối so với lượt 1 |

**Áp quy tắc:**
- Run 3 (`run-3@20261127-222235`, chấm sơ bộ): nguồn 22/22, nội dung 20/22, hỏi rõ 3/3, từ chối 5/5 → đạt cả 4 metric (`eval/report.md`).
- Chi phí / giờ tiết kiệm ở trường hợp xấu nhất (Pro, T = 3 phút) ≈ $0.118, dưới ngưỡng 1 USD khoảng 8 lần.

**Kết luận một dòng: Go — thí điểm LessonLens ở một bài của một lớp.** Chi phí model không phải điều cản trở (dưới $0.04 / người / tháng kể cả model mạnh). Điều chưa chắc là giá trị: 61,9 phút là cận trên, và điểm Run 3 mới chấm sơ bộ trên 30 câu chưa có câu nào từ lời người dùng. Thí điểm phải đo đúng hai điều này: học viên mở đúng đoạn nhanh hơn bao nhiêu phút, và tỉ lệ câu trả lời đạt trên câu hỏi thật.
