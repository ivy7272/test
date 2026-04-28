"""
日志工具模块
========================
功能概述：
    1. 配置系统日志
    2. 提供日志记录工具函数
    3. 集中管理日志格式和输出
"""
import logging
import os
from src.config.config import Config


def configure_logger():
    """
    配置系统日志
    设置日志级别、格式和输出
    """
    try:
        # 确保日志目录存在
        os.makedirs(Config.LOG_DIR, exist_ok=True)
        
        # 配置日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(Config.LOG_FILE, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        logger = logging.getLogger(__name__)
        logger.info("日志配置成功")
        return logger
    except Exception as e:
        # 如果日志配置失败，使用默认日志
        print(f"日志配置错误: {e}")
        return logging.getLogger(__name__)


# 创建全局日志对象
logger = configure_logger()
