from aiogram import Bot
from loguru import logger
from app.db.method import get_users
from datetime import datetime

from config import SettingConfig


async def push_sub(bot: Bot):
    users = await get_users()
    logger.success('Рассылка для пользователей с подпиской запущена')
    for user in users:
        try:
            del_time = (datetime.today()-user.data_start).days
            if del_time == 27:
                await bot.send_message(chat_id=user.id_user,
                                       text='Через 3 дня у вас закончится подписка, не забудьте продлить')
            elif del_time == 29:
                await bot.send_message(chat_id=user.id_user,
                                       text=f"Завтра подписка истекает, продлите прямо сейчас")
            elif del_time == 30:
                await bot.send_message(chat_id=user.id_user,
                                       text="Сегодня последний день! Если хотите остаться в канале, оплатите продление по вашей личной цене (она сохраняется за вами)")
            elif del_time == 31:
                await bot.ban_chat_member(user_id=user.id_user, chat_id=str(SettingConfig.channel_id))
                await bot.send_message(chat_id=user.id_user,
                                       text="Вы удалены из канала!")
        except Exception as e:
            logger.error(e)
            continue