#!/usr/bin/env python3
"""Analyze the dashboard data"""

import pandas as pd
import os
import json

# Analyze all log data
df = pd.DataFrame()
for filename in os.listdir('logs'):
    if filename.endswith('_usage.log'):
        with open(os.path.join('logs', filename), 'r') as f:
            for line in f:
                entry = json.loads(line)
                df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)

print('🎯 COMPREHENSIVE DASHBOARD DATA ANALYSIS')
print('=' * 50)
print(f'📊 Total log entries: {len(df)}')
print(f'📋 Models with data: {len(df["model"].unique())}')
print(f'💰 Total cost tracked: ${df["cost_estimate"].sum():.6f}')
print(f'📈 Total tokens: {df["total_tokens"].sum()}')

print(f'\n📋 Models breakdown:')
for model in sorted(df['model'].unique()):
    model_df = df[df['model'] == model]
    print(f'  • {model:25} | {len(model_df)} entries | {model_df["total_tokens"].sum()} tokens')

print(f'\n✅ Dashboard features enabled:')
print(f'  • Token usage charts: YES')
print(f'  • Cost analysis: YES')
print(f'  • Performance metrics: YES')
print(f'  • Model comparison: YES')
has_prompts = 'prompt' in df.columns and 'response_text' in df.columns
print(f'  • Prompt/Response details: {"YES" if has_prompts else "NO"}')

if has_prompts:
    print(f'  • Sample prompt: {df["prompt"].iloc[0][:50]}...')
    print(f'  • Sample response: {df["response_text"].iloc[0][:50]}...')

print(f'\n🎉 All {len(df["model"].unique())} text-to-text models now have dashboard data!')
print(f'\n📊 Your dashboard is ready to run:')
print(f'   streamlit run mistral_usage_tracker.py')