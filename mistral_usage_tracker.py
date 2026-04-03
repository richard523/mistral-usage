# mistral_token_tracker.py
# mistral_usage_tracker.py
import os
import json
from datetime import datetime
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from collections import defaultdict
import argparse

load_dotenv()

def log_token_usage(response, model_name, log_dir="logs"):
    os.makedirs(log_dir, exist_ok=True)
    # Access usage from the response object
    usage = {
        "prompt_tokens": response.usage.prompt_tokens,
        "completion_tokens": response.usage.completion_tokens,
        "total_tokens": response.usage.total_tokens,
    }
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "model": model_name,
        "prompt_tokens": usage["prompt_tokens"],
        "completion_tokens": usage["completion_tokens"],
        "total_tokens": usage["total_tokens"],
    }
    filename = f"{log_dir}/{model_name}_usage.log"
    with open(filename, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

# Rest of the file remains the same...
def aggregate_token_usage(log_dir="logs"):
    model_totals = defaultdict(lambda: defaultdict(int))
    os.makedirs(log_dir, exist_ok=True)
    for filename in os.listdir(log_dir):
        if filename.endswith("_usage.log"):
            model_name = filename.replace("_usage.log", "")
            with open(os.path.join(log_dir, filename), "r") as f:
                for line in f:
                    data = json.loads(line)
                    model_totals[model_name]["prompt_tokens"] += data["prompt_tokens"]
                    model_totals[model_name]["completion_tokens"] += data["completion_tokens"]
                    model_totals[model_name]["total_tokens"] += data["total_tokens"]
    return dict(model_totals)

def run_dashboard(log_dir="logs"):
    os.makedirs(log_dir, exist_ok=True)
    st.title("Mistral Model Token Usage Dashboard")
    df = pd.DataFrame()
    for filename in os.listdir(log_dir):
        if filename.endswith("_usage.log"):
            model_name = filename.replace("_usage.log", "")
            with open(os.path.join(log_dir, filename), "r") as f:
                for line in f:
                    entry = json.loads(line)
                    entry["model"] = model_name
                    df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)

    if df.empty:
        st.warning("No log files found. Run the logger first!")
        return

    models = df["model"].unique()
    selected_models = st.multiselect("Select models", models, default=models)
    filtered_df = df[df["model"].isin(selected_models)]

    st.subheader("Token Usage Over Time")
    st.line_chart(
        filtered_df.pivot(index="timestamp", columns="model", values="total_tokens")
    )

    st.subheader("Total Token Usage by Model")
    totals = filtered_df.groupby("model").sum(numeric_only=True)
    st.bar_chart(totals[["prompt_tokens", "completion_tokens", "total_tokens"]])

    st.subheader("Raw Data")
    st.dataframe(filtered_df)

if __name__ == "__main__":
    # Check if we're running under Streamlit
    import sys
    if "streamlit" in sys.modules:
        # When run with streamlit, automatically show dashboard
        run_dashboard()
    else:
        # Normal command line usage
        parser = argparse.ArgumentParser(description="Mistral Token Usage Tracker")
        parser.add_argument("--log", action="store_true", help="Log token usage from API responses")
        parser.add_argument("--aggregate", action="store_true", help="Aggregate token usage")
        parser.add_argument("--dashboard", action="store_true", help="Run the Streamlit dashboard")
        args = parser.parse_args()

        if args.log:
            print("Run this script with --log in your API call handler.")
        elif args.aggregate:
            totals = aggregate_token_usage()
            print("Total token usage per model:")
            for model, data in totals.items():
                print(f"{model}: {data}")
        elif args.dashboard:
            run_dashboard()
        else:
            print("Use --log, --aggregate, or --dashboard to run.")
