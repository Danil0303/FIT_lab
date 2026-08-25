from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def start_button()->InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🧪 Что такое лаборатория', callback_data='lab')],
            [InlineKeyboardButton(text='📦 Что внутри', callback_data='inside')],
            [InlineKeyboardButton(text='👤 Кому подойдет', callback_data='who')],
            [InlineKeyboardButton(text='💰 Стоимость', callback_data='price')],
            [InlineKeyboardButton(text='💸 Оплатить', callback_data='pay')],
            [InlineKeyboardButton(text='📝 Юридическая информация', callback_data='info')]

    ])


def payment_button(url: str)-> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Оплатить подписку",
                              url=url)]
    ])
