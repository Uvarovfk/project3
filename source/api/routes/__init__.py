from fastapi import APIRouter
from source.api.books import router as books_router
from source.api.users import router as users_router
from source.api.reviews import router as review_router
from source.api.recomendation import router as recomendation_router

main_router = APIRouter()

main_router.include_router(books_router, prefix="/books")
main_router.include_router(users_router, prefix="/users")
main_router.include_router(review_router, prefix="/users")
main_router.include_router(recomendation_router, prefix="/users")