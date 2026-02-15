import os
from openai import OpenAI
from prompt_templates import create_master_prompt

# --- CONFIG ---
BASE_URL = "https://openrouter.ai/api/v1"

# Wahi Model jo Recipe App me 100% working tha
MODEL_NAME = "stepfun/step-3.5-flash:free"

def generate_recipe(language, user_input, style="Home Style"):
    
    # 1. API KEY CHECK (More Robust)
    # Yeh pehle 'OPENROUTER_API_KEY' dhundega, agar wo na mili to 'API_KEY' dhundega
    api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("API_KEY")
    
    if not api_key:
        return "⚠️ Error: API Key is missing in Vercel Environment Variables. Please add 'OPENROUTER_API_KEY'."

    # 2. Prompt Creation
    system_prompt = create_master_prompt(language, user_input, style)

    try:
        client = OpenAI(base_url=BASE_URL, api_key=api_key)

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a Professional Chef. Write complete sentences."},
                {"role": "user", "content": system_prompt}
            ],
            max_tokens=1500,
            temperature=0.7,
            extra_headers={
                "HTTP-Referer": "https://vercel.app", 
                "X-Title": "Pro AI Chef",
            },
        )

        if response and response.choices:
            return response.choices[0].message.content
        else:
            return "⚠️ Chef is thinking... (No response)"

    except Exception as e:
        return f"Connection Error: {str(e)}"
