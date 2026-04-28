"""
项目主程序
========================
功能概述：
1. 系统入口，负责用户登录状态校验（基于Cookie）
2. 配置Streamlit页面基础属性（标题、布局、侧边栏等）
3. 构建多模块导航结构（订单操作、BOM管理）
4. 处理用户注销逻辑，清理会话状态和Cookie
"""
import streamlit as st
from src.utils.logger import logger
from src.config.page_config import configure_page
from src.auth.auth_flow import init_login_state, check_login_status, get_current_user
from src.navigation.navigation import init_navigation
from src.ui.sidebar import render_sidebar
# ========================= 页面全局配置 =========================
# 注意：set_page_config() 只能调用一次，且必须是第一个Streamlit命令
# 我们将在程序入口根据登录状态决定调用哪个配置函数

def main() -> None:
    """
    主函数：已登录用户的核心逻辑入口
    负责：
        1. 构建系统的多页面导航结构
        2. 运行用户选中的页面逻辑
        3. 在侧边栏渲染用户信息与注销功能
    """
    try:
        # 如果会话中存在当前用户信息，记录登录日志
        user_info = get_current_user()
        if user_info:
            logger.info(f"用户 {user_info['username']} (角色: {user_info['role']}) 登录系统")

        # 初始化导航组件并运行选中的页面
        pg = init_navigation()
        if pg:
            pg.run()  # 执行当前选中页面的核心逻辑

        # 渲染侧边栏
        render_sidebar()

    except Exception as e:
        # 捕获主程序运行异常，记录错误并提示用户
        logger.error(f"主函数执行错误: {e}")
        st.error("系统发生错误，请稍后重试")

# ========================= 程序入口 =========================
if __name__ == "__main__":
    try:
        # 首先配置页面，确保 set_page_config() 是第一个 Streamlit 命令
        configure_page()
        
        logger.info("系统启动")

        # 初始化登录状态（从Cookie恢复）
        init_login_state()

        # 如果未登录 → 跳转到登录页
        if not check_login_status():
            from pages.login import show_login_page
            logger.info("显示登录页面")

            # 显示登录界面
            show_login_page()
            # 停止执行后续代码，避免进入主程序
            st.stop()

        # 已登录 → 运行主界面
        main()

    except Exception as e:
        logger.error(f"系统启动错误: {e}")
        st.error("系统启动失败，请稍后重试")