"""TaskFlow: a command-line task manager (Python + MySQL)."""
from datetime import date
from getpass import getpass

import mysql.connector

import auth
import tasks
import validators as v

AUTH_MENU = """
===== TaskFlow =====
 1. Register
 2. Log in
 0. Exit
"""

TASK_MENU = """
===== TaskFlow: {user} =====
 1. Add task            5. Edit task
 2. View all tasks      6. Mark done / pending
 3. View pending        7. Delete task
 4. View completed      0. Log out
"""


def ask(prompt, parser):
    """Keep asking until the parser accepts the input."""
    while True:
        try:
            return parser(input(prompt))
        except ValueError as err:
            print(f"  {err}")


def show_tasks(rows):
    if not rows:
        print("  (no tasks)")
        return
    print(f"{'ID':<4} {'Status':<8} {'Priority':<9} {'Due':<12} Title")
    print("-" * 60)
    today = date.today()
    for task_id, title, priority, due, is_done, _description in rows:
        status = "Done" if is_done else "Pending"
        due_text = str(due) if due else "-"
        if due and not is_done and due < today:
            due_text += "!"
        print(f"{task_id:<4} {status:<8} {priority:<9} {due_text:<12} {title}")
    print("  ('!' next to a date means overdue)")


# ---------- Task actions ----------
def add_task(user_id):
    title = ask("Title: ", v.parse_title)
    description = ask("Description (optional): ", v.parse_description)
    priority = ask("Priority 1=low 2=medium 3=high (Enter for medium): ", v.parse_priority)
    due_date = ask("Due date YYYY-MM-DD (optional): ", v.parse_due_date)
    task_id = tasks.add_task(user_id, title, description, priority, due_date)
    print(f"  Task added with ID {task_id}.")


def edit_task(user_id):
    task_id = ask("Task ID to edit: ", v.parse_id)
    task = tasks.get_task(user_id, task_id)
    if not task:
        print("  Task not found.")
        return
    _, title, description, priority, due_date, _done = task
    print("  Press Enter to keep the current value.")
    new_title = input(f"Title [{title}]: ").strip()
    title = v.parse_title(new_title) if new_title else title
    new_desc = input(f"Description [{description or ''}]: ").strip()
    description = new_desc or description
    new_priority = input(f"Priority [{priority}]: ").strip()
    priority = v.parse_priority(new_priority) if new_priority else priority
    new_due = input(f"Due date [{due_date or 'none'}]: ").strip()
    due_date = v.parse_due_date(new_due) if new_due else due_date
    tasks.update_task(user_id, task_id, title, description, priority, due_date)
    print("  Task updated.")


def toggle_task(user_id):
    task_id = ask("Task ID: ", v.parse_id)
    task = tasks.get_task(user_id, task_id)
    if not task:
        print("  Task not found.")
        return
    now_done = not task[5]
    tasks.set_done(user_id, task_id, now_done)
    print("  Marked as done." if now_done else "  Marked as pending.")


def delete_task(user_id):
    task_id = ask("Task ID to delete: ", v.parse_id)
    if input("  Delete this task? (y/n): ").strip().lower() != "y":
        print("  Cancelled.")
        return
    print("  Task deleted." if tasks.delete_task(user_id, task_id) else "  Task not found.")


def task_menu(user_id, username):
    while True:
        print(TASK_MENU.format(user=username))
        choice = input("Choose an option: ").strip()
        try:
            if choice == "1":
                add_task(user_id)
            elif choice == "2":
                show_tasks(tasks.list_tasks(user_id))
            elif choice == "3":
                show_tasks(tasks.list_tasks(user_id, "pending"))
            elif choice == "4":
                show_tasks(tasks.list_tasks(user_id, "done"))
            elif choice == "5":
                edit_task(user_id)
            elif choice == "6":
                toggle_task(user_id)
            elif choice == "7":
                delete_task(user_id)
            elif choice == "0":
                print("  Logged out.")
                return
            else:
                print("  Invalid option, try again.")
        except ValueError as err:
            print(f"  {err}")
        except mysql.connector.Error as err:
            print(f"  Database error: {err}")


# ---------- Register / log in ----------
def register():
    username = ask("Choose a username: ", v.parse_username)
    password = ask_password("Choose a password: ")
    if getpass("Repeat password: ") != password:
        print("  Passwords did not match.")
        return
    try:
        auth.register(username, password)
        print("  Account created. You can log in now.")
    except ValueError as err:
        print(f"  {err}")


def ask_password(prompt):
    while True:
        try:
            return v.parse_password(getpass(prompt))
        except ValueError as err:
            print(f"  {err}")


def log_in():
    username = input("Username: ").strip()
    password = getpass("Password: ")
    user_id = auth.login(username, password)
    if user_id is None:
        print("  Invalid username or password.")
        return
    task_menu(user_id, username)


def main():
    while True:
        print(AUTH_MENU)
        choice = input("Choose an option: ").strip()
        try:
            if choice == "1":
                register()
            elif choice == "2":
                log_in()
            elif choice == "0":
                print("Goodbye!")
                break
            else:
                print("  Invalid option, try again.")
        except mysql.connector.Error as err:
            print(f"  Database error: {err}")


if __name__ == "__main__":
    main()
