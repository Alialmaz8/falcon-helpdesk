import sqlite3
from pathlib import Path

from flask import Flask, redirect, render_template, request, url_for


app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "database" / "falcon_helpdesk.db"

ALLOWED_STATUSES = {
    "Open",
    "In Progress",
    "Resolved",
    "Closed",
}


def get_database_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    DATABASE_PATH.parent.mkdir(exist_ok=True)

    with get_database_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                requester TEXT NOT NULL,
                department TEXT NOT NULL,
                priority TEXT NOT NULL,
                category TEXT NOT NULL,
                subject TEXT NOT NULL,
                description TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Open',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


@app.route("/")
def dashboard():
    with get_database_connection() as connection:
        stats = connection.execute(
            """
            SELECT
                SUM(CASE WHEN status = 'Open' THEN 1 ELSE 0 END) AS open,
                SUM(CASE WHEN status = 'In Progress' THEN 1 ELSE 0 END)
                    AS in_progress,
                SUM(CASE WHEN status = 'Resolved' THEN 1 ELSE 0 END)
                    AS resolved,
                SUM(CASE WHEN status = 'Closed' THEN 1 ELSE 0 END)
                    AS closed
            FROM tickets
            """
        ).fetchone()

        recent_tickets = connection.execute(
            """
            SELECT id, requester, priority, subject, status
            FROM tickets
            ORDER BY id DESC
            LIMIT 5
            """
        ).fetchall()

    return render_template(
        "dashboard.html",
        stats=stats,
        tickets=recent_tickets,
    )


@app.route("/tickets/new", methods=["GET", "POST"])
def create_ticket():
    if request.method == "POST":
        requester = request.form["requester"].strip()
        department = request.form["department"]
        priority = request.form["priority"]
        category = request.form["category"]
        subject = request.form["subject"].strip()
        description = request.form["description"].strip()

        with get_database_connection() as connection:
            connection.execute(
                """
                INSERT INTO tickets (
                    requester,
                    department,
                    priority,
                    category,
                    subject,
                    description
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    requester,
                    department,
                    priority,
                    category,
                    subject,
                    description,
                ),
            )

        return redirect(url_for("all_tickets"))

    return render_template("create_ticket.html")


@app.route("/tickets")
def all_tickets():
    with get_database_connection() as connection:
        tickets = connection.execute(
            """
            SELECT *
            FROM tickets
            ORDER BY id DESC
            """
        ).fetchall()

    return render_template(
        "tickets.html",
        tickets=tickets,
    )


@app.route("/tickets/<int:ticket_id>/status", methods=["POST"])
def update_ticket_status(ticket_id):
    new_status = request.form.get("status", "").strip()

    if new_status not in ALLOWED_STATUSES:
        return "Invalid ticket status.", 400

    with get_database_connection() as connection:
        connection.execute(
            """
            UPDATE tickets
            SET status = ?
            WHERE id = ?
            """,
            (new_status, ticket_id),
        )

    return redirect(url_for("all_tickets"))


initialize_database()


if __name__ == "__main__":
    app.run(debug=True)