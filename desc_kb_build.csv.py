import csv
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings


def chunk_text(text, chunk_size=500, overlap=100):
    """
    将文本分块
    :param text: 输入的文本
    :param chunk_size: 每个分块的大小
    :param overlap: 分块之间的重叠部分大小
    :return: 分块后的文本列表
    """
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start = end - overlap
    return chunks


# 加载嵌入模型
model = SentenceTransformer('all-MiniLM-L6-v2')

# 初始化 Chroma 客户端
client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory=".chromadb"
))

# 创建一个集合
collection = client.create_collection(name="knowledge_base")

input_file = 'classified_data.csv'
with open(input_file, 'r', encoding='utf-8', newline='') as infile:
    reader = csv.DictReader(infile)
    id_counter = 0
    for row in reader:
        desc = row.get('desc', '')
        if desc:
            # 文本分块
            chunks = chunk_text(desc)
            # 向量化
            embeddings = model.encode(chunks)
            # 将分块文本和对应的向量存储到数据库中
            for chunk, embedding in zip(chunks, embeddings):
                collection.add(
                    documents=[chunk],
                    embeddings=[embedding.tolist()],
                    ids=[str(id_counter)]
                )
                id_counter += 1

# 保存数据库
client.persist()

print("知识库已构建并存储到向量数据库中。")