"""
Speech input module for audio capture and transcription.

Handles microphone recording and local speech-to-text conversion using faster-whisper.
"""

import numpy as np
from typing import Optional, Tuple

from app.utils import logger
from app.config import (
    SAMPLE_RATE, SPEECH_TIMEOUT, SILENCE_THRESHOLD,
    MIN_SPEECH_DURATION, DEBUG_MODE
)

try:
    import sounddevice as sd
    SOUNDDEVICE_AVAILABLE = True
except ImportError:
    SOUNDDEVICE_AVAILABLE = False
    logger.warning("sounddevice not installed")

try:
    from faster_whisper import WhisperModel
    WHISPER_AVAILABLE = True
except ImportError:
    try:
        import whisper
        WHISPER_AVAILABLE = True
    except ImportError:
        WHISPER_AVAILABLE = False
        logger.warning("faster-whisper or whisper not installed")


class AudioInput:
    """Handles audio capture from microphone."""

    def __init__(self, sample_rate: int = SAMPLE_RATE):
        """
        Initialize audio input device.

        Args:
            sample_rate: Audio sample rate in Hz
        """
        if not SOUNDDEVICE_AVAILABLE:
            raise RuntimeError("sounddevice not installed. "
                             "Install with: pip install sounddevice")

        self.sample_rate = sample_rate
        logger.info(f"Audio input initialized at {sample_rate} Hz")

    def record(self, duration: float) -> np.ndarray:
        """
        Record audio from microphone for specified duration.

        Args:
            duration: Recording duration in seconds

        Returns:
            Audio data as numpy array (mono, float32)
        """
        try:
            logger.info(f"Recording for {duration} seconds...")
            audio = sd.rec(
                int(duration * self.sample_rate),
                samplerate=self.sample_rate,
                channels=1,
                dtype=np.float32,
                blocksize=2048
            )
            sd.wait()
            logger.info(f"Recording complete. Duration: {len(audio) / self.sample_rate:.2f}s")
            return audio.flatten()

        except Exception as e:
            logger.error(f"Recording failed: {e}")
            raise

    def detect_speech_end(self, timeout: float = SPEECH_TIMEOUT) -> np.ndarray:
        """
        Record until speech ends (silence detected).

        Args:
            timeout: Maximum recording duration in seconds

        Returns:
            Audio data
        """
        logger.info("Listening for speech (press Ctrl+C to stop)...")
        
        chunk_size = int(self.sample_rate * 0.1)  # 100ms chunks
        chunks = []
        silence_count = 0
        max_silence_chunks = int(1.0 / (chunk_size / self.sample_rate))  # 1 second silence threshold

        try:
            stream = sd.InputStream(
                samplerate=self.sample_rate,
                channels=1,
                blocksize=chunk_size,
                dtype=np.float32
            )
            stream.start()

            with stream:
                for _ in range(int(timeout * self.sample_rate / chunk_size)):
                    chunk, _ = stream.read(chunk_size)
                    chunk = chunk.flatten()
                    chunks.append(chunk)

                    # Check if chunk is mostly silent
                    energy = np.mean(np.abs(chunk))
                    if energy < SILENCE_THRESHOLD:
                        silence_count += 1
                    else:
                        silence_count = 0

                    # If enough silence detected and we have speech
                    if silence_count > max_silence_chunks and len(chunks) > int(MIN_SPEECH_DURATION * self.sample_rate / chunk_size):
                        logger.info("Speech ended detected")
                        break

            if chunks:
                return np.concatenate(chunks)
            return np.array([], dtype=np.float32)

        except Exception as e:
            logger.error(f"Speech detection failed: {e}")
            raise


class SpeechRecognition:
    """Handles speech-to-text conversion."""

    def __init__(self, model_size: str = "base"):
        """
        Initialize speech recognition model.

        Args:
            model_size: Model size (tiny, base, small, medium, large)
        """
        if not WHISPER_AVAILABLE:
            raise RuntimeError("faster-whisper or whisper not installed. "
                             "Install with: pip install faster-whisper")

        try:
            # Try faster-whisper first (faster)
            self.model = WhisperModel(model_size, device="cpu", compute_type="int8")
            self.use_faster_whisper = True
            logger.info(f"Loaded faster-whisper model: {model_size}")
        except:
            try:
                # Fallback to regular whisper
                import whisper
                self.model = whisper.load_model(model_size)
                self.use_faster_whisper = False
                logger.info(f"Loaded whisper model: {model_size}")
            except Exception as e:
                logger.error(f"Failed to load speech recognition model: {e}")
                raise

    def transcribe(self, audio: np.ndarray, sample_rate: int = SAMPLE_RATE) -> str:
        """
        Transcribe audio to text.

        Args:
            audio: Audio data as numpy array
            sample_rate: Sample rate of audio

        Returns:
            Transcribed text
        """
        try:
            if DEBUG_MODE:
                logger.debug(f"Transcribing audio ({len(audio)} samples)...")

            if self.use_faster_whisper:
                # faster-whisper returns (segments, info)
                segments, info = self.model.transcribe(audio, language="en")
                text = " ".join([segment.text for segment in segments])
            else:
                # Regular whisper
                result = self.model.transcribe(audio, language="en")
                text = result.get("text", "").strip()

            if DEBUG_MODE:
                logger.debug(f"Transcribed: {text}")

            logger.info(f"Speech recognized: {text[:100]}..." if len(text) > 100 else f"Speech recognized: {text}")
            return text

        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            return ""


# Singleton instances
_audio_input: Optional[AudioInput] = None
_speech_recognition: Optional[SpeechRecognition] = None


def get_audio_input() -> AudioInput:
    """Get or create audio input instance."""
    global _audio_input
    if _audio_input is None:
        _audio_input = AudioInput()
    return _audio_input


def get_speech_recognition() -> SpeechRecognition:
    """Get or create speech recognition instance."""
    global _speech_recognition
    if _speech_recognition is None:
        _speech_recognition = SpeechRecognition()
    return _speech_recognition
