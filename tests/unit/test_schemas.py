import pytest
from pydantic import ValidationError
from app.schemas.user import UserCreate, PasswordUpdate

# --- Tests for UserCreate Schema ---

def test_user_create_success():
    """Test that UserCreate validates successfully with correct data."""
    try:
        UserCreate(
            first_name="Valid", last_name="User", email="valid@example.com",
            username="validuser", password="ValidPassword123!",
            confirm_password="ValidPassword123!"
        )
    except ValidationError as e:
        pytest.fail(f"UserCreate raised an unexpected validation error: {e}")

def test_user_create_password_mismatch():
    """Test that UserCreate raises an error if passwords do not match."""
    with pytest.raises(ValidationError, match="Passwords do not match"):
        UserCreate(
            first_name="Test", last_name="User", email="test@example.com",
            username="testuser", password="SecurePass123!",
            confirm_password="DIFFERENT_PASSWORD"
        )

@pytest.mark.parametrize(
    "password, expected_error",
    [
        ("short", "String should have at least 8 characters"),
        ("noupper1!", "Password must contain at least one uppercase letter"),
        ("NOLOWER1!", "Password must contain at least one lowercase letter"),
        ("NoDigit!!", "Password must contain at least one digit"),
        ("NoSpecial1", "Password must contain at least one special character"),
    ],
)
def test_user_create_password_strength(password: str, expected_error: str):
    """Test password strength validation for various failure cases."""
    with pytest.raises(ValidationError, match=expected_error):
        UserCreate(
            first_name="Test", last_name="User", email="test@example.com",
            username="testuser", password=password, confirm_password=password
        )

# --- Tests for PasswordUpdate Schema ---

def test_password_update_success():
    """Test that PasswordUpdate validates successfully with correct data."""
    try:
        PasswordUpdate(
            current_password="OldPass123!",
            new_password="NewValidPassword123!",
            confirm_new_password="NewValidPassword123!"
        )
    except ValidationError as e:
        pytest.fail(f"PasswordUpdate raised an unexpected validation error: {e}")

def test_password_update_mismatch():
    """Test an error is raised if new passwords do not match."""
    with pytest.raises(ValidationError, match="New password and confirmation do not match"):
        PasswordUpdate(
            current_password="OldPass123!",
            new_password="NewSecurePassword123!",
            confirm_new_password="DIFFERENT_PASSWORD"
        )

def test_password_update_same_as_current():
    """Test an error is raised if the new password is the same as the old one."""
    with pytest.raises(ValidationError, match="New password must be different from current password"):
        PasswordUpdate(
            current_password="OldPass123!",
            new_password="OldPass123!",
            confirm_new_password="OldPass123!"
        )