import os
import sqlite3
from functools import wraps
from pathlib import Path

from flask import (
    Flask,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)

app.secret_key = os.environ.get(
    "FALCON_SECRET_KEY",
    "falcon-helpdesk-local-key",
)

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
            INSERT OR IGNORE INTO users (
                full_name,
                username,
                password_hash,
                role
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                "Ali Almazrouei",
                "ali",
                generate_password_hash("Falcon123!"),
                "Administrator",
            ),
        )


def login_required(view_function):
    @wraps(view_function)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))

        return view_function(*args, **kwargs)

    return wrapped_view


@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    error = None

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        with get_database_connection() as connection:
            user = connection.execute(
                """
                SELECT *
                FROM users
                WHERE username = ?
                """,
                (username,),
            ).fetchone()

        if user and check_password_hash(
            user["password_hash"],
            password,
        ):
            session.clear()
            session["user_id"] = user["id"]
            session["full_name"] = user["full_name"]
            session["role"] = user["role"]

            return redirect(url_for("dashboard"))

        error = "The username or password is incorrect."

    return render_template(
        "login.html",
        error=error,
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/")
@login_required
def dashboard():
    with get_database_connection() as connection:
        stats = connection.execute(
            """
            SELECT
                SUM(
                    CASE WHEN status = 'Open'
                    THEN 1 ELSE 0 END
                ) AS open,

                SUM(
                    CASE WHEN status = 'In Progress'
                    THEN 1 ELSE 0 END
                ) AS in_progress,

                SUM(
                    CASE WHEN status = 'Resolved'
                    THEN 1 ELSE 0 END
                ) AS resolved,

                SUM(
                    CASE WHEN status = 'Closed'
                    THEN 1 ELSE 0 END
                ) AS closed

            FROM tickets
            """
        ).fetchone()

        recent_tickets = connection.execute(
            """
            SELECT
                id,
                requester,
                priority,
                subject,
                status

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
@login_required
def create_ticket():
    message = None

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

        message = "Ticket created and saved successfully."

    return render_template(
        "create_ticket.html",
        message=message,
    )


@app.route("/tickets")
@login_required
def all_tickets():
    search = request.args.get("search", "").strip()
    status = request.args.get("status", "").strip()
    priority = request.args.get("priority", "").strip()

    sql = """
        SELECT *
        FROM tickets
        WHERE 1 = 1
    """

    values = []

    if search:
        sql += """
            AND (
                subject LIKE ?
                OR requester LIKE ?
                OR department LIKE ?
                OR category LIKE ?
                OR description LIKE ?
            )
        """

        search_value = f"%{search}%"
        values.extend([search_value] * 5)

    if status:
        sql += " AND status = ?"
        values.append(status)

    if priority:
        sql += " AND priority = ?"
        values.append(priority)

    sql += " ORDER BY id DESC"

    with get_database_connection() as connection:
        tickets = connection.execute(
            sql,
            values,
        ).fetchall()

    return render_template(
        "tickets.html",
        tickets=tickets,
        search=search,
        selected_status=status,
        selected_priority=priority,
    )


@app.route("/tickets/<int:ticket_id>")
@login_required
def ticket_details(ticket_id):
    with get_database_connection() as connection:
        ticket = connection.execute(
            """
            SELECT *
            FROM tickets
            WHERE id = ?
            """,
            (ticket_id,),
        ).fetchone()

    if ticket is None:
        return "Ticket not found.", 404

    return render_template(
        "ticket_details.html",
        ticket=ticket,
    )


@app.route(
    "/tickets/<int:ticket_id>/edit",
    methods=["GET", "POST"],
)
@login_required
def edit_ticket(ticket_id):
    with get_database_connection() as connection:
        ticket = connection.execute(
            """
            SELECT *
            FROM tickets
            WHERE id = ?
            """,
            (ticket_id,),
        ).fetchone()

        if ticket is None:
            return "Ticket not found.", 404

        if request.method == "POST":
            requester = request.form["requester"].strip()
            department = request.form["department"]
            priority = request.form["priority"]
            category = request.form["category"]
            subject = request.form["subject"].strip()
            description = request.form["description"].strip()
            status = request.form["status"]

            if status not in ALLOWED_STATUSES:
                return "Invalid ticket status.", 400

            connection.execute(
                """
                UPDATE tickets

                SET requester = ?,
                    department = ?,
                    priority = ?,
                    category = ?,
                    subject = ?,
                    description = ?,
                    status = ?

                WHERE id = ?
                """,
                (
                    requester,
                    department,
                    priority,
                    category,
                    subject,
                    description,
                    status,
                    ticket_id,
                ),
            )

            return redirect(
                url_for(
                    "ticket_details",
                    ticket_id=ticket_id,
                )
            )

    return render_template(
        "edit_ticket.html",
        ticket=ticket,
    )


@app.route(
    "/tickets/<int:ticket_id>/status",
    methods=["POST"],
)
@login_required
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
            (
                new_status,
                ticket_id,
            ),
        )

    return redirect(url_for("all_tickets"))


@app.route(
    "/tickets/<int:ticket_id>/delete",
    methods=["POST"],
)
@login_required
def delete_ticket(ticket_id):
    with get_database_connection() as connection:
        ticket = connection.execute(
            """
            SELECT id
            FROM tickets
            WHERE id = ?
            """,
            (ticket_id,),
        ).fetchone()

        if ticket is None:
            return "Ticket not found.", 404

        connection.execute(
            """
            DELETE FROM tickets
            WHERE id = ?
            """,
            (ticket_id,),
        )

    return redirect(url_for("all_tickets"))


initialize_database()


if __name__ == "__main__":
    app.run(debug=True)