import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import os
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder

# --- 1. 数据库连接 ---
engine = create_engine(f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:5432/{os.getenv('DB_NAME')}")
SCHEMA_NAME = "ecommerce_logistics"

# --- 2. 核心 SQL (增加卖家发货延迟计算) ---
query = f"""
WITH items_agg AS (
    SELECT 
        oi.order_id,
        SUM(oi.price) as total_price,
        SUM(oi.freight_value) as total_freight,
        COUNT(oi.order_item_id) as total_items,
        SUM(p.product_weight_g) as total_weight,
        AVG(p.product_photos_qty) as avg_photos_qty,
        MAX(p.product_category_name) as raw_category,
        MAX(oi.seller_id) as main_seller_id,
        -- 新增：计算卖家发货限期与交给物流商时间之差 (即卖家发货延迟)
        -- 注意：这里需要聚合，我们取该订单内最晚的限期值
        MAX(oi.shipping_limit_date) as max_shipping_limit
    FROM {SCHEMA_NAME}.olist_order_items_dataset oi
    LEFT JOIN {SCHEMA_NAME}.olist_products_dataset p ON oi.product_id = p.product_id
    GROUP BY 1
),
pay_agg AS (
    SELECT order_id, MAX(payment_type) as primary_payment_type, MAX(payment_installments) as max_installments
    FROM {SCHEMA_NAME}.olist_order_payments_dataset GROUP BY 1
)
SELECT 
    o.order_id,
    o.order_purchase_timestamp,
    o.order_delivered_customer_date,
    o.order_estimated_delivery_date,
    o.order_delivered_carrier_date, -- 新增：传给物流商的时间
    i.max_shipping_limit,           -- 新增：卖家最晚发货限期
    r.review_score,
    COALESCE(t.product_category_name_english, i.raw_category) as category_english,
    i.total_price, i.total_freight, i.total_items, i.total_weight, i.avg_photos_qty,
    pa.primary_payment_type, pa.max_installments,
    c.customer_state, s.seller_state
FROM {SCHEMA_NAME}.olist_orders_dataset o
JOIN {SCHEMA_NAME}.olist_order_reviews_dataset r ON o.order_id = r.order_id
INNER JOIN items_agg i ON o.order_id = i.order_id
LEFT JOIN pay_agg pa ON o.order_id = pa.order_id
LEFT JOIN {SCHEMA_NAME}.olist_customers_dataset c ON o.customer_id = c.customer_id
LEFT JOIN {SCHEMA_NAME}.olist_sellers_dataset s ON i.main_seller_id = s.seller_id
LEFT JOIN {SCHEMA_NAME}.product_category_name_translation t ON i.raw_category = t.product_category_name
WHERE o.order_status = 'delivered';
"""

df = pd.read_sql(query, engine)

# --- 3. 特征工程 (加入新字段逻辑) ---
def run_engineering(df):
    df = df.copy()
    time_cols = ['order_purchase_timestamp', 'order_delivered_customer_date', 
                 'order_estimated_delivery_date', 'order_delivered_carrier_date', 'max_shipping_limit']
    for col in time_cols:
        df[col] = pd.to_datetime(df[col])
    
    # 过滤核心缺失值
    df = df.dropna(subset=['order_delivered_customer_date', 'order_delivered_carrier_date']).copy()
    
    # A. 配送天数指标
    df['actual_days'] = (df['order_delivered_customer_date'] - df['order_purchase_timestamp']).dt.days
    df['delay_days'] = (df['order_delivered_customer_date'] - df['order_estimated_delivery_date']).dt.days
    
    # B. 新增特征：卖家发货延迟天数 (shipping_limit - delivered_carrier)
    # 根据你的逻辑：limit 减去 carrier，如果结果为负，说明卖家早于限期交货
    df['seller_ship_delay_days'] = (df['order_delivered_carrier_date']-df['max_shipping_limit']).dt.days
    
    # C. 业务洞察：7天心理阈值标记 (参考报告 x=7 结论)
    df['is_late_over_7'] = (df['delay_days'] > 7).astype(int)
    
    # D. 财务与属性
    df['freight_ratio'] = df['total_freight'] / (df['total_price'] + df['total_freight'] + 0.1)
    
    # 填充其余小额缺失值
    for col in ['total_weight', 'avg_photos_qty']:
        df[col] = df[col].fillna(df[col].median())
        
    cat_cols = ['category_english', 'customer_state', 'seller_state', 'primary_payment_type']
    for col in cat_cols:
        df[col] = df[col].fillna('unknown')
        df[col] = LabelEncoder().fit_transform(df[col].astype(str))
    
    df['target'] = (df['review_score'] <= 2).astype(int)
    return df

df_ml = run_engineering(df)

# --- 4. 训练与阈值调整 ---
features = ['actual_days', 'delay_days', 'seller_ship_delay_days','is_late_over_7',
            'total_items', 'total_weight', 'freight_ratio', 'category_english', 
            'customer_state', 'seller_state', 'primary_payment_type', 'max_installments']

X = df_ml[features]
y = df_ml['target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

model = XGBClassifier(n_estimators=100, learning_rate=0.1, max_depth=6, 
                      scale_pos_weight=(len(y)-y.sum())/y.sum(), eval_metric='logloss')
model.fit(X_train, y_train)

# --- 5. 解决“虚警”：调整阈值为 0.7 ---
# 默认 predict() 使用 0.5 阈值，这里我们手动获取概率
probs = model.predict_proba(X_test)[:, 1] 
custom_preds = (probs > 0.7).astype(int) # 只有概率大于 0.7 才判定为差评

print("\n--- 调整后的模型报告 (Threshold = 0.7) ---")
print(classification_report(y_test, custom_preds))

importance = pd.DataFrame({'f': features, 'i': model.feature_importances_}).sort_values('i', ascending=False)
print("\nTop Features:")
print(importance)