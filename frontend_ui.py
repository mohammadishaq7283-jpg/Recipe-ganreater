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
        }
        body { font-family: sans-serif; background: var(--bg); margin: 0; padding: 20px; display: flex; flex-direction: column; height: 100vh; }
        
        .header { text-align: center; margin-bottom: 20px; }
        .logo { font-size: 24px; font-weight: bold; color: var(--primary); }
        
        .card { background: var(--card); padding: 20px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); margin-bottom: 20px; }
        
        select, input { width: 100%; padding: 15px; margin-bottom: 15px; border: 1px solid #ddd; border-radius: 10px; font-size: 16px; box-sizing: border-box; }
        
        /* CAMERA / GALLERY BUTTON */
        .camera-box {
            background: #ffe3e3; border: 2px dashed var(--primary); border-radius: 12px;
            padding: 20px; text-align: center; cursor: pointer; margin-bottom: 20px;
        }
        .camera-text { color: var(--primary); font-weight: bold; display: block; margin-top: 5px; }

        .btn-generate {
            width: 100%; padding: 15px; background: var(--primary); color: white;
            border: none; border-radius: 10px; font-size: 18px; font-weight: bold; cursor: pointer;
        }
        .btn-generate:active { transform: scale(0.98); }

        #screen-result { display: none; }
        .recipe-content { white-space: pre-wrap; line-height: 1.6; color: #444; font-size: 16px; }
        
        .action-bar { display: flex; gap: 10px; margin-top: 20px; }
        .btn-action { flex: 1; padding: 12px; border: none; border-radius: 8px; font-weight: bold; color: white; cursor: pointer; }
        .btn-copy { background: #333; }
        .btn-whatsapp { background: #25D366; }
        .btn-new { background: #ddd; color: #333; margin-bottom: 10px; width: 100%; }

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
            <label><b>1. Select Language</b></label>
            <select id="language">
                <option value="English">English</option>
                <option value="Urdu">Urdu (اردو)</option>
                <option value="Roman Urdu">Roman Urdu</option>
                <option value="Hindi">Hindi</option>
            </select>

            <label><b>2. Add Ingredients</b></label>
            
            <!-- 
               NOTE: Yahan se 'capture' attribute hata diya hai.
               Ab yeh Gallery aur Camera dono khol sakega.
            -->
            <input type="file" id="camera-file" accept="image/*" style="display:none" onchange="handleImage()">
            
            <div class="camera-box" onclick="document.getElementById('camera-file').click()">
                <i class="fas fa-camera" style="font-size: 30px; color: #ff6b6b;"></i>
                <span class="camera-text">Upload from Gallery / Camera</span>
            </div>

            <input type="text" id="user-input" placeholder="Or type here (e.g. Chicken, Aloo)...">

            <button class="btn-generate" onclick="generateRecipe()">
                Generate Recipe <i class="fas fa-magic"></i>
            </button>
        </div>
    </div>

    <!-- PAGE 2: RESULT -->
    <div id="screen-result">
        <button class="btn-action btn-new" onclick="location.reload()">
            <i class="fas fa-arrow-left"></i> Make New Recipe
        </button>
        
        <div class="card">
            <h2 style="margin-top:0; color:#ff6b6b;">🍽️ Your Recipe</h2>
            <div id="recipe-text" class="recipe-content"></div>
        </div>

        <div class="action-bar">
            <button class="btn-action btn-copy" onclick="copyText()">Copy</button>
            <button class="btn-action btn-whatsapp" onclick="shareWhatsapp()">WhatsApp</button>
        </div>
    </div>

    <div id="loading">
        <div class="spinner"></div>
        <p style="margin-top:10px; font-weight:bold;">Chef is cooking...</p>
    </div>

<script>
    let currentRecipe = "";

    function handleImage() {
        const file = document.getElementById('camera-file').files[0];
        if(file) {
            // Image select hone par input box me naam likh denge
            document.getElementById('user-input').value = "Image Selected: " + file.name;
            // User ko visual confirmation
            const camText = document.querySelector('.camera-text');
            camText.innerText = "✅ Image Selected!";
            camText.style.color = "green";
        }
    }

    async function generateRecipe() {
        const input = document.getElementById('user-input').value;
        const lang = document.getElementById('language').value;

        if(!input) {
            alert("Please select an image or type a name!");
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
                    style: "Home Style"
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
