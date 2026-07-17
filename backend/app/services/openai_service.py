from functools import lru_cache

from openai import OpenAI

from app.core.config import settings


@lru_cache(maxsize=1)
def get_openai_client() -> OpenAI:
    api_key = settings.OPENAI_API_KEY.strip()

    if not api_key or api_key == "public-demo-disabled":
        raise RuntimeError(
            "AI execution is disabled. Configure OPENAI_API_KEY to enable it."
        )

    return OpenAI(api_key=api_key)


def ask_ai(prompt: str):
    client = get_openai_client()

    response = client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response.choices[0].message.content
