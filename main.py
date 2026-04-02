import os
from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Render Environment Variable ကနေ API Key ကို ဖတ်မယ်
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

@app.route('/')
def home():
    return "AI Assistant Server is Running!"

@app.route('/process', methods=['POST'])
def process_command():
    try:
        data = request.json
        user_input = data.get("text", "").lower()

        if not user_input:
            return jsonify({"command": "NONE", "error": "No input provided"})

        # AI ကို ခိုင်းမယ့် ညွှန်ကြားချက် (System Instruction)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        You are a smartphone automation expert. You understand Burmese and English perfectly.
        The user said: '{user_input}'
        
        Task: 
        1. Identify the app the user wants to open.
        2. Even if they speak in indirect Burmese (e.g., 'သီချင်းနားထောင်ချင်တယ်'), understand they want 'YouTube' or 'Spotify'.
        3. Return ONLY the Android package name.
        
        Common Package Names:
        - Facebook: com.facebook.katana
        - YouTube: com.google.android.youtube
        - Messenger: com.facebook.orca
        - TikTok: com.ss.android.ugc.trill
        - Telegram: org.telegram.messenger
        - Browser: com.android.chrome
        
        If no app is identified, return 'NONE'. 
        Response must be ONLY the package name.
        """

        response = model.generate_content(prompt)
        command = response.text.strip()

        return jsonify({"command": command})

    except Exception as e:
        return jsonify({"command": "NONE", "error": str(e)})

if __name__ == "__main__":
    # Render အတွက် Port 10000 ကို သုံးရပါမယ်
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
