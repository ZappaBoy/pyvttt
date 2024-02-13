from transformers import MBartForConditionalGeneration, MBart50TokenizerFast

from pyvttt.models.device import Device
from pyvttt.models.language import Language
from pyvttt.services.abstract_model_service import AbstractModelService


class Translator(AbstractModelService):

    def __init__(self, force_cpu: bool = False):
        super().__init__(force_cpu)
        # Check available models using "whisper.available_models()"
        model_name = "facebook/mbart-large-50-many-to-many-mmt"
        self.model = MBartForConditionalGeneration.from_pretrained(model_name)
        self.tokenizer = MBart50TokenizerFast.from_pretrained(model_name)

    def set_threads(self, threads: int) -> None:
        pass

    def get_available_device(self) -> Device:
        pass

    def set_device(self, device: Device) -> None:
        super().set_device(device)

    def translate(self, text: str, src_language: Language, target_language: Language = Language.ENGLISH) -> str:
        self.tokenizer.src_lang = src_language.get_code()
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
        return translation
