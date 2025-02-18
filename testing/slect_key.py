import csv

# 定义关键字列表
keywords = [ "路线","机位","吃","周末","夜","咖啡","博物馆","情侣","游客","亲子","寺"]

# 初始化分类字典，每个关键字对应一个空列表
classified_data = {keyword: [] for keyword in keywords}

# 读取 CSV 文件
try:
    with open('../data/cleaned_notes.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        # 获取 CSV 文件的字段名
        fieldnames = reader.fieldnames
        for row in reader:
            # 将每一行数据转换为字符串
            row_str = ' '.join(row.values())
            for keyword in keywords:
                if keyword in row_str:
                    # 如果包含关键字，则将该行数据添加到相应的分类列表中
                    classified_data[keyword].append(row)

    # 输出分类结果到新的 CSV 文件
    for keyword, data in classified_data.items():
        filename = f'{keyword}_classified.csv'
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                writer.writerow(row)
        print(f"包含关键字 '{keyword}' 的数据已保存到 {filename}")

except FileNotFoundError:
    print("未找到 'cleaned_notes.csv' 文件，请检查文件路径。")