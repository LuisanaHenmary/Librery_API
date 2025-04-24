from fastapi import (
    FastAPI,
    Request,
    Body,
    status,
    Path
)

from typing import List

from app.db import connect_to_db

from app.queries import (
    get_authors,
    create_author,
    get_categories,
    create_category,
    get_user_by_username,
    create_user,
    create_book,
    get_books,
    create_loan,
    get_loans,
    get_books_by_id,
    get_books_by_author,
    get_books_by_category,
    get_book_by_term,
    get_loan_by_user,
    update_book,
    delete_book
)


from datetime import timedelta
from app.auth import hash_password, verify_password, create_access_token

from models.author import Author, AuthorResponce
from models.category import Category, CategoryResponce
from models.user import UserAuth, UserRegister
from models.book import Book, BookResponce, UpdateBook
from models.loan import Loan, LoanResponce

from app.utils import Depends, get_current_user, require_admin, HTTPException
import os

app = FastAPI()

@app.on_event("startup")
async def startup():
    app.state.db = await connect_to_db()

@app.on_event("shutdown")
async def shutdown():
    await app.state.db.close()

# Default
@app.get("/")
async def get_start():
    return {
        "Documentacion": os.getenv('API_DOCS_URL'),
        "Note":"For endpoints with authentication use postman."
    }

# Users
@app.post(
    path="/register",
    status_code=status.HTTP_201_CREATED,
    tags=["Users"]
)
async def register_user(user: UserRegister, request: Request):

    """This path operation register a new user."""

    conn = request.app.state.db

    hashed = hash_password(user.password)

    return await create_user(
        conn,
        user.ci,
        user.username,
        user.email,
        user.phone_number,
        hashed
    )

@app.post(
    path="/login",
    status_code=status.HTTP_200_OK,
    tags=["Users"]
)
async def login_user(user: UserAuth, request: Request):
    """This path operation is to log in."""

    conn = request.app.state.db
    db_user = await get_user_by_username(conn, user.username)

    if not db_user or not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token(
        data={"sub": db_user["username"], "is_admin": db_user["is_admin"]},
        expires_delta=timedelta(minutes=30)
    )
    
    return {"access_token": token, "token_type": "bearer"}

@app.get(
    path="/me",
    status_code=status.HTTP_200_OK,
    tags=["Users"]
)
async def read_profile(user=Depends(get_current_user)):
    """This path operation is to look the user type and username."""
    return user

# Authors
@app.get(
    path="/authors",
    status_code=status.HTTP_200_OK,
    response_model=List[AuthorResponce],
    tags=["Authors"]
)
async def get_authors_list(request: Request):

    """This path operation shows all registered authors."""

    conn = request.app.state.db
    return await get_authors(conn)

@app.post(
    path="/authors",
    status_code=status.HTTP_201_CREATED,
    response_model=AuthorResponce,
    tags=["Authors"]
)
async def add_author(author: Author, request: Request, user=Depends(require_admin)):

    """This path operation register a new author."""
    conn = request.app.state.db
    return await create_author(conn, author.name)

# Categories
@app.get(
    path="/categories",
    status_code=status.HTTP_200_OK,
    response_model=List[CategoryResponce],
    tags=["Categories"]
)
async def get_categories_list(request: Request):

    """This path operation shows all registered categories."""

    conn = request.app.state.db
    return await get_categories(conn)

@app.post(
    path="/categories",
    status_code=status.HTTP_201_CREATED,
    response_model=CategoryResponce,
    tags=["Categories"]
)
async def add_category(category: Category, request: Request, user=Depends(require_admin)):

    """This path operation register a new category."""

    conn = request.app.state.db
    return await create_category(conn, category.name)

# Books
@app.get(
    path="/books",
    status_code=status.HTTP_200_OK,
    response_model=List[BookResponce],
    tags=["Books"]
)
async def get_books_list(request: Request):
    """This path operation shows all registered books."""
    conn = request.app.state.db
    return await get_books(conn)

@app.post(
    path="/books",
    status_code=status.HTTP_201_CREATED,
    response_model=BookResponce,
    tags=["Books"]
)
async def add_book(
    request: Request,
    book: Book = Body(...),
    user=Depends(require_admin)
):
    """This path operation register a new book."""
    conn = request.app.state.db
    return await create_book(conn, book)
    
@app.put(
    path="/books/{id}",
    status_code=status.HTTP_200_OK,
    response_model=BookResponce,
    tags=["Books"]
)
async def update_a_book(
    request: Request,
    id: int = Path(
        ...,
        title="Book ID",
        description="It is the ID of one of many books"
    ),
    book: UpdateBook = Body(...),
    user=Depends(require_admin)
):
    """This path operation update a specific book."""
    conn = request.app.state.db
    return await update_book(conn, id, book)

@app.delete(
    path="/books/{id}",
    status_code=status.HTTP_200_OK,
    tags=["Books"]
)
async def delete_a_book(
    request: Request,
    id: int = Path(
        ...,
        title="Book ID",
        description="It is the ID of one of many books"
    ),
    user=Depends(require_admin)
):
    """This path operation remove a specific book."""
    conn = request.app.state.db
    return await delete_book(conn, id)

# Loans

@app.get(
    path="/loans",
    status_code=status.HTTP_200_OK,
    response_model=List[LoanResponce],
    tags=["Loans"]
)
async def get_loans_list(
    request: Request,
    user=Depends(require_admin)
):
    """This path operation shows all registered loans."""
    conn = request.app.state.db
    return await get_loans(conn)

@app.post(
    path="/loans",
    status_code=status.HTTP_201_CREATED,
    response_model=LoanResponce,
    tags=["Loans"]
)
async def add_loan(
    request: Request,
    loan: Loan = Body(...),
    user=Depends(require_admin)
):
    """This path operation register a new loan."""
    conn = request.app.state.db
    return await create_loan(conn, loan)
    
# Search

@app.get(
    path="/books/{id}",
    status_code=status.HTTP_200_OK,
    response_model=List[BookResponce],
    tags=["Books","Search"]
)
async def get_books_list_by_id(
    request: Request,
    id: int = Path(
        ...,
        title="Book ID",
        description="It is the ID of one of many books"
    ),
    user=Depends(get_current_user)
):
    """This path operation shows a specific book."""
    conn = request.app.state.db
    return await get_books_by_id(conn, id)

@app.get(
    path="/authors/{author_id}/books",
    status_code=status.HTTP_200_OK,
    response_model=List[BookResponce],
    tags=["Books", "Authors","Search"]
)
async def get_books_list_by_author(
    request: Request,
    author_id: int = Path(
        ...,
        title="Author ID",
        description="It is the ID of one of many authors"
    ),
    user=Depends(get_current_user)
):
    """This path operation shows all registered books of a specific author."""
    conn = request.app.state.db
    return await get_books_by_author(conn, author_id)


@app.get(
    path="/categories/{id_category}/books",
    status_code=status.HTTP_200_OK,
    response_model=List[BookResponce],
    tags=["Books", "Categories","Search"]
)
async def get_books_list_by_category(
    request: Request,
    id_category: int = Path(
        ...,
        title="Category ID",
        description="It is the ID of one of many categories"
    ),
    user=Depends(get_current_user)
):
    """This path operation shows all registered books of a specific category."""
    conn = request.app.state.db
    return await get_books_by_category(conn, id_category)

@app.get(
    path="/books/search",
    status_code=status.HTTP_200_OK,
    response_model=List[BookResponce],
    tags=["Books", "Search"]
)
async def search_books_by_term(
    request: Request,
    title: str = "",
    user=Depends(get_current_user)
):
    """This path operation shows all registered books by a term."""
    conn = request.app.state.db
    return await get_book_by_term(conn, title)

@app.get(
    path="/users/{id_user}/loans",
    status_code=status.HTTP_200_OK,
    response_model=List[LoanResponce],
    tags=["Users", "Loans","Search"]
)
async def get_loans_list_by_user(
    request: Request,
    id_user: int = Path(
        ...,
        title="User ID",
        description="It is the ID of one of many users"
    ),
    user=Depends(require_admin)
):
    """This path operation shows all registered loans of a specific user."""
    conn = request.app.state.db
    return await get_loan_by_user(conn, id_user)
