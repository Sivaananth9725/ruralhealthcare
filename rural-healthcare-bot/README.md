# 🏥 Rural Healthcare Decision Support Bot

An AI-powered healthcare decision support system designed for rural communities using **FastAPI**, **Streamlit**, **Retrieval-Augmented Generation (RAG)**, and **Groq LLM**.

## 📋 Overview

This application provides preliminary health guidance based on patient symptoms and clinical guidelines. It uses advanced AI techniques to retrieve relevant medical information and generate appropriate healthcare recommendations with referral urgency levels.

**⚠️ Important Disclaimer**: This tool provides educational guidance only and is **NOT** a substitute for professional medical advice. Always consult qualified healthcare providers.

## 🎯 Key Features

- **RAG-powered**: Retrieves relevant clinical guidelines using semantic search
- **LLM Integration**: Uses Groq's llama-3.3-70b-versatile model for healthcare guidance
- **Referral Urgency**: Recommends urgency levels (LOW, MEDIUM, HIGH) for medical attention
- **Database Storage**: Stores queries and responses for analysis
- **User-Friendly Interface**: Simple Streamlit UI for non-technical users
- **Offline Capable**: Works with local guidelines
- **CORS Enabled**: Ready for multi-origin access

## 🏗️ Project Architecture

```
rural-healthcare-bot/
│
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── db.py                   # SQLAlchemy database setup
│   ├── models.py               # Database models
│   ├── schemas.py              # Pydantic request/response schemas
│   ├── rag.py                  # RAG module with FAISS indexing
│   │
│   ├── services/
│   │   └── llm_service.py      # Groq LLM integration
│   │
│   ├── routes/
│   │   └── diagnosis.py        # /diagnose endpoint router
│   │
│   └── guidelines/             # Medical guideline PDFs
│
├── frontend/
│   └── app.py                  # Streamlit UI application
│
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

## 🔧 Technology Stack

### Backend
- **FastAPI**: High-performance Python web framework
- **SQLAlchemy**: ORM for database operations
- **SQLite**: Lightweight database for storing queries
- **FAISS**: Facebook AI Similarity Search for vector indexing
- **Sentence-Transformers**: All-MiniLM-L6-v2 for text embeddings
- **Groq**: Advanced LLM API for healthcare guidance
- **PyPDF2**: PDF parsing for clinical guidelines

### Frontend
- **Streamlit**: Simple Python web framework for UI
- **Requests**: HTTP client for backend communication

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Setup Steps

1. **Clone or navigate to the project**
   ```bash
   cd rural-healthcare-bot
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables**
   ```bash
   # Create .env file in project root
   # Windows (PowerShell)
   echo "GROQ_API_KEY=your_groq_api_key_here" > .env

   # macOS/Linux
   export GROQ_API_KEY="your_groq_api_key_here"
   ```

   To get your Groq API key:
   - Visit [Groq Console](https://console.groq.com)
   - Create an account and generate an API key

5. **Add medical guidelines** (optional)
   - Place PDF files containing clinical guidelines in `backend/guidelines/` folder
   - If no PDFs are added, the system will work with placeholder guidance

## 🚀 Running the Application

### Start Backend Server

```bash
# Navigate to backend directory
cd backend

# Run FastAPI server
python main.py
# or
uvicorn main:app --reload
```

Server will be available at: `http://localhost:8000`

- API Documentation: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Start Frontend (New Terminal)

```bash
# Navigate to frontend directory
cd frontend

# Run Streamlit app
streamlit run app.py
```

Frontend will be available at: `http://localhost:8501`

## 📡 API Endpoints

### POST /api/diagnose
Analyzes symptoms and returns healthcare guidance.

**Request Body:**
```json
{
  "symptoms": "I have a fever for 3 days, headache, and body aches"
}
```

**Response:**
```json
{
  "answer": "Based on your symptoms...",
  "referral_urgency": "MEDIUM"
}
```

### GET /
Root endpoint with API information.

### GET /health
Health check endpoint.

## 🔍 How It Works

1. **User Input**: Patient describes symptoms in Streamlit UI
2. **RAG Retrieval**: System retrieves relevant medical guidelines using FAISS
3. **LLM Generation**: Groq LLM generates healthcare guidance based on guidelines
4. **Urgency Assessment**: System extracts referral urgency level
5. **Database Storage**: Query and response saved to SQLite database
6. **UI Display**: Results shown with color-coded urgency levels

## 📊 Database Schema

### PatientQuery Table
```sql
CREATE TABLE patient_queries (
    id INTEGER PRIMARY KEY,
    symptoms VARCHAR(500) NOT NULL,
    response TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## 🔐 Security Considerations

- Keep `GROQ_API_KEY` secure and never commit to version control
- Use `.env` files to store sensitive data
- Disable CORS in production or restrict to specific origins
- Validate and sanitize user inputs
- Ensure HTTPS in production

## 🧪 Testing

### Test Backend Health
```bash
curl http://localhost:8000/health
```

### Test Diagnosis Endpoint
```bash
curl -X POST http://localhost:8000/api/diagnose \
  -H "Content-Type: application/json" \
  -d '{"symptoms": "I have a fever"}'
```

## 📝 Adding Medical Guidelines

1. Collect PDF files with clinical guidelines
2. Place in `backend/guidelines/` directory
3. Restart the backend server
4. Guidelines will be automatically loaded and indexed

Example sources:
- WHO Clinical Guidelines
- Ministry of Health documents
- Standard treatment protocols
- Regional health department guides

## 🐛 Troubleshooting

### Backend Connection Error
- Ensure FastAPI server is running on `http://localhost:8000`
- Check firewall settings
- Verify port 8000 is not in use

### Groq API Key Error
- Verify `GROQ_API_KEY` environment variable is set
- Check API key is valid at [Groq Console](https://console.groq.com)
- Ensure you have API quota remaining

### No Guidelines Loaded
- Add PDF files to `backend/guidelines/` folder
- Check file paths and permissions
- Review logs for specific errors

### Database Issues
- Delete `patients.db` to reset database
- Verify write permissions in backend directory
- Check SQLAlchemy configuration

## 📚 Dependencies Explained

| Package | Purpose |
|---------|---------|
| fastapi | Web framework for REST API |
| uvicorn | ASGI server for FastAPI |
| streamlit | Web UI framework |
| sentence-transformers | Text embeddings (all-MiniLM-L6-v2) |
| faiss-cpu | Vector similarity search |
| pypdf | PDF text extraction |
| sqlalchemy | ORM for database |
| groq | LLM API client |
| pydantic | Data validation |
| python-dotenv | Environment variable management |

## 📈 Future Enhancements

- Multi-language support for rural areas
- Offline model support for low-internet regions
- Integration with health registries
- SMS-based interface
- Audio/voice input support
- Advanced analytics and reporting
- Mobile app version
- Real-time telemedicine integration

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the project
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## ⚖️ Legal & Ethics

- **Medical Disclaimer**: This tool is not a medical device. Always consult healthcare professionals.
- **Data Privacy**: Handle patient data securely and in compliance with regulations
- **Accuracy**: While AI-assisted, guidance may contain errors
- **Liability**: Developers are not responsible for medical decisions made based on this tool

## 📞 Support

For issues, questions, or suggestions:
- Check the troubleshooting section
- Review backend logs
- Check API documentation at `/docs` endpoint

## 🙏 Acknowledgments

- **Groq**: For providing the powerful LLM API
- **Streamlit**: For the simple and effective UI framework
- **FAISS**: For efficient vector search
- **Hugging Face**: For sentence-transformers models
- **Open Source Community**: For all the amazing tools

---

**Version**: 1.0.0  
**Last Updated**: February 2026  
**Status**: Active Development

🏥 Making healthcare accessible to rural communities through AI
