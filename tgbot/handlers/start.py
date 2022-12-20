from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hcode

from tgbot.keyboards.inline import buttons, admin
from tgbot.misc.states import AnswerState
from tgbot.services.parser import create_url_and_start_parser


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
    message = f"""
📋 Профиль

В процессе разработки👷🏻‍♂️
    """
    await call.message.answer(message)
    await call.answer()


async def solve_test(call: CallbackQuery):
    await call.message.answer('❗️Отправте ссылку на ваш тест!')
    await call.answer()
    await AnswerState.first()


async def parse_data(message: Message, state: FSMContext):
    try:
        a = 3 / 0
        url = message.text
        answers = create_url_and_start_parser(url)
        msg = ''
        for answer in answers:
            ans = answer[2].replace('[', '').replace(']', '')
            msg += f'<b>{answer[0]}</b>. {answer[1]}\n<b>Ответ</b>: {hcode(ans)}\n'
        await message.answer(msg)
    except Exception:
        await message.answer('Ошибка')
    await state.finish()


def register_start(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"])
    dp.register_callback_query_handler(profile, text='profile')
    dp.register_callback_query_handler(solve_test, text='solve_test')
    dp.register_message_handler(parse_data, state=AnswerState.GetURL)
