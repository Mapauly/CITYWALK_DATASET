import csv
from kafka import KafkaProducer
import json

# 配置 Kafka 生产者
# 请将 <远程主机 IP> 替换为实际的远程主机 IP 地址
producer = KafkaProducer(
    bootstrap_servers=['47.99.178.77:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# 定义 Kafka 主题，将 <主题名称> 替换为实际要使用的 Kafka 主题
kafka_topic = '<citywalk_dataset>'

try:
    # 打开 CSV 文件
    with open('cleaned_notes.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        # 逐行读取 CSV 文件内容
        for row in reader:
            # 发送每一行数据到 Kafka 主题
            producer.send(kafka_topic, value=row)
            producer.flush()  # 确保消息立即发送
            print(f"Sent message: {row}")

    print("All messages from CSV file have been sent to Kafka.")

except Exception as e:
    print(f"Error sending messages to Kafka: {e}")

finally:
    # 关闭 Kafka 生产者
    producer.close()