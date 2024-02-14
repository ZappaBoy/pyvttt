import torch
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast

from pyvttt.models.device import Device
from pyvttt.models.language import Language
from pyvttt.services.abstract_model_service import AbstractModelService


class Translator(AbstractModelService):
    model = None
    tokenizer = None
    max_tokens = 1024

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
        if self.model is None or self.tokenizer is None:
            self.model = MBartForConditionalGeneration.from_pretrained(self.model_name)
            self.tokenizer = MBart50TokenizerFast.from_pretrained(self.model_name)

    def clean_memory(self) -> None:
        self.model = None
        self.tokenizer = None

    def translate(self, text: str, source_language: Language, target_language: Language = Language.ENGLISH) -> str:
        self.load_model()
        self.tokenizer.src_lang = source_language.get_code()
        sentences = text.split('. ')
        sentences = [sentence + '.' for sentence in sentences]

        paragraphs = []
        tokens = []
        while len(sentences) > 0:
            sentence = sentences.pop(0).split(' ')
            if len(tokens) + len(sentence) > self.max_tokens:
                paragraphs.append(tokens)
                tokens = []
            else:
                tokens.extend(sentence)

        if len(tokens) > 0:
            paragraphs.append(tokens)

        chunks = []
        for paragraph in paragraphs:
            encoded_text = self.tokenizer(' '.join(paragraph), return_tensors="pt")
            generated_tokens = self.model.generate(
                **encoded_text,
                forced_bos_token_id=self.tokenizer.lang_code_to_id[target_language.get_code()]
            )
            generated_tokens = generated_tokens[0]
            chunks.append(generated_tokens)
        decoded_tokens = self.tokenizer.batch_decode(chunks, skip_special_tokens=True)
        translation = ' '.join(decoded_tokens)
        self.clean_memory()
        return translation
