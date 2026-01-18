import sqlite3

# ===============================
# DATABASE CONNECTION UTILITIES
# ===============================

def connect_db():
    """
    Establish and return a connection to the 'ebookstore' database.
    Using 'with' statements ensures the connection is safely managed.
    """
    return sqlite3.connect("ebookstore.db")


def create_tables():
    """
    Create the required tables: 'book' and 'author'.
    Each table is created only if it doesn't already exist.
    """
    with connect_db() as conn:
        cursor = conn.cursor()

        # Create the 'author' table to store author details.
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS author (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                country TEXT NOT NULL
            )
        ''')

        # Create the 'book' table with a foreign key linking to 'author'.
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS book (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                authorID INTEGER NOT NULL,
                qty INTEGER NOT NULL,
                FOREIGN KEY (authorID) REFERENCES author(id)
            )
        ''')

        conn.commit()  # Save table creation changes


# ===============================
# DATABASE SEEDING (INITIAL DATA)
# ===============================

def populate_tables():
    """
    Populate both 'author' and 'book' tables with sample data if they are empty.
    """
    with connect_db() as conn:
        cursor = conn.cursor()

        # Check if author table already has data
        cursor.execute("SELECT COUNT(*) FROM author")
        if cursor.fetchone()[0] == 0:
            authors = [
                (1290, "Charles Dickens", "England"),
                (8937, "J.K. Rowling", "England"),
                (2356, "C.S. Lewis", "Ireland"),
                (6380, "J.R.R. Tolkien", "South Africa"),
                (5620, "Lewis Carroll", "England")
            ]
            cursor.executemany("INSERT INTO author VALUES (?, ?, ?)", authors)

        # Check if book table already has data
        cursor.execute("SELECT COUNT(*) FROM book")
        if cursor.fetchone()[0] == 0:
            books = [
                (3001, "A Tale of Two Cities", 1290, 30),
                (3002, "Harry Potter and the Philosopher's Stone", 8937, 40),
                (3003, "The Lion, the Witch and the Wardrobe", 2356, 25),
                (3004, "The Lord of the Rings", 6380, 37),
                (3005, "Alice's Adventures in Wonderland", 5620, 12)
            ]
            cursor.executemany("INSERT INTO book VALUES (?, ?, ?, ?)", books)

        conn.commit()


# ===============================
# MENU FUNCTIONALITIES
# ===============================

def enter_book():
    """Add a new book to the database."""
    try:
        # Gather input data from the user
        id = int(input("Enter book ID (4 digits): "))
        title = input("Enter book title: ").strip()
        authorID = int(input("Enter author ID (4 digits): "))
        qty = int(input("Enter quantity: "))

        # Insert data into the book table
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO book VALUES (?, ?, ?, ?)", (id, title, authorID, qty))
            conn.commit()
            print(f"\n✅ Book '{title}' successfully added.\n")
    except Exception as e:
        print("❌ Error adding book:", e)


def update_book():
    """Update an existing book's information (title, authorID, or quantity)."""
    try:
        book_id = int(input("Enter the ID of the book to update: "))

        # Display update options to the user
        print("\nUpdate Options:")
        print("1. Quantity")
        print("2. Title")
        print("3. Author ID")
        print("4. Author Name/Country")
        choice = input("Enter your choice (1-4): ")

        with connect_db() as conn:
            cursor = conn.cursor()

            # Option 1: Update quantity
            if choice == "1":
                qty = int(input("Enter new quantity: "))
                cursor.execute("UPDATE book SET qty = ? WHERE id = ?", (qty, book_id))

            # Option 2: Update title
            elif choice == "2":
                title = input("Enter new title: ")
                cursor.execute("UPDATE book SET title = ? WHERE id = ?", (title, book_id))

            # Option 3: Update author ID
            elif choice == "3":
                authorID = int(input("Enter new author ID: "))
                cursor.execute("UPDATE book SET authorID = ? WHERE id = ?", (authorID, book_id))

            # Option 4: Update author details (name and country)
            elif choice == "4":
                cursor.execute('''
                    SELECT a.id, a.name, a.country FROM author a
                    JOIN book b ON a.id = b.authorID
                    WHERE b.id = ?
                ''', (book_id,))
                author = cursor.fetchone()

                if author:
                    print(f"\nCurrent Author: {author[1]} ({author[2]})")
                    new_name = input("Enter new author name (leave blank to keep current): ").strip() or author[1]
                    new_country = input("Enter new country (leave blank to keep current): ").strip() or author[2]

                    cursor.execute("UPDATE author SET name = ?, country = ? WHERE id = ?", (new_name, new_country, author[0]))
                else:
                    print("❌ Author not found for this book.")
            else:
                print("⚠️ Invalid choice.")

            conn.commit()
            print("\n✅ Book/Author updated successfully.\n")

    except Exception as e:
        print("❌ Error updating book:", e)


def delete_book():
    """Remove a book record from the database."""
    try:
        book_id = int(input("Enter the ID of the book to delete: "))
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM book WHERE id = ?", (book_id,))
            conn.commit()
            print(f"\n🗑️ Book with ID {book_id} deleted successfully.\n")
    except Exception as e:
        print("❌ Error deleting book:", e)


def search_books():
    """Search for books by title (partial match allowed)."""
    keyword = input("Enter a keyword to search for: ").strip()
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM book WHERE title LIKE ?", ('%' + keyword + '%',))
        results = cursor.fetchall()

        if results:
            print("\n🔎 Search Results:")
            for row in results:
                print(f"ID: {row[0]}, Title: {row[1]}, Author ID: {row[2]}, Quantity: {row[3]}")
        else:
            print("❌ No books found with that keyword.")


def view_all_books():
    """Display all book details, including author name and country."""
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT b.title, a.name, a.country
            FROM book b
            INNER JOIN author a ON b.authorID = a.id
        ''')
        results = cursor.fetchall()

        print("\n📚 Book Details:")
        for title, name, country in results:
            print(f"""
Title: {title}
Author's Name: {name}
Author's Country: {country}
            """)


# ===============================
# MAIN MENU
# ===============================

def main():
    """Main menu that allows the clerk to interact with the system."""
    create_tables()
    populate_tables()

    while True:
        print("\n====== EBOOKSTORE MENU ======")
        print("1. Enter book")
        print("2. Update book")
        print("3. Delete book")
        print("4. Search books")
        print("5. View details of all books")
        print("0. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            enter_book()
        elif choice == "2":
            update_book()
        elif choice == "3":
            delete_book()
        elif choice == "4":
            search_books()
        elif choice == "5":
            view_all_books()
        elif choice == "0":
            print("👋 Goodbye! Have a great day.")
            break
        else:
            print("⚠️ Invalid selection. Please choose again.")


# Run the program when the file is executed
if __name__ == "__main__":
    main()
