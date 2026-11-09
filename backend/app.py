from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import mysql.connector
import os

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# CORS configuration
frontend_origin = os.getenv("FRONTEND_ORIGIN", "*")
CORS(app, resources={r"/*": {"origins": frontend_origin}})


# Database configuration
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "port": int(os.getenv("DB_PORT", 3306))
}


# Database connection function
def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)


# Home API
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Employee Management API is running"
    })


# Health check API
@app.route("/health", methods=["GET"])
def health():
    try:
        conn = get_db_connection()
        conn.close()

        return jsonify({
            "status": "healthy",
            "database": "connected"
        })

    except mysql.connector.Error:
        app.logger.exception("Database health check failed")

        return jsonify({
            "status": "unhealthy",
            "database": "disconnected"
        }), 500


# GET: Retrieve all employees
@app.route("/employees", methods=["GET"])
def get_employees():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM employees ORDER BY id"
        )

        employees = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(employees)

    except mysql.connector.Error:
        app.logger.exception("Failed to retrieve employees")

        return jsonify({
            "error": "Unable to retrieve employees"
        }), 500


# POST: Add a new employee
@app.route("/employees", methods=["POST"])
def add_employee():

    data = request.get_json(silent=True) or {}

    required_fields = [
        "name",
        "email",
        "department",
        "salary"
    ]

    if not all(data.get(field) not in (None, "") for field in required_fields):
        return jsonify({
            "error": "All fields are required"
        }), 400

    try:
        salary = float(data["salary"])

        if salary < 0:
            return jsonify({
                "error": "Salary cannot be negative"
            }), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO employees
            (name, email, department, salary)
            VALUES (%s, %s, %s, %s)
        """

        values = (
            data["name"].strip(),
            data["email"].strip(),
            data["department"].strip(),
            salary
        )

        cursor.execute(query, values)

        conn.commit()

        employee_id = cursor.lastrowid

        cursor.close()
        conn.close()

        return jsonify({
            "message": "Employee added successfully",
            "id": employee_id
        }), 201

    except ValueError:
        return jsonify({
            "error": "Salary must be a valid number"
        }), 400

    except mysql.connector.Error:
        app.logger.exception("Failed to add employee")

        return jsonify({
            "error": "Unable to add employee. Check the email and database."
        }), 500


# GET: Retrieve one employee
@app.route("/employees/<int:employee_id>", methods=["GET"])
def get_employee(employee_id):

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM employees WHERE id = %s",
            (employee_id,)
        )

        employee = cursor.fetchone()

        cursor.close()
        conn.close()

        if employee is None:
            return jsonify({
                "error": "Employee not found"
            }), 404

        return jsonify(employee)

    except mysql.connector.Error:
        app.logger.exception("Failed to retrieve employee")

        return jsonify({
            "error": "Unable to retrieve employee"
        }), 500


# PUT: Update an employee
@app.route("/employees/<int:employee_id>", methods=["PUT"])
def update_employee(employee_id):

    data = request.get_json(silent=True) or {}

    required_fields = [
        "name",
        "email",
        "department",
        "salary"
    ]

    if not all(data.get(field) not in (None, "") for field in required_fields):
        return jsonify({
            "error": "All fields are required"
        }), 400

    try:
        salary = float(data["salary"])

        if salary < 0:
            return jsonify({
                "error": "Salary cannot be negative"
            }), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            UPDATE employees
            SET name = %s,
                email = %s,
                department = %s,
                salary = %s
            WHERE id = %s
        """

        values = (
            data["name"].strip(),
            data["email"].strip(),
            data["department"].strip(),
            salary,
            employee_id
        )

        cursor.execute(query, values)

        updated = cursor.rowcount

        conn.commit()

        cursor.close()
        conn.close()

        if updated == 0:
            return jsonify({
                "error": "Employee not found or no changes made"
            }), 404

        return jsonify({
            "message": "Employee updated successfully"
        })

    except ValueError:
        return jsonify({
            "error": "Salary must be a valid number"
        }), 400

    except mysql.connector.Error:
        app.logger.exception("Failed to update employee")

        return jsonify({
            "error": "Unable to update employee. Check the email and database."
        }), 500


# DELETE: Delete an employee
@app.route("/employees/<int:employee_id>", methods=["DELETE"])
def delete_employee(employee_id):

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM employees WHERE id = %s",
            (employee_id,)
        )

        deleted = cursor.rowcount

        conn.commit()

        cursor.close()
        conn.close()

        if deleted == 0:
            return jsonify({
                "error": "Employee not found"
            }), 404

        return jsonify({
            "message": "Employee deleted successfully"
        })

    except mysql.connector.Error:
        app.logger.exception("Failed to delete employee")

        return jsonify({
            "error": "Unable to delete employee"
        }), 500


# Start Flask server
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
