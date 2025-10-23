#!/usr/bin/env python
"""
Complete Setup Script for Voice Assistant v2.1
Installs all dependencies and configures the system
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(cmd, description=""):
    """Run a shell command"""
    print(f"\n>>> {description}")
    print(f"    Command: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"    Status: SUCCESS")
            if result.stdout:
                print(f"    Output: {result.stdout[:200]}")
            return True
        else:
            print(f"    Status: FAILED")
            print(f"    Error: {result.stderr[:200]}")
            return False
    except Exception as e:
        print(f"    Status: ERROR - {str(e)}")
        return False

def main():
    print("=" * 70)
    print("VOICE ASSISTANT v2.1 - COMPLETE SETUP")
    print("=" * 70)
    
    venv_python = r'.\venv\Scripts\python'
    venv_pip = r'.\venv\Scripts\pip'
    
    # Step 1: Verify Python
    print("\n[1/6] Verifying Python Installation...")
    if not run_command(f'{venv_python} --version', 'Checking Python version'):
        print("ERROR: Python not found in virtual environment")
        return False
    
    # Step 2: Upgrade pip
    print("\n[2/6] Upgrading pip...")
    run_command(f'{venv_pip} install --upgrade pip', 'Upgrading pip')
    
    # Step 3: Install all dependencies
    print("\n[3/6] Installing all dependencies...")
    if not run_command(f'{venv_pip} install -r requirements.txt', 'Installing from requirements.txt'):
        print("ERROR: Failed to install dependencies")
        return False
    
    # Step 4: Verify all packages
    print("\n[4/6] Verifying all packages...")
    packages = ['flask', 'flask_sqlalchemy', 'flask_login', 'requests', 'bcrypt']
    all_ok = True
    for pkg in packages:
        cmd = f'{venv_python} -c "import {pkg}; print(\'OK\')"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        status = "OK" if result.returncode == 0 else "MISSING"
        print(f"    {pkg}: {status}")
        if result.returncode != 0:
            all_ok = False
    
    if not all_ok:
        print("ERROR: Some packages are missing")
        return False
    
    # Step 5: Fix database
    print("\n[5/6] Fixing database schema...")
    if not run_command(f'{venv_python} fix_database.py', 'Running database fix'):
        print("WARNING: Database fix had issues, but continuing...")
    
    # Step 6: Verify app
    print("\n[6/6] Verifying Flask app...")
    if not run_command(f'{venv_python} -c "from app import create_app; app = create_app(); print(\'OK\')"', 'Testing app creation'):
        print("ERROR: Flask app creation failed")
        return False
    
    print("\n" + "=" * 70)
    print("SETUP COMPLETE - ALL SYSTEMS READY")
    print("=" * 70)
    print("\nTo start the server, run:")
    print("  python run.py")
    print("\nThen visit:")
    print("  http://127.0.0.1:5000/")
    print("\n" + "=" * 70)
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

