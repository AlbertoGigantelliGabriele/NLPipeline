from pydantic import ValidationError
from pipeline import Pipeline
from validation_models import TextCleanerInput


def main():
    p = Pipeline(config_path="config.yaml")

    # Il primo modulo è "TextCleaner", che si aspetta un TextCleanerInput
    initial_input = TextCleanerInput(text="   Hello World!   ")

    try:
        result = p.run(initial_data=initial_input)
        print("OUTPUT FINALE:")
        print(result)
    except (ValueError, ValidationError) as e:
        print(f"Errore: {e}")


if __name__ == "__main__":
    main()
