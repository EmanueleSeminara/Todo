# category.py

class Category:
    def __init__(self, name):
        self.name = name


    def set_id(self, id):
        self.id = id

    def __str__(self):
        return f"{self.name}"