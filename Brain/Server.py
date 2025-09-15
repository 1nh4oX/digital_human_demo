# 从api文件夹里获取信息，设置端口与前端通讯
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
PORT=5200
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": f"http://localhost:{PORT}"}})

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

# @app.route("/chat", methods=["POST"])
# def chat():
#     data = request.get_json()
#     question = data.get("message", "")

#     if not question.strip():
#         return jsonify({"reply": "我没有收到有效问题。"})

#     topic = classify_topic(question)
#     answer = search_memory(question, memory_data, topic=topic)

#     if answer:
#         return jsonify({"reply": answer})

#     messages = [ChatMessage(role="user", content=question)]
#     response = spark.generate([messages])
#     ai_reply = response.generations[0][0].text

#     return jsonify({"reply": ai_reply})

# @app.route("/chat", methods=["POST"])
# def chat():
#     data = request.get_json()
#     question = data.get("message", "")

#     if not question.strip():
#         return jsonify({"reply": "我没有收到有效问题。"})

#     topic = classify_topic(question)
#     answer = search_memory(question, memory_data, topic=topic)

#     if answer:
#         return jsonify({"reply": answer})

#     messages = [ChatMessage(role="user", content=question)]
#     response = spark.generate([messages])
#     ai_reply = response.generations[0][0].text

#     return jsonify({"reply": ai_reply})

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    question = data.get("message", "")

    if not question.strip():
        return jsonify({"reply": "我没有收到有效问题。"})

    topic = classify_topic(question)
    answer = search_memory(question, memory_data, topic=topic)

    # 如果有记忆：提供参考内容 + 自由表达
    # 如果有记忆：提供参考内容 + 自由表达
    if answer:
        messages = [
            ChatMessage(role="system", content=(
                "你是一名简洁自然的助手，"
                "请根据提供的信息，用20到100字简洁表达出来，"
                "不要重复记忆内容原话，也不要解释。"
                "记忆中有网址要包含在内容里，网址不算字数。"
            )),
            ChatMessage(role="user", content=f"问题：{question}\n可参考的资料：{answer}")
        ]
        response = spark.generate([messages])
        ai_reply = response.generations[0][0].text
        return jsonify({"reply": ai_reply})


    # 没有记忆：正常提问
    messages = [
        ChatMessage(role="system", content="你是一名简洁的助手，回答请控制在20-100字内，简明扼要，不要啰嗦。"),
        ChatMessage(role="user", content=question)
    ]

    # 没有记忆：正常提问
    messages = [
        ChatMessage(role="system", content="你是一名简洁的助手，回答请控制在20-100字内，简明扼要，不要啰嗦。"),
        ChatMessage(role="user", content=question)
    ]
    response = spark.generate([messages])
    ai_reply = response.generations[0][0].text

    return jsonify({"reply": ai_reply})

if __name__ == '__main__':
    app.run(port=PORT, debug=True)