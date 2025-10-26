#!/usr/bin/env python3
"""
Test Flask API endpoints
"""

import requests
import json
import time

BASE_URL = 'http://127.0.0.1:5000'

def test_widget_chat():
    """Test widget chat endpoint"""
    print("=" * 60)
    print("Testing Widget Chat API")
    print("=" * 60)
    
    url = f"{BASE_URL}/widget/api/chat"
    headers = {"Content-Type": "application/json"}
    payload = {
        "message": "Hello, how are you?",
        "sessionId": "test-session-123",
        "synthesize": False
    }
    
    print(f"\n📍 URL: {url}")
    print(f"📦 Payload: {json.dumps(payload, indent=2)}")
    
    try:
        print("\n🚀 Sending request...")
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        print(f"\n✅ Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ SUCCESS!")
            print(f"📄 Response: {json.dumps(data, indent=2)}")
            
            if data.get('success'):
                print(f"\n💬 Assistant: {data.get('response')}")
            else:
                print(f"\n❌ Error: {data.get('error')}")
        else:
            print(f"\n❌ ERROR!")
            print(f"📄 Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("\n❌ Connection error - Flask server may not be running")
        print(f"   Make sure to start the server with: python run.py")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

if __name__ == '__main__':
    print("Waiting for Flask server to be ready...")
    time.sleep(2)
    test_widget_chat()

