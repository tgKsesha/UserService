from unittest.mock import MagicMock, patch

# Импортируем функции бизнес-логики, которые будем тестировать
from user_service import format_user, register_user, login_user



# Тест функции format_user


def test_format_user_correct_mapping():
    """
    Unit-тест проверяет корректное преобразование строки,
    полученной из базы данных, в словарь пользователя.

    Функция format_user:
    - не работает с БД
    - не вызывает внешние сервисы
    - содержит только бизнес-логику

    Поэтому данный тест является unit-тестом.
    """
    row_from_db = (1, "Ivan", "ivan@mail.com")

    result = format_user(row_from_db)

    assert result == {
        "id": 1,
        "name": "Ivan",
        "email": "ivan@mail.com"
    }


# Тест функции register_user


@patch("user_service.get_connection")
def test_register_user_unit(mock_get_connection):
    """
    Unit-тест функции register_user.

    Реальная база данных в данном тесте не используется.
    Вместо этого функция get_connection подменяется мок-объектом.

    Это позволяет проверить бизнес-логику функции,
    не выполняя реальных SQL-запросов.
    """

    # Создаём мок подключения к БД
    mock_connection = MagicMock()
    mock_cursor = MagicMock()

    # Настраиваем поведение моков
    mock_get_connection.return_value = mock_connection
    mock_connection.cursor.return_value = mock_cursor

    # Имитируем ответ БД после INSERT ... RETURNING
    mock_cursor.fetchone.return_value = (1, "Ivan", "ivan@mail.com")

    # Вызываем тестируемую функцию
    user = register_user("Ivan", "ivan@mail.com", "1234")

    # Проверяем результат работы функции
    assert user["id"] == 1
    assert user["name"] == "Ivan"
    assert user["email"] == "ivan@mail.com"

    # Проверяем, что изменения были зафиксированы
    mock_connection.commit.assert_called_once()

    # Проверяем, что соединение было закрыто
    mock_connection.close.assert_called_once()


# Тест функции login_user


@patch("user_service.get_connection")
def test_login_user_success_unit(mock_get_connection):
    """
    Unit-тест успешной авторизации пользователя.

    База данных подменяется моками.
    Проверяется корректная обработка случая,
    когда пользователь найден.
    """

    mock_connection = MagicMock()
    mock_cursor = MagicMock()

    mock_get_connection.return_value = mock_connection
    mock_connection.cursor.return_value = mock_cursor

    # Имитируем найденного пользователя в БД
    mock_cursor.fetchone.return_value = (1, "Ivan", "ivan@mail.com")

    user = login_user("ivan@mail.com", "1234")

    assert user == {
        "id": 1,
        "name": "Ivan",
        "email": "ivan@mail.com"
    }


@patch("user_service.get_connection")
def test_login_user_not_found_unit(mock_get_connection):
    """
    Unit-тест случая, когда пользователь с такими
    данными не найден в базе.

    В этом случае функция должна вернуть None.
    """

    mock_connection = MagicMock()
    mock_cursor = MagicMock()

    mock_get_connection.return_value = mock_connection
    mock_connection.cursor.return_value = mock_cursor

    # Имитируем отсутствие пользователя
    mock_cursor.fetchone.return_value = None

    user = login_user("wrong@mail.com", "wrong")

    assert user is None
