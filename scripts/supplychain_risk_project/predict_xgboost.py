import pandas as pd
import xgboost as xgb
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score, log_loss
from sqlalchemy import create_engine
import os
import joblib
import matplotlib
matplotlib.use('Agg')

# --- 1. 数据库连接配置 ---
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')
db_url = f"postgresql://{user}:{password}@{host}:5432/{db_name}"
engine = create_engine(db_url)

# --- 2. 数据读取 (一次性加载) ---
SCHEMA_NAME = "supplychainrisk"
TABLE_NAME = "datacosupplychaindataset"

# 仅选择关键变量，避免内存污染
query = f"""
    SELECT "Type", "Shipping Mode", "Market", "Days for shipment (scheduled)","order date (DateOrders)","Late_delivery_risk"
    FROM {SCHEMA_NAME}.{TABLE_NAME}
"""
df = pd.read_sql(query, engine)
df['order_hour'] = pd.to_datetime(df['order date (DateOrders)']).dt.hour

# --- 3. 特征工程 ---
features = ['Type', 'Shipping Mode', 'Market', 'Days for shipment (scheduled)','order_hour']
target = 'Late_delivery_risk'

# 独热编码 (One-Hot Encoding)
X = pd.get_dummies(df[features], columns=['Type', 'Shipping Mode', 'Market','order_hour'])
y = df[target]

# --- 4. 三折法数据切分 (Train: 60%, Val: 20%, Test: 20%) ---
# 第一次切分：留出 20% 最终测试集
X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 第二次切分：从剩余 80% 中切出 25% 作为验证集 (即总体的 20%)
X_train, X_val, y_train, y_val = train_test_split(X_temp, y_temp, test_size=0.25, random_state=42)

# --- 5. 模型定义与训练 ---
model = xgb.XGBClassifier(
    objective='binary:logistic',
    n_estimators=200,      # 增加迭代次数
    learning_rate=0.05,    # 降低步长提高精度
    max_depth=6,
    eval_metric='logloss',
    early_stopping_rounds=10 # 如果验证集损失不再下降则提前停止
)

model.fit(
    X_train, y_train,
    eval_set=[(X_val, y_val)],
    verbose=False
)

# --- 6. 模型评估 (验证集) ---
val_probs = model.predict_proba(X_test)[:, 1]
val_preds = model.predict(X_test)

metrics = {
    "Accuracy": accuracy_score(y_test, val_preds),
    "ROC-AUC": roc_auc_score(y_test, val_probs),
    "LogLoss": log_loss(y_test, val_probs)
}

print("\n" + "="*40)
print("📊 最终模型评估报告 (测试集)")
print("="*40)
for k, v in metrics.items():
    print(f"{k:<10}: {v:.4f}")
print("="*40)


# 1. 指定非交互式后端 (防止报错)
import matplotlib
matplotlib.use('Agg') 

# 2. 绘图
fig, ax = plt.subplots(figsize=(10, 8))
xgb.plot_importance(model, ax=ax)

# 3. 保存而不是 show
plt.savefig('feature_importance.png', dpi=300, bbox_inches='tight')
print("✅ 特征重要性图表已保存为 feature_importance.png")
# --- 7. 模型持久化 ---
joblib.dump(model, 'xgboost_delivery_model.pkl')
joblib.dump(X.columns.tolist(), 'model_features.pkl')

print("\n✅ 模型及特征列表已保存。")