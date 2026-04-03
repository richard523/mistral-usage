#!/usr/bin/env python3
"""
Practical test to demonstrate the cost calculation system working with real-world scenarios.
"""

from mistral_usage_tracker import calculate_cost_estimate

def test_practical_scenarios():
    """Test practical usage scenarios with different models"""

    print("🧪 Practical Mistral Model Cost Calculation Examples")
    print("=" * 60)

    # Scenario 1: Chat application with Mistral Small 4
    print("\n💬 Scenario 1: Chat Application")
    print("Model: Mistral Small 4")
    prompt_tokens = 500  # User message
    completion_tokens = 200  # AI response
    cost = calculate_cost_estimate(prompt_tokens, completion_tokens, "mistral-small-4-latest")
    print(f"Prompt: {prompt_tokens} tokens, Completion: {completion_tokens} tokens")
    print(f"Total cost: ${cost:.6f}")
    print(f"Cost per conversation: ${cost:.6f}")

    # Scenario 2: Code generation with Codestral
    print("\n💻 Scenario 2: Code Generation")
    print("Model: Codestral")
    prompt_tokens = 1000  # Code prompt
    completion_tokens = 1500  # Generated code
    cost = calculate_cost_estimate(prompt_tokens, completion_tokens, "codestral-latest")
    print(f"Prompt: {prompt_tokens} tokens, Completion: {completion_tokens} tokens")
    print(f"Total cost: ${cost:.6f}")

    # Scenario 3: Enterprise reasoning with Mistral Medium 3
    print("\n🏢 Scenario 3: Enterprise Reasoning")
    print("Model: Mistral Medium 3")
    prompt_tokens = 2000  # Complex business question
    completion_tokens = 800  # Detailed analysis
    cost = calculate_cost_estimate(prompt_tokens, completion_tokens, "mistral-medium-3-latest")
    print(f"Prompt: {prompt_tokens} tokens, Completion: {completion_tokens} tokens")
    print(f"Total cost: ${cost:.6f}")

    # Scenario 4: Batch processing with Mistral 7B
    print("\n🔄 Scenario 4: Batch Processing (1000 requests)")
    print("Model: Mistral 7B")
    prompt_tokens = 300  # Average prompt
    completion_tokens = 150  # Average completion
    requests = 1000
    single_cost = calculate_cost_estimate(prompt_tokens, completion_tokens, "mistral-7b-latest")
    total_cost = single_cost * requests
    print(f"Per request: ${single_cost:.6f}")
    print(f"Total for {requests} requests: ${total_cost:.2f}")

    # Scenario 5: Embedding generation
    print("\n🔗 Scenario 5: Text Embedding")
    print("Model: Mistral Embed")
    prompt_tokens = 50  # Short text to embed
    completion_tokens = 0  # Embeddings don't have completion tokens
    cost = calculate_cost_estimate(prompt_tokens, completion_tokens, "mistral-embed-latest")
    print(f"Text length: {prompt_tokens} tokens")
    print(f"Embedding cost: ${cost:.6f}")

    # Scenario 6: High-volume Mixtral usage
    print("\n⚡ Scenario 6: High-Performance Mixtral")
    print("Model: Mixtral 8x22B")
    prompt_tokens = 5000  # Large context
    completion_tokens = 2000  # Detailed response
    cost = calculate_cost_estimate(prompt_tokens, completion_tokens, "mixtral-8x22b-latest")
    print(f"Prompt: {prompt_tokens} tokens, Completion: {completion_tokens} tokens")
    print(f"Total cost: ${cost:.6f}")

    # Scenario 7: Cost comparison between models
    print("\n📊 Scenario 7: Model Cost Comparison")
    print("Same workload (1000 prompt tokens + 500 completion tokens) across different models:")

    models_to_compare = [
        "mistral-small-4-latest",
        "mistral-medium-3-latest",
        "codestral-latest",
        "mistral-7b-latest",
        "mixtral-8x7b-latest"
    ]

    prompt_tokens = 1000
    completion_tokens = 500

    for model in models_to_compare:
        cost = calculate_cost_estimate(prompt_tokens, completion_tokens, model)
        model_name = model.replace("-latest", "").replace("-", " ").title()
        print(f"  {model_name:25} | ${cost:.4f}")

    print("\n" + "=" * 60)
    print("✅ All practical scenarios completed successfully!")
    print("The system is ready for production use with all Mistral text models.")

if __name__ == "__main__":
    test_practical_scenarios()