def get_connection():
    """
    Функция создания подключения к базе данных.

    Импорт драйвера базы данных выполнен внутри функции,
    чтобы unit-тесты не зависели от наличия psycopg2
    и не падали на этапе импорта модуля.
    """
    import psycopg2

    """return psycopg2.connect(
        host="host.docker.internal",
        database="user_db",
        user="postgres",
        password="0000"
   )"""
    import psycopg2

    return psycopg2.connect(
        host="localhost",
        database="user_db",
        user="postgres",
        password="0000",
        port=5432
    )