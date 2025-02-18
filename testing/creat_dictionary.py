import csv
import os
import openai
import json

# 配置 OpenAI 客户端以兼容百炼 API
client = openai.OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

input_file = '../data/classified_data.csv'
knowledge_base = []

def extract_fields(desc):
    try:
        response = client.chat.completions.create(
            model="qwen-turbo",  # 使用通义千问模型
            messages=[
                {"role": "system", "content": "请从以下文本中提取关键信息并以字典形式输出。"},
                {"role": "user", "content": desc}
            ]
        )
        result = response.choices[0].message.content.strip()
        try:
            # 尝试将大模型返回的文本转换为字典
            info_dict = eval(result)
            return info_dict
        except:
            print(f"无法将结果转换为字典: {result}")
            return {}
    except Exception as e:
        print(f"处理文本时出错: {e}")
        return {}

with open(input_file, 'r', encoding='utf-8', newline='') as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        desc = row.get('desc', '')
        info_dict = extract_fields(desc)
        knowledge_base.append(info_dict)

# 保存知识库为 JSON 文件
output_file = 'knowledge_base.json'
with open(output_file, 'w', encoding='utf-8') as outfile:
    json.dump(knowledge_base, outfile, ensure_ascii=False, indent=4)

print(f"知识库已保存到 {output_file}")