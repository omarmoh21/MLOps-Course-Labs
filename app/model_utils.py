"""
Model loading and prediction logic.

The model must be loaded ONCE at module level, NOT inside the predict function.
"""

import warnings
from pathlib import Path

import joblib
import pandas as pd

# TODO 1: Load your serialized churn model from data/model.joblib
_DATA_DIR = Path(__file__).parent.parent / "data"

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    model = joblib.load(_DATA_DIR / "model.joblib")
    column_transformer = joblib.load(_DATA_DIR / "column_transformer.joblib")

# Input feature order expected by the API / column transformer
FEATURE_NAMES = [
    "CreditScore",
    "Geography",
    "Gender",
    "Age",
    "Tenure",
    "Balance",
    "NumOfProducts",
    "HasCrCard",
    "IsActiveMember",
    "EstimatedSalary",
]

# Geography and Gender unique values (for validation / docs)
GEOGRAPHY_OPTIONS = ["France", "Germany", "Spain"]
GENDER_OPTIONS = ["Male", "Female"]


def predict_churn(features: list) -> int:
    """
    Takes a list of feature values matching FEATURE_NAMES order and returns
    a churn prediction (0 or 1).

    Features order:
        CreditScore, Geography, Gender, Age, Tenure, Balance,
        NumOfProducts, HasCrCard, IsActiveMember, EstimatedSalary
    """
    # TODO 2: Use model.predict() to get a prediction and return it as an int
    row = dict(zip(FEATURE_NAMES, features))
    df = pd.DataFrame([row])

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        X_transformed = column_transformer.transform(df)
        X_df = pd.DataFrame(X_transformed, columns=model.feature_names_in_)
        prediction = model.predict(X_df)

    return int(prediction[0])


if __name__ == "__main__":
    # TODO 3: Replace with sample features that match your model
    sample = [
        600,
        "France",
        "Male",
        40,
        3,
        60000.0,
        2,
        1,
        1,
        50000.0,
    ]
    print(f"Input:      {sample}")
    print(f"Prediction: {predict_churn(sample)}")
