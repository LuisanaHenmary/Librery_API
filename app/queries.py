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
