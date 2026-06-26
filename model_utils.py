
import os
import subprocess
import soundfile as sf
import numpy as np
from faster_whisper import WhisperModel

def convert_to_wav(input_path, output_path, ffmpeg_path):
    subprocess.run([
        ffmpeg_path, "-i", input_path,
        "-ar", "16000", "-ac", "1", output_path, "-y"
    ], check=True)

def transcribe_audio(model, audio_path, chunk_size_sec=5):
    audio, sample_rate = sf.read(audio_path, dtype="float32")
    chunk_samples = int(chunk_size_sec * sample_rate)
    total_chunks = (audio.shape[0] + chunk_samples - 1) // chunk_samples

    full_transcript = []
    for chunk_index in range(total_chunks):
        start_sample = chunk_index * chunk_samples
        end_sample = min(start_sample + chunk_samples, audio.shape[0])
        chunk = audio[start_sample:end_sample]
        if len(chunk) < 100:


    model = WhisperModel("tiny", compute_type="int8", device="cpu", cpu_threads=1)
    transcript = transcribe_audio(model, output_path)
    return transcript
