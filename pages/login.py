"""
登录页面模块
========================
功能概述：
    1. 渲染系统登录界面（含标题、角色选择、账号密码输入）
    2. 处理用户登录表单提交逻辑
    3. 调用认证工具验证账号/密码/角色的合法性
    4. 登录成功后维护会话状态（session_state）和用户Cookie
"""
import streamlit as st
import logging
from src.auth.auth import validate_user, get_all_roles
from src.config.config import Config

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Config.LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def show_login_page() -> None:
    """
    渲染并处理登录页面的核心函数
    流程：
        1. 渲染页面标题（居中样式）
        2. 获取系统可用角色列表（无数据时使用兜底默认角色）
        3. 构建登录表单（角色选择、账号/密码输入、登录按钮）
        4. 处理表单提交：验证用户信息，成功则维护登录态并跳转
    """
    try:
        # from pathlib import Path
        # import base64
        # # 👉 固定写法：读取本地图片并转换为可显示格式
        # img_path = Path("assets/images/bom_home_page.png")
        # with open(img_path, "rb") as f:
        #     encoded = base64.b64encode(f.read()).decode()
        # <img src="data:image/png;base64,{encoded}" style="height: 80px; margin-bottom: 10px;">
        # 标题 + 图片居中显示
        st.markdown(f"""
        <div style='text-align: center; padding: 20px;'>
            <h1>{Config.APP_ICON} {Config.APP_NAME}</h1>
        </div>
        """, unsafe_allow_html=True)
        # ------------------------ 角色列表加载 ------------------------
        # 获取系统中配置的所有可用角色（从数据库/配置文件读取）
        available_roles = get_all_roles()
        # 兜底处理：如果无可用角色，使用默认角色列表（避免页面异常）
        if not available_roles:
            available_roles = ["Admin", "产品设计工程师", "工艺工程师", "生产人员"]

        # ------------------------ 登录表单构建 ------------------------
        # 创建登录表单，clear_on_submit=True：提交后清空表单输入
        with st.form("login_form", clear_on_submit=True):
            # 渲染页面标题（居中样式，使用HTML自定义排版）
            st.markdown(f"""
            <div style='text-align: center; padding: 20px;'>
                <h3>用户登录</h3>
            </div>
            """, unsafe_allow_html=True)

            # 构建三列布局，仅中间列显示表单（居中效果）
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:  # 中间列：表单核心内容
                # 角色选择下拉框，默认选中第一个角色
                role = st.selectbox("角色", available_roles, index=0)
                # 账号输入框（带占位提示）
                username = st.text_input("账号", placeholder="请输入用户名")
                # 密码输入框（密码类型，隐藏输入内容）
                password = st.text_input("密码", type="password", placeholder="请输入密码")

                # 登录提交按钮（主样式按钮，突出显示）
                submit_btn = st.form_submit_button("登录", type="primary")

                # ------------------------ 登录逻辑处理 ------------------------
                # 点击登录按钮时触发验证逻辑
                if submit_btn:
                    # 空值校验：账号/密码不能为空
                    if not username or not password:
                        st.error("账号和密码不能为空！")
                        logger.warning(f"登录尝试：账号或密码为空")
                    # 调用认证函数：验证账号、密码、角色是否匹配
                    elif validate_user(username, password, role):
                        # 登录成功：构造用户信息字典
                        user_info = {"username": username, "role": role}
                        # 1. 维护Streamlit会话状态（标记已登录、存储用户信息）
                        st.session_state.logged_in = True
                        st.session_state.current_user = user_info
                        # 提示登录成功
                        st.success("登录成功！正在跳转...")
                        # 2. 持久化用户信息到Cookie（避免页面刷新丢失登录态）
                        from src.auth.cookies import cookie_setAndremove
                        cookie_setAndremove(sign='设置', user_info=user_info)
                        # 记录登录成功信息
                        logger.info(f"用户 {username} (角色: {role}) 登录成功")
                        # 重新运行页面：跳转到系统主界面
                        st.rerun()
                    # 认证失败：提示用户信息不匹配
                    else:
                        st.error("账号/密码/角色不匹配，请重试！")
                        logger.warning(f"登录失败：账号 {username} 密码错误或角色不匹配")
    except Exception as e:
        logger.error(f"登录页面错误: {e}")
        st.error("系统发生错误，请稍后重试")