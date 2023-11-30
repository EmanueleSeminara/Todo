# main.py
from todolist import TodoList
from pocket import Pocket
from os import system, name
from task import Task
from db import connect_db, process_directory, confronta_e_aggiorna, add_category, get_category_by_name
from utils import rimuovi_vecchio_db
import os, json
from category import Category
from datetime import datetime
from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory




def start():
    # Ottieni il percorso della directory del progetto
    project_directory = os.getcwd()

    # Crea la cartella 'temp' se non esiste già
    temp_directory = os.path.join(project_directory, 'temp')
    os.makedirs(temp_directory, exist_ok=True)

    # Crea la cartella 'csv' se non esiste già
    csv_directory = os.path.join(project_directory, 'csv')
    os.makedirs(csv_directory, exist_ok=True)

    # Definisci i dati da inserire nel file config.json
    config_data = {
        "MOVEMENTS_RECORD_PAGE": "10",
        "TASKS_RECORD_PAGE": "10"
    }

    # Crea il percorso completo del file config.json
    config_file_path = os.path.join(project_directory, 'config.json')

    # Scrivi i dati nel file config.json se il file non esiste già
    if not os.path.exists(config_file_path):
        with open(config_file_path, 'w') as config_file:
            json.dump(config_data, config_file, indent=2)
        print("File config.json creato con successo nella directory del progetto.")

    print(f"Cartella 'temp' creata con successo nella directory del progetto: {temp_directory}")
    print(f"Cartella 'csv' creata con successo nella directory del progetto: {csv_directory}")

def create_default_category(db_path):
    conn = connect_db(db_path)

    # Verifica se la categoria "Default" è già presente prima di aggiungerla
    existing_category = get_category_by_name(conn, "Default")

    if existing_category is None:
        add_category(conn, Category("Default"))
    else:
        print("La categoria 'Default' è già presente.")

def clear_screen():
    system('clear' if name == 'posix' else 'cls')

def help_message():
    return "--------- HELP ----------\nComandi:\tTaSK, Movement + option\n\t\tConfig, Help\n\nEx1: task add\nEx2: tsk a\nEx3: config"

def error_message():
    return "##### Usa help per visualizzare i comandi #####"

def start_message():
    return "##### Benvenuto su ToDo #####"


def main():
    start()
    db_path = "todo.db"
    db_temp_path = "temp/temp.dp"
    connect_db(db_temp_path)
    old_db_path = db_path
    new_db_path = db_temp_path
    confronta_e_aggiorna(old_db_path, new_db_path)
    rimuovi_vecchio_db(new_db_path)
    create_default_category(db_path)
    todo_list = TodoList(db_path)
    pocket = Pocket(db_path)
    first = True
    history = InMemoryHistory()

    while True:
        if(first):
            clear_screen()
            print(start_message())
            first = False
        print("\nOption: [A]dd [L]ist [S]elect [R]emove [E]dit [H]elp [EX]it")
        scelta = prompt('> ', history=history).upper().split()
        tipo = ""
        number_page = -1

        if(len(scelta) == 0):
            print(error_message())
            continue
        if(len(scelta) == 2):
            tipo = scelta[0]
            scelta = scelta[1]
        elif(len(scelta) == 3):
            tipo = scelta[0]
            number_page = int(scelta[2])
            scelta = scelta[1]

        print(f"Scelta: {scelta} - Tipo: {tipo} - Scelta[0]: {scelta[0]}")
        if(scelta[0] in ("H", "HELP")):
            clear_screen()
            print(help_message())
            continue
        elif(scelta[0] in ("EX", "EXIT")):
            break
        elif(scelta[0] in ("C", "CONFIG")):
            clear_screen()
            print("--------- CONFIG ----------")
            print("1. Record per pagina Movimenti")
            print("2. Record per pagina Tasks")
            print("3. Importa transazioni")
            print("4. Pulisci movimenti")
            print("5. Pulisci task")

            scelta = input("> ").upper()
            if scelta in ("EX", "EXIT") : continue

            if(scelta == "1"):
                print(f"Valore attuale: {movements.recordPageNumber}")
                num = input("Inserisci record per pagina: ")
                if num in ("EX", "EXIT") : continue
                print(num)
                pocket.setRecordPage(num)
            elif(scelta == "2"):
                print(f"Valore attuale: {todo_list.recordPageNumber}")
                num = input("Inserisci record per pagina: ")
                if num in ("EX", "EXIT") : continue
                print(num)
                todo_list.setRecordPage(num)
            elif(scelta == "3"):
                path = "./csv"
                directory_path = path
                conn = connect_db(db_path)
                movements, saldo_data, saldo = process_directory(conn, directory_path)
                if(movements):
                    header = movements[0]
                    movements = movements[1:]
                    for row_movements in movements:
                        pocket.aggiungi_movement("", row_movements[0], row_movements[1], row_movements[2], row_movements[3], "", row_movements[4], "")
            elif(scelta == "4"):
                confirm = input("Sei sicuro di voler eliminare tutti i movimenti: ")
                if confirm in ("EX", "EXIT") : continue
                if(confirm.upper() in ("Y", "YES")):
                    pocket.clean_all()
            elif(scelta == "5"):
                confirm = input("Sei sicuro di voler eliminare tutti i tasks: ")
                if confirm in ("EX", "EXIT") : continue
                if(confirm.upper() in ("Y", "YES")):
                    todo_list.clean_all()
            else:
                continue
        

        elif(tipo in ("TSK", "TASK")):

            if(scelta in ("A", "ADD")):
                clear_screen()
                print("----- Aggiunta nuovo task ------")
                nome = input("Nome: ")
                data = input("Data:: ")
                print(*todo_list.categories)
                category_input = input("Categoria: ")
                found_category = next((category for category in todo_list.categories if category_input.upper() == category.name.upper()), None)
                if(found_category):
                    category_id = found_category.id
                    print(f"La variabile '{category_input}' è contenuta nella lista di oggetti. ID della categoria: {category_id}")
                else:
                    category_id = None
                    print(f"La variabile '{category_input}' non è contenuta nella lista di oggetti.")
                    # prevedere aggiunta nuova categoria se non presente
                todo_list.aggiungi_task(nome, data, category_id)
                print("Task aggiunto con successo!")
                input()
                clear_screen()
            elif((scelta == "L" or scelta == "LIST") and number_page > 0):
                clear_screen()
                todo_list.mostra_tasks_page(int(number_page))
            elif(scelta == "L" or scelta == "LIST"):
                clear_screen()
                print(f"{number_page}")
                todo_list.mostra_task()
                #input()
            elif(scelta in ("S", "SELECT") and number_page > 0):
                clear_screen()
                print(f"----- VISUALIZZAZIONE TASK ID {number_page} ------")
                task_to_show = todo_list.get_task(number_page)
                real_category = next((category for category in todo_list.categories if task_to_show.category == category.id), None)
                real_date = f"{task_to_show.date.strftime('%d')} {todo_list.months_dict[int(task_to_show.date.strftime('%m'))]} {task_to_show.date.strftime('%y')}"
                print(f"ID: {task_to_show.id}\nNome: {task_to_show.name}\nCategoria: {real_category}\nData: {real_date}\n\n")
                #input("Premere invio per tornare al menu'")
            elif(scelta == "R" or scelta == "REMOVE"):
                task_id = input("Inserire l'id del task da rimuovere: ")
                todo_list.remove_task(task_id)
            elif(scelta in ("E", "EDIT") and number_page > 0):
                clear_screen()
                old_task = todo_list.get_task(number_page)
                if(old_task is not None):
                    real_category = next((category for category in todo_list.categories if old_task.category == category.id), None)
                    real_date = f"{old_task.date.strftime('%d')} {todo_list.months_dict[int(old_task.date.strftime('%m'))]} {old_task.date.strftime('%y')}"
                    print(f"----- MODIFICA TASK ID {number_page} -----")
                    print(f"ID: {number_page}\nNome: {old_task.name}\nCategoria: {real_category}\nData: {real_date}\n\n")
                    print(f"Seleziona cosa modificare:\n1. Nome\n2. Categoria\n3. Data\n")
                    
                    resp = input("> ")
                    if(resp == '1'):
                        task_name = input("Nome: ")
                        new_task = Task(task_name, old_task.date, old_task.category)
                    elif(resp == '2'):
                        print(*todo_list.categories)
                        category_input = input("Categoria: ")
                
                        found_category = next((category for category in todo_list.categories if category_input.upper() == category.name.upper()), None)
                        if(found_category):
                            category_id = found_category.id
                            print(f"La variabile '{category_input}' è contenuta nella lista di oggetti. ID della categoria: {category_id}")
                        else:
                            category_id = None
                            print(f"La variabile '{category_input}' non è contenuta nella lista di oggetti.")
                            # prevedere aggiunta nuova categoria se non presente
                        new_task = Task(old_task.name, old_task.date, category_id)
                    elif(resp == '3'):
                        task_date = input("Data: ")
                        task_date = datetime.strptime(task_date, "%d/%m/%Y")
                        new_task = Task(old_task.name, task_date, old_task.category)
                    
                    

                    new_task.set_id(number_page)
                    todo_list.mod_task(number_page, new_task)
            elif(scelta == "E" or scelta == "EDIT"):
                task_id = input("Id del task da modificare: ")
                if task_id in ("EX", "EXIT") : continue
                clear_screen()
                old_task = todo_list.get_task(task_id)
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
            elif((scelta == "L" or scelta == "LIST") and number_page > 0):
                clear_screen()
                pocket.mostra_movements_page(int(number_page))
            elif(scelta == "L" or scelta == "LIST"):
                clear_screen()
                pocket.mostra_movement()
                input()
            elif(scelta in ("R", "REMOVE")):
                mv_id = input("ID del movimento da RIMUOVERE: ")
                pocket.remove_movement(mv_id)
            elif(scelta in ("S", "STATS")):
                if(number_page == -1):
                    number_page = datetime.now().year
                pocket.stats_movements(number_page)
        else:
            clear_screen()
            print(error_message())


if(__name__ == "__main__"):
    main()
