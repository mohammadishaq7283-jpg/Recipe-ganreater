# recipe_engine.py

import os
from openai import OpenAI

# --- PROMPT TEMPLATE ---
try:
    from prompt_templates import create_master_prompt
except ImportError:
    # Backup agar file missing ho
    def create_master_prompt(language, veggies_list, style, recipe_type):
        return f"Generate a {style} recipe using {', '.join(veggies_list)} in {language}."


# --- OPENROUTER SETTINGS ---
BASE_URL = "https://openrouter.ai/api/v1"

# Free Model
MODEL_NAME = "google/gemini-2.0-flash-lite-preview-02-05:free"


def generate_recipe(language, veggies_list, style, recipe_type):
    """
    OpenRouter AI se recipe generate karta hai
    """

    # 1. API KEY CHECK
    api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("API_KEY")

    if not api_key:
        print("❌ API KEY NOT FOUND")
        return "Error: OPENROUTER_API_KEY missing in Vercel Environment Variables."

    print(f"✅ API Key OK | Model: {MODEL_NAME}")

    # 2. PROMPT BANANA
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
                    "content": "You are a professional chef AI. Follow clean formatting."
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
        print("❌ AI ERROR:", e)
        return f"AI Error: {str(e)}"
