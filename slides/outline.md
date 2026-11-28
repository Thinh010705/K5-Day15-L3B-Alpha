# LessonLens · Dàn slide CP4

Bản nộp [demo-slides.pdf](../demo-slides.pdf). Kịch bản demo dùng B01 và B18.

## 1. Trợ giảng có nguồn cho pre-class

**231 / 576** · lượt trả lời thiếu mốc nguồn (40,1%)

- Học viên K5 cần lời giải thích sát câu hỏi và một đoạn bài giảng để tự kiểm.
- 15/20 người khảo sát gặp khó khi tìm đoạn căn cứ. 3/3 người được phỏng vấn kể được một lần cụ thể.

Nguồn · evidence/summary.md · M1, khảo sát 20 phiếu hợp lệ, phỏng vấn P1–P3

Người trình bày (đề xuất) · Nguyễn Năng Thịnh

## 2. Vì sao chọn truy xuất nguồn

**88,7 giờ** · mỗi tháng, cận trên ở nhóm 58 học viên gặp vấn đề

- 58 người × 9,18 lần/tháng × 10 phút mỗi lần. Tần suất ngoại suy từ 13 ngày, thời gian lấy trung vị phỏng vấn.
- Thiếu ngữ cảnh ước tính 7,2 giờ/tháng. Giữ nhánh hỏi rõ ngay trong bản chạy thử.

Nguồn · spec.md §2 · evidence/data-mining.md M1, M4

Người trình bày (đề xuất) · Nguyễn Năng Thịnh

## 3. Một câu hỏi, một quyết định

**11 đoạn** · viết lại từ slide AI20K, có mã trang để đối chiếu

- Câu hỏi → tra tối đa 3 đoạn → xét đủ căn cứ → kiểm mã → trả lời kèm nguồn.
- Câu thiếu ngữ cảnh được hỏi lại. Câu thiếu nguồn hoặc yêu cầu làm hộ được từ chối.
- Demo đối chiếu trang PDF. Tích hợp video cần transcript và mốc giây.

Nguồn · spec.md §4 · data/DATA_CARD.md

Người trình bày (đề xuất) · Cao Minh Quang

## 4. Demo LessonLens

**B01 · B18** · hai đường đi qua cùng một lệnh python run.py

- B01 · Output và Outcome khác nhau thế nào? → giải thích và dẫn SL-16.
- B18 · Giải thích tiếp ý đoạn vừa rồi → hỏi tên khái niệm hoặc mã đoạn, 0 lần gọi model.

Nguồn · eval/benchmark.csv · eval/run-3.csv · traces/run-3.jsonl

Người trình bày (đề xuất) · Cao Minh Quang

## 5. B18 đã hỏi lại đúng chỗ

**83,3% → 93,3%** · Run 1 đạt 25/30, Run 2 đạt 26/30, Run 3 đạt 28/30

- 30 câu, gồm 10 câu từ slide. Run 3: nguồn 22/22, nội dung 20/22, hỏi rõ 3/3, từ chối 5/5.
- So với Run 2 cùng model, B03 và B18 chuyển sang đạt. B07 thiếu trình tự, B14 lặp tiền đề sai.
- Run 1: 20261127-212409 · Run 2: 20261127-213001 · Run 3: 20261127-222235. Điểm sơ bộ.

Nguồn · eval/report.md · eval/metric_spec.yaml

Người trình bày (đề xuất) · Nguyễn Quang Dũng

## 6. Chi phí model khi dùng thật

**144 · 436 · 721** · người dùng ở ba kịch bản thấp, cơ sở và cao

- gemini-3.1-flash-lite · $0.0021 / task · $0.9626 / $2.91 / $4.82 mỗi tháng.
- gemini-2.5-pro · $0.0132 / task · $6.15 / $18.61 / $30.77 mỗi tháng.
- 16/50 phiên hợp lệ. 34 phiên lỗi HTTP 429 do hết hạn mức ngày. Impact cận trên 91,8 phút/người gặp/tháng.

Nguồn · cost/cost-estimate.md · cost/personas.yaml

Người trình bày (đề xuất) · Hoàng Minh Quyền

## 7. Tiếp tục thử trên một bài

**93,3%** · điểm sơ bộ trên benchmark 30 câu

- Bản chạy đáp ứng chuẩn CP2 trên bộ thử hiện có. Cần kiểm xem học viên có tìm được đúng đoạn nhanh hơn khi dùng thật.
- Ước tính 88,7 giờ/tháng là cận trên của vấn đề trong tập dữ liệu. Hiệu quả tiết kiệm thời gian cần được đo.

Nguồn · spec.md §2, §7 · eval/report.md

Người trình bày (đề xuất) · Nguyễn Năng Thịnh

## 8. Nếu có thêm một tuần

**2 / 30** · câu còn trượt trong Run 3

- B07 · kiểm tra phản hồi có đủ thứ tự của khung.
- B14 · kiểm tra trợ giảng phát hiện tiền đề trái với nguồn.
- Gắn mốc giây cho một transcript, thử với học viên và đo thời gian mở đúng đoạn.

Nguồn · eval/report.md §4 · validation/log.md

Người trình bày (đề xuất) · Nguyễn Quang Dũng

Video dự phòng [bản demo 30 giây](https://drive.google.com/file/d/1QlZSenJmeB5RB7QsUE-de7_X0wmrT3lk/view?usp=sharing).

Link video mở được trang Google Drive khi kiểm tra không đăng nhập. Kiểm lại khả năng phát video và cấu hình model thật trước khi trình bày.
