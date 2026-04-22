# 🚀 数据分析作品集：Power BI 与 高级建模

欢迎来到我的数据分析仓库。本项目集合了四个深入的商业分析案例，涵盖了德国交通效率、全球供应链风险及电商物流洞察。

---

## 🛠 技术架构 (工程化亮点)
*为了模拟真实的企业级数据环境，我搭建了一个混合跨平台架构：*
- **后端服务器 (Mac Mini):** - 使用 **Docker** 部署 **PostgreSQL** 数据库容器。
    - 配置 **Python** 建模环境 (Pandas, Scikit-learn)。
- **前端与工作流 (Windows 客户端):** - 通过 **SSH** 隧道将 **Power BI Desktop** 连接至远程 PostgreSQL 数据库。
    - 在客户端进行复杂的 DAX 建模与交互式可视化开发。
- **核心技术栈:** 跨平台系统集成、容器化 (Docker)、SQL、DAX、Python 机器学习建模。

---

## 📂 项目概览

### 1. DB 德国铁路：区域准点率与路网复杂度研究
**核心维度:** 对比北威州 (NRW) 与巴符州 (BW) 的铁路表现。
- **深度洞察:** - 反驳了“车站越多越延误”的直觉，识别出 **巴符州 (BW) 的结构性瓶颈** 在于路网高耦合。
    - 证明了 **北威州 (NRW)** 通过结构冗余成功吸收了路网复杂度带来的风险。
- **商业价值:** 建议在高密度节点引入动态缓冲规划，以缓解系统性延误的级联效应。
- **相关资源:**  [db_network.pdf](./scripts/db_network_project/db_network.pdf) | [db_network_predict.py](./scripts/db_network_project/db_network_predict.py) | [db_network.pbix](./scripts/db_network_project/db_network.pbix) | [readme.md](./scripts/db_network_project/readme.md)

### 2. 智慧供应链：交付风险与“成本陷阱”识别
**核心维度:** 识别物流延误根因与财务利润保护。
- **深度洞察:** - 定义并量化了 **“成本陷阱” (Cost Trap)**：识别出那些利润为负、却在使用昂贵的特快物流处理的异常订单。
    - 隔离出行政端延误（如支付审核）是抵消物流投资收益的核心痛点。
- **商业价值:** 通过重新分配物流资源，保护企业核心利润率。
- **相关资源:** [supplychainrisk.pdf](./scripts/supplychain_risk_project/supplychainrisk.pdf) | [predict_xgboost.py](./scripts/supplychain_risk_project/predict_xgboost.py) | [supplychainrisk.pbix](./scripts/supplychain_risk_project/supplychainrisk.pbix) | [readme.md](./scripts/supplychain_risk_project/readme.md)

### 3. 电商物流：客户情绪与数据欺诈检测
**核心维度:** 交付速度与客户评价真实性的相关性分析。
- **深度洞察:** - **异常检测:** 通过统计学手段识别出疑似“刷单/虚假评论”数据（如延误 100 天却获得满分好评）。
    - **7天黄金窗口期:** 识别出客户满意度在延误 7 天后呈指数级下降，之后的补救努力在统计学上几乎无效。
- **商业价值:** 建立早期预警系统，重点监控接近 7 天临界点的订单。
- **相关资源:** [ecommerce_logistics.pdf](./scripts/ecommerce_logistics_project/ecommerce_logistics.pdf) | [delivery_time_regression.py](./scripts/ecommerce_logistics_project/delivery_time_regression.py) | [review_score_prediction.py](./scripts/ecommerce_logistics_project/review_score_prediction.py)| [ecommerce_logistics.pbix](./logistik/scripts/ecommerce_logistics_project/ecommerce_logistics.pbix) | [readme.md](./scripts/ecommerce_logistics_project/readme.md)

### 4. 2024 柏林 S-Bahn 运行表现分析
**核心维度:** 公共交通延误的韧性分析与归因。
- **深度洞察:** - 识别出 **罢工 (平均延误 41.26 分钟)** 是系统瘫痪的首要原因，影响远超技术故障。
    - 发现系统对天气的响应呈**非线性特征**：在降雨量小于 10mm/天时表现极强韧性，仅在极端天气（Stormy）下延误才发生质变。
- **商业价值:** 为交通部门提供大规模突发事件下的主动危机管理策略建议。
- **相关资源:** [Berlin_SBahn_Project.pdf](./scripts/berlin_sbahn_project/Berlin_SBahn_Project.pdf) | [Python Script](./scripts/berlin_sbahn_project/metadata_streamlit.py) | [Berlin_SBahn_Project.pbix](./scripts/berlin_sbahn_project/Berlin_SBahn_Project.pbix) | [readme.md](./scripts/berlin_sbahn_project/readme.md)
---

## 📈 核心职业竞争力 

1. **端到端 Pipeline 落地:** 具备从数据库搭建 (PostgreSQL) 到数据处理 (Python/SQL) 再到最终决策支持 (Power BI) 的全流程能力。
2. **商业结果导向:** 关注 ROI、利润率保护和运营效率，而非单纯的可视化呈现。
3. **合规意识:** 所有项目均使用匿名公开数据集，严格遵守德国及欧盟的 **GDPR/DSGVO** 数据隐私规范。

---

## 📫 联系方式
*寻求杜塞尔多夫或远程数据分析岗位*
- **姓名:** Jinjing Cheng
- **坐标:** 德国，杜塞尔多夫
- **Email:** cjjhust@gmail.com