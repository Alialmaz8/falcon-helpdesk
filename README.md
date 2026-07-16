<div align="center">

# 🟥⬜ 🇦🇪 Falcon HelpDesk

### IT Support and Ticket Management System

Built by an Emirati Computer Science student from Abu Dhabi studying in California.

</div>

---

## About the Project

Falcon HelpDesk is a web-based IT support and ticket management system developed using **Python**, **Flask**, and **SQLite**.

The project was created to practice full-stack web development concepts, including user authentication, database management, CRUD operations, role-based access, and responsive user interface design.

---

## Features

- Secure login system
- Password hashing
- Administrator, Technician, and User accounts
- Create support tickets
- View ticket details
- Edit tickets
- Delete tickets
- Update ticket status
- Search and filter tickets
- Dashboard with live statistics
- Asset inventory management
- Search and edit assets
- User management
- Reports dashboard
- Responsive interface

---

## User Roles

### Administrator

- Full access to the system
- Manage users
- Manage tickets
- Manage assets
- View reports

### Technician

- View assigned tickets
- Update ticket status
- Manage assets
- View reports

### User

- Create tickets
- View tickets
- View dashboard

---

## Technologies Used

- Python
- Flask
- SQLite
- HTML5
- CSS3
- Jinja2
- Werkzeug
- Git
- GitHub

---

# Screenshots

## Login Page

![Login](screenshots/login.png)

---

## Dashboard

![Dashboard](screenshots/dashboard.png)

---

## Tickets

![Tickets](screenshots/tickets.png)

---

## Assets

![Assets](screenshots/assets.png)

---

## Reports

![Reports](screenshots/reports.png)

---

# Installation

Clone the repository.

```bash
git clone https://github.com/Alialmaz8/falcon-helpdesk.git
cd falcon-helpdesk
```

Create a virtual environment.

```bash
python -m venv .venv
```

Activate it.

### Windows

```powershell
.\.venv\Scripts\activate
```

Install the required packages.

```bash
pip install -r requirements.txt
```

Run the application.

```bash
flask --app app run --debug
```

Open your browser and visit:

```
http://127.0.0.1:5000
```

---

# Project Structure

```
falcon-helpdesk
│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── database
│   └── falcon_helpdesk.db
│
├── screenshots
│   ├── login.png
│   ├── dashboard.png
│   ├── tickets.png
│   ├── assets.png
│   └── reports.png
│
├── static
│   ├── css
│   ├── images
│   └── js
│
└── templates
    ├── base.html
    ├── dashboard.html
    ├── login.html
    ├── create_ticket.html
    ├── tickets.html
    ├── ticket_details.html
    ├── edit_ticket.html
    ├── assets.html
    ├── edit_asset.html
    ├── users.html
    ├── reports.html
    └── settings.html
```

---

# What I Learned

While building this project I practiced:

- Flask routing
- SQLite database design
- SQL queries
- CRUD operations
- User authentication
- Password hashing
- Session management
- Jinja templates
- HTML forms
- CSS layout and responsive design
- Git and GitHub workflow

---

# Future Improvements

Some features that could be added in future versions include:

- Email notifications
- File attachments for tickets
- Charts and graphs in reports
- Asset maintenance history
- Dark mode
- REST API
- Password reset by email

---

# Author

**Ali Mansoor Almazrouei**

🇦🇪 Abu Dhabi, United Arab Emirates

Computer Science Student

California State University, San Bernardino

GitHub:
https://github.com/Alialmaz8

---

## License

