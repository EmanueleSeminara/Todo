# account.py

class Account:
    def __init__(self, name, type, saldo, data_saldo, id=None):
        self.name = name
        self.type = type
        self.saldo = saldo
        self.data_saldo = data_saldo
        self.id = id

    def set_id(self, id):
        self.id = id

    def __str__(self):
        return f"{self.name}"
