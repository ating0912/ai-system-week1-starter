# Week 3 Dataset Spec v0.2

學號：7114029021

姓名：陳羿婷

## 1. Source / Owner

本資料集來源為課程 Week 1 Starter Repo 中的合成客服訊息資料：

```text
data/customer_intent_demo.csv
```

資料用途是教學示範與 baseline 練習，不是真實公司客服資料。資料 owner 可視為課程 repo 維護者。因為資料為 synthetic / curated data，本資料集可以用來練習 Dataset Spec、Baseline 與 Failure Case 分析，但不能直接主張它代表真實客服場域。

## 2. Unit of Analysis

一筆資料是一則客服訊息。

每筆資料對應一個使用者輸入文字與一個意圖標籤：

- `message`：客服訊息文字。
- `intent`：正確意圖類別。

此 unit 與 Week 2 AI Problem Spec 一致，因為 AI 任務是對單一客服訊息做意圖分類。

## 3. Time Range

目前資料集沒有真實時間欄位，也沒有資料抽取日期、工單建立時間或訊息發生時間。

因此，本資料集不能支援 time split，也不能用來模擬「未來客服訊息」的泛化表現。若未來改用真實客服資料，應加入 `timestamp` 或 ticket 建立時間，並考慮以時間切分 train / validation / test。

## 4. Fields

| Field | Type | Meaning | Available at Decision Time | Use as Input |
| --- | --- | --- | --- | --- |
| `message` | text | 客服訊息文字 | Yes | Yes |
| `intent` | category | 意圖標籤 | No, this is the target | No |

目前資料欄位很少，因此 leakage 風險主要不是來自多餘欄位，而是來自 label 設計、split 設計與 synthetic data coverage。

## 5. Label / Codebook

Target label 為 `intent`，共有四類：

| Label | Meaning |
| --- | --- |
| `order_delivery` | 訂單／配送 |
| `refund_return` | 退款／退貨 |
| `account_login` | 帳號／登入 |
| `product_info` | 商品資訊 |

目前 label 來自合成資料設計，不是多位標註者依 codebook 標註後產生。因此 label quality 的限制包括：

- 沒有標註者一致性紀錄。
- 沒有 uncertain / disagreement 標記。
- 一句話若同時包含多個意圖，目前只能放入單一 label。
- 類別優先順序尚未正式定義，例如「訂錯東西，現在可以取消或退款嗎？」可能同時接近 order change、cancellation 與 refund。

## 6. Inclusion / Exclusion

目前納入規則：

- 納入繁體中文客服短訊息。
- 每筆資料需有 `message` 與 `intent`。
- 類別限定為四個意圖類別。

目前排除或未涵蓋：

- 無文字訊息。
- 多輪對話。
- 含圖片、附件、語音或電話轉錄的客服內容。
- 真實 user_id、ticket_id、timestamp、channel、agent_id、resolution 等營運欄位。
- 無法判斷或多重意圖案例。

## 7. Population / Coverage

Target population 是未來可能進入客服系統的中文客服訊息。

Observed population 則是目前課程設計的 100 筆合成客服訊息。兩者不同，因此 coverage limitation 很重要。

目前資料的 coverage：

- 類別平衡，四類各 25 筆。
- 訊息長度短，平均約 10.25 個字。
- 主要涵蓋常見、清楚、單句的客服問題。

主要 coverage limitation：

- 不包含真實客服中的錯字、口語、省略句與情緒性文字。
- 不包含多輪上下文。
- 不包含電話、門市、Email、App、Web 等不同 channel。
- 不包含同一使用者多次詢問或同一案件轉單紀錄。
- 不包含罕見但高風險案例，例如詐騙、法規、個資或金流爭議。

## 8. Train / Validation / Test Rule

目前資料沒有 timestamp 或 user_id，因此不適合做 time split 或 group split。若只是課堂示範，可使用 stratified random split，確保四個 label 在 train / validation / test 中都有樣本。

建議示範切分：

```text
Train：70%
Validation：15%
Test：15%
Stratify by：intent
Random seed：42
```

但此 split 只能回答「在同一批合成資料分布下，新訊息是否能被分類」；它不能回答以下問題：

- 對未來月份真實客服訊息是否有效。
- 對新使用者是否有效。
- 對新 channel 是否有效。
- 對多輪對話或高風險案例是否有效。

若未來資料加入 `timestamp`，應優先考慮 time split。若資料加入 `user_id` 或 `ticket_id`，應檢查 group overlap，避免同一使用者或同一案件跨 train / test。

## 9. Leakage Risks

目前資料集只有 `message` 與 `intent`，沒有 resolution、final status 或人工處理結果，因此 future leakage 風險較低。

仍需注意以下 leakage / split risks：

- `intent` 是 target，不能放入 input。
- 若未來加入 `resolution`、`agent_note`、`refund_completed_at`、`final_case_code`，這些多半是事後欄位，不能直接當作部署時 input。
- 若未來同一 user 或同一 ticket 有多筆紀錄，不能讓同一 group 跨 train / test。
- 若有 FAQ 模板或近重複訊息，random split 可能讓 train 和 test 出現高度相似文字，使 test score 偏高。
- 若做文字正規化、詞彙表或統計特徵，必須只用 train fit，再套用到 validation / test，避免 preprocessing leakage。

## 10. Quality Issues

依據目前 `data/customer_intent_demo.csv` 的 audit：

| Check | Result |
| --- | --- |
| Row count | 100 |
| Columns | `message`, `intent` |
| Missing values | 0 |
| Exact duplicate rows | 0 |
| Duplicate messages | 0 |
| Label distribution | 四類各 25 筆 |
| Average message length | 約 10.25 字 |

目前資料結構乾淨，但品質限制仍存在：

- synthetic data 可能比真實資料乾淨。
- label 完全平衡，可能不像真實客服分布。
- 沒有 uncertain label 或 multi-label case。
- 缺少時間、群組與來源欄位，無法檢查 time leakage、group leakage 或 channel coverage。

## 11. Version / Provenance

目前資料版本：

```text
dataset_v1.0
file：data/customer_intent_demo.csv
rows：100
labels：4 classes
purpose：Week 1-3 course demo
```

目前已知 provenance：

- 由課程 starter repo 提供。
- 資料為合成客服訊息。
- 與 Week 1 rule-based baseline、Week 2 AI Problem Spec 使用同一份資料。

若未來資料更新，需要記錄：

- 資料來源。
- 抽取日期。
- 清理規則。
- label codebook 版本。
- split seed 或 split rule。
- 已知限制。

## 12. Known Limitations

本資料集目前最重要的限制是：它是平衡且乾淨的合成資料，不能代表真實客服場景。

因此，Week 1 的 Accuracy = 0.950 只能視為課堂 baseline 證據，不能直接外推成真實部署表現。若要往真實 AI system 推進，下一步需要取得更接近部署場景的資料，至少包含時間、來源、群組或 ticket 資訊，並重新設計 split 與 leakage 檢查。

## 13. Dataset Audit Evidence

本週 audit notebook 位於：

```text
notebooks/week03_dataset_audit.ipynb
```

文字摘要位於：

```text
evidence/week03_dataset_audit_summary.md
```

## 14. Mini Defense

### Q1. Test set 到底模擬哪一種未知？

目前若使用 stratified random split，test set 只模擬「同一合成資料分布下的新訊息」。它不模擬未來月份、新使用者、新 channel 或真實客服資料。

### Q2. 哪個欄位最可能造成 leakage？

目前資料中最明顯不能作為 input 的欄位是 `intent`，因為它就是 target。若未來加入 `resolution` 或 `final_case_code`，這些事後欄位會是更高風險的 leakage 欄位。

### Q3. Dataset 最重要的 coverage limitation 是什麼？

最重要限制是資料為 synthetic / curated data，缺少真實客服中的錯字、多輪對話、情緒文字、channel 差異、使用者群組與高風險罕見案例。
