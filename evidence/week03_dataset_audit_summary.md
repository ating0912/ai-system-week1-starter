# Week 3 Dataset Audit Summary

學號：7114029021

姓名：陳羿婷

## Dataset

```text
data/customer_intent_demo.csv
```

## Audit Results

| Check | Result |
| --- | --- |
| Rows | 100 |
| Columns | `message`, `intent` |
| Missing values in `message` | 0 |
| Missing values in `intent` | 0 |
| Exact duplicate rows | 0 |
| Duplicate messages | 0 |
| Label classes | 4 |
| Label distribution | each class has 25 rows |
| Mean message length | 10.25 characters |
| Min message length | 6 characters |
| Max message length | 16 characters |

## Label Distribution

| Label | Count |
| --- | ---: |
| `account_login` | 25 |
| `order_delivery` | 25 |
| `product_info` | 25 |
| `refund_return` | 25 |

## One Data Quality Issue

資料太乾淨且完全平衡。這對教學很方便，但真實客服資料通常會有類別不平衡、錯字、多輪對話、重複模板與高風險少數類別。因此目前 audit 沒有發現 missing 或 exact duplicate，不代表資料已足以支持真實部署。

## One Leakage / Split Risk

目前資料沒有 `user_id`、`ticket_id` 或 `timestamp`，因此無法檢查同一使用者、同一案件或未來資料是否跨 train / test。若直接使用 random split，只能模擬同分布合成訊息，不能保證對未來真實客服資料有效。

## One Label Quality Risk

資料只有單一 `intent` label，沒有 uncertain 或 multi-label 標記。若一句話同時包含「訂單」「取消」「退款」等訊息，目前 codebook 沒有明確優先規則，可能導致標籤不一致。

## Week 3 Conclusion

這份資料可以支持 Week 1-3 的課堂練習，但不能直接支持真實客服系統部署。若要進一步做真實 AI system，下一版 Dataset Spec 應加入資料來源、時間、使用者或 ticket group、label codebook 與真實 split strategy。
