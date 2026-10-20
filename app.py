
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash
)
from db import connect_db

app = Flask(__name__)
app.secret_key = "student-management-local-key"


# Home page, Search and Dashboard
@app.route("/")
def index():
    search_query = request.args.get("q", "").strip()
    connection = connect_db()

    if connection is None:
        return "Database connection failed. Check db.py and MySQL."

    cursor = None

    try:
        cursor = connection.cursor()

        # Search students by name or course
        if search_query:
            query = """
                SELECT * FROM students
                WHERE name LIKE %s OR course LIKE %s
                ORDER BY id
            """
            search_value = "%" + search_query + "%"
            cursor.execute(query, (search_value, search_value))
        else:
            cursor.execute("SELECT * FROM students ORDER BY id")

        students = cursor.fetchall()

        # Dashboard: total students
        cursor.execute("SELECT COUNT(*) FROM students")
        total_students = cursor.fetchone()[0]

        # Dashboard: total unique courses
        cursor.execute(
            """
            SELECT COUNT(DISTINCT course)
            FROM students
            WHERE course IS NOT NULL AND course != ''
            """
        )
        total_courses = cursor.fetchone()[0]

        return render_template(
            "index.html",
            students=students,
            search_query=search_query,
            total_students=total_students,
            total_courses=total_courses
        )

    except Exception as error:
        print("Error loading students:", error)
        return "Unable to load student records. Check the terminal."

    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


# Add Student
@app.route("/add", methods=["POST"])
def add_student():
    name = request.form.get("name", "").strip()
    age_text = request.form.get("age", "").strip()
    course = request.form.get("course", "").strip()
    email = request.form.get("email", "").strip()

    if not name:
        flash("Student name is required.", "error")
        return redirect(url_for("index"))

    age = None

    if age_text:
        try:
            age = int(age_text)
            if age <= 0:
                flash("Age must be greater than zero.", "error")
                return redirect(url_for("index"))
        except ValueError:
            flash("Please enter a valid age.", "error")
            return redirect(url_for("index"))

    connection = connect_db()

    if connection is None:
        return "Database connection failed."

    cursor = None

    try:
        cursor = connection.cursor()

        query = """
            INSERT INTO students (name, age, course, email)
            VALUES (%s, %s, %s, %s)
        """

        cursor.execute(query, (name, age, course, email))
        connection.commit()

        flash("Student added successfully!", "success")

    except Exception as error:
        connection.rollback()
        print("Error adding student:", error)
        flash("Unable to add student.", "error")

    finally:
        if cursor is not None:
            cursor.close()
        connection.close()

    return redirect(url_for("index"))


# Edit Student: show existing details
@app.route("/edit/<int:student_id>")
def edit_student(student_id):
    connection = connect_db()

    if connection is None:
        return "Database connection failed."

    cursor = None

    try:
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM students WHERE id = %s",
            (student_id,)
        )

        student = cursor.fetchone()

        if student is None:
            flash("Student not found.", "error")
            return redirect(url_for("index"))

        return render_template("edit.html", student=student)

    except Exception as error:
        print("Error loading student:", error)
        return "Unable to load student details."

    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


# Update Student
@app.route("/update/<int:student_id>", methods=["POST"])
def update_student(student_id):
    name = request.form.get("name", "").strip()
    age_text = request.form.get("age", "").strip()
    course = request.form.get("course", "").strip()
    email = request.form.get("email", "").strip()

    if not name:
        flash("Student name is required.", "error")
        return redirect(url_for("edit_student", student_id=student_id))

    age = None

    if age_text:
        try:
            age = int(age_text)
            if age <= 0:
                flash("Age must be greater than zero.", "error")
                return redirect(
                    url_for("edit_student", student_id=student_id)
                )
        except ValueError:
            flash("Please enter a valid age.", "error")
            return redirect(
                url_for("edit_student", student_id=student_id)
            )

    connection = connect_db()

    if connection is None:
        return "Database connection failed."

    cursor = None

    try:
        cursor = connection.cursor()

        query = """
            UPDATE students
            SET name = %s, age = %s, course = %s, email = %s
            WHERE id = %s
        """

        cursor.execute(
            query,
            (name, age, course, email, student_id)
        )
        connection.commit()

        if cursor.rowcount > 0:
            flash("Student updated successfully!", "success")
        else:
            flash("Student details unchanged or student not found.", "error")

    except Exception as error:
        connection.rollback()
        print("Error updating student:", error)
        flash("Unable to update student.", "error")

    finally:
        if cursor is not None:
            cursor.close()
        connection.close()

    return redirect(url_for("index"))


# Delete Student
@app.route("/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    connection = connect_db()

    if connection is None:
        return "Database connection failed."

    cursor = None

    try:
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM students WHERE id = %s",
            (student_id,)
        )
        connection.commit()

        if cursor.rowcount > 0:
            flash("Student deleted successfully!", "success")
        else:
            flash("Student not found.", "error")

    except Exception as error:
        connection.rollback()
        print("Error deleting student:", error)
        flash("Unable to delete student.", "error")

    finally:
        if cursor is not None:
            cursor.close()
        connection.close()

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
