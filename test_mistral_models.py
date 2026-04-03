#!/usr/bin/env python3
"""
Test script to verify that all Mistral text models and their costs are properly configured.
"""

from mistral_usage_tracker import calculate_cost_estimate

def test_mistral_models():
    """Test that all Mistral text models have correct pricing"""

    # Test cases: (model_name, prompt_tokens, completion_tokens, expected_cost_range)
    test_cases = [
        # Flagship models
        ("mistral-large-latest", 1000000, 1000000, (1.9, 2.1)),  # $0.5 + $1.5 = $2.0

        # Mistral Small 4
        ("mistral-small-4-latest", 1000000, 1000000, (0.7, 0.8)),  # $0.15 + $0.6 = $0.75

        # Mistral Medium 3
        ("mistral-medium-3-latest", 1000000, 1000000, (2.3, 2.5)),  # $0.4 + $2.0 = $2.4

        # Mistral Small 3.2
        ("mistral-small-3.2-latest", 1000000, 1000000, (0.35, 0.45)),  # $0.1 + $0.3 = $0.4

        # Devstral models
        ("devstral-2-latest", 1000000, 1000000, (2.3, 2.5)),  # $0.4 + $2.0 = $2.4
        ("devstral-small-2-latest", 1000000, 1000000, (0.35, 0.45)),  # $0.1 + $0.3 = $0.4

        # Codestral
        ("codestral-latest", 1000000, 1000000, (1.1, 1.3)),  # $0.3 + $0.9 = $1.2

        # Leanstral (free)
        ("leanstral-latest", 1000000, 1000000, (-0.1, 0.1)),  # $0.0 + $0.0 = $0.0

        # Magistral models
        ("magistral-medium-latest", 1000000, 1000000, (6.9, 7.1)),  # $2.0 + $5.0 = $7.0
        ("magistral-small-latest", 1000000, 1000000, (1.9, 2.1)),  # $0.5 + $1.5 = $2.0

        # Ministral 3 models
        ("ministral-3-3b-latest", 1000000, 1000000, (0.15, 0.25)),  # $0.1 + $0.1 = $0.2
        ("ministral-3-8b-latest", 1000000, 1000000, (0.25, 0.35)),  # $0.15 + $0.15 = $0.3
        ("ministral-3-14b-latest", 1000000, 1000000, (0.35, 0.45)),  # $0.2 + $0.2 = $0.4

        # Mixtral models
        ("mixtral-8x7b-latest", 1000000, 1000000, (1.3, 1.5)),  # $0.7 + $0.7 = $1.4
        ("mixtral-8x22b-latest", 1000000, 1000000, (7.9, 8.1)),  # $2.0 + $6.0 = $8.0

        # Mistral 7B
        ("mistral-7b-latest", 1000000, 1000000, (0.45, 0.55)),  # $0.25 + $0.25 = $0.5

        # Embedding models (typically only prompt tokens matter)
        ("mistral-embed-latest", 1000000, 0, (0.05, 0.15)),  # $0.1 per 1M tokens

        # Default fallback
        ("unknown-model", 1000000, 1000000, (10.7, 10.9)),  # $2.7 + $8.1 = $10.8
    ]

    print("Testing Mistral model pricing...")
    print("=" * 60)

    all_passed = True

    for model_name, prompt_tokens, completion_tokens, expected_range in test_cases:
        actual_cost = calculate_cost_estimate(prompt_tokens, completion_tokens, model_name)
        expected_min, expected_max = expected_range

        if expected_min <= actual_cost <= expected_max:
            status = "✅ PASS"
        else:
            status = "❌ FAIL"
            all_passed = False

        print(f"{status} {model_name:30} | Cost: ${actual_cost:8.4f} | Expected: ${expected_min:5.2f}-${expected_max:5.2f}")

    print("=" * 60)

    if all_passed:
        print("🎉 All tests passed! All Mistral text models are properly configured.")
    else:
        print("⚠️  Some tests failed. Please check the pricing configuration.")

    return all_passed

def list_all_models():
    """List all available models in the system"""
    print("\nAvailable Mistral Text Models:")
    print("=" * 40)

    # Import the function to access the model_pricing dictionary
    from mistral_usage_tracker import calculate_cost_estimate
    import inspect

    # Get the source code of the function
    source = inspect.getsource(calculate_cost_estimate)

    # Extract model names from the source
    models = []
    for line in source.split('\n'):
        if '": {' in line and 'prompt"' in line:
            # Extract model name
            model_start = line.find('"') + 1
            model_end = line.find('"', model_start)
            if model_start > 0 and model_end > model_start:
                model_name = line[model_start:model_end]
                models.append(model_name)

    # Sort and display models
    models.sort()
    for i, model in enumerate(models, 1):
        print(f"{i:2}. {model}")

    print(f"\nTotal: {len(models)} models configured")

if __name__ == "__main__":
    success = test_mistral_models()
    list_all_models()

    if success:
        print("\n✅ System is ready to track usage and costs for all Mistral text models!")
    else:
        print("\n❌ Please review the model pricing configuration.")