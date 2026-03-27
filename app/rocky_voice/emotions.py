"""
Emotion system for tone modulation.

Maps conversational context to emotional states that affect tone generation.
"""

from typing import Optional
from enum import Enum

from app.utils import logger


class Emotion(Enum):
    """Emotional states for Rocky."""
    NEUTRAL = "neutral"
    CURIOUS = "curious"
    CONFUSED = "confused"
    EXCITED = "excited"
    CONCERNED = "concerned"


class EmotionAnalyzer:
    """Analyzes conversation context to determine emotional state."""

    # Keywords that trigger emotions
    CURIOSITY_TRIGGERS = {
        'how', 'why', 'what', 'where', 'when', 'question',
        'explain', 'understand', 'meaning', 'function', 'work',
        'process', 'fascinating', 'interesting', 'curious'
    }

    CONFUSION_TRIGGERS = {
        'why', 'human', 'emotion', 'feeling', 'culture', 'social',
        'tradition', 'custom', 'strange', 'weird', 'odd', 'confuse',
        'not understand', "don't understand", "doesn't understand"
    }

    EXCITEMENT_TRIGGERS = {
        'discovery', 'found', 'breakthrough', 'eureka', 'solution',
        'success', 'excellent', 'amazing', 'great', 'fantastic',
        'engineering', 'technical', 'perfect', 'optimal', 'efficient'
    }

    CONCERN_TRIGGERS = {
        'problem', 'error', 'danger', 'risk', 'fail', 'wrong',
        'issue', 'threat', 'concern', 'worried', 'dangerous',
        'careful', 'warning', 'critical'
    }

    def __init__(self):
        """Initialize emotion analyzer."""
        logger.info("Emotion analyzer initialized")

    def analyze(self, text: str) -> Emotion:
        """
        Analyze text to determine emotional response.

        Args:
            text: Input text to analyze

        Returns:
            Emotion enum value
        """
        text_lower = text.lower()
        words = set(text_lower.split())

        # Count triggers
        curiosity_score = len(words & self.CURIOSITY_TRIGGERS)
        confusion_score = len(words & self.CONFUSION_TRIGGERS)
        excitement_score = len(words & self.EXCITEMENT_TRIGGERS)
        concern_score = len(words & self.CONCERN_TRIGGERS)

        scores = {
            Emotion.CURIOUS: curiosity_score,
            Emotion.CONFUSED: confusion_score,
            Emotion.EXCITED: excitement_score,
            Emotion.CONCERNED: concern_score,
        }

        # Find highest scoring emotion
        emotion = max(scores, key=scores.get)

        if max(scores.values()) == 0:
            emotion = Emotion.NEUTRAL

        logger.debug(f"Emotion analysis - Text: '{text[:50]}...' -> {emotion.value}")
        return emotion

    def get_tone_parameters(self, emotion: Emotion) -> dict:
        """
        Get tone generation parameters for emotion.

        Args:
            emotion: Emotional state

        Returns:
            Dictionary of tone parameters
        """
        params = {
            Emotion.CURIOUS: {
                'frequency_shift': 1.05,      # Slightly higher
                'vibrato_rate': 6.0,          # Faster vibrato
                'vibrato_depth': 25.0,        # Deeper modulation
                'sustain_level': 0.85,
            },
            Emotion.CONFUSED: {
                'frequency_shift': 0.98,      # Slightly lower
                'vibrato_rate': 4.0,          # Slower vibrato
                'vibrato_depth': 15.0,        # Subtle modulation
                'sustain_level': 0.7,
            },
            Emotion.EXCITED: {
                'frequency_shift': 1.15,      # Much higher
                'vibrato_rate': 8.0,          # Fast vibrato
                'vibrato_depth': 35.0,        # Deep modulation
                'sustain_level': 0.9,
            },
            Emotion.CONCERNED: {
                'frequency_shift': 0.92,      # Lower pitch
                'vibrato_rate': 3.0,          # Slow vibrato
                'vibrato_depth': 10.0,        # Minimal modulation
                'sustain_level': 0.65,
            },
            Emotion.NEUTRAL: {
                'frequency_shift': 1.0,
                'vibrato_rate': 5.0,
                'vibrato_depth': 20.0,
                'sustain_level': 0.8,
            },
        }

        return params.get(emotion, params[Emotion.NEUTRAL])


# Singleton instance
_emotion_analyzer: Optional[EmotionAnalyzer] = None


def get_emotion_analyzer() -> EmotionAnalyzer:
    """Get or create emotion analyzer instance."""
    global _emotion_analyzer
    if _emotion_analyzer is None:
        _emotion_analyzer = EmotionAnalyzer()
    return _emotion_analyzer
