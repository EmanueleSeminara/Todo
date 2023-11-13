# movement.py

class Movement:
    def __init__(self, nome, data_contabile, data_valuta, causale_abi, descrizione, category, amount, mv_type):
        self.name = nome
        self.data_contabile = data_contabile
        self.data_valuta = data_valuta
        self.causale_abi = causale_abi
        self.descrizione = descrizione
        self.category = category
        self.amount = amount
        self.type = mv_type

    def set_id(self, id):
        self.id = id
