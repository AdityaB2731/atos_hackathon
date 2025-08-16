from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
import tempfile
import time
import json
from typing import List
import asyncio
from dotenv import load_dotenv

# Import the existing functions from app.py
import sys
sys.path.append('.')

# Load environment variables
load_dotenv()

# Import the existing functions (we'll need to modify them slightly)
from langchain_groq import ChatGroq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import (
    PyPDFLoader,
    UnstructuredWordDocumentLoader,
    TextLoader,
    CSVLoader,
    UnstructuredExcelLoader,
)
from langchain.schema import Document

app = FastAPI(title="LegalBuddy API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state (in production, use a proper database)
documents_text = []
documents_metadata = []
chat_history = []
extraction_result = None
summary_result = None

# Initialize LLM
groq_api_key = os.getenv('GROQ_API_KEY')
llm = ChatGroq(groq_api_key=groq_api_key, model_name="Llama3-8b-8192")

def process_uploaded_file(uploaded_file):
    """Process uploaded file and return documents"""
    file_name = uploaded_file.filename
    file_extension = file_name.split('.')[-1].lower()

    # Create a temporary file to store the uploaded file
    with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{file_extension}') as tmp_file:
        content = uploaded_file.file.read()
        tmp_file.write(content)
        tmp_path = tmp_file.name

    # Process different file types
    try:
        if file_extension == 'pdf':
            loader = PyPDFLoader(tmp_path)
            documents = loader.load()
        elif file_extension == 'txt':
            loader = TextLoader(tmp_path)
            documents = loader.load()
        elif file_extension == 'csv':
            loader = CSVLoader(tmp_path)
            documents = loader.load()
        elif file_extension == 'xlsx':
            loader = UnstructuredExcelLoader(tmp_path)
            documents = loader.load()
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")
    finally:
        # Clean up the temporary file
        os.unlink(tmp_path)

    return documents

def vector_embedding(documents):
    """Process documents and store in global state"""
    global documents_text, documents_metadata
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    final_documents = text_splitter.split_documents(documents)
    
    # Store documents in global state
    documents_text = [doc.page_content for doc in final_documents]
    documents_metadata = [doc.metadata for doc in final_documents]

def estimate_tokens(text):
    """Rough estimate of token count (1 token ≈ 4 characters)"""
    return len(text) // 4

def simple_text_search(query, documents_text, top_k=5):
    """Simple text-based search using keyword matching"""
    query_lower = query.lower()
    results = []
    
    # If no query or empty documents, return all documents
    if not query or not documents_text:
        return documents_text[:top_k]
    
    for i, doc_text in enumerate(documents_text):
        doc_lower = doc_text.lower()
        # Simple keyword matching
        score = sum(1 for word in query_lower.split() if word in doc_lower)
        if score > 0:
            results.append((score, doc_text, i))
    
    # Sort by score and return top_k results
    results.sort(key=lambda x: x[0], reverse=True)
    
    # If no matches found, return first few documents
    if not results:
        return documents_text[:top_k]
    
    return [doc_text for score, doc_text, idx in results[:top_k]]

def convert_to_json(extraction_text):
    """Convert the extracted text into a structured JSON format"""
    sections = {
        "entities_and_contacts": {},
        "contract_timeline": {},
        "scope": "",
        "sla_clauses": [],
        "penalty_clauses": [],
        "confidentiality": {},
        "renewal_termination": {},
        "commercial_terms": {},
        "risks_assumptions": []
    }
    
    # Parse the extraction text and populate sections
    current_section = None
    for line in extraction_text.split('\n'):
        line = line.strip()
        if not line:
            continue
            
        if any(key.replace('_', ' ').upper() in line.upper() for key in sections.keys()):
            current_section = next(key for key in sections.keys() if key.replace('_', ' ').upper() in line.upper())
            continue
            
        if current_section and line:
            if isinstance(sections[current_section], dict):
                # Split on first colon for key-value pairs
                if ':' in line:
                    key, value = line.split(':', 1)
                    sections[current_section][key.strip()] = value.strip()
            elif isinstance(sections[current_section], list):
                sections[current_section].append(line)
            else:
                sections[current_section] = line
    
    return sections

@app.post("/api/process_documents")
async def process_documents(files: List[UploadFile] = File(...)):
    """Process uploaded documents"""
    global documents_text, documents_metadata
    
    try:
        all_documents = []
        for uploaded_file in files:
            documents = process_uploaded_file(uploaded_file)
            all_documents.extend(documents)
        
        if all_documents:
            vector_embedding(all_documents)
            return JSONResponse({
                "success": True,
                "message": f"Processed {len(files)} documents successfully",
                "chunks": len(documents_text)
            })
        else:
            raise HTTPException(status_code=400, detail="No valid documents found")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/extract")
async def extract_details():
    """Extract key details from processed documents"""
    global documents_text, extraction_result
    
    if not documents_text:
        raise HTTPException(status_code=400, detail="No documents processed. Please upload documents first.")
    
    try:
        # Limit the number of documents to avoid token limit issues
        max_chunks = min(2, len(documents_text))
        selected_docs = documents_text[:max_chunks]
        
        # If still too large, reduce further
        total_text = " ".join(selected_docs)
        estimated_tokens = estimate_tokens(total_text)
        
        if estimated_tokens > 4000:
            max_chunks = 1
            selected_docs = documents_text[:max_chunks]
        
        # Create documents for the chain
        documents = [Document(page_content=doc) for doc in selected_docs]
        
        # Create extraction prompt
        extraction_prompt = ChatPromptTemplate.from_template("""
        You are an expert legal document analyst. Analyze the following document sections and extract key legal information.

        Document Content:
        {context}

        Please extract and categorize the following information:

        1. **Entities & Contact Details**: Parties involved, names, addresses, contact information
        2. **Contract Timeline**: Start date, end date, key dates
        3. **Scope of Agreement**: Purpose, obligations, deliverables
        4. **Service Level Agreement (SLA)**: Performance metrics, response times
        5. **Penalty Clauses**: Conditions, consequences for non-compliance
        6. **Confidentiality**: Obligations, duration, scope
        7. **Renewal & Termination**: Conditions, notice periods
        8. **Commercial Terms**: Payment terms, pricing, invoicing
        9. **Risks & Assumptions**: Potential risks, mitigation strategies

        If any information is not found, state "N/A" for that section.
        Provide a structured analysis of the document sections provided.
        """)
        
        document_chain = create_stuff_documents_chain(llm, extraction_prompt)
        
        start = time.process_time()
        response = document_chain.invoke({'context': documents, 'input': 'Extract all key legal information from the document'})
        elapsed = time.process_time() - start

        # Handle response
        if isinstance(response, dict):
            answer = response.get('answer', str(response))
        else:
            answer = str(response)

        # Convert to JSON
        json_data = convert_to_json(answer)

        # Store the result
        extraction_result = {
            "answer": answer,
            "json_data": json_data,
            "elapsed": elapsed,
            "context": [doc.page_content for doc in documents]
        }

        return extraction_result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat")
async def chat_with_documents(message: dict):
    """Chat with documents"""
    global documents_text, chat_history
    
    if not documents_text:
        raise HTTPException(status_code=400, detail="No documents processed. Please upload documents first.")
    
    try:
        user_message = message.get("message", "")
        if not user_message:
            raise HTTPException(status_code=400, detail="Message is required")
        
        # Add to chat history
        chat_history.append({"type": "user", "content": user_message})
        
        # Use simple text search to get relevant documents
        relevant_docs = simple_text_search(user_message, documents_text)
        
        # Create documents for the chain
        documents = [Document(page_content=doc) for doc in relevant_docs]
        
        # Create QA prompt
        qa_prompt = ChatPromptTemplate.from_template("""
        You are a legal document assistant. Provide precise and contextual answers.

        📜 *Document Context*:
        <context>
        {context}
        </context>

        🔍 *User Question*: {input}

        Provide a clear, concise answer based strictly on the document context.
        """)
        
        document_chain = create_stuff_documents_chain(llm, qa_prompt)
        
        start = time.process_time()
        response = document_chain.invoke({'context': documents, 'input': user_message})
        elapsed = time.process_time() - start
        
        # Handle response
        if isinstance(response, dict):
            answer = response.get('answer', str(response))
        else:
            answer = str(response)
        
        # Add AI response to chat history
        chat_history.append({"type": "ai", "content": answer})
        
        return {
            "answer": answer,
            "elapsed": elapsed,
            "context": [doc.page_content for doc in documents]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/summary")
async def generate_summary():
    """Generate document summary"""
    global documents_text, summary_result
    
    if not documents_text:
        raise HTTPException(status_code=400, detail="No documents processed. Please upload documents first.")
    
    try:
        # Use simple text search to get relevant documents
        relevant_docs = simple_text_search("summary overview main points", documents_text)
        
        # Create documents for the chain
        documents = [Document(page_content=doc) for doc in relevant_docs]
        
        # Create summary prompt
        summary_prompt = ChatPromptTemplate.from_template("""
        You are an expert document summarizer. Provide a comprehensive yet concise summary of the document.

        Key Summary Requirements:
        - Capture the main purpose and context of the document
        - Highlight key points and critical information
        - Maintain objectivity and clarity
        - Be precise and avoid unnecessary details

        📜 Document Context:
        <context>
        {context}
        </context>

        Generate a clear, structured summary that captures the essence of the document.
        """)
        
        document_chain = create_stuff_documents_chain(llm, summary_prompt)
        
        start = time.process_time()
        response = document_chain.invoke({'context': documents, 'input': 'Generate a comprehensive summary of the entire document'})
        elapsed = time.process_time() - start

        # Handle response
        if isinstance(response, dict):
            summary = response.get('answer', str(response))
        else:
            summary = str(response)

        summary_result = {
            "summary": summary,
            "elapsed": elapsed
        }

        return summary_result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/chat_history")
async def get_chat_history():
    """Get chat history"""
    global chat_history
    return {"history": chat_history}

@app.delete("/api/chat_history")
async def clear_chat_history():
    """Clear chat history"""
    global chat_history
    chat_history = []
    return {"message": "Chat history cleared"}

@app.get("/api/status")
async def get_status():
    """Get application status"""
    global documents_text, chat_history
    return {
        "documents_processed": len(documents_text),
        "chat_messages": len(chat_history),
        "has_extraction": extraction_result is not None,
        "has_summary": summary_result is not None
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
