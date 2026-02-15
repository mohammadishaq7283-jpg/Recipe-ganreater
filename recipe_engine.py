import os
from openai import OpenAI
# Prompt file import kar rahe hain
try:
    from prompt_templates import create_master_prompt
except ImportError:
    def create_master_prompt(lang, inp, style): return f"Recipe for {inp} in {lang}"

# --- CONFIG ---
BASE_URL = "https://openrouter.ai/api/v1"

# Wahi model jo Recipe App ke liye best tha
MODEL_NAME = "stepfun/step-3.5-flash:free"

def generate_recipe(language, user_input, style="Home Style", recipe_type="Detailed"):
    
    api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("API_KEY")
    if not api_key:
        return "⚠️ Error: API Key missing in Vercel Settings!"

    # Prompt Banana
    system_prompt = create_master_prompt(language, user_input, style)

    try:
        client = OpenAI(base_url=BASE_URL, api_key=api_key)

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a Professional Chef. Write complete sentences."},
                {"role": "user", "content": system_prompt}
            ],
            # YAHAN CHANGE KIYA HAI:
            max_tokens=1500,  # Limit barha di taake recipe na katay
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
