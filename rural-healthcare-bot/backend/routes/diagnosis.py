"""
FastAPI router for healthcare diagnosis endpoint.
Integrates RAG context retrieval and LLM response generation.
"""

import logging
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schemas import QueryRequest, QueryResponse
from db import get_db
from models import PatientQuery
from rag import retrieve_context
from services.llm_service import generate_answer

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api",
    tags=["diagnosis"],
)


@router.post("/diagnose", response_model=QueryResponse)
async def diagnose(
    query: QueryRequest,
    db: Session = Depends(get_db)
) -> QueryResponse:
    """
    Diagnose endpoint for healthcare guidance.
    
    Process:
    1. Retrieve relevant medical guidelines using RAG
    2. Generate healthcare guidance using Groq LLM
    3. Save query and response to database
    4. Return formatted response with referral urgency
    
    Args:
        query (QueryRequest): Patient symptoms query
        db (Session): Database session dependency
    
    Returns:
        QueryResponse: Healthcare guidance response with urgency level
    """
    try:
        logger.info(f"Processing diagnosis request for symptoms: {query.symptoms[:100]}...")
        
        # Step 1: Retrieve relevant guidelines using RAG
        logger.info("Retrieving relevant medical guidelines...")
        context = retrieve_context(query.symptoms, k=3)
        
        # Step 2: Generate response using LLM
        logger.info("Generating healthcare guidance...")
        answer, referral_urgency = generate_answer(query.symptoms, context)
        
        # Step 3: Save to database
        logger.info("Saving query to database...")
        db_query = PatientQuery(
            symptoms=query.symptoms,
            response=answer
        )
        db.add(db_query)
        db.commit()
        db.refresh(db_query)
        logger.info(f"Query saved with ID: {db_query.id}")
        
        # Step 4: Return response
        response = QueryResponse(
            answer=answer,
            referral_urgency=referral_urgency
        )
        
        logger.info("Diagnosis request processed successfully")
        return response
        
    except Exception as e:
        logger.error(f"Error processing diagnosis request: {e}")
        
        # Return error response
        return QueryResponse(
            answer=f"An error occurred while processing your request: {str(e)}. Please try again.",
            referral_urgency=None
        )
