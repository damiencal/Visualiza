"""
Tests for authentication endpoints: register, login, /me, refresh.
"""
from __future__ import annotations

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


BASE = "/api/v1/auth"


@pytest.mark.asyncio
class TestRegister:
    async def test_register_success(self, client: AsyncClient):
        resp = await client.post(
            f"{BASE}/register",
            json={
                "email": "newuser@example.com",
                "password": "Secure123!",
                "full_name": "New User",
            },
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["email"] == "newuser@example.com"
        assert "id" in data
        assert "hashed_password" not in data

    async def test_register_duplicate_email(self, client: AsyncClient):
        payload = {
            "email": "dup@example.com",
            "password": "Secure123!",
            "full_name": "Dup User",
        }
        r1 = await client.post(f"{BASE}/register", json=payload)
        r2 = await client.post(f"{BASE}/register", json=payload)
        assert r1.status_code == 201
        assert r2.status_code in (400, 409, 422)

    async def test_register_invalid_email(self, client: AsyncClient):
        resp = await client.post(
            f"{BASE}/register",
            json={"email": "not-an-email", "password": "Secure123!", "full_name": "X"},
        )
        assert resp.status_code == 422


@pytest.mark.asyncio
class TestLogin:
    async def test_login_success(self, client: AsyncClient, db: AsyncSession):
        # Register first
        await client.post(
            f"{BASE}/register",
            json={
                "email": "logintest@example.com",
                "password": "Login123!",
                "full_name": "Login Test",
            },
        )
        resp = await client.post(
            f"{BASE}/login",
            json={"email": "logintest@example.com", "password": "Login123!"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

    async def test_login_wrong_password(self, client: AsyncClient):
        await client.post(
            f"{BASE}/register",
            json={"email": "wrongpass@example.com", "password": "Good123!", "full_name": "X"},
        )
        resp = await client.post(
            f"{BASE}/login",
            json={"email": "wrongpass@example.com", "password": "WrongPassword"},
        )
        assert resp.status_code in (400, 401)

    async def test_login_nonexistent_user(self, client: AsyncClient):
        resp = await client.post(
            f"{BASE}/login",
            json={"email": "ghost@example.com", "password": "Ghost123!"},
        )
        assert resp.status_code in (400, 401, 404)


@pytest.mark.asyncio
class TestMe:
    async def test_me_authenticated(self, client: AsyncClient, admin_headers: dict):
        resp = await client.get(f"{BASE}/me", headers=admin_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["email"] == "testadmin@visualisa.web.do"
        assert data["role"] == "admin"

    async def test_me_unauthenticated(self, client: AsyncClient):
        resp = await client.get(f"{BASE}/me")
        assert resp.status_code in (401, 403)

    async def test_me_invalid_token(self, client: AsyncClient):
        resp = await client.get(
            f"{BASE}/me", headers={"Authorization": "Bearer invalidtoken"}
        )
        assert resp.status_code in (401, 403)
