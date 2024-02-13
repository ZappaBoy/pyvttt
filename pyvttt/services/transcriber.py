import whisper

from pyvttt.shared.utils.logger import Logger

GPU = "GPU"
CPU = "CPU"


class Transcriber:

    def __init__(self, force_cpu: bool = False):
        self.logger = Logger()
        if force_cpu:
            whisper.torch.cuda.is_available = lambda: False
        self.device = GPU if whisper.torch.cuda.is_available() else CPU
        self.logger.info(f"Using device: {self.device}")
        # Check available models using "whisper.available_models()"
        self.stt_model = whisper.load_model("large-v3")

    def transcribe(self, audio_path: str) -> str:
        transcription = self.stt_model.transcribe(audio_path, verbose=False, fp16=self.device == GPU)
        return transcription['text']

    @staticmethod
    def set_threads(threads: int) -> None:
        whisper.torch.set_num_threads(threads)
