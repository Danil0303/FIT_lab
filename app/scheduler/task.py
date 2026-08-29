from aiogram import Bot
from loguru import logger
from app.db.method import get_users, delete_user
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
                                       text="""
                                        Привет! На связи FIT-ЛАБОРАТОРИЯ👋🏽\n\nТвоя подписка заканчивается через 3 дня.\n\nЦена зафиксируется за тобой, если продлишь доступ в канал сразу по окончании действующей подписки.\n\nЕсли захочешь вернуться спустя время — цена будет уже выше😢\n\nПродлить сейчас — сохранить старую цену👇🏼
                                       """)
            elif del_time == 29:
                await bot.send_message(chat_id=user.id_user,
                                       text=f"Привет! На связи FIT-ЛАБОРАТОРИЯ👋🏽\n\nТвоя подписка заканчивается через 24 часа.\n\nЦена зафиксируется за тобой, если продлишь доступ в канал сразу по окончании действующей подписки.\n\nЕсли захочешь вернуться спустя время — цена будет уже выше😢\n\nПродлить сейчас — сохранить старую цену👇🏼")
            elif del_time == 30:
                await bot.send_message(chat_id=user.id_user,
                                       text="Сегодня последний день! Если хотите остаться в канале, оплатите продление по вашей личной цене (она сохраняется за вами)")
            elif del_time == 31:
                await delete_user(user_id=user.id_user, username=user.username)
                await bot.ban_chat_member(user_id=user.id_user, chat_id=str(SettingConfig.channel_id))
                await bot.unban_chat_member(user_id=user.id_user, chat_id=str(SettingConfig.channel_id))
                await bot.send_message(chat_id=user.id_user,
                                       text="Вы удалены из канала!")
        except Exception as e:
            logger.error(e)
            continue