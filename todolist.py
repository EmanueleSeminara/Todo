# todolist.py
from task import Task
from os import system
from db import connect_db, add_task, get_all_tasks, delete_task, edit_task, get_task
from datetime import datetime

class TodoList:
    def __init__(self, db_path):
        self.conn = connect_db(db_path)
        self.tasks = get_all_tasks(self.conn)
        print(self.tasks)

    def aggiungi_task(self, nome, data, category):
        data = datetime.strptime(data, "%Y-%m-%d")
        print(data)
        
        task = Task(nome, data, category)
        add_task(self.conn, task)
        self.tasks = get_all_tasks(self.conn)

    def mostra_task(self):
        if not self.tasks:
            print(f"La lista delle attivita' e' vuota {self.tasks}.")
            return

        print("{:<3} {:<40} {:<8} {:<15}".format("ID", "Nome", "Data", "Categoria"))
        for task in self.tasks:
            print("{:<3} {:<40} {:<8} {:<15}".format(task.id, task.name[:30], task.date.strftime('%d/%m'), task.category))

    def remove_task(self, id):
        delete_task(self.conn,  id)
        self.tasks = get_all_tasks(self.conn)

    def mod_task(self, task_id, edited_task):
        edited_task.set_id(task_id)
        edit_task(self.conn, edited_task)
        self.tasks = get_all_tasks(self.conn)


    def mostra_tasks_page(self, page, num_for_page = 3):
        
        tasks_to_show = self.tasks[(page - 1) * num_for_page : page * num_for_page]
        print(f"{tasks_to_show}")

        print("{:<3} {:<40} {:<8} {:<15}".format("ID", "Nome", "Data", "Categoria"))
        for task in tasks_to_show:
            print("{:<3} {:<40} {:<8} {:<15}".format(task.id, task.name[:30], task.date.strftime('%d/%m'), task.category))