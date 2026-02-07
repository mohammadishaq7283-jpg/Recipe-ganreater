# recipe_engine.py#import os
from openai import OpenAI

# Prompt banane wali file
try:
    from prompt_templates import create_master_prompt
except ImportError:
    def create_master_prompt(lang, veg, style, type_):
        veg_str = ", ".join(veg or [])
        return f"Generate a {style} recipe in {lang} using: {veg_str}"

# OpenRouter base URL
BASE_URL = "https://openrouter.ai/api/v1"

# Model ka naam ENV se lo, warna default LLaMA free model use karo
DEFAULT_MODEL = "meta-llama/llama-3.1-8b-instruct:free"
MODEL_NAME = os.getenv("OPENROUTER_MODEL", DEFAULT_MODEL)

def generate_recipe(language, veggies_list, style, recipe_type):
    # 1) API KEY CHECK
    api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("API_KEY")
    if not api_key:
        return "Error: OPENROUTER_API_KEY Vercel env me set nahi hai."

    # 2) PROMPT banaao
    try:
        system_prompt = create_master_prompt(language, veggies_list, style, recipe_type)
    except Exception as e:
        return f"Error creating prompt: {e}"

    # 3) CLIENT banao
    client = OpenAI(
        base_url=BASE_URL,
        api_key=api_key,
    )

    # 4) CALL MODEL
    try:
        print(f"Using model: {MODEL_NAME}")  # Logs me dikhega

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": "You are Pro AI Chef. Follow the requested format exactly."
                },
                {
                    "role": "user",
                    "content": system_prompt
                }
            ],
            extra_headers={
                "HTTP-Referer": "https://vercel.app",
                "X-Title": "Pro AI Chef",
            },
        )

        if not response or not response.choices:
            return "Error: Empty response from AI."

        return response.choices[0].message.content

    except Exception as e:
        # Model ka naam bhi error ke sath dikhao
        return f"AI Error (model={MODEL_NAME}): {e}" recipe_engine.py


