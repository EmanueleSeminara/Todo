# task.py
from datetime import datetime

class Task:
    def __init__(self, name, date, category):
        self.name = name
        print(date)
        self.date = date if date is not None else None
        self.category = int(category) if category is not None else None

    def set_id(self, id):
        self.id = id

    def __str__(self):
        return f"{self.name} {self.date} {self.category}"