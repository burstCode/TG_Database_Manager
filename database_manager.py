import psycopg2

import config

connection = psycopg2.connect(
    dbname=config.dbname,
    host=config.host,
    user=config.user,
    password=config.password,
    port=config.port
)

cursor = connection.cursor()


def execute_query(query: str) -> list:
    """
    Выполняет SQL-запрос к базе данных, возвращает список
    :param query:
    :return:
    """
    cursor.execute(query)
    output = cursor.fetchall()
    connection.commit()

    return output


def close_connection() -> None:
    """
    Закрывает соединение и курсор
    :return:
    """
    if cursor:
        cursor.close()
    if connection:
        connection.close()
