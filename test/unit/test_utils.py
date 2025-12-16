from utils import normalize_email

# Данный тест проверяет корректную работу вложенной функции normalize_email.
# Функция должна:
# - привести email к нижнему регистру
# - удалить пробелы в начале и в конце строки
# Тест не использует БД или внешние зависимости,
# поэтому относится к unit-тестированию.

def test_normalize_email_lowercase_and_strip():
    email = "  Test@Example.COM  "

    result = normalize_email(email)

    assert result == "test@example.com"


# Данный тест проверяет поведение функции,
# если на вход передано не строковое значение.
# В этом случае функция должна вернуть входное значение без изменений.

def test_normalize_email_not_string():
    email = None

    result = normalize_email(email)

    assert result is None
