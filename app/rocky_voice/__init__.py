"""Rocky Assistant Voice Module.

Handles text-to-tone conversion with emotion and effects.
"""

from app.rocky_voice.mapper import ChordMapper
from app.rocky_voice.synthesizer import get_synthesizer, ToneSynthesizer
from app.rocky_voice.emotions import get_emotion_analyzer, EmotionAnalyzer, Emotion

__all__ = [
    'ChordMapper',
    'get_synthesizer',
    'ToneSynthesizer',
    'get_emotion_analyzer',
    'EmotionAnalyzer',
    'Emotion',
]
