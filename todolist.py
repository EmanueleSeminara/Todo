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

def main():
    todo_list = TodoList()

    while True:
        #system("clear")
        print("\n1. Aggiungi Task")
        print("2. Mostra Task")
        print("3. Rimuovi Task")
        print("4. Modifica Task")
        print("0. Esci")

        scelta = input("Scegli un'opzione: ")
        #system("clear")
        if(scelta == "1"):
            nome = input("Nome: ")
            data = input("Data:: ")
            category = input("Categoria: ")
            todo_list.aggiungi_task(nome, data, category)
            print("Task aggiunto con successo!")
            input()
        elif(scelta == "2"):
            system("clear")
            todo_list.mostra_task()
            #input()
        elif(scelta == "3"):
            task_id = input("Inserire l'id del task da rimuovere: ")
            todo_list.remove_task(task_id)
        elif(scelta == "4"):
            task_id = input("Inserire l'id del task da modificare: ")
            task_name = input("Nome: ")
            task_date = input("Data: ")
            task_category = input("Categoria: ")
            
            new_task = Task(task_name, task_date, task_category)
            new_task.set_id(task_id)
            todo_list.mod_task(task_id, new_task)
        elif(scelta == "0"):
             break

        else:
             print("Scelta non valida, Riprova.")

        if(__name__ == "__main__"):
             main()
