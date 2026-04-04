#!/usr/bin/env python3
"""
Test EXACT models from the pricing list - no guesswork!
"""

from mistralai.client import Mistral
from mistral_usage_tracker import log_token_usage
from dotenv import load_dotenv
import os
import time

# Load API key
load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")
if not api_key or api_key == "your_mistral_api_key_here":
    print("❌ Please set your MISTRAL_API_KEY in .env file")
    exit(1)

print("🔬 Testing EXACT models from pricing list")

# EXACT models from your pricing list (no additions!)
exact_models = [
    "mistral-large-latest",
    "mistral-small-latest",
    "mistral-medium-latest",
    "devstral-medium-latest",
    "devstral-small-latest",
    "codestral-latest",
    "magistral-medium-latest",
    "magistral-small-latest",
    "ministral-3b-latest",
    "ministral-8b-latest",
    "ministral-14b-latest",
    "mistral-embed",
]

prompts = ["Hello, how are you today?"]

model_status = {}

for model in exact_models:
    print(f"\n📋 Testing {model}:")
    model_status[model] = {"success": 0, "failed": 0, "error": None}
    
    try:
        with Mistral(api_key=api_key) as client:
            response = client.chat.complete(
                model=model,
                messages=[{"role": "user", "content": prompts[0]}]
            )
            
            log_token_usage(
                response,
                model,
                response_time=1.0,
                cache_hit=False,
                input_length=len(prompts[0]),
                temperature=0.7,
                prompt=prompts[0],
                response_text=response.choices[0].message.content
            )
            
            model_status[model]["success"] += 1
            print(f"    ✅ SUCCESS!")
            
    except Exception as e:
        model_status[model]["failed"] += 1
        model_status[model]["error"] = str(e)
        
        if "Invalid model" in str(e):
            print(f"    ❌ INVALID MODEL")
        elif "API key scope" in str(e):
            print(f"    ❌ API SCOPE LIMITED")
        else:
            print(f"    ❌ ERROR: {e}")
    
    time.sleep(1)

print(f"\n{'='*60}")
print("📊 EXACT MODEL TESTING RESULTS")
print(f"{'='*60}")

working = []
failed = []

for model, status in model_status.items():
    if status["success"] > 0:
        working.append(model)
        print(f"✅ {model}")
    else:
        failed.append(model)
        error_type = "INVALID" if "Invalid model" in status["error"] else "SCOPE"
        print(f"❌ {model:25} ({error_type})")

print(f"\nWorking: {len(working)}/{len(exact_models)}")
print(f"Failed: {len(failed)}/{len(exact_models)}")

print(f"\n✅ Done! Check logs/ for working model data")