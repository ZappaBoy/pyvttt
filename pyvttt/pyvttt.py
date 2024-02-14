import argparse
import importlib.metadata as metadata
import multiprocessing
import os
import sys
from argparse import Namespace

__version__ = metadata.version(__package__ or __name__)

from pyvttt.models.language import Language
from pyvttt.models.log_level import LogLevel
from pyvttt.services.content_downloader import ContentDownloader
from pyvttt.services.summarizer import Summarizer
from pyvttt.services.transcriber import Transcriber
from pyvttt.services.translator import Translator
from pyvttt.shared.utils.logger import Logger


class Pyvttt:
    def __init__(self):
        self.logger = Logger()
        self.args = self.parse_args()
        self.set_verbosity()
        self.content_downloader = None
        self.transcriber = None
        self.translator = None
        self.summarizer = None

    def run(self):
        self.check_args()
        self.logger.info(f"Running...")
        self.logger.debug(self.args)
        urls = []
        if self.args.urls:
            urls.extend(self.args.urls)
        if self.args.file:
            urls.extend(self.read_uncommented_lines_from_file(filename=self.args.file))

        if '.' not in os.path.basename(self.args.output):
            os.makedirs(self.args.output, exist_ok=True)
        else:
            output_dir = os.path.dirname(self.args.output)
            if output_dir not in ["", ".", ".."] and not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)

        self.content_downloader = ContentDownloader()
        self.transcriber = Transcriber(force_cpu=self.args.cpu)
        self.translator = Translator(force_cpu=self.args.cpu)
        self.summarizer = Summarizer(force_cpu=self.args.cpu)

        if self.args.threads:
            self.logger.info(f"Setting number of threads to {self.args.threads}")
            self.transcriber.set_threads(self.args.threads)
            self.translator.set_threads(self.args.threads)
            self.translator.set_threads(self.args.threads)

        audio_paths = []
        titles = []
        for url in urls:
            audio_path, title = self.content_downloader.download_audio(url)
            audio_paths.append(audio_path)
            titles.append(title)

        if self.args.audio:
            for audio_path in self.args.audio:
                audio_paths.append(audio_path.name)
                titles.append(os.path.basename(audio_path.name))

        for audio_path, title in zip(audio_paths, titles):
            self.logger.info(f"Processing: {title}")
            output = self.transcriber.transcribe(audio_path)

            if self.args.translate or self.args.summarize:
                source_language = self.detect_audio_language(audio_path)
                if self.args.summarize:
                    target_language = Language.ENGLISH
                    output = self.translate_audio(output, source_language, target_language)
                    output = self.summarizer.summarize(output, strength=self.args.summarize)
                    source_language = target_language
                if self.args.translate:
                    target_language = Language.get(str(self.args.translate).lower())
                    output = self.translate_audio(output, source_language, target_language)

            if self.args.stdout:
                print(output)
            if self.args.output:
                if os.path.isdir(self.args.output):
                    filepath = os.path.join(self.args.output, self.get_transcription_filename(title))
                    self.save_output(output, filepath)
                else:
                    self.save_output(output, self.args.output)
            else:
                audio_dir = os.path.dirname(audio_path)
                transcription_path = os.path.join(audio_dir, self.get_transcription_filename(title))
                self.save_output(output, transcription_path)

    def detect_audio_language(self, audio_path: str) -> Language:
        return self.transcriber.detect_language(audio_path)

    def translate_audio(self, text: str, source_language: Language, target_language: Language):
        if source_language == target_language:
            return text
        return self.translator.translate(text, source_language=source_language, target_language=target_language)

    @staticmethod
    def read_uncommented_lines_from_file(filename):
        read_lines = []
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if not line.startswith('#'):
                    read_lines.append(line)
        return read_lines

    @staticmethod
    def get_transcription_filename(title: str) -> str:
        return f"{title}_transcription.txt"

    @staticmethod
    def save_output(text: str, path: str) -> None:
        with open(path, 'w') as f:
            f.write(text)

    @staticmethod
    def parse_args() -> Namespace:
        parser = argparse.ArgumentParser(description="pyvttt is a simple Video-to-Text Transcriber written in Python.")
        parser.add_argument('--verbose', '-v', action='count', default=1,
                            help='Increase verbosity. Use more than once to increase verbosity level (e.g. -vvv).')
        parser.add_argument('--debug', action='store_true', default=False,
                            help='Enable debug mode.')
        parser.add_argument('--quiet', '-q', action=argparse.BooleanOptionalAction, default=False,
                            required=False, help='Do not print any output/log')
        parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}',
                            help='Show version and exit.')
        parser.add_argument('--url', '-u', type=str, nargs='+',
                            help='URL(s) of the video to download and transcribe.')
        parser.add_argument('--file', '-f', type=str, help='Path to file with urls to download and transcribe.')
        parser.add_argument('--output', '-o', type=str, help='Path to save the transcription.')
        parser.add_argument('--stdout', '-s', action=argparse.BooleanOptionalAction, default=False)
        parser.add_argument('--threads', '-t', type=int, default=multiprocessing.cpu_count() // 2,
                            help='Number of threads to use. Default is half of the available cores.')
        parser.add_argument('--cpu', '-c', action=argparse.BooleanOptionalAction, default=False,
                            help='Force to use CPU instead of GPU.')
        parser.add_argument('--force-download', '-d', action=argparse.BooleanOptionalAction, default=False,
                            help='Force to download the video even if it is already downloaded')
        parser.add_argument('--translate', '-l', type=str,
                            help='Translate transcription to the specified language. Default is english.')
        parser.add_argument('--summarize', '-m', type=int,
                            help='Summarize transcription, you can define a summarization strength between 0 and 100. '
                                 'Suggested value: 90.')
        parser.add_argument('--audio', '-a', type=argparse.FileType('r'), nargs='+',
                            help='Audio file(s) to process. Supported formats: m4a, mp3, webm, mp4, mpga, wav and mpeg')
        return parser.parse_args(args=None if sys.argv[1:] else ['--help'])

    def check_args(self) -> None:
        error_message = ""
        if self.args.url is None and self.args.file is None and self.args.audio is None:
            error_message += "No url or file specified. Please specify at least one url or file."
        if error_message != "":
            self.logger.error(error_message)
            exit(1)

    def set_verbosity(self) -> None:
        if self.args.quiet:
            verbosity_level = LogLevel.DISABLED
        else:
            if self.args.debug or self.args.verbose > LogLevel.DEBUG.value:
                verbosity_level = LogLevel.DEBUG
            else:
                verbosity_level = self.args.verbose
        self.logger.set_log_level(verbosity_level)
