import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os
SCHEMA_NAME = "berlin_sbahn"
# 1. 设置页面标题（这会在浏览器标签页显示）
st.set_page_config(page_title="S-Bahn Data Health Check", layout="wide")

st.title("📊 柏林 S-Bahn 数据体检仪表盘")
st.markdown("这是从 PostgreSQL 数据库实时提取的元数据报告。")

# 数据库连接逻辑 (保持不变)
def get_engine():
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST')
    db_name = os.getenv('DB_NAME')
    url = f"postgresql://{user}:{password}@{host}:5432/{db_name}"
    return create_engine(url)

# 获取数据的逻辑
@st.cache_data # Streamlit 缓存机制，避免每次刷新页面都去查数据库
def load_health_data():
    engine = get_engine()
    # 这里运行你之前的元数据逻辑，为了演示，我们假设它返回那个 final_report DataFrame
    # 也可以直接读取你生成的 data_health_report.csv
    return pd.read_csv("data_health_report.csv")

try:
    df = load_health_data()

    # 2. 增加侧边栏过滤器
    st.sidebar.header("过滤器")
    selected_table = st.sidebar.multiselect("选择查看的表", options=df['Table'].unique(), default=df['Table'].unique())
    
    filtered_df = df[df['Table'].isin(selected_table)]

    # 3. 展示核心指标卡片 (Metrics)
    col1, col2, col3 = st.columns(3)
    col1.metric("总表数", len(df['Table'].unique()))
    col2.metric("总字段数", len(df))
    col3.metric("平均缺失率", f"{df['Null Percentage'].mean():.2f}%")

    # 4. 展示数据表格
    st.subheader("详细列元数据")
    st.dataframe(filtered_df, width="stretch")

    # 5. 在 Streamlit 中添加这段，看看延误的严重程度
    st.divider()
    st.subheader("⏰ 延误分钟数分布 (实时采样)")

    if 'trips' in selected_table:
        try:
            # 1. 重新获取数据库连接
            engine = get_engine() 
            
            # 2. 只读取 trips 表的延误列，LIMIT 5000 保证网页飞快
            query = f"SELECT delay_minutes FROM {SCHEMA_NAME}.trips WHERE is_delayed = True LIMIT 5000"
            delay_data = pd.read_sql(query, engine)
            
            if not delay_data.empty:
                # 3. 计算分布并画图
                # 我们用 value_counts 看看 1分钟、2分钟...各有多少次
                dist = delay_data['delay_minutes'].value_counts().sort_index().head(20)
                st.bar_chart(dist)
                st.caption("注：此处展示前 5000 条已延误班次的延误时长分布（分钟）")
            else:
                st.write("目前没有延误数据。")
                
        except Exception as e:
            st.error(f"提取延误数据失败: {e}")
    
    # 6. 在 Streamlit 中添加这段，看看延误的严重程度
    with st.expander("🔍 深度分析：天气与延误的关联"):
        # 这条 SQL 直接在数据库里对齐时间并计算
        join_query = f"""
        SELECT 
            w.weather_condition, 
            AVG(t.delay_minutes) as avg_delay
        FROM {SCHEMA_NAME}.trips t
        JOIN {SCHEMA_NAME}.weather w 
        ON DATE_TRUNC('hour', t.scheduled_departure_time::timestamp) = w.timestamp::timestamp
        GROUP BY w.weather_condition
        """
        analysis_df = pd.read_sql(join_query, engine)
        st.write("不同天气下的平均延误时间：")
        st.table(analysis_df)

except Exception as e:
    st.error(f"连接数据库失败: {e}")