# Зависимости проекта
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from source.database.db import get_session_sinc

# инъекция зависимостей. Для работы с сессией в эндпоинте
SessionDep = Annotated[Session, Depends(get_session_sinc)]