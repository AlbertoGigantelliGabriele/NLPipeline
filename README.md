# NLPipeline

## Struttura del Progetto

Il progetto è organizzato in diversi file chiave, ognuno con un ruolo specifico:

- **`main.py`**  
  Punto di ingresso principale dell'applicazione. Crea un'istanza della classe `Pipeline` utilizzando il percorso di configurazione specificato (`config.yaml`). Prepara un input iniziale con il modello di validazione `TextCleanerInput` e avvia l'esecuzione della pipeline, gestendo eventuali errori di validazione o di valore.

- **`pipeline.py`**  
  Definisce la classe `Pipeline`, che gestisce l'esecuzione sequenziale dei moduli definiti nella configurazione. Carica i moduli specificati nel file `config.yaml` ed esegue ciascuno in ordine, passando i dati elaborati da un modulo al successivo.

  **Metodo `run` nella Classe `Pipeline`**  
  Responsabile dell'esecuzione sequenziale dei vari moduli. Itera attraverso i moduli caricati precedentemente in memoria, passando i dati elaborati da uno all'altro. Include una condizione specifica per il modulo `TextGenerator` per gestire il suo comportamento particolare.

- **`components.py`**  
  Contiene l'implementazione dei moduli individuali utilizzati nella pipeline. Ad esempio, il modulo `TextCleaner` si occupa della pulizia del testo, rimuovendo spazi extra, caratteri speciali e altre operazioni di pre-elaborazione.

  esempio di codice:
  ```python
  from abc import ABC, abstractmethod

  class PipelineComponent(ABC):
      @abstractmethod
      def run(self, data):
          pass
  
- **`validation_models.py`**
  Definisce i modelli di dati utilizzati per la validazione degli input e degli output dei moduli. Utilizza `pydantic` per assicurare che i dati rispettino gli schemi previsti, facilitando la gestione degli errori e garantendo l'integrità dei dati durante l'elaborazione.

  ```python
  class TextCleaner(PipelineComponent):
      def run(self, data):
          # Logica per pulire il testo
          return cleaned_data
  ```

- **`config.yaml`**

  File di configurazione in formato YAML che specifica i moduli da includere nella pipeline e l'ordine di esecuzione. Permette una facile configurazione e modifica della pipeline senza alterare il codice sorgente.

  ```yaml
  pipeline:
  - name: cleaner
    type: TextCleaner

  - name: extractor
    type: EntityExtractor

  - name: sentiment
    type: SentimentAnalyzer

  - name: generator
    type: TextGenerator
    params:
      max_length: 100
  ```

## Setup

1. **Clona il repository:**

   ```bash
   git clone https://github.com/AlbertoGigantelliGabriele/NLPipeline.git
   cd NLPipeline
   ```

2. **Costruisci l'immagine Docker:**
   ```bash
   docker-compose build
   ```

3. **Avvia i container:**
   ```bash
   docker-compose up
   ```
   
4. **In alternativa:**
   ```
   docker-compose up --build
   ```

   Così è possibile visualizzare l'ultimo output della pipeline, ovvero il testo fittizio generato. Se si vuole visualizzare informazioni aggiuntive, è possibile decommentare le print all'interno della funzione `run()` della pipeline.
