# 📚 Ebookstore Database Management System

A Python-based command-line application that manages an ebook inventory using a relational SQLite database.  
This project demonstrates database design, CRUD operations, and structured Python programming.

---

## 🔍 Project Overview

This application simulates a small ebookstore system where a user (clerk/admin) can:

- Manage books and authors
- Store data persistently using SQLite
- Perform full CRUD operations
- Query and join relational tables

The system is built with clean modular functions and follows best practices for database interaction.

---

## 🧠 Key Features

- Relational database design (`book` and `author` tables)
- Foreign key relationships
- Create, read, update, and delete (CRUD) operations
- Partial keyword search
- SQL joins to display enriched book details
- Persistent local database (`ebookstore.db`)
- Menu-driven command-line interface

---

## 🛠️ Technologies Used

- **Python**
- **SQLite**
- **SQL**
- Standard Library: `sqlite3`

---

## 🗂️ Database Schema

**Author Table**
- `id` (Primary Key)
- `name`
- `country`

**Book Table**
- `id` (Primary Key)
- `title`
- `authorID` (Foreign Key)
- `qty`

---

## ▶️ How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/caleb-05y/ebookstore-database.git
2. Navigate to the project folder:
   cd ebookstore-database

3. Run the application:
   python ebookstore.py
