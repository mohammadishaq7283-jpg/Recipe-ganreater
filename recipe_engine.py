import os
from openai import OpenAI
from prompt_templates import create_master_prompt

BASE_URL = "https://openrouter.ai/api/v1"
MODEL_NAME = "stepfun/step-3.5-flash:free"

def generate_recipe(language, user_input, style="Home Style"):
    api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("API_KEY")
    if not api_key: return "⚠️ API Key Missing"

    system_prompt = create_master_prompt(language, user_input, style)

    try:
        client = OpenAI(base_url=BASE_URL, api_key=api_key)
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a Chef. Write complete sentences."},
                {"role": "user", "content": system_prompt}
            ],
            max_tokens=1500,
            temperature=0.7,
            extra_headers={"HTTP-Referer": "https://vercel.app", "X-Title": "Pro AI Chef"},
        )
        if response and response.choices:
            return response.choices[0].message.content
        return "Chef is thinking... Try again."
    except Exception as e:
        return f"Error: {str(e)}"
