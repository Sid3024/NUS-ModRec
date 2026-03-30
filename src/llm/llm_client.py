from openai import OpenAI
from src.config.config import MyConfig

client = OpenAI()

def call_llm(messages: list[dict]) -> str:
    response = client.chat.completions.create(
        model=MyConfig.LLM_MODEL,
        messages=messages,
        temperature=MyConfig.LLM_TEMPERATURE
    )
    raw_out = response.choices[0].message.content
    return clean_llm_response(raw_out)

def clean_llm_response(response: str) -> str:
    response = response.strip()

    if response.startswith("```"):
        lines = response.splitlines()

        # remove first fence line
        lines = lines[1:]

        # remove last fence line if present
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        response = "\n".join(lines).strip()

    return response
