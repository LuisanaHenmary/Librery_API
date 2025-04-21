from fastapi import FastAPI, Request
from app.db import connect_to_db
from app.queries import get_authors, create_author, get_categories, create_category

from models.author import Author
from models.category import Category

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
async def add_book(author: Author, request: Request):
    conn = request.app.state.db
    return await create_author(conn, author.name)

@app.get("/categories")
async def get_categories_list(request: Request):
    conn = request.app.state.db
    return await get_categories(conn)

@app.post("/categories")
async def add_category(category: Category, request: Request):
    conn = request.app.state.db
    return await create_category(conn, category.name)