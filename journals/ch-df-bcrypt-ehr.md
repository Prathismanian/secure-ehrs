\# An Efficient CH-Based Authentication and Authorization for Secure EHR Using DF-BCrypt and Hashed Access Structure



\- \*\*Authors \& Year:\*\* S.Prathima and R.Durga

\- \*\*Journal / Source:\*\* An Efficient CH based authentication and authorization for secure EHR using DF-BCrypt and hashed access structure

\- \*\*Publication:\*\* Springer Nature Switzerland, International Conference on Advancements in Smart Computing and Information Security, 2023, pages 207–226

\- \*\*Link:\*\* https://link.springer.com/chapter/10.1007/978-3-031-59100-6\_16

\- \*\*Date Published:\*\* 2023

\- \*\*Tags:\*\* `EHR-security` `ehr` `authentication` `access-control` `cryptography`



\---



\## 1. The Existing Issues

\- \*\*Clinical Goal:\*\* Safely collect, store, and share large-scale Electronic Health Records (EHRs) between hospitals and researchers without communication delays.

\- \*\*Privacy \& Security Problem:\*\* When EHRs are shared across networks, existing systems suffer from three big risks: unauthorized access/weak login security, data tampering (manipulation), and slow, untrusted data sharing between parties.



\## 2. Proposed Solution

The authors designed a three-part security pipeline covering \*\*Authentication\*\* (who you are), \*\*Authorization\*\* (what you can access), and \*\*Data Encryption\*\* (locking the medical files):



\- \*\*Privacy \& Security Techniques Used:\*\*

&#x20; 1. \*\*HPU-PPCC-DF-BCrypt (Cipher Hashing Authentication):\*\* Combines \*Hospital ID, Patient ID, and Username\* with \*Public-Private keys, Caesar Cipher, Digit Folding,\* and \*BCrypt\* to create strong, uncrackable login hashes.

&#x20; 2. \*\*SHA-512 Hash Tree Access Structure (Authorization):\*\* Uses SHA-512 hash codes organized into a hash tree so access policies are verified quickly without exposing plain-text rules.

&#x20; 3. \*\*CCECC (Coefficient-based Elliptic Curve Cryptography):\*\* Encrypts and decrypts the actual EHR medical files so outsiders cannot read or tamper with the records.



\- \*\*How this Works:\*\*

&#x20; 1. \*\*Credential Creation \& Login:\*\* The system takes the Hospital ID, Patient ID, and Username, transforms them via Public-Private keys and a Caesar Cipher (\*\*HPU-PPCC\*\*), and converts that ciphertext into a secure password hash using Digit Folding + BCrypt (\*\*DF-BCrypt\*\*).

&#x20; 2. \*\*Permission Check:\*\* Before granting access, the system verifies the user against a \*\*SHA-512 hash tree access structure\*\* to confirm they have authorization.

&#x20; 3. \*\*EHR Encryption/Decryption:\*\* Finally, the health records themselves are locked and unlocked using \*\*CCECC\*\* (Elliptic Curve Cryptography), protecting the data during storage and transfer.



\## 3. Data \& System Details

\- \*\*Dataset / Environment Used:\*\* Large-scale Electronic Health Record (EHR) data\ https://www.kaggle.com/datasets/johnsmith88/heart-disease-dataset

\- \*\*Core Algorithms:\*\* HPU-PPCC, Digit Folding BCrypt (DF-BCrypt), SHA-512 Hash Tree, and Coefficient-based Elliptic Curve Cryptography (CCECC).



\## 4. Key Results \& Trade-offs

\- \*\*Main Result:\*\* Compared against existing EHR security methods, the proposed framework successfully prevented data tampering and improved authentication/authorization security while keeping processing efficient.

\- \*\*Limitations / Trade-offs:\*\* 

&#x20; - \*\*Multi-Step Pipeline:\*\* Chaining multiple transformations (Caesar Cipher + Public/Private keys + Digit Folding + BCrypt + SHA-512 + CCECC) requires careful implementation across hospital systems.

&#x20; - \*\*Relevance to ML:\*\* While this paper does not train a machine learning model directly, it solves a major real-world hurdle for clinical ML: \*\*how researchers can securely receive and verify untampered EHR datasets\*\* before running ML experiments.



\## 5. My Personal Takeaways

\- \*\*What I learned:\*\* Before we even run an ML model on medical data, hospitals need strong \*Cipher Hashing\* (authentication), \*Hash Trees\* (authorization), and \*Elliptic Curve Cryptography\* (encryption) so patient records aren't altered or leaked in transit.

\- \*\*New terms I had to look up:\*\* 

&#x20; - \*Digit Folding:\* A hashing technique where a long number/string is split into equal parts and added/combined together to produce a compact hash value.

&#x20; - \*SHA-512 Hash Tree:\* A tree structure of cryptographic hashes (512-bit) that lets a system quickly verify permissions and check that data hasn't been tampered with.

&#x20; - \*Elliptic Curve Cryptography (ECC):\* A fast, modern encryption method that provides strong security using much smaller keys than older methods like RSA.

\- \*\*Can I try this in code?\*\* Yes — in Python, I can use the built-in `hashlib` library (`hashlib.sha512`) and the `bcrypt` package to practice hashing user/patient IDs before loading my sample heart disease dataset!



