import pathlib
import re
import asyncio
from aiogram import Router, types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile
from aioyookassa import YooKassa
from aioyookassa.types.payment import Money, Confirmation, Receipt, PaymentItem
from aioyookassa.types.enum import PaymentStatus, ConfirmationType, Currency, PaymentSubject, PaymentMode
from aioyookassa.types.params import CreatePaymentParams
from loguru import logger
from app.button import start_button, payment_button
from datetime import datetime, timedelta

from app.db.method import add_user, get_users, get_user
from app.errors.error import TimeOutPayments
from config import EmailReg, YooKasConfig

router_pay = Router()

class Form(StatesGroup):
    waiting_for_email = State()

def create_payment_method(user_id: int, email: str, price):
    return CreatePaymentParams(
        amount=Money(value=float(YooKasConfig.value_cur), currency=Currency.RUB),
        confirmation=Confirmation(
            type=ConfirmationType.REDIRECT,
            return_url=YooKasConfig.return_url_api
        ),
        description=f"Подписка 30 дней на FIT-лабораторию - {price}p",
        metadata = {'user_id': user_id},
        capture=True,
        receipt=Receipt(
            items=[
                PaymentItem(description=f"Подписка 30 дней на FIT-лабораторию - {price}p",
                            amount=Money(value=float(YooKasConfig.value_cur), currency=Currency.RUB),
                            quantity=1,
                            vat_code=11,
                            payment_subject=PaymentSubject.COMMODITY,
                            payment_mode=PaymentMode.FULL_PAYMENT
                            ),
            ],
            tax_system_code=1,
            internet=True,
            email=email


        ),
        save_payment_method=False
    )

@router_pay.callback_query(lambda c: c.data == 'yes')
async def buy(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Пожалуйста, введите ваш email для чека:")
    await state.set_state(Form.waiting_for_email)
    await callback_query.answer()

@router_pay.callback_query(lambda c: c.data == 'not')
async def not_buy(callback_query: types.CallbackQuery):
    await callback_query.message.answer(
        text='Буду тебя ждать',
        reply_markup=start_button()
    )
    await callback_query.answer()


@router_pay.message(Form.waiting_for_email)
async def process_email(message: types.Message, state: FSMContext, bot: Bot):
    email = message.text
    user_price = await get_user(message.from_user.id)
    if user_price:
        price = float(user_price.price)
    else:
        users = len(await get_users)
        if users <= 25:
            price = float(1299)
        elif 25 < users <= 50:
            price = float(1599)
        elif users > 50:
            price = float(1799)
    logger.success(price)
    # if bool(re.match(EmailReg.EMAIL_REGEXP, email)):
    #     await state.update_data(user_email=email)
    #     await message.answer("Начинаем оформление подписки...")
    #     await asyncio.sleep(2)
    #     try:
    #         price = 1
    #         async with YooKassa(api_key=YooKasConfig.api_key, shop_id=int(YooKasConfig.shop_id)) as client:
    #             payment_response = create_payment_method(user_id=message.from_user.id, email=email, price=price)
    #             payment = await client.payments.create_payment(payment_response, )
    #             logger.success(f"✅ Платеж создан: {payment.id}")
    #             await message.answer(text=f"Оплата подписки 30 дней на FIT-лабораторию👇🏻\n\n"
    #                                                      f"Цена подписки - {price}p\n",
    #                                                 reply_markup=payment_button(payment.confirmation.url))
    #             start_time = datetime.now()
    #             timeout = timedelta(minutes=int(YooKasConfig.time_delta))
    #             payment_info = await client.payments.get_payment(payment.id)
    #             try:
    #                 while payment_info.status == PaymentStatus.PENDING:
    #                     current_time = datetime.now()
    #                     elapsed_time = current_time - start_time
    #                     payment_info = await client.payments.get_payment(payment.id)
    #                     if elapsed_time > timeout:
    #                         raise TimeOutPayments('Вышло время оплаты подписки')
    #                     if payment_info.status.lower() != PaymentStatus.PENDING:
    #                         break
    #                     await asyncio.sleep(10)
    #                 logger.info(f"📊 Статус платежа: {payment_info.status}")
    #                 if payment_info.status == PaymentStatus.SUCCEEDED:
    #                     logger.success("Платеж подтвержден")
    #                     await add_user(id_user=message.from_user.id,
    #                                    username=message.from_user.username,
    #                                    email=email,
    #                                    price=float(price))
    #                     await message.answer_photo(
    #                         photo=FSInputFile(path=pathlib.Path(r'templates/images/pay_s.jpg')),
    #                         caption=f"""
    #                             Поздравляю, оплата прошла успешно!✅
    #                             Ссылка для входа👉🏻 {YooKasConfig.link}
    #                             Доступ активен 30 дней с момента оплаты.
    #                         """
    #                     )
    #                     return await bot.send_message(chat_id=822290548, text=f'Пользователь: {message.from_user.username} оплатил подписку!')
    #                 await message.answer(text="Оплата не прошла!")
    #                 await bot.send_message(chat_id=822290548,
    #                                        text=f'Пользователь: {message.from_user.username} не смог оплатить подписку!')
    #             except TimeOutPayments as exp:
    #                 logger.error(exp)
    #                 await message.answer(text="Оплата не прошла!")
    #                 await bot.send_message(chat_id=822290548,
    #                                        text=f'Пользователь: {message.from_user.username} не смог оплатить подписку!')
    #     except Exception as e:
    #         logger.error(e)
    #         await message.answer( "Упс, похоже, что-то пошло не так. Обратись за помощью сюда: @alla_an")
    #     finally:
    #         await state.clear()
    # else:
    #     await message.answer("Некорректный email!\n/start")