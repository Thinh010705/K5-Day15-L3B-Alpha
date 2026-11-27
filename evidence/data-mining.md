# Đào data — cách đếm và kết quả

> Điền ở guide bước 1.2. Ôn lại: ngày 2, ngày 6 · lab ngày 2, lab ngày 6.
> Script đếm: `evidence/count.py` (chỉ thư viện chuẩn). Người khác chạy lại phải ra cùng số.
> Repo chỉ chứa số đã tổng hợp và vài mã dòng làm ví dụ — không chép lại nguyên file data.
> Người phụ trách: Hoàng Minh Quyền (TV2 — Data & Research Lead). Chỉ đếm những gì kế hoạch nhóm (`PROJECT_EXECUTION_PLAN_LessonLens.md` §4.4, §5.1, §5.3) yêu cầu.
> M1, M4, M5, M7 viết và commit **trước** khi chạy script đếm; độ nhạy M1, M8, V3 thêm **sau** khi xem kết quả — ghi rõ ở từng dòng.

## 1. Cách đếm — viết TRƯỚC khi chạy

- **Data dùng:** data pack pre-class BTC cấp (AI20K Level 3-4, khoá 5), đã chuẩn hoá bằng `python evidence/prepare_data.py` → `data-btc/preclass/` (không commit; sha256 ở `data-btc/MANIFEST.txt`). File: `events.csv`, `chat.csv`, `learners.csv`. Khoảng thời gian: **05/11/2026 → 25/11/2026 (giờ UTC)**, Day01 → Day13, 21 ngày lịch.
- **Script:** `python evidence/count.py` → in bảng số và ghi `evidence/data-mining-output.json` (chỉ số tổng hợp).
- **Nối bảng:** `events.ref_id` (dòng `chat_sent` / `agent_replied`) = `chat.id`. "Trợ giảng" = `chat.agent_id = teaching_assistant` (bỏ các bạn học AI `classmate_*`).
- **Đơn vị:** một **lượt** = một dòng `chat.csv` (một câu học viên nhắn + một câu AI trả lời). Một **người** = một mã `hv` duy nhất.

### Các tập người (mẫu số cho số "bao nhiêu người" — kế hoạch §5.2: chỉ đếm người duy nhất đủ điều kiện)

| Mã | Tập | Cách lấy |
|---|---|---|
| P0 | Tài khoản | mọi dòng `learners.csv` |
| P1 | Người có hoạt động | `hv` duy nhất có ≥1 dòng `events.csv` với `actor = learner` |
| P2 | Người hỏi trợ giảng | `hv` duy nhất có ≥1 lượt trợ giảng trong `chat.csv` |

### Các số sẽ đếm (theo cách đo ở kế hoạch §5.1)

| Mã | Hướng (kế hoạch §5.1) | Đếm gì (x) | Mẫu số (N) | Lọc / cửa sổ |
|---|---|---|---|---|
| **M1** | A1.1 — "tỷ lệ phản hồi thiếu mốc trích dẫn" | lượt trợ giảng có `moc_trich_dan = []` (danh sách rỗng) | lượt trợ giảng **có ghi khoá** `moc_trich_dan` trong `agent_replied.data` | từ 00:00 UTC của ngày đầu tiên có dòng `agent_replied` ghi khoá `moc_trich_dan` (script tự tìm) đến hết data |
| M1-người | A1.1 | người nhận ≥1 lượt M1 | người có ≥1 lượt trong mẫu số M1 | như M1 |
| M1-độ nhạy | A1.1 — kiểm mẫu số | như M1 nhưng **bỏ** lượt AI ghi `missing_context = true` (có thể là câu hỏi lại, vốn không cần mốc) | như M1, bỏ các lượt đó | *thêm ở CP3 khi kiểm mẫu số, sau khi xem kết quả* |
| **M4** | A1.2 — "`missing_context`" | lượt trợ giảng có `missing_context = true` | lượt trợ giảng có ghi khoá `missing_context` | cả 21 ngày |
| M5 | A1.2 — "lượt hỏi tiếp" | lượt hỏi dưới video mà cùng học viên hỏi trợ giảng tiếp về **cùng video** trong **5 phút** sau câu trả lời | lượt trợ giảng `channel = video_question` | cả 21 ngày; độ nhạy 2 và 10 phút |
| M8 | A1.3 — "`verdict`, `reply_kind`" | `verdict`, `reply_kind` ghi ở lượt nào: kênh, AI nào, có phải trả lời lại một lời AI (`chat_sent.reply_to`) | mọi lượt có ghi khoá đó | chỉ mô tả; *thêm ở CP3 khi kiểm logic, sau khi xem kết quả* |
| M7 | Giả thuyết thay thế 4 (§4.2 "thời gian phản hồi"; §4.4 "độ trễ") | trung vị, p90 của `latency_ms`; lượt chờ > 10 giây | lượt trợ giảng có `cached = false` | cả 21 ngày |
| V1 | Số người và số lượt tương tác (CP2) | số lượt trợ giảng / người: trung vị, p75, p90, lớn nhất | P2 | cả 21 ngày; đổi ra / tháng = × 30/21 *(ngoại suy tuyến tính)* |
| V2 | Số lượt tương tác (CP2) | số **phiên hỏi** / người và số lượt / phiên; một phiên = chuỗi lượt trợ giảng của cùng học viên cách nhau ≤ 30 phút *(ngưỡng nhóm tự chọn)* | P2 | cả 21 ngày |
| V3 | Tần suất sử dụng cho `cost/personas.yaml` (CP4) | chia P2 theo số phiên hỏi / 21 ngày: **1 phiên = `dung_it` · 2–3 = `dung_vua` · ≥4 = `dung_nhieu`** (tên persona theo khung `cost/personas.yaml`); mỗi nhóm: share, số phiên TB × 30/21 = phiên / tháng, lượt / phiên TB (làm tròn) | P2 | quy tắc đặt ở CP4 **cùng commit với kết quả** (không đăng ký trước); kế hoạch CP4: TV1 chốt ba persona |

Với M1, M4 còn đếm **số người** gặp (≥1 lần) và **số lần trung bình / người gặp** → N và F cho bảng Impact (kế hoạch §5.3). T (phút mất mỗi lần) **không có trong data** — kế hoạch §5.3: lấy từ phỏng vấn.

### Mẫu số — vì sao chọn như vậy

- **Không** dùng 721 tài khoản làm mẫu số (kế hoạch §5.2): chỉ người có hoạt động (P1) hoặc người hỏi trợ giảng (P2).
- **M1 chỉ tính dòng có ghi khoá `moc_trich_dan`.** Khoá này không có trong dòng ghi trước ngày bắt đầu ghi (README BTC: "mỗi loại dữ liệu bắt đầu ghi từ ngày khác nhau; ô trống trước ngày đó không có nghĩa là học viên không làm"). Dòng không ghi khoá **không** bị tính là "không trích dẫn". Dòng trong cửa sổ mà vẫn không ghi khoá (u) báo riêng, kèm khoảng chặn: thấp = x/(N+u), cao = (x+u)/(N+u).
- Lượt `cached = true` (dùng lại câu trả lời cũ) vẫn tính vì học viên vẫn thấy câu trả lời đó; báo tách riêng.
- Ngưỡng giả thuyết (`evidence/hypothesis.md`, commit trước khi xem data): M1 **≥ 20%** thì ủng hộ giả thuyết. Giữ nguyên ngưỡng này dù kết quả ra sao.

### Những điều cách đếm này KHÔNG trả lời được (kế hoạch §4.4)

- Data không có câu chữ câu hỏi / câu trả lời → không kết luận trợ giảng trả lời **sai** hay **bịa**; "không có mốc trích dẫn" chỉ là thiếu căn cứ để học viên tự kiểm.
- M5 là **dấu vết hành vi** — hỏi tiếp có thể vì lý do khác (hỏi câu mới). Không kết luận nguyên nhân.

## 2. Đọc trước, đếm sau

Đã đọc: `README.md` của data pack, toàn bộ `column_dictionary.csv` (71 dòng) và `event_types.csv` (38 loại việc), 5 dòng đầu mỗi file, cấu trúc khoá JSON trong cột `data` của `chat_sent` (1.260 dòng) và `agent_replied` (1.260 dòng). Các *kiểu* hành vi thấy được (trước khi định nghĩa thứ cần đếm):

- Học viên hỏi trợ giảng ngay dưới video (`chat.channel = video_question`), hỏi bằng cách bôi đen chữ trên slide (`slide_text_asked`), hoặc nhắn với bạn học AI trong khung thảo luận (`video_discussion_reply`). Chỉ có **độ dài** câu hỏi / câu trả lời, không có câu chữ.
- Mỗi câu trả lời của AI có `agent_replied` trong `events.csv`: `missing_context` (thiếu ngữ cảnh), `moc_trich_dan` (danh sách mốc dạng `DayNN/dNN-....txt@giây` hoặc chỉ `@giây`, có khi rỗng `[]`), `latency_ms`, `cached`, `model`; ít dòng hơn có `verdict` (`correct` / `partial` / `incorrect`) và `reply_kind`.
- **Các khoá bắt đầu ghi vào những ngày khác nhau:** `missing_context`, `latency_ms` có từ 05/11; `moc_trich_dan`, `ngu_canh` chỉ từ **13/11**; `verdict` chỉ 46 dòng (08–20/11); `reply_kind` 169 dòng; `prompt_version`, `guidance_ids`, `learning_mode` chỉ ngày 25/11.
- Câu hỏi dưới video có `lesson_id` gần như luôn trống; ngày học lấy từ `transcript` (`DayNN/...`). Giờ ghi theo UTC (giờ Việt Nam = UTC + 7).

## 3. Kết quả

Chạy `python evidence/count.py` ngày 27/11/2026 trên data 05/11 → 25/11/2026 (UTC). Số đầy đủ: `evidence/data-mining-output.json`. Đã kiểm chéo M1 và M4 bằng một cách đếm độc lập — khớp.

**Số người và số lượt tương tác**

| Đếm gì | x / N | % | Ghi chú |
|---|---|---|---|
| P1 người có hoạt động / tài khoản | 436/721 | 60.5% | khớp README BTC |
| P2 người hỏi trợ giảng / người có hoạt động | 144/436 | 33.0% | |
| Lượt trợ giảng / mọi lượt chat | 1.153/1.260 | 91.5% | còn lại là bạn học AI |
| V1 lượt trợ giảng / người (P2, 21 ngày) | TB 8.0 · trung vị 4 · p75 10 · p90 18 · max 72 | — | |
| V2 phiên hỏi / người (cách nhau ≤ 30 phút) | TB 2.2 · trung vị 1 · p90 4 | — | 321 phiên |
| V2 lượt / phiên | TB 3.6 · trung vị 2 · p90 8 | — | |

**V3 — tần suất sử dụng cho `cost/personas.yaml` (CP4)**

| Persona | Quy tắc | Người | Share | Phiên / tháng *(× 30/21)* | Lượt / phiên (TB) |
|---|---|---|---|---|---|
| `dung_it` | 1 phiên | 75/144 | 0.521 | 1.4 | 2.88 → 3 |
| `dung_vua` | 2–3 phiên | 48/144 | 0.333 | 3.4 | 3.74 → 4 |
| `dung_nhieu` | ≥4 phiên | 21/144 | 0.146 | 8.9 | 3.87 → 4 |

**Pain theo từng hướng**

| Mã | Đếm gì | x / N | % | Ghi chú |
|---|---|---|---|---|
| **M1** | Lượt trợ giảng **không có mốc trích dẫn** (13/11 → 25/11) | **231/576** | **40.1%** | ≥ ngưỡng 20% của giả thuyết. Khoảng chặn khi tính cả 7 lượt không ghi khoá: 39.6% … 40.8% |
| M1 | … chỉ câu hỏi dưới video | 231/557 | 41.5% | khung thảo luận: 0/19 |
| M1-độ nhạy | … bỏ 38 lượt AI ghi thiếu ngữ cảnh (37 trong số đó không có mốc) | 194/538 | 36.1% | vẫn ≥ 20%; người gặp 51/83 (61.4%) |
| M1 | Người nhận ≥1 câu trả lời không có mốc / người nhận trả lời trong cửa sổ | 58/86 | 67.4% | TB 3.98 lần / người gặp trong 13 ngày ≈ **9.2 lần / tháng** *(ngoại suy × 30/13)* |
| **M4** | Lượt trợ giảng ghi `missing_context = true` | 100/1.138 | 8.8% | người gặp: 50/142 (35.2%), TB 2.0 lần / 21 ngày ≈ 2.9 lần / tháng |
| M5 | Câu hỏi dưới video → hỏi tiếp cùng video trong 5 phút | 520/1.091 | 47.7% | 2 phút: 444/1.091 (40.7%) · 10 phút: 556/1.091 (51.0%) |
| M8 | `verdict` (46 dòng) / `reply_kind` (169 dòng) ghi ở đâu | verdict: 46/46 ở khung thảo luận, 44/46 (95.7%) là học viên trả lời lại một lời AI · reply_kind: 151/169 (89.3%) ở khung thảo luận, 107/169 do bạn học AI | — | hai trường này **chấm tin nhắn của học viên** (đúng / một phần / sai; kiểu tin nhắn), **không** cho biết trợ giảng có từ chối khi thiếu căn cứ |
| M7 | Độ trễ trợ giảng (không cache): trung vị / p90 | 2,4 s / 4,6 s | — | chờ > 10 s: 1/1.138 (0.1%) |

**Đối chiếu với giả thuyết (`evidence/hypothesis.md`) và kế hoạch §5.1**

- Vế data của giả thuyết ("≥ 20% phản hồi không có mốc trích dẫn") **đạt**: 40.1% (36.1% nếu bỏ các lượt có thể là câu hỏi lại). Vế phỏng vấn (≥ 2/3 người kể được tình huống cụ thể) chưa có số.
- Giả thuyết thay thế 4 (thời gian phản hồi): độ trễ trung vị 2,4 s, chỉ 0.1% lượt chờ > 10 s.
- A1.3: `verdict` / `reply_kind` không đo được hành vi từ chối (M8) → theo kế hoạch §5.1, A1.3 còn đo bằng phỏng vấn và benchmark.

## 4. ≥5 ví dụ cụ thể (mã dòng / mã đã ẩn danh, không đoán ai là ai)

Chọn tất định bằng `evidence/count.py` (lượt **sớm nhất** của mỗi kiểu — khoá `vi_du` trong `evidence/data-mining-output.json`). Chỉ ghi mã lượt chat (`chat.id`, BTC đã thay mã), không ghi mã học viên. Data không có câu chữ nên ví dụ là **metadata**, không phải trích dẫn lời học viên.

1. **`C01187`** — 13/11, hỏi trợ giảng dưới video `d06-r1-v01`: câu hỏi 92 ký tự → câu trả lời 600 ký tự, `moc_trich_dan = []`. *(M1)*
2. **`C00882`** — 13/11, dưới video `d05-r2-v06`: câu hỏi 18 ký tự → trả lời 220 ký tự, `moc_trich_dan = []`. *(M1)*
3. **`C00983`** — 05/11, dưới video `d01-r1-v05`: câu hỏi 29 ký tự → trả lời 182 ký tự, trợ giảng ghi `missing_context = true`. *(M4)*
4. **`C00992`** — 08/11, dưới video `d02-r2-v01`: câu hỏi 34 ký tự → trả lời 298 ký tự, `missing_context = true`. *(M4)*
5. **`C00581`** — 05/11, dưới video `d01-r1-v02`: câu hỏi 82 ký tự; trong 5 phút sau câu trả lời, cùng học viên hỏi tiếp về cùng video. *(M5)*
6. **`C00499`** — 05/11, cùng video `d01-r1-v02`: câu hỏi 183 ký tự; lại có câu hỏi tiếp trong 5 phút. *(M5)*

### Kiểm mẫu số và cách tính (CP3)

| Kiểm gì | Kết quả |
|---|---|
| P1 tự đếm so với README BTC (436 người có hoạt động) | 436 = 436 ✓ |
| Lượt trợ giảng tự đếm so với `chat.agent_id` | 1.153 = 1.153 ✓ |
| Số dòng 7 file + 38 loại việc so với README / `event_types.csv` (`prepare_data.py`) | khớp hết ✓ |
| M1, M4 đếm lại bằng đoạn code độc lập (không dùng `count.py`) | 231/576, u = 7 · 100/1.138 — khớp ✓ |
| M1 có lệch vì 7 lượt không ghi khoá không? | khoảng chặn 39.6% … 40.8% — kết luận không đổi |
| M1 có do lượt "hỏi lại" (AI ghi thiếu ngữ cảnh) kéo lên không? | bỏ 38 lượt đó (37 không có mốc): 194/538 (36.1%) — vẫn ≥ 20% |
| M1 có do lượt dùng lại (cache) kéo lên không? | không cache 226/561 (40.3%) · cache 5/15 (33.3%) |
| Độ nhạy M5 (2 · 5 · 10 phút) | 40.7% · 47.7% · 51.0% |
| Test tự động cho cách đếm | `python -m unittest discover -s evidence/tests` → 29/29 OK |

## 5. Giới hạn của data

Data cho biết người ta **làm gì**, không cho biết **vì sao**. Thiếu gì, lệch về phía nào:
- **Không có câu chữ** câu hỏi / câu trả lời → không biết câu trả lời không có mốc là sai, đúng hay chỉ thiếu căn cứ; không kết luận trợ giảng "bịa" (kế hoạch §4.4).
- `moc_trich_dan` chỉ ghi từ 13/11 (13 ngày) → M1 không nói gì về giai đoạn trước.
- `verdict` và `reply_kind` (kế hoạch §5.1 định dùng cho A1.3) chấm **tin nhắn của học viên** trong khung thảo luận (M8) → data **không** đo được việc trợ giảng từ chối khi thiếu căn cứ.
- M5 dùng cửa sổ 5 phút do nhóm tự chọn; hỏi tiếp có thể vì lý do khác.
- Lệch: chỉ 144/436 người có hoạt động từng hỏi trợ giảng, và vài người hỏi rất nhiều (max 72 lượt) → số theo lượt nghiêng về người hỏi nhiều; vì vậy luôn báo kèm số theo người.
- `occurred_at` theo đồng hồ máy học viên, giờ UTC; chỉ là một khoá, một nhóm lớp.

→ Kiểm lại bằng phỏng vấn P1–P4 (kế hoạch §4.3): câu 2 (làm gì để kiểm tra câu trả lời), câu 3–4 (lần gần nhất phải tua lại / hỏi lại, mất bao nhiêu phút → **T** cho Impact), câu 5 (mong trợ giảng xử lý thế nào khi không có trong bài → A1.3).

## 6. Số cho bảng Impact (kế hoạch §5.3 — TV1 chốt ở `spec.md` §2)

| Hướng | N — người gặp (cửa sổ quan sát) | F — lần / người gặp / tháng | N × F | T — phút / lần | Nguồn |
|---|---|---|---|---|---|
| A1.1 | 58 (trong 86 người nhận trả lời, 13/11–25/11) | ≈ 9.18 *(ngoại suy từ 3.98 lần / 13 ngày)* | ≈ 532 | **chưa có** — phỏng vấn | M1 |
| A1.2 | 50 (trong 142 người, 05/11–25/11) | ≈ 2.86 *(ngoại suy từ 2.0 lần / 21 ngày)* | ≈ 143 | **chưa có** — phỏng vấn | M4 |
| A1.3 | **không đo được từ data** (M8) | — | — | **chưa có** — phỏng vấn | kế hoạch §5.1: phỏng vấn, benchmark |

- N là số người **trong cửa sổ quan sát**, không phải mỗi tháng; chỉ là học viên khoá này trên trang pre-class.
- Tần suất cho persona (§8): V1–V3 ở mục 3.

## 7. Dữ liệu cho bộ câu thử (CP3 — bàn giao TV4)

Data **không có câu chữ** câu hỏi → không cung cấp được câu hỏi nguyên văn. Chỉ có độ dài câu hỏi, kèm tỉ lệ M4 / M1 theo độ dài (khoá `phan_ra.by_length`):

| Độ dài câu hỏi (ký tự) | Lượt trợ giảng | Thiếu ngữ cảnh (M4) | Không có mốc trích dẫn (M1, 13–25/11) |
|---|---|---|---|
| 1–20 | 187 (16.2%) | 23/187 (12.3%) | 36/73 (49.3%) |
| 21–60 | 416 (36.1%) | 46/411 (11.2%) | 59/191 (30.9%) |
| 61–150 | 515 (44.7%) | 27/505 (5.3%) | 133/301 (44.2%) |
| > 150 | 35 (3.0%) | 4/35 (11.4%) | 3/11 (27.3%) |

Mã lượt ví dụ: mục 4.

---
*Thay đổi ở CP3 (rà theo kế hoạch): đã bỏ các chỉ số không nằm trong cách đo của kế hoạch §5.1 — M2 / M3 (bấm link, tua lùi sau câu trả lời; dựa vào nghĩa `by = link` mà từ điển BTC không định nghĩa) và M6 (nhãn `rubric_bam_bai` của giám khảo AI, thay cho `verdict` / `reply_kind`). Số cũ còn trong lịch sử git (PR #4, #6, #9, #10).*
