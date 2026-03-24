from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class TerrainComponent(BaseModel):
    name: str
    percentage: float
    color: str


class TerrainAnalysis(BaseModel):
    is_terrain: bool
    terrain_type: str
    components: List[TerrainComponent]
    fertile_areas: List[str]
    technical_report: str
    recommendations: List[str]
    overall_fertility_score: float


class AnalysisCreate(BaseModel):
    filename: str
    original_image: str
    heatmap_image: Optional[str] = None
    analysis_result: str


class AnalysisResponse(BaseModel):
    id: int
    filename: str
    original_image: str
    heatmap_image: Optional[str] = None
    analysis_result: TerrainAnalysis
    created_at: datetime

    class Config:
        from_attributes = True
