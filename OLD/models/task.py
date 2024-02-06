# task.py
from datetime import datetime

class Task:
    def __init__(self, name, date, category, id=None):
        self.id = id
        self.name = name
        self.date = date if date is not None else None
        try:
            self.category = int(category) if category is not None else None
        except:
            self.category = category

    def set_id(self, id):
        self.id = id

    def __str__(self):
        return f"{self.name} {self.date} {self.category}"