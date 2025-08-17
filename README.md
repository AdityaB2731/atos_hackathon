# LegalBuddy - AI Legal Document Analysis

A modern web application for analyzing legal documents using AI. Built with FastAPI backend.

## Features

- 📁 **Document Upload**: Support for PDF, TXT, CSV, and XLSX files
- 🔍 **Key Details Extraction**: Automatic extraction of legal information
- 💬 **Chat with Documents**: Ask questions about your legal documents
- 📜 **Chat History**: Review previous conversations
- 📄 **Document Summary**: Generate comprehensive summaries
- 🎨 **Modern API**: RESTful API with comprehensive documentation

## Tech Stack

### Backend
- **FastAPI** for API endpoints
- **LangChain** for document processing
- **Groq** for AI/LLM integration
- **Uvicorn** for ASGI server

## Setup Instructions

### Prerequisites
- Python (v3.8 or higher)
- pip (Python package manager)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd atos_hackathon
```

### 2. Backend Setup

#### Install Python Dependencies
```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Set Up Environment Variables
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
```

#### Start the Backend Server
```bash
python backend.py
```
The FastAPI server will start on `http://localhost:8000`

## Usage

### API Endpoints

#### Document Processing
- `POST /api/process_documents` - Upload and process documents
- `GET /api/status` - Get application status

#### Analysis
- `POST /api/extract` - Extract key details from documents
- `POST /api/chat` - Chat with documents
- `POST /api/summary` - Generate document summary

#### Chat Management
- `GET /api/chat_history` - Get chat history
- `DELETE /api/chat_history` - Clear chat history

### Example Usage

#### Upload and Process Documents
```bash
curl -X POST "http://localhost:8000/api/process_documents" \
  -H "Content-Type: multipart/form-data" \
  -F "files=@your_document.pdf"
```

#### Extract Key Details
```bash
curl -X POST "http://localhost:8000/api/extract" \
  -H "Content-Type: application/json" \
  -d '{"document_id": "your_document_id"}'
```

#### Chat with Documents
```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "What are the key terms in this contract?"}'
```

## Development

### Backend Development
```bash
# Start with auto-reload (requires uvicorn[standard])
uvicorn backend:app --reload --host 0.0.0.0 --port 8000

# Run with specific settings
python backend.py
```

### API Documentation
Once the backend is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Project Structure

```
atos_hackathon/
├── backend.py             # FastAPI backend
├── app.py                 # Original Streamlit app
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## Configuration

### CORS Settings
The backend allows requests from all origins by default. Update `backend.py` for production domains.

## Deployment

### Backend (FastAPI)
```bash
# Production server
uvicorn backend:app --host 0.0.0.0 --port 8000

# With Gunicorn (recommended for production)
pip install gunicorn
gunicorn backend:app -w 4 -k uvicorn.workers.UvicornWorker
```

## Troubleshooting

### Common Issues

1. **File Upload Issues**
   - Verify file format is supported (PDF, TXT, CSV, XLSX)
   - Check file size limits

2. **API Key Errors**
   - Ensure `.env` file exists with correct API keys
   - Verify API keys are valid and have sufficient credits

3. **Token Limit Errors**
   - The app automatically handles token limits
   - Large documents are processed in chunks

### Performance Tips

1. **Large Documents**
   - The app processes documents in 500-character chunks
   - Extraction uses only first 1-2 chunks to avoid token limits

2. **Chat History**
   - Chat history is stored in memory (clears on server restart)
   - For production, implement database storage

3. **File Processing**
   - Multiple files are processed sequentially
   - Consider implementing parallel processing for large datasets

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review API documentation at `http://localhost:8000/docs`
3. Create an issue in the repository

---

**Made with ❤ by LegalBuddy Team**
