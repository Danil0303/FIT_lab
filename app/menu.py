import pathlib

from aiogram import Router, types
from aiogram.types import FSInputFile

from app.button import start_button, pay_button

router_menu = Router()

@router_menu.callback_query(lambda c: c.data =='lab')
async def lab(callback_query: types.CallbackQuery):
    await callback_query.message.answer_photo(
        photo=FSInputFile(path=pathlib.Path(r'templates/images/lab.jpg')),
        caption="""
            FIT-лаборатория – это твоя фитнес-база в одном месте.

        Я собрала то, что обычно приходится искать по десяткам аккаунтов, видео, заметкам, и то, что не всегда возможно там найти 
            
        Ты получаешь доступ к материалам и постепенно собираешь из них свою систему работы над телом.
        """,
        reply_markup=start_button()
    )
    await callback_query.answer()

@router_menu.callback_query(lambda c: c.data=='inside')
async def inside(callback_query: types.CallbackQuery):
    await callback_query.message.answer_photo(
        photo=FSInputFile(path=pathlib.Path(r'templates/images/inside.jpg')),
        reply_markup=start_button()
    )
    await callback_query.answer()

@router_menu.callback_query(lambda c: c.data == 'who')
async def who(callback_query: types.CallbackQuery):
    await callback_query.message.answer_photo(
        photo=FSInputFile(path=pathlib.Path(r'templates/images/who.jpg')),
        reply_markup=start_button()
    )
    await callback_query.answer()

@router_menu.callback_query(lambda c: c.data=='price')
async def price(callback_query: types.CallbackQuery):
    await callback_query.message.answer(
        text="555555",
        reply_markup=start_button()
    )
    await callback_query.answer()

@router_menu.callback_query(lambda c: c.data == 'pay')
async def pay(callback_query: types.CallbackQuery):
    await callback_query.message.answer_document(
        document=FSInputFile(path=pathlib.Path(r'templates/documents/document.docx')),
        reply_markup=pay_button()
    )
    await callback_query.answer()

