"""
Main assistant pipeline orchestrator.

Coordinates all components: speech input, LLM, tone generation, and audio output.
"""

from typing import Optional
import time

from app.utils import logger
from app.audio import get_audio_input, get_speech_recognition, get_audio_output
from app.brain import get_llm
from app.rocky_voice import ChordMapper, get_synthesizer, get_emotion_analyzer
from app.audio.effects import ToneEffects
from app.config import INTERACTIVE_MODE, EMOTION_MODULATION


class RockyAssistant:
    """Main orchestrator for Rocky alien communication assistant."""

    def __init__(self):
        """Initialize all components."""
        logger.info("Initializing Rocky Assistant...")

        self.audio_input = get_audio_input()
        self.speech_recognition = get_speech_recognition()
        self.audio_output = get_audio_output()
        self.llm = get_llm()
        self.chord_mapper = ChordMapper()
        self.synthesizer = get_synthesizer()
        self.tone_effects = ToneEffects()
        self.emotion_analyzer = get_emotion_analyzer()

        self.conversation_history = []
        logger.info("Rocky Assistant initialized successfully")

    def listen(self, timeout: float = 10) -> str:
        """
        Listen for user speech.

        Args:
            timeout: Maximum listening time in seconds

        Returns:
            Transcribed text
        """
        try:
            logger.info("Listening for speech...")
            audio_data = self.audio_input.detect_speech_end(timeout=timeout)

            if len(audio_data) == 0:
                logger.warning("No speech detected")
                return ""

            text = self.speech_recognition.transcribe(audio_data)
            logger.info(f"User: {text}")

            return text

        except KeyboardInterrupt:
            logger.info("Listening interrupted")
            return ""
        except Exception as e:
            logger.error(f"Listening failed: {e}")
            return ""

    def think(self, user_input: str) -> str:
        """
        Generate response using LLM.

        Args:
            user_input: User's spoken input

        Returns:
            Rocky's response
        """
        try:
            # Build conversation context
            context = "\n".join(self.conversation_history[-4:]) if self.conversation_history else None

            # Get response from LLM
            response = self.llm.generate(
                prompt=user_input,
                context=context,
                temperature=0.7
            )

            logger.info(f"Rocky: {response}")

            return response

        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            return "Processing error."

    def speak(self, text: str) -> None:
        """
        Convert text to tone sequence and play.

        Args:
            text: Text to convert to tones
        """
        try:
            logger.info(f"Converting to tones: {text[:50]}...")

            # Analyze emotion to modulate tone
            emotion = self.emotion_analyzer.analyze(text)
            tone_params = self.emotion_analyzer.get_tone_parameters(emotion)

            # Convert text to chords
            chords = self.chord_mapper.text_to_chords(text)

            if not chords:
                logger.warning("No chords generated")
                return

            # Apply emotion modulation to chord frequencies
            if EMOTION_MODULATION:
                modulated_chords = []
                for frequencies, duration in chords:
                    if frequencies:
                        # Apply frequency shift based on emotion
                        shift = tone_params['frequency_shift']
                        shifted_freqs = [f * shift for f in frequencies]
                        modulated_chords.append((shifted_freqs, duration))
                    else:
                        modulated_chords.append((frequencies, duration))
                chords = modulated_chords

            # Generate waveform
            waveform = self.synthesizer.generate_from_chords(chords)

            # Apply effects
            waveform = self.tone_effects.apply_all(
                waveform,
                base_frequency=440,
                use_adsr=True,
                use_vibrato=True,
                use_harmonics=True
            )

            # Apply fade
            waveform = self.synthesizer.apply_fade(waveform)

            # Play audio
            logger.debug(f"Playing tone sequence ({len(waveform)} samples)")
            self.audio_output.play(waveform, blocking=True, volume=0.7)
            logger.info(f"🎵 Tone sequence complete ({len(waveform)} samples, {len(waveform)/22050:.1f}s)")

        except Exception as e:
            logger.warning(f"Tone generation issue (non-fatal): {str(e)[:80]}")
            logger.debug("Application will continue - audio may be unavailable")

    def run(self, test_input: Optional[str] = None) -> None:
        """
        Run the main interactive loop.

        Args:
            test_input: Optional test input (for non-interactive mode)
        """
        try:
            logger.info("Starting Rocky Assistant...")
            logger.info("Type 'quit' to exit\n")

            # Print welcome
            print("\n" + "="*60)
            print("🎵 ROCKY ASSISTANT - ALIEN COMMUNICATION SYSTEM 🎵")
            print("="*60)
            print("\nRocky is listening... (Use non-interactive mode for speech input)")
            print("\nEnter messages (or 'quit' to exit):\n")

            iteration = 0
            while True:
                iteration += 1
                logger.debug(f"=== Iteration {iteration} ===")

                # Get user input
                if test_input:
                    user_input = test_input
                    test_input = None
                else:
                    try:
                        # Standard interactive mode (text input)
                        user_input = input("You: ").strip()
                    except EOFError:
                        # When running in non-interactive terminal
                        logger.info("EOF detected, exiting")
                        break

                if not user_input:
                    continue

                if user_input.lower() == 'quit':
                    logger.info("User requested exit")
                    break

                # Process: Think -> Speak
                try:
                    # Add to history
                    self.conversation_history.append(f"User: {user_input}")

                    # Generate response
                    response = self.think(user_input)

                    if response:
                        self.conversation_history.append(f"Rocky: {response}")

                        # Convert to tones and play
                        print(f"\nRocky: {response}\n")
                        self.speak(response)
                    else:
                        print("Rocky: [No response]\n")

                    print("-" * 60 + "\n")

                except KeyboardInterrupt:
                    logger.info("Processing interrupted")
                    print("\n[Processing interrupted]\n")
                    break
                except Exception as e:
                    logger.error(f"Conversation loop error: {e}")
                    print(f"[Error: {e}]\n")

        except KeyboardInterrupt:
            logger.info("Application interrupted by user")
        except Exception as e:
            logger.error(f"Fatal error in main loop: {e}")
            raise
        finally:
            logger.info("Rocky Assistant shutting down")
            self.audio_output.stop()
            print("\n" + "="*60)
            print("Rocky has returned to the stars. Goodbye!")
            print("="*60 + "\n")


# Singleton instance
_assistant: Optional[RockyAssistant] = None


def get_assistant() -> RockyAssistant:
    """Get or create assistant instance."""
    global _assistant
    if _assistant is None:
        _assistant = RockyAssistant()
    return _assistant
