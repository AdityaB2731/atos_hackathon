# LegalBuddy - AI Legal Document Analysis

A modern web application for analyzing legal documents using AI. Built with React frontend and FastAPI backend.

## Features

- 📁 **Document Upload**: Drag & drop support for PDF, TXT, CSV, and XLSX files
- 🔍 **Key Details Extraction**: Automatic extraction of legal information
- 💬 **Chat with Documents**: Ask questions about your legal documents
- 📜 **Chat History**: Review previous conversations
- 📄 **Document Summary**: Generate comprehensive summaries
- 🎨 **Modern UI**: Beautiful, responsive interface with glassmorphism design

## Tech Stack

### Frontend
- **React 18** with Vite
- **React Dropzone** for file uploads
- **Lucide React** for icons
- **Axios** for API communication
- **Modern CSS** with glassmorphism effects

### Backend
- **FastAPI** for API endpoints
- **LangChain** for document processing
- **Groq** for AI/LLM integration
- **Uvicorn** for ASGI server

## Setup Instructions

### Prerequisites
- Node.js (v16 or higher)
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

### 3. Frontend Setup

#### Install Node.js Dependencies
```bash
npm install
```

#### Start the Development Server
```bash
npm run dev
```
The React app will start on `http://localhost:3000`

## Usage

### 1. Upload Documents
- Drag and drop your legal documents (PDF, TXT, CSV, XLSX) into the upload area
- Or click to select files from your computer
- Click "Process Documents" to analyze them

### 2. Choose an Action
After processing, you can:

#### Extract Key Details
- Automatically extracts legal information like:
  - Entities & Contact Details
  - Contract Timeline
  - Scope of Agreement
  - SLA Clauses
  - Penalty Clauses
  - Confidentiality Terms
  - Renewal & Termination
  - Commercial Terms
  - Risks & Assumptions

#### Chat with Documents
- Ask specific questions about your documents
- Get contextual answers based on document content
- View chat history

#### Generate Summary
- Get a comprehensive overview of document contents
- Download summary as text file

### 3. Download Results
- Download extraction results as JSON or text
- Download summaries as text files
- All results are available for offline use

## API Endpoints

### Document Processing
- `POST /api/process_documents` - Upload and process documents
- `GET /api/status` - Get application status

### Analysis
- `POST /api/extract` - Extract key details from documents
- `POST /api/chat` - Chat with documents
- `POST /api/summary` - Generate document summary

### Chat Management
- `GET /api/chat_history` - Get chat history
- `DELETE /api/chat_history` - Clear chat history

## Development

### Frontend Development
```bash
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

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
├── src/                    # React frontend source
│   ├── App.jsx            # Main React component
│   ├── main.jsx           # React entry point
│   └── index.css          # Global styles
├── backend.py             # FastAPI backend
├── app.py                 # Original Streamlit app
├── requirements.txt       # Python dependencies
├── package.json           # Node.js dependencies
├── vite.config.js         # Vite configuration
├── index.html             # HTML template
└── README.md              # This file
```

## Configuration

### Vite Configuration
The frontend is configured to proxy API requests to the backend:
- Development: `http://localhost:3000` → `http://localhost:8000`
- Production: Update `vite.config.js` for your deployment

### CORS Settings
The backend allows requests from:
- `http://localhost:3000` (React dev server)
- Update `backend.py` for production domains

## Deployment

### Frontend (React)
```bash
# Build for production
npm run build

# Deploy the `dist` folder to your hosting service
# (Netlify, Vercel, AWS S3, etc.)
```

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

1. **CORS Errors**
   - Ensure the backend is running on port 8000
   - Check CORS settings in `backend.py`

2. **File Upload Issues**
   - Verify file format is supported (PDF, TXT, CSV, XLSX)
   - Check file size limits

3. **API Key Errors**
   - Ensure `.env` file exists with correct API keys
   - Verify API keys are valid and have sufficient credits

4. **Token Limit Errors**
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
