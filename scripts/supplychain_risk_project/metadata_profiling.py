import pandas as pd
from sqlalchemy import create_engine, text
import os

# --- 1. 配置连接 (请确保与你的 .env 一致) ---
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST') # 容器内连数据库通常用 service 名，比如 'db'
db_name = os.getenv('DB_NAME')

# 依然可以动态合成 URL
db_url = f"postgresql://{user}:{password}@{host}:5432/{db_name}"
    
SCHEMA_NAME = "supplychainrisk"
engine = create_engine(db_url)

def get_metadata_report():
    # 2. 获取该 Schema 下的所有表名
    query_tables = text(f"""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = '{SCHEMA_NAME}';
    """)
    
    with engine.connect() as conn:
        tables = pd.read_sql(query_tables, conn)['table_name'].tolist()
        
    all_reports = []

    print(f"🚀 开始扫描 Schema: {SCHEMA_NAME} ...\n")

    for table in tables:
        print(f"📊 正在处理表: {table}")
        
        # 读取数据 (采样前 10000 行提高速度，或者全部读取)
        df = pd.read_sql(f"SELECT * FROM {SCHEMA_NAME}.{table}", engine)
        
        # 3. 核心统计逻辑
        report = pd.DataFrame({
            'Table': table,
            'Column': df.columns,
            'Dtype': df.dtypes.values,
            'Non-Null Count': df.notnull().sum().values,
            'Null Count': df.isnull().sum().values,
            'Null Percentage': (df.isnull().sum().values / len(df) * 100).round(2),
            'Unique Values': [df[col].nunique() for col in df.columns]
        })
        
        # 针对数值列增加统计
        all_reports.append(report)

    # 合并结果
    final_report = pd.concat(all_reports, ignore_index=True)
    
    # 4. 输出到控制台
    print("\n" + "="*50)
    print("📈 数据体检报告摘要")
    print("="*50)
    print(final_report.to_string(index=False))
    
    # 5. 保存为 CSV 供 Word/Power BI 使用
    final_report.to_csv("data_health_report.csv", index=False)
    print(f"\n✅ 报告已生成并保存为: data_health_report.csv")

if __name__ == "__main__":
    get_metadata_report()