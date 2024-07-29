from aiogram.fsm.state import StatesGroup, State
from keyboards.admin.reply_admin import spam_actions_kb


class UserRegistrationState(StatesGroup):
    start = State()
    children = State()
    parent = State()
    name_get = State()
    texts = {
        'UserRegistrationState:start': ['Выберите действие', spam_actions_kb],
        'UserRegistrationState:choose_block': 'Выбор задания для удаления',
        'UserRegistrationState:choose_block_or_test': 'Подтверждение',
    }
    data = []
    block_pool = []
    block_name = None
    block_id = None
    children_id = None
