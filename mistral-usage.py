import streamlit as st
import pandas as pd
import json

def load_usage_data(log_file="token_usage.log"):
    data = []
    with open(log_file, "r") as f:
        for line in f:
            data.append(json.loads(line))
    return pd.DataFrame(data)

def main():
    st.title("Token Usage Dashboard")
    df = load_usage_data()

    st.line_chart(
        df.set_index("timestamp")[["prompt_tokens", "completion_tokens", "total_tokens"]]
    )

    st.dataframe(df)

if __name__ == "__main__":
    main()
