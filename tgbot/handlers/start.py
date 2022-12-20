from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery

from tgbot.keyboards.inline import buttons


async def user_start(message: Message):
    ans = """
👋🏼 Привет!
Я бот, который может решить почти
любой тест на <b>skysmart</b>!
    
Стоимость - БЕСПЛАТНО❗
💯Да, вам не показалось, решение тестов,
абсолютно бесплатно!

Выберите нужный для вас пункт👇🏻
    """
    await message.answer(ans, reply_markup=buttons)


async def profile(call: CallbackQuery):
    await call.message.answer('Ваш профиль')
    await call.answer()


async def solve_test(call: CallbackQuery):
    await call.message.answer('Решаем тест')
    await call.answer()


def register_start(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_callback_query_handler(profile, text='profile')
    dp.register_callback_query_handler(solve_test, text='solve_test')
