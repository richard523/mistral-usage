# mistral_token_tracker.py
# mistral_usage_tracker.py
import os
import json
from datetime import datetime
import streamlit as st
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from collections import defaultdict
import argparse

load_dotenv()

def log_token_usage(response, model_name, log_dir="logs", response_time=None, cache_hit=None, input_length=None, temperature=None, max_tokens=None, prompt=None, response_text=None):
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
        "response_time_seconds": response_time,
        "cache_hit": cache_hit,
        "input_length": input_length,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "cost_estimate": calculate_cost_estimate(usage["prompt_tokens"], usage["completion_tokens"], model_name),
        "prompt": prompt,
        "response_text": response_text
    }
    filename = f"{log_dir}/{model_name}_usage.log"
    with open(filename, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

# Rest of the file remains the same...
def calculate_cost_estimate(prompt_tokens, completion_tokens, model_name):
    """Estimate cost based on token usage and model pricing"""
    # Mistral model pricing (per 1M tokens) - based on provided data
    model_pricing = {
        # Flagship multimodal and multilingual models
        "mistral-large-latest": {"prompt": 0.5, "completion": 1.5},  # $0.50 and $1.50 per 1M tokens

        # Mistral Small 4 - A new standard for multimodal, reasoning-optimized models
        "mistral-small-4-latest": {"prompt": 0.15, "completion": 0.6},  # $0.15 and $0.60 per 1M tokens

        # Mistral Medium 3 - State-of-the-art performance. Simplified enterprise deployments. Cost-efficient.
        "mistral-medium-3-latest": {"prompt": 0.4, "completion": 2.0},  # $0.40 and $2.00 per 1M tokens

        # Mistral Small 3.2 - SOTA. Multimodal. Multilingual. Apache 2.0.
        "mistral-small-3.2-latest": {"prompt": 0.1, "completion": 0.3},  # $0.10 and $0.30 per 1M tokens

        # Devstral 2 - Enhanced model for advanced coding agents.
        "devstral-2-latest": {"prompt": 0.4, "completion": 2.0},  # $0.40 and $2.00 per 1M tokens

        # Devstral Small 2 - The best open-source model for coding agents.
        "devstral-small-2-latest": {"prompt": 0.1, "completion": 0.3},  # $0.10 and $0.30 per 1M tokens

        # Codestral - Lightweight, fast, and proficient in over 80 programming languages.
        "codestral-latest": {"prompt": 0.3, "completion": 0.9},  # $0.30 and $0.90 per 1M tokens

        # Leanstral - First open-source code agent for Lean 4.
        "leanstral-latest": {"prompt": 0.0, "completion": 0.0},  # Free API endpoint

        # Magistral Medium - Thinking model excelling in domain-specific, transparent, and multilingual reasoning.
        "magistral-medium-latest": {"prompt": 2.0, "completion": 5.0},  # $2.00 and $5.00 per 1M tokens

        # Magistral Small - Thinking model excelling in domain-specific, transparent, and multilingual reasoning.
        "magistral-small-latest": {"prompt": 0.5, "completion": 1.5},  # $0.50 and $1.50 per 1M tokens

        # Ministral 3 models - Best-in-class frontier AI to the edge.
        "ministral-3-3b-latest": {"prompt": 0.1, "completion": 0.1},  # $0.10 and $0.10 per 1M tokens
        "ministral-3-8b-latest": {"prompt": 0.15, "completion": 0.15},  # $0.15 and $0.15 per 1M tokens
        "ministral-3-14b-latest": {"prompt": 0.2, "completion": 0.2},  # $0.20 and $0.20 per 1M tokens

        # Voxtral TTS - State-of-the-art text-to-speech.
        "voxtral-tts-latest": {"prompt": 0.016, "completion": 0.016},  # $0.016 per 1k characters (approximated)

        # Voxtral transcription models
        "voxtral-mini-transcribe-2-latest": {"prompt": 0.003, "completion": 0.003},  # $0.003 per minute
        "voxtral-realtime-latest": {"prompt": 0.006, "completion": 0.006},  # $0.006 per minute
        "voxtral-small-latest": {"prompt": 0.004, "completion": 0.3},  # $0.004 (audio) / $0.1 (text) per minute, $0.30 per 1M tokens
        "voxtral-mini-latest": {"prompt": 0.001, "completion": 0.04},  # $0.001 (audio) / $0.04 (text) per minute, $0.04 per 1M tokens

        # Pixtral models - Vision-capable models
        "pixtral-large-latest": {"prompt": 2.0, "completion": 6.0},  # $2.00 and $6.00 per 1M tokens
        "pixtral-12b-latest": {"prompt": 0.15, "completion": 0.15},  # $0.15 and $0.15 per 1M tokens

        # Mistral NeMo - State-of-the-art Mistral model trained specifically for code tasks.
        "mistral-nemo-latest": {"prompt": 0.15, "completion": 0.15},  # $0.15 and $0.15 per 1M tokens

        # Mistral 7B - A 7B transformer model, fast-deployed and easily customisable.
        "mistral-7b-latest": {"prompt": 0.25, "completion": 0.25},  # $0.25 and $0.25 per 1M tokens

        # Mixtral models - Sparse Mixture-of-Experts models
        "mixtral-8x7b-latest": {"prompt": 0.7, "completion": 0.7},  # $0.70 and $0.70 per 1M tokens
        "mixtral-8x22b-latest": {"prompt": 2.0, "completion": 6.0},  # $2.00 and $6.00 per 1M tokens

        # Embedding models
        "codestral-embed-latest": {"prompt": 0.15, "completion": 0.15},  # $0.15 per 1M tokens (input only for embeddings)
        "mistral-embed-latest": {"prompt": 0.1, "completion": 0.1},  # $0.10 per 1M tokens (input only for embeddings)

        # Agent API - Enhances AI with built-in tools
        "agent-api-latest": {"prompt": 2.7, "completion": 8.1},  # Model cost per M token + Tool call

        # Classifier models
        "mistral-moderation-latest": {"prompt": 0.1, "completion": 0.1},  # $0.10 per 1M tokens
        "classifier-api-model-8b-latest": {"prompt": 0.1, "completion": 0.1},  # $0.10 per 1M tokens
        "classifier-api-model-3b-latest": {"prompt": 0.04, "completion": 0.04},  # $0.04 per 1M tokens

        # Default fallback pricing (mistral-medium-latest)
        "mistral-medium-latest": {"prompt": 2.7, "completion": 8.1},  # $2.70 and $8.10 per 1M tokens
        "mistral-small-latest": {"prompt": 1.0, "completion": 3.0},  # $1.00 and $3.00 per 1M tokens
    }

    pricing = model_pricing.get(model_name, {"prompt": 2.7, "completion": 8.1})
    prompt_cost = (prompt_tokens / 1_000_000) * pricing["prompt"]
    completion_cost = (completion_tokens / 1_000_000) * pricing["completion"]
    return prompt_cost + completion_cost

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
                    model_totals[model_name]["response_time"] += data.get("response_time_seconds", 0)
                    model_totals[model_name]["cost"] += data.get("cost_estimate", 0)
                    model_totals[model_name]["count"] += 1
    return dict(model_totals)

def run_dashboard(log_dir="logs"):
    os.makedirs(log_dir, exist_ok=True)
    st.title("🚀 Mistral Model Usage Dashboard")
    st.markdown("Comprehensive tracking of API calls, tokens, performance, and costs")

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

    # Convert timestamp to datetime for better plotting
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp")

    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    models = df["model"].unique()
    selected_models = st.sidebar.multiselect("Select models", models, default=models)
    filtered_df = df[df["model"].isin(selected_models)]

    # Date range filter
    min_date = filtered_df["timestamp"].min().date()
    max_date = filtered_df["timestamp"].max().date()
    date_range = st.sidebar.date_input(
        "Date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    if len(date_range) == 2:
        filtered_df = filtered_df[
            (filtered_df["timestamp"].dt.date >= date_range[0]) &
            (filtered_df["timestamp"].dt.date <= date_range[1])
        ]

    st.header("📊 Token Usage Analysis")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Token Usage Over Time")
        token_chart_data = filtered_df.pivot_table(
            index="timestamp",
            columns="model",
            values="total_tokens",
            aggfunc="sum"
        )
        st.line_chart(token_chart_data)

    with col2:
        st.subheader("Token Distribution")
        token_types = filtered_df[["prompt_tokens", "completion_tokens"]].sum()
        st.bar_chart(token_types)

    st.header("⏱️ Performance Metrics")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Response Time Distribution")
        if "response_time_seconds" in filtered_df.columns and not filtered_df["response_time_seconds"].isna().all():
            # Create histogram using numpy and streamlit bar chart
            response_times = filtered_df["response_time_seconds"].dropna()
            hist, bin_edges = np.histogram(response_times, bins=20)
            bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

            # Create histogram chart data
            hist_data = pd.DataFrame({
                'Response Time (seconds)': [f"{edge:.1f}-{bin_edges[i+1]:.1f}" for i, edge in enumerate(bin_edges[:-1])],
                'Frequency': hist
            })

            st.bar_chart(hist_data.set_index('Response Time (seconds)'))
            avg_response_time = response_times.mean()
            st.metric("Average Response Time", f"{avg_response_time:.2f} seconds")
        else:
            st.info("No response time data available")

    with col2:
        st.subheader("Response Time by Model")
        if "response_time_seconds" in filtered_df.columns and not filtered_df["response_time_seconds"].isna().all():
            response_time_by_model = filtered_df.groupby("model")["response_time_seconds"].mean()
            st.bar_chart(response_time_by_model)
        else:
            st.info("No response time data available")

    st.header("💰 Cost Analysis")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Cost Over Time")
        if "cost_estimate" in filtered_df.columns:
            cost_chart_data = filtered_df.pivot_table(
                index="timestamp",
                columns="model",
                values="cost_estimate",
                aggfunc="sum"
            )
            st.area_chart(cost_chart_data)
        else:
            st.info("No cost data available")

    with col2:
        st.subheader("Cost by Model")
        if "cost_estimate" in filtered_df.columns:
            cost_by_model = filtered_df.groupby("model")["cost_estimate"].sum()
            st.bar_chart(cost_by_model)

            total_cost = filtered_df["cost_estimate"].sum()
            st.metric("Total Estimated Cost", f"${total_cost:.4f}")
        else:
            st.info("No cost data available")

    st.header("📈 Advanced Analytics")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Input Length Analysis")
        if "input_length" in filtered_df.columns and not filtered_df["input_length"].isna().all():
            # Create histogram using numpy and streamlit bar chart
            input_lengths = filtered_df["input_length"].dropna()
            hist, bin_edges = np.histogram(input_lengths, bins=15)
            bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

            # Create histogram chart data
            hist_data = pd.DataFrame({
                'Input Length (characters)': [f"{int(edge)}-{int(bin_edges[i+1])}" for i, edge in enumerate(bin_edges[:-1])],
                'Frequency': hist
            })

            st.bar_chart(hist_data.set_index('Input Length (characters)'))
            avg_input_length = input_lengths.mean()
            st.metric("Avg Input Length", f"{avg_input_length:.1f} chars")
        else:
            st.info("No input length data available")

    with col2:
        st.subheader("Cache Hit Rate")
        if "cache_hit" in filtered_df.columns:
            cache_hits = filtered_df["cache_hit"].sum()
            total_requests = len(filtered_df)
            cache_hit_rate = (cache_hits / total_requests * 100) if total_requests > 0 else 0
            st.metric("Cache Hit Rate", f"{cache_hit_rate:.1f}%")
        else:
            st.info("No cache data available")

    with col3:
        st.subheader("Request Statistics")
        total_requests = len(filtered_df)
        st.metric("Total Requests", total_requests)

        if total_requests > 0:
            avg_tokens_per_request = filtered_df["total_tokens"].mean()
            st.metric("Avg Tokens/Request", f"{avg_tokens_per_request:.1f}")

    st.header("🔬 Detailed Data Exploration")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Summary Statistics")
        numeric_cols = filtered_df.select_dtypes(include=['number']).columns
        summary_stats = filtered_df[numeric_cols].describe()
        st.dataframe(summary_stats)

    with col2:
        st.subheader("Model Comparison")
        if len(selected_models) > 1:
            model_comparison = filtered_df.groupby("model").agg({
                "total_tokens": "sum",
                "response_time_seconds": "mean",
                "cost_estimate": "sum",
                "prompt_tokens": "sum",
                "completion_tokens": "sum"
            })
            st.dataframe(model_comparison)
        else:
            st.info("Select multiple models to compare")

    st.header("📝 Prompt and Response Details")
    if "prompt" in filtered_df.columns and "response_text" in filtered_df.columns:
        selected_row = st.selectbox(
            "Select a log entry to view details",
            range(len(filtered_df)),
            format_func=lambda x: f"Entry {x + 1}: {filtered_df.iloc[x]['timestamp']}"
        )
        
        st.subheader("Prompt")
        st.text_area("Prompt", filtered_df.iloc[selected_row]["prompt"], height=100, disabled=True)
        
        st.subheader("Response")
        st.text_area("Response", filtered_df.iloc[selected_row]["response_text"], height=200, disabled=True)
    else:
        st.info("No prompt or response data available.")

    st.header("📋 Raw Data")
    # Only show columns that exist in the dataframe
    available_columns = [
        "timestamp", "model", "prompt_tokens", "completion_tokens", "total_tokens"
    ]
    optional_columns = [
        "response_time_seconds", "cost_estimate", "input_length", "cache_hit",
        "temperature", "max_tokens"
    ]

    # Add optional columns if they exist
    for col in optional_columns:
        if col in filtered_df.columns:
            available_columns.append(col)

    st.dataframe(
        filtered_df[available_columns],
        width='stretch',
        height=300
    )

    # Download button for raw data
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Data as CSV",
        data=csv,
        file_name="mistral_usage_data.csv",
        mime="text/csv"
    )

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
