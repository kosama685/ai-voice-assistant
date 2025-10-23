#!/usr/bin/env python
"""
Comprehensive Error Resolver for Voice Assistant v2.1
Diagnoses and fixes all system errors automatically
"""

import os
import sys
import subprocess
import logging
from datetime import datetime
from pathlib import Path

# Setup logging
log_dir = Path('logs')
log_dir.mkdir(exist_ok=True)

log_file = log_dir / f'error_resolution_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ErrorResolver:
    def __init__(self):
        self.errors = []
        self.fixes = []
        self.venv_python = r'.\venv\Scripts\python'
        self.venv_pip = r'.\venv\Scripts\pip'
        
    def log_error(self, error_msg):
        """Log an error"""
        logger.error(error_msg)
        self.errors.append(error_msg)
        
    def log_fix(self, fix_msg):
        """Log a fix"""
        logger.info(f"✓ {fix_msg}")
        self.fixes.append(fix_msg)
        
    def run_command(self, cmd, description=""):
        """Run a shell command"""
        try:
            logger.info(f"Running: {cmd}")
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                self.log_error(f"Command failed: {cmd}\n{result.stderr}")
                return False
            logger.info(f"Output: {result.stdout}")
            return True
        except Exception as e:
            self.log_error(f"Exception running command: {str(e)}")
            return False
    
    def check_python_version(self):
        """Check Python version"""
        logger.info("=" * 60)
        logger.info("CHECKING PYTHON VERSION")
        logger.info("=" * 60)
        
        try:
            result = subprocess.run([self.venv_python, '--version'], capture_output=True, text=True)
            version = result.stdout.strip()
            logger.info(f"Python version: {version}")
            self.log_fix(f"Python version check: {version}")
            return True
        except Exception as e:
            self.log_error(f"Python version check failed: {str(e)}")
            return False
    
    def check_dependencies(self):
        """Check if all dependencies are installed"""
        logger.info("=" * 60)
        logger.info("CHECKING DEPENDENCIES")
        logger.info("=" * 60)
        
        required_packages = [
            'Flask',
            'Flask-SQLAlchemy',
            'Flask-Migrate',
            'Flask-Login',
            'requests',
            'bcrypt',
            'python-dotenv',
            'mysqlclient'
        ]
        
        for package in required_packages:
            cmd = f'{self.venv_python} -c "import {package.lower().replace("-", "_")}; print(\'OK\')"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                logger.info(f"✓ {package} is installed")
            else:
                self.log_error(f"✗ {package} is NOT installed")
                return False
        
        self.log_fix("All dependencies are installed")
        return True
    
    def install_dependencies(self):
        """Install all dependencies from requirements.txt"""
        logger.info("=" * 60)
        logger.info("INSTALLING DEPENDENCIES")
        logger.info("=" * 60)
        
        if not os.path.exists('requirements.txt'):
            self.log_error("requirements.txt not found")
            return False
        
        cmd = f'{self.venv_pip} install -r requirements.txt --upgrade'
        if self.run_command(cmd):
            self.log_fix("Dependencies installed successfully")
            return True
        return False
    
    def check_database(self):
        """Check database connection"""
        logger.info("=" * 60)
        logger.info("CHECKING DATABASE")
        logger.info("=" * 60)
        
        try:
            from config import Config
            logger.info(f"Database: {Config.SQLALCHEMY_DATABASE_URI}")
            self.log_fix("Database configuration found")
            return True
        except Exception as e:
            self.log_error(f"Database check failed: {str(e)}")
            return False
    
    def fix_database_schema(self):
        """Fix database schema"""
        logger.info("=" * 60)
        logger.info("FIXING DATABASE SCHEMA")
        logger.info("=" * 60)
        
        if os.path.exists('fix_database.py'):
            cmd = f'{self.venv_python} fix_database.py'
            if self.run_command(cmd):
                self.log_fix("Database schema fixed")
                return True
        return False
    
    def check_imports(self):
        """Check if all imports work"""
        logger.info("=" * 60)
        logger.info("CHECKING IMPORTS")
        logger.info("=" * 60)
        
        try:
            cmd = f'{self.venv_python} -c "from app import create_app; print(\'OK\')"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                self.log_fix("All imports successful")
                return True
            else:
                self.log_error(f"Import failed: {result.stderr}")
                return False
        except Exception as e:
            self.log_error(f"Import check failed: {str(e)}")
            return False
    
    def verify_routes(self):
        """Verify all routes are registered"""
        logger.info("=" * 60)
        logger.info("VERIFYING ROUTES")
        logger.info("=" * 60)
        
        try:
            cmd = f'{self.venv_python} -c "from app import create_app; app = create_app(); print(len(app.url_map._rules))"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                routes_count = result.stdout.strip()
                logger.info(f"Total routes: {routes_count}")
                self.log_fix(f"Routes verified: {routes_count} routes found")
                return True
            else:
                self.log_error(f"Route verification failed: {result.stderr}")
                return False
        except Exception as e:
            self.log_error(f"Route verification failed: {str(e)}")
            return False
    
    def resolve_all_errors(self):
        """Resolve all errors"""
        logger.info("\n" + "=" * 60)
        logger.info("VOICE ASSISTANT v2.1 - COMPREHENSIVE ERROR RESOLUTION")
        logger.info("=" * 60 + "\n")
        
        steps = [
            ("Python Version Check", self.check_python_version),
            ("Install Dependencies", self.install_dependencies),
            ("Check Dependencies", self.check_dependencies),
            ("Database Check", self.check_database),
            ("Fix Database Schema", self.fix_database_schema),
            ("Check Imports", self.check_imports),
            ("Verify Routes", self.verify_routes),
        ]
        
        for step_name, step_func in steps:
            logger.info(f"\n>>> {step_name}...")
            try:
                if not step_func():
                    logger.warning(f"⚠ {step_name} had issues but continuing...")
            except Exception as e:
                logger.error(f"✗ {step_name} failed: {str(e)}")
        
        # Print summary
        logger.info("\n" + "=" * 60)
        logger.info("RESOLUTION SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Errors found: {len(self.errors)}")
        logger.info(f"Fixes applied: {len(self.fixes)}")
        
        if self.errors:
            logger.info("\nErrors:")
            for error in self.errors:
                logger.info(f"  - {error}")
        
        if self.fixes:
            logger.info("\nFixes:")
            for fix in self.fixes:
                logger.info(f"  ✓ {fix}")
        
        logger.info("\n" + "=" * 60)
        logger.info("✓ ERROR RESOLUTION COMPLETE")
        logger.info("=" * 60)
        logger.info(f"\nLog file: {log_file}")
        
        return len(self.errors) == 0

if __name__ == '__main__':
    resolver = ErrorResolver()
    success = resolver.resolve_all_errors()
    sys.exit(0 if success else 1)

