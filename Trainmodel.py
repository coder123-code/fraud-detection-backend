import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report

from lightgbm import LGBMClassifier


# Load Dataset


df = pd.read_csv(
    "fraudTrain.csv",
    low_memory=False
)

print("Dataset Loaded:", df.shape)

# ==========================
# Feature Engineering
# ==========================

df["trans_date_trans_time"] = pd.to_datetime(
    df["trans_date_trans_time"]
)

# Late Night Feature

df["is_late_night"] = (
    (df["trans_date_trans_time"].dt.hour <= 5)
    |
    (df["trans_date_trans_time"].dt.hour >= 23)
).astype(int)

# Category Encoding

le_category = LabelEncoder()

df["category_encoded"] = le_category.fit_transform(
    df["category"]
)

# Rolling Amount Feature

df["rolling_30d_amt"] = (
    df["amt"]
    .rolling(window=30, min_periods=1)
    .mean()
)

# Distance Feature
# Original implementation unknown.
# Most likely placeholder.

df["distance_from_prev_txn"] = 0.0

# ==========================
# Features
# ==========================

features = [
    "amt",
    "is_late_night",
    "rolling_30d_amt",
    "distance_from_prev_txn",
    "category_encoded"
]

X = df[features]

y = df["is_fraud"]

# ==========================
# Split Data
# ==========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# ==========================
# Train Model
# ==========================

model = LGBMClassifier(
    learning_rate=0.05,
    max_depth=10,
    n_estimators=150,
    random_state=42,
    reg_alpha=0.1,
    reg_lambda=0.1,
    scale_pos_weight=100
)

print("Training Model...")

model.fit(
    X_train,
    y_train
)

# ==========================
# Evaluation
# ==========================

pred = model.predict(X_test)

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        pred
    )
)

# ==========================
# Save Model
# ==========================

joblib.dump(
    {
        "model": model,
        "le_category": le_category,
        "features": features
    },
    "fraud_detector_model_fixed.pkl"
)

print("\nModel Saved Successfully!")
