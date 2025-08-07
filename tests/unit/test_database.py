# tests/unit/test_database.py

import pytest
from unittest import mock
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import Engine
from unittest.mock import patch


from app.database import get_db, get_engine, get_sessionmaker

def test_get_engine_and_sessionmaker():
    """
    Tests the factory functions for creating an engine and sessionmaker.
    It uses an in-memory SQLite database for speed and isolation.
    """
    # Use an in-memory SQLite DB for this test
    test_db_url = "sqlite:///:memory:"
    
    # 1. Test get_engine()
    engine = get_engine(database_url=test_db_url)
    assert isinstance(engine, Engine)
    assert str(engine.url) == test_db_url

    # 2. Test get_sessionmaker()
    TestSessionLocal = get_sessionmaker(engine)
    assert isinstance(TestSessionLocal, sessionmaker)

    # Verify that we can create a session from the new sessionmaker
    db = TestSessionLocal()
    assert isinstance(db, Session)
    db.close()

@mock.patch('app.database.SessionLocal')

def test_get_db_yields_session_and_closes(mock_session_local):
    """
    Tests that the get_db generator yields a session and then closes it.
    """
    # Get the generator from your function
    db_generator = get_db()

    # The first `next()` call runs the `try` block and yields the session
    session = next(db_generator)

    # 1. Assert that the yielded object is a real SQLAlchemy Session
    assert isinstance(session, Session)

    # 2. We mock the `close` method on the specific session object that was yielded
    with patch.object(session, 'close') as mock_close:

        # 3. Exhaust the generator to trigger the 'finally' block
        with pytest.raises(StopIteration):
            next(db_generator)

        # 4. Assert that the mocked `close` method was called exactly once
        mock_close.assert_called_once()