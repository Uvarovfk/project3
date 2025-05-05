# схемы проекта
from pydantic import BaseModel, Field, ConfigDict


# схема для добавления книги пользователем
class AddBook(BaseModel):
    title: str = Field(max_length=100)
    author: str = Field(max_length=100)
    # пусть нельзя вводить любые другие данные
    model_config = ConfigDict(extra='forbid')


# схема для получения книги из бд
class GetBook(BaseModel):
    id: int = Field(ge=0)
    title: str = Field(max_length=100)
    author: str = Field(max_length=100)


# схема для обновления данных книги
class ChangeBook(BaseModel):
    id: int = Field(ge=0)
    title: str = Field(max_length=100)
    author: str = Field(max_length=100)
    # пусть нельзя вводить любые другие данные
    model_config = ConfigDict(extra='forbid')


# схема для удаления книги
class DeleteBook(BaseModel):
    id:  int = Field(ge=0)