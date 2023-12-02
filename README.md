# ToDo App

Questo repository contiene un'applicazione di gestione delle attività "to-do" e dei movimenti finanziari. L'applicazione è progettata per aiutarti a tenere traccia dei tuoi compiti e delle tue transazioni finanziarie.

## Struttura del Progetto

La struttura del progetto è organizzata nei seguenti file e cartelle:

- **category.py**: Contiene la definizione della classe `Category` per gestire le categorie delle attività.
- **config.json**: File di configurazione contenente le impostazioni dell'applicazione.
- **csv**: Cartella che contiene i file CSV con i movimenti finanziari.
- **db.py**: Modulo per la gestione del database SQLite.
- **main.py**: File principale del programma che coordina l'esecuzione dell'applicazione.
- **movement.py**: Contiene la classe `Movement` per rappresentare i movimenti finanziari.
- **pocket.py**: Modulo per la gestione dei movimenti finanziari.
- **task.py**: Contiene la classe `Task` per rappresentare le attività.
- **temp**: Cartella temporanea per archiviare dati temporanei.
- **todo.db**: File del database SQLite che memorizza i dati dell'applicazione.
- **todolist.py**: Modulo per la gestione delle liste di attività.
- **utils.py**: Contiene funzioni di utilità per il progetto.

## Requisiti e Installazione

Per eseguire l'applicazione, segui questi passaggi:

1. Clona il repository:

   ```bash
   git clone https://github.com/TUO_USERNAME/ToDo.git

    ```

2. Crea un ambiente virtuale utilizzando il modulo `venv` di Python. Esegui i seguenti comandi:

    ```bash
    python -m venv venv
    ```

3. Attiva l'ambiente virtuale. La procedura può variare a seconda del sistema operativo:

   - Su Linux/Mac, utilizza il seguente comando:

     ```bash
     source venv/bin/activate
     ```

   - Su Windows, utilizza il seguente comando:

     ```bash
     venv\Scripts\activate
     ```

4. Installa le dipendenze necessarie eseguendo il seguente comando:

    ```bash
    pip install -r requirements.txt
    ```

5. Una volta completati i passaggi sopra indicati, puoi eseguire il tool usando il seguente comando:

    ```bash
    python main.py
    ```

## Utilizzo dell'Applicazione

L'applicazione offre diverse funzionalità, tra cui l'aggiunta, la visualizzazione, la modifica e la rimozione di attività ("to-do") e movimenti finanziari. Puoi interagire con l'applicazione tramite comandi da console.

Esempi di comandi:

- Aggiungi un nuovo task:

  ```bash
  python main.py TASK ADD
  ```
- Visualizza la lista di task:

    ```bash
    TASK LIST
    ```
- Aggiungi un nuovo movimento finanziario:

    ```bash
    MOVEMENT ADD
    ```
- Visualizza la lista dei movimenti finanziari:

    ```bash
    MOVEMENT LIST
    ```
- Per ulteriori dettagli sui comandi disponibili, esegui:

    ```bash
    HELP
    ```

Buona gestione delle attività e dei movimenti finanziari!