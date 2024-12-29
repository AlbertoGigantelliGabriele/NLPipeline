import yaml
from typing import List, Dict, Any
from pydantic import BaseModel, ValidationError
from validation_models import *
from components import *

MODULE_REGISTRY = {
    "TextCleaner": TextCleaner,
    "EntityExtractor": EntityExtractor,
    "SentimentAnalyzer": SentimentAnalyzer,
    "TextGenerator": TextGenerator,
}

# Per sapere quale "schema di input" serve a ciascun modulo
# (Potremmo prendere la classe e leggere la type-hint di run(),
#  ma in modo semplice facciamo un mapping manuale)
INPUT_SCHEMAS = {
    "TextCleaner": TextCleanerInput,
    "EntityExtractor": EntityExtractorInput,
    "SentimentAnalyzer": SentimentAnalyzerInput,
    "TextGenerator": TextGeneratorInput,
}


class Pipeline:
    def __init__(self, config_path: str):
        """
        Inizializza la pipeline leggendo un file YAML.
        """
        self.config_path = config_path
        self.steps: List[Dict[str, Any]] = []
        self._load_config()

    def _load_config(self):
        """
        Carica dal file .yaml la configurazione, gli steps
        :return:
        """

        with open(self.config_path, "r") as f:
            config = yaml.safe_load(f)

        pipeline_steps = config.get("pipeline", [])

        # print("pipeline_steps:") print("\n".join(str(step) for step in pipeline_steps) + "\n")

        for step_conf in pipeline_steps:

            module_type = step_conf["type"]
            module_class = MODULE_REGISTRY.get(module_type)
            if not module_class:
                raise ValueError(f"Tipo di modulo sconosciuto: {module_type}")

            instance = module_class()  # istanziamo il modulo
            params = step_conf.get("params", {})  # parametri extra

            self.steps.append({
                "name": step_conf.get("name", module_type),
                "module_type": module_type,
                "instance": instance,
                "params": params
            })

            # verifichiamo che siano memorizzati correttamente
            # print( f"name: {step_conf.get('name', module_type)},\nmodule_type: {module_type},\ninstance: {instance},\nparams: {params}\n")

    def run(self, initial_data: BaseModel) -> BaseModel:
        """
        Esegue la pipeline in sequenza.
        :param initial_data: Il modello pydantic che rappresenta l'input al primo step.
        :return: L'output finale dell'ultimo step (BaseModel).
        """

        data = initial_data  # text='\tHello World!\t"

        for step in self.steps:
            module_instance: BaseModule = step["instance"]  # instanza della classe
            module_type = step["module_type"]
            params = step["params"]

            # Merge dei param nel "data" se serve
            data_dict = data.model_dump()
            data_dict.update(params)

            input_schema = INPUT_SCHEMAS[module_type]  # ricaviamo lo schema di input corretto
            # print(f"module_type: {module_type}")

            try:
                if module_type == "TextGenerator":
                    step_input = input_schema(**{"prompt": "Hello World!", "max_length": 50})
                else:
                    step_input = input_schema(**data_dict)
            except ValidationError as ve:
                raise ValueError(
                    f"Errore di validazione input per modulo {module_type}: {ve}"
                )

            step_output = module_instance.run(step_input)
            # print(step_output)
            data = step_output

        return data
