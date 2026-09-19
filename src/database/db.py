import sqlite3

db_file = sqlite3.connect("src/database/history.db")
cursor = db_file.cursor()

def create_table():
    res = cursor.execute("CREATE TABLE history(id INTEGER PRIMARY KEY AUTOINCREMENT, action TEXT, target TEXT)")
    db_file.commit()

    res = cursor.execute("SELECT name FROM sqlite_master")
    print(res.fetchall())

create_table()