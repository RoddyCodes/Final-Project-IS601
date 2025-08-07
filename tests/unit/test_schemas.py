# tests/unit/test_schemas.py

import pytest
from pydantic import ValidationError
from app.schemas.user import UserCreate, PasswordUpdate

# --- Tests for UserCreate Schema ---

def test_user_create_password_mismatch():
    """
    Test that UserCreate raises a ValueError if passwords do not match.
    This covers lines 53-55 in user.py.
    """
    with pytest.raises(ValidationError) as excinfo:
        UserCreate(
            first_name="Test",
            last_name="User",
            email="test@example.com",
            username="testuser",
            password="SecurePass123!",
            confirm_password="DIFFERENT_PASSWORD" # Mismatch
        )
    # Check that the specific error message is present
    assert "Passwords do not match" in str(excinfo.value)

@pytest.mark.parametrize(
    "password, expected_error",
    [
        ("short", "String should have at least 8 characters"),
        ("noupper1!", "Password must contain at least one uppercase letter"),
        ("NOLOWER1!", "Password must contain at least one lowercase letter"),
        ("NoDigit!!", "Password must contain at least one digit"),
        ("NoSpecial1", "Password must contain at least one special character"),
    ],
    ids=[
        "too_short",
        "no_uppercase",
        "no_lowercase",
        "no_digit",
        "no_special_char",
    ],
)
def test_user_create_password_strength(password: str, expected_error: str):
    """
    Test password strength validation for various failure cases.
    This covers lines 60-71 in user.py.
    """
    with pytest.raises(ValidationError) as excinfo:
        UserCreate(
            first_name="Test",
            last_name="User",
            email="test@example.com",
            username="testuser",
            password=password,
            confirm_password=password,
        )
    assert expected_error in str(excinfo.value)

# --- Tests for PasswordUpdate Schema ---

def test_password_update_mismatch():
    """
    Test that PasswordUpdate raises an error if new passwords do not match.
    This covers one of the checks in the 'verify_passwords' validator.
    """
    with pytest.raises(ValidationError) as excinfo:
        PasswordUpdate(
            current_password="OldPass123!",
            new_password="NewSecurePassword123!",
            confirm_new_password="DIFFERENT_PASSWORD" # Mismatch
        )
    assert "New password and confirmation do not match" in str(excinfo.value)

def test_password_update_same_as_current():
    """
    Test that PasswordUpdate raises an error if the new password is the same as the old one.
    This covers the second check in the 'verify_passwords' validator.
    """
    with pytest.raises(ValidationError) as excinfo:
        PasswordUpdate(
            current_password="OldPass123!",
            new_password="OldPass123!", # Same as current
            confirm_new_password="OldPass123!",
        )
    assert "New password must be different from current password" in str(excinfo.value)

def test_user_create_success():
    """Test that UserCreate validates successfully with correct data."""
    try:
        UserCreate(
            first_name="Valid",
            last_name="User",
            email="valid@example.com",
            username="validuser",
            password="ValidPassword123!",
            confirm_password="ValidPassword123!",
        )
    except ValidationError as e:
        pytest.fail(f"UserCreate raised an unexpected validation error: {e}")

def test_password_update_success():
    """Test that PasswordUpdate validates successfully with correct data."""
    try:
        PasswordUpdate(
            current_password="OldPass123!",
            new_password="NewValidPassword123!",
            confirm_new_password="NewValidPassword123!",
        )
    except ValidationError as e:
        pytest.fail(f"PasswordUpdate raised an unexpected validation error: {e}")