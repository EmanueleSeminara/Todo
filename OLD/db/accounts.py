# accounts.py
from models.account import Account

def add_account(conn, account):
    query = "INSERT INTO accounts (name, type, saldo, data_saldo) VALUES (?, ?, ?, ?)"
    conn.execute(query, (account.name, account.type, account.saldo, account.data_saldo))
    conn.commit()

def clean_accounts(conn):
    conn.execute("DELETE FROM accounts;")
    conn.commit()

def get_all_accounts(conn):
    query = "SELECT id, name, type, saldo, data_saldo FROM accounts"
    cursor = conn.execute(query)
    accounts = [Account(*account_data[1:], id=account_data[0]) for account_data in cursor.fetchall()]
    return accounts

def delete_account(conn, id):
    conn.execute("DELETE FROM accounts WHERE id=?", (id,))
    conn.commit()

