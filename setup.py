#!/usr/bin/env python3
"""
Quick setup script for Dream Journal
Automates the installation and initial setup process
"""

import subprocess
import sys
import os

def print_step(step, message):
    """Print formatted step message"""
    print(f"\n{'='*60}")
    print(f"STEP {step}: {message}")
    print('='*60)

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"\n→ {description}...")
    try:
        if isinstance(command, list):
            result = subprocess.run(command, check=True, capture_output=True, text=True)
        else:
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error during {description}")
        print(f"  Error: {e.stderr}")
        return False

def main():
    """Main setup function"""
    print("""
    ╔════════════════════════════════════════════╗
    ║   Dream Journal Emotion Tracker Setup     ║
    ║            Quick Setup Script              ║
    ╚════════════════════════════════════════════╝
    """)
    
    # Step 1: Check Python version
    print_step(1, "Checking Python version")
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("✗ Python 3.8 or higher is required!")
        print(f"  Current version: {sys.version}")
        sys.exit(1)
    print(f"✓ Python {python_version.major}.{python_version.minor}.{python_version.micro} detected")
    
    # Step 2: Create virtual environment
    print_step(2, "Creating virtual environment")
    if not os.path.exists('venv'):
        if run_command([sys.executable, '-m', 'venv', 'venv'], "Creating venv"):
            print("  Virtual environment created at ./venv")
    else:
        print("✓ Virtual environment already exists")
    
    # Step 3: Determine pip path
    print_step(3, "Setting up package installation")
    if sys.platform == "win32":
        pip_path = os.path.join('venv', 'Scripts', 'pip.exe')
        python_path = os.path.join('venv', 'Scripts', 'python.exe')
    else:
        pip_path = os.path.join('venv', 'bin', 'pip')
        python_path = os.path.join('venv', 'bin', 'python')
    
    # Step 4: Upgrade pip
    print_step(4, "Upgrading pip")
    run_command([python_path, '-m', 'pip', 'install', '--upgrade', 'pip'], "Upgrading pip")
    
    # Step 5: Install dependencies
    print_step(5, "Installing Python dependencies")
    if run_command([pip_path, 'install', '-r', 'requirements.txt'], "Installing requirements"):
        print("✓ All dependencies installed")
    else:
        print("✗ Failed to install dependencies")
        sys.exit(1)
    
    # Step 6: Download spaCy model
    print_step(6, "Downloading spaCy language model")
    if run_command([python_path, '-m', 'spacy', 'download', 'en_core_web_sm'], "Downloading en_core_web_sm"):
        print("✓ spaCy model downloaded")
    else:
        print("⚠ Warning: spaCy model download failed. You may need to run manually:")
        print(f"  {python_path} -m spacy download en_core_web_sm")
    
    # Step 7: Initialize database
    print_step(7, "Initializing database")
    init_code = "from app import app, db; app.app_context().push(); db.create_all(); print('Database initialized')"
    if run_command([python_path, '-c', init_code], "Creating database tables"):
        print("✓ Database initialized at ./dream_journal.db")
    else:
        print("⚠ Warning: Database initialization failed")
    
    # Final message
    print(f"\n{'='*60}")
    print("✓ SETUP COMPLETE!")
    print('='*60)
    print("\nTo start the Dream Journal application:")
    print("  1. Activate the virtual environment:")
    if sys.platform == "win32":
        print("     .\\venv\\Scripts\\Activate")
    else:
        print("     source venv/bin/activate")
    print("  2. Run the application:")
    print("     python app.py")
    print("  3. Open your browser to:")
    print("     http://localhost:5000")
    print("\nHappy dreaming! 🌙✨\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✗ Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n✗ Unexpected error: {e}")
        sys.exit(1)
