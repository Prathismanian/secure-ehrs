import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# 1. Load your real Kaggle Heart Disease dataset
df = pd.read_csv("Data/heart.csv")

# Automatically handle either Kaggle heart.csv version ('target' or 'HeartDisease')
target_col = "target" if "target" in df.columns else df.columns[-1]
X = pd.get_dummies(
    df.drop(columns=[target_col]), drop_first=True
)  # Convert any text columns to numbers
y = df[target_col].values

# 2. Split into training patients and unseen test patients
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

# Scale clinical features (age, blood pressure, cholesterol) so Logistic Regression learns evenly
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# 3. Split training patients across TWO separate hospitals (raw data stays private!)
hospital_A_X, hospital_B_X = np.array_split(X_train, 2)
hospital_A_y, hospital_B_y = np.array_split(y_train, 2)

# 4. Each hospital trains its own local model independently
model_A = LogisticRegression(max_iter=1000).fit(hospital_A_X, hospital_A_y)
model_B = LogisticRegression(max_iter=1000).fit(hospital_B_X, hospital_B_y)

# 5. Federated Averaging (FedAvg): Server averages ONLY the learned weights
global_model = LogisticRegression(max_iter=1000)
global_model.fit(
    X_train[:10], y_train[:10]
)  # Initialize classes and shapes
global_model.coef_ = (model_A.coef_ + model_B.coef_) / 2
global_model.intercept_ = (model_A.intercept_ + model_B.intercept_) / 2

# 6. Print real clinical accuracy results!
print(f"Loaded {len(df)} real patient records (Target column: '{target_col}')")
print(
    f"Hospital A Alone Accuracy : {accuracy_score(y_test, model_A.predict(X_test)):.2%}"
)
print(
    f"Hospital B Alone Accuracy : {accuracy_score(y_test, model_B.predict(X_test)):.2%}"
)
print(
    f"Federated Global Accuracy : {accuracy_score(y_test, global_model.predict(X_test)):.2%}"
)
