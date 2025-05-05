from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from source.api.dependencies import SessionDep
from source.api.users import security
from source.models.all_models import BookModel, ReviewModel

router = APIRouter()


# эндпоинт рекомендации:

@router.get("/recomendation", dependencies=[Depends(security.access_token_required)], tags=["Рекомендации"], summary="Популярная книга: только для авторизованных пользователей")
def recomend(session: SessionDep):
    try:
        result = session.execute(select(ReviewModel))
        review_data = result.scalars().all()
        result = session.execute(select(BookModel))
        book_data = result.scalars().all()
        if len(review_data) != 0:
            id_not_empty = []
            for r in review_data:
                id_not_empty.append(r.book_id)
            max_popular_index = 0
            popular_book = select(BookModel).where(BookModel.id == id_not_empty[0])
            for i in id_not_empty:
                query = select(ReviewModel).where(ReviewModel.book_id == i)
                result = session.execute(query)
                all_reviews_of_book = result.scalars().all()
                mark_mean = 0
                t = 0
                for item in all_reviews_of_book:
                    mark_mean += item.mark
                    t += 1
                mark_mean = mark_mean / t
                alpha = 0.5
                res = alpha * (mark_mean / 5.) + (1 - alpha) * (len(all_reviews_of_book) / len(review_data))
                if res > max_popular_index:
                    max_popular_index = res
                    popular_book = select(BookModel).where(BookModel.id == i)

            result = session.execute(popular_book)
            recommendation = result.scalars().one()
            print(recommendation)
            return {recommendation}
        else:
            return {"Пока нет популярных книг"}
    except:
        return{"Вы не авторизованы"}

