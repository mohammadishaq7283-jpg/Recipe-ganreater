from flask import Flask, request, jsonify
import os
import sys

# --- FLASK APP SETUP ---
app = Flask(__name__)

# --- DEBUGGING WRAPPER ---
# Yeh check karega ke doosri files mein koi error to nahi
import_errors = ""

try:
    from validator import validate_veggies
except Exception as e:
    import_errors += f"Error importing validator.py: {str(e)}\n"

try:
    from recipe_engine import generate_recipe
except Exception as e:
    import_errors += f"Error importing recipe_engine.py: {str(e)}\n"

# --- ROUTES ---

@app.route('/', methods=['GET'])
def home():
    # Agar imports mein error aya, to wo screen par dikhaye ga
    if import_errors:
        return f"""
        <h1>⚠️ SYSTEM ERROR</h1>
        <p>App start nahi ho saki kyunki files mein error hai:</p>
        <pre style="background: #f8d7da; padding: 10px; color: #721c24;">{import_errors}</pre>
        <p>Please check your files.</p>
        """
    return """
    <h1>✅ Pro AI Chef is Running!</h1>
    <p>Status: All Systems Go.</p>
    <p>Send POST request to /generate</p>
    """

@app.route('/generate', methods=['POST'])
def generate():
    if import_errors:
        return jsonify({"error": "Server Configuration Error", "details": import_errors}), 500

    try:
        data = request.json
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        language = data.get('language', 'English')
        veggies_list = data.get('veggies', [])
        style = data.get('style', 'Home Style')
        recipe_type = data.get('type', 'Short')

        # Validation
        is_valid, message = validate_veggies(veggies_list)
        if not is_valid:
            return jsonify({"error": message}), 400

        # Generation
        recipe_text = generate_recipe(language, veggies_list, style, recipe_type)
        return jsonify({"recipe": recipe_text})

    except Exception as e:
        return jsonify({"error": f"Runtime Error: {str(e)}"}), 500

# Vercel Entry Point
if __name__ == '__main__':
    app.run()
