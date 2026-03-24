import os
import json
import base64
from openai import OpenAI
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


def analyze_image(image_base64: str) -> TerrainAnalysis:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY não configurada")

    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": ANALYSIS_PROMPT,
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}",
                            "detail": "high",
                        },
                    },
                ],
            }
        ],
        max_tokens=2000,
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content
    data = json.loads(content)

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
