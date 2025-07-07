#!/usr/bin/env python3
"""
Startup script for the Three-App Architecture
Runs all backend services concurrently
"""
import asyncio
import subprocess
import sys
import time
import signal
import os
from typing import List, Dict

class ServiceManager:
    def __init__(self):
        self.processes: List[subprocess.Popen] = []
        self.services = {
            "api_gateway": {
                "command": [sys.executable, "api_gateway/main.py"],
                "port": 8000,
                "description": "API Gateway"
            },
            "customer_api": {
                "command": [sys.executable, "customer_api/main.py"],
                "port": 8001,
                "description": "Customer API"
            },
            "merchant_api": {
                "command": [sys.executable, "merchant_api/main.py"],
                "port": 8002,
                "description": "Merchant API"
            },
            "admin_api": {
                "command": [sys.executable, "admin_api/main.py"],
                "port": 8003,
                "description": "Admin API"
            }
        }
    
    def start_service(self, service_name: str) -> subprocess.Popen:
        """Start a single service"""
        service = self.services[service_name]
        print(f"🚀 Starting {service['description']} on port {service['port']}...")
        
        process = subprocess.Popen(
            service["command"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        self.processes.append(process)
        return process
    
    def start_all_services(self):
        """Start all backend services"""
        print("🏪 Starting Three-App Architecture Backend Services...")
        print("=" * 60)
        
        for service_name in self.services.keys():
            try:
                self.start_service(service_name)
                time.sleep(1)  # Small delay between starts
            except Exception as e:
                print(f"❌ Failed to start {service_name}: {e}")
                self.shutdown()
                sys.exit(1)
        
        print("=" * 60)
        print("✅ All services started successfully!")
        print("\n📊 Service URLs:")
        print("   API Gateway:    http://localhost:8000")
        print("   Customer API:   http://localhost:8001")
        print("   Merchant API:   http://localhost:8002")
        print("   Admin API:      http://localhost:8003")
        print("\n📚 API Documentation:")
        print("   API Gateway:    http://localhost:8000/docs")
        print("   Customer API:   http://localhost:8001/docs")
        print("   Merchant API:   http://localhost:8002/docs")
        print("   Admin API:      http://localhost:8003/docs")
        print("\n🛑 Press Ctrl+C to stop all services")
    
    def shutdown(self):
        """Shutdown all services"""
        print("\n🛑 Shutting down all services...")
        
        for process in self.processes:
            try:
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
            except Exception as e:
                print(f"Warning: Could not terminate process: {e}")
        
        print("✅ All services stopped")
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        self.shutdown()
        sys.exit(0)

def main():
    # Set up signal handlers
    manager = ServiceManager()
    signal.signal(signal.SIGINT, manager.signal_handler)
    signal.signal(signal.SIGTERM, manager.signal_handler)
    
    try:
        # Check if required files exist
        required_files = [
            "api_gateway/main.py",
            "customer_api/main.py", 
            "merchant_api/main.py",
            "admin_api/main.py"
        ]
        
        for file_path in required_files:
            if not os.path.exists(file_path):
                print(f"❌ Required file not found: {file_path}")
                print("Please ensure you're running this script from the project root directory")
                sys.exit(1)
        
        # Start all services
        manager.start_all_services()
        
        # Keep the script running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        manager.shutdown()
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        manager.shutdown()
        sys.exit(1)

if __name__ == "__main__":
    main() 