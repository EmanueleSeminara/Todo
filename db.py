# db.py
from sqlite3 import connect
from task import Task
from movement import Movement

def connect_db():
    conn = connect("todo.db")
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date TEXT,
            category TEXT NOT NULL

        )
    ''')
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS movements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date TEXT,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            type TEXT NOT NULL
        )
    ''')
    return conn

def add_task(conn, task):
    conn.execute("INSERT INTO tasks (name, date, category) VALUES (?, ?, ?)", (task.name, task.date, task.category))
    conn.commit()

def get_all_tasks(conn):
    cursor = conn.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    result = []
    for task_data in tasks:
        task = Task(task_data[1], task_data[2], task_data[3])
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
    result.set_id(id)
    return result

# MOVEMENTS
def add_movement(conn, movement):
    print(f"{movement.name} {movement.date} {movement.category} {movement.amount} {movement.type}")
    conn.execute("INSERT INTO movements (name, date, category, amount, type) VALUES (?, ?, ?, ?, ?)", (movement.name, movement.date, movement.category, movement.amount, movement.type))
    conn.commit()

def get_all_movements(conn):
    cursor = conn.execute("SELECT * FROM movements")
    movements = cursor.fetchall()
    result = []
    for movement_data in movements:
        movement = Movement(movement_data[1], movement_data[2], movement_data[3], movement_data[4], movement_data[5])
        movement.set_id(movement_data[0])
        result.append(movement)
    return result

def delete_movement(conn, id):
    conn.execute("DELETE FROM movements WHERE id=?", (id, ))
    conn.commit()
