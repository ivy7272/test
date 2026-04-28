# 修改 cookies.py 中的 Cookie 操作逻辑
import json
import streamlit as st
import logging
from streamlit_cookies_controller import CookieController
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

controller = CookieController(key='cookies')

# 碎片装饰器：让局部组件刷新，不刷新整个页面！
@st.fragment
def cookie_setAndremove(sign, user_info=None):
    """
    Cookie操作：存储/读取完整用户信息
    sign: '设置'/'删除'/'查询'
    user_info: 设置时传入字典，如 {"username": "admin", "role": "Admin"}
    """
    try:
        match sign:
            case '设置':
                if user_info and isinstance(user_info, dict):
                    # 将用户信息字典转为JSON字符串存储
                    controller.set(name='user_info', value=json.dumps(user_info))
                    logger.info(f"设置Cookie成功：用户 {user_info.get('username')}")

            case '删除':
                controller.remove(name='user_info')
                logger.info("删除Cookie成功")
                st.rerun(scope='app')

            case '查询':
                cookie_str = controller.get(name='user_info')
                if cookie_str:
                    try:
                        # 将JSON字符串转回字典
                        user_info = json.loads(cookie_str)
                        st.session_state['logged_in'] = True
                        st.session_state['current_user'] = user_info  # 直接恢复完整用户信息
                        logger.info(f"查询Cookie成功：用户 {user_info.get('username')}")
                        return False  # 已登录
                    except json.JSONDecodeError as e:
                        logger.error(f"Cookie解析失败: {e}")
                        return True  # 未登录
                else:
                    logger.info("查询Cookie：未找到用户信息")
                    return True  # 未登录

            case _:
                logger.warning(f"不支持的操作类型：{sign}")
                st.warning(f"不支持的操作类型：{sign}")
                return None
    except Exception as e:
        logger.error(f"Cookie操作错误: {e}")
        return True  # 出错时视为未登录