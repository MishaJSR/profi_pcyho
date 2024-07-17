import os

from aiogram.filters import BaseFilter
from aiogram.types import Message
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
admin_list = os.getenv('ADMIN_ID').split(", ")
admin_list = [int(ad_id) for ad_id in admin_list]


class AdminFilter(BaseFilter):
    is_admin: bool = True

    async def __call__(self, obj: Message) -> bool:
        return obj.from_user.id in admin_list
