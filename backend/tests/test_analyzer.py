import json
import os
from unittest.mock import patch, MagicMock

import pytest

from schemas import TerrainAnalysis, TerrainComponent


def test_analyze_no_api_key():
    with patch.dict(os.environ, {}, clear=True):
        os.environ.pop("GEMINI_API_KEY", None)
        from analyzer import analyze_image
        with pytest.raises(ValueError, match="GEMINI_API_KEY não configurada"):
            analyze_image("some_base64_image")


def test_analyze_with_mock():
    mock_response_data = {
        "is_terrain": True,
        "terrain_type": "Pastagem",
        "components": [
            {"name": "Vegetação", "percentage": 60.0, "color": "#228B22"},
            {"name": "Solo Exposto", "percentage": 40.0, "color": "#8B4513"},
        ],
        "fertile_areas": ["Área central"],
        "technical_report": "Pastagem em bom estado.",
        "recommendations": ["Rotação de cultura"],
        "overall_fertility_score": 8.0,
    }

    mock_response = MagicMock()
    mock_response.text = json.dumps(mock_response_data)

    mock_model = MagicMock()
    mock_model.generate_content.return_value = mock_response

    with patch.dict(os.environ, {"GEMINI_API_KEY": "test_key"}), \
         patch("analyzer.genai") as mock_genai:
        mock_genai.GenerativeModel.return_value = mock_model
        from analyzer import analyze_image
        result = analyze_image("dGVzdA==")

    assert result.is_terrain is True
    assert result.terrain_type == "Pastagem"
    assert len(result.components) == 2
    assert result.overall_fertility_score == 8.0

    assert mock_model.generate_content.called


def test_parse_response():
    mock_response_data = {
        "is_terrain": False,
        "terrain_type": "Não identificado",
        "components": [],
        "fertile_areas": [],
        "technical_report": "Não é terreno.",
        "recommendations": [],
        "overall_fertility_score": 0.0,
    }

    mock_response = MagicMock()
    mock_response.text = json.dumps(mock_response_data)

    mock_model = MagicMock()
    mock_model.generate_content.return_value = mock_response

    with patch.dict(os.environ, {"GEMINI_API_KEY": "test_key"}), \
         patch("analyzer.genai") as mock_genai:
        mock_genai.GenerativeModel.return_value = mock_model
        from analyzer import analyze_image
        result = analyze_image("dGVzdA==")

    assert result.is_terrain is False
    assert result.overall_fertility_score == 0.0
    assert result.components == []


def test_extract_json_with_markdown_fences():
    from analyzer import _extract_json

    json_str = '```json\n{"is_terrain": true}\n```'
    result = _extract_json(json_str)
    assert result == {"is_terrain": True}


def test_extract_json_plain():
    from analyzer import _extract_json

    json_str = '{"is_terrain": false}'
    result = _extract_json(json_str)
    assert result == {"is_terrain": False}
