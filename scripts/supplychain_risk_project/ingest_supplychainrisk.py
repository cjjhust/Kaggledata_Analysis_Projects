import pandas as pd
import os
import sys
from sqlalchemy import create_engine, text

def ingest_supplychainrisk():
    # --- 1. 项目配置（路径写死，确保准确性） ---
    PROJECT_NAME = "supplychainrisk"
    DATA_DIR = "/app/data_raw/supply_chain_risk"  # 确保这个路径在 Docker 中正确挂载了数据
    
    # --- 2. 严格的数据库连接检查 ---
    # 仅从环境变量获取，不设置任何备选默认值
    # 变量已经在容器的环境变量里了，直接拿
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST') # 容器内连数据库通常用 service 名，比如 'db'
    db_name = os.getenv('DB_NAME')

    # 依然可以动态合成 URL
    db_url = f"postgresql://{user}:{password}@{host}:5432/{db_name}"
    
    
    if not db_url:
        print("❌ 运行失败：未检测到环境变量 [DB_URL]！")
        print("💡 安全提示：请在运行环境或 .env 文件中设置 DB_URL，不要将密码写在代码中。")
        print("示例：export DB_URL='postgresql://user:password@host:port/dbname'")
        sys.exit(1) # 直接异常退出

    # --- 3. 路径存在性检查 ---
    if not os.path.exists(DATA_DIR):
        print(f"❌ 运行失败：找不到数据目录 {DATA_DIR}，请检查 Docker 挂载。")
        sys.exit(1)

    engine = create_engine(db_url)
    
    # --- 4. 数据库 Schema 初始化 ---
    try:
        with engine.connect() as conn:
            conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {PROJECT_NAME};"))
            conn.commit()
            print(f"🏗️  数据库 Schema [{PROJECT_NAME}] 已锁定。")
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        sys.exit(1)

    # --- 5. 扫描并导入 CSV ---
    files = [f for f in os.listdir(DATA_DIR) if f.endswith('.csv')]
    
    if not files:
        print(f"❓ 警告：目录 {DATA_DIR} 下没有 CSV 文件。")
        return

    for file in files:
        file_path = os.path.join(DATA_DIR, file)
        table_name = os.path.splitext(file)[0].lower()
        
        print(f"🚚 正在导入: {file} -> {PROJECT_NAME}.{table_name}")
        
        first_chunk = True
        try:
            # 分块读写以处理潜在的大数据量
            for chunk in pd.read_csv(file_path, chunksize=50000,encoding="latin-1"):
                mode = 'replace' if first_chunk else 'append'
                chunk.to_sql(
                    table_name, 
                    engine, 
                    schema=PROJECT_NAME, 
                    if_exists=mode, 
                    index=False
                )
                first_chunk = False
            print(f"   ✅ {table_name} 导入成功。")
        except Exception as e:
            print(f"   ❌ {table_name} 导入失败: {e}")

    print(f"\n✨ 项目 [{PROJECT_NAME}] 导入任务全部完成！")

if __name__ == "__main__":
    ingest_supplychainrisk()