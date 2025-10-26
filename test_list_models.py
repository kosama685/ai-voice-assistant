#!/usr/bin/env python3
"""
List available Gemini models
"""

import requests
import json

API_KEY = 'AIzaSyBHAl_-FQIXwNK43WUs0c6vxQMKf0OKw14'
BASE_URL = 'https://generativelanguage.googleapis.com/v1beta/models'

def list_models():
    """List available models"""
    print("=" * 60)
    print("Listing Available Gemini Models")
    print("=" * 60)
    
    url = f"{BASE_URL}"
    headers = {
        "Content-Type": "application/json",
    }
    
    print(f"\n📍 URL: {url}")
    print(f"🔑 API Key: {API_KEY[:20]}...")
    
    try:
        print("\n🚀 Sending request...")
        response = requests.get(
            f"{url}?key={API_KEY}",
            headers=headers,
            timeout=30
        )
        
        print(f"\n✅ Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ SUCCESS!")
            print(f"📄 Response: {json.dumps(data, indent=2)}")
            
            if 'models' in data:
                print(f"\n📋 Available Models:")
                for model in data['models']:
                    print(f"  - {model['name']}")
                    if 'supportedGenerationMethods' in model:
                        print(f"    Methods: {model['supportedGenerationMethods']}")
        else:
            print(f"\n❌ ERROR!")
            print(f"📄 Response: {response.text}")
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

if __name__ == '__main__':
    list_models()

