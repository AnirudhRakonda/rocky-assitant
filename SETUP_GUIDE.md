# SETUP GUIDE - Rocky Assistant

Complete step-by-step setup instructions for different operating systems.

---

## 🖥️ System Requirements

- **OS**: macOS, Linux, or Windows 10/11
- **Python**: 3.8 or higher
- **RAM**: 4 GB minimum (8 GB recommended)
- **Storage**: 3-5 GB free space (for LLM models)
- **Audio**: Microphone and speakers/headphones
- **Internet**: For initial model downloads only

---

## 📦 Installation Steps

### Step 1: Install Ollama (Local LLM Server)

#### macOS
```bash
# Download and install from:
# https://ollama.ai/download/mac

# Or use brew
brew install ollama

# Start Ollama server
ollama serve
```

The server will start at `http://localhost:11434`

#### Linux
```bash
# Install Ollama
curl https://ollama.ai/install.sh | sh

# Start the service
systemctl start ollama

# Or run directly
ollama serve
```

#### Windows
```bash
# Download installer from:
# https://ollama.ai/download/windows

# Install and run the GUI application
# Server will auto-start in background
```

### Step 2: Download a Model

In a new terminal (while Ollama server is running):

```bash
# Recommended: Mistral (fast, good quality)
ollama pull mistral

# Or: Llama 3 (better quality, slower)
ollama pull llama3

# Or: Neural Chat (fastest)
ollama pull neural-chat

# Verify model is downloaded
ollama list
```

First download may take 5-15 minutes depending on internet speed.

### Step 3: Install Python Dependencies

#### Create Virtual Environment (Recommended)

**macOS/Linux:**
```bash
cd rocky-assistant
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
cd rocky-assistant
python -m venv venv
venv\Scripts\activate
```

#### Install Requirements

```bash
# Upgrade pip first
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# This installs:
# - numpy (numerical computation)
# - sounddevice (audio I/O)
# - python-dotenv (environment config)
# - requests (HTTP client)
# - faster-whisper (speech recognition)
# - pytest (for testing)
```

On macOS, you might need to install portaudio first:
```bash
brew install portaudio
```

### Step 4: Configure Environment

```bash
# Copy example config
cp .env.example .env

# Edit .env if needed (most defaults should work)
# nano .env
# or
# code .env
```

Default `.env` settings:
```env
OLLAMA_MODEL=mistral
OLLAMA_HOST=http://localhost:11434
WHISPER_MODEL=base
LOG_LEVEL=INFO
DEBUG_MODE=false
```

### Step 5: Verify Installation

```bash
# Check Python installation
python --version

# Check Ollama connection (Ollama server must be running)
python -c "
from app.brain import get_llm
try:
    llm = get_llm()
    print('✓ Ollama connected successfully')
except Exception as e:
    print(f'✗ Error: {e}')
"

# Test audio devices
python -c "
import sounddevice as sd
print('Available audio devices:')
sd.query_devices()
"

# Run test suite
pytest tests/ -v
```

---

## 🚀 Running Rocky Assistant

### Prerequisites Checklist

- [ ] Ollama installed
- [ ] Model downloaded (`ollama list`)
- [ ] Python 3.8+ installed
- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] .env configured
- [ ] Microphone and speakers connected

### Starting the Application

**Terminal 1: Start Ollama Server**
```bash
ollama serve
```

You'll see:
```
2024/03/27 10:15:30 "GET /api/tags HTTP/1.1" 200 256
```

**Terminal 2: Start Rocky**
```bash
# Activate virtual environment first (if using one)
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Run Rocky
python app/main.py
```

You'll see:
```
============================================================
🎵 ROCKY ASSISTANT - ALIEN COMMUNICATION SYSTEM 🎵
============================================================

Rocky is listening... (Use non-interactive mode for speech input)

Enter messages (or 'quit' to exit):

You: 
```

### Interactive Mode

Enter text and press Enter:
```
You: What is your name?

Rocky: I am Rocky. My designation is explorer probe from Project Hail Mary.

[🎵 Musical alien tones play 🎵]

You: 
```

Type `quit` to exit.

### Test Mode (Without Ollama)

Test tone generation without LLM:
```bash
python app/main.py --test "Hello Rocky"
```

### Debug Mode

Enable detailed logging:
```bash
python app/main.py --debug
```

Logs are saved to `logs/` directory.

---

## 🎵 Running Examples

Try the example scripts without speech input:

```bash
# Interactive examples
python example_usage.py

# Or test individual components
python -c "
from app.rocky_voice import ChordMapper
mapper = ChordMapper()
chords = mapper.text_to_chords('Hi')
print(f'Chords generated: {len(chords)}')
"
```

---

## 🧪 Testing

Run the test suite to verify everything works:

```bash
# All tests
pytest tests/ -v

# Specific test file
pytest tests/test_rocky.py -v

# Specific test
pytest tests/test_rocky.py::TestChordMapper::test_text_to_chords -v

# With coverage report
pytest tests/ --cov=app --cov-report=html
```

---

## 📝 Configuration Guide

### Choosing Models

**For Speed (Recommended for first run):**
```bash
ollama pull neural-chat
# Edit .env:
# OLLAMA_MODEL=neural-chat
# WHISPER_MODEL=tiny
```

**For Quality:**
```bash
ollama pull mistral
# Edit .env:
# OLLAMA_MODEL=mistral
# WHISPER_MODEL=base
```

**For Best Quality (Slower):**
```bash
ollama pull llama3
# Edit .env:
# OLLAMA_MODEL=llama3
# WHISPER_MODEL=small
```

### Audio Configuration

Adjust audio settings in `app/config.py`:

```python
SAMPLE_RATE = 22050  # Hz (22.05 kHz)
AUDIO_DURATION_DEFAULT = 0.15  # seconds per tone
TONE_PITCH_BASE = 440  # Hz (A4 note)
VIBRATO_RATE = 5  # Hz (modulation speed)
VIBRATO_DEPTH = 20  # Hz (modulation amount)
```

### Rocky Personality

Customize Rocky's responses in `app/brain/prompts.py`:
- Modify `SYSTEM_PROMPT`
- Add/edit `CONVERSATION_STARTERS`
- Adjust `EMOTION_PROMPTS`

---

## ❌ Troubleshooting

### Ollama Connection Failed

**Error:** "Cannot connect to Ollama at http://localhost:11434"

**Solution:**
1. Is Ollama running? Check Terminal 1: `ollama serve`
2. Try restart: `killall ollama` then `ollama serve`
3. Verify port: `lsof -i :11434` (macOS/Linux)
4. Change host in `.env` if using different port
5. Check firewall settings

### Model Not Found

**Error:** "Connection refused" or "Model not found"

**Solution:**
```bash
# Check downloaded models
ollama list

# Download missing model
ollama pull mistral

# Verify download completed
ollama list
```

### No Audio Input/Output

**Error:** "No audio device found" or "Recording failed"

**Solution:**
```bash
# List available devices
python -c "import sounddevice as sd; print(sd.query_devices())"

# Check microphone permissions (macOS)
# System Preferences → Security & Privacy → Microphone

# Try specifying device in code or reinstall sounddevice:
pip install --force-reinstall sounddevice
```

### Whisper Model Download Stuck

**Error:** Taking very long to download (~4 GB)

**Solution:**
```bash
# Cancel (Ctrl+C) and try smaller model
# Edit .env:
WHISPER_MODEL=tiny  # Only ~40 MB

# Or download separately
python -c "from faster_whisper import WhisperModel; WhisperModel('tiny')"
```

### Memory Issues

**Error:** "Out of memory" or very slow response

**Solution:**
1. Use smaller LLM model: `ollama pull neural-chat`
2. Use smaller Whisper model: `WHISPER_MODEL=tiny`
3. Close other applications
4. Check available RAM: `free -h` (Linux) or `top` (macOS)

### Very Slow Response Times

**Normal behavior:**
- First run: 5-10 seconds (model loading)
- Subsequent runs: 2-5 seconds

**To speed up:**
1. Use faster model: `OLLAMA_MODEL=neural-chat`
2. Use CPU offloading in Ollama (if GPU available)
3. Wait for model to cache in memory

---

## 🔧 Manual Testing

### Test Ollama Connection
```python
python -c "
import requests
ollama_host = 'http://localhost:11434'
try:
    r = requests.get(f'{ollama_host}/api/tags', timeout=5)
    print('✓ Ollama connected')
    print('Models:', r.json())
except:
    print('✗ Ollama not responding')
"
```

### Test Audio Devices
```python
import sounddevice as sd
print(sd.query_devices())
# Look for input (Microphone) and output (Speakers)
```

### Test Tone Generation
```python
python -c "
from app.rocky_voice import ChordMapper, get_synthesizer
mapper = ChordMapper()
synth = get_synthesizer()
chords = mapper.text_to_chords('Test message')
waveform = synth.generate_from_chords(chords)
print(f'Generated {len(waveform)} audio samples')
print(f'Duration: {len(waveform)/22050:.2f} seconds')
"
```

---

## 🐳 Docker Setup (Optional)

For isolated environment:

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app/main.py"]
```

Build and run:
```bash
docker build -t rocky-assistant .
docker run -it --network host rocky-assistant
```

---

## 🔄 Updating/Reinstalling

### Update Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Fresh Start
```bash
# Deactivate virtual environment if active
deactivate

# Remove old environment
rm -rf venv

# Create new environment
python3 -m venv venv
source venv/bin/activate

# Install fresh
pip install -r requirements.txt

# Run again
python app/main.py
```

### Clear Cache
```bash
# Pre-trained models cache
rm -rf ~/.cache/whisper/*

# Python cache
find . -type d -name __pycache__ -exec rm -rf {} +
find . -name "*.pyc" -delete
```

---

## ✅ First Run Summary

```bash
# 1. Terminal 1: Start Ollama
ollama serve

# 2. Terminal 2: Setup and run Rocky
cd rocky-assistant
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app/main.py

# 3. Type your first message
You: Hello Rocky!
```

---

## 📞 Getting Help

1. Check **Troubleshooting** section above
2. Review logs: `cat logs/$(date +%Y%m%d)_rocky.log`
3. Enable debug: `python app/main.py --debug`
4. Test components individually (see Manual Testing)
5. Verify prerequisites are met

---

**Happy communicating with Rocky! 🎵**
