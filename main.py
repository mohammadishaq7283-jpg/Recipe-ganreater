from flask import Flask, request, jsonify, render_template_string
from frontend_ui import HTML_CODE
from recipe_engine import generate_recipe

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string(HTML_CODE)

@app.route('/generate', methods=['POST'])
def generate_api():
    try:
        data = request.json
        user_input = data.get('user_input', '')
        language = data.get('language', 'English')
        style = data.get('style', 'Home Style')
        
        recipe_text = generate_recipe(language, user_input, style)
        return jsonify({"recipe": recipe_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()
