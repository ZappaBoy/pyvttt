import whisper

from pyvttt.models.device import Device
from pyvttt.models.language import Language
from pyvttt.services.abstract_model_service import AbstractModelService


class Transcriber(AbstractModelService):
    model = None

    def __init__(self, force_cpu: bool = False):
        super().__init__(force_cpu)
        # Check available models using "whisper.available_models()"
        self.model_name = "large-v3"

    def set_threads(self, threads: int) -> None:
        whisper.torch.set_num_threads(threads)

    def get_available_device(self) -> Device:
        return Device.GPU if whisper.torch.cuda.is_available() else Device.CPU

    def set_device(self, device: Device) -> None:
        if device == Device.CPU:
            whisper.torch.cuda.is_available = lambda: False
        super().set_device(device)

    def load_model(self) -> None:
        if self.model is None:
            self.model = whisper.load_model(self.model_name)

    def clean_memory(self) -> None:
        self.model = None

    def transcribe(self, audio_path: str) -> str:
        self.load_model()
        transcription = self.model.transcribe(audio_path, verbose=False, fp16=self.is_gpu_available())
        self.clean_memory()
        return transcription['text'].strip()

    def detect_language(self, audio_path: str) -> Language:
        self.load_model()
        audio = whisper.load_audio(audio_path)
        audio = whisper.pad_or_trim(audio)
        # make log-Mel spectrogram and move to the same device as the model
        mel = whisper.log_mel_spectrogram(audio, n_mels=128).to(self.model.device)
        _, probs = self.model.detect_language(mel)
        options = whisper.DecodingOptions(fp16=self.is_gpu_available())
        result = whisper.decode(self.model, mel, options)
        return Language.get(result.language)
