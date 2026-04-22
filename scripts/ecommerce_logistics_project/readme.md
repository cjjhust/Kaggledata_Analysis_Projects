# Logistic Predictor & Business Intelligence: Brazilian E-Commerce Analysis

## Projektübersicht | 项目概述
Dieses Projekt kombiniert Business Intelligence (PowerBI) mit Machine Learning (XGBoost), um die Lieferperformance und Kundenzufriedenheit auf dem brasilianischen Markt (Olist) zu analysieren und vorherzusagen. Es bietet eine datengestützte Entscheidungsgrundlage zur Reduzierung von Kundenabwanderung durch proaktive Interventionsstrategien.
该项目结合商业智能 (PowerBI) 与机器学习 (XGBoost)，针对巴西电商市场 (Olist) 的物流表现与客户满意度进行深度分析与建模。通过建立预警机制，实现在潜在差评发生前进行干预，有效降低客户流失率。

## Kernergebnisse der Business Intelligence | 商业智能核心发现
Anhand einer detaillierten Analyse der Logistikkette wurden folgende kritische Schwellenwerte und Muster identifiziert:
通过对物流链条的精细化分析，识别出以下关键临界点与模式：

* **Der 7-Tage-Psychologiewert:** Die Daten zeigen einen massiven Einbruch der Bewertungsscores, sobald die Lieferverzögerung 7 Tage überschreitet. Dies markiert den Wendepunkt der Kundentoleranz.
  **7天心理阈值：** 数据显示，一旦物流延误超过7天，客户评分会出现断崖式下跌。这标志着客户耐心的终点。
* **Logistische Black Holes:** Bestimmte Regionen (z.B. MA, AL, PI) und Städte (z.B. Maceió) weisen eine überproportional hohe Verzögerungsrate auf.
  **物流黑洞：** 特定地区（如 MA, AL, PI）及城市（如马塞约）表现出异常高的延误率。
* **Verkäufereffizienz:** Eine Verzögerung beim Versand durch den Verkäufer von mehr als 9 Tagen erhöht die Wahrscheinlichkeit einer verspäteten Gesamtzustellung um das 9,35-fache.
  **卖家效能：** 卖家发货环节若延迟超过9天，最终导致整体订单延误的可能性将激增9.35倍。

## Machine Learning Modellierung | 机器学习建模
Um die oben genannten Erkenntnisse in operative Maßnahmen zu übersetzen, wurde ein XGBoost-Klassifikationsmodell entwickelt.
为了将上述洞察转化为实际业务操作，本项目开发了基于 XGBoost 的分类模型。

### Feature Engineering | 特征工程
* **Optimierte Zeitmetriken:** Berechnung der tatsächlichen Lieferzeit, der Verzögerungstage und der spezifischen Verzögerung im Verkäuferprozess (`seller_ship_delay_days`).
  **优化时间指标：** 计算实际配送天数、逾期天数以及卖家环节的特定延迟天数。
* **Kategorische Kodierung:** Professionelle Verarbeitung von Produktkategorien und geografischen Daten mittels Label Encoding.
  **类别编码：** 对产品品类及地理位置数据进行专业的标签编码处理。
* **Datenbereinigung:** Ausschluss von statistisch unmöglichen Ausreißern (z.B. 100+ Tage Verzögerung bei 5-Sterne-Bewertung), um Modellverzerrungen zu vermeiden.
  **数据清洗：** 剔除统计学意义上不可能的异常值（如延误100天仍获好评），避免模型产生逻辑偏差。

### Modellleistung | 模型性能
* **Präzisionsfokus:** Durch Anpassung des Entscheidungsschwellenwerts auf **0,7** wurde die Präzision für die Vorhersage von negativem Feedback (1-2 Sterne) auf **0,58** gesteigert.
  **精准打击：** 通过将预测阈值调优至 **0.7**，将差评（1-2分）的预测精确率提升至 **0.58**。
* **Geschäftlicher Nutzen:** Das Modell fungiert als Frühwarnsystem. Anstatt blindlings alle Bestellungen zu bearbeiten, kann sich das Serviceteam auf die vom Modell identifizierten 60 % der tatsächlichen Problemfälle konzentrieren, was die Effizienz der Interventionsmaßnahmen verdoppelt.
  **业务价值：** 模型充当预警系统。售后团队无需盲目干预所有订单，而是专注于模型识别出的高危订单，使干预效率提升了一倍。

### Advanced Analytics: Delay Magnitude Prediction | 深度分析：延误时长预测
Neben der reinen Klassifizierung (Verschlechterung der Bewertung) wurde ein Regressionsmodell entwickelt, um die exakte Anzahl der Verzögerungstage vorherzusagen. 
除了分类模型外，本项目还开发了一个回归模型，用于预测具体的延误天数。

* **Metrik:** Das Modell erreichte einen MAE (Mean Absolute Error) von [X] Tagen.
  **指标：** 模型实现了 [X] 天的平均绝对误差。
* **Strategischer Nutzen:** Dies ermöglicht eine granulare Priorisierung des Kundensupports. Bestellungen mit einer prognostizierten Verzögerung von >7 Tagen werden automatisch für eine manuelle Eskalation priorisiert.
  **战略效益：** 这实现了售后服务的精细化分级。预测延误超过7天的订单将自动进入人工高级处理流程。

* **Strategische Analyse: Vorhersagegenauigkeit vs. Geschäftsnutzen | 战略分析：预测精度与业务价值的权衡**
    * **Beobachtung | 观察**: Die inhärente Komplexität der brasilianischen Logistik führt zu einem Basis-MAE (mittlerer absoluter Fehler) von ca. 6 Tagen. 
      巴西物流环境固有的复杂性导致基础 MAE（平均绝对误差）约为 6 天。
    * **Modellnutzen | 模型效用**: Anstatt eine präzise tagesgenaue Vorhersage zu treffen, wird das Modell zur **Priorisierung von Risiken (Ranking)** eingesetzt. 
      模型并非用于精确的天数预测，而是用于**风险优先级排序（排名）**。
    * **Ergebnis | 结果**: Das Modell identifiziert die **obersten 10 % der Hochrisiko-Sendungen**, die **16,13 % aller 1-Sterne-Bewertungen** abdecken. Dies entspricht einer **60 % höheren Effizienz** im Vergleich zu einer zufälligen Stichprobe (Lift = 1,61).
      模型成功识别出了**前 10% 的高风险发货单**，这些订单覆盖了全场 **16.13%** 的 1 星差评。相比随机抽样，识别效率提升了 **60%**（提升度 Lift = 1.61）。

## Technischer Stack | 技术栈
* **Datenanalyse:** SQL (PostgreSQL), PowerBI
* **Sprachen & Bibliotheken:** Python (Pandas, NumPy, Scikit-Learn, XGBoost)
* **Infrastruktur:** SQLAlchemy (Datenbankanbindung), GitHub (Versionierung)
---
**Analysiert von / 分析师:** Jinjing Cheng