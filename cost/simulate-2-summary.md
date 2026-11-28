# Tóm tắt mô phỏng simulate-2@20261128-093944

Do `python run.py simulate` sinh ra — không sửa tay. Chép bảng sang `cost/cost-estimate.md`.

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| dung_it | 28 | 3 | 1107 | 844 | 2.8 | 10.8 |
| dung_vua | 18 | 4 | 1441 | 1127 | 3.6 | 14.1 |
| dung_nhieu | 4 | 4 | 1528 | 939 | 3.8 | 15.0 |

Tỉ lệ đạt dùng để tính: 28/30 (93%) — lượt run-3@20261127-222235

- Tỉ lệ đạt lấy từ lượt nhóm chọn: eval/run-3.csv (--rate-from).

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (144 người) | Chi phí / tháng — cơ sở (436 người) | Chi phí / tháng — cao (721 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| gemini-3.1-flash-lite (vào 0.25 · ra 1.5 $/1M) | $0.0017 | $0.0019 | $0.00054 | $0.8313 | $2.52 | $4.16 | $0.0058 |
| gemini-2.5-pro (vào 1.25 · ra 10.0 $/1M) | $0.0111 | $0.0119 | $0.0035 | $5.28 | $15.98 | $26.42 | $0.0366 |

- Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt. Chi phí / câu hỏi đạt = chi phí / phiên ÷ số lượt hỏi trung bình mỗi phiên (3.4) ÷ tỉ lệ đạt — tỉ lệ đạt đo theo từng câu thử.
- Token đo trên model: nvidia/nemotron-3-ultra-550b-a55b:free. Giá tính theo từng model trong bảng — model khác bộ tách token thì số token thật có thể lệch; ghi rõ "đo trên model X, tính giá model Y" trong cost/cost-estimate.md.
- Phiên lỗi (không tính vào trung bình): 0/50.
