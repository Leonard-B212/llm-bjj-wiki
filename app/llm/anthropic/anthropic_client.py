# Implements Anthropic-specific LLM access.
# Converts Anthropic responses into the shared completion format.

from types import SimpleNamespace

from anthropic import Anthropic

from app.config import ANTHROPIC_API_KEY


def create_chat_completion(model, messages, temperature=None):
    client = Anthropic(api_key=ANTHROPIC_API_KEY)

    system_messages = []
    conversation = []

    for message in messages:
        if message["role"] == "system":
            system_messages.append(message["content"])
        else:
            conversation.append(message)

    kwargs = {
        "model": model,
        "max_tokens": 8192,
        "messages": conversation,
    }

    if system_messages:
        kwargs["system"] = "\n\n".join(system_messages)

    if temperature is not None:
        kwargs["temperature"] = temperature

    response = client.messages.create(**kwargs)

    content = "".join(
        block.text
        for block in response.content
        if block.type == "text"
    )

    return SimpleNamespace(
        choices=[
            SimpleNamespace(
                message=SimpleNamespace(content=content)
            )
        ],
        usage=SimpleNamespace(
            prompt_tokens=response.usage.input_tokens,
            completion_tokens=response.usage.output_tokens,
            total_tokens=(
                response.usage.input_tokens
                + response.usage.output_tokens
            ),
        ),
    )