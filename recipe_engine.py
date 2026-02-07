# recipe_engine.py# recipe_engine.py

import os
from openai import OpenAI

# --- PROMPT LOGIC ---
try:
    from prompt_templates import create_master_prompt
except ImportError:
    def create_master_prompt(language, veggies_list, style, recipe_type):
        return f"Generate a recipe for {', '.join(veggies_list)}."


# --- OPENROUTER SETTINGS ---
BASE_URL = "https://openrouter.ai/api/v1"

# ✅ WORKING FREE MODEL
MODEL_NAME = "google/gemini-2.0-flash-exp:free"


def generate_recipe(language, veggies_list, style, recipe_type):

    # 1. API KEY CHECK
    api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("API_KEY")

    if not api_key:
        return "Error: API Key missing in Vercel Settings (OPENROUTER_API_KEY)."

    # 2. PROMPT CREATE
    try:
        prompt = create_master_prompt(
            language,
            veggies_list,
            style,
            recipe_type
        )
    except Exception as e:
        return f"Prompt Error: {str(e)}"

    # 3. OPENROUTER CLIENT
    client = OpenAI(
        api_key=api_key,
        base_url=BASE_URL
    )

    # 4. AI CALL
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional chef. Format output clearly."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            extra_headers={
                "HTTP-Referer": "https://vercel.app",
                "X-Title": "Pro AI Chef"
            }
        )

        if response and response.choices:
            return response.choices[0].message.content.strip()

        return "Error: Empty response from AI."

    except Exception as e:
        return f"AI Error: {str(e)}"


