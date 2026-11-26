# Federated Learning for Smart Healthcare: A Survey

- **Authors & Year:** Dinh C. Nguyen et al., 2021 / 2022
- **Journal / Source:** ACM Computing Surveys (also open-access on arXiv)
- **Link:** https://arxiv.org
- **Date Read:** 2026-11-26
- **Tags:** `clinical-ml` `federated-learning` `privacy` `survey` `healthcare-ai`

---

## 1. The Actual Scenario 
- **Clinical Goal:** Train accurate healthcare AI models (for disease diagnosis, patient monitoring, and EHR analysis) using data from many hospitals and wearable devices.
- **Privacy Problem:** Traditional AI requires pooling all patient data into one central server, which violates patient privacy laws and creates a massive target for hackers which is more prevelant.

## 2. What did The Journal Solve?
- **Privacy Technique Used:** Federated Learning (FL), often combined with Differential Privacy (DP) and Encryption.
- **The Model:**
  1. A central server sends a blank/initial AI model to multiple participating hospitals.
  2. Each hospital trains the model locally on its own private patient records—**the raw data never leaves the hospital**.
  3. Each hospital sends *only* the learned model updates (weights/gradients) back to the central server.
  4. The server averages those updates together (e.g., using *Federated Averaging*) to create a smarter global model, and repeats the process.

## 3. Data & Model Details
- **Datasets Covered:** Multi-hospital Electronic Health Records (EHRs), medical imaging (X-rays, MRIs), and wearable/IoMT heart-rate sensor data.
- **ML Models Covered:** Neural Networks, CNNs (for images), and standard tabular classifiers (like Logistic Regression for EHRs).

## 4. Key Results & Trade-offs
- **Main Result:** Federated Learning allows hospitals to collaborate and build stronger AI models than any single hospital could train alone, while keeping patient records under local hospital control.
- **Limitations / Trade-offs:** 
  - **Data Heterogeneity (Non-IID Data):** Different hospitals have different patient demographics and machines, which can make training harder.
  - **Gradient Leakage:** Even model updates can occasionally leak clues about patients unless combined with Differential Privacy (noise) or encryption.

## 5. My Understanding
- **My Learning:** You don't have to move patient data to train an AI model—you can send the *AI model to the data* instead!
- **New terms I had to look up:** 
  - *Federated Averaging (FedAvg):* The standard algorithm that combines model weights trained at different hospitals into one shared model.
  - *Non-IID Data:* Data that is not identically distributed across hospitals (e.g., one clinic sees mostly older heart patients while another sees younger patients).
- **can this be coded?** Yes — I can split my heart disease dataset into 2 or 3 simulated "hospitals" in Python, train separate models on each split, and average their weights!

- **Real-Data Experiment (`src/federated_kaggle_heart.py`):** Tested Federated Averaging across 2 simulated hospitals on 1,025 real patient records from Kaggle (`Data/heart.csv`). Hospital A scored 78.21%, Hospital B scored 78.21%, and the combined Federated Global Model outperformed both at **78.60%** without sharing raw patient records!

