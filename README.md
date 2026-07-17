<div align="center">

<img src="./screenshots/uae_flag.png" width="90" alt="UAE Flag">
&nbsp;&nbsp;&nbsp;&nbsp;
<img src="./screenshots/abudhabi_flag.png" width="90" alt="Abu Dhabi Flag">

# Falcon HelpDesk

### IT Support and Ticket Management System

A Computer Science student project built with Python, Flask, and SQLite.

</div>

---

## About

Falcon HelpDesk is a small web application for managing IT support tickets.

I built this project to practice Python web development and learn how a Flask application connects to a database.

The system includes user accounts, support tickets, asset inventory, and basic reports.

This is a learning project and is not intended to be used as a production help desk system.

---

## Main Features

- User login and logout
- Password hashing
- Administrator, Technician, and User roles
- Create support tickets
- View ticket details
- Edit and delete tickets
- Change ticket status
- Search and filter tickets
- Ticket form validation
- Dashboard ticket statistics
- Asset inventory
- Add, edit, search, and delete assets
- User account management
- Basic reports

---

## User Roles

### Administrator

The Administrator has access to all parts of the application.

An Administrator can:

- Manage tickets
- Manage assets
- Create user accounts
- Delete user accounts
- View reports

### Technician

A Technician can:

- View tickets
- Edit tickets
- Change ticket status
- Manage assets
- View reports

### User

A User can:

- Sign in
- View the dashboard
- Create tickets
- View tickets

---

## Technologies

- Python
- Flask
- SQLite
- HTML
- CSS
- Jinja
- Werkzeug
- Git
- GitHub

---

## Screenshots

### Login

![Login page](screenshots/login.png)

### Dashboard

![Dashboard](screenshots/dashboard.png)

### Tickets

![Tickets](screenshots/tickets.png)

### Assets

![Assets](screenshots/assets.png)

### Reports

![Reports](screenshots/reports.png)

---

## How to Run the Project

### 1. Clone the repository

```bash
git clone https://github.com/Alialmaz8/falcon-helpdesk.git
cd falcon-helpdesk
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install the required packages

```bash
pip install -r requirements.txt
```

### 5. Create an administrator account

```bash
python create_admin.py
```

Enter your name, username, and password when the program asks for them.

The account information is stored locally in the SQLite database. The password is stored as a hash.

### 6. Start the application

```bash
python app.py
```

You can also start it using Flask debug mode:

```bash
flask --app app run --debug
```

### 7. Open the application

Open this address in your browser:

```text
http://127.0.0.1:5000
```

---

## Project Structure

```text
falcon-helpdesk
│
├── app.py
├── create_admin.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── database
│   └── falcon_helpdesk.db
│       Generated locally and not uploaded to GitHub
│
├── screenshots
│   ├── uae_flag.png
│   ├── abudhabi_flag.png
│   ├── login.png
│   ├── dashboard.png
│   ├── tickets.png
│   ├── assets.png
│   └── reports.png
│
├── static
│   └── css
│       ├── style.css
│       ├── login.css
│       ├── assets.css
│       └── reports.css
│
└── templates
    ├── base.html
    ├── login.html
    ├── dashboard.html
    ├── create_ticket.html
    ├── tickets.html
    ├── ticket_details.html
    ├── edit_ticket.html
    ├── assets.html
    ├── edit_asset.html
    ├── users.html
    └── reports.html
```

The `.secret_key` file and SQLite database are created locally and are excluded from GitHub.

---

## Database Tables

The application uses three main database tables.

### Users

Stores:

- Full name
- Username
- Hashed password
- User role

### Tickets

Stores:

- Requester name
- Department
- Priority
- Category
- Subject
- Description
- Status
- Creation date

### Assets

Stores:

- Asset tag
- Asset name
- Asset type
- Serial number
- Location
- Assigned employee
- Asset status

---

## What I Learned

While working on this project, I practiced:

- Creating routes with Flask
- Using HTML forms
- Reading form information in Python
- Validating submitted information
- Creating and querying SQLite tables
- Using parameterized SQL queries
- Creating login sessions
- Hashing passwords
- Adding role-based permissions
- Using Jinja templates
- Creating reusable page layouts
- Styling pages with CSS
- Using Git commits and GitHub

---

## Possible Future Improvements

Some improvements I may add later are:

- Assigning tickets to specific technicians
- Allowing users to view only their own tickets
- Ticket comments
- File attachments
- Password changes
- Email notifications
- Report charts
- Automated tests

---

## Author

**Ali Mansoor Almazrouei**

Computer Science Student  
California State University, San Bernardino  


GitHub: `Alialmaz8`