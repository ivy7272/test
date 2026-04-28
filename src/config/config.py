"""
配置管理模块
============================
功能概述：
    1. 集中管理项目配置信息
    2. 加载环境变量
    3. 提供应用配置、路径配置等
"""
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class Config:
    """应用配置类"""
    # ========================= Streamlit 页面基础配置 =========================
    # 系统应用名称（浏览器标签页标题、页面标题使用）
    APP_NAME = "项目框架测试系统"
    # 页面图标（浏览器标签栏图标，支持 Emoji 表情 / 图片路径）
    APP_ICON = "💻"
    # 页面布局方式
    # - wide：宽屏布局，最大化利用屏幕宽度    # - centered：居中布局，内容区域较窄
    PAGE_LAYOUT = "wide"
    # 侧边栏初始展示状态
    # - collapsed：默认折叠侧边栏    # - expanded：默认展开侧边栏
    INITIAL_SIDEBAR_STATE = "collapsed"
    
    # 用户信息数据文件路径
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, "data")
    USER_DATA_FILE = os.path.join(DATA_DIR, "users.xlsx")
    
    # 认证配置
    SESSION_EXPIRY = 3600  # 会话过期时间（秒）
    
    # 日志配置
    LOG_DIR = os.path.join(BASE_DIR, "logs")
    LOG_FILE = os.path.join(LOG_DIR, "app.log")


# 创建必要的目录
os.makedirs(Config.DATA_DIR, exist_ok=True)
os.makedirs(Config.LOG_DIR, exist_ok=True)