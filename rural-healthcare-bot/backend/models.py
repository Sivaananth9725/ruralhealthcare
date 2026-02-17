"""
SQLAlchemy models for Rural Healthcare Decision Support Bot.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from db import Base


class PatientQuery(Base):
    """
    Model for storing patient health queries and responses.
    
    Columns:
        id (int): Primary key
        symptoms (str): Patient's symptoms description
        response (str): Generated healthcare guidance response
        created_at (datetime): Timestamp when query was created
    """
    __tablename__ = "patient_queries"

    id = Column(Integer, primary_key=True, index=True)
    symptoms = Column(String(500), nullable=False)
    response = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<PatientQuery(id={self.id}, symptoms={self.symptoms[:50]}...)>"
