# utils.py

def normalize_email(email: str) -> str:
    """
    Вложенная функция для обработки email.
    Практика требует, чтобы эндпоинт вызывал функцию из внешнего файла.
    """
    if not isinstance(email, str):
        return email
    return email.strip().lower()
