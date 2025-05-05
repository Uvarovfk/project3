from source.database.db import Base
from sqlalchemy.orm import relationship
from sqlalchemy import select, ForeignKey
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from source.database.db import Base
from pydantic import BaseModel, Field, EmailStr, ConfigDict

# модель таблицы книг
class BookModel(Base):
    __tablename__ = 'books' #library_books
    id: Mapped[int] = mapped_column(primary_key=True) # первичный ключ
    title: Mapped[str]
    author: Mapped[str]
    reviews = relationship('ReviewModel', back_populates='books')



# модель таблицы отзывов
class ReviewModel(Base):
    __tablename__ = 'reviews' #library_books
    id: Mapped[int] = mapped_column(primary_key=True) #первичный ключ
    guest_name: Mapped[str] = mapped_column(ForeignKey('users.id'))
    text: Mapped[str]
    mark: Mapped[int]
    book_id: Mapped[int] = mapped_column(ForeignKey('books.id'))
    # relationship( название класса, название класса)
    books = relationship('BookModel', back_populates='reviews')
    users = relationship('UserModel', back_populates='reviews')


class UserModel(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True) #первичный ключ
    email: Mapped[str] # EmailStr
    name: Mapped[str]
    age: Mapped[int]
    password: Mapped[str]
    reviews = relationship('ReviewModel', back_populates='users')