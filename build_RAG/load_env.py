from dotenv import load_dotenv, find_dotenv
import os

# 加载 .env 文件
env_path = find_dotenv()
if not env_path:
    raise EnvironmentError("No .env file found. Please create a .env file with the required API keys.")

load_dotenv(env_path)

# 获取 OpenAI API 配置
api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL")

if not api_key or not base_url:
    raise EnvironmentError("Missing API key or base URL in environment variables.")
