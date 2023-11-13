# todolist.py
from task import Task
from os import system
from db import connect_db, add_task, get_all_tasks, delete_task, edit_task, get_task
from datetime import datetime
import json


class TodoList:
    def __init__(self, db_path):
        self.conn = connect_db(db_path)
        self.tasks = get_all_tasks(self.conn)
        print(self.tasks)
        # Nome del file JSON
        file_path = "config.json"

        # Leggi il file JSON
        with open(file_path, "r") as json_file:
            data = json.load(json_file)

        # Estrai la costante
        TASKS_RECORD_PAGE = data.get("TASKS_RECORD_PAGE")
        self.recordPageNumber = TASKS_RECORD_PAGE

        # Stampa la costante
        print("TASKS_RECORD_PAGE:", TASKS_RECORD_PAGE)

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
        num_for_page = int(self.recordPageNumber)
        j = int(page) * int(num_for_page)
        page = int(page - 1)
        i = page if page == 0 else page * num_for_page
        i = int(i)
        task_to_show = self.tasks[i : j]
        
        print("------------------------------------------------------------------------------------")
        print("| {:<3}|{:<40}|{:<12}|{:<22} |".format("ID", "Nome", "Data", "Categoria"))
        print("------------------------------------------------------------------------------------")
        for task in task_to_show:
            print(isinstance(task.date, str))
            print("| {:<3}|{:<40}|{:<12}|{:<22} |".format(task.id, task.name[:30], task.date if isinstance(task.date, str) else task.date.strftime('%d%m'), task.category))
        print("------------------------------------------------------------------------------------")
        print(len(self.tasks))
    def setRecordPage(self, tasks_record_number):
        # Nome del file JSON
        file_path = "config.json"

        # Leggi il file JSON
        with open(file_path, "r") as json_file:
            data = json.load(json_file)

        # Modifica la costante
        data["TASKS_RECORD_PAGE"] = tasks_record_number  # Modifica il valore secondo le tue esigenze
        self.recordPageNumber = tasks_record_number
        # Scrivi il file JSON aggiornato
        with open(file_path, "w") as json_file:
            json.dump(data, json_file, indent=2)

        print("File JSON aggiornato con successo.")
