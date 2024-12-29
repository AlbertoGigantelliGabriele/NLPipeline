from abc import ABC, abstractmethod
from typing import Any, List
from validation_models import *


# region base
class BaseModule(ABC):

    @abstractmethod
    def run(self, input_data: Any) -> Any:
        """
        Metodo che accomuna tutti i moduli, esegue il task del modulo validando input e output

        :param text:
        :param kwargs:
        :return:
        """
        pass


# endregion

# region TextCleaner
class TextCleaner(BaseModule):

    def clean(self, text: str) -> str:
        # rimuove caratteri speciali
        return text.strip()

    def run(self, input_data: TextCleanerInput) -> TextCleanerOutput:
        text_in = input_data.text
        cleaned_text = self.clean(text_in)

        return TextCleanerOutput(text=cleaned_text)


# endregion

# region EntityExtractor
class EntityExtractor(BaseModule):

    def extract_entities(self, text: str, **kwargs) -> List[str]:
        # estrae entità dal testo
        return ["entity1", "entity2"]

    def run(self, input_data: EntityExtractorInput) -> EntityExtractorOutput:
        text_in = input_data.text
        entities_ = self.extract_entities(text_in)

        return EntityExtractorOutput(text=text_in, entities=entities_)


# endregion

# region SentimentAnalyzer
class SentimentAnalyzer(BaseModule):

    def analyze(self, text: str) -> float:
        # calcola sentiment score (-1 to 1)
        return 0.8

    def run(self, input_data: SentimentAnalyzerInput) -> SentimentAnalyzerOutput:
        txt = input_data.text

        return SentimentAnalyzerOutput(score=self.analyze(txt))


# endregion

# region TextGenerator
class TextGenerator(BaseModule):

    def generate(self, text: str, max_length: int = 50) -> str:
        # genera testo dato un prompt
        return f"Generated text based on: {text[:max_length]}"

    def run(self, input_data: TextGeneratorInput) -> TextCleanerOutput:
        result = self.generate(input_data.prompt, input_data.max_length)

        return TextGeneratorOutput(generated_txt=result)
# endregion
