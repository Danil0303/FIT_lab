from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta
from app.db.base import connection
from app.db.databases import async_sessions
from app.db.model import FitSubscribe
from sqlalchemy import select, update, delete
from loguru import logger

@connection
async def get_users(session: async_sessions) -> list[FitSubscribe]:
    result = await session.execute(select(FitSubscribe))
    users = result.scalars().all()
    return users

@connection
async def get_user(session: async_sessions, id_user: int) -> FitSubscribe:
    result = await session.execute(
        select(FitSubscribe)
        .where(FitSubscribe.id_user == id_user)
    )
    user = result.scalar()
    return user

@connection
async def add_user(session: async_sessions, id_user: int, username: str, email: str, price: float):
    user = await get_user(id_user)
    if user:
        logger.info(f'Пользователь {id_user} ({username})уже существует')
        return await update_date_subscribe(id_user, username)
    try:
        data = datetime.today()
        user_new = FitSubscribe(id_user=id_user,
                             data_start=data,
                             data_end=data+timedelta(days=30),
                             username=username,
                             price=price,
                             email_str=email
                             )
        session.add(user_new)
        await session.commit()
        logger.success(f"Зарегистрировал пользователя с ID {id_user}!")
    except (SQLAlchemyError, Exception)as exp:
        logger.error(exp)
        await session.rollback()

@connection
async def update_date_subscribe(session: async_sessions, user_id: int, username: str):
    data = datetime.today()
    try:
        await session.execute(update(FitSubscribe).filter_by(id_user=user_id).values(data_start=data,
                                                                                  data_end=data+timedelta(days=30),
                                                                                  ))
        await session.commit()
        logger.success(f'Данные пользователя обновлены: {user_id} ({username}')
    except SQLAlchemyError as exp:
        logger.error(exp)
        await session.rollback()

@connection
async def delete_user(session: async_sessions, user_id: int, username: str):
    try:
        await session.execute(delete(FitSubscribe).where(FitSubscribe.id_user==user_id))
        await session.commit()
        logger.success(f'Данные пользователя: {user_id} ({username}) удалены')
    except SQLAlchemyError as exp:
        logger.error(exp)
        await session.rollback()