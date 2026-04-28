"""
页面配置模块
========================
功能概述：
    1. 配置Streamlit页面基础属性
    2. 提供页面配置相关工具函数
    3. 集中管理页面布局和样式
"""
import streamlit as st
import logging
from src.config.config import Config

logger = logging.getLogger(__name__)


def configure_page():
    """
    配置Streamlit页面基础属性
    需在所有页面渲染前执行
    """
    try:
        # 配置Streamlit页面基础属性
        st.set_page_config(
            page_title=Config.APP_NAME,  # 浏览器标签页标题
            page_icon=Config.APP_ICON,    # 页面图标（支持emoji/图片路径）
            layout=Config.PAGE_LAYOUT,    # 宽屏布局（默认centered，改为wide最大化利用屏幕）
            initial_sidebar_state=Config.INITIAL_SIDEBAR_STATE  # 初始状态折叠侧边栏，节省主内容区空间
        )
        logger.info("页面配置成功")
    except Exception as e:
        logger.error(f"页面配置错误: {e}")



