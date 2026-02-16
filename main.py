from flask import Flask, request, jsonify, render_template_string
from frontend_ui import HTML_CODE

try:
    from recipe_engine import generate_recipe
except ImportError:
    def generate_recipe(lang, inp, style): return "Error: Backend file missing."

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string(HTML_CODE)

@app.route('/generate', methods=['POST'])
def generate_api():
    try:
        data = request.json
        
        # Inputs from Frontend
        user_input = data.get('user_input', '')
        language = data.get('language', 'English')
        style = data.get('style', 'Home Style')
        # Note: Recipe Length logic prompt me handle hogi
        # Hum style variable me hi thoda modification bhej denge prompt ke liye
        full_style = f"{style} ({data.get('type', 'Detailed')} Version)"
        
        # Call AI
        recipe_text = generate_recipe(language, user_input, full_style)
        
        return jsonify({"recipe": recipe_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()
