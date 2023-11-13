# pocket.py
from movement import Movement
from os import system
from db import connect_db, add_movement, get_all_movements, delete_movement
class Pocket:
    def __init__(self, db_path):
        self.conn = connect_db(db_path)
        self.movements = get_all_movements(self.conn)
        print(self.movements)

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
        
        mv_to_show = self.movements[(page - 1) * num_for_page : page * num_for_page]
        print(f"{mv_to_show}")

        print("{:<3} {:<30} {:<10} {:<10} {:<10} {:<15}".format("ID", "Nome", "Data", "Categoria", "Cifra", "Tipologia"))
        for movement in mv_to_show:
            print("{:<3} {:<30} {:<10} {:<10} {:<10} {:<15}".format(movement.id, movement.name[:30], movement.data_contabile, movement.category, movement.amount, movement.type))
