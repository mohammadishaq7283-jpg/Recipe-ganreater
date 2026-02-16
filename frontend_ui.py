HTML_CODE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Pro AI Chef</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --primary: #ff6b6b;
            --bg: #fffbf0;
            --card: #ffffff;
            --text: #333;
            --selected-border: #ff6b6b;
            --unselected-bg: #f9f9f9;
        }
        body { font-family: sans-serif; background: var(--bg); margin: 0; padding: 15px; display: flex; flex-direction: column; min-height: 100vh; }
        
        .header { text-align: center; margin-bottom: 15px; }
        .logo { font-size: 24px; font-weight: bold; color: var(--primary); }
        
        .card { background: var(--card); padding: 20px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); margin-bottom: 20px; }
        
        label { font-weight: bold; display: block; margin-bottom: 8px; font-size: 14px; color: #555; }
        select, input[type="text"] { width: 100%; padding: 12px; margin-bottom: 15px; border: 1px solid #ddd; border-radius: 10px; font-size: 16px; box-sizing: border-box; }
        
        /* --- NEW ICONS GRID (STYLE & LENGTH) --- */
        .options-grid { display: flex; gap: 10px; margin-bottom: 15px; }
        .opt-box { 
            flex: 1; padding: 10px; border: 2px solid #eee; border-radius: 10px; 
            text-align: center; cursor: pointer; background: var(--unselected-bg); transition: 0.2s;
            font-size: 13px; font-weight: bold; color: #555; display: flex; flex-direction: column; align-items: center; gap: 5px;
        }
        .opt-box i { font-size: 20px; margin-bottom: 2px; }
        
        /* SELECTED STATE */
        .opt-box.selected { border-color: var(--primary); background: #fff0f0; color: var(--primary); }

        /* CAMERA / GALLERY BUTTON */
        .camera-box {
            background: #ffe3e3; border: 2px dashed var(--primary); border-radius: 12px;
            padding: 15px; text-align: center; cursor: pointer; margin-bottom: 15px;
        }
        .camera-text { color: var(--primary); font-weight: bold; display: block; margin-top: 5px; font-size: 14px; }

        /* GENERATE BUTTON */
        .btn-generate {
            width: 100%; padding: 15px; background: var(--primary); color: white;
            border: none; border-radius: 10px; font-size: 18px; font-weight: bold; cursor: pointer;
        }
        
        /* RESULT SCREEN */
        #screen-result { display: none; }
        .recipe-content { white-space: pre-wrap; line-height: 1.6; color: #444; font-size: 15px; }
        
        .action-bar { display: flex; gap: 10px; margin-top: 20px; }
        .btn-action { flex: 1; padding: 12px; border: none; border-radius: 8px; font-weight: bold; color: white; cursor: pointer; font-size: 14px; display: flex; align-items: center; justify-content: center; gap: 5px;}
        .btn-copy { background: #333; }
        .btn-whatsapp { background: #25D366; }
        .btn-new { background: #ddd; color: #333; margin-bottom: 10px; width: 100%; display: flex; align-items: center; justify-content: center; gap: 5px; padding: 10px; border:none; border-radius:8px; font-weight:bold;}

        #loading { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(255,255,255,0.95); display: none; justify-content: center; align-items: center; flex-direction: column; z-index: 100; }
        .spinner { border: 4px solid #f3f3f3; border-top: 4px solid var(--primary); border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    </style>
</head>
<body>

    <div class="header">
        <div class="logo"><i class="fas fa-hat-chef"></i> Pro AI Chef</div>
    </div>

    <!-- PAGE 1: INPUT -->
    <div id="screen-home">
        <div class="card">
            
            <!-- Language -->
            <label>1. Select Language</label>
            <select id="language">
                <option value="English">English</option>
                <option value="Urdu">Urdu (اردو)</option>
                <option value="Roman Urdu">Roman Urdu</option>
                <option value="Hindi">Hindi</option>
            </select>

            <!-- Cooking Style (New) -->
            <label>2. Cooking Style</label>
            <div class="options-grid">
                <div class="opt-box selected" id="style-home" onclick="selectStyle('Home Style', 'style-home')">
                    <i class="fas fa-home"></i> Home Style
                </div>
                <div class="opt-box" id="style-rest" onclick="selectStyle('Restaurant Style', 'style-rest')">
                    <i class="fas fa-utensils"></i> Restaurant
                </div>
            </div>

            <!-- Recipe Length (New) -->
            <label>3. Recipe Length</label>
            <div class="options-grid">
                <div class="opt-box" id="type-short" onclick="selectType('Short', 'type-short')">
                    <i class="fas fa-bolt"></i> Short
                </div>
                <div class="opt-box selected" id="type-detail" onclick="selectType('Detailed', 'type-detail')">
                    <i class="fas fa-list-ol"></i> Detailed
                </div>
            </div>

            <!-- Image Input (Gallery Fixed) -->
            <label>4. Ingredients (Photo/Text)</label>
            
            <!-- Note: No 'capture' attribute to force OS picker -->
            <input type="file" id="camera-file" accept="image/*" style="display:none" onchange="handleImage()">
            
            <div class="camera-box" onclick="document.getElementById('camera-file').click()">
                <i class="fas fa-images" style="font-size: 28px; color: #ff6b6b;"></i>
                <span class="camera-text">Pick from Gallery / Camera</span>
            </div>

            <input type="text" id="user-input" placeholder="Or type ingredients here...">

            <button class="btn-generate" onclick="generateRecipe()">
                Generate Recipe <i class="fas fa-magic"></i>
            </button>
        </div>
    </div>

    <!-- PAGE 2: RESULT -->
    <div id="screen-result">
        <button class="btn-new" onclick="location.reload()">
            <i class="fas fa-arrow-left"></i> Make Another Recipe
        </button>
        
        <div class="card">
            <h2 style="margin-top:0; color:#ff6b6b;">🍽️ Recipe Ready</h2>
            <div id="recipe-text" class="recipe-content"></div>
        </div>

        <div class="action-bar">
            <button class="btn-action btn-copy" onclick="copyText()">
                <i class="fas fa-copy"></i> Copy
            </button>
            <button class="btn-action btn-whatsapp" onclick="shareWhatsapp()">
                <i class="fab fa-whatsapp"></i> Share
            </button>
        </div>
    </div>

    <div id="loading">
        <div class="spinner"></div>
        <p style="margin-top:10px; font-weight:bold;">Chef is cooking...</p>
    </div>

<script>
    let currentRecipe = "";
    
    // Default Values
    let selectedStyle = "Home Style";
    let selectedType = "Detailed";

    function selectStyle(val, id) {
        selectedStyle = val;
        document.getElementById('style-home').classList.remove('selected');
        document.getElementById('style-rest').classList.remove('selected');
        document.getElementById(id).classList.add('selected');
    }

    function selectType(val, id) {
        selectedType = val;
        document.getElementById('type-short').classList.remove('selected');
        document.getElementById('type-detail').classList.remove('selected');
        document.getElementById(id).classList.add('selected');
    }

    function handleImage() {
        const file = document.getElementById('camera-file').files[0];
        if(file) {
            document.getElementById('user-input').value = "Image: " + file.name;
            const camText = document.querySelector('.camera-text');
            camText.innerText = "✅ Image Selected!";
            camText.style.color = "green";
        }
    }

    async function generateRecipe() {
        const input = document.getElementById('user-input').value;
        const lang = document.getElementById('language').value;

        if(!input) {
            alert("Please upload a photo or type ingredients!");
            return;
        }

        document.getElementById('loading').style.display = 'flex';

        try {
            const res = await fetch('/generate', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    user_input: input,
                    language: lang,
                    style: selectedStyle, // Passing selected style
                    type: selectedType    // Passing selected length
                })
            });
            
            const data = await res.json();
            
            if(data.error) {
                alert("Error: " + data.error);
            } else {
                currentRecipe = data.recipe;
                document.getElementById('recipe-text').innerHTML = data.recipe.replace(/\*\*(.*?)\*\*/g, '<b>$1</b>');
                
                document.getElementById('screen-home').style.display = 'none';
                document.getElementById('screen-result').style.display = 'block';
                window.scrollTo(0, 0);
            }

        } catch(e) {
            alert("Network Error: " + e.message);
        } finally {
            document.getElementById('loading').style.display = 'none';
        }
    }

    function copyText() {
        navigator.clipboard.writeText(currentRecipe);
        alert("Copied!");
    }

    function shareWhatsapp() {
        const text = encodeURIComponent(currentRecipe);
        window.open(`https://wa.me/?text=${text}`, '_blank');
    }
</script>

</body>
</html>
"""
