# 🚀 Data Analytics Portfolio: Power BI & Advanced Modeling

Welcome to my data analytics portfolio. This repository showcases four comprehensive data projects, ranging from European transportation efficiency to global supply chain risk management. 
> 🇨🇳 [中文版说明 (Chinese Version)](./README_CN.md)
---

## 🛠 Technical Architecture (Engineering Excellence)
*To simulate a professional enterprise data environment, I developed a hybrid cross-platform architecture:*
- **Backend (Mac Mini Server):** - Deployed **Docker** containers for **PostgreSQL** database.
    - Integrated **Python** modeling environment (Pandas, Scikit-learn).
- **Frontend & Workflow (Windows Client):** - Connected **Power BI Desktop** to the remote PostgreSQL instance via **SSH** and local network.
    - Developed advanced DAX measures and interactive dashboards on the client side.
- **Key Skills:** Hybrid System Integration, Containerization (Docker), SQL, DAX, Python Modeling.

---

## 📂 Project Highlights | 项目概览

### 1. DB Network: Regional Punctuality & Complexity
**Focus:** Comparative analysis of railway performance between NRW and Baden-Württemberg (BW).
- **Core Insights:** - Debunked the myth that "more stations = more delays." 
    - Identified a **structural bottleneck in BW** due to network complexity, while **NRW** absorbs complexity through better structural redundancy.
- **Business Value:** Proposing dynamic buffer planning for high-density railway nodes.
- **Resources:** [db_network.pdf](./scripts/db_network_project/db_network.pdf) | [db_network_predict.py](./scripts/db_network_project/db_network_predict.py) | [db_network.pbix](./scripts/db_network_project/db_network.pbix) | [readme.md](./scripts/db_network_project/readme.md)

### 2. Smart Supply Chain: Delivery Risk & Cost Trap
**Focus:** Root cause analysis of logistics delays and financial margin protection.
- **Core Insights:** - Defined the **"Cost Trap"**: identified orders with negative margins being shipped via expensive premium logistics.
    - Isolated administrative delays (payment processing) as a major bottleneck that nullifies logistical investments.
- **Business Value:** Strategic reallocation of logistics resources to protect profit margins.
- **Resources:** [supplychainrisk.pdf](./scripts/supplychain_risk_project/supplychainrisk.pdf) | [predict_xgboost.py](./scripts/supplychain_risk_project/predict_xgboost.py) | [supplychainrisk.pbix](./scripts/supplychain_risk_project/supplychainrisk.pbix) | [readme.md](./scripts/supplychain_risk_project/readme.md)


### 3. E-commerce Logistics: Sentiment & Fraud Detection
**Focus:** Correlation between delivery speed and customer review integrity.
- **Core Insights:** - **Fraud Detection:** Spotted statistical anomalies suggesting "Review Manipulation" (high ratings for 100+ days delayed orders).
    - **7-Day Window:** Identified that customer satisfaction drops exponentially after 7 days, making late recovery efforts cost-ineffective.
- **Business Value:** Implementing early-warning systems for orders approaching the 7-day critical limit.
- **Resources:** [ecommerce_logistics.pdf](./scripts/ecommerce_logistics_project/ecommerce_logistics.pdf) | [delivery_time_regression.py](./scripts/ecommerce_logistics_project/delivery_time_regression.py) | [review_score_prediction.py](./scripts/ecommerce_logistics_project/review_score_prediction.py)| [ecommerce_logistics.pbix](./logistik/scripts/ecommerce_logistics_project/ecommerce_logistics.pbix) | [readme.md](./scripts/ecommerce_logistics_project/readme.md)

### 4. Berlin S-Bahn Performance Analysis 2024
**Focus:** Operational resilience and root cause attribution of public transport delays.
- **Core Insights:** - Identified that **strikes (41.26 min avg. delay)** have a significantly higher impact than technical incidents.
    - Discovered a **non-linear response** to weather; the system remains resilient until precipitation exceeds 10mm/day (Stormy).
- **Business Value:** Recommendations for proactive crisis management during large-scale strikes.
- **Resources:** [Berlin_SBahn_Project.pdf](./scripts/berlin_sbahn_project/Berlin_SBahn_Project.pdf) | [Python Script](./scripts/berlin_sbahn_project/metadata_streamlit.py) | [Berlin_SBahn_Project.pbix](./scripts/berlin_sbahn_project/Berlin_SBahn_Project.pbix) | [readme.md](./scripts/berlin_sbahn_project/readme.md)
---

## 📈 Key Professional Competencies | 核心能力 

1. **End-to-End Pipeline:** Experience in setting up databases (PostgreSQL), processing data (Python/SQL), and delivering insights (Power BI).
2. **Business-Centric Analysis:** Focus on ROI, margin protection, and operational efficiency rather than just "pretty charts."
3. **GDPR/DSGVO Awareness:** All projects use anonymized public datasets, following strict data privacy principles applicable in Germany.

---

## 📫 Contact
*Seeking a Data Analyst role in Düsseldorf or Remote.*
- **Name:** Jinjing Cheng
- **Location:** Düsseldorf, Germany
- **Email:** cjjhust@gmail.com