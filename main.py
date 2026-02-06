import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from dotenv import load_dotenv  

from handler import router
from database import create_table


load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("TOKEN DOESN'T EXIST")

async def main():
    create_table()

    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode="HTML")
    )

    dp = Dispatcher()
    dp.include_router(router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
