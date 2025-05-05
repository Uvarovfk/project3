# эндпоинты проекта. Так как эндпоинты находятся не в main.py, отсутствует доступ к @app.
# для этого испольщуем APIRouter и создаем роут
from fastapi import APIRouter
from sqlalchemy import select, delete, update
#from sqlalchemy.orm.sync import update

from source.api.dependencies import SessionDep
from source.database.db import engine, Base
from source.models.all_models import BookModel
from source.schemas.books import AddBook, GetBook, ChangeBook, DeleteBook
router = APIRouter()

@router.post("/create", tags=["бд"], summary="create bd")
def db(session: SessionDep):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    return{"БД пересоздана"}

# эндпоинт добавления книги в бд:
@router.post("", tags=["Книги"], summary="Добавить книгу")
def add_book(book: AddBook, session: SessionDep):
    query = select(BookModel)
    result = session.execute(query)
    all_books_now = result.scalars().all()
    flag = 0
    for item in all_books_now:
        if (item.author == book.author) & (item.title == book.title):
            flag = 1
    if flag == 0:
        new_book = BookModel(
            id=len(all_books_now) + 1,
            title=book.title,
            author=book.author,
        )
        session.add(new_book)  # в alchemy
        session.commit()  # добавляем в бд все выше (сразу)
        return {"Книга успешно добавлена", new_book}
    else:
        return {"Такая книга уже есть"}


# эндпоинт: получить весь список книг из бд:
@router.get("", tags=["Книги"], summary="Получить список книг")
def get_books(session: SessionDep):
    query = select(BookModel)
    result = session.execute(query)
    books = result.scalars().all()
    if len(books) != 0:
        return {"Список книг": books}
    else:
        return {"message": "В каталоге еще нет книг"}


# получить конкретную книгу из бд по id:
@router.get("/{book_id}", tags=["Книги"], summary="Получить определенную книгу")
def get_one_book(book_id: int, session: SessionDep):
    query = select(BookModel).where(BookModel.id == book_id)
    result = session.execute(query)
    books = result.scalars().all()
    #for book in books:
    #    if book.id == book_id:
    #        return book

    if books != []:
        return books
    #for book in books:
    else:
        return {f"Книги с id {book_id} нет"}

# обновить данные книги (id)
@router.patch("/{book_id}", tags=["Книги"], summary="Обновить данные книги")
def change_book(book_changed: ChangeBook, session: SessionDep):
    query = select(BookModel)
    result = session.execute(query)
    books = result.scalars().all()
    for book in books:
        if book.id == book_changed.id:
            to_do = update(BookModel).where(BookModel.id == book_changed.id).values(title=book_changed.title,
                                                                                    author=book_changed.author)
            session.execute(to_do)

            #new_book = book
            #session.delete(book)
            #new_book.title = book_changed.title
            #new_book.author = book_changed.author
            #session.add(new_book)  # в alchemy
            session.commit()  # добавляем в бд все выше (сразу)
            return {"Данные обновлены"}
        else:
            return {f"Книги с id {book_changed.id} нет"}



# удалить книгу
@router.delete("/{book_id}", tags=["Книги"], summary="Удалить книгу")
def delete_book(book_deleted: DeleteBook, session: SessionDep):
    query = select(BookModel)
    result = session.execute(query)
    books = result.scalars().all()
    last_id = len(books)
    flag = 0
    for book in books:
        if book.id == book_deleted.id:
            flag = 1
    if flag == 1:
        to_do = delete(BookModel).where(BookModel.id == book_deleted.id)
        session.execute(to_do)
        if book_deleted.id != last_id:
            to_do2 = update(BookModel).where(BookModel.id == last_id).values(id=book_deleted.id)
            session.execute(to_do2)
        session.commit()
        return {"Книга удалена"}
    else:
        return {f"Книги с id {book_deleted.id} нет"}


