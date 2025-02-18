from langchain_milvus import Milvus
from langchain_openai import OpenAIEmbeddings
from build_RAG.load_chunk_PDF import texts
from build_RAG.load_env import api_key, base_url
from build_RAG.log import logger

# Milvus 配置信息
MILVUS_HOST = "x.x.x.x"
MILVUS_PORT = "19530"
COLLECTION_NAME = "langchain_rag_demo"
EMBEDDING_DIM = 1536# 与 OpenAI 模型的嵌入维度匹配

# 嵌入模型初始化
embeddings = OpenAIEmbeddings(
    model="text-embedding-ada-002",
    openai_api_key=api_key,
    openai_api_base=base_url
)

# 初始化 Milvus 向量存储
logger.info(f"Connecting to Milvus at {MILVUS_HOST}:{MILVUS_PORT}")
vector_store = Milvus(
    embedding_function=embeddings,
    collection_name=COLLECTION_NAME,
    connection_args={"uri": f"tcp://{MILVUS_HOST}:{MILVUS_PORT}"},
    drop_old=True,  # 如果集合已存在，删除旧集合
    auto_id=True    # 自动生成唯一 ID
)
logger.info(f"Initialized Milvus vector store: {COLLECTION_NAME}")

# 向量化并存储文档
logger.info("Starting document embedding and storage")
try:
    vector_store.add_documents(texts)
    logger.info("Successfully added documents to Milvus")
except Exception as e:
    logger.error(f"Failed to add documents to Milvus: {str(e)}")
    raise

# 检查存储内容
try:
    stats = vector_store.get_stats()
    logger.info(f"Milvus collection stats: {stats}")
except Exception as e:
    logger.error(f"Error retrieving Milvus stats: {str(e)}")
    raise

# 配置检索器
logger.info("Configuring retriever with top-k=2")
retriever = vector_store.as_retriever(search_kwargs={"k": 2})
