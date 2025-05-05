from fastapi import APIRouter
from sqlalchemy import select, delete, update
#from sqlalchemy.orm.sync import update
from source.api.dependencies import SessionDep
from source.database.db import engine, Base
from source.models.all_models import ReviewModel, BookModel
from source.schemas.reviews import AddReview, GetReview

router = APIRouter()


# эндпоинт добавления:
@router.post("/reviews", tags=["Отзывы"], summary="Добавить отзыв")
def add_rew(data: AddReview, session: SessionDep):
    result = session.execute(select(BookModel))
    books = result.scalars().all()
    flag = 0
    for book in books:
        if book.id == data.book_id:
            flag = 1
    if flag == 1:
        query = select(ReviewModel)
        result = session.execute(query)
        num_of_rew = len(result.scalars().all())
        new_review = ReviewModel(
            id=num_of_rew + 1,
            guest_name=data.guest_name,
            text=data.text,
            mark=data.mark,
            book_id=data.book_id,
        )
        session.add(new_review)
        session.commit()
        return {"Рецензия добавлена", new_review}
    else:
        return {"message": "Книги с таким id нет"}


# эндпоинт: получить весь список отзывов из бд:
@router.get("/reviews", tags=["Отзывы"], summary="Получить все отзывы на книгу")
def get_rew(book_id: int, session: SessionDep):
    result = session.execute(select(BookModel))
    books = result.scalars().all()
    flag = 0
    for book in books:
        if book.id == book_id:
            flag = 1
    if flag == 1:
        result = session.execute(select(ReviewModel))
        rewievs = result.scalars().all()
        flag = 0
        k=0
        mean=0
        abc = []
        for r in rewievs:
            if r.book_id == book_id:
                mean+=r.mark
                k+=1
                abc.append(r.text)
        if abc == []:
            return{"На эту книгу пока нет отзывов"}
        else:
            mean=mean/k
            return {"Средняя оценка": mean, "Отзывы о книге": abc}

    else:
        return {"message": "Книги с таким id нет"}
