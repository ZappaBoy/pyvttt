import os
import tempfile
from typing import Tuple

from pytube import YouTube

from pyvttt.shared.utils.logger import Logger


# Only YouTube videos are actually supported
class ContentDownloader:
    temp_dir = tempfile.gettempdir()

    def __init__(self):
        self.logger = Logger()

    def download_audio(self, url: str, force_download: bool = False) -> Tuple[str, str]:
        self.logger.info(f"Downloading video from {url}")

        yt: YouTube = YouTube(url)
        self.logger.info(f"Downloading: {yt.title}")
        audio_streams = yt.streams.get_audio_only()
        download_dir = os.path.join(self.temp_dir, yt.video_id)
        download_path = audio_streams.download(output_path=download_dir, skip_existing=not force_download)
        self.logger.info(f"Downloaded audio to {download_path}")
        return download_path, yt.title
