import logging

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # 输出到控制台
        logging.FileHandler('log/langchain_rag_system.log')  # 输出到文件
    ]
)
logger = logging.getLogger(__name__)
logger.info("Logging system initialized.")
