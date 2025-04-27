
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
            continue
        if np.max(np.abs(chunk)) > 0:
            chunk = chunk / np.max(np.abs(chunk))

        temp_chunk_path = f"temp_chunk_{chunk_index}.wav"
        sf.write(temp_chunk_path, chunk, sample_rate)

        segments, _ = model.transcribe(
            temp_chunk_path, language="en", beam_size=1,
            no_speech_threshold=0.5, condition_on_previous_text=False
        )
        segment_list = list(segments)
        if segment_list:
            chunk_text = " ".join([segment.text.strip() for segment in segment_list])
            full_transcript.append(chunk_text)

        os.remove(temp_chunk_path)

    return " ".join(full_transcript)

def process_audio_file(input_path):
    ffmpeg_path = "D:/ffmpeg/bin/ffmpeg.exe"  # <-- Change if needed
    if not input_path.endswith(".wav"):
        output_path = input_path.rsplit('.', 1)[0] + ".wav"
        convert_to_wav(input_path, output_path, ffmpeg_path)
    else:
        output_path = input_path

    model = WhisperModel("tiny", compute_type="int8", device="cpu", cpu_threads=1)
    transcript = transcribe_audio(model, output_path)
    return transcript
