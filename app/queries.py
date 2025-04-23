from fastapi import HTTPException
from asyncpg.exceptions import UniqueViolationError


# Author functions
async def get_authors(conn):

    rows = await conn.fetch("SELECT * FROM author")
    return [dict(row) for row in rows]

async def create_author(conn, name):

    row = None

    try:
        query = """
        INSERT INTO author (name)
        VALUES ($1)
        RETURNING id, name
        """
        row = await conn.fetchrow(query, name)

    except UniqueViolationError:
        raise HTTPException(status_code=400, detail="This author already exists")

    return dict(row)
    
# Category functions
async def get_categories(conn):
    rows = await conn.fetch("SELECT * FROM category")
    return [dict(row) for row in rows]

async def create_category(conn, name):

    row = None

    try:

        query = """
        INSERT INTO category (name)
        VALUES ($1)
        RETURNING id, name
        """
        row = await conn.fetchrow(query, name)

    except UniqueViolationError:
        raise HTTPException(status_code=400, detail="This category already exists")
    
    return dict(row)

# User functions
async def get_user_by_username(conn, username: str):
    query = "SELECT * FROM users WHERE username = $1"
    row = await conn.fetchrow(query, username)
    return dict(row) if row else None

async def create_user(
    conn,
    ci: str,
    username: str,
    email: str,
    phone_number,
    hashed_password: str,
    is_admin=False
):
    row = None

    try:

        query = """
        INSERT INTO users (username, ci, phone_number, email, is_admin, hashed_password)
        VALUES ($1, $2, $3, $4, $5, $6)
        RETURNING id, username, ci, phone_number, email
        """
        row = await conn.fetchrow(
            query,
            username,
            ci,
            phone_number,
            email,
            is_admin, 
            hashed_password
        )

    except UniqueViolationError:
        raise HTTPException(status_code=400, detail="This user or email already exists")

    return dict(row)

# Book functions
async def create_book(conn, book):

    row = None

    try:
        query = """
        INSERT INTO book (title, code, publish_date, edition, author_id, id_category)
        VALUES ($1, $2, $3, $4, $5, $6)
        RETURNING id, title, code, publish_date, edition, author_id, id_category
        """
        row = await conn.fetchrow(
        query,
        book.title,
        book.code,
        book.publish_date,
        book.edition,
        book.author_id,
        book.id_category
        )

    except UniqueViolationError:
        raise HTTPException(status_code=400, detail="This code for the book already exists")
    
    return dict(row)

async def get_books(conn):
    rows = await conn.fetch("SELECT * FROM book")
    return [dict(row) for row in rows]

async def get_books_by_author(conn, author_id):
    rows = await conn.fetch(f"SELECT * FROM book where author_id={author_id}")
    return [dict(row) for row in rows]

async def get_books_by_category(conn, id_category):
    rows = await conn.fetch(f"SELECT * FROM book where id_category={id_category}")
    return [dict(row) for row in rows]

async def get_books_by_id(conn, id):
    rows = await conn.fetch(f"SELECT * FROM book where id={id}")
    return [dict(row) for row in rows]

async def get_book_by_term(conn, search: str):
    query = """
    SELECT * FROM book
    WHERE LOWER(title) LIKE LOWER($1)
    """
    values = [f"%{search}%"]
    rows = await conn.fetch(query, *values)
    return [dict(row) for row in rows]

# Loan functions
async def create_loan(conn, loan):

    row = None

    try:
        query = """
        INSERT INTO loans (initial_date, delivere_date, id_user, id_book)
        VALUES ($1, $2, $3, $4)
        RETURNING id, initial_date, delivere_date, id_user, id_book, was_delivered_on_time
        """
        row = await conn.fetchrow(
            query,
            loan.initial_date,
            loan.delivere_date,
            loan.id_user,
            loan.id_book
        )

    except Exception:
        pass
    
    return dict(row)

async def get_loans(conn):
    rows = await conn.fetch("SELECT * FROM loans")
    return [dict(row) for row in rows]

async def get_loan_by_user(conn, id_user):
    rows = await conn.fetch(f"SELECT * FROM loans where id_user={id_user}")
    return [dict(row) for row in rows]
    