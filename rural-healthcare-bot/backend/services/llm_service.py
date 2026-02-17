"""
Groq LLM service for generating healthcare guidance responses.
Uses Groq API with llama-3.3-70b-versatile model.
"""

import os
import logging
from typing import Optional
from groq import Groq

logger = logging.getLogger(__name__)

# Initialize Groq client
client = None


def initialize_groq() -> bool:
    """
    Initialize Groq client with API key from environment variable.
    
    Returns:
        bool: True if initialized successfully, False otherwise
    """
    global client
    
    try:
        api_key = os.getenv("GROQ_API_KEY")
        
        if not api_key:
            logger.error("GROQ_API_KEY environment variable not set")
            return False
        
        client = Groq(api_key=api_key)
        logger.info("Groq client initialized successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error initializing Groq client: {e}")
        return False


def generate_answer(symptoms: str, context: str) -> tuple[str, Optional[str]]:
    """
    Generate healthcare guidance response using Groq LLM.
    
    Args:
        symptoms (str): Patient's symptom description
        context (str): Medical guideline context retrieved by RAG
    
    Returns:
        tuple: (answer, referral_urgency) where answer is the generated response
               and referral_urgency is one of "LOW", "MEDIUM", "HIGH" or None
    """
    global client
    
    if client is None:
        logger.warning("Groq client not initialized. Calling initialize_groq()...")
        if not initialize_groq():
            return ("Unable to generate response: Groq service not available", None)
    
    try:
        # System prompt for rural healthcare assistant
        system_prompt = """You are a Rural Healthcare Decision Support Assistant. Your role is to:
1. Provide preliminary health guidance based on symptoms and medical guidelines
2. NEVER provide final diagnosis - emphasize this is preliminary support only
3. Suggest when referral to a healthcare provider is needed with urgency level
4. Be empathetic and clear in your language
5. Recommend appropriate referral urgency: LOW (routine checkup), MEDIUM (within a few days), or HIGH (urgent/emergency)

IMPORTANT: Always remind users that this is not a medical diagnosis and they should consult a qualified healthcare provider."""

        # User message combining symptoms and context
        user_message = f"""Based on the following medical guidelines and patient symptoms, provide preliminary health guidance:

PATIENT SYMPTOMS:
{symptoms}

MEDICAL GUIDELINES CONTEXT:
{context}

Please provide:
1. Preliminary health guidance based on the symptoms and guidelines
2. Possible conditions to discuss with a healthcare provider
3. Recommended referral urgency level (LOW, MEDIUM, or HIGH)
4. Home care recommendations if appropriate"""

        # Call Groq API
        message = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            max_tokens=1024,
            temperature=0.7,
        )
        
        response_text = message.choices[0].message.content
        
        # Extract referral urgency from response
        referral_urgency = None
        if "HIGH" in response_text.upper():
            referral_urgency = "HIGH"
        elif "MEDIUM" in response_text.upper():
            referral_urgency = "MEDIUM"
        elif "LOW" in response_text.upper():
            referral_urgency = "LOW"
        
        logger.info(f"Generated response with urgency level: {referral_urgency}")
        
        return response_text, referral_urgency
        
    except Exception as e:
        logger.error(f"Error generating response from Groq: {e}")
        return (f"Error generating health guidance: {str(e)}", None)
