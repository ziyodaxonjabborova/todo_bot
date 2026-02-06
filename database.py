import sqlite3

# 🔹 Database connection function
def get_connect():
    """Establishes a connection to the SQLite database."""
    return sqlite3.connect("database.db")


# 🔹 Table creation
def create_table():
    """Initializes the tasks table if it does not exist."""
    sql = """
    CREATE TABLE IF NOT EXISTS tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    with get_connect() as db:
        cur = db.cursor()
        cur.execute(sql)
        db.commit()


# 🔹 Add a new task
def add_task(user_id, name):
    """Inserts a new task into the database for a specific user."""
    sql = "INSERT INTO tasks (user_id, name) VALUES (?, ?)"
    with get_connect() as db:
        cur = db.cursor()
        cur.execute(sql, (user_id, name))
        db.commit()


# 🔹 Retrieve tasks by status
def get_tasks_by_status(user_id, status):
    """Fetches tasks based on their status (all, pending, or done)."""
    with get_connect() as db:
        cur = db.cursor()
        if status == "all":
            cur.execute("SELECT name, status FROM tasks WHERE user_id = ?", (user_id,))
        elif status == "pending":
            cur.execute("SELECT name, status FROM tasks WHERE user_id = ? AND status = 'pending'", (user_id,))
        elif status == "done":
            cur.execute("SELECT name, status FROM tasks WHERE user_id = ? AND status = 'done'", (user_id,))
        else:
            return []

        rows = cur.fetchall()
        # Returns a list of dictionaries for easier handling in the bot logic
        return [{"name": row[0], "status": row[1]} for row in rows]


# 🔹 Update task name
def update_task_name(user_id, old_name, new_name):
    """Renames an existing task for a specific user."""
    db = get_connect()
    cur = db.cursor()
    cur.execute(
        "UPDATE tasks SET name = ? WHERE user_id = ? AND name = ?", 
        (new_name, user_id, old_name)
    )
    db.commit()
    count = cur.rowcount
    db.close()
    return count > 0


# 🔹 Update task status
def update_task_status(user_id, task_name, new_status):
    """Changes the status of a task (e.g., from 'pending' to 'done')."""
    db = get_connect()
    cur = db.cursor()
    cur.execute(
        "UPDATE tasks SET status = ? WHERE user_id = ? AND name = ?", 
        (new_status, user_id, task_name)
    )
    db.commit()
    count = cur.rowcount
    db.close()
    return count > 0


# 🔹 Delete a task
def delete_task(user_id, task_name):
    """Removes a task from the database using case-insensitive name matching."""
    task_name = task_name.strip()
    db = get_connect()
    cur = db.cursor()
    cur.execute(
        "DELETE FROM tasks WHERE user_id = ? AND LOWER(name) = LOWER(?)", 
        (user_id, task_name)
    )
    deleted_count = cur.rowcount
    db.commit()
    db.close()
    return deleted_count > 0