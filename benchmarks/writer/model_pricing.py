MODEL_PRICING = {
    "gpt-4.1-mini": {
        "input_per_million": 0.40,
        "output_per_million": 1.60,
    },
    "gpt-5-mini": {
        "input_per_million": 0.25,
        "output_per_million": 2.00,
    },
    "gpt-5.4-nano": {
        "input_per_million": 0.20,
        "output_per_million": 1.25,
    },
    "gpt-5.6-luna": {
        "input_per_million": 0.20,
        "output_per_million": 1.20,
    },
}


def calculate_cost(model, input_tokens, output_tokens):
    pricing = MODEL_PRICING.get(model)

    if pricing is None:
        return None

    input_cost = (
        input_tokens / 1_000_000
        * pricing["input_per_million"]
    )

    output_cost = (
        output_tokens / 1_000_000
        * pricing["output_per_million"]
    )

    return input_cost + output_cost