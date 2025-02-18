from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from build_RAG.log import logger

# 加载 PDF 文档
logger.info("Starting document processing pipeline")
loader = PyMuPDFLoader("data/llama2.pdf")  # 替换为你的文档路径
pages = loader.load_and_split()
logger.info(f"Loaded {len(pages)} pages from PDF")

# 初始化文本分割器
logger.info("Initializing text splitter")
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,  # 每个块的最大字符数
    chunk_overlap=100,  # 每个块的重叠部分，确保上下文完整性
    length_function=len,  # 使用字符长度作为分割标准
    add_start_index=True,  # 为每个块添加起始索引
)

# 分割文档
texts = text_splitter.create_documents(
    [page.page_content for page in pages[:4]]  # 处理前4页内容
)
logger.info(f"Created {len(texts)} text chunks")
logger.debug(f"Average chunk size: {sum(len(t.page_content) for t in texts) / len(texts):.0f} characters")


# 打印前5个分块内容和大小
for i, chunk in enumerate(texts[:5]):
    logger.info(f"Chunk {i + 1}: {chunk.page_content[:50]}... (Length: {len(chunk.page_content)})")
