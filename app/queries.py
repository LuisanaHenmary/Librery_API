async def get_authors(conn):
    rows = await conn.fetch("SELECT * FROM author")
    return [dict(row) for row in rows]

async def create_author(conn, name):
    query = """
    INSERT INTO author (name)
    VALUES ($1)
    RETURNING id, name
    """
    row = await conn.fetchrow(query, name)
    return dict(row)


async def get_categories(conn):
    rows = await conn.fetch("SELECT * FROM category")
    return [dict(row) for row in rows]

async def create_category(conn, name):
    query = """
    INSERT INTO category (name)
    VALUES ($1)
    RETURNING id, name
    """
    row = await conn.fetchrow(query, name)
    return dict(row)

async def get_user_by_name(conn, name: str):
    query = "SELECT * FROM users WHERE name = $1"
    row = await conn.fetchrow(query, name)
    return dict(row) if row else None

async def create_user(
        conn,
        ci: str,
        name: str,
        email: str,
        phone_number,
        hashed_password: str,
        is_admin=False
        ):
    
    query = """
    INSERT INTO users (name, ci, phone_number, email, is_admin, hashed_password)
    VALUES ($1, $2, $3, $4, $5, $6)
    RETURNING id, name, ci, phone_number, email
    """
    row = await conn.fetchrow(query, name, ci, phone_number, email, is_admin, hashed_password)
    return dict(row)
