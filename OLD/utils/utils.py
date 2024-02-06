from db import movements
from os import path, listdir, remove, system, name, makedirs, getcwd
import csv, json
from sqlite3 import connect, Connection, PARSE_DECLTYPES, PARSE_COLNAMES
from datetime import datetime


def process_directory(directory_path, logger):
    db_path = "db/todo.db"
    conn = connect(db_path, detect_types=PARSE_DECLTYPES | PARSE_COLNAMES)
    # Ottieni la lista di file nella directory
    files = [f for f in listdir("./csv") if f.upper().endswith('.CSV')]
    result_csv_movements = []
    result_saldo_data = ""
    result_saldo = ""


    for i, file in enumerate(files):
        file_path = path.join(directory_path, file)

        # Verifica se il file è già presente nel database
        if(not movements.check_file_exists(conn, file)):
            # Se il file non è presente, elabora il file CSV e inserisci nel database
            logger.info(f"File '{file}' non presente nel database.")
            movements.add_movements_file(conn, file)
            csv_movements, saldo_data, saldo = process_csv_file(file_path)
            print(f"{saldo} - result: {result_saldo}")
            if(result_saldo_data == "" or result_saldo_data < datetime.strptime(saldo_data, "%d/%m/%Y")):
                result_saldo_data = datetime.strptime(saldo_data, "%d/%m/%Y")
                result_saldo = saldo
            if(i > 0):
                csv_movements = csv_movements[1:]
            result_csv_movements.extend(csv_movements)
        else:
            logger.info(f"File '{file}' già presente nel database.")
    print(f"{result_saldo_data} - {result_saldo}")
    return result_csv_movements, result_saldo_data, result_saldo

def check_basic_folder():
    # Ottieni il percorso della directory del progetto
    project_directory = getcwd()

    # Crea la cartella 'temp' se non esiste già
    temp_directory = path.join(project_directory, 'temp')
    makedirs(temp_directory, exist_ok=True)

    # Crea la cartella 'csv' se non esiste già
    csv_directory = path.join(project_directory, 'csv')
    makedirs(csv_directory, exist_ok=True)

    # Crea la cartella 'config' se non esiste già
    config_directory = path.join(project_directory, 'config')
    makedirs(config_directory, exist_ok=True)

    # Crea la cartella 'log' se non esiste già
    log_directory = path.join(project_directory, 'log')
    makedirs(log_directory, exist_ok=True)

def rimuovi_vecchio_db(old_db_path, logger):
    try:
        remove(old_db_path)
        logger.info(f"File {old_db_path} rimosso con successo.")
    except FileNotFoundError:
        logger.info(f"File {old_db_path} non trovato.")
    except Exception as e:
        logger.error(f"Si è verificato un errore durante la rimozione del file: {str(e)}")

def start(logger):
    logger.info(f"\n\n----- INIZIO PROCEDURE DI AVVIO -----\n")
    # Ottieni il percorso della directory del progetto
    project_directory = getcwd()

    # Definisci i dati da inserire nel file config.json
    config_data = {
        "MOVEMENTS_RECORD_PAGE": "10",
        "TASKS_RECORD_PAGE": "10",
        "MOVEMENTS_MAX_EXPENSES": "0"
    }

    word_category_data = {
        "Stipendio": {
            "keywords": [
                "PAROLA CHIAVE 1",
                "PAROLA CHIAVE 2",
                "PAROLA CHIAVE 3"
            ],
            "min_entry": 0,
            "max_expense": -1
        },
        "Prelievi": {
            "keywords": [
                "PAROLA CHIAVE 1",
                "PAROLA CHIAVE 2",
                "PAROLA CHIAVE 3"
            ],
            "min_entry": 0,
            "max_expense": -1
        },
        "Spese Domestiche": {
            "keywords": [
                "PAROLA CHIAVE 1",
                "PAROLA CHIAVE 2",
                "PAROLA CHIAVE 3"
            ],
            "min_entry": 0,
            "max_expense": -1
        },
        "Cibo e Generi Alimentari": {
            "keywords": [
                "PAROLA CHIAVE 1",
                "PAROLA CHIAVE 2",
                "PAROLA CHIAVE 3"
            ],
            "min_entry": 0,
            "max_expense": -1
        },
        "Trasporti": {
            "keywords": [
                "PAROLA CHIAVE 1",
                "PAROLA CHIAVE 2",
                "PAROLA CHIAVE 3"
            ],
            "min_entry": 0,
            "max_expense": -1
        },
        "Assicurazioni": {
            "keywords": [
                "PAROLA CHIAVE 1",
                "PAROLA CHIAVE 2",
                "PAROLA CHIAVE 3"
            ],
            "min_entry": 0,
            "max_expense": -1
        },
        "Spese Mediche": {
            "keywords": [
                "PAROLA CHIAVE 1",
                "PAROLA CHIAVE 2",
                "PAROLA CHIAVE 3"
            ],
            "min_entry": 0,
            "max_expense": -1
        },
        "Divertimento e Tempo Libero": {
            "keywords": [
                "PAROLA CHIAVE 1",
                "PAROLA CHIAVE 2",
                "PAROLA CHIAVE 3"
            ],
            "min_entry": 0,
            "max_expense": -1
        },
        "Debiti e Prestiti": {
            "keywords": [
                "PAROLA CHIAVE 1",
                "PAROLA CHIAVE 2",
                "PAROLA CHIAVE 3"
            ],
            "min_entry": 0,
            "max_expense": -1
        },
        "Risparmi e Investimenti": {
            "keywords": [
                "PAROLA CHIAVE 1",
                "PAROLA CHIAVE 2",
                "PAROLA CHIAVE 3"
            ],
            "min_entry": 0,
            "max_expense": -1
        },
        "Educazione": {
            "keywords": [
                "PAROLA CHIAVE 1",
                "PAROLA CHIAVE 2",
                "PAROLA CHIAVE 3"
            ],
            "min_entry": 0,
            "max_expense": -1
        },
        "Abbigliamento e Accessori": {
            "keywords": [
                "PAROLA CHIAVE 1",
                "PAROLA CHIAVE 2",
                "PAROLA CHIAVE 3"
            ],
            "min_entry": 0,
            "max_expense": -1
        },
        "Emergenze": {
            "keywords": [
                "PAROLA CHIAVE 1",
                "PAROLA CHIAVE 2",
                "PAROLA CHIAVE 3"
            ],
            "min_entry": 0,
            "max_expense": -1
        },
        "Vizi": {
            "keywords": [
                "PAROLA CHIAVE 1",
                "PAROLA CHIAVE 2",
                "PAROLA CHIAVE 3"
            ],
            "min_entry": 0,
            "max_expense": -1
        },
        "Acquisti Online": {
            "keywords": [
                "PAROLA CHIAVE 1",
                "PAROLA CHIAVE 2",
                "PAROLA CHIAVE 3"
            ],
            "min_entry": 0,
            "max_expense": -1
        },
        "Rimborsi": {
            "keywords": [
                "PAROLA CHIAVE 1",
                "PAROLA CHIAVE 2",
                "PAROLA CHIAVE 3"
            ],
            "min_entry": 0,
            "max_expense": -1
        },
        "Abbonamenti": {
            "keywords": [
                "PAROLA CHIAVE 1",
                "PAROLA CHIAVE 2",
                "PAROLA CHIAVE 3"
            ],
            "min_entry": 0,
            "max_expense": -1
        },
        "Regali": {
            "keywords": [
                "PAROLA CHIAVE 1",
                "PAROLA CHIAVE 2",
                "PAROLA CHIAVE 3"
            ],
            "min_entry": 0,
            "max_expense": -1
        },
        "Bancomat pay": {
            "keywords": [
                "PAROLA CHIAVE 1",
                "PAROLA CHIAVE 2",
                "PAROLA CHIAVE 3"
            ],
            "min_entry": 0,
            "max_expense": -1
        },
        "Paypal": {
            "keywords": [
                "PAROLA CHIAVE 1",
                "PAROLA CHIAVE 2",
                "PAROLA CHIAVE 3"
            ],
            "min_entry": 0,
            "max_expense": -1
        }
    }

    # Crea il percorso completo del file config.json
    config_file_path = path.join(project_directory, 'config/config.json')

    # Crea il percorso completo del file config.json
    word_category_file_path = path.join(project_directory, 'config/word_category.json')

    # Scrivi i dati nel file config.json se il file non esiste già
    if not path.exists(config_file_path):
        with open(config_file_path, 'w') as config_file:
            json.dump(config_data, config_file, indent=2)
        logger.info("File config.json creato con successo nella directory del progetto.")
    
    # Scrivi i dati nel file config.json se il file non esiste già
    if not path.exists(word_category_file_path):
        with open(word_category_file_path, 'w') as word_category_file:
            json.dump(word_category_data, word_category_file, indent=4)
        logger.info("File config.json creato con successo nella directory del progetto.")
    else:
        with open(word_category_file_path, 'r') as json_file:
            loaded_data = json.load(json_file)
        # Ottieni una lista dei tipi
        are_all_lists = all(isinstance(value, list) for value in loaded_data.values())
        if(are_all_lists):
            replace_keywords(word_category_file_path, word_category_file_path, logger)
    
    # # Carica il contenuto del file word_category.json
    # with open(word_category_file_path, 'r') as word_category_file:
    #     word_category_data = json.load(word_category_file)

    logger.info(f"File config.json aggiornato con successo nella directory del progetto.")
    logger.info("Categorie aggiunte al file config_data.")

def clear_screen():
    system('clear' if name == 'posix' else 'cls')

def help_message():
    return "--------- HELP ----------\nComandi:\tTaSK, Movement + option\n\t\tConfig, Help\n\nEx1: task add\nEx2: tsk a\nEx3: config"

def error_message():
    return "##### Usa help per visualizzare i comandi #####"

def start_message():
    return "##### Benvenuto su ToDo #####"

def process_csv_file(file_path):
    # Leggi il file CSV e prepara la struttura per l'inserimento nel database
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        first_row = next(csv_reader)
        saldo_data = first_row[1]
        saldo = first_row[2]
        data = [row for row in csv_reader][2:]

        return (data, saldo_data, saldo)

def update_word_category_format(input_path, output_path, logger):
    # Leggi il contenuto attuale del file word_category.json
    with open(input_path, 'r') as input_file:
        word_category_data = json.load(input_file)

    # Modifica il formato delle categorie
    updated_word_category_data = {}
    for category, data in word_category_data.items():
        if isinstance(data, dict):
            updated_data = {
                "keywords": data.get("keywords", []),
                "min_entry": data.get("min_entry", -1),
                "max_expense": data.get("max_expense", -1)
            }
        elif isinstance(data, list):
            updated_data = {
                "keywords": data,
                "min_entry": -1,
                "max_expense": -1
            }
        else:
            logger.info(f"Formato non valido per la categoria {category}.")
            continue

        updated_word_category_data[category] = updated_data

    # Scrivi il nuovo formato nel file output_path
    with open(output_path, 'w') as output_file:
        json.dump(updated_word_category_data, output_file, indent=4)

    logger.info(f"File {output_path} creato con successo nel nuovo formato.")

def replace_keywords(input_path, output_path, logger):
    with open(input_path, 'r') as input_file:
        word_category_data = json.load(input_file)
        for category, data in word_category_data.items():
            word_category_data[category] = data
        # Scrivi il nuovo formato nel file output_path
        with open(output_path, 'w') as output_file:
            json.dump(word_category_data, output_file, indent=4)

        logger.info(f"File {output_path} creato con successo nel nuovo formato.")
        update_word_category_format(output_path, output_path, logger)
