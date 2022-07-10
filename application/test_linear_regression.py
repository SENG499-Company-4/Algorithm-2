import sys
import pytest
sys.path.insert(1, '../algorithm')
import algorithm.linear_regression as linear_regression


pytest.test_model = linear_regression.linear_regression()

def test_linear_model():
    result = pytest.test_model.predict_size("test")
    assert result.startswith('Predicted')