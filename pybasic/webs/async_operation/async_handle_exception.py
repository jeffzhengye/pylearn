import asyncio
import logging
import sys
import traceback
from loguru import logger

# 配置loguru日志
loguru_format = "<green>{time:MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"

logger.remove()
logger.add(
    sys.stdout,
    level=logging.DEBUG,
    format=loguru_format,
    enqueue=True,
    backtrace=True,
    diagnose=True
)

logger.add(
    sink="logs/test_errors.log",
    format=loguru_format,
    level="WARNING",
    enqueue=True,
    rotation="50 MB",
    retention="30 days",
    backtrace=True,
    diagnose=True
)

def handle_async_exception(loop, context):
    """处理异步异常的函数"""
    # context["message"] will always be there; but context["exception"] may not
    msg = context.get("exception", context["message"])
    logger.error(f"Caught exception: {msg}")
    if "exception" in context:
        # 获取实际的异常对象并记录完整的堆栈跟踪
        exception = context.get("exception")
        logger.error(f"Exception type: {type(exception)}")
        logger.error("Exception details:", exc_info=exception)
    logger.error(f"Exception in loop: {id(loop)}")

async def problematic_task():
    """一个会引发异常的异步任务"""
    await asyncio.sleep(1)
    raise ValueError("这是一个测试异常")

async def scheduled_exception():
    """通过call_later调度的异常"""
    # raise RuntimeError("这是一个调度的异常")
    raise Exception("这是回调函数中的异常")

def callback_exception():
    """回调函数中的异常"""
    raise Exception("这是回调函数中的异常")

async def main():
    """主函数"""
    logger.info("开始测试异步异常处理")
    
    # 创建事件循环并设置异常处理器
    loop = asyncio.get_event_loop()
    loop.set_exception_handler(handle_async_exception)
    
    # 测试1: 直接运行会引发异常的任务（需要在任务中捕获）
    logger.info("测试1: 直接运行会引发异常的任务")
    # try:
    #     await problematic_task()
    # except Exception as e:
    #     logger.exception(f"捕获到异常: {e}")
    
    # 测试2: 使用ensure_future运行任务（会被事件循环异常处理器捕获）
    # logger.info("测试2: 使用ensure_future运行任务")
    # task = asyncio.ensure_future(problematic_task())
    # 不等待任务完成，让它在后台运行并触发异常处理器
    
    # 测试3: 使用call_soon抛出异常
    # logger.info("测试3: 使用call_soon抛出异常")
    # loop.call_soon(callback_exception)
    
    # 测试4: 使用call_later抛出异常（正确的方法）
    # logger.info("测试4: 使用call_later抛出异常")
    # 方法1: 使用普通函数
    # loop.call_later(0.1, callback_exception)
    loop.call_soon_threadsafe(scheduled_exception())
    
    # 方法2: 如果要测试协程异常，需要使用 asyncio.create_task()
    # asyncio.create_task(scheduled_exception())
    
    # 给一些时间让异步任务执行并触发异常处理器
    await asyncio.sleep(2)
    
    logger.info("所有测试完成")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.exception("主程序异常退出")