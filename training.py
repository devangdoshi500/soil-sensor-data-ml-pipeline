from pathlib import Path
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from config import OUTPUT_DIR, CLEAN_CSV_NAME, MODEL_NAME

FEATURES = ["AirTemp", "AirHumidity", "SoilTemp", "SoilMoisture", "EC", "pH", "N", "P", "K"]
def train_random_forest(df: pd.DataFrame,
                        test_size: float = 0.2,
                        random_state: int = 5812):
    X = df[FEATURES]
    y = df["SoilHealth"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    rf = RandomForestRegressor(
        n_estimators=300,
        max_depth=None,
        min_samples_split=2,
        min_samples_leaf=1,
        random_state=random_state,
        n_jobs=-1
    )
    rf.fit(X_train, y_train)
    y_pred = rf.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2  = r2_score(y_test, y_pred)
    return rf, mae, r2

def save_outputs(df_labeled: pd.DataFrame, model, out_dir: Path = OUTPUT_DIR):
    out_dir.mkdir(parents=True, exist_ok=True)
    df_labeled.to_csv(out_dir / CLEAN_CSV_NAME, index=False)
    joblib.dump(model, out_dir / MODEL_NAME)
    return (out_dir / CLEAN_CSV_NAME, out_dir / MODEL_NAME)