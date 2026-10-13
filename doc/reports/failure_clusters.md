# Phân tích lỗi Phase A

Nhóm: K4 Track 3A

Người phụ trách: Nguyễn Phát Thịnh - 2A202602645 (Member 1)

Nguồn: `artifacts/ragas_50q.json`; run timestamp: `2026-10-13T00:38:54.744706+00:00`.
Run là live, generation/evaluator LLM dùng `deepseek-v4.1-flash` và evaluator
embedding dùng `BAAI/bge-m3`. Hai PDF scan không có text layer bị bỏ qua;
enrichment có response JSON lỗi/rate-limit và được ghi nhận bằng fallback thực tế.

## Điểm theo distribution

| Metric | factual (20) | multi_hop (20) | adversarial (10) |
|---|---:|---:|---:|
| faithfulness | 0.9500 | 0.6904 | 0.8600 |
| answer_relevancy | 0.8995 | 0.6593 | 0.8619 |
| context_precision | 0.8667 | 0.7625 | 0.9333 |
| context_recall | 0.7083 | 0.5958 | 0.6333 |
| avg_score | 0.8561 | 0.6770 | 0.8221 |

## Bottom 10 và nguyên nhân

| Rank | ID | Distribution | Avg | Worst metric | Diagnosis | Suggested fix |
|---:|---:|---|---:|---|---|---|
| 1 | 5 | factual | 0.0000 | faithfulness | LLM hallucinating | Tighten system prompt, lower temperature |
| 2 | 30 | multi_hop | 0.3523 | answer_relevancy | Answer doesn't match question | Improve prompt template |
| 3 | 33 | multi_hop | 0.3958 | answer_relevancy | Answer doesn't match question | Improve prompt template |
| 4 | 22 | multi_hop | 0.4583 | answer_relevancy | Answer doesn't match question | Improve prompt template |
| 5 | 50 | adversarial | 0.4699 | faithfulness | LLM hallucinating | Tighten system prompt, lower temperature |
| 6 | 39 | multi_hop | 0.4908 | context_precision | Too many irrelevant chunks | Add reranking or metadata filter |
| 7 | 27 | multi_hop | 0.5000 | answer_relevancy | Answer doesn't match question | Improve prompt template |
| 8 | 21 | multi_hop | 0.5208 | answer_relevancy | Answer doesn't match question | Improve prompt template |
| 9 | 24 | multi_hop | 0.5941 | faithfulness | LLM hallucinating | Tighten system prompt, lower temperature |
| 10 | 26 | multi_hop | 0.6483 | context_precision | Too many irrelevant chunks | Add reranking or metadata filter |

Các câu multi-hop thấp chủ yếu cần ghép nhiều policy section, nên context
recall thấp hơn factual (0.5958 so với 0.7083). Các câu 30, 33, 22 và 21
đều cần kết hợp nhiều điều kiện nên answer relevancy thấp. Câu 5 có điểm 0
và cần kiểm tra lại retrieval/reference trước khi kết luận là lỗi model.
Câu 50 là bẫy cho phép VPN cá nhân; điểm thấp không tự chứng minh pipeline đã
nhận diện đúng chính sách hạn chế.

## Matrix và nhóm yếu nhất

```text
                         factual  multi_hop  adversarial
faithfulness                  1          6           2
answer_relevancy              8          6           1
context_precision             4          4           1
context_recall                7          4           6
```

Nhóm yếu theo mean thấp nhất là `multi_hop` với mean `0.6770`.
Worst metric xuất hiện nhiều nhất là `context_recall` với 17 câu. Tổng các
cột vẫn là 20/20/10; đó là kích thước nhóm, không phải chất lượng.

Ưu tiên cải thiện hierarchical chunking và hybrid BM25 cho truy vấn ghép
policy; sau đó dùng reranker/metadata filter để giảm context nhiễu. Chạy lại
đúng cùng `answers_50q.json`, ghi source hashes mới và so sánh riêng
`multi_hop.context_recall` cùng bottom 10.

## Bẫy adversarial và giới hạn

Adversarial có mean `0.8221`, thấp hơn factual `0.8561` nhưng cao hơn
multi-hop. Câu 50 liên quan cho phép VPN cá nhân; cần kiểm tra nội dung context
để phân biệt lỗi phủ định với lỗi retrieval. Mẫu adversarial chỉ có 10 câu,
evaluator là một model DeepSeek và enrichment có fallback do endpoint không ổn
định, vì vậy không được khẳng định quan hệ nhân quả chỉ từ điểm trung bình.
