from aiogram import Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hcode

from tgbot.config import load_config
from tgbot.keyboards.inline import buttons, report_admin_button
from tgbot.misc.states import AnswerState
from tgbot.services.parser import create_url_and_start_parser

err = {
    'url': '',
    'error': '',
    'user_id': ''
}


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
    msg = """
 ✍🏻 Решить тест

❗️Отправьте ссылку на ваш тест!
    """
    await call.message.answer(msg)
    await call.answer()
    await AnswerState.first()


async def parse_data(message: Message, state: FSMContext):
    await message.answer('Решаем🧐')
    url = message.text
    try:
        q_lst, a_lst = create_url_and_start_parser(url)
        msg = ''
        for id, question in enumerate(q_lst):
            msg += f'<b>{id + 1}</b>. {question}\n<b>Ответ</b>: {hcode(", ".join(a_lst[id]))}\n'

        await message.answer(msg)
    except Exception as ex:
        err['url'] = url
        err['error'] = str(ex)
        err['user_id'] = message.from_user.id
        msg = """
⚠️ Произошла неизвестная ошибка ⚠
        
Проверьте введённые данные и попробуйте ещё раз❗
Если ошибка не пропадет, то, пожалуйста, доложите
информацию администратору

👇 Благодаря вам бот станет ещё лучше❤️
"""
        await message.answer(msg, reply_markup=report_admin_button)
    await state.finish()


async def report_admin(call: CallbackQuery):
    await call.answer(f'Спасибо❤')
    await call.message.delete_reply_markup()

    config = load_config(".env")
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    admin = config.tg_bot.admin_ids[0]

    error_message = f"""
Произошла ошибка:
user_id: {err['user_id']}
url: {err['url']}
error: {err['error']}
    """
    await bot.send_message(admin, error_message)


def register_start(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"])
    dp.register_callback_query_handler(profile, text='profile')
    dp.register_callback_query_handler(solve_test, text='solve_test')
    dp.register_message_handler(parse_data, state=AnswerState.GetURL)
    dp.register_callback_query_handler(report_admin, text='report_admin')
