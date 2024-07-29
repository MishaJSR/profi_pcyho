import os
from dotenv import find_dotenv, load_dotenv

from pydantic import StrictStr, ConfigDict, StrictInt, BaseModel, validator, field_validator

load_dotenv(find_dotenv())


class Config(BaseModel):
    redis_user: str

    @classmethod
    def get_config(cls):
        return cls()

    @classmethod
    def load_config(cls):
        return cls(redis_user=os.getenv(""))


configuration = Config.load_config()
print(configuration.redis_user)
