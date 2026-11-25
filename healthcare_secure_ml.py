

import hashlib
import random
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split

# ==============================================================================
# PART 1: Generate 500 Synthetic (Fake) Electronic Health Records (EHR)
# ==============================================================================
def create_synthetic_ehr(num_patients=500):
    random.seed(42)
    records = []

    for i in range(1, num_patients + 1):
        age = random.randint(25, 85)
        blood_pressure = random.randint(95, 185)
        glucose = round(random.uniform(75.0, 230.0), 1)
        bmi = round(random.uniform(18.5, 40.0), 1)

        # Realistic medical risk formula so the ML model learns real patterns
        risk_points = (
            0.04 * (age - 40)
            + 0.03 * (blood_pressure - 115)
            + 0.02 * (glucose - 100)
            + 0.08 * (bmi - 24)
            + random.gauss(0, 1.0)
        )
        heart_risk = 1 if risk_points > 2.0 else 0

        records.append({
            # Private Identity Columns (Must stay hidden from Data Scientists!)
            "patient_id": f"DE-PAT-{1000 + i}",
            "patient_name": f"Patient_{i}",
            # Safe Clinical Columns (Allowed for ML modeling)
            "age": age,
            "blood_pressure": blood_pressure,
            "glucose": glucose,
            "bmi": bmi,
            "heart_risk": heart_risk,
        })

    return pd.DataFrame(records)


# ==============================================================================
# PART 2: Journal-Inspired Security Gate (Partial Keys + SHA-512 Hash Access)
# Inspired by:
#   1) SHA-512 Hashed Access Structures (Prathima & Durga, 2024)
#   2) Partial Key Distributed EHR Access (PDHSMICK)
# ==============================================================================
def sha512_hash(text):
    return hashlib.sha512(text.encode("utf-8")).hexdigest()

# Allowed permissions stored as SHA-512 hashes
ALLOWED_POLICY_HASHES = {
    sha512_hash("data_scientist:age"),
    sha512_hash("data_scientist:blood_pressure"),
    sha512_hash("data_scientist:glucose"),
    sha512_hash("data_scientist:bmi"),
    sha512_hash("data_scientist:heart_risk"),
}

def unlock_safe_ml_data(raw_df, role, hospital_key, ethics_board_key):
    # Check 1: Both partial keys must be present (Multi-party governance)
    if not hospital_key or not ethics_board_key:
        raise PermissionError("Access Denied: Missing partial authorization key.")

    # Check 2: Filter columns using SHA-512 hashed access policies
    allowed_columns = [
        col for col in raw_df.columns
        if sha512_hash(f"{role}:{col}") in ALLOWED_POLICY_HASHES
    ]

    return raw_df[allowed_columns].copy()


# ==============================================================================
# PART 3: Machine Learning Prediction & Explainability (What Recruiters Love!)
# ==============================================================================
if __name__ == "__main__":
    print("STEP 1: Creating 500 synthetic patient EHR records...")
    full_ehr_df = create_synthetic_ehr(500)
    print(f"Raw EHR columns (contains private info): {list(full_ehr_df.columns)}\n")

    print("STEP 2: Verifying partial keys & SHA-512 hashed access rules...")
    safe_df = unlock_safe_ml_data(
        raw_df=full_ehr_df,
        role="data_scientist",
        hospital_key="HOSP-KEY-8842",
        ethics_board_key="ETHICS-KEY-9910",
    )
    print(f"Unlocked ML columns (PII removed!): {list(safe_df.columns)}\n")

    print("STEP 3: Training Random Forest model to predict Heart Risk...")
    X = safe_df[["age", "blood_pressure", "glucose", "bmi"]]
    y = safe_df["heart_risk"]

    # Split 80% for training, 20% for testing (prevents data leakage)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate performance
    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]

    acc = accuracy_score(y_test, predictions)
    auc = roc_auc_score(y_test, probabilities)

    print(f"Model Accuracy : {acc:.2%}")
    print(f"Model ROC-AUC  : {auc:.3f}\n")

    # Show which clinical features mattered most (Explainable AI)
    print("Top Clinical Risk Drivers (Feature Importance):")
    for feature, importance in sorted(
        zip(X.columns, model.feature_importances_), key=lambda item: item[1], reverse=True
    ):
        print(f"  - {feature:15s}: {importance:.1%}")
