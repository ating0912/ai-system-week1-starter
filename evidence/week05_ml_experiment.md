# Week 5 ML Experiment v1

學號：7114029021

姓名：陳羿婷

## 1. Task / Y

Decision：將一則客服訊息分流到正確處理流程，讓訂單配送、退款退貨、帳號登入與商品資訊問題能進入對應客服流程。

X：`message`，也就是預測當下可取得的客服訊息文字。

Y：`intent`，四個類別為 `account_login`、`order_delivery`、`product_info`、`refund_return`。

Y 的來源：`data/customer_intent_demo.csv` 中已標註的合成客服意圖標籤。這是課程 demo dataset，不是線上客服系統真實標註資料。

## 2. Dataset / Split

Dataset：`data/customer_intent_demo.csv`。

版本：`dataset_v1.0_customer_intent_demo`。

筆數：100 rows。

Label distribution：

| intent         |   count |
|:---------------|--------:|
| account_login  |      25 |
| order_delivery |      25 |
| product_info   |      25 |
| refund_return  |      25 |

Split：stratified random split，seed = 42。

| split      |   rows |
|:-----------|-------:|
| train      |     70 |
| validation |     15 |
| test       |     15 |

Split 理由：目前資料是互相獨立的合成客服訊息，沒有同一客戶、同一案件或同一設備的 group key，也不是時間序列資料，因此使用 stratified random split 維持四個 intent 的比例。Test set 只用於最後比較，不用來選模型或調整規則。

Dataset risk：資料乾淨且規模小，coverage 不足以代表真實客服中的錯字、口語、多意圖、情緒、長對話或新商品情境。

## 3. Baseline / Comparison

W4 credible baseline：Rule-based Keyword。

本週比較三種方法：

- Majority Class：naive baseline，只使用 train label distribution。
- Rule-based Keyword：W4 credible baseline，使用 `src/rule_baseline.py` 關鍵字規則。
- TF-IDF Logistic Regression：Week5 simple ML candidate，TF-IDF 只在 train split fit。

Comparison results：

| method                     | split   |   accuracy |   macro_f1 |   refund_return_recall | threshold   |   runtime_seconds | note                                                 |
|:---------------------------|:--------|-----------:|-----------:|-----------------------:|:------------|------------------:|:-----------------------------------------------------|
| Majority Class             | test    |     0.2667 |     0.1053 |                 0      | N/A         |            0.0064 | Naive reference using train label distribution only. |
| Rule-based Keyword         | test    |     1      |     1      |                 1      | N/A         |            0.0003 | Week 4 credible baseline from src/rule_baseline.py.  |
| TF-IDF Logistic Regression | test    |     0.7333 |     0.6984 |                 0.3333 | N/A         |            0.0793 | Simple ML candidate; TF-IDF fit on train only.       |

Difference：TF-IDF Logistic Regression 相較 Rule-based Keyword 的 Macro F1 變化為 -0.3016。本次沒有改善，主要退步出現在 `refund_return` recall。

是否改善：No。Rule-based Keyword 仍是目前 minimum sufficient solution。

額外成本：TF-IDF Logistic Regression 需要訓練、保存 preprocessing pipeline，且在小型合成資料上沒有帶來較好 failure metric。

## 4. Metric / Threshold

Primary Metric：Macro F1。

理由：四個 intent 都重要，Macro F1 能避免只看整體 accuracy 而忽略少數或高風險類別。

Failure Metric：`refund_return` recall。

理由：退款退貨若被漏判，可能導致客戶進入錯誤流程，處理成本和客訴風險較高。

False Positive 後果：非退款案件被送入退款流程，會增加人工確認與流程成本。

False Negative 後果：退款退貨案件沒有進入退款流程，可能延誤處理並提高客訴風險。

Threshold：N/A。本週三個方法都輸出單一類別，不使用 probability threshold。若未來改成機率式模型，才需要另外設定 refund-return review threshold。

## 5. Top-3 Failure

|   case_id | message                   | intent         | prediction    | method                     | failure_type              | possible_cause                                                     | next_step                                                           |
|----------:|:--------------------------|:---------------|:--------------|:---------------------------|:--------------------------|:-------------------------------------------------------------------|:--------------------------------------------------------------------|
|        14 | 我想查訂單編號A1023的進度 | order_delivery | refund_return | TF-IDF Logistic Regression | refund/semantic ambiguity | Short synthetic text gives weak evidence for this intent boundary. | Add harder refund/order examples and review feature representation. |
|        18 | 海外訂單大概多久到貨      | order_delivery | refund_return | TF-IDF Logistic Regression | refund/semantic ambiguity | Short synthetic text gives weak evidence for this intent boundary. | Add harder refund/order examples and review feature representation. |
|        28 | 請問七天鑑賞期怎麼算      | refund_return  | product_info  | TF-IDF Logistic Regression | refund/semantic ambiguity | Short synthetic text gives weak evidence for this intent boundary. | Add harder refund/order examples and review feature representation. |

Failure taxonomy：

- Semantic ambiguity：短文字同時接近退款、訂單或商品資訊語意。
- Representation limitation：TF-IDF 在 100 筆合成資料上沒有足夠 evidence 學到穩定文字邊界。
- Naive collapse：Majority Class 不讀訊息，只能作最低比較基準。

下一輪優先處理：先擴充更困難的客服資料，尤其退款/訂單/商品資訊邊界模糊、多意圖、口語與錯字案例；再重新比較 Rule-based 與 simple ML。

## 6. 本次結論與下一步

在相同 Dataset / Split / Metric 下，TF-IDF Logistic Regression 沒有超過 Rule-based Keyword。Rule-based Keyword 的 Macro F1 = 1.0000，`refund_return` recall = 1.0000；TF-IDF Logistic Regression 的 Macro F1 = 0.6984，`refund_return` recall = 0.3333。

本週結論：不升級到較複雜模型。下一步應先增加真實或更困難的客服資料，再確認複雜模型的增益是否集中在 high-risk failure cases。

## 7. Reproducibility

- Notebook：`notebooks/week05_ml_experiment.ipynb`
- Data：`data/customer_intent_demo.csv`
- Outputs：`outputs/week05_results.csv`、`outputs/week05_predictions.csv`、`outputs/week05_top3_failures.csv`
- Split：stratified random split
- Seed：42
- Packages：pandas、scikit-learn、ipykernel
