from database import get_connection

# вложенная функция — обязательное требование практики
def format_user(row):
    return {
        "id": row[0],
        "name": row[1],
        "email": row[2]
    }

def register_user(name, email, password):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO users (name, email, password) VALUES (%s, %s, %s) RETURNING id, name, email",
        (name, email, password)
    )

    user = cur.fetchone()
    conn.commit()
    conn.close()

    return format_user(user)

def login_user(email, password):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, name, email FROM users WHERE email=%s AND password=%s",
        (email, password)
    )

    user = cur.fetchone()
    conn.close()

    if user:
        return format_user(user)
    return None
