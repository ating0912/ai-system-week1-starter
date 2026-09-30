# Week 4 Solution Choice Note

## Current Evidence

在相同 Dataset、Split、Metric 與 Information Boundary 下，Rule-based Keyword 是目前最好的方案。

| method             | dataset_information                           |   accuracy |   macro_f1 |   refund_return_recall |   runtime_seconds | complexity   | note                                                       |
|:-------------------|:----------------------------------------------|-----------:|-----------:|-----------------------:|------------------:|:-------------|:-----------------------------------------------------------|
| Majority Class     | message only; stratified random split seed=42 |     0.2667 |     0.1053 |                 0      |            0.0029 | Low          | Naive baseline; predicts the most frequent training label. |
| Rule-based Keyword | message only; stratified random split seed=42 |     1      |     1      |                 1      |            0.0005 | Low          | Current credible baseline from Week 1; uses keyword rules. |
| TF-IDF Logistic    | message only; stratified random split seed=42 |     0.7333 |     0.6984 |                 0.3333 |            0.034  | Low-Mid      | Simple ML candidate; preprocessing is fit on train only.   |

## Remaining Failure

本次 test set 中 Rule-based Keyword 沒有錯誤，但 Week 2 已指出多意圖或多關鍵字訊息仍是風險。例如退貨訊息同時包含物流詞時，規則順序可能造成誤判。

## Minimum Sufficient Solution

目前選擇 Rule-based Keyword 作為 minimum sufficient solution。

理由：它在本次 locked test set 上達到 Macro F1 = 1.0000，`refund_return` recall = 1.0000，而且成本低、可解釋、容易人工檢查。

## Next Candidate

目前不建議升級到更複雜模型。下一步應先增加更接近真實客服的資料，包含錯字、口語、多意圖、情緒文字與不同 channel。若新資料顯示 rule-based baseline 明顯失敗，再測試 simple ML 或其他 candidate。

## Complexity Justification

TF-IDF Logistic Regression 的 Macro F1 = 0.6984，`refund_return` recall = 0.3333，沒有提供足夠增量 evidence。增加模型複雜度目前不值得。
