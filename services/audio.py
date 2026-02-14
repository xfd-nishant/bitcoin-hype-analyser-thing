import os
import tempfile
import subprocess

def download_audio(video_url: str) -> str:
    """
    Downloads audio from a YouTube video and returns the path to the audio file.
    """
    temp_dir = tempfile.mkdtemp()
    output_template = os.path.join(temp_dir, "%(id)s.%(ext)s")

    command = [
        "yt-dlp",
        "-f", "bestaudio",
        "--extract-audio",
        "--audio-format", "mp3",
        "-o", output_template,
        video_url
    ]

    subprocess.run(command, check=True)

    # Find the downloaded file
    for file in os.listdir(temp_dir):
        if file.endswith(".mp3"):
            return os.path.join(temp_dir, file)

    raise FileNotFoundError("Audio file not found after download.")
