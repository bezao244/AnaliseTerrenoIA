import base64
import io

import pytest
from PIL import Image

from heatmap import generate_heatmap
from schemas import TerrainAnalysis, TerrainComponent


def _make_image_bytes(width: int = 200, height: int = 150) -> bytes:
    img = Image.new("RGB", (width, height), color=(100, 150, 100))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()


@pytest.fixture
def sample_analysis() -> TerrainAnalysis:
    return TerrainAnalysis(
        is_terrain=True,
        terrain_type="Pastagem",
        components=[
            TerrainComponent(name="Vegetação", percentage=50.0, color="#228B22"),
            TerrainComponent(name="Solo Exposto", percentage=30.0, color="#8B4513"),
            TerrainComponent(name="Rocha", percentage=20.0, color="#808080"),
        ],
        fertile_areas=["Área norte"],
        technical_report="Solo fértil.",
        recommendations=["Irrigação regular"],
        overall_fertility_score=8.0,
    )


def test_generate_heatmap(sample_analysis):
    image_bytes = _make_image_bytes()
    result = generate_heatmap(image_bytes, sample_analysis)

    assert isinstance(result, str)
    assert len(result) > 0

    decoded = base64.b64decode(result)
    img = Image.open(io.BytesIO(decoded))
    assert img.size[0] == 200
    assert img.size[1] > 150


def test_heatmap_with_empty_components():
    analysis = TerrainAnalysis(
        is_terrain=True,
        terrain_type="Desconhecido",
        components=[],
        fertile_areas=[],
        technical_report="Sem componentes.",
        recommendations=[],
        overall_fertility_score=0.0,
    )
    image_bytes = _make_image_bytes()
    result = generate_heatmap(image_bytes, analysis)

    assert isinstance(result, str)
    assert len(result) > 0

    decoded = base64.b64decode(result)
    img = Image.open(io.BytesIO(decoded))
    assert img.size[0] == 200


def test_heatmap_color_mapping():
    analysis = TerrainAnalysis(
        is_terrain=True,
        terrain_type="Floresta",
        components=[
            TerrainComponent(name="Água", percentage=25.0, color="#0077BE"),
            TerrainComponent(name="Floresta", percentage=50.0, color="#006400"),
            TerrainComponent(name="Areia", percentage=25.0, color="#F4A460"),
        ],
        fertile_areas=[],
        technical_report="Área com floresta.",
        recommendations=[],
        overall_fertility_score=6.0,
    )
    image_bytes = _make_image_bytes()
    result = generate_heatmap(image_bytes, analysis)

    assert isinstance(result, str)
    decoded = base64.b64decode(result)
    img = Image.open(io.BytesIO(decoded))
    assert img is not None
