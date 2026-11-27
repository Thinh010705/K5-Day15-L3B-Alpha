# Đào data — cách đếm và kết quả

> Điền ở guide bước 1.2. Ôn lại: ngày 2, ngày 6 · lab ngày 2, lab ngày 6.
> Script đếm: `evidence/count.py` (chỉ thư viện chuẩn). Người khác chạy lại phải ra cùng số.
> Repo chỉ chứa số đã tổng hợp và vài mã dòng làm ví dụ — không chép lại nguyên file data.
> Người phụ trách: Hoàng Minh Quyền (TV2 — Data & Research Lead). Mục 1 viết và commit **trước** khi chạy script đếm.

## 1. Cách đếm — viết TRƯỚC khi chạy

- **Data dùng:** data pack pre-class BTC cấp (AI20K Level 3-4, khoá 5), đã chuẩn hoá bằng `python evidence/prepare_data.py` → `data-btc/preclass/` (không commit; sha256 ở `data-btc/MANIFEST.txt`). File: `events.csv`, `chat.csv`, `answers.csv`, `learners.csv`. Khoảng thời gian: **05/11/2026 → 25/11/2026 (giờ UTC)**, Day01 → Day13, 21 ngày lịch.
- **Script:** `python evidence/count.py` → in bảng số và ghi `evidence/data-mining-output.json` (chỉ số tổng hợp).
- **Nối bảng:** `events.ref_id` (dòng `chat_sent` / `agent_replied`) = `chat.id` = `answers.ref` (dòng `nguon = chat`). "Trợ giảng" = `chat.agent_id = teaching_assistant` (bỏ các bạn học AI `classmate_*`).
- **Đơn vị:** một **lượt** = một dòng `chat.csv` (một câu học viên nhắn + một câu AI trả lời). Một **người** = một mã `hv` duy nhất.

### Các tập người (mẫu số cho số "bao nhiêu người")

| Mã | Tập | Cách lấy |
|---|---|---|
| P0 | Tài khoản | mọi dòng `learners.csv` |
| P1 | Người có hoạt động | `hv` duy nhất có ≥1 dòng `events.csv` với `actor = learner` |
| P2 | Người hỏi trợ giảng | `hv` duy nhất có ≥1 lượt trợ giảng trong `chat.csv` |

### Các số sẽ đếm

| Mã | Hướng | Đếm gì (x) | Mẫu số (N) | Lọc / cửa sổ |
|---|---|---|---|---|
| **M1** | A1.1 — kiểm chứng nguồn | lượt trợ giảng có `moc_trich_dan = []` (danh sách rỗng) | lượt trợ giảng **có ghi khoá** `moc_trich_dan` trong `agent_replied.data` | từ 00:00 UTC của ngày đầu tiên có dòng `agent_replied` ghi khoá `moc_trich_dan` (script tự tìm) đến hết data |
| M1-người | A1.1 | người nhận ≥1 lượt M1 | người có ≥1 lượt trong mẫu số M1 | như M1 |
| M2 | Giả thuyết thay thế 3 — có dùng nguồn không | lượt có mốc trích dẫn (danh sách không rỗng) mà trong **10 phút** sau câu trả lời, cùng học viên có `video_seeked` với `by = link` | lượt trợ giảng có `moc_trich_dan` không rỗng | như M1; độ nhạy: 30 phút |
| M3 | Pain "phải tua lại" | lượt hỏi dưới video mà trong **5 phút** sau câu trả lời, cùng học viên tua **lùi** (`by = player`, `to < from`) trong **cùng video** | lượt trợ giảng `channel = video_question` có tên video | cả 21 ngày; tách riêng lượt có / không có mốc trích dẫn trong cửa sổ M1 |
| **M4** | A1.2 — câu hỏi mơ hồ | lượt trợ giảng có `missing_context = true` | lượt trợ giảng có ghi khoá `missing_context` | cả 21 ngày |
| M5 | A1.2 — hỏi tiếp | lượt hỏi dưới video mà cùng học viên hỏi trợ giảng tiếp về **cùng video** trong **5 phút** sau câu trả lời | lượt trợ giảng `channel = video_question` | cả 21 ngày |
| **M6** | A1.3 — câu ngoài bài | câu nhắn trợ giảng được giám khảo AI chấm `rubric_bam_bai = 0` ("không liên quan bài") | dòng `answers.csv` `nguon = chat`, `trang_thai_cham = da_cham`, nối được tới lượt trợ giảng | cả 21 ngày |
| M7 | Giả thuyết thay thế 4 — chờ lâu | trung vị, p90 của `latency_ms`; lượt chờ > 10 giây | lượt trợ giảng có `cached = false` | cả 21 ngày |
| V1 | Khối lượng (cho Impact, persona) | số lượt trợ giảng / người: trung vị, p75, p90, lớn nhất | P2 | cả 21 ngày; đổi ra / tháng = × 30/21 *(ngoại suy tuyến tính)* |
| V2 | Khối lượng | số **phiên hỏi** / người và số lượt / phiên; một phiên = chuỗi lượt trợ giảng của cùng học viên cách nhau ≤ 30 phút *(ngưỡng nhóm tự chọn)* | P2 | cả 21 ngày |

| V3 | Persona chi phí (CP4) | chia P2 theo số phiên hỏi / 21 ngày: **1 phiên = `dung_it` · 2–3 = `dung_vua` · ≥4 = `dung_nhieu`**; mỗi nhóm: share, số phiên TB × 30/21 = phiên / tháng, lượt / phiên TB (làm tròn) | P2 | quy tắc chốt ở CP4 trước khi chạy V3 (viết trong test trước) |

Với M1, M4, M6 còn đếm **số người** gặp (≥1 lần) và **số lần trung bình / người gặp** → dùng làm N và F cho bảng Impact (`spec.md` §2). T (phút mất mỗi lần) **không có trong data** — lấy từ phỏng vấn.

### Mẫu số — vì sao chọn như vậy

- **Không** dùng 721 tài khoản làm mẫu số: chỉ người có hoạt động (P1) hoặc người hỏi trợ giảng (P2) mới có thể gặp vấn đề.
- **M1 chỉ tính dòng có ghi khoá `moc_trich_dan`.** Khoá này không có trong dòng ghi trước ngày bắt đầu ghi (README BTC: "mỗi loại dữ liệu bắt đầu ghi từ ngày khác nhau; ô trống trước ngày đó không có nghĩa là học viên không làm"). Dòng không ghi khoá **không** bị tính là "không trích dẫn". Dòng trong cửa sổ mà vẫn không ghi khoá (u) báo riêng, kèm khoảng chặn: thấp = x/(N+u), cao = (x+u)/(N+u).
- Lượt `cached = true` (dùng lại câu trả lời cũ) vẫn tính vì học viên vẫn thấy câu trả lời đó; báo tách riêng.
- Ngưỡng giả thuyết (`evidence/hypothesis.md`, commit trước khi xem data): M1 **≥ 20%** thì ủng hộ giả thuyết. Giữ nguyên ngưỡng này dù kết quả ra sao.

### Những điều cách đếm này KHÔNG trả lời được

- Data không có câu chữ câu hỏi / câu trả lời → không kết luận trợ giảng trả lời **sai** hay **bịa**; "không có mốc trích dẫn" chỉ là thiếu căn cứ để học viên tự kiểm.
- M2, M3, M5 là **dấu vết hành vi** (proxy) — tua lại / hỏi tiếp có thể vì lý do khác. Chỉ dùng để so sánh, không kết luận nguyên nhân.
- `by = link` trong `video_seeked` được hiểu là tua do bấm một đường link (nhiều khả năng là mốc trích dẫn trong câu trả lời). Từ điển BTC không giải thích giá trị này → script kiểm thêm: bao nhiêu lần `by = link` xảy ra ngay sau một câu trả lời có mốc trích dẫn.

## 2. Đọc trước, đếm sau

Đã đọc: `README.md` của data pack, toàn bộ `column_dictionary.csv` (71 dòng) và `event_types.csv` (38 loại việc), 5 dòng đầu mỗi file, cấu trúc khoá JSON trong cột `data` của `chat_sent` (1.260 dòng) và `agent_replied` (1.260 dòng). Các *kiểu* hành vi thấy được (trước khi định nghĩa thứ cần đếm):

- Học viên hỏi trợ giảng ngay dưới video (`chat.channel = video_question`), hỏi bằng cách bôi đen chữ trên slide (`slide_text_asked`), hoặc nhắn với bạn học AI trong khung thảo luận (`video_discussion_reply`). Chỉ có **độ dài** câu hỏi / câu trả lời, không có câu chữ.
- Mỗi câu trả lời của AI có `agent_replied` trong `events.csv`: `missing_context` (thiếu ngữ cảnh), `moc_trich_dan` (danh sách mốc dạng `DayNN/dNN-....txt@giây` hoặc chỉ `@giây`, có khi rỗng `[]`), `latency_ms`, `cached`, `model`; ít dòng hơn có `verdict` (`correct` / `partial` / `incorrect`) và `reply_kind`.
- **Các khoá bắt đầu ghi vào những ngày khác nhau:** `missing_context`, `latency_ms` có từ 05/11; `moc_trich_dan`, `ngu_canh` chỉ từ **13/11**; `verdict` chỉ 46 dòng (08–20/11); `reply_kind` 169 dòng; `prompt_version`, `guidance_ids`, `learning_mode` chỉ ngày 25/11 → `verdict` và `reply_kind` quá ít để làm mẫu số chính.
- Học viên tua video (`video_seeked`) bằng thanh video (`by = player`) hoặc bằng link (`by = link`, rất ít dòng) — tua lùi và tua tới đều có.
- Câu nhắn AI của học viên được giám khảo AI chấm 3 tiêu chí 0–2 trong `answers.csv` (`rubric_bam_bai`, `rubric_y_moi`, `rubric_dung_ngu_canh`) — điểm do máy chấm, không có người kiểm lại.
- Câu hỏi dưới video có `lesson_id` gần như luôn trống; ngày học lấy từ `transcript` (`DayNN/...`). Giờ ghi theo UTC (giờ Việt Nam = UTC + 7).

## 3. Kết quả

Chạy `python evidence/count.py` ngày 27/11/2026 trên data 05/11 → 25/11/2026 (UTC). Số đầy đủ: `evidence/data-mining-output.json`. Đã kiểm chéo M1 và M4 bằng một cách đếm độc lập — khớp.

**Quy mô (tập người, khối lượng)**

| Đếm gì | x / N | % | Ghi chú |
|---|---|---|---|
| P1 người có hoạt động / tài khoản | 436/721 | 60.5% | khớp README BTC |
| P2 người hỏi trợ giảng / người có hoạt động | 144/436 | 33.0% | 2/3 người có hoạt động chưa từng hỏi trợ giảng |
| Lượt trợ giảng / mọi lượt chat | 1.153/1.260 | 91.5% | còn lại là bạn học AI |
| V1 lượt trợ giảng / người (P2, 21 ngày) | TB 8.0 · trung vị 4 · p75 10 · p90 18 · max 72 | — | lệch mạnh: ít người hỏi rất nhiều |
| V2 phiên hỏi / người (cách nhau ≤ 30 phút) | TB 2.2 · trung vị 1 · p90 4 | — | 321 phiên |
| V2 lượt / phiên | TB 3.6 · trung vị 2 · p90 8 | — | |

**V3 — persona cho `cost/personas.yaml` (CP4)**

| Persona | Quy tắc | Người | Share | Phiên / tháng *(× 30/21)* | Lượt / phiên (TB) |
|---|---|---|---|---|---|
| `dung_it` | 1 phiên | 75/144 | 0.521 | 1.4 | 2.88 → 3 |
| `dung_vua` | 2–3 phiên | 48/144 | 0.333 | 3.4 | 3.74 → 4 |
| `dung_nhieu` | ≥4 phiên | 21/144 | 0.146 | 8.9 | 3.87 → 4 |

**Pain theo từng hướng**

| Mã | Đếm gì | x / N | % | Ghi chú |
|---|---|---|---|---|
| **M1** | Lượt trợ giảng **không có mốc trích dẫn** (13/11 → 25/11) | **231/576** | **40.1%** | ≥ ngưỡng 20% của giả thuyết → **ủng hộ** (vế data). Khoảng chặn khi tính cả 7 lượt không ghi khoá: 39.6% … 40.8% |
| M1 | … chỉ câu hỏi dưới video | 231/557 | 41.5% | khung thảo luận: 0/19 |
| M1 | Người nhận ≥1 câu trả lời không có mốc / người nhận trả lời trong cửa sổ | 58/86 | 67.4% | TB 3.98 lần / người gặp trong 13 ngày ≈ **9.2 lần / tháng** *(ngoại suy × 30/13)* |
| M2 | Câu trả lời có mốc → học viên bấm link trong 10 phút | 25/345 | 7.2% | 30 phút: 26/345 (7.5%). 22/40 lần `by = link` xảy ra ngay sau câu trả lời có mốc; 39/40 lần từ 13/11 trở đi |
| M3 | Câu hỏi dưới video → tua lùi cùng video trong 5 phút | 91/1.091 | 8.3% | |
| M3 | … sau câu trả lời **có** mốc | 39/326 | 12.0% | **ngược** chiều cơ chế giả thuyết: tua lùi nhiều hơn khi *có* mốc |
| M3 | … sau câu trả lời **không có** mốc | 10/231 | 4.3% | |
| **M4** | Lượt trợ giảng ghi `missing_context = true` | 100/1.138 | 8.8% | người gặp: 50/142 (35.2%), TB 2.0 lần / 21 ngày ≈ 2.9 lần / tháng |
| M5 | Câu hỏi dưới video → hỏi tiếp cùng video trong 5 phút | 520/1.091 | 47.7% | gần một nửa câu hỏi có câu hỏi nối tiếp |
| **M6** | Câu hỏi trợ giảng bị giám khảo AI chấm `rubric_bam_bai = 0` | 243/1.122 | 21.7% | người gặp: 104/143 (72.7%), TB 2.3 lần / 21 ngày ≈ 3.3 lần / tháng. Nhãn do máy chấm |
| M7 | Độ trễ trợ giảng (không cache): trung vị / p90 | 2,4 s / 4,6 s | — | chờ > 10 s: 1/1.138 (0.1%) → giả thuyết thay thế 4 (chờ lâu) **không** được ủng hộ |

**Đọc kết quả (chưa phải kết luận — còn chờ phỏng vấn)**

- Vế data của giả thuyết đạt: 40.1% câu trả lời trợ giảng không có mốc trích dẫn, và 2/3 người nhận trả lời đã gặp ít nhất một lần.
- Nhưng khi **có** mốc, học viên hiếm khi bấm (7.2%), và họ tua lùi **nhiều hơn** chứ không ít hơn (12.0% so với 4.3%). Có hai cách đọc cần phỏng vấn để phân biệt: (a) mốc trích dẫn khiến học viên quay lại video để kiểm chứng — tức nhu cầu kiểm chứng có thật; (b) học viên chưa biết / chưa tin cách dùng mốc (giả thuyết thay thế 3).
- Thời gian chờ không phải vấn đề (trung vị 2,4 s).

## 4. ≥5 ví dụ cụ thể (mã dòng / mã đã ẩn danh, không đoán ai là ai)

Chọn tất định bằng `evidence/count.py` (lượt **sớm nhất** của mỗi kiểu — khoá `vi_du` trong `evidence/data-mining-output.json`). Chỉ ghi mã lượt chat (`chat.id`, BTC đã thay mã), không ghi mã học viên. Data không có câu chữ nên ví dụ là **metadata**, không phải trích dẫn lời học viên.

1. **`C01187`** — 13/11, hỏi trợ giảng dưới video `d06-r1-v01`: câu hỏi 92 ký tự → câu trả lời 600 ký tự, `moc_trich_dan = []`. Trả lời dài nhưng không có mốc nào để học viên tự kiểm. *(M1)*
2. **`C00882`** — 13/11, dưới video `d05-r2-v06`: câu hỏi 18 ký tự → trả lời 220 ký tự, `moc_trich_dan = []`. *(M1)*
3. **`C00872`** — 13/11, hỏi khi đang ở video `d01-r1-v01`; câu trả lời dẫn 6 mốc đều ở **video khác** (`Day01/d01-r1-v04.txt@31` … `@45`); trong 10 phút sau, học viên có `video_seeked` `by = link`. Mốc trích dẫn được dùng thật. *(M2)*
4. **`C00394`** — 13/11, dưới video `d06-r1-v04`: trả lời có 4 mốc (`d06-r1-v02@18`, `@29`, `d06-r1-v04@4`, `@12`); trong 5 phút sau, học viên tự tua **lùi** trong cùng video bằng thanh video. *(M3 — tua lùi sau câu trả lời có mốc)*
5. **`C00983`** — 05/11, dưới video `d01-r1-v05`: câu hỏi 29 ký tự, trợ giảng ghi `missing_context = true`, giám khảo AI chấm câu hỏi `rubric_bam_bai = 0`. Câu hỏi ngắn, thiếu ngữ cảnh. *(M4, M6)*
6. **`C00581`** → **`C00499`** — 05/11, cùng video `d01-r1-v02`: hỏi (82 ký tự), nhận trả lời, rồi hỏi tiếp về cùng video trong vòng 5 phút (183 ký tự). *(M5)*
7. **`C01056`** — 05/11, dưới video `d01-r1-v01`: câu hỏi chỉ **2 ký tự**, bị chấm `rubric_bam_bai = 0`. *(M6 — câu không bám bài)*

### Kiểm mẫu số và cách tính (CP3)

| Kiểm gì | Kết quả |
|---|---|
| P1 tự đếm so với README BTC (436 người có hoạt động) | 436 = 436 ✓ |
| Lượt trợ giảng tự đếm so với `chat.agent_id` | 1.153 = 1.153 ✓ |
| Số dòng 7 file + 38 loại việc so với README / `event_types.csv` (`prepare_data.py`) | khớp hết ✓ |
| M1, M4 đếm lại bằng đoạn code độc lập (không dùng `count.py`) | 231/576, u = 7 · 100/1.138 — khớp ✓ |
| M1 có lệch vì 7 lượt không ghi khoá không? | khoảng chặn 39.6% … 40.8% — kết luận không đổi |
| M1 có do lượt dùng lại (cache) kéo lên không? | không cache 226/561 (40.3%) · cache 5/15 (33.3%) |
| Độ nhạy M2 (cửa sổ 10 → 30 phút) | 7.2% → 7.5% |
| Độ nhạy M3 (2 · 5 · 10 phút), có mốc vs không mốc | 7.4% vs 2.6% · 12.0% vs 4.3% · 15.3% vs 5.2% — chiều chênh lệch giữ nguyên |
| Độ nhạy M5 (2 · 5 · 10 phút) | 40.7% · 47.7% · 51.0% |
| Test tự động cho cách đếm | `python -m unittest discover -s evidence/tests` → 30/30 OK |

## 5. Giới hạn của data

Data cho biết người ta **làm gì**, không cho biết **vì sao**. Thiếu gì, lệch về phía nào:
- **Không có câu chữ** câu hỏi / câu trả lời → không biết câu trả lời không có mốc là sai, đúng hay chỉ thiếu căn cứ; không kết luận trợ giảng "bịa".
- `moc_trich_dan` chỉ ghi từ 13/11 (13 ngày); 39/40 lần bấm link cũng từ 13/11 → có thể tính năng mốc trích dẫn chỉ có từ ngày này, nên M1 không nói gì về giai đoạn trước.
- M2, M3, M5 là dấu vết hành vi trong cửa sổ 5–10 phút do nhóm tự chọn; tua lùi / hỏi tiếp có thể vì lý do khác (xem lại đoạn khó, hỏi câu mới).
- M6 dùng nhãn `rubric_bam_bai` do **giám khảo AI** chấm, không có người kiểm lại.
- Lệch: chỉ 144/436 người có hoạt động từng hỏi trợ giảng, và vài người hỏi rất nhiều (max 72 lượt) → số theo lượt nghiêng về người hỏi nhiều; vì vậy luôn báo kèm số theo người.
- `occurred_at` theo đồng hồ máy học viên, giờ UTC; chỉ là một khoá, một nhóm lớp.

→ Kiểm lại bằng phỏng vấn P1–P4 (`PROJECT_EXECUTION_PLAN` §4.3): câu 2 (làm gì để kiểm tra câu trả lời — có bấm mốc không, vì sao), câu 3–4 (lần gần nhất phải tua lại / hỏi lại, mất bao nhiêu phút → **T** cho Impact), câu 5 (mong trợ giảng xử lý thế nào khi không có trong bài).

## 6. Số đưa sang `spec.md` §2 và `canvas.md` (cho TV1)

| Hướng | N — người gặp (cửa sổ quan sát) | F — lần / người gặp / tháng | T — phút / lần | Nguồn |
|---|---|---|---|---|
| A1.1 Source traceability | 58 (trong 86 người nhận trả lời, 13/11–25/11) | ≈ 9.2 *(ngoại suy từ 3.98 lần / 13 ngày)* | **chưa có** — lấy từ phỏng vấn P1–P4 | M1 |
| A1.2 Ambiguity | 50 (trong 142 người, 05/11–25/11) | ≈ 2.9 *(ngoại suy từ 2.0 lần / 21 ngày)* | **chưa có** | M4 |
| A1.3 Safe abstention | 104 (trong 143 người, 05/11–25/11) | ≈ 3.3 *(ngoại suy từ 2.34 lần / 21 ngày; nhãn máy chấm)* | **chưa có** | M6 |

- N là số người **trong cửa sổ quan sát**, không phải mỗi tháng; chỉ là học viên khoá này trên trang pre-class (không phải mọi học viên AI20K).
- Persona (§8): xem V1–V2 — trung vị 4 lượt / người / 21 ngày, trung vị 2 lượt / phiên.
- Dòng canvas "Bằng chứng đầu" có thể ghi: *"40.1% (231/576) câu trả lời trợ giảng 13–25/11 không có mốc trích dẫn; 58/86 người nhận trả lời gặp ≥1 lần (data pre-class BTC, `evidence/data-mining.md`)"*.
