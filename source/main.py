from fastapi import Depends, FastAPI
from source.api.routes import main_router
import uvicorn

from source.database.db import engine, Base

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
print("БД создана")
app = FastAPI()
app.include_router(main_router)
