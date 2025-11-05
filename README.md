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
├── db/                             #from previous project
│   ├── raw_data.duckdb
│   ├── db_connection.py
│   ├── init_schema.py
│   ├── fetch_and_insert.py
│   ├── transformations.py
│
├── airflow/                        #from previous project
│   ├── dags/
│   │   └── etl_pipeline.py
│   ├── docker-compose.yaml
│
├── agents/
│   ├── insights_agent.py
│   ├── scheduler.py
│
├── mcp_layer/
│   ├── client.py
│   ├── servers/
│   │   ├── duckdb_server.py
│   │   ├── filesystem_server.py
│   │   ├── ai_server.py
│
├── dashboard/
│   └── app.py
│
├── reports/
│   ├── daily_summary.txt
│   ├── anomalies.json
│
├── config/
│   ├── config.json
│   ├── .env
│
├── requirements.txt                #from previous project
├── .gitignore
└── README.md
