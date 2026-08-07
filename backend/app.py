from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import os
import time

app = Flask(__name__)
CORS(app)


def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "mysql-service"),
        user=os.getenv("DB_USER", "studentuser"),
        password=os.getenv("DB_PASSWORD", "studentpass"),
        database=os.getenv("DB_NAME", "studentdb")
    )


def initialize_database():
    for attempt in range(10):
        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(100) NOT NULL,
                    course VARCHAR(100) NOT NULL
                )
            """)

            connection.commit()
            cursor.close()
            connection.close()

            print("Database initialized successfully")
            return

        except mysql.connector.Error as error:
            print(f"Database connection failed: {error}")
            print("Retrying in 5 seconds...")
            time.sleep(5)

    print("Could not connect to database")


@app.route("/")
def home():
    return jsonify({
        "message": "Student Management API is running"
    })


@app.route("/students", methods=["GET"])
def get_students():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()

        cursor.close()
        connection.close()

        return jsonify(students)

    except mysql.connector.Error as error:
        return jsonify({"error": str(error)}), 500


@app.route("/students", methods=["POST"])
def add_student():
    try:
        data = request.get_json()

        name = data.get("name")
        email = data.get("email")
        course = data.get("course")

        if not name or not email or not course:
            return jsonify({
                "error": "Name, email and course are required"
            }), 400

        connection = get_db_connection()
        cursor = connection.cursor()

        query = """
            INSERT INTO students (name, email, course)
            VALUES (%s, %s, %s)
        """

        cursor.execute(query, (name, email, course))
        connection.commit()

        student_id = cursor.lastrowid

        cursor.close()
        connection.close()

        return jsonify({
            "message": "Student added successfully",
            "id": student_id
        }), 201

    except mysql.connector.Error as error:
        return jsonify({"error": str(error)}), 500


@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM students WHERE id = %s",
            (student_id,)
        )

        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({
            "message": "Student deleted successfully"
        })

    except mysql.connector.Error as error:
        return jsonify({"error": str(error)}), 500


if __name__ == "__main__":
    initialize_database()

    app.run(
        host="0.0.0.0",
        port=5000
    )