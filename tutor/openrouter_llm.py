try:
    from openrouter_api_key import OPENROUTER_API_KEY
except ImportError:
    OPENROUTER_API_KEY = None
from openai import OpenAI

def openrouter_llm(prompt: str, model: str = "openai/gpt-3.5-turbo") -> str:
    if not OPENROUTER_API_KEY or not isinstance(OPENROUTER_API_KEY, str):
        raise RuntimeError("OpenRouter API key is missing or not a string. Please check openrouter_api_key.py.")
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
    )
    completion = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        extra_headers={},
        extra_body={},
    )
    content = completion.choices[0].message.content
    return content.strip() if content else "Sorry, I couldn't process your input right now." 