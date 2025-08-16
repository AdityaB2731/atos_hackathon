#!/usr/bin/env python3
"""
Start script for LegalBuddy application
"""

import subprocess
import sys
import os
import time
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import fastapi
        import uvicorn
        import langchain_groq
        print("✅ Backend dependencies found")
    except ImportError as e:
        print(f"❌ Missing backend dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False
    return True

def check_env_file():
    """Check if .env file exists"""
    if not Path('.env').exists():
        print("❌ .env file not found")
        print("Please create a .env file with your API keys:")
        print("GROQ_API_KEY=your_groq_api_key_here")
        print("GOOGLE_API_KEY=your_google_api_key_here")
        return False
    print("✅ .env file found")
    return True

def start_backend():
    """Start the FastAPI backend server"""
    print("\n🚀 Starting LegalBuddy Backend...")
    print("Backend will be available at: http://localhost:8000")
    print("API Documentation: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop the backend server")
    print("-" * 50)
    
    try:
        subprocess.run([sys.executable, "backend.py"], check=True)
    except KeyboardInterrupt:
        print("\n\n🛑 Backend server stopped")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Failed to start backend: {e}")
        return False
    return True

def main():
    print("📚 LegalBuddy - AI Legal Document Analysis")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Check environment file
    if not check_env_file():
        return
    
    print("\n📋 Setup Instructions:")
    print("1. Backend will start on port 8000")
    print("2. In a new terminal, run: npm install")
    print("3. Then run: npm run dev")
    print("4. Frontend will be available at: http://localhost:3000")
    print("\n" + "=" * 50)
    
    # Start backend
    start_backend()

if __name__ == "__main__":
    main()
