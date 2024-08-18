from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(SQLAlchemyBaseUserTableUUID, Base):
    pass
