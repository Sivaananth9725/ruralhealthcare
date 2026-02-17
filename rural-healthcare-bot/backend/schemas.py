"""
Pydantic schemas for Rural Healthcare Decision Support Bot API.
"""

from pydantic import BaseModel, Field
from typing import Optional


class QueryRequest(BaseModel):
    """
    Request schema for healthcare query endpoint.
    
    Attributes:
        symptoms (str): Patient's symptom description
    """
    symptoms: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Description of patient symptoms"
    )


class QueryResponse(BaseModel):
    """
    Response schema for healthcare query endpoint.
    
    Attributes:
        answer (str): Generated healthcare guidance response
        referral_urgency (Optional[str]): Urgency level (LOW, MEDIUM, HIGH)
    """
    answer: str = Field(
        ...,
        description="Generated healthcare guidance based on symptoms and medical guidelines"
    )
    referral_urgency: Optional[str] = Field(
        None,
        description="Referral urgency level (LOW, MEDIUM, or HIGH)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "answer": "Based on the symptoms provided...",
                "referral_urgency": "MEDIUM"
            }
        }
