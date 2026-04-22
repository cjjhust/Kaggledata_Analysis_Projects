import os
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import shap
import matplotlib.pyplot as plt
import seaborn as sns

# --- 1. 配置连接 (从你的配置读取) ---
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST') 
db_name = os.getenv('DB_NAME')
db_url = f"postgresql://{user}:{password}@{host}:5432/{db_name}"
SCHEMA_NAME = "db_network"

engine = create_engine(db_url)

def load_and_preprocess():
    # --- 2. SQL 数据提取 ---
    # 我们直接在 SQL 端计算 target 并提取时间小时，减轻 Python 压力
    query = f"""
    SELECT 
        state, 
        category,
        arrival_delay_m,
        departure_delay_m,
        (departure_delay_m - arrival_delay_m) as delay_diff,
        departure_plan -- 用于提取小时
    FROM {SCHEMA_NAME}.dbtrainrides
    WHERE departure_plan IS NOT NULL
    """
    
    print("正在从 PostgreSQL 提取数据...")
    df = pd.read_sql(query, engine)
    
    # --- 3. 特征工程 (Feature Engineering) ---
    print("正在进行特征工程...")
    
    # 转换时间：提取小时并进行周期性编码 (Circular Encoding)
    # 23点和0点在物理时间上是接近的，sin/cos转换能帮模型识别这一特性
    df['departure_plan'] = pd.to_datetime(df['departure_plan'])
    df['hour'] = df['departure_plan'].dt.hour
    df['hour_sin'] = np.sin(2 * np.pi * df['hour']/24)
    df['hour_cos'] = np.cos(2 * np.pi * df['hour']/24)
    
    # 州 (State) 的 One-hot 编码
    df = pd.get_dummies(df, columns=['state'], prefix='state')
    
    # 定义特征列和目标列
    # 注意：我们预测的是 delay_diff，不能把 departure_delay_m 放入特征，否则会发生标签泄露
    feature_cols = [col for col in df.columns if col.startswith('state_')] + \
                   ['category', 'hour_sin', 'hour_cos', 'arrival_delay_m']
    
    X = df[feature_cols]
    y = df['delay_diff']
    
    return train_test_split(X, y, test_size=0.2, random_state=42)

# --- 4. 训练 XGBoost 模型 ---
X_train, X_test, y_train, y_test = load_and_preprocess()

print(f"训练集大小: {X_train.shape}, 测试集大小: {X_test.shape}")

# 初始化模型：使用回归器预测连续的分钟增量
model = xgb.XGBRegressor(
    n_estimators=1000,
    learning_rate=0.05,
    max_depth=6,
    early_stopping_rounds=10,
    subsample=0.8,
    colsample_bytree=0.8,
    n_jobs=-1,
    random_state=42,
    tree_method='hist' # 针对大规模数据加速
)

print("模型训练中...")
model.fit(
    X_train, y_train,
    eval_set=[(X_test, y_test)],
    
    verbose=50
)

# --- 5. 模型评估 (Model Evaluation) ---
print("\n--- 模型评估报告 ---")
y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"RMSE (均方根误差): {rmse:.4f} min")
print(f"MAE  (平均绝对误差): {mae:.4f} min")
print(f"R2 Score (解释强度): {r2:.4f}")

# --- 6. 可视化与解释 (Insight Generation) ---
# 1. 特征重要性排序
print("正在生成特征重要性图...")
# 显式创建一个 figure，确保大小可控
fig, ax = plt.subplots(figsize=(10, 8))

# 调用 xgboost 的绘图函数，传入 ax 参数
xgb.plot_importance(model, max_num_features=15, importance_type='gain', ax=ax)

plt.title("XGBoost Feature Importance (Gain)")

# 导出图片
importance_output = "feature_importance_gain.png"
plt.savefig(importance_output, bbox_inches='tight', dpi=300)
plt.close() # 及时关闭，防止内存占用

print(f"✅ 特征重要性图已保存至: {os.getcwd()}/{importance_output}")

# 2. 偏差分析 (Residual Analysis)

print("正在生成偏差分析图 (Seaborn)...")
plt.figure(figsize=(10, 6))
# sns.regplot 会绘制散点图并自动拟合一条回归线
# 如果散点紧密围绕红线，说明预测非常准；如果红线平缓，说明模型倾向于低估极端延误
sns.regplot(x=y_test, y=y_pred, 
            scatter_kws={'alpha':0.3, 's':10, 'color':'blue'}, 
            line_kws={'color':'red', 'label':'Regression Line'})

plt.xlabel("Actual Delay Increment [min]")   # 真实延误增量
plt.ylabel("Predicted Delay Increment [min]") # 预测延误增量
plt.title("Actual vs Predicted - Model Bias Analysis")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)

# 远程环境必须保存为图片
plt.savefig("residual_analysis.png", bbox_inches='tight', dpi=300)
plt.close() 
print("✅ 偏差分析图已保存为: residual_analysis.png")

# 3. SHAP 解释 (深入了解特定变量如何推高延误)
print("计算 SHAP 值 (可能需要几分钟)...")
explainer = shap.TreeExplainer(model)
# 抽样 5000 条进行解释以节省计算资源
X_sample = X_test.sample(min(5000, len(X_test)), random_state=42)
shap_values = explainer.shap_values(X_sample)

#  创建绘图对象 (不显示窗口)
plt.figure(figsize=(12, 8))

# 绘制 Summary Plot
# 注意：show=False 必须加上，否则它会尝试打开窗口导致报错
shap.summary_plot(shap_values, X_sample, show=False)

# 导出图片到当前目录
output_file = "shap_summary_plot.png"
plt.savefig(output_file, bbox_inches='tight', dpi=300)
plt.close() # 释放内存

print(f"✅ SHAP 分析图已成功导出至: {os.getcwd()}/{output_file}")