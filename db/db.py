# db.py
from sqlite3 import connect, Connection, PARSE_DECLTYPES, PARSE_COLNAMES

def connect_db(db_path: str) -> Connection:
    conn = connect(db_path, detect_types=PARSE_DECLTYPES | PARSE_COLNAMES)
    create_tables(conn)
    return conn

def create_tables(conn: Connection) -> None:
    tables = {
        'tasks': '''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                date TIMESTAMP,
                category_id INTEGER,
                stato TEXT,
                frequenza TEXT,
                priorita TEXT,
                FOREIGN KEY (category_id) REFERENCES categories(id)
            )
        ''',
        'categories': '''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        ''',
        'movements': '''
            CREATE TABLE IF NOT EXISTS movements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                data_contabile TIMESTAMP,
                data_valuta TIMESTAMP,
                causale_abi TEXT,
                descrizione TEXT,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                type TEXT NOT NULL
            )
        ''',
        'movements_files': '''
            CREATE TABLE IF NOT EXISTS movements_files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_name TEXT NOT NULL
            )
        ''',
        'goals': '''
            CREATE TABLE IF NOT EXISTS goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        ''',
        'person': '''
            CREATE TABLE IF NOT EXISTS person (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                surname TEXT,
                phone TEXT,
                email TEXT
            )
        ''',
        'ideas': '''
            CREATE TABLE IF NOT EXISTS ideas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT
            )
        ''',
        'accounts': '''
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                type TEXT,
                saldo TEXT,
                data_saldo TIMESTAMP
            )
        '''
    }

    for table_name, table_query in tables.items():
        conn.execute(table_query)

def confronta_e_aggiorna(old_db_path: str, new_db_path: str) -> None:
    conn_old = connect(old_db_path)
    conn_new = connect(new_db_path)

    cur_old = conn_old.execute("SELECT name FROM sqlite_master WHERE type='table';")
    cur_new = conn_new.execute("SELECT name FROM sqlite_master WHERE type='table';")

    tables_old = [table[0] for table in cur_old.fetchall()]
    tables_new = [table[0] for table in cur_new.fetchall()]

    for table in tables_old:
        if table in tables_new:
            cur_old = conn_old.execute(f"PRAGMA table_info({table});")
            columns_old = [column[1] for column in cur_old.fetchall()]

            cur_new = conn_new.execute(f"PRAGMA table_info({table});")
            columns_new = [column[1] for column in cur_new.fetchall()]

            columns_diff = list(set(columns_new) - set(columns_old))

            for column in columns_diff:
                cur_old.execute(f"ALTER TABLE {table} ADD COLUMN {column} TEXT DEFAULT '';")

            cur_old = conn_old.execute(f"SELECT * FROM {table};")

    conn_old.commit()
    conn_old.close()
    conn_new.close()
