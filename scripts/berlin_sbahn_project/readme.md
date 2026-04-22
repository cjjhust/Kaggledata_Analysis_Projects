# Berlin S-Bahn Performance Analysis 2024
# 2024年柏林城市快铁（S-Bahn）运行表现分析

## Projektübersicht | 项目概述

**DE:** Dieses Projekt analysiert die Pünktlichkeit und operative Resilienz der Berliner S-Bahn im Jahr 2024. Ziel ist es, die Hauptursachen für Verspätungen zu identifizieren, den Einfluss von Wetterbedingungen zu untersuchen und die Stabilität verschiedener Linien (z. B. Ringbahn vs. Radiallinien) zu vergleichen.
**CN:** 本项目分析了2024年柏林城市快铁（S-Bahn）的准点率与运营韧性。旨在识别导致延误的主要原因，研究天气因素的影响，并对比不同线路（如环线与射线线路）的稳定性。

---

## Technische Architektur & Engineering | 技术架构与工程实现

Das Projekt implementiert eine robuste, containerisierte Pipeline, die auf industrielle Standards setzt:
- **Containerisierung & Isolation:** Vollständige Trennung von Entwicklungsumgebung (Python-Container) und Datenbank (PostgreSQL-Container) mittels **Docker**. Dies garantiert Umgebungskonsistenz und einfache Portabilität.
- **Effizientes ETL-Design:** Der Ingest-Prozess ist für große Datenmengen optimiert. Durch die Verwendung von **Chunk-Processing (`chunksize=50000`)** wird eine speichereffiziente Verarbeitung ermöglicht, die Memory-Overflow-Fehler verhindert und die Skalierbarkeit des Systems sicherstellt.
- **Remote Development:** Windows-Host-Entwicklung über **SSH-Tunnel** direkt in die Container-Laufzeitumgebung.
- **BI-Integration:** Direkte Kopplung von **Power BI** an die PostgreSQL-Instanz für Echtzeit-Visualisierungen.

本项目实现了一套符合工业标准的鲁棒性容器化流水线：
- **容器化与隔离：** 通过 **Docker** 实现了开发环境（Python 容器）与数据库（PostgreSQL 容器）的完全分离。这确保了环境的一致性与高度的可移植性。
- **高效 ETL 设计：** 针对大数据量优化了导入流程。通过 **分块处理技术 (`chunksize=50000`)**，实现了内存高效型计算，有效防止内存溢出（OOM），保证了系统的可扩展性。
- **远程开发：** Windows 主机通过 **SSH 隧道** 直接连接至容器运行环境进行开发。
- **BI 集成：** **Power BI** 直接挂载 PostgreSQL 实例，实现数据的实时可视化呈现。

---
## Analytische Highlights & Statistische Validierung | 分析亮点与统计验证

Über die reine Visualisierung hinaus konzentriert sich die Analyse auf die Identifikation von Artefakten und Kausalitäten:
- **Bereinigung statistischer Rauschen:** Identifikation von "Schein-Verspätungen". [cite_start]Analyse ergab, dass extreme Peaks in den Nachtstunden auf extrem geringe Stichprobengrößen ($n < 3$) zurückzuführen sind und somit **statistische Artefakte** darstellen, keine operativen Fehler[cite: 88, 89].
- **Kausalitätsanalyse:** Untersuchung der Korrelation zwischen Niederschlag und Verspätung. [cite_start]Die S-Bahn zeigt hohe Resilienz bis 10mm Regen; erst bei Extremwetter (Stormy) kippt die Systemstabilität[cite: 83, 84].
- [cite_start]**Netzwerk-Interdependenz:** Die Ringbahn (S41/S42) wurde als kritischer Schwachpunkt identifiziert, da Störungen hier aufgrund der Systemkopplung Kettenreaktionen auslösen[cite: 92, 93].

除了常规可视化，本项目重点关注数据异常值的识别与因果关系分析：
- [cite_start]**统计噪声消除：** 识别“虚假延误”。分析证明，深夜时段出现的极端延误峰值是由极低样本量（**样本数少于3次**）导致的**统计学上的“虚假信号” (Artefacts)**，而非实际运营故障 [cite: 90]。
- [cite_start]**因果关系研究：** 深入探讨降雨量与延误的相关性。数据显示 S-Bahn 在 10mm 以下降雨中表现出极高韧性，仅在极端天气（Stormy）下系统稳定性才会受损 [cite: 86]。
- [cite_start]**网络耦合性分析：** 识别出环线（S41/S42）为核心脆弱点，其高度耦合的特性会导致局部故障迅速引发全线连锁反应 [cite: 94]。

---


## Haupterkenntnisse | 核心发现

### 1. Primäre Störfaktoren | 首要干扰因素
- **DE:** Koordinierte **Streiks** sind mit durchschnittlich **41,26 Min.** die Hauptursache für massive Netzstörungen. Überraschenderweise werden gemeldete Vorfälle (Incidents) im Alltag effizient umgangen (nur 1,31 Min. Verspätung).
- **CN:** 有组织的**罢工**是导致网络瘫痪的首要因素，平均延误达 **41.26 分钟**。令人惊讶的是，日常报备的突发事故（Incidents）处理效率极高（仅导致 1.31 分钟延误）。

### 2. Wettereinfluss | 天气影响
- **DE:** Die S-Bahn zeigt eine hohe Resilienz gegenüber moderatem Regen (5-10 mm). Erst bei **extremen Wetterlagen (Stormy)** steigen die Verspätungen signifikant an.
- **CN:** S-Bahn 对中雨（5-10mm）表现出极强的韧性。只有在**极端天气（风暴）**下，延误才会大幅增加。

### 3. Linienanalyse: Die Ringbahn | 线路分析：环线
- **DE:** Die **Ringbahn (S41/S42)** ist aufgrund ihrer hohen Systemkopplung anfälliger für Kettenreaktionen als Radiallinien (z. B. S2).
- **CN:** 由于系统耦合度高，**环线（S41/S42）**比射线线路（如 S2）更容易产生连锁反应，导致延误扩散。

---

## Datenquelle | 数据来源
- **Kaggle:** [Berlin S-Bahn Punctuality Database](https://www.kaggle.com/datasets/alperenmyung/berlin-s-bahn-punctuality-database)

---

## Installation & Ausführung | 安装与运行

### 1. Docker Setup
```bash
# Starten der Container-Umgebung | 启动容器环境
docker-compose up -d
```
### 2. Data Ingestion (ETL)
```bash
# Ausführen im Python-Container | 在 Python 容器中执行导入
python ingest_berlin_sbahn.py
```
### 3. Power BI Dashboard

Verbinden Sie Power BI mit `localhost:5432` (PostgreSQL). Die Anmeldedaten werden über Umgebungsvariablen verwaltet.

将 Power BI 连接至 `localhost:5432` (PostgreSQL)。数据库凭据通过环境变量进行安全管理。

---

**Analysiert von / 分析师:** Jinjing Cheng
