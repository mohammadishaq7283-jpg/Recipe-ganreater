import os
from openai import OpenAI

# --- SETTINGS ---
BASE_URL = "https://openrouter.ai/api/v1"

# Aapka pasandida Model
MODEL_NAME = "stepfun/step-3.5-flash:free"

# --- PROMPT LOGIC (Safe Import) ---
try:
    from prompt_templates import create_master_prompt
except ImportError:
    # Agar prompt file missing ho to crash na ho, basic prompt banaye
    def create_master_prompt(lang, veg, style, type_):
        return f"Create a {style} recipe for {', '.join(veg)} in {lang}."

def generate_recipe(language, veggies_list, style, recipe_type):
    """
    Recipe generate karne wala main function.
    """
    
    # 1. API Key Check (Vercel Env se)
    api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("API_KEY")
    
    if not api_key:
        return "Error: API Key is missing in Vercel Settings (OPENROUTER_API_KEY)."

    # 2. Prompt Banana
    try:
        system_prompt = create_master_prompt(language, veggies_list, style, recipe_type)
    except Exception as e:
        return f"Error creating prompt: {str(e)}"

    print(f"Connecting to AI... Model: {MODEL_NAME}")

    # 3. AI ko Call karna
    try:
        client = OpenAI(
            base_url=BASE_URL,
            api_key=api_key,
        )

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system", 
                    "content": "You are a professional chef. Output strictly in the requested format."
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

        # 4. Jawab Return karna
        if response and response.choices:
            return response.choices[0].message.content
        else:
            return "Error: AI sent an empty response."

    except Exception as e:
        return f"AI Connection Error: {str(e)}"
