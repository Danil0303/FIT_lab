import pathlib

from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from aiogram.types import FSInputFile

from app.button import start_button

start_command = Router()

@start_command.message(CommandStart())
async def start_bot(message: types.Message):
    await message.answer_photo(
        photo=FSInputFile(path=pathlib.Path(r'templates/images/main_photo.jpg')),
        caption="""
            <b>FIT - лаборатория 

            Привет! 👋🏽 
            Если ты здесь, скорее всего тебе хочется привести тело в форму, при этом не жить в режиме «тренер 24/7 контролирует каждый мой шаг»

            Я создала FIT-лабораторию — пространство, где собрала всё необходимое для работы над телом, питанием и тренировками.
            
            Что хочешь узнать?</b>
        """,
        parse_mode='HTML',
        reply_markup=start_button()
    )

@start_command.message(Command('help'))
async def message_help(message: types.Message):
    await message.answer("Если есть какие-либо вопросы по клубу или сложности с оплатой, смело пиши мне лично: @alla_an ❤️")