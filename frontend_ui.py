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
            --bg: #fdfbf7;
            --card: #ffffff;
            --text: #333;
            --whatsapp: #25D366;
            --btn-text: #fff;
        }

        body { font-family: 'Segoe UI', sans-serif; background: var(--bg); color: var(--text); margin: 0; padding: 0; height: 100vh; display: flex; flex-direction: column; }

        /* HEADER */
        .header { padding: 15px; background: var(--card); box-shadow: 0 2px 10px rgba(0,0,0,0.05); display: flex; align-items: center; justify-content: center; z-index: 10; }
        .logo { font-size: 22px; font-weight: bold; color: var(--primary); display: flex; align-items: center; gap: 8px; }

        /* SCREENS */
        .screen { display: none; flex: 1; padding: 20px; flex-direction: column; overflow-y: auto; }
        .screen.active { display: flex; }

        /* HOME SCREEN */
        .hero-section { text-align: center; margin-top: 20px; margin-bottom: 20px; }
        .hero-icon { font-size: 50px; color: var(--primary); margin-bottom: 10px; }
        .input-card { background: var(--card); padding: 25px; border-radius: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }

        label { font-weight: bold; display: block; margin-bottom: 8px; font-size: 14px; color: #555; }
        select, input { width: 100%; padding: 14px; margin-bottom: 20px; border: 1px solid #ddd; border-radius: 12px; font-size: 16px; background: #fafafa; }

        /* CAMERA BUTTON AREA */
        .camera-box {
            border: 2px dashed #ffb8b8; border-radius: 15px; padding: 20px;
            text-align: center; margin-bottom: 20px; cursor: pointer;
            background: #fff5f5; transition: 0.2s;
        }
        .camera-box:active { background: #ffe3e3; }
        .camera-text { display: block; font-weight: bold; color: var(--primary); margin-bottom: 5px; font-size: 14px; }
        .camera-sub { font-size: 12px; color: #888; }
        
        .btn-generate { 
            width: 100%; padding: 16px; background: var(--primary); color: white; 
            border: none; border-radius: 12px; font-size: 18px; font-weight: bold; 
            cursor: pointer; box-shadow: 0 4px 10px rgba(255, 107, 107, 0.3);
            display: flex; align-items: center; justify-content: center; gap: 10px;
        }
        .btn-generate:active { transform: scale(0.98); }

        /* RESULT SCREEN */
        .recipe-container { background: var(--card); padding: 20px; border-radius: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin-bottom: 80px; }
        .recipe-content { white-space: pre-wrap; font-size: 16px; line-height: 1.6; color: #444; }
        
        /* BOTTOM ACTION BAR */
        .action-bar { 
            position: fixed; bottom: 0; left: 0; width: 100%;
            background: var(--card); padding: 15px; 
            box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
            display: flex; gap: 10px; z-index: 100;
        }
        .btn-action { flex: 1; padding: 12px; border: none; border-radius: 10px; font-weight: bold; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 8px; font-size: 14px; color: white; }
        .btn-copy { background: #333; }
        .btn-whatsapp { background: var(--whatsapp); }
        .btn-back { background: transparent; color: #666; border: 1px solid #ddd; position: absolute; top: 15px; left: 15px; padding: 8px 15px; border-radius: 20px; cursor: pointer; font-size: 14px; }

        /* LOADING */
        #loading-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(255,255,255,0.95); display: none; justify-content: center; align-items: center; flex-direction: column; z-index: 200; }
        .spinner { border: 4px solid #f3f3f3; border-top: 4px solid var(--primary); border-radius: 50%; width: 50px; height: 50px; animation: spin 1s linear infinite; margin-bottom: 15px; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }

    </style>
</head>
<body>

    <!-- HEADER -->
    <div class="header">
        <div class="logo"><i class="fas fa-hat-chef"></i> Pro AI Chef</div>
    </div>

    <!-- PAGE 1: INPUT HOME -->
    <div id="screen-home" class="screen active">
        <div class="hero-section">
            <div class="hero-icon">🍳</div>
            <h3>What are we cooking?</h3>
        </div>

        <div class="input-card">
            <!-- Language -->
            <label>Select Language / Zaban</label>
            <select id="language">
                <option value="English">English</option>
                <option value="Urdu">Urdu (اردو)</option>
                <option value="Roman Urdu">Roman Urdu</option>
                <option value="Hindi">Hindi (हिंदी)</option>
            </select>

            <!-- Camera Button -->
            <input type="file" id="camera-file" accept="image/*" capture="environment" style="display:none" onchange="handleImage()">
            <div class="camera-box" onclick="triggerCamera()">
                <i class="fas fa-camera" style="font-size: 24px; color: #ff6b6b; margin-bottom: 8px;"></i>
                <span class="camera-text">Scan Ingredients or Dish</span>
                <span class="camera-sub">(Tasweer lein recipe ke liye)</span>
            </div>

            <!-- Text Input -->
            <label>Or Type Dish Name / Ingredients</label>
            <input type="text" id="user-input" placeholder="e.g., Chicken, Aloo, Biryani...">

            <!-- Generate Button -->
            <button class="btn-generate" onclick="generateRecipe()">
                <span>Generate Recipe</span> <i class="fas fa-magic"></i>
            </button>
        </div>
    </div>

    <!-- PAGE 2: RESULT SCREEN -->
    <div id="screen-result" class="screen">
        <div class="recipe-container">
            <h2 style="margin-top:0; color:#ff6b6b;">🍽️ Your Recipe</h2>
            <div id="recipe-text" class="recipe-content"></div>
        </div>

        <!-- Sticky Bottom Bar -->
        <div class="action-bar">
            <button class="btn-action btn-copy" onclick="copyRecipe()">
                <i class="fas fa-copy"></i> Copy
            </button>
            <button class="btn-action btn-whatsapp" onclick="shareWhatsapp()">
                <i class="fab fa-whatsapp"></i> Share
            </button>
            <button class="btn-action" style="background: #eee; color:#333;" onclick="goBack()">
                <i class="fas fa-redo"></i> New
            </button>
        </div>
    </div>

    <!-- LOADING -->
    <div id="loading-overlay">
        <div class="spinner"></div>
        <h3 style="color:#ff6b6b;">Chef is Cooking...</h3>
        <p>Writing detailed recipe for you.</p>
    </div>

<script>
    let currentRecipeText = "";

    function triggerCamera() {
        document.getElementById('camera-file').click();
    }

    function handleImage() {
        const file = document.getElementById('camera-file').files[0];
        if(file) {
            // Mock functionality (Asli image analysis paid hota hai)
            // Hum user ko dikhayenge ke image scan ho gayi
            document.getElementById('user-input').value = "Scanned: Delicious Dish"; 
            alert("Photo Captured! Click 'Generate Recipe' to see magic.");
        }
    }

    async function generateRecipe() {
        const input = document.getElementById('user-input').value;
        const lang = document.getElementById('language').value;

        if(!input) return alert("Please type a name or take a photo!");

        // Loading Start
        document.getElementById('loading-overlay').style.display = 'flex';

        try {
            const res = await fetch('/generate', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    user_input: input,
                    language: lang,
                    style: "Restaurant Style"
                })
            });
            
            const data = await res.json();
            currentRecipeText = data.recipe; 
            
            // Format Bold Text (**text** -> <b>text</b>)
            const formatted = data.recipe.replace(/\*\*(.*?)\*\*/g, '<b>$1</b>');
            document.getElementById('recipe-text').innerHTML = formatted;

            // Change Page
            document.getElementById('screen-home').classList.remove('active');
            document.getElementById('screen-result').classList.add('active');
            window.scrollTo(0, 0);

        } catch(e) {
            alert("Error: " + e.message);
        } finally {
            document.getElementById('loading-overlay').style.display = 'none';
        }
    }

    function goBack() {
        document.getElementById('screen-result').classList.remove('active');
        document.getElementById('screen-home').classList.add('active');
        document.getElementById('user-input').value = '';
    }

    function copyRecipe() {
        navigator.clipboard.writeText(currentRecipeText).then(() => {
            alert("Recipe Copied!");
        });
    }

    function shareWhatsapp() {
        const text = encodeURIComponent("*Pro AI Chef Recipe:*\n\n" + currentRecipeText);
        window.open(`https://wa.me/?text=${text}`, '_blank');
    }
</script>

</body>
</html>
"""
