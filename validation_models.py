from pydantic import BaseModel, PositiveInt
from typing import List


# region TextCleaner
class TextCleanerInput(BaseModel):
    text: str


class TextCleanerOutput(BaseModel):
    text: str


# endregion

# region EntityExtractor
class EntityExtractorInput(BaseModel):
    text: str


class EntityExtractorOutput(BaseModel):
    text: str
    entities: List[str]


# endregion

# region SentimentAnalyzer
class SentimentAnalyzerInput(BaseModel):
    # text: str
    entities: List[str]


class SentimentAnalyzerOutput(BaseModel):
    score: float


# endregion

# region TextGenerator
class TextGeneratorInput(BaseModel):
    prompt: str
    max_length: PositiveInt = 1  # > 0


class TextGeneratorOutput(BaseModel):
    generated_txt: str
# endregion
