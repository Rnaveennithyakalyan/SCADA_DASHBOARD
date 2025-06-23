import pandas as pd
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

def run_detection(df, contamination=0.02):
    results = {}

    # Fill missing values
    df = df.ffill()

    # Feature selection
    features = ["IRRADIATION", "AMBIENT_TEMPERATURE", "MODULE_TEMPERATURE", "AC_POWER"]
    X = df[features]

    # --- Isolation Forest ---
    iso_forest = IsolationForest(contamination=contamination, random_state=42)
    iso_forest.fit(X)
    df["IF_anomaly"] = pd.Series(iso_forest.predict(X)).map({1: "Normal", -1: "Anomaly"})

    # --- Random Forest ---
    df["RF_label"] = df["IF_anomaly"].map({"Normal": 0, "Anomaly": 1})
    X_train, X_test, y_train, y_test = train_test_split(X, df["RF_label"], test_size=0.2, random_state=42)
    rf_model = RandomForestClassifier(n_estimators=200, random_state=42)
    rf_model.fit(X_train, y_train)
    df["RF_anomaly"] = rf_model.predict(X)
    df["RF_anomaly"] = df["RF_anomaly"].map({0: "Normal", 1: "Anomaly"})

    # Evaluation
    acc = accuracy_score(y_test, rf_model.predict(X_test))
    report = classification_report(y_test, rf_model.predict(X_test), output_dict=True)

    # Package results
    results["df"] = df
    results["accuracy"] = acc
    results["report"] = report

    return results