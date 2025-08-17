# Glean

A powerful legal document analysis and extraction tool that helps you understand and extract key information from legal documents using AI.

## 🚀 Features

- **Document Upload**: Support for PDF, TXT, CSV, XLSX, and DOCX files
- **AI-Powered Extraction**: Automatically extract key legal information including:
  - Entities & Contact Details
  - Contract Timeline (Start/End dates)
  - Scope of Agreement
  - Service Level Agreements (SLA)
  - Penalty Clauses
  - Confidentiality Terms
  - Renewal & Termination Clauses
  - Commercial Terms
  - Risks & Assumptions
- **Interactive Chat**: Ask specific questions about your documents
- **Document Summarization**: Generate comprehensive summaries
- **Export Options**: Download results in JSON or text format
- **Chat History**: Maintain conversation history for reference

## 🛠️ Setup

### Prerequisites
- Python 3.8 or higher
- Required API keys:
  - GROQ_API_KEY (for LLM processing)
  - GOOGLE_API_KEY (for embeddings)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd atos_hackathon
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**
   Create a `.env` file in the root directory with your API keys:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   GOOGLE_API_KEY=your_google_api_key_here
   ```

6. **Run the application**
   ```bash
   streamlit run app.py
   ```

## 📖 Usage

1. **Upload Documents**: Use the file uploader to upload your legal documents
2. **Process Documents**: Click "Process Documents" to analyze your files
3. **Choose Action**: Use the sidebar to select your desired action:
   - **Extract Key Details**: Automatic extraction of critical legal information
   - **Chat with Docs**: Ask specific questions about your documents
   - **Chat History**: Review previous conversations
   - **Generate Summary**: Get a comprehensive document overview

## 🔧 Application

- **app.py**: Main application with document processing and AI-powered analysis

## 📁 Project Structure

```
atos_hackathon/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── us_census/         # Sample documents
└── venv/              # Virtual environment
```

## 🤝 Contributing

This project was developed for the Atos Srijan Hackathon. Feel free to contribute improvements and new features.

## 📄 License

This project is part of the Atos Srijan Hackathon submission.

---

**Made with ❤ by Glean Team**
