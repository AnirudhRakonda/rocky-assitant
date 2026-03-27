"""
Audio output module for playback.

Handles audio playback using sounddevice.
"""

import numpy as np
from typing import Optional

from app.utils import logger
from app.config import SAMPLE_RATE

try:
    import sounddevice as sd
    SOUNDDEVICE_AVAILABLE = True
except ImportError:
    SOUNDDEVICE_AVAILABLE = False
    logger.warning("sounddevice not installed")


class AudioOutput:
    """Handles audio playback."""

    def __init__(self, sample_rate: int = SAMPLE_RATE):
        """
        Initialize audio output.

        Args:
            sample_rate: Target sample rate in Hz
        """
        if not SOUNDDEVICE_AVAILABLE:
            raise RuntimeError("sounddevice not installed. "
                             "Install with: pip install sounddevice")

        self.sample_rate = sample_rate
        logger.info(f"Audio output initialized at {sample_rate} Hz")

    def play(
        self,
        audio_data: np.ndarray,
        blocking: bool = True,
        volume: float = 0.8
    ) -> None:
        """
        Play audio data.

        Args:
            audio_data: Audio waveform as numpy array (float32, -1.0 to 1.0)
            blocking: Wait for playback to complete
            volume: Volume multiplier (0.0 to 1.0, default 0.8)
        """
        try:
            # Apply volume
            audio = audio_data * volume

            # Clip to prevent clipping distortion
            audio = np.clip(audio, -1.0, 1.0)

            logger.debug(f"Playing audio: {len(audio)} samples, volume={volume}")

            sd.play(audio, samplerate=self.sample_rate, blocking=blocking)

        except Exception as e:
            logger.warning(f"Audio playback skipped: {str(e)[:80]}")
            logger.debug("This is OK - audio device may not be available")
            # Don't raise - allow app to continue

    def stop(self) -> None:
        """Stop current playback."""
        try:
            sd.stop()
            logger.debug("Playback stopped")
        except Exception as e:
            logger.error(f"Failed to stop playback: {e}")

    @staticmethod
    def list_devices() -> None:
        """Print available audio devices."""
        if SOUNDDEVICE_AVAILABLE:
            print("\nAvailable audio devices:")
            print(sd.query_devices())


# Singleton instance
_audio_output: Optional[AudioOutput] = None


def get_audio_output() -> AudioOutput:
    """Get or create audio output instance."""
    global _audio_output
    if _audio_output is None:
        _audio_output = AudioOutput()
    return _audio_output
