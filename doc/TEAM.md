# Nhóm thực hiện K4 Track 3A

Tên nhóm: T132

Repo chung: https://github.com/Giangsd14/K4-L3-DAY24-T132-Eval-Guard

Trưởng nhóm/người nộp: Nguyễn Thanh Giang - 2A202602576

Ngày lab/deadline áp dụng: 13/10/2026

Commit dùng để chấm: b5d22d11ea9d685aeef049b6f88c0ef709876732

Mỗi nhóm nộp một repo. Điền đủ thành viên và một mục INDIVIDUAL cho từng người.
Thêm/xóa rows để khớp nhóm thật; mẫu ba rows không ép nhóm phải có ba người.

## Thành viên và phân công

| STT | Họ và tên | MSSV | Vai trò / công việc thật | Bằng chứng |
|---|---|---|---|---|
| 1 | Nguyễn Phát Thịnh | 2A202602645 | Member 1 / Evaluation Lead: Phase 0 (5 RAG modules m1-m5, answers_50q), Phase A (RAGAS evaluation), Phase B (LLM-as-a-judge G-Eval) | Commits cb16617, 28d432b, 9fccf8a, 4397ebc, f204598, a5c0295, 31cf15a, 8b0584f; artifacts answers_50q.json, ragas_50q.json, judge_results.json; failure_clusters.md, bias_report.md |
| 2 | Nguyễn Thanh Giang | 2A202602576 | Member 2 / Guardrails & Systems Lead: Phase C (Presidio PII, NeMo Guardrails, Latency profiling), Task 13 (CI/CD Blueprint), PR Integration | Commits 780983c, 620b3f2; artifacts guard_results.json; doc/reports/blueprint.md, docs/EVIDENCE_TRACKER.md; merge PR và giải quyết conflict config.py |

Người tích hợp/chạy batch/nộp link: Nguyễn Thanh Giang - 2A202602576 (thực hiện merge PR, giải quyết xung đột config.py, kiểm thử check_lab.py xuất xưởng và nộp link repo).

## Môi trường và chuẩn bị trước lớp

OS/Python/compiler: Ubuntu 24.04 WSL2, Linux 5.15 x86_64, Python 3.12.3, GCC/G++ 13.2.0 build Annoy 1.17.3 native.
Virtualenv/dependencies/imports: venv /home/haha/.venv_lab24, nemoguardrails 0.10.0, presidio-analyzer/anonymizer 2.2.364, spacy 3.8.16 (en_core_web_lg), ragas, langchain-openai. Toàn bộ import kiểm tra thành công.
Models/Qdrant/50 answers đã chuẩn bị: Qdrant 1.9.7 Docker container tại localhost:6333; API deepseek-v4.1-flash tại https://modelapi.vn/v1; 50 answers tạo live qua setup_answers.py và 4 artifacts JSON đúng chuẩn schema v2.
Nếu cài full NeMo chưa thành công, ghi lỗi thực tế; không dùng unit test pass hoặc pip resolve để khẳng định runtime đã chạy: NeMo Guardrails 0.10.0 đã được cài đặt và cấu hình thành công với custom provider FastChatOpenAI hỗ trợ auto-retry và timeout an toàn.

## INDIVIDUAL

Sao chép mẫu cho mỗi thành viên; tiêu đề họ tên không dấu-MSSV.

### Nguyen Phat Thinh-2A202602645

- Phần được giao và phần thực tế đã làm: Member 1/Evaluation Lead; chuẩn bị
  môi trường và 5 module RAG, tạo 50 answers live, implement Phase A Tasks
  1-4 và Phase B Tasks 5-8, chạy hai live evaluation.
- Bằng chứng: commits `cb16617`, `28d432b`, `9fccf8a`, `4397ebc`,
  `f204598`, `a5c0295`, `31cf15a`, `8b0584f`; artifacts `answers_50q.json`,
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

### Nguyen Thanh Giang-2A202602576

- Phần được giao và phần thực tế đã làm: Member 2/Guardrails & Systems Lead; triển khai toàn bộ Phase C (Task 9a PII scan với regex và spaCy NER tiếng Việt cho CCCD/SĐT/Email, Task 9b check_input_rail với NeMo Colang flow, Task 10 adversarial suite 28 inputs, Task 11 check_output_rail, Task 12 đo độ trễ P95 tuần tự); hoàn thiện bản phác thảo CI/CD Task 13 (blueprint.md); chủ trì merge nhánh và giải quyết xung đột tích hợp.
- Bằng chứng: commits `780983c`, `620b3f2` trên nhánh feat/guard-phase-c; artifacts `guard_results.json` (chặn 20/20 attacks đạt bonus +3đ, 8/8 clean controls allowed 0% FPR, 4/4 output cases đúng, 20 latency samples); report `blueprint.md`; script `src/phase_c_guard.py`.
- Cách kiểm tra: `pytest tests/test_phase_c.py -v` đạt 12/12 passed (0.11s); `scripts/run_experiments.py --phase c --live --latency-samples 20` chạy thực nghiệm thành công; `scripts/check_lab.py --with-tests` đạt 86 passed và 0 failed checks.
- Điều đã học: kiến trúc defense-in-depth nhiều tầng guardrail; đăng ký custom provider FastChatOpenAI cho NeMo với cơ chế retry và timeout; lọc thực thể PII mục tiêu loại bỏ hoàn toàn false positives trên tiếng Việt; đo lường độ trễ percentile tuyến tính và thiết kế CI/CD quality gates trong sản xuất.
- Giới hạn/cách xử lý: NeMo self-check gọi remote LLM API qua mạng công cộng có độ trễ cao (P95 đạt 9027ms); đã ghi nhận trung thực trong blueprint.md và đề xuất giải pháp thay thế bằng mô hình phân loại cục bộ SLM (DeBERTa / TensorRT-LLM) để đưa độ trễ về dưới 80ms.
- Nguồn/AI hỗ trợ nếu có: sử dụng Antigravity coding assistant để hỗ trợ phân tích traceback, rà soát hợp đồng JSON schemas, đối chiếu kiểm định rubric và tối ưu quy trình merge Git.

## Cập nhật sau khi nộp

Bản nộp chính thức trước hạn chót. Không có cập nhật sau deadline.
