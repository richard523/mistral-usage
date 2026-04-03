#!/usr/bin/env python3
"""
Test script to generate sample data with enhanced metadata
This will create log entries with all the new metadata fields
"""

import json
import os
from datetime import datetime, timedelta
import random

def generate_sample_data():
    """Generate sample log entries with enhanced metadata"""
    os.makedirs("logs", exist_ok=True)

    models = ["mistral-medium-latest", "mistral-small-latest"]
    prompts = [
        "Explain quantum computing in simple terms",
        "Write a Python function to sort a list",
        "What are the latest advances in AI?",
        "Generate a marketing plan for a tech startup",
        "Debug this Python code for me"
    ]

    # Generate sample data for the last 7 days
    now = datetime.now()
    for i in range(20):  # Generate 20 sample entries
        days_ago = random.randint(0, 6)
        timestamp = now - timedelta(days=days_ago, hours=random.randint(0, 23), minutes=random.randint(0, 59))

        model = random.choice(models)
        prompt = random.choice(prompts)

        # Generate realistic token counts
        prompt_tokens = random.randint(10, 100)
        completion_tokens = random.randint(50, 500)
        total_tokens = prompt_tokens + completion_tokens

        # Generate metadata
        response_time = round(random.uniform(0.5, 10.0), 2)
        cache_hit = random.choice([True, False, False, False])  # 25% cache hit rate
        input_length = len(prompt)
        temperature = round(random.uniform(0.1, 1.0), 1)
        max_tokens = random.choice([None, 100, 256, 512])

        # Calculate cost
        if model == "mistral-medium-latest":
            prompt_cost = (prompt_tokens / 1_000_000) * 2.7
            completion_cost = (completion_tokens / 1_000_000) * 8.1
        else:  # mistral-small-latest
            prompt_cost = (prompt_tokens / 1_000_000) * 1.0
            completion_cost = (completion_tokens / 1_000_000) * 3.0

        cost_estimate = prompt_cost + completion_cost

        # Create log entry
        log_entry = {
            "timestamp": timestamp.isoformat(),
            "model": model,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
            "response_time_seconds": response_time,
            "cache_hit": cache_hit,
            "input_length": input_length,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "cost_estimate": cost_estimate
        }

        # Write to log file
        filename = f"logs/{model}_usage.log"
        with open(filename, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

        print(f"Generated sample entry: {model} - {prompt_tokens} prompt tokens, {completion_tokens} completion tokens")

if __name__ == "__main__":
    print("🔄 Generating sample data with enhanced metadata...")
    generate_sample_data()
    print("✅ Sample data generation complete!")
    print("📊 You can now run the dashboard to see all the new visualizations:")
    print("   streamlit run mistral_usage_tracker.py")