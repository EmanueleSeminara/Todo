import csv
import os

def process_csv_file(file_path):
    # Leggi il file CSV e prepara la struttura per l'inserimento nel database
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        first_row = next(csv_reader)
        saldo_data = first_row[1]
        saldo = first_row[2]
        data = [row for row in csv_reader][2:]

        return (data, saldo_data, saldo)

def rimuovi_vecchio_db(old_db_path):
    try:
        os.remove(old_db_path)
        print(f"File {old_db_path} rimosso con successo.")
    except FileNotFoundError:
        print(f"File {old_db_path} non trovato.")
    except Exception as e:
        print(f"Si è verificato un errore durante la rimozione del file: {str(e)}")