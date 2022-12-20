from aiogram.dispatcher.filters.state import StatesGroup, State


class AnswerState(StatesGroup):
    GetURL = State()
