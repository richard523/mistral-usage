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

    models = [
        "mistral-medium-latest", "mistral-small-latest",  # Legacy models
        "mistral-medium-3-latest", "mistral-small-4-latest",  # Latest 2024 models
        "devstral-2-latest", "codestral-latest",           # Latest coding models
        "ministral-3-8b-latest", "mixtral-8x7b-latest"     # Latest efficient models
    ]
    prompts = [
        "Explain quantum computing in simple terms",
        "Write a Python function to sort a list",
        "What are the latest advances in AI?",
        "Generate a marketing plan for a tech startup",
        "Debug this Python code for me"
    ]

    # Generate sample data for the last 7 days (current dates)
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

        # Calculate cost using proper pricing for each model
        if model == "mistral-medium-latest":
            prompt_cost = (prompt_tokens / 1_000_000) * 2.7
            completion_cost = (completion_tokens / 1_000_000) * 8.1
        elif model == "mistral-small-latest":
            prompt_cost = (prompt_tokens / 1_000_000) * 1.0
            completion_cost = (completion_tokens / 1_000_000) * 3.0
        elif model == "mistral-medium-3-latest":
            prompt_cost = (prompt_tokens / 1_000_000) * 0.4
            completion_cost = (completion_tokens / 1_000_000) * 2.0
        elif model == "mistral-small-4-latest":
            prompt_cost = (prompt_tokens / 1_000_000) * 0.15
            completion_cost = (completion_tokens / 1_000_000) * 0.6
        elif model == "devstral-2-latest":
            prompt_cost = (prompt_tokens / 1_000_000) * 0.4
            completion_cost = (completion_tokens / 1_000_000) * 2.0
        elif model == "codestral-latest":
            prompt_cost = (prompt_tokens / 1_000_000) * 0.3
            completion_cost = (completion_tokens / 1_000_000) * 0.9
        elif model == "ministral-3-8b-latest":
            prompt_cost = (prompt_tokens / 1_000_000) * 0.15
            completion_cost = (completion_tokens / 1_000_000) * 0.15
        elif model == "mixtral-8x7b-latest":
            prompt_cost = (prompt_tokens / 1_000_000) * 0.7
            completion_cost = (completion_tokens / 1_000_000) * 0.7
        else:
            # Default fallback
            prompt_cost = (prompt_tokens / 1_000_000) * 2.7
            completion_cost = (completion_tokens / 1_000_000) * 8.1

        cost_estimate = prompt_cost + completion_cost

        # Generate prompt and response text for dashboard display
        prompt_text = prompt
        response_text = f"This is a sample response from {model} for the prompt: '{prompt}'"
        if "Python" in prompt:
            response_text = """def sort_list(lst):
    return sorted(lst)

# Example usage:
my_list = [3, 1, 4, 1, 5, 9, 2]
sorted_list = sort_list(my_list)
print(sorted_list)  # Output: [1, 1, 2, 3, 4, 5, 9]"""
        elif "quantum computing" in prompt:
            response_text = "Quantum computing uses quantum bits (qubits) that can exist in multiple states simultaneously, enabling much faster computation for certain problems compared to classical computers."
        elif "AI" in prompt:
            response_text = "Recent advances in AI include transformer architectures, diffusion models for image generation, and improved reinforcement learning techniques for decision making."
        elif "marketing plan" in prompt:
            response_text = "A tech startup marketing plan should include target audience analysis, competitive positioning, digital marketing strategies, and metrics for measuring success."
        elif "Debug" in prompt:
            response_text = "Common Python debugging techniques include using print statements, the pdb debugger, analyzing tracebacks, and writing unit tests to isolate issues."

        # Create log entry with all fields
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
            "cost_estimate": cost_estimate,
            "prompt": prompt_text,
            "response_text": response_text
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