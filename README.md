# mcp-automation-engine
An automation engine powered by the Model Context Protocol (MCP) — connect, orchestrate, and execute intelligent workflows with AI and external tools.

        ┌──────────────────────────────┐
        │ Mock API → Airflow (ETL)     │
        │ fetch_and_insert + transform │
        └─────────────┬────────────────┘
                      │
             Updates DuckDB
                      │
           ┌──────────┴──────────┐
           │ MCP Client (agent)  │
           └──────────┬──────────┘
                      │
     ┌────────────────┴───────────────────┐
     ▼                                    ▼
 DuckDB Server (data)           AI Server (LLM)
     │                                    │
     └──────────► Filesystem Server ◄─────┘
                      │
                 Saves Reports
                      │
                 Streamlit Dashboard

