import argparse
import importlib.metadata as metadata
import multiprocessing
import os
from argparse import Namespace

__version__ = metadata.version(__package__ or __name__)

from pyvttt.models.language import Language
from pyvttt.models.log_level import LogLevel
from pyvttt.services.content_downloader import ContentDownloader
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

    def run(self):
        self.check_args()
        self.logger.info(f"Running...")
        self.logger.debug(self.args)
        urls = []
        if self.args.url:
            urls.append(self.args.url)
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

        if self.args.threads:
            self.logger.info(f"Setting number of threads to {self.args.threads}")
            self.transcriber.set_threads(self.args.threads)
            self.translator.set_threads(self.args.threads)

        for url in urls:
            audio_path, title = self.content_downloader.download_audio(url)
            transcription = self.transcriber.transcribe(audio_path)
            if self.args.translate:
                audio_language = self.transcriber.detect_language(audio_path)
                required_language = Language.get(str(self.args.translate).lower())
                self.logger.info(
                    f"Translating {title} from {audio_language.long_language} to {required_language.long_language}")
                transcription = self.translator.translate(transcription, src_language=audio_language,
                                                          target_language=required_language)

            if self.args.stdout:
                print(transcription)
            if self.args.output:
                if os.path.isdir(self.args.output):
                    filepath = os.path.join(self.args.output, self.get_transcription_filename(title))
                    self.save_transcription(transcription, filepath)
                else:
                    self.save_transcription(transcription, self.args.output)
            else:
                audio_dir = os.path.dirname(audio_path)
                transcription_path = os.path.join(audio_dir, self.get_transcription_filename(title))
                self.save_transcription(transcription, transcription_path)

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
    def save_transcription(transcription: str, path: str) -> None:
        with open(path, 'w') as f:
            f.write(transcription)

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
        parser.add_argument('--url', '-u', type=str, help='URL of the video to download and transcribe.')
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
        return parser.parse_args()

    def check_args(self) -> None:
        error_message = ""
        # Add arguments checks here
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
