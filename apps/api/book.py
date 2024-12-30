import fastapi as fa
from core import dependency
from schemas import book as sb
from services.book import BookServices


book_router = fa.APIRouter(
    prefix="/books",
    tags=["books"],
)


@book_router.get("/", response_model=list[sb.Book])
async def get_books(session: dependency.AsyncSessionDepency):
    return await BookServices(session).get_books()


@book_router.get("/{book_id}/", response_model=sb.Book)
async def get_book_id(book_id: int, session: dependency.AsyncSessionDepency):
    return await BookServices(session).get_book_by_id(book_id)


@book_router.post(
    "/",
    response_model=sb.BookResponse,
    status_code=fa.status.HTTP_201_CREATED,
)
async def create_book(
    session: dependency.AsyncSessionDepency,
    book_data: sb.BookCreate,
):
    return await BookServices(session).post_book(book_data)


@book_router.put("/{book_id}/", response_model=sb.BookUpdate)
async def put_book(
    session: dependency.AsyncSessionDepency,
    book_id: int,
    book_data: sb.BookUpdate,
):
    return await BookServices(session).put_book(book_id, book_data)


@book_router.delete(
    "/{book_id}/",
    response_model=sb.BookResponse,
    status_code=fa.status.HTTP_200_OK,
)
async def delete_book(
    session: dependency.AsyncSessionDepency,
    book_id: int,
):
    await BookServices(session).delete_book(book_id)
    return fa.responses.JSONResponse(
        content="Book deleled", status_code=fa.status.HTTP_200_OK
    )
