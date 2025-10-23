import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'

    # Database configuration
    DB_CONNECTION = os.environ.get('DB_CONNECTION', 'mysql')
    DB_HOST = os.environ.get('DB_HOST', '127.0.0.1')
    DB_PORT = os.environ.get('DB_PORT', '3306')
    DB_DATABASE = os.environ.get('DB_DATABASE', 'voiceast')
    DB_USERNAME = os.environ.get('DB_USERNAME', 'root')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'root')

    # Construct database URI
    SQLALCHEMY_DATABASE_URI = f"{DB_CONNECTION}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ============ AI & LLM CONFIGURATION ============
    # Google Gemini API
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', 'AIzaSyBHAl_-FQIXwNK43WUs0c6vxQMKf0OKw14')
    GEMINI_MODEL = os.environ.get('GEMINI_MODEL', 'gemini-1.5-flash')

    # ============ SPEECH-TO-TEXT (ASR) CONFIGURATION ============
    # Google Speech-to-Text API
    GOOGLE_CLOUD_PROJECT = os.environ.get('GOOGLE_CLOUD_PROJECT', 'projects/500069590671')
    GOOGLE_CLOUD_CREDENTIALS = os.environ.get('GOOGLE_CLOUD_CREDENTIALS', '')

    # Whisper (OpenAI) - Local or API
    WHISPER_MODEL = os.environ.get('WHISPER_MODEL', 'base')  # base, small, medium, large
    WHISPER_USE_LOCAL = os.environ.get('WHISPER_USE_LOCAL', 'true').lower() == 'true'

    # ============ TEXT-TO-SPEECH (TTS) CONFIGURATION ============
    # Google Cloud TTS
    GOOGLE_TTS_ENABLED = os.environ.get('GOOGLE_TTS_ENABLED', 'true').lower() == 'true'

    # ElevenLabs TTS
    ELEVENLABS_API_KEY = os.environ.get('ELEVENLABS_API_KEY', '')
    ELEVENLABS_VOICE_ID = os.environ.get('ELEVENLABS_VOICE_ID', 'EXAVITQu4vr4xnSDxMaL')

    # Coqui TTS (Local)
    COQUI_TTS_ENABLED = os.environ.get('COQUI_TTS_ENABLED', 'true').lower() == 'true'
    COQUI_TTS_MODEL = os.environ.get('COQUI_TTS_MODEL', 'tts_models/en/ljspeech/tacotron2-DDC')

    # ============ PAYMENT GATEWAY ============
    CLICKPAY_PROFILE_ID = os.environ.get('CLICKPAY_PROFILE_ID', '44272')
    CLICKPAY_SERVER_KEY = os.environ.get('CLICKPAY_SERVER_KEY', 'SHJNLTLLM2-JLNJLDLZLH-GBRHMTJ92M')

    # ============ FEATURE FLAGS ============
    ENABLE_VOICE_CHAT = os.environ.get('ENABLE_VOICE_CHAT', 'true').lower() == 'true'
    ENABLE_AI_RESPONSES = os.environ.get('ENABLE_AI_RESPONSES', 'true').lower() == 'true'
    ENABLE_ANALYTICS = os.environ.get('ENABLE_ANALYTICS', 'true').lower() == 'true'
    ENABLE_PAYMENT = os.environ.get('ENABLE_PAYMENT', 'true').lower() == 'true'