# movements.py
from models.movement import Movement

def add_movement(conn, movement):
    query = "INSERT INTO movements (name, data_contabile, data_valuta, causale_abi, descrizione, category, amount, type) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    conn.execute(query, (movement.name, movement.data_contabile, movement.data_valuta, movement.causale_abi, movement.descrizione, movement.category, movement.amount, movement.type))
    conn.commit()

def clean_movements(conn):
    conn.execute("DELETE FROM movements;")
    conn.commit()

def get_all_movements(conn):
    query = "SELECT id, name, data_contabile, data_valuta, causale_abi, descrizione, category, amount, type FROM movements"
    cursor = conn.execute(query)
    movements = [Movement(*movement_data[1:], id=movement_data[0]) for movement_data in cursor.fetchall()]
    return movements

def delete_movement(conn, id):
    conn.execute("DELETE FROM movements WHERE id=?", (id,))
    conn.commit()

def add_movements_file(conn, file_name):
    query = "INSERT INTO movements_files (file_name) VALUES (?)"
    conn.execute(query, (file_name,))
    conn.commit()

def check_file_exists(conn, file_name):
    query = "SELECT COUNT(*) FROM movements_files WHERE file_name = ?"
    result = conn.execute(query, (file_name,)).fetchall()[0][0]
    return result > 0

def clean_movements_files(conn):
    conn.execute("DELETE FROM movements_files;")
    conn.commit()
