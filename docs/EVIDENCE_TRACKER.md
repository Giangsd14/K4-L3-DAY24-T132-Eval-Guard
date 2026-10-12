# Bảng Theo dõi Bằng chứng & Đánh giá Rubric (Evidence Tracker)
## K4 Track 3A — Production Eval + Guardrail Stack

> **Mục tiêu**: Đảm bảo mọi tiêu chí chấm điểm trong `doc/RUBRIC.md` đều có bằng chứng số liệu và file cụ thể tương ứng, phân định rõ ràng giữa **Yêu cầu bắt buộc của Rubric** và **Đề xuất bổ sung**.

---

## 1. Bảng Theo dõi Tổng hợp theo Rubric

| Task ID | Tiêu chí Rubric | Điểm Rubric | Người phụ trách | Loại Evidence | Vị trí lưu Evidence | Lệnh kiểm tra xác minh | Trạng thái |
|---|---|---:|---|---|---|---|:---:|
| **Task 0.1** | Đầy đủ 5 module RAG m1-m5 trong `src/` | *Tiền đề* | Member 1 | **Bắt buộc** | `src/m1_chunking.py` ... `m5_enrichment.py` | `scripts/check_lab.py` | Pending |
| **Task 0.2** | 50 câu trả lời RAG thật (`answers_50q.json`) | *Tiền đề (-30đ nếu thiếu)* | Member 1 | **Bắt buộc** | `artifacts/answers_50q.json` | `scripts/check_lab.py` | Pending |
| **Task A.1** | Group đúng 20 factual, 20 multi_hop, 10 adversarial | 5 | Member 1 | **Bắt buộc** | `src/phase_a_ragas.py`, Pytest log | `pytest tests/test_phase_a.py -k test_group_exact_counts` | Pending |
| **Task A.2** | `RagasEvaluation` 50 kết quả thật, 4 metric hữu hạn $[0,1]$ | 10 | Member 1 | **Bắt buộc** | `src/phase_a_ragas.py`, `artifacts/ragas_50q.json` | `pytest tests/test_phase_a.py -k test_ragas_adapter_preserves_rows` | Pending |
| **Task A.3** | Bottom 10 câu tăng avg_score, đầy đủ rank/diagnosis/fix | 7 | Member 1 | **Bắt buộc** | `src/phase_a_ragas.py`, `doc/reports/failure_clusters.md` | `pytest tests/test_phase_a.py -k test_bottom_10` | Pending |
| **Task A.4** | Ma trận worst_metric × dist, nhóm yếu nhất theo mean | 8 | Member 1 | **Bắt buộc** | `src/phase_a_ragas.py`, `doc/reports/failure_clusters.md` | `pytest tests/test_phase_a.py -k test_cluster_analysis` | Pending |
| **Bonus A** | Adversarial mean < factual mean, kèm phân tích bẫy | +4 (Bonus) | Member 1 | **Bonus** | `artifacts/ragas_50q.json`, `doc/reports/failure_clusters.md` | Đối chiếu điểm trung bình trong report | Pending |
| **Task B.1** | Pairwise LLM judge 5 cặp cố định (ids 1,5,12,21,41) | 10 | Member 1 | **Bắt buộc** | `src/phase_b_judge.py`, `artifacts/judge_results.json` | `pytest tests/test_phase_b.py -k test_pairwise_uses_json_judge` | Pending |
| **Task B.2** | Swap-and-average 2 lượt/cặp, hoán đổi thứ tự | 10 | Member 1 | **Bắt buộc** | `src/phase_b_judge.py`, `artifacts/judge_results.json` | `pytest tests/test_phase_b.py -k test_swap_conversion_and_calls` | Pending |
| **Task B.3** | Cohen's $\kappa$ trên 10 nhãn binary so với người | 10 | Member 1 | **Bắt buộc** | `src/phase_b_judge.py`, `artifacts/judge_results.json` | `pytest tests/test_phase_b.py -k test_cohen_kappa` | Pending |
| **Task B.4** | Position bias & verbosity bias rate có diễn giải | 5 | Member 1 | **Bắt buộc** | `src/phase_b_judge.py`, `doc/reports/bias_report.md` | `pytest tests/test_phase_b.py -k test_bias_report` | Pending |
| **Bonus B** | Cohen's $\kappa > 0.6$ trên 10 supplied model_answers | +3 (Bonus) | Member 1 | **Bonus** | `artifacts/judge_results.json`, `doc/reports/bias_report.md` | Kiểm tra giá trị kappa trong report | Pending |
| **Task C.1** | Presidio detect/redact CCCD/CMND, VN phone, email | 10 | Member 2 | **Bắt buộc** | `src/phase_c_guard.py`, Pytest log | `pytest tests/test_phase_c.py -k test_pii_scan` | **Unit Passed (5/5)** |
| **Task C.2** | Async input rail phản ánh activated_rails | 5 | Member 2 | **Bắt buộc** | `src/phase_c_guard.py`, Pytest log | `pytest tests/test_phase_c.py -k test_input_rail` | **Unit Passed (2/2)** |
| **Task C.3** | 20 attacks $\ge 15/20$; clean controls $8/8$ allowed | 10 | Member 2 | **Bắt buộc** | `src/phase_c_guard.py`, Pytest log | `pytest tests/test_phase_c.py -k "test_input_suite_exact_rows or test_attack_and_clean_control"` | **Unit Passed (2/2)** |
| **Task C.4** | Output rail: giữ output sạch, redact output nhạy cảm | 5 | Member 2 | **Bắt buộc** | `src/phase_c_guard.py`, Pytest log | `pytest tests/test_phase_c.py -k test_output_checks_supplied_answer` | **Unit Passed (2/2)** |
| **Task C.5** | Latency input layers: warm-up 2, $\ge 20$ samples, linear P95 | 5 | Member 2 | **Bắt buộc** | `src/phase_c_guard.py`, `artifacts/guard_results.json` | `pytest tests/test_phase_c.py -k test_latency` | Pending |
| **Bonus C** | Attacks $\ge 18/20$ VÀ clean controls $8/8$ allowed | +3 (Bonus) | Member 2 | **Bonus** | `artifacts/guard_results.json`, `doc/reports/blueprint.md` | Đối chiếu pass counts trong guard_results | Pending |
| **Task D.1** | Bản thiết kế CI/CD Blueprint đầy đủ, không để trống | *Tiền đề (-10đ nếu thiếu)* | Member 2 | **Bắt buộc** | `doc/reports/blueprint.md` | `scripts/check_lab.py` | Pending |
| **Task D.2** | Phân công nhóm, INDIVIDUAL, 0 lỗi checker | *Tiền đề* | Cả nhóm | **Bắt buộc** | `doc/TEAM.md`, Git log | `python scripts/check_lab.py --with-tests` | Pending |

---

## 2. Phân loại Bằng chứng (Evidence Taxonomy)

### 2.1 Bằng chứng bắt buộc theo Rubric (Mandatory Evidence)
1. **Source code sạch TODO**: 3 file `src/phase_a_ragas.py`, `src/phase_b_judge.py`, `src/phase_c_guard.py` và 5 module `m1-m5`.
2. **Bốn file JSON trong `artifacts/`**: Chứa dữ liệu chạy live thật, đúng schema phiên bản 2, có timestamp và tách riêng 4 vai trò model (`generation`, `evaluator`, `judge`, `guard`).
3. **Ba file Markdown trong `doc/reports/`**: Điền đầy đủ các bảng số liệu, không giữ placeholder `{{...}}`, không giữ dấu `?`.
4. **Hồ sơ nhóm `doc/TEAM.md`**: Có MSSV, nhiệm vụ, bằng chứng đóng góp, và mục `INDIVIDUAL` riêng biệt cho từng người.
5. **Git Commit History**: Mỗi thành viên có commit gắn với Task ID trên repo chung.

### 2.2 Bằng chứng đề xuất bổ sung (Recommended Additional Evidence)
1. **Test Logs**: Lưu lại output của `pytest tests/ -q` và `scripts/check_lab.py --with-tests` vào file log hoặc phần ghi chú trong `doc/TEAM.md` để chứng minh đã kiểm thử nghiêm ngặt.
2. **Pull Request Descriptions**: Mô tả chi tiết PR #1 và PR #2 kèm link tới các Task ID để tạo bằng chứng review rõ ràng trong Git workflow.
3. **Docker Status Log**: Ghi lại log xác nhận Qdrant đã pin đúng phiên bản `qdrant/qdrant:v1.9.7`.

---

## 3. Ma trận Đối chiếu Đóng góp Cá nhân (Contribution Alignment)

| Thành viên | Vai trò | Trọng số Rubric | Bằng chứng Code | Bằng chứng Thực nghiệm | Bằng chứng Báo cáo |
|---|---|:---:|---|---|---|
| **Member 1** | Evaluation Lead | 65đ + 7đ bonus | `phase_a_ragas.py`, `phase_b_judge.py` | `answers_50q.json`, `ragas_50q.json`, `judge_results.json` | `failure_clusters.md`, `bias_report.md`, `TEAM.md` (INDIVIDUAL 1) |
| **Member 2** | Guardrails & Systems Lead | 35đ + 3đ bonus + Blueprint | `phase_c_guard.py` | `guard_results.json` (20 latency samples, 28 inputs) | `blueprint.md`, `TEAM.md` (INDIVIDUAL 2), Check lab audit |

