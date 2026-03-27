# Rocky Assistant

🎵 **Rocky Assistant** - An alien communication system that speaks in musical tones, inspired by Rocky from *Project Hail Mary*.

Instead of traditional text-to-speech, Rocky generates **musical chords and tones** to simulate alien communication. Each character maps to unique frequencies, creating an otherworldly, harmonic language.

---

## 🌟 Features

- **Alien-like Musical Communication**: Generates chords and multi-frequency tones instead of speech
- **Local LLM**: Uses Ollama with Mistral/Llama3 (no cloud APIs)
- **Speech Input**: Converts human speech to text using local Whisper
- **Emotion Modulation**: Tones vary based on Rocky's emotional response
- **Audio Effects**: Vibrato, ADSR envelopes, harmonics for musicality
- **Production Architecture**: Modular, well-documented codebase

---

## 🎯 How It Works

1. **Listen**: Capture speech from microphone
2. **Transcribe**: Convert speech to text (local Whisper)
3. **Think**: Generate response using local LLM (Ollama)
4. **Analyze**: Determine emotional state from response
5. **Speak**: Convert text to musical chords
6. **Synthesize**: Generate waveform with effects
7. **Play**: Output alien-like audio tones

---

## 📋 Prerequisites

### System Requirements
- Python 3.8+
- macOS, Linux, or Windows
- Microphone (for speech input)
- Speakers/Headphones (for audio output)

### Required Software

#### 1. Ollama (Local LLM)

Download and install from: https://ollama.ai

After installation, pull a model:

```bash
ollama pull mistral
# or
ollama pull llama3
```

Start the Ollama server:

```bash
ollama serve
```

The server will run at `http://localhost:11434`

#### 2. Python Dependencies

```bash
pip install -r requirements.txt
```

---

## 🚀 Quick Start

### Setup

1. **Clone/create project**:
   ```bash
   cd rocky-assistant
   ```

2. **Create virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   # or
   venv\Scripts\activate  # Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env if needed (defaults should work)
   ```

### Running the Assistant

**Ensure Ollama is running first**:
```bash
ollama serve
```

**In another terminal, start Rocky**:

```bash
python app/main.py
```

**Or with test input**:
```bash
python app/main.py --test "Hello Rocky"
```

**With debug logging**:
```bash
python app/main.py --debug
```

---

## 💬 Example Interaction

```
============================================================
🎵 ROCKY ASSISTANT - ALIEN COMMUNICATION SYSTEM 🎵
============================================================

You: What is your name?

Rocky: I am Rocky. I come from far away star system.

[🎵 Musical alien tones play 🎵]

You: How did you survive your journey?
```

---

## 🗂️ Project Structure

```
rocky-assistant/
│
├── app/
│   ├── main.py                 # Entry point
│   ├── config.py               # Configuration
│   │
│   ├── brain/
│   │   ├── llm.py              # Ollama integration
│   │   └── prompts.py          # Rocky personality
│   │
│   ├── audio/
│   │   ├── input.py            # Microphone + Whisper
│   │   ├── output.py           # Audio playback
│   │   └── effects.py          # ADSR, vibrato effects
│   │
│   ├── rocky_voice/
│   │   ├── mapper.py           # Text → Chords
│   │   ├── synthesizer.py      # Waveform generation
│   │   └── emotions.py         # Emotion analysis
│   │
│   ├── pipeline/
│   │   └── assistant.py        # Main orchestrator
│   │
│   └── utils/
│       └── logger.py           # Logging
│
├── tests/                      # Test files
├── requirements.txt
├── .env.example
└── README.md
```

---

## ⚙️ Configuration

Edit `.env` to customize:

```env
# Model to use (mistral or llama3)
OLLAMA_MODEL=mistral

# Whisper model size (tiny, base, small, medium, large)
WHISPER_MODEL=base

# Logging level (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL=INFO

# Enable/disable debug mode
DEBUG_MODE=false
```

---

## 🎵 How Alien Tones Are Generated

### Text → Chords Mapping

Each character is mapped to frequencies based on its type:

- **Vowels** (A, E, I, O, U): Higher frequencies (528-1175 Hz), 3-note chords
- **Consonants**: Medium frequencies (352-616 Hz), 2-note chords
- **Punctuation**: Lower frequencies (220 Hz), 1-note tones
- **Spaces**: Silence (150-200 ms between words)

Example: "Hi"
- H → [330, 440] Hz for ~80 ms
- I → [528, 660, 823] Hz for ~120 ms
- Total duration: ~200 ms of musical tones

### Audio Effects

1. **ADSR Envelope**: Attack → Decay → Sustain → Release
2. **Vibrato**: Frequency modulation (5-8 Hz rate)
3. **Harmonics**: Natural overtones for musicality
4. **Emotion Modulation**: Frequency shift based on emotional state

---

## 🧠 Personality & Emotions

Rocky responds with emotional inflection:

- **Curious** 😲: Higher pitch, faster vibrato
- **Confused** 🤔: Lower pitch, slower vibrato
- **Excited** 🎉: Much higher pitch, deep modulation
- **Concerned** 😟: Low pitch, minimal modulation
- **Neutral** 😐: Standard pitch and modulation

Example emotions trigger words:
- Curious: "how", "why", "fascinating", "understand"
- Confused: "human", "emotion", "culture", "why"
- Excited: "discovery", "success", "engineering", "technical"
- Concerned: "problem", "danger", "risk", "fail"

---

## 🔧 Troubleshooting

### No audio output
- Check speakers/headphones are connected and powered
- Verify audio device: `python -c "import sounddevice; sounddevice.query_devices()"`

### Ollama connection failed
- Ensure Ollama is running: `ollama serve` in terminal
- Check host address in `.env` (default: http://localhost:11434)
- Verify model is downloaded: `ollama list`

### Whisper model not loading
- First run downloads the model (~140 MB for 'base')
- Ensure internet connection for download
- Can manually download: `python -c "from faster_whisper import WhisperModel; WhisperModel('base')"`

### Microphone not working
- Check microphone permissions
- List devices: `python -c "import sounddevice; sounddevice.query_devices()"`
- Try different device ID in code if needed

### Slow response times
- First-run loads models (Whisper + LLM)
- Subsequent runs are faster
- Use smaller Whisper model: `WHISPER_MODEL=tiny` in `.env`

---

## 📚 Code Examples

### Using Rocky Programmatically

```python
from app.pipeline import get_assistant

# Get assistant instance
assistant = get_assistant()

# Process a message
user_input = "What is physics?"
response = assistant.think(user_input)
print(f"Rocky: {response}")

# Convert to tones and play
assistant.speak(response)
```

### Direct Tone Generation

```python
from app.rocky_voice import ChordMapper, get_synthesizer

mapper = ChordMapper()
synth = get_synthesizer()

# Text to chords
text = "Hello alien"
chords = mapper.text_to_chords(text)

# Generate waveform
waveform = synth.generate_from_chords(chords)

# Play (requires audio output initialization)
```

---

## 🎨 Customization

### Change Rocky's Personality

Edit `app/brain/prompts.py`:

```python
SYSTEM_PROMPT = """You are Rocky, an alien...
[Customize personality here]
"""
```

### Modify Tone Characteristics

Edit `app/config.py`:

```python
TONE_PITCH_BASE = 440  # Base frequency
VIBRATO_RATE = 5  # Hz
VIBRATO_DEPTH = 20  # Hz
RANDOMNESS_FACTOR = 0.1  # Variation (0-1)
```

### Add New Emotions

Edit `app/rocky_voice/emotions.py`:

Add to `EMOTION_PROMPTS` and `EmotionAnalyzer.get_tone_parameters()`.

---

## 📊 Performance Notes

- **Response time**: 2-10 seconds (depends on LLM model)
- **Audio generation**: <1 second for typical response
- **Memory usage**: ~500-800 MB (LLM dependent)
- **Latency**: Optimized with local processing (no network delays)

---

## 🔐 Privacy

✅ **Fully Local**: All processing happens on your machine
- ✅ No cloud APIs
- ✅ No data transmission
- ✅ No tracking
- ✅ Ollama runs locally
- ✅ Whisper runs locally

---

## 🤝 Contributing

Contributions welcome! Areas for enhancement:

- Additional emotion states
- More sophisticated tone variations
- Music composition algorithms
- Integration with other local LLMs
- Web interface
- Visualization of tone patterns

---

## 📄 License

This project is inspired by *Project Hail Mary* by Andy Weir. Created for educational and entertainment purposes.

---

## 🎯 Future Ideas

- **Multi-language support**: Different tone mappings for other languages
- **Real-time tone visualization**: Spectrograms and waveform display
- **Conversation memory**: Extended context tracking
- **Tone recording**: Save alien conversations to audio files
- **Music composition**: Generate complete "songs" from conversations
- **API mode**: Serve as audio API for other applications

---

## 📞 Support

For issues or questions:

1. Check the **Troubleshooting** section above
2. Verify all prerequisites are installed
3. Enable debug mode: `python app/main.py --debug`
4. Check logs in `logs/` directory

---

**🎵 Enjoy communicating with Rocky! 🎵**

*"Your music... it uses harmonic frequencies. Why this pattern?"*
