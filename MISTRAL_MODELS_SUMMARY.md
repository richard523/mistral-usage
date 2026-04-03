# Mistral Text Models - Complete List with Pricing

This document summarizes all Mistral text models that have been added to the system with their respective pricing.

## Flagship Models

### Mistral Large
- **Model ID**: `mistral-large-latest`
- **Type**: Open-weight, general-purpose, flagship multimodal and multilingual model
- **Pricing**:
  - Input: $0.50 per 1M tokens
  - Output: $1.50 per 1M tokens

## Mistral Small Series

### Mistral Small 4
- **Model ID**: `mistral-small-4-latest`
- **Type**: A new standard for multimodal, reasoning-optimized models
- **Pricing**:
  - Input: $0.15 per 1M tokens
  - Output: $0.60 per 1M tokens

### Mistral Small 3.2
- **Model ID**: `mistral-small-3.2-latest`
- **Type**: SOTA. Multimodal. Multilingual. Apache 2.0.
- **Pricing**:
  - Input: $0.10 per 1M tokens
  - Output: $0.30 per 1M tokens

## Mistral Medium Series

### Mistral Medium 3
- **Model ID**: `mistral-medium-3-latest`
- **Type**: State-of-the-art performance. Simplified enterprise deployments. Cost-efficient.
- **Pricing**:
  - Input: $0.40 per 1M tokens
  - Output: $2.00 per 1M tokens

## Developer/Coding Models

### Devstral 2
- **Model ID**: `devstral-2-latest`
- **Type**: Enhanced model for advanced coding agents
- **Pricing**:
  - Input: $0.40 per 1M tokens
  - Output: $2.00 per 1M tokens

### Devstral Small 2
- **Model ID**: `devstral-small-2-latest`
- **Type**: The best open-source model for coding agents
- **Pricing**:
  - Input: $0.10 per 1M tokens
  - Output: $0.30 per 1M tokens

### Codestral
- **Model ID**: `codestral-latest`
- **Type**: Lightweight, fast, and proficient in over 80 programming languages
- **Pricing**:
  - Input: $0.30 per 1M tokens
  - Output: $0.90 per 1M tokens

### Leanstral
- **Model ID**: `leanstral-latest`
- **Type**: First open-source code agent for Lean 4
- **Pricing**: Free API endpoint

### Mistral NeMo
- **Model ID**: `mistral-nemo-latest`
- **Type**: State-of-the-art Mistral model trained specifically for code tasks
- **Pricing**:
  - Input: $0.15 per 1M tokens
  - Output: $0.15 per 1M tokens

## Ministral 3 Series (Edge Models)

### Ministral 3 - 3B
- **Model ID**: `ministral-3-3b-latest`
- **Type**: Best-in-class frontier AI to the edge
- **Pricing**:
  - Input: $0.10 per 1M tokens
  - Output: $0.10 per 1M tokens

### Ministral 3 - 8B
- **Model ID**: `ministral-3-8b-latest`
- **Type**: Best-in-class frontier AI to the edge
- **Pricing**:
  - Input: $0.15 per 1M tokens
  - Output: $0.15 per 1M tokens

### Ministral 3 - 14B
- **Model ID**: `ministral-3-14b-latest`
- **Type**: Best-in-class frontier AI to the edge
- **Pricing**:
  - Input: $0.20 per 1M tokens
  - Output: $0.20 per 1M tokens

## Legacy Models

### Mistral 7B
- **Model ID**: `mistral-7b-latest`
- **Type**: A 7B transformer model, fast-deployed and easily customisable
- **Pricing**:
  - Input: $0.25 per 1M tokens
  - Output: $0.25 per 1M tokens

## Mixtral Models (Sparse Mixture-of-Experts)

### Mixtral 8x7B
- **Model ID**: `mixtral-8x7b-latest`
- **Type**: A 7B sparse Mixture-of-Experts (SMoE). Uses 12.9B active parameters out of 45B total
- **Pricing**:
  - Input: $0.70 per 1M tokens
  - Output: $0.70 per 1M tokens

### Mixtral 8x22B
- **Model ID**: `mixtral-8x22b-latest`
- **Type**: Currently the most performant open model. Uses only 39B active parameters out of 141B
- **Pricing**:
  - Input: $2.00 per 1M tokens
  - Output: $6.00 per 1M tokens

## Reasoning Models (Magistral)

### Magistral Medium
- **Model ID**: `magistral-medium-latest`
- **Type**: Thinking model excelling in domain-specific, transparent, and multilingual reasoning
- **Pricing**:
  - Input: $2.00 per 1M tokens
  - Output: $5.00 per 1M tokens

### Magistral Small
- **Model ID**: `magistral-small-latest`
- **Type**: Thinking model excelling in domain-specific, transparent, and multilingual reasoning
- **Pricing**:
  - Input: $0.50 per 1M tokens
  - Output: $1.50 per 1M tokens

## Embedding Models

### Mistral Embed
- **Model ID**: `mistral-embed-latest`
- **Type**: State-of-the-art model for extracting representation of text extracts
- **Pricing**: $0.10 per 1M tokens (input only)

### Codestral Embed
- **Model ID**: `codestral-embed-latest`
- **Type**: State-of-the-art embedding model for code
- **Pricing**: $0.15 per 1M tokens (input only)

## Agent & Tool Models

### Agent API
- **Model ID**: `agent-api-latest`
- **Type**: Enhances AI with built-in tools for code execution, web search, image generation, persistent memory, and agentic orchestration
- **Pricing**: Model cost per M token + Tool call

## Moderation & Classification

### Mistral Moderation
- **Model ID**: `mistral-moderation-latest`
- **Type**: A classifier service for text content moderation
- **Pricing**: $0.10 per 1M tokens

### Classifier API Model 8B
- **Model ID**: `classifier-api-model-8b-latest`
- **Type**: Fine-tune Ministral 8B for classification tasks
- **Pricing**:
  - Input: $0.10 per 1M tokens
  - Output: $0.10 per 1M tokens

### Classifier API Model 3B
- **Model ID**: `classifier-api-model-3b-latest`
- **Type**: Fine-tune Ministral 3B for classification tasks
- **Pricing**:
  - Input: $0.04 per 1M tokens
  - Output: $0.04 per 1M tokens

## Default/Fallback

### Mistral Medium (Legacy)
- **Model ID**: `mistral-medium-latest`
- **Type**: Default fallback model
- **Pricing**:
  - Input: $2.70 per 1M tokens
  - Output: $8.10 per 1M tokens

## Implementation Notes

- All models are now available in the `calculate_cost_estimate()` function in `mistral_usage_tracker.py`
- The system automatically falls back to default pricing for unknown models
- Cost calculations are based on per-1M-token pricing
- The dashboard will automatically recognize and display usage for all these models
- Log files will be created with appropriate model names for tracking and analysis

## Total Models Configured: 31