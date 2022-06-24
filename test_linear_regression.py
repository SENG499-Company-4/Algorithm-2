from linear_regression import linear_regression
import pytest

pytest.test_model = linear_regression()

def test_linear_model():
    result = pytest.test_model.predict_size("test")
    assert result.startswith('Predicted')