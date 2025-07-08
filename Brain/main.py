from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage
import time

from memory.Memory import load_memory,search_memory, classify_topic
from api.API import (
    SPARKAI_URL,
    SPARKAI_APP_ID,
    SPARKAI_API_KEY,
    SPARKAI_API_SECRET,
    SPARKAI_DOMAIN
)

if __name__ == '__main__':
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
    
    # main loop
    handler = ChunkPrintHandler()
    while(True):  
        # user asking
        question = input("User: ")
        if question in ["再见", "quit", "拜拜"]:
            print("ONOM: See you!")
            break;
        # memory searching...
        topic = classify_topic(question)
        answer = search_memory(question, memory_data, topic=topic)
        if answer: # if find the answer from memory
            print("ONOM: " + answer)
            continue

        # if out of answer then search by model
        messages = [ChatMessage(
            role="user",
            content=question
        )]
        # get the answer
        response = spark.generate([messages], callbacks=[handler])
        ai_reply = response.generations[0][0].text
        # AI answering
        print("ONOM: " + ai_reply)
        # time setter
        time.sleep(0.8)