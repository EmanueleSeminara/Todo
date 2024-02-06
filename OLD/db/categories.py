# categories.py
from models.category import Category
from sqlite3 import Connection

def get_all_categories(conn: Connection) -> list[Category]:
    cursor = conn.execute("SELECT * FROM categories")
    categories = [Category(category_data[1], category_data[0]) for category_data in cursor.fetchall()]
    return categories

def add_category(conn: Connection, category: Category) -> None:
    conn.execute("INSERT INTO categories (name) VALUES (?)", (category.name,))
    conn.commit()

def get_category_by_name(conn: Connection, name: str) -> Category:
    cursor = conn.execute("SELECT * FROM categories WHERE name = ?", (name,))
    category_data = cursor.fetchone()
    cursor.close()

    return Category(category_data[1], category_data[0]) if category_data else None

def create_default_category(conn: Connection) -> None:
    if not get_category_by_name(conn, "Default"):
        add_category(conn, Category("Default"))
