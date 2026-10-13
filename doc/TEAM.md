# Nhóm thực hiện K4 Track 3A

Tên nhóm: {{Tên nhóm}}

Repo chung: {{Link repo}}

Trưởng nhóm/người nộp: {{Họ tên và MSSV}}

Ngày lab/deadline áp dụng: {{Ngày giờ theo thông báo lớp}} — Asia/Ho_Chi_Minh (UTC+07:00)

Commit dùng để chấm: {{Commit SHA}}

Mỗi nhóm nộp một repo. Điền đủ thành viên và một mục INDIVIDUAL cho từng người.
Thêm/xóa rows để khớp nhóm thật; mẫu ba rows không ép nhóm phải có ba người.

## Thành viên và phân công

| STT | Họ và tên | MSSV | Vai trò / công việc thật | Bằng chứng |
|---|---|---|---|---|
| 1 | {{Họ tên}} | {{MSSV}} | {{Phase/file/hàm}} | {{Commit/PR/report}} |
| 2 | {{Họ tên}} | {{MSSV}} | {{Phase/file/hàm}} | {{Commit/PR/report}} |
| 3 | {{Họ tên}} | {{MSSV}} | {{Phase/file/hàm}} | {{Commit/PR/report}} |

Người tích hợp/chạy batch/nộp link: {{Họ tên, công việc và bằng chứng}}.

## Môi trường và chuẩn bị trước lớp

OS/Python/compiler: {{Phiên bản thực tế}}.
Virtualenv/dependencies/imports: {{Lệnh và kết quả}}.
Models/Qdrant/50 answers đã chuẩn bị: {{Bằng chứng và giới hạn/fallback}}.
Nếu cài full NeMo chưa thành công, ghi lỗi thực tế; không dùng unit test pass
hoặc pip resolve để khẳng định runtime đã chạy.

## INDIVIDUAL

### Nguyen Phat Thinh-2A202602645

- Phần được giao và phần thực tế đã làm: Member 1/Evaluation Lead; chuẩn bị
  môi trường và 5 module RAG, tạo 50 answers live, implement Phase A Tasks
  1-4 và Phase B Tasks 5-8, chạy hai live evaluation.
- Bằng chứng: commits `cb16617`, `28d432b`, `9fccf8a`, `4397ebc`,
  `f204598`, `a5c0295`, `31cf15a`; artifacts `answers_50q.json`,
  `ragas_50q.json`, `judge_results.json`; reports `failure_clusters.md` và
  `bias_report.md`.
- Cách kiểm tra: `pytest tests/test_phase_a.py tests/test_phase_b.py
  tests/test_report_contracts.py -q` đạt 44 passed; Phase A chạy 200 metric
  jobs và Phase B tạo 5 pairwise results cùng 10 calibration judgments.
- Điều đã học: cách giữ provenance model, source hashes, swap-and-average,
  Cohen's kappa và phân tích failure cluster theo worst metric.
- Giới hạn/cách xử lý: hai PDF scan không có text layer; enrichment DeepSeek
  có JSON lỗi/rate-limit. Các giới hạn được ghi nhận, không thay bằng số liệu
  giả.
- Nguồn/AI hỗ trợ nếu có: dùng coding assistant để rà contract và test; mọi
  artifact live, số đo và kết luận đều được kiểm tra lại từ file chạy thật.

Sao chép mẫu cho mỗi thành viên; tiêu đề họ tên không dấu-MSSV.

### {{HoVaTen}}-{{MSSV}}

- Phần được giao và phần thực tế đã làm: {{Nhiệm vụ, file/hàm, mục đích}}.
- Bằng chứng: {{Commit/PR và artifacts/reports liên quan}}.
- Cách kiểm tra: {{Unit mock hoặc live experiment, lệnh và kết quả}}.
- Điều đã học: {{Khái niệm và cách thể hiện trong bài}}.
- Giới hạn/cách xử lý: {{Vấn đề và kiểm chứng}}.
- Nguồn/AI hỗ trợ nếu có: {{Công cụ, phạm vi, cách tự kiểm chứng}}.

## Cập nhật sau khi nộp

{{Ghi phiên bản nộp; nếu sửa sau deadline, ghi commit/thời điểm/lý do và thông báo
coach cho phép áp dụng bản cập nhật. Nếu không có cập nhật, ghi rõ không có.}}
