import fastapi as fa
from core import dependency
from schemas import borrow as sb
from services.borrow import BorrowServices


borrow_router = fa.APIRouter(
    prefix="/borrows",
    tags=["borrows"],
)


@borrow_router.get("/", response_model=list[sb.BorrowResponse])
async def get_borrows(session: dependency.AsyncSessionDepency):
    return await BorrowServices(session).get_borrows()


@borrow_router.get("/{borrow_id}/", response_model=sb.BorrowResponse)
async def get_borrow_id(
    borrow_id: int, session: dependency.AsyncSessionDepency
):
    return await BorrowServices(session).get_borrow_by_id(borrow_id)


@borrow_router.post(
    "/",
    response_model=sb.BorrowResponse,
    status_code=fa.status.HTTP_201_CREATED,
)
async def create_borrow(
    session: dependency.AsyncSessionDepency,
    borrow_data: sb.BorrowCreate,
):
    return await BorrowServices(session).post_borrow(borrow_data)


@borrow_router.patch("/{borrow_id}/return/", response_model=sb.BorrowResponse)
async def patch_borrow(
    session: dependency.AsyncSessionDepency,
    borrow_id: int,
):
    return await BorrowServices(session).patch_borrow(borrow_id)
