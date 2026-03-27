"""Rocky Assistant Audio Module.

Handles audio input, output, and effects.
"""

from app.audio.input import get_audio_input, get_speech_recognition, AudioInput, SpeechRecognition
from app.audio.output import get_audio_output, AudioOutput
from app.audio.effects import ADSREnvelope, Vibrato, ToneEffects

__all__ = [
    'get_audio_input',
    'get_speech_recognition',
    'AudioInput',
    'SpeechRecognition',
    'get_audio_output',
    'AudioOutput',
    'ADSREnvelope',
    'Vibrato',
    'ToneEffects',
]
