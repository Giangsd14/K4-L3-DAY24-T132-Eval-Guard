# Phân tích lỗi Phase A

Nhóm: K4 Track 3A

Người phụ trách: Nguyễn Phát Thịnh - 2A202602645 (Member 1)

Nguồn: `artifacts/ragas_50q.json`; run timestamp: `2026-10-13T00:00:11.628925+00:00`.
Run là live, generation và evaluator dùng `deepseek-v4.1-flash`. Hai PDF scan
không có text layer bị bỏ qua; enrichment có response JSON lỗi/rate-limit và
được ghi nhận bằng fallback thực tế trong pipeline.

## Điểm theo distribution

| Metric | factual (20) | multi_hop (20) | adversarial (10) |
|---|---:|---:|---:|
| faithfulness | 0.9333 | 0.7115 | 0.8500 |
| answer_relevancy | 0.8963 | 0.7496 | 0.8722 |
| context_precision | 0.9167 | 0.8417 | 0.8833 |
| context_recall | 0.7583 | 0.6208 | 0.6583 |
| avg_score | 0.8762 | 0.7309 | 0.8160 |

## Bottom 10 và nguyên nhân

| Rank | ID | Distribution | Avg | Worst metric | Diagnosis | Suggested fix |
|---:|---:|---|---:|---|---|---|
| 1 | 5 | factual | 0.0000 | faithfulness | LLM hallucinating | Tighten system prompt, lower temperature |
| 2 | 39 | multi_hop | 0.4553 | context_precision | Too many irrelevant chunks | Add reranking or metadata filter |
| 3 | 26 | multi_hop | 0.4769 | faithfulness | LLM hallucinating | Tighten system prompt, lower temperature |
| 4 | 50 | adversarial | 0.5338 | faithfulness | LLM hallucinating | Tighten system prompt, lower temperature |
| 5 | 22 | multi_hop | 0.5833 | answer_relevancy | Answer doesn't match question | Improve prompt template |
| 6 | 38 | multi_hop | 0.6037 | faithfulness | LLM hallucinating | Tighten system prompt, lower temperature |
| 7 | 33 | multi_hop | 0.6250 | answer_relevancy | Answer doesn't match question | Improve prompt template |
| 8 | 49 | adversarial | 0.6569 | context_recall | Missing relevant chunks | Improve chunking or add BM25 |
| 9 | 37 | multi_hop | 0.6903 | context_recall | Missing relevant chunks | Improve chunking or add BM25 |
| 10 | 23 | multi_hop | 0.7051 | faithfulness | LLM hallucinating | Tighten system prompt, lower temperature |

Các câu multi-hop thấp chủ yếu cần ghép nhiều policy section, nên context
recall thấp hơn factual (0.6208 so với 0.7583). Câu 39 cần đối chiếu hai
version policy và câu 38 cần kết hợp ngày công tác, thành phố và giới hạn
khách sạn. Câu 5 có điểm 0 và cần kiểm tra lại retrieval/reference trước khi
kết luận là lỗi model. Câu 49 là bẫy version; điểm thấp không tự chứng minh
pipeline đã nhận diện đúng phủ định hoặc version hiện hành.

## Matrix và nhóm yếu nhất

```text
                         factual  multi_hop  adversarial
faithfulness                  1          6           1
answer_relevancy             10          4           1
context_precision             3          3           2
context_recall                6          7           6
```

Nhóm yếu theo mean thấp nhất là `multi_hop` với mean `0.7309`.
Worst metric xuất hiện nhiều nhất là `context_recall` với 19 câu. Tổng các
cột vẫn là 20/20/10; đó là kích thước nhóm, không phải chất lượng.

Ưu tiên cải thiện hierarchical chunking và hybrid BM25 cho truy vấn ghép
policy; sau đó dùng reranker/metadata filter để giảm context nhiễu. Chạy lại
đúng cùng `answers_50q.json`, ghi source hashes mới và so sánh riêng
`multi_hop.context_recall` cùng bottom 10.

## Bẫy adversarial và giới hạn

Adversarial có mean `0.8160`, thấp hơn factual `0.8762` nhưng cao hơn
multi-hop. Câu 50 liên quan cho phép VPN cá nhân và câu 49 liên quan policy
v2023/v2024; cần kiểm tra nội dung context để phân biệt lỗi phủ định/version
với lỗi retrieval. Mẫu adversarial chỉ có 10 câu, evaluator là một model
DeepSeek và enrichment có fallback do endpoint không ổn định, vì vậy không
được khẳng định quan hệ nhân quả chỉ từ điểm trung bình.
