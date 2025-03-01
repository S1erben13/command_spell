import logging
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.client.bot import DefaultBotProperties
import httpx
from config import TOKEN, API_URL

logging.basicConfig(level=logging.INFO)


# Инициализация бота и диспетчера
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


# Асинхронная функция для отправки POST-запроса к вашему API
async def send_message_to_api(author_id: str, text: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                API_URL,
                json={"author_id": author_id, "text": text},
                timeout=10.0
            )
            response.raise_for_status()  # Проверка на ошибки HTTP
            return response.json()
        except httpx.HTTPError as e:
            logging.error(f"Ошибка при отправке запроса к API: {e}")
            return None


# Обработчик текстовых сообщений
@dp.message()
async def echo(message: types.Message):
    # Получаем ID пользователя и текст сообщения
    author_id = str(message.from_user.id)
    text = message.text

    # Отправляем данные на ваш API
    api_response = await send_message_to_api(author_id, text)

    if api_response:
        await message.answer(f"Сообщение успешно отправлено! Ответ API: {api_response}")
    else:
        await message.answer("Произошла ошибка при отправке сообщения. Попробуйте позже.")


# Запуск бота
async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
