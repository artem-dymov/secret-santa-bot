import asyncio
from aiogram import Bot, Dispatcher
from router import router
import config


# Запуск бота
async def main():
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()

    # Запускаем бота и пропускаем все накопленные входящие
    # Да, этот метод можно вызвать даже если у вас поллинг
    # await bot.delete_webhook(drop_pending_updates=True)
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    print('running')
    asyncio.run(main())
