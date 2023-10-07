# task.py

class Task:
    def __init__(self, name, date, category):
        self.name = name
        self.date = date
        self.category = category

    def set_id(self, id):
        self.id = id
