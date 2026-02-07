from flask import Flask, request, jsonify, render_template_string
import os
import sys

# --- CONFIG ---
app = Flask(__name__)

# --- DEBUG CHECKS ---
import_errors = ""
try:
    from validator import validate_veggies
except ImportError:
    import_errors += "Validator file missing. "

try:
    from recipe_engine import generate_recipe
except ImportError:
    import_errors += "Recipe Engine file missing. "

# --- FRONTEND UI (HTML/CSS/JS) ---
HTML_UI = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pro AI Chef</title>
    <style>
        body { font-family: sans-serif; background: #f4f4f9; padding: 20px; max-width: 600px; margin: 0 auto; }
        .card { background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; text-align: center; }
        label { font-weight: bold; display: block; margin-top: 15px; }
        input, select, button { width: 100%; padding: 12px; margin-top: 8px; border: 1px solid #ddd; border-radius: 8px; box-sizing: border-box; }
        button { background: #27ae60; color: white; font-size: 16px; border: none; cursor: pointer; font-weight: bold; }
        button:hover { background: #219150; }
        button:disabled { background: #ccc; }

        #veggie-list { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px; }
        .tag { background: #e8f5e9; color: #2e7d32; padding: 5px 10px; border-radius: 15px; font-size: 14px; display: flex; align-items: center; }
        .tag span { margin-left: 8px; cursor: pointer; font-weight: bold; color: #c62828; }

        #result-area { margin-top: 20px; white-space: pre-wrap; background: #fff3e0; padding: 15px; border-radius: 8px; display: none; border-left: 5px solid #ff9800; }
        .loader { text-align: center; display: none; margin-top: 10px; }
    </style>
</head>
<body>

<div class="card">
    <h1>👨‍🍳 Pro AI Chef</h1>

    <label>Select Language:</label>
    <select id="language">
        <option value="English">English</option>
        <option value="Hindi">Hindi (हिंदी)</option>
        <option value="Urdu">Urdu (اردو)</option>
        <option value="Roman Urdu">Roman Urdu</option>
    </select>

    <label>Add Vegetables:</label>
    <div style="display: flex; gap: 5px;">
        <input type="text" id="veg-input" placeholder="e.g. Potato">
        <button onclick="addVeg()" style="width:auto;">+</button>
    </div>
    <div id="veggie-list"></div>

    <label>Cooking Style:</label>
    <select id="style">
        <option value="Home Style">Home Style</option>
        <option value="Restaurant Style">Restaurant Style</option>
    </select>

    <label>Recipe Type:</label>
    <select id="type">
        <option value="Short">Short</option>
        <option value="Detailed">Detailed</option>
    </select>

    <button onclick="generateRecipe()" id="gen-btn" style="margin-top:20px;">Generate Recipe 🍳</button>

    <div class="loader" id="loader">Processing...</div>
    <div id="result-area"></div>
</div>

<script>
let veggies = [];

function addVeg() {
    const input = document.getElementById('veg-input');
    const val = input.value.trim();
    if (val) {
        veggies.push(val);
        renderVeggies();
        input.value = '';
    }
}

function removeVeg(index) {
    veggies.splice(index, 1);
    renderVeggies();
}

function renderVeggies() {
    const list = document.getElementById('veggie-list');
    list.innerHTML = veggies.map((v,i) =>
        `<div class="tag">${v} <span onclick="removeVeg(${i})">×</span></div>`
    ).join('');
}

async function generateRecipe() {
    if (veggies.length === 0) {
        alert("Please add at least one vegetable!");
        return;
    }

    const btn = document.getElementById('gen-btn');
    const loader = document.getElementById('loader');
    const result = document.getElementById('result-area');

    btn.disabled = true;
    loader.style.display = 'block';
    result.style.display = 'none';

    const data = {
        language: document.getElementById('language').value,
        veggies: veggies,
        style: document.getElementById('style').value,
        type: document.getElementById('type').value
    };

    try {
        const res = await fetch('/generate', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        const json = await res.json();
        result.innerText = json.recipe || json.error;
    } catch (e) {
        result.innerText = "Network Error";
    }

    loader.style.display = 'none';
    btn.disabled = false;
    result.style.display = 'block';
}
</script>

</body>
</html>
"""

# --- ROUTES ---
@app.route("/", methods=["GET"])
def home():
    if import_errors:
        return f"<h1>System Error</h1><p>{import_errors}</p>"
    return render_template_string(HTML_UI)

@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.json
        recipe_text = generate_recipe(
            data.get("language"),
            data.get("veggies"),
            data.get("style"),
            data.get("type")
        )
        return jsonify({"recipe": recipe_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()
