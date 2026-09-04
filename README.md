# One
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![Status](https://img.shields.io/badge/status-active-success)

One is a Python-based project designed to act as a voice assistant capable of understanding and executing commands such as opening the browser or terminal, adjusting the volume, and various other tasks. The goal is to provide a lightweight assistant that runs in the background, waiting for commands—potentially eliminating the need to download resource-heavy AI systems for simple tasks.

## System Architecture

The system operates using the **Producer-Consumer** pattern, ensuring the application's main loop never freezes during audio capture and processing:

* **Producer (Capture & VAD):** An audio callback runs in the background, analyzing 30ms chunks (480 samples at 16kHz). A state machine tracks the duration of silence. Once a phrase is complete (e.g., 450ms of continuous silence), the audio segments are merged.
* **Safe Buffer (Queue):** The consolidated audio is packaged and sent to a `queue.Queue()`, ensuring secure transfer from the capture thread to the main thread.
* **Consumer (Transcription):** The main loop consumes packets from the queue and triggers the Faster Whisper model (CPU-optimized with `compute_type="int8"`) to generate clean text.
* **Action Executor:** The formatted text is passed to the `Actions` class, which interprets and executes the corresponding system command.

## What works today?

* Command to play a specific song by saying: "play (music name)", (I will add an explanation of how to do this in the future.)
* Commands to open Firefox and Kitty (if yours are different, you can specify the browser and terminal you use simply by changing the names in the respective functions).
* Player control commands, such as: increase volume, decrease volume, pause music, start music, and next track.
* The ability to update the system via voice commands is configured for Arch-based Linux distributions, but you can also modify it to suit your specific distribution.

## Possible future implementations

* Search for something on Google.
* Search for videos on YouTube.
* Search for something on Google and/or an AI (like Gemini).
* The assistant responds to commands, something like: "OK! Opening Firefox".
* An interface.
* The ability to execute commands on another computer of yours. For example, you leave One running on one PC, and when you issue a command, it sends it to your other PC.

##  Installation and Configuration

### Prerequisites
* **Python 3.8+**
* System dependencies for audio hardware (e.g., `portaudio19-dev` on Linux).

### Step-by-Step

1. Clone the repository:
```
git clone https://github.com/alanmachadozx/One.git
cd One
```
2. Create and activate a virtual environment (recommended):
```
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```  
3. Install the listed dependencies:
```
pip install -r requirements.txt
```
