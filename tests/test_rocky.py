"""
Test suite for Rocky Assistant.

Run tests with: pytest tests/
"""

import pytest
import numpy as np
from app.rocky_voice import ChordMapper, get_synthesizer
from app.audio.effects import ADSREnvelope, Vibrato, ToneEffects
from app.rocky_voice.emotions import EmotionAnalyzer, Emotion


class TestChordMapper:
    """Test chord mapping functionality."""

    def test_mapper_initialization(self):
        """Test chord mapper initializes correctly."""
        mapper = ChordMapper()
        assert mapper.base_frequency == 440

    def test_vowel_mapping(self):
        """Test vowel characters map to chords."""
        mapper = ChordMapper()
        chord = mapper.freq_map.get('a')
        assert chord is not None
        assert len(chord) == 3  # Vowels are 3-note chords

    def test_consonant_mapping(self):
        """Test consonant characters map to chords."""
        mapper = ChordMapper()
        chord = mapper.freq_map.get('b')
        assert chord is not None
        assert len(chord) == 2  # Consonants are 2-note chords

    def test_text_to_chords(self):
        """Test text conversion to chord sequence."""
        mapper = ChordMapper()
        chords = mapper.text_to_chords("hi")
        assert len(chords) > 0
        assert all(isinstance(c, tuple) and len(c) == 2 for c in chords)

    def test_emotion_modulation(self):
        """Test emotion-based chord modulation."""
        mapper = ChordMapper()
        base_chord = [440, 550, 660]

        happy_chord = mapper.get_chord_for_emotion('happy', base_chord)
        sad_chord = mapper.get_chord_for_emotion('sad', base_chord)

        # Happy should have higher frequencies
        assert np.mean(happy_chord) > np.mean(base_chord)
        # Sad should have lower frequencies
        assert np.mean(sad_chord) < np.mean(base_chord)


class TestSynthesizer:
    """Test audio synthesis."""

    def test_synthesizer_initialization(self):
        """Test synthesizer initializes."""
        synth = get_synthesizer()
        assert synth.sample_rate == 22050

    def test_sine_wave_generation(self):
        """Test sine wave generation."""
        synth = get_synthesizer()
        wave = synth.generate_sine_wave(440, 0.1)
        assert len(wave) == int(440 * 0.1 / 440 * 22050)  # ~2205 samples
        assert wave.dtype == np.float32
        assert np.max(np.abs(wave)) <= 1.0

    def test_chord_generation(self):
        """Test chord (multi-frequency) generation."""
        synth = get_synthesizer()
        freqs = [440, 550, 660]
        chord = synth.generate_chord(freqs, 0.1)
        assert len(chord) > 0
        assert chord.dtype == np.float32

    def test_empty_chord(self):
        """Test empty chord generates silence."""
        synth = get_synthesizer()
        silence = synth.generate_chord([], 0.1)
        assert np.all(silence == 0)


class TestADSREnvelope:
    """Test ADSR envelope."""

    def test_envelope_initialization(self):
        """Test ADSR envelope initializes."""
        envelope = ADSREnvelope()
        assert envelope.attack_samples > 0
        assert envelope.sustain_level == 0.8

    def test_envelope_application(self):
        """Test envelope application to waveform."""
        envelope = ADSREnvelope()
        wave = np.ones(22050)  # 1 second
        enveloped = envelope.apply(wave)

        assert len(enveloped) == len(wave)
        # Start should be lower (attack)
        assert enveloped[0] < enveloped[1000]
        # End should be lower (release)
        assert enveloped[-1] < enveloped[-1000]


class TestVibrato:
    """Test vibrato effect."""

    def test_vibrato_initialization(self):
        """Test vibrato initializes."""
        vibrato = Vibrato()
        assert vibrato.rate == 5.0
        assert vibrato.depth == 20.0

    def test_vibrato_application(self):
        """Test vibrato application."""
        vibrato = Vibrato(rate=5, depth=20)
        wave = np.sin(np.linspace(0, 2*np.pi*10, 22050))
        modulated = vibrato.apply(wave, 440, 440)

        assert len(modulated) == len(wave)
        assert modulated.dtype == np.float32


class TestEmotionAnalyzer:
    """Test emotion analysis."""

    def test_analyzer_initialization(self):
        """Test emotion analyzer initializes."""
        analyzer = EmotionAnalyzer()
        assert analyzer is not None

    def test_emotion_detection_curious(self):
        """Test detection of curious emotion."""
        analyzer = EmotionAnalyzer()
        emotion = analyzer.analyze("How does this fascinating process work?")
        assert emotion in [Emotion.CURIOUS, Emotion.EXCITED]

    def test_emotion_detection_confused(self):
        """Test detection of confused emotion."""
        analyzer = EmotionAnalyzer()
        emotion = analyzer.analyze("Why do humans experience emotions?")
        assert emotion in [Emotion.CONFUSED, Emotion.CURIOUS]

    def test_tone_parameters(self):
        """Test tone parameters for different emotions."""
        analyzer = EmotionAnalyzer()

        curious_params = analyzer.get_tone_parameters(Emotion.CURIOUS)
        excited_params = analyzer.get_tone_parameters(Emotion.EXCITED)

        # Excited should have higher frequency shift
        assert excited_params['frequency_shift'] > curious_params['frequency_shift']


class TestIntegration:
    """Integration tests for complete pipeline."""

    def test_text_to_audio_pipeline(self):
        """Test complete text-to-audio conversion."""
        mapper = ChordMapper()
        synth = get_synthesizer()

        text = "hello"
        chords = mapper.text_to_chords(text)
        waveform = synth.generate_from_chords(chords)

        assert len(waveform) > 0
        assert waveform.dtype == np.float32
        assert np.max(np.abs(waveform)) <= 1.0

    def test_effects_pipeline(self):
        """Test effects pipeline."""
        effects = ToneEffects()
        wave = np.sin(np.linspace(0, 2*np.pi*10, 22050))

        processed = effects.apply_all(
            wave,
            base_frequency=440,
            use_adsr=True,
            use_vibrato=True,
            use_harmonics=True
        )

        assert len(processed) == len(wave)
        assert processed.dtype == np.float32


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
