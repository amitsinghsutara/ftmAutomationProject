import os
from concurrent.futures import ThreadPoolExecutor
from pydub import AudioSegment

def convert_wav_to_mp3(wav_path, output_folder):
    try:
        audio = AudioSegment.from_wav(wav_path)
        mp3_path = os.path.join(output_folder, os.path.basename(wav_path).replace(".wav", ".mp3"))
        audio.export(mp3_path, format="mp3")
        print(f"Converted {wav_path} to {mp3_path}")
    except Exception as e:
        print(f"Error converting {wav_path}: {e}")

def batch_convert(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with ThreadPoolExecutor() as executor:
        for root, _, files in os.walk(input_folder):
            for file in files:
                if file.lower().endswith(".wav"):
                    wav_path = os.path.join(root, file)
                    executor.submit(convert_wav_to_mp3, wav_path, output_folder)

if __name__ == "__main__":
    input_folder = "/home/amitsingh/Documents/frenchAudios/"  # Change this to the folder containing WAV files
    output_folder = "output_mp3_folder"  # Change this to the desired output folder
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    batch_convert(input_folder, output_folder)
