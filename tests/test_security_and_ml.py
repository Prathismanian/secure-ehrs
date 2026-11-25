import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from kaggle_heart_secure_ml import load_hospital_ehr, unlock_safe_ml_data

def test_valid_keys_strip_pii():
    raw_df = load_hospital_ehr("data/heart.csv")
    safe_df = unlock_safe_ml_data(
        raw_df=raw_df,
        role="data_scientist",
        hospital_key="HOSP-KEY-8842",
        ethics_board_key="ETHICS-KEY-9910",
    )
    assert "patient_id" not in safe_df.columns
    assert "patient_name" not in safe_df.columns
    assert len(safe_df.columns) == 14

def test_invalid_keys_denied():
    raw_df = load_hospital_ehr("data/heart.csv")
    with pytest.raises(PermissionError):
        unlock_safe_ml_data(
            raw_df=raw_df,
            role="data_scientist",
            hospital_key="WRONG-KEY",
            ethics_board_key="ETHICS-KEY-9910",
        )

def test_unauthorized_role_gets_zero_columns():
    raw_df = load_hospital_ehr("data/heart.csv")
    safe_df = unlock_safe_ml_data(
        raw_df=raw_df,
        role="untrusted_intern",
        hospital_key="HOSP-KEY-8842",
        ethics_board_key="ETHICS-KEY-9910",
    )
    assert safe_df.shape[1] == 0
