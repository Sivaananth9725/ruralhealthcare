"""
RAG (Retrieval-Augmented Generation) module for clinical guidelines.
Loads PDF files from guidelines folder, creates FAISS index, and provides retrieval functions.
"""

import os
import numpy as np
from typing import List, Tuple
from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss
import logging

try:
    from PyPDF2 import PdfReader
except ImportError:
    PdfReader = None

logger = logging.getLogger(__name__)

# Initialize sentence transformer model for embeddings
MODEL_NAME = "all-MiniLM-L6-v2"
embedder = None
faiss_index = None
guideline_chunks = []


def load_guidelines() -> bool:
    """
    Load PDF files from backend/guidelines folder and create FAISS index.
    
    Returns:
        bool: True if guidelines loaded successfully, False otherwise
    """
    global embedder, faiss_index, guideline_chunks
    
    try:
        # Initialize embedder
        logger.info(f"Loading embedder model: {MODEL_NAME}")
        embedder = SentenceTransformer(MODEL_NAME)
        
        # Get guidelines folder path
        guidelines_path = Path(__file__).parent / "guidelines"
        
        if not guidelines_path.exists():
            logger.warning(f"Guidelines folder not found at {guidelines_path}")
            # Create empty index for testing
            embeddings = embedder.encode(["No guidelines available"])
            faiss_index = faiss.IndexFlatL2(embeddings.shape[1])
            guideline_chunks = ["No clinical guidelines available. Please add PDF files to the guidelines folder."]
            return False
        
        # Extract text from all PDF files
        all_text = []
        pdf_files = list(guidelines_path.glob("*.pdf"))
        
        if not pdf_files:
            logger.warning("No PDF files found in guidelines folder")
            embeddings = embedder.encode(["No guidelines available"])
            faiss_index = faiss.IndexFlatL2(embeddings.shape[1])
            guideline_chunks = ["No clinical guidelines available. Please add PDF files to the guidelines folder."]
            return False
        
        logger.info(f"Found {len(pdf_files)} PDF files")
        
        for pdf_file in pdf_files:
            try:
                logger.info(f"Reading PDF: {pdf_file.name}")
                if PdfReader is None:
                    logger.warning(f"PyPDF2 not installed, skipping PDF: {pdf_file.name}")
                    continue
                    
                pdf_reader = PdfReader(pdf_file)
                
                for page_num, page in enumerate(pdf_reader.pages):
                    text = page.extract_text()
                    if text.strip():
                        all_text.append(text)
            except Exception as e:
                logger.error(f"Error reading PDF {pdf_file.name}: {e}")
                continue
        
        # Split text into chunks (sentence-level chunking)
        guideline_chunks = split_into_chunks(all_text, chunk_size=200)
        
        if not guideline_chunks:
            logger.warning("No text extracted from PDFs")
            embeddings = embedder.encode(["No guidelines available"])
            faiss_index = faiss.IndexFlatL2(embeddings.shape[1])
            guideline_chunks = ["No valid text extracted from guidelines."]
            return False
        
        logger.info(f"Created {len(guideline_chunks)} text chunks")
        
        # Create embeddings
        logger.info("Creating embeddings...")
        embeddings = embedder.encode(guideline_chunks, show_progress_bar=True)
        embeddings = embeddings.astype(np.float32)
        
        # Create FAISS index
        dimension = embeddings.shape[1]
        faiss_index = faiss.IndexFlatL2(dimension)
        faiss_index.add(embeddings)
        
        logger.info(f"FAISS index created with {faiss_index.ntotal} vectors")
        return True
        
    except Exception as e:
        logger.error(f"Error loading guidelines: {e}")
        return False


def split_into_chunks(texts: List[str], chunk_size: int = 200) -> List[str]:
    """
    Split texts into chunks by word count.
    
    Args:
        texts (List[str]): List of text strings to chunk
        chunk_size (int): Number of words per chunk
    
    Returns:
        List[str]: List of text chunks
    """
    chunks = []
    
    for text in texts:
        words = text.split()
        
        for i in range(0, len(words), chunk_size):
            chunk = " ".join(words[i:i + chunk_size])
            if chunk.strip():
                chunks.append(chunk)
    
    return chunks


def retrieve_context(query: str, k: int = 3) -> str:
    """
    Retrieve top matching guideline chunks for a query using FAISS.
    
    Args:
        query (str): User query/symptoms
        k (int): Number of top chunks to retrieve (default: 3)
    
    Returns:
        str: Concatenated context from top matching chunks
    """
    global embedder, faiss_index, guideline_chunks
    
    if embedder is None or faiss_index is None:
        logger.warning("Guidelines not loaded. Call load_guidelines() first.")
        return "No clinical guidelines available."
    
    if len(guideline_chunks) == 0:
        return "No clinical guidelines available."
    
    try:
        # Encode query
        query_embedding = embedder.encode([query])
        query_embedding = query_embedding.astype(np.float32)
        
        # Search FAISS index
        distances, indices = faiss_index.search(query_embedding, min(k, len(guideline_chunks)))
        
        # Retrieve and concatenate chunks
        retrieved_chunks = []
        for idx in indices[0]:
            if idx < len(guideline_chunks):
                retrieved_chunks.append(guideline_chunks[idx])
        
        context = "\n\n".join(retrieved_chunks)
        logger.info(f"Retrieved {len(retrieved_chunks)} relevant guideline chunks")
        
        return context
        
    except Exception as e:
        logger.error(f"Error retrieving context: {e}")
        return "Error retrieving clinical guidelines."
