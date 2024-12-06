import requests
import json

import config

with open('prompt.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Api-Key {config.YANDEX_API_KEY}"
}


def ask_yandex_gpt(text_query: str) -> str:
    """
    Отправляет запрос к Yandex GPT и возвращает SQL-запрос
    :param text_query:
    :return:
    """

    data["modelUri"] = config.YANDEX_MODEL_URI
    data["messages"][1]["text"] = text_query

    response = requests.post(
        "https://llm.api.cloud.yandex.net/foundationModels/v1/completion",
        headers=headers,
        json=data
    )

    response_json = json.loads(response.text)

    sql_query = response_json['result']['alternatives'][0]['message']['text']

    return sql_query
