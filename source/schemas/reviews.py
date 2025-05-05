# схемы проекта
from pydantic import BaseModel, Field, ConfigDict


# схема добавления
class AddReview(BaseModel):
    guest_name: str = Field(max_length=100)
    text: str = Field(max_length=500)
    mark: int = Field(ge=0, le=5)
    book_id: int = Field(ge=0)
    # пусть нельзя вводить любые другие данные
    model_config = ConfigDict(extra='forbid')


# схема для просмотра отзывов к книге
class GetReview(BaseModel):
    book_id: int = Field(ge=0)