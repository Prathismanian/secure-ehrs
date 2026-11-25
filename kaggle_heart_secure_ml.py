import hashlib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split

# ==============================================================================
# PART 1: Load Real Kaggle Heart Disease Data + Simulate Raw Hospital IDs
# ==============================================================================
def load_hospital_ehr(csv_path="data/heart.csv"):
    df = pd.read_csv(csv_path)

    # Simulate private hospital identifiers that exist in real EHR databases
    df.insert(0, "patient_id", [f"DE-HOSP-{1000 + i}" for i in range(len(df))])
    df.insert(1, "patient_name", [f"Patient_{i + 1}" for i in range(len(df))])
    return df


# ==============================================================================
# PART 2: Journal-Inspired Security Gate (Partial Keys + SHA-512 Hash Access)
# ==============================================================================
def sha512_hash(text):
    return hashlib.sha512(text.encode("utf-8")).hexdigest()

# Pre-registered hash of valid combined partial keys (HOSP-KEY-8842 + ETHICS-KEY-9910)
VALID_COMBINED_KEY_HASH = sha512_hash("HOSP-KEY-8842:ETHICS-KEY-9910")

# The 13 clinical columns + 1 target column allowed for the Data Scientist
CLINICAL_COLUMNS = [
    "age", "sex", "cp", "trestbps", "chol", "fbs",
    "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal", "target"
]

ALLOWED_POLICY_HASHES = {
    sha512_hash(f"data_scientist:{col}") for col in CLINICAL_COLUMNS
}

def unlock_safe_ml_data(raw_df, role, hospital_key, ethics_board_key):
    if not hospital_key or not ethics_board_key:
        raise PermissionError("Access Denied: Missing partial authorization key.")

    # Verify cryptographic integrity of the split keys
    if sha512_hash(f"{hospital_key}:{ethics_board_key}") != VALID_COMBINED_KEY_HASH:
        raise PermissionError("Access Denied: Invalid partial key combination.")

    allowed_cols = [
        col for col in raw_df.columns
        if sha512_hash(f"{role}:{col}") in ALLOWED_POLICY_HASHES
    ]
    return raw_df[allowed_cols].copy()


# ==============================================================================
# PART 3: Train & Evaluate Machine Learning Model on Real Clinical Data
# ==============================================================================
if __name__ == "__main__":
    raw_ehr_df = load_hospital_ehr("data/heart.csv")
    print(f"STEP 1: Loaded {len(raw_ehr_df):,} patient records from Kaggle heart.csv...")
    print(f"Raw EHR columns ({len(raw_ehr_df.columns)} cols): {list(raw_ehr_df.columns)}\n")

    print("STEP 2: Applying Partial Key Check & SHA-512 Hashed Access Rules...")
    safe_df = unlock_safe_ml_data(
        raw_df=raw_ehr_df,
        role="data_scientist",
        hospital_key="HOSP-KEY-8842",
        ethics_board_key="ETHICS-KEY-9910",
    )

    # Deduplicate after PII removal to prevent train/test data leakage
    before_dedup = len(safe_df)
    safe_df = safe_df.drop_duplicates().reset_index(drop=True)
    print(f"Deduplicated records: {before_dedup} -> {len(safe_df)} unique patients")
    print(f"Unlocked ML columns ({len(safe_df.columns)} cols - PII removed!):")
    print(list(safe_df.columns), "\n")

    print("STEP 3: Training Random Forest on Real Clinical Features...")
    X = safe_df.drop(columns=["target"])
    y = safe_df["target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    model = RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]

    print(f"Model Accuracy : {accuracy_score(y_test, predictions):.2%}")
    print(f"Model ROC-AUC  : {roc_auc_score(y_test, probabilities):.3f}\n")

    print("Top 5 Clinical Risk Drivers:")
    ranked_features = sorted(
        zip(X.columns, model.feature_importances_),
        key=lambda item: item[1],  # Sort by importance score, not feature name
        reverse=True,
    )
    for feature, importance in ranked_features[:5]:
        print(f"  - {feature:10s}: {importance:.1%}")
