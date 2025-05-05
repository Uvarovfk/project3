# Тут части кода, отвечающие за создание движка (sqlite), сессии работы вс бд, и кродимтельский (для таблиц бд) класс Base
#создание движка (строка для подключения к бд)

from sqlalchemy import select, create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm import sessionmaker

#engine = create_engine("sqlite:///books_lib.db")
engine = create_engine("sqlite:///baa.db")
new_session = sessionmaker(engine)

def get_session_sinc():
    with new_session() as session:
        yield session

class Base(DeclarativeBase):
    pass

