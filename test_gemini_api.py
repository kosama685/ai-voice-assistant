#!/usr/bin/env python3
"""
Test Gemini API directly
"""

import requests
import json

API_KEY = 'AIzaSyBHAl_-FQIXwNK43WUs0c6vxQMKf0OKw14'
MODEL = 'gemini-2.0-flash'
BASE_URL = 'https://generativelanguage.googleapis.com/v1beta/models'

def test_gemini_api():
    """Test Gemini API"""
    print("=" * 60)
    print("Testing Gemini API")
    print("=" * 60)
    
    url = f"{BASE_URL}/{MODEL}:generateContent"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "VoiceAssistant/2.3"
    }
    
    payload = {
        "contents": [{
            "parts": [{"text": "Hello, how are you?"}]
        }],
        "generationConfig": {
            "temperature": 0.7,
            "topK": 40,
            "topP": 0.95,
            "maxOutputTokens": 1024,
        }
    }
    
    print(f"\n📍 URL: {url}")
    print(f"🔑 API Key: {API_KEY[:20]}...")
    print(f"📦 Payload: {json.dumps(payload, indent=2)}")
    
    try:
        print("\n🚀 Sending request...")
        response = requests.post(
            f"{url}?key={API_KEY}",
            json=payload,
            headers=headers,
            timeout=30
        )
        
        print(f"\n✅ Status Code: {response.status_code}")
        print(f"📝 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ SUCCESS!")
            print(f"📄 Response: {json.dumps(data, indent=2)}")
            
            if 'candidates' in data and data['candidates']:
                text = data['candidates'][0]['content']['parts'][0]['text']
                print(f"\n💬 Assistant: {text}")
            else:
                print("\n⚠️ No candidates in response")
        else:
            print(f"\n❌ ERROR!")
            print(f"📄 Response: {response.text}")
            
    except requests.exceptions.Timeout:
        print("\n❌ Request timeout")
    except requests.exceptions.ConnectionError as e:
        print(f"\n❌ Connection error: {str(e)}")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

if __name__ == '__main__':
    test_gemini_api()

