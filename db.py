# db.py
from sqlite3 import connect
from task import Task

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
