"""
导航配置模块
========================
功能概述：
    1. 定义系统导航页面结构
    2. 支持动态导航配置
    3. 提供导航组件初始化功能
"""
import streamlit as st
import logging
from src.config.config import Config

logger = logging.getLogger(__name__)


def get_navigation_pages() -> dict:
    """
    获取导航页面结构
    返回：导航页面字典，键为分组名称，值为页面列表
    """
    try:
        # 采用【字典 + 列表】结构，实现Streamlit侧边栏分组菜单
        # 字典key = 分组名称（空字符串表示无分组，直接显示在一级）
        # 列表内容 = 该分组下的所有页面（st.Page对象）
        pages = {
            # 空分组 → 页面直接显示在一级菜单（Home）
            "": [
                st.Page(r"pages\home.py", title="Home", icon=":material/home:"),
            ],
            # 普通分组 → 折叠菜单
            "PageGroup": [
                st.Page(r"pages\page1.py", title="Page1_title", icon=":material/settings:"),
                st.Page(r"pages\page2.py", title="Page2_title", icon=":material/star:"),
                st.Page(r"pages\page3.py", title="Page3_title", icon=":material/key:"),
            ],
        }
        return pages
    except Exception as e:
        logger.error(f"获取导航页面结构错误: {e}")
        # 返回默认导航结构
        return {
            "": [
                st.Page(r"pages\home.py", title="Home", icon=":material/home:"),
            ],
        }


def init_navigation() -> st.navigation:
    """
    初始化导航组件
    返回：导航组件对象
    """
    try:
        pages = get_navigation_pages()
        # 初始化导航组件并运行选中的页面
        # expanded=False：导航栏初始折叠状态 | 返回值pg为当前选中的页面对象
        pg = st.navigation(pages, expanded=False)
        return pg
    except Exception as e:
        logger.error(f"初始化导航组件错误: {e}")
        # 返回None，调用方需要处理
        return None
