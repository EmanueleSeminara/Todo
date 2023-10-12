# main.py
from todolist import TodoList
from os import system
from task import Task
from db import get_task, connect_db

def main():
    todo_list = TodoList()

    while True:
        #system("clear")
        print("\n[A]dd [L]ist [S]elect [R]emove [E]dit [EX]it/n> ")

        scelta = input("\nScegli un'opzione: ")
        #system("clear")
        if(scelta.upper() == "A" or scelta.upper() == "ADD"):
            system("clear")
            print("----- Aggiunta nuovo task ------")
            nome = input("Nome: ")
            data = input("Data:: ")
            category = input("Categoria: ")
            todo_list.aggiungi_task(nome, data, category)
            print("Task aggiunto con successo!")
            input()
        elif(scelta.upper() == "L" or scelta.upper() == "LISTA"):
            system("clear")
            todo_list.mostra_task()
            #input()
        elif(scelta == "S" or scelta.upper() == "SELECT"):
            task_id = input("Task id: ")
            system("clear")
            print("----- Task in visualizzazione ------")
            conn = connect_db()
            task_to_show = get_task(conn, task_id)
            print(f"ID: {task_id}\nNome: {task_to_show.name}\nCategoria: {task_to_show.category}\nData: {task_to_show.date}\n\n")
            input()
        elif(scelta.upper() == "R" or scelta.upper() == "REMOVE"):
            task_id = input("Inserire l'id del task da rimuovere: ")
            todo_list.remove_task(task_id)
        elif(scelta.upper() == "E" or scelta.upper() == "EDIT"):
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
        elif(scelta.upper() == "EX" or scelta.upper() == "EXIT"):
             break

        else:
             print("Scelta non valida, Riprova.")


if(__name__ == "__main__"):
    main()
