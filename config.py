import os

# Vercel Environment Variable se key uthayega
# Vercel dashboard me "OPENROUTER_API_KEY" ke naam se variable add karna
API_KEY = os.getenv("OPENROUTER_API_KEY")

# Agar key na mile to warning (Error handling engine me hoga)
if not API_KEY:
    print("Warning: API Key not found in Environment Variables.")

# OpenRouter Settings
BASE_URL = "https://openrouter.ai/api/v1"
MODEL_NAME = "google/gemini-2.0-flash-lite-preview-02-05:free"  # Ya jo bhi model aap chahein

# App Meta
APP_NAME = "Pro AI Chef"
