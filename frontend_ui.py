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
            --bg-color: #ffffff;
            --text-color: #333333;
            --sidebar-bg: #f8f9fa;
            --card-bg: #ffffff;
            --input-bg: #f0f2f5;
            --border-color: #e0e0e0;
            --primary-color: #ff6b6b; /* Chef Red/Orange */
            --chat-user: #ff6b6b;
            --chat-ai: #f1f3f4;
            --chat-ai-text: #333;
        }

        [data-theme="dark"] {
            --bg-color: #121212;
            --text-color: #e0e0e0;
            --sidebar-bg: #1a1a1a;
            --card-bg: #1e1e1e;
            --input-bg: #2d2d2d;
            --border-color: #444;
            --primary-color: #ff8787;
            --chat-user: #ff8787;
            --chat-ai: #333333;
            --chat-ai-text: #fff;
        }

        * { box-sizing: border-box; }
        body { font-family: 'Segoe UI', sans-serif; background-color: var(--bg-color); color: var(--text-color); margin: 0; padding: 0; width: 100%; height: 100vh; overflow: hidden; }
        
        .app-container { display: flex; flex-direction: column; height: 100%; width: 100%; }

        /* HEADER */
        .header {
            flex-shrink: 0; height: 60px; padding: 0 15px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border-color); background: var(--bg-color); z-index: 10;
        }
        .title { font-weight: bold; font-size: 20px; color: var(--primary-color); display:flex; align-items:center; gap:5px;}
        .menu-btn { background: none; border: none; font-size: 20px; cursor: pointer; color: var(--text-color); }

        /* CONTENT AREA */
        .content-area { flex: 1; position: relative; overflow: hidden; display: flex; flex-direction: column; }
        .screen { display: none; width: 100%; height: 100%; overflow-y: auto; padding: 20px; }
        .screen.active { display: block; }

        /* DASHBOARD SPECIFIC */
        #screen-dashboard {
            display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; height: 100%; padding-bottom: 80px;
        }
        
        .lang-select-container { margin-bottom: 20px; width: 100%; max-width: 300px; }
        .lang-select { 
            width: 100%; padding: 15px; font-size: 16px; border-radius: 12px; 
            border: 2px solid var(--primary-color); background: var(--card-bg); color: var(--text-color); font-weight: bold;
        }

        .hero-image { font-size: 60px; margin-bottom: 20px; color: var(--primary-color); }
        .instruction-text { font-size: 18px; line-height: 1.5; margin-bottom: 30px; max-width: 80%; }

        /* CHAT SCREEN */
        #screen-chat { display: none; flex-direction: column; padding: 0; height: 100%; }
        #screen-chat.active { display: flex; }
        .chat-header-bar { flex-shrink: 0; padding: 10px; background: var(--card-bg); border-bottom: 1px solid var(--border-color); display: flex; align-items: center; justify-content: space-between; }
        #chat-history { flex: 1; overflow-y: auto; padding: 15px; display: flex; flex-direction: column; gap: 15px; padding-bottom: 80px; }

        /* INPUT BAR (FIXED BOTTOM) */
        .chat-input-area {
            position: fixed; bottom: 0; left: 0; width: 100%; height: 70px;
            background: var(--bg-color); border-top: 1px solid var(--border-color);
            display: flex; align-items: center; gap: 10px; padding: 0 10px; z-index: 100;
        }
        .input-wrapper { flex: 1; position: relative; display: flex; align-items: center; background: var(--input-bg); border-radius: 30px; border: 1px solid var(--border-color); padding: 0 15px; }
        .chat-input-area input { width: 100%; padding: 12px; padding-right: 40px; border: none; background: transparent; color: var(--text-color); outline: none; font-size: 16px; }
        
        .camera-btn { position: absolute; right: 10px; background: none; border: none; color: var(--primary-color); font-size: 22px; cursor: pointer; padding: 5px; }
        .send-btn { width: 45px; height: 45px; background: var(--primary-color); color: white; border: none; border-radius: 50%; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 18px; flex-shrink: 0; }

        /* MESSAGES */
        .message { padding: 12px 18px; border-radius: 18px; max-width: 85%; line-height: 1.5; font-size: 15px; }
        .user-msg { align-self: flex-end; background: var(--chat-user); color: white; border-bottom-right-radius: 4px; }
        .ai-msg { align-self: flex-start; background: var(--chat-ai); color: var(--chat-ai-text); border-bottom-left-radius: 4px; }

        /* LOADING */
        #loading-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); display: none; justify-content: center; align-items: center; flex-direction: column; z-index: 2000; color: white; }
        .spinner { border: 4px solid #f3f3f3; border-top: 4px solid var(--primary-color); border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite; margin-bottom: 10px; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }

    </style>
</head>
<body>

<div class="app-container">
    <!-- HEADER -->
    <div class="header">
        <div class="title"><i class="fas fa-utensils"></i> Pro AI Chef</div>
        <button class="menu-btn" onclick="toggleTheme()"><i class="fas fa-adjust"></i></button>
    </div>

    <div class="content-area">
        
        <!-- DASHBOARD (MAIN SCREEN) -->
        <div id="screen-dashboard" class="screen active">
            
            <div class="hero-image"><i class="fas fa-carrot"></i></div>
            
            <!-- 1. LANGUAGE SELECTION -->
            <div class="lang-select-container">
                <select id="main-lang-select" class="lang-select" onchange="updateLanguage()">
                    <option value="English">English</option>
                    <option value="Urdu">Urdu (اردو)</option>
                    <option value="Hindi">Hindi (हिंदी)</option>
                    <option value="Roman Urdu">Roman Urdu</option>
                </select>
            </div>

            <!-- 2. DYNAMIC TEXT -->
            <div id="instruction-text" class="instruction-text">
                Use the camera to scan ingredients or type a dish name to get a recipe!
            </div>

        </div>

        <!-- CHAT SCREEN -->
        <div id="screen-chat" class="screen">
            <div class="chat-header-bar">
                <button onclick="showDashboard()" style="background:none; border:none; font-size:18px; color: var(--text-color);"><i class="fas fa-arrow-left"></i> Back</button>
                <b id="chat-title">Recipe Chat</b>
            </div>
            <div id="chat-history"></div>
        </div>

    </div>
</div>

<!-- FIXED BOTTOM INPUT BAR -->
<div class="chat-input-area">
    <input type="file" id="camera-input" accept="image/*" capture="environment" style="display: none;" onchange="handleImageSelect()">
    
    <div class="input-wrapper">
        <input type="text" id="user-input" placeholder="Type ingredient or dish name..." onkeypress="if(event.key==='Enter') sendMessage()">
        <!-- CAMERA ICON INSIDE BAR -->
        <button class="camera-btn" onclick="triggerCamera()"><i class="fas fa-camera"></i></button>
    </div>
    
    <button class="send-btn" onclick="sendMessage()"><i class="fas fa-paper-plane"></i></button>
</div>

<div id="loading-overlay"><div class="spinner"></div><div id="loading-text">Cooking...</div></div>

<script>
    // --- TRANSLATIONS ---
    const translations = {
        "English": {
            text: "Use the camera to scan ingredients or type a dish name to get a recipe!",
            placeholder: "Type ingredient or dish name..."
        },
        "Urdu": {
            text: "Apne ingredients ki tasweer lein ya dish ka naam likh kar recipe hasil karein!",
            placeholder: "Dish ya sabzi ka naam likhein..."
        },
        "Hindi": {
            text: "Samagri ki photo lein ya dish ka naam likhkar recipe payein!",
            placeholder: "Dish ka naam likhein..."
        },
        "Roman Urdu": {
            text: "Camera se tasweer lein ya dish ka naam likhein recipe ke liye!",
            placeholder: "Yahan likhein..."
        }
    };

    let currentLang = "English";

    document.addEventListener("DOMContentLoaded", () => {
        const theme = localStorage.getItem('theme') || 'light';
        document.body.setAttribute('data-theme', theme);
        updateLanguage();
    });

    // --- LOGIC ---
    function updateLanguage() {
        const select = document.getElementById('main-lang-select');
        currentLang = select.value;
        const data = translations[currentLang] || translations["English"];
        
        // Update Text
        document.getElementById('instruction-text').innerText = data.text;
        document.getElementById('user-input').placeholder = data.placeholder;
    }

    function showDashboard() {
        document.getElementById('screen-chat').classList.remove('active');
        document.getElementById('screen-dashboard').classList.add('active');
    }

    function triggerCamera() {
        document.getElementById('camera-input').click();
    }

    function handleImageSelect() {
        // Mock Image Analysis
        const fileInput = document.getElementById('camera-input');
        if (fileInput.files && fileInput.files[0]) {
            const fileName = fileInput.files[0].name;
            // Fake analysis message
            const input = document.getElementById('user-input');
            input.value = "Analyzed Image: Mixed Vegetables"; // Auto-fill for demo
            sendMessage();
        }
    }

    async function sendMessage() {
        const input = document.getElementById('user-input');
        const text = input.value.trim();
        if(!text) return;

        // Switch to Chat Screen if not active
        document.getElementById('screen-dashboard').classList.remove('active');
        document.getElementById('screen-chat').classList.add('active');

        addMessage(text, 'user-msg');
        input.value = '';
        
        const loadingId = addMessage("👨‍🍳 Chef is thinking...", 'ai-msg');
        
        // Timeout Safety
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 15000);

        try {
            const res = await fetch('/api/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ 
                    message: text, 
                    subject: "Cooking", // Force subject
                    language: currentLang 
                }),
                signal: controller.signal
            });
            clearTimeout(timeoutId);
            const data = await res.json();
            document.getElementById(loadingId).innerHTML = formatRecipe(data.reply);
        } catch(e) {
            document.getElementById(loadingId).innerText = "⚠️ Network Error. Try again.";
        }
    }

    function addMessage(text, cls) {
        const d = document.createElement('div');
        d.className = 'message ' + cls;
        d.innerHTML = text;
        const h = document.getElementById('chat-history');
        h.appendChild(d);
        h.scrollTop = h.scrollHeight;
        return d.id;
    }

    function formatRecipe(text) {
        // Simple formatter to make bold text look good
        return text.replace(/\*\*(.*?)\*\*/g, '<b>$1</b>').replace(/\n/g, '<br>');
    }

    function toggleTheme() {
        const body = document.body;
        const newTheme = body.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
        body.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
    }
</script>

</body>
</html>
"""
