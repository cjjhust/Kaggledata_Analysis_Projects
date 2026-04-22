# 📦 Predictive Logistics Risk Modeling | 供应链交付风险预测模型

## 📖 Projektübersicht | 项目概述
Dieses Projekt implementiert ein Machine-Learning-Modell auf Basis von **XGBoost**, um das Risiko von Lieferverzögerungen in einer globalen Lieferkette vorherzusagen. Das Modell nutzt Transaktionsdaten, um die Wahrscheinlichkeit von Verspätungen (Late Delivery) zu berechnen und die wichtigsten Risikofaktoren zu identifizieren.

本项目实现了一个基于 **XGBoost** 的机器学习模型，用于预测全球供应链中的交付延误风险。模型利用交易数据计算延误（Late Delivery）概率，并识别出导致风险的核心变量。

---

## 📊 Datenquelle | 数据源
Die für dieses Projekt verwendeten Daten stammen aus dem **DataCo Smart Supply Chain Dataset**:
本项目所使用的数据来源于 **DataCo 智能供应链数据集**:
👉 [Kaggle Dataset Link](https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis)

---

## 🛠️ Methodik | 技术实现

### 1. Feature Engineering | 特征工程
* **One-Hot-Encoding**: Transformation von kategorialen Variablen (`Type`, `Shipping Mode`, `Market`).
    * **独热编码**: 将分类变量（支付类型、物流模式、市场）转换为二进制矩阵。
* **Zeitliche Merkmale**: Extraktion der Bestellstunde (`order_hour`) aus den Zeitstempeln.
    * **时间特征**: 从订单时间戳中提取“下单小时”变量。
* **Basis-Benchmark**: Nutzung der geplanten Versandtage (`Days for shipment (scheduled)`) als Referenzwert.
    * **基准标尺**: 利用“计划发货天数”作为模型的核心参考指标。

### 2. Modellierung | 模型构建
* **Algorithmus**: XGBoost Classifier (Gradient Boosting).
* **Validierung**: "Three-Split-Method" (60/20/20) zur Vermeidung von Overfitting.
* **训练验证**: 采用“三折法”并结合 `early_stopping_rounds` 机制防止过拟合。

---

## 📈 Ergebnisse | 评估报告

Das Modell erreichte auf dem unabhängigen Testdatensatz folgende Werte:
模型在独立测试集上的表现如下：

- **Accuracy**: `0.7187` (72% 准确率)
- **ROC-AUC**: `0.7783` (78% 区分度)
- **LogLoss**: `0.5252`

---

## 🔍 Wichtige Erkenntnisse | 核心洞察

Die Analyse der Feature Importance ergab eine Diskrepanz zur rein deskriptiven Statistik:
特征重要性分析揭示了与纯描述性统计之间有趣的差异：

1. **Dominanz der Planung**: `Days for shipment (scheduled)` ist der stärkste Prädiktor.
   - **计划的主导地位**: “计划发货天数”是预测力最强的变量。
2. **Präzision vs. Volumen (TRANSFER vs. DEBIT)**:
   - **Deskriptiv**: `DEBIT`-Aufträge verursachen das höchste **Volumen** an Verspätungen.
   - **Prädiktiv**: Das Modell identifiziert `TRANSFER` als den **stärksten Signalgeber**.
   - **精确度 vs. 规模**: 统计显示 `DEBIT` 支付产生的延误订单**总量**最多；但模型识别出 `TRANSFER`（转账）是**最强信号源**，具有更高的预测确定性。

---


## 🚀 Nutzung | 使用
1. Modell trainieren: `python3 :/app/scripts/supplychain_risk_project/predict_xgboost.py`
2. Das Modell wird als `xgboost_delivery_model.pkl` gespeichert.

**Analysiert von / 分析师:** Jinjing Cheng