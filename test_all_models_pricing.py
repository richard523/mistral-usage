# test_all_models_pricing.py
"""
Script to test all Mistral models and verify their pricing based on API calls.
This script iterates through all available models, makes a sample API call,
and verifies the pricing against the expected values.
"""

from mistralai.client import Mistral
from mistral_usage_tracker import log_token_usage, calculate_cost_estimate
from dotenv import load_dotenv
import os
import time
import json

# Load API key from .env
load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")
if not api_key:
    raise ValueError("MISTRAL_API_KEY not found in .env file.")

# List of available Mistral models to test
# Based on the API key scope, only mistral-medium-latest is available
models_to_test = [
    "mistral-medium-latest",
    "mistral-small-latest",  # Adding another model to test
    "mistral-tiny-latest",   # Adding another model to test
    # Add other models here if they become available
]

# Sample prompt to use for testing
sample_prompt = "Hello, how are you?"

def test_model_pricing(model_name):
    """Test a specific model and verify its pricing."""
    print(f"\n{'='*60}")
    print(f"Testing model: {model_name}")
    print(f"{'='*60}")
    
    try:
        with Mistral(api_key=api_key) as client:
            # Start timing
            start_time = time.time()
            
            # Make API call
            response = client.chat.complete(
                model=model_name,
                messages=[{"role": "user", "content": sample_prompt}]
            )
            
            # End timing
            end_time = time.time()
            duration = end_time - start_time
            
            # Extract token usage
            prompt_tokens = response.usage.prompt_tokens
            completion_tokens = response.usage.completion_tokens
            total_tokens = response.usage.total_tokens
            
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Completion tokens: {completion_tokens}")
            print(f"Total tokens: {total_tokens}")
            print(f"Response time: {duration:.2f} seconds")
            
            # Calculate cost estimate
            cost_estimate = calculate_cost_estimate(prompt_tokens, completion_tokens, model_name)
            print(f"Estimated cost: ${cost_estimate:.6f}")
            
            # Verify pricing against expected values
            expected_pricing = get_expected_pricing(model_name)
            if expected_pricing:
                expected_cost = calculate_expected_cost(prompt_tokens, completion_tokens, expected_pricing)
                print(f"Expected cost: ${expected_cost:.6f}")
                
                # Check if the calculated cost matches the expected cost
                if abs(cost_estimate - expected_cost) < 1e-6:
                    print("✅ Pricing verification passed!")
                else:
                    print("⚠️ Pricing verification failed!")
            else:
                print("⚠️ No expected pricing data available for this model.")
            
            # Log token usage
            log_token_usage(
                response,
                model_name,
                response_time=duration,
                cache_hit=False,
                input_length=len(sample_prompt),
                temperature=0.7,
                max_tokens=None,
                prompt=sample_prompt,
                response_text=response.choices[0].message.content
            )
            
            print(f"✅ Successfully tested {model_name}")
            
            return {
                "model": model_name,
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": total_tokens,
                "response_time": duration,
                "cost_estimate": cost_estimate,
                "expected_cost": expected_cost if expected_pricing else None
            }
            
    except Exception as e:
        print(f"❌ Error testing {model_name}: {str(e)}")
        return None

def get_expected_pricing(model_name):
    """Get the expected pricing for a model from the Mistral pricing page."""
    # Expected pricing based on Mistral's pricing page
    expected_pricing = {
        "mistral-medium-latest": {"prompt": 2.7, "completion": 8.1},
        "mistral-small-latest": {"prompt": 1.0, "completion": 3.0},  # Updated to match actual pricing
        "mistral-tiny-latest": {"prompt": 0.1, "completion": 0.3},
    }
    return expected_pricing.get(model_name)

def calculate_expected_cost(prompt_tokens, completion_tokens, pricing):
    """Calculate the expected cost based on token usage and pricing."""
    prompt_cost = (prompt_tokens / 1_000_000) * pricing["prompt"]
    completion_cost = (completion_tokens / 1_000_000) * pricing["completion"]
    return prompt_cost + completion_cost

def main():
    """Main function to test all models and verify pricing."""
    print("Starting Mistral model pricing verification...")
    print(f"Testing {len(models_to_test)} models...")
    
    results = []
    
    for model_name in models_to_test:
        result = test_model_pricing(model_name)
        if result:
            results.append(result)
        
        # Small delay between requests to avoid rate limiting
        time.sleep(1)
    
    # Print summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"Total models tested: {len(results)}")
    print(f"Total cost estimate: ${sum(r['cost_estimate'] for r in results):.6f}")
    print(f"Total tokens used: {sum(r['total_tokens'] for r in results)}")
    
    # Save results to a JSON file
    with open("model_pricing_verification_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("\nResults saved to model_pricing_verification_results.json")
    print("Pricing verification complete!")

if __name__ == "__main__":
    main()