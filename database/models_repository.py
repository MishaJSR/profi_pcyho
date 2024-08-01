from database.models import Users
from database.repository import SQLAlchemyRepository


class UsersRepository(SQLAlchemyRepository):
    model = Users