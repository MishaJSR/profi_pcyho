import os
from abc import ABC, abstractmethod

from aiogram.fsm.state import StatesGroup, State
from dotenv import find_dotenv, load_dotenv

from pydantic import StrictStr, ConfigDict, StrictInt, BaseModel, validator, field_validator

load_dotenv(find_dotenv())


class CustomTreeState(ABC, StatesGroup):
    @abstractmethod
    def calculate_area(self):
        pass


class UserCallbackState(CustomTreeState):
    start_callback = State()
    image_callback = State()
    test_callback = State()
    user_callback = State()
    tasks = []
    count_tasks = None
    block_id = None
    now_task = None
    list_of_answers = []
    callback_data = None


class Config(BaseModel):
    redis_user: str

    @classmethod
    def get_config(cls):
        return cls()

    @classmethod
    def load_config(cls):
        return cls(redis_user=os.getenv("REDISUSERNAME"),
                   redis_host=os.getenv("REDISHOST"),
                   )


configuration = Config.load_config()
print(configuration.redis_user)
