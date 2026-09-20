import sqlite3
from datetime import datetime

db_file = sqlite3.connect("database/one.db")
cursor = db_file.cursor()

def create_table():
    _ = cursor.execute("CREATE TABLE history(id INTEGER PRIMARY KEY AUTOINCREMENT, action TEXT, target TEXT)")
    _ = cursor.execute("CREATE TABLE tasks(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, time_remaining DATETIME)")
    db_file.commit()

def create_task(name: str, time_remaining: datetime):
    _ = cursor.execute("INSERT INTO tasks(name, time_remaining) VALUES(?, ?)", (name, time_remaining))
    db_file.commit()

def history_insert(action:str, target: str):
    res = cursor.execute("INSERT INTO history(action, target) VALUES(?, ?)", (action, target))
    db_file.commit()

def db_query():
    for row in cursor.execute("SELECT * FROM history"):
        print(row)