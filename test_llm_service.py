#!/usr/bin/env python3
"""
Test LLM Service directly
"""

import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set environment variables
os.environ['GEMINI_API_KEY'] = 'AIzaSyBHAl_-FQIXwNK43WUs0c6vxQMKf0OKw14'
os.environ['GEMINI_MODEL'] = 'gemini-2.0-flash'

from services.llm_service import llm_service

def test_llm_service():
    """Test LLM service"""
    print("=" * 60)
    print("Testing LLM Service")
    print("=" * 60)
    
    print("\n🚀 Sending request to LLM service...")
    
    try:
        result = llm_service.generate_response("Hello, how are you?")
        
        print(f"\n✅ Status: {result['success']}")
        
        if result['success']:
            print(f"💬 Response: {result['response']}")
            print(f"📊 Provider: {result['provider']}")
            print(f"⏱️ Timestamp: {result['timestamp']}")
        else:
            print(f"❌ Error: {result['error']}")
            
    except Exception as e:
        print(f"\n❌ Exception: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_llm_service()

