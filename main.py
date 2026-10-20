
from db import connect_db


# 1. Add Student
def add_student():
    name = input("Enter student name: ").strip()

    if not name:
        print("Student name cannot be empty!")
        return

    try:
        age = int(input("Enter student age: "))

        if age <= 0:
            print("Age must be greater than zero!")
            return

    except ValueError:
        print("Please enter a valid age!")
        return

    course = input("Enter course name: ").strip()
    email = input("Enter student email: ").strip()

    connection = connect_db()

    if connection is None:
        print("Database connection failed!")
        return

    cursor = None

    try:
        cursor = connection.cursor()

        query = """
        INSERT INTO students (name, age, course, email)
        VALUES (%s, %s, %s, %s)
        """

        values = (name, age, course, email)

        cursor.execute(query, values)
        connection.commit()

        print("Student added successfully!")
        print("Student ID:", cursor.lastrowid)

    except Exception as error:
        connection.rollback()
        print("Error adding student:", error)

    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


# 2. View All Students
def view_students():
    connection = connect_db()

    if connection is None:
        print("Database connection failed!")
        return

    cursor = None

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM students ORDER BY id")

        students = cursor.fetchall()

        if not students:
            print("No student records found.")
        else:
            print("\n========== STUDENT RECORDS ==========")

            for student in students:
                print("\nID:", student[0])
                print("Name:", student[1])
                print("Age:", student[2])
                print("Course:", student[3])
                print("Email:", student[4])
                print("-------------------------------------")

    except Exception as error:
        print("Error viewing students:", error)

    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


# 3. Search Student by ID
def search_student():
    try:
        student_id = int(input("Enter student ID to search: "))

        if student_id <= 0:
            print("Student ID must be greater than zero!")
            return

    except ValueError:
        print("Please enter a valid numeric ID!")
        return

    connection = connect_db()

    if connection is None:
        print("Database connection failed!")
        return

    cursor = None

    try:
        cursor = connection.cursor()

        query = "SELECT * FROM students WHERE id = %s"
        cursor.execute(query, (student_id,))

        student = cursor.fetchone()

        if student is None:
            print("Student not found!")
        else:
            print("\n========== STUDENT DETAILS ==========")
            print("ID:", student[0])
            print("Name:", student[1])
            print("Age:", student[2])
            print("Course:", student[3])
            print("Email:", student[4])
            print("=====================================")

    except Exception as error:
        print("Error searching student:", error)

    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


# 4. Update Student
def update_student():
    try:
        student_id = int(input("Enter student ID to update: "))

        if student_id <= 0:
            print("Student ID must be greater than zero!")
            return

    except ValueError:
        print("Please enter a valid numeric ID!")
        return

    connection = connect_db()

    if connection is None:
        print("Database connection failed!")
        return

    cursor = None

    try:
        cursor = connection.cursor()

        # Check whether student exists
        cursor.execute(
            "SELECT * FROM students WHERE id = %s",
            (student_id,)
        )

        student = cursor.fetchone()

        if student is None:
            print("Student not found!")
            return

        print("\nCurrent Student Details")
        print("Name:", student[1])
        print("Age:", student[2])
        print("Course:", student[3])
        print("Email:", student[4])

        # Enter updated details
        name = input("Enter new name: ").strip()

        try:
            age = int(input("Enter new age: "))

            if age <= 0:
                print("Age must be greater than zero!")
                return

        except ValueError:
            print("Please enter a valid age!")
            return

        course = input("Enter new course: ").strip()
        email = input("Enter new email: ").strip()

        if not name or not course or not email:
            print("Name, course and email cannot be empty!")
            return

        # Update record
        query = """
        UPDATE students
        SET name = %s, age = %s, course = %s, email = %s
        WHERE id = %s
        """

        values = (name, age, course, email, student_id)

        cursor.execute(query, values)
        connection.commit()

        print("Student details updated successfully!")

    except Exception as error:
        connection.rollback()
        print("Error updating student:", error)

    finally:
        if cursor is not None:
            cursor.close()

        connection.close()


# 5. Delete Student
def delete_student():
    try:
        student_id = int(input("Enter student ID to delete: "))

        if student_id <= 0:
            print("Student ID must be greater than zero!")
            return

    except ValueError:
        print("Please enter a valid numeric ID!")
        return

    connection = connect_db()

    if connection is None:
        print("Database connection failed!")
        return

    cursor = None

    try:
        cursor = connection.cursor()

        # Check whether student exists
        query = "SELECT * FROM students WHERE id = %s"
        cursor.execute(query, (student_id,))

        student = cursor.fetchone()

        if student is None:
            print("Student not found!")
            return

        print("\nStudent Details")
        print("ID:", student[0])
        print("Name:", student[1])
        print("Age:", student[2])
        print("Course:", student[3])
        print("Email:", student[4])

        confirm = input(
            "Are you sure you want to delete this student? (yes/no): "
        ).strip().lower()

        if confirm != "yes":
            print("Deletion cancelled.")
            return

        # Delete student
        query = "DELETE FROM students WHERE id = %s"
        cursor.execute(query, (student_id,))
        connection.commit()

        print("Student deleted successfully!")

    except Exception as error:
        connection.rollback()
        print("Error deleting student:", error)

    finally:
        if cursor is not None:
            cursor.close()

        connection.close()


# 6. Main Menu
def main():
    while True:
        print("\n================================")
        print("   STUDENT MANAGEMENT SYSTEM")
        print("================================")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Exit")
        print("================================")

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            search_student()
        elif choice == "4":
            update_student()
        elif choice == "5":
            delete_student()
        elif choice == "6":
            print("Thank you for using the system!")
            break
        else:
            print("Invalid choice! Please enter 1, 2, 3, 4, 5, or 6.")


# Start Program
if __name__ == "__main__":
    main()
