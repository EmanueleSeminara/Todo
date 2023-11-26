# todolist.py
from task import Task
from os import system
from db import connect_db, add_task, get_all_tasks, delete_task, edit_task, get_task, get_all_categories, clean_tasks
from datetime import datetime
import json
from math import ceil
from category import Category


class TodoList:
    def __init__(self, db_path):
        self.conn = connect_db(db_path)
        self.tasks = get_all_tasks(self.conn)
        self.categories = get_all_categories(self.conn)
        self.months_dict = {
                                1: 'Gennaio',
                                2: 'Febbraio',
                                3: 'Marzo',
                                4: 'Aprile',
                                5: 'Maggio',
                                6: 'Giugno',
                                7: 'Luglio',
                                8: 'Agosto',
                                9: 'Settembre',
                                10: 'Ottobre',
                                11: 'Novembre',
                                12: 'Dicembre'
                            }
        #print(self.tasks)
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

    def aggiungi_task(self, nome, data, category_id):
        data = datetime.strptime(data, "%d/%m/%Y")
        print(data)
        
        task = Task(nome, data, category_id)
        print(task)
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
        if not self.tasks:
            print(f"La lista delle attivita' e' vuota {self.tasks}.")
            return
        num_for_page = int(self.recordPageNumber)
        if(page > ceil(len(self.tasks)/num_for_page)):
            print(f"Pagina richiesta non presente.")
            return
        
        j = int(page) * int(num_for_page)
        page = int(page - 1)
        i = page if page == 0 else page * num_for_page
        i = int(i)

        sorted_tasks = sorted(self.tasks, key=lambda x: x.date)

        task_to_show = sorted_tasks[i : j]
        
        print("{:<135}".format("-" * 135))
        print("| {:^3} | {:^80} | {:^17} | {:^22} |".format("ID", "Nome", "Data", "Categoria"))
        print("{:<135}".format("-" * 135))
        for task in task_to_show:
            category_name = next((category_item.name for category_item in self.categories if category_item.id == task.category), "")
            task_id = task.id if task.id is not None else ""
            task_name = task.name if task.name is not None else ""
            #task_date = task.date.strftime('%d%m') if isinstance(task.date, str) else task.date.strftime('%d%m') if task.date is not None else ""
            if task.date:
                if isinstance(task.date, datetime):
                    task_date = f"{task.date.strftime('%d')} {self.months_dict[int(task.date.strftime('%m'))]} {task.date.strftime('%y')}"
                else:
                    task_date = task.date
            else:
                task_date = ""


            print("| {:^3} | {:^80} | {:^17} | {:^22} |".format(task_id, task_name, task_date, category_name))
        print("{:<135}".format("-" * 135))
        print("| {:<44}{:^44}{:>43} |".format(f"TOT: {len(self.tasks)}", "Pagina " + str(page + 1) + " di " + str(ceil(len(self.tasks)/num_for_page)), ""))
        print("{:<135}".format("-" * 135))

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

    def clean_all(self):
        clean_tasks(self.conn)
        self.tasks = []
    
    def get_task(self, task_id):
        return get_task(self.conn, task_id)