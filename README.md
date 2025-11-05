# ✈️ Flight Intelligence Automation Agent

A local AI-powered automation system that transforms flight sales data into actionable insights — built on top of your `Flight Sales Data Pipeline` project using **DuckDB**, **Airflow**, **Streamlit**, and **open-source LLMs** orchestrated via the **Model Context Protocol (MCP)**.

---

## 🧭 Overview

This project extends the previous Airflow ETL pipeline into a full **AI automation system**.  
It connects flight sales data (simulated via Mock API) with a local Hugging Face LLM to:
- Generate **daily business insights** from flight data.
- Automate summaries and anomaly detection.
- Store and visualize insights in a **Streamlit dashboard**.
- Run fully **locally**, using the **MCP framework** for modular automation.

---

## ⚙️ Tech Stack

| Layer | Tool | Purpose |
|-------|------|----------|
| 🐍 Programming | Python | Core scripting language |
| 🪶 Storage | DuckDB | Analytical database |
| 🧱 Orchestration | Apache Airflow | ETL and automation |
| 🧠 AI Model | Hugging Face (Phi-2 / Mistral / Llama) | Insight generation |
| 🔗 Protocol | MCP (Model Context Protocol) | Tool orchestration |
| 📊 Visualization | Streamlit | Interactive dashboards |
| 🪄 Automation | Watchdog / Cron | Local triggers for automation |
| 🐳 Containerization | Docker | Optional Airflow deployment |

---

## 📂 Folder Structure

```bash
flight_intelligence_agent/
├── db/                             
│   ├── raw_data.duckdb
│   ├── db_connection.py
│   ├── init_schema.py
│   ├── fetch_and_insert.py
│   └── transformations.py
│
├── airflow/                        
│   ├── dags/
│   │   └── etl_pipeline.py
│   └── docker-compose.yaml
│
├── agents/
│   ├── insights_agent.py
│   └── scheduler.py
│
├── mcp_layer/
│   ├── client.py
│   └── servers/
│       ├── duckdb_server.py
│       ├── filesystem_server.py
│       └── ai_server.py
│
├── dashboard/
│   └── app.py
│
├── reports/
│   ├── daily_summary.txt
│   └── anomalies.json
│
├── config/
│   ├── config.json
│   └── .env
│
├── requirements.txt                
├── .gitignore
└── README.md
```

## 🧩 Architecture

![Architecture Diagram](flight_intelligence_architecture.png)

---

## 🔍 How It Works

### 🛫 Data Ingestion
- `fetch_and_insert.py` fetches flight data from the **Mock API**.
- Airflow DAG (`etl_pipeline.py`) automates the daily **ETL** process *(Extract → Transform → Load)*.
- Data is stored in **DuckDB** under the schema `raw.bookings`.

---

### 🔄 Data Transformation
- `transformations.py` computes KPIs such as **total revenue**, **average ticket price**, and **unique passenger count**.
- Processed data is stored in the **processed schema** for analysis.

---

### 🧠 AI Insights Layer
- The **MCP AI Agent** (`insights_agent.py`) connects to **DuckDB** and retrieves KPIs.
- It feeds the data into an **open-source Hugging Face model** (e.g. `Phi-2` or `Mistral`).
- The agent generates **natural-language summaries** and **anomaly alerts**, saved in `/reports/`.

---

### ⚙️ Automation via MCP
- The **MCP Client** orchestrates communication between multiple local servers:

| Server | Purpose |
|---------|----------|
| 🪶 `duckdb_server.py` | Exposes SQL queries and KPI data. |
| 📁 `filesystem_server.py` | Manages local report generation and file monitoring. |
| 🧠 `ai_server.py` | Wraps a Hugging Face LLM for text generation and inference. |

➡️ The **AI Agent** acts as the central orchestrator, dynamically calling these servers through the **Model Context Protocol**.

---

### 📊 Visualization
- The **Streamlit dashboard** reads processed data from **DuckDB** and insights from `/reports/`.
- Displays **real-time KPIs**, **sales trends**, and **AI-generated summaries**.

---

## 🧠 Example Output

**Example AI Summary:**

> Revenue increased **8% week-over-week**, primarily driven by **Business Class bookings** from *Paris → New York.*  
> However, **Economy fares** saw a **5% drop** in occupancy rate due to seasonal effects.

---

## 🚀 Quickstart

### 1️⃣ Setup Environment
```bash
git clone https://github.com/<your-username>/flight_intelligence_agent.git
cd flight_intelligence_agent
pip install -r requirements.txt
```

### 2️⃣ Run ETL Pipeline
```bash
python db/init_schema.py
python db/fetch_and_insert.py
```
Or start with Airflow:
```bash
docker-compose up
```

### 3️⃣ Run AI Insight Agent
```bash
python agents/insights_agent.py
```

### 4️⃣ Launch Dashboard
```bash
streamlit run dashboard/app.py
```