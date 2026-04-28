"""
首页 - 系统仪表盘
========================
功能概述：
    1. 展示系统概览和统计数据
    2. 显示当前登录用户信息
    3. 提供快速导航和功能入口
    4. 展示系统状态和通知
"""
import streamlit as st
import pandas as pd
import logging
from datetime import datetime, timedelta
from src.auth.auth import check_permission, get_all_roles
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


def show_home_page():
    """渲染首页内容"""
    try:
        # 页面标题
        st.title(f"{Config.APP_ICON} {Config.APP_NAME}")
        st.markdown("---")
        
        # 获取当前用户信息
        current_user = st.session_state.get("current_user", {})
        username = current_user.get("username", "未知用户")
        role = current_user.get("role", "未知角色")
        
        # 欢迎信息
        st.markdown(f"### 👋 欢迎回来，{username}！")
        st.markdown(f"**当前角色：** {role}")
        st.markdown(f"**登录时间：** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        st.markdown("---")
        
        # 系统概览统计
        st.markdown("### 📊 系统概览")
        
        # 创建统计卡片
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="总用户数",
                value="4",
                delta="+0"
            )
        
        with col2:
            st.metric(
                label="在线用户",
                value="1",
                delta="+1"
            )
        
        with col3:
            st.metric(
                label="系统运行时间",
                value="正常",
                delta="✓"
            )
        
        with col4:
            st.metric(
                label="数据文件",
                value="已连接",
                delta="✓"
            )
        
        st.markdown("---")
        
        # 快速功能入口
        st.markdown("### 🚀 快速入口")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            with st.container(border=True):
                st.markdown("#### 📋 数据管理")
                st.markdown("管理BOM数据、查看数据详情")
                if st.button("进入数据管理", key="goto_data", use_container_width=True):
                    st.info("请使用左侧导航栏进入数据管理页面")
        
        with col2:
            with st.container(border=True):
                st.markdown("#### 📈 数据可视化")
                st.markdown("查看数据统计图表和趋势分析")
                if st.button("查看图表", key="goto_charts", use_container_width=True):
                    st.info("请使用左侧导航栏进入数据可视化页面")
        
        with col3:
            with st.container(border=True):
                st.markdown("#### ⚙️ 系统设置")
                st.markdown("配置系统参数和用户管理")
                # 权限控制示例：仅管理员可见
                if check_permission(["Admin"]):
                    if st.button("系统设置", key="goto_settings", use_container_width=True):
                        st.info("系统设置功能开发中...")
                else:
                    st.info("🔒 需要管理员权限")
        
        st.markdown("---")
        
        # 用户角色分布
        st.markdown("### 👥 用户角色分布")
        
        # 获取所有角色
        roles = get_all_roles()
        if roles:
            # 创建角色分布数据
            role_data = {
                "角色": roles,
                "用户数": [1] * len(roles),  # 示例数据
                "权限级别": ["高" if r == "Admin" else "中" if "工程师" in r else "低" for r in roles]
            }
            df_roles = pd.DataFrame(role_data)
            st.dataframe(df_roles, use_container_width=True, hide_index=True)
        else:
            st.info("暂无角色数据")
        
        st.markdown("---")
        
        # 系统公告
        st.markdown("### 📢 系统公告")
        
        with st.container(border=True):
            st.markdown("**🎉 欢迎使用BOM管理系统！**")
            st.markdown("- 系统已更新至v1.0版本")
            st.markdown("- 新增用户认证和权限管理功能")
            st.markdown("- 优化了页面加载速度和用户体验")
            st.markdown(f"- **当前时间：** {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")
        
        st.markdown("---")
        
        # 使用帮助
        st.markdown("### ❓ 使用帮助")
        
        with st.expander("点击查看使用指南"):
            st.markdown("""
            **1. 导航使用**
            - 使用左侧导航栏切换不同功能页面
            - 点击页面名称即可进入对应功能模块
            
            **2. 权限说明**
            - **Admin**：系统管理员，拥有所有权限
            - **产品设计工程师**：负责EBOM管理
            - **工艺工程师**：负责PBOM管理
            - **生产人员**：负责MBOM和订单管理
            
            **3. 数据管理**
            - 所有数据变更都会自动保存
            - 支持Excel文件导入导出
            - 操作日志会记录在系统中
            
            **4. 安全提示**
            - 请妥善保管您的账号密码
            - 离开座位时请注销登录
            - 发现异常请及时联系管理员
            """)
        
        # 记录页面访问日志
        logger.info(f"用户 {username} 访问首页")
        
    except Exception as e:
        logger.error(f"首页加载错误: {e}")
        st.error("页面加载失败，请刷新重试")


# 页面入口
if __name__ == "__main__":
    show_home_page()