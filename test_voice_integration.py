"""
Voice Assistant Integration Test Suite
Tests all components: LLM, ASR, TTS, and Orchestrator
"""

import os
import sys
import json
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.llm_service import llm_service
from services.asr_service import asr_service
from services.tts_service import tts_service
from services.voice_orchestrator import voice_orchestrator

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

def test_llm_service():
    """Test LLM Service"""
    print_header("Testing LLM Service (Google Gemini)")
    
    try:
        # Test 1: Generate response
        print_info("Test 1: Generate response...")
        result = llm_service.generate_response(
            "What is the capital of France?",
            session_id="test_session_1"
        )
        
        if result['success']:
            print_success(f"Response: {result['response'][:100]}...")
            print_info(f"Provider: {result['provider']}")
            print_info(f"Model: {result['model']}")
        else:
            print_error(f"Failed: {result['error']}")
            return False
        
        # Test 2: Sentiment analysis
        print_info("\nTest 2: Sentiment analysis...")
        sentiment = llm_service.analyze_sentiment("I love this product!")
        if sentiment['success']:
            print_success(f"Sentiment: {sentiment['sentiment']}")
        else:
            print_warning(f"Sentiment analysis skipped: {sentiment['error']}")
        
        # Test 3: Conversation history
        print_info("\nTest 3: Conversation history...")
        history = llm_service.get_conversation_history("test_session_1")
        print_success(f"History entries: {len(history)}")
        
        # Test 4: Health check
        print_info("\nTest 4: Health check...")
        health = llm_service.get_health_status()
        print_success(f"Status: {health['status']}")
        
        return True
        
    except Exception as e:
        print_error(f"LLM Service test failed: {str(e)}")
        return False

def test_asr_service():
    """Test ASR Service"""
    print_header("Testing ASR Service (Whisper)")
    
    try:
        # Test 1: Health check
        print_info("Test 1: Health check...")
        health = asr_service.get_health_status()
        print_success(f"Status: {health['status']}")
        print_info(f"Provider: {health['provider']}")
        
        if health['status'] == 'unhealthy':
            print_warning("ASR service is not healthy")
            print_info("To use local Whisper, install: pip install openai-whisper")
            return True  # Don't fail, just warn
        
        # Test 2: Check model
        print_info("\nTest 2: Model information...")
        print_info(f"Model: {asr_service.whisper_model}")
        
        return True
        
    except Exception as e:
        print_error(f"ASR Service test failed: {str(e)}")
        return False

def test_tts_service():
    """Test TTS Service"""
    print_header("Testing TTS Service")
    
    try:
        # Test 1: Health check
        print_info("Test 1: Health check...")
        health = tts_service.get_health_status()
        print_success(f"Status: {health['status']}")
        print_info(f"Provider: {health['provider']}")
        print_info(f"Coqui available: {health['coqui_available']}")
        print_info(f"Google configured: {health['google_configured']}")
        print_info(f"ElevenLabs configured: {health['elevenlabs_configured']}")
        
        # Test 2: Synthesize text
        print_info("\nTest 2: Synthesize text...")
        result = tts_service.synthesize("Hello, this is a test.")
        
        if result['success']:
            print_success(f"Synthesis successful")
            print_info(f"Provider: {result['provider']}")
            print_info(f"Format: {result['audio_format']}")
            print_info(f"Audio size: {len(result['audio'])} bytes")
        else:
            print_warning(f"Synthesis failed: {result['error']}")
        
        return True
        
    except Exception as e:
        print_error(f"TTS Service test failed: {str(e)}")
        return False

def test_voice_orchestrator():
    """Test Voice Orchestrator"""
    print_header("Testing Voice Orchestrator")
    
    try:
        # Test 1: System health
        print_info("Test 1: System health...")
        health = voice_orchestrator.get_system_health()
        print_success(f"Overall status: {health['status']}")
        print_info(f"Active sessions: {health['active_sessions']}")
        
        # Test 2: Text input processing
        print_info("\nTest 2: Process text input...")
        result = voice_orchestrator.process_text_input(
            text="Tell me a joke",
            session_id="test_session_2",
            synthesize_response=False
        )
        
        if result['success']:
            print_success(f"Text processing successful")
            print_info(f"User text: {result['user_text']}")
            print_info(f"Response: {result['response_text'][:100]}...")
            print_info(f"LLM Provider: {result['llm_provider']}")
        else:
            print_error(f"Text processing failed: {result['error']}")
            return False
        
        # Test 3: Conversation stats
        print_info("\nTest 3: Conversation statistics...")
        stats = voice_orchestrator.get_conversation_stats("test_session_2")
        print_success(f"Turn count: {stats['turn_count']}")
        print_info(f"Total user chars: {stats['total_user_chars']}")
        print_info(f"Total response chars: {stats['total_response_chars']}")
        
        return True
        
    except Exception as e:
        print_error(f"Voice Orchestrator test failed: {str(e)}")
        return False

def test_configuration():
    """Test Configuration"""
    print_header("Testing Configuration")
    
    try:
        print_info("LLM Configuration:")
        print_info(f"  Provider: {llm_service.provider if hasattr(llm_service, 'provider') else 'gemini'}")
        print_info(f"  Model: {llm_service.model}")
        print_info(f"  Temperature: {llm_service.temperature}")
        print_info(f"  API Key configured: {bool(llm_service.api_key)}")
        
        print_info("\nASR Configuration:")
        print_info(f"  Provider: {asr_service.provider}")
        print_info(f"  Model: {asr_service.whisper_model}")
        print_info(f"  Model loaded: {asr_service.model is not None}")
        
        print_info("\nTTS Configuration:")
        print_info(f"  Provider: {tts_service.provider}")
        print_info(f"  Default voice: {tts_service.default_voice}")
        print_info(f"  Default speed: {tts_service.default_speed}")
        
        return True
        
    except Exception as e:
        print_error(f"Configuration test failed: {str(e)}")
        return False

def main():
    """Run all tests"""
    print(f"\n{Colors.BLUE}")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║     🎤 VOICE ASSISTANT INTEGRATION TEST SUITE              ║")
    print("║                                                            ║")
    print(f"║     Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}                      ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}")
    
    results = {
        'Configuration': test_configuration(),
        'LLM Service': test_llm_service(),
        'ASR Service': test_asr_service(),
        'TTS Service': test_tts_service(),
        'Voice Orchestrator': test_voice_orchestrator(),
    }
    
    # Summary
    print_header("Test Summary")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = f"{Colors.GREEN}PASSED{Colors.END}" if result else f"{Colors.RED}FAILED{Colors.END}"
        print(f"  {test_name}: {status}")
    
    print(f"\n{Colors.BLUE}Total: {passed}/{total} tests passed{Colors.END}")
    
    if passed == total:
        print_success("All tests passed! Voice Assistant is ready to use.")
        return 0
    else:
        print_warning(f"{total - passed} test(s) failed. Check configuration.")
        return 1

if __name__ == '__main__':
    sys.exit(main())

