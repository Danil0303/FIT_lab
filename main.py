import functools
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.scheduler.task import push_sub
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from loguru import logger
from aiogram import Dispatcher, Bot
from aiogram.types import BotCommand, BotCommandScopeDefault
from app.command_start import start_command
from app.menu import router_menu
from app.pay_button import router_pay
from app.db.base import create_tables
from config import SettingConfig

scheduler = AsyncIOScheduler()

dp = Dispatcher()
dp.include_router(start_command)
dp.include_router(router_menu)
dp.include_router(router_pay)

async def start_bot(bot: Bot):
    await set_commands(bot)
    await create_tables()
    scheduler.add_job(push_sub,'cron', hour='20', minute='00', args=[bot], id='push_sub')
    scheduler.start()
    logger.success('Бот запустился!')

async def stop_bot():
    scheduler.shutdown()
    logger.success('Бот остановился!')


async def set_commands(bot: Bot):
    menu_command = [BotCommand(command='/start', description='Старт'),
                    BotCommand(command='/help', description='Помощь')]
    await bot.set_my_commands(menu_command, BotCommandScopeDefault())


async def main():
    bot = Bot(SettingConfig.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.startup.register(functools.partial(start_bot, bot))
    dp.shutdown.register(stop_bot)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

