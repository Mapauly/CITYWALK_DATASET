import pymysql
import csv
import os

# 从环境变量获取数据库配置，若未设置则使用默认值
RELATION_DB_PWD = os.getenv("RELATION_DB_PWD", "root")
RELATION_DB_USER = os.getenv("RELATION_DB_USER", "root")
RELATION_DB_HOST = os.getenv("RELATION_DB_HOST", "localhost")
# 将端口号转换为整数类型
RELATION_DB_PORT = int(os.getenv("RELATION_DB_PORT", 3306))
RELATION_DB_NAME = os.getenv("RELATION_DB_NAME", "media_crawler")

def clean_xhs_notes():
    try:
        # 建立数据库连接
        conn = pymysql.connect(
            host=RELATION_DB_HOST,
            user=RELATION_DB_USER,
            password=RELATION_DB_PWD,
            port=RELATION_DB_PORT,
            database=RELATION_DB_NAME
        )
        cursor = conn.cursor()

        # 执行 SQL 查询，从 xhs_note 表中获取所需数据
        cursor.execute('''
            SELECT title, `desc`, tag_list 
            FROM xhs_note
        ''')

        # 用于存储清洗后的数据
        cleaned_data = []
        # 遍历查询结果
        for row in cursor.fetchall():
            # 处理标题，去除首尾空格，若为空则设为 '无标题'
            title = row[0].strip() if row[0] else '无标题'
            # 处理正文，去除首尾空格并将换行符替换为空格，若为空则设为空字符串
            desc = row[1].strip().replace('\n', ' ') if row[1] else ''
            # 处理标签，分割标签字符串并去除每个标签的首尾空格和内部空格
            tags = []
            if row[2]:
                tags = [tag.strip().replace(' ', '') for tag in row[2].split(',') if tag.strip()]

            # 将处理后的数据添加到 cleaned_data 列表中
            cleaned_data.append({
                'title': title,
                'desc': desc,
                'tags': tags
            })

        # 将清洗后的数据保存到 CSV 文件
        with open('cleaned_notes.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['title', 'desc', 'tags'])
            writer.writeheader()
            for item in cleaned_data:
                writer.writerow({
                    'title': item['title'],
                    'desc': item['desc'],
                    'tags': ', '.join(item['tags'])
                })

        print(f"成功处理{len(cleaned_data)}条数据，结果已保存到 cleaned_notes.csv")

    except pymysql.Error as e:
        print(f"数据库连接或操作出错: {e}")
    finally:
        if 'conn' in locals():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    clean_xhs_notes()