# Week 4 Baseline Report v1.0

學號：7114029021

姓名：陳羿婷

## 1. Task & Dataset

本週沿用 Week 2 與 Week 3 已確認的客服問題意圖分類任務。

- Task：將單一客服訊息分類為四種 intent。
- Unit：一則客服訊息。
- Input：`message` 欄位。
- Target：`intent` 欄位。
- Dataset version：`dataset_v1.0`，檔案為 `data/customer_intent_demo.csv`。
- Dataset size：100 rows。
- Labels：`account_login`、`order_delivery`、`product_info`、`refund_return`。

Label distribution：

| intent         |   count |
|:---------------|--------:|
| account_login  |      25 |
| order_delivery |      25 |
| product_info   |      25 |
| refund_return  |      25 |

## 2. Baseline Plan

本週建立 baseline ladder，先看簡單方法是否已足夠支援決策。

| Role | Method | Why reasonable | Expected weakness |
| --- | --- | --- | --- |
| Baseline 1 | Majority Class | 最便宜的 naive reference，只使用訓練資料 label 分布 | 完全不看訊息文字，容易漏掉非多數類別 |
| Baseline 2 | Rule-based Keyword | Week 1 已建立的 current / credible baseline，符合客服規則分流直覺 | 同一句話若含多類關鍵字，可能受規則順序影響 |
| Candidate | TF-IDF + Logistic Regression | 合理的 simple ML text classification candidate | 小型合成資料可能不足以學到穩定文字模式 |

本週不加入 LLM、RAG、Agent 或其他複雜方案，因為 Week 4 目標是先確認 baseline evidence。

## 3. Fair Comparison / Experiment Spec

- Dataset：所有方法使用 `data/customer_intent_demo.csv`。
- Split：沿用 Week 3 建議的 stratified random split。
- Split ratio：Train 70%、Validation 15%、Test 15%。
- Random seed：42。
- Test lock：Yes，同一份 test set 比較所有方法。
- Information boundary：所有方法只能使用 `message`；不能使用 `intent` 或任何事後欄位。
- Primary Metric：Macro F1，方向越高越好。
- Failure Metric：`refund_return` recall，方向越高越好。
- Threshold policy：N/A，本週方法輸出單一類別，不使用 probability threshold。
- Runtime / Cost：以本機 notebook 執行秒數記錄。

Split rows：

| split      |   rows |
|:-----------|-------:|
| train      |     70 |
| validation |     15 |
| test       |     15 |

## 4. Results

| method             | dataset_information                           |   accuracy |   macro_f1 |   refund_return_recall |   runtime_seconds | complexity   | note                                                       |
|:-------------------|:----------------------------------------------|-----------:|-----------:|-----------------------:|------------------:|:-------------|:-----------------------------------------------------------|
| Majority Class     | message only; stratified random split seed=42 |     0.2667 |     0.1053 |                 0      |            0.0029 | Low          | Naive baseline; predicts the most frequent training label. |
| Rule-based Keyword | message only; stratified random split seed=42 |     1      |     1      |                 1      |            0.0005 | Low          | Current credible baseline from Week 1; uses keyword rules. |
| TF-IDF Logistic    | message only; stratified random split seed=42 |     0.7333 |     0.6984 |                 0.3333 |            0.034  | Low-Mid      | Simple ML candidate; preprocessing is fit on train only.   |

Interpretation：

- Majority Class 表現很低，表示不能只靠 label 分布處理客服分流。
- Rule-based Keyword 在本次 locked test set 上 Macro F1 = 1.0000，`refund_return` recall = 1.0000。
- TF-IDF Logistic Regression 的 Macro F1 = 0.6984，`refund_return` recall = 0.3333，沒有超過 rule-based baseline。

## 5. Failure Analysis

Representative failure cases：

| method          |   case_id | message                   | ground_truth   | prediction     | failure_type          | possible_cause                                                                         | decision_impact                                                                |
|:----------------|----------:|:--------------------------|:---------------|:---------------|:----------------------|:---------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------|
| TF-IDF Logistic |        36 | 發票開錯想退費可以改嗎    | refund_return  | order_delivery | short-text ambiguity  | The small synthetic training set does not provide enough evidence for similar wording. | High risk because refund or return messages may miss the refund handling flow. |
| TF-IDF Logistic |        14 | 我想查訂單編號A1023的進度 | order_delivery | refund_return  | short-text ambiguity  | The small synthetic training set does not provide enough evidence for similar wording. | May route the customer to the wrong support flow.                              |
| TF-IDF Logistic |        28 | 請問七天鑑賞期怎麼算      | refund_return  | product_info   | short-text ambiguity  | The small synthetic training set does not provide enough evidence for similar wording. | High risk because refund or return messages may miss the refund handling flow. |
| Majority Class  |        74 | 會員生日資料可以修改嗎    | account_login  | order_delivery | single-class collapse | The method ignores text and sends every message to the same label.                     | May route the customer to the wrong support flow.                              |

Failure interpretation：

- Majority Class 的錯誤主要是 single-class collapse，因為它不讀文字。
- TF-IDF Logistic 的錯誤集中在短文字與語意相近的 case，尤其 `refund_return` 容易和 `order_delivery` 或 `product_info` 混淆。
- Rule-based Keyword 在這次 test set 沒有錯誤，但不代表真實部署沒有風險。Week 2 已觀察到 rule order 可能在含有「退貨」與「物流」的訊息上造成錯誤。

## 6. Minimum Sufficient Solution

Minimum Sufficient Solution：目前採用 Rule-based Keyword baseline。

Evidence：在相同 dataset、split、metric 與 information boundary 下，Rule-based Keyword 的 Macro F1 與 `refund_return` recall 都是 1.0000，且成本低、可解釋、容易人工檢查。

Cost / Risk：Rule-based 方法維護成本低，但需要人工更新關鍵字。若遇到真實客服中的錯字、口語、多意圖訊息或新商品情境，表現可能下降。

目前是否需要升級：No。

理由：TF-IDF Logistic Regression 沒有帶來增量 evidence，反而降低 high-risk `refund_return` recall。本週沒有足夠 evidence 支持增加模型複雜度。

## 7. Solution Choice Note

Current evidence：Rule-based Keyword 明顯優於 Majority Class，也優於 TF-IDF Logistic Regression。

Remaining failure：現有合成 test set 沒有暴露 rule-based 錯誤，但 Week 2 failure case 顯示多意圖或多關鍵字訊息仍可能出錯。

Minimum solution：Rule-based Keyword 暫時是 minimum sufficient solution。

Next candidate：目前不升級到更複雜模型。下一步應先擴充真實或更困難的客服資料，加入多意圖、口語、錯字、情緒與不同 channel，再重新測試 rule-based baseline。

Justification：如果資料仍是 100 筆乾淨合成訊息，複雜模型的額外成本與維護風險不值得。若未來 failure 集中在 rule 無法處理的語意變化，再測試 simple ML 或其他候選方案。

## 8. Reproducibility / Run Record

- Notebook：`notebooks/week04_baseline.ipynb`
- Data：`data/customer_intent_demo.csv`
- Output artifacts：`outputs/week04_results.csv`、`outputs/week04_failure_cases.csv`
- Random seed：42
- Python packages：pandas、scikit-learn、ipykernel
- Commit message suggestion：`Complete Week 4 baseline report`

## 9. Mini Defense

### Q1. 為什麼你的 Baseline 合理？

我的 task 是客服訊息四分類。Majority Class 是 naive reference，用來確認只看 label 分布會做到什麼程度。Rule-based Keyword 使用 `message` 中的客服關鍵字，在這個情境是合理起點，因為客服分流本來就常由明確詞彙觸發，例如退款、退貨、登入、配送、商品規格。

### Q2. 複雜模型多出的增益，集中在哪些案例？

本週 TF-IDF Logistic 沒有比 Rule-based Keyword 帶來增益。它在部分短文字與退款相關案例出錯，且 `refund_return` recall 只有 0.3333。因此目前沒有 evidence 顯示複雜度增加能降低重要 failure cost。

### Q3. 如果只提升 1–2%，你還會選它嗎？

目前不會。因為候選模型沒有提升 1–2%，而是低於 rule-based baseline。即使未來有小幅提升，也需要確認增益是否集中在高風險 failure，例如 refund / return recall，而不是只改善一般案例。若增益很小但增加維護與監控成本，就不值得升級。
