import pytest
from httpx import AsyncClient
from bson import ObjectId
from backend.auth.main import app
from backend.auth.db import db, connect_db, close_db
from backend.auth.security import hash_password


@pytest.fixture
async def client():
    """Fixture to provide async HTTP client for testing."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def test_db():
    """Fixture to initialize and clean up test database."""
    await connect_db()
    yield db
    # Cleanup
    await db.users.delete_many({})
    await close_db()


@pytest.mark.asyncio
async def test_register_new_user(client, test_db):
    """Test successful user registration."""
    response = await client.post("/register", json={
        "email": "testuser@example.com",
        "password": "securepassword123",
        "role": "user"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "testuser@example.com"
    assert data["role"] == "user"
    assert "id" in data


@pytest.mark.asyncio
async def test_register_duplicate_email(client, test_db):
    """Test registration fails with duplicate email."""
    email = "duplicate@example.com"
    # First registration
    await client.post("/register", json={
        "email": email,
        "password": "password123"
    })
    # Second registration with same email
    response = await client.post("/register", json={
        "email": email,
        "password": "password456"
    })
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]


@pytest.mark.asyncio
async def test_login_success(client, test_db):
    """Test successful login and JWT token generation."""
    email = "logintest@example.com"
    password = "testpass123"
    
    # Register user
    await client.post("/register", json={
        "email": email,
        "password": password,
        "role": "user"
    })
    
    # Login
    response = await client.post("/login", data={
        "username": email,
        "password": password
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_credentials(client, test_db):
    """Test login fails with incorrect credentials."""
    email = "user@example.com"
    await client.post("/register", json={
        "email": email,
        "password": "correctpassword"
    })
    
    response = await client.post("/login", data={
        "username": email,
        "password": "wrongpassword"
    })
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_me_authenticated(client, test_db):
    """Test retrieving current user info with valid token."""
    email = "authtest@example.com"
    password = "authpass123"
    
    # Register user
    await client.post("/register", json={
        "email": email,
        "password": password
    })
    
    # Login to get token
    login_response = await client.post("/login", data={
        "username": email,
        "password": password
    })
    token = login_response.json()["access_token"]
    
    # Get current user
    response = await client.get(
        "/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == email


@pytest.mark.asyncio
async def test_admin_only_route_denied(client, test_db):
    """Test that regular users cannot access admin-only routes."""
    email = "regularuser@example.com"
    password = "userpass123"
    
    # Register as regular user
    await client.post("/register", json={
        "email": email,
        "password": password,
        "role": "user"
    })
    
    # Login
    login_response = await client.post("/login", data={
        "username": email,
        "password": password
    })
    token = login_response.json()["access_token"]
    
    # Try to access admin route
    response = await client.get(
        "/admin-only",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403
    assert "Admin privileges required" in response.json()["detail"]


@pytest.mark.asyncio
async def test_admin_only_route_allowed(client, test_db):
    """Test that admin users can access admin-only routes."""
    email = "adminuser@example.com"
    password = "adminpass123"
    
    # Register as admin
    await client.post("/register", json={
        "email": email,
        "password": password,
        "role": "admin"
    })
    
    # Login
    login_response = await client.post("/login", data={
        "username": email,
        "password": password
    })
    token = login_response.json()["access_token"]
    
    # Access admin route
    response = await client.get(
        "/admin-only",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert "admin-only" in response.json()["message"]
