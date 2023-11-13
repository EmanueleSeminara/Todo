# pocket.py
from movement import Movement
from os import system
from db import connect_db, add_movement, get_all_movements, delete_movement
import json

class Pocket:
    def __init__(self, db_path):
        self.conn = connect_db(db_path)
        self.movements = get_all_movements(self.conn)
        print(self.movements)
        # Nome del file JSON
        file_path = "config.json"

        # Leggi il file JSON
        with open(file_path, "r") as json_file:
            data = json.load(json_file)

        # Estrai la costante
        MOVEMENTS_RECORD_PAGE = data.get("MOVEMENTS_RECORD_PAGE")
        self.recordPageNumber = MOVEMENTS_RECORD_PAGE

        # Stampa la costante
        print("MOVEMENTS_RECORD_PAGE:", MOVEMENTS_RECORD_PAGE)

    def aggiungi_movement(self, nome, data_contabile, data_valuta, causale_abi, descrizione, category, amount, mv_type):
        movement = Movement(nome, data_contabile, data_valuta, causale_abi, descrizione, category, amount, mv_type)
        add_movement(self.conn, movement)
        self.movements = get_all_movements(self.conn)

    def mostra_movement(self):
        #movements = get_all_movements(self.conn)
        if not self.movements:
            print(f"La lista delle attivita' e' vuota {self.movements}.")
            return

        print("{:<3} {:<30} {:<10} {:<10} {:<10} {:<15}".format("ID", "Nome", "Data", "Categoria", "Cifra", "Tipologia"))
        for movement in self.movements:
            print("{:<3} {:<30} {:<10} {:<10} {:<10} {:<15}".format(movement.id, movement.name[:30], movement.data_contabile, movement.category, movement.amount, movement.type))

    def remove_movement(self, id):
        delete_movement(self.conn, id)
        self.movements = get_all_movements(self.conn)

    def mostra_movements_page(self, page, num_for_page = 3):
        num_for_page = int(self.recordPageNumber)
        j = int(page) * int(num_for_page)
        page = int(page - 1)
        i = page if page == 0 else page * num_for_page
        i = int(i)
        mv_to_show = self.movements[i : j]
        
        print("--------------------------------------------------------------------------------------------------------------------")
        print("|{:<3}|{:<30}|{:<17}|{:<17}|{:<15}|{:<12}|{:<15}|".format("ID", "Nome", "Data contabile", "data_valuta", "Categoria", "Cifra", "Tipologia"))
        print("--------------------------------------------------------------------------------------------------------------------")
        for movement in mv_to_show:
            print("|{:<3}|{:<30}|{:<17}|{:<17}|{:<15}|{:<12}|{:<15}|".format(movement.id, movement.name[:30], movement.data_contabile, movement.data_valuta, movement.category, movement.amount, movement.type))
        print("--------------------------------------------------------------------------------------------------------------------")

    def setRecordPage(self, movements_record_number):
        # Nome del file JSON
        file_path = "config.json"

        # Leggi il file JSON
        with open(file_path, "r") as json_file:
            data = json.load(json_file)

        # Modifica la costante
        data["MOVEMENTS_RECORD_PAGE"] = movements_record_number  # Modifica il valore secondo le tue esigenze
        self.recordPageNumber = movements_record_number
        # Scrivi il file JSON aggiornato
        with open(file_path, "w") as json_file:
            json.dump(data, json_file, indent=2)

        print("File JSON aggiornato con successo.")
