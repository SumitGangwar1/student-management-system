
import os
import mysql.connector


def connect_db():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "student_db")
        )

        if connection.is_connected():
            print("MySQL Database Connected Successfully!")

        return connection

    except mysql.connector.Error as error:
        print("Database connection failed:", error)
        return None


if __name__ == "__main__":
    db = connect_db()

    if db is not None:
        db.close()
        print("Database connection closed.")
