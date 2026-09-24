import sqlite3


DB_PATH = "library.db"

def create_database():
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
   
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            book_id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            quantity INTEGER NOT NULL
        )
    """)
    
   
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reservations (
            reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER,
            student_id TEXT NOT NULL,
            reserved_date TEXT DEFAULT (datetime('now', 'localtime')),
            status TEXT DEFAULT 'Reserved',
            FOREIGN KEY (book_id) REFERENCES inventory(book_id)
        )
    """)

    dummy_books = [
            (101, "Hands-On Machine Learning with Scikit-Learn", 3),
            (102, "Deep Learning with Python", 2),
            (103, "Clean Code: A Handbook of Agile Software Craftsmanship", 5),
            (104, "Introduction to Algorithms", 1)
        ]
    cursor.executemany("INSERT INTO inventory VALUES (?, ?, ?)", dummy_books)
    print("Dummy data successfully inserted into inventory.")

    conn.commit()
    conn.close()
    print(f"Database created successfully at: {DB_PATH}")

if __name__ == "__main__":
    create_database()