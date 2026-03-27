"""
Configuration module for Rocky Assistant.

Central configuration management for all system parameters.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project root
PROJECT_ROOT = Path(__file__).parent.parent

# ============================================================================
# AUDIO CONFIGURATION
# ============================================================================
SAMPLE_RATE = 22050  # Hz
AUDIO_DURATION_DEFAULT = 0.15  # seconds per tone
AUDIO_CHUNK_SIZE = 2048  # for streaming

# ============================================================================
# LLM CONFIGURATION
# ============================================================================
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_TIMEOUT = 60  # seconds

# ============================================================================
# SPEECH RECOGNITION
# ============================================================================
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")  # tiny, base, small, medium, large
SPEECH_TIMEOUT = 10  # seconds to wait for speech
SILENCE_THRESHOLD = 0.02  # audio level threshold to detect silence
MIN_SPEECH_DURATION = 0.5  # minimum seconds required to process

# ============================================================================
# ROCKY VOICE SYSTEM
# ============================================================================
TONE_PITCH_BASE = 440  # Hz - A4 base note
VIBRATO_RATE = 5  # Hz
VIBRATO_DEPTH = 20  # Hz
EMOTION_INTENSITY = 1.0  # 0.0 to 2.0

# ADSR Envelope (Attack, Decay, Sustain, Release) in seconds
ENVELOPE_ATTACK = 0.05
ENVELOPE_DECAY = 0.1
ENVELOPE_SUSTAIN = 0.3
ENVELOPE_RELEASE = 0.1

# Chord configuration (frequencies per character)
CHORD_FREQUENCIES = {
    'vowel': [440, 550, 660],
    'consonant': [330, 440, 550],
    'punctuation': [220, 330],
    'silence': []  # pauses
}

# ============================================================================
# LOGGING
# ============================================================================
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)

# ============================================================================
# BEHAVIOR
# ============================================================================
DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"
INTERACTIVE_MODE = True  # continuous listening
EMOTION_MODULATION = True  # vary tones based on emotion
RANDOMNESS_FACTOR = 0.1  # slight randomness in frequencies (0-1)
