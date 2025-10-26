#!/usr/bin/env python3
"""
Voice Assistant Setup Script
Automated setup for all voice assistant components
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BLUE}{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.END}")

def run_command(cmd, description):
    """Run a shell command"""
    print_info(f"Running: {description}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print_success(f"{description} completed")
            return True
        else:
            print_error(f"{description} failed: {result.stderr}")
            return False
    except Exception as e:
        print_error(f"{description} error: {str(e)}")
        return False

def check_python_version():
    """Check Python version"""
    print_header("Checking Python Version")
    
    version = sys.version_info
    print_info(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print_success("Python version is compatible")
        return True
    else:
        print_error("Python 3.8+ is required")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    print_header("Checking Dependencies")
    
    required = [
        'flask',
        'flask_sqlalchemy',
        'flask_login',
        'dotenv',
        'requests',
        'google.generativeai',
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package.replace('.', '_'))
            print_success(f"{package} is installed")
        except ImportError:
            print_warning(f"{package} is not installed")
            missing.append(package)
    
    return len(missing) == 0

def install_dependencies():
    """Install Python dependencies"""
    print_header("Installing Dependencies")
    
    if not os.path.exists('requirements.txt'):
        print_error("requirements.txt not found")
        return False
    
    return run_command(
        'pip install -r requirements.txt',
        'Installing Python dependencies'
    )

def install_whisper():
    """Install Whisper for local speech-to-text"""
    print_header("Installing Whisper (Speech-to-Text)")
    
    print_info("Whisper is optional but recommended for offline speech recognition")
    response = input("Install Whisper? (y/n): ").lower()
    
    if response == 'y':
        return run_command(
            'pip install openai-whisper',
            'Installing Whisper'
        )
    else:
        print_info("Skipping Whisper installation")
        return True

def install_coqui_tts():
    """Install Coqui TTS for local text-to-speech"""
    print_header("Installing Coqui TTS (Text-to-Speech)")
    
    print_info("Coqui TTS is optional but recommended for offline speech synthesis")
    response = input("Install Coqui TTS? (y/n): ").lower()
    
    if response == 'y':
        return run_command(
            'pip install TTS',
            'Installing Coqui TTS'
        )
    else:
        print_info("Skipping Coqui TTS installation")
        return True

def setup_env_file():
    """Setup .env file"""
    print_header("Setting Up Environment File")
    
    if os.path.exists('.env'):
        print_warning(".env file already exists")
        response = input("Overwrite? (y/n): ").lower()
        if response != 'y':
            return True
    
    if not os.path.exists('.env.example'):
        print_error(".env.example not found")
        return False
    
    try:
        shutil.copy('.env.example', '.env')
        print_success(".env file created from template")
        
        # Prompt for API key
        print_info("\nConfiguring API keys...")
        gemini_key = input("Enter Gemini API key (or press Enter to use default): ").strip()
        
        if gemini_key:
            with open('.env', 'r') as f:
                content = f.read()
            
            content = content.replace(
                'GEMINI_API_KEY=AIzaSyBHAl_-FQIXwNK43WUs0c6vxQMKf0OKw14',
                f'GEMINI_API_KEY={gemini_key}'
            )
            
            with open('.env', 'w') as f:
                f.write(content)
            
            print_success("Gemini API key configured")
        
        return True
    except Exception as e:
        print_error(f"Failed to setup .env: {str(e)}")
        return False

def create_directories():
    """Create necessary directories"""
    print_header("Creating Directories")
    
    directories = [
        'logs',
        'uploads',
        'models',
        'cache',
    ]
    
    for directory in directories:
        try:
            Path(directory).mkdir(exist_ok=True)
            print_success(f"Directory created: {directory}")
        except Exception as e:
            print_error(f"Failed to create {directory}: {str(e)}")
            return False
    
    return True

def run_tests():
    """Run integration tests"""
    print_header("Running Integration Tests")
    
    if not os.path.exists('test_voice_integration.py'):
        print_warning("test_voice_integration.py not found")
        return True
    
    response = input("Run integration tests? (y/n): ").lower()
    
    if response == 'y':
        return run_command(
            'python test_voice_integration.py',
            'Running integration tests'
        )
    else:
        print_info("Skipping tests")
        return True

def print_summary():
    """Print setup summary"""
    print_header("Setup Complete!")
    
    print_success("Voice Assistant is ready to use!")
    print_info("\nNext steps:")
    print_info("1. Configure API keys in .env file")
    print_info("2. Start Flask application: python run.py")
    print_info("3. Access test page: http://127.0.0.1:5000/voice-assistant-test")
    print_info("4. Check documentation: VOICE_ASSISTANT_INTEGRATION_GUIDE.md")
    
    print_info("\nUseful commands:")
    print_info("  python run.py                    - Start Flask app")
    print_info("  python test_voice_integration.py - Run tests")
    print_info("  pip install -r requirements.txt  - Install dependencies")
    
    print_info("\nDocumentation:")
    print_info("  VOICE_ASSISTANT_INTEGRATION_GUIDE.md - Setup guide")
    print_info("  VOICE_ASSISTANT_FEATURES.md          - Features list")
    print_info("  VOICE_ASSISTANT_README.md            - Project README")

def main():
    """Main setup function"""
    print(f"\n{Colors.BLUE}")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║     🎤 VOICE ASSISTANT SETUP SCRIPT                        ║")
    print("║                                                            ║")
    print("║     This script will setup all voice assistant components  ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}")
    
    steps = [
        ("Check Python Version", check_python_version),
        ("Check Dependencies", check_dependencies),
        ("Install Dependencies", install_dependencies),
        ("Install Whisper", install_whisper),
        ("Install Coqui TTS", install_coqui_tts),
        ("Create Directories", create_directories),
        ("Setup Environment File", setup_env_file),
        ("Run Tests", run_tests),
    ]
    
    completed = 0
    for step_name, step_func in steps:
        try:
            if step_func():
                completed += 1
            else:
                print_warning(f"Skipped: {step_name}")
        except Exception as e:
            print_error(f"Error in {step_name}: {str(e)}")
    
    print_summary()
    
    print(f"\n{Colors.BLUE}Setup completed: {completed}/{len(steps)} steps{Colors.END}\n")
    
    return 0 if completed == len(steps) else 1

if __name__ == '__main__':
    sys.exit(main())

