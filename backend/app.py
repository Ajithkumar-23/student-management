from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import os
import time


app = Flask(__name__)

CORS(app)



def get_connection():

    return mysql.connector.connect(

        host=os.getenv("DB_HOST","mysql-service"),

        user=os.getenv("DB_USER","studentuser"),

        password=os.getenv("DB_PASSWORD","studentpass"),

        database=os.getenv("DB_NAME","studentdb"),

        port=3306

    )





@app.route("/")
def home():

    return jsonify({

        "message":"Student Management API is running"

    })





@app.route("/students",methods=["GET"])
def get_students():


    conn=get_connection()

    cursor=conn.cursor(dictionary=True)


    cursor.execute("SELECT * FROM students")


    data=cursor.fetchall()


    cursor.close()

    conn.close()


    return jsonify(data)






@app.route("/students",methods=["POST"])
def add_student():


    data=request.get_json()


    name=data["name"]

    email=data["email"]

    course=data["course"]



    conn=get_connection()

    cursor=conn.cursor()



    cursor.execute(

        """
        INSERT INTO students(name,email,course)
        VALUES(%s,%s,%s)
        """,

        (name,email,course)

    )


    conn.commit()


    student_id=cursor.lastrowid


    cursor.close()

    conn.close()



    return jsonify({

        "message":"Student added successfully",

        "id":student_id

    })







@app.route("/students/<int:id>",methods=["DELETE"])
def delete_student(id):


    conn=get_connection()

    cursor=conn.cursor()


    cursor.execute(

        "DELETE FROM students WHERE id=%s",

        (id,)

    )


    conn.commit()


    cursor.close()

    conn.close()



    return jsonify({

        "message":"Student deleted successfully"

    })







if __name__=="__main__":


    app.run(

        host="0.0.0.0",

        port=5000

    )