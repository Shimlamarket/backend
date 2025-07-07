#!/usr/bin/env python3
"""
Startup script for Market Merchant API Backend
Automatically sets up the environment and starts the server
"""

import os
import sys
import subprocess
import platform

def check_python_version():
    """Check if Python version is 3.8 or higher"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version}")

def check_and_create_venv():
    """Check if virtual environment exists, create if not"""
    venv_path = "venv"
    
    if not os.path.exists(venv_path):
        print("📦 Creating virtual environment...")
        try:
            subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)
            print("✅ Virtual environment created")
        except subprocess.CalledProcessError:
            print("❌ Failed to create virtual environment")
            sys.exit(1)
    else:
        print("✅ Virtual environment exists")
    
    return venv_path

def get_pip_path(venv_path):
    """Get pip executable path based on platform"""
    if platform.system() == "Windows":
        return os.path.join(venv_path, "Scripts", "pip.exe")
    else:
        return os.path.join(venv_path, "bin", "pip")

def get_python_path(venv_path):
    """Get python executable path based on platform"""
    if platform.system() == "Windows":
        return os.path.join(venv_path, "Scripts", "python.exe")
    else:
        return os.path.join(venv_path, "bin", "python")

def install_dependencies(venv_path):
    """Install required dependencies"""
    pip_path = get_pip_path(venv_path)
    
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt not found")
        print("Make sure you have the requirements.txt file in the current directory")
        sys.exit(1)
    
    print("📥 Installing dependencies...")
    try:
        subprocess.run([pip_path, "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        sys.exit(1)

def check_main_file():
    """Check if main.py exists"""
    if not os.path.exists("main.py"):
        print("❌ main.py not found")
        print("Make sure you have the main.py file in the current directory")
        sys.exit(1)
    print("✅ main.py found")

def start_server(venv_path):
    """Start the FastAPI server"""
    python_path = get_python_path(venv_path)
    
    print("\n🚀 Starting Market Merchant API Backend...")
    print("📍 Server will be available at:")
    print("   - API Base: http://localhost:8001")
    print("   - Swagger Docs: http://localhost:8001/docs")
    print("   - ReDoc: http://localhost:8001/redoc")
    print("\n💡 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        # Start uvicorn server
        subprocess.run([
            python_path, "-m", "uvicorn", "main:app",
            "--host", "0.0.0.0",
            "--port", "8001",
            "--reload"
        ], check=True)
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped gracefully")
    except subprocess.CalledProcessError:
        print("❌ Failed to start server")
        sys.exit(1)

def main():
    """Main startup function"""
    print("🏪 Market Merchant API Backend Setup")
    print("=" * 40)
    
    # Check requirements
    check_python_version()
    check_main_file()
    
    # Setup environment
    venv_path = check_and_create_venv()
    install_dependencies(venv_path)
    
    # Start server
    start_server(venv_path)

if __name__ == "__main__":
    main()
