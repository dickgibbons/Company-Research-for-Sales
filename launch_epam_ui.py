#!/usr/bin/env python3
"""
EPAM Business Intelligence UI Launcher
Simple launcher script for the web application
"""

import os
import sys
import subprocess
import webbrowser
import time

def check_requirements():
    """Check if required packages are installed"""
    try:
        import flask
        import docx
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("Please install required packages:")
        print("pip3 install flask python-docx --user")
        return False

def launch_application():
    """Launch the EPAM UI application"""
    if not check_requirements():
        return

    print("🚀 Launching EPAM Business Intelligence Web UI...")
    print("=" * 60)

    # Start the Flask application
    app_path = os.path.join(os.path.dirname(__file__), 'epam_ui_app.py')

    if not os.path.exists(app_path):
        print(f"❌ Application file not found: {app_path}")
        return

    print("📱 Starting web server on http://localhost:8080")
    print("🎯 The application will open in your browser automatically")
    print("💡 Press Ctrl+C to stop the server")
    print("=" * 60)

    # Wait a moment then open browser
    def open_browser():
        time.sleep(2)
        webbrowser.open('http://localhost:8080')

    import threading
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()

    # Run the Flask app
    try:
        subprocess.run([sys.executable, app_path])
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error running application: {e}")

if __name__ == "__main__":
    launch_application()