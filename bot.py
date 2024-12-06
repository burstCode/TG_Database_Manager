import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

import database_manager
import gpt_manager

import config

TOKEN = config.BOT_TOKEN

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    Хендлер обрабатывает сообщения с командой /start
    :param message:
    :return:
    """
    await message.answer(
        f"Здравствуйте, {message.from_user.full_name}!\n"
        f"Я - Ваш помощник по работе с базой данных.\n"
        f"Напишите сюда свой поисковый запрос на естественном языке, "
        f"а я переведу его в SQL-запрос и выполню 😼"
    )


@dp.message()
async def search_message_handler(message: Message) -> None:
    """
    Хендлер обрабатывает сообщение с поисковым запросом на естественном языке
    :param message:
    :return:
    """

    query = gpt_manager.ask_yandex_gpt(message.text)

    search_result = database_manager.execute_query(query)

    search_result_text = ""
    for element in search_result:
        search_result_text += " ".join(map(str, element)) + "\n"

    await message.answer(
        f"Итоговый SQL-запрос: {query}\n"
        f"Результат поиска:\n"
        f"{search_result_text}"
    )


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
