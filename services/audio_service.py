from pathlib import Path

from moviepy.video.io.VideoFileClip import VideoFileClip
from pydub import AudioSegment


def extract_audio_from_video(*, video_path: Path) -> Path:
    audio_path = video_path.parent / "extracted_audio.mp3"
    video = VideoFileClip(str(video_path))
    audio = video.audio
    audio.write_audiofile(audio_path, logger=None)
    video.close()
    return audio_path


def split_audio(*, audio_path, max_size=26214400):
    audio = AudioSegment.from_file(audio_path)
    chunk_size_ms = (max_size // (audio.frame_rate * audio.frame_width)) * 1000  # Convert to milliseconds
    chunks = [audio[i:i + chunk_size_ms] for i in range(0, len(audio), chunk_size_ms)]
    return chunks