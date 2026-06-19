import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/add_student', methods=['GET', 'POST'])
def add_student():

    if request.method == 'POST':

        name = request.form['name']
        roll_no = int(request.form['roll_no'])
        student_class = request.form['student_class']

        try:
            with sqlite3.connect('students.db') as conn:
                cursor = conn.cursor()

                cursor.execute(
                    """
                    INSERT INTO students (name, roll_no, student_class)
                    VALUES (?, ?, ?)
                    """,
                    (name, roll_no, student_class)
                )

                conn.commit()

            return redirect(url_for('add_marks'))

        except sqlite3.IntegrityError:
            return "Roll number already exists."

    return render_template('add_student.html')


@app.route('/add_marks', methods=['GET', 'POST'])
def add_marks():

    if request.method == 'POST':

        roll_no = int(request.form['roll_no'])
        math = int(request.form['math'])
        english = int(request.form['english'])
        science = int(request.form['science'])

        with sqlite3.connect('students.db') as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO marks (roll_no, math, english, science)
                VALUES (?, ?, ?, ?)
                """,
                (roll_no, math, english, science)
            )

            conn.commit()

        return redirect(url_for('result', roll_no=roll_no))

    return render_template('add_marks.html')


@app.route('/result/<int:roll_no>')
def result(roll_no):

    with sqlite3.connect('students.db') as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                students.name,
                students.roll_no,
                students.student_class,
                marks.math,
                marks.science,
                marks.english
            FROM students
            JOIN marks
                ON students.roll_no = marks.roll_no
            WHERE students.roll_no = ?
            """,
            (roll_no,)
        )

        data = cursor.fetchone()

    if data is None:
        return "Student not found!"

    name = data[0]
    roll_no = data[1]
    student_class = data[2]
    math = int(data[3])
    science = int(data[4])
    english = int(data[5])

    total = math + science + english
    percentage = (total / 300) * 100

    if percentage >= 90:
        grade = "A+"
    elif percentage >= 80:
        grade = "A"
    elif percentage >= 70:
        grade = "B"
    else:
        grade = "C"

    return render_template(
        'result.html',
        name=name,
        roll_no=roll_no,
        student_class=student_class,
        math=math,
        science=science,
        english=english,
        total=total,
        percentage=round(percentage, 2),
        grade=grade
    )


if __name__ == '__main__':
    app.run(debug=True)