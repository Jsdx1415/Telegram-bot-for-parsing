from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from config import settings

engine = create_async_engine(settings.db_url)
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    login = mapped_column(String)
    password = mapped_column(String)

    # def __repr__(self):
    #     return f"User with id {str(self.tg_id)} and login {self.login}"
    # def __str__(self):
    #     return f"User with id {str(self.tg_id)} and login {self.login}"


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
