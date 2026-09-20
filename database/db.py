import sqlite3
from datetime import datetime

#create database
db_file = sqlite3.connect("database/one.db")
cursor = db_file.cursor()

def create_table():
    _ = cursor.execute("CREATE TABLE IF NOT EXISTS history(id INTEGER PRIMARY KEY AUTOINCREMENT, action TEXT, target TEXT)")
    _ = cursor.execute("CREATE TABLE IF NOT EXISTS tasks(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, time_remaining TEXT | NULL, status TEXT DEFAULT 'pending', description TEXT | NULL)")
    db_file.commit()

def create_task(name: str, time_remaining: str | None, description: str | None):
    _ = cursor.execute("INSERT INTO tasks(name, time_remaining, description) VALUES(?, ?, ?)", (name, time_remaining, description))
    db_file.commit()

def history_insert(action:str, target: str):
    _ = cursor.execute("INSERT INTO history(action, target) VALUES(?, ?)", (action, target))
    db_file.commit()

def db_query():
    for row in cursor.execute("SELECT * FROM history"):
        print(row)