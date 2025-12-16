import pytest
from user_service import register_user, login_user
from database import get_connection


@pytest.fixture(scope="module", autouse=True)
def prepare_database():
    """
    Фикстура подготавливает базу данных для интеграционных тестов.

    Здесь используется реальное подключение к PostgreSQL.
    Таблица users создаётся, если она не существует.
    Перед выполнением тестов данные очищаются.
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        );
    """)

    cur.execute("DELETE FROM users;")
    conn.commit()

    cur.close()
    conn.close()


def test_register_user_integration():
    """
    Интеграционный тест регистрации пользователя.

    Проверяется, что:
    - пользователь сохраняется в реальной базе данных;
    - функция возвращает корректные данные пользователя.
    """
    user = register_user(
        name="Ivan",
        email="ivan@test.com",
        password="1234"
    )

    assert user["id"] is not None
    assert user["name"] == "Ivan"
    assert user["email"] == "ivan@test.com"


def test_login_user_success_integration():
    """
    Интеграционный тест успешной авторизации пользователя.

    Проверяется, что пользователь,
    сохранённый в базе данных,
    может быть получен по email и password.
    """
    user = login_user(
        email="ivan@test.com",
        password="1234"
    )

    assert user is not None
    assert user["email"] == "ivan@test.com"


def test_login_user_not_found_integration():
    """
    Интеграционный тест случая,
    когда пользователь не найден в базе данных.
    """
    user = login_user(
        email="unknown@test.com",
        password="wrong"
    )

    assert user is None
