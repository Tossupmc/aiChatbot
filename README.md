# Voice-Controlled Conversational Interface

This Python script implements a voice-controlled conversational interface by combining audio recording, text-to-speech, and OpenAI's GPT-3.5 Turbo. Users can interact with the AI by speaking into the microphone, and the AI responds with synthesized audio.

## Features

- Records user input as an MP3 file
- Transcribes MP3 to text using OpenAI's API
- Generates AI responses with GPT-3.5 Turbo
- Converts text responses to MP3 using OpenAI's TTS API
- Plays synthesized audio in real-time

## Requirements

- Python 3.x
- Required packages:
    - `pathlib`
    - `openai`
    - `pydub`
    - `pyaudio`
    - `wave`
    - `keyboard`
    - `time`

## Setup

1. Add your OpenAI API key as an environment variable named `OPENAI_API_KEY`.
2. Run the script: `python aiChatbot.py`

## Usage

- Press and hold the `Shift` key to start recording audio.
- To exit the program, say the word `Exit` as the first word during a conversation.

## Configuration

- Adjust settings in the script, such as audio parameters, OpenAI models, and conversation roles.

## License

This project is licensed under the [MIT License](https://en.wikipedia.org/wiki/MIT_License).

## Acknowledgments

- Special thanks to [OpenAI](https://openai.com) for providing powerful language models.