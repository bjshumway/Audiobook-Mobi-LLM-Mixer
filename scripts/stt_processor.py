import os
import sys
import json
import subprocess
import datetime
from faster_whisper import WhisperModel

def get_audio_duration(file_path):
    """Uses ffprobe to get the exact duration of the audio file in seconds."""
    cmd = [
        'ffprobe', '-v', 'error', '-show_entries', 'format=duration', 
        '-of', 'default=noprint_wrappers=1:nokey=1', file_path
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return float(result.stdout.strip())

def extract_audio_chunk(input_path, output_path, start_time, duration):
    """Uses ffmpeg to extract a specific chunk of audio."""
    # We export as a 16kHz WAV file because Whisper natively expects this format anyway, making it faster.
    cmd = [
        'ffmpeg', '-y', '-i', input_path, 
        '-ss', str(start_time), '-t', str(duration), 
        '-ar', '16000', '-ac', '1', '-c:a', 'pcm_s16le', 
        '-loglevel', 'error', output_path
    ]
    subprocess.run(cmd)

def transcribe_local_audio(mp3_path):
    """
    Transcribes a massive MP3 file by chunking it to prevent RAM explosion.
    """
    print(f"Loading local Whisper model...")
    model = WhisperModel("base", device="auto", compute_type="int8")

    if not os.path.exists(mp3_path):
        print(f"Error: File not found at {mp3_path}")
        return None

    # 1. Get total duration
    print("Analyzing audio file length...")
    total_duration = get_audio_duration(mp3_path)
    total_formatted = str(datetime.timedelta(seconds=int(total_duration)))
    print(f"Total Audio Duration: {total_formatted}")

    all_words = []
    full_transcript = ""

    # 2. Setup Chunking Variables (30 minutes per chunk)
    chunk_duration = 1800 
    current_time = 0
    temp_file = "temp_processing_chunk.wav"
    chunk_index = 1
    total_chunks = int(total_duration // chunk_duration) + 1

    print(f"\nProcessing in {total_chunks} chunks to conserve RAM...")

    # 3. Loop through the audio
    while current_time < total_duration:
        print(f"\n--- Extracting Chunk {chunk_index}/{total_chunks} (Starts at {str(datetime.timedelta(seconds=int(current_time)))}) ---")
        
        # Extract the specific 30-minute window
        extract_audio_chunk(mp3_path, temp_file, current_time, chunk_duration)

        print("Transcribing chunk...")
        segments, info = model.transcribe(temp_file, word_timestamps=True)

        for segment in segments:
            full_transcript += segment.text + " "
            for word in segment.words:
                # IMPORTANT: We add the current_time offset to the word's timestamp
                # so the final JSON aligns perfectly with the massive 25-hour file.
                absolute_start = current_time + word.start
                absolute_end = current_time + word.end
                
                all_words.append({
                    "word": word.word.strip(),
                    "start": round(absolute_start, 2),
                    "end": round(absolute_end, 2)
                })
                
            # Print progress based on the absolute timestamp
            progress_time = current_time + segment.end
            progress_formatted = str(datetime.timedelta(seconds=int(progress_time)))
            print(f"  -> Transcribed up to {progress_formatted}...")

        # Move the window forward
        current_time += chunk_duration
        chunk_index += 1

    # Clean up the temporary file
    if os.path.exists(temp_file):
        os.remove(temp_file)

    print("\nTranscription complete! RAM survived.")
    return {
        "full_transcript": full_transcript.strip(),
        "words": all_words
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python stt_processor.py <path_to_mp3_file>")
        sys.exit(1)

    test_mp3 = sys.argv[1]
    
    print("--- Starting STT Processing ---")
    results = transcribe_local_audio(test_mp3)
    
    if results and results["words"]:
        # Save full test output to a json file
        output_file = "stt_test_output.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        print(f"\nSUCCESS! Full transcription saved to {output_file}")
    else:
        print("\nTranscription failed.")