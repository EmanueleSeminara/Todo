# movement.py

class Movement:
    def __init__(self, nome, data_contabile, data_valuta, causale_abi, descrizione, category, amount, mv_type, account_id, id=None):
        self.id = id
        self.name = nome
        self.data_contabile = data_contabile if data_contabile is not None else None
        self.data_valuta = data_valuta if data_valuta is not None else None
        self.causale_abi = causale_abi
        self.descrizione = descrizione
        self.category = category
        self.amount = str(amount)
        self.type = mv_type
        self.account_id = account_id

    def set_id(self, id):
        self.id = id

    def __str__(self):
        return f"{self.data_contabile} {self.data_valuta} {self.amount} {self.account_id}"