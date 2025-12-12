from flask import Flask, request, jsonify
import psycopg2
from database import get_connection
from utils import normalize_email   # вложенная функция импортируется отсюда

app = Flask(__name__)



#        CREATE USER
@app.route("/users", methods=["POST"])
def create_user():
    data = request.json

    name = data.get("name")

    #  Тут используется ВЛОЖЕННАЯ ФУНКЦИЯ
    email = normalize_email(data.get("email"))  # вложенная функция
    #  Это вызов функции из другого файла utils.py

    password = data.get("password")

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s) RETURNING id;",
            (name, email, password)
        )

        user_id = cur.fetchone()[0]
        conn.commit()

        return jsonify({"status": "success", "user_id": user_id}), 201

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

    finally:
        cur.close()
        conn.close()


#        GET USER
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT id, name, email FROM users WHERE id = %s;", (user_id,))
        row = cur.fetchone()

        if not row:
            return jsonify({"status": "not_found"}), 404

        user_data = {
            "id": row[0],
            "name": row[1],
            "email": row[2]
        }

        return jsonify(user_data), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

    finally:
        cur.close()
        conn.close()



#        RUN APP
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)

