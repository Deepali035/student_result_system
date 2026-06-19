import sqlite3

conn = sqlite3.connect('students.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE students(
    roll_no INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    student_class INTEGER NOT NULL
)
''')

cursor.execute('''
CREATE TABLE marks(
    roll_no INTEGER PRIMARY KEY AUTOINCREMENT,
    student_class INTEGER,
    math INTEGER,
    science INTEGER,
    english INTEGER
)
''')

conn.commit()
conn.close()

print("Database created successfully!")