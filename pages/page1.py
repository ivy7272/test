"""
数据管理页面 - 示例页面
========================
功能概述：
    1. 展示如何使用认证模块进行权限控制
    2. 展示如何使用配置模块管理设置
    3. 展示数据CRUD操作（增删改查）
    4. 展示数据可视化功能
    5. 展示文件上传下载功能
"""
import streamlit as st
import pandas as pd
import logging
import os
from datetime import datetime
from src.auth.auth import check_permission, check_login_status
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

# 示例数据文件路径
SAMPLE_DATA_FILE = os.path.join(Config.DATA_DIR, "sample_data.csv")


def load_sample_data():
    """加载示例数据"""
    try:
        if os.path.exists(SAMPLE_DATA_FILE):
            return pd.read_csv(SAMPLE_DATA_FILE)
        else:
            # 创建默认示例数据
            default_data = pd.DataFrame({
                "ID": range(1, 11),
                "产品名称": [f"产品_{i}" for i in range(1, 11)],
                "产品类型": ["电子", "机械", "电子", "机械", "电子", "机械", "电子", "机械", "电子", "机械"],
                "数量": [10, 20, 15, 25, 30, 12, 18, 22, 28, 35],
                "单价": [100.0, 200.0, 150.0, 250.0, 300.0, 120.0, 180.0, 220.0, 280.0, 350.0],
                "创建时间": [datetime.now().strftime("%Y-%m-%d")] * 10,
                "状态": ["正常", "正常", "停用", "正常", "正常", "停用", "正常", "正常", "正常", "停用"]
            })
            default_data.to_csv(SAMPLE_DATA_FILE, index=False)
            return default_data
    except Exception as e:
        logger.error(f"加载示例数据失败: {e}")
        return pd.DataFrame()


def save_sample_data(df):
    """保存示例数据"""
    try:
        df.to_csv(SAMPLE_DATA_FILE, index=False)
        logger.info("示例数据保存成功")
        return True
    except Exception as e:
        logger.error(f"保存示例数据失败: {e}")
        return False


def show_data_management_page():
    """渲染数据管理页面"""
    try:
        # 页面标题
        st.title("📋 数据管理示例")
        st.markdown("---")
        
        # 获取当前用户信息
        current_user = st.session_state.get("current_user", {})
        username = current_user.get("username", "未知用户")
        role = current_user.get("role", "未知角色")
        
        # 显示当前用户信息
        st.markdown(f"**当前用户：** {username} | **角色：** {role}")
        st.markdown("---")
        
        # 权限检查示例
        st.markdown("### 🔐 权限控制演示")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # 检查是否已登录
            if check_login_status():
                st.success("✅ 已登录")
            else:
                st.error("❌ 未登录")
        
        with col2:
            # 检查是否有管理员权限
            if check_permission(["Admin"]):
                st.success("✅ 管理员权限")
            else:
                st.info("ℹ️ 普通用户权限")
        
        with col3:
            # 检查是否有工程师权限
            if check_permission(["产品设计工程师", "工艺工程师"]):
                st.success("✅ 工程师权限")
            else:
                st.info("ℹ️ 非工程师权限")
        
        st.markdown("---")
        
        # 配置信息展示
        st.markdown("### ⚙️ 配置信息演示")
        
        with st.expander("点击查看系统配置"):
            st.markdown(f"**应用名称：** {Config.APP_NAME}")
            st.markdown(f"**应用图标：** {Config.APP_ICON}")
            st.markdown(f"**数据目录：** {Config.DATA_DIR}")
            st.markdown(f"**日志文件：** {Config.LOG_FILE}")
            st.markdown(f"**用户数据文件：** {Config.USER_DATA_FILE}")
            st.markdown(f"**会话过期时间：** {Config.SESSION_EXPIRY}秒")
        
        st.markdown("---")
        
        # 数据管理功能
        st.markdown("### 📊 数据管理功能")
        
        # 加载数据
        df = load_sample_data()
        
        if df.empty:
            st.error("数据加载失败")
            return
        
        # 数据筛选
        st.markdown("#### 🔍 数据筛选")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # 按产品类型筛选
            product_types = df["产品类型"].unique().tolist()
            selected_type = st.selectbox("选择产品类型", ["全部"] + product_types)
        
        with col2:
            # 按状态筛选
            status_list = df["状态"].unique().tolist()
            selected_status = st.selectbox("选择状态", ["全部"] + status_list)
        
        with col3:
            # 搜索功能
            search_term = st.text_input("搜索产品名称", placeholder="输入关键词")
        
        # 应用筛选
        filtered_df = df.copy()
        if selected_type != "全部":
            filtered_df = filtered_df[filtered_df["产品类型"] == selected_type]
        if selected_status != "全部":
            filtered_df = filtered_df[filtered_df["状态"] == selected_status]
        if search_term:
            filtered_df = filtered_df[filtered_df["产品名称"].str.contains(search_term, case=False, na=False)]
        
        # 显示筛选结果
        st.markdown(f"**显示 {len(filtered_df)} 条记录（共 {len(df)} 条）**")
        
        # 数据表格
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # 数据操作（需要管理员权限）
        st.markdown("### ✏️ 数据操作")
        
        if check_permission(["Admin"]):
            st.success("您有权限进行数据操作")
            
            tab1, tab2, tab3 = st.tabs(["添加数据", "编辑数据", "删除数据"])
            
            with tab1:
                st.markdown("#### ➕ 添加新数据")
                with st.form("add_data_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        new_name = st.text_input("产品名称", placeholder="输入产品名称")
                        new_type = st.selectbox("产品类型", ["电子", "机械"])
                        new_quantity = st.number_input("数量", min_value=1, value=1)
                    
                    with col2:
                        new_price = st.number_input("单价", min_value=0.0, value=100.0, step=10.0)
                        new_status = st.selectbox("状态", ["正常", "停用"])
                    
                    submit_add = st.form_submit_button("添加数据", type="primary")
                    
                    if submit_add:
                        if new_name:
                            # 生成新ID
                            new_id = df["ID"].max() + 1 if not df.empty else 1
                            
                            # 添加新行
                            new_row = pd.DataFrame({
                                "ID": [new_id],
                                "产品名称": [new_name],
                                "产品类型": [new_type],
                                "数量": [new_quantity],
                                "单价": [new_price],
                                "创建时间": [datetime.now().strftime("%Y-%m-%d")],
                                "状态": [new_status]
                            })
                            
                            df = pd.concat([df, new_row], ignore_index=True)
                            
                            if save_sample_data(df):
                                st.success(f"✅ 产品 '{new_name}' 添加成功！")
                                logger.info(f"用户 {username} 添加新产品: {new_name}")
                                st.rerun()
                            else:
                                st.error("❌ 数据保存失败")
                        else:
                            st.error("❌ 请输入产品名称")
            
            with tab2:
                st.markdown("#### 📝 编辑数据")
                
                # 选择要编辑的记录
                edit_id = st.selectbox("选择要编辑的产品ID", df["ID"].tolist())
                
                if edit_id:
                    edit_row = df[df["ID"] == edit_id].iloc[0]
                    
                    with st.form("edit_data_form"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            edit_name = st.text_input("产品名称", value=edit_row["产品名称"])
                            edit_type = st.selectbox("产品类型", ["电子", "机械"], 
                                                   index=0 if edit_row["产品类型"] == "电子" else 1)
                            edit_quantity = st.number_input("数量", min_value=1, 
                                                          value=int(edit_row["数量"]))
                        
                        with col2:
                            edit_price = st.number_input("单价", min_value=0.0, 
                                                       value=float(edit_row["单价"]), step=10.0)
                            edit_status = st.selectbox("状态", ["正常", "停用"],
                                                     index=0 if edit_row["状态"] == "正常" else 1)
                        
                        submit_edit = st.form_submit_button("保存修改", type="primary")
                        
                        if submit_edit:
                            # 更新数据
                            df.loc[df["ID"] == edit_id, "产品名称"] = edit_name
                            df.loc[df["ID"] == edit_id, "产品类型"] = edit_type
                            df.loc[df["ID"] == edit_id, "数量"] = edit_quantity
                            df.loc[df["ID"] == edit_id, "单价"] = edit_price
                            df.loc[df["ID"] == edit_id, "状态"] = edit_status
                            
                            if save_sample_data(df):
                                st.success(f"✅ 产品 '{edit_name}' 修改成功！")
                                logger.info(f"用户 {username} 修改产品: {edit_name}")
                                st.rerun()
                            else:
                                st.error("❌ 数据保存失败")
            
            with tab3:
                st.markdown("#### 🗑️ 删除数据")
                
                # 选择要删除的记录
                delete_id = st.selectbox("选择要删除的产品ID", df["ID"].tolist(), key="delete_select")
                
                if delete_id:
                    delete_row = df[df["ID"] == delete_id].iloc[0]
                    st.warning(f"⚠️ 确定要删除产品 '{delete_row['产品名称']}' 吗？")
                    
                    if st.button("确认删除", type="primary"):
                        # 删除数据
                        df = df[df["ID"] != delete_id].reset_index(drop=True)
                        
                        if save_sample_data(df):
                            st.success(f"✅ 产品 '{delete_row['产品名称']}' 删除成功！")
                            logger.info(f"用户 {username} 删除产品: {delete_row['产品名称']}")
                            st.rerun()
                        else:
                            st.error("❌ 数据保存失败")
        else:
            st.info("🔒 数据操作功能需要管理员权限")
        
        st.markdown("---")
        
        # 数据可视化
        st.markdown("### 📈 数据可视化")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 产品类型分布")
            type_counts = filtered_df["产品类型"].value_counts()
            st.bar_chart(type_counts)
        
        with col2:
            st.markdown("#### 状态分布")
            status_counts = filtered_df["状态"].value_counts()
            st.bar_chart(status_counts)
        
        # 数据统计
        st.markdown("#### 📊 数据统计")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("总产品数", len(filtered_df))
        
        with col2:
            total_quantity = filtered_df["数量"].sum()
            st.metric("总数量", int(total_quantity))
        
        with col3:
            total_value = (filtered_df["数量"] * filtered_df["单价"]).sum()
            st.metric("总价值", f"¥{total_value:,.2f}")
        
        with col4:
            avg_price = filtered_df["单价"].mean()
            st.metric("平均单价", f"¥{avg_price:,.2f}")
        
        st.markdown("---")
        
        # 文件操作
        st.markdown("### 📁 文件操作")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📥 导出数据")
            
            # 准备导出数据
            csv = filtered_df.to_csv(index=False).encode('utf-8')
            
            st.download_button(
                label="下载CSV文件",
                data=csv,
                file_name=f"产品数据_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            st.markdown("#### 📤 导入数据")
            
            # 权限检查
            if check_permission(["Admin"]):
                uploaded_file = st.file_uploader("上传CSV文件", type=['csv'])
                
                if uploaded_file is not None:
                    try:
                        # 读取上传的文件
                        uploaded_df = pd.read_csv(uploaded_file)
                        
                        # 显示预览
                        st.markdown("**数据预览：**")
                        st.dataframe(uploaded_df.head(), use_container_width=True, hide_index=True)
                        
                        if st.button("确认导入", type="primary"):
                            # 合并数据
                            df = pd.concat([df, uploaded_df], ignore_index=True)
                            
                            if save_sample_data(df):
                                st.success(f"✅ 成功导入 {len(uploaded_df)} 条记录！")
                                logger.info(f"用户 {username} 导入数据: {len(uploaded_df)} 条")
                                st.rerun()
                            else:
                                st.error("❌ 数据导入失败")
                    except Exception as e:
                        st.error(f"❌ 文件读取失败: {e}")
                        logger.error(f"文件导入失败: {e}")
            else:
                st.info("🔒 导入功能需要管理员权限")
        
        st.markdown("---")
        
        # 日志查看（仅管理员）
        st.markdown("### 📝 操作日志")
        
        if check_permission(["Admin"]):
            if st.button("查看最近日志", use_container_width=True):
                try:
                    if os.path.exists(Config.LOG_FILE):
                        with open(Config.LOG_FILE, 'r', encoding='utf-8') as f:
                            logs = f.readlines()
                            # 显示最后20行日志
                            recent_logs = logs[-20:] if len(logs) > 20 else logs
                            st.code(''.join(recent_logs), language='text')
                    else:
                        st.info("暂无日志文件")
                except Exception as e:
                    st.error(f"读取日志失败: {e}")
        else:
            st.info("🔒 日志查看需要管理员权限")
        
        # 记录页面访问日志
        logger.info(f"用户 {username} 访问数据管理页面")
        
    except Exception as e:
        logger.error(f"数据管理页面加载错误: {e}")
        st.error("页面加载失败，请刷新重试")


# 页面入口
if __name__ == "__main__":
    show_data_management_page()