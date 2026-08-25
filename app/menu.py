import pathlib

from aiogram import Router, types
from aiogram.types import FSInputFile, InputMediaDocument

from app.button import start_button
from app.db.method import  get_users

router_menu = Router()

@router_menu.callback_query(lambda c: c.data =='lab')
async def lab(callback_query: types.CallbackQuery):
    await callback_query.message.answer_photo(
        photo=FSInputFile(path=pathlib.Path(r'templates/images/lab.jpg')),
        caption="""
            FIT-лаборатория – это твоя фитнес-база в одном месте.\n\nЯ собрала то, что обычно приходится искать по десяткам аккаунтов, видео, заметкам, и то, что не всегда возможно там найти\n\nТы получаешь доступ к материалам и постепенно собираешь из них свою систему работы над телом.
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
    data = await get_users()
    if len(data) <= 25:
        text = "первые 25 мест - 1299₽/мес"
    elif 25 < len(data) <= 50:
        text = "Доступ на 30 дней - <del>1799₽</del> 1599₽"
    else:
        text = "Доступ на 30 дней - 1799₽/мес"
    await callback_query.message.answer(
        text=f"<b>{text}</b>\n*цена фиксируется за тобой, если продлеваешь доступ вовремя",
        parse_mode="HTML",
        reply_markup=start_button()
    )
    await callback_query.answer()


@router_menu.callback_query(lambda c: c.data == 'info')
async def info(callback_query: types.CallbackQuery):
    await callback_query.message.answer(
        text="ИП Антонова Алла Эдуардовна\nОГРНИП 326710000030811\nИНН 711610566034\nТульская обл., г.Новомосковск\n n.yackova2017@yandex.ru",
        reply_markup=start_button(),
    )
    await callback_query.message.answer_media_group(
        media=[
            InputMediaDocument(media=FSInputFile(path=r'templates/documents/Публичная оферта на оказание платных образовательных услуг.docx')),
            InputMediaDocument(media=FSInputFile(path=r'templates/documents/Политика в отношении обработки персональных данных.docx')),
            InputMediaDocument(media=FSInputFile(path=r'templates/documents/Согласие на обработку персональных данных.docx')),
            InputMediaDocument(media=FSInputFile(path=r'templates/documents/Согласие на рассылку электронных сообщений.docx'))
        ],

    )

