import asyncio
import logging
import sys
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from app.handlers import router
from aiogram.fsm.storage.memory import MemoryStorage


load_dotenv()
TG_TOKEN = os.getenv('TOKEN')
bot = Bot(token=TG_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

async def main():
    dp.include_router(router)

    logging.info('Бот запущен')
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Остановка!!')
