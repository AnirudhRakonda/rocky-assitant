"""
Audio synthesizer for chord generation.

Generates waveforms from frequency specifications.
"""

import numpy as np
from typing import List, Tuple

from app.utils import logger
from app.config import SAMPLE_RATE, AUDIO_DURATION_DEFAULT


class ToneSynthesizer:
    """Generates audio waveforms from frequency specifications."""

    def __init__(self, sample_rate: int = SAMPLE_RATE):
        """
        Initialize synthesizer.

        Args:
            sample_rate: Audio sample rate in Hz
        """
        self.sample_rate = sample_rate
        logger.info(f"Tone synthesizer initialized at {sample_rate} Hz")

    def generate_sine_wave(
        self,
        frequency: float,
        duration: float
    ) -> np.ndarray:
        """
        Generate a pure sine wave.

        Args:
            frequency: Frequency in Hz
            duration: Duration in seconds

        Returns:
            Audio samples as numpy array (float32)
        """
        num_samples = int(duration * self.sample_rate)
        t = np.arange(num_samples) / self.sample_rate
        wave = np.sin(2 * np.pi * frequency * t).astype(np.float32)
        return wave

    def generate_chord(
        self,
        frequencies: List[float],
        duration: float
    ) -> np.ndarray:
        """
        Generate a chord (multiple frequencies played together).

        Args:
            frequencies: List of frequencies in Hz
            duration: Duration in seconds

        Returns:
            Combined waveform (normalized)
        """
        if not frequencies:
            # Return silence
            return np.zeros(int(duration * self.sample_rate), dtype=np.float32)

        # Generate individual sine waves
        waves = [self.generate_sine_wave(f, duration) for f in frequencies]

        # Mix waves (average them)
        combined = np.mean(waves, axis=0).astype(np.float32)

        # Normalize to prevent clipping
        max_val = np.max(np.abs(combined))
        if max_val > 0:
            combined = combined / max_val * 0.95

        return combined

    def generate_from_chords(
        self,
        chords: List[Tuple[List[float], float]]
    ) -> np.ndarray:
        """
        Generate complete waveform from chord sequence.

        Args:
            chords: List of (frequencies, duration) tuples

        Returns:
            Complete audio waveform (float32)
        """
        waveforms = []

        for frequencies, duration in chords:
            if duration > 0:
                wave = self.generate_chord(frequencies, duration)
                waveforms.append(wave)

        if not waveforms:
            return np.array([], dtype=np.float32)

        # Concatenate all waveforms
        complete = np.concatenate(waveforms).astype(np.float32)

        # Final normalization
        max_val = np.max(np.abs(complete))
        if max_val > 0:
            complete = complete / max_val * 0.9

        return complete

    def apply_fade(
        self,
        waveform: np.ndarray,
        fade_in_ms: float = 50,
        fade_out_ms: float = 50
    ) -> np.ndarray:
        """
        Apply fade-in and fade-out to waveform.

        Args:
            waveform: Input waveform
            fade_in_ms: Fade-in duration in milliseconds
            fade_out_ms: Fade-out duration in milliseconds

        Returns:
            Faded waveform
        """
        result = waveform.copy()
        fade_in_samples = int(fade_in_ms * self.sample_rate / 1000)
        fade_out_samples = int(fade_out_ms * self.sample_rate / 1000)

        if fade_in_samples > 0:
            fade_in = np.linspace(0, 1, fade_in_samples)
            result[:fade_in_samples] *= fade_in

        if fade_out_samples > 0 and len(result) > fade_out_samples:
            fade_out = np.linspace(1, 0, fade_out_samples)
            result[-fade_out_samples:] *= fade_out

        return result


# Singleton instance
_synthesizer: ToneSynthesizer = None


def get_synthesizer() -> ToneSynthesizer:
    """Get or create synthesizer instance."""
    global _synthesizer
    if _synthesizer is None:
        _synthesizer = ToneSynthesizer()
    return _synthesizer
