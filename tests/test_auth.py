from datetime import timedelta
import pytest
from httpx import AsyncClient

from app.core.security import create_access_token


@pytest.mark.asyncio
async def test_register_user(async_client: AsyncClient) -> None:
    response = await async_client.post(
        "/api/v1/auth/register",
        json={"email": "alice@example.com", "password": "supersecretpassword"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "alice@example.com"
    assert data["is_active"] is True
    assert "id" in data
    assert "password" not in data
    assert "hashed_password" not in data


@pytest.mark.asyncio
async def test_register_duplicate_user(async_client: AsyncClient) -> None:
    # First registration
    await async_client.post(
        "/api/v1/auth/register",
        json={"email": "duplicate@example.com", "password": "password123"},
    )
    # Second registration should fail
    response = await async_client.post(
        "/api/v1/auth/register",
        json={"email": "duplicate@example.com", "password": "anotherpassword"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "User with this email already exists"


@pytest.mark.asyncio
async def test_login_oauth2_and_protected_route(async_client: AsyncClient) -> None:
    # Register user
    await async_client.post(
        "/api/v1/auth/register",
        json={"email": "bob@example.com", "password": "mypassword123"},
    )

    # Login with form data (OAuth2 standard)
    login_response = await async_client.post(
        "/api/v1/auth/login",
        data={"username": "bob@example.com", "password": "mypassword123"},
    )
    assert login_response.status_code == 200
    tokens = login_response.json()
    assert "access_token" in tokens
    assert tokens["token_type"] == "bearer"

    token = tokens["access_token"]

    # Access protected /users/me
    me_response = await async_client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert me_response.status_code == 200
    me_data = me_response.json()
    assert me_data["email"] == "bob@example.com"


@pytest.mark.asyncio
async def test_login_json(async_client: AsyncClient) -> None:
    await async_client.post(
        "/api/v1/auth/register",
        json={"email": "charlie@example.com", "password": "charliepassword"},
    )

    login_response = await async_client.post(
        "/api/v1/auth/login/json",
        json={"email": "charlie@example.com", "password": "charliepassword"},
    )
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()


@pytest.mark.asyncio
async def test_login_invalid_password(async_client: AsyncClient) -> None:
    await async_client.post(
        "/api/v1/auth/register",
        json={"email": "dana@example.com", "password": "correctpassword"},
    )

    response = await async_client.post(
        "/api/v1/auth/login/json",
        json={"email": "dana@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"


@pytest.mark.asyncio
async def test_access_protected_route_without_token(async_client: AsyncClient) -> None:
    response = await async_client.get("/api/v1/users/me")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_access_protected_route_with_expired_token(async_client: AsyncClient) -> None:
    expired_token = create_access_token(
        subject="expired@example.com",
        expires_delta=timedelta(seconds=-10),
    )
    response = await async_client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {expired_token}"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"
