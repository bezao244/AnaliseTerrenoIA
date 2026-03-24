import json
import os
from unittest.mock import patch, MagicMock

import pytest

from schemas import TerrainAnalysis, TerrainComponent


def test_analyze_no_api_key():
    with patch.dict(os.environ, {}, clear=True):
        os.environ.pop("OPENAI_API_KEY", None)
        from analyzer import analyze_image
        with pytest.raises(ValueError, match="OPENAI_API_KEY não configurada"):
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

    mock_message = MagicMock()
    mock_message.content = json.dumps(mock_response_data)

    mock_choice = MagicMock()
    mock_choice.message = mock_message

    mock_completion = MagicMock()
    mock_completion.choices = [mock_choice]

    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_completion

    with patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"}), \
         patch("analyzer.OpenAI", return_value=mock_client):
        from analyzer import analyze_image
        result = analyze_image("base64encodedimage")

    assert result.is_terrain is True
    assert result.terrain_type == "Pastagem"
    assert len(result.components) == 2
    assert result.overall_fertility_score == 8.0

    call_args = mock_client.chat.completions.create.call_args
    assert call_args is not None
    kwargs = call_args.kwargs if call_args.kwargs else call_args[1]
    messages = kwargs.get("messages") or call_args[0][0] if call_args[0] else []
    assert mock_client.chat.completions.create.called


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

    mock_message = MagicMock()
    mock_message.content = json.dumps(mock_response_data)

    mock_choice = MagicMock()
    mock_choice.message = mock_message

    mock_completion = MagicMock()
    mock_completion.choices = [mock_choice]

    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_completion

    with patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"}), \
         patch("analyzer.OpenAI", return_value=mock_client):
        from analyzer import analyze_image
        result = analyze_image("base64image")

    assert result.is_terrain is False
    assert result.overall_fertility_score == 0.0
    assert result.components == []
