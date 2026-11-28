# Reflection — Nguyễn Quang Dũng-2A202604031

> Bản nháp để Dũng kiểm tra và bổ sung trải nghiệm cá nhân trước khi nộp.

## 1. Vai trò và phần việc

- Phụ trách đánh giá và QA của LessonLens. Bộ câu thử có 30 câu, trong đó B21–B30 được soạn từ các trang slide đã đối chiếu. [Benchmark](../eval/benchmark.csv)
- Theo dõi kết quả Run 1, Run 2 và Run 3 theo chuẩn CP2. Run 3 đạt sơ bộ 28/30. Lần chấm đối chiếu của TV3 khớp 4/5 câu sau khi đọc lại B07. [Báo cáo đánh giá](../eval/report.md)
- Chuẩn bị dàn slide về kết quả đánh giá và giới hạn của bản chạy thử. [Dàn slide](../slides/outline.md)

## 2. AI hỗ trợ và chỗ cần kiểm lại

- Codex hỗ trợ soạn B21–B30 từ kho đoạn đã đối chiếu và chấm sơ bộ đầu ra theo từng tiêu chí.
- Ở lần đọc đầu Run 3, Codex cho B14 đạt vì thấy đủ ba năng lực và đúng mã. Khi đối chiếu lại với SL-30, điểm được sửa thành trượt vì đầu ra lặp tiền đề “kỹ sư AI”, còn slide nói về sinh viên kỹ thuật.
- Trường hợp này cho thấy người chấm cần đọc đoạn nguồn và tiêu chí cùng với đầu ra. [Ghi chú AI](../docs/ai-usage.md) · [Run 3](../eval/run-3.csv)

## 3. Một câu trượt và bài học

- B07 yêu cầu nêu đúng trình tự Who–What–How. Run 3 đưa đúng tên khung và mã SL-11 nhưng chỉ có tên khung.
- Chấm đạt cần thấy câu trả lời nói rõ thứ tự: xác định ai gặp vấn đề, làm rõ việc họ đang khó hoàn thành, rồi mới thiết kế cách giải.
- Khi đánh giá một trợ giảng có trích dẫn, cần kiểm riêng độ đúng của mã nguồn và độ đầy đủ của lời giải thích. [Tiêu chí CP2](../eval/metric_spec.yaml) · [Kho đoạn](../data/lesson_product_ai20k.json)
