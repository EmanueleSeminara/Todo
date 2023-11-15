# pocket.py
from movement import Movement
from os import system
from db import connect_db, add_movement, get_all_movements, delete_movement, get_all_categories
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
        print(f"{data_contabile} - {amount}")
        movement = Movement(nome, data_contabile, data_valuta, causale_abi, descrizione, category, amount, mv_type)
        print(movement.amount)
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
        j = int(page) * int(num_for_page)
        page = int(page - 1)
        i = page if page == 0 else page * num_for_page
        i = int(i)
        mv_to_show = self.movements[i : j]

        sorted_tasks = sorted(mv_to_show, key=lambda x: x.data_contabile)
        amount_sum = sum(float(task.amount.replace('.', '').replace(',', '.')) for task in self.movements)
        
        print("--------------------------------------------------------------------------------------------------------------------")
        print("| {:<3} | {:<30} | {:<17} | {:<17} | {:<15} | {:<12} | {:<15} |".format("ID", "Nome", "Data contabile", "data_valuta", "Categoria", "Cifra", "Tipologia"))
        print("--------------------------------------------------------------------------------------------------------------------")
        for movement in sorted_tasks:
            print("| {:<3} | {:<30} | {:<17} | {:<17} | {:<15} | {:<12} | {:<15} |".format(movement.id, movement.name[:30], movement.data_contabile, movement.data_valuta, movement.category, movement.amount, movement.type))
            
           # print(f"Name: {movement.name}\namount: {movement.amount}\nid: {movement.id}\ndata contabile: {movement.data_contabile}\ndata valuta:{movement.data_valuta}\ncategory: {movement.category}\ntype: {movement.type}")
        print("--------------------------------------------------------------------------------------------------------------------")
        print("| {:<3}{:<30} | {:<17} | {:<17} | {:<15} | {:<12} | {:<15} |".format("TOT:", len(self.movements), "-----------", "--------", "-----", "{:.2f}".format(amount_sum), str(page + 1) + " di " + str(ceil(len(self.movements)/num_for_page))))


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
