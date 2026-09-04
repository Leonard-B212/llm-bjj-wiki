# Implements OpenAI-specific LLM access for the provider-neutral LLM layer.
# All direct communication with the OpenAI SDK is kept inside this module.

from openai import OpenAI

from app.config import OPENAI_API_KEY


client = OpenAI(api_key=OPENAI_API_KEY)


# Creates a chat completion while only passing optional parameters when provided.
def create_chat_completion(model, messages, temperature=None):
    kwargs = {
        "model": model,
        "messages": messages,
    }

    if temperature is not None:
        kwargs["temperature"] = temperature

    return client.chat.completions.create(**kwargs)