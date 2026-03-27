"""
Text to musical chords mapper.

Converts text into sequences of frequencies (chords) for alien-like communication.
"""

import random
from typing import List, Dict, Tuple
import string

from app.utils import logger
from app.config import TONE_PITCH_BASE, RANDOMNESS_FACTOR


class ChordMapper:
    """Maps text to musical chords."""

    # Define character classes
    VOWELS = set('aeiouAEIOU')
    CONSONANTS = set(string.ascii_letters) - VOWELS
    PUNCTUATION = set('.,!?;:')

    def __init__(self, base_frequency: float = TONE_PITCH_BASE):
        """
        Initialize chord mapper.

        Args:
            base_frequency: Base frequency for chord generation (Hz)
        """
        self.base_frequency = base_frequency
        self._build_frequency_map()
        logger.info(f"Chord mapper initialized with base frequency: {base_frequency} Hz")

    def _build_frequency_map(self) -> None:
        """Build deterministic frequency mappings for characters."""
        self.freq_map: Dict[str, List[float]] = {}

        # Vowels: higher frequencies (more resonant, musical)
        vowel_bases = [
            self.base_frequency * 1.2,      # ~528 Hz
            self.base_frequency * 1.5,      # ~660 Hz
            self.base_frequency * 1.87,     # ~823 Hz
            self.base_frequency * 2.25,     # ~990 Hz
            self.base_frequency * 2.67,     # ~1175 Hz
        ]

        for i, vowel in enumerate(sorted(self.VOWELS)):
            idx = i % len(vowel_bases)
            self.freq_map[vowel] = self._generate_chord(
                vowel_bases[idx],
                num_notes=3
            )

        # Consonants: medium frequencies
        consonant_bases = [
            self.base_frequency * 0.8,      # ~352 Hz
            self.base_frequency * 0.9,      # ~396 Hz
            self.base_frequency * 1.0,      # ~440 Hz
            self.base_frequency * 1.1,      # ~484 Hz
            self.base_frequency * 1.25,     # ~550 Hz
            self.base_frequency * 1.4,      # ~616 Hz
        ]

        for i, consonant in enumerate(sorted(self.CONSONANTS)):
            idx = i % len(consonant_bases)
            self.freq_map[consonant] = self._generate_chord(
                consonant_bases[idx],
                num_notes=2
            )

        # Punctuation and numbers: distinctive patterns
        for char in self.PUNCTUATION:
            self.freq_map[char] = self._generate_chord(
                self.base_frequency * 0.5,  # Lower frequency
                num_notes=1
            )

        # Numbers
        for i in range(10):
            digit_freq = self.base_frequency * (0.5 + i * 0.3)
            self.freq_map[str(i)] = self._generate_chord(digit_freq, num_notes=2)

    def _generate_chord(
        self,
        base_freq: float,
        num_notes: int = 3,
        interval: float = 1.25
    ) -> List[float]:
        """
        Generate a chord (multiple frequencies) around a base frequency.

        Args:
            base_freq: Base frequency in Hz
            num_notes: Number of notes in the chord
            interval: Frequency multiplier between notes

        Returns:
            List of frequencies (Hz)
        """
        chord = []
        for i in range(num_notes):
            freq = base_freq * (interval ** (i - (num_notes - 1) / 2))
            # Add slight randomness for "aliveness"
            if RANDOMNESS_FACTOR > 0:
                variation = 1.0 + random.uniform(-RANDOMNESS_FACTOR, RANDOMNESS_FACTOR)
                freq *= variation
            chord.append(freq)
        return chord

    def text_to_chords(
        self,
        text: str,
        add_pauses: bool = True
    ) -> List[Tuple[List[float], float]]:
        """
        Convert text to sequence of (chord, duration) tuples.

        Args:
            text: Input text
            add_pauses: Add pauses between words

        Returns:
            List of (frequencies, duration_in_seconds) tuples
        """
        chords_sequence = []
        words = text.split()

        for word_idx, word in enumerate(words):
            for char_idx, char in enumerate(word):
                char_lower = char.lower()

                if char_lower in self.freq_map:
                    chord = self.freq_map[char_lower]
                else:
                    # Unknown character: use neutral tone
                    chord = self._generate_chord(self.base_frequency, num_notes=1)

                # Duration varies:
                # - Vowels: longer (more resonant)
                # - Consonants: medium
                # - Punctuation: short
                if char_lower in self.VOWELS:
                    duration = 0.12
                elif char_lower in self.CONSONANTS:
                    duration = 0.08
                elif char_lower in self.PUNCTUATION:
                    duration = 0.06
                else:
                    duration = 0.10

                chords_sequence.append((chord, duration))

                # Add brief space between characters within word
                if char_idx < len(word) - 1:
                    chords_sequence.append(([], 0.02))  # 20ms silence

            # Add pause between words
            if add_pauses and word_idx < len(words) - 1:
                chords_sequence.append(([], 0.15))  # 150ms silence

        return chords_sequence

    def get_chord_for_emotion(
        self,
        emotion: str,
        base_chord: List[float]
    ) -> List[float]:
        """
        Modulate a chord based on emotional state.

        Args:
            emotion: 'happy', 'sad', 'curious', 'concerned'
            base_chord: Original chord frequencies

        Returns:
            Modulated frequencies
        """
        if not base_chord:
            return []

        modulated = []
        for freq in base_chord:
            if emotion == 'happy':
                # Higher frequencies for positive emotions
                new_freq = freq * 1.1
            elif emotion == 'sad':
                # Lower frequencies for negative emotions
                new_freq = freq * 0.9
            elif emotion == 'curious':
                # Slight upward shift with more variation
                new_freq = freq * (1.0 + random.uniform(0, 0.15))
            elif emotion == 'concerned':
                # Downward shift, slightly dissonant
                new_freq = freq * (0.95 + random.uniform(-0.05, 0))
            else:
                new_freq = freq

            modulated.append(new_freq)

        return modulated
