# ARCHITECTURE - Rocky Assistant

Technical architecture and design documentation for the Rocky Assistant system.

---

## 🏗️ System Overview

Rocky Assistant is a modular Python application that simulates alien communication through musical tones. The system processes human speech, generates intelligent responses, and outputs unique audio signatures based on emotional context.

### Data Flow

```
User Speech (Audio)
    ↓
[Audio Input]
    ↓
[Speech Recognition] (Whisper) → Text
    ↓
[LLM] (Ollama) → Response Text
    ↓
[Emotion Analysis]
    ↓
[Text → Chords Mapper]
    ↓
[Synthesizer] → Waveform
    ↓
[Effects] (ADSR, Vibrato)
    ↓
[Audio Output]
    ↓
Speaker/Headphones
```

---

## 📁 Module Architecture

### 1. Configuration Layer (`config.py`)

**Purpose:** Centralized configuration management

**Responsibilities:**
- Load environment variables
- Define audio parameters
- Set LLM model configuration
- Configure UI/UX settings
- Manage logging levels

**Key Exports:**
- `SAMPLE_RATE`: 22050 Hz
- `OLLAMA_MODEL`: LLM to use
- `TONE_PITCH_BASE`: Base frequency (440 Hz)
- `ENVELOPE_*`: ADSR timing

---

### 2. Logging Utility (`app/utils/logger.py`)

**Purpose:** Consistent logging across all modules

**Features:**
- Console and file output
- Configurable log levels
- Timestamped logs
- Thread-safe operations

**Usage:**
```python
from app.utils import logger
logger.info("Starting process...")
logger.debug("Debug information")
logger.error("An error occurred")
```

---

### 3. Brain Module (`app/brain/`)

#### `llm.py` - Local LLM Interface

**Purpose:** Communication with local Ollama server

**Class:** `OllamaLLM`
- Connects to Ollama HTTP API
- Sends prompts with context
- Manages conversation history
- Handles timeouts and errors

**Key Methods:**
- `generate(prompt, context, temperature)` → response text
- `get_model_info()` → model metadata
- `_verify_connection()` → health check

**Error Handling:**
- Connection failures → raises RuntimeError
- Timeouts → returns error message
- JSON parsing errors → logs and returns placeholder

#### `prompts.py` - Rocky Personality

**Purpose:** Define Rocky's communication patterns

**Exports:**
- `SYSTEM_PROMPT`: Core personality definition
- `CONVERSATION_STARTERS`: Opening messages
- `EMOTION_PROMPTS`: Emotion-specific modifiers
- `get_system_prompt()` → system prompt
- `get_emotion_prompt(emotion)` → emotion modifier

**Rocky's Characteristics:**
- Curious and logical
- Engineering-focused
- Confused by human emotions
- Direct communication style

---

### 4. Audio Input Module (`app/audio/input.py`)

#### `AudioInput` Class

**Purpose:** Microphone recording

**Methods:**
- `record(duration)` → numpy array
- `detect_speech_end(timeout)` → audio until silence detected

**Features:**
- Silence detection (energy threshold)
- Automatic speech stopping

#### `SpeechRecognition` Class

**Purpose:** Audio → Text conversion

**Backends:**
- `faster-whisper` (default): CPU-optimized
- `whisper` (fallback): OpenAI's model

**Methods:**
- `transcribe(audio)` → text
- Supports multiple languages
- English optimized by default

---

### 5. Audio Output Module (`app/audio/output.py`)

#### `AudioOutput` Class

**Purpose:** Waveform playback

**Methods:**
- `play(audio_data, blocking, volume)` → None
- `stop()` → stops playback
- `list_devices()` → prints available devices

**Features:**
- Volume control (0.0 to 1.0)
- Automatic clipping prevention
- Blocking or non-blocking modes

---

### 6. Audio Effects Module (`app/audio/effects.py`)

#### `ADSREnvelope` Class

**Purpose:** Amplitude modulation over time

**Parameters:**
- Attack: 0 → 1 (e.g., 50ms)
- Decay: 1 → sustain_level (e.g., 100ms)
- Sustain: constant level (e.g., 300ms)
- Release: sustain_level → 0 (e.g., 100ms)

**Effect:**
```
Amplitude │     ╱╲
          │    ╱  ╲___╲
          │   ╱       ╲
          └─────────────► Time
            A D  S   R
```

#### `Vibrato` Class

**Purpose:** Frequency modulation (LFO)

**Parameters:**
- Rate: 4-8 Hz typical
- Depth: 10-30 Hz typical

**Effect:** Periodic pitch variation

#### `ToneEffects` Class

**Purpose:** Combined effects processing

**Methods:**
- `add_harmonics(samples)` → harmonic overtones
- `apply_all(samples, base_freq)` → complete processing

---

### 7. Rocky Voice Module (`app/rocky_voice/`)

#### `mapper.py` - Text to Chord Mapping

**Purpose:** Convert text characters to musical frequencies

**Mapping Strategy:**

| Character Type | Frequency Range | Notes | Chord Size |
|---|---|---|---|
| Vowels (A, E, I, O, U) | 528-1175 Hz | Higher, resonant | 3 notes |
| Consonants | 352-616 Hz | Medium | 2 notes |
| Punctuation | 220 Hz | Lower | 1 note |
| Numbers | 352-990 Hz | Based on digit | 2 notes |
| Spaces | Silence | 150-200ms | N/A |

**Example Conversion:**
```
Text: "Hi"
H → [330, 440, 550] Hz for ~80ms
i → [528, 660, 823] Hz for ~120ms
Space → Silence 150ms
Result → ~350ms of tones
```

**Class:** `ChordMapper`
- `_build_frequency_map()` → deterministic mappings
- `_generate_chord(base_freq)` → chord around base
- `text_to_chords(text)` → [(frequencies, duration), ...]
- `get_chord_for_emotion(emotion, chord)` → modulated chord

#### `synthesizer.py` - Waveform Generation

**Purpose:** Convert frequency specifications to audio

**Class:** `ToneSynthesizer`

**Methods:**
- `generate_sine_wave(freq, duration)` → single sine
- `generate_chord(frequencies, duration)` → mixed waveform
- `generate_from_chords(chords)` → complete audio
- `apply_fade(waveform)` → fade in/out

**Synthesis Process:**
1. Generate individual sine waves for each frequency
2. Mix (average) together
3. Normalize to prevent clipping
4. Apply fade-in/fade-out
5. Return normalized float32 array

#### `emotions.py` - Emotion Analysis & Modulation

**Purpose:** Context-aware tone variation

**Class:** `Emotion` (Enum)
- `NEUTRAL`, `CURIOUS`, `CONFUSED`, `EXCITED`, `CONCERNED`

**Class:** `EmotionAnalyzer`

**Methods:**
- `analyze(text)` → Emotion based on keywords
- `get_tone_parameters(emotion)` → modulation params

**Emotion Parameters:**

| Emotion | Freq Shift | Vibrato Rate | Vibrato Depth | Sustain Level |
|---|---|---|---|---|
| CURIOUS | 1.05x | 6 Hz | 25 Hz | 0.85 |
| CONFUSED | 0.98x | 4 Hz | 15 Hz | 0.70 |
| EXCITED | 1.15x | 8 Hz | 35 Hz | 0.90 |
| CONCERNED | 0.92x | 3 Hz | 10 Hz | 0.65 |
| NEUTRAL | 1.00x | 5 Hz | 20 Hz | 0.80 |

**Trigger Words:**
- Curious: "how", "why", "fascinating"
- Confused: "emotion", "culture", "why"
- Excited: "discovery", "technical", "breakthrough"
- Concerned: "problem", "danger", "issue"

---

### 8. Pipeline Module (`app/pipeline/assistant.py`)

#### `RockyAssistant` Class

**Purpose:** Main orchestrator coordinating all components

**Initialization:**
- Instantiates all subsystems
- Verifies Ollama connection
- Initializes audio devices
- Sets up singleton instances

**Main Methods:**

1. **`listen(timeout)`** → text
   - Records from microphone
   - Detects speech end
   - Transcribes to text

2. **`think(user_input)`** → response text
   - Builds conversation context
   - Sends to LLM
   - Returns Rocky's response

3. **`speak(text)`** → None
   - Analyzes emotion
   - Maps text to chords
   - Applies emotion modulation
   - Generates waveform
   - Applies effects
   - Plays audio

4. **`run(test_input)`** → None
   - Main interactive loop
   - Gets user input (text or test)
   - Processes through pipeline
   - Handles errors gracefully

**Conversation Loop:**
```python
while running:
    user_input = listen() or input()
    response = think(user_input)
    speak(response)
    save_to_history()
```

---

## 🔄 Processing Pipeline Details

### 1. Input Processing

**Speech Input:**
```
Microphone → Sounddevice → NumPy Array → Whisper → Text
```

**Text Input:**
```
Stdin → String → (skip speech recognition)
```

### 2. LLM Processing

**Prompt Construction:**
```python
full_prompt = f"""
{SYSTEM_PROMPT}

Context: {recent_conversation_history}

User: {user_input}
Rocky:
"""
```

**API Call:**
```python
response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": model_name,
        "prompt": full_prompt,
        "temperature": 0.7
    }
)
```

### 3. Tone Generation

**Phase 1: Text Analysis**
- Analyze response for emotion
- Calculate tone parameters

**Phase 2: Mapping**
- Convert each character to chord
- Handle punctuation and spaces

**Phase 3: Synthesis**
- Create sine waves for each frequency
- Mix frequencies together
- Normalize amplitude

**Phase 4: Effects**
- Apply ADSR envelope
- Add vibrato modulation
- Optionally add harmonics

**Phase 5: Output**
- Apply fade in/out
- Verify audio levels
- Send to speakers

---

## 🔌 External Dependencies

### Core Dependencies

| Package | Version | Purpose |
|---|---|---|
| numpy | >=1.21.0 | Numerical computation |
| sounddevice | >=0.4.5 | Audio I/O |
| faster-whisper | >=0.9.0 | Speech recognition |
| requests | >=2.27.0 | HTTP client |
| python-dotenv | >=0.19.0 | Environment config |

### Optional Dependencies

| Package | Purpose |
|---|---|
| pytest | Testing framework |
| black | Code formatting |
| pylint | Linting |

### External Services

1. **Ollama** (Local HTTP API)
   - Runs on port 11434
   - Provides LLM inference
   - Fully local (no internet required)

2. **System Audio Devices**
   - Microphone (input)
   - Speakers/Headphones (output)

---

## 🧵 Threading & Async

**Current Implementation:** Blocking (synchronous)

**Potential Improvements:**
- Async LLM requests (long timeout)
- Background audio playback
- Real-time waveform visualization
- Concurrent recording & synthesis

---

## 📊 Performance Characteristics

### Latency Profile

| Operation | Time | Notes |
|---|---|---|
| Model load (first run) | 1-5s | Ollama cache |
| LLM inference | 2-10s | Model dependent |
| Whisper transcription | 5-15s | Audio length dependent |
| Chord generation | <100ms | Deterministic |
| Synthesis | <500ms | Waveform length dependent |
| Total E2E | 10-30s | First response slower |

### Memory Profile

| Component | Memory | Notes |
|---|---|---|
| Ollama model | 3-8 GB | Shared (server process) |
| Whisper model | 400-900 MB | First load to disk cache |
| Application | 50-150 MB | Python runtime + data |
| Audio buffer | 1-5 MB | Per chunk |

### Scalability Notes

- Single-user synchronous application
- Not designed for concurrent users
- Can be extended to queue-based system
- REST API wrapper possible for multi-client

---

## 🛡️ Error Handling Strategy

### Error Layers

1. **Connection Errors**
   - Ollama unreachable → RuntimeError on init
   - Audio device unavailable → RuntimeError on init

2. **Operation Errors**
   - Whisper transcription fails → return empty string
   - LLM timeout → return error message
   - Audio synthesis fails → logged, continue

3. **Recovery**
   - Graceful degradation
   - User notification
   - Detailed logging
   - Automatic retry on some operations

---

## 🔐 Security Considerations

### Data Privacy

✅ **No data collection**
- All processing local
- No remote logging
- No analytics
- No tracking

### Potential Attack Vectors

- Arbitrary code execution via LLM (mitigated: local only)
- Malicious audio input (handled gracefully)
- Resource exhaustion (mitigated: timeouts)

### Recommendations

- Validate audio paths
- Monitor resource usage
- Use principle of least privilege
- Regular dependency updates

---

## 🚀 Optimization Opportunities

### Short Term

1. **Model Caching**
   - Pre-load models at startup
   - Reduce first-response latency

2. **Waveform Optimization**
   - Use scipy.signal for faster synthesis
   - Vectorize operations

3. **Memory Management**
   - Clear old conversation history
   - Stream large audio instead of buffering

### Medium Term

1. **Async Processing**
   - Non-blocking LLM calls
   - Parallel synthesis & playback
   - Real-time visualization

2. **Advanced Effects**
   - More sophisticated emotion modulation
   - Frequency analysis feedback
   - Dynamic chord selection

### Long Term

1. **Machine Learning**
   - Learn emotion from conversation patterns
   - User-specific tone adjustments
   - Generative music sequences

2. **Multi-Modal**
   - Text visualization
   - Waveform animation
   - Web interface

---

## 📈 Monitoring & Debugging

### Debug Logging

```python
# Enable in .env
DEBUG_MODE=true
LOG_LEVEL=DEBUG
```

### Performance Profiling

```bash
python -m cProfile -s cumulative app/main.py
```

### Audio Analysis

```python
import numpy as np
import matplotlib.pyplot as plt

waveform = synth.generate_from_chords(chords)
plt.plot(waveform)
plt.specgram(waveform, Fs=22050)
plt.show()
```

---

## 🧪 Testing Architecture

### Test Pyramid

```
    △
   ╱ ╲  Integration Tests (5)
  ╱   ╲
 ╱─────╲
╱       ╲ Unit Tests (25)
╱─────────╲ Component Tests (10)
```

### Test Categories

1. **Unit Tests** (`test_*.py`)
   - Individual class methods
   - Isolated functionality
   - Mock external dependencies

2. **Component Tests**
   - Function combinations
   - Local integrations
   - No network calls

3. **Integration Tests**
   - Full pipeline (requires Ollama)
   - End-to-end flows
   - With real models

---

**Architecture Version:** 1.0  
**Last Updated:** 2024-03-27  
**Status:** Production Ready
