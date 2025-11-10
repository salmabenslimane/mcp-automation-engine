import os
import sys
import logging
from pathlib import Path
from textwrap import dedent

import duckdb
import pandas as pd
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# === CONFIGURATION ===
MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"  # ✅ Open-source model (no login required)
DB_PATH = Path(__file__).resolve().parents[1] / "db" / "raw_data.duckdb"
LOG_LEVEL = logging.INFO

# === LOGGING SETUP ===
logging.basicConfig(
    stream=sys.stdout,
    level=LOG_LEVEL,
    format="%(levelname)s: %(message)s"
)
log = logging.getLogger(__name__)


# === MODEL LOADING ===
def load_model(model_name: str):
    """
    Load TinyLlama model and tokenizer into a text-generation pipeline.
    """
    log.info("🧠 Loading model: %s", model_name)
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto")
        gen = pipeline("text-generation", model=model, tokenizer=tokenizer, device_map="auto")
        return gen
    except Exception as exc:
        log.exception("❌ Failed to load model: %s", exc)
        raise


# === DATABASE FETCH ===
def fetch_recent_kpis(db_path: Path, table: str = "processed.bookings_summary", limit: int = 7) -> pd.DataFrame:
    """
    Fetch the last `limit` rows of KPIs from DuckDB.
    """
    if not db_path.exists():
        raise FileNotFoundError(f"Database file not found: {db_path}")

    query = f"SELECT * FROM {table} ORDER BY load_date DESC LIMIT {limit};"
    try:
        with duckdb.connect(str(db_path)) as conn:
            df = conn.execute(query).fetchdf()
        log.info("✅ Retrieved %d rows from %s", len(df), table)
        return df
    except Exception as exc:
        log.exception("❌ Error querying DuckDB: %s", exc)
        raise


# === INSIGHT GENERATION ===
def generate_insights(llm_pipeline, df: pd.DataFrame) -> str:
    """
    Use the LLM to analyze the KPI table and produce a short summary.
    """
    if df.empty:
        return "⚠️ No KPI data found. Please run your ETL pipeline first."

    try:
        table_text = df.to_markdown(index=False)
    except Exception:
        table_text = df.to_string(index=False)

    prompt = dedent(f"""
        You are an AI business analyst.
        Analyze the last {len(df)} days of flight KPIs shown below:

        {table_text}

        Write a short, professional summary of revenue trends, growth, or anomalies.
    """).strip()

    log.info("🤖 Generating insights...")
    try:
        outputs = llm_pipeline(
            prompt,
            max_new_tokens=250,
            do_sample=True,           # ✅ enable sampling to avoid empty output
            temperature=0.7,          # ✅ adds variability
            top_p=0.9,                # ✅ nucleus sampling
            repetition_penalty=1.1,   # ✅ avoids repetitive loops
        )

        if not outputs:
            raise RuntimeError("No output from model pipeline.")

        generated = outputs[0].get("generated_text", "").strip()

        # Remove prompt echo if present
        if generated.startswith(prompt):
            generated = generated[len(prompt):].strip()

        return generated
    except Exception as exc:
        log.exception("❌ Error during generation: %s", exc)
        raise


# === MAIN ENTRY POINT ===
def main():
    try:
        llm = load_model(MODEL_NAME)
    except Exception:
        log.error("🚨 Model load failed. Exiting.")
        return

    try:
        df = fetch_recent_kpis(DB_PATH)
    except Exception:
        log.error("🚨 Failed to fetch KPIs. Exiting.")
        return

    try:
        insights = generate_insights(llm, df)
        print("\n💡 AI Insight:\n")
        print(insights if insights else "⚠️ Model returned no text.")
    except Exception:
        log.error("🚨 Insight generation failed.")


if __name__ == "__main__":
    main()
