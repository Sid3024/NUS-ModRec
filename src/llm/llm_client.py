from openai import OpenAI
from src.config.config import MyConfig

client = OpenAI()

def call_llm(messages: list[dict]) -> str:
    response = client.chat.completions.create(
        model=MyConfig.LLM_MODEL,
        messages=messages,
        temperature=MyConfig.LLM_TEMPERATURE
    )
    return response.choices[0].message.content
