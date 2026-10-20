"""All task SQL. Every query includes user_id so users can only touch their own tasks."""
from db import execute, fetch_all

ORDER = "ORDER BY is_done, FIELD(priority, 'high', 'medium', 'low'), due_date IS NULL, due_date, id"


def add_task(user_id, title, description, priority, due_date):
    task_id, _ = execute(
        "INSERT INTO tasks (user_id, title, description, priority, due_date) VALUES (%s, %s, %s, %s, %s)",
        (user_id, title, description, priority, due_date),
    )
    return task_id


def list_tasks(user_id, status="all"):
    sql = "SELECT id, title, priority, due_date, is_done, description FROM tasks WHERE user_id = %s"
    if status == "pending":
        sql += " AND is_done = FALSE"
    elif status == "done":
        sql += " AND is_done = TRUE"
    return fetch_all(f"{sql} {ORDER}", (user_id,))


def get_task(user_id, task_id):
    rows = fetch_all(
        "SELECT id, title, description, priority, due_date, is_done FROM tasks WHERE id = %s AND user_id = %s",
        (task_id, user_id),
    )
    return rows[0] if rows else None


def update_task(user_id, task_id, title, description, priority, due_date):
    _, changed = execute(
        "UPDATE tasks SET title = %s, description = %s, priority = %s, due_date = %s WHERE id = %s AND user_id = %s",
        (title, description, priority, due_date, task_id, user_id),
    )
    return changed


def set_done(user_id, task_id, done):
    _, changed = execute(
        "UPDATE tasks SET is_done = %s WHERE id = %s AND user_id = %s",
        (done, task_id, user_id),
    )
    return changed


def delete_task(user_id, task_id):
    _, deleted = execute("DELETE FROM tasks WHERE id = %s AND user_id = %s", (task_id, user_id))
    return deleted
