import pytest
from unittest import mock
from datetime import timedelta
from uuid import uuid4
from jose import JWTError
from fastapi import HTTPException, status

from app.schemas.token import TokenType
from app.auth.jwt import create_token, decode_token, get_current_user

# --- Tests for create_token() ---
# These are synchronous tests and do not need the asyncio mark.

def test_create_token_with_uuid_subject():
    user_id = uuid4()
    token = create_token(user_id, TokenType.ACCESS)
    assert isinstance(token, str)

def test_create_refresh_token_no_delta():
    user_id = "testuser"
    token = create_token(user_id, TokenType.REFRESH)
    assert isinstance(token, str)

@mock.patch('app.auth.jwt.jwt.encode', side_effect=Exception("Encoding failed"))
def test_create_token_encode_exception(mock_jwt_encode):
    with pytest.raises(HTTPException) as excinfo:
        create_token("testuser", TokenType.ACCESS)
    assert excinfo.value.status_code == 500
    assert "Could not create token" in str(excinfo.value.detail)


# --- Tests for decode_token() ---
# These are asynchronous tests and need the decorator.

@pytest.mark.asyncio
async def test_decode_token_expired():
    user_id = "testuser"
    expired_token = create_token(user_id, TokenType.ACCESS, expires_delta=timedelta(minutes=-1))
    with pytest.raises(HTTPException, match="Token has expired"):
        await decode_token(expired_token, TokenType.ACCESS)

@pytest.mark.asyncio
async def test_decode_token_invalid_type():
    access_token = create_token("testuser", TokenType.ACCESS)
    with pytest.raises(HTTPException, match="Could not validate credentials"):
        await decode_token(access_token, TokenType.REFRESH)

@pytest.mark.asyncio
@mock.patch('app.auth.jwt.is_blacklisted', return_value=True)
async def test_decode_token_blacklisted(mock_is_blacklisted):
    token = create_token("testuser", TokenType.ACCESS)
    with pytest.raises(HTTPException, match="Token has been revoked"):
        await decode_token(token, TokenType.ACCESS)
    mock_is_blacklisted.assert_called_once()

@pytest.mark.asyncio
@mock.patch('app.auth.jwt.jwt.decode', side_effect=JWTError)
async def test_decode_token_jwt_error(mock_jwt_decode):
    with pytest.raises(HTTPException, match="Could not validate credentials"):
        await decode_token("a-bad-token", TokenType.ACCESS)


# --- Tests for get_current_user() ---

@pytest.mark.asyncio
@mock.patch('app.auth.jwt.decode_token')
async def test_get_current_user_not_found(mock_decode_token):
    mock_decode_token.return_value = {"sub": str(uuid4())}
    mock_db_session = mock.MagicMock()
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    with pytest.raises(HTTPException, match="User not found"):
        await get_current_user(token="fake_token", db=mock_db_session)

@pytest.mark.asyncio
@mock.patch('app.auth.jwt.decode_token')
async def test_get_current_user_inactive(mock_decode_token):
    mock_user = mock.MagicMock()
    mock_user.is_active = False
    mock_decode_token.return_value = {"sub": str(uuid4())}
    mock_db_session = mock.MagicMock()
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_user
    with pytest.raises(HTTPException, match="Inactive user"):
        await get_current_user(token="fake_token", db=mock_db_session)

# ** NEW TEST TO INCREASE COVERAGE **
@pytest.mark.asyncio
@mock.patch('app.auth.jwt.decode_token')
async def test_get_current_user_missing_sub(mock_decode_token):
    """
    Test the final `except` block in get_current_user by simulating
    a token payload that is missing the 'sub' (subject) key.
    """

    # Simulate a validly decoded token but without the user ID
    mock_decode_token.return_value = {"type": "access"} 
    mock_db_session = mock.MagicMock()

    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token="fake_token", db=mock_db_session)
    
    # This should be caught by the final generic exception handler
    assert excinfo.value.status_code == 401
    assert "Could not process token" in str(excinfo.value.detail)