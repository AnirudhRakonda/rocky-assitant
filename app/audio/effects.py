"""
Audio effects for alien-like tone modulation.

Implements vibrato, ADSR envelopes, and other effects.
"""

import numpy as np
from typing import Tuple

from app.utils import logger
from app.config import (
    SAMPLE_RATE, VIBRATO_RATE, VIBRATO_DEPTH,
    ENVELOPE_ATTACK, ENVELOPE_DECAY, ENVELOPE_SUSTAIN, ENVELOPE_RELEASE
)


class ADSREnvelope:
    """Attack, Decay, Sustain, Release envelope for amplitude modulation."""

    def __init__(
        self,
        attack: float = ENVELOPE_ATTACK,
        decay: float = ENVELOPE_DECAY,
        sustain: float = ENVELOPE_SUSTAIN,
        release: float = ENVELOPE_RELEASE,
        sustain_level: float = 0.8,
        sample_rate: int = SAMPLE_RATE
    ):
        """
        Initialize ADSR envelope.

        Args:
            attack: Attack time in seconds
            decay: Decay time in seconds
            sustain: Sustain time in seconds
            release: Release time in seconds
            sustain_level: Sustain amplitude (0-1)
            sample_rate: Sample rate in Hz
        """
        self.attack_samples = int(attack * sample_rate)
        self.decay_samples = int(decay * sample_rate)
        self.sustain_samples = int(sustain * sample_rate)
        self.release_samples = int(release * sample_rate)
        self.sustain_level = sustain_level

    def apply(self, samples: np.ndarray) -> np.ndarray:
        """
        Apply ADSR envelope to audio samples.

        Args:
            samples: Audio samples

        Returns:
            Enveloped samples
        """
        envelope = np.ones_like(samples)
        idx = 0

        # Attack: 0 to 1
        if self.attack_samples > 0:
            attack = np.linspace(0, 1, self.attack_samples)
            envelope[idx:idx + len(attack)] = attack
            idx += len(attack)

        # Decay: 1 to sustain_level
        if self.decay_samples > 0 and idx < len(envelope):
            decay = np.linspace(1, self.sustain_level, self.decay_samples)
            end_idx = min(idx + len(decay), len(envelope))
            envelope[idx:end_idx] = decay[:end_idx - idx]
            idx = end_idx

        # Sustain: stay at sustain_level
        if self.sustain_samples > 0 and idx < len(envelope):
            end_idx = min(idx + self.sustain_samples, len(envelope))
            envelope[idx:end_idx] = self.sustain_level
            idx = end_idx

        # Release: sustain_level to 0
        if self.release_samples > 0 and idx < len(envelope):
            remaining = len(envelope) - idx
            release = np.linspace(self.sustain_level, 0, min(self.release_samples, remaining))
            envelope[idx:idx + len(release)] = release
            idx += len(release)

        # Fade remaining to 0 if needed
        if idx < len(envelope):
            envelope[idx:] = 0

        return samples * envelope


class Vibrato:
    """Vibrato effect (frequency modulation)."""

    def __init__(
        self,
        rate: float = VIBRATO_RATE,
        depth: float = VIBRATO_DEPTH,
        sample_rate: int = SAMPLE_RATE
    ):
        """
        Initialize vibrato effect.

        Args:
            rate: Vibrato rate in Hz (typically 4-8 Hz)
            depth: Vibrato depth in Hz (typically 10-20 Hz)
            sample_rate: Sample rate in Hz
        """
        self.rate = rate
        self.depth = depth
        self.sample_rate = sample_rate

    def apply(
        self,
        samples: np.ndarray,
        base_frequency: float,
        carrier_frequency: float
    ) -> np.ndarray:
        """
        Apply vibrato to audio samples.

        Args:
            samples: Audio samples
            base_frequency: Base frequency of the tone
            carrier_frequency: Carrier frequency for modulation

        Returns:
            Vibrato-modulated samples
        """
        num_samples = len(samples)
        t = np.arange(num_samples) / self.sample_rate

        # LFO (Low Frequency Oscillator)
        lfo = np.sin(2 * np.pi * self.rate * t) * self.depth

        # Apply frequency modulation
        phase_mod = 2 * np.pi * np.cumsum(lfo) / self.sample_rate
        vibrato_samples = samples * np.sin(phase_mod)

        return vibrato_samples


class ToneEffects:
    """Collection of audio effects."""

    def __init__(self, sample_rate: int = SAMPLE_RATE):
        """Initialize effects processor."""
        self.sample_rate = sample_rate
        self.adsr = ADSREnvelope(sample_rate=sample_rate)
        self.vibrato = Vibrato(sample_rate=sample_rate)

    def add_harmonics(
        self,
        samples: np.ndarray,
        harmonics: list = [1, 2, 3]
    ) -> np.ndarray:
        """
        Add harmonic overtones.

        Args:
            samples: Base audio samples
            harmonics: List of harmonic multipliers (1=fundamental)

        Returns:
            Samples with added harmonics
        """
        result = samples * 0  # Start fresh
        weights = [1.0 / h for h in harmonics]  # Diminishing amplitude
        total_weight = sum(weights)

        for harmonic, weight in zip(harmonics, weights):
            result += samples * (weight / total_weight)

        return result

    def apply_all(
        self,
        samples: np.ndarray,
        base_frequency: float,
        use_adsr: bool = True,
        use_vibrato: bool = True,
        use_harmonics: bool = True
    ) -> np.ndarray:
        """
        Apply all effects to audio samples.

        Args:
            samples: Base audio samples
            base_frequency: Base frequency of the tone
            use_adsr: Apply ADSR envelope
            use_vibrato: Apply vibrato effect
            use_harmonics: Add harmonic overtones

        Returns:
            Processed samples
        """
        result = samples.copy()

        if use_harmonics:
            result = self.add_harmonics(result, harmonics=[1, 2, 3])

        if use_adsr:
            result = self.adsr.apply(result)

        if use_vibrato:
            result = self.vibrato.apply(result, base_frequency, base_frequency)

        return result
