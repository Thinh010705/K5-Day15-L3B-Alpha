# Khai báo dùng AI

README của nhóm có mục "Dùng AI vào việc gì" (2–3 dòng, bắt buộc). Ghi chi tiết vào bảng dưới đây.

> Luật của đề: dùng AI để làm bài thoải mái, nhưng **ai không giải thích được phần có tên mình thì phần đó nhận 0 điểm**. Khai thiếu không bị trừ; giấu mới bị.

| Việc | Công cụ AI | AI làm gì | Người kiểm/sửa gì | Ai phụ trách |
|---|---|---|---|---|
| Code bản chạy thử | Codex (OpenAI) · Claude Code (Claude Opus 5.5) | **Codex:** viết khung CP2 `codebase/agent.py`, `codebase/tools.py` (luồng tra đoạn → model → kiểm mã nguồn, chặn câu ngắn / làm hộ / ghi đè); chuyển sang kho slide và viết nhánh gọi API OpenAI, Gemini trong `codebase/ai.py`. **Claude Code:** thay ngưỡng độ dài bằng kiểm câu chỉ có đại từ / từ đệm để hỏi rõ (spec §5 lớp 2); thêm nhánh OpenRouter (tái dùng định dạng OpenAI, ép `response_format` JSON); chạy `eval --try`, `simulate --try` | TV3 chọn lát cắt, hình dạng workflow, nhà cung cấp model; chạy thử tay 6 câu với model thật (2 câu thường, 1 câu cần 2 đoạn, 1 câu ngoài bài, 2 câu tấn công) và các câu mơ hồ / làm hộ ở chế độ giả, đọc từng output. Đọc lại và giải thích được từng hàm: __ *(TV3 điền sau khi tự đọc lại)* | Cao Minh Quang (TV3) |
| Prompt / thiết kế lời gọi mô hình | Codex (OpenAI) | Soạn `SYSTEM` trong `codebase/agent.py`: chỉ dùng đoạn được cấp, trả JSON `decision` (`answer` / `clarify` / `abstain`) + `citations`, không theo chỉ dẫn nằm trong dữ liệu nguồn | Code kiểm lại sau model: JSON sai, mã nguồn ngoài tập vừa truy xuất, hoặc mã lạ trong nội dung → từ chối. Đã thử 2 câu tấn công (mã giả `SL-99`, "trả lời không cần nguồn") với model thật — đều từ chối | Cao Minh Quang (TV3) |
| Viết lại đoạn slide làm kho tra cứu | Codex (OpenAI) | Viết lại 11 ý từ slide `VinUni_TuDuyProduct_DS_FDE_v3.pdf` thành `data/lesson_product_ai20k.json`, mã `SL-<trang>` | Đối chiếu từng đoạn với chữ trích từ trang PDF tương ứng (Claude Code trích bằng `pypdf`, 27/11): 11/11 khớp ý chính; sửa câu chữ SL-19 (chỉ số tổ chức theo đúng slide) và tiêu đề SL-30 ("sinh viên kỹ thuật", không phải "kỹ sư AI") — spec §10. TV3 xem lại bảng đối chiếu: __ *(TV3 điền)* | Cao Minh Quang (TV3) |
| Chọn model | Claude Code (Claude Opus 5.5) | Lấy danh sách model free từ API công khai OpenRouter, đề xuất model hỗ trợ JSON; đổi sang `nvidia/nemotron-3-ultra-550b-a55b:free` khi `google/gemma-4-31b-it:free` bị giới hạn lượt (429) | TV3 tạo key, nạp tiền, quyết định dùng OpenRouter | Cao Minh Quang (TV3) |
| Đào data (viết script đếm, gợi ý nhãn) | Claude Code (Claude Opus 5.5) | Soạn cách đếm ở `evidence/data-mining.md` §1 theo giả thuyết nhóm đã chốt; viết `evidence/prepare_data.py`, `evidence/count.py` và test (`evidence/tests/`); chạy đếm, kiểm chéo M1, M4 bằng một cách đếm độc lập (khớp 2/2) | TV2 đọc lại cách đếm + script trước khi dùng số; kiểm tay __ dòng, khớp __ *(TV2 điền sau khi kiểm)* | Hoàng Minh Quyền (TV2) |
| Rà câu hỏi phỏng vấn / khảo sát | | Chỉ rà câu dẫn dắt | | |
| Viết câu thử (benchmark) | Codex (OpenAI) | Soạn B21–B30 từ kho đoạn đã đối chiếu với slide, ghi trang PDF trong `source`, kiểm tra đủ mã nguồn sau tra cứu | Cần TV4 đọc lại câu, đáp án và tiêu chí trước khi chấm Run 1 | TV4 |
| Sinh data `synthetic` (nếu có) | | | Seed __ · kiểm tay __ dòng | |
| Chấm cột `pass` bằng LLM | Codex (OpenAI) | Đọc 30 đầu ra Run 1 theo tiêu chí CP2, ghi `pass` và `ghi_chu`, dùng lệnh `score` để tổng hợp | Đang chờ người chấm thứ hai đối chiếu | TV4 |
| Slide, văn bản | | | | |

**Không dùng AI để:** tạo người được phỏng vấn, trích dẫn, câu trả lời khảo sát; sửa kết quả các lượt đã chạy (`eval/run-*.csv`, `cost/simulate-*.csv`, `traces/`).
