# pocket.py
from movement import Movement
from os import system
from db import connect_db, add_movement, get_all_movements
class Pocket:
    def __init__(self):
        self.conn = connect_db()
        self.movements = get_all_movements(self.conn)
        print(self.movements)

    def aggiungi_movement(self, nome, data, category, amount, type):
        movement = Movement(nome, data, category, amount, type)
        add_movement(self.conn, movement)
        self.movements = get_all_movements(self.conn)

    def mostra_movement(self):
        #movements = get_all_movements(self.conn)
        if not self.movements:
            print(f"La lista delle attivita' e' vuota {self.movements}.")
            return

        print("{:<3} {:<30} {:<10} {:<10} {:<10} {:<15}".format("ID", "Nome", "Data", "Categoria", "Cifra", "Tipologia"))
        for movement in self.movements:
            print("{:<3} {:<30} {:<10} {:<10}".format(movement.id, movement.name[:30], movement.date, movement.category))
