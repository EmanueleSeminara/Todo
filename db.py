# db.py
from sqlite3 import connect, PARSE_DECLTYPES, PARSE_COLNAMES
from task import Task
from movement import Movement
from datetime import datetime
import os
from utils import process_csv_file


def connect_db(db_path):
    conn = connect(db_path, detect_types=PARSE_DECLTYPES | PARSE_COLNAMES)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date TIMESTAMP,
            category_id TEXT,
            stato TEXT,
            frequenza TEXT,
            priorita TEXT,
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS movements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            data_contabile TEXT,
            data_valuta TEXT,
            causale_abi TEXT,
            descrizione TEXT,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            type TEXT NOT NULL
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS movements_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT NOT NULL
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS person (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            surname TEXT,
            phone TEXT,
            email TEXT
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS ideas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
        )
    ''')

    return conn

def add_task(conn, task):
    conn.execute("INSERT INTO tasks (name) VALUES (?)", (task.name,))
    conn.commit()

def get_all_tasks(conn):
    cursor = conn.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    result = []
    for task_data in tasks:
        # Converti la data da stringa a oggetto datetime
        # task_date = datetime.strptime(task_data[2], "%Y-%m-%d %h:%m:%s").date()
        task_date = task_data[2]
        print(f"DATA TYPE: {type(task_date)}")

        task = Task(task_data[1], task_date, task_data[3])
        task.set_id(task_data[0])
        result.append(task)
    return result

def delete_task(conn, id):
    conn.execute("DELETE FROM tasks WHERE id=?", (id, ))
    conn.commit()

def edit_task(conn, task):
    conn.execute("UPDATE tasks SET name = ?, date = ?, category = ? WHERE id = ?", (task.name, task.date, task.category, task.id))
    conn.commit()

def get_task(conn, edit_task_id):
    cursor = conn.execute("SELECT * FROM tasks WHERE id = ?", (edit_task_id,))
    task_data = cursor.fetchone()
    result = Task(task_data[1], task_data[2], task_data[3])
    result.set_id(edit_task_id)
    return result

# MOVEMENTS
def add_movement(conn, movement):
    #print(f"{movement.name} {movement.date} {movement.category} {movement.amount} {movement.type}")
    conn.execute("INSERT INTO movements (name, data_contabile, data_valuta, causale_abi, descrizione, category, amount, type) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (movement.name, movement.data_contabile, movement.data_valuta, movement.causale_abi, movement.descrizione, movement.category, movement.amount, movement.type))
    conn.commit()

def get_all_movements(conn):
    cursor = conn.execute("SELECT * FROM movements")
    movements = cursor.fetchall()
    result = []
    for movement_data in movements:
        movement = Movement(movement_data[1], movement_data[2], movement_data[3], movement_data[4], movement_data[5], movement_data[6], movement_data[7], movement_data[8])
        movement.set_id(movement_data[0])
        result.append(movement)
    return result

def delete_movement(conn, id):
    conn.execute("DELETE FROM movements WHERE id=?", (id, ))
    conn.commit()


def check_file_exists(conn, file_name):
    print(file_name)
    query = "SELECT COUNT(*) FROM movements_files WHERE file_name = ?"
    cursor = conn.execute(query, (file_name,))
    result = cursor.fetchall()[0][0]

    print(result)
    return result > 0

def process_directory(conn, directory_path):
    # Ottieni la lista di file nella directory
    files = [f for f in os.listdir(directory_path) if f.endswith('.csv')]

    for file in files:
        file_path = os.path.join(directory_path, file)

        # Verifica se il file è già presente nel database
        if not check_file_exists(conn, file):
            # Se il file non è presente, elabora il file CSV e inserisci nel database
            return process_csv_file(file_path)
            
        else:
            print(f"File '{file}' già presente nel database.")


def confronta_e_aggiorna(old_db_path, new_db_path):
    # Connessione ai database
    conn_old = connect(old_db_path)
    conn_new = connect(new_db_path)

    # Creazione dei cursori
    cur_old = conn_old.execute("SELECT name FROM sqlite_master WHERE type='table';")
    cur_new = conn_new.execute("SELECT name FROM sqlite_master WHERE type='table';")

    # Ottenere la lista delle tabelle nei due database
    #cur_old.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables_old = [table[0] for table in cur_old.fetchall()]
    print(tables_old)

    #cur_new.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables_new = [table[0] for table in cur_new.fetchall()]
    print(tables_new)

    # Iterare attraverso le tabelle
    for table in tables_old:
        # Se la tabella esiste anche nel nuovo database
        if table in tables_new:
            # Ottenere la lista delle colonne nella tabella del vecchio database
            cur_old = conn_old.execute(f"PRAGMA table_info({table});")
            columns_old = [column[1] for column in cur_old.fetchall()]
            print(columns_old)

            # Ottenere la lista delle colonne nella tabella del nuovo database
            cur_new = conn_new.execute(f"PRAGMA table_info({table});")
            columns_new = [column[1] for column in cur_new.fetchall()]
            print(columns_new)

            # Trovare le colonne che sono presenti solo nel nuovo database
            columns_diff = list(set(columns_new) - set(columns_old))

            # Aggiungere colonne mancanti alla tabella del vecchio database
            for column in columns_diff:
                cur_old.execute(f"ALTER TABLE {table} ADD COLUMN {column} TEXT DEFAULT '';")
            print(f"INSERT INTO {table} SELECT * FROM {table};")
            # Trasferire i dati dalla tabella del vecchio database a quella del nuovo
            cur_old = conn_old.execute(f"SELECT * FROM {table};")
            print(cur_old.fetchall())

    # Committare le modifiche e chiudere le connessioni
    conn_old.commit()
    conn_old.close()
    conn_new.close()

def add_movements_file(conn, file_name):
    #print(f"{movement.name} {movement.date} {movement.category} {movement.amount} {movement.type}")
    conn.execute("INSERT INTO movements_files (file_name) VALUES (?)", (file_name, ))
    conn.commit()

# CATEGORIES

def get_all_categories(conn):
    cursor = conn.execute("SELECT * FROM categories")
    categories = cursor.fetchall()
    result = []
    for category_data in categories:
        category = Movement(category_data[1], category_data[2], category_data[3], category_data[4], category_data[5], category_data[6], category_data[7], category_data[8])
        category.set_id(category_data[0])
        result.append(category)
    return result