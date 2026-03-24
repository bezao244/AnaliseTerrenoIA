from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from database import Base


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    original_image = Column(Text, nullable=False)
    heatmap_image = Column(Text, nullable=True)
    analysis_result = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
