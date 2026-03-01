"""
Kronaghor - Backend Tests
Tests para endpoints y funcionalidades.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set test database before importing app
os.environ["DATABASE_URL"] = "sqlite:///./test_kronaghor.db"

import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session

from main import app
from db.database import engine as default_engine


# Create test engine
test_engine = create_engine("sqlite:///./test_kronaghor.db", echo=False)


@pytest.fixture(autouse=True)
def setup_test_db():
    """Setup test database."""
    # Create tables
    SQLModel.metadata.create_all(test_engine)
    yield
    # Clean up
    SQLModel.metadata.drop_all(test_engine)


def get_test_session():
    """Get test session."""
    with Session(test_engine) as session:
        yield session


# Override dependency
from fastapi import Depends
from backend.db.database import get_session

app.dependency_overrides[get_session] = get_test_session


# Test client
client = TestClient(app)


class TestHealth:
    """Tests de salud."""
    
    def test_health_check(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_root(self):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "Kronaghor" in data["name"]


class TestAuth:
    """Tests de autenticación."""
    
    def test_register(self):
        response = client.post("/api/auth/register", json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpass123"
        })
        assert response.status_code == 200
        assert response.json()["username"] == "testuser"
    
    def test_login(self):
        # Register first
        client.post("/api/auth/register", json={
            "email": "login@example.com",
            "username": "loginuser",
            "password": "password123"
        })
        
        response = client.post("/api/auth/login", data={
            "username": "loginuser",
            "password": "password123"
        })
        assert response.status_code == 200
        assert "access_token" in response.json()
    
    def test_login_invalid(self):
        response = client.post("/api/auth/login", data={
            "username": "nonexistent",
            "password": "wrongpass"
        })
        assert response.status_code == 401
    
    def test_get_me_with_token(self):
        # Register and login
        client.post("/api/auth/register", json={
            "email": "me@example.com",
            "username": "meuser",
            "password": "password123"
        })
        
        login_resp = client.post("/api/auth/login", data={
            "username": "meuser",
            "password": "password123"
        })
        token = login_resp.json()["access_token"]
        
        response = client.get("/api/auth/me", headers={
            "Authorization": f"Bearer {token}"
        })
        assert response.status_code == 200


class TestExpedientes:
    """Tests de expedientes."""
    
    @pytest.fixture
    def auth_headers(self):
        client.post("/api/auth/register", json={
            "email": "exp@example.com",
            "username": "expuser",
            "password": "password123"
        })
        
        login_resp = client.post("/api/auth/login", data={
            "username": "expuser",
            "password": "password123"
        })
        token = login_resp.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    
    def test_create_expediente(self, auth_headers):
        response = client.post("/api/expedientes",
            headers=auth_headers,
            json={
                "numero": "2026-001-TEST",
                "tipo": "civil",
                "demandante": "Test Demandante",
                "demandado": "Test Demandado"
            }
        )
        assert response.status_code == 200
        assert response.json()["numero"] == "2026-001-TEST"
    
    def test_list_expedientes(self, auth_headers):
        response = client.get("/api/expedientes", headers=auth_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_get_expediente(self, auth_headers):
        create_resp = client.post("/api/expedientes",
            headers=auth_headers,
            json={"numero": "2026-002-TEST", "tipo": "penal"}
        )
        exp_id = create_resp.json()["id"]
        
        response = client.get(f"/api/expedientes/{exp_id}", headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["numero"] == "2026-002-TEST"
    
    def test_delete_expediente(self, auth_headers):
        create_resp = client.post("/api/expedientes",
            headers=auth_headers,
            json={"numero": "2026-004-TEST", "tipo": "laboral"}
        )
        exp_id = create_resp.json()["id"]
        
        response = client.delete(f"/api/expedientes/{exp_id}", headers=auth_headers)
        assert response.status_code == 200


class TestAudiencias:
    """Tests de audiencias."""
    
    @pytest.fixture
    def auth_headers(self):
        client.post("/api/auth/register", json={
            "email": "aud@example.com",
            "username": "auduser",
            "password": "password123"
        })
        
        login_resp = client.post("/api/auth/login", data={
            "username": "auduser",
            "password": "password123"
        })
        token = login_resp.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    
    def test_create_audiencia(self, auth_headers):
        exp_resp = client.post("/api/expedientes",
            headers=auth_headers,
            json={"numero": "2026-010-TEST", "tipo": "civil"}
        )
        exp_id = exp_resp.json()["id"]
        
        response = client.post("/api/audiencias",
            headers=auth_headers,
            json={
                "expediente_id": exp_id,
                "tipo": "conciliación",
                "fecha": "2026-03-15T10:00:00",
                "duracion_minutos": 60
            }
        )
        assert response.status_code == 200


class TestMetrics:
    """Tests de métricas."""
    
    @pytest.fixture
    def auth_headers(self):
        client.post("/api/auth/register", json={
            "email": "metrics@example.com",
            "username": "metricsuser",
            "password": "password123"
        })
        
        login_resp = client.post("/api/auth/login", data={
            "username": "metricsuser",
            "password": "password123"
        })
        token = login_resp.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    
    def test_dashboard(self, auth_headers):
        response = client.get("/api/metrics/dashboard", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "total_expedientes" in data
