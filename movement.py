# movement.py

class Movement:
    def __init__(self, name, date, category, amount, type):
        self.name = name
        self.date = date
        self.category = category
        self.amount = amount
        self.type = type

    def set_id(self, id):
        self.id = id
