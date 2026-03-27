#!/usr/bin/env python
"""
Quick test runner for Rocky Assistant.
"""
import sys
sys.path.insert(0, '/Users/anirudhrakonda/Desktop/rocky/rocky-assistant')

print("\n" + "="*60)
print("🎵 ROCKY ASSISTANT - TEST MODE 🎵")
print("="*60 + "\n")

print("🔄 Loading components...")

try:
    from app import get_assistant
    print("✓ Application loaded")
    
    assistant = get_assistant()
    print("✓ Assistant initialized")
    
    # Test with sample input
    print("\n" + "-"*60)
    print("Processing test input: 'Hello Rocky!'")
    print("-"*60 + "\n")
    
    response = assistant.think("Hello Rocky!")
    print(f"\n✓ LLM Response: {response['response'][:100] if isinstance(response, dict) else response[:100]}...")
    
    print("\n🎵 Tone generation would play here in interactive mode\n")
    print("="*60)
    print("✓ Test completed successfully!")
    print("="*60 + "\n")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print(f"\nTroubleshooting checklist:")
    print(f"1. Is Ollama running? (ollama serve)")
    print(f"2. Is a model available? (ollama list)")
    print(f"3. Are dependencies installed? (pip install -r requirements.txt)")
    import traceback
    traceback.print_exc()
