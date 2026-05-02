# your_telegram_bot_project/bot/states/common_states.py

from aiogram.fsm.state import State, StatesGroup


class LanguageSelection(StatesGroup):
    """
    Состояния для процесса выбора языка пользователем.
    """
    waiting_for_language = State()
