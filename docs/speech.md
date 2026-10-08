# Speech and Audio Interaction Module

This document details the core speech generation, speech recognition, and interactive querying components of the "One" project, as implemented in `speech.py`. 

## Text-to-Speech Generation and Feedback

The `speech` function handles vocal feedback by converting text responses into spoken English audio. It utilizes the `gTTS` (Google Text-to-Speech) library to synthesize the provided string into an MP3 file. Once generated, the audio file is played back asynchronously using `ffplay` with silenced standard output and error streams to keep the terminal clean and non-intrusive. 

To ensure proper resource management and prevent leftover clutter, the function automatically cleans up by deleting the temporary `speech.mp3` file from disk immediately after playback finishes. A brief pause of 400 milliseconds is introduced at the end of execution to prevent audio clipping or overlapping with subsequent system actions.

## Audio Transcription and Keyword Guidance

Audio chunks captured by the system are converted into text through `transcribe_audio`, powered by the `faster_whisper` model running locally on the CPU with INT8 quantization for optimal performance. The transcription pipeline is heavily optimized for command execution accuracy by passing a custom `initial_prompt` containing domain-specific keywords (such as commands for closing, searching, starting, and managing tasks). 

Parameters such as a fixed English language constraint, beam search size of 5, and an integrated Voice Activity Detection (VAD) filter ensure that background noise is suppressed and speech segments are accurately isolated. The resulting transcription is passed through a companion `clean_text` utility that strips all punctuation, converts characters to lowercase, and trims whitespaces to standardize the command string before it is processed by the rest of the application.

## Interactive Querying and Context Management

The module coordinates interactive dialogue loops using the `ask_user` function alongside the `limited_hear` context manager. When the system needs to prompt the user for input, `ask_user` first invokes the `speech` function to voice the question. 

To isolate this conversational exchange from background listening routines, `limited_hear` acts as a context manager that flushes any stale data from the global state queue (`state.q`) and temporarily overrides processing flags (`state.is_processing = False`). Inside this guarded block, the system enters a polling loop that listens specifically for the user's response chunk, transcribes it through the Whisper pipeline, and returns the cleaned text as soon as a valid utterance is captured.