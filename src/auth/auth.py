"""
用户认证工具模块
============================
功能概述：
    1. 基于Excel文件实现用户数据的持久化存储（自动创建默认数据）
    2. 提供用户登录信息验证（账号/密码/角色三重校验）
    3. 封装角色管理、登录状态检查、权限校验等核心认证功能
    4. 异常处理：兼容文件不存在、读取失败等边界场景

数据文件：
    - 存储路径：data/users.xlsx
    - 字段说明：username(账号)、password(密码)、role(角色)

"""
import streamlit as st
import pandas as pd
import os
from src.config.config import Config

# ========================= 全局配置 =========================
# 使用配置文件中的用户数据文件路径
USER_DATA_FILE = Config.USER_DATA_FILE


def load_user_data() -> pd.DataFrame:
    """
    加载/初始化用户数据（核心基础函数）
    流程：
        1. 检查并创建data目录（确保存储目录存在）
        2. 若用户数据文件不存在：创建默认Excel文件并返回默认数据
        3. 若文件存在：读取Excel文件并返回用户数据DataFrame
        4. 读取失败时捕获异常，返回空DataFrame

    返回值：
        pd.DataFrame: 用户数据表格（列：username/password/role）
    """
    # 确保data目录存在，不存在则自动创建（避免文件写入失败）
    os.makedirs(os.path.dirname(USER_DATA_FILE), exist_ok=True)

    # 场景1：用户数据文件不存在 → 创建默认文件并初始化数据
    if not os.path.exists(USER_DATA_FILE):
        # 构造默认用户数据（覆盖系统核心角色）
        default_users = pd.DataFrame([
            {"username": "admin", "password": "admin123", "role": "Admin"},  # 系统管理员
            {"username": "designer", "password": "design123", "role": "产品设计工程师"},  # 设计角色
            {"username": "process", "password": "process123", "role": "工艺工程师"},  # 工艺角色
            {"username": "produce", "password": "produce123", "role": "生产人员"}  # 生产角色
        ])
        # 将默认数据写入Excel文件（index=False：不写入行索引）
        default_users.to_excel(USER_DATA_FILE, index=False)
        return default_users
    # 场景2：用户数据文件存在 → 尝试读取
    else:
        try:
            # 读取Excel文件返回用户数据
            return pd.read_excel(USER_DATA_FILE)
        except Exception as e:
            # 捕获文件读取异常（如文件损坏、格式错误），前端提示错误
            st.error(f"读取用户数据文件失败: {e}")
            # 返回空DataFrame，避免后续逻辑报错
            return pd.DataFrame()


def validate_user(username: str, password: str, role: str) -> bool:
    """
    验证用户登录信息（账号/密码/角色三重校验）
    核心逻辑：匹配用户输入与Excel中存储的完整信息

    参数：
        username (str): 用户输入的账号
        password (str): 用户输入的密码
        role (str): 用户选择的角色

    返回值：
        bool: 验证结果（True=匹配成功，False=匹配失败）
    """
    # 加载最新的用户数据
    df_users = load_user_data()

    # 布尔索引筛选：同时匹配账号、密码、角色的记录
    # 注：pandas布尔索引会返回所有满足条件的行
    match_records = df_users[
        (df_users['username'] == username) &  # 账号匹配
        (df_users['password'] == password) &  # 密码匹配
        (df_users['role'] == role)  # 角色匹配
        ]

    # 判断是否存在匹配记录：非空则验证通过（True），空则失败（False）
    return not match_records.empty


def get_all_roles() -> list:
    """
    获取系统中所有可用的角色列表（去重）
    用于登录页面的角色下拉框渲染

    返回值：
        list: 角色名称列表（如["Admin", "产品设计工程师"...]）
    """
    # 加载用户数据
    df_users = load_user_data()
    # 检查DataFrame是否包含role列（避免KeyError）
    if 'role' in df_users.columns:
        # 去重并转换为列表（unique()去重，tolist()转列表）
        return df_users['role'].unique().tolist()
    # 无role列时返回空列表
    return []


# ========================= 权限校验扩展函数 =========================
def check_login_status() -> bool:
    """
    检查用户当前登录状态（基于Streamlit会话状态）
    用于页面权限控制：未登录用户无法访问系统功能

    返回值：
        bool: 登录状态（True=已登录，False=未登录）
    """
    # get方法避免KeyError：无logged_in键时默认返回False
    return st.session_state.get("logged_in", False)


def check_permission(required_roles: list) -> bool:
    """
    细粒度权限校验：检查当前用户是否拥有指定角色权限
    用于功能模块的权限控制（如仅管理员可访问配置页）

    参数：
        required_roles (list): 所需角色列表（如["Admin", "产品设计工程师"]）

    返回值：
        bool: 权限检查结果（True=有权限，False=无权限）
    """
    # 前置校验：未登录用户直接无权限
    if not check_login_status():
        return False

    # 校验当前用户角色是否在所需角色列表中
    return st.session_state.current_user["role"] in required_roles