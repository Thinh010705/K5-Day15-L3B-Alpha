# Tóm tắt mô phỏng simulate-1@20261128-092259

Do `python run.py simulate` sinh ra — không sửa tay. Chép bảng sang `cost/cost-estimate.md`.

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| dung_it | 9 | 3 | 1199 | 1102 | 3.0 | 11.7 |
| dung_vua | 6 | 4 | 1366 | 985 | 3.5 | 13.3 |
| dung_nhieu | 1 | 4 | 1610 | 1374 | 4.0 | 16.0 |

Tỉ lệ đạt dùng để tính: 28/30 (93%) — lượt run-3@20261127-222235

- Tỉ lệ đạt lấy từ lượt nhóm chọn: eval/run-3.csv (--rate-from).

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (144 người) | Chi phí / tháng — cơ sở (436 người) | Chi phí / tháng — cao (721 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| gemini-3.1-flash-lite (vào 0.25 · ra 1.5 $/1M) | $0.0019 | $0.0021 | $0.00060 | $0.9626 | $2.91 | $4.82 | $0.0067 |
| gemini-2.5-pro (vào 1.25 · ra 10.0 $/1M) | $0.0124 | $0.0132 | $0.0039 | $6.15 | $18.61 | $30.77 | $0.0427 |

- Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt. Chi phí / câu hỏi đạt = chi phí / phiên ÷ số lượt hỏi trung bình mỗi phiên (3.4) ÷ tỉ lệ đạt — tỉ lệ đạt đo theo từng câu thử.
- Token đo trên model: nvidia/nemotron-3-ultra-550b-a55b:free. Giá tính theo từng model trong bảng — model khác bộ tách token thì số token thật có thể lệch; ghi rõ "đo trên model X, tính giá model Y" trong cost/cost-estimate.md.
- Phiên lỗi (không tính vào trung bình): 34/50.
