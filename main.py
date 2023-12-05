# main.py
from todolist import TodoList
from pocket import Pocket
from os import system, name
from models.task import Task
from db import db, categories
from utils import rimuovi_vecchio_db, start, clear_screen, start_message, error_message, process_directory, help_message, check_basic_folder
from datetime import datetime
from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory
import logging
from logging.handlers import TimedRotatingFileHandler


def main():
    check_basic_folder()

    # Configura il logger
    logger = configure_logger()

    start(logger)

    logger.info("-------- Avvio ToDo --------")

    # Configurazione del percorso del file di log
    log_file_path = f'log/logTodo_{(datetime.now().strftime("%d_%m_%Y"))}.log'

    db_path = "db/todo.db"
    db_temp_path = "temp/temp.dp"
    logger.info(f"db path: {db_path} - db temp path: {db_temp_path}")

    db.connect_db(db_temp_path)
    logger.info(f"Connesso al db temp")

    old_db_path = db_path
    new_db_path = db_temp_path
    db.confronta_e_aggiorna(old_db_path, new_db_path)
    rimuovi_vecchio_db(new_db_path, logger)

    categories.create_default_category(db.connect_db(db_path))

    todo_list = TodoList(db_path)
    pocket = Pocket(db_path)
    first = True
    history = InMemoryHistory()

    while True:
        if first:
            clear_screen()
            print(start_message())
            first = False

        print("\nOption: [A]dd [L]ist [S]elect [R]emove [E]dit [H]elp [EX]it")
        scelta = prompt('> ', history=history).upper().split()
        tipo = ""
        number_page = -1
        month_stats = -1

        if len(scelta) == 0:
            print(error_message())
            continue
        if len(scelta) == 2:
            tipo = scelta[0]
            scelta = scelta[1]
        elif len(scelta) == 3:
            tipo = scelta[0]
            number_page = int(scelta[2])
            scelta = scelta[1]
        elif len(scelta) == 4:
            month_stats = scelta[3]
            tipo = scelta[0]
            number_page = int(scelta[2])
            scelta = scelta[1]

        if scelta[0] in ("H", "HELP"):
            clear_screen()
            print(help_message())
            continue
        elif scelta[0] in ("EX", "EXIT"):
            break
        elif scelta[0] in ("C", "CONFIG"):
            handle_config(logger, pocket, todo_list)
        elif tipo in ("TSK", "TASK"):
            handle_task_operations(scelta, number_page, todo_list)
        elif tipo in ("MV", "MOVEMENT"):
            handle_movement_operations(scelta, number_page, month_stats, pocket)
        else:
            clear_screen()
            print(error_message())

def configure_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Crea un gestore di log per scrivere su un file di log rotante
    log_file_path = f'log/logTodo_{(datetime.now().strftime("%d_%m_%Y"))}.log'
    handler = TimedRotatingFileHandler(log_file_path, when="midnight", interval=1, backupCount=7)
    handler.setLevel(logging.DEBUG)

    # Formattazione dei log
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Aggiungi il gestore al logger
    logger.addHandler(handler)

    return logger

def handle_config(logger, pocket, todo_list):
    clear_screen()
    print("--------- CONFIG ----------")
    print("1. Record per pagina Movimenti")
    print("2. Record per pagina Tasks")
    print("3. Importa transazioni")
    print("4. Pulisci movimenti")
    print("5. Pulisci task")

    scelta = input("> ").upper()
    if scelta in ("EX", "EXIT"):
        return

    if scelta == "1":
        handle_config_record_page(pocket)
    elif scelta == "2":
        handle_config_record_page(todo_list)
    elif scelta == "3":
        handle_import_transactions(logger, pocket)
    elif scelta == "4":
        handle_clean_movements(logger, pocket)
    elif scelta == "5":
        handle_clean_tasks(logger, todo_list)

def handle_config_record_page(obj):
    clear_screen()
    print(f"Valore attuale: {obj.record_page_number}")
    num = input("Inserisci record per pagina: ")
    if num in ("EX", "EXIT"):
        return
    obj.setRecordPage(num)

def handle_import_transactions(logger, pocket):
    path = "./csv"
    directory_path = path
    movements, saldo_data, saldo = process_directory(directory_path, logger)
    if movements:
        header = movements[0]
        movements = movements[1:]
        for row_movements in movements:
            pocket.aggiungi_movement("", row_movements[0], row_movements[1], row_movements[2], row_movements[3], "", row_movements[4], "")

def handle_clean_movements(logger, pocket):
    confirm = input("Sei sicuro di voler eliminare tutti i movimenti: ")
    if confirm in ("EX", "EXIT"):
        return
    if confirm.upper() in ("Y", "YES"):
        pocket.clean_all()

def handle_clean_tasks(logger, todo_list):
    confirm = input("Sei sicuro di voler eliminare tutti i tasks: ")
    if confirm in ("EX", "EXIT"):
        return
    if confirm.upper() in ("Y", "YES"):
        todo_list.clean_all()

def handle_task_operations(scelta, number_page, todo_list):
    if scelta in ("A", "ADD"):
        handle_add_task(todo_list)
    elif (scelta == "L" or scelta == "LIST") and number_page > 0:
        clear_screen()
        todo_list.mostra_tasks_page(int(number_page))
    elif scelta == "L" or scelta == "LIST":
        clear_screen()
        todo_list.mostra_task()
    elif scelta in ("S", "SELECT") and number_page > 0:
        handle_view_task(todo_list, number_page)
    elif scelta == "R" or scelta == "REMOVE":
        handle_remove_task(todo_list)
    elif scelta in ("E", "EDIT") and number_page > 0:
        handle_edit_task(todo_list, number_page)

def handle_add_task(todo_list):
    clear_screen()
    print("----- Aggiunta nuovo task ------")
    nome = input("Nome: ")
    data = input("Data: ")
    data = datetime.strptime(data, "%d/%m/%Y")
    if data < datetime.now():
        input_past_date = input("Data nel passato, confermare: ").upper()
        if input_past_date in ("N", "NO"):
            return
    print(*todo_list.categories)
    category_input = input("Categoria: ")
    found_category = next((category for category in todo_list.categories if category_input.upper() == category.name.upper()), None)
    if found_category:
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

def handle_view_task(todo_list, number_page):
    clear_screen()
    print(f"----- VISUALIZZAZIONE TASK ID {number_page} ------")
    task_to_show = todo_list.get_task(number_page)
    real_category = next((category for category in todo_list.categories if task_to_show.category == category.id), None)
    real_date = f"{task_to_show.date.strftime('%d')} {todo_list.months_dict[int(task_to_show.date.strftime('%m'))]} {task_to_show.date.strftime('%y')}"
    print(f"ID: {task_to_show.id}\nNome: {task_to_show.name}\nCategoria: {real_category}\nData: {real_date}\n\n")

def handle_remove_task(todo_list):
    task_id = input("Inserire l'id del task da rimuovere: ")
    todo_list.remove_task(task_id)

def handle_edit_task(todo_list, number_page):
    clear_screen()
    old_task = todo_list.get_task(number_page)
    if old_task is not None:
        real_category = next((category for category in todo_list.categories if old_task.category == category.id), None)
        real_date = f"{old_task.date.strftime('%d')} {todo_list.months_dict[int(old_task.date.strftime('%m'))]} {old_task.date.strftime('%y')}"
        print(f"----- MODIFICA TASK ID {number_page} -----")
        print(f"ID: {number_page}\nNome: {old_task.name}\nCategoria: {real_category}\nData: {real_date}\n\n")
        print(f"Seleziona cosa modificare:\n1. Nome\n2. Categoria\n3. Data\n")

        resp = input("> ")
        if resp == '1':
            task_name = input("Nome: ")
            new_task = Task(task_name, old_task.date, old_task.category)
        elif resp == '2':
            handle_edit_task_category(todo_list, old_task)
        elif resp == '3':
            task_date = input("Data: ")
            task_date = datetime.strptime(task_date, "%d/%m/%Y")
            new_task = Task(old_task.name, task_date, old_task.category)

        new_task.set_id(number_page)
        todo_list.mod_task(number_page, new_task)

def handle_edit_task_category(todo_list, old_task):
    print(*todo_list.categories)
    category_input = input("Categoria: ")
    found_category = next((category for category in todo_list.categories if category_input.upper() == category.name.upper()), None)
    if found_category:
        category_id = found_category.id
        print(f"La variabile '{category_input}' è contenuta nella lista di oggetti. ID della categoria: {category_id}")
    else:
        category_id = None
        print(f"La variabile '{category_input}' non è contenuta nella lista di oggetti.")
        # prevedere aggiunta nuova categoria se non presente
    new_task = Task(old_task.name, old_task.date, category_id)

def handle_movement_operations(scelta, number_page, month_stats, pocket):
    if scelta in ("A", "ADD"):
        handle_add_movement(pocket)
    elif (scelta == "L" or scelta == "LIST") and number_page > 0:
        clear_screen()
        pocket.mostra_movements_page(int(number_page))
    elif scelta == "L" or scelta == "LIST":
        clear_screen()
        pocket.mostra_movement()
        input()
    elif scelta in ("R", "REMOVE"):
        handle_remove_movement(pocket)
    elif scelta in ("S", "STATS"):
        handle_stats_movement(number_page, month_stats, pocket)

def handle_add_movement(pocket):
    clear_screen()
    print("----- Aggiunta nuovo movement ------")
    nome = input("Nome: ")
    data = input("Data:: ")
    category = input("Categoria: ")
    cifra = input("Cifra: ")
    tipologia = input("Tipologia: ")
    pocket.aggiungi_movement(nome, data, data, "", "", category, cifra, tipologia)
    print("Movimento aggiunto con successo!")
    input()
    clear_screen()

def handle_remove_movement(pocket):
    mv_id = input("ID del movimento da RIMUOVERE: ")
    pocket.remove_movement(mv_id)

def handle_stats_movement(number_page, month_stats, pocket):
    if number_page == -1:
        number_page = datetime.now().year
        pocket.stats_movements(number_page, month_stats)
    elif int(number_page) in [2023] and int(month_stats) in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]:
        pocket.stats_movements(number_page, month_stats)

if(__name__ == "__main__"):
    main()