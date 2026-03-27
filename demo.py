#!/usr/bin/env python
"""
Interactive demo of Rocky Assistant.
Shows LLM responses and tone generation for multiple queries.
"""
import sys
sys.path.insert(0, '/Users/anirudhrakonda/Desktop/rocky/rocky-assistant')

from app import get_assistant
import time

def demo():
    """Run the demo with multiple test inputs."""
    
    print("\n" + "="*70)
    print("🎵 ROCKY ASSISTANT - INTERACTIVE DEMO 🎵")
    print("="*70)
    
    assistant = get_assistant()
    
    print("\n✓ Rocky initialized and ready!\n")
    
    # Test inputs to showcase different emotions and responses
    test_messages = [
        "What is your name?",
        "How did you travel to Earth?",
        "What do you find curious about humans?",
        "Tell me about physics and mathematics"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print("-" * 70)
        print(f"[Query {i}/{len(test_messages)}]")
        print(f"You: {message}\n")
        
        try:
            # Get response from LLM
            response = assistant.think(message)
            print(f"Rocky: {response}\n")
            
            # Analyze emotion
            emotion = assistant.emotion_analyzer.analyze(response)
            print(f"📊 Detected Emotion: {emotion.value}")
            print(f"🎵 Generating musical response tones...\n")
            
            # Generate chords from response
            chords = assistant.chord_mapper.text_to_chords(response)
            print(f"   → Chord events generated: {len(chords)}")
            print(f"   → Character mapping: {response[:20]}... → {len(chords)} tones")
            
            # Synthesize waveform
            waveform = assistant.synthesizer.generate_from_chords(chords)
            print(f"   → Waveform synthesized: {len(waveform)} samples")
            print(f"   → Duration: {len(waveform)/22050:.2f} seconds")
            
            # Get tone parameters from emotion
            tone_params = assistant.emotion_analyzer.get_tone_parameters(emotion)
            print(f"   → Frequency shift: {tone_params['frequency_shift']:.2f}x")
            print(f"   → Vibrato rate: {tone_params['vibrato_rate']} Hz")
            print(f"   → Sustain level: {tone_params['sustain_level']:.2f}\n")
            
            # In real mode, would play here with: assistant.speak(response)
            print("🎵 [Musical tones would play here in full mode]\n")
            
        except Exception as e:
            print(f"❌ Error: {e}\n")
        
        if i < len(test_messages):
            time.sleep(0.5)
    
    print("-" * 70)
    print("\n" + "="*70)
    print("✓ Demo Complete!")
    print("="*70)
    print("\nTo run interactive mode, use:")
    print("  python app/main.py")
    print("\n🎵 Enjoy communicating with Rocky! 🎵\n")


if __name__ == "__main__":
    try:
        demo()
    except KeyboardInterrupt:
        print("\n\n⚠️ Demo interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
