# эндпоинты проекта. Так как эндпоинты находятся не в main.py, отсутствует доступ к @app.
# для этого испольщуем APIRouter и создаем роут

from fastapi import APIRouter, HTTPException, Response, Depends
from authx import AuthX, AuthXConfig
from sqlalchemy import select, delete, update
from source.api.dependencies import SessionDep
from source.models.all_models import UserModel, BookModel
from source.schemas.users import LogIn, ChangeUser, AddNewUser

router = APIRouter()

config = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET_KEY"
config.JWT_ACCESS_COOKIE_NAME = "user_token"
config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=config)


# эндпоинт регистрации
@router.post("/register", tags=["Пользователи"], summary="Регистрация пользователя")
def regis(creds: AddNewUser, session: SessionDep, response: Response):
    query = select(UserModel)
    result = session.execute(query)
    all_users = result.scalars().all()
    flag = 0
    for p in all_users:
        if (p.email == creds.email):
            flag = 1
    if flag == 0:
        new_user = UserModel(
        id=len(all_users) + 1,
        email=creds.email,
        name=creds.name,
        age=creds.age,
        password=creds.password,
        )
        session.add(new_user)
        session.commit()
        token = security.create_access_token(uid=creds.email)
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return{"message": "Вы зарегестрированы", "access_token": token}
    else:
        return{"Пользователь с таким email уже зарегестрирован"}


# эндпоинт авторизации
@router.post("/login", tags=["Пользователи"], summary="Авторизация пользователя")
def auth(creds: LogIn, session: SessionDep, response: Response):
    query = select(UserModel)
    result = session.execute(query)
    all_users = result.scalars().all()
    flag = 0
    for p in all_users:
        if (p.email == creds.email) & (p.password == creds.password):
            flag = 1
    if flag == 1:
        token =security.create_access_token(uid=creds.email)
        #послыаем в куки
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return{'access_token': token}
    raise HTTPException(401, detail={"message": "Неверный логин или пароль"})
