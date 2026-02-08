from openai import OpenAI
import os
from prompt_templates import create_master_prompt

# Config se settings lena (Agar config file hai)
# Agar config file nahi hai to hum direct ENV se le lenge safe side ke liye
try:
    from config import BASE_URL, MODEL_NAME
except ImportError:
    BASE_URL = "https://openrouter.ai/api/v1"
    MODEL_NAME = "google/gemini-2.0-flash-lite-preview-02-05:free"

def generate_recipe(language, veggies_list, style, recipe_type):
    """
    Yeh function OpenRouter AI ko call karta hai.
    """
    
    # 1. API Key Uthana (Vercel Environment se)
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    if not api_key:
        return "Error: API Key is missing in Vercel Settings!"

    # 2. Prompt create karna
    # Note: Make sure prompt_templates.py file bhi maujood ho!
    try:
        system_prompt = create_master_prompt(language, veggies_list, style, recipe_type)
    except NameError:
        return "Error: 'prompt_templates.py' file is missing or broken."

    print(f"Connecting to AI... Model: {MODEL_NAME}")
    
    try:
        # 3. Client Setup
        client = OpenAI(
            base_url=BASE_URL,
            api_key=api_key,
        )

        # 4. API Call
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a professional chef. Follow strict formatting rules."},
                {"role": "user", "content": system_prompt}
            ],
            extra_headers={
                "HTTP-Referer": "https://vercel.app",
                "X-Title": "Pro AI Chef App",
            },
        )

        # 5. Result nikalna
        recipe_text = response.choices[0].message.content
        return recipe_text

    except Exception as e:
        return f"AI Error: {str(e)}"
