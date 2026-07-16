import sqlite3
from pathlib import Path

from werkzeug.security import generate_password_hash


BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "database" / "falcon_helpdesk.db"


def create_admin():
    print()
    print("Create a Falcon HelpDesk administrator")
    print("--------------------------------------")

    full_name = input("Full name: ").strip()
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    confirm_password = input("Confirm password: ").strip()

    if not full_name:
        print("Error: Full name cannot be blank.")
        return

    if not username:
        print("Error: Username cannot be blank.")
        return

    if not password:
        print("Error: Password cannot be blank.")
        return

    if len(password) < 8:
        print("Error: Password must contain at least 8 characters.")
        return

    if password != confirm_password:
        print("Error: The passwords do not match.")
        return

    DATABASE_PATH.parent.mkdir(exist_ok=True)

    try:
        with sqlite3.connect(DATABASE_PATH) as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    full_name TEXT NOT NULL,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    role TEXT NOT NULL
                )
                """
            )

            connection.execute(
                """
                INSERT INTO users (
                    full_name,
                    username,
                    password_hash,
                    role
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    full_name,
                    username,
                    generate_password_hash(password),
                    "Administrator",
                ),
            )

        print()
        print("Administrator account created successfully.")
        print(f"Username: {username}")
        print("You can now start Falcon HelpDesk and sign in.")

    except sqlite3.IntegrityError:
        print()
        print("Error: That username already exists.")
        print("Run the program again and choose a different username.")

    except Exception as error:
        print()
        print("An unexpected error happened:")
        print(error)


if __name__ == "__main__":
    create_admin()