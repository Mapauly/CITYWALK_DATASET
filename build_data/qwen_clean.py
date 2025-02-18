import csv
import os
import openai

# 配置 OpenAI 客户端以兼容百炼 API
client = openai.OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

input_file = '../data/cleaned_notes.csv'
output_file = '../data/qwen_cleaned_notes.csv'

def simplify_description(desc):
    try:
        response = client.chat.completions.create(
            model="qwen-turbo",  # 使用通义千问模型
            messages=[
                {"role": "system", "content": "请去掉多余表情符号和语气内容。"},
                {"role": "user", "content": desc}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"处理文本时出错: {e}")
        return desc

fields_to_keep = ['desc']

with open(input_file, 'r', encoding='utf-8', newline='') as infile, \
        open(output_file, 'w', encoding='utf-8', newline='') as outfile:
    reader = csv.DictReader(infile)
    # 筛选出要保留的字段名
    fieldnames = [field for field in reader.fieldnames if field in fields_to_keep]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        new_row = {}
        if 'desc' in row:
            row['desc'] = simplify_description(row['desc'])
        for field in fieldnames:
            if field in row:
                new_row[field] = row[field]
        writer.writerow(new_row)

print(f"处理后的数据已保存到 {output_file}")