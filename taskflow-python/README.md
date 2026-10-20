# TaskFlow – Task Manager in Python

A command-line task manager built with **Python** and **MySQL**. Each user registers, logs in and manages
their own tasks. No web framework is needed.

## Features
- Register and log in; passwords are salted and hashed (PBKDF2) and never stored as plain text
- Add, view, edit and delete tasks, each with a priority and an optional due date
- Filter tasks by status (all, pending, completed) and mark them done or pending
- Overdue tasks are flagged with `!`
- Users can only see and change their own tasks (every query filters on `user_id`)
- Parameterized SQL queries (protects against SQL injection) and input checks before saving

## Tech Stack
Python, MySQL, `mysql-connector-python`, `hashlib`, `unittest`

## Project Structure
```
taskflow-python/
├── main.py          # menus and user input
├── auth.py          # register and log in
├── tasks.py         # all task SQL queries
├── security.py      # password hashing
├── validators.py    # input checks
├── db.py            # MySQL connection helpers
├── schema.sql       # users and tasks tables
├── tests/test_basics.py
├── requirements.txt
└── .env.example
```

## Database Design
- `users` (id, username, password_hash, created_at)
- `tasks` (id, user_id, title, description, priority, due_date, is_done, created_at)
- `tasks.user_id` is a foreign key to `users.id`, with `ON DELETE CASCADE`

## Setup (VS Code)
1. Install Python 3.10+ and MySQL, then open this folder in VS Code.
2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   venv\Scripts\activate        # Windows
   source venv/bin/activate     # macOS / Linux
   ```
3. `pip install -r requirements.txt`
4. Create the tables: run `schema.sql` in MySQL Workbench (or `mysql -u root -p < schema.sql`).
5. Copy `.env.example` to `.env` and enter your MySQL password.
6. Run the app: `python main.py`

## Run the tests
```
python -m unittest discover tests
```
The tests cover password hashing and input checks and need no database.
