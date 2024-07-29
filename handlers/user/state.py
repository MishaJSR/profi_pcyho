from aiogram.fsm.state import StatesGroup, State


class UserState(StatesGroup):
    start_user = State()
    payment_user = State()
    user_task = State()
    user_callback = State()
    data = {
        'subj': None,
        'module': None,
        'under_prepare': [],
        'under_prepare_choose': None,
        'prepare': None,
    }