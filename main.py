# main.py
from todolist import TodoList
from os import system
from task import Task
from db import get_task, connect_db

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
            task_id = input("Id del task da modificare: ")
            system("clear")
            conn = connect_db()
            old_task = get_task(conn, task_id)
            print("----- Task in modifica ------")
            print(f"ID: {task_id}\nNome: {old_task.name}\nCategoria: {old_task.category}\nData: {old_task.date}\n\n")
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
