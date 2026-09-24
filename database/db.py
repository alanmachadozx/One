import sqlite3
from datetime import datetime
import queue
import threading

from numpy._core.numeric import result_type

q_requests = queue.Queue()
q_result = queue.Queue()

def db_manager():
    db_file = sqlite3.connect("database/one.db")
    cursor = db_file.cursor()

    while True:
        request = q_requests.get()

        if request is None: break

        #sql is the command text containing (?, ?) where the data should be inserted
        #params is the data to be inserted
        sql, params = request

        try:
            cursor.execute(sql, params)
            
            # if the query is a SELECT, fetch the results and put them in the result queue
            if sql.strip().upper().startswith("SELECT"):
                result = cursor.fetchall()
                q_result.put(result)

            # if the query is not a SELECT, commit the changes
            else:
                db_file.commit()
                q_result.put(True)

        except Exception as e:

            # if the query fails, put False in the result queue
            q_result.put(False)
            
        q_requests.task_done()

# create the database manager thread
db_thread = threading.Thread(target = db_manager, daemon = True)
db_thread.start()
    
    
def create_table():
    # When there are no variables to substitute, use an empty tuple
    q_requests.put(("CREATE TABLE IF NOT EXISTS history(id INTEGER PRIMARY KEY AUTOINCREMENT, action TEXT, target TEXT)", ()))
    q_result.get()
    
    q_requests.put(("CREATE TABLE IF NOT EXISTS task(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, time_remaining TEXT, status TEXT DEFAULT 'pending', description TEXT)", ()))
    q_result.get()
    

def create_task(name: str, time_remaining: str | None, description: str | None):
    sql = "INSERT INTO task(name, time_remaining, description) VALUES(?, ?, ?)"
    q_requests.put((sql, (name, time_remaining, description)))
    q_result.get()
    

def view_tasks():
    q_requests.put(("SELECT * FROM task", ()))
    result = q_result.get()
    
    if isinstance(result, Exception):
        print(f"Error in {result}")
        return
    
    for row in result:
        print(row)

def history_insert(action:str, target: str):
    sql = "INSERT INTO history(action, target) VALUES(?, ?)"
    q_requests.put((sql, (action, target)))
    q_result.get()

def db_query():
    q_requests.put(("SELECT * FROM history", ()))
    result = q_result.get()
    
    if isinstance(result, Exception):
        print(f"Error in {result}")
        return
    
    for row in result:
        print(row)

create_table()