import functools
import asyncio
from loguru import logger
from aiogram import Dispatcher, Bot
from aiogram.types import BotCommand, BotCommandScopeDefault

dp = Dispatcher()

async def start_bot(bot: Bot):
    await set_commands(bot)
    logger.success('Бот запустился!')

async def stop_bot():
    logger.success('Бот остановился!')


async def set_commands(bot: Bot):
    menu_command = [BotCommand(command='/start', description='Старт'),
                    BotCommand(command='/help', description='Помощь')]
    await bot.set_my_commands(menu_command, BotCommandScopeDefault())


async def main():
    bot = Bot()
    dp.startup.register(functools.partial(start_bot, bot))
    dp.shutdown.register(stop_bot)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

