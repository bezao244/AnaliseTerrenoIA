import os
import json
import base64
import re
import google.generativeai as genai
from schemas import TerrainAnalysis, TerrainComponent


ANALYSIS_PROMPT = """Analise esta imagem de terreno e retorne APENAS um objeto JSON válido (sem markdown, sem texto adicional) com a seguinte estrutura:

{
  "is_terrain": true,
  "terrain_type": "Tipo do terreno (ex: Solo Argiloso, Pastagem, Floresta, etc.)",
  "components": [
    {"name": "Vegetação", "percentage": 40.0, "color": "#228B22"},
    {"name": "Solo Exposto", "percentage": 30.0, "color": "#8B4513"},
    {"name": "Rocha", "percentage": 20.0, "color": "#808080"},
    {"name": "Água", "percentage": 10.0, "color": "#0077BE"}
  ],
  "fertile_areas": ["Área norte com vegetação densa", "Vale com solo úmido"],
  "technical_report": "Relatório técnico detalhado sobre o terreno analisado...",
  "recommendations": [
    "Recomendação 1 para uso do terreno",
    "Recomendação 2 para manejo"
  ],
  "overall_fertility_score": 7.5
}

Se a imagem NÃO for um terreno (ex: foto de pessoa, objeto, etc.), retorne:
{
  "is_terrain": false,
  "terrain_type": "Não identificado",
  "components": [],
  "fertile_areas": [],
  "technical_report": "A imagem fornecida não representa um terreno.",
  "recommendations": [],
  "overall_fertility_score": 0.0
}

IMPORTANTE: Retorne SOMENTE o JSON, sem blocos de código ou texto adicional."""


def _extract_json(text: str) -> dict:
    """Extract JSON from response text, stripping markdown fences if present."""
    cleaned = text.strip()
    match = re.search(r"```(?:json)?\s*(.*?)\s*```", cleaned, re.DOTALL)
    if match:
        cleaned = match.group(1)
    return json.loads(cleaned)


def analyze_image(image_base64: str) -> TerrainAnalysis:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY não configurada")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-1.5-flash")

    image_data = base64.b64decode(image_base64)

    response = model.generate_content(
        [
            ANALYSIS_PROMPT,
            {"mime_type": "image/jpeg", "data": image_data},
        ],
        generation_config=genai.types.GenerationConfig(
            max_output_tokens=2000,
        ),
    )

    data = _extract_json(response.text)

    components = [TerrainComponent(**c) for c in data.get("components", [])]

    return TerrainAnalysis(
        is_terrain=data.get("is_terrain", False),
        terrain_type=data.get("terrain_type", "Não identificado"),
        components=components,
        fertile_areas=data.get("fertile_areas", []),
        technical_report=data.get("technical_report", ""),
        recommendations=data.get("recommendations", []),
        overall_fertility_score=float(data.get("overall_fertility_score", 0.0)),
    )
