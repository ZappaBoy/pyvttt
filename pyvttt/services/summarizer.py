import torch
from transformers import pipeline

from pyvttt.models.device import Device
from pyvttt.services.abstract_model_service import AbstractModelService


class Summarizer(AbstractModelService):
    model = None

    def __init__(self, force_cpu: bool = False):
        super().__init__(force_cpu)
        self.model_name = "facebook/bart-large-cnn"

    def set_threads(self, threads: int) -> None:
        torch.set_num_threads(threads)

    def get_available_device(self) -> Device:
        return Device.GPU if torch.cuda.is_available() else Device.CPU

    def set_device(self, device: Device) -> None:
        if device == Device.CPU:
            torch.cuda.is_available = lambda: False
        super().set_device(device)

    def load_model(self) -> None:
        if self.model is None:
            self.model = pipeline("summarization", model=self.model_name)

    def clean_memory(self) -> None:
        self.model = None

    def summarize(self, text: str, strength: int) -> str:
        self.load_model()
        max_length = len(text.split(' ')) * strength // 100
        min_length = max_length * 90 // 100
        summary = self.model(text, max_length=max_length, min_length=min_length, do_sample=False)
        self.clean_memory()
        return summary[0]['summary_text']
