from aiogram.fsm.state import StatesGroup, State
from keyboards.admin.reply_admin import start_kb, back_kb, reset_kb, block_actions, send_media_kb, send_media_check_kb, \
    block_pool_kb, \
    test_actions, type_task_kb, spam_actions_kb


class UserRegistrationState(StatesGroup):
    start = State()
    children = State()
    parent = State()
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
