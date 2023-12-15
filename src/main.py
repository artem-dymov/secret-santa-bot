import asyncio
from aiogram import Dispatcher
from src.router import router
from src.router_after_reg import router_after_reg
import src.config as config
from src.bot import bot

# Запуск бота
async def main():
    dp = Dispatcher()

    if config.mode == 1:
        dp.include_router(router)
    elif config.mode == 2:
        dp.include_router(router_after_reg)

    await dp.start_polling(bot)


if __name__ == "__main__":
    print('running')
    asyncio.run(main())
