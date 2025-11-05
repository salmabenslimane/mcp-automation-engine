from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import duckdb
import pandas as pd

MODEL_NAME = "google/gemma-2b-it"


print(f"🧠 Loading model: {MODEL_NAME}")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    device_map="auto",
    trust_remote_code=True,
)
llm = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=300)

DB_PATH = "db/raw_data.duckdb"

def generate_insights():
    conn = duckdb.connect(DB_PATH)
    df = conn.execute("SELECT * FROM processed.bookings_summary ORDER BY load_date DESC LIMIT 7;").fetchdf()
    conn.close()

    if df.empty:
        return "⚠️ No KPI data found. Please run your ETL pipeline first."

    prompt = f"""
    You are an AI business analyst. Analyze the last 7 days of flight KPIs:
    {df.to_markdown()}
    Provide a short professional summary of revenue trends, growth, or anomalies.
    """

    print("🧠 Generating insights...")
    result = llm(prompt)[0]["generated_text"]
    return result.split(prompt)[-1].strip()

if __name__ == "__main__":
    insights = generate_insights()
    print("\n💡 AI Insight:\n")
    print(insights)
