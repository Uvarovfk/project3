# схемы проекта
from pydantic import BaseModel, Field, EmailStr, ConfigDict


# добавление нового пользователя
class AddNewUser(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1, max_length=100)
    age: int = Field(gt=0, lt=150)
    password: str = Field(min_length=1, max_length=100)
    # пусть нельзя вводить любые другие данные
    model_config = ConfigDict(extra='forbid')


# схема для авторизации
class LogIn(BaseModel):
    email: EmailStr
    password: str
    # пусть нельзя вводить любые другие данные
    model_config = ConfigDict(extra='forbid')


# схема для обновления данных
class ChangeUser(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1, max_length=100)
    age: int = Field(gt=0, lt=150)
    password: str
    # пусть нельзя вводить любые другие данные
    model_config = ConfigDict(extra='forbid')


# схема для удаления
class DeleteUser(BaseModel):
    email: EmailStr
    password: str
    # пусть нельзя вводить любые другие данные
    model_config = ConfigDict(extra='forbid')
