import httpx
import os

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
#MODEL = "mistralai/mistral-7b-instruct:free"  # Or 
MODEL= "deepseek/deepseek-r1-distill-llama-70b:free"

SYSTEM_PROMPT = {
    "role": "system",
    "content": "You are a helpful, accurate educator tutor."
}

async def chat_with_model(user_messages: list[dict]):
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [SYSTEM_PROMPT] + user_messages,
        "temperature": 0.7,
        "max_tokens": 1000
    }

    timeout = httpx.Timeout(60.0)  # ⏱️ increase to 60 seconds

    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.post(OPENROUTER_URL, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
