import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from uuid import uuid4

from app.main import app
from app.database import Base, get_db
from app.auth.dependencies import get_current_user
from app.auth.jwt import get_password_hash
from app.models import User, Calculation

# --- Test Database Setup ---
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# --- Pytest Fixture for the Test Client ---

@pytest.fixture(scope="function")
def client():
    """
    A fixture that creates a new database and client for each test.
    This ensures complete test isolation.
    """
    # 1. Create all tables in the in-memory database
    Base.metadata.create_all(bind=engine)
    
    # 2. Set up dependency overrides using a local session
    db = TestingSessionLocal()
    
    test_user = User(
        id=uuid4(), email="test@example.com", username="testuser",
        password=get_password_hash("testpassword123"),
        first_name="Test", last_name="User",
        is_active=True, is_verified=True,
    )
    db.add(test_user)
    db.commit()

    def override_get_db():
        yield db

    def override_get_current_user():
        # Query the user from the test session to ensure it's attached
        return db.query(User).filter(User.id == test_user.id).first()

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user

    # 3. Yield the client for the test to use
    yield TestClient(app)

    # 4. Clean up after the test is done
    db.close()
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


# --- HTML Web Route Tests ---

@pytest.mark.parametrize("path", [
    "/",
    "/login",
    "/register",
    "/dashboard",
    "/dashboard/view/some-fake-id",
    "/dashboard/edit/some-fake-id",
])
def test_html_web_routes(client, path):
    """Test that all basic HTML pages return a 200 OK status."""
    response = client.get(path)
    assert response.status_code == 200
    assert "text/html" in response.headers['content-type']


