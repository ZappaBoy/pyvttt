import torch
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast

from pyvttt.models.device import Device
from pyvttt.models.language import Language
from pyvttt.services.abstract_model_service import AbstractModelService


class Translator(AbstractModelService):
    model = None
    tokenizer = None

    def __init__(self, force_cpu: bool = False):
        super().__init__(force_cpu)
        # Check model https://huggingface.co/facebook/mbart-large-50-many-to-many-mmt
        self.model_name = "facebook/mbart-large-50-many-to-many-mmt"

    def set_threads(self, threads: int) -> None:
        torch.set_num_threads(threads)

    def get_available_device(self) -> Device:
        return Device.GPU if torch.cuda.is_available() else Device.CPU

    def set_device(self, device: Device) -> None:
        if device == Device.CPU:
            torch.cuda.is_available = lambda: False
        super().set_device(device)

    def load_model(self) -> None:
        if self.model_name is None or self.tokenizer is None:
            self.model = MBartForConditionalGeneration.from_pretrained(self.model_name)
            self.tokenizer = MBart50TokenizerFast.from_pretrained(self.model_name)

    def clean_memory(self) -> None:
        self.model = None
        self.tokenizer = None

    def translate(self, text: str, source_language: Language, target_language: Language = Language.ENGLISH) -> str:
        self.load_model()
        self.tokenizer.src_lang = source_language.get_code()
        tokens = []
        sentences = text.split('. ')
        for sentence in sentences:
            encoded_text = self.tokenizer(sentence, return_tensors="pt")
            generated_tokens = self.model.generate(
                **encoded_text,
                forced_bos_token_id=self.tokenizer.lang_code_to_id[target_language.get_code()]
            )
            tokens.append(generated_tokens[0])
        decoded_tokens = self.tokenizer.batch_decode(tokens, skip_special_tokens=True)
        translation = ' '.join(decoded_tokens)
        self.clean_memory()
        return translation
