"""
认证流程模块
========================
功能概述：
    1. 初始化登录状态
    2. 检查用户登录状态
    3. 处理用户注销逻辑
    4. 提供认证相关工具函数
"""
import streamlit as st
import logging
from src.config.config import Config

logger = logging.getLogger(__name__)


def init_login_state():
    """
    初始化登录状态
    从Cookie中恢复登录状态
    """
    try:
        if "logged_in" not in st.session_state:
            from src.auth.cookies import cookie_setAndremove
            is_not_logged = cookie_setAndremove(sign="查询")
            st.session_state.logged_in = not is_not_logged
            logger.info(f"初始化登录状态: {'已登录' if st.session_state.logged_in else '未登录'}")
    except Exception as e:
        logger.error(f"初始化登录状态错误: {e}")
        st.session_state.logged_in = False


def check_login_status() -> bool:
    """
    检查登录状态
    返回：是否已登录
    """
    if "logged_in" not in st.session_state:
        init_login_state()
    return st.session_state.logged_in


def get_current_user() -> dict:
    """
    获取当前用户信息
    返回：用户信息字典，如果未登录返回None
    """
    if "current_user" in st.session_state:
        return st.session_state.current_user
    return None


def logout_user() -> bool:
    """
    处理用户注销
    清空会话状态和Cookie
    返回：是否注销成功
    """
    try:
        # 记录用户注销信息
        user_info = get_current_user()
        if user_info:
            logger.info(f"用户 {user_info['username']} 注销系统")
        
        # 清空Streamlit会话状态（包含登录用户信息）
        st.session_state.clear()
        # 导入Cookie操作模块，删除登录态Cookie
        from src.auth.cookies import cookie_setAndremove
        cookie_setAndremove(sign='删除')
        logger.info("用户注销成功")
        return True
    except Exception as e:
        logger.error(f"用户注销错误: {e}")
        return False
