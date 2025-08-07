# tests/unit/test_models.py

from app.models.calculation import Addition, Subtraction

def test_addition_model_get_result():
    """Test the get_result method of the Addition model."""
    # Arrange
    add_calc = Addition(inputs=[10, 20, 5])
    
    # Act
    result = add_calc.get_result()
    
    # Assert
    assert result == 35

def test_subtraction_model_get_result():
    """Test the get_result method of the Subtraction model."""
    # Arrange
    sub_calc = Subtraction(inputs=[100, 20, 10])
    
    # Act
    result = sub_calc.get_result()
    
    # Assert
    assert result == 70