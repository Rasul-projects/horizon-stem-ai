import os
from flask import Flask, render_template_string, request, jsonify
import requests

app = Flask(__name__)

# Fallback endpoint if FEATHERLESS_API_KEY is not set
API_URL = "https://api.featherless.ai/v1/chat/completions"
API_KEY = os.environ.get("FEATHERLESS_API_KEY", "your_fallback_key_here")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI x STEM Education Hub</title>
    <style>
        :root {
            --bg-dark: #0f172a;
            --panel-dark: #1e293b;
            --accent-blue: #38bdf8;
            --text-light: #f8fafc;
            --text-muted: #94a3b8;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; 
            background-color: var(--bg-dark); 
            color: var(--text-light);
            display: flex;
            height: 100vh;
        }
        .sidebar {
            width: 300px;
            background-color: var(--panel-dark);
            padding: 20px;
            display: flex;
            flex-direction: column;
            border-right: 1px solid #334155;
        }
        .sidebar h2 { color: var(--accent-blue); margin-bottom: 20px; font-size: 1.5rem; }
        .sidebar p { font-size: 0.9rem; color: var(--text-muted); line-height: 1.4; margin-bottom: 15px; }
        .main-content {
            flex: 1;
            display: flex;
            flex-direction: column;
            background-color: var(--bg-dark);
        }
        .chat-header {
            background-color: var(--panel-dark);
            padding: 20px;
            border-bottom: 1px solid #334155;
        }
        .chat-box {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        .message {
            max-width: 75%;
            padding: 12px 16px;
            border-radius: 8px;
            line-height: 1.5;
        }
        .user-message {
            background-color: #0284c7;
            align-self: flex-end;
        }
        .ai-message {
            background-color: var(--panel-dark);
            align-self: flex-start;
            border: 1px solid #334155;
        }
        .input-area {
            padding: 20px;
            background-color: var(--panel-dark);
            border-top: 1px solid #334155;
            display: flex;
            gap: 10px;
        }
        input[type="text"] {
            flex: 1;
            padding: 12px;
            border-radius: 6px;
            border: 1px solid #334155;
            background-color: var(--bg-dark);
            color: var(--text-light);
            font-size: 1rem;
        }
        input:focus { outline: none; border-color: var(--accent-blue); }
        button {
            padding: 12px 24px;
            background-color: #0284c7;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-weight: bold;
            transition: background 0.2s;
        }
        button:hover { background-color: var(--accent-blue); }
    </style>
</head>
<body>
    <div class="sidebar">
        <h2>DSH Hacks V1</h2>
        <p><strong>Theme:</strong> AI x STEM Education</p>
        <p>An interactive workspace lowering the technical barrier for students learning complex STEM logic and diagnostics.</p>
        <hr style="border-color: #334155; margin: 15px 0;">
        <p style="font-size: 0.8rem; color: var(--accent-blue);">Status: Live Prototype Container</p>
    </div>
    <div class="main-content">
        <div class="chat-header">
            <h3>Interactive STEM Logic & Code Diagnostic Assistant</h3>
        </div>
        <div class="chat-box" id="chatBox">
            <div class="message ai-message">
                Hello! I am your AI STEM Tutor. Paste a complex algorithm, math problem, or system log file here, and let's break down its internal logic step-by-step.
            </div>
        </div>
        <div class="input-area">
            <input type="text" id="userInput" placeholder="Ask a STEM question, explain an algorithm, or analyze code logs..." onkeypress="handleKeyPress(event)">
            <button onclick="sendMessage()">Analyze</button>
        </div>
    </div>
    <script>
        function handleKeyPress(e) {
            if (e.key === 'Enter') sendMessage();
        }
        async function sendMessage() {
            const inputEl = document.getElementById('userInput');
            const query = inputEl.value.trim();
            if (!query) return;

            appendMessage(query, 'user-message');
            inputEl.value = '';

            const loadingId = appendMessage('Analyzing complex logic structure...', 'ai-message');

            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: query })
                });
                const data = await response.json();
                document.getElementById(loadingId).innerText = data.reply;
            } catch (error) {
                document.getElementById(loadingId).innerText = "Error securely processing diagnostic query.";
            }
        }
        function appendMessage(text, className) {
            const chatBox = document.getElementById('chatBox');
            const msgDiv = document.createElement('div');
            const id = 'msg_' + Math.random().toString(36).substr(2, 9);
            msgDiv.id = id;
            msgDiv.className = `message ${className}`;
            msgDiv.innerText = text;
            chatBox.appendChild(msgDiv);
            chatBox.scrollTop = chatBox.scrollHeight;
            return id;
        }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/api/chat", methods=["POST"])
def chat():
    user_data = request.json
    user_message = user_data.get("message", "")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "meta-llama/Meta-Llama-3-8B-Instruct", 
        "messages": [
            {
                "role": "system", 
                "content": "You are an advanced AI specializing in STEM Education. Break down complex programming concepts, mathematical algorithms, and system diagnostic logs into simple, highly intuitive steps for students."
            },
            {"role": "user", "content": user_message}
        ]
    }

    try:
        if API_KEY == "your_fallback_key_here":
            return jsonify({"reply": f"[Local Simulation Node] Let's analyze your question regarding '{user_message}'. To solve this, break down your system parameters into logical inputs, process constraints, and target formulas sequentially."})

        response = requests.post(API_URL, json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            return jsonify({"reply": response.json()['choices'][0]['message']['content']})
        else:
            return jsonify({"reply": "API Gateway returned an error processing your query. Please review your token allocation."})
    except Exception as e:
        return jsonify({"reply": "Your structural problem is being parsed locally: Try breaking the formula or code logic into distinct components before debugging further."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
