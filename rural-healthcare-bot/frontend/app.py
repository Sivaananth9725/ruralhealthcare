"""
Streamlit frontend for Rural Healthcare Decision Support Bot.
Provides user-friendly interface for symptom analysis and healthcare guidance.
"""

import streamlit as st
import requests
import json
from typing import Optional

# Streamlit page configuration
st.set_page_config(
    page_title="Rural Healthcare Bot",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        max-width: 900px;
        margin: 0 auto;
    }
    .stTitle {
        color: #2E7D32;
    }
    .urgency-high {
        background-color: #ffebee;
        padding: 15px;
        border-left: 4px solid #d32f2f;
        border-radius: 4px;
    }
    .urgency-medium {
        background-color: #fff3e0;
        padding: 15px;
        border-left: 4px solid #f57c00;
        border-radius: 4px;
    }
    .urgency-low {
        background-color: #e8f5e9;
        padding: 15px;
        border-left: 4px solid #388e3c;
        border-radius: 4px;
    }
    </style>
""", unsafe_allow_html=True)

# Backend API URL
API_URL = "http://localhost:8000/api"

# Page title and description
st.title("🏥 Rural Healthcare Decision Support Bot")
st.markdown("""
    **AI-powered healthcare guidance for rural communities**
    
    *Note: This tool provides preliminary health guidance only. 
    Please consult a qualified healthcare provider for diagnosis and treatment.*
""")

# Sidebar information
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
        This application provides:
        - Symptom analysis based on clinical guidelines
        - Preliminary health guidance
        - Referral urgency recommendations
        - Integration with Groq LLM for accurate responses
        
        **Disclaimer**: This is NOT a medical diagnosis tool.
        Always consult healthcare professionals.
    """)
    
    st.header("📞 Guidelines")
    st.markdown("""
        - Describe your symptoms clearly
        - Include duration and severity
        - Mention any relevant medical history
        - Follow referral recommendations
    """)


def call_backend(symptoms: str) -> Optional[dict]:
    """
    Call backend /diagnose endpoint.
    
    Args:
        symptoms (str): Patient symptoms description
    
    Returns:
        dict: Response with answer and referral_urgency or None if error
    """
    try:
        response = requests.post(
            f"{API_URL}/diagnose",
            json={"symptoms": symptoms},
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error from server: {response.status_code}")
            return None
            
    except requests.exceptions.ConnectionError:
        st.error(
            "❌ Cannot connect to backend server. "
            "Please ensure the FastAPI server is running on http://localhost:8000"
        )
        return None
    except requests.exceptions.Timeout:
        st.error("⏱️ Request timed out. Please try again.")
        return None
    except Exception as e:
        st.error(f"Error communicating with server: {str(e)}")
        return None


def display_response(response: dict):
    """
    Display formatted response with urgency highlighting.
    
    Args:
        response (dict): Response from backend containing answer and referral_urgency
    """
    # Display the healthcare guidance
    st.subheader("💊 Healthcare Guidance")
    st.markdown(response.get("answer", "No response received"))
    
    # Display referral urgency with color coding
    urgency = response.get("referral_urgency")
    
    if urgency:
        st.subheader("🚨 Referral Urgency")
        
        if urgency == "HIGH":
            st.markdown(
                f'<div class="urgency-high"><b>🔴 URGENT</b> - Seek immediate medical attention</div>',
                unsafe_allow_html=True
            )
        elif urgency == "MEDIUM":
            st.markdown(
                f'<div class="urgency-medium"><b>🟡 MODERATE</b> - Schedule appointment within a few days</div>',
                unsafe_allow_html=True
            )
        elif urgency == "LOW":
            st.markdown(
                f'<div class="urgency-low"><b>🟢 LOW</b> - Routine checkup recommended</div>',
                unsafe_allow_html=True
            )
        else:
            st.info(f"Urgency: {urgency}")


# Main input section
st.header("📝 Describe Your Symptoms")

# Create tabs for different sections
tab1, tab2 = st.tabs(["Symptom Analysis", "About the Bot"])

with tab1:
    # Symptom input
    symptoms = st.text_area(
        label="Please describe your symptoms in detail:",
        placeholder="E.g., 'I have a fever for 3 days, headache, body aches, and cough. No appetite. Temperature is 101°F.'",
        height=150,
        help="Provide as much detail as possible for better guidance"
    )
    
    # Additional information
    col1, col2 = st.columns(2)
    
    with col1:
        age_group = st.selectbox(
            "Age group (optional):",
            ["Not specified", "0-5 years", "6-18 years", "19-40 years", "41-60 years", "60+ years"]
        )
    
    with col2:
        chronic_condition = st.multiselect(
            "Existing conditions (optional):",
            ["None", "Diabetes", "Hypertension", "Asthma", "Heart Disease", "Other"]
        )
    
    # Combine information if provided
    if age_group != "Not specified" or chronic_condition:
        supplementary_info = f"\nAdditional info: Age group: {age_group}"
        if chronic_condition and chronic_condition != ["None"]:
            supplementary_info += f", Existing conditions: {', '.join(chronic_condition)}"
        symptoms = symptoms + supplementary_info
    
    # Analyze button
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        analyze_button = st.button("🔍 Analyze Symptoms", use_container_width=True)
    
    with col2:
        clear_button = st.button("🗑️ Clear", use_container_width=True)
    
    if clear_button:
        st.rerun()
    
    # Process analysis
    if analyze_button:
        if not symptoms.strip():
            st.warning("⚠️ Please describe your symptoms before analyzing.")
        else:
            with st.spinner("🔄 Analyzing symptoms and retrieving guidelines..."):
                response = call_backend(symptoms)
                
                if response:
                    display_response(response)
                    
                    # Add feedback option
                    st.divider()
                    st.markdown("### 📋 Feedback")
                    feedback = st.text_area(
                        "Was this helpful? Share your feedback:",
                        height=80,
                        key="feedback_area"
                    )

with tab2:
    st.markdown("""
        ### How It Works
        
        This application uses:
        1. **RAG (Retrieval-Augmented Generation)**: Retrieves relevant medical guidelines
        2. **Sentence Transformers**: Converts text to embeddings for semantic search
        3. **FAISS**: Fast vector similarity search
        4. **Groq LLM**: Advanced language model for healthcare guidance
        5. **FastAPI**: Backend service
        6. **Streamlit**: User-friendly frontend
        
        ### Important Disclaimer
        
        ⚠️ **This tool provides educational guidance only and is NOT a substitute for professional medical advice.**
        
        - Always consult with qualified healthcare professionals
        - In case of emergency, seek immediate medical attention
        - This system uses AI and may make errors
        - Medical decisions should be made by healthcare providers
        
        ### Privacy
        
        Your symptoms are processed by the local backend and stored for analysis purposes.
        Please be cautious with sensitive personal information.
    """)

# Footer
st.divider()
st.caption("🏥 Rural Healthcare Decision Support Bot v1.0.0 | Powered by AI and Open Source Technologies")
