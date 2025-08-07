# tests/unit/test_auth_jwt.py

import pytest
from unittest import mock
from datetime import timedelta
from uuid import uuid4
from jose import JWTError
from fastapi import HTTPException, status

from app.schemas.token import TokenType
from app.auth.jwt import create_token, decode_token, get_current_user

# Mark all tests in this file as async
pytestmark = pytest.mark.asyncio


## --- Tests for create_token() ---

def test_create_token_with_uuid_subject():
    """
    Test that create_token correctly handles a UUID object for the user_id.
    This covers line 46.
    """
    user_id = uuid4()
    # This should run without errors
    token = create_token(user_id, TokenType.ACCESS)
    assert isinstance(token, str)

def test_create_refresh_token_no_delta():
    """
    Test creating a refresh token using the default expiration.
    This covers lines 76-77.
    """
    user_id = "testuser"
    # This should run without errors and use the 'else' block
    token = create_token(user_id, TokenType.REFRESH)
    assert isinstance(token, str)

@mock.patch('app.auth.jwt.jwt.encode')
def test_create_token_encode_exception(mock_jwt_encode):
    """
    Test that an HTTPException is raised if jwt.encode fails.
    This covers line 58.
    """
    # Configure the mock to raise an exception when called
    mock_jwt_encode.side_effect = Exception("Encoding failed")
    
    with pytest.raises(HTTPException) as excinfo:
        create_token("testuser", TokenType.ACCESS)
        
    assert excinfo.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Could not create token" in str(excinfo.value.detail)


## --- Tests for decode_token() ---

async def test_decode_token_expired():
    """
    Test decoding an expired token.
    This covers the ExpiredSignatureError block (line 118).
    """
    user_id = "testuser"
    # Create a token that expired 1 minute ago
    expired_token = create_token(
        user_id, TokenType.ACCESS, expires_delta=timedelta(minutes=-1)
    )
    
    with pytest.raises(HTTPException) as excinfo:
        await decode_token(expired_token, TokenType.ACCESS)
        
    assert excinfo.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Token has expired" in excinfo.value.detail

async def test_decode_token_invalid_type():
    """
    Test decoding a token with a mismatched type.
    This covers the invalid token type check (line 105).
    """
    access_token = create_token("testuser", TokenType.ACCESS)
    
    with pytest.raises(HTTPException) as excinfo:
        # Try to decode an access token as if it were a refresh token
        await decode_token(access_token, TokenType.REFRESH)
        
    assert excinfo.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Could not validate credentials" in excinfo.value.detail
@mock.patch('app.auth.jwt.is_blacklisted', return_value=True)
async def test_decode_token_blacklisted(mock_is_blacklisted):
    """
    Test decoding a token that has been blacklisted/revoked.
    This covers the blacklisted check (line 111).
    """
    token = create_token("testuser", TokenType.ACCESS)
    
    with pytest.raises(HTTPException) as excinfo:
        await decode_token(token, TokenType.ACCESS)
        
    assert excinfo.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Token has been revoked" in excinfo.value.detail
    mock_is_blacklisted.assert_called_once()

@mock.patch('app.auth.jwt.jwt.decode', side_effect=JWTError)
async def test_decode_token_jwt_error(mock_jwt_decode):
    """
    Test decoding a malformed token that causes a JWTError.
    This covers the generic JWTError block (line 124).
    """
    with pytest.raises(HTTPException) as excinfo:
        await decode_token("a-bad-token", TokenType.ACCESS)
        
    assert excinfo.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Could not validate credentials" in excinfo.value.detail


## --- Tests for get_current_user() ---

@mock.patch('app.auth.jwt.decode_token')
async def test_get_current_user_not_found(mock_decode_token):
    """
    Test get_current_user when the user ID from the token is not in the DB.
    This covers the 'user is None' check (line 146).
    """
    # Setup mocks
    mock_decode_token.return_value = {"sub": str(uuid4())}
    mock_db_session = mock.MagicMock()
    mock_db_session.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token="fake_token", db=mock_db_session)
        
    assert excinfo.value.status_code == status.HTTP_404_NOT_FOUND
    assert "User not found" in excinfo.value.detail

@mock.patch('app.auth.jwt.decode_token')
async def test_get_current_user_inactive(mock_decode_token):
    """
    Test get_current_user for an inactive user.
    This covers the 'not user.is_active' check (line 152).
    """
    # Setup mocks
    mock_user = mock.MagicMock()
    mock_user.is_active = False # The crucial part for this test
    mock_decode_token.return_value = {"sub": str(uuid4())}
    mock_db_session = mock.MagicMock()
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_user

    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token="fake_token", db=mock_db_session)
        
    assert excinfo.value.status_code == status.HTTP_400_BAD_REQUEST
    assert "Inactive user" in excinfo.value.detail