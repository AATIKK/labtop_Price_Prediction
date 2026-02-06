import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import joblib

# Load your dataset
df = pd.read_csv("data/laptops.csv")

# Example feature extraction - adjust to your dataset columns
df = df.dropna(subset=["price_usd", "brand", "ram_gb", "storage_gb", "cpu"])
X = df[["brand", "cpu", "ram_gb", "storage_type", "storage_gb", "gpu", "screen_size_in", "os", "age_years", "condition"]]
y = df["price_usd"]

# Simple preprocessing
categorical = ["brand", "cpu", "storage_type", "gpu", "os", "condition"]
numeric = ["ram_gb", "storage_gb", "screen_size_in", "age_years"]

preprocessor = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="ignore", sparse=False), categorical),
    ("num", StandardScaler(), numeric),
])

model = Pipeline([
    ("pre", preprocessor),
    ("rf", RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1))
])

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
model.fit(X_train, y_train)

pred = model.predict(X_val)
print("MAE:", mean_absolute_error(y_val, pred))

# Save pipeline
joblib.dump(model, "backend/model.joblib")
print("Saved model to backend/model.joblib")
