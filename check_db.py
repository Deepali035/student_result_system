import sqlite3

conn = sqlite3.connect('students.db')
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS students")
cursor.execute("DROP TABLE IF EXISTS marks")

cursor.execute("""CREATE TABLE students(
               roll_no INTEGER PRIMARY KEY , name TEXT, student_class INTEGER)""")

cursor.execute("""CREATE TABLE marks(
               roll_no INTEGER, math INTEGER, english INTEGER, science INTEGER,
               FOREIGN KEY (roll_no) REFERENCES students(roll_no))""")

conn.commit()
conn.close()

print("Tables created successfully!")