# tasks.py
from models.task import Task

def add_task(conn, task):
    query = "INSERT INTO tasks (name, date, category_id) VALUES (?, ?, ?)"
    conn.execute(query, (task.name, task.date, task.category if task.category is not None else 1))
    conn.commit()

def get_all_tasks(conn):
    query = "SELECT id, name, date, category_id FROM tasks"
    cursor = conn.execute(query)
    tasks = [Task(*task_data[1:], task_data[0]) for task_data in cursor.fetchall()]
    return tasks

def create_task_from_data(task_data):
    task_date = task_data[2]
    task = Task(task_data[1], task_date, task_data[3])
    task.set_id(task_data[0])
    return task

def delete_task(conn, id):
    query = "DELETE FROM tasks WHERE id=?"
    conn.execute(query, (id,))
    conn.commit()

def edit_task(conn, task):
    query = "UPDATE tasks SET name = ?, date = ?, category_id = ? WHERE id = ?"
    conn.execute(query, (task.name, task.date, task.category if task.category is not None else 1, task.id))
    conn.commit()

def get_task(conn, task_id):
    query = "SELECT * FROM tasks WHERE id = ?"
    cursor = conn.execute(query, (task_id,))
    task_data = cursor.fetchone()
    return create_task_from_data(task_data) if task_data else None

def clean_tasks(conn):
    conn.execute("DELETE FROM tasks;")
    conn.commit()
