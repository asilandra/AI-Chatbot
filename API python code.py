from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv # <-- Import the new library

# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)

# Get the API key from the environment variable
API_KEY = os.getenv('OPENAI_API_KEY') # <-- Secure way to get the key

# Helper function to call the API
def call_chatbot_api(user_message):
    url = "https://api.openai.com/v1/chat/completions"  # OpenAI endpoint
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",  # Specify the model
        "messages": [{"role": "user", "content": user_message}],
        "max_tokens": 150,
        "temperature": 0.7,
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code}, {response.text}"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_message = request.form.get("message")
    if not user_message:
        return jsonify({"reply": "Please enter a message."})

    bot_reply = call_chatbot_api(user_message)
    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    app.run(debug=True)