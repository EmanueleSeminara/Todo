# main.py
from todolist import TodoList
from pocket import Pocket
from os import system, name
from task import Task
from db import get_task, connect_db

def clear_screen():
    system('clear' if name == 'posix' else 'cls')

def help_message():
    return "--------- HELP ----------\nComandi:\tTaSK, Movement + option\n\t\tConfig, Help\n\nEx1: task add\nEx2: tsk a\nEx3: config"
def error_message():
    return "##### Usa help per visualizzare i comandi #####"

def main():
    todo_list = TodoList()
    pocket = Pocket()
    first = True

    while True:
        if(first):
            clear_screen()
            first = False
        print("\nOption: [A]dd [L]ist [S]elect [R]emove [E]dit [H]elp [EX]it")
        scelta = input("> ").upper().split()
        tipo = ""

        if(len(scelta) == 0):
            print(error_message())
            continue
        print(len(scelta))
        if(len(scelta) == 2):
            tipo = scelta[0]
            scelta = scelta[1]

        print(f"Scelta: {scelta} - Tipo: {tipo}")
        if(scelta[0] in ("H", "HELP")):
            clear_screen()
            print(help_message())
            continue
        elif(scelta[0] in ("EX", "EXIT")):
            break
        elif(scelta[0] in ("C", "CONFIG")):
            clear_screen()
            print("--------- CONFIG ----------")
            print("1. Record per pagina")
        
        if(tipo in ("TSK", "TASK")):

            if(scelta in ("A", "ADD")):
                clear_screen()
                print("----- Aggiunta nuovo task ------")
                nome = input("Nome: ")
                data = input("Data:: ")
                category = input("Categoria: ")
                todo_list.aggiungi_task(nome, data, category)
                print("Task aggiunto con successo!")
                input()
                clear_screen()
            elif(scelta == "L" or scelta == "LIST"):
                clear_screen()
                todo_list.mostra_task()
                #input()
            elif(scelta == "S" or scelta == "SELECT"):
                task_id = input("Task id: ")
                clear_screen()
                print("----- Task in visualizzazione ------")
                conn = connect_db()
                task_to_show = get_task(conn, task_id)
                print(f"ID: {task_id}\nNome: {task_to_show.name}\nCategoria: {task_to_show.category}\nData: {task_to_show.date}\n\n")
                #input("Premere invio per tornare al menu'")
            elif(scelta == "R" or scelta == "REMOVE"):
                task_id = input("Inserire l'id del task da rimuovere: ")
                todo_list.remove_task(task_id)
            elif(scelta == "E" or scelta == "EDIT"):
                task_id = input("Id del task da modificare: ")
                clear_screen()
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
        elif(tipo in ("MV", "MOVEMENT")):
            if(scelta in ("A", "ADD")):
                clear_screen()
                print("----- Aggiunta nuovo movement ------")
                nome = input("Nome: ")
                data = input("Data:: ")
                category = input("Categoria: ")
                cifra = input("Cifra: ")
                tipologia = input("Tipologia: ")
                pocket.aggiungi_movement(nome, data, category, cifra, tipologia)
                print("Movimento aggiunto con successo!")
                input()
                clear_screen()
            elif(scelta == "L" or scelta == "LIST"):
                clear_screen()
                pocket.mostra_movement()
                #input()
        else:
             print("Scelta non valida, Riprova.")


if(__name__ == "__main__"):
    main()
