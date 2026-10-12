# Bảng Phân công Nhiệm vụ Chi tiết (Task Assignment)
## K4 Track 3A — Production Eval + Guardrail Stack

> **Tài liệu này được thiết kế để từng thành viên có thể copy task tương ứng đưa thẳng vào AI coding agent (Codex / Antigravity) để thực thi mà không cần giải thích lại đề bài.**

---

# PHẦN I: MEMBER 1 — EVALUATION LEAD (Phase 0, Phase A, Phase B)

### Nhánh làm việc: `feat/eval-phase-ab`
### Tổng điểm phụ trách: 65 điểm bắt buộc + 7 điểm bonus (Tối đa 72 điểm)

---

### [Task 0.1] Setup Pipeline RAG & Environment
- **Người phụ trách**: Member 1
- **Mục tiêu**: Đưa 5 module RAG từ Day 18 (`m1_chunking.py`, `m2_search.py`, `m3_rerank.py`, `m4_eval.py`, `m5_enrichment.py`) vào `src/`; tạo `.env` từ `.env.example` với `OPENAI_API_KEY`; kiểm tra Qdrant v1.9.7 qua Docker.
- **File chỉnh sửa**: `src/m1_chunking.py`, `src/m2_search.py`, `src/m3_rerank.py`, `src/m4_eval.py`, `src/m5_enrichment.py`, `.env` (không commit `.env`).
- **Nguồn tài liệu**: `README.md`, `doc/ENVIRONMENT.md`, `doc/PIPELINE_INTERFACE.md`.
- **Dependency**: Không.
- **Làm song song với**: Task C.1 (Member 2 có thể code Presidio PII ngay).
- **Definition of Done (DoD)**: 5 file module tồn tại trong `src/`; `python -c "import src.m1_chunking"` không lỗi; Qdrant phản hồi tại `localhost:6333`.
- **Lệnh kiểm tra**: `python -c "from src import m1_chunking, m2_search, m3_rerank, m4_eval, m5_enrichment; print('OK')"`
- **Evidence**: Log import thành công; status Docker Qdrant.
- **Commit đề xuất**: `feat(setup): add RAG m1-m5 pipeline modules and config - [Member 1]`

---

### [Task 0.2] Sinh 50 Answers Thực nghiệm
- **Người phụ trách**: Member 1
- **Mục tiêu**: Chạy `python scripts/setup_answers.py --live` để sinh tập 50 câu trả lời từ RAG pipeline.
- **File tạo ra**: `artifacts/answers_50q.json`.
- **Nguồn tài liệu**: `README.md`, `doc/CHECKPOINTS.md` (CP0), `doc/REPORT_SCHEMAS.md`.
- **Dependency**: Task 0.1.
- **Làm song song với**: Task C.1, C.2 của Member 2.
- **Definition of Done (DoD)**: `artifacts/answers_50q.json` chứa đúng 50 bản ghi (20 factual, 20 multi_hop, 10 adversarial), giữ nguyên `id`, `question`, `distribution`, `ground_truth`; `generation_mode` là `"llm"`; `generation_model` là model ID (gpt-4o-mini).
- **Lệnh kiểm tra**: `python -c "import json; data=json.load(open('artifacts/answers_50q.json')); assert len(data)==50; print('50 answers valid')"`
- **Evidence**: `artifacts/answers_50q.json` đã sinh.
- **Commit đề xuất**: `feat(setup): generate 50 RAG answers with live pipeline - [Member 1]`

---

### [Task A.1] Implement Task 1 — `group_by_distribution`
- **Người phụ trách**: Member 1
- **Mục tiêu**: Hoàn thiện hàm `group_by_distribution(test_set)` nhóm 50 câu hỏi thành 3 nhóm đúng tỷ lệ 20/20/10.
- **File chỉnh sửa**: `src/phase_a_ragas.py`.
- **Nguồn tài liệu / Rubric**: `doc/RUBRIC.md` (Phase A Task 1 - 5 điểm); `doc/ASSIGNMENT.md` Task 1.
- **Dependency**: Không (có thể dùng `fixtures/test_set_50q.json`).
- **Làm song song với**: Task C.1, Task C.2 (Member 2).
- **DoD**: Trả về dict với 3 keys `"factual"` (20 phần tử), `"multi_hop"` (20 phần tử), `"adversarial"` (10 phần tử). Xóa `# TODO`.
- **Lệnh kiểm tra**: `pytest tests/test_phase_a.py -k test_group_exact_counts -q`
- **Evidence**: Terminal output của pytest PASS.
- **Commit đề xuất**: `feat(phase-a): implement Task 1 group_by_distribution - [Member 1]`

---

### [Task A.2] Implement Task 2 — `run_ragas_50q`
- **Người phụ trách**: Member 1
- **Mục tiêu**: Hoàn thiện hàm `run_ragas_50q(answers)` gọi `m4_eval.evaluate_ragas` tính 4 metrics (faithfulness, answer_relevancy, context_precision, context_recall), trả về `RagasEvaluation(results, raw["metadata"]["evaluator_models"])`. Chuyển đổi metric sang float chuẩn.
- **File chỉnh sửa**: `src/phase_a_ragas.py`.
- **Nguồn tài liệu / Rubric**: `doc/RUBRIC.md` (Phase A Task 2 - 10 điểm); `doc/PIPELINE_INTERFACE.md`.
- **Dependency**: Task A.1.
- **Làm song song với**: Task C.2, Task C.3 (Member 2).
- **DoD**: Trả về `RagasEvaluation` có 50 `RagasResult`, mỗi result có 4 metric hữu hạn trong $[0, 1]$, giữ đúng `evaluator_models`. Xóa `# TODO`.
- **Lệnh kiểm tra**: `pytest tests/test_phase_a.py -k test_ragas_adapter_preserves_rows -q`
- **Evidence**: Terminal output của pytest PASS.
- **Commit đề xuất**: `feat(phase-a): implement Task 2 run_ragas_50q evaluation adapter - [Member 1]`

---

### [Task A.3] Implement Task 3 — `bottom_10`
- **Người phụ trách**: Member 1
- **Mục tiêu**: Hoàn thiện hàm `bottom_10(results)` sắp xếp tăng dần theo `avg_score`, lấy 10 câu tệ nhất kèm rank (1-10), chẩn đoán lỗi (`diagnosis`) và giải pháp (`suggested_fix`) từ `DIAGNOSTIC_TREE`.
- **File chỉnh sửa**: `src/phase_a_ragas.py`.
- **Nguồn tài liệu / Rubric**: `doc/RUBRIC.md` (Phase A Task 3 - 7 điểm); `doc/ASSIGNMENT.md` Task 3.
- **Dependency**: Task A.2.
- **Làm song song với**: Task C.3 (Member 2).
- **DoD**: Trả về list 10 dicts với đầy đủ trường quy định, sắp xếp avg_score tăng dần. Xóa `# TODO`.
- **Lệnh kiểm tra**: `pytest tests/test_phase_a.py -k test_bottom_10 -q`
- **Evidence**: Terminal output của pytest PASS.
- **Commit đề xuất**: `feat(phase-a): implement Task 3 bottom_10 error diagnosis - [Member 1]`

---

### [Task A.4] Implement Task 4 — `cluster_analysis`
- **Người phụ trách**: Member 1
- **Mục tiêu**: Hoàn thiện hàm `cluster_analysis(results)` xây dựng ma trận `worst_metric × distribution`, tìm `dominant_failure_distribution` bằng mean avg_score thấp nhất (không chọn bằng tổng số câu), tìm `dominant_failure_metric` và sinh insight có nghĩa.
- **File chỉnh sửa**: `src/phase_a_ragas.py`.
- **Nguồn tài liệu / Rubric**: `doc/RUBRIC.md` (Phase A Task 4 - 8 điểm); `doc/ASSIGNMENT.md` Task 4.
- **Dependency**: Task A.3.
- **Làm song song với**: Task C.4 (Member 2).
- **DoD**: Ma trận 4x3 đếm đúng số câu theo metric thấp nhất của từng câu; nhóm yếu nhất tính theo mean thấp nhất. Xóa `# TODO`.
- **Lệnh kiểm tra**: `pytest tests/test_phase_a.py -k test_cluster_analysis -q`
- **Evidence**: Terminal output của pytest PASS.
- **Commit đề xuất**: `feat(phase-a): implement Task 4 cluster_analysis matrix - [Member 1]`

---

### [Task A.5] Chạy Live Phase A & Soạn Báo cáo `failure_clusters.md`
- **Người phụ trách**: Member 1
- **Mục tiêu**: Chạy `python scripts/run_experiments.py --phase a --live` sinh `artifacts/ragas_50q.json`; đối chiếu số liệu và điền hoàn chỉnh `doc/reports/failure_clusters.md` (xóa sạch mọi placeholder).
- **File chỉnh sửa / tạo ra**: `artifacts/ragas_50q.json`, `doc/reports/failure_clusters.md`.
- **Nguồn tài liệu / Rubric**: `doc/RUBRIC.md` (Phase A 30đ + Bonus Phase A +4đ nếu adversarial mean < factual mean); `doc/REPORT_SCHEMAS.md`.
- **Dependency**: Task 0.2 và Tasks A.1-A.4.
- **Làm song song với**: Task C.5, C.6 (Member 2).
- **DoD**: `artifacts/ragas_50q.json` pass schema; `doc/reports/failure_clusters.md` được điền đầy đủ bảng điểm, bottom 10, ma trận, phân tích bẫy version/negation (hướng tới bonus +4đ). Không còn placeholder `{{...}}`.
- **Lệnh kiểm tra**: `python -c "from src.report_contracts import validate_markdown; validate_markdown('doc/reports/failure_clusters.md'); print('Markdown valid')"`
- **Evidence**: `artifacts/ragas_50q.json`, `doc/reports/failure_clusters.md`.
- **Commit đề xuất**: `feat(phase-a): run live RAGAS eval and complete failure_clusters report - [Member 1]`

---

### [Task B.1] Implement Task 5 — `pairwise_judge`
- **Người phụ trách**: Member 1
- **Mục tiêu**: Hoàn thiện hàm `pairwise_judge(question, answer_a, answer_b, reference)` gọi LLM Judge đánh giá 2 câu trả lời dựa trên reference theo 3 tiêu chí: độ chính xác, đầy đủ, súc tích. Trả về JSON chứa `winner` ("A"|"B"|"tie"), `reasoning`, `scores`.
- **File chỉnh sửa**: `src/phase_b_judge.py`.
- **Nguồn tài liệu / Rubric**: `doc/RUBRIC.md` (Phase B Task 5 - 10 điểm); `doc/ASSIGNMENT.md` Task 5.
- **Dependency**: Không.
- **Làm song song với**: Task C.4, C.5 (Member 2).
- **DoD**: Trả về đúng format JSON; scores nằm trong $[0, 1]$; prompt sử dụng reference. Xóa `# TODO`.
- **Lệnh kiểm tra**: `pytest tests/test_phase_b.py -k test_pairwise_uses_json_judge -q`
- **Evidence**: Terminal output của pytest PASS.
- **Commit đề xuất**: `feat(phase-b): implement Task 5 pairwise_judge prompt and parser - [Member 1]`

---

### [Task B.2] Implement Task 6 — `swap_and_average`
- **Người phụ trách**: Member 1
- **Mục tiêu**: Hoàn thiện hàm `swap_and_average` gọi `pairwise_judge` 2 lượt (lượt 1: A,B; lượt 2: B,A). Quy đổi winner và scores của lượt 2 về không gian ban đầu. Quyết định đồng thuận (`final_winner` chỉ nhận A hoặc B nếu cả 2 lượt cùng chọn, ngược lại là `"tie"`).
- **File chỉnh sửa**: `src/phase_b_judge.py`.
- **Nguồn tài liệu / Rubric**: `doc/RUBRIC.md` (Phase B Task 6 - 10 điểm); `doc/ASSIGNMENT.md` Task 6.
- **Dependency**: Task B.1.
- **Làm song song với**: Task C.5 (Member 2).
- **DoD**: Trả về `JudgeResult` chứa thông tin 2 passes, `position_consistent`, và `final_winner`. Xóa `# TODO`.
- **Lệnh kiểm tra**: `pytest tests/test_phase_b.py -k test_swap_conversion_and_calls -q`
- **Evidence**: Terminal output của pytest PASS.
- **Commit đề xuất**: `feat(phase-b): implement Task 6 swap_and_average consistency logic - [Member 1]`

---

### [Task B.3] Implement Task 7 — `cohen_kappa`
- **Người phụ trách**: Member 1
- **Mục tiêu**: Hoàn thiện hàm `cohen_kappa(judge_labels, human_labels)` tính hệ số Cohen's $\kappa$ giữa nhãn của LLM Judge và nhãn của con người. Hỗ trợ trường hợp hoàn hảo và trường hợp mẫu nhỏ.
- **File chỉnh sửa**: `src/phase_b_judge.py`.
- **Nguồn tài liệu / Rubric**: `doc/RUBRIC.md` (Phase B Task 7 - 10 điểm; Bonus +3 điểm nếu $\kappa > 0.6$).
- **Dependency**: Không.
- **Làm song song với**: Task C.5, Task D.1 (Member 2).
- **DoD**: Trả về float $\kappa \in [-1, 1]$. Tính toán chính xác theo công thức $(P_o - P_e)/(1 - P_e)$. Xóa `# TODO`.
- **Lệnh kiểm tra**: `pytest tests/test_phase_b.py -k test_cohen_kappa -q`
- **Evidence**: Terminal output của pytest PASS.
- **Commit đề xuất**: `feat(phase-b): implement Task 7 cohen_kappa calculation - [Member 1]`

---

### [Task B.4] Implement Task 8 — `bias_report`
- **Người phụ trách**: Member 1
- **Mục tiêu**: Hoàn thiện hàm `bias_report(judge_results)` đo lường tỷ lệ thiên lệch vị trí (`position_bias_rate`) và thiên lệch độ dài (`verbosity_bias`), chi tiết số lượng A/B thắng khi dài hơn, và đưa ra `interpretation`.
- **File chỉnh sửa**: `src/phase_b_judge.py`.
- **Nguồn tài liệu / Rubric**: `doc/RUBRIC.md` (Phase B Task 8 - 5 điểm); `doc/ASSIGNMENT.md` Task 8.
- **Dependency**: Task B.2.
- **Làm song song với**: Task D.1 (Member 2).
- **DoD**: Trả về dict đầy đủ schema với các tỷ lệ trong $[0, 1]$. Xóa `# TODO`.
- **Lệnh kiểm tra**: `pytest tests/test_phase_b.py -k test_bias_report -q`
- **Evidence**: Terminal output của pytest PASS.
- **Commit đề xuất**: `feat(phase-b): implement Task 8 bias_report metrics - [Member 1]`

---

### [Task B.5] Chạy Live Phase B & Soạn Báo cáo `bias_report.md`
- **Người phụ trách**: Member 1
- **Mục tiêu**: Chạy `python scripts/run_experiments.py --phase b --live` sinh `artifacts/judge_results.json` (chấm 5 cặp A/B và 10 binary judgments); điền hoàn chỉnh `doc/reports/bias_report.md`.
- **File chỉnh sửa / tạo ra**: `artifacts/judge_results.json`, `doc/reports/bias_report.md`.
- **Nguồn tài liệu / Rubric**: `doc/RUBRIC.md` (Phase B 35đ + Bonus Phase B +3đ nếu $\kappa > 0.6$).
- **Dependency**: Task 0.2 và Tasks B.1-B.4.
- **Làm song song với**: Task D.1, Task D.2 (Member 2).
- **DoD**: `artifacts/judge_results.json` pass schema; `doc/reports/bias_report.md` điền đủ 5 cặp so sánh, 10 lượt calibration so với người, Cohen's $\kappa$, phân tích bias. Xóa sạch placeholder `{{...}}`.
- **Lệnh kiểm tra**: `python -c "from src.report_contracts import validate_markdown; validate_markdown('doc/reports/bias_report.md'); print('Markdown valid')"`
- **Evidence**: `artifacts/judge_results.json`, `doc/reports/bias_report.md`.
- **Commit đề xuất**: `feat(phase-b): run live judge experiment and complete bias report - [Member 1]`

---

# PHẦN II: MEMBER 2 — GUARDRAILS & SYSTEMS LEAD (Phase C, Task 13, Integration)

### Nhánh làm việc: `feat/guard-phase-c`
### Tổng điểm phụ trách: 35 điểm bắt buộc + 3 điểm bonus + Task 13 Blueprint (Tối đa 38 điểm)

---

### [Task C.1] Implement Task 9a — `pii_scan` (Presidio Detection & Redaction)
- **Người phụ trách**: Member 2
- **Mục tiêu**: Hoàn thiện hàm `pii_scan(text, analyzer, anonymizer)` sử dụng Presidio AnalyzerEngine và AnonymizerEngine. Đăng ký các PatternRecognizer cho dữ liệu Việt Nam: CCCD/CMND (`VN_CCCD`: 9 hoặc 12 số), Số điện thoại (`VN_PHONE`: đầu 03,05,07,08,09 + 8 số), Email (`EMAIL_ADDRESS`). Trả về `has_pii`, danh sách `entities` (kèm start/end), và văn bản đã ẩn danh `anonymized`.
- **File chỉnh sửa**: `src/phase_c_guard.py`.
- **Nguồn tài liệu / Rubric**: `doc/RUBRIC.md` (Phase C Task 9a - 10 điểm); `doc/ASSIGNMENT.md` Task 9a.
- **Dependency**: Không (chạy độc lập ngay từ đầu bài Lab).
- **Làm song song với**: Task 0.1, 0.2, A.1 (Member 1).
- **DoD**: Phát hiện và thay thế chính xác CCCD, SĐT, Email bằng các tag `<VN_CCCD>`, `<VN_PHONE>`, `<EMAIL_ADDRESS>`. Xóa `# TODO`.
- **Lệnh kiểm tra**: `pytest tests/test_phase_c.py -k test_pii_scan -q`
- **Evidence**: Terminal output của pytest PASS.
- **Commit đề xuất**: `feat(phase-c): implement Task 9a Presidio PII scan with VN patterns - [Member 2]`

---

### [Task C.2] Implement Task 9b — `check_input_rail` (Async NeMo Rail)
- **Người phụ trách**: Member 2
- **Mục tiêu**: Hoàn thiện hàm async `check_input_rail(text, rails)` gọi `rails.generate_async` với `options={"rails": ["input"], "log": {"activated_rails": True}}`. Đọc quyết định chặn từ `result.log.activated_rails` (bất kỳ rail nào có `rail.stop == True`), tuyệt đối KHÔNG đoán bằng từ khóa refusal trong text.
- **File chỉnh sửa**: `src/phase_c_guard.py`.
- **Nguồn tài liệu / Rubric**: `doc/RUBRIC.md` (Phase C Task 9b - 5 điểm); `doc/ASSIGNMENT.md` Task 9b.
- **Dependency**: Không.
- **Làm song song với**: Task A.1, A.2 (Member 1).
- **DoD**: Trả về `{"allowed": bool, "blocked_reason": str|None, "response": str}`. Xóa `# TODO`.
- **Lệnh kiểm tra**: `pytest tests/test_phase_c.py -k test_input_rail -q`
- **Evidence**: Terminal output của pytest PASS.
- **Commit đề xuất**: `feat(phase-c): implement Task 9b check_input_rail using activated_rails - [Member 2]`

---

### [Task C.3] Implement Task 10 — `run_adversarial_suite` (Suite 20 Attacks + 8 Clean)
- **Người phụ trách**: Member 2
- **Mục tiêu**: Hoàn thiện hàm `run_adversarial_suite(adversarial_set, rails, analyzer, anonymizer)` chạy tuần tự Full Guard Stack cho batch 28 câu:
  1. Tầng 1: `pii_scan` $\rightarrow$ chặn nếu có PII (`blocked_by = "presidio"`).
  2. Tầng 2: Nếu chưa chặn, chạy `check_input_rail` $\rightarrow$ chặn nếu input rail kích hoạt (`blocked_by = "nemo_input"`).
  Xử lý async bên trong 1 event loop duy nhất bằng `asyncio.run(_run_all())` bọc ngoài, không gọi `asyncio.run()` trong vòng lặp.
- **File chỉnh sửa**: `src/phase_c_guard.py`.
- **Nguồn tài liệu / Rubric**: `doc/RUBRIC.md` (Phase C Task 10 - 10 điểm; Bonus +3đ nếu attacks $\ge 18/20$ và clean controls $8/8$).
- **Dependency**: Task C.1, Task C.2.
- **Làm song song với**: Task A.3, A.4 (Member 1).
- **DoD**: Trả về 28 kết quả có `id`, `category`, `input`, `expected`, `actual`, `blocked_by`, `passed`. Đạt $\ge 15/20$ attacks và $8/8$ clean allowed. Xóa `# TODO`.
- **Lệnh kiểm tra**: `pytest tests/test_phase_c.py -k test_adversarial_suite -q`
- **Evidence**: Terminal output của pytest PASS.
- **Commit đề xuất**: `feat(phase-c): implement Task 10 run_adversarial_suite pipeline - [Member 2]`

---

### [Task C.4] Implement Task 11 — `check_output_rail` (Async NeMo Output)
- **Người phụ trách**: Member 2
- **Mục tiêu**: Hoàn thiện hàm async `check_output_rail(question, answer, rails)` đưa cả ngữ cảnh câu hỏi và câu trả lời vào `rails.generate_async(options={"rails": ["output"]})`. Kiểm tra `activated_rails`, giữ nguyên nếu sạch hoặc trả về response đã redact nếu vi phạm.
- **File chỉnh sửa**: `src/phase_c_guard.py`.
- **Nguồn tài liệu / Rubric**: `doc/RUBRIC.md` (Phase C Task 11 - 5 điểm); `doc/ASSIGNMENT.md` Task 11.
- **Dependency**: Không.
- **Làm song song với**: Task B.1 (Member 1).
- **DoD**: Trả về `{"safe": bool, "flagged_reason": str|None, "final_answer": str}`. Xóa `# TODO`.
- **Lệnh kiểm tra**: `pytest tests/test_phase_c.py -k test_output_rail -q`
- **Evidence**: Terminal output của pytest PASS.
- **Commit đề xuất**: `feat(phase-c): implement Task 11 check_output_rail - [Member 2]`

---

### [Task C.5] Implement Task 12 — `measure_p95_latency` (Linear Percentiles)
- **Người phụ trách**: Member 2
- **Mục tiêu**: Hoàn thiện hàm `measure_p95_latency(test_inputs, n_runs=20, ...)` đo độ trễ tuần tự `input_layers_sequential`:
  1. Chạy 2 lần warm-up thật bị loại bỏ khỏi thống kê mẫu.
  2. Thu thập đủ $n\_runs \ge 20$ mẫu đo timed bằng `time.perf_counter()`, luôn đo cả Presidio và NeMo input (không short-circuit).
  3. Sử dụng helper `summarize_latency` để tính P50, P95, P99 theo phương pháp nội suy tuyến tính (`linear`).
- **File chỉnh sửa**: `src/phase_c_guard.py`.
- **Nguồn tài liệu / Rubric**: `doc/RUBRIC.md` (Phase C Task 12 - 5 điểm); `doc/ASSIGNMENT.md` Task 12.
- **Dependency**: Task C.1, Task C.2.
- **Làm song song với**: Task B.2, B.3 (Member 1).
- **DoD**: Trả về dict đúng schema với $n\_samples \ge 20$, $warmup\_runs = 2$, đủ các trường `presidio_ms`, `nemo_input_ms`, `input_guard_ms`. Xóa `# TODO`.
- **Lệnh kiểm tra**: `pytest tests/test_phase_c.py -k test_latency -q`
- **Evidence**: Terminal output của pytest PASS.
- **Commit đề xuất**: `feat(phase-c): implement Task 12 measure_p95_latency profiler - [Member 2]`

---

### [Task C.6] Chạy Live Phase C & Xuất `artifacts/guard_results.json`
- **Người phụ trách**: Member 2
- **Mục tiêu**: Chạy `python scripts/run_experiments.py --phase c --live --latency-samples 20` để sinh kết quả thực tế cho Phase C.
- **File tạo ra**: `artifacts/guard_results.json`.
- **Nguồn tài liệu / Rubric**: `doc/RUBRIC.md` (Phase C 35 điểm + Bonus Phase C +3 điểm).
- **Dependency**: Tasks C.1–C.5.
- **Làm song song với**: Task A.5, Task B.5 (Member 1).
- **DoD**: File `artifacts/guard_results.json` được tạo, hợp lệ theo `phase_c.schema.json`, attacks pass $\ge 15/20$ (hướng tới $\ge 18/20$ để lấy bonus), clean pass $8/8$, samples $\ge 20$.
- **Lệnh kiểm tra**: `python -c "from src.report_contracts import read_json, validate_metadata; r=read_json('artifacts/guard_results.json'); print('Guard results valid')"`
- **Evidence**: `artifacts/guard_results.json`.
- **Commit đề xuất**: `feat(phase-c): execute live guard experiment with 20 latency samples - [Member 2]`

---

### [Task D.1] Task 13 — Thiết kế Bản phác thảo CI/CD `blueprint.md`
- **Người phụ trách**: Member 2
- **Mục tiêu**: Điền hoàn chỉnh `doc/reports/blueprint.md` dựa trên dữ liệu thực tế từ Task C.6:
  - Sơ đồ kiến trúc & luồng dữ liệu (Data flow, failure action, secrets management, fallback).
  - Bảng độ trễ Presidio / NeMo / Input Guard tuần tự (điền đúng số liệu P50, P95, P99 đo được). Ghi rõ RAG/Output guard là "chưa đo" kèm kế hoạch.
  - Đề xuất CI Gates: RAGAS Faithfulness $\ge 0.75$, avg_score $\ge 0.65$, Attacks $\ge 18/20$, Clean $8/8$, lệnh trả về exit code nonzero.
  - Kế hoạch monitoring, xử lý false-positives, drift, và 3-5 đề xuất cải tiến cụ thể.
- **File chỉnh sửa**: `doc/reports/blueprint.md`.
- **Nguồn tài liệu / Rubric**: `doc/RUBRIC.md` (Task 13 Blueprint - bắt buộc, thiếu bị trừ 10 điểm); `doc/ASSIGNMENT.md` Task 13.
- **Dependency**: Task C.6 (cần số liệu latency thật).
- **Làm song song với**: Task B.5 (Member 1).
- **DoD**: Xóa sạch placeholder `{{...}}`, không để sót dấu `?`, đầy đủ bảng số liệu và đề xuất kỹ thuật.
- **Lệnh kiểm tra**: `python -c "from src.report_contracts import validate_markdown; validate_markdown('doc/reports/blueprint.md'); print('Blueprint valid')"`
- **Evidence**: `doc/reports/blueprint.md`.
- **Commit đề xuất**: `docs(blueprint): finalize production CI/CD architecture and latency blueprint - [Member 2]`

---

### [Task D.2] Tích hợp PR, Hoàn tất `doc/TEAM.md` & Kiểm định Xuất xưởng
- **Người phụ trách**: Member 1 & Member 2 (Phối hợp)
- **Mục tiêu**:
  1. Review và merge cả 2 PR (`feat/eval-phase-ab` và `feat/guard-phase-c`) vào `main`.
  2. Cả 2 thành viên điền đầy đủ thông tin vào `doc/TEAM.md` (Họ tên, MSSV, vai trò, commit SHA, mục `INDIVIDUAL`).
  3. Chạy `python scripts/check_lab.py --with-tests` để kiểm tra toàn diện.
- **File chỉnh sửa**: `doc/TEAM.md`.
- **Nguồn tài liệu / Rubric**: `doc/SUBMISSION.md`, `doc/RULES.md`.
- **Dependency**: Tất cả các tasks trên cả 2 nhánh đã hoàn thành.
- **DoD**: Lệnh `check_lab.py --with-tests` báo `0 failed checks` và `PASS` toàn bộ; Git log sạch secrets.
- **Lệnh kiểm tra**: `python scripts/check_lab.py --with-tests`
- **Evidence**: Terminal log `0 failed checks`; commit SHA cuối cùng.
- **Commit đề xuất**: `docs(team): update team contributions and finalize submission checks - [Team]`
