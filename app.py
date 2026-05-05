from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os # 👈 추가: 시스템 기능을 쓰는 도구
from dotenv import load_dotenv # 👈 추가: .env 파일을 읽는 도구

# .env 파일에 적힌 비밀번호를 읽어와라!
load_dotenv() 

app = Flask(__name__)
CORS(app) 

# 🚨 이제 키를 직접 적지 않고, 금고(.env)에서 꺼내오라고 시켜!
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

# --- 이하 코드는 아까랑 똑같아! ---
my_model_name = 'gemini-1.5-flash'
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        if 'gemini' in m.name:
            my_model_name = m.name.replace('models/', '')
            break
                
print(f"✅ AI 사서 로딩 완료! (사용 모델: {my_model_name})")
model = genai.GenerativeModel(my_model_name)

@app.route('/api/recommend', methods=['POST'])
def recommend_book():
    data = request.json
    user_message = data.get('message')
    if not user_message:
        return jsonify({'error': '질문이 없습니다.'}), 400

    prompt = f"""너는 '나만의 독서 아카이브' 웹사이트의 친절하고 전문적인 AI 사서야.
    사용자의 요청: "{user_message}"
    이 요청에 맞춰서 읽기 좋은 책 1~2권을 추천해주고, 추천하는 이유도 다정하게 설명해줘."""

    try:
        response = model.generate_content(prompt)
        return jsonify({'reply': response.text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)