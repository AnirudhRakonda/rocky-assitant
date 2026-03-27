"""
Example usage of Rocky Assistant API.

This script demonstrates how to use Rocky programmatically.
"""

from app.pipeline import get_assistant
from app.rocky_voice import ChordMapper, get_synthesizer, get_emotion_analyzer
from app.audio import get_audio_output


def example_1_basic_interaction():
    """Example 1: Basic conversation with output."""
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic Interaction")
    print("="*60)

    assistant = get_assistant()

    # Test inputs (no speech recognition)
    test_messages = [
        "What is your name?",
        "How are you feeling?",
        "Tell me about physics."
    ]

    for user_input in test_messages:
        print(f"\nYou: {user_input}")
        response = assistant.think(user_input)
        print(f"Rocky: {response}")
        # In a real scenario, you'd call: assistant.speak(response)


def example_2_direct_tone_generation():
    """Example 2: Generate tones directly from text."""
    print("\n" + "="*60)
    print("EXAMPLE 2: Direct Tone Generation")
    print("="*60)

    mapper = ChordMapper()
    synth = get_synthesizer()
    audio_output = get_audio_output()

    text = "Hello world"
    print(f"\nConverting to tones: '{text}'")

    # Convert text to chords
    chords = mapper.text_to_chords(text)
    print(f"Generated {len(chords)} chord events")

    # Generate waveform
    waveform = synth.generate_from_chords(chords)
    print(f"Generated waveform: {len(waveform)} samples")

    # Play (if you have speakers/headphones)
    print("Playing audio...")
    audio_output.play(waveform, blocking=True, volume=0.7)


def example_3_emotion_analysis():
    """Example 3: Analyze emotions in text."""
    print("\n" + "="*60)
    print("EXAMPLE 3: Emotion Analysis")
    print("="*60)

    analyzer = get_emotion_analyzer()

    texts = [
        "How fascinating! Tell me more about this discovery!",
        "I do not understand human emotions. Why?",
        "There is a critical problem we must solve.",
        "This is a standard communication.",
    ]

    for text in texts:
        emotion = analyzer.analyze(text)
        params = analyzer.get_tone_parameters(emotion)
        print(f"\nText: '{text}'")
        print(f"Emotion: {emotion.value}")
        print(f"Freq shift: {params['frequency_shift']:.2f}x")


def example_4_chord_mapping():
    """Example 4: Explore chord mappings."""
    print("\n" + "="*60)
    print("EXAMPLE 4: Chord Mapping Exploration")
    print("="*60)

    mapper = ChordMapper()

    print("\nVowel mappings (first 5):")
    for vowel in ['a', 'e', 'i', 'o', 'u']:
        chord = mapper.freq_map.get(vowel)
        if chord:
            avg_freq = sum(chord) / len(chord)
            print(f"  {vowel}: {chord[0]:.1f}, {chord[1]:.1f}, {chord[2]:.1f} Hz (avg: {avg_freq:.1f})")

    print("\nConsonant mappings (first 5):")
    for consonant in ['b', 'c', 'd', 'f', 'g']:
        chord = mapper.freq_map.get(consonant)
        if chord:
            avg_freq = sum(chord) / len(chord)
            print(f"  {consonant}: {chord[0]:.1f}, {chord[1]:.1f} Hz (avg: {avg_freq:.1f})")


def example_5_waveform_stats():
    """Example 5: Analyze generated waveforms."""
    print("\n" + "="*60)
    print("EXAMPLE 5: Waveform Analysis")
    print("="*60)

    import numpy as np
    mapper = ChordMapper()
    synth = get_synthesizer()

    text = "Rocky"
    chords = mapper.text_to_chords(text)
    waveform = synth.generate_from_chords(chords)

    print(f"\nText: '{text}'")
    print(f"Chord events: {len(chords)}")
    print(f"Waveform samples: {len(waveform)}")
    print(f"Duration: {len(waveform) / 22050:.3f} seconds")
    print(f"Min value: {np.min(waveform):.4f}")
    print(f"Max value: {np.max(waveform):.4f}")
    print(f"Mean value: {np.mean(waveform):.4f}")
    print(f"RMS energy: {np.sqrt(np.mean(waveform**2)):.4f}")


if __name__ == "__main__":
    print("\n🎵 Rocky Assistant - Usage Examples 🎵\n")

    try:
        # Run examples
        example_1_basic_interaction()
        example_3_emotion_analysis()
        example_4_chord_mapping()
        example_5_waveform_stats()

        # Uncomment this if you want audio output (requires speakers):
        # example_2_direct_tone_generation()

        print("\n" + "="*60)
        print("Examples complete!")
        print("="*60 + "\n")

    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        print("\nMake sure:")
        print("  1. Ollama is running: ollama serve")
        print("  2. Model is downloaded: ollama pull mistral")
        print("  3. Dependencies installed: pip install -r requirements.txt")
