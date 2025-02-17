import csv
from transformers import BartForConditionalGeneration, BartTokenizer

# 加载预训练模型和分词器
model_name = 'facebook/bart-large-cnn'
tokenizer = BartTokenizer.from_pretrained(model_name)
model = BartForConditionalGeneration.from_pretrained(model_name)
# 定义输入和输出 CSV 文件的路径
input_file = 'cleaned_notes.csv'
output_file = 'nlp_cleaned_notes.csv'

with open(input_file, 'r', encoding='utf-8', newline='') as infile, \
        open(output_file, 'w', encoding='utf-8', newline='') as outfile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        if 'desc' in row:
            inputs = tokenizer([row['desc']], max_length=1024, return_tensors='pt')
            summary_ids = model.generate(inputs['input_ids'], num_beams=4, max_length=150, early_stopping=True)
            summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            row['desc'] = summary
        writer.writerow(row)

print(f"处理后的数据已保存到 {output_file}")