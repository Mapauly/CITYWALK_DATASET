from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from build_RAG.load_env import api_key, base_url
from build_RAG.log import logger
from build_RAG.milvus import retriever

# 定义 Prompt 模板
template = """Answer the question based only on the following context:
{context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

# 初始化 LLM（生成模型）
logger.info("Initializing LLM with model: gpt-4o-mini")
llm = ChatOpenAI(
    temperature=0,  # 确保回答的确定性
    model="gpt-4o-mini",  # 替换为所需的模型
    openai_api_key=api_key,
    openai_api_base=base_url
)

# 构建 RAG 流程
logger.info("Building RAG chain")
rag_chain = (
        {"question": RunnablePassthrough(), "context": retriever}
        | prompt
        | llm
        | StrOutputParser()
)
logger.info("RAG system initialization complete")

def process_query(question: str):
    """处理单个查询并返回答案"""
    logger.info(f"Processing query: {question}")
    try:
        logger.info("Retrieving relevant documents")
        response = rag_chain.invoke(question)
        logger.info("Successfully generated response")
        return response
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise

# 启动交互式问答
logger.info("Starting interactive chat loop")
while True:
    question = input("\nEnter your question (or press Enter to exit): ")
    if question.strip() == "":
        logger.info("User requested exit")
        break

    logger.info("Processing user question")
    try:
        response = process_query(question)
        print(f"\nResponse: {response}\n")
        logger.info("Successfully provided response to user")
    except Exception as e:
        logger.error(f"Error in chat loop: {str(e)}")
        print(f"An error occurred: {str(e)}")
    print("-" * 50)
