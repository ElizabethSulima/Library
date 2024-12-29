import fastapi as fa
from core import dependency
from schemas import author as sa
from services.author import AuthorServices


author_router = fa.APIRouter(
    prefix="/authors",
    tags=["authors"],
)


@author_router.get("/", response_model=list[sa.AuthorResponse])
async def get_authors(session: dependency.AsyncSessionDepency):
    return await AuthorServices(session).get_authors()


@author_router.get("/{author_id}/", response_model=sa.AuthorResponse)
async def get_author_id(
    author_id: int, session: dependency.AsyncSessionDepency
):
    return await AuthorServices(session).get_author_by_id(author_id)


@author_router.post(
    "/",
    response_model=sa.AuthorResponse,
    status_code=fa.status.HTTP_201_CREATED,
)
async def create_author(
    session: dependency.AsyncSessionDepency,
    author_data: sa.AuthorCreate,
):
    return await AuthorServices(session).post_author(author_data)


@author_router.put("/{author_id}/", response_model=sa.AuthorResponse)
async def put_author(
    session: dependency.AsyncSessionDepency,
    author_id: int,
    author_data: sa.AuthorUpdate,
):
    return await AuthorServices(session).put_author(author_id, author_data)


@author_router.delete(
    "/{author_id}/",
    response_model=sa.AuthorResponse,
    status_code=fa.status.HTTP_200_OK,
)
async def delete_author(
    session: dependency.AsyncSessionDepency,
    author_id: int,
):
    await AuthorServices(session).delete_author(author_id)
    return fa.responses.JSONResponse(
        content="Author deleled", status_code=fa.status.HTTP_200_OK
    )
