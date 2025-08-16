import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { 
  Upload, 
  FileText, 
  Search, 
  MessageSquare, 
  History, 
  BarChart3,
  X,
  Send,
  Download,
  RefreshCw
} from 'lucide-react';
import axios from 'axios';

function App() {
  const [files, setFiles] = useState([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [currentView, setCurrentView] = useState('upload'); // upload, actions, extraction, qa, history, summary
  const [extractionResult, setExtractionResult] = useState(null);
  const [chatHistory, setChatHistory] = useState([]);
  const [chatInput, setChatInput] = useState('');
  const [summary, setSummary] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState(null);

  const onDrop = useCallback((acceptedFiles) => {
    const newFiles = acceptedFiles.map(file => ({
      file,
      id: Math.random().toString(36).substr(2, 9),
      name: file.name,
      size: (file.size / 1024).toFixed(1) + ' KB'
    }));
    setFiles(prev => [...prev, ...newFiles]);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'text/plain': ['.txt'],
      'text/csv': ['.csv'],
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx']
    }
  });

  const removeFile = (id) => {
    setFiles(prev => prev.filter(f => f.id !== id));
  };

  const processDocuments = async () => {
    if (files.length === 0) {
      setMessage({ type: 'error', text: 'Please upload at least one file' });
      return;
    }

    setIsProcessing(true);
    setMessage({ type: 'info', text: 'Processing documents...' });

    try {
      const formData = new FormData();
      files.forEach(({ file }) => {
        formData.append('files', file);
      });

      console.log('Sending request to /api/process_documents');
      const response = await axios.post('/api/process_documents', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      console.log('Response received:', response.data);

      if (response.data.success) {
        setMessage({ type: 'success', text: 'Documents processed successfully!' });
        setCurrentView('actions');
      } else {
        setMessage({ type: 'error', text: response.data.error || 'Failed to process documents' });
      }
    } catch (error) {
      console.error('Error processing documents:', error);
      console.error('Error details:', error.response?.data || error.message);
      setMessage({ type: 'error', text: `Failed to process documents: ${error.response?.data?.detail || error.message}` });
    } finally {
      setIsProcessing(false);
    }
  };

  const handleExtraction = async () => {
    setIsLoading(true);
    setMessage({ type: 'info', text: 'Extracting key details...' });

    try {
      const response = await axios.post('/api/extract');
      setExtractionResult(response.data);
      setMessage({ type: 'success', text: 'Extraction completed successfully!' });
      setCurrentView('extraction');
    } catch (error) {
      console.error('Error during extraction:', error);
      setMessage({ type: 'error', text: 'Failed to extract details. Please try again.' });
    } finally {
      setIsLoading(false);
    }
  };

  const handleQA = () => {
    setCurrentView('qa');
  };

  const handleHistory = () => {
    setCurrentView('history');
  };

  const handleSummary = async () => {
    setIsLoading(true);
    setMessage({ type: 'info', text: 'Generating summary...' });

    try {
      const response = await axios.post('/api/summary');
      setSummary(response.data.summary);
      setMessage({ type: 'success', text: 'Summary generated successfully!' });
      setCurrentView('summary');
    } catch (error) {
      console.error('Error generating summary:', error);
      setMessage({ type: 'error', text: 'Failed to generate summary. Please try again.' });
    } finally {
      setIsLoading(false);
    }
  };

  const sendMessage = async () => {
    if (!chatInput.trim()) return;

    const userMessage = chatInput;
    setChatInput('');
    setChatHistory(prev => [...prev, { type: 'user', content: userMessage }]);

    try {
      const response = await axios.post('/api/chat', { message: userMessage });
      setChatHistory(prev => [...prev, { type: 'ai', content: response.data.answer }]);
    } catch (error) {
      console.error('Error sending message:', error);
      setChatHistory(prev => [...prev, { type: 'ai', content: 'Sorry, I encountered an error. Please try again.' }]);
    }
  };

  const downloadResult = (content, filename, type = 'text/plain') => {
    const blob = new Blob([content], { type });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const clearChatHistory = () => {
    setChatHistory([]);
  };

  const renderUploadView = () => (
    <div className="card">
      <h2>📁 Upload Legal Documents</h2>
      <div
        {...getRootProps()}
        className={`upload-area ${isDragActive ? 'dragover' : ''}`}
      >
        <input {...getInputProps()} />
        <div className="upload-icon">
          <Upload size={48} />
        </div>
        <div className="upload-text">
          {isDragActive ? 'Drop the files here...' : 'Drag & drop files here, or click to select'}
        </div>
        <div className="upload-hint">
          Supported formats: PDF, TXT, CSV, XLSX
        </div>
      </div>

      {files.length > 0 && (
        <div className="file-list">
          {files.map(({ id, name, size }) => (
            <div key={id} className="file-item">
              <div className="file-info">
                <FileText size={20} />
                <span className="file-name">{name}</span>
                <span className="file-size">({size})</span>
              </div>
              <button
                className="btn btn-danger"
                onClick={() => removeFile(id)}
              >
                <X size={16} />
              </button>
            </div>
          ))}
        </div>
      )}

      {files.length > 0 && (
        <button
          className="btn"
          onClick={processDocuments}
          disabled={isProcessing}
        >
          {isProcessing ? (
            <>
              <div className="spinner"></div>
              Processing...
            </>
          ) : (
            <>
              <FileText size={20} />
              Process Documents
            </>
          )}
        </button>
      )}
    </div>
  );

  const renderActionsView = () => (
    <div className="card">
      <h2>🎯 Choose an Action</h2>
      <div className="actions-grid">
        <div className="action-card" onClick={handleExtraction}>
          <div className="action-icon">🔍</div>
          <div className="action-title">Extract Key Details</div>
          <div className="action-description">
            Automatic extraction of critical legal information from your documents
          </div>
        </div>

        <div className="action-card" onClick={handleQA}>
          <div className="action-icon">💬</div>
          <div className="action-title">Chat with Documents</div>
          <div className="action-description">
            Ask specific questions about your legal documents
          </div>
        </div>

        <div className="action-card" onClick={handleHistory}>
          <div className="action-icon">📜</div>
          <div className="action-title">Chat History</div>
          <div className="action-description">
            Review your previous conversations and questions
          </div>
        </div>

        <div className="action-card" onClick={handleSummary}>
          <div className="action-icon">📄</div>
          <div className="action-title">Generate Summary</div>
          <div className="action-description">
            Get a comprehensive overview of your document contents
          </div>
        </div>
      </div>

      <button
        className="btn btn-secondary"
        onClick={() => setCurrentView('upload')}
        style={{ marginTop: '2rem' }}
      >
        <RefreshCw size={20} />
        Upload New Documents
      </button>
    </div>
  );

  const renderExtractionView = () => (
    <div className="card">
      <h2>📑 Legal Document Insights</h2>
      {extractionResult && (
        <div className="result-section">
          <div className="result-title">
            <BarChart3 size={24} />
            Analysis Results
          </div>
          <div className="result-content">{extractionResult.answer}</div>
          
          <div style={{ marginTop: '1rem', display: 'flex', gap: '1rem' }}>
            <button
              className="btn btn-secondary"
              onClick={() => downloadResult(extractionResult.answer, 'legal_extraction.txt')}
            >
              <Download size={16} />
              Download Text
            </button>
            <button
              className="btn btn-secondary"
              onClick={() => downloadResult(JSON.stringify(extractionResult.json_data, null, 2), 'legal_extraction.json', 'application/json')}
            >
              <Download size={16} />
              Download JSON
            </button>
          </div>
        </div>
      )}

      <button
        className="btn btn-secondary"
        onClick={() => setCurrentView('actions')}
        style={{ marginTop: '2rem' }}
      >
        ← Back to Actions
      </button>
    </div>
  );

  const renderQAView = () => (
    <div className="card">
      <h2>💬 Chat with Your Documents</h2>
      <div className="chat-container">
        <div className="chat-messages">
          {chatHistory.length === 0 ? (
            <div style={{ textAlign: 'center', color: 'rgba(255, 255, 255, 0.6)', marginTop: '2rem' }}>
              Start asking questions about your documents...
            </div>
          ) : (
            chatHistory.map((msg, index) => (
              <div key={index} className={`message ${msg.type}`}>
                {msg.content}
              </div>
            ))
          )}
        </div>
        
        <div className="chat-input">
          <input
            type="text"
            value={chatInput}
            onChange={(e) => setChatInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
            placeholder="Ask a question about your documents..."
          />
          <button className="btn" onClick={sendMessage}>
            <Send size={16} />
          </button>
        </div>
      </div>

      <div style={{ marginTop: '1rem', display: 'flex', gap: '1rem' }}>
        <button className="btn btn-secondary" onClick={clearChatHistory}>
          Clear History
        </button>
        <button className="btn btn-secondary" onClick={() => setCurrentView('actions')}>
          ← Back to Actions
        </button>
      </div>
    </div>
  );

  const renderHistoryView = () => (
    <div className="card">
      <h2>📜 Chat History</h2>
      {chatHistory.length === 0 ? (
        <div style={{ textAlign: 'center', color: 'rgba(255, 255, 255, 0.6)', marginTop: '2rem' }}>
          No chat history available
        </div>
      ) : (
        <div className="chat-messages">
          {chatHistory.map((msg, index) => (
            <div key={index} className={`message ${msg.type}`}>
              {msg.content}
            </div>
          ))}
        </div>
      )}

      <div style={{ marginTop: '1rem', display: 'flex', gap: '1rem' }}>
        <button className="btn btn-secondary" onClick={clearChatHistory}>
          Clear History
        </button>
        <button className="btn btn-secondary" onClick={() => setCurrentView('actions')}>
          ← Back to Actions
        </button>
      </div>
    </div>
  );

  const renderSummaryView = () => (
    <div className="card">
      <h2>📄 Document Summary</h2>
      {summary && (
        <div className="result-section">
          <div className="result-title">
            <FileText size={24} />
            Summary
          </div>
          <div className="result-content">{summary}</div>
          
          <button
            className="btn btn-secondary"
            onClick={() => downloadResult(summary, 'document_summary.txt')}
            style={{ marginTop: '1rem' }}
          >
            <Download size={16} />
            Download Summary
          </button>
        </div>
      )}

      <button
        className="btn btn-secondary"
        onClick={() => setCurrentView('actions')}
        style={{ marginTop: '2rem' }}
      >
        ← Back to Actions
      </button>
    </div>
  );

  const renderCurrentView = () => {
    switch (currentView) {
      case 'upload':
        return renderUploadView();
      case 'actions':
        return renderActionsView();
      case 'extraction':
        return renderExtractionView();
      case 'qa':
        return renderQAView();
      case 'history':
        return renderHistoryView();
      case 'summary':
        return renderSummaryView();
      default:
        return renderUploadView();
    }
  };

  return (
    <div>
      <nav className="navbar">
        <div className="navbar-content">
          <div className="navbar-brand">
            📚 LegalBuddy
          </div>
        </div>
      </nav>

      <main className="main-content">
        <div className="container">
          {message && (
            <div className={`${message.type}-message`}>
              {message.text}
            </div>
          )}

          {isLoading && (
            <div className="loading">
              <div className="spinner"></div>
              Processing...
            </div>
          )}

          {renderCurrentView()}
        </div>
      </main>
    </div>
  );
}

export default App;
