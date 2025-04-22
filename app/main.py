from fastapi import (
    FastAPI,
    Request,
    Body,
    status
)
from app.db import connect_to_db
from app.queries import (
    get_authors,
    create_author,
    get_categories,
    create_category,
    get_user_by_name,
    create_user,
    create_book,
    get_books
)

from datetime import timedelta
from app.auth import hash_password, verify_password, create_access_token

from models.author import Author
from models.category import Category
from models.user import UserLogin, UserRegister
from models.book import Book

from app.utils import Depends, get_current_user, require_admin, HTTPException

app = FastAPI()

@app.on_event("startup")
async def startup():
    app.state.db = await connect_to_db()

@app.on_event("shutdown")
async def shutdown():
    await app.state.db.close()


@app.get("/")
async def get_start():
    return "hello"

@app.get("/authors")
async def get_authors_list(request: Request):
    conn = request.app.state.db
    return await get_authors(conn)

@app.post("/authors")
async def add_author(author: Author, request: Request, user=Depends(require_admin)):
    conn = request.app.state.db
    return await create_author(conn, author.name)

@app.get("/categories")
async def get_categories_list(request: Request):
    conn = request.app.state.db
    return await get_categories(conn)

@app.post("/categories")
async def add_category(category: Category, request: Request, user=Depends(require_admin)):
    conn = request.app.state.db
    return await create_category(conn, category.name)

@app.post("/register")
async def register_user(user: UserRegister, request: Request):
    conn = request.app.state.db
    existing_user = await get_user_by_name(conn, user.name)

    if existing_user:
        raise HTTPException(status_code=400, detail="Usuario ya existe")
    
    hashed = hash_password(user.password)
    return await create_user(
        conn,
        user.ci,
        user.name,
        user.email,
        user.phone_number,
        hashed
        )

@app.post("/login")
async def login_user(user: UserLogin, request: Request):
    conn = request.app.state.db
    db_user = await get_user_by_name(conn, user.name)

    if not db_user or not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    token = create_access_token(
        data={"sub": db_user["name"], "is_admin": db_user["is_admin"]},
        expires_delta=timedelta(minutes=30)
    )
    return {"access_token": token, "token_type": "bearer"}

@app.get("/me")
async def read_profile(user=Depends(get_current_user)):
    return user

@app.get(
        path="/books",
        status_code=status.HTTP_200_OK,
        tags=["Book"]
        )
async def get_books_list(request: Request):
    conn = request.app.state.db
    return await get_books(conn)

@app.post(
        path="/books",
        status_code=status.HTTP_201_CREATED,
        tags=["Book"]
    )
async def add_book(
    request: Request,
    book: Book = Body(...),
    user=Depends(require_admin)
    ):
    conn = request.app.state.db
    return await create_book(conn, book)
