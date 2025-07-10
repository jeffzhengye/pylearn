import asyncio
import sys
from pathlib import Path
from typing import List
from dotenv import load_dotenv

from camel.models import ModelFactory
from camel.toolkits import FunctionTool, SearchToolkit, CodeExecutionToolkit, ExcelToolkit, FileWriteToolkit
from camel.types import ModelPlatformType, ModelType
from camel.logger import set_log_level
from camel.toolkits import MCPToolkit
from camel.societies import RolePlaying
from owl.utils import run_society


# 加载环境变量
base_dir = Path(__file__).parent.parent
env_path = base_dir / "owl" / ".env"
load_dotenv(dotenv_path=str(env_path))

# 设置日志级别
set_log_level(level="DEBUG")

async def construct_society(
    question: str,
    tools: List[FunctionTool],
) -> RolePlaying:
    """
    构建一个基于DeepSeek模型的多智能体社会实例。

    参数:
        question (str): 要解决的问题。
        tools (List[FunctionTool]): 可用的工具列表。
    返回:
        RolePlaying: 配置好的多智能体社会实例。
    """
    # 创建DeepSeek模型实例
    models = {
        "user": ModelFactory.create(
            model_platform=ModelPlatformType.DEEPSEEK,
            model_type=ModelType.DEEPSEEK_CHAT,
            model_config_dict={"temperature": 0},
        ),
        "assistant": ModelFactory.create(
            model_platform=ModelPlatformType.DEEPSEEK,
            model_type=ModelType.DEEPSEEK_CHAT,
            model_config_dict={"temperature": 0},
        ),
    }

    # 配置用户智能体参数
    user_agent_kwargs = {"model": models["user"]}
    # 配置助手智能体参数，包括可用工具
    assistant_agent_kwargs = {"model": models["assistant"], "tools": tools}

    # 配置任务参数
    task_kwargs = {
        "task_prompt": question,
        "with_task_specify": False,
    }

    # 创建并返回多智能体社会实例
    society = RolePlaying(
        **task_kwargs,
        user_role_name="user",
        user_agent_kwargs=user_agent_kwargs,
        assistant_role_name="assistant",
        assistant_agent_kwargs=assistant_agent_kwargs,
        output_language="Chinese",
    )
    return society

async def main():
    # 加载MCP服务器配置
    config_path = Path(__file__).parent / "mcp_servers_config.json"
    mcp_toolkit = MCPToolkit(config_path=str(config_path))

    try:
        # 连接到MCP服务器
        await mcp_toolkit.connect()
        print("成功连接到MCP服务器")
        # 获取工具列表
        tools = mcp_toolkit.get_tools()
        processed_tools = []
        tool_names = []

        for tool in tools:
            if asyncio.iscoroutinefunction(tool):
                # 如果是协程函数，可能需要进一步处理，这里简单提示
                print(f"警告: 工具 {tool.func.__name__} 是协程函数，需要正确处理")
                # 这里可以根据实际情况决定是否调用并等待协程
                # result = await tool()
                # processed_tools.append(result)
            else:
                processed_tools.append(tool)
                try:
                    tool_names.append(tool.func.__name__)
                except AttributeError:
                    tool_names.append(str(tool))

        print(f"当前可用MCP服务器工具名称: {tool_names}")

        # 合并工具列表
        all_tools = [
            *processed_tools,
            # *CodeExecutionToolkit(sandbox="subprocess", verbose=True).get_tools(),
            # SearchToolkit().search_duckduckgo,
            # SearchToolkit().search_wiki,
            # SearchToolkit().search_baidu,
            # *ExcelToolkit().get_tools(),
            # *FileWriteToolkit(output_dir="./").get_tools(),
        ]

        # 设置默认任务
        default_task = ("use chrome, navigate me to baidu.com, and search for 'camel'")

        # 如果提供了命令行参数，则使用该参数作为任务，否则使用默认任务
        task = sys.argv[1] if len(sys.argv) > 1 else default_task

        # 构建并运行智能体社会
        society: RolePlaying = await construct_society(task, all_tools)
        answer, chat_history, token_count = run_society(society)
        print(f"\n结果: {answer}")

    except KeyboardInterrupt:
        print("\n收到退出信号，正在关闭...")
    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        # 确保安全断开连接
        try:
            await mcp_toolkit.disconnect()
        except Exception as e:
            print(f"断开连接时发生错误: {e}")

if __name__ == "__main__":
    asyncio.run(main())