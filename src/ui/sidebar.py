"""
侧边栏管理模块
========================
功能概述：
    1. 渲染侧边栏用户信息
    2. 提供注销功能
    3. 支持不同角色显示不同侧边栏内容
"""
import streamlit as st
import logging
from src.auth.auth_flow import get_current_user, logout_user
from src.config.config import Config

logger = logging.getLogger(__name__)


def render_sidebar():
    """
    渲染侧边栏
    显示用户信息和注销按钮
    """
    try:
        with st.sidebar:
            # 显示当前用户信息
            user_info = get_current_user()
            if user_info:
                st.markdown(f"### 当前用户：{user_info['username']}")
                st.markdown(f"### 角色：{user_info['role']}")
                st.divider()

                # 注销按钮：清空会话状态 + 删除登录Cookie
                if st.button(
                        label='🔴 注销',
                        key='log_off',          # 唯一标识，避免组件冲突
                        type='secondary',       # 按钮样式（secondary/primary）
                        use_container_width=True  # 按钮宽度适配侧边栏
                ):
                    # 处理注销逻辑
                    success = logout_user()
                    if success:
                        # 重新运行页面，跳转到登录页
                        st.rerun()
    except Exception as e:
        logger.error(f"渲染侧边栏错误: {e}")
