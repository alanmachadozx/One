# Database Management 

The `db.py` module serves as the dedicated SQLite database interface for the "One" project. To ensure smooth performance and avoid blocking the main application flow, the database connection and all its operations run entirely on a separate background daemon thread, independently from the UI and the audio listener pipeline.

## Thread-Safe Execution Architecture

Because SQLite connections cannot be safely shared across multiple threads by default, this module implements a producer-consumer architecture using Python's `queue` system. All database interactions are managed by a continuous `db_manager` loop running on a dedicated thread. 

Other parts of the application do not execute SQL directly. Instead, they communicate with the database thread using two queues:
* **`q_requests`**: Receives tuples containing the SQL command string and the parameters to be inserted `(sql, params)`.
* **`q_result`**: Returns the outcome of the requested operation back to the caller.

Inside the `db_manager` loop, the system evaluates the incoming SQL command. If the query starts with `SELECT`, it executes the read operation, fetches all resulting rows, and pushes the data into `q_result`. If it is a write operation (such as `INSERT` or `CREATE`), it executes the command, commits the changes to the database, and pushes a boolean `True` to the result queue. If any database error occurs during execution, a `False` flag is returned to ensure the application handles the failure gracefully.

## Schema and Initialization

Upon importing or running the module, it automatically connects to (or creates) the `one.db` database file located in the `database/` directory and invokes the `create_table()` setup function. The schema consists of two primary tables:
* **History Table**: Acts as a log for user interactions, storing an auto-incrementing `id`, the recognized `action` (intent), and the specific `target` of that action.
* **Task Table**: Serves as a to-do list or scheduling structure, storing an `id`, task `name`, `time_remaining`, `description`, and a `status` which defaults to `'pending'`.

