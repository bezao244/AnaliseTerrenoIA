import base64
import io
import json
from datetime import datetime
from unittest.mock import patch, MagicMock

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base, get_db
from main import app
from schemas import TerrainAnalysis, TerrainComponent

TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(setup_database):
    with TestClient(app) as c:
        yield c


@pytest.fixture
def sample_analysis() -> TerrainAnalysis:
    return TerrainAnalysis(
        is_terrain=True,
        terrain_type="Solo Argiloso",
        components=[
            TerrainComponent(name="Vegetação", percentage=40.0, color="#228B22"),
            TerrainComponent(name="Solo Exposto", percentage=35.0, color="#8B4513"),
            TerrainComponent(name="Rocha", percentage=25.0, color="#808080"),
        ],
        fertile_areas=["Área norte com vegetação densa"],
        technical_report="Solo com boa capacidade de retenção hídrica.",
        recommendations=["Realizar análise química do solo", "Irrigação moderada"],
        overall_fertility_score=7.5,
    )


def _make_test_image() -> bytes:
    from PIL import Image
    img = Image.new("RGB", (100, 100), color=(34, 139, 34))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


def test_upload_image(client, sample_analysis):
    image_bytes = _make_test_image()

    with patch("main.analyze_image", return_value=sample_analysis), \
         patch("main.generate_heatmap", return_value=base64.b64encode(image_bytes).decode()):

        response = client.post(
            "/api/analyses",
            files={"file": ("test_terrain.jpg", image_bytes, "image/jpeg")},
        )

    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "test_terrain.jpg"
    assert data["analysis_result"]["terrain_type"] == "Solo Argiloso"
    assert data["analysis_result"]["overall_fertility_score"] == 7.5
    assert "id" in data


def test_list_analyses(client, sample_analysis):
    image_bytes = _make_test_image()

    with patch("main.analyze_image", return_value=sample_analysis), \
         patch("main.generate_heatmap", return_value=base64.b64encode(image_bytes).decode()):
        client.post(
            "/api/analyses",
            files={"file": ("terrain1.jpg", image_bytes, "image/jpeg")},
        )
        client.post(
            "/api/analyses",
            files={"file": ("terrain2.jpg", image_bytes, "image/jpeg")},
        )

    response = client.get("/api/analyses")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2


def test_get_analysis(client, sample_analysis):
    image_bytes = _make_test_image()

    with patch("main.analyze_image", return_value=sample_analysis), \
         patch("main.generate_heatmap", return_value=base64.b64encode(image_bytes).decode()):
        create_resp = client.post(
            "/api/analyses",
            files={"file": ("terrain.jpg", image_bytes, "image/jpeg")},
        )

    analysis_id = create_resp.json()["id"]
    response = client.get(f"/api/analyses/{analysis_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == analysis_id
    assert data["filename"] == "terrain.jpg"


def test_get_analysis_not_found(client):
    response = client.get("/api/analyses/99999")
    assert response.status_code == 404


def test_get_heatmap(client, sample_analysis):
    image_bytes = _make_test_image()
    heatmap_b64 = base64.b64encode(image_bytes).decode()

    with patch("main.analyze_image", return_value=sample_analysis), \
         patch("main.generate_heatmap", return_value=heatmap_b64):
        create_resp = client.post(
            "/api/analyses",
            files={"file": ("terrain.jpg", image_bytes, "image/jpeg")},
        )

    analysis_id = create_resp.json()["id"]
    response = client.get(f"/api/analyses/{analysis_id}/heatmap")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"


def test_get_report(client, sample_analysis):
    image_bytes = _make_test_image()

    with patch("main.analyze_image", return_value=sample_analysis), \
         patch("main.generate_heatmap", return_value=base64.b64encode(image_bytes).decode()):
        create_resp = client.post(
            "/api/analyses",
            files={"file": ("terrain.jpg", image_bytes, "image/jpeg")},
        )

    analysis_id = create_resp.json()["id"]
    response = client.get(f"/api/analyses/{analysis_id}/report")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert len(response.content) > 0


def test_not_terrain(client):
    not_terrain = TerrainAnalysis(
        is_terrain=False,
        terrain_type="Não identificado",
        components=[],
        fertile_areas=[],
        technical_report="A imagem fornecida não representa um terreno.",
        recommendations=[],
        overall_fertility_score=0.0,
    )
    image_bytes = _make_test_image()

    with patch("main.analyze_image", return_value=not_terrain):
        response = client.post(
            "/api/analyses",
            files={"file": ("not_terrain.jpg", image_bytes, "image/jpeg")},
        )

    assert response.status_code == 422
    data = response.json()
    assert "terreno" in data["detail"].lower()
