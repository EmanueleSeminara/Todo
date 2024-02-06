# main.py
from todolist import TodoList
from pocket import Pocket
from os import system, name
from models.task import Task
from db import db, categories
from utils import (
    rimuovi_vecchio_db, start, clear_screen, start_message,
    error_message, process_directory, help_message,
    check_basic_folder
)
from datetime import datetime
from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory
import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from data import *

# Import tkinter modules selectively
from tkinter import (
    Tk, Canvas, Entry, Text, Button, PhotoImage, ttk, 
    messagebox, simpledialog, Toplevel
)


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
    
    window.mainloop()


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

# INIZIO INTERFACCIA GRAFICA

def ricarica_tabella():
    print("RICARICA TABELLA")
    # Pulisci la tabella
    print(table.get_children())
    for row in table.get_children():
        print(row)
        table.delete(row)

    # Ottieni i nuovi dati e inseriscili nella tabella
    print(todo_list.mostra_task()[-1])
    for row_data in todo_list.mostra_task():
        line = [row_data.id, row_data.name, row_data.date]
        table.insert(parent="", index="end", values=line)

def add_task():
    task_name = simpledialog.askstring("Aggiungi Task", "Inserisci un nuovo task:")
    if task_name:
        category = simpledialog.askstring("Aggiungi Task", "Inserisci la categoria:")
        due_date = simpledialog.askstring("Aggiungi Task", "Inserisci la data (formato: DD/MM/YYYY):")

        if due_date:
            try:
                due_date = datetime.strptime(due_date, "%d/%m/%Y")
            except ValueError:
                messagebox.showerror("Errore", "Formato data non valido. Utilizza il formato YYYY-MM-DD.")
                return

        task = {"name": task_name, "category": category, "due_date": due_date}
        # self.tasks.append(task)
        # self.refresh_listbox()
    #data = datetime.strptime(data, "%d/%m/%Y")
    # if data < datetime.now():
    #     input_past_date = input("Data nel passato, confermare: ").upper()
    #     if input_past_date in ("N", "NO"):
    #         return
    category_input = category
    db_path = "db/todo.db"
    todo_list = TodoList(db_path)
    found_category = next((category for category in todo_list.categories if category_input.upper() == category.name.upper()), None)
    if found_category:
        category_id = found_category.id
        print(f"La variabile '{category_input}' è contenuta nella lista di oggetti. ID della categoria: {category_id}")
    else:
        category_id = None
        print(f"La variabile '{category_input}' non è contenuta nella lista di oggetti.")
        # prevedere aggiunta nuova categoria se non presente
    todo_list.aggiungi_task(task_name, due_date, category_id)
    print("Task aggiunto con successo!")
    ricarica_tabella()

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/home/zifro/git/Tkinter-Designer/build/assets/frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("862x480")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 480,
    width = 862,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    0.0,
    0.0,
    862.0,
    74.0,
    fill="#2C41B1",
    outline="")

canvas.create_text(
    57.0,
    19.0,
    anchor="nw",
    text="Dashboard",
    fill="#FFFFFF",
    font=("Inter Bold", 30 * -1)
)

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    326.0,
    276.0,
    image=image_image_1
)

# Creating Table

table = ttk.Treeview(master=window, columns=table_columns, show="headings")

width = 0
for column in table_columns:
    print(column)
    if(column.upper() in ("ID")):
        width = 35
    elif(column.upper() in ("NOME")):
        width = 350
    elif(column.upper() in ("DATA")):
        width = 80
    elif(column.upper() in ("CATEGORIA")):
        width = 100
    elif(column.upper() in ("FREQUENZA")):
        width = 30
    else:
        width = 5
    table.heading(column=column, text=column)
    table.column(column=column, width=width)

db_path = "db/todo.db"
todo_list = TodoList(db_path)


for row_data in todo_list.mostra_task():
    line = [row_data.id, row_data.name, row_data.date]
    table.insert(parent="", index="end", values=line)

style = ttk.Style()
style.theme_use("default")
style.configure("Treeview", font=("Arial", 12), background="#917FB3", fieldbackground="#917FB3", foreground="white")
style.configure("Treeview.Heading", background="#917FB3", fieldbackground="#917FB3", foreground="white")
style.map("Treeview", background=[("selected", "#E5BEEC")])

def item_selected(event):
    for selected_item in table.selection():
        item = table.item(selected_item)
        record = item['values']
        print(record)
        # show a message
        # showinfo(title='Information', message=record)

def show_full_info(event):
    for selected_item in table.selection():
        item = table.item(selected_item)
        record = item['values']

        # Creazione di una nuova finestra
        info_window = Toplevel(window)
        info_window.title("Informazioni complete")

        # Aggiungi widget e visualizza le informazioni complete nella nuova finestra
        for col, val in zip(table_columns, record):
            label = ttk.Label(info_window, text=f"{col}: {val}")
            label.pack(padx=10, pady=5)

def complete_task():
    print(table.selection())
    for selected_item in table.selection():
        item = table.item(selected_item)
        record = item['values']
        print(record)
        todo_list.remove_task(record[0])
    

table.bind('<Double-1>', show_full_info)
table.bind('<<TreeviewSelect>>', item_selected)

table.place(x=25, y=100, height=350)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    767.0,
    37.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    819.0,
    37.0,
    image=image_image_3
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    30.0,
    37.0,
    image=image_image_4
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=add_task,
    relief="flat"
)
button_1.place(
    x=655.0,
    y=92.0,
    width=196.0,
    height=56.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=complete_task,
    relief="flat"
)
button_2.place(
    x=655.0,
    y=159.0,
    width=196.0,
    height=56.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat"
)
button_3.place(
    x=655.0,
    y=226.0,
    width=196.0,
    height=56.0
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_4 clicked"),
    relief="flat"
)
button_4.place(
    x=655.0,
    y=293.0,
    width=196.0,
    height=56.0
)

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=ricarica_tabella,
    relief="flat"
)
button_5.place(
    x=655.0,
    y=360.0,
    width=196.0,
    height=56.0
)
window.resizable(False, False)
# FINE INTERFACCIAGRAFICA

if(__name__ == "__main__"):
    main()
    