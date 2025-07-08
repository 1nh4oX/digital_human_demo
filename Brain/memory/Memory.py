import json
import os
from fuzzywuzzy import fuzz


# 新增：根据用户输入判断所属话题类别
def classify_topic(user_input):
    user_input = user_input.lower()
    if "深圳大学" in user_input or "深大" in user_input:
        if any(kw in user_input for kw in ["学费", "招生", "学院", "专业", "介绍"]):
            return "szu_school"
        elif any(kw in user_input for kw in ["食堂", "宿舍", "生活", "难吃", "好吃", "贵", "社团"]):
            return "szu_life"
        else:
            return "szu_school"  # 默认分配给学校类
    return "other"

def load_memory():
     # 获取 memory.json 的绝对路径
    dir_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(dir_path, "memory.json")
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def search_memory(user_input, memory_data, topic=None, threshold=80):
    best_match = None
    highest_score = 0

    for item in memory_data:
        if topic and item.get("topic") != topic:
            continue
        score = fuzz.ratio(user_input.lower(), item["question"].lower())
        if score > highest_score and score >= threshold:
            highest_score = score
            best_match = item["answer"]

    return best_match