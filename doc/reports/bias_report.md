# Đánh giá LLM Judge Phase B

Nhóm: K4 Track 3A

Người phụ trách: Nguyễn Phát Thịnh - 2A202602645 (Member 1)

Nguồn: `artifacts/judge_results.json`; run timestamp:
`2026-10-13T00:10:03.526278+00:00`. Generation và judge dùng
`deepseek-v4.1-flash`.

## Năm cặp A/B và hai lượt

Nguồn cố định: A từ `artifacts/answers_50q.json:answer`; B từ
`fixtures/human_labels_10q.json:model_answer`; reference từ
`fixtures/test_set_50q.json:ground_truth`. IDs: 1, 5, 12, 21, 41.

| ID | Winner pass 1 | Winner pass 2 (đã quy về A/B gốc) | Final | Consistent | Scores pass 1 / pass 2 |
|---:|---|---|---|---|---|
| 1 | B | B | B | true | A 0.8/B 0.95; A 0.6/B 0.8 |
| 5 | tie | tie | tie | true | A 0/B 0; A 0/B 0 |
| 12 | A | A | A | true | A 1/B 0.9; A 1/B 0.8 |
| 21 | B | B | B | true | A 0.5/B 1; A 0.5/B 1 |
| 41 | A | A | A | true | A 1/B 0; A 1/B 0 |

Position bias count/rate: `0 / 5 = 0.0`. Verbosity win rate: `0.5`;
decisive cases: `4`. Không có case không nhất quán trong năm cặp. Hai case
decisive chọn answer dài hơn (một A, một B), đây là tín hiệu mô tả chứ chưa
đủ mẫu để kết luận judge có verbosity bias.

## Calibration đúng model_answer

Judge nhận đúng `question`, `model_answer` và reference; không nhận
`human_label`, `human_note` hoặc phân bố nhãn human.

| ID | Judge label | Human label | Agree |
|---:|---:|---:|---|
| 1 | 1 | 1 | true |
| 5 | 0 | 0 | true |
| 12 | 1 | 1 | true |
| 21 | 1 | 1 | true |
| 23 | 1 | 1 | true |
| 29 | 0 | 0 | true |
| 33 | 1 | 1 | true |
| 41 | 0 | 0 | true |
| 46 | 1 | 1 | true |
| 50 | 0 | 0 | true |

Cohen's kappa: `1.0`. Observed agreement là `10/10 = 1.0`; chance
agreement cũng là `0.52` theo phân bố nhãn; kappa đạt 1.0 vì observed
agreement bằng 1.0. Đây là kết quả trên chỉ 10 nhãn, không phải bằng chứng
đủ để khẳng định khả năng tổng quát.

## Giới hạn và cách dùng judge

Judge dùng prompt JSON với ba tiêu chí accuracy, completeness và conciseness,
chạy hai lượt swap cho 5 cặp. Calibration dùng 10 `model_answer` cố định.
Kappa hoàn hảo nhưng mẫu nhỏ và cùng một model/provider nên cần kiểm chứng
thêm bằng người đánh giá độc lập, tăng số câu và theo dõi các case tie hoặc
không nhất quán. Judge là công cụ đo lường có provenance, không phải đáp án
tuyệt đối.
