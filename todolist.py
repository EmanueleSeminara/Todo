# todolist.py
from task import Task
from os import system
from db import connect_db, add_task, get_all_tasks, delete_task, edit_task, get_task

class TodoList:
    def __init__(self):
        self.conn = connect_db()
        self.tasks = get_all_tasks(self.conn)

    def aggiungi_task(self, nome, data, category):
        task = Task(nome, data, category)
        add_task(self.conn, task)
        self.tasks = get_all_tasks(self.conn)

    def mostra_task(self):
        #tasks = get_all_tasks(self.conn)
        if not self.tasks:
            print("La lista delle attivita' e' vuota.")
            return

        print("{:<3} {:<30} {:<10} {:<10}".format("ID", "Nome", "Data", "Categoria"))
        for task in self.tasks:
            print("{:<3} {:<30} {:<10} {:<10}".format(task.id, task.name[:30], task.date, task.category))

    def remove_task(self, id):
        delete_task(self.conn,  id)
        self.tasks = get_all_tasks(self.conn)

    def mod_task(self, task_id, edited_task):
        print(f"{edited_task} - {task_id}")
        old_task = get_task(self.conn, task_id)
        edited_task.set_id(task_id)
        edit_task(self.conn, edited_task)
        self.tasks = get_all_tasks(self.conn)


