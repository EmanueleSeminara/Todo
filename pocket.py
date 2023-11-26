# pocket.py
from movement import Movement
from os import system
from db import connect_db, add_movement, get_all_movements, delete_movement, get_all_categories, clean_movements, clean_movements_files
import json
from math import ceil


class Pocket:
    def __init__(self, db_path):
        self.conn = connect_db(db_path)
        self.movements = get_all_movements(self.conn)
        self.categories = get_all_categories(self.conn)
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
        #print(f"{data_contabile} - {amount}")
        movement = Movement(nome, data_contabile, data_valuta, causale_abi, descrizione, category, amount, mv_type)
        #print(movement.amount)
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
        if not self.movements:
            print(f"La lista dei movimenti e' vuota {self.movements}.")
            return
        num_for_page = int(self.recordPageNumber)
        if(page > ceil(len(self.movements)/num_for_page)):
            print(f"Pagina richiesta non presente.")
            return
        j = int(page) * int(num_for_page)
        page = int(page - 1)
        i = page if page == 0 else page * num_for_page
        i = int(i)
        sorted_movements = sorted(self.movements, key=lambda x: x.data_contabile)

        amount_sum = sum(
            float(movement.amount.replace('.', '').replace(',', '.')) 
            if movement and movement.amount 
            else 0
            for movement in self.movements
        )


        mv_to_show = sorted_movements[i : j]
        
        print("{:<131}".format("-" * 131))
        print("| {:^3} | {:^30} | {:^17} | {:^17} | {:^15} | {:^12} | {:^15} |".format("ID", "Nome", "Data contabile", "data_valuta", "Categoria", "Cifra", "Tipologia"))
        print("{:<131}".format("-" * 131))
        for movement in mv_to_show:
            print("| {:^3} | {:^30} | {:^17} | {:^17} | {:^15} | {:^12} | {:^15} |".format(movement.id, movement.name[:30], movement.data_contabile, movement.data_valuta, movement.category, movement.amount, movement.type))
            
        print("{:<131}".format("-" * 131))
        print("| {:<42}{:^43}{:>42} |".format(f"TOT: {len(self.movements)}", "Pagina " + str(page + 1) + " di " + str(ceil(len(self.movements)/num_for_page)), "SOMMA MOVIMENTI: {:.2f}".format(amount_sum)))
        print("{:<131}".format("-" * 131))

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

    def get_categories(self):
        return self.categories

    def clean_all(self):
        clean_movements(self.conn)
        clean_movements_files(self.conn)
        self.movements = []