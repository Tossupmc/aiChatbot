from pathlib import Path
from openai import OpenAI as ai
from pydub import AudioSegment
from pydub.playback import play
import pyaudio
import wave
import keyboard
import time

__role = "aiExpert with a hard limit of 32 word"
dialog = [{"role": "system", "content": __role}]

def record_audio(
        file_path, sample_rate=44100, format=pyaudio.paInt16
    ) -> None:

    chunk_size = 1024
    audio_init = pyaudio.PyAudio()
    n_channels = 2
    samp_width = audio_init.get_sample_size(format)

    try:
        stream = audio_init.open(
            format=format, channels=n_channels, rate=sample_rate,
            input=True, frames_per_buffer=chunk_size
            )

        print("Hold SHIFT key to record!", end="\r")
        keyboard.wait("shift")
        print("                         ", end="\r")

        audio_frame = []

        timer = time.time()
        while keyboard.is_pressed("shift"):
            data = stream.read(chunk_size)
            audio_frame.append(data)
            print(f"Recording {(time.time() - timer):0.2f}s", end="\r", flush=True)
        print(f"Recording for {(time.time() - timer):0.2f}s", end="\n", flush=True)

    finally:
        stream.stop_stream()
        stream.close()
        audio_init.terminate()

    with wave.open(file_path, 'wb') as wa:
        wa.setnchannels(n_channels)
        wa.setsampwidth(samp_width)
        wa.setframerate(sample_rate)
        wa.writeframes(b''.join(audio_frame))

def mp3_to_text(file_name) -> str:
    return ai().audio.transcriptions.create(
        model="whisper-1",
        file=open(file_name, "rb")
    ).text


def generate_respond(prompt) -> str:
    dialog.append({"role": "user", "content": prompt})
    response = ai().chat.completions.create(
        model="gpt-3.5-turbo-1106",
        # stream=True,
        messages=dialog,
        temperature=0.5,
        max_tokens=1024,
    ).choices[0].message.content
    dialog.append({"role": "assistant", "content": response})
    return response

def text_to_mp3(respond, file_name) -> None:
    speech_file_path = Path(__file__).parent / file_name
    with ai().audio.speech.with_streaming_response.create(
        model="tts-1",
        voice="alloy",
        input=respond
    ) as response:
        response.stream_to_file(speech_file_path)

def play_sound_file(file_name) -> None:
    song = AudioSegment.from_file(file_name)
    play(song)

def main_function() -> None:
    while True:
        file_name = "aiAudio.mp3"
        record_audio(file_name)

        transcription = mp3_to_text(file_name)

        if transcription[:4] == "Exit":
            break

        print(f"Q: {transcription}", end="\n")
        respond = generate_respond(transcription)
        print(f"A: {respond}", end="\n")
        
        text_to_mp3(respond, file_name)
        play_sound_file(file_name)

if __name__ == "__main__":
    main_function()