import os
from flask import Flask, jsonify, request
from azure.identity import ManagedIdentityCredential
from azure.keyvault.secrets import SecretClient
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Retrieve database password from Azure Key Vault
vault_url = os.environ["KEY_VAULT_URL"]

credential = ManagedIdentityCredential()

secret_client = SecretClient(
    vault_url=vault_url,
    credential=credential
)

db_password = secret_client.get_secret(
    "taskdb-password"
).value


# PostgreSQL connection
def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="taskdb",
        user="taskuser",
        password=db_password,
        cursor_factory=RealDictCursor
    )


# Test application
@app.route("/")
def home():
    return jsonify({
        "message": "DevOps Task Manager API is running!",
        "database": "PostgreSQL",
        "secret_management": "Azure Key Vault"
    })


# Get all tasks
@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM tasks ORDER BY id DESC")
            tasks = cur.fetchall()
        return jsonify(tasks)
    finally:
        conn.close()


# Add a task
@app.route("/api/tasks", methods=["POST"])
def add_task():
    data = request.get_json(silent=True) or {}
    title = data.get("title")

    if not isinstance(title, str) or not title.strip():
        return jsonify({"error": "Task title is required"}), 400

    conn = get_db_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO tasks (title) VALUES (%s) RETURNING id",
                    (title.strip(),)
                )
                task_id = cur.fetchone()["id"]

        return jsonify({
            "message": "Task created",
            "id": task_id
        }), 201
    finally:
        conn.close()


# Delete a task
@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    conn = get_db_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM tasks WHERE id = %s",
                    (task_id,)
                )
                deleted = cur.rowcount

        if deleted == 0:
            return jsonify({"error": "Task not found"}), 404

        return jsonify({"message": "Task deleted"})
    finally:
        conn.close()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
