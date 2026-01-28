from sklearn.datasets import load_breast_cancer
from mlops_enterprise.validation import validate_df


def test_validation_passes():
    ds = load_breast_cancer(as_frame=True)
    df = ds.frame.copy().rename(columns={"target": "label"})
    feature_cols = [c for c in df.columns if c != "label"]
    out = validate_df(df.sample(n=30, random_state=0), feature_cols)
    assert out.shape[0] == 30
