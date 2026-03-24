import base64
import json
from datetime import datetime
from typing import List

from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from sqlalchemy.orm import Session

from database import get_db, create_tables
from models import Analysis
from schemas import AnalysisResponse, TerrainAnalysis
from analyzer import analyze_image
from heatmap import generate_heatmap
from pdf_export import generate_pdf

app = FastAPI(title="AnaliseTerrenoIA API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    create_tables()


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "AnaliseTerrenoIA API está funcionando"}


@app.post("/api/analyses", response_model=AnalysisResponse)
async def create_analysis(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    image_bytes = await file.read()
    if not image_bytes:
        raise HTTPException(status_code=400, detail="Arquivo de imagem vazio")

    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    terrain_analysis = analyze_image(image_base64)

    if not terrain_analysis.is_terrain:
        raise HTTPException(
            status_code=422,
            detail="A imagem fornecida não representa um terreno válido"
        )

    heatmap_base64 = None
    try:
        heatmap_base64 = generate_heatmap(image_bytes, terrain_analysis)
    except Exception:
        pass

    analysis_json = terrain_analysis.model_dump_json()

    db_analysis = Analysis(
        filename=file.filename,
        original_image=image_base64,
        heatmap_image=heatmap_base64,
        analysis_result=analysis_json,
        created_at=datetime.utcnow(),
    )
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)

    return _to_response(db_analysis)


@app.get("/api/analyses", response_model=List[AnalysisResponse])
def list_analyses(db: Session = Depends(get_db)):
    analyses = db.query(Analysis).order_by(Analysis.id.desc()).all()
    return [_to_response(a) for a in analyses]


@app.get("/api/analyses/{analysis_id}", response_model=AnalysisResponse)
def get_analysis(analysis_id: int, db: Session = Depends(get_db)):
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Análise não encontrada")
    return _to_response(analysis)


@app.get("/api/analyses/{analysis_id}/heatmap")
def get_heatmap(analysis_id: int, db: Session = Depends(get_db)):
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Análise não encontrada")
    if not analysis.heatmap_image:
        raise HTTPException(status_code=404, detail="Mapa de calor não disponível")

    image_bytes = base64.b64decode(analysis.heatmap_image)
    return Response(content=image_bytes, media_type="image/png")


@app.get("/api/analyses/{analysis_id}/report")
def get_report(analysis_id: int, db: Session = Depends(get_db)):
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Análise não encontrada")

    terrain_analysis = TerrainAnalysis.model_validate_json(analysis.analysis_result)
    created_at = analysis.created_at or datetime.utcnow()

    pdf_bytes = generate_pdf(analysis.filename, terrain_analysis, created_at)

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="relatorio_{analysis_id}.pdf"'
        },
    )


def _to_response(analysis: Analysis) -> AnalysisResponse:
    return AnalysisResponse(
        id=analysis.id,
        filename=analysis.filename,
        original_image=analysis.original_image,
        heatmap_image=analysis.heatmap_image,
        analysis_result=TerrainAnalysis.model_validate_json(analysis.analysis_result),
        created_at=analysis.created_at or datetime.utcnow(),
    )
