# movement.py

class Movement:
    def __init__(self, name, date, category, amount, mv_type):
        self.name = name
        self.date = date
        self.category = category
        self.amount = amount
        self.type = mv_type

    def set_id(self, id):
        self.id = id
