from flask import Flask, request, jsonify
from flask_cors import CORS
from sparkai.llm.llm import ChatSparkLLM
from sparkai.core.messages import ChatMessage
from memory.Memory import load_memory, search_memory, classify_topic
from api.API import (
    SPARKAI_URL,
    SPARKAI_APP_ID,
    SPARKAI_API_KEY,
    SPARKAI_API_SECRET,
    SPARKAI_DOMAIN
)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

# 初始化模型
spark = ChatSparkLLM(
    spark_api_url=SPARKAI_URL,
    spark_app_id=SPARKAI_APP_ID,
    spark_api_key=SPARKAI_API_KEY,
    spark_api_secret=SPARKAI_API_SECRET,
    spark_llm_domain=SPARKAI_DOMAIN,
    streaming=False,
    spark_llm_params={
        "max_tokens": 50,
        "temperature": 0.3
    }
)

memory_data = load_memory()

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    question = data.get("message", "")

    if not question.strip():
        return jsonify({"reply": "我没有收到有效问题。"})

    topic = classify_topic(question)
    answer = search_memory(question, memory_data, topic=topic)

    if answer:
        return jsonify({"reply": answer})

    messages = [ChatMessage(role="user", content=question)]
    response = spark.generate([messages])
    ai_reply = response.generations[0][0].text

    return jsonify({"reply": ai_reply})

if __name__ == '__main__':
    app.run(port=5000, debug=True)