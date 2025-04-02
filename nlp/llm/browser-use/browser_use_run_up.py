from langchain_openai import ChatOpenAI
from browser_use import Agent
import asyncio
from dotenv import load_dotenv
from pydantic import SecretStr
import os
from logging_config import setup_logging

# 配置日志
setup_logging(verbose=True)

load_dotenv(dotenv_path="/mnt/d/wps/notes/configure_bakup/.env")

# model="qwen-max"
# model="gpt-4o-mini"
DEEPSEEK_API_KEY=os.getenv("DEEPSEEK_API_KEY")
# Initialize the model
llm=ChatOpenAI(base_url='https://api.deepseek.com/v1', model='deepseek-chat', api_key=SecretStr(DEEPSEEK_API_KEY))
use_vision=False # 是否使用视觉, deepseek不支持视觉

async def main():
    agent = Agent(
        # task="Compare the price of gpt-4o and DeepSeek-V3",
        # task = "open baidu.com and search deepseek, get the first result",
        task="打开百度搜索，搜索'东方雨虹'新闻，获取第一个结果后抽取新闻标题、时间、文本内容,然后退出",
        llm=llm,
        use_vision=use_vision,
        save_conversation_path="logs/conversation"
    )
    history = await agent.run()
    
    # Access (some) useful information
    # history.urls()              # List of visited URLs
    # history.screenshots()       # List of screenshot paths
    print("action names", history.action_names())      # Names of executed actions
    history.extracted_content() # Content extracted during execution
    history.errors()           # Any errors that occurred
    print("model actions", history.model_actions())     # All actions with their parameters

asyncio.run(main())