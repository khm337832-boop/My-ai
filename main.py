import os
from flask import Flask, request, jsonify
import g4f # API Key မလိုတဲ့ library

app = Flask(__name__)

@app.route('/')
def home():
    return "Free AI Assistant is Running!"

@app.route('/process', methods=['POST'])
def process_command():
    try:
        data = request.json
        user_input = data.get("text", "").lower()

        # AI ကို ခိုင်းမယ့် ညွှန်ကြားချက်
        prompt = f"Identify the android app to open for: '{user_input}'. Return ONLY package name (e.g. com.facebook.katana). If none, return NONE."

        # Free AI model တစ်ခုခုကို သုံးပြီး အဖြေတောင်းမယ်
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_35_turbo,
            messages=[{"role": "user", "content": prompt}],
        )
        
        command = response.strip()
        return jsonify({"command": command})

    except Exception as e:
        return jsonify({"command": "NONE", "error": str(e)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
