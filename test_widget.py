#!/usr/bin/env python
"""
Test Widget Integration
Verifies all widget components are working correctly
"""

import sys
import os

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test all imports"""
    print("✅ Testing imports...")
    try:
        from app import create_app
        print("  ✓ app.create_app")
        
        from routes.widget import widget_bp
        print("  ✓ routes.widget.widget_bp")
        
        from routes.widget import WidgetSession
        print("  ✓ routes.widget.WidgetSession")
        
        print("✅ All imports successful!\n")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}\n")
        return False

def test_app_creation():
    """Test app creation with widget blueprint"""
    print("✅ Testing app creation...")
    try:
        from app import create_app
        app = create_app()
        print("  ✓ App created successfully")
        
        # Check if widget blueprint is registered
        blueprints = app.blueprints
        if 'widget' in blueprints:
            print("  ✓ Widget blueprint registered")
        else:
            print("  ✗ Widget blueprint NOT registered")
            return False
        
        print("✅ App creation successful!\n")
        return True
    except Exception as e:
        print(f"❌ App creation error: {e}\n")
        return False

def test_widget_session():
    """Test WidgetSession class"""
    print("✅ Testing WidgetSession...")
    try:
        from routes.widget import WidgetSession
        
        session = WidgetSession("test_session_123")
        print("  ✓ WidgetSession created")
        
        session.add_message("user", "Hello")
        print("  ✓ Message added")
        
        session.add_message("assistant", "Hi there!")
        print("  ✓ Response added")
        
        data = session.to_dict()
        assert data['session_id'] == "test_session_123"
        assert len(data['messages']) == 2
        assert data['turn_count'] == 2
        print("  ✓ Session data correct")
        
        print("✅ WidgetSession tests passed!\n")
        return True
    except Exception as e:
        print(f"❌ WidgetSession error: {e}\n")
        return False

def test_routes():
    """Test widget routes"""
    print("✅ Testing widget routes...")
    try:
        from app import create_app
        app = create_app()
        
        with app.test_client() as client:
            # Test health check
            response = client.get('/widget/health')
            assert response.status_code == 200
            print("  ✓ Health check endpoint")
            
            # Test chat endpoint
            response = client.post('/widget/api/chat', 
                json={'message': 'Hello', 'sessionId': 'test_123'})
            assert response.status_code == 200
            data = response.get_json()
            assert data['success'] == True
            print("  ✓ Chat endpoint")
            
            # Test session endpoint
            response = client.get('/widget/api/session/test_123')
            assert response.status_code == 200
            print("  ✓ Session endpoint")
            
            print("✅ All routes working!\n")
            return True
    except Exception as e:
        print(f"❌ Route error: {e}\n")
        import traceback
        traceback.print_exc()
        return False

def test_static_files():
    """Test static files exist"""
    print("✅ Testing static files...")
    try:
        widget_js = os.path.join(os.path.dirname(__file__), 'static', 'widget.js')
        if os.path.exists(widget_js):
            print(f"  ✓ widget.js exists ({os.path.getsize(widget_js)} bytes)")
        else:
            print("  ✗ widget.js NOT found")
            return False
        
        print("✅ Static files OK!\n")
        return True
    except Exception as e:
        print(f"❌ Static files error: {e}\n")
        return False

def test_templates():
    """Test template files exist"""
    print("✅ Testing templates...")
    try:
        templates = [
            'widget_demo.html',
            'widget_dashboard.html'
        ]
        
        for template in templates:
            path = os.path.join(os.path.dirname(__file__), 'templates', template)
            if os.path.exists(path):
                print(f"  ✓ {template} exists")
            else:
                print(f"  ✗ {template} NOT found")
                return False
        
        print("✅ All templates OK!\n")
        return True
    except Exception as e:
        print(f"❌ Template error: {e}\n")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🎤 VOICE ASSISTANT WIDGET - TEST SUITE")
    print("="*60 + "\n")
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("App Creation", test_app_creation()))
    results.append(("WidgetSession", test_widget_session()))
    results.append(("Static Files", test_static_files()))
    results.append(("Templates", test_templates()))
    results.append(("Routes", test_routes()))
    
    print("="*60)
    print("📊 TEST RESULTS")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print("="*60)
    print(f"\n🎉 {passed}/{total} tests passed!\n")
    
    if passed == total:
        print("✅ ALL TESTS PASSED - WIDGET IS PRODUCTION READY!")
        return 0
    else:
        print("❌ SOME TESTS FAILED - PLEASE FIX ISSUES")
        return 1

if __name__ == '__main__':
    sys.exit(main())

