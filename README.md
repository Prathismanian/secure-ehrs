\# Privacy-Preserving Clinical Risk Pipeline (Split-Key SHA-512 + Leak-Free ML)



A GDPR-inspired, privacy-by-design Machine Learning pipeline demonstrating \*\*dual-authorization cryptographic data governance\*\*, \*\*automated PII redaction\*\*, and \*\*leak-free clinical modeling\*\* on Electronic Health Record (EHR) data.



\## Why This Matters (Healthcare \& Regulated AI)

In real clinical environments (e.g., EU/German hospital Trusted Research Environments), Data Scientists and Annotators cannot access raw patient identifiers. Furthermore, uncurated clinical exports often contain duplicate records that cause severe train/test data leakage.



\## Architecture \& Security Workflow

1\. \*\*Zero-Trust Split-Key Gate:\*\* Requires simultaneous authorization from two independent parties (`Hospital Key` + `Ethics Board Key`), verified via \*\*SHA-512 cryptographic hashing\*\*.

2\. \*\*Role-Based Column Governance:\*\* Dynamically strips direct PII (`patient\_id`, `patient\_name`) by matching `SHA-512(role:column)` against approved policy hashes.

3\. \*\*Data Hygiene \& Deduplication:\*\* Identifies and removes 723 duplicate patient entries (`1,025 -> 302` unique records) \*before\* splitting to prevent model memorization.

4\. \*\*Interpretable Clinical Modeling:\*\* Trains a depth-constrained Random Forest classifier and ranks validated cardiovascular risk drivers.



\## Key Results (Validated on Unique Patient Cohort)

\* \*\*PII Exposure:\*\* 0% (All identifiers stripped prior to ML ingestion)

\* \*\*ROC-AUC:\*\* `0.853` | \*\*Accuracy:\*\* `77.05%` (Leak-free baseline)

\* \*\*Top Clinical Risk Drivers:\*\*

&#x20; 1. `cp` (Chest Pain Type): `18.3%`

&#x20; 2. `thalach` (Max Heart Rate): `13.5%`

&#x20; 3. `ca` (Major Vessels Colored): `11.3%`

&#x20; 4. `thal` (Thalassemia Defect): `10.1%`

&#x20; 5. `oldpeak` (ST Depression): `9.8%`





\## Reading Log



My research papers on electronic Health Records data security and privacy-preserving using machine learning techniques.



| # | Paper Title | Key Topics | Notes |

| :--- | :--- | :--- | :--- |

| 01 | An Efficient CH-Based Authentication and Authorization for Secure EHR Using DF-BCrypt and Hashed Access Structure | Authentication, SHA-512 Hash Tree, Elliptic Curve Cryptography |(./journals/01-ch-df-bcrypt-ehr.md) |

&#x20;02 | Federated Learning for Smart Healthcare: A Survey | Federated Learning, Healthcare AI, Data Privacy | (./papers/02-federated-learning-healthcare.md) |





